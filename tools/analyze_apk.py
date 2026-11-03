"""Read-only local APK analysis CLI. Output is metadata, never an APK copy."""
import argparse
import json
import os
from pathlib import Path
import sys

from marufyt.analysis import analyze
from marufyt.compatibility import CompatibilityError, check_release
from marufyt.models import AnalysisError, ApkIdentity


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('apk', type=Path)
    parser.add_argument('--sdk', default=os.environ.get('ANDROID_HOME'))
    parser.add_argument('--java-home', default=os.environ.get('JAVA_HOME'))
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--releases', type=Path)
    args = parser.parse_args()
    try:
        if not args.sdk or not args.java_home:
            raise AnalysisError('Set ANDROID_HOME and JAVA_HOME or pass --sdk and --java-home')
        source = args.apk.resolve(strict=True)
        output = args.output.resolve()
        if output == source or output.suffix.lower() in {'.apk', '.aab', '.apks', '.xapk', '.obb'}:
            raise AnalysisError('Output must be a metadata file distinct from the APK')
        # Refuse overwrites, including hardlinks to the source or existing analysis evidence.
        if output.exists(): raise AnalysisError('Output already exists; choose a new metadata filename')
        report = analyze(source, args.sdk, args.java_home)
        status = 0
        if args.releases:
            config = json.loads(args.releases.read_text(encoding='utf-8'))
            try:
                report['compatibility'] = check_release(ApkIdentity(**report['manifest']['identity']), report['sha256'], config)
            except CompatibilityError as exc:
                report['compatibility'] = {'status': 'UNSUPPORTED_INPUT', 'patch_supported': False, 'error': str(exc)}
                status = 2
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('x', encoding='utf-8') as stream:
            json.dump(report, stream, indent=2, ensure_ascii=False)
            stream.write('\n')
        print(json.dumps({key: report[key] for key in ('path', 'size_bytes', 'sha256', 'unchanged')}))
        print('Identity:', json.dumps(report['manifest']['identity']))
        print('Metadata written to', output)
        return status
    except (AnalysisError, OSError, ValueError) as exc:
        print(f'Analysis failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
