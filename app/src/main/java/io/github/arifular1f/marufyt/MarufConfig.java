package io.github.arifular1f.marufyt;

import android.content.Context;
import android.content.SharedPreferences;
import java.util.HashSet;
import java.util.Set;

/**
 * Validated, persistent settings manager for MarufYT Android.
 * Interfaces companion UI preferences with runtime customization contracts.
 */
public final class MarufConfig {
    public static final String PREF_NAME = "marufyt_config";
    public static final int CONFIG_VERSION = 1;

    // Keys
    public static final String KEY_THEME = "general_theme";
    public static final String KEY_AMOLED = "general_amoled";
    public static final String KEY_SPEED = "player_speed";
    public static final String KEY_REPEAT = "player_repeat";
    public static final String KEY_REMEMBER_SPEED = "player_remember_speed";
    public static final String KEY_QUALITY_WIFI = "quality_wifi";
    public static final String KEY_QUALITY_CELLULAR = "quality_cellular";
    public static final String KEY_CAPTIONS_AUTO = "captions_auto";
    public static final String KEY_CAPTIONS_SCALE = "captions_scale";
    public static final String KEY_GESTURES_BRIGHTNESS = "gestures_brightness";
    public static final String KEY_GESTURES_VOLUME = "gestures_volume";
    public static final String KEY_GESTURES_HOLD_SPEED = "gestures_hold_speed";
    public static final String KEY_BG_AUDIO = "bg_audio";
    public static final String KEY_BG_AUDIO_FOCUS = "bg_audio_focus";
    public static final String KEY_SB_ENABLED = "sb_enabled";
    public static final String KEY_SB_MODE = "sb_mode";
    public static final String KEY_SB_CATEGORIES = "sb_categories";
    public static final String KEY_SB_TOAST = "sb_toast";
    public static final String KEY_ADS_FEED = "ads_feed";
    public static final String KEY_ADS_VIDEO = "ads_video";
    public static final String KEY_WATCH_COMMENTS = "watch_hide_comments";
    public static final String KEY_FEED_SHORTS = "feed_hide_shorts";
    public static final String KEY_SHORTS_STYLE = "shorts_style";
    public static final String KEY_TABS_HIDDEN = "tabs_hidden";
    public static final String KEY_DIAGNOSTICS = "privacy_diagnostics";

    private final SharedPreferences prefs;

    public MarufConfig(Context context) {
        this.prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }

    public MarufConfig(SharedPreferences prefs) {
        this.prefs = prefs;
    }

    // General
    public String getTheme() { return prefs.getString(KEY_THEME, "SYSTEM"); }
    public void setTheme(String theme) { prefs.edit().putString(KEY_THEME, theme).apply(); }

    public boolean isAmoled() { return prefs.getBoolean(KEY_AMOLED, false); }
    public void setAmoled(boolean amoled) { prefs.edit().putBoolean(KEY_AMOLED, amoled).apply(); }

    // Player
    public float getPlaybackSpeed() { return prefs.getFloat(KEY_SPEED, 1.0f); }
    public void setPlaybackSpeed(float speed) { prefs.edit().putFloat(KEY_SPEED, Math.max(0.25f, Math.min(2.0f, speed))).apply(); }

    public boolean isAutoRepeat() { return prefs.getBoolean(KEY_REPEAT, false); }
    public void setAutoRepeat(boolean repeat) { prefs.edit().putBoolean(KEY_REPEAT, repeat).apply(); }

    // Gestures
    public boolean isBrightnessGesture() { return prefs.getBoolean(KEY_GESTURES_BRIGHTNESS, true); }
    public void setBrightnessGesture(boolean enabled) { prefs.edit().putBoolean(KEY_GESTURES_BRIGHTNESS, enabled).apply(); }

    public boolean isVolumeGesture() { return prefs.getBoolean(KEY_GESTURES_VOLUME, true); }
    public void setVolumeGesture(boolean enabled) { prefs.edit().putBoolean(KEY_GESTURES_VOLUME, enabled).apply(); }

    // SponsorBlock
    public boolean isSponsorBlockEnabled() { return prefs.getBoolean(KEY_SB_ENABLED, false); }
    public void setSponsorBlockEnabled(boolean enabled) { prefs.edit().putBoolean(KEY_SB_ENABLED, enabled).apply(); }

    public String getSponsorBlockMode() { return prefs.getString(KEY_SB_MODE, "AUTOMATIC"); }
    public void setSponsorBlockMode(String mode) { prefs.edit().putString(KEY_SB_MODE, mode).apply(); }

    public Set<String> getSponsorBlockCategories() {
        Set<String> defaults = new HashSet<>();
        defaults.add("sponsor");
        defaults.add("intro");
        defaults.add("outro");
        return prefs.getStringSet(KEY_SB_CATEGORIES, defaults);
    }
    public void setSponsorBlockCategories(Set<String> categories) {
        prefs.edit().putStringSet(KEY_SB_CATEGORIES, categories).apply();
    }

    // Ads
    public boolean isBlockFeedAds() { return prefs.getBoolean(KEY_ADS_FEED, true); }
    public void setBlockFeedAds(boolean block) { prefs.edit().putBoolean(KEY_ADS_FEED, block).apply(); }

    public boolean isBlockVideoAds() { return prefs.getBoolean(KEY_ADS_VIDEO, true); }
    public void setBlockVideoAds(boolean block) { prefs.edit().putBoolean(KEY_ADS_VIDEO, block).apply(); }

    // Shorts
    public String getShortsStyle() { return prefs.getString(KEY_SHORTS_STYLE, "DEFAULT"); }
    public void setShortsStyle(String style) { prefs.edit().putString(KEY_SHORTS_STYLE, style).apply(); }

    // Tabs
    public Set<String> getHiddenTabs() { return prefs.getStringSet(KEY_TABS_HIDDEN, new HashSet<String>()); }
    public void setHiddenTabs(Set<String> hiddenTabs) { prefs.edit().putStringSet(KEY_TABS_HIDDEN, hiddenTabs).apply(); }

    // Privacy
    public boolean isDiagnosticsEnabled() { return prefs.getBoolean(KEY_DIAGNOSTICS, false); }
    public void setDiagnosticsEnabled(boolean enabled) { prefs.edit().putBoolean(KEY_DIAGNOSTICS, enabled).apply(); }
    public boolean isTelemetryAllowed() { return false; } // Invariant: telemetry is strictly forbidden

    // Reset
    public void resetAll() {
        prefs.edit().clear().apply();
    }
}
