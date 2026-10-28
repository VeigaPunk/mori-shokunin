# Mo60SimplifierA2 — dead-weight + verdict-gap audit of count-c1.py / count-c3.py

**Status: proposals only.** No lane file, corpus registry, SCORECARD, LOG or VCS was
touched; no fleet/sibling writes. Everything below is either a read of the lane or a
scratch-copy experiment under `/fast/scratch/hyaku/mori-r60/Mo60SimplifierA2/`.

## 0. Pins used (every re-derivation named)

| object | sha256 | where verified |
|---|---|---|
| `.ufo/waves/round-60/count-c1.py` | `795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae` | `ac496c7…`, `b3c2561…`, working tree — **all three identical** |
| `.ufo/waves/round-60/count-c3.py` | `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514` | `ac496c7…`, `b3c2561…`, working tree — **all three identical** |

```
$ for f in count-c1.py count-c3.py; do git show ac496c7…:$f | sha256sum; \
    git show b3c2561…:$f | sha256sum; sha256sum $f; done
→ each file: three identical hashes
```

Revisions referenced: amended freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`,
entering `ddfb12fb0838b4307c445194a844f0c4b1950195`, tip observed at audit time
`b3c256138f00c704d5aa56eb0332d74506502ef2`. c2 was not audited (other seats); it is
byte-pinned here only where c3 reads it (`PIN_C2 = 8c4814f5…df976`, matched).

Tools: pyflakes 4.0.3, ruff 0.17.2, vulture 2.16, Python 3.14.8. No installs performed.

## 1. Unused variables / imports — exact list (2, both imports)

```
$ pyflakes count-c1.py count-c3.py
count-c1.py:34:1: 'hashlib' imported but unused
count-c3.py:43:1: 'json' imported but unused
$ vulture --min-confidence 60 count-c1.py
count-c1.py:34: unused import 'hashlib' (90% confidence)
$ vulture --min-confidence 60 count-c3.py
count-c3.py:43: unused import 'json' (90% confidence)
```

`ruff check --select F,ARG,B,PIE,RET,SIM` agrees (F401 ×2) and adds `B905`
`count-c1.py:90` (`zip()` without `strict=`).

A bespoke AST pass (assigned-but-never-loaded locals, unused params, module-level
never-read names) found **nothing beyond those two imports**. Its only other hits were
`chk()`'s `passed`/`failed`, which are `nonlocal` names updated by `AugAssign` — a
scanner artifact, **checked and rejected**, not findings.

## 2. The selftest `good_row` reuse in count-c1.py (lines 263–269)

```python
263  good_row = ("| Mo59Critic29 | present | present | wrong-supersedED "
264              "| p |\n")
265  bad = parse_absent_table(good_row.replace("wrong-superseded",
266                                            "wrong-supersedED"))
267  chk("table_shape", bad is None)
268  good_row = "| Mo59Critic29 | present | present | wrong-superseded | p |"
269  t = parse_absent_table(good_row)
```

Three separate defects in one block:

1. **The name is wrong for its first binding.** Line 263 binds a *bad* row (disposition
   cell `wrong-supersedED`), then line 268 rebinds the same name to a genuinely good row.
2. **The `.replace()` is dead computation — a no-op.** The literal already contains
   `wrong-supersedED`, the replacement text; the searched-for string `wrong-superseded`
   never occurs.

```
$ python3 -c 'first = "| Mo59Critic29 | present | present | wrong-supersedED | p |\n"; \
  print("wrong-superseded" in first); \
  print(first.replace("wrong-superseded","wrong-supersedED") == first)'
