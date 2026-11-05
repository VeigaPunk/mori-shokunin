# Mo99ScribeLesson — draft round-99 lesson sections (for L1 MoriR99 to integrate)

Seat: scribe. Axes judged: operability, calibration. Draft only; nothing committed, no lane file edited except this
report. Scratch `/fast/scratch/hyaku/mori-r99/Mo99ScribeLesson` (TMPDIR set there), removed at the end. No tool
installed. No sudo run, no sysctl touched, no git mutation (read-only `git show`/`diff`/`archive` only, plus one
`git archive` into scratch for the counter runs).

Entering `73308ff6e5c933f53498e9501ef95917b0ef7171` (r98 admitted). Frozen contract `.ufo/waves/round-99/contract.md`
at freeze `462cef1cc637de4c6e993aefd00ed9df32895984`, every control executed and committed before the freeze:
`.ufo/waves/round-99/evidence/controls-r99.txt` (`CONTROLS_DONE unexpected=0`, 19 lines `AS_EXPECTED`). Landing
`5013f0be8ac9e7fce3c08b680e43cf9cbd49620d`.

---

## Claims (frozen)

- **C1 operability (score 7)** — `tools/mori-userns-runway.py` (registered probe since r98): its journal write-scan
  now reads sudo's own `COMMAND=` rendering (single quotes only around arguments with a space, backslash-escaped
  `'` and `\`, control characters as `#0nn` — sudo v1.9.17p2 `eventlog.c`/`lbuf.c`, S635/S636), joins
  `(command continued)` lines by pid, reads a `sh -c` script as POSIX words/quotes/comments/operators (S634), skips
  `sysctl -r/--pattern` arguments and ` ; EXIT=` exit events (S633, S635), accepts `journalctl -o short` timestamps
  (S014), and fails closed (`SYSCTL_WRITES_SETUP unparsed=U`, exit 2) on sudo lines it cannot read. Self-test 19
  cases. Knowledge `corpus/knowledge/sudo-log-grammar-r99.md`; rows S633–S636 in `corpus/SOURCES.md`, pinned at
  `corpus/evidence/sources-r99/`. The counter generates its battery at measurement time from a printed seed
  (16 journal families × 3 + 12 fake-`/proc` runway cases), expected answers computed from what it planted.
  Before `C1=unmet cases_ok=24/60 ... checks_failed=battery,sourced`; landing `C1=met cases_ok=60/60 ...
  checks_failed=-`. Disclosed: the r98 capture (filtered on `COMMAND=`, lost a continuation line) now scores the same
  six writes but exits 2 (`unparsed=1`); the full r99 capture scores rc 1, `n=6 userns_zero=2`.
- **C2 calibration (score 5)** — `SCORECARD.md` `## Axes` Evidence cells now lead with a located pointer to the latest
  admitted closure per axis (fleet `MANIFEST.json` at `4ad377eae8e3eed8f7f32ab5d335feb25dbae94b`: coverage r98,
  operability r97, depth r86, freshness r97, calibration r98, adjacency r19 via `rounds[398]`); Last-change cells of
  coverage and calibration gain `round 98 (improved, score held); `. Before `C2=unmet mismatches=5 ... gate=rc1`;
  landing `C2=met mismatches=0 cells_unchanged=yes gate=ok`.

Counter receipts re-run by this seat at both revisions (fresh seeds; frozen counters, frozen instrument bytes):

```
$ python3 .ufo/waves/round-99/count-c1.py --root $D_entering --work $S/w0   # exit=1
C1=unmet cases_ok=24/60 seed=232660927470885 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=unmet checks_failed=battery,sourced
$ python3 .ufo/waves/round-99/count-c1.py --root $D_landing  --work $S/w1   # exit=0
C1=met cases_ok=60/60 seed=217534272179933 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
$ python3 .ufo/waves/round-99/count-c2.py 73308ff6e5c933f53498e9501ef95917b0ef7171   # exit=1
C2=unmet mismatches=5 cells_unchanged=yes gate=rc1 mismatched_axes=coverage,operability,depth,freshness,calibration rev=73308ff6e5c9
$ python3 .ufo/waves/round-99/count-c2.py 5013f0be8ac9e7fce3c08b680e43cf9cbd49620d   # exit=0
C2=met mismatches=0 cells_unchanged=yes gate=ok mismatched_axes=- rev=5013f0be8ac9
```

Committed receipts, verbatim (copied here as cited):

