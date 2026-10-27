# Mo53ScribeScorecard — SCORECARD.md additions for round 53 (fenced drafts, not applied)

Seat: scribe, wave w1, round 53. Lane: mori-shokunin. Report path relative to
`/home/vgpnk/Projects/shokunin/mori-shokunin`. I wrote no lane file except this report; both drafts below are
verbatim blocks the L1 integrates.

## What I read (read-only)

| # | Command | Result |
|---|---|---|
| 1 | `read .ufo/waves/round-53/contract.md` | C1 (freshness) / C2 (coverage), P-C1 and P-C2, kill rules, controls, separability, round-52 routed defects 1–3 |
| 2 | `grep -n "^## " SCORECARD.md` (`wc -l` = 2771) | round-52 section is lines 2737–2771; last section of the file |
| 3 | `sed -n '2737,2771p' SCORECARD.md` | house shape of the round-52 section: header line, claim table with the columns Claim, Axis (held), Counting command, Before, After; then the controls paragraph, the capability paragraph, the limits paragraph and `Planned (round 53)` |
| 4 | `sed -n '1950,1988p' SCORECARD.md` | capabilities register table (5 columns ending `first-working round`), rows `rounds[313]`–`rounds[495]` (rounds 12–31) |
| 5 | `sed -n '1536,1576p' SCORECARD.md`, plus `grep -n "correction" SCORECARD.md` (which printed line 2309) | `### capabilities: first demonstrated round NN` subsection shape used by rounds 24, 25, 41 (4 columns: capability, what it can do, evidence, round) |
| 6 | `sed -n '2656,2706p' SCORECARD.md`, then `sed -n '2706,2740p'` | round-50 and round-51 sections (entry line, claim table, controls, "No capability row is claimed", limits, `Planned`) |
| 7 | `grep -n "correction" SCORECARD.md` | append-only correction precedents: `:1716`, `:1853` (r31 tip-receipt correction bullet), `:2179`, `:2189`, `:2272`, `:2383` |
| 8 | `sed -n '118,135p' corpus/lessons/round-52-verifier-spotcheck.md`, then `sed -n '20,45p'` of the same file | routed defect 1 (append-only correction naming the superseded line), routed defect 3 (the three standing limits, "carried in `Planned (round 53)`" per the contract), and D2 (the `items=42 … locators=27` vs `43/28` attribution) |
| 9 | `grep -n "^C1=" .ufo/waves/round-52/evidence/c1-at-data.txt .ufo/waves/round-52/evidence/c1-at-landed.txt` | at-data `:44` `items=42 … locators=27 … rev=8524904adb25e44f24d9f25aac7eae909625c18c`; at-landed `:45` `items=43 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=28 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=e7e056b8a17e54516a3c17798221c30e9902c250` |
| 10 | `tail -4` of `.ufo/waves/round-53/evidence/{control-c1-do-nothing,c1-at-data,control-c2-do-nothing,c2-at-data,selftest-c1,selftest-c2,census-start}.txt` | C1 before/at-data, C2 before/at-data, selftest tallies, census rc 0 with 23 W04 (quoted in the drafts) |
| 11 | `for f in control-c1-{all-held,v72-copies,no-votes,witness}.txt control-c2-{mode-blind,no-band,memoriser,witness}.txt; grep -E '^(C1=|C2=|exit=)'` | control readings (agree/disagree, failed= lists) reproduced in the controls draft |
| 12 | `ls .ufo/waves/round-53/controls` | `c1-data.py`, `controls.py` — the witness builders the contract names |
| 13 | `sed -n '1,40p' .ufo/waves/round-53/count-c1.py`, `sed -n '1,45p' count-c2.py` | both docstring predicates and both named-limit lists (source of the limits draft) |
| 14 | `grep -n "Round53" -A 12 SKILL.md` | `## Round53` decision table and `Round53 registry additions` row (23 cases, `PASS 23/23`) |
| 15 | `sed -n '1,5p' corpus/knowledge/commit-runway-read-r53.md` | entry header: `source:` S499, S511, S512… (S511–S513 rows) |
| 16 | `cat .ufo/waves/round-53/evidence/selftests/mori-commit-runway.txt` | `MATCHER: rejected 23/23 corrupted expectations` / `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23` / `exit=0`, run from a git archive of the data commit |
| 17 | `git rev-parse HEAD`; `git log --oneline -4` (read-only) | HEAD `95cf78eef71979f9b740ef6bc3c5299b6beff86e` (w1 spec); `2a4213bf` data; `f4da3fd4` freeze; `20edafa5` entering tip |
| 18 | `wc -l .ufo/waves/round-53/evidence/freeze-sha256.txt` | 33 frozen prefixes |

