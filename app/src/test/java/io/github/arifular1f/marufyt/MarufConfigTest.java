package io.github.arifular1f.marufyt;

import android.content.SharedPreferences;
import org.junit.Before;
import org.junit.Test;
import java.util.*;

import static org.junit.Assert.*;

public class MarufConfigTest {

    private FakeSharedPreferences fakePrefs;
    private MarufConfig config;

    @Before
    public void setUp() {
        fakePrefs = new FakeSharedPreferences();
        config = new MarufConfig(fakePrefs);
    }

    @Test
    public void defaultValuesMatchSchema() {
        assertEquals("SYSTEM", config.getTheme());
        assertFalse(config.isAmoled());
        assertEquals(1.0f, config.getPlaybackSpeed(), 0.001f);
        assertFalse(config.isAutoRepeat());
        assertTrue(config.isBrightnessGesture());
        assertTrue(config.isVolumeGesture());
        assertFalse(config.isSponsorBlockEnabled());
        assertEquals("AUTOMATIC", config.getSponsorBlockMode());
        assertTrue(config.isBlockFeedAds());
        assertTrue(config.isBlockVideoAds());
        assertEquals("DEFAULT", config.getShortsStyle());
        assertFalse(config.isDiagnosticsEnabled());
        assertFalse(config.isTelemetryAllowed());
    }

    @Test
    public void themeAndAmoledMutationsPersist() {
        config.setTheme("DARK");
        assertEquals("DARK", config.getTheme());
        config.setAmoled(true);
        assertTrue(config.isAmoled());
    }

    @Test
    public void playbackSpeedClamping() {
        config.setPlaybackSpeed(1.5f);
        assertEquals(1.5f, config.getPlaybackSpeed(), 0.001f);

        // Lower clamp
        config.setPlaybackSpeed(0.1f);
        assertEquals(0.25f, config.getPlaybackSpeed(), 0.001f);

        // Upper clamp
        config.setPlaybackSpeed(3.0f);
        assertEquals(2.0f, config.getPlaybackSpeed(), 0.001f);
    }

    @Test
    public void sponsorBlockCategoriesManagement() {
        Set<String> custom = new HashSet<>();
        custom.add("sponsor");
        custom.add("interaction");
        config.setSponsorBlockCategories(custom);

        Set<String> retrieved = config.getSponsorBlockCategories();
        assertEquals(2, retrieved.size());
        assertTrue(retrieved.contains("sponsor"));
        assertTrue(retrieved.contains("interaction"));
        assertFalse(retrieved.contains("outro"));
    }

    @Test
    public void telemetryInvariantIsAlwaysFalse() {
        assertFalse(config.isTelemetryAllowed());
    }

    @Test
    public void resetAllClearsPreferences() {
        config.setTheme("LIGHT");
        config.setAmoled(true);
        config.setPlaybackSpeed(1.75f);
        config.setSponsorBlockEnabled(true);

        config.resetAll();

        assertEquals("SYSTEM", config.getTheme());
        assertFalse(config.isAmoled());
        assertEquals(1.0f, config.getPlaybackSpeed(), 0.001f);
        assertFalse(config.isSponsorBlockEnabled());
    }

    /** In-memory SharedPreferences implementation for lightweight JVM unit testing */
    private static class FakeSharedPreferences implements SharedPreferences {
        final Map<String, Object> map = new HashMap<>();

        @Override
        public Map<String, ?> getAll() { return new HashMap<>(map); }

        @Override
        public String getString(String key, String defValue) {
            Object val = map.get(key);
            return val instanceof String ? (String) val : defValue;
        }

        @Override
        @SuppressWarnings("unchecked")
        public Set<String> getStringSet(String key, Set<String> defValues) {
            Object val = map.get(key);
            return val instanceof Set ? new HashSet<>((Set<String>) val) : defValues;
        }

        @Override
        public int getInt(String key, int defValue) {
            Object val = map.get(key);
            return val instanceof Integer ? (Integer) val : defValue;
        }

        @Override
        public long getLong(String key, long defValue) {
            Object val = map.get(key);
            return val instanceof Long ? (Long) val : defValue;
        }

        @Override
        public float getFloat(String key, float defValue) {
            Object val = map.get(key);
            return val instanceof Float ? (Float) val : defValue;
        }

        @Override
        public boolean getBoolean(String key, boolean defValue) {
            Object val = map.get(key);
            return val instanceof Boolean ? (Boolean) val : defValue;
        }

        @Override
        public boolean contains(String key) { return map.containsKey(key); }

        @Override
        public Editor edit() { return new FakeEditor(this); }

        @Override
        public void registerOnSharedPreferenceChangeListener(OnSharedPreferenceChangeListener listener) {}

        @Override
        public void unregisterOnSharedPreferenceChangeListener(OnSharedPreferenceChangeListener listener) {}
    }

    private static class FakeEditor implements SharedPreferences.Editor {
        private final FakeSharedPreferences target;
        private final Map<String, Object> staging = new HashMap<>();
        private boolean clearFlag = false;

        FakeEditor(FakeSharedPreferences target) { this.target = target; }

        @Override
        public SharedPreferences.Editor putString(String key, String value) { staging.put(key, value); return this; }

        @Override
        public SharedPreferences.Editor putStringSet(String key, Set<String> values) { staging.put(key, values != null ? new HashSet<>(values) : null); return this; }

        @Override
        public SharedPreferences.Editor putInt(String key, int value) { staging.put(key, value); return this; }

        @Override
        public SharedPreferences.Editor putLong(String key, long value) { staging.put(key, value); return this; }

        @Override
        public SharedPreferences.Editor putFloat(String key, float value) { staging.put(key, value); return this; }

        @Override
        public SharedPreferences.Editor putBoolean(String key, boolean value) { staging.put(key, value); return this; }

        @Override
        public SharedPreferences.Editor remove(String key) { staging.put(key, this); return this; }

        @Override
        public SharedPreferences.Editor clear() { clearFlag = true; return this; }

        @Override
        public boolean commit() { apply(); return true; }

        @Override
        public void apply() {
            if (clearFlag) {
                target.map.clear();
            }
            for (Map.Entry<String, Object> entry : staging.entrySet()) {
                if (entry.getValue() == this) {
                    target.map.remove(entry.getKey());
                } else {
                    target.map.put(entry.getKey(), entry.getValue());
                }
            }
        }
    }
}
