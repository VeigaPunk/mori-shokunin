measured 2026-10-23T08:52:12Z
# Round 26 capability-register finding

## Draft for L1

```DRAFT SCORECARD.md
ROW: | rounds[462].capabilities_added[0] | Userspace OOM killer one-shot read | Reads earlyoom 1.9.0, systemd-oomd state, and four startup thresholds; counts current-invocation send/escalation/failed-kill/low-memory log lines and this-boot oomd notices; returns KILLER_ACTED/KILLERS_UNKNOWN/KILLERS_QUIET. 32/32 covers pre-freeze cases only; A2 lacks case file; counts are log lines, not processes. | `tools/mori-oom-killers.py` | 26 |
Citations: MANIFEST.json:13722; .ufo/reports/round-26/mori.md:61; corpus/lessons/round-26-verifier-spotcheck.md:93,103-117.
Selected path: `tools/mori-oom-killers.py` is the strongest single artifact because the closure's C2 check names it and verifies its frozen-case evidence (corpus/lessons/round-26-verifier-spotcheck.md:93,103-107).
VERDICT: rounds[462].capabilities_added[0] supported — the fleet report records a live current-invocation result, KILLERS_QUIET (.ufo/reports/round-26/mori.md:61); the 32/32 case result was evidence-verified, not rerun (corpus/lessons/round-26-verifier-spotcheck.md:93,103-117).
```

The row's behavior and limitations are verbatim in scope of the frozen capability string (MANIFEST.json:13722). The spot-check bounds PASS 32/32 to pre-freeze cases and says amendment-A2 rules have no committed case file (corpus/lessons/round-26-verifier-spotcheck.md:110-117). The fleet report's live result is distinct from that selftest evidence (.ufo/reports/round-26/mori.md:59-64).

## Candidate path gate

The read-only command below checked the counter's candidate conditions. Its output was: lane HEAD `913df22e29f131ef9cb5de9dcb7e3e272256c5f0`; candidate at tip `yes`; candidate at closure `yes`; diff status `A tools/mori-oom-killers.py`; closure blob `3fb78bbc2612c38e463e04083bdb213954647568`.

```sh
timeout 120 bash -c 'set -euo pipefail; r=/home/vgpnk/Projects/shokunin/mori-shokunin; printf "lane HEAD: "; git -C "$r" rev-parse HEAD; printf "candidate at tip: "; git -C "$r" cat-file -e HEAD:tools/mori-oom-killers.py && printf "yes\n"; printf "candidate at closure: "; git -C "$r" cat-file -e ef9dbee136d6ed2ef98687f5cb0c0a16506a5155:tools/mori-oom-killers.py && printf "yes\n"; printf "change from previous closure to target:\n"; git -C "$r" diff --no-ext-diff --name-status 829d8c9072d5907b9050d06c16cc34b0bb73d0f8 ef9dbee136d6ed2ef98687f5cb0c0a16506a5155 -- tools/mori-oom-killers.py; printf "blob at closure: "; git -C "$r" rev-parse ef9dbee136d6ed2ef98687f5cb0c0a16506a5155:tools/mori-oom-killers.py'
```

The path equals the path named by the capability and appears as a whole path in the closure evidence: MANIFEST.json:13722, the spot-check at lines 93-107, and fleet report lines 13-14. It is under `tools/`, exists at both required revisions, and was added between the previous and target mori closures. The source describes a read-only survey and live collection (tools/mori-oom-killers.py:2-7,567-575).

## Provenance and gates

- Timestamp command: `timeout 120 date -u +%FT%TZ` → `2026-10-23T08:52:12Z`.
- Read-only source snapshots: lane spot-check `git show fc09f96c8036094bef06370dbb4b436edf96e6e3:corpus/lessons/round-26-verifier-spotcheck.md`; fleet manifest and report `git show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json` and `git show 37b51a243302e8009c7067431e8a47f9a722fd14:.ufo/reports/round-26/mori.md`; lane artifact `git show ef9dbee136d6ed2ef98687f5cb0c0a16506a5155:tools/mori-oom-killers.py`. Manifest identifies round 26 at `rounds[462]`, the spot-check commit, and closure commit (MANIFEST.json:13721-13730).
- Initial lookup outcomes: the spot-check was not present at the closure commit (`git -C /home/vgpnk/Projects/shokunin/mori-shokunin show ef9dbee136d6ed2ef98687f5cb0c0a16506a5155:corpus/lessons/round-26-verifier-spotcheck.md` returned `fatal: path 'corpus/lessons/round-26-verifier-spotcheck.md' exists on disk, but not in 'ef9dbee136d6ed2ef98687f5cb0c0a16506a5155'`); it was then read at the manifest's fc09f96c8036094bef06370dbb4b436edf96e6e3 commit. Looking for `MANIFEST.json` with `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json` returned `fatal: path 'MANIFEST.json' does not exist in '37b51a243302e8009c7067431e8a47f9a722fd14'`; the corrected read used the fleet repo root.
- Captured source files were kept only under `/fast/scratch/hyaku/mori-r35/RowR26/`: `MANIFEST.json`, `fleet-report.md`, `spotcheck.md`, and `mori-oom-killers.py`. Read ranges included manifest lines 13720-13738, spot-check lines 1-183 and 93-117, fleet report lines 1-109 and 59-64, and tool lines 1-183, 240-458, and 491-575.
- No counter, selftest, or tool execution was performed for this finding. The cited closure itself says the 32/32 result was evidence-verified, not executed by the closure (MANIFEST.json:13728; spot-check:103-117); the live `KILLERS_QUIET` result is recorded in the fleet report (line 61).
- No tool installs. No product, manifest, fleet report, or lane Git state was changed; this report is the only write in the lane.

## Touched surfaces and limits

- Lane write: `.ufo/waves/round-35/w1/RowR26.md` only. Scratch reads: `/fast/scratch/hyaku/mori-r35/RowR26/` as listed above.
- Out of scope: editing SCORECARD.md or product code, changing frozen claims, running gates/tests, or modifying Git state. The report is a draft for the L1 integration owner, not a lane commit.
- Artifact: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/w1/RowR26.md`.
