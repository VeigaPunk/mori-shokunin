# SeatTool — mori round 17 wave 1 (C1 coverage tool)

Seat: `MoriR17.SeatTool-5` (executor, leaf; no subagent dispatch).
Clone: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatTool`
(base `24526ea9617cd020fee16c28fe4d4a2789dc28cb`, clean at start).
Lane checkout untouched; no VCS mutation anywhere.

## Files changed

| Path (inside the SeatTool clone) | Size | Mode | SHA-256 |
|---|---|---|---|
| `tools/mori-seat-terminal.py` (A1 + wave-2 strict projection) | 102173 bytes | `-rwxr-xr-x` | `93d7948786285a1f91eff09573c099f46df58ee5cb8c1992db5977ece2b3635d` |

No other file was created or edited; `.scratch/` was used only as `TMPDIR` for the selftest.

## What the tool implements

Contract interface read at `.ufo/waves/round-17/contract.md:24-67` (C1 tool contract) and the
fixture/gate shape at `:69-77`. Implementation anchors in the tool:

- CLI/help: `tools/mori-seat-terminal.py:1057-1134`; the three required limit statements are the
  `LIMITS` constant (`:97-102`) and the argparse description/epilog (`:1060-1078`). Observed
  `--help` (command below) prints all three limits and rc=0.
- Walk: `:267-304`. `os.walk(..., followlinks=False)`, sorted dirs/files, regular + non-symlink
  `lstat`, stop with rc2 `too-many-files` on the first discovery above `--max-files`.
- Bounded tail: `:192-228`. `os.open` with `O_NOFOLLOW`, `fstat` size, seek to
  `max(0, size - --max-tail-bytes)`, bounded read; when `start > 0` the first (possibly partial)
  line is dropped through its newline.
- Record selection: `:145-169` and `:230-242`. Line decoded UTF-8 then `json.loads`; decode/parse
  failures skipped; only `type == "message"` with a dict `message` is considered; the last such
  record in the tail is terminal; only `role`, `stopReason`, `errorStatus`, `errorMessage`,
  `provider`, `model` are retained.
- Classification: `:172-190`, in contract order — completed, aborted, dead_rate_limit (429 or the
  five message tokens), dead_quota (quota tokens, after rate-limit), dead_error_other, incomplete;
  `unavailable` when the tail has no parseable message (`:303`). Non-string/non-int values are
  ignored; `errorStatus` bool is not an int.
- Per-seat derived scalars and no text: `:244-259`. Emits exactly `seat`, `prefix`, `class`,
  `provider`, `model`, `error_status`, `retry_exhausted`, `retries`, `error_code`; `errorMessage`
  is used only for `startswith("Retry budget exhausted")`, `after N retries`, and `(type=NNNN)`.
- Tallies/output: `:306-332`. `totals` has all seven classes (zeros included); `by_prefix` and
  `by_provider_model` are built with the same zero-filled shape; top-level `retry_exhausted` is an
  int seat count (per-seat field stays bool); `seats` is a list of per-seat objects sorted by seat
  id; the only stdout write is one JSON document (`_emit`, `:116-122`).
- Exit codes: `:332` — 1 iff any class starts with `dead_`; 0 otherwise; 2 via
  `_setup` (`:124-133`) for unavailable dir, too-many-files, invalid numeric args, and missing
  `--sessions-dir`. `sessions_dir` is emitted verbatim.

Interface points confirmed with the owning peers (IRC, 2026-10-20):

- `MoriR17.SeatGate-5`: gate reads top-level key `finding` with values
  `MORI_SEAT_TERMINAL_OK/_DEAD/_SETUP`; `seats` is graded as a JSON list of per-seat objects
  sorted by seat id, projected to `{seat: class}`; top-level `retry_exhausted` is graded as a
  non-bool int seat count; rc2 output needs `schema` + `finding`, `sessions_dir` when present must
  match, `reason` tolerated, totals/seats not required unless a fixture declares them.
- `MoriR17.SeatFixtures-5`: `want.seats` is a dict seat→class; tool `seats` is expected as a list
  of per-seat objects sorted by seat id.
- `MoriR17.SeatGate-5`: `files_scanned` tolerance is `len(seats) <= files_scanned <= walked`;
  unfiltered requires equality. The tool increments `files_scanned` only for files it reads, so
  unfiltered = walked = len(seats) (unique basenames) and filtered = len(seats).

## Exact retained evidence

> This section records the initial C1 build. Amendment A1 (below) supersedes it: the
> authoritative post-A1 command, rc, pass count and hash are in the A1 section.

Selftest (the only execution run; `TMPDIR` inside the clone, never `/tmp`):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatTool
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatTool/.scratch \
  python3 tools/mori-seat-terminal.py --selftest
```

