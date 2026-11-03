# sponsorblock

Future responsibility: Opt-in SponsorBlock contracts and client.

The Java runtime module remains empty: no YouTube playback integration is verified. The independently functional host client is tools/marufyt/sponsorblock.py, exposed by tools/sponsorblock_lookup.py. It supports opt-in hash-prefix lookup, category/response validation, timeout/error handling and bounded memory caching; tests/test_sponsorblock.py covers it. It does not skip playback. See Documentation/SPONSORBLOCK.md and SEMANTIC_VALIDATION.md.
