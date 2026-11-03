# Phase 2B: read-only structural fingerprint report

Date: 2026-11-03 (Asia/Kuala_Lumpur). This report distinguishes observed declarations/explicit references from inferred feature roles and unknown runtime behavior. No YouTube code was executed or modified.

## Mandatory integrity gate

- Exact APK: `C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk`.
- Package: com.google.android.youtube; version: 21.44.528; code: 1561310186.
- File size: 220,576,405 bytes.
- Expected, initial and final SHA-256: `55be430ce82dcedcb737ea27d1b78576737b75d11cde04aa89989e5376d3ae6c`.
- Gate PASSED. The reusable script hashes before opening DEX/resources/native metadata, then compares SDK-decoded package/name/code with configured expected identity. Hash/identity mismatches abort. Identity extraction itself is the only inspection allowed before the complete gate passes.
- Source was opened read-only. Matching full-file hashes before and after provide cryptographic evidence that its bytes are unchanged. No source replacement, re-signing, extraction back into the APK or modified APK output exists.
- Fresh apksigner verification also passes for v3/v3.1 and source stamp. This is not independent publisher-provenance or stable-channel proof.

## Coverage and evidence rules

The [machine-readable inventory](PHASE2B_FINGERPRINT_INVENTORY.json) validates against [FINGERPRINT_SCHEMA.json](FINGERPRINT_SCHEMA.json). It records version/hash identity, declaration locations, method prototypes, flags, instruction lengths/hashes, fields, resource IDs/resolved paths, manifest contracts, ELF metadata and feature mappings.

- All eight root DEX metadata tables scanned: 57,767 class definitions.
- Selected declarations: 89 classes (49 name-query candidates plus 40 defined ancestors, at most two superclass levels), 1,485 methods, 869 fields.
- SDK-disassembled classes with exact independent method-declaration agreement: 21.
- Resource table declarations indexed: 28,524; selected resource fingerprints: 210.
- Manifest components/aliases/application: 145; native .so entries: 156.
- Relationships: 2,844 explicit invoke references, 89 superclass declarations, 68 resource literals and 21 manifest aliases (3,022 total). Duplicate calls from the same source to the same target are deduplicated; these are not execution counts.
- Five resource XML/layout files decoded after resolving symbolic names to obfuscated ZIP paths. No unresolved tool/resource failures in the final run.

HIGH means directly observed identity/declaration/explicit relationship. MEDIUM means plausible feature association supported by structural evidence. LOW means an opportunity or weakly resolved association. A class can have HIGH-confidence existence while its feature role remains LOW. Method names and typed arguments do not prove implementation semantics. Invoke targets may be inherited, virtual, native, generated or unreachable at runtime. Resource literals establish constant presence, not a resolved UI/data-flow edge.

This is a comprehensive study of the requested twelve areas with explicitly bounded coverage, not a decompilation or semantic audit of all 57,767 classes. No blanket absence claim is based on the 49 selection candidates. Obfuscated transitive call graphs, reflection, server experiments, native implementations, protected media and runtime state remain unresolved.

## DEX identity

| DEX | Defined classes | Method ID references | SHA-256 |
| --- | ---: | ---: | --- |
| classes.dex | 4765 | 65527 | `1acd158fa071504402ce3e3170209670e7bfe76a5a61e01a7a82b2a21e6cddab` |
| classes2.dex | 6372 | 65533 | `c1f2e214a660fdcea7f518951ff603fbbd0524d0a63e229d21f3a738242327d3` |
| classes3.dex | 9490 | 65533 | `63b2ca0ee6fc99253d9b58154866a190ebe75f0006502f66a1fbf8d83bbc5877` |
| classes4.dex | 7660 | 65536 | `5105cb038fa14797a250994eca3112415b57408fa0a49c6e9853c9a2fdde3e62` |
| classes5.dex | 8806 | 65536 | `c1f210c83bb6729707c70ce982aa95c64e73d9c50c2e552290478f3808fe6b59` |
| classes6.dex | 8485 | 65536 | `04d8598f35c3d2cc85b045401edd6ad69aacb656a9c63d7a0dab10b5cd44bb6a` |
| classes7.dex | 11539 | 55256 | `aee149f648de1cfde635250d7f393c7ba35bb14b7a9703da3ff1ebd0992db753` |
| classes8.dex | 650 | 5696 | `9432a28f39b98edb49ec34a33d84b85fc9c3da9234ef692c0a7678c7f5a9a725` |

Method ID counts include references, not only definitions. The reader supports DEX 035; other formats fail explicitly. Member metadata and instruction bytes are bounded by offsets and validated archive/DEX integrity checks. Instruction hashes exclude try/catch tables/debug metadata and are exact-build evidence, not semantic signatures.

## 1. Application startup and main activity

