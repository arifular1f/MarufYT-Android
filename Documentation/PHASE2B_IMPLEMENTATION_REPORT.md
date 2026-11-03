# Phase 2B implementation report

Date: 2026-11-03, Asia/Kuala_Lumpur. Scope completed: read-only, SHA-pinned YouTube structural fingerprint study. No Phase 2C, patch execution, runtime change, proprietary APK redistribution or GitHub push.

## Integrity gate and preservation

Input: `C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk`, 220,576,405 bytes.

Expected, initial, post-analysis and final verification SHA-256: `55be430ce82dcedcb737ea27d1b78576737b75d11cde04aa89989e5376d3ae6c`.

SDK-decoded identity: com.google.android.youtube / 21.44.528 / 1561310186, matching the required identity. Gate PASSED. The reusable generator repeats this gate before its structural inspection and aborts on hash or identity mismatch. Negative tests verify that hash failure invokes no SDK inspection and identity failure is rejected.

The source was read only; matching whole-file hashes confirm cryptographic byte-level integrity before and after. No replace, re-sign, overwrite, APK transformation or runtime loading occurred. Existing Android app/Gradle files, AGP 8.13.2, Gradle 8.13, JDK 17, SDK 36 and memory settings remain unchanged. The existing foundation APK is still 6,969 bytes with SHA-256 `1bdfcc9994cb06643220dbda0482b191f864907bff9d486749c8ef148e85e31f`.

Branch remains main. All foundation/Phase 2A files were already untracked at entry, so Git cannot provide a committed-baseline diff. No staging, commit, remote configuration or push was performed. The iOS repository was not modified; its pre-existing untracked documentation remains untouched.

## Deliverables

- [Structural fingerprint report](PHASE2B_FINGERPRINT_REPORT.md): twelve areas, full class/package/DEX mappings, method/field examples, manifest/resource references, observed relationships, confidence and unknowns.
- [Feature mapping](PHASE2B_FEATURE_MAPPING.md): all thirteen requested iOS feature concepts mapped to Android evidence, feasibility limitations and confidence.
- [Patch compatibility design](PHASE2B_PATCH_COMPATIBILITY.md): version/symbol/resource/manifest/native requirements, dependency gates, mismatch behavior and no automatic fallback.
- [Reusable JSON Schema](FINGERPRINT_SCHEMA.json): Draft 2020-12; no hardcoded package, version or current resource IDs.
- [Fingerprint inventory](PHASE2B_FINGERPRINT_INVENTORY.json): metadata-only measured baseline.
- This implementation report, reproducible host scripts, synthetic regression tests and CI validation updates.

## Findings and inventory summary

| Coverage | Verified result |
| --- | --- |
| DEX scan | Eight files; 57,767 class definitions |
| Selected classes | 89: 49 query candidates plus 40 ancestors |
| Selected declared methods / fields | 1,485 / 869 |
| SDK method-declaration cross-check | 21 classes, exact agreement |
| Resource declarations / selected fingerprints | 28,524 / 210 |
| Manifest application/components/aliases | 145 |
| Native libraries | 156, with per-file hash, ELF machine/class and load alignment |
| Structural relationships | 3,022: 2,844 invoke references, 89 superclass declarations, 68 resource literals, 21 aliases |
| Decoded resource files | Five, resolved through resource-table file mappings |
| Tool/resource failures in final study | None |

High-value verified declarations include watchwhile.MainActivity.onCreate(Bundle)V (classes.dex), BackgroundPlayerService.onStartCommand(Intent, int, int)I (classes2.dex), VideoQualityPrefsFragment.aS()V (classes4.dex), SubtitleWindowView.onMeasure(II)V (classes6.dex), PivotBar (classes2.dex) and the Shorts pager/progress classes (classes4.dex). The inventory records exact descriptor syntax rather than assigning meanings to obfuscated methods.

