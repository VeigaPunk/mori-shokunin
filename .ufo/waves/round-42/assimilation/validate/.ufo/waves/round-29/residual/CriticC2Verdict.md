# CriticC2Verdict — residual critic of the L1's "C2 = miss" proposal (round 29)

Seat: MoriR29.CriticC2Verdict (leaf). Lane tip read: `cdfcf66d` (tool) and `07b9a4b9` (current HEAD, adds only C1
row fixes). Scratch: `/fast/scratch/hyaku/mori-r29/residual/CriticC2Verdict/` (sandbox clone `lane/` at `cdfcf66d`).
Tools installed or updated: none. No lane/fleet writes besides this report; the oom-killers tool was run only with
`--selftest --cases` and `--inputs` on case inputs and invented inputs.

## Verdict proposal

**C2 = miss, but the reasons need to be reattributed.** Reasons (1) and (3) each make it a miss on their own under
the contract's text. Reason (2) is the counted cause: the counter prints `a2_r29_selftest=FAIL`. But "the contract
decides the opposite" is not a sound way to state it. The honest wording is: "three judged tool errors were left
unfixed by the L1's choice, which `may` permits; a fix was feasible; the L1's dissent goes to round 30."

Counter at the landed tip (sandbox, `bash .ufo/waves/round-29/count-c2.sh cdfcf66d`): `blind_violations=20`,
`provenance=24/24 unselected=0`, `shape_a207=3/2`, `shape_a210=6/2`, `a2_r29_selftest=FAIL(exit=1)`, `C2=unmet`,
exit 1.

## Ranked findings

### F1 (high): declining the Judge11-13 tool errors was a choice, not something the contract forced, and the stated reason does not hold

- **Counterexample: a fix exists.** I made a scratch copy of the landed tool (`probe.diff`, 54 lines, 4 hunks). It
  gives a non-active unit a bounded scope at a non-zero `ActiveEnterTimestampMonotonic`, reports version/grammar
  and the two line counts, and keeps `actions: null` and `scope_complete: false`. Results:
  `cases.json PASS 32/32`, `cases-supplementary.json PASS 32/32`, `cases-a2.json PASS 30/30`,
  `cases-a2-r29.json PASS 24/24` (`probe-selftest.txt`). The landed tool on the same files gives
  32/32, 32/32, 30/30 and `FAIL 21/24`.
- **Differential, landed vs probe, over 134 inputs.** The inputs are all four case files plus
  `.ufo/waves/round-26/evidence/a2-detectors/*.json`. Result: `changed=30 verdict_flips=[]`. No `KILLER_ACTED`
  changed, so the contract condition at `contract.md:77-79` holds. The probe is a feasibility proof, not a
  landable fix. It also turns `null` into `0` for unreadable-show states (`c25`, `c32`), which a real fix must not
  do.
- **The cited text does not decide the question.**
  - `round-26/contract.md:102-104` is about `actions: null` for an "inactive or absent" killer. It says nothing
    about `version` or `grammar`, which are not counts.
  - "Never zero counts" is not applied generally, even by the landed tool. It reports
    `earlier_invocation_send_lines` (a count) as `0` for the inactive unit in Judge11
    (`c2-fix-selftest.txt` lists no mismatch on that field). Frozen `cases-a2.json` `a2-06` pins it to `3` for an
    inactive unit.
  - Judge12's unit is `failed`, which maps to `unavailable` (`round-26/contract.md:162-163`). Lines 102-104 name
    only inactive or absent, so the cited clause does not cover that case at all.
  - `:78-79` says "current invocation". It does not say a stopped unit has none. "Only an active unit has a current
    invocation" is a comment in the tool (`tool-landed.py:274`), not contract text.
- **The older frozen files pin nothing that conflicts.** Among non-active cases they pin only `actions`,
  `scope_complete` and `earlier_invocation_send_lines` (scan of all three older files, scratch command log). None
  pins `version`, `grammar`, `dryrun_send_lines` or `process_group_lines`.
- **Honesty under "the L1 may change the tool"** (`contract.md:77`). Declining is permitted, and its consequence
  (selftest FAIL, `C2=unmet`) is reported. The problem is the framing: the L1 is re-ruling questions that the
  procedure gives to non-author judges (`contract.md:75-77`), which creates a second authority. The defensible
  statement is "tool error (judged), unfixed; L1 dissent: <reading>".
