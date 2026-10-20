# KnowledgeJjBranch — round 17 wave 1, C2 knowledge draft

Seat: `MoriR17.KnowledgeJjBranch-5` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`, entering tip `24526ea9617cd020fee16c28fe4d4a2789dc28cb`.
Scope: draft only, in this report. `corpus/knowledge/jj-branch-anchor-r17.md` was NOT written. No VCS write, no jj command, no gate or census run, no journal query.

Axes named for this item: C2 probe correctness (which repo, which ref), coverage (what the helper does and does not guarantee), operability (failure windows), calibration (claims limited to static reads), preservation (frozen gates untouched), adjacency (S044–S047 provisional rows, JjAuditMori F3/F4).

## Findings (observed or read; cited)

### F-1. The contract does not say which repo row 6 reads (contract ambiguity for L1)

`contract.md:84` says to use `refs/heads/<branch>` for "the report-closure `cat-file -e` and `log -1` (row 6)". The census implements row 6 in `ps_report_closed`, which runs against `$ROOT`, not the lane repo:

- `tools/mori-census.sh:2099-2102`: `cat-file -e "HEAD:$rpath"` and `log -1 --format=%ct -- "$rpath"` with `-C "$ROOT"`. The comment at `:2093-2094` says the report path is fleet-root-relative "for every lane".
- `tools/mori-census.sh:1967-1970` (`lane_repo`) returns the lane repo for ordinary lanes; `ps_report_closed` does not call it.

So the branch for row 6 must be resolved for the fleet root, not for the lane. Current state, read-only: fleet root `symbolic-ref -q HEAD` → `refs/heads/master` (rc 0); `HEAD` = `refs/heads/master` = `bb44c290cb4af797541e61267560bb87abd431e6`; no `.jj` (`ls -d` rc 2). For row 6 the change is therefore a no-op today, but the contract text should name the repo. Recommended: resolve the branch inside `ps_report_closed` with `-C "$ROOT"`.

### F-2. Row numbering: contract vs. JjAuditMori

The contract's "row 6" (report closure) and "row 9" (authorship) are census grading rows. JjAuditMori's table uses its own numbers (`.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md:206-247`). Mapping, observed in the census source:

| census site | command | repo | JjAuditMori row | contract row |
|---|---|---|---|---|
| `mori-census.sh:2100` | `cat-file -e HEAD:$rpath` | `$ROOT` (fleet) | 1 | 6 |
| `mori-census.sh:2102` | `log -1 -- $rpath` | `$ROOT` (fleet) | 2 | 6 |
| `mori-census.sh:2197` | `rev-parse --verify -q HEAD` | lane | 5 | 9 |
| `mori-census.sh:2207` | `log --since … ` (default rev HEAD) | lane | 6 | 9 |
| `mori-census.sh:2180` | `ls-files -mo --exclude-standard` | lane | 4 | unchanged |

### F-3. Colocation detaches HEAD; HEAD and the branch can disagree (JjAuditMori F2, F3)

- F2 (`JjAuditMori.md:43-60`, sandbox measurement by that auditor, not re-run here): after `jj commit`, `git symbolic-ref -q HEAD` → rc 1 and `git rev-parse '@{u}'` → rc 128.
- F3 (`JjAuditMori.md:62-77`): after a second commit without a bookmark move, `HEAD` = `d19d559`, `refs/heads/master` = `611dfb5`. Under jj, HEAD follows the working-copy parent immediately; the bookmark moves in a later `jj bookmark set`, and the remote in a later `jj git push`.
- Live lane today (read-only): `.jj` exists; `symbolic-ref -q HEAD` → `refs/heads/master` (rc 0); `HEAD` = `refs/heads/master` = `24526ea9617cd020fee16c28fe4d4a2789dc28cb`. Attachment today is not the detached state F2 measured, because no jj commit has run since init [INFERENCE: no lane commit since colocation was observed; not confirmed].

### F-4. The helper's guarantee is oid equality on the success path, with named exceptions

`scripts/hyaku/jj-lane.sh` (fleet root path; the file is not in the lane). Read-only, static; no run.

- Success path, `cmd_commit` (`:493-671`): lock at `:511`; author stamped first by `metaedit --update-author` (`:598-601`); `jj commit` (`:602-605`); parent must be the branch tip (`:612-616`); path and phantom-deletion guards (`:620-656`); `bookmark set "$branch" -r "$hash"` (`:658`); then `do_push` (`:669`). So on success `refs/heads/<branch>` is moved to the new commit before any push, and HEAD carries the same oid.
- HEAD attachment is NOT part of that guarantee. Under colocation HEAD is detached after `jj commit` (F2; S044 provisional).

Failure windows where HEAD and `refs/heads/<branch>` differ after the helper exits [INFERENCE from source; HEAD effect not measured]:

1. Guards that exit after the commit exists and before `bookmark set`: `:614-616` (parent not tip), `:623` and `:628` (path outside request; these `exit 1` inside `path_ok`, after `jj commit` at `:604`), `:652-653` (phantom deletion). HEAD ahead of branch; the helper does not revert the commit.
2. `bookmark set` failure at `:658-659`: same state.
3. Push recovery (`recover_remote_move`, `:280-342`): the rebase is followed by `bookmark set` (`:307`, `:329`). `reanchor_wc` moves `@` only when empty (`:265-275`); the helper's own comment at `:262-264` says a non-empty `@` is left alone and that the recovery rebase "can leave @ on the pre-rebase parent". HEAD may then point at a commit that is not the branch tip.
4. `do_push` failure, exit 3 (`:669`, `:701`): HEAD equals the branch locally but the commit is not on `origin/<branch>`. The census's HEAD-vs-branch check cannot see this; it is a landed-vs-pushed question (out of C2 scope).
5. Any `jj commit` outside the helper: F3 mechanism; HEAD moves, the bookmark does not.

So the claim "the helper keeps HEAD==branch except in its failure windows" holds only as commit-id equality on the success path. It is not a statement about attachment, and it says nothing about push state.

### F-5. Identity: the helper stamps the author, `jj commit` alone does not (JjAuditMori F4)

- F4 (`JjAuditMori.md:79-98`): a `jj commit` with ambient config kept the ambient author and gave the lane only the committer.
- The helper's `metaedit --update-author` (`jj-lane.sh:598-601`) runs before `jj commit` (`:602-605`) and sets both author and committer through per-command `--config`. Helper commits therefore satisfy `<lane>-shokunin <lane>@shokunin.local` on both fields.
- The helper also accepts `--as protocol` (`:516`). A `protocol-shokunin` committer is not the lane's committer and must not trigger `LANE_AUTHOR_MISMATCH`.
- Limit [INFERENCE]: a commit with ambient author and ambient committer (no lane committer) is not detected by a committer-keyed rule. Only the F4 signature (lane committer, foreign author) is in scope.

### F-6. Frozen gates: bytes match the receipts; r16's own gate has no receipt

Read-only `sha256sum`, lane at `24526ea` (`merge-base --is-ancestor 24526ea HEAD` rc 0; `HEAD` = `24526ea`):

| file | sha256 (prefix) | receipt |
|---|---|---|
| `tools/mori-census.sh` | `f1f8d1b6…` | `round-16/evidence/preservation.json` `files` after; `round-16/frozen/entering-capability.json` `production_pins` |
| `tools/mori-silence-cases.sh` | `34cd5770…` | same |
| `tools/mori-round13-regressions.py` | `23b753c1…` | same |
| `tools/mori-round14-regressions.py` | `533218a5…` | same |
| `tools/mori-round15-regressions.py` | `6a55c33c…` | same |
| `corpus/evidence/baseline-r10-20261015T2231Z.json` | `0993b235…` | same |
| `tools/mori-round16-regressions.py` | `e70ed67c…` | NOT in `preservation.json` or `production_pins` |

- The receipt's `entering_commit` is `b83edc6`, its `measured_commit` is `87a57c1`, and its scope is "Static byte preservation only; prior committed r15 gate receipts retained, not rerun." Current digests equal its `after` values, so the bytes are unchanged since that measurement.
- Frozen controls are pinned inside the gates as well: r13 `FROZEN_PINS` (`mori-round13-regressions.py:180`), r14 red digest (`mori-round14-regressions.py:186-189`), r15 `PINNED_FROZEN_SHA256` with git blob `0fa5e0d` (`mori-round15-regressions.py:49-52`, `:718-730`).
- So "r13–r16 gates are pinned by preservation receipts" is true for r13, r14, r15 and the census. It is not established for the r16 gate `tools/mori-round16-regressions.py`; this seat found no receipt for its bytes.

Why the gates are not edited: a gate's bytes are the subject of its receipt. Editing one changes its digest, breaks the receipt, and turns a historical red/green record into a different instrument. Each gate also embeds its frozen control. C2 is therefore tested by a new gate, `tools/mori-round17-jj-regressions.py` (`contract.md:91-94`), run against the entering census (`git show 24526ea:tools/mori-census.sh`) and the delivered census.

Known gaps carried, NOT fixed here (JjAuditMori F10, F12): the r16 and r15 gates run git without the census hardening (`mori-round16-regressions.py:701-703`, `mori-round15-regressions.py:782-784`); r13/r14/r15 selftests use stubs or never reach the revision probes (F11); the `.jj` output guard is missing from r13/r14 and from r15:1418 and r16:747 (F12). The HEAD-based `rev-parse` probes in r13:1245, r14:432, r15:806 and r16:712 remain as recorded (JjAuditMori rows 10, 12, 15, 17). They pin a commit under test, not a branch identity.

### F-7. Finding semantics the census must honour

- `HEAD_BRANCH_MISMATCH`: `git merge-base --is-ancestor HEAD refs/heads/<branch>` returning 1 fires. This catches HEAD ahead of the branch (the F-4 windows). It does NOT fire when HEAD is behind the branch (ancestor check passes). Exit 128 (unreadable repo or unknown ref) must map to unavailable, not to mismatch. Exit-status semantics: S046 (provisional; quote pending).
- Branch resolver (contract): `symbolic-ref -q HEAD` → `refs/remotes/origin/HEAD` → unique of `refs/heads/master`/`refs/heads/main`. Under a detached HEAD step 1 falls through, as `jj-lane.sh` `detect_branch` does (`:115-126`). The helper prefers `lane.branch` / the trunk alias first (`:87-103`, `:513`), which the census cannot read cheaply. If `lane.branch` ever differs from `origin/HEAD`, census and helper can disagree. Not observed in this read [INFERENCE].
- Resolver source for row 6 is the fleet root (F-1); for rows 9 it is the lane.

## Provisional sources (not verified by this seat)

- S044 — jj git-compatibility, colocated workspaces, Git HEAD detached. Planned row from `wave1-dispatch.json` (`SrcJjGitCompat`). Not registered in `corpus/SOURCES.md` (registry ends at S040 at read time; grep for `S04[3-9]` returned no rows). Quote pending.
- S045 — jj CLI reference, `jj metaedit --update-author` and `jj commit` author handling. Planned (`SrcJjMetaedit`). Quote pending.
- S046 — git-merge-base, `--is-ancestor` exit status. Planned (`SrcGitMergeBase`). Quote pending.
- S047 — git-symbolic-ref, `-q` on detached HEAD. Planned (`SrcGitSymbolicRef`). Quote pending.

The sibling reports `build/SrcJjGitCompat.md`, `SrcJjMetaedit.md`, `SrcGitMergeBase.md`, `SrcGitSymbolicRef.md` did not exist at read time (only `SrcRfc6585.md` was in `build/`). This seat did not open the upstream pages; the four rows stay provisional and carry no quotation here.

## Draft: `corpus/knowledge/jj-branch-anchor-r17.md` (draft in this report only)

````markdown
source: S044 (provisional) — https://jj-vcs.github.io/jj/latest/git-compatibility/ — jj git-compatibility, colocated workspaces; Git HEAD detached. S045 (provisional) — https://jj-vcs.github.io/jj/latest/cli-reference/ — `jj metaedit --update-author`, `jj commit` author handling. S046 (provisional) — https://git-scm.com/docs/git-merge-base — `--is-ancestor` exit status. S047 (provisional) — https://git-scm.com/docs/git-symbolic-ref — `-q` on detached HEAD. Rows are provisional: not yet in `corpus/SOURCES.md`; quotes pending the source scribes. Measured evidence: `.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md` F2, F3, F4 (sandbox, that auditor's run, not re-run here).
verified-at: 2026-10-20 — static reads of `tools/mori-census.sh`, `scripts/hyaku/jj-lane.sh`, the round-16 receipts and the JjAuditMori report; read-only `sha256sum` and `git rev-parse` at lane tip `24526ea`. No jj command, census run, gate run or journal query.
recheck: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 24526ea:tools/mori-census.sh | grep -nE 'HEAD|refs/heads'`; `sha256sum tools/mori-census.sh` expecting `f1f8d1b6…`; `grep -nE 'bookmark set|metaedit' /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh`.

