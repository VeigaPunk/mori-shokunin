# CriticFrontier — round 17 wave 1 (critic, advisory; not a judgment)

Seat: MoriR17.CriticFrontier-5. Date 2026-10-20. Scope: §2b frontier step of
`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-17.md:42-74`: (a) is the misroot fix
"shown able to fail" (`:71`)? (b) is the sourced-claim linkage (`:73-74`) real or decorative?

Axes: **A1** mistake-mining integrity (the fix is falsifiable and actually in the loop);
**A2** provenance (a cited `S###` must constrain the claim it is cited for); **A3** C1 coverage (6),
specifically whether the `dead_rate_limit` / `dead_quota` tallies are honest; **A4** C2 operability (7).

## Verdict summary

| question | verdict | one-line reason |
|---|---|---|
| (a) misroot fix shown able to fail | **Designed to fail, not yet shown; fix not yet in the loop** | The delivered selftest discriminates legacy from new (pathspec mutant and `-uall` mutant are both caught), but no run output is recorded. The live replay cannot happen because the r16 artifact is now tracked. The Mistakes draft's fix is the prompt command, and that command's content-attribution step misses the real r16 file. |
| (b1) C2 ← S046 | **Real (load-bearing)** | Census branches on rc 0 / 1 / other, citing S046. A fixture asserts rc≠1 is never promoted. Live git gives rc 128 for a missing ref. |
| (b2) C1 ← S041/S043 | **Decorative, and S043 contradicts the classifier** | The draft knowledge entry says "The tool is unaffected" by S043. S043 lists ≥11 quota/balance/subscription codes on HTTP 429, and the tool classifies any 429 as rate-limit before it tests for quota. |

## (a) Misroot fix — counterexamples and evidence

Delivered tool: `.ufo/worktrees/round-17/MisrootSweep/tools/mori-misroot-sweep.py` (26014 B,
mtime 15:58). I read it. I did not run it (not my item; I write only this report).

What holds (static mutation reasoning over the selftest arms at `:445-521`, assertions `:538-608`):
- **Mutant "re-add default pathspec"** is caught. The `no-pathspec-round16` arm wants `MoriR16.Lesson`
  (`:453`), and `:605-606` fails if the planted root file is missing.
- **Mutant "drop `--untracked-files=all`"** is caught. With the flag removed, the nested
  `.ufo/waves/round-16/build/MoriNote.md` (`:314`) collapses to a directory entry. `:234-236` skips it
  as non-regular, so the path-set equality at `:563` fails in both arms. r16 actually showed this
  collapse: `.ufo/waves/round-16/evidence/misroot-sweep.json` `observed_stdout` is `?? .ufo/waves/hyaku/`
  and `?? .ufo/waves/round-16/build/`.
- **Mutant "drop path matching"** is caught by `path-only-match` (`:490-494`). **Mutant "drop content
  matching"** is caught by `sibling-detected-for-own-lane` (`:479-483`, `TabiR17` appears only in the body).
- Negative controls exist: CLEAN for another lane and for an unrelated lane+round (`:472-488`), so the
  detector is not constant-red. A sandbox byte snapshot including `.git` (`:441,591-599`) guards
  against index writes.

Counterexamples / defects:
1. **The r16 "shape" plant is not the r16 artifact.** `_PLANTED_TEXT` (`:307-311`) contains `MoriR16`
   in the body. The real file `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson`
   (847 B, sha256 `15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e`) contains no lane
   or round token: `grep -c -i -E 'mori|r16|round-16|round 16|round16'` → `0`, rc 1. In-memory, the
   tool's own regexes (`:113-128`) on the real body give lane=False, round=False. The real file is
   attributable **only by its path**. The canonical r16 arm therefore passes through content, and it
   would keep passing with path matching removed. Only the separate synthetic `MoriR15.note` arm protects
   the property that actually decided r16. Correction: give the planted body no lane/round token
   (e.g. a `BootContinuity disclosure …` line) and assert `matched_in == ["path"]` on it.
