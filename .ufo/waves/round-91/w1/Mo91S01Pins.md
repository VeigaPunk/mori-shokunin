# Mo91S01Pins — frozen receipts/counters that pin the round-87 subject's selftest arm count

Read-only mapping at entering revision `79eaa8cfe5e0b9b1c5ff45f524199d4a123f0520` (lane
`/home/vgpnk/Projects/shokunin/mori-shokunin`, branch `master`). No git writes; no lane edits outside
my two write paths. Subject = `.ufo/waves/round-87/count-c2.py` (the round-87 receipt gate; the
round-91 C1 subject per contract §C1). `pins.txt` is the one-line-per-hit expansion of the table
(77 lines; hits sharing a file+literal share a table row).

## 1. The subject's arm count at 79eaa8cf — **26**

Scratch clone: `git clone --shared <lane> $S/repo && git -C $S/repo checkout --detach 79eaa8cf…`.

```
$ cd $S/repo && TMPDIR=$S/tmp python3 -I .ufo/waves/round-87/count-c2.py --selftest
PASS marker_literal label
C2_COUNTER_SELFTEST pass=26 fail=0
rc=0
$ git show 79eaa8cf:.ufo/waves/round-87/count-c2.py | grep -c 'cases.append'
26
$ git show 79eaa8cf:.ufo/waves/round-87/count-c2.py | sha256sum
3fc9cc44a4f7ba6462aa36db48618f90018cb407981a532c183bdf13c6f1b377
```

**26 arms.** The gate has **no** `EXPECTED_ARMS` / `own_arms_pinned` constant (`git show
79eaa8cf:…/round-87/count-c2.py | grep -n -E 'EXPECTED_ARMS|own_arms_pinned'` → empty); its count is
observable only as the printed tally `pass=%d` (`count-c2.py:843`, from `len(cases)`). Its
`SUBJECT_ARMS = 13` (`:42`) pins the round-86 subject — a different one.

## 2. Table — every committed file whose text pins this fact

`kind`: **live-counter** = a `.py` that fails if the arm count changes; **frozen-receipt** =
`evidence/` text (immutable; superseded by record only); **frozen-contract** = predicate text;
**prose** = report/lesson text (no enforcement); *different-subject* = another file's own count.

