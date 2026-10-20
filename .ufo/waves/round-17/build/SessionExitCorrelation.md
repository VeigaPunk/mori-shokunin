# SessionExitCorrelation — terminal message class × last `session_exit` record

Seat: `MoriR17.SessionExitCorrelation-5` (leaf, advisory; no subagent dispatch, no VCS mutation).
Question (verbatim): *In the 12-57-31 session dir, cross-tabulate the terminal message class
(contract.md) with the last `session_exit` record's data.reason/kind (custom records) per file.
Does any error-terminal seat show a normal exit, or any stop-terminal seat lack session_exit?
Counts only.*

## Scope and snapshot

- Sessions dir:
  `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07`
  (recursive: 109 top-level `*.jsonl` + 24 lane subdirs + `url-search`/`local` with no `*.jsonl`).
- Corpus is **live**: seats append while this ran. Pinned snapshot window
  **T0 = 2026-10-20T18:58:49.194Z … T1 = 18:58:54.205Z**, **2509** `*.jsonl` files, each read
  once, bytes parsed in one pass (so per-file counts and classes are mutually consistent).
- Requires a re-read to reproduce; counts move minute to minute. Drift measured across two
  passes is reported below and is itself part of the finding.

## Method

- Terminal class: exact replica of `contract.md` C1 rules on the **last** `type=="message"`
  record with a dict `message`: `completed` (assistant/`stop`), `aborted`
  (assistant/`aborted`), `dead_rate_limit` (assistant/`error` and `errorStatus==429` or an
  errorMessage class token `429|rate_limit|Rate limit|RATE_LIMITED|resource_exhausted`),
  `dead_quota` (next, `quota|usage limit|402|credits`), `dead_error_other`, `incomplete`
  (role `toolResult`/`user` or any other assistant stopReason), `unavailable` (no message
  record).
- Exit side: the **last** `type=="custom"`, `customType=="session_exit"` record in the same
  file; fields read `data.reason`, `data.kind` only (plus, for the counts below,
  `errorStatus`, the contract's errorMessage class tokens and `(type=NNNN)` digits — no text,
  content or usage was read or printed).
- Full-file scan, not the C1 tail window, for both sides; the tail-window consequence is
  quantified separately (see "Tail-window caveat").

## Cross-tabulation (pinned snapshot, 2509 files)

Exit records found: **2428** records over **2375** files. Exit-record values observed:
`kind` = `normal` **2428/2428**; `reason` = `dispose` **2428/2428**; any other kind **0**;
any other reason **0**. (So the reason/kind axis is constant — the cross-tab collapses to
presence/absence.)

| terminal class | files | last `session_exit` present | …`kind=normal`,`reason=dispose` | no `session_exit` |
|---|---:|---:|---:|---:|
| `completed`   | 2197 | 2122 | 2122 | **75** |
| `aborted`     |   80 |   80 |   80 | 0 |
| `dead_rate_limit` | 166 | 166 | 166 | 0 |
| `dead_quota`  |    2 |    2 |    2 | 0 |
| `dead_error_other` | 0 | 0 | 0 | 0 |
| `incomplete`  |   64 |    5 |    5 | 59 |
| `unavailable` |    0 |    0 | 0 | 0 |
| **total**     | **2509** | **2375** | **2375** | **134** |

Exit-record multiplicity per file: 0 → 134 files, 1 → 2330, 2 → 37, 3 → 8 (max 3).
Records that are the file's **final** record: 2371 of 2428 (2375 files minus the 4
resume cases below).

## Answers (counts)

1. **Error-terminal seat showing a normal exit: YES — 168 of 168 (100%).**
   `dead_rate_limit` 166/166 and `dead_quota` 2/2. In every one of the 168 the `session_exit`
   is `{"reason":"dispose","kind":"normal"}` **and** is the file's final record, positioned
   after the terminal error message. Example:
   `KaidokuR17/KaidokuR17.PinsAttack.jsonl` — 0-based non-empty record #84 is the terminal
   `message` (`stopReason=error`, `errorStatus=429`, provider `devin`/`swe-2`), record #85 is
   `session_exit` `normal`/`dispose`.
   Dead-seat field aggregates (contract fields only): `errorStatus` 429 → 153, null → 15;
   `Retry budget exhausted…` prefix → 119; `(type=1302)` → 122, no code → 46.
   By provider/model: zai/glm-5.3-flash 122, anthropic/claude-opus-5-5 24, devin/swe-2 13,
   anthropic/claude-haiku-5-5 6, devin/gpt-6-1-sol 2 (quota), cursor/claude-haiku-5-5 1.
