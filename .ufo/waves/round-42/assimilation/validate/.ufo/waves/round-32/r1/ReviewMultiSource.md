# R1 residual — independent second opinion on S058, S117, S128, S149, S071

Seat: `MoriR32A2.ReviewMultiSource` (leaf; no subagents, no background jobs). Data under review: lane commit `837b2802c60a6e37a9d462f2354107307fba6ef1`.
Question per row: does the quoted live page carry the row's `teaches` cell, and is verdict `current` honest under the contract's definition ("the live page still supports the teaches cell", contract.md:25)?

## Method (all checks offline; zero live fetches this seat)

- Frozen inputs: `.ufo/waves/round-32/contract.md` (C1, verdict definitions at :23-27), `.ufo/waves/round-32/count-c1.py` (row checks R1-R5, docstring :11-29), `.ufo/waves/round-32/c1-population.json` (rows S058/S071/S117/S128/S149), controls `.ufo/waves/round-32/evidence/c1-controls.txt`.
- Recheck table: `git show 837b2802…:corpus/lessons/round-32.md` — S058 line 41, S071 line 47, S117 line 51, S128 line 52, S149 line 54. Section identical at tip a45850f0 (`count-c1.py --section-sha` = `251bf664717bbdf4` at both revs).
- Base source rows: `git show 641a6e86…:corpus/SOURCES.md` — S058:64, S071:77, S117:123, S128:134, S149:155.
- Copies hashed in place: `S058.src` 6eca09d9…, `S071.src` 96ad0ef9…, `S117.src` 423c4361…, `S128.src` = `S149.src` 769edf3b… (byte-identical, `cmp` exit 0). All equal the shas in the table rows.
- Normalised text via the counter's own rule: `python3 .ufo/waves/round-32/seat-check.py text <copy>`; every count and quote check below ran on that output in my scratch dir `/fast/scratch/hyaku/mori-r32/MoriR32A2.ReviewMultiSource/`.
- No tool installs (nothing missing; pacman untouched). No api.github.com fetch, no live fetch of any URL — S117 evidence is the committed copy only.

## S058 — git-rev-list(1) (+ git-diff-tree(1))

Teaches (SOURCES-base.md:64, verbatim): "Commit ordering: --topo-order shows no parent before its children and --reverse flips the output, so rev-list --reverse --topo-order base..tip lists ancestors first; the default is only reverse chronological. Diff-tree: -r recurses subtrees; merges need an explicit <commit>^1 <commit> two-tree form because the doc states merge diffs are not shown by default under --stdin; a root commit needs --root; --name-status is the status-bearing listing."

- Carried by the receipted page (`S058.src` normalised): all three table quotes verbatim; `--topo-order`, `--reverse`, `--first-parent`, "reverse chronological", "2.56.0" — 1 occurrence each.
- NOT carried: the whole Diff-tree half. `--root`, `--name-status`, `--name-only`, `--no-commit-id`: 0 occurrences. The only `diff-tree` hit is the EXAMPLES pipeline "git rev-list HEAD | git diff-tree --stdin --format=medium -p"; the "merge diffs are not shown by default under --stdin" rule is a diff-tree-page sentence.

**Finding 1 — MEDIUM: S058's `current` is receipted on half the teaches cell.**
The second source URL (git-scm.com/docs/git-diff-tree) is a live, unpinned docs page; it is not the population url, so R1-R3 never look at it (count-c1.py:11-20). The only currency evidence for the Diff-tree half is w1/Recheck058.md §6 — an out-of-band fetch (sha256 72cce597…) saved in the seat's scratch, NOT committed under corpus/evidence/recheck-r32/ and not hash-bound anywhere at tip. I verified that scratch copy still carries all five diff-tree facts (`-r` "Recurse into sub-trees", `--root` "big creation event", "does not show differences for merge commits", `--name-status` definition, two-tree synopsis `<tree-ish> [ <tree-ish> ]` — 1 each), so the seat's conclusion is right today; but the verdict recorded in the table rests on evidence covering only the ordering half. Under the literal contract definition the rev-list page does not support the Diff-tree clauses; `current` is honest only under a source-set reading. This is exactly the pre-data false-accept class the controls handed to R4 ("a real on-topic-token sentence that does not support the teaches cell", c1-controls.txt). The judge wave must decide it explicitly; the counter cannot see it.

