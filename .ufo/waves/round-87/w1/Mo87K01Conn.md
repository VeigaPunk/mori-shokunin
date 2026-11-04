# Mo87K01Conn — sibling-overlap scan: who else replays a receipt body, and who else grades a lane's own mutation arms (mori round 87, w1)

Read-only seat. I wrote exactly one file: this report. Nothing in any lane, the fleet root,
`.ufo/state/`, `MANIFEST.json`, `SCORECARD.md`, `LOG.md` or `considerthese/` was written; no mutating
git/jj command ran in any lane; no lane file was copied into the lane (fixtures lived only under my
scratch). Scratch `/fast/scratch/hyaku/mori-r87/Mo87K01Conn/` was created and deleted before yield.
No tool was installed or upgraded.

Revisions and hashes actually read (siblings land while a seat scans — both facts are recorded):

| item | value |
|---|---|
| scan open HEAD | `b9e6f68d887c570909c7bacc8bac86579d850d1d` |
| scan close HEAD | `728bc5f48363e668710579ed2b7822632383178a` (round-87 integration: after receipt, lesson, QUALITY 181–182, SCORECARD, LOG landed mid-scan) |
| freeze / entering / claims | `142542e0d8…`, `6fc09d69ed…`, C1 `03b66a43…`, C2 `98f48dba…` |
| `round-87/contract.md` | `bf208a448e096da4da5169e1b27db1b1ca97999119a2e43e49954c894042eb07` |
| `round-87/evidence/controls-r87.txt` | `53d65a426632acdb5c88721a2e7847110780e8c668f8c8fbd4b1bdd5df75e616` |
| `round-87/evidence/probe-r87.txt` | `530e35e6058edfa5d690343e149e53392e3daa81ea3f13f3fe7224f26db3180d` |
| `round-87/count-c1.py` | `e2ff968721678cc61d6a1674def8da3e27a43f3fed8daab79d53c657ae2c266e` (worktree == HEAD at both revisions) |
| `round-87/count-c2.py` | `264a43f04af1f9f939da7b3890f608a669a0c7fc2922656ee83f35adb236b14d` (A1 bytes; worktree == HEAD at both revisions) |
| subject arm counts, counted with `grep -c 'cases.append('` at `03b66a43` and `98f48dba` | 18 / 13 / 23 |

This seat did **not** grade C1 or C2. It read their receipts (`after-r87.txt` `282513c0…`,
`supersede-controls-r87.txt` `b9ca89cf…`, at `728bc5f4`) and ran **one** instrument measurement of its
own (§5). Everything below about a sibling is a file:line claim; everything below about mori is a
file:line claim over the bytes named above.

---

## 1. Verdict and adjacency matrix

Two mechanisms, twelve sibling grounds checked. The scan found:

- **one duplicate** of mori's C2 core mechanism, landed ~54 rounds earlier (kama r33);
- **one contradiction** of mori's C1 kill rule, landed ~44 rounds earlier (tameshi r43's K/D/E/U), not
  exercised at r87 by measurement (§5);
