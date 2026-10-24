measured 2026-10-23T19:05Z

# ExecSelftests — mori round 36 wave 2 (three tool self-tests + falsification of their discrimination)

Seat: `mori-r36-w2-ExecSelftests-11` (executor, leaf).
Item attacked: the three round-36 registered tool self-tests —
`tools/mori-source-drift.py --selftest` (C1 probe), `tools/mori-sources-appendonly.py --selftest` (C2 gate),
`tools/mori-index-clean.sh --selftest` (QUALITY 103 gate) — as *evidence*: do the three PASS lines actually
discriminate, i.e. would a broken tool also print PASS?

Scope: read-only. No lane file was edited by this seat except this report. No `git add/commit/push/fetch/reset`,
no mutating `jj` command. The lane's real tools were never edited; every mutant was a **copy** under
`/fast/scratch/hyaku/mori-r36/ExecSelftests/` and was passed to the lane's frozen counters via `--tool FILE`
(controls/mutants only, never the lane's real tool). No remediation, no kills, no config edits, no installs
(tool, version, channel, reason: none — no install was needed).

---

## 1. The assigned target — three PASS lines, reproduced

Commands (exactly as assigned), lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`, lane tip `6827d6e`:

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 tools/mori-source-drift.py --selftest
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 tools/mori-sources-appendonly.py --selftest
cd /home/vgpnk/Projects/shokunin/mori-shokunin && bash tools/mori-index-clean.sh --selftest
```

Observed output and exit codes:

```
selftest exit_code            PASS
selftest row_states           PASS
selftest summary              PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)
EXIT=0
```

```
MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0
EXIT=0
```

```
MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0
EXIT=0
```

**Three PASS lines, three exit 0.** The assigned target is met.

Robustness of those three lines (same commands, three consecutive runs each; outputs byte-identical across runs):

```
drift run1 exit=0 / run2 exit=0 / run3 exit=0 ; cmp d.1 d.2 && cmp d.2 d.3 -> drift_deterministic
appendonly run1 exit=0 / run2 exit=0 / run3 exit=0 ; cmp a.1 a.2 && cmp a.2 a.3 -> appendonly_deterministic
index run1 exit=0 / run2 exit=0 / run3 exit=0 ; cmp i.1 i.2 && cmp i.2 i.3 -> index_deterministic
```

Re-run from a foreign cwd with a foreign `TMPDIR`
(`cd /tmp && TMPDIR=/fast/scratch/hyaku/mori-r36/ExecSelftests/tmpwork`): all three PASS, exit 0, and the
scratch `TMPDIR` was left **empty** (`ls -A "$TMPDIR"` → no output) — the self-tests clean up after themselves.

Tool bytes at `6827d6e` (`git hash-object`, matching `evidence/freeze-v3.txt:16-18`):

```
103965ac82df721d5d6edf17c7f917e5175579d9  tools/mori-source-drift.py
dfb5040b159f7a0b4afedc90a633d997352908f0  tools/mori-sources-appendonly.py
d171da39f667e5d3af6f2b76f0481a7f0c3a8a4  tools/mori-index-clean.sh
```

sha256 of the same three files (unchanged before and after every run in this seat):

```
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  tools/mori-source-drift.py
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  tools/mori-sources-appendonly.py
cc5cf667f2603c47c4bc0089c748fe72ccd2f77fc34d1a2fd7ea1f815da759d7  tools/mori-index-clean.sh
```

---

## 2. Are the PASS lines meaningful? — mutation battery (the falsification half of this seat)

Method: copy each lane tool to scratch, apply one rule-destroying mutation, run the tool's **own** self-test
against the copy. A self-test that prints PASS on a broken copy is a self-test that does not discriminate.
Every mutant below is a scratch copy; the lane tool is byte-identical before and after (sha256 above).

### 2a. Self-tests that DO discriminate (mutant killed → self-test printed FAIL)

| mutant (scratch copy) | rule destroyed | self-test result |
|---|---|---|
| `drift_m1.py` | `excerpt` ⇄ `drifted` inverted | `MORI_SOURCE_DRIFT_SELFTEST: FAIL (3/4)`, exit 1 |
| `drift_m2.py` | newest copy → **oldest** copy (S101 decoy) | `FAIL (2/4)`, exit 1 |
| `drift_m3.py` | `unavailable` → `fresh` | `FAIL (2/4)`, exit 1 |
| `drift_m4.py` | sha-only (no `excerpt` rule) | `FAIL (2/4)`, exit 1 |
| `drift_m6.py` | connection error → `fresh` | `FAIL (2/4)`, exit 1 |
| `drift_vac_nooutput.py` | prints no row lines | `FAIL (3/4)`, exit 1 |
| `drift_vac_always_fresh.py` | every row `fresh` | `FAIL (1/4)`, exit 1 |
| `drift_e1_always_exit0.py` | always exit 0 | `FAIL (3/4)`, exit 1 |
| `drift_e3_noexit2.py` | setup error → exit 0 | `FAIL (3/4)`, exit 1 |
| `app_m1.py` | `deleted` arm removed | `FAIL deleted row: deleted: want ['S002'] got []` — `pass=7 fail=1`, exit 1 |
| `app_m2.py` | `MUTABLE = ()` (status/recheck/used-by become immutable) | `FAIL mutable-only edit: ids: want [] got ['S001']` — `pass=7 fail=1`, exit 1 |
| `app_m3.py` | `round_changed` endpoint-only | `FAIL` on 4 cases — `pass=4 fail=4`, exit 1 |
| `app_m4.py` | `superseded` list emptied | `FAIL superseding row: superseded: want ['S001'] got []` — `pass=7 fail=1`, exit 1 |
| `app_m6.py` | a superseder removes the id from `ids` | `pass=7 fail=1`, exit 1 |
| `app_m8.py` | endpoint compared against *previous* commit, not first ancestry | `pass=6 fail=2`, exit 1 |
| `app_m9_true_linepos.py` | rows keyed by **line position**, not id | `FAIL row reorder: ids: want [] got ['S001','S002']` — `pass=7 fail=1`, exit 1 |
| `app_vac_empty_summary.py` | always prints an empty summary | `pass=4 fail=4`, exit 1 |
| `idx_m1.sh` | intent-to-add detection removed from porcelain v1 | `MORI_INDEX_CLEAN_SELFTEST pass=3 fail=1`, exit 1 |
| `idx_m2.sh` | staged count forced to 0 | `pass=3 fail=1`, exit 1 |
| `idx_m3.sh` | always verdict "clean" | `pass=2 fail=2`, exit 1 |

21 mutants killed. The three self-tests are **not** vacuous: they catch inversion, decoy-copy selection, missing
states, missing arms, wrong endpoint, wrong row keying, missing exit codes, and the do-nothing shape.

### 2b. Self-tests that do NOT discriminate (mutant survived → self-test still printed PASS)

These are the residual findings. Each is a **coverage gap in the self-test**, not a defect in the shipped tool
(§3 verifies the shipped tool's behaviour directly on each of these branches).

| mutant (scratch copy) | rule destroyed | self-test | frozen counter |
|---|---|---|---|
| `drift_m5_500_as_body.py` | HTTP 500 treated as a body | `PASS (4 cases)`, exit 0 | **C1=unmet** (blind 3 mismatches) |
| `drift_m7_no_429_retry.py` | 429 retry / `Retry-After` handling removed | `PASS (4 cases)`, exit 0 | **C1=unmet** |
| `drift_e2_always_exit1.py` | always exit 1 (never 0) | `PASS (4 cases)`, exit 0 | **C1=met** (survived) |
| `app_m7_nobase_exit0.py` | without `--round-base`, exit code always 0 | `pass=8 fail=0`, exit 0 | **C2=met** (survived) |
| `app_h1b_fixed_idx_correct.py` | columns by fixed index, not header position | `pass=8 fail=0`, exit 0 | **C2=met** (survived) |
| `app_h2_unstripped.py` | cells compared unstripped | `pass=8 fail=0`, exit 0 | **C2=met** (survived) |
| `idx_m4_no_cap.sh` | `MAX_PATHS` cap removed | `pass=4 fail=0`, exit 0 | n/a (no counter) |
| `idx_m5_no_disagree_check.sh` | porcelain v1/v2 disagreement check removed | `pass=4 fail=0`, exit 0 | n/a (no counter) |

Root causes, each located in the lane source:

- `tools/mori-source-drift.py:259` — the fixture registers `routes["/boom"] = (500, b"server error\n")` but **no
  registry row ever references `/boom`** (rows use `/fresh`, `/excerpt`, `/drifted`, `/gone`, `/close`, `/trail`;
  verified by `grep -oE '%s/[a-z]+'` → no `boom`). The 5xx branch at
  `tools/mori-source-drift.py:135` (`if 500 <= code < 600 and attempt < FETCH_TRIES - 1`) is therefore never
  exercised by the self-test. The frozen counter **does** kill this mutant, so the C1 claim is not affected.
- `tools/mori-source-drift.py:120` — the 429 / `Retry-After` branch has **no fixture row at all** (no 429 route is
  registered). The frozen counter also kills this mutant (C1=unmet), so again the claim is not affected.
- `tools/mori-source-drift.py:316` — the self-test asserts `rc == 1` only. The tool's own contract
  (`tools/mori-source-drift.py:197`, `return 1 if counts["drifted"] else 0`) also defines **exit 0 when
  `drifted=0`**, and that branch is never asserted by the self-test; the counter's blind arm accepts `rc in (0, 1)`
  (`.ufo/waves/round-36/count-c1.py:555`, `:631`), so `drift_e2_always_exit1` survives both.
- `tools/mori-sources-appendonly.py:410` — every self-test case is invoked **with** `--round-base`, so the
  no-`--round-base` exit branch at `tools/mori-sources-appendonly.py:495`
  (`return 1 if (result["ids"] or result["deleted"]) else 0`) is never exercised; the counter also always passes
  `--round-base` (`.ufo/waves/round-36/count-c2.py:601`, `:629`), so `app_m7_nobase_exit0` survives both.
- `tools/mori-sources-appendonly.py:162` (`immutable_indices`) — the **header-position** rule is never
  distinguished, because every fixture and every counter sandbox writes the canonical column order
  (`.ufo/waves/round-36/count-c2.py:261` writes `"| " + " | ".join(COLUMNS) + " |"`). A fixed-index
  implementation is indistinguishable (see §3d).
- `tools/mori-sources-appendonly.py:151` (`parse_registry` strips every cell) — this makes `imm_key`'s own
  `.strip()` redundant, so `app_h2_unstripped` is a *semantically equivalent* mutant, not a real gap.
  Independently confirmed: the counter's own parser strips identically
  (`.ufo/waves/round-36/count-c2.py:124`).
- `tools/mori-index-clean.sh:136` (`MAX_PATHS` cap) and `tools/mori-index-clean.sh:110` (porcelain v1/v2
  disagreement → exit 2) have **no** self-test case: the four cases are clean / `add -N` / `add` / not-a-repo
  (`tools/mori-index-clean.sh:162`, `:171`, `:182`, `:194`). No frozen counter covers this tool.

### 2c. Mutants that were *equivalent*, not survivors (checked, not assumed)

- `app_m5_line_position.py` — survived the self-test, so I checked whether it was a real gap. Differential test
  over 12 randomized histories (append / edit / delete / supersede ops) plus the lane tip: **identical=12
  differing=0** on stdout *and* exit code. It is an equivalent mutant (the `cid not in first` clause is dead code
  because every tip id is in `first`), so it is **not** counted as a gap.
- `app_h2_unstripped.py` — equivalent, see above.

---

## 3. The shipped tools are correct on every branch the self-tests leave uncovered

Each residual mutant was checked against the **real lane tool** on the branch the self-test misses.

**(a) HTTP 500 → `unavailable` (drift).** Real tool against a local server serving 500/418/429/200:

```
REAL TOOL exit: 0
S001 unavailable      (500)
S002 unavailable      (418)
S003 unavailable      (429)
S004 fresh            (200)
MORI_SOURCE_DRIFT rows=4 fresh=1 excerpt=0 drifted=0 unavailable=3 no-copy=0
```

The mutant on the same fixture prints `S001 drifted` (exit 1) — i.e. the shipped tool implements the rule and the
self-test simply does not cover it.

**(b) 429 retry / `Retry-After` (drift).** Real tool against a server that always answers 429 with
`Retry-After: 0`: `S001 unavailable`, and the server **saw 3 requests** (the retry loop at
`tools/mori-source-drift.py:120-134` ran). Correct.

**(c) `drifted=0` → exit 0 (drift).** Same 4-row fixture above (no drifted row): `REAL TOOL exit: 0`. Correct.

**(d) Header-position columns (append-only).** The only case where the shipped tool and a fixed-index mutant
diverge, built with correctly named cells and a **permuted** header (`status` at index 1, `anchor` at index 7),
changing only the mutable `status` cell — which the contract says is *not* a violation:

```
PERMUTED header, status-only change (contract: mutable -> no violation):
  REAL           exit=0 | appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  MUTANT_h1b     exit=1 | changed S001 superseded_by=- | appendonly_violations=1 ids=[S001] ... round_changed=[S001]
CANONICAL header, status-only change (control):
  REAL           exit=0 | appendonly_violations=0 ids=[] ...      (both agree here)
```

The shipped tool reads the header (`tools/mori-sources-appendonly.py:162` → `immutable_indices(colmap)`) and is
right; the fixed-index mutant is wrong. The gap is that no self-test and no counter sandbox permutes the header.

**(e) No-`--round-base` exit code (append-only).** Real tool without `--round-base` on an immutable-cell edit:
`exit=1`, `appendonly_violations=1 ids=[S001] ...`; with `--round-base`: `exit=1`,
`round_changed=[S001]`. Both branches correct (`tools/mori-sources-appendonly.py:494-495`).

**(f) `MAX_PATHS` cap (index-clean).** Real tool against a repo with 25 staged paths:
`MORI_INDEX_CLEAN staged=25 intent_to_add=0`, 20 `..._PATH` lines, `MORI_INDEX_CLEAN_MORE 5`, exit 1. Correct.

**(g) porcelain v1/v2 disagreement (index-clean).** Real tool, with v1 ITA detection removed, is refused rather
than mis-reported: `MORI_INDEX_CLEAN_ERROR intent-to-add disagreement in <repo>: porcelain v1=0 porcelain v2=1`,
exit 2. The guard at `tools/mori-index-clean.sh:110-113` works.

---

## 4. The lane's own claims re-measured with the frozen counters (read-only, scratch clone)

Because the lane worktree's `corpus/` is **currently dirty** from in-flight sibling seats
(`git status --porcelain corpus/` → ` M corpus/SOURCES.md`, ` M corpus/lessons/round-36.md`), the C1 real arm
refuses to run in the lane (`count-c1.py:575-580` requires `corpus/` to equal the revision):

```
=== count-c1 in the LANE now ===
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real=unmet worktree_corpus_differs_from_rev
C1=unmet
=== count-c2 in the LANE now ===
blind arm: 24/24 sandbox histories matched the hidden truth (2.6s; coverage: deletions=23 changed-back=15 superseded=7)
real arm: pass (0.4s)
C2=met
```

That `C1=unmet` is a **worktree-state artifact, not a claim failure**. On a scratch clone of the same commits with
a clean `corpus/`, both counters reproduce the receipts:

```
C1 at 6827d6e (clean clone):
  blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
  real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
  C1=met   seed=3240224627795134842   exit 0

C1 at bf0df77 (clean clone):
  blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
  real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
  C1=met   seed=5570394790754296087   exit 0

C2 at 6827d6e (clean clone):
  blind arm: 24/24 sandbox histories matched the hidden truth
  real arm: pass (0.7s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  C2=met   seed=4617537939429368086   exit 0
```

Both `evidence/c1-after.txt` and `evidence/c2-after.txt` reproduce byte-for-byte in substance at the landed tip.

Counter and predicate identity re-checked (frozen bytes unchanged):

```
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  .ufo/waves/round-36/count-c1.py
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  .ufo/waves/round-36/count-c2.py
```

matching `evidence/freeze-v2.txt:3-4`. The predicate sentences P-C1/P-C2 are unchanged between the frozen
contract and the current one (`diff` of the `^P-C1:` / `^P-C2:` lines → identical).

---

## 5. Lane hygiene and side effects of this seat

- Lane index unchanged by the index-clean tool (read-only guarantee verified):
  `index_sha_before=96f905a2f505121d791fee3dfe288243e7cc57a75489fcfb7b64b338c7bb3ad6`,
  `index_sha_after=` same, `mtime_before=1792780426 after=1792780426` → `INDEX_UNCHANGED`.
- Running all three self-tests leaves the lane's `git status` byte-identical:
  `before=6fef23c095733f47a5edca62acc75de483f96d6b9a5110639e438fc46b643f16 -`,
  `after=` same → `LANE_STATUS_UNCHANGED`.
- The three tool sha256s are identical before and after all runs (§1).
- No lane file was written by this seat except this report. All scratch (mutants, probe repos, the scratch clone)
  lives under `/fast/scratch/hyaku/mori-r36/ExecSelftests/`.
- `git diff --stat tools/ corpus/` after the runs shows **no** change to the three tools.

---

## 6. Findings, ranked

1. **The three self-tests PASS and are discriminating.** 21 rule-destroying mutants are killed (inversion, decoy
   copy, missing states, missing arms, wrong endpoint, wrong row keying, missing exit codes, do-nothing). The
   three PASS lines are evidence, not decoration. No claim defect found here.
2. **Self-test coverage gap (drift), non-claim-affecting.** `tools/mori-source-drift.py:259` registers a
   `/boom` (500) route that no fixture row references, so the 5xx branch
   (`tools/mori-source-drift.py:135`) is untested by the self-test; the 429 branch
   (`tools/mori-source-drift.py:120`) has no fixture at all. The frozen counter kills both mutants
   (C1=unmet), and the shipped tool is correct on both branches (§3a, §3b). Residual risk is confined to the
   self-test, not to the C1 receipt.
3. **Self-test + counter coverage gap (drift), exit-code branch.** The `drifted=0 → exit 0` contract
   (`tools/mori-source-drift.py:197`) is asserted by neither the self-test (`:316` asserts `rc == 1` only) nor
   the counter (`count-c1.py:555`, `:631` accept `rc in (0, 1)`). An always-exit-1 tool passes both. The shipped
   tool is correct (§3c). This is the only gap that touches a **documented** exit-code rule that no witness in
   this round exercises.
4. **Self-test + counter coverage gap (append-only), two branches.** The no-`--round-base` exit branch
   (`tools/mori-sources-appendonly.py:495`) is exercised by neither the self-test (`:410`) nor the counter
   (`count-c2.py:601`, `:629`); and the **header-position** column rule
   (`tools/mori-sources-appendonly.py:162`) is never distinguished because every fixture and every counter
   sandbox uses the canonical column order (`count-c2.py:261`). The shipped tool is correct on both (§3d, §3e).
   Note the shipped tool's behaviour *is* correct here, so this is a witness gap, not a behaviour gap.
5. **Self-test coverage gap (index-clean).** `MAX_PATHS` cap (`tools/mori-index-clean.sh:136`) and the
   porcelain v1/v2 disagreement guard (`tools/mori-index-clean.sh:110`) have no self-test case, and no frozen
   counter covers this tool at all. The shipped tool is correct on both (§3f, §3g).
6. **Operational hazard for the L1's post-integration re-score (not a claim defect).** `count-c1.py`'s real arm
   requires the *worktree* `corpus/` to equal the revision (`.ufo/waves/round-36/count-c1.py:575-580`). While
   sibling seats have uncommitted `corpus/` edits, a re-score run **in the lane** returns
   `real=unmet worktree_corpus_differs_from_rev` → `C1=unmet` even though nothing about the tool changed
   (reproduced twice: §4). A re-score must therefore be run against a clean `corpus/` tree (or a clone), and
   the `C1=unmet` seen in the dirty lane is not a finding about the claim.
7. **No freshness admission is inferred from C1 anywhere in the lane.** Checked the committed tree at `bf0df77`
   and at `6827d6e`: `corpus/lessons/round-36.md:10` records C1 as "**admitted as technique; claim lands
   `unprovable`**" and states no freshness verdict is carried; `SCORECARD.md:2012` labels the receipt
   "`C1=met` as byte-behavior evidence"; `SCORECARD.md:2017` records C1 as **unprovable**; the round-36
   `SCORECARD.md` freshness **score** cell still reads `5` with "round 28 (improved, score held)" — unchanged
   by round 36; `corpus/README.md` and `corpus/knowledge/source-drift-r36.md` both carry the "no freshness
   verdict is claimed" wording; `SKILL.md:872` types the tool as `probe`, not `gate`. QUALITY 105
   (`corpus/QUALITY.md:837-843`) requires the drifted→source-change comparison before a witness is used as a
   target. Nothing infers freshness admission from the byte receipt.

---

## 7. Verdict

**VERDICT: PASS** — the assigned target holds (three PASS lines, exit 0 each, deterministic, hermetic, lane
untouched) and the three self-tests are shown to discriminate: 21 rule-destroying mutants are killed. No defect
in the C1 or C2 claims was found by this seat. The residuals in §6.2–§6.5 are **witness-coverage gaps in the
self-tests (and, for two branches, in the frozen counters)** where the *shipped* tools are verified correct by
direct measurement (§3) and, for the two drift mutants, the frozen counter independently kills them. §6.6 is a
re-score procedure hazard for the L1, not a claim defect; §6.7 records that no freshness admission is inferred
from C1.

**Recommended (next-round, non-blocking):** add one drift fixture row hitting the registered `/boom` route and
one 429 route; assert `rc == 0` for a drifted-free fixture; add an append-only self-test case without
`--round-base` and one with a **permuted** header; add index-clean cases for the `MAX_PATHS` cap and the
porcelain-disagreement guard. These are r37 debt items, not remediation for this round — no change was made here.