Launcher aliases target MainActivity; application startup traverses defined obfuscated superclasses. The background service has an observed Android Service superclass chain and explicit lifecycle calls. Quality-resource literals resolve to actual preference XML, including obfuscated ZIP paths. PlaybackControllerWrapper has typed SabrSeek/Time/SelectableFormats boundaries, but their safe externally usable semantics are not established. Home/feed containers, watch composition, navigation views, offline services and logging/network boundaries are identified with unresolved controller ownership.

An important privacy observation is the network XML's base cleartext allowance, with explicit cleartext prohibitions for youtube.com/googleapis.com. This does not demonstrate actual traffic or native-stack enforcement. No global HTTPS claim is made. Native ELF load alignments are measured, not device loading/page-size certification.

All thirteen Android feature implementations remain not started. SponsorBlock opportunity confidence is LOW; trustworthy video identity/time/seek and consent boundaries remain unresolved. The full per-feature matrix distinguishes structural existence from implementation feasibility. No native SponsorBlock absence claim is made from a bounded candidate study.

## Implementation decisions

Added a small standard-library DEX 035 metadata reader instead of installing a full decompiler. It parses bounded declaration tables, class data, prototypes, fields, code-item instruction lengths/hashes, modified UTF-8 and ULEB128. It does not execute instructions or rewrite files. The existing Phase 2A archive/DEX integrity logic and SDK adapter are reused.

Discovery queries are separate from release identity. Ancestor traversal is bounded to two levels. SDK disassembly checks selected method declarations independently and provides explicit invoke/resource-literal references; no string matches are promoted to call edges. Resource paths are resolved from the table rather than guessed from symbolic names. Native inspection is limited to hashes and ELF/program headers. JSON Schema validation plus cross-record checks resolve class/method/resource/DEX/feature references and prevent patch_supported=true.

The published inventory contains no instruction bodies, resource values, arbitrary APK strings or private keys. Ignored raw evidence contains disassembly/resources and must remain local. CI validates metadata and generated synthetic fixtures without acquiring or requiring the proprietary APK.

The generator itself adds no external dependency. Standards-compliant schema validation uses host-only jsonschema 4.25.1 from tests/requirements.txt. No Android runtime or Gradle dependencies changed. Third-party host dependency resolution is separate from the pinned Android toolchain.

## Validation results

| Check | Result |
| --- | --- |
| Initial hash/package/version/code gate | PASS |
| ZIP CRC and DEX structural integrity | PASS through reused Phase 2A inspection |
| Eight DEX metadata tables / selected member parsing | PASS |
| 21 independent SDK declaration checks | PASS |
| JSON Schema meta-schema and generated inventory | PASS |
| Fresh-run reproducibility | PASS; a second final-script run produced byte-for-byte identical metadata; inventory SHA-256 8f8c78372af7f14a97a395c1f0e2a33cfa99da7c255ff220cf31104fb6040582 |
| Cross-record references, ownership and hash consistency | PASS |
| Python tests | 35 passed: 22 existing and 13 new |
| Script syntax validation | PASS |
| Gradle help/test/assembleDebug | BUILD SUCCESSFUL in 9s; 58 tasks, 1 executed/57 up-to-date |
| Android/JVM domain tests | NO-SOURCE, unchanged; no feature coverage claimed |
| Original and foundation APK signatures | PASS (YouTube v3/v3.1/source stamp; foundation v2) |
| Original APK hash after analysis | PASS, matches expected hash |
| Workflow YAML/actionlint | PASS locally |
| Structure and limited source secret/key checks | PASS |
| Remote GitHub workflow | NOT RUN; no push performed |
| Physical device/runtime tests | NOT RUN; outside this read-only study |

The new tests cover a generated DEX class/field/method/code hash, truncated/invalid headers, out-of-bounds tables, invalid indices/ULEB/string sizes, integrity/identity aborts, symbol-to-obfuscated-resource mapping, explicit versus string-only call evidence, ELF/unknown headers, published schema validity and rejection of inconsistent/unsupported claims. Fixtures contain no proprietary binary data.