Observed stdout (one JSON line), rc=0:

```
{"arms":22,"finding_id":"SELFTEST_OK","passed":22,"schema":"mori-seat-terminal-selftest-v1","tool_sha256":"daaf7c398c906d7d83f01cbb9a86a089991b75997be190e5fce3bc9bca2188d9"}
```

First selftest run before the `_materialize` str/Path fix failed with an `AttributeError` and rc=1
(no arm ran). The fix is `tools/mori-seat-terminal.py:357-370`; the passing run above is the
post-fix run, and its embedded `tool_sha256` equals the `sha256sum` of the file after the run.

Help (read-only, rc=0): `python3 tools/mori-seat-terminal.py --help` printed the three required
limits verbatim — last-observed state, seats-not-incidents, prefixes-not-authenticated-membership
— plus "message text, content and usage are never emitted".

`sha256sum tools/mori-seat-terminal.py` →
`daaf7c398c906d7d83f01cbb9a86a089991b75997be190e5fce3bc9bca2188d9`; `stat` → 37408 bytes,
`-rwxr-xr-x`.

### Selftest arms (22; each runs the CLI as a real subprocess on synthetic TMPDIR transcripts)

| # | Arm | Assertion |
|---|---|---|
| 1 | `stop-completed` | assistant `stop` → completed, rc0/OK |
| 2 | `error-then-stop` | 429 error record followed by `stop` → completed (last record wins) |
| 3 | `retry-exhausted-429-zai` | 429 + `Retry budget exhausted after 10 retries ... (type=1302)` → dead_rate_limit, rc1/DEAD, `error_status=429`, `retry_exhausted=true`, `retries=10`, `error_code="1302"`, provider/model `zai/glm-4.6` |
| 4 | `devin-resource-exhausted` | error text `resource_exhausted` without 429 → dead_rate_limit (token), null status/retries/code |
| 5 | `weekly-quota` | error text `usage limit ... quota` → dead_quota, rc1 |
| 6 | `thinking-loop-error` | error text `thinking loop` → dead_error_other, rc1 |
| 7 | `aborted` | assistant `aborted` → aborted, rc0 |
| 8 | `tooluse-terminal` | assistant `toolUse` → incomplete, rc0 |
| 9 | `toolresult-last` | assistant `toolUse` then `toolResult` message → incomplete (last record) |
| 10 | `empty-file` | 0-byte file → unavailable, rc0 |
| 11 | `malformed-lines` | non-JSON, `null`, non-message record, valid `stop`, unterminated broken line → completed |
| 12 | `partial-first-line-after-tail-cut` | 4 KiB aborted line then stop line with `--max-tail-bytes 512` → completed (partial line dropped) |
| 13 | `credential-pin-never-echoed` | message content, a `credential_pin` record, `session_init` and `custom` all carry a fake token/sentinel; class completed and stdout contains no fake token, sentinel, `errorMessage`, `credential_pin`, `"content"` or `"usage"` |
| 14 | `symlink-skipped` | symlinked `*.jsonl` pointing at a dead transcript → no seat scanned, files_scanned 0, rc0 |
| 15 | `prefix-keep-kama` | `--prefix KamaR17` keeps only the completed seat, rc0, files_scanned 1 |
| 16 | `prefix-keep-tameshi` | `--prefix TameshiR17` keeps only the dead_quota seat, rc1, files_scanned 1 |
| 17 | `max-files-setup` | 2 files with `--max-files 1` → rc2 SETUP, reason `too-many-files` |
| 18 | `unavailable-dir` | nonexistent sessions dir → rc2 SETUP, reason `unavailable-dir` |
| 19 | `message-beyond-tail` | completed message then a 4 KiB non-message record, tail 512 → unavailable |
| 20 | `invalid-max-tail-bytes` | `--max-tail-bytes 0` → rc2 SETUP, reason `invalid-max-tail-bytes` |
| 21 | `empty-sessions-dir` | no files → zero totals, empty seats/tallies, rc0 |
| 22 | `non-object-message-skipped` | `type=message` with a non-dict `message` → unavailable |

