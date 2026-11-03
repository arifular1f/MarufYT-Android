# MarufYT Android

[![Android checks](https://github.com/arifular1f/MarufYT-Android/actions/workflows/android.yml/badge.svg)](https://github.com/arifular1f/MarufYT-Android/actions/workflows/android.yml)

**A clear, lightweight starting point for Android settings and APK research.** By [arifular1f](https://github.com/arifular1f). Developer preview **0.2.0-preview.1**.

MarufYT currently provides a standalone native settings preview, read-only APK analysis/fingerprints, and an optional host SponsorBlock lookup tool. It does not modify YouTube or implement playback features. No affiliation with YouTube or Google.

| Capability | Verified status |
| --- | --- |
| Native settings companion | Compiles; System/Light/Dark choice and reset implemented; physical-device UI/persistence checks pending |
| SponsorBlock lookup | Host CLI implemented and unit-tested; explicit real API request completed; no automatic skipping |
| APK identity, signatures, fingerprints | Tested local tooling; exact SHA-pinned research input |
| Background playback / screen-off / media controls | Unavailable; lifecycle and entitlement integration unverified |
| Quality, captions, gestures, watch/feed/Shorts/tabs/top bar | Research candidates documented; YouTube customization unavailable |
| Downloads | Unavailable |
| Privacy | Companion has no network permission or telemetry; optional CLI networking documented separately |

The companion exposes all thirteen requested sections, with informational unavailable states instead of inert toggles. General appearance and Privacy reset are the functional controls.

## Compatibility

Companion: Android 8.0+ (API 26), platform Java/UI, no bundled native libraries. Physical-device compatibility remains untested. Research input only: YouTube 21.44.528, code 1561310186, minimum API 29, ARM64/ARMv7/x86/x86_64 payloads, SHA-256 `55be430ce82dcedcb737ea27d1b78576737b75d11cde04aa89989e5376d3ae6c`. No patched base version or stable fallback is supported.

## Build and install

JDK 17, AGP 8.13.2, Gradle 8.13, SDK 36 and Build Tools 35.0.0. Python 3.12+ is used for host checks. Set JAVA_HOME and ANDROID_HOME, then on Windows:

```powershell
python -m pip install -r tests/requirements.txt
python tools/validate_foundation.py
python -m unittest discover -s tests -v
.\gradlew.bat test assembleDebug lintDebug --stacktrace
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Linux/macOS: use `bash gradlew`. See [installation](Documentation/INSTALLATION.md), [build guide](Documentation/BUILD_GUIDE.md), and [device checklist](Documentation/DEVICE_TEST_CHECKLIST.md). The 1.5 GB Gradle heap/two-worker limits support an 8 GB development PC. No emulator is required.

## Tooling and research

```powershell
python tools/validate_input.py "main apk/YouTube_21.44.528_APKPure.apk" --output validation-local/new-input-report.json
python tools/sponsorblock_lookup.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

The first command validates a user-supplied local input and explicitly blocks modification when no validated transforms exist. The second performs an opt-in host API lookup; replace VIDEO_ID with a valid 11-character ID. It never controls playback. See [SponsorBlock behavior/privacy](Documentation/SPONSORBLOCK.md), [semantic findings](Documentation/SEMANTIC_VALIDATION.md), [fingerprints](Documentation/PHASE2B_FINGERPRINT_REPORT.md), and [architecture](Documentation/ARCHITECTURE.md).

## Screenshots

Real-device screenshots are pending. No mockup is represented as a verified app screenshot. Light/dark rendering, large text and system insets must be checked on a physical phone.

## Releases and limitations

GitHub preview assets contain **project-owned source, tooling and documentation only**. No YouTube APK, Google components, raw code bodies, datasets, installers, keys or credentials are included. Source ZIP checksums and a file manifest accompany the release. [Release notes](Documentation/RELEASE_NOTES.md), [release guide](Documentation/RELEASE_GUIDE.md), [final report](Documentation/MARUFYT_ANDROID_FINAL_RELEASE_REPORT.md), and [changelog](CHANGELOG.md).

Static references are not runtime validation. No device tests or working YouTube hooks are claimed. Server experiments, active video identity, seek completion, audio focus and entitlement behavior remain unresolved. [Security policy](SECURITY.md), [contribution guide](CONTRIBUTING.md).

## License and attribution

Original Android-code licensing is **not assigned**. This is a source-available review preview, not yet an open-source licensed release. The separate iOS license is not automatically applicable. See [license status](LICENSE_STATUS.md) and [third-party notices](THIRD_PARTY_NOTICES.md). Gradle wrapper Apache 2.0 notices are preserved; no iOS implementation or SponsorBlock extension code was copied.
