"""Semantic validation and data-flow contracts for YouTube Android internals.

Provides evidence-backed models and verification rules for video identity,
playback timeline, seek boundaries, Shorts progress, and feature feasibility
derived from APK structural analysis. No runtime injection or proprietary code.
"""
from dataclasses import dataclass
from enum import Enum
import math
import re

# Standard YouTube 11-character video ID regex
VIDEO_ID_REGEX = re.compile(r'^[A-Za-z0-9_-]{11}$')

# ExoPlayer / YouTube internal sentinel timestamps (microsecond scale)
EXO_TIME_UNSET = -0x7FFFFFFFFFFFFFFF
TIME_POSITIVE_INFINITY = 0x7FFFFFFFFFFFFFFF
TIMESCALE_MICROS = 1_000_000
TIMESCALE_MILLIS = 1_000


class SemanticError(ValueError):
    """Raised when data violates verified structural or timing contracts."""
    pass


class FeatureFeasibility(Enum):
    """Classification of Android feature integration readiness."""
    FEASIBLE_STANDALONE = 'FEASIBLE_STANDALONE'
    FEASIBLE_WITH_HOOKS = 'FEASIBLE_WITH_HOOKS'
    BLOCKED_ENTITLEMENT = 'BLOCKED_ENTITLEMENT'
    BLOCKED_NO_INJECTION_POINT = 'BLOCKED_NO_INJECTION_POINT'
    BLOCKED_PROPRIETARY_DRM = 'BLOCKED_PROPRIETARY_DRM'


@dataclass(frozen=True)
class FeatureAssessment:
    name: str
    feasibility: FeatureFeasibility
    required_preconditions: tuple[str, ...]
    blocking_reasons: tuple[str, ...]
    candidate_symbols: tuple[str, ...]


class PlaybackTimelineContract:
    """Validates rational time conversions and sentinel handling matching

    com.google.android.libraries.youtube.media.interfaces.Time.
    """

    @staticmethod
    def is_sentinel(ticks: int) -> bool:
        """Checks if tick count matches an ExoPlayer/YouTube sentinel value."""
        return ticks in (EXO_TIME_UNSET, TIME_POSITIVE_INFINITY)

    @staticmethod
    def ticks_to_seconds(ticks: int, timescale: int) -> float:
        """Converts integer ticks and timescale to finite seconds.

        Rejects non-integers, sentinels, negative values, and non-positive timescales.
        """
        if isinstance(ticks, bool) or isinstance(timescale, bool):
            raise SemanticError('Boolean values are not valid timeline numbers')
        if not isinstance(ticks, int) or not isinstance(timescale, int):
            raise SemanticError('Ticks and timescale must be integers')
        if PlaybackTimelineContract.is_sentinel(ticks):
            raise SemanticError('Cannot convert sentinel tick value to playback seconds')
        if ticks < 0:
            raise SemanticError('Playback ticks cannot be negative')
        if timescale <= 0 or timescale > 2**63 - 1:
            raise SemanticError('Timescale must be a positive 63-bit integer')

        return ticks / timescale

    @staticmethod
    def micros_to_millis(micros: int) -> int:
        """Converts microseconds (timescale 1,000,000) to rounded milliseconds."""
        if isinstance(micros, bool) or not isinstance(micros, int):
            raise SemanticError('Microsecond timestamp must be an integer')
        if PlaybackTimelineContract.is_sentinel(micros):
            raise SemanticError('Cannot convert sentinel microseconds to milliseconds')
        if micros < 0:
            raise SemanticError('Microsecond timestamp cannot be negative')
        return round(micros / 1000)

    @staticmethod
    def validate_duration(duration_sec: float) -> float:
        """Validates that a video duration is finite, positive, and <= 24 hours."""
        if isinstance(duration_sec, bool) or not isinstance(duration_sec, (int, float)):
            raise SemanticError('Duration must be a real number')
        if not math.isfinite(duration_sec):
            raise SemanticError('Duration must be finite')
        if duration_sec <= 0:
            raise SemanticError('Duration must be strictly positive')
        if duration_sec > 86400:
            raise SemanticError('Duration exceeds 24-hour supported playback window')
        return float(duration_sec)