Feature-role confidence: **HIGH**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/apps/youtube/app/YouTubeTikTokRoot_Application;`<br>classes.dex | `Lijs;` | No identifiable non-constructor declaration | None declared |
| `Lcom/google/android/apps/youtube/app/watchwhile/MainActivity;`<br>classes.dex | `Lrsa;` | `onCreate(Landroid/os/Bundle;)V`<br>`dispatchTouchEvent(Landroid/view/MotionEvent;)Z` | `m:Lrty;`<br>`n:Laylf;` |
| `Lcom/google/android/apps/youtube/app/application/Shell_UrlActivity;`<br>classes4.dex | `Lird;` | `onCreate(Landroid/os/Bundle;)V`<br>`n()Lirq;`<br>`o()V` | `l:Lirq;`<br>`m:Laylf;` |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** `com.google.android.apps.youtube.app.YouTubeTikTokRoot_Application`; `com.google.android.apps.youtube.app.application.Shell_UrlActivity`; `com.google.android.apps.youtube.app.application.Shell$UrlActivity`; `com.google.android.youtube.UrlActivity`; `com.google.android.youtube.InternalUrlActivity`; `com.google.android.apps.youtube.app.watchwhile.MainActivity`; `com.google.android.youtube.app.honeycomb.Shell$Icon1Activity`; `com.google.android.youtube.app.honeycomb.Shell$Icon2Activity`; `com.google.android.youtube.app.honeycomb.Shell$Icon3Activity`; `com.google.android.apps.youtube.app.application.InternalShell_HomeActivity`; `com.google.android.apps.youtube.app.application.Shell_HomeActivity`; `com.google.android.youtube.HomeActivity`; `com.google.android.youtube.app.application.Shell$HomeActivity`; `com.google.android.youtube.app.honeycomb.Shell$HomeActivity`; `com.google.android.apps.youtube.app.watchwhile.WatchWhileActivity`; `com.google.android.apps.youtube.app.watchwhile.InternalMainActivity`; `com.google.android.apps.youtube.app.WatchWhileActivity`

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `id/watch_while_layout` = `0x7f0b18d1`
- `id/watch_while_layout_coordinator_layout` = `0x7f0b18d2`
- `id/watch_while_time_bar_view` = `0x7f0b18d3`
- `id/watch_while_time_bar_view_overlay` = `0x7f0b18d4`
- `id/watch_while_time_bar_view_stub` = `0x7f0b18d5`
- `id/watch_while_timebar_overlay_stub` = `0x7f0b18d6`
- `layout/watch_while_activity_animation_view_stub_resized` = `0x7f0e0976` -> `res/cP5.xml`
- `layout/watch_while_activity_with_drawer_and_next_gen_view_stub_and_bottom_bar_refactor_for_player_reparenting_fullscreen` = `0x7f0e097a` -> `res/pED.xml`
- `layout/watch_while_activity_with_drawer_and_next_gen_view_stub_and_bottom_bar_refactor_for_player_reparenting_optimized_fullscreen` = `0x7f0e097b` -> `res/Z3u.xml`
- `layout/watch_while_activity_with_drawer_and_next_gen_view_stub_and_bottom_bar_refactor_fullscreen` = `0x7f0e097c` -> `res/Xoz.xml`
- Additional selected IDs are in the inventory area entry.

**Observed relationships:**
- Explicit invoke: `Lcom/google/android/apps/youtube/app/watchwhile/MainActivity;->C()Lrty;` -> `Lcom/google/android/apps/youtube/app/watchwhile/MainActivity;->n()V`.
- Explicit invoke: `Lcom/google/android/apps/youtube/app/watchwhile/MainActivity;->applyOverrideConfiguration(Landroid/content/res/Configuration;)V` -> `Lcom/google/android/apps/youtube/app/watchwhile/MainActivity;->getBaseContext()Landroid/content/Context;`.
- Explicit invoke: `Lcom/google/android/apps/youtube/app/watchwhile/MainActivity;->dispatchKeyEvent(Landroid/view/KeyEvent;)Z` -> `Lcom/google/android/apps/youtube/app/watchwhile/MainActivity;->C()Lrty;`.

**Unknown/unresolved:**
- Full injected startup graph and experiment configuration are unresolved.

## 2. Navigation and tabs

Feature-role confidence: **MEDIUM**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/apps/youtube/app/common/ui/navigationbar/NavigationBarDividerLayout;`<br>classes.dex | `Landroid/view/ViewGroup;` | `onDraw(Landroid/graphics/Canvas;)V`<br>`onMeasure(II)V`<br>`onLayout(ZIIII)V` | `a:Landroid/graphics/Paint;`<br>`b:I` |
| `Lcom/google/android/libraries/youtube/rendering/ui/hometabs/DefaultTabsBar;`<br>classes2.dex | `Lavgl;` | `dispatchTouchEvent(Landroid/view/MotionEvent;)Z`<br>`onLayout(ZIIII)V` | `A:Lj$/util/Optional;`<br>`B:I` |
| `Lcom/google/android/libraries/youtube/rendering/ui/pivotbar/PivotBar;`<br>classes2.dex | `Lavni;` | `dispatchTouchEvent(Landroid/view/MotionEvent;)Z`<br>`v(Landroid/content/Context;)V`<br>`a(II)Landroid/content/res/ColorStateList;` | `a:Ljava/util/List;`<br>`b:Landroid/content/res/Resources;` |
| `Lcom/google/android/libraries/youtube/rendering/ui/tabs/DefaultTabsBar;`<br>classes2.dex | `Lavni;` | `onLayout(ZIIII)V`<br>`I(Landroid/view/View;)F`<br>`J(Landroid/view/View;)I` | `F:I`<br>`G:F` |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** None directly associated by exact selected-class or alias-target identity; this does not prove no runtime relationship.

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `id/home_tabs_bar` = `0x7f0b0943`
- `id/home_tabs_bar_host` = `0x7f0b0944`
- `id/pivot_back` = `0x7f0b0efd`
- `id/pivot_bar` = `0x7f0b0efe`
- `id/pivot_bar_thumbnail` = `0x7f0b0eff`
- `id/pivot_bar_thumbnail_back_last` = `0x7f0b0f00`
- `id/pivot_bar_thumbnail_back_last_mask` = `0x7f0b0f01`
- `id/pivot_bar_thumbnail_back_middle` = `0x7f0b0f02`
- `id/pivot_bar_thumbnail_back_middle_mask` = `0x7f0b0f03`
- `id/pivot_header` = `0x7f0b0f04`
- Additional selected IDs are in the inventory area entry.

**Observed relationships:**
- Explicit invoke: `Lcom/google/android/libraries/youtube/rendering/ui/hometabs/DefaultTabsBar;-><init>(Landroid/content/Context;)V` -> `Lcom/google/android/libraries/youtube/rendering/ui/hometabs/DefaultTabsBar;->O(Landroid/content/Context;Landroid/util/AttributeSet;)V`.
- Explicit invoke: `Lcom/google/android/libraries/youtube/rendering/ui/hometabs/DefaultTabsBar;-><init>(Landroid/content/Context;Landroid/util/AttributeSet;)V` -> `Lcom/google/android/libraries/youtube/rendering/ui/hometabs/DefaultTabsBar;->O(Landroid/content/Context;Landroid/util/AttributeSet;)V`.
- Explicit invoke: `Lcom/google/android/libraries/youtube/rendering/ui/hometabs/DefaultTabsBar;-><init>(Landroid/content/Context;Landroid/util/AttributeSet;I)V` -> `Lcom/google/android/libraries/youtube/rendering/ui/hometabs/DefaultTabsBar;->O(Landroid/content/Context;Landroid/util/AttributeSet;)V`.

**Unknown/unresolved:**
- Tab models, ordering and server-driven routing are not resolved.

## 3. Home and feed architecture

