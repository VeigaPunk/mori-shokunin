measured 2026-10-23T08:55:07Z

# mori round 35 — wave 1 — AxesOracle (Repair 6, not a claim)

Seat: `MoriR35.AxesOracle`. Scope: `SCORECARD.md:6-15` `## Axes` — recompute each row's `Last change` from the
fleet `MANIFEST.json` at `37b51a24` and rebind the evidence pointer to the line that grades the axis. Read-only over
the lane; no claim counter was run; no lane file was edited (this report is the only lane write).

Definitions used (read off the frozen records, not invented):
- Admitted mori closure = `MANIFEST.json` round with `lane == "mori"` and `admitted == true`. Rejected rounds are
  excluded: 13 (`rejected-harmed`), 17 (`rejected-harmed`), 20 (`rejected-harmed`), 23, 27, 29, 30, 32, 33, 34
  (`rejected-honest-stop`).
- Oracle round for an axis = the highest `lane_round` among admitted mori closures whose `verdicts.<axis>` is
  `improved`.
- Table round = the `round N` token in the row's last cell at lane rev `dd76eb79`.

`git -C /home/vgpnk/Projects/shokunin show 37b51a24…:MANIFEST.json` gives these admitted-improved rounds per axis
(index = `rounds[i]`, `lane_round` = round): coverage 12(313), 14(339), 15(345), 16(353), 24(443), 25(455), 26(462);
operability 18(386), 28(476), 31(495); depth 12(313), 31(495); freshness 21(412), 26(462), 28(476); calibration
12(313), 18(386), 19(398), 21(412), 22(427), 24(443), 25(455); adjacency 14(339), 18(386), 19(398).

`rounds[495]` (mori round 31) reads `admitted: true`, `verdict: "admitted"`, `verdicts: {coverage: unchanged,
operability: improved, depth: improved, freshness: unchanged, calibration: unchanged, adjacency: unchanged}`,
`spotcheck: "mori-shokunin/corpus/lessons/round-31-verifier-spotcheck.md@641a6e86ecc60634d215c0a47ab86c47661abf86"`.

## Oracle script (scratch, read-only) — 57 lines, sha256 `0df09582469b09c8ab3ca28bb731918662653a765b161c608c1018ecb86cd236`

Path: `/fast/scratch/hyaku/mori-r35/AxesOracle/axis-oracle.py`. Only `git show`; writes nothing.

```python
#!/usr/bin/env python3
"""Read-only oracle: SCORECARD Axes `Last change` vs the latest admitted mori
closure grading the axis improved (fleet MANIFEST 37b51a24), plus its grade line.
Usage: axis-oracle.py [lane-rev] [--lane R] [--fleet R] [--fleet-rev V]."""
import argparse, json, re, subprocess, sys
AXES = ["coverage", "operability", "depth", "freshness", "calibration", "adjacency"]
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
FREV = "37b51a243302e8009c7067431e8a47f9a722fd14"

def git(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout

def table_rounds(text):
    out, inside = {}, False
    for line in text.splitlines():
        if line.startswith("## Axes"): inside = True; continue
        if inside and line.startswith("## "): break
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if inside and line.startswith("|") and len(c) >= 4 and c[0] in AXES:
            m = re.search(r"round (\d+)", c[-1])
            out[c[0]] = int(m.group(1)) if m else None
    return out

def grade_line(lane, spec, ax):
    if "@" not in spec: return "-"
    path, rev = spec.rsplit("@", 1)
    if not path.endswith(".md") or " " in path: return "-"
    try: text = git(lane, rev, re.sub(r"^mori-shokunin/", "", path))
    except subprocess.CalledProcessError: return "-"
    hit = [i for i, l in enumerate(text.splitlines(), 1) if l.startswith(f"| {ax} | improved")]
    return f"{path}:{hit[0]}" if hit else "-"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?", default="dd76eb79")
    for k, v in (("--lane", LANE), ("--fleet", FLEET), ("--fleet-rev", FREV)):
        ap.add_argument(k, default=v)
    a = ap.parse_args()
    best = {}
    for r in json.loads(git(a.fleet, a.fleet_rev, "MANIFEST.json"))["rounds"]:
        if r.get("lane") != "mori" or not r.get("admitted"): continue
        sc = (r.get("verification") or {}).get("spotcheck", "") or "-"
        for ax in AXES:
            if (r.get("verdicts") or {}).get(ax) == "improved" and r["lane_round"] > best.get(ax, (0,))[0]:
                best[ax] = (r["lane_round"], sc)
    tbl = table_rounds(git(a.lane, a.rev, "SCORECARD.md"))
    for ax in AXES:
        t, (o, sc) = tbl.get(ax), best.get(ax, (None, "-"))
        print(f"{ax:12s} table={t} oracle={o} {'MISMATCH' if t != o else 'ok':8s} "
              f"grade={grade_line(a.lane, sc, ax)}")
    print("axes=%d mismatches=%d lane_rev=%s fleet_rev=%s" % (len(AXES),
          sum(tbl.get(x) != best.get(x, (None,))[0] for x in AXES), a.rev, a.fleet_rev[:8]))
    return 0

sys.exit(main())
```

