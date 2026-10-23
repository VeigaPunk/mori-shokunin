# RevCensusFresh — fresh census re-run vs start receipt + registry row delta (round 38, wave 2)

Verdict: **PASS** — no E-lines, row delta is the claimed +1 (S226), and the lesson's census
paragraph reproduces. All commands run first-hand on 2026-10-23; the lane repo was not mutated.

## 1. Fresh census run

Command (as assigned):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

- Exit code: **0**
- Output: 16 lines — 15 `W04` warning lines (all `duplicate url ... across scopes`) plus the
  final `mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` line.
- **Zero E-class lines** (and zero new line classes of any kind).

## 2. Diff against `evidence/census-start.txt`

```
$ diff .ufo/waves/round-38/evidence/census-start.txt /tmp/census-fresh.txt
17d16
< CENSUS_EXIT=0
```

The only difference is the receipt's own `CENSUS_EXIT=0` trailer at line 17 — that line is the
receipt's recorded exit trailer, not census output. The 16 census output lines are
**byte-identical** to the start receipt. (My run's observed exit code 0 matches the trailer's
recorded `CENSUS_EXIT=0`.)

Cross-check: `evidence/census-end.txt` is also byte-identical to `census-start.txt` (same 16
output lines + `CENSUS_EXIT=0`), so the lesson's "start and round end" pairing holds on the
receipts.

## 3. Registry row counts (contract's frozen grep `grep -cE '^\| S[0-9]{3} '`)

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e33bb561712b32f46861362a3fa43762fa70ae4f:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} '
225
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show f725f3076972e6e70595b5ac8279be524a111ff8:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} '
226
```

- `e33bb561712b32f46861362a3fa43762fa70ae4f` (entering tip): **225** rows
- `f725f3076972e6e70595b5ac8279be524a111ff8` (scored tip): **226** rows
- Delta: **+1** — the claimed delta. Id-set diff (`grep -oE '^\| S[0-9]{3} ' | sort`) shows
  exactly one added id: `| S226 `. No id was removed or renumbered.

Companion check on the lesson's registry sentence ("no existing row's `status`, `recheck` or
`used-by` cell was edited"): `git diff e33bb561… f725f307… -- corpus/SOURCES.md` contains only
the `+| S226 |` row line and the appended "Round 38 bounded search" log block — no `-`/`+` pair
touches any existing row.

## 4. Lesson census paragraph

`corpus/lessons/round-38.md:15-16` claims:

> Census: `sources-census.sh validate mori` exit 0 at round start and round end, benign W04
> lines only (`evidence/census-start.txt`, `census-end.txt`).

Reproduced: the fresh run exits 0 with 15 W04 lines + one `ok` line and no other classes;
both receipts record `CENSUS_EXIT=0` over identical output. The paragraph's neighboring claims
also check out: the Gate table's single admitted candidate is S226 (`round-38.md:9`) matching
the +1 delta, and the registry-changes sentence matches the SOURCES.md diff (§3).

## 5. Fail-condition sweep

| Condition | Result |
|---|---|
| Any E-line in fresh output | none — 15 W04 + 1 ok only |
| Row delta ≠ +1 | delta is exactly +1 (225 → 226, new id S226) |
| Lesson claim not reproduced | all claims reproduced (exit 0 both ends, W04-only, S226 the sole registry addition) |

Tooling: no installs or upgrades were needed (system `bash`, `git`, `grep`, `diff` sufficed);
nothing was written outside this report.

Report: .ufo/waves/round-38/w2/RevCensusFresh.md
