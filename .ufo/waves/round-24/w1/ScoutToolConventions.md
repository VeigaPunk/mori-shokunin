# ScoutToolConventions — round 24 wave 1, C1/C2 conformance of two declared tools to the lane's existing tool conventions

Seat: `MoriR24.ScoutToolConventions`, scout, read-only. Lane repo
`/home/vgpnk/Projects/shokunin/mori-shokunin`, tip read `4059ffb5` (entering tip `c725aa37`,
contract landed `29c1bf45`). Installs and upgrades: none. I read
`/home/vgpnk/.omp/agent/RULES.md`; no tool was needed and no pacman transaction was attempted.

**The tree moved under this read.** My convention reads were taken at tip `4059ffb5`. While I
wrote, the lane advanced to `06a7686e` and two commits landed the C2 implementation: `f6a2970`
froze `tools/fixtures/mori-pressure/cases.json` and `6ee6248` added `tools/mori-pressure.py`.
§1–§4 are contract-vs-convention findings and stand at either tip; §3b records the landed bytes I
re-read afterwards. I ran none of it.

Scope: the JSON schema naming, exit-code conventions, selftest output line shape and
`python3 -I` usage of `tools/mori-wave-settlement.py`, `tools/mori-seat-terminal.py` and
`tools/mori-journal-window.py`, then every place where `.ufo/waves/round-24/contract.md` C1 or
C2 departs from them. No production edit; the only file I created is this report. No git
mutation; no jj command.

Method: direct reads of the three tool files and of the lane/fleet convention sources
(`SKILL.md` registry table, `corpus/QUALITY.md`, `PROTOCOL.md`, `SCORECARD.md`), plus
`git show` of the withdrawn round-23 quota probe. Everything below marked **[OBSERVED]** is a
byte in a file at the cited line; **[INFERENCE]** marks a conclusion I drew from those bytes.
One repo-wide recursive grep for `python3 -I` was interrupted by a 300 s timeout after it had
printed only its first hit; the `-I` evidence below rests on the targeted greps listed, not on
that interrupted sweep.

## 1. The three surfaces as they are

| Fact | wave-settlement (714 lines, r20) | seat-terminal (2942 lines, r17) | journal-window (913 lines, r16) |
|---|---|---|---|
| shebang | `#!/usr/bin/env python3` :1 | same :1 | same :1 |
| schema constant | `SCHEMA = "mori-wave-settlement-v1"` :33; input dispatch files `DISPATCH_SCHEMA = "ufo-swarm-wave-dispatch-v1"` :34 | `SCHEMA = "mori-seat-terminal-v1"` :112 | none for its own output; `ANCHOR_SCHEMA = "mori-journal-anchor-v1"` :43 is the **input** anchor file's schema, validated at :285-300 |
| machine verdict word | `"schema"` discriminator + per-wave `state` :371-380 | `"schema"` + `"finding_id"` ∈ `MORI_SEAT_TERMINAL_OK/_DEAD/_SETUP` :113-115, :1109-1110 | `"finding_id"` ∈ `MORI_JOURNAL_WINDOW_OK/_UNAVAILABLE/_SETUP` :39-41, :493 |
| stdout shape | exactly one compact sorted JSON object + `\n` (`_json_bytes` :62-63, write :709); optional `--out` writes identical bytes :701-708 | exactly one JSON object, docstring :80-84; `_emit` sort_keys/compact/`ensure_ascii=True` :231-236 | exactly one JSON object :105-106, docstring :17 |
| exit map | 0 all waves `settled`/`no-spawn` :379; 1 any other state; 2 usage error / unreadable lane root / non-directory fleet root :698-699, :707-708 (documented SKILL.md:488) | 0 no dead_* seat; 1 ≥1 dead_* seat; 2 setup/unavailable (`prefix-matched-none`, `root-symlink`, `walk-error`, `lstat-failed`, uncaught internal error) :81-84 | 0 `MORI_JOURNAL_WINDOW_OK` :506; 2 for every failure — unavailable :109-116, setup and internal error :906-913. **No exit 1 at all** |
| selftest entry | argv must be exactly `["--selftest"]` :686-688 | `--selftest` argparse flag :2894-2898; refuses scan args with `FINDING_SETUP` rc 2 :2905-2914 | `--selftest` argparse flag :883, :894-895 |
| selftest output | **text tally**: `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (N cases, P passed, F failed)` :671, FAIL variant :640 | **JSON**: `{"finding_id": "SELFTEST_OK"|"SELFTEST_FAIL", "schema": "mori-seat-terminal-selftest-v1", "arms", "passed", ["failures"], "tool_sha256"}` :2787-2804 | **JSON**: `{"finding_id": "MORI_JOURNAL_WINDOW_SELFTEST", "cases", "passed", "failed", "failures"}` :711-719 |
| selftest exit | 0 pass / 1 fail :672 | 0 pass / 1 fail :2787-2804 | 0 pass / **2** fail :719 |
| frozen cases | `.ufo/waves/round-20/frozen/c2-expected.json`, found by walking up from the tool's own dir :383-392, plus in-script `REFINEMENT_CASES` :41-56 | in-script (registry row: pinned values "none", SKILL.md:173) | in-script (SKILL.md:172) |
| `python3 -I` in code | absent | absent | absent |

