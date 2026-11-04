# Mo84K01Conn — sibling-overlap scan of the three grounds (mori round 84, w1)

Read-only seat. I wrote exactly one file: this report. Nothing in any lane, fleet root,
`.ufo/state/`, MANIFEST/SCORECARD/LOG was written; no mutating git/jj command ran in any lane.
Scratch `/fast/scratch/hyaku/mori-r84/Mo84K01Conn/` was created and deleted before yield.

Revisions used: entering `5adf4337b6510dd246b247092c11cbaa97c930d3`; freeze
`daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4`; lane HEAD at scan open
`dbdb1aaa4d5b293d678a18b15c50a4a55bc90759` (A1); lane HEAD at scan close
`39190f8a` (A2, landed while this seat scanned). The graded `.ufo/waves/round-83/` bytes are
identical at all four (`git diff --stat 5adf4337 dbdb1aaa -- .ufo/waves/round-83/` → empty, and
`39190f8a` touches only `round-84/contract.md` and `round-84/count-c1.py`).

Read first, in order: `round-84/contract.md`, `round-84/evidence/controls-r84.txt`, the three
frozen counters, `round-83/w1/Mo83R01C1.md` §6, `corpus/lessons/round-83-verifier-spotcheck.md`
§routed defects, `SCORECARD.md` §Planned (round 84). Then swept
`{kumitate,kengaku,chousa,tsukuroi,kotoba,tameshi}-shokunin/corpus/` and each `PROVINCE.md`.

The scan found one blocker-class defect in the freeze bytes (§6) — fixed by the L1's amendment A2
during the scan, with one evidence gap left (§7) — and one contested rule boundary that mori's C1
sits directly on (§5.1). Both are reported, neither is resolved here.

---

## 1. Adjacency matrix (all six lanes × three grounds)

`overlap` = same ground, sibling row governs it. `distinct` = adjacent, boundary named.
`contested` = the sibling row and this round's rule cannot both hold as written. `none` = no row
on that ground (negative sweep in §8).

| ground | kumitate | kengaku | chousa | tsukuroi | kotoba | tameshi |
|---|---|---|---|---|---|---|
| (a) equivalent-mutant / mutation adequacy | **overlap** (equivalent recorded, not hidden) | **overlap** (witness-before-freeze; equivalent = limit of the freeze) | **contested (headline) / distinct (check)** | distinct (one incidental instance) | **contested** (fixed equivalent set cannot be a claim) | **overlap — method owner** |
| (b) anchor ambiguity / first-match | **overlap** (occurrence index is anchor identity) | **overlap** (per-row anchor binding) + sibling's own unresolved first-match defect | **overlap** on defect class, **distinct** fix (named line) | distinct (three-class drift census) | none on point (S3) | none (Bash `case` note only) |
| (c) live-vs-snapshot delta | **overlap — closest owner** (which side scores) | distinct (re-run classification) | distinct (live URL vs archive pairing) | **overlap** (three-class drift vocabulary) | none on point (S4) | **overlap** (snapshot is the only citable side) |

---

## 2. Ground (a) — equivalent-mutant adjudication / mutation-adequacy rules

### 2.1 tameshi owns the method (overlap)

- `tameshi-shokunin/PROVINCE.md:3-16` — domain is "verification-fixture craft … mutation testing";
  it owns "the method"; "every lane's gate remains its own; tameshi owns only the reusable craft
  (a pattern is admitted from evidence in TWO independent lanes before it is claimed general)".
  So tameshi owns the *rule*, mori owns its counter; neither substitutes for the other.
- `tameshi-shokunin/corpus/knowledge/r43-survivor-resolution-rule.md:51-66` — the K/D/E/U rule.
  E is empirical and corpus-relative: "`E — equivalent` | The mutant differs from the pristine tool
  on no case in the declared corpus" (`:59`); "A survivor is never relabelled. D and E are named
  classes with their own evidence" (`:64`). `:9-11` states the lane "never decides equivalence by
  assertion".
- `tameshi-shokunin/SKILL.md:2169` — an equivalent is "keep[d] … in the table and the score …
  name it equivalent in the entry; do not count it as a hole". `SKILL.md:250-252` — "If no
  observable input differs, the mutant may be *equivalent code* — record that as a calibration
  item, not as a gap."
