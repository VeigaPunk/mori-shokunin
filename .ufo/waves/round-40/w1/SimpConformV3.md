# SimpConformV3 — seat report: conform.py v3 line accounting vs r39 bytes

Date: 2026-10-24. Seat: simplifier (read-only; the only file written is this report).
Subject: `.ufo/waves/round-40/conform.py` (805 lines) vs
`fixtures/extracted/conform-v2-r39.py` (552 lines).

## Verdict

**The +253-line delta is fully accounted for by the three new checks
(`timeout_scope` hardening, `drain_bind`, `selftest_conjunct` v3), their two new
selftest mutations, and the rename/retarget apparatus that carries them. Zero
added lines are unaccountable.** Three retained r39 lines are stale under the
rename and one docstring line contradicts the code; all are findings only (the
bytes are frozen; I made no production edits).

## Identity of the counted bytes

- `sha256sum` both files:
  - r40 `conform.py` = `5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf` — equals the pin at `evidence/freeze-r40.txt:9` and equals `git show 265a955cc67be4eae97d2dc5a9338a25f31eb29b:.ufo/waves/round-40/conform.py | sha256sum` (805 lines). Counted bytes == scored-tip bytes.
  - r39 `conform-v2-r39.py` = `fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987` (552 lines), both files newline-terminated.
