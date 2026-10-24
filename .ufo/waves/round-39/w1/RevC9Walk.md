# RevC9Walk — C9 lane-walk receipt verification (round 39, wave 1)

Target: `.ufo/waves/round-39/evidence/c9-after-lane.txt` at scored tip `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`.

**Verdict: FAIL on the receipt's absolute counts (F1); PASS on the `6531ac60` differential, the
`%P` parent-carrying log call, and the lane-line byte parity.**

No lane file was modified. All git reads are read-only; scratch is
`.ufo/waves/round-39/scratch/RevC9Walk/`.

---

## F1 — MEDIUM — receipt counts do not reproduce at the scored tip

`c9-after-lane.txt:4-5` state `v2 walk commits (full-history): 53` and
`v1 walk commits (default simplification): 52`. At the scored tip the counts are **54** and **53**:

```
$ git log --full-history --oneline 13bfba23b7 -- corpus/SOURCES.md | wc -l
54
$ git log --oneline 13bfba23b7 -- corpus/SOURCES.md | wc -l
53
$ git rev-list --count --full-history 13bfba23b7 -- corpus/SOURCES.md
54
$ git rev-list --count 13bfba23b7 -- corpus/SOURCES.md
53
```

Off by exactly one commit in both columns. The delta is `f920eaf7` "round-39: data — S227
gitrevisions + S228 (supersedes S226, corrected quote) …" — a **linear** commit, the round's own
`corpus/SOURCES.md` data commit, not a simplification artifact:

```
$ diff <(git log --full-history --format='%H %P %s' 13f3db7e -- corpus/SOURCES.md) \
       <(git log --full-history --format='%H %P %s' 13bfba2 -- corpus/SOURCES.md)
0a1
> f920eaf7… 87ec3d99… round-39: data — S227 gitrevisions + S228 …
```

### Provenance of the printed pair

Every number on lines 4-6 reproduces exactly on the **inherited lane**, before the round wrote its
own data row:

| rev | full-history | default | `6531ac60` full | `6531ac60` default |
|---|---|---|---|---|
| `13bfba2` (scored tip) | 54 | 53 | 1 | 0 |
| `f920eaf7` | 54 | 53 | 1 | 0 |
| `f920eaf7^` = `87ec3d99` | **53** | **52** | **1** | **0** |
| `13f3db7e` (entering tip) | **53** | **52** | **1** | **0** |

So lines 4-6 are the inherited-lane baseline, presented without a rev; line 1 names `f920eaf7` only
as a byte anchor. Alternative readings are excluded by measurement: `--first-parent` gives 53/53,
`--simplify-merges` 53, `--no-merges` 53/53, `--ancestry-path` 0 — none yields 53/52, and all would
also have to produce `6531ac60 present: v2=1 v1=0`, which only the full-history/default pair at the
inherited tip does.

The v1 column is genuine, not fabricated: the r38 gate walk at `b6993744` is
`git log --format=%H --reverse <rev> -- <path>` (`git show b6993744:tools/mori-sources-appendonly.py`
lines 220-221), and that command on the inherited tip counts 52.

### Propagation (same stale pair)

- `corpus/knowledge/gate-ancestry-r39.md:32` — "(`6531ac60` appears only under `--full-history`, 53 vs 52 commits)"
- `SCORECARD.md:2200` — "drops `6531ac60` (53 vs 52 commits)"

The *difference* of one commit is correct at every rev; the absolute numbers are one round behind.

### Impact

Evidence-only. `report()` prints no commit count (`tools/mori-sources-appendonly.py:389-406`), so no
gate behavior depends on these numbers. The defect is reproducibility of a cited number, not logic.

---

## P1 — PASS — `6531ac60` appears only with `--full-history`

At the scored tip, `6531ac60` is present 1× under `--full-history` and 0× under default
simplification, and the set difference of the two walks is exactly that commit:

```
$ comm -13 <(default list) <(full list)
6531ac6029e200a6392bb76673b6a17d3c895c96
$ comm -23 <(default list) <(full list)
(empty)
```

