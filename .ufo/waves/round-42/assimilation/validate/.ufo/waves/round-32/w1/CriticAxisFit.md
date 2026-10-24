# CriticAxisFit — round-32 claim-design review

Read-only advisory review; no admission or canonical-runtime judgment. Paths below are lane-relative unless they start `../` or `/`. Existing C0 outputs are cited, not re-executed.

## Axes and short answers

- **Freshness:** live re-verification and honest drift/unreachable disposition. **Calibration:** conclusions and provenance no stronger than evidence. **Depth:** substantive source support, not topic-token overlap. **Coverage:** the actual dependency set reached. **Operability:** reproducible counter behavior. **Adjacency:** keep the lane-local reviewer distinct from outside judgment. Definitions: `../AXES.md:11-16,20-23,27-38`.
- Freshness is the appropriate surface-based name; it also contributes to the quality learning trend. One claim is permitted. The serious risks are incomplete source-chain rechecks and treating an integrator-writable reviewer label as authenticated semantic evidence; details below.

## F1 — High: first-URL rechecks can miss the proposition being re-verified

**Counterexample:** S117's frozen URL is the tags listing, while its teaches cell asserts changes to message grammar across releases and width-5 percentage formatting. The listing establishes tag-to-commit mappings, not those code facts (`.ufo/waves/round-32/c1-population.json:246-251`). Its original source cell deliberately includes releases and multiple `main.c`, `kill.c`, `msg.h` and README URLs (`corpus/SOURCES.md:123`).

**Evidence tested here:** `/fast/scratch/hyaku/mori-r32/CtlPositive/lane/corpus/evidence/recheck-r32/S117.src:1-50` contains tag names, archive links and commit identities. A read-only search of that complete copy for `mem avail|mem <=|sending|escalat|PRIPCT|space.padded|width.?5` returned `No matches found`. C0 itself explicitly says this quote supports tag provenance only, not the teaches-cell grammar/percentage claims (`.ufo/waves/round-32/c0/CtlPositive.md:35-37`), yet its synthetic receipt yields `rows_ok=3/34`, including S117 (`:65-70`). This is a mechanical positive control, not a semantic positive control.

S058 similarly combines rev-list and diff-tree but freezes only rev-list; S128/S149 combine two manuals and kernel comparisons but freeze only the adjustment manual (`corpus/SOURCES.md:64,134,155`; `.ufo/waves/round-32/c1-population.json:166-171,254-275`).

**Impacted axes:** freshness, depth, calibration.

**Smallest safe correction:** preserve the frozen population and predicate; supplement the evidence with the actual supporting dependency files and ask the real reviewer to assess the full teaches propositions. A tags-only quote must not be presented as re-verifying grammar. If the frozen row requirements cannot honestly be met, record the miss rather than replace the population URL or bless a narrower fact. Distinguish a pre-existing citation-chain gap from an observed upstream change; do not invent drift to obtain a convenient verdict (`.ufo/waves/round-32/contract.md:5-6,23-27,31-44`).

## F2 — High, conditional trust tradeoff: C0 does not establish shortcut resistance at 34/34

**Observed, not inferred:** do-nothing at both base and freeze gives `rows_ok=0/34`, `new_ok=0`, `C1=unmet`; fabricated 34-row junk also fails substantive checks (`.ufo/waves/round-32/c0/CtlDoNothingJunk.md:82-103,114-119`). Thus an unchanged tree or bare id/label table does not reach the target in the recorded runs.

**Strongest local counterexamples:**

- S068's real sentence `The Python UTF-8 Mode is enabled by default.` passes the topic test although it says nothing about stat/lstat. Four such unsupported rows fail only `judge`; adding forged reviewer metadata changes the same four rows to `rows_ok=4/34` (`.ufo/waves/round-32/c0/CtlOffTopic.md:50-58,114-130`).
- Forging only a receipt fails; adding an editable dispatch entry makes all three supplied rows pass (`.ufo/waves/round-32/c0/CtlForgedJudge.md:96-113`). The implementation authenticates neither actual dispatch nor actual reviewer authorship (`.ufo/waves/round-32/count-c1.py:199-217,266-271`).
- A quote cut inside `unprotected`, page furniture, and a one-line quote-only source copy count when the synthetic judge agrees (`.ufo/waves/round-32/c0/CtlNormaliser.md:35-40,65-72`). Fake unreachable transcript content also passes its existence test for S056; only the missing judge rejects that row (`.ufo/waves/round-32/c0/CtlDoNothingJunk.md:130-135,158-160`).

Every reported full C1 result remains unmet, but the forged/off-topic controls intentionally omit most population rows and the new source. Their global failure is therefore not evidence that the supplied bad rows were rejected (`.ufo/waves/round-32/evidence/c1-controls.txt:17-23`).

**Answer about 34/34:** no full 34/34 shortcut is demonstrated. [INFERENCE] The row checks are independent, and id-indexed real-quote snippets plus forged matching judge metadata could extend the demonstrated per-row false accepts wherever those snippets pass R2/R3; no additional cross-row semantic check appears before the final equality test (`.ufo/waves/round-32/count-c1.py:221-271,317-323`). An id alone cannot substitute for a quote actually found at that id's live URL. Do not report either universal immunity or an exercised 34/34 exploit.

