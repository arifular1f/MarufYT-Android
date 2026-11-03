import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from prepare_release import build,source_files

class ReleaseTests(unittest.TestCase):
    def fixture(self,root):
        subprocess.run(['git','init',str(root)],check=True,capture_output=True)
        (root/'release.json').write_text(json.dumps({'version':'0.2.0-preview.1','tag':'v0.2.0-preview.1','prerelease':True,'patch_supported':False}))
        (root/'README.md').write_text('Synthetic source fixture\n')
    def test_deterministic_source_archive_and_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'repository';root.mkdir();self.fixture(root)
            with contextlib.redirect_stdout(io.StringIO()):
                first=build(Path(directory)/'one',root=root);second=build(Path(directory)/'two',root=root)
            self.assertEqual(first.read_bytes(),second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                manifest=json.loads(archive.read('SOURCE_MANIFEST.json'))
                self.assertEqual(set(manifest),{'README.md','release.json'})
    def test_forced_proprietary_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.fixture(root)
            (root/'app').mkdir();(root/'app/private.apk').write_bytes(b'synthetic fixture')
            with self.assertRaises(ValueError):source_files(root)
    def test_release_requires_exact_tag_and_preview(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'repository';root.mkdir();self.fixture(root)
            with self.assertRaises(ValueError):build(Path(directory)/'out','v99',root)
