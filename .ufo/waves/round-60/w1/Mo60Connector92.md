# Mo60Connector92 — cross-round defect classes, rounds 57–59 → round-60 lesson

seat: connector · round 60 · wave w1
date: 2026-10-28
pinned revision for every read below: `b3c256138f00c704d5aa56eb0332d74506502ef2`
(lane `master`, `git status --porcelain` empty for tracked files; only untracked
round-60 wave files present). Entering `ddfb12fb…`, freeze `ac496c7c…` read from
the contract, not re-scored by me.
Work performed read-only: `grep`, `sed`, `git show`, `git cat-file`, `sha256sum`.
No VCS mutation, no fixture, no write outside this file and an empty scratch dir
(`/fast/scratch/hyaku/mori-r60/Mo60Connector92`, removed at yield).

## 1. Routed-defect inventory (what each spot-check actually routed)

Thirteen numbered items across the three spot-checks (counted by
`grep -n '^[0-9]\. \*\*' corpus/lessons/round-5[789]-verifier-spotcheck.md`):

| # | Pointer | Item (abbreviated) | Class (fleet vocabulary) |
|---|---|---|---|
| r57 D1 | `round-57-verifier-spotcheck.md:72` | counter binds the FIRST `## Capabilities` heading, not the active register; "carried from r57" | reference-drift (superseded target) |
| r57 D2 | `:73` | `count-c1` never resolves an evidence pointer; `count-c2` accepts any backticked text — false-green constructions reproduced | vacuous |
| r57 D3 | `:74` | observation: S549 quote normalizes a line-break hyphenation | reference-drift (precision, not a defect) |
| r58 D1 | `round-58-verifier-spotcheck.md:84` | report's SHONEN lines cite `kotodama-shokunin/SHONEN.md` — a sibling lane's checklist | reference-drift (cross-lane binding) |
| r58 D2 | `:85` | S552 re-admits S478's paper/sha; sibling-row sweep never run | taste / registry duplicate |
| r58 D3 | `:86` | required target token `selftest=ok` is never emitted by the counter — "carried from this round's own criterion 154" | vacuous |
| r58 D4 | `:87` | C2 control (c): frontmatter-less body scores `met` | vacuous |
| r58 D5 | `:88` | observation: planner-seat mapping drift; wave-marker commit after cited tip | landing (observation) |
| r59 D1 | `round-59-verifier-spotcheck.md:93` | `c1-entering.txt` / `c2-entering.txt` / `controls.txt` cited, never committed under those names | reference-drift |
| r59 D2 | `:96` | late seat files + `w1-results.json` uncommitted at tip | landing |
| r59 D3 | `:99` | report's missing-set (3) vs lesson's absent-at-filing set (5) — 2 were committed | number-drift |
| r59 D4 | `:102` | no committed receipt for `C1=met`/`C2=met` at data rev `7b86704d` | provenance / receipt |
| r59 D5 | `:104-109` | seven carried sub-items: `tool_ok` gate, containment, attacker `expect.txt`, self-graded semantic arms, selftest-consistency, expect-prefix, `grammar:` orphaning / distinct span / row↔copy / drift attribution | vacuous (bundle) |

Class labels are the fleet's own vocabulary, not mine:
`vacuous · survivor · stale-premise · reference-drift · number-drift · scope ·
attribution · landing · provider` (`/home/vgpnk/Projects/shokunin/CORPUS.md:175-179`,
defining section `.ufo/waves/kaika-w1/mistakes.md:156-176` for C04 and
`:447-449` for the vocabulary list).

Routed volume is not shrinking: r57 routed 2 defects (+1 observation), r58 4 (+1),
r59 4 (+1 bundle of 7 carried items).

## 2. Recurrence matrix

| Class | r57 | r58 | r59 | rounds |
|---|---|---|---|---|
| **vacuous** (instrument false-green) | D2 | D3, D4 | D5 | **3/3** |
| **reference-drift** (wrong/dead pointer) | D1, D3(obs) | D1 | D1 | **3/3** |
| landing | — | D5(obs) | D2 | 2/3 |
| number-drift | — | — | D3 | 1/3 |
| provenance (receipts) | — | (C1 token) | D4 | 1/3 |
| taste / registry duplicate | — | D2 | — | 1/3 |
| scope / attribution / survivor / stale-premise | — | — | — | 0/3 |

Only two classes reach 3/3, and they are the two the seat named. The r60 lesson
carries a row for reference-drift (`corpus/lessons/round-60.md:65`) and for landing
(`:75`) — and no row for **vacuous**, which is the class all three round-60 claims
are written against.

