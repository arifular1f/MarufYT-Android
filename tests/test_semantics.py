"""Unit tests for semantic validation data-flow contracts."""
import math
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from marufyt.semantics import (
    EXO_TIME_UNSET,
    TIME_POSITIVE_INFINITY,
    TIMESCALE_MICROS,
    TIMESCALE_MILLIS,
    FeatureFeasibility,
    FEATURE_ASSESSMENTS,
    PlaybackTimelineContract,
    SemanticError,
    SeekBoundaryContract,
    ShortsProgressContract,
    VideoIdentityContract,
)


class PlaybackTimelineContractTests(unittest.TestCase):
    def test_sentinel_detection(self):
        self.assertTrue(PlaybackTimelineContract.is_sentinel(EXO_TIME_UNSET))
        self.assertTrue(PlaybackTimelineContract.is_sentinel(TIME_POSITIVE_INFINITY))
        self.assertFalse(PlaybackTimelineContract.is_sentinel(0))
        self.assertFalse(PlaybackTimelineContract.is_sentinel(1000000))

    def test_ticks_to_seconds_valid(self):
        # 1,500,000 micros with 1,000,000 scale = 1.5s
        self.assertAlmostEqual(PlaybackTimelineContract.ticks_to_seconds(1_500_000, TIMESCALE_MICROS), 1.5)
        # 2,500 millis with 1,000 scale = 2.5s
        self.assertAlmostEqual(PlaybackTimelineContract.ticks_to_seconds(2_500, TIMESCALE_MILLIS), 2.5)
        # 0 ticks = 0.0s
        self.assertEqual(PlaybackTimelineContract.ticks_to_seconds(0, TIMESCALE_MICROS), 0.0)

    def test_ticks_to_seconds_rejects_invalid(self):
        # Sentinels
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.ticks_to_seconds(EXO_TIME_UNSET, TIMESCALE_MICROS)
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.ticks_to_seconds(TIME_POSITIVE_INFINITY, TIMESCALE_MICROS)
        # Negative ticks
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.ticks_to_seconds(-100, TIMESCALE_MICROS)
        # Zero or negative timescale
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.ticks_to_seconds(100, 0)
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.ticks_to_seconds(100, -1000)
        # Booleans or non-integers
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.ticks_to_seconds(True, TIMESCALE_MICROS)
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.ticks_to_seconds(100, False)
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.ticks_to_seconds('100', 1000)

    def test_micros_to_millis(self):
        self.assertEqual(PlaybackTimelineContract.micros_to_millis(1_000_000), 1000)
        self.assertEqual(PlaybackTimelineContract.micros_to_millis(1_234_567), 1235)
        self.assertEqual(PlaybackTimelineContract.micros_to_millis(0), 0)
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.micros_to_millis(-1)
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.micros_to_millis(EXO_TIME_UNSET)

    def test_validate_duration(self):
        self.assertEqual(PlaybackTimelineContract.validate_duration(120.5), 120.5)
        self.assertEqual(PlaybackTimelineContract.validate_duration(86400), 86400.0)
        # Zero or negative
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.validate_duration(0)
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.validate_duration(-10)
        # NaN or Inf
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.validate_duration(float('nan'))
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.validate_duration(float('inf'))
        # Over 24 hours
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.validate_duration(86401)
        # Booleans
        with self.assertRaises(SemanticError):
            PlaybackTimelineContract.validate_duration(True)


class VideoIdentityContractTests(unittest.TestCase):
    def test_valid_video_id(self):
        self.assertEqual(VideoIdentityContract.validate_video_id('dQw4w9WgXcQ'), 'dQw4w9WgXcQ')
        self.assertEqual(VideoIdentityContract.validate_video_id('abcdefghijk'), 'abcdefghijk')
        self.assertEqual(VideoIdentityContract.validate_video_id('  dQw4w9WgXcQ  '), 'dQw4w9WgXcQ')

    def test_invalid_video_id(self):
        for invalid in ('', None, 'too_short', 'too_long_video_id_123', 'bad!chars@@', 12345):
            with self.subTest(invalid=invalid), self.assertRaises(SemanticError):
                VideoIdentityContract.validate_video_id(invalid)

    def test_disambiguate_context(self):
        # Valid active playback
        vid = 'dQw4w9WgXcQ'
        self.assertEqual(VideoIdentityContract.disambiguate_context(vid, is_active_playback=True, is_preload=False), vid)

        # Inactive or background instance
        with self.assertRaises(SemanticError):
            VideoIdentityContract.disambiguate_context(vid, is_active_playback=False, is_preload=False)

        # Preload instance
        with self.assertRaises(SemanticError):
            VideoIdentityContract.disambiguate_context(vid, is_active_playback=True, is_preload=True)