Every scan arm additionally asserts: exactly one JSON document on stdout, empty stderr, exact
top-level key set, exact per-seat key set, prefix derivation, field types, sorted seat ids,
seven-class zero-filled `totals` recomputed from the expected seats, int top-level
`retry_exhausted` equal to the per-seat true count, and `by_prefix`/`by_provider_model`
recomputed from the emitted seat records.

## Risks / limits (no blocker)

> Pre-A1 list; superseded by the A1 risks section at the end (notably: duplicate stems are now
> separate rows, and schema/settle/main rules replace the earlier assumptions).

- Token matching is literal and case-sensitive as the contract writes it (`429`, `rate_limit`,
  `Rate limit`, `RATE_LIMITED`, `resource_exhausted`; `quota`, `usage limit`, `402`, `credits`).
  A different casing or wrapped number can change a class; bare `429`/`402` substrings can match
  unrelated text. Not measured against real transcripts (none read by this seat).
- The terminal record is the last message in the bounded tail only. A terminal record before a
  >256 KiB tail of non-message records reads as `unavailable` (arm 19 exercises the bound).
- Duplicate basenames in different subdirectories collapse to one seat id (last sorted path wins)
  while `files_scanned` counts both. Fixtures/gate are expected to avoid duplicates [INFERENCE].
- A symlinked `--sessions-dir` root is opened as the explicitly given directory; symlink entries
  beneath it (files or dirs) are never followed.
- Missing `provider`/`model` become null per seat and `unknown` in the `by_provider_model` key.
- Setup reason strings other than the contract's `too-many-files` (`unavailable-dir`,
  `invalid-max-tail-bytes`, `invalid-max-files`, `sessions-dir-required`,
  `selftest-takes-no-scan-args`) are this tool's choice; the gate confirmed `reason` is tolerated.
- The contract's summary-line sentence (`contract.md:60-61`) is garbled; the tool follows the only
  consistent reading — the JSON document is the sole stdout output — and the selftest enforces it.
- No real OMP transcript, journal, credential file or `/tmp` path was read or written. No tool
  install or upgrade was performed (none needed).

---

# Amendment A1 (contract.md:109-123, items 1-8 and 10) — implemented

Authoritative artifact after A1: `tools/mori-seat-terminal.py`, 62383 bytes,
`-rwxr-xr-x`, SHA-256 `5819c3c06e4ceded02b043ef1edbe15043359f176f1b24830b4d3cae24adbdba`.
A1 supersedes the earlier C1 output-key/shape text and the earlier 22-arm evidence above.

## Behavior changes and anchors

| A1 item | Implementation |
|---|---|
| 1 quota-first | `_classify` `:262-272`: quota tokens (`:86`) tested before rate tokens (`:78-85`) and `errorStatus == 429`; the rate token list adds `rate limit` |
| 2 settle window | `_message_view` reads `completedAt`/`timestamp` in ms epoch from the message dict, then the record (`:188-205`, `:207-245`); `_classify` `:259-261` returns `error_unsettled` when `terminal_ms > now_ms - settle_seconds*1000`; CLI `--settle-seconds` (default 900) and `--now-ms` at `:1774-1785`; output `now_ms`/`settle_seconds` at `:492-493`; default is the real clock only when `--now-ms` is absent (`main`, `:1815-1818`) |
| 3 keys/duplicates/main | `_scan` `:443-458`: `key` = relative path minus `.jsonl`, `seat` = stem, `kind` from direct-file + `MAIN_STEM_RE` (`:93`); duplicates are separate rows; `duplicate_stems` counts extra copies beyond the first per stem among seat rows (`:481-482`); `main_sessions` counts main rows (`:483`); rows sorted by `key` (`:486`) |
| 4 prefix none | `_scan` `:460-466`: `--prefix` and zero seat rows ⇒ rc2 `prefix-matched-none` (main rows never satisfy the seat count) |
| 5 robustness | regular files only via `lstat` (`:427-432`, symlinks/FIFOs/devices excluded); malformed/undecodable lines skipped in `_terminal_view` (`:354-366`); default `--max-tail-bytes` 524288 (`:98`); `main` catches `Exception` and returns rc2 `internal-error` (`:1827-1830`) |
| 6 schema | `_read_head` reads at most 4096 bytes (`:276-300`); `_header_ok` requires the first `type:session` record's integer `version == 3` (`:302-317`); `_analyze` labels `schema` / `no-message` / `unreadable` (`:392-406`) |
| 7 retries/roles | `_RETRIES_RE = after (\d+) retr(?:y|ies)` (`:91`); any terminal role other than `assistant` is `incomplete` (`:251-252`) |
| 8 output schema | key `finding_id`; top-level `now_ms`, `settle_seconds`, `main_sessions`, `duplicate_stems`; per-seat `key`, `kind`, `terminal_ms`, `reason` (null/schema/no-message/unreadable); key sets at `:102-136`, record builder `:368-384`, payload `:487-500` |
| 10 error codes | constants `:87-88`; code test before token tests in `_classify` `:262-266`: `1113`/`1308` ⇒ `dead_quota` even with 429, `1302` ⇒ `dead_rate_limit` |

