# CriticClaimC1 — round-33 claim-design review

Advisory findings only: no row judgment, admission, integration, runtime invocation, or counter execution. The operative claim is P-C1-A1 with unchanged R-J, not the original counter alone (`.ufo/waves/round-33/contract.md:103-134`). Predictions below are explicitly marked [INFERENCE].

## Axes and direct answers

- **Depth** is the appropriate proposed axis for genuinely new, sourced disk-accounting decisions in `corpus/knowledge/` and `SKILL.md`; it is not established merely by a new filename, new URLs, or ten rows. The canonical definition requires actionable technical detail without filler (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:9-16`; `.ufo/waves/round-33/contract.md:16-22`; `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-33.md:361-365`).
- **Calibration** is exposed by the inaccurate novelty baseline, by treating receipt shape as semantic support, and by overstating control discrimination; **operability** by non-hermetic replay; **freshness** by live URL dependence. These are review dimensions, not additional claimed moves (`SCORECARD.md:10-15`; `.ufo/waves/round-33/contract.md:26-42,73-77`).
- **Coverage** must not be credited as implementing FR6: its current boundary explicitly defers a two-sample census rate until the latency budget is met. **Adjacency** remains detection/report only, never block-setting or host remediation (`corpus/README.md:340`; `PROVINCE.md:12-16,49`).
- The subject does differ from rounds 31 and 32: round 31's new knowledge surface was FR5 watchdog identity, while round 32 rechecked source freshness. Reusing a decision-table format is not itself an anti-loop violation; re-documenting already-held disk facts without new decisions would be (`corpus/lessons/round-31-verifier-spotcheck.md:81-107`; `corpus/lessons/round-32-verifier-spotcheck.md:64-98,130-137`; prompt `:361-365` above).
- The after-state has one Boolean label and one command, but it is **not a function of committed bytes alone**, and semantic validity still requires an actual independent reading. See findings 2, 3 and 5 (`.ufo/waves/round-33/contract.md:35-41,73-75,125-127`).

## Ranked findings

### 1. HIGH — The target can reward a glossary rather than a new write-rate decision surface

**Exact phrases attacked:** “how to turn /proc/diskstats into a disk write rate (FR6)” and “at least 10 pairwise-distinct data rows” (`.ufo/waves/round-33/contract.md:24-30`); “no two observation cells are equal” and the six-word-copy prohibition (`:119-123`).

**Counterexample/evidence:** The existing C0 fixture has topic-label observations and a universal `report` verdict, explicitly defined to mean restating a source. Its ten readings cover completed writes, sectors, layout, sector unit, cgroup keys/writeback, process syscall/byte accounting, caches and bio flags; it supplies neither a two-sample rate calculation nor a decision about comparable samples (`/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo/corpus/knowledge/disk-write-rate-r33.md:7-20`; committed report `.ufo/waves/round-33/c0/CtlShortcutIds.md:75-86`). The original counter accepted this honest-receipt fixture; A1 rejects its baseline `69e5a0f23fb6` **only** for `reading_copies_quote` (`.ufo/waves/round-33/c0/CtlShortcutIds.md:34-62`; `.ufo/waves/round-33/evidence/c1-controls.txt:65`).

[INFERENCE] Rephrase those readings to break the six-word overlaps while preserving their meaning, then obtain a genuine fresh receipt. That repairs the named A1 failure without adding any rate interpretation. Likewise, ten semantic duplicates with genuinely different labels and paraphrases are not rejected by normalized textual inequality; normalization is not a test of distinct decisions (`.ufo/waves/round-33/count-c1-a1.py:86-91,175-203,268-278`). These are unrun controls, not claimed passes.

**Impacted axes:** depth and calibration. URL/hash diversity is not diversity of knowledge: the predicate checks registration/byte differences, not whether the fact was already held or whether the source is another presentation of the same authority (`.ufo/waves/round-33/count-c1-a1.py:207-258`).

**Smallest safe correction:** Keep the frozen predicate unchanged. Make the real table earn its proposed depth through new, quote-supported decisions about the named disk-accounting hazards, and distinguish those from retained baseline facts. Do not equate `C1=met` with a depth move absent that substantive difference. A counter pass obtained solely by rephrasing already-held rules is the quality-only case in addendum §9, not permission for a depth label (`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-33.md:361-365`). A future counter design could enumerate semantic cases before data; this round cannot retrofit them into P-C1-A1 (`.ufo/waves/round-33/contract.md:134`).

### 2. HIGH — “One command over committed bytes” is defeated by measurement-time networking

**Exact phrase attacked:** “the URL fetched at measurement time hashes to the same sha256” (`.ufo/waves/round-33/contract.md:35`), against addendum §9's “one command over committed bytes” (`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-33.md:343-345`).

**Evidence/counterexample:** The counter performs up to three live curl attempts per URL and makes `fetch_ok != n` a claim failure (`.ufo/waves/round-33/count-c1-a1.py:94-99,239-258`). [INFERENCE] The identical committed revision can therefore fail after a transient network/upstream availability change, even with unchanged and correct committed copies. Pinned raw URLs reduce mutation risk; they cannot make live availability a committed byte.

**Impacted axes:** operability, freshness and calibration. This is an explicit reproducibility tradeoff, not evidence that the disk knowledge disappeared.

**Smallest safe correction:** Do not remove or bypass the frozen live condition now. Report the exact measured revision and fetch outcome separately from offline copy integrity, without calling the command hermetic. A prospective design should separate committed-byte reconstruction from live recheck. Closure must retain the current condition rather than silently accepting an offline substitute (`.ufo/waves/round-33/contract.md:60-64,134`).

### 3. HIGH — An entry-only judge hash leaves the judged evidence bundle unidentified

**Exact phrase attacked:** “judged-sha256: line equal to the sha256 of the entry” (`.ufo/waves/round-33/contract.md:38-40`).

**Evidence/counterexample:** The receipt hash binds only the entry; the counter independently reads the current revision's registry, Gate, copies and dispatch. Its semantic proxy is a six-word span anywhere in a cited new copy (`.ufo/waves/round-33/count-c1-a1.py:124-126,204-245,279-313`). [INFERENCE] After an honest judgment, changing a cited source's URL/Gate/copy while retaining its id and a qualifying span can leave `judged-sha256` valid although the judge never read the replacement evidence. Fresh hash consistency is not proof that these were the judge's inputs. This mutation was not run here.

The existing stronger adversarial witness changes a receipt rather than its inputs: forged junk commit `5ae82bab4037` is recorded `C1=met` under A1 while honest junk `be0bad2a9a0f` is `C1=unmet` (`.ufo/waves/round-33/evidence/c1-controls.txt:61-63`). The contract properly declares receipt integrity uncounted; it must remain visible rather than being promoted to a semantic guarantee (`.ufo/waves/round-33/contract.md:73-75,129-134`).

**Impacted axes:** calibration and depth; provenance of a real judgment can become false without changing the table.

**Smallest safe correction:** Dispatch the real judge against an immutable revision containing the final entry, registry, Gate and copies; retain that revision in the receipt/transcript and demonstrate that its relevant evidence bytes are the landed ones. Additional provenance evidence need not change the frozen counter. If evidence changes, obtain a new real judgment, not merely a regenerated entry hash. A future mechanical design should bind the complete input manifest.

### 4. MEDIUM — The novelty baseline is partly false, and filename absence cannot establish it

**Exact phrases attacked:** “the lane has the census's since-boot average only”; “no entry states the sector unit”; “The command that shows it unmoved” (`.ufo/waves/round-33/contract.md:17-21`).

**Direct local falsifier:** `surfaces-r7.md` already states `sectors_written × 512 / uptime_s`, identifies field 10, and gives the exact 20000×512/500 byte-rate example (`corpus/knowledge/surfaces-r7.md:122-138`). It also records a two-sample 13984-sector/10-second calculation, its latency deferral, and non-fleet/non-burst limitations (`:140-157`). Thus “only” omits held interval-rate knowledge, and the sector-to-byte multiplier is already present even if a new source will give it a stronger explanation.

The existing S033 is not merely a field list: its teaches cell already says cumulative counters need boot/device-reset context, although it is queued rather than mined (`corpus/SOURCES.md:39`). Do not confuse an unmined source lead with an admitted knowledge entry, but do not erase its held content either.

Historical provenance check: `timeout 20s prlimit --as=536870912 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/mori-shokunin --no-pager diff 7d382043016e8854e3be2ee523a095b409c3d8a1 fdf4371fb6d5f7c4e8b1f29f4735afaead5d45c9 -- corpus/knowledge/surfaces-r7.md corpus/knowledge/surfaces-r8.md corpus/SOURCES.md` produced **no output**. Those paths were unchanged between entering tip and the A1/control commit.

**Impacted axes:** calibration and depth. The counter's absent-entry branch tests the one new path, not whether equivalent knowledge existed under another path (`.ufo/waves/round-33/count-c1-a1.py:124-138`).

**Smallest safe correction:** Append an explicit baseline correction, preserving the frozen record. Credit stronger sourcing of the multiplier as quality; identify any genuinely added distinctions separately. Retain FR6's implementation/latency boundary (`corpus/README.md:340`; `corpus/knowledge/surfaces-r8.md:75-91`). This does not show that completion, wrapping, topology or version-layout decisions were already held; it defeats the broader absence claim, not every proposed addition.

### 5. MEDIUM — R-J is inspectable, but its semantic boundary still admits two reasonable readings

**Exact attacked text:** “the quotes located”; “state every fact”; “follows from that reading without any further fact”; “any part of which is not so stated”; “with a caveat” (`.ufo/waves/round-33/contract.md:47-50`).

| Ambiguous words | Concrete competing readings / falsifier |
|---|---|
| “the quotes located” | Only the 1–4 Gate excerpts, or any passage the judge can locate elsewhere in the cited copy? A formula present elsewhere but absent from the Gate excerpts separates the readings. The counter accepts its span from anywhere in the copy (`count-c1-a1.py:223-242,299-304` under the same wave directory). |
| “state every fact” | Explicitly stated paraphrases, or facts derived from code/arithmetic? Quotes giving sector units and cumulative counts do not necessarily explicitly state a proposed delta formula or a device-identity continuity assumption. [INFERENCE] A row adding that formula could receive different decisions unless its cited excerpts actually state it. |
| “follows … without any further fact” | Logical consequence versus a reasonable lane reporting policy. A counter description does not itself select an alert threshold, prescribe a sampling clock, or justify a durability claim. Those additions need support; report-only wording must not smuggle them in. |
| “any part … not so stated” | Literal quotation support for the verdict too, versus the preceding clause's allowance for a verdict that follows from the reading. A lane instruction to report a stated counter exposes that scope tension. |
| “with a caveat” | A version qualifier already inside the observation/reading versus a rescue qualifier added by the judge. An unqualified fixed-field-count claim cannot be rescued by silently assuming the quoted version. [INFERENCE] These are different uses of “caveat.” |

**Evidence boundary:** This is a finite manual clause-to-quote review, not a claim that textual entailment is mathematically undecidable. The script enumerates row labels and spans; it does not extract/assert a complete list of the row's factual clauses (`.ufo/waves/round-33/count-c1-a1.py:291-313`). Round 32 demonstrates the consequence of accepting companion-source/absence-of-contradiction reasoning in place of the frozen meaning (`corpus/lessons/round-32-verifier-spotcheck.md:34-56,82-98`).

**Impacted axes:** calibration and depth.

**Smallest safe correction:** Preserve R-J verbatim. Have the real receipt expose each observation/reading clause and its supporting Gate excerpt/locator, with version limits in the row itself. Keep the verdict to a reporting consequence that adds no factual premise. Do not rescue an unsupported clause with background knowledge, a source absent from the row, or a post-hoc qualifier. If an ambiguous case cannot meet the strict frozen wording, report it unsupported rather than inventing a relaxed rule.

### 6. MEDIUM — The A1 controls do not establish honest reachability or saturation

**Exact phrases attacked:** “all negative controls print C1=unmet” and the forged state “also serves as the positive control showing the A1 predicate is reachable” (`.ufo/waves/round-33/contract.md:129-134`).

**Evidence:** The exception is explicitly disclosed, so it is not a hidden contradiction: Part B records forged-receipt `5ae82bab` as the sole met state (`.ufo/waves/round-33/evidence/c1-controls.txt:16-77`). That demonstrates structural reachability, not an honestly judged, semantically valid A1 positive. The original honest glossary baseline fails A1's quote-copy check (`:65`). Several original negatives combine absent sources/judge artifacts with the feature being attacked; their author explicitly warns against treating their rejection as single-fault coverage (`.ufo/waves/round-33/c0/CtlDoNothingLabels.md:22-31,254`).

**Impacted axes:** calibration and operability. This is an evidence gap, not proof that an honest solution is impossible.

**Smallest safe correction:** Describe the positive as a forged structural witness only; do not claim semantic reachability or saturation from it. Retain the already-repaired span/copy/punctuation failures as historical findings, not current A1 defects (`.ufo/waves/round-33/contract.md:112-123`). The L1 can score a genuine A1 positive and focused controls without amending the frozen claim.

## Universal-clause audit

- **Enumerated mechanically:** cited S180+ ids and their registry/Gate/copy/fetch checks; each table row's source existence and lexical overlap; complete row-number receipt coverage; A1 normalized row/observation inequality, six-word runs and every supported-row span (`.ufo/waves/round-33/count-c1-a1.py:175-278,291-313`). These bounded universals have explicit sets.
- **Not enumerated by the counter:** “no entry states …” ranges across prior knowledge but the script reads only the new entry path plus source registry; “every fact” / “any part” have no clause inventory and rely on real judging (`.ufo/waves/round-33/contract.md:19-21,47-50`; counter `:124-138,291-313`).
- **Locator truth is not mechanically enumerated:** the regex consumes a locator but retains only quote text; copy checking searches normalized text anywhere, not at the stated filename/line range. [INFERENCE] replacing a locator with `S180.src:999999` while leaving its real quote/copy unchanged is an unrun single-fault falsifier of locator verification, not of literal quote presence (`.ufo/waves/round-33/count-c1-a1.py:59,223-242`). The real judge must inspect locators.
- **Effective source requirement is stronger than the headline eight:** every supported row needs a span in a cited **new** copy. Consequently all ten minimum supported rows need a new id; eight new-id rows plus two old-only rows cannot supply ten supports (`.ufo/waves/round-33/contract.md:39-41`; counter `:299-312`; `.ufo/waves/round-33/c0/CtlShortcutIds.md:508`). This is not an unenumerated universal, but it is an easy drafting trap.

## Concrete cheap controls and status

1. **Do nothing, sourceless rows, id relabeling:** already recorded unmet, not candidate successes (`.ufo/waves/round-33/evidence/c1-controls.txt:16-21`).
2. **No-rate glossary:** reuse `69e5a0f23fb6`'s ten source-backed topic rows and `report` policy, rewriting only copied six-word runs, then obtain a real judgment. [INFERENCE] This may meet A1 while still skipping the advertised rate-reading work; its current sole failure is recorded at `evidence/c1-controls.txt:65` in the round-33 wave.
3. **Semantic duplicates:** ten differently named/paraphrased instances of one supported fact, with five otherwise-valid new source records. [INFERENCE] A1's textual distinctness can miss the duplicate knowledge; no pass claimed (`.ufo/waves/round-33/count-c1-a1.py:175-203,268-278`).
4. **Fresh URLs for old authority:** use different pinned/versioned presentations of already-held statements, with distinct bytes, rather than acquire new decisions. [INFERENCE] Registration/hash novelty alone does not reject this; the C0 fixture already uses five pinned Linux documentation views (`.ufo/waves/round-33/c0/CtlShortcutIds.md:68-75`; counter `:228-258`).
5. **Stale judged evidence / false line locator:** mutate only the source bundle after judging, or only a quote locator; preserve the entry hash and qualifying spans. [INFERENCE] These target the unbound-input and locator gaps in findings 3 and the universal audit, respectively; neither was run here.
6. **Forged favorable receipt:** an observed A1 success, explicitly not a legitimate depth witness (`.ufo/waves/round-33/evidence/c1-controls.txt:61-63`; `.ufo/waves/round-33/contract.md:73-75,129-134`).

The legitimate direction is new technical depth on FR6 knowledge, not a claim that the deferred FR6 runtime surface moved. A numeric success bought with unchanged knowledge, invented provenance, or a softened R-J is a trade the canonical judge must not mistake for an improvement (addendum §9 `:351-365`; `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:33-36`). No verdict is issued by this seat.

## Inspection and containment

Read the requested contract/A1, scorecard, frontier, addendum, round-32 closure, prior disk knowledge, both counters and committed C0 reports/receipts. The only shell command was the bounded, memory-limited historical git diff reproduced in finding 4; it returned with no output. No counter, test, build, formatter, external fetch, model/judge runtime, background job, package installation/update, device-setting write, git write or jj write was performed. Only this assigned report was written; no child process remains from the completed diff command. Tool installs/updates: none.