class SeekBoundaryContractTests(unittest.TestCase):
    def test_valid_seek_target(self):
        # Seek from 1000ms to 5000ms in a 10000ms video
        self.assertEqual(SeekBoundaryContract.validate_seek_target(5000, 10000, 1000), 5000)
        # Seek to 0
        self.assertEqual(SeekBoundaryContract.validate_seek_target(0, 10000, 1000), 0)
        # Seek to end
        self.assertEqual(SeekBoundaryContract.validate_seek_target(10000, 10000, 1000), 10000)

    def test_invalid_seek_target(self):
        # Target beyond duration
        with self.assertRaises(SemanticError):
            SeekBoundaryContract.validate_seek_target(10001, 10000, 1000)
        # Negative target
        with self.assertRaises(SemanticError):
            SeekBoundaryContract.validate_seek_target(-1, 10000, 1000)
        # Redundant micro-seek within 50ms
        with self.assertRaises(SemanticError):
            SeekBoundaryContract.validate_seek_target(1020, 10000, 1000)
        # Non-integers / booleans
        with self.assertRaises(SemanticError):
            SeekBoundaryContract.validate_seek_target(True, 10000, 1000)
        with self.assertRaises(SemanticError):
            SeekBoundaryContract.validate_seek_target(5000, 0, 1000)


class ShortsProgressContractTests(unittest.TestCase):
    def test_calculate_progress_ratio(self):
        self.assertAlmostEqual(ShortsProgressContract.calculate_progress_ratio(5000, 10000), 0.5)
        self.assertAlmostEqual(ShortsProgressContract.calculate_progress_ratio(0, 10000), 0.0)
        self.assertAlmostEqual(ShortsProgressContract.calculate_progress_ratio(10000, 10000), 1.0)
        # Clamped ratio if position slightly exceeds duration
        self.assertAlmostEqual(ShortsProgressContract.calculate_progress_ratio(10500, 10000), 1.0)

    def test_invalid_shorts_progress(self):
        with self.assertRaises(SemanticError):
            ShortsProgressContract.calculate_progress_ratio(-1, 10000)
        with self.assertRaises(SemanticError):
            ShortsProgressContract.calculate_progress_ratio(5000, 0)
        with self.assertRaises(SemanticError):
            ShortsProgressContract.calculate_progress_ratio(5000, -100)


class FeatureAssessmentMatrixTests(unittest.TestCase):
    def test_thirteen_features_present(self):
        expected_features = {
            'SponsorBlock', 'BackgroundAudio', 'VideoQuality', 'Captions',
            'Gestures', 'WatchPage', 'HomeFeed', 'Shorts', 'Tabs', 'TopBar',
            'Downloads', 'GeneralSettings', 'PrivacySettings'
        }
        self.assertEqual(set(FEATURE_ASSESSMENTS.keys()), expected_features)

    def test_feasibility_classifications(self):
        # Settings should be standalone feasible
        self.assertEqual(FEATURE_ASSESSMENTS['GeneralSettings'].feasibility, FeatureFeasibility.FEASIBLE_STANDALONE)
        self.assertEqual(FEATURE_ASSESSMENTS['PrivacySettings'].feasibility, FeatureFeasibility.FEASIBLE_STANDALONE)

        # Background audio should be blocked by entitlement
        self.assertEqual(FEATURE_ASSESSMENTS['BackgroundAudio'].feasibility, FeatureFeasibility.BLOCKED_ENTITLEMENT)

        # Downloads should be blocked by DRM
        self.assertEqual(FEATURE_ASSESSMENTS['Downloads'].feasibility, FeatureFeasibility.BLOCKED_PROPRIETARY_DRM)

        # HomeFeed should be blocked by lack of injection point
        self.assertEqual(FEATURE_ASSESSMENTS['HomeFeed'].feasibility, FeatureFeasibility.BLOCKED_NO_INJECTION_POINT)

        # SponsorBlock, VideoQuality, Captions, Gestures, Shorts, Tabs, TopBar require hooks
        for f in ('SponsorBlock', 'VideoQuality', 'Captions', 'Gestures', 'Shorts', 'Tabs', 'TopBar'):
            self.assertEqual(FEATURE_ASSESSMENTS[f].feasibility, FeatureFeasibility.FEASIBLE_WITH_HOOKS)


if __name__ == '__main__':
    unittest.main()
