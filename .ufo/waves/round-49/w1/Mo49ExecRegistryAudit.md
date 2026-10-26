# Mo49ExecRegistryAudit — false-red audit across SKILL.md history

Lane: mori-shokunin (leaf seat, round 49 wave w1). Measured 2026-10-25.
Frozen contract read first: `.ufo/waves/round-49/contract.md` (freeze `0df17b7b`); entering tip read:
`b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`; baseline arm `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`.
Tools under test (bytes untouched, sha256 re-read):
`controls/tool-v3-entering.py` `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`,
`controls/tool-r48-merged-witness.py` `c30ab6232893d984d1440784b6ce962d7c987c6d5538db0ead2f458a8ea1c9f0`.

## Question

For every lane revision that changed `SKILL.md` in the last 60 commits, run BOTH the entering tool
(v3) and the L1-merged witness with `--skill <that revision's SKILL.md written to scratch>` against
the entering tip and the round-48 baseline; any revision where the witness says `unmet` and v3 says
`met` is a candidate false red, to be classified TRUE-FINDING or FALSE-RED.

## Result (headline)

- 60 revisions audited; 120 tool runs (2 tools × 60 revisions), 4-way parallel.
- **2** revisions: v3 `met`, witness `met` (`91fbbc2a`, `e4dfff32`).
- **58** revisions: v3 `unmet`, witness `unmet`.
- **0** revisions: v3 `met`, witness `unmet` — **no candidate false red exists in this span**.
- **0** revisions: v3 `unmet`, witness `met`.
- On 60/60 revisions the two tools' counters are identical; the only byte difference in each pair of
  output files is the witness's extra `misattributed=0` field in the verdict line. Summed over the 60
  revisions: `tally_pins=279 digest_pins=101 mismatches=78 unparsed=0 no_command=0 dropped=1572
  rebound=0 duplicate=0 hidden=0` for v3, and the same plus `misattributed=0` for the witness.
- The top revision `91fbbc2a` carries the **same SKILL.md bytes as the entering tip**
  (sha256 `063be309e5d1d0eb6f498dd00a66527e66101e0e60dfad0fa7d9228542a55293`), so that row IS the
  entering registry, and the witness's `met` there reproduces the freeze receipt in `contract.md`
  (witness row, `C1=met … variants=26`). `e4dfff32` (sha256 `62602b2e438a…`) is a different SKILL.md
  and is `met` under both tools as well.

## Exact commands

Setup and per-revision invocation (run 4-way in parallel by
`.scratch/r49-Mo49ExecRegistryAudit/run-audit.sh` — v3 half — and `.../run-witness.sh` — witness half):

```bash
BASE=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecRegistryAudit
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
CTL=$LANE/.ufo/waves/round-49/controls
REV=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
BASELINE=2d85e33d14198d388fd3cda9cc15ec07e57e7a53
export TMPDIR=$BASE/tmp; mkdir -p "$TMPDIR" "$BASE/skills" "$BASE/out"

# 1. every SKILL.md revision of the last 60 commits, written to scratch
cd "$LANE"
for r in $(git log --format=%H -n 60 -- SKILL.md); do
  git show "$r:SKILL.md" > "$BASE/skills/$r.md"
done

# 2. both tools, same flags, per revision (4 parallel; one call per tool per revision)
python3 "$CTL/tool-v3-entering.py"        --skill "$BASE/skills/$r.md" --rev "$REV" --repo "$LANE" \
        --min-tally-pins 1 --baseline-rev "$BASELINE" > "$BASE/out/$r.v3-entering.py.txt" 2>&1
python3 "$CTL/tool-r48-merged-witness.py" --skill "$BASE/skills/$r.md" --rev "$REV" --repo "$LANE" \
        --min-tally-pins 1 --baseline-rev "$BASELINE" > "$BASE/out/$r.witness.txt" 2>&1

# 3. liveness probes (do the witness's new arms fire at all under these invocations?)
python3 "$CTL/tool-v3-entering.py"        --skill "$BASE/probe/p1-misattributed.md" --rev "$REV" --repo "$LANE" --min-tally-pins 1
python3 "$CTL/tool-r48-merged-witness.py" --skill "$BASE/probe/p1-misattributed.md" --rev "$REV" --repo "$LANE" --min-tally-pins 1
python3 "$CTL/tool-v3-entering.py"        --skill "$BASE/probe/p2-indented.md"     --rev "$REV" --repo "$LANE" --min-tally-pins 1
python3 "$CTL/tool-r48-merged-witness.py" --skill "$BASE/probe/p2-indented.md"     --rev "$REV" --repo "$LANE" --min-tally-pins 1
```