- **one implemented rule that closes the exact gap mori's own QUALITY 177 declares "Not covered"**
  (kaidoku r79; kama r75 is the second lane, so tameshi's two-lane admission bar is already met);
- **one fleet-wide map of the receipt family** already written by the connector role itself
  (kaidoku r67), which mori's r87 knowledge entry and QUALITY 181/182 do not cite;
- **no sibling** that grades *supersede gated on replay* (mori's one genuinely new clause here);
- several complements and two named limits mori should state rather than absorb.

`duplicate` = same mechanism, named difference; `complement` = adjacent, boundary named;
`contradicts` = the two rules cannot both be applied to the same object as written;
`distinct` = adjacent vocabulary, different object; `none` = no row on that ground.

| lane | (a) receipt replay / body-equals-command | (b) mutation-arm grading of own counters |
|---|---|---|
| kama | **duplicate** — `tools/round33-gate-receipts.py:414,448` replays and compares stdout | **duplicate (shape) + stronger** — `tools/round75-survivor-probe.py:20,42,88` |
| kotodama | **complement** — `tools/check-receipt-seq.py:1-40` binds headers/tree/digest only | none |
| tameshi | **complement** — `tools/receipt-revision-gate.py:45-49` (11 refusal codes) | **contradicts** — `corpus/knowledge/r43-survivor-resolution-rule.md:57-60` |
| kaidoku | distinct — r34 replay gate, r38 json-out parity, r40–49 parameter replay | **complement + stronger** — `tools/round-79/gate-mutation.py:17-21` |
| mado | **complement** — `tools/mado-tripwire.py:131-152` `--frozen` | **duplicate (shape) + stronger control** — `quality/counters/c1-r81-overflow-auto.py:465`, `c1-r73-summary-mutants.py:224` |
| kasegi | **complement** — `corpus/QUALITY.md:50` (R8), `:401` (R54) | none |
| kengaku | **complement** — `corpus/QUALITY.md:161` (R1), `:165` (R5), `:762` | **complement** — `corpus/QUALITY.md:441` (limit of the freeze) |
| tabi / protocol | **distinct policy** — latest-row-wins / last-row-wins (via `kengaku …/round73/w1/sibling-overlap.md:48`) | none |
| kumitate | **adjacent, weaker identity** — `corpus/QUALITY.md:157-165` (Q19) | **complement** — `corpus/QUALITY.md:196-198` (equivalent kept, not hidden) |
| tsukuroi | distinct — `corpus/knowledge/adjacency-anchors-r19.md:13,43` | **complement** — `corpus/knowledge/memory-arm-mutants-s8.md:13-15,112` |
| kotoba | none | **contradicts (partially)** — `corpus/QUALITY.md:58` (Q47) |
| chousa | none | **satisfied by construction** — `corpus/QUALITY.md:957-958` |

---

## 2. Ground (a) — receipt replay / body-must-equal-command

### 2.1 kama — duplicate of the mechanism, landed at round 33 (the finding this seat exists for)

`kama-shokunin/tools/round33-gate-receipts.py` is the same mechanism as mori's `# replay:` pass:

- `:1-8` — "Audit reads only committed receipt blobs and **replays each case from its pinned source
  revision**; the lane repository is never mutated."
- `:229` `expected_receipts(repo, source_rev)` — rebuilds each expected receipt by **re-running the
  pinned gate at `source_rev`**.
- `:414` `audit(...)` — for each committed receipt, compares the parsed record against that re-run.
- `:448` — `and stdout == expected_stdout` (and `:449` `stderr == expected_stderr`), beside a
  stable-header comparison (`FORMAT`, `FIXTURE`, `COMMAND`, `SOURCE_REV`, `EVALUATED_REV`,
  `EVALUATED_TREE`, `GATE_SHA256`, `EXIT_CODE`).
- `:210,218,223` — a structured receipt grammar (`FORMAT=KAMA_GATE_RECEIPT_V1`, `COMMAND=`,
  `STDOUT_BEGIN … STDOUT_END`, `STDERR_BEGIN … STDERR_END`).

Named differences from mori C2 (they are real, and they are the whole of mori's contribution):

| | kama r33 | mori r87 |
|---|---|---|
| population | four named fixture cases, one gate path, compiled into the tool | a seven-receipt population declared in `count-c2.py:39-48`, each with `# cmd:` / `# rev:` / `# replay:` |
| binding | expected body rebuilt from a fixed case table | expected body = stdout of the receipt's *own* recorded command |
| stderr | compared (`:449`) | **discarded** — `replay_body` returns `p.stdout` only (`count-c2.py:170-201`) |
| supersede | none | **the new clause**: `supersede_counts` (`count-c2.py:139-147`) retires a legacy receipt only through a clean, replaying successor |

**Relation: duplicate mechanism, distinct generality and a genuinely new supersede clause.** Mori may
claim the `# cmd:`-generic population, the `--shared` clone mode, and the supersede gating; it may not
claim the class. Neither mori's QUALITY 178 nor the r87 knowledge entry cites this file (§6.3).

### 2.2 kotodama — complement, and the exact limit mori closes

- `tools/check-receipt-seq.py:1-40` — the header discipline: `# stamped revision:`,
  `# evaluated revision:`, `# measured revision (lane main):`, `# tree:`, `# counter sha256 (self):`;
  `stamped == evaluated == measured`, the recorded tree == `git rev-parse <rev>^{tree}`, and, when a
  counter path is paired, the recorded digest == `sha256(counter)`.
- The connector role already characterised it: `kaidoku …/.ufo/waves/round-77/w1/ConnectorCross.md:48`
  — "`stamped == evaluated == measured` + tree + counter sha256; `--lands` reads committed bytes;
  `moved_past` is computed and **deliberately never changes a verdict** | **no argv, no env, no value
  clauses**".

Mori C2 is exactly the "argv" leg kotodama lacks, and its `# counter-sha256:` leg is the same digest
discipline under a different spelling. **Relation: complement.** Two consequences mori should state:
(i) the grammars are disjoint — a mori receipt does not satisfy `check-receipt-seq.py` (it has no
`# stamped revision:`/`# tree:` lines) and a kotodama receipt has no `# cmd:`, so no single receipt
serves both checkers; (ii) mori's digest line is per-path and repeatable, kotodama's is a single
self-digest, so mori's grammar is the more general of the two.

### 2.3 tameshi — complement on revision binding, with 11 named refusal codes

- `tools/receipt-revision-gate.py:1-10` — the r54/55 defect: "a positive control was scored at the
  FREEZE commit, which predated the work it certified, and every gate in the lane accepted it because
  none compared the `rev=` a receipt names with the revision under test."
- `:25-28` — refusal codes `RECEIPT_REV_ABSENT`, `RECEIPT_REV_AMBIGUOUS`, `RECEIPT_REV_UNRESOLVABLE`,
  `RECEIPT_REV_MISMATCH`, `RECEIPT_REV_CONTENT_DRIFT`, `RECEIPT_CONTROL_NOT_ANCESTOR`,
  `RECEIPT_DIGEST_MISMATCH`, `RECEIPT_REQUIRED_LINE_MISSING`, plus missing/empty/not-blob.

Mori's `# rev:` check is `ancestor(repo, fields["rev"], rev)` (`count-c2.py:174-176`), i.e. the
`RECEIPT_CONTROL_NOT_ANCESTOR` leg only. **Relation: complement (mori is the weaker subset).** One
mori limit is named by tameshi's code, not by mori: `RECEIPT_REV_CONTENT_DRIFT` — a receipt can name
an ancestor revision whose bytes at the certified path have since changed. Mori's `bound` leg reads
`sha256_at(repo, fields["rev"] or "", bpath)`, so the *digest* is rev-bound; but a receipt with no
`# counter-sha256:` line has no such leg, and mori's grammar does not require one.

### 2.4 mado — complement; the closest *semantic* sentence in the fleet

`tools/mado-tripwire.py:131-152` (`--frozen`) — "proves a committed snapshot still reproduces the
pinned verdict over pinned bytes. It validates its pin before replay: … an unreachable pin is
`frozen_error`, never a failed verdict. It does not prove the snapshot was copied faithfully from the
transcript it names: provenance is the snapshot author's claim, not checked."

That is (i) the same **setup-versus-mismatch split** mori makes with `replay-rc:<n>` versus
`replay-mismatch` (`count-c2.py:273-275`), and (ii) an explicit statement of the gap mori's
`body == out` closes for mori's own receipts. **Relation: complement.** Mori should cite it as the
boundary it moves: mado replays a *verdict over fixture bytes* and disclaims body provenance; mori
replays the *body* and therefore can speak to provenance.

### 2.5 Distinct uses of "replay" (do not mistake for overlap)

- `kaidoku-shokunin/tools/round-34/replay-gate.py:2,14` — "P34-shortcut-replay: **pre-freeze
  structure-blind replay gate**". It replays *shortcut readers* under the counter's own predicate and
  refuses a freeze (`REPLAY_GATE_CLEAN` / `REPLAY_GATE_REFUSED` / `REPLAY_GATE_UNEVALUABLE`). The word
  names the shortcut class, not a receipt. No overlap with C2; adjacent to C1 only as "pre-freeze
  adequacy".
- `kaidoku-shokunin/tools/round-40…49/c1-counter.py` — "the run replays the committed receipt's
  recorded **extraction parameters**" (e.g. `round-49/c1-counter.py:104,1862`). It replays inputs and
  compares artifacts, not the body.
- `kaidoku-shokunin/tools/round-38/freeze-drift.py:198-208,216` — `json_out_parity`: `text ==
  p.stdout` inside a selftest (`--json-out` parity). A real body-equals-stdout comparison, but
  self-test-local, not a receipt population.

### 2.6 Supersede policies already partitioned — mori's is a fourth

`kengaku-shokunin/corpus/evidence/round73/w1/sibling-overlap.md:48` — "tabi latest-row-wins and
protocol closure-ledger last-row-wins are deliberate append-only supersession policies; C2
deliberately rejects duplicate names and prices every row. Importing either sibling policy would undo
D3." Three policies exist: *latest wins* (tabi `scripts/check-gate-registry.mjs:37`), *last wins*
(protocol closure ledger), *reject duplicates* (kengaku C2).

Mori's supersede is a **fourth**: *a successor retires a predecessor only by naming it and proving
its own replay*. It must not be presented as the correct policy, must not import the other three, and
must not be read as a duplicate-row policy (the population has seven distinct basenames).

Adjacent append-only rules, all complements:

- `kasegi-shokunin/corpus/QUALITY.md:50` (R8) — "a corrected anchor or broadened scope in a registry
  row is a new row beginning 'supersedes S### —'"; `:401` (R54) — "A superseding source row does not
  automatically reject its predecessor … If a frozen claim demanded the harmful transition, report
  that claim unmet; do not weaken B3 or rewrite the frozen predicate to manufacture success." R54 is
  precisely the discipline mori C2 obeys when it leaves `after-r85.txt` `legacy` rather than minting a
  successor for a live-observation body.
- `kengaku-shokunin/corpus/QUALITY.md:161` (R1) — "corrections are appended, never rewritten … the old
  line stays byte-identical"; `:165` (R5) — a superseded premise gets a dated erratum *naming the
  receipt and line*; `:762` — a correction "lands as a NEW row whose `teaches` cell opens
  `supersedes S0NN —`". Mori names the predecessor by **basename only** and cites no line; kengaku
  names a row id inside the row itself. Same discipline, weaker address.

### 2.7 kumitate — the identity mori uses is the one Q19 forbids (named limit, not a contradiction)

`kumitate-shokunin/corpus/QUALITY.md:157-165` (Q19) — "Identity for an anchor is its raw text, its
resolved path and its occurrence index, never the token, the key or any other field the edit under
test can rewrite."

Mori's supersede identity is `os.path.basename(path)` (`count-c2.py:133-137`): a successor supersedes
`record-sweep-r85.txt`, not a path. Two receipts with the same basename in different directories would
alias, and a redirect of the legacy path would not be seen. **Not exercised** — all seven population
basenames are distinct — so this is a named limit, not a defect of the current claim. Q19 governs
floors, not receipt populations; the principle travels, the rule does not.

---

## 3. Ground (b) — mutation-arm grading of a lane's own counters

### 3.1 tameshi — the method owner, and a rule that contradicts mori's kill rule as written

`tameshi-shokunin/corpus/knowledge/r43-survivor-resolution-rule.md:57-60`:

- `:58` **K — killed** — "The round's battery produces at least one FAIL under the **exit-plus-FAIL**
  oracle: the tool exits 0 with parseable output and a case differs from its declared classification."
- `:60` **U — unresolved** — "Anything else: `not_killed` …, `runtime_error` (**non-zero exit,
  traceback** or unparseable output), `apply_error` …" — "does not count toward resolution".

Mori's kill rule (`count-c1.py:104-105`) is `rc != 0 or bool(FAIL.search(out))`. Under tameshi's
K/D/E/U, **a crashed mutant (non-zero exit, no parseable FAIL) is U, not K**. **Relation:
contradicts, as written.** It is not exercised at r87: §5 measures every one of the six kills as
`rc=1` with exactly one `FAIL <arm>` line and no traceback, so mori's tally is also a tameshi tally
this round. The contradiction is about the rule, not the data.

Tameshi also owns the method and refuses to let a lane own it: `tameshi-shokunin/PROVINCE.md:3-16` —
"every lane's gate remains its own; tameshi owns only the reusable craft (a pattern is admitted from
evidence in **TWO independent lanes** before it is claimed general)". Mori citing kaidoku r79 and kama
r75 satisfies that bar; mori must not claim the method.

Complement on anchor discipline: `tameshi-shokunin/corpus/QUALITY.md:438` — "deleting any anchor
produces INCONCLUSIVE, not [a kill]". Mori's `unanchored` (`count-c1.py:157-161`) is the same
disposition and its contract says so in the same words.

### 3.2 kaidoku r79 — the implemented rule that closes mori's own declared gap

`kaidoku-shokunin/tools/round-79/gate-mutation.py:17-21`:

> "A mutant is KILLED only when its **declared case** is present in the mutant's selftest output and
> fails there. An absent declared case is a SURVIVOR, never a pass (that is exactly the round-78
> defect: a detector that does not exist cannot catch anything). A mutant whose anchor does not occur
> exactly once, or whose copy does not produce a SELFTEST summary, is INCONCLUSIVE and never counted
> as killed."

Mori has the second sentence (`unanchored`), the fourth (`arms_of` returning `(-1,-1)` then a red
pristine), but **not the first**: `killed()` has no notion of *which* case must fail. This is exactly
the clause mori's own QUALITY 177 declares uncovered — "Not covered: an arm whose assertion is
vacuous but still turns its own mutant red for an unrelated reason" (`corpus/QUALITY.md:2037-2049`,
the clause at `:2048`).
**Relation: complement; the sibling is strictly stronger, and mori's criterion already names the
gap.**