# jj branch anchor for the lane census — HEAD versus refs/heads, identity mismatch, frozen gates — round 17

## Claim

Under jj colocation, `HEAD` names a commit, not a branch, and it is detached. The census should grade lane progress and report closure from `refs/heads/<branch>`, and should name a HEAD-ahead-of-branch divergence as `HEAD_BRANCH_MISMATCH` rather than grade silently from HEAD. A commit whose committer is the lane while its author is not is a `LANE_AUTHOR_MISMATCH` identity finding. Nothing else is claimed: no completeness of commits, no push state, no authentication of committers.

## Evidence

### 1. Colocation detaches HEAD

After `jj commit` in a colocated sandbox, `git symbolic-ref -q HEAD` returns rc 1 and `git rev-parse '@{u}'` returns rc 128 (JjAuditMori F2, `.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md:43-60`). Attachment is not an identity: the census must not require an attached HEAD. S044 and S047 describe the detached state (provisional).

### 2. HEAD and the branch diverge when the bookmark is not moved

JjAuditMori F3 (`JjAuditMori.md:62-77`): after a second commit without `jj bookmark set`, `HEAD` = `d19d559` and `refs/heads/master` = `611dfb5`. Under jj, HEAD follows the working-copy parent at once; the bookmark moves in a separate command and the remote in a later push.