class VideoIdentityContract:
    """Validates video identity resolution contracts across DEX boundaries."""

    @staticmethod
    def validate_video_id(candidate: str | None) -> str:
        """Validates that candidate is an 11-character alphanumeric video ID."""
        if not candidate or not isinstance(candidate, str):
            raise SemanticError('Video ID must be a non-empty string')
        candidate = candidate.strip()
        if not VIDEO_ID_REGEX.match(candidate):
            raise SemanticError(f'Invalid video ID format: {candidate!r}')
        return candidate

    @staticmethod
    def disambiguate_context(video_id: str, is_active_playback: bool, is_preload: bool) -> str:
        """Ensures metadata from preload/feed instances is not treated as active playback."""
        clean_id = VideoIdentityContract.validate_video_id(video_id)
        if not is_active_playback:
            raise SemanticError('Inactive or background video model cannot supply active playback ID')
        if is_preload:
            raise SemanticError('Preload model instance cannot supply active playback ID')
        return clean_id


class SeekBoundaryContract:
    """Models constraints on seek operations to prevent seek storms or desync."""

    MIN_SEEK_INTERVAL_MS = 250  # Debounce interval to avoid hammering media source

    @staticmethod
    def validate_seek_target(target_ms: int, duration_ms: int, current_pos_ms: int) -> int:
        """Validates that seek target is within [0, duration] and not a redundant micro-seek."""
        if isinstance(target_ms, bool) or not isinstance(target_ms, int):
            raise SemanticError('Seek target must be an integer')
        if isinstance(duration_ms, bool) or not isinstance(duration_ms, int) or duration_ms <= 0:
            raise SemanticError('Duration must be a positive integer')
        if isinstance(current_pos_ms, bool) or not isinstance(current_pos_ms, int) or current_pos_ms < 0:
            raise SemanticError('Current position must be a nonnegative integer')

        if target_ms < 0:
            raise SemanticError('Seek target cannot be negative')
        if target_ms > duration_ms:
            raise SemanticError('Seek target exceeds duration')

        if abs(target_ms - current_pos_ms) < 50:
            raise SemanticError('Redundant seek: target within micro-seek threshold (< 50ms)')

        return target_ms


class ShortsProgressContract:
    """Validates Shorts progress presenter state and ratio calculations."""

    @staticmethod
    def calculate_progress_ratio(position_ms: int, duration_ms: int) -> float:
        """Calculates progress ratio clamped to [0.0, 1.0]."""
        if isinstance(position_ms, bool) or not isinstance(position_ms, int):
            raise SemanticError('Position must be an integer')
        if isinstance(duration_ms, bool) or not isinstance(duration_ms, int):
            raise SemanticError('Duration must be an integer')
        if duration_ms <= 0:
            raise SemanticError('Duration must be positive')
        if position_ms < 0:
            raise SemanticError('Position cannot be negative')

        ratio = position_ms / duration_ms
        return max(0.0, min(1.0, ratio))


