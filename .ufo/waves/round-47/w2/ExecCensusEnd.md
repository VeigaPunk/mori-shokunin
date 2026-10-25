# ExecCensusEnd — round-47 w2 findings (falsify landed round)

Seat: ExecCensusEnd (leaf; no subagent spawned; labrat not needed). Scope: fleet sources census
validation + registry row/tier/status census at E=2d85e33d14198d388fd3cda9cc15ec07e57e7a53
and T=68d66ca53d89be5c34a62f46af7c37449d9f9b63 (master), freeze F=63eecf2. All paths below
are absolute. No tools installed (nothing needed; channel/reason n/a).

## 1. `sources-census.sh validate` — command, exit code, non-W04 lines

Command (run from scratch cwd; TMPDIR per lane rules):

```
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecCensusEnd \
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Exit code: **0** (validated against the working-tree registry; `sha256sum` of
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` = `e0c4c39b2804a16d51979bff3ceb9f1ff277b14cabb39b17bca2164f20ca911a` =
`git show T:corpus/SOURCES.md | sha256sum`, so the run exercised exactly T's registry bytes).

Non-W04 lines (complete): exactly one

```
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

No E01–E12, no unlisted, no missing lines.

## 2. W04 count vs baseline `evidence/census-start.txt`

- Baseline (census-start.txt): **19** W04 lines (S035 S037 S073 S074 S075 S076 S147 S148 S149
  S150 S166 S168 S201 S218 S220 S228 S349 S351 S470).
- Now: **20** W04 lines. `diff` of sorted W04 sets shows exactly one added line; all 19 baseline
  lines byte-identical, none removed:

```
> mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
```

Explanation: S476 is a new C2-surface row (v7.2 `mm/oom_kill.c` copy); the same URL already
exists on S003 in a different scope, so the validator's W04 fires. This is the same URL-across-
scopes warning class already accepted in the baseline; no new E-class finding.

## 3. Registry rows at E and T

`git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`:

- E: **247**
- T: **251** (+4)

(Cross-check: the census awk's own `rows` counter gives 247/251 too; every registry row carries a
valid S-id — no row shape anomalies.)

## 4. Tier / status histograms at both revs (reproduced CORPUS.md census awk)

The `row_pass` gawk program from `scripts/sources-census.sh` (census mode) run over
`git show <rev>:corpus/SOURCES.md` for each rev:

```
E (2d85e33): rows 247 | tier.A 216 tier.B 14 tier.C 17 tier.invalid 0
              | status.mined 196 status.queued 25 status.rejected 26 status.invalid 0
T (68d66ca): rows 251 | tier.A 220 tier.B 14 tier.C 17 tier.invalid 0
              | status.mined 201 status.queued 24 status.rejected 26 status.invalid 0
```

Deltas E→T: +4 rows, +4 tier.A, +5 mined, −1 queued; B/C/rejected/invalid unchanged.
FLEET missing output: 0 (no `missing` for mori).

## 5. New ids and per-row movement

New ids at T (absent at E), via sorted id-set diff (`comm` on the registry id column):

- **S475** — `code`/A/`mined`, opened 2026-10-25, recheck on-release, used-by
  `corpus/knowledge/oom-tracepoints-r47.md`. Source names Linux v7.2
  `include/trace/events/oom.h` (copy pinned with sha256 82f04ad4…). Matches P-C2's required
  SOURCES row shape (mined tier-A code row naming v7.2 and include/trace/events/oom.h, used-by =
  the entry).
- **S476** — `code`/A/`mined`, used-by the same entry; v7.2 `mm/oom_kill.c`,
  `mm/page_alloc.c`, `fs/proc/base.c` copies (source of the +1 W04, see §2).
- **S477** — `own-work`/A/`mined`, host tracefs receipt (evidence/host-tracefs.txt), used-by the
  same entry.
- **S478** — `paper`/A/`mined`, ROMA paper (IEEE TSC 2026), used-by the same entry.

Removed ids at T: none.

Status flip (only one): **S005 queued → mined** — this accounts for the histogram delta of +5
mined/−1 queued against only 4 new rows. No tier flips anywhere; no recheck/opened anomalies in
new rows (all opened 2026-10-25, recheck on-release or 90d).

## Verdict

Attack target: fleet census validation state and registry census at T vs E vs baseline. **Holds**
on the census surface: validate exits 0, zero E-findings, zero missing, histograms strictly
consistent with the landed change set (4 new C2-surface rows + one queued→mined promotion), and
the only W04 delta is the expected URL-across-scopes warning created by the new S476 copy row.
No census evidence falsifies the landed round. Not an independent judge of P-C1/P-C2; the census
observations are consistent with C2's intended footprint (S475/S476/S477/S478).

## Evidence retained

- Validate output: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecCensusEnd/validate-mori.txt` (exit 0)
- W04 sorted sets: `.../.scratch/r47w2-ExecCensusEnd/w04-base.txt`, `w04-now.txt` (diff = one added S476 line)
- SOURCES blobs: `.../.scratch/r47w2-ExecCensusEnd/E-SOURCES.md`, `T-SOURCES.md`
- Id/status/tier maps: `E-ids.txt`, `T-ids.txt`, `E-status.txt`, `T-status.txt`, `E-tier.txt`, `T-tier.txt`

Risks/blockers: none. Files changed: this report only.
