# Mo54ConnCrossClaim — Cross-Claim Synthesis and the Single-Channel Proxy Gap

**Seat:** Mo54ConnCrossClaim (Connector)  
**Lane:** mori-shokunin (round 54, wave w1)  
**Data revision:** `78295c764093ff1f6cee08d7246679900bde7265`  
**Entering tip:** `39dcf4d7e410d362781a47e8365ca23b5c807598`  
**Host:** Linux 7.2.11-arch1-1 (MACHINE_ID: MACHINE_ID)  
**Role:** UFO-FSD Connector (Evidence, Affected Axes, Proposed Move, Risks, Verification; leaf seat, no subagents)

---

## 1. Cross-Claim Pattern and the Shared Principle

Round 54 addresses two lowest non-retired axes: **C1 (freshness)** and **C2 (depth)**. Each claim resolves an instance of an epistemic failure mode that has recurred throughout the lane's history:

1. **C1 Freshness Pattern (`kernel-v7.3-recheck-r54.md`):**  
   *A located quote is not a located claim.*  
   Round 53 verified that quoted strings from Linux v7.2 survived in Linux v7.3 sources (`status = held`), but lexical token survival in a source file does not prove that the code at that location means what the claim asserts. Round 54 introduces a dual arm:
   - **The line arm:** Locates the exact line of the v7.3 copy on which the quote begins, proving spatial placement.
   - **The voter disposition arm:** Human/seat review determining whether the claim still holds (`disposition = holds` vs `changed`), binding semantic truth to independent verification rather than lexical presence.

2. **C2 Depth Pattern (`memory-failure-kills-r54.md`):**  
   *A death without an OOM record is not an unexplained death.*  
   Previously, mori's kill observability rested entirely on OOM mechanisms (kernel OOM killer, memcg OOM events, userspace daemons). If a process terminated via `SIGKILL` or `SIGBUS` with no accompanying `memory.events oom_kill` or kernel `Out of memory:` log line, telemetry called the death "unexplained" or attributed it to "cause unknown". C2 demonstrates that the kernel's hardware memory-failure subsystem (`mm/memory-failure.c`) issues forced `SIGKILL` (when unmapping corrupted pages fails) and `SIGBUS` (with `BUS_MCEERR_AR` / `BUS_MCEERR_AO`), tracking these fatal events in `/proc/meminfo HardwareCorrupted`, `/sys/devices/system/node/node*/memory_failure/*`, and `Memory failure:` logs. The absence of an OOM event is not evidence of the absence of a kernel kill.

### The Unified Shared Principle: The Single-Channel Proxy Fallacy

Both claims confront the identical epistemological breakdown:  
**A single-channel syntactic or observability proxy must never be substituted for multidimensional semantic or causal ground truth: syntactic token survival does not establish semantic validity, and single-subsystem silence does not establish event absence.**

- **The Positive Fallacy (C1):** Conflating lexical string survival (`held`) with semantic truth. A substring can persist verbatim across kernel releases while the enclosing control flow, caller preconditions, or data structures invert its meaning. Proving claim truth requires explicit spatial anchoring (the line arm) and semantic adjudication (the disposition vote).
- **The Negative Fallacy (C2):** Conflating unobserved evidence in one channel (no OOM records) with the non-occurrence of an event ("unexplained death"). Proving absence of an event requires complete enumeration of all causal delivery paths (`mm/memory-failure.c` alongside `mm/oom_kill.c`).

---

## 2. Governing QUALITY Criteria

The lane's quality constitution (`corpus/QUALITY.md`) records explicit criteria that formalize this shared principle across historical rounds:

