# QUALITY-154 — predicate-identity audit of the round-60 frozen target tokens

Seat: Mo60Reviewer13 (leaf, read-only). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze revision audited: `ac496c7cde8cad965079858accae3bedfe4a73f2`; entering
`ddfb12fb0838b4307c445194a844f0c4b1950195`; tip observed during the audit
`b3c256138f00c704d5aa56eb0332d74506502ef2`. Contract read in full from
`.ufo/waves/round-60/contract.md`.

Question asked: **do the contract's frozen target tokens for C1/C2/C3 each come out of the
corresponding counter's own print line, and is the printed token the measured predicate?**

Answer in one line: **every target token name is printed by its counter (no missing token),
but C3's three gate tokens are not identity-bound to their gates, C3's `met` silently drops
the count-c1 pin, and C2's `claims=/files=` target values are not entailed by P-C2.**

Counter bytes at the freeze revision equal the working-tree bytes (kill-rule precondition,
verified), so all line pointers below are simultaneously freeze-rev and worktree lines.

```
$ git show ac496c7c:.ufo/waves/round-60/count-c1.py | sha256sum
795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae
$ git show ac496c7c:.ufo/waves/round-60/count-c2.py | sha256sum
8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976
$ git show ac496c7c:.ufo/waves/round-60/count-c3.py | sha256sum
fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514
$ sha256sum .ufo/waves/round-60/count-{c1,c2,c3}.py     # identical, worktree
```

---

## 1. Token inventory (presence check) — PASS, nothing is unprintable

Target token names were extracted mechanically from the three `Frozen target output (after)`
literals in the contract and compared with the `NAME=%` format items in each counter's
`main()` print expression.

| claim | contract target tokens | tokens printed by the print line | line |
|---|---|---|---|
| C1 | C1, dead-uncorrected, receipts, absent-set, lesson, rev | C1, dead-uncorrected, receipts, absent-set, lesson, rev | `count-c1.py:296-301` |
| C2 | C2, selftest, scan, drift, trees, entry, rows, pins, tree, claims, files, spans, rev | C2, selftest, scan, drift, trees, entry, rows, pins, tree, claims, files, spans, rev | `count-c2.py:475-483` |
| C3 | C3, toolgate, containment, expectgate, cases, rev | C3, toolgate, containment, expectgate, cases, rev | `count-c3.py:298-307` |

Exact set equality in all three cases; no extra tokens, no missing tokens. **Named
unprintable token: none.**

End-to-end reproduction of each target from unmodified bytes at a pinned revision:

```
$ TMPDIR=<scratch> python3 .ufo/waves/round-60/count-c1.py b3c25613... --repo "$PWD" --scratch <scratch>/c1tip
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c256138f00c704d5aa56eb0332d74506502ef2
EXIT=0
$ TMPDIR=<scratch> python3 .ufo/waves/round-60/count-c2.py ac496c7c... --repo "$PWD" --scratch <scratch>/c2
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=ac496c7cde8cad965079858accae3bedfe4a73f2
EXIT=0
$ TMPDIR=<scratch> python3 .ufo/waves/round-60/count-c2.py b3c25613... --repo "$PWD" --scratch <scratch>/c2tip
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=b3c256138f00c704d5aa56eb0332d74506502ef2
EXIT=0
$ TMPDIR=<scratch> python3 .ufo/waves/round-60/count-c3.py ac496c7c... --repo "$PWD" --scratch <scratch>/c3
C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7cde8cad965079858accae3bedfe4a73f2
EXIT=0
$ TMPDIR=<scratch> python3 .ufo/waves/round-60/count-c1.py ac496c7c... --repo "$PWD" --scratch <scratch>/c1
C1=unmet dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent rev=ac496c7cde8cad965079858accae3bedfe4a73f2 failed=absent_set=0/5,absent_table_absent,correction_incomplete,dead=2,lesson_absent,receipt_absent:.ufo/waves/round-60/evidence/r59-c1-met.txt,receipt_absent:.ufo/waves/round-60/evidence/r59-c2-met.txt,receipts=0/2
EXIT=1
```

