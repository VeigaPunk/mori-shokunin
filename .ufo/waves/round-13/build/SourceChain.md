# SourceChain: S013, S014, S015, S031 Chain & Registry Transition Analysis

**Seat:** `MoriR13.SourceChain` (Connector)  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Milestone:** Round 13 structured scopes and verdict integrity  
**Assigned Deliverable:** `.ufo/waves/round-13/build/SourceChain.md`  
**Judged Axes:** Coverage (score 6), Operability (score 6)  
**Date:** 2026-10-20  

---

## 1. Godspeed Posture & Named Axes

In accordance with `/skill:godspeed`:
1. **Name the axes:**
   - **Coverage (C1):** Transitioning mori's journal inspection from fragile, un-scoped raw `MESSAGE` regex scraping (`c_oom`, `c_kill`, `c_seg`, `c_unit`) to structured, 128-bit `MESSAGE_ID` catalog matching (`fe6faa94e7774663a0da52717891d8ef`, `d989611b15e44c9dbf31e3c81256e4ed`, `fc2e22bc6ee647b6b90729ab34a250b1`) across explicitly separated `user` and `system` journal scopes, strictly suppressing `MESSAGE` text output via `-o json --output-fields=_BOOT_ID`.
   - **Operability (C2):** Preserving honest verdict grammar, exit code parity, and zero pipeline failures. Specifically repairing long-history SIGPIPE authorship loss (defect F01 / QUALITY 7) and eliminating invalid/forged verdicts in the silence oracle (defect F02 / QUALITY 26).
2. **Iterate cheap, in parallel:** Synthesized local repository evidence, primary sources (S013, S014, S015, S031), sibling reports (`CatalogSource.md`, `JournalSource.md`, `FieldsSource.md`, `PipeSource.md`, `PlanningWalk.md`, `PriorReview.md`, `ClaimConnections.md`, `FrontierConnection.md`), and round 12/13 lessons.
3. **Keep moves that improve any axis and harm none:** Advancing structured system-journal notice observation without pretending kernel OOM victim attribution or fleet causality are solved.
4. **Don't aim — let the frontier walk itself:** Truthfully separating what Round 13 settles (structured system/user unit notice counts) from what remains on the frontier (event-time kernel OOM attribution, `task_memcg` token extraction, and fleet task correlation).

---

## 2. Tooling Directive Record

In accordance with the operator tooling directive (2026-10-19):
- **Tools installed/updated by this seat:** None. (Inspection completed using built-in read-only file and search operations without altering host packages).
- **Referenced sibling seat tooling:** PipeSource recorded installation of `core/man-pages` (`6.19-1`) via `sudo pacman -S --needed --noconfirm man-pages` to inspect authoritative upstream `pipe(7)` documentation.

---

## 3. Deep Analysis of Registry Rows: S013, S014, S015, S031

### 3.1 Row S013: systemd Message Catalog (`systemd.catalog.in`)
- **Source Identifier:** `S013`
- **Source URL:** `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in`
- **Pinned Commit:** `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` (2026-10-19)
- **SHA-256 Digest:** `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592`
- **Kind / Tier:** `code` / Tier `A`
- **Scope & Anchors:**
  - `:66-77`: `fc2e22bc6ee647b6b90729ab34a250b1` — Subject: Process dumped core (`systemd-coredump(8)`). Program crash/abnormal termination notice. NOT an OOM kill.
  - `:604-617`: `fe6faa94e7774663a0da52717891d8ef` — Subject: A process of @UNIT@ unit has been killed by the OOM killer. Systemd notification of kernel OOM killer activity affecting a unit.
  - `:884-897`: `d989611b15e44c9dbf31e3c81256e4ed` — Subject: systemd-oomd killed one or more processes in unit @UNIT@. Userspace oomd termination notice.
- **What It Teaches:** The catalog provides stable 128-bit machine-typed keys for coredumps, kernel OOM unit notices, and oomd notices. Cardinality is strictly **non-1:1** with kernel victims (multi-unit fan-out across parent scopes and manager instances: measured 5 kernel kills vs 7 user + 9 system notices on boot `7bd93aee71144017b870212161a3dabf`).
- **Prior Round 12 State:**
  - `status`: `mined`
  - `used-by`: `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/userspace-oom-killers-r12.md`

