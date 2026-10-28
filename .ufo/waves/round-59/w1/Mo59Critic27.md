# Mo59Critic27 — counter-honesty audit: self-graded arms in count-c1.py / count-c2.py

Seat: critic, lane `mori-shokunin`, round 59 w1. Read-only audit + counter
executions under scratch `$HYAKU_SCRATCH/mori-r59/Mo59Critic27/` (cleaned).
Freeze `60b3a76a` / `ccfd554e`; entering `2b9f0397`; observed tip `7b86704d`.

## Verdict

**No counterexample to met-ness.** Both counters behaved correctly on the two
live observations available (C1 met at HEAD; C2 falsified a real violation then
went met after the lane fix). **But the self-graded-arm audit lands hard:** for
C1, every semantic subclaim of the frozen predicate ((a) unique-register
identity, (b) key/name/pointer binding, (c) MANIFEST `rounds[832]` binding) is
graded by the pinned tool's own JSON, not re-derived by the counter. For C2,
the `scan`/`drift`/`selftest` arms are tool-graded while the `entry`/`pins`/
`rows`/`tree`/`trees` arms are genuine second-implementation checks.

## Provenance (the premise holds)

`git log` — contract, both counters, both tools, all fixtures/expects landed in
one commit `ccfd554e` (amended `60b3a76a`), author+committer
`mori-shokunin <mori@shokunin.local>`. Same-author counter/tool is structural;
the only independence available is implementation-level (counter re-derives vs
delegates). On that axis the two counters differ sharply.

## Per-arm independence

### C1 (`.ufo/waves/round-59/count-c1.py`, 277 lines)

| arm | independent? | evidence |
|---|---|---|
| tool sha→PIN | YES | counter re-sha256s `git show R:tool` (L96-99) |
| `selftest` | NO — tool-self-reported | L108-114: `rc==0 and EXPECT_SELFTEST in stdout`; no check the 12 cases ran/are sound. Mitigated: tool selftest is functional (tools/mori-register-check.py L239-282, real synthetic cases) and the fixture arm exercises `check()` independently |
| `fixtures` | PARTIAL | L122-163: unmet-bit is real discrimination, but reason match is **coverage-only** (`all(any(r.startswith(e))`); a tool emitting all 6 unique prefixes always passes — 13 fixtures collapse to 6 prefixes: `binding, keys, pointers, manifest:name, manifest:lane, manifest, manifest:lane_round`. Extras unpenalized; **fixture count not asserted** (only `if not dirs: fixtures_absent`); `got` (L151-154) is dead code |
| `real` | NO — fully tool-graded | L187-194: `verdict` and `bound` read from tool JSON; counter never parses SCORECARD.md or MANIFEST.json itself. `--require` keys are fed to the tool then echoed back into `bmap` keys — the tool can satisfy the check by parroting its own argv |
| `pointers` | PARTIAL | existence counter-verified via `git cat-file -e` (L178-183); completeness (omitted/broken pointer in register) is tool-graded |
| counter `--selftest` | n/a | 6 constant tautologies (L219-236: prefix/length/nonzero checks); zero functional coverage — `selftest=ok` oversells |

**C1 net: zero counter-side re-derivation of the register/manifest semantics.
The only counter-proven bits: tool-bytes identity, pointer existence,
unmet-on-hostile-fixtures.**

### C2 (`.ufo/waves/round-59/count-c2.py`, 464 lines)

