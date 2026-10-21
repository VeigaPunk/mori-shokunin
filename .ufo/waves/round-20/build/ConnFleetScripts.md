# ConnFleetScripts — Overlap Scan with Fleet Tooling (C2 Wave Settlement)

**Seat:** `MoriR20.ConnFleetScripts` (UFO-FSD connector; leaf seat, read-only on fleet and lane trees, no subagent dispatch).  
**Target:** Overlap scan between fleet tooling (`scripts/hyaku/wave-live.py`, `status.sh`, `wave-slot.sh`, `inline.sh`) and Round 20 C2 per-seat wave settlement in `mori-shokunin/.ufo/waves/round-20/contract.md`.  
**Date:** 2026-10-21.

---

## 1. Executive Finding

**Does any fleet script already count per-seat report settlement?**  
**NO.** None of the four scripts (`wave-live.py`, `status.sh`, `wave-slot.sh`, `inline.sh`) counts, parses, or tracks per-seat wave report settlement.

- `wave-live.py` estimates *active agent process count* in an active OMP session transcript directory (`SESSION_DIR`) for concurrency gating; it does not inspect lane repositories, dispatch manifests, or wave reports.
- `status.sh` displays orchestrator-level campaign rounds, in-flight L1 claims, and event logs.
- `wave-slot.sh` manages *admission gating* and seat reservation prior to dispatch against a 200-seat global target and RAM limits; it is unconcerned with post-execution wave artifacts.
- `inline.sh` drives mechanical steps for L1 lane rounds; its `verify` step inspects only the *single L1 lane-level round report* (`.ufo/reports/round-$n/$lane.md`), leaving the settlement of subagent swarm waves completely unobserved.

---

## 2. Detailed Semantic Comparison: Fleet Scripts vs. C2 Contract

### A. `scripts/hyaku/wave-live.py` vs. C2 (`contract.md:49-88`)

| Dimension | `scripts/hyaku/wave-live.py` | C2 `tools/mori-wave-settlement.py` |
| :--- | :--- | :--- |
| **Primary Purpose** | Estimate runtime concurrency of active subagents (`wave-live.py:1-3,19`) | Observe post-execution settlement of dispatched swarm wave reports (`contract.md:49-55`) |
| **Target Directory** | OMP session transcript dir (`SESSION_DIR`, `wave-live.py:4,180-185`) | Lane repository root (`<lane-root>`, `contract.md:60,64`) |
| **Input Files Inspected** | Transcript event logs (`*.jsonl`, `wave-live.py:162`) | Dispatch manifests (`.ufo/waves/*.json` with `schema: ufo-swarm-wave-dispatch-v1`, `contract.md:64-67`) |
| **Artifact Evaluated** | Sibling `<agent_id>.md` in session directory (`wave-live.py:75`) | Scoped report paths from task trailer (`.ufo/waves/round-X/build/<Name>.md`, `contract.md:70-76`) |
| **Report Status Logic** | `stat.S_ISREG` and `size > 0` and `st_mtime > when` (`wave-live.py:78-79`) | `present` (`S_ISREG` and `size > 0`), `empty` (`size == 0`), `missing`, `unsafe`, `unparsed`, `misrooted` (`contract.md:74-76`) |
| **Symlink Handling** | Refuses directory and file symlinks (`O_NOFOLLOW`, `follow_symlinks=False`, `wave-live.py:29-30,34,75,166`) | Refuses directory and file symlinks (`follow_symlinks=False`, `not_followed: true`, `contract.md:67,74`) |
| **Report Content Emission** | Never executes or prints transcript bodies (`wave-live.py:11-12`) | Never emits report bytes; only status and counts (`contract.md:77,19`) |
| **Output Data Shape** | Emits a single decimal integer (`wave-live.py:193`) | Emits structured JSON (`schema: mori-wave-settlement-v1`) with wave states and missing seat lists (`contract.md:82-86`) |
| **Exit Code Protocol** | `0` = success (integer printed), `2` = usage/inspection failure (`wave-live.py:183,192,194`) | `0` = all waves `settled` or `no-spawn`, `1` = any other state (`partial`, `unsettled`, `unavailable`), `2` = usage/unreadable root (`contract.md:87-88`) |

#### Agreements:
1. **Zero Content Emission:** Both utilities strictly prohibit outputting or echoing report/transcript contents (`wave-live.py:11-12`; `contract.md:77,19`).
2. **Symlink Safety:** Both explicitly decline following filesystem symlinks (`wave-live.py:18,29-30,75,166`; `contract.md:67,74`).
3. **Empty File Distinction:** Both differentiate between 0-byte files and regular files with positive size (`wave-live.py:78`; `contract.md:74`).
4. **Vocabulary Discipline:** Neither utility conflates a missing or inactive artifact with terminal agent failure or termination (`wave-live.py:19` "This is a snapshot estimate, not a scheduler/process liveness oracle"; `contract.md:80-81` "A missing report is NOT a dead seat: the output never says `dead`, `failed` or `killed`").

