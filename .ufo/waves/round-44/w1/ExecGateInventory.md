# ExecGateInventory — lane gate/probe inventory against the `## Gates` standard

Seat: `L1Mori44-4.ExecGateInventory` (round 44, wave 1, executor).
Measured revision: `7cb59c68` → `7cb59c6891d4f5d0266fe062565f094da835dc84` (printed by the auditor on every run).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. No file edited except this report; no row added; SKILL.md untouched.

Instrument bytes (frozen, unmodified): `git show 7cb59c68:tools/mori-gate-registry.py | sha256sum`
→ `743996b11d19261b87e3ea6c0d0be4c0e5e6750d05f6d603af51dc1a7e125a1f`.
`git show 7cb59c68:SKILL.md | sha256sum` equals `sha256sum SKILL.md`
(`f9b1e2bf…6d05`), so the worktree registry is the measured registry.

## 1. What "the standard" is, as the auditor implements it

`## Gates` at `SKILL.md:156`. Its table (header `SKILL.md:162`) is the registry: 23 rows, all 8 cells.
The auditor (`tools/mori-gate-registry.py`) locates `## gates`, takes the **first** table under it whose
header is the eight field names, and **stops at the next `## ` heading** (`parse_gate_table`, lines 74-96).
For a target path it needs a row whose `entry` cell invokes the path (`entry_names`, lines 78-82),
falls back to a substring match when `entry_names` finds nothing, requires all eight cells non-empty,
the path to resolve at `--rev`, and the literal bytes `--selftest` in the tool.

Two consequences that shape everything below: (a) the table scope is exactly one table, and
(b) a `probe` row satisfies the audit exactly like a `gate` row (the `kind` cell is only checked for non-emptiness).

## 2. Inventory of every `tools/*.py` and `tools/*.sh` presenting as a gate or probe

33 files (29 `.py`, 4 `.sh`). All 33 present as a gate or probe: each carries `--selftest`,
a stable verdict token, or a 0/1/2 exit map (scan: `--selftest`, `selftest|SELFTEST|run_selftest`,
`0 clean|could-not-evaluate|_SETUP`, `MORI_[A-Z_]+|C[123]=|REGISTRY=`). None was excluded as a non-gate.

Command shape (one invocation, 33 `--audit` flags):

```
python3 tools/mori-gate-registry.py --rev 7cb59c68 --audit tools/<each>.py --audit tools/<each>.sh
→ rev=7cb59c6891d4f5d0266fe062565f094da835dc84
  REGISTRY=unmet
  EXIT=1
```

### 2a. PASS — 18 tools

| path | kind | `## Gates` row the auditor attributed | audit reason |
|---|---|---|---|
| tools/mori-census.sh | gate | `drift pin` (L165) — **mis-attributed, see §5** | 8 cells, entry resolves, --selftest present |
| tools/mori-silence-cases.sh | gate | `silence oracle` (L166) — matched by substring fallback | 8 cells, entry resolves, --selftest present — **FALSE POSITIVE, see §5.5** |
| tools/mori-content-review.py | gate | `r19 content review (C1)` (L181) | 8 cells, entry resolves, --selftest present |
| tools/mori-dispatch-ledger.py | gate | `r18 dispatch ledger (C3)` (L180) | 8 cells, entry resolves, --selftest present |
| tools/mori-freeze-order.py | gate | `r18 freeze-order (C2)` (L179) | 8 cells, entry resolves, --selftest present |
| tools/mori-gate-registry.py | gate | `r44 gate registry (C2)` (L184) | 8 cells, entry resolves, --selftest present |
| tools/mori-journal-window.py | probe | `journal window (r16)` (L172) | 8 cells, entry resolves, --selftest present |
| tools/mori-misroot-sweep.py | probe | `misroot sweep (r17)` (L176) | 8 cells, entry resolves, --selftest present |
| tools/mori-retention-gate.py | gate | `r18 retention (C1)` (L178) | 8 cells, entry resolves, --selftest present |
| tools/mori-round13-regressions.py | gate | `r13 regressions` (L167) | 8 cells, entry resolves, --selftest present |
| tools/mori-round14-regressions.py | gate | `r14 regressions` (L168) | 8 cells, entry resolves, --selftest present |
| tools/mori-round15-regressions.py | gate | `r15 regressions` (L169) | 8 cells, entry resolves, --selftest present |
| tools/mori-round16-context-check.py | gate | `r16 context check` (L171) | 8 cells, entry resolves, --selftest present |
| tools/mori-round16-regressions.py | gate | `r16 regressions` (L170) | 8 cells, entry resolves, --selftest present |
| tools/mori-round17-context-check.py | gate | `r17 context check` (L177) | 8 cells, entry resolves, --selftest present |
| tools/mori-round17-jj-regressions.py | gate | `r17 jj regressions` (L175) | 8 cells, entry resolves, --selftest present |
| tools/mori-round17-seat-regressions.py | gate | `r17 seat regressions` (L174) | 8 cells, entry resolves, --selftest present |
| tools/mori-seat-terminal.py | probe | `seat terminal status (r17)` (L173) | 8 cells, entry resolves, --selftest present |

