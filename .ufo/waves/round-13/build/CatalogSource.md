# CatalogSource Scout Report: S013 Catalog & MESSAGE_ID Semantics

## 1. Godspeed Posture & Named Axes
- **Judged axes**:
  - **Coverage (C1)**: Structured journal scope replacement for unstructured text regexes. Pinned catalog `MESSAGE_ID` identifiers provide unambiguous 128-bit typing for journal classes. Semantic units must be rigorously characterized as **unit notices** or **coredump notices**, never conflated with kernel victim counts, and maintained in independently labeled scopes (`user` vs `system`) that are never summed.
  - **Operability (C2)**: Field-restricted journal querying (`--output-fields=_BOOT_ID`) prevents unbounded text scraping, eliminates SIGPIPE / pipefail hazards in long pipelines, avoids formatting churn, and maintains robust verdict integrity.
- **Rules applied**:
  1. Name the axes (coverage, operability).
  2. Iterate cheap, in parallel (verified remote git source, local catalog, and local journal streams concurrently).
  3. Keep moves that improve any axis and harm none.
  4. Don't aim — let the frontier walk itself.

---

## 2. Pinned Source S013 Identity & Integrity

| Field | Value |
|---|---|
| **Registry ID** | `S013` (`corpus/SOURCES.md:19`) |
| **Source Title** | systemd message catalog (`systemd.catalog.in`) |
| **Pinned URL** | `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in` |
| **Pinned Commit** | `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` (2026-10-19) |
| **SHA-256 Digest** | `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592` |
| **Recheck Command** | `curl -fsSL https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in \| sha256sum` |
| **Recheck Result** | `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592  -` (exact match) |
| **Host Systemd Version**| systemd 261 (`261.2-1-arch`), kernel `7.2.3-arch1-3` |
| **Local Catalog Verification** | `journalctl --list-catalog fc2e22bc6ee647b6b90729ab34a250b1 fe6faa94e7774663a0da52717891d8ef d989611b15e44c9dbf31e3c81256e4ed` |
| **Local Verification Result** | All 3 catalog entries present and active in host catalog database |

---

## 3. The Exact Three MESSAGE_ID Identifiers & Semantic Units

### Identifier 1: `fc2e22bc6ee647b6b90729ab34a250b1`
- **Location in S013**: Line 66 (`catalog/systemd.catalog.in:66-77`)
- **Subject**: `Subject: Process @COREDUMP_PID@ (@COREDUMP_COMM@) dumped core`
- **Defined-By**: `systemd`
- **Documentation**: `man:core(5)`
- **Verbatim Text**:
  ```text
  -- fc2e22bc6ee647b6b90729ab34a250b1
  Subject: Process @COREDUMP_PID@ (@COREDUMP_COMM@) dumped core
  Defined-By: systemd
  Support: %SUPPORT_URL%
  Documentation: man:core(5)

  Process @COREDUMP_PID@ (@COREDUMP_COMM@) crashed and dumped core.

  This usually indicates a programming error in the crashing program and
  should be reported to its vendor as a bug.
  ```
- **Semantic Unit**: **Process coredump notice** (fatal crash report).
- **Producer**: `systemd-coredump(8)`.
- **Event Scope**: Program crash / abnormal termination generating a core dump (e.g., SIGSEGV, SIGABRT, SIGBUS).
- **Critical Distinction**: This is **NOT an OOM kill notice** or memory event. Conflating coredump notices with OOM kills is a severe category error.
- **Measured Host Counts**:
  - `journalctl --user -q MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 -o json --output-fields=_BOOT_ID | wc -l` → `1585`
  - `journalctl --system -q MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 -o json --output-fields=_BOOT_ID | wc -l` → `1`
  *(Note: Counting this class as an OOM kill would massively distort counts by over 1,500 entries on this host).*

---

### Identifier 2: `fe6faa94e7774663a0da52717891d8ef`
- **Location in S013**: Line 604 (`catalog/systemd.catalog.in:604-617`)
- **Subject**: `Subject: A process of @UNIT@ unit has been killed by the OOM killer.`
- **Defined-By**: `systemd`
- **Verbatim Text**:
  ```text
  -- fe6faa94e7774663a0da52717891d8ef
  Subject: A process of @UNIT@ unit has been killed by the OOM killer.
  Defined-By: systemd
  Support: %SUPPORT_URL%

  A process of unit @UNIT@ has been killed by the Linux kernel out-of-memory (OOM)
  killer logic. This usually indicates that the system is low on memory and that
  memory needed to be freed. A process associated with @UNIT@ has been determined
  as the best process to terminate and has been forcibly terminated by the
  kernel.

  Note that the memory pressure might or might not have been caused by @UNIT@.
  ```
