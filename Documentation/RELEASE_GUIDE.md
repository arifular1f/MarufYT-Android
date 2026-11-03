# Release guide

Version/tag: release.json (`0.2.0-preview.1`, `v0.2.0-preview.1`). Always mark this version prerelease. Source/tooling/documentation are the only GitHub release payloads; do not upload YouTube inputs, raw disassembly, keys or the companion APK as a release asset.

Run the complete tests, debug build/lint, signature checks and secret guard. Inspect `git diff --cached --stat` and `git diff --cached --name-only` before commit. The original-code license is pending; do not label this an open-source licensed/stable product until resolved.

```powershell
python tools/prepare_release.py --output dist/review --tag v0.2.0-preview.1
python tools/audit_release.py dist/review/MarufYT-Android-0.2.0-preview.1-source.zip
Get-Content dist/review/SHA256SUMS.txt
```

The archive uses a reviewed allowlist, fixed ZIP timestamps and per-file SHA-256 manifest. A second run under the same toolchain must produce the same archive. Compression library versions can affect compressed bytes across environments; compare each published asset with its accompanying checksums. The adjacent release report records source commit where available; the Git tag is authoritative for source provenance. Checksums cannot be embedded recursively into the source file that defines their own archive.

The Android workflow validates/test/lints/builds and verifies the project-owned debug APK. The tag-triggered release workflow waits for those checks, packages/audits source and publishes a prerelease using GitHub's short-lived token. No signing secret is configured or required. Read-only token permissions apply except the release job's contents:write.

For manual publication after a clean reviewed commit and successful CI (never force-push):

```powershell
gh repo create arifular1f/MarufYT-Android --public --source . --remote origin
git push -u origin main
git tag -a v0.2.0-preview.1 -m "Developer preview: source and tooling only"
git push origin v0.2.0-preview.1
```

Do not rerun repository creation or overwrite an existing tag/release. Inspect remote history first. If credentials/permissions are missing, leave the artifacts local and ask the repository owner to execute the remaining commands. Repository visibility, tags, release assets and workflow run IDs must be checked before claiming publication.
