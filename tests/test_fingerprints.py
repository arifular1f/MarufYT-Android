import copy
import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/apk-analysis'))
from dex_reader import DexError, DexReader
from fingerprint_apk import gate, resources_from_dump, smali_relationships, elf_metadata
from marufyt.models import AnalysisError
from validate_fingerprints import validate_inventory


def uleb(value):
    result = bytearray()
    while value > 127:
        result.append((value & 127) | 128)
        value >>= 7
    result.append(value)
    return result


def synthetic_dex():
    """A small generated class with a field, method and return-void code item."""
    data = bytearray(204)
    data[:8] = b'dex\n035\0'
    strings = ['Ltest/Fixture;', 'V', 'run', 'I', 'number']
    for i, text in enumerate(strings):
        struct.pack_into('<I', data, 112 + 4 * i, len(data))
        data.extend(uleb(len(text)) + text.encode() + b'\0')
    struct.pack_into('<III', data, 132, 0, 1, 3)
    struct.pack_into('<III', data, 144, 1, 1, 0)
    struct.pack_into('<HHI', data, 156, 0, 2, 4)
    struct.pack_into('<HHI', data, 164, 0, 0, 2)
    class_data = len(data)
    code = (class_data + 10 + 3) & ~3
    data.extend(bytes([0, 1, 1, 0, 0, 1, 0, 1]) + uleb(code))
    data.extend(b'\0' * (code - len(data)))
    data.extend(struct.pack('<HHHHIIH', 1, 1, 0, 0, 0, 1, 0x000e))
    struct.pack_into('<IIIIIIII', data, 172, 0, 1, 0xffffffff, 0, 0xffffffff, 0, class_data, 0)
    struct.pack_into('<III', data, 32, len(data), 112, 0x12345678)
    for at, count, offset in ((56, 5, 112), (64, 3, 132), (72, 1, 144), (80, 1, 156), (88, 1, 164), (96, 1, 172)):
        struct.pack_into('<II', data, at, count, offset)
    return bytes(data)


class DexMetadataTests(unittest.TestCase):
    def test_declared_members_and_instruction_hash(self):
        reader = DexReader(synthetic_dex())
        cls = list(reader.definitions())[0]
        fields, methods = reader.members(cls)
        self.assertEqual(cls['descriptor'], 'Ltest/Fixture;')
        self.assertEqual(fields[0]['identifier'], 'Ltest/Fixture;->number:I')
        self.assertEqual(methods[0]['identifier'], 'Ltest/Fixture;->run()V')
        self.assertEqual(methods[0]['instruction_sha256'], hashlib.sha256(b'\x0e\0').hexdigest())

    def test_reject_truncated_and_invalid_headers(self):
        for data in (b'bad', synthetic_dex()[:-1], b'dex\n039\0' + synthetic_dex()[8:]):
            with self.subTest(size=len(data)), self.assertRaises(DexError): DexReader(data)

    def test_reject_out_of_bounds_table(self):
        data = bytearray(synthetic_dex())
        struct.pack_into('<I', data, 60, len(data) + 1)
        with self.assertRaises(DexError): DexReader(data)

    def test_reject_bad_indices_and_uleb_overflow(self):
        reader = DexReader(synthetic_dex())
        with self.assertRaises(DexError): reader.method_id(999)
        reader.data += b'\xff' * 5
        with self.assertRaises(DexError): reader.uleb(len(reader.data) - 5)

    def test_reject_string_length_mismatch(self):
        data = bytearray(synthetic_dex())
        data[struct.unpack_from('<I', data, 112)[0]] = 1
        with self.assertRaises(DexError): list(DexReader(data).definitions())


class StudyBoundaryTests(unittest.TestCase):
    def test_hash_failure_never_invokes_sdk_or_analysis(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input with spaces.apk'
            path.write_bytes(b'synthetic input')
            with patch('fingerprint_apk.run_tool') as tool, self.assertRaises(AnalysisError):
                gate(path, {'sha256': '0' * 64}, {}, [])
            tool.assert_not_called()

    def test_identity_failure_after_correct_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.apk'
            path.write_bytes(b'synthetic input')
            expected = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'package': 'expected', 'version_name': '1', 'version_code': 1}
            tools = dict.fromkeys(('java', 'command_tools', 'analyzer_jar'), Path(directory))
            with patch('fingerprint_apk.run_tool', return_value='<manifest package="other"/>'), self.assertRaises(AnalysisError):
                gate(path, expected, tools, [])

    def test_resource_symbol_to_obfuscated_file(self):
        text = 'resource 0x7f180001 xml/prefs\n () (file) res/Abc.xml type=XML\n'
        self.assertEqual(resources_from_dump(text)[0]['file_paths'], ['res/Abc.xml'])

    def test_only_explicit_instruction_edges(self):
        text = '.method public run()V\n const-string v0, "Lfake;->call()V"\n invoke-static {}, Ltest/Other;->call()V\n const v0, 0x7f010001\n.end method'
        calls, resources, declarations = smali_relationships(text, 'Ltest/Fixture;', {'0x7f010001': {}})
        self.assertEqual(calls, [('Ltest/Fixture;->run()V', 'Ltest/Other;->call()V')])
        self.assertEqual(resources, [('Ltest/Fixture;->run()V', '0x7f010001')])
        self.assertEqual(declarations, {'Ltest/Fixture;->run()V'})

    def test_elf_header_and_unknown(self):
        data = bytearray(64)
        data[:6] = b'\x7fELF\x02\x01'
        struct.pack_into('<H', data, 18, 183)
        self.assertEqual(elf_metadata(data)['machine'], 183)
        self.assertIsNone(elf_metadata(b'not ELF')['elf_class'])


class InventoryValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / 'Documentation/FINGERPRINT_SCHEMA.json').read_text())
        cls.inventory = json.loads((ROOT / 'Documentation/PHASE2B_FINGERPRINT_INVENTORY.json').read_text())

    def test_published_inventory(self):
        self.assertEqual(validate_inventory(self.inventory, self.schema), [])

    def test_reject_false_patch_claim_and_bad_hash(self):
        data = copy.deepcopy(self.inventory)
        data['patch_supported'] = True
        self.assertTrue(validate_inventory(data, self.schema))
        data['patch_supported'] = False
        data['integrity']['sha256_after'] = '0' * 64
        self.assertTrue(validate_inventory(data, self.schema))

    def test_reject_unresolved_feature_reference(self):
        data = copy.deepcopy(self.inventory)
        data['areas'][0]['class_identifiers'].append('Ldoes/not/Exist;')
        self.assertIn('Unresolved area class', validate_inventory(data, self.schema))