```
C1=unmet cases_ok=24/60 seed=104000810118508 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=unmet checks_failed=battery,sourced   [before-c1.txt, exit=1]
C1=met cases_ok=60/60 seed=222744766262981 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=- rev=5013f0be8ac9e7fce3c08b680e43cf9cbd49620d   [landing-c1.txt, exit=0]
axis coverage expect=round_98 pointer=missing | axis operability expect=round_97 pointer=missing | axis depth expect=round_86 pointer=missing | axis freshness expect=round_97 pointer=missing | axis calibration expect=round_98 pointer=missing | axis adjacency expect=round_19 pointer=ok   [before-c2.txt]
C2=unmet mismatches=5 cells_unchanged=yes gate=rc1 mismatched_axes=coverage,operability,depth,freshness,calibration rev=73308ff6e5c9   [before-c2.txt, exit=1]
C2=met mismatches=0 cells_unchanged=yes gate=ok mismatched_axes=- rev=5013f0be8ac9   [landing-c2.txt, exit=0]
```

`SCORECARD.md` `## Axes`, per-axis cell comparison entering → landing (parsed from the two revisions):

```
coverage    score 6→6 (byte-equal)  Last-change: "round 80 (improved, score held); …" → "round 98 (improved, score held); round 80 …"   Evidence: leading pointer added → corpus/lessons/round-98-verifier-spotcheck.md:89 (round 98, MANIFEST rounds[1389])
operability score 7→7 (byte-equal)  Last-change unchanged ("round 97 …")                                                                   Evidence: → corpus/lessons/round-97-verifier-spotcheck.md:78 (round 97, MANIFEST rounds[1384])
depth       score 5→5 (byte-equal)  Last-change unchanged ("round 86 …")                                                                   Evidence: → corpus/lessons/round-86-verifier-spotcheck.md:145 (round 86, MANIFEST rounds[1205])
freshness   score 5→5 (byte-equal)  Last-change unchanged ("round 97 …")                                                                   Evidence: → corpus/lessons/round-97-verifier-spotcheck.md:79 (round 97, MANIFEST rounds[1384])
calibration score 5→5 (byte-equal)  Last-change: "round 93 (improved, score held); …" → "round 98 (improved, score held); round 93 …"     Evidence: → corpus/lessons/round-98-verifier-spotcheck.md:90 (round 98, MANIFEST rounds[1389])
adjacency   score 6→6 (byte-equal)  Last-change unchanged ("round 19 …")                                                                   Evidence: unchanged (MANIFEST rounds[398], no lane spot-check file)
```

---

## Gate

