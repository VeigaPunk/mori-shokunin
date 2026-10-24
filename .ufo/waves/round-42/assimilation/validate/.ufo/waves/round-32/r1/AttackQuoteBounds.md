# AttackQuoteBounds — residual R1

Advisory critic findings only; no row judgment, admission, integration, or runtime invocation.

## Axes and evidence boundary

- **Freshness:** does the re-opened source support the frozen teaches cell? **Calibration:** do quotations preserve qualifications and honestly distinguish support from provenance? **Depth:** do excerpts retain the operative technical distinction? The declared claim is freshness only (`.ufo/waves/round-32/contract.md:8-13,23-27`).
- Reviewed **837b2802c60a6e37a9d462f2354107307fba6ef1**, not the moving worktree. Recheck-section SHA-256: `251bf664717bbdf4c6c99ccde5cc33607b08f03550a0bd913168be2c5a348407`. Frozen population SHA-256: `4426b6501a01c07bdb3347c712c5e858447be47204fa9017c02ab6113e83e178` (`/fast/scratch/hyaku/mori-r32/AttackQuoteBounds/summary.txt:1-3`).
- In citations below, **D** means `/fast/scratch/hyaku/mori-r32/AttackQuoteBounds/contexts.md`; **P** means `.ufo/waves/round-32/c1-population.json` at freeze `29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4`. Lane corpus citations name the reviewed commit. D records each quote, every occurrence, normalized character offsets, adjacent characters, and 30 whitespace-delimited context tokens on either side; fewer are supplied only at a source edge. `⟦…⟧` marks the quotation, not an omission.
- Executed: `timeout 120s prlimit --as=1073741824 --cpu=90 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE PYTHONDONTWRITEBYTECODE=1 TMPDIR=/fast/scratch/hyaku/mori-r32/AttackQuoteBounds python3 -B /fast/scratch/hyaku/mori-r32/AttackQuoteBounds/audit_quotes.py`. Output: `FETCHED_ROWS=33 QUOTES=90 OCCURRENCES=95`; every quote located, every copy matched its table digest. Functions were loaded from the frozen counter without calling its main/fetch/judge paths; normalization is the frozen implementation (`audit_quotes.py:19-35,37-90`; `summary.txt:4-38`; `count-c1.py:77-114`).
- All 90 quotations and all 95 contexts were inspected. No excerpt consisting only of navigation, copyright, version/date furniture, or category boilerplate was found. No dropped negating word or negating lexical prefix was found. One raw-normalized word-boundary anomaly is a JSON escape, not a severed word; see F5. Scope/exception losses are below (D:1-260).

## Suspect excerpts and smallest safe corrections

### F1 — S128 Q3 and S149 Q2 remove the explicit privilege exception

**Strongest counterexample:** the source itself says a process can *always increase its own* legacy `oom_adj`. Both excerpts stop immediately before `, although`, leaving an apparently unconditional capability requirement. This is a quotation defect, not evidence that the live source drifted, and not a claim about modern kernel behavior (`corpus/lessons/round-32.md:52,54`; `corpus/evidence/recheck-r32/S128.src:133-149`; D:244,258). Axes at risk: calibration, depth, and a freshness receipt that treats the shortened statement as complete.

Shared exact context for both occurrences (30 tokens each side):
> this process. A positive score increases the likelihood of this process being killed by the OOM-killer; a negative score decreases the likelihood. The default value for this file is 0; ⟦a new process inherits its parent's oom_adj setting. A process must be privileged ( CAP_SYS_RESOURCE ) to update this file⟧, although a process can always increase its own oom_adj setting (since Linux 2.6.20). Since Linux 2.6.36, use of this file is deprecated in favor of /proc/ pid /oom_score_adj ,

**Smallest safe correction:** replace the affected quote in both rows with the complete 25-word privilege sentence: `A process must be privileged ( CAP_SYS_RESOURCE ) to update this file, although a process can always increase its own oom_adj setting (since Linux 2.6.20).` It is contiguous at normalized offsets 3731–3886. The inheritance sentence remains in the source/context; do not silently turn the legacy paragraph into an `oom_score_adj` rule (`S128.src:134-149`; D:238-244; command receipt below).

### F2 — S044 Q3 discards both the mode and the import/export qualification

The excerpt starts at `either`, omitting `unless you explicitly use ... import ... export`; the paragraph is specifically about **disabled colocation**, whereas the row's scope is colocated jj/Git HEAD state. Q1 and Q2 already support the teaches cell without this detour (`corpus/lessons/round-32.md:33`; `corpus/evidence/recheck-r32/S044.src:2225-2247`; D:99-105). Axes at risk: calibration and depth; the row's substantive detached-HEAD claim is not contradicted.

