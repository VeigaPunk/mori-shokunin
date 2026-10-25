# ScribeRegistryRows — round-45 registry rows (draft only; SKILL.md not edited)

Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`. Worktree HEAD at start `3ad8faaa637ae466c61f9427fea1c208bf49ea82`
(the round-45 freeze commit); the contract's entering tip is `554ff416459c92f0…`. Scratch
`TMPDIR=<lane>/.ufo/waves/round-45/tmp/ScribeRegistryRows` (created by this seat). No tool was installed or
upgraded during this seat. Every command below ran read-only against the lane; no lane file was written by me
except this report and the per-run scratch files under my `TMPDIR` (the clone in §5 is a throwaway copy).

**Deliverable: 10 rows**, all copy-paste Markdown, all eight cells non-empty and free of a raw `|`:
3 tool rows (item 1), 3 round-45 counter rows (item 2), 4 append-only superseding rows (item 3, corrected to
four by the L1's message of this wave), plus the routed-r24 cell replacement (item 4).

**Where they go:** immediately after `SKILL.md:186` (the `r44 corpus coverage (C3)` row), i.e. as the last rows
of the `## Gates` table, before the blank line that is now `SKILL.md:187`. Inserted there they become lines
**187–196**, and the prose now at `SKILL.md:187-188` (`Round19 freeze receipt entry supersedes…`) shifts to
`197-198`. The four superseding rows must stay *after* rows 183–186: the registry's own attribution rule for the
write-scope arm is "the last such row in document order supersedes earlier ones"
(`.ufo/waves/round-45/fixtures/write-scope.json`, key `source.attribution`; `evidence/write-scope.txt:31-35`).

**Row-count arithmetic the L1 asked for.** The auditor v2 over the declared population, measured in a throwaway
clone (§5), moved during this seat because residual seats were landing selftest branches while I measured:

| clone state | registered | unregistered | no_selftest | duplicate | wrong_row | tables | verdict |
|---|---|---|---|---|---|---|---|
| before my rows, HEAD tools | 29 | 6 | 4 | 0 | 0 | 7 | `unmet` |
| my rows + the three ExecSelftestModes branches | 36 | 0 | 3 | 0 | 0 | 7 | `unmet` |
| my rows + every branch this wave has now landed | 39 | 0 | 0 | 0 | 0 | 7 | `met` |

My six registering rows close `unregistered` 6 → 0 exactly. The middle row is the honest intermediate state:
`tools/mori-disk-rate.py` and `tools/mori-round41-calibration.py` had no selftest at all, so registering them
*moved two paths into* `no_selftest` (v2 has no escape for "none" — `tools/mori-gate-registry.py:389-396`,
`declared_flag(cells[4])` only lets a row name a *different* flag), and routed-r24's branch had not landed. The
last row is the state at the end of this seat: those two tools and routed-r24 now carry real branches (§1, §4,
measured tallies below), and the final clone audit reads
`registered=39 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=7`, `REGISTRY=met` rc 0.
**P-C2 clause 5 is reachable with these rows because the branches landed — the rows alone cannot make
`no_selftest=0`.**

## 1. The three tools that had no row

### Evidence (every command run; rc pasted)

```
$ python3 tools/mori-disk-rate.py --help                     rc=0
usage: mori-disk-rate.py [-h] [--a FILE] [--b FILE] [--sysfs DIR] --interval-ms N
$ python3 tools/mori-wave-settlement.py --help                rc=0
usage: mori-wave-settlement.py [-h] {scan} ...        # scan only; no --selftest in help
$ python3 tools/mori-round41-calibration.py --help            rc=0
usage: mori-round41-calibration.py [-h] --repo REPO --reference-rev REFERENCE_REV revision

# disk-rate, live, TMPDIR set (bounded, 200 ms):  rc=0
{"devices": {...}, "host_basis": ["nvme0n1","nvme1n1","sda","sr0"], "host_write_Bps": 0}
# …11 devices; nvme/dm/sr0 classified disk/stacked/virtual per R3
# disk-rate, offline pair (sda sectors 5000 -> 9000 over 1000 ms):  rc=0
"sda": {"class": "disk", "state": "ok", "write_Bps": 2048000}      # (9000-5000)*512*1000//1000
# disk-rate, --a without --b:   rc=2   "mori-disk-rate.py: error: --a and --b must be given together, or neither"
# disk-rate, --interval-ms 0:   rc=2   "mori-disk-rate.py: error: --interval-ms must be a positive number of milliseconds"
# disk-rate, unreadable sample: rc=1   "mori-disk-rate.py: cannot read the sample(s) given"

# wave-settlement, current lane, --out to scratch:  rc=1
totals {"waves": 46, "members": 2273, "present": 1900, "missing": 371, "states": {"settled": 27, "partial": 18, "unsettled": 1}}
sha256(--out file) == sha256(stdout) == a208f0a7c38a281b15ffafeb449d0dd903e632d8243fa1ab9a4ea584416c04d2
# wave-settlement --selftest:  rc=0
MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)

# r41 calibration at 554ff416 with --reference-rev 554ff416:  rc=1
SCORECARD.md recorded_as_of=35 observed_as_of=37 recorded_extension=17 observed_extension=19
LOG.md … same … corpus/lessons/round-40.md … same …
MORI_R41_CALIBRATION mismatches=6 observed_as_of=37 extension_rows=19
```