2. **Stop-terminal seat lacking `session_exit`: YES — 75 of 2197 `completed` (3.4%).**
   All 75 are open/in-flight: 16 mtime ≤ 1 min, 59 ≤ 10 min before snapshot, none older than
   7 min. Lanes: KamaR17 40, MoriR17 34, MadoR19 1. Example:
   `KamaR17/KamaR17.AppendOnlyDocs.jsonl` — 64 records, last message `assistant`/`stop`,
   zero `session_exit`.
3. Bonus counts on the same axis: `aborted` shows a normal exit **80/80** even though the
   terminal record is `stopReason=aborted`. `incomplete` shows an exit in **5/64** — those 5
   have a `session_exit` written *after* a `toolResult`/`user` terminal record (e.g.
   `SoujiR16/SoujiR16.SentinelCensusFinal-4.jsonl` message #38, exit #39), i.e. dispose can be
   recorded mid-turn.

## Falsifiers of "session_exit marks the end of a seat"

- **4 files have message records after the last `session_exit`** (exit record is not terminal;
  the seat resumed after dispose):
  `MadoR19/MadoR19.GateFreshJj.jsonl` (exit #509, last message #569, 3 exits),
  `SoujiR17-3.jsonl` (exit #466, message #511, class `incomplete`),
  `TabiR18.jsonl` (exit #102, message #120, `incomplete`),
  `TameshiR17/TameshiR17.RR7-2.jsonl` (exit #86, message #147, size 1.07 MB).
- **Multi-exit:** 45 files hold 2–3 `session_exit` records (37 files ×2, 8 ×3); all identical
  `normal`/`dispose`. "The last" exit is therefore a per-file choice, and earlier ones are
  historical.
- **Drift across two passes ~2 min apart** (18:56:5x → 18:58:5x, 2508 → 2509 files):
  34 seats flipped `incomplete → completed`; 56 files gained exactly one `session_exit`
  (presence only, never lost); `0` seats moved out of `dead_rate_limit`/`dead_quota` and `0`
  out of `completed` in that window; total no-exit files fell 190 → 134 while
  `completed`-without-exit rose 48 → 75 (new turns finish faster than sessions dispose).
- **Tail-window caveat:** with the C1 default `--max-tail-bytes 262144`, the *last* exit record
  falls outside the tail in **3 of 2375** files (`MadoR19.GateFreshJj.jsonl`,
  `SoujiR17-3.jsonl`, `TameshiR17.RR7-2.jsonl`) — all large, all resumed. A tail-only reader
  would report those three as having no `session_exit` at all.
  By contrast, on the terminal-**message** side the 256 KiB tail changed the class of
  **0 of 2509** files versus a full-file scan (both passes).

## Reading for C1 (advisory, not a verdict)

- `data.kind`/`data.reason` of `session_exit` are **constant** (`normal`/`dispose`) across all
  2428 records in this corpus: they record process disposal, not outcome. They cannot
  discriminate completion from rate-limit death, and must not be used as an outcome signal —
  e.g. never as a "clean shutdown" predicate in a seat-health tool.
- Presence of `session_exit` is a reasonable *"this transcript has been disposed at least
  once"* marker, nothing stronger: 168 error-terminal seats are disposed-normal, 75
  stop-terminal seats are not disposed, and 4 seats continue after a dispose.
- The C1 tool's own `dead_*` classes do not encode resumability. The 2-minute drift shows
  `incomplete → completed` is common and `dead_* → *` was not observed in that window
  [INFERENCE: a longer window would be needed to certify `dead_*` irreversibility; not
  observed here].

## Limits / remaining unknowns

- Single sessions directory (the assigned 12-57-31 dir of project `-Projects-shokunin`,
  OMP runtime 18.12.3). Other timestamped dirs and other projects were not scanned, so
  "other `kind`/`reason` values never occur" is **not** established globally.
- Counts are a moving snapshot of a live corpus; the report's tables are valid for T0–T1 only.
- Files with zero parseable message records: 0 (`unavailable` = 0), so no class was guessed.
- Terminal class was taken from the last message record in the **whole file**; equality with
  the tail-window rule was measured (0 divergences) but only for this snapshot.
- No `errorMessage` text, content, usage or non-allowlisted field was read or printed.

## Commands run (read-only) and tooling

- `ls -d …/sessions/…12-57-31…`, `ls`, `find … -type f -name '*.jsonl' | wc -l` (2509),
  `find … | xargs grep -o -h '"customType":"session_exit"' | wc -l` (2428) and
  `grep -L` per-file filter — all rc 0.
- Parsing/classification: in-process `python3` (eval) reading each file once; no scripts or
  artifacts written, no scratch, nothing under `/tmp`, no writes outside this report.
- Tool installs/upgrades: **none**. No pacman, no VCS command, no journal query.