| Criterion | Rule Text / Essence | Connection to C1 / C2 Principle |
|:---|:---|:---|
| **QUALITY 150** | *A release recheck says where each quote now begins, not only that its words survive.* (Round 54) | Direct C1 rule: Lexical presence (`held`) proves only that words occur somewhere. Mechanical line location (`line_ok`) plus independent disposition votes are required to verify the claim. |
| **QUALITY 151** | *A death with no OOM record is not called unexplained until the memory-failure counters are read.* (Round 54) | Direct C2 rule: OOM evidence alone cannot exclude a kernel kill because `mm/memory-failure.c` kills outside the OOM path; reading `node*/memory_failure/total` and `HardwareCorrupted` is required before asserting "no cause". |
| **QUALITY 71** | *Do not turn a partial collection into a negative or uniqueness verdict.* (Round 23) | Prohibits deriving "no kill" or "cause unknown" from a partial observation set (checking only OOM channels while ignoring memory-failure channels). |
| **QUALITY 17** | *A detection recipe states which delivery paths it cannot see.* (Round 12) | A kill detector must enumerate its blind spots (e.g., an OOM probe cannot see `SIGBUS`/`SIGKILL` delivered by hardware memory corruption handlers). |
| **QUALITY 14** | *A counter's semantics cite its increment site, not only documentation wording.* (Round 12) | Documentation words (like "any kind of OOM killer") are superficial proxies; semantic truth lies in the concrete code increment site, mirroring C1's distinction between quote text and code meaning. |
| **QUALITY 8** | *A "cannot fake / cannot fail / cannot accept" claim enumerates the channels or inputs tested; untested classes are named residuals.* (Round 12) | Prohibits blanket negative assertions without channel enumeration. |
| **QUALITY 34** | *... a valid empty capture is a positive 0 ... never evidence that no event occurred ...* (Round 15) | An empty capture on an OOM journal query proves zero OOM records were matched; it does not prove no kill event occurred on the host. |
| **QUALITY 124** | *A stated count of kernel objects carries the enumerating command over a pinned source.* (Round 47) | Prohibits assertions of exclusivity or completeness without complete mechanical enumeration over source bytes. |

---

## 3. Open Surfaces Exhibiting the Same Gap

An exhaustive sweep of the lane's runtime tools (`tools/`) and knowledge base (`corpus/knowledge/`) reveals critical surfaces where the identical gap remains open:

### 3.1. Tool Telemetry Reporting "No Cause" from OOM-Only Evidence

1. **`tools/mori-census.sh` (Lines 1464 and 1630):**  
   In the unit signal check and `KILL_SIGNAL_JOURNAL` alarm generation:
   - Line 1464:  
     `subj="class=unit_sigkill_record unit=record message_id=$JOURNAL_ID_UNIT_SIGKILL signal=9 count=$n scope=$scope attribution=none note=unit process exited on SIGKILL; cause unknown (a kernel OOM can also deliver SIGKILL) boot=${sboot[$scope]}"`
   - Line 1630:  
     `emit_finding KILL_SIGNAL_JOURNAL warn "... note=unit process exited on SIGKILL and/or unit failed with result signal; cause unknown (a kernel OOM can also deliver SIGKILL); ..."`
   - **The Gap:** The census tool checks only systemd journal messages for OOM (`fe6faa94e77746638e4971863ec7709d`) and kernel OOM records. When a process terminates on `SIGKILL` without an OOM journal record, the tool emits a finding asserting `cause unknown (a kernel OOM can also deliver SIGKILL)`.  
   - This assumes that kernel OOM is the *sole* kernel-delivered `SIGKILL` path. It completely ignores `mm/memory-failure.c:470-472` (`pr_err("%#lx: forcibly killing %s:%d because of failure to unmap corrupted page\n", ...); do_send_sig_info(SIGKILL, ...)`).  
   - Crucially, `tools/mori-census.sh` already possesses a helper `meminfo_field` at line 647 (used for `MemTotal` and `MemAvailable` at lines 1791–1792), yet it never reads `meminfo_field HardwareCorrupted` or `/sys/devices/system/node/node*/memory_failure/total`. It asserts "cause unknown" in direct violation of QUALITY 151 and QUALITY 71.

2. **`tools/mori-seat-terminal.py` (Lines 788–799):**  
   When a wave seat or agent session terminates with an unclassified error status, `_classify()` falls back to `dead_error_other`. It never checks host hardware corruption counters or signal codes to determine if the seat runner was terminated by `SIGBUS` (`BUS_MCEERR_AR`/`AO`) or unmap `SIGKILL`.

3. **`tools/mori-oom-killers.py` (Lines 68–74, 324–329):**  
   Evaluates earlyoom and systemd-oomd statuses, returning `KILLERS_QUIET` (exit 0) when those daemons did not act. In fleet contexts, a quiet OOM killer is often conflated by higher-level scripts with "no resource-induced terminations occurred", ignoring hardware memory corruption kills.

### 3.2. Knowledge Base Entries with Prose Anchors at Old Tags

The C1 freshness recheck counter (`count-c1.py`) discovers claims exclusively through `scope()` (lines 219–224), which requires Markdown tables matching the header `["claim", "source", "quote"]`. Any knowledge entry that records its kernel anchors in prose catalogues is completely invisible to `count-c1.py`:

