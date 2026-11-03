# Phase 2A implementation report

Date: 2026-11-03, Asia/Kuala_Lumpur. Scope: read-only APK analysis, research compatibility gates and patch architecture. No Phase 2B, APK modification or GitHub push.

## Inspection and preservation

Inspected the Android source/configuration inventory, README and existing Documentation, all module READMEs/build scripts, settings/root/app Gradle configuration, wrapper properties, workflow, validation/tests, existing outputs and main apk directory before editing. Branch: main. Foundation files were untracked at entry; no commits or remote were present. Existing outputs included app-debug.apk (6,969 bytes), output-metadata.json, debug/release manifest-merger reports and the Gradle problems report. No source modules contained domain implementation; only MainActivity displayed foundation text.

The existing iOS source was read only for feature mapping. Its pre-existing untracked documentation was not changed. The Android app, dependency versions, Gradle memory settings and wrapper were preserved. No git add, commit, remote setup or push was performed.

## Exact local input and findings

- Path: `C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk`.
- Size: **220,576,405 bytes**.
- SHA-256 before/after: `55be430ce82dcedcb737ea27d1b78576737b75d11cde04aa89989e5376d3ae6c` (unchanged).
- Package `com.google.android.youtube`; label YouTube; version `21.44.528`; code `1561310186`.
- minSdk 29; target/compile SDK 37; compile codename DEV.
- 17,047 ZIP entries, 465,176,681 uncompressed bytes, eight valid DEX 035 files, 16,170 resource entries, 443 assets, 156 native libraries (39 each for arm64-v8a, armeabi-v7a, x86, x86_64).
- ZIP CRCs and DEX header/SHA-1/Adler-32 checks pass.
- apksigner verification passes: v3/v3.1, source stamp verified, SDK-specific legacy/new certificate records for one signer. Certificate subjects, fingerprints, exact signature output, permissions and native inventory are in [the forensic report](YOUTUBE_APK_FORENSIC_REPORT.md).
- Static structure supports a standalone universal APK: no required split declarations, standalone stamp metadata, fused base module and empty split-name language mappings. No OBB payload/declaration identified. Runtime assets, optional delivery and actual installation remain untested.

## Version decision

