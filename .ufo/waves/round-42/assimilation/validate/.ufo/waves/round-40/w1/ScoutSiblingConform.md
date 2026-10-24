# ScoutSiblingConform — sibling-lane collision scan for mori conform v3

Seat: ScoutSiblingConform (scout, mori-r40-w1). Question: does any sibling lane own a
'counter conformance' or 'scope-aware static fold' artifact that could collide with mori's
conform v3 (`.ufo/waves/round-40/conform.py`, prints `CONFORM=`/`CONFORM_SELFTEST`, checks
`timeout_scope`/`drain_bind` over mori counter instruments)?

Note on path: the wave spec (`w1-spec.json`) item for this seat carries no explicit `Report:`
trailer; `reportDir` is `.ufo/waves/round-40/w1` and round-39 used `<SeatName>.md`, so this
report lands here.

## Verdict

**No collision.** No sibling lane has an artifact that audits mori "counter" instruments,
prints `CONFORM=`/`CONFORM_SELFTEST`, or performs scope-aware static resolution of `timeout=`
keyword values on subprocess calls. Two artifacts are adjacent on one axis each and are
recorded below; neither is a semantic collision.

## Commands run and outputs

1. `find /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40 -type f`
   → instruments + evidence + fixtures present; no `w1/` dir yet (this report creates it).
2. `ls /home/vgpnk/Projects/shokunin/*/SKILL.md` → 19 lane SKILL.md exist:
   audio has none; present lanes = chousa, game-dev-3d, kagi, kaidoku, kake, kama, kasegi,
   kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi,
   tsukuroi. (Near-named empty dirs `mori-shokukin/`, `tameshi-shokukin/` hold no SKILL.md
   or tools — verified by `find`; `mori-shokukin` is empty, `tameshi-shokukin` contains only
   an empty nested `tameshi-shokunin` dir.)
3. `grep -iE 'conform|timeout[_ -]?fold|scope.aware' /home/vgpnk/Projects/shokunin/*/SKILL.md`
   → **no matches in any of the 19 SKILL.md**, including mori's own (mori SKILL.md uses
   "scope" only for journal/cgroup/PSI sensor scopes — verified separately with
   `grep -inE 'conform|timeout|fold|scope' .../mori-shokunin/SKILL.md`).
4. `grep -rIlE 'conform|timeout_fold|scope.aware|CONFORM' /home/vgpnk/Projects/shokunin/*/tools`
   → content matches only in: kotodama (`tools/harness/round_runner_conformance.py`,
   `tools/gates/provenance-audit.py`, `tools/gates/costume-era-consistency-gate.py`,
   `tools/check-gate-battery.py`, `tools/harness/claims-freshness.py`, `tools/d2-typed-labels.py`,
   plus frozen/baseline copies under `tools/gates/{frozen,expected}/`), tameshi
   (`tools/registry.json`, `tools/mte-interop.py`), tsukuroi (11 `check-*.py`). Each inspected
   (below).
5. `find /home/vgpnk/Projects/shokunin -maxdepth 3 \( -iname '*conform*' -o -iname '*fold*' \)`
   → only `audio-shokunin/reports/final-namespace-fold.md` (a report; its "fold" is a
   test-family fold of metadata tests, unrelated to AST constant folding).
6. `grep -rlE 'ast\.(parse|literal_eval|walk)|static.?fold' /home/vgpnk/Projects/shokunin/*/tools/`
   → AST users: kotodama `round_runner_conformance.py`, `d2-typed-labels.py` (+ frozen
   copies), `harness/receipt_guard_adoption.py`; mado `mado-tripwire.py`; souji
   `cand-s16-cert.py`; tsukuroi `check-revision-binding.py`, `probe-child-env-allowlist-r3{3,4,6}.py`;
   kaidoku `tools/round-34/elf-version-needs.py` (ELF tooling, unrelated).
