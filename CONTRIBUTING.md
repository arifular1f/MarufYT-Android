# Contributing

Start with LICENSE_STATUS.md: original-code licensing is not finalized. Discuss contribution licensing with the maintainer before submitting code intended for reuse.

Use Java 17 and the pinned Gradle wrapper. Install host validation dependencies with `python -m pip install -r tests/requirements.txt`. Run `python -m unittest discover -s tests -v`, the fingerprint validator, and `gradlew test assembleDebug lintDebug` (Windows: gradlew.bat).

Keep analysis, tooling and Android runtime code separate. Tests must use generated or project-owned fixtures. Never submit proprietary APKs, raw decompiled code, API datasets, credentials or signing keys. Use main apk/ and validation-local/ only for ignored local work.

Describe exact evidence, negative cases and device results. A declared method or static call is not runtime validation. Avoid controls without implemented behavior and do not weaken integrity/version tests. See the issue/PR templates and Documentation/DEVICE_TEST_CHECKLIST.md.
