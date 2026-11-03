"""Structure and limited accidental-secret checks; no third-party dependencies."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['README.md', 'settings.gradle', 'build.gradle', 'app/build.gradle',
    'app/src/main/AndroidManifest.xml', 'app/ui-settings/README.md',
    'tools/apk-analysis/build.gradle', 'tools/apk-validation-signing/build.gradle',
    'patches/patch-management/build.gradle', 'integrations/sponsorblock/build.gradle',
    'integrations/player-customization/build.gradle', 'integrations/privacy-diagnostics/build.gradle',
    'Documentation/ARCHITECTURE.md', 'Documentation/BUILD_GUIDE.md',
    'Documentation/ROADMAP.md', 'Documentation/SECURITY.md',
    'gradlew', 'gradlew.bat', 'gradle/wrapper/gradle-wrapper.jar',
    'gradle/wrapper/gradle-wrapper.properties', '.github/workflows/android.yml']
REQUIRED += ['tools/analyze_apk.py', 'tools/marufyt/models.py', 'tools/marufyt/analysis.py',
    'tools/marufyt/compatibility.py', 'patches/releases.json', 'tests/test_analysis.py',
    'Documentation/YOUTUBE_APK_FORENSIC_REPORT.md', 'Documentation/YOUTUBE_VERSION_COMPATIBILITY.md',
    'Documentation/ANDROID_PATCH_ARCHITECTURE.md', 'Documentation/IOS_TO_ANDROID_FEATURE_MAPPING.md',
    'Documentation/PHASE2A_IMPLEMENTATION_REPORT.md']
REQUIRED += ['tools/apk-analysis/dex_reader.py', 'tools/apk-analysis/fingerprint_apk.py',
    'tools/apk-analysis/validate_fingerprints.py', 'tools/apk-analysis/study_targets.json',
    'tests/test_fingerprints.py', 'tests/requirements.txt',
    'Documentation/PHASE2B_FINGERPRINT_REPORT.md', 'Documentation/PHASE2B_FEATURE_MAPPING.md',
    'Documentation/PHASE2B_PATCH_COMPATIBILITY.md', 'Documentation/FINGERPRINT_SCHEMA.json',
    'Documentation/PHASE2B_FINGERPRINT_INVENTORY.json', 'Documentation/PHASE2B_IMPLEMENTATION_REPORT.md']
REQUIRED += ['release.json','LICENSE_STATUS.md','THIRD_PARTY_NOTICES.md','SECURITY.md','CONTRIBUTING.md','CHANGELOG.md',
    'tools/prepare_release.py','tools/audit_release.py','tools/validate_input.py','tools/sponsorblock_lookup.py',
    'tools/marufyt/sponsorblock.py','tools/marufyt/semantics.py','tests/test_sponsorblock.py','tests/test_semantics.py','tests/test_release.py',
    'Documentation/MARUFYT_ANDROID_FINAL_RELEASE_REPORT.md','Documentation/SEMANTIC_VALIDATION.md','Documentation/PHASE2C_SEMANTIC_VALIDATION_REPORT.md',
    'Documentation/DEVICE_TEST_CHECKLIST.md','Documentation/INSTALLATION.md','Documentation/RELEASE_GUIDE.md',
    'Documentation/RELEASE_NOTES.md','.github/workflows/release.yml']

def validate(root=ROOT):
    errors = [f'Missing file: {name}' for name in REQUIRED if not (root / name).is_file()]
    if (root / '.git').exists():
        tracked = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--', 'main apk'],
                                 capture_output=True, check=True).stdout
        if tracked:
            errors.append('Local APK input directory must never contain tracked files')
    patterns = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                r'gh[pousr]_[A-Za-z0-9]{30,}', r'AKIA[0-9A-Z]{16}']
    for path in root.rglob('*'):
        if not path.is_file(): continue
        if path.relative_to(root).parts[0] == 'dist': continue
        if set(path.relative_to(root).parts) & {'.git', '.gradle', 'build', '__pycache__', 'validation-local'}: continue
        if path.name == 'local.properties': continue
        # User-supplied local binaries are allowed only in the dedicated ignored input directory.
        if path.suffix.lower() in {'.apk', '.apks', '.xapk', '.obb'} and path.relative_to(root).parts[0] == 'main apk':
            continue
        if path.suffix.lower() in {'.jks', '.keystore', '.pem', '.p12', '.apk', '.aab', '.apks', '.xapk', '.obb'}:
            errors.append(f'Forbidden asset: {path.relative_to(root)}')
            continue
        if path.suffix == '.jar': continue
        data = path.read_text(encoding='utf-8', errors='replace')
        if any(re.search(pattern, data) for pattern in patterns):
            errors.append(f'Possible secret: {path.relative_to(root)}')
    return errors

if __name__ == '__main__':
    errors = validate()
    if errors: raise SystemExit('\n'.join(errors))
    print('Foundation structure and secret guard: PASS')
