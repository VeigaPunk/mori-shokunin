# ExecIndexClean — round-36 wave 2 (falsify + verify, attempt 2)

- Seat: `mori-r36-w2-ExecIndexClean-11`, executor (leaf; no subagents dispatched). Date: 2026-10-23.
- Item attacked: **the index-clean gate's live check** — `bash tools/mori-index-clean.sh <lane>` must print
  `staged=0 intent_to_add=0` and exit 0, and `git status --porcelain --untracked-files=no` must be empty at the
  landed tip. Any tracked dirty file is a FAIL by the seat's own criterion.
- Method: read-only git/bash against the lane repo. No lane file was edited except this report; no `git add/
  commit/push/fetch/reset`, no mutating jj command; no pacman; nothing installed. Scratch only under
  `/fast/scratch/hyaku/mori-r36/ExecIndexClean/`.
- Environment measured: `git version 2.56.0`; `GNU bash, version 5.3.20(1)-release`; `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` (read-only, `--ignore-working-copy`).

## 1. The two required outputs, at the tip

**Gate** — `cd /home/vgpnk/Projects/shokunin/mori-shokunin && bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin`:

```
$ bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin
MORI_INDEX_CLEAN staged=0 intent_to_add=0
EXIT=0
```

**Status** — `git status --porcelain --untracked-files=no`:

```
$ git status --porcelain --untracked-files=no
$ echo $?
0
```

Empty output, exit 0 — **no tracked dirty file at the tip**.