False
True
```

3. **Consequence:** `parse_absent_table` returns `None` both with and without the
   `.replace`, so the assertion still passes — but it would pass identically if the
   `.replace` were deleted. The assertion itself is worth keeping (it is the only check
   that an out-of-vocabulary disposition cell is rejected), so the fix is a rename plus
   deletion of the no-op, not deletion of the test.

## 3. Redundant predicate in `parse_absent_table` (count-c1.py:110)

```python
110  if cells[0] in ("name",) or cells[0].startswith("Mo") is False:
```

`"name".startswith("Mo")` is `False`, so the right-hand conjunct already `continue`s;
the left-hand membership test can never change the outcome. ruff reports it verbatim as
`FURB171 Membership test against single-item container`. Collapsing to
`if not cells[0].startswith("Mo"):` is provably behaviour-identical — confirmed on the
real table (see §6, `absent-set=5/5` unchanged).

## 4. Verdict gaps — the `failed` list is not the verdict (highest severity)

Both counters compute checks into `failed` and then **suppress** them, because `met`
does not reference them and `failed=` is only printed when `met` is False. Any check not
in `met` is therefore unenforceable *and* invisible.

### 4a. count-c1.py — real-pointer existence is orphaned

Predicate P-C1(a) requires "both real files … exist at R"; the counter checks it but the
verdict ignores it:

```
160        for rp in REAL_POINTERS:            ← check, appends pointer_absent:…
161            if not exists(repo, rev, rp):
162                failed.append("pointer_absent:%s" % rp)
…
234    met = (dead == 0 and corr and got == len(R59_COUNTERS)   ← pointer_ok absent
235           and rows_ok == len(NAMES) and lesson == "ok")
```

**Empirical proof.** Scratch clone at tip, one tracked pointer file deleted, committed
(`509cb569…`; `cat-file -e` → rc 128):

```
$ python3 .ufo/waves/round-60/count-c1.py 509cb569… --repo <clone> --scratch <scratch>
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=509cb569…
exit=0
```

`C1=met` at a revision that violates P-C1(a). All other c1 append-tokens are covered by
`met` (`dead`, `corr`, `got`, `rows_ok`, `lesson`) — `pointer_absent` is the only orphan.

### 4b. count-c3.py — the mandated c1 pin is orphaned

`contract.md:122–123` says "count-c3 pins count-c1 (sha `795c1f31…ddbae`)" — so the pin
is contract-required, not optional. But:

```
145    c1_b = git_show(repo, rev, C1_REL)
147    if c1_b is None:  failed.append("count_c1_absent")
149    elif sha256(c1_b) != PIN_C1:  failed.append("count_c1_sha")
…
255    met = (c2_ok and toolgate and old_hole and containment and expectgate)
                                                             ↑ no c1_ok
```

**Empirical proof.** Scratch clone, one comment line appended to `count-c1.py`, committed
(`2d6cbe82…`; c1 sha becomes `9849ef3d…`, c2 still `8c4814f5…`), then the **frozen** c3
(materialized from `ac496c7`) run against it:

```
$ python3 c3-frozen.py 2d6cbe82… --repo <clone> --scratch <scratch>
C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=2d6cbe82…
exit=0
```

`C3=met` with a drifted c1, and no `failed=` suffix at all: the `count_c1_sha` failure is
computed, recorded, then thrown away by the `if not met:` print guard. (`r59_counter_absent`
is the only other append-token outside `met`, and it is covered transitively via
`g1_old_skipped → old_hole`.)

## 5. Three dead gate words in count-c3.py (lines 298–307)

```python
300  "ok" if "toolgate"    not in failed and "g1_new_skipped" not in failed else "bad",
302  "ok" if "containment" not in failed and "g2_skipped"    not in failed else "bad",
304  "ok" if "expectgate"  not in failed and "g3_skipped"    not in failed else "bad",
```

The first conjunct of each is **vacuously true**: no `failed.append` ever emits those
three tokens. Enumerating every literal handed to `failed.append` (19 sites, AST walk):

```
line 143 'count_c2_absent'      line 183 'g1_new_skipped'
line 145 'count_c2_sha'         line 198 'g1_old_control_did_not_reproduce'
line 148 'count_c1_absent'      line 200 'g1_old_skipped'
line 150 'count_c1_sha'         line 222 'g2_parent_escape'
line 153 'r59_counter_absent'   line 224 'g2_inside_rejected'
line 160 'poc:%s'               line 226 'g2_symlink_escape'
line 178 'g1_new_no_tool_sha'   line 228 'g2_escape_written'
line 180 'g1_new_executed:%s'   line 230 'g2_skipped'
                                line 239 'poc2:%s'
                                line 251 'g3_no_tamper_flag'
                                line 253 'g3_skipped'

