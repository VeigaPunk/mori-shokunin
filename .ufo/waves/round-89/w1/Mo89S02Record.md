# Mo89S02Record — round-89 lesson / QUALITY draft, and the correction of record (calibration)

seat: Mo89S02Record (scribe, axes: calibration) · lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
L1: MoriR89 · wave: mori-r89-w1 · round 89 attempt 1 · milestone: *Draft mistake lesson and correction of record*

**Scope discipline.** This seat writes **one file**: this report, plus a scratch tree it has since
deleted. It wrote **no corpus byte** (no lesson, no QUALITY row, no README row, no SOURCES row, no
knowledge entry) and **no product/instrument byte**; it did not commit, push, or touch the
production checkout, the fleet root, or any sibling repo. The corpora edits that exist in the
working tree (below, §2.6) are **not mine** — I wrote no corpus byte and can attribute them to no
commit (`git status --porcelain` shows ` M corpus/README.md` and
` M corpus/knowledge/receipt-counterfeit-r88.md`, uncommitted).

Everything below is *proposed text for L1 to land*, with the measurement that grounds it.

---

## 0. What I ran (exact commands, rc, inputs, digests)

All work is read-only over the lane plus scratch copies. **No lane-owned gate was executed** — the
registered round-89 counters (`.ufo/waves/round-89/count-c1.py`, `count-c2.py`) were never run, and
no lane checkout was graded. My scratch runs were on *copies* of subject bytes under my own scratch
root, used only to characterise a control fixture; they produced no claim value.

| # | command (abridged) | rc | result |
|---|---|---|---|
| 1 | `git -C <lane> log/status/show` over `30a29797012281b9fd0c748b38b929ac67f8c754`, `760428abf925d98025b34bf23f2cbf54cbeb3bca`, `1bd5ec3fa260458f74eb32a2e5bb157209c5934d`, `d5e2eda494877a85edaa4e287d6ad81843d9a8a1` | 0 | HEAD = `760428ab…` (round-89 C1 landing); no C2 landing exists yet |
| 2 | `git show <rev>:.ufo/waves/round-87/count-c2.py` — entering vs after byte diff | 0 | entering has **0** occurrences of `missing-replay|cmd-binding|def binding_problems|def declared_replay_problem|def absent_supersede_targets`; after has **9** |
| 3 | `git show 1bd5ec3f:…/round-87/count-c2.py` lines 297-302 | 0 | entering gate **already** refused an absent supersede target (`if target not in known:` → `unexpected+=1`, `SUPERSEDE … absent=1`, `ok=False`) |
| 4 | `grep -c 'cases.append('` on r87 gate at `1bd5ec3f` / `d5e2eda4` | 0 | **17 → 23** (six arms added in r88) |
| 5 | `git show <rev>:…/round-88/count-c1.py` lines 93-99 | 0 | r88 kill rule = `rc != 0 or bool(FAIL.search(out))` — no declared-arm attribution |
| 6 | scratch: export `count-c1.py`/`count-c2.py` at `30a2979` via `git show`, apply **verbatim** the `controls-r89.sh` §2a/§2b patches, run `python3 -I <copy> --selftest --scratch <my scratch>` with `TMPDIR` set | 0 | §2a patched r87 gate: `pass=26 fail=0` (green). §2b patched r88 count-c1: `FAIL per_file_arms_frozen 24`, `FAIL own_arms_pinned 25/28`, `pass=26 fail=2`, rc=1 (**red**). §2b patched r88 count-c2: `pass=26 fail=0` (green) |
| 7 | scratch: apply the two declared C1 mutation anchors to the §2b-patched count-c1 copy, run its `--selftest` | 1 | both mutants: rc=1, FAIL lines = the **same two** (`per_file_arms_frozen`, `own_arms_pinned`), **no** `FAIL arms_last_tally` / `FAIL green_mixed_fail` |
| 8 | scratch: a *sound* §2b variant (three labels inserted **before** `own_arms_pinned`, `EXPECTED_ARMS` 25→28, `ARMS_BY_FILE`/`per_file_arms_frozen` kept consistent) | 0 | pristine `pass=28 fail=0` (green); both C1 mutants then read rc=0, **no FAIL line** (green) |
| 9 | scratch: `python3 -I <copy of candidates/r88-count-c1.py> --selftest` / `…/r88-count-c2.py` | 0 | `C1_COUNTER_SELFTEST pass=28 fail=0`; `C2_COUNTER_SELFTEST pass=26 fail=0` |
| 10 | `grep`/`sed` sweeps over `corpus/`, `.ufo/waves/round-8*/`, `LOG.md`, `SCORECARD.md` for the newness claim and its mentions | 0 | every mention listed in §2.5 |
| 11 | `sha256sum` over the frozen contract, both frozen counters, the controls receipt, the two candidates | 0 | `d6b7ec25…` contract · `f8e6c39e…` count-c1 · `40eacccc…` count-c2 · `ba8c58f8…` controls-r89.txt · `d5b83c77…` cand c1 · `6c2ac8fd…` cand c2 |

Digests of the subjects I read: r88 count-c1 at `30a2979` = `3ba0f97b…` (unchanged by the C1
landing); r87 gate at `30a2979` = `7e577f53…`; r87 gate at `760428ab` = `d7ea961a…`.
Scratch root: `/fast/scratch/hyaku/mori-r89/Mo89S02Record/` — **deleted** before yield.

Tooling: none installed or upgraded (no pacman/uv/npx transaction). `git`, `python3` 3.14.8,
`sha256sum`, `grep`/`sed` — all pre-installed.

---

## 1. Summary of findings (calibration axis)

