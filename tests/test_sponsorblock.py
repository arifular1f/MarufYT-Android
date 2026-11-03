import sys
from pathlib import Path
import json
from email.message import Message
import unittest
from urllib.error import HTTPError, URLError
from unittest.mock import Mock

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from marufyt.sponsorblock import Client, SponsorBlockError, parse_response, seconds_to_milliseconds, video_id, NoRedirect, rational_seconds

VIDEO='abcdefghijk'
def payload(**changes):
    return [{'videoID':VIDEO,'segments':[{'segment':[1.25,5.5],'UUID':'abc123','category':'sponsor','actionType':'skip','videoDuration':100,**changes}]}]

class SponsorBlockTests(unittest.TestCase):
    def test_supported_identities(self):
        for value in (VIDEO,'https://youtu.be/'+VIDEO,'https://www.youtube.com/watch?v='+VIDEO,'https://youtube.com/shorts/'+VIDEO):
            self.assertEqual(video_id(value),VIDEO)
    def test_reject_foreign_or_insecure_urls(self):
        for value in ('https://youtube.com.evil/watch?v='+VIDEO,'http://youtu.be/'+VIDEO,'bad','https://user:pass@youtu.be/'+VIDEO):
            with self.subTest(value=value), self.assertRaises(SponsorBlockError):video_id(value)
    def test_parse_and_duration(self):
        segment=parse_response(payload(),VIDEO,{'sponsor'},100)[0]
        self.assertEqual((segment.start,segment.end),(1.25,5.5))
        self.assertEqual(seconds_to_milliseconds(segment.end),5500)
        with self.assertRaises(SponsorBlockError):parse_response(payload(),VIDEO,{'sponsor'},120)
    def test_reject_invalid_timestamps(self):
        for interval in ([5,1],[-1,2],[True,3],[0,float('nan')],[0,float('inf')],[0,90000]):
            with self.subTest(interval=interval),self.assertRaises(SponsorBlockError):parse_response(payload(segment=interval),VIDEO,{'sponsor'})
    def test_actions_categories_and_video_filtering(self):
        self.assertEqual(parse_response(payload(actionType='mute'),VIDEO,{'sponsor'}),())
        self.assertEqual(parse_response(payload(),VIDEO,{'intro'}),())
        self.assertEqual(parse_response(payload(),'otherid1234',{'sponsor'}),())
    def test_duplicate_ids_rejected(self):
        data=payload();data[0]['segments']*=2
        with self.assertRaises(SponsorBlockError):parse_response(data,VIDEO,{'sponsor'})
    def test_response_shape_rejected(self):
        for data in ({},[{'videoID':VIDEO,'segments':None}],payload(UUID='../../invalid')):
            with self.subTest(data=data),self.assertRaises(SponsorBlockError):parse_response(data,VIDEO,{'sponsor'})
    def test_cache_expiry_and_private_request(self):
        now=[0];opener=Mock();response=Mock();headers=Message();headers['Content-Type']='application/json'
        response.headers=headers;response.read.return_value=json.dumps(payload()).encode()
        response.__enter__=Mock(return_value=response);response.__exit__=Mock(return_value=False)
        opener.open.return_value=response
        response.geturl.side_effect=lambda:opener.open.call_args.args[0].full_url
        client=Client(opener=opener,clock=lambda:now[0])
        self.assertEqual(len(client.lookup(VIDEO)),1);client.lookup(VIDEO)
        self.assertEqual(opener.open.call_count,1)
        self.assertNotIn(VIDEO,opener.open.call_args.args[0].full_url)
        now[0]=601;client.lookup(VIDEO);self.assertEqual(opener.open.call_count,2)
    def test_not_found_and_timeout(self):
        opener=Mock();opener.open.side_effect=HTTPError('https://sponsor.ajay.app',404,'Not found',None,None)
        self.assertEqual(Client(opener=opener).lookup(VIDEO),())
        opener.open.side_effect=URLError('test timeout')
        client=Client(opener=opener)
        with self.assertRaises(SponsorBlockError):client.lookup(VIDEO)
        self.assertEqual(len(client.cache),0)
    def test_redirects_are_rejected(self):
        with self.assertRaises(SponsorBlockError):NoRedirect().redirect_request(None,None,302,'',{},'http://evil')
    def test_untrusted_client_options(self):
        with self.assertRaises(SponsorBlockError):Client(timeout=0)
        with self.assertRaises(SponsorBlockError):Client().lookup(VIDEO,['unknown'])
        for value in (True,-1,float('inf')):
            with self.assertRaises(SponsorBlockError):seconds_to_milliseconds(value)
    def test_rational_clock_requires_finite_valid_scale(self):
        self.assertEqual(rational_seconds(2500,1000),2.5)
        for ticks,scale in ((1,0),(-1,1000),(True,1000),(1,2**64)):
            with self.assertRaises(SponsorBlockError):rational_seconds(ticks,scale)
    def test_untrusted_response_body_and_destination(self):
        for case in ('large','html','json','destination'):
            opener=Mock();response=Mock();headers=Message();headers['Content-Type']='text/html' if case=='html' else 'application/json'
            response.headers=headers;response.read.return_value=b'x'*(2*1024*1024+1) if case=='large' else b'not json'
            response.__enter__=Mock(return_value=response);response.__exit__=Mock(return_value=False);opener.open.return_value=response
            response.geturl.side_effect=lambda:'https://other.invalid/' if case=='destination' else opener.open.call_args.args[0].full_url
            client=Client(opener=opener)
            with self.subTest(case=case),self.assertRaises(SponsorBlockError):client.lookup(VIDEO)
            self.assertEqual(len(client.cache),0)