- `tameshi-shokunin/corpus/knowledge/witness-equivalence-rule.md:21` — an `accept+vector` witness
  must show *behavioral equivalence* (same `(exit, first-line)` tuple with changed bytes), not a
  textual difference. This is the fleet's set-aware behavioural-equivalence witness, beside
  kengaku's pre-freeze witness rule (named QUALITY Q29 in `corpus/lessons/round-40.md:38`), which
  requires a witness of each mutant's declared direction but does not define equivalence.

**Boundary for mori C1:** mori proves equivalence analytically (coupling marker) and never runs
M24c/M24d against a declared case corpus beyond each tool's own `--selftest`. That is *stronger*
than tameshi's E (a proof implies E), but it is not tameshi's *method*, and the reference survives
only because the marker occurs once. Whether an analytic proof may stand in for tameshi's declared-
corpus witness is a tameshi-owner question; this seat does not decide it.

### 2.2 kumitate (overlap) and kengaku (overlap)

- `kumitate-shokunin/corpus/QUALITY.md:196-198` — "An equivalent mutant is a survivor, not a kill
  (S034), and it is recorded rather than hidden." Same accounting as mori's `equivalent=2`.
- `kengaku-shokunin/corpus/QUALITY.md:441` — "the mutant list is the denominator … an equivalent
  mutant found later is reported as a limit of the freeze, never removed". Adjacent: kengaku's
  equivalent is found *after* the freeze; mori's is registered *before*. Both keep it.
- `kengaku-shokunin/corpus/lessons/round-40.md:38` (O13, labelled reachable, measured equivalent,
  withdrawn before the freeze) and `corpus/lessons/round-41.md:16` (S10 `EQUIVALENT-BY-RC`,
  withdrawn before the freeze) — kengaku's operative discipline is a witness of the declared
  direction *before* the freeze, not an assertion after it.

### 2.3 chousa — headline contested, check distinct

- `chousa-shokunin/corpus/QUALITY.md:958` — "**A frozen mutant set holds no equivalent mutant**; a
  survivor is classified before the target is fixed." The check is narrower than the headline:
  "rebuild the set with each mutant's first edit only and run the counter; a survivor the landed
  builder cannot kill is a mutant-set defect, never a data result."
- mori's M24c/M24d are single-token edits (one conjunct dropped), so they are "first edit only" by
  construction and pass chousa's *check*. They violate chousa's *headline* outright: mori's frozen
  set holds two equivalents by design. **Contested at the headline, compatible at the check —
  report both, absorb neither.**

### 2.4 kotoba — contested, with a measured break

- `kotoba-shokunin/corpus/QUALITY.md:58` (Q47) — "A mutation-kill measure is two-sided … and its
  equivalents are not a fixed published list: a fixed list is a label a self-test can key on, so
  the set is generated at measurement time or the measure stays a record, never a claim." The
  row's scope cell is literally "mutation-sweep counters and claims".
- `kotoba-shokunin/corpus/lessons/round-58.md:61-66` (M75 `fixed-equivalent-set-is-a-label`) —
  kotoba's C2 used a fixed published set of five equivalent rewrites; a source-grep self-test that
  checked the eleven mutant texts met the predicate; **fix: C2 withdrawn before data**.
- The measured break: `kotoba-shokunin/.ufo/waves/round-58/controls/CtlC2SourceGrep.md:1` —
  "Result: BREAKS — A source-text-only self-test met the frozen C2 predicate with K=11, E=5,
  exit 0 without exercising correction-sweep behavior"; `:13` — "the shortcut rejects every frozen
  mutant while accepting every frozen equivalent."

**Why this is the sharpest boundary for mori C1.** `round-84/count-c1.py:52-58` is a fixed,
published `EQUIVALENT` dict keyed by label; `:134-141` counts a survivor `equivalent` when its
label is in that dict and the markers occur once. That is exactly Q47's forbidden shape, and the
counter's own selftest exercises the map. The coupling markers are a proof *of* the registered
pair; they are not a measurement-time *generation* of the equivalent set. Q47 offers two exits —
generate the set at measurement time, or keep the measure a record and not a claim — and mori C1
as frozen takes neither. This is a cross-lane contradiction between kotoba's rule and
tameshi/kumitate/kengaku's "name and keep the equivalent" practice; **mori C1 stands on the
boundary and must state which reading it claims.**

