"""Bounded, read-only ZIP/DEX inspection and SDK tool adapters."""
from collections import Counter
import hashlib
from pathlib import Path, PurePosixPath
import re
import struct
import subprocess
import zipfile
import zlib

from .models import AnalysisError, parse_manifest

CHUNK = 1024 * 1024
MAX_UNCOMPRESSED = 2 * 1024**3
MAX_ENTRY = 512 * 1024**2
MAX_ENTRIES = 100000


def sha256_file(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def inspect_zip(path):
    """Never extract or execute entries. CRC-check streams after enforcing size limits."""
    try:
        with zipfile.ZipFile(path) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_ENTRIES or sum(e.file_size for e in entries) > MAX_UNCOMPRESSED:
                raise AnalysisError('ZIP exceeds analysis limits')
            seen = set()
            for entry in entries:
                # ZipInfo.filename normalizes backslashes on Windows and truncates NULs.
                name = entry.orig_filename
                parts = PurePosixPath(name).parts
                if (name in seen or '\\' in name or '\x00' in name or ':' in name or name.startswith('/')
                        or '..' in parts or entry.file_size > MAX_ENTRY or entry.flag_bits & 1
                        or ((entry.external_attr >> 16) & 0o170000) == 0o120000):
                    raise AnalysisError(f'Unsafe, duplicate, encrypted or oversized ZIP entry: {name}')
                seen.add(name)
            if 'AndroidManifest.xml' not in seen:
                raise AnalysisError('Not a direct APK: root AndroidManifest.xml missing (container/split archive?)')
            inventory, dex = [], []
            for entry in entries:
                item = {'name': entry.filename, 'size': entry.file_size,
                        'compressed_size': entry.compress_size, 'crc32': f'{entry.CRC:08x}'}
                inventory.append(item)
                is_dex = bool(re.fullmatch(r'classes(?:[2-9]|[1-9][0-9]+)?\.dex', entry.filename))
                digest, checksum, header, count = hashlib.sha1(), 1, b'', 0
                with archive.open(entry) as stream:
                    while block := stream.read(CHUNK):
                        if is_dex:
                            if count == 0: header = block[:112]
                            if count + len(block) > 32: digest.update(block[max(0, 32 - count):])
                            if count + len(block) > 12: checksum = zlib.adler32(block[max(0, 12 - count):], checksum)
                        count += len(block)
                        if count > entry.file_size or count > MAX_ENTRY:
                            raise AnalysisError('ZIP stream exceeds declared size or limit')
                if is_dex:
                    valid = (len(header) >= 112 and bool(re.fullmatch(b'dex\n[0-9]{3}\x00', header[:8]))
                             and struct.unpack_from('<I', header, 32)[0] == count
                             and struct.unpack_from('<I', header, 36)[0] == 112
                             and struct.unpack_from('<I', header, 40)[0] == 0x12345678
                             and struct.unpack_from('<I', header, 8)[0] == checksum & 0xffffffff
                             and header[12:32] == digest.digest())
                    dex.append({**item, 'header_and_checksums_valid': valid,
                                'dex_version': header[4:7].decode('ascii', errors='replace')})
            if not dex or not all(e['header_and_checksums_valid'] for e in dex):
                raise AnalysisError('No supported root DEX files, or DEX header/checksum failure')
            libs = [e for e in inventory if re.fullmatch(r'lib/[^/]+/[^/]+\.so', e['name'])]
            abis = sorted({e['name'].split('/')[1] for e in libs})
            return {'crc_valid': True, 'entry_count': len(entries),
                    'uncompressed_bytes': sum(e.file_size for e in entries),
                    'dex': dex, 'abis': abis, 'native_libraries': libs,
                    'resource_count': sum(e['name'].startswith('res/') for e in inventory),
                    'asset_count': sum(e['name'].startswith('assets/') for e in inventory),
                    'top_level_counts': dict(sorted(Counter(e['name'].split('/')[0] for e in inventory).items())),
                    'entries': inventory}
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, OSError, EOFError) as exc:
        raise AnalysisError(f'APK ZIP validation failed: {exc}') from exc