Per-revision outputs: `.scratch/r49-Mo49ExecRegistryAudit/out/<rev>.v3-entering.py.txt` and
`<rev>.witness.txt`; probe skills and outputs under `.scratch/r49-Mo49ExecRegistryAudit/probe/`;
witness exit codes recorded in `out/rcs-witness.txt` (`rc=0` ×2, `rc=1` ×58).

### Batch integrity disclosure

The first batch fed a three-field line (`<rev> <tool> <tag>`) to `xargs -n 2`, which splits on
whitespace, not lines: the v3 half happened to run correctly (pairs `<rev> tool-v3-entering.py`) but
the witness half ran `python3 <rev>` (60 `rc=2` setup failures) and the extra pairs were noise. Those
60 garbage files are parked in `out/../garbage/` and are NOT evidence; the witness was rerun with
`xargs -I{}` (one revision per invocation) and the 60 files in `out/*.witness.txt` are that rerun.
The v3 files in `out/*.v3-entering.py.txt` predate that bug and carry genuine verdicts (verified by
content: per-revision counter differences, `PIN_CHECK=` lines, in-tree `cmd=` names).

## Table — revision, v3 verdict line, witness verdict line

Every verdict line below is verbatim (only the trailing `(rc=N)` is derived: both tools return
`0 if met else 1`, tool-v3-entering.py:683 / tool-r48-merged-witness.py:758).