(the last line is the C1 pre-data state at the freeze rev, matching
`evidence/control-c1-do-nothing.txt` on every token except `rev=`; the C1 data landed at
`398d3225`, which is why the tip run above is met.)

So the target **strings** are all reachable. The defects below are in token **identity**,
not token presence.

---

## 2. Findings

### F1 (HIGH) — C3's `toolgate=`, `containment=`, `expectgate=` tokens are not the measured gates

`count-c3.py:298-307` computes each gate token from membership of a literal in `failed`:

```python
"ok" if "toolgate" not in failed and "g1_new_skipped" not in failed else "bad",
"ok" if "containment" not in failed and "g2_skipped" not in failed else "bad",
"ok" if "expectgate" not in failed and "g3_skipped" not in failed else "bad",
```

The measured values are the local booleans `toolgate`, `containment`, `expectgate`
(`count-c3.py:163-183`, `203-230`, `233-252`). The strings `"toolgate"`, `"containment"`,
`"expectgate"` **never enter `failed`**: the complete append set is

```
$ grep -n 'failed.append' .ufo/waves/round-60/count-c3.py
143 count_c2_absent   145 count_c2_sha   148 count_c1_absent   150 count_c1_sha
153 r59_counter_absent  160 poc:%s  178 g1_new_no_tool_sha  180 g1_new_executed:%s
183 g1_new_skipped   198 g1_old_control_did_not_reproduce   200 g1_old_skipped
222 g2_parent_escape  224 g2_inside_rejected  226 g2_symlink_escape
228 g2_escape_written  230 g2_skipped  239 poc2:%s  251 g3_no_tamper_flag  253 g3_skipped
```

Consequently the first conjunct of each test is permanently true and the tokens degrade to
"gate was not skipped". Each gate's own failure literal still prints `ok`:

```
$ python3 -c '<eval of the verbatim print expressions>'
['g1_new_executed:/x/EXEC-MARKER'] -> ('ok', 'ok', 'ok')
['g2_escape_written']              -> ('ok', 'ok', 'ok')
['g3_no_tamper_flag']              -> ('ok', 'ok', 'ok')
['g2_skipped']                     -> ('ok', 'bad', 'ok')
```

Reachability with **unmodified frozen bytes and the pinned module** (no doctoring): the G2
arm's write-attribution test `not (g2.parent / "escape.txt").exists()` (`count-c3.py:218`)
reads the scratch root, so a pre-existing scratch file flips the `containment` variable to
False while nothing escaped. Pre-seeding `<scratch>/escape.txt` (13 bytes) and running the
frozen counter at the freeze rev:

```
$ mkdir -p <scratch>/c3env && printf 'pre-existing\n' > <scratch>/c3env/escape.txt
$ TMPDIR=<scratch>/c3env python3 .ufo/waves/round-60/count-c3.py ac496c7c... --repo "$PWD" --scratch <scratch>/c3env
C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7cde8cad965079858accae3bedfe4a73f2 failed=g2_escape_written
EXIT=1
```

The line contradicts itself: `containment=ok` next to `failed=g2_escape_written`, with
`met = ... and containment and ...` (`count-c3.py:255`) evaluating False. The frozen target
`containment=ok` is therefore printable while the containment arm is failing. The analogous
`toolgate`/`expectgate` lie is latent at R (their failure paths need the pinned count-c2 to
misbehave) but structurally identical, and `g1_new_no_tool_sha` / `g1_new_executed:` /
`g3_no_tamper_flag` are appended by exactly the code paths that should force `bad`.

Fix direction (for the L1, not applied here): derive the tokens from the measured booleans,
i.e. `"ok" if toolgate else "bad"`, `"ok" if containment else "bad"`,
`"ok" if expectgate else "bad"`.

