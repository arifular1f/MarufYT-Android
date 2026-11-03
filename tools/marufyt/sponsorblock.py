"""Opt-in host lookup only. No player attachment or automatic seeking."""
from collections import OrderedDict
from dataclasses import dataclass
import hashlib
import json
import math
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

CATEGORIES = frozenset(('sponsor', 'intro', 'outro', 'selfpromo', 'interaction', 'music_offtopic', 'preview', 'filler'))
MAX_RESPONSE = 2 * 1024 * 1024


class SponsorBlockError(ValueError):
    pass


def video_id(value):
    if re.fullmatch(r'[A-Za-z0-9_-]{11}', value): return value
    url = urlparse(value)
    if url.scheme != 'https' or url.username or url.password or url.port:
        raise SponsorBlockError('Use an 11-character video ID or an HTTPS YouTube URL')
    if url.hostname == 'youtu.be': candidate = url.path.strip('/')
    elif url.hostname in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
        if url.path == '/watch': candidate = parse_qs(url.query).get('v', [''])[0]
        elif re.fullmatch(r'/(shorts|embed)/[A-Za-z0-9_-]{11}/?', url.path): candidate = url.path.strip('/').split('/')[1]
        else: candidate = ''
    else: candidate = ''
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', candidate): raise SponsorBlockError('Unsupported video identity')
    return candidate


def number(value):
    try: valid = not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)
    except OverflowError: valid = False
    if not valid:
        raise SponsorBlockError('Invalid numeric response value')
    return float(value)


def rational_seconds(ticks, timescale):
    if (isinstance(ticks, bool) or isinstance(timescale, bool) or not isinstance(ticks, int)
            or not isinstance(timescale, int) or not 0 <= ticks <= 2**63-1 or not 0 < timescale <= 2**63-1):
        raise SponsorBlockError('Invalid finite rational clock value')
    return ticks / timescale


def seconds_to_milliseconds(seconds):
    seconds = number(seconds)
    if not 0 <= seconds <= 86400: raise SponsorBlockError('Timestamp outside supported range')
    return round(seconds * 1000)


@dataclass(frozen=True)
class Segment:
    start: float
    end: float
    category: str
    uuid: str


def parse_response(payload, identity, categories, duration=None):
    if not isinstance(payload, list) or len(payload) > 5000: raise SponsorBlockError('Invalid response collection')
    if any(not isinstance(item, dict) or not isinstance(item.get('videoID'), str) or not isinstance(item.get('segments'), list) for item in payload):
        raise SponsorBlockError('Malformed video response')
    matches = [item for item in payload if isinstance(item, dict) and item.get('videoID') == identity]
    if len(matches) > 1: raise SponsorBlockError('Duplicate video response')
    if not matches: return ()
    segments = matches[0].get('segments')
    if not isinstance(segments, list) or len(segments) > 5000: raise SponsorBlockError('Invalid segment collection')
    if duration is not None and number(duration) <= 0: raise SponsorBlockError('Invalid current duration')
    result, seen = [], set()
    for item in segments:
        if not isinstance(item, dict): raise SponsorBlockError('Invalid segment')
        if item.get('actionType') != 'skip' or item.get('category') not in categories: continue
        interval = item.get('segment')
        if not isinstance(interval, list) or len(interval) != 2: raise SponsorBlockError('Invalid interval')
        start, end = map(number, interval)
        if not 0 <= start < end <= 86400: raise SponsorBlockError('Invalid interval bounds')
        uuid = item.get('UUID')
        if not isinstance(uuid, str) or not re.fullmatch(r'[a-fA-F0-9-]{1,128}', uuid) or uuid in seen:
            raise SponsorBlockError('Invalid/duplicate segment identifier')
        submitted = number(item.get('videoDuration', 0))
        if submitted < 0: raise SponsorBlockError('Invalid submitted duration')
        if duration is not None:
            if end > duration or (submitted and abs(submitted - duration) > 1):
                raise SponsorBlockError('Duration mismatch; timestamps are not safe to map')
        seen.add(uuid)
        result.append(Segment(start, end, item['category'], uuid))
    return tuple(sorted(result, key=lambda segment: (segment.start, segment.end, segment.uuid)))


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise SponsorBlockError('Redirect rejected')


class Client:
    def __init__(self, *, timeout=8, ttl=600, clock=time.monotonic, opener=None):
        if not 0 < timeout <= 30 or not 0 < ttl <= 3600: raise SponsorBlockError('Invalid client limits')
        self.timeout, self.ttl, self.clock = timeout, ttl, clock
        self.opener = opener or build_opener(NoRedirect())
        self.cache = OrderedDict()

    def lookup(self, identity, categories=('sponsor', 'intro', 'outro'), duration=None):
        identity = video_id(identity)
        categories = tuple(sorted(set(categories)))
        if not categories or not set(categories) <= CATEGORIES: raise SponsorBlockError('Unsupported category selection')
        if duration is not None:
            duration = number(duration)
            if not 0 < duration <= 86400: raise SponsorBlockError('Invalid current duration')
        key = identity, categories, duration
        now = self.clock()
        if key in self.cache:
            expires, data = self.cache.pop(key)
            if expires > now:
                self.cache[key] = expires, data
                return data
        prefix = hashlib.sha256(identity.encode('ascii')).hexdigest()[:4]
        query = urlencode({'categories': json.dumps(categories), 'actionTypes': '["skip"]', 'service': 'YouTube'})
        request = Request('https://sponsor.ajay.app/api/skipSegments/' + prefix + '?' + query,
                          headers={'User-Agent': 'MarufYT-Android-Research/0.2', 'Accept': 'application/json'})
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                if response.geturl() != request.full_url: raise SponsorBlockError('Unexpected response location')
                if response.headers.get_content_type() != 'application/json': raise SponsorBlockError('Unexpected content type')
                raw = response.read(MAX_RESPONSE + 1)
                if len(raw) > MAX_RESPONSE: raise SponsorBlockError('Response exceeds size limit')
                data = parse_response(json.loads(raw), identity, categories, duration)
        except HTTPError as exc:
            if exc.code == 404: data = ()
            else: raise SponsorBlockError('SponsorBlock HTTP failure: ' + str(exc.code)) from None
        except (URLError, TimeoutError, OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise SponsorBlockError('SponsorBlock lookup failed; no cached success was created') from None
        self.cache[key] = now + self.ttl, data
        while len(self.cache) > 64: self.cache.popitem(last=False)
        return data