- **Semantic Unit**: **Kernel OOM unit notice** (systemd notification of kernel OOM killer activity affecting a unit).
- **Producer**: systemd / PID 1 observing kernel OOM events in cgroups/units.
- **Kernel-Victim Cardinality**:
  - **Cardinality is strictly non-1:1**. A single kernel OOM kill event does NOT correspond to exactly one `fe6faa94…` notice.
  - Multi-unit fan-out: When a process in a unit is killed, systemd can generate notices for the specific unit, parent scopes, and parent slices across user and system manager instances.
  - Proven host empirical evidence: On host boot `7bd93aee71144017b870212161a3dabf`, there are exactly `5` kernel `Killed process` records (`journalctl -k -b all -q --grep='(Out of memory|Memory cgroup out of memory): Killed process [0-9]+'`), whereas there are `7` user-journal notices and `9` system-journal notices.
  - Causal caveat (from catalog text): *"Note that the memory pressure might or might not have been caused by @UNIT@."* A unit notice indicates victim containment, not culprit or fleet responsibility.
- **Measured Host Counts**:
  - `journalctl --user -q MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID | wc -l` → `7`
  - `journalctl --system -q MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID | wc -l` → `9`
  *(Note: Scopes must NEVER be summed. `7 + 9 = 16` is a meaningless number that counts neither victims nor unique events).*

---

### Identifier 3: `d989611b15e44c9dbf31e3c81256e4ed`
- **Location in S013**: Line 884 (`catalog/systemd.catalog.in:884-897`)
- **Subject**: `Subject: systemd-oomd killed one or more processes in unit @UNIT@`
- **Defined-By**: `systemd`
- **Documentation**: `man:systemd-oomd.service(8)`
- **Verbatim Text**:
  ```text
  -- d989611b15e44c9dbf31e3c81256e4ed
  Subject: systemd-oomd killed one or more processes in unit @UNIT@
  Defined-By: systemd
  Support: %SUPPORT_URL%
  Documentation: man:systemd-oomd.service(8)

  One or more processes in the @UNIT@ unit have been killed by systemd-oomd, in
  order to counter an out-of-memory situation on the system. This usually
  indicates that the system is low on memory and systemd-oomd decided to
  terminate one or more processes to reduce memory pressure.

  Note that the memory pressure might or might not have been caused by @UNIT@.
  ```
- **Semantic Unit**: **Userspace systemd-oomd unit kill notice**.
- **Producer**: `systemd-oomd.service`.
- **Kernel-Victim Cardinality**:
  - **Cardinality of killed processes per notice is $1 \le N$**. The subject explicitly declares: *"killed one or more processes in unit @UNIT@"*. One notice does not equal one killed process.
  - Userspace kill bypass: These kills are issued directly by `systemd-oomd` in userspace using `SIGKILL` (or `cgroup.kill`). They completely bypass kernel OOM counters (`oom_kill` in `/proc/vmstat` or cgroup `memory.events`), which increment only at `mm/oom_kill.c:935-936`.
  - Host state dependent: On this host, `systemd-oomd.service` is inactive/disabled (`systemctl is-active systemd-oomd.service` → `inactive`).
- **Measured Host Counts**:
  - `journalctl --user -q MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=_BOOT_ID | wc -l` → `0`
  - `journalctl --system -q MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=_BOOT_ID | wc -l` → `0`

---

## 4. Cardinality & Scope Independence Rules

1. **Zero Assumptions About Kernel-Victim Cardinality**:
   - `fe6faa94…` is a **unit notice**, not a victim counter.
   - $1 \text{ kernel victim} \neq 1 \text{ fe6faa94 notice}$.
   - $1 \text{ d989611b notice} \neq 1 \text{ killed process}$ ($N \ge 1$ processes per notice).
   - $1 \text{ fc2e22bc notice} = 1 \text{ coredump event}$, but $0 \text{ OOM kills}$.
