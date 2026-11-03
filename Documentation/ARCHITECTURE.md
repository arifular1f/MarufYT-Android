# Architecture

| Boundary | Location / Gradle module | Future responsibility |
| --- | --- | --- |
| Android shell | app / :app | Lifecycle and composition root |
| UI settings | app/ui-settings | Explicit preferences and Android presentation |
| APK analysis | tools/apk-analysis | Read-only metadata, hashes and compatibility |
| Patch management | patches/patch-management | Compatibility gates and patch orchestration |
| SponsorBlock | integrations/sponsorblock | Opt-in client contracts and segment models |
| Player customization | integrations/player-customization | Player adapters and preference models |
| Privacy and diagnostics | integrations/privacy-diagnostics | Consent, redaction and local diagnostics |
| APK validation/signing | tools/apk-validation-signing | Package validation and explicit signing |

Only :app contains Android runtime implementation: the standalone preview with companion appearance/reset controls. All other Gradle modules are independent Java 17 libraries with no runtime classes or dependencies. The UI settings boundary remains within app to avoid the cost of an unused Android library. Host tooling is separate; no YouTube playback integration is implied.

Phase 2A adds a separate Python host-tooling package for read-only analysis, exact version gates and metadata dependency planning. Android runtime modules remain as described above. Current contracts and status are documented in [ANDROID_PATCH_ARCHITECTURE.md](ANDROID_PATCH_ARCHITECTURE.md).

Phase 2B adds a gated DEX 035 metadata reader, selected SDK-disassembly cross-checks, resource indirection resolution, manifest/native fingerprints and schema validation under tools/apk-analysis. Published metadata and limitations are in [PHASE2B_FINGERPRINT_REPORT.md](PHASE2B_FINGERPRINT_REPORT.md). These tools run on the host only; no runtime integration or patch executor exists. Phase 2C requires explicit approval.

The consolidated preview adds functional standalone appearance/reset UI and a separate host SponsorBlock lookup client. It does not add a YouTube runtime adapter. Current semantic gaps, source-only release boundaries and actual verification are recorded in [the final release report](MARUFYT_ANDROID_FINAL_RELEASE_REPORT.md). Historical phase reports describe their original states; the consolidated request authorizes this later work without additional internal phase approvals.

Future dependency direction: host orchestration consumes analysis and validation contracts; app composes approved integration implementations through narrow interfaces. Integrations should not depend on one another. Keep host tools independent of Android lifecycle APIs. Introduce dependencies and tests only when concrete contracts are approved. Domain unit tests belong in each module's src/test/java directory.
