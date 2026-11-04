# Mo87M01Mut — mutation matrix over the two round-87 counters (w1, round 87)

seat Mo87M01Mut · lane mori · round-87 attempt 1 · wave w1 · 2026-11-04 · L1 MoriR87 · leaf seat, no subagent dispatch

**Scope.** Mutate `count-c1.py` and `count-c2.py`, run each mutated copy's own `--selftest`, and report which clauses the counter's own selftest does not catch. No lane file was edited; every mutation is a copy under my scratch. Detection and report only.

## Bytes read (recorded because siblings land work while this seat runs)

| object | bytes | sha256 |
|---|---|---|
| `count-c1.py` worktree (= blob at `03b66a43`) | 14904 | `e2ff968721678cc61d6a1674def8da3e27a43f3fed8daab79d53c657ae2c266e` |
| `count-c2.py` worktree (HEAD `b9e6f68d`) | 20617 | `264a43f04af1f9f939da7b3890f608a669a0c7fc2922656ee83f35adb236b14d` |
| `count-c2.py` blob at `98f48dba` (pre-A1) | 20560 | `e1dfd45a161b11a1ddfeae9bfe3d83f0f4f64c7d93dc0f85fc81d18e87ba7166` |

Lane HEAD when the seat started: `a42b1d795a7ebe9383f2421582182e2e341455bb`. Lane HEAD when this report was written: `22fa29194bba5508f372cb3b6a05d9bf7db5f64b` (siblings landed lesson/after-receipt commits while the matrix ran). Re-hashed at the writing HEAD: `count-c1.py` `e2ff968721678cc61d6a1674def8da3e27a43f3fed8daab79d53c657ae2c266e`, `count-c2.py` `264a43f04af1f9f939da7b3890f608a669a0c7fc2922656ee83f35adb236b14d` — both identical to the bytes above, so the moving HEAD did not move the counters.

`git diff 98f48dba -- .ufo/waves/round-87/count-c2.py` is exactly the contract's A1 amendment (three hunks: `SUBJECT_ARMS 11 → 13`, two extra labels, the `subject_arms` case renumbered); the C2 target string is byte-identical. Because the seat names both the worktree and the `98f48dba` bytes, the whole C2 table was run against **both** byte sets. `git diff 03b66a43 -- .ufo/waves/round-87/count-c1.py` is empty.

## Method