Notes that shaped the cells:
- **Selftest status changed under this seat.** When it began, `mori-disk-rate.py` and
  `mori-round41-calibration.py` had **no** `--selftest` (`grep -c -- --selftest` = 0 for both, `--help` listed
  none), which is the round-46 finding the wave expected. Both branches landed during the seat and I measured
  them (`MORI_DISK_RATE_SELFTEST pass=14 fail=0`, `MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0`, rc 0 each), so
  the cells name the delivered branch; F-R45-1 keeps the earlier state as withdrawn history.
- `mori-disk-rate.py`'s docstring stdout sentence (lines 35-36) still documents only rc 0 and rc 2; rc 1
  (unreadable sample, `mori-disk-rate.py:495`) and the selftest's rc 1/2 are real and undeclared there —
  round-46 finding.
- `mori-wave-settlement.py --selftest` **does** exist but is invisible to `--help`: `main()` intercepts
  `args_list == ["--selftest"]` before argparse (`tools/mori-wave-settlement.py:686-688`), and the only
  registered subcommand is `scan`. The row therefore prints the exact invocation rather than "`--selftest`".
- `mori-round41-calibration.py` at the current tip exits 1 *by design*: it compares three round-40 record
  files with the round-40 gate re-run at `--reference-rev`; those records moved after round 40. The row says so,
  so a later reader does not score the rc-1 as a regression.
- The `wave-settlement` totals above are a **snapshot, not a pin**: its scan walks every `*dispatch*.json`
  under `<lane>/.ufo/waves`, and sibling seats' scratch fixture repos under
  `.ufo/waves/round-45/tmp/**` contained 162 such files during this seat. A second run of the same command
  during the same wave read `waves=182 members=9018` (`settled=108 partial=74`). The row pins the schema, the
  oracle and the regex, never a wave count.

### Rows (item 1 — 3 rows)

| disk write rate (r34) | probe | `python3 tools/mori-disk-rate.py --interval-ms N` (live: read, wait N ms, read again; `--a FILE --b FILE` for two saved samples; `--sysfs DIR` default `/sys`) | 0 → one JSON report on stdout (`interval_ms`, `devices`, `host_basis`, `host_write_Bps`), every state other than `ok` carrying `write_Bps` null and never zero · 1 → a requested sample cannot be read (`mori-disk-rate.py: cannot read the sample(s) given`) · 2 → usage (`--interval-ms` not positive, or `--a` and `--b` given singly); the docstring's stdout sentence names only 0 and 2, so both the sample rc 1 and the selftest rc 1 are undeclared there — round-46 finding | `python3 tools/mori-disk-rate.py --selftest` → measured `MORI_DISK_RATE_SELFTEST pass=14 fail=0` rc 0, added round 45: it runs against synthetic samples and a synthetic sysfs root under the caller TMPDIR (no live `/proc` or `/sys` read) and exits 1 on a failing arm, 2 when the fixtures cannot be built; while it did not exist, the able-to-fail evidence was the offline pair (rc 0, sda state ok at 2048000 B/s), the unreadable sample (rc 1) and the two usage arms (rc 2) quoted in `.ufo/waves/round-45/w1/ScribeRegistryRows.md` | `SECTOR_BYTES = 512`; `VALID_TOKEN_COUNTS = (14, 18, 20)`; sectors-written is token 10 (`SECTORS_WRITTEN_INDEX = 9`); class and state order R1–R7 of `.ufo/waves/round-34/contract.md` §C1; sources S180–S198 | writes nothing: it creates no file, and `/proc/diskstats` (or the `--a` and `--b` files) plus `<sysfs>/class/block` are read only | mori |
| wave settlement (r20) | gate | `python3 tools/mori-wave-settlement.py scan --lane-root DIR [--fleet-root DIR] [--out PATH]`; `python3 tools/mori-wave-settlement.py --selftest` (accepted only as the sole argument, and absent from `--help`, whose only subcommand is `scan`) | 0 → every scanned wave is `settled` or `no-spawn` · 1 → any wave is `partial`, `unsettled` or `unavailable` (missing, empty, stub, unsafe or misrooted members) · 2 → the lane root is unreadable or not a directory, the fleet root is not a directory, or `--out` cannot be written; `ignored_json` and `unreadable_json` are counted and never flip the verdict | `python3 tools/mori-wave-settlement.py --selftest` → measured `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)` rc 0 = the 14 frozen cases in `.ufo/waves/round-20/frozen/c2-expected.json` plus the 9 in-script `REFINEMENT_CASES` (R1–R5, r6 missing taskCall, r7 `..` component, r8 symlinked parent), each case built under `tempfile.TemporaryDirectory(dir=$TMPDIR)` | `.ufo/waves/round-20/frozen/c2-expected.json` (the frozen 14, never edited); schema `mori-wave-settlement-v1` and dispatch `ufo-swarm-wave-dispatch-v1`; trailer regex `^Report: write your scoped findings to (\S+)$`; `STATUS_NAMES` = present, empty, stub, missing, misrooted, unsafe, unparsed | stdout is one JSON object; `--out PATH` writes exactly that file, creating its parent directories, and no other repo path is written; the selftest writes only under the caller TMPDIR; a `..` component or a symlinked parent on a report path is `unsafe` and never followed | mori |
| r41 calibration | probe (one dated self-assessment measurement, not a standing gate) | `python3 tools/mori-round41-calibration.py <revision> --repo DIR --reference-rev REV` (both options required; the reference gate is loaded byte-for-byte from `REV` and executed there) | 0 → `MORI_R41_CALIBRATION mismatches=0` with one `recorded_…/observed_…` line per record · 1 → `mismatches>0`: measured `mismatches=6 observed_as_of=37 extension_rows=19` at `554ff416` because the round-40 records moved after that round, so rc 1 reports the value of a dated reading, not a standing verdict · 2 → `MORI_R41_CALIBRATION_SETUP: <reason>` on stderr (git failure or timeout, reference-gate exit outside 0/1, missing summary or timing line, unparsable record) | `python3 tools/mori-round41-calibration.py --selftest` → measured `MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0` rc 0, added round 45: it builds a synthetic git repository and synthetic record files under the caller TMPDIR and checks the old-record, correction-line and setup paths; while it did not exist, the able-to-fail evidence was the rc-1 run at `554ff416` and the four setup paths read in `main`, quoted in `.ufo/waves/round-45/w1/ScribeRegistryRows.md` | `GATE_PATH = tools/mori-sources-appendonly.py` read at `--reference-rev`; `RECORD_PATHS` = `SCORECARD.md`, `LOG.md`, `corpus/lessons/round-40.md`; `CORRECTION_RE`, `SUMMARY_RE`, `TIMING_RE`; git timeout 120 s, reference-gate timeout 180 s | stdout only; it writes its reference-gate copy into a `mori-r41-gate-` `tempfile.TemporaryDirectory` under the caller TMPDIR and executes that committed program with the caller's privileges; the gate reads `--repo` and writes nothing outside its own selftest fixtures | mori |

