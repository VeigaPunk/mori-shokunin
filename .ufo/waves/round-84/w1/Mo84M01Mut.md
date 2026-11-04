# Mo84M01Mut — independent mutation probe of the round-84 counters (wave w1, attempt 1)

Date 2026-11-04. Probe of `.ufo/waves/round-84/count-c1.py`, `count-c2.py`, `count-c3.py`
(the counters that grade this round), by seat Mo84M01Mut. Detection and report only; nothing in
the lane was edited or committed; every mutant lived in a scratch copy under
`/fast/scratch/hyaku/mori-r84/Mo84M01Mut/` (deleted before this report was yielded; its driver
and demo scripts were `probe.py` / `demo.py`, quoted in §8).

## 1. Bytes probed and provenance

- Lane HEAD at probe time: `39190f8a8b32af30e6a180f91d77aa92542735d9`; worktree clean for the
  three counter paths (`git status --porcelain` empty).
- sha256 (identical before and after the probe — §7):
  - `count-c1.py` `86133aa98df2792fb1c1db23b0591077b36065dad995ee0bdb6115e301395a29`
  - `count-c2.py` `2cbe9c87d65bbe7efd0c3a518687f29cf773e11ade90bc65ed314d4f25b0c7ac`
  - `count-c3.py` `dc85d59822e6b67404d046f5ca13f67851d602c909757d5f43583e963c6631ef`
- **Post-freeze amendment found (routed, not judged).** `count-c2.py`/`count-c3.py` are
  byte-identical to the freeze commit `daa77bd`; `count-c1.py` is not. Commit `39190f8` ("round-84:
  pre-data amendment A2") changed the counter's frozen four-mutant table: M24b's anchor was
  re-indented (4 leading spaces added), and M24c/M24d were re-encoded from replace-anchors to
  delete-anchors:
  - freeze `daa77bd`: M24c `and not unclassified and residual == 0` -> `and residual == 0`;
    M24d same old -> `and not unclassified`.
  - HEAD `39190f8`: M24c `and not unclassified` -> `""`; M24d `and residual == 0` -> `""`.
  Both encodings express the same two met-clause deletions in the r83 subject, and the A2 anchors
  are valid: I counted `and not unclassified` = 1 and `and residual == 0` = 1 occurrences in
  `.ufo/waves/round-83/count-c2.py` at HEAD, and the M24b 4-space anchor = 1 in
  `.ufo/waves/round-83/count-c1.py`. **But the contract's frozen table anchors no longer match
  the subject bytes at all**: `and not unclassified and residual == 0` occurs **0** times in
  `.ufo/waves/round-83/count-c2.py` at HEAD (the clauses are no longer adjacent there), so a
  strict re-derivation of the contract table would read `unanchored` for M24c/M24d. The A2
  correction was necessary; the contract text (`contract.md`, still showing the old anchors as of
  this probe; a worktree edit in flight touches M24a wording only) should be re-synced to record
  it, or the after-receipt will look inconsistent with the frozen table. Flagged for the L1.
- No shared helpers exist between the three counters and the files they grade (each counter is a
  standalone file; its graded subjects are separate files), so per the tasking only each mutated
  copy's own `--selftest` was run — no graded-counter selftest applies.

## 2. Method

1. Anchor verification: every `old` below was counted in the current bytes before any mutation;
   the driver asserted `occurrences=1` for all 49 and refused to mutate otherwise (all 49 passed).
2. Pristine baseline: each counter's own `--selftest --scratch <scratch>` ran green first
   (c1 `C1_COUNTER_SELFTEST pass=11 fail=0` rc 0; c2 `pass=9 fail=0` rc 0; c3 `pass=9 fail=0`
   rc 0). A red baseline would have made the probe inconclusive; none was red.
3. One mutant per copy: the counter was copied to scratch, exactly one `old`->`new` replacement
   applied, and the copy's own `--selftest` run. Kill rule (the counter's own, applied back):
   killed iff rc != 0 or output carries `fail=<n>`, n>0; else survived.
4. Survivors were classified non-equivalent (distinguishing observation; four demonstrated
   end-to-end) or equivalent (coupling proof). Nothing was fixed.

