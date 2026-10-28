# Mo59MutationTester38 — counter selftest honesty (mutation probe)

Seat: mutation-tester. Scope: do the counter selftests exercise the same code
path as the measure path? Mutate a pure function; report whether selftest or
measure catches it. Read-only on the lane; all mutation on scratch copies under
`/fast/scratch/hyaku/mori-r59/Mo59MutationTester38/` (deleted after report).

Detector revision: lane HEAD `8ff344ff18924c1ea63d46c3b3969f9fea05bc51`
(worktree == freeze `60b3a76` for all three frozen files — verified by sha256
below). At HEAD, `tools/mori-register-check.py` and `tools/mori-settlement-scan.py`
exist (both scan/drift/trees/selftest arms live); the C2 entry/copies/registry
rows are not yet landed, so C2's `entry/rows/pins/tree` arms are `bad` at
baseline — inconclusive there, but every arm my mutants touch (tool-sha gate,
selftest arm, 12 hostile trees) is green at baseline.

## Static code-path analysis

`count-c1.py` `selftest()` (lines 214–236): six `chk()` calls, all constant-shape
probes (`len(REQUIRE)==2`, `BOUND[...].startswith`, `len(MANIFEST_REV)==40`,
`PIN != "0"*64`, `not FIXDIR.startswith("/")`, `EXPECT_SELFTEST.endswith("fail=0")`).
It calls **zero** functions used by `measure()` — not `sha256`, `git`,
`git_show`, `run_tool`, `materialize`, nor `eval` of any kind. The
`importlib.util.spec_from_file_location`/`here` scaffold at lines 215–218 is
dead code (loaded spec never executed). Separately, lines 155–157 compute a
`got` variable that is never read — dead code inside `measure` itself.
C1 selftest overlap with the measure path: **none**.

`count-c2.py` `selftest()` (lines 365–427): nine `chk`s — CLAIM/ROW regex
probes, `MIN_CLAIMS==10`, `ARTIFACTS` values under `.ufo/`, `len(REAL_SCAN)==5`,
plus a functional block (lines 391–425) that builds a synthetic root and calls
`eval_entry()` twice: once on a compliant tree (`synth_good`), once on a
frontmatter-less rewrite (`synth_no_frontmatter`). `eval_entry` IS the same
function `measure` runs on the real root and on all 12 hostile trees — genuine
shared-path coverage, unlike C1. But: it never touches `git`, `git_show`,
`measure`, the scan/drift/tree-copy arms, or the tool subprocess, and its pin
check is self-consistent — it fabricates claim pins with the same `sha256` it
later verifies against (line 408), so a format-preserving corruption of
`sha256` is invisible to it.

## Mutation matrix (each mutant = 1 line vs pristine; detectors: `--selftest`, then `measure` at HEAD)

| mutant | change | `--selftest` | `measure` @8ff344ff | verdict |
|---|---|---|---|---|
| c1-m1-sha | L50 `sha256` `+ "deadbeef"` | `C1_SELFTEST pass=6 fail=0` exit 0 — **SURVIVES** | `C1=unmet … failed=tool_sha` exit 1 — KILLED | selftest blind, measure catches |
| c1-m2-expect | L37 `EXPECT_SELFTEST` `pass=12`→`pass=11` | `pass=6 fail=0` exit 0 — **SURVIVES** (chk is only `.endswith("fail=0")`) | `C1=unmet selftest=bad … failed=selftest` exit 1 — KILLED | constant-chk shallow, measure catches |
| c2-m1-sha | L87 `sha256` → `return "f"*64` | `C2_SELFTEST pass=9 fail=0` exit 0 — **SURVIVES** | `C2=unmet … failed=…,tool_sha,…` exit 1 — KILLED | self-consistency blind spot confirmed |
| c2-m2-claims | L130 `len(claims) < MIN_CLAIMS` → `< 0` | `pass=9 fail=0` exit 0 — **SURVIVES** | `C2=unmet trees=bad … failed=…,tree:t05-few-claims:verdict,trees` exit 1 — KILLED | hostile tree catches, selftest doesn't |
| c2-m3-front | L81 drop `"coverage-map:"` from `FRONTMATTER` | `pass=9 fail=0` exit 0 — **SURVIVES** | `C2=unmet` line **byte-identical to pristine baseline** (same `failed=` list) — **SURVIVES** | survives all detectors — coverage finding |
| c2-m4-expect | L50 `EXPECT_SELFTEST` `pass=10`→`pass=9` | `pass=9 fail=0` exit 0 — **SURVIVES** | `C2=unmet selftest=bad … failed=…,selftest,…` exit 1 — KILLED | C2 has no expect-token chk at all |

An earlier c2-m1 variant (`+ "deadbeef"`, 72-char pin) WAS caught by C2
selftest — `FAIL synth_good` — because the corrupted pin broke the `CLAIM`
regex `[0-9a-f]{64}` on lines the selftest itself generated. That kill detects
the format break, not the digest corruption; the refined format-preserving
mutant above isolates the real blind spot.

