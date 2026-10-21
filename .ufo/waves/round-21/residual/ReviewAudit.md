# ReviewAudit — round-21 residual implementation-completeness review

Seat: MoriR21.ReviewAudit. Scope: integrated production `tools/mori-evidence-loss.py`, `.ufo/waves/round-21/oracle-loss.py`, `.ufo/waves/round-21/fixture-loss.py` at HEAD `2afee133cc1cd3ce734554b67a610890f45c534d`. Read-only; no tests, builds, pins, or census; two read-only `audit` invocations were run against committed lane data as evidence for the accounting comparison (no mutation; the tool performs read-only git/file ops only).

## Findings

### F1 — High: fixture `duplicate-accounting-id` expects rc1; contract and tool both say rc2 (guaranteed acceptance-run failure)

- `.ufo/waves/round-21/fixture-loss.py:280-284` sets `"expected_rc": 1` for `duplicate-accounting-id` (case built at `:216-217`).
- The tool rejects duplicate accounting ids at load time: `tools/mori-evidence-loss.py:377-378` (`duplicate_observation_id`), surfaced as `SetupError` → rc2 (`:1216-1218`). Same for required ids (`:354-355`).
- Contract: `.ufo/waves/round-21/contract.md:14` — "rc0 only complete valid accounting and zero unresolved; rc1 expected blocker or omission; rc2 setup/input failure." A duplicate id is malformed input, i.e. rc2. The tool's own selftest asserts rc2 for both duplicate cases (`tools/mori-evidence-loss.py:946-953, 1022-1029`).
- Consequence: both fixture runs of this case record `run-N-expected-rc` failure (harness check at `fixture-loss.py:477-479`), the case reports `fail`, and `run_harness` exits rc1 (`:617-620`). L1's single acceptance run can never pass this harness as frozen. `build/FixtureLoss.md:22` ("the other cases expect rc=1") shows this expectation was not revisited; unlike F2 it is not acknowledged anywhere.

### F2 — High: fixture `valid-independently-disposed` control still encodes pre-refinement pin semantics (guaranteed failure on at least five fields)

- Expectation: `.ufo/waves/round-21/fixture-loss.py:266-269` — rc=0, `unresolved:0`, `disposed:1`, `invalid:0`, `pin_allowed:true`.
- Shipped tool behavior, by design: any structurally clean disposed row still appends `external_review_required` to `unresolved` and an `invalid=false` issue (`tools/mori-evidence-loss.py:580-595`), so the observed result is rc=1, `unresolved=1`, `pin_allowed=false`. This is mandated by `.ufo/waves/round-21/trust-refinement.md:5` ("the actual audit must never grant baseline acceptance from a submitted disposed declaration alone") and confirmed by the tool's own `declared_disposition` selftest (`tools/mori-evidence-loss.py:1127-1148`, rc=1).
- Independent second defect in the same case: the synthetic disposition record `evidence/row-disposition.json` (`fixture-loss.py:144-152`) contains extra keys `fixture` and `kind`, while the tool requires the hash-verified record to contain exactly `{id, actor, wave_id, disposition, independent}` (`tools/mori-evidence-loss.py:462`). The case therefore also trips `disposition_record_mismatch` → `invalid=1`, `disposed=0` — so the mismatch is not attributable solely to the trust-refinement delta.
- `build/FixtureLoss.md:44` acknowledges the rc0-vs-block delta ("a later run will report an expected-versus-observed mismatch … not a test pass") but does not re-baseline the expectation table, and does not mention the record-key mismatch at all. As frozen, this harness contradicts the wave's own authoritative refinement; a corrected expectation (rc=1, `unresolved=1`, `disposed=1`, `invalid=0`, `pin_allowed=false`, `external_review_required` finding present) would still exercise the positive control honestly.

### F3 — Medium: disposition record content check is exact-key equality, stricter than the stated interface

- `tools/mori-evidence-loss.py:462`: `set(value) != {"id", "actor", "wave_id", "disposition", "independent"}` → `disposition_record_mismatch`.
- The tool-author interface note recorded in `build/FixtureLoss.md:31-33` says the record "must itself declare" the five fields — a superset condition (`⊇`). The implementation enforces equality (`=`), rejecting a hash-and-commit-verified record that declares all five fields plus contextual fields (timestamps, reviewer notes). Contract `contract.md:14` requires the accounting-side disposition object fields and record presence; it nowhere forbids additional record keys.
- Concrete interop consequence is demonstrated inside this wave: the fixture's own record payload (F2) fails this check. Any future independently reviewed per-wave statement (the acceptance path trust-refinement.md:5 anticipates) must be byte-shaped to exactly five keys or the gate misreports a well-formed record as `disposition_record_mismatch`.

### F4 — Medium: integrated oracle never independently verifies the C1 `unresolved` visibility counter

- `.ufo/waves/round-21/oracle-loss.py:77-90`: it independently computes `expected_omitted` from the accounting file and checks only `schema`, `exit_code==1`, empty stderr, `pin_allowed is False`, and `omitted`. The claim "after:0 omitted,2 unresolved remain visible" (`contract.md:7`) is only half measured: `unresolved`, `retained`, `disposed`, `invalid` are recorded but never cross-checked.
- A regression reporting `unresolved:0` (e.g. dropping the `:542-543` append) with `omitted:0` and `pin_allowed:false` would pass the oracle green while erasing the evidence C1 exists to preserve. The predecessor scratch oracle computed this independently — `.scratch/round21/OracleLoss/oracle-loss.py:292-312` builds `unresolved_required_ids` and `unexpected_accounting_ids` — the integrated rewrite dropped both checks.
- The accounting states are already in hand at `oracle-loss.py:77` (`source_rows`); the missing check is one set comparison per phase.

### F5 — Low: unreachable `pin_allowed` conjuncts (dead conditions)

- `tools/mori-evidence-loss.py:612-619`: `not unresolved` already precludes `len(disposed) == len(required_rows)` from ever being reached true (every disposed row adds an `unresolved` entry via `:590-594`), and `not omitted` already implies `len(retained_ids) == len(required_rows)` (both derive from the same id sets, `:611`). Harmless to behavior — `pin_allowed` is correctly false in every reachable state — but the dead conjuncts mislead a future auditor into thinking a structurally-disposed population could flip the gate without external review, which trust-refinement.md:5 forbids.

### F6 — Low: `--selftest` writes into the lane working tree, ignoring TMPDIR

- `tools/mori-evidence-loss.py:785-787`: `TemporaryDirectory(prefix=".mori-evidence-loss-selftest-", dir=clone_root)` where `clone_root` is the lane root (`parents[1]` of `tools/mori-evidence-loss.py`), and the nested fixture repo is `git init`-ed under it (`:733-737`). Normal exit cleans up, but a hard kill leaves untracked `.mori-evidence-loss-selftest-*` inside the production tree, catchable by any later `git add -A`. The sibling harness honors and validates `TMPDIR` (`fixture-loss.py:547-561`); the selftest should route through `TMPDIR`/tempfile defaults for the same isolation the contract's "builds isolated fixtures" (`contract.md:16`) implies.

### F7 — Low: audit accepts any commit object in the object DB, not only reachable/committed history

- `tools/mori-evidence-loss.py:279-291`: `cat-file -t <revision>` == `commit` plus `ls-tree` of that revision is the only binding; a dangling or unreferenced commit object satisfies "committed own-lane evidence copy". Content integrity is still fully bound (blob bytes hashed against the recorded sha256 at `:326-327`), and the oracle separately binds its measurement inputs to the measured revision (`oracle-loss.py:35-41`), so this weakens only the audit gate's provenance claim, not measurement identity. An ancestry check (e.g. `merge-base --is-ancestor <rev> HEAD`) would close it.

## Accounting comparison (actual vs required) — measured, matches claims