### 3. The helper keeps the oids equal on success; named exceptions remain

`scripts/hyaku/jj-lane.sh` `cmd_commit` moves `refs/heads/<branch>` to the new commit (`bookmark set`, `:658`) before `do_push` (`:669`), under one lock. Exceptions where HEAD and the branch differ after exit: guard exits after the commit and before the bookmark move (`:614`, `:623`, `:628`, `:652`); bookmark-set failure (`:659`); push recovery with a non-empty working copy (`:262-275`, `:280-342`); exit 3 after a local commit that is not on origin (landed-versus-pushed, out of scope); a `jj commit` run outside the helper (F3). The equality claim is about commit ids only.

### 4. Identity is stamped by the helper, not by `jj commit`

JjAuditMori F4 (`JjAuditMori.md:79-98`): `jj commit` kept the ambient author and gave the lane only the committer. The helper runs `metaedit --update-author` before `jj commit` (`jj-lane.sh:598-605`). A commit whose committer is the lane and whose author is foreign is therefore evidence of a commit outside the helper. Ambient author plus ambient committer is not detected by this rule.

### 5. The census probes and their repositories

- `ps_report_closed` (`tools/mori-census.sh:2097-2110`) reads the fleet root (`-C "$ROOT"`), so row 6 resolves the branch of the fleet root, not of the lane.
- Authorship (`:2197`, `:2207`) reads the lane repo; the default revision is `HEAD`, which the change replaces with `refs/heads/<branch>`.
- `ls-files -mo` (`:2180`) is measured safe under colocation (F7) and is unchanged.

