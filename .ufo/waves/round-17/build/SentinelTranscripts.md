# SentinelTranscripts — C1 security review (`tools/mori-seat-terminal.py` contract)

Seat: `MoriR17.SentinelTranscripts-5` (sentinel, advise-only). Date: 2026-10-20.
Surface: `.ufo/waves/round-17/contract.md:24-78` (C1 tool + gate) against the live corpus at
`/home/vgpnk/.omp/agent/sessions`, inspected key-only.
No tool draft existed at review time (`.ufo/worktrees/round-17/SeatTool/tools/` lists no
`mori-seat-terminal.py`), so this reviews the contract and gives guards for the executor.

**Verdict: the contract is sound in intent, but as written it does NOT require 4 guards needed for
safety. Without them, one bad transcript line forces a false `DEAD` exit, symlinks or FIFOs escape
the walk, and the provider/model tally merges entries silently. 12 required guards are listed below.**

Axes: (a) secret non-exposure, (b) crash/DoS resistance, (c) exit-code truthfulness, (d) tally integrity.

## Method (all read-only; no installs; nothing written outside this report)

| # | Command | Result |
|---|---|---|
| 1 | `ls -la …/worktrees/round-17/; ls -ld ~/.omp ~/.omp/agent ~/.omp/agent/sessions; stat -c '%F'` | rc0; sessions = real directory (0755) under `~/.omp/agent` (0700) |
| 2 | eval py: `os.walk(followlinks=False)` + `lstat` census | 5815 `*.jsonl` regular files, 0 symlinks, 0 non-regular, 21165 other-ext files |
| 3 | eval py: last 262144 B of each file; `credential_pin` lines skipped by raw prefix **before** parsing; only aggregate counts, key names, value *types*, and the contract's named tokens printed | see Observations |
| 4 | eval py: crosstab of terminal records (stopReason × has errorMessage × has errorStatus) | see Observations |
| 5 | eval py: parser probes, only on in-memory synthetic bytes | see F1/F3 |
| 6 | `python3 -c 'print(os.DirEntry.is_file.__text_signature__)'`; `git ls-files -- .ufo/interactive-sessions \| wc -l`; `git check-ignore -v` | rc0; `($self, /, *, follow_symlinks=True)`; 0 tracked; ignored by `.gitignore:1` |

I printed no content, errorMessage text, usage, credential, hash, or responseId value. Provider names
were printed; `message.provider` is an allowlisted field.

Incidental exposure (self-disclosed): my first lane grep (`credential_pin|errorMessage|stopReason`
over the lane, gitignore off) matched the lane-resident transcript copy
`.ufo/interactive-sessions/20261015T050057Z/*.jsonl`. It displayed one `credential_pin` record
line (keys `type,id,parentId,timestamp,provider,hash`) plus content lines. I did not copy any value
into this report. See F11.

## Observations (key-only)

- Tail mode is normal, not an edge case. 5165 of 5815 files are larger than 262144 B. The largest
  is 14,891,155 B; p99 is 3,065,601 B.
- Record types seen in the tails: message 178600, custom 103549, custom_message 2668, model_change
  1291, session_init 803, thinking_level_change 666, title/session 650, **credential_pin 604**,
  model_usage 500, service_tier_change 51, title_change 38, ttsr_injection 1, compaction 1.
  Every one of 290,084 non-`credential_pin` lines starts with `{"type":"`; no `credential_pin`
  appeared with a different key order. 12 lines failed to parse.
- Every tail contains at least one newline. 17 tails end mid-line, which means a live writer was
  still appending. 13 files have no message record in the tail (→ `unavailable`). The longest line
  in a tail is 254,856 B. Terminal-message line length: max 254,856 B, p99 82,978 B.
- Keys on terminal `message` objects: role, content, api, provider, model, usage, stopReason,
  timestamp, responseId, duration, ttft, **credentialId**, completedAt, contextSnapshot,
  errorMessage, **errorId**, serviceTier, providerPayload, attribution, requestControls,
  inputTransformations, toolCallId, toolName, details, isError, stopDetails, errorStatus,
  retryRecovery, useless.
