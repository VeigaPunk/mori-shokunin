# CriticC2Verdict — round 30, wave 2 (falsify the author's C2 verdict)

**Verdict: agree. C2 is a miss under the contract text, both with the A3 gate and with the A2 gate. Separately, I
found one defect that is not counted: the gate's self-test treats a round-29 false positive as an expected hit. It
does not change the C2 result.**

Attacked item: the author's claim in `evidence/c2-after.txt` and commit `0b828c2` that `C2=unmet` with
`blind_violations=1` as the only failing condition and "all other conditions met".

## How I checked it

- Lane tip `ad0f047`; measure commit `0b828c2`; freeze commit `db1ec46`. I ran the counter from its commit blob,
  `bash <(git show 8ac9535:.ufo/waves/round-30/count-c2.sh) <rev>`. The blob is `f4f86b0d…`, the same at `8ac9535`
  and `ad0f047`.
- I extracted gate blobs to scratch: A2 version `893e69d1` (at `32e287f`) and A3 version `dbcbe50e` (at `55f9a69`).
  `dbcbe50e` is the same blob at `db1ec46` and `ad0f047` (`git rev-parse <rev>:.ufo/waves/round-30/check-blind-wave.sh`).
- I ran the gates with `cwd` set to the lane. They make read-only git calls, and their self-test temporary repository
  goes under my scratch `TMPDIR`. I made no lane writes.

## (a) Is C2 really a miss, or is there a reading under which it is met?

It is a miss under every reading I could build.

1. **The literal reading.** `contract.md:79` requires the gate, run at the freeze commit, to print
   `blind_violations=0`. A2 (`contract.md:165`) repeats that requirement. "Counters from blobs" (`contract.md:194-196`)
   says the gate at the freeze commit is the freeze commit's blob. That blob is the A3 version, and it prints:
   ```
   scanned=4
   blind_violations=1
   .ufo/waves/round-30/w1/CaseR30a.md:105:writer-forbidden-opened-path
   exit=1
   ```
   The counter gives the same result at both `ad0f047` and `0b828c2`: every other line passes, then `scanned=4`,
   `blind_violations=1`, `C2=unmet`, `exit=1`.
2. **Reading "met" by treating line 105 as an adjudicated false positive.** No such route exists in this contract.
   "adjudicat" occurs only at `contract.md:76` and `:172`, and both refer to round-29 hits. No clause lets the L1
   adjudicate a round-30 gate hit away. Round 29 withdrew its own escape clause (A4; commit `67779aa` subject). The
   after-data diagnostic gate (`evidence/gate-a4-diagnostic.txt`: 0 violations) is explicitly uncounted, and
   `contract.md:194-196` forbids substituting it.
3. **Reading by the claim's purpose ("Gate fixed (R5)", `contract.md:75`).** R5 says "the matcher cannot separate
   writer vocabulary from tool leakage" (`corpus/lessons/round-29-verifier-spotcheck.md:162-163`). `CaseR30a.md:105`
   is ordinary writer prose: "The scratch JSON passed python3 json.load; I opened no lane tool source…". The gate trims
   the trailing `;` (gate `:37`), sees a dot in `json.load`, treats it as a path (`:46-48`), and finds it is not on the
   allowlist. That is the same class of failure R5 names. So the purpose reading also says "not fixed", and the defect
   below makes it worse.

Conclusion (a): the author's "miss" is correct. No reading gives `C2=met`.

## (b) If A3 is disregarded, what does the A2 gate say?

It also misses, and by more. A2 blob `893e69d1` run at `db1ec46` on `.ufo/waves/round-30/w1` gives `scanned=4`,
`blind_violations=4`, exit 1:

- `CaseR30a.md:96`, `CaseR30b.md:116`, `CaseR30c.md:79` and `CaseR30d.md:110`, all `writer-forbidden-opened-path`.
- Each flagged line is the godspeed skill path (`CaseR30a.md:96`, `b:116`, `c:79`, `d:110` at `db1ec46`).

This matches the committed `evidence/gate-a2-prefreeze.txt`. The gate reports only the first forbidden line per file
(gate `:129-131`), so under A2 `CaseR30a.md:105` is also forbidden but hidden behind `:96`. That makes the A2 result
at least 4 hits, with the line-105 problem inside it.

Under A2 these 4 hits are not parser errors. The writers really opened the files (their `## Files opened` lists say
so), and A2's allowlist says "anything else is a violation" (`contract.md:166-172`). So A2 fails C2.4 by its own
definition.