### 6. Frozen gates stay byte-identical

The r13, r14 and r15 gate scripts and the census, silence oracle and r10 baseline match the digests in `.ufo/waves/round-16/evidence/preservation.json` (`files.*.after`) and `.ufo/waves/round-16/frozen/entering-capability.json` (`production_pins`). The r16 gate has no such receipt and is not claimed. Gates are not edited in round 17: editing a gate changes its receipted bytes and its embedded frozen control. C2 is tested by `tools/mori-round17-jj-regressions.py`, which runs the entering census (`git show 24526ea:tools/mori-census.sh`) and the delivered census against real colocated jj sandboxes built in a temporary tree.

Known gaps not fixed in round 17: r15 and r16 gates run git without census hardening (JjAuditMori F10); HEAD-based `rev-parse` probes in r13, r14, r15, r16 remain as recorded (JjAuditMori rows 10, 12, 15, 17); the `.jj` output guard is absent from r13/r14 (F12).

## Limits

- Static reads and the JjAuditMori sandbox measurements. The census and the new gate were not run for this note.
- HEAD-vs-branch is a local property. Whether a commit is on `origin/<branch>` is a separate question and is not established here.
- Authorship is observed from commit fields only; it is not an authentication of the committer.
- `merge-base --is-ancestor` exit semantics: S046 provisional, quote pending.
- A lane whose `lane.branch` differs from `origin/HEAD` could make the census resolver and the helper disagree; not observed.

