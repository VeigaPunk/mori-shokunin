# Seat Mo49ConnPriorRounds — recurrence scan across the lane's own history

Report: `.ufo/waves/round-49/w1/Mo49ConnPriorRounds.md`

Seat `Mo49ConnPriorRounds` (leaf; no subagents). Lane: mori-shokunin. Round: 49, wave w1.
Method: read-only. Read: `corpus/lessons/round-{45,46,47,48}-verifier-spotcheck.md` and the
`## Mistakes` tables of `corpus/lessons/round-{45,46,47,48}.md`; `corpus/QUALITY.md` criteria
40/123/124; the frozen `.ufo/waves/round-49/contract.md`; committed receipts under
`.ufo/waves/round-{47,48,49}/evidence/` checked with plain `grep`/`ls` (commands and outputs in §4).
No lane tool was executed; nothing was written outside this report. Lines cited are the lines read at
the current working tree (the lane tip `b3e3453d` entering round 49).

## 1. Mistake classes by round

| Class | round 45 | round 46 | round 47 | round 48 | Recurred after a criterion/fix claimed to capture it? |
|---|---|---|---|---|---|
| Harness leak / counter survivor (a check reads text, not semantics; false green; over/under-accept) | M1, M2, M3, M4, M5, M6 (`round-45.md:168-173`) | M1 (`round-46.md:10-12`) | M2, M5 (`round-47.md:65,68`) | M2, M3 (`round-48.md:112-113`) | **YES — every round.** QUALITY 40 ("A tally cites the counted universe recomputed…", `QUALITY.md:40-41`) did not catch r46 M1; "A fix is shown able to fail" (CORPUS.md) did not stop r47 M2/M5; QUALITY 123 (`QUALITY.md:1028-1040`) "checked values, not visibility" (r48 M2); v3 R1-R10 still leave D1/D2/D5/D18 green (r48 M3) and 7 of 14 v3 probes green (routed to r49, `round-48.md:163-168`). |
| Number-drift / pins stale (reported count or registry pin ≠ committed bytes) | M10 (`round-45.md:177`); verifier: 29/29 vs 27 OK and four stale registry cells (`round-45-verifier-spotcheck.md:33-37,50-66`) | M2 (`round-46.md:14-18`) | M1 (`round-47.md:64`; receipt `evidence/control-c1-donothing.txt` line 912) | M4 (`round-48.md:114`) | **YES — r47 and r48.** r46's `count-repins.py` substring counter was ruled unprovable (`round-46.md:5-6`; `round-46-verifier-spotcheck.md:71`); pin-check v2 (QUALITY 123) missed truncated-digest pins; v3 R6 caught r48 M4. |
| Attribution / overclaim / misattribution | M7, M9 (`round-45.md:174,176`) | — | M3 (`round-47.md:66`) | M6, M7 (`round-48.md:116-117`) | **YES — r48.** QUALITY 124 (added after r47 M3, `QUALITY.md:1041+`) covers enumerated counts; it did not cover negative claims (M7) or seat identity/output provenance (M6). |
| Scope (edited a tracked file instead of a scratch copy) | — | — | M4 (`round-47.md:67`) | M5 (`round-48.md:115`, "the round-47 M4 class, again") | **YES — once.** Wave-context wording + sha256 compare did not prevent r48 M5. |
| Landing / late files untracked | — | — | verifier §1 defect: 53 untracked paths incl. w2 results (`round-47-verifier-spotcheck.md:20,96`) | M1 (`round-48.md:111`); verifier defect (a): 114 untracked `.scratch/` dirs, same class (`round-48-verifier-spotcheck.md:23-27`) | **YES — r48**, after `mori-unlanded-check.py`; its scope excludes `.scratch`. |
| Id-collision / reservation | M8 (`round-45.md:175`) | — | — | — | no |

## 2. The three highest-recurrence classes

### 2.1 Harness leak / counter survivor — highest recurrence (11 mistake rows across 4 rounds, every round)

