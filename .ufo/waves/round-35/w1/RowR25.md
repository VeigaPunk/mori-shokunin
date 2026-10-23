measured 2026-10-23T08:52:05Z

# Round 25 capability-register findings

Scope: rows `rounds[455].capabilities_added[0]` and `[1]`, evaluated against fleet commit `37b51a243302e8009c7067431e8a47f9a722fd14`, lane closure `829d8c9072d5907b9050d06c16cc34b0bb73d0f8`, and previous mori closure `4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e`.

## Draft rows

ROW: | rounds[455].capabilities_added[0] | Routed-defect and Axes check | Checks D1–D3 and D5 from git objects plus D4 hygiene; lane report records 4/4 held at two revisions, while closure remeasured 4→0 by plain git/Python; no selftest or registry row. | `tools/mori-routed-r24.py` | 25 |
Citations: `MANIFEST.json@37b51a24:13432,13435-13438`; `.ufo/reports/round-25/mori.md@37b51a24:33-38`; `corpus/lessons/round-25-verifier-spotcheck.md@248408f5:11-17,34-36,42-53`; `tools/mori-routed-r24.py@829d8c90:2-13,14-65`.
Path rationale: `tools/mori-routed-r24.py` is the best single path because the fleet report records that command and its exit-0 4/4 result at two revisions (`.ufo/reports/round-25/mori.md:33-35`).
VERDICT: supported — the lane report records the checker run; the verifier itself did not execute the tool and independently remeasured the result using plain git/Python reads (`corpus/lessons/round-25-verifier-spotcheck.md:11-17,42-53`).

ROW: | rounds[455].capabilities_added[1] | Background-job runway read | Reads one settings file and binary for configured cap, clamp/default, effective cap and verdict, not live job count; evidence records PASS 21/21, a block-style host RUNWAY_CLAMPED effective 100, and noncommitted probe with 72/307 false 100s. | `tools/mori-job-runway.py` | 25 |
Citations: `MANIFEST.json@37b51a24:13431,13435-13438`; `.ufo/reports/round-25/mori.md@37b51a24:39-41`; `corpus/lessons/round-25-verifier-spotcheck.md@248408f5:64-88`; `tools/mori-job-runway.py@829d8c90:12-16,18-47,77-81`.
Path rationale: `tools/mori-job-runway.py` is the best single path because the fleet report records its frozen selftest and live-run results (`.ufo/reports/round-25/mori.md:39-41`; spot-check `corpus/lessons/round-25-verifier-spotcheck.md:64-72`).
VERDICT: supported — the selftest is evidence-verified, not rerun by the verifier; the live run and block-style boundary are recorded, while the 72/307 probe count is evidence-cited and not re-derived (`MANIFEST.json@37b51a24:13431,13438`; spot-check `corpus/lessons/round-25-verifier-spotcheck.md:64-82`).

## Evidence and path qualification

- The frozen manifest record names both candidate paths in its capability strings and identifies the closure report and verifier spot-check (`MANIFEST.json@37b51a24:13431-13438`).
- Read each candidate from the closure commit. The runway tool describes reading one config and one binary, computing configured/clamp/default/effective/verdict, and bounds its scope to those files (`tools/mori-job-runway.py@829d8c90:12-16,18-47`). Its docstring says it reports the cap, not the live running-job count (`tools/mori-job-runway.py@829d8c90:77-81`). The routed checker describes read-only git-object checks and the counted D1-D5 plus hygiene predicates (`tools/mori-routed-r24.py@829d8c90:2-13,14-65`).
- Both files exist at closure and at observed lane tip `913df22e29f131ef9cb5de9dcb7e3e272256c5f0`; each was added between previous closure and round-25 closure. The successful `cat-file -e` reads emitted no errors; `git diff --name-status 4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e 829d8c9072d5907b9050d06c16cc34b0bb73d0f8 -- <candidate>` returned `A <candidate>` for both. Each path is under `tools/`, exactly matches its capability string, and appears in the frozen report and manifest.
- C1 execution evidence is specifically the lane report: it gives the checker command and exit-0 result at `e06d4a02` and `e0e33c11` (`.ufo/reports/round-25/mori.md:33-38`). The verifier says its own closure measurement was plain git/Python over blobs, not a lane tool run (`corpus/lessons/round-25-verifier-spotcheck.md:11-17`). The routed checker still had no registry row or selftest (`corpus/lessons/round-25-verifier-spotcheck.md:33-36`).
- C2 closure evidence says the frozen 21-case output was evidence-verified, not rerun; its live run returned `RUNWAY_CLAMPED` at effective 100. The 72/307 false-100 probe is explicitly not independently re-derived because its probe script was not committed; the tool's admitted boundary is block-style config (`corpus/lessons/round-25-verifier-spotcheck.md:64-88`).

