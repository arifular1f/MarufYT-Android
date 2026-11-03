# MarufYT Android — Development & Contribution Guide (Phase 3)

**Author:** Lead Software Architect & Tooling Engineer  
**Project:** MarufYT Android (`arifular1f/MarufYT-Android`)  

---

## 1. Prerequisites & Environment Setup

To build, test, and contribute to MarufYT Android, ensure your workstation meets the following requirements:

- **Operating System:** Windows 10/11, macOS (Apple Silicon/Intel), or Linux (Ubuntu 22.04+).
- **Java Development Kit (JDK):** OpenJDK 17 (Temurin 17.0.20+ recommended).
- **Android SDK:**
  - Android SDK Platform API 36 (`android-36`).
  - Android SDK Build-Tools `35.0.0`.
  - Android SDK Platform-Tools.
- **Python:** Python 3.10 or newer (tested on 3.10 through 3.13).
- **Git:** Git 2.30+ with long paths enabled on Windows (`git config --system core.longpaths true`).

### Environment Variables
Configure the following environment variables:
```bash
# Windows PowerShell
$env:JAVA_HOME = "C:\Path\To\jdk-17"
$env:ANDROID_HOME = "C:\Path\To\Android\sdk"
$env:Path = "$env:JAVA_HOME\bin;$env:ANDROID_HOME\platform-tools;$env:ANDROID_HOME\build-tools\35.0.0;$env:Path"

# Linux / macOS (bash or zsh)
export JAVA_HOME="/path/to/jdk-17"
export ANDROID_HOME="/path/to/android-sdk"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/35.0.0:$PATH"
```

---

## 2. Repository Layout

```
MarufYT-Android/
├── .github/
│   └── workflows/              # GitHub Actions CI/CD workflows
├── app/                        # Android companion app module
│   ├── src/main/java/...       # MainActivity, MarufConfig, ThemeMode
│   ├── src/test/java/...       # JVM unit tests (MarufConfigTest, ThemeModeTest)
│   └── build.gradle            # Module build configuration
├── integrations/               # Decoupled integration subprojects
│   ├── player-customization/
│   ├── privacy-diagnostics/
│   └── sponsorblock/
├── patches/                    # Patch management scripts and target releases
├── tools/                      # Static analysis & automation toolchain
│   ├── apk-analysis/           # DEX parser and fingerprinting engine
│   ├── marufyt/                # Core Python modules (settings_bridge, sponsorblock_controller)
│   └── validate_foundation.py  # Repository integrity & secret scanner
├── tests/                      # Python automated test suite (80 unit tests)
└── Documentation/              # Technical specifications, reports, and architecture
```

---

## 3. Building & Verification Commands

### 3.1 Running the Python Automated Test Suite
The repository includes a comprehensive 80-test Python verification suite covering APK forensics, semantic contracts, SponsorBlock controller state machines, and configuration serialization:
```powershell
python -m unittest discover -s tests -v
```

### 3.2 Running the Foundation & Secret Integrity Guard
Validates that required structural files exist and that zero proprietary binaries (`.apk`, `.keystore`) or secrets are tracked:
```powershell
python tools/validate_foundation.py
```

### 3.3 Running Android Unit Tests & Gradle Tasks
```powershell
# Run Java unit tests
.\gradlew.bat test

# Assemble debug companion APK
.\gradlew.bat assembleDebug

# Run Android Lint static code analysis
.\gradlew.bat lintDebug

# Execute all verification tasks in a single pass
.\gradlew.bat test assembleDebug lintDebug
```

---

## 4. Smali Analysis & Fingerprinting Workflow

When validating a new YouTube target version (e.g. `21.44.528`):
1. Place the clean, unmodified reference APK in the local, git-ignored directory `main apk/`.
2. Run the automated static fingerprint scanner:
   ```powershell
   python tools/apk-analysis/fingerprint_apk.py
   ```
3. Verify that all 13 core targets match the published structural signatures in `Documentation/FINGERPRINT_SCHEMA.json`:
   ```powershell
   python tools/apk-analysis/validate_fingerprints.py
   ```
4. **NEVER** commit the input APK or extracted Smali trees to git. Only commit metadata reports and contract tests.

---

## 5. Development Rules & Contribution Invariants

1. **Strictly Source-Only:** Under no circumstances should modified YouTube APKs, proprietary binaries, or private keystores be committed or pushed.
2. **Zero Telemetry Policy:** The companion application and tools must never contain telemetry SDKs, crashlytics, or analytics beacons.
3. **Android Scope Only:** Do not modify the sibling iOS repository or conflate iOS tweak implementations with Android bytecode architecture.
4. **Honest Capability Reporting:** Never mark a blocked or unverified feature as working. If an Android feature is blocked by host architecture (e.g. Background Playback entitlement check or Widevine DRM), document the exact Smali blocker.