## 2. The three round-45 counters (item 2 — 3 rows)

Covering note for all three write-scope cells: the round-45 write-scope arm reports each counter
`UNAVAILABLE` at HEAD because no committed row named it yet when it ran
(`.ufo/waves/round-45/evidence/write-scope.txt:301-330` region, `WRITESCOPE=met` at `:171` counts them
`unavailable=3`). So the cells below state what the code does and what I observed; they claim no measured
TRUE. I ran every counter with `TMPDIR` set to this seat's scratch, and no `c1st-`/`c2st-`/`c3st-` path
remained under it afterwards.

| r45 ledger counter (C1) | gate | `python3 .ufo/waves/round-45/count-c1.py <rev>` (`--repo PATH`, `--ledger PATH` default `.ufo/waves/round-45/figures.tsv`, `--other-rev REV`, `--witness-dir DIR`, `--min-rows N`, `--min-classes N`, `--timeout S`, `--selftest`) | 0 → `C1=met mismatches=0` · 1 → `C1=unmet` (a rejected row grammar, a duplicate id or command, a HEAD-reading or revision-constant row, a value that does not recompute, a floor below 12 rows or 4 classes, or an accepted witness; `failed=` names the checks) · 2 → `C1_SETUP` (usage, `WORK`, unresolvable revision, git timeout); the floors clamp UP and the verdict line prints floors, revision, repo, other revision and `witnesses=<rejected>/<total>` | `python3 .ufo/waves/round-45/count-c1.py --selftest` → measured `C1_SELFTEST pass=10 fail=0` rc 0 at sha256 `f80e75ac7421…`; the mutant `.ufo/waves/round-45/fixtures/mutants/count-c1.py` disables the duplicate-command check (`if key in cmds:` to `if False:`) and its own run reads `C1_SELFTEST pass=8 fail=2` rc 1 | `.ufo/waves/round-45/figures.tsv` at the measured revision; `.ufo/waves/round-45/fixtures/witnesses/w-revconst.tsv`, `w-head.tsv`, `w-dup.tsv`; floors 12 rows and 4 classes; `GIT_VERBS` = show, grep, ls-tree, rev-list, cat-file, log | stdout only; the selftest writes only under a `c1st-` `tempfile.mkdtemp` in the caller TMPDIR, and child git runs with `GIT_*` scrubbed, `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`; there is no `bash -c` anywhere | mori |
| r45 gate conformance (C2) | gate | `python3 .ufo/waves/round-45/count-c2.py <rev>` (`--rev REV` is the alternate spelling and only one of the two may be given; `--repo PATH`, `--auditor PATH`, `--write-scope PATH` default `.ufo/waves/round-45/fixtures/write-scope.json`, `--mutants-dir DIR` default `.ufo/waves/round-45/fixtures/mutants`, `--timeout S`, `--selftest`) | 0 → `C2=met` with `tables= registered= unregistered= no_selftest= duplicate= wrong_row= writescope_mismatch= auditor_selftest=pass=/fail= mutant= rev= repo=` · 1 → `C2=unmet`, where `checks_failed=` names the failing checks (an absent or non-v2 auditor, a red auditor selftest, an unregistered or thin row, a duplicate, a surviving mutant, a write-scope mismatch) · 2 → `C2_SETUP` (usage or both revision spellings, not a git checkout, unresolvable revision, timeout) | `python3 .ufo/waves/round-45/count-c2.py --selftest` → measured `C2_SELFTEST pass=10 fail=0` rc 0 at sha256 `e8ee29eb8852…` (ten arms: conformant, auditor absent, auditor red, duplicate row, comment-only selftest, surviving mutant, write-scope mismatch, narrowed v1 fallback, registered mismatch, tables floor); the mutant `.ufo/waves/round-45/fixtures/mutants/count-c2.py` (sha256 `d67ffacdb3ec…`) is a one-check byte-diff that disables the write-scope arm (`ws["mismatch"] == 0` to `True`) and its own selftest reads `C2_SELFTEST pass=9 fail=1` rc 1, i.e. the arm catches it | `AUDITOR_REL = tools/mori-gate-registry.py` (v2, sha256 `64db765e60e3…`, 622 lines); `WRITESCOPE_REL` and `MUTANTS_REL` above; `COUNTER_KEYS` = tables, registered, unregistered, no_selftest, duplicate, wrong_row plus writescope_mismatch; the write-scope fixture's `TRUE`/`FALSE`/`UNEXERCISED`/`UNAVAILABLE` map and its sorted-`sha256sum` tree digest | stdout only; it extracts its own copy with `git archive` into a `c2st-` `tempfile.mkdtemp` under the caller TMPDIR and runs the audited counters, the auditor and the write-scope arm from there; those children run with the caller's privileges, so their writes are bounded by what each child is told, not by this counter | mori |
| r45 corpus coverage (C3) | gate | `python3 .ufo/waves/round-45/count-c3.py <rev> --entry PATH --row S###` (`--entry`, `--row` and `--coverage-map` are each repeatable; `--root` defaults to the parent directory of `--repo`; `--census PATH` defaults to `<root>/scripts/sources-census.sh`; `--readme`, `--repo`, `--timeout S`, `--selftest`) | 0 → `C3=met rev=… entries=N rows=… census_sha256=…` · 1 → `C3=unmet` (an entry absent or missing `source:`/`verified-at:`/`recheck:`/`coverage-map:`, a declared row absent, not `mined`, or not naming the entry in `used-by`, a token collision such as S473 against S4731 or FR5 against FR12, a red census, or no README map row) · 2 → `C3_SETUP` (usage, a missing `--entry` or `--row`, unresolvable revision, census timeout) | `python3 .ufo/waves/round-45/count-c3.py --selftest` → measured `C3_SELFTEST pass=19 fail=0` rc 0 at sha256 `37fd7c24ff52…`; the mutant `.ufo/waves/round-45/fixtures/mutants/count-c3.py` (sha256 `69bf9b6eb29b…`) disables the census exit check (`proc.returncode == 0` to `True`) and its own run reads `C3_SELFTEST pass=17 fail=2` rc 1 | `--census` default `<root>/scripts/sources-census.sh`, whose sha256 the verdict line prints; the `corpus/README.md` map section; the declared entries and rows; lane `mori` | stdout only; fixtures are written under a `c3st-` `tempfile.mkdtemp` in the caller TMPDIR; the census arm executes `bash <root>/scripts/sources-census.sh validate --root <root> mori` with the caller's privileges, so that caller-named program is not sandboxed | mori |

