# Phase 2C: Deep Semantic Validation and Feature Implementation Readiness Report

**Date:** 2026-11-03 (Asia/Kuala_Lumpur)  
**Package:** `com.google.android.youtube` / Target version: `21.44.528` (code `1561310186`)  
**SHA-256:** `55be430ce82dcedcb737ea27d1b78576737b75d11cde04aa89989e5376d3ae6c`  
**Status:** Read-only semantic analysis, data-flow verification, contract tests added, and readiness assessment complete. Source-only repository preserved. No modified APK or proprietary binaries generated.

---

## 1. Executive Summary

Phase 2C completes deep semantic validation of the YouTube Android application based on disassembled SDK Smali evidence from the SHA-pinned 21.44.528 APK.

Key outcomes:
1. **Data-flow & Caller Evidence Traced:** Concrete execution paths and constraints identified for Video ID, Playback Timeline, Seek Operations, Background Service, Shorts, and Player Lifecycle.
2. **Clarified Misconceptions:**
   - `PlaybackControllerWrapper.i(SabrSeek)` was previously suspected to be a seek API. Disassembly proves it is the internal `onSabrSeek` callback from the SABR streaming protocol, which manipulates buffer managers and media push sources. It cannot be safely invoked from external code to seek the player.
   - `PlaybackControllerWrapper.c()` is confirmed by constant string `"fail to getCurrentPlaybackPosition"` to return the current playback position as a `Time` object with microsecond scale (`1,000,000`).
   - Multiple `getVideoId()` methods (`bpnu`, `biyw`, `bovv`) return protobuf string fields, but coexist across feed previews, preloads, and playlists. Static discovery cannot disambiguate active foreground playback from preloaded metadata without runtime context.
3. **Automated Data-Flow Contracts:** Added `tools/marufyt/semantics.py` and `tests/test_semantics.py` (14 new automated unit tests, bringing the suite to 65 passing tests).
4. **Feasibility Matrix Established:** All 13 core features formally classified across five technical feasibility tiers.

---

## 2. Deep Caller & Data-Flow Investigation

### A. Video Identity Data Flow
* **Observed Method Declarations:** 47 references to `getVideoId()`, `getDuration()`, `getCurrentPosition()`.
* **Concrete Implementations:**
  - `bpnu.getVideoId()Ljava/lang/String;`: reads `iget-object p0, p0, Lbpnu;->c:Lbpnv;` then `iget-object p0, p0, Lbpnv;->e:Ljava/lang/String;`.
  - `biyw.getVideoId()Ljava/lang/String;`: reads `iget-object p0, p0, Lbiyw;->d:Lbiyx;` then `iget-object p0, p0, Lbiyx;->e:Ljava/lang/String;`.
  - `bovv.getVideoId()Ljava/lang/String;`: reads `iget-object p0, p0, Lbovv;->c:Lbovw;` then `iget-object p0, p0, Lbovw;->e:Ljava/lang/String;`.
* **Semantics:** These are generated Protobuf accessor methods returning video ID strings from internal proto data structures.
* **Blocker / Integration Risk:** In YouTube for Android, multiple video models coexist simultaneously (e.g. inline video in feed, active player, upcoming playlist video, adjacent Shorts in pager). Hooking an arbitrary getter triggers on background/prefetched video metadata. Active video identity must be coupled to the active player controller state.

### B. Playback Timeline & Clock
* **Class:** `com.google.android.libraries.youtube.media.interfaces.Time` (`classes2.dex`).
* **Fields:** `ticks: J`, `timescale: J`.
* **Methods:**
  - `a()D`: returns `ticks / timescale` (seconds as double).
  - `c()J`: requests scale `1,000,000` (microseconds) via JNI bridge.
  - `d()J`: requests scale `1,000` (milliseconds) via JNI bridge.
* **Playback Position (`PlaybackControllerWrapper.c()`):**
  - Reads `MediaPushMediaSource.e: J` (position).
  - Handles ExoPlayer sentinels: `C.TIME_UNSET` (`-0x7fffffffffffffffL`) and `Long.MAX_VALUE` (`0x7fffffffffffffffL`).
  - Constructs `new Time(pos, 1000000L)`.
  - Error handler catches exceptions with message `"fail to getCurrentPlaybackPosition"`.
* **Integration Readiness:** Rational clock conversions and sentinels are now fully modeled in `PlaybackTimelineContract` with millisecond precision and 24-hour duration bounds.

