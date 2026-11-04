# Mo85M01Mut — mutation probe of the three round-85 counters

Seat: Mo85M01Mut (mutation tester), mori round 85 w1, 2026-11-04. Milestone: round 85 w1
mutation probe of the three r85 counters. Detection and report only; no lane file other than
this report was touched.

## Scope and method

- Subjects: `.ufo/waves/round-85/count-c1.py`, `count-c2.py`, `count-c3.py` **byte-exact at the
  freeze commit `ab2608655ea52ba6d151b3a31d69a3b18cd2b41e`**, extracted with
  `git show <freeze>:<path>` into scratch. Note: HEAD (`91f657f6`) carries pre-data amendments
  A1–A4 which rewrote `count-c2.py` and `count-c3.py` (C1 is byte-identical freeze→HEAD,
  sha `da5fb27b…`). The primary probe is on the assigned freeze bytes; §5 re-runs the same
  detector arms against the amended HEAD bytes so the next round's clause list reflects the
  counters that will actually grade.
- Every mutant: one scratch copy, anchor `old` asserted to occur **exactly once** before
  mutating (`occurrences=1`, else refused — 0 refused), then that copy's own `--selftest`
  (`--scratch` under my scratch for C1/C3; C2's selftest is pure). Kill rule (frozen): killed
  iff rc != 0 **or** output contains `fail=<n>` with n > 0.
- Pristine baselines first, all green (below). A red pristine would have made everything
  inconclusive; none was red.
- Fixture repos for end-to-end demos: `mktemp`-style dirs under
  `/fast/scratch/hyaku/mori-r85/Mo85M01Mut/fixtures/`, each `git init`-ed with
  `-c user.name=t -c user.email=t@t` and asserted `rev-parse --show-toplevel == $dir` before
  first commit. Counters ran read-only against those fixtures. Scratch deleted before yield.
- Tooling: stock `python3` (system) and `git`; **no tools installed or upgraded** (pacman guard
  respected; nothing else needed).

Subjects (sha256, freeze bytes) and pristine selftests:

| counter | sha256 (freeze bytes) | baseline `--selftest` |
|---|---|---|
| count-c1.py | `da5fb27b9cd9b9cfbbefc58fb2465fb162f796cd280f82d0aeee0e8deca485fe` | rc 0, `pass=18 fail=0` |
| count-c2.py | `b7a4e691738f8161660887f3dada1045757e3bce4241968028d3dc353586d474` | rc 0, `pass=15 fail=0` |
| count-c3.py | `c035e32f465eb5457870c6e5b18a05212e3cdee27f4f79f0cd65999b1f147b44` | rc 0, `pass=19 fail=0` |

## 1. Headline

**MUTANTS total=48 killed=18 survivors=30** (refused=0, all anchors occurrences=1).

| counter | total | killed | survivors | non-equivalent survivors | equivalent survivors |
|---|---|---|---|---|---|
| C1 | 17 | 9 | 8 | 6 | 2 |
| C2 | 14 | 4 | 10 | 8 | 2 |
| C3 | 17 | 5 | 12 | 11 | 1 |

The selftests are real detectors — every clause they arm, they kill (18/18 predicted kills
confirmed) — but they arm only their synthetic cases. 30 behavior changes pass green, and 27 of
them change a real run's verdict (demonstrated end-to-end for 19 of them; the rest differ by the
same mechanism). Two freeze-era gaps the amendments were already closing (bind-at-own-rev,
subject verdict) are confirmed with fixture evidence, and their fixes are themselves unguarded
(§5).

## 2. Killed mutants (detector arms work)

