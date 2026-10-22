# ScoutShapeCoverage — round 29 wave 2 (falsify)

Seat: MoriR29.ScoutShapeCoverage. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin` at
`8809a3fe1eaa87a0afa177a15263d174378e7462` (`git rev-parse HEAD`). Case file
`tools/fixtures/mori-oom-killers/cases-a2-r29.json`: blob `cc309d8e30cabc9767d0e1ac5d28d402cee261ee`, equal to the
blob at `d6d5cb0a` (`git rev-parse d6d5cb0a:<path>` = `git hash-object <path>`), `git diff d6d5cb0a..HEAD -- <path>`
empty, sha256 `1c76ea1f10e08acedb82c001a875ea84a9f552acf931ca2837645d482bb9d252`.

Read: the case file only (plus the rule text: `.ufo/waves/round-27/contract.md:55` A2-07, `:58` A2-10;
`.ufo/waves/round-26/contract.md:173-188`; `.ufo/waves/round-29/contract.md:138-145,170-172,179-181`).
Not read and not run: `tools/mori-oom-killers.py` and any tool output (task constraint; I did not open the C2 counter
either, so the counted-shape numbers are my reading of the contract wording, marked [INFERENCE]).

Method: per case I parsed `inputs.earlyoom_show` (LoadState, ActiveState, ActiveEnterTimestampMonotonic) and split
`inputs.earlyoom_journal` at every `earlyoom <version>` line into segments S1..Sn; every record was classified V
(version), D (`dryrun mode enabled`), S (send / escalation / process-group) or o; every record's position was derived
from its `__MONOTONIC_TIMESTAMP` against the boundary (at-or-after = in scope). Script:
`/fast/scratch/hyaku/mori-r29/w2/ScoutShapeCoverage/shape_scan.py`, output `scan.out`.

## Notation

`l/a` = LoadState/ActiveState. `B <n>` = bounded, `ActiveEnterTimestampMonotonic=<n>`; `U∅` = active, key absent;
`U0` = active, `<0>`; `NA` = unit not active. `1/3` = version lines in counted scope / total version lines.
`S2 dry (in)` = segment 2 holds `dryrun mode enabled`, segment lies inside the counted scope; `(pre)` = before the
boundary; `(cur)` = the last version line's segment. Pins: `st`=sigterm, `sk`=sigkill, `esc`=escalations,
`ei`=earlier_invocation_send_lines, `dsl`=dryrun_send_lines, `sc`=scope_complete, `nt`=oomd.notices_this_boot.
Shape column is the contract shape (round-29/contract.md:138-145) after the A4 R1 decisive pin (`:170-172`).

## 24-case input-shape table

| # | case (file:line) | rule/author | unit | scope | V in scope | dry-run segments | stamp-less records | decisive pins | verdict/exit | shape |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | f:12 | A2-07/207a | l/a | B 2000 | 1/2 | S1 dry (pre, no send); S2 real send (in) | none | st=1 | KILLER_ACTED/1 | – |
| 2 | f:61 | A2-07/207a | l/a | B 4000 | 1/3 | S1 dry (pre, no send); S2 real send (pre); S3 real send (in) | none | st=1, ei=1 | KILLER_ACTED/1 | – |
| 3 | f:118 | A2-07/207a | l/a | B 3000 | 2/3 | S2 dry (in); S1 real send (pre); S3 real send (in) | none | sk=1, ei=1 | KILLER_ACTED/1 | **a207** |
| 4 | f:175 | A2-07/207b | l/a | B 70000000 | 1/2 | S2 dry (in, cur); S1 real 2 sends (pre) | none | st=0, sk=0, dsl=1, ei=2 | KILLERS_QUIET/0 | – |
| 5 | f:233 | A2-07/207b | l/a | B 81000000 (vline at boundary) | 1/2 | S2 dry + 2 sends (in, cur); S1 SIGTERM+escalation (pre) | none | st=0, sk=0, dsl=2, ei=2 | KILLERS_QUIET/0 | – |
| 6 | f:295 | A2-07/207b | l/a | B 92000000 | 1/3 | S2 dry (pre); S1 real send (pre); S3 real 2 sends (in) | none | st=1, sk=1, ei=1 | KILLER_ACTED/1 | – |
| 7 | f:355 | A2-07/207c | l/a | U∅ | 2/2 | S1 dry (in); S2 real send (in, cur) | none | st=1, sc=false | KILLER_ACTED/1 | **a207** |
| 8 | f:404 | A2-07/207c | l/a | U0 | 2/2 | S1 real send (in); S2 dry + send (in, cur) | none | st=0, sk=0, dsl=1, ei=1, sc=false | KILLERS_UNKNOWN/2 | structural (loose reading) only, no >0 pin |
| 9 | f:457 | A2-07/207c | l/a | U∅ | 3/3 | S2 dry (in, middle); S1 real send (in); S3 real send (in) | none | sk=1, ei=1, sc=false | KILLER_ACTED/1 | **a207** |
| 10 | f:514 | A2-07/207d | l/a | B 60000000 | 1/2 | S1 dry + 2 sends (pre); S2 real 2 sends (in) | none | st=1, sk=1 | KILLER_ACTED/1 | – |
| 11 | f:572 | A2-07/207d | l/a | B 85000000 | 1/2 | S2 dry + 2 sends (in, cur); S1 real 2 sends (pre) | none | st=0, sk=0, dsl=2, ei=2 | KILLERS_QUIET/0 | – |
| 12 | f:632 | A2-07/207d | l/a | B 93000000 | 1/2 | S2 dry + 4 sends (in, cur); S1 dry (pre, no send) | none | st=0, sk=0, dsl=4, ei=0 | KILLERS_QUIET/0 | – |
| 13 | f:696 | A2-10/210a | l/a | U∅ | 1/1 | none | idx1 SIGTERM, key absent (after vline) | st=0, sk=0, sc=false | KILLERS_UNKNOWN/2 | **a210** |
| 14 | f:737 | A2-10/210a | l/a | U0 | 1/1 | none | idx1 SIGKILL `not-numeric` (after vline) | st=1, sk=0, sc=false | KILLER_ACTED/1 | **a210** |
| 15 | f:783 | A2-10/210a | l/a | U0 | 1/1 | none | idx1 SIGTERM, key absent (after vline) | sk=1, sc=false | KILLER_ACTED/1 | **a210** |
| 16 | f:828 | A2-10/210b | l/a | B 7200000 (vline at boundary) | 1/1 | none | idx1 SIGTERM, key absent (after vline) | st=0, sk=0, sc=false | KILLERS_UNKNOWN/2 | – (bounded, enter≠0) |
| 17 | f:868 | A2-10/210b | l/a | B 8300000 (vline at boundary) | 1/1 | none | idx2 SIGKILL `clock-unavailable` (after in-scope SIGTERM) | st=1, sk=0, sc=false | KILLER_ACTED/1 | – |
| 18 | f:913 | A2-10/210b | l/a | B 9400000 (vline at boundary) | 1/1 | none | idx1 SIGTERM `not-a-decimal` (after vline) | nt=2, st=0, sk=0, sc=false | KILLER_ACTED/1 | – |
| 19 | f:954 | A2-10/210c | l/i | NA (enter 4100000) | n/a | none | idx1 SIGTERM, key absent | actions=null, sc=false, ei=0 | KILLERS_QUIET/0 | **a210** (non-active) |
| 20 | f:989 | A2-10/210c | l/f | NA (enter 5200000) | n/a | none | idx2 SIGKILL `not-a-number`; stamped SIGTERM idx1 | no actions pin, ei=0, sc=false | KILLER_ACTED/1 | **a210** (non-active) |
| 21 | f:1028 | A2-10/210c | nf/i | NA (enter 6300000) | n/a | none | idx2 SIGKILL `unknown`; stamped SIGTERM before vline | actions=null, ei=1, sc=false | KILLER_ACTED/1 | **a210** (non-active) |
| 22 | f:1068 | A2-10/210d | l/a | B 51000000 | 1/1 | S1 dry (in) | idx2 `""`, idx3 `clock` (generic, after dry) | st=0, sk=0, dsl=0, sc=false | KILLERS_UNKNOWN/2 | – (no stamp-less send) |
| 23 | f:1122 | A2-10/210d | l/a | B 62000000 | 1/1 | none | idx2 `62000002.5` (generic); idx1 `-62000002` is numeric, < boundary | esc=1, sc=false | KILLER_ACTED/1 | – |
| 24 | f:1174 | A2-10/210d | l/a | B 74000000 | 1/1 | S1 dry (in) | idx3 `"   "`, idx4 key absent (generic); pre-scope idx0 is stamped | st=0, sk=0, sc=false | KILLERS_UNKNOWN/2 | – (no stamp-less send) |

Verdict spread: A2-07 7 ACTED / 4 QUIET / 1 UNKNOWN; A2-10 7 ACTED / 1 QUIET / 4 UNKNOWN.

## Shape tally (my reading, [INFERENCE] on the counter's implementation)

- `shape_a207` = **3 cases / 2 authors** — #3 (CaseA207a), #7 (CaseA207c), #9 (CaseA207c). #8 satisfies the
  structural clause on the loose reading (2 in-scope version lines, a dry segment, a non-dry segment with a send; the
  dry segment sits after the last version line, so a strict "between version lines" reading excludes it too) but in
  any case pins `st=0 sk=0`, so A4 R1 (`contract.md:170-171`) excludes it. Bounded branch: 1 case, 1 author.
  Unbounded branch: 2 cases, 1 author.
- `shape_a210` = **6 cases / 2 authors** — #13, #14, #15 (CaseA210a) and #19, #20, #21 (CaseA210c). Active+unbounded
  branch 3/1 (all 210a); non-active branch 3/1 (all 210c).
- Both shapes sit exactly on the `≥2 cases from ≥2 authors` floor of `contract.md:143-145`. One `case error` on any
  counted case drops that shape to a single author and turns C2 into a miss. Zero slack.
- Pins that do not carry the rule, yet count: #18's verdict rides on `oomd.notices_this_boot=2` (A4's integer pin is
  `sigterm=0`); #20 pins no `earlyoom.actions.*` at all (A4's integer pin is `earlier_invocation_send_lines=0`).

## Gap list — input shapes of A2-07 no case covers

0/12 A2-07 cases are non-active and 0/12 hold any stamp-less record.

1. **Non-active earlyoom** (`inactive`/`failed`/`not-found`/`activating`) + ≥2 version lines + one dry invocation +
   another invocation with real sends. All 12 A2-07 cases load `ActiveState=active` (already named debt, `:180-181`).
2. **Stamp-less version line** (no numeric `__MONOTONIC_TIMESTAMP` on the `earlyoom <version>` record). 0/12; all 28
   A2-07 version lines are stamped (40 stamped version lines in the file).
3. **Stamp-less send inside a dry-run invocation** (the A2-10 "left uncounted" clause against A2-07 dry-run routing).
   0 cases; no A2-07 journal carries any stamp-less record.
4. **Dry-run marker before the first version line** (preamble; no invocation to attribute it to). 0/12 — every
   `dryrun mode enabled` follows a version line.
5. **Two `dryrun mode enabled` lines in one invocation segment.** 0/12.
6. **Dry-run invocation straddling `ActiveEnterTimestampMonotonic`** (marker before the boundary, its send after it,
   same segment). 0/12; the three straddling segments (#1, #3, #6) hold no record at or after the boundary.
7. **Bounded scope with ≥2 in-scope version lines, real→dry ordering** (earlier in-scope invocation real, later
   in-scope invocation dry with sends). 0/12: #3 is dry→real inside scope; #4 and #11 are real→dry but all real sends
   are pre-scope. The "one dry-run invocation does not zero another's real sends" direction is only tested
   dry-before-real, never real-before-dry, inside a bounded scope.
8. **Escalation inside a dry-run segment** (`escalating to SIGKILL` — dry-run send line, or real escalation?). 0 of the
   2 escalation lines: #5 is a real pre-boundary segment, #23 is stamped and non-dry.
9. **`killing whole process group` / `kill failed` / `low memory` inside a dry-run segment.** 0 lines of the first
   kind in the whole file, 0 in a dry segment for the others.
10. **Version change across invocations** (e.g. `earlyoom 1.8.0` then `1.9.0`). All 40 version lines read
    `earlyoom 1.9.0`, so "split at each version line" never sees two distinct version strings.
11. **Zero version lines** with a dry-run marker and sends (a dry-run invocation with no version line at all). 0.

## Gap list — input shapes of A2-10 no case covers

1. **Stamp-less record before the bounded scope start of an active unit.** 0; the file's only pre-scope record
   (`73999999`, #24) is stamped. Whether a pre-scope stamp-less record still sets `scope_complete=false` is untested.
2. **Stamp-less send as the only evidence on a `not-found` unit.** 0; #21 pairs it with a stamped earlier-invocation
   send, so the A2-09 (removed unit's sends are positive) vs A2-10 (unclocked send uncounted) collision is untested —
   QUIET or UNKNOWN is unpinned.
3. **Inactive unit with a stamp-less send plus a stamped in-scope send.** 0; #19 has only the stamp-less send.
4. **Non-active unit whose `ActiveEnterTimestampMonotonic` is missing or `0`** (the "not active" and "unbounded"
   clauses never co-occur). 0; #19/#20/#21 carry 4100000/5200000/6300000.
5. **Unbounded active unit with a stamp-less non-send record plus a stamped send.** 0; #14/#15 have stamp-less sends.
6. **Dry-run invocation plus a stamp-less send.** 0; #22 and #24 combine a dry-run marker with stamp-less *generic*
   records and both pin `dryrun_send_lines=0`.
7. **Stamp-less escalation / kill-failed / low-memory / process-group line.** 0; #23's escalation is stamped and every
   stamp-less record in the file is a send or placeholder text (`empty-stamp record`, `clock`, `62000002.5`, `"   "`).
8. **Two or more stamp-less records with at least one a send.** 0; #22/#24 hold two generic records each.
9. **Decimal- or negative-shaped stamp on a send line.** 0; #14's send stamp is `not-numeric`, #23's `62000002.5` is a
   generic record.
10. **Whitespace-padded numeric stamp** (`" 74000003"`). 0; the whitespace variant is an all-blank string, so
    strip-then-parse is untested.
11. **Active bounded unit with a stamp-less generic record, no send and no dry-run marker** (plain
    QUIET-with-incomplete-scope output). 0; #22/#24 put a dry-run marker in the same scope.

Cross-rule: no case combines a stamp-less record (A2-10) with an A2-07 multi-invocation dry-run split — the two
routed shapes never co-occur in one input.

## Sensitivity and remaining unknowns

- [INFERENCE] The counted-shape numbers assume `contract.md:139-141` ("counted scope") and `:141-143` ("one segment
  between version lines holding `dryrun mode enabled` and another segment without it holding a send line"). Whether
  the dry segment must itself lie between version lines changes only #8, which A4 R1 already excludes.
- Alternative reading of "the unit is not active" as absent/failed only (excluding `ActiveState=inactive`) gives
  `shape_a210` = 5/2; the ≥2/≥2 floor still holds but the margin stays zero.
- Unknown to me: the tool's actual output on each case (source unread, tool unrun); the counter's implementation
  (unread); whether "current invocation" is the last version line — #7/#8/#9's expectations are consistent with that
  reading, which is all I can observe.
- Unrun checks: no tool run, no counter run, no case-file mutation. Nothing above is a PASS/FAIL of the tool.

## Reproduce

```sh
python3 /fast/scratch/hyaku/mori-r29/w2/ScoutShapeCoverage/shape_scan.py \
  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases-a2-r29.json
```

Scan output: `scan.out` (24 lines) in the same scratch dir. Shape tallies from it: A2-07 `structural=True` 4 cases
(`decisive>0=True` 3); A2-10 `structural=True` 6 cases, all with an integer decisive pin.