### 3.3 kama r75 — the second lane, with per-mutant arm attribution

`kama-shokunin/tools/round75-survivor-probe.py`:

- `:20` PREDICATE — "prints one `SURVIVORS2 mutants=5 killed=5 escaped=0` line and exits 0 only when
  it applies five named source mutations to a copy of the committed `tools/round74-receipt-claim-binding.py`
  in its own scratch, runs the pristine module's selftest green and every mutated copy's selftest red,
  and **names for each mutant the selftest arm that fails**".
- `:42` `EXPECTED_ARMS = {...}`; `:88` `and EXPECTED_ARMS.get(row["mutant"]) in row["failed_arms"]`;
  `:91` `"escaped": len(rows) - killed`; `:151` `SURVIVORS2_ARM {name} ok|FAIL`.

Mori's tally shape is the same (`mutants=6 killed=6 survivors=0` vs `mutants=5 killed=5 escaped=0`);
mori's word for kama's `escaped` is `survivors`, and mori has no `EXPECTED_ARMS`. **Relation:
duplicate shape, stronger attribution.** With kaidoku r79 it is the second independent lane tameshi's
admission rule requires.

### 3.4 mado — a self-certifying mutant tally, and a two-sided control

- `quality/counters/c1-r81-overflow-auto.py:442-469` — per-mutant `MADO_R81_MUTANT: name=… killed=…`
  lines, then `MADO_R81_BARFOOT: cases=%d correct=%d mutants=%d killed=%d base_correct=%d/%d …`, with
  `target = (correct == CASES and killed == MUTANTS and base_correct == BASE_EXPECT …)`.
  Receipt: `corpus/knowledge/bar-footprint-rounding-auto-r81.md:29` — `mutants=28 killed=28
  base_correct=33/39 … verdict=TARGET_MET`. **Duplicate shape**: a counter self-certifying its mutant
  tally in its own receipt line, exactly as mori's `mutants=6 killed=6 survivors=0`.