### Measured tallies (raw, with the sha each was measured at)

| counter | sha256 (12) | `--selftest` | rc | mutant sha256 (12) | mutant `--selftest` | rc |
|---|---|---|---|---|---|---|
| count-c1.py | `f80e75ac7421` | `C1_SELFTEST pass=10 fail=0` | 0 | `…/mutants/count-c1.py` | `C1_SELFTEST pass=8 fail=2` | 1 |
| count-c2.py | `e8ee29eb8852` | `C2_SELFTEST pass=10 fail=0` | 0 | `d67ffacdb3ec` | `C2_SELFTEST pass=9 fail=1` | 1 |
| count-c3.py | `37fd7c24ff52` | `C3_SELFTEST pass=19 fail=0` | 0 | `69bf9b6eb29b` | `C3_SELFTEST pass=17 fail=2` | 1 |

The counter and its mutant both moved several times while this seat measured. At one point c2's selftest was red
(`C2_SELFTEST pass=1 fail=7` at `8d9fa42c4fd0…`, seven arms `raised name '_token' is not defined`) and its
mutant was stale (not a one-check diff). At the bytes quoted above both are final: the counter is green and the
mutant is a clean one-check byte-diff that its own selftest catches. A later edit invalidates the sha, not the
method — re-run `--selftest` before landing.

## 3. Item 3 — superseding rows (four, per the L1's correction)

The L1's message supersedes the "two cells" wording: the honest unit is **four rows**, `SKILL.md:183-186`, in
two classes. The original cells, exactly as they read now (cells extracted programmatically from `SKILL.md`,
and identical to the quotes in `.ufo/waves/round-44/w1/SentTools.md` §F8 at `:437-440`):