### C. Seek Operations
* **Method:** `PlaybackControllerWrapper.i(SabrSeekOuterClass$SabrSeek)`
* **Smali Disassembly Findings:**
  - Converts `SabrSeek.b: J` and `SabrSeek.c: I` via `Lappk;->b(JJ)J`.
  - Checks if stream is `LiveTimeline`.
  - Validates seek mode enum `bmdp`.
  - Checks buffer status in `BufferManagerImpl` (`p(scz, J)` and `q(scz)`).
  - Throws or logs with message `"onSabrSeek."` and error code `";r.sabr_seek_fail"`.
* **Crucial Finding:** This is NOT an external seekTo API. It is an internal streaming engine callback triggered by the SABR network protocol. Attempting to invoke this directly from a tweak desynchronizes ExoPlayer audio/video buffers and triggers SABR errors. Real seeking must interface with the higher-level Player UI controls or ExoPlayer controller wrapper.

### D. Background Player Service
* **Class:** `com.google.android.libraries.youtube.player.background.service.BackgroundPlayerService` (`classes2.dex`).
* **Superclass:** `arez` (extends `android.app.Service`).
* **Manifest declaration:** Non-exported, `foregroundServiceType="mediaPlayback"`.
* **Smali Disassembly Findings:**
  - `onStartCommand` invokes `iget-object p1, p0, ...;->b:Lasll; invoke-virtual {p1, p0}, Lasll;->d(Service)V` and returns `2` (`START_NOT_STICKY`).
  - `Lasll` performs YouTube Premium / entitlement validation before promoting the service or binding audio focus.
  - Upon `MainActivity.onPause()` / `onStop()`, the app dispatches an event instructing the player to pause if entitlement is not present.
* **Crucial Finding:** Background playback is BLOCKED by entitlement validation. Simply keeping `BackgroundPlayerService` alive without modifying the entitlement logic in `Lasll` and the activity pause listeners results in immediate playback pause.

### E. Shorts Architecture
* **Classes:**
  - `ShortsPlayerProgressPresenter` (`classes4.dex`): extends `View`.
  - `ReelWatchPagerViewPager` (`classes4.dex`): handles swipe transitions.
  - `ReelRecyclerView` (`classes6.dex`): container recycler view.
* **Smali Disassembly Findings for `ShortsPlayerProgressPresenter`:**
  - Contains `volatile a: J` (position) and `volatile b: J` (duration).
  - Uses `Paint` (`u`, `v`, `w`) and `RectF` (`x`).
  - `onDraw(Canvas)` draws progress bars across segmented intervals.
  - State updated via `a(Lblpb;ZIIIF)V`.
* **Integration Readiness:** Progress presenter state is directly verifiable. However, auto-advance requires synthetic touch injection or pager navigation calls on `ReelWatchPagerViewPager`.

### F. Player Lifecycle & Activity
* **Class:** `MainActivity` (`classes.dex`).
* **Superclass:** `rsa` (extends `FragmentActivity`).
* **Framework:** Injects `Laylf;` (Dagger/TikTok framework lifecycle coordinator) and delegates to peer `Lrty;`.
* **Touch Dispatch:**
  - `MainActivity.dispatchTouchEvent` delegates to `rtz.z(MotionEvent)`.
  - `YouTubePlayerOverlaysLayout.dispatchTouchEvent` wraps superclass call with NPE guard catching uninitialized overlay components.

---

## 3. Comprehensive Feature Feasibility Matrix

