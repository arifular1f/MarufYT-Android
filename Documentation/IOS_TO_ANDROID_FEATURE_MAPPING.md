# iOS to Android feature mapping

Reference only: `C:\Users\oriyan\Desktop\ios App\MarufYT`. Read its README.md, docs/FEATURE_MATRIX.md, Documentation/MODULES.md and relevant names/preferences in Tweak/Settings/YTKACESettingsPages.mm. No iOS files were changed. Its documented current iOS versions 21.43.5/21.39.4 and feature claims do not establish Android support or independently verified device behavior.

Android evidence input: `C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk`, 220,576,405 bytes, SHA-256 `55be430ce82dcedcb737ea27d1b78576737b75d11cde04aa89989e5376d3ae6c`. Tool versions and static findings are in [forensics](YOUTUBE_APK_FORENSIC_REPORT.md); tests and build results are in [the phase report](PHASE2A_IMPLEMENTATION_REPORT.md).

| iOS feature | Android equivalent | Feasibility / dependencies | Android implementation status |
| --- | --- | --- | --- |
| Background Audio | Background Playback | Concept portable; Android audio focus, foreground lifecycle and YouTube player gates require new research. Host hooks unverified. | Not started |
| SponsorBlock | SponsorBlock | Category and preference concepts portable; HTTPS client is Android-specific, player timing/seek hooks depend on YouTube internals. API/license/privacy review pending. | Not started |
| Video Quality | Video Quality | Preferences portable; stream selection and network policy need Android-specific host adapters and version fingerprints. | Not started |
| Captions | Captions | Preference concepts portable; Android track selection and host caption UI hooks unverified. | Not started |
| Gestures | Player Gestures | Volume/brightness concepts portable; Android input dispatch, accessibility and host-player touch integration require new implementation. | Not started |
| Home & Feed | Feed Customization | Settings concepts portable; renderer/filter internals and experiments are version-dependent and unverified. | Not started |
| Shorts | Shorts Customization | UX concepts portable; Shorts lifecycle, navigation and playback internals require Android-specific fingerprints. | Not started |
| Tabs | Navigation Customization | Hide/order/startup concepts portable; host navigation components and account/experiment changes are unverified. iOS Liquid Glass APIs do not port. | Not started |
| Downloads | Supported Download Integration | Unverified. Android storage and permitted user-owned content workflows need an independent design. Do not assume iOS SABR/FFmpeg integration, authentication replay or protected-stream access is reusable. | Not started |
| Privacy | Privacy Controls | HTTPS, opt-in controls, local redacted diagnostics and minimal retention are portable policies. Android request/redirect/storage mechanisms require new implementation; host YouTube behavior remains separate. | Not started |

The iOS source also names ad blocking, DeArrow, PiP, sleep timer, loop, speed and localization. These are reference concepts only and are outside the requested implementation. UIKit, Objective-C runtime selectors, Logos hooks, Apple media frameworks and iOS preference keys are not reusable Android hook implementations.

Directly portable: requirements, category labels, consent/default policies and UX intent, subject to license and product review. Android-specific: code, lifecycle, storage, rendering, input, network and persistence. YouTube-internal: method/resource fingerprints and adapters for playback, feeds, navigation and settings insertion. Unsupported/unverified: all Android behavior rows until implemented and tested, stable fallback selection, and actual playback/device compatibility.

No Android feature is promoted to functional based on the iOS documentation. Next development work requires explicit Phase 2B approval and a narrowly scoped read-only fingerprint study before modifying anything.
