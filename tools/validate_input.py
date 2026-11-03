"""Validate user-owned input; never generate a modified YouTube APK."""
import argparse
import json
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'apk-analysis'))
from fingerprint_apk import gate
from marufyt.analysis import analyze,sdk_paths
from marufyt.compatibility import check_release
from marufyt.models import ApkIdentity

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('apk',type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    try:
        if args.output.exists() or args.output.suffix!='.json':raise ValueError('Use a fresh JSON output')
        target=json.loads((Path(__file__).resolve().parents[1]/'patches/releases.json').read_text())
        sdk,java=os.environ['ANDROID_HOME'],os.environ['JAVA_HOME']
        gate(args.apk.resolve(),target['primary'],sdk_paths(sdk,java),[])
        report=analyze(args.apk,sdk,java)
        readiness=check_release(ApkIdentity(**report['manifest']['identity']),report['sha256'],target)
        result={'identity':report['manifest']['identity'],'sha256':report['sha256'],'signature_verified':report['signature_verified'],
                'unchanged':report['unchanged'],'compatibility':readiness,'registered_patches':[],
                'build_decision':'BLOCKED_NO_VALIDATED_TRANSFORMS','modified_apk_created':False}
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2)
        print(json.dumps(result));return 0
    except (ValueError,OSError,KeyError) as exc:
        print('Input validation failed: '+str(exc),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