Three of these 18 verdicts rest on a weaker match than the row they cite: `mori-census.sh` lands on the
wrong row (§5.1), and `mori-silence-cases.sh` matches only through the substring fallback because
`entry_names` rejects its backtick-terminated entry cell. `mori-round19-regressions.py` (a FAIL, §2b)
matches the same way for the same reason — its entry cell starts `TMPDIR=… python3 …`. One PASS is
outright false: `mori-silence-cases.sh` has **no `--selftest` mode** (§5.5), so the auditor's 18 PASS
contains 1 false positive and its 15 FAIL undercounts non-conformance by one.

### 2b. FAIL — 15 tools

| path | kind | audit reason (verbatim) |
|---|---|---|
| tools/mori-disk-rate.py | probe | `unregistered: no row names mori-disk-rate.py` |
| tools/mori-evidence-loss.py | probe + gate | `unregistered: no row names mori-evidence-loss.py` |
| tools/mori-job-runway.py | gate | `unregistered: no row names mori-job-runway.py` |
| tools/mori-oom-killers.py | gate | `unregistered: no row names mori-oom-killers.py` |
| tools/mori-pressure.py | gate | `unregistered: no row names mori-pressure.py` |
| tools/mori-retention-reconcile.py | gate | `unregistered: no row names mori-retention-reconcile.py` |
| tools/mori-round41-calibration.py | probe | `unregistered: no row names mori-round41-calibration.py` |
| tools/mori-routed-check.py | gate | `unregistered: no row names mori-routed-check.py` |
| tools/mori-routed-r24.py | gate | `unregistered: no row names mori-routed-r24.py` |
| tools/mori-source-drift.py | probe | `unregistered: no row names mori-source-drift.py` |
| tools/mori-sources-appendonly.py | gate | `unregistered: no row names mori-sources-appendonly.py` |
| tools/mori-wave-settlement.py | probe | `unregistered: no row names mori-wave-settlement.py` |
| tools/mori-blind-check.sh | gate | `unregistered: no row names mori-blind-check.sh` |
| tools/mori-index-clean.sh | gate | `unregistered: no row names mori-index-clean.sh` |
| tools/mori-round19-regressions.py | gate | `row 'r19 finite regressions' tool has no --selftest mode` |

## 3. The unregistered set

`--selftest` presence was verified in the tool bytes (a real `--selftest` argv branch, not a docstring
mention): `grep -oE -- '--selftest' tools/<path>` plus a read of the argv branch for the
custom-parser tools. "Registry row" is split by where the row lives, because the auditor reads only
the first table.