Mechanism verified: `6531ac60` is a merge with parents `bf7cdc4` + `b2e1ca2`; its
`corpus/SOURCES.md` blob is byte-identical to the first parent's (`git diff --quiet 6531ac60^1
6531ac60 -- corpus/SOURCES.md` → TREESAME-first-parent), and the second parent does not carry the
path (`git cat-file -e 6531ac60^2:corpus/SOURCES.md` → absent). TREESAME to the first parent is
exactly what default simplification elides, so the receipt's parenthetical "history simplification
was dropping a commit on the lane" is accurate.

---

## P2 — PASS — the gate's log call carries `%P` parents

`tools/mori-sources-appendonly.py` at the scored tip:

```
263:    for line in git(repo, "log", "--format=%H%x09%P", "--reverse",
264:                    "--full-history", rev_full, "--", path).splitlines():
```

Parents are parsed at 265-267 and actually consumed, not decorative:

```
304:        for parent in parents_of.get(commit, []):
306:                nearest_path_commit(repo, parent, path)
311:                ref = states[pidx]
318:        is_merge = len(parents_of.get(commit, [])) > 1
```

Byte identity of the source under test: sha256 of the blob at the scored tip is
`62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7`, equal to
`freeze-r39.txt:14`, to the blob at `f920eaf7` (the receipt's byte anchor), and to the worktree file
`tools/mori-sources-appendonly.py` on disk. So the reviewed semantics are the pinned ones, not a
worktree drift.

---

## P3 — PASS (adjacent) — lane-history lines are byte-identical

The v2 gate body at the scored tip with `--round-base f10a320d` is byte-identical to the body of
`.ufo/waves/round-38/evidence/gate-after.txt`; at `e37dcc6` it is byte-identical to
`gate-after-e37dcc6.txt`, including `stale_supersede=[S069]`. At the tip the summary is
`supersede_timing superseded_as_of=[…18 ids…] stale_supersede=[]`, matching P-C9's "no id is stale at
the round-39 tip".

One wording caution: the receipt's `identical, exit 0` is `diff`'s exit status, not the gate's. Both
the r38 receipts and v2 at `e37dcc6` and at the tip print `EXIT=1` (`appendonly_violations=18`).

---

## Residual risk

1. **Count drift recurs by construction.** Lines 4-6 name no rev, so every future round's own
   `SOURCES.md` data commit will invalidate them again; the same failure already reached knowledge and
   scorecard (F1 propagation). The qualitative claim (+1 commit, merge dropped) is stable; only the
   absolutes are not.
2. **Merge path unexercised by me.** I confirmed the `is_merge` guard exists (`:318`) and that the
   lane merge is TREESAME-first-parent, but I did not run the committed fixture C/D DAGs that prove
   no fabricated edit across a merge — that is other seats' evidence.
3. **Peer data, not verified here.** `mori-r39.CritC9Semantics` reported by IRC a counterexample
   where `nearest_path_commit` resolves to a deletion commit and the walk then falls through to the
   second parent, making the contract's first-parent-state clause stronger than the code. I did see
   the fall-through loop at `:304-312` (`if pidx is not None and states[pidx] is not None`), but I did
   not build or verify that counterexample; it is recorded as received data outside this ticket.

## Verification gaps

- **No `lsp` device in this seat's tool inventory** (read/bash/edit/eval/glob/grep/task/wait/
  web_search/write only), so `references`/`definition`/`diagnostics` were unavailable. Caller and
  definition checks were done from committed blobs (`git show 13bfba2:tools/…`), which is the literal
  fallback; this is recorded as unavailability, not as a passed semantic check.
- I did not run `--selftest`, the C7 counter, `conform.py`, or any mutation fixture.
- Counts were re-confirmed at `HEAD` `20260b0c` (a descendant of the scored tip): `git diff --stat
  13bfba2 HEAD -- tools/mori-sources-appendonly.py corpus/SOURCES.md` is empty, so 54/53 holds there
  too.

## Tooling

No installs or upgrades were performed.