Live tool runs I executed myself (both read-only, no writes; no scratch needed):

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 -I -B tools/mori-commit-runway.py --selftest
MATCHER: rejected 23/23 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23
$ echo $?
0

$ python3 -I -B tools/mori-commit-runway.py
{"band_kb": null, "batch_pages": null, "commit_limit_kb": 47583772, "committed_as_kb": 37388200,
 "cpus_present": 32, "enforced": false, "findings": [], "headroom_kb": 10195572,
 "limit_consistent": true, "limit_recomputed_kb": 47583772, "mode": 0,
 "notes": ["mode 0 (guess): only a single request above RAM + swap is refused; CommitLimit is printed, not enforced"],
 "reserve_kb": null, "schema": "mori-commit-runway-v1", "single_request_cap_kb": 63444672,
 "usable_kb": null, "verdict": "COMMIT_HEURISTIC"}
$ echo $?
0
```

Consequence for the drafts: this host reads mode 0, so the mode-2 band — the round's novelty — has no live leg here;
the fixtures and the counter's REF carry it (stated in the limits draft, finding F3).

Scratch: I created no clone and no temp file, so `/fast/scratch/hyaku/mori-r53/Mo53ScribeScorecard/` was never
needed and nothing is left behind. No tool installed or upgraded. No network fetch. No credential material.

I did not run either counter (the L1's data receipts are the evidence I quote); I did not edit any lane file.

---

## Draft 1 — appended at the end of the `## Round 52` section, immediately before the new `## Round 53` heading

Placement reason: the corrected row is `SCORECARD.md:2746`; the house precedent for an append-only correction that
names superseded text is a heading-free paragraph or bullet right after the affected table (`:1855` bullet,
`:2179`/`:2189` subsections, `:2383` standalone line). Keeping it inside the round-52 section leaves the round-53
section terminal.

```markdown
**Round-52 correction:** the round-52 C1 row's After cell above carries the superseded tally `items=42 axes=6
pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0` and must be read as
`items=43 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=28 mismatches=0 errors=0 hidden=0 lane_writes=0`. The
receipt that row cites (`.ufo/waves/round-52/evidence/c1-at-landed.txt:45`, measured
`e7e056b8a17e54516a3c17798221c30e9902c250`) prints the 43/28 form with `manifest=6209bdb8e400`, rc 0; the two
superseded tokens are verbatim the at-data tally (`evidence/c1-at-data.txt:44`, measured
`8524904adb25e44f24d9f25aac7eae909625c18c`), written before the landed receipt existed. Every other token, the
`C1=met` verdict and the exit code agree; the row above is retained as filed (append-only, round-52 closure D2).
```

---

## Draft 2 — the `## Round 53` section, appended after Draft 1

```markdown
## Round 53 — the release-pinned quotes re-verified at Linux v7.3 (C1) and the commit ledger as a runway read (C2)

L1 MoriR53, attempt 1. Entering tip `20edafa59b38dac1ca358893f0259b1f436372d3` (round-52 verifier spot-check);
freeze `f4da3fd400fa88a6db8ea544a4f7045c15d2410e` (`.ufo/waves/round-53/contract.md`; both counters, the controls,
the receipts, both counter selftests, census-start, the sweeps and the twelve source copies); data
`2a4213bf8da72f7cd78189ba5bb9be825dca1df`. Scores entering: coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6; C1 works a lowest (tied 5) axis and C2 is a coverage move with a capability row. No
score change is claimed by the lane; the non-author closure rules.

| Claim | Axis (held) | Counting command | Before | After |
|---|---|---|---|---|
| C1 the release-pinned located-quote claims of `memavailable-estimate-r51.md` and `overcommit-commit-limit-r52.md` re-verified at Linux v7.3: one ledger row per claim hash (46), each with a v7.3 source row, a located v7.3 quote and a `holds`/`changed` disposition, and two RECHECK voters per row whose final line carries that disposition, neither a proposer of the row's quote | freshness 5 | `python3 .ufo/waves/round-53/count-c1.py R` | `C1=unmet scope=46 rows=0 matched=0 status_ok=0 quote_ok=0 source_rows=bad pins=bad provenance=bad held=0 absent=0 holds=0 changed=0 voted=0 dissent=0 … failed=ledger_absent,pins`, rc 1 — `evidence/control-c1-do-nothing.txt` | [L1 fills — paste `evidence/c1-at-landed.txt` verbatim; target tokens `C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0`, rc 0]. The data commit before any vote read `… voted=0 dissent=0 … failed=votes`, rc 1 — `evidence/c1-at-data.txt` |
| C2 the commit ledger (`CommitLimit` / `Committed_AS`) as a runway surface `tools/mori-commit-runway.py` reads by overcommit mode, with the mode-2 per-CPU error band and a `--selftest` over its own fixtures | coverage 6 | `python3 .ufo/waves/round-53/count-c2.py R [--scratch DIR]` | `C2=unmet tool=absent selftest=error n=0 fixtures=80 agree=0 disagree=0 registry=bad live=error failed=registry,tool_absent`, rc 1 — `evidence/control-c2-do-nothing.txt` | [L1 fills — paste `evidence/c2-at-landed.txt` verbatim; target tokens `C2=met tool=present selftest=pass n≥12 fixtures=80 agree=80 disagree=0 registry=ok live=ok`, rc 0]. The data commit read `n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok`, rc 0 — `evidence/c2-at-data.txt` |

The C1 landing is `corpus/knowledge/kernel-v7.3-recheck-r53.md` with rows S502–S510 and the nine pinned v7.3 copies
under `corpus/evidence/sources-r53/`. The C2 landing is `tools/mori-commit-runway.py` with
`tools/fixtures/mori-commit-runway/cases.json` (23 cases), the `## Round53` registry row in `SKILL.md`, the band
entry `corpus/knowledge/commit-runway-read-r53.md` and rows S511–S513.