- Terminal crosstab:

  | stopReason | errorMessage | errorStatus | count |
  |---|---|---|---|
  | `stop` | – | – | 4759 |
  | `aborted` | yes | – | 379 |
  | none (toolResult/user) | – | – | 370 |
  | `error` | yes | – | 96 |
  | `error` | yes | yes | 189 |
  | `toolUse` | – | – | 9 |

  errorStatus is always an int (190). errorMessage is always a str; the longest is 239 chars.
- Named-token hits on terminal errorMessage: `429` 163, `Rate limit` 125, `rate_limit` 67,
  `resource_exhausted` 64, `402` 27, `credits` 27, `quota` 2, `RATE_LIMITED` 1, `usage limit` 1.
  `Retry budget exhausted` prefix 149, `after N retries` 149, `(type=NNNN)` 125.
- `retryRecovery` lives under `message`. Key shapes:
  - `{attempt:int, kind:str, note:str, recovery:str, status:str}` ×1560
  - `+recoveredAt:str, supersededBy:{model,provider,responseId:str,timestamp:int}` ×2122
  - the same without `responseId` ×20

  2 of these sit on terminal `error` records.
- Provider/model: 1127 of 5431 assistant terminals contain `/` in provider or model. 370–371
  terminals (toolResult/user) have no provider or model. No control characters were found; the
  longest provider+model is 39 chars.
- The live tree changed between passes (no-stopReason terminals went from 371 to 370), so any scan
  is a snapshot of "last observed", not an atomic census.

## Findings (severity · exploit path · evidence · impact · smallest remediation)

**F1 — HIGH — a parse crash becomes a false `DEAD` exit (c, b).**
- **Exploit path:** any transcript line in any of ~5.8k files is deeply nested JSON, a number with
  more than 4300 digits, or invalid UTF-8. The tool raises `RecursionError`, `ValueError` (int
  digit limit) or `UnicodeDecodeError`. None of these is a `JSONDecodeError`.
- **Evidence:** `b'['*200000` raised RecursionError in 3 ms. A 5000-digit `errorStatus` raised
  ValueError "Exceeds the limit (4300 digits)". `b'{"a":"\xff"}'` raised UnicodeDecodeError.
  Measured on Python 3.14.8.
- **Impact:** an uncaught exception exits with Python's default **rc 1**, which the contract
  (`contract.md:61-63`) defines as "≥1 dead". You get no JSON and a false DEAD signal, and the
  traceback goes to stderr.
- **Remediation:** per line, catch `(ValueError, RecursionError)` (which covers JSONDecodeError and
  UnicodeDecodeError) and skip the line. Wrap `main` so that any other exception becomes rc2
  `MORI_SEAT_TERMINAL_SETUP reason=internal-error`, without echoing `str(e)`. Reuse
  `tools/mori-journal-window.py:283,377`.

**F2 — HIGH — symlink, FIFO and TOCTOU escape from the walk (a, b).**
- **Exploit path:** someone places `X.jsonl -> ~/.omp/agent/agent.db` (or an auth file) inside the
  sessions directory, or swaps a file for a symlink or FIFO between listing and opening. The
  traps:
  - `os.walk(followlinks=False)` still lists symlinked *files* in `filenames`.
  - `DirEntry.is_file()` defaults to `follow_symlinks=True` (signature checked, command 6).
  - `os.walk(top)` follows a symlinked `top`.
  - `open()` on a FIFO blocks forever (POSIX fifo(7) semantics, [INFERENCE]: not executed here).
  - An intermediate directory component swapped for a symlink defeats `O_NOFOLLOW` on the last
    component.
- **Evidence:** no symlinks exist today (command 2), so the risk is latent.
- **Impact:** the tool reads credential stores, which violates the seat secrets rule even though
  the output allowlist limits what gets emitted. A FIFO hangs the scan, a DoS.
- **Remediation:**
  - Walk with `os.fwalk(top, follow_symlinks=False)`.
  - Open each file with `os.open(name, O_RDONLY|O_NOFOLLOW|O_NONBLOCK|O_CLOEXEC, dir_fd=dirfd)`,
    then `fstat` and require `S_ISREG`; otherwise class it `unavailable`.
  - `lstat` the root and give rc2 `reason=sessions-dir-symlink` if it is a link.
  - The pattern already exists at `tools/mori-journal-window.py:248-275`.

