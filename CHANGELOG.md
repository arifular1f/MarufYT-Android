# Changelog

## 0.3.0-dev (Phase 3) — 2026-03

- **SponsorBlock Automatic Skipping Controller:** Implemented `SponsorBlockPlaybackController` with continuous timeline position evaluation, active playback context disambiguation, 250ms debouncing, repeated-skip prevention by UUID, and fail-open resilience.
- **Settings-to-Runtime Bridge:** Formalized versioned configuration schema (`CONFIG_VERSION = 1`) across 15 operational sections with SHA-256 tamper-evident export/import bundles and hardcoded zero-telemetry invariance.
- **Companion App Overhaul:** Rewrote `MainActivity.java` and created `MarufConfig.java` featuring a premium dark-hacker/AMOLED UI, responsive window insets, status pills, and interactive preference controls.
- **Automated Verification Expansion:** Expanded the test suite to 80 Python unit tests and added Java-level JUnit tests for preference management and theme resolution.
- **Comprehensive Audits:** Published `ANDROID_SECURITY_AUDIT.md`, `ANDROID_PERFORMANCE_REPORT.md`, `ANDROID_ARCHITECTURE.md`, `ANDROID_DEVELOPMENT_GUIDE.md`, and `ANDROID_FEATURE_MATRIX.md`.
- **Repository Professionalization:** Redesigned README, added EditorConfig, Code of Conduct, and YAML issue templates.

## 0.2.0-preview.1 — 2026-11-03

- Preserve the Foundation and Phase 2A/2B analysis toolchain and evidence.
- Add a standalone native settings preview with persisted System/Light/Dark appearance and reset; all thirteen sections identify actual availability.
- Add an explicit host SponsorBlock lookup client with hash-prefix requests, category filtering, validation, finite timestamp utilities, timeout handling and bounded in-memory cache. No player skipping.
- Extend static semantic study of rational media time, lifecycle and seek boundaries; record unresolved runtime/entitlement/video-identity dependencies.
- Add source-only release packaging/auditing, checksums, contributor/security documents and CI/release automation.
- Playback patches, background playback and YouTube runtime customization remain unavailable. Device testing and original-code licensing remain pending.