- Required population: `aggregator-r10`, `aggregator-r10-resume` (`.ufo/waves/round-21/frozen/required.json`); both reference baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` @ `e9f340c` with sha256 `0993b235…` (byte-verified in working tree).
- Actual accounting `corpus/evidence/loss-accounting-r21.json` (committed at HEAD): both rows `unresolved`, `independent_disposition:null`, cleanup actor `souji-shokunin <souji@shokunin.local>`, deletion/cleanup copies bound to ancestor commit `a8442a018aa9c51b21b92c3ce3b17736317375b1` (verified reachable from HEAD; both blobs present in that tree).
- Read-only audit of after state: `omitted=0, retained=2, unresolved=2, disposed=0, invalid=0, pin_allowed=false, rc=1` — exactly the C1 "after" claim and trust-refinement.md:9 ("The real receipt must say blocked").
- Read-only audit of before state (`frozen/before-accounting.json`, empty register): `omitted=2, retained=0, unresolved=0, disposed=0, invalid=0, pin_allowed=false, rc=1` — matches the C1 "before" claim (2 absent from retained register). Note the oracle (`oracle-loss.py:83-86`) hardcodes rc==1 for both phases, which both measured runs satisfy.

## Non-defects verified (axes with no finding)

- Strict schemas/types: closed key sets for every object (`_require_keys`, `tools/mori-evidence-loss.py:335-341, 345-383, 641-674`); duplicate JSON object keys rejected (`_unique_object`, `:68-74`); strict `type(x) is bool` rejecting 1/0 (`:667-669`, selftested `:1113, 1119`); NaN/Infinity constants rejected (`_reject_constant`, `:64-65, 166`).
- Duplicate ids: required, accounting, and cases each rejected with rc2, selftested (`:354-355, 377-378, 665-666`).
- Numeric counters: all five counts are `len()` of their parallel `*_ids` lists (`:511-631`); payload counts and lists agree; the real before/after runs above confirm. `retained` counts id membership including malformed rows — ambiguity acknowledged in `build/FixtureLoss.md:24` with minimum-count assertions; not a contract violation.
- Symlink refusal: root opened component-wise with `O_NOFOLLOW` (ELOOP → setup error, `:77-99`); `..` components refused everywhere (`:89-90, 117-118, 177`); final-component symlinks lstat-rejected for CLI inputs (`:123-125`) and evidence copies (`:197-201`, reason `unsafe_symlink`); TOCTOU guarded by before/after inode+stat identity (`:126-129, 202-220`); FIFO hang prevented via `O_NONBLOCK` + ISREG. Selftest (`:969-987`) and fixture (`symlink-escape`, `fixture-loss.py:246-250`) both cover it.
- Raw-byte hashes: working-tree bytes hashed against the recorded sha256 (`:207-222, 437-439`), and the committed blob's bytes hashed independently against the same value (`:323-327`), so uncommitted replacement fails as `revision_hash_mismatch` (selftested `:928-940`); read stability re-checked post-read (`evidence_changed`, `:216-220`).
- Git-commit binding: revision must be a commit object; path resolved against that revision's full tree with `--show-prefix` join; blob kind + regular mode enforced (`:276-328`); real accounting references verified clean by the measured run.
- classify decision logic implements exactly the contract rule for both rule modes (`:683-692`); frozen `cases.json` matches the contract table (`contract.md:20-25`) row-for-row in all five columns; before-rule mismatched=2 / after-rule 0 proven in selftest (`:1082-1097`); the oracle transitively enforces that the rule object is actually read (independent expected-rc computation, `oracle-loss.py:92-105`) — ignoring the rule would flip the before-phase rc and be flagged.
- `--root` as a required audit argument is contract-sanctioned (`contract.md:14` "beneath --root (required argument)").
- `ordinary_state_change` is schema-carried but decision-inert by the contract's own rule text (only lost/independent decide); frozen table confirms (`loss-unknown` has `ordinary_state_change:true` yet `census-regression`). Not a defect.
- The required row's `evidence` citation (`path:line`) is format-validated only, never opened — `contract.md:14` defines no verification for it, and the baseline provenance is fully verified instead. Informational, listed for completeness.

## Residual risk and verification gaps

- I ran the two read-only `audit` invocations against the working tree at HEAD `2afee133`; I did not run `--selftest`, `fixture-loss.py`, or `oracle-loss.py` (tests and the acceptance run are L1's). F1/F2 are derived from expectation tables vs implemented behavior plus the tool's selftest assertions, not from a harness run.
- No independent verification exists for `unresolved/retained/disposed/invalid` counters in any committed harness (F4); until fixed, the C1 after-side rests on the tool's own payload plus this review's manual run.
- `oracle-loss.py` performs no output-overlap check on `--out` (binds inputs first, writes last); L1 must keep `--out` outside the input set, as the bounds already require.
- F3 means any future real disposition record must be exactly five top-level keys; reconciliation with an external-review statement format is undecided upstream.
- Fixture/oracle scratch copies under `.scratch/round21/` differ from the integrated files (oracle substantially rewritten, fixture identical per `diff`); this review judges only the integrated paths.
- No tools were installed or updated during this review.
