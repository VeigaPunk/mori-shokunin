# ReviewOracleRename — static review of `.ufo/waves/round-23/oracle-rename.py`

Seat: `MadoR22-2.ReviewOracleRename-8` (reviewer, leaf, no delegation).
Target: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/oracle-rename.py`
Baseline: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/oracle-reconcile-v2.py`
Method: **static only**. Nothing was executed — no oracle run, no tool run, no fixture creation, no
build/test/lint. No tool was installed or updated in this review (none needed); the host toolchain
(`git`, `python3`) was used read-only for diffing and hashing.

---

## 0. Verified anchors (sha256, computed read-only)

| Artifact | sha256 | Declared in | Match |
|---|---|---|---|
| `.ufo/waves/round-23/oracle-rename.py` | `a55b2b50d3e7447a1d5312c8b066a13137a6a6895f0343b3240ebf081d97c5f2` | `frozen/c1-requirements.json:oracle_sha256` | ✅ |
| `.ufo/waves/round-22/frozen/fixture-builder-v2.py` | `1b3e16f74a032e066dd881c15affbc4401f2f44447d78efc650ee98a6d2d15d1` | `frozen/c1-requirements.json:fixture_builder_sha256` (= r22 `requirements-v2.json:fixture_builder_sha256`) | ✅ |
| `.ufo/waves/round-22/frozen/requirements-v2.json` | `48ea2369dad5958bd62922483438124b11597a61a5e1ddc02bbeb213c89d0bea` | `frozen/c1-requirements.json:r22_requirements_v2_sha256` | ✅ |
| `.ufo/waves/round-23/contract.md` | `2bb35aefb08d3fafc467260f859453c0f096effe18b2446503f2b2ee87fe69e7` | `frozen/c1-requirements.json:contract_sha256` | ✅ |
| `.ufo/waves/round-23/oracle-rename.py` @ `4dc80c1` | same as above | landed in the pre-registration commit `4dc80c1` (`git diff --stat 1bfe708..HEAD` shows only `.ufo/waves/round-23/*` + `LOG.md`/`SCORECARD.md`) | ✅ pre-registration ordering holds |

`tools/mori-retention-reconcile.py` is byte-identical at `1bfe708` (entering revision) and in the
work tree (`0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32`), so the pre-C1
behaviour analysed below is the exact "before" artefact.

---

## 1. Verdict

**Only the declared differences exist.** The complete `diff -u r22/oracle-reconcile-v2.py
r23/oracle-rename.py` is 32 insertions / 7 deletions and every hunk is accounted for: the three
declared field substitutions (R02/R11/R12), the two declared new requirements (R25/R26), and four
benign self-description changes (docstring, observation schema id, builder import path, oracle
finding-id string).

**R26's independent count is genuinely independent of the SUT**, and is *more* discriminating than
the contract requires (it hard-codes the literals 2 and 4, so it cannot be satisfied by an
implementation that merely agrees with itself).

**R25 cannot pass vacuously at round level.** The `bool(parsed)` guard makes R25 red whenever no
run produced a JSON object, and — more importantly — *every one of the 18 oracle arms* is
independently required by R01–R24 to emit a JSON object (`record()` at `oracle-rename.py:44` requires
`isinstance(v,dict)`), so an arm that stops producing a JSON object turns its own requirement red
and the round cannot be green.

**Requirements made weaker: 1 declared-and-intended, 1 declared-adjacent (cosmetic), 4 residual
gaps** that are *not* defects of the oracle but leave contract C1 clauses under-frozen. Details in
§5. No blocking defect found.

---

## 2. Declared-difference audit (complete diff enumeration)

| # | Change | Declared? | Assessment |
|---|---|---|---|
| 1 | docstring rewritten (`oracle-rename.py:2-6`) | no (cosmetic) | benign |
| 2 | builder import path → `HERE.parent/'round-22'/'frozen'/'fixture-builder-v2.py'` (`:14-16`) | implied (contract R26 names "the frozen r22 builder"; `c1-requirements.json` pins that file's sha) | benign, but see §5-F1 / §7-4 (cross-wave path coupling) |
| 3 | observation schema `mori-r22-finite-observations-v1` → `mori-r23-c1-observations-v1` (`:27`) | no (cosmetic, self-description) | benign; consumers keying on the old string must be updated (none in r22 driver, which reads `counts`) |
| 4 | **R02** `v['raw_unallowlisted']==1 and v['scanner_unallowlisted']==1` → `v['scanner_unallowlisted']==1 and v['scanner_unallowlisted']==1` (`:52`) | **yes** (contract: "R02, R11, R12 read `scanner_unallowlisted` where they read `raw_unallowlisted`") | semantically faithful — see §3.1; second conjunct is now a tautological duplicate (dead conjunct, cosmetic) |
| 5 | **R11** `raw_unallowlisted==3` → `scanner_unallowlisted==3` (`:56`) | **yes** | faithful |
| 6 | **R12** `raw_unallowlisted==1` → `scanner_unallowlisted==1` (`:57`) | **yes** | faithful |
| 7 | new `raw_not_allowlisted(f)` helper (`:66-74`) | yes (R26) | see §3.2 |
| 8 | new `record('R26', …)` + forbidden-arm conjunction (`:75-76`) | yes (R26) | see §3.2 |
| 9 | new parsed/misleading_alias_runs/schema_v2_runs/parsed_runs block (`:77-84`) | yes (R25 + headline counter) | see §4 |
| 10 | `data['results'].insert(24, R25)` (`:85`) | yes (R25) | index arithmetic verified: 25 entries (R01–R24 + R26) → insert at 24 yields order R01…R24, R25, R26 ✅ |
| 11 | `data['counts']['misleading_alias_runs']` added (`:90`) | yes (headline counter, contract) | benign, additive |
| 12 | oracle finding id `R22_REQUIREMENTS_MATCH` → `R23_C1_REQUIREMENTS_MATCH` (`:92`) | no (cosmetic, self-description) | benign; downstream driver must use the new string |

**Nothing else changed.** Verified structurally: every other line of the r22 oracle
(`record()` body, the R05–R10/R13–R21 arm lists, the bool-metric conjunct at `:58-59`, R22/R23/R24
predicates, the `capability_absent` branch, `fixture_files` digest sweep, counts computation, exit
code `int(bool(unmet))`) is byte-identical. In particular the `record()` helper, the R18
conjunct's index arithmetic (`results[-2]` == R18 at that point) and the `capability_absent`
short-circuit are untouched.

## 3. Faithfulness of the declared substitutions, and R26's independence

### 3.1 Faithfulness of the R02/R11/R12 substitution

The pre-C1 SUT computes **both** fields from the same object —
`tools/mori-retention-reconcile.py:234`:
`'raw_unallowlisted':len(unallowed),'scanner_unallowlisted':len(unallowed)`.
The two values are the *same expression*, so the contract's claim ("its value is identical to
`scanner_unallowlisted`") is not merely asserted, it is verifiable at the source line, and the r22
frozen expectations agree (`round-22/frozen/expected-real.json` has `raw_unallowlisted: 4` **and**
`scanner_unallowlisted: 4`; the fixture arms require 1/1, 3/3, 1/1). The substitution therefore
removes a *redundant* conjunct, not a distinct observation.

Consequence (honest statement of loss): after the cutover the oracle can no longer observe the
*agreement* of the two fields, because one of them no longer exists. That is inherent to the
pre-registered removal, not an oracle defect. r22's dual check was the only place where "the two
names denote the same number" was pinned; after C1 that property becomes unobservable by
construction.

---

### 3.2 R26 — independence of the independent count

`oracle-rename.py:66-76`.

**Data flow.** `raw_not_allowlisted(f)` derives its inputs from:
* the fixture's **committed** policy bytes — `git -C <repo> show HEAD:policy.json` (`:69`),
* the fixture's **committed** allowlist bytes — `git -C <repo> show HEAD:allowlist.json` (`:70`),
* the frozen r22 builder's expectation lists `f['expected_scanner_hits']` / `f['expected_policy_hits']` (`:73`),
* and literals `2` (valid arm, `:75`) and `4` (forbidden arm, `:76`).

It never reads the SUT's output to compute the expected value; the SUT's value is only *compared*
to it. The comparison is a three-way chain `v['raw_not_allowlisted'] == raw_not_allowlisted(f) == 2`,
so the expected side is pinned by a literal as well as by the fixture — an implementation cannot
satisfy R26 by echoing itself.

**Independent re-derivation of the literals (static, from `round-22/frozen/fixture-builder-v2.py`
and `tools/mori-retention-reconcile.py` only):**

Fixture raw hits (builder `:47-53`): `policy.json` → 1 hit (only the `"synthetic": "R22_SAMPLE"`
line matches; the `"regex": "[R]22_SAMPLE"` line does **not** contain the literal `R22_SAMPLE`);
`allowed.txt` → 2 hits (identical text ⇒ identical `line_sha256`); `unallowed.txt` → 1;
`non-author.txt` → 1; `binary.bin` → skipped (NUL). Total 5 ⇒ `raw_total 5`,
`policy_excluded 1`, `scanner_total 4` — exactly R03's literals. Allowlist rows
(builder `:54-58`): 2 rows after dedup (`policy.json`, `allowed.txt`).

* **valid arm** — `must_redact_paths` empty ⇒ effective keys = {policy row, allowed.txt row} ⇒
  uncovered raw hits = {`unallowed.txt`, `non-author.txt`} = **2** ⇒ oracle literal 2 ✅ and the SUT's
  formula (`tools/mori-retention-reconcile.py:235`, `hits` minus `allowed_keys`) yields the same 2 ✅.
* **forbidden arm** — `must_redact_paths=['allowed.txt']` ⇒ the `allowed.txt` row becomes *forbidden*
  (SUT `:209-217`), so effective keys = {policy row} ⇒ uncovered = {`allowed.txt`×2, `unallowed.txt`,
  `non-author.txt`} = **4** ⇒ oracle literal 4 ✅ and the SUT yields 4 ✅.

**Discriminating power.** A wrong formula is caught, not echoed:
scanner-only counting would give 1/3 (red); counting against all rows including `must_redact_paths`
would give 1/3 as well (red); a constant would have to be 2 *and* 4 (impossible). The two arms
differ only in the allowlist row's `must_redact_paths` membership, so R26 pins the exact dependency
the contract specifies.

**Independence caveats (both benign here, both worth recording):**
1. The oracle's effective-key set = *all* allowlist rows whose path is not in `must_redact_paths`;
   the SUT's `allowed_keys` = rows that are not `must`-scoped **and** actually match a scanned hit
   (stale rows are demoted to `warnings`, SUT `:209-217`). The two definitions coincide in this
   fixture (both rows match hits — the receipt's `warnings` is `[]` and the SUT computes
   `stale=[]`, otherwise the r22 arms R01 would already be red). Any future fixture carrying a
   stale row would make the oracle's independent count and the SUT's count legitimately disagree —
   the oracle's definition, not the SUT's, would then be the odd one out. Contract-conformant
   today; flag for the next fixture.
2. The "raw hits" side of the count comes from the builder's in-memory expectation lists, not from
   a re-scan of the committed tree. The builder is sha-pinned in `frozen/c1-requirements.json`, and
   its lists are derived from the same bytes it commits, so the count is reproducible and
   tamper-evident — but it is builder-derived, not tree-derived. This matches the contract wording
   ("expected scanner hits + expected policy hits from the frozen r22 builder … read from the
   fixture's committed allowlist/policy bytes") ✅.

---

## 4. R25 — can it pass vacuously?

`oracle-rename.py:77-85`.

```python
parsed = [json.loads(row['stdout']) for every run, if the result is a dict]
misleading_alias_runs = sum('raw_unallowlisted' in o for o in parsed)
schema_v2_runs         = sum(o.get('schema')=='mori-retention-reconciliation-v2' for o in parsed)
R25.pass = bool(parsed) and misleading_alias_runs==0 and schema_v2_runs==len(parsed)
```

**No vacuous pass, by three independent guards:**

1. **Empty-parse guard.** `bool(parsed)` is false ⇒ R25 red. If the SUT emitted no JSON object on
   any arm (crash, empty stdout, non-object JSON), R25 is red, not green.
2. **Per-arm guard.** `record()` (`:44-49`) requires `isinstance(v,dict)` for *every* arm
   (R01–R24). An arm whose stdout stops being a JSON object turns *its own* requirement red, so
   the round's `unmet>0` fires independently of R25. A green round therefore implies all 18 arms
   produced JSON objects, and R25 then inspects all of them.
3. **Capability-absent branch.** If the tool file is absent (`:28-29`), R25 is never inserted and
   all 26 ids are `capability_absent` with `pass:False` ⇒ `counts.pass==0`, `unmet==26`, oracle
   exit 1. R25 cannot be satisfied by the absence of the SUT.

**Before/after arithmetic (derived statically, not executed).** The 18 distinct SUT invocations
split into 8 `check`-output arms (valid, drop, inject, digest, line, class, metric, forbidden — all
of which emit the full key set, `raw_unallowlisted` included, SUT `:231-240`) and 10 setup-error
arms (invalid-revision, diverged, policy-changed, allowlist-changed, malformed, bool-line,
bool-metric, duplicate, unsafe-receipt, symlink — which emit only
`{schema,finding_id,error,privacy_clearance,receipt_match}`, SUT `:287-289`).

* **Before** (tool @ `1bfe708`, `SCHEMA='mori-retention-reconciliation-v1'`, `raw_unallowlisted`
  present at SUT `:234`): `misleading_alias_runs = 8`, `schema_v2_runs = 0`, `parsed_runs = 18` ⇒
  **R25 red**; R01–R24 and R26 green ⇒ **25/26**, `unmet == ['R25']` — matches
  `frozen/c1-requirements.json:before_expected` ✅ and the contract's "passes before expected 25/26
  (R25 red)" ✅.
* **After** (key removed, `SCHEMA` → v2): `misleading_alias_runs = 0`, `schema_v2_runs = 18` ⇒ R25
  green ⇒ **26/26** ✅.

---

## 5. Requirements made weaker (and residual gaps)

**W1 — declared and intended.** R02/R11/R12 lose the `raw_unallowlisted` conjunct; R02's
replacement is now `v['scanner_unallowlisted']==1 and v['scanner_unallowlisted']==1` (`:52`) — the
first conjunct is a tautological duplicate (dead code). Consequence: the "both names denote the
same number" agreement property is no longer observable (§3.1). *Not a defect; recommend the dead
conjunct be dropped for readability before sealing, since the file is the frozen artifact whose
sha is published in `c1-requirements.json`.*

**W2 — self-description identifiers changed without being named in the contract** (`:27`,
`:92`): observation schema id and finding id. Any consumer keying on
`R22_REQUIREMENTS_MATCH` / `mori-r22-finite-observations-v1` must be updated. The r22 driver reads
only `counts`, so nothing in-tree breaks; the r23 driver must use
`R23_C1_REQUIREMENTS_MATCH`.

**G1 — the contract clause "No other output key, value, exit code or finding id changes" is only
partly frozen.** Exit codes and finding ids *are* pinned per arm (`record()`'s `code`/`finding`
arguments). Output *values* are pinned for `raw_total`, `policy_excluded`, `scanner_total`,
`scanner_unallowlisted`, `non_author`, `forbidden_allowlist`, `retention_state`,
`privacy_clearance`, `input_revision`, `measured_revision`, `tool_sha256`, `inputs_sha256`,
`argv`, `raw_hits`/`scanner_hits`/`policy_excluded_hits` — but **no requirement pins the output key
set**, and no synthetic-arm requirement reads `allowlisted`, `exclusion_basis`, `differences`,
`receipt_match`, `receipt_authenticity` or `error`. An implementation that renamed
`allowlisted` → `allowlisted_count` (or changed `exclusion_basis`) would still score 26/26 on the
synthetic arms. The real control (`frozen/c1-expected-real.json`) *does* pin `allowlisted: 86`,
`exclusion_basis`, `receipt_match`, `non_author`, etc., so the clause is covered on the real arm
only. *Severity: medium-low. Recommendation: add one key-set/diff assertion to the r23 driver
(output keys == r22 key set − `raw_unallowlisted`) or a 27th frozen requirement; this is the one
C1 clause with no frozen, per-arm witness.*

**G2 — R25's alias detection is top-level only** (`:82`: `'raw_unallowlisted' in o`). The contract
says the key is "removed from every output" and R25 is worded "no key `raw_unallowlisted`"; the
implementation checks only the top level of each run's JSON object. A *nested* alias (e.g. inside a
sub-object) would pass R25. For the current SUT shape (flat metrics + `raw_hits`/`argv`/
`inputs_sha256` sub-structures whose keys are pinned elsewhere) the risk is negligible, but the
oracle is weaker than the contract wording. *Severity: low.*

**G3 — the `--selftest` output path is not covered by any frozen requirement.** The contract's C1
bullet requires `SCHEMA` to become v2 "in **every** output (check, setup error, **selftest**)".
The oracle never invokes `--selftest` (all 18 arms are `check`), and the SUT's own selftest
asserts only `finding_id` and `privacy_clearance` (SUT `:274`), never `schema`. So "selftest output
schema v2" is unverified by any round-23 witness. (In the current implementation all three paths
share one `SCHEMA` constant, so the risk is theoretical — but the *witness* is missing, and the
r22 driver runs `--selftest` separately, `measure-round22.py:79`.) *Severity: low.*