| Feature | Category | Feasibility | Technical Prerequisites | Blockers / Risks |
|---|---|---|---|---|
| **SponsorBlock** | Playback | **FEASIBLE WITH HOOKS** | Active video ID resolution; continuous timeline observer; safe seekTo | Internal seek is SABR-based; need higher-level ExoPlayer seek |
| **Background Audio** | Playback | **BLOCKED (ENTITLEMENT)** | BackgroundPlayerService control; AudioFocus management | Entitlement checks in `Lasll`; activity pause hooks |
| **Video Quality** | Playback | **FEASIBLE WITH HOOKS** | SelectableFormats protobuf interceptor; ProtoDataStore sync | Dynamic ABR overrides static quality on network jitter |
| **Captions** | Playback | **FEASIBLE WITH HOOKS** | SubtitleWindowView binding; CaptionMediaSegmentHolder | Track selection logic is decoupled from window view |
| **Gestures** | UI / Touch | **FEASIBLE WITH HOOKS** | YouTubePlayerOverlaysLayout touch interceptor; AudioManager | Multi-layer overlays cause swipe target conflicts |
| **Watch Page** | UI | **FEASIBLE WITH HOOKS** | WatchFeedResizeBehavior layout params; View visibility | Litho / Elements component trees generate UI dynamically |
| **Home & Feed** | UI / Content | **BLOCKED (NO INJECTION POINT)** | Browse response protobuf interceptor | Items rendered by native Element engine; no simple adapter hook |
| **Shorts** | UI / Playback | **FEASIBLE WITH HOOKS** | ShortsPlayerProgressPresenter override; ViewPager control | Auto-advance requires synthetic gesture dispatch |
| **Tabs** | Navigation | **FEASIBLE WITH HOOKS** | PivotBar view enumeration and layout adjust | PivotBar dynamically creates tabs from backend config |
| **Top Bar** | Navigation | **FEASIBLE WITH HOOKS** | MainCollapsingToolbarLayout child visibility | Toolbar items inflated dynamically per account/cast state |
| **Downloads** | Storage | **BLOCKED (PROPRIETARY DRM)** | Custom stream fetcher and FFmpeg remuxer | Widevine DRM and encrypted cache used by official app |
| **General Settings** | Settings | **FEASIBLE STANDALONE** | Standalone Settings Activity / SharedPreferences | None (Already verified in companion app preview) |
| **Privacy Settings** | Settings | **FEASIBLE STANDALONE** | SharedPreferences reset, zero telemetry, backup disabled | None (Already verified in companion app preview) |

---

## 4. Practical Android Device Test Plan

This reproducible test plan verifies physical Android device behaviors without relying on emulators.

### Prerequisites:
- Physical Android phone with USB Debugging enabled (Android 8.0+ / API 26+).
- Connected via ADB (`adb devices -l`).
- Test APK: `app/build/outputs/apk/debug/app-debug.apk`.

### Test Cases:

| Case ID | Feature Area | Test Action | Expected Result | Pass Criteria |
|---|---|---|---|---|
| **DEV-01** | App Installation | `adb install -r app-debug.apk` | App installs cleanly with code `Success` | Returncode 0, package visible in `pm list packages` |
| **DEV-02** | Cold Launch & UI | Launch MarufYT Preview from launcher | Main activity renders with 13 section cards and availability badges | No crashes, system insets respected |
| **DEV-03** | Appearance Toggle | Select Light, Dark, System in General Settings | UI updates theme dynamically | State persists across app kill and relaunch |
| **DEV-04** | Privacy Reset | Tap "Reset Settings" in Privacy section | Appearance preference resets to default System | SharedPreferences cleared, UI refreshes |
| **DEV-05** | Zero Network | Inspect logcat with network monitor active | No outbound sockets or HTTP connections created | Zero internet permission declared, 0 network syscalls |
| **DEV-06** | SponsorBlock CLI | Run `python tools/sponsorblock_lookup.py <valid_url>` | Returns parsed segments or empty array for valid video | JSON stdout, 0 crash, TLS certificate validated |
| **DEV-07** | Clock Timeline Sync | Test rational clock conversion with simulated tick input | Converts microseconds to milliseconds correctly | No overflow, sentinels rejected |

---

## 5. Next Implementation Roadmap

### Milestone 1: SponsorBlock & Timeline Integration Readiness
- Implement high-level ExoPlayer controller hook mapping (avoiding SABR `onSabrSeek` pitfalls).
- Build active video ID state holder that listens to navigation transitions.
- Wire local SponsorBlock client cache to playback position updates.

### Milestone 2: Background Playback & Entitlement Bypass Research
- Analyze `Lasll` entitlement verification bytecode and experiment flag structures.
- Map `AudioManager.requestAudioFocus` contracts.
- Prototype Activity lifecycle decoupling to prevent pause on `onStop()`.

### Milestone 3: Interface & Navigation Customization
- Implement `PivotBar` item filter to allow hiding unwanted tabs (Shorts, Create, Subscriptions).
- Implement gesture volume/brightness overlay on `YouTubePlayerOverlaysLayout`.
- Add Shorts progress bar styling options via `ShortsPlayerProgressPresenter`.

### Milestone 4: Settings Integration
- Connect standalone companion settings to shared preference store accessible by hook runtime (e.g., World-readable SharedPreferences or ContentProvider).
- Provide toggle switches for SponsorBlock categories, gesture controls, and tab visibility.

---

## 6. Verification & Test Evidence

- **Python Tests:** 65 passed (all 51 prior tests preserved + 14 new semantic contract tests).
- **Gradle Verification:** `test assembleDebug lintDebug` passed in 12 seconds with 0 errors.
- **Repository Integrity:** Clean working tree, source-only, no proprietary binaries or secrets committed.