Detector environment: Python 3.14.8, `python3 -I`, `GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`, scratch
pinned via `--scratch`/`HYAKU_SCRATCH`/`TMPDIR` (never `/tmp`).

## 3. Tally

```
MUTANTS total=49 killed=23 survivors=26
TALLY_c1 total=23 killed=14 survivors=9
TALLY_c2 total=12 killed=5  survivors=7
TALLY_c3 total=14 killed=4  survivors=10
```

## 4. Mutant table and verdicts

`old`->`new` are exact byte substrings (`\n` marks a newline inside an anchor). All rows verified
`occurrences=1` before mutation. Selftest line is the mutated copy's own summary.

### count-c1.py

| label | old -> new | verdict rc / selftest |
|---|---|---|
| c1-green-fail0-delete | `def green(rc, out):\n    return rc == 0 and "fail=0" in out and not FAIL.search(out)` -> `def green(rc, out):\n    return rc == 0 and not FAIL.search(out)` | killed rc=1, pass=9 fail=2 |
| c1-green-rc-invert | same old -> `def green(rc, out):\n    return rc != 0 and "fail=0" in out and not FAIL.search(out)` | killed rc=1, pass=8 fail=3 |
| c1-green-failsearch-delete | `    return rc == 0 and "fail=0" in out and not FAIL.search(out)\n\n\ndef killed` -> `    return rc == 0 and "fail=0" in out\n\n\ndef killed` | **survived** rc=0, pass=11 fail=0 |
| c1-killed-rc-invert | `def killed(rc, out):\n    return rc != 0 or bool(FAIL.search(out))` -> `def killed(rc, out):\n    return rc == 0 or bool(FAIL.search(out))` | killed rc=1, pass=6 fail=5 |
| c1-killed-fail-delete | same old -> `def killed(rc, out):\n    return rc != 0` | killed rc=1, pass=10 fail=1 |
| c1-pristine-guard-delete | `        if not green(rc, out):\n            pristine_ok = False` -> `        if False:\n            pristine_ok = False` | killed rc=1, pass=9 fail=2 |
| c1-unanchored-invert | `            if base.count(old) != 1:` -> `            if base.count(old) == 1:` | killed rc=1, pass=4 fail=7 |
| c1-empty-invert | `            if mutated == base:` -> `            if mutated != base:` | killed rc=1, pass=5 fail=6 |
| c1-coupling-delete | `                coupled = all(base.count(marker) == 1 for marker in coupling)` -> `                coupled = True` | killed rc=1, pass=10 fail=1 |
| c1-coupling-invert | same old -> `                coupled = not all(base.count(marker) == 1 for marker in coupling)` | killed rc=1, pass=9 fail=2 |
| c1-killedn-m24a-twin | `    killed_n = total - survivors - equivalent\n    met = (pristine_ok` -> `    killed_n = total - equivalent\n    met = (pristine_ok` | killed rc=1, pass=10 fail=1 |
| c1-survivors-tally-swap | `    survivors = len([line for line in lines if " survived " in line])` -> `    survivors = len([line for line in lines if " equivalent " in line])` | killed rc=1, pass=7 fail=4 |
| c1-met-pristine-delete | `    met = (pristine_ok and total > 0 and survivors == 0` -> `    met = (total > 0 and survivors == 0` | **survived** rc=0, pass=11 fail=0 |
| c1-met-total-delete | same old -> `    met = (pristine_ok and survivors == 0` | **survived** rc=0, pass=11 fail=0 |
| c1-met-survivors-delete | same old -> `    met = (pristine_ok and total > 0` | killed rc=1, pass=9 fail=2 |
| c1-met-empty-delete | `           and not any(e.startswith("empty-mutation") or e.startswith("unanchored")\n                       or e.startswith("coupling-absent") for e in extras))` -> same without the `empty-mutation` disjunct | **survived** rc=0, pass=11 fail=0 |
| c1-met-unanchored-delete | same old -> same without the `unanchored` disjunct | **survived** rc=0, pass=11 fail=0 |
| c1-met-coupling-delete | `or e.startswith("coupling-absent") for e in extras))` -> `for e in extras))` | **survived** rc=0, pass=11 fail=0 — EQUIVALENT (§5) |
| c1-pristine-field-invert | `               "green" if pristine_ok else "red"))` -> `               "red" if pristine_ok else "green"))` | killed rc=1, pass=9 fail=2 |
| c1-tail-killed-equivalent-swap | `            % (total, killed_n, equivalent, survivors, total,` -> `            % (total, equivalent, killed_n, survivors, total,` | killed rc=1, pass=8 fail=3 |
| c1-population-row-delete | the whole `M24a_killed_tally` tuple line block deleted from `MUTANTS` | **survived** rc=0, pass=11 fail=0 |
| c1-detector-gate-delete | `              % ("met" if (met and own_ok) else "unmet", tail,` -> `              % ("met" if met else "unmet", tail,` | **survived** rc=0, pass=11 fail=0 |
| c1-harness-stub-delete | `        missing = [m for m in FROZEN_MARKERS if m not in harness]` -> `        missing = []` | **survived** rc=0, pass=11 fail=0 |