| # | revision | date | v3-entering (rc) | r48-merged-witness (rc) |
|---|---|---|---|---|
| 1 | `91fbbc2a` | 2026-10-25 | `PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=0) | `PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=0) |
| 2 | `e4dfff32` | 2026-10-25 | `PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=0) | `PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=0) |
| 3 | `af2250d8` | 2026-10-25 | `PIN_CHECK=unmet tally_pins=28 digest_pins=8 mismatches=2 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=28 digest_pins=8 mismatches=2 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 4 | `4dea3d09` | 2026-10-25 | `PIN_CHECK=unmet tally_pins=28 digest_pins=8 mismatches=2 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=28 digest_pins=8 mismatches=2 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 5 | `2f04605a` | 2026-10-25 | `PIN_CHECK=unmet tally_pins=26 digest_pins=8 mismatches=2 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=26 digest_pins=8 mismatches=2 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 6 | `18fd68b0` | 2026-10-25 | `PIN_CHECK=unmet tally_pins=28 digest_pins=6 mismatches=12 unparsed=0 no_command=0 dropped=5 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=28 digest_pins=6 mismatches=12 unparsed=0 no_command=0 dropped=5 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 7 | `7cb59c68` | 2026-10-25 | `PIN_CHECK=unmet tally_pins=10 digest_pins=1 mismatches=3 unparsed=0 no_command=0 dropped=21 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=10 digest_pins=1 mismatches=3 unparsed=0 no_command=0 dropped=21 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 8 | `265a955c` | 2026-10-24 | `PIN_CHECK=unmet tally_pins=6 digest_pins=1 mismatches=2 unparsed=0 no_command=0 dropped=25 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=6 digest_pins=1 mismatches=2 unparsed=0 no_command=0 dropped=25 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 9 | `f920eaf7` | 2026-10-24 | `PIN_CHECK=unmet tally_pins=5 digest_pins=1 mismatches=2 unparsed=0 no_command=0 dropped=26 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=5 digest_pins=1 mismatches=2 unparsed=0 no_command=0 dropped=26 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 10 | `daa1d4d2` | 2026-10-23 | `PIN_CHECK=unmet tally_pins=5 digest_pins=1 mismatches=2 unparsed=0 no_command=0 dropped=26 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=5 digest_pins=1 mismatches=2 unparsed=0 no_command=0 dropped=26 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 11 | `4bfa0490` | 2026-10-23 | `PIN_CHECK=unmet tally_pins=4 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=27 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=4 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=27 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 12 | `9ca8f2eb` | 2026-10-23 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 13 | `bf0df77f` | 2026-10-23 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 14 | `42a8ae65` | 2026-10-23 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 15 | `6d3d94b3` | 2026-10-23 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 16 | `cedb0ec4` | 2026-10-23 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 17 | `8d56809a` | 2026-10-23 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 18 | `ab8f4cfe` | 2026-10-23 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 19 | `62db24c0` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 20 | `7766732a` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 21 | `d0cac478` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 22 | `efcb7324` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 23 | `458ff1c3` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 24 | `5b728304` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 25 | `d03203c5` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 26 | `95cd794e` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 27 | `ee61010d` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 28 | `af42101d` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 29 | `1c4c186e` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 30 | `5e500d99` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 31 | `47f6543a` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 32 | `b89ac342` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 33 | `79ecf58b` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 34 | `126e192d` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 35 | `327fbcca` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=3 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=28 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 36 | `86477e8b` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=30 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=30 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 37 | `8ef481ea` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=30 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=30 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 38 | `575a9f3f` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=30 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=30 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 39 | `a536b184` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=30 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=30 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 40 | `6fce88a3` | 2026-10-22 | `PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=30 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=30 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 41 | `0d8f2d50` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 42 | `1979a9de` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 43 | `50b6f754` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 44 | `8cb4afbf` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 45 | `9fb1f911` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 46 | `ce413b9d` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 47 | `a8442a01` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 48 | `71abd41f` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 49 | `8f8c58ee` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 50 | `a4f79dd4` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 51 | `367927c5` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 52 | `9db51685` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 53 | `daceeec8` | 2026-10-21 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 54 | `2be82940` | 2026-10-20 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 55 | `273aa74a` | 2026-10-20 | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 56 | `114ebe5e` | 2026-10-20 | `PIN_CHECK=unmet tally_pins=0 digest_pins=2 mismatches=2 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=2 mismatches=2 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 57 | `26f6589d` | 2026-10-20 | `PIN_CHECK=unmet tally_pins=0 digest_pins=2 mismatches=2 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=2 mismatches=2 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 58 | `52512aea` | 2026-10-20 | `PIN_CHECK=unmet tally_pins=0 digest_pins=2 mismatches=2 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=2 mismatches=2 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 59 | `8d22d18f` | 2026-10-20 | `PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |
| 60 | `80bd58a4` | 2026-10-20 | `PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) | `PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=31 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes` (rc=1) |

## Classified list of candidates

**Empty.** No revision in the 60-commit span has the witness `unmet` while v3 is `met`, so there is
no candidate to classify: **0 TRUE-FINDING, 0 FALSE-RED**.

The 58 `unmet` revisions are `unmet` under both tools, and for the same reasons. Those findings are
therefore not witness-specific and cannot be candidates by the acceptance rule; they are recorded
here so the L1 can see what the audit excluded and why:

| class | revisions | finding lines (identical under v3 and witness) | reading |
|---|---|---|---|
| baseline drops | 55 revisions, rev 06 `18fd68b0` … rev 60 `80bd58a4` | `pin kind=baseline state=dropped row='r44 gate registry (C2)' pin=sha256 count=1` (rev 06 `18fd68b0`) | artifact of the prescribed flags: `--baseline-rev 2d85e33d` is *newer* than these SKILL.md revisions, so pins that did not exist yet count as dropped (summed `dropped=1572`) |
| tally drift (old pin, tip code) | 56 revisions, rev 03 `af2250d8` … rev 58 `52512aea` | rev 03 `af2250d8` `SKILL.md:938` pins `` `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` ``; observed `pass=60 fail=0`, rc=0 — `pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=mismatch pinned='pass=34 fail=0' observed='pass=60 fail=0'` | the audit mixes an old registry with the entering tip's code tree, so a self-test tally that legitimately moved between rounds reads as a mismatch (summed `mismatches=78`) |
| digest drift | the same 56 revisions | rev 03 `af2250d8` `SKILL.md:168` (the `r14 regressions` row): `pin line=168 kind=digest state=mismatch digest=c39e5a73… file=None` | same cause: the digest pinned in round 14 no longer equals the tip's file |
| new-arm findings (hidden / misattributed / duplicate / unparsed) | none | — | zero on all 60 revisions |

Structural (tree-independent) arms are the only ones that could produce a false red, and they are
silent on the whole span: `hidden=0`, `misattributed=0`, `duplicate=0`, `unparsed=0`,
`no_command=0`, `rebound=0` at every revision, with `tally_pins=279` evaluated in total (41 finding
lines at each of the two `met` revisions — 31 tally, 8 digest, 2 line-count — all `state=match`).

## Liveness evidence — the witness's new arms do fire under this invocation

Two scratch skills were built from the honest pin
`` `python3 tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=13 fail=0` `` so that
the null above cannot be an inactive-code artifact.

P1 — entry cell names instrument A, self-test cell runs instrument B (R11 shape):

```
$ python3 .ufo/waves/round-49/controls/tool-v3-entering.py --skill $BASE/probe/p1-misattributed.md \
      --rev b3e3453d... --repo . --min-tally-pins 1