### F2 (HIGH) — C3's `met` drops the count-c1 pin, and `failed=` is suppressed when met

`count-c3.py:255`:

```python
met = (c2_ok and toolgate and old_hole and containment and expectgate)
```

`count_c1_absent` / `count_c1_sha` (appended at `count-c3.py:148,150`) are not conjuncts,
and `count-c1.py` is used nowhere else in the file (`C1_REL` occurs only at lines 53, 146).
Because the failed suffix is printed only `if not met` (`count-c3.py:307-308`), a wrong
count-c1 is not observable in the target line at all. The contract's C3 kill-rule sentence
"count-c3 pins count-c1 (sha `795c1f31…ddbae`) and count-c2 …" is checked but not enforced.

Empirical proof with unmodified frozen counter bytes: in a throwaway clone under scratch
(`git clone --shared`, toplevel asserted) I rewrote only
`.ufo/waves/round-60/count-c1.py` at a new commit on top of the freeze tree and ran the
lane's frozen `count-c3.py` against that revision:

```
$ git -C <clone> rev-parse --show-toplevel
/fast/scratch/hyaku/mori-r60/Mo60Reviewer13/alias-clone
$ git -C <clone> show <audit-rev>:.ufo/waves/round-60/count-c1.py | sha256sum
f5ed5dd7c9a7bf36eb43eea64f5ba4f16c3e1cf83562eae1b37cb083575048d6   # != PIN_C1
$ git -C <clone> show <audit-rev>:.ufo/waves/round-60/count-c2.py | sha256sum
8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976   # == PIN_C2
$ TMPDIR=<scratch>/c3alias python3 .ufo/waves/round-60/count-c3.py ec53e32c... --repo <clone> --scratch <scratch>/c3alias
C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=ec53e32ce883e01c48d815ea4082e0fbb7c11cd2
EXIT=0
```

Direct `measure()` on the same inputs shows the orphaned reason:

```
met = True
failed = ['count_c1_sha']
detail = {'cases': 6}
```

The bogus count-c1 was a two-line stub printing a met-looking C1 line, so the frozen C3
target line is reproducible — byte for byte, exit 0 — while the C1 counter under test is
not the pinned one. No production byte was touched; the rewrite happened only in the scratch
clone (`git -C <clone>` for every command).

### F3 (MEDIUM) — C3's containment arm cannot attribute the write it refuses