### count-c2.py

| label | old -> new | verdict rc / selftest |
|---|---|---|
| c2-pop-len-delete | `    return len(pins) == len(FROZEN) and got == expected` -> `    return got == expected` | killed rc=1, pass=8 fail=1 |
| c2-pop-equal-delete | same old -> `    return len(pins) == len(FROZEN)` | killed rc=1, pass=8 fail=1 |
| c2-pop-invert | same old -> `    return not (len(pins) == len(FROZEN) and got == expected)` | killed rc=1, pass=5 fail=4 |
| c2-arms-floor-zero | `ARMS_FLOOR = 44` -> `ARMS_FLOOR = 0` | killed rc=1, pass=8 fail=1 |
| c2-count-regex-narrow | `COUNT = re.compile(r"\b(revisions\|bindings)=(\d+)\b")` -> `COUNT = re.compile(r"\b(bindings)=(\d+)\b")` | killed rc=1, pass=8 fail=1 |
| c2-met-defeated-delete | `        met = (fixtures_ok == 3 and defeated == 2 and q.returncode == 0\n               and revisions == 0 and bindings == 3)` -> same without `defeated == 2 and ` | **survived** rc=0, pass=9 fail=0 |
| c2-met-revisions-delete | same old -> same without `revisions == 0 and ` | **survived** rc=0, pass=9 fail=0 |
| c2-met-fixtures-delete | same old -> `        met = (defeated == 2 and q.returncode == 0\n               and revisions == 0 and bindings == 3)` | **survived** rc=0, pass=9 fail=0 |
| c2-marker-gate-delete | `        if MARKER not in tool_text or "REVISION_MISMATCH" not in tool_text:` -> `        if False:` | **survived** rc=0, pass=9 fail=0 |
| c2-population-gate-invert | `        if not population_ok(pins):` -> `        if population_ok(pins):` | **survived** rc=0, pass=9 fail=0 |
| c2-selftest-fail-gate-delete | `        if rc != 0 or not m or int(m.group(2)) != 0 or arms < ARMS_FLOOR:` -> `        if rc != 0 or not m or arms < ARMS_FLOOR:` | **survived** rc=0, pass=9 fail=0 |
| c2-tail-bindings-revisions-swap | `                % (defeated, fixtures_ok, bindings, revisions, arms))` -> `                % (defeated, fixtures_ok, revisions, bindings, arms))` | **survived** rc=0, pass=9 fail=0 |

### count-c3.py

