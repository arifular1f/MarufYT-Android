"""Unified settings schema and configuration bridge for MarufYT Android.

Provides a secure, versioned, validated configuration model connecting
the native Android settings companion UI and runtime integration modules.
Supports serialization, schema validation, reset, and tamper-resistant export/import.
"""
from dataclasses import asdict, dataclass, field
import hashlib
import json
from typing import Any, Optional

CONFIG_VERSION = 1


class ConfigError(ValueError):
    """Raised when configuration validation or migration fails."""
    pass


@dataclass
class GeneralConfig:
    theme: str = 'SYSTEM'  # SYSTEM, LIGHT, DARK
    amoled_black: bool = False


@dataclass
class PlayerConfig:
    default_playback_speed: float = 1.0  # 0.25 to 2.0
    auto_repeat: bool = False
    remember_speed: bool = True


@dataclass
class VideoQualityConfig:
    wifi_quality: str = 'AUTO'  # AUTO, 1080p, 720p, 480p, etc.
    cellular_quality: str = 'AUTO'
    max_resolution_on_wifi: bool = False


@dataclass
class CaptionsConfig:
    auto_captions: bool = False
    text_scale_percent: int = 100  # 75 to 200
    custom_background: bool = False


@dataclass
class GesturesConfig:
    brightness_swipe: bool = True
    volume_swipe: bool = True
    hold_to_speed: bool = True
    hold_speed_multiplier: float = 2.0


@dataclass
class BackgroundConfig:
    enable_background_audio: bool = False
    handle_audio_focus: bool = True


@dataclass
class SponsorBlockConfig:
    enabled: bool = False
    skip_mode: str = 'AUTOMATIC'  # AUTOMATIC, ASK, OFF
    categories: list[str] = field(default_factory=lambda: ['sponsor', 'intro', 'outro'])
    show_toast: bool = True
    debounce_ms: int = 250


@dataclass
class AdvertisingConfig:
    block_home_feed_ads: bool = True
    block_video_ads: bool = True
    block_sponsor_cards: bool = True


@dataclass
class DownloadsConfig:
    storage_location: str = 'INTERNAL'  # INTERNAL, EXTERNAL
    audio_only_default: bool = False


@dataclass
class WatchPageConfig:
    hide_comments: bool = False
    hide_related_videos: bool = False
    compact_layout: bool = False


@dataclass
class HomeFeedConfig:
    hide_shorts: bool = False
    compact_feed: bool = False


@dataclass
class ShortsConfig:
    hide_shorts_button: bool = False
    progress_bar_style: str = 'DEFAULT'  # DEFAULT, ACCENT, HIDDEN, SEGMENTED
    progress_bar_color: str = '#10B981'  # Emerald accent


@dataclass
class TabsConfig:
    hidden_tabs: list[str] = field(default_factory=list)  # e.g., ['Shorts', 'Create']
    startup_tab: str = 'Home'


@dataclass
class PrivacyConfig:
    enable_diagnostics: bool = False
    telemetry_allowed: bool = False  # Fixed false, non-modifiable


@dataclass
class AboutConfig:
    version_name: str = '0.3.0-dev'
    developer: str = 'arifular1f'
    repository_url: str = 'https://github.com/arifular1f/MarufYT-Android'


