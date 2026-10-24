# ScoutDeadSeatCorrelation — round 27, wave 1 (read-only)

Seat: `MoriR27.ScoutDeadSeatCorrelation`. Question: within boot -1, do any fleet dead-seat
records fall near earlyoom sends, and which records' error text names a signal. Read-only: the only
lane write is this file. Tool installs or upgrades: none (existing `journalctl`, `python3`, `curl`).

## Answer

- Boot -1 is `3e7084f4…` from **2026-10-20T12:57:09.518Z to 2026-10-22T07:54:50.588Z**
  (`journalctl --list-boots -o json`; boot 0 starts 2026-10-22T07:55:41.626Z).
- The earlyoom unit logged **252 records and 39 send lines: 38 SIGTERM and 1 SIGKILL**, no
  `Suppressed … messages` line, no dry-run line, no whole-group line. This matches the round-26
  count (`corpus/lessons/round-26.md:22-24`).
- Dead-seat records written inside that window: **425 entries in 29 files** carrying
  `dead`/`dead_seats`/`deaths`/`deadSeats` lists, plus **288 seat-shaped entries in 43 files whose
  name marks dead-seat accounting**. Signal-language counts over both sets:
  - **23 records name SIGHUP** (all one host event, 2026-10-21T16:10:51Z);
  - **3 records say "killed" with no signal name** (host predecessor killed);
  - **33 further seats** (kaidoku round 19) have a cause text saying "killed" but name only a
    provider 429 — no signal;
  - **0 records name SIGTERM, 0 name SIGKILL, 0 name exit 143, 0 name exit 137.**
- **No dead-seat record falls within 60 s of a send line.** The closest dead-record file write is
  **339.6 s** from a send; the SIGHUP event is 32,487 s (9.02 h) from the nearest send.
- The send set is fleet-heavy by class label: **27 python, 1 omp, 11 other** (28/39 = 71.8 %), and
  **all 39 victims' `/proc` `oom_score_adj` read 200** at kill time. The largest burst (20 sends,
  `06:15:59–06:16:05Z` on 10-22) is **19 python + 1 omp**, and the fleet wrote no
  record at all in that span.

## Method

1. `journalctl --list-boots -o json --no-pager` for exact boot bounds (values above).
2. `journalctl -u earlyoom.service -b -1 -o json --output-fields=__REALTIME_TIMESTAMP,MESSAGE
   --no-pager` read into memory; only counts, hours and class labels printed. Send lines matched
   `sending SIG(TERM|KILL) to process`; the log line's 8th field is the process name
   (`kill.c:627-628`), cross-checked against the stricter regex
   `to process \d+ uid \d+ "<name>"` — both agree (27 python, 1 omp, 11 other).
3. Window file set: every file with mtime in the boot -1 span under
   `/home/vgpnk/Projects/shokunin/*/.ufo/waves` (depth 1–4) and `.ufo/reports` (depth 1–4) —
   **24,187 files**, of which **1,588** are round-root run/spec/report files (1,499 wave + 89 fleet
   reports). Driver: `find … -newermt @1792501029 ! -newermt @1792655690` where the two epochs are
   boot start and boot end.
4. Structured pass: JSON objects with `dead`/`dead_seats`/`deaths`/`deadSeats` lists, and every
   file whose name matches `dead[-_]?seat|deaths`; each seat's string fields tested for
   `SIGTERM|SIGKILL|SIGHUP|SIGABRT|SIGSEGV|SIGQUIT|SIGINT`, `\bkilled\b`, and
   `exit|status|code … 143|137`.
5. Text pass: every candidate file searched line-wise for death wording together with a signal
   token, and separately for exit/status 143/137 (69 and 38 lines respectively; all are docs,
   tests, mutation records or fixtures, none a dead-seat record).

## Hourly correlation (UTC, boot -1)

`dead entries` is assigned by the containing file's mtime — a write-time proxy, not the death
instant. `files` counts every scanned record file written in that hour.

