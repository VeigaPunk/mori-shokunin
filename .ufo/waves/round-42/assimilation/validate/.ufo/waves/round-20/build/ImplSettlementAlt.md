# ImplSettlementAlt — round 20 C2

## Result

Implemented an independent, stdlib-only, scan-only settlement scanner at `.ufo/waves/round-20/build/ImplSettlementAlt/tools/mori-wave-settlement.py`. It discovers regular JSON dispatch records under the lane wave tree without following symlinks, parses the task report trailer, checks safe report paths without reading report contents, classifies per-member status, hashes dispatch bytes, and emits deterministic JSON. No selftest mode was added, as requested.

The requested scan output is `.ufo/waves/round-20/build/ImplSettlementAlt/mori-scan.json`.

## Scan evidence

Command run once:

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/ImplSettlementAlt/tools/mori-wave-settlement.py scan --lane-root /home/vgpnk/Projects/shokunin/mori-shokunin --fleet-root /home/vgpnk/Projects/shokunin --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/ImplSettlementAlt/mori-scan.json
```

Exit code: **1**. The scan recorded 11 waves, 671 members, 586 present, 85 missing, 0 misrooted, 462 ignored JSON files, and 2 unreadable JSON files. State totals were 8 settled and 3 partial. The partial states account for exit 1, consistent with the contract's exit rule (`.ufo/waves/round-20/contract.md:82-88`).

| Dispatch path | Wave | Members | Present | Missing | Misrooted |
|---|---|---:|---:|---:|---:|
| `.ufo/waves/round-13/dispatch.json` | `mori-r13-build` | 32 | 32 | 0 | 0 |
| `.ufo/waves/round-14/dispatch.json` | `mori-r14-repair` | 32 | 32 | 0 | 0 |
| `.ufo/waves/round-15/dispatch.json` | `mori-r15-positive` | 64 | 64 | 0 | 0 |
| `.ufo/waves/round-16/wave1-dispatch.json` | `mori-r16-window-build` | 64 | 64 | 0 | 0 |
| `.ufo/waves/round-17/wave1-dispatch.json` | `mori-r17-w1-build` | 70 | 70 | 0 | 0 |
| `.ufo/waves/round-17/wave2-dispatch.json` | `mori-r17-w2-falsify` | 64 | 64 | 0 | 0 |
| `.ufo/waves/round-18/wave1-dispatch.json` | `mori-r18-w1-build` | 68 | 53 | 15 | 0 |
| `.ufo/waves/round-18/wave2-dispatch.json` | `mori-r18-w2-falsify` | 67 | 67 | 0 | 0 |
| `.ufo/waves/round-19/wave1-run.json` | `mori-r19-attempt2-build` | 64 | 16 | 48 | 0 |
| `.ufo/waves/round-19/wave2-run.json` | `mori-r19-attempt2-falsify` | 70 | 48 | 22 | 0 |
| `.ufo/waves/round-20/wave1-run.json` | `mori-r20-build` | 76 | 76 | 0 | 0 |

The live round-19 wave-1 demonstration recorded 16 present of 64 members, matching the contract's stated demonstration criterion (`.ufo/waves/round-20/contract.md:95-98`). Missing-report classifications are not evidence that a seat is dead; the contract explicitly forbids that inference (`.ufo/waves/round-20/contract.md:78-80`).

Scanner SHA-256 (from `sha256sum`):

```text
59f3751c9309da2a90a1e5b1a9a74889ad32fcf3f0e74711afbf481a4808f26b  .ufo/waves/round-20/build/ImplSettlementAlt/tools/mori-wave-settlement.py
```

## Checks, risks, blockers

- The one requested `scan` invocation was run. No selftest, build, lint, formatter, or other test was run.
- The scan reported 2 unreadable JSON files; the output provides only the count, and they were not investigated further.
- No tool was installed or updated.
- No implementation blocker observed. The three partial waves and their missing-member counts are scan findings, not claims about seat liveness.
