# ScoutHostJournal — C2 live-data reconnaissance (read-only)

Seat `MoriR26.ScoutHostJournal`, round 26, wave 1. Read-only host survey of earlyoom and
systemd-oomd journal data for the C2 tool (`tools/mori-oom-killers.py`) and its case file.
No lane writes outside this report; scratch under `/fast/scratch/hyaku/mori-r26/ScoutHostJournal/`.
No tools installed or upgraded (nothing needed: `curl`, `journalctl`, `python3`, `getfacl` already present).
No unit, journal, config, OMP or fleet state touched. No LSP server exists for this question (host
runtime data plus static upstream source), so source facts are line-anchored against the fetched
tag bytes; no `lsp` device is in this seat's tool inventory.

Access date for every upstream URL: **2026-10-22**.

## 1. Retained boots

`journalctl --list-boots | wc -l` → `7` (one header line, so 6 boots).

| Idx | Boot ID (prefix) | First entry | Last entry |
|---|---|---|---|
| -5 | `be045967` | 2026-10-19 18:55:14 -03 | 2026-10-19 22:47:26 -03 |
| -4 | `430d3038` | 2026-10-19 22:48:24 -03 | 2026-10-20 06:37:07 -03 |
| -3 | `84755511` | 2026-10-20 06:37:55 -03 | 2026-10-20 08:54:20 -03 |
| -2 | `ed8819b0` | 2026-10-20 08:58:00 -03 | 2026-10-20 09:56:15 -03 |
| -1 | `3e7084f4` | 2026-10-20 09:57:09 -03 | 2026-10-22 04:54:50 -03 |
| 0 | `6a7f4fdf` | 2026-10-22 04:55:41 -03 | 2026-10-22 10:14:14 -03 |

Journal on disk: `journalctl --disk-usage` → `Archived and active journals take up 86.4M`.
Package `earlyoom 1.9.0-1`, Install Date `Tue 20 Oct 2026 09:16:28 AM -03` (`pacman -Qi earlyoom`).
Boots -5..-3 predate the install and hold **zero** earlyoom records; the first earlyoom version line
in retention is boot -2 at `2026-10-20 09:20:41.150162 -03` (4 min after install). The
`2026-10-22 04:55:44` stamp in the wave framing is the **current invocation's** start (boot 0 version
line `04:55:44.094371 -03`), not the first activation: an entry must say "active and enabled", not
"active since 2026-10-22".

## 2. Per-boot grammar census

Command per boot: `journalctl -q -b <idx> -u earlyoom.service -o json --output-fields=MESSAGE,__MONOTONIC_TIMESTAMP`,
one JSON object per line, classified in memory with `python3` (contract.md:80-94 classes, prefix-anchored
after `lstrip()`). Counts only; no MESSAGE text was retained or printed.

| Boot | total | version | term_thr | kill_thr | SIGTERM act | SIGKILL act | escalation | kill_failed | lowmem_SIGTERM | lowmem_SIGKILL | dryrun | unclassified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| -5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| -4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| -3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| -2 | 8 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 |
| -1 | 252 | 1 | 1 | 1 | 38 | 1 | 0 | 0 | 39 | 1 | 0 | 170 |
| 0 | 13 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |

`unclassified` decomposes into families (no text emitted): boot 0 = 2 filter echoes + 1 `mem total:` +
6 `mem avail:` + 1 unit lifecycle; boot -2 = 2 + 1 + 1 + 1; boot -1 = 2 + 1 + 83 + 39 `kill_release:` +
39 `process N exited` + 1 `memory situation has recovered…` + 5 unit lifecycle.

Cross-checks on the only boot with actions (-1): actions 38+1 = 39, `kill_release:` 39, `process N exited` 39,
low-memory warnings 39+1 = 40, of which one did not kill (the `…recovered while selecting victim` line).
Zero escalation and zero failed kills: the single SIGKILL was a first-signal kill at the SIGKILL limits.

Byte-array `MESSAGE` values: 0 of 273 records in retention (the decoder path is not exercised by live data).

Exact numbers: 273 earlyoom-unit records total across the 6 retained boots; 88 classified, 185 unclassified.

## 3. Scope clock (assignment item 3)

`systemctl show earlyoom.service -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic`
→ `loaded / active / enabled / ActiveEnterTimestampMonotonic=19964362` (µs), `InvocationID=04ce630c…`,
which matches the boot-0 earlyoom records' `_SYSTEMD_INVOCATION_ID`.

| Clock mark, boot 0 | `__MONOTONIC_TIMESTAMP` (µs) | delta vs ActiveEnter |
|---|---|---|
| `ActiveEnterTimestampMonotonic` | 19964362 | 0 |
| systemd's own `Started earlyoom.service` record (first in-scope record) | 19964370 | **+8 µs** |
| first earlyoom-identifier record (the version line) | 19981126 | **+16 764 µs (16.764 ms)** |