Feature-role confidence: **MEDIUM**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/apps/youtube/app/common/ui/inline/DefaultInlinePlaybackLifecycleController;`<br>classes.dex | `Ljava/lang/Object;` | `onCreate(Lcwm;)V`<br>`stateTransitionDetails(I)Ljava/lang/String;`<br>`t(ILkmg;)Z` | `a:Landroid/os/Handler;`<br>`b:I` |
| `Lcom/google/android/apps/youtube/app/common/rendering/SnappyRecyclerView;`<br>classes.dex | `Landroid/support/v7/widget/RecyclerView;` | `a(I)I`<br>`at(II)Z`<br>`onAttachedToWindow()V` | `ah:Z`<br>`ai:I` |
| `Lcom/google/android/apps/youtube/app/common/ui/navigation/BrowseBackgroundBehavior;`<br>classes4.dex | `Lccl;` | `n(Landroid/view/View;)Z`<br>`nW(Landroidx/coordinatorlayout/widget/CoordinatorLayout;Landroid/view/View;Landroid/view/View;)Z`<br>`nX(Landroidx/coordinatorlayout/widget/CoordinatorLayout;Landroid/view/View;I)Z` | `a:Landroid/view/View;` |
| `Lcom/google/android/apps/youtube/app/watch/nextgenwatch/overscroll/WatchFeedResizeBehavior;`<br>classes5.dex | `Lccl;` | `O()I`<br>`P()Lafti;`<br>`Q()V` | `a:Landroid/content/Context;`<br>`b:Lbtqv;` |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** None directly associated by exact selected-class or alias-target identity; this does not prove no runtime relationship.

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `id/feed_tabbed_back` = `0x7f0b080f`
- `id/feed_tabbed_header` = `0x7f0b0810`
- `id/feed_tabbed_header_title_text` = `0x7f0b0811`
- `id/feed_tabbed_more` = `0x7f0b0812`
- `id/home_tabs_bar` = `0x7f0b0943`
- `id/home_tabs_bar_host` = `0x7f0b0944`
- `layout/feed_channel_filter_header` = `0x7f0e0271` -> `res/007.xml`
- `layout/feed_filter_bar` = `0x7f0e0272` -> `res/Cs2.xml`
- `layout/feed_filter_bar_with_overlay` = `0x7f0e0273` -> `res/FLZ.xml`
- `layout/feed_tabbed_header` = `0x7f0e0274` -> `res/UR7.xml`
- Additional selected IDs are in the inventory area entry.

**Observed relationships:**
- Explicit invoke: `Lcom/google/android/apps/youtube/app/common/rendering/SnappyRecyclerView;->at(II)Z` -> `Lcom/google/android/apps/youtube/app/common/rendering/SnappyRecyclerView;->a(I)I`.
- Explicit invoke: `Lcom/google/android/apps/youtube/app/common/rendering/SnappyRecyclerView;->onAttachedToWindow()V` -> `Lcom/google/android/apps/youtube/app/common/rendering/SnappyRecyclerView;->getContext()Landroid/content/Context;`.
- Explicit invoke: `Lcom/google/android/apps/youtube/app/watch/nextgenwatch/overscroll/WatchFeedResizeBehavior;->Q()V` -> `Lcom/google/android/apps/youtube/app/watch/nextgenwatch/overscroll/WatchFeedResizeBehavior;->P()Lafti;`.

**Unknown/unresolved:**
- Renderer data pipeline and Home filtering controller remain obfuscated; a reusable list class is not a Home-specific entry point.

## 4. Video player architecture

Feature-role confidence: **MEDIUM**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/apps/youtube/app/common/player/overlay/YouTubePlayerOverlaysLayout;`<br>classes.dex | `Lasxl;` | `dispatchTouchEvent(Landroid/view/MotionEvent;)Z`<br>`onMeasure(II)V`<br>`onLayout(ZIIII)V` | `A:Ljava/util/Set;`<br>`B:Z` |
| `Lcom/google/android/apps/youtube/app/player/YouTubePlayerViewNotForReflection;`<br>classes.dex | `Ljqf;` | `onLayout(ZIIII)V`<br>`d()Z`<br>`a(Ljqy;)V` | `a:Z`<br>`b:Ljkt;` |
| `Lcom/google/android/libraries/youtube/media/interfaces/PlaybackController;`<br>classes2.dex | `Ljava/lang/Object;` | `A(Lcom/google/android/libraries/youtube/media/interfaces/DeferredMediaCache;)V`<br>`B(Lcom/google/android/libraries/youtube/media/interfaces/SabrDataProviderWrapper;)V`<br>`a()V` | None declared |
| `Lcom/google/android/libraries/youtube/player/ui/PlayerView;`<br>classes2.dex | `Lasxl;` | `h()V` | `d:Lapru;`<br>`e:Lcjk;` |
| `Lcom/google/android/libraries/youtube/media/player/exo2/platypus/PlaybackControllerWrapper;`<br>classes2.dex | `Lcom/google/android/libraries/youtube/media/interfaces/PlaybackControllerCallbacks;` | `P()Ljava/util/ArrayList;`<br>`Q()V`<br>`R()V` | `A:Ljava/util/concurrent/atomic/AtomicBoolean;`<br>`a:Lcom/google/android/libraries/youtube/media/interfaces/PlaybackController;` |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** None directly associated by exact selected-class or alias-target identity; this does not prove no runtime relationship.

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `id/player_control_button` = `0x7f0b0f3d`
- `id/player_control_button_wrapper` = `0x7f0b0f3e`
- `id/player_control_fast_forward_button` = `0x7f0b0f3f`
- `id/player_control_fast_forward_button_touch_area` = `0x7f0b0f40`
- `id/player_control_next_button` = `0x7f0b0f43`
- `id/player_control_next_button_touch_area` = `0x7f0b0f44`
- `id/player_control_play_pause_button` = `0x7f0b0f45`
- `id/player_control_play_pause_replay_button` = `0x7f0b0f46`
- `id/player_control_play_pause_replay_button_touch_area` = `0x7f0b0f47`
- `id/player_control_previous_button` = `0x7f0b0f48`
- Additional selected IDs are in the inventory area entry.

**Observed relationships:**
- Explicit invoke: `Lcom/google/android/apps/youtube/app/common/player/overlay/YouTubePlayerOverlaysLayout;->B(Ljava/util/List;Ljava/util/List;)V` -> `Lcom/google/android/apps/youtube/app/common/player/overlay/YouTubePlayerOverlaysLayout;->D(Lasxj;)V`.
- Explicit invoke: `Lcom/google/android/apps/youtube/app/common/player/overlay/YouTubePlayerOverlaysLayout;->C(Ljava/util/Map;)V` -> `Lcom/google/android/apps/youtube/app/common/player/overlay/YouTubePlayerOverlaysLayout;->D(Lasxj;)V`.
- Explicit invoke: `Lcom/google/android/apps/youtube/app/common/player/overlay/YouTubePlayerOverlaysLayout;->D(Lasxj;)V` -> `Lcom/google/android/apps/youtube/app/common/player/overlay/YouTubePlayerOverlaysLayout;->removeView(Landroid/view/View;)V`.

**Unknown/unresolved:**
- Obfuscated method semantics, active engine selection, native dispatch and video identity ownership need additional tracing.

## 5. Background playback components

