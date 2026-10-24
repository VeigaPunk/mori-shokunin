# MutCountC1Amended — mutation test of the A1-amended C1 counter

**Verdict: holds** for the six assigned mutants — every one reads `C1=unmet` — but the counter has **three
survivors in adjacent defect classes** (M7, M8, M9), each with a verified smallest fix. A fourth (M10) is
contract-consistent, not a defect.

Attack target: `count-c1.sh` blob `8682687f55f48bc32b4fe1d5e8c19424c1faddbf`
(sha256 `0d7a1be0cbe6ad90296ea911d7441ef0dc6ee9454f76259bf8a40a1369f67980`), identical at the pinned
revision `f2de0eedcd60d2e354da75265ea6122bc3896073` and at the landed tip `1fc6bb0e…` (unchanged by wave 2).
Sandbox: `/fast/scratch/hyaku/mori-r28-w2/MutCountC1Amended/sandbox2` (`git clone --no-hardlinks`).

## Method

The counter hardcodes `LANE=/home/vgpnk/Projects/shokunin/mori-shokunin` (count-c1.sh:11), so each run used
`unshare --user --map-root-user --mount` with the sandbox bind-mounted over that path. The frozen QUALITY 81
check is taken by the counter from blob `df886be1…` (count-c1.sh:25); that blob is byte-identical in the
sandbox (`dc3ddad006defefa0378f5945f504433cf94c047` both sides). Mutants are **sibling commits** built with
`commit-tree` (temp index), so the sandbox worktree was never mutated: `git status --porcelain` empty and
`HEAD` = `1fc6bb0e…` after every run. The lane was read-only; `git -C <lane> status --porcelain` shows no
tracked modification and the lane tip is still `1fc6bb0e…`.

**Baseline.** At the pinned revision `f2de0eed…` the counter already read `C1=unmet`
(`fail S147 row_absent`, `superseding=7/8`) because S147 did not exist yet — a baseline failure, so it proves
nothing. I therefore anchored every mutant to the **real landed tip** `1fc6bb0e…`, where the counter reads
`C1=met` (exit 0). A mutant is *killed* only when it flips that to `C1=unmet` (exit 1).

## The six assigned mutants — all killed (C1=unmet)

| # | Mutation | Commit | Counter output | Verdict |
|---|---|---|---|---|
| M1 | S145 `teaches` copied from superseded row S096 | `8925531c` | `fail S145 teaches_unchanged` | **killed** |
| M2 | S145 `used-by` → `corpus/README.md` (cites no S145) | `09ba4268` | `fail S145 used_by_not_citing=corpus/README.md` | **killed** |
| M3 | S145 Gate line loses its sha256 | `69430e27` | `fail S145 gate_line` | **killed** |
| M4 | S145 status `rejected` over mined S096 | `038b3033` | `fail S145 status=rejected` | **killed** |
| M5 | live reader re-cites S096 | `e8078dd5` | `readers_left=1` | **killed** |
| M6 | restored row S096 differs in one cell | `3b178e28` | `row_identity=… changed=1` | **killed** |

M1 was also built **born-with-the-copy** (M11 `051b59a8`: S145's first publication already carries S096's
wording, so QUALITY 81 is blind to it) — still `fail S145 teaches_unchanged`, `C1=unmet`. The
`teaches_unchanged` branch is therefore live on its own, not merely shadowed by `changed=1`.

## Survivors (adjacent classes) — smallest fix each

### M7 — a reader line naming tsukuroi escapes `readers_left` (commit `712ebd3d`, reads **met**)

A reader line citing a superseded id *and* mentioning tsukuroi is dropped whole. `count-c1.sh:81` filters
`grep -v -E 'tsukuroi'`, which deletes the entire line, not just the tsukuroi id-enumeration. The contract
excludes "lines naming tsukuroi's own ids" (contract.md A1), not lines that merely mention tsukuroi.
At the landed tip exactly one reader line mentions tsukuroi (`corpus/knowledge/oom-victim-selection-r27.md:204`,
`tsukuroi S115, S118, S120 and S127 are psi.rst`) — it is excluded for the right reason, but the filter is
line-scoped, so a mori id on the same line is lost with it.

**Smallest fix** (one line, count-c1.sh:81) — strip the tsukuroi enumeration, then count what remains:
```sh
left=$(git -C "$LANE" grep -n -w -E "$olds" "$R" -- $READERS 2>/dev/null | sed -E 's/tsukuroi ([^;.]*)//g' | grep -w -E "$olds" | wc -l)
```
Verified with a patched copy: reference still `readers_left=0`/`C1=met` (exit 0); M7 → `readers_left=1`/`C1=unmet`;
M5 still `readers_left=1`/`C1=unmet`. No regression.

