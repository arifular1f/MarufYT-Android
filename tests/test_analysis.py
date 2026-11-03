"""Synthetic APK fixtures only; CI never requires the proprietary local input."""
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from marufyt.analysis import inspect_zip, sha256_file
from marufyt.compatibility import CompatibilityError, PatchMetadata, PatchRegistry, check_release
from marufyt.models import AnalysisError, ApkIdentity, parse_manifest

XML = '''<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="com.google.android.youtube" android:versionName="21.44.528" android:versionCode="1561310186"
android:compileSdkVersion="37" android:compileSdkVersionCodename="DEV">
<uses-sdk android:minSdkVersion="29" android:targetSdkVersion="37"/>
<uses-permission android:name="android.permission.INTERNET"/>
<uses-feature android:name="android.hardware.camera" android:required="false"/>
<application><meta-data android:name="com.android.vending.splits" android:resource="@xml/splits0"/></application>
</manifest>'''


def dex_bytes():
    data = bytearray(112)
    data[:8] = b'dex\n035\0'
    struct.pack_into('<III', data, 32, len(data), 112, 0x12345678)
    data[12:32] = hashlib.sha1(data[32:]).digest()
    struct.pack_into('<I', data, 8, zlib.adler32(data[12:]))
    return data


def fixture(path, extra=None):
    with zipfile.ZipFile(path, 'w') as archive:
        archive.writestr('AndroidManifest.xml', b'synthetic binary manifest placeholder')
        archive.writestr('classes.dex', dex_bytes())
        archive.writestr('lib/arm64-v8a/libtest.so', b'synthetic library placeholder')
        for name, data in (extra or {}).items(): archive.writestr(name, data)


class ManifestTests(unittest.TestCase):
    def test_identity_and_metadata(self):
        report = parse_manifest(XML)
        self.assertEqual(report['identity']['version_name'], '21.44.528')
        self.assertEqual(report['identity']['version_code'], 1561310186)
        self.assertEqual(report['identity']['min_sdk'], '29')
        self.assertEqual(report['identity']['compile_codename'], 'DEV')
        self.assertEqual(len(report['permissions']), 1)
        self.assertEqual(len(report['declared_features']), 1)
        self.assertEqual(len(report['split_indicators']['application_metadata']), 1)

    def test_unknown_values_remain_unknown(self):
        report = parse_manifest('<manifest/>')
        self.assertTrue(all(value is None for value in report['identity'].values()))

    def test_version_code_major(self):
        report = parse_manifest(XML.replace('android:versionCode="1561310186"', 'android:versionCode="7" android:versionCodeMajor="2"'))
        self.assertEqual(report['identity']['version_code'], (2 << 32) | 7)

    def test_reject_malformed_xml_and_entities(self):
        for text in ('not XML', '<other/>', '<!DOCTYPE manifest><manifest/>', XML.replace('1561310186', '-1')):
            with self.subTest(text=text), self.assertRaises(AnalysisError): parse_manifest(text)