pin line=3 kind=tally prefix=UNLANDED_SELFTEST state=match pinned='pass=13 fail=0' observed='pass=13 fail=0' rc=0 cmd='python3 tools/mori-unlanded-check.py --selftest'
PIN_CHECK=met ... mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 ...
$ python3 .ufo/waves/round-49/controls/tool-r48-merged-witness.py --skill $BASE/probe/p1-misattributed.md \
      --rev b3e3453d... --repo . --min-tally-pins 1
pin line=3 kind=tally prefix=UNLANDED_SELFTEST state=misattributed claimed=tools/mori-silence-cases.sh bound=tools/mori-unlanded-check.py
PIN_CHECK=unmet ... mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=1 ...
```

P2 — the same honest row plus a four-space-indented pipe line carrying `--selftest`, placed after
prose (outside any table, so v3's `^ {0,3}\|` does not see it):

```
$ python3 .../tool-v3-entering.py        --skill $BASE/probe/p2-indented.md --rev b3e3453d... --repo . --min-tally-pins 1
PIN_CHECK=met ... hidden=0 ...
$ python3 .../tool-r48-merged-witness.py --skill $BASE/probe/p2-indented.md --rev b3e3453d... --repo . --min-tally-pins 1
pin line=6 kind=row state=hidden row='    | loose | gate | `python3 tools/foo.py` | 0 ok | `FOO_SELFTEST pass=1 fail=0'
PIN_CHECK=unmet ... hidden=1 ...
```

Both new arms are live: `misattributed` and the widened `hidden` rule each turn an otherwise-honest
registry red when the forbidden shape is present, and neither fires on any of the 60 historical
SKILL.md revisions.

## Named limits (observed, not closed)

- The prescribed *verdict* test can only speak on revisions where v3 is `met` — 2 of 60. On the other
  58, the `--baseline-rev` arm (baseline newer than the revision) and pin/code drift dominate, so
  "witness agrees with v3" there is weak evidence on its own. The substantive audit therefore rests on
  the arms instead: `misattributed` (entry cell versus bound argv), `hidden` (line shapes), `duplicate`
  (one command, two exit contracts) and `unparsed` (span shape / header recognition) are all decided
  from SKILL.md plus the registry's own cells and do not depend on the measured tree. Those arms are
  therefore fully exercised against every one of the 60 registries by these runs, and each produced
  zero findings. Only `mismatches`, `dropped` and `rebound` are tree/baseline dependent, and both
  tools compute them identically (proved: stripping the `misattributed=` field makes all 60 verdict
  pairs byte-identical).
- Not measured: revisions older than the 60-commit window; the uncommitted working tree (siblings are
  mid-wave, `SKILL.md` unmodified); either tool's `--selftest`; the C1 target tool (the witness is a
  feasibility witness, not the claim's tool).
- The witness's R11 mutant carve-out is load-bearing for honest rows: at `91fbbc2a`, `SKILL.md:190`
  and `:192` bind `python3 .ufo/waves/round-45/fixtures/mutants/count-c1.py --selftest` and
  `.../count-c3.py --selftest` while their entry cells name `.ufo/waves/round-45/count-c1.py` /
  `count-c3.py`; basename equality under `fixtures/mutants` is what keeps those two pins green.

## Findings

- **MED** — the prescribed candidate test is non-discriminating on 58 of 60 revisions: with
  `--baseline-rev 2d85e33d` (round 48) applied to revisions as old as round 13, the dropped arm
  contributes 1572 findings (55 revisions) and pin/code drift 78 mismatches (56 revisions), so a
  v3-`met` row (the precondition for a candidate) can only exist at `91fbbc2a`/`e4dfff32`. Concern:
  `.ufo/waves/round-49/contract.md` frontier item (c) reads as a history-wide false-red clearance, but
  the verdict rule yields one bit — "no false red on the entering registry". The history-wide result
  this seat can defend is the arm-level one: the four new arms are tree-independent and silent on all
  60 registries. A revision-local pass (`--rev <rev>` with that revision's SKILL.md) would make the
  verdict rule itself speak across the span; it is not needed for the arm conclusion and was not run
  (it would execute round-13-era tools).
- **LOW** — R11's mutant carve-out (basename equality under a `fixtures`/`mutants` segment) is the
  only reason `SKILL.md:190` and `:192` at `91fbbc2a` are `met`: their entry cells name
  `.ufo/waves/round-45/count-c1.py` / `count-c3.py`, their self-test cells bind
  `fixtures/mutants/count-c1.py` / `count-c3.py`. Any wave-2 tightening of R11 that drops the
  basename test (or requires the mutant path in the entry cell) converts two honest pins into
  `misattributed` — a false red the claim's counter would score as junk_met=0 but which the lane
  would have to repair.
- **LOW** — old-revision verdicts are dominated by pin/code drift, e.g. `af2250d8` `SKILL.md:938`
  pins `PIN_CHECK_SELFTEST pass=34 fail=0` while the tip tool prints `pass=60 fail=0` and `SKILL.md:168`
  pins digest `c39e5a73…` with `file=None`. Any later reader of these receipts who reads only
  `unmet` will mislabel honest round-47-and-earlier registries as dishonest; the receipts keep the
  finding lines, so the misreading is preventable but not structurally excluded.
- **MED** — the pin reconciler leaks its export on every killed run: `.scratch/pin-check-*` held 88
  directories at 22:02-22:07 on 2026-10-25 — 75 with a full `tree/` export, 24 with `tree.tar`
  (11 with both, none empty), each 310-324 MB in three sampled dirs (≈27 GB total if that rate holds;
  `df` 349G/930G used), and new ones appear while sibling seats run the instrument. Cause:
  `controls/tool-v3-entering.py:649-652` builds the export under `<repo>/.scratch/pin-check-*` and
  `:685` (`tool-r48-merged-witness.py:760`) removes it only in `finally: shutil.rmtree(scratch)`,
  which a SIGKILL bypasses — a counter `--timeout` kill (contract: "a tool crash, setup exit or
  timeout is `errors`"), or a killed wave job. A dir with `tree.tar` is a run killed during
  extraction; a dir with only `tree/` was killed later, while running the registry's commands.
  `.scratch/` is already in `.gitignore` (line 5), so `git status --porcelain` stays clean and the
  growth is silent. Concern: `.ufo/waves/round-49/count-c1.py` (26 variants, one export each) and
  `.ufo/waves/round-49/controls/*`; a sweep of `pin-check-*` dirs older than the current wave plus a
  narrower `git archive` (SKILL.md + `tools/` + `.ufo/waves/`) would stop it. The removal belongs to
  the lane, not to this seat.

No tool was installed or upgraded for this seat (python3 and git from the host were sufficient); no
host mutation, no `pacman`, no git write, no jj command. My own writes went only to
`.scratch/r49-Mo49ExecRegistryAudit/` and this report file; the prescribed runs do leave lane-side
artifacts through the tools themselves — see the last finding.

## Side effects observed while running the prescribed command

- `mori-pin-check` exports the measured revision under `<repo>/.scratch/pin-check-*` and removes it in
  its `finally` block; a SIGKILL (counter timeout, killed job) bypasses that, leaving the export
  behind (75 of the 88 observed dirs hold a full `tree/`, 24 hold `tree.tar`; 310-324 MB per sampled
  dir). At 22:02-22:07 the lane held 88 such directories, newest created while sibling seats were
  running the same instrument, i.e. this is a fleet-wide artifact of the current wave, not of one
  seat. Disk: `/home` 349G used of 930G at that moment. I deleted nothing (siblings were live and lane
  state is not mine to mutate).
- Row-bound self-tests also create `.ufo/waves/round-40/scratch/mori-conform-selftest-*` when a
  historical registry row runs the round-40 conformance selftest; those dirs are the instruments'
  own, and the same pattern is present for rounds 37-41.