- **The dissent is not recorded.** At HEAD `07b9a4b9` no committed `.md` outside the Judge files mentions
  Judge11-13, the decline, or `21/24` (grep, no hits). The lesson's mistakes section (`corpus/lessons/round-29.md:25-45`)
  is silent on it.
- Impacted axes: operability (the shipped tool keeps three judged errors), calibration (how the miss is
  attributed).
- **Smallest safe correction:** in the lesson and closure, attribute the C2 miss to (a) the selftest FAIL 21/24,
  caused by three judged tool errors left unfixed by L1 choice, (b) Judge02's `unclear text`, and (c)
  `blind_violations=20`. Record the L1's reading as a dissent with these pointers. Do not cite `:102-104` as
  deciding version/grammar, and never for the failed-unit case.

### F2 (high): reason (1) holds procedurally, but two judges ruled the same question in opposite ways

- Judge02 rules `earlyoom.dryrun` `unclear text` (`w2/Judge02.md:37,43-46`). Judge04 rules the same field, with
  the same semantics (expected `false` when an earlier dry-run invocation exists and the current invocation is
  real, scope unbounded), as `tool error`, saying the text decides it per invocation (`w2/Judge04.md:29`). All
  three frozen `dryrun` pins come from one author (CaseA207c) and consistently mean "the current invocation's
  flag".
- The contract makes `unclear text` on any case a miss (`contract.md:79`), so reason (1) stands. Note also that the
  plain text arguably decides `true` here. Round 29's own definition of unbounded scope is "every stamped record"
  (`contract.md:139-140`), and `round-26/contract.md:89` maps `dryrun mode enabled` to the flag. On that reading
  the case is wrong, not the text unclear. Either way the outcome is a miss, never a tool error.
- **Smallest safe correction:** report Judge02 and Judge04 as conflicting rulings on one question. Do not use
  Judge04 to override Judge02.

### F3 (medium): reason (3) holds; the adjudication explains the hits but does not clear the gate

- I re-ran the gate at the freeze commit, which amendment A4 specifies (the committed receipt was taken at
  `221cbd8f`): `bash .ufo/waves/round-29/check-blind-wave.sh d6d5cb0a .ufo/waves/round-29/w1 '^CaseA2(07|10)[a-d]\.md$'`
  prints `blind_violations=20`. Also `git diff --stat 221cbd8 d6d5cb0 -- .ufo/waves/round-29/w1` is empty, so
  AdjudicateBlindHits judged the same bytes.
- A4 R3 says the gate "must print `blind_violations=0`; otherwise C2 is a miss" (`contract.md:177-178`). The
  counter enforces this (`count-c2.sh:268`). Adjudicating the hits as false positives cannot change the printed
  value.
- **Hidden gap.** For the 7 writer hits the files-opened heading did not match `files_header_re`
  (`check-blind-wave.sh:59`). The `writer-forbidden-opened-path` scan (`:121-150`) therefore never ran on those 7
  lists. That blindness rests only on the adjudicator reading them by hand (`w2/AdjudicateBlindHits.md:47-68`). The
  instrument had a false-negative surface as well as false positives. Lesson M2 (`round-29.md:32-36`) names only
  the false positives.
- **Correction:** extend M2 to cover the scan that never ran. Before round 30 binds the gate, fix the writer
  heading in the writer template (or widen the regex) and keep a receipt of a clean run.

### F4 (medium): the landed change harms operability in one shape, and gives `dryrun` two meanings