| path | gate or probe | `--selftest` | row in `## Gates` | 8-cell row elsewhere in SKILL.md | named in SKILL.md prose only |
|---|---|---|---|---|---|
| tools/mori-disk-rate.py | probe (report-only; exit 0 JSON / 1 unreadable / 2 usage) | no | no | no | **yes** — `## Round34` heading L830, rule bullet L835; no table row anywhere |
| tools/mori-evidence-loss.py | probe (`retained-loss audit`) + gate (`evidence-loss rule comparison`) | yes | no | yes — L526, L527 (`## Round21`) | — |
| tools/mori-job-runway.py | gate | yes | no | yes — L722 (`## Round26` table) | yes — L665 |
| tools/mori-oom-killers.py | gate | yes | no | yes — L720 (`## Round26` table) | yes — L682 |
| tools/mori-pressure.py | gate | yes | no | yes — L645 (`## Round24` table) | yes — L617 |
| tools/mori-retention-reconcile.py | gate | yes | no | yes — L590 (`## Round23` table) | — |
| tools/mori-round41-calibration.py | probe (counts recorded-vs-observed mismatches; `MORI_R41_CALIBRATION`, exit 0/1/2) | no | no | no | **no — not named anywhere in SKILL.md** |
| tools/mori-routed-check.py | gate | no | no | yes — L646 (`## Round24` table; its self-test cell says "none built in") | — |
| tools/mori-routed-r24.py | gate | yes | no | yes — L721 (`## Round26` table) | — |
| tools/mori-source-drift.py | probe | yes | no | yes — L883, L886 (`## Round36` table) | yes — L862 |
| tools/mori-sources-appendonly.py | gate | yes | no | yes — L884, L893 (`## Round36` table) | yes — L868 |
| tools/mori-wave-settlement.py | probe (read-only settlement scan; JSON + lane-wide exit 0/1/2) | yes | no | no | **yes** — `## Wave settlement scan and drift re-pin (r20)` L476 and a 4-column guidance-table row L482 (`When to run the settlement scan`), which is not a registry row |
| tools/mori-blind-check.sh | gate | yes | no | yes — L798 (`## Round32` table) | yes — L776, L778, L793 |
| tools/mori-index-clean.sh | gate | yes | no | yes — L885 (`## Round36` table) | yes — L877 |

Plus the registered-but-non-conforming tools, listed here because they are the ones that are not
"unregistered": **tools/mori-round19-regressions.py** (gate, no `--selftest`, row `r19 finite regressions`
at `## Gates` L182 whose self-test cell honestly describes no `--selftest` mode) and
**tools/mori-silence-cases.sh** (gate, no `--selftest` mode, row `silence oracle` at `## Gates` L166,
audited PASS only because its bytes contain the literal `--selftest` in two comments — §5.5).

### 3a. Named in SKILL.md prose without a registry row — the direct answer

Of the 14 unregistered tools:

- **3 have no 8-cell row anywhere** and are the ones the prose-only question is really about:
  `tools/mori-disk-rate.py` (prose only, L830/L835), `tools/mori-wave-settlement.py`
  (Round20 guidance table L482, not a registry table), and `tools/mori-round41-calibration.py`
  (**named nowhere in SKILL.md at all** — not prose, not a table).
- **11 have a complete 8-cell row** with the standard header, non-empty in all eight cells, in a
  secondary table outside `## Gates`: `mori-evidence-loss.py`, `mori-retention-reconcile.py`,
  `mori-pressure.py`, `mori-routed-check.py`, `mori-routed-r24.py`, `mori-oom-killers.py`,
  `mori-job-runway.py`, `mori-blind-check.sh`, `mori-source-drift.py`,
  `mori-sources-appendonly.py`, `mori-index-clean.sh`. They are registered *somewhere*; the
  auditor simply does not read that somewhere.

Six such tables exist, all with the identical header
`| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`:
L524 (`## Round21`, 2 rows), L588 (`## Round23`, 1), L643 (`## Round24`, 2), L718 (`## Round26`, 3),
L796 (`## Round32`, 1), L881 (`## Round36`, 11 — 5 of them name `tools/` paths, 6 name `.ufo/waves/`
counters).

## 4. The real gap versus the reported gap

- As the frozen auditor measures it: **14 unregistered + 1 thin row** (`REGISTRY=unmet`, exit 1).
  That is the number a round reporting only "its own three counters are registered" would miss.
- Correcting the auditor's one false positive (`mori-silence-cases.sh`, §5.5): **16 of 33 tools
  are non-conforming** — the 14 unregistered, plus `tools/mori-round19-regressions.py` and
  `tools/mori-silence-cases.sh`, neither of which has a `--selftest` mode.
- Under the same eight-cell/resolve/`--selftest` test applied to **all seven** registry tables in
  SKILL.md, the residual gap is **6 tools**:
  - no registry row anywhere: `tools/mori-disk-rate.py`, `tools/mori-wave-settlement.py`,
    `tools/mori-round41-calibration.py`;
  - row exists, no `--selftest` mode: `tools/mori-silence-cases.sh` (`## Gates` L166),
    `tools/mori-round19-regressions.py` (`## Gates` L182), `tools/mori-routed-check.py`
    (`## Round24` L646).
  The other 11 FAILs pass cells + resolve + `--selftest` in their secondary rows.