> Git repository will be hidden inside a sub-directory of the .jj directory. Moreover, unless you explicitly use the jj git import and jj git export commands, that Git repository will ⟦either have no branches at all (not even a main branch) or will have branches that are out of date with jj's bookmarks⟧. Colocation can be disabled because it does have some disadvantages: Interleaving jj and git commands increases the chance of confusing branch conflicts or conflicted (AKA divergent) change ids .

**Smallest safe correction:** remove Q3 and retain Q1–Q2. Reframing the unqualified fragment as a universal statement would be a regression, not an improvement (D:103-105).

### F3 — S051 Q3 cuts off the additional litigation-hold obligation

The footnote is substantive guidance, not page furniture. Its sentence continues `(NARA), as well as in accordance with agency litigation holds.` The quote supports the narrow schedules clause but weakens the source's full disposal condition; it must not be used to imply that schedule compliance alone licenses disposal (`corpus/lessons/round-32.md:38`; D:143; `.ufo/waves/round-32/w1/Recheck051.md:35-42`). Axes at risk: calibration and depth. This omission alone does not establish teaches-cell drift.

>  Data Field Sensitivity. Organizations should evaluate the sensitivity of each individual PII data field. For example, an individual's SSN or financial account number is generally more sensitive than 7 ⟦Disposal of PII should be conducted in accordance with the retention schedules approved by the National Archives and Records Administration⟧ (NARA), as well as in accordance with agency litigation holds. 8 OMB Memorandum 07-16, Safeguarding Against and Responding to the Breach of Personally Identifiable Information, http://www.whitehouse.gov/omb/memoranda/fy2007/m07-16.pdf. 9 FIPS 199, Standards

**Smallest safe correction:** use the contiguous 25-word tail `conducted in accordance with the retention schedules approved by the National Archives and Records Administration (NARA), as well as in accordance with agency litigation holds.` Locate it as the disposal footnote, rather than presenting it as a standalone complete sentence. It preserves both obligations within the frozen length limit (normalized offsets 16620–16796; command receipt below).

### F4 — S062 Q1 stops before “code units”

`arrays of UTF-16` omits the noun that makes the teaches cell's **code-unit** ordering distinction verifiable. This is an under-specified excerpt, not a reversal: the missing words are immediately after the reference marker, and can fit within the limit (`corpus/lessons/round-32.md:42`; `corpus/evidence/recheck-r32/S062.src:550-556`; P:174-178; D:165). Axes at risk: depth and calibration.

> measures MUST be adhered to: ¶ The sorting process is applied to property name strings in their "raw" (unescaped) form. That is, a newline character is treated as U+000A. ¶ ⟦Property name strings to be sorted are formatted as arrays of UTF-16⟧ [ UNICODE ] code units. The sorting is based on pure value comparisons, where code units are treated as unsigned integers, independent of locale settings. ¶ Property name strings either

**Smallest safe correction:** extend Q1 to the complete 17-word sentence: `Property name strings to be sorted are formatted as arrays of UTF-16 [ UNICODE ] code units.` (normalized offsets 12182–12274; command receipt below).

### F5 — S137 Q2: normalized-text boundary anomaly, not a negation/prefix attack

At normalized offset 14971, the preceding character is the literal `n` from the JSON escape `\n`; therefore an ordinary `\w` boundary check flags `nThis`. Parsing the API JSON instead gives `process.\n\nThis` with real newlines: `This` starts a genuine word/paragraph. No lexical prefix, negation, or contrary condition was removed (`corpus/lessons/round-32.md:53`; `corpus/evidence/recheck-r32/S137.src:344`; D:251; command receipt below). Axis at risk: calibration if a mechanical escape artifact is mislabeled a semantic attack.

Exact raw-normalized context (escapes remain literal):
> "name": "Jakob Unterwurzacher", "email": "jakobunt@gmail.com", "date": "2026-02-17T20:30:10Z" }, "message": "kill: option for triggering kernel oom killer\n\nAs mentioned in issue\nhttps://github.com/rfjakob/earlyoom/issues/358 and README, after\nLinux 5.17, OOM sysrq will always kill a process.\n\n⟦This implements an option for trigger the kernel oom killer⟧ i.e.\nwrite an `f` to `/proc/sysrq-trigger`. Since the victim cannot be\nchosen by earlyoom, some of the features about customized victim\nselection won't take effect.", "tree": { "sha": "d8363214aee38f53a32ffef73919511b03c6e492", "url": "https://api.github.com/repos/rfjakob/earlyoom/git/trees/d8363214aee38f53a32ffef73919511b03c6e492" }, "url":

