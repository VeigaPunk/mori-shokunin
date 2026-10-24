# ScoutRefusalRecount — round 25, wave 2 (falsify)

Seat: `MoriR25.ScoutRefusalRecount` (leaf). Target: the refusal sentence in
`corpus/lessons/round-25.md` ("Wave-1 seat RefusalCensus counted 48 failed tool calls carrying the
text in 24 transcript files from 2026-10-20T13:55Z to 2026-10-22T10:04Z, every one with `(100)`"),
i.e. claim C2's live-fact evidence, re-derived by an independent read-only recount.

## Verdict: **weakened**

The numbers reproduce exactly as *occurrences of the refusal text inside failed tool results*
(48 occurrences, 24 files, first 2026-10-20T13:55:38.259Z, last 2026-10-22T10:04:50.044Z, every
parenthesised payload `100`). They do **not** reproduce as *failed tool calls*: those 48
occurrences live in **29** failed tool-result records, and only **26** of those records are the
harness refusal itself. No refusal anywhere names a number other than 100.

## Method (my own, independent of wave 1)

* Script: `/fast/scratch/hyaku/mori-r25/w2-ScoutRefusalRecount/recount.py` (Python 3.14.8 stdlib,
  `mmap`+`find`, read-only, opens nothing for write; sha256 `3db159c1…`). Probes `probe3.py`
  (`0aff7da5…`), `probe4.py` (`da5789d4…`). Output capture `recount-output.txt` (`437f0e4a…`).
  Run: `python3 -I -B recount.py` from that directory.
* Surface: `~/.omp/agent/sessions/**/*.jsonl` only — 3,798 transcript files, 3.53 GB, 0 unparsable
  marker lines. Snapshot taken 2026-10-22T11:46:17Z (a 11:40Z run gave identical failed-set counts).
* Definitions (mine): *failed tool result* = record `type=message`, `message.role=toolResult`,
  `message.isError` truthy; *strict marker* = regex `Background job limit reached \((\d+)\)`; window
  by the record's own `timestamp` (UTC), `[2026-10-20T13:55:00Z, 2026-10-22T10:05:00Z)`.
* Privacy: counts, timestamps, tool names, call ids and the fixed refusal text only; no message
  content is reported.

## Findings

**F1 — the claim's headline numbers hold as occurrence counts. Severity: none (reproduction).**
In the window: 48 strict `(100)` occurrences inside failed tool results, in 24 files, first
`2026-10-20T13:55:38.259Z`, last `2026-10-22T10:04:50.044Z`, strict numbers `{100: 48}`, per-date
split 1 / 40 / 7 (10-20 / 10-21 / 10-22) — identical to the wave-1 `harness_error` tier and its
per-date lines. Whole tree (no time filter): 31 failed records, 49 `(100)` occurrences.

**F2 — "48 failed tool calls" is a unit error; it is 29 records. Severity: moderate.**
The 48 occurrences sit in 29 distinct failed tool-result records (29 distinct `toolCallId`s, 0 ids
in more than one file), across 24 files (4 files hold more than one). Two records alone carry 21 of
the 48: `TabiR22-2.jsonl` 16:27:31.343Z has 14 occurrences on 7 lines; `Tabi22HeldHoldBounds.jsonl`
18:58:48.131Z has 7 occurrences on 1 line. Counting text occurrences as "failed tool calls"
overstates the number of failed calls by 19 (65%).

**F3 — only 26 of the 29 records are refusals at all; the window's last item is not one.
Severity: moderate.**
26 records have the refusal as their *own* message (content begins with the template, no process
details; tool `bash`, `isError=true`) — 26 occurrences, 22 files. The other 3 are bash failures
whose `details` carry `exitCode`/`timeoutSeconds`/`wallTimeMs` (a process ran) and whose *output
text* contains refusal lines: 16:27:31.343Z (7 refusal lines / 14 occurrences), 18:58:48.131Z
(1 line / 7), and 10:04:50.044Z (1 line / 1). The window's upper bound `2026-10-22T10:04Z` is set
by that last *data* record, not by a refusal; the last record whose own message is a refusal is
`2026-10-22T08:30:12.232Z`. Distinct in-window own-refusals: 26 records in 22 files.

**F4 — no refusal names a number other than 100. Severity: none (the load-bearing fact holds).**
Every strict match inside a failed tool result is `100`: 48/48 in-window, 49/49 whole tree. The only
non-numeric payload after the marker in any failed record is `${this.#maxRunningJobs}` — the harness
*source template* quoted by a bash failure at 2026-10-22T10:26:54.541Z (after the window), not a
refusal. The only strict numbers other than 100 anywhere in the tree are `1` and `15`, in 11
records, all `isError=false` (agent prose and bash/read outputs: `1` from truncated byte dumps and
reasoning text, `15` from the upstream issue quote of S110). None is a failed tool call. So the
answer to "does any refusal name a number other than 100" is **no**.

**F5 — growth, disclosed.** Whole-tree failed set at snapshot: 31 records (30 `bash`, 1 `edit`); the
two post-window records are the source-template quote above and an `edit` result at
`2026-10-22T10:31:37.541Z` carrying one `(100)` occurrence as data. No failed `task` or `eval`
spawn records exist in the tree (0), consistent with the registration-path reading but not a test
of it.

## Smallest fix

Reword the lesson sentence to the unit actually measured: "48 occurrences of `Background job limit
reached (100)` inside failed tool results — 29 records, 26 of them the refusal itself, in 24 files
(22 for the refusals) from 2026-10-20T13:55Z to 2026-10-22T10:04Z" — or recount by records (29/26).
No change needed to the `(100)` finding, which this recount independently confirms.

## Scope and limits

* Transcripts (`*.jsonl`) only, as assigned. Wave-1's `artifact` tier (non-transcript files) was
  not recounted here — not checked, not a pass.
* The tree is live; counts are snapshots. The failed set was stable across two runs 6 minutes apart
  (31 records / 49 occurrences whole tree; 29 / 48 in-window).
* No tool was installed or upgraded; no pacman/uv/npm/cargo transaction; no host service touched.

Report: .ufo/waves/round-25/w2/ScoutRefusalRecount.md