#### Differences:
1. **Inspection Substrate & Timing:** `wave-live.py` requires an active OMP runtime session directory containing live `.jsonl` streams; it is useless for offline, committed, or historical wave evaluation (`contract.md:52-54,95-97`).
2. **Trailer & Prompt Parsing:** `wave-live.py` has no parser for `ufo-swarm-wave-dispatch-v1` files, `taskCall.tasks[*]`, or regex trailers (`contract.md:68-73`).
3. **Misrooting Detection:** C2 detects when seat reports are accidentally written under `--fleet-root` rather than `<lane-root>` (`misrooted`, `contract.md:75-76`), an issue `wave-live.py` does not address.

---

### B. `scripts/hyaku/status.sh` vs. C2 (`contract.md:49-88`)

- **Role:** `status.sh:2-17` inspects `$STATE/claims/*/`, `$STATE/blocked/`, `$STATE/events.log`, and `$H/pool.txt` to display the status of L1 lane rounds in a Hyaku campaign.
- **Overlap:** Zero. `status.sh` operates entirely at the multi-lane campaign level and has no visibility into intra-round swarm waves, subagent dispatches, or seat reports.

---

### C. `scripts/hyaku/wave-slot.sh` vs. C2 (`contract.md:49-88`)

- **Role:** `wave-slot.sh:2-17` acts as a concurrency admission gate (`acquire`, `release`, `status`). It reserves seat allocations in `$STATE/wave-slots` (`wave-slot.sh:22,81`) based on `live()` estimates from `wave-live.py` (`wave-slot.sh:61-66`), pending reservations (`wave-slot.sh:67`), and host memory availability (`wave-slot.sh:68,80`).
- **Agreements:** Both tools recognize swarm waves as bounded groups of seats.
- **Differences:**
  - *Phase:* `wave-slot.sh` is an *admission gate* executed *before* dispatch to throttle load. C2 is an *observability tool* executed *after* dispatch to verify artifact settlement.
  - *State & Locking:* `wave-slot.sh` mutates host state (`$STATE/wave-slots`) and holds a POSIX advisory flock (`wave-slot.sh:76,93`). C2 is stateless, read-only, and side-effect-free (`contract.md:56-57`).
  - *Seat Representation:* In `wave-slot.sh:72-73`, a seat is a fungible integer count (`seats`). In C2 (`contract.md:68-74`), a seat is a specific named task entity (`taskCall.tasks[*]`) with an expected report path and individual settlement lifecycle.

---

### D. `scripts/hyaku/inline.sh` vs. C2 (`contract.md:49-88`)

- **Role:** `inline.sh:2-15` automates the lifecycle of in-session L1 rounds (`queue`, `dispatch`, `verify`, `fail`, `closure`, `advance`).
- **Inspection in `verify`:** In `inline.sh:107-133`, `verify` calls `report_of "$lane" "$n"` (defined in `scripts/shokunin-watchdog.sh:140-147`).
  - `report_of` checks only the *single L1 lane-level round report*: `.ufo/reports/round-$n/$lane.md`.
  - It checks whether this L1 report contains a `SHONEN` heading and exceeds `MIN_REPORT_BYTES` (`shokunin-watchdog.sh:140-144`), then sweeps and commits it if left uncommitted (`inline.sh:111-116`).
- **Differences:**
  - `inline.sh` does NOT inspect intra-round swarm waves. It has zero code reading `<lane-root>/.ufo/waves/` or verifying subagent seat reports (`.ufo/waves/round-X/build/<Name>.md`).
  - `inline.sh` inspects report *content* (`SHONEN` heading, size threshold); C2 explicitly *forbids* reading or emitting report content (`contract.md:77`).
  - `inline.sh` is an operational driver with write/commit/push side effects; C2 is strictly read-only.

---

## 3. Recommendation: Reuse vs. Separate

### Recommendation: **Strictly Separate Implementation, Unidirectional Downstream Consumption**

1. **Reject Internal Reuse:** `tools/mori-wave-settlement.py` must NOT import, wrap, or depend on `wave-live.py`, `wave-slot.sh`, or `inline.sh`.
   - *Province Integrity:* Mori's province (`PROVINCE.md:6-16`) mandates read-only observability, detection, and reporting, while rejecting orchestration mechanism. Fleet scripts belong to the execution/orchestrator domain.
   - *Runtime Decoupling:* Fleet scripts depend on transient host state (`$HYAKU_STATE`, `HYAKU_SESSION_DIR`, active OMP JSONL transcripts). C2 must run deterministically in any offline environment, on static git checkouts, and across synthetic fixtures (`frozen/c2-expected.json`).
   - *Language & Stdlib Bound:* C2 is constrained to stdlib Python 3 with no external dependencies (`contract.md:56`).