## Survivors / gap characterization (bounded method)

Executed survivors: **c2-m3-front** — the frozen predicate requires "the four
frontmatter keys", but weakening enforcement to three keys is undetectable:
the only frontmatter hostile tree (`t01-no-frontmatter`, expect=`frontmatter`)
drops the whole header block, so it still emits `frontmatter:*` reasons under
the mutant; no tree removes exactly one key; selftest's negative case likewise
drops all four lines at once (L420). The mutation would also be invisible at a
compliant scoring revision, since a landed entry carrying all four keys scores
identically under pristine and mutated code.

Statically-derived additional survivor classes (not executed; evidence cited):

- `claims_min` boundary: `t05-few-claims` carries exactly **7** claims
  (`git show …t05…/wave-settlement-artifacts-r59.md | grep -c 'Quote:'` → 7;
  pristine `eval_entry` on a materialized t05 → `False ['claims_min:7']`).
  Any threshold `>7` (e.g. `MIN_CLAIMS - 1`, `< 9`, `< 11`) still emits
  `claims_min:7` — same verdict, same expect prefix → survives measure.
  `chk("min_claims")` pins the constant `MIN_CLAIMS` but not its use site, so
  `len(claims) < MIN_CLAIMS - 1` also survives selftest.
- `span:short` boundary (`len(q) < 3` → `< 2`/`≤`): `t11-quote-short`'s
  hostile quote is `` `ab` `` (2 chars, `offset:1`, expect=`span`); the copy's
  bytes at offset 1 are `\n ` (od: `{ \n   " s e a t`), so the quote fails the
  offset match and still yields `span:K1` → mutant survives measure; nothing
  in selftest covers `span:short` at all.

## Answer to the seat question

No — neither counter selftest exercises the same code path as the measure
path. C1's is purely decorative for the measure path (six constant probes,
zero shared functions, dead import scaffold, plus a dead `got` computation in
`measure`). C2's shares `eval_entry` and the grammar regexes but only on a
happy-path synthetic tree and one whole-block negative; it cannot see
corruption in `sha256` (self-generated pins), boundary mutants in the
`claims_min`/`span:short` gates, or completeness of the `FRONTMATTER` keyset.

The honest reading: the `selftest=` token in each measure output is the
**tool's** selftest (`REGCHECK_SELFTEST`/`SETSCAN_SELFTEST` run against
pinned bytes), not the counter's — counter `--selftest` is a pre-flight
constant sanity probe. All counter-mutant detection actually comes from
measure's hard anchors: the `PIN` sha gate (`tool_sha`), the tool's own
selftest output token, and the frozen hostile fixtures/trees. That layer is
genuinely behavioral — every mutating probe that touched a verdict-bearing
path was killed there — but its granularity is verdict-plus-expect-prefix, so
single-key/boundary weakenings inside `eval_entry` (the m3-front and the two
static classes above) are verdict-invisible.

Note: three selftests exist here (counter `--selftest`, tool
`REGCHECK_SELFTEST`, tool `SETSCAN_SELFTEST`); reports/receipts should keep
the names distinct.

## Recommendations (draft only — no contract/counter changes made)

1. C1 counter `--selftest`: either exercise real functions (e.g. run `sha256`
   on a known vector, `eval`-check one constant against a digest of the file)
   or be renamed to reflect that it only sanity-checks constants.
2. C2: add one hostile tree missing exactly `coverage-map:` (expect
   `frontmatter:coverage-map`) and one positive-control tree (empty expect
   file — `want_ok = not expect` already supports it), plus a tree probing a
   `claims_min` boundary above its current 7-claim floor.
3. Counter selftests could pin `EXPECT_SELFTEST`/`FRONTMATTER` by value, not
   by suffix/shape.

## Integrity / restoration evidence

- Lane files byte-identical before and after; equal to freeze `60b3a76`:
  `count-c1.py` `2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd`,
  `count-c2.py` `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be`,
  `contract.md` `427fca0bf2a928133c09b37746e58a2d98c6c551651046f31320531a43de107e`
  (sha256, worktree vs `git show 60b3a76:` — all equal).
- `git status --porcelain .ufo/waves/round-59/` post-run: only
  `?? w1.ready.dispatched`, `?? w1/` (wave artifacts; this report).
- Mutations applied only to copies under
  `/fast/scratch/hyaku/mori-r59/Mo59MutationTester38/mut/` — scratch tree
  deleted after this report; no git mutations anywhere (all lane access via
  `git show`/`ls-tree`/`cat-file`).
- No tools installed or updated; disk-guard status green at start (592.6G
  free on /fast/scratch/hyaku).

Verdict: **adversarial finding** — counter selftests do not cover the measure
path (C1: zero; C2: partial with a self-consistency blind spot), and one
executed mutant (frontmatter-keyset weakening) plus two statically-derived
boundary mutant classes survive all shipped detectors.