[OBSERVED] Two further details the tables above imply but are worth stating because the round-24
declarations interact with them: the seat-terminal selftest's own `finding_id` is the bare
`SELFTEST_OK`/`SELFTEST_FAIL` (no `MORI_` prefix) and its selftest `schema` is a string literal
inside the selftest, not a module constant (:2788, :2799-2800). And wave-settlement is the only
one of the three whose selftest emits no JSON object at all.

## 2. Cross-cutting conventions these three sit inside

**[OBSERVED] Registry home.** The lane's tool inventory is the table in `SKILL.md:167-182`
(rows through r19) plus later rows at `SKILL.md:478-488` (wave settlement, r20),
`SKILL.md:522-523` (evidence-loss, r21) and `SKILL.md:586` (retention-reconcile, r23). Every
row's entry column is `python3 tools/<name>.py ...`; **`-I` never appears in a registry entry.**

**[OBSERVED] Fleet gate clause** (`PROTOCOL.md:380-406`): `0` = `clean`, `1` = `failed`
fleet-wide; every other code a gate exits is declared in its registry entry and mapped onto
`clean | failed | could-not-evaluate`, and an undeclared nonzero code reads as
could-not-evaluate (`:380-384`). "Every gate exposes a self-invocation mode over isolated fixtures
... asserting both the exit code and a stable expected finding-id, with the expected values
committed in the owning repo and independent of the recomputation" (`:385-389`). Row fields: name,
`gate|probe`, entry command, verdict map (code → class), self-test command and spelling,
pinned-value path, write scope, owner (`:398-403`). `PROTOCOL.md:404-405`: frozen baseline names
resolve under any `.ufo/waves/*/frozen` root; a bare name matching more than one root fails closed.

**[OBSERVED] `python3 -I` is an evidence-command convention, not a tool contract.** It appears in
measurement and declaration commands: `SCORECARD.md:1465` (round-23 MeasureDriver),
`SCORECARD.md:1481` (retention-gate `scan` at `4994c0d`), `SCORECARD.md:1501-1502` (the round-24
C1/C2 declaration rows themselves), and the round-23 falsifier argv, e.g.
`.ufo/waves/round-23/falsify/QBtrfsSquota.md:55`:
`argv: python3 -I .../tools/mori-quota-surface.py --fixture /fast/scratch/.../fixture.json`.
None of the three tools mentions `-I` in its own bytes.

**[OBSERVED] What `-I` costs.** Host `python3 -V` → `Python 3.14.8`. `-I` implies `-E -s -P`, so
the script's own directory is not `sys.path[0]`: `python3 -I /tmp/_sptest.py` prints
`/usr/lib/python314.zip`, while `python3 /tmp/_sptest.py` prints `/tmp` (my run, same host).
[INFERENCE] A tool whose after-value command uses `-I` must be self-contained: no sibling-module
import from `tools/`, no reliance on `PYTHON*` environment variables.

**[OBSERVED] Selftest output has three families in this lane, not one.**

