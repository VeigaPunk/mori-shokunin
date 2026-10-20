# S014 `journalctl(1)` Primary Source Report: Structured Fields, Scopes, and Safe Query Mechanics

**Target Axis**: Coverage (C1 structured journal scopes), Operability (C2 pipeline & exit status integrity)  
**Source Key**: S014  
**Primary Source**: `journalctl(1)` man page — `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html`  
**Access Date**: 2026-10-20  
**Upstream Version**: systemd 262  
**Observed Host Version**: systemd 261 (261.2-1-arch), Linux kernel 7.2.3-arch1-3  

---

## 1. Executive Summary & Frontier Axes

- **Coverage**: Transitioning kill/OOM detection away from free-form regexes over raw `MESSAGE` strings to structured `MESSAGE_ID` and trusted metadata tokens (`_BOOT_ID`, `__REALTIME_TIMESTAMP`). S014 provides the operational foundation via `--output-fields=`, `-b`, and scope switches (`--user`, `--system`, `-k`).
- **Operability**: Rescuing pipelines from SIGPIPE (141) and silent permission failure masking. S014 specifies exit code mechanics (`rc=0` on success, non-zero on failure), with measured permission denial returning `rc=1` (`No journal files were opened due to insufficient permissions`).

---

## 2. `--output-fields=`

### Quote & Source Anchor
- **Section**: `Output Options`
- **Anchor**: `#--output-fields=`
- **Verbatim Text**:
  > `A comma separated list of the fields which should be included in the output. This has an effect only for the output modes which would normally show all fields (verbose, export, json, json-pretty, json-sse and json-seq), as well as on cat. For the former, the "__CURSOR", "__REALTIME_TIMESTAMP", "__MONOTONIC_TIMESTAMP", and "_BOOT_ID" fields are always printed.`
- **Version Added**: Added in version 236.

### Semantic Analysis
- By default, full-object output modes (such as `json` or `export`) dump all fields present on an entry, including arbitrary, multi-line, unescaped, or sensitive free-text `MESSAGE=` values.
- Passing `--output-fields=` constrains the fields emitted in the output objects to only the user-specified list, plus the four automatic mandatory fields.
- Crucially: `MESSAGE` is **not** on the mandatory list. Specifying `--output-fields=_BOOT_ID` or `--output-fields=MESSAGE_ID,_BOOT_ID` completely eliminates `MESSAGE` from the serialized JSON. This satisfies the requirement for strictly MESSAGE-free extraction.
- In `cat` mode: S014 notes: *"If combined with the `--output-fields=` option will output the listed fields for each log record, instead of the message."* In `cat` mode, even the four mandatory fields are suppressed, emitting only the explicitly requested field values.

---

## 3. Automatic Mandatory Fields

### Observed Mandatory Fields
For all modes that normally print full fields (`verbose`, `export`, `json`, `json-pretty`, `json-sse`, `json-seq`):
1. `__CURSOR` — journal entry location identifier (used for stateful resumption and pagination via `--after-cursor=`).
2. `__REALTIME_TIMESTAMP` — microsecond UTC wallclock timestamp since Unix epoch.
3. `__MONOTONIC_TIMESTAMP` — microsecond monotonic boot timestamp.
4. `_BOOT_ID` — 128-bit boot identifier matching `/proc/sys/kernel/random/boot_id`.

### Invariance for Structured Scopes
- Regardless of which fields are passed to `--output-fields=` (e.g. `--output-fields=_BOOT_ID` or `--output-fields=MESSAGE_ID`), `journalctl` always injects these four internal metadata fields into JSON objects.
- Any parser consuming `journalctl -o json --output-fields=...` can unconditionally rely on `_BOOT_ID` and `__REALTIME_TIMESTAMP` for grouping and time-bounding without explicitly requesting them.
- No textual `MESSAGE` payload is injected unless `MESSAGE` is explicitly requested in `--output-fields=`.

---

## 4. Permission-Error Return Code (`rc`) & Failure Behavior

### Quote & Source Anchors
- **Section**: `Description`
- **Anchor**: `#Description`
- **Verbatim Text**:
  > `All users are granted access to their private per-user journals. However, by default, only root and users who are members of a few special groups are granted access to the system journal and the journals of other users. Members of the groups "systemd-journal", "adm", and "wheel" can read all journal files. Note that the two latter groups traditionally have additional privileges specified by the distribution. Members of the "wheel" group can often perform administrative tasks.`
- **Section**: `Output Options` (under `-q`, `--quiet`)
- **Anchor**: `#-q`
- **Verbatim Text**:
  > `Suppresses all informational messages (i.e. "-- Journal begins at …", "-- Reboot --"), any warning messages regarding inaccessible system journals when run as a normal user.`
- **Section**: `Exit status`
- **Anchor**: `#Exit%20status`
- **Verbatim Text**:
  > `On success, 0 is returned; otherwise, a non-zero failure code is returned.`

### Host-Verified Empirical Behavior
When an unprivileged user without membership in `systemd-journal`, `adm`, or `wheel` (tested via `nobody`) attempts to query inaccessible journals:
1. `journalctl --system -n 1`:
   - `stderr`:
     ```text
     Hint: You are currently not seeing messages from other users and the system.
           Users in groups 'adm', 'systemd-journal', 'wheel' can see all messages.
           Pass -q to turn off this notice.
     No journal files were opened due to insufficient permissions.
     ```
   - Exit code: `rc = 1`.