Same clock, yes: `__MONOTONIC_TIMESTAMP` is boot-relative CLOCK_MONOTONIC in µs, and systemd's own
start record lands 8 µs after the ActiveEnter stamp it was derived from. The +8 µs record is *inside*
the scope and is not the version line, so `scope_complete` must be a membership test ("the version
line is in scope"), not "the first in-scope record is the version line".

Across the three boots with earlyoom, the version line trails systemd's start record by 16.8 ms (boot 0),
17.1 ms (boot -1: 14892353 − 14875281) and 28.6 ms (boot -2: 1379176757 − 1379148147).

Unit shape (`systemctl cat earlyoom.service`): `[Service]` has **no `Type=`** → systemd default
`Type=simple`, so ActiveEnter is stamped at exec and the version line necessarily follows it.
`Restart=always` is present (line 18), so a restart in one boot creates a second invocation and moves
the bound forward; no restart was observed in retention (one invocation per boot). [INFERENCE] With
`Type=notify` the bound would move after the version print and `scope_complete` would be false on a
healthy host — the current answer depends on the unit staying `Type=simple`.

Inactive reference: `systemctl show systemd-oomd.service` → `inactive / disabled /
ActiveEnterTimestampMonotonic=0`. An inactive unit therefore has bound 0, which makes the whole boot
in scope; `scope_complete` then reduces to "a version line survives in retention".

## 4. Journal access without sudo (assignment item 4)

`id -nG` membership test: **`wheel` present, `systemd-journal` absent.** Reads succeeded without sudo:
every `journalctl` call above returned rc 0 and non-empty output for boots -2..0. Mechanism:
`getfacl -p /var/log/journal` shows `group:wheel:r-x` (and `group:adm:r-x`) on a
`root:systemd-journal` directory. [INFERENCE] A user in neither `systemd-journal` nor `wheel` (nor
`adm`) gets an unreadable journal; `journalctl` then exits non-zero, which the tool must map to
`null` inputs → `KILLERS_UNKNOWN`, never to zero counts.

## 5. systemd-oomd notices (assignment item 5)

`journalctl -q -b <idx> MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID`
— whole journal, not unit-filtered — returned **0 lines in every retained boot** (-5..0).
Local catalog: `journalctl --list-catalog d989611b…` →
`d989611b15e44c9dbf31e3c81256e4ed systemd: systemd-oomd killed one or more processes in unit @UNIT@`.
Upstream: `sd-messages.h:195` `#define SD_MESSAGE_UNIT_OOMD_KILL SD_ID128_MAKE(d9,89,61,1b,15,e4,4c,9d,bf,31,e3,c8,12,56,e4,ed)`.
One notice means "one or more processes in a unit", so `notices_this_boot` counts events, not kills.

## 6. Host-observed grammar facts

The three fixed-format startup lines, verbatim from boot 0's current invocation (the only MESSAGE text
quoted anywhere in this report):

```
earlyoom 1.9.0
sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,
        SIGKILL when mem avail <=  5.00% and swap free <=  5.00%
```

Observed consequences:

1. **Width padding.** `msg.h:10` `#define PRIPCT "%5.2lf%%"`, so a one-digit percent renders as
   ` 5.00%` — two spaces after `<=`. The term line passes a single-space pattern only because `10.00`
   fills the five columns. A host with `--term 5` would fail exactly like the kill line does today.
   Sibling seats already accept this padding (`BuildOomKillersTool.md:114-116`,
   `WriteOomKillersCases.md:72,158`); my data is the live confirmation.
2. **The two threshold lines are separate journal records**, not one multi-line MESSAGE: each `fprintf`
   (`main.c:414`, `main.c:416`) becomes its own entry. The kill record carries 8 leading spaces
   (the format string's indentation), so `lstrip()` is required but sufficient. Kill-threshold records
   observed: 1 per invocation in all three boots — the class is real and must be parseable after the pad.
3. **Action line** `kill.c:627`: `warn("sending %s to process %d uid %d \"%s\": oom_score …")` — the
   literal prefixes `sending SIGTERM to process ` / `sending SIGKILL to process ` hold. The `sig == 0`
   startup self-test prints `sending 0 (no-op signal) to process …` and must not match either prefix.
4. **Not in the contract grammar, present live:** `kill_release: pid=…: process_mrelease … success`
   (`kill.c:253,255`), `process %d exited after %.3f seconds` (`kill.c:329`), `process %d did not exit`
   (`kill.c:338`), `mem total:` once per start (`main.c:412`), `mem avail:` hourly (`meminfo.c:279`),
   two filter echoes, and systemd's own unit-lifecycle records (1 per boot, 5 in the boot where the
   unit stopped). On boot 0 the `mem total:` record and the first `mem avail:` record sit 2.7 ms apart at
   startup, then `mem avail:` repeats every 3600.3 s (6 records, 5 intervals).
5. **Near-miss for positive evidence:** `memory situation has recovered while selecting victim`
   (`main.c:537`, quoted from source) appeared once on boot -1, exactly at a low-memory warning that
   produced no kill (one journal record equals the source literal byte-for-byte, 53 chars). It is
   pressure evidence, not action evidence; it must stay unclassified and must not turn a quiet verdict
   into acted.