- So 11 of 15 auditor FAILs are an artifact of table scope, not of missing gate evidence, while the
  no-`--selftest` class is undercounted by one. If the round wants a true operability number it must
  say which of these three it means: 15 (auditor), 16 (auditor corrected), 6 (whole-file scope,
  mode checked).

## 5. Precision defects found in the frozen auditor (reported, not patched)

1. **Wrong row attributed to `tools/mori-census.sh`.** The audit prints
   `row 'drift pin': 8 cells, entry resolves, --selftest present`. The `census` row (L164) is the
   row that registers the bare tool, but its entry cell is
   `` `bash tools/mori-census.sh` (`MORI_SHOKUNIN_ROOT=…`) `` — the path is followed immediately by
   a closing backtick, and `entry_names` requires `(?:\s|$)` after the path, so it returns `False`
   (measured directly: `entry_names(census_cell, "tools/mori-census.sh") = False`;
   `entry_names(drift_pin_cell, …) = True`). The auditor then picks the shortest matching entry cell
   and reports the `--drift` row as the census's registration. A PASS is still produced, so the
   defect hides inside a green line.
2. **The same backtick-termination rejects `silence oracle` (L166)** — that PASS comes only from the
   substring fallback, as does `r19 finite regressions` (L182), whose entry cell starts `TMPDIR=… python3 …`.
3. **Table scope.** `parse_gate_table` stops at the next `## ` heading, so the six secondary
   standard-header tables (§3a) are invisible; 11 conforming registrations are scored as absent.
4. **`kind` is not enforced.** Probe rows satisfy the audit identically (`journal window (r16)`,
   `seat terminal status (r17)`, `misroot sweep (r17)` all PASS). The standard's first cell says
   gate or probe, but the audit cannot tell a probe from a gate.
5. **`--selftest` is a byte-substring test** (`b"--selftest" in body`), not a mode check, and it has
   one measured false positive: **`tools/mori-silence-cases.sh` has no `--selftest` mode at all.**
   The literal occurs exactly twice, both in comments —
   L20 `# Each case runs the actual census CLI (bash "$CENSUS", no --selftest) and` and
   L290 `# idiom the census selftest uses; git deliberately NOT stubbed — real repos)` —
   and its own usage is `bash tools/mori-silence-cases.sh [path-to-census]`. Measured:
   `bash tools/mori-silence-cases.sh --selftest` → `mori-silence-cases: census not readable: --selftest`,
   `rc=2` (the flag is consumed as the census path). The auditor prints
   `row 'silence oracle': 8 cells, entry resolves, --selftest present`, which is false.
   Its `silence oracle` row is honest — the self-test cell reads `itself (hermetic case table, 28 cases)` —
   so the defect is the auditor crediting a comment, not a lying row. The inverted case is
   `mori-round19-regressions.py`, which has the same "self-test is the tool itself" shape and FAILs.
   The same check therefore both over- and under-counts: no `## Gates` PASS is otherwise at risk —
   the remaining 16 PASS tools were read for a real argv branch
   (`args.selftest`, `argv == ["--selftest"]`, `add_argument("--selftest"…)`, or the bash
   `--selftest) selftest=1` case in `mori-census.sh:4721`) and all 16 have one.
6. **Cell content is only checked for emptiness**; a `verdict map` or `self-test` cell of any text
   passes. Not a finding against any row today (all 23 `## Gates` rows carry substantive text).

## 6. Limits

- Registry conformance only. No gate `--selftest` suite was executed by this seat (C2 owns tallies and
  mutant kills); presence and wiring were read from bytes. The one command executed against a tool was
  `bash tools/mori-silence-cases.sh --selftest`, which fails immediately on argument handling
  (`census not readable: --selftest`, rc 2) and runs no case — it is the proof for §5.5, not a tally.
- `tools/fixtures/` and the round-44 counters under `.ufo/waves/round-44/` are out of this
  assignment's scope (`tools/*.py`, `tools/*.sh`); the three r44 rows (L183, L185, L186) name those
  counters and were not audited here.
- Scratch analysis ran from `/tmp` copies of `git show 7cb59c68:SKILL.md`; the lane checkout was not
  mutated and no git write command was run.