Main rows are emitted with their class but excluded from `totals`, `by_prefix`,
`by_provider_model`, the top-level retry count, dead determination and the exit code; they are
counted in `files_scanned`, `len(seats)` and `main_sessions`. `error_unsettled` is a total class
and never dead.

## A1 selftest evidence

Exact command (executed once after the rewrite):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatTool
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatTool/.scratch \
  python3 tools/mori-seat-terminal.py --selftest
```

Observed stdout (one JSON line), rc=0, 33/33 arms:

```
{"arms":33,"finding_id":"SELFTEST_OK","passed":33,"schema":"mori-seat-terminal-selftest-v1","tool_sha256":"5819c3c06e4ceded02b043ef1edbe15043359f176f1b24830b4d3cae24adbdba"}
```

`sha256sum tools/mori-seat-terminal.py` after the run printed the same digest; `stat` printed
62383 bytes, `-rwxr-xr-x`. `--help` (read-only) exited 0 and printed the last-observed,
settle-window/error_unsettled, seats-not-incidents, prefixes-not-membership, mains-not-seats and
no-message-text limits.

The 11 new A1 arms (all previous 22 arms remain, updated to headers/`finding_id`):

| A1 item | Arm(s) | Assertion |
|---|---|---|
| 1 | `a1-quota-token-before-429` | 429 + `usage limit ... quota` ⇒ dead_quota (quota before rate) |
| 2 | `a1-settle-window` | fresh `timestamp` NOW-60s ⇒ error_unsettled; old `completedAt` NOW-1000s ⇒ dead_rate_limit; rc1 from the stale seat only; both `terminal_ms` pinned |
| 3 | `a1-keys-duplicates-main` | nested `a/Dup.Seat` + `b/Dup.Seat` distinct keys, same stem, both counted in totals; `duplicate_stems=1`; direct main-named file kind main, class dead_rate_limit but excluded from totals and rc (rc0); `main_sessions=1`; 4 files scanned; rows sorted by key |
| 4 | `a1-prefix-none` | `--prefix NomatchR17` with one seat ⇒ rc2 SETUP `prefix-matched-none` |
| 5 | `a1-fifo-skipped` | FIFO named `*.jsonl` never opened/skipped; real seat still scanned, files_scanned 1 |
| 5 | `a1-undecodable-line` | `\xff\xfe` line skipped, later message classified completed |
| 6 | `a1-schema-version-2` | header version 2 ⇒ unavailable `reason: schema` |
| 6 | `a1-schema-absent` | no header ⇒ unavailable `reason: schema` (empty-file arm now also schema) |
| 7 | `a1-retry-singular-role` | `after 1 retry` ⇒ `retries=1`, retry_exhausted true; `developer` role with error ⇒ incomplete |
| 8 | `a1-output-shape` | explicit `finding_id` + top-level/per-seat key set, `now_ms`, `settle_seconds`, `main_sessions`, `duplicate_stems`, `key`, `kind`, `terminal_ms`, `reason` |
| 10 | `a1-code-before-tokens` | 1113 with a rate token/429 ⇒ dead_quota; 1308 with quota+rate tokens/429 ⇒ dead_quota; 1302 with a quota token/429 ⇒ dead_rate_limit |

Every scan arm additionally asserts exactly one JSON document, empty stderr, exact top-level and
per-seat key sets, `key`/`seat`/`kind`/`prefix` coherence (including the main-stem regex rule and
that a direct main-named row is never kind seat), reason↔unavailable coherence, field types,
sorted keys, zero-filled eight-class `totals` recomputed from the graded classes, main exclusion
from totals/prefix/provider tallies/retry count, `duplicate_stems` recomputation, `finding_id` ↔
seat-dead coherence, `now_ms` pinned to `--now-ms`, and `settle_seconds`.

## A1 interface confirmations (IRC, 2026-10-20)

- `MoriR17.SeatGate-5`: A1 gate tolerates either `duplicate_stems` reading (type-check only),
  accepts sort by seat id or by key when all keys are present, excludes `kind:"main"` rows from
  totals/by-prefix/by-provider-model/retry/`want.seats` and from rc/finding dead coherence while
  counting them in `files_scanned`/`len(seats)`/`main_sessions`, allows mains under `--prefix`,
  and for rc2 needs `schema` + `finding_id=SETUP` with extra keys tolerated.
- `MoriR17.SeatFixtures-5`: expected.json pins rc/`finding_id`/totals/seats; the duplicate case
  expects two same-stem rows with distinct keys and totals counting both; seat order prefers key
  sort; the main case uses no prefix.

## A1 risks / limits (no blocker)

- `duplicate_stems` is emitted as an int count of extra copies beyond the first per stem among
  seat rows; the gate type-checks it and does not recompute, so the alternate "distinct duplicated
  stems" reading would also pass. Stated choice, not measured against fixtures.
- Main rows are kept under `--prefix` (the gate tolerates either; the fixture main case uses no
  prefix). `--prefix` matching only main rows is rc2 `prefix-matched-none`.
- Schema acceptance is strict: integer `version == 3`; a string `"3"`, float, bool or a header
  line split at the 4096-byte boundary reads as `unavailable`/`schema`.
- An error record without a numeric `completedAt`/`timestamp` cannot be established as recent and
  is classified as dead; a future timestamp reads `error_unsettled`.
- The settle comparison uses the single `--now-ms` value for every file (fixtures pin it); the
  real clock is sampled once per scan when the flag is absent.
- Any unforeseen exception is caught at the top and reported as rc2 `internal-error` without
  message text, satisfying "never rc1" but hiding the cause by design.
- No real OMP transcript, journal, credential file or `/tmp` path was read or written; no tool
  install or upgrade was performed.

---

# Wave 2 — PrivacyFinal filesystem/privacy hardening (clone base `5c1dfb8`, QUALITY39)

Clone recreated at `5c1dfb8d0530c74eb0e1630c2b522b735b486274`; the only file changed in this
wave is `tools/mori-seat-terminal.py` (the report itself is this append). Per QUALITY39 no
selftest, probe, lint, build or Python execution was performed. All statements below are static
code/interface evidence; the selftest arm counts are static, not observed runs.

Artifact: `tools/mori-seat-terminal.py`, 88642 bytes, `-rwxr-xr-x`,
SHA-256 `e2991600bbee98f5816aea280c1901e100be9e3bdac07ca3e8e2d3a1c2790b10`.

## Fixes mapped to `falsify/PrivacyFinal.md`

| Finding | Fix (anchors in the tool) |
|---|---|
| HIGH false clean from suppressed traversal | Root opened once (`_open_dir` `:642-647`); walk errors raise setup (`_collect_entries` `:684-748`); every `lstat`/`entry` stat error raises `lstat-failed` (`:713-715`); no `continue` on a failed stat remains. `os.walk` is gone |
| MEDIUM regular→FIFO open hang | Files opened `O_RDONLY|O_NOFOLLOW|O_NONBLOCK` (`_file_flags` `:634-639`), then `fstat` must be regular (`_open_regular_at` `:669-681`, `_open_regular` `:602-623`); FIFO open cannot block and is rejected before any read |
| MEDIUM symlinked sessions root | Trailing separators stripped before `islink` (`_scan` `:834-843`); root opened `O_DIRECTORY|O_NOFOLLOW` and ELOOP maps to rc2 `root-symlink` (`:838-843`) |
| MEDIUM source reads exceed allowlist | Whole-line `json.loads` replaced by a bounded byte scanner (`:257-406`) and field projector (`:416-518`); `json.loads` now appears only for bounded approved spans (`:380`) and for the selftest's own tool-output parse |
| MEDIUM committed live receipt path | Not a tool change; evidence redaction is L1/gate work. The tool still emits the caller-supplied `sessions_dir` verbatim as the contract requires. No receipt was read or edited by this seat |

## Filesystem safety detail

- Traversal is descriptor-relative: the sessions root is opened once and every child directory is
  opened with `O_NOFOLLOW|O_DIRECTORY` relative to its parent descriptor (`_collect_entries`
  `:684-748`). A symlinked ancestor introduced after discovery cannot redirect the walk.
- Analysis opens the leaf through `_open_leaf` (`:649-667`): each path component is opened
  `O_NOFOLLOW|O_DIRECTORY` with `dir_fd`, and the leaf with `O_NOFOLLOW|O_NONBLOCK`; the root
  descriptor is held for the whole scan (`_scan` `:830-912`), so a swapped path prefix or root
  rename cannot substitute a different tree.
- Both the 4096-byte header and the bounded tail come from one descriptor (`_analyze_fd`
  `:763-781`); the `fstat` regular-file check covers the bytes actually read.
- `os.scandir` is fed a duplicated descriptor and the duplicate is closed defensively with EBADF
  ignored (`:696-743`), so the held directory descriptor is never at the mercy of iterator
  ownership. Directory descriptors for pending subtrees are closed by the traversal `finally`.
- Discovery skips symlinks, FIFOs and devices by `lstat` mode; a path accepted as regular but
  replaced by a non-regular inode before open becomes an `unavailable` row with reason
  `unreadable` (no hang, no silently dropped seat).

## Parser/privacy safety detail

- Each line is scanned byte-by-byte: strings, objects, arrays, numbers, booleans and null are
  structurally walked without decoding their contents. Only approved field spans are decoded;
  `content`, `usage`, `credential_pin` payloads and every unapproved member are stepped over in
  place and never copied or materialized.
- Approved decodes are bounded: keys/type 64 bytes, role/stopReason 256, provider/model 512,
  numeric spans 32 bytes, retry/code digits 12. Over-bound values are ignored.
- `errorMessage` is never decoded. Its raw string span is folded immediately into derived
  metadata: retry-exhausted prefix (`bytes.startswith`), `after N retr(y|ies)` count,
  `(type=NNNN)` digit string, and literal quota/rate token presence (`bytes.find`). Escaped
  spellings are not decoded and are therefore not matched; the original text never enters the
  view, output, or class decision other than through those derived scalars.
- Header validation decodes only `type` and `version` from the first 4096 bytes; a non-session,
  absent, non-integer or non-3 version yields `unavailable` reason `schema`.
- Malformed, truncated, undecodable or trailing-garbage lines fail the structural match and are
  skipped; an unexpected exception is caught at the top and reported as rc2 `internal-error`,
  never rc1.
- Permitted input set is documented in the module docstring (`:26-50`) and help epilog: record
  type and record/message `completedAt`/`timestamp`; message `role`, `stopReason`,
  `errorStatus`, `provider`, `model`; `errorMessage`-derived metadata only.

## Semantic corrections folded in

- Terminal assistant error with no usable numeric `completedAt`/`timestamp` is `unavailable`
  with reason `terminal-time` (`_classify` `:570-576`), not dead and not unsettled.
- Z.AI business codes are scoped to provider exactly `zai` (`_classify` `:577-596`): 1113/1308 →
  dead_quota, 1302 → dead_rate_limit. An unmapped Z.AI code is not rate evidence from HTTP 429
  alone: explicit quota/rate text still classifies, otherwise dead_error_other. Codes are ignored
  for other providers. This is a classification hint, not an authenticated vendor cause and not
  a full vendor table.
- Bare `resource_exhausted` was removed from the rate token set (it can be quota/resource); it
  now falls through to dead_error_other unless an explicit status/rate/quota/code clue exists.
  Lower-case `rate limit` remains a rate token.
- Classes/CLI/output schema unchanged otherwise (`finding_id` values, `totals`, `by_*`,
  `main_sessions`, `duplicate_stems`, `now_ms`, `settle_seconds`, per-seat fields).

## Selftest arms added (static; NOT executed per QUALITY39)

41 subprocess arms plus 2 direct safety arms (43 total) are present. New wave-2 arms:

| Arm | Static expectation |
|---|---|
| `a2-root-symlink` | symlinked sessions root → rc2 SETUP `root-symlink` |
| `a2-root-symlink-trailing-slash` | same with a trailing separator spelling → rc2 `root-symlink` |
| `a2-walk-error` | chmod-000 nested directory → rc2 SETUP `walk-error` (requires non-root execution) |
| `a2-fifo-open-safety` (direct, daemon-thread with 10 s join) | `_analyze` on a FIFO returns `(None, "unavailable", "unreadable")` without blocking |
| `a2-walk-error-raiser` (direct) | `_raise_walk_error` raises `_SetupError("walk-error")` |
| `a2-credential-pin-only` | header + credential_pin/custom records with fake token → unavailable `no-message`, token/sentinel absent from stdout |
| `a2-error-no-terminal-time` | assistant error with 429/rate text but no timestamp → unavailable `terminal-time`, rc0 |
| `a2-unknown-zai-code` | zai `(type=9999)` under 429 without text → dead_error_other; with `rate limit` text → dead_rate_limit |
| `a2-nonzai-code-control` | same 1113/1302 codes under non-zai providers ignored → dead_error_other |
| `resource-exhausted-other` | bare `resource_exhausted` → dead_error_other |
| `devin-free-model-rate-limit` | `Reached free model rate limit` → dead_rate_limit |

All pre-existing error-terminal arms were given settled `completedAt` timestamps so they still
test their intended dead classes under the new `terminal-time` rule. Every scan arm keeps the
prior shape assertions (one JSON document, empty stderr, exact key sets, sorted keys, totals,
main exclusion, duplicate count, prefix/provider tallies, finding coherence, pinned now_ms).

## Coordination (IRC, 2026-10-20)

- `MoriR17.SeatGate-5`: A2 cases pin `root-symlink` and `walk-error` exactly; the gate compares a
  declared `want.reason` type-strict and does not hardcode reasons. Confirmed my emissions;
  `lstat-failed` is an additional possible setup reason.
- `MoriR17.SeatFixtures-5`: fixture pins confirmed for root symlink, chmod-000 walk error, static
  FIFO skip, credential_pin-only `no-message`, bare `resource_exhausted` → dead_error_other,
  free-model `rate limit` → dead_rate_limit, timestamp-free error → `terminal-time`, and unknown
  zai code (their example 1309) under 429 → dead_error_other.

## Risks / limits (no blocker)

- **No execution in this wave (QUALITY39).** The 43-arm selftest, `--help`, and gate fixtures have
  not been run against this revision; L1 owns the settled executed check. Static review only.
- `a2-walk-error` depends on chmod-000 actually denying the scanning user; under uid 0 the walk
  would succeed and that arm would fail. It is documented rather than special-cased.
- Empty/`unreadable` directories are reported as setup (`walk-error`) by design; the tool no
  longer attempts a partial scan.
- A regular file that shrinks between `fstat` and `pread` can yield a short/empty tail and thus
  `unavailable`/`no-message`; it cannot fabricate a dead class or hang.
- `os.scandir` on a duplicated fd is used for entry metadata; the duplicate-close wrapper makes
  the held descriptor ownership-independent, but this path is unexecuted in this wave.
- Raw-span token/code matching is literal: JSON-escaped spellings of the allowed tokens/codes
  are ignored (documented). This is deliberate field-minimization, not a full text decoder.
- `duplicate_stems` remains extra-copies-beyond-first over seat rows (gate type-checks only);
  main rows stay under `--prefix` (gate tolerates; fixture main case has no prefix).
- No live transcript, journal, credential file, `/tmp` path, VCS mutation, build, or test was
  performed in this wave; no tool install or upgrade was needed.

---

# Wave 2 follow-up — strict projection (still no execution, QUALITY39)

This subsection supersedes the artifact metadata above for the current tool revision.

Artifact: `tools/mori-seat-terminal.py`, 102173 bytes, `-rwxr-xr-x`,
SHA-256 `93d7948786285a1f91eff09573c099f46df58ee5cb8c1992db5977ece2b3635d`.
No selftest, probe or Python execution was performed.

## Counterexamples closed (PrivacyFinal.md:61-67)

- **Strict skipped-value syntax.** `_scan_string` (`:301-336`) now validates every JSON escape
  form (`\" \\ \/ \b \f \n \r \t \uXXXX`) and raw UTF-8 sequences via `_utf8_length`
  (`:272-298`), including overlong/surrogate/out-of-range rejection. `_scan_number`
  (`:339-363`) implements the complete JSON number grammar; arbitrary `+-.eE` runs and leading
  zeros no longer parse. Any invalid token makes the whole line fail the structural walk and be
  skipped.
