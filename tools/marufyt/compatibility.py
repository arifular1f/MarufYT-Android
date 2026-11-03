"""Exact-match release gates and dependency planning, without patch execution."""
from dataclasses import dataclass
import re


class CompatibilityError(ValueError):
    pass


def check_release(identity, sha256, config):
    """A known research input is never reported as patch-supported."""
    if config.get('schema_version', 1) != 1:
        raise CompatibilityError('Unknown release configuration schema')
    for role in ('primary', 'fallback'):
        target = config.get(role)
        if target is None: continue
        if (not isinstance(target, dict) or not all(key in target for key in ('package', 'version_name', 'version_code', 'sha256'))
                or not isinstance(target['sha256'], str) or not re.fullmatch(r'[0-9a-fA-F]{64}', target['sha256'])):
            raise CompatibilityError(f'Invalid {role} release metadata')
        if (identity.package, identity.version_name, identity.version_code, sha256.lower()) == (
                target['package'], target['version_name'], target['version_code'], target['sha256'].lower()):
            return {'role': role, 'status': 'RESEARCH_ONLY', 'patch_supported': False}
    raise CompatibilityError('UNSUPPORTED_INPUT: package/version/code/SHA-256 does not match an approved research input')


@dataclass(frozen=True)
class PatchMetadata:
    patch_id: str
    package: str
    versions: tuple[tuple[str, int], ...]
    dependencies: tuple[str, ...] = ()


class PatchRegistry:
    """Metadata registration and deterministic preflight only. No executor exists."""
    def __init__(self):
        self._patches = {}

    def register(self, patch):
        if not re.fullmatch(r'[a-z][a-z0-9.-]*', patch.patch_id):
            raise CompatibilityError('Invalid patch ID')
        if patch.patch_id in self._patches:
            raise CompatibilityError(f'Duplicate patch ID: {patch.patch_id}')
        if not patch.package or not patch.versions:
            raise CompatibilityError('Patch must specify package and exact version pairs')
        self._patches[patch.patch_id] = patch

    def plan(self, requested, identity):
        ordered, visiting, visited = [], set(), set()
        def visit(patch_id):
            if patch_id in visiting: raise CompatibilityError(f'Dependency cycle at {patch_id}')
            if patch_id in visited: return
            patch = self._patches.get(patch_id)
            if patch is None: raise CompatibilityError(f'Unknown patch/dependency: {patch_id}')
            if patch.package != identity.package or (identity.version_name, identity.version_code) not in patch.versions:
                raise CompatibilityError(f'Unsupported version for patch: {patch_id}')
            visiting.add(patch_id)
            for dependency in patch.dependencies: visit(dependency)
            visiting.remove(patch_id)
            visited.add(patch_id)
            ordered.append(patch_id)
        for patch_id in requested: visit(patch_id)
        return tuple(ordered)