**F3 — MEDIUM — type confusion produces bad output (c, d, a).**
- **Exploit path:**
  - `errorStatus: true` passes `isinstance(int)` and is emitted as `true`.
  - `errorStatus: 429.0` equals 429, and Python json accepts `NaN`/`1e999`. `json.dumps` then
    emits the bare token `NaN`/`Infinity`, so the output is invalid JSON.
  - `after 9…9 retries` with more than 4300 digits makes `int()` raise ValueError (measured), and
    long-but-legal numbers produce unbounded ints.
  - With `ensure_ascii=False`, a lone surrogate in a filename or model string crashes with
    UnicodeEncodeError (measured).
- **Remediation:**
  - Accept error_status only if `type(v) is int and 100 <= v <= 599`, else null.
  - Use bounded regexes `after (\d{1,6}) retries` and `\(type=(\d{1,8})\)`.
  - Call `json.dumps(..., ensure_ascii=True, allow_nan=False, sort_keys=True)`.
  - Validate provider/model against `^[A-Za-z0-9._:@/+-]{1,128}$` and emit `"invalid"` otherwise
    (this field is target-controlled). Bound seat-name length the same way.

**F4 — MEDIUM — `by_provider_model` keys collide (d).**
- **Exploit path:** `"provider/model"` keys are ambiguous when either part contains `/`.
  `"a/b"+"/"+"c" == "a"+"/"+"b/c"` is True (measured). In the corpus, 1127 of 5431 terminals
  carry a `/`.
- **Impact:** tallies merge silently.
- **Remediation (contract change):** nest the structure as `{provider: {model: totals}}`, or
  require the split on the *first* `/` and reject providers that contain `/`. Also give
  toolResult/user terminals (370) a defined `unknown` provider/model; today they would produce
  `None/None`.

**F5 — MEDIUM — seat ids collide (d).**
- **Exploit path:** the seat id is the bare file stem, and the walk is recursive. Top-level L1
  session files (1342 stems without a dot) also count as "seats". The corpus already has 34
  duplicate stems, all of them non-seat names; dotted seat stems have 0 duplicates today.
- **Impact:** `seats`, sorted by id, gets ambiguous duplicates, and `expected.json` `seats{seat:class}`
  overwrites entries.
- **Remediation:** report `duplicate_seat_ids` and key seats by path relative to `--sessions-dir`
  (the stem can remain a display field). Optionally limit the walk to dotted stems at depth 3,
  the observed seat layout.

**F6 — MEDIUM — the resource bounds are incomplete (b).**
- **Exploit path:** `--max-tail-bytes` and `--max-files` have no upper or lower limit. The worst
  case is 20000 × N bytes read and parsed; N=0 or a negative N is undefined.
- **Remediation:**
  - Require 4096 ≤ max-tail-bytes ≤ 16 MiB and 1 ≤ max-files ≤ 100000; otherwise argparse rc2.
  - Read with one `os.pread(fd, n, max(0, size-n))`.
  - Scan lines **in reverse** and stop at the first valid `type=="message"` record. This bounds
    CPU per file and means most non-message lines are never parsed.
- **Note:** a terminal record longer than the tail is invisible and an older record gets
  classified. Observed max is 254,856 B, which is 97% of the default. State this in `--help` next
  to "last observed state".

**F7 — LOW — `credential_pin` cannot be "skipped unread" with parse-then-filter (a).**
- **Evidence:** contract `:37-38`; 604 `credential_pin` lines sit in the scanned tails.
- **Remediation:**
  - Reject lines whose raw bytes start with `{"type":"credential_pin"` before `json.loads`. The
    corpus is 100% type-first, so this works today; keep the post-parse `type` check as the real
    gate.
  - Never retain, log or repr non-message records.
  - The emit path must use an explicit output dict built only from the 8 allowlisted per-seat
    keys; never `dict(msg)`/`msg.get` passthrough. `credentialId`, `errorId`, `responseId`,
    `providerPayload` and `retryRecovery.note` all exist on terminal records.

