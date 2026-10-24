# HelperFailureWindows — where `jj-lane.sh commit`/`state` can leave HEAD off-branch or a foreign author on it

Seat: MoriR17.HelperFailureWindows-5 (scout, read-only). Date: 2026-10-20.
Scope: `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh` `cmd_commit`, the `do_push` /
`recover_remote_move` / `report_landed` machinery it reaches, and `cmd_state`. Nothing was edited;
no VCS write was run anywhere; no tool installed (jj 0.45.1 and git 2.56.0 pre-existing).

Binding context read: `.ufo/waves/round-17/contract.md` (C2 lines 88-99), `.ufo/waves/round-17/wave1-context.txt`.
Routed evidence read: `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md` (F2, F3, F4).

## 0. Ground facts (observed, read-only)

Live lane `/home/vgpnk/Projects/shokunin/mori-shokunin` (jj-colocated, entering tip 24526ea):

```
$ cat .git/HEAD                       -> ref: refs/heads/master        rc=0
$ git --no-optional-locks symbolic-ref -q HEAD -> refs/heads/master    rc=0   (attached)
$ git --no-optional-locks rev-parse HEAD refs/heads/master
  24526ea9617cd020fee16c28fe4d4a2789dc28cb
  24526ea9617cd020fee16c28fe4d4a2789dc28cb                              rc=0
$ git merge-base --is-ancestor HEAD refs/heads/master                  rc=0
$ jj --ignore-working-copy log -r '@ | @-'
  9008771a7b72 | parents=24526ea9617c | bookmarks= | nonempty
  24526ea9617c | parents=786ebed0efe3 | bookmarks=master | nonempty
$ jj --ignore-working-copy config get 'revset-aliases."trunk()"'        -> master@origin rc=0
$ git config --get lane.branch -> master ; lane.id -> mori              rc=0/0
$ git log -1 --format='%an <%ae>|%cn <%ce>' refs/heads/master
  protocol-shokunin <protocol@shokunin.local>|protocol-shokunin <protocol@shokunin.local>
$ jj --ignore-working-copy config get user.name                         -> mori-shokunin
```

Material invariant used below: **`git rev-parse HEAD` must be reachable from `refs/heads/<branch>`**.
In this repo `HEAD = @-` (the working-copy parent): observed live (HEAD=24526ea=@-, attached because
the bookmark points there), and observed in the routed sandbox immediately after `jj commit`
(JjAuditMori.md F2/F3: `symbolic-ref` rc=1, `HEAD=d19d559` vs `refs/heads/master=611dfb5`).
`jj commit` moves HEAD to the new `@-` while `refs/heads/<branch>` stays put until a later
`jj bookmark set`; the helper performs exactly those two separate steps (604 then 658).
Whether jj re-attaches HEAD (symref) when the bookmark later catches up is **not observed**
[none of HEAD attachment after 658 measured; `inline.sh:33` states colocated lanes are detached].
The material test must therefore use ancestry, not `symbolic-ref`.

`jj bookmark set` refuses backwards/sideways moves without `-B`: jj 0.45.1 binary carries
`Refusing to move bookmark backwards or sideways:` … `Use --allow-backwards to allow it.`
(`strings $(command -v jj)`; `jj bookmark set --help` rc=0 shows `-B, --allow-backwards`).
The helper never passes `-B` (658), so a concurrent forward move **cannot rewind the branch** — it
makes the set fail (window W4) instead.

Consumers (why the windows matter): `inline.sh:37` (`lane_tip` = `state … local`), `inline.sh:119-124`
(verify durability-pushes only when `state` `ahead` ≠ 0, else declares the lane landed), and
`closure-prompt.md:24-26` (closure precondition is `state … ahead=0`). `state` never reports the
commit HEAD points to, so a commit that never reached `refs/heads` is invisible to all three.

Selftest coverage: `jj-lane-selftest.sh:170-174` (case e) asserts only
`merge-base --is-ancestor $CHASH HEAD` and merely *prints* attached/detached; `:493-503` (z12) covers
a seat's stray `jj commit`; grep over all `case_z*` shows **no case that makes the 658
`bookmark set` fail**, and no case that inspects HEAD/branch state after a post-commit refusal.

## 1. `cmd_commit` step inventory (line → action → ref/HEAD effect)