- (a) `MORI_<TOOL>_SELFTEST: PASS (N cases, P passed, F failed)` — wave-settlement :671; the census
  prints the same grammar (`MORI_CENSUS_SELFTEST: PASS (56 cases, 56 passed, 0 failed)`,
  `corpus/knowledge/selftest-flake-r9.md` §4).
- (b) `SELFTEST <tool> PASS n/N` — `tools/mori-retention-gate.py:703` (FAIL :701, :704, rc 1) and
  `tools/mori-freeze-order.py:670` (`SELFTEST freeze-order PASS %d/12`, rc 0; FAIL to stderr at
  :666, :670, rc 1).
- (c) JSON object with `schema` + `finding_id` — seat-terminal :2787-2804, journal-window :711-719,
  `tools/mori-evidence-loss.py` (`SELFTEST_SCHEMA = "mori-evidence-loss-selftest-v1"` :28),
  `tools/mori-retention-reconcile.py:274` (`RECONCILE_SELFTEST_PASS/FAIL`, rc `int(passed!=total)`),
  `tools/mori-misroot-sweep.py` (`MORI_MISROOT_SELFTEST_OK/_FAIL/_SETUP`),
  `tools/mori-content-review.py:464` (`findings: [{"code": "CONTENT_REVIEW_SELFTEST_CLEAN"}]`),
  and the withdrawn round-23 probe (`git show 1979a9d:tools/mori-quota-surface.py`,
  `finding_id` `QUOTA_SELFTEST_OK`/`QUOTA_SELFTEST_FAIL` at its :1863-1873).

[OBSERVED] Counted over `tools/*.py` (19 files): `grep -L -- '--selftest' tools/*.py` returns
exactly one file, `tools/mori-round19-regressions.py`. The other 18 carry the flag.

**[OBSERVED] Frozen case files live under the wave, not under `tools/`.**
`.ufo/waves/round-20/frozen/c2-expected.json` (wave-settlement :386), `.ufo/waves/round-21/frozen/cases.json`
(`tools/mori-evidence-loss.py classify --cases ...`, SKILL.md:523; schema
`mori-evidence-loss-cases-v1` :32), `.ufo/waves/round-23/frozen/quota-cases/*.json` (case schema
`mori-quota-case-v1`, fixture schema `mori-quota-fixture-v1`). `tools/fixtures/` did not exist at
my first read (`ls tools/fixtures` → `No such file or directory` at `4059ffb5`); it first appears
with this round's cases commit `f6a2970`.

**[OBSERVED] Synthetic-mode precedent** (round-23 quota probe, `git show 1979a9d:...`):
`--fixture FILE` synthetic mode in which "the fixture file is the only file opened" (:84-89,
parser :823-824), usage errors for unknown args, relative `--path`, `--fixture` together with
`--path`, and `--selftest` together with any other flag (round-23 contract :74 and the tool's own
docstring :88-89).

## 3. C2 (`contract.md:51-103`) against those conventions

**D1 — the selftest line shape is a hybrid with no exact precedent, and it carries no finding id.**
[OBSERVED] Contract :82 declares `MORI_PRESSURE_SELFTEST: PASS n/12` (or `FAIL`). Family (a) uses
the `MORI_<TOOL>_SELFTEST:` prefix with a parenthesised `(N cases, P passed, F failed)` tally;
family (b) uses the bare `SELFTEST <tool>` prefix with the `n/N` tally. C2 takes the prefix of (a)
and the tally of (b). No existing tool prints `MORI_<TOOL>_SELFTEST: PASS n/N`. [INFERENCE] The
tally grammar itself is fine; the real departure is that 2 of the 3 named surfaces, and every
newest tool (evidence-loss r21, retention-reconcile r23, quota-surface r23), publish the selftest
as a JSON object with a stable finding id, while C2 publishes a text line with none — and
`PROTOCOL.md:385-389` requires the self-test to assert "a stable expected finding-id". Wave
settlement's text line is C2's only precedent among the three named surfaces.

**D2 — the selftest's own exit code is undeclared.** [OBSERVED] Contract :97 fixes only the passing
case (`exit 0`). The three surfaces split: wave-settlement 0/1 (:672), seat-terminal 0/1
(:2787-2804), journal-window 0/2 (:719). `PROTOCOL.md:385-389` requires the self-test to assert the
exit code. A builder that picks 2 will look like journal-window; one that picks 1 will look like
the other two; the contract does not say which, and the after-value command does not pin it.

