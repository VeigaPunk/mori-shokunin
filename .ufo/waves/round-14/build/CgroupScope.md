# CgroupScope — Round 14 Scoped Findings

**Seat:** `MoriR14.CgroupScope` (scout, leaf member)  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Report Target:** `.ufo/waves/round-14/build/CgroupScope.md`  
**Judged Axis:** `coverage` (primary); impacted: `adjacency`, `operability`, `calibration`  
**Milestone:** restore OOM alarm and structured fleet routing  
**Contract Constraints:** Leaf member — no subagent dispatch; source-only inspection; no build, test, lint, format, smoke or live check execution; no tool installs/updates. All runtime behaviors are deduced from upstream source and documentation authority without live verification.

---

## 1. Executive Summary & Named Axes

1. **Named Axes:**
   - **coverage (primary judged axis):** Round 13 attempted a cutover from MESSAGE-grepped journal text to structured catalog-ID queries (`C1`). However, demoting the kernel-OOM journal notice (`fe6faa94...`) to `info` and eliminating `OOM_KILL_JOURNAL crit` under the assumption that the cgroup surface (`CGROUP_OOM_KILL`) provided replacement coverage was judged a harmful regression. Closure reviewer Hyaku rejected Round 13 as `rejected-harmed` (`corpus/lessons/round-13-verifier-spotcheck.md:72-89`). Restoring genuine coverage requires establishing the precise boundary between cgroup instance scalar counters and journal event notifications.
   - **adjacency:** Preserving the division between fleet unit health (`mori`) and host/desktop OS triage (`tsukuroi`, `PROVINCE.md:12-16`). Cgroup cumulative counters at ancestor slices conflate fleet kills with desktop kills.
   - **operability & calibration:** Accurate finding severities (`crit` flipping `DRIFT` vs `info`), eliminating misleading variable names and dead fallback branches, and avoiding false equivalence between disjoint observation planes.

2. **Core Findings (Source-Only Deduced, No Live Verification):**
   - **Selection Dynamics in Census:** In `tools/mori-census.sh:1157-1164`, the census probe derives `LOCAL_EVENTS` from `CGROUP_EVENTS` (`user-1000.slice/memory.events.local`) and evaluates `if [ -r "$LOCAL_EVENTS" ]`. On any cgroup instance where `.events.local` is present and readable, this branch succeeds unconditionally, so the fallback to `SERVICE_EVENTS` (`user@1000.service/memory.events`) is **not taken on that instance**. The fallback remains valid design when `.events.local` is absent or unreadable (e.g. unexposed accounting or older kernel mounts), but whenever `.local` exists and is readable, it bypasses the session service check.
   - **Descendant Exclusion by S002 Authority:** By definition in Linux cgroup v2 documentation (Source `S002`, `memory.events.local:1505-1509`), `memory.events.local` counts events occurring strictly in that specific cgroup node and **excludes all descendants**. In standard systemd cgroup v2 hierarchies with controller delegation enabled, slice nodes act as intermediate routers and processes run within leaf units (`user@1000.service`, `app-*.scope`, `session-*.scope`). While not claimed to be perpetually zero under all possible custom controller configurations, S002 guarantees that any OOM kill of a process in a descendant unit increments the leaf's local counter and ancestor hierarchical counters, but **does not increment the ancestor slice's `memory.events.local`**.
   - **Why Cgroup Cannot Replace Journal OOM Alarms:**
     1. *Descendant exclusion:* As governed by S002, `memory.events.local` cannot see kills in child cgroups.
     2. *Scope boundaries:* `user-1000.slice` has zero visibility into system services (`system.slice`), container runtimes, or other user slices (`user-0.slice`).
     3. *Instance lifecycle vs Event log:* Cgroup counter lifetime is tied to the cgroup instance. When a transient scope or service exits after an OOM kill, its cgroup directory is removed by systemd (`ENOENT`), destroying its local counter. The journal, however, retains durable, timestamped, boot-anchored structured records (`_BOOT_ID`, `MESSAGE_ID=fe6faa94...`).
     4. *Presence flag vs Event alarm:* At ancestor slices (`user-1000.slice/memory.events`), old kills persist across the slice's instance lifetime (which may span days or the whole boot). Firing `crit` on that cumulative counter forced permanent false drift, leading `mori` to grade it as `CGROUP_OOM_KILL_CUMULATIVE info`.
     5. *Decisive harm from lost coverage:* Demoting the journal notice to `info` left the local cgroup critical branch (`CGROUP_OOM_KILL crit`) technically present in code, not literally zero alarm paths registered. However, because local slice counters do not guarantee visibility into descendant services/scopes or out-of-scope system units, the critical cgroup path cannot substitute for the lost journal OOM alarm. That missing descendant and out-of-scope guarantee is itself decisive harm (`round-13-verifier-spotcheck.md:85`).
   - **Authority Ruling (Round 14 Gate):**
     `| Cgroup local counter substitutes for all journal OOM alarms | rejected | Selected memory.events.local excludes descendants and unrelated scopes; event planes are not equivalent. |` (`corpus/lessons/round-14.md:29`).