Feature-role confidence: **MEDIUM**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/libraries/youtube/player/background/service/BackgroundPlayerService;`<br>classes2.dex | `Larez;` | `onCreate()V`<br>`onStartCommand(Landroid/content/Intent;II)I`<br>`onBind(Landroid/content/Intent;)Landroid/os/IBinder;` | `g:Lazii;`<br>`a:Laspm;` |
| `Lcom/google/android/libraries/youtube/mdx/background/MdxBackgroundPlaybackBroadcastReceiver;`<br>classes6.dex | `Lanpx;` | `onReceive(Landroid/content/Context;Landroid/content/Intent;)V` | `c:Lankl;`<br>`d:Lanpv;` |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** `com.google.android.libraries.youtube.player.background.service.BackgroundPlayerService`; `com.google.android.libraries.youtube.mdx.background.MdxBackgroundPlaybackBroadcastReceiver`

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `array/background_audio_policy_entries` = `0x7f030005`
- `array/background_audio_policy_values` = `0x7f030006`

**Observed relationships:**
- Explicit invoke: `Lcom/google/android/libraries/youtube/player/background/service/BackgroundPlayerService;->onBind(Landroid/content/Intent;)Landroid/os/IBinder;` -> `Lcom/google/android/libraries/youtube/player/background/service/BackgroundPlayerService;->d()V`.
- Explicit invoke: `Lcom/google/android/libraries/youtube/player/background/service/BackgroundPlayerService;->onCreate()V` -> `Lcom/google/android/libraries/youtube/player/background/service/BackgroundPlayerService;->d()V`.

**Unknown/unresolved:**
- Entitlement decisions, audio-focus ownership and eligibility conditions are not established.

## 6. Shorts architecture

Feature-role confidence: **MEDIUM**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/apps/youtube/app/extensions/reel/shorts/ShortsPlayerProgressPresenter;`<br>classes4.dex | `Landroid/view/View;` | `onDraw(Landroid/graphics/Canvas;)V`<br>`d(Landroid/graphics/Canvas;FFFFLandroid/graphics/Paint;)V`<br>`a(Lblpb;ZIIIF)V` | `a:J`<br>`b:J` |
| `Lcom/google/android/apps/youtube/app/extensions/reel/watch/fragment/ReelWatchPagerViewPager;`<br>classes4.dex | `Lafvg;` | `onInterceptTouchEvent(Landroid/view/MotionEvent;)Z`<br>`onTouchEvent(Landroid/view/MotionEvent;)Z` | `h:Z`<br>`i:Z` |
| `Lcom/google/android/apps/youtube/app/extensions/reel/watch/player/ReelScrubbedPreviewView;`<br>classes4.dex | `Lmqn;` | `d()I`<br>`e(J)V` | `a:Latub;` |
| `Lcom/google/android/libraries/youtube/reel/internal/pager/ReelRecyclerView;`<br>classes6.dex | `Landroid/support/v7/widget/RecyclerView;` | `aO(Landroid/view/ViewGroup;FF)Landroid/view/View;`<br>`a(Z)V`<br>`aM(Lcom/google/android/libraries/youtube/reel/internal/fragment/ReelTouchCaptureView;)V` | `ah:Z`<br>`ai:Latub;` |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** None directly associated by exact selected-class or alias-target identity; this does not prove no runtime relationship.

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `id/reel_watch_fragment_root` = `0x7f0b1205`
- `id/reel_watch_pager_view_pager` = `0x7f0b1206`
- `id/reel_watch_player` = `0x7f0b1207`
- `id/reel_watch_refresher` = `0x7f0b1208`
- `id/reel_watch_splash_screen_container` = `0x7f0b1209`
- `id/reel_watch_splash_screen_stub` = `0x7f0b120a`
- `id/reel_watch_splash_screen_title` = `0x7f0b120b`
- `id/reel_watch_survey_element_container` = `0x7f0b120c`
- `layout/reel_watch_fragment` = `0x7f0e06a0` -> `res/nb_.xml`
- `layout/reel_watch_fragment_linear` = `0x7f0e06a1` -> `res/NR1.xml`
- Additional selected IDs are in the inventory area entry.

**Observed relationships:**
- Explicit invoke: `Lcom/google/android/apps/youtube/app/extensions/reel/shorts/ShortsPlayerProgressPresenter;->a(Lblpb;ZIIIF)V` -> `Lcom/google/android/apps/youtube/app/extensions/reel/shorts/ShortsPlayerProgressPresenter;->b()V`.
- Explicit invoke: `Lcom/google/android/apps/youtube/app/extensions/reel/shorts/ShortsPlayerProgressPresenter;->a(Lblpb;ZIIIF)V` -> `Lcom/google/android/apps/youtube/app/extensions/reel/shorts/ShortsPlayerProgressPresenter;->getContext()Landroid/content/Context;`.
- Explicit invoke: `Lcom/google/android/apps/youtube/app/extensions/reel/shorts/ShortsPlayerProgressPresenter;->a(Lblpb;ZIIIF)V` -> `Lcom/google/android/apps/youtube/app/extensions/reel/shorts/ShortsPlayerProgressPresenter;->getHeight()I`.

**Unknown/unresolved:**
- Shorts controller, active video lifecycle and seek behavior remain unverified.

## 7. Captions and playback controls

