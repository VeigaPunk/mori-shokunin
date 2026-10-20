# Frontier Connection: Mapping FR1 Partial Advance & Precision Boundary Updates

**Seat:** `MoriR13.FrontierConnection`  
**Role:** UFO-FSD Connector  
**Axes Named:** Coverage (C1), Operability (C2)  
**Milestone:** Round 13 Structured Scopes & Verdict Integrity  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Date:** 2026-10-20  

---

## 1. Godspeed Posture & Named Axes

In accordance with `/skill:godspeed`:
1. **Name the axes:**
   - **Coverage (C1):** Journal observability moves from fragile, un-scoped raw `MESSAGE` regex scraping (`c_oom`, `c_kill`, `c_seg`, `c_unit` text grep) to structured, 128-bit `MESSAGE_ID` catalog matching (`fe6faa94e7774663a0da52717891d8ef`, `d989611b15e44c9dbf31e3c81256e4ed`, `fc2e22bc6ee647b6b90729ab34a250b1`) across explicitly separated `user` and `system` journal scopes, strictly suppressing `MESSAGE` text output via `-o json --output-fields=_BOOT_ID`.
   - **Operability (C2):** Preserving honest verdict grammar, exit code parity, and zero pipeline failures. Specifically repairing long-history SIGPIPE authorship loss (defect F01 / QUALITY 7) and eliminating invalid/forged verdicts in the silence oracle (defect F02 / QUALITY 26).
2. **Iterate cheap, in parallel:** Synthesizing local repository evidence, primary sources (S003, S004, S013, S014, S015, S031), sibling reports (`JournalSource.md`, `CatalogSource.md`, `PipeSource.md`), and historical audits (`audit-r11.md`, `kernel-oom-line-attribution-r12.md`, `kill-classes-by-message-id-r12.md`).
3. **Keep moves that improve any axis and harm none:** Advancing structured system-journal notice observation without pretending kernel OOM victim attribution or fleet causality are solved.
4. **Don't aim — let the frontier walk itself:** Truthfully separating what Round 13 settles (structured system/user unit notice counts) from what remains on the frontier (event-time kernel OOM attribution, `task_memcg` token extraction, and fleet task correlation).

---

## 2. Non-Obvious Move: The Synthesis Across Round 13 Proposals

### The Tension in Round 13 Proposals
In Round 13, two competing temptations emerged across executor, critic, and reviewer seats:
- **Temptation A (Overclaiming / "FR1 Core"):** Declaring that adding a system-journal notice probe fully settles FR1 ("System-journal kill/segfault scope, kernel OOM attribution, and fleet correlation") into core territory.
- **Temptation B (Semantic Regression / Breaking Operability):** Replacing all user-journal signals with an empty JSON query stub or conflating `fe6faa94…` unit notices with actual kernel victim kills, creating a false equivalence between systemd unit notifications and kernel process terminations.

### The Compatible Synthesis
The non-obvious move is **explicit frontier decomposition**:
1. **Partition FR1 into an Admitted Sub-Scope (FR1a) and an Unresolved Residual (FR1b/c):**
   - **Settled into Core (FR1a):** Structured system-journal notice counting (`fe6faa94…`, `d989611b…`, `fc2e22bc…`) in an independent `SURFACE journal_system` (or dual-scope `SURFACE journal`), eliminating raw text scraping and honoring QUALITY criteria 15 and 16.
   - **Retained on Frontier (FR1b):** Event-time kernel OOM victim attribution (`oom-kill:constraint=...`, `task_memcg=...`, PID, UID from `mm/oom_kill.c:447-453` and `memcontrol.c:1820-1826`). This requires strict token-shape validation without echoing `MESSAGE`, which the Round 13 notice probe does *not* implement.
   - **Retained on Frontier (FR1c):** Fleet-task correlation. A host kernel or systemd notice alone never proves a fleet-caused kill (PROVINCE boundary).
2. **Second-Order Effects Across Surfaces:**
   - **Runtime surface:** `tools/mori-census.sh` gains robust, isolated user and system probes that exit `unavailable` on `rc != 0` (e.g. permission denied) rather than emitting false `0`s (QUALITY 6).
   - **Contract surface:** `PROVINCE.md` and `README.md` retain their hard boundary—refusing OS-state remediation and distinguishing unit notices from victim kills.
   - **Verification surface:** Baseline drift masks (`tools/mori-census.sh:DRIFT_COUNTER_KEYS`) must explicitly mask new structured counter keys to preserve drift-pin verification across baseline comparisons without masking structural drifts.

---

## 3. Grounded Evidence: What Advances vs What Remains

### 3.1 What Has Advanced in Round 13 (Settled into Core)
- **Primary Sources Anchored:**
  - `S013` (`systemd.catalog.in:66,604,884` commit `cf8ebfc6`): Defines 128-bit catalog IDs for core dumps (`fc2e22bc…`), kernel OOM unit notices (`fe6faa94…`), and systemd-oomd kills (`d989611b…`).
  - `S014` (`journalctl(1)` systemd 262): Anchor `#--output-fields=` guarantees that `--output-fields=_BOOT_ID` suppresses `MESSAGE` text while automatically including `_BOOT_ID`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, and `__CURSOR`.
  - `S015` (`systemd.journal-fields(7):34-46`): Verifies `MESSAGE` is free-text unparsed payload, whereas `MESSAGE_ID` is the machine-typed 128-bit key.
