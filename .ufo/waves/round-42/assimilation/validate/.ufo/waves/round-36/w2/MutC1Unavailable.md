# MutC1Unavailable — frozen C1 counter vs a 404/connection-close-as-`drifted` tool

Seat: `mori-r36-w2-MutC1Unavailable-28` (mutation tester, wave 2). 2026-10-23.
Claim under attack: C1 counter `count-c1.py` (P-C1), data tip `bf0df77fee4b6ef54a90aea09335c7617f125151`.
Lane HEAD at run time: `5a2fe05` (close-out). Lane read-only; only scratch files written besides this report.

## What this attacks

P-C1's falsifiability at the transport-failure boundary.  The counter's blind truth encodes a fetch that
never produced a body — a closed connection, a 404, a 500 — as `unavailable`, and content-change as
`drifted` (`count-c1.py:455-464`: one `"close"` row, then alternating 404/500).  A tool that collapses the
two axes by calling a 404 or a dropped connection "drifted" must be rejected by the counter; if the counter
still says `C1=met`, the predicate cannot distinguish "the source moved" from "the source was unreachable".

## Pins and environment (measured)

```
$ git -C mori-shokunin rev-parse HEAD                      -> 5a2fe05d2d403943912b8080ba1477a02cf2e9f5
$ git rev-parse bf0df77...:tools/mori-source-drift.py      -> 103965ac82df721d5d6edf17c7f917e5175579d9
$ git rev-parse HEAD:tools/mori-source-drift.py            -> 103965ac82df721d5d6edf17c7f917e5175579d9
$ git hash-object /fast/scratch/hyaku/mori-r36/MutC1Unavailable/pristine.py
                                                           -> 103965ac82df721d5d6edf17c7f917e5175579d9
$ sha256sum .ufo/waves/round-36/count-c1.py                -> 86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0
   (matches evidence/freeze-v2.txt; git blob b5888afe0c494c45e3a8abe06e6e60e849c101f0 = freeze-v3 pin)
$ sha256sum /fast/scratch/hyaku/mori-r36/MutC1Unavailable/pristine.py
                                                           -> 578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56
```

The counter's `PREDICATE` constant is byte-identical to `contract.md:22` (`P-C1:`), checked by importing the
frozen file and comparing strings: `predicate_equals_contract_line: True`.

Because the frozen predicate is evaluated at R, the real arm requires the worktree `corpus/` to equal R
(`count-c1.py:580`), and the current HEAD corpus no longer equals `bf0df77` (see caveats), all detector runs
used a clean clone of the lane at R:

```
$ git clone --quiet mori-shokunin /fast/scratch/hyaku/mori-r36/MutC1Unavailable/lane-tip
$ git -C lane-tip checkout --quiet --detach bf0df77fee4b6ef54a90aea09335c7617f125151
$ git -C lane-tip rev-parse HEAD          -> bf0df77fee4b6ef54a90aea09335c7617f125151
$ git -C lane-tip status --porcelain | wc -l -> 0
$ git -C lane-tip diff --quiet bf0df77 -- corpus; echo $? -> 0
```

## Mutant

Copied the committed tool (not the worktree file, which was concurrently edited — see caveats) to
`mutant.py`, then changed three lines, one purpose: `404` and connection close/error are reported as
`drifted` instead of `unavailable`; the 5xx retry path is untouched.  Line numbers are those of the
measured copy (identical to `git show bf0df77:tools/mori-source-drift.py`).

```diff
--- pristine.py
+++ mutant.py
@@ -135,13 +135,13 @@
                 if 500 <= code < 600 and attempt < FETCH_TRIES - 1:
                     time.sleep(2.0 if attempt == 0 else 8.0)
                     continue
-                return "unavailable", None
+                return ("drifted", None) if code == 404 else ("unavailable", None)
             return "unavailable", None
         except Exception:
             if attempt < FETCH_TRIES - 1:
                 time.sleep(1.0 if attempt == 0 else 3.0)
                 continue
-            return "unavailable", None
+            return "drifted", None
     return "unavailable", None
@@ -183,7 +183,7 @@
             else:
                 outcome, body = fetch(url)
                 if outcome != "body":
-                    state = "unavailable"
+                    state = "drifted" if outcome == "drifted" else "unavailable"
                 else:
                     state = classify(body, copy)
```