| # | file:line | literal pinned | what it asserts | kind |
|---|---|---|---|---|
| 1 | `.ufo/waves/round-88/count-c2.py:35` | `SUBJECT_ARMS = 26` | the r87 gate's selftest arm count (its `SUBJECT` is the gate) | live-counter |
| 2 | `.ufo/waves/round-88/count-c2.py:39` | `TARGET = "real=met fx=4 clean=1 refused=2 absent=1 arms=26"` | arms field of the r88 counter's met line (mirrors the gate's count) | live-counter |
| 3 | `.ufo/waves/round-88/count-c2.py:265,267` | `target_fields` arm requires `"arms=26"` in `TARGET`; `target_full`: `TARGET == "…arms=26"` | the literal 26 inside TARGET, twice asserted | live-counter |
| 4 | `.ufo/waves/round-88/count-c2.py:282-283` | `own_ok_red` fixtures `"C2_COUNTER_SELFTEST pass=26 fail=0"` | self-fixture strings, not gate-derived | live-counter |
| 5 | `.ufo/waves/round-88/count-c2.py:300,385` | `frozen_constants`: `SUBJECT_ARMS == 26`; `subject_ok = … arms == (SUBJECT_ARMS, 0)` | the constant re-asserted, and the gate's measured tally must be (26,0) | live-counter |
| 6 | `.ufo/waves/round-88/count-c2.py:9` (docstring) | "green at exactly 26 selftest arms" | prose restatement | live-counter prose |
| 7 | `.ufo/waves/round-89/count-c1.py:30` | `SUBJECT_ARMS = 26` (`SUBJECT` = the r87 gate) | the gate's selftest arm count | live-counter |
| 8 | `.ufo/waves/round-89/count-c1.py:34` | `TARGET = "equiv=accepted comment=refused selfprint=refused real=met arms=26"` | arms field of the r89 C1 met line | live-counter |
| 9 | `.ufo/waves/round-89/count-c1.py:204,205` | `target_fields` requires `"arms=26"`; `arms_pinned`: `SUBJECT_ARMS == 26` | literal 26 and the constant re-asserted | live-counter |
| 10 | `.ufo/waves/round-89/count-c1.py:267` | `subject_ok = … arms == (SUBJECT_ARMS, 0)` | the gate's measured tally must be (26,0) | live-counter |
| 11 | `.ufo/waves/round-89/count-c1.py:8-9` (docstring) | "`… real=met arms=26`" / "green at exactly 26 selftest arms" | prose restatement | live-counter prose |
| 12 | `.ufo/waves/round-89/count-c2.py:52-53,56` | mutant anchors `'TARGET = "real=met … arms=26"'` etc. in `round-88/count-c2.py` | exact-once anchor on row 2's literal | live-counter (anchor) |
| 13 | `.ufo/waves/round-90/count-c2.py:62-63,66` | the same three anchors on the same r88 literal | exact-once anchor on row 2's literal | live-counter (anchor) |
| 14 | `.ufo/waves/round-89/count-c2.py:39,300` | `ARMS_BY_FILE = {"count-c1.py": 28, "count-c2.py": 26}` | r88 counters' **own** arm counts | live-counter, different-subject |
| 15 | `.ufo/waves/round-90/count-c2.py:49,396` | `ARMS_BY_FILE = {"count-c1.py": 29, "count-c2.py": 27}` | r88 counters' own arm counts | live-counter, different-subject |
| 16 | `.ufo/waves/round-89/evidence/selftests-r89.txt:3` | `C2_COUNTER_SELFTEST pass=26 fail=0` (cmd line 2 = the gate's `--selftest`) | the gate's arm count = 26 | frozen-receipt |
| 17 | `.ufo/waves/round-89/evidence/after-r89.txt:14`; `after-r89-final.txt:15` | `C1=met … real=met arms=26 rev=9f4d20b9290f`; `… rev=7715bb56dce6` | gate green at 26 arms at both revs | frozen-receipt |
| 18 | `.ufo/waves/round-89/evidence/controls-r89.txt:40` | `C1=unmet … real=met arms=26 detector=green rev=817595354de4` | labels-without-rule control: gate still at 26 arms | frozen-receipt |
| 19 | `.ufo/waves/round-89/evidence/controls-r89.txt:8,9` | `… arms=23 subject=arms:(23, 0) rev=30a29797`; `C2_COUNTER_SELFTEST pass=23 fail=0` | gate at **23** arms at r89 entering | frozen-receipt, historical |
| 20 | `.ufo/waves/round-89/evidence/controls-r89.txt:51` | `EXTRA pristine-red .ufo/waves/round-88/count-c1.py rc=1 arms=26` | r88-c1's own pass count | frozen-receipt, different-subject |
| 21 | `.ufo/waves/round-89/evidence/controls-r89.txt:64` | `C2=unmet … arms=26,26 detector=green` | r89-c2's own arms-by-file (confounded control) | frozen-receipt, different-subject |
| 22 | `.ufo/waves/round-90/evidence/after-r90.txt:32` | `C2=met … arms=29,27 rev=11197820c6dc` | r88 counters' own arms | frozen-receipt, different-subject |
| 23 | `.ufo/waves/round-90/evidence/after-r90.txt:44` | `EXTRA pristine-arms .ufo/waves/round-88/count-c2.py arms=26 want=27` | r88-c2's own arms | frozen-receipt, different-subject |
| 24 | `.ufo/waves/round-90/evidence/controls-r90.txt:21` | `C2=unmet … arms=28,26 detector=green rev=037c02ca43a5` | r88 counters' own arms | frozen-receipt, different-subject |
| 25 | `.ufo/waves/round-88/evidence/after-r88.txt:21` | `C2=met … arms=23 rev=d5e2eda49487` | gate at 23 arms at the r88 landing | frozen-receipt, historical |
| 26 | `.ufo/waves/round-88/evidence/selftests-r88.txt:11` | `C2_COUNTER_SELFTEST pass=23 fail=0` | gate at 23 arms at the r88 landing | frozen-receipt, historical |
| 27 | `.ufo/waves/round-88/evidence/controls-r88.txt:66` | `C2=unmet … arms=17 subject=arms:(17, 0) rev=1bd5ec3fa260` | gate at **17** arms at r88 entering | frozen-receipt, historical |
| 28 | `.ufo/waves/round-89/contract.md:48` | `C1=met equiv=accepted comment=refused selfprint=refused real=met arms=26` | the frozen P-C1 label | frozen-contract |
| 29 | `.ufo/waves/round-89/contract.md:53` | "the gate at R is green at exactly **26** selftest arms (`C2_COUNTER_SELFTEST pass=26 fail=0`)" | the frozen P-C1 predicate clause | frozen-contract |
| 30 | `.ufo/waves/round-88/contract.md:65-66` | `… arms=23` / "green at exactly 23 selftest arms" | r88's frozen P-C2 (superseded) | frozen-contract, historical |
| 31 | `.ufo/waves/round-90/contract.md:45` | `… arms=29,27` | r88 counters' own arms | frozen-contract, different-subject |
| 32 | `.ufo/waves/round-87/contract.md:82,92` | `SUBJECT_ARMS = 11` (→ amended 13) | the **round-86** subject's count | frozen-contract, different-subject |
| 33 | `.ufo/waves/round-90/w1/Mo90K01Conn.md:11,13,33-42,144` (33-42 = the prior supersession table); `Mo90C01Critic.md:104,124`; `Mo90E03ArmsB46.md:18` | "`SUBJECT_ARMS = 26` **is the round-87 gate's arm count**"; the r88/r89 pin table | prior-round map of these pins; names the referent | prose |
| 34 | `.ufo/waves/round-89/w1/Mo89K01Conn.md:75,90`; `Mo89Sc01Scope.md:222,231`; `Mo89E03Replay.md:61`; `Mo89R01C1.md:10`; `round-90/w1/Mo90M01Mut.md:252` | "arms=26 is overloaded across at least four distinct facts"; "moves the r87 gate off 26 arms and breaks, in one stroke"; `pass=26 fail=0` | the overload warning, the break prediction, replayed measurements | prose |
| 35 | `SCORECARD.md:4630`; `corpus/lessons/round-90.md:17,79`; `corpus/lessons/round-89.md:39`; `corpus/lessons/round-89-verifier-spotcheck.md:49,116`; `corpus/QUALITY.md:2163` | "the gate's own selftest stays at **26 arms** (the r88/r89 `arms=26` pins are therefore not moved)"; "stale statements … only if the gate's arm count moves" | the r90 precedent: the pins stayed because the count did not move | prose (outside `.ufo/waves/`) |

Rows 1-11 are the **enforcing** pins; rows 12-13 are **anchor** pins on row 2's literal; rows 16-18
are the frozen receipts recording the fact; rows 19, 25-27 are the superseded historical values
(17 → 23 → 26) a supersession record should name; rows 14-15, 20-24, 31-32 are marked
*different-subject*.

## 3. Which pins actually break — measured, not inferred

**Fixture A (gate at 27 arms).** Scratch clone of the lane at 79eaa8cf; one extra `cases.append` in
the gate's selftest, committed in the fixture clone only (`rev-parse --show-toplevel` = `$D`).
```
$ python3 -I .ufo/waves/round-87/count-c2.py --selftest      # in the fixture clone
C2_COUNTER_SELFTEST pass=27 fail=0
$ python3 -I .ufo/waves/round-88/count-c2.py <fixture-rev> --repo $D --scratch $S/e1
C2=unmet real=met fx=4 clean=1 refused=2 absent=1 arms=27 subject=arms:(27, 0) rev=291da9fd6f08
rc=1
$ python3 -I .ufo/waves/round-89/count-c1.py <fixture-rev> --repo $D --scratch $S/e2
C1=unmet equiv=accepted comment=refused selfprint=refused real=met arms=27 subject=arms:(27, 0) rev=291da9fd6f08
rc=1
```

Rows 1-11 break on a 27-arm gate: r88's C2 counter and r89's C1 counter both read
`unmet … subject=arms:(27, 0)`, rc 1. **The r88/r89 `arms=26` pins are live-counter pins on the
gate's count.** **Fixture B (r88 TARGET literal edited 26→27, gate untouched):** rows 1-11 still
hold but rows 12-13 (exact-once anchors) do not:

```
$ python3 -I .ufo/waves/round-90/count-c2.py <fixture-rev> --repo $D --scratch $S/s90c2c
EXTRA isolated .ufo/waves/round-88/count-c2.py C2-no-supersedes arm=absent_without_supersedes fails=absent_without_supersedes,target_fields,target_full
C2=unmet mutants=14 killed=4 survivors=0 unattributed=0 unanchored=1 isolated=10 literal_anchors=0 arms=29,25 detector=green rev=731da9464611
```

Editing row 2's literal to follow a moved gate turns the r90 C2 population `unanchored=1
isolated=10` — **do not edit the r88 TARGET literal to track the gate**; record supersession
instead (coupling in `corpus/lessons/round-89.md:39`).

**Baseline at 79eaa8cf (pristine clone, same commands):**

```
round-88/count-c2.py rc=0  C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=26 rev=79eaa8cfe5e0
round-89/count-c1.py rc=0  C1=met equiv=accepted comment=refused selfprint=refused real=met arms=26 rev=79eaa8cfe5e0
round-89/count-c2.py rc=1  C2=unmet mutants=12 killed=12 survivors=0 unattributed=0 unanchored=0 arms=29,27 detector=green rev=79eaa8cfe5e0
round-90/count-c1.py rc=0  C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78 rev=79eaa8cfe5e0
round-90/count-c2.py rc=0  C2=met mutants=15 killed=15 survivors=0 unattributed=0 unanchored=0 isolated=0 literal_anchors=0 arms=29,27 rev=79eaa8cfe5e0
```

Measured caveat: `round-89/count-c2.py` is **already unmet at the entering revision** (rc 1,
`arms=29,27` vs its pinned `28,26`) — the r90 landing moved the r88 counters' own arm counts, so
row 14's pins are stale before round 91 starts. Rows 12-13's anchors still occur exactly once in
`round-88/count-c2.py` at 79eaa8cf (`grep -c` → 1): the r90 C2 population is intact.

**Gate self-pin gap.** The gate's count is derived at runtime from `len(cases)`, so a landing that
appends arms moves it with **no in-file constant to edit** — but it immediately contradicts rows
1-11, which live outside the subject and cannot be edited under the landing constraint.

## 4. Files written

- `.ufo/waves/round-91/w1/candidates/pins.txt` — 77 rows, one per hit, `path:line | pin | kind`
  — sha256 `43f8df25c155f5c043f55cf7ddf12e8ec742b5a24d5a92144e0c446cf3fbf061`
- `.ufo/waves/round-91/w1/Mo91S01Pins.md` — this report (digest in the yield message).

Both paths are absolute under `/home/vgpnk/Projects/shokunin/mori-shokunin/`. Nothing else in the
lane was written; no git mutation; scratch `$S` deleted before yield.

## 5. Limits and open defects

- Only pins whose referent is the **round-87 gate's own selftest arm count** are enforcing. Other
  `arms=26` occurrences are other files' own counts (r88/r86 counters, `tools/` selftests), labelled
  `different-subject`; the overload is documented at `round-89/w1/Mo89Sc01Scope.md:222`.
- The task's grep returns ~8 000 lines under `.ufo/waves/` (round-31 … round-86 files, JSON dispatch
  blobs, `pass=26` from `tools/` selftests). I filtered to the round-87 subject's own count; rows
  14-15, 20-24, 31-32 are kept but marked `different-subject`. The round-31 `count-c2.py` family was
  not opened: a different subject (round-31's own C2), not the round-87 gate.
- `round-89/count-c2.py`'s unmet state at entering (§3) means it cannot serve as a live witness in
  round 91; only its anchor row (12) remains meaningful.
- The round-91 counter (`count-c1.py`, frozen at the round root per contract) does not exist at
  79eaa8cf, so I could not measure its `pins=<a>` field against a moved gate.