7. `grep -rIlE 'timeout_value|drain_bind|drain_shape|CONFORM=|CONFORM_SELFTEST' /home/vgpnk/Projects/shokunin`
   (fleet-wide, excluding mori-shokunin; ran to completion as background job)
   → hits only in: `.ufo/reports/round-{38,39,40}/mori.md` (mori's own fleet receipts),
   `MANIFEST.json` (round-39 closure entry quoting mori's own claim name
   "counter conformance v2" and `drain_shape`), vendored noise
   (`kaidoku-shokunin/.ufo/.../vyper-venv/.../connectionpool.py`,
   `tabi-shokunin/corpus/evidence/.../playwright-core/.../coreBundle.js`).
   **No sibling source file emits `CONFORM=` or names `timeout_value`/`drain_bind`.**
8. `find /home/vgpnk/Projects/shokunin -iname '*conform*' -not -path '*/mori-shokunin/*'`
   (completed in same job) → fleet `.ufo/waves/shokunin12h-...audit/members/*RecordConformance.md`
   (round-14 audit seat docs), `tabi-shokunin/.ufo/waves/round-20/gate-conformance-handoff.md`,
   kotodama `corpus/knowledge/verification/header-conformance-readings.md`,
   `reports/round-3{3,4,5,6}/cross/X02-conformance.md`,
   `reports/round-50/telemetry/final-conformance.json`, and
   `tools/harness/round_runner_conformance.py`. All documents/reports except the last.

## Inspected candidates

- **kotodama `tools/harness/round_runner_conformance.py`** — "Static conformance audit for
  acceptance runners; never executes a runner" (line 2). Its `_constants()` (lines 103–121)
  collects *every* `ast.Assign`/`AnnAssign` found by `ast.walk` into one flat name→value map,
  iterated to fixpoint — **read-site-blind, exactly the defect class mori conform v2 had and
  v3 fixes** (function-local shadows would wrongly enter the map). But the fold is applied
  (lines 175, 190, 288, 357) only to resolve path expressions for write-target auditing of
  `round_runner_*` acceptance runners — `grep -inE 'timeout|subprocess|Popen|communicate|counter'`
  shows no `timeout=`/subprocess/counter resolution. Audited object ≠ mori counters; no
  `CONFORM=` output. → No collision; flagged for completeness: same latent scope-blindness
  bug exists fleet-side if it ever folds values read at multiple sites.
- **mado `tools/mado-tripwire.py`** — contains a genuinely scope-aware binding tracker:
  `module_unsafe_names` (lines 1438–1460) marks names rebound by conditionals, loops,
  tuple/aug/walrus/import targets, and `global`/`nonlocal` in nested scopes; plus
  keyword-arg aware call inspection (lines 1616+, 1844+). Purpose: Hyprland tripwire /
  spawn-command literal analysis (`SPAWN_FUNCS`, `--timeout` CLI-flag parsing at line 547).
  It is not a conformance checker and does not resolve `timeout=` kwarg *values* on
  `Popen`/`communicate`. → Mechanism-adjacent only; no collision. (If mori v3 needed
  precedence, mado's `module_unsafe_names` is independent prior art for the technique.)
- **tsukuroi `tools/probe-child-env-allowlist-r3{3,4,6}.py`** — `ast.walk` audits
  *presence* of the `env` kwarg on `subprocess.run/Popen/call/...` call sites (docstring
  line 49), and observes runtime `timeout` (lines 198–199, 299). Presence check, not a
  scope-aware value fold; no conformance verdict on counters. → No collision.
- **tsukuroi `tools/check-revision-binding.py`** — `ast.parse`/`ast.walk` (lines 288, 823–825)
  used for an import/bind-call census and to enumerate a judge tool's `add_argument` options;
  revision-binding domain, no timeout fold. → No collision.
- **tsukuroi `check-*.py` conformance gates** (check-root-dac-correction, check-source-scope-
  correction, check-locator-clarification, check-section-citations, check-freshness-r17,
  check-review-cohort, check-boot-chain, check-kernel-taint, check-storage-health) —
  "bounded conformance" gates over named corrections/cohorts; none statically folds
  `timeout=` or reads mori counters. `check-source-scope-correction.py` is about *source*
  scope corrections, not Python name resolution. → Name-adjacent only.
- **tameshi `tools/mte-interop.py`** — runtime tally-leg verdicts `MTE_LEG ... CONFORMS|FAILS`
  and `MTE_INTEROP PASS`; executes fixtures, no static analysis. `registry.json` carries the
  expected-output string `legs_conforming=9/9`. → Different surface; no collision.
- **souji `tools/cand-s16-cert.py`** — `ast.parse` only for an assert→recorded-check
  `NodeTransformer` in `tolerant_source` (lines 225+); runtime `--timeout`. → No.
- **kaidoku `tools/round-34/elf-version-needs.py`**, **d2-typed-labels.py / frozen copies** —
  ELF needs / typed-label domain (`D2L-SCOPE` = label scope, not Python scope). → No.
- **audio `reports/final-namespace-fold.md`** — report about folding a test family;
  unrelated meaning of "fold". → No.

## Absence recorded

- No sibling artifact audits a "counter" file or emits `CONFORM=`/`CONFORM_SELFTEST`
  (fleet-wide marker grep, item 7).
- No sibling artifact performs scope-aware static resolution of `timeout=` keyword values
  (only mado has scope-aware name tracking at all, and it targets spawn-config literals,
  not subprocess timeout kwargs).
- No SKILL.md of any lane advertises a conform/timeout-fold/counter-check capability
  (item 3).
- Conformance-named docs under fleet `.ufo` and kotodama reports are prose/telemetry, not
  instruments (item 8).

## Caveats

- Searches covered the working trees as of this run; vendored trees (kaidoku `.ufo` venv,
  tabi node_modules) excluded as third-party noise. I did not search inside `.git`/jj object
  stores or packed history — a collision would need live bytes a seat could invoke, which the
  tree scan covers.
- No tools installed (stock python3/grep/find sufficient). No pacman transactions.
- Unresolved: none material to the collision question.

Report: `.ufo/waves/round-40/w1/ScoutSiblingConform.md`
