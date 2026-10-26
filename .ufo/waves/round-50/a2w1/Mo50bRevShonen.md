# Mo50bRevShonen — SHONEN.md review at 487941b (round 50, wave a2w1)

Seat: reviewer, leaf (no subagents). Scope: `SHONEN.md` at `487941b9395e89678af0053cc443cdb49cdee6e3` — (1) the two
tally pins re-run from committed bytes and compared with the receipts; (2) every other pointer in the four boxes
opened at R and judged against its box text. Frozen counters/predicates untouched; no file outside this report
written. No tool installed or upgraded (none needed). No host identifiers, credentials or session URLs below.

Method: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 487941b… | tar -x -C /fast/scratch/hyaku/mori-r50/Mo50bRevShonen/arch`
(one archive, no clone); selftests run inside the extract with `TMPDIR=/fast/scratch/hyaku/mori-r50/Mo50bRevShonen/tmp`.
Line numbers below are from byte-exact greps of the extracted tree at R. Scratch removed at the end of the seat.

## 1. The two tally pins (SHONEN.md line 7, box 3)

Pins as landed: `` `python3 tools/mori-pin-check.py --selftest` (114/114) `` and
`` `python3 tools/mori-unlanded-check.py --selftest` (17/17) ``; both forms are backticked repo-relative
`--selftest` spans directly followed by `(N/M)` — the frozen P-C1(b) shape.

Runs at R (git archive of 487941b, TMPDIR in scratch):

```
$ python3 tools/mori-pin-check.py --selftest
...
PIN_CHECK_SELFTEST pass=114 fail=0
rc=0
$ python3 tools/mori-unlanded-check.py --selftest
...
UNLANDED_SELFTEST pass=17 fail=0
rc=0
```

- Pin 1: `114/114` = pass=114, fail=0 → N=P, M=P+F. MATCH.
- Pin 2: `17/17` = pass=17, fail=0 → N=P, M=P+F. MATCH.

Receipts `.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt` and `mori-unlanded-check.txt`:

- Both tracked at R (`git ls-tree 487941b -- .ufo/waves/round-50/evidence/selftests/` lists both).
- Archive copies byte-identical to the working tree (`cmp` → identical, both files).
- `mori-pin-check.txt` carries `PIN_CHECK_SELFTEST pass=114 fail=0` + `exit=0`; `mori-unlanded-check.txt`
  carries `UNLANDED_SELFTEST pass=17 fail=0` + `exit=0` — the same lines I observed at R.
- Receipt provenance: both headers record `git archive of 950e99be6757a52b00e9eb70ae1a1a7bbe2ea379; TMPDIR=<scratch>;
  2026-10-26T05:49:15-03:00` (and :22). 950e99be is an ancestor of R (`git merge-base --is-ancestor` → yes) and
  `git diff --stat 950e99be 487941b -- tools/` is EMPTY — the instrument bytes that produced the receipts are
  byte-identical to the instruments at R, so the receipts' lines hold for R. Named limit: the equivalence rests on
  that empty tools diff, not on the receipt itself (the receipt names 950e99be, not R); the frozen counter checks
  only that the receipt holds the observed line, which it does.
- No other tally token anywhere else in SHONEN.md at R: the only `--selftest` / `(N/M)` matches in the file are on
  line 7 (box 3). The hidden-scan constraint holds for the current file and for my draft below.

Verdict part 1: both pins are true at R; receipts carry the same lines; pins floor (≥2) and boxes floor (4) met.

## 2. Every other pointer in the four boxes, opened at R

| box | pointer | verdict at R | evidence |
|---|---|---|---|
| 1 | `SKILL.md:941-980` (Round48 section, quota decision row) | ACCURATE — exact | `## Round48 — pin reconciler v3, …` = line 941; `### Decision row — FR2 filesystem quota (round 48)` = 975 with the quota decision row at 979; `## Round49 — …` = 981. The range is exactly the Round48 section including the quota decision row. No drift: SKILL.md is absent from `git diff --stat 7197160b 487941b` (the landing did not touch it). |
| 1 | `corpus/QUALITY.md:1050-1087` | ACCURATE — exact | `## Criteria added round 48 — hidden pins, junk next to honest edits, host paths, a located quote per claim` = line 1050; criteria 125–128 inside; 1088 blank; `## Criteria added round 49 …` = 1089. The range is exactly the round-48 criteria block, each criterion citing its lesson and check. QUALITY.md untouched by the landing. |
| 2 | `LOG.md:2689-2722` (Round 48: FR2 quota entry, pin reconciler v3) | ACCURATE — deliberate two-block span | 2689 = `### Erratum to the round-47 entry above (append-only, 2026-10-25, round 48)`; `## Round 48 (L1 MoriR48; C1 calibration, C2 depth)` = 2700; entry ends `- Wave 1: 49 seats, 39 reports on disk.` = 2722; 2723 blank; `## Round 49 (L1 MoriR49, attempt 1)` = 2724. The range starts exactly at the erratum header and ends exactly at the entry's last line, i.e. all round-48 LOG.md material; the named FR2 quota entry (C2 bullet) and pin reconciler v3 (C1 bullet) are inside. LOG.md is untouched by the landing. A reader wanting only the entry should read 2700-2722 (optional tightening, see findings). |
| 4 | `PROVINCE.md:3-16` unchanged | ACCURATE | 3–16 = `**Domain:**` through `**Detection and report only — never remediation.**` (17 blank, 18 out-of-province line). `git diff 7197160b 487941b -- PROVINCE.md` and `git diff 950e99be 487941b -- PROVINCE.md` both empty; last commit touching PROVINCE.md is `af42101d` (2026-10-22). Content still matches the lane's observed surfaces (watchdog liveness, wave settlement, kill/OOM journals + memory.events, runway, silence grading; detection-only). |
| 4 | `corpus/knowledge/quota-observability-r48.md` Boundaries (read-only, no quota command run) | ACCURATE | `## Boundaries` = line 53; lines 55–56: "**Read-only.** mori observes and reports quota state; it never sets a limit, starts accounting, changes a grace period or runs a repair. No quota command was run against this host for this entry." |
| 4 | `w2/R48ConnSiblings.md` (no contested scope) | **BROKEN as written** | No `w2/` exists at the repo root at R (archive top level has none). Every other pointer in SHONEN.md is repo-root-relative, so the citation does not resolve — the same defect class the lane's QUALITY 108 already names for capability-row paths ("every path … resolves from the repository root at R"). The intended file exists and is tracked at R: `.ufo/waves/round-48/w2/R48ConnSiblings.md`; its verdict line reads "**Verdict: HOLDS — class CLEAN_SEPARATION (zero contested scope, zero duplicate knowledge, zero semantic contradiction)**", which supports the box text. Only the path is wrong. |

