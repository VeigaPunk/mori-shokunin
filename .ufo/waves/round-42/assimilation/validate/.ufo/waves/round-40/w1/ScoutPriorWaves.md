# ScoutPriorWaves — r38/r39 instrument findings vs round-40 evidence coverage

Scope: read all 13 `.ufo/waves/round-38/w1/*.md` and all 31 `.ufo/waves/round-39/w1/*.md`
seat reports (4252 lines total), extracted every finding raised **against the conform
checker or the append-only gate** (the two instruments under attack in C1/C2), then
checked each against round-40's instruments (`conform.py` v3, `tools/mori-sources-appendonly.py`
v3), contract, fixtures and `evidence/c10-*`/`c11-*` receipts. Counter-instrument
(`count-c7`/`count-c8`) and non-instrument findings are listed separately as
carried-forward residuals and out-of-scope notes. Read-only seat: no lane file touched;
the only mutation probe ran on a `/tmp` copy.

## Finding classes round 40 DOES address (not the ask; one line each)

- **Eligible-set edit-bound (`ids ∩ sup_map` drops never-edited superseded rows; S226
  invisible)** — `RevCensus.md` MEDIUM, `RevGateS228.md` check 4 FAIL, `RevFreeze.md` F1 →
  P-C11: `superseded = sorted(cid for cid in tip if cid in sup_map)` (gate `:354`),
  `edit_commit = last_edit.get(cid) or first_commit.get(cid)` (`:365`);
  `c11-after-lane.txt` shows S226 in `superseded_as_of`; fixture dag-n.
- **First-parent-lacks-path fall-through to another parent** — `CritC9Semantics.md`
  counterexample 2 → gate `:297-311` now reads `parents[0]`'s own tree only
  (`ref = states[pidx]` or direct blob); no fall-through loop; fixture dag-p.
- **Linear delete-then-re-add fabricated `changed` event** — `CritC9Semantics.md`
  counterexample 1 → "no `elif not is_merge` re-add branch" (`:318` comment); fixture dag-r.
- **`drain_shape` existential/per-function bypasses: wait+read+decoy, discarded-result
  tuple/`_`, undrained second Popen** — `RevC8Drain.md` F1/F2/F3, `RevReceipts.md` F1,
  `RevScorecard.md` F1 → new `drain_bind` check (per-Popen, name-bound, consumed-result);
  survivors decoy/underscore/tuple/second-popen + `drain_bind`/`drain_bind_decoy`
  selftest arms; `c10-red-decoy.txt` gives the genuine r39-accepts before-control
  (r39 `drain_shape` PASS, `CONFORM=met`).
- **`timeout_value` fold unsound: function-local shadow, conditional module rebind,
  `1e400`, fold crashes as exit-2** — `RevC8Value.md` H1/H2/M3/L4 → `timeout_scope`
  (scope-aware `_resolve_timeout_name`, `unconditional`/`conditional` maps,
  `ArithmeticError`/`RecursionError` caught into `value_violations`, `:402-410`);
  survivors shadow-none/shadow-neg/cond/inf/divzero.
- **`selftest_conjunct` kill rule unread from checker's own mutation table;
  comm_violations first-counter-only** — `RevC8Conjunct.md` F1/F2 → `entry_live` +
  `SELFTEST_MUTATION_NAMES`/`CONJUNCT_MUTATION` read from `selftest_mutations`'s own
  source (`conform.py:605-620`), per-counter loop (`:609-641`); `c10-red-conjunct.txt`,
  `c10-red-multicounter.txt`.
- **Frozen-contract staleness classes fixed this round**: `pass=11` vs actual (`RevFreeze.md`
  F2, `CritC9Semantics` row, `RevReceipts.md` F5) → contract/receipt agree on `pass=15`;
  nonexistent `fixtures/make-ancestry-dags.py` citation (`RevFreeze.md` F3) → r40 cites
  `run-c11-dags.py` + gate `_make_dag_repo`; missing/unrunnable `command:` receipts
  (`RevReceipts.md` F4/F6) → every `c1[01]-*.txt` carries a literal first line;
  receipts naming the wrong rev (`RevReceipts.md` F8/F2, `RevC7*` LOW-*s,
  `RevC9Walk.md` F1) → receipts name `bb1f2457`/extracted bytes/`265a955`.