probe 'toolgate'     exact-match tokens appended: NONE -> conjunct always True
probe 'containment'  exact-match tokens appended: NONE -> conjunct always True
probe 'expectgate'   exact-match tokens appended: NONE -> conjunct always True
```

So the word reduces to `"bad"` only for `*_skipped`, which is appended **only in the
`else` of `if c2_ok:`**. Therefore: **whenever the c2 pins match, all three gate words
print `ok` unconditionally — including on the exact failure each gate exists to catch.**
Evaluating the frozen source's own `line = (…)` expression with the tokens the frozen
code actually emits:

```
failed=['g3_no_tamper_flag']            -> C3=unmet toolgate=ok containment=ok expectgate=ok …
failed=['g2_parent_escape']             -> C3=unmet toolgate=ok containment=ok expectgate=ok …
failed=['g1_new_no_tool_sha']           -> C3=unmet toolgate=ok containment=ok expectgate=ok …
failed=['g1_new_executed:/x/EXEC-MARKER']-> C3=unmet toolgate=ok containment=ok expectgate=ok …
failed=['g3_skipped']                   -> C3=unmet toolgate=ok containment=ok expectgate=bad …
```

The word is a second, divergent source of truth for a gate whose authoritative value is
already the `toolgate`/`containment`/`expectgate` boolean feeding `met`. Deleting the
probes and printing from the booleans removes 6 expressions and one whole class of
misreport.

Reachability note (honesty): the divergence is latent under the *current* pinned c2 —
`count-c2.py` pin-gates both `mori-entry-claims-check.py` (`tool_sha`/`tool_absent`) and
`mori-settlement-scan.py` (`scan_tool_sha`/`scan_tool_absent`), so no marker is produced
today. The dead conjuncts are dead by construction regardless, and the misreport becomes
live the moment any gate's own failure token fires.

## 6. Proposal set and validation

Two scratch copies were produced (`c1-new.py` sha `70b275ba…`, `c3-new.py` sha
`f56824d5…`) and validated. **Nothing was written to the lane.**

| id | file | change | kind |
|---|---|---|---|
| P1 | c1 | delete `import hashlib` (34) | dead weight |
| P2 | c1 | `zip(..., strict=True)` (90) | dead weight |
| P3 | c1 | collapse redundant header test (110) | dead weight |
| P4 | c1 | `good_row` → `bad_row`, delete no-op `.replace` (263–267) | dead weight |
| P5 | c1 | add `pointer_ok` to `met` (149–163, 234) | **verdict fix (P-C1a)** |
| P6 | c3 | delete `import json` (43) | dead weight |
| P7 | c3 | carry `g1/g2/g3` booleans in `d`, print from them (255–258, 300–305) | dead weight + honesty |
| P8 | c3 | add `c1_ok` to `met` (146–150, 255) | **verdict fix (contract 122–123)** |
| P9 | c3 | replace tautological `frozen_tamper_rel` check (272–273) | dead weight, count-preserving |

P9 note: `TAMPER_REL.endswith("h02-malformed-claim/expect.txt")` asserts a constant ends
with a substring that is literally its own suffix — it cannot fail. It cannot simply be
deleted because `contract.md` freezes `C3_SELFTEST pass=3 fail=0`; the replacement asserts
a real G1 precondition instead (the decoy prints the selftest lines the PoC relies on) and
keeps `pass=3`.

### Behaviour retention (real tree, tip `b3c2561…`)

```
C1 frozen    : C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c2561…
C1 proposed  : C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c2561…
C3 frozen    : C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=b3c2561…
C3 proposed  : C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=b3c2561…
```

Selftests unchanged and lint clean on the proposals:

```
C1_SELFTEST pass=6 fail=0        (frozen: pass=6 fail=0)
C3_SELFTEST pass=3 fail=0        (frozen: pass=3 fail=0)
pyflakes: exit 0 · ruff --select F,ARG,B,PIE,RET,SIM,FURB: "All checks passed!"
```

Baseline for the frozen c3 at the freeze revision reproduces the recorded evidence:
`C3=met … cases=6 rev=ac496c7cde8cad965079858accae3bedfe4a73f2`, exit 0 (matches
`evidence/c3-at-freeze.txt`), and `count-c3.py --selftest`-independent baseline C1 at tip
reproduces `evidence/c1-at-data.txt` shape (`C1=met … receipts=2/2 absent-set=5/5`).

### The fixes close the gaps (mutants, scratch clone only)

```
C1 @ REV2 509cb569… (real pointer deleted)
  frozen   : C1=met   … exit=0
  proposed : C1=unmet … failed=pointer_absent:.ufo/waves/round-59/evidence/control-c1-do-nothing.txt  exit=1

C3 @ REV  2d6cbe82… (count-c1 bytes drifted)
  frozen   : C3=met   … exit=0
  proposed : C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 … failed=count_c1_sha  exit=1