Feature-role confidence: **MEDIUM**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/apps/youtube/app/common/player/overlay/InlineTimeBarWrapper;`<br>classes.dex | `Ljry;` | `onMeasure(II)V`<br>`onLayout(ZIIII)V` | `a:Ljsi;`<br>`b:Z` |
| `Lcom/google/android/libraries/youtube/media/player/exo2/platypus/mediapush/CaptionMediaSegmentHolder;`<br>classes2.dex | `Lcom/google/android/libraries/youtube/media/player/exo2/platypus/mediapush/MediaSegmentHolder;` | `N(Lcom/google/android/libraries/youtube/media/player/exo2/platypus/mediapush/BufferedMediaSegment;JJ)V`<br>`a(J)V`<br>`b()V` | `L:Z`<br>`M:Lbbqp;` |
| `Lcom/google/android/apps/youtube/app/player/autonav/AutonavSwitch;`<br>classes4.dex | `Landroid/support/v7/widget/SwitchCompat;` | No identifiable non-constructor declaration | None declared |
| `Lcom/google/android/libraries/youtube/player/subtitles/ui/SubtitleWindowView;`<br>classes6.dex | `Landroid/view/ViewGroup;` | `onMeasure(II)V`<br>`onLayout(ZIIII)V` | `a:Z`<br>`b:Landroid/content/res/Resources;` |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** None directly associated by exact selected-class or alias-target identity; this does not prove no runtime relationship.

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `id/caption_toggle` = `0x7f0b0348`
- `id/caption_toggle_container` = `0x7f0b0349`
- `id/player_control_button` = `0x7f0b0f3d`
- `id/player_control_button_wrapper` = `0x7f0b0f3e`
- `id/player_control_fast_forward_button` = `0x7f0b0f3f`
- `id/player_control_fast_forward_button_touch_area` = `0x7f0b0f40`
- `id/player_control_next_button` = `0x7f0b0f43`
- `id/player_control_next_button_touch_area` = `0x7f0b0f44`
- `id/player_control_play_pause_button` = `0x7f0b0f45`
- `id/player_control_play_pause_replay_button` = `0x7f0b0f46`
- Additional selected IDs are in the inventory area entry.

**Observed relationships:**
- Explicit invoke: `Lcom/google/android/libraries/youtube/player/subtitles/ui/SubtitleWindowView;-><init>(Landroid/content/Context;)V` -> `Lcom/google/android/libraries/youtube/player/subtitles/ui/SubtitleWindowView;->m(Landroid/content/Context;Landroid/content/res/Resources;)Laswv;`.
- Explicit invoke: `Lcom/google/android/libraries/youtube/player/subtitles/ui/SubtitleWindowView;-><init>(Landroid/content/Context;Landroid/util/AttributeSet;)V` -> `Lcom/google/android/libraries/youtube/player/subtitles/ui/SubtitleWindowView;->m(Landroid/content/Context;Landroid/content/res/Resources;)Laswv;`.
- Explicit invoke: `Lcom/google/android/libraries/youtube/player/subtitles/ui/SubtitleWindowView;-><init>(Landroid/content/Context;Landroid/util/AttributeSet;I)V` -> `Lcom/google/android/libraries/youtube/player/subtitles/ui/SubtitleWindowView;->m(Landroid/content/Context;Landroid/content/res/Resources;)Laswv;`.

**Unknown/unresolved:**
- Track selection, caption availability and control action dispatch are not traced.

## 8. Player settings and preferences

Feature-role confidence: **MEDIUM**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/apps/youtube/app/settings/SettingsActivity;`<br>classes.dex | `Lphc;` | `onCreate(Landroid/os/Bundle;)V`<br>`g()Lpht;`<br>`h()V` | `b:Lpht;`<br>`c:Laylf;` |
| `Lcom/google/android/libraries/youtube/media/interfaces/PlaybackAgnosticUserPreferences;`<br>classes2.dex | `Ljava/lang/Object;` | `toString()Ljava/lang/String;` | `obf05a8b8b654814373668ec64c0c3fab5a737335f5663138c7b95885e6a972cb25:I`<br>`obf7bf586a3980b19e00c5c528b70e080ef2092b902b4d9413fa7f273b43b0ebcf3:I` |
| `Lcom/google/android/apps/youtube/app/settings/GeneralPrefsFragment;`<br>classes4.dex | `Lpih;` | `aS()V`<br>`aX(Ljava/lang/CharSequence;)V`<br>`aZ()V` | `aA:Lauid;`<br>`aB:Lnjt;` |
| `Lcom/google/android/apps/youtube/app/settings/videoquality/VideoQualityPrefsFragment;`<br>classes4.dex | `Lpmh;` | `aS()V`<br>`ag()V`<br>`o()Lbuwz;` | `aj:Lakxt;`<br>`ak:Z` |
| `Lcom/google/android/apps/youtube/app/ui/QuickSeekListPreference;`<br>classes4.dex | `Lcom/google/android/libraries/youtube/common/ui/preferences/ProtoDataStoreListPreference;` | `m()Ljava/lang/CharSequence;` | None declared |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** `com.google.android.apps.youtube.app.settings.SettingsActivity`

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `id/menu_settings` = `0x7f0b0c32`
- `id/quality_button` = `0x7f0b10bb`
- `xml/general_prefs` = `0x7f180014` -> `res/HCa.xml`
- `xml/video_audio_quality_prefs` = `0x7f18002c` -> `res/OAl.xml`
- `xml/videoquality_nonbeta_prefs` = `0x7f18002d` -> `res/MrS.xml`
- `xml/videoquality_prefs` = `0x7f18002e` -> `res/tQJ.xml`

**Observed relationships:**
- Explicit invoke: `Lcom/google/android/apps/youtube/app/settings/SettingsActivity;->a(Landroidx/preference/Preference;)Z` -> `Lcom/google/android/apps/youtube/app/settings/SettingsActivity;->g()Lpht;`.
- Explicit invoke: `Lcom/google/android/apps/youtube/app/settings/SettingsActivity;->applyOverrideConfiguration(Landroid/content/res/Configuration;)V` -> `Lcom/google/android/apps/youtube/app/settings/SettingsActivity;->getBaseContext()Landroid/content/Context;`.
- Explicit invoke: `Lcom/google/android/apps/youtube/app/settings/SettingsActivity;->b(Landroidx/preference/Preference;)Z` -> `Lcom/google/android/apps/youtube/app/settings/SettingsActivity;->g()Lpht;`.

**Unknown/unresolved:**
- Preference-to-playback synchronization and persistent store schemas are unresolved.

## 9. Download-related components