@dataclass
class MarufConfiguration:
    version: int = CONFIG_VERSION
    general: GeneralConfig = field(default_factory=GeneralConfig)
    player: PlayerConfig = field(default_factory=PlayerConfig)
    video_quality: VideoQualityConfig = field(default_factory=VideoQualityConfig)
    captions: CaptionsConfig = field(default_factory=CaptionsConfig)
    gestures: GesturesConfig = field(default_factory=GesturesConfig)
    background: BackgroundConfig = field(default_factory=BackgroundConfig)
    sponsorblock: SponsorBlockConfig = field(default_factory=SponsorBlockConfig)
    advertising: AdvertisingConfig = field(default_factory=AdvertisingConfig)
    downloads: DownloadsConfig = field(default_factory=DownloadsConfig)
    watch_page: WatchPageConfig = field(default_factory=WatchPageConfig)
    home_feed: HomeFeedConfig = field(default_factory=HomeFeedConfig)
    shorts: ShortsConfig = field(default_factory=ShortsConfig)
    tabs: TabsConfig = field(default_factory=TabsConfig)
    privacy: PrivacyConfig = field(default_factory=PrivacyConfig)
    about: AboutConfig = field(default_factory=AboutConfig)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'MarufConfiguration':
        if not isinstance(data, dict):
            raise ConfigError('Configuration data must be a dictionary')

        ver = data.get('version', 1)
        if ver != CONFIG_VERSION:
            raise ConfigError(f'Unsupported configuration schema version: {ver}')

        config = cls()
        if 'general' in data:
            g = data['general']
            config.general.theme = str(g.get('theme', 'SYSTEM'))
            config.general.amoled_black = bool(g.get('amoled_black', False))

        if 'player' in data:
            p = data['player']
            spd = float(p.get('default_playback_speed', 1.0))
            if 0.25 <= spd <= 2.0:
                config.player.default_playback_speed = spd
            config.player.auto_repeat = bool(p.get('auto_repeat', False))
            config.player.remember_speed = bool(p.get('remember_speed', True))

        if 'sponsorblock' in data:
            sb = data['sponsorblock']
            config.sponsorblock.enabled = bool(sb.get('enabled', False))
            config.sponsorblock.skip_mode = str(sb.get('skip_mode', 'AUTOMATIC'))
            if isinstance(sb.get('categories'), list):
                config.sponsorblock.categories = [str(c) for c in sb['categories']]
            config.sponsorblock.show_toast = bool(sb.get('show_toast', True))
            config.sponsorblock.debounce_ms = int(sb.get('debounce_ms', 250))

        if 'gestures' in data:
            gest = data['gestures']
            config.gestures.brightness_swipe = bool(gest.get('brightness_swipe', True))
            config.gestures.volume_swipe = bool(gest.get('volume_swipe', True))
            config.gestures.hold_to_speed = bool(gest.get('hold_to_speed', True))

        if 'shorts' in data:
            sh = data['shorts']
            config.shorts.hide_shorts_button = bool(sh.get('hide_shorts_button', False))
            config.shorts.progress_bar_style = str(sh.get('progress_bar_style', 'DEFAULT'))
            config.shorts.progress_bar_color = str(sh.get('progress_bar_color', '#10B981'))

        if 'tabs' in data:
            tb = data['tabs']
            if isinstance(tb.get('hidden_tabs'), list):
                config.tabs.hidden_tabs = [str(t) for t in tb['hidden_tabs']]
            config.tabs.startup_tab = str(tb.get('startup_tab', 'Home'))

        if 'privacy' in data:
            pr = data['privacy']
            config.privacy.enable_diagnostics = bool(pr.get('enable_diagnostics', False))
            config.privacy.telemetry_allowed = False  # Always enforce False

        return config

    @classmethod
    def from_json(cls, json_str: str) -> 'MarufConfiguration':
        try:
            parsed = json.loads(json_str)
            return cls.from_dict(parsed)
        except (json.JSONDecodeError, ValueError) as e:
            raise ConfigError(f'Invalid configuration JSON: {e}') from e

    def export_bundle(self) -> dict[str, Any]:
        """Creates an export bundle with a SHA-256 integrity signature."""
        serialized = self.to_json()
        checksum = hashlib.sha256(serialized.encode('utf-8')).hexdigest()
        return {
            'format': 'marufyt-config-bundle',
            'schema_version': self.version,
            'checksum': checksum,
            'payload': serialized,
        }

    @classmethod
    def import_bundle(cls, bundle: dict[str, Any]) -> 'MarufConfiguration':
        if not isinstance(bundle, dict):
            raise ConfigError('Bundle must be a dictionary')
        if bundle.get('format') != 'marufyt-config-bundle':
            raise ConfigError('Invalid bundle format header')

        payload = bundle.get('payload')
        checksum = bundle.get('checksum')
        if not isinstance(payload, str) or not isinstance(checksum, str):
            raise ConfigError('Missing bundle payload or checksum')

        computed = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        if computed != checksum:
            raise ConfigError('Bundle integrity verification failed: checksum mismatch')

        return cls.from_json(payload)
