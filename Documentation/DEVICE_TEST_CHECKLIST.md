# Physical Android test checklist

Current evidence: `adb devices -l` showed no attached device. Every device/runtime item is NOT TESTED. Do not mark a checklist item passed without recording device model, Android version, source commit, installed APK SHA-256, steps and observed outcome. Avoid account details, URLs/history and tokens in shared evidence.

| Check | Procedure / expected result | Current status |
| --- | --- | --- |
| Installation | Install project-owned debug APK on API 26+ phone; separate io.github.arifular1f.marufyt package | NOT TESTED |
| First launch | Native preview displays 13 sections, honest availability text, no crash/cut-off text | NOT TESTED |
| Light/dark/system | Change appearance; check contrast, large text, rotation, system theme and screen insets | NOT TESTED |
| Settings persistence | Choose Dark, force-stop/relaunch, verify selection; reset and verify system default | NOT TESTED |
| App restart | Repeat selection/reset across process death; test corrupt/old preference recovery separately | NOT TESTED |
| YouTube login | Preview does not replace or sign into YouTube; confirm normal official app login independently | NOT TESTED; no integration claim |
| Video / Shorts playback | No preview playback feature exists; verify official YouTube remains unaffected | NOT TESTED; not a supported preview feature |
| SponsorBlock | CLI can query metadata; no Android skip behavior to exercise | Android integration BLOCKED |
| Background / screen-off | No background-playback implementation or toggle | BLOCKED |
| Audio focus / notifications | No preview audio service; no claim about host lifecycle | BLOCKED |
| Network failure recovery | Host CLI: offline, timeout, non-JSON, redirect and 404 tests; app itself has no network permission | Automated host cases covered; device NOT TESTED |
| Screenshots | Capture real device light/dark views only after installation, remove personal identifiers | PENDING |

Do not install a re-signed or modified YouTube binary: none is produced. Any future playback integration needs a new device plan including transitions, ads/live streams, seek completion, headphones/calls, focus loss, lock screen, cleanup, error recovery and account/entitlement variations.
