# YouTube version compatibility

Phase 2A, 2026-11-03 (Asia/Kuala_Lumpur). Binary facts are in [the forensic report](YOUTUBE_APK_FORENSIC_REPORT.md); implementation/test results are in [the phase report](PHASE2A_IMPLEMENTATION_REPORT.md).

## Verified local identity

Input: `C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk`.

- Size: 220,576,405 bytes.
- SHA-256: `55be430ce82dcedcb737ea27d1b78576737b75d11cde04aa89989e5376d3ae6c`.
- Package: `com.google.android.youtube`; version name `21.44.528`; version code `1561310186`.
- Minimum SDK 29, target/compile SDK 37, compile codename `DEV`.
- Universal native-library inventory: arm64-v8a, armeabi-v7a, x86, x86_64.
- Read-only ZIP, DEX, manifest and signing analysis succeeded. No patch execution exists.

## External metadata and limits

The [APKPure version-history page](https://apkpure.net/youtube-app/com.google.android.youtube/versions), consulted 2026-11-03, lists 21.44.528, code 1561310186, dated October 31, 2026, as Latest, with Android 10+ and a rounded 210.4 MB size. These identity and size claims agree with the local binary. Its [main listing](https://apkpure.net/youtube-app/com.google.android.youtube) exposed an older date/size snapshot, so the listing views are not completely synchronized.

This is corroboration of the distributor's claim, not independent proof of Google's stable rollout channel. No publisher-controlled exact-version stable release record or published exact-file SHA-256 was established. Manifest BuildType=RELEASE distinguishes a release build configuration; it does not prove stable rather than beta distribution. Compile codename DEV is another reason to keep release-channel certainty separate from metadata identity. Signature verification demonstrates cryptographic consistency, not safety or a complete chain of download provenance.

## Recommendation

Primary **research** input: this exact SHA-pinned 21.44.528 binary. Stable-channel designation: UNKNOWN. Patch support: NONE. A safe, reproducible research candidate is not a supported modified release.

Stable fallback: UNKNOWN; `fallback` remains null. APKPure lists older Android versions, but none was locally analyzed or tested. iOS versions 21.43.5 and 21.39.4 are not evidence of Android compatibility. Do not designate a stable Android fallback from those iOS numbers or a distributor's popularity label.

## Implemented compatibility model

`patches/releases.json` schema version 1 contains primary metadata and an optional fallback. `tools/marufyt/models.py` extracts package, exact version string, 64-bit version code (including versionCodeMajor), and SDK metadata. Missing metadata stays null in machine output and UNKNOWN in reports; versions are not interpreted as semantic version ranges.

`tools/marufyt/compatibility.py` matches package + version name + version code + SHA-256. Every recognized release returns RESEARCH_ONLY and patch_supported=false. A mismatch raises UNSUPPORTED_INPUT; CLI returns exit code 2 and writes its rejection metadata. Tool/input errors return 1; successful analysis returns 0. Existing outputs are never overwritten. Malformed release metadata is rejected.

PatchMetadata and PatchRegistry implement metadata-only registration and preflight: reject duplicate IDs, unsupported exact version pairs, missing dependencies and cycles; return a deterministic dependency-first plan. There are **zero production patch registrations**, no patch implementations and no executor. Test metadata is synthetic and confined to tests. Dependency planning alone does not establish that any bytecode location or patch can work.

## Structural feasibility and future gates

The host tooling can inspect the current multidex/resources/native ZIP structure with the existing SDK tools. The foundation's SDK 36 app is a separate package; its minimum SDK 26 does not lower the YouTube input's minimum SDK 29. No SDK upgrade is necessary for the completed static inspection. Rebuilding a host targeting SDK 37 would need a separately reviewed toolchain assessment in a later phase.

Before a version becomes patch-supported, require exact binary identity and certificate review, complete input/split resolution, bytecode/resource fingerprint evidence, negative-version tests, isolated transform validation, post-output integrity/signature checks and physical-device results. None of those future patch/runtime gates is satisfied by this phase's static analysis alone.
