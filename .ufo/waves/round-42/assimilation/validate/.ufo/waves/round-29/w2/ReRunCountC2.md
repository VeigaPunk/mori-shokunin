# ReRunCountC2 — wave-2 falsify run of the C2 counter (seat MoriR29.ReRunCountC2)

Role: review-only. No edits, no lane commits. Counter executed verbatim:
`bash .ufo/waves/round-29/count-c2.sh <rev>` (revision hash verified via `rev-parse --verify`).
No tools installed (nothing needed; RULES.md read). Tool runs were `--selftest --cases` only, never live.

## 1. Counter runs — every key=value line and exit

### 1a. At 7118f320a5ef18d20c1e361eff77db0e1a97b2d6 (entering tip) — exit 1
```
rev=7118f320a5ef18d20c1e361eff77db0e1a97b2d6
tool_blob=3fb78bbc2612c38e463e04083bdb213954647568
cases_blob=5b4dcee7b682c896c8e9f22ed1f8ac58d0176556
cases_baseline_blob=5b4dcee7b682c896c8e9f22ed1f8ac58d0176556
cases_blob_state=match
cases_a2_blob=7ba553d45e3b00d507e57132cc3c28fb140f83fd
cases_a2_baseline_blob=7ba553d45e3b00d507e57132cc3c28fb140f83fd
cases_a2_blob_state=match
cases_a2_r29_blob=absent
cases_selftest=PASS 32/32
cases_a2_selftest=PASS 30/30
freeze_commit=none
freeze_path=none
freeze_adds=0
freeze_adds_raw=0
freeze_renames=0
freeze_deletes=0
freeze_edits=0
freeze_blob_versions=0
cases_changed_since_freeze=1
tool_blob_at_freeze=none
writer_absent=CaseA207a / CaseA207b / CaseA207c / CaseA207d / CaseA210a / CaseA210b / CaseA210c / CaseA210d
blind_exit=not_run
blind_violations=not_run
provenance=0/0 unselected=0
provenance_errors=0
a2_r29_schema=absent
a2_r29_cases=0
a2_r29_ids=absent
a2_r29_rules_covered=0/2
a2_r29_distinct_inputs=0/0
a2_r29_legacy_input_overlaps=0
a2_r29_input_checks=fail:file_absent
a2_r29_rule_checks=fail:file_absent
shape_a207=0/0
shape_a210=0/0
a2_r29_selftest=absent
C2=unmet
exit=1
```
This block is byte-identical to the committed before evidence `.ufo/waves/round-29/evidence/c2-before.txt` (same
script sha256 220eb99122d0cb9a4c96f6f88656f4170d025427afaca895a7d4f2bd89c2c51f).

### 1b. At d6d5cb0a026f7cebe3f6d2094204b4b57eeef576 (freeze) — exit 1
```
rev=d6d5cb0a026f7cebe3f6d2094204b4b57eeef576
tool_blob=3fb78bbc2612c38e463e04083bdb213954647568
cases_blob=5b4dcee7b682c896c8e9f22ed1f8ac58d0176556
cases_baseline_blob=5b4dcee7b682c896c8e9f22ed1f8ac58d0176556
cases_blob_state=match
cases_a2_blob=7ba553d45e3b00d507e57132cc3c28fb140f83fd
cases_a2_baseline_blob=7ba553d45e3b00d507e57132cc3c28fb140f83fd
cases_a2_blob_state=match
cases_a2_r29_blob=cc309d8e30cabc9767d0e1ac5d28d402cee261ee
cases_selftest=PASS 32/32
cases_a2_selftest=PASS 30/30
freeze_commit=d6d5cb0a026f7cebe3f6d2094204b4b57eeef576
freeze_path=tools/fixtures/mori-oom-killers/cases-a2-r29.json
freeze_adds=1
freeze_adds_raw=1
freeze_renames=0
freeze_deletes=0
freeze_edits=0
freeze_blob_versions=1
cases_changed_since_freeze=0
tool_blob_at_freeze=3fb78bbc2612c38e463e04083bdb213954647568
blind_exit=1
blind_violations=20
provenance=24/24 unselected=0
provenance_errors=0
a2_r29_A2-07=cases=12 distinct=12 authors=4 unpinned=0
a2_r29_A2-10=cases=12 distinct=12 authors=4 unpinned=0
a2_r29_schema=ok
a2_r29_cases=24
a2_r29_ids=unique_printable
a2_r29_rules_covered=2/2
a2_r29_distinct_inputs=24/24
a2_r29_legacy_input_overlaps=0
shape_a207=3/2
shape_a210=6/2
a2_r29_rule_checks=ok
a2_r29_shape_checks=ok
a2_r29_input_checks=ok
a2_r29_selftest=FAIL(exit=1)
C2=unmet
exit=1
```