---

## 2. Census Cgroup Selection Code Inspection

### 2.1 Code Anchors in `tools/mori-census.sh`

In `tools/mori-census.sh`:

1. **Default Path Definitions (Lines 278, 1157–1159):**
   ```bash
   278: CGROUP_EVENTS=${MORI_CGROUP_EVENTS:-/sys/fs/cgroup/user.slice/user-$(id -u).slice/memory.events}
   ...
   1157: LOCAL_EVENTS=${MORI_CGROUP_LOCAL_EVENTS:-${CGROUP_EVENTS%.events}.events.local}
   1158: SERVICE_EVENTS=${MORI_CGROUP_SERVICE_EVENTS:-/sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/memory.events}
   ```
   - When running for UID 1000 without environment overrides:
     - `CGROUP_EVENTS` resolves to `/sys/fs/cgroup/user.slice/user-1000.slice/memory.events`.
     - `LOCAL_EVENTS` resolves to `/sys/fs/cgroup/user.slice/user-1000.slice/memory.events.local`.
     - `SERVICE_EVENTS` resolves to `/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.events`.

2. **Counter Selection Logic (Lines 1160–1165):**
   ```bash
   1160: service_oom_kill=''
   1161: if [ -r "$LOCAL_EVENTS" ]; then
   1162:   service_oom_kill=$(cgroup_field "$LOCAL_EVENTS" oom_kill)
   1163: elif [ -r "$SERVICE_EVENTS" ]; then
   1164:   service_oom_kill=$(cgroup_field "$SERVICE_EVENTS" oom_kill)
   1165: fi
   ```

3. **Finding Emission Logic (Lines 1294–1303):**
   ```bash
   1294: # presence flag semantics (tsukuroi note): oom_kill is a flag/counter, not a meter to clear
   1295: if [ -n "$service_oom_kill" ] && [ "$service_oom_kill" -gt 0 ] 2>/dev/null; then
   1296:   emit_finding CGROUP_OOM_KILL crit "local_oom_kill=$service_oom_kill path=${LOCAL_EVENTS} (local counter: kills in this cgroup only)"
   1297:   st=drift
   1298: elif [ "$oom_kill" -gt 0 ] 2>/dev/null; then
   1299:   emit_finding CGROUP_OOM_KILL_CUMULATIVE info "parent_slice_oom_kill=$oom_kill service_scope_oom_kill=${service_oom_kill:-unavailable} note=cumulative boot counter; attribute the event before treating it as fleet evidence"
   1300: fi
   ```

### 2.2 Operational Flaws Observed in the Selection Logic

1. **Fallback Not Taken When Local Readable:**
   When `/sys/fs/cgroup/user.slice/user-1000.slice/memory.events.local` is present and readable, `[ -r "$LOCAL_EVENTS" ]` evaluates to true, so the `elif [ -r "$SERVICE_EVENTS" ]` fallback branch is not taken on that instance. The fallback is not universally unreachable in the abstract (it remains reachable when `.local` is absent or unreadable), but whenever `.local` exists and is readable, it unconditionally takes precedence.
2. **Misleading Variable Naming:**
   The variable storing the result is named `service_oom_kill`. However, when reading `$LOCAL_EVENTS`, it holds the reading of `user-1000.slice/memory.events.local`, which is an **ancestor slice local counter**, NOT a service counter.
3. **Intent vs Implementation Contradiction:**
   The comment at lines 1150–1156 states:
   > *"The fleet-relevant reading is the session service. Prefer `memory.events.local` — it counts kills in THIS cgroup only, so it is immune to two traps the cumulative/ancestor reads hit: (1) propagation... and (2) a restart... A walk of 101 cgroups found no live cgroup with local oom_kill > 0."*
   
   The comment conflates reading `memory.events.local` at the slice level with reading the session service (`user@1000.service`). Reading `memory.events.local` at `user-1000.slice` does NOT observe `user@1000.service`; it observes ONLY processes directly attached to `user-1000.slice`.