| # | lines | step | writes |
|---|---|---|---|
| 1 | 493-508 | arg parse; `--as`/`-m`/`--` required; `--as` charset | — |
| 2 | 509-512 | `lane_realdir` (real .git dir, fleet root refused, 74-83); `.jj` required; `take_lock` (132-138: per-physical-path flock, 300 s); `cd` | lock file only |
| 3 | 513-517 | branch = jj `trunk()` alias (90-96) → git `lane.branch` (98-103); lane id = jj `user.name` (106-111); `--as` must equal lane id or `protocol` | — |
| 4 | 519-521 | repo `snapshot.auto-track == "none()"` sentinel else exit 1 | — |
| 5 | 523-551 | path canonicalize (`realpath -m`), root/repo-internals/`.ufo` refusals, dir/file/missing split, 10 MiB cap; empty set → `nothing to commit` rc0 (551) | — |
| 6 | 553-554 | `tip = rev-parse refs/heads/<branch>` (read before any jj write) | — |
| 7 | 559-566 | `jj file track --include-ignored` (files) / `jj file track` (dirs) — snapshotting calls | jj wc snapshot; HEAD rewritten to `@-` if it moved |
| 8 | 570-573 | `jj diff --summary -- <filesets>` — snapshots the wc; failure is fatal (never "nothing") | jj wc snapshot / HEAD to `@-` |
| 9 | 575-578 | empty diff → `nothing to commit` rc0 | — |
| 10 | 584-594 | `base=@-`; if `base != tip`: empty `@` → `jj new $tip` (587-589, lane identity); non-empty `@` → refuse rc1 (591-592) | re-anchor moves `@` (and HEAD) onto `$tip` |
| 11 | 598-601 | `jj metaedit --update-author` under per-command `<id>-shokunin` identity | rewrites `@` author (and committer) |
| 12 | 602-605 | `jj commit -m "$msg" -- <filesets>` under the same identity | creates the new commit (`@-`), new empty `@`; **HEAD := new commit**; bookmark unmoved |
| 13 | 606-607 | `hash = @-`; empty → rc1 | — |
| 14 | 612-616 | guard 1: `hash^` must equal `tip` else rc1 | bookmark stays |
| 15 | 620-656 | guard 2: every changed path under the request, never `.ufo/state` (620-629); rename parse (633-645); guard 3: phantom deletion (649-655) — every failure `exit 1` from the main shell | bookmark stays |
| 16 | 658-660 | `jj bookmark set <branch> -r $hash` (write, `--ignore-working-copy`, no `-B`) | `refs/heads/<branch>` := hash (jj export) |
| 17 | 664-667 | warn for named files jj refused to track | — |
| 18 | 669-670 | `do_push branch id hash`; failure → **exit 3**, else exit 0 | remote |

Push machinery reached from 669 (and from `cmd_push` 701):

| lines | step | effect |
|---|---|---|
| 346-348 | `do_push` → `push_preflight` | static gates |
| 198 | lane id re-derived from jj `user.name` (never `lane.id`) | identity source |
| 200-207 | conflicted bookmark / conflicted tip → refuse | — |
| 208-214 | origin ref present; `merge-base --is-ancestor origin/<b> <b>` (no backwards/sideways) | — |
| 218-228 | every commit in `origin/<b>..<b>`: author AND committer ∈ {`<lane>-shokunin`, `protocol-shokunin`} and matching e-mails; **only authorship gate in the helper** | — |
| 349-353 | up to 3 attempts: `jj git push --bookmark <b>`; on success `report_landed` | remote |
| 237-244 | `ls-remote` remote tip must equal local tip | — |
| 246-256 | if this run's `own` was rewritten, re-find it by change id; prints `rewritten <old> -> <new>` + `landed <tip>` | — |
| 354-357 | lease rejection → `recover_remote_move` → re-preflight → retry | — |
| 359-363 | other rejection / 3 strikes → rc1 → caller exit 3 | — |
| 280-342 | recovery: `jj git fetch`; refuse rewritten remote (289-292); conflicted-bookmark path (297-315); normal path (316-339); `rebase -b <tip> -d <b>@origin` under requested identity (302-305 / 324-327); `bookmark set` (307/329) or adopt `b@origin` (337); conflict check (309-312/331-334); `reanchor_wc` (313/340) | rewrites unpushed commits, committer := requested id |

