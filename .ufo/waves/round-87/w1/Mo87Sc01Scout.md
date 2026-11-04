# Mo87Sc01Scout — round-87 w1 reconnaissance

**Seat** Mo87Sc01Scout (scout, leaf — no dispatch) · **lane** mori-shokunin · **round** 87 · **wave** w1
**Read at** `03b66a437e68d493ce0aacd1d80c321cc2e6bf7c` (C1 tip; lane `HEAD` was `98f48dba3267a73714b862d0fd4fc8c0e82a1d04` while I ran)
**Scope** detection and report only. No lane file edited, no commit, no mutating git/jj. Scratch under `/fast/scratch/hyaku/mori-r87/Mo87Sc01Scout/`, deleted at exit.

Bytes I actually read (sha256, computed from `git show 03b66a43:<path>` **and** matched against the worktree — identical for all three):

| file | sha256 at `03b66a43` | lines |
|---|---|---|
| `.ufo/waves/round-86/count-c1.py` | `bcd66561093aa3046739f2be57a5f418e1ce87dd2da451beaece1e6ecffd5e7a` | 337 |
| `.ufo/waves/round-86/count-c2.py` | `28d667338674402fa6e72aa9c567f3f18c2387e4f8c1f0f5e4c63a894e02c584` | 419 |
| `.ufo/waves/round-86/count-c3.py` | `2e618dce42b38418e85868e48f4da2c895c39dcb634fd5626c5761818927a760` | 363 |

Arms measured by running each file's own `--selftest` on those bytes: `C1_COUNTER_SELFTEST pass=18 fail=0`, `C2_… pass=13 fail=0`, `C3_… pass=23 fail=0` — the frozen post-C1 counts.

---

## 0. Answer

**55 clauses in the three r86 counters are reachable by no selftest arm, beyond the six this round armed.** Each is stated as `(file, anchor, replacement)` with the anchor verified to occur **exactly once** in the bytes above, and each mutated copy was run through its own `--selftest`: **55/55 survive** (rc 0, correct tally). Distribution: `count-c1.py` 15, `count-c2.py` 25, `count-c3.py` 15.

They do not all deserve an arm:

- **Tier A — 25 acceptance gates**: `main()`'s entire accept/reject path plus the two `main`-only baseline parsers (`baseline_names`, `volatile_fields`; the third, `observe()`, runs the census and cannot be armed deterministically). No `selfcheck` arm can reach them as written; the cheap fix is to extract the gate as a pure predicate and arm that. This is the highest-value next-round item and the largest single block: every `C*=met/unmet` decision the counters print lives here and is currently unfalsifiable by their own selftests.
- **Tier B — 12 verdict clauses in reachable functions**: cheap, deterministic arms. I **demonstrated kills for 8 of them** (arm added to a scratch copy → pristine green at N+1 arms, mutant dies with a named `FAIL`).
- **Tier C — 15 structural/detail clauses**: real but lower stakes; all cheap to arm (4 demonstrated).
- **Tier D — 3 not worth an arm**: one conjunct is implied by another, one alternative is never read, one skip is unobservable for real commands. The right action is deletion, not an arm.

**The two C2 replay commands read nothing outside committed bytes.** Every read in `tools/mori-record-sweep.py` and `tools/mori-claim-sweep.py` is a committed path, a filesystem stat over the checkout, or a child process (`git`, `python3`, `bash`) whose own config is neutralised by the frozen counter's replay environment. The residual non-committed inputs are the toolchain, the inherited environment, and — for `record-sweep` — the *older* commits its pins resolve, which a `--shared` clone supplies through `info/alternates` (see §5.4).

---

## 1. Method, and what is measured vs inferred