2. **The prompt procedure the Mistakes row cites as the fix fails on the real case.** Prompt
   `mori-round-17.md:272-276` says run `git … status --porcelain` (no `-uall`), then attribute a file
   when "its content names your lane/round". The real r16 body names neither (item 1). An L1 who follows
   the prompt literally sees `?? MoriR16.Lesson` and, at the attribution step, concludes it is not
   mori's. `LessonMistakesDraft.md` M1 gives as fix: "Future fleet sweeps run `git -C <fleet> status
   --porcelain` with no pathspec". That fix is neither the tool nor `-uall`, and it has no able-to-fail
   evidence. Under `:71` ("counts only once shown able to fail") M1's fix does not count yet.
   Correction: the fix column names `tools/mori-misroot-sweep.py` (path+content matching, `-uall`) and
   cites the recorded `--selftest` command, rc and JSON (`planted_found_without_pathspec: true`,
   `planted_found_with_legacy_pathspec: false`). The pre-report sweep evidence is that tool's live
   `--lane Mori --round 17` JSON, not the bare prompt command.
3. **"Shown" is unobserved.** No MisrootSweep report is in `build/`, and I saw no selftest output.
   [INFERENCE] The design should pass. Showing it still requires a recorded run.
4. **A live replay cannot falsify anything.** `git ls-files --error-unmatch .ufo/waves/hyaku/misroots/MoriR16.Lesson`
   → rc 0 (tracked since `ac0a7fc 2026-10-20 ops(hyaku): wrap-up …`). An untracked-only sweep never
   sees it. Even untracked, its archive location sits inside the legacy pathspec `.ufo/waves`, so a live
   run could not tell old from new. The sandbox selftest is the only discriminating falsifier, which
   makes item 3 binding.
5. **Captured-by column misused.** M1's captured-by names the hyaku closure verifier, i.e. who found it.
   `:70` defines captured-by as "the criterion or rule that should have caught it". That is the r16
   pre-report sweep rule with the addendum pathspec `-- .ufo/waves .ufo/reports` (misroot-sweep.json
   `command`).
6. **Destructive follow-on with weak attribution (tradeoff; L1 decides).** Candidates feed a
   copy-and-delete step (`:274-276`). The regexes accept loose co-occurrence. In-memory, lane=Mori,
   round=17: `'TabiR17 cites mori-shokunin'` → match, `'error17 Mori'` → match, `'for17 mori'` → match.
   A sibling lane's overlap note that mentions `mori-shokunin` and its own R17 is flagged. The `Memori`
   left guard and the `R170` right guard (`:117,126`) have no fixture, so those mutants survive.
   Smallest fix: add an `attribution` field, `seat_id` when `<lane>R<N>` is adjacent in path or body
   and `tokens` otherwise, and add one fixture each for `Memori…R16` and `MoriR160`.
7. **Protected and ignored paths.** Neither `.ufo/state/` (never-touch, prompt `:277`) nor ignored paths
   are handled. Live fleet now: `.ufo/state/mori.report-baseline` is untracked and path-matches the
   lane (round token absent today → not a candidate; [INFERENCE] a future driver write naming the round
   would make it one). The fleet `.gitignore` hides `.ufo/waves/*/*-scratch/` and `*-shokunin/`
   (`git check-ignore`; `--ignored=matching` also lists `.tower/`). A seat writing
   `.ufo/waves/round-17/mori-scratch/x` at the fleet would be invisible. The docstring (`:21`) states
   this limit, but the JSON carries no ignored count. Tracked-file overwrites (` M`, currently
   `.ufo/watchdog.log`) are out of scope and not stated. Smallest fix: mark `.ufo/state/` hits as
   `protected` and never as `candidate_misroot`; emit an `ignored_entries` count (excluding
   `*-shokunin/`) and a `tracked_modified` count as limits.

Impacted axes: A1 (items 1-5), A2 (item 2 cites a fix that cannot catch the real case), safety
(items 6-7).

## (b) Sourced-claim linkage

The prompt test (`:73-74`: "the knowledge entry or evidence it lands cites that S###") checks only
that a citation exists, so a decorative citation satisfies it. The test I applied is counterfactual:
**if the row taught something different, would a code branch or fixture assertion change?**

### C2 ← S046 (git-merge-base `--is-ancestor`): REAL
- Source: `build/SrcGitMergeBase.md:11,15` ("exit with status 0 if true, or with status 1 if not. Errors
  are signaled by a non-zero status that is not 1"). I did not re-open the URL; I rely on the sibling
  gate draft.
- Code depends on it: `.ufo/worktrees/round-17/CensusJj/tools/mori-census.sh:2139-2144` (comment cites
  S046) and `:2161-2177` (`0)` consistent; `1)` → `GL_HBM=1`; `*)` →
  `head_branch_probe_unavailable=rc-$CAP_RC`). The finding is emitted only on `GL_HBM -eq 1` (`:2441-2442`).
- A fixture asserts the teaching: `:4015-4029` (stub rc 2 → CLEAN, and `bad` if promoted to
  `HEAD_BRANCH_MISMATCH`).
- Live behaviour confirms the error branch is reachable. Read-only in the lane:
  `git merge-base --is-ancestor HEAD refs/heads/does-not-exist` → `fatal: Not a valid object name`,
  rc **128**; `… refs/heads/master` → rc 0.
- Residual gap: the fixture is a stubbed git returning rc 2. JjGate's real-sandbox gate had no
  `merge-base` hit in `JjGate/tools` at read time, so no case shows real git producing rc 128 there.
  Correction: add one real-sandbox case where `refs/heads/<branch>` is absent or unreadable after HEAD
  resolves, and assert `head_branch_probe_unavailable=rc-128` with no finding. Also register S046 as
  `mined` with used-by `corpus/knowledge/jj-branch-anchor-r17.md` and a `## Gate` line. Until it is
  registered, the linkage is real in code but not yet registered as provenance.
- S047 (symbolic-ref `-q`) is weaker. In the live lane `git symbolic-ref -q HEAD` → `refs/heads/master`
  rc 0 (attached), and `git config lane.branch` = `master`. `scripts/hyaku/jj-lane.sh:387` resolves
  `lane_branch_jj` → `lane_branch_git` (`lane.branch`) → `detect_branch`, but the C2 contract
  (`contract.md:82-83`) copies only `detect_branch`, which jj-lane.sh marks as "used ONLY by init"
  (`:113`). That is a duplicate-authority risk for C2 (CriticC2's ground). It means S047's
  detached-HEAD case exercises a fallback, not the authority. Cite S047 as context, not as the sourced
  claim.

### C1 ← S041 (RFC 6585) / S043 (Z.AI codes): DECORATIVE, and contradicted
- The draft entry admits non-dependence: `build/KnowledgeSeatTerminal.md:67` says "The tool is
  unaffected: it keys on `errorStatus`, on error-message tokens, and on the digit string". `:66` relies
  on S041 only for the general meaning of 429. RFC 6585 §4 itself "does not define how the origin
  server identifies the user, nor how it counts requests" (`build/SrcRfc6585.md:27`). No branch in
  `mori-seat-terminal.py` would change if either row were rejected.
- **S043 falsifies the classifier as built.** I fetched `https://docs.z.ai/api-reference/api-code.md`
  (accessed 2026-10-20, `curl … | grep -n -E '^\| *1[0-9]{3} *\| *429'`, rc 0/0). It lists HTTP 429
  for 1113 "Insufficient balance…", 1302 "Rate limit reached for requests", 1305 overload, 1308 "Usage
  limit reached for…", 1309 plan expired, 1310 "Weekly/Monthly Limit Exhausted", 1311, 1313-1315, and
  1316-1321 "Usage limit reached for the past 5 hours/7 days…" (lines 16, 31-45). The delivered tool
  `.ufo/worktrees/round-17/SeatTool/tools/mori-seat-terminal.py:181-186` tests `error_status == 429`
  or the `429` token **before** the quota tokens, and it never uses `error_code` (`:64,257` extract it
  only). A Z.AI quota/balance/plan death is therefore tallied `dead_rate_limit` and never `dead_quota`.
  The contract (`contract.md:51`) and the draft entry (`KnowledgeSeatTerminal.md:55`) restate this as
  intended. `QUOTA_TOKENS` `"usage limit"` (`:60`) is case-sensitive and would also miss Z.AI's `Usage
  limit` [INFERENCE: depends on the transcript errorMessage carrying that text]. Citing S043 under
  `source:` for that entry would be false provenance: the cited row refutes the claim's rate/quota
  split.
- Smallest safe correction (pick one; L1 decides):
  (i) make S043 load-bearing. When `error_code` is present, classify by the S043 table before the
  429 test: 1302 → `dead_rate_limit`; 1113, 1308-1310 and 1316-1321 → `dead_quota`; other 429 codes →
  `dead_error_other` or a stated bucket. Add one fixture per branch. C1 would then be a second real
  sourced claim.
  (ii) drop S041/S043 from C1's `source:`, register them `queued` with used-by `—`, and add the S043
  teaching to the entry's limits: on Z.AI, `dead_rate_limit` includes quota deaths.
  Under either option the round's sourced claim must be C2/S046, as `build/FrontierLinkage.md:35`
  proposes. Note that FrontierLinkage `:30` understates the C1 problem: it recommends renaming the
  class's meaning, but the class counts are wrong for the provider that motivated C1 (`contract.md:13-15`).
- S042 (Retry-After) and S048 (pacman log) attach to no claim. Neither C1 nor C2 reads the header or
  pacman.log (`FrontierLinkage.md:16,22`). They are fine as `queued` with `—`. Do not count them toward
  `:73`.

Impacted axes: A2 (C1 false-provenance risk), A3 (C1 dead-class honesty on zai), A4 (C2 sound; one
real-git case missing).

## Commands run (all read-only; `GIT_OPTIONAL_LOCKS=0` on every git)
My item named no commands. These are disclosed as read-only probes:
- `git -C /home/vgpnk/Projects/shokunin status --porcelain=v1 --untracked-files=all` (rc 0; 10-11
  `??`, 1 ` M`). `--ignored=matching` listing. `check-ignore -v` (rc 1). `ls-files --error-unmatch` (rc 0).
  `log -1 --format` on the archive.
- `git -C mori-shokunin symbolic-ref -q HEAD` (rc 0), `symbolic-ref -q refs/remotes/origin/HEAD`
  (rc 0), `config --get-regexp`, `merge-base --is-ancestor` ×2 (rc 128, rc 0).
- `grep -c`, `sha256sum`, `stat` on the archived r16 file. In-memory regex simulation (copied
  `:113-128`) over the fleet untracked list and the archive. Token counts only; no foreign file content
  printed.
- `curl -sS -L --max-time 30 https://docs.z.ai/api-reference/api-code.md | grep …` to stdout (rc 0/0).
- No transcripts, journal, /tmp, VCS writes, or installs (tooling: none installed or updated). The only
  write is this file.
