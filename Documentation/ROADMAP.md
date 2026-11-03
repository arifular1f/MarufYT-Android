# Roadmap

1. Foundation (completed): lightweight Android shell, isolated module boundaries, pinned build, CI and documentation.
2. Phase 2A (implemented): user-supplied local APK inspection, exact research-input gates, dependency preflight and synthetic tests. Stable-channel status remains UNKNOWN. See PHASE2A_IMPLEMENTATION_REPORT.md.
   Phase 2B (implemented): read-only structural fingerprints, resource/manifest/native relationships and schema-backed evidence across twelve study areas. See PHASE2B_IMPLEMENTATION_REPORT.md. Static candidates do not establish runtime or patch compatibility.
3. Separately approved: patch lifecycle and integration contracts, then scoped implementation with compatibility gates and rollback tests.
4. Separately approved: opt-in settings, privacy controls and physical-device verification.
5. Separately approved: validation, external signing configuration and release provenance.

The consolidated task authorizes later feasible work: semantic analysis, a standalone settings preview, host SponsorBlock lookup and source-only preview release preparation. See MARUFYT_ANDROID_FINAL_RELEASE_REPORT.md. Runtime hooks remain blocked by missing evidence; never fetch proprietary APKs in CI or promote static matches to working playback features.