**Smallest safe correction if raw-normalized whole-word boundaries are demanded:** remove redundant Q2; Q1 is a whole-word subject quote bearing on the same re-introduction event. Do not change the frozen normalizer to make this data pass (D:250-251; `count-c1.py:97-104`). Otherwise record this as a non-semantic exception, not a fabricated prefix-cut finding.

## Rows whose exact overlap is only with anchor/scope

The frozen content-token function is `[a-z]+`, length ≥4, minus its stop set (`count-c1.py:54-56,112-113`). **Exactly S071 and S117** have zero teaches-token overlap; every other fetched row has at least one (`/fast/scratch/hyaku/mori-r32/AttackQuoteBounds/summary.txt:4-37`). This is a locator, not a semantic verdict: synonyms can bear on a teaching without sharing exact tokens.

### S071 — vocabulary analogy, not support for the observe-only boundary

Both quotes share only `controller,current,desired,state` with anchor/scope, and no content tokens with teaches. They do bear by analogy on separating declared from observed quantities; they do **not** teach `mori ... never acts to close it`. The source describes making changes, the scope already disclaims observe-only behavior, and S074 explicitly supersedes that attribution (`P:214-234`; D:200-205; `.ufo/waves/round-32/w1/Recheck071074.md:34-37`). Do not misreport this as wholly unrelated boilerplate; do not upgrade the analogy into source authority for the lane's boundary. Axes at risk: freshness and calibration.

Q1 context:
> or request changes where needed. Each controller tries to move the current cluster state closer to the desired state. Controller pattern A controller tracks at least one Kubernetes resource type. ⟦These objects have a spec field that represents the desired state.⟧ The controller(s) for that resource are responsible for making the current state come closer to that desired state. The controller might carry the action out itself; more commonly, in Kubernetes,

Q2 context:
> current cluster state closer to the desired state. Controller pattern A controller tracks at least one Kubernetes resource type. These objects have a spec field that represents the desired state. ⟦The controller(s) for that resource are responsible for making the current state come closer to that desired state.⟧ The controller might carry the action out itself; more commonly, in Kubernetes, a controller will send messages to the API server that have useful side effects. You'll see examples of

**Smallest safe correction:** make the vocabulary-only support versus lane-owned application explicit in the reviewer reasoning, retaining the frozen teaches text. If calling it `current` requires replacing the frozen whole-cell definition with “some page-borne clause is unchanged,” that is a claim tradeoff for the canonical judge, not a quote repair (`contract.md:23-27`; D:201-205).

### S117 — tag-to-object provenance, not the log-grammar teaching

All three quotes are API tag metadata. Their shared anchor/scope tokens are `commit,ddaf,earlyoom,tags`; `ddaf` is a substring of the hexadecimal object id, not explanatory prose. Teaches-token overlap is zero. No quote states the `mem avail`/`mem <=` contrast, action/escalation stability, or width-5 percentage formatting (`P:246-250`; D:230-236). The author explicitly acknowledges the literals are not on this page and argues through pinned-source identity instead (`.ufo/waves/round-32/w1/Recheck117.md:49-69`). This is indirect provenance evidence, not page furniture and not direct semantic support. Axes at risk: freshness and calibration if identity is silently substituted for teaching verification.