### 2.5 tsukuroi — incidental only

`tsukuroi-shokunin/corpus/lessons/round-68.md:111` — "Five killed; c3 equivalent for the specified
fixture survives". One measured instance, no rule on this ground.

---

## 3. Ground (b) — record-anchor ambiguity / first-match selection

### 3.1 kumitate: occurrence index is already part of anchor identity (overlap)

- `kumitate-shokunin/corpus/QUALITY.md:157-165` (Q19) — "Identity for an anchor is its raw text,
  its resolved path and **its occurrence index**, never the token, the key or any other field the
  edit under test can rewrite" (`:163`). A per-anchor floor; a re-pin refuses any anchor that was
  true and is no longer true (`PIN_REGRESSION`, `:134-146`, Q17).
- `kumitate-shokunin/corpus/QUALITY.md:126-133` (Q16) — a gate that admits anchors is checked
  against symbol-on-line truth with an independent parser against the pinned revision.

**Boundary:** kumitate pins *one* occurrence per anchor and uses the index as identity; mori
grades *every* row a substring anchor selects. Same mechanism (occurrence identity), different
object (pinning vs exhaustive grading). No duplicate.

### 3.2 kengaku: per-row anchor binding, and its own unresolved first-match

- `kengaku-shokunin/corpus/QUALITY.md:383` (Q26) — every `sha256` token in a `SOURCES.md` row must
  sit in that row's `anchor` cell and resolve; `plans/anchor_digest_check.py:60-70` implements
  row-scoped binding with `anchor-unbound` and `digest-wrong-capture`.
- `kengaku-shokunin/.ufo/waves/round-38/build/R38AnchorBind.md:55` — "Every row that carries an
  anchor token is bound — `rows_with_anchor_tokens=15 unbound=0`". That is the closest shape to
  mori's all-anchor-rows requirement, but the unit is the row's *own capture*, not all rows a
  substring selects. Its disclosed limit `:148` — "Multi-capture rows take the first locator source
  only … the checker does not arbitrate which one the anchor means" — is a first-match selection
  the sibling keeps as a named limit.
- The same defect class measured in the sibling's own gate:
  `kengaku-shokunin/corpus/evidence/round73/w1/c2-critic.md:64` — "`check_errata` tests only
  `revision not in items[owners[0]]`; it establishes substring co-occurrence in the first matching
  item, not the asserted relation, polarity, exclusivity, or every item's correctness";
  `kengaku-shokunin/corpus/evidence/round73/w1/c2-blindspots.md:491,524` — "first matching item masks
  a later contradictory binding". The land state still first-matches:
  `kengaku-shokunin/plans/round73_c2_registry_audit.py:196` still reads `items[owners[0]]`.
  This is evidence that the defect class is real in a sibling gate; it is not a rule.

### 3.3 Duplicate-row policies are already partitioned (kengaku's census)

`kengaku-shokunin/corpus/evidence/round73/w1/sibling-overlap.md:48` — "tabi latest-row-wins and
protocol closure-ledger last-row-wins are deliberate append-only supersession policies; C2
deliberately rejects duplicate names and prices every row. Importing either sibling policy would
undo D3." Three policies already exist: *latest wins*, *last wins*, *reject duplicates*. mori's
all-anchor-rows rule is a fourth: *all matching rows must state the same `key=value`*. It must not
claim novelty over the three, and it must not import them.

### 3.4 chousa: same defect class, different fix

- `chousa-shokunin/corpus/knowledge/line-binding-r31.md:20` — "the bound occurrence need not be
  the first one, which is the only one `at=` reports when no line is named." The fix is a *named
  line/range*, not all occurrences.
- `chousa-shokunin/corpus/knowledge/hardening-r10.md:197` — "not location binding or uniqueness
  (`at=` is the first occurrence, informational)" — first-occurrence selection is a documented
  by-design limit of that gate.