## S117 — earlyoom tags API

Teaches (SOURCES-base.md:123, verbatim): "The `mem avail` threshold wording was introduced in v1.8 and is unchanged in v1.9.0, so a v1.7-era invocation prints `mem <=` and never the contract's threshold line; the action and escalation prefixes are stable across v1.7–v1.9.0 while their trailing fields change, so the version line, not the action line, identifies the grammar; percentages are printed through a width-5 field, so a single-digit threshold is space-padded."

- Carried by the receipted page (`S117.src` normalised): exactly the tag→commit identity layer — 29 `"name"`/`"commit"`/`"sha"` triples; newest-first order starts v1.9.0, v1.8.2, v1.8.1, and the v1.8 and v1.7 entries are present; all three quoted JSON slices verbatim.
- NOT carried: every wording/format clause — `SIGTERM`, `SIGKILL`, `escalating`, `mem avail`, `PRIPCT`, `main.c`, `width`, `releases`: 0 occurrences each. The grammar, prefix-stability, v1.7 `mem <=` and width-5 claims live in the raw.githubusercontent files at tags (source-cell URLs 3-10), all tag-pinned.

**Finding 2 — LOW-MEDIUM: S117's quotes carry zero teaches tokens; the topic gate passes via anchor tokens only.**
Counter tokens of the three quotes = {name, zipball, https, api, github, repos, rfjakob, earlyoom, refs, tags, tarball, commit, sha, ddaf}; the teaches cell contains none of them — R2's "share at least 2 distinct content tokens with p.teaches + p.anchor + p.scope" (count-c1.py:14-17, gate at :251-252) is met only through anchor/scope tokens (`tags`, `commit`, `ddaf`, `earlyoom`). That is the "anchor boilerplate counted as topic tokens" shape the controls documented as a counter false-accept that only R4 can catch (c1-controls.txt). The verdict itself is nonetheless honest, via a chain the seat states (w1/Recheck117.md §3): the row's only drift-capable surface is the tags listing; it is unchanged in exactly the particulars the claims depend on (v1.9.0 → 202d4db0…, v1.8 and v1.7 still published), and the wording claims are pinned to those commits, whose bytes cannot drift while the mapping holds. Recommendation to the judge: record that the grammar/width clauses are re-certified transitively (mapping unchanged), not observed on the page.

## S128 and S149 — oom_score_adj(5) man page (+ kernel code)

Teaches S128 (SOURCES-base.md:134, verbatim): "The two files are different contracts: oom_score_adj is the writable -1000..+1000 preference whose value the kernel scales by totalpages/1000, oom_score is a read-only [0, 2000] export folding that preference in, and the page's inheritance and privilege sentences belong to the legacy oom_adj file, not to oom_score_adj."
Teaches S149 (SOURCES-base.md:155, verbatim): "supersedes S128 — … the pages do place them only inside the oom_adj paragraph (adj:145-149), but that placement is a documentation gap, not an absent kernel rule, because the kernel still copies oom_score_adj and its floor at fork (kernel/fork.c:1768-1769,1949-1966) and refuses an unprivileged write below oom_score_adj_min (fs/proc/base.c:1131-1133). The two files are different contracts: oom_score_adj is the writable -1000..+1000 preference whose value the kernel scales by totalpages/1000 (mm/oom_kill.c:232-234), oom_score is a read-only [0, 2000] export folding that preference in (fs/proc/base.c:596-597), and the pages' 3% root clause (adj:86-88) has no implementation in v7.2 oom_badness (mm/oom_kill.c:199-237)."