| hour UTC | sends | send classes | dead entries | files |
|---|---|---|---|---|
| 10-20 13Z | 0 | - | 0 | 21 |
| 10-20 14Z | 0 | - | 0 | 41 |
| 10-20 15Z | 0 | - | 0 | 39 |
| 10-20 16Z | 1 | 1 other | 0 | 25 |
| 10-20 17Z | 3 | 3 other | 0 | 20 |
| 10-20 18Z | 2 | 2 other | 0 | 20 |
| 10-20 19Z | 0 | - | 1 | 46 |
| 10-20 20Z | 4 | 4 other | 44 | 36 |
| 10-20 21Z | 0 | - | 8 | 51 |
| 10-20 22Z | 1 | 1 other | 0 | 24 |
| 10-20 23Z | 0 | - | 0 | 11 |
| 10-21 00Z | 0 | - | 0 | 6 |
| 10-21 01Z | 0 | - | 0 | 4 |
| 10-21 02Z | 0 | - | 0 | 1 |
| 10-21 03Z | 0 | - | 0 | 5 |
| 10-21 04Z | 0 | - | 0 | 10 |
| 10-21 05Z | 0 | - | 0 | 22 |
| 10-21 06Z | 4 | 4 python | 1 | 66 |
| 10-21 07Z | 4 | 4 python | 0 | 58 |
| 10-21 08Z | 0 | - | 56 | 102 |
| 10-21 09Z | 0 | - | 43 | 50 |
| 10-21 10Z | 0 | - | 27 | 44 |
| 10-21 11Z | 0 | - | 1 | 63 |
| 10-21 12Z | 0 | - | 53 | 146 |
| 10-21 13Z | 0 | - | 82 | 138 |
| 10-21 14Z | 0 | - | 5 | 145 |
| 10-21 15Z | 0 | - | 1 | 116 |
| 10-21 16Z | 0 | - | 103 | 105 |
| 10-21 17Z | 0 | - | 0 | 67 |
| 10-21 18Z | 0 | - | 0 | 32 |
| 10-21 19Z | 0 | - | 0 | 8 |
| 10-21 20Z | 0 | - | 0 | 23 |
| 10-21 21Z | 0 | - | 0 | 22 |
| 10-21 22Z | 0 | - | 0 | 4 |
| 10-21 23Z | 0 | - | 0 | 13 |
| 10-22 01Z | 0 | - | 0 | 1 |
| 10-22 02Z | 0 | - | 0 | 3 |
| 10-22 06Z | 20 | 19 python, 1 omp | 0 | 0 |

Hours with no fleet write at all are omitted (10-22 00Z, 03Z–05Z, 07Z up to 07:54:50Z). The only
hours containing both sends and dead-seat writes are 10-20 20Z (4 sends, 44 entries) and 10-21 06Z
(4 sends, 1 entry).

Send times (39): 10-20 16:54:08, 17:04:59, 17:12:19, 17:27:19, 18:05:12 (SIGKILL), 18:59:56,
20:35:04, 20:49:25, 20:50:34, 20:51:06, 22:51:30; 10-21 06:05:25, 06:08:19, 06:26:10, 06:46:49,
07:04:43, 07:06:06, 07:07:24, 07:09:23; 10-22 06:15:59–06:16:05 (20 lines inside 6 s).
All boot -1 sends are process-scope; none is a whole-group send.

## Dead-seat records that name a signal

| Record set | Entries | Names SIGTERM/SIGKILL/143/137 | Names SIGHUP | Says "killed" only |
|---|---|---|---|---|
| `dead*` lists, 29 files | 425 | 0 | 23 | 3 |
| `*dead-seat*`/`*deaths*` files, 43 files | 288 | 0 | 23 | 0 |
| kaidoku round 19 missing-report seats | 42 (33 with "killed") | 0 | 0 | 33 |

- The 23 SIGHUP records are one event: `kengaku-shokunin/.ufo/waves/round-29/build-dead-seats.json:14`
  and `:23` (cause: host session killed by SIGHUP, 2026-10-21T16:10:51Z, session id omitted here).
  The same event's file-level record is
  `revenger-shokunin/.ufo/waves/round-61/falsify/dead-seats.json:4` (host end SIGHUP,
  2026-10-21T13:10:51−03:00) and `:7` (`"dead": 65`); its 65 per-seat `last_error` values say only
  "Request was aborted". Together those two files account for **88 seats from one host event**.
- The 3 "killed" records are
  `mado-shokunin/.ufo/waves/round-22/evidence/resume/seat-accounting.json:48,54,60`
  ("dead when predecessor host killed").
- The 33 "killed" causes are
  `kaidoku-shokunin/.ufo/waves/round-19/wave1-outcomes.json:73` and 32 sibling lines: "killed when
  the L1 session KaidokuR19 exited on an Anthropic 429". One session exit, no OS signal.
- Other lanes record the same SIGHUP event in prose (`.ufo/reports/round-22/souji.md:9`,
  `.ufo/reports/round-23/kama.md:14`, `.ufo/reports/round-24/tameshi.md:11`,
  `.ufo/reports/round-27/kagi.md:5`, `.ufo/reports/round-27/chousa.md:87`,
  `.ufo/reports/round-29/kengaku.md:140`); none attributes a seat death to earlyoom.
- Noise explicitly excluded: `.ufo/reports/round-18/souji.md:131` discloses a lane's own SIGKILL of
  four unowned processes (an action, not a dead seat); mori's census fixtures contain a literal
  `Out of memory: Killed process` stub (`.ufo/waves/round-17/frozen/mori-census.sh:3430`) with a fake
  pid. Neither is a fleet death record.

## 60-second proximity test

Using record timestamps where present and file mtime otherwise, against the 39 send instants:

| Dead-record time | Source | Nearest send | Gap |
|---|---|---|---|
| 10-21 06:31:49Z | `kagi-shokunin/.ufo/waves/round-24/final-verification.json:60-61` (1 seat, Codex rate limit at spawn) | 06:26:10Z | 339.6 s |
| 10-20 20:00:11Z | `tsukuroi-shokunin/.ufo/waves/round-17/falsify/outcome.json` | 20:35:04Z | 2,092.7 s |
| 10-20 19:35:09Z | `tsukuroi-shokunin/.ufo/waves/round-18/build/outcome.json` | 18:59:56Z | 2,112.6 s |
| 10-21 08:10:47Z | `kake-shokunin/.ufo/waves/round-23/residual-deaths.json` (`noticedAt`, explicit) | 07:09:23Z | 3,684 s |
| 10-21 16:10:51Z | the SIGHUP event (23 + 65 seats) | 07:09:23Z | 32,487 s |