```

Gate-word precision under the proposal (one gate failing at a time):

```
failed=['g1_new_no_tool_sha']  -> C3=unmet toolgate=bad containment=ok  expectgate=ok  …
failed=['g2_parent_escape']    -> C3=unmet toolgate=ok  containment=bad expectgate=ok  …
failed=['g3_no_tamper_flag']   -> C3=unmet toolgate=ok  containment=ok  expectgate=bad …
```

### Diff (condensed; full unified diff reproduced from the scratch copies)

```diff
--- count-c1.py
-import hashlib
-    for name, real in zip(DEAD_NAMES, REAL_POINTERS):
+    for name, real in zip(DEAD_NAMES, REAL_POINTERS, strict=True):
-        if cells[0] in ("name",) or cells[0].startswith("Mo") is False:
+        if not cells[0].startswith("Mo"):
+        pointer_ok = False                    # sc_b is None branch
-        for rp in REAL_POINTERS:
-            if not exists(repo, rev, rp):
-                failed.append("pointer_absent:%s" % rp)
+        missing = [rp for rp in REAL_POINTERS if not exists(repo, rev, rp)]
+        for rp in missing:
+            failed.append("pointer_absent:%s" % rp)
+        pointer_ok = not missing
-    met = (dead == 0 and corr and got == len(R59_COUNTERS)
+    met = (dead == 0 and corr and pointer_ok and got == len(R59_COUNTERS)
-    good_row = ("| Mo59Critic29 | present | present | wrong-supersedED " "| p |\n")
-    bad = parse_absent_table(good_row.replace("wrong-superseded", "wrong-supersedED"))
-    chk("table_shape", bad is None)
+    bad_row = ("| Mo59Critic29 | present | present | wrong-supersedED " "| p |\n")
+    chk("table_shape", parse_absent_table(bad_row) is None)

--- count-c3.py
-import json
+    c1_ok = c1_b is not None and sha256(c1_b) == PIN_C1
-    elif sha256(c1_b) != PIN_C1:
+    elif not c1_ok:
-        return False, sorted(set(failed)), {"cases": cases}
+        return False, sorted(set(failed)), {"cases": cases, "g1": False, "g2": False, "g3": False}
-    met = (c2_ok and toolgate and old_hole and containment and expectgate)
-    return met, sorted(set(failed)), {"cases": cases}
+    met = (c2_ok and c1_ok and toolgate and old_hole and containment and expectgate)
+    return met, sorted(set(failed)), {"cases": cases, "g1": toolgate,
+                                      "g2": containment, "g3": expectgate}
-    chk("frozen_tamper_rel", TAMPER_REL.endswith("h02-malformed-claim/expect.txt"))
+    chk("evil_blob_mimicry", "ENTRYCLAIMS_SELFTEST" in EVIL_BLOB
+        and "SETSCAN_SELFTEST" in EVIL_BLOB)
-               "ok" if "toolgate" not in failed and "g1_new_skipped" not in failed else "bad",
-               "ok" if "containment" not in failed and "g2_skipped" not in failed else "bad",
-               "ok" if "expectgate" not in failed and "g3_skipped" not in failed else "bad",
+               "ok" if d["g1"] else "bad",
+               "ok" if d["g2"] else "bad",
+               "ok" if d["g3"] else "bad",
```

Net: c1 11714 → 11670 bytes (−44); c3 11471 → 11473 bytes (+2). c3's byte count is
nearly flat because the six removed status-probe expressions are replaced by one dict
carrying the same three values that already feed `met`.

## 7. Tradeoffs and what I deliberately did not do

- **These are proposes, not edits.** Both files are frozen at `ac496c7` and already
  measure met; P5/P8 change verdict semantics, so they need a recorded amendment. Note the
  coupling: editing `count-c1.py` changes its sha and therefore `PIN_C1` **inside**
  `count-c3.py`, which changes c3's bytes too — so any amendment must re-freeze both
  together, and c3's own pin is what makes the coupling load-bearing.
- **P5/P8 are predicate conformance, not scope widening.** Both checks already exist in
  the source and are already mandated (P-C1(a); contract §122–123). The proposal only
  routes existing results into the verdict; it adds no new check.
- **No axis harmed on the real tree:** identical output lines, identical selftest counts,
  exit codes unchanged (0/0). The only behavioural difference is on trees that already
  violate a frozen predicate, where the counter now says `unmet` instead of `met`.
- **Not proposed (out of dead-weight scope):** the shared argv loop
  (`while i < len(argv): … argv[i+1]`) raises `IndexError` on a trailing `--repo`/`--scratch`
  in c1 and c3 rather than the documented exit 2 — a real but low-value robustness gap, and
  changing it would alter the usage contract, so I left it for a reviewer to decide.
- **Not touched:** `count-c2.py`, the contract, evidence files, `trees-c2h`, SCORECARD,
  LOG, corpus. `git status --porcelain -- .ufo/waves/round-60` shows only pre-existing
  untracked wave artifacts (`w1/`, `w1.ready*`, `evidence/c1-at-data.txt`), none of them
  mine except this report.

## 8. Scratch hygiene

All work under `/fast/scratch/hyaku/mori-r60/Mo60SimplifierA2/` with `TMPDIR` set there
and `--scratch` passed to every counter run. The only git writes were in
`mutant.KHxFBW/lane` (a `--no-hardlinks` clone; `rev-parse --show-toplevel` asserted to
equal the clone path before each commit, fixture identity per commit). The lane repo
received no writes; both counters re-hashed identical at the end of the audit. Scratch
tree removed before yield; the receipts above are inline in this report.