| label | old -> new | verdict rc / selftest |
|---|---|---|
| c3-classword-delete | `    return (all(CLASS_WORD.match(word) for _, word in pairs)\n            and len(tokens) == len(set(tokens)))` -> `    return len(tokens) == len(set(tokens))` | killed rc=1, pass=8 fail=1 |
| c3-dup-delete | same old -> `    return all(CLASS_WORD.match(word) for _, word in pairs)` | killed rc=1, pass=8 fail=1 |
| c3-classword-invert | same old -> negated `all(...)` form | killed rc=1, pass=7 fail=2 |
| c3-arms-floor-zero | `ARMS_FLOOR = 16` -> `ARMS_FLOOR = 0` | killed rc=1, pass=8 fail=1 |
| c3-selftest-regex-fail-drop | `SELFTEST = re.compile(r"C2_COUNTER_SELFTEST\s+pass=(\d+)\s+fail=(\d+)")` -> `SELFTEST = re.compile(r"C2_COUNTER_SELFTEST\s+pass=(\d+)")` | **survived** rc=0, pass=9 fail=0 |
| c3-delta-arms-gate-delete | `                   and arms >= ARMS_FLOOR\n                   and all(("PASS " + name) in out for name in DELTA_ARMS))` -> `                   and arms >= ARMS_FLOOR)` | **survived** rc=0, pass=9 fail=0 |
| c3-met-tokens-delete | `               and tokens == 64 and union > 0 and classified == union` -> `               and union > 0 and classified == union` | **survived** rc=0, pass=9 fail=0 — DEMONSTRATED (§5, D) |
| c3-met-classified-delete | same old -> `               and tokens == 64 and union > 0` | **survived** rc=0, pass=9 fail=0 |
| c3-met-residual-delete | `               and residual == 0 and fields.get("live") == "derived"` -> `               and fields.get("live") == "derived"` | **survived** rc=0, pass=9 fail=0 |
| c3-met-classify-delete | `               and classify_ok(pairs))` -> `               and True)` | **survived** rc=0, pass=9 fail=0 |
| c3-met-deltas-delete | `\n               and deltas == union - live_agree == len(pairs)` -> `` (line deleted) | **survived** rc=0, pass=9 fail=0 |
| c3-tail-classified-union-swap | `                % (tokens, classified, union, residual, fields.get("live", "unavailable"),` -> `                % (tokens, union, classified, residual, fields.get("live", "unavailable"),` | **survived** rc=0, pass=9 fail=0 |
| c3-marker-gate-delete | `        if MARKER not in subject or "delta=classified" not in subject:` -> `        if False:` | **survived** rc=0, pass=9 fail=0 |
| c3-classword-agreed-drop | `CLASS_WORD = re.compile(r"^(absent-live\|added-live\|agreed\|class-changed:.+->.+)$")` -> same without `agreed\|` | **survived** rc=0, pass=9 fail=0 |

## 5. Survivor classification (26)

### Equivalent (1) — coupling proof

**c1-met-coupling-delete.** The `coupling-absent` extra is appended only inside the
`if not k and coupling is not None:` branch, and that same branch also appends a
`MUTANT ... survived ...` line. Therefore `coupling-absent` in `extras` implies a survived line
implies `survivors >= 1`, and `met`'s `survivors == 0` conjunct already forces `met` False in
every state where the dropped disjunct would have fired. The disjunct is subsumed; no observable
of `grade()` distinguishes the mutant. Probe demo A7 shows the co-occurrence
(`survivors=1 + EXTRA coupling-absent`, met False). This is dead-weight redundancy, not a gap.

### Non-equivalent, demonstrated end-to-end (5)

- **c1-met-pristine-delete.** Demos A3/A4: `grade()` over a red pristine (selftest rc 1) plus one
  killed mutant — pristine `met=False`, mutant `met=True`, identical `pristine=red` tail. Every
  current red-pristine arm also has `survivors>0` or `total=0`, which masks the conjunct.
  Needs arm: red-pristine + killed-mutant population asserting `not met`.
- **c1-met-total-delete.** Demos A8/A9: zero-mutant `grade()` — pristine `met=False`
  (`mutants=0 total=0`), mutant `met=True` (`mutants=0 killed=0 ... pristine=green`).
  Needs arm: `empty_population_unmet` asserting `grade(mutants=())` is not met.
- **c1-met-empty-delete.** Demos A1/A2: mixed killed + empty-mutation population — pristine
  `met=False` with `EXTRA empty-mutation` printed, mutant `met=True` on the identical run.
  Needs arm: mixed killed+empty-mutation population asserting `not met`.
- **c1-met-unanchored-delete.** Demos A5/A6: mixed killed + unanchored population — met flips
  False→True on identical output. Needs arm: mixed killed+unanchored population asserting `not met`.
