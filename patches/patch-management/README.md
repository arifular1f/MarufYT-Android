# patch-management

Future responsibility: Version-gated patch plans and orchestration.

Java 17 extension module remains empty. Phase 2A host tooling in tools/marufyt/compatibility.py implements exact research-input gates, metadata registration and dependency preflight; patches/releases.json records one research candidate and no fallback. No production patches are registered. No executor or APK modification code exists. Synthetic tests cover unsupported versions, missing dependencies, duplicates and cycles.
