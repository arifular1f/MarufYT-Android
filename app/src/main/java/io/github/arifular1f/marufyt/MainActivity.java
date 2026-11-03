package io.github.arifular1f.marufyt;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.res.Configuration;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.WindowInsets;
import android.widget.*;
import java.util.HashSet;
import java.util.Set;

/**
 * Premium native companion and settings dashboard for MarufYT Android (Phase 3).
 * Provides unified, verified configuration controls across 15 modular functional domains.
 */
public final class MainActivity extends Activity {
    private MarufConfig config;
    private boolean dark;
    private boolean amoled;
    private int bgPrimary;
    private int cardBg;
    private int fgPrimary;
    private int fgSecondary;
    private int accentColor;
    private int emeraldColor;
    private int badgeBg;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        config = new MarufConfig(this);
        ThemeMode mode = ThemeMode.parse(config.getTheme());
        boolean sysDark = (getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES;
        dark = mode.isDark(sysDark);
        amoled = dark && config.isAmoled();

        setTheme(dark ? android.R.style.Theme_Material_NoActionBar : android.R.style.Theme_Material_Light_NoActionBar);
        super.onCreate(savedInstanceState);

        // Color palette
        bgPrimary = amoled ? Color.BLACK : (dark ? Color.rgb(15, 18, 26) : Color.rgb(242, 245, 250));
        cardBg = amoled ? Color.rgb(18, 18, 18) : (dark ? Color.rgb(27, 32, 45) : Color.WHITE);
        fgPrimary = dark ? Color.rgb(240, 244, 255) : Color.rgb(22, 28, 42);
        fgSecondary = dark ? Color.rgb(160, 172, 196) : Color.rgb(90, 102, 124);
        accentColor = Color.rgb(87, 128, 240);
        emeraldColor = Color.rgb(16, 185, 129);
        badgeBg = dark ? Color.rgb(36, 44, 62) : Color.rgb(228, 234, 245);

        ScrollView scroll = new ScrollView(this);
        scroll.setBackgroundColor(bgPrimary);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(18), dp(20), dp(18), dp(36));
        scroll.addView(root);

        // Window insets
        scroll.setOnApplyWindowInsetsListener((view, insets) -> {
            int top = 0, bottom = 0;
            if (Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets bars = insets.getInsets(WindowInsets.Type.systemBars());
                top = bars.top;
                bottom = bars.bottom;
            } else {
                top = insets.getSystemWindowInsetTop();
                bottom = insets.getSystemWindowInsetBottom();
            }
            view.setPadding(0, top, 0, bottom);
            return insets;
        });

        // 1. Header / Hero section
        renderHeader(root);

        // 2. General Section
        renderGeneralSection(root, mode);

        // 3. Player Section
        renderPlayerSection(root);

        // 4. Video Quality Section
        renderQualitySection(root);

        // 5. Captions Section
        renderCaptionsSection(root);

        // 6. Gestures Section
        renderGesturesSection(root);

        // 7. Background Playback Section
        renderBackgroundSection(root);

        // 8. SponsorBlock Section
        renderSponsorBlockSection(root);

        // 9. Advertising & Promotion Section
        renderAdvertisingSection(root);

        // 10. Downloads Section
        renderDownloadsSection(root);

        // 11. Watch Page Section
        renderWatchPageSection(root);

        // 12. Home & Feed Section
        renderHomeFeedSection(root);

        // 13. Shorts Section
        renderShortsSection(root);

        // 14. Navigation Tabs Section
        renderTabsSection(root);

        // 15. Privacy & Security Section
        renderPrivacySection(root);

        // 16. About Section
        renderAboutSection(root);

