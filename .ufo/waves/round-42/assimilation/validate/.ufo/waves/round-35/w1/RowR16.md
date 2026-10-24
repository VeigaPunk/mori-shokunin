measured 2026-10-23T08:52:07Z
# Round 16 capabilities-register finding — RowR16

Axes reviewed: row support, strong-path admissibility, and claim-scope fidelity. No scoreboard axis or frozen contract was changed.

## Finding


DRAFT SCORECARD.md — last `## Capabilities` section
```DRAFT SCORECARD.md
ROW: | rounds[353].capabilities_added[0] | Exact-anchor journal window | Reads one user or system window after an exact, retained same-boot anchor without MESSAGE; unsafe captures are unavailable, 64 fixtures matched, and live observations were anchor-only, not positive load or proof of no event. | `tools/mori-journal-window.py` | 16 |
```

Path choice: `tools/mori-journal-window.py` is the direct C1 probe named as added in the closure report, and the verifier spot-check names its cursor query construction; the other candidates are a knowledge note or gates (/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/mori.md:7; corpus/lessons/round-16-verifier-spotcheck.md:101-102).

Citations for the row: the fleet MANIFEST records the capability and says the static recount matched 64/64 while live user/system evidence was anchor-only (/home/vgpnk/Projects/shokunin/MANIFEST.json:8083-8093 at fleet commit `37b51a243302e8009c7067431e8a47f9a722fd14`). The fleet report scopes the tool to an exact anchor, one scope, MESSAGE-free capture, and records the finite and live results (/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/mori.md:5-11,46-69). The verifier recount says 64→0 unmet, records unsafe-capture spot-reads, and limits live evidence to anchor-only rather than no-event or positive-load evidence (/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-16-verifier-spotcheck.md:90-119 at lane commit `24526ea9617cd020fee16c28fe4d4a2789dc28cb`).
VERDICT: supported

## Provenance and gates

- Timestamp command: `date -u +%FT%TZ` → `2026-10-23T08:52:07Z`.
- Read `MANIFEST.json` at fleet commit `37b51a243302e8009c7067431e8a47f9a722fd14` with `ulimit -v 1048576; timeout 120s git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json | jq '.rounds[353]'`; output identifies round 16 and the single capability. Exact source lines 8083-8093 name the capability, report, spot-check, and verifier recount.
- Read all four candidate blobs at lane commit `24526ea9617cd020fee16c28fe4d4a2789dc28cb` with `ulimit -v 1048576; for p in corpus/knowledge/journal-cursor-window-r16.md tools/mori-journal-window.py tools/mori-round16-context-check.py tools/mori-round16-regressions.py; do printf '\n=== %s ===\n' "$p"; timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 24526ea9617cd020fee16c28fe4d4a2789dc28cb:"$p" | nl -ba; done`. The selected tool directly constructs the single-scope `--cursor=` query (`mori-shokunin/tools/mori-journal-window.py`:432-444); the closure report names it as the added C1 tool (/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/mori.md:7). The knowledge note and context/regression gates were reviewed but are less direct evidence of the behavior being registered.
- Strong-path commands used `ulimit -v 1048576; timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-status b83edc6ee3db6822382ab673d7e6e984e420f22f..24526ea9617cd020fee16c28fe4d4a2789dc28cb -- corpus/knowledge/journal-cursor-window-r16.md tools/mori-journal-window.py tools/mori-round16-context-check.py tools/mori-round16-regressions.py; timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-status 24526ea9617cd020fee16c28fe4d4a2789dc28cb..HEAD -- corpus/knowledge/journal-cursor-window-r16.md tools/mori-journal-window.py tools/mori-round16-context-check.py tools/mori-round16-regressions.py`. First output: `A` for all four candidates. Second output: only `M corpus/knowledge/journal-cursor-window-r16.md`; the chosen tool is unchanged and present at lane tip. `tools/` is an admitted path. The whole path is named in the fleet report (/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/mori.md:7) and verifier spot-check (corpus/lessons/round-16-verifier-spotcheck.md:101-102).
- Closure execution evidence is distinguished from verifier work: the fleet report records L1's finite gate and two live observations (/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/mori.md:46-69). The non-author spot-check labels its receipts “Evidence-verified, not executed” and states that the reviewer ran no sibling gate, selftest, probe, or live query (/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-16-verifier-spotcheck.md:6-7,104-119). This seat ran no counter, gate, selftest, probe, or live query.

## Surfaces, bounds, and artifacts

- Lane write: this report only, `.ufo/waves/round-35/w1/RowR16.md`. No product code, SCORECARD, MANIFEST, judge, or commit was changed.
- Read surfaces: fleet `MANIFEST.json` and fleet round-16 report at the specified fleet revision; lane round-16 verifier spot-check at `24526ea9617cd020fee16c28fe4d4a2789dc28cb`; the four candidate blobs at that lane commit; lane candidate-path diff against previous closure `b83edc6ee3db6822382ab673d7e6e984e420f22f` and lane tip `913df22e29f131ef9cb5de9dcb7e3e272256c5f0`.
- Claim limits: live observations were anchor-only, not positive load or evidence that no event occurred; unsafe-capture boundaries are supported by finite fixtures, not live vacuum/alias/cross-boot experiments (/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/mori.md:11,69; corpus/lessons/round-16-verifier-spotcheck.md:95-119). The verifier performed a static recount, not gate execution (corpus/lessons/round-16-verifier-spotcheck.md:77-93,104-119).
- Scratch artifacts read from the specified revisions: `/fast/scratch/hyaku/mori-r35/RowR16/manifest-37b.json`, `journal-cursor-window-r16.md`, `mori-journal-window.py`, `mori-round16-context-check.py`, and `mori-round16-regressions.py`. No tool was installed or updated.