| id | site (freeze bytes) | mutation | evidence |
|---|---|---|---|
| C1-01 | `green()` | drop `rc == 0` conjunct | `green_boundary` arm, rc 1 fail=1 |
| C1-02 | `killed()` | drop `FAIL.search` conjunct | `killed_boundary` arm |
| C1-04 | `TARGET` | `(2,0,2)`→`(2,0,3)` | `target_split_ok` arm |
| C1-05 | `TARGET_ARMS` | 17→18 | `arms_green`/`target_split_ok` arms |
| C1-06 | `TAIL_ARMS` | `(\d+)`→`(\d)` | `target_split_ok` arm crashes on unmatchable `arms=17` |
| C1-14 | grade kill decision | `k = killed(rc, out)`→`k = False` | `killed_counted` arm |
| C1-15 | survivor scan | `" survived "`→`" killed "` | `survivor_counted` arm |
| C1-16 | `subject_ok` | `all`→`any` | `subject_markers_missing` arm |
| C1-17 | `FROZEN_MARKERS` | `= SUBJECT_MARKERS`→`() ` | `subject_markers_missing` arm |
| C2-11 | parse header counts | drop `missing-<name>` problem | `bad_rev` arm (relies on missing-rev) |
| C2-12 | separator counts | drop `missing-separator` problem | `missing_separator` arm |
| C2-13 | binding counts | drop `missing-binding` problem | `missing_binding` arm |
| C2-14 | duplicate header counts | drop `duplicate-<name>` problem | `duplicate_cmd` arm |
| C3-12 | `reconcile` unmatched dir | `if mine != word:`→`if False:` | `reconcile_mismatch` arm |
| C3-13 | `derive` SURFACE branch | unknown surface → value-changed | `derive_surface_new` arm |
| C3-15 | `live_delta` set | `set(live_tokens)`→`set(snapshot_tokens)` | `delta_pairs` arm |
| C3-16 | `classifications` malformed | bogus line becomes stated value-changed | `classifications` arm |
| C3-17 | `classifications` dupes | `duplicates += 1`→`+= 0` | `classifications` arm |

## 3. Surviving mutants — the finding

### C1 (8 survivors; `arms=17` met path)

| id | site | mutation | class | observation |
|---|---|---|---|---|
| C1-03 | `FAIL` regex | `[1-9]`→`[2-9]` (fail=1 no longer fails) | **non-equivalent** | `green_boundary`/`killed_boundary` only test fail=0/fail=2. Fixture `c1a-flag`: pristine `C1=met killed=2` rc 0 → mutant `killed=0 survivors=2` rc 1. |
| C1-07 | `R84` regex | `total=4`→`total=\d+` | **non-equivalent** | `r84_target_free` only tries killed=3. Fixture `c1b-r84total9`: r84 stub printing `…total=9` — pristine rc 1 `r84=unmet`; mutant `C1=met … r84=met` rc 0. |
| C1-08 | `r84_at_rev` | drop `R84.search`, rc-only | **non-equivalent** | no selftest arm runs `r84_at_rev`. Fixture `c1c-r84wrong`: stub printing `C1=unmet …` rc 0 — pristine rc 1; mutant `C1=met` rc 0. |
| C1-09 | main tail conjunct | drop `int(tail_arms…) != TARGET_ARMS` | **non-equivalent** | `arms_ok` (which does check count) is never called by `grade()`/`main`. Fixture `c1d-arms15`: 15-arm harness — pristine rc 1; mutant prints `C1=met … arms=15` rc 0. |
| C1-10 | tail format | `arms=%d` fed `killed_n` instead of measured arms | **non-equivalent** | `c1a-flag`: pristine met → mutant `C1=unmet … arms=2`. |
| C1-11 | measured-arms assignment | `arms = arms_of(out)[0]`→`-1` | **non-equivalent** | `c1a-flag`: pristine met → mutant `C1=unmet … arms=-1`. |
| C1-12 | `met` conjuncts | drop unanchored/empty-mutation `not any(...)` | equivalent | Coupling: `TARGET=(2,0,2)` forces `total==2`; an unanchored or empty mutation is skipped and cannot be counted, so `target_split` already rejects every input this conjunct would reject. The conjunct never independently flips `met`. |
| C1-13 | `met` conjuncts | drop `total > 0` | equivalent | Same coupling: `total==0` leaves extras (`unanchored`/`empty-mutation`) that the remaining conjunct already rejects, and `MUTANTS` is a frozen non-empty pair, so `total>0` is implied whenever the other conjuncts hold. |

Note (finding, not a mutant): `arms_ok()` — the only function that checks the pristine harness's
arm count *and* both PASS labels — is armed in the selftest but **never called** by `grade()` or
`main()`. The met path checks arms only through the tail string, which is why C1-09/10/11
survive.

### C2 (10 survivors; receipt grammar)

