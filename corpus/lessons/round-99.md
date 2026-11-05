# Round 99 — lesson (mori, L1 MoriR99, attempt 1)

Entering `73308ff6e5c933f53498e9501ef95917b0ef7171` (r98 admitted). Frozen contract `.ufo/waves/round-99/contract.md`
at freeze `462cef1cc637de4c6e993aefd00ed9df32895984`, with every control (do-nothing, constant and lookup forgeries,
seven single-fix-removed mutants, missing-knowledge and unmined-row trees, positives) executed and committed first:
`.ufo/waves/round-99/evidence/controls-r99.txt` (`CONTROLS_DONE unexpected=0`, 19 lines `AS_EXPECTED`). Landing
`5013f0be8ac9e7fce3c08b680e43cf9cbd49620d`.

## Claims (frozen)

- **C1 operability** — the journal write-scan of `tools/mori-userns-runway.py` reads sudo's own `COMMAND=` rendering,
  joins `(command continued)` lines by pid, reads a `sh -c` script as POSIX words, quotes, comments and operators,
  skips `sysctl -r PATTERN` and exit events, accepts `journalctl -o short`, and fails closed on lines it cannot read.
  Counter battery generated at measurement time (QUALITY 209). Before `C1=unmet cases_ok=24/60 ... checks_failed=battery,sourced`;
  landing `C1=met cases_ok=60/60 ... checks_failed=-`.
- **C2 calibration** — SCORECARD `## Axes` Evidence cells point at the latest admitted closure per axis (located
  spot-check line, or `rounds[I]`), and the coverage and calibration Last-change cells carry the admitted r98
  closure. Before `C2=unmet mismatches=5 ... gate=rc1`; landing `C2=met mismatches=0 cells_unchanged=yes gate=ok`.

## Gate

New rows written this round (CORPUS rule 1), all opened 2026-11-05 by the L1, pinned at `corpus/evidence/sources-r99/`:

| row | URL | access (UTC) | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S633 | https://man7.org/linux/man-pages/man8/sysctl.8.html | 2026-11-05T21:55:09Z, HTTP 200, 14152 B, sha256 `a63af3f6…95f3` | "Only apply settings that match pattern." (raw lines 134-136 after tags are stripped, 6 words) | admit, mined, tier A |
| S634 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | 2026-11-05T21:55:10Z, HTTP 200, 357953 B, sha256 `0889867a…1acd` | "it and all subsequent characters up to, but excluding, the next <newline> shall be discarded as a comment." (raw lines 303-304, 17 words) | admit, mined, tier A |
| S635 | https://raw.githubusercontent.com/sudo-project/sudo/v1.9.17p2/lib/eventlog/eventlog.c | 2026-11-05 ~22:05Z, HTTP 200, 42109 B, sha256 `5bdea0ae…c84b` | "Wrap args containing spaces in single quotes." (line 202, 7 words) | admit, mined, tier A |
| S636 | https://raw.githubusercontent.com/sudo-project/sudo/v1.9.17p2/lib/util/lbuf.c | 2026-11-05 ~22:05Z, HTTP 200, 12373 B, sha256 `eda9e0a3…0212` | "Any non-printable characters are escaped in octal as #0nn." (line 145, 9 words) | admit, mined, tier A |

Row changes logged old→new: S014 (journalctl(1), re-opened 2026-11-05T21:55:11Z, HTTP 200, 87375 B, pinned
`corpus/evidence/sources-r99/S014-journalctl-r99.html`) `used-by`: `…, corpus/knowledge/journal-cursor-window-r16.md`
→ `…, corpus/knowledge/journal-cursor-window-r16.md, corpus/knowledge/sudo-log-grammar-r99.md`. Located quote:
"is the default and generates an output that is mostly identical to the formatting of classic syslog files"
(Output Options, `short`). Status and recheck unchanged.