- `chousa-shokunin/corpus/evidence/round50/claims-erratum.md:18` — closest precedent for the
  *fix shape*: "the appended row's `used-by` now names the entries citing ANY staged id that maps
  to the row … the old tool kept only the first row's citing entry". A first-row → all-rows fix,
  on the id→entry citation mapping, landed as a post-freeze erratum item.

### 3.5 tsukuroi: three-class anchor-drift census (distinct)

`tsukuroi-shokunin/corpus/knowledge/adjacency-anchors-r19.md:13,43` — inbound pointers classified
`RESOLVES` / `DRIFTED` (content exists at another line) / `UNRESOLVABLE` (absent), each with a
bounded search command. Adjacent: it classifies *where* the anchored content moved; it does not
decide which of several rows an anchor selects.

### 3.6 Does a sibling already own the all-anchor-rows rule?

**No.** Sweep (`§8`, S2) over the six corpora returns no row that grades **every row selected by a
substring anchor** on both a worktree and a revision blob. The nearest owners each bind a different
object:

| sibling row | what it binds | why it is not the same rule |
|---|---|---|
| kumitate Q19 (`QUALITY.md:157-165`) | one occurrence, pinned by index | identity, not exhaustive grading |
| kengaku Q26 + `anchor_digest_check.py:60-70` | each token row to its own capture | row-scoped, first locator wins (`R38AnchorBind.md:148`) |
| chousa line-binding (`line-binding-r31.md:20`) | one named line/range | resolves ambiguity by *naming one*, not by grading all |
| chousa round-50 erratum (`claims-erratum.md:18`) | id → every citing entry | different object (used-by citations) |
| kengaku round-73 C2 (`round73_c2_registry_audit.py:26,163`) | every *registry* row's fields | selection is the registry, not an anchor |

mori's rule is a genuine addition, but it is a fourth duplicate-row policy (§3.3) and it consumes
kumitate's occurrence-index identity (§3.1). It should cite both.

---

## 4. Ground (c) — live-versus-snapshot delta classification

### 4.1 kumitate: the closest owner (overlap)

- `kumitate-shokunin/corpus/knowledge/snapshot-bound-derived-scores.md:9-14` — a score derived
  from a live operator-owned surface MUST read a committed, pinned snapshot by default, MUST
  disclose `source=snapshot`, MUST offer an explicit live mode, and "the live-vs-snapshot
  comparison stays a **separate, non-scoring diagnostic**."
- `kumitate-shokunin/corpus/knowledge/shape-receipt-live-drift.md:13-24` — the comparison contract
  `OMP_SHAPE_COMPARE: IN_SYNC|DRIFT entries= receipt= added= removed= changed= first=`, with
  0/1/2 exits and "This is non-scoring: no proxy term depends on the comparison."

**Boundary:** kumitate's rule answers *which side scores* and keeps the comparison non-scoring;
mori's C3 answers *is every token in the union classified exactly once* and scores classification
completeness, not a delta value. Different propositions, same vocabulary (`added`/`removed`/
`changed` ≈ `added-live`/`absent-live`/`class-changed`). mori should cite this entry for the
vocabulary rather than present it as new.

### 4.2 tameshi: the snapshot is the only citable side (overlap)

`tameshi-shokunin/corpus/QUALITY.md:944-950` (criterion 79) — "A mined row that presents a located
quote as support is not citable until a committed snapshot contains that quote. A live fetch that
cannot be repeated … is not a substitute for the bytes." The general rule behind kumitate's
instance.

### 4.3 tsukuroi (overlap) and the other two (distinct)

- `tsukuroi-shokunin/corpus/knowledge/adjacency-anchors-r19.md:13,43` — `RESOLVES` / `DRIFTED` /
  `UNRESOLVABLE`, a three-class snapshot-vs-tip classification.