**Impacted axes:** freshness and calibration; false provenance can also undermine depth.

**Smallest safe correction:** enforce the already-declared trust boundary, not a post-data counter amendment: preserve the actual reviewer's report byte-exact, independently retain its delivered origin, and require review of full copies, quotation boundaries, teaches support, failed-fetch evidence and substantive corrections. The contract expressly discloses integrator-forged dispatch plus receipt as outside its protection (`.ufo/waves/round-32/contract.md:63-65`; `evidence/c1-controls.txt:25-32`). A canonical judgment must be given that limitation, not a claim that C0 closed it. R4 is lane-local evidence, not the outside discernment/admission authority (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:40-46`).

## F3 — Medium: frozen selector is transparent, but its description overstates completeness and immutability

The declared selector is **mined + first source-cell URL only + syntactic pin exclusions**, not every mutable dependency of every mined row (`.ufo/waves/round-32/c1-population.json:2-3`). Relevant inclusion/exclusion examples:

| Case | What actually happens and why | Evidence |
|---|---|---|
| Bare API listings | S117 `/tags` and S137 `/commits?path=main.c` are included: their request URLs contain no selected tag/commit, even though returned items and anchors name commits. | `c1-population.json:246-267` under `.ufo/waves/round-32/` |
| Tag-specific API listings | S131 `/git/trees/v1.9.0` and S151 the same path with `?recursive=1` are excluded by the `/v<digit>` path convention, not merely because they are API responses. | `corpus/SOURCES.md:137,157`; population `:3-278` |
| Moving documentation | systemd `/man/latest/`, jj `/latest/`, and Python `/3/` pages are included; version text in an anchor does not pin the fetched URL. | population `:22-51,62-82,102-114,198-226` |
| Explicit commit identities | S004/S066 have full commit URLs; S125 has the short commit segment `157ee255`; these are excluded by the hex conventions. | `corpus/SOURCES.md:10,72,131`; population `:3` |
| Release-oriented objects | S003/S011 use named tags; S146 uses `man-pages-6.20.tar.xz`; S169-S172/S174 use `?h=man-pages-6.20`. They are excluded by tag-path, release-tarball or query rules. | `corpus/SOURCES.md:9,17,152,175-178,180`; population `:3` |
| Mixed/versioned specification | S060 starts with `/spec/v1.0/provenance`, so is excluded by the version-looking path convention, although the same source cell explicitly includes unpinned in-toto `blob/main` files. | `corpus/SOURCES.md:66`; population `:3-278` |
| Additional mutable dependencies | S058's second URL, `https://git-scm.com/docs/git-diff-tree`, is not fetched by the frozen first-URL row. | `corpus/SOURCES.md:64`; population `:166-171` |