        setContentView(scroll);
        scroll.requestApplyInsets();
    }

    private void renderHeader(LinearLayout parent) {
        LinearLayout badgeLayout = new LinearLayout(this);
        badgeLayout.setOrientation(LinearLayout.HORIZONTAL);
        badgeLayout.setPadding(dp(10), dp(4), dp(10), dp(4));
        GradientDrawable badgeShape = new GradientDrawable();
        badgeShape.setColor(badgeBg);
        badgeShape.setCornerRadius(dp(8));
        badgeLayout.setBackground(badgeShape);

        TextView badgeText = new TextView(this);
        badgeText.setText("MARUFYT ANDROID · PHASE 3");
        badgeText.setTextSize(11);
        badgeText.setTextColor(accentColor);
        badgeText.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        badgeLayout.addView(badgeText);

        LinearLayout.LayoutParams badgeParams = new LinearLayout.LayoutParams(-2, -2);
        badgeParams.bottomMargin = dp(10);
        parent.addView(badgeLayout, badgeParams);

        TextView title = new TextView(this);
        title.setText("Companion Settings");
        title.setTextSize(26);
        title.setTextColor(fgPrimary);
        title.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        parent.addView(title);

        TextView sub = new TextView(this);
        sub.setText("Modular runtime architecture, SponsorBlock auto-skip, zero-telemetry configuration engine.");
        sub.setTextSize(13);
        sub.setTextColor(fgSecondary);
        sub.setPadding(0, dp(4), 0, dp(14));
        parent.addView(sub);
    }

    private void renderGeneralSection(LinearLayout parent, ThemeMode mode) {
        LinearLayout card = createCard(parent, "General & Appearance");
        createDescription(card, "Customize companion visual presentation and system interface behaviors.");

        createSubLabel(card, "Theme Mode");
        Spinner themeSpinner = new Spinner(this);
        ArrayAdapter<String> themeAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item,
                new String[]{"Follow System", "Light Mode", "Dark Mode"});
        themeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        themeSpinner.setAdapter(themeAdapter);
        themeSpinner.setSelection(mode.ordinal());
        card.addView(themeSpinner, new LinearLayout.LayoutParams(-1, dp(48)));

        themeSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> p, View v, int pos, long id) {
                String chosen = ThemeMode.values()[pos].name();
                if (!chosen.equals(config.getTheme())) {
                    config.setTheme(chosen);
                    recreate();
                }
            }
            @Override public void onNothingSelected(AdapterView<?> p) {}
        });

        createSwitch(card, "Pure AMOLED Black", "Eliminate deep navy background in dark mode for OLED displays",
                config.isAmoled(), (btn, isChecked) -> {
                    config.setAmoled(isChecked);
                    recreate();
                });
    }

    private void renderPlayerSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Playback Engine");
        createDescription(card, "Configure media player behavioral policies, rate adjustments, and looping.");

        createSubLabel(card, "Default Playback Speed");
        Spinner speedSpinner = new Spinner(this);
        String[] speeds = {"0.25x", "0.5x", "0.75x", "1.0x (Normal)", "1.25x", "1.5x", "1.75x", "2.0x"};
        final float[] speedVals = {0.25f, 0.5f, 0.75f, 1.0f, 1.25f, 1.5f, 1.75f, 2.0f};
        ArrayAdapter<String> speedAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, speeds);
        speedAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        speedSpinner.setAdapter(speedAdapter);

        float currentSpeed = config.getPlaybackSpeed();
        int selectedSpeedIdx = 3;
        for (int i = 0; i < speedVals.length; i++) {
            if (Math.abs(speedVals[i] - currentSpeed) < 0.01f) {
                selectedSpeedIdx = i;
                break;
            }
        }
        speedSpinner.setSelection(selectedSpeedIdx);
        card.addView(speedSpinner, new LinearLayout.LayoutParams(-1, dp(48)));

        speedSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> p, View v, int pos, long id) {
                config.setPlaybackSpeed(speedVals[pos]);
            }
            @Override public void onNothingSelected(AdapterView<?> p) {}
        });

        createSwitch(card, "Auto-Repeat Playback", "Loop current media segment automatically on playback completion",
                config.isAutoRepeat(), (btn, isChecked) -> config.setAutoRepeat(isChecked));
    }

    private void renderQualitySection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Video Quality & Formats");
        createDescription(card, "Resolution selection policies and network-adaptive stream preferences.");
        createStatusPill(card, "CONTRACT DEFINED", emeraldColor);
        createDescription(card, "Default Wi-Fi Target: 1080p60 · Cellular Target: 720p30 (Auto fallback on high-latency connection).");
    }

    private void renderCaptionsSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Captions & Subtitles");
        createDescription(card, "Accessibility track controls, auto-generation behavior, and font sizing.");
        createStatusPill(card, "FRAMEWORK READY", emeraldColor);
        createDescription(card, "Auto-enable English track if present. Font scaling multiplier: 1.0x (Clean outline rendering).");
    }

    private void renderGesturesSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Player Gestures");
        createDescription(card, "Interactive touch swipe controls overlaying ExoPlayer surface.");

        createSwitch(card, "Swipe Brightness Control", "Vertical swipe on left half adjusts screen backlight level",
                config.isBrightnessGesture(), (btn, isChecked) -> config.setBrightnessGesture(isChecked));

        createSwitch(card, "Swipe Volume Control", "Vertical swipe on right half adjusts media audio stream",
                config.isVolumeGesture(), (btn, isChecked) -> config.setVolumeGesture(isChecked));
    }

    private void renderBackgroundSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Background Playback");
        createDescription(card, "Audio continuation during screen-off, task switching, and PiP.");
        createStatusPill(card, "BLOCKED BY HOST ENTITLEMENT", Color.rgb(239, 68, 68));
        createDescription(card, "BackgroundPlayerService calls Lasll;->d(Service)V validating YouTube Premium entitlements. Direct bypass without native runtime hook causes immediate stop.");
    }

    private void renderSponsorBlockSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "SponsorBlock Integration");
        createDescription(card, "Automated and interactive segment skipping with privacy-preserving hash prefix lookups.");

        createSwitch(card, "Enable SponsorBlock Engine", "Active playback monitoring against crowdsourced segment timestamps",
                config.isSponsorBlockEnabled(), (btn, isChecked) -> config.setSponsorBlockEnabled(isChecked));

        createSubLabel(card, "Skip Action Mode");
        Spinner modeSpinner = new Spinner(this);
        ArrayAdapter<String> modeAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item,
                new String[]{"AUTOMATIC (Seamless Skip)", "ASK (Interactive Toast Prompt)"});
        modeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        modeSpinner.setAdapter(modeAdapter);
        modeSpinner.setSelection("ASK".equals(config.getSponsorBlockMode()) ? 1 : 0);
        card.addView(modeSpinner, new LinearLayout.LayoutParams(-1, dp(48)));

        modeSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> p, View v, int pos, long id) {
                config.setSponsorBlockMode(pos == 1 ? "ASK" : "AUTOMATIC");
            }
            @Override public void onNothingSelected(AdapterView<?> p) {}
        });

        createSubLabel(card, "Active Category Filter");
        Set<String> activeCats = config.getSponsorBlockCategories();
        String[] catKeys = {"sponsor", "intro", "outro", "interaction", "selfpromo"};
        String[] catTitles = {"Sponsor Segments", "Intro / Title Cards", "Outro / End Cards", "Interaction Reminders", "Self Promotion"};

        for (int i = 0; i < catKeys.length; i++) {
            final String key = catKeys[i];
            createSwitch(card, catTitles[i], "Skip matching segment class",
                    activeCats.contains(key), (btn, isChecked) -> {
                        Set<String> updated = new HashSet<>(config.getSponsorBlockCategories());
                        if (isChecked) updated.add(key);
                        else updated.remove(key);
                        config.setSponsorBlockCategories(updated);
                    });
        }
    }

    private void renderAdvertisingSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Advertising & Promotions");
        createDescription(card, "Content sanitization and promotional element suppression.");

        createSwitch(card, "Suppress Feed Advertisements", "Filter promotional sponsored cards from home browse feeds",
                config.isBlockFeedAds(), (btn, isChecked) -> config.setBlockFeedAds(isChecked));

        createSwitch(card, "Suppress Video Ad Breaks", "Skip pre-roll and mid-roll commercial ad streams",
                config.isBlockVideoAds(), (btn, isChecked) -> config.setBlockVideoAds(isChecked));
    }

    private void renderDownloadsSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Downloads & Offline");
        createDescription(card, "Local offline media storage and caching architecture.");
        createStatusPill(card, "BLOCKED BY WIDEVINE DRM", Color.rgb(239, 68, 68));
        createDescription(card, "Official offline caching relies on Widevine DRM hardware decoders. Exporting unencrypted streams is blocked by DRM security policies.");
    }

    private void renderWatchPageSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Watch Page & Layout");
        createDescription(card, "Adjust video details, comments display, and metadata card visibility.");
        createStatusPill(card, "PARTIALLY FEASIBLE", Color.rgb(245, 158, 11));
        createDescription(card, "Targeting Litho ComponentTree mutations to collapse comment sections and engagement panels.");
    }

    private void renderHomeFeedSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Home & Feed");
        createDescription(card, "Browse tab filtering and layout density customization.");
        createStatusPill(card, "BLOCKED BY ELEMENT LITHO ENGINE", Color.rgb(239, 68, 68));
        createDescription(card, "Protobuf-driven browse response streams feed directly into Element Litho hierarchy with no public view hooks.");
    }

    private void renderShortsSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Shorts Player");
        createDescription(card, "Vertical short-form video player interface and progress styling.");

        createSubLabel(card, "Progress Bar Indicator Style");
        Spinner styleSpinner = new Spinner(this);
        ArrayAdapter<String> styleAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item,
                new String[]{"DEFAULT (Standard)", "GRADIENT (Accent Tint)", "HIDDEN (Clean Immersive)"});
        styleAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        styleSpinner.setAdapter(styleAdapter);
        String curStyle = config.getShortsStyle();
        int sIdx = "GRADIENT".equals(curStyle) ? 1 : ("HIDDEN".equals(curStyle) ? 2 : 0);
        styleSpinner.setSelection(sIdx);
        card.addView(styleSpinner, new LinearLayout.LayoutParams(-1, dp(48)));

        styleSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> p, View v, int pos, long id) {
                String val = pos == 1 ? "GRADIENT" : (pos == 2 ? "HIDDEN" : "DEFAULT");
                config.setShortsStyle(val);
            }
            @Override public void onNothingSelected(AdapterView<?> p) {}
        });
    }

    private void renderTabsSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Navigation Bar & Tabs");
        createDescription(card, "Customize visible bottom navigation destinations.");

        Set<String> hidden = config.getHiddenTabs();
        createSwitch(card, "Hide Shorts Navigation Tab", "Remove Shorts icon from bottom navigation bar",
                hidden.contains("shorts"), (btn, isChecked) -> {
                    Set<String> set = new HashSet<>(config.getHiddenTabs());
                    if (isChecked) set.add("shorts"); else set.remove("shorts");
                    config.setHiddenTabs(set);
                });

        createSwitch(card, "Hide Create / Upload (+) Tab", "Remove Create button from center navigation bar",
                hidden.contains("create"), (btn, isChecked) -> {
                    Set<String> set = new HashSet<>(config.getHiddenTabs());
                    if (isChecked) set.add("create"); else set.remove("create");
                    config.setHiddenTabs(set);
                });
    }

    private void renderPrivacySection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "Privacy & Telemetry Invariant");
        createDescription(card, "Guaranteed zero analytics, zero external telemetry, zero proprietary trackers.");

        createStatusPill(card, "ZERO TELEMETRY ENFORCED", emeraldColor);

        createSwitch(card, "Local Diagnostic Logs", "Retain crash/validation trace locally in private storage only",
                config.isDiagnosticsEnabled(), (btn, isChecked) -> config.setDiagnosticsEnabled(isChecked));

        Button resetBtn = new Button(this);
        resetBtn.setText("Reset All Preferences to Defaults");
        resetBtn.setTextColor(Color.rgb(239, 68, 68));
        LinearLayout.LayoutParams btnParams = new LinearLayout.LayoutParams(-1, -2);
        btnParams.topMargin = dp(14);
        card.addView(resetBtn, btnParams);

        resetBtn.setOnClickListener(v -> new AlertDialog.Builder(this)
                .setTitle("Reset Configuration?")
                .setMessage("All customized preferences across all 15 domains will be reverted to safe default values.")
                .setNegativeButton("Cancel", null)
                .setPositiveButton("Reset", (dialog, which) -> {
                    config.resetAll();
                    recreate();
                }).show());
    }

    private void renderAboutSection(LinearLayout parent) {
        LinearLayout card = createCard(parent, "About MarufYT Android");
        createDescription(card, "MarufYT Android Companion & Runtime · Version 0.3.0-dev (Phase 3 Complete)\n"
                + "Developed by Maruf (arifular1f)\n"
                + "Repository: https://github.com/arifular1f/MarufYT-Android\n\n"
                + "Strict Open-Source Source-Only Project.\n"
                + "No proprietary binaries, keys, or modified APKs are distributed.\n"
                + "Not affiliated with YouTube, LLC or Google, Inc.");
    }

    // UI Helpers
    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    private LinearLayout createCard(LinearLayout parent, String title) {
        LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(dp(18), dp(16), dp(18), dp(18));

        GradientDrawable shape = new GradientDrawable();
        shape.setColor(cardBg);
        shape.setCornerRadius(dp(16));
        card.setBackground(shape);

        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(-1, -2);
        params.topMargin = dp(16);
        parent.addView(card, params);

        TextView titleView = new TextView(this);
        titleView.setText(title);
        titleView.setTextSize(18);
        titleView.setTextColor(fgPrimary);
        titleView.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        titleView.setPadding(0, 0, 0, dp(6));
        card.addView(titleView);

        return card;
    }

    private void createDescription(LinearLayout card, String text) {
        TextView desc = new TextView(this);
        desc.setText(text);
        desc.setTextSize(13);
        desc.setTextColor(fgSecondary);
        desc.setLineSpacing(dp(2), 1.15f);
        desc.setPadding(0, 0, 0, dp(8));
        card.addView(desc);
    }

    private void createSubLabel(LinearLayout card, String text) {
        TextView label = new TextView(this);
        label.setText(text);
        label.setTextSize(13);
        label.setTextColor(accentColor);
        label.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        label.setPadding(0, dp(8), 0, dp(4));
        card.addView(label);
    }

    private void createStatusPill(LinearLayout card, String text, int color) {
        LinearLayout pill = new LinearLayout(this);
        pill.setOrientation(LinearLayout.HORIZONTAL);
        pill.setPadding(dp(8), dp(3), dp(8), dp(3));

        GradientDrawable shape = new GradientDrawable();
        shape.setColor(dark ? Color.rgb(30, 36, 48) : Color.rgb(238, 242, 250));
        shape.setStroke(dp(1), color);
        shape.setCornerRadius(dp(6));
        pill.setBackground(shape);

        TextView tv = new TextView(this);
        tv.setText(text);
        tv.setTextSize(11);
        tv.setTextColor(color);
        tv.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        pill.addView(tv);

        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(-2, -2);
        params.topMargin = dp(4);
        params.bottomMargin = dp(8);
        card.addView(pill, params);
    }

    private void createSwitch(LinearLayout card, String title, String subtitle, boolean currentVal,
                              CompoundButton.OnCheckedChangeListener listener) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setPadding(0, dp(8), 0, dp(8));

        LinearLayout textCol = new LinearLayout(this);
        textCol.setOrientation(LinearLayout.VERTICAL);
        LinearLayout.LayoutParams textParams = new LinearLayout.LayoutParams(0, -2, 1.0f);
        textCol.setLayoutParams(textParams);

        TextView titleView = new TextView(this);
        titleView.setText(title);
        titleView.setTextSize(15);
        titleView.setTextColor(fgPrimary);
        titleView.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        textCol.addView(titleView);

        TextView subView = new TextView(this);
        subView.setText(subtitle);
        subView.setTextSize(12);
        subView.setTextColor(fgSecondary);
        textCol.addView(subView);

        row.addView(textCol);

        Switch sw = new Switch(this);
        sw.setChecked(currentVal);
        sw.setOnCheckedChangeListener(listener);
        row.addView(sw, new LinearLayout.LayoutParams(-2, -2));

        card.addView(row);
    }
}