## 3. Proposed corrected SHONEN.md (fenced draft)

Minimal diff: box 4's sibling pointer repointed at the tracked path. Every box keeps `[~]`; box 3 (pins + receipts)
byte-unchanged; no tally token added anywhere else.

```markdown
# mori-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:941-980` (Round48 section, quota decision row); `corpus/QUALITY.md:1050-1087`
- [~] At least one end-to-end domain task executed and logged in LOG.md — `LOG.md:2689-2722` (Round 48: FR2 quota entry, pin reconciler v3)
- [~] Instructions executable by an agent without oral context — `python3 tools/mori-pin-check.py --selftest` (114/114); `python3 tools/mori-unlanded-check.py --selftest` (17/17); receipts `.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt`, `.ufo/waves/round-50/evidence/selftests/mori-unlanded-check.txt` (round-50 C1)
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md:3-16` unchanged; `corpus/knowledge/quota-observability-r48.md` Boundaries (read-only, no quota command run); `.ufo/waves/round-48/w2/R48ConnSiblings.md` (no contested scope)
```

The draft contains tally tokens only on the box-3 line, so the counter's hidden scan stays at 0 if applied.

## Findings

- **MED** — `SHONEN.md:8` (box 4): pointer `w2/R48ConnSiblings.md` does not resolve from the repository root at
  `487941b` (no top-level `w2/`); the tracked target is `.ufo/waves/round-48/w2/R48ConnSiblings.md`. Calibration
  defect outside C1's counter (C1 only checks tally pins and the hidden scan); the box's substantive claim ("no
  contested scope") is supported by the target's verdict line. Fix: apply the draft above.
- **LOW** — `SHONEN.md:6` (box 2): `LOG.md:2689-2722` leads with 11 lines of the round-48 erratum to the round-47
  entry (2689–2699) before the Round 48 entry (2700–2722). The named content is inside, so the pointer is not
  stale; optional tightening to `LOG.md:2700-2722` if the box should name the entry alone.
- **LOW (named limit, no fix)** — `.ufo/waves/round-50/evidence/selftests/*.txt`: receipts were produced from a
  `git archive` of the attempt-1 freeze `950e99be`, not of R. Equivalent for R only because
  `git diff 950e99be 487941b -- tools/` is empty (and 950e99be is an ancestor of R); a future reader must redo that
  two-command check, since the receipts' own headers name 950e99be. The frozen counter's requirement (receipt holds
  the observed `PREFIX pass=P fail=F` line) is met either way.

Verified clean (no finding): both tally pins match the instruments' output at R (`PIN_CHECK_SELFTEST pass=114
fail=0`, `UNLANDED_SELFTEST pass=17 fail=0`, both rc 0); receipts tracked at R, byte-identical to the working tree,
carrying those lines; `SKILL.md:941-980`, `corpus/QUALITY.md:1050-1087`, `PROVINCE.md:3-16`, the quota entry's
Boundaries block all accurate at R; landing touched neither SKILL.md, QUALITY.md, LOG.md nor PROVINCE.md, so no
round-50 drift behind any pointer; no stray tally token in SHONEN.md.

Residual risk / verification gaps: I did not re-run the frozen counters (out of seat scope; L1's runs are the
recorded data). The SCORECARD half of C1 belongs to another seat. R48ConnSiblings' CLEAN_SEPARATION verdict is
taken from that report's own text, not re-derived. Scratch `/fast/scratch/hyaku/mori-r50/Mo50bRevShonen/` is
removed after this write.
