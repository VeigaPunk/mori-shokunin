# CensusStartCheck — wave 1 report (mori round 31)

Seat: `MoriR31.CensusStartCheck`. Method: read-only validator run on the real fleet
root, then sandbox probes under `/fast/scratch/hyaku/mori-r31/CensusStartCheck/`
(clone + temporary fleet-root layout + vocabulary-probe lane). Script **never
edited**; every finding is from execution output or from `scripts/sources-census.sh`
line numbers.

## 1. Validator run on the real fleet root (read-only)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
$ echo $?
0
```

Exit code 0. The 10 `W04` lines are warnings (same normalized URL across scopes) and
do not affect exit status (script header lines 31–33; `W04` emitted at gawk line 645,
exit handling: `[ "$findings" = 1 ] && exit 1` at end of file, findings only set by
`E[0-9]+` lines, header line 16). `mori ok <file>` means the lane had no E-code
findings (`[ "$lane_errors" = 1 ] || emit "$lane	ok	$f"`).

## 2. How the validator sees a lane

- Target selection (`resolve_targets`, line 495): explicit lane name → roster lookup;
  explicit directory (contains `/`) → validated directly (lines 512–514, 521–523).
- Roster (`build_roster`, line 452): parses `$ROOT/shokunin.conf` textually with sed
  (line 470); conf entries whose repo is `.` are skipped (line 466); unlisted
  `$ROOT/*-shokunin` dirs are appended by glob (line 472). `mori` is listed in the
  real conf (`/home/vgpnk/Projects/shokunin/shokunin.conf:63`:
  `mori|mori-shokunin|...`), which is why no `unlisted` row appeared.
- `--root DIR` works with a temporary fleet-root layout: it only needs
  `$ROOT/shokunin.conf` (die if missing, line 453) and the lane dirs; the script never
  touches anything outside `$ROOT` except the explicit args. (Verified — section 4.)
- Row parsing (gawk in `row_pass`, line 574): only rows inside the `## Registry`
  section count (section flag set/cleared on headings, lines ~610–621); 0–3 leading
  spaces allowed (lines 540–541 and gawk regex `^ {0,3}\|`); separator rows skipped;
  a row-shaped `S...` outside Registry → E12 (line 621).
- Row shape: `-F'|'` → a full row has NF=13 (11 data cells). `fields=%d` in E01
  reports NF−2 (line 636).

## 3. Checks a new S161+ row must satisfy (script line numbers)

| Code | Check | Script lines | Empirically confirmed by |
|---|---|---|---|
| E01 | Exactly 11 cells (NF=13) | 635–636 | S814 short row → `E01 S814 fields=10` |
| E02 | id matches `^S[0-9]{3,}$` | 640 | X99 → `E02 X99` |
| E03 | id not already seen in registry | 641 | (selftest fixture) |
| E04 | URL not duplicated within the same scope unless status=rejected or teaches contains `supersedes S[0-9]{3}` | 646–649 | S812 vs S811 same scope → `E04 duplicate url probe.example/s811 within scope p` |
| W04 | Same URL in different scopes (warning only) | 644–645 | real run: S035/S037/... |
| E05 | kind ∈ `spec|docs|paper|code|tool|dataset|talk|book|community|own-work` | 655–656 | S803 kind=webpage → E05 |
| E06 | tier ∈ `A|B|C` | 657 | S804 tier=Z → E06 |
| E07 | status ∈ `queued|mined|rejected` | 658–659 | S802 status=watch → E07 |
| E08 | opened is a valid ISO date ≤ today | 660–662 | S805 opened=2027-01-01 → E08 |
| E09 | recheck is ISO date, `NNd`, or symbolic `^[A-Za-z][A-Za-z0-9 _-]*$` | 663–666 | S806 recheck=7x → E09 |
| E10 | tier=A and kind=community forbidden | 668 | S808 → `E10 community-at-A` |
| W01 | tier=C with status=mined and used-by ≠ `—` (warning) | 669–670 | S810 → W01 |
| W02 | status=rejected with teaches < 8 chars (warning) | 671–672 | S809 → W02 |
| W03 | status=mined with used-by = `—` (warning) | 673–674 | S807 → W03 |
| E11 | Every used-by path must exist on disk **relative to that lane's directory** | 538, 566–567 | S811 → E11; also S810 → E11 because the path exists in mori's repo but not in the probe lane (`usedby_findings` uses `$dir/$path`) |
| E12 | No row-shaped source outside `## Registry` | 621 | S815 → E12 |

Exit semantics (header lines 16–18): 0 = clean or warnings-only; 1 = E-findings
(overdue, or missing registry in census); 2 = usage/env/missing registry; 3 =
selftest. W-codes never flip status.

## 4. Sandbox probe: well-formed S161 row passes

Setup (all under scratch):

```
/fast/scratch/hyaku/mori-r31/CensusStartCheck/
  sandbox/                 # git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin
  fleet-root/
    shokunin.conf          # LANES="mori|mori-shokunin|probe lane"
    mori-shokunin/         # cp -a of the clone
    probe-shokunin/        # vocabulary probe lane
```

Baseline validate on `fleet-root` reproduced the exact real-run output (same 10 W04s,
`mori ok`, exit 0). Then the dummy row was appended inside `## Registry` right after
S160 (line 167 of the copy):

```
| S161 | Probe source — https://example.invalid/probe-s161 | code | A | probe: sources-census validator checks for a new row | probe:1-2 | Dummy well-formed row proving a new S161+ row passes every registry field check. | mined | 2026-10-22 | on-release | corpus/lessons/round-30-verifier-spotcheck.md |
```

Result: identical output, `mori ok`, exit 0 — no finding names S161. So a conforming
S161+ row passes when: NF=13; id `S\d{3,}`; id and URL+scope not duplicated (or E04
exemption met); kind/tier/status from the fixed vocabularies; opened ≤ today; recheck
in the accepted vocab; not community+A; and every used-by path exists in the lane at
validation time. To stay warning-free for a *mined* row: used-by must list ≥1 existing
file (else W03), teaches should be ≥8 chars, and tier C+mined must not carry used-by
(else W01).

## 5. Vocabulary probe: every code reproduced in one run

`probe-shokunin` registry (one violating row per check) full validate output:

```
probe-shokunin	E07	S802 status=watch
probe-shokunin	E05	S803 kind=webpage
probe-shokunin	E06	S804 tier=Z
probe-shokunin	E08	S805 opened=2027-01-01
probe-shokunin	E09	S806 recheck=7x
probe-shokunin	W03	S807 mined but unused
probe-shokunin	E10	S808 community-at-A
probe-shokunin	W02	S809 thin reject reason
probe-shokunin	W01	S810 tierC mined used-by=corpus/lessons/round-30-verifier-spotcheck.md
probe-shokunin	E04	S812 duplicate url probe.example/s811 within scope p
probe-shokunin	E02	X99
probe-shokunin	E01	S814 fields=10
probe-shokunin	E12	S815 row outside Registry section
probe-shokunin	E11	S810 missing used-by corpus/lessons/round-30-verifier-spotcheck.md
probe-shokunin	E11	S811 missing used-by corpus/nope/missing.md
EXIT=1
```

All codes E01–E12 and W01–W03 reproduced; E11 resolution is lane-relative (confirmed by
S810 firing in the probe lane for a path that exists in mori's own repo). Exit 1
confirmed for E-findings.

## 6. Risks / notes for C1/C2 seats

- A new S161+ row with used-by pointing at a not-yet-created C1 deliverable (e.g.
  `corpus/knowledge/watchdog-identity-r31.md`) will fail validation with E11 until that
  file exists. Order matters: create the used-by files before running `validate`, or
  use `queued` + `—` (only W03-free rule is for mined rows; queued rows with `—` are
  clean).
- Same URL in a different scope is only W04 (exit 0); same URL in the same scope is
  E04 unless the row is `rejected` or its teaches says `supersedes S###` (lines
  646–648) — the standard route for corrections.
- `--root` + temp fleet-root layout works; a single explicit lane dir also validates
  with no conf at all (lines 512–514).
- No tools installed (generic-rules record: none needed; nothing added or updated).
- All commands ran under `timeout 120`; no background jobs; no repo mutations outside
  scratch; script untouched.