1. **`corpus/knowledge/system-pressure-r24.md`:**  
   - Pinned to Linux `v7.2` throughout (sources S090–S095).
   - Inlines over 25 explicit GitHub URL pointers with hardcoded line numbers to `v7.2` files across sections F1–F12, Decision Table, and U1–U5:
     - `psi.rst:36-38`, `psi.c:1710-1721` (line 66, 68)
     - `psi.rst:40-43`, `psi.c:1290-1296`, `psi.rst:45-56` (lines 75, 78, 81)
     - `psi.rst:57-59`, `psi.c:1282-1288`, `psi.c:1540,1545,1550,1686` (lines 85, 87, 89)
     - `psi.rst:60-65`, `psi.c:1284-1288`, `psi.c:160-164`, `psi.c:1268-1270`, `psi.c:600-602` (lines 94, 96, 98, 100, 101)
     - `psi.c:1273-1296`, `psi.c:1032-1042`, `psi.c:1364-1367` (lines 106, 107, 109)
     - `psi.c:1717-1719`, `psi.c:1260-1263` (lines 113, 116)
     - `psi.c:1257-1258`, `psi.c:228-240`, `psi.c:149-158`, `psi.c:1553-1566`, `psi.c:1711-1719` (lines 120, 121, 123, 124, 126)
     - `psi.rst:67-88`, `psi.c:1372-1373`, `psi.c:167`, `psi.c:1596-1598` (lines 132, 134, 136)
     - `psi.rst:178-187`, `cgroup.c:4077-4091`, `cgroup.c:4127`, `sched_clock.c:48-50, 242-243` (lines 142, 144, 146, 165)
   - Because it contains no claim table, `count-c1.py` derived 0 rows from it. Contract named limits explicitly disclose: *"D covers claim|source|quote tables only (not prose, oom-tracepoints-r47.md's catalogue or system-pressure-r24.md's v7.2 anchors)"*. These 25+ line anchors remain unverified historical debts at v7.3.

2. **`corpus/knowledge/oom-tracepoints-r47.md`:**  
   - Headlined `# The OOM tracepoints at Linux v7.2: eight events, and which one names the victim`.
   - Sources S475 and S476 pin `v7.2`.
   - Contains 10+ explicit line anchors:
     - Header lines: `include/trace/events/oom.h:12, 34, 76, 118, 134, 150, 166, 183` (line 17), `oom.h:105` (line 35).
     - Call site lines: `mm/oom_kill.c:751-775` (line 41), `mm/oom_kill.c:560-562` (line 48), `mm/oom_kill.c:980-984` (line 55), `mm/page_alloc.c:3807-3808` (line 57), `fs/proc/base.c:1138-1140` (line 59).
   - Structured as a prose catalogue and lifecycle description; lacks a claim|source|quote table and was therefore omitted from C1.

3. **`corpus/knowledge/census-cgroup-levels-r45.md` (Lines 3, 5):**  
   Source S473 pins `https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst` and the recheck instruction runs `curl` against the `@v7.2` tag, with no automated recheck at v7.3.

4. **`corpus/knowledge/kernel-oom-line-attribution-r12.md` (Lines 1, 3) & `oom-kill-counter-kernel-only-r12.md` (Lines 1, 3):**  
   Both anchor to `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c` lines 935–936 and 447–453 in prose headers rather than claim tables.

---

## 4. Comprehensive Cross-Surface Comparison