- `quality/counters/c1-r73-summary-mutants.py:29-31,224-231` — `cases=10 mutants=4 killed=<n>
  base_killed=<m>`, exit 0 iff `killed == 4 and base_killed == 2`, with the base measured at
  `--base-rev` (`:246,296`). Selftest arms `:391-393`: `verdict_met(4,2)`; `not verdict_met(4,3)` —
  "verdict refuses a held-set kill of four"; `not verdict_met(3,2)` — "refuses a weak new set".

**Relation: complement, stronger control.** mado's control is **two-sided** (the mutant set must kill
exactly 2 at the base and all 4 after hardening), so a set the base already nearly kills
(`base_killed=3`) is refused. Mori's control is one-sided: the entering bytes must read `killed=0`,
which is the degenerate `base_killed=0` member of mado's family. Mori's six-mutant set is likewise not checked for
discrimination against the *entering* counters beyond "all six survived" — which is the same fact,
so the family is joined with a weaker member, not contradicted.

### 3.5 tsukuroi — own-case kills, the shape mori lacks

`corpus/knowledge/memory-arm-mutants-s8.md:13-15` — "the 8 memory-arm selftest cases … are now
measured against injected defects — **8/8 own-case kills, D2–D8 each uniquely**"; `:95`
`MUTATE: DONE (target=tsukuroi-census-s7-2-memory-arm defects=11 killed=8 survived=3
inconclusive=0 kill-rate=73%)`; `:112` "every one of the 8 round-7 memory-arm cases kills a defect of
exactly its own [case]". Measured with tameshi's runner (pinned sha `cf41efaa…`).