2. `journalctl --system -q -n 1`:
   - `stderr`:
     ```text
     No journal files were opened due to insufficient permissions.
     ```
   - Exit code: `rc = 1`.
3. `journalctl --user -n 1` (where no user journal directory exists or is accessible):
   - `stderr`: `No journal files were opened due to insufficient permissions.`
   - Exit code: `rc = 1`.

### Operability Rule
- **Silent failure avoidance**: Probes must never pipe `journalctl` into a counter or grep without gating on `journalctl`'s exit code (`rc=0`).
- If `journalctl` exits with `rc=1` (insufficient permissions / unreadable journal), the probe must emit an explicit unavailability/permission error, **never** a count of `0`. A count of `0` falsely claims no events occurred, violating QUALITY criterion 6 and 24.

---

## 5. `-b` / `--boot=` Scope Mechanics & Interactions

### Quote & Source Anchor
- **Section**: `Filtering Options`
- **Anchor**: `#-b%20ID%C2%B1offset%7Call`
- **Verbatim Text**:
  > `Show messages from a specific boot. This will add a match for "_BOOT_ID=".`  
  > `The argument may be empty, in which case logs for the current boot will be shown.`  
  > `If the boot ID is omitted, a positive offset will look up the boots starting from the beginning of the journal, and an equal-or-less-than zero offset will look up boots starting from the end of the journal. Thus, 1 means the first boot found in the journal in chronological order, 2 the second and so on; while -0 is the last boot, -1 the boot before last, and so on. An empty offset is equivalent to specifying -0, except when the current boot is not the last boot (e.g. because --directory= was specified to look at logs from a different machine).`  
  > `If the 32-character ID is specified, it may optionally be followed by offset which identifies the boot relative to the one given by boot ID. Negative values mean earlier boots and positive values mean later boots. If offset is not specified, a value of zero is assumed, and the logs for the boot given by ID are shown.`  
  > `The special argument all can be used to negate the effect of an earlier use of -b.`  
  > `Added in version 186.`

### Critical Parameter Interactions
1. **Default journalctl scope**:
   - Without `-b` or `-k`, `journalctl` prints entries across **all boots** accessible in the journal, starting with the oldest.
2. **Current boot scope**:
   - `-b` (empty argument) or `-b 0` or `-b -0` explicitly restricts queries to `_BOOT_ID=<current_boot>`.
3. **The `-k` / `--dmesg` trap**:
   - S014 Anchor `#-k`: *"Show only kernel messages. This adds the match `_TRANSPORT=kernel`. This implies `--boot=0` unless explicitly specified otherwise. Added in version 205."*
   - **Crucial implication**: `-k` implicitly constrains output to the current boot (`--boot=0`). To query kernel logs across all boots (e.g. for host-wide multi-boot OOM accounting), `-k -b all` **must** be explicitly supplied.
4. **The `-e` / `--pager-end` trap**:
   - Anchor `#-e`: implies `--lines=1000` and `--boot=0` unless explicitly overridden.

---

## 6. Safe Query Mechanics Specification

To guarantee conformance with fleet standards (no raw MESSAGE, rc-gated pipelines, scope isolation, no SIGPIPE):

### Mechanics Checklist
1. **Structured Matching**:
   Filter using field matches: `MESSAGE_ID=<hex>` (e.g., `fe6faa94e7774663a0da52717891d8ef`). Multiple `MESSAGE_ID`s can be combined with `+` for disjunction.
2. **MESSAGE-Free Output**:
   Always pass `-o json --output-fields=_BOOT_ID` (or include required structured fields such as `MESSAGE_ID`, `PRIORITY`, `_SYSTEMD_UNIT`). Never allow `MESSAGE` to be emitted.
3. **Quiet Mode (`-q`)**:
   Always pass `-q` to prevent warning hints and boot boundary markers from polluting stdout/stderr.
4. **Explicit Boot Scoping**:
   - For current-boot scoped counters: specify `-b 0`.
   - For kernel multi-boot sweeps: specify `-k -b all -q`.
5. **Scope Separation (QUALITY criterion 16)**:
   - Query user scope via `--user` (user session services).
   - Query system scope via `--system` (system services and kernel).
   - **Never sum** `--user` and `--system` counts; record each in its independent labeled scope.
6. **Pipeline & Error Gating (QUALITY criterion 6 & 7)**:
   - Do not pipe `journalctl` directly into short-lived consumers (`head -n 1`, `grep -q`) under `pipefail` (risk of SIGPIPE 141).
   - Buffer output or use `jq` to parse line streams.
   - Check `journalctl`'s exit code: if `rc != 0` (e.g., permission failure `rc=1`), abort and report `unavailable (permissions)`, not `0`.

### Exemplar Safe Query Command Templates

```bash
# Template 1: User-scope MESSAGE-free notice count for current boot
journalctl --user -q -b 0 MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID

# Template 2: System-scope MESSAGE-free notice count for current boot
journalctl --system -q -b 0 MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID

# Template 3: Kernel dmesg sweep across all boots (explicit -b all required due to -k default)
journalctl -k -b all -q -o json --output-fields=_BOOT_ID
```
