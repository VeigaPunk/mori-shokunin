# mori round 99 — frozen claim contract (L1 MoriR99, attempt 1)

Entering revision: `73308ff6e5c933f53498e9501ef95917b0ef7171` (master = origin/master, `jj-lane.sh state`:
ahead=0 behind=0 tracked=0 untracked=0). Fresh-start authorization (prompt Amendment 35) covers mori; the last three
rejected closures (r94, r95, r96 — `corpus/lessons/round-9{4,5,6}-verifier-spotcheck.md`) failed on predicates a
do-nothing control already met (r95 C2, QUALITY 208), on an operability claim whose axis-move a critic broke (r94
K01), and on a freshness predicate the vendor stamp could not meet (r96). r97 and r98 were admitted. The r98
closure routed D1 (a fixture-shape lookup stub passes the frozen r98 counter; QUALITY 209), D2 (mutant m03 and
classifier gaps F1–F3), D3 (Evidence cells cite superseded closures). This contract binds, before any wave output,
do-nothing controls that FAIL at entering, forgery and single-fix-removed mutants through the tool's public CLI, and
positive controls — executed and committed with this freeze: `evidence/controls-r99.txt`, produced by
`controls-r99.py --lane <lane> --entering 73308ff6… --scratch <dir>`. The first draft run is kept as
`evidence/controls-draft-prefreeze-r99.txt` (two UNEXPECTED, fixed before this freeze; lesson Mistakes).

Frozen instrument bytes (sha256 prefixes on the first line of `evidence/controls-r99.txt`): `count-c1.py`,
`count-c2.py`, `controls-r99.py`, the candidate tool `candidate/tools/mori-userns-runway.py`, the C2 transform
`candidate/apply-c2.py`, the landing bytes of `SKILL.md`, `corpus/SOURCES.md` and
`corpus/knowledge/sudo-log-grammar-r99.md`, and the incident capture `evidence/journal-incident-r99.txt` (sha256
pinned inside `count-c1.py`). Never edited after this freeze; a defect found later is reported, not patched.

## C1 — operability (score 7): the write scan reads sudo's real log grammar and a shell script as a shell does

Surface moved: the runnable instrument `tools/mori-userns-runway.py` (registered probe, r98) — its journal-scan
input classes. AXES.md operability: "A checklist item can be run and produces the stated outcome." At entering the
scan's stated outcome fails on real input classes (`w1/Mo98RevC1.md` F1–F3 and this round's capture study):
sudo's own `COMMAND=` quoting (`\'`, `#012`) is read by a POSIX splitter (25 of the incident capture's sudo lines
fail it and fall back to whitespace split), `(command continued)` lines are dropped, a `-c` script is matched by
regexes that fire inside quotes and comments and miss `printf`, nested `sysctl`, `env` prefixes and fd
redirections, `sysctl -r PATTERN` and ` ; EXIT=` words are read as writes, and the default `journalctl -o short`
timestamp makes a write read as "no write" (rc 0). Candidate bytes: `candidate/tools/mori-userns-runway.py`
(sudo-rendering inverter, continuation join by pid, POSIX token reader, fail-closed `SYSCTL_WRITES_SETUP
unparsed=U` exit 2, 19-case self-test). The runway read is unchanged (m03 clamp now has a fixture).

Predicate P1 (same sentence as `count-c1.py` docstring): on the tree DIR of revision R, (a) `--selftest` exits 0
with `MORI_USERNS_RUNWAY_SELFTEST: PASS (<n> cases)`; (b) the tool answers every case of a battery generated at
measurement time from a printed seed (16 journal families × 3 instances in sudo's own `COMMAND=` rendering, 12
fake-/proc runway cases), each expected answer computed by the counter from what it planted — journal cases match
rc, summary and the (key, value) multiset; runway cases match rc and the whole line; (c) a live run agrees with
the counter's own read of the limit and the distinct non-initial `ns/user` links in one of 3 attempts; (d) the
full round-99 incident capture (sha256 pinned) scores rc 1, `SYSCTL_WRITES n=6 keys=1 userns_zero=2`, the six
pinned writes, no setup line; (e) the gate auditor prints `REGISTRY=met`; (f)
`corpus/knowledge/sudo-log-grammar-r99.md` cites in a `source:` line an S-id above S632 whose row is `mined` and
lists that path in `used-by`.

