# ReviewRetentionBase — independent retention-gate re-run (R8 no-harm baseline)

Seat: MoriR26.ReviewRetentionBase (leaf; no subagents used). Date: 2026-10-22.
All commands run read-only against the lane at `/home/vgpnk/Projects/shokunin/mori-shokunin`;
outputs under `/fast/scratch/hyaku/mori-r26/ReviewRetentionBase/` (`base.json`, `landed.json`).

## 1. What was run

Both scans with the exact invocation from the contract's no-harm clause, differing only in `--rev`:

```sh
python3 -I -B tools/mori-retention-gate.py scan \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --rev <REV> \
  --policy .ufo/waves/round-18/frozen/c1-policy.json \
  --allowlist corpus/evidence/retention-allowlist.json
```

- `base.json`: `--rev 248408f5b6610a85bcbdebe7ac0b4fa7ed51422a` (entering tip), exit 1.
- `landed.json`: `--rev 28b0494004fe1f064544224eca56dd42605db384` (landed tip), exit 1.

`policy_sha256` in both outputs: `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128`.
`warnings: []`, `forbidden_allowlist: []`, `routed: 0` in both.

## 2. Results (counts only, no hit text)

| Rev | hits | allowlisted | unallowlisted (= metric) | exit |
|---|---|---|---|---|
| 248408f5 (entering) | 109 | 100 | **4** | 1 |
| 28b04940 (landed) | 109 | 100 | **4** | 1 |

The two outputs are identical in every field except `commit` (`hits` and `unallowlisted_hits`
compared equal in Python, including each hit's `line_sha256`). No round-26 work added or removed a
retention finding.

Cross-check vs the L1 receipt `.ufo/waves/round-26/evidence/retention-scan-base.txt`
("unallowlisted_hits: 4 (metric 4); hits 109; allowlisted 100", exit 1): **matches my base re-run
exactly** on all four numbers.

### The 4 unallowlisted hits (paths and classes, counts only)

All four sit in one file, one hit per class:

- Path (all 4): `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`
- Classes: R2 ×1 (line 8), R5 ×1 (line 11), R6 ×1 (line 12), R8 ×1 (line 14)

These are pre-existing at the entering tip (the L1's own R8 receipt shows the same 4), so they are
round-25-inherited state, not round-26 regressions.

### No-harm verdict at the landed tip

Contract: "its value at the landed tip must not exceed the entering value" (contract.md, Held-not-
claimed section). Landed metric 4 == entering metric 4 → **no-harm holds** at 28b04940.

## 3. Does the tool scan only commits? — Yes

Evidence in `tools/mori-retention-gate.py`:

- `scan()` resolves the scanned content exclusively through
  `_scan_git_revision(args.repo, args.rev, classes)` (line 314).
- `_scan_git_revision` (line 177) feeds `<rev>^{commit}` to
  `git cat-file --batch-check=%(objectname) %(objecttype)` (lines 183-184) and rejects anything that
  does not peel to a commit object (`revision_not_commit`, line 187). A blob/tree/index path or a
  dirty worktree state cannot be passed.
- Content is then read only from that commit's tree: `git ls-tree -r -z --full-tree` + per-blob
  `git cat-file blob` (lines 189-201). There is no index or worktree scanning mode in `scan`.
  (The separate `--frozen-run` mode reads pinned snapshot files, not a candidate; `--expect-population`
  only compares against a pre-recorded population that itself pins a commit, lines 213-237.)

So an uncommitted candidate (dirty worktree, or staged files with no commit) **cannot** be scanned
by `--rev` as-is. Two structural facts make the temp-clone method clean:

- `--policy` and `--allowlist` are read as ordinary filesystem paths relative to the process CWD
  (`read_json`, lines 49-55; `scan()`, lines 311, 317-319) — independent of `--repo`.
- Scanned bytes come only from the repo given by `--repo`.

## 4. How the L1 should scan an uncommitted candidate before each commit

Recommended: temporary clone in scratch, never touching lane refs, index, ODB, or jj state. The lane
is git/jj colocated (`.git` and `.jj` both present), so the copy excludes both.

```sh
# Run from the lane root; write nothing into the lane.
lane=/home/vgpnk/Projects/shokunin/mori-shokunin
cand=/fast/scratch/hyaku/mori-r26/MoriR26/cand-$(date +%s)
mkdir -p "$cand"
rsync -a --exclude .git --exclude .jj "$lane/" "$cand/worktree/"
git -C "$cand/worktree" init -q
git -C "$cand/worktree" add -A                       # respects the lane's .gitignore
tree=$(git -C "$cand/worktree" write-tree)
commit=$(git -C "$cand/worktree" commit-tree "$tree" -m retention-candidate)
python3 -I -B tools/mori-retention-gate.py scan \
  --repo "$cand/worktree" --rev "$commit" \
  --policy .ufo/waves/round-18/frozen/c1-policy.json \
  --allowlist corpus/evidence/retention-allowlist.json
```

Why this is correct:

- `git init`/`add`/`write-tree`/`commit-tree` run **in the scratch clone only**; the lane's
  "no git add/commit/stash/…" bound is untouched (nothing is written anywhere under `$lane`).
- `--policy`/`--allowlist` stay CWD-relative, so the clone is scanned against the same frozen policy
  bytes (same `policy_sha256` `db06e981…`) and the same frozen allowlist as the committed-tip runs.
- `commit-tree` needs no `user.name`/`user.email` configuration.
- Interpretation: `metric`/`unallowlisted_hits` from this run is the value the commit would produce;
  it must not exceed the entering value 4 (contract.md, no-harm clause).

Caveats:

- Untracked-but-not-ignored files in the worktree are included by `add -A` (jj would snapshot them
  too), so scratch junk inflates the scan. That errs in the safe direction for no-harm; clean scratch
  files first if you want the exact committed population.
- Do NOT use `git stash create` or `git commit-tree` inside the lane to materialize a candidate:
  both write objects into the lane's ODB, which seats must not mutate.
- Alternative (only if the candidate is already a jj working-copy snapshot): the colocated repo's
  git ODB already holds that commit, and a read-only `jj` query with `--ignore-working-copy` can
  yield its git sha for `--rev`. Any jj command that snapshots or mutates state is out of bounds.

## 5. Tooling directive record

No tools installed or upgraded; stock `python3`, `git`, `rsync` sufficed.

## 6. Residual risk and verification gaps

- `hits: 109` at both tips includes allowlisted context in `.ufo/` history files; I verified counts,
  fingerprints, and the four unallowlisted entries, not the semantic correctness of every allowlisted
  row (out of scope for a re-run).
- The 4 unallowlisted hits live under a round-20 falsify fixture path; whether they should gain
  allowlist rows is an integration decision for the L1, not a defect I assert.
- My temp-clone procedure is reasoned from the tool source cited above but was exercised only in its
  committed-rev form (the two scans); I did not run the clone flow end-to-end on a dirty worktree,
  since the lane worktree is not mine to reproduce and no candidate was pending at scan time.
  [INFERENCE] on the clone flow's exact numbers, not on the commit-only claim, which is source-verified.