| Surface / Artifact | Category | Monitored / Checked Proxy | Ground Truth Omitted / Ignored | Governing QUALITY Rule | Exact Pointer |
|:---|:---|:---|:---|:---|:---|
| `tools/mori-census.sh` | Tool (Runtime) | Journal OOM IDs & cgroup `oom_kill` only | Memory-failure SIGKILL (`mm/memory-failure.c:470-472`), `HardwareCorrupted`, `node*/memory_failure/total` | QUALITY 151, QUALITY 71, QUALITY 17 | `tools/mori-census.sh:1464,1630` |
| `tools/mori-seat-terminal.py` | Tool (Settlement) | Exit status / API error code | SIGBUS (`BUS_MCEERR_AR`/`AO`) or unmap SIGKILL from MCE | QUALITY 151, QUALITY 8 | `tools/mori-seat-terminal.py:794,799` |
| `tools/mori-oom-killers.py` | Tool (OOM) | `earlyoom` / `systemd-oomd` unit state | Hardware memory-failure kill events | QUALITY 71, QUALITY 34 | `tools/mori-oom-killers.py:68-74` |
| `corpus/knowledge/system-pressure-r24.md` | Knowledge (Prose) | v7.2 raw GitHub URLs with line numbers | v7.3 code shifts; omitted from `count-c1.py` because not in a claim table | QUALITY 150, QUALITY 124 | `system-pressure-r24.md:66-165` (25+ inline anchors) |
| `corpus/knowledge/oom-tracepoints-r47.md` | Knowledge (Prose) | v7.2 tracepoint line numbers in prose | v7.3 header lines & call sites; omitted from `count-c1.py` scope | QUALITY 150, QUALITY 124 | `oom-tracepoints-r47.md:17-59` (10+ inline anchors) |
| `corpus/knowledge/census-cgroup-levels-r45.md` | Knowledge (Entry) | v7.2 jsdelivr raw URL | v7.3 cgroup-v2 documentation navigation drift | QUALITY 150 | `census-cgroup-levels-r45.md:3,5` |
| `corpus/knowledge/kernel-v7.3-recheck-r54.md` | Knowledge (Ledger) | Lexical quote match (`held`) | Code semantics around quote (resolved only by voter disposition) | QUALITY 150, QUALITY 14 | `kernel-v7.3-recheck-r54.md:21-53` |
| `corpus/knowledge/memory-failure-kills-r54.md` | Knowledge (Entry) | Source text analysis at v7.3 | Runtime enforcement in tools (disclosed: knowledge only) | QUALITY 151 | `memory-failure-kills-r54.md:49-61` |

---

## 5. Bounded Connector Move: The Dual Channel-Completeness Binding

In accordance with the UFO-FSD Connector specification, this proposal identifies one non-obvious synthesis that improves declared round axes without harming any other axis.

### 5.1. Affected Axes
- **Depth (declared round axis, currently 5):** Advances from passive documentation in `memory-failure-kills-r54.md` to active operational verification in `tools/mori-census.sh`.
- **Freshness (declared round axis, currently 5):** Expands the C1 line-arm recheck surface to capture previously untouchable prose anchors in `system-pressure-r24.md` and `oom-tracepoints-r47.md`.
- **Calibration (lowest non-retired axis, tied at 5):** Eliminates a false-negative finding note in `mori-census.sh` that claims "cause unknown" whenever a non-OOM SIGKILL occurs.
- **Operability (currently 7, unharmed):** Adds zero heavy runtime dependencies; reuses existing `meminfo_field` helper.

### 5.2. Proposed Move

**Title:** Channel-Completeness Binding: Operationalize Hardware Memory-Failure Telemetry in `mori-census.sh` and Table-Bind Prose Anchors for Round 55.

The move consists of two complementary, structurally identical actions routed for round 55:

1. **Substrate A (Runtime Telemetry in `tools/mori-census.sh`):**  
   Eliminate the uncalibrated "cause unknown (a kernel OOM can also deliver SIGKILL)" finding note.
   - Extend `tools/mori-census.sh` to read `/proc/meminfo HardwareCorrupted` using the existing `meminfo_field HardwareCorrupted` function (line 647).
   - Add a lightweight, rc-gated sysfs check for `/sys/devices/system/node/node*/memory_failure/total`.
   - Update lines 1464 and 1630: If a unit terminates on `SIGKILL` without an OOM record, but `HardwareCorrupted > 0` or node memory failure totals are non-zero, attribute the termination to `hwpoison_memory_failure` rather than `attribution=none note=cause unknown`. If both are zero, report `cause unknown (OOM and hardware memory failure excluded by zero counters)`. This directly satisfies QUALITY 151 and QUALITY 71.

2. **Substrate B (Knowledge Recheck Architecture in `corpus/knowledge/`):**  
   Convert the unverified prose anchor catalogues into standardized claim tables.
   - Restructure `corpus/knowledge/system-pressure-r24.md` and `corpus/knowledge/oom-tracepoints-r47.md` to move their inline line-number anchors into standard `| claim | source | quote |` Markdown tables.
   - This automatically brings their 35+ v7.2 line anchors into the scope of `count-c1.py`'s line-arm and voter-disposition recheck engine on subsequent release triggers, eliminating the unmonitored prose debt disclosed in the round-54 contract.

### 5.3. Second-Order Effects and Risks