Run at the measured rev:

```
$ python3 axis-oracle.py dd76eb79
coverage     table=26 oracle=26 ok       grade=mori-shokunin/corpus/lessons/round-26-verifier-spotcheck.md:133
operability  table=28 oracle=31 MISMATCH grade=mori-shokunin/corpus/lessons/round-31-verifier-spotcheck.md:155
depth        table=12 oracle=31 MISMATCH grade=mori-shokunin/corpus/lessons/round-31-verifier-spotcheck.md:154
freshness    table=28 oracle=28 ok       grade=mori-shokunin/corpus/lessons/round-28-verifier-spotcheck.md:92
calibration  table=25 oracle=25 ok       grade=mori-shokunin/corpus/lessons/round-25-verifier-spotcheck.md:124
adjacency    table=19 oracle=19 ok       grade=-
axes=6 mismatches=2 lane_rev=dd76eb79 fleet_rev=37b51a24
EXIT=0
```

Same two mismatches at lane tip `913df22` (`tail -3` of a second run: `calibration table=25 oracle=25 ok`,
`adjacency table=19 oracle=19 ok`, `axes=6 mismatches=2 lane_rev=913df22 fleet_rev=37b51a24`). The four `ok` rows
reproduce the cites already in the table (`SCORECARD.md:10,13,14`), so the oracle is not blanket-mismatching — that
is the parser's positive control. `adjacency` prints `grade=-` because its MANIFEST spotcheck cell is prose
(`rounds[398].verification.spotcheck` contains spaces), not a `path@rev` binding; the row at `SCORECARD.md:15`
already says so and stays unchanged.

## Grade-line checks (the cited line must state the grade)

`git show dd76eb79:corpus/lessons/round-31-verifier-spotcheck.md | grep -n "^| depth \|^| operability "` →

```
154:| depth | improved | C1 verified (§3); score stays 5 unless a closure states the move. This closure states none |
155:| operability | improved | C2 verified (§3); the score stays 7 |
```

- Line numbers hold at the closure's own spot-check commit: the same two lines are `641a6e8` lines 154/155, and
  `git diff --stat 641a6e8 dd76eb79 -- corpus/lessons/round-31-verifier-spotcheck.md` is empty (no output).
- Section context: the per-axis table sits under `## 4. Per-axis verdicts and no-harm` (heading at
  `641a6e8:corpus/lessons/round-31-verifier-spotcheck.md:138`), and C1/C2 are titled
  `### C1 — depth: watchdog identity decision table — **verified (re-measured)**` (`:81`) and
  `### C2 — operability: `tools/mori-blind-check.sh` — **verified (evidence-verified)**` (`:109`).
- Each line states the grade word (`improved`) for its axis and states the held score (5 and 7), which matches the
  score cells at `SCORECARD.md:11-12`.

## Positive control — the draft rows close the mismatch (sandbox only)

`git clone --no-hardlinks` of the lane into `/fast/scratch/hyaku/mori-r35/AxesOracle/clone`, the two draft rows pasted
in, sandbox commit `86126bf` (`git show --stat 86126bf` → `SCORECARD.md | 4 ++--`, one file, 2 insertions/2 deletions;
`git diff dd76eb79 HEAD --numstat -- SCORECARD.md` → `2  2  SCORECARD.md`). Oracle over that sandbox:

