# Security policy

Use GitHub private vulnerability reporting if enabled, or contact the maintainer privately through an available verified GitHub channel. Do not post secrets or proprietary APKs in public issues.

The Android preview has no network permission or telemetry. The optional host SponsorBlock lookup uses TLS verification, a fixed HTTPS origin, hash-prefix queries, bounded responses/timeouts and memory-only caching; redirects are rejected. A hash prefix provides limited privacy, not anonymity.

No release signing credentials are configured. Android debug signing keys are local development material and must never be committed. GitHub releases contain source/tooling/documentation only. Review Documentation/SECURITY.md and Documentation/RELEASE_GUIDE.md for input validation, static-analysis limits and artifact rules.

Neither valid APK signatures nor successful static analysis certify the proprietary host's safety. No safe YouTube playback hook has been established for this preview.
