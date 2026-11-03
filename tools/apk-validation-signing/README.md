# apk-validation-signing

Future responsibility: APK validation and explicit signing with external keys.

Java 17 extension module remains empty. Phase 2A host adapter ../marufyt/analysis.py validates input ZIP/DEX integrity and invokes apksigner verification. It never signs or modifies an APK. Output validation, signing and execution reports remain future work. See Documentation/ANDROID_PATCH_ARCHITECTURE.md.