- `SKILL.md:183` (r44 figure ledger (C1)): `stdout only; reads the repo at `--rev`; the selftest writes only under the caller TMPDIR`
- `SKILL.md:184` (r44 gate registry (C2)): `stdout only; reads the registry and the audited paths at `--rev`; the selftest writes only under the caller TMPDIR`
- `SKILL.md:185` (r44 gate conformance (C2)): `stdout only; counter bytes materialize under the caller TMPDIR; nothing in the repo is written`
- `SKILL.md:186` (r44 corpus coverage (C3)): `stdout only; the registry copy handed to the census is materialized under the caller TMPDIR`

F8's own sentence (`.ufo/waves/round-44/w1/SentTools.md:443-445`): "the C1 gate executes arbitrary pipelines
(writes anywhere), the C3 gate executes an arbitrary program (writes anywhere), and all four self-tests write
wherever `GIT_DIR` says."

**What I observed myself, and what I did not.** The round-45 write-scope arm has landed and it reports all four
as `TRUE` — `.ufo/waves/round-45/evidence/write-scope.txt:82` (C1), `:96` (C2 conformance), `:110` (C3),
`:124` (gate registry), `WRITESCOPE=met` at `:171`, with `writes_outside_tmpdir=0` for each. That verdict is
**bounded** and does not discharge F8: the arm runs only the instrument's own `--selftest`, with
`HOME`/`XDG_*` redirected, `GIT_CEILING_DIRECTORIES` set and "no inherited `GIT_DIR`/`GIT_WORK_TREE`/
`GIT_INDEX_FILE`" (`write-scope.txt:19-25`), and it states its own limit at `:40-48`: it "falsifies the
*location* clause, not the materialisation clause" and measures filesystem effects only. So it (a) never runs
the C1 production path that executes ledger rows, (b) never runs the C3 census program, and (c) deliberately
removes the `GIT_*` inheritance that class (ii) is about. I therefore cite it as "the `--selftest` runs wrote
nothing", not as "the cells are true".

My own measurement, for the one class the arm masks — v1 gate registry under inherited `GIT_*`:

```
$ sha256sum tools/mori-gate-registry.py        # at probe time
743996b11d19261b87e3ea6c0d0be4c0e5e6750d05f6d603af51dc1a7e125a1f   (v1, 308 lines)
$ export GIT_DIR=$TMPDIR/gdirtest/gi.git GIT_WORK_TREE=$TMPDIR/gdirtest/wt
$ python3 tools/mori-gate-registry.py --selftest
selftest FAIL registered_row_met: raised registry absent at main: SKILL.md
… all six arms the same …
GATE_REGISTRY_SELFTEST pass=0 fail=6        rc=1
$ find $TMPDIR/gdirtest -maxdepth 3
…/gdirtest/gi.git/hooks/… …/gi.git/info/exclude …/gi.git/description     # the selftest's `git init` wrote here
```
i.e. the fixture repos went wherever the environment pointed, not into the tool's own temp dirs. v2
(`64db765e60e3…`, 622 lines) now scrubs `GIT_*` in `child_env()` (`tools/mori-gate-registry.py:96-106`), so the
old cell is true of v2 bytes and false of the bytes it described — which is exactly why the supersede row says
which sha it is talking about. For C1/C3 I did not run a production-path write probe; those rows say
"superseded on F8's reading, not re-measured by this row".

### Rows (item 3 — 4 rows)

