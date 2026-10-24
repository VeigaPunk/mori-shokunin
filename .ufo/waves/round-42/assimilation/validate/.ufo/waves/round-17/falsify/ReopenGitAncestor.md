# ReopenGitAncestor — fresh falsification of source row S046

Seat: `MoriR17.ReopenGitAncestor-4` (scout, leaf; no dispatch). Date and source access
date: **2026-10-20**. Targets: `corpus/SOURCES.md:52` (S046), `corpus/lessons/round-17.md:52`
(Gate row) and `:42-43` (access-date rule), `corpus/knowledge/jj-branch-anchor-r17.md:1,25`,
against the live page, the opening receipt `.ufo/waves/round-17/build/SrcGitMergeBase.md`,
and the delivered census/gates. Read the round-17 contract including Amendment A1 and
`PINNED_INPUTS.json` first. Attacked scope is the S046 row and its dependency links only.

## Verdict

**AGREE with S046's source, scope, anchor, tier, opened/recheck, canonical quote, and
status/used-by links.** The page exists (HTTP 200), the lesson quote is a verbatim 11-word
fragment located in the `--is-ancestor` item under `OPERATION MODES`, the version claim is
exact, and the knowledge note and delivered census genuinely depend on the fact (code branch
plus a stub assertion), so it is not decorative. No falsification of the row was found.

Two precision caveats and one verification gap, none of which invalidate the row:

1. `teaches` paraphrases the page's one-way statement ("errors are signaled by a non-zero
   status that is not 1") as its converse ("another nonzero status means error"). The
   operational rule the lane needs (only status 1 may be read as "not ancestor") is supported
   by the contrapositive, and the census's rc>1 silence is conservative; the converse itself
   is **[INFERENCE]**, not page text.
2. The canonical Gate quote at `corpus/lessons/round-17.md:52` is the error half only. The
   exit-0/exit-1 half asserted by the row's `teaches` is in the same `--is-ancestor` item and
   is quoted in the opening receipt (`build/SrcGitMergeBase.md:13-15`, 25 words). Combined,
   the record covers both halves; the lessons quote alone does not.
3. The C2 real-sandbox gate has no rc>1 case; S046's error/status-1 distinction is exercised
   only by the census's stub-based selftest. The knowledge note's `recheck` command therefore
   cannot detect a regression of that specific branch.

## Live source evidence

- URL: https://git-scm.com/docs/git-merge-base — fetched 2026-10-20 (audit time 19:49 GMT).
- `curl -sS -o /dev/null -w ...` → `http=200 remote_ip=2606:4700:10::ac42:95b9 time=0.08`, rc0.
- `curl -sSI` → `HTTP/2 200`, `content-type: text/html; charset=utf-8`,
  `last-modified: Tue, 20 Oct 2026 04:47:16 GMT` (same-day site regeneration; fetched text
  matches the row, so the edit did not invalidate it). No redirect; no `<link rel=canonical>`.
- Title: `Git - git-merge-base Documentation`.
- Located section: `<h2 id="_operation_modes">OPERATION MODES</h2>` (raw HTML line 1668),
  item `<dt ... id="Documentation/git-merge-base.txt---is-ancestor">` (raw line 1701), then:

  > Check if the first &lt;commit&gt; is an ancestor of the second &lt;commit&gt;,
  > and exit with status 0 if true, or with status 1 if not.
  > Errors are signaled by a non-zero status that is not 1.

  (raw `<dd><p>` at bytes ~30074-30127; `<span class="hover-term" data-term="commit">`
  markup around the two `&lt;commit&gt;` tokens only).
- SYNOPSIS also carries `git merge-base --is-ancestor <commit> <commit>` — exactly the
  two-commit form the census invokes.
- Version evidence: page says `git-merge-base last updated in 2.43.0`; version table first
  entry `2.43.1 → 2.56.0 no changes`. Host binary at audit: `git version 2.56.0`, so the
  documented baseline is current for the installed git (no version skew observed).
- Machine checks after tag stripping, HTML unescape and whitespace normalization:
  error sentence **1 occurrence, 11 words**; 0/1 sentence **1 occurrence, 25 words**.

## Immutable-field attack