* Detector for every row: `python3 -I <mutated copy> --selftest --scratch <fresh dir>` with `TMPDIR=<fresh dir>/tmp`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_GLOBAL=GIT_CONFIG_SYSTEM=/dev/null`, cwd inside the fresh dir. `--scratch` only chooses where the counter puts its temp trees; it does not change the graded logic. Each mutant got a fresh scratch dir.
* Kill criterion: non-zero exit **or** a `FAIL ` arm line — the counters' own `killed()` predicate. A mutated copy that did not compile would be reported separately (`syntax` field in the harness JSON); none did.
* Anchors are exact byte strings and each occurs exactly once in its base (the harness refused to run otherwise; final table has 0 unanchored). Rendering: a real newline inside an anchor is shown as `\n`, and a literal pipe is `\|`; no anchor mixes a real newline with a literal backslash-n, so the rendering is unambiguous.
* No lane file was modified. Lane `count-c1.py`/`count-c2.py` hashes after the seat are identical to the hashes before it (restoration evidence: this seat never wrote them; the copies lived under `/fast/scratch/hyaku/mori-r87/Mo87M01Mut/`).
* Two full matrix runs produced byte-identical verdict/rc/FAIL sets (`matrix-run1.json` vs `matrix.json`), so the matrix is deterministic here.

## Baselines (pristine bytes, same harness)

| copy | rc | tally |
|---|---|---|
| `count-c1.py` worktree | 0 | `C1_COUNTER_SELFTEST pass=18 fail=0` |
| `count-c2.py` worktree | 0 | `C2_COUNTER_SELFTEST pass=17 fail=0` |
| `count-c2.py` @ `98f48dba` | 0 | `C2_COUNTER_SELFTEST pass=17 fail=0` |

Both counters are green on their own bytes: 18 arms (C1) and 17 arms (C2). The contract pins the *subjects'* arm counts (18/13/23 for the r86 counters) but not the r87 counters' own arm counts; that gap is finding 25/26 below.

## Matrix — 52 mutants

`expected detector` is the mutated copy's own `--selftest`; the expected verdict for a clause the selftest actually covers is `killed`.

| # | file | mutant | category | anchor | replacement | verdict | rc | FAIL arm(s) |
|---|---|---|---|---|---|---|---|---|
| 1 | `count-c1.py` | `c1-target-killed` | target-constant | `TARGET = (6, 0, 6)` | `TARGET = (6, 1, 6)` | **killed** | 1 | FAIL target_split_ok 6/0/6/54 |
| 2 | `count-c1.py` | `c1-target-arms` | target-constant | `TARGET_ARMS = 54` | `TARGET_ARMS = 48` | **killed** | 1 | FAIL target_split_ok 6/0/6/54; FAIL target_arms_free 48; FAIL per_file_arms_frozen 54 |
| 3 | `count-c1.py` | `c1-arms-table` | target-constant | `ARMS_BY_FILE = {\n    "count-c1.py": 18,\n    "count-c2.py": 13,` | `ARMS_BY_FILE = {\n    "count-c1.py": 18,\n    "count-c2.py": 11,` | **killed** | 1 | FAIL per_file_arms_frozen 54 |
| 4 | `count-c1.py` | `c1-met-floor` | met-conjunct | `    met = (pristine_ok and total > 0 and survivors == 0` | `    met = (pristine_ok and total >= 0 and survivors == 0` | **killed** | 1 | FAIL zero_mutants_unmet no mutants |
| 5 | `count-c1.py` | `c1-met-survivors` | met-conjunct | `and survivors == 0` | `and survivors >= 0` | **killed** | 1 | FAIL survivor_counted mutants=1 killed=0 survivors=1 total=1 arms=1 |
| 6 | `count-c1.py` | `c1-met-no-guard` | met-conjunct | `and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras))` | `and True)` | **survived** | 0 | — |
| 7 | `count-c1.py` | `c1-met-drop-unanchored` | met-conjunct | `("empty-mutation", "unanchored")) for e in extras))` | `("empty-mutation",)) for e in extras))` | **survived** | 0 | — |
| 8 | `count-c1.py` | `c1-met-drop-empty` | met-conjunct | `("empty-mutation", "unanchored")) for e in extras))` | `("unanchored",)) for e in extras))` | **survived** | 0 | — |
| 9 | `count-c1.py` | `c1-met-pristine` | met-conjunct | `    met = (pristine_ok and total > 0 and survivors == 0` | `    met = (True and total > 0 and survivors == 0` | **killed** | 1 | FAIL pristine_arms_floor 18 wanted; FAIL red_pristine_reported mutants=1 killed=1 survivors=0 total=1 arms=0 |
| 10 | `count-c1.py` | `c1-kill-rc-only` | kill-rule | `return rc != 0 or bool(FAIL.search(out))` | `return rc != 0` | **killed** | 1 | FAIL killed_boundary killed() |
| 11 | `count-c1.py` | `c1-kill-fail-only` | kill-rule | `return rc != 0 or bool(FAIL.search(out))` | `return bool(FAIL.search(out))` | **killed** | 1 | FAIL killed_boundary killed() |
| 12 | `count-c1.py` | `c1-green-drop-rc` | green-gate | `return rc == 0 and "fail=0" in out and not FAIL.search(out)` | `return "fail=0" in out and not FAIL.search(out)` | **killed** | 1 | FAIL green_boundary green() |
| 13 | `count-c1.py` | `c1-green-drop-failzero` | green-gate | `return rc == 0 and "fail=0" in out and not FAIL.search(out)` | `return rc == 0 and not FAIL.search(out)` | **killed** | 1 | FAIL green_boundary green() |
| 14 | `count-c1.py` | `c1-arms-first` | arms-tally | `for m in ARMS.finditer(out):` | `for m in list(ARMS.finditer(out))[:1]:` | **survived** | 0 | — |
| 15 | `count-c1.py` | `c1-killed-n` | arms-tally | `killed_n = total - survivors` | `killed_n = total` | **survived** | 0 | — |
| 16 | `count-c1.py` | `c1-survivors-match` | arms-tally | `survivors = len([line for line in lines if " survived " in line])` | `survivors = len([line for line in lines if " killed " in line])` | **killed** | 1 | FAIL killed_counted mutants=1 killed=0 survivors=1 total=1 arms=1; FAIL survivor_counted mutants=1 killed=1 survivors=0 total=1 arms=1 |
| 17 | `count-c1.py` | `c1-arms-total` | arms-tally | `arms_total += max(passed, 0)` | `arms_total += 1` | **survived** | 0 | — |
| 18 | `count-c1.py` | `c1-tail-arms` | arms-tally | `% (total, killed_n, survivors, total, arms_total))` | `% (total, killed_n, survivors, total, TARGET_ARMS))` | **killed** | 1 | FAIL arms_tally_read arms from subject |
| 19 | `count-c1.py` | `c1-anchor-guard` | anchor-accounting | `if base.count(old) != 1:` | `if base.count(old) == 0:` | **survived** | 0 | — |
| 20 | `count-c1.py` | `c1-split-field` | target-split | `fields.get("killed"), fields.get("survivors"),` | `fields.get("mutants"), fields.get("survivors"),` | **survived** | 0 | — |
| 21 | `count-c1.py` | `c1-fail-regex` | kill-rule | `FAIL = re.compile(r"\bfail=([1-9][0-9]*)\b")` | `FAIL = re.compile(r"\bfail=([0-9]+)\b")` | **killed** | 1 | FAIL killed_counted mutants=1 killed=1 survivors=0 total=1 arms=1; FAIL survivor_counted mutants=1 killed=1 survivors=0 total=1 arms=1; FAIL green_boundary green(); FAIL killed_boundary killed(); FAIL unanchored_plus_killed_unmet mutants=1 killed=1 survivors=0 total=1 arms=0 |
| 22 | `count-c1.py` | `c1-own-ok` | self-gate | `own_ok = (own.returncode == 0 and "C1_COUNTER_SELFTEST" in own_out` | `own_ok = (True or "C1_COUNTER_SELFTEST" in own_out` | **survived** | 0 | — |
| 23 | `count-c1.py` | `c1-mutant-spec-c2` | mutant-spec | `"met = (pristine_ok and total > 0", "met = (pristine_ok and total >= 0"` | `"met = (pristine_ok and total > 0", "met = (False or total >= 0"` | **survived** | 0 | — |
| 24 | `count-c1.py` | `c1-drop-arm` | arm-deletion | `    cases.append(("labels_unique", len(set(m[1] for m in MUTANTS)) == 6, "six labels"))\n` | `` | **survived** | 0 | — |
| 25 | `count-c2.py` | `c2-target-superseded` | target-constant | `matched=6 defeated=1 superseded=2 legacy=1 unexpected=0")` | `matched=6 defeated=1 superseded=1 legacy=1 unexpected=0")` | **killed** | 1 | FAIL target_line line |
| 26 | `count-c2.py` | `c2-target-replay` | target-constant | `"receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 "` | `"receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=3 "` | **killed** | 1 | FAIL target_line line |
| 27 | `count-c2.py` | `c2-subject-arms` | target-constant | `SUBJECT_ARMS = 13` | `SUBJECT_ARMS = 12` | **killed** | 1 | FAIL subject_arms 13/13 |
| 28 | `count-c2.py` | `c2-population-clone` | population | `(".ufo/waves/round-87/evidence/claim-sweep-r87.txt", "met", "clone", "CLAIM_SWEEP"),` | `(".ufo/waves/round-87/evidence/claim-sweep-r87.txt", "met", "required", "CLAIM_SWEEP"),` | **killed** | 1 | FAIL population_shape 3/2/1 |
| 29 | `count-c2.py` | `c2-population-legacy` | population | `(".ufo/waves/round-85/evidence/claim-sweep-r85.txt", "met", "legacy", "CLAIM_SWEEP"),` | `(".ufo/waves/round-85/evidence/claim-sweep-r85.txt", "met", "required", "CLAIM_SWEEP"),` | **killed** | 1 | FAIL population_shape 3/2/1 |
| 30 | `count-c2.py` | `c2-supersede-call-clean` | supersede-call | `if clean and supersede_verdict(name, clean_names, superseders):` | `if supersede_verdict(name, clean_names, superseders):` | **survived** | 0 | — |
| 31 | `count-c2.py` | `c2-supersede-verdict-clean` | supersede-call | `name in clean_names and target == legacy_name` | `target == legacy_name` | **killed** | 1 | FAIL supersede_absent_target absent; FAIL supersede_requires_clean unclean successor |
| 32 | `count-c2.py` | `c2-supersede-verdict-eq` | supersede-call | `name in clean_names and target == legacy_name` | `name in clean_names and target != legacy_name` | **killed** | 1 | FAIL supersede_matched match; FAIL supersede_counts_positive clean successor; FAIL supersede_wrong_target other |
| 33 | `count-c2.py` | `c2-supersede-counts-swap` | supersede-call | `counts["superseded"], counts["legacy"] = supersede_counts(` | `counts["legacy"], counts["superseded"] = supersede_counts(` | **survived** | 0 | — |
| 34 | `count-c2.py` | `c2-supersede-absent-target` | absent-accounting | `if target not in known:` | `if False:` | **survived** | 0 | — |
| 35 | `count-c2.py` | `c2-replay-compare-off` | replay-compare | `if body != out.rstrip("\n"):` | `if False:` | **survived** | 0 | — |
| 36 | `count-c2.py` | `c2-replay-compare-rstrip` | replay-compare | `if body != out.rstrip("\n"):` | `if body != out:` | **survived** | 0 | — |
| 37 | `count-c2.py` | `c2-absent-accounting` | absent-accounting | `counts["absent"] += 1` | `counts["unexpected"] += 1` | **survived** | 0 | — |
| 38 | `count-c2.py` | `c2-absent-ok` | absent-accounting | `            if expect != "reject":\n                ok = False\n` | `            if False:\n                ok = False\n` | **survived** | 0 | — |
| 39 | `count-c2.py` | `c2-defeated-accounting` | absent-accounting | `counts["defeated"] += 1` | `counts["matched"] += 1` | **survived** | 0 | — |
| 40 | `count-c2.py` | `c2-summary-token` | summary | `if token in body:` | `if True:` | **survived** | 0 | — |
| 41 | `count-c2.py` | `c2-binding-digest` | binding | `if measured == sha:` | `if True:` | **survived** | 0 | — |
| 42 | `count-c2.py` | `c2-rev-ancestor` | rev-bound | `rev_ok = bool(fields["rev"]) and ancestor(repo, fields["rev"], rev)` | `rev_ok = bool(fields["rev"])` | **survived** | 0 | — |
| 43 | `count-c2.py` | `c2-limits-words` | limits | `and len(fields["limits"].split()) >= 3:` | `and len(fields["limits"].split()) >= 1:` | **survived** | 0 | — |
| 44 | `count-c2.py` | `c2-replay-count` | replay-count | `if replay_mode != "legacy" or fields["replay"] is not None:` | `if True:` | **survived** | 0 | — |
| 45 | `count-c2.py` | `c2-no-replay-words` | header-parse | `or len(fields["no_replay"].split()) < 3):` | `or len(fields["no_replay"].split()) < 4):` | **survived** | 0 | — |
| 46 | `count-c2.py` | `c2-no-replay-normalize` | header-parse | `    if fields["replay"] == "none":\n        fields["replay"] = None\n` | `    if False:\n        fields["replay"] = None\n` | **killed** | 1 | FAIL no_replay_reason [] |
| 47 | `count-c2.py` | `c2-dup-supersedes` | header-parse | `problems.append("duplicate-supersedes")` | `problems.append("duplicate-supersedes-x")` | **killed** | 1 | FAIL duplicate_supersedes dup |
| 48 | `count-c2.py` | `c2-sep-regex` | header-parse | `SEP = re.compile(r"^#\s*---\s*$")` | `SEP = re.compile(r"^#\s*--\s*$")` | **killed** | 1 | FAIL parse_replay []; FAIL body_trailing_newline rstrip |
| 49 | `count-c2.py` | `c2-replay-regex` | header-parse | `REPLAY = re.compile(r"^#\s*replay:\s*(required\|none\|clone)\s*$")` | `REPLAY = re.compile(r"^#\s*replay:\s*(required\|none)\s*$")` | **killed** | 1 | FAIL parse_supersedes []; FAIL clone_mode_parsed clone |
| 50 | `count-c2.py` | `c2-body-rstrip` | header-parse | `return lines[:cut], "\n".join(lines[cut + 1:]).rstrip("\n")` | `return lines[:cut], "\n".join(lines[cut + 1:]).rstrip(" ")` | **killed** | 1 | FAIL body_trailing_newline rstrip |
| 51 | `count-c2.py` | `c2-export-guard` | export-path | `if not token or token.startswith("-") or "/" not in token or not PATHISH.match(token):` | `if not token or token.startswith("-") or "/" not in token:` | **survived** | 0 | — |
| 52 | `count-c2.py` | `c2-drop-arm` | arm-deletion | `    cases.append(("subject_arms", SUBJECT_ARMS == 13\n                  and len(SUBJECT_LABELS) == 13, "13/13"))\n` | `` | **survived** | 0 | — |

Totals: **52 mutants, 0 unanchored, 25 killed, 27 survived** — `count-c1.py` 24 mutants (13 killed / 11 survived), `count-c2.py` 28 mutants (12 killed / 16 survived).

C2 second column over the pre-A1 blob at `98f48dba` (26 anchors exist there; `c2-subject-arms` and `c2-drop-arm` do not): **11 killed / 15 survived / 2 unanchored**. Every verdict agrees with the A1 copy; the amendment changes the subject gate's constants, not the selftest's coverage.

## Ranked survivors

Rank = exposure of the mutated clause to the frozen target string, then how completely the selftest is blind to it. The expected detector for every entry is the mutated copy's own `--selftest`; the expected verdict for a covered clause is `killed`. Every survivor is classified: **26 of 27 are proven non-equivalent by a witness, 1 is non-equivalent by inspection and not reachable from a selftest input, 0 are equivalent.**

**1. `c1-met-no-guard`** · `count-c1.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `met`'s refusal of an unanchored anchor (`and not any(...)`) is deleted outright.
*Witness W1:* a two-file mutant set: one killed anchor plus one anchor occurring twice, with both pristine arm counts matching → pristine `False`, mutated `True` (`DIFF`).
*Why the selftest misses it:* The conjunct the round's own M1 probe targets, in the r87 counter's copy of it. Every selftest population that reaches `met` has `total == 0`, where `total > 0` already forces `False`, so no arm can see the difference.

**2. `c1-met-drop-unanchored`** · `count-c1.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* same conjunct, `unanchored` dropped from the tuple (empty-mutation still refused).
*Witness W2:* same population (killed + unanchored) → pristine `False`, mutated `True` (`DIFF`).
*Why the selftest misses it:* Same masking: the only `unanchored` populations are `total == 0`.

**3. `c1-met-drop-empty`** · `count-c1.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* same conjunct, `empty-mutation` dropped from the tuple (unanchored still refused).
*Witness W3:* a two-file population: one killed anchor plus one anchor whose replacement equals it → pristine `False`, mutated `True` (`DIFF`).
*Why the selftest misses it:* The only `empty-mutation` population is `total == 0`; `empty_mutation_unmet` passes on the `total > 0` floor, not on the guard.

**4. `c2-replay-compare-off`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* the replay comparison is replaced by `if False:` — a replay whose output differs from the receipt body is accepted.
*Witness W15:* receipt body `RIGHT`, `# cmd: echo WRONG`, `# replay: required` → pristine `{'matched': 0, 'unexpected': 1}`, mutated `{'matched': 1, 'unexpected': 0}` (`DIFF`).
*Why the selftest misses it:* No selftest arm calls `replay_body`; the comparison has no arm at all. This is the one clause P-C2's do-nothing control says the supersede rule reads.

**5. `c2-replay-compare-rstrip`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* the `rstrip("\n")` on the replay output is dropped — every normal command output (with its trailing newline) mismatches its body.
*Witness W16:* receipt body `TOKEN`, `# cmd: echo TOKEN`, `# replay: required` → pristine `{'matched': 1, 'unexpected': 0}`, mutated `{'matched': 0, 'unexpected': 1}` (`DIFF`).
*Why the selftest misses it:* As 4, and the mutant is the dangerous direction: it reddens correct receipts.

**6. `c2-binding-digest`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `if measured == sha:` → `if True:` — every `# counter-sha256:` binding counts as bound whatever the blob bytes are.
*Witness W20:* `# counter-sha256: <64 zeros> notes/a.txt` at the fixture tip → pristine `{'bound': 0, 'unexpected': 1}`, mutated `{'bound': 1, 'unexpected': 0}` (`DIFF`).
*Why the selftest misses it:* No selftest arm binds a digest; `bound=9` in the frozen target is unexercised.

**7. `c2-supersede-call-clean`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* the supersede call site drops `clean and` — an unclean legacy receipt counts as superseded when a clean successor names it.
*Witness W12:* unclean legacy `L.txt` (body lacks the token) named by clean successor `S.txt` → pristine `{'legacy': 2, 'matched': 1, 'superseded': 0}`, mutated `{'legacy': 1, 'matched': 1, 'superseded': 1}` (`DIFF`).
*Why the selftest misses it:* `supersede_requires_clean` varies the successor's cleanliness only; the legacy row's `clean` flag is never varied. Witness flips `superseded 0 → 1`.

**8. `c2-supersede-counts-swap`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `counts["superseded"], counts["legacy"] =` assigns the pair in the wrong order.
*Witness W13:* two clean legacy receipts, one of them named by a clean successor → pristine `{'legacy': 2, 'superseded': 1}`, mutated `{'legacy': 1, 'superseded': 2}` (`DIFF`).
*Why the selftest misses it:* No arm reads the `counts` assignment; witness flips `(1,2) → (2,1)`.

**9. `c2-absent-accounting`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* a missing receipt is charged to `unexpected` instead of `absent`.
*Witness W17:* a two-row population with both receipts absent → pristine `{'absent': 2, 'unexpected': 0}`, mutated `{'absent': 0, 'unexpected': 2}` (`DIFF`).
*Why the selftest misses it:* `grade_population` is never called from the selftest (it needs a repo); the whole absent/unexpected accounting is unexercised.

**10. `c2-absent-ok`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* an absent non-reject receipt no longer clears `ok`.
*Witness W17b:* a two-row population with both receipts absent → pristine `False`, mutated `True` (`DIFF`).
*Why the selftest misses it:* Same; `ok` stays `True` for a population whose receipts are all missing.

**11. `c2-defeated-accounting`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* a defeated reject receipt is counted `matched` instead of `defeated`.
*Witness W18:* one present reject receipt with no `# rev:` line → pristine `{'defeated': 1, 'matched': 0}`, mutated `{'defeated': 0, 'matched': 1}` (`DIFF`).
*Why the selftest misses it:* Same; `defeated` is never exercised by the selftest.

**12. `c2-supersede-absent-target`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* the post-loop check that a `# supersedes:` target is inside the population is deleted.
*Witness W14:* successor naming `GONE.txt`, which is not in the population → pristine `{'legacy': 1, 'superseded': 0, 'unexpected': 1}`, mutated `{'legacy': 1, 'superseded': 0, 'unexpected': 0}` (`DIFF`).
*Why the selftest misses it:* Same; also `ok` stays `True` under the mutant (witness W14b).

**13. `c2-summary-token`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `if token in body:` → `if True:` — the body summary token is no longer required.
*Witness W19:* receipt at the fixture tip whose body lacks the required token → pristine `{'matched': 0, 'unexpected': 1}`, mutated `{'matched': 1, 'unexpected': 0}` (`DIFF`).
*Why the selftest misses it:* Same; a receipt without the summary token is counted `matched`.

**14. `c2-rev-ancestor`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `rev_ok` drops the ancestry test — any 40-hex `# rev:` is accepted.
*Witness W21:* `# rev: bbb…` (not present in the fixture repo) → pristine `{'revs': 0, 'unexpected': 1}`, mutated `{'revs': 1, 'unexpected': 0}` (`DIFF`).
*Why the selftest misses it:* Same; `revs` counts any syntactically valid 40-hex rev.

**15. `c2-replay-count`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `replay=` counts every row instead of only rows with a `# replay:` line (or a non-legacy mode).
*Witness W23:* a legacy receipt with no `# replay:` line → pristine `{'replay': 0}`, mutated `{'replay': 1}` (`DIFF`).
*Why the selftest misses it:* Same; `replay` is a target field and no arm reads it.

**16. `c2-limits-words`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* the `# limits:` gate relaxes from ≥3 words to ≥1.
*Witness W22:* `# limits: limit` (one word) → pristine `{'limits': 0}`, mutated `{'limits': 1}` (`DIFF`).
*Why the selftest misses it:* Same; a one-word limits field enters the `limits` count.

**17. `c1-killed-n`** · `count-c1.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `killed_n = total - survivors` → `killed_n = total` — the tail reports survivors as also killed.
*Witness W5:* a two-file population with one killed and one surviving mutant → pristine `'mutants=2 killed=1 survivors=1 total=2 arms=2'`, mutated `'mutants=2 killed=2 survivors=1 total=2 arms=2'` (`DIFF`).
*Why the selftest misses it:* The target's `killed=` is computed from `survivors`; only single-mutant fixtures are tested (where `total - survivors == total`).

**18. `c1-arms-total`** · `count-c1.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `arms_total += max(passed, 0)` → `arms_total += 1` — the tail `arms=` stops being the subject tally.
*Witness W6:* a subject whose own selftest prints `pass=18 fail=0` → pristine `'mutants=1 killed=1 survivors=0 total=1 arms=18'`, mutated `'mutants=1 killed=1 survivors=0 total=1 arms=1'` (`DIFF`).
*Why the selftest misses it:* Only pass=1 subjects are used, so `+= 1` and `+= passed` coincide; the target's `arms=54` is a `+= passed` sum.

**19. `c1-split-field`** · `count-c1.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `target_split` compares `mutants` where it means `killed`.
*Witness W8:* tail `mutants=6 killed=5 survivors=0 total=6 arms=54` → pristine `False`, mutated `True` (`DIFF`).
*Why the selftest misses it:* Every fixture has `mutants == killed`, so the two fields are interchangeable there.

**20. `c1-anchor-guard`** · `count-c1.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `if base.count(old) != 1:` → `== 0:` — a repeated anchor is graded instead of excluded.
*Witnesses W9a/W9b:* a two-occurrence anchor (`GUARD = 1` twice) → the arm predicate `(not met) and "unanchored" in " ".join(extras)` is `True` in both, while the mix moves from `mutants=0 total=0` (anchor excluded, `unanchored …`) to `mutants=1 survivors=1 total=1` (anchor graded, `survivor …`).
*Why the selftest misses it:* The arms `unanchored_excluded` / `unanchored_plus_killed_unmet` test `"unanchored" in " ".join(extras)`, and a survivor line reads `survivor … M1-unanchored-conjunct` — the label itself contains `unanchored`. The assertion is satisfied by the mutant's label, so it passes under the mutation (witness W9a is identical `True`/`True`; W9b shows the real divergence).

**21. `c1-arms-first`** · `count-c1.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `arms_of` keeps the first `COUNTER_SELFTEST` line instead of the last.
*Witness W7:* `…pass=1…\n…pass=18…` in one output → pristine `[18, 0]`, mutated `[1, 0]` (`DIFF`).
*Why the selftest misses it:* No subject in the selftest prints two tally lines.

**22. `c1-mutant-spec-c2`** · `count-c1.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* the M2 probe's replacement is edited in the `MUTANTS` table; nothing pins the six anchors to the frozen clause each names.
*Witness W10:* `MUTANTS[1][3]` in the loaded module → pristine `'met = (pristine_ok and total >= 0'`, mutated `'met = (False or total >= 0'` (`DIFF`).
*Why the selftest misses it:* `marker_literal` only checks one label string; `labels_unique` only checks uniqueness. The witness shows the tampered replacement produces a different subject byte-stream (`fail=1` vs `fail=2` on the r86 count-c1.py), so the counter would grade a different defect under the same label. Both variants are still killed there, so this tamper does not move P-C1's kill count by itself.

**23. `c2-no-replay-words`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* the `# no-replay:` reason gate relaxes from <3 words to <4.
*Witness W24:* `# no-replay: one two three` → pristine `[]`, mutated `['missing-no-replay']` (`DIFF`).
*Why the selftest misses it:* The only no-replay fixture has 5 words, which both thresholds accept.

**24. `c2-export-guard`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `export_rev` drops the `PATHISH` filter, so tokens the command names are exported even when they are not shaped like repo paths.
*Witness W25:* `export_rev` on `notes/a~.txt` → pristine `[]`, mutated `['notes/a~.txt']` (`DIFF`).
*Why the selftest misses it:* `export_rev` is never called from the selftest.

**25. `c1-drop-arm`** · `count-c1.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* one selftest arm (`labels_unique`) is deleted; the counter still prints `fail=0`.
*Matrix output:* the counter's own `--selftest` (18 → 17 arms) → `C1_COUNTER_SELFTEST pass=17 fail=0`, rc=0 (pristine `pass=18 fail=0`); `own_ok` still green.
*Why the selftest misses it:* `own_ok` accepts any `pass=<n> fail=0`, and the arm count is not asserted anywhere in either counter's own selftest (`subject_arms` pins only the r86 subject's 13).

**26. `c2-drop-arm`** · `count-c2.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* one selftest arm (`subject_arms`) is deleted; the counter still prints `fail=0`.
*Matrix output:* the counter's own `--selftest` (17 → 16 arms) → `C2_COUNTER_SELFTEST pass=16 fail=0`, rc=0 (pristine `pass=17 fail=0`); `own_ok` still green.
*Why the selftest misses it:* Same hole on the C2 side: the C2 counter has no analogue of the subject's `subject_arms` self-pin, so its own 17 arms are not asserted by its own selftest.

**27. `c1-own-ok`** · `count-c1.py` · verdict `survived` (rc=0) · non-equivalent

*Clause mutated:* `own_ok` becomes `(True or …)`, so `main()`'s detector-red branch is unreachable.
*No behavioural witness:* inspection only — no selftest input reaches `main()`.
*Why the selftest misses it:* The mutated statement is `own_ok = (True or "C1_COUNTER_SELFTEST" in own_out`; no input to `--selftest` reaches that line.

## What the matrix says

1. **The clause this round grades in the subject is uncovered in the counter.** `met`'s unanchored/empty guard (ranks 1–3) is the same conjunct the frozen M1 probe mutates in `.ufo/waves/round-86/count-c1.py`. In the r87 counter's own selftest every population that reaches `met` has `total == 0`, where `total > 0` already forces `False`; the guard is therefore never load-bearing in any arm. A witness with one killed mutant plus one unanchored anchor flips `met` from `False` to `True` for all three mutants.
2. **The whole C2 population machine is outside the selftest.** No arm calls `grade_population` or `replay_body` (they need a repo). Every target field whose computation lives in `grade_population` — `absent`, `unexpected`, `defeated`, `summary`, `bound`, `revs`, `limits`, `replay`, `matched`, `superseded`/`legacy` — survived mutation, as did the replay comparison the supersede rule reads. (`receipts`, `bindings` and `cmd` were not mutated; `bound` was.) The selftest covers only header parsing, `supersede_verdict`/`supersede_counts` in isolation, the population shape, the target string, `header_and_body`, and the subject gate.
3. **Three selftest assertions are satisfied for the wrong reason.** (a) `unanchored_excluded`/`unanchored_plus_killed_unmet` search for the substring `unanchored`, which also occurs in the mutant label `M1-unanchored-conjunct`; a `survivor … M1-unanchored-conjunct` line satisfies the same test that is meant to detect a repeated anchor (rank 20). (b) `unanchored_plus_killed_unmet` is vacuous outright: its fixture `zero.py` contains exactly one `GUARD = 1`, so nothing in it is unanchored; measured on the pristine module, `met=False` comes from `pristine-arms` plus the survivor, and the only `unanchored` substring is the label in `extras=['pristine-arms tools/zero.py arms=-1 want=1', 'survivor tools/zero.py M1-unanchored-conjunct']`. That arm cannot exercise the branch it names, under any implementation. (c) `empty_mutation_unmet` and `zero_mutants_unmet` pass on the `total > 0` floor rather than on the guard they name. Either way the arm is green while the clause is gone.
4. **Aggregate accounting is pinned only where it coincides.** `killed = total - survivors` (rank 17) and `arms_total += passed` (rank 18) are only exercised on single-mutant / `pass=1` fixtures, where the constants are indistinguishable. Both feed the frozen C1 target (`killed=`, `arms=54`).
5. **Neither counter bounds its own arm count.** Deleting an arm leaves `fail=0` and `rc=0`; `own_ok` only regex-matches `pass=<n> fail=0`. The r86 subject gate pins `SUBJECT_ARMS = 13`, but nothing pins 18 (C1) or 17 (C2). This is the same class of hole the A1 amendment fixed on the subject side.
6. **The six probe anchors are mutable data.** Nothing checks that each `MUTANTS` entry names the frozen clause; rank 22 edits M2's replacement and the selftest stays green. On the real r86 subject both variants are killed (fail=1 vs fail=2), so this particular tamper does not move P-C1's `killed=6`, but the counter is not evidence that the six probes are the frozen six.

## Scope limits (not run, not claimed)

* Only `--selftest` was graded, as the seat specifies. I did not run either counter against the after revision, and I make no claim about the after value; that is the executors' seat.
* Not mutated: `main()` argv/scratch/git plumbing (`ancestor`, `sha256_at`, `replay_body` clone/checkout mechanics beyond the comparison), the `--repo` default, and the self-check harness itself. The `absent`/`unexpected` rows above are reached through `grade_population` with a stub loader, not through `main()`.
* Where a survivor would also move at the after revision I say so only as inference; e.g. `c1-arms-total` (54 vs 3) and `c2-replay-compare-rstrip` (every replay reddens) would move the frozen target, while `c1-killed-n`, `c1-split-field`, `c1-anchor-guard`, ranks 1–3, 6, 9, 10, 12–16, 20, 21 and the arm deletions would leave the after tail byte-identical. [INFERENCE] — not measured by this seat.
* No tools were installed or upgraded (python3 3.14.8 and git as found; no pacman transaction, no `uv tool`).
* Scratch `/fast/scratch/hyaku/mori-r87/Mo87M01Mut/` was removed after the report was written; harness, `matrix.json`, `witness.json` and the fixture repo lived only there.