6. **Journal field behaviour:** `journalctl -o json --output-fields=MESSAGE` still emits
   `__MONOTONIC_TIMESTAMP` (plus `__REALTIME_TIMESTAMP`, `__CURSOR`, `__SEQNUM`, `_BOOT_ID`), so the
   contract's live collection command yields the scope field without naming it. systemd lifecycle records
   carry no `_SYSTEMD_INVOCATION_ID`; the earlyoom records do (one per boot here).

## 7. What this means for the tool

**Scope rule.** The stated bound (`__MONOTONIC_TIMESTAMP ≥ ActiveEnterTimestampMonotonic`) selects the
current invocation correctly on this host and excludes prior invocations after a restart, because
ActiveEnter moves forward on each activation and journald's monotonic values are boot-relative. Three
refinements the data supports:

- `scope_complete` must test membership of the version line, not first-ness: the `Started` record is
  8 µs inside the bound and precedes the version line by ~17 ms.
- An inactive unit (`ActiveEnterTimestampMonotonic=0`, as observed on systemd-oomd) puts the whole boot
  in scope. That is harmless under contract rule 1 (positive evidence stands) but means "inactive" does
  not imply "no actions this boot"; `actions` is an invocation-horizon number while
  `notices_this_boot` is a boot-horizon number — the output should not imply otherwise.
- Never mix boots: monotonic stamps are per-boot, so reading `-b -1` while in boot 0 and comparing to the
  current ActiveEnter is meaningless. The contract's current-boot-only collection is the right boundary.

**"quiet" versus "unknown".** With the corrected padding, boot 0 today is a clean `KILLERS_QUIET`:
`scope_complete` true (version line +16.8 ms inside), grammar verified (both threshold records present,
`10.00/10.00/5.00/5.00`), all action counters zero, oomd inactive with 0 notices. That quiet is
*informative*, not an artifact of missing data: the in-scope journal is non-empty (13 records, hourly
`mem avail:` lines through five hours), so silence is the killer's silence.

The failure modes the data makes concrete:

- **False unknown (highest risk, already handled by siblings):** with a single-space threshold pattern,
  the kill line on this very host fails to classify. If `grammar` then reads `unverified`, contract
  rule 2 returns `KILLERS_UNKNOWN` on a healthy quiet host. The host-shaped cases must include the
  double-space `5.00` line *and* a `10.00` line, and the parser must use `\s+` after `<=`.
- **False unknown #2:** treating `thresholds: null` because the kill record is absent from scope. Both
  records carry the *same* `__MONOTONIC_TIMESTAMP` at startup (boot 0: both `19981234`, 108 µs after the
  version line; boot -1: both `14892457`, 104 µs after it), so in a complete scope they always co-occur;
  absence means an incomplete scope, not a missing feature. Equal stamps also mean no ordering between
  the two records can be assumed.
- **False quiet:** an empty in-scope journal. Boots -5..-3 are genuinely empty (unit not yet installed),
  so this shape exists in the wild. Rule 2 already covers it via `scope_complete=false`; an
  implementation that skips the version-line test would report quiet on those boots.
- **False acted:** any loose `sending \w+ to process` pattern counts the `0 (no-op signal)` self-test as
  a kill. Keep the two literal prefixes.
- **Privacy:** the live inputs do contain the two filter-echo records, i.e. the `--avoid`/`--prefer`
  expressions, plus action lines with names, uids and cmdlines. `--dump-inputs` must stay redacted as
  the tool seat already specifies (`BuildOomKillersTool.md:184-188`); never echo raw `MESSAGE`.

## 8. Residual unknowns / not run

- Restart-in-boot behaviour is [INFERENCE]: reproducing it needs a unit restart, which this seat must not
  perform. The `Restart=always` + forward-moving ActiveEnter reasoning is from unit semantics, not observed.
- The emitter of `SD_MESSAGE_UNIT_OOMD_KILL` was not located in the fetched `oomd.c`, `oomd-util.c`,
  `oomd-manager.c` or `core/unit.c`; the ID, its v262 name and the local catalog text are confirmed, the
  call site is not. Low value for C2 (counts only).
- A permission-denied journal read could not be exercised (no non-`wheel` account available); the ACL is
  the evidence, and the mapping "read failure → null → UNKNOWN" is [INFERENCE] from contract.md:99.
- No live `--inputs` object was produced here; that is the tool seat's receipt, not this seat's.

## 9. Upstream bytes fetched (all 2026-10-22, `curl -fsSL`)

| URL | sha256 |
|---|---|
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c` | `526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb` |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/systemd/sd-messages.h` | `fb613f71807344eb29b9353cad8c09cb644fff4a18b1651fda9b49e0a23064fc` |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c` | `2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a` |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd.c` | `d674980745dcbe30a18a4bcfb62d5cab4e0daff9e3b0a0d1c0f19dd1ce2fc6a1` |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.c` | `052f19b36d54997b78c4ca93fae17d8c8513ce7240b0b58a47a1efdad0da3a15` |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c` | `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7` |
