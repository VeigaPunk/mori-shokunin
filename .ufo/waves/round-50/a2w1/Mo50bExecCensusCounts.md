# Mo50bExecCensusCounts — round 50 (attempt 2), wave a2w1: frontier-step census before → after

Seat: executor (leaf). Lane `mori-shokunin`, repo `/home/vgpnk/Projects/shokunin/mori-shokunin`, fleet root
`/home/vgpnk/Projects/shokunin`. Contract read first: `.ufo/waves/round-50/contract.md` (frozen at
`950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`; §Frontier step: "Census at round start: `evidence/census-start.txt`
(rc 0; 21 W04 warnings + `ok`). Round end: same command."). Measured revisions: entering tip
`7197160b927f04db294c9553fb48fadcc7a3f4e3` and landed data `487941b9395e89678af0053cc443cdb49cdee6e3`.
Lane HEAD while running: `4548a34d` (working-tree `corpus/SOURCES.md` byte-identical to the landed blob — sha
below). Environment: `GNU bash 5.3.20(1)`, `GNU Awk 5.4.1`, `git 2.56.0`.

Scope: frontier-step census measurement only. No judgement of C1 or C2, no edit to any lane file, no counter,
predicate, control or kill rule changed or proposed, no host state touched. This report is the only file I
wrote.

## Verdict (answers first)

**The census delta is exactly the expected one: +3 rows, all tier A, all mined — S489, S490, S491 — and
nothing else moved.**

- `sources-census.sh validate` on `git archive 7197160b` → rc **0**, 21 `W04` + `ok`, 0 E-codes.
  On `git archive 487941b9` → rc **0**, 22 `W04` + `ok`, 0 E-codes. The only difference between the two
  outputs is one added line: `W04 S491 duplicate url …/linux/v7.2/mm/oom_kill.c across scopes` — the warning
  the contract predicts ("same URL as S003 and S476, different scope — a W04 warning, not an error").
- Rows by tier/status (one-line awk over the `## Registry` table, 0–3 leading spaces accepted):
  rows **261 → 264** (+3), `tier.A` **230 → 233** (+3), `tier.B` 14 → 14, `tier.C` 17 → 17,
  `status.mined` **211 → 214** (+3), `status.queued` 24 → 24, `status.rejected` 26 → 26.
  Cross-tab: only `A/mined` moves (201 → 204); every other tier×status cell is unchanged.
- The three new rows are `corpus/SOURCES.md:268-270` at the landed tip, each `tier A`, `status mined`,
  `opened 2026-10-26`, `used-by corpus/knowledge/oom-memcg-stat-r50.md` (that file is present in the landed
  tree), ids unique, registry ordered S488 → S489 → S490 → S491.
- The tool's own `census` mode reproduces my awk counts **exactly** at both revisions, and a validate run
  against the live fleet root (`/home/vgpnk/Projects/shokunin`, worktree = landed bytes) is byte-identical to
  the `git archive 487941b9` run, so the isolated scratch fleet root did not alter the result.
- Instrument health: `sources-census.sh selftest` → rc 0, `selftest ok`.
- Baseline confirmation: my before-run output is byte-identical to the committed
  `evidence/census-start.txt` (lines 1–22; path line normalized), i.e. the round-start baseline in evidence
  is what `7197160b` actually prints.

## Method (exact, reproducible)

Scratch `S = /fast/scratch/hyaku/mori-r50/Mo50bExecCensusCounts`, `export TMPDIR=$S/tmp`. `mkdir -p` first,
`rm -rf` after the report was written. Disk guard checked before the runs: `/fast/scratch/hyaku 24%, 613.7G
free`, `/tmp 2%, 125.3G free` — no ENOSPC risk. No installs at all (pacman paused host-wide and not needed;
no uv, no npx, no `~/.local/bin` addition), so there is no tool/version/channel line to record beyond the
three stock tools named above.

The script's usage was read first (`scripts/sources-census.sh:2-38`, what `usage()` prints): `validate` takes lane ids resolved from
`--root`'s `shokunin.conf` plus `$ROOT/*-shokunin`; `--root` must therefore be fleet-shaped (`shokunin.conf`
present, line 453 `conf=$ROOT/shokunin.conf`). Two scratch fleet-shaped roots were built, each holding a
byte-identical copy of `shokunin.conf` (`sha256 bfdf96c4feddb37a4411a750c706e5b53ecd1402153c53983e2bd4923614a3f8`,
same as the fleet's) and one `mori-shokunin/` extracted from the respective `git archive`. `mori` is a
registered lane (`shokunin.conf:63 mori|mori-shokunin|…`), so the assignment's literal `--root … mori`
invocation is what ran.

Instrument identity (fleet side, read-only): `scripts/sources-census.sh`
`sha256 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`, last touched by fleet commit
`f47ad6ba`; `selftest` rc 0 (`…/census-selftest.txt`, ends `killed H1-no-table-cell-execution`,
`killed gawk-failure-is-error-not-ok`, `selftest ok`).

```bash
S=/fast/scratch/hyaku/mori-r50/Mo50bExecCensusCounts
export TMPDIR=$S/tmp; mkdir -p "$S/tmp" "$S/fleet-before" "$S/fleet-after"
cp /home/vgpnk/Projects/shokunin/shokunin.conf "$S/fleet-before/shokunin.conf"
cp /home/vgpnk/Projects/shokunin/shokunin.conf "$S/fleet-after/shokunin.conf"
cd /home/vgpnk/Projects/shokunin/mori-shokunin
git archive 7197160b927f04db294c9553fb48fadcc7a3f4e3 | tar -x -C "$S/fleet-before"  --one-top-level=mori-shokunin   # rc=0
git archive 487941b9395e89678af0053cc443cdb49cdee6e3 | tar -x -C "$S/fleet-after"   --one-top-level=mori-shokunin   # rc=0

scripts=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
$scripts validate --root "$S/fleet-before" mori   # rc=0, 21 W04 + ok
$scripts validate --root "$S/fleet-after"  mori   # rc=0, 22 W04 + ok
$scripts census   --root "$S/fleet-before" mori --out "$S/census-before.tsv"   # rc=0
$scripts census   --root "$S/fleet-after"  mori --out "$S/census-after.tsv"    # rc=0
```

Both archives extracted cleanly; `corpus/SOURCES.md` is 328 lines before and 331 lines after.

## Validate, entering tip `7197160b` (rc 0)

```
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
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf across scopes
mori	W04	S351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	ok	/fast/scratch/hyaku/mori-r50/Mo50bExecCensusCounts/fleet-before/mori-shokunin/corpus/SOURCES.md
```

(`.err` files both empty; counts: `W04=21 ok=1 E=0`.)

## Validate, landed data `487941b9` (rc 0)

Identical to the block above except for one additional warning line, inserted at position 22 (verified by
`diff` of the two outputs with only the `ok` path line normalized):

```
21a22
> mori	W04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
```

so the full 22-warning set is S035, S037, S073, S074, S075, S076, S147, S148, S149, S150, S166, S168, S201,
S218, S220, S228, S349, S351, S470, S476, S486, **S491**, then `mori	ok	…/fleet-after/mori-shokunin/corpus/SOURCES.md`.
Counts: `W04=22 ok=1 E=0`, rc 0. No `E01`–`E12` code appears at either revision, so the new rows introduce no
malformed row, no duplicate id, no duplicate URL+scope collision without supersedes, no enum violation, no bad
date/cadence, no tier-A community, no missing `used-by` path, and no row-shaped source outside the registry.

## Row census by status and tier (one-line awk, 0–3 leading spaces accepted)

The Registry table spans `corpus/SOURCES.md:5-271` at the landed tip (header `| id | source | kind | tier |
scope | anchor | teaches | status | opened | recheck | used-by |`, 11 columns, `NF=13`); `## Paths` begins at
line 272, so the awk is scoped to the Registry section (heading match, 0–3 leading spaces) and takes tier from
field 5 and status from field 9.

```bash
awk -F'|' '/^ {0,3}#/ {sec=($0 ~ /^ {0,3}##[[:space:]]+Registry[[:space:]]*$/)} sec && /^ {0,3}\|[[:space:]]*S[0-9][0-9]+[[:space:]]*\|/ {t=$5; s=$9; gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); tier[t]++; stat[s]++; n++} END {printf "rows=%d", n; for (k in tier) printf " tier.%s=%d", k, tier[k]; for (k in stat) printf " status.%s=%d", k, stat[k]; print ""}' "$F"
```

| revision | awk output | rc |
|---|---|---|
| `7197160b` | `rows=261 tier.A=230 tier.B=14 tier.C=17 status.mined=211 status.queued=24 status.rejected=26` | 0 |
| `487941b9` | `rows=264 tier.A=233 tier.B=14 tier.C=17 status.mined=214 status.queued=24 status.rejected=26` | 0 |

Cross-tab (tier/status cell, same awk predicate, second pass):

| tier/status | before | after | delta |
|---|---|---|---|
| A/mined | 201 | 204 | **+3** |
| A/queued | 22 | 22 | 0 |
| A/rejected | 7 | 7 | 0 |
| B/mined | 10 | 10 | 0 |
| B/queued | 2 | 2 | 0 |
| B/rejected | 2 | 2 | 0 |
| C/rejected | 17 | 17 | 0 |

Delta summary: **rows +3, `tier.A` +3, `status.mined` +3, `A/mined` +3; every other cell 0.** Expected
"+3 rows: S489-S491, tier A, mined" — matched exactly, with no incidental drift anywhere else.

## Cross-check against the tool's own counter (`census` mode)

`census --root "$S/fleet-before" mori --out …` (rc 0):

```
mori	rows	261
mori	tier.A	230
mori	tier.B	14
mori	tier.C	17
mori	status.mined	211
mori	status.queued	24
mori	status.rejected	26
FLEET	rows	261
FLEET	tier.A	230
FLEET	tier.B	14
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	24
FLEET	status.mined	211
FLEET	status.rejected	26
FLEET	status.invalid	0
FLEET	missing	0
```

`census --root "$S/fleet-after" mori --out …` (rc 0):

```
mori	rows	264
mori	tier.A	233
mori	tier.B	14
mori	tier.C	17
mori	status.mined	214
mori	status.queued	24
mori	status.rejected	26
FLEET	rows	264
FLEET	tier.A	233
FLEET	tier.B	14
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	24
FLEET	status.mined	214
FLEET	status.rejected	26
FLEET	status.invalid	0
FLEET	missing	0
```

Every `mori` figure equals my awk output at the same revision; `tier.invalid=0` and `missing=0` at both.

**Live-root control (no isolated-root bias):** the same validate run against the real fleet root, whose
`mori-shokunin/` working tree carries the landed bytes, is byte-identical to the archive-after run:

```bash
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori   # rc=0
diff <(sed 's#^mori\tok\t.*#mori\tok\t<path>#' validate-live-root.txt) <(sed 's#^mori\tok\t.*#mori\tok\t<path>#' validate-after.txt)
```

→ no output ("IDENTICAL"), `W04=22 ok=1 E=0` for both.

**Baseline control:** the committed `evidence/census-start.txt` (round-start census in the frozen contract) is
reproduced exactly by my before-run — diff of the two, with the `ok` path line normalized and the evidence
file's trailing `census-rc=0` line dropped, prints nothing ("IDENTICAL"), 21 W04 + ok. So the frozen entry
baseline is confirmed from the `git archive 7197160b` bytes and is not merely a transcription.

## Byte identity of the measured bytes

```
archive-after   sha256 33f294439e479f3891fbc5b71b5ceb0a623871cad6980285dcbc696be04fc185
blob 487941b9   sha256 33f294439e479f3891fbc5b71b5ceb0a623871cad6980285dcbc696be04fc185   (git cat-file blob 487941b9:corpus/SOURCES.md)
worktree        sha256 33f294439e479f3891fbc5b71b5ceb0a623871cad6980285dcbc696be04fc185   (lane HEAD 4548a34d; git diff --stat 487941b9 -- corpus/SOURCES.md → empty, rc 0)
archive-before  sha256 2411aa96ec7ff6d5b94fbcf1d391310ead9da2542047d96ad6de3a7f08d40453
blob 7197160b   sha256 2411aa96ec7ff6d5b94fbcf1d391310ead9da2542047d96ad6de3a7f08d40453
git diff --numstat 7197160b 487941b9 -- corpus/SOURCES.md → 3	0	corpus/SOURCES.md
```

`git archive` introduced no byte change and there are exactly three insertions, zero deletions, so no existing
row was edited, reordered or re-scoped by the landed data.

The three added rows in the landed tree (key columns; `id | tier | status | opened | used-by`, line numbers in
the extracted archive):

```
268: S489 | A | mined | 2026-10-26 | corpus/knowledge/oom-memcg-stat-r50.md
269: S490 | A | mined | 2026-10-26 | corpus/knowledge/oom-memcg-stat-r50.md
270: S491 | A | mined | 2026-10-26 | corpus/knowledge/oom-memcg-stat-r50.md
267: S488 | A | mined | 2026-10-25 | corpus/knowledge/journal-reach-r49.md   (last pre-existing row)
```

`corpus/knowledge/oom-memcg-stat-r50.md` is present in the landed archive (`[ -f … ]` → PRESENT), which is why
`E11` (used-by path missing on disk) does not fire. URLs are the three frozen sources the contract names
(`docs.kernel.org/7.2/admin-guide/cgroup-v2.html`, `raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c`,
`…/mm/oom_kill.c`); S491's URL is the S003/S476 URL, hence the added W04.

## Indentation acceptance probe (method validity for the "0–3 leading spaces" rule)

The counting method must accept 0–3 leading spaces and ignore 4+ (documented at `scripts/sources-census.sh:40-41`).
Two fixtures were built by copying the landed archive to scratch and inserting three rows with 1, 3 and 4
leading spaces (`S901`, `S902`, `S903`, all `docs | A | queued | 2026-10-26 | —`):

- **Rows inserted inside the Registry section** (after the last registry row, before `## Paths`):
  `census --file` → `rows 266`, `tier.A 235`, `status.queued 26` (rc 0); `validate --file` → rc 0, the only
  non-W04 line is `file ok` (23 lines total = 22 W04 + ok). My awk on the same file →
  `rows=266 tier.A=235 tier.B=14 tier.C=17 status.mined=214 status.queued=26 status.rejected=26`. Agreement
  is exact: 1-space and 3-space rows counted by both, 4-space row ignored by both, and the 4-space row raises
  **no** code.
- **Rows appended after the last section** (outside `## Registry`): `validate --file` → rc **1** with
  `E12 S901 row outside Registry section` and `E12 S902 row outside Registry section`; the 4-space `S903` is
  again silent; `census --file` stays `rows 264` (outside-registry rows are never counted).

Real data is unaffected: `grep -cE "^ {4,}\|[[:space:]]*S[0-9]+[[:space:]]*\|"` → **0** (rc 1) at both
revisions, and the 1–3-space variant → **0** (rc 1). Every registry row in the real file starts at column 0.

## Fleet context (for scale only)

Live fleet census (`census --root /home/vgpnk/Projects/shokunin`, rc 0): `FLEET rows 3217`, `tier.A 2669`,
`tier.B 433`, `tier.C 115`, `invalid 0`, `status.mined 2722`, `queued 289`, `rejected 206`, `missing 0`,
across 21 lanes. mori's 264 rows are ~8.2 % of the fleet total. This is the after state only — no
fleet-wide "before" exists, because the other lanes are live working trees, not archived revisions; the
before/after pair in this report is the mori lane only, as assigned.

**Reading hazard:** inside a `--root <isolated scratch fleet>` run, the `FLEET.*` lines describe *that root's*
fleet (one lane: mori), so `FLEET.rows 264` above is **not** a fleet-wide figure. Do not quote the scratch
`FLEET` numbers as fleet totals.

## Named limits

- The counts are of the `## Registry` section only, exactly as the parser defines it. A row-shaped line
  outside that section is `E12` for `validate` and is never counted by `census` or by my awk (probed above);
  a 4+ space-indented row-shaped line is invisible to the row count *and* to `E12` (probed above), so a
  row accidentally indented four spaces would silently vanish from the census. No such line exists at either
  measured revision.
- The census counts rows, ids, tier and status cells as written; `E06`/`E07` at rc 0 mean the enums are valid,
  not that a row's tier or status is the right classification for its source. It says nothing about whether a
  row's quote/anchor is correct (that is C2's surface) or whether the entry the rows feed is good.
