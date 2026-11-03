# SponsorBlock host lookup

Implemented: an explicit Python CLI, separate from the Android app. It follows the [official API documentation](https://wiki.sponsor.ajay.app/w/API_Docs): GET skipSegments with a four-character SHA-256 video-ID prefix, category selection and skip actions. Returned intervals are seconds. A documented 404 is treated as an empty result, not a fabricated segment.

```powershell
python tools/sponsorblock_lookup.py "https://www.youtube.com/watch?v=VIDEO_ID" --categories sponsor,intro,outro
```

Replace VIDEO_ID with an actual 11-character ID. Optional --duration checks submission/current duration agreement within one second and interval bounds. Supported categories: sponsor, intro, outro, selfpromo, interaction, music_offtopic, preview and filler. This prints validated metadata only; it does not seek or attach to a player. No skip preference is shown in the app because there is no skip implementation.

The client enforces a fixed HTTPS origin and certificate verification, rejects redirects, caps responses at 2 MiB, uses an eight-second socket timeout and a 64-entry memory-only cache with ten-minute expiry. It validates identity syntax, collection shapes, action/category, finite increasing intervals and duplicate identifiers. HTTP/network/JSON errors are reported without URLs or credentials. A prefix reduces disclosed identity detail but is not anonymity: the server sees the prefix, IP and selected categories. No user account, submissions, voting, telemetry or automatic requests are added.

Synthetic tests exercise parsing, timestamp calculations, identity filtering, malformed input, redirects, caching and failures. One live lookup for a public video completed with zero matching segments; that proves the observed request completed, not automatic skip behavior. Live service availability is not required by CI. API datasets/responses are not bundled with source artifacts; review the service's data/API terms before redistribution.

Android integration remains blocked by the evidence gaps in SEMANTIC_VALIDATION.md. The empty Java SponsorBlock module remains reserved; the concrete host implementation lives in tools/marufyt/sponsorblock.py.