class ArchiveTests(unittest.TestCase):
    def test_read_only_inventory_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix='MarufYT path with spaces ') as directory:
            path = Path(directory) / 'input file.apk'
            fixture(path, {'classes2.dex': dex_bytes(), 'res/test.xml': b'fixture', 'assets/test': b'fixture'})
            before = sha256_file(path)
            report = inspect_zip(path)
            self.assertTrue(report['crc_valid'])
            self.assertEqual(report['abis'], ['arm64-v8a'])
            self.assertEqual(len(report['dex']), 2)
            self.assertEqual(report['asset_count'], 1)
            self.assertEqual(before, sha256_file(path))

    def test_reject_unsafe_zip_paths(self):
        for name in ('../outside', '/absolute', 'C:/absolute', 'lib\\unsafe'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'input.apk'
                fixture(path, {name: b'fixture'})
                # Windows ZipInfo normalizes backslashes when writing fixtures.
                if name == 'lib\\unsafe':
                    path.write_bytes(path.read_bytes().replace(b'lib/unsafe', b'lib\\unsafe'))
                with self.assertRaises(AnalysisError): inspect_zip(path)

    def test_reject_invalid_dex(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.apk'
            fixture(path, {'classes2.dex': b'invalid'})
            with self.assertRaises(AnalysisError): inspect_zip(path)

    def test_reject_containers_and_non_zip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.apk'
            path.write_bytes(b'not zip')
            with self.assertRaises(AnalysisError): inspect_zip(path)
            with zipfile.ZipFile(path, 'w') as archive: archive.writestr('base.apk', b'fixture')
            with self.assertRaises(AnalysisError): inspect_zip(path)

    def test_enforce_size_limits(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.apk'
            fixture(path)
            with patch('marufyt.analysis.MAX_ENTRY', 1), self.assertRaises(AnalysisError): inspect_zip(path)

    def test_crc_corruption(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.apk'
            fixture(path)
            raw = path.read_bytes().replace(b'synthetic library placeholder', b'corrupted library placeholder')
            path.write_bytes(raw)
            with self.assertRaises(AnalysisError): inspect_zip(path)

    def test_cli_refuses_to_overwrite_input(self):
        with tempfile.TemporaryDirectory(prefix='CLI spaces ') as directory:
            path = Path(directory) / 'input.apk'
            fixture(path)
            before = sha256_file(path)
            script = Path(__file__).resolve().parents[1] / 'tools/analyze_apk.py'
            result = subprocess.run([sys.executable, str(script), str(path), '--output', str(path),
                                     '--sdk', directory, '--java-home', directory], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('distinct from the APK', result.stderr)
            self.assertEqual(before, sha256_file(path))


class CompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.identity = ApkIdentity(**parse_manifest(XML)['identity'])
        self.target = {'package': self.identity.package, 'version_name': self.identity.version_name,
                       'version_code': self.identity.version_code, 'sha256': 'a' * 64}

    def test_primary_and_fallback_never_claim_patch_support(self):
        for role in ('primary', 'fallback'):
            result = check_release(self.identity, 'a' * 64, {role: self.target})
            self.assertEqual(result['role'], role)
            self.assertEqual(result['status'], 'RESEARCH_ONLY')
            self.assertFalse(result['patch_supported'])

    def test_reject_wrong_package_version_code_and_hash(self):
        for field, value in (('package', 'other'), ('version_name', '21.44.529'), ('version_code', 1), ('sha256', 'b' * 64)):
            target = {**self.target, field: value}
            with self.subTest(field=field), self.assertRaises(CompatibilityError):
                check_release(self.identity, 'a' * 64, {'primary': target})

    def test_dependency_order_and_deduplication(self):
        registry = PatchRegistry()
        registry.register(PatchMetadata('test.base', self.identity.package, (('21.44.528', 1561310186),)))
        registry.register(PatchMetadata('test.child', self.identity.package, (('21.44.528', 1561310186),), ('test.base',)))
        self.assertEqual(registry.plan(['test.child', 'test.base'], self.identity), ('test.base', 'test.child'))

    def test_reject_duplicate_missing_cycle_and_unsupported(self):
        patch_data = PatchMetadata('test.only', self.identity.package, (('21.44.528', 1561310186),))
        registry = PatchRegistry()
        registry.register(patch_data)
        with self.assertRaises(CompatibilityError): registry.register(patch_data)
        with self.assertRaises(CompatibilityError): registry.plan(['missing'], self.identity)
        registry.register(PatchMetadata('test.cycle', self.identity.package, patch_data.versions, ('test.cycle',)))
        with self.assertRaises(CompatibilityError): registry.plan(['test.cycle'], self.identity)
        registry.register(PatchMetadata('test.future', self.identity.package, (('99', 99),)))
        with self.assertRaises(CompatibilityError): registry.plan(['test.future'], self.identity)

    def test_empty_registry(self):
        self.assertEqual(PatchRegistry().plan([], self.identity), ())
        with self.assertRaises(CompatibilityError): PatchRegistry().plan(['background'], self.identity)

    def test_reject_invalid_release_config(self):
        for config in ({'schema_version': 99}, {'primary': {}}, {'primary': {**self.target, 'sha256': 'bad'}}):
            with self.subTest(config=config), self.assertRaises(CompatibilityError):
                check_release(self.identity, 'a' * 64, config)