1. **Byte identity** — `git show 03b66a43:<path>` hashed and compared with the worktree before any analysis (table above). The three counters did not change between `03b66a43` and `98f48dba`.
2. **Arm counts** — each counter's own `--selftest` run on a copy of the exact bytes, `TMPDIR`/`HYAKU_SCRATCH` inside scratch, `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM=/dev/null`, `python3 -I`. Result 18/13/23, matching the contract.
3. **Line-arc coverage** — an in-process `sys.settrace` instrument (`lines.py` in scratch, stdlib only) recorded executed source lines and line→line arcs per code object while `--selftest` ran. This is what identifies the never-executed regions in §2. It is **not** used as proof that a clause is unarmed: a single-expression helper produces no arcs at all while still being fully armed (see §2.2).
4. **Mutation evidence** — the operational definition of "no arm reaches it" is the frozen kill rule: a mutant the subject's own `--selftest` does not kill. 55 candidate mutants were applied to scratch copies and run; all 55 returned rc 0 with the pristine tally.
5. **Anchor uniqueness** — `base.count(anchor) == 1` asserted for every candidate before mutation; zero unanchored, zero empty-mutation, zero killed.
6. **Kill demonstrations** — for 8 tier-B candidates (and 4 tier-C) I added the proposed arm to the scratch copy and re-ran: pristine = green at N+1 arms, mutant = the named `FAIL` line / non-zero rc.
7. I did **not** run `.ufo/waves/round-87/count-c1.py` or `count-c2.py`. Verifying C1/C2 is other seats' work; my claims about them are limited to what the contract and the r86/r87 source say.

Everything in the tables below is measured against the bytes above unless marked `[INFERENCE]`.

---

## 2. What the current arm sets actually reach

### 2.1 Functions with zero selftest coverage

| file | function | reached by |
|---|---|---|
| `count-c1.py` | `main()` lines 283–331 | nothing (only argparse + the `--selftest` return at 277–282 run) |
| `count-c2.py` | `main()` lines 330–413 | nothing (same) |
| `count-c3.py` | `main()` lines 288–357 | nothing (same) |
| `count-c3.py` | `baseline_names()` 53–60 | only `main()` |
| `count-c3.py` | `volatile_fields()` 78–82 | only `main()` |
| `count-c3.py` | `observe()` 161–185 | only `main()` (and it runs the census, so it cannot be armed deterministically) |

`count-c3.py`'s `selfcheck` never calls `baseline_names`, `volatile_fields` or `observe` — confirmed by both the coverage trace and a call-site grep. That is 3 of its 12 non-`main` functions with no detector at all.

### 2.2 Helpers that look uncovered but are armed

`green()`, `killed()` and `atom_stable()` are one-expression functions; the tracer reports one executed line and **zero** arcs, because the boolean short-circuits inside a single line. Reading the arms, all three are in fact fully armed in both directions:

- `green()` — `green_boundary` exercises `rc != 0`, missing `fail=0`, and a `fail=N>0` body.
- `killed()` — `killed_boundary` exercises `rc != 0`, a `fail=2` body, and the negative.
- `atom_stable()` — `stability_empty` exercises `[]` (False) and a single map (True); `stability_atoms` exercises a mismatch.

Do not put these in a mutation population.

### 2.3 What each arm label is worth

18 + 13 + 23 arms, but some assert constants rather than behaviour: `target_arms`, `population_shape`, `target_line`, `observations`, `labels_unique`, and `marker_literal` (in all three files). They are legitimate — they would catch a target-constant edit — but they cannot detect a logic regression, and `arms=` as a progress metric counts them equally.

One arm is outright vacuous: `count-c2.py:265`

```
    cases.append(("export_lists_token", True, "no repo -> nothing exported"))
```

The predicate is the literal `True`. It cannot fail, and its label claims a property (`export_lists_token`) that the two real export arms do not test — both only exercise the *empty* export path. This is the one arm I would call coverage theatre. It should either become a real assertion or be removed.

---

## 3. Ranked unarmed clauses

Tier A = acceptance gate (blocks `met`/`unmet`); B = verdict clause in a function `selfcheck` already calls, cheap arm, deterministic; C = structural/detail; D = not worth an arm. Within a tier, ordered by what a regression would let through.

Every row: anchor occurs exactly once at `03b66a43`; the mutant survives today's selftest (measured).

### Tier A — acceptance gates (25 of 55)

#### `.ufo/waves/round-86/count-c1.py` (9)