---

## 3. Authority Analysis: S002 (Cgroup v2 Specification)

### 3.1 Kernel Documentation Anchors (S002)
- **Source:** S002 — `Control Group v2` (`https://docs.kernel.org/admin-guide/cgroup-v2.html`), sections `memory.events:1448–1509` and `memory.events.local:1505–1509` (opened 2026-10-19; `corpus/SOURCES.md:8`).
- **Implementation:** S003 — Linux kernel v7.2 `mm/oom_kill.c:935–936` (`count_vm_event(OOM_KILL); memcg_memory_event_mm(mm, MEMCG_OOM_KILL);`); S004 — `mm/memcontrol.c:4965–4966` (`events[MEMCG_OOM_KILL]`).

### 3.2 Hierarchical (`memory.events`) vs Local (`memory.events.local`)
1. **Hierarchical Counter (`memory.events:1448-1509`):**
   - *"The counters in memory.events are cumulative and show the aggregate count in the cgroup and its subtree."*
   - Field `oom_kill`: *"The number of processes belonging to this cgroup killed by any kind of OOM killer."*
   - Propagation mechanism: When the kernel OOM killer triggers on a process (S003 `mm/oom_kill.c:936`), `memcg_memory_event_mm` increments `MEMCG_OOM_KILL` on the victim's memcg. The kernel traverses up the ancestor hierarchy, incrementing `memory.events` for every containing ancestor up to root.
2. **Local Counter (`memory.events.local:1505-1509`):**
   - *"Similar to memory.events but the counters are for the cgroup itself and don't include descendants."*
   - Strict Non-Propagation: The local counter increments **only** if the victim process's direct cgroup membership (`mm->owner->cgroups`) matches that exact cgroup. Descendant kills do not touch `memory.events.local` of any parent cgroup.

### 3.3 The "No Internal Processes" Constraint & Descendant Exclusion
In cgroup v2:
- A non-root cgroup cannot distribute domain controllers (including `memory`) to child cgroups if it contains processes (`cgroup.procs` must be empty before enabling controllers in `cgroup.subtree_control`).
- In standard systemd unified cgroup hierarchies, `user.slice` and `user-1000.slice` serve as intermediate routing nodes, while managed processes are assigned to leaf units (`user-1000.slice/user@1000.service/...`, `user-1000.slice/session-*.scope`, `user-1000.slice/app-*.scope`).
- **Consequence:** Under this standard configuration, `user-1000.slice/memory.events.local` does not record kills occurring in descendant units. It is not asserted to be perpetually zero across all conceivable configurations without live verification, but by S002 authority it cannot count descendant kills.

---

## 4. Why Cgroup `memory.events.local` Cannot Replace the Journal OOM Alarm

In Round 13, ClaimAttack (`.ufo/waves/round-13/build/ClaimAttack.md:51`) posited:
> *"The parent's follow-up directs the replacement. If it lands, the remaining OOM side is fine: an OOM inside the user slice still flips DRIFT through `CGROUP_OOM_KILL` (the same `memory.events` counter that cgroup.c `:3084-3086` watches). No new CGROUP probe is needed."*

This reasoning was flawed and led directly to the Round 13 `rejected-harmed` verdict. There are four structural reasons why `memory.events.local` cannot replace the journal OOM alarm:

### 4.1 Descendant Exclusion by Kernel Design (S002)
- All user-session processes, services, and agent jobs reside in descendants of `user-1000.slice`.
- When an OOM killer terminates a process inside `user@1000.service/mori.service`, `user-1000.slice/memory.events.local` **does not increment**.
- If census checks `user-1000.slice/memory.events.local` for `service_oom_kill > 0`, it reads `0`.
- The `CGROUP_OOM_KILL crit` finding **does not fire for that descendant kill**.
- If the journal notice (`fe6faa94...`) is demoted to `info` and `OOM_KILL_JOURNAL crit` is removed, the descendant OOM kill produces no critical alarm and no `DRIFT`.

### 4.2 Out-of-Scope System Units and Other Slices
- System daemons in `system.slice` (Docker, containerd, hypervisors, system services) and processes in other user sessions (`user-0.slice`) are outside the `user-1000.slice` tree entirely.
- Neither `memory.events` nor `memory.events.local` under `user-1000.slice` receives any signal when a system-level process is OOM-killed.
- The system journal (`journalctl --system`) captures system unit OOM notices (`SD_MESSAGE_UNIT_OUT_OF_MEMORY`), but `user-1000.slice` has zero visibility into them.

