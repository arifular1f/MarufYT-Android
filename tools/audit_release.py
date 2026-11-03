"""Verify the source archive's complete manifest and proprietary-input exclusion."""
import argparse,hashlib,json
from pathlib import Path,PurePosixPath
import zipfile
from prepare_release import ALLOWED_DIRS,ALLOWED_FILES,FORBIDDEN

def audit(path):
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)):raise ValueError('Duplicate archive entries')
        manifest=json.loads(archive.read('SOURCE_MANIFEST.json'))
        if set(names)!=set(manifest)|{'SOURCE_MANIFEST.json'}:raise ValueError('Manifest does not cover the entire archive')
        for name,digest in manifest.items():
            p=PurePosixPath(name)
            if '..' in p.parts or p.is_absolute() or '\\' in name or ':' in name:raise ValueError('Unsafe archive path')
            if p.parts[0] not in ALLOWED_DIRS and name not in ALLOWED_FILES:raise ValueError('Unreviewed archive file')
            if p.suffix.lower() in FORBIDDEN or set(p.parts)&{'build','main apk','validation-local','.git','__pycache__'}:raise ValueError('Forbidden archive payload')
            if hashlib.sha256(archive.read(name)).hexdigest()!=digest:raise ValueError('Source hash mismatch: '+name)
        if archive.testzip():raise ValueError('ZIP CRC failure')
    return len(manifest)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('archive',type=Path);args=parser.parse_args()
    print('Source archive audit: PASS;',audit(args.archive),'files')