| r44 figure ledger (C1) — write scope superseded | gate | `python3 .ufo/waves/round-44/count-c1.py <rev>` (`--ledger PATH`, `--repo PATH`, `--min-rows N`, `--min-classes N`, `--selftest`) | unchanged from row `r44 figure ledger (C1)` (SKILL.md:183), which remains the verdict-map authority for this instrument; this row supersedes that row's write-scope cell only | unchanged from row `r44 figure ledger (C1)`: `python3 .ufo/waves/round-44/count-c1.py --selftest` → measured `C1_SELFTEST pass=6 fail=0` rc 0 (re-run 2026-10-25) | unchanged from row `r44 figure ledger (C1)` (SKILL.md:183) | superseded: the cell at SKILL.md:183 reads "stdout only; reads the repo at `--rev`; the selftest writes only under the caller TMPDIR", and that is false as written — the counter executes every ledger row through `bash -c` (`.ufo/waves/round-44/count-c1.py:113-114`) with the caller's cwd and environment, so a committed row writes anywhere the caller can; the round-45 arm's `TRUE` (`evidence/write-scope.txt:82`) covers only its `--selftest` run and not that production path. Superseded on the round-44 sentinel's F8 reading (`.ufo/waves/round-44/w1/SentTools.md` §F8), not re-measured by this row | mori |
| r44 gate registry (C2) — write scope superseded | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <repo-relative path> [--audit ...]` (`--registry PATH`, `--repo PATH`, `--selftest`) | unchanged from row `r44 gate registry (C2)` (SKILL.md:184), which remains the verdict-map authority; this row supersedes that row's write-scope cell only | unchanged from row `r44 gate registry (C2)`: `python3 tools/mori-gate-registry.py --selftest` → measured v1 `GATE_REGISTRY_SELFTEST pass=6 fail=0` and v2 `GATE_REGISTRY_SELFTEST pass=10 fail=0`, both rc 0 (re-run 2026-10-25) | unchanged from row `r44 gate registry (C2)` (SKILL.md:184) | superseded: the cell at SKILL.md:184 reads "stdout only; reads the registry and the audited paths at `--rev`; the selftest writes only under the caller TMPDIR", and that is false for the bytes it described — measured 2026-10-25 at sha256 `743996b1…` (v1, 308 lines): with `GIT_DIR` and `GIT_WORK_TREE` exported, `--selftest` initialized `$GIT_DIR` (hooks and description written there) and all six arms failed with `registry absent at main: SKILL.md`, so the fixture writes landed where the environment pointed; v2 (sha256 `64db765e…`, 622 lines) scrubs `GIT_*` in `child_env()`, so the claim holds for v2 bytes only | mori |
| r44 gate conformance (C2) — write scope superseded | gate | `python3 .ufo/waves/round-44/count-c2.py <rev> --counter PATH [--counter PATH ...]` (`--mutants-dir PATH`, `--min-arms N`, `--selftest`) | unchanged from row `r44 gate conformance (C2)` (SKILL.md:185), which remains the verdict-map authority; this row supersedes that row's write-scope cell only | unchanged from row `r44 gate conformance (C2)`: `python3 .ufo/waves/round-44/count-c2.py --selftest` → measured `C2_SELFTEST pass=5 fail=0` rc 0 (re-run 2026-10-25) | unchanged from row `r44 gate conformance (C2)` (SKILL.md:185) | superseded: the cell at SKILL.md:185 reads "stdout only; counter bytes materialize under the caller TMPDIR; nothing in the repo is written", and that is false for the bytes it described — `.ufo/waves/round-44/count-c2.py:111` builds `env = dict(os.environ)` and hands it to every audited counter, every mutant and the auditor, so a fixture commit lands wherever `GIT_DIR` says instead of only under the caller TMPDIR; the round-45 arm's `TRUE` (`evidence/write-scope.txt:96`) was taken with `GIT_*` removed, so it cannot see this. Superseded on the round-44 sentinel's F8 reading (`.ufo/waves/round-44/w1/SentTools.md` §F8), not re-measured by this row | mori |
| r44 corpus coverage (C3) — write scope superseded | gate | `python3 .ufo/waves/round-44/count-c3.py <rev> --entry PATH --row S### [--row S### ...]` (`--coverage-map`, `--census PATH`, `--readme PATH`, `--selftest`) | unchanged from row `r44 corpus coverage (C3)` (SKILL.md:186), which remains the verdict-map authority; this row supersedes that row's write-scope cell only | unchanged from row `r44 corpus coverage (C3)`: `python3 .ufo/waves/round-44/count-c3.py --selftest` → measured `C3_SELFTEST pass=6 fail=0` rc 0 (re-run 2026-10-25) | unchanged from row `r44 corpus coverage (C3)` (SKILL.md:186) | superseded: the cell at SKILL.md:186 reads "stdout only; the registry copy handed to the census is materialized under the caller TMPDIR", and that is false as a write-scope claim — it names where one copy goes and omits that the census arm executes a caller-named program (`.ufo/waves/round-44/count-c3.py:139`: `bash <census> validate --file <staged>`) unsandboxed, so that program writes anywhere; the round-45 arm's `TRUE` (`evidence/write-scope.txt:110`) covers only its `--selftest` run. Superseded on the round-44 sentinel's F8 reading (`.ufo/waves/round-44/w1/SentTools.md` §F8), not re-measured by this row | mori |

**Auditor consequence of the supersede (check this before landing).** The auditor v2 attributes a path to
`matches[0]`, the *first* row in document order that names it (`tools/mori-gate-registry.py:359-363`), while the
write-scope arm's documented rule is *last* wins (`write-scope.json` `source.attribution`;
`write-scope.txt:31-35`). Appending the four superseding rows after 183–186 therefore has the intended effect on
the write-scope arm and **no effect** on the auditor's attribution — which is harmless (the auditor reads only
the entry cell and the tool body) but is an inconsistency the L1 should know about: two instruments in one round
define "supersedes" in opposite directions. I verified in the throwaway clone (§5) that the four superseding rows
pass the auditor as ordinary rows (8 cells, entry resolves, `--selftest` branch present), and that
`duplicate=0 wrong_row=0` is unaffected by them.

## 4. Item 4 — the routed-r24 self-test cell

The row is `SKILL.md:721`, name `routed round-24 items (r25, C1)`, entry
`python3 -I -B tools/mori-routed-r24.py --repo REPO --rev REV [--rerun]`. Its self-test cell now reads, verbatim:

```
none built in — the tool has no `--selftest`; able-to-fail evidence is the round-25 wave-2 mutation reports
(`.ufo/waves/round-25/w2/MutRoutedD1.md`, `MutRoutedD2.md`, `MutRoutedD3D5.md`, `MutRoutedHygiene.md`).
**A committed self-test is still owed** (routed defect R5)
```