| Field | Attacked against live page | Verdict |
|---|---|---|
| source | Official Git documentation host; 200; title matches; URL is the canonical rendered page used by S047. | **AGREE**. Caveat: unversioned `latest` URL, no content digest retained (same convention as S044/S047); only access date + `on-release` recheck pin it. |
| scope | `ancestry-check exit status`. The quoted sentences are inside the `--is-ancestor` item and describe only exit status, not merge-base output or jj semantics. The row does not claim jj behavior. | **AGREE** |
| anchor | `OPERATION MODES, --is-ancestor; last updated 2.43.0, no changes listed through 2.56.0`. Both halves verified: section heading and `dt` anchor exist; version strings match exactly. HTML has no stable line numbers, so the section/item anchor is the right granularity. | **AGREE** |
| teaches | Clause 1 (`0` ancestor, `1` not ancestor) is literal. Clause 2 ("another nonzero status means error; a probe must not report every nonzero status as divergence") is the operational partition; the doc's one-way sentence supports reading only status 1 as "not ancestor". The converse "non-1 nonzero ⇒ error" is not a page sentence. | **AGREE as distillation; converse is [INFERENCE]** — low-severity wording, not a false fact |
| tier | `docs`, tier `A`: official Git project documentation, primary for Git CLI exit codes; same tier-A convention as S039/S040 and S047. | **AGREE** |
| opened 2026-10-20 | Matches this fresh access and the Gate-wide access-date rule (`corpus/lessons/round-17.md:42`). | **AGREE** |
| recheck `on-release` | Appropriate: the page is an unversioned docs URL whose content changes are tied to releases (version table). | **AGREE** |

## Quote audit (`corpus/lessons/round-17.md:52`)

Canonical quote: “Errors are signaled by a non-zero status that is not 1.”

- Verbatim: exact substring of the live page, **1 occurrence**, final period preserved,
  ASCII `non-zero`, no internal quotes. Outer typographic quotes are the lane's table
  delimiters, not page content.
- Length: **11 words** (≤25). Location label `OPERATION MODES --is-ancestor` is correct
  (h2 + dt), not the SYNOPSIS occurrence of the option name.
- Coverage: the quote proves only the error-signal half. The 0/1 semantics are in the
  preceding page sentence and are quoted at `build/SrcGitMergeBase.md:13-15` (25 words,
  verified verbatim and 1 occurrence). The lessons row and the receipt together cover the
  full `--is-ancestor` contract; the canonical quote alone does not.

## Status and used-by recheck

- `corpus/SOURCES.md:52`: `status=mined`, `used-by=corpus/knowledge/jj-branch-anchor-r17.md`,
  `recheck=on-release`, `opened=2026-10-20`. No cell contradicts the lessons claim
  (`corpus/lessons/round-17.md:56-59`).
- The used-by note exists in the worktree and at measured commit
  `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` (`git cat-file -e` rc0 for both the note and
  `corpus/SOURCES.md`). It cites S046 at `:1` (source header) and `:25`
  (`| another nonzero status | probe error, not proof of divergence (S046) |`).
- `corpus/README.md:356` indexes the note (lane-silence VCS provenance). `SCORECARD.md:1024`
  says "S046 drives status1-versus-error handling in C2". Consistent.
- `grep -rn S046 corpus/knowledge/` returns only `jj-branch-anchor-r17.md`, so used-by is
  not incomplete for knowledge notes. No row still says queued for S046. No stale link.

## Dependency: does the knowledge note actually depend on S046?

Counterfactual: if S046 taught "every nonzero status means not ancestor", would code or a
fixture assertion change? Yes:

- `tools/mori-census.sh:2142-2145` — comment: "rc 1 = HEAD is ahead … any other rc = probe
  error. A probe error emits nothing — it is never promoted to the mismatch finding (S046)".
- `tools/mori-census.sh:2157-2170` — `rev-parse` HEAD, then
  `merge-base --is-ancestor HEAD "refs/heads/$branch"`, then `case "$CAP_RC" in 0) ;; 1) …
  GL_HBM=1 ;; esac`. rc>1 falls through silently; `GL_HBM` is emitted as a finding only at
  `:2442`. Collapsing `1)` into `*)` would be the contrary teaching.
- `tools/mori-census.sh:4041-4056` — stub `git-merge-base.rc=2` case asserts rc0 CLEAN and
  explicitly fails if `HEAD_BRANCH_MISMATCH` is promoted. This assertion inverts under the
  contrary teaching.
- `corpus/knowledge/jj-branch-anchor-r17.md:25` — the table row would become false/incomplete.

Therefore the dependency is **real but narrow**: S046 is load-bearing for the probe-error
edge of the `HEAD_BRANCH_MISMATCH` predicate, not for the branch-anchoring premise (S044/
S045 and JjAuditMori F3/F4 carry that). Not decorative.