- `W04` is a warning that does not affect lane status; the warning count is not a quality score, and the
  fleet rule is that warnings never make a lane unclean.
- The after state measured is the landed-data tip `487941b9`, not the round-end census: `.ufo/waves/round-50/evidence/`
  at the landed tip holds `census-start.txt` but no `census-end.txt`, so the contract's round-end run is still
  owed at closure. Because `census`/`validate` read `corpus/SOURCES.md` only, that closure run will print the
  same numbers as the after state reported here unless SOURCES.md changes again in wave 2 (264 rows / 233 A /
  214 mined, 22 W04, rc 0).
- Only the mori lane is measured from archived revisions; fleet totals are live-tree readings at one instant.
- I did not audit the census script's own selftest arms beyond its rc-0 verdict, and I ran no mutation of the
  script (frozen instruments are not mine to alter).

## Findings

- **F1 — LOW (the measured claim, no defect)** — `corpus/SOURCES.md` registry at `487941b9`: rows 261 → 264
  (+3), `tier.A` 230 → 233, `status.mined` 211 → 214, cross-tab `A/mined` 201 → 204, every other tier/status
  cell unchanged; `validate` rc 0 with 0 E-codes at both revisions. The new rows are `corpus/SOURCES.md:268-270`
  (S489, S490, S491), tier A, mined, opened 2026-10-26, `used-by corpus/knowledge/oom-memcg-stat-r50.md`,
  which exists in the landed tree. The delta is exactly the contract's expectation, and `git diff --numstat`
  is `3 0`, so no pre-existing row was touched.