| arm | independent? | evidence |
|---|---|---|
| tool sha→PIN | YES | L199-203 |
| `selftest` | NO — tool-self-reported | L208-215; tool selftest functional (10 cases) but unverified |
| `scan` | NO — tool-graded | L220-244: verdict + `members==seats` read from tool JSON; counter does not re-parse the five committed artifacts; `all()` over `out["files"]` is vacuously true on a partial/empty list — file count/identity never asserted |
| `drift` | NO — single bit | L247-258: `rc != 0` only; crash/parse-error indistinguishable from a correct FAIL judgment; verdict string unchecked |
| `tree` (copies byte-equal) | YES | L261-273: counter sha256s each `sources-r59` copy vs its `.ufo` artifact at R |
| `entry`/`rows`/`pins`/`claims`/`files` | YES — real second implementation | `eval_entry` (L100-190): own regex grammar, byte-exact quote span checks (line/offset), sha-pin checks, SOURCES row cell checks. Proven live this round (below) |
| `trees` (12 hostile trees) | PARTIAL | exercises `eval_entry` (tool-independent) but same coverage-only prefix matching (L340-350) and **count not asserted**; no committed positive-control tree (empty `expect` ⇒ `want_ok`); only positive controls are the synthetic selftest + the real entry |

## Live evidence (commands run, outputs)

```
$ python3 count-c1.py --selftest        → C1_SELFTEST pass=6 fail=0   (rc 0)
$ python3 count-c2.py --selftest        → C2_SELFTEST pass=9 fail=0   (rc 0)
$ python3 count-c1.py HEAD --scratch …  → C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD   (rc 0)
$ python3 count-c2.py HEAD --scratch …  → C2=unmet … entry=bad … claims=14 files=7 failed=entry   (rc 1)
   (run raced lane commit be737211: K11 cited w1-results-r53.json, outside
    the frozen 6-file ARTIFACTS map → eval_entry emitted files:outside.
    The arm fired on real data — genuine falsification signal.)
$ python3 count-c2.py 7b86704d --scratch … → C2=met … entry=ok … claims=13 files=6   (rc 0)
   (after lane demoted K11 to prose; 13 claims over exactly the 6 pinned copies)
```

Also verified: landed tools sha256-match frozen PINs
(`38b733d8…472b8`, `4c04bf21…5ac9a9`); tools/fixtures absent at entering
`2b9f0397` (do-nothing arms hold); 13 fixture dirs + 12 tree dirs present at
HEAD with frozen expects.

## Defects (fixable, counter bytes frozen — next-round lessons)

1. Coverage-only reason matching in both hostile arms (C1 L157, C2 L345-349):
   extras unpenalized, 13→6 and 12→12 prefix collapse. Require exact reason-set
   equality (or ≤ expected set) + assert committed dir count.
2. C1 `real` arm trusts `out["bound"]` verbatim; smallest fix is a counter-side
   mini-parser of the `## Capabilities` table + MANIFEST `rounds[832]` cell
   check, mirroring `eval_entry`.
3. C2 `scan` arm: assert `len(files)==len(REAL_SCAN)` and re-derive
   members==seats counter-side (artifacts are committed JSON); `drift`: require
   `rc!=0 AND verdict=="SETTLEMENT_SCAN_FAIL"`.
4. C1 counter selftest is 6 tautologies; C2's has 2 functional cases. Selftest
   arms are smoke signals, not correctness proof — acceptable in the met
   conjunction only because hostile arms exist.

## Impacted axes

- **Calibration (C1):** evidence quality overstated — `real=ok`/`selftest=ok`
  are tool-graded; counter-proof reduces to sha-pin + pointer-existence +
  hostile-unmet-bit.
- **Depth (C2):** entry-path arms are independently proven (including a live
  falsification this round); tool-path arms (`scan`, `drift`, `selftest`) are
  self-graded single-bit checks.

## Bounded method

Static read of both frozen counters + both tools + all 25 expect files; auth
provenance via `git log`/`ls-tree`/`cat-file`; dynamic probes = the two
counter `--selftest`s and three counter runs (C1@HEAD, C2@be737211-race,
C2@7b86704d) under seat scratch. Did not inject hostile tools (PIN binds bytes;
a hostile tool fails `tool_sha` by construction, so the residual risk is
authoring-time REF-equivalence, which is what this table reports).