Rejected this round: sudo's `main` branch as the grammar source (fetched first, 2026-11-05, `lib/eventlog/eventlog.c`
HTTP 200). Reason: the host runs sudo 1.9.17p2 (`sudo --version`), and a log reader is grounded in the producer at
the host's version; `main` can change the rendering without the host changing. Flip: a host upgrade to a sudo whose
tag differs re-opens the rows at that tag (the knowledge entry's `recheck`). A second rejection: re-scoping S014 as
a new row. The URL is already S014 (within-scope duplicate, census E04); only its `used-by` changed.

Assimilation: none this round (the `merge/mori/` package holds no sudo-log or shell-grammar theme that fits C1 or C2).
considerthese: `considerthese/2026-11-05.md` proposals 1–5 read; none taken (proposal 5, a mutation-survivor trend,
is served for this round by the w1 mutation seat's report, not a new instrument).

## Frontier step — census

Round start (`.ufo/waves/round-99/evidence/census-before.txt`): `mori ok`, `exit=0`, 43 `W04`
(`grep -c W04 .ufo/waves/round-99/evidence/census-before.txt` → 43), rows 404
(`git show 73308ff6:corpus/SOURCES.md | grep -cE '^ {0,3}\| *S[0-9]{3,}'`).
Round end (`.ufo/waves/round-99/evidence/census-after.txt`, run at `88c5c70c`): `mori ok`, `exit=0`, 44 `W04`
(the added one is S634, Mistake 7), rows 408 (`git show 88c5c70c:corpus/SOURCES.md | grep -cE '^ {0,3}\| *S[0-9]{3,}'`).
Misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`): 12 untracked fleet-root files, none written
by a mori seat (PDF/HTML sources of another lane and `w4lines.txt`, a number list naming no lane); none moved.

Correction of record (w1 `Mo99ScoutSrc.md`): the S634 row and this Gate table give the quote as 17 words; it has 18
(`it … comment.`, counted by whitespace). Still ≤25. The S634 row is not edited (CORPUS rule 2).

## Wave findings (w1, 12 seats)

- C1 replays: landing `C1=met cases_ok=60/60` on seeds 1, 42, 2026 and unseeded; entering `24/60` on every seed;
  controls re-run with all 19 rows `AS_EXPECTED` (`w1/Mo99ExecReplay.md`). The do-nothing control fails the same 12
  families on six seeds (`w1/Mo99CritC1.md`).
- C1 counter gameable: a zero-grammar forgery (16 templates read off the counter's own generator, a continuation and
  exit-event surface rule, and the pinned capture answered by sha256) scores `C1=met cases_ok=60/60` on four seeds.
  On ten hand-written held-out sudo lines the landed tool is right 10/10 and the forgery covers 3/10
  (`w1/Mo99CritC1.md`, VERDICT needs-amend). The claim stays as frozen; new QUALITY 212.
- Real sudo, real journal: three `sudo -n /usr/bin/true` probes logged exactly as S635/S636 predict (`it\'s`, `x#012y`,
  a 3550-char argv split into one first line and three `(command continued)` lines under one pid); the landed tool
  recovered all three argv lists exactly (`w1/Mo99ExecSudo.md`). The seat also ran `sudo -n -l` once, outside its
  authorized form (non-mutating; disclosed in its report).
- Live journal trial (2026-11-03 to 2026-11-05): on `-o short-iso` windows both tools report the same writes; on the
  default `journalctl -o short` text of the incident window the entering tool reads the six writes as `n=0` rc 0 and
  the landed tool reads `n=6 userns_zero=2` rc 1. The pinned r99 capture is byte-identical to a fresh extract of the
  same window (`w1/Mo99ExecTrial.md`).
- Review: eight findings (`w1/Mo99RevC1.md`). F1 `>|`, F2 backslash-newline (silent misses), F3 here-document bodies
  read as commands, F4 `#040` decoded wrong, F5 docstring, F6 quoted ` ; EXIT=` text, F7 empty argument (documented
  limit), F8 reordered continuations (fails closed). F1–F6 were fixed after the landing measurement, each with a
  self-test case (22 cases); F7 is now in the knowledge entry's Limits. The landing measurement is unchanged by them.
- Replay of the r98 frozen counter at landing (`w1/Mo99ExecReplay.md`): J1 changed as the contract disclosed, and J2
  also changed: a `systemd[1]: Started sudo[108] COMMAND=…` decoy was counted as an unreadable sudo line (rc 2). Fixed
  after the landing (a sudo entry must carry `sudo[PID]:`); at the final tip only the disclosed J1 differs.
- Sources: every row and knowledge claim located and supported; sudo main equals v1.9.17p2 in the cited blocks
  (`w1/Mo99ScoutSrc.md`).
- C2: holds on independent derivation from the pinned MANIFEST and at fleet HEAD (`w1/Mo99ExecCalib.md`,
  `w1/Mo99RevC2.md`, `w1/Mo99CritC2.md`). The registered gate run with its default base `66c5518e` now prints
  `columns_unchanged=no`; that is the designed detection firing on the sanctioned Evidence move, not a harm
  (`w1/Mo99RevC2.md` §8). Counter residual: a passing mention that names the axis and the verdict word on one line
  would also be accepted (`w1/Mo99RevC2.md`).
- Adjacency: tsukuroi's r24 archival captures use the same `COMMAND=` filter plus `cut -c1-220`, the same capture
  defect class as Mistake 1; reported to the operator through this report, never edited (`w1/Mo99ConnSibling.md`).

## Mistakes (CORPUS: class · evidence · captured-by · fix)

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| 1 | capture-truncation | the r98 capture is exactly the `COMMAND=`-filtered view of the r99 capture (`grep 'COMMAND='` of the r99 file is byte-identical to the r98 file, sha256 `97850413…9738`); the one `(command continued)` line was dropped and pid 1749648's command was cut mid-quote (`w1/Mo99ScribeLesson.md` Mistake 1) | none before this round | QUALITY 211; the r99 capture keeps every `sudo[` line; the tool fails closed on a quote still open. Shown able to fail: the landed tool reads the r98 capture with `unparsed=1`, exit 2 |
| 2 | silent-fallback | the r98 `split_cmd` fell back to `cmd.split()` on `ValueError`; on the capture 24 of the 276 `COMMAND=` values took that path with no output saying so | none | QUALITY 210; `split_cmd` inverts sudo's own rendering and raises `Unparsed`. Shown able to fail: `before-c1.txt` (entering `24/60`) |
| 3 | vacuous-control | first pre-freeze control run: K8 (a mutant equivalent under the draft R4 family) and K11 (the control's regex matched no row) `UNEXPECTED` (`evidence/controls-draft-prefreeze-r99.txt`) | the positive/negative control discipline (QUALITY 206/208): the run itself | R4 now plants an accept + exit event pair for one write; K11 counts 6 cells before status; the frozen run is `CONTROLS_DONE unexpected=0`. Shown able to fail: the draft receipt |
| 4 | number-drift | the frozen contract says 25 lines fall back; the entering code path gives 24 (25 counts the joined reading, which adds pid 1749648) (`w1/Mo99ScribeLesson.md` Mistake 4) | none: a count written without its command | QUALITY 210 and the knowledge entry corrected before commit; the contract is frozen and keeps 25 (this correction of record). Shown able to fail: the two counts printed by the scribe's instrumented run |
| 5 | survivor (counter) | a template forgery passes the frozen r99 counter 60/60 on four seeds (`w1/Mo99CritC1.md`) | QUALITY 209 was meant to; it asked for generated fixtures but did not forbid a readable generator and a tree-carried answer key | QUALITY 212. Shown able to fail: the forgery passes the frozen counter |
| 6 | regression-unchecked | the landed tool read a non-sudo decoy line in the r98 counter's J2 case as an unreadable sudo line (`w1/Mo99ExecReplay.md`); the predecessor's frozen counter was not run on the candidate before freeze | none | fixed post-landing (`SUDO_ENTRY_RE`, self-test `journal-not-sudo-entry`); next rounds run the predecessor capability's frozen counter on the candidate before the freeze and disclose every changed case. Shown able to fail: the r98 counter at landing `5013f0be` lists J1 and J2; at the final tip only J1 |
| 7 | duplicate-ground | S634 (XCU ch. 2, opened this round) repeats the URL of S611–S614, and S611 already holds the `#` comment rule this round cites; the round-end census adds one `W04 S634 duplicate url … across scopes` (`evidence/census-after.txt` 44 W04 vs 43 at start) | the census W04 warning, after the append | the comment claim in `corpus/knowledge/sudo-log-grammar-r99.md` now names S611 as the earlier row for the same rule; before appending a row, grep SOURCES.md for the URL (`grep -c V3_chap02 corpus/SOURCES.md` → 5 at the final tip). Shown able to fail: the census-after receipt |

Mutation (`w1/Mo99MutC1.md`, 37 single-point mutants of the landed tool, seeds 7 and 8, identical verdicts): 17
killed (every grammar-core path the battery plants), 4 equivalent survivors with proofs, 16 battery gaps, each with a
verified distinguishing sudo line (G1–G16: e.g. `; SIGNAL=KILL` exit events, glued `0>` fd, `echo -E`, `sysctl -f`,
an unterminated quote inside the `-c` script). Routed to the next counter (QUALITY 212 held-out set). The r98
survivor m03 (runway clamp) is now killed (`runway-clamp-off`).

## Routed (next round)

1. A successor C1 counter per QUALITY 212: a held-out set outside the lane tree (the CritC1 U01–U10 lines and the
   MutC1 G1–G16 lines are candidates), the template forgery as a frozen control.
2. C2 counter residual: a passing mention naming axis and verdict on one line is accepted (`w1/Mo99RevC2.md`).
3. Carried: r97 auditor residuals R1–R3; calibration-counter survivor M10; 31 `prefix_only` digest rows; operator
   L0s mori | round-94/95/96.
