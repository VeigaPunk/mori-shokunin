# ReopenJjCompat — fresh falsification of source row S044

Seat: `MoriR17.ReopenJjCompat-4` (scout, leaf; no dispatch). Date and source access date:
**2026-10-20**. Target: `corpus/SOURCES.md:50` (S044), `corpus/lessons/round-17.md:50`,
`corpus/knowledge/jj-branch-anchor-r17.md:1,9,15-19`, checked against the live page and the
opening receipt `.ufo/waves/round-17/build/SrcJjGitCompat.md`. Read the round-17 contract
(including Amendment A1) and `PINNED_INPUTS.json` first.

## Verdict

**AGREE with S044, with two non-blocking precision caveats and one dependency limit.** The
source exists, is the canonical page, the lesson quote is a verbatim 25-word fragment found
exactly once on the live page, and every immutable field is defensible. No falsification found.
The caveats are: (a) the anchor also names a feature row that does not host the quote; (b) the
second `teaches` clause is a valid entailment, not a literal sentence, and the page's Branches
section is a TODO so it cannot ground bookmark mapping or an off-branch HEAD. The knowledge
note's operative claims are carried by JjAuditMori F2/F3 and S046/S047; S044 is a premise
citation, not decorative but not the proof of the off-branch hazard.

## Live source evidence

- URL: https://docs.jj-vcs.dev/latest/git-compatibility/
- Fetch: `curl -sS -L -o /dev/null -w ...` → `http=200 final=https://docs.jj-vcs.dev/latest/git-compatibility/ type=text/html; charset=UTF-8`, rc0. Title: `Git compatibility - Jujutsu docs`.
- Located section: **Colocated Jujutsu/Git workspaces** (`#colocated-jujutsugit-workspaces`),
  in the paragraph that begins “It is allowed to mix `jj` and `git` commands in such a
  workspace in any order.”
- Located quote (tags stripped, whitespace normalized):

  > jj commands will usually put the Git repo in a "detached HEAD" state, since in jj there is not concept of a "currently tracked branch".

- Machine checks: exact substring after markup stripping/whitespace normalization; **1
  occurrence**; **25 words**; the upstream text has `<code>jj</code>` markup, so the only
  difference from the lesson table is removed code formatting, which the opening receipt
  already discloses. The ungrammatical “there is not concept” is upstream and preserved.
- Same page, other checkable anchors: feature row “**Detached HEAD: Yes.** Jujutsu supports
  anonymous branches, so this is a natural state.”; Branches section is literally “TODO:
  Describe how branches are mapped”; the only documented branch-position disagreement is the
  conflicted-branch caveat (“the position of the branch in the Git repo will disagree …”).

## Immutable-field attack

| Field | Attacked against live page | Verdict |
|---|---|---|
| source | `jj Git compatibility — https://docs.jj-vcs.dev/latest/git-compatibility/`; 200, canonical `docs.jj-vcs.dev`, title matches. Wave-1 `jj-vcs.github.io` URL redirects here (`build/SrcJjGitCompat.md:9-10,47-48`). | **AGREE** |
| scope | `colocated jj/Git HEAD state`. Quote is inside the colocated-workspaces section and is about the Git repo's HEAD; L1 correctly dropped the receipt draft's broader “and branch mapping” because the page's Branches section is TODO. | **AGREE** |
| anchor | `Detached HEAD feature row and Colocated Jujutsu/Git workspaces; opened 2026-10-20`. The quoted sentence is located in the second anchor only; the feature row exists but says detached HEAD is a natural state, not that jj commands put Git there. Both anchors are real page locations; one is context, not the quote site. | **AGREE, precision caveat** |
| teaches | Clause 1 “jj commands usually put Git in detached HEAD state” is literal with the page's hedge “will usually”. Clause 2 “a commit-id read is not a branch-identity proof” is an entailment of “there is not concept of a currently tracked branch”, not a located sentence. | **AGREE as distillation; clause 2 is [INFERENCE]** |
| tier | Official jj project documentation, primary. Same tier-A convention as S039/S040 (systemd man pages) and S046/S047 (git-scm docs). Caveat: the page is the `latest` alias with no pinned jj version; only the access date pins it. | **AGREE** |
| opened 2026-10-20 | Matches this fresh access; lesson Gate states all access dates 2026-10-20 (`corpus/lessons/round-17.md:42`). | **AGREE** |
| recheck `on-release` | Appropriate for a `latest` docs alias; no fixed version marker exists on the page (only a version-selector widget). | **AGREE** |

## Quote audit (`corpus/lessons/round-17.md:50`)

- URL and location label “Colocated workspaces:” point at the correct section (heading is
  “Colocated Jujutsu/Git workspaces”; the shortening is locatable).