**Ruling consequence: the A3 question is moot for the verdict.** C2 misses on the A2 version (4) and on the A3
version (1). The closure does not need to decide whether A3 is admissible in order to rule C2 a miss.

A3 is still a counted-condition loosening made after data. It widened the allowlist after the L1 had seen the A2
output (`contract.md:207-222`). It conflicts with the preamble "never withdrawn or narrowed" (`contract.md:5`) and
with A2's "nothing is narrowed" (`contract.md:159`). The disclosure is honest, but it should not serve as a precedent
or be credited.

One finding cuts both ways: the godspeed and RULES gap was visible before any round-30 data existed. The round-29
writers that the A2 self-test runs on also list both files (for example `CaseA210c.md:196-197` at `d6d5cb0a`, and
`.ufo/waves/round-29/w2/AdjudicateBlindHits.md:51-57`). So A3 fixes a real pre-data blind spot, but it fixed it late.

## (c) Is any other C2 condition failing that the author missed?

None of the counted conditions fails apart from C2.4. I re-derived each one from committed bytes:

| Condition | Re-derived from committed bytes | Result |
|---|---|---|
| Residual (C2.1), r29 blob | counter: `r29_selftest=PASS 24/24`, `r29_blob_ok=yes` | holds |
| Older pins (C2.2) | `older=PASS 32/32 / PASS 32/32 / PASS 30/30`, `blobs_ok=yes` | holds |
| Freeze identity (A2 F1) | first add of `cases-a2-r30.json` is `db1ec46`; `git diff --quiet 7aa7748 ad0f047 -- tools/` is clean; `git log 7aa7748..ad0f047 -- tools/ …gate …count-c2.sh` is empty; sha256 of the freeze bytes is `b68843e754977e78465039d196582f6d099f85ac7b17f7330fb8a8145f993735`, matching the commit subject | holds |
| Order | `merge-base --is-ancestor`: counter `8ac9535` and gate `32e287f` are both ancestors of `db1ec46` (parent chain `db1ec46`→`8ac9535`→`55f9a69`→`32e287f`) | holds |
| Provenance and authorship | counter: `provenance=8/8 unselected=0`, `authors=4`; author keys are `CaseR30a`, `CaseR30b`, `MoriR30.CaseR30c` and `CaseR30d` (both forms allowed by `contract.md:192-193`) | holds |
| Shape (C2.3 + A2 S1) | my own script: 8 distinct ids and 8 distinct inputs; every timestamp is a digit string and non-decreasing; no leading-whitespace send line. The later "send-like" lines (for example `escalation` index 4, `sigkill` index 3) are threshold banners `sending SIGTERM when …`, not `sending SIGTERM to process `. The counter's lack of `lstrip` on send lines therefore hides nothing here | holds (8/8) |
| Pins: allowed set (`contract.md:84-86`; the counter does not check this) | my script: no field outside the 7 permitted keys in any case | holds |
| Undecided mandatory pins (A2 W1/D1, `contract.md:183-186`; the counter does not check this) | grep of the four reports: only `CaseR30b.md:7,55` ("does not decide additional permitted field pins") and `CaseR30c.md:75` ("Other fields: Not pinned"). Neither names `sigterm` or `earlier_invocation_send_lines` | holds |
| Literal-reading miss (A2) | all 8 cases expect `KILLERS_UNKNOWN`, exit 2; base and fixed tools both print `PASS 8/8`; `shape_verdicts=8/8` | holds |
| Tool run order (A2 F2) | freeze commit committed at 21:48:21Z; base receipt stamped 21:48:29Z; fixed receipt 21:48:52Z; fix commit `7aa7748` committed at 21:49:15Z (`git log --format=%cI`). The tool at `7aa7748` has sha256 `9c88ef27…0fe1`, matching the fixed receipt; `fix-tool.diff` hunks are identical to `git diff db1ec46 7aa7748 -- tools/mori-oom-killers.py` | holds (the timestamps are self-reported; the order is consistent) |
| Differential bound (A2) | counter: `differential=94/94 changed=2 disallowed=0 acted_lost=0 errors=0`. Receipt `c2-differential.txt`: the 2 older changes are `a2-02` (`ActiveState=deactivating`) and `a2-06` (`inactive`), exit unchanged | holds |
| Receipts | `receipts=3/3` | holds |
| Gate self-test and mutants | `gate_selftest=PASS`, `gate_mutants=4/4` (counter); `--selftest` PASS for both blobs (my run) | holds as counted; see the defect below |

### Defect found (uncounted): the gate's self-test treats a false positive as an expected hit