New rows written this round (CORPUS rule 1), opened 2026-11-05 by the L1 (HTTP 200 each; byte counts and digests are
the SOURCES rows' own), pinned at `corpus/evidence/sources-r99/`:

| row | URL | access (UTC) | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S633 | https://man7.org/linux/man-pages/man8/sysctl.8.html | 2026-11-05T21:55:09Z, HTTP 200, 14152 B, sha256 `a63af3f6…95f3` | "Only apply settings that match pattern." (6 words; pinned copy raw lines 134–136 after tags are stripped — the option header is on 134, the sentence on 135) | admit, mined, tier A |
| S634 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | 2026-11-05T21:55:10Z, HTTP 200, 357953 B, sha256 `0889867a…1acd` | "it and all subsequent characters up to, but excluding, the next <newline> shall be discarded as a comment." (17 words per the row; 18 by whitespace split, because the `<newline>` placeholder is its own token; pinned copy raw lines 303–304) | admit, mined, tier A |
| S635 | https://raw.githubusercontent.com/sudo-project/sudo/v1.9.17p2/lib/eventlog/eventlog.c | 2026-11-05T22:05Z, HTTP 200, 42109 B, sha256 `5bdea0ae…c84b` | "Wrap args containing spaces in single quotes." (7 words, pinned copy line 202) | admit, mined, tier A |
| S636 | https://raw.githubusercontent.com/sudo-project/sudo/v1.9.17p2/lib/util/lbuf.c | 2026-11-05T22:05Z, HTTP 200, 12373 B, sha256 `eda9e0a3…0212` | "Any non-printable characters are escaped in octal as #0nn." (9 words, pinned copy line 145) | admit, mined, tier A |

Pin digests re-verified by this seat (`sha256sum corpus/evidence/sources-r99/*`): `a63af3f6…95f3`, `0889867a…1acd`,
`5bdea0ae…c84b`, `eda9e0a3…0212`, S014 `75440570…9722` — all four match the SOURCES rows exactly.

Row changes logged old→new:

- **S014** (journalctl(1); re-opened 2026-11-05T21:55:11Z, HTTP 200, 87375 B, pinned
  `corpus/evidence/sources-r99/S014-journalctl-r99.html`) — `used-by`:
  `…, corpus/knowledge/journal-cursor-window-r16.md`
  → `…, corpus/knowledge/journal-cursor-window-r16.md, corpus/knowledge/sudo-log-grammar-r99.md`.
  Status (`mined`) and recheck (`on-release`) unchanged; no other cell changed. The re-open's located quote
  ("is the default and generates an output that is mostly identical to the formatting of classic syslog files",
  Output Options `short`, pinned copy lines 194–195 after tags are stripped) is carried in the knowledge entry, not
  in the row.

Rejected this round — **sudo's `main` branch** as the grammar ground (fetched by this seat on 2026-11-05:
`lib/eventlog/eventlog.c` HTTP 200, 43770 B, sha256 `b80c26ec…4774`; `lib/util/lbuf.c` HTTP 200, 12205 B, sha256
`4e0f9d3d…12af`). Reason: the host runs sudo 1.9.17p2 (`/var/lib/pacman/local/sudo-1.9.17.p2-6/desc`:
`%VERSION% 1.9.17.p2-6`; read from the package database, no `sudo` executed), and a reader that inverts a producer's
log grammar must be grounded in the producer at the host's version — `main` can change the rendering without the
host changing, and its line numbers differ (the `COMMAND=` block sits at `main` 216–247 vs the pinned tag's 199–230,
so a quote located on the pin would not locate on `main`). Flip: at the next sudo release the two rows are re-opened
at that tag and the `COMMAND=` block is diffed (the knowledge entry's `recheck:` line says exactly this). Note for
the L1: this rejection is about the *pinned ground*, not about drift — the `COMMAND=` block and the `escape()` /
`should_quote` code are byte-identical between the tag and `main` (`diff` of the two block ranges is empty), so no
grammar change is pending upstream.

Second candidate considered and refused, not opened: **sudoers(5)** for `syslog_maxlen`. The tool never needs the
configured length — it treats any `sudo[pid]: … : (command continued) …` line as a continuation of that pid's
command and joins it with one space — so no row was opened and no default value is asserted anywhere this round.
Flip: a claim that needs the host's configured `syslog_maxlen` opens sudoers(5) as its own row.

---

## Mistakes (CORPUS: class · evidence · captured-by · fix)

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| 1 | capture-truncation | The r98 capture is exactly the `COMMAND=`-filtered view of the same window: `grep 'COMMAND=' .ufo/waves/round-99/evidence/journal-incident-r99.txt` is byte-identical to `.ufo/waves/round-98/evidence/journal-incident-r98.txt` (both sha256 `978504134c53a4a4b404bf5175b51aa31f5afd27ad62cd517e4a2fbc2cd79738`, 276 lines), so the `(command continued)` line — one of the 829 `sudo[` lines of the r99 capture, 1 continuation + 552 `pam_unix` + 276 `COMMAND=` — was dropped and the command truncated. | none before this round: the r98 counter's incident case read the truncated capture and passed, so the loss changed no count. | The r99 capture keeps every `sudo[` line of the window (`journal-incident-r99.txt`, sha256 `7ec650c9…090d`, the digest `count-c1.py` pins), and the tool joins a continuation onto its pid's command and **fails closed** on a command whose quoted argument is still open at the end (`SYSCTL_WRITES_SETUP unparsed=1`, exit 2) instead of reading it as "no write". Shown able to fail: the landed tool on the r98 capture prints `SYSCTL_WRITES n=6 keys=1 userns_zero=2` **and** `SYSCTL_WRITES_SETUP unparsed=1`, exit 2; on the full r99 capture it prints the same six writes with no setup line, exit 1; the frozen control `K5-no-continuation` scores `checks_failed=selftest,battery,incident` with `incident=fail(rc=2)`. |
| 2 | silent-fallback | The r98 classifier read sudo's `COMMAND=` text with a POSIX splitter and, on `ValueError`, silently fell back to `cmd.split()` (`tools/mori-userns-runway.py` at entering: `split_cmd` = `try: return shlex.split(cmd) / except ValueError: return cmd.split()`). sudo escapes `'` and `\` inside an argument, so a POSIX splitter reads `\'` inside single quotes as the end of the quote: `shlex.split` raises "No closing quotation" on 24 of the capture's 276 `COMMAND=` lines (e.g. pid 1863991, tail `(\'/tmp/hello\').read() if __import__(\'os\')…`), and the fallback then re-splits on whitespace with nothing in the output saying so. The fallback was harmless *on this capture* — 0 of those 24 lines carries a `sysctl` write or a `/proc/sys` path — which is why the six-write count never moved. | none before this round: the r98 counter did not exercise sudo's quoting, and the r98 tool's own output reported no fallback. | The tool now inverts sudo's own rendering (S635/S636) instead of a generic splitter, reads a `-c` script with the POSIX shell rules the producer's escapes imply (S634), and counts any line it cannot read as `unparsed` and exits 2. Shown able to fail: the frozen control `K4-no-sudo-unquote` scores `selftest=fail … cases_ok=57/60`, `K6-fail-open` scores `cases_ok=54/60`, and the entering tool scores `cases_ok=24/60` on the same generated battery (`checks_failed=battery`); the misreading itself is directly observable — `shlex.split` raises on 24 of the capture's 276 `COMMAND=` lines while the landed tool reads the capture with `unparsed` absent (exit 1). |
| 3 | vacuous-control | First pre-freeze control run: `control K8-no-exit-skip expect=unmet got=met rc=0 UNEXPECTED` (the mutant was equivalent to the candidate under the draft R4 family, because `split_cmd` already stripped the exit suffix, so no case distinguished it) and `control K11-rows-not-mined expect=unmet got=met rc=0 UNEXPECTED` (the control's own regex matched no row, so the rows stayed `mined` and the "not mined" tree was indistinguishable); `CONTROLS_DONE unexpected=2 K8-no-exit-skip,K11-rows-not-mined`. | the pre-freeze control run itself (`.ufo/waves/round-99/evidence/controls-draft-prefreeze-r99.txt`), before the freeze — the draft receipt is kept. | Fixed before the freeze: R4 now plants an accept **and** an exit-event line for one write (a tool that does not skip exit events double-counts it — the frozen `count-c1.py` R4 family returns two lines and one expected write), and the K11 mutation now rewrites the `mined` status of rows S633–S636 to `proposed` with a regex that counts 6 cells before the status cell (the draft's regex matched no row). Shown able to fail: the frozen `evidence/controls-r99.txt` records `K8-no-exit-skip … checks_failed=battery` and `K11-rows-not-mined … checks_failed=sourced`, both `AS_EXPECTED`, ending `CONTROLS_DONE unexpected=0`. |
| 4 | number-drift | The frozen contract ("25 of the incident capture's sudo lines fail it and fall back to whitespace split") and `corpus/QUALITY.md` 210 ("on the 2026-11-05 capture 25 sudo lines fail its POSIX splitter and fall back to whitespace splitting without any output saying so") carry the number 25. Under the entering tool's own code path the number of lines that *fall back* is **24**: `scan_journal` requires `" COMMAND=" in line`, so it splits only the 276 `COMMAND=` values and never the continuation line, and 24 of those 276 `split_cmd` calls raise `ValueError` and take the `cmd.split()` branch. The figure 25 is reachable only by a different reading of the same file, and there are two: (a) read *every* sudo line's body — 24 `COMMAND=` bodies plus the one `(command continued)` body also raise "No closing quotation" (25 of 829); (b) join the continuation onto its pid's command first, as the r99 reader does, and 25 of the 276 joined commands raise, the extra one being pid 1749648 (`(command continued) … printf \'%s | %s\\n\' …`). Same capture, three numbers; the sentence as written does not carry its command, and in reading (a) one of the 25 lines is never split at all, so it cannot "fall back to whitespace splitting". | this seat's measurement (`w1/Mo99ScribeLesson.md`), after the freeze; no pre-freeze control exercised the fallback count. | The count must name the reading it counts, as r98's lesson recorded ("a count carries its command"): write "24 of the capture's 276 `COMMAND=` lines fall back to whitespace split under the entering reader (25 sudo lines fail the splitter if the continuation line is read as well)". Shown able to fail: the three commands print three different numbers for the same file — `scanned_command_lines=276 shlex_ValueError_fallbacks=24` (entering reader), `all sudo lines=829 shlex-fail over every line body=25 by kind={'CONTINUED': 1, 'COMMAND': 24}`, `joined commands=276 shlex_fail=25` (joined reading). |

Reproduction commands for the evidence in the table (scratch only; the captures are cited by path and digest, not
copied into this file):

```
# mistake 1 — the r98 capture is the COMMAND= filter of the r99 capture
grep 'COMMAND=' .ufo/waves/round-99/evidence/journal-incident-r99.txt > $S/filtered99.txt
cmp $S/filtered99.txt .ufo/waves/round-98/evidence/journal-incident-r98.txt   # identical
sha256sum $S/filtered99.txt .ufo/waves/round-98/evidence/journal-incident-r98.txt
978504134c53a4a4b404bf5175b51aa31f5afd27ad62cd517e4a2fbc2cd79738  $S/filtered99.txt
978504134c53a4a4b404bf5175b51aa31f5afd27ad62cd517e4a2fbc2cd79738  .../round-98/evidence/journal-incident-r98.txt
# 829 sudo[ lines in the r99 capture: 276 with COMMAND=, 1 "(command continued)", 552 pam_unix

# mistake 2 — the entering reader's silent fallback, and the landing tool's fail-closed answer
python3 -c "…(instrumented split_cmd over the capture)…"   # split_cmd calls=276 whitespace_fallback=24 writes=6   (both captures)
python3 tool-landing.py --journal .ufo/waves/round-98/evidence/journal-incident-r98.txt   # rc=2, SYSCTL_WRITES_SETUP unparsed=1
python3 tool-landing.py --journal .ufo/waves/round-99/evidence/journal-incident-r99.txt   # rc=1, SYSCTL_WRITES n=6 keys=1 userns_zero=2

# mistake 4 — the two counts for the same file
entering reader:  scanned_command_lines=276 shlex_ValueError_fallbacks=24
joined reading:   joined commands=276 shlex_fail=25   (extra pid: 1749648)
```

Receipt lines cited above, copied verbatim from the frozen receipts:

```
# .ufo/waves/round-99/evidence/controls-r99.txt
control K4-no-sudo-unquote expect=unmet got=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=57/60 seed=990099 selftest=fail live=ok(limit=122865,used_lb=8,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
control K5-no-continuation expect=unmet got=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=57/60 seed=990099 selftest=fail live=ok(limit=122865,used_lb=8,state=ok) incident=fail(rc=2) registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery,incident
control K6-fail-open expect=unmet got=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=54/60 seed=990099 selftest=fail live=ok(limit=122865,used_lb=8,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
control K8-no-exit-skip expect=unmet got=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=57/60 seed=990099 selftest=ok live=ok(limit=122865,used_lb=7,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=battery
control K11-rows-not-mined expect=unmet got=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=60/60 seed=990099 selftest=ok live=ok(limit=122865,used_lb=7,state=ok) incident=ok registry=met sourced=unmet checks_failed=sourced
CONTROLS_DONE unexpected=0

# .ufo/waves/round-99/evidence/controls-draft-prefreeze-r99.txt
control K8-no-exit-skip expect=unmet got=met rc=0 UNEXPECTED :: C1=met cases_ok=60/60 seed=990099 selftest=ok live=ok(limit=122865,used_lb=7,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
control K11-rows-not-mined expect=unmet got=met rc=0 UNEXPECTED :: C1=met cases_ok=60/60 seed=990099 selftest=ok live=ok(limit=122865,used_lb=7,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
CONTROLS_DONE unexpected=2 K8-no-exit-skip,K11-rows-not-mined
```

Tools installed: none. No `pacman`, no `uv tool install`, no network install — every command above used `git`,
`python3`, `grep`, `sha256sum`, `cmp`, `sed` and `curl` (read-only fetch of the two sudo `main` files, both HTTP 200).

Note for the L1 (observed, not edited by this seat): the working tree now carries post-landing w1 review fixes on top
of `5013f0be` — `SKILL.md`, `corpus/knowledge/sudo-log-grammar-r99.md` and `tools/mori-userns-runway.py` are modified
in the worktree (the self-test is described there as "19 cases at landing `5013f0be`, 22 after the post-landing
fixes"), and `corpus/QUALITY.md` carries the uncommitted criteria 210–211. The landed tool's self-test is 19 cases
(`MORI_USERNS_RUNWAY_SELFTEST: PASS (19 cases)`, exit 0, measured at `5013f0be`); the 22-case figure belongs to the
uncommitted worktree, not to the landing bytes. This draft quotes only the landing bytes.

Unrun checks (named, not claimed): `sudo --version` was not executed (seat rules forbid running sudo on this host);
the host's sudo version is read from `/var/lib/pacman/local/sudo-1.9.17.p2-6/desc`. The r99 wave's other seats'
reports were not consulted for this draft beyond `w1/Mo99ScoutSrc.md` (source re-verification) and the frozen
receipts; the L1's in-progress `corpus/lessons/round-99.md` was read once for shape and was not edited.

Report: .ufo/waves/round-99/w1/Mo99ScribeLesson.md