`reanchor_wc` (265-275): only re-anchors an **empty** `@` whose parent ≠ bookmark tip; `jj new "$tip"`
failure is swallowed (`|| true`, 274).

### Exit-code map (observed)

- `0`: 551 (no such paths), 577 (`nothing to commit`), 670 (landed).
- `1`: any refusal before 658, including every post-commit guard failure (607/613/628/643/653) and
  the `bookmark set` failure itself (659); `cmd_state` failures at 168/171/172.
- `3`: 669 (`do_push` failed from `commit`), 694 (`push` preflight), 696 (`push` rejected,
  `--no-rebase`), 697 (`report_landed` failed), 701 (`do_push` from `push`).
- `64`: usage (62, 508).

**The asymmetry that matters:** exit 3 always implies the bookmark was already moved (658), so HEAD
is on the branch; exit 1 *after* 604 implies it was not, yet 1 is documented as generic failure while
3 is the only "commit kept" signal (57-60). Every W1/W4 stranded commit reports through the less
informative code.

## 2. Failure windows — HEAD not reachable from `refs/heads/<branch>`

Ordered by likelihood. "Persists" = still true after the helper has exited.

**W1 — post-`jj commit`, pre-`bookmark set` (604 → 658).** HEAD becomes the new commit (F3),
`refs/heads/<branch>` is still `tip`. Every exit in this interval persists the mismatch:
- 606-607: `hash` unreadable → rc1;
- 612-616: parent-not-tip guard → rc1;
- 623/628/643/653: path / rename-parse / phantom-deletion guards → rc1;
- 658-659 (W4): `bookmark set` fails → rc1.
In every case the commit object exists, is reachable only from `@`'s ancestry, is not on the branch,
and was never pushed. Severity is raised by the **retry trap**:
- rerun with the same paths → 570 sees an empty `@` diff → `nothing to commit` rc0 (575-578);
- rerun with any other path → `base = @- = stranded commit ≠ tip` and `@` non-empty → refuse rc1 (591).
`cmd_push` cannot heal it either: `push_preflight` passes (range empty) and `jj git push` is a no-op
that prints `landed <old tip>`. So the lane is wedged for all future helper commits until a human runs
`jj bookmark set <branch> -r @-`, `jj edit`, or `jj abandon`.

**W2 — off-tip empty `@`, no diff (575-578).** If `@` is empty and sits on a non-tip commit, an empty
diff exits **rc0 `nothing to commit` before the 584 re-anchor check**. This is the W1 retry state: the
helper reports a benign no-op while HEAD is off-branch. Off-tip non-empty `@` is refused correctly
(591), but nothing repairs it.

**W3 — pre-existing off-tip `@` with changes (584-594).** Refusal by design; HEAD was already
off-branch and stays so. No repair, no diagnostic beyond "refusing to sweep or strand work".

**W4 — `bookmark set` failure (658-659).** The only step that moves the branch. Any jj error (op
lock, stale wc, conflicted bookmark, concurrent move) → `err "bookmark set failed"` rc1, with no hash
and no `stranded` line. A concurrent forward bookmark move makes jj refuse (no `-B`, see §0) — safe
from rewinds, but this is precisely the stranded-commit state of W1 with a fully validated commit.
Exit 1 is documented as generic "failure" (57) — unlike exit 3 ("committed but push failed"), nothing
tells the caller a commit now exists.

**W5 — recovery rebase and re-anchor.**
- 309-312 and 331-334: a rebase that produced conflicts returns **before** `reanchor_wc` (313/340).
  The comment at 262-264 states the recovery rebase can leave `@` on the pre-rebase parent, which is
  no longer an ancestor of the rebased branch → HEAD off-branch + exit 3. Persists.
- 274: `reanchor_wc`'s `jj new` failure is swallowed; a successful push then exits 0 with `@` still
  on the pre-rebase parent → **exit 0 with HEAD off-branch** [INFERENCE: requires the `jj new` to
  fail after a successful rebase; the swallow is observed code, the resulting state is inferred].
- 307-308/329-330: `bookmark set` after a successful rebase. jj normally auto-moves a bookmark whose
  target is rewritten, so this is a safety re-point [INFERENCE about auto-move; not measured]; if it
  fails the caller still exits 3.