Feature-role confidence: **MEDIUM**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/libraries/youtube/offline/transfer/service/OfflineKeepAliveService;`<br>classes2.dex | `Landroid/app/Service;` | `onCreate()V`<br>`onStartCommand(Landroid/content/Intent;II)I`<br>`onBind(Landroid/content/Intent;)Landroid/os/IBinder;` | `a:Lbweo;`<br>`b:Lardi;` |
| `Lcom/google/android/apps/youtube/app/settings/OfflinePrefsFragment;`<br>classes4.dex | `Lpij;` | `aS()V`<br>`aU(Ljava/lang/Throwable;)V`<br>`aV(Landroidx/preference/PreferenceCategory;Landroidx/preference/Preference;)V` | `aA:Lkhy;`<br>`aB:Laqyw;` |
| `Lcom/google/android/apps/youtube/app/settings/offline/SmartDownloadsPrefsFragment;`<br>classes4.dex | `Lpkh;` | `aS()V`<br>`aU(Landroidx/preference/Preference;)V`<br>`ag()V` | `aj:Lcom/google/android/apps/youtube/app/settings/offline/SmartDownloadsStorageUseRadioButton;`<br>`ak:Lcom/google/android/apps/youtube/app/settings/offline/SmartDownloadsStorageUseRadioButton;` |
| `Lcom/google/android/libraries/youtube/offline/transfer/service/OfflineUserInitiatedDataTransferJobService;`<br>classes6.dex | `Larbq;` | `onStartJob(Landroid/app/job/JobParameters;)Z`<br>`onStopJob(Landroid/app/job/JobParameters;)Z` | `a:Lbweo;`<br>`b:Lardi;` |
| `Lcom/google/android/libraries/youtube/offline/ui/DownloadNetworkSelectionDialogPreference;`<br>classes6.dex | `Landroidx/preference/Preference;` | No identifiable non-constructor declaration | `a:Lazhf;`<br>`b:Landroid/content/Context;` |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** `com.google.android.libraries.youtube.offline.transfer.service.OfflineKeepAliveService`; `com.google.android.libraries.youtube.offline.transfer.service.OfflineUserInitiatedDataTransferJobService`

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `id/offline_arrow` = `0x7f0b0dc0`
- `id/offline_badge` = `0x7f0b0dc1`
- `id/offline_badge_beside_details` = `0x7f0b0dc2`
- `id/offline_button` = `0x7f0b0dc3`
- `id/offline_candidate_arrow` = `0x7f0b0dc4`
- `id/offline_candidate_layout` = `0x7f0b0dc5`
- `id/offline_downloaded_badge` = `0x7f0b0dc6`
- `id/offline_icon` = `0x7f0b0dc7`
- `id/offline_smart_downloads_bar_layout` = `0x7f0b0dcb`
- `id/offline_storage_controls_widget_layout` = `0x7f0b0dcc`
- Additional selected IDs are in the inventory area entry.

**Observed relationships:**
- Explicit invoke: `Lcom/google/android/libraries/youtube/offline/transfer/service/OfflineKeepAliveService;->a()V` -> `Lcom/google/android/libraries/youtube/offline/transfer/service/OfflineKeepAliveService;->getApplicationInfo()Landroid/content/pm/ApplicationInfo;`.
- Explicit invoke: `Lcom/google/android/libraries/youtube/offline/transfer/service/OfflineKeepAliveService;->a()V` -> `Lcom/google/android/libraries/youtube/offline/transfer/service/OfflineKeepAliveService;->startForeground(ILandroid/app/Notification;)V`.
- Explicit invoke: `Lcom/google/android/libraries/youtube/offline/transfer/service/OfflineKeepAliveService;->onCreate()V` -> `Lcom/google/android/libraries/youtube/offline/transfer/service/OfflineKeepAliveService;->a()V`.

**Unknown/unresolved:**
- Offline entitlement, protected-content handling and transfer pipeline are not audited; no supported downloader is implemented.

## 10. Network and API boundaries

Feature-role confidence: **MEDIUM**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/libraries/youtube/media/player/exo2/platypus/EnvoyNetFetchProvider;`<br>classes2.dex | `Ljava/lang/Object;` | `a(Lcom/google/android/libraries/youtube/media/interfaces/Executor;)Lcom/google/android/libraries/youtube/media/interfaces/NetFetch;`<br>`b(Lcom/google/android/libraries/youtube/media/interfaces/Executor;)Lcom/google/android/libraries/youtube/media/interfaces/NetFetch;`<br>`c(Ljava/lang/Throwable;Ljava/lang/String;)V` | `a:Lcom/google/android/libraries/youtube/media/player/exo2/platypus/ExecutorImpl;`<br>`b:Laprd;` |
| `Lcom/google/android/libraries/youtube/media/player/exo2/platypus/PlaybackNetFetchFactory;`<br>classes2.dex | `Ljava/lang/Object;` | `b(Lapjv;)Lcom/google/android/libraries/youtube/media/player/exo2/platypus/PlaybackNetFetchFactory$Transport;`<br>`a(Lapjv;Lcom/google/android/libraries/youtube/media/interfaces/Executor;)Lcom/google/android/libraries/youtube/media/player/exo2/platypus/PlaybackNetFetchFactory$Transport;` | `a:Laprd;`<br>`b:Lanit;` |
| `Lorg/chromium/net/CronetEngine;`<br>classes3.dex | `Ljava/lang/Object;` | `addRequestFinishedListener(Lorg/chromium/net/RequestFinishedInfo$Listener;)V`<br>`addRttListener(Lorg/chromium/net/NetworkQualityRttListener;)V`<br>`addThroughputListener(Lorg/chromium/net/NetworkQualityThroughputListener;)V` | `ACTIVE_REQUEST_COUNT_UNKNOWN:I`<br>`CONNECTION_METRIC_UNKNOWN:I` |
| `Lorg/chromium/net/impl/CronetUrlRequest;`<br>classes3.dex | `Lorg/chromium/net/ExperimentalUrlRequest;` | `i(ILjava/lang/String;[Ljava/lang/String;ZLjava/lang/String;Ljava/lang/String;JZ)Lbxtl;`<br>`j(Lorg/chromium/net/CronetException;)V`<br>`k(Ljava/lang/Runnable;Ljava/lang/String;)V` | `A:[B`<br>`B:Ljava/nio/ByteBuffer;` |
| `Lcom/google/android/libraries/youtube/composition/assets/net/InnertubeContextProvider;`<br>classes5.dex | `Ljava/lang/Object;` | `a()Lcom/google/android/libraries/youtube/composition/common/types/StatusOr;`<br>`b(Lcom/google/android/libraries/youtube/composition/assets/net/InnertubeServiceType;)Lcom/google/common/util/concurrent/ListenableFuture;`<br>`obfb19b44d906292bdb6cfc166c444e2b33655dc063537d0eadc032987a42c2cff8()Lcom/google/android/libraries/youtube/composition/common/types/StatusOr;` | None declared |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** None directly associated by exact selected-class or alias-target identity; this does not prove no runtime relationship.

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `xml/network_security_config_ct` = `0x7f180021` -> `res/OAv.xml`

**Observed relationships:**
- Superclass/interface declarations are recorded; no SDK invoke study was selected for these particular declarations.

**Unknown/unresolved:**
- Actual endpoint/authentication flows, redirect policy and native transport ownership are not audited.

## 11. SponsorBlock integration opportunities