Verification gap (does not falsify the row): the measured C2 gate
`tools/mori-round17-jj-regressions.py:693-706` has 12 real-sandbox cases
(`git-plain-progress`, `git-detached-at-tip`, `git-detached-commit`, `git-detached-behind`,
`git-report-on-branch`, `git-report-off-branch`, `git-foreign-author`, `jj-helper-commit`,
`jj-commit-no-bookmark`, `jj-ambient-author`, `jj-sibling-author`, `git-fallback-head`); all
have either a resolvable branch (rc0/rc1) or no branch (HEAD fallback). None produces rc>1.
The gate's dormant fixture census also uses `! git … merge-base --is-ancestor` (any nonzero)
at `tools/mori-round17-jj-regressions.py:988`, but that fixture is gate selftest only, never
installed, and never sees rc>1. So only `tools/mori-census.sh --selftest` exercises S046's
distinction; the note's `recheck` (jj gate) cannot detect its regression. This matches
CriticFrontier's already-recorded residual (`build/CriticFrontier.md:112`).

Incidental, outside S046's row: `build/CriticFrontier.md:103` and
`build/SkillRegistry.md:110,223` cite a `head_branch_probe_unavailable=rc-$CAP_RC`
diagnostic. `grep` of the delivered `tools/mori-census.sh` finds no such variable; the
delivered behavior is silence (`:2144-2145`). The downstream build-report claim is stale
relative to delivered bytes. The knowledge note does not make that claim.

## Residuals / unknowns

1. [INFERENCE] `teaches` clause 2's converse ("another nonzero status means error") is not a
   page sentence. The page states only that errors use a non-1 nonzero status. Operationally
   safe for git and for the census's conservative no-finding path.
2. [info] The canonical Gate quote covers the error half only; the 0/1 half lives in the
   opening receipt's 25-word quote. If the Gate rule is read as "the quote must carry the
   whole `teaches` cell", the canonical quote under-covers; the anchor plus receipt cover it.
3. [info] Unversioned docs URL, no archived page digest; `on-release` + access date are the
   only drift controls. The version table (`2.43.0`, no changes through `2.56.0`) and host
   git 2.56.0 agree today.
4. [info] No real-sandbox rc>1 assertion in the C2 gate; only the stub selftest holds the
   S046 distinction. A future census edit that collapsed rc>1 into the finding could pass
   the C2 measurement and the note's recheck.
5. [INFERENCE] S046 documents exit codes, not history completeness. In a shallow/grafted
   repository a true ancestor outside the available object graph could return status 1 and
   be read as "not ancestor"; the page is silent. The lane repo is not shallow at audit
   (`git rev-parse --is-shallow-repository` → `false`), so no observed false positive.
6. [INFERENCE] The census probes `HEAD` at `:2158` after verifying `$h` at `:2157`, so a
   concurrent HEAD move between the two calls could make the answered commit differ from the
   reported short head. Not observed; doc semantics still apply to the probed commit.
7. [observed] Page `last-modified` is the same day as access; the quote and version strings
   match the fetched bytes, so the same-day regeneration did not stale the row.

## Commands run (read-only; no probe reruns, no writes outside this report)

| Command | rc | Output |
|---|---|---|
| `curl -sS -o /dev/null -w ... https://git-scm.com/docs/git-merge-base` | 0 | `http=200 time=0.08` |
| `curl -sSI …` | 0 | `HTTP/2 200`, `last-modified: Tue, 20 Oct 2026 04:47:16 GMT` |
| `python3` fetch + tag-strip/unescape/normalize + substring count | 0 | error quote `occ 1, words 11`; 0/1 quote `occ 1, words 25`; `last updated in 2.43.0`; `2.43.1 → 2.56.0 no changes` |
| `git --version` | 0 | `git version 2.56.0` |
| `git rev-parse --is-shallow-repository` | 0 | `false` |
| `git cat-file -e 273aa74:corpus/knowledge/jj-branch-anchor-r17.md` / `…:corpus/SOURCES.md` | 0 | both present |
| `git show 273aa74:… \| grep -n S046` | 0 | note `:1,:25`; registry `:52`; census `:2145,:4042` |
| `grep -rn S046 corpus/` / `corpus/knowledge/` / `tools/` | 0 | registry, lessons, one knowledge note, census comments |

## Scope limits

No source-registry edit, no corpus edit, no other report touched, no VCS mutation, no
background job, no live journal query, no pacman transaction, no package install or update,
no `/tmp` writes, no credential/transcript reads. This report attacks evidence only; L1
`MoriR17` remains the sole integrator and judge. **No defect was found in the row's source,
scope, anchor, tier, quote, status or used-by links**; the items above are wording precision,
a real-sandbox coverage gap, and scope limits, not a falsification.