| ID | line | clause | anchor → replacement | what would kill it |
|---|---|---|---|---|
| R88-01 | 289 | main: unresolvable-revision setup gate | `        if p.returncode != 0:` → `        if False:` | unresolvable rev → `C1_SETUP`, rc 2 |
| R88-02 | 301 | main: the counter's own PASS marker in own_out | `        own_ok = (own.returncode == 0 and "C1_COUNTER_SELFTEST" in own_out` → `        own_ok = (own.returncode == 0 and True` | helper arm with an own-output lacking `C1_COUNTER_SELFTEST` → unmet |
| R88-03 | 301 | main: own selftest rc==0 | `        own_ok = (own.returncode == 0 and "C1_COUNTER_SELFTEST" in own_out` → `        own_ok = (True and "C1_COUNTER_SELFTEST" in own_out` | helper arm with `own_ok` built from rc=1 → unmet |
| R88-04 | 304 | main: subject absent gate | `        if harness is None:` → `        if False:` | fixture repo without `.ufo/waves/round-85/count-c3.py` → `harness=absent`, rc 1 |
| R88-05 | 312 | main: detector=red gate | `        if not own_ok:` → `        if False:` | helper arm routing `own_ok=False` to the `detector=red` path |
| R88-06 | 321 | main: subject arms_ok gate | `        if not arms_ok(prc, pout):` → `        if False:` | helper arm with `subject_arms_ok=False`, all else green → unmet |
| R88-07 | 326 | main's detector=green gate: `met` conjunct | `if (not met or not target_split(tail)` → `if (not target_split(tail)` | helper arm with `met=False` and a target-shaped tail → must be unmet |
| R88-08 | 326 | main: target_split conjunct of the green gate | `if (not met or not target_split(tail)` → `if (not met` | helper arm with `met=True` and tail `killed=5 survivors=1` → unmet |
| R88-09 | 327 | main: `arms=` must equal TARGET_ARMS | `                or tail_arms is None or int(tail_arms.group(1)) != TARGET_ARMS):` → `                or False):` | helper arm with tail `… arms=25` → unmet |

#### `.ufo/waves/round-86/count-c2.py` (8)

| ID | line | clause | anchor → replacement | what would kill it |
|---|---|---|---|---|
| R88-10 | 352 | main: subject absent gate | `        if subject is None:` → `        if False:` | fixture repo without the subject path → `receipts=0 subject=absent` |
| R88-11 | 356 | main: missing-label stub gate | `        if missing:` → `        if False:` | subject bytes lacking one label string → `subject=stub missing=…` |
| R88-12 | 371 | main: subject carries the three labels | `        labels_ok = all(("PASS " + label) in sout for label in ARM_LABELS)` → `        labels_ok = True` | helper arm over a subject output missing one `PASS <label>` → unmet |
| R88-13 | 372 | main: subject arms == (TARGET_ARMS, 0) | `        subject_selftest_ok = (srun.returncode == 0 and arms == (TARGET_ARMS, 0)` → `        subject_selftest_ok = (srun.returncode == 0 and True` | helper arm with `arms=(20, 0)` → unmet |
| R88-14 | 396 | main: detector=red gate | `        if not own_ok:` → `        if False:` | helper arm with `own_ok=False` → unmet |
| R88-15 | 400 | main: subject selftest gate | `        if not subject_selftest_ok:` → `        if False:` | helper arm with `subject_selftest_ok=False` → unmet |
| R88-16 | 405 | main: subject run line gate | `        if not subject_run_ok:` → `        if False:` | helper arm with `subject_run_ok=False` → unmet |
| R88-17 | 409 | main: tail != TARGET conjunct | `        if not ok or tail != TARGET:` → `        if not ok:` | helper arm with `ok=True` and a tail ≠ TARGET → unmet |

#### `.ufo/waves/round-86/count-c3.py` (8)

| ID | line | clause | anchor → replacement | what would kill it |
|---|---|---|---|---|
| R88-18 | 57 | baseline_names: SURFACE name parse | `            surfaces.add(line[len("SURFACE "):].split(":", 1)[0])` → `            surfaces.add(line)` | arm: `baseline_names('SURFACE lane.mori: x\nFINDING WATCHDOG_STALE severity=high')` equals the three expected sets |
| R88-19 | 81 | volatile_fields: header field parse | `        if line.startswith("# volatile_fields="):` → `        if False:` | arm: `volatile_fields('# volatile_fields= age_s pid\n') == {'age_s','pid'}` and `volatile_fields('x') == set()` |
| R88-20 | 311 | main: census/baseline absent gate | `        if census is None or baseline is None:` → `        if False:` | fixture repo without `tools/mori-census.sh` → `observations=absent` |
| R88-21 | 314 | main: classification/snapshot absent gate | `        if classes is None or snapshot is None:` → `        if False:` | fixture repo without `corpus/evidence/drift-classification-r82.txt` → `observations=absent` |
| R88-22 | 327 | main: fulls_ok requires SURFACE rows | `            and all("SURFACE " in out for _rc, out in fulls)` → `            and True` | helper arm with `fulls_ok=False` (a full-run output without `SURFACE `) → `aa=unstable` |
| R88-23 | 328 | main: aa conjunct | `        aa = stability(rcs, token_lines, live_atoms) and fulls_ok` → `        aa = True` | helper arm with `aa=False` → unmet |
| R88-24 | 345 | main: value_rows==14 and contradicting==2 | `               and value_rows == 14 and contradicting == 2` → `               and True` | helper arm with `value_rows=13` → unmet |
| R88-25 | 349 | main: printed target must be the computed one | `        met = met and ("observations=%d` → `        met = ("observations=%d` | helper arm where the printed target equals TARGET but the counts do not → unmet |