Controls that skip the work stay unmet (receipts under `.ufo/waves/round-53/evidence/`, readings in the table at the
end of the contract): C1 do-nothing `rows=0 … pins=bad … failed=ledger_absent,pins`; all-held
`status_ok=44 quote_ok=44 … voted=46 dissent=0`, `failed=quote,status` — labelling everything held fails exactly the
two MAP_NORESERVE rows; v72-copies `held=46 absent=0 … pins=bad`, `failed=pins,quote,status`; no-votes
`status_ok=46 quote_ok=46 … voted=0`, `failed=votes`; the witness (feasibility only, built by the L1 with
`controls/c1-data.py`) met. C2 do-nothing `tool=absent … failed=registry,tool_absent`; mode-blind
`agree=53 disagree=27`, `failed=fixtures`; no-band `agree=71 disagree=9`; memoriser `agree=71 disagree=9`, exact on
the frozen 16 and wrong on the seeded near-edge cases (the counter's own junk tools print a fake `PASS 12/12`
selftest, so the fixture arm is what separates them); the witness (the counter's REF wrapped as a tool, `n=12` at the
floor) met, disclosed. Counter selftests `C1_SELFTEST pass=37 fail=0` and `C2_SELFTEST pass=30 fail=0`
(`evidence/selftest-c1.txt`, `evidence/selftest-c2.txt`).

### capabilities: first demonstrated round 53

Capability rows (demonstrated running this round; the closure admits them, and the register's `key` cell is filled
then — the round-41 shape):

| key | name | what it can now do | evidence | first working |
|---|---|---|---|---|
| round-53 C2 | commit runway read by overcommit mode | Reads `CommitLimit` and `Committed_AS` from `/proc/meminfo`, five `/proc/sys/vm` files, the present-CPU mask and the page size, and prints one `mori-commit-runway-v1` JSON object whose verdict follows the mode: `COMMIT_HEURISTIC` (mode 0 — only a single request above RAM+swap is refused, `single_request_cap_kb`, never LOW), `COMMIT_UNLIMITED` (mode 1, never LOW), `COMMIT_OK` / `COMMIT_LOW` (mode 2 — LOW iff `usable_kb` = limit − committed − `admin_reserve_kbytes` − `user_reserve_kbytes` is at or below `band_kb` = batch × present CPUs × page, batch = `max(min(ram_pages/cpus/256, INT_MAX), max(2×cpus, 32))`), `COMMIT_UNKNOWN` (exit 2) when an input is missing, unreadable or malformed or the mode is outside 0–2; recomputes the limit and reports `limit_consistent`; read-only, writes nothing. Not a calibrated alarm (`COMMIT_LOW` means "inside the counter's own error band"; FR8 stays open) and no cgroup-level commit, because there is none | `python3 -I -B tools/mori-commit-runway.py --selftest` → `MATCHER: rejected 23/23 corrupted expectations`, `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23`, exit 0, from a git archive of the data commit (`evidence/selftests/mori-commit-runway.txt`); fixtures `tools/fixtures/mori-commit-runway/cases.json`; counter agreement `fixtures=80 agree=80 disagree=0` (`evidence/c2-at-data.txt`); live host read `{"mode": 0, "verdict": "COMMIT_HEURISTIC", "commit_limit_kb": 47583772, "committed_as_kb": 37388200, "limit_consistent": true, "cpus_present": 32}`, exit 0 | 53 |

