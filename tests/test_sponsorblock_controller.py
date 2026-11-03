"""Unit tests for SponsorBlock playback controller and skip logic."""
from unittest.mock import Mock
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from marufyt.sponsorblock import Client, Segment, SponsorBlockError
from marufyt.sponsorblock_controller import (
    PlaybackState,
    SkipActionType,
    SkipMode,
    SponsorBlockPlaybackController,
)

VIDEO = 'dQw4w9WgXcQ'


def mock_segment(start=10.0, end=25.0, cat='sponsor', uuid='seg-1'):
    return Segment(start=start, end=end, category=cat, uuid=uuid)


class SponsorBlockPlaybackControllerTests(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(spec=Client)
        self.mock_client.lookup.return_value = (
            mock_segment(start=10.0, end=20.0, cat='sponsor', uuid='uuid-sponsor'),
            mock_segment(start=50.0, end=65.0, cat='intro', uuid='uuid-intro'),
        )
        self.current_time = 1000.0
        self.controller = SponsorBlockPlaybackController(
            client=self.mock_client,
            enabled_categories=('sponsor', 'intro', 'outro'),
            skip_mode=SkipMode.AUTOMATIC,
            debounce_ms=250,
            clock=lambda: self.current_time,
        )

    def test_on_video_started_active_playback(self):
        success = self.controller.on_video_started(VIDEO, duration_sec=120.0, is_active_playback=True)
        self.assertTrue(success)
        self.assertIsNotNone(self.controller.active_session)
        self.assertEqual(len(self.controller.active_session.segments), 2)
        self.assertEqual(self.controller.active_session.duration_ms, 120000)

    def test_on_video_started_rejects_preload(self):
        success = self.controller.on_video_started(VIDEO, duration_sec=120.0, is_preload=True)
        self.assertFalse(success)
        self.assertIsNone(self.controller.active_session)

    def test_on_video_started_rejects_inactive(self):
        success = self.controller.on_video_started(VIDEO, duration_sec=120.0, is_active_playback=False)
        self.assertFalse(success)
        self.assertIsNone(self.controller.active_session)

    def test_network_failure_fails_open(self):
        self.mock_client.lookup.side_effect = SponsorBlockError('Network timeout')
        success = self.controller.on_video_started(VIDEO, duration_sec=120.0)
        self.assertTrue(success)
        self.assertEqual(len(self.controller.active_session.segments), 0)

    def test_auto_skip_trigger(self):
        self.controller.on_video_started(VIDEO, duration_sec=120.0)

        # Position before segment: 5000ms -> NONE
        decision = self.controller.on_position_updated(5000)
        self.assertEqual(decision.action, SkipActionType.NONE)

        # Position inside first segment (10s - 20s): 12000ms -> SKIP to 20000ms
        self.current_time += 1.0  # Advance past debounce
        decision = self.controller.on_position_updated(12000)
        self.assertEqual(decision.action, SkipActionType.SKIP)
        self.assertEqual(decision.target_ms, 20000)
        self.assertEqual(decision.segment.uuid, 'uuid-sponsor')

    def test_prevent_repeated_skips(self):
        self.controller.on_video_started(VIDEO, duration_sec=120.0)
        self.current_time += 1.0

        # First trigger skips
        decision = self.controller.on_position_updated(15000)
        self.assertEqual(decision.action, SkipActionType.SKIP)

        # Immediate subsequent position update within same segment does not re-skip
        self.current_time += 1.0
        decision = self.controller.on_position_updated(16000)
        self.assertEqual(decision.action, SkipActionType.NONE)

    def test_debounce_guard(self):
        self.controller.on_video_started(VIDEO, duration_sec=120.0)
        self.current_time += 1.0

        # Trigger skip
        decision = self.controller.on_position_updated(12000)
        self.assertEqual(decision.action, SkipActionType.SKIP)

        # Rapid update within 100ms (< 250ms debounce)
        self.current_time += 0.1
        decision = self.controller.on_position_updated(55000)
        self.assertEqual(decision.action, SkipActionType.NONE)
        self.assertIn('Debounce', decision.reason)

        # After debounce expires (0.3s later), second segment (50s - 65s) triggers
        self.current_time += 0.3
        decision = self.controller.on_position_updated(55000)
        self.assertEqual(decision.action, SkipActionType.SKIP)
        self.assertEqual(decision.target_ms, 65000)

    def test_ask_mode_prompts_notification(self):
        self.controller.set_skip_mode(SkipMode.ASK)
        self.controller.on_video_started(VIDEO, duration_sec=120.0)
        self.current_time += 1.0

        decision = self.controller.on_position_updated(12000)
        self.assertEqual(decision.action, SkipActionType.NOTIFY)
        self.assertEqual(decision.target_ms, 20000)

        # Confirming manual skip
        confirm = self.controller.confirm_manual_skip('uuid-sponsor')
        self.assertEqual(confirm.action, SkipActionType.SKIP)
        self.assertEqual(confirm.target_ms, 20000)

    def test_disabled_category_is_ignored(self):
        self.controller.set_enabled_categories(('intro',))
        self.controller.on_video_started(VIDEO, duration_sec=120.0)
        self.current_time += 1.0

        # Position in sponsor segment (not enabled)
        decision = self.controller.on_position_updated(15000)
        self.assertEqual(decision.action, SkipActionType.NONE)

        # Position in intro segment (enabled)
        decision = self.controller.on_position_updated(55000)
        self.assertEqual(decision.action, SkipActionType.SKIP)


if __name__ == '__main__':
    unittest.main()