- `kengaku-shokunin/corpus/evidence/round12-fleet/r12-review-baseline.md:33` — "`REPRODUCE
  (superseded)` … host disappearance is `DRIFTED-HOST`, not falsification": a re-run-vs-documented
  state classification. Distinct: per-command re-run, not a per-token union.
- `chousa-shokunin/corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md:11` —
  a live URL beside its archive capture; provenance pairing, not delta classes.

### 4.4 mori C3's own reading (checked, not asserted)

`round-83/count-c2.py:244-249` computes `tokens = len(snapshot_tokens)` (snapshot side) and prints
`live_tokens=` / `live_agree=` separately; `.ufo/waves/round-83/count-c2.py:21-22` says the live
numbers are "readings, not required — the census is a live observation, the classification is
bound to the snapshot." `round-84/count-c3.py:195` grades `tokens == 64`, i.e. the **snapshot**
count; `live_tokens` is unconstrained. That is kumitate's rule, honored.

**Wording ambiguity, clarified by A3 at scan close:** the C3 contract sentence "met never requires
a particular token count" reads as a contradiction of `count-c3.py:195` unless it means the *live*
count. An uncommitted A3 block at the end of the worktree `contract.md` (filed from seat
`Mo84S02Quality`'s finding, after A2) now states exactly the reading derived here: `tokens=64` is
the snapshot's own token-line count fixed by the committed snapshot, and the live side is graded
only by `classified == union`, `deltas == union - live_agree` and `live=derived`. No predicate
change is proposed or needed.

---

## 5. Contradictions, stated not smoothed

1. **Equivalence disposition.** tameshi (`SKILL.md:2169`, `r43…:59-66`), kumitate
   (`QUALITY.md:198`) and kengaku (`QUALITY.md:441`) say: name the equivalent, keep it in the
   table/score, never count it as a kill. kotoba (Q47, `QUALITY.md:58`; M75, `lessons/round-58.md:61-66`)
   says: a fixed published equivalent set is a label a self-test can key on, so a measure using one
   stays a record, never a claim — and kotoba withdrew its own C2 over exactly this. chousa's
   headline (`QUALITY.md:958`) forbids a frozen set holding an equivalent at all. mori C1 counts
   `equivalent=2` from a frozen map; three sibling positions exist and cannot all bind. **The
   round must name the position it takes; this seat does not choose it.** At scan close the lane
   carries an untracked knowledge entry `corpus/knowledge/equivalent-mutant-adjudication-r84.md`
   (66 lines) that states the exemption rule and its coupling discipline but cites only S599 and
   none of these sibling positions (`grep -niE 'kotoba|Q47|tameshi|fixed|two-sided'` → no hits), so
   the boundary is still unstated in the lane's own record.
2. **Anchor policy.** Three duplicate-row policies are already partitioned among siblings
   (`kengaku …/sibling-overlap.md:48`); mori adds a fourth. If the round presents all-rows as the
   only correct policy, it contradicts tabi/protocol's deliberate supersession policies. State the
   Fourth policy, do not import or condemn the other three.
3. **Snapshot side.** kumitate and tameshi require the snapshot to be the scored side; mori C3
   conforms (§4.4). Any future C3 arm that grades `live_tokens` would contradict both.

---

## 6. C1 anchor defect in the freeze bytes — independent confirmation, and the landed A2

This is not a sibling finding; it is a defect in the frozen grader, found while checking ground
(a). It was fixed by the L1's amendment A2 **while this seat was scanning**; the measurements below
are the pre-A2 and post-A2 states, both executed.

### 6.1 Freeze-state measurement (pre-A2 counter, from git bytes)

The counter as committed at the freeze `daa77bd` and at `dbdb1aaa`, run from a scratch copy of
`git show dbdb1aaa:.ufo/waves/round-84/count-c1.py` against the freeze's subjects:

```
$ python3 -I <scratch>/frozen-count-c1.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <scratch>
MUTANT count-c1.py M24a_killed_tally survived rc=0
EXTRA unanchored .ufo/waves/round-83/count-c1.py M24b_green_fail_token occurrences=2
EXTRA unanchored .ufo/waves/round-83/count-c2.py M24c_met_unclassified occurrences=0
EXTRA unanchored .ufo/waves/round-83/count-c2.py M24d_met_residual occurrences=0
C1=unmet mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=green detector=green
rc=1
```

At the entering revision the harness guard fires first: `C1=unmet harness=absent
rev=5adf4337b651`, rc 1. The contract (`contract.md` §P-C1) declares the freeze population control
as `C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 ...`; **the pre-A2 counter cannot print
that line.**

### 6.2 Root causes (byte-level)

- **M24b** `old` = `return rc == 0 and "fail=0" in out and not FAIL.search(out)` occurs **twice**
  in `.ufo/waves/round-83/count-c1.py`: line 33 (the catalogue literal for the r82 mutant
  `green_ignores_fail_token`) and line 129 (the live `green()` body). The frozen precondition
  `base.count(old) != 1` (`round-84/count-c1.py:119`) therefore reports `unanchored` and never runs
  the mutant.
- **M24c/M24d** `old` = `and not unclassified and residual == 0` occurs **zero** times in
  `.ufo/waves/round-83/count-c2.py`: the `met` expression wraps after `and not unclassified`
  (line 241) and continues `and residual == 0` (line 242). The flat string in the freeze table
  (`contract.md:42-43`) and in `round-84/count-c1.py:42,45` is a transcription artifact of the
  r83 reviewer's rendered table.
- Both facts also hold at the r83 reviewer's revision `c4845c83`, so §6 of
  `round-83/w1/Mo83R01C1.md` rendered its anchors flat while its driver evidently used the wrapped
  bytes. M24a is sound at every revision checked.

### 6.3 A2 landed during this scan (HEAD `39190f8a`)

`git log --oneline` at the end of the scan:

```
39190f8a round-84: pre-data amendment A2 (M24b/M24c/M24d anchors corrected; population control now mutants=4 survivors=2)
dbdb1aaa round-84: pre-data amendment A1 (fixture finding line numbers; no predicate change)
daa77bd5 round-84: freeze contract, counters and entering controls (C1 operability, C2 calibration, C3 depth)
```

`contract.md:163` opens "Pre-data amendment A2 — the M24b/M24c/M24d anchors corrected (no
predicate, target or kill-rule change)". A2 diagnoses the same three anchors and names seat
`Mo84S02Quality` and the L1 as independent finders; this seat's measurement is a third,
independent one. A2's replacement anchors, measured with `str.count` over `git show <rev>:<path>`:

| label | A2 `old` anchor | count at 5adf4337 | count at daa77bd | count at 39190f8a |
|---|---|---|---|---|
| M24b | `    return rc == 0 and "fail=0" in out and not FAIL.search(out)` (four-space indent) | 1 | 1 | 1 |
| M24c | `and not unclassified` | 1 | 1 | 1 |
| M24d | `and residual == 0` | 1 | 1 | 1 |

The A2 counter reproduces the declared control at the freeze commit, and preserves the entering
control:

```
$ python3 -I .ufo/waves/round-84/count-c1.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4 ...
MUTANT count-c1.py M24a_killed_tally survived rc=0
MUTANT count-c1.py M24b_green_fail_token survived rc=0
MUTANT count-c2.py M24c_met_unclassified equivalent rc=0
MUTANT count-c2.py M24d_met_residual equivalent rc=0
C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 total=4 pristine=green detector=green rev=daa77bd5684c
rc=1