Same code as F1's reachability proof, stated as its own defect: `not (g2.parent /
"escape.txt").exists()` and `not (g2 / "nowhere" / "f.txt").exists()`
(`count-c3.py:218-219`, `227`) are path-existence checks, not effects of `materialize()`. Any
pre-existing file at those paths (stale scratch, a sibling seat's stray write, a recycled
`--scratch` dir) makes `containment` False and `C3=unmet` although no escape occurred — the
demonstrated `failed=g2_escape_written` run above is exactly that false negative. The
converse (a real escape that leaves no file, e.g. a write to a symlinked *file* target, or
content written and removed) is also unobserved by this arm. Suggest recording the
pre-run existence state, or asserting the specific path does not exist *and* was not
created by the probe, and adding a symlinked-file escape case.

### F4 (MEDIUM) — C2's `claims=`/`files=` frozen values are not entailed by P-C2

P-C2 and `count-c2.py:330-332` require `claims >= MIN_CLAIMS (10)`, `files >= MIN_FILES (3)`,
`spans == claims`. The target pins the exact data-driven values `claims=13 files=6
spans=13`, printed straight from the pinned tool's stats dict (`count-c2.py:326-328`,
`479-480`). A conforming met run therefore can print, e.g., `claims=11 files=4 spans=11`,
exit 0, and **not** the frozen target line. The target's numeric identity rests on the
content of `corpus/knowledge/wave-settlement-artifacts-r59.md` and the six ARTIFACTS copies,
not on the predicate. Observed values currently match at both revisions tested
(`ac496c7c` and tip `b3c25613`: 13/6/13, exit 0), so this is a target-vs-predicate gap, not
a live failure — but it is the token group most exposed to the C1 data landing during this
wave (SOURCES.md rows feed `rows`/`pins` binding; `files` is pinned by the ARTIFACTS map).
Either freeze the expected numbers as predicates or state the target's numeric cells as
data receipts rather than as predicate consequences.

### F5 (LOW) — C1's correction sub-arm has no token

`count-c1.py:234-236` requires `corr` (`corrected_lines_name_real`, `count-c1.py:88-97`),
but the print line has no `corr` token, so a correction-only failure reads
`C1=unmet dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok` plus
`failed=correction_incomplete`. Not a target-token gap (the contract does not tokenize it);
recorded so a future reader does not take `dead-uncorrected=0` as the whole dead-name arm.

### F6 (INFO) — C1's numeric tokens are fully entailed; denominators are literals

Every C1 numeric token is a met conjunct with a fixed denominator that currently equals the
collection size: `receipts=%d/2` with `len(R59_COUNTERS)==2`, `absent-set=%d/5` with
`len(NAMES)==5`, `dead-uncorrected=0` required by `dead == 0` (`count-c1.py:234-236`).
Hardcoding `/2` and `/5` is latent brittleness only (counter bytes are frozen); if either
collection grows, the printed denominator silently lies. `dead-uncorrected` can print `-1`
when `SCORECARD.md` is absent (`count-c1.py:150`), but only on an unmet line.

---

## 3. Residual risk and verification gaps

- Freeze/tip drift: C2 and C3 were re-measured at the freeze rev and again at tip
  `b3c25613`; both still print their frozen targets. C1's data landed mid-wave
  (`398d3225`), and the tip run prints the frozen target. A later C1/SOURCES landing could
  still move C2's `rows`/`pins` tokens (not observed) — every figure in this report is
  pinned to `ac496c7c` or `b3c25613` and none is an unpinned working-tree read.
- The count-c1-pin hole (F2) means the C3 after-receipt cannot distinguish a genuine C1
  counter from a substituted one; the C1 claim must be receipt-checked separately (it is:
  C1's receipts arm re-runs the r59 counters, not count-c1) — but the C3 line itself gives
  no evidence for the pin the contract asserts.
- F1's `toolgate`/`expectgate` lie is reported as structural; I could not make the pinned
  count-c2 misbehave (which would be required to reach those two literals), so the empirical
  demonstration covers `containment` only. I did not doctor the pinned module, because that
  would have invalidated the identity of the artefact under test.
- C1 at the freeze rev prints the pre-data `unmet` line by construction (data lands during
  the wave); that is expected and is not scored here.

## 4. Method / hygiene

- Work read-only on the lane: `git show`, `git cat-file`, `git ls-tree` through the counters,
  plus `sed`/`grep` reads of the frozen bytes. No lane write, no VCS mutation, no
  SCORECARD/LOG/corpus edit, no fleet or sibling-repo write.
- All scratch under `/fast/scratch/hyaku/mori-r60/Mo60Reviewer13/`; every radiused counter
  run used `--scratch` there with `TMPDIR` set; the only git writes were in
  `/fast/scratch/hyaku/mori-r60/Mo60Reviewer13/alias-clone` (toplevel asserted before the
  first write), which was created with `git clone --shared` and removed afterwards.
- Disk guard green before heavy work (`/fast/scratch/hyaku 26% free 598.7G`).
- No tool installs, no package-manager transactions, no `pacman`. Nothing installed or
  updated, so no tool/version/channel record is due.
- Scratch cleaned before yield.

## Verdict

Token presence: PASS (0 tokens missing, 0 extra). Predicate identity: **FAIL** on
C3's three gate tokens (F1, empirically demonstrated) and on C3's `met` vs the count-c1 pin
(F2, empirically demonstrated); **PARTIAL** on C2's exact numeric target cells (F4). The
frozen C1 target line is exactly entailed by P-C1 and reproduced at tip.