### Tier B — verdict clauses in functions `selfcheck` already calls (12 of 55)

#### `.ufo/waves/round-86/count-c1.py` (3)

| ID | line | clause | anchor → replacement | what would kill it |
|---|---|---|---|---|
| R88-26 | 116 | arms_ok: green(rc,out) conjunct | `    return (green(rc, out) and failed == 0 and passed == TARGET_ARMS` → `    return (failed == 0 and passed == TARGET_ARMS` | **demonstrated** — `not arms_ok(1, label_out + tally)` arm kills it (`FAIL arms_red_rc`) |
| R88-27 | 133 | grade: loader raised -> setup=read | `            return False, "setup=read:%s:%s" % (path, exc), lines, extras` → `            return True, "setup=read:%s:%s" % (path, exc), lines, extras` | **demonstrated** — loader that raises → `FAIL setup_read_unmet` (`setup=read:tools/x.py:nope`) |
| R88-28 | 135 | grade: loader None -> setup=absent | `            return False, "setup=absent:%s" % path, lines, extras` → `            return True, "setup=absent:%s" % path, lines, extras` | **demonstrated** — loader returning `None` → `FAIL setup_absent_unmet` |

#### `.ufo/waves/round-86/count-c2.py` (6)

| ID | line | clause | anchor → replacement | what would kill it |
|---|---|---|---|---|
| R88-29 | 166 | ancestor(): merge-base direction | `    return run(["git", "-C", repo, "merge-base", "--is-ancestor", rev, tip]).returncode == 0` → `    return run(["git", "-C", repo, "merge-base", "--is-ancestor", rev, tip]).returncode != 0` | **demonstrated** — two-commit fixture, `ancestor(older,newer) and not ancestor(newer,older)` → `FAIL ancestor_direction` |
| R88-30 | 183 | grade_population: an absent receipt makes the population unmet | `            ok = False<br>            continue` → `            continue` | arm: a population row whose loader returns `None` must leave `ok` False and print `absent=1` |
| R88-31 | 197 | grade_population: rev_ok (rev present and ancestor) | `        rev_ok = bool(fields["rev"]) and ancestor(repo, fields["rev"], rev)` → `        rev_ok = True` | arm: `# rev:` naming a sibling commit that is not an ancestor → `rev` problem |
| R88-32 | 214 | replay: rc != 0 -> replay-rc | `            if rc != 0:` → `            if False:` | arm: `# cmd: false` (rc 1, empty stdout) with an empty body → `replay-rc:1` must appear |
| R88-33 | 216 | replay: body != stdout.rstrip | `            if body != out.rstrip("\n"):` → `            if False:` | **demonstrated** — `required` receipt whose body ≠ stdout → `FAIL replay_mismatch` |
| R88-34 | 220 | grade_population: reject routing | `        if expect == "reject":` → `        if expect == "rejected":` | arm: a `reject` row whose body has a problem → `ok` stays True, `defeated=1` |

#### `.ufo/waves/round-86/count-c3.py` (3)

| ID | line | clause | anchor → replacement | what would kill it |
|---|---|---|---|---|
| R88-35 | 70 | derive: FINDING branch | `        return "value-changed" if body[len("FINDING:"):] in findings else "added-since-r10"` → `        return "value-changed"` | **demonstrated** — `derive('+FINDING:WATCHDOG_STALE')`/`('+FINDING:NEW')` → `FAIL derive_finding` |
| R88-36 | 105 | stability: empty token line is unstable | `    if not all(token_lines) or any(tokens != token_lines[0] for tokens in token_lines[1:]):` → `    if any(tokens != token_lines[0] for tokens in token_lines[1:]):` | **demonstrated** — `stability([1,1],[[],[]],…)` must be False → `FAIL stability_empty_tokens` |
| R88-37 | 152 | value_verdict: one-sided absence | `    if not base or not live:` → `    if not base and not live:` | **demonstrated** — `value_verdict('x', base, live-without-x) == 'absent'`; the mutant dies by `TypeError` (rc≠0), not by a FAIL line |


