# S015 `systemd.journal-fields(7)` Primary Source Report: User vs Trusted Metadata, Representation, and Spoofability Limits

**Target Axis**: Coverage (C1 structured journal scopes), Operability (C2 pipeline & verdict integrity)  
**Source Key**: S015  
**Primary Source**: `systemd.journal-fields(7)` man page — `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html`  
**Access Date**: 2026-10-20  
**Upstream Version**: systemd 262  
**Observed Host Version**: systemd 261 (`261.2-1-arch`), Linux kernel `7.2.3-arch1-3`  

---

## 1. Executive Summary & Frontier Axes

- **Coverage (C1)**:
  - Transitioning mori's journal inspection from fragile, unstructured regexes on free-form message strings to typed, structured identifiers.
  - S015 formally divides journal fields into client-supplied **User Journal Fields** (such as `MESSAGE` and `MESSAGE_ID`) and implicitly kernel/journald-generated **Trusted Journal Fields** (prefixed with an underscore, e.g., `_BOOT_ID`, `_TRANSPORT`, `_UID`, `_PID`, `_SYSTEMD_UNIT`).
  - S015 explicitly mandates: `MESSAGE` is *"not supposed to be parsed for metadata"*, whereas `MESSAGE_ID` is a 128-bit identifier specifically designed for recognizing message types without text scraping.
- **Operability (C2)**:
  - Defense against spoofed journal entries: Any client process communicating via `sd_journal_send(3)` can supply arbitrary user fields, including `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`.
  - To prevent spoofed denial-of-service / false DRIFT attacks, probes must understand which fields are forgeable and how trusted underscore-prefixed fields (`_UID`, `_PID`, `_TRANSPORT`, `_SYSTEMD_UNIT`, `_BOOT_ID`) provide authoritative bounding.
  - Understanding JSON serialization rules in `journalctl`: non-unique fields and non-UTF8/binary payloads are serialized as JSON arrays or raw byte arrays, requiring robust parsing or field whitelisting via `--output-fields=`.

---

## 2. Pinned Source S015 Identity & Anchors

| Field | Value |
|---|---|
| **Registry ID** | `S015` (`corpus/SOURCES.md:21`) |
| **Source Title** | `systemd.journal-fields(7)` — Special journal fields |
| **Canonical URL** | `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html` |
| **Section Anchors** | `User Journal Fields` (`MESSAGE=`, `MESSAGE_ID=`); `Trusted Journal Fields` (`_BOOT_ID=`, `_TRANSPORT=`, `_UID=`, `_SYSTEMD_UNIT=`); `Address Fields` (`__CURSOR`, `__REALTIME_TIMESTAMP`) |
| **Local Manual Section** | `man 7 systemd.journal-fields` (systemd 261) |

---

## 3. User Journal Fields vs. Trusted Underscore Fields

### 3.1 User Journal Fields (`MESSAGE=`, `MESSAGE_ID=`, etc.)
- **Definition** (S015 `User Journal Fields`):
  > *"User fields are fields that are directly passed from clients and stored in the journal."*
  > *"Note that the journal service does not validate the values of any structured journal fields whose name is not prefixed with an underscore..."*
- **`MESSAGE=` Specification**:
  > *"The human-readable message string for this entry. This is supposed to be the primary text shown to the user. It is usually not translated (but might be in some cases), and is not supposed to be parsed for metadata."*
  - **Verdict on `MESSAGE`**: Parsing `MESSAGE` violates upstream design contract. It creates brittle probes subject to localization, wording revisions, and formatting drift.
- **`MESSAGE_ID=` Specification**:
  > *"A 128-bit message identifier ID for recognizing certain message types, if this is desirable. This should contain a 128-bit ID formatted as a lower-case hexadecimal string, without any separating dashes or suchlike. This is recommended to be a UUID-compatible ID, but this is not enforced, and formatted differently. Developers can generate a new ID for this purpose with systemd-id128 new."*
  - **Trust Boundary**: `MESSAGE_ID` is a **User Journal Field**. It is submitted by the logging application over the native journal socket (`sd_journal_send(3)`). The journal daemon does **not** validate that the client is authorized to emit a specific `MESSAGE_ID`.