Tip identity at that moment (`git rev-parse HEAD`): `6827d6e322e87a0b5857bdd25ceb45970732fcd1`
("round-36: close-out — critic corrections (contract history, novelty bound, disposition wording), post-land
check records", 2026-10-23T16:00:47-03:00). `git rev-parse origin/master` → the same hash: **the tip is pushed**.
Stability: two samples 30 s apart (19:02:19Z and 19:02:49Z) show the same HEAD and an empty status both times.

Independent corroboration of the same fact (not the tool's own counting):

```
$ git diff --cached --name-only | wc -l                → 0
$ git status --porcelain=v2 --untracked-files=no | grep -c '^1 \.A '   → 0   (intent-to-add, v2 records)
$ git status --porcelain --untracked-files=no | grep -c '^ A'         → 0   (intent-to-add, v1 records)
$ git ls-files --debug | grep -c 'flags: 20004000'                   → 0   (CE_INTENT_TO_ADD flag)
$ git ls-files -u | wc -l                                             → 0   (unmerged entries)
$ git ls-files -v | grep -vc '^H '                                    → 0   (no skip-worktree/assume-unchanged)
$ git ls-files | wc -l                                               → 10303
$ git ls-tree -r --name-only HEAD | wc -l                             → 10303  (index == HEAD tree)
```

No staged path, no intent-to-add entry, no unmerged entry, no hidden index flag, and the index holds exactly the
tip's tree.

## 2. The lane was in flux during this check — the tip moved twice

This is the substantive operational fact of my seat and it bounds every other wave-2 measurement.

Measured tips during my run (`git rev-parse HEAD` / `git log --oneline`):

| time (UTC) | HEAD | what happened |
|---|---|---|
| 18:33–18:58 | `bf0df77fee4b6ef54a90aea09335c7617f125151` | the tip named in my assignment (data commit) |
| 18:59 | `9ca8f2eb4f48e5c73659d5ed536866786b7708ba` | integration commit (receipts, freeze-v3, w2 evidence, documentary repairs) |
| 19:00 | `6827d6e322e87a0b5857bdd25ceb45970732fcd1` | close-out commit (critic corrections, post-land check records) |

**Tracked dirty files observed during the window** (each is an L1/concurrent-seat integration edit that later
landed as a commit; none was mine; none is an index write):

```
18:45Z  M .ufo/waves/round-36/dispatch-log.txt
18:45Z  M corpus/README.md
18:49Z  M .ufo/waves/round-36/contract.md
18:49Z  M corpus/knowledge/source-drift-r36.md
18:54Z  M SKILL.md
18:54Z  M corpus/QUALITY.md
18:54Z  M corpus/SOURCES.md
18:58Z  M SCORECARD.md
```

Every one was a worktree modification (`.M` — index side unmodified, per porcelain v2 `1 .M N...`), never staged and
never intent-to-add; all were committed by `9ca8f2e` / `6827d6e` and the tree is clean at the tip. The gate stayed
green (`staged=0 intent_to_add=0`, exit 0) through every one of those moments — it correctly does not count
unstaged worktree edits.

**Risk this creates for the round (measured, not inferred).** While `corpus/SOURCES.md` was dirty (S205's
`used-by` cell being changed from `tools/mori-source-drift.py` to `corpus/knowledge/source-drift-r36.md`,
`git diff --numstat` = `1 1`, hunk `@@ -211 +211 @@`), the frozen C1 counter's real-arm precondition was broken:

```
$ git diff --quiet bf0df77fee4b6ef54a90aea09335c7617f125151 -- corpus ; echo $?
1        # count-c1.py:575-580 requires corpus/ == rev, else "real=unmet worktree_corpus_differs_from_rev"
```

So any `count-c1.py` run started while a concurrent seat had `corpus/` dirty returns `C1=unmet` for a reason
unrelated to the probe. **This is now resolved** — at the tip `git diff --quiet <tip> -- corpus` exits 0 and
`git ls-files --others --exclude-standard -- corpus/ | wc -l` is 0, so the precondition holds. Sibling seats
(ExecReC1A, ExecDriftLive) hit the same window; the fix is to re-run the counters only on a clean tree.

## 3. Gate semantics — measured behaviour, and the one deliberate narrowing

Probes run in fresh sandbox repos under `/fast/scratch/hyaku/mori-r36/ExecIndexClean/`
(`git init`, one commit, then the named mutation):

| case | gate output | exit |
|---|---|---|
| A clean repo | `MORI_INDEX_CLEAN staged=0 intent_to_add=0` | 0 |
| B `git add -N c.txt` (intent-to-add only) | `staged=0 intent_to_add=1` + `MORI_INDEX_CLEAN_PATH c.txt` | 1 |
| C unstaged edit to a tracked file only | `staged=0 intent_to_add=0` | 0 |
| D `git rm --cached a.txt` (staged deletion) | `staged=1 intent_to_add=0` + `MORI_INDEX_CLEAN_PATH a.txt` | 1 |
| E nonexistent repo path | `MORI_INDEX_CLEAN_ERROR not a directory: /nonexistent-repo` | 2 |
| F `--selftest` | `MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0` | 0 |

**The round-35 M4 blind spot is closed.** Reproducing the exact mistake — `git add -N .` over 30 untracked files —
gives `staged=0 intent_to_add=30`, 20 `MORI_INDEX_CLEAN_PATH` lines, `MORI_INDEX_CLEAN_MORE 10`, exit 1. In the
same sandbox `git diff --cached --name-only | wc -l` → **0**: a checker built on the cached diff alone would have
called this clean. The gate uses the porcelain records and sees it.

**Read-only, proven.** In a sandbox repo the lane tool left `.git/index` byte-identical (sha256 unchanged, same
inode, same mtime). In the lane the index content sha256 was stable at `96f905a2f505121d791fee3dfe288243e7cc57a75489fcfb7b64b338c7bb3ad6` across all my gate runs, changing only when the L1's own commits landed. Side note measured separately: a plain `git status` (no `--no-optional-locks`) rewrites `.git/index` with **identical content bytes** but a new inode/mtime (stat-cache refresh) — the gate's `--no-optional-locks` + `GIT_OPTIONAL_LOCKS=0` correctly avoids even that.

**One deliberate narrowing vs the wave-1 build spec — observation, not a defect.** The wave-1 build task
(`.ufo/waves/round-36/w1-spec.json`, seat `BuildIndexCheck`) specified: *"exits 0 iff `git -C <repo> status
--porcelain --untracked-files=no` is empty AND `git -C <repo> diff --cached --name-only` is empty AND no
intent-to-add entry exists"*. The builder implemented exactly that and raised the semantic question in
`w1/BuildIndexCheck.md` §6 ("the ambiguity is in the condition, not in the implementation"). The L1 then narrowed
the landed tool to the index-only condition — `tools/mori-index-clean.sh:119`:

```
119:     if (( staged_n == 0 && ita_v1 == 0 )); then
120:         return 0
121:     fi
```

and rewrote the header at `tools/mori-index-clean.sh:5-6` ("unstaged worktree edits to tracked files are not index
state and do not count; L1 round 36"). The round's governing documents were updated to match: `corpus/QUALITY.md:822`
("the lane git index holds no staged path and no intent-to-add entry … prints `staged=0 intent_to_add=0`, exit 0")
and the `SKILL.md` registry row ("index clean (r36) | gate | … | 0 `staged=0 intent_to_add=0` · 1 staged or
intent-to-add entries"). The narrowing is documented, deliberate, L1-owned, and propagated consistently — I record
it because it is the reason my seat's second condition (`git status` empty) is not enforced by the gate itself,
and it is the behaviour the L1 chose.

## 4. QUALITY 103's dispatch-log record — one landed commit without a record

QUALITY 103 (`corpus/QUALITY.md:822-823`) requires: *"After every lane helper commit, the lane git index holds no
staged path and no intent-to-add entry, and **the round's dispatch log records the check after each `landed` line**."*

At the tip, `git show HEAD:.ufo/waves/round-36/dispatch-log.txt` contains 4 `landed` mentions and 2 index-clean
records:

```
30: 15:4xZ  data commit landed bf0df77fee4b6ef54a90aea09335c7617f125151 (helper push verified)
35:         round append-only gate: round_changed=[] exit 0; index clean staged=0 intent_to_add=0
43: 17:3xZ  integration commit landed 9ca8f2eb4f48e5c73659d5ed536866786b7708ba (helper push verified);
44:         post-land checks: index clean staged=0 intent_to_add=0 exit 0 (QUALITY 103);
47: 17:4xZ  close-out: w2 critic corrections (contract :4-5 history, README/novelty + disposition wording,
48:         note novelty bound); wave-2 outstanding seats still landing in w2/ … final receipts + census end next
```

The close-out commit `6827d6e` (2026-10-23T16:00:47-03:00, pushed) has **no `landed` line and no post-land
index-clean record** in the dispatch log at the tip — structurally, a commit cannot contain its own landing
record, so this can only be closed by a subsequent commit. The log itself says more is coming ("final receipts +
census end next"). **Risk, not a defect:** if the round closes at `6827d6e` with no further commit, QUALITY 103's
per-landed-line recording is unmet for the close-out commit. For the two commits whose records do exist, the
recorded check is true: I re-ran the gate at those tips and it printed `staged=0 intent_to_add=0` exit 0.

## 5. Cross-checks against the claims this gate is recorded beside (measured at the final tip)

```
$ python3 tools/mori-sources-appendonly.py 6827d6e322e87a0b5857bdd25ceb45970732fcd1 --round-base 6bd57097
appendonly_violations=18 ids=[S041,…,S193] deleted=[] superseded=[…18 ids…] round_changed=[]
EXIT=0
```

Round-append-only gate green at the final tip as well (`round_changed=[]`, exit 0) — the 18 in-place-edited ids
remain discharged by S205–S220.

Freeze-v3 pin record at the tip (`evidence/freeze-v3.txt`) vs the tip blobs:

| artifact | freeze-v3 pin | tip blob | match |
|---|---|---|---|
| `contract.md` | `f68a06c2329e878e468d49031ac04560c5b70485` | `f505594b292c93bcd86cc5918b7016b1c55ed8ff` | **NO — stale** |
| `count-c1.py` | `b5888afe0c494c45e3a8abe06e6e60e849c101f0` | `b5888afe0c494c45e3a8abe06e6e60e849c101f0` | yes |
| `count-c2.py` | `d8c41d96616eb7caed5ad12cf4e8a2b93c2237dc` | `d8c41d96616eb7caed5ad12cf4e8a2b93c2237dc` | yes |
| `tools/mori-index-clean.sh` | `d171da39f667ed5d3af6f2b76f0481a7f0c3a8a4` | `d171da39f667ed5d3af6f2b76f0481a7f0c3a8a4` | yes |

The `contract.md` pin went stale **after** freeze-v3 was written: the close-out commit `6827d6e` edited
`contract.md` (`git diff 9ca8f2e 6827d6e -- .ufo/waves/round-36/contract.md`, hunk `@@ -1,10 +1,11 @@`, 5
insertions / 4 deletions) and freeze-v3 was not re-issued. The edit is confined to the preamble/history sentence
(round-36's anti-loop ruling) and **does not touch the frozen predicate bytes** — verified byte-identical:

```
P-C1 identical between 9ca8f2e and 6827d6e:  diff <(git show 9ca8f2e:…contract.md | grep '^P-C1:') <(git show HEAD:…contract.md | grep '^P-C1:')  → no output
P-C2 identical between 9ca8f2e and 6827d6e:  (same, '^P-C2:')                                                                                                              → no output
```

and the committed receipts' label lines still equal the predicates verbatim at the tip (sha256 of the receipt's
first line vs the contract's predicate line): P-C2 `5bfa852ce057fab1ca4d5c376f8cc65c7abe1babbbffc725898a6914a8998b11` on
both sides; P-C1 `304a3d0afb5682e12e4c2d8c3be7ba7e01eddcf2d838de290d52dd5cba771c2a` on both sides. This is the
same *class* of pin staleness RevFreezeIntegrity recorded against freeze-v2 (F1), now re-occurring one commit
later against freeze-v3. It is **outside my item** (I attack the index-clean gate) and I did not touch it; it is
recorded because the pin chain is load-bearing for the claims the gate is recorded beside. Remediation is out of
my lane.

Also measured: the two data receipts the round cites are **committed at the tip** (this was an open item when I
started — they were untracked `??` at `bf0df77`):

```
$ git ls-tree -r --name-only HEAD -- .ufo/waves/round-36/evidence | grep -E 'c[12]-after|freeze-v3'
.ufo/waves/round-36/evidence/c1-after.txt
.ufo/waves/round-36/evidence/c2-after.txt
.ufo/waves/round-36/evidence/freeze-v3.txt
$ git show HEAD:.ufo/waves/round-36/evidence/c2-after.txt | tail -3
  tool exit=1
C2=met
seed=15440749816798970567
$ git show HEAD:.ufo/waves/round-36/evidence/c1-after.txt | tail -3
C1=met
seed=7388485190103051243
C1_EXIT=0
```

## 6. Risks and blockers

- **Risk (measured, now resolved):** the lane tip moved twice during this wave's execution (`bf0df77` →
  `9ca8f2e` → `6827d6e`). Any wave-2 measurement that states "at the landed tip <hash>" is only valid for the
  hash it names; re-verification against the final tip is required before the round closes. The data receipts are
  scored at `bf0df77` and committed later — `evidence/freeze-v3.txt` states this explicitly ("scored at clean tip
  bf0df77, committed here"), and the dispatch log records a `C2=met` re-score at the integration tip with seed
  `14475316978074684109` (`dispatch-log.txt:45-46`), distinct from the receipt's seed `15440749816798970567`.
- **Risk (measured, outside my item):** `evidence/freeze-v3.txt` pins `contract.md` to a blob that the final tip
  no longer has (`f68a06c2…` pinned vs `f505594b…` at the tip). Predicate bytes are unaffected; the pin is stale.
- **Risk (structural):** QUALITY 103's "record the check after each `landed` line" cannot be satisfied by the
  final commit itself; the close-out commit `6827d6e` currently has no landing/index-clean record.
- **No blocker** for this item. Gate green, index provably clean, tip pushed and stable.
- **Tooling:** nothing installed or updated; no pacman, uv, npm or cargo transaction. `git`, `bash`, `jj` were
  already present.
- **Lane hygiene:** read-only throughout. No `git add/commit/push/fetch/reset`, no mutating jj command, no lane
  file edited except this report. The only lane-adjacent writes were sandbox repos under
  `/fast/scratch/hyaku/mori-r36/ExecIndexClean/` and short-lived `/tmp` files (moved into that scratch root and
  removed).

## 6a. Post-report observation — the lane went dirty again after my final clean snapshot

Immediately after I wrote this report (16:09 local), a further set of concurrent L1 edits appeared — so the clean
status reported in §1 was a true reading at 19:01–19:02Z, not a durable end state:

```
$ git rev-parse HEAD            → 6827d6e322e87a0b5857bdd25ceb45970732fcd1   (unchanged)
$ git status --porcelain --untracked-files=no
 M .ufo/waves/round-36/dispatch-log.txt     (2 insertions)
 M corpus/SOURCES.md                        (12 insertions / 12 deletions)
 M corpus/lessons/round-36.md               (27 insertions / 2 deletions)
$ bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin
MORI_INDEX_CLEAN staged=0 intent_to_add=0
EXIT=0
```

HEAD is still `6827d6e`; these are worktree edits only (index side unmodified), and the gate stays green. Note
`corpus/SOURCES.md` is dirty again — 12 insertions / 12 deletions, larger than the earlier 1-line edit — so the
frozen C1 counter's real-arm precondition (`git diff --quiet <rev> -- corpus`) is broken again at this instant,
and any counter re-run must wait for that file to settle. My own report file is the only file I wrote
(`git status --porcelain -- .ufo/waves/round-36/w2/ExecIndexClean.md` → `?? …`, i.e. untracked and unstaged).

**Consequence for the L1:** the "tree clean at the tip" property is only true in a quiescent window. The round
cannot be considered closed until a final post-edit gate run is recorded after the last lane write.

## 7. What this item attacks

The round-36 index-clean gate's live check at the landed tip — the routed round-35 repair for lesson M4
(`git add -N .` in the lane): does `tools/mori-index-clean.sh` report the lane index clean and exit 0, is
`git status --porcelain --untracked-files=no` empty at the tip, does the gate actually catch the M4 mistake the
round-35 blind spot would have missed, and is the gate itself read-only.

VERDICT: PASS — at the final tip `6827d6e322e87a0b5857bdd25ceb45970732fcd1` (pushed to `origin/master`) the gate
prints `MORI_INDEX_CLEAN staged=0 intent_to_add=0` and exits 0, and `git status --porcelain --untracked-files=no`
is empty — no tracked dirty file, corroborated independently by `git diff --cached` (0), porcelain v1/v2
intent-to-add counts (0/0), the `CE_INTENT_TO_ADD` index flag (0), unmerged entries (0), hidden index flags (0)
and index-vs-HEAD tree equality (10303 = 10303); the gate is shown able to fail (exit 1) on `git add -N .`,
staged, and staged-deletion cases, is byte-non-mutating, and its selftest is `pass=4 fail=0`. No tracked dirty
file at the tip. Caveats carried for the L1, none of which changes this item's verdict: the lane tip moved twice
during the wave and the tree was transiently dirty (up to 8 tracked files, all L1 integration edits, all landed;
a dirty `corpus/` breaks the frozen C1 counter's real-arm precondition — resolved at the tip); the gate's
exit-0 condition was deliberately narrowed by the L1 to index-only state versus the wave-1 build spec, with
QUALITY 103 and the `SKILL.md` registry row updated to match; QUALITY 103's post-land dispatch-log record is
missing for the final commit; and `evidence/freeze-v3.txt`'s `contract.md` pin is stale against the final tip
(predicate bytes unaffected) — the last two are outside this item and are recorded, not remediated.