## Commands, outcomes, and provenance

Commands were bounded by `timeout 120s` and shell virtual-memory limits (256 or 512 MiB); no background jobs were started.

- `timeout 120s bash -c 'ulimit -v 262144; date -u +%FT%TZ'` → `2026-10-23T08:52:05Z`.
- Initial manifest lookup used the lane repository by mistake: `timeout 120s bash -c 'ulimit -v 524288; set -o pipefail; git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json | jq ".rounds[455]"'` → `fatal: path 'MANIFEST.json' does not exist`. Corrected command: `timeout 120s bash -c 'ulimit -v 524288; set -o pipefail; git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json | jq ".rounds[455]"'` → round 25, admitted, both capability strings, verification summary, report path, and closure commit. `git show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json` was also numbered in memory for frozen lines 13431-13438.
- Read-only artifact commands: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 829d8c9072d5907b9050d06c16cc34b0bb73d0f8:tools/mori-job-runway.py | nl -ba`; same command with `tools/mori-routed-r24.py`; `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 248408f5b6610a85bcbdebe7ac0b4fa7ed51422a:corpus/lessons/round-25-verifier-spotcheck.md | nl -ba`; and `git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:.ufo/reports/round-25/mori.md | nl -ba`. Each returned the named committed artifact; lines cited above.
- Lane source checks (run under `timeout 120s`, `ulimit -v 524288`) observed `HEAD` `913df22e29f131ef9cb5de9dcb7e3e272256c5f0`. For runway: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 829d8c9072d5907b9050d06c16cc34b0bb73d0f8:tools/mori-job-runway.py` and the same command with `HEAD:tools/mori-job-runway.py` both succeeded without output; `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-status 4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e 829d8c9072d5907b9050d06c16cc34b0bb73d0f8 -- tools/mori-job-runway.py` → `A tools/mori-job-runway.py`. The equivalent `cat-file -e` checks for `tools/mori-routed-r24.py` succeeded, and its `diff --name-status ... -- tools/mori-routed-r24.py` → `A tools/mori-routed-r24.py`.
- `git -C /home/vgpnk/Projects/shokunin rev-parse 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json` → `896107926967c0c901327b9d60fdec32d1e014b7`. The current worktree `git hash-object MANIFEST.json` → `64caaeaec70752207f23f428cfc1a6033d3eaddf`; they differ, so citations use the frozen commit object, not the current manifest.
- Bounded report-search pipeline `timeout 120s bash -c 'ulimit -v 524288; set -o pipefail; git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:.ufo/reports/round-25/mori.md | nl -ba | rg "mori-job-runway|mori-routed-r24|routed-r24-after|runway-live-run|PASS 21/21|plain git reads"'` returned cited report lines 9, 14, 33, 35, 37, 39, 40 and 101.

## Gates, surfaces, and limits

- No product code, manifest, verifier, gate, or source artifact was changed. The only file written is this report. No test, gate, build, or selftest was run by this seat; no install or scratch file was made. No Git/JJ write was performed.
- The canonical Rust judge was not invoked or inspected, so no canonical-judge result or conflict is asserted. The lane report records an earlier C1 tool run; the verifier separately states it used plain reads during its closure (`.ufo/reports/round-25/mori.md:33-38`; `corpus/lessons/round-25-verifier-spotcheck.md:11-17`).
- Out of scope: changing either capability string, repairing routed findings R1/R5, adding registry entries or selftests, re-running the historical gates, and editing the fleet manifest/report or lane source.
- Report artifact: `.ufo/waves/round-35/w1/RowR25.md`.
