# YouTube APK forensic report

Analyzed locally on 2026-11-03 (Asia/Kuala_Lumpur). All binary findings below are measured from the supplied input; interpretations and unknowns are explicitly labeled.

## Input and integrity

- Exact path: `C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk`.
- File size: 220,576,405 bytes (210.358 MiB).
- SHA-256 before and after analysis: `55be430ce82dcedcb737ea27d1b78576737b75d11cde04aa89989e5376d3ae6c`.
- Original unchanged: VERIFIED (matching streaming hashes). No archive extraction, modification, code injection or APK redistribution performed.
- ZIP entry CRCs: PASS for every streamed entry. No duplicate, unsafe, encrypted or oversized entries detected. DEX header length, endian tag, file length, SHA-1 and Adler-32 checks: PASS for every root DEX.
- These checks demonstrate structural/cryptographic consistency; they are not a malware verdict, proof of download provenance, or a device test.

## Package identity and Android compatibility

| Field | Verified value |
| --- | --- |
| Package ID | com.google.android.youtube |
| Version name | 21.44.528 |
| Version code | 1561310186 |
| Application label (resolved by aapt2) | YouTube |
| minSdk | 29 (Android 10+) |
| targetSdk | 37 |
| compileSdk / codename | 37 / DEV |

The separate MarufYT foundation app still uses compile/target 36 and minSdk 26. This static analysis did not require upgrading that app. The YouTube input cannot be assumed to run on Android 8/9 merely because the foundation can. Target/compile 37 and DEV are manifest values, not proof of release-channel membership.

## Distribution and split assessment

Verified manifest facts: no root split name, no uses-split dependencies, no isSplitRequired=true, and no requiredSplitTypes. Metadata declares com.android.dynamic.apk.fused.modules=base and com.android.stamp.type=STAMP_TYPE_STANDALONE_APK. com.android.stamp.source names the Play store; that string alone does not establish how the local file was obtained.

The manifest also references com.android.vending.splits. Its res/xml/splits0.xml resource was decoded; every split attribute is empty, with languages pointing into the base package. The existence of the PlayCoreMissingSplitsActivity class name does not by itself require additional splits.

Assessment: structurally a standalone universal APK, suitable for the completed static analysis, rather than an XAPK/APKS container or an ABI-only split. No additional install-time split requirement was found. No OBB entry is present and no OBB dependency was identified in manifest metadata. Runtime asset downloads, server feature delivery, Google services availability and full installation/playback usability remain UNKNOWN until device/code-level checks. No claim of proven runtime completeness is made.

## Archive, DEX, resources and assets

- ZIP entries: 17,047; total declared uncompressed bytes: 465,176,681.
- Root DEX files: 8; each uses DEX version 035.
- Resource entries under res/: 16,170; resources.arsc: 20,843,656 bytes.
- Assets: 443; native libraries: 156.
- Assets include fonts, binary protobuf/config files, baseline.prof/baseline.profm and image/effect assets. Their names and sizes are inventoried locally; no proprietary asset contents are included in this report.
- Other top-level groups include META-INF, com, okhttp3, licensing files and stamp-cert-sha256. The full 17,047-entry inventory with sizes/CRCs is retained only in ignored validation-local/youtube-phase2a-final.json.

| DEX file | Uncompressed bytes | CRC32 | Header/checksums |
| --- | ---: | --- | --- |
| classes.dex | 8,398,640 | c9ec09a8 | PASS |
| classes2.dex | 7,929,932 | 16814291 | PASS |
| classes3.dex | 7,708,592 | 736b3a8a | PASS |
| classes4.dex | 7,620,428 | ac6f772a | PASS |
| classes5.dex | 7,755,532 | e2b53153 | PASS |
| classes6.dex | 8,045,388 | 32514e03 | PASS |
| classes7.dex | 6,699,636 | aed38ed3 | PASS |
| classes8.dex | 590,460 | 01292fd0 | PASS |

## Native libraries and CPU compatibility

Verified archive directories: arm64-v8a, armeabi-v7a, x86, x86_64, with 39 .so files per ABI (156 total). ARM64 native payload is present. Universal here means these four ABI payloads are packaged together; ELF execution, 16 KB page-size behavior, CPU instructions and device-level loading have not been tested.

