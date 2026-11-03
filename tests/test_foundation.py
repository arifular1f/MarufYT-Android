import importlib.util
from pathlib import Path
import tempfile
import unittest
import subprocess

spec = importlib.util.spec_from_file_location('foundation', Path(__file__).resolve().parents[1] / 'tools/validate_foundation.py')
foundation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foundation)

class FoundationTests(unittest.TestCase):
    def test_repository_policy(self):
        self.assertEqual([], foundation.validate())

    def test_rejects_secret_and_key(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'credential.txt').write_text('gh' + 'p_' + 'x' * 36)
            (root / 'release.jks').write_bytes(b'fixture')
            errors = foundation.validate(root)
            self.assertTrue(any('Possible secret' in e for e in errors))
            self.assertTrue(any('Forbidden asset' in e for e in errors))

    def test_missing_structure(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = foundation.validate(Path(directory))
            self.assertEqual(len(foundation.REQUIRED), len(errors))

    def test_local_input_allowed_but_signing_keys_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inputs = root / 'main apk'
            inputs.mkdir()
            (inputs / 'fixture.apk').write_bytes(b'synthetic fixture')
            (inputs / 'private.jks').write_bytes(b'synthetic fixture')
            errors = foundation.validate(root)
            self.assertFalse(any('fixture.apk' in error for error in errors))
            self.assertTrue(any('Forbidden asset: main apk' in error for error in errors))

    def test_tracked_local_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', str(root)], check=True, capture_output=True)
            inputs = root / 'main apk'
            inputs.mkdir()
            (inputs / 'fixture.apk').write_bytes(b'synthetic fixture')
            subprocess.run(['git', '-C', str(root), 'add', 'main apk'], check=True, capture_output=True)
            self.assertTrue(any('must never contain tracked' in error for error in foundation.validate(root)))