- **Escaped class tokens.** `errorMessage` is stream-decoded through `_iter_decoded`
  (`:493-552`) into `_error_metadata` (`:555-636`): ASCII code points reached via `\u` escapes
  are yielded, non-ASCII yields a sentinel that breaks token continuity, and the decoded text is
  never retained. Token/prefix/retry matching uses a bounded 97-byte carry window (64 retained).
  Escaped `rate_limit`, `quota`, `Retry budget exhausted`, retry counts and `(type=1302)` now
  classify as intended.
- **Overlong unknown Z.AI codes.** `_error_metadata` keeps an `unknown_code_present` bit when a
  `(type=...)` token has more than the 12-digit display bound; `_classify` (`:792-804`) treats
  code-present-but-unmapped Z.AI errors conservatively, so a 13+-digit code under 429 without
  explicit text is `dead_error_other`, not status-only rate-limit.
- **Integer-only selected numbers.** `_parse_int_span` (`:473-481`) uses `_INT_RE`
  (`:148`) full-match only: schema version, `errorStatus`, and `completedAt`/`timestamp` reject
  fractions/exponents. `429.0` status is null (no status-rate inference), a decimal timestamp is
  `terminal-time` (age unproven), and `3.0` header version is `schema`.
- **Root ancestor caveat.** Kept explicit in the docstring (`:24-27`): the caller-selected root
  pathname is resolved once with only its final component O_NOFOLLOW-checked; ancestors above it
  are caller scope. Every descendant component is opened relative to a held descriptor with
  O_NOFOLLOW, so the child tree remains no-follow.