2. **Substrate Pattern Borrowing (No-Harm Synthesis):**
   While code reuse is rejected, C2 should adopt the exact POSIX filesystem safety mechanics validated in `wave-live.py:29-30,75,166`:
   - Use `os.lstat()` or `os.stat(..., follow_symlinks=False)` to verify that candidate reports are genuine regular files (`stat.S_ISREG`) and not symlinks, satisfying oracle case `symlink-report` (`frozen/c2-expected.json:16`).
   - Reject paths containing `..` components lexically before resolution, preventing path traversal escapes (`frozen/c2-expected.json:14`).

3. **Future Fleet Consumption (The Bridge):**
   Fleet tooling (`inline.sh verify`) currently has a major blind spot: it verifies that an L1 produced a round report, but cannot detect when an L1 fails to collect subagent seat reports (the exact failure mode of Round 19 Wave 1, where 48 of 64 seat reports were missing, `contract.md:51-54`).
   Because `tools/mori-wave-settlement.py` adheres to standard exit codes (`0` for `settled` / `no-spawn`, `1` for `partial` / `unsettled` / `unavailable`, `contract.md:87-88`), `inline.sh verify` can in future rounds invoke `tools/mori-wave-settlement.py scan --lane-root "$cwd"` as a passive health check without altering Mori's boundaries.

---

## 4. UFO-FSD Connector Synthesis: Non-Obvious Move

### A. Evidence
- In Round 19 Wave 1, the L1 round was marked landed because `.ufo/reports/round-19/mori.md` existed, despite 48 out of 64 dispatched subagents failing to settle their reports (`contract.md:51-54`; `inline.sh:109-110`).
- Fleet tooling (`wave-live.py:66-80`) checks `<agent_id>.md` mtimes against transcript timestamps, but this is only usable while the OMP session directory is live on the host. Once the session terminates, all wave-settlement visibility vanishes from fleet tooling.
- C2 specifies a clean, self-contained CLI contract: `mori-wave-settlement.py scan --lane-root DIR [--fleet-root DIR] [--out FILE]` exiting `0` on `settled`/`no-spawn` and `1` on any unsettled state (`contract.md:59-62,87-88`).

### B. Affected Axes
- **Coverage (C2):** Directly advances FR3 wave-settlement observability from zero to complete seat-level accounting.
- **Operability:** Eliminates the blind spot where rounds advance despite missing worker reports, without burdening operators with manual recovery.
- **Boundary Clarity / Independence:** Prevents improper coupling between Mori's measurement tooling and Hyaku's runtime session state.

### C. Proposed Move
**Retain `tools/mori-wave-settlement.py` as an autonomous, self-contained stdlib Python 3 tool inside Mori, while standardizing its CLI interface and exit semantics (`0` = all settled/no-spawn, `1` = unsettled/partial/unavailable) so that Hyaku fleet tooling (`inline.sh verify`) can consume it as an optional downstream read-only gate.**
- Do not add fleet imports to Mori.
- Do not let C2 access `$HYAKU_STATE` or `SESSION_DIR`.
- Incorporate `follow_symlinks=False` / `stat.S_ISREG` checks directly into C2's implementation to fulfill `c2-expected.json` without depending on `wave-live.py`.

### D. Risks & Second-Order Effects
- *Risk: False Coupling:* If an implementer attempts to import `wave-live.py` functions, C2 will fail in environments without active OMP session directories. *Mitigation:* C2 must remain 100% self-contained in `tools/mori-wave-settlement.py`.
- *Risk: Vocabulary Leakage:* Conflating "missing report" with "dead agent" violates the C2 contract (`contract.md:80-81`). *Mitigation:* Ensure C2 emits strictly the closed status set (`present`, `empty`, `missing`, `unsafe`, `unparsed`, `misrooted`) and wave states (`settled`, `partial`, `unsettled`, `no-spawn`, `unavailable`), excluding `dead`, `failed`, or `killed`.

### E. Verification
- Contract alignment verified against `mori-shokunin/.ufo/waves/round-20/contract.md:49-110`.
- Oracle alignment verified against `mori-shokunin/.ufo/waves/round-20/frozen/c2-expected.json` (all 14 test cases).
- Code paths inspected in `/home/vgpnk/Projects/shokunin/scripts/hyaku/`:
  - `wave-live.py:1-198`
  - `status.sh:1-17`
  - `wave-slot.sh:1-105`
  - `inline.sh:1-173`
  - `shokunin-watchdog.sh:139-147`
- No host or lane modifications were executed; all inspections were read-only. No pacman commands or tooling installations were attempted.