def run_tool(command, records):
    """Argument arrays, no shell; callers provide trusted SDK executables."""
    try:
        result = subprocess.run([str(arg) for arg in command], capture_output=True,
                                text=True, encoding='utf-8', errors='replace', timeout=180, shell=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise AnalysisError(f'Tool unavailable or timed out: {command[0]}: {exc}') from exc
    records.append({'argv': [str(arg) for arg in command], 'exit_code': result.returncode,
                    'stdout': result.stdout, 'stderr': result.stderr})
    if result.returncode:
        raise AnalysisError(f'Tool failed ({result.returncode}): {command[0]}: {result.stderr[-1500:]}')
    return result.stdout


def sdk_paths(sdk, java_home):
    sdk, java_home = Path(sdk).resolve(), Path(java_home).resolve()
    suffix = '.exe' if __import__('os').name == 'nt' else ''
    command_tools = sdk / 'cmdline-tools/latest'
    return {'aapt2': sdk / ('build-tools/35.0.0/aapt2' + suffix),
            'java': java_home / ('bin/java' + suffix),
            'apksigner_jar': sdk / 'build-tools/35.0.0/lib/apksigner.jar',
            'analyzer_jar': command_tools / 'lib/apkanalyzer-classpath.jar',
            'command_tools': command_tools}


def analyze(path, sdk, java_home):
    path = Path(path).resolve(strict=True)
    before = sha256_file(path)
    records = []
    report = {'schema_version': 1, 'path': str(path), 'size_bytes': path.stat().st_size,
              'sha256': before, 'commands': records}
    report['zip'] = inspect_zip(path)
    tools = sdk_paths(sdk, java_home)
    java = tools['java']
    for name, location in tools.items():
        if not location.exists(): raise AnalysisError(f'Missing SDK/JDK component {name}: {location}')
    report['tool_versions'] = {
        'aapt2': run_tool([tools['aapt2'], 'version'], records).strip(),
        'apksigner': run_tool([java, '-jar', tools['apksigner_jar'], 'version'], records).strip(),
        'java': run_tool([java, '-version'], records).strip() or records[-1]['stderr'].strip(),
        'command_line_tools': (tools['command_tools'] / 'source.properties').read_text().strip(),
        'python': __import__('sys').version,
    }
    report['badging'] = run_tool([tools['aapt2'], 'dump', 'badging', path], records)
    label = re.search(r"^application-label:'(.*)'$", report['badging'], re.MULTILINE)
    report['application_label'] = label.group(1) if label else None
    report['xmltree'] = run_tool([tools['aapt2'], 'dump', 'xmltree', path, '--file', 'AndroidManifest.xml'], records)
    decoded = run_tool([java, '-Dcom.android.sdklib.toolsdir=' + str(tools['command_tools']),
        '-cp', tools['analyzer_jar'], 'com.android.tools.apk.analyzer.ApkAnalyzerCli',
        'manifest', 'print', path], records)
    report['manifest'] = parse_manifest(decoded)
    split_resources = [entry['name'] for entry in report['zip']['entries']
                       if re.fullmatch(r'res/xml/splits[^/]*\.xml', entry['name'])]
    if len(split_resources) > 32:
        raise AnalysisError('Too many split metadata resources')
    report['split_resource_trees'] = {name: run_tool(
        [tools['aapt2'], 'dump', 'xmltree', path, '--file', name], records) for name in split_resources}
    report['signature_output'] = run_tool([java, '-jar', tools['apksigner_jar'],
                                         'verify', '--verbose', '--print-certs', path], records)
    report['signature_verified'] = True
    after = sha256_file(path)
    report['unchanged'] = before == after
    if not report['unchanged']: raise AnalysisError('Input changed during analysis')
    return report