**D3 — `PRESSURE_PARTIAL` exits 0.** [OBSERVED] Contract :77-79: exit 1 on `PRESSURE_HIGH`, exit 2
"when every resource is unavailable or on usage error; else exit 0 (PARTIAL means at least one
resource unavailable or malformed)". Among the three surfaces, an unavailable input is exactly what
maps to 2 — journal-window sends every unavailable path to `_fail(...)` → 2 (:109-116) and
seat-terminal's 2 is "setup/unavailable" (:81-84) — and the round-23 quota probe put its unknown
state on 2 (`Exit 2 QUOTA_STATE_UNKNOWN`, tool :104-106). [OBSERVED] One lane precedent does exit 0
with a non-clean verdict word: retention-reconcile "0 RETENTION_RECONCILED even when red"
(SKILL.md:586). [INFERENCE] That precedent is a *completed* comparison, not an unreadable input, so
C2 remains the only declared mapping in this set where an unreadable or malformed resource still
exits 0. It is declared, so it does not violate `PROTOCOL.md:380`; it does depart from the three
surfaces and from the r23 comparable.

**D4 — no `finding_id`; a new top-level `verdict` enum.** [OBSERVED] Contract :75-77 declares
`schema`, `resources`, `verdict` ∈ `PRESSURE_OK|PRESSURE_HIGH|PRESSURE_PARTIAL|PRESSURE_UNAVAILABLE`,
`findings[]`. The named surfaces' machine verdict word is `finding_id` (seat-terminal :112-115,
journal-window :39-41) or `schema` + per-object state (wave-settlement :33, :371-380). No
`tools/*.py` emits a top-level `verdict` key: `tools/mori-freeze-order.py` uses `verdict` as a
**row** field with values like `could-not-evaluate`/`pre-build` (:255, :298-318) and
`tools/mori-retention-gate.py` uses a boolean `verdict_match` (:383, :390). [INFERENCE] `findings[]`
as a key is precedent-backed (`tools/mori-dispatch-ledger.py:336`, `tools/mori-content-review.py:162`),
but its item vocabulary there is `finding_id`/`code`, not the interface's `{id, resource}`. Net:
C2's verdict vocabulary is new top-level surface, and the round-24 tool will not be readable by the
same key a reader of the other probes uses.

**D5 — the contract prose omits the `root` key the cases interface requires.** [OBSERVED] The frozen
cases interface (wave context) fixes the top level as `schema`, `root`, `resources`, `verdict`,
`findings`; contract :75-77 lists schema, resources, verdict, findings only. The builder prompt
says "exactly per contract.md section C2 **and** the shared cases interface in the wave context",
so the two must agree; as written the contract under-specifies its own output. [INFERENCE] This is
a contract-vs-interface gap, not a departure from the three tools, but it is the one place where
following the contract literally would produce a JSON object the frozen matcher does not expect.

**D6 — frozen cases are placed under `tools/`, in a new `tools/fixtures/` root.** [OBSERVED]
Contract :80 puts them at `tools/fixtures/mori-pressure/cases.json`. Every other frozen case set
sits under `.ufo/waves/<round>/frozen/` (§2). `PROTOCOL.md:404-405` resolves frozen baseline names
under `.ufo/waves/*/frozen` roots only, so this path is outside the protocol's resolution rule, and
`tools/fixtures/` did not exist before this round. The *schema name* `mori-pressure-cases-v1` is
not a departure — it matches `mori-evidence-loss-cases-v1` (`tools/mori-evidence-loss.py:32`) and
`mori-quota-case-v1`. [INFERENCE] Two consequences for the L1: the registry row's pinned-value
column will point outside the protocol's frozen roots, and the tool ships its own fixture, so a
later edit of `cases.json` is not covered by the "expected values committed ... independent of the
recomputation" clause unless the cases file is frozen by digest.