- **Counterexample:** the A3 gate at `d6d5cb0a` on the round-29 wave prints `blind_violations=9`. One hit is
  `CaseA210c.md:1:writer-missing-files-opened-list`. But `CaseA210c.md:194-205` at `d6d5cb0a` does hold a full
  files-opened list under the label `Files opened:`. The gate recognizes that label (`:116`) but credits only entries
  under an H2 heading (`:128`), so it reports a missing list where one exists.
- **The self-test locks this hit in:** `expected_pairs` contains `'CaseA210c.md|writer-missing-files-opened-list'`
  (gate `:176`, comment `:215`).
- **Why it gets past the contract's check:** it is not one of the 20 round-29 hits (`AdjudicateBlindHits.md:37-43`
  lists 7 writer `:1` hits, without A210c), so A2's "none of the 20" test (`contract.md:170-172`) passes. Measured
  against the original C2.4 clause ("it reports 0 on the round-29 writer wave", `contract.md:76`), it is a new false
  positive. A2's replacement of "reports 0" with "an exact expected set" (9 hits) is itself a loosening. The amendment
  was made before data, but its preamble's claim that "nothing is narrowed" (`contract.md:159`) does not hold for that
  clause.
- **Impact:** this strengthens "R5 not fixed". The gate makes 2 known false-positive classes (an H2-only files list,
  and prose with a dotted token), not one.

### Other findings (the claim's substance and the structure)

- **The brief itself produced the line-105 false positive, and that was knowable before data.** The writer brief
  (`wave1-dispatch.json` `/tasks/0/task`) requires "a heading line exactly `## Files opened` followed by one line per
  file path … (nothing else under that heading); then one sentence that you opened no tool…". It gives no new heading,
  so the mandated sentence must fall under the files heading. The same brief says "Validate the JSON with python3
  json.load". The gate's planted reports (gate `:192-198`) never include a closing sentence. Running the self-test on
  a brief-conforming planted report would have caught this before the freeze.
- **Hole in the counter's structure (premature saturation):** the counter checks only that the gate's first add is an
  ancestor of the freeze (`count-c2.sh:188-189`), and then runs the freeze blob. Any gate edit between first add and
  freeze is invisible to it, even though the writer reports were committed (`b039dd4`) before the gate was first added
  (`32e287f`). A3 is exactly such an edit. If A3 had also allowlisted the line-105 pattern, the counter would print
  `C2=met` on a gate tuned after data [INFERENCE: I did not run that mutant; it follows from `:188-200`].
- **Stale lesson text:** `corpus/lessons/round-30.md:90` (M4) says "the fixed gate must print 0 there" (the round-29
  wave). The landed gate prints 9 there, by A2's design. This drift does not change C2.

## Impacted axes

- **Operability (C2):** no move; the miss stands.
- **Discernment and calibration (process):** A3 is an after-data loosening. It is disclosed, does not change the
  outcome, and should not be credited.
- **No axis harmed by C2's tool change:** `acted_lost=0` and `disallowed=0` (counter).

## Ruling recommendation

1. **Rule C2 a miss (`rejected-honest-stop` on C2).** The literal counter fails on both gate versions (A3: 1, A2: 4),
   and the claim's purpose (R5) also fails. The author's statement that all other counted conditions hold is
   accurate; I re-derived each one.
2. **Do not decide C2 on A3.** Record it as moot (a miss either way) and do not admit it as a precedent for changing a
   counted condition after data.
3. **Route R5 again with two named false-positive classes:** (i) a dotted prose token on a brief-mandated closing line
   (`CaseR30a.md:105`), and (ii) a non-H2 `Files opened:` list counted as missing (`CaseA210c.md:1`, locked into the
   expected set at gate `:176`).
4. **Smallest safe correction for next round, before data:**
   - Pin the gate blob hash in the contract at declaration. The counter then requires `blob(freeze, gate) ==` that
     hash, and any change requires a pre-data amendment.
   - Add a planted report that follows the brief to the letter (with its closing sentence) as a must-pass case in the
     self-test.
   - Have the gate stop parsing entries at the first non-list line under the files heading, or require a closing
     sentence under its own heading in the brief.
   - Drop `CaseA210c` missing-list from `expected_pairs`.
5. Fix the stale wording in `round-30.md:90` by appending a correction, not by editing the text.

## Tooling

No tools installed or updated (python3, git and bash were already present). The scratch gate copies and the
self-test temporary directory are under `/fast/scratch/hyaku/mori-r30-w2/CriticC2Verdict/`.