### Tier C — structural and detail clauses (15 of 55)

#### `.ufo/waves/round-86/count-c1.py` (1)

| ID | line | clause | anchor → replacement | what would kill it |
|---|---|---|---|---|
| R88-38 | 100 | arms_of: last tally wins | `    for m in ARMS.finditer(out):` → `    for m in list(ARMS.finditer(out))[:1]:` | **demonstrated** — `arms_of(two tallies) == (20, 0)` → `FAIL arms_two_tallies` |

#### `.ufo/waves/round-86/count-c2.py` (10)

| ID | line | clause | anchor → replacement | what would kill it |
|---|---|---|---|---|
| R88-39 | 71 | header_and_body: no `# ---` -> empty body | `        return lines, ""` → `        return lines, text` | **demonstrated** — `header_and_body('# cmd: printf x\n')` body == `''` → `FAIL no_separator_empty_body` |
| R88-40 | 83 | header_fields: duplicate-cmd problem | `                problems.append("duplicate-cmd")` → `                problems.append("dup-cmd")` | **demonstrated** — two `# cmd:` lines → `FAIL duplicate_cmd` |
| R88-41 | 89 | header_fields: duplicate-rev problem | `                problems.append("duplicate-rev")` → `                problems.append("dup-rev")` | arm: two `# rev:` lines → `duplicate-rev` in problems |
| R88-42 | 95 | header_fields: duplicate-limits problem | `                problems.append("duplicate-limits")` → `                problems.append("dup-limits")` | arm: two `# limits:` lines → `duplicate-limits` in problems |
| R88-43 | 112 | no-replay reason: >= 3 words | `len(fields["no_replay"].split()) < 3` → `len(fields["no_replay"].split()) < 0` | arm: `# replay: none` with a 2-word reason → `missing-no-replay` |
| R88-44 | 158 | sha256_at: missing blob -> None | `    if q.returncode != 0:` → `    if False:` | arm: a binding naming a path absent at rev → `sha:<path>`; the mutant differs only if a receipt binds `sha256('')` |
| R88-45 | 191 | limits sub-gate: >= 3 words | `                and len(fields["limits"].split()) >= 3:` → `                and len(fields["limits"].split()) >= 1:` | arm: `# limits: limit x` (2 words) → `counts['limits'] == 0` |
| R88-46 | 209 | grade_population: legacy drops missing-replay | `        if replay_mode == "legacy":` → `        if replay_mode == "legacy-x":` | arm: a legacy row whose only problem is `missing-replay` must be clean |
| R88-47 | 216 | replay: trailing-newline normalisation | `            if body != out.rstrip("\n"):` → `            if body != out:` | arm: cmd prints `body\n`, receipt body is `body` → clean only because of `rstrip('\n')` |
| R88-48 | 228 | grade_population: matched counter | `                counts["matched"] += 1` → `                counts["matched"] += 2` | arm: a problem-free `met` row over the fixture → `counts['matched'] == 1` |

#### `.ufo/waves/round-86/count-c3.py` (4)

| ID | line | clause | anchor → replacement | what would kill it |
|---|---|---|---|---|
| R88-49 | 103 | stability: len(rcs) < 2 | `    if len(rcs) < 2 or any(rc != 1 for rc in rcs):` → `    if any(rc != 1 for rc in rcs):` | arm: `stability([1], [['a']], [{'x': 1}])` is False |
| R88-50 | 115 | token_line: literal `none` filtered | `        tokens = [token for token in m.group(1).split() if token != "none"]` → `        tokens = [token for token in m.group(1).split() if token != "NONE"]` | arm: `token_line('MORI_DRIFT: none x') == ['x']` |
| R88-51 | 124 | classifications: non-DRIFT_CLASS lines skipped | `        if not line.startswith("DRIFT_CLASS"):` → `        if False:` | arm: `classifications('noise\nDRIFT_CLASS A value-changed\n') == ([('A','value-changed')], 0, 0)` |
| R88-52 | 143 | value_body: non-keyshape body -> None | `    if body.startswith(NAME_SHAPE) or body in WORD_SHAPE or not KEYSHAPE.match(body):` → `    if body.startswith(NAME_SHAPE) or body in WORD_SHAPE:` | **demonstrated** — `value_body('foo*bar') is None` → `FAIL value_body_keyshape` |