**G4 — `raw_not_allowlisted()` is the only unsanitised git call in the harness.**
`:69-70` run `git -C <repo> show HEAD:<path>` with the **inherited environment**, no timeout, no
`--no-replace-objects`, and `check=True`. Everywhere else in this codebase the git env is scrubbed
(`round-22/frozen/fixture-builder-v2.py:24-32` strips `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`
and sets `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`; the SUT strips *all* `GIT_*` and
adds `--no-replace-objects`, SUT `:55-63`). Consequences: (a) under a hostile/odd env
(`GIT_DIR` set, a replace-ref base configured) the oracle could read bytes the SUT never saw, or
`git show` could fail; (b) `check=True` raises `CalledProcessError`, which is **not** in
`record()`'s caught set (`KeyError, TypeError, ValueError`, `:48`) ⇒ the whole oracle run would
abort with a traceback instead of reporting R26 as unmet. *Severity: low (the fixture repos are
private, freshly `git init`-ed, and the driver runs in a clean shell), but this is a real
robustness asymmetry and the fix is three lines (reuse `FIX.git`, which already sanitises the env,
or mirror the SUT's env scrub).*

**F1 — the requirements-file id list is not enforced.** `ids = expected['requirements']` (`:26`) is
used **only** in the capability-absent branch (`:29`). In the present branch the oracle hard-codes
R01–R26, so `counts.total` is 26 regardless of what `--requirements` declares. A mismatch between
`frozen/c1-requirements.json` and the produced set would be invisible to the oracle itself (a
driver that compares `counts.total` against `len(ids)` would catch it). *Severity: low; today the
two agree exactly (26 ids ↔ 26 results, in order R01…R24, R25, R26).*

**F2 — the oracle's `raw_not_allowlisted` helper name shadows the *SUT field* name while computing
the *oracle's* expectation; and the builder key `expected_policy_hits` actually holds the
**non-author-excluded** hits (builder `:107-108`), not policy-file hits. Both names are inherited
from r22 (`R04` uses the same key for `policy_excluded_hits`), so no functional defect, but the
next reader of `:73` can easily mis-derive the count. *Severity: informational.*

---

## 6. Integration hazards for L1 / the MeasureDriver seat (outside my lane, but caused by this file)

* **H1 — the r22 "before" assertion must not be copied.** `measure-round22.py:185` asserts
  `before['counts']['capability_absent']==24`, because the r22 "before" was *capability-absent*.
  In r23 the tool **exists** at the entering revision `1bfe708` (byte-identical to the work tree,
  `0795bac9…`), so the r23 "before" run takes the *present* branch: `capability_absent == 0`,
  `misleading_alias_runs == 8`, `pass == 25`, `unmet == ['R25']`, oracle exit 1. The correct r23
  before-expectation is `frozen/c1-requirements.json:before_expected`
  (`unmet:["R25"]`, `misleading_alias_runs: ">0"`). The oracle already exposes the counter at
  `counts.misleading_alias_runs` (`:90`) — note it is **`None`** (not `0`) when the tool is absent
  (`:90` uses `data.get(...)`), so a driver must guard `None > 0` before comparing.
* **H2 — `safe_outputs` (r22 `measure-round22.py:19-20`) is an allow-list** (`set(value) <= allowed`),
  so it cannot express "the alias must be absent"; it still contains `raw_unallowlisted` in the
  permitted set and will keep passing after C1. The r23 driver must carry the *deny* side
  explicitly: R25 (synthetic arms) plus `frozen/c1-expected-real.json:forbidden_keys`
  (`["raw_unallowlisted"]`) for the real control. `c1-expected-real.json` already supplies the
  real-arm raw complement (`raw_not_allowlisted: 9`), which the r22 driver checked as
  `raw_not_allowlisted == raw_total - allowlisted == 9` (`measure-round22.py:150`) — the r23 driver
  should carry that assertion forward unchanged.
* **H3 — the MeasureDriver spec names the C2 oracle at `.ufo/waves/round-23/oracle-quota.py`, while
  the `OracleQuota` seat delivers to `.ufo/waves/round-23/build/OracleQuota/oracle-quota.py`.**
  Flagged for L1 (sealing path reconciliation); out of my lane, not mine to fix.
* **H4 — the r23 driver must bind `round-22/frozen/fixture-builder-v2.py`** in its
  `executing-input-bindings` check (the r22 driver bound its own wave's copy, `measure-round22.py:60`),
  because the r23 oracle imports it by relative path across wave boundaries. The oracle already
  records `fixture_builder_sha256` in its observation (`:27`), so drift is detectable, but the
  binding assertion is the r22 driver's pattern and should be carried over.

---

## 7. Residual risk / verification gaps (not resolvable from the artifacts at hand)

1. **No execution evidence.** Every number in this report is a static derivation (the 8/18 arm
   split, the 2/4 R26 literals, the 25/26 before-state) — the driver must confirm them on the
   integrated revision; this review is not a substitute for that measurement.
2. **No mutation suite for r23.** r22's driver killed 22 named mutants against specific frozen
   rows (`measure-round22.py:85-147`); the r23 MeasureDriver spec does not mention mutants, so the
   r23 oracle's discriminating power is asserted here statically, not exercised by mutation. R26's
   discriminating power is argued analytically (§3), not demonstrated by a killed mutant.
3. **G1/G3 leave two contract C1 clauses without a per-arm witness** ("no other output key/value
   changes"; "selftest output schema v2"). Both are covered on the real arm / by construction, but
   not frozen.
4. **Cross-wave coupling (F/H4).** The r23 oracle is not self-contained: it imports r22's frozen
   builder by relative path (`oracle-rename.py:14-16`). If round-22's frozen tree is ever pruned or
   the wave directory is relocated independently, the r23 oracle breaks. The sha pin in
   `frozen/c1-requirements.json` makes the dependency *detectable*, not *removable*.
5. **Carried open debt (unchanged by this review, per contract):** 4 unallowlisted retention hits;
   original permission control RED 11/12; two historical wave dispositions unknown; baseline
   acceptance blocked; **no privacy clearance** (the SUT hard-codes `privacy_clearance: False`,
   `SUT:238`/`:274`, and the oracle asserts it is `False` in R02/R11/R23).

---

## 8. Recommendation

Accept `oracle-rename.py` as the C1 frozen oracle. Before sealing, L1 may optionally (a) drop the
duplicated conjunct in R02 (`:52`), (b) route the R26 git calls through `FIX.git` for env hygiene
(`:69-70`), and (c) add one key-set assertion elsewhere (driver-side) to close G1. None of these is
blocking: no vacuous pass, no tool-dependent expectation, and no undeclared semantic change was
found in R01–R24.

*Reviewer's note on scope: this review is static only. No test, build, lint or smoke run was
executed; no tool was installed or updated; no file other than this report was written.*
