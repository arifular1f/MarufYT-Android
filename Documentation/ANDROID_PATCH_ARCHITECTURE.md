# Android patch architecture

Phase 2A: read-only analysis and compatibility preflight. Evidence anchor: the 220,576,405-byte input at `C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk`, SHA-256 `55be430ce82dcedcb737ea27d1b78576737b75d11cde04aa89989e5376d3ae6c`. See [forensics](YOUTUBE_APK_FORENSIC_REPORT.md) for tool versions and [validation results](PHASE2A_IMPLEMENTATION_REPORT.md). No bytecode transforms or playback changes exist.

## Preserve the existing boundaries

| Boundary | Existing location | Implemented now | Future contract/responsibility |
| --- | --- | --- | --- |
| APK analysis | tools/apk-analysis; host adapter tools/marufyt/analysis.py | Streaming SHA-256, bounded ZIP/CRC/DEX checks, SDK metadata/signing adapters, inventories | Structured bytecode/resource fingerprints and complete split-set resolution |
| Version identity | tools/marufyt/models.py | Decoded XML identity and SDK parsing; unknown preservation | Evidence schema evolution without inventing version support |
| Patch manager | patches/patch-management; patches/releases.json; tools/marufyt/compatibility.py | Exact release gate, metadata registry, dependency preflight only | Patch metadata, transform contracts, execution reports and failure isolation |
| Player | integrations/player-customization | Empty Java module | Background playback adapters, quality, gestures and player preferences |
| SponsorBlock | integrations/sponsorblock | Empty Java module | Opt-in HTTPS API client, segment/category models, skip policy and preferences |
| UI settings | app/ui-settings within :app | Documented boundary only; app shows foundation status | MarufYT Settings, dark/light themes, player, Home/Feed, Shorts, navigation/tabs and general preferences |
| Privacy | integrations/privacy-diagnostics | Empty Java module; host subprocesses use no shell | HTTPS and redirect rules, sensitive-data handling, log redaction, network-request review and consent |
| Validation/signing | tools/apk-validation-signing; host analysis adapter | Input CRC/hash/identity and apksigner verification; metadata report output | Output validation, signing with external keys, build/provenance report |

The six Java library modules remain empty and dependency-free. Python host adapters are a small tooling package, not Android runtime libraries. They operationalize the documented analysis/preflight boundaries without forcing Python into an Android APK or duplicating Java functionality. Module READMEs point to their implemented host adapters. No untested Java API scaffolding was added.

## Data flow and ownership

User-provided ignored input -> streaming inventory -> SDK manifest/signing adapters -> immutable identity -> SHA-pinned research gate -> metadata report. No stage writes to the source APK. The CLI refuses existing output files and output APK/container extensions; it hashes the source before and after analysis. Raw local evidence stays in ignored validation-local and is not uploaded by CI.

Use decoded manifest data for identity and split declarations; use aapt2 badging for resolved labels and implied features. Preserve SDK command arrays, return codes, stdout/stderr and tool versions locally. Published reports contain selected metadata, public certificate fingerprints and inventories; raw manifests may contain embedded service identifiers and must not be committed indiscriminately.

The APK is a universal standalone candidate with eight DEX files; inspection does not identify a single patchable player method or prove runtime completeness. No JADX/Apktool install was needed for this phase's inventory. A later approved fingerprint study may justify one.

## Patch execution design (not implemented)

Future Patch definitions should expose an ID, revision, target package, exact validated versions and fingerprints, dependencies, affected files, prerequisites and expected postconditions. Registration must never execute a patch. Preflight resolves and validates the complete dependency graph before making any output.

Future execution must use a new staging directory with an immutable source, structured per-patch states (planned, running, succeeded, failed, blocked), safe error codes, redacted diagnostics and postcondition checks. On failure, block dependents and discard staged output; independent work may continue only for diagnostics and must never publish a partially patched APK. Commit an output only after all required transforms and validation succeed. No such executor or state machine is claimed in Phase 2A.

Signing stays behind a separate explicit boundary: verify input before processing, validate output package/integrity before signing, obtain a key only from an external local/CI secret mechanism, then verify the final signature. This phase invokes verification only; it never signs the proprietary input.

## Tests and extension policy

Synthetic tests cover identity/unknowns, version code major fields, XML rejection, Windows paths, unsafe/corrupt/container ZIPs, DEX checks, size limits, output overwrite rejection, exact research gates and registry dependency errors. CI runs these without proprietary inputs. Actual SDK adapter calls and the complete supplied APK were exercised locally; see the forensic report for their exact commands. Gradle build and JVM NO-SOURCE results are reported separately from Python test coverage.

Keep player/SponsorBlock/UI/privacy implementation pending. Add no switches until their corresponding behavior and tests exist. Do not port Objective-C++ hooks or iOS dependency code into Android modules. Phase 2B requires explicit approval.
