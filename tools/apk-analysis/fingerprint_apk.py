"""Gated, read-only DEX/resource/manifest/ELF fingerprint study."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from marufyt.analysis import inspect_zip, run_tool, sdk_paths, sha256_file
from marufyt.models import AnalysisError, ANDROID, parse_manifest
from dex_reader import DexError, DexReader


def gate(path, expected, tools, commands):
    """Identity extraction is the only APK inspection allowed before this gate passes."""
    if not path.is_file(): raise AnalysisError('Missing APK')
    digest = sha256_file(path)
    if digest != expected['sha256'].lower(): raise AnalysisError('INTEGRITY_GATE_FAILED: SHA-256 mismatch')
    text = run_tool([tools['java'], '-Dcom.android.sdklib.toolsdir=' + str(tools['command_tools']),
        '-cp', tools['analyzer_jar'], 'com.android.tools.apk.analyzer.ApkAnalyzerCli',
        'manifest', 'print', path], commands)
    identity = parse_manifest(text)['identity']
    if any(identity[key] != expected[key] for key in ('package', 'version_name', 'version_code')):
        raise AnalysisError('IDENTITY_GATE_FAILED: package/version/code mismatch')
    return digest, text, identity


def descriptor(name, package):
    if name.startswith('.'): name = package + name
    elif '.' not in name: name = package + '.' + name
    return 'L' + name.replace('.', '/') + ';'


def manifest_components(text, package):
    root = ET.fromstring(text)
    app = root.find('application')
    result = []
    keep = ('name', 'targetActivity', 'exported', 'enabled', 'permission', 'process', 'foregroundServiceType', 'networkSecurityConfig')
    for element in [app] + list(app):
        if element.tag not in ('application', 'activity', 'activity-alias', 'service', 'receiver', 'provider'): continue
        attributes = {key: element.get(ANDROID + key) for key in keep if element.get(ANDROID + key) is not None}
        if 'name' not in attributes: continue
        filters = [{'actions': [e.get(ANDROID + 'name') for e in f.findall('action')],
                    'categories': [e.get(ANDROID + 'name') for e in f.findall('category')]}
                   for f in element.findall('intent-filter')]
        result.append({'kind': element.tag, 'identifier': attributes['name'],
                       'descriptor': descriptor(attributes['name'], package),
                       'attributes': attributes, 'intent_filters': filters})
    return result


def resources_from_dump(text):
    result = {}
    current = None
    for line in text.splitlines():
        match = re.match(r'\s*resource (0x[0-9a-fA-F]{8}) ([A-Za-z0-9_./]+)', line)
        if match:
            current = {'id': match[1].lower(), 'name': match[2], 'file_paths': []}
            result[current['id']] = current
        elif current:
            file = re.search(r'\(file\) (res/\S+)', line)
            if file and file[1] not in current['file_paths']: current['file_paths'].append(file[1])
    return sorted(result.values(), key=lambda r: r['id'])


def smali_relationships(text, owner, resources):
    """Only explicit invoke instructions and resource consts; no string-based call guesses."""
    current, calls, used, declarations = None, set(), set(), set()
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith('.method '):
            current = owner + '->' + line.split()[-1]
            declarations.add(current)
        elif line == '.end method': current = None
        elif current and line.startswith('invoke-'):
            match = re.search(r',\s*(L[^;]+;->[^\s]+)', line)
            if match: calls.add((current, match[1]))
        elif current and line.startswith('const'):
            for value in re.findall(r'0x7f[0-9a-fA-F]{6}\b', line):
                if value.lower() in resources: used.add((current, value.lower()))
    return sorted(calls), sorted(used), declarations


def elf_metadata(header):
    if len(header) < 64 or header[:4] != b'\x7fELF' or header[5] != 1 or header[4] not in (1, 2):
        return {'elf_class': None, 'machine': None, 'load_alignments': []}
    bits = 64 if header[4] == 2 else 32
    machine = struct.unpack_from('<H', header, 18)[0]
    phoff = struct.unpack_from('<Q' if bits == 64 else '<I', header, 32 if bits == 64 else 28)[0]
    size, count = struct.unpack_from('<HH', header, 54 if bits == 64 else 42)
    aligns = []
    minimum = 56 if bits == 64 else 32
    if size >= minimum and phoff + size * count <= len(header):
        for i in range(count):
            start = phoff + size * i
            if struct.unpack_from('<I', header, start)[0] == 1:
                aligns.append(struct.unpack_from('<Q' if bits == 64 else '<I', header, start + (48 if bits == 64 else 28))[0])
    return {'elf_class': bits, 'machine': machine, 'load_alignments': sorted(set(aligns))}


def study(path, expected, targets, sdk, java_home, evidence):
    tools, commands = sdk_paths(sdk, java_home), []
    before, manifest, identity = gate(path, expected, tools, commands)
    archive_info = inspect_zip(path)
    components = manifest_components(manifest, identity['package'])
    queries = [re.compile(area['class_pattern']) for area in targets['areas']]
    extra = re.compile(targets['extra_class_pattern'])
    selected, index, dex_summaries = [], {}, []
    # Read one DEX at a time, keeping declaration metadata only.
    with zipfile.ZipFile(path) as archive:
        for item in archive_info['dex']:
            name = item['name']
            data = archive.read(name)
            reader = DexReader(data)
            definitions = list(reader.definitions())
            dex_summaries.append({'name': name, 'sha256': hashlib.sha256(data).hexdigest(),
                'class_count': len(definitions), 'method_id_count': reader.methods[0], 'field_id_count': reader.fields[0]})
            for definition in definitions:
                owner = definition['descriptor']
                if owner in index: raise AnalysisError('Ambiguous class definition: ' + owner)
                index[owner] = {'dex': name, **definition}
                if any(query.search(owner) for query in queries) or extra.search(owner):
                    fields, methods = reader.members(definition)
                    selected.append({'descriptor': owner, 'dex': name, 'class_def_index': definition['class_def_index'],
                        'access_flags': definition['access_flags'], 'superclass': definition['superclass'],
                        'interfaces': definition['interfaces'], 'fields': fields, 'methods': methods,
                        'confidence': 'HIGH', 'evidence_kind': 'DEX_DECLARATION', 'selection_reason': 'AREA_QUERY'})
            del reader, data
        ancestors = set()
        frontier = {c['descriptor'] for c in selected}
        for _ in range(targets.get('follow_parent_depth', 0)):
            frontier = {index[name]['superclass'] for name in frontier if name in index and index[name]['superclass'] in index}
            ancestors.update(frontier)
        ancestors -= {c['descriptor'] for c in selected}
        for item in dex_summaries:
            wanted = [index[name] for name in sorted(ancestors) if index[name]['dex'] == item['name']]
            if not wanted: continue
            reader = DexReader(archive.read(item['name']))
            for definition in wanted:
                fields, methods = reader.members(definition)
                selected.append({'descriptor': definition['descriptor'], 'dex': item['name'],
                    'class_def_index': definition['class_def_index'], 'access_flags': definition['access_flags'],
                    'superclass': definition['superclass'], 'interfaces': definition['interfaces'],
                    'fields': fields, 'methods': methods, 'confidence': 'HIGH',
                    'evidence_kind': 'DEX_DECLARATION', 'selection_reason': 'ANCESTOR'})
            del reader
        native = []
        for item in archive_info['native_libraries']:
            with archive.open(item['name']) as stream:
                header = stream.read(65536)
                digest = hashlib.sha256(header)
                while block := stream.read(1048576): digest.update(block)
            native.append({**item, 'sha256': digest.hexdigest(), **elf_metadata(header)})
    resource_text = run_tool([tools['aapt2'], 'dump', 'resources', path], commands)
    # Raw resource values remain in ignored local evidence, never in published inventory.
    evidence.mkdir(parents=True, exist_ok=False)
    (evidence / 'resources.txt').write_text(resource_text, encoding='utf-8')
    all_resources = resources_from_dump(resource_text)
    resource_map = {resource['id']: resource for resource in all_resources}
    patterns = [re.compile(area['resource_pattern']) for area in targets['areas']] + [re.compile(targets['extra_resource_pattern'])]
    selected_resources = {r['id']: r for r in all_resources if any(p.search(r['name']) for p in patterns)}
    relationships, decode_results, failures, confirmed = [], [], [], []
    for component in components:
        component['defined_dex'] = index.get(component['descriptor'], {}).get('dex')
        target = component['attributes'].get('targetActivity')
        if target:
            relationships.append({'source': component['descriptor'], 'target': descriptor(target, identity['package']),
                'kind': 'MANIFEST_ALIAS', 'confidence': 'HIGH', 'evidence': 'AndroidManifest.xml'})
    for cls in selected:
        if cls['superclass']:
            relationships.append({'source': cls['descriptor'], 'target': cls['superclass'], 'kind': 'EXTENDS',
                                  'confidence': 'HIGH', 'evidence': cls['dex'] + ':class_def:' + str(cls['class_def_index'])})
        if not re.search(targets['disassemble_pattern'], cls['descriptor']): continue
        name = cls['descriptor'][1:-1].replace('/', '.')
        # Never use an untrusted DEX identifier as an OS filename.
        local = evidence / (hashlib.sha256(cls['descriptor'].encode()).hexdigest() + '.smali')
        try:
            text = run_tool([tools['java'], '-Dcom.android.sdklib.toolsdir=' + str(tools['command_tools']),
                '-cp', tools['analyzer_jar'], 'com.android.tools.apk.analyzer.ApkAnalyzerCli',
                'dex', 'code', '--class', name, path], commands)
            local.write_text(text, encoding='utf-8')
            calls, used, declarations = smali_relationships(text, cls['descriptor'], resource_map)
            expected_methods = {method['identifier'] for method in cls['methods']}
            if declarations != expected_methods:
                raise AnalysisError('Independent SDK method-declaration cross-check failed for ' + name)
            confirmed.append(cls['descriptor'])
            for source, target in calls:
                relationships.append({'source': source, 'target': target, 'kind': 'INVOKES', 'confidence': 'HIGH',
                                      'evidence': 'apkanalyzer dex code:' + name})
            for source, target in used:
                selected_resources[target] = resource_map[target]
                relationships.append({'source': source, 'target': target, 'kind': 'RESOURCE_LITERAL', 'confidence': 'HIGH',
                    'evidence': 'apkanalyzer dex code:' + name + '; literal presence, not a resolved data-flow edge'})
        except AnalysisError as exc:
            failures.append(str(exc))
    decoded_resources = []
    entries = {e['name'] for e in archive_info['entries']}
    for symbol in targets['decode_resources']:
        matches = [r for r in all_resources if r['name'] == symbol]
        if not matches:
            failures.append('Resource symbol absent: ' + symbol)
            continue
        for resource in matches[0]['file_paths']:
            if resource not in entries:
                failures.append('Resource file absent: ' + resource)
                continue
            text = run_tool([tools['aapt2'], 'dump', 'xmltree', path, '--file', resource], commands)
            filename = resource.replace('/', '_') + '.txt'
            (evidence / filename).write_text(text, encoding='utf-8')
            decoded_resources.append({'name': symbol, 'path': resource,
                                      'xmltree_sha256': hashlib.sha256(text.encode()).hexdigest()})
    areas = []
    for area, query in zip(targets['areas'], queries):
        classes = [c['descriptor'] for c in selected if query.search(c['descriptor'])]
        areas.append({'id': area['id'], 'title': area['title'], 'confidence': area['confidence'],
            'class_identifiers': classes,
            'resource_identifiers': [r['id'] for r in all_resources if re.search(area['resource_pattern'], r['name'])],
            'manifest_identifiers': [c['identifier'] for c in components if c['descriptor'] in classes or descriptor(c['attributes'].get('targetActivity', c['identifier']), identity['package']) in classes],
            'relationship_assessment': 'Declarations and explicit edges are verified; functional ownership is inferred and runtime behavior is unknown.',
            'unknowns': area['unknowns']})
    after = sha256_file(path)
    if after != before: raise AnalysisError('Input changed during read-only study')
    # Command output contains proprietary code/embedded identifiers. Keep raw output local.
    (evidence / 'commands.json').write_text(json.dumps(commands, indent=2), encoding='utf-8')
    return {'schema_version': 1, 'identity': {**identity, 'sha256': before, 'size_bytes': path.stat().st_size},
        'integrity': {'gate_passed': True, 'sha256_before': before, 'sha256_after': after, 'unchanged': True},
        'tooling': {'reader': 'MarufYT DEX 035 metadata reader v1', 'python': sys.version,
                   'aapt2': run_tool([tools['aapt2'], 'version'], []).strip(),
                   'sdk_command_line_tools': (tools['command_tools'] / 'source.properties').read_text().strip()},
        'coverage': {'total_defined_classes': len(index), 'resource_entry_count': len(all_resources),
                     'sdk_cross_checked_classes': confirmed, 'limitations': failures},
        'dex_files': dex_summaries, 'classes': sorted(selected, key=lambda c: c['descriptor']),
        'resources': sorted(selected_resources.values(), key=lambda r: r['id']),
        'manifest_components': components, 'native_libraries': native,
        'decoded_resources': decoded_resources, 'relationships': relationships, 'areas': areas,
        'patch_supported': False,
        'observations': ['No patch/runtime execution. Name-based feature selection is a research heuristic.',
            'Instruction hashes cover instruction bytes only, not try/catch tables or full behavior.',
            'Invoke edges are syntactic references, not proof of runtime dispatch or reachability.',
            'Native metadata and load alignment do not prove device/page-size compatibility.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('apk', type=Path)
    parser.add_argument('--releases', required=True, type=Path)
    parser.add_argument('--target', default='primary', choices=('primary', 'fallback'))
    parser.add_argument('--targets', type=Path, default=Path(__file__).with_name('study_targets.json'))
    parser.add_argument('--sdk', default=os.environ.get('ANDROID_HOME'))
    parser.add_argument('--java-home', default=os.environ.get('JAVA_HOME'))
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--evidence', required=True, type=Path)
    args = parser.parse_args()
    try:
        path, output, evidence = args.apk.resolve(), args.output.resolve(), args.evidence.resolve()
        if output.exists() or evidence.exists() or output.suffix.lower() != '.json':
            raise AnalysisError('Use a new JSON output and a new evidence directory; overwrites are forbidden')
        if path == output or evidence == path or not args.sdk or not args.java_home:
            raise AnalysisError('Invalid source/output or missing SDK/JDK environment')
        expected = json.loads(args.releases.read_text(encoding='utf-8'))[args.target]
        if not expected: raise AnalysisError('No configured release for selected role')
        report = study(path, expected, json.loads(args.targets.read_text(encoding='utf-8')), args.sdk, args.java_home, evidence)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('x', encoding='utf-8') as stream: json.dump(report, stream, indent=2)
        print(json.dumps({'gate': report['integrity'], 'classes': len(report['classes']),
            'relationships': len(report['relationships']), 'limitations': report['coverage']['limitations']}))
        return 0
    except (AnalysisError, DexError, OSError, ValueError, KeyError, struct.error) as exc:
        print('Fingerprint study failed: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())