## Gate

`tools/mori-round17-jj-regressions.py --census PATH --output DIR` (contract `contract.md:91-94`): counts failed case assertions against the entering census (`git show 24526ea:tools/mori-census.sh`) and the delivered census.
````

## Recommendations to L1 (advisory; not judged here)

1. Name the repo for row 6 in `contract.md:84`: the branch resolved for `$ROOT` in `ps_report_closed`, not the lane branch (F-1).
2. Record in `SKILL.md`/`corpus/README.md` that the r13–r15 gates carry receipts; decide whether the r16 gate needs its own receipt (F-6). Do not edit the gates to add it.
3. Keep S044–S047 marked provisional until the four scribe reports land and the rows are registered in `corpus/SOURCES.md`; quotes are not in this draft.
4. Do not claim "HEAD==branch" as a lane property in the knowledge note; claim it only as the success-path oid equality with the F-4 exceptions.

## Checks the main agent should run

None assigned to this seat. For the integration owner: the `tools/mori-round17-jj-regressions.py` gate against `24526ea` and the delivered census (per contract), and a re-run of the `sha256sum` set in F-6 after any gate edit.

## Commands run (read-only; all rc recorded)

- `sha256sum` over the six pinned files plus `tools/mori-round16-regressions.py` in `mori-shokunin` — rc 0.
- `git rev-parse HEAD refs/heads/master` and `git merge-base --is-ancestor 24526ea… HEAD` in the lane — rc 0 (ancestor rc 0).
- `ls -d .jj` in the lane — rc 0 (exists). `ls -d /home/vgpnk/Projects/shokunin/.jj` — rc 2 (absent).
- `git symbolic-ref -q HEAD` in the lane and in the fleet root — rc 0 each (`refs/heads/master`).
- `git rev-parse --verify -q HEAD` in the fleet root — rc 0 (`bb44c290…`).
- `git log -1 … HEAD` in the lane — rc 0 (`24526ea`, protocol-shokunin author and committer).
- `jj --version` — rc 0 (`jj 0.45.1-7c41cdeb…`); no jj repo command run.

Installs or updates: none.

## Out of scope / not done

- `corpus/knowledge/jj-branch-anchor-r17.md` was not written (draft in this report, per assignment).
- No edit to any gate, census, helper, `SOURCES.md`, `MANIFEST.json`, `.ufo/state`, or any sibling lane. No VCS write.
- Not verified: the four S044–S047 upstream pages; live HEAD behaviour after the helper's failure windows (static reading only); the r16 gate's receipt status beyond its absence from `preservation.json`.