**F8 — LOW — `retryRecovery` is not handled by the contract (c).**
- **Evidence:** 2 terminal `error` records carry `retryRecovery` (shapes in Observations). Its
  `note` is free text and `supersededBy.responseId` is an identifier; neither may ever be emitted.
- **Impact:** [INFERENCE] a seat in the middle of a retry may be counted `dead_*`. I did not
  inspect `status` values.
- **Remediation:** document it as a `--help` limit, or a contract clarification from L1. If the
  tool reads it, read only the key presence or enumerated `status`/`kind` values.

**F9 — LOW — `retry_exhausted` is not gated on `stopReason=="error"` (c).**
- **Evidence:** contract `:53`. All 379 aborted terminals carry errorMessage. 0 `Retry budget`
  prefixes appear on non-error records today.
- **Remediation:** compute `retry_exhausted`, `retries` and `error_code` only when
  `stopReason=="error"`.

**F10 — LOW — substring false positives on `429`/`402`.**
- **Evidence:** 0 cases of `429` without status 429 or another rate token; `402` co-occurs with
  `credits` 27/27.
- **Remediation:** none required now. The fixtures should include a case where `429` appears only
  inside an identifier.

**F11 — LOW (process) — a transcript copy lives inside the lane.**
- **Evidence:** `.ufo/interactive-sessions/20261015T050057Z/` holds 2 `*.jsonl` files with
  `credential_pin` and content. They are untracked and ignored by `.gitignore:1`.
- **Impact:** any lane-wide grep or read surfaces them (it happened in this review), and
  `--sessions-dir <lane>/.ufo` would scan them.
- **Remediation:** fixture and review seats must exclude `.ufo/interactive-sessions` from greps.
  Relocating the copy is an L1/operator decision outside this seat.

## Required guards (for SeatTool / SeatFixtures / SeatGate)

1. **Per line:** catch `(ValueError, RecursionError)`. **Top level:** any other exception → rc2 SETUP `reason=internal-error`, no `str(e)`, no traceback (F1).
2. **Walk:** `os.fwalk(follow_symlinks=False)` plus `O_RDONLY|O_NOFOLLOW|O_NONBLOCK|O_CLOEXEC` with `dir_fd`, `fstat` must be `S_ISREG`, and a symlinked root gives rc2 (F2). Reuse `mori-journal-window.py:248-275`.
3. **Emit:** build each seat dict from scratch with exactly `seat, prefix, class, provider, model, error_status, retry_exhausted, retries, error_code` (F7).
4. **Field types:** `error_status` must be `type is int` and in 100–599. Regexes are `\d{1,6}`/`\d{1,8}`. Provider/model/seat must match a charset+length allowlist, else `"invalid"` (F3).
5. **Output:** `json.dumps(ensure_ascii=True, allow_nan=False, sort_keys=True)`. Stdout carries only the JSON document (F3).
6. **Provider/model keys:** nest them, or use an unambiguous split, plus a defined `unknown` for provider-less terminals (F4).
7. **Seat ids:** key seats by relative path, or emit `duplicate_seat_ids` (F5).
8. **Argument bounds:** cap `--max-tail-bytes` and `--max-files` above and below. Use one `pread`. Reverse scan with early stop (F6).
9. **`credential_pin` prefilter:** skip raw `{"type":"credential_pin"` lines before parsing (F7).
10. **Error-only fields:** gate `retry_exhausted`, `retries` and `error_code` on `stopReason=="error"` (F9). Document the `retryRecovery`/mid-retry limit (F8).
11. **Fixtures must cover:** a deeply nested line; a >4300-digit int; invalid UTF-8; a symlinked `.jsonl`; a FIFO `.jsonl`; a symlinked root; `errorStatus: true`/`429.0`/`NaN`; a `/` in the model; duplicate stems; a `credential_pin` last line followed by no message; a terminal line longer than the tail; a trailing partial line. For each, assert that rc is never 1 except for a genuine `dead_*` seat. Fixtures stay synthetic (`contract.md:71-72`).
12. **Gate/selftest:** temp dirs only under the clone's `.scratch` via `TMPDIR`. Never point the tool at the real `~/.omp/agent/sessions` or the lane `.ufo` in fixtures (F11).

Installs/updates: none.
