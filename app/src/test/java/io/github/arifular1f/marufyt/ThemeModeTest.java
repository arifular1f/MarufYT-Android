package io.github.arifular1f.marufyt;
import org.junit.Test;
import static org.junit.Assert.*;
public class ThemeModeTest {
    @Test public void corruptValuesUseSystem() {
        assertEquals(ThemeMode.SYSTEM,ThemeMode.parse(null));
        assertEquals(ThemeMode.SYSTEM,ThemeMode.parse("corrupt"));
    }
    @Test public void savedChoicesRoundTripAndOverrideSystem() {
        for (ThemeMode mode:ThemeMode.values()) assertEquals(mode,ThemeMode.parse(mode.name()));
        assertTrue(ThemeMode.DARK.isDark(false)); assertFalse(ThemeMode.LIGHT.isDark(true));
        assertTrue(ThemeMode.SYSTEM.isDark(true)); assertFalse(ThemeMode.SYSTEM.isDark(false));
    }
}