The following matrix lists every native library and its uncompressed byte size for each ABI.

| Library | arm64-v8a | armeabi-v7a | x86 | x86_64 |
| --- | ---: | ---: | ---: | ---: |
| libGfxPluginCardboard_only_gles2.so | 121264 | 68868 | 126136 | 120176 |
| libandroid_gif_drawable_jni.so | 35656 | 26564 | 38640 | 35656 |
| libandroidx.graphics.path.so | 10320 | 8464 | 8448 | 10328 |
| libavif_android.so | 951352 | 721340 | 1266400 | 1894712 |
| libc2pa_embedder.so | 18680 | 5612 | 5544 | 18680 |
| libc2pajni_prod.so | 18680 | 5612 | 5544 | 18680 |
| libcardboard_sdk_jni.so | 121216 | 68844 | 130208 | 120128 |
| libcomposition.so | 18680 | 5612 | 5544 | 18680 |
| libcronet.157.0.8103.14.so | 7393984 | 4394176 | 7302708 | 8327664 |
| libdatastore_shared_counter.so | 10560 | 5864 | 6424 | 7424 |
| libdav1dJNI.so | 747640 | 586716 | 1000616 | 1643616 |
| libdrishti_jni_native.so | 18680 | 5612 | 5544 | 18680 |
| libelements.so | 18712 | 5628 | 5560 | 18712 |
| libelements2.so | 18680 | 5612 | 5544 | 18680 |
| libenvoy_jni.so | 18680 | 5612 | 5544 | 18680 |
| libfilterframework_jni.so | 70080 | 35032 | 59632 | 69160 |
| libframesequence.so | 284992 | 224456 | 384272 | 366072 |
| libgoogle3.so | 66667296 | 48846356 | 89104216 | 76874984 |
| libgvr_audio.so | 864248 | 596284 | 960644 | 877424 |
| libimage_processing_util_jni.so | 32528 | 24464 | 44876 | 49416 |
| libjingle_peerconnection_so.so | 18680 | 5612 | 5544 | 18680 |
| liblogsampler.so | 18680 | 5612 | 5544 | 18680 |
| libmedia3EffectJNI.so | 18920 | 9828 | 9764 | 18928 |
| libmemorymappedbufferjni.so | 18680 | 5612 | 5544 | 18680 |
| libmutatecomposition.so | 18680 | 5612 | 5544 | 18680 |
| libnative_crash_handler_jni.so | 53848 | 26984 | 51528 | 52944 |
| libnativecrashdetectorutil.so | 18680 | 5612 | 5544 | 18680 |
| libopusV2JNI.so | 169872 | 117992 | 171080 | 168632 |
| libplatypus.so | 18680 | 5612 | 5544 | 18680 |
| librenderer_gl_android.so | 18448 | 5472 | 5408 | 18448 |
| librenderer_gl_android_v1.so | 18448 | 5472 | 5408 | 18448 |
| libresampler.so | 360904 | 217972 | 389844 | 359136 |
| librive-android-v1.so | 4411768 | 3209572 | 5294396 | 4749376 |
| librive-android.so | 18728 | 5636 | 5568 | 18728 |
| libsurface_util_jni.so | 4896 | 3460 | 3812 | 4912 |
| libvpx.so | 398312 | 445380 | 510808 | 462720 |
| libvpxV2JNI.so | 54128 | 31392 | 47552 | 53216 |
| libxeno_capabilities_manifest.so | 18680 | 5612 | 5544 | 18680 |
| libxmp_data_handler.so | 18680 | 5612 | 5544 | 18680 |

## Required permissions

The decoded manifest declares the following 50 requested permissions. Declaration does not mean granted or required for every operation; actual grant policy varies by Android version and protection level. No permission was added to the foundation app.