- **F2 — LOW (expected warning, not an error)** — `corpus/SOURCES.md:270` (S491): its URL is the S003/S476
  `mm/oom_kill.c` URL, which raises the validate warning count 21 → 22 (`W04 S491 duplicate url …`). The
  contract anticipates exactly this ("a W04 warning, not an error"); rc stays 0 and no E-code appears. No
  action implied.
- **F3 — LOW (counting-instrument limit, frozen; reported not fixed)** — `scripts/sources-census.sh:40-41`
  parser behavior: a row-shaped line indented 4+ spaces is treated as indented code and is invisible to both
  the row count and `E12` (probe: `S903` produced no code and no count), while 1–3 spaces are counted and (if
  outside the Registry) flagged `E12`. An accidental four-space indent would therefore cause a silent
  undercount of `rows`/`tier.*`/`status.*` with a clean-looking lane. Current data has zero such lines at
  both revisions, so today's numbers are unaffected. Named limit of the census, not a proposed counter change.
- **F4 — LOW (baseline confirmation for the contract's frontier step)** —
  `.ufo/waves/round-50/evidence/census-start.txt`: reproduced byte-identically from `git archive 7197160b`
  (21 W04 + ok, rc 0) once the `ok` path line is normalized and the evidence file's extra trailing
  `census-rc=0` line (not part of the script's stdout) is dropped. The round-start baseline is therefore
  verifiable from the frozen bytes.
- **F5 — LOW (integration obligation, not a current defect)** — `.ufo/waves/round-50/evidence/`: no
  `census-end.txt` at the landed tip, while `contract.md` §Frontier step requires a round-end census with the
  same command. The L1 owes that run at closure; the numbers it should print, if SOURCES.md is unchanged, are
  `rows=264 tier.A=233 tier.B=14 tier.C=17 status.mined=214 status.queued=24 status.rejected=26` with 22 W04
  and rc 0.
- **F6 — LOW (label hazard when citing this report)** — an isolated `--root` run makes `FLEET.*` mean "the
  scratch root's fleet": it prints `FLEET.rows 261/264` for the one-lane scratch roots, against the live
  fleet's `3217`. Anyone citing `FLEET.rows 264` from the scratch output as a fleet total would be wrong; the
  correct fleet figure at measurement time is 3217 rows over 21 lanes.

## Verification status

Every statement above is observed command output from this seat's own runs (command + output + exit code
quoted inline); UNVERIFIED applies only to the items listed under named limits (whether the live fleet's other
lanes would change the mori lane's W04 set — no, but I did not enumerate them per lane; and the census
script's selftest arm internals). No lane, fleet, jj or git index state was mutated (only `git archive`,
`git cat-file`, `git log`, `git diff`, `sha256sum`, `grep`, `awk`, `diff`, `tar`, `cp`, `mkdir`, `rm` under
scratch were used). No pacman transaction; no host log MESSAGE read; no credential or session material read.
No `/tmp` path is cited as evidence. Scratch `/fast/scratch/hyaku/mori-r50/Mo50bExecCensusCounts` was removed
after this report was written; every quoted output was copied above first.