**W6 — adopt-remote path (335-340).** `bookmark set -r <b>@origin` then `reanchor_wc`. If the set
fails, exit 3 with the branch where it was; if `reanchor_wc` is skipped because `@` is non-empty
(271), the branch has moved to origin while `@`/HEAD stay on the old line until the next snapshot.
No `-B`, so no rewind.

**W7 — concurrency between the `tip` read (553) and `bookmark set` (658).** The helper's lock is
advisory among helper invocations only; a seat's raw `jj`/`git` command is outside it. A bookmark
moved in that interval makes 658 refuse (W4). The guards cannot see it: 612 compares against the
stale `tip` only. No rewind possible (no `-B`) — the failure mode is stranded, not rewritten.

**W8 — exit 3 is not a HEAD window but is ambiguous.** After a *successful* push whose `ls-remote`
verification fails (237-244 transient error) `report_landed` returns 1 → `do_push` 1 → exit 3, the
same code as a rejected push. The correct retry is `push` (the bookmark was set before the push, so
HEAD == branch); retrying `commit` prints `nothing to commit` rc0 (575-578) while the remote already
has the commit [INFERENCE: depends on whether the push landed before the verification error].

## 3. Failure windows — author/committer not the lane identity

**A1 — metaedit is the only author stamp, and it is separate from the commit (598-605).** Per the
helper's own rationale (596-597) and the measured F4 (jj commit keeps `@`'s author; bare `--config`
only fixes the committer), 600 is required. Failure at 600 exits before any commit; `@` keeps its
author but no history changes. No persistence.

**A2 — no post-commit author assertion.** Guards 612-656 check parent and paths but never
`git log -1 --format='%an|%ae|%cn|%ce' "$hash"`. The first author check is `push_preflight`
218-228, after the bookmark has already moved (658). So a commit that somehow bypassed metaedit
would still be placed on the branch and only refused at push — where it persists (A3). This is the
asymmetry: parent/path violations are refused **before** the branch moves; identity violations are
refused **after**.

**A3 — a foreign-author commit already on the branch is permanent.** A raw `git commit` in the
colocated repo (selftest z13, `jj-lane-selftest.sh:505-515`) or a seat's `jj commit` + manual
`jj bookmark set` puts a foreign-authored commit in `origin/<b>..<b>`. 220-227 refuse → exit 3; the
commit stays on `refs/heads/<branch>`; every later `commit`/`push`/`push --no-rebase` (preflight 694)
refuses for the same reason. The driver sees `state` `ahead>0`, durability-pushes, fails, and reports
"FAIL lane has N unpushed commit(s) and a fast-forward push failed" (`inline.sh:119-124`) without
naming authorship. The helper has no repair subcommand; the documented repair is
`jj metaedit --update-author` (SrcJjMetaedit.md finding 1), run by hand.

**A4 — lane id is read from mutable jj config, not the lane.id mirror.** `push_preflight` calls
`lane_id_jj` (198 → 106-111), which parses `jj config get user.name`. `lane.id` is written at init
(440) but grep shows **no reader**. Re-running `jj-lane.sh init <dir> <new-id>` overwrites
`user.name` (427); every older branch commit then carries the old id and becomes "foreign" for
220-227 → A3 permanently, although git config `lane.id` still records the old binding. Current lane:
`user.name=mori-shokunin`, `lane.id=mori` — consistent today [observed].

**A5 — TOCTOU between the preflight (348) and the push (350) / recovery rebase (302-327).** The
authorship gate reads the branch before the push, nothing re-checks it inside `jj git push`, and the
helper's lock (132-138) does not exclude a seat's raw `git`/`jj` command. A foreign commit that
enters `origin/<b>..<b>` in that window has two outcomes:
- push succeeds → the foreign commit ships **unverified** (the gate ran before it existed);
- push is a lease rejection → `recover_remote_move` rebases it under the requested identity
  (302-305 / 324-327): author preserved, committer := `${id}-shokunin` — exactly the shape contract
  C2 calls `LANE_AUTHOR_MISMATCH`; the re-preflight at 356 then refuses (author still foreign) →
  exit 3 with the mismatched commit left on the branch.
Narrow, concurrency-only [INFERENCE]; the preflight is never re-run between 348 and 350.

