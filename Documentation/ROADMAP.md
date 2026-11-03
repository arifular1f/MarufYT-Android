# Roadmap

1. **Foundation (completed):** lightweight Android shell, isolated module boundaries, pinned build, CI and documentation.
2. **Phase 2A (completed):** user-supplied local APK inspection, exact research-input gates, dependency preflight and synthetic tests. See `PHASE2A_IMPLEMENTATION_REPORT.md`.
3. **Phase 2B (completed):** read-only structural fingerprints, resource/manifest/native relationships and schema-backed evidence across twelve study areas. See `PHASE2B_IMPLEMENTATION_REPORT.md`.
4. **Consolidated Preview (completed):** standalone settings preview, host SponsorBlock lookup client, ThemeMode JVM tests, source release packaging (`v0.2.0-preview.1`). See `MARUFYT_ANDROID_FINAL_RELEASE_REPORT.md`.
5. **Phase 2C — Deep Semantic Validation & Feature Implementation Readiness (completed):**
   - Investigated caller and data flows for Video ID, Playback Timeline (`Time` microseconds scale), Seek operations (`onSabrSeek` vs `seekTo`), `BackgroundPlayerService` entitlement gates, Shorts (`ShortsPlayerProgressPresenter`), and Player Lifecycle (`MainActivity` / Dagger TikTok / ExoPlayer).
   - Formally classified all 13 features across 5 feasibility tiers.
   - Implemented automated data-flow contracts (`tools/marufyt/semantics.py`) and 14 unit tests (`tests/test_semantics.py`).
   - Prepared practical Android device test plan (`DEV-01` through `DEV-07`).
   - See `Documentation/PHASE2C_SEMANTIC_VALIDATION_REPORT.md`.
6. **Next Milestones (Awaiting Phase 3 Approval):**
   - **Milestone 1:** SponsorBlock automatic skip & timeline observer integration.
   - **Milestone 2:** Background playback & entitlement bypass investigation (`Lasll` analysis).
   - **Milestone 3:** UI & navigation customization (`PivotBar`, `YouTubePlayerOverlaysLayout` gestures, Shorts styling).
   - **Milestone 4:** Full settings synchronization between companion app and hook runtime.