| # | finding | severity | status |
|---|---|---|---|
| F1 | The r88 newness claim is overstated in **two corpus files** and under-specified in a third: the gate added **two** new refusal conditions (`missing-replay`, token `cmd-binding`) plus a helper+coverage extraction over an **existing** refusal (absent supersede target), not three new conditions. | medium (record accuracy) | errata text drafted below; L1 lands |
| F2 | The round-89 **skip-work control 2b is confounded on its `count-c1.py` leg**: the control's own patch breaks two of that subject's self-pin arms, so the patched pristine is **red at 26/28**, and the recorded `arms=26,26` is 26 *passes* of a broken subject, not the intended **28,26** green configuration. The two `unattributed` count-c1 mutant lines are red for that pre-existing reason, not because the attribution rule discriminated. | **high** (the control overclaims) | demonstrated in scratch (§3); L1 must not cite 2b as proof the attribution rule rejects a forger |
| F3 | The round-89 C1 counter's `FX <kind> accepted|refused` label **changes meaning between runs** for the same fixture (`FX comment refused problems=-` at entering vs `FX comment accepted problems=cmd-binding` at the landing). This is the r88-routed FX-wording defect reappearing with opposite polarity. The frozen predicate line is unaffected. | low-medium (legibility) | draft erratum/lesson row below |
| F4 | The `execution-binding-r89.md` cross-reference in the pending knowledge errata points at a **file that does not exist** in the repo (the sources seat proposes `cmd-binding-r89.md` instead). | medium (pointer resolves? QUALITY 9) | flag for L1 |
| F5 | Prior round-88 defects **D2** (genuine `./path` replay falsely refused) and **D3** (a kill credited from an unrelated nonzero exit) are now *specified* fixed, with pointers below; D3's fix is **specified but not yet demonstrated end-to-end** (no C2 landing, no after-receipt). | medium | pointers below |

---

## 2. F1 — the newness attribution: measurement, errata, and every-mention sweep

### 2.1 What the claim says, where

| site | text |
|---|---|
| `corpus/knowledge/receipt-counterfeit-r88.md:11-14` | "The round instrument `.ufo/waves/round-87/count-c2.py` **adds three necessary conditions** to its existing ancestry, digest, summary-token and replay checks." |
| `corpus/README.md:919` | "**Three further necessary checks** in the fixed seven-receipt instrument: parsed replay marker, whitespace-token binding and present supersede target." |
| `corpus/lessons/round-88.md:29-31` | "the r87 receipt gate **gains three refusal paths** (`declared_replay_problem`, `binding_problems`, `absent_supersede_targets`) and six arms (selftest 17 → 23)" |
| `corpus/lessons/round-88-verifier-spotcheck.md:60` | the **detection** of the defect, already stating the correct formulation |
| `.ufo/waves/round-88/w1/Mo88S02Knowledge.md:325` | "adds three further necessary conditions" (seat report; the origin of the corpus wording) |
| `.ufo/waves/round-88/w1/Mo88S01Lesson.md:102` | "adds three refusal paths" (seat report) |

### 2.2 What is actually new (measured, not recalled)

- **New refusal #1 — `missing-replay`.** Entering r87 gate at `1bd5ec3f`: **0** occurrences of
  `declared_replay_problem` / `missing-replay`. After r88 (`d5e2eda4`): present
  (`.ufo/waves/round-87/count-c2.py:133-136`, call site `:261`). Five r88 arms cover it
  (`missing_replay_required`, `missing_replay_clone`, plus the fixture arms).
- **New refusal #2 — token `cmd-binding`.** Entering r87 gate: **no** `binding_problems` function
  at all (the binding check was digest-only, `sha256_at`). After r88: `binding_problems` at
  `:140-145`, call site `:264`. Three r88 arms cover it (`binding_not_in_cmd`,
  `binding_in_cmd_ok`, `binding_skipped_for_legacy`).
- **NOT new — the absent supersede target refusal.** Entering r87 gate, `grade_population`
  (bytes at `1bd5ec3f`, lines 297-302) already contains
  `known = set(present)` / `for name, target in superseders:` / `if target not in known:` →
  `counts["unexpected"] += 1`, `lines.append("SUPERSEDE %s target=%s absent=1")`, `ok = False`.
  **Behavioural proof in a committed receipt**: `.ufo/waves/round-88/evidence/controls-r88.txt:65`
  — the *entering* gate reading `FX absent-target rc=1 refused supersede-absent=1`. What r88 added
  here was **extraction** of the predicate into `absent_supersede_targets` (`:148-150`, call site
  `:323`) plus one coverage arm (`absent_target_helper`) — i.e. a helper and coverage, not a new
  condition.

**Correct formulation:** round 88 added **two** new refusal conditions (`missing-replay`; token
`cmd-binding`) to the r87 gate, and **extracted** the already-existing absent-supersede-target
refusal into a helper with new coverage. The three-condition *decision table* in the knowledge
entry is unchanged and remains correct as a description of the instrument's checks; only the
*newness attribution* at lines 11-14 (and the README row) is overstated.

Corroboration that this is a live, not cosmetic, defect: the counter's own arm census moved
17 → 23 in r88 (six arms: five for the two new conditions, one for the pre-existing refusal), and
`corpus/lessons/round-88.md:31` counts them as "six arms" — the arm census and the "three
conditions" claim cannot both be read the same way.

### 2.3 Proposed named append-only errata (L1 lands; old bytes preserved)

Per QUALITY 4 (errata are append-only blocks) the correction is an **appended** block; the
original bytes at `:11-14` and `:919` are **not** edited.

**(a) `corpus/knowledge/receipt-counterfeit-r88.md`** — append at end of file:

```markdown
## Round-89 correction of record — newness, not the number of conditions

Supersedes the attribution at lines 11–14, not the three-condition decision table.
Round 88 added **two** new refusal conditions to this gate — `missing-replay`
(`declared_replay_problem`) and token `cmd-binding` (`binding_problems`) — and **extracted**
the already-existing absent-supersede-target refusal into the helper
`absent_supersede_targets` with new coverage for it. The entering r87 gate already refused an
absent supersede target (`if target not in known:` in `grade_population`; the r88 entering control
reads `FX absent-target rc=1 refused supersede-absent=1`), so that refusal is not a round-88
addition. Ground: `corpus/lessons/round-88-verifier-spotcheck.md`, "Newness attribution defect
found by this closure"; gate bytes at `1bd5ec3fa260458f74eb32a2e5bb157209c5934d` (entering) and
`d5e2eda494877a85edaa4e287d6ad81843d9a8a1` (after). The original lines remain historical, not a
standing claim of three new behaviors.
```

**(b) `corpus/README.md`** — append after the Round-88 row:

```markdown
## Round-89 correction of record — receipt-counterfeit newness

Supersedes “Three further necessary checks” in the Round-88 row above **as a newness claim**:
round 88 added **two** new refusal conditions (`missing-replay`; token `cmd-binding`) plus a
helper/coverage extraction for an **existing** refusal (the absent supersede target, already
refused by the entering gate). The three-condition decision table itself is unchanged.
Ground: `knowledge/receipt-counterfeit-r88.md`, “Round-89 correction of record”;
`lessons/round-88-verifier-spotcheck.md`, “Newness attribution defect found by this closure”.
Historical row bytes are preserved.
```

> **F4 (blocking for (a)).** The pending knowledge errata in the working tree ends with
> "see `execution-binding-r89.md` for the measured positives, counterfeits and limitations."
> **No such file exists** (`find . -name '*execution-binding*'` → nothing; `corpus/knowledge/` has
> 95 files, none for r89). The sources seat (`w1/Mo89S01Sources.md`) proposes the r89 entry as
> `corpus/knowledge/cmd-binding-r89.md`. L1 must land that file and repoint the sentence, or drop
> the sentence. A pointer that does not resolve at the carrying commit fails QUALITY 9.

**(c) `corpus/lessons/round-88.md`** — append at end of file (the gap in the sweep: this lesson
carries the same three-count wording and currently has **no** errata):

```markdown
## Round-89 correction of record — the round-88 C2 refusal paths are two new refusals and one extraction

Supersedes the wording at lines 29–31 ("the r87 receipt gate gains three refusal paths"), not
the round's arm census ("six arms (selftest 17 → 23)", which is correct and unchanged). Round 88
added two new refusal conditions (`missing-replay`; token `cmd-binding`) and one **extracted**
helper with coverage (`absent_supersede_targets`) over a refusal the entering gate already
enforced. Ground: `corpus/lessons/round-88-verifier-spotcheck.md`, "Newness attribution defect
found by this closure"; `knowledge/receipt-counterfeit-r88.md`, "Round-89 correction of record".
```

### 2.4 Every-mention sweep (all mentions, with disposition)

Sweep commands: `grep -rn "three necessary\|three further\|Three further\|three conditions\|Three
conditions\|three refusal\|adds three" --include=*.md .` over the whole lane, plus targeted greps of
`corpus/`, `LOG.md`, `SCORECARD.md`, `.ufo/waves/round-8*/`.

| # | site | wording | disposition |
|---|---|---|---|
| M1 | `corpus/knowledge/receipt-counterfeit-r88.md:11-14` | "adds three necessary conditions" | **needs errata** — §2.3(a). Old bytes preserved. (A block with this content already exists as an uncommitted working-tree edit, written by someone other than me; my text is the version to land, minus the dangling `execution-binding-r89.md` sentence.) |
| M2 | `corpus/README.md:919` | "Three further necessary checks" | **needs errata** — §2.3(b). Old bytes preserved. (Also already present as an uncommitted working-tree edit.) |
| M3 | `corpus/lessons/round-88.md:29-31` | "gains three refusal paths" | **needs errata** — §2.3(c). Not yet present in the working tree; the r88 closure's routed item 1 named only the knowledge entry and the README. |
| M4 | `corpus/lessons/round-88-verifier-spotcheck.md:60` | the closure's detection sentence, already giving the correct formulation | **no change** — it is the ground for M1/M2/M3 |
| M5 | `.ufo/waves/round-88/w1/Mo88S02Knowledge.md:325` | "adds three further necessary conditions" | **no byte edit** — historical seat report under a closed wave; the corpus errata (M1/M2) is the correction of record. Named here so the sweep is complete, not silent. |
| M6 | `.ufo/waves/round-88/w1/Mo88S01Lesson.md:102` | "adds three refusal paths" | **no byte edit** — same as M5 |
| M7 | `LOG.md:5486-5490` (r88 entry) | "the r87 receipt gate refuses the two counterfeits … — `missing-replay` … `cmd-binding` — **arms its** `SUPERSEDE … absent=1` branch" | **already correct — no change.** The LOG already distinguishes the two new refusals from the armed existing branch |
| M8 | `LOG.md:5513` (r88 routed-defect disposition) | "the two refusal paths, the absent-target arm" | **already correct — no change** |
| M9 | `corpus/QUALITY.md:183-185` | criteria 183 (`missing-replay`), 184 (`cmd-binding`), 185 (no-harm vs equivalent valid inputs) | **no change** — each names one condition; none asserts "three new conditions" |
| M10 | `corpus/lessons/round-87.md:115,132-134` | the r87 record that `missing-replay` was **dropped** in r87 and routed for restoration in r88 | **no change** — it already frames r88's `missing-replay` as a restoration of a dropped r86 rule, not a novel condition. M1–M3 are consistent with it |
| M11 | `corpus/knowledge/receipt-counterfeit-r88.md:16-24` (the three-row table) and `:26-28` | the decision table | **no change** — a correct description of the instrument's checks; the errata explicitly preserves it |

