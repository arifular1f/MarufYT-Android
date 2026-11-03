# Build guide

## Prerequisites

Windows 10, JDK 17 (for example Temurin), Python 3.12+ for repository checks, Git, Android SDK command-line tools, internet and several GB of free disk. Android Studio is optional. No emulator, NDK, Kotlin, Compose or node packages are needed.

Set JAVA_HOME to your JDK directory and add its bin directory to PATH. Set ANDROID_HOME to your Android SDK directory. Add platform-tools and cmdline-tools/latest/bin to PATH. Review and accept SDK licenses interactively, then install:

```powershell
sdkmanager --licenses
sdkmanager "platform-tools" "platforms;android-36" "build-tools;35.0.0"
```

Alternatively create ignored local.properties containing `sdk.dir=C:/Users/YOUR_NAME/AppData/Local/Android/Sdk`. Never commit machine paths or SDK license files.

## Validation and build

```powershell
.\gradlew.bat --version
python tools/validate_foundation.py
python -m pip install -r tests/requirements.txt
python -m unittest discover -s tests -v
.\gradlew.bat help test assembleDebug --stacktrace --console=plain
```

Linux/macOS: replace `.\gradlew.bat` with `bash gradlew`. The wrapper downloads Gradle 8.13 and verifies its official distribution SHA-256. A global Gradle installation is unnecessary.

The consolidated preview runs 50 Python tests and two app JVM theme-policy tests. JSON Schema validation is host-only; JUnit 4.13.2 is test-only. Empty integration modules still report NO-SOURCE. No instrumented/device tests are claimed. Use `gradlew.bat test assembleDebug lintDebug`; output is app/build/outputs/apk/debug/app-debug.apk.

Build memory settings: 1536 MB Gradle heap, two workers, no parallel project execution and no persistent daemon. Close unnecessary applications on an 8 GB PC; use --max-workers=1 if memory pressure occurs.

## Physical phone

Use an API 26+ phone. Enable developer options and USB debugging and authorize the computer:

```powershell
adb devices
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Open MarufYT Foundation and check the status text. It has a separate application ID and does not replace YouTube. This manual test has to be performed on your device.

## GitHub Actions and troubleshooting

Publish this directory's contents as repository root in arifular1f/MarufYT-Android. The workflow runs on pushes and PRs and retains its debug APK artifact for seven days. Local validation does not imply a successful remote run.

JAVA_HOME errors: select JDK 17. SDK errors: check ANDROID_HOME/local.properties and license acceptance. Download errors: check access to Google Maven, Maven Central, Gradle and SDK repositories. Inspect the first failing task and its stack trace. Debug keys differ across machines and CI runs; uninstall the old foundation app if signatures conflict (this clears its data).

Pinned compatibility is documented in the [official AGP compatibility table](https://developer.android.com/build/releases/agp-8-13-0-release-notes). This stable toolchain is intentionally pinned; it is not a claim to use the newest AGP major release. YouTube's latest stable APK version must be independently assessed in a later approved phase.

## Phase 2A read-only local analysis

The SDK command-line tools must use the standard cmdline-tools/latest/bin and cmdline-tools/latest/lib layout. With ANDROID_HOME and JAVA_HOME set, run:

```powershell
python tools/analyze_apk.py "main apk/YouTube_21.44.528_APKPure.apk" --output validation-local/new-analysis.json --releases patches/releases.json
```

The CLI supports quoted Windows paths with spaces, never extracts or writes the source APK, and refuses existing output filenames. It uses pinned Build Tools 35.0.0 and the SDK apkanalyzer Java adapter. The current machine has command-line tools revision 19.0. Read-only reports contain ZIP inventories, manifest attributes, tool output and command arrays; keep them local because raw manifest metadata can include embedded service identifiers. Do not upload main apk/ or validation-local/ as artifacts.

Return codes: 0 successful analysis, 1 input/tool/configuration error, 2 unsupported research identity. Known inputs are RESEARCH_ONLY and never patch-supported. A missing optional local proprietary input does not affect CI's synthetic tests or foundation build.

## Phase 2B fingerprints

Use fingerprint_apk.py as documented in [tools/apk-analysis/README.md](../tools/apk-analysis/README.md). It performs the hash and manifest identity gate before DEX/resource/native study. Use fresh output and evidence paths. Validate the published JSON independently:

```powershell
python tools/apk-analysis/validate_fingerprints.py Documentation/PHASE2B_FINGERPRINT_INVENTORY.json
```

Do not publish raw evidence or interpret static name/call matches as validated playback hooks. See [Phase 2B results](PHASE2B_IMPLEMENTATION_REPORT.md).