Primary research candidate: **this exact SHA-pinned 21.44.528 input**. The [APKPure history](https://apkpure.net/youtube-app/com.google.android.youtube/versions) matches name/code/date and rounded size. Stable channel and independently published file hash/publisher certificate trust pin remain UNKNOWN. No stable fallback recommendation is supported by local evidence; fallback=null. No second YouTube binary was downloaded. See [version compatibility](YOUTUBE_VERSION_COMPATIBILITY.md).

## Implemented behavior and architecture

The new dependency-free Python host package inventories APK ZIP/DEX structures, resolves manifest identity/labels through installed SDK tools, verifies signatures, records command arrays/tool versions, hashes before and after, and writes a new JSON metadata file. It rejects unsafe ZIP paths, duplicate/encrypted/symlink entries, size-limit violations, corrupt DEX/ZIP inputs, non-direct APK containers and output overwrites. Windows original ZIP names are checked before ZipInfo normalization.

Compatibility models retain unknown values, support Android long version codes and exact package/name/code/hash research gates. Recognized candidates are RESEARCH_ONLY with patch_supported=false. Patch metadata registry and dependency preflight reject duplicates, missing dependencies, cycles and unsupported exact versions. There are zero production patches and no executor. Future isolation, failure reporting, signing and runtime contracts are design only.

Existing Java integration/tool modules remain empty; no Android features or nonfunctional controls were added. Host adapters are documented alongside their module boundaries. CI runs synthetic fixtures only; no local proprietary input or raw evidence is uploaded. See [patch architecture](ANDROID_PATCH_ARCHITECTURE.md) and [iOS mapping](IOS_TO_ANDROID_FEATURE_MAPPING.md).

## Tools

- Java: Eclipse Temurin 17.0.20.1.
- AGP 8.13.2; Gradle 8.13; foundation SDK 36/min SDK 26; Build Tools 35.0.0.
- aapt2: Android Asset Packaging Tool 2.19-11948202; apksigner 0.9.
- SDK command-line tools revision 19.0 (apkanalyzer Java adapter).
- Python 3.15 locally; standard-library runtime tooling; CI Python remains 3.12.
- Validation utilities already installed: PyYAML 6.0.3 and actionlint 1.7.7.
- No JADX/Apktool installation was necessary for the accepted metadata/structure scope.

The existing SDK command-line tools had an extra nested cmdline-tools directory. apkanalyzer initially failed SDK discovery; copying its bin/lib and metadata into the standard latest layout resolved it. SDK tools remain outside the repository at `%LOCALAPPDATA%/MarufYT-BuildTools`. No project dependency was changed.

## Validation results

| Check | Result |
| --- | --- |
| Actual supplied APK analysis and research gate | PASS; input unchanged |
| ZIP CRCs and eight DEX checks | PASS |
| Actual package/name/code extraction | PASS, matches supplied candidate |
| Signature verification | PASS; detailed certificates/schemes in forensic report |
| Python synthetic/foundation tests | 22 passed |
| Quoted Windows paths with spaces | PASS, actual CLI and synthetic fixtures |
| Gradle help/test/assembleDebug | BUILD SUCCESSFUL in 11s; 58 tasks, 1 executed/57 up-to-date |
| JVM/Android domain tests | NO-SOURCE; no domain test coverage claimed |
| Workflow YAML parsing and push/PR triggers | PASS |
| actionlint | PASS, zero findings |
| Structure and limited secret guard | PASS; local APK input ignored and never staged |
| Existing foundation debug APK | Build preserved; real analyzer/signature check passed, 6,969 bytes, SHA-256 1bdfcc9994cb06643220dbda0482b191f864907bff9d486749c8ef148e85e31f (matches foundation report) |
| GitHub remote workflow | NOT RUN; no push performed |
| Physical Android phone | NOT TESTED |

Tests use generated, non-proprietary fixtures. They cover identity/unknowns/long version codes, malformed XML, archive paths/limits/corruption, DEX validation, input overwrite protection, exact research gates and malformed configs, dependency ordering/rejections, local input exclusions and tracked-input/key rejection. A test exposed Windows ZipInfo filename normalization; validation now checks orig_filename and the regression test passes. Test fixture patch records are not production patch implementations.

The source secret guard checks selected patterns and forbidden assets, not every possible credential. Raw manifest/service identifiers stay in ignored validation-local; reports publish selected metadata and public certificate fingerprints only. No secrets, signing keys or credentials were added. Independent publisher provenance, runtime security and full decompilation were not audited.

## Files created (12)

- `tools/analyze_apk.py`
- `tools/marufyt/__init__.py`
- `tools/marufyt/analysis.py`
- `tools/marufyt/models.py`
- `tools/marufyt/compatibility.py`
- `tests/test_analysis.py`
- `patches/releases.json`
- `Documentation/YOUTUBE_APK_FORENSIC_REPORT.md`
- `Documentation/YOUTUBE_VERSION_COMPATIBILITY.md`
- `Documentation/ANDROID_PATCH_ARCHITECTURE.md`
- `Documentation/IOS_TO_ANDROID_FEATURE_MAPPING.md`
- `Documentation/PHASE2A_IMPLEMENTATION_REPORT.md`

## Existing files modified (12)

- `.gitignore` (dedicated local input/container exclusions)
- `.github/workflows/android.yml` (accurate synthetic-analysis test step name; discovery already runs all tests)
- `README.md`
- `Documentation/ARCHITECTURE.md`
- `Documentation/BUILD_GUIDE.md`
- `Documentation/ROADMAP.md`
- `Documentation/SECURITY.md`
- `tools/validate_foundation.py`
- `tests/test_foundation.py`
- `tools/apk-analysis/README.md`
- `tools/apk-validation-signing/README.md`
- `patches/patch-management/README.md`

Ignored local outputs include JSON inventories/SDK command output, badging/manifest/split trees, signature output, test/build validation logs and existing build/cache outputs. No proprietary APK or decoded asset was added to the source inventory. The original FOUNDATION_REPORT.md remains a historical record of the previous phase.

## Reproduction and next step

From the Android repository root in PowerShell:

```powershell
$marufTools = Join-Path $env:LOCALAPPDATA 'MarufYT-BuildTools'
$env:JAVA_HOME = (Get-ChildItem "$marufTools/jdk" -Directory | Select-Object -First 1).FullName
$env:ANDROID_HOME = "$marufTools/sdk"
python tools/analyze_apk.py "main apk/YouTube_21.44.528_APKPure.apk" --output validation-local/new-analysis.json --releases patches/releases.json
python tools/validate_foundation.py
python -m unittest discover -s tests -v
.\gradlew.bat help test assembleDebug --warning-mode all --stacktrace --console=plain
& "$marufTools/actionlint/actionlint.exe" -no-color .github/workflows/android.yml
```

Use a fresh analysis output name. Exact SDK argument lists and measured versions are recorded in the forensic report and ignored JSON evidence. CI needs neither main apk/ nor any YouTube download.

Remaining limitations are explicit: stable rollout/provenance not independently established, no analyzed fallback, no physical-device results, no bytecode fingerprint discovery and no patch/runtime compatibility claim. They do not prevent the completed read-only structure/identity analysis, but block designating a stable patched release.

Exact next development step: obtain explicit approval for Phase 2B, then define a narrow read-only player/resource fingerprint study and its acceptance tests against the SHA-pinned input before approving any transform implementation. Do not alter the source APK, implement playback/SponsorBlock modifications, push to GitHub or begin Phase 2B from this task. Stop for approval.