S060's live specification also links directly to in-toto `blob/main/spec/v1/statement.md` and `resource_descriptor.md`: https://slsa.dev/spec/v1.0/provenance, Schema and BuildDefinition. A version-looking documentation path is not evidence of a Git commit pin. More fundamentally, the assertion that tag URLs' bytes **cannot** drift is too strong: Git documents replacing a tag with `-f` and the hazards of published re-tagging (https://git-scm.com/docs/git-tag, “On Re-tagging”). No tag movement is alleged here.

**Impacted axes:** freshness, coverage and calibration.

**Smallest safe correction:** append an exclusion/risk explanation, without changing the frozen 34: call this the selected **first-URL, conventionally unpinned** population. Record tag movement, versioned-page edits and secondary-URL dependencies as unmeasured, rather than declaring them impossible. A predeclared bounded subset is not post-data cherry-picking, but it cannot substantiate freshness of the entire source dependency graph (`../.ufo/prompts/mori-round-32.md:346-347,351,357-365`).

## F4 — Medium: the baseline's “last opened when added” assertion is false

The contract says every selected row was last opened in the round that added it (`.ufo/waves/round-32/contract.md:17-19`). S014/S015 were opened on 2026-10-19 in their existing catalog rows (`corpus/SOURCES.md:20-21`), then explicitly reopened in round 13 on 2026-10-20 (`corpus/lessons/round-13.md:47,55-62`); S015 is again marked reopened in round 14 (`corpus/lessons/round-14.md:58`). The corpus index already calls S013/S014/S015 reopened (`corpus/README.md:39`).

**Impacted axes:** calibration and freshness provenance.

**Smallest safe correction:** append a precision note: the new deliverable is a population-wide, round-32 live recheck with committed copies and bound review, not the first reopening of each row. Keep the old opened date as original provenance; do not infer last verification from it. The new round-specific after-state still has a distinct surface even after this correction.

## F5 — Low: anti-loop rationale misstates the rule; C1 does not require an exception

The contract turns two rounds on depth/operability into exclusion of both axes (`.ufo/waves/round-32/contract.md:10-12`). The campaign's actual trigger is **same axis+surface claim OR same routed defect class for three rounds running**, followed by a move to a different frontier area—not a two-round ban on an axis (`../.scratch/goal-20261022-hyaku-12h.md:168-173`; the round prompt references that campaign file at `../.ufo/prompts/mori-round-32.md:144-153`).

The declared sequence is round 29 calibration + operability (A2 cases), round 30 depth (invocation scope) + operability, round 31 depth (watchdog identity) + operability (blind-list parser): `SCORECARD.md:1783-1788,1808-1814,1834-1840`. Merely repeating depth twice does not establish that trigger; repeated operability needs surface/defect-class analysis, not just its label. Freshness is absent from all three declaration sets and tied lowest at 5 (`SCORECARD.md:12-14`), so selecting live source rechecks neither needs a lowest-axis waiver nor repeats those declared surfaces.

**Impacted axis:** calibration of the design rationale; no claim of saturation is warranted from this sequence alone (`../AXES.md:33-38,66-73`).

**Smallest safe correction:** append the exact three-round axis+surface history and state that freshness is a different live-source surface. Do not install a second, broader anti-loop authority in the frozen contract.

## F6 — Informational: freshness and one claim are legitimate choices

`../AXES.md:14` defines freshness as claims re-verified against live surfaces with stale items flagged/fixed. C1 names mutable source rows, a live reopen, supporting quotes and a current/drifted/unreachable disposition, rather than naming its axis after `34` (`.ufo/waves/round-32/contract.md:15-29`). This differs from replaying an existing rule on fixtures; the live check prevents a sourceless echo from being sufficient (`count-c1.py:247-255`; C0 echo result at `evidence/c1-controls.txt:14-15`, both under `.ufo/waves/round-32/`). Freshness is also quality-trend work, not an alternative to quality (`../AXES.md:20-23`). This gives no separate coverage/depth gain merely from row counts.

One claim lies within the binding 1–3 range (`../AXES.md:27-33`; `../.ufo/prompts/mori-round-32.md:9-19`). “Prefer 2” is not “require 2” (`../.ufo/prompts/mori-round-32.md:350`); the contract records why it declined a second calibration claim (`.ufo/waves/round-32/contract.md:12-13`). Smallest safe action: keep one honest distinct-axis claim; do not manufacture another or add it after data.

## F7 — Medium: new-source and correction checks are weaker than their prose obligations

The new-source branch checks a novel URL string, mined/admit labels, copied-byte hash, quote in the copy and an id mention in README; it neither live-fetches that URL nor includes the Gate section in R4's judged-section hash (`.ufo/waves/round-32/count-c1.py:192-216,272-316`). [INFERENCE] A fabricated new source with internally consistent copy/quote/labels could satisfy `new_ok>=1` without opening that source. This limitation is separate from the declared forged-R4 trust limit; it does not bypass the 34 row checks.

Likewise R5 checks an added `Round32`/id line, not whether it corrects stale knowledge. C0's explicitly control-only sentence saying no drift is asserted satisfies it in every required file (`.ufo/waves/round-32/c0/CtlPositive.md:53-57,96-103,134-136`).

**Impacted axes:** depth, freshness and calibration.

**Smallest safe correction:** retain actual new-source fetch evidence and review the method citation and every correction substantively before presenting them as sourced/corrected. Do not describe these marker checks as proof of those facts, or silently strengthen the frozen counter after data (`.ufo/waves/round-32/contract.md:5-6,28-29,60-65`).

## F8 — Medium reporting limitation: 34/34 is not 34 currently supporting sources or an offline invariant

The predicate permits `unreachable` rows, including no source-body quote, to count after failed live fetches and judge agreement (`.ufo/waves/round-32/count-c1.py:237-267`). Its result also depends on the counter's live network calls, not solely on committed bytes (`:116-120,253-265,320-323`). Thus the one-command requirement is met as an executable command shape, but an identical revision is not an offline, time-invariant after-value (`../.ufo/prompts/mori-round-32.md:343-345`).

**Impacted axes:** operability and calibration.

**Smallest safe correction:** publish the exact live run's revision, timestamp and current/drifted/unreachable split, alongside its committed stdout; say “34 rows adjudicated under the frozen checks” rather than “34 source teachings confirmed current.” Never upgrade a failed later live check to a pass from an older receipt. Whether that live reproducibility tradeoff meets closure remains for the canonical judge.

## Exercised evidence and boundaries

- Read/grep inspection only; no new counter, seat-check, build, test, judge or alternative runtime invoked. The direct S117 content search is described in F1. C0 results remain attributed to their original reports.
- Bounded read-only command: `timeout 120 prlimit --as=1073741824 --cpu=110 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 641a6e86ecc60634d215c0a47ab86c47661abf86 -- corpus/SOURCES.md` returned no output; catalog examples matched the frozen base at inspection time.
- Tool installs/updates: none. No subagents, background jobs, services, lane VCS writes or source edits. Only this assigned report was written; the one shell command completed synchronously.
