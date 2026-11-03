# Installation

GitHub preview releases contain source/tooling/documentation only. They do not include a YouTube APK or an Android installer. Verify the downloaded source ZIP with its attached SHA256SUMS.txt, extract into a new directory, and follow BUILD_GUIDE.md.

Windows prerequisites: JDK 17, Android SDK platform 36/Build Tools 35.0.0/platform-tools, Python 3.12+ and Git. Set JAVA_HOME and ANDROID_HOME. Then:

```powershell
python -m pip install -r tests/requirements.txt
python tools/validate_foundation.py
python -m unittest discover -s tests -v
.\gradlew.bat test assembleDebug lintDebug --stacktrace
```

Enable USB debugging on an API 26+ phone, authorize the computer, and run:

```powershell
adb devices -l
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Launch MarufYT Preview. It is a separate companion with appearance/reset controls. It does not replace YouTube, ask for a Google login or control playback. Debug signatures may differ between machines/CI; a signature conflict requires uninstalling the old companion, which clears its appearance choice.

The companion contains no native libraries and targets API 26+, but actual device verification is pending. The separately supplied research YouTube APK requires API 29+ and has four ABI payloads; that is static input compatibility, not companion playback support. Follow DEVICE_TEST_CHECKLIST.md before claiming installation/runtime success.