Mori's six mutants are likewise killed by exactly the arm added for each (§5), but mori does not
*assert* it: the attribution lives in a wave report, not in the predicate. **Relation: complement.**

### 3.6 kotoba Q47 — the contested half, narrowed by r87

`kotoba-shokunin/corpus/QUALITY.md:58` (Q47) — "A mutation-kill measure is **two-sided** (every
declared mutant killed AND every semantics-preserving equivalent survives) and its equivalents are not
a fixed published list: a fixed list is a label a self-test can key on, so the set is generated at
measurement time or the measure stays a record, never a claim."

Two changes from r84 (where this was the sharpest boundary):

1. **r87 has no equivalent class at all.** The target is `mutants=6 killed=6 survivors=0` — no
   `equivalent=` token, no `EQUIVALENT` map. Q47's "two-sided" half is therefore not violated by an
   equivalent set; it is simply not measured. That is a narrowing, not a discharge: the lane cannot
   say whether any of the six is semantics-preserving, only that all six are killed.
2. **The kill is measured by the subject's own selftest, not by mori's.** kotoba's M75
   (`lessons/round-58.md:61-66`) withdrew a C2 whose *source-grep self-test* met the predicate. Mori's
   `selfcheck` cannot do that: the kill in `grade()` comes from running the mutated *subject's*
   `--selftest` (`count-c1.py:169-170`), and mori's own arms only grade the detector
   (`marker_literal` greps mori's own source for a label, which is detector-side). So the label cannot
   be keyed on to fake a kill — but the six anchors **are** published in the frozen counter, and a
   subject's selftest could in principle key on the mutated bytes. Mori's guard is the
   `unanchored`/`empty-mutation` pair, not a generation rule.

**Relation: contradicts the "fixed published list" half as written; the "two-sided" half is simply
unmeasured by r87.** State which reading the lane takes; do not claim Q47 compliance.

### 3.7 chousa — satisfied by construction this round

`chousa-shokunin/corpus/QUALITY.md:958` — "A frozen mutant set holds no equivalent mutant; a survivor
is classified before the target is fixed. … rebuild the set with each mutant's first edit only and run
the counter; a survivor the landed builder cannot kill is a mutant-set defect, never a data result."

r87 satisfies the headline **by construction**: a set holding an equivalent cannot reach
`survivors=0`, so a met target proves no equivalent survived. The check also passes: each of the six
mutants is one exact old→new replacement, and I measured each anchor occurring exactly once (§5). This
is a genuine improvement over r84, which carried `equivalent=2` from a fixed map and stood on the
chousa/kotoba boundary. `corpus/QUALITY.md:957` (a kill rule cannot be satisfied by a tool that
alternates behaviour or counts calls) is adjacent to the attribution gap in §3.2.

---

## 4. Contradictions, stated not smoothed

1. **A crash counts as a kill under mori's rule, and tameshi says it does not.** `count-c1.py:104-105`
   versus `r43-survivor-resolution-rule.md:58,60`. Measured not exercised at r87 (§5). The rule, not
   the data, is the disagreement.
2. **The mutant set is a fixed published list, and kotoba says a measure using one stays a record.**
   `count-c1.py:58-72` (published `MUTANTS`) versus `kotoba/corpus/QUALITY.md:58`. Narrowed by the
   absent equivalent class and by subject-side kills, not discharged.
3. **Mori C2 restates a mechanism kama implemented at round 33 and cites no sibling.**
   `kama/tools/round33-gate-receipts.py:414,448` versus `corpus/QUALITY.md:2051-2068` (QUALITY 178)
   and `corpus/knowledge/receipt-supersede-r87.md` — neither names kama, tameshi or kotodama. The
   claim survives; a novelty claim would not.
4. **The fleet's own connector map of the receipt family already exists and is not cited.**
   `kaidoku …/round-67/w1/ConnectorCross/overlap.md:162-168` (C-1…C-5, "at least six lanes carry a
   receipt-sequence, receipt-completeness, receipt-citation or receipt-pinning gate"; verdict: "the
   receipt-revision convention is established and multiply owned") and `…/round-77/w1/ConnectorCross.md:48`.
   The r87 lesson has **no** adjacency mention at all (`grep -niE 'adjacency|sibling|kama|kotodama|tameshi|kaidoku'
   corpus/lessons/round-87.md` → no hits at `728bc5f4`).
5. **Supersede identity is a basename where kumitate Q19 requires path plus index.** Not exercised;
   named as a limit.

---

## 5. The one instrument measurement this seat ran (own run, own scratch)

Purpose: decide whether contradiction 1 bites at r87, and whether the six kills land on the arms the
contract says were added for them. Method: `git show` each subject at its claim revision into my
scratch, apply the frozen `MUTANTS` old→new exactly as `count-c1.py:58-72` declares, run the mutated
copy's own `--selftest` in a temp dir under my scratch, print the failing lines. No lane file was
written; nothing was committed.

Command (script kept in scratch, deleted at yield): `python3 attrib.py` over
`.ufo/waves/round-86/count-c1.py` @ `03b66a43`, `count-c2.py` @ `98f48dba`, `count-c3.py` @
`03b66a43`.

| mutant | anchor occ. | rc | passes | FAIL lines | arm that fails |
|---|---|---|---|---|---|
| `M1-unanchored-conjunct` | 1 | 1 | 17 | 1 | `unanchored_plus_killed_unmet` |
| `M2-total-floor` | 1 | 1 | 17 | 1 | `zero_mutants_unmet` |
| `M3-arms-tally` | 1 | 1 | 17 | 1 | `arms_tally_from_subject` |
| `M4-receipt-summary` | 1 | 1 | 12 | 1 | `summary_required` |
| `M5-binding-digest` | 1 | 1 | 12 | 1 | `binding_required` |
| `M6-keyshape` | 1 | 1 | 22 | 1 | `derive_keyshape` |

No traceback in any run. Each failing arm is one of the six added at `03b66a43` (+3 arms in count-c1.py, +2 in count-c2.py, +1 in count-c3.py),
which is the causal story the contract asserts. Reading: (i) every kill is a parseable FAIL, so
tameshi's `U` class does not bite this round; (ii) the map is 1:1 and unique, so it is free to pins —
no mutant needs an ambiguous expectation.

After writing the table I read the sibling executor report `w1/Mo87E01C1Arms.md` (in the untracked
`w1/` dir at `728bc5f4`, not committed). It reaches the same six killer arms with the same rc and
tallies (`:63-70`), and it carries one control I did not run: neuter **only** the killer arm in the
after subject, re-apply the mutant, and require `rc 0, fail=0,` the frozen arm count (`:17`, `:100-111`)
— which proves the arm is *load-bearing* for the kill, not merely the only arm that happened to fail.
That is the stronger form of my attribution table, and it is exactly the control §7 needs; it lives
today as a wave artifact, not as a graded clause.

---

## 6. `considerthese/2026-10-26.md` — disposition of all four, and the line I would cite

| # | line | proposal | status at `728bc5f4` |
|---|---|---|---|
| 1 | `:46-50` | split pin-check mismatches into "can't run here" and "stale" | **landed** — `corpus/QUALITY.md:1283-1300` (QUALITY 138), `tools/mori-pin-check.py` v5 |
| 2 | `:51-53` | carry unfixed critic flags forward into a next-round ledger | **criterion landed, ledger outstanding** — `corpus/QUALITY.md:1522-1535` (QUALITY 153) itself records "the `carry-over-flag ledger` as outstanding" (`lessons/round-55.md:106`); `lessons/round-58.md:26` says it "remain[s] unimplemented" |
| 3 | `:54-56` | re-execute what closures only evidence-verified | **landed** — `corpus/QUALITY.md:1223-1240` (QUALITY 136, r50) and `:2051-2070` (QUALITY 178, r86), which names this suggestion as its motivation. r87's C2 is its direct extension, so this round does **not** get to claim it |
| 4 | `:57-60` | keep a suggestion-adoption status line | **adopted as a status line** (`lessons/round-58.md:26`), whose own text records the residual I would cite |

**The line I would cite: `considerthese/2026-10-26.md:58-59`** — "suggestion 2 adopted as a criterion
(QUALITY 127) but not yet acted on (count still 13, and new spec builders repeat the path)".

Why that line and not `:54` (which is the round's obvious thematic fit but already landed): QUALITY
127 is "instruments carry no absolute host path", and it is **still unarmed**, while the r87 C2 replay
is the first graded mechanism that can silently depend on it. Measured at `b9e6f68d`:

- `after-c1-r86.txt:2` and `replay-defeat-r86.txt:2` carry `# cmd: python3 -I
  .ufo/waves/round-86/count-c1.py 8764461… --repo /home/vgpnk/Projects/shokunin/mori-shokunin
  --scratch .` — an absolute host path in the recorded command of **two of the seven** population
  receipts, both `# replay: required`.
- `export_rev` (`count-c2.py:150-168`) splits the command on whitespace and skips any token failing
  `PATHISH` (`:62`, `^[A-Za-z0-9_.]…`), so both the leading-`-` flag and the leading-`/` path are
  skipped; the receipt's own line records `exported=1` (the counter only). The replayed command
  therefore runs with `cwd` = the scratch export but `--repo` = the **live lane repo**, and passes
  only because that path exists here.
- The two r87 successors carry no absolute path (`--root . --pins .ufo/...`), so the round already
  demonstrates the better form beside the worse one.

That is exactly QUALITY 182's own disclosed "Not covered" clause — "a command whose output depends on
the environment outside the exported tree" (`corpus/QUALITY.md`, round-87 block) — and QUALITY 127 is
the unlanded arm that would grade it. Do not implement it in this round; it belongs to the L1 to
route, and it is a natural operability carrier in a later round.

Suggestion 2 at `:51-53` is the only wholly-unimplemented numbered proposal, but it does not fit either
of this round's mechanisms; it fits any round that routes defects, so it is a general carry, not a
round-87 fit.

### 6.3 The round's own knowledge entry cites no sibling

`corpus/knowledge/receipt-supersede-r87.md` (at `728bc5f4`) cites S603, S600 and S602 and **no lane**:
`grep -niE 'kama|tameshi|kotodama|kaidoku|kengaku|kasegi|tabi|mado|fleet|sibling|lane'` → only line 63
("it is not a fleet lifecycle, result-acceptance or authorship verdict"). Its `## Limits` are sound
(no authorship, no dependency identity, no side effects, clone completeness), and QUALITY 181's
"Not covered: a successor that verifies but records the wrong revision" is tameshi's
`RECEIPT_REV_CONTENT_DRIFT` class. The two clauses that need a citation are:

1. "A receipt that records a command is bound to that command only by re-executing it" → kama r33
   `tools/round33-gate-receipts.py:414,448`.
2. "A legacy receipt is superseded, never rewritten" → kasegi R8/R54 (`corpus/QUALITY.md:50,401`) and
   kengaku R1/R5 (`corpus/QUALITY.md:161,165`), and the fourth-policy framing from
   `kengaku …/round73/w1/sibling-overlap.md:48`.

The supersede-gated-on-replay clause itself I found **no prior art for** — that is the one part the
lane can hold as its own.

---

## 7. The one bounded move

**Adopt declared-arm attribution for the counter-mutation kill rule: each mutant carries the arm that
must fail, and `killed` is true only when that arm's `FAIL` line is present.**

*Evidence.* §5 measures the map as total, unique and already satisfied: six mutants, six distinct
arms, each added for its mutant at `03b66a43`. The map costs six constants and one regex
(`FAIL <arm>`); the arm labels already exist in the subject bytes, so nothing new is published that
is not already in the r86 counters. The SCORECARD (`728bc5f4`) already **asserts** the map in prose —
"each is killed by the arm added for it (measured line-by-line in the wave's `Mo87E01C1Arms` report)"
— so the move converts a report sentence into a graded clause that a later reader can re-derive
without the report.

*Affected axes.* Operability (the kill rule can now fail for the right reason; a crash stops counting
as a kill, so the r87↔tameshi contradiction in §4.1 closes without touching r87's frozen bytes) and
calibration (the round grades the causal claim "the six clauses get **the failing arm each**", not
only the tally).

*Not harmed.* The r87 predicate is frozen and stays: nothing in `count-c1.py` moves. The new rule is a
strictly stronger predicate that the r87 bytes already satisfy by measurement, so it can land as the
round-88 counter and the r87 claim keeps its after-value.

*Risks.* (i) The arm labels live in the *subject* counters, so a later r86 edit that renames an arm
breaks the map — pin the map to the subject digest with the existing `# counter-sha256:` machinery.
(ii) A future crash-kill would now read `survived`/`unresolved` and could turn a met claim unmet;
that is the honest direction, but it must be disclosed as a behaviour change, not a tightening of an
existing rule. (iii) It is a second published label set, which kotoba Q47 warns about — the guard is
that the *subject* prints the FAIL line and mori's own selftest cannot satisfy it, which is already
true of mori's kills.

*Verification.* (a) The map reproduces `mutants=6 killed=6 survivors=0` at r87 with the six labels of
§5; (b) a **wrong-arm control**: take `M1` and additionally break an unrelated arm so the declared arm
passes — the current rule reads `killed`, the mapped rule reads `survived`; the counter's `selfcheck`
already builds synthetic subjects (`count-c1.py:186-277`), and the sibling's arm-neuter control
(`w1/Mo87E01C1Arms.md:100-111`) already shows the arm is load-bearing, so the fixture exists and only
needs to move into the counter; (c) the do-nothing control stays `killed=0 survivors=6`, and the
entering/label-only controls are unchanged.

*Ownership.* kaidoku r79 owns the declared-case rule, kama r75 owns `EXPECTED_ARMS`, tameshi owns
K/D/E/U. Mori adopts and cites all three; the two-lane admission bar is met without mori claiming the
method.

*Second-order surfaces.* Runtime: one more regex and six constants per graded mutant — negligible.
Contract: the r88 predicate sentence must carry "the arm that must fail", or the counter and the
contract diverge, which is the class QUALITY already polices. Substrate: the map is pinned to subject
bytes, so it ages with the r86 counters rather than with mori's. Verification: the wrong-arm control
is a new "shown able to fail" arm in the counter's own selftest, which is where QUALITY 177's
"Not covered" clause currently has nothing.

**Considered but not proposed** (one line each, no action sought): C2's replay discards stderr where
kama r33 compares it; C2's supersede identity is a basename where kumitate Q19 wants path+index; C2's
`# replay: none` reason is required but not graded against the body's shape.

---

## 8. Contested ownership, routed (not absorbed)

Each row names the lane that owns the rule. Mori must cite or defer; it must not restate as its own,
and mori's frozen predicate is not changed by any of them.

| row | owner | what mori must do |
|---|---|---|
| body-equals-command is a fleet-class rule | **kama** (`tools/round33-gate-receipts.py:414,448`, r33) | cite as prior art; keep only the generic population, clone mode and supersede gating as its own |
| receipt revision binding, incl. content drift | **tameshi** (`tools/receipt-revision-gate.py:45-49`) | cite; mori holds the weaker ancestor leg only |
| declared-case attribution and INCONCLUSIVE | **kaidoku** (`tools/round-79/gate-mutation.py:17-21`) | adopt (§7); do not claim |
| `EXPECTED_ARMS` and `escaped` | **kama** (`tools/round75-survivor-probe.py:20,42,88`) | adopt; align vocabulary or state the difference |
| K/D/E/U survivor adjudication | **tameshi** (`r43-survivor-resolution-rule.md:57-60`) | state which reading the kill rule takes; a crash-kill is `U` under the owner's rule |
| append-only supersede, "superseding does not reject" | **kasegi** (`corpus/QUALITY.md:50,401`) | cite R54 as the reason `after-r85.txt` stays legacy |
| supersede identity (path + index) | **kumitate** (`corpus/QUALITY.md:157-165`) | name the basename limit; do not import |
| latest-row-wins / last-row-wins / reject-duplicates | **tabi, protocol, kengaku** (`…/round73/w1/sibling-overlap.md:48`) | present mori's rule as the fourth policy, never as the correct one |
| fixed-published-mutant-set measure | **kotoba** (`corpus/QUALITY.md:58`) | state the reading; r87 is a record of kills, not a two-sided measure |
| receipt-family map (C-1…C-5) | connector rows at **kaidoku r67 / r77**, **kama r72–74** | cite the map; the class is "established and multiply owned" |
| method admission (two independent lanes) | **tameshi** (`PROVINCE.md:3-16`) | cite kaidoku + kama; never claim the craft |

---

## 9. Negative sweep

Searched and found nothing on either ground, read-only, at the revisions above:

- `grep -rn --include='*.py' --include='*.sh' -E 'replay' *-shokunin/tools/` — 40+ hits; the ones I
  inspected fall into these families: kaidoku r34 shortcut-replay gate, kaidoku r40–49 parameter
  replay, kotodama receipt-seq (no argv), kama r33 (the duplicate), or a selftest's own replay of a
  fixture. **No hit outside kama r33 compares a receipt body to a command's output.**
- `grep -rn -E '#\s*(replay|supersedes|counter-sha256):' *-shokunin/tools/ *-shokunin/corpus/knowledge/`
  — one comment in kama `round64-c1-counter.py:2001` (unrelated prose), mori's own two knowledge
  entries, and no sibling receipt grammar.
- `grep -rn 'mutants=' 'survivors=' 'killed='` over `tools/` and `corpus/knowledge/` — no lane grades
  *its own counter* with a `survivors=` token; tameshi/kama/kaidoku/mado/tsukuroi grade tools,
  fixtures or modules. Mori's exact tally token is its own; its *shape* is not (§3.3, §3.4).
- `*-shokunin/.ufo/waves/round-8{4,5,6}/` — only mori, revenger and kotoba have those directories;
  revenger's are census logs (`census-round-*.log`, `postadjudication-sweep.log`) and kotoba's r84 is
  a receipt directory whose one relevant line is "it stays as filed (unedited) and is superseded by"
  (`receipts/r84-counter-base-regenerated.txt:17`) — append-only, no replay, no overlap.
- No lane holds a **supersede-gated-on-replay** rule. kasegi and kengaku supersede by appending a
  naming row; kumitate by refusing a re-pin; tabi/protocol by position. None requires the successor to
  reproduce a command.

## 10. In-flight and not mine

- `after-r87.txt` and `corpus/knowledge/receipt-supersede-r87.md` were **untracked at scan open**; I
  read them there and re-read the committed bytes. `supersede-controls-r87.txt`, the round lesson and
  QUALITY 181–182 did not exist at scan open and I read them only after the `728bc5f4` landing. Every
  quoted byte above is the `728bc5f4` byte.
- `count-c2.py` changed from `e1dfd45a…` at freeze `142542e0` to `264a43f0…` at A1 `b9e6f68d`; the
  amended bytes are the ones graded and the ones I read. No target, population or supersede rule
  moved (A1's own text).
- The round lesson's `## Gate` writes no row (gate-input absent at its read time), so the routed items
  in §8 have no Gate carrier at `728bc5f4`. That is a record gap for the L1, not a defect this seat
  may close.
- Sibling reports cited above are read-only evidence of *their* rules; no sibling claim is restated
  as my measurement. §5's table is my own run.