### 2.5 Working-tree corpus state (not mine) — for L1

`git status --porcelain` shows ` M corpus/README.md` and
` M corpus/knowledge/receipt-counterfeit-r88.md` (uncommitted; mtime 18:02:26). Their content is
the M1/M2 correction of record; the README block's wording matches §2.3(b) and the knowledge
block's wording matches §2.3(a) — **except** its final sentence, which points at the non-existent
`execution-binding-r89.md` (F4). I verified their factual claims against the bytes (§2.2): both are
correct as written.

---

## 3. F2 — the skip-work C2 control (2b) is confounded on its `count-c1.py` leg

**Claim under test (contract §2, control 2b):** "the r88 counters with twelve always-passing arms
appended (labels present, no assertion) → `C2=unmet mutants=7 killed=0 survivors=5 unattributed=2
unanchored=5 arms=26,26`: the five refactored anchors stay absent and the two mutations that break
another arm's assertion are refused as `unattributed`, not counted killed — the attribution rule
doing its job on the forger."

The recorded receipt matches that string exactly (`evidence/controls-r89.txt:64`:
`C2=unmet mutants=7 killed=0 survivors=5 unattributed=2 unanchored=5 arms=26,26 detector=green
rev=b4984fb6d4dd`, rc 1). **The control is therefore not a deviation from its frozen expectation —
the expectation itself is the problem, and the executed control is confounded.**

### 3.1 What the receipt already says, read closely

- `evidence/controls-r89.txt:51` — `EXTRA pristine-red .ufo/waves/round-88/count-c1.py rc=1 arms=26`.
  The control's own **pristine** count-c1 subject was **red**. The counter's `grade()` therefore set
  `pristine_ok=False` (`count-c2.py:171-173`) and the verdict was `unmet` **before any mutant was
  graded**. The `arms=26` in the tail is `arm_list`'s **pass count** of that red subject
  (`count-c2.py:170` `arm_list.append(passed)`), i.e. 26 passes out of 28 cases — not "26 arms".
- The intended configuration is `arms=28,26`: `ARMS_BY_FILE = {"count-c1.py": 28, "count-c2.py": 26}`
  (`count-c2.py:39`) and the P-C2 target string `… arms=28,26` (`count-c2.py`, `TARGET`).

### 3.2 Why the pristine is red — the control patch's own doing (scratch replication)

`controls-r89.sh:50-62` patches the r88 count-c1 subject by (i) inserting three always-true labels
**before** the `ok = sum(...)` anchor, i.e. **after** the subject's own `own_arms_pinned` case, and
(ii) setting `EXPECTED_ARMS = 28` and `ARMS_BY_FILE = {"count-c1.py": 28}` — while leaving the two
arms that *pin* those constants untouched:
- `own_arms_pinned` (`.ufo/waves/round-88/count-c1.py:320-321`) evaluates
  `len(cases) + 1 == EXPECTED_ARMS`; at its evaluation point `len(cases)` is still 24, so it computes
  `25 == 28` → **FAIL**;
- `per_file_arms_frozen` (`:270-271`) asserts the literal `ARMS_BY_FILE == {"count-c1.py": 24}` and
  `sum(...) == TARGET_ARMS` (24) → the patched constant is 28 → **FAIL**.