- `android.permission.READ_MEDIA_VISUAL_USER_SELECTED`
- `android.permission.INTERNET`
- `android.permission.ACCESS_NETWORK_STATE`
- `android.permission.ACCESS_WIFI_STATE`
- `android.permission.WRITE_EXTERNAL_STORAGE`
- `android.permission.READ_MEDIA_IMAGES`
- `android.permission.READ_MEDIA_VIDEO`
- `android.permission.RECEIVE_BOOT_COMPLETED`
- `android.permission.MANAGE_DOCUMENTS`
- `android.permission.GET_ACCOUNTS`
- `com.google.android.providers.gsf.permission.READ_GSERVICES`
- `com.google.android.c2dm.permission.RECEIVE`
- `android.permission.WAKE_LOCK`
- `android.permission.NFC`
- `android.permission.CAMERA`
- `android.permission.FOREGROUND_SERVICE_CAMERA`
- `android.permission.FOREGROUND_SERVICE_MEDIA_PROJECTION`
- `android.permission.FOREGROUND_SERVICE_MICROPHONE`
- `android.permission.VIBRATE`
- `com.google.android.gms.permission.AD_ID_NOTIFICATION`
- `com.google.android.gms.permission.AD_ID`
- `com.google.android.youtube.permission.C2D_MESSAGE`
- `android.permission.GET_PACKAGE_SIZE`
- `android.permission.FOREGROUND_SERVICE`
- `android.permission.FOREGROUND_SERVICE_DATA_SYNC`
- `android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK`
- `android.permission.RUN_USER_INITIATED_JOBS`
- `android.permission.USE_FINGERPRINT`
- `android.permission.USE_BIOMETRIC`
- `android.permission.MODIFY_AUDIO_SETTINGS`
- `android.permission.READ_CONTACTS`
- `android.permission.ACCESS_FINE_LOCATION`
- `android.permission.ACCESS_COARSE_LOCATION`
- `android.permission.RECORD_AUDIO`
- `android.permission.READ_PHONE_STATE`
- `android.permission.SYSTEM_ALERT_WINDOW`
- `android.permission.ACCESS_LOCAL_NETWORK`
- `android.permission.HIGH_SAMPLING_RATE_SENSORS`
- `com.sec.android.provider.badge.permission.READ`
- `com.sec.android.provider.badge.permission.WRITE`
- `com.htc.launcher.permission.READ_SETTINGS`
- `com.htc.launcher.permission.UPDATE_SHORTCUT`
- `com.sonyericsson.home.permission.BROADCAST_BADGE`
- `com.sonymobile.home.permission.PROVIDER_INSERT_BADGE`
- `android.permission.POST_NOTIFICATIONS`
- `android.permission.ACCESS_ADSERVICES_ATTRIBUTION`
- `android.permission.ACCESS_ADSERVICES_AD_ID`
- `com.google.android.youtube.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`
- `com.android.vending.BILLING`
- `android.permission.DETECT_SCREEN_CAPTURE`

## Features

Explicit declarations: OpenGL ES 2.0 (0x20000) required; camera, portrait screen, telephony, microphone, location, GPS and network location optional. aapt2 additionally infers required faketouch and Wi-Fi from defaults/permission declarations. These are static filtering indications, not results from a physical device.

## Signing

apksigner verify --verbose --print-certs: PASS. Exact public certificate and signature output:

```text
Verifies
Verified using v1 scheme (JAR signing): false
Verified using v2 scheme (APK Signature Scheme v2): false
Verified using v3 scheme (APK Signature Scheme v3): true
Verified using v3.1 scheme (APK Signature Scheme v3.1): true
Verified using v4 scheme (APK Signature Scheme v4): false
Verified for SourceStamp: true
Number of signers: 1
Signer (minSdkVersion=33, maxSdkVersion=2147483647) certificate DN: CN=Android, OU=Android, O=Google Inc., L=Mountain View, ST=California, C=US
Signer (minSdkVersion=33, maxSdkVersion=2147483647) certificate SHA-256 digest: 5aad2bee6db95d17e05a08d7d1e64c10a1511879154483916b6ae6c7fd9cb0c6
Signer (minSdkVersion=33, maxSdkVersion=2147483647) certificate SHA-1 digest: f8456b1d9986acf9ce21fb450b0d32b895f36885
Signer (minSdkVersion=33, maxSdkVersion=2147483647) certificate MD5 digest: 0ea37f3786c8273287600bee47186c32
Signer (minSdkVersion=33, maxSdkVersion=2147483647) key algorithm: RSA
Signer (minSdkVersion=33, maxSdkVersion=2147483647) key size (bits): 4096
Signer (minSdkVersion=33, maxSdkVersion=2147483647) public key SHA-256 digest: 8421d0982672e31240d472608709442945fa174612f5596e7549bbc66c5bf82f
Signer (minSdkVersion=33, maxSdkVersion=2147483647) public key SHA-1 digest: b9dd74abe6d6a269c9b8853d7d09aa4e2e6b20d4
Signer (minSdkVersion=33, maxSdkVersion=2147483647) public key MD5 digest: 5e0e1135419f24c48e2b78e8dcf265dd
Signer (minSdkVersion=24, maxSdkVersion=32) certificate DN: CN=Unknown, OU="Google, Inc", O="Google, Inc", L=Mountain View, ST=CA, C=US
Signer (minSdkVersion=24, maxSdkVersion=32) certificate SHA-256 digest: 3d7a1223019aa39d9ea0e3436ab7c0896bfb4fb679f4de5fe7c23f326c8f994a
Signer (minSdkVersion=24, maxSdkVersion=32) certificate SHA-1 digest: 24bb24c05e47e0aefa68a58a766179d9b613a600
Signer (minSdkVersion=24, maxSdkVersion=32) certificate MD5 digest: d046fc5d1fc3cd0e57c5444097cd5449
Signer (minSdkVersion=24, maxSdkVersion=32) key algorithm: RSA
Signer (minSdkVersion=24, maxSdkVersion=32) key size (bits): 1024
Signer (minSdkVersion=24, maxSdkVersion=32) public key SHA-256 digest: 6c95c299bfaeda37ca92352261d23ae1d35409d97b4678dbf31a6398b5a69c20
Signer (minSdkVersion=24, maxSdkVersion=32) public key SHA-1 digest: e256b17cd660aacd71f077c4e5d8d04a0d104cf7
Signer (minSdkVersion=24, maxSdkVersion=32) public key MD5 digest: 9a95dc52e727ca53ea19bf10c13ff134
Source Stamp Signer certificate DN: CN=Android, OU=Android, O=Google Inc., L=Mountain View, ST=California, C=US
Source Stamp Signer certificate SHA-256 digest: 3257d599a49d2c961a471ca9843f59d341a405884583fc087df4237b733bbd6d
Source Stamp Signer certificate SHA-1 digest: b1af3a0bf998aeede1a8716a539e5a59da1d86d6
Source Stamp Signer certificate MD5 digest: 577b8a9fbc7e308321aec6411169d2fb
Source Stamp Signer key algorithm: RSA
Source Stamp Signer key size (bits): 4096
Source Stamp Signer public key SHA-256 digest: 4c53c1d28f2ecceadcb1351603f0b702615b3454b6e30070de759359f241b802
Source Stamp Signer public key SHA-1 digest: 188b067a9ee881bde55dabe0f8f7ecb320b1a091
Source Stamp Signer public key MD5 digest: 965afac83f033aa037a54482eb6922d5
INFO: SourceStamp: No digests are available in the source stamp for signature scheme: 31
```

Verified schemes: v3 and v3.1; v1/v2/v4 are reported false by this invocation. No external .idsig was supplied; v4=false is not a failed overall signature verification. Two SDK-specific certificate entries are reported for one signer: newer certificate for SDK 33+ and legacy certificate for SDK 24-32. Source-stamp verification is true; apksigner also reports no source-stamp digest for scheme 31. Do not mislabel this as two independent package signers.

The certificate subjects and fingerprints above are observations, not a separately established publisher trust pin. Independent publisher fingerprint/provenance validation remains unresolved. Signature checks ran with Build Tools 35.0.0; device verification behavior on newer Android releases has not been exercised.

## Version validation and recommendation