Feature-role confidence: **LOW**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/libraries/youtube/player/ui/PlayerView;`<br>classes2.dex | `Lasxl;` | `h()V` | `d:Lapru;`<br>`e:Lcjk;` |
| `Lcom/google/android/libraries/youtube/media/player/exo2/platypus/PlaybackControllerWrapper;`<br>classes2.dex | `Lcom/google/android/libraries/youtube/media/interfaces/PlaybackControllerCallbacks;` | `P()Ljava/util/ArrayList;`<br>`Q()V`<br>`R()V` | `A:Ljava/util/concurrent/atomic/AtomicBoolean;`<br>`a:Lcom/google/android/libraries/youtube/media/interfaces/PlaybackController;` |
| `Lcom/google/android/apps/youtube/app/extensions/reel/shorts/ShortsPlayerProgressPresenter;`<br>classes4.dex | `Landroid/view/View;` | `onDraw(Landroid/graphics/Canvas;)V`<br>`d(Landroid/graphics/Canvas;FFFFLandroid/graphics/Paint;)V`<br>`a(Lblpb;ZIIIF)V` | `a:J`<br>`b:J` |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** None directly associated by exact selected-class or alias-target identity; this does not prove no runtime relationship.

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `id/player_control_button` = `0x7f0b0f3d`
- `id/player_control_button_wrapper` = `0x7f0b0f3e`
- `id/player_control_fast_forward_button` = `0x7f0b0f3f`
- `id/player_control_fast_forward_button_touch_area` = `0x7f0b0f40`
- `id/player_control_next_button` = `0x7f0b0f43`
- `id/player_control_next_button_touch_area` = `0x7f0b0f44`
- `id/player_control_play_pause_button` = `0x7f0b0f45`
- `id/player_control_play_pause_replay_button` = `0x7f0b0f46`
- `id/player_control_play_pause_replay_button_touch_area` = `0x7f0b0f47`
- `id/player_control_previous_button` = `0x7f0b0f48`
- Additional selected IDs are in the inventory area entry.

**Observed relationships:**
- Explicit invoke: `Lcom/google/android/libraries/youtube/media/player/exo2/platypus/PlaybackControllerWrapper;-><init>(Lapjv;Lanit;Lcom/google/android/libraries/youtube/media/player/exo2/platypus/mediapush/MediaPushMediaSource;Lcom/google/android/libraries/youtube/media/player/exo2/platypus/mediapush/BufferManagerImpl;Lcom/google/android/libraries/youtube/media/player/exo2/platypus/ErrorHandler;Landroid/os/Handler;Laprw;Laplw;Lcom/google/android/libraries/youtube/media/player/exo2/platypus/PlaybackControllerWrapper$Callbacks;Ljava/util/concurrent/ScheduledExecutorService;Ljava/util/concurrent/Executor;)V` -> `Lcom/google/android/libraries/youtube/media/interfaces/PlaybackControllerCallbacks;-><init>()V`.
- Explicit invoke: `Lcom/google/android/libraries/youtube/media/player/exo2/platypus/PlaybackControllerWrapper;->A(Ljava/lang/String;Lcom/google/android/libraries/youtube/media/player/exo2/platypus/event/PlatypusException;)V` -> `Lcom/google/android/libraries/youtube/media/interfaces/QoeError;-><init>(Ljava/lang/String;Ljava/util/ArrayList;)V`.
- Explicit invoke: `Lcom/google/android/libraries/youtube/media/player/exo2/platypus/PlaybackControllerWrapper;->A(Ljava/lang/String;Lcom/google/android/libraries/youtube/media/player/exo2/platypus/event/PlatypusException;)V` -> `Lcom/google/android/libraries/youtube/media/interfaces/QoeErrorDetail;-><init>(Ljava/lang/String;Ljava/lang/String;)V`.

**Unknown/unresolved:**
- No native SponsorBlock integration was identified by these selectors. Reliable video ID/time/seek and consent boundaries are unproven; this is a design opportunity only.

## 12. Logging and privacy boundaries

Feature-role confidence: **MEDIUM**. Symbol existence is directly observed; role assumptions below do not establish a working feature.

| Class descriptor / DEX | Superclass | Example declared methods | Example fields |
| --- | --- | --- | --- |
| `Lcom/google/android/libraries/youtube/composition/logger/ClientLogger;`<br>classes2.dex | `Ljava/lang/Object;` | `a(Lio/grpc/Status;)V`<br>`b(Lio/grpc/Status;Lcom/google/android/libraries/youtube/composition/WrappedMediaEngineMetadataProto$WrappedMediaEngineMetadata;)V`<br>`c(Lcom/google/android/libraries/youtube/composition/WrappedClientEventProto$WrappedClientEvent;)V` | None declared |
| `Lcom/google/android/libraries/youtube/media/interfaces/QoeLogger;`<br>classes2.dex | `Ljava/lang/Object;` | `a(JJ)V`<br>`b(J)V`<br>`c(Ljava/lang/String;Ljava/lang/String;)V` | None declared |
| `Landroidx/work/impl/diagnostics/DiagnosticsReceiver;`<br>classes4.dex | `Landroid/content/BroadcastReceiver;` | `onReceive(Landroid/content/Context;Landroid/content/Intent;)V` | `a:Ljava/lang/String;` |
| `Landroidx/work/impl/workers/DiagnosticsWorker;`<br>classes4.dex | `Landroidx/work/Worker;` | `c()Ldeh;` | None declared |
| `Lcom/google/android/apps/youtube/app/settings/PrivacyPrefsFragment;`<br>classes4.dex | `Lpik;` | `aS()V`<br>`b()Lbmgu;`<br>`f(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Landroid/os/Bundle;)Landroid/support/v7/widget/RecyclerView;` | `c:Lakyk;`<br>`d:Lavvz;` |
| `Lcom/google/android/libraries/youtube/logging/flogger/PrimesLoggerHolder;`<br>classes6.dex | `Ljava/lang/Object;` | No identifiable non-constructor declaration | `singletonLogger:Lazpc;` |
| `Lcom/google/android/libraries/youtube/logging/sampling/LogSamplerImpl;`<br>classes6.dex | `Ljava/lang/Object;` | `configureLogSampler([B)V`<br>`nativeDisableCoordination(I)V`<br>`nativeShouldCollect(I)[I` | `a:Z`<br>`b:Lanit;` |

Methods/fields above are examples; all selected declarations, exact signatures, flags and instruction fingerprints are in the JSON inventory. Obfuscated names are retained without invented meanings.

**Related manifest identifiers:** `androidx.work.impl.diagnostics.DiagnosticsReceiver`

**Related resource declarations (name association unless an explicit literal/XML relationship is stated):**

- `id/privacy_settings` = `0x7f0b101d`
- `id/privacy_settings_title` = `0x7f0b101e`
- `xml/network_security_config_ct` = `0x7f180021` -> `res/OAv.xml`

**Observed relationships:**
- Explicit invoke: `Lcom/google/android/libraries/youtube/composition/logger/ClientLogger;->obf083bf65d972a3382d4d0900c2896cb9d708a1427675b9b3d767b246b3585ebb9(Lio/grpc/Status;Lcom/google/android/libraries/youtube/composition/WrappedMediaEngineMetadataProto$WrappedMediaEngineMetadata;)V` -> `Lcom/google/android/libraries/youtube/composition/logger/ClientLogger;->b(Lio/grpc/Status;Lcom/google/android/libraries/youtube/composition/WrappedMediaEngineMetadataProto$WrappedMediaEngineMetadata;)V`.
- Explicit invoke: `Lcom/google/android/libraries/youtube/composition/logger/ClientLogger;->obf1830b0cf01dac250d89a83faa5f4a4f8dcf86020195251299d6f09c6cc36da8d(Lio/grpc/Status;)V` -> `Lcom/google/android/libraries/youtube/composition/logger/ClientLogger;->a(Lio/grpc/Status;)V`.
- Explicit invoke: `Lcom/google/android/libraries/youtube/composition/logger/ClientLogger;->obf6a1a3bac2dbfb319f96854a7cd46bdf519aac62baf2f86cf073ed9905e95e4ab(Lcom/google/android/libraries/youtube/composition/WrappedClientEventProto$WrappedClientEvent;)V` -> `Lcom/google/android/libraries/youtube/composition/logger/ClientLogger;->c(Lcom/google/android/libraries/youtube/composition/WrappedClientEventProto$WrappedClientEvent;)V`.

**Unknown/unresolved:**
- Payload content, redaction, retention and all network sinks remain unverified. A privacy UI class does not prove privacy enforcement.

## Additional high-value observations

- Startup: launcher activity aliases (including honeycomb Shell$HomeActivity and Icon aliases) target com.google.android.apps.youtube.app.watchwhile.MainActivity. The target activity is not exported directly. Application class YouTubeTikTokRoot_Application extends Lijs;, which extends Lijw;; Lijw; declares onCreate()V in classes.dex. This identifies inherited startup structure, not the complete dependency graph.
- Background: BackgroundPlayerService extends Larez; in classes2.dex; Larez; extends android.app.Service. The service onCreate explicitly invokes Larez;->onCreate()V and its own d()V. Manifest exported=false and foregroundServiceType=0x2 are observed. Entitlement, audio focus and playback eligibility remain unknown.
- Settings: VideoQualityPrefsFragment.aS()V contains literals 0x7f18002c/2d/2e (video_audio_quality_prefs, videoquality_nonbeta_prefs, videoquality_prefs). Decoded quality XML declares mobile/wifi auto/high/low preference keys. These establish settings structure, not a direct stream-selection API.
- Player/SponsorBlock opportunity: PlaybackControllerWrapper.c() returns media.interfaces.Time; i(SabrSeek)V explicitly references BufferManagerImpl and MediaPushMediaSource.N(J)V/P(J)V. The typed message and calls are real; position units, error handling, entitlement, caller/thread ownership and safe seek behavior are not validated. Do not promote this to an integration API.
- Shorts: ShortsPlayerProgressPresenter.onDraw(Canvas)V invokes Android Canvas operations and its own drawing method. This is drawing evidence, not proof that this view owns playback position or seek.
- Top Bar: MainCollapsingToolbarLayout is in classes.dex. Its b(RecyclerView)V declaration and other selected methods/fields are present in the inventory even though Top Bar is a feature mapping rather than a separate one of the twelve study areas.

## Resource indirection and decoded XML

| Symbol | Actual archive path | Decoded XML SHA-256 |
| --- | --- | --- |
| `xml/videoquality_prefs` | `res/tQJ.xml` | `3514fb72f8ba5c7b6577ca3a7f0982eab4475af0b63b91ce6c86d653387076a7` |
| `xml/videoquality_nonbeta_prefs` | `res/MrS.xml` | `093c97ba9eca6c7841eda2c8688eb6480ef304e54eaea2cd8251340052401402` |
| `xml/network_security_config_ct` | `res/OAv.xml` | `7ec01b310b12fb8e749830af58a5ca5e9ae6be386bf917461c6e4b7d33585594` |
| `xml/offline_prefs` | `res/8fo.xml` | `016b2b0bbb2d429eb585c9a73cf57e9815a856a6857db955f5a0d4cef83006cc` |
| `layout/reel_watch_fragment` | `res/nb_.xml` | `fc632306e70d9ceeb6a0f3d1f5c3ef097bcc97b64748e7a23ed690c3871be3ce` |

The XML hashes above cover aapt2 textual xmltree output in UTF-8, not raw binary XML bytes. The APK/DEX/native hashes cover original binary bytes. Resource IDs, names, paths and configuration choice are separate requirements; never derive a ZIP path from a symbol alone.

Decoded offline_prefs declares background_audio_policy using array/background_audio_policy_entries and array/background_audio_policy_values, as well as smart_downloads_opted_in and a dependency to the SmartDownloadsPrefsFragment entry. It uses ProtoDataStore preference types; the underlying storage/update semantics remain untraced.

Decoded network_security_config_ct (manifest reference 0x7f180021) declares base cleartextTrafficPermitted=true, system trust anchors, certificateTransparency enabled=true and domainEncryption mode=disabled. A domain-config sets cleartextTrafficPermitted=false for youtube.com/googleapis.com including subdomains. Debug-overrides lists user/system certificates. These are observed XML declarations: platform support, debug-override applicability and enforcement by Cronet/native transports were not tested. This is not evidence that cleartext requests occurred, and it is not global HTTPS enforcement.

## Native metadata

All 156 native libraries have file hashes, ELF class/machine and observed PT_LOAD alignment values in the inventory. All 39 arm64-v8a entries are ELF64/machine183; all 39 x86_64 entries are ELF64/machine62. Their observed PT_LOAD alignment is 16,384 bytes. The 32-bit entries are ELF32/machine40 (ARM) or machine3 (x86), with mostly 4,096-byte load alignment and four per ABI at 16,384. This does not validate 16 KB installation/loading or full CPU compatibility.

Native payload includes libgoogle3.so, libcronet.157.0.8103.14.so and media/rendering JNI libraries. Only headers/program-header metadata and hashes were studied. Native symbols/control flow and engine dispatch remain unknown; no native library was loaded.

## Reproduction and tool provenance

The metadata reader follows the [AOSP DEX format](https://source.android.com/docs/core/runtime/dex-format). SDK cross-checks use the documented [apkanalyzer commands](https://developer.android.com/tools/apkanalyzer). No JADX or Apktool installation was required; no decompiled code is committed. Raw disassembly/resource values remain in ignored validation-local.

- Toolchain retained: Java 17 (local Temurin 17.0.20.1), Build Tools 35.0.0/aapt2 2.19-11948202, command-line tools 19.0/apkanalyzer Java adapter, Python 3.15 locally. JSON Schema validation uses host-only jsonschema 4.25.1; CI remains Python 3.12.
- Query configuration: tools/apk-analysis/study_targets.json. Version identity: patches/releases.json. Script: tools/apk-analysis/fingerprint_apk.py. Raw command arrays/outputs: validation-local/phase2b-final-evidence/commands.json.

```powershell
$marufTools = Join-Path $env:LOCALAPPDATA 'MarufYT-BuildTools'
$env:JAVA_HOME = (Get-ChildItem "$marufTools/jdk" -Directory | Select-Object -First 1).FullName
$env:ANDROID_HOME = "$marufTools/sdk"
python tools/apk-analysis/fingerprint_apk.py "main apk/YouTube_21.44.528_APKPure.apk" --releases patches/releases.json --output validation-local/new-study.json --evidence validation-local/new-study-evidence
python -m pip install -r tests/requirements.txt
python tools/apk-analysis/validate_fingerprints.py validation-local/new-study.json
```

Use fresh output/evidence names. Existing files are never overwritten. The final measured run used validation-local/phase2b-final.json and phase2b-final-evidence; the metadata-only inventory was copied into Documentation after review. Local evidence generated before the resource-path fix is superseded by the final run.

The SDK adapter uses Java argument arrays (no shell). Each disassembled class command uses dex code --class followed by its fully qualified class name. Resource commands use aapt2 dump resources and aapt2 dump xmltree with the resolved ZIP path. The generator records exact arguments/return codes locally; code/resource values are intentionally excluded from published metadata.

## Validation and unresolved scope

35 current tests passed, including the 22 prior foundation/analysis/compatibility tests. JSON Schema meta-schema, generated inventory and cross-record references pass. Foundation debug APK builds and verifies; original input hash is unchanged. Full results and created/modified files: [implementation report](PHASE2B_IMPLEMENTATION_REPORT.md).

Unknowns: stable-channel/provenance certification, safe modification points, exact obfuscated method semantics, reflection/dynamic dispatch, native algorithms, runtime/server configuration, full data-flow/caller constraints, device behavior and fallback release. No modified YouTube APK, SponsorBlock implementation, background-playback implementation or fake UI was produced. Await approval before Phase 2C.