| id | site | mutation | class | observation |
|---|---|---|---|---|
| C2-01 | parse: duplicate separator | drop `duplicate-separator` problem | **non-equivalent** | No selftest arm duplicates the separator. Fixture `c2g-twosep` (two `# ---` lines): pristine rc 1 mismatch=1 → mutant `C2=met` rc 0. |
| C2-02 | grade mismatch accumulator | `mismatch += len(problems)`→`+= 0` | **non-equivalent** | `duplicate_cmd` arm checks `parse_receipt` only, never grade. Fixture `c2a-dupcmd`: pristine unmet mismatch=1 → mutant met. |
| C2-03 | grade limits tally | drop `not problems.count("weak-limits")` | equivalent | Coupling: `parse_receipt` already emits the `weak-limits` *problem*, and grade adds every problem to `mismatch`; `met` requires `mismatch==0`, so a weak `# limits:` line can never reach the `limits==3` tally on a met path. The exclusion is redundant; no fixture can flip. |
| C2-04 | grade summary | `token in fields["body"]`→`token in text` | **non-equivalent** | `body_after_separator` arm checks `parse_receipt`'s body field, not grade's summary. Fixture `c2b-tokhdr` (token only in the header block): pristine `summary=2` rc 1 → mutant met rc 0. |
| C2-05 | `ancestor()` | non-equal path → `return True` | **non-equivalent** | Only `ancestor_equal` (rev==tip) is armed. Fixture `c2c-orphan` (receipt `# rev:` = parentless commit carrying the same tree): pristine `revs=2 bound=4` rc 1 → mutant met rc 0. |
| C2-06 | `verify_bindings` absent | absent path counts as bound | **non-equivalent** | No arm uses an empty loader. Fixture `c2f-ghost` (binds `tools/ghost.py`, not in tree): pristine `bound=4` rc 1 → mutant met rc 0. |
| C2-07 | `safe_path` | drop `"\\" in path` clause | **non-equivalent** | `safe_path` arm tests `/a`, `a/../b`, `a//b` — never backslash. Fixture `c2d-backslash` (real file named `tools\x.py`; git paths may contain backslash): pristine `unsafe-path` rc 1 → mutant met rc 0. |
| C2-08 | digest compare | `measured == sha`→`measured[:16] == sha[:16]` | **non-equivalent** | `stale_sha_mismatch` uses `0*64` which fails any prefix. Fixture `c2h-truncsha` (16 correct hex + 48 zeros): pristine rc 1 → mutant met rc 0. |
| C2-09 | grade bad-rev recheck | drop `bad-rev` block | equivalent (at freeze) | At freeze, `fields["rev"]` is only ever assigned from the `REV` regex match, which already requires exactly 40 lowercase hex and a full line — the `HEX` recheck is unreachable-false. Dead code; no behavior change. (At HEAD this code is reachable and armed — §5.) |
| C2-10 | `met` conjuncts | drop `mismatch == 0` | **non-equivalent** | No arm runs grade. Fixture `c2a-dupcmd`: mutant prints `C2=met … mismatch=1` rc 0. |

### C3 (12 survivors; census observation + reconciliation)

| id | site | mutation | class | observation |
|---|---|---|---|---|
| C3-01 | `observe_three` rc rule | `all(rc == 1)`→`all(rc in (0, 1))` | **non-equivalent** | Selftest never calls `observe_three`. Fixture `c3-exit0` (census stub exits 0 with a drift line): pristine `aa=unstable rcs=0,0,0` rc 1 → mutant met rc 0. Contract: every run must exit 1. |
| C3-02 | `observe_three` rc clause | drop rc clause | **non-equivalent** | Same fixture: mutant met rc 0. |
| C3-03 | stability compare | `tokens == first`→`sorted(tokens) == sorted(first)` | **non-equivalent** | Fixture `c3-shuf` (stub reorders 4 tokens per run): pristine `aa=unstable rcs=1,1,1` rc 1 → mutant met rc 0. `aa=stable` becomes set-equality. |
| C3-04 | `reconcile` unnamed dir | drop `agreed` skip | **non-equivalent** | All three reconcile arms pass with the skip removed (traced case-by-case). Fixture `c3-flagship` (all-agreed tokens, subject names no deltas): pristine met → mutant `unnamed=4` rc 1. |
| C3-05 | `derive` final line | known key → always `added-since-r10` | **non-equivalent** | No arm reaches the final line with a `KEYSHAPE` body (`+memory.peak` has a dot; `VERDICT` is caught earlier). Flagship fixture: pristine met → mutant `unnamed=2` (`+WATCHDOG`, `+CORE` flip to class-changed). |
| C3-06 | `derive` FINDING branch | unknown finding → always `value-changed` | **non-equivalent** | `derive_finding` only tests the known side. Flagship: `+FINDING:NEW` flips → `unnamed=1` rc 1. |
| C3-07 | `met` conjuncts | drop `subject_tokens == len(own_tokens)` | **non-equivalent** | Fixture `c3-tok99` (subject self-reports `live_tokens=99`): pristine rc 1 → mutant `C3=met … subject_tokens=99` rc 0. |
| C3-08 | `drift_tokens` | drop `token != "none"` filter | **non-equivalent** | `snapshot_parse` arm has no `none` token. Fixture `c3-none`: pristine met (own=1) → mutant `own_tokens=2 … unnamed=1` rc 1. |
| C3-09 | `met` conjuncts | drop `malformed == 0` | **non-equivalent** | Fixture `c3-bogus` (classification file with `DRIFT_CLASS ZZZ totally-bogus`): pristine rc 1 → mutant met rc 0. |
| C3-10 | `met` conjuncts | drop `duplicates == 0` | **non-equivalent** | Fixture `c3-dup` (duplicate DRIFT_CLASS line): pristine rc 1 → mutant met rc 0. |
| C3-11 | `met` conjuncts | drop `own_tokens` truthiness | equivalent | Coupling: `main` returns unmet at `if not stable or not own_tokens` before `met` is evaluated, so `met` is unreachable with empty `own_tokens`; the conjunct cannot flip any verdict. |
| C3-14 | `derive` table | `("VERDICT","HEADER","BLANK")`→`("VERDICT",)` | **non-equivalent** | `derive_table_word` only pins `VERDICT`. Fixture `c3-header` (token `HEADER`, stated value-changed, not a baseline key): pristine met → mutant `unnamed=1` rc 1. |