### 1c. At 8809a3fe1eaa87a0afa177a15263d174378e7462 (wave-2 lane tip) — exit 1
Output is byte-identical to block 1b (all 46 lines) with only `rev=8809a3fe1eaa87a0afa177a15263d174378e7462`
differing, so `C2=unmet`, exit 1 at the landed tip. The tip counter result therefore does not meet the declared
after-value (`C2=met`, exit 0).

## 2. Stability confirmations

- Counter blob unchanged since 221cbd8f: `git log --format=%h -- .ufo/waves/round-29/count-c2.sh` prints only
  `221cbd8`; blob `4ad9abc8fd6560e827ccb5a8813940a9197b0a1e` at both 221cbd8f and HEAD (identical).
- Case file unchanged since d6d5cb0a: `git log --format='%h %s' -- tools/fixtures/mori-oom-killers/cases-a2-r29.json`
  prints only the freeze commit `d6d5cb0`; blob `cc309d8e30cabc9767d0e1ac5d28d402cee261ee` at both d6d5cb0a and
  HEAD; absent at 7118f320 (rev-parse exit 1).
- Provenance (A3 F2) at freeze/tip: `provenance=24/24 unselected=0`, `provenance_errors=0`; no `writer_absent`
  lines. Each of the eight reports contains exactly one fenced ```json array (checked per file); each author has 3
  cases in the file (24 total), so every report case appears and every file case matches its author's first array.
  Before: `0/0 unselected=0` (reports absent).
- Shapes: `shape_a207=3/2`, `shape_a210=6/2` at freeze/tip (both ≥2 cases from ≥2 authors → shape_ok); `0/0`
  before. A2-07: 12 cases/12 distinct inputs/4 authors; A2-10 same; `unpinned=0` for both rules.
- Blind: `blind_exit=not_run` at 7118f320 (check script absent there); `blind_exit=1`, `blind_violations=20` at
  freeze and tip. Direct run of `check-blind-wave.sh HEAD .ufo/waves/round-29/w1 '^CaseA2(07|10)[a-d]\.md$'`
  reproduces the 20 lines: 13 nonwriter-tool-run-output/citation (AxisOperability.md:19; BuildTipReceipts.md:5,135,
  136,137,140; DraftQualityCriteria.md:75,76,77,86; ReviewLateMutCountC1Amended.md:78; ReviewLateMutHeadingCheck.md:37,
  39) + 7 writer-missing-files-opened-list (CaseA207a-d, CaseA210a,b,d). w1 tree is byte-identical from 221cbd8f
  through d6d5cb0a to HEAD (`git diff d6d5cb0a HEAD -- .ufo/waves/round-29/w1` = 0 lines), so the freeze-state result
  is exactly this.

## 3. Why C2=unmet at tip (two independent causes)

1. `a2_r29_selftest=FAIL(exit=1)` — the tool at tip has blob 3fb78bbc2612c38e463e04083bdb213954647568 = the freeze
   blob (`tool_blob_at_freeze`), i.e. the L1 draft fix is NOT landed; evidence/c2-freeze-selftest.txt records the same
   first run on the frozen file as FAIL 11/24. The counter requires the exact marker `PASS 24/24`.
2. `blind_violations=20` ≠ 0 — A4 R3 condition fails at the freeze commit and at tip.

## 4. Counter read against amendments A2–A4 (rules implemented looser than written)

Conformance (all checked against count-c2.sh text):
- A2 shape lines: bounded/unbounded scope logic matches the text (skip unstamped records; in bounded mode skip stamps
  before a non-zero ActiveEnterTimestampMonotonic; active-unit gate via `ActiveState=active`); `shape_a207` needs ≥2
  version segments, one holding `dryrun mode enabled`, another without it holding a send line; `shape_a210` needs a
  send record without numeric `__MONOTONIC_TIMESTAMP` while active-with-0/missing or inactive. Thresholds ≥2 cases /
  ≥2 authors per shape.
- A3 F1: required-field pin is presence-only (`unpinned` counts cases missing any REQ key), matching the written
  statement; the A2-07 round-28 map is preserved via `PASS 30/30` on `cases-a2.json`.
- A3 F2: canonical JSON equality (sort_keys), first fenced array per report, multiplicity-aware `unselected`, errors
  counted. No selection gap on the actual reports (single fence each).
- A4 R1: decisive pins enforced exactly — A2-07 needs `earlyoom.actions.sigterm`/`sigkill` as integer > 0; A2-10
  needs one of sigterm/sigkill/escalations/earlier_invocation_send_lines as integer (any value). Verified on data:
  `r29-a2-07-real-then-dryrun-zero-enter` (sigterm=0, sigkill=0) matches the shape but is correctly excluded from
  `shape_a207`.
- A4 R2: writer set exactly CaseA207a–d/CaseA210a–d; `writer_absent` is printed and informational (not a pass
  condition by itself).
- A4 R3: requires `blind_exit=0` AND `blind_violations=0`.

Looser-than-written items (none affect the current verdict):
1. **Blindness anchor (formal only):** A4 R3 words the run "at the freeze commit"; the counter runs the check at the
   passed `<rev>` (the landed tip). Identical result here because w1 is byte-identical freeze→tip.
2. **Heuristic regex breadth (residual risk):** `VERSION`/`SEND` use word-boundary patterns (`\bversion\b`,
   `\bearlyoom\s+v?\d+(\.\d+)+\b`, `\bsend(?:ing)?\b`). A journal line merely containing the words "version"/"send"
   would count; on the frozen shape cases the matched lines are the canonical `earlyoom 1.9.0` / `sending SIGTERM
   …` lines, so no spurious counts observed.
3. **Required-field pin presence-only:** matches the written statement; the integer constraint exists only in A4 R1
   for shapes, which IS enforced.

Counter additions beyond the amendments are strictly tighter (per-rule distinct inputs ≥2, global input distinctness,
no legacy input overlap, selftest N/N on the new file, baseline blobs + `PASS 32/32`/`PASS 30/30`, freeze_adds==1,
no renames/deletes, `provenance_errors=0`), never looser.

## 5. Findings by severity

- **Blocker 1 (C2 unmet):** `a2_r29_selftest=FAIL(exit=1)` at freeze and tip; tool blob unchanged since 7118f320,
  draft fix not landed. Counter correctly reports `C2=unmet` (count-c2.sh lines 264–265).
- **Blocker 2 (C2 unmet):** `blind_violations=20` at the freeze commit and tip (A4 R3 miss). 13 nonwriter tool
  citations/outputs (BuildTipReceipts.md, DraftQualityCriteria.md, AxisOperability.md, ReviewLateMut*.md) and 7
  writers lacking a check-conforming files-opened header. Note: all eight writer reports do contain disclosure
  sections, but only CaseA210c's literal `Files opened:` matches the check grammar; CaseA207b and CaseA207d further
  self-report fixture exposure ("cannot claim an uncontaminated blind process" / "cannot certify a clean blind
  process"). Even setting the header-format issue aside, the nonwriter citations are true rule breaches (A3 F3).
- **Observation:** provenance, shapes, fixed writer set, freeze analysis, and baseline selftests all pass their
  checks at freeze/tip; the counter itself is stable (single commit 221cbd8f, unchanged blob; case file single commit
  d6d5cb0a, unchanged blob).

## 6. Residual risk / verification gaps

- The un-landed draft tool fix is out of my scope (not in the lane; I did not run or read it). Its landing cannot be
  evaluated here.
- The counter's pass/fail is only as good as the blind-check script's regexes (see §4.2) and its own heuristics; no
  false positives found on the frozen data.
- Process conditions ("committed before the L1 runs the tool", writer file-opened evidence) are reported separately,
  not counted; they currently fail independently (7/8 header misses + 13 nonwriter citations).