Measured tools: Python 3.15 locally, Temurin 17.0.20.1, aapt2 2.19-11948202 (Build Tools 35.0.0), SDK command-line tools/apkanalyzer revision 19.0, apksigner 0.9, jsonschema 4.25.1, PyYAML 6.0.3 and actionlint 1.7.7. No JADX/Apktool is installed or required for the completed coverage. The metadata reader and selected disassembly do not replace full semantic/native analysis.

## Files created (12)

- `Documentation/PHASE2B_FINGERPRINT_REPORT.md`
- `Documentation/PHASE2B_FEATURE_MAPPING.md`
- `Documentation/PHASE2B_PATCH_COMPATIBILITY.md`
- `Documentation/FINGERPRINT_SCHEMA.json`
- `Documentation/PHASE2B_FINGERPRINT_INVENTORY.json`
- `Documentation/PHASE2B_IMPLEMENTATION_REPORT.md`
- `tools/apk-analysis/dex_reader.py`
- `tools/apk-analysis/fingerprint_apk.py`
- `tools/apk-analysis/study_targets.json`
- `tools/apk-analysis/validate_fingerprints.py`
- `tests/test_fingerprints.py`
- `tests/requirements.txt`

## Files modified (8)

- `.github/workflows/android.yml`: install host validator dependency and validate published inventory.
- `tools/validate_foundation.py`: require Phase 2B deliverables/tools/tests.
- `tools/apk-analysis/README.md`: document read-only workflow and limits.
- `README.md`: current phase and test prerequisite.
- `Documentation/BUILD_GUIDE.md`: schema dependency, commands and current test coverage.
- `Documentation/ARCHITECTURE.md`: host fingerprint boundary and Phase 2C approval gate.
- `Documentation/ROADMAP.md`: mark Phase 2B complete and stop before Phase 2C.
- `Documentation/SECURITY.md`: raw-evidence handling, parser limits and measured network-policy caveat.

Ignored local artifacts include intermediate and final JSON, SDK resources/disassembly/command records, test/build logs and existing caches. No proprietary APK or resource/code body is part of the source inventory. The Phase 2A reports remain historical records.

## Reproduction

Set JAVA_HOME/ANDROID_HOME using BUILD_GUIDE, then from repository root:

```powershell
python -m pip install -r tests/requirements.txt
python tools/apk-analysis/fingerprint_apk.py "main apk/YouTube_21.44.528_APKPure.apk" --releases patches/releases.json --output validation-local/new-study.json --evidence validation-local/new-study-evidence
python tools/apk-analysis/validate_fingerprints.py validation-local/new-study.json
python tools/validate_foundation.py
python -m unittest discover -s tests -v
.\gradlew.bat help test assembleDebug --warning-mode all --stacktrace --console=plain
```

Use fresh output/evidence names. The final measured evidence is validation-local/phase2b-final-evidence, with exact SDK argument arrays and output in commands.json. Additional raw native/resource data is derived read-only from the input. Schema validation itself never opens the proprietary APK.

The final-script reproduction used validation-local/phase2b-repro.json and phase2b-repro-evidence (hashed evidence filenames); its inventory is byte-for-byte identical to the published baseline. The initial final-evidence directory predates the evidence-filename hardening but contains the same measured SDK output and metadata. Both runs passed the input gate and post-analysis hash check.

## Remaining unknowns and next phase

Unresolved: full obfuscated call/data flow, actual engine/experiment selection, clock/seek/video identity semantics, thread/lifecycle and entitlement constraints, subtitle track selection, feed/tab model ownership, native algorithms, telemetry payload/redaction/retention, runtime network enforcement, physical-device behavior, stable-channel provenance and a tested fallback release. The study is complete for its bounded read-only deliverables; it does not certify safe modification points.

Recommended next phase, only after explicit approval: a scoped semantic and compatibility-validation plan, starting with caller/data-flow evidence for video identity, time and seek, plus negative fingerprint tests. Decide device/runtime test scope separately before executing the host app. Do not inject patches or implement playback/SponsorBlock merely because these structural candidates exist.

STOP: Phase 2C has not begun. Await user approval. No GitHub push.