### 3.2 Trusted Journal Fields (`_` Prefix)
- **Definition** (S015 `Trusted Journal Fields`):
  > *"Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly added by the journal and cannot be altered by client code."*
- **Key Trusted Fields**:
  - `_PID=`, `_UID=`, `_GID=`: Kernel-authenticated caller process credentials (obtained via `SO_PEERCRED` on the local socket). Note: entries originating from standard output/error redirection of forked processes reflect the parent process that initiated the connection to journald.
  - `_COMM=`, `_EXE=`, `_CMDLINE=`: Process identity inspected from `/proc` by `systemd-journald`.
  - `_SYSTEMD_CGROUP=`, `_SYSTEMD_UNIT=`, `_SYSTEMD_SLICE=`, `_SYSTEMD_USER_UNIT=`: Systemd service hierarchy determined by `systemd-journald` from the caller's cgroup path.
  - `_BOOT_ID=`: 128-bit kernel boot ID (`/proc/sys/kernel/random/boot_id`).
  - `_TRANSPORT=`: Transport mechanism by which the entry was ingested.
- **Address Fields (`__` Prefix)**:
  - `__CURSOR=`, `__REALTIME_TIMESTAMP=`, `__MONOTONIC_TIMESTAMP=`: Serialized addressing metadata added during formatting. Not stored fields; cannot be matched via `sd_journal_add_match(3)`.

---

## 4. `_BOOT_ID` & `_TRANSPORT` Mechanics

### 4.1 `_BOOT_ID=`
- **Specification**:
  > *"The kernel boot ID for the boot the message was generated in, formatted as a 128-bit hexadecimal string."*
- **Properties**:
  - Invariant per boot cycle; assigned by the kernel.
  - Automatically injected by `systemd-journald` for every entry.
  - Mandatory in `journalctl -o json --output-fields=...` output.
  - Enables grouping and isolating multi-boot journal records without parsing timestamps or relying on shell-level boot filters.

### 4.2 `_TRANSPORT=`
- **Specification**:
  > *"How the entry was received by the journal service. Valid transports are: `audit` (for those read from the kernel audit subsystem), `driver` (for internally generated messages), `syslog` (for those received via the local syslog socket), `journal` (for those received via the native journal protocol), `stdout` (for those read from a service's standard output or error output), `kernel` (for those read from the kernel)."*
- **Transport Security Significance**:
  1. `_TRANSPORT=kernel`: Ingested directly from `/dev/kmsg`. Cannot be generated by unprivileged userspace applications via `sd_journal_send`.
  2. `_TRANSPORT=journal`: Ingested via native Unix domain socket `/run/systemd/journal/socket`. Used for structured logging calls (`sd_journal_send`, `sd_journal_sendv`).
  3. `_TRANSPORT=stdout`: Ingested via stream socket attached to a unit's stdout/stderr. Subject to stream reconnection and line breaking (`_STREAM_ID=`, `_LINE_BREAK=`).
  4. `_TRANSPORT=driver`: Emitted by `systemd-journald` itself (e.g. rotation, missed messages notice `e9bf28e6e834481bb6f48f548ad13606`).

---

## 5. JSON Array Representation in `journalctl -o json`

According to `journalctl(1)` (`Output Options > json`):
1. **Scalar Default**: Field values are generally encoded as JSON strings.
2. **Exception 1 (Fields > 4096 bytes)**:
   > *"Fields larger than 4096 bytes are encoded as null values. (This may be turned off by passing --all...)"*