$ same counter at 5adf4337...
C1=unmet harness=absent rev=5adf4337b651
rc=1

$ python3 -I .ufo/waves/round-84/count-c1.py --selftest ...
C1_COUNTER_SELFTEST pass=11 fail=0
rc=0
```

My independent repair (a different M24b anchor: the two-line `def green(rc, out):` context, plus
the wrapped M24c/M24d string) also reproduced the control and kept the counter's own selftest green
(`C1_COUNTER_SELFTEST pass=11 fail=0`, rc 0). Two different anchor choices converge on the same
graded line, which strengthens the diagnosis: the defect was transcription, not predicate.

**Operability reading:** the freeze-time blocker is closed by A2. C1 remains unmet only until the
C1 seat lands its two arms (the population control is `killed=0`, as declared pre-data).

### 6.4 Remaining gaps

1. **No population-control receipt.** `git show --stat 39190f8a` lists exactly two files
   (`contract.md`, `count-c1.py`); `.ufo/waves/round-84/evidence/` still holds only
   `controls-r84.txt`. A2 asserts the measured population control but commits no receipt, the
   D83-1 class. The contrast pair is in §6.1/§6.3 of this report only.
2. **Stale flat substring in two freeze sentences.** `contract.md:42-43` (the P-C1 table's `old`
   column) and `contract.md:128-129` (P-C3: "The substrings `and not unclassified and residual ==
   0`, … must each still occur exactly once") still carry the flat string, which occurs zero times.
   A2's table (`contract.md:179`) and its replacement-anchor table correct the anchors and restate
   E03's preservation obligation, so the contract read with A2 is coherent; a reader who stops at
   P-C3 reads an unsatisfiable clause. No round-84 counter grades that preservation sentence
   (`grep -n 'and not unclassified\|and residual == 0\|agreed == len\|residual += duplicates\|duplicates == 0'`
   over `count-c2.py`/`count-c3.py` returns only `count-c3.py:197`'s tail `residual == 0`), so it is
   ungraded prose, not a second blocker. Correct it in a later record entry; do not rewrite the
   filed text.

---

## 7. One bounded proposed move

**Commit the freeze population-control receipt — `.ufo/waves/round-84/evidence/population-control-r84.txt`
— carrying the two measured lines and their exact commands: the pre-A2 counter at `daa77bd`
(`mutants=1 … survivors=1`, three `unanchored` extras) and the A2 counter at `daa77bd`
(`mutants=4 killed=0 equivalent=2 survivors=2 total=4`), each naming the counter revision it ran at
(`39190f8a`) and the subject revision (`daa77bd`).**

*Evidence.* §6.1 and §6.3 (executed); `contract.md` §Measurement protocol 1 ("The counters are run
at the entering revision … and at the freeze commit before any seat writes; both receipts are
committed under `.ufo/waves/round-84/evidence/`"); A2's own text; the routed defect D83-1
("status-neutral, evidence gap … the claims are derivable but not receipted"). Sibling grounding:
chousa `corpus/QUALITY.md:203` ("A declaration's named input set is complete at its own freeze
revision, and every literal count it states binds to a committed receipt") and `:974` (criterion
115, a frozen counter must demonstrate its positive verdict path before it binds round data).

*Affected axes.* Operability improves: the C1 baseline becomes provable from committed bytes and
the A2 amendment is dated pre-data by a receipt rather than by prose; the after-run has a receipted
before-state. Calibration and depth are untouched: no predicate, target, kill rule, counter or
fixture changes, and no other file is written.

*Risks.* (i) A receipt generated now must name the counter revision it ran (`39190f8a`) and the
subject revision (`daa77bd`), or it becomes exactly the named limit in chousa
`corpus/QUALITY.md:908` ("a receipt can name a revision it did not run at"). (ii) Keep both lines:
dropping the pre-A2 line hides the amendment's before-state, the D83-1 failure mode itself.
(iii) If the L1 prefers to fold the pair into the after receipt, the freeze baseline then lives in
a later file; that is weaker but not false, provided the subject revision is named.

*Verification.* The receipt's two commands are §6.1 and §6.3 verbatim; re-running them must print
the same two lines with the same `rev=` tails, and `ls .ufo/waves/round-84/evidence/` must then show
the file beside `controls-r84.txt`.

---

## 8. Verification ledger

Every command below was run read-only from `/home/vgpnk/Projects/shokunin/mori-shokunin` unless
noted; `<scratch>` = `/fast/scratch/hyaku/mori-r84/Mo84K01Conn`.

| id | command | result |
|---|---|---|
| S1 | `grep -rniE 'mutation.adequa\|equivalent mutant\|mutant.*equivalen\|equivalen.*mutant' <6 lanes>/corpus` | hits in all six; per-lane file counts kumitate 5, kengaku 6, chousa 8, tsukuroi 1, kotoba 8, tameshi 36 |
| S2 | `grep -rniE 'every row (carrying\|that carries\|selected)\|all rows (carrying\|that carry)\|row carrying the anchor' <6 lanes>` | no rule hit in any `corpus/`; the only hits are wave artifacts (`kengaku …/R38AnchorBind.md:55`, kumitate round-61/62 probes) |
| S3 | `grep -rniE 'first[- ]match\|first matching\|first occurrence\|anchor.*ambig\|row_contains' <6 lanes>/corpus` | the rows cited in §3; per-lane file counts kumitate 6, kengaku 9, chousa 9, tsukuroi 7, kotoba 7, tameshi 8 (most incidental; only §3 rows opened) |
| S4 | `grep -rliE 'live.vs.snapshot\|snapshot.*live\|delta class\|IN_SYNC\|DRIFTED\|absent.live' <6 lanes>/corpus` | per-lane file counts kumitate 26, kengaku 30, chousa 18, tsukuroi 43, kotoba 36, tameshi 63; only §4 rows are on point |
| C1 | committed counter at `5adf4337…` | `C1=unmet harness=absent rev=5adf4337b651`, rc 1 |
| C2 | **pre-A2** counter from `git show dbdb1aaa:.ufo/waves/round-84/count-c1.py`, at `daa77bd` | `C1=unmet mutants=1 killed=0 equivalent=0 survivors=1 total=1 …`, rc 1, 3 `unanchored` extras (§6.1) |
| A1 | my scratch patch `--selftest` | `C1_COUNTER_SELFTEST pass=11 fail=0`, rc 0 |
| A2 | my scratch patch at `daa77bd` / `dbdb1aaa` | `C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 total=4 …`, rc 1 |
| A3 | **landed A2** counter (`39190f8a`) at `daa77bd` and at `39190f8a`; `--selftest` | same declared control, rc 1; at `5adf4337` → `harness=absent`, rc 1; selftest `pass=11 fail=0`, rc 0 (§6.3) |
| K1 | `str.count` of the flat/wrapped anchors over `git show <rev>:<path>` at three revisions | pre-A2 M24b 2/2/2, flat M24c-M24d 0/0/0; A2 anchors 1/1/1; coupling markers 1/1/1 (§6.2, §6.3) |
| K2 | `git diff --stat 5adf4337 dbdb1aaa -- .ufo/waves/round-83/` | empty — the graded subjects did not move during the freeze |
| K3 | `git diff daa77bd dbdb1aaa -- .ufo/waves/round-84/` | A1 contract block only; counters and anchors unchanged at `dbdb1aaa`; A2 lands later at `39190f8a` |
| K4 | `git show --stat 39190f8a` | 2 files (`contract.md`, `count-c1.py`); no evidence file added (§6.4) |
| K5 | grep for the P-C3 preservation substrings over `count-c2.py`/`count-c3.py` | only `count-c3.py:197`'s tail `residual == 0`; the source-byte preservation sentence is ungraded (§6.4) |

Quote lines were opened in the cited files; every `path:line` above was read, not inferred from a
grep hit alone. No tool was installed; pacman was not invoked.

---

## 9. What I could not verify

- Whether kotoba Q47 binds a lane outside kotoba. Its province is prompt/skill craft; the row's
  scope cell claims mutation-sweep counters and claims. The contradiction in §5.1 is reported; the
  authority question belongs to the fleet root, not this seat.
- Whether tameshi would accept an analytic coupling proof as an E witness. tameshi's E is
  corpus-relative and its lane "never decides equivalence by assertion"; mori asserts a proof. The
  boundary is stated; no adjudication is made here.
- The C1/C2/C3 after-values: none exists at scan close. A2 is landed but no seat has landed an arm;
  C1's declared population control is reproduced, `killed=0`. The A2 ground truth is committed
  bytes; my scratch patch is corroboration only.
- Whether the C1/C3 seats' arms will reach the declared counts: E01 must kill M24a/M24b and E03
  must preserve the two wrapped conjuncts. Both are other seats' assignments, not verified here.
- Whether the A2 evidence gap (§7) will be closed by the L1 or folded into the after receipt.

## 10. Files written

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/w1/Mo84K01Conn.md` (this file).
- Scratch `/fast/scratch/hyaku/mori-r84/Mo84K01Conn/` (amended counter copy, pre-A2 copy, outputs)
  removed after the measurements.
- Four transient anchor-count dumps (`/tmp/x1.py`, `/tmp/x2.py`, `/tmp/c1.py`, `/tmp/c2.py`) were
  written by the first `str.count` check and deleted immediately; none is cited and no measurement
  rests on them (the reported counts were re-derived from `git show` within the same commands).
