# Mo93M01Mut: mutation test of the frozen round-93 counters (w1)

Seat: Mo93M01Mut (mutation-tester, leaf). Entering revision `7b3fe9d5`; patch base `6d82b8d7`.
Frozen files checked at `6d82b8d7` (git blob sha256, first 16 hex): `count-c1.py` 98ed3e3ea9a14789,
`count-c2.py` a87ab2e467700df2, `controls-r93.sh` d6053c6135511422. The copies I mutated match these.
Scratch `/fast/scratch/hyaku/mori-r93/Mo93M01Mut` (removed at exit). No lane file, counter, control,
contract or evidence file was edited. The seat patch `w1/patches/Mo93M01Mut.patch` is 0 bytes (clone unchanged).

## Result

- Unmutated copy: all seven frozen controls read `unmet`, as the contract requires.
- Six single-point mutants, 42 control verdicts. Two mutants make a control read `met`:
  **m2** (forgery control) and **m5** (rename control). Under the task definition both are **survived: yes**.
- Four mutants (m1, m3, m4, m6) leave every frozen control `unmet`, so the round would not stop on them.
  They **escape** the frozen set. Supplemental fixtures (scratch only, not frozen, not in the contract)
  catch each one. See Findings.

## Mutants (one line changed in a scratch copy; `diff` confirmed; `ast.parse` ok; other scripts byte-identical)

| id | lane site | change | conjunct removed or altered |
|---|---|---|---|
| m1 | `count-c1.py:141` | `if ac and va and ac[:7] in va:` to `if ac and va:` | 7-char admission-hash prefix test |
| m2 | `count-c1.py:165` | `if patched != len(TWELVE):` to `if False:` | patched12 conjunct |
| m3 | `count-c1.py:80` | in `trio_count`, `head_lines(...)` (65536 chars) to `open(...).read(4096).splitlines()[:12]` | trio read window |
| m4 | `count-c1.py:169` | `if not census_ok:` to `if False:` | census conjunct |
| m5 | `count-c2.py:89` | `if home_lits != 0:` to `if False:` | HOME_RE conjunct |
| m6 | `count-c2.py:91` | `if vgp != 0:` to `if False:` | vgpnk_refs conjunct |

Run per mutant (six in parallel, each with its own TMPDIR; the frozen script run unmodified):
`TMPDIR=$S/tmp/mN bash $S/mut/mN/controls-r93.sh /home/vgpnk/Projects/shokunin/mori-shokunin $S/out/mN.txt`
The script exits 0 whatever the verdicts, so verdicts were read from the printed `C1=`/`C2=` lines.
m1-m4 only change `count-c1.py`, so their C2 rows equal base. m5/m6 only change `count-c2.py`, so their C1 rows equal base.

## Control verdicts (every control, every mutant)

"Survived" uses the task definition: yes if the control reads `met`.

| mutant | control | verdict (printed line, key fields) | survived |
|---|---|---|---|
| base | C1 do-nothing | unmet; adm_fail=12 patched12=0; checks admission,patched12 | no |
| base | C1 text-only | unmet; adm_fail=12 patched12=0 | no |
| base | C1 deletion | unmet; trio=86; checks trio,admission,patched12 | no |
| base | C1 forgery | unmet; adm_ok=19 patched12=11; checks patched12 | no |
| base | C2 do-nothing | unmet; home_literals=18 vgpnk_refs=18 | no |
| base | C2 deletion | unmet; tools=0 selftests=0/3 | no |
| base | C2 rename | unmet; home_literals=18 vgpnk_refs=0 | no |
| m1 | C1 do-nothing | unmet; claim_r92_true=1 adm_ok=19 patched12=0; checks patched12 | no |
| m1 | C1 text-only | unmet; claim_r92_true=1 adm_ok=19 patched12=0; checks patched12 | no |
| m1 | C1 deletion | unmet; trio=86 adm_fail=12; checks trio,admission,patched12 | no |
| m1 | C1 forgery | unmet; patched12=11; checks patched12 | no |
| m1 | C2 x3 | as base (unmet, unmet, unmet) | no |
| m2 | C1 do-nothing | unmet; checks admission | no |
| m2 | C1 text-only | unmet; checks admission | no |
| m2 | C1 deletion | unmet; trio=86; checks trio,admission | no |
| m2 | C1 forgery | **met** (rc=0): `C1=met trio=98 claim_r92_true=1 ... adm_ok=19 adm_fail=0 patched12=11 seven_same=7 census=ok` | **yes** |
| m2 | C2 x3 | as base | no |
| m3 | C1 do-nothing | unmet; trio=97; checks trio,admission,patched12 | no |
| m3 | C1 text-only | unmet; trio=97; checks trio,admission,patched12 | no |
| m3 | C1 deletion | unmet; trio=85; checks trio,admission,patched12 | no |
| m3 | C1 forgery | unmet; trio=97 patched12=11; checks trio,patched12 | no |
| m3 | C2 x3 | as base | no |
| m4 | C1 do-nothing | unmet; checks admission,patched12 | no |
| m4 | C1 text-only | unmet; checks admission,patched12 | no |
| m4 | C1 deletion | unmet; checks trio,admission,patched12 | no |
| m4 | C1 forgery | unmet; checks patched12 | no |
| m4 | C2 x3 | as base | no |
| m5 | C1 x4 | as base | no |
| m5 | C2 do-nothing | unmet; checks vgpnk_refs (home_literals=18 not checked) | no |
| m5 | C2 deletion | unmet; checks tools,selftests | no |
| m5 | C2 rename | **met** (rc=0): `C2=met home_literals=18 vgpnk_refs=0 tools=3 selftests=3/3 census=ok` | **yes** |
| m6 | C1 x4 | as base | no |
| m6 | C2 do-nothing | unmet; checks home_literals (vgpnk_refs not checked) | no |
| m6 | C2 deletion | unmet; checks tools,selftests | no |
| m6 | C2 rename | unmet; checks home_literals | no |