The [APKPure version-history listing](https://apkpure.net/youtube-app/com.google.android.youtube/versions), consulted 2026-11-03, names 21.44.528 (1561310186), dated October 31, 2026, with Android 10+ and approximately 210.4 MB. Its identity and rounded size agree with this binary. The filename alone was not used for detection. The distributor Latest label does not independently establish stable-channel status. The main listing exposed an older date/size snapshot. No additional binary was downloaded.

Primary recommendation: exact SHA-pinned 21.44.528 for further research only. Stable channel: UNKNOWN. Stable fallback: UNKNOWN, because no fallback binary or device evidence was provided. See [compatibility model](YOUTUBE_VERSION_COMPATIBILITY.md).

## Tools and exact commands

No extra decompiler was installed. Python standard library supplies zipfile/hashlib/zlib/struct; SDK tools supply manifest/resource and signature inspection. Tool versions measured by the analyzer:

### aapt2

```text

```

### apksigner

```text
0.9
```

### java

```text
openjdk version "17.0.20.1" 2026-08-18
OpenJDK Runtime Environment Temurin-17.0.20.1+1 (build 17.0.20.1+1)
OpenJDK 64-Bit Server VM Temurin-17.0.20.1+1 (build 17.0.20.1+1, mixed mode, sharing)
```

### command_line_tools

```text
Pkg.Revision=19.0
Pkg.Path=cmdline-tools;19.0
Pkg.Desc=Android SDK Command-line Tools
```

### python

```text
3.15.1 (tags/v3.15.1:c37e74c, Oct 21 2026, 06:24:08) [MSC v.1951 64 bit (AMD64)]
```

The apkanalyzer adapter uses the Java main class shipped with command-line tools revision 19.0. A nested command-line-tools layout from foundation installation initially prevented apkanalyzer SDK discovery. Copying its bin/lib and metadata into the standard SDK cmdline-tools/latest layout fixed discovery; no application dependency changed.

PowerShell driver (environment setup is documented in BUILD_GUIDE and the phase report):

```powershell
python tools/analyze_apk.py 'main apk/YouTube_21.44.528_APKPure.apk' --output validation-local/youtube-phase2a-final.json --releases patches/releases.json
Get-FileHash -LiteralPath 'main apk/YouTube_21.44.528_APKPure.apk' -Algorithm SHA256
```

The analyzer executed the following exact Windows argument lists (rendered as command lines for reproducibility). Each returned 0. It hashes before/after and streams ZIP/DEX checks in-process; it never invokes a shell.

```text
C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\sdk\build-tools\35.0.0\aapt2.exe version
C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\jdk\jdk-17.0.20.1+1\bin\java.exe -jar C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\sdk\build-tools\35.0.0\lib\apksigner.jar version
C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\jdk\jdk-17.0.20.1+1\bin\java.exe -version
C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\sdk\build-tools\35.0.0\aapt2.exe dump badging "C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk"
C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\sdk\build-tools\35.0.0\aapt2.exe dump xmltree "C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk" --file AndroidManifest.xml
C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\jdk\jdk-17.0.20.1+1\bin\java.exe -Dcom.android.sdklib.toolsdir=C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\sdk\cmdline-tools\latest -cp C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\sdk\cmdline-tools\latest\lib\apkanalyzer-classpath.jar com.android.tools.apk.analyzer.ApkAnalyzerCli manifest print "C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk"
C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\sdk\build-tools\35.0.0\aapt2.exe dump xmltree "C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk" --file res/xml/splits0.xml
C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\jdk\jdk-17.0.20.1+1\bin\java.exe -jar C:\Users\oriyan\AppData\Local\MarufYT-BuildTools\sdk\build-tools\35.0.0\lib\apksigner.jar verify --verbose --print-certs "C:\Users\oriyan\Desktop\ios App\MarufYT-Android\main apk\YouTube_21.44.528_APKPure.apk"
```

The earlier direct confirmation commands used the same Build Tools 35.0.0 aapt2 dump badging/xmltree and apksigner.bat verify --verbose --print-certs invocations. Full local machine output and command arrays remain ignored, with metadata only summarized here.

## Tests, limitations and unresolved issues

The actual analyzer completed successfully with compatibility status RESEARCH_ONLY and patch_supported=false. The source SHA-256 remained unchanged. Synthetic tests and Gradle/workflow results are recorded in [PHASE2A_IMPLEMENTATION_REPORT.md](PHASE2A_IMPLEMENTATION_REPORT.md).

UNKNOWN: official stable rollout status, independently pinned download hash/publisher certificate, fallback release, physical-device installation, runtime network/assets/OBB behavior and any patchable internal API. No JADX/Apktool bytecode decompilation, player-hook discovery, APK rewriting or signing operation was performed. Phase 2B has not begun.