### Tier D — not worth an arm (3 of 55)

#### `.ufo/waves/round-86/count-c1.py` (2)

| ID | line | clause | anchor → replacement | what would kill it |
|---|---|---|---|---|
| R88-53 | 63 | COUNT: `mutants` alternative never read | `COUNT = re.compile(r"\b(mutants\|killed\|survivors\|total)=(\d+)\b")` → `COUNT = re.compile(r"\b(killed\|survivors\|total)=(\d+)\b")` | not observable — no predicate reads `mutants=`; delete the alternative |
| R88-54 | 116 | arms_ok: failed==0 conjunct (implied by green) | `failed == 0 and passed == TARGET_ARMS` → `passed == TARGET_ARMS` | not killable — `failed == 0` is implied by `green()`; the fix is deleting the conjunct |

#### `.ufo/waves/round-86/count-c2.py` (1)

| ID | line | clause | anchor → replacement | what would kill it |
|---|---|---|---|---|
| R88-55 | 124 | export_rev: skip `-`-prefixed tokens | `        if not token or token.startswith("-") or "/" not in token or not PATHISH.match(token):` → `        if not token or "/" not in token or not PATHISH.match(token):` | not observable for real cmds — a `-`-prefixed token never resolves at `# rev:` |


### 3.1 The six already armed this round — do not re-propose

From the C1 diff (`6fc09d69..03b66a43`): `count-c1.py` gained `unanchored_plus_killed_unmet`, `zero_mutants_unmet`, `arms_tally_from_subject`; `count-c2.py` gained `summary_required`, `binding_required` and a `population=` parameter on `grade_population`; `count-c3.py` gained `derive_keyshape`. Those kill, respectively, the `not any(...)` conjunct in `met`, the `total > 0` floor, the `arms=` reading in the tail, the body summary-token requirement, the counter-sha256 comparison, and `derive()`'s keyshape branch. None of my 55 duplicates them. Note in particular that `c3-value-body-keyshape` is the **`value_body()`** copy of the keyshape test, not `derive()`'s (M6).

### 3.2 The probe's own named survivors that are still unarmed

`evidence/probe-r87.txt` named 17 survivors at the entering revision; C1 armed 6. The remaining 11 map onto this inventory as:

| probe label | my id |
|---|---|
| `c1-ownpass` | `c1-main-ownpass` |
| `c1-tailarms` | `c1-main-tailarms` |
| `c1-ownrc` | `c1-main-ownrc` |
| `c1-armsokmain` | `c1-main-armsok` |
| `c1-splitmain` | `c1-main-split` |
| `c2-replaymismatch` | `c2-replay-mismatch` |
| `c2-replayrc` | `c2-replay-rc` |
| `c2-limits3` | `c2-limits-len` |
| `c2-ancestor` | `c2-ancestor-invert` |
| `c2-revexists` | `c2-rev-ok` |
| `c2-unexpected` | `c2-expect-reject` + `c2-absent-ok` |

Everything else in §3 was **not** in the probe's population: the probe wrote 17 mutants and my static pass found 44 more. A next round that only consumes the probe's list will under-count the remaining surface by roughly 4×.

---

## 4. The cheapest path to tier A

Two shapes, in cost order:

**(a) Extract the gate.** Each `main()` is `parse argv → grade → print`. Move the decision into a pure function, e.g.

- `count-c1.py`: `def accept(own_ok, subject_arms_ok, met, tail) -> str|None` returning the unmet reason or `None`.
- `count-c2.py`: `def accept(own_ok, subject_present, subject_arms_ok, subject_run_ok, ok, tail)`.
- `count-c3.py`: `def accept(own_ok, aa, counts, printed) -> str|None`.

`main()` then only prints what `accept()` returns. One arm per disjunct kills each tier-A row, costs ~0.1 s, and needs no fixture repo. **This is a change to a frozen counter's internals, not to its printed predicate** — the frozen sentence is about the output line, so my reading is that no contract amendment is needed; that call belongs to the L1.