Raw output files are in scratch and are removed at exit; the lines above are copied from them.

## Supplemental fixtures (scratch, not frozen; extra evidence only)

Each fixture is a scratch clone at the entering tree with one change, committed on a scratch branch.
Each counter ran as `python3 -I <mutant>/count-cN.py HEAD --repo <fixture>`.

| fixture | change | counter | base | mutants (read as) | caught by fixture |
|---|---|---|---|---|---|
| p0 repaired | 12 `verified-at` values given the admission hash, `(orig)` kept | count-c1 | met | m1 met, m2 met, m4 met, m3 unmet (trio=97) | **m3** |
| p1 wrong hash | same, hash `0000000` | count-c1 | unmet (admission) | m1 **met**, m2 unmet, m3 unmet, m4 unmet | **m1** |
| p2 census broken | p0 plus one malformed `SOURCES.md` table row (too few fields) | count-c1 | unmet (census rc1) | m1 unmet, m2 unmet, m3 unmet, m4 **met** | **m4** |
| p5 repaired C2 | `/home/vgpnk` rewritten to `/srv` in the three tools, no vgpnk | count-c2 | met | m5 met, m6 met | (reference) |
| p4 vgpnk-only | p5 plus one non-path comment `# maintainer note: vgpnk` | count-c2 | unmet (vgpnk_refs=1) | m5 unmet, m6 **met** | **m6** |

p0 and p5 show the counters reach `met` on a repaired tree. No frozen fixture does this, so the frozen set never
checks the `met` branch.

## Findings

1. **m2 survives.** With the patched12 conjunct off, the forgery control reads `met` while printing `patched12=11`.
   The verdict contradicts its own printed field. This is the only frozen control where patched12 decides the verdict.
2. **m5 survives.** With the HOME_RE conjunct off, the rename control reads `met`. The contract says the regex
   clause is what refuses rename (contract C2, Rename control). Under the kill rule, a control that reads `met`
   stops the round, so m2 and m5 are the mutants the frozen set flags.
3. **m1 escapes.** Under m1 the do-nothing and text-only controls print `claim_r92_true=1` with `adm_ok=19`, although
   nothing was repaired. The verdict stays `unmet` only through patched12. No frozen control carries a wrong admission hash.
   p1 catches m1.
4. **m3 escapes, and the 4096 window is load-bearing on the entering tree.** The trio count is 98 with the 65536-char
   window and 97 with 4096 chars, and that moves printed `trio=` values in four controls without changing a verdict.
   Diagnostic: `corpus/knowledge/userspace-oom-killers-r26.md` (entering `7b3fe9d5`) has its `source:`/`verified-at:`/
   `recheck:` keys only beyond 4096 chars. This is a named-limit candidate missing from contract C1. p0 catches m3.
5. **m4 escapes.** No frozen fixture breaks `SOURCES.md`, so census never decides a verdict. The census validator
   fails on any non-13-field row (`scripts/sources-census.sh:635`, exit at `:805`). p2 catches m4.
6. **m6 escapes.** No frozen fixture has vgpnk occurrences with zero home literals. p4 catches m6.
7. **Frozen set coverage gap (no contract change this round).** The frozen controls contain no wrong-hash case, no
   census-broken case, no vgpnk-only case, and no repaired-met reference. Candidate controls for a later round:
   p0 (repaired reference), p1 (wrong hash), p2 (census broken), p4 (vgpnk only). Not added here: the contract and
   counters are frozen (kill rule).
8. **Observation, outside C2's predicate.** `count-c1.py:39` and `count-c2.py:39` hardcode
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`. The counters are outside `tools/`, so C2 does not
   count them. They are frozen and were not edited. Route to a later C2 follow-up.

## Checks run and not run

Run: baseline controls (1 run, `unmet` x7); six mutant control runs (42 verdicts); `diff` and `ast.parse` per mutant;
blob-hash check of frozen files at `6d82b8d7`; five supplemental fixtures with 16 counter runs; m3 diagnostic
(`git show 7b3fe9d5:corpus/knowledge/*`).
Not run: counters at the landing revision (L1 owns that step); the census validator directly beyond the counters'
own call; any mutant of `controls-r93.sh`.
Caveat: probe counters ran from the eval kernel without TMPDIR pinned; the counters use TemporaryDirectory and
no leftover `/tmp/tmp*` remained afterwards. Controls runs pinned TMPDIR to scratch.
Lane state seen during the run: lane HEAD `d8a9b28c` with other seats' uncommitted files. Results refer to the
frozen blobs at `6d82b8d7`, which the check above confirmed.

## Tooling

No installs or updates. Read `/home/vgpnk/.omp/agent/RULES.md` (operator directive; nothing needed). Host tools used:
`/usr/bin/python3` 3.14.8, `/usr/bin/git` 2.56.0, `/usr/bin/bash`. No pacman transaction.

## Evidence pointers

- Frozen mutation sites (lane): `.ufo/waves/round-93/count-c1.py:80,141,165,169`, `.ufo/waves/round-93/count-c2.py:89,91`.
- Frozen blobs at `6d82b8d7`: see the header hashes.
- Baseline and mutant verdicts: the table above (copied from scratch output files, removed at exit).
- Patch: `.ufo/waves/round-93/w1/patches/Mo93M01Mut.patch` (0 bytes; scratch clone unchanged).
