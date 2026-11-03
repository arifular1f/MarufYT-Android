package io.github.arifular1f.marufyt;

import android.app.Activity;
import android.os.Bundle;
import android.widget.*;
import android.content.SharedPreferences;
import android.content.res.Configuration;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.app.AlertDialog;
import android.view.View;
import android.view.WindowInsets;

/** Standalone settings preview. No YouTube attachment or playback controls. */
public final class MainActivity extends Activity {
    private SharedPreferences preferences;
    private boolean dark;
    private int foreground, secondary;
    @Override public void onCreate(Bundle state) {
        preferences = getSharedPreferences("appearance", MODE_PRIVATE);
        ThemeMode mode = ThemeMode.parse(preferences.getString("theme", "SYSTEM"));
        dark = mode.isDark((getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES);
        setTheme(dark ? android.R.style.Theme_Material_NoActionBar : android.R.style.Theme_Material_Light_NoActionBar);
        super.onCreate(state);
        foreground = dark ? Color.rgb(240,242,248) : Color.rgb(25,30,44);
        secondary = dark ? Color.rgb(175,184,202) : Color.rgb(82,92,113);
        ScrollView scroll = new ScrollView(this);
        scroll.setBackgroundColor(dark ? Color.rgb(15,18,26) : Color.rgb(242,244,249));
        LinearLayout body = new LinearLayout(this);
        body.setOrientation(LinearLayout.VERTICAL);
        body.setPadding(dp(20),dp(24),dp(20),dp(32));
        scroll.addView(body);
        scroll.setOnApplyWindowInsetsListener((view, insets) -> {
            int top, bottom;
            if (android.os.Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets bars = insets.getInsets(WindowInsets.Type.systemBars());
                top = bars.top; bottom = bars.bottom;
            } else { top = insets.getSystemWindowInsetTop(); bottom = insets.getSystemWindowInsetBottom(); }
            view.setPadding(0,top,0,bottom); return insets;
        });
        label(body,"MARUFYT / ANDROID",13,Color.rgb(87,128,240),true);
        label(body,"Your settings.\nA clear starting point.",30,foreground,true);
        label(body,"Developer preview · 0.2.0-preview.1",15,secondary,false);
        label(card(body,"Preview status"),"Independent companion app. YouTube integration is unavailable. No automatic skipping or background playback.",15,secondary,false);
        String[] sections = {"Player","Video Quality","Captions","Gestures","SponsorBlock","Watch Page","Home & Feed","Shorts","Tabs","Top Bar","Downloads"};
        String[] reasons = {"Playback lifecycle and entitlement integration is unverified.","Stream-selection integration is unverified.","Track-selection integration is unverified.","Player gestures and accessibility behavior are unverified.","The separate host lookup tool works; Android playback integration is unavailable.","Watch-page customization is not implemented.","Feed filtering is not implemented.","Shorts customization is not implemented.","Navigation customization is not implemented.","Toolbar customization is not implemented.","No download integration is implemented."};
        for (int i=0;i<sections.length;i++) label(card(body,sections[i]),getString(R.string.unavailable_reason,reasons[i]),14,secondary,false);
        LinearLayout general = card(body,"General");
        label(general,"Appearance",16,foreground,true);
        label(general,"Changes this companion only. Saved on this device.",14,secondary,false);
        Spinner picker = new Spinner(this);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this,android.R.layout.simple_spinner_item,new String[]{"Use system theme","Light","Dark"});
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        picker.setAdapter(adapter); picker.setSelection(mode.ordinal());
        picker.setContentDescription("Companion appearance");
        general.addView(picker,new LinearLayout.LayoutParams(-1,dp(56)));
        picker.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            public void onItemSelected(AdapterView<?> parent,View view,int position,long id) {
                String selected = ThemeMode.values()[position].name();
                if (!selected.equals(preferences.getString("theme","SYSTEM"))) {
                    preferences.edit().putString("theme",selected).apply(); recreate();
                }
            }
            public void onNothingSelected(AdapterView<?> parent) { }
        });
        LinearLayout privacy = card(body,"Privacy");
        label(privacy,"No network permission or telemetry. Only your appearance choice is stored. The optional host CLI makes explicit network requests separately.",14,secondary,false);
        Button reset = new Button(this); reset.setText(R.string.reset_appearance); privacy.addView(reset);
        reset.setOnClickListener(view -> new AlertDialog.Builder(this).setTitle("Reset appearance?")
            .setMessage("Clear the companion app's saved appearance choice?").setNegativeButton("Cancel",null)
            .setPositiveButton("Reset",(dialog,which) -> { preferences.edit().clear().apply(); recreate(); }).show());
        label(body,"By arifular1f\nNot affiliated with YouTube or Google.\nPhysical-device verification pending.",12,secondary,false);
        setContentView(scroll); scroll.requestApplyInsets();
    }
    private int dp(int value) { return Math.round(value*getResources().getDisplayMetrics().density); }
    private void label(LinearLayout parent,String text,int size,int color,boolean bold) {
        TextView view = new TextView(this); view.setText(text); view.setTextSize(size); view.setTextColor(color);
        view.setPadding(0,dp(7),0,dp(7)); if (bold) view.setTypeface(Typeface.DEFAULT,Typeface.BOLD); parent.addView(view);
    }
    private LinearLayout card(LinearLayout parent,String title) {
        LinearLayout card = new LinearLayout(this); card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(dp(18),dp(12),dp(18),dp(16));
        GradientDrawable shape = new GradientDrawable(); shape.setColor(dark?Color.rgb(27,32,45):Color.WHITE);
        shape.setCornerRadius(dp(18)); card.setBackground(shape);
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(-1,-2); params.topMargin=dp(14); parent.addView(card,params);
        label(card,title,19,foreground,true); return card;
    }
}
