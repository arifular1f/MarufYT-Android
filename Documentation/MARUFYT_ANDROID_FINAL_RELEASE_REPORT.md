# MarufYT Android ? final developer preview report

Date: 2026-11-03 (Asia/Kuala_Lumpur). Version **0.2.0-preview.1**, intended tag **v0.2.0-preview.1**. This is a research/tooling and standalone settings preview, not a modified YouTube release or a stable playback product.

## Executive result

Preserved the successful foundation and completed feasible semantic study, an independently functional host SponsorBlock lookup client, a native companion settings preview, security/quality checks, source-only packaging/auditing and GitHub publication preparation. No safe YouTube runtime integration was established; no broken patch or fake toggle was shipped. Physical-device tests are pending. Original Android-code licensing is unassigned, so this is source-available review material, not yet an open-source licensed product.

The original iOS project was not changed. The original YouTube input was not modified, replaced, re-signed, uploaded or redistributed. Initial repository state had no commits, remote or tags; all prior project files were untracked. There was no commit history to overwrite. Existing user work was preserved and extended; the initial source snapshot is recorded only in ignored local validation evidence.

## Feature-by-feature status

| Feature | Actual result |
| --- | --- |
| SponsorBlock | Host-only explicit API lookup, categories including sponsor/intro/outro, validated response/identity/timestamps, timeout/error handling and memory cache; no Android/player skip integration |
| Background playback | Blocked: active playback lifecycle, audio focus, entitlement and cleanup integration are not validated; no toggle, service or screen-off claim |
| Quality / captions / gestures | Static boundaries documented; host behavior changes unavailable |
| Watch Page / Home & Feed / Shorts / Tabs / Top Bar | Research mappings available; no runtime customization |
| Downloads | No supported integration |
| General settings | Native companion appearance selection, System/Light/Dark, stored using private SharedPreferences; policy JVM tests pass; device persistence/rendering not tested |
| Privacy settings | Functional reset of the appearance preference; backup disabled; no app network permission or telemetry |
| Settings UI | Thirteen organized native sections, light/dark palette, rounded cards, insets and availability text; no inert feature switches; actual screenshots pending |

## Semantic validation and blockers

See [SEMANTIC_VALIDATION.md](SEMANTIC_VALIDATION.md) for exact observations. New evidence identifies rational Time ticks/timescale, scale conversion requests of 1,000,000/1,000 through JNI, finite/sentinel branches, a microsecond-scaled wrapper path, SabrSeek field/mode usage, background-service delegate/return behavior, and concrete getVideoId getter data flow. The named reference scan found 47 references including repeated cross-DEX entries.

These static facts do not prove active-video association, live/ad/Shorts timeline coherence, caller/thread safety, seek completion or entitlement eligibility. They block automatic SponsorBlock skipping and background playback. Generic finite time calculations and URL/ID mapping are independently tested host utilities, not execution of the proprietary player. Existing fingerprint schema/inventory remains unchanged and always patch_supported=false.

## APK compatibility and validation

Research input: `C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk`, com.google.android.youtube, 21.44.528, code 1561310186, 220,576,405 bytes. Expected/before/after SHA-256: `55be430ce82dcedcb737ea27d1b78576737b75d11cde04aa89989e5376d3ae6c`. Hash, identity, ZIP/DEX and signature checks passed. Input has minimum API 29, target/compile 37 and four ABI payloads. No fallback/stable-channel certification exists.

`tools/validate_input.py` repeats the strict pre-analysis gate, reuses full analysis/signature checks and emits an explicit BLOCKED_NO_VALIDATED_TRANSFORMS decision. No modified APK is generated. Project-owned debug builds are a different package and do not use YouTube classes/resources.

## Security, privacy and licensing

The companion has no INTERNET permission, stores one non-sensitive appearance choice, disables backup and adds no telemetry. The host SponsorBlock client is opt-in, fixed-origin HTTPS with certificate verification, four-character ID hash-prefix queries, redirect rejection, bounded response/timeouts and memory-only expiry cache. It validates intervals, duration mismatch and malformed data. Prefix lookup is not anonymity. A real request completed with zero matching segments; no API response dataset is distributed. See [SPONSORBLOCK.md](SPONSORBLOCK.md).

The proprietary host's network base-config permits cleartext with selected domain restrictions; no blanket HTTPS enforcement or runtime safety claim is made. No release signing key, password or credential is committed. CI uses a short-lived GitHub token only for source-release publication. Dependency review covers standard-library networking, JSON Schema validation, test-only JUnit and wrapper attribution; it is not an exhaustive vulnerability certification.