- **Scope Independence Proved (QUALITY 16):**
  - Host empirical measurement (`corpus/knowledge/kill-classes-by-message-id-r12.md:15-16`): Boot `7bd93aee71144017b870212161a3dabf` holds `7` user notices and `9` system notices for `fe6faa94…`.
  - Scopes are independently queried and never summed ($7 + 9 \neq 16$ victims).
- **Safe Pipeline Execution (QUALITY 7 & S031):**
  - S031 (`pipe(7)`) demonstrates that early-exiting readers cause producer `SIGPIPE` (141) under `pipefail`. Capturing output once into shell buffers or here-strings eliminates F01.

### 3.2 What Remains on the Frontier (Cannot Be Absorbed into Core)
1. **Kernel OOM Victim Line Attribution:**
   - Linux kernel 7.2 source `mm/oom_kill.c:447-453` (`dump_oom_victim`) and `memcontrol.c:1820-1826` (`mem_cgroup_print_oom_context`) emit:
     `oom-kill:constraint=...,task=%s,pid=%d,uid=%d`
     `...,task_memcg=...,oom_memcg=...`
   - These are kernel log messages (`_TRANSPORT=kernel`), not catalog `MESSAGE_ID` notices.
   - Reading these fields requires token shape-validation (decimal PID/UID, sanitized cgroup path) to satisfy the "never echo raw `MESSAGE`" constraint.
   - The Round 13 structured probe reads catalog `MESSAGE_ID`s only; it does not parse or extract kernel victim tokens.
2. **Cardinality Disconnect (Notice $\neq$ Victim):**
   - In boot `7bd93aee71144017b870212161a3dabf`, there were exactly `5` kernel `Killed process` records, yet `7` user notices and `9` system notices.
   - A unit notice indicates that systemd observed a kill affecting a unit; it is subject to multi-unit fan-out (parent slices, root scopes). It is not a 1:1 process kill count.
3. **Fleet Causal Attribution:**
   - S013 catalog explicitly cautions: *"Note that the memory pressure might or might not have been caused by @UNIT@"*.
   - A host-level event does not prove that a specific shokunin fleet agent or wave caused the OOM.
   - Correlating host events with fleet task execution requires event-time `task_memcg` / slice matching against active watchdog and wave registers. Re-reading cgroups post-mortem fails (`ENOENT`, QUALITY 18).

---

## 4. Affected Axes

| Axis | Pre-Round 13 State | Post-Round 13 State | Frontier vs Core Distinction |
|:---|:---|:---|:---|
| **Coverage (C1)** | User journal text regexes (`grep -ciE 'Out of memory'`); zero system journal coverage; unreadable journalctl masked or unhandled. | Dual-scope (`user` and `system`) structured catalog `MESSAGE_ID` matching (`fe6faa94…`, `d989611b…`, `fc2e22bc…`) with `--output-fields=_BOOT_ID`. | **Core:** Structured unit notices in user and system scopes.<br>**Frontier:** Event-time kernel OOM victim attribution (`task_memcg`, PID/UID) and fleet correlation. |
| **Operability (C2)** | F01: Long history triggers SIGPIPE 141 in `sed`, causing authorship loss.<br>F02: Oracle accepts BANANA verdict prefix without checking final roll and rc parity. | F01 repaired via here-string / single-pass capture (no live pipe to early-exit grep).<br>F02 repaired via strict `verdict_grade` checking roll grammar and rc 0/1 agreement. | Fully settled into Core operability. |

---

## 5. Precise Recommendations for `PROVINCE.md` & `README.md`

To preserve truthfulness and prevent premature closure of FR1, updates to `PROVINCE.md` and `README.md` must be bounded and surgical:

### 5.1 Updates to `PROVINCE.md`

#### A. Under `## Core` (Section line 24):
**Current text:**
```markdown
- **Kill/OOM classes** — `SURFACE journal` and `SURFACE cgroup`: user-journal OOM/kill/segfault/unit-failure counts plus cgroup memory-event counters; these are scoped counts, not victim, event-time, or fleet-cause attribution.
```
**Recommended update:**
```markdown
- **Kill/OOM classes** — `SURFACE journal`: structured MESSAGE-free `MESSAGE_ID` unit notice and coredump counts across independently labeled `user` and `system` journal scopes (catalog IDs `fe6faa94…`, `d989611b…`, `fc2e22bc…`); `SURFACE cgroup`: cgroup memory-event counters. These are scoped notice counts only, not victim, event-time, or fleet-cause attribution.
```

