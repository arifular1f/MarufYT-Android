# apk-analysis

Future responsibility: Read-only APK metadata, hashes and compatibility analysis.

Java 17 extension module remains empty. Phase 2A host analysis is implemented in ../marufyt/analysis.py and ../marufyt/models.py, invoked by ../analyze_apk.py. It performs read-only ZIP/DEX/manifest inventories and hashes using standard-library code and SDK adapters. Synthetic tests live in tests/test_analysis.py. No transformation engine exists.

Phase 2B adds fingerprint_apk.py and dex_reader.py: gated read-only DEX declarations/instruction hashes, SDK-disassembled explicit edges, manifest components, resource ID/file mappings and ELF metadata. Selection queries are version-neutral and configurable in study_targets.json. No transformation or patch executor exists. See Documentation/PHASE2B_FINGERPRINT_REPORT.md for exact coverage and limits.

From repository root, with ANDROID_HOME and JAVA_HOME set, use fresh output/evidence paths:

```powershell
python tools/apk-analysis/fingerprint_apk.py "main apk/YouTube_21.44.528_APKPure.apk" --releases patches/releases.json --output validation-local/new-fingerprints.json --evidence validation-local/new-fingerprint-evidence
python -m pip install -r tests/requirements.txt
python tools/apk-analysis/validate_fingerprints.py validation-local/new-fingerprints.json
```

The generator itself uses only the standard library and installed Android SDK/JDK. The validator requires the host-only JSON Schema dependency. Raw disassembly/resources remain ignored; the published inventory contains identifiers/hashes/relationships, not code bodies or resource values. Neither CI validation nor synthetic unit tests need a proprietary APK. The parser supports DEX 035 and fails explicitly for other formats; future formats need reviewed support, not a version-label bypass.
