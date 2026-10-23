measured 2026-10-23T08:57:16Z

# MineAppendOnly — append-only checker for corpus/SOURCES.md (round-35 wave 1, seat MoriR35.MineAppendOnly)

Target: round 34 rewrote S182 and S193 in place, which CORPUS rule 2 forbids
(`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`: only `status`, `recheck`, `used-by` change in place;
a correction is a new row whose `teaches` opens `supersedes S0NN —`). Round 34's lesson claims the
opposite in the narrow sense (`corpus/lessons/round-34.md:46`: "No status or recheck cell of an existing
row changed"). Routed by `corpus/lessons/round-34-verifier-spotcheck.md:118,121,202-203`.
## Deliverable

`/fast/scratch/hyaku/mori-r35/MineAppendOnly/check-sources-appendonly.py` — 109 lines, python3 stdlib only, read-only git
(`rev-parse`, `log --reverse`, `cat-file -e`, `show`), every git call capped at `timeout=120`; sha256
`f56dbdafdc7e884f0598b46a21b0b440f3fbc09dc2d996077c9a7b5f1aa51f06`. For each row's first-seen commit in `<rev>`'s ancestry it
compares the 11 cells minus status(8), recheck(10), used-by(11), names every ancestry commit that changed a compared cell, and
discharges an id only when a row at `<rev>` has `teaches` starting `supersedes S###`. Full text:

```python
#!/usr/bin/env python3
"""check-sources-appendonly.py <rev> [--repo DIR] [--show-cells]

CORPUS.md rule 2 for corpus/SOURCES.md: only status (col 8), recheck (col 10)
and used-by (col 11) may change in place; any other rewrite must land as a new
row whose teaches opens `supersedes S###`.

For every `| S###` row of corpus/SOURCES.md at <rev>, find the first commit in
<rev>'s ancestry holding that id, compare the row's 11 cells with the cells at
<rev>, and flag each id whose compared cells differ when no row at <rev>
supersedes it. Each flag names every ancestry commit that changed a compared
cell.  exit: 0 no violation, 1 violation(s), 2 error.  Read-only git only.
"""
import argparse
import re
import subprocess
import sys

PATH = "corpus/SOURCES.md"
COMPARE = [0, 1, 2, 3, 4, 5, 6, 8]  # all but status(7), recheck(9), used-by(10)
NAMES = dict(zip(COMPARE, "id source kind tier scope anchor teaches opened".split()))
SUPERSEDES = re.compile(r"^supersedes\s+(S\d{3})\b")


def git(repo, *args):
    try:
        p = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                           text=True, timeout=120)
    except subprocess.TimeoutExpired:
        sys.exit("error: git %s timed out" % " ".join(args))
    if p.returncode != 0:
        sys.exit("error: git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout


def rows_at(repo, rev):
    spec = "%s:%s" % (rev, PATH)
    p = subprocess.run(["git", "-C", repo, "cat-file", "-e", spec],
                       capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        return {}
    out = {}
    for line in git(repo, "show", spec).splitlines():
        if not line.startswith("| S"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 11 or not re.fullmatch(r"S\d{3}", cells[0]):
            sys.exit("error: %s row with %d cells: %r" % (PATH, len(cells), line[:60]))
        out[cells[0]] = cells
    return out


def key(cells):
    return tuple(cells[i] for i in COMPARE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--show-cells", action="store_true")
    a = ap.parse_args()

    rev = git(a.repo, "rev-parse", "--verify", a.rev + "^{commit}").strip()
    tip = rows_at(a.repo, rev)
    if not tip:
        sys.exit("error: no | S### rows in %s at %s" % (PATH, rev))
    commits = git(a.repo, "log", "--reverse", "--format=%H", rev, "--", PATH).split()
    print("rev=%s rows=%d commits=%d" % (rev, len(tip), len(commits)))

    origin, first_at, changes, prev = {}, {}, {}, {}
    for c in commits:
        for i, cells in rows_at(a.repo, c).items():
            if i not in origin:
                origin[i], first_at[i], changes[i] = cells, c, []
            elif key(cells) != key(prev[i]):
                changes[i].append(c)
            prev[i] = cells

    superseded_by = {}
    for i, cells in tip.items():
        m = SUPERSEDES.match(cells[6])
        if m:
            superseded_by.setdefault(m.group(1), i)

    violations, discharged = [], []
    for i in sorted(tip):
        if i not in origin or key(tip[i]) == key(origin[i]):
            continue
        (discharged if i in superseded_by else violations).append(i)

    for i in discharged:
        print("SUPERSEDED id=%s by=%s origin=%s changed_at=%s"
              % (i, superseded_by[i], first_at[i], ",".join(changes[i]) or "?"))
    for i in violations:
        cols = [NAMES[k] for k in COMPARE if tip[i][k] != origin[i][k]]
        print("CHANGED id=%s origin=%s changed_at=%s cols=%s"
              % (i, first_at[i], ",".join(changes[i]) or "?", ",".join(cols)))
        if a.show_cells:
            for k in COMPARE:
                if tip[i][k] != origin[i][k]:
                    print("  %s @%s: %s" % (NAMES[k], first_at[i][:12], origin[i][k]))
                    print("  %s @%s: %s" % (NAMES[k], rev[:12], tip[i][k]))
    print("appendonly_violations=%d ids=[%s]" % (len(violations), ",".join(violations)))
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
```

## Runs (each `timeout 120 python3 check-sources-appendonly.py <rev> --repo <dir>`)

Run 1 — dd76eb79, lane repo, **exit 1**:
```
CHANGED id=S041 origin=273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7 changed_at=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 cols=teaches
CHANGED id=S044 origin=273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7 changed_at=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 cols=teaches
CHANGED id=S051 origin=daceeec8c04e0f44cc5130369e86f21fbaf5a3ad changed_at=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 cols=teaches
CHANGED id=S062 origin=daceeec8c04e0f44cc5130369e86f21fbaf5a3ad changed_at=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8,ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3 cols=teaches
CHANGED id=S064 origin=367927c56eb1a00613e1fed65e5c47245fd570b9 changed_at=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8,ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3 cols=scope,teaches
CHANGED id=S179 origin=55c3ed5e3386e1adf524a63589f51cc0540607fa changed_at=5126891f6b6c8d79763cb9271811468b81acd908 cols=scope,teaches
CHANGED id=S180 origin=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 changed_at=ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3 cols=anchor,teaches
CHANGED id=S181 origin=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 changed_at=ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3 cols=source,scope,anchor
CHANGED id=S182 origin=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 changed_at=ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3,8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 cols=anchor
CHANGED id=S183 origin=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 changed_at=ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3 cols=anchor,teaches
CHANGED id=S184 origin=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 changed_at=ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3 cols=anchor
CHANGED id=S185 origin=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 changed_at=ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3 cols=anchor,teaches
CHANGED id=S186 origin=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 changed_at=ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3 cols=scope,anchor,teaches
CHANGED id=S188 origin=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 changed_at=ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3 cols=scope,anchor,teaches
CHANGED id=S189 origin=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 changed_at=ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3 cols=anchor
CHANGED id=S190 origin=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 changed_at=ab8f4cfe81a6c12c5bf305c6116cf0b01d7eecf3 cols=scope,anchor,teaches
CHANGED id=S193 origin=8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 changed_at=406d91a4b891766e36272415df3bdaca87548d96 cols=anchor,teaches
appendonly_violations=17 ids=[S041,S044,S051,S062,S064,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193]
```
Run 2 — 3a7a89ea, lane, **exit 1**: 17 ids; after dropping `^rev=` the output is byte-identical to Run 1 (`diff` empty).
Run 3 — f10a320d, lane, **exit 1**: `rows=190 commits=43`, `appendonly_violations=16 ids=[S041,S044,S051,S062,S064,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190]`
— S193 absent (row did not exist yet) and S182's `changed_at` stops at ab8f4cfe (8d56809a is not an ancestor); all else matches Run 1.

Clone runs: sandbox clone at `/fast/scratch/hyaku/mori-r35/MineAppendOnly/clone`, commits built on dd76eb79 by `supersede.py`;
each inserted row's `teaches` opens `supersedes SNNN —` and its source cell says "sandbox clone only, no source opened".
- Run 4 — `e841b33f`, supersede rows for S182 and S193 only, **exit 1**: 15 ids `[S041,S044,S051,S062,S064,S179,S180,S181,S183,S184,S185,S186,S188,S189,S190]`; S182 discharged `by=S199`, S193 `by=S200` — per id, not blanket.
- Run 5 — `b5cb8ccc`, supersede rows for all 17, **exit 0**: `rows=215 commits=47`, `appendonly_violations=0 ids=[]`, 18 `SUPERSEDED` lines (17 plus S069 by S073, already superseded).
- Run 6 — `1c5e56e1`, on top of Run 5: S191 status `mined`→`queued`, recheck `on-release`→`90d`, used-by→`—`, **exit 0**: `appendonly_violations=0 ids=[]` — allowed columns are excluded.
- Run 7 — `d677b378`, on top of Run 6: S191 anchor `221-246`→`221-247`, **exit 1**: `CHANGED id=S191 origin=8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 changed_at=d677b378c5cb55bff1e998716721337cd4f1c41c cols=anchor`, `appendonly_violations=1 ids=[S191]` — an immutable-cell edit on a non-superseded row is caught.

## Flagged ids at dd76eb79 (none is superseded there; first seen, changed-at, columns in each line)

VERDICT: S041 defect — teaches at 62db24c0; first seen 273aa74a; cross-round edit.
VERDICT: S044 defect — teaches at 62db24c0; first seen 273aa74a; cross-round edit.
VERDICT: S051 defect — teaches at 62db24c0; first seen daceeec8; cross-round edit.
VERDICT: S062 defect — teaches at 62db24c0 and ab8f4cfe; first seen daceeec8; cross-round.
VERDICT: S064 defect — scope,teaches at 62db24c0 and ab8f4cfe; first seen 367927c5; cross-round.
VERDICT: S179 defect — scope,teaches at 5126891f; first seen 55c3ed5e; same-round (round 32).
VERDICT: S180 defect — anchor,teaches at ab8f4cfe; first seen 62db24c0; same-round (round 33).
VERDICT: S181 defect — source,scope,anchor at ab8f4cfe; first seen 62db24c0; same-round.
VERDICT: S182 defect — anchor at ab8f4cfe then 8d56809a; first seen 62db24c0; round 34 in-place edit.
VERDICT: S183 defect — anchor,teaches at ab8f4cfe; first seen 62db24c0; same-round.
VERDICT: S184 defect — anchor at ab8f4cfe; first seen 62db24c0; same-round.
VERDICT: S185 defect — anchor,teaches at ab8f4cfe; first seen 62db24c0; same-round.
VERDICT: S186 defect — scope,anchor,teaches at ab8f4cfe; first seen 62db24c0; same-round.
VERDICT: S188 defect — scope,anchor,teaches at ab8f4cfe; first seen 62db24c0; same-round.
VERDICT: S189 defect — anchor at ab8f4cfe; first seen 62db24c0; same-round.
VERDICT: S190 defect — scope,anchor,teaches at ab8f4cfe; first seen 62db24c0; same-round.
VERDICT: S193 defect — anchor,teaches at 406d91a4; first seen 8d56809a; round 34 in-place edit.

Same-round rewrites are defects by the lane's precedent: the round-34 spot check judged S193's same-round rescope a form defect
(`corpus/lessons/round-34-verifier-spotcheck.md:118`). Every difference is verified cell text (`--show-cells` dump:
`/fast/scratch/hyaku/mori-r35/MineAppendOnly/cells-dd76eb79.txt`). S182's round-34 delta is `485-486,512-518,620-623 (__add_disk …)`
added at 8d56809a; S193's is `4653-4657` plus the requalified teaches at 406d91a4. Neither is superseded at dd76eb79.
VERDICT: holds — round 34 edited S182 (8d56809a) and S193 (406d91a4) in place; `round-34.md:46` is literally true for status
and recheck but reads as a denial of any row change, and 15 ids were already edited in place before round 34.
## Limits (measured, not inferred)

- Discharge is blanket per id: later edits to an already superseded row are also discharged; comparing `changed_at` to the supersede row's first-seen commit would tighten it (not implemented).
- Only ids present at `<rev>` are checked; a row deleted after an in-place edit is not reported. Text-only: it reads
  `^supersedes S\d{3}` from `teaches` and never verifies the supersede row's own cells.
- Column mapping assumes 11 cells and no escaped `|`; every `| S` row at all four lane revs measured has exactly 11 cells
  (198/198 at dd76eb79 and 3a7a89ea, 190/190 at f10a320d), else the script exits 2.
- Detection only: the 17 in-place edits are reported, not repaired. Runtime ≈0.15 s per run; no installs; writes only under
  `/fast/scratch/hyaku/mori-r35/MineAppendOnly/` and this report. An uncommitted lane `corpus/SOURCES.md` change (+6 lines, mtime
  06:00:06 -0300, not mine) appeared during my runs; every run reads committed git objects, so results are unaffected.
