# LiveRunner — round 20 C2 fleet-live

## Result

Implemented the fleet collector at `mori-shokunin/.ufo/waves/round-20/build/LiveRunner/c2-fleet-live.py`. It discovers top-level `*-shokunin` directories, invokes the supplied tool once per lane with `scan --lane-root … --fleet-root … --out <temporary file>`, and emits `mori-r20-c2-fleet-live-v1` JSON with sorted per-lane `waves`, `members`, `present`, `missing`, `empty`, `misrooted`, `unsafe`, `unparsed`, `unreadable_json`, and `exit` fields. The filename flags use only `dispatch_path` values from the scan result and flag paths whose filename matches `preview|undispatched|validation|not-dispatched`; report contents are not read or emitted by this collector.

Added `mori-shokunin/.ufo/waves/round-20/build/LiveRunner/fake-wave-settlement.py`, a 10-line fake used only for the requested unit check.

## Evidence

- Fake-tool line count: `wc -l /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/LiveRunner/fake-wave-settlement.py` → `10 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/LiveRunner/fake-wave-settlement.py`.
- SHA-256: `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/LiveRunner/c2-fleet-live.py` → `7633c1f131f76936e0f1352a75dda691d8f271fd7e0865c8dea8a420010d403e`.
- Unit-check command used the fake tool, not a real settlement tool: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/LiveRunner/c2-fleet-live.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/LiveRunner/fake-wave-settlement.py --fleet-root /home/vgpnk/Projects/shokunin`.
- Exact fake-tool output (all totals below are synthetic fixture values, not live settlement counts):

```json
{
  "dispatch_filename_flags": [
    {
      "lane": "audio-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "chousa-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "game-dev-2d-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "game-dev-3d-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "kagi-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "kaidoku-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "kake-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "kama-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "kasegi-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "kengaku-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "kotoba-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "kotodama-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "kumitate-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "lore-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "mado-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "mori-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "revenger-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "souji-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "tabi-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "tameshi-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    },
    {
      "lane": "tsukuroi-shokunin",
      "path": ".ufo/waves/round-20/wave-preview.json"
    }
  ],
  "fleet_root": "/home/vgpnk/Projects/shokunin",
  "lanes": [
    {
      "empty": 0,
      "exit": 0,
      "lane": "audio-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "chousa-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "game-dev-2d-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "game-dev-3d-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "kagi-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "kaidoku-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "kake-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "kama-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "kasegi-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "kengaku-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "kotoba-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "kotodama-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "kumitate-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "lore-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "mado-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 1,
      "lane": "mori-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "revenger-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "souji-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "tabi-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "tameshi-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    },
    {
      "empty": 0,
      "exit": 0,
      "lane": "tsukuroi-shokunin",
      "members": 2,
      "misrooted": 0,
      "missing": 1,
      "present": 1,
      "unparsed": 0,
      "unreadable_json": 0,
      "unsafe": 0,
      "waves": 1
    }
  ],
  "schema": "mori-r20-c2-fleet-live-v1"
}
```

## Risks and blockers

- No real `mori-wave-settlement.py` was present; per the assignment, this collector was not run against a real tool. Integration should confirm the settlement output keys match the frozen C2 contract.
- No tool installation was needed. No LSP refactor/reference operation applied to this new standalone script.
- No blockers to the scoped implementation.