## 4. End-to-end fixture demos (freeze-byte counters)

22 verdict flips on 16 disposable fixture repos (each row: same fixture, pristine vs mutated
counter; full lines in the run log under my scratch, `fixt.json`):

- C1: `c1a-flag` (control met; C1-03/10/11 unmet), `c1b-r84total9`, `c1c-r84wrong`,
  `c1d-arms15` (pristine rc 1 → each mutant `C1=met` rc 0).
- C2: `c2-base` (control met), `c2a-dupcmd` (C2-02, C2-10), `c2b-tokhdr` (C2-04),
  `c2c-orphan` (C2-05), `c2d-backslash` (C2-07), `c2f-ghost` (C2-06), `c2g-twosep` (C2-01),
  `c2h-truncsha` (C2-08) — all unmet → met.
- C3: `c3-flagship` (control met; C3-04 unnamed=4, C3-05 unnamed=2, C3-06 unnamed=1),
  `c3-exit0` (C3-01, C3-02), `c3-shuf` (C3-03), `c3-tok99` (C3-07), `c3-none` (C3-08),
  `c3-bogus` (C3-09), `c3-dup` (C3-10), `c3-header` (C3-14) — flips as listed.

Recording caveats (honesty): in `c1b`/`c1c` the captured tail line is the r84 stub's own
`C1=…` line (the counter prints the stub's line after its verdict; my scraper takes the last
`C1=` line) — the **rc** is the counter's verdict in every row. C3-05's observation is
`unnamed=2`, not 1, because both key-shaped tokens (`+WATCHDOG`, `+CORE`) flip together.

## 5. Amendment delta — the same arms against HEAD (`91f657f6`, A1–A4)

Freeze mutants re-run on the amended bytes where the anchor still occurs exactly once:

- **C2**: C2-02/03/04/05/06/07/08/10/11 still **survive** the 18-arm HEAD selftest; C2-13/14
  still killed; C2-01/09/12 anchors moved (re-shaped by A2 — re-tested below).
- **C3**: all 11 freeze survivors still survive the 20-arm HEAD selftest; C3-12/13/15/16/17
  still killed. A3 added the verdict capture but armed none of the open clauses.
- **C1**: byte-identical at HEAD — all C1 results apply as-is.

HEAD-adapted mutants (new anchors):