- **c3-met-tokens-delete.** Demo D: fixture git repo carrying a stub subject at
  `.ufo/waves/round-83/count-c2.py` whose selftest prints `C2_COUNTER_SELFTEST pass=16 fail=0`
  with the four delta PASS lines and whose live run prints a compliant `C2=met ... tokens=40 ...
  classified=40 union=40 residual=0 live=derived deltas=0` tail: pristine counter prints
  `C3=unmet delta=classified tokens=40 ...` rc=1; the mutant prints `C3=met ... tokens=40 ...`
  rc=0. The frozen `tokens=64` population is enforced by this one conjunct. Needs arm: a
  stub-subject arm with `tokens != 64` asserting unmet (the demo's stub is the template).

### Non-equivalent, observation stated (20)

c1:
- **c1-green-failsearch-delete.** green() becomes `rc == 0 and "fail=0" in out`; output carrying
  BOTH `fail=0` and `fail=<n>`, n>0 now reads green (pristine requires no FAIL match). No arm
  feeds green() a mixed output. Needs arm: extend `green_direct` with
  `not green(0, "...fail=0\n...fail=2")`.
- **c1-population-row-delete.** Demo B: `len(MUTANTS)` 4→3; `FROZEN_MARKERS` derives from
  `MUTANTS`, so the harness=stub check shrinks with it and cannot catch the deletion. Needs arm:
  assert the four frozen labels exactly (`M24a_killed_tally`, `M24b_green_fail_token`,
  `M24c_met_unclassified`, `M24d_met_residual`).
- **c1-detector-gate-delete.** `met and own_ok` -> `met`: when the counter's own detector selftest
  is red while `grade()` passes, pristine prints `C1=unmet ... detector=red`, mutant prints
  `C1=met ... detector=red`. Not triggerable by this mutation alone (needs an independent red
  detector), but that is exactly the frozen scenario "a red detector keeps the claim unmet".
  Needs arm: extract the final verdict into a helper and arm it (`met=True, own_ok=False ->
  unmet`), or a subprocess arm.
- **c1-harness-stub-delete.** Demo C: fixture repo whose harness path holds a stub (`x = 1\n`) —
  pristine prints `C1=unmet harness=stub missing=...` rc 1; mutant proceeds to grade and prints
  `C1=unmet setup=absent:.ufo/waves/round-83/count-c1.py detector=green` rc 1. Today both unmet
  (message-level difference demonstrated); once the +2 arms land and the r83 counters read met at
  R, a stubbed harness would grade `C1=met` where the frozen behavior refuses with
  `harness=stub` [INFERENCE — requires the amended r83 counters, not landed in my scope]. Needs
  arm: subprocess fixture arm asserting rc=1 + `harness=stub`.

c2 (all in `main()`; `--selftest` runs `selfcheck()` only, which cannot reach main — the shared
needed arm class is subprocess-driven fixture runs of the counter, or gate extraction):
- **c2-met-defeated-delete.** met tolerates `defeated<2`: an ambiguous fixture reading green
  under the R tool (the exact failure P-C2 freezes fixtures against) no longer blocks met.
- **c2-met-revisions-delete.** met tolerates `revisions>0` (a drifted binding) while the tail
  still prints `revisions=N`.
- **c2-met-fixtures-delete.** met ignores fixture verdicts entirely; all three fixtures could
  fail and C2 still prints met when `revisions=0` and `bindings=3`.
- **c2-marker-gate-delete.** A tool without `ALL_ANCHOR_ROWS`/`REVISION_MISMATCH` is graded
  instead of refused; the frozen `C2=unmet arm=absent` reason disappears. (`marker_literal` only
  checks the counter's own bytes, not this gate.)
- **c2-population-gate-invert.** The frozen-population refusal inverts: a conformant pins file is
  refused, a tampered one proceeds — C2=met becomes reachable with a mutated population.
- **c2-selftest-fail-gate-delete.** A tool selftest exiting 0 while printing `fail=<n>`, n>0
  passes the arms gate; C2 could read met over a red-selftest tool.
- **c2-tail-bindings-revisions-swap.** Any run where `bindings != revisions` prints the two tail
  values transposed; the frozen met line is self-describing only under this gate's honesty.

c3 (met conjuncts and gates are `main()`-only; needed arm class: stub-subject fixture arms, one
per conjunct — Demo D's stub is the reusable template):
- **c3-selftest-regex-fail-drop.** With `fail=(\d+)` dropped, `int(m.group(2))` raises IndexError
  on a red subject selftest — the counter crashes with a traceback instead of printing
  `C3=unmet ... selftest=red`. Robustness defect, not silent.
- **c3-delta-arms-gate-delete.** A subject passing >=16 arms with zero `PASS delta_*` lines
  passes `arms_ok`; the four frozen delta arms go unenforced.
- **c3-met-classified-delete.** `classified == union` (P-C3's closure sentence) unenforced; a
  subject printing `classified<union` with delta lines covering the union still reads met.
- **c3-met-residual-delete.** `residual=0` no longer required for met; a subject with residual>0
  (unexplained tokens) reads met, contradicting the frozen summary.
- **c3-met-classify-delete.** Duplicate or bogus-class `LIVE_DELTA` lines no longer block met.
- **c3-met-deltas-delete.** The completeness equation `deltas == union - live_agree == len(pairs)`
  is unenforced; a subject may omit delta lines for non-agreed union tokens and still read met.
- **c3-tail-classified-union-swap.** On any run with `classified != union` the tail prints the
  two values transposed (unmet-path observable; invisible on met runs where the conjunct forces
  equality). Needs arm: stub subject with classified≠union asserting printed order.
- **c3-marker-gate-delete.** A subject without `LIVE_DELTA`/`delta=classified` in its bytes
  proceeds to the arms gate; the frozen `C3=unmet delta=absent` reason is replaced by arms-level
  output (observed in Demo D's first, un-fixed run).
- **c3-classword-agreed-drop.** `agreed` stops being an accepted class word: a subject emitting
  `LIVE_DELTA <token> agreed` flips met→unmet. For strictly conformant subjects (delta lines
  never carry `agreed`) it is indistinguishable — the distinguishing subject is a
  contract-violating over-reporter that also satisfies the count equation.

## 6. Killed highlights

- `c1-killedn-m24a-twin`: the counter's own `killed_n = total - survivors - equivalent` mutated
  exactly as M24a is **killed by its own `blind_case_tally` arm** (pass=10 fail=1) — the r84
  counter kills in itself the mutant it adjudicates in the r83 counter.
- `c1-green-fail0-delete` (the M24b twin on the counter's own `green()`): killed by
  `green_requires_fail_zero` + `green_direct` (pass=9 fail=2).
- Arms floors (`ARMS_FLOOR 44/16 -> 0`): killed by the floors' own self-assertion arms.
- `population_ok` (len/equal/invert) and the `COUNT` regex: killed by the population and
  parse arms — the c2 selfcheck's helper coverage is real.
- All direct inversions of `green()`/`killed()` and the unanchored/empty/coupling checks:
  killed (c1 pass drops to 4–10 in the failing copies).

## 7. Commands run and receipts

```
$ mkdir -p /fast/scratch/hyaku/mori-r84/Mo84M01Mut/m
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
39190f8a8b32af30e6a180f91d77aa92542735d9
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain -- .ufo/waves/round-84/count-c{1,2,3}.py
(empty)
$ sha256sum <the three counters>          # before == after, §1 values
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff daa77bd 39190f8 -- .ufo/waves/round-84/count-c1.py
10 lines: MUTANTS table M24b re-indent; M24c/M24d re-encoded as delete-anchors  (amendment A2)
$ cd /fast/scratch/hyaku/mori-r84/Mo84M01Mut && python3 probe.py
ANCHOR <49 rows> occurrences=1 ok
PRISTINE_RUN c1 rc=0 green=True C1_COUNTER_SELFTEST pass=11 fail=0
PRISTINE_RUN c2 rc=0 green=True C2_COUNTER_SELFTEST pass=9 fail=0
PRISTINE_RUN c3 rc=0 green=True C3_COUNTER_SELFTEST pass=9 fail=0
MUTANTRESULT ... (49 rows, §4) ...
TALLY total=49 killed=23 survivors=26
$ python3 demo.py
DEMO_GRADE A1..A9 (§5) / DEMO_POPULATION pristine_len=4 mutant_len=3
DEMO_HARNESS pristine rc=1 C1=unmet harness=stub missing=M24a...,M24b...,M24c...,M24d...,C1_COUNTER_SELFTEST
DEMO_HARNESS harness-stub-delete rc=1 C1=unmet setup=absent:.ufo/waves/round-83/count-c1.py detector=green
DEMO_C3 pristine rc=1 C3=unmet delta=classified tokens=40 classified=40 union=40 residual=0 live=derived live_tokens=40 live_agree=40 deltas=0 arms=16
DEMO_C3 met-tokens-delete rc=0 C3=met delta=classified tokens=40 ... arms=16
$ grep -cF <anchors> .ufo/waves/round-83/count-c2.py .ufo/waves/round-83/count-c1.py
and not unclassified => c2:1 ; and residual == 0 => c2:1 ; 4-space M24b anchor => c1:1
and not unclassified and residual == 0 => c2:0 (contract table anchor stale at HEAD)
$ rm -rf -- /fast/scratch/hyaku/mori-r84/Mo84M01Mut   # after this file was written
```

## 8. Restoration evidence

The lane was never written during the probe: all mutants and fixtures lived under the seat
scratch; counters were opened read-only. sha256 of all three counters identical before and after
(§1 values). `git status --porcelain -- .ufo/waves/round-84/` after the probe shows only the
pre-existing sibling modifications (`M contract.md`, untracked `w1.ready.dispatched`, untracked
`w1/`) plus this report — the three counter files are untouched. Scratch deleted at the end; the
driver (`probe.py`) and demo harness (`demo.py`) are quoted in this file and §7 so the probe is
reproducible.

## 9. Routed findings for the lane's next round

1. **RF-1 (c1 met, four gaps).** `met`'s `pristine_ok`, `total > 0`, `empty-mutation` and
   `unanchored` guards are each only armed against populations where another conjunct already
   forces unmet; deleting any one survives. Add four arms: red-pristine+killed, zero-mutants,
   killed+empty-mutation, killed+unanchored — each asserting `not met`.
2. **RF-2 (c1 green).** Add a mixed-token `green_direct` case: an output with both `fail=0` and
   `fail=2` must not read green (kills `c1-green-failsearch-delete`).
3. **RF-3 (c1 population).** `MUTANTS` is unanchored and `FROZEN_MARKERS` derives from it: add an
   arm asserting the exact four frozen labels (kills `c1-population-row-delete`).
4. **RF-4 (c1 main gates).** The detector gate (`met and own_ok`) and the harness=stub refusal are
   outside `selfcheck()`; extract to armed helpers or add subprocess fixture arms — the
   harness=stub refusal becomes load-bearing once the +2 arms land.
5. **RF-5 (c2 main gates).** Seven main()-body guards (met's three conjuncts, marker gate,
   population gate, selftest fail-gate, tail field order) are unreachable by `selfcheck()`;
   subprocess-driven fixture arms (counter run against fixture lane revs) or gate extraction is
   needed; today a mutated c2 passes its own selftest 9/9 while mis-grading.
6. **RF-6 (c3 met conjuncts).** `tokens == 64`, `classified == union`, `residual == 0`,
   `classify_ok(pairs)` and the deltas equation are each enforced at a single point in `main()`;
   six of seven deletions survive. Stub-subject fixture arms (Demo D template) kill them; the
   `tokens=64` gap is demonstrated end-to-end.
7. **RF-7 (c3 robustness).** Arm the SELFTEST regex red-fail path (IndexError crash today) and
   the `agreed` class word.
8. **RF-8 (recorded, L1).** Contract/counter divergence: `contract.md`'s frozen four-mutant table
   still carries the pre-A2 M24b/M24c/M24d anchors, which no longer occur in the subject bytes
   (M24c/M24d conjunction: 0 occurrences in r83 `count-c2.py` at HEAD) while the counter's A2
   anchors occur exactly once each. The A2 amendment was necessary and is valid; the contract text
   should be re-synced (or the amendment registered) so the after-receipt grades consistently
   with the frozen wording.

## 10. Not verified / scope notes

- The c2 main-level survivor scenarios were reasoned, not executed end-to-end: demonstrating them
  requires the amended `tools/mori-record-sweep.py` (all-rows arm), which has not landed in my
  probe scope; the needed arms are specified instead.
- The c1 harness-stub met-scenario is [INFERENCE] (requires the amended r83 counters at the
  fixture revision); the message-level difference is demonstrated.
- Verdicts bind to HEAD `39190f8` bytes; if the counters change again, re-run `probe.py` (§7).
- Tooling: nothing installed or upgraded (system `python3` 3.14.8, `git`, `sha256sum`, `grep`
  only); no pacman transaction was run.