No root LICENSE was invented: the Android project had none and the iOS MIT grant does not automatically apply. See [LICENSE_STATUS.md](../LICENSE_STATUS.md) and [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Selecting/authorizing the original-code license remains an owner action before calling the project open source.

## Validation results

- Python: 51 tests passed (35 previous tests preserved; SponsorBlock and source-release cases added).
- Java: two ThemeMode test cases pass for debug and release variants; no instrumented tests run.
- Gradle: test, assembleDebug and lintDebug succeeded; final local build completed in 19 seconds. Android lint: zero issues.
- Published fingerprint JSON Schema/cross-record checks: pass. Script syntax and source guard: pass.
- YAML/actionlint: validated locally for CI and source-release workflows.
- Original APK and project-owned preview signature checks: pass. Preview uses a local debug v2 signature; no production signing is configured.
- Reproducible source archive: fixed paths/timestamps and file hashes; same-environment deterministic packaging is tested, and complete archive payload auditing is required before publication.
- Live SponsorBlock request: completed with zero validated matching segments. No automatic seek performed.
- Device: adb showed no connected phone. Installation, UI, login compatibility, persistence, audio focus, background/screen-off and network recovery on a phone are NOT TESTED. No fake device screenshots.

## Build/artifact inventory and checksums

The local preview debug APK is not a GitHub release asset. Its exact size/hash/identity are in [PREVIEW_BUILD_VERIFICATION.json](PREVIEW_BUILD_VERIFICATION.json). Local SHA-256: `c0255f7a1eb3cbe94cffca9c65bf84abdbf7daff02639d4ae8656105236007a6`, size 15,825 bytes. CI-generated debug keys make CI APK hashes different; each CI build supplies its own checksum.

Source release payloads: `MarufYT-Android-0.2.0-preview.1-source.zip`, `RELEASE_REPORT.json`, `SHA256SUMS.txt`. The ZIP includes SOURCE_MANIFEST.json with every packaged source file's hash. No APK/Google components/raw disassembly/API dataset/keys/local environment files are included. The adjacent checksum file is authoritative for those exact release bytes; embedding the archive's own checksum into an archived source report would be recursive. RELEASE_REPORT.json records the source commit at packaging time; the immutable Git tag identifies release source.

## GitHub publication status

Publication is the final external step after local validation and staged-file review. Target: https://github.com/arifular1f/MarufYT-Android . GitHub authentication was verified as arifular1f and the repository was initially absent/inaccessible. Actual publication results, commit/tag and workflow evidence will be appended after the authorized publication attempt; no successful remote run is inferred from local checks.

## Exact build and installation

Install JDK 17, Android SDK 36/Build Tools 35.0.0/platform-tools, Git and Python 3.12+. Set JAVA_HOME and ANDROID_HOME. From repository root:

```powershell
python -m pip install -r tests/requirements.txt
python tools/validate_foundation.py
python -m unittest discover -s tests -v
python tools/apk-analysis/validate_fingerprints.py Documentation/PHASE2B_FINGERPRINT_INVENTORY.json
.\gradlew.bat test assembleDebug lintDebug --stacktrace
adb devices -l
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Launch MarufYT Preview, a separate package. It never requests Google login or modifies the official YouTube installation. Source-only releases must be built locally; there is no released installer. See [installation](INSTALLATION.md), [release guide](RELEASE_GUIDE.md) and [device checklist](DEVICE_TEST_CHECKLIST.md).

## Remaining limitations

No verified runtime hooks, playback patches or background/Shorts integration. No physical-device evidence, stable YouTube provenance or analyzed fallback. Original-code license pending; debug signing only. The preview is not ready to claim a stable modified YouTube product. Future work should validate active video identity, timeline, caller/lifecycle/thread/entitlement conditions and device behavior before implementing playback actions. No unrelated work is started.

## Detailed file inventory

Created (31):

- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/pull_request_template.md`
- `.github/workflows/release.yml`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `Documentation/DEVICE_TEST_CHECKLIST.md`
- `Documentation/INSTALLATION.md`
- `Documentation/MARUFYT_ANDROID_FINAL_RELEASE_REPORT.md`
- `Documentation/PREVIEW_BUILD_VERIFICATION.json`
- `Documentation/RELEASE_GUIDE.md`
- `Documentation/RELEASE_NOTES.md`
- `Documentation/SEMANTIC_VALIDATION.md`
- `Documentation/SPONSORBLOCK.md`
- `LICENSE_STATUS.md`
- `SECURITY.md`
- `THIRD_PARTY_NOTICES.md`
- `app/src/main/java/io/github/arifular1f/marufyt/ThemeMode.java`
- `app/src/main/res/drawable/ic_marufyt.xml`
- `app/src/main/res/values/strings.xml`
- `app/src/main/res/xml/data_extraction_rules.xml`
- `app/src/test/java/io/github/arifular1f/marufyt/ThemeModeTest.java`
- `licenses/GRADLE_WRAPPER_LICENSE.txt`
- `release.json`
- `tests/test_release.py`
- `tests/test_sponsorblock.py`
- `tools/audit_release.py`
- `tools/marufyt/sponsorblock.py`
- `tools/prepare_release.py`
- `tools/sponsorblock_lookup.py`
- `tools/validate_input.py`

Modified (12):

- `.github/workflows/android.yml`
- `.gitignore`
- `Documentation/ARCHITECTURE.md`
- `Documentation/BUILD_GUIDE.md`
- `Documentation/ROADMAP.md`
- `README.md`
- `app/build.gradle`
- `app/src/main/AndroidManifest.xml`
- `app/src/main/java/io/github/arifular1f/marufyt/MainActivity.java`
- `app/ui-settings/README.md`
- `integrations/sponsorblock/README.md`
- `tools/validate_foundation.py`
