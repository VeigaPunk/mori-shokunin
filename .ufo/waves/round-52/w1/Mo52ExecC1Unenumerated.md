# Mo52ExecC1Unenumerated — C1 arm (C): every command-tally pin the frozen counter does not enumerate

Seat Mo52ExecC1Unenumerated (executor), round 52 wave w1, lane mori-shokunin. Read-only: no lane, fleet or
corpus byte was written; the only writes are this report and my scratch tree.
Measured revision R = `8524904adb25e44f24d9f25aac7eae909625c18c` (the data commit); entering tip E =
`4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`. Frozen instrument read: `.ufo/waves/round-52/count-c1.py`
(arm C = `living_pins`/`check_living`/`superseded`, source lines 291-364; grammar `LPIN`, lines 73-80).
This seat is a dispatched executor; it does not judge the claims.

## 0. What arm (C) enumerates, exactly

`LPIN` requires, all **on one line**: a backticked span with no backtick and no newline inside that contains
`--selftest`, immediately followed by `(N/M)` or by `→`/`->` and a **backticked** `[PREFIX ]pass=N fail=K`.
`living_pins` over both living documents at R returns 9 raw spans, of which the counter prints `living=7
superseded=4` (`evidence/c1-at-data.txt`): QUALITY 885 (superseded), 909 (superseded), 1360 (ok); README 607
(superseded), 608 (superseded), 727 -> `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` (ok), 728 ->
`CONFORM_SELFTEST pass=9 fail=0` (ok). Two further raw spans on README 727/728 are the quoted stale pins the
`quoted()` rule drops.

## 1. Inventory — command-tally pins outside that grammar (6)

All line numbers are at R, both files read from a `git archive` of R.

| # | location | pinned text (verbatim shape) | why not enumerated | output of the command at R | match? |
|---|---|---|---|---|---|
| 1 | `corpus/QUALITY.md:588` (criterion 91) | ``Check: `bash .ufo/waves/round-30/check-blind-wave.sh --selftest` prints `PASS`\) | tally is the word `PASS`, not `(N/M)`/`pass=N fail=K` | in a git repo: `PASS`, rc 0; in the .git-less archive: `FAIL`, rc 1 | match in a repo; mismatch in the archive |
| 2 | `corpus/QUALITY.md:899-900` (criterion 111) | `` `python3 .ufo/waves/round-38/conform.py <rev> --selftest --counter .ufo/waves/round-38/count-c1.py` → `CONFORM_SELFTEST pass=6 fail=0` `` | backticked span crosses the 899/900 line break, **and** carries the placeholder `<rev>` | `CONFORM_SELFTEST pass=6 fail=0`, rc 0 | match |
| 3 | `corpus/QUALITY.md:933-934` (criterion 114) | `` `python3 .ufo/waves/round-42/conform.py <rev> --repo <lane> --contract .ufo/waves/round-39/contract.md --counter .ufo/waves/round-41/fixtures/c1/count-c8.py --selftest` → `CONFORM_SELFTEST pass=17 fail=0` `` | span crosses the 933/934 line break, **and** carries `<rev>` and `<lane>` | `CONFORM_SELFTEST pass=17 fail=0`, rc 0 | match |
| 4 | `corpus/README.md:579` (Round-36 coverage row) | ``Self-test `python3 tools/mori-source-drift.py --selftest` — PASS 4 cases at `bf0df77`.`` | tally `PASS 4 cases` sits outside backticks and outside the numeric grammar | `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)`, rc 0 | **mismatch** (pin 4 cases, today 6) |
| 5 | `corpus/README.md:580` (Round-36 coverage row) | `…`python3 tools/mori-sources-appendonly.py <tip> --round-base <entering tip>` exits 0 with `round_changed=[]`. … Self-test PASS 8 cases.`` | tally `Self-test PASS 8 cases` has no command printed and no numeric grammar | tool named in the row: `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, rc 0 | **mismatch** (pin 8 cases, today 22) |
| 6 | `corpus/README.md:593` (Round-37 coverage row) | `` `tools/mori-source-drift.py` (`--selftest` 6 cases) `` | case count outside backticks; the command path is in a different cell | `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)`, rc 0 | match |

Counted-but-command-less (a separate class, enumerated but never resolved):

| 7 | `corpus/README.md:607` (Round-39 coverage row) | `` `--selftest` → `pass=9 fail=0` `` | `LPIN` accepts a bare flag as the "command" (`living_argv` would return None); the pin is marked `superseded` by README 728 before any resolution | the row's tool `.ufo/waves/round-39/conform.py` needs a revision; judged through README 728's runnable form the counter ran at R and matched `CONFORM_SELFTEST pass=9 fail=0` | unrunnable as printed |

Searched and empty, at R:

- `(N/M)` after a non-backticked command: none. The only `(N/M)` tokens in the two files are `(27/27)` at
  `README.md:20` (a census bullseye, no command) and `(60/60)`, `(13/13)` at `QUALITY.md:1180` (quotations of
  SHONEN pins, no command here).