- **H1, evidence lost under unbounded scope** (invented inputs `probe/H1*.json`). The unit is active with
  `ActiveEnterTimestampMonotonic` missing (and, separately, `0`). The journal holds a version line, a real
  SIGTERM-to-process line, then a version line (a plain restart). Base `7118f320`: `KILLER_ACTED`, exit 1,
  `sigterm 1`. Landed: `KILLERS_UNKNOWN`, exit 2, `sigterm 0`, `earlier 1`.
  - The cause is `tool-landed.py:293-302`, which starts the scope at the last version line. For an active unit,
    earlier sends never decide the verdict (`:316-323`, `:468`).
  - This is consistent with A2-06 and with frozen `r29-a2-07-real-then-dryrun-zero-enter`.
  - It contradicts round 29's own counted-scope definition ("unbounded: every stamped record", `contract.md:140`)
    and the base comment "evidence is never dropped" (fix-landed.diff:9-11). No amendment changed the rule text,
    so the tool now holds an unstated rule.
  - Bound on harm, from code: unbounded scope always has `scope_complete = False` (`:424`, `scope_known` is
    False). An active unit with an incomplete scope is `UNKNOWN` when nothing acted (`:488`). So the change can
    only move ACTED to UNKNOWN, never to QUIET.
  - [INFERENCE] Real-world reach is small: systemd sets a non-zero `ActiveEnterTimestampMonotonic` on activation,
    so this needs a truncated or odd show read.
- **H2, two meanings for `dryrun`.**
  - In a bounded scope the flag is true if any segment in scope logged dry-run (`:410`, never reset). Frozen
    `r29-a2-07-dryrun-inside-scope` on the landed tool gives `KILLER_ACTED`, `actions.sigkill 1`, `dryrun true`.
    Invented `H2` (dry-run segment, then a real segment) gives `KILLER_ACTED`, `sigterm 1`, `dryrun true`.
  - In an unbounded scope, truncation makes it the current invocation's flag (Judge04's case passes with `false`).
  - A reader sees `dryrun: true` next to real, counted sends. Under Judge04's reading this is an unpinned tool
    error.
- **Correction:** do not change the tool again in round 29. Name both in the lesson as debt created by the landed
  change. In round 30, amend the rule text first (see below).

### F5 (low): the remaining blind gap is still debt

`contract.md:180-181` names "A2-07 shape with a non-active earlyoom" as debt. Judge12 shows that the non-active
scope question (is a send after the retained `ActiveEnterTimestampMonotonic` current or earlier?) also affects
A2-10. Carry the two together under one name.

## What round 30 should do with the two readings

1. **Amend the rule text before any writer or tool work, as a numbered and counted decision.** It must settle:
   - (a) whether a non-active unit with a non-zero retained `ActiveEnterTimestampMonotonic` has a bounded "last
     invocation" that supplies `version`/`grammar`, and whether in-bound sends are current or earlier (Judge12);
   - (b) whether `dryrun_send_lines`/`process_group_lines` are `null` or `0` when `actions` is `null`, made
     consistent with `earlier_invocation_send_lines` being a reported count for non-active units;
   - (c) `dryrun` means the current invocation's flag in both bounded and unbounded scope (F2, F4 H2);
   - (d) unbounded scope is either "every stamped record" (`contract.md:140`) or "from the last version line"
     (landed), with H1's verdict stated explicitly.
2. **Keep `cases-a2-r29.json` frozen and unchanged.** Whichever reading the amendment adopts, the round-29 cases
   either pass after a judged fix (writers' reading; the probe shows this is feasible with all older tallies kept
   and zero verdict flips across 134 inputs) or stay failing and are carried as named `case error` debt. They are
   never edited or re-tagged.
3. **Judge consistency.** Group cases that share a semantic question under one judge, or add a reconciliation
   step, so Judge02/Judge04-style splits are caught before closure.
4. **Fix the blind gate** (F3) and receipt it on a known-clean input before binding it as a counted condition.

## Evidence index (scratch, not lane)

- `probe-selftest.txt` — landed vs probe selftest markers, four files.
- `probe.diff` (sha256 prefix `9b17b55663d04629`), `tool-probe.py` (`3a8d87cf02bd2609`); `tool-landed.py` sha256
  `41464957…` equals the header of `evidence/c2-fix-selftest.txt:1`; `tool-base.py` = `git show 7118f320:tools/mori-oom-killers.py`.
- `probe/H1-*.json`, `probe/H2-*.json`, `probe/H3-*.json`, `probe/dryrun-inside-scope.json` — invented or case
  inputs. H3 (real send, then a dry-run current invocation, unbounded) is `KILLERS_UNKNOWN` on both base and
  landed: no regression.
- Not run: the C2 counter on the probe tool. [INFERENCE] It would still print `C2=unmet` because of
  `blind_violations=20` (`count-c2.sh:268`) and Judge02's ruling.

Report: .ufo/waves/round-29/residual/CriticC2Verdict.md