- **PrivacyFinal F6 (`resource_exhausted`) rejected as stale contract text.** L1's A2 line
  explicitly removes bare `resource_exhausted` as rate evidence; the tool keeps the removal.
  Bare `resource_exhausted` remains `dead_error_other` unless an explicit status/text/code clue
  exists; lower-case `rate limit` remains a rate token.

## Selftest arms added (named; NOT executed)

47 subprocess arms plus 2 direct safety arms (49 total). New strict-projection arms:

| Arm | Static expectation |
|---|---|
| `a2-strict-escape` | line with invalid `\q` escape inside skipped content is skipped; following completed message wins, rc0 |
| `a2-strict-number` | line with `42+9` status number is skipped (old parser would have accepted it and classified quota), following completed message wins, rc0 |
| `a2-escaped-error-tokens` | `(type=\u0031302)` → dead_rate_limit with code 1302; escaped `rate\u005flimit` + `after 2 retries` → dead_rate_limit, retry flags |
| `a2-long-zai-code` | 13-digit `(type=1234567890123)` under zai/429 → dead_error_other |
| `a2-float-status-time` | `429.0` status → error_status null and dead_error_other; decimal timestamp → unavailable terminal-time |
| `a2-float-version` | header `version:3.0` → unavailable schema |

Fixtures (SeatFixtures-5, IRC) report matching emitted cases: `escaped_quota_token_classified`,
`escaped_rate_token_classified`, `malformed_field_lines_skipped` (invalid `\q` and `:01`),
`decimal_timestamp_unknown_age`, `decimal_schema_version_unavailable`,
`decimal_status_not_429`, `long_code_13_digit_unknown`; 66 cases / 96 pins, expected SHA
`78071149679cf9871343286baff411cd0cb9215952521a8ed4dffd1d823853a9` (their artifact, not re-read
here). Gate (SeatGate-5) confirms tolerance for null `error_status`, `terminal-time`, `schema`,
escaped tokens/codes and long code strings; no class/reason pin conflict.

## Risks (strict-projection follow-up)

- Unverified by execution; L1 owns the settled run. Static review only.
- `_error_metadata` intentionally drops digit bytes inside a `(type=...)` token from its carry
  window; a contract token that overlaps code digits is not expected and would not match.
- Escaped non-ASCII code points yield a break sentinel; escaped ASCII spellings of the approved
  tokens match, but a token split by a non-ASCII escape is intentionally not reconstructed.
- The retry-count regex remains display-bounded at 12 digits; an absurd longer retry count reads
  as null while the retry-exhausted prefix still matches.
- `a2-walk-error` still requires non-root execution to deny chmod-000 traversal.