When this seat started, the tool had no branch and the cell was accurate; the residual seat landed one during
the seat, so the cell is stale **now**. Measured at the delivered bytes:
`python3 -I -B tools/mori-routed-r24.py --selftest` → `ROUTED_R24_SELFTEST pass=26 fail=0` rc 0 (2026-10-25).
Replacement text for that one cell:

```
`python3 -I -B tools/mori-routed-r24.py --selftest` → `ROUTED_R24_SELFTEST pass=26 fail=0`, added round 45: it runs the D1–D5 fixture rows through the real CLI over isolated throwaway git repos under `$TMPDIR`; able-to-fail evidence remains the round-25 wave-2 mutation reports (`.ufo/waves/round-25/w2/MutRoutedD1.md`, `MutRoutedD2.md`, `MutRoutedD3D5.md`, `MutRoutedHygiene.md`)
```

Measured, not inferred: the token is the delivered one and it matches the sibling pattern
(`ROUTED_CHECK_SELFTEST`, `R19_SELFTEST`). Re-run before landing in case the seat edits again.

**Same staleness, one row earlier, with a measured tally.** `SKILL.md:646` (`routed round-23 items (r24, C1)`,
`tools/mori-routed-check.py`) still says `none built in; able-to-fail evidence is thirteen sandbox mutants…`.
That tool now has a real branch — measured 2026-10-25: `ROUTED_CHECK_SELFTEST pass=20 fail=0` rc 0
(`python3 -I tools/mori-routed-check.py --selftest`). Its replacement cell:

```
`python3 -I tools/mori-routed-check.py --selftest` → `ROUTED_CHECK_SELFTEST pass=20 fail=0`, added round 45; able-to-fail evidence remains the thirteen sandbox mutants in `.ufo/waves/round-24/w1/BuildRoutedCheck.md`
```

The other new branch, for the same wave: `R19_SELFTEST pass=26 fail=0` rc 0
(`python3 tools/mori-round19-regressions.py --selftest`), which belongs in the `r19 finite regressions` row
(`SKILL.md:182`) when that seat's report lands.

**In place, or append-only?** Update these self-test cells **in place**, and record the change in the prose
section that owns the row (for `:721`, a one-line dated `Round26`-style footnote; for `:646`, the same under
`## Round24`). Reasoning against the lane's house style:
1. The lane's append-only habit protects *claims and history* — `corpus/SOURCES.md` rows and prior-round
   findings — and SKILL.md rows have been superseded by appending a sibling row with a later round marker
   (`source drift (r36)` then `source drift (r37)`; `r44 …` rows beside the `r18`/`r19` ones).
2. But a self-test cell is a statement about *the tool as it is now*, not a dated claim, and the auditor reads
   exactly one row per path — `matches[0]`, the **first** (`tools/mori-gate-registry.py:359-363`). An appended
   replacement row for the same path is inert for the auditor: the stale cell stays the one the instrument
   reads. That is the decisive argument, and it is measured, not stylistic.
3. Updating in place costs nothing an append-only note cannot recover: the change is visible in `git log -p`
   and in the appended footnote, and no prior *verdict* is rewritten — only a description of current bytes.
4. If the L1 prefers a superseding row anyway (to match the r44 write-scope pattern), it must also patch v2's
   attribution to last-wins, or the new row will not be read. That is a code change, not a registry edit, and
   I did not make it.

## 5. Verification I ran on the rows themselves

Throwaway clone under my TMPDIR (`git clone --shared <lane> $TMPDIR/regclone`), the three round-45 counters
copied in, my ten rows spliced after `SKILL.md:186`, one commit, then the auditor v2 twice — because the
residual seats kept landing branches while I measured.

**Run A** (rows + the four instrument edits that existed at that moment: `mori-gate-registry.py` v2,
`mori-round19-regressions.py`, `mori-routed-check.py`, `mori-silence-cases.sh`):

```
$ python3 tools/mori-gate-registry.py --repo $TMPDIR/regclone --rev HEAD --audit-all
audit tools/mori-disk-rate.py             FAIL row='disk write rate (r34)' (row 'disk write rate (r34)' tool has no real --selftest argv branch)
audit tools/mori-round41-calibration.py   FAIL row='r41 calibration' (row 'r41 calibration' tool has no real --selftest argv branch)
audit tools/mori-routed-r24.py            FAIL row='routed round-24 items (r25, C1)' (row 'routed round-24 items (r25, C1)' tool has no real --selftest argv branch)
tables=7
rev=<clone HEAD>
mode=population
population_digest=…
registered=36 unregistered=0 no_selftest=3 duplicate=0 wrong_row=0 tables=7
REGISTRY=unmet
rc=1
```

**Run B** (the same clone after copying every branch this wave has now landed — `mori-disk-rate.py`,
`mori-round41-calibration.py` and `mori-routed-r24.py` in addition):

```
$ python3 tools/mori-gate-registry.py --repo $TMPDIR/regclone --rev HEAD --audit-all
registered=39 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=7
REGISTRY=met
rc=0
```

Baseline in the same clone **before** the rows:
`registered=29 unregistered=6 no_selftest=4 duplicate=0 wrong_row=0 tables=7` (`REGISTRY=unmet`, rc 1).