Q1 context (only two tokens precede this quote because it starts at the first API object):
> [ { ⟦"name": "v1.9.0", "zipball_url": "https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.9.0", "tarball_url": "https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.9.0", "commit": { "sha": "202d4db0d308ca6478f68de68b46cae34896ddaf"⟧, "url": "https://api.github.com/repos/rfjakob/earlyoom/commits/202d4db0d308ca6478f68de68b46cae34896ddaf" }, "node_id": "MDM6UmVmMTU4NTA3ODQ6cmVmcy90YWdzL3YxLjkuMA==" }, { "name": "v1.8.2", "zipball_url": "https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.8.2", "tarball_url": "https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.8.2", "commit": { "sha": "d5791d300aafa77b8f6a3d3d97f481a4ef904a38", "url": "https://api.github.com/repos/rfjakob/earlyoom/commits/d5791d300aafa77b8f6a3d3d97f481a4ef904a38" }, "node_id": "MDM6UmVmMTU4NTA3ODQ6cmVmcy90YWdzL3YxLjguMg==" }, { "name": "v1.8.1", "zipball_url": "https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.8.1", "tarball_url":

Q2 context:
> "tarball_url": "https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.8.2", "commit": { "sha": "d5791d300aafa77b8f6a3d3d97f481a4ef904a38", "url": "https://api.github.com/repos/rfjakob/earlyoom/commits/d5791d300aafa77b8f6a3d3d97f481a4ef904a38" }, "node_id": "MDM6UmVmMTU4NTA3ODQ6cmVmcy90YWdzL3YxLjguMg==" }, { "name": "v1.8.1", "zipball_url": "https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.8.1", "tarball_url": "https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.8.1", "commit": { "sha": "4965c8315a3a5479b6241ac2ac96e674218df8fd", "url": "https://api.github.com/repos/rfjakob/earlyoom/commits/4965c8315a3a5479b6241ac2ac96e674218df8fd" }, "node_id": "MDM6UmVmMTU4NTA3ODQ6cmVmcy90YWdzL3YxLjguMQ==" }, { ⟦"name": "v1.8", "zipball_url": "https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.8", "tarball_url": "https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.8", "commit": { "sha": "62625072ce8671f497a5cea5fc3db63226469093"⟧, "url": "https://api.github.com/repos/rfjakob/earlyoom/commits/62625072ce8671f497a5cea5fc3db63226469093" }, "node_id": "MDM6UmVmMTU4NTA3ODQ6cmVmcy90YWdzL3YxLjg=" }, { "name": "v1.7", "zipball_url": "https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.7", "tarball_url": "https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.7", "commit": { "sha": "ebaea9526bcee14889b00d83a9dd3d038315cee2", "url": "https://api.github.com/repos/rfjakob/earlyoom/commits/ebaea9526bcee14889b00d83a9dd3d038315cee2" }, "node_id": "MDM6UmVmMTU4NTA3ODQ6cmVmcy90YWdzL3YxLjc=" }, { "name": "v1.6.2", "zipball_url": "https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.6.2", "tarball_url":

Q3 context:
> "tarball_url": "https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.8.1", "commit": { "sha": "4965c8315a3a5479b6241ac2ac96e674218df8fd", "url": "https://api.github.com/repos/rfjakob/earlyoom/commits/4965c8315a3a5479b6241ac2ac96e674218df8fd" }, "node_id": "MDM6UmVmMTU4NTA3ODQ6cmVmcy90YWdzL3YxLjguMQ==" }, { "name": "v1.8", "zipball_url": "https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.8", "tarball_url": "https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.8", "commit": { "sha": "62625072ce8671f497a5cea5fc3db63226469093", "url": "https://api.github.com/repos/rfjakob/earlyoom/commits/62625072ce8671f497a5cea5fc3db63226469093" }, "node_id": "MDM6UmVmMTU4NTA3ODQ6cmVmcy90YWdzL3YxLjg=" }, { ⟦"name": "v1.7", "zipball_url": "https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.7", "tarball_url": "https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.7", "commit": { "sha": "ebaea9526bcee14889b00d83a9dd3d038315cee2"⟧, "url": "https://api.github.com/repos/rfjakob/earlyoom/commits/ebaea9526bcee14889b00d83a9dd3d038315cee2" }, "node_id": "MDM6UmVmMTU4NTA3ODQ6cmVmcy90YWdzL3YxLjc=" }, { "name": "v1.6.2", "zipball_url": "https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.6.2", "tarball_url": "https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.6.2", "commit": { "sha": "445bda11fc98f233a4fe87a033e2350f4d93f610", "url": "https://api.github.com/repos/rfjakob/earlyoom/commits/445bda11fc98f233a4fe87a033e2350f4d93f610" }, "node_id": "MDM6UmVmMTU4NTA3ODQ6cmVmcy90YWdzL3YxLjYuMg==" }, { "name": "v1.6.1", "zipball_url": "https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.6.1", "tarball_url":

**Smallest safe correction:** present this as an explicit provenance chain, with pre-data object identities and the already-pinned source passages that actually state each grammar claim. The frozen anchor contains the v1.9.0 object id but not full v1.8/v1.7 object ids; mere continued tag existence does not itself establish unchanged comparison bytes (P:248-250; Recheck117.md:54-69). More API-metadata quotes cannot repair that logical gap. If direct teaching support is required by the frozen definition, changing it to tag reachability would be a tradeoff for the canonical judge, not an acceptable silent narrowing (`contract.md:23-27`).

## Complete fetched-row coverage

All entries below were located in the committed normalized copy. “No concern” means no meaning-changing cut/prefix/furniture issue found in the quoted passages; it is **not** an R1–R5 or `current` judgment. D supplies the actual per-quote contexts and offsets.

| Row | Quotes | Context evidence | Quotation finding |
|---|---:|---|---|
| S001 | 3 | D:5-7 | No concern |
| S002 | 3 | D:13-15 | No concern |
| S007 | 3 | D:21-23 | No concern; eligibility not universalized by the teaches cell |
| S012 | 2 | D:29-30 | Affected/patched metadata is relevant, not furniture |
| S014 | 3 | D:36-38 | Generic Q1 accompanied by substantive cursor/field quotes |
| S015 | 3 | D:44-46 | No concern |
| S031 | 2 | D:52-53 | Conditional and consequence preserved across Q1–Q2 |
| S037 | 3 | D:59-66 | Q3 occurs six times; occurrence 5 belongs to the same unit-field paragraph as Q2 |
| S039 | 2 | D:72-73 | No concern |
| S040 | 3 | D:79-81 | No concern |
| S041 | 3 | D:87-89 | No concern; no category/standards-track-only excerpt |
| S043 | 3 | D:95-97 | No concern |
| S044 | 3 | D:103-105 | F2: Q3 qualification/mode loss |
| S045 | 2 | D:111-112 | `not modified` retained |
| S046 | 3 | D:118-120 | Conditional status mapping and separate error class retained |
| S047 | 2 | D:126-127 | No concern |
| S049 | 3 | D:133-135 | `usually not`, hashing condition and malformed-field context retained |
| S051 | 3 | D:141-143 | F3: Q3 additional disposal obligation omitted |
| S052 | 3 | D:149-151 | `may not` and small/predictable-input condition retained |
| S058 | 3 | D:157-159 | No concern in the quoted rev-list passages |
| S062 | 3 | D:165-167 | F4: Q1 omits code-unit noun; Q2 retains MUST NOT |
| S064 | 3 | D:173-175 | No concern |
| S067 | 2 | D:181-182 | Actual-versus-desired/correct distinction retained |
| S068 | 3 | D:188-190 | Q3 preserves its conditional; Q1–Q2 supply link behavior |
| S069 | 3 | D:196-198 | No meaning reversal; teaches attribution beyond the quote is separate |
| S071 | 2 | D:204-205 | Anchor/scope-only exact tokens; semantic limit above |
| S073 | 3 | D:211-213 | No concern; resolve remedy retained in Q2 |
| S074 | 3 | D:219-221 | Action-on-gap explicitly retained |
| S076 | 2 | D:227-228 | Actual-versus-desired distinction retained |
| S117 | 3 | D:234-236 | Anchor/scope-only tokens; provenance, not grammar evidence |
| S128 | 3 | D:242-244 | F1: Q3 drops `although` exception |
| S137 | 2 | D:250-251 | F5: Q2 JSON-escape lexical anomaly only |
| S149 | 3 | D:257-259 | F1: Q2 drops same exception |

S056 has no quotation and is outside this 33-fetched-row review (`corpus/lessons/round-32.md:40`; `summary.txt:23`).

## Executed corrective-span inspection and limits

Executed `timeout 120s prlimit --as=536870912 --cpu=90 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE PYTHONDONTWRITEBYTECODE=1 TMPDIR=/fast/scratch/hyaku/mori-r32/AttackQuoteBounds python3 -B /fast/scratch/hyaku/mori-r32/AttackQuoteBounds/quote_details.py`. Output: S128 replacement `chars=3731:3886 words=25`; S062 `chars=12182:12274 words=17`; S051 `chars=16620:16796 words=25`; `S137 decoded start_is_word_boundary=True`; `TEACHES_ZERO_ROWS=S071,S117`; `MISSING_QUOTES=0`. These are source-span inspections, not counter/judge passes.

The controls already warned that supporting semantics and dropped prefixes must be caught outside token overlap (`.ufo/waves/round-32/evidence/c1-controls.txt:25-34`). F1–F4 are local quotation repairs; fixing them does not authorize changing the contract, teaches cells, counter, or reviewer authority. The S071/S117 semantic-support boundaries remain for the designated judge; no acceptance verdict is issued here.

No live fetches were made, including none to S117/S137. No counter, build, test suite, or canonical runtime was run. Only this report and this seat's scratch artifacts were written; no git/jj writes, background jobs, installations, or updates were performed. Both bounded foreground analysis commands exited normally; no process tree was left running.