Limits named before data (the wave's own findings land in `corpus/lessons/round-53.md` `## Wave w1 — integrated
findings`): `held` proves the v7.2 quote's words still occur somewhere in the v7.3 file, not at the same place nor
with the same meaning — the disposition and its two votes carry the meaning; the vote arm proves two lane seats
recorded a judgment, not outside verification, and a vote records a judgment, not its correctness; D covers the
claim tables of the two entries only (46 rows), not `oom-tracepoints-r47.md` (whose recheck is `90d`), the round-50
memcg entry, prose outside the tables or the SOURCES anchors; the v7.3 copies were fetched from git.kernel.org cgit
and their sha256 pins prove the bytes are what the L1 fetched, not that cgit served the tag; C2's REF function and
the tool share one author, so a shared misreading of the kernel passes both; the band is an upper bound from the
batch rule with present CPUs and totalram at read time, not a measured deviation; the 64 seeded fixtures are
derivable from the data commit's id, so a tool written after it could memorise them; the live leg compares stable
fields only and depends on the host — this host reads mode 0, so the mode-2 band arm is exercised by fixtures, not
live; `RECHECK` voters are seats of the lane, not a second lane's verdict. Counter weaknesses the wave names are
routed for round 54 and were not fixed in-round (frozen bytes).

Planned (round 54): the round-52 standing limits carried in as routed defect 3 — the locator arm's scope
(`QUALITY.md` and `README.md` hold 78 pointers it does not read), receipts that are pure text, and arm A's verdict
pinned only to `admitted`; the v7.3 trigger for what D does not cover (`oom-tracepoints-r47.md` at its 90-day
recheck, the round-50 memcg entry, the SOURCES anchors); C1 depth — a `held` row that pins place and meaning rather
than the presence of words, and a voter set wider than the lane's own twelve seats; C2's shared-author arm — an
independent re-derivation of the band from the committed v7.2 copies by a seat that did not write REF, and a mode-2
live leg on a host whose `vm.overcommit_memory` is 2; FR8's calibrated `COMMIT_LOW` threshold, which needs measured
refusal behaviour and is not a counter change; the counter weaknesses routed from wave w1.
```

---

## Findings

- **LOW — `SCORECARD.md:2746` (round-52 C1 After cell):** records `items=42 … locators=27` while citing
  `evidence/c1-at-landed.txt`, whose line 45 prints `items=43 … locators=28` at
  `e7e056b8a17e54516a3c17798221c30e9902c250`. Both receipts print `C1=met … mismatches=0 errors=0`, rc 0, so the
  verdict is unaffected; the numbers are the at-data tally (`c1-at-data.txt:44`). Draft 1 is the append-only fix.
- **LOW — `SCORECARD.md:1969-1988` (capabilities register):** the register's newest row is `rounds[495]`
  (round 31), because rows enter only through an admitted closure that records the key; later rounds that
  demonstrated a capability put a round-local `Capability rows (demonstrated running this round; closure admits
  them):` table in the register's own 5-column shape (`SCORECARD.md:2305-2310`, round 41, keys `round-41 C1`–`C3`).
  Draft 2 follows that precedent, so the register stays a closure-driven artifact and the L1 moves the row (or
  records the MANIFEST key) after admission.
- **MED — the mode-2 band has no live leg on this host:** `python3 -I -B tools/mori-commit-runway.py` reads
  `mode: 0`, `COMMIT_HEURISTIC`, exit 0, so `band_kb = null` and the round's new rule (LOW iff `usable_kb ≤ band_kb`)
  is proven only by fixtures and the counter's REF at `2a4213bf`. There is no synthetic mode-2 host read without
  writing a sysctl, which the lane forbids; the limits paragraph states it.
- **LOW — the C2 control witness prints `n=12`, the landed tool `n=23`:** the floor is 12 (`MIN_SELFTEST`), so a
  witness at the floor shows feasibility, not the landed tool's case count. The contract discloses both; Draft 2
  labels the witness accordingly so the row cannot be read as the landed self-test tally.
- **LOW — the corrections' placement is load-bearing:** appending the correction as its own `## Round-52
  correction` heading after the round-52 section would make the round-52 section non-terminal and put a heading
  between the row and the round-53 section; Draft 1 keeps it as a paragraph inside the round-52 section, matching
  `SCORECARD.md:1853-1855`, `:2179`, `:2383`.