## 3. The recurring classes, one line each

- **vacuous / instrument false-green** — every round froze a *new* counter, the
  routed false-green was repaired on that instance, and the class returned on the
  next instrument (r57 D2 → r58 D3/D4 → r59 D5); it is the class C2/C3 exist to close.
- **reference-drift** — a pointer or control names something that is not the object
  the claim intends (superseded stub `SCORECARD.md:596` vs the self-declaring
  register at `:1951`; a sibling lane's SHONEN; two receipt names never committed);
  `git cat-file -e` proves existence, never identity, so the class survives the
  existence sweep.

Lineage of the class rows, for continuity: `corpus/lessons/round-58.md:9` class
`Frozen-counter identity and false-green resistance` → `corpus/lessons/round-59.md:14`
class `instrument` → `corpus/lessons/round-60.md`: absent
(`grep -c 'class vacuous\|class instrument\|false-green\|false green'` → **0** at
`b3c25613`). Round 59's label `instrument` is also off-vocabulary; `vacuous` is the
registered label for this class.

## 4. Draft rows for `corpus/lessons/round-60.md` `## Mistakes` (append as row 3)

Style matches rows 1–2 (`N. class <label> · evidence: … · captured-by: … · fix: …`).

> 3. class vacuous · evidence: the false-green predicate is the one defect class
>    routed in all three prior spot-checks — r57 `:73` (`count-c1` never resolved an
>    evidence pointer; `count-c2` never read the source copy), r58 `:86-87` (the
>    frozen C1 target token was never emitted by the counter; C2 control (c) scored a
>    frontmatter-less body `met`), r59 `:104-109` (seven carried sub-items:
>    `grammar:` orphaned, no distinct-span bound, no row↔copy binding, exit-code-only
>    drift arm) — and it is the class this round's C1/C2/C3 are written against, yet
>    `grep -c 'vacuous\|instrument\|false-green' corpus/lessons/round-60.md` at
>    `b3c25613` prints 0 · captured-by: none before this round — each round froze a
>    new counter, so the previous round's hostile fixtures died with it, and no rule
>    required one hostile case per declared failure token (fleet precedent C04, five
>    recurrences after its rule: `.ufo/waves/kaika-w1/mistakes.md:156-176`) · fix:
>    QUALITY 157 with this round's hostile trees (`count-c2.py` H1-H5 over the 13
>    `trees-c2h/` trees, `count-c3.py` G1-G3); the durable bar is "one hostile case
>    per declared failure token, frozen beside the counter"; residual: self-graded
>    semantic arms stay judge work (QUALITY 157 "Not covered").

And one clause appended to the existing row 1 (its remainder is correct and stands):

>    Residual (same class, uncovered half): QUALITY 156's sweep is `git cat-file -e`
>    per hit, which proves a pointer resolves, not that it names the object the claim
>    intends — r57 `:72` (counter bound the superseded `— none yet —` stub at
>    `SCORECARD.md:596` instead of the self-declaring register at `:1951`) and r58
>    `:84` (SHONEN bound to `kotodama-shokunin/SHONEN.md`) both resolve while naming
>    the wrong artifact, and the C1 DEAD-NAME ARM counts two literal names only
>    (`.ufo/waves/round-60/count-c1.py:41`). Open until the sweep carries an identity
>    cell.

Nothing proposed for `landing`, `number-drift`, `provenance`, `taste`, `scope`:
they are sub-threshold (≤2/3) and rows 1–2 plus QUALITY 155/156 already own them.
Adding them would over-claim recurrence.

## 5. Governance reading the lesson does not state (sentinel)

The fleet carries a drift sentinel: "Same axis and surface 3 rounds running →
the lane's next round must work a different frontier area"
(`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/PHASE3.md:403`; rule text and
precedent in `.ufo/waves/round-25/w1/CriticSizing.md:107-124`, which records the
calibration-repair loop as a confirmed trip there).

mori's readings at `b3c25613`, all `| C1: … | calibration 5 |`:

- r57 — "add the two admitted round-56 capabilities to the active current register"
  (`SCORECARD.md:2915`)
- r58 — "frozen active-register counter **binds the two round-56 rows**" (`:2929`)
- r59 — "pinned `tools/mori-register-check.py` **verifies the two round-56 rows**"
  (`:2950`)
- r60 — `C1 — calibration (score 5, tied lowest non-retired)` (contract `:34`)