3. **Exception 2 (Non-unique fields → JSON Array of Strings)**:
   > *"Journal entries permit non-unique fields within the same log entry. JSON does not allow non-unique fields within objects. Due to this, if a non-unique field is encountered a JSON array is used as field value, listing all field values as elements."*
4. **Exception 3 (Binary / Non-UTF-8 bytes → JSON Array of Unsigned Numbers)**:
   > *"Fields containing non-printable or non-UTF8 bytes are encoded as arrays containing the raw bytes individually formatted as unsigned numbers."*
   - Example observed on host:
     `"MESSAGE": [27, 91, 49, 59, 51, ...]` (ANSI escape sequence encoded as array of byte integers `0..255`).

### Impact on JSON Consumers:
- A naive JSON parser expecting `entry["FIELD"]` to always be a string can crash or fail when encountering a list (either array of strings for multi-occurrence fields, or array of integer bytes for binary data).
- When filtering with `--output-fields=_BOOT_ID` or `--output-fields=MESSAGE_ID,_BOOT_ID`:
  - `_BOOT_ID` is strictly single, printable hexadecimal ASCII (always a JSON string).
  - `MESSAGE_ID` when present as a valid catalog ID is 32 lowercase hex characters (always a JSON string).
  - Eliminating `MESSAGE` via `--output-fields=` completely removes the primary source of large payloads, binary byte arrays, and multiline string expansions.

---

## 6. Spoofable ID Limits & Threat Model

### 6.1 What Can Be Spoofed?
- Any local user with write access to `/run/systemd/journal/socket` (which is world-writable, `0666`, on standard systemd systems) can run:
  ```bash
  python3 -c "import systemd.journal; systemd.journal.send('Fake notice', MESSAGE_ID='fe6faa94e7774663a0da52717891d8ef')"
  ```
  or use a raw datagram containing `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef\nMESSAGE=evil`.
- In an unauthenticated journal query (`journalctl MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`), this spoofed entry **will match**.
- A hostile or buggy userspace process could intentionally spam spoofed catalog `MESSAGE_ID`s to trigger artificial alerts or inflate error metrics.

### 6.2 What CANNOT Be Spoofed?
Client code **cannot** forge trusted underscore fields:
1. `_UID`: Assigned by `systemd-journald` from kernel socket credentials (`SO_PEERCRED`). An unprivileged user cannot set `_UID=0`.
2. `_PID`: Assigned from socket credentials.
3. `_SYSTEMD_UNIT` / `_SYSTEMD_USER_UNIT`: Derived by journald from `/proc/$PID/cgroup`. A process cannot masquerade as `user@1000.service` or `systemd-oomd.service` unless placed in that unit by systemd.
4. `_TRANSPORT`: Assigned based on the ingest socket/channel. A userspace datagram cannot set `_TRANSPORT=kernel`.
5. `_BOOT_ID`: Injected by journald matching current kernel boot.

### 6.3 Authentic Producer Verification Profiles

To verify whether a catalog `MESSAGE_ID` notice is authentic or a spoofed entry:

| Catalog Notice | Expected `MESSAGE_ID` | Authentic Producer Profile | Trusted Guard Fields |
|---|---|---|---|
| **Kernel OOM Unit Notice** | `fe6faa94e7774663a0da52717891d8ef` | `systemd` (PID 1 in `--system`, `systemd --user` in `--user`) | `_COMM=systemd`<br>`_PID=1` (for system scope) or `_SYSTEMD_USER_UNIT=init.scope`<br>`_TRANSPORT=journal` |
| **systemd-oomd Unit Notice** | `d989611b15e44c9dbf31e3c81256e4ed` | `systemd-oomd.service` | `_SYSTEMD_UNIT=systemd-oomd.service`<br>`_COMM=systemd-oomd`<br>`_UID=0` (or systemd-oomd dynamic uid) |
| **Coredump Notice** | `fc2e22bc6ee647b6b90729ab34a250b1` | `systemd-coredump` kernel helper | `_COMM=systemd-coredump`<br>`_UID=0`<br>`_TRANSPORT=journal` |
| **Direct Kernel OOM** | *(None; uses dmesg/kmsg text)* | Linux Kernel | `_TRANSPORT=kernel` |

