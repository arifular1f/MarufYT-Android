# Phase 2B: MarufYT feature mapping

All Android features below are **not implemented**. Class existence and exact signatures are verified in [the inventory](PHASE2B_FINGERPRINT_INVENTORY.json); their roles and implementation feasibility are inferences, not runtime results. The [fingerprint report](PHASE2B_FINGERPRINT_REPORT.md) provides full package paths, DEX locations, resources, field samples and uncertainties. HIGH means strong evidence for the stated structural claim, not a working feature.

iOS reference: the existing MarufYT feature documentation reviewed in Phase 2A (README, docs/FEATURE_MATRIX.md, Documentation/MODULES.md and settings names). This phase reads the prior [migration mapping](IOS_TO_ANDROID_FEATURE_MAPPING.md); no iOS source is changed. Objective-C++ hooks, UIKit and iOS selectors cannot be reused as Android hooks.

| iOS feature | Identified Android candidates / evidence | Feasibility and missing information | Mapping confidence |
| --- | --- | --- | --- |
| Background Audio | BackgroundPlayerService, classes2.dex, onStartCommand(Intent, int, int); non-exported manifest media-playback service; offline_prefs declares background_audio_policy | Existing service/settings boundaries are real. Entitlement, audio focus, active engine and lifecycle still need tracing; no background-playback implementation | MEDIUM |
| Video Quality | VideoQualityPrefsFragment.aS()V, classes4.dex, contains resource literals for three quality XML screens; mobile/wifi auto/high/low keys observed | Preferences are identifiable; mapping choices to actual stream selection and experiments remains unverified | MEDIUM |
| Captions | SubtitleWindowView.onMeasure(II)V/onLayout(ZIIII)V in classes6.dex; id/caption_toggle; CaptionMediaSegmentHolder in classes2.dex | Subtitle rendering boundary identifiable; track selection, language and availability controller unresolved | MEDIUM |
| Gestures | MainActivity.dispatchTouchEvent(MotionEvent)Z and its explicit call to Lrtz;->z(MotionEvent)Z; overlay/PivotBar touch methods | Android input boundaries identifiable; consuming a touch event is not proof of a player gesture policy. Volume, brightness, seek and accessibility interactions unresolved | LOW |
| SponsorBlock | PlaybackControllerWrapper.c()Time, i(SabrSeek)V; player/progress classes and network boundary | Research opportunity only. No integration identified by the selectors. Video ID, clock/time scale, safe seek, consent and API behavior all unresolved | LOW |
| Watch Page | watchwhile.MainActivity, YouTubePlayerOverlaysLayout; WatchFeedResizeBehavior, classes5.dex | Host/view composition visible; current watch renderer/controller and server-experiment layout selection unresolved | MEDIUM |
| Home & Feed | SnappyRecyclerView, home-tabs DefaultTabsBar; home_tabs_bar resources | Reusable UI containers identified, not Home-specific data/filter ownership. Browse pipeline and response-to-renderer mapping unresolved | LOW |
| Shorts | ReelWatchPagerViewPager, ShortsPlayerProgressPresenter.onDraw(Canvas)V, classes4.dex; ReelRecyclerView; reel_watch layouts | Pager/progress structure visible; per-video identity, seek/lifecycle and active controller unresolved | MEDIUM |
| Tabs | PivotBar and two DefaultTabsBar classes, classes2.dex; id/pivot_bar | Navigation views identifiable. Tab model, order, labels, account/experiment routing and click destinations unresolved | MEDIUM |
| Top Bar | MainCollapsingToolbarLayout, classes.dex; b(RecyclerView)V; resource IDs for toolbar/appbar/masthead | Collapsing toolbar boundary exists. Host action ownership, visibility and accessibility effects unresolved | MEDIUM |
| Downloads | OfflineKeepAliveService and OfflineUserInitiatedDataTransferJobService; OfflinePrefsFragment/SmartDownloadsPrefsFragment; offline_prefs XML | Existing offline plumbing is not a supported MarufYT download integration. Entitlement, content authorization, storage, protected content and actual transfer API unresolved | LOW |
| General Settings | SettingsActivity.onCreate(Bundle)V; a(Preference)Z/b(Preference)Z; GeneralPrefsFragment; ProtoDataStore preference classes referenced by decoded XML | Settings boundary identifiable. Safe host insertion, store schema, persistence and migrations unresolved; no controls added | MEDIUM |
| Privacy | PrivacyPrefsFragment, ClientLogger, QoeLogger, LogSamplerImpl, DiagnosticsReceiver; decoded network policy | Observed policy permits cleartext in base-config while selected domains disallow it; cannot claim global HTTPS. Payloads, native transports, retention/redaction and network sinks require audit | MEDIUM |

## Important distinctions

Directly portable: feature requirements, consent/default policies, category labels and UX concepts, subject to license review. Android-specific: lifecycle, input routing, views, services, persistence, network/storage and accessibility. YouTube-specific: every obfuscated method/resource fingerprint, experiment-dependent controller and internal protocol. Unverified: actual feature behavior and every proposed modification point.

Examples of verified relationships: MainActivity.onCreate invokes an inherited Lrsa; method; BackgroundPlayerService.onCreate invokes Larez;->onCreate and its own d()V; VideoQualityPrefsFragment.aS contains quality-resource literals. These are structural references, not proof of safe injection points or runtime reachability. The player wrapper's SabrSeek parameter is evidence for further study, not a verified externally callable seek API.

No feature should be promoted to feasible-for-release without caller/data-flow analysis, lifecycle/threading constraints, positive and negative compatibility tests and physical-device results. Await explicit approval for any Phase 2C work.
