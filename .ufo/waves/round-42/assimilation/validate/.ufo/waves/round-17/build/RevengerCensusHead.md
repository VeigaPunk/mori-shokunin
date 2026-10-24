# Census `HEAD` anchor — historical reconstruction

## Axis in scope

C2 operability: correctness of the census Git probes in a jj-colocated lane (`.ufo/waves/round-17/contract.md:16-20,80-90`). This is a reconstruction, not a verdict or an edit to the census.

## Reconstructed contract and evidence chain

**The r1 defect that motivated the cutover was the measurement, not a documented `HEAD`/branch dispute.** `LOG.md:73-80` records that r1 used a rolling window rather than the launch line and treated any in-window activity as progress, so it could grade a wrapped mission and misclassify sibling-only activity. The round-3 log says the r2 census cutover was launch-anchored and authorship-aware (`LOG.md:222-247`). The log does not state an explicit historical rationale for choosing `HEAD` over a named branch; that distinction is an inference from the implementation and its contract.

**Row 6 — committed report closure.** The r2 decision table defines closure as both (1) report-path presence in the committed tree and (2) the newest commit touching that path having `launch_epoch < ct ≤ NOW_EPOCH` (`corpus/knowledge/silence-grading-r2.md:103-113,180-197`; precursor `corpus/knowledge/lane-silence-r2.md:151-176`). The current helper implements this with `git cat-file -e HEAD:<path>` and an implicit-`HEAD` `git log -1 --format=%ct -- <path>` (`tools/mori-census.sh:2092-2110`). Thus `HEAD` is the committed-view anchor: an untracked or staged report does not close a mission, an old report cannot close a relaunch, and presence does not validate report contents. The note explicitly describes this as a narrow “mission open?” fact, not evidence that work passed.

**Row 9 — launch-window progress and authorship.** The r2 rule searches *all* commits in the post-launch window, not just the tip commit; exact lane author identity yields `progressing`, sibling-authored commits alone yield `progressing-weak`, and only absence of subject commits, sibling commits, and qualifying files yields `silent` (`silence-grading-r2.md:115-126`). The `rev-parse --verify -q HEAD` check is a guard for a repository with a commit history; the authorship `git log` has no explicit revision and therefore walks commits reachable from `HEAD` (`tools/mori-census.sh:2194-2237`). This is not “is the latest HEAD commit authored by this lane?” The decision note states the empty-history guard separately from the subsequent log scan (`corpus/knowledge/progressing-weak-r2.md:76-85`), and the cutover note specifically preserves a subject commit hidden behind a later sibling HEAD (`silence-cutover-r3.md:46-50,163-168`). The code also keeps the strict `(launch, NOW]` window and exact `%an <%ae>` match (`mori-census.sh:2213-2237`).

History pins both selectors to the first r2 cutover implementation: `git log -S'HEAD:'` and `git log -S'rev-parse --verify -q HEAD'` each identify `1439c47` (2026-10-15); `git log -L :ps_report_closed:tools/mori-census.sh` shows the row-6 helper introduced there, and `git log -L '/-- row 9: authorship/,+35:tools/mori-census.sh'` shows row 9 introduced there. The later row-9 change in `18d7d55` hardens environment handling and capture/membership behavior, not the reference anchor. The round-3 `LOG.md` section was appended in `bbcc1ad`; its entry describes the landed rule as “launch-anchored, authorship-aware” and records the closure predicate, rows A–D, and test receipts (`LOG.md:222-290`). The `HEAD` choice is therefore observed as the original Git implementation/default, but its authorial rationale beyond the predicates above is **[INFERENCE]**.

## Divergence and branch-anchor assessment

The current census does not resolve a lane branch: row 6 tests `HEAD:<path>` and implicitly logs from `HEAD`; row 9 verifies `HEAD` and implicitly scans from `HEAD` (`tools/mori-census.sh:2097-2108,2194-2207`). That matches ordinary Git when `HEAD` and the lane branch tip coincide, but they need not identify the same commit in a colocated/multi-workspace setting. A stale or divergent workspace `HEAD` can omit branch-visible commits/report updates; conversely, a workspace-only commit can be counted even when it is not on the lane branch. These are the ref-domain differences C2 is intended to expose, not a change to the launch/authorship contract.

**Yes—branch anchoring preserves the intent, with a deliberate and beneficial correction when the refs diverge.** Resolve the lane branch by the contract’s order (`symbolic-ref -q HEAD`, then `refs/remotes/origin/HEAD`, then a unique `refs/heads/master`/`main`) and use the same `refs/heads/<branch>` for row 6’s presence *and* newest-path-commit checks, and row 9’s existence guard *and* commit-history scan (`contract.md:82-85`). Keep the report path, strict time window, all-post-launch history scan, exact author fields, row A/B/C grading, and row-B dirty/untracked-filesystem evidence unchanged. In particular, branch anchoring must not become a tip-only author test or switch from author to committer identity. The contract makes the ref divergence visible as `HEAD_BRANCH_MISMATCH` and adds `LANE_AUTHOR_MISMATCH` without changing A/B/C grading semantics (`contract.md:86-90`). If HEAD and the resolved branch have the same commit history, results are equivalent; if not, the revised result intentionally measures the named lane branch, while the mismatch finding reports the divergence.

## Confidence and limits

- **High** on the implemented predicates and their first appearance: current source, historical notes, `git log -S`/`-L`, and the round-3 `LOG.md` entry agree.
- **High, conditional** that branch refs preserve the intended committed-progress/closure measurement when applied consistently to the same resolved lane branch; **medium** on the original reason for using `HEAD`, because no inspected commit/log text explains a branch-vs-HEAD design choice.
- No LSP device/server was exposed in the available tool inventory. Text search was used only to locate the current code; interpretation is based on anchored source reads and the history/decision notes, not grep as semantic proof. The attempt to read `mori-shokunin/PROTOCOL.md:153-168` returned “path not found”; the cited r2 notes reference that protocol, but it was not independently inspected here.
- A preliminary repository-wide search was too broad and reached `.ufo/interactive-sessions`; I stopped using it. No session/transcript payload is used or reproduced in this report.

## Read-only command trail

Commands were run against `master` to disambiguate the jj-colocated repository’s multiple refs; all successful history reads exited 0:

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log master --format='COMMIT %h %ad %s' --date=short -S'HEAD:' -- tools/mori-census.sh` — **0**, `1439c47`.
- Same command with `-S'rev-parse --verify -q HEAD'` — **0**, `1439c47`.
- `git ... log master ... -L :ps_report_closed:tools/mori-census.sh` — **0**.
- `git ... log master ... -L '/-- row 9: authorship/,+35:tools/mori-census.sh'` — **0**, including the later non-anchor hardening at `18d7d55`.
- `git ... log master ... -L 222,290:LOG.md` — **0**, section introduced at `bbcc1ad`.
- Initial `git log --all ... -S'HEAD:'` / `-L` attempts — **128** (`More than one commit to dig from` with `refs/jj/keep/...` and `refs/heads/master`); a first LOG regex range also exited **128** because its end pattern did not match. Re-running with explicit `master` and the current LOG line range succeeded.

No tests or runtime probes were run; no tools were installed or files other than this report were written.