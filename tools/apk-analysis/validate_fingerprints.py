"""Validate JSON Schema plus cross-record integrity, without opening any APK."""
import argparse
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator


def validate_inventory(inventory, schema):
    Draft202012Validator.check_schema(schema)
    errors = [str(error.message) for error in Draft202012Validator(schema).iter_errors(inventory)]
    if errors: return errors
    for key in ('classes', 'resources', 'manifest_components', 'dex_files', 'areas'):
        field = {'classes': 'descriptor', 'resources': 'id', 'manifest_components': 'identifier',
                 'dex_files': 'name', 'areas': 'id'}[key]
        names = [item[field] for item in inventory[key]]
        if len(names) != len(set(names)): errors.append('Duplicate ' + key + ' identifiers')
    identity = inventory['identity']
    if not identity['package'] or not identity['version_name']:
        errors.append('Identity must include package and version')
    if not identity['sha256'] == inventory['integrity']['sha256_before'] == inventory['integrity']['sha256_after']:
        errors.append('Input integrity hashes disagree')
    classes = {c['descriptor'] for c in inventory['classes']}
    methods = {m['identifier'] for c in inventory['classes'] for m in c['methods']}
    resources = {r['id'] for r in inventory['resources']}
    components = {c['identifier'] for c in inventory['manifest_components']}
    component_descriptors = {c['descriptor'] for c in inventory['manifest_components']}
    dex = {d['name'] for d in inventory['dex_files']}
    if sum(d['class_count'] for d in inventory['dex_files']) != inventory['coverage']['total_defined_classes']:
        errors.append('DEX aggregate class count disagrees')
    for c in inventory['classes']:
        if c['dex'] not in dex: errors.append('Unresolved class DEX: ' + c['descriptor'])
        identifiers = [m['identifier'] for m in c['methods']] + [f['identifier'] for f in c['fields']]
        if len(identifiers) != len(set(identifiers)): errors.append('Duplicate class members')
        if any(not identifier.startswith(c['descriptor'] + '->') for identifier in identifiers):
            errors.append('Class member owner mismatch')
        for method in c['methods']:
            if bool(method['code_offset']) != (method['instruction_sha256'] is not None):
                errors.append('Method body/hash presence disagrees')
    for c in inventory['coverage']['sdk_cross_checked_classes']:
        if c not in classes: errors.append('Unresolved cross-checked class')
    for area in inventory['areas']:
        if not set(area['class_identifiers']) <= classes: errors.append('Unresolved area class')
        if not set(area['resource_identifiers']) <= resources: errors.append('Unresolved area resource')
        if not set(area['manifest_identifiers']) <= components: errors.append('Unresolved area component')
    for relation in inventory['relationships']:
        kind = relation['kind']
        if kind in ('INVOKES', 'RESOURCE_LITERAL') and relation['source'] not in methods:
            errors.append('Unresolved relationship method source')
        if kind in ('EXTENDS', 'IMPLEMENTS') and relation['source'] not in classes:
            errors.append('Unresolved relationship class source')
        if kind == 'MANIFEST_ALIAS' and relation['source'] not in component_descriptors:
            errors.append('Unresolved alias source')
        if kind == 'RESOURCE_LITERAL' and relation['target'] not in resources:
            errors.append('Unresolved resource literal')
    return sorted(set(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inventory', type=Path)
    parser.add_argument('--schema', type=Path, default=Path(__file__).resolve().parents[2] / 'Documentation/FINGERPRINT_SCHEMA.json')
    args = parser.parse_args()
    try:
        errors = validate_inventory(json.loads(args.inventory.read_text(encoding='utf-8')),
                                    json.loads(args.schema.read_text(encoding='utf-8')))
        if errors: raise ValueError('\n'.join(errors))
        print('Fingerprint schema and cross-record validation: PASS')
        return 0
    except (OSError, ValueError) as exc:
        print('Fingerprint validation failed: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())
