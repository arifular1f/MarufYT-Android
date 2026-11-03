# Phase 2B: read-only patch compatibility design

This is a compatibility design and measured structural baseline, not a patch implementation or authorization to change runtime behavior. Input identity and inventory are in [the fingerprint report](PHASE2B_FINGERPRINT_REPORT.md) and [JSON inventory](PHASE2B_FINGERPRINT_INVENTORY.json). No patch is supported by this phase.

## Version fingerprint requirements

Before any future transform can even be considered, require exact package, version name, Android long version code and whole-file SHA-256. The present research baseline is com.google.android.youtube, 21.44.528, 1561310186, `55be430ce82dcedcb737ea27d1b78576737b75d11cde04aa89989e5376d3ae6c`. Check each required DEX's hash and expected class location; reject missing or ambiguous declarations. An unchanged filename or version label is insufficient.

The generator reads expected release identity from patches/releases.json, while selection queries are separate, configurable and version-neutral. The schema supports future versions without assuming the same names, DEX numbers, resource IDs or feature ownership. A newly analyzed version needs a new evidence inventory; do not extend support by editing only a version string.

## Example measured signature requirements

These declarations exist in the baseline. Their semantic role and suitability as modification points are not established by their signatures.

| Candidate declaration | DEX | Additional evidence required before implementation |
| --- | --- | --- |
| com.google.android.apps.youtube.app.watchwhile.MainActivity.onCreate(Landroid/os/Bundle;)V | classes.dex | Launcher alias chain, startup dependencies and lifecycle tests |
| com.google.android.libraries.youtube.player.background.service.BackgroundPlayerService.onStartCommand(Landroid/content/Intent;II)I | classes2.dex | Inherited behavior, audio focus, entitlement and process lifecycle |
| com.google.android.apps.youtube.app.settings.videoquality.VideoQualityPrefsFragment.aS()V | classes4.dex | Preference/store/controller data flow and experiment branches |
| com.google.android.libraries.youtube.media.player.exo2.platypus.PlaybackControllerWrapper.i(Lcom/google/android/apps/youtube/proto/streaming/SabrSeekOuterClass$SabrSeek;)V | classes2.dex | Message semantics, time base, caller ownership and safe thread |
| com.google.android.libraries.youtube.player.subtitles.ui.SubtitleWindowView.onMeasure(II)V | classes6.dex | Rendering inputs versus track-selection controller |

For each required method match its complete owner/name/prototype, access flags, direct/virtual classification and declared body presence. The inventory also supplies code offsets, instruction unit counts and SHA-256 of instruction bytes. These hashes include DEX-local index operands and are deliberately exact-version evidence. They do not cover debug metadata, exception tables, native code, runtime dispatch or full semantic equivalence. Do not treat a hash match alone as behavioral proof or apply the same hash to a recompiled DEX.

## Resource and manifest checks

Match both symbolic name and numeric resource ID, plus resolved archive path where relevant. Examples: id/pivot_bar=`0x7f0b0efe`, id/caption_toggle=`0x7f0b0348`, id/quality_button=`0x7f0b10bb`, xml/videoquality_prefs=`0x7f18002e` -> res/tQJ.xml. Resolve file paths through resources.arsc; symbolic names are not necessarily ZIP paths. Different configurations may provide multiple files.

Check component kind, alias target, exported/enabled state, permission and foregroundServiceType. Launcher aliases target the actual MainActivity; an alias need not have a DEX class. BackgroundPlayerService is non-exported with foregroundServiceType=0x2. Never substitute an alias name for the target class descriptor. Compare required native ABI/machine/ELF metadata separately; load alignment alone does not prove platform compatibility.

## Dependency relationships and report format (design)

Future prerequisites should be explicit, for example: input integrity -> manifest/resources/DEX identity -> required-symbol resolution -> feature-specific semantic evidence -> isolated implementation tests -> output integrity/signature -> device regression. Playback consumers such as a future SponsorBlock integration additionally depend on reliable video identity, current time, seek semantics, lifecycle and consent. A view or progress bar does not satisfy those dependencies.

The existing Phase 2A PatchRegistry provides metadata-only dependency ordering and detects duplicates, missing dependencies and cycles. Phase 2B adds structural evidence but does not connect an executor or register production patches. Future read-only compatibility reports should contain requirement IDs, observed evidence references, MATCH/MISMATCH/UNKNOWN states, blocked dependencies and a clear not-executable decision whenever any required evidence is missing. MATCH must mean only that the stated structural requirement matched.

The current inventory is always patch_supported=false. A HIGH-confidence declaration means the symbol or edge was observed; an area rated MEDIUM or LOW still has unresolved feature ownership. The JSON Schema prevents converting this inventory into a positive patch-support claim.

## Failure and fallback rules

Abort input analysis on missing APK, hash mismatch or identity mismatch. Reject malformed/out-of-bounds DEX, ambiguous duplicate classes, unsupported DEX formats and invalid inventory/schema references. SDK decoding failures are recorded as coverage limitations and must block any requirement relying on them. Changed code signatures, body hashes, resource names/IDs/configurations, manifest contracts or ABI assumptions produce MISMATCH or UNKNOWN, never silent success.

For a missing fingerprint: disable/block only the proposed dependent feature in the future compatibility report, propagate blocked dependencies and leave the host unchanged. Do not guess an obfuscated method by argument count, select the first similarly named class, use a wildcard version range or silently switch to an older binary.

No analyzed fallback exists (fallback=null). A fallback would require separately supplied and analyzed input, its own signature/provenance review, fingerprints and device evidence. Do not download another APK automatically, copy iOS version numbers, or treat this research baseline as an approved stable modified release.

## Status and remaining work

Implemented: reusable metadata extraction, integrity gate, schema/cross-reference validation and recorded static evidence. Design only: patch-specific semantic requirements, execution failure isolation, rollback and signing/output checks. Unknown: runtime feature correctness, server experiments, caller/thread/entitlement semantics and safe modification points. Recommended next phase is an explicitly approved, scoped compatibility/semantic-validation plan, not automatic patch implementation. Phase 2C has not started.