- **Runtime & Substrate Risk:**  
  Reading `/sys/devices/system/node/node*/memory_failure/total` on a machine without NUMA or with restricted sysfs could fail.  
  *Mitigation:* Sysfs reads must be rc-gated with fallback to `0` or `unavailable` (per QUALITY 6). `HardwareCorrupted` in `/proc/meminfo` is universally available on Linux kernels with `CONFIG_MEMORY_FAILURE=y` and is already safely parsed by `meminfo_field`.
- **Contract & Downstream Compatibility:**  
  Downstream scripts parsing `KILL_SIGNAL_JOURNAL` finding lines might rely on the exact substring `cause unknown`.  
  *Mitigation:* Retain the finding ID `KILL_SIGNAL_JOURNAL` and severity `warn`, altering only the structured key-value tokens in the finding body (e.g., adding `hardware_corrupted_kb=N mf_total=M`).
- **Counter Invariance (Round 54 Rule):**  
  Neither `count-c1.py` nor `count-c2.py` is modified during round 54. This move is pre-registered and routed as a candidate claim for round 55, preserving the frozen round-54 contract byte-for-byte.

### 5.4. Verification Plan

1. **Synthetic Fixture Verification (for Substrate A):**  
   Construct a fixture in `tools/fixtures/` with a non-zero `HardwareCorrupted: 4 kB` in `/proc/meminfo` and a simulated `SIGKILL` unit exit. Verify that `mori-census.sh` emits `class=kill_signal` with `attribution=hwpoison` rather than `cause unknown`.
2. **Mechanical Recheck Verification (for Substrate B):**  
   Run `python3 .ufo/waves/round-54/count-c1.py --scope` against a branch containing the restructured table. Verify that `scope()` discovers the new rows and that `line_ok` correctly locates them in the v7.3 sources.

---

## 6. Housekeeping & Execution Record

- **Scratch directory:** `/fast/scratch/hyaku/mori-r54/Mo54ConnCrossClaim/` created with `mkdir -p`, `export TMPDIR=/fast/scratch/hyaku/mori-r54/Mo54ConnCrossClaim/tmp`, and verified. Cleaned up upon seat completion.
- **Tools:** No tools installed or upgraded (none needed; pacman untouched).
- **Mutations:** Read-only operations only. Zero git or jj mutations executed in `/home/vgpnk/Projects/shokunin/mori-shokunin` or `/home/vgpnk/Projects/shokunin`.
- **Host reads:** Read-only inspection of repository files, live host kernel `7.2.11-arch1-1`, `/proc/meminfo`, and `/sys/devices/system/node/node0/memory_failure/*`. No sysctls modified, no memory injected or unpoisoned.
- **Vote lines:** Zero lines begin with reserved vote keywords (`RECHECK`, `QUOTE`, `ENTAIL`, `REPLACE`).

---

## Findings

- **HIGH** — `tools/mori-census.sh:1464,1630`: `mori-census.sh` emits finding notes claiming `cause unknown (a kernel OOM can also deliver SIGKILL)` upon detecting unit `SIGKILL` records without inspecting `/proc/meminfo HardwareCorrupted` or `/sys/devices/system/node/node*/memory_failure/total`. This constitutes a false-negative attribution that violates QUALITY 151 and QUALITY 71 by treating absence of OOM evidence as absence of an explained kernel kill.
- **HIGH** — `corpus/knowledge/system-pressure-r24.md:66-165`: Over 25 inline GitHub URL anchors with line numbers to Linux `v7.2` files (`psi.c`, `psi.rst`, `cgroup.c`, `sched_clock.c`) are embedded in unstructured prose and tables lacking the `claim | source | quote` format. Consequently, `count-c1.py`'s scope discovery completely skips them, leaving them unverified at Linux v7.3.
- **MED** — `corpus/knowledge/oom-tracepoints-r47.md:17-59`: 10+ line-number anchors into `include/trace/events/oom.h` and `mm/oom_kill.c` at Linux `v7.2` are recorded as prose and catalogue sections without a claim table, evading automated v7.3 freshness verification.
- **LOW** — `tools/mori-seat-terminal.py:794,799`: Terminal session classifier maps unclassified process deaths to `dead_error_other` without verifying whether runner processes were killed by machine-check `SIGBUS` or `SIGKILL`.
- **LOW** — `corpus/knowledge/census-cgroup-levels-r45.md:3,5`: Source S473 recheck command hardcodes the `linux@v7.2` CDN URL, preventing automated detection of upstream documentation restructuring at v7.3.