- Word count **25**, so the ≤25-word Gate rule holds exactly. The quote is a fragment of a
  longer sentence (“One reason for this (see below for more) is that …”); it preserves
  “will usually”, the straight double quotes around `detached HEAD` and `currently tracked
  branch`, and the final period.
- Only formatting deltas: upstream `<code>jj</code>` markup removed and typographic outer
  quotes added. Disclosed in `build/SrcJjGitCompat.md:14,18-22`. Not a verbatim defect.

## Status and used-by recheck

- `corpus/SOURCES.md:50`: status **mined**, used-by `corpus/knowledge/jj-branch-anchor-r17.md`.
  The note exists; line 1 cites S044/S045 with the correct pairing (“colocation, metaedit
  --update-author”), and lines 23/38 cite S046/S045 inline.
- `corpus/lessons/round-17.md:56` states S044 enters mined with the new knowledge path; the
  registry row agrees. S042/S048 remain queued as stated. No stale status link found.
- `grep -rn S044 corpus/` shows no other `corpus/knowledge/` note citing S044, so used-by is
  not incomplete for knowledge notes. The Gate row at lessons:50 is the opening record, not
  a used-by entry (same convention as S039/S040: `corpus/lessons/round-16.md:119`).
- The opening receipt exists and records the same 25-word quote and the attached-HEAD lane
  observation; no newer source receipt contradicts it.

## Dependency: does the knowledge note actually depend on S044?

Paths in `corpus/knowledge/jj-branch-anchor-r17.md`:

- `:1` header lists S044/S045/S046/S047 plus JjAuditMori F3/F4 and JjTrialMori.
- `:9` “A detached HEAD still names a valid commit, but that commit need not be on the lane bookmark.”
- `:15-19` resolver order (attached symbolic HEAD → `origin/HEAD` → unique master/main) and
  “that fallback is not a branch-identity proof”.
- `:25` S046 is cited inline for status-1 vs other-nonzero; `:38` S045 inline for update-author.

S044 supports the premise that under colocation Git HEAD is **usually** detached, which is why
the resolver's first step can fail and why the fallback exists. It does **not** state that the
detached HEAD commit may be off the lane bookmark, nor how `refs/heads/<branch>` maps to a jj
bookmark: the page says “TODO: Describe how branches are mapped”, and its only documented
disagreement is the conflicted-branch caveat. The note's off-branch hazard is measured in
JjAuditMori F3 (and the resolver-status semantics are S046/S047). Therefore: **used-by is
legitimate but thin — S044 is load-bearing for the detached-HEAD premise and not for the
central branch-identity claim; it is not purely decorative.** No correction to the note is
warranted by this audit, but a reader must not cite S044 as proof that HEAD can diverge from
the lane bookmark.

## Residuals / unknowns

1. [info] `teaches` clause 2 is an entailment, not page text; if the registry requires literal
   teaches cells, it is over-distilled. The first clause is literal and hedged.
2. [info] Anchor lists the “Detached HEAD: Yes.” feature row alongside the actual quote site;
   a reader scanning only the feature row will not find the quoted sentence.
3. [info] `latest` alias with no pinned jj version; a future release can change wording, and
   only `on-release` recheck + the access date constrain drift. No archived page digest is
   retained in corpus [UNKNOWN whether one exists elsewhere].
4. [observed, incidental] At audit time `git symbolic-ref -q HEAD` in the lane returned rc1
   (detached), while `build/SrcJjGitCompat.md` recorded an attached `refs/heads/master` at
   opening. These are time-stamped environment observations; the change is consistent with
   the page's “usually” hedge but is not used here as source or measurement evidence.
5. Local `jj --version` = `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`; the page does not
   state which release `latest` served today [INFERENCE: page tracks the newest release docs].

## Commands run (read-only; no probe reruns, no writes outside this report)

| Command | rc | Output |
|---|---|---|
| `curl -sS -L -o /dev/null -w 'http=... final=...' https://docs.jj-vcs.dev/latest/git-compatibility/` | 0 | `http=200 final=https://docs.jj-vcs.dev/latest/git-compatibility/` |
| `curl … \| python3` (strip tags, normalize whitespace, count) | 0 | `occurrences 1 words 25`; `hedge_will_usually True`; `feature_row True`; `branches_todo True`; `conflict_disagree True` |
| `jj --version` | 0 | `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` |
| `git symbolic-ref -q HEAD` | 1 | empty (detached at audit time) |
| `grep -rn S044 corpus/ .ufo/waves/round-17/` | 0 | row S044 at `corpus/SOURCES.md:50`, Gate at `corpus/lessons/round-17.md:50`, note header at `corpus/knowledge/jj-branch-anchor-r17.md:1` |

## Scope limits

No source-registry edit, no corpus edit, no other report touched, no VCS mutation, no package
transaction, no background job, no live journal query, no credential/transcript read. No tool
installed or updated. This report attacks evidence only; L1 is the sole integrator and judge.