- `pass=N fail=K` outside backticks: none attached to a command. Every other `pass=` occurrence is a prose
  quotation of another file's pin (`QUALITY.md:1034, 1104, 1164, 1172, 1273, 1305, 1344`; `README.md` census
  bullets).
- Case-count tallies with no command at all: `README.md:93, 161, 212, 239, 277` (`PASS (N cases, N passed, 0
  failed)`) are census narrative bullets with no command and no revision qualifier, so I excluded them; named
  here so the L1 can overrule the exclusion.

## 2. Count

- Non-enumerated command-tally pins: **6** (QUALITY 588, 899-900, 933-934; README 579, 580, 593).
- If arm (C)'s grammar were extended to these four shapes and every pin run at R in a git repository:
  **2 mismatches** (README 579: 4 vs 6 cases; README 580: 8 vs 22 cases), **1 unrunnable** (README 607,
  today credited `superseded`), **3 matches** (QUALITY 899-900, QUALITY 933-934, README 593).
- Sandbox-conditional: **1** (QUALITY 588) — `PASS` rc 0 inside a repo, `FAIL` rc 1 in the `.git`-less archive
  that arm (C) itself runs every pin in (tool docstring: "the counter runs the pinned commands unsandboxed in an
  archive of R"; the script's first act is `git rev-parse --show-toplevel`).

So of the 4 non-enumerated pins that print a number, 2 pin a stale number and 2 are current; the one
word-tally pin is current in a repo and red in the counter's sandbox.

## 3. Corroboration on the enumerated set (why these gaps matter)

- `QUALITY.md:885` (109's check cell) is enumerated and read `superseded`. Run as printed at R it is not
  merely stale, it is red: `conformance setup error: expected str, bytes or os.PathLike object, not NoneType`,
  rc 2 — exactly QUALITY 111's claim. The supersession is credited from 111's cell, and 111's own
  *runnable-form* pin (899-900) is one of the pins this arm cannot see. Net: the arm's `ok` for 109's check
  cell rests on a command it never runs and is invisible to the command that proves the row.
- `QUALITY.md:909` (112's check cell) and `README.md:608` are likewise credited `superseded` without running;
  the replacement pins (QUALITY 1360, README 727) are enumerated and printed
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` at R (verified in this seat's run, §4).
- `README.md:607` shows the second half of the gap: a pin whose "command" is the bare flag is counted, then
  disposed by supersession, so no arm ever asks whether it names an executable.

## 4. Runs (literal commands, outputs, rc)

Scratch root `S=/fast/scratch/hyaku/mori-r52/Mo52ExecC1Unenumerated`; `TMPDIR=$S/tmp` for every run; `git
archive 8524904a… | tar -x -C $S/archive`; one `git clone --shared` of the lane checked out at R at `$S/clone`
(`rev-parse --show-toplevel` = `$S/clone`, HEAD = `8524904adb25e44f24d9f25aac7eae909625c18c`). `<rev>` was
filled with R; `<lane>` with `$S/clone`.

1. `cd $S/clone && bash .ufo/waves/round-30/check-blind-wave.sh --selftest` -> last line `PASS`, rc 0.
2. `cd $S/archive && bash .ufo/waves/round-30/check-blind-wave.sh --selftest` -> `FAIL`, rc 1 (no `.git`;
   script line 186 `git rev-parse --show-toplevel … || { printf 'FAIL\n'; return 1; }`).
3. `cd $S/archive && python3 .ufo/waves/round-38/conform.py 8524904adb25e44f24d9f25aac7eae909625c18c
   --selftest --counter .ufo/waves/round-38/count-c1.py` -> six `PASS <check>` lines then
   `CONFORM_SELFTEST pass=6 fail=0`, rc 0 (42.9 s).
4. `cd $S/archive && python3 .ufo/waves/round-42/conform.py 8524904adb25e44f24d9f25aac7eae909625c18c
   --repo $S/clone --contract .ufo/waves/round-39/contract.md --counter
   .ufo/waves/round-41/fixtures/c1/count-c8.py --selftest` -> fourteen `PASS <mutation>` lines, three
   `PASS <*_positive|source_order>` fixture lines, then `CONFORM_SELFTEST pass=17 fail=0`, rc 0 (78.3 s).
5. `cd $S/archive && python3 tools/mori-source-drift.py --selftest` -> six `selftest <arm> PASS` lines then
   `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)`, rc 0.
6. `cd $S/archive && python3 tools/mori-sources-appendonly.py --selftest` ->
   `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, rc 0.
7. `cd $S/archive && python3 .ufo/waves/round-38/conform.py --selftest` (the printed form of 109's pin) ->
   `conformance setup error: expected str, bytes or os.PathLike object, not NoneType`, rc 2.

Archive writes from pinned commands: none — a full file-mtime listing of the extraction before and after all
runs is identical (the only difference ever seen was a `__pycache__/*.pyc` my own `importlib` load of the
frozen counter created; removed before the final comparison).

One write was observed from a pinned command, in the repository it measures: run 4 creates
`$S/clone/.ufo/waves/round-41/scratch/` (`conform.py:944`, `os.makedirs(..., exist_ok=True)` plus a
`tempfile.mkdtemp(dir=…)` it removes). The directory is absent from the tree at R
(`git ls-tree 8524904a .ufo/waves/round-41/` lists `conform.py`, `contract.md`, `evidence/`, `fixtures/`,
`w1-spec.json`, `w1/`), was created at 21:16:46 local by this run, and is empty (0 entries). Because it is
empty, `git status --porcelain --ignored` prints nothing — so arm (C)'s `lane_writes` counter, defined as
"lines of `git status --porcelain --ignored` … that appear while the pinned commands run", cannot see a pinned
command leaving it inside the repo it measures.

## 5. Boundaries and limits of this inventory

- The inventory is complete only for the two files' `--selftest` command-tally shapes at R. Verdict-only check
  cells (e.g. `QUALITY.md:962-963` `… --counter …` prints `C2=met`; `QUALITY.md:424-425` prints
  `blind_violations=<n>`) name no numeric tally and were counted outside this inventory.
- Runs 3 and 4 execute the pinned commands with real values; the counters themselves are frozen bytes from
  `git show R:.ufo/waves/round-52/count-c1.py`, and I did not edit, copy into the lane or re-freeze anything.
- The archive sandbox is not neutral for git-dependent pins; that is a property of arm (C) as frozen, recorded
  here as a named limit, not as a proposal to change it.
- `PASS 4 cases at bf0df77` (README 579) is historically true of the r36 bytes; it is stale as a current tally.
  Both readings are given so the L1 can decide whether a dated qualifier or a supersession line is the right
  data-side correction. No superseding line quotes either case-count tally today (`grep -n supersedes
  corpus/README.md` returns rows about other pins).
- Reads were confined to the lane's git objects (`git archive`, `git ls-tree`), the extracted copies, `/proc`
  nothing, and the lane's frozen counter source; no host state was written and no pacman/uv/npx install was
  needed (recorded: none installed or upgraded).

## Findings

1. **MED** — `corpus/README.md:579` pins `PASS 4 cases` for `python3 tools/mori-source-drift.py --selftest`; at R
   the command prints `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)`, rc 0. Stale, unsuperseded, and outside arm
   (C) (mismatch #1 if enumerated).
2. **MED** — `corpus/README.md:580` pins `Self-test PASS 8 cases` for the tool `tools/mori-sources-appendonly.py`;
   that tool's selftest prints `pass=22 fail=0`, rc 0 at R. Stale, unsuperseded, outside arm (C) (mismatch #2 if
   enumerated).
3. **MED** — `corpus/QUALITY.md:899-900` (criterion 111) and `933-934` (criterion 114) are the only executable
   check cells for those rows and are invisible to arm (C) (span across lines plus `<rev>`/`<lane>` placeholders).
   Both match at R when run with real values. The arm's `C1=met` therefore says nothing about them.
4. **MED** — `corpus/QUALITY.md:885` (criterion 109's check cell) is enumerated only to be marked `superseded`;
   run as printed at R it exits 2 with `conformance setup error`. Its replacement pin is finding 3's 899-900.
5. **LOW** — `corpus/QUALITY.md:588` (criterion 91) pins the word `PASS` rather than a tally. It prints `PASS`
   rc 0 in a git repository and `FAIL` rc 1 in the `.git`-less archive arm (C) runs pins in, so the sandbox, not
   the pin, decides the verdict.
6. **LOW** — `corpus/README.md:607` is counted as a pin, names no command (`--selftest` alone), and is disposed
   by supersession before `living_argv` ever rejects it.
7. **LOW** — `corpus/QUALITY.md:933-934`'s command leaves `.ufo/waves/round-41/scratch/` (empty) inside the
   `--repo` it measures; `git status --porcelain --ignored` does not list an empty directory, so arm (C)'s
   `lane_writes` is blind to it (round-51 closure item 8 class: an in-lane writer).
8. **LOW** — `corpus/README.md:593` pins `--selftest` at 6 cases; at R the tool prints 6 cases. Current; no
   action beyond keeping it in the enumerated set when the grammar grows.

Routed for round 53 (counter-side changes are frozen this round; listed, not applied): (a) enumerate
line-crossing spans and document a substitution rule for `<rev>`/`<lane>`; (b) accept word tallies
(`prints PASS`) and case-count tallies (`PASS N cases`) or declare them out of scope in the docstring rather
than in prose; (c) require a resolvable command even on a `superseded` pin; (d) run git-dependent pins in a
git-visible copy, or record the sandbox as part of the verdict; (e) K4 data-side: supersede or date-qualify the
two stale case-count tallies, and consider reflowing QUALITY 111/114's check cells to one line so the arm can
see them.