- Carried by the receipted page (`S128.src` = `S149.src`, normalised): all four quoted sentences verbatim (range; "added to the badness score"; inheritance+privileged; "root processes are given 3% extra memory over other tasks"). The placement claim is real: `inherits` ×1, `privileged` ×1, `CAP_SYS_RESOURCE` ×1, all inside the oom_adj HISTORY paragraph; `oom_adj` ×5; footer "Linux man-pages 6.19" still served; "Its value is scaled linearly with oom_score_adj" keeps the two-contracts contrast alive.
- NOT carried: "kernel scales by totalpages/1000" (`totalpages` ×0) and "read-only [0, 2000] export" (`2000` ×0). The first is pinned v7.2 code (oom_kill.c:232-234); the second is split between the unchecked score-page URL and pinned base.c:591-594.

**Finding 3 — LOW: S128/S149 verdicts rest on pinned code plus one unchecked mutable URL.**
The kernel-code clauses are drift-proof (tag-pinned), so unlike S058 nothing unchecked here can silently drift; but the score-page clause ("oom_score is a read-only … export") is the S058 shape in miniature: a second live man7.org URL named in the source cell, absent from the population url cell, never fetched by R3, with no committed copy. The verdicts are defensible for what the receipted page bears; the judge should note the score-page clause is unchecked this round — w1/Recheck128149.md §6 says the same. Note: both rows sharing one byte-identical copy is rule-compliant (one copy per id), and each row receipts its distinct clause (S128 the "added" wording, S149 the 3% clause); no defect there.

## S071 — Kubernetes Controllers page

Teaches (SOURCES-base.md:77, verbatim): "Name the declared set (dispatch members) and the observed set (reports) separately; mori observes the gap and never acts to close it."

- Carried by the receipted page (`S071.src` normalised): both quotes verbatim; "desired state" ×12, "current state" ×8, "spec field" ×1; the last-modified stamp "September 01, 2024" still matches the anchor.
- NOT carried: the mori clause — `never acts` ×0, `dispatch` ×0 — and the page stays acting-themed: "The controller might carry the action out itself" and "Other control loops can observe that reported data and take their own actions" both present.

**Verdict: honest.** The second clause is lane doctrine with no source URL to drift from; the row's scope cell disclaims it ("the page describes acting controllers, not observe-only ones") and S074 exists to record the acting wording. Clause 1 is verbatim-current. `current` is honest under either reading of the contract definition.

## Finding 4 — STATUS: R4 is still open at the reviewed commit and at tip

`.ufo/waves/round-32/judge/JudgeRecheck.md` does not exist at `837b2802…` nor at tip `a45850f0…` (`git show <rev>:<path>` rc=128 both). Frozen counter `--no-live` at both revs: `recheck_rows=34 header_ok=True section_sha256=251bf664717bbdf4 judge_ok=False judge_agree=0`, `rows_ok=0/34` with every failure being `judge` alone (R1/R2/quote checks pass for all 34; verdicts 33 current + 1 unreachable; R3 skipped in diagnostic mode), `new_ok=3 new_failures=none`. Not a defect of the five rows' data — but until the receipt lands, C1 is unmet by construction, and R4 is the only check that can catch the Finding 1 and Finding 2 shapes. Hand those two to the judge wave verbatim.

## Root cause (one sentence)

The verdict definition is page-scoped ("the live page", contract.md:25) while the teaches cell is row-scoped over a multi-URL source cell and the frozen selector pinned only URL #1, so compound rows (S058, S117, S128/S149) can be `current` only under a source-set reading — and their off-page parts are receipted to different standards: tag-pinned parts are drift-proof, unpinned parts (S058 diff-tree, S128/S149 score page) are unchecked or uncommitted.

## Residual risk and verification gaps

- I re-fetched nothing (bound: prefer committed copies; never re-fetch S117/S137). R3's live re-fetch of these five rows is unexercised by me; it was exercised by seat-check during the wave and would be by the counter's live mode.
- The S058 diff-tree evidence (sha 72cce597…) lives only in `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck058/` and is ephemeral; only the integration owner can commit it as evidence.
- S137 shares S117's api.github.com surface pattern but is outside this assignment; if the mapping-stability chain is judged honest for S117, S137 needs the same scrutiny.
- Population rows and table rows verified only for the five in-scope ids.

Tooling: no installs or updates this seat (curl, python3, sha256sum, git already present).

Report: .ufo/waves/round-32/r1/ReviewMultiSource.md