### 4.3 Cgroup Instance Lifecycle vs Persistent Journal Event History
- Cgroup counter lifetime is bounded by the lifetime of the cgroup instance, not a universal boot duration.
- When a transient cgroup (such as a systemd scope created for a runner, terminal, or batch job) suffers an OOM kill and its remaining processes exit, systemd deconstructs and removes the cgroup from `/sys/fs/cgroup`.
- Once the directory is unlinked, its `memory.events.local` file disappears (`ENOENT`).
- Even for persistent services (`user@1000.service`), if the service manager restarts, its cgroup is recreated and counters reset.
- In contrast, the systemd journal is an append-only event log. It retains persistent, timestamped, boot-anchored structured records (`_BOOT_ID`, `MESSAGE_ID=fe6faa94...`, `UNIT=`, `USER_UNIT=`, `UNIT_RESULT=oom-kill`). It preserves the evidence of the kill regardless of whether the cgroup still exists.

### 4.4 Disjoint Semantic Planes: State Presence Flag vs Event Alarm
- As established in `corpus/knowledge/oom-kill-counter-kernel-only-r12.md` and `SiblingOverlap.md:31,144`:
  - `memory.events oom_kill` at ancestor slices is a **stored cumulative presence flag** across that cgroup instance's lifetime, not a real-time event meter.
  - A positive value on `user-1000.slice/memory.events` indicates that *at least one process in the user slice was killed at some point during that instance's lifetime*.
  - On a desktop/development workstation, this counter frequently reflects an unrelated desktop crash from days ago (e.g. an interactive terminal `python3` on 2026-10-13, as documented in census line 1148).
  - Firing `crit` on `user-1000.slice/memory.events` causes permanent false `DRIFT` across the entire boot/session and absorbs `tsukuroi`'s OS triage into `mori`.
  - For this reason, `mori` downgraded `user-1000.slice/memory.events > 0` to `CGROUP_OOM_KILL_CUMULATIVE info`.
  - Demoting the journal notice to `info` and removing `OOM_KILL_JOURNAL crit` left the local cgroup critical branch (`CGROUP_OOM_KILL crit`) technically present in code, rather than literally zero alarm paths registered. However, because local slice counters do not guarantee visibility into descendant services/scopes or out-of-scope system units, the critical cgroup path cannot substitute for the lost journal OOM alarm. That missing descendant and out-of-scope guarantee is itself decisive harm (`round-13-verifier-spotcheck.md:85`).

---

## 5. Precise Counter Boundaries (Comparative Matrix)

The following matrix defines the boundaries, authority, scope, and behavior of all relevant OOM detection channels across cgroup and journal planes:

