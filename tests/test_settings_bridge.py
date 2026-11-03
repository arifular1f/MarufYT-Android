"""Unit tests for MarufConfiguration and settings bridge."""
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from marufyt.settings_bridge import (
    CONFIG_VERSION,
    ConfigError,
    MarufConfiguration,
)


class SettingsBridgeTests(unittest.TestCase):
    def test_default_configuration_structure(self):
        config = MarufConfiguration()
        self.assertEqual(config.version, CONFIG_VERSION)
        self.assertEqual(config.general.theme, 'SYSTEM')
        self.assertEqual(config.player.default_playback_speed, 1.0)
        self.assertFalse(config.sponsorblock.enabled)
        self.assertEqual(config.sponsorblock.skip_mode, 'AUTOMATIC')
        self.assertFalse(config.privacy.telemetry_allowed)
        self.assertEqual(config.about.developer, 'arifular1f')

    def test_serialization_roundtrip(self):
        config = MarufConfiguration()
        config.general.theme = 'DARK'
        config.player.default_playback_speed = 1.5
        config.sponsorblock.enabled = True
        config.sponsorblock.categories = ['sponsor', 'selfpromo']
        config.tabs.hidden_tabs = ['Shorts']

        json_str = config.to_json()
        restored = MarufConfiguration.from_json(json_str)

        self.assertEqual(restored.general.theme, 'DARK')
        self.assertEqual(restored.player.default_playback_speed, 1.5)
        self.assertTrue(restored.sponsorblock.enabled)
        self.assertEqual(restored.sponsorblock.categories, ['sponsor', 'selfpromo'])
        self.assertEqual(restored.tabs.hidden_tabs, ['Shorts'])
        self.assertFalse(restored.privacy.telemetry_allowed)

    def test_export_and_import_bundle_verified(self):
        config = MarufConfiguration()
        config.general.amoled_black = True
        config.shorts.progress_bar_color = '#06B6D4'

        bundle = config.export_bundle()
        self.assertEqual(bundle['format'], 'marufyt-config-bundle')
        self.assertIn('checksum', bundle)

        imported = MarufConfiguration.import_bundle(bundle)
        self.assertTrue(imported.general.amoled_black)
        self.assertEqual(imported.shorts.progress_bar_color, '#06B6D4')

    def test_import_bundle_detects_tampering(self):
        config = MarufConfiguration()
        bundle = config.export_bundle()

        # Tamper with payload
        payload_dict = json.loads(bundle['payload'])
        payload_dict['general']['theme'] = 'TAMPERED'
        bundle['payload'] = json.dumps(payload_dict)

        with self.assertRaises(ConfigError):
            MarufConfiguration.import_bundle(bundle)

    def test_reject_unsupported_version(self):
        with self.assertRaises(ConfigError):
            MarufConfiguration.from_dict({'version': 999})

    def test_telemetry_always_false(self):
        # Even if data attempts to set telemetry_allowed=True, it is coerced to False
        data = {
            'version': CONFIG_VERSION,
            'privacy': {'telemetry_allowed': True, 'enable_diagnostics': False},
        }
        config = MarufConfiguration.from_dict(data)
        self.assertFalse(config.privacy.telemetry_allowed)


if __name__ == '__main__':
    unittest.main()