**Result: zero records within 60 s, zero within 300 s; the minimum over all 29 dead-record files
and all explicit timestamps is 339.6 s.** The 20-send burst on 10-22 06:15:59–06:16:05Z has no
fleet record within 2.5 h: the last fleet write before it is `.ufo/reports/round-28/chousa.md` at
02:59:41Z, and the next records begin after boot 0 starts (07:55:41Z).

Caveat: mtime is a write-time proxy. A seat that died at T can be recorded at T+minutes in a file
written later, so a true 60 s co-occurrence could be hidden. The explicit timestamps available
(one SIGHUP event, two kake `noticedAt` values, one quota-reset value dated 2026-10-25) show no
send-time clustering either.

## Victim classes and oom_score_adj (counts only)

| boots | records | sends | classes |
|---|---|---|---|
| -4 | 0 | 0 | no records (unit not active or not yet installed) |
| -3 | 0 | 0 | no records (unit not active or not yet installed) |
| -2 | 8 | 0 | none |
| -1 | 252 | 39 | 27 python, 1 omp, 11 other |

- Boot -1 split: 11 sends on 10-20 are all `other`; 8 sends on 10-21 06–07Z are all `python`; the
  20-send burst on 10-22 06:16Z is 19 `python` + 1 `omp`. The single SIGKILL (10-20 18:05:12Z) hit
  class `other`.
- **Every one of the 39 send lines reported `oom_score_adj` 200.** That value is read from
  `/proc/<pid>/oom_score_adj` (`meminfo.c:191-194`, `kill.c:470`) and is not modified by earlyoom,
  so it is the victim's real value at kill time. This is victim-only evidence, not a host census;
  the census belongs to `SrcOmpBunOomAdj`/`HostUnitOomAdjust`.
- Do not reuse the logged `oom_score` field as a kernel score: `kill.c:405-421` adds ±300 to it for
  processes matching `--prefer`/`--avoid` (constants at `kill.c:24-32`), and the logged VmRSS can
  likewise carry ±3 GiB from the same branches. This seat therefore reports no score or RSS numbers.
- [INFERENCE] The 19 `python` + 1 `omp` victims of the 06:16 burst are consistent with the fleet's
  own runtime processes, because those names are the fleet's runtime class labels; no seat record
  ties any of those sends to a named seat, and the fleet wrote nothing between 02:59:41Z and the
  reboot, so the burst cannot be confirmed as a seat kill from lane records alone.

## Confidence and gaps

- High confidence: boot bounds, send count/hour/class table, dead-record inventories, the 60 s
  negative (two independent scans agree), the SIGHUP event identity.
- Medium: dead-entry counts are entries in accounting files, and some files re-list inherited seats
  (for example tameshi's round-21 `total.dead`), so 425 entries are not 425 unique deaths (402
  distinct lane+seat pairs).
- Unknown, not covered: records written after boot -1 (boot 0) about a boot -1 death, e.g. any
  post-reboot accounting of the 06:16 burst; in-memory seat deaths never written to a file; other
  senders (systemd-oomd, kernel OOM) — round 26 counted 0 systemd-oomd notices, and this seat did
  not re-count them. A spot check of the one boot-0 dead-seat-named file found by name
  (`kake-shokunin/.ufo/waves/round-31/w1/dead-seats.json`, dispatched 2026-10-22T15:54:40Z,
  18 seats) shows an error text with no signal token and no earlyoom reference.
- Privacy: no journal MESSAGE text, pid, uid, session id or session-store path is reproduced; class
  labels are the four allowed runtime names plus `other`; settings values are not reported.

## Commands run (read-only)

```sh
journalctl --list-boots -o json --no-pager
journalctl -u earlyoom.service -b -1 -o json --output-fields=__REALTIME_TIMESTAMP,MESSAGE --no-pager   # 252 records
journalctl -u earlyoom.service -b -2|-3|-4 -o json --output-fields=__REALTIME_TIMESTAMP,MESSAGE --no-pager
for w in /home/vgpnk/Projects/shokunin/*/; do
  find "$w.ufo/waves" -mindepth 1 -maxdepth 4 -type f -newermt @1792501029 ! -newermt @1792655690; done
find /home/vgpnk/Projects/shokunin/.ufo/reports -maxdepth 4 -type f -newermt @1792501029 ! -newermt @1792655690
```

Sources fetched on 2026-10-22 with `curl` (official tag bytes): `kill.c` (v1.9.0)
sha256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` — re-opens existing row
S118, anchor only, no new row; `meminfo.c` sha256
`526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb` and `procinfo.c` sha256
`d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` — fetched to interpret the log
fields, no SOURCES row claimed here. Scratch under `/fast/scratch/hyaku/mori-r27/ScoutDeadSeatCorrelation/`.