So: calibration claimed four rounds running, on a surface that was literally the
same two rows for r57–r59. Round 60 changes the surface (the r59 record, not the
register) but not the axis, and all three claims are repairs of the r59 routed list
(C1 ← D1/D3/D4; C2 ← D5 + r58 D4; C3 ← D5) — no frontier area is worked.

Two honest limits on that reading:
1. The rule lives in the driver's sentinel table, not in mori's
   `PROTOCOL.md`/`AXES.md` (`grep -in sentinel PROTOCOL.md AXES.md PROVINCE.md` → no
   hit), so it binds the closure, not the lane's own contract.
2. Under the strict surface reading the trip occurred at the **r59** closure; under
   a loosened reading it occurs at r60. Either way the axis half is satisfied three
   rounds running and no spot-check or contract line mentions the rule
   (`grep -in sentinel` over the three spot-checks + contract returns only seat
   names `Sentinel57/58`).

This is a contradiction to state, not to smooth: the round's declared work and the
drift rule point opposite directions. Recording it in `## Mistakes` (or a one-line
`## Gate` note) is the minimum; whether r61 must move frontier is the L1/driver call,
not mine.

## 6. Verification (commands + observed output at `b3c25613`)

```
$ grep -n '^[0-9]\. \*\*' corpus/lessons/round-5[789]-verifier-spotcheck.md
  57:72, 57:73, 57:74
  58:84, 58:85, 58:86, 58:87, 58:88
  59:93, 59:96, 59:99, 59:102, 59:104          # 13 items, as tabulated above
$ grep -c 'class vacuous\|class instrument\|false-green\|false green' corpus/lessons/round-60.md
  0        # exit 1 (no match); the zero is the finding, the status is grep's
$ grep -n 'class reference-drift\|class landing' corpus/lessons/round-60.md
  65:1. class reference-drift · evidence: r59 report + `SCORECARD.md` (r59
  75:2. class landing · evidence: `f091bd77` committed `w1-results.json` and the
$ grep -n '^| C1' SCORECARD.md | tail -4
  2905: … FR5 driver-liveness probe …            (not calibration; context row)
  2915: … add the two admitted round-56 capabilities … | calibration 5 |
  2929: … binds the two round-56 rows …             | calibration 5 |
  2950: … verifies the two round-56 rows …          | calibration 5 |
$ sed -n '9p' corpus/lessons/round-58.md   → class cell: Frozen-counter identity and false-green resistance
$ sed -n '14p' corpus/lessons/round-59.md  → class cell: instrument
$ sed -n '596p;1951p' SCORECARD.md
  596: ## Capabilities                                    (superseded stub)
  1951: Round 35 (claim C1, calibration). This is the lane's current capabilities register, …
$ sha256sum corpus/lessons/round-60.md  → ca3f1e10cbb8d4b9673097a568eab762ea5e863255b434ae0a3e0777a2264b78
  (equals `git show HEAD:corpus/lessons/round-60.md` — worktree not ahead of HEAD)
$ git diff --stat ac496c7c HEAD -- .ufo/waves/round-60/{count-c1.py,count-c2.py,count-c3.py,contract.md}
  (empty — frozen bytes unchanged since freeze)
```

## 7. Risks and limits

- **Drafts are unverified by construction.** A non-author closure must sample the two
  rows: the vacuous row's evidence set is reproducible by the §6 grep pair; the row-1
  residual is reproduced by pointing QUALITY 156 at a *live* superseded pointer
  (`SCORECARD.md:596`), which 156's `cat-file -e` sweep cannot fail — the red-before
  I could not produce read-only, and the row says so.
- **The sentinel reading rests on axis labels, not on a lane rule.** If the L1 rules
  that r60's C1 surface (r59 record) is a different surface *and* that the rule counts
  only same-surface runs, the trip becomes a 2-round observation. Both readings are
  stated above; neither is scored here.
- **Class counts are item counts, not severity.** r59's D5 carries seven sub-items;
  counting it as one routed item understates the bundle. I kept item counts to stay
  honest about the text.
- I did not re-derive the counters' verdicts (other seats own that); everything here
  is over committed bytes at `b3c25613`.
- `corpus/lessons/round-60.md` is being edited concurrently during the wave (another
  seat added the absent-set reading note after my read: `git diff` — 13 insertions,
  no `## Mistakes` change). Row numbers and line pointers above remain those of
  `b3c25613`; the `grep … → 0` and `class reference-drift` → `:65` results still hold
  on the current worktree bytes.