| Surface / Channel | Authority & Anchor | Plane | Scope / Coverage | Excluded Boundaries | Lifetime & Retention | Census Finding ID & Severity | Triage Routing & Owner |
|---|---|---|---|---|---|---|---|
| **Local Slice Cgroup**<br>`user-1000.slice/memory.events.local` | S002 `memory.events.local:1505-1509` | State (scalar counter) | Direct slice processes only (rarely hosting processes under cgroup v2) | **All descendants** (`user@1000.service`, scopes), all system units, other user slices | Cgroup instance duration (resets if slice recreated) | `CGROUP_OOM_KILL crit`<br>*(Bypasses descendant kills)* | `tsukuroi` (OS/desktop) |
| **Ancestor Slice Cgroup**<br>`user-1000.slice/memory.events` | S002 `memory.events:1448-1509`; S004 `mm/memcontrol.c:4965-4966` | State (cumulative presence flag) | Hierarchical across `user-1000.slice` subtree (services + desktop scopes) | All system units (`system.slice`), kernel threads, other user slices | Cgroup instance duration (typically spans user session / boot); cumulative | `CGROUP_OOM_KILL_CUMULATIVE info` | `tsukuroi` (OS/desktop; cumulative note) |
| **User Service Cgroup**<br>`user@1000.service/memory.events` | S002 `memory.events:1448-1509` | State (hierarchical counter) | Hierarchical across `systemd --user` managed services | Desktop scopes outside `user@1000.service` (e.g. `app-*.scope`), login sessions, system units | Resets if `user@1000.service` restarts | Fallback not taken when `.events.local` readable | `mori` (if fleet service) / `tsukuroi` |
| **Journal User Scope**<br>`journalctl --user -b`<br>`MESSAGE_ID=fe6faa94...` | S013 `catalog:604-616`; `sd-messages.h:198-199`; `src/core/cgroup.c:3097-3100` | Event stream (unit notice) | Units managed by `systemd --user` where `memory.events oom_kill` increased | Processes outside systemd units; unmanaged processes; system units | Persisted in user journal across unit restarts; boot-bounded (`_BOOT_ID`) | Restored: `OOM_KILL_JOURNAL crit`<br>(+ `KERNEL_OOM_NOTICE_JOURNAL_USER`) | Split by `UNIT`/`USER_UNIT`: fleet units → `mori`; non-fleet → `tsukuroi` |
| **Journal System Scope**<br>`journalctl --system -b`<br>`MESSAGE_ID=fe6faa94...` | S013 `catalog:604-616`; `sd-messages.h:198-199`; `src/core/cgroup.c:3097-3100` | Event stream (unit notice) | Units managed by PID 1 in `system.slice` | User units (unless forwarded); unmanaged processes | Persisted in system journal across service restarts; boot-bounded (`_BOOT_ID`) | `KERNEL_OOM_NOTICE_JOURNAL_SYSTEM info` | `tsukuroi` (system/OS services) |
| **Journal Process Exit**<br>`MESSAGE_ID=98e32220...`<br>`EXIT_CODE=killed`<br>`EXIT_STATUS=9` | S035 `catalog:568-575`; S036 `unit.c:6379-6391` | Event stream (process termination record) | Systemd-observed unit processes exiting via SIGKILL (includes OOM SIGKILL and admin SIGKILL) | Processes not monitored as unit main/control pid; sender/cause unrecorded | Persisted in journal for queried boot | `KILL_SIGNAL_JOURNAL warn` (user)<br>`KILL_SIGNAL_JOURNAL_SYSTEM info` (system) | `mori` (warns on user scope; attribution none) |

---

## 6. Synthesis & Recommendations for Round 14 C1

1. **Restore `OOM_KILL_JOURNAL crit` / `DRIFT`:**
   - A positive count of user-scope kernel-OOM notices (`MESSAGE_ID=fe6faa94...`) or observed `UNIT_RESULT=oom-kill` must emit `OOM_KILL_JOURNAL crit` and set `st=drift` in `probe_journal`.
   - Counting notices as structured catalog records does not require suppressing the alarm.
2. **Do Not Treat Cgroup Counters as a Replacement for Journal Alarms:**
   - The cgroup probe (`probe_cgroup`) must remain what it actually is: a check on resource runway (`memory.pressure`, fill ratio, peak high-watermark) and a presence flag for cumulative instance-level events (`CGROUP_OOM_KILL_CUMULATIVE info`).
   - It cannot and must not be cited as replacement coverage for journal event alarms.
3. **Clean Up Selection Semantics in `probe_cgroup`:**
   - Clarify the variable naming: `user-1000.slice/memory.events.local` should be identified as the slice's local counter, not labeled as `service_oom_kill`.
   - If monitoring the user service is intended, `SERVICE_EVENTS` must not be hidden behind an unconditional `if [ -r "$LOCAL_EVENTS" ]` check.
4. **Preserve Scope Partitioning & Routing:**
   - Preserve independent reporting of `journal.user` and `journal.system`.
   - Preserve separate classification of failed units via subject metadata (`UNIT=`, `USER_UNIT=` per S037) into fleet units (`UNIT_FAILURE_JOURNAL`) vs desktop/OS units (`UNIT_FAILURE_OUT_OF_SCOPE` routed to `tsukuroi`).
   - Missing or unreadable subject metadata must be graded as `unknown`, never guessed.

---

## 7. Operational Status

- **Verification:** Source-only inspection. No test, build, lint, format, smoke or live check command was run (Contract §5 / Leaf Bounds). Hypotheses regarding live controller configurations or runtime states are qualified as source deductions without live verification.
- **Tools:** No tools installed or upgraded.
- **Deliverable:** Scoped report written to `.ufo/waves/round-14/build/CgroupScope.md`.
- **Peer Coordination:** Findings ground the Round 14 C1 coverage claim, closing verifier defect 2 (`round-13-verifier-spotcheck.md:85`) and informing `MoriR14.OomAttack`, `MoriR14.CensusRepair`, and `MoriR14.JournalRegression`.