Reading: every one of my ten rows is structurally accepted (8 cells, entry resolves at a revision, no
duplicate name, no wrong row), the six previously unregistered paths are now registered, and the verdict flips
to `met` as soon as the three late branches exist. The rows alone do **not** reach `no_selftest=0` (Run A); the
branches do the rest (Run B). Nothing in the lane was modified: `git -C <lane> rev-parse HEAD` stayed
`3ad8faaa637ae466c61f9427fea1c208bf49ea82` and `git status --porcelain` showed only untracked round-45 scratch
plus the seats' own modified instruments.

## 6. Findings (route to round 46 unless marked otherwise)

- **F-R45-1 (WITHDRAWN — was the bound on C2)** — when this seat began, `tools/mori-disk-rate.py` and
  `tools/mori-round41-calibration.py` had no `--selftest` argv branch at all (their `--help` listed none and
  `grep -c -- --selftest` was 0), so their honest rows carried `no_selftest` and the intermediate audit read
  `no_selftest=3` (§5, Run A). Both branches landed during the wave: measured at the end of this seat
  `MORI_DISK_RATE_SELFTEST pass=14 fail=0` and `MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0`, rc 0 each, and
  Run B reads `no_selftest=0`. Nothing is owed here; the history stays because a reader of this round's reports
  would otherwise meet those two tallies with no provenance.
- **F-R45-2 (LOW, tool text)** — `tools/mori-disk-rate.py`'s stdout sentence still reads "The exit status is 0
  whenever that JSON is produced and 2 on a usage error" (docstring `:35-36`); the implemented rc 1 for an
  unreadable sample (`:495`) and the selftest's rc 1/2 are undeclared there. Measured: rc 1 on an unreadable
  `--a`.
- **F-R45-3 (LOW, discoverability)** — `tools/mori-wave-settlement.py --selftest` exists but is invisible to
  `--help` (intercepted at `:686-688` before argparse). A caller who trusts `--help` concludes the tool has
  none; the row prints the exact string instead.
- **F-R45-4 (MEDIUM, cross-instrument)** — supersede direction disagrees: the auditor v2 takes `matches[0]`
  (`:359-363`), the write-scope arm documents last-wins (`write-scope.txt:31-35`). A superseding row therefore
  reaches one instrument and not the other. Remediation is a code decision for the auditor seat.
- **F-R45-5 (arithmetic, for the L1)** — the rows move `unregistered` 6→0 and leave every other counter alone;
  `no_selftest` reads 4 before the rows (four tools with no real branch), 3 after the rows alone (§5 Run A) and
  0 once the wave's branches land (§5 Run B, `REGISTRY=met`). The rows are necessary and not sufficient: a
  registry row cannot give a tool a selftest, and v2 has no escape for "none".
- **F-R45-6 (MEDIUM, evidence scope)** — the write-scope arm reports all four r44 cells `TRUE`
  (`write-scope.txt:82,96,110,124`) by running only `--selftest` with `GIT_*` removed; its own §"NOT VERIFIED"
  (`:40-48`) says it does not exercise production paths. The TRUE does not contradict F8, and the supersede
  rows say so explicitly; a reader who takes `WRITESCOPE=met` as "F8 refuted" would overclaim.
- **F-R45-7 (WITHDRAWN at the delivered bytes — was a mutant/red-selftest gap)** — during this seat
  `count-c2.py` was red at one point (`C2_SELFTEST pass=1 fail=7` at `8d9fa42c4fd0…`, seven arms `raised name
  '_token' is not defined`) and its mutant was then a stale multi-change diff (it lacked `TABLE_FLOOR = 7`,
  `_work_ignore` and `_token`; tally `pass=7 fail=1` against the counter's ten arms). At the final bytes measured
  here — counter `e8ee29eb8852…` `pass=10 fail=0`, mutant `d67ffacdb3ec…` a one-check diff to `True` with
  `pass=9 fail=1` — both are sound. No round-46 action; kept so the intermediate readings in the seats' logs
  have a disposition.
- **Observation, not a finding** — `/tmp` held `c2-*`, `c2-acc*` and `c2-after.*` paths during this seat. Every
  command I ran exported `TMPDIR`; I created none of them and deleted none of them (the lane's rule is that
  `/tmp` is not a scratch target).

## 7. What I did not do

- I did not edit `SKILL.md`, any tool, any counter, any fixture, or another seat's report (the clone in §5 is
  outside the lane, under my TMPDIR).
- I did not run the r44 C1/C3 production paths to force a write; their supersede rows say "not re-measured by
  this row". I did run the r44 v1 gate-registry selftest under inherited `GIT_*` and recorded it above.
- I did not measure `mori-routed-r24.py`'s future token or tally; the replacement cell marks both as
  unmeasured and tells the L1 to substitute the delivered values.
- I did not verify byte-identical production output for the three ExecSelftestModes tools (that seat's job);
  I only ran their `--selftest` to know the tokens.

Artifacts: this report; scratch under `.ufo/waves/round-45/tmp/ScribeRegistryRows/` (`rows.md`, `regclone/`
throwaway clone, `dr-live.json`, `a.diskstats`, `b.diskstats`, `settle-out.json`, `settle-stdout.json`,
`settlement-scan.json`, `regfix/`, `gdirtest/`).