### 3.2 Row S014: `journalctl(1)` Manual
- **Source Identifier:** `S014`
- **Source URL:** `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html`
- **Version:** systemd 262 (host installed: systemd 261, `261.2-1-arch`)
- **Kind / Tier:** `docs` / Tier `A`
- **Scope & Anchors:**
  - Filtering Options `#--after-cursor=`: Cursor-based forward pagination without re-reading historical streams.
  - Filtering Options `#-b`: Boot selection (`-b all` vs `-b 0`).
  - Output Options `#--output-fields=`: Comma-separated list of fields to include in output. Explicitly guarantees: `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, and `_BOOT_ID` are always printed for full-field modes (`json`), while `MESSAGE` is completely suppressed unless explicitly listed.
  - Exit Status `#Exit%20status`: Exit status returns `0` on success, non-zero on failure. Insufficient permissions on system journal yields `rc=1` (`No journal files were opened due to insufficient permissions`).
- **What It Teaches:** Probes must select explicit scopes (`--user` vs `--system` vs `-k`) and restrict output fields (`-o json --output-fields=_BOOT_ID`), ensuring no sensitive or arbitrary `MESSAGE` content is echoed, and gate on return codes to avoid masking permission failures as zero events.
- **Prior Round 12 State:**
  - `status`: `mined`
  - `used-by`: `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md`

### 3.3 Row S015: `systemd.journal-fields(7)` Manual
- **Source Identifier:** `S015`
- **Source URL:** `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html`
- **Version:** systemd 262
- **Kind / Tier:** `docs` / Tier `A`
- **Scope & Anchors:**
  - User Journal Fields `MESSAGE=`: Primary human-readable text shown to the user; explicitly *"not supposed to be parsed for metadata"*.
  - User Journal Fields `MESSAGE_ID=`: 128-bit message identifier for recognizing message types. Client-supplied via `sd_journal_send(3)`; unvalidated by journald daemon.
  - Trusted Journal Fields `_BOOT_ID=`: Kernel boot ID formatted as 128-bit hex string; immutable and trusted.
  - Trusted Journal Fields `_TRANSPORT=`: Transport mechanism (`kernel`, `journal`, `stdout`, `syslog`, `driver`, `audit`). `_TRANSPORT=kernel` comes from `/dev/kmsg` and cannot be forged by unprivileged userspace clients.
- **What It Teaches:** Distinguishes client-forgeable user fields (`MESSAGE_ID`) from immutable, daemon-authenticated trusted metadata fields prefixed with `_`. Clarifies that while `MESSAGE_ID` allows typed querying, it can be spoofed by unprivileged processes writing to `/run/systemd/journal/socket`; trusted underscore fields bound authorization.
- **Prior Round 12 State:**
  - `status`: `mined`
  - `used-by`: `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md`

### 3.4 Row S031: `pipe(7)` Linux Programmer's Manual
- **Source Identifier:** `S031`
- **Source URL:** `https://man7.org/linux/man-pages/man7/pipe.7.html`
- **Version:** Linux man-pages 6.19 (date 2026-07-10)
- **Kind / Tier:** `docs` / Tier `A`
- **Scope & Anchors:**
  - Section `I/O on pipes and FIFOs` paragraph 5: *"If all file descriptors referring to the read end of a pipe have been closed, then a write(2) will cause a SIGPIPE signal to be generated for the calling process."*
  - Section `Pipe capacity`: Default capacity 16 pages (65,536 bytes).
  - Section `PIPE_BUF`: Atomic write limit 4096 bytes.
- **What It Teaches:** Explains the physical kernel mechanism behind pipeline failure under `set -o pipefail`. An early-exiting reader (`grep -Fxq`, `head -n1`) closes the read end; any subsequent write by an upstream producer (`printf`, `sed`) generates `SIGPIPE` (141). Under `pipefail`, `141 ≠ 0` causes the shell pipeline to return 141, inverting `if` conditionals.
- **Prior Round 12 State:**
  - `status`: `queued`
  - `used-by`: `—`

---

## 4. Source-to-Note-to-SKILL/Coverage Mapping

The table below documents the end-to-end evidence trail connecting primary source rows to the new Round 13 knowledge notes, and forward to the operational claims in `SKILL.md` and `SCORECARD.md`:

| Source ID | Upstream Authority & Anchor | New Knowledge Note (`corpus/knowledge/`) | SKILL.md Section & Operational Anchor | Coverage / Operability Claim |
|---|---|---|---|---|
| **S013** | `systemd.catalog.in:66,604,884` (commit `cf8ebfc6`) | `structured-journal-scopes-r13.md` | `## Error patterns` line 30 (`journal kill/OOM class counts`), `## Decision table` line 17 (`Did something get killed?`) | **Claim C1 (Coverage):** Displaces raw text regexes (`grep -ciE 'Out of memory|oom-kill'`). Replaces text matching with exact 128-bit catalog IDs for core dumps (`fc2e22bc…`), kernel OOM unit notices (`fe6faa94…`), and oomd notices (`d989611b…`). Enforces `notice` units, never process kills. |
| **S014** | `journalctl(1)` systemd 262 (`--output-fields=`, `-b`, exit rc) | `structured-journal-scopes-r13.md` | `## Boundaries (hard)` lines 46-47; `## Secret-exposure exclusions` lines 143-157 | **Claim C1 (Coverage) & C2 (Operability):** Eliminates `MESSAGE` exposure by invoking `-o json --output-fields=_BOOT_ID`. Mandates rc checks: insufficient permission on `--system` returns rc 1 and must yield `unavailable`, never `0` kills (QUALITY 6/24). |
| **S015** | `systemd.journal-fields(7)` systemd 262 (`MESSAGE=`, `MESSAGE_ID=`, `_TRANSPORT=`) | `structured-journal-scopes-r13.md` | `## Error patterns` line 30; `## Secret-exposure exclusions` line 157 | **Claim C1 (Coverage):** Distinguishes user metadata (`MESSAGE_ID`) from unparsed display text (`MESSAGE`). Establishes trust boundaries: `MESSAGE_ID` is client-supplied; trusted underscore fields (`_TRANSPORT`, `_BOOT_ID`, `_SYSTEMD_UNIT`) prevent spoofed event inflation. |
| **S031** | `pipe(7)` man-pages 6.19 (`I/O on pipes and FIFOs`, `SIGPIPE` 141) | `verdict-contract-r13.md` | `## Checklist (executable)` lines 53-56; `## Error patterns` (pipeline safety) | **Claim C2 (Operability):** Solves defect F01 in `tools/mori-census.sh:1494`. Proves why streaming 12,000 commits into `sed | grep -Fxq` raises SIGPIPE (141) under `pipefail`, wrongly downgrading active lane to `progressing-weak`. Grounds the capture-first / here-string fix. |

---

## 5. Allowed Source Registry Changes (Contract v1 Rule 1)

Under the strict contract governing `corpus/SOURCES.md`, leaf seats and connectors are permitted to propose mutations **only** to the mutable cells (`status` and `used-by`) for existing rows. No row IDs may be inserted out-of-order, no tiers may be inflated, and no recheck policies or URLs may be modified.

### Concrete Recommendations for `corpus/SOURCES.md` Table:

#### 1. Row S013
- **id:** `S013`
- **Field `status`:**
  - Old: `mined`
  - New: `mined` (unchanged)
- **Field `used-by`:**
  - Old: `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/userspace-oom-killers-r12.md`
  - New: `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/userspace-oom-killers-r12.md, corpus/knowledge/structured-journal-scopes-r13.md`
- **Justification:** Reopened and actively cited by the new Round 13 note on structured journal scopes.

#### 2. Row S014
- **id:** `S014`
- **Field `status`:**
  - Old: `mined`
  - New: `mined` (unchanged)
- **Field `used-by`:**
  - Old: `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md`
  - New: `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md`
- **Justification:** Reopened and actively cited for field suppression (`--output-fields=_BOOT_ID`) and scope isolation in Round 13.

#### 3. Row S015
- **id:** `S015`
- **Field `status`:**
  - Old: `mined`
  - New: `mined` (unchanged)
- **Field `used-by`:**
  - Old: `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md`
  - New: `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md`
- **Justification:** Reopened and actively cited for user field vs trusted metadata distinctions in Round 13.

#### 4. Row S031
- **id:** `S031`
- **Field `status`:**
  - Old: `queued`
  - New: `mined` (promoted upon first consumption in a committed knowledge note)
- **Field `used-by`:**
  - Old: `—`
  - New: `corpus/knowledge/verdict-contract-r13.md`
- **Justification:** Opened by PipeSource and HistoryKnowledge; first consumed in `verdict-contract-r13.md` to ground the F01 SIGPIPE mechanism. Promoted from `queued` to `mined` per contract rules.

### Summary Diff for Source Registry Rows:

```diff
--- a/corpus/SOURCES.md
+++ b/corpus/SOURCES.md
@@ -19,9 +19,9 @@
-| S013 | systemd message catalog — https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | code | A | systemd message identifiers for coredumps, kernel OOM and systemd-oomd kills | catalog/systemd.catalog.in:66,604,884; systemd main commit cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af (2026-10-19) | The catalog gives distinct stable MESSAGE_ID values to core dumps, kernel OOM notices and oomd notices. | mined | 2026-10-19 | on-release | corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/userspace-oom-killers-r12.md |
+| S013 | systemd message catalog — https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | code | A | systemd message identifiers for coredumps, kernel OOM and systemd-oomd kills | catalog/systemd.catalog.in:66,604,884; systemd main commit cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af (2026-10-19) | The catalog gives distinct stable MESSAGE_ID values to core dumps, kernel OOM notices and oomd notices. | mined | 2026-10-19 | on-release | corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/userspace-oom-killers-r12.md, corpus/knowledge/structured-journal-scopes-r13.md |
-| S014 | journalctl(1) — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | docs | A | journal source selection, cursor pagination and field-limited JSON output | Source Options; Filtering Options --after-cursor:187-190; Output Options --output-fields:489-492; systemd 262 man page opened 2026-10-19 | Select journal scope and cursor bounds, and request only structured fields for count-only queries. | mined | 2026-10-19 | on-release | corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md |
+| S014 | journalctl(1) — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | docs | A | journal source selection, cursor pagination and field-limited JSON output | Source Options; Filtering Options --after-cursor:187-190; Output Options --output-fields:489-492; systemd 262 man page opened 2026-10-19 | Select journal scope and cursor bounds, and request only structured fields for count-only queries. | mined | 2026-10-19 | on-release | corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md |
-| S015 | systemd.journal-fields(7) — https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | docs | A | journal MESSAGE, MESSAGE_ID and trusted metadata fields | User Journal Fields > MESSAGE=:32-39 and MESSAGE_ID=:41-44; Trusted Journal Fields > _TRANSPORT=:204; systemd 262 man page opened 2026-10-19 | MESSAGE is display text rather than metadata; MESSAGE_ID is the typed key and underscore-prefixed fields are trusted. | mined | 2026-10-19 | on-release | corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md |
+| S015 | systemd.journal-fields(7) — https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | docs | A | journal MESSAGE, MESSAGE_ID and trusted metadata fields | User Journal Fields > MESSAGE=:32-39 and MESSAGE_ID=:41-44; Trusted Journal Fields > _TRANSPORT=:204; systemd 262 man page opened 2026-10-19 | MESSAGE is display text rather than metadata; MESSAGE_ID is the typed key and underscore-prefixed fields are trusted. | mined | 2026-10-19 | on-release | corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md |
...
-| S031 | pipe(7) — https://man7.org/linux/man-pages/man7/pipe.7.html | docs | A | pipe write behavior when readers close and SIGPIPE generation | I/O on pipes and FIFOs; man-pages 6.19, fetched 2026-09-09 | When all pipe read ends close, a write generates SIGPIPE; that pipe behavior explains a producer failure after an early-exiting consumer. | queued | 2026-10-19 | on-release | — |
+| S031 | pipe(7) — https://man7.org/linux/man-pages/man7/pipe.7.html | docs | A | pipe write behavior when readers close and SIGPIPE generation | I/O on pipes and FIFOs; man-pages 6.19, fetched 2026-09-09 | When all pipe read ends close, a write generates SIGPIPE; that pipe behavior explains a producer failure after an early-exiting consumer. | mined | 2026-10-19 | on-release | corpus/knowledge/verdict-contract-r13.md |
```

---

## 6. Risks, Boundaries, and Second-Order Effects

1. **Second-Order Risk: Drift Pin Baseline Invalidation:**
   - When C1 modifies `SURFACE journal` field names (from `oom_kill=` text matches to `notice_user_oom=`, `notice_system_oom=`), running `--drift` against `baseline-r10-20261015T2231Z.json` will detect non-volatile key changes (`-oom_kill`, `+notice_user_oom`, `+notice_system_oom`).
   - *Mitigation:* Ensure `DRIFT_COUNTER_KEYS` in `tools/mori-census.sh` is updated to include the new structured notice counter keys. Freshness re-pin is intentionally deferred to avoid disguising semantic changes as pure noise.
2. **Cardinality Disconnect Boundary (Notice ≠ Kill):**
   - The census must never sum `notice_user_oom` and `notice_system_oom` into an aggregate number. A single kernel OOM event can fan out to both user and system unit notices.
   - S013 text explicitly notes memory pressure might not have been caused by the unit receiving the notice. Host notice counts cannot prove fleet blame.
3. **Execution Safety Boundary:**
   - As a leaf connector seat, `MoriR13.SourceChain` executes no builds, no test suites, no gate verifications, and modifies no shared runtime code. All verification is deferred to the canonical planner (L1) at integration.