**D7 — no CLI-visible synthetic mode.** [OBSERVED] Contract :83 injects snapshots and errnos "using
an in-process open hook, documented as such". The round-23 comparable had `--fixture FILE` with the
fixture file as the only file opened (round-23 contract :74; tool :84-89). [INFERENCE] As declared,
a frozen case can only be replayed through `--selftest`; there is no way for an independent seat to
run one case from the CLI, which is how the round-23 cases were falsified (`--fixture` argv in
every `Q*` report). This is a departure from the r23 comparable, not from the three named surfaces
(whose selftests are in-script too).

**D8 — `--selftest` combined with other flags is undeclared.** [OBSERVED] The three surfaces differ:
wave-settlement accepts only the bare argv `["--selftest"]` (:687), seat-terminal refuses scan args
with rc 2 (:2905-2914), the quota probe made `--selftest` with any other flag a usage error
(tool :1802-1803). C2 declares `--root` and `--interval` (:60, :72) and says nothing about
combining them with `--selftest`. [INFERENCE] Minor, but it is the kind of case the frozen
`expect.exit` interface can express (a case with `--selftest --interval 1` would have to be
refused or honoured), so the ambiguity can surface in the selftest itself.

**D9 — the usage-error payload is undeclared.** [OBSERVED] Contract :77-79 declares exit 2 on usage
error but not what is printed. journal-window emits `{"finding_id": MORI_JOURNAL_WINDOW_SETUP,
"reason": ...}` (:109-116, :906-913); wave-settlement prints nothing on stdout and one line on
stderr (:698); seat-terminal emits its `FINDING_SETUP` object (:241-245); the quota probe had a
`QUOTA_SETUP` finding. C2's exit 2 also carries a *verdict* word (`PRESSURE_UNAVAILABLE`), so a
reader cannot tell setup from an all-resources-unavailable run by exit code alone — which is
precisely the class `corpus/QUALITY.md:11` (criterion 6, "a crash exit code never equals a verdict
code") and `PROTOCOL.md:380-384` exist to keep legible.

**Not departures in C2.** [OBSERVED] `python3 -I tools/mori-pressure.py --selftest`
(contract :89, :97) matches the evidence-command convention (§2), and because `-I` consumes the
python flags, `sys.argv` is still exactly `["--selftest"]` for a bare-argv tool. The schema name
`mori-pressure-v1` matches `<stem>-v1`. `--interval` bounds `0 < S ≤ 10` and the `total_delta_us` /
`stall_ratio` fields have no convention conflict. [INFERENCE] The one thing the registry row should
not do is copy the `-I` from the after-value command into the entry column; every existing registry
entry is written as plain `python3 tools/<name>.py ...`.

### 3b. Landed bytes, observed after the tree moved (contract-vs-implementation, not a verdict on the claim)

[OBSERVED] `tools/mori-pressure.py` is 569 lines, committed at `6ee6248`; the cases file is
committed at `f6a2970`. Read-only observations against the conventions in §1–§2:

- Schema constants match precedent: `SCHEMA = "mori-pressure-v1"` :66,
  `CASES_SCHEMA = "mori-pressure-cases-v1"` :67, `SELFTEST_PREFIX = "MORI_PRESSURE_SELFTEST"` :68.
- **JSON is pretty-printed, not one line.** `_emit` :389-390 is
  `json.dumps(payload, sort_keys=True, indent=2)`. All three named surfaces emit one compact line
  with `separators=(",", ":")` (wave-settlement :64, seat-terminal :233, journal-window :106).
  [INFERENCE] This is the one delivered-bytes departure the contract did not ask for; the lane's
  JSON receipts are single-line (`SKILL.md:478` "byte-identical on re-run of an unchanged tree;
  commit it with the scan time as the settlement receipt"). Any later consumer that diffs the
  receipt byte-wise, or that greps for a one-line object, sees a different shape than every other
  mori tool.
- Payload keys :347-358: `schema`, `root`, `threshold{metric,value,label}`, `resources`, `verdict`,
  `findings`; with `--interval` also `interval_s` and `elapsed_us` (:359-361). [INFERENCE] `root`
  resolves D5 in the delivered object; `threshold`, `interval_s` and `elapsed_us` are undeclared
  additions to contract :75-77 (the interface's subset matching should tolerate them, but the
  contract and the object are not the same set of keys).
- Exit mapping :338-345 implements contract :77-79 exactly, including D3's `PARTIAL` → rc 0.
- Usage errors: `_Parser.error` raises `_UsageError` (:369-372); `main` emits
  `{"schema", "root", "error"}` and returns 2 (:389-394, :546-550). So D9's payload is a schema-only
  setup envelope with **no stable finding id** — a reader must key on the `error` key to tell setup
  from `PRESSURE_UNAVAILABLE`, which shares exit 2.
- Selftest exits, resolving D2 concretely but in two classes: `PASS n/N` → 0 (:540-541); case
  failures → `FAIL n/N` plus one line per failed case id → 1 (:536-539); a missing, unreadable,
  wrong-schema or empty cases file → `MORI_PRESSURE_SELFTEST: FAIL 0/0` → 2 (:496-520). The contract
  declared neither code. [INFERENCE] The `FAIL 0/0` form also drops the total, where retention-gate
  keeps it (`SELFTEST retention-gate FAIL 0/21`, :462-475).
- `--selftest` is checked (:551-552) **before** `--interval` and `--warn-avg10` validation
  (:553-558), so `--selftest --interval 99` runs the selftest and ignores the interval. D8 is
  therefore resolved permissively, and differently from seat-terminal's refusal (:2905-2914).
- Cases resolution: `_cases_path()` (:396-404) tries `<script_dir>/fixtures/mori-pressure/cases.json`
  then `<script_dir>/../tools/fixtures/mori-pressure/cases.json`; there is no walk-up to the lane
  root. [INFERENCE] Under `python3 -I` this still resolves (the path is built from the script's real
  path), but a copy of the tool without the fixtures tree exits 2 with `FAIL 0/0` rather than
  reporting a case failure.
- An undeclared guard: negative `--warn-avg10` emits the setup envelope and returns 2 (:556-558).

## 4. C1 (`contract.md:11-50`) against those conventions

**E1 — no `--selftest` is declared, in a lane where 18 of 19 `tools/*.py` carry one.**
[OBSERVED] C1's whole section declares `--repo`, `--rev`, the output object and the exit map
(:20-34); the falsifier is "one sandbox mutant per item" (:39-41). All three named surfaces carry
`--selftest`; `grep -L -- '--selftest' tools/*.py` returns only `mori-round19-regressions.py`; and
`PROTOCOL.md:385-389` requires every **gate** to expose a self-invocation mode asserting exit code
plus a stable expected finding-id, with the registry recording the spelling. [INFERENCE] If
`mori-routed-check.py` is registered as a `gate`, its registry row's self-test column has no value,
and the check's own comparison logic is the only thing that decides `held` — nothing in the tool
can show the comparison itself is alive. C2 by contrast does declare one. `corpus/QUALITY.md:100`
(criterion 39) only forbids *running* a selftest before the integration owner does, so it does not
make a selftest optional for a gate.

**E2 — no registry row is declared.** [OBSERVED] C1 promises "Each item becomes a QUALITY.md
criterion line tagged `routed r23-R<n>`" (:49) but names no `SKILL.md` registry row, while C2
declares a "SCORECARD capability row" (:98) and the wave-1 spec asks a seat to draft the pressure
tool's registry row in the table's column shape. [INFERENCE] The lane's tool inventory is the
registry table (§2), so C1 would land a new gate that the inventory does not list. `PROTOCOL.md:398-403`
is where row fields are defined. Secondary, but
it is the same class as E1. [OBSERVED] Minor path precision: :49 writes `QUALITY.md` where the
lane file is `corpus/QUALITY.md` (SKILL.md:478, :484 cite it that way).

**E3 — the nested `verify` exit code is not mapped.** [OBSERVED] R4 (:26-30) requires each round-24
attempts file to "verify clean with `tools/mori-dispatch-ledger.py verify` at REV". That tool's own
codes are `RC_CLEAN = 0`, `RC_FINDINGS = 1`, `RC_UNAVAILABLE = 2`
(`tools/mori-dispatch-ledger.py:18-20`), and its parser exits `RC_UNAVAILABLE` on usage errors
(:347-350). C1 does not say whether a nested rc 2 (could-not-evaluate) marks the R4 item red, makes
the check itself exit 2, or is reported as a third per-item state. [INFERENCE] This is the one place
where C1's map can silently read a nested setup code as a verdict — the exact conflation
`corpus/QUALITY.md:11` names — and R4 is the only item whose verdict depends on another tool's exit
code.

**E4 — the exit-2 payload is undeclared.** [OBSERVED] :32-34 fixes exit 2 for "repo/rev/base cannot
be read" but not what is printed. The three surfaces disagree on this path too (wave-settlement
prints nothing on stdout :698; journal-window and seat-terminal print a setup object), so the gap
is the same class as C2 D9 and, unlike D9, C1 does not even declare a verdict word for the setup
case.

**E5 — flat CLI, no subcommand.** [OBSERVED] C1 declares `--repo PATH --rev REV` with no verb
(:20-21). The comparable revision scanners use one: `scan` (wave-settlement :678-680, retention-gate
:714), `check` (freeze-order :684, content-review :346), `verify` (dispatch-ledger :559). The
round-23 quota probe was flat (`--path`), so precedent is mixed. [INFERENCE] Minor, and it costs
nothing; listed for completeness, not as a defect.

**Not departures in C1.** [OBSERVED] `schema: mori-routed-check-v1` matches `<stem>-v1`. A
`schema`-only output object with no `finding_id` is exactly wave-settlement's shape (:33, :372).
Exit 0/1/2 with 1 = a real failed item and 2 = could-not-evaluate is the lane's and the fleet's map
(SKILL.md rows, `PROTOCOL.md:380-384`). The after-value command
`python3 -I tools/mori-routed-check.py --repo ... --rev ...` (contract :38) matches the
evidence-command convention. And because C1's after-value is the check's own live run rather than a
selftest tally, the missing `--selftest` (E1) does not leave the claim without a measurement — it
leaves the *instrument* without an independent liveness arm, which is what the mutant arms (:39-41)
and the before-value `held: 3` (:36-37) partially cover.

## 5. What this does not establish

- [UNKNOWN] Whether the L1 will register `mori-routed-check.py` and `mori-pressure.py` as `gate` or
  `probe`. The self-test clause (`PROTOCOL.md:385-389`) binds gates; the registry row is required
  either way, and C1 declares no row at all. Nothing in the contract decides this.
- [UNKNOWN] Whether `tools/fixtures/` is intended as the lane's new fixture home. It has no other
  occupant, and no convention document names it; if it is meant to be durable, `PROTOCOL.md:404-405`
  and the registry's pinned-value column need to be reconciled with it.
- [UNKNOWN] Whether C2's selftest FAIL line should print per-case ids. The wave-1 build prompt adds
  "plus one line per failed case id"; contract :82 does not say it. Two sources, two shapes.
- [UNKNOWN] Whether the seat that freezes `cases.json` is expected to publish its digest anywhere
  C2 can pin. The commit order now satisfies "landed before the tool" (`f6a2970` cases, then
  `6ee6248` tool), but the contract names no digest or freeze commit, so
  `PROTOCOL.md:390-397`'s "expected values committed ... independent of the recomputation" is not
  demonstrable from the contract text alone — the cases file is only protected by git history, not
  by a pin the selftest verifies.
- [NOT RUN] I did not run any of the three tools, any `--selftest`, or the new tools. At my first
  read (`4059ffb5`) neither `tools/mori-pressure.py` nor `tools/mori-routed-check.py` existed
  (`ls` → `No such file or directory` for both); by the time of writing, `tools/mori-pressure.py`
  and `tools/fixtures/mori-pressure/cases.json` are present at HEAD `06a7686e` (commits `6ee6248`
  and `f6a2970`, see §3b) and `tools/mori-routed-check.py` still does not exist. Every exit code and
  output shape above is read from source bytes or from the registry/protocol documents, not
  observed from a run.
- [NOT RUN] The repo-wide recursive `grep -rln 'python3 -I'` over `*.md` was interrupted by a 300 s
  timeout; the `-I` inventory above comes from targeted greps (`SCORECARD.md`, round-23 falsify
  directory, the three tool files, `SKILL.md`, `PROTOCOL.md`) and may miss a further mention
  elsewhere in the tree.