| id | mutation | verdict | end-to-end |
|---|---|---|---|
| H-C2-01 | drop `duplicate-separator` (A2 shape) | **survived** (no arm) | `c2g-twosep-h`: HEAD-pristine rc 1 mismatch=1 → mutant met rc 0. Still open. |
| H-C2-A1 | `make_loader(rev)`→`loader` (reintroduce bind-at-tip) | **survived** (selftest is pure) | `c2i-earlyrev-h`: HEAD-pristine met rc 0 → mutant rc 1 `bound=4`. The A1 fix has no regression guard. |
| H-C3-verdict | remove A3's `fields["verdict"] = m.group(1)` | killed | `subject_verdict_required` arm — A3's capture is armed. |
| H-C3-metverdict | drop `fields.get("verdict") != "met"` from main | **survived** | `c3-unmetsubj-h`: HEAD-pristine rc 1 (subject prints `C2=unmet`) → mutant met rc 0. The *met-level* verdict conjunct is unguarded. |
| H-C2-12 | drop missing-separator (A2 shape) | killed | `missing_separator` arm (mutant copy crashes the arm's case — still a kill under the frozen rule). |
| H-C2-09 | drop bad-rev recheck (now reachable after A2) | killed | `bad_rev` arm — A2 armed it. |

Amendment closures confirmed with fixtures (both directions on identical fixture bytes):

- **A1** (bind at the receipt's own rev): fixture `c2i-earlyrev` — a contract-correct receipt
  bound at an ancestor commit with the *ancestor* bytes. Freeze counter: `C2=unmet … bound=4`
  (it hashed at the graded tip). HEAD counter: `C2=met` rc 0. The freeze-era code, not the
  predicate, was wrong — as A1's record states.
- **A3** (subject verdict): fixture `c3-unmetsubj` — subject prints `C2=unmet … live=derived`.
  Freeze counter: `C3=met` rc 0. HEAD counter: rc 1. A3 caught the code up to the frozen
  sentence.

## 6. Findings for the lane (detection only; not remediated)

1. **The met paths trust arithmetic the selftest never exercises.** Every C1/C2/C3 clause listed
   in §3 is a real detector clause with zero arm coverage at grade/observe level; the selftests
   pin their pure helpers and stop there. 19 of the 27 non-equivalent survivors flip a real
   `C[1-3]=met/unmet` verdict on a fixture.
2. **C1 `arms_ok()` is dead code on the met path** — the arms=17 guarantee flows only through
   the `arms=%d` tail field, so three independent plumbing mutants (C1-09/10/11) turn
   "17 arms" into an unfalsifiable claim. A1/A2's C1 row ("arm whose assertion is vacuous is the
   round's mutation-probe finding") is exactly this class.
3. **A1's fix is unguarded** (H-C2-A1 survivor + flip): one identifier swap reintroduces
   bind-at-tip with a green selftest. Same for **A3's met-level verdict conjunct**
   (H-C3-metverdict survivor + flip).
4. **Equivalent-by-coupling survivors** (C1-12/13, C2-03/09, C3-11) are not defects, but they
   show the selftests cannot distinguish conjunct-level edits — arming them requires
   restructuring (e.g. running `grade()` on synthetic loader/rev_ok pairs).

## 7. Unarmed clauses to arm next round

C1 (bytes identical at freeze and HEAD):
1. `FAIL` digit floor — add a `fail=1` boundary to `green_boundary`/`killed_boundary` (kills C1-03).
2. `R84` tail shape — arm `r84_at_rev` with a `total=9` stub and a wrong-verdict stub (kills C1-07/08).
3. Tail-arms plumbing — call `arms_ok()` on the pristine harness in `main` (or assert the tail's arms against `arms_of` output) (kills C1-09/10/11).

C2 (all still open at HEAD unless noted):
4. duplicate-separator problem → verdict (C2-01/H-C2-01).
5. grade-level problem accounting: run `grade()` on synthetic receipts with a duplicated `# cmd:` (kills C2-02, C2-10).
6. summary-token-after-separator at grade level (C2-04).
7. `ancestor()` non-equal path — a synthetic rev_ok pair or a fixture arm (C2-05).
8. `verify_bindings` with an absent path and with a wrong digest that shares a prefix (kills C2-06, C2-08).
9. `safe_path` backslash case (C2-07).
10. HEAD-only: `empty-cmd/rev/limits` and `malformed-binding` are new A2 problems with no grade-level arm.

C3 (all still open at HEAD):
11. `observe_three`: rc-must-be-1 and exact-order stability (C3-01/02/03) — needs a harness that injects synthetic run triples, or a pure `stability(rcs, token_lines)` helper the selftest can pin.
12. `reconcile` agreed-skip (C3-04); `derive` final-line key table, FINDING negative side, HEADER/BLANK words (C3-05/06/14).
13. `met` conjuncts: subject-token equality, malformed, duplicates (C3-07/09/10) — arm by calling the met expression on synthetic field dicts.
14. `drift_tokens` none-filter (C3-08).

## 8. Restoration evidence

- Lane files before and after the probe (sha256, unchanged; `git status --porcelain` clean on
  all four paths including the r84 subject):
  - `.ufo/waves/round-85/count-c1.py` `da5fb27b…` (== freeze bytes)
  - `.ufo/waves/round-85/count-c2.py` `49773893…` (== HEAD, A1–A3 bytes)
  - `.ufo/waves/round-85/count-c3.py` `43ad71d8…` (== HEAD, A3 bytes)
- Probe subjects were scratch copies at the freeze bytes; mutated copies lived only under
  `/fast/scratch/hyaku/mori-r85/Mo85M01Mut/mut/`; fixture repos under `…/fixtures/`. The whole
  scratch tree is deleted after this report is written.
- No commits, no mutating git/jj anywhere; fixture commits only (`user.name=t`), each fixture
  asserted `rev-parse --show-toplevel == fixture dir`.