### M8 — a rejected row can supersede a row flipped to `rejected` (commit `16452650`, reads **met**)

The contract admits `rejected` only for the 404 case (contract.md A1: "`rejected` when the row it supersedes is
`rejected` (S097 is a 404 page)"). The counter tests the *superseded row's current* status
(count-c1.sh:57-62), so flipping S096 `mined`→`rejected` alongside S145 `rejected` satisfies it — even though
S096 is a restored row whose **first-published** status is `mined` (verified from history:
`git show <first-commit>:corpus/SOURCES.md`). S097 is the only old row legitimately `rejected`
(first-published `rejected`, confirmed).

**Smallest fix**: compare against the superseded row's **first-published** status, not its current one, so the
`rejected` branch is anchored to history. A one-line change at count-c1.sh:57 needs the first-published status
in scope; the counter already reads history for `check-row-identity.py`, so the lookup can reuse that
(`git log --full-history --topo-order --reverse -- corpus/SOURCES.md`, first commit carrying the id).
**Not verified end-to-end** — I did not land a patch for this one; the defect and its cause are shown above.

### M9 — no live reader has to cite the new id (commit `4f50f4ab`, reads **met**)

`used-by` is validated only for "path cites the new id" (count-c1.sh:64-66), and `corpus/lessons/round-28.md`
is a history file that a Gate row makes cite every new id. Setting S145's `used-by` to that lesson alone and
stripping S145 from SKILL.md / PROVINCE.md / the knowledge note leaves **no live reader citing S145** — yet the
counter reads `superseding=8/8`, `readers_left=0`, `C1=met`. This is exactly round-28 lesson M4 ("superseding
rows that no reader cites", lesson round-28.md:47-52) re-entering through the `used-by` cell.

**Smallest fix** (three lines, count-c1.sh:63-64) — require at least one **live** reader path in `used-by` that
cites the new id:
```python
    live = [p for p in paths if p in ("SKILL.md", "PROVINCE.md", "corpus/README.md") or p.startswith("corpus/knowledge/")]
    if not any(exists_with_id(p, new) for p in live):
        fails.append(f"fail {new} no_live_reader_cites_new_id"); continue
```
Verified with a patched copy: reference still `C1=met` (all eight rows have a live citing reader — checked
per row); M9 → `fail S145 no_live_reader_cites_new_id`/`C1=unmet`; M2 still `C1=unmet`; M1/M3/M4/M6 still
`C1=unmet`. No regression.

### M10 — restored row differing in a *mutable* cell (commit `bef498f4`, reads **met**) — not a defect

S096's `status` cell differs from first-published, and the counter reads `met`. This is **contract-consistent**:
CORPUS Rule 2 (cited in the QUALITY 81 docstring) allows in-place change to the `status`, `recheck` and
`used-by` cells only, so QUALITY 81 correctly reports `changed=0`. Recorded for completeness; no fix proposed.

## Restoration evidence

- Sandbox `sandbox2`: `git status --porcelain` empty, `HEAD` = `1fc6bb0eaab40d9ea4fe996b64d140282b76337d`
  after all runs; mutants live only as sibling commits.
- Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`: read-only throughout; `git status --porcelain` shows no
  tracked modification, tip unchanged at `1fc6bb0e…`.
- Pristine blob hashes at the landed tip (unchanged by this seat):
  `corpus/SOURCES.md bae2e85249981dc81d441b3fa1b652da8f6d6435`,
  `corpus/lessons/round-28.md 0d371475813841a1bc471acc938adb347450f6be`,
  `PROVINCE.md 00b3450458ff394173761d13b28b70c0025272de`,
  `SKILL.md de2e5a8f56d8194edd518eeafcaa678f62c75d6a`,
  `.ufo/waves/round-28/count-c1.sh 8682687f55f48bc32b4fe1d5e8c19424c1faddbf`.
- Scratch tree (mine only): `/fast/scratch/hyaku/mori-r28-w2/MutCountC1Amended/` — `build3.py`, `revs2.json`
  (all mutant revs), `run-counter2.sh`, `fixA.sh`, `fixAB.sh`.

## Limits

- M8's fix is reasoned from the counter's own logic and the first-published statuses I read from history; I did
  not land and re-run a patched counter for it, unlike M7 and M9.
- The counter's `row_identity` leg comes from the frozen `df886be1…` check script, so `changed=1` kills a
  mutation of any non-mutable cell; M6 is killed by that leg rather than by the counter's own Python.
- `used-by` path validation uses `git grep -q -w -F` per path (count-c1.sh:43-45); a path that does not exist
  at `<rev>` also fails, which is why M2's `corpus/README.md` (present, but not citing S145) is the sharper case.
- Tooling: no packages installed; `git`, `python3`, `bash`, `unshare` from the host base system. No pacman
  transaction was run (host-wide pacman pause).
