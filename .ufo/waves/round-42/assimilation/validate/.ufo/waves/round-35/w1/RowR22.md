measured 2026-10-23T08:52:19Z
Clock measurement: `date -u +%FT%TZ` returned `2026-10-23T08:52:19Z`.

## Draft

```DRAFT SCORECARD.md
ROW: | rounds[427].capabilities_added[0] | Retention receipt reconciliation | Independently recounts a committed retention receipt’s measured Git tree, reports identity agreement and policy exclusions, and shows red retention; agreement is accounting only, not privacy clearance (.ufo/reports/round-22/mori.md:7,44; MANIFEST.json:12007,12018) | `tools/mori-retention-reconcile.py` | 22 |
VERDICT: supported — the closure verification records a selftest and direct check of the r21 receipt returning rc0 RETENTION_RECONCILED with privacy_clearance false (MANIFEST.json:12018; .ufo/reports/round-22/mori.md:44).
```

Path rationale: The closure names this exact tool and hash and records its direct run against the r21 receipt, making it the strongest single evidence path (MANIFEST.json:12007,12018).

Citations: The pinned manifest entry gives the capability string and report/closure references (fleet commit 37b51a243302e8009c7067431e8a47f9a722fd14, MANIFEST.json:12007,12009-10); the report describes the measured capability and bounded result (.ufo/reports/round-22/mori.md:7,11,44); the closure source scans the measured tree and returns reconciliation and clearance fields (lane commit 1bfe708a170c877db3319060d0ab38771efe03ac, tools/mori-retention-reconcile.py:143-157,231-240).

## Gates and provenance

- `git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json` extraction returned `rounds[427]`, round 22, admitted closure, the requested capability string, report path, and closure commit (MANIFEST.json:12007,12009-10).
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-status 77a5bbe8a0b41dfbfd2546d024d36e294b814bd0 1bfe708a170c877db3319060d0ab38771efe03ac -- tools/mori-retention-reconcile.py` returned `A tools/mori-retention-reconcile.py`.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 1bfe708a170c877db3319060d0ab38771efe03ac:tools/mori-retention-reconcile.py` and the corresponding `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 913df22e29f131ef9cb5de9dcb7e3e272256c5f0:tools/mori-retention-reconcile.py` both exited 0. The path is under `tools/` and is named in full by the capability string (MANIFEST.json:12007).
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 1bfe708a170c877db3319060d0ab38771efe03ac:tools/mori-retention-reconcile.py | sha256sum` returned `0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32`, matching the capability digest and closure report (MANIFEST.json:12007,12018; .ufo/reports/round-22/mori.md:11).
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --quiet 1bfe708a170c877db3319060d0ab38771efe03ac 913df22e29f131ef9cb5de9dcb7e3e272256c5f0 -- tools/mori-retention-reconcile.py` exited 1. The lane-tip path exists but its blob differs from the closure blob; this draft and digest refer to the requested closure commit.
- Closure execution evidence is recorded, not rerun by this scribe: the manifest reports a direct r21-receipt check and 4/4 selftest (MANIFEST.json:12018); the report records identity agreement, 95 raw hits, red retention, and privacy_clearance false (.ufo/reports/round-22/mori.md:44).

## Behavior, bounds, and known limits

The capability is accounting reconciliation only and never grants privacy clearance (MANIFEST.json:12007; .ufo/reports/round-22/mori.md:7,44). The receipt remains red with four unallowlisted hits; this row does not imply that retention debt was cleared (.ufo/reports/round-22/mori.md:7,44). The closure report notes residual lone surrogate escapes, per-blob cat-file cost, strict refusal of non-UTF-8 paths, and refusal of mode 100664 files (.ufo/reports/round-22/mori.md:44).

## Touched surfaces and out of scope

The assigned report is the only remaining written artifact. A misplaced duplicate at `/home/vgpnk/Projects/shokunin/mori-shokukin/mori-shokunin/.ufo/waves/round-35/w1/RowR22.md` was briefly written by this scribe and then deleted with `REM`; it is not retained. The manifest, fleet report, lane code, and scorecard were read-only; no tool was installed and no test or counter was run by this scribe. Evidence paths are listed above.

## Artifact path

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/w1/RowR22.md`