```
$ python3 axis-oracle.py 86126bf --lane /fast/scratch/hyaku/mori-r35/AxesOracle/clone
coverage     table=26 oracle=26 ok       grade=mori-shokunin/corpus/lessons/round-26-verifier-spotcheck.md:133
operability  table=31 oracle=31 ok       grade=mori-shokunin/corpus/lessons/round-31-verifier-spotcheck.md:155
depth        table=31 oracle=31 ok       grade=mori-shokunin/corpus/lessons/round-31-verifier-spotcheck.md:154
freshness    table=28 oracle=28 ok       grade=mori-shokunin/corpus/lessons/round-28-verifier-spotcheck.md:92
calibration  table=25 oracle=25 ok       grade=mori-shokunin/corpus/lessons/round-25-verifier-spotcheck.md:124
adjacency    table=19 oracle=19 ok       grade=-
axes=6 mismatches=0 lane_rev=86126bf fleet_rev=37b51a24
EXIT=0
```

The sandbox commit exists only inside `/fast/scratch/hyaku/mori-r35/AxesOracle/clone`; it does not touch lane state
and exists only to measure the draft.

## DRAFT Axes rows

Replace `SCORECARD.md:11` (operability) and `SCORECARD.md:12` (depth), nothing else. Both cells are whole table rows
so the L1 can paste them over the current lines; the `Score` cells are unchanged.

```DRAFT Axes rows
| operability | 7 | census `--selftest` PASS (134 cases) before and after round 24 (`SCORECARD.md` round-24 measured outcome); 7 was first set in round 13's table (6 → 7), which closed rejected-harmed; first held in round 14's admitted table and kept since (round 14's closure grades operability unchanged and states the scores, `corpus/lessons/round-14-verifier-spotcheck.md:87`); round-28 closure grades operability improved (ten A2 rules pinned by 30 frozen cases) (`corpus/lessons/round-28-verifier-spotcheck.md:93`); latest admitted closure grades operability improved (blind-writer gate `tools/mori-blind-check.sh`, C2 verified) and states the score stays 7 (`corpus/lessons/round-31-verifier-spotcheck.md:155`) | round 31 (improved, score held) |
| depth | 5 | source-linked knowledge entries with `source:`/`verified-at:`/`recheck:` lines (round 12 claim 1); the round-12 closure states the move (`corpus/lessons/round-12-verifier-spotcheck.md:17`); latest admitted closure grades depth improved (watchdog identity decision table, C1 re-measured) and states the score stays 5 (`corpus/lessons/round-31-verifier-spotcheck.md:154`); round 27's depth improvement was verified under a rejected-honest-stop closure and is not counted | round 31 (improved, score held) |
```

If a smaller diff is preferred, the two edits alone are: operability last cell `round 28 (improved, score held)` →
`round 31 (improved, score held)` and its clause "latest admitted closure … (`…round-28-verifier-spotcheck.md:93`)"
repointed to `…round-31-verifier-spotcheck.md:155`; depth last cell `round 12 (4 → 5)` → `round 31 (improved, score
held)` and the round-31 clause inserted before the round-27 sentence. The full-row drafts above also preserve the
round-28/round-12 history rather than dropping it.

## Verdicts (per axis; code repair)

VERDICT: coverage no defect found
VERDICT: operability defect
VERDICT: depth defect
VERDICT: freshness no defect found
VERDICT: calibration no defect found
VERDICT: adjacency no defect found

Operability defect: `SCORECARD.md:11` last cell says round 28, but the latest admitted improved closure is mori round
31 (`MANIFEST.json rounds[495]`, `verdicts.operability: improved`) and its grade line is
`corpus/lessons/round-31-verifier-spotcheck.md:155`. Depth defect: `SCORECARD.md:12` last cell says round 12, while
mori round 31 is the latest admitted improved closure (`rounds[495].verdicts.depth: improved`), grade line `:154`;
the row's own sentence about round 27 being rejected remains true and is kept.

## Containment, risks, blockers

- Writes: this report plus the scratch script and sandbox clone under
  `/fast/scratch/hyaku/mori-r35/AxesOracle/` (allowed scratch root). No lane file, no git/jj write,
  no fleet/sibling write, no process left running (all commands under `timeout`).
- No tools installed or updated this seat.
- Risk (semantic, for the L1): the drafted cells read `Last change` as "latest admitted closure grading the axis
  improved", per the frozen contract's ruling; if the column is meant as "last numeric move" the depth cell would
  instead stay round 12. The frozen contract (`contract.md` §"Not claims" item 6) already rules the round-31 reading,
  so the draft follows it.
- Risk (binding): the cited lines are in an append-only lesson file, so they are stable; the SCORECARD edit itself
  does not move them. Measured in the sandbox above: the two draft rows give `mismatches=0` (`86126bf`).
- No blockers. The two counters and the frozen C1 predicate were not touched; nothing here is counted by P-C1.