Counter: `git -C <lane> archive R | tar -x -C DIR`, then `python3 .ufo/waves/round-99/count-c1.py --root DIR
[--seed N] [--work SCRATCH]`. Label `C1=met` / `C1=unmet`.
Before (do-nothing, entering): `C1=unmet cases_ok=24/60 ... checks_failed=battery,sourced` exit 1
(`evidence/before-c1.txt`).
Target (after, landing): `C1=met cases_ok=60/60 ... incident=ok registry=met sourced=met(S...) checks_failed=-`
exit 0, on any seed.
Kill rule: any other output at the landing revision is unmet; no re-declaration, no counter edit.
Controls (committed, pre-freeze): K0 do-nothing; K1 constant printer; K2 lookup forgery (the candidate's own
self-test journals answered by sha256, everything else by the entering tool — QUALITY 209); K3–K9 the candidate
with one fix removed each (comment, sudo unquote, continuation, fail-closed, `-r` skip, exit-event skip, runway
clamp m03); K10 no knowledge entry; K11 rows not mined → all `unmet`; P1 the full candidate → `met`.

Sourced: S633 sysctl(8), S634 POSIX XCU ch. 2, S635 sudo eventlog.c v1.9.17p2, S636 sudo lbuf.c v1.9.17p2 — opened
this round, pinned at `corpus/evidence/sources-r99/`; S014 journalctl(1) re-opened (used-by gains the new entry).

Disclosed behaviour change: the round-98 capture `.ufo/waves/round-98/evidence/journal-incident-r98.txt` was
filtered on `COMMAND=` and lost one `(command continued)` line; the candidate scores the same six writes on it but
exits 2 (`SYSCTL_WRITES_SETUP unparsed=1`), so the frozen r98 counter's J1 case no longer holds at landing. That is
the fail-closed rule applied to a truncated capture, not a lost capability: the full capture (every `sudo[` line
of the same window, re-read from this host's journal) scores rc 1 with the same writes.

## C2 — calibration (score 5, lowest non-retired tier): SCORECARD Axes cells point at the admitted record

Surface moved: SCORECARD.md `## Axes` — the Evidence cells (r98 D3: five cells cite closures that later admitted
closures supersede) and the Last-change cells of coverage and calibration (graded improved by the admitted r98
closure, MANIFEST rounds[1389]; the cells lead with rounds 80 and 93). AXES.md calibration: "SHONEN.md/SCORECARD
entries match observed repo state"; §9: a calibration claim counts mismatches between self-assessment and record.

Predicate P2 (same sentence as `count-c2.py` docstring): at revision R, every `## Axes` Evidence cell carries a
located pointer to the highest admitted mori closure grading that axis improved/harmed in MANIFEST.json at fleet
`4ad377ea` (`corpus/lessons/round-N-verifier-spotcheck.md:L` with line L naming the axis and the verdict word, or
`rounds[I]` when no spot-check file exists), every Score cell is byte-equal to entering, every Last-change cell is
entering bytes or one prepended `round N (verdict, score held); ` clause, and the registered calibration gate
(entering bytes) run with `--base R` prints `C1=met`.

Counter: `python3 .ufo/waves/round-99/count-c2.py R`. Label `C2=met` / `C2=unmet`.
Before (entering): `C2=unmet mismatches=5 cells_unchanged=yes gate=rc1
mismatched_axes=coverage,operability,depth,freshness,calibration` exit 1 (`evidence/before-c2.txt`).
Target (landing): `C2=met mismatches=0 cells_unchanged=yes gate=ok mismatched_axes=-` exit 0.
Kill rule: any other output at the landing revision is unmet.
Controls (fixture clones, pre-freeze): K0c do-nothing, K1c pointers without the Last-change clauses, K2c wrong
round, K3c wrong line, K4c Score edited → `unmet`; P1c the candidate transform → `met`.

## Causal separation

C1 touches `tools/mori-userns-runway.py`, the tool's SKILL.md registry row, `corpus/knowledge/`, `corpus/SOURCES.md`
and evidence files; C2 touches only SCORECARD `## Axes` cells. C1's counter reads no SCORECARD byte; C2's counter
reads SCORECARD, the spot-check files and the pinned MANIFEST only.