**A6 — `--as protocol` is an allowed non-lane author, by design (516-517, 220-227).** A protocol
commit has author AND committer `protocol-shokunin`, so C2's `LANE_AUTHOR_MISMATCH`
(committer lane, author differs) will not flag it. This is not hypothetical: the lane's entering tip
24526ea is `protocol-shokunin|protocol-shokunin` [observed]. The census wording must either state
protocol as an allowed author or name it as a separate class; otherwise "every branch commit is
lane-authored" is false in the lane's own history before round 17 starts.

## 4. `cmd_state` — steps and blind spots

Steps: 156 arity; 158 `lane_realdir`; 162-167 branch = git `lane.branch` → `detect_branch`
(`symbolic-ref -q HEAD` 117 → `origin/HEAD` 121 → unique `master`/`main` 164-166); 169-172
`refs/heads/<branch>` and `refs/remotes/origin/<branch>` (40-hex required); 173-174 ahead/behind;
175 `head=attached|detached` via `symbolic-ref -q HEAD`; 176-178 `git status --porcelain` counts;
179 single line.

Confirmation of the blind spot: after any W1/W4 exit, `state` returns `local=<old tip>`,
`ahead=<unchanged, usually 0>`, `head=detached`, `tracked/untracked` counted against the git index —
which jj has just aligned to HEAD (the stranded commit), so the lane *looks clean*. None of those
fields encodes "which commit does HEAD point to" or "is HEAD an ancestor of the branch".
Consequences:
- `lane_tip` (`inline.sh:37`) and closure (`closure-prompt.md:24-26`, `ahead=0`) both pass.
- `head=attached` is also ambiguous: it only means HEAD is a symref to *some* branch; 175 never
  prints which one (`git checkout -b seat` would still read `attached`).
- 162-167 and 513 resolve the branch from **different sources** (`lane.branch` vs jj `trunk()`);
  out-of-band edits make `commit` and `state` grade different branches.
- 173-174 `|| echo 0` and 176 `2>/dev/null` turn a failed `rev-list`/`status` into a clean-looking
  line rather than an error.
- No field for a stranded commit, no author check, no `HEAD_BRANCH_MISMATCH`.

## 5. Impact on round-17 C2 and the helper (advisory to L1; nothing applied)

1. C2's `HEAD_BRANCH_MISMATCH` will detect W1/W4 **only if it uses the material test**
   `merge-base --is-ancestor HEAD refs/heads/<branch>` (contract line 92 already says this). Do not
   treat `symbolic-ref` failure/detachment as a mismatch: detached-at-tip is the normal post-commit
   state (F2, `inline.sh:33`).
2. `LANE_AUTHOR_MISMATCH` as defined catches A3/A4/A5 but not A6 (protocol), and it must be scoped
   to post-launch commits as the contract says — the entering tip is protocol-authored.
3. The helper's exit codes do not distinguish "nothing written" from "commit orphaned". A distinct
   code (or a `stranded <hash>` stderr line) between 604 and 658 would let the lane retry/repair
   instead of silently no-op'ing. A post-commit identity assertion at 606-610, using the same matrix
   as 220-227, would move the author refusal before the bookmark moves.
4. `state` could expose `head_commit=` and `head_on_branch=0|1` cheaply (one `rev-parse HEAD` + one
   `merge-base --is-ancestor`), which is what the driver currently lacks.
5. Selftest gap: no case forces 658-659 to fail and inspects the resulting `state`/HEAD; z7/z12
   exercise post-commit refusals but assert only the remote contents, not the local branch/HEAD
   relationship.

## 6. Limits

- No mutating jj/git command was run (contract forbids); everything past `jj commit` is inferred from
  code, the routed sandbox measurements (F2/F3/F4) and jj 0.45.1's binary strings.
- Whether jj re-attaches HEAD after `bookmark set` is unmeasured; the material invariant does not
  depend on it.
- The live lane has had no helper commit yet (jj op log: init ops + one snapshot only), so the
  attached-HEAD observation is the pre-commit steady state.
- "Persistence" of W1/W4 is derived from the `@`-empty retry path (570-578) and the non-empty
  re-anchor refusal (584-594); neither was executed in this read-only seat.

## Install / update record

None. Tools used: `jj` 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5, `git` 2.56.0, coreutils,
`strings` (binutils), all pre-existing. All commands read-only: `cat .git/HEAD`,
`git --no-optional-locks {symbolic-ref,rev-parse,merge-base,log,reflog,rev-list,config}`, `jj
--ignore-working-copy {log,config,bookmark list,op log}`, `jj bookmark set --help`, `strings`.
