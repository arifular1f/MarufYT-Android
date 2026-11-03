# MarufYT Android 0.2.0-preview.1

Developer preview of a standalone settings companion and APK research tooling. **No YouTube modification, automatic SponsorBlock skipping, background playback or patched APK is included.**

- Native companion: thirteen availability sections; working System/Light/Dark appearance selection and reset. Device rendering/persistence verification is pending.
- Host SponsorBlock CLI: explicit privacy-prefix lookup, category/interval validation, timeout/errors and memory cache; no player actions.
- SHA-pinned analysis and fingerprints for user-supplied YouTube 21.44.528 (1561310186). This is a research target, not a supported patched release or independently certified stable distribution.
- Tested host parsers/compatibility/release packaging, Android unit policy tests, debug build, lint and signature verification.
- Source-only ZIP, SHA256SUMS.txt and RELEASE_REPORT.json. No YouTube/Google components, raw disassembly, dataset, installer, credentials or signing keys.

Known limitations: no physical device attached; active video identity/seek/lifecycle/entitlement integration unverified; no fallback APK tested. Original Android-code licensing is not assigned; this is a source-available review preview, not yet an open-source licensed release. Gradle wrapper notices are preserved.

Build/install instructions: Documentation/INSTALLATION.md. Runtime and security evidence: Documentation/SEMANTIC_VALIDATION.md and SECURITY.md. CI debug APKs are development artifacts only and are not release assets. Not affiliated with YouTube or Google.
