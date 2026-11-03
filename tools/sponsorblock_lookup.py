"""Explicit network lookup: sends a four-character hash prefix, never skips playback."""
import argparse
from dataclasses import asdict
import json
import sys
from marufyt.sponsorblock import Client, SponsorBlockError

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video')
    parser.add_argument('--categories', default='sponsor,intro,outro')
    parser.add_argument('--duration', type=float)
    args = parser.parse_args()
    try:
        result = Client().lookup(args.video, args.categories.split(','), args.duration)
        print(json.dumps({'segments': [asdict(s) for s in result], 'playback_integration': False}, indent=2))
        return 0
    except (SponsorBlockError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

if __name__ == '__main__': raise SystemExit(main())
