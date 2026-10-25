# ConnCrossClaim — round-47 wave w1: cross-claim and cross-round pattern check

Seat: `ConnCrossClaim` (connector, leaf — no subagents dispatched).
Date: 2026-10-25.
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Fleet root: `/home/vgpnk/Projects/shokunin`.
Frozen contract: `.ufo/waves/round-47/contract.md` (committed at freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0`, entering tip `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`).

---

## 1. Executive Summary

This report delivers the cross-claim and cross-round pattern analysis requested by the assignment:
1. **(a) Causal separability**: C1 (calibration) and C2 (depth) are causally separable as specified in `contract.md:80-84`. C1's counting command (`tools/mori-pin-check.py`) executes `--selftest` commands of gate rows in an isolated `git archive` export and touches only `SKILL.md` registry cells; C2's counting command (`.ufo/waves/round-47/count-c2.py`) evaluates only `corpus/knowledge/oom-tracepoints-r47.md`, `corpus/SOURCES.md` (row S475), and `corpus/evidence/sources-r47/`. However, a second-order coupling was identified in the working-tree draft of `SKILL.md`, where ephemeral wave counter `count-c2.py` was registered as a permanent gate row at line 926. If committed, this couples C1 to C2.
2. **(b) Claim surface vs Round 46 closure (Re-scoring: Quality vs Calibration)**: C1 does **not** repeat round 46's claim surface in a manner that would justify the closure re-scoring it as quality or operability. In round 46, the closure verifier spot-check independently re-measured the four repaired pins (`SKILL.md:184, 190, 191, 194`) and already ruled `calibration: improved` (`corpus/lessons/round-46-verifier-spotcheck.md:39-45`). If round 47 C1 merely re-measured those same four cells with a non-vacuous tool, precedent from round 45 C1 (`SCORECARD.md:2553`) and `scripts/hyaku/lane-addendum.md:295-299` would classify the move as operability or quality (instrument conformance). Round 47 C1 avoids this because it uncovers and fixes a previously uncaught, genuinely drifted self-assessment pin at `SKILL.md:912` (`MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` vs observed `pass=22 fail=0`, stale since round 41 commit `d72ac167`). The surface changed is `SKILL.md:912`, not the four round-46 cells.
3. **(c) C2 depth framing vs AXES.md definitions**: C2's framing matches `AXES.md:11` ("Verifiable technical detail ... cited sources"). It provides an exhaustive, field-by-field catalogue of all 8 `TRACE_EVENT` declarations from Linux v7.2 `include/trace/events/oom.h`, their complete `TP_STRUCT__entry` field sets, and emitting kernel call sites, cited via new mined tier-A code row S475. While AXES.md mentions "decision tables with real thresholds", C2 establishes an architectural decision boundary ("attribution ceiling" for FR13): `mark_victim` carries memory and process identity, but no cgroup path and no culprit task, proving an observer cannot attribute container culpability from kernel OOM tracepoints alone.
4. **UFO-FSD Connector Move**: Decouple ephemeral round-47 counter `count-c2.py` from `SKILL.md`. Register only permanent lane tools (`tools/mori-pin-check.py`) in `SKILL.md:925`, omitting line 926. This preserves pure causal separability across git reverts and prevents the recurring round-45 mistake class where registering wave counters produced stale registry pins that harmed calibration.

---

## 2. Observed Evidence (Commands, Outputs, Exit Codes)

All commands were run in `/home/vgpnk/Projects/shokunin/mori-shokunin` with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ConnCrossClaim`:

### 2.1 Revisions and Instrument Freezes
- Entering tip: `2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (round-46 closure `corpus/lessons/round-46-verifier-spotcheck.md`).
- Freeze commit: `63eecf2738db96f46b0bd02b1b2dfd66787493d0` (`git rev-parse HEAD` at freeze).
- Freeze diff: 25 files committed at freeze, including `tools/mori-pin-check.py`, `.ufo/waves/round-47/count-c2.py`, controls, evidence receipts, and four Linux v7.2 source files under `corpus/evidence/sources-r47/`. `SKILL.md` was unchanged between entering and freeze commits.

### 2.2 Instrument Self-Tests
- `tools/mori-pin-check.py --selftest`:
  ```text
  PASS honest  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
  PASS stale_tally  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
  PASS stale_in_cell_true_elsewhere  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
  PASS pin_moved_out_of_cell  PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
  ...
  PIN_CHECK_SELFTEST pass=22 fail=0
  ```
  Exit code: 0.

- `.ufo/waves/round-47/count-c2.py --selftest`:
  ```text
  PASS honest  C2=met events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture
  PASS missing_event_three_of_eight_class  C2=unmet events=2 rows=1 name_mismatch=1 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture failed=name_mismatch
  ...
  C2_SELFTEST pass=13 fail=0
  ```
  Exit code: 0.

### 2.3 Entering-State Measurement (C1 Do-Nothing Control)
- `python3 tools/mori-pin-check.py --rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53`:
  ```text
  pin line=166 kind=tally prefix=MORI_SILENCE_CASES_SELFTEST state=match pinned='pass=24 fail=0' observed='pass=24 fail=0' rc=0 cmd='bash tools/mori-silence-cases.sh --selftest'
  ...
  pin line=184 kind=tally prefix=GATE_REGISTRY_SELFTEST state=match pinned='pass=15 fail=0' observed='pass=15 fail=0' rc=0 cmd='python3 tools/mori-gate-registry.py --selftest'
  pin line=184 kind=digest state=match digest=8b82ac999091 file=tools/mori-gate-registry.py
  pin line=190 kind=tally prefix=C1_SELFTEST state=match pinned='pass=16 fail=0' observed='pass=16 fail=0' rc=0 cmd='python3 .ufo/waves/round-45/count-c1.py --selftest'
  pin line=191 kind=tally prefix=C2_SELFTEST state=match pinned='pass=14 fail=0' observed='pass=14 fail=0' rc=0 cmd='python3 .ufo/waves/round-45/count-c2.py --selftest'
  pin line=194 kind=tally prefix=GATE_REGISTRY_SELFTEST state=match pinned='pass=15 fail=0' observed='pass=15 fail=0' rc=0 cmd='python3 tools/mori-gate-registry.py --selftest'
  ...
  pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest'
  PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 baseline=yes
  ```
  Exit code: 1.
  Key observation: Exactly 26 tally pins and 5 digest pins are found. The four round-45/46 pins at lines 184, 190, 191, 194 all evaluate to `state=match`. The **sole mismatch** across the entire registry is line 912 (`MORI_SOURCES_APPENDONLY_SELFTEST`).

### 2.4 Freeze-State Measurement (C2 Do-Nothing Control)
- `python3 .ufo/waves/round-47/count-c2.py 63eecf2738db96f46b0bd02b1b2dfd66787493d0`:
  ```text
  C2=unmet events=8 rows=0 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=bad provenance=bad rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 failed=entry_absent,source_row
  ```
  Exit code: 1.

### 2.5 Probe of Working-Tree SKILL.md Coupling
- Running `tools/mori-pin-check.py --rev 2d85e33... --skill SKILL.md ...` against the working tree draft:
  ```text
  pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0 cmd='...'
  pin line=925 kind=tally prefix=PIN_CHECK_SELFTEST state=mismatch pinned='pass=22 fail=0' observed=None rc=2 cmd='python3 tools/mori-pin-check.py --selftest'
  pin line=926 kind=tally prefix=C2_SELFTEST state=mismatch pinned='pass=13 fail=0' observed=None rc=2 cmd='python3 .ufo/waves/round-47/count-c2.py --selftest'
  PIN_CHECK=unmet tally_pins=28 digest_pins=5 mismatches=2 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 ...
  ```
  Exit code: 1.
  Key observation: Line 912 flips to `match` as expected. However, lines 925 and 926 in the draft table register tools inside revision `2d85e33...` where they did not exist, causing `rc=2`. Specifically, line 926 introduces `count-c2.py` as a tally pin evaluated by `mori-pin-check.py`.

---

## 3. Analysis (a): Causal Separability of C1 and C2

### 3.1 Contract Specification
`contract.md:80-84` states:
> "C1 touches only SKILL.md registry cells and `tools/mori-pin-check.py`; C2 touches only the FR13 knowledge entry, its SOURCES rows and `corpus/evidence/sources-r47/`. Either counter can be run with the other claim's changes reverted."

`AXES.md:30-32` states the fleet rule:
> "Claims must be causally separable — each verifiable without the others having landed — and name distinct axes; two claims on one axis in one round count as one claim."

### 3.2 Evaluation of Separability
1. **From C1 to C2**:
   - C1 measures whether all tally pins and sha256 digests in `SKILL.md` reproduce from revision R.
   - The counting command `python3 tools/mori-pin-check.py --rev R --min-tally-pins 26 --baseline-rev 2d85e33...` exports R with `git archive` and inspects only tables containing `self-test` headers in `SKILL.md`.
   - If C2's knowledge entry (`corpus/knowledge/oom-tracepoints-r47.md`), S475 in `corpus/SOURCES.md`, and `corpus/evidence/sources-r47/` are completely reverted or never landed, C1 evaluates without error: none of these paths are read or checked by `mori-pin-check.py`.
   - In `SKILL.md:912`, `tools/mori-sources-appendonly.py` is tested via `--selftest`, which uses synthetic fixtures created under TMPDIR; it does not read `corpus/SOURCES.md`.
   - The baseline revision `2d85e33...` carries 26 tally pins (meeting the floor of 26); none of those baseline pins belong to C2.

2. **From C2 to C1**:
   - C2 measures the 8 `TRACE_EVENT`s from `corpus/evidence/sources-r47/include_trace_events_oom.h` catalogued in `corpus/knowledge/oom-tracepoints-r47.md` and row S475 in `corpus/SOURCES.md`.
   - The counting command `python3 .ufo/waves/round-47/count-c2.py R` reads exclusively from `corpus/` via `git show`. It contains zero references to `SKILL.md` or `tools/mori-pin-check.py`.
   - If C1 is completely reverted (i.e., `SKILL.md:912` retains `pass=15 fail=0`), `count-c2.py` still evaluates to `C2=met`.

### 3.3 The Second-Order Coupling Contradiction
Although the frozen contract defines pure separability, a practical leakage exists in the working-tree integration draft:
- In `SKILL.md`, draft lines 923–926 add a new gate table registering both `tools/mori-pin-check.py` (line 925) and `.ufo/waves/round-47/count-c2.py` (line 926).
- Line 926 carries the pin: `` `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` ``.
- Because `mori-pin-check.py` parses *every* table in `SKILL.md` with a `self-test` header, adding line 926 causes C1 to execute C2's wave counter on every C1 evaluation.
- If C2 is reverted or its counter modified, C1 fails. This contradicts `contract.md:83-84` ("Either counter can be run with the other claim's changes reverted").
- **Verdict on (a)**: C1 and C2 are causally separable under their frozen contract definitions; however, committing C2's counter into `SKILL.md` destroys this separability. Section 6 proposes the bounded fix.

---

## 4. Analysis (b): C1 Surface vs Round 46 Closure — Re-scoring (Quality vs Calibration)

### 4.1 The Round-46 Closure Precedent
In round 46:
- The lane declared C1 (calibration repair) to fix four stale registry cells from round 45 (`SKILL.md:184, 190, 191, 194`), but used `count-repins.py`, which checked whole-row substring occurrences rather than semantic cells.
- The lane declared C1 `unprovable` due to the counter's reachability by false-green mutations (`corpus/lessons/round-46.md` M1).
- The non-author closure verifier spot-check (`corpus/lessons/round-46-verifier-spotcheck.md:39`) ruled:
  > "However, **my own direct re-measurement of the four pins against the committed instruments shows every pinned tally, digest and line count matches observed instrument state**. The round-45 harm (four stale registry cells at SKILL.md:184/190/191/194) is therefore repaired, even though the counter is weak. I grade the **calibration axis on my own measurement: improved**, and say so explicitly ... I grade calibration improved; operability unchanged."
- The closure routed defect 1:
  > "Replace or retire `count-repins.py` as a calibration proof. It must parse designated cells (`split("|")`), require each needle inside its own semantic cell, re-measure instruments live at check time (selftest tally, sha256, line count), count mismatches per pin, and ship a red-before stale-string control before it is used to declare any claim again."

### 4.2 The "Re-scoring" / Quality Trap
Under fleet doctrine (`scripts/hyaku/lane-addendum.md:295-299`):
> "Name the axis by the surface the round changes, not by the number it produces (kaidoku r29). Re-scoring a rule the lane already holds on new inputs, or counting rows a sourceless fixture also counts, is quality work, never coverage or depth."

Furthermore, in `SCORECARD.md:2553` (Round 45 C1):
- Round 44 had shipped a vacuous figure ledger counter. Round 45 repaired this by creating a non-vacuous counter that checked revision sensitivity and rejected 3/3 witnesses.
- This repair of an unprovable/vacuous counter was classified on the **operability** axis ("C1 ledger gate stops being vacuous | operability"), *not* calibration.

If round 47 C1 were framed as: "Round 46's counter `count-repins.py` was unprovable, so we wrote `tools/mori-pin-check.py` to re-score the four round-45/46 pins", the closure verifier would rightly conclude:
1. The four round-45/46 pins were **already verified and admitted as calibration: improved** by the closure verifier in round 46 on independent re-measurement.
2. Building an honest, non-vacuous instrument is **operability** (runnable artifact) or **quality** (instrument conformance), not a new calibration move.
3. Simply running an improved tool over the previously repaired cells constitutes "re-scoring a rule the lane already holds on new inputs."

### 4.3 Why Round 47 C1 is Genuine Calibration
Round 47 C1 successfully escapes the re-scoring trap because the surface changed is **not** the four round-46 cells:
1. **Fresh Calibration Defect at `SKILL.md:912`**:
   - `SKILL.md:912` pinned `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`.
   - History shows this pin had been stale since commit `d72ac167` (round 41), when `tools/mori-sources-appendonly.py` grew from 15 to 22 test cases.
   - Neither round 44, 45, nor 46 caught this discrepancy.
2. **Empirical Before State**:
   - As measured in Section 2.3, the four round-46 cells (lines 184, 190, 191, 194) **already pass** `mori-pin-check.py` at entering revision `2d85e33...`.
   - The only reason `PIN_CHECK=unmet` at the entering revision is line 912 (`mismatches=1`).
3. **The Measured Surface is Self-Assessment Truth**:
   - `AXES.md:15` defines calibration: "Self-assessment quality: gaps named honestly, confidence graded, overreach caught — SHONEN.md/SCORECARD entries match observed repo state."
   - The surface changed is `SKILL.md:912`: bringing the lane's registered self-assessment into alignment with the real tool output (`pass=22 fail=0`).
   - `tools/mori-pin-check.py` is the *instrument*, not the claim surface. Even with the new tool committed at freeze `63eecf27`, C1 remains unmet until `SKILL.md:912` is corrected.
- **Verdict on (b)**: C1 does not repeat round 46's claim surface. It moves calibration by resolving an uncalibrated gate pin at line 912. However, the round report **must explicitly present line 912 as the primary calibration surface**, avoiding any framing that suggests C1 exists merely to re-score round 46's four pins.

---

## 5. Analysis (c): C2 Depth Framing vs AXES.md Definitions

### 5.1 Canonical AXES.md Definitions
- `AXES.md:11`:
  > `| **depth** | Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources | A reader can act on SKILL.md alone; no filler |`
- `AXES.md:12`:
  > `| **coverage** | Fraction of the domain's real surfaces the skill governs (repo paths, tools, edge classes) | PROVINCE.md lists every surface; none unexplored without reason |`
- `AXES.md:14`:
  > `| **freshness** | Drift detection — skill claims re-verified against live surfaces; stale items flagged or fixed | Each round LOG entry includes a re-verification result |`
- `AXES.md:21`:
  > `quality ↔ depth + freshness + operability; discernment ↔ calibration.`

### 5.2 Evaluation of C2's Depth Framing
1. **Verifiable Technical Detail**:
   - C2 replaces an erroneous, superficial assertion ("has exactly three named tracepoints" from staged entry `oom-tracing-tracepoints-r42.md:12-13`) with the complete, verifiable technical schema of the Linux v7.2 kernel:
     - All 8 `TRACE_EVENT` declarations in `include/trace/events/oom.h`: `oom_score_adj_update`, `reclaim_retry_zone`, `mark_victim`, `wake_reaper`, `start_task_reaping`, `finish_task_reaping`, `skip_task_reaping`, `compact_retry`.
     - The exact `TP_STRUCT__entry` field set for each event (e.g. `mark_victim`'s 9 fields: `pid`, `comm`, `total_vm`, `anon_rss`, `file_rss`, `shmem_rss`, `uid`, `pgtables`, `oom_score_adj`).
     - The emitting call sites across kernel subsystems (`mm/oom_kill.c`, `mm/page_alloc.c`, `fs/proc/base.c`).
2. **Cited Sources**:
   - Sourced through new row S475 in `corpus/SOURCES.md`, an admitted mined tier-A code row naming Linux v7.2 `include/trace/events/oom.h`, verified against frozen sha256 digests (`PINS`).
3. **Exclusion of Other Axes**:
   - **Not coverage**: `PROVINCE.md:56` already lists FR13 (eBPF kill/OOM tracing) as a governed frontier area ("retain this as knowledge/frontier only"). C2 does not expand the fraction of domain surfaces governed; no resident tracer is added to core or the census.
   - **Not freshness**: Freshness requires re-verification against *live surfaces* (`AXES.md:14`). C2 does not probe a live host kernel or tracefs; it audits committed Linux v7.2 source code.
4. **Nuance and Alignment with "Decision Tables"**:
   - `AXES.md:11` specifies "decision tables with real thresholds, named error signatures".
   - C2's catalogue table (`| tracepoint | fields | emitted in |`) is an architectural schema catalogue rather than an operational threshold decision table.
   - However, in mori's domain, this catalogue establishes an indispensable **architectural decision ceiling**:
     - It proves that `mark_victim` carries victim process memory, comm, and uid, but **no cgroup path** and **no culprit task**.
     - An observer examining only kernel OOM tracepoints *cannot* attribute container culpability or fleet seat origin from the kernel record alone.
     - This directly reinforces mori's province boundaries: kill attribution must rely on journald and cgroup accounting (`PROVINCE.md:44, 53`), not resident kernel tracing.
   - Precedent: Non-author verifier closures in round 44 (C3 pid-probe, `round-44-verifier-spotcheck.md:18`) and round 45 (C3 cgroup levels, `round-45-verifier-spotcheck.md:48`) explicitly ruled knowledge entries defining kernel boundary details as `depth`.
- **Verdict on (c)**: C2's depth framing strictly adheres to `AXES.md:11` and established lane precedent.

---

## 6. UFO-FSD Connector Move (Bounded Proposal)

### 6.1 Evidence
1. In round 45, the lane registered wave-44 counters (`count-c1.py`, `count-c2.py`, `count-c3.py`) into `SKILL.md` tables. When those counters were updated, four registry cells became stale (`SKILL.md:184, 190, 191, 194`), resulting in a non-author verdict of `calibration: harmed` (`round-45-verifier-spotcheck.md:50-68`).
2. In round 47, working-tree draft `SKILL.md` introduces line 926:
   `| r47 tracepoint catalogue (C2) | gate | python3 .ufo/waves/round-47/count-c2.py ... | ... | python3 .ufo/waves/round-47/count-c2.py --selftest -> C2_SELFTEST pass=13 fail=0 | ...`
3. As demonstrated in Section 2.5, `tools/mori-pin-check.py` dynamically parses every `self-test` cell. Registering `count-c2.py` in `SKILL.md` couples C1's execution to an ephemeral wave counter, creating a false failure at baseline revs and breaking causal separability if C2 is reverted.
4. `contract.md:82` explicitly defines C2's surface: "C2 touches only the FR13 knowledge entry, its SOURCES rows and `corpus/evidence/sources-r47/`." Registering C2 in `SKILL.md` is an uncontracted cross-claim mutation.

### 6.2 Proposed Move
**Do not register `.ufo/waves/round-47/count-c2.py` in `SKILL.md`. Register only `tools/mori-pin-check.py` as a permanent gate in `SKILL.md:925`, and omit line 926 entirely.**

### 6.3 Affected Axes
- **Calibration (improved / protected)**: Eliminates the coupling between C1 and C2. Prevents the recurrence of round 45's stale-cell registry harm when round 47 closes. Ensures `mori-pin-check.py` measures permanent lane tools rather than ephemeral wave scripts.
- **Operability (preserved)**: `tools/mori-pin-check.py` is established as a permanent, registered lane gate with 22 passing selftest cases. `count-c2.py` remains fully operable as the wave's counting instrument without polluting the permanent gate registry.
- **Depth (preserved)**: C2 remains cleanly focused on FR13 technical detail, S475, and kernel evidence without out-of-scope metadata edits.

### 6.4 Risks and Tradeoffs
- *Risk*: Does omitting `count-c2.py` from `SKILL.md` violate any gate requirement?
  *Mitigation*: No. In mori, wave counters (`.ufo/waves/round-N/count-c*.py`) are wave-specific measurement instruments executed by the wave harness and closure verifiers. They are not permanent repo gates. Only reusable tools placed under `tools/` belong in `SKILL.md`.

### 6.5 Verification Procedure
1. Verify C1 in isolation:
   ```bash
   python3 tools/mori-pin-check.py --rev <landed-tip> --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
   ```
   Confirm `PIN_CHECK=met mismatches=0 dropped=0` with exactly 27 tally pins (26 baseline + 1 for `mori-pin-check.py` at line 925).
2. Test causal separability via revert:
   In a scratch branch, revert C2's commits (`corpus/knowledge/oom-tracepoints-r47.md`, S475 in `corpus/SOURCES.md`, and `corpus/evidence/sources-r47/`). Re-run the C1 command above; confirm `PIN_CHECK=met` still passes.
3. Verify C2:
   ```bash
   python3 .ufo/waves/round-47/count-c2.py <landed-tip>
   ```
   Confirm `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok`.

---

## 7. Tooling & Environment Authorization Disclosure

Per operator tooling directive (2026-10-19) and RULES.md:
- **Tools installed or updated**: None. All checks were executed using host-native `python3` (v3.13), `git`, `bash`, and standard POSIX coreutils.
- **Pacman guard**: Pacman was not invoked; host-wide pacman pause respected.
- **Scratch isolation**: All temporary runs and selftest executions used isolated directory `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ConnCrossClaim/`.
- **Substrate safety**: Read-only git operations only (`git rev-parse`, `git show`, `git diff`, `git log`, `git status`). No mutating git or jj commands run. No production files edited.

Report: `.ufo/waves/round-47/w1/ConnCrossClaim.md`