`sha256sum`: `pristine.py 578667ca…`, `mutant.py 26fbe0c4704ddfe1a8c9561c753b770da15000ebc427e32b62e5c4555833abfb`
(the third hunk is needed because `run()` maps any non-`body` outcome to `unavailable`; without it the
mutation would be inert.  The mutant keeps `fetch()`'s docstring unchanged, as a mutant does.)

## Detector — own tool (pristine) vs mutant vs restored, seed 11

Command (same for all three; the only variable is `--tool`):

```
python3 .../round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
  --repo /fast/scratch/hyaku/mori-r36/MutC1Unavailable/lane-tip \
  --tool /fast/scratch/hyaku/mori-r36/MutC1Unavailable/<file> --seed 11
```

**Pristine** (`pristine.py`, sha256 `578667ca…`) — `EXIT=0`:

```
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=11
```

**Mutant** (`mutant.py`, sha256 `26fbe0c4…`) — `EXIT=1`, killed:

```
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=5
blind_mismatch S022 tool=drifted truth=unavailable
blind_mismatch S073 tool=drifted truth=unavailable
blind_mismatch S124 tool=drifted truth=unavailable
blind_mismatch S151 tool=drifted truth=unavailable
blind_mismatch S287 tool=drifted truth=unavailable
real_arm=skipped
C1=unmet
seed=11
```

**Restored** (`mutant.py` rewritten from `pristine.py`; sha256 back to `578667ca…`) — `EXIT=0`:

```
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=11
```

The real arm is skipped for the mutant by the counter's own control flow (`count-c1.py:706`), so the kill is
blind-arm-only; the mutant's stdout has all 40 rows and no extraneous rows (`tool_rows=40`), i.e. the counter
did not kill it for a shape error.

### Why exactly five mismatches

`build_fixture` gives the 8 `unavailable` rows deterministically as 1 × connection close, then 4 × 404 and
3 × 500 (`count-c1.py:458-464`, keyed on `unavailable_seen`).  The mutant reclassifies the close and the four
404s (5 rows) and leaves the three 500s as `unavailable`, which still match.  The observed mismatch count is
therefore exactly the intended defect, and the counter demonstrably distinguishes transport failures the
mutant changed from the one sub-kind it did not.

Exit code did not flip: pristine and mutant both make the tool exit 1 (the blind fixture contains real
drifted rows).  The rejection rests on per-row comparison, not on the tool's exit status.

## Selftest receipts

```
$ python3 pristine.py --selftest
selftest exit_code            PASS
selftest row_states           PASS
selftest summary              PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)          exit 0

$ python3 mutant.py --selftest
selftest exit_code            PASS
selftest row_states           FAIL (got=[... ('S104','drifted'), ('S105','drifted') ...] want=[... ('S104','unavailable'), ('S105','unavailable') ...])
selftest summary              FAIL (summary=('8','2','1','3','0','2'))
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: FAIL (2/4)              exit 1
```

This is *not* the "selftest passes while the counter fails" strongest form: the tool's own selftest covers the
same 404-and-close rows and also fails.  The counter's kill is nevertheless independent — the counter's truth
is generated at run time from the hidden `(body, copy, status)` tuple, and the counter never executes the
tool's selftest.

## Seed matrix (same mutant, second draw)

`mutant42.py` (byte-identical to `mutant.py`, sha256 `26fbe0c4…`), seed 42, same command:

```
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=5
blind_mismatch S014 tool=drifted truth=unavailable
blind_mismatch S017 tool=drifted truth=unavailable
blind_mismatch S045 tool=drifted truth=unavailable
blind_mismatch S141 tool=drifted truth=unavailable
blind_mismatch S195 tool=drifted truth=unavailable
real_arm=skipped
C1=unmet
seed=42                                                          (process exit 1)
```

Different ids, same 5-row shape: the kill is seed-independent, as the fixture's close/404/500 split is
deterministic.

## Restoration evidence

```
$ cp pristine.py mutant.py && sha256sum pristine.py mutant.py
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  pristine.py
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  mutant.py
$ cmp pristine.py mutant.py && echo RESTORED_IDENTICAL
RESTORED_IDENTICAL
$ git -C mori-shokunin show bf0df77:tools/mori-source-drift.py | sha256sum
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  -
```

The restored run above (`C1=met`, `EXIT=0`) proves the detector's failure is attributable to the mutation and
not to the scratch environment.  `mutant42.py` is retained only as the seed-matrix artifact in scratch.

## Environment caveats (facts; not part of the probe, no remediation)

1. **The literal command at the current tip cannot baseline.** With the default repo (worktree at `5a2fe05`),
   `count-c1.py bf0df77 --tool pristine.py --seed 11` prints
   `blind_rows=40 … mismatches=0` / `real=unmet worktree_corpus_differs_from_rev` / `C1=unmet` (process exit 1).
   The worktree corpus differs from `bf0df77` in 5 files (`corpus/QUALITY.md`, `corpus/README.md`,
   `corpus/SOURCES.md`, `corpus/knowledge/source-drift-r36.md`, `corpus/lessons/round-36.md`), so the v2 guard
   at `count-c1.py:580` refuses.  Re-scoring R requires a checkout at R; all three runs above used
   `--repo <clean clone at bf0df77>`.
2. **The lane worktree tool was edited by a concurrent seat mid-wave.** At 16:14 my copy matched the committed
   blob `103965ac`; at 16:18 the worktree file had an uncommitted +47/−3 edit (public-destination guard,
   4 MiB read cap, selftest `S109`/`huge`) and by ~16:20 its blob was `f8d55760`.  Every measurement here uses
   the committed bytes at R (`103965ac`), never the worktree file.
3. **Freeze pin churn on contract.md (documentary, other seats own it).** `freeze-v3.txt` pins contract blob
   `f68a06c2` (state at `9ca8f2e`), but `bf0df77` carries `3fcfffcf` and `6827d6e`…`5a2fe05` carry `f505594b`.
   The P-C1 sentence itself is unchanged and still equals the counter's `PREDICATE` (checked above).
4. No tools were installed or upgraded; no pacman (host guard honoured).  The lane repo was not written —
   `git status` changes visible during the wave belong to concurrent seats (LOG.md, tools, w2 reports).

## Verdict

The frozen counter kills the mutant: on the same bytes the pristine and restored tool score `C1=met`
(exit 0) and the 404/connection-close-as-`drifted` tool scores `C1=unmet` (exit 1, 5 blind mismatches at
seed 11 and seed 42, all `unavailable → drifted`, no false positives on the 500 rows).  P-C1 is falsifiable
at the transport-failure boundary; no defect found in the counter for this probe.

VERDICT: PASS (mutant killed; no defect found)

Report: .ufo/waves/round-36/w2/MutC1Unavailable.md
