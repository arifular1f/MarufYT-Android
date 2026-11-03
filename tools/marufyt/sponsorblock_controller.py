"""SponsorBlock playback controller and automatic skip manager.

Provides a safe, verified integration layer connecting active video identity,
continuous timeline tracking, configurable category skipping, seek debouncing,
and repeated-skip prevention. Designed to interface with YouTube Android playback
lifecycle without invoking dangerous low-level SABR callbacks.
"""
from dataclasses import dataclass, field
from enum import Enum
import math
import time
from typing import Optional

from .semantics import (
    PlaybackTimelineContract,
    SeekBoundaryContract,
    SemanticError,
    VideoIdentityContract,
)
from .sponsorblock import (
    CATEGORIES,
    Client,
    Segment,
    SponsorBlockError,
    seconds_to_milliseconds,
    video_id as validate_video_id_format,
)


class PlaybackState(Enum):
    STOPPED = 'STOPPED'
    BUFFERING = 'BUFFERING'
    PLAYING = 'PLAYING'
    PAUSED = 'PAUSED'
    ENDED = 'ENDED'


class SkipMode(Enum):
    AUTOMATIC = 'AUTOMATIC'
    ASK = 'ASK'
    OFF = 'OFF'


class SkipActionType(Enum):
    NONE = 'NONE'
    SKIP = 'SKIP'
    NOTIFY = 'NOTIFY'


@dataclass(frozen=True)
class SkipDecision:
    action: SkipActionType
    target_ms: int = 0
    segment: Optional[Segment] = None
    reason: str = ''


@dataclass
class PlaybackSession:
    video_id: str
    duration_sec: float
    duration_ms: int
    segments: tuple[Segment, ...] = ()
    executed_skips: set[str] = field(default_factory=set)
    state: PlaybackState = PlaybackState.BUFFERING
    last_position_ms: int = 0
    last_seek_timestamp: float = 0.0


class SponsorBlockPlaybackController:
    """Manages active video SponsorBlock lifecycle, segment evaluation, and skip decisions."""

    DEFAULT_DEBOUNCE_MS = 250
    SEEK_TOLERANCE_MS = 50

    def __init__(
        self,
        client: Client,
        enabled_categories: tuple[str, ...] = ('sponsor', 'intro', 'outro'),
        skip_mode: SkipMode = SkipMode.AUTOMATIC,
        debounce_ms: int = DEFAULT_DEBOUNCE_MS,
        clock=time.monotonic,
    ):
        self.client = client
        self.enabled_categories = set(enabled_categories)
        self.skip_mode = skip_mode
        self.debounce_ms = max(50, debounce_ms)
        self.clock = clock
        self.active_session: Optional[PlaybackSession] = None

    def set_enabled_categories(self, categories: tuple[str, ...]):
        cats = set(categories)
        if not cats <= CATEGORIES:
            raise SponsorBlockError('Invalid categories in selection')
        self.enabled_categories = cats

    def set_skip_mode(self, mode: SkipMode):
        if not isinstance(mode, SkipMode):
            raise SponsorBlockError('Invalid skip mode')
        self.skip_mode = mode

    def on_video_started(
        self,
        candidate_video_id: str,
        duration_sec: float,
        is_active_playback: bool = True,
        is_preload: bool = False,
    ) -> bool:
        """Called when a video starts. Disambiguates active playback from preloads and fetches segments."""
        try:
            clean_id = VideoIdentityContract.disambiguate_context(
                candidate_video_id,
                is_active_playback=is_active_playback,
                is_preload=is_preload,
            )
            valid_duration = PlaybackTimelineContract.validate_duration(duration_sec)
        except SemanticError:
            self.active_session = None
            return False

        duration_ms = round(valid_duration * 1000)
        segments: tuple[Segment, ...] = ()

        if self.enabled_categories and self.skip_mode != SkipMode.OFF:
            try:
                raw_segments = self.client.lookup(
                    clean_id,
                    categories=tuple(sorted(self.enabled_categories)),
                    duration=valid_duration,
                )
                segments = tuple(raw_segments)
            except SponsorBlockError:
                # Network or parsing failure fails open: video plays normally without skipping
                segments = ()

        self.active_session = PlaybackSession(
            video_id=clean_id,
            duration_sec=valid_duration,
            duration_ms=duration_ms,
            segments=segments,
            executed_skips=set(),
            state=PlaybackState.PLAYING,
            last_position_ms=0,
            last_seek_timestamp=self.clock(),
        )
        return True

    def on_playback_state_changed(self, new_state: PlaybackState):
        if self.active_session:
            self.active_session.state = new_state

    def on_position_updated(self, current_pos_ms: int) -> SkipDecision:
        """Evaluates current playback position against active SponsorBlock segments."""
        if not self.active_session or self.active_session.state != PlaybackState.PLAYING:
            return SkipDecision(SkipActionType.NONE, reason='No active playing session')

        if self.skip_mode == SkipMode.OFF:
            return SkipDecision(SkipActionType.NONE, reason='SponsorBlock disabled')

        session = self.active_session
        session.last_position_ms = current_pos_ms

        now = self.clock()
        time_since_last_seek = (now - session.last_seek_timestamp) * 1000
        if time_since_last_seek < self.debounce_ms:
            return SkipDecision(SkipActionType.NONE, reason='Debounce active')

        for segment in session.segments:
            if segment.category not in self.enabled_categories:
                continue
            if segment.uuid in session.executed_skips:
                continue

            seg_start_ms = round(segment.start * 1000)
            seg_end_ms = round(segment.end * 1000)

            # Check if player position is within the segment
            if seg_start_ms <= current_pos_ms < seg_end_ms:
                # Clamp seek target to video duration
                target_ms = min(seg_end_ms, session.duration_ms)

                # Avoid redundant micro-seeks
                if abs(target_ms - current_pos_ms) < self.SEEK_TOLERANCE_MS:
                    continue

                if self.skip_mode == SkipMode.AUTOMATIC:
                    session.executed_skips.add(segment.uuid)
                    session.last_seek_timestamp = now
                    return SkipDecision(
                        action=SkipActionType.SKIP,
                        target_ms=target_ms,
                        segment=segment,
                        reason=f'Auto-skip segment [{seg_start_ms}ms - {seg_end_ms}ms] ({segment.category})',
                    )
                elif self.skip_mode == SkipMode.ASK:
                    return SkipDecision(
                        action=SkipActionType.NOTIFY,
                        target_ms=target_ms,
                        segment=segment,
                        reason=f'Prompt skip for segment [{seg_start_ms}ms - {seg_end_ms}ms] ({segment.category})',
                    )

        return SkipDecision(SkipActionType.NONE, reason='No active segment at current position')

    def confirm_manual_skip(self, segment_uuid: str) -> SkipDecision:
        """Executes a user-confirmed skip from an ASK notification."""
        if not self.active_session:
            return SkipDecision(SkipActionType.NONE, reason='No active session')

        session = self.active_session
        for segment in session.segments:
            if segment.uuid == segment_uuid:
                session.executed_skips.add(segment.uuid)
                session.last_seek_timestamp = self.clock()
                target_ms = min(round(segment.end * 1000), session.duration_ms)
                return SkipDecision(
                    action=SkipActionType.SKIP,
                    target_ms=target_ms,
                    segment=segment,
                    reason=f'Manual user skip confirmed for {segment_uuid}',
                )

        return SkipDecision(SkipActionType.NONE, reason='Segment UUID not found in session')

    def on_video_ended(self):
        """Cleans up session upon playback completion."""
        self.active_session = None
