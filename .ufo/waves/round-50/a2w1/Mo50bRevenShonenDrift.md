# Mo50bRevenShonenDrift — how SHONEN.md's tally pins went stale (M1 evidence)

Seat: Mo50bRevenShonenDrift (revenger, leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Frozen contract read first: `.ufo/waves/round-50/contract.md` @ `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`.
Landed data revision examined: `487941b9395e89678af0053cc443cdb49cdee6e3` (C1/C2 data, attempt 2).

**Scope of this seat:** reconstruct how the two SHONEN tally pins `(60/60)` and `(13/13)` became stale, which
commits changed the instruments' selftest counts, which round owed the SHONEN edit, and when each of the four
stale Axes `Last change` cells stopped being updated. Detection and reconstruction only: no file outside this
report was written. The counters, predicates, controls and kill rules were not touched or proposed against.

**Provenance note.** The lane worktree HEAD is `4548a34dc8b4072abaa4335c1f54a9efcfcc314a`, not the landed
`487941b9`. Every byte quoted below was read with `git show <rev>:<path>` or from a `git archive` of `<rev>`
under `/fast/scratch/hyaku/mori-r50/Mo50bRevenShonenDrift/`; the five lines I also cite from the worktree
(`SKILL.md:1004`, `LOG.md:2727`, `corpus/lessons/round-29.md:26`, `corpus/QUALITY.md:1028`, `SHONEN.md:7`)
were diffed against `487941b9` and are identical (`SAME` for all five). Scratch removed at seat end; every
citation below is a repo path, never a scratch path.

---

## 1. The commit that set `(60/60)` and `(13/13)`

`git log --format='%H %ad %s' --date=short -- SHONEN.md` returns six commits for the whole lane history:

```
487941b9395e89678af0053cc443cdb49cdee6e3 2026-10-26 round-50: data (attempt 2, L1 MoriR50a2) — …
91fbbc2a6a3591e3539c10a378c4f68f65c81aa4 2026-10-25 round-48: wave 2 settled — results, entry overclaim reworded, …
2f04605ab1d113ecf27e77adc0202a21c9bb6ec7 2026-10-25 round-46: repair r45 calibration records
1f07f1dd1eed59f10c4859726e2f780199190b22 2026-10-19 round-12: source registry (33 rows) + …
27acf40c418b6d790b58202094e241e571ee6f56 2026-10-14 mint: real province, skill, shonen, MINT evidence and corpus bar
ec0664e1ae4d1aa94ed7a960bbc87db11c8b354c 2026-10-14 mint: seed mori-shokunin (fleet & host observability …)
```

`git show 91fbbc2a -- SHONEN.md` (rc 0) is the commit that introduced both pins. The added line:

```
+- [~] Instructions executable by an agent without oral context — `python3 tools/mori-pin-check.py --selftest` (60/60); `python3 tools/mori-unlanded-check.py --selftest` (13/13)
```

replacing the round-46 form `— \`SKILL.md:162-194\`; \`tools/mori-gate-registry.py --selftest\`` (no tally). So
`91fbbc2a` (author `2026-10-25T20:25:44-03:00`, committer `20:25:48`) is the birth of every numeric SHONEN pin.
Before it, SHONEN carried no tally to go stale.

**The pins were accurate at birth.** Re-running both selftests from a `git archive` of `91fbbc2a` prints
`PIN_CHECK_SELFTEST pass=60 fail=0` (rc 0) and `UNLANDED_SELFTEST pass=13 fail=0` (rc 0) — see §2. The staleness
is not a transcription error at write time; it is a later instrument change.

## 2. Every commit that changed the instruments' selftest counts

`git log --format='%H %ad %s' --date=short -- tools/mori-pin-check.py tools/mori-unlanded-check.py` gives five
commits (`63eecf27`, `4dea3d09`, `af2250d8`, `e4dfff32`, `64c2d5fc`); `91fbbc2a` is added as a sixth row because
it wrote the pins. I ran the selftests at each commit from a `git archive`
(the tool only needs `python3` and the archive root; `TMPDIR` inside scratch), rc recorded:

```
S=/fast/scratch/hyaku/mori-r50/Mo50bRevenShonenDrift; export TMPDIR=$S/tmp
D=$S/arch-$c; mkdir -p "$D"; git archive "$c" | tar -x -C "$D"
(cd "$D" && TMPDIR=$TMPDIR python3 tools/$t.py --selftest); echo rc=$?
```

| commit | committer time | pin-check | unlanded-check | what the commit did |
|---|---|---|---|---|
| `63eecf2738db96f46b0bd02b1b2dfd66787493d0` | 2026-10-25T16:32:10-03:00 (author 10:19:06) | `PIN_CHECK_SELFTEST pass=22 fail=0` rc=0 | file absent | round-47 freeze: introduces `mori-pin-check.py` (v1) |
| `4dea3d091820cb3bd73b509b6ec047d017cdb023` | 2026-10-25T16:58:58-03:00 | `pass=30 fail=0` rc=0 | absent | round-47 data, pin-check v2 |
| `af2250d80033ded23ec34af328068eeb85007d1c` | 2026-10-25T17:03:53-03:00 | `pass=34 fail=0` rc=0 | absent | round-47 v2 closes w1 M1/M3/L1 |
| `e4dfff32d4f97c7ef250e9a7538fa75d4f284492` | 2026-10-25T19:30:52-03:00 | `pass=60 fail=0` rc=0 | `UNLANDED_SELFTEST pass=13 fail=0` rc=0 | round-48 data: pin-check v3 + new `mori-unlanded-check.py` |
| `91fbbc2a6a3591e3539c10a378c4f68f65c81aa4` | 2026-10-25T20:25:48-03:00 | `pass=60` | `pass=13` | round-48 wave-2 close: **writes both pins** (values current) |
| `64c2d5fcd95a11f195de0387fa791cab7a54ecb1` | 2026-10-25T22:49:54-03:00 | `pass=114 fail=0` rc=0 | `UNLANDED_SELFTEST pass=17 fail=0` rc=0 | **round-49 data: pin-check v4 (114 cases), unlanded check 17 cases** |

After `64c2d5fc` no commit in the lane changes either tool: `git log --format='%h %s' 64c2d5fc..487941b9 -- tools/`
prints nothing (rc 0). Therefore `114`/`17` were the true values for the entire stale window below.

The stale window is exactly `64c2d5fc..487941b9`:

- **break:** `64c2d5fc` touched 65 files (`git show --name-only --format='' 64c2d5fc | grep -c .` → `65`);
  `… | grep -x 'SHONEN.md'` prints nothing (rc 1) — SHONEN.md was **not** in the round-49 landing commit.
- **age at break:** `20:25:48 → 22:49:54` = 2h24m06s (the pin existed, correct, for 2h24m).
- **fix:** `487941b9` (`2026-10-26T09:27:40-03:00`) rewrites the line to `(114/114)` / `(17/17)` plus two receipt
  paths; `git show 487941b9 -- SHONEN.md` (rc 0) is a one-line replacement, `-`/`+` as quoted in the diff above.
- **total stale:** `22:49:54 → 09:27:40` = 10h37m46s, across `43d84666`, `2023465f`, `7197160b` (round-49 end /
  spot-check / closure snapshot), the round-50 freeze `950e99be`, `649e14cf` and `9b8562a3`. None touched
  SHONEN.md.

Corroboration from the frozen C1 counter's own entering receipt,
`.ufo/waves/round-50/evidence/control-c1-do-nothing.txt:8-9`:

```
item pin python3_tools/mori-pin-check.py_--selftest expect=(60/60) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=mismatch
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(13/13) got=UNLANDED_SELFTEST_pass=17_fail=0 state=mismatch
```

and the landed receipts `.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt:116`
(`PIN_CHECK_SELFTEST pass=114 fail=0`) and `…/mori-unlanded-check.txt:19` (`UNLANDED_SELFTEST pass=17 fail=0`).

## 3. Which round's checklist step should have updated SHONEN

Short answer: **round 49** — the round whose landing commit (`64c2d5fc`) raised the instruments — owed the
rewrite, and no checklist step in the lane says so. That absence is the mechanism; the drift is its symptom.
The grounded chain:

1. Fleet duty, continuous, no step number: `PROTOCOL.md:517` (pinned rev `e0144996`) —
   "Axis work does not displace the file contract — a round that moves an axis while `corpus/`, `LOG.md`, or
   `SHONEN.md` drift is a conformance defect like any other." The same file's file table (`PROTOCOL.md:432`)
   says SHONEN is lane-owned — "Gates evolve — when they change, the owning lane regenerates `SHONEN.md`
   verbatim from the template on its next steered round (the lane is the only allowed writer inside its repo)"
   — and that "marks are confined to the box character plus one indented evidence line per box".
2. Axis definition: `AXES.md:15` — calibration is "SHONEN.md/SCORECARD entries match observed repo state",
   i.e. a SHONEN pin that disagrees with the tool is a calibration defect by definition.
3. The round prompt's step list names only SCORECARD: `.ufo/prompts/mori-round-50.md:22` ("Record per claim in
   SCORECARD.md: the score delta, evidence pointer, counting command, and measured commit"), and its §9 clause
   (`.ufo/prompts/mori-round-50.md:445`) only requires that a *calibration claim* count SCORECARD/SHONEN
   mismatches. Nothing in steps 1–9 instructs a SHONEN.md write.
4. The one lane rule that *does* require a same-commit instrument edit is `SKILL.md:1004`: "Run it before
   landing any round that edits a registry row or a registered tool; edit the reconciler's own row (the
   `PIN_CHECK_SELFTEST pass=N` pin above) in the same commit as the tool." Round 49 obeyed this exactly for the
   SKILL rows — `git show 64c2d5fc:SKILL.md` carries `PIN_CHECK_SELFTEST pass=114 fail=0` (row `SKILL.md:938`)
   and `UNLANDED_SELFTEST pass=17 fail=0` (row `SKILL.md:973`) — while SHONEN.md:7, a *second carrier of the
   same two tallies*, was not recognised as in scope.
