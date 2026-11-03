package io.github.arifular1f.marufyt;
public enum ThemeMode {
    SYSTEM, LIGHT, DARK;
    public static ThemeMode parse(String value) {
        try { return valueOf(value); }
        catch (IllegalArgumentException | NullPointerException error) { return SYSTEM; }
    }
    public boolean isDark(boolean systemDark) { return this == DARK || (this == SYSTEM && systemDark); }
}