- **Mutant-prediction undercount** (`MutC9IndexOrder.md` "pass=11 fail=1" predicted,
  10/2 observed) — moot; the same reverted-to-index-order behavior is covered by the
  v3 selftest's ancestry fixtures (pass=15).
- **Dead lines D1–D4** (`SimpCounters.md`) — removed from the v3 copies.
- **r37 counter `--tool` relative-path cwd bug** (`RevC9Compat.md` F1) — implicitly
  addressed: `run_tool` in count-c8 no longer passes `cwd="/"`, so a relative `--tool`
  resolves against the caller's cwd.

## UNADDRESSED finding classes (the ask)

| # | Finding class | Prior report file(s) | Evidence it persists / why r40 evidence does not cover it |
|---|---|---|---|
| U1 | **`head_pin` is a live-HEAD tautology**: counter `--pin-only` prints live `rev-parse HEAD`, checker compares to live `rev-parse HEAD`; `rev` argument never used → passes for any rev, labels the worktree not the measured bytes, races a moving tip | `RevReceipts.md` F3 (MEDIUM); `RevScorecard.md` F9; `RevC8Value.md` residual; `ExecC8Replay.md` risk | `conform.py:517-525` still `run(--pin-only)` → `pin==tip` where `tip` is a second live `rev-parse HEAD`; `count-c8.py:404-409` still prints `git rev-parse HEAD`. No evidence file exercises head_pin binding. It *did* align at `265a955` in `c10-after.txt`, but only because HEAD == the pinned tip at measurement time. |
| U2 | **CLI-selected counter/tool is unsandboxed arbitrary Python execution** | `SentCounters.md` HIGH | `conform.py:127-133` still `subprocess.run([sys.executable, first, ...])` for `--print-predicate`/`--pin-only`/`--print-tool` before any static check; `--counter` paths not rejected for symlinks/non-repo. Unchanged by design; no r40 evidence covers it. |
| U3 | **`scratch` check is lexical, not confinement**: substring match on `SCRATCH_ROOT`'s source segment; real destination never resolved/inspected (symlink, mode, ownership) | `SentCounters.md` MEDIUM | `conform.py:464-470` still `all(part in segment ...)` on `ast.get_source_segment`. NEW DETAIL: the required parts are still `(".ufo","waves","round-39","scratch")` while the v3 docstring (`:43-44`) says the parent is `.ufo/waves/round-40/scratch` — a counter genuinely rooted at round-40 scratch would now *fail* the lexical check; the honest counter's `"round-39"` string is grandfathered. No survivor fixture exercises a real scratch escape. |
| U4 | **Checker-side timeout does not reap a counter's process group** | `SentCounters.md` MEDIUM | `conform.py:127-133` still bare `subprocess.run(timeout=…)` — no `start_new_session`, no `killpg`. A counter that spawns a child and hangs is killed only at the direct child. Unchanged. |
| U5 | **Incomparable-event selection policy undisclosed**: "latest superseding row" and "last immutable-cell edit" are picked by walk order (max index), not ancestry-unique; swapping commit dates on incomparable branches flips the verdict | `CritC9Semantics.md` (two UNDISCLOSED SELECTION POLICY rows + counterexamples) | Gate v3 identical: `supersede_landing[target] = (index, by)` iff `index > previous[0]` (`:347-349`); `last_edit[cid] = commits[index]` last-write-wins (`:355-358`). P-C11 bounds neither; no dag fixture has two incomparable superseders or two incomparable edits with swapped dates. |
| U6 | **`--full-history` clause unwitnessed by any committed fixture** | `RevC9Ancestry.md` F3 (LOW) | Empirically still true: I removed the flag from a scratch copy (`sed`-equivalent byte edit of `gate-nofh.py`) and ran `python3 gate-nofh.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` exit 0 — all 6 DAG cases (a, c, d, n, p, r) are full-history-agnostic. The flag matters only on lane history (6531ac60), which no fixture reproduces. |
| U7 | **Gate header docstring contradicts implemented equality semantics**: "descendant of (strictly later than)" / stale "landed at or before the edit" vs `is_ancestor` equality counting as as-of (dag-d prints as-of at equality) | `RevC9Ancestry.md` F2 (LOW) | `tools/mori-sources-appendonly.py:28-33` unchanged verbatim ("strictly later than", "at or before"); `is_ancestor(repo, edit_commit, commits[landing_index])` (`:366-367`) still equality-permissive; dag-d expectation still `as_of=[S001]`. |
| U8 | **`bounded_reads` docstring overclaims communicate coverage** | `RevC8Conjunct.md` F2 (second clause) | v3 docstring `:17-19` still claims "every `communicate(` in every counter carries a `timeout=` keyword" under `bounded_reads`; `bounded_violations` (`:383-396`) still fills only from `run`/`check_output`/`check_call`. The per-counter comm audit moved to `selftest_conjunct` (so coverage is now real — via a differently-named check than the docstring claims), but the name-boundary misattribution persists; a missing `timeout=` on `communicate` fails `selftest_conjunct`, not `bounded_reads`. |
| U9 | **Dangling `supersedes S###` (target absent at R) is invisible** | `RevCensus.md` residual risk | Eligible set is `cid for cid in tip if cid in sup_map` (`:354`) — still requires the target *present* at R. A supersedes row naming a deleted/nonexistent id never reaches the timing line; no fixture or receipt exercises it. |
| U10 | **Contract-literal vs instrument-output defect recurs (new instance of the r39 F1/F2 class)** | `RevFreeze.md` F1/F2; `RevReceipts.md` F5; `RevGateS228.md` check 4 | `contract.md:137` (and the P-C11 text embedded in `conform.py`/gate PREDICATE) declares `superseded_as_of=[19 ids incl. S226]`; `evidence/c11-after-lane.txt` prints **34** ids (S226 + 15 additional never-edited superseded ids: S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140 — the eligible-set extension caught more than the contract anticipated). The summary `superseded=` list agrees (34). Frozen prose is off by 15 in the same way r39's `pass=11` was off by one. |
| U11 | **`timeout_state` blind to dropped `timeout=` kwarg when a default still bounds** | `MutC5Bounds.md` observation (r38) | Same shape holds: only the static `bounded_reads` audit catches a removed `timeout=` kwarg; `timeout_state` still cannot see it when the helper default applies. Design-bounded, still true. |
| U12 | **Violation messages cite line numbers, never the binding name** | `MutC8NoneVal.md` note | `value_violations`/`bounded_violations` still print `line %d (%s): %s` with the call name, not the identifier (e.g. `UNBOUNDED_DRAIN_S`); only the unbound-name path spells the symbol. Cosmetic; persists. |
| U13 | **`timeout_scope`/`_resolve` still over-rejects valid forms (fail-closed)** | `RevC8Value.md` L5 (LOW) | `_resolve` (`:160-207`) still cannot fold `IfExp`, `BoolOp`, `Call`, `AnnAssign`, `AugAssign`, multi-target, floor-div, dict/set literals, `UAdd`, negative subscript; all fail closed (false FAILs only). Conservative by design; persists. |
| U14 | **`--out`-style output path unconfined in wave fixture tooling** | `SentWitnessSandbox.md` MEDIUM (r38 `make-witness-sandbox.py`) | The r40 sibling `fixtures/run-c11-dags.py:35` does `out_path = os.path.abspath(argv[3])` with no containment check — the same "caller-controlled destination, no resolve-and-confine" class. The r38 file itself was not re-examined (not in r40's instrument set). |

## Carried-forward residuals on the counter instrument (count-c8 = count-c7 − D1–D4)

The ask names conform/gate; these r39 findings are against the *counter of record*
(which conform audits), so they sit adjacent. Each persists byte-for-byte in count-c8:

- **`--arms selftest` mode can never pass an honest probe**: `parse_rowstates`
  (`count-c8.py:335`) still requires exactly one space in `^selftest row_states (PASS|FAIL)`
  while the probe pads the arm name (`"selftest %-20s %s"`) → `row_states=None`,
  `C7=unmet` on a good tool. Dead `ROWSTATES_RE` was removed (D1) but the live
  single-space regex remains. — `RevC7Kill.md` F1
- **Negative witnesses read from the worktree, not from rev R** (`count-c8.py:516-526`
  opens `dirname(__file__)/fixtures/witness-*`) — `RevC7Negatives.md` LOW-2.
- **`live_rows_v2` existence-only copy check / ill-balanced receipts** —
  `RevC7Clone.md` F1/F2 (MEDIUM/LOW). Unchanged code (`copy_paths_at` membership test).
- **Docstring/string-parked anchors count as "code"** (`code_occurrences` comment rule
  only) — `RevC7Anchors.md` LOW-2, `RevC7Negatives.md` residual. Unchanged.
- **`paths_in` token grammar skips extensionless/non-backticked paths; check is
  existence/type only** — `RevC7CapPath.md` residuals. Unchanged.
- **`rows=` not reconciled against registry; non-drifted states unchecked** —
  `RevC7Live.md` L1/L2. Unchanged.
- **Probe-authored `want` table: no honest-table baseline captured** — `RevC7Kill.md` §6;
  `ScoutC7Bounds.md` bound 1. Narrowed by contract erratum (r39 routed finding 1),
  code unchanged.
- **`--arms selftest` narrow success path** (exit-zero/PASS only) —
  `ScoutC7Bounds.md` scope note. Unchanged.
- **`real_arm`/`real_draw_arm` never check child exit code** — `RevC9Compat.md` F4.
  Unchanged.
- **Seed predictability** (`random.Random(seed)` over 4 states) — `ScoutC7Bounds.md` bound
  2. Unchanged; disclosed bound.

## Out-of-scope/non-instrument findings noted, not counted

`ExecIndexCleanLog.md` FAIL (dispatch-log commit coverage — process hygiene, not
conform/gate); `RevReceipts.md` F2 (before-receipt provenance ordering — addressed as
receipt discipline: r40 reds ran extracted `bb1f2457` bytes and name them);
`RevFreeze.md` F4/F5 (receipt `command:` lines — addressed); `ScoutMisroot.md`,
`ScribeTrendVerdicts.md`, `ScribeLesson.md` (lesson-row defects routed to erratum),
`ScoutFrontierRows.md` (FR-row unresolved question — corpus indexing, not instruments),
`ConnSibling.md` (sibling-walk audit), `MutC8NoneVal.md` verdict-line wording (folded
into U12), `MutC7Cheat.md`/`MutC5Tool.md`/`RevC4Kill.md` (clean kills), `ExecCensusEnd.md`/
`RevCensus.md` (PASS), `ScribeLesson.md` M20/M21/F4.

## Commands run (all observed)

- `wc -l` over all 44 prior reports (4252 lines); full reads via the read tool.
- `python3` JSON dump of `.ufo/waves/round-40/w1-spec.json` → `reportDir` =
  `.ufo/waves/round-40/w1`; report-name convention `<item>.md` confirmed against r39
  (every spec item ↔ same-named `.md`, zero orphans).
- `grep -n`/`sed -n` over `conform.py`, `count-c8.py`, `tools/mori-sources-appendonly.py`
  for head_pin/scratch/drain/resolve/supersede internals (lines cited above).
- `cat`/`head`/`tail` of `c10-after.txt`, `c10-after-selftest.txt`, `c10-red-decoy.txt`,
  `c10-red-multicounter.txt`, `c11-after-lane.txt`, `c11-after-selftest.txt`,
  `c11-red-neveredited.txt` — outputs quoted above; 34-id `superseded_as_of` counted
  verbatim from `c11-after-lane.txt` lines.
- Mutation probe on a `/tmp/scoutpw/gate-nofh.py` copy: deleted `"--full-history",`
  from the `git log` call; `python3 gate-nofh.py --selftest` → `pass=15 fail=0` exit 0
  (basis for U6).
- `read` of `contract.md`, `conform.py` sections 14-50/75-133/342-500/499-642/596-767/764-805,
  gate `analyze()` 236-400, `run-c11-dags.py` main.

## Confidence / unknowns

High confidence on U1–U14 (each rests on committed v3 bytes or a run). Open edges:
whether P-C11's "every superseded id present at R" intends the 34-id set or the
contract's 19-id gloss (U10 is a frozen-prose defect either way); whether the
`"round-39"` literal inside the v3 scratch check is deliberate back-compat or a stale
constant (U3's new detail); incomparable-branch verdicts under non-monotone commit dates
(U5) are untested both by fixtures and by me. No tools installed; pacman untouched.