#### B. Under `## Frontier` (Section lines 31):
**Current text:**
```markdown
- **FR1 — System-journal kill/segfault scope, kernel OOM attribution, and fleet correlation** (state F1/F8 + art F2). First evidence: `corpus/knowledge/kernel-oom-line-attribution-r12.md:10-16`; `corpus/knowledge/kill-classes-by-message-id-r12.md:10-16`; `corpus/knowledge/audit-r11.md:203-204`. Boundary: system-journal coverage is not the current user-journal probe; never echo `MESSAGE`, and a host event alone does not prove a fleet-caused kill.
```
**Recommended update:**
```markdown
- **FR1 — Kernel OOM event-time attribution and fleet correlation** (state F1/F8 + art F2). First evidence: `corpus/knowledge/kernel-oom-line-attribution-r12.md:10-16`; `corpus/knowledge/audit-r11.md:203-204`. Progress in round 13: system-journal structured unit notice counts advanced to Core (`SURFACE journal` system scope). Boundary remaining on Frontier: parsing event-time kernel OOM summary and victim lines (`task_memcg`, PID, UID) requires strict token-shape validation without echoing `MESSAGE`; a host event alone does not prove a fleet-caused kill, and post-event cgroup lookup cannot restore deleted victim paths.
```

### 5.2 Updates to `corpus/README.md` (Frontier Table line 285)
**Current text:**
```markdown
| FR1 | System-journal kill/segfault scope, kernel OOM attribution, and fleet correlation | `knowledge/kernel-oom-line-attribution-r12.md:10-16`; `knowledge/kill-classes-by-message-id-r12.md:10-16`; `knowledge/audit-r11.md:203-204` | System-journal coverage is not the current user-journal probe; never echo `MESSAGE`; a host event alone does not prove a fleet-caused kill. |
```
**Recommended update:**
```markdown
| FR1 | Kernel OOM event-time attribution and fleet correlation | `knowledge/kernel-oom-line-attribution-r12.md:10-16`; `knowledge/audit-r11.md:203-204` | System-journal unit notices settled round 13; event-time kernel attribution (`task_memcg`, PID/UID token validation without `MESSAGE`) and fleet task correlation remain on frontier. |
```

### 5.3 Updates to Root `README.md`
Root `README.md` is a high-level overview. Ensure line 6 ("Domain") retains its strict non-remediation and refusal boundaries:
```markdown
**Domain:** "Fleet & host observability (森) — detect and report fleet liveness, wave settlement, kill/OOM events and resource runway. Triggers: 'fleet health', 'did a wave die', 'why did the daemon vanish', 'watchdog liveness', 'OOM kill'. Anti-trigger: NOT dispatch/orchestration (kumitate), NOT OS package/systemd/driver state (tsukuroi), NOT endpoint health (kama)"
```
No change to root `README.md` domain scope is required, confirming that mori reports observability evidence only and never remediates or absorbs host OS administration.

---

## 6. Risks & Verification Surfaces

### 6.1 Risks Identified
1. **Conflation of Notice with Victim (Category Error):**
   If downstream agents treat `fe6faa94…` count as "processes killed", they will misestimate kill counts by 140% to 180% due to unit hierarchy fan-out (7 user notices and 9 system notices vs 5 kernel victims).
   *Mitigation:* Explicit labeling in census output (`notice_user=... notice_system=...` or `scope=user scope=system`), with documentation citing QUALITY 16.
2. **Permission Denial Masking:**
   When running as an unprivileged user without `systemd-journal` or `adm` group membership, `journalctl --system` fails with exit code `1`.
   *Mitigation:* In accordance with S014 and QUALITY 6, the probe must emit `SURFACE journal unavailable "cmd=...; rc=1; permission denied"` rather than reporting `0` notices.
3. **Drift Baseline False Red:**
   Adding new counter keys to census output will trip baseline comparison `--drift` unless those keys are either normalized in the baseline or added to `DRIFT_COUNTER_KEYS` / volatile field exclusions.
   *Mitigation:* Coordinate with `DriftScope` and `CensusFix` to include new structured keys in counter masks.

### 6.2 Proposed Checks for L1 Integrator (No Mid-Flight Verification Executed)
The leaf connector does not run tests. The L1 integrator should verify this synthesis using:

```bash
# 1. Verify structured system notice probe emits unavailable on permission failure (unreadable canary)
MORI_JOURNALCTL_BIN="/bin/false" tools/mori-census.sh verify 2>&1 | grep -q 'SURFACE journal.*unavailable'

# 2. Verify MESSAGE suppression: journalctl command template emits zero MESSAGE lines
journalctl --system -q -b 0 MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID | grep -F '"MESSAGE"' | wc -l
# Expected: 0

# 3. Verify long-history authorship pipeline does not trigger SIGPIPE 141
# (Tested by CensusFix / RegressionHarness long-history test fixture)

# 4. Verify silence oracle rejects invalid BANANA verdict roll
tools/mori-silence-cases.sh verify
# Expected: 28/28 passing, with BANANA mutant cleanly rejected
```

---

## 7. Tooling Record
- **Tools installed/updated:** None. Inspection was conducted using existing repository files, internal URLs, and primary sources.
