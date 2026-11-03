"""Produce a deterministic source-only preview archive from reviewed repository paths."""
import argparse
import hashlib
import json
from pathlib import Path,PurePosixPath
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
ALLOWED_DIRS={'.github','app','patches','integrations','tools','tests','Documentation','gradle','licenses'}
ALLOWED_FILES={'.gitignore','.gitattributes','README.md','CHANGELOG.md','CONTRIBUTING.md','SECURITY.md','LICENSE_STATUS.md','THIRD_PARTY_NOTICES.md','build.gradle','settings.gradle','gradle.properties','gradlew','gradlew.bat','release.json'}
FORBIDDEN={'.apk','.aab','.apks','.xapk','.obb','.keystore','.jks','.pem','.p12'}

def source_files(root=ROOT):
    raw=subprocess.check_output(['git','-C',str(root),'ls-files','-z','--cached','--others','--exclude-standard'])
    result=[]
    for name in sorted(set(raw.decode('utf-8').strip('\0').split('\0'))):
        if not name:continue
        path=PurePosixPath(name)
        if (path.parts[0] not in ALLOWED_DIRS and name not in ALLOWED_FILES):raise ValueError('Unreviewed release path: '+name)
        if (set(path.parts)&{'build','.gradle','__pycache__','main apk','validation-local','.git'} or path.suffix.lower() in FORBIDDEN
                or any(part.startswith('.env') for part in path.parts) or (path.suffix=='.jar' and name!='gradle/wrapper/gradle-wrapper.jar')):
            raise ValueError('Forbidden release input: '+name)
        local=root/name
        if local.is_symlink():raise ValueError('Symlink release input rejected')
        result.append(name)
    return result

def build(output,tag=None,root=ROOT):
    release=json.loads((root/'release.json').read_text())
    if tag is not None and tag!=release['tag']:raise ValueError('Tag does not match release.json')
    if not release['prerelease'] or release['patch_supported']:raise ValueError('Only a research preview is supported')
    files=source_files(root)
    if output.exists():raise ValueError('Release output exists; use a new directory')
    contents={name:(root/name).read_bytes() for name in files}
    manifest={name:hashlib.sha256(data).hexdigest() for name,data in contents.items()}
    output.mkdir(parents=True)
    archive=output/('MarufYT-Android-'+release['version']+'-source.zip')
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as stream:
        for name,data in sorted(contents.items()):
            item=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));item.create_system=3
            item.external_attr=(0o100755 if name=='gradlew' else 0o100644)<<16
            item.compress_type=zipfile.ZIP_DEFLATED;stream.writestr(item,data)
        item=zipfile.ZipInfo('SOURCE_MANIFEST.json',date_time=(1980,1,1,0,0,0));item.create_system=3;item.external_attr=0o100644<<16
        stream.writestr(item,json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    report=output/'RELEASE_REPORT.json'
    revision=subprocess.run(['git','-C',str(root),'rev-parse','--verify','HEAD'],capture_output=True,text=True)
    report.write_text(json.dumps({**release,'source_file_count':len(files),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
        'source_commit':revision.stdout.strip() if revision.returncode==0 else None,
        'license_status':'Original-code license not assigned; see LICENSE_STATUS.md','device_tested':False,'proprietary_payloads':False},indent=2)+'\n')
    sums=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in (archive,report))
    (output/'SHA256SUMS.txt').write_text(sums,encoding='ascii')
    print(sums,end='')
    return archive

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True,type=Path);p.add_argument('--tag')
    args=p.parse_args()
    try:build(args.output.resolve(),args.tag);return 0
    except (ValueError,OSError,subprocess.SubprocessError) as exc:print('Release preparation failed: '+str(exc));return 1
if __name__=='__main__':raise SystemExit(main())