5. The round-49 record proves the numbers were known and written the same round: `LOG.md:2727` in `487941b9`
   reads "… (`F1–F5`, …, R12–R14; selftest 114) and `tools/mori-unlanded-check.py` (17 arms) …". The tally was
   landed in prose and in SKILL.md, and omitted from SHONEN.
6. The round-49 closure also inventoried the tally's carriers and missed SHONEN:
   `corpus/lessons/round-49-verifier-spotcheck.md:27` (D-d) — "`PIN_CHECK_SELFTEST pass=114 fail=0` and the
   unlanded check's 17/17 appear only as prose in the report, `LOG.md` and the lesson."
7. Precedent for the class, scoped to the table half only: `corpus/lessons/round-29.md:26` — "M1 —
   self-assessment table not updated after admitted closures (class: stale self-assessment)", whose fix was a
   one-shot counter (round-29 `count-c1.sh`, `mismatches=11 → 0` at `420d05ad`). It covered the six `## Axes`
   rows, never SHONEN's pins, and it did not survive as a standing gate.

Two instruments exist and neither covers SHONEN currency:

- `grep -c 'SHONEN' tools/mori-pin-check.py tools/mori-unlanded-check.py` → `0` and `0`; QUALITY 123
  (`corpus/QUALITY.md:1028-1040`) scopes that standing gate to SKILL.md registry rows ("`python3
  tools/mori-pin-check.py --rev <rev> --baseline-rev <entering>` exits 0 before a round that edits a registry
  row or a registered tool lands").
- The only tool under `tools/` that reads SHONEN.md is `tools/mori-round13-regressions.py`
  (`DEFAULT_SHONEN = REPO / "SHONEN.md"`, line 171; `check_shonen`, line 1599). It requires whole-file byte
  equality with the 8-line `CANONICAL_SHONEN` seed (`matched = actual == expected`, line 1630) whose boxes are
  all `[ ]`. **A file carrying any `[~]` pointer is unequal to that seed**, so this arm is red for every
  annotated SHONEN — it can never measure pin currency. `[INFERENCE from code reading; harness not executed —
  it needs `--output` and runs census/journal fixtures, out of scope for this seat.]`

So the answer to the ticket's question, stated precisely: the lane has **no round-close checklist step that
names SHONEN.md**; the duty exists only as `PROTOCOL.md:517`'s conformance clause plus `AXES.md:15`. The round
that first owed it under that clause after the pins existed is **round 49** (`64c2d5fc`), and rounds 48 and 49
also owed it for the four Axes cells in §4.

## 4. When each of the four `Axes` `Last change` cells stopped being updated

Method (rc 0 at every step): walk all 99 revisions of `SCORECARD.md` oldest-first, take the last pipe cell of
each of the six axis rows **without** collapsing `\|`, and print only revisions where that cell changed. Cheap
re-runnable form:

```
git log --format=%H -- SCORECARD.md | tac | while read h; do \
  printf '%s ' "${h:0:8}"; git show $h:SCORECARD.md | grep -E '^\| (coverage|operability|depth|freshness|calibration|adjacency) \|' \
  | sed -E 's/\\\|/@/g; s/^(\| [a-z]+ \|).*\|\s*([^|]*)\|\s*$/\1 LAST=[\2]/'; done
```

Row positions verified identical (header at line 8, axis rows at lines 10-15) at
`420d05ad`, `cedb0ec4`, `bcf65505`, `daa1d4d2` and `487941b9`. Closure dates come from the fleet ledger
(`git -C /home/vgpnk/Projects/shokunin log --format='%h %cI %s' -- MANIFEST.json | grep 'mori r… closure'`;
MANIFEST verdicts read at the pinned fleet revision `e0144996`).

| axis | last write of the cell | cell's leading round | next improving closure **after** that write (first round the cell was already stale) | last improving closure ≤ 49 (true value) | rounds whose SCORECARD edits ignored it |
|---|---|---|---|---|---|
| **coverage** | `420d05ad7945e865ac6560289e5470f09409a9a1` 2026-10-22T17:14:24 (round-29 C1 fix) | `round 26` | **r47** — `0671906f` 2026-10-25T17:30:07 | r47 (improved) | r48 `e4dfff32`, r48 `91fbbc2a`, r49 `64c2d5fc` |
| **operability** | advanced last at `cedb0ec4f3a4f672804deac388b7191258f01fcd` 2026-10-23T06:06:42 (round-35); rewritten without advancing at `daa1d4d2` 2026-10-23T17:55:25 (round-38) | `round 31` | **r36** — `837ae190` 2026-10-23T16:28:49 (then r37 `51e86638` 17:29:11, i.e. **before** the `daa1d4d2` rewrite) | r47 (improved) | r36–r38, r39, r41, r43, r44, r46, r47, r48, r49 |
| **depth** | `cedb0ec4f3a4f672804deac388b7191258f01fcd` 2026-10-23T06:06:42 (round-35) | `round 31` | **r38** — `18b486c6` 2026-10-24T00:02:25 | r49 (improved) | r39, r41, r43, r44, r46, r47, r48, r49 |
| **calibration** | `bcf65505cf016fa50cd19e52f6dc287a3ca206a5` 2026-10-23T17:04:18 (round-37 receipts; added the "round-37 claim C1 …" note) | `round 25` | **r37** — `51e86638` 2026-10-23T17:29:11, i.e. **25 minutes after the cell was written** | r49 (improved) | r37–r38, r39, r41, r43, r44, r46, r47, r48, r49 |
| freshness | `bcf65505` / re-affirmed `daa1d4d2` | `round 28` | none — r28 (`0cbc5204` 2026-10-22T16:30:11) is still the last improving closure | r28 (agrees) | — |
| adjacency | `420d05ad` | `round 19` | none — r19 (`e76050da` 2026-10-21T07:17:44) is still the last improving closure | r19 (agrees) | — |

Reading the four stale cells: coverage stopped advancing on 2026-10-22 at 17:14 and was correct until r47
closed on 2026-10-25 at 17:30; operability stopped advancing on 2026-10-23 at 06:06 and was correct until r36
closed at 16:28; depth stopped on 2026-10-23 at 06:06 and was correct until r38 closed at 2026-10-24 00:02;
calibration stopped on 2026-10-23 at 17:04 and was correct for 25 minutes. The two never-stale cells are the
two whose last improving closure predates every write of the cell.

MANIFEST per-axis improving/harmed sets used above (admitted mori rounds only, pinned `e0144996`, rc 0):

```
coverage     r12 r14 r15 r16 r24 r25 r26 r47
operability  r18 r28 r31 r36 r37 r38 r39 r41 r43 r44 r47
depth        r12 r31 r38 r39 r41 r44 r47 r48 r49
freshness    r21 r26 r28
calibration  r12 r18 r19 r21 r22 r24 r25 r37 r38 r39 r41 r43 r44 r46 r47 r48 r49
adjacency    r14 r18 r19
```

## 5. Divergences from the last-known-good invariant

Last-known-good invariant, as the frozen C1 predicate states it (`.ufo/waves/round-50/contract.md`, P-C1):
every `Last change` first `round N` equals the latest admitted closure grading that axis improved/harmed, and
every SHONEN tally pin equals what the pinned instrument prints at R.

- **D1 (SHONEN half).** The pin was written correct (`91fbbc2a`) and the *same commit* that invalidated it
  (`64c2d5fc`) updated the SKILL registry row but not SHONEN.md: the tool is calibrated in one carrier and
  uncalibrated in the other for 10h38m. There is no instrument that could have caught it.
- **D2 (calibration cell).** The commit that wrote the cell (`bcf65505`) named round 37 in its text and left
  `round 25` as the leading round; the r37 closure landed 25 minutes later and the cell was never re-read. A
  cell can therefore cite a round in prose while its machine-readable leading round stays older — exactly the
  shape the round-29 counter was built to catch, and the reason a text-note is not a substitute.
- **D3 (operability cell).** `daa1d4d2` is the strongest instance: 1h27m after r36's closure (16:28) and 26 min
  after r37's (17:29) it rewrote the cell to add "round-37 C2 re-attributed here (score held, 7)" and still led
  with `round 31`. The writer had the closure fact in hand and did not advance the field it edits.
- **D4 (coverage, depth).** By the fix, both cells had sat through 44 (coverage) and 29 (depth) later SCORECARD
  revisions (`git log --format=%h <cell-last-write>..487941b9 -- SCORECARD.md | wc -l`, rc 0) without being
  re-read; `91fbbc2a` — the very commit that repaired the SHONEN line — left all six Axes cells citing closures
  ≤ r28 while r47's closure (all four axes improved) had been on the ledger for 2h55m.
- **D5 (class recurrence).** Round 29 fixed this class (`corpus/lessons/round-29.md:26`) with a one-shot
  counter; no standing gate replaced it. QUALITY 123's standing instrument stops at SKILL.md, and the only
  SHONEN reader asserts seed equality. So the same defect reappeared within 24h of the round-29 fix and stood
  for about 3 days.

## 6. Dated timeline (single view, hashes)

```
2026-10-14  ec0664e1  SHONEN seed minted (no tallies)
2026-10-14  27acf40c  SHONEN real province
2026-10-19  1f07f1dd  SHONEN r12 pointer update
2026-10-22  420d05ad  SCORECARD Axes: coverage→r26, operability→r28, freshness→r28, calibration→r25, adjacency→r19   [coverage's LAST WRITE]
2026-10-22  299d008a  (fleet) mori r31 closure (operability/depth improved)
2026-10-23  cedb0ec4  SCORECARD Axes: operability→r31, depth→r31                                              [operability+depth LAST WRITE]
2026-10-23  837ae190  (fleet) mori r36 closure (operability improved)             ← operability cell stale from here
2026-10-23  06:06     cedb0ec4 wrote r31 correctly; r36 closes 10h22m later and the cell is not re-read
2026-10-23  bcf65505  SCORECARD Axes: calibration note added, leading round stays r25                            [calibration LAST WRITE 17:04]
2026-10-23  51e86638  (fleet) mori r37 closure (calibration improved) 17:29     ← calibration cell stale 25 min after its write
2026-10-23  daa1d4d2  SCORECARD Axes: operability rewritten ("round-37 C2 re-attributed"), leads r31 — already stale
2026-10-24  18b486c6  (fleet) mori r38 closure (depth/operability improved)      ← depth cell stale from here
2026-10-25  16:32:10  63eecf27  tools/mori-pin-check.py introduced          selftest pass=22
2026-10-25  16:58:58  4dea3d09  pin-check v2                                pass=30
2026-10-25  17:03:53  af2250d8  pin-check v2 closes w1 findings            pass=34
2026-10-25  17:30:07  0671906f  (fleet) mori r47 closure (all four stale axes improved) ← coverage/operability/depth/calibration true value becomes r47
2026-10-25  19:30:52  e4dfff32  pin-check v3 + NEW mori-unlanded-check.py   pass=60 / pass=13
2026-10-25  20:25:48  91fbbc2a  SHONEN pins written (60/60) (13/13) — accurate at birth; Axes cells left ≤r28
2026-10-25  20:31:07  86475fb9  (fleet) mori r48 closure (depth/calibration improved)
2026-10-25  22:49:54  64c2d5fc  pin-check v4 (114) + unlanded 17; SKILL.md:938/973 updated; SHONEN.md NOT touched ← PINS STALE FROM HERE
2026-10-25  22:56:42  43d84666  round-49 end receipts        (SHONEN still 60/60)
2026-10-25  23:04:10  2023465f  round-49 verifier spot-check (D-d notes 114/17 as prose carriers; SHONEN not listed)
2026-10-25  23:04:30  a8292ab8  (fleet) mori r49 closure (calibration/depth improved) ← true Axes values become 49/49
2026-10-25  23:16:36  7197160b  round-49 closure snapshot (entering tip of round 50)
2026-10-26  05:45:42  950e99be  round-50 freeze (counter records expect=(60/60)/(13/13), got=114/17)
2026-10-26  09:27:40  487941b9  SHONEN → (114/114) (17/17) + receipts; Axes → 47/47/49/49  ← FIXED (stale 10h37m46s)
```

## 7. Draft M1 evidence block for `corpus/lessons/round-50.md` (fenced; the L1 owns the file)

```markdown
| M1 | self-assessment drift (class: stale self-assessment; round-29 M1 recurrence) | SHONEN.md:7 pinned `(60/60)` and `(13/13)` from `91fbbc2a` (2026-10-25T20:25:48) while `tools/mori-pin-check.py` printed `PIN_CHECK_SELFTEST pass=114 fail=0` and `tools/mori-unlanded-check.py` printed `UNLANDED_SELFTEST pass=17 fail=0` from `64c2d5fc` (2026-10-25T22:49:54) onward — 10h37m46s, five commits, no tool byte changed in between (`git log --format=%h 64c2d5fc..487941b9 -- tools/` empty). The same commit updated the SKILL rows `SKILL.md:938`/`:973` per the `SKILL.md:1004` same-commit rule and did not touch SHONEN.md (65 files, `SHONEN.md` absent); `LOG.md:2727` already carried "selftest 114 … 17 arms". Axes cells: coverage stuck at r26 from `420d05ad` (correct until r47 closed 2026-10-25T17:30:07), operability at r31 from `cedb0ec4` (stale from r36 `837ae190`; rewritten without advancing at `daa1d4d2` 1h27m after r36), depth at r31 from `cedb0ec4` (stale from r38 `18b486c6`), calibration at r25 from `bcf65505` (stale 25 min later at r37 `51e86638`). Receipt: `.ufo/waves/round-50/evidence/control-c1-do-nothing.txt:8-9`; analysis `.ufo/waves/round-50/a2w1/Mo50bRevenShonenDrift.md` | captured-by: seat Mo50bRevenShonenDrift (read-only git + `git archive` selftest re-runs at each tool commit) | fix: the round-50 C1 data commit `487941b9`; durable fix is a standing instrument over SHONEN.md/SCORECARD Axes — `corpus/QUALITY.md:1028` (QUALITY 123) stops at SKILL.md, `tools/mori-pin-check.py` has 0 SHONEN references, and `tools/mori-round13-regressions.py:1630` requires whole-file seed equality, so no existing gate can measure pin currency |
```

## 8. Unverified / limits of this seat

- `tools/mori-round13-regressions.py` was **not executed** (it requires `--output` and builds census/journal
  fixtures). The conclusion that its SHONEN arm is red for any annotated file is read from
  `CANONICAL_SHONEN`/`matched = actual == expected` and is marked `[INFERENCE]`.
- Fleet ledger dates are day-granular; I used the MANIFEST **commit** timestamps (the `hyaku` closure commits)
  as the closure times. The ordering conclusions that matter (r36/r37 before `daa1d4d2`; r37 after `bcf65505`)
  hold on commit timestamps and are stated with them.
- I did not re-run any round's counter; the counter verdicts quoted are the frozen receipts' own text.
- No kernel log, no cgroup, no systemd state was touched; nothing outside `git show`/`git archive`/`python3
  --selftest` was executed against the lane.
- No tool was installed or upgraded (nothing was needed; `python3` and `git` sufficed) — no RULES.md channel
  was used.
- Scratch `/fast/scratch/hyaku/mori-r50/Mo50bRevenShonenDrift/` (six `git archive` trees, `TMPDIR`) removed at
  seat end; `disk-guard.sh status` was read before the run (`/fast/scratch/hyaku` 24% used, 612.6G free).

## Findings

| # | severity | finding | file / line |
|---|---|---|---|
| F1 | **HIGH** | The two SHONEN tally pins were stale for 10h37m46s (2h24m after being written correct): `(60/60)` and `(13/13)` while the tools printed 114 and 17 from `64c2d5fc` to `487941b9`. The pin's own carrier was not updated by the commit that invalidated it. | `SHONEN.md:7` (at `91fbbc2a`…`9b8562a3`) |
| F2 | **HIGH** | No standing instrument covers SHONEN.md or the SCORECARD Axes cells: `mori-pin-check.py` reads SKILL.md only (`grep -c SHONEN` → 0; QUALITY 123 scopes it to registry rows), and the sole SHONEN reader requires whole-file equality with the `[ ]` seed, so any annotated SHONEN is red and pin currency is unmeasurable. This is why the round-29 M1 class recurred. | `corpus/QUALITY.md:1028-1040`; `tools/mori-pin-check.py`; `tools/mori-round13-regressions.py:1630` |
| F3 | **MED** | The calibration `Last change` cell was written with a round-37 note while leading with `round 25`, and went stale 25 minutes later when r37's closure landed (`51e86638`, 2026-10-23T17:29:11); it stayed ten improving closures behind (r37, r38, r39, r41, r43, r44, r46, r47, r48, r49) until round 50. | `SCORECARD.md:14` (at `bcf65505`, 2026-10-23T17:04:18) |
| F4 | **MED** | The operability cell was rewritten at `daa1d4d2` 1h27m after r36's closure and 26m after r37's, adding "round-37 C2 re-attributed here" while leaving the machine-readable leading round at `31` — the write had the closure fact and did not advance the field. | `SCORECARD.md:11` (at `daa1d4d2`, 2026-10-23T17:55:25) |
| F5 | **MED** | Coverage and depth cells were never re-read after 2026-10-22/23 through 44 and 29 later SCORECARD revisions respectively (`git log --format=%h <last-write>..487941b9 -- SCORECARD.md`); `91fbbc2a`, the commit that repaired SHONEN, left all six cells citing closures ≤ r28 while r47's closure had been on the ledger 2h55m. | `SCORECARD.md:10` (coverage), `SCORECARD.md:12` (depth) |
| F6 | **LOW** | The only lane rule requiring a same-commit instrument edit names "the reconciler's own row" (SKILL.md) and does not mention SHONEN.md, which carries the same two tallies; round 49 followed the rule literally and the second carrier drifted. | `SKILL.md:1004`; `SHONEN.md:7` |
| F7 | **LOW** | SHONEN's marks sit inline on the box line, while the fleet file contract says marks are "the box character plus one indented evidence line per box"; the form divergence is part of why the r13 whole-file arm cannot be used as a currency check. `[INFERENCE — contract reading; not adjudicated with the protocol lane.]` | `PROTOCOL.md:432` (fleet `e0144996`); `SHONEN.md:7` |