# Comprehensive assessment matrix for all 13 Android feature areas
FEATURE_ASSESSMENTS: dict[str, FeatureAssessment] = {
    'SponsorBlock': FeatureAssessment(
        name='SponsorBlock',
        feasibility=FeatureFeasibility.FEASIBLE_WITH_HOOKS,
        required_preconditions=(
            'Active video ID resolution (disambiguated from feed/preload)',
            'Continuous playback clock observer (millisecond accuracy)',
            'Safe seekTo bridge (caller thread safety and debounce guard)',
            'User opt-in consent and category preference storage',
        ),
        blocking_reasons=(
            'Host player seek entry point is internal SABR onSabrSeek callback',
            'No public non-obfuscated seekTo method identified without active controller instance',
        ),
        candidate_symbols=(
            'Lcom/google/android/libraries/youtube/media/player/exo2/platypus/PlaybackControllerWrapper;->c()Lcom/google/android/libraries/youtube/media/interfaces/Time;',
            'Lbpnu;->getVideoId()Ljava/lang/String;',
        ),
    ),
    'BackgroundAudio': FeatureAssessment(
        name='BackgroundAudio',
        feasibility=FeatureFeasibility.BLOCKED_ENTITLEMENT,
        required_preconditions=(
            'BackgroundPlayerService lifecycle control',
            'AudioManager audio focus management',
            'Notification channel and media session integration',
        ),
        blocking_reasons=(
            'Service onStartCommand is gated by internal entitlement check in Lasll',
            'YouTube client pauses playback upon onPause/onStop activity lifecycle events',
            'Server-driven experiment flags enforce Premium subscription check',
        ),
        candidate_symbols=(
            'Lcom/google/android/libraries/youtube/player/background/service/BackgroundPlayerService;',
        ),
    ),
    'VideoQuality': FeatureAssessment(
        name='VideoQuality',
        feasibility=FeatureFeasibility.FEASIBLE_WITH_HOOKS,
        required_preconditions=(
            'Format selection model resolution',
            'ProtoDataStore or SharedPreferences preference synchronization',
        ),
        blocking_reasons=(
            'VideoQualityPrefsFragment XML handles only UI preferences, not stream engine override',
            'Dynamic ABR (Adaptive Bitrate) controller overrides fixed manual format on network jitter',
        ),
        candidate_symbols=(
            'Lcom/google/android/apps/youtube/app/settings/videoquality/VideoQualityPrefsFragment;->aS()V',
            'Lcom/google/android/libraries/youtube/media/player/exo2/platypus/PlaybackControllerWrapper;->j(Lcom/google/android/apps/youtube/proto/streaming/SelectableFormatsOuterClass$SelectableFormats;)V',
        ),
    ),
    'Captions': FeatureAssessment(
        name='Captions',
        feasibility=FeatureFeasibility.FEASIBLE_WITH_HOOKS,
        required_preconditions=(
            'SubtitleWindowView visibility binding',
            'CaptionMediaSegmentHolder stream interceptor',
        ),
        blocking_reasons=(
            'SubtitleWindowView only handles rendering dimensions, not track discovery or fetch',
        ),
        candidate_symbols=(
            'Lcom/google/android/libraries/youtube/player/subtitles/ui/SubtitleWindowView;',
            'Lcom/google/android/libraries/youtube/media/player/exo2/platypus/mediapush/CaptionMediaSegmentHolder;',
        ),
    ),
    'Gestures': FeatureAssessment(
        name='Gestures',
        feasibility=FeatureFeasibility.FEASIBLE_WITH_HOOKS,
        required_preconditions=(
            'Overlay touch event interception on YouTubePlayerOverlaysLayout',
            'Brightness and audio stream volume managers',
        ),
        blocking_reasons=(
            'Touch events are handled by multi-layered overlay views with conflicting swipe targets',
        ),
        candidate_symbols=(
            'Lcom/google/android/apps/youtube/app/common/player/overlay/YouTubePlayerOverlaysLayout;->dispatchTouchEvent(Landroid/view/MotionEvent;)Z',
            'Lcom/google/android/apps/youtube/app/watchwhile/MainActivity;->dispatchTouchEvent(Landroid/view/MotionEvent;)Z',
        ),
    ),
    'WatchPage': FeatureAssessment(
        name='WatchPage',
        feasibility=FeatureFeasibility.FEASIBLE_WITH_HOOKS,
        required_preconditions=(
            'WatchFeedResizeBehavior layout parameters',
            'Overlay visibility flags',
        ),
        blocking_reasons=(
            'Watch page layout is dynamically generated from Litho / Elements component trees',
        ),
        candidate_symbols=(
            'Lcom/google/android/apps/youtube/app/watch/nextgenwatch/overscroll/WatchFeedResizeBehavior;',
        ),
    ),
    'HomeFeed': FeatureAssessment(
        name='HomeFeed',
        feasibility=FeatureFeasibility.BLOCKED_NO_INJECTION_POINT,
        required_preconditions=(
            'Browse response model interceptor',
            'RecyclerView adapter filter',
        ),
        blocking_reasons=(
            'Feed items are served as protobuf Elements rendered natively; SnappyRecyclerView is a generic list view without filter hooks',
        ),
        candidate_symbols=(
            'Lcom/google/android/apps/youtube/app/common/rendering/SnappyRecyclerView;',
        ),
    ),
    'Shorts': FeatureAssessment(
        name='Shorts',
        feasibility=FeatureFeasibility.FEASIBLE_WITH_HOOKS,
        required_preconditions=(
            'ShortsPlayerProgressPresenter view modification or custom overlay',
            'ReelWatchPagerViewPager page change listener',
        ),
        blocking_reasons=(
            'Shorts auto-advance requires synthesizing swipe gestures on ReelRecyclerView',
        ),
        candidate_symbols=(
            'Lcom/google/android/apps/youtube/app/extensions/reel/shorts/ShortsPlayerProgressPresenter;',
            'Lcom/google/android/apps/youtube/app/extensions/reel/watch/fragment/ReelWatchPagerViewPager;',
        ),
    ),
    'Tabs': FeatureAssessment(
        name='Tabs',
        feasibility=FeatureFeasibility.FEASIBLE_WITH_HOOKS,
        required_preconditions=(
            'PivotBar tab enumeration and view hiding',
        ),
        blocking_reasons=(
            'Removing tabs requires intercepting PivotBar.c view creation and adjusting index mappings',
        ),
        candidate_symbols=(
            'Lcom/google/android/libraries/youtube/rendering/ui/pivotbar/PivotBar;',
            'Lcom/google/android/libraries/youtube/rendering/ui/hometabs/DefaultTabsBar;',
        ),
    ),
    'TopBar': FeatureAssessment(
        name='TopBar',
        feasibility=FeatureFeasibility.FEASIBLE_WITH_HOOKS,
        required_preconditions=(
            'MainCollapsingToolbarLayout child visibility control',
        ),
        blocking_reasons=(
            'Toolbar action icons are inflated dynamically based on account and cast state',
        ),
        candidate_symbols=(
            'Lcom/google/android/apps/youtube/app/ui/actionbar/MainCollapsingToolbarLayout;',
        ),
    ),
    'Downloads': FeatureAssessment(
        name='Downloads',
        feasibility=FeatureFeasibility.BLOCKED_PROPRIETARY_DRM,
        required_preconditions=(
            'Offline stream fetch and muxing pipeline',
        ),
        blocking_reasons=(
            'YouTube offline service uses Widevine DRM and encrypted storage',
            'No open download pipeline exists in YouTube Android codebase without external tools',
        ),
        candidate_symbols=(
            'Lcom/google/android/libraries/youtube/offline/transfer/service/OfflineKeepAliveService;',
        ),
    ),
    'GeneralSettings': FeatureAssessment(
        name='GeneralSettings',
        feasibility=FeatureFeasibility.FEASIBLE_STANDALONE,
        required_preconditions=(
            'Standalone settings activity or preferences injection',
        ),
        blocking_reasons=(),
        candidate_symbols=(
            'Lcom/google/android/apps/youtube/app/settings/SettingsActivity;',
        ),
    ),
    'PrivacySettings': FeatureAssessment(
        name='PrivacySettings',
        feasibility=FeatureFeasibility.FEASIBLE_STANDALONE,
        required_preconditions=(
            'Local private SharedPreferences and diagnostics control',
        ),
        blocking_reasons=(),
        candidate_symbols=(
            'Lcom/google/android/apps/youtube/app/settings/PrivacyPrefsFragment;',
        ),
    ),
}
