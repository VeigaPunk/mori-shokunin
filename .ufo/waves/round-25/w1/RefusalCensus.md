# RefusalCensus — round 25, claim C2 (harness background-job runway, live-fact evidence)

Seat: `MoriR25.RefusalCensus` (executor). Assignment: `wave1-spec.json` → `RefusalCensus`
("Live-fact evidence for C2. Surface: OMP session transcripts under `~/.omp/agent/sessions`
(find the directory; read-only) … counting script in the sandbox clone
`/fast/scratch/hyaku/mori-r25/wt-refusals` (path `tools-scratch/refusal-count.py`, never committed
to the lane) … counts of the exact text `Background job limit reached (` grouped by the number inside
the parentheses and by date (UTC), over files modified 2026-10-19..2026-10-22, reporting only
counts, the number in parentheses, file counts and first/last timestamps … State whether any refusal
shows a number other than 100. Commit in the sandbox only.").

## Files changed

| Path | Where | Note |
|---|---|---|
| `tools-scratch/refusal-count.py` | sandbox clone `/fast/scratch/hyaku/mori-r25/wt-refusals` (branch `r25-wt-refusals`) | new file, read-only, committed in the sandbox only |
| `tools-scratch/refusal-count-output.txt` | same sandbox | captured stdout of the run pasted below, committed in the sandbox |
| `.ufo/waves/round-25/w1/RefusalCensus.md` | lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin` | this report (written, not committed — the lane index is the L1's) |

Sandbox commits: `ca539f8` (script + first capture), `e1a140f` (strict tiers + recapture), both on
top of `7634be7`. sha256 of the committed script blob
`git show HEAD:tools-scratch/refusal-count.py`:
`08027b29c90f4411674345de5915b44784155798d6a17b8ede0faea7c5174bef`; of the captured output:
`62a47a3ca6ad630a8965eb486ac0793ba55db9f74410df7bd77e109b4fd8fbfb`. Nothing was pushed (the
sandbox's `origin` is the lane repo; mutating the lane is out of bounds for a seat). The lane working
tree contains no file of mine other than this report.

## Surface (read-only discovery)

* Session directory: `/home/vgpnk/.omp/agent/sessions` — found by listing `/home/vgpnk/.omp/agent/`
  (`RULES.md`, `agent.db`, `config.yml`, `sessions`, …). It holds 45 workspace sub-directories and
  ~31.7k files (transcripts are `*.jsonl`; a session directory also holds agent-written artifacts:
  `*.md`, `*.log`, `*.json`).
* Only the session directory was read; the operator's OMP settings file was read once (line range only, see
  below); nothing under `~/.omp` was edited, and `omp` was never run.

## Method

`tools-scratch/refusal-count.py` (Python 3 standard library only, runs under `python3 -I -B`,
read-only: it opens files for reading and writes nothing):

* window — files whose **mtime** (UTC) falls in 2026-10-19..2026-10-22 inclusive;
* match — the strict regular expression `Background job limit reached \((\d+)\)` (the closing
  parenthesis is required, so only a well-formed `…(N)` counts; see "Non-100 numbers" below);
* date — for a session transcript (`*.jsonl`) the timestamp of the **record** that carries the
  occurrence (top-level `timestamp` field, UTC); for any other file the file **mtime** (UTC);
* grouping — by (UTC date, number); reported as occurrences, distinct-file count, first and last
  timestamp;
* privacy — the tool prints counts, the parenthesised number, file counts and timestamps only. It
  prints no file path beyond the session directory name and no message content.

Occurrence tiers (the same occurrence is counted in every tier it qualifies for):

| Tier | Meaning |
|---|---|
| `all` | every occurrence in every file of the window |
| `transcript` | occurrences inside `*.jsonl` transcripts |
| `toolresult` | occurrences inside transcript records whose role is `toolResult` (harness/tool output) |
| `harness` | `toolresult` records that carry the refusal as a harness-emitted error: `isError` true, **or** the tool is `task` (the async spawn tool), **or** the record carries the harness error suffix |
| `harness_error` | the strict subset of `harness`: `toolResult` records with `isError` true — the refusal delivered as a failed tool call |
| `prose` | transcript records that are **not** tool results (agent-authored assistant/user text, unparsable lines) — i.e. quotes of the refusal, not refusals |
| `artifact` | occurrences in files that are not session transcripts (dated by mtime) |

## Command and output

```
$ cd /fast/scratch/hyaku/mori-r25/wt-refusals
$ python3 -I -B tools-scratch/refusal-count.py --exclude-name 'MoriR25.RefusalCensus'
REFUSAL_CENSUS v1
root: /home/vgpnk/.omp/agent/sessions
window (file mtime, UTC): 2026-10-19..2026-10-22
excluded name tokens: MoriR25.RefusalCensus
scan: files_seen=31683 files_in_window=31191 transcripts_in_window=3424 files_with_hits=531 bytes_read=3792510950 unreadable=0 workspaces_total=45 workspaces_with_hits=2

tier all: occurrences=20323 files_with_hits=520 groups=4
  numbers: 100=20322, 15=1
  date=2026-10-20 number=100 occurrences=153 files=11 first=2026-10-20T08:02:03.325Z last=2026-10-20T23:26:38.918Z
  date=2026-10-21 number=100 occurrences=15753 files=349 first=2026-10-21T03:33:56.423Z last=2026-10-21T23:59:32.261Z
  date=2026-10-22 number=100 occurrences=4416 files=166 first=2026-10-22T00:00:24.646Z last=2026-10-22T10:09:49.187Z
  date=2026-10-22 number=15 occurrences=1 files=1 first=2026-10-22T10:05:15.357Z last=2026-10-22T10:05:15.357Z

tier transcript: occurrences=8974 files_with_hits=346 groups=4
  numbers: 100=8973, 15=1
  date=2026-10-20 number=100 occurrences=144 files=2 first=2026-10-20T08:02:03.325Z last=2026-10-20T22:05:07.204Z
  date=2026-10-21 number=100 occurrences=7057 files=220 first=2026-10-21T03:33:56.423Z last=2026-10-21T23:59:32.261Z
  date=2026-10-22 number=100 occurrences=1772 files=130 first=2026-10-22T00:00:24.646Z last=2026-10-22T10:09:49.187Z
  date=2026-10-22 number=15 occurrences=1 files=1 first=2026-10-22T10:05:15.357Z last=2026-10-22T10:05:15.357Z

tier toolresult: occurrences=6562 files_with_hits=342 groups=3
  numbers: 100=6562
  date=2026-10-20 number=100 occurrences=130 files=2 first=2026-10-20T08:02:03.325Z last=2026-10-20T22:05:07.204Z
  date=2026-10-21 number=100 occurrences=5679 files=219 first=2026-10-21T03:33:56.423Z last=2026-10-21T23:59:32.261Z
  date=2026-10-22 number=100 occurrences=753 files=127 first=2026-10-22T00:00:24.646Z last=2026-10-22T10:09:46.808Z

tier harness: occurrences=5313 files_with_hits=150 groups=3
  numbers: 100=5313
  date=2026-10-20 number=100 occurrences=58 files=2 first=2026-10-20T08:03:42.725Z last=2026-10-20T20:29:20.835Z
  date=2026-10-21 number=100 occurrences=4867 files=111 first=2026-10-21T05:23:20.025Z last=2026-10-21T23:58:43.228Z
  date=2026-10-22 number=100 occurrences=388 files=39 first=2026-10-22T00:00:24.646Z last=2026-10-22T10:07:55.566Z

tier harness_error: occurrences=48 files_with_hits=24 groups=3
  numbers: 100=48
  date=2026-10-20 number=100 occurrences=1 files=1 first=2026-10-20T13:55:38.259Z last=2026-10-20T13:55:38.259Z
  date=2026-10-21 number=100 occurrences=40 files=16 first=2026-10-21T16:27:31.343Z last=2026-10-21T23:56:46.114Z
  date=2026-10-22 number=100 occurrences=7 files=7 first=2026-10-22T08:22:13.784Z last=2026-10-22T10:04:50.044Z

tier prose: occurrences=2412 files_with_hits=119 groups=4
  numbers: 100=2411, 15=1
  date=2026-10-20 number=100 occurrences=14 files=2 first=2026-10-20T08:02:26.360Z last=2026-10-20T18:57:52.530Z
  date=2026-10-21 number=100 occurrences=1378 files=79 first=2026-10-21T05:24:02.838Z last=2026-10-21T23:58:43.222Z
  date=2026-10-22 number=100 occurrences=1019 files=41 first=2026-10-22T00:00:35.552Z last=2026-10-22T10:09:49.187Z
  date=2026-10-22 number=15 occurrences=1 files=1 first=2026-10-22T10:05:15.357Z last=2026-10-22T10:05:15.357Z

tier artifact: occurrences=11349 files_with_hits=174 groups=3
  numbers: 100=11349
  date=2026-10-20 number=100 occurrences=9 files=9 first=2026-10-20T08:26:37.733Z last=2026-10-20T23:26:38.918Z
  date=2026-10-21 number=100 occurrences=8696 files=129 first=2026-10-21T05:50:48.444Z last=2026-10-21T23:54:28.599Z
  date=2026-10-22 number=100 occurrences=2644 files=36 first=2026-10-22T00:00:33.730Z last=2026-10-22T10:03:37.913Z

distinct numbers (tier all): 15, 100
distinct numbers (tier harness): 100
distinct numbers (tier harness_error): 100
distinct numbers (tier prose): 15, 100
any number other than 100 (tier all): YES 15
any number other than 100 (tier harness): NO
any number other than 100 (tier harness_error): NO
any number other than 100 (tier prose): YES 15
```

Exit status 0 (stdout captured verbatim in
`/fast/scratch/hyaku/mori-r25/wt-refusals/tools-scratch/refusal-count-output.txt`, sha256
`62a47a3ca6ad630a8965eb486ac0793ba55db9f74410df7bd77e109b4fd8fbfb`).

## Answer: does any refusal show a number other than 100?

**No.** Every refusal the harness emitted on this host carries the number **100**:

* tier `toolresult` (harness/tool output records): 6,562 occurrences, **only 100**;
* tier `harness` (refusal delivered as an error, `isError` true or `task` tool or the harness error
  suffix): 5,313 occurrences, **only 100**;
* tier `harness_error` (strictest: `toolResult` with `isError` true, i.e. the refusal as a failed
  tool call): 48 occurrences in 24 files, **only 100**;
* distinct numbers across the whole census: `100` plus one prose hit (`15`, see below).

### The non-100 numbers, and why they are not refusals

Two kinds of non-100 match exist in the tree; neither is a harness refusal on this host:

1. **`15` — one occurrence, 2026-10-22T10:05:15.357Z** (tiers `all`, `transcript`, `prose`; absent
   from `toolresult`, `harness`, `harness_error`). It sits in an **assistant** record of a sibling
   seat of this same wave (agent-authored prose quoting an upstream issue title), so it is a quote of
   the text, not a refusal produced here.
2. **`1` — six occurrences, all in this seat's own transcript** (`MoriR25.RefusalCensus.jsonl`),
   produced by my own reasoning text that spells the marker with a truncated number. The census run
   excludes this file with `--exclude-name 'MoriR25.RefusalCensus'`; the run *without* that flag
   reports `distinct numbers (tier all): 1, 100` and `any number other than 100 (tier all): YES 1`,
   which is pure self-contamination. A separate attribution pass over the whole tree (not restricted
   to the window) attributes **every** non-100 match to that one own-seat file:
   `('.jsonl', 'own-seat', '1') -> 6`, and no other file.

A looser regex that accepts an unterminated number (`Background job limit reached \((\d+)` without
the closing parenthesis) adds three further artefacts, all excluded by the strict form: truncated
byte-dump strings ending `…(1` / `…(10`, and one agent-written byte-offset listing
`…(95794256, …)`. None of them is a parenthesised cap.

## Live-fact value for C2

* the operator's OMP settings file reads `async:` / `  maxJobs: 200` — the **configured** runway.
* The installed binary's clamp (`maxRunningJobs: () => Math.min(100, XPe.get(R))`, byte search by
  the L1 on 2026-10-22) and this census agree on the **effective** value: every observed refusal
  message interpolates `100`, never `200` — 6,562 harness-side occurrences, zero exceptions, over
  three consecutive days (2026-10-20 … 2026-10-22) and 342 files.
* Therefore the live host behaves as `effective = min(clamp 100, configured 200) = 100`
  (`RUNWAY_CLAMPED` under contract rule 5). This is an observation of the cap the binary applies, not
  a count of running jobs.
* Timeline of the refusal traffic (tier `harness_error`, the failed-tool-call subset): first
  2026-10-20T13:55:38.259Z, 40 occurrences on 2026-10-21 (16 files), 7 on 2026-10-22 up to
  2026-10-22T10:04:50.044Z. The whole-day `harness` tier runs 2026-10-20T08:03:42.725Z →
  2026-10-22T10:07:55.566Z. There are **no** occurrences dated 2026-10-19 (the window's first day).

## Tooling

No package was installed or upgraded: the census is Python 3 standard library only.
`python3 -VV` → `Python 3.14.8 (main, Oct 2 2026, 10:23:31) [GCC 16.2.1 20260810]`. No `pacman`,
`uv`, `npm` or `cargo` transaction was run; no host service was restarted.

## Risks, limits, blockers

* **The tree is live.** Sessions are being written while the census runs, so the counts are a
  snapshot, not a closed set: two runs minutes apart differ by a few dozen occurrences in the
  `all`/`transcript`/`artifact` tiers (e.g. 19,339 → 20,322 occurrences of `100` in tier `all`).
  The strict `harness_error` tier was 48 occurrences in both runs in which it was measured, and
  `harness` was 5,313 in the last two runs. The committed capture is the one pasted above.
* **Tier definitions are mechanical, not semantic.** `toolresult` counts every tool-output record
  carrying the text, including tool output that merely *displays* a quoted error (e.g. a `read` of a
  wave document). `harness` narrows this with the `task` tool and the harness error suffix;
  `harness_error` is the strictest (a failed tool call). Only `harness_error` is a refusal the
  harness raised in that moment; the higher tiers are text frequency.
* **Dates come from two different clocks**: record timestamps for transcripts, file mtime for
  artifacts and for transcripts whose record carries no parsable timestamp. A refusal whose record
  timestamp differs from the file mtime is therefore attributed to the record's date, not the file's.
* **The window is by file mtime**, as assigned; a file written before 2026-10-19 but touched later
  is in scope, and a file written inside the window but later touched outside it would fall out.
* **Not answered here** (out of this seat's scope, and not readable from outside the session): how
  many background jobs are running now, whether queued jobs count toward the cap, and the
  per-session vs per-host scope of the cap. The census bounds the *cap value* observed in refusals,
  not the utilisation.
* No blockers.

Report: .ufo/waves/round-25/w1/RefusalCensus.md