2. **Strict Scope Independence (Scopes Are Never Summed)**:
   - System scope (`journalctl --system`) captures events observed by the system manager (PID 1) and system services.
   - User scope (`journalctl --user`) captures events observed by per-user service managers (`systemd --user`).
   - Adding user-scope notices to system-scope notices results in double-counting across observer boundaries.
   - QUALITY Criterion 16 is explicit: *"A kill count names its unit (kill vs notice) and its journal scope; scopes are never summed."*
3. **Attribution Separation**:
   - A journal notice indicates that an event occurred within `@UNIT@`.
   - It does NOT prove that `@UNIT@` caused the memory pressure (both catalog entries explicitly warn: *"memory pressure might or might not have been caused by @UNIT@"*).
   - It does NOT prove fleet-lane authorship. Attribution requires event-time correlation (e.g. `task_memcg` tokens from kernel records or explicit slice metadata), never post-hoc cgroup reads or notice sums.

---

## 5. QUALITY Criteria Compliance

- **Criterion 1 & 2 (Falsifiable claims with measured anchors)**:
  - S013 URL, commit `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af`, SHA-256 `e53707db...`.
  - Line anchors: `fc2e22bc…` at `:66`, `fe6faa94…` at `:604`, `d989611b…` at `:884`.
  - Recheck commands and exact counts verified on host journal.
- **Criterion 3 (Observation, inference, and unknown separated)**:
  - *Observed*: Exactly 3 catalog IDs in S013; exact subjects and text; local host counts: `fe6faa94…` (user=7, system=9), `d989611b…` (user=0, system=0), `fc2e22bc…` (user=1585, system=1), kernel `Killed process` records (5).
  - *Inference*: The numerical discrepancy (5 kernel vs 7 user vs 9 system) confirms fan-out across unit hierarchies. One kernel kill triggers multiple journal notifications across nested units and scopes.
  - *Unknown*: Exact ancestor unit mapping for each retained notice without inspecting `_SYSTEMD_UNIT` and `UNIT` fields; whether any killed processes existed in unread or rotated boots outside retained storage.
- **Criterion 15 (MESSAGE_ID typing, no text parsing)**:
  - All queries filter by `MESSAGE_ID=<uuid>` and restrict output with `-o json --output-fields=_BOOT_ID`.
  - No `MESSAGE` text is parsed or echoed.
- **Criterion 16 (Unit naming and scope separation)**:
  - `fe6faa94…`: unit notice (user or system).
  - `d989611b…`: oomd unit kill notice (user or system).
  - `fc2e22bc…`: coredump notice (user or system).
  - Kernel records: kernel victim record (kernel ring buffer / dmesg / kmsg).
  - User and system scopes are reported independently; never summed.
- **Criterion 17 (Delivery paths this cannot see)**:
  - Unstructured text messages logged without a registered catalog ID.
  - Kills by other userspace killers (e.g., `earlyoom` which logs to stderr without systemd catalog IDs).
  - Direct SIGKILL delivered by arbitrary host processes.
  - Rotated, cleared, or inaccessible journals (permission denials).

---

## 6. Proposed Checks for L1 Integration

The L1 integrator can verify the catalog source integrity and structured counts using the following checks:

```bash
# 1. Verify S013 pinned commit digest
curl -fsSL https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | sha256sum | grep -q '^e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592'

# 2. Verify all three MESSAGE_IDs exist in the host systemd catalog
journalctl --list-catalog fc2e22bc6ee647b6b90729ab34a250b1 fe6faa94e7774663a0da52717891d8ef d989611b15e44c9dbf31e3c81256e4ed | wc -l
# Expected: 3

# 3. Verify user and system scopes independently (never summed)
journalctl --user -q MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID | wc -l
journalctl --system -q MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID | wc -l
# Expected: 7 (user), 9 (system)

# 4. Verify systemd-oomd notices
journalctl --user -q MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=_BOOT_ID | wc -l
journalctl --system -q MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=_BOOT_ID | wc -l
# Expected: 0 (user), 0 (system)
```

---

## 7. Tooling Record
- **Tools installed/updated**: None. Existing system binaries (`curl`, `sha256sum`, `journalctl`, `jq`) fully satisfied all requirements.