- `wc -l`: 805 − 552 = **+253**. Unified-diff hunk headers sum Σ(new−old) = +253; difflib opcodes give **+389 added / −136 deleted = +253** (GNU diff's printed "135 deletions" disagrees with its own hunk arithmetic by one; wc and hunk sums are authoritative).

## Added-line ledger (+389, difflib, bucketed by r40 line ranges)

| Bucket | +lines | Accounts to |
|---|---|---|
| docstring/usage (≤68) | 37 | prose of the three checks: `timeout_scope` (scope-aware, finite-positive, fold-as-violation), `drain_bind` (bound, own timeout, consumed), `selftest_conjunct` v3 (per-counter, mutation-table liveness); "eleven textual mutations" sentence |
| imports/paths/CHECK_NAMES/mutation tables (69–96) | 21 | `import inspect` (conjunct v3 reads its own sources), `import math` (`isfinite` for `1e400`), r39→r40 `SCRATCH_ROOT`/`DEFAULT_COUNTERS` retarget + 2-line provenance comment on why `DEFAULT_CONTRACT` stays at round-39, `CHECK_NAMES` rename, `SELFTEST_MUTATION_NAMES` (11) + `MUTATION_CHECK_ALIAS` (2) |
| PREDICATE (97–126) | 22 | frozen P-C8 → P-C10 text (the three checks' wording) |
| `_finite_positive` + `_timeout_value` (195–209) | 13 | timeout_scope: finiteness hardening |
| `_module_assignments`/`_function_bindings`/`_global_names`/`_resolve_timeout_name` (210–308) | 99 | timeout_scope: conditional module rebind fail-closed, function-local shadow, `global` rebinding, scope-aware resolution |
| `_popen_name`/`_result_consumed` (309–341) | 29 | drain_bind: Popen binding name; consumed-result rule (non-`_` assign / return; tuple/`_` rejected) |
| static_checks rewiring (354–450) | 20 | scope wiring (1) + Name-dispatch and fold-error→violation handlers (timeout_scope, r39 finding 4/M3/L4) + per-Popen drain_bind loop |
| evaluate (560–644) | 30 | `timeout_scope` rename (1), drain_bind per-counter loop (drain no longer first-counter-only), selftest_conjunct v3 per-counter block |
| `CONJUNCT_FIND`/`CONJUNCT_MUTATION` (645–650) | 6 | selftest_conjunct v3 constants |
| `selftest_mutations` (651–737) | 62 | the 11-arm table; NEW arms `timeout_scope_shadow` (function-local `TIMEOUT = None`) and `drain_bind_decoy` (decoy used communicate beside wait+read); drain block build moved intact from r39's inline hack |
| `selftest()` alias rewiring (753–766) | 9 | resolve expected failing check through `MUTATION_CHECK_ALIAS` |
| `main()`/tail (770–805) | **0** | CLI surface and exit contract (0 met / 1 unmet / 2 setup) unchanged |

Classifier dump of the "other" buckets (17 + 24 lines) inspected line-by-line: all are continuation lines of the timeout_scope dispatch, drain_bind loop, per-counter drain loop, and conjunct v3 loop — none orphaned.

## Deletion ledger (−136)

| Bucket | −lines | Why gone |
|---|---|---|
| old docstring/usage | 21 | replaced by v3 check prose |
| r39 paths/`CHECK_NAMES` | 14 | retargeted/renamed |
| old `_timeout_value` body | 4 | superseded by `_finite_positive` wrapper |
| old timeout/drain loops in `static_checks` | 12 | replaced by scope-aware dispatch + bound-drain loop |
| `has_communicate_timeout` + `_first_communicate_segment` | 11 | r38-era approximation keys dead under v3 (AST drain_bind / per-counter strips replace them) — part of the D-series dead-line cleanup |
| evaluate `drain_shape` first-counter-only block | 6 | replaced by per-counter `drain_bind` |
| old evaluate `selftest_conjunct` block | 61 | replaced by v3 per-counter block |
| old inline mutations table/loop text | 7 | table moved into `selftest_mutations()` |

## Mutations: 9 → 11

r39 table (9) → r40 table (11): `timeout_value`→`timeout_scope` and `drain_shape`→`drain_bind` renames, 7 arms carried, **+2 new arms for the new checks** (`timeout_scope_shadow`, `drain_bind_decoy`). Verified programmatically: `len(SELFTEST_MUTATION_NAMES) == 11`, names = (predicate, head_pin, tool_resolve, bounded_reads, timeout_scope, timeout_scope_shadow, drain_bind, drain_bind_decoy, timeout_state, scratch, selftest_conjunct), aliases `{timeout_scope_shadow→timeout_scope, drain_bind_decoy→drain_bind}`, `CONJUNCT_MUTATION in selftest_mutations(...)` True. Consistent with the frozen receipt `evidence/c10-after-selftest.txt` (`pass=11 fail=0`); I did not rerun the selftest (read-only seat; receipts are ground truth).

## Findings (report-only; bytes frozen at 265a955cc)

1. **Stale check names retained through the rename** — `conform.py:345` (static_checks docstring: "bounded_reads/timeout_value/drain_shape/scratch detail"; keys are now `timeout_scope`/`drain_bind`) and `conform.py:472-473` (comment: "belongs to the timeout_value check"; now `timeout_scope`). Cosmetic; no behavior.
2. **Docstring/code mismatch on the scratch parent** — `conform.py:44` says the counter carries a scratch parent under `.ufo/waves/round-40/scratch`, but the code (`conform.py:469-470`) requires `"round-39"` in the counter's `SCRATCH_ROOT` segment. The code is right for the counter of record (`count-c8.py:62` keeps the round-39 path — the frozen P-C7 world); the docstring's mechanical r39→r40 retarget overreached. Future counter version: fix line 44, not line 470.
3. **Redundant except clause (deletion candidate, −3 lines, behavior-identical)** — `conform.py:410-412` `except (ArithmeticError, RecursionError)` is fully shadowed by the identical-body `except Exception` at 413-415 (ZeroDivisionError ⊂ ArithmeticError ⊂ Exception; RecursionError ⊂ RuntimeError ⊂ Exception; both append the same "fold error" violation). A future version can collapse to the single `except Exception`.
4. Note, not a defect: helper `_timeout_value` (line 205, called at 406 for non-Name kwargs) keeps its r39 name while its check renamed — still accurate for what it does.
5. Deliberate r39 paths verified, not stale: `DEFAULT_CONTRACT` (74), `FIXTURE_REL` (75), `HANG_FIXTURE` (76), scratch segment check (470), scratch mutation anchor (731-733) all match count-c8.py's frozen world; anchors confirmed present in count-c8 bytes (line 62 scratch path; communicate anchors at 113/147; `start_new_session` Popen anchors at 111/145 feeding the drain_bind_decoy arm).

## Corroboration / imports

`inspect.getsource` + module import of conform.py is side-effect-free (empty stdout on import); `PREDICATE` begins `P-C10: at revision R, the round-40 conformance checker passe…`.

## Commands run (all read-only)

1. `wc -l` + `sha256sum` on both files.
2. `grep -n '^def \|^MUTATIONS\|^PREDICATE\|^[A-Z_]* ='` on both files (function map).
3. `diff -u fixtures/extracted/conform-v2-r39.py .ufo/waves/round-40/conform.py` (full 652-line diff read; hunks @@ -1,48 +1,64 … @@ -502,12 +753,14; none after → tail/main unchanged).
4. Python difflib ledger (added/deleted bucket tables above) + mutation-table/anchor/PREDICATE/import corroboration.
5. Greps: stale names (`timeout_value|drain_shape|has_communicate_timeout|first_communicate_segment`) → only 205/345/406/472-473; count-c8.py anchors → 62/111/113/145/147; finding lines (`round-40/scratch|"round-39"|except \(ArithmeticError`) → 44/470/472-473/410/732.
6. `grep 5025b966… evidence/freeze-r40.txt` → line 9; `git show 265a955cc:…conform.py | sha256sum` + `wc -l` → identical hash, 805 lines.
7. Region reads: conform.py 28-44, 396-417, 450-498.

## Bounds & tooling

No production edits; no sibling-lane, jj, Git-index, `.ufo/state/`, or watchdog contact; git used read-only (`git show`). Tooling authorization: nothing installed — no new tool was needed; pacman untouched. Next deletion would be finding 3's three lines, but only in a future counter version (frozen bytes here).