**(b) Subprocess arm.** `selfcheck` builds a fixture git repo in scratch and runs `python3 -I <this file> <rev> --repo <fixture>` twice (once clean, once with one planted survivor), asserting `C1=met …` / `C1=unmet … survivors=1`. This kills the tier-A rows without touching `main()`, but the fixture must carry a subject that contains all six `old` anchors and is killed by all six mutations — i.e. a synthetic copy of the r85 C3 counter. Cost is an order of magnitude higher and the arm becomes slow (~6 × 2 subprocesses).

---

## 5. The two C2 replay commands: every read

Both successors replay as `# replay: clone`, so the counter gives the command a real `git clone --shared` checked out at the receipt's `# rev:` and runs `bash -c <# cmd:>` with `cwd=<clone>`, `env = os.environ + {TMPDIR, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_SYSTEM=/dev/null, PYTHONDONTWRITEBYTECODE=1}` (`.ufo/waves/round-87/count-c2.py:170-200`).

`record-sweep-r87.txt` → `python3 -I tools/mori-record-sweep.py --root . --pins .ufo/waves/round-82/record-pins.json`
`claim-sweep-r87.txt` → `python3 -I tools/mori-claim-sweep.py --root . --pins .ufo/waves/round-80/claim-pins.json`
Both `# rev:` = `25a74d4c34e8430e4fbb18d4038ef5db872fb0ee`.

### 5.1 `tools/mori-record-sweep.py` — reads

| # | read | source | committed at `# rev:`? |
|---|---|---|---|
| 1 | `--root` (`.`) → `Path.resolve()`, `is_dir()` | filesystem metadata | n/a (the checkout) |
| 2 | `pins.read_text(encoding='utf-8')` | `.ufo/waves/round-82/record-pins.json` | **yes** |
| 3 | `texts[name] = lane_path(root,name).read_text()` | `SCORECARD.md` + every binding's `carrier` (this pins set has no bindings → only `SCORECARD.md`) | **yes** |
| 4 | per binding: `subprocess.run(binding['command'], cwd=root, encoding='utf-8', errors='replace')` | arbitrary argv; this pins set has **zero** bindings, so no child runs | n/a |
| 5 | `git -C <git> rev-parse --verify --end-of-options <rev>^{commit}` per revision binding | git object DB / refs (`--git` defaults to root = the clone) | **yes** — three bindings, revs `075574c8…` (×2) and `482dc48d…` |
| 6 | `git -C <git> show <commit>:<path>` | git object DB | **yes** — `SCORECARD.md` blobs |
| 7 | `git` itself: repo config, `$HOME`/XDG config, `.gitattributes` | global/system config forced to `/dev/null` by the caller; blob output is not textconv'd (`--textconv` is not passed) | yes / neutralised |

No clock, no randomness, no network, no socket, no temp file, no `os.environ` lookup by name, no absolute path outside `--root`.

### 5.2 `tools/mori-claim-sweep.py` — reads

| # | read | source | committed at `# rev:`? |
|---|---|---|---|
| 1 | `read_text(pins)` | `.ufo/waves/round-80/claim-pins.json` | **yes** |
| 2 | `read_text(lane_path(root, carrier))` per carrier | `SCORECARD.md`, `SKILL.md`, `SHONEN.md`, `LOG.md` (defaults; none passed here) | **yes** |
| 3 | `Path.resolve()` per pointer | symlink resolution on the checkout | yes |
| 4 | `exists(path)` per pointer | `stat` | yes |
| 5 | `glob.glob(str(path))` for `*`/`?` pointers | directory walk of the checkout | yes |
| 6 | `Path.is_symlink()` on every glob match and parent | `lstat` | yes |
| 7 | pinned tallies → `subprocess.run([sys.executable,'-I',tool,'--selftest'], cwd=root)` | `tools/mori-control-receipt.py`, whose `--selftest` is in-memory ("no files written, no subprocess") per its own docstring; `open()` exists only on the non-selftest path | **yes** |

No git at all, no clock, no randomness, no network, no writes.

### 5.3 Verdict

For these two receipts, in a clone checked out at `25a74d4c`, **every byte read is a committed byte**, with four conditions that the determinism argument rests on:

1. **Working tree, not blobs.** Both tools read files from the checkout. That is committed bytes *because* the replay clone is fresh and clean; in the lane worktree it is whatever is on disk — which is exactly why the r85 worktree receipts cannot be reproduced and are counted `legacy`. The `clone` mode is what turns this from a hope into a property.
2. **No `.gitattributes` at `25a74d4c`.** `git ls-tree -r` shows only `.gitignore`, so checkout bytes == blob bytes. If a future commit adds `eol` or `working-tree-encoding` attributes, `record-sweep` would compare working-tree bytes against `git show` blobs and the two would silently diverge.
3. **Toolchain, not repo state.** `python3`, `bash`, `git` are resolved through the inherited `PATH`; their versions and the stdlib are inputs the receipt does not pin. `git`'s global/system config is neutralised (`GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM=/dev/null`), and `python3 -I` ignores `PYTHON*` user env — so this is a *toolchain* dependency, not a repository one.
4. **Older commits for `record-sweep`.** Its three revision bindings resolve `075574c8…` and `482dc48d…`, which are ancestors of `# rev:` but are *not* the receipt's own revision. `git clone --shared` gives the clone `.git/objects/info/alternates`, so it borrows the source object store and these resolve. Consequence: the replay's input set includes the **source repository's object database at replay time**, not only the graded revision. Pruning those objects (or replaying from a clone whose alternates no longer reach them) turns the receipt into `rev-unresolvable` → `REVISION_MISMATCH` → non-zero. That is the one place where "reproduces from committed bytes" is true only if the graded repo still carries the history the pins name.

`claim-sweep` has no git read at all and therefore has none of condition 4.

### 5.4 One clause inside the replay that no arm covers

`record-sweep`'s `revision_sweep` reports on `git show` output; `claim-sweep`'s `parse_count` accepts four success grammars and rejects conflicting counts. Both are exercised only when the pins file names revisions / tallies — i.e. only in the population run, never in `--selftest`, and the r87 counter's replay arm does not inspect intermediate verdicts. If the C2 calibration axis wants the replay to be graded rather than merely reproduced, note that a body can be reproduced while the *reason* it is reproduced has changed (e.g. all three revision bindings could fall to `rev-unresolvable` and still print a different body — that would surface as `replay-mismatch`, so this specific case is caught; a change that keeps the summary line identical is not).

---

## 6. Confidence and remaining unknowns

| claim | evidence | confidence |
|---|---|---|
| 55 unarmed clauses, anchors unique, all survive | measured (55/55, rc 0, tally 18/13/23) | high |
| arms = 18/13/23 | measured on the exact bytes | high |
| `main()` bodies never execute under `--selftest` | coverage trace + line spans | high |
| `baseline_names`/`volatile_fields`/`observe` never called by `selftest` | coverage trace + call-site grep | high |
| 8 tier-B + 4 tier-C kills demonstrated | measured (pristine N+1 green, mutant FAIL) | high |
| tier-D equivalence judgments | static reading (`green` implies `failed == 0`; `mutants=` unread; `-`-token unreachable) | medium — `[INFERENCE]`; no arm can falsify an equivalent mutant |
| both replay commands read only committed bytes | full source read of both tools + the counter's replay env | high, conditional on §5.3 items 1–4 |
| `c3-main-target` is an equivalent mutant (`met = True and (…)`) | measured: survived, but semantically identical to pristine | high — deliberately excluded from the 55 |
| the `main()` refactor needs no contract amendment | reading of the frozen sentence (it constrains the printed line) | medium — `[INFERENCE]`, L1's call |

Things I could not settle from source alone:

- Whether a future pins edit could name a revision that the `--shared` clone cannot resolve. Both current pins resolve; I did not attempt to construct a failing one (that would be a mutation of a frozen population, not reconnaissance).
- Whether `claim-sweep`'s default carrier set is stable across revisions — `LOG.md` and `SHONEN.md` are read unconditionally, so a revision that deletes either makes the receipt `SETUP` (rc 2), not `met`. It is present at `25a74d4c`.

## 7. Hygiene

- No tool installed or upgraded. `python3` 3.14.8 and `git` were already present; the coverage instrument is stdlib-only and lived in scratch.
- No lane, OS, unit, service, credential, harness or orchestration state touched. No `agent://all`.
- Scratch `/fast/scratch/hyaku/mori-r87/Mo87Sc01Scout/` removed at the end of the seat's run, after this report was composed.