My scratch replication of that patch (command #6) reproduces exactly:
`FAIL per_file_arms_frozen 24`, `FAIL own_arms_pinned 25/28`, `C1_COUNTER_SELFTEST pass=26 fail=2`,
rc=1. **Independently, sibling seat `Mo89R02C2` measured the same two FAIL lines in its own 2b
replay** (its §4) — two independent routes to the same fixture defect.

### 3.3 Consequence: the two `unattributed` count-c1 lines are not attribution evidence

Applying the two declared C1 mutation anchors to the §2b-patched subject (scratch command #7) gives
mutant copies that are red with the **same two** FAIL lines and **no** `FAIL arms_last_tally` /
`FAIL green_mixed_fail`. So the counter's `unattributed` verdict is correct as computed, but the
redness is **inherited from the patched pristine**, not caused by the mutation and not caught by the
declared arm. In a *sound* §2b variant (labels inserted before `own_arms_pinned`, pins kept
consistent — scratch command #8) the patched pristine is **green at 28/0** and both C1 mutants are
**green** (rc=0, no FAIL line). A sound skip-work control therefore reads
`killed=0 survivors=7 unattributed=0 unanchored=5 arms=28,26`, not `survivors=5 unattributed=2
arms=26,26`.

**Therefore:**
1. The count-c2 leg of 2b **is** sound evidence: its patched subject is green at 26/0
   (`pass=26 fail=0`, measured), its five anchored mutants survive green, and the five refactored
   anchors stay unanchored. *"Labels without assertions produce no kill"* is genuinely shown.
2. The count-c1 leg of 2b **is not** evidence that "the attribution rule [is] doing its job on the
   forger". Its pristine is red for the control's own reasons, its two mutants are red for the same
   pre-existing reason, and the `unattributed=2` line would be produced by **any** mutation of that
   subject — including a no-op-shaped one — because red-without-a-declared-FAIL is `unattributed` by
   construction (`count-c2.py:120-126`).
3. The recorded `arms=26,26` must not be read as the intended `28,26`; the count-c1 slot is a pass
   count over a broken subject, and the two numbers coincide misleadingly (26 = the count-c2 leg's
   genuine 26-arm green subject).

**Draft lesson row for this (L1 lands):**

| Class | Evidence pointer | Captured-by | Fix delivered and what makes it able to fail |
|---|---|---|---|
| `control-fixture-red-before-mutation` — the skip-work control's own patch broke two of the subject's self-pin arms, so the "pristine" was red at 26/28 before any mutant was graded; the two `unattributed` count-c1 lines are inherited redness, not the attribution rule discriminating, and the tail's `arms=26,26` is a pass count, not the intended 28/26 configuration. | `.ufo/waves/round-89/evidence/controls-r89.txt:51` (`pristine-red … rc=1 arms=26`) and `:44-45` (the two `unattributed` count-c1 lines); the patch at `.ufo/waves/round-89/controls-r89.sh:50-62`; the subject's pins at `.ufo/waves/round-88/count-c1.py:270-271` and `:320-321`; the counter's pass-count arm list at `.ufo/waves/round-89/count-c2.py:170-176` | round-89 wave, `Mo89R02C2` §4 (independent replay of the same two FAIL lines) and `Mo89S02Record` §3 (static re-derivation + scratch replication) | Rebuild 2b so the patched count-c1 subject is **green at 28 arms** (labels inserted before `own_arms_pinned`; `EXPECTED_ARMS`/`ARMS_BY_FILE`/`per_file_arms_frozen` consistent) and re-record; until then cite 2b only for its count-c2 leg. It is able to fail: with the pristine green, a mutation that the declared arm should catch reads `survived rc=0`, so a green pristine and `unattributed=2` cannot coexist by accident |

**Recommendation to L1 (calibration):** when the r89 lesson states the skip-work result, write it as
*"twelve labels without assertions produce no kill (count-c2 leg: 5 anchored mutants survive a green
26-arm subject; the five refactored anchors stay unanchored)"*, and record the count-c1 leg as
**confounded** (pristine red, `arms` field = pass count) rather than as the attribution rule
rejecting a forger. Do not restate `arms=26,26` as if it were the intended 28/26 configuration.

---

## 4. F3 — the r89 C1 counter's `FX` label flips meaning between runs

`evidence/controls-r89.txt:5-7` (entering): `FX equiv refused problems=cmd-binding`,
`FX comment refused problems=-`, `FX selfprint refused problems=-`.
`w1/Mo89E03Replay-receipts.txt:40-42` (landing): `FX equiv accepted problems=-`,
`FX comment accepted problems=cmd-binding`, `FX selfprint accepted problems=cmd-binding`.

Same fixture, opposite words, opposite meanings: in the counter, `good` means *the expectation was
met*, and the expectation for `comment`/`selfprint` is **refusal** — so `FX comment accepted
problems=cmd-binding` means "the fixture was correctly refused", while the entering run's
`FX comment refused problems=-` means "the fixture was not refused as expected"
(`count-c1.py:289-290`: `print("FX %s %s %s" % (kind, "accepted" if good else "refused", detail))`;
`state[kind] = want if good else …`). The r88 round routed exactly this class ("rename the r88 C2
counter's `FX … refused` wording so a clean fixture reads `ok`", `SCORECARD.md:4551` (Planned round-89
item 2) and `corpus/lessons/round-88.md:140`); the new counter reintroduces it with the opposite polarity.

**Impact:** none on the frozen predicate — `count-c1.py:34` `TARGET = "equiv=accepted
comment=refused selfprint=refused real=met arms=26"` and the printed summary line use the
`state[...]` words, which are unambiguous. The defect is in the per-fixture `FX` line only.

**Draft lesson row (L1 lands):**

| Class | Evidence pointer | Captured-by | Fix delivered and what makes it able to fail |
|---|---|---|---|
| `fixture-label-polarity-flips` — the same fixture is printed `accepted` in one run and `refused` in another, with the word tracking *expectation-met* rather than *fixture-behaviour*, so a reader can invert the meaning. | `.ufo/waves/round-89/count-c1.py:289-290`; `.ufo/waves/round-89/evidence/controls-r89.txt:5-7` vs `.ufo/waves/round-89/w1/Mo89E03Replay-receipts.txt:40-42` | round-89 wave, `Mo89S02Record` §4 (byte-level reading of both receipts) | Print the fixture's **actual behaviour** beside the expectation (e.g. `FX comment refused-by-gate expected=refused problems=cmd-binding`), or reuse the r88 counter's convention consistently across counters. It is able to fail: the two runs of the *same* fixture must not print the same word for opposite gate behaviours |

---

## 5. F5 — mining the two prior regressions (before failure → criterion → fix pointers)

### 5.1 D2 — genuine `./path` replay falsely refused (operability harm, r88)

- **Before failure.** The r87 gate's binding rule compared **token spelling**:
  `.ufo/waves/round-87/count-c2.py:140-145` at `d5e2eda4` —
  `tokens = set(token.strip(";'\"") for token in re.split(r"\s+", cmd or ""))`;
  `return ["cmd-binding"] if any(path not in tokens …)`. A genuine equivalent invocation
  `./tools/mori-record-sweep.py` (same file, replay rc=0, body matched) was refused:
  `RECEIPT record-sweep-r87.txt expect=met failed problems=cmd-binding` → `C2=unmet` rc 1 —
  measured by `w1/Mo88C01Critic.md:106-112` (ATTACK C2-no-harm, result=succeeded). Routed as
  **R89-C2-path-identity** (`corpus/lessons/round-88.md:188`); closure verdict "operability harmed"
  (`corpus/lessons/round-88-verifier-spotcheck.md:70`).
- **Criterion pointer.** QUALITY **185** (`corpus/QUALITY.md:2146-2156`): "no-harm is checked
  against semantically equivalent valid inputs as well as the original population" and "a later rule
  must defeat the canary and accept the equivalent spelling before claiming those classes closed";
  QUALITY 184's "Not covered" notes the token check's limits.
- **Fix pointer.** Round-89 C1 landing `760428abf925d98025b34bf23f2cbf54cbeb3bca`:
  `.ufo/waves/round-87/count-c2.py:149-199` — `command_invocations` (`:149`, `shlex.split(...,
  comments=True)`, `;`-separated), `same_path` (`:162`, `normpath`/`realpath`), `script_position`
  (`:172`, interpreter + index 1, or index 2 after a flag) and the rewritten `binding_problems`
  (`:181-199`, now repo-aware); three new arms at `:470-478`; r88 caller pin migrated
  (`SUBJECT_ARMS 23 → 26`, `TARGET arms 23 → 26`); registry row 23 (`SKILL.md:1375`).
  **Equivalence-positive control**: `.ufo/waves/round-89/count-c1.py:42-46` fixture
  `("equiv", "python3 -I ./tools/mori-record-sweep.py --root . --pins …", "accepted")` — the control
  the r88 round asked for; the frozen predicate `count-c1.py:34`.
- **Status.** C1 after-value is **measured met** at `760428ab` — `C1=met equiv=accepted
  comment=refused selfprint=refused real=met arms=26 rev=760428abf925` (rc 0) in
  `w1/Mo89E03Replay-receipts.txt:43` and `w1/Mo89R01C1-evidence/counter-c1-after.out:5`; the
  entering reading is `C1=unmet equiv=refused comment=accepted selfprint=accepted real=met arms=26`
  (`evidence/controls-r89.txt:5-7,40`). **Honest limit:** those receipts live in the wave's
  *untracked* `w1/` tree; the committed evidence directory holds only `controls-r89.txt` — there is
  **no committed `.ufo/waves/round-89/evidence/after-r89.txt`**. L1 must land one before the
  lesson cites it.

### 5.2 D3 — a kill credited from an unrelated nonzero exit (calibration harm, r88)

- **Before failure.** The r88 C1 counter's kill rule was
  `.ufo/waves/round-88/count-c1.py:97-98` (bytes at `d5e2eda4`):
  `def killed(rc, out): return rc != 0 or bool(FAIL.search(out))` — **any** nonzero exit (crash,
  timeout, checksum canary) or any FAIL text counted as a kill, with no declared-arm attribution.
  Measured: an arms-free checksum-canary subject (fixture `79143f945e424b79892e730c431d5659ca0d07a7`)
  makes the frozen counter print the exact target line `C1=met mutants=6 killed=6 survivors=0
  total=6 arms=24 rev=79143f945e42` rc 0 — `w1/Mo88C01Critic.md:23-50` (ATTACK C1-vacuity,
  result=succeeded); routed **R89-C1-subject-identity** (`corpus/lessons/round-88.md:181-184`).
- **Criterion pointer.** QUALITY **185** (its "Ground" cites exactly this counterexample) and
  QUALITY 174 (`:1970-1998`, "red on the unarmed subject is fixture defect, never discrimination")
  and 177 (`:2037-2050`, label-only stub must read `unmet`).
- **Fix pointer.** Round-89 C2 counter, frozen at `d4438695998894aad7ff9b20f46d9f1852ea3c7d`:
  `.ufo/waves/round-89/count-c2.py:115-126` — `arm_failed` matches `^FAIL <arm>(\s|$)` and
  `killed = red(rc,out) and arm_failed(out, arm)`; `unattributed` is the red-without-declared-FAIL
  case; the counter's own negative control arm `canary_unattributed` (`:252`) reads a synthetic
  checksum canary as **unattributed, never killed** — recorded green in
  `.ufo/waves/round-89/evidence/controls-r89.txt:68` (`PASS canary_unattributed mutants=1 killed=0
  survivors=0 unattributed=1 unanchored=0 arms=1`), with the detectors' own selftests
  `pass=17 fail=0` / `pass=15 fail=0` (`:70-71`).
- **Status — the honest part.** The *instrument* is frozen and its own arms are measured green, but
  **there is no C2 landing and no C2 after-value**: HEAD is still the C1 landing `760428ab`, the
  twelve-arm subjects exist only as wave drafts (`w1/candidates/r88-count-c1.py`,
  `w1/candidates/r88-count-c2.py`; selftests green at 28/0 and 26/0 in my scratch), and the
  twelve-mutant kill/attribution claim has **not** been measured end-to-end. The lesson must say
  "specified, not yet demonstrated", and the QUALITY row must not cite an after-value that does
  not exist.

---

## 6. Draft QUALITY additions (L1 lands; numbers provisional, L1 assigns final)

Numbers follow QUALITY 185 (`corpus/QUALITY.md:2146`). Text follows the house shape
(Ground / Shown able to fail / Not covered).

> **186.** A refusal rule that matches the **spelling** of a path rather than the **file** it names
>      refuses a semantically equivalent genuine invocation; the rule is re-derived by identity
>      (normalised and real path) and by the bound path's position as the executed script, and the
>      no-harm check carries an **acceptance** fixture for the equivalent spelling, not only a
>      refusal fixture for the counterfeit.
>      Ground: QUALITY 185 (no-harm against semantically equivalent valid inputs) and its
>      "Not covered" note that 184 is a necessary token check only; the r88 rule
>      (`.ufo/waves/round-87/count-c2.py:140-145` at `d5e2eda4`) compared a whitespace-token set, so
>      the genuine equivalent `./tools/mori-record-sweep.py` was refused `cmd-binding` although its
>      replay exited 0 and its body matched (`w1/Mo88C01Critic.md:106-112`; closure verdict
>      "operability harmed", `corpus/lessons/round-88-verifier-spotcheck.md:70`).
>      Shown able to fail: the round-89 C1 landing replaces the rule
>      (`.ufo/waves/round-87/count-c2.py:149-199` at `760428ab`: `command_invocations`, `same_path`,
>      `script_position`, repo-aware `binding_problems`; arms `:470-478`) and adds the
>      equivalence-**acceptance** fixture (`.ufo/waves/round-89/count-c1.py:42-46`); the entering
>      revision reads `equiv=refused` (`evidence/controls-r89.txt:5`) and the landing reads
>      `C1=met equiv=accepted comment=refused selfprint=refused real=met arms=26`
>      (`w1/Mo89E03Replay-receipts.txt:43`). A rule that accepts only the exact spelling fails this
>      criterion on the equivalence fixture alone.
>      Not covered: a script that dispatches to another file at run time; a symlink whose real path
>      differs from the repo-relative name; the rule still establishes naming-and-position, not
>      execution provenance; the equivalence fixture is one spelling family, not a census.

> **187.** A mutation is credited as **killed** only when the mutated copy's own selftest prints a
>      FAIL line naming that mutant's declared arm; a nonzero exit, a timeout, a crash, or a
>      checksum canary establishes no kill, and a red pristine establishes nothing about the
>      mutation.
>      Ground: QUALITY 174 (red on the unarmed subject is fixture defect, never discrimination) and
>      185 (the arms-free checksum canary that reached the r88 target line,
>      `w1/Mo88C01Critic.md:23-50`, fixture `79143f94`); the r88 kill rule
>      (`.ufo/waves/round-88/count-c1.py:97-98`: `rc != 0 or bool(FAIL.search(out))`) credited any
>      nonzero exit.
>      Shown able to fail: the round-89 C2 counter requires the declared-arm FAIL line
>      (`.ufo/waves/round-89/count-c2.py:115-126`) and its own `canary_unattributed` arm (`:252`)
>      reads a synthetic checksum canary as `unattributed`, never `killed`
>      (`evidence/controls-r89.txt:68`, `PASS canary_unattributed mutants=1 killed=0 survivors=0
>      unattributed=1 unanchored=0 arms=1`); a red pristine makes every mutant red, so the
>      criterion's "red pristine" clause is what stops a broken fixture from being read as
>      attribution.
>      Not covered: the C2 population is **not yet measured end-to-end** (no C2 landing at
>      `760428ab`; the twelve-arm subjects exist only as wave drafts under `w1/candidates/`), so this
>      row rests on the detector's own selftest arms and the canary, not on a landed twelve-mutant
>      run; a FAIL line whose arm name is a prefix of another arm's name; a subject that fails for
>      reasons unrelated to the mutation while still printing the declared arm's label.

> **188.** A control fixture's own edit must leave the subject **green at the intended arm count**
>      before the control's reading is used: a control whose patched subject is red, or at a
>      different arm count than the claim's target, measures the control's own breakage, and its
>      recorded tally is a pass count of a broken subject rather than the configuration it stands for.
>      Ground: the round-89 skip-work control 2b patched the r88 count-c1 subject by appending three
>      always-true labels after its `own_arms_pinned` arm while bumping `EXPECTED_ARMS` and
>      `ARMS_BY_FILE` (`.ufo/waves/round-89/controls-r89.sh:50-62`), leaving the pins at
>      `.ufo/waves/round-88/count-c1.py:270-271` and `:320-321` broken; the receipt then reads
>      `EXTRA pristine-red … rc=1 arms=26` (`.ufo/waves/round-89/evidence/controls-r89.txt:51`) and
>      the two `unattributed` count-c1 mutant lines (`:44-45`) are inherited redness, while the
>      counter's arm list records **pass counts** (`.ufo/waves/round-89/count-c2.py:170-176`) and the
>      claim's intended configuration is `arms=28,26` (`:39`).
>      Shown able to fail: with the same patch applied to a green-consistent subject (labels before
>      the pin arm; the pinned constants updated together) the pristine reads green at 28 arms and
>      the two declared C1 mutants read green with no FAIL line — so a red pristine and an
>      `unattributed` line cannot coexist in a sound fixture by accident.
>      Not covered: controls whose subject is intentionally red; arm-count floors for subjects
>      without a self-pin; the counter's own `pristine-arms` check fires only when the pristine is
>      green, so a red pristine hides an arm-count mismatch behind `pristine-red`.

---

## 7. Draft lesson section for `corpus/lessons/round-89.md` (L1 lands; file does not yet exist)

`corpus/lessons/round-89.md` — **not present** at this writing (`ls corpus/lessons | grep round-89`
→ 0). The below is the shape L1 should land, with every factual slot either filled from the
measurements above or marked **MISSING**.

```markdown
## Mistakes

| Class | Evidence pointer | Captured-by | Fix delivered and what makes it able to fail |
|---|---|---|---|
| `newness-counted-by-helper-not-by-refusal` — round 88's corpus claimed three new gate
conditions; the entering gate already refused the absent supersede target, so r88 added two new
refusals and one extracted helper. | `corpus/knowledge/receipt-counterfeit-r88.md:11-14`;
`corpus/README.md:919`; entering bytes `1bd5ec3fa260458f74eb32a2e5bb157209c5934d`
`.ufo/waves/round-87/count-c2.py:297-302`; r88 entering control
`.ufo/waves/round-88/evidence/controls-r88.txt:65`; closure finding
`corpus/lessons/round-88-verifier-spotcheck.md:60` | round-88 closure (routed item 1);
round-89 `Mo89S02Record` §2 (byte-level re-derivation) | named append-only errata in the
knowledge entry, the README and the round-88 lesson (M1/M2/M3), old bytes preserved; every
mention swept. It is able to fail: a claim of *N* new conditions is refuted by the entering
bytes refusing the Nth condition |
| `control-fixture-red-before-mutation` — the round-89 skip-work control 2b broke two of the
subject's own self-pin arms; its pristine was red at 26/28 before any mutant was graded, so its
two `unattributed` count-c1 lines and its `arms=26,26` are the control's own breakage, not the
attribution rule working. | `.ufo/waves/round-89/evidence/controls-r89.txt:44-45,51`;
`.ufo/waves/round-89/controls-r89.sh:50-62`; pins at `.ufo/waves/round-88/count-c1.py:270-271`,
`:320-321`; counter pass-count arm list `.ufo/waves/round-89/count-c2.py:170-176` | round-89
`Mo89R02C2` §4 and `Mo89S02Record` §3 (independent routes) | rebuild 2b green at 28 arms and
re-record; until then cite only its count-c2 leg. It is able to fail: a green pristine turns a
would-be `unattributed` mutant into `survived rc=0` |
| `fixture-label-polarity-flips` — the same fixture prints `accepted` in one run and `refused` in
another, because the word tracks expectation-met rather than fixture behaviour. |
`.ufo/waves/round-89/count-c1.py:289-290`; `evidence/controls-r89.txt:5-7` vs
`w1/Mo89E03Replay-receipts.txt:40-42` | round-89 `Mo89S02Record` §4 | print the fixture's actual
behaviour beside the expectation, consistently across counters. It is able to fail: the same
fixture's two runs print the same word for opposite gate behaviours |
```

**Gate section — draft with the gaps marked (L1 fills the MISSING slots).**

```markdown
## Gate

Sources opened this round: the round-89 sources seat proposes S607–S610 (Python `shlex`,
`os.path`, command-line docs) with one scope-rejection row and a new knowledge entry
`corpus/knowledge/cmd-binding-r89.md` (`w1/Mo89S01Sources.md` §2). **MISSING at this writing:**
the S-row ids/decisions as landed in `corpus/SOURCES.md` (the registry still ends at S606, 379
rows), the landed knowledge entry, and the round-89 after-receipt path/revision.

Registry census: **MISSING** — L1 to run
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin mori`
and `… validate --root … mori` before and after landing, and quote both rc and row counts.

After-evidence: **MISSING** — `.ufo/waves/round-89/evidence/` currently holds only
`controls-r89.txt`; there is no `after-r89.txt`, and the C1 after reading
(`C1=met equiv=accepted comment=refused selfprint=refused real=met arms=26 rev=760428abf925`)
exists only in wave seat artifacts under the untracked `w1/` tree.
```

---

## 8. Scope boundaries and out-of-scope items

**Out of scope for this seat (named, not silently dropped):**
- **No corpus byte written** — the errata blocks, the lesson, the QUALITY rows and the knowledge
  entry in §2.3/§6/§7 are drafts for L1 to land.
- **No C2 measurement** — the twelve-mutant kill/attribution claim has no after-value (no C2
  landing, no after-receipt). Nothing in this report asserts a C2 verdict.
- **No instrument change** — I did not touch the frozen counters, the contract, the controls
  script, the C1 landing, the r88 subjects, or the candidates. The skip-work defect in §3 is
  reported **for L1 to rebuild the control**, not repaired here: the contract froze the control's
  expected string and the controls script is a committed instrument of the freeze.
- **No source opened** — I opened no URL this round, so I propose no S-row and cite no registry
  row beyond what `Mo89S01Sources.md` already proposes.
- **Not mine to decide:** whether the r88 wave reports (M5/M6) get an appended note; whether the
  r89 knowledge entry lands as `cmd-binding-r89.md` or `execution-binding-r89.md` (F4).

**Bounds honoured:** production checkout, fleet root, sibling repos, operator settings and the
git/jj index were read-only; no seat in this wave committed or pushed from my seat; no task
dispatch, no subagents, no background jobs; scratch confined to
`/fast/scratch/hyaku/mori-r89/Mo89S02Record/`, TMPDIR/`--scratch` set explicitly, **scratch deleted**
before yield; only my uniquely named report written under `.ufo/waves/round-89/w1/`.

---

## 9. Handoff to L1 (MoriR89), in priority order

1. **F4 (blocking):** fix the dangling `execution-binding-r89.md` pointer in the pending knowledge
   errata — land `corpus/knowledge/cmd-binding-r89.md` (the sources seat's proposed name) and
   repoint, or drop the sentence. Do not land the errata with a pointer that does not resolve.
2. **F2 (calibration):** rebuild skip-work control 2b so the patched count-c1 subject is green at
   28 arms, re-record, and re-state the control's claim in the lesson as *"labels without
   assertions produce no kill"* citing the count-c2 leg; do not present the count-c1 leg's
   `unattributed=2` as the attribution rule catching a forger.
3. **F1:** land the three named append-only errata (M1 knowledge, M2 README, M3 r88 lesson) with
   the wording in §2.3, preserving the original bytes; the sweep (M1–M11) is complete, so nothing
   stays silently wrong.
4. **Evidence:** commit an after-receipt for round 89 (`.ufo/waves/round-89/evidence/after-r89.txt`)
   before the lesson cites the C1 after-value; the only committed round-89 evidence today is
   `controls-r89.txt`.
5. **F3:** adopt the FX-label wording fix in the r89 C1 counter or record the defect in the lesson;
   the predicate line is unaffected either way.
6. **QUALITY:** land rows 186–188 (§6) with final numbering; 187 must say "specified, not yet
   measured end-to-end" until a C2 landing exists.