### 6.4 Defensive Recommendations for Mori
1. **Scope Isolation**:
   - Query `--user` and `--system` independently.
   - For fleet health, mori focuses on the fleet user scope (`--user`).
2. **Primary Structured Filter**:
   - `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`
3. **Optional Spoof Guard**:
   - In environments where adversarial unprivileged processes might inject catalog IDs, supplement queries with `_COMM=systemd` (for PID 1 / systemd manager notices) or verify `_UID`.
4. **Field Restriction**:
   - Always pass `-o json --output-fields=_BOOT_ID` to prevent buffer bloating, suppress raw `MESSAGE` text, and avoid JSON array anomalies from multi-occurrence or binary message strings.

---

## 7. QUALITY Criteria Conformance

- **Criterion 1 & 2 (Falsifiable claims & measured anchors)**:
  - Man page citations: S015 `User Journal Fields` (`MESSAGE=`, `MESSAGE_ID=`), `Trusted Journal Fields` (`_BOOT_ID=`, `_TRANSPORT=`, `_UID=`, `_PID=`).
  - Empirical verification: Real entry retrieved from host journal (`_BOOT_ID=7bd93aee...`, `_COMM=systemd`, `_PID=1539`, `_TRANSPORT=journal`, `CODE_FILE=src/core/cgroup.c`).
- **Criterion 3 (Separate observation, inference, and unknown)**:
  - *Observed*: `MESSAGE_ID` is in the `User Journal Fields` section; fields without leading underscore are not validated by journald; underscore fields are added by journald from peer credentials/kernel; non-unique fields serialize as arrays; non-UTF8 fields serialize as integer arrays.
  - *Inference*: Any unprivileged process sending datagrams to the journal socket can emit an arbitrary `MESSAGE_ID`. Therefore, `MESSAGE_ID` alone is not cryptographically authentic, but can be authenticated when paired with trusted fields (`_COMM=systemd`, `_SYSTEMD_UNIT`, `_TRANSPORT`).
  - *Unknown*: Specific rate-limiting or datagram drop behavior under intentional multi-megabyte `MESSAGE_ID` flood on this host kernel without running a live stress test.
- **Criterion 15 (Count by MESSAGE_ID, never text)**:
  - Replaces regex parsing of `MESSAGE` with structured queries on `MESSAGE_ID`.
- **Criterion 16 (Unit naming & scope independence)**:
  - Documents independent scopes (`user` vs `system`), distinct semantics (unit notices vs victim kills), and forbids summing scopes.

---

## 8. Proposed Verification Checks for L1 Integration

```bash
# 1. Verify that MESSAGE is eliminated by --output-fields=_BOOT_ID
journalctl --user -n 1 -o json --output-fields=_BOOT_ID | jq -e 'has("MESSAGE")' | grep -q 'false'

# 2. Verify that _BOOT_ID and addressing metadata are always retained
journalctl --user -n 1 -o json --output-fields=_BOOT_ID | jq -e 'has("_BOOT_ID") and has("__REALTIME_TIMESTAMP")' | grep -q 'true'

# 3. Verify trusted transport of kernel vs journal messages
journalctl -k -n 1 -o json --output-fields=_TRANSPORT | jq -r '._TRANSPORT' | grep -q '^kernel$'

# 4. Verify authentic producer of fe6faa94 notices in user scope
journalctl --user -q MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_COMM,_TRANSPORT | jq -r '._COMM' | sort -u | grep -q '^systemd$'
```

---

## 9. Tooling Record

- **Tools installed/updated**: None. System standard tools (`man`, `journalctl`, `jq`, `python3`) were used exclusively.