- **Criterion that was supposed to catch it:** QUALITY 40 ("A tally cites the counted universe
  recomputed from delivered artifacts at the carrying commit", `QUALITY.md:40-41`) — cited as the
  captured-by for r46 M1 and as "did not catch"; CORPUS.md "A fix is shown able to fail" (captured-by
  for r47 M2/M5, where the v1 selftest had no adversarial-rebinding arm); QUALITY 123
  (`QUALITY.md:1028-1040`, "a registry pin is calibrated only when an instrument re-runs it from
  committed bytes and reads it from its own cell") — captured-by for r48 M2, which states it "checked
  values, not visibility"; the v1→v2→v3 selftest arm sets (R1-R10).
- **Latest recurrence:** r48 M2 (v2 prints `PIN_CHECK=met` on eight structural junk edits —
  `evidence/control-c1-tool-v2-entering.txt`: `junk_met=8`) and r48 M3 (D1/D2/D5/D18 survive the
  spec's R1-R8); carried into r49 as the N1-N9 variants — the freeze do-nothing control
  `evidence/control-c1-tool-v3-entering.txt` still prints `junk_met=9` at the entering tip
  (`contract.md:147`). The F1 form (a tool keyed on the harness's variant filename) scored `C1=met`
  under the r48 counter — `evidence/control-c1-sniffer-under-r48-counter.txt` (`contract.md:150`).
- **What check would have caught the latest recurrence:** score the candidate tool against the junk
  variant set and require zero `junk_met`/`got=met` before any claim — exactly what the r48 wave-1
  critic did for D1/D2/D5/D18 (`w1/CritJunkClasses.md`) and what the r49 counter now does with opaque
  handles. It is a run of the frozen counter, not a new tool.
- **Counting command (one per class):** `grep -h '^C1=' .ufo/waves/round-49/evidence/control-c1-*.txt | grep -cE 'junk_met=[1-9]'`
  → number of control receipts on which the candidate scores junk `met`; non-zero means the class is
  live. Observed now: 5 of 8 r49 controls print `junk_met>=1` (do-nothing 9, surface-fixes 1,
  r11-only 7, stub-always-met 18, stub-filename-sniffer 18) — the class is open at entry by design.

### 2.2 Number-drift / pins stale — second-highest recurrence (4 mistake rows + verifier evidence across 4 rounds)

- **Criterion that was supposed to catch it:** r46's `count-repins.py` (four registry cells) — judged
  unprovable because it matched needles anywhere in a row (`round-46.md:5-6,10-12`); then QUALITY 123 +
  `tools/mori-pin-check.py` v2 (r47 fix, `round-47.md:64`) — which "covers tallies and full digests,
  not truncated ones" (`round-48.md:114`); v3 R6 closed the latest.
- **Latest recurrence:** r48 M4 — `SKILL.md:168` pinned the r14 harness as a sha256 since round 14;
  no file in the tree carries that prefix (whole-tree scan of 12,111 files, `w1/ExecRealRegistryAudit.md`).
- **What check would have caught the latest recurrence:** compare every pinned digest against in-tree
  bytes (or run the reconciler and count mismatch lines); the r47 do-nothing receipt is the in-repo
  proof that this shape is visible (`evidence/control-c1-donothing.txt`: `PIN_CHECK=unmet …
  mismatches=1`, `pin line=912 … state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0'`).
- **Counting command (one per class):** `python3 tools/mori-pin-check.py --rev <tip> --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 | grep -c 'state=mismatch'`
  → mismatched pin lines; must be 0 (was 1 at the r47 tip; found 1 at `e5dbac05` for r48 M4).

### 2.3 Attribution / overclaim / misattribution — third-highest recurrence (5 rows across 3 rounds)

- **Criterion that was supposed to catch it:** QUALITY 124 ("A stated count of kernel objects carries
  the enumerating command over a pinned source", `QUALITY.md:1041+`, added after r47 M3); plus the
  source-census/quote-location machinery for admits.
- **Latest recurrence:** r48 M6 (eight wave-1 results carried other lanes' seats of the same name;
  `w1-results.json` — names only a round/lane, no report under `w1/`) and r48 M7 (a negative claim
  "absent from the Aliyun copy" searched the raw HTML — with tag-split words — not the normalised text
  the counter uses; the copy holds it at offset 5042). The w2 erratum corrected the mechanism: the raw
  bytes contain the text contiguously at offsets 26626 and 81461 (`round-48.md:150-151`).
- **What check would have caught the latest recurrence:** for M7, search the exact copy the counter
  consumes; for M6, verify each wave report's identity against the dispatch (unique seat names per
  round/lane — already a routed defect for r49, `contract.md:133`).
- **Counting command (one per class):** `grep -c 'Disk quota exceeded' corpus/evidence/sources-r48/aliyun-nas-quota.html`
  → 2 (observed), disproving the negative claim. (M6 counting: `find .ufo/waves/round-49/w1 -type f -name '*.md' | wc -l`
  vs spawned seats; r48's wave-1 accounting did this: 49 spawned, 39 reported, `round-48.md:140-142`.)

### Runner-up (named in the round prompt's examples): late files untracked

- Occurred r47 (53 untracked paths incl. w2 results, `round-47-verifier-spotcheck.md:20,96`); fix
  claimed r48 M1 (`mori-unlanded-check.py`); recurred in weaker form at r48 end (114 untracked
  `.scratch/` dirs — the check's scope excludes `.scratch`, `round-48-verifier-spotcheck.md:23-27`).
  The r49 contract carries the cleanup + `.gitignore` entry (`contract.md:133-134`).
- Counting command: `git status --porcelain | wc -l` → non-zero untracked/modified leftovers at the
  integrating tip (was 53 at r47, 114 at r48).

## 3. Counting commands (one per class)

| Class | Counting command | Signal |
|---|---|---|
| harness leak / survivor | `grep -h '^C1=' .ufo/waves/round-49/evidence/control-c1-*.txt | grep -cE 'junk_met=[1-9]'` | 0 after a fix (observed 5 at freeze) |
| number-drift / pins stale | `python3 tools/mori-pin-check.py --rev <tip> --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 | grep -c 'state=mismatch'` | 0 (was 1 at r47 tip; r48 M4) |
| attribution / overclaim | `grep -c 'Disk quota exceeded' corpus/evidence/sources-r48/aliyun-nas-quota.html` | ≥1 disproves the negative claim (observed 2) |
| late files untracked | `git status --porcelain | wc -l` | 0 at the integrating tip (was 53/114) |

## 4. Observed evidence (read-only commands run this seat)

```
$ ls .ufo/waves/round-49/evidence/ | grep -E 'control-c1|sniffer'
control-c1-sniffer-under-r48-counter.txt
control-c1-stub-always-met.txt
control-c1-stub-always-unmet.txt
control-c1-stub-filename-sniffer.txt
control-c1-tool-r48-merged-witness.txt
control-c1-tool-r48-r11-only.txt
control-c1-tool-r48-surface-fixes.txt
control-c1-tool-v3-entering.txt

$ grep -h '^C1=' .ufo/waves/round-49/evidence/control-c1-*.txt | sort | uniq -c
      1 C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=b3e3453d…
      1 C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…
      1 C1=unmet junk_met=0 honest_unmet=8 real=unmet errors=0 variants=26 rev=b3e3453d…
      2 C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…
      1 C1=unmet junk_met=1 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…
      1 C1=unmet junk_met=7 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…
      1 C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…

$ grep -E '^PIN_CHECK=' .ufo/waves/round-47/evidence/control-c1-donothing.txt
PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33d… baseline=yes

$ grep -E 'line=912|MORI_SOURCES_APPENDONLY' .ufo/waves/round-47/evidence/control-c1-donothing.txt
pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 2d85e33d… --selftest'

$ grep -c 'Disk quota exceeded' corpus/evidence/sources-r48/aliyun-nas-quota.html
2
```

UNVERIFIED: `w2/R48CritV3Junk1.md` was not opened by this seat; its seven surviving shapes are
recorded here as the r49 N1-N7 variants from the contract (`contract.md:19-21,34-44`) and the r48
lesson (`round-48.md:163-168`). The r49 counter's own ~10-minute run was not executed (frozen
receipts read instead).

## Findings

- **HIGH** — Harness-leak/counter-survivor class recurred in every round since 45 despite a fresh
  criterion each time (QUALITY 40, "A fix is shown able to fail", QUALITY 123, v1→v3 selftest arms).
  Latest: r48 M2/M3; live at r49 entry (freeze do-nothing prints `junk_met=9`). Concerns
  `round-48.md:112-113`; `contract.md:147-151`; `QUALITY.md:40,1028-1040`.
- **HIGH** — Number-drift/pins-stale class recurred at r47 and r48 after criteria claimed to capture it
  (`count-repins.py` judged unprovable; pin-check v2 missed truncated digests). Latest: r48 M4
  (`SKILL.md:168`). Concerns `round-47.md:64`, `round-48.md:114`, `round-46.md:5-6,10-12`,
  `evidence/control-c1-donothing.txt` (line 912).
- **MED** — Attribution/overclaim recurred at r48 (M6/M7) after QUALITY 124 was added post-r47-M3;
  the negative-claim and seat-identity forms were uncovered. Concerns `round-48.md:116-117`;
  `QUALITY.md:1041+`.
- **MED** — Late-files-untracked class persists across rounds: r47 w2 results untracked → r48 M1 fix
  (`mori-unlanded-check.py`) → r48 end still 114 untracked `.scratch/` dirs because the check excludes
  `.scratch`. Concerns `round-47-verifier-spotcheck.md:20,96`, `round-48.md:111`,
  `round-48-verifier-spotcheck.md:23-27`, `contract.md:133-134`.
- **LOW** — Scope class (editing tracked `tools/` files) recurred once (r47 M4 → r48 M5); the r48
  counter-measure (unlanded-check listing modified `tools/` + frozen-sha256 compare before integration)
  still leaves an edit-and-restore-between-two-runs gap. Concerns `round-47.md:67`, `round-48.md:115`.
