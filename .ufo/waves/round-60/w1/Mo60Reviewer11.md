# Mo60Reviewer11 — dead-name sweep (mori round 60, wave w1)

Seat: Mo60Reviewer11, reviewer (leaf). Read-only work: no commits, no VCS mutation, no fleet or
sibling-repo writes. Scratch `/fast/scratch/hyaku/mori-r60/Mo60Reviewer11` (created with `mkdir -p`,
`TMPDIR` set to it, deleted before yield).

## Revisions (every read pinned)

| role | revision |
|---|---|
| R (measured tip, `master`, also lane `HEAD`) | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| entering | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| freeze (amended) | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| r59 data revision | `7b86704d7c0754a09958d131b64dbfa2a6d3eaed` |

`git diff --quiet HEAD -- SCORECARD.md` → IDENTICAL, so the working-tree `grep` the seat names and
the pinned-blob reads below agree at R. Lane worktree has four **untracked** entries from sibling
seats in flight (`.ufo/waves/round-60/evidence/c1-at-data.txt`, `w1.ready`,
`w1.ready.dispatched`, `w1/`); none is tracked and none touches `SCORECARD.md`.

## Verdict

**The frozen C1 DEAD-NAME ARM passes at R.** The seat's two checks hold, exactly:

1. every occurrence of `c1-entering.txt` / `c2-entering.txt` in `SCORECARD.md` sits on a line
   carrying `r60-correction:` and names the real committed pointer;
2. both real pointers (`control-c1-do-nothing.txt`, `control-c2-do-nothing.txt`) exist at R.

The frozen counter independently reproduces the contract's target output at R (rc 0) and its
do-nothing control at the entering revision (rc 1). Two residuals the arm cannot see are recorded
as F1/F3; neither contradicts the frozen predicate sentence.

## 1. Occurrence census at R

```
$ grep -n 'c1-entering\.txt\|c2-entering\.txt' SCORECARD.md        # worktree, == R
2950:| C1: pinned `tools/mori-register-check.py` ... `C1=unmet selftest=bad fixtures=bad real=bad pointers=bad failed=...` , rc 1 (`.ufo/waves/round-59/evidence/control-c1-do-nothing.txt` — r60-correction: the r59 report and this cell cited a dead name `c1-entering.txt`; the committed control receipt is `control-c1-do-nothing.txt`) | ...
2951:| C2: pinned `tools/mori-settlement-scan.py` ... (`.ufo/waves/round-59/evidence/control-c2-do-nothing.txt` — r60-correction: the r59 report and this cell cited a dead name `c2-entering.txt`; the committed control receipt is `control-c2-do-nothing.txt`) | ...
```

Pinned-blob census (python over `git show R:SCORECARD.md`) — whole SCORECARD, not just the two rows:

```
LINE 2950: hits=['c1-entering.txt'] marker=True  len=1271  count(c1-entering.txt)=1
LINE 2951: hits=['c2-entering.txt'] marker=True  len=1189  count(c2-entering.txt)=1
```

* total occurrences **2**, occurrences on lines **without** the marker **0**;
* marker-line census at R: `git grep -c 'r60-correction:' R -- '*.md'` →
  `contract.md:1`, `SCORECARD.md:2`, `QUALITY.md:1`, `corpus/lessons/round-60.md:1` — the only two
  marker lines in `SCORECARD.md` are the two dead-name lines, so no marker line exists without a
  dead name and no dead name outside a marker line.
* lane-wide `git grep -e 'c1-entering\.txt' -e 'c2-entering\.txt' R -- .` finds the two SCORECARD
  lines plus (i) round-60 instrument/spec text that quotes the names as the predicate's subject
  (`contract.md:41`, `count-c1.py`, `w1-spec.json`/`w1-dispatch.json`/`build-w1-spec.py`), (ii) the
  round-50 scribe note naming its own round-50 `c1-entering.txt` capture, and (iii) the r59
  spot-check lesson and the r60 lesson describing the defect. No lane file follows either name as
  a live evidence pointer.

At the entering revision the same cells were live dead pointers, which is why the control fires:

```
$ git grep -n 'c1-entering\.txt' ddfb12fb -- SCORECARD.md
ddfb12fb:SCORECARD.md:2950: ... rc 1 (`.ufo/waves/round-59/evidence/c1-entering.txt`) | ...
ddfb12fb:SCORECARD.md:2951: ... rc 1 (`.ufo/waves/round-59/evidence/c2-entering.txt`) | ...
```

## 2. Real pointers exist at R, and the corrected lines resolve completely

```
$ git cat-file -e R:.ufo/waves/round-59/evidence/control-c1-do-nothing.txt   -> EXISTS
$ git cat-file -e R:.ufo/waves/round-59/evidence/control-c2-do-nothing.txt   -> EXISTS
$ git show R:.ufo/waves/round-59/evidence/control-c1-do-nothing.txt | sha256sum
b2a9ff4ac95cdbc4a3de9219343c309c4175b7681a87bd2412e35c5e120cbc99
$ ... control-c2-do-nothing.txt | sha256sum
ae2f00d39c6b0d9ab57ab78183e29cb5884c4e3155a7678e9902bb64e452982a
```

`git ls-tree` shows both in `.ufo/waves/round-59/evidence/` at entering `ddfb12fb`, at the r59 data
revision `7b86704d`, and at R — the receipts pre-date the correction, so the correction points at
files that were already committed when the r59 rows were filed.

The corrected lines carry no other dead pointer. QUALITY-156-style sweep, `(\.ufo/…|corpus/…|tools/…)`
per hit + `git cat-file -e` at R:

```
line 2950: 3/3 OK   tools/mori-register-check.py
                    .ufo/waves/round-59/count-c1.py
                    .ufo/waves/round-59/evidence/control-c1-do-nothing.txt
line 2951: 4/4 OK   tools/mori-settlement-scan.py
                    corpus/knowledge/wave-settlement-artifacts-r59.md
                    .ufo/waves/round-59/count-c2.py
                    .ufo/waves/round-59/evidence/control-c2-do-nothing.txt
```

The correction's factual premise also holds: neither dead name was **ever** committed, on any ref —

```
$ git log --all --oneline -- '*c1-entering.txt'   -> 0 commits
$ git log --all --oneline -- '*c2-entering.txt'   -> 0 commits
```

and the r59 evidence tree contains exactly `c1-at-freeze.txt`, `c2-at-freeze.txt`,
`census-start.txt`, `control-c1-do-nothing.txt`, `control-c2-do-nothing.txt`, `selftests.txt` at
both `ddfb12fb` and `7b86704d` — no `c1-entering.txt`/`c2-entering.txt`, no `controls.txt`.

## 3. Frozen-counter corroboration (read-only, frozen bytes, `--scratch` under seat scratch)

```
$ python3 .ufo/waves/round-60/count-c1.py --selftest
C1_SELFTEST pass=6 fail=0                        rc=0        (contract: pass=6 fail=0)

$ python3 .ufo/waves/round-60/count-c1.py b3c25613… --scratch $S/c1-tip
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…   rc=0
                                                 (byte-for-byte the contract's target line)

$ python3 .ufo/waves/round-60/count-c1.py ddfb12fb… --scratch $S/c1-entering
C1=unmet dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent rev=ddfb12fb… failed=absent_set=0/5,absent_table_absent,correction_incomplete,dead=2,lesson_absent,receipt_absent:…,receipts=0/2
                                                 rc=1
$ cmp <that run> <git show R:.ufo/waves/round-60/evidence/control-c1-do-nothing.txt>
BYTE-EQUAL                                       (the arm is non-vacuous today, not only in receipt)
```

No lane mutation occurred during these runs (`git status --porcelain` after them shows only the four
sibling untracked entries above); the counter materialises revision-pinned r59 counter bytes under
`--scratch` and uses `git show`/`cat-file` on the repo.

## 4. Findings by severity

### F1 — MEDIUM (residual, explicitly outside the frozen arm): the "report" half of routed defect #1 is still live in the fleet repo

The r60 correction clause says "the r59 report and this cell cited a dead name … the committed
control receipt is `control-c1-do-nothing.txt`". That statement is true — but the r59 report itself
was never corrected; at fleet HEAD it still tells a reader to open three files that never existed:

```
$ cd /home/vgpnk/Projects/shokunin
$ git grep -n -e 'c1-entering\.txt' -e 'c2-entering\.txt' HEAD -- .ufo/reports .ufo/waves LOG.md
HEAD:.ufo/reports/round-59/mori.md:120:`.ufo/waves/round-59/evidence/`: `c1-entering.txt`, `c2-entering.txt` (do-nothing controls),
        `c1-at-freeze.txt`, `c2-at-freeze.txt`, `selftests.txt` (…), `controls.txt`, `census-start.txt`, …
```

* `c1-entering.txt`, `c2-entering.txt` and `controls.txt` were never committed under
  `.ufo/waves/round-59/evidence/` (`git log --all --oneline -- '.ufo/waves/round-59/evidence/controls.txt'`
  is empty; rounds 56 and 58 do own an `evidence/controls.txt`, round 59 does not).
* The report never names the real receipts: `git grep -n 'control-c[12]-do-nothing' HEAD -- .ufo/reports/round-59`
  is empty. Fleet worktree == fleet HEAD for that file (`git diff --stat` empty).
* `corpus/QUALITY.md:1602-1604` discloses the scoping gap — "Not covered: pointers outside
  `.ufo/`/`corpus/` (fleet-repo report paths are resolved by the closure, not this sweep)" — and
  `corpus/lessons/round-60.md` Mistakes 1 lists the fix as the SCORECARD re-pointing + the count-c1
  arm + QUALITY 156, not a report edit. So this is a **disclosed open item, not a violated claim**;
  the L1 must close it at closure (fleet-repo edit or an explicit closure note) or the r60 record
  will read as if report+SCORECARD were both repaired when only SCORECARD was.

### F2 — LOW (checked, no defect): the correction's claim about the report is accurate

The clause's "the r59 report … cited a dead name" resolves to the fleet line above; the cell claim
resolves to `ddfb12fb:SCORECARD.md:2950-2951`. The correction clause does not overstate what was
cited. Note it also uses the basename (`control-c1-do-nothing.txt`) while the full lane-relative
path already sits in the same cell, so the pointer is unambiguous.

### F3 — LOW (predicate-faithful blind spot, demonstrated): the arm skips whole marker lines and knows only two names

The frozen sentence exempts "lines carrying the literal marker", and `dead_uncorrected()` implements
that literally by `continue`-ing the whole line. Two consequences, shown on crafted inputs with the
frozen functions (no repo change):

```
# one corrected line + one stray marker line that still points at the dead name
dup: dead_uncorrected=0 corrected_names=True     <- stray dead pointer in the stray row survives
# a dead pointer whose name is not in DEAD_NAMES
controls.txt uncorrected: dead_uncorrected=0     <- invisible
```

At R there is no such stray mention (only the two occurrences, both on the corrected lines), so the
arm's verdict is sound for this tip. The residual is that a future edit could re-introduce a dead
mention on any marker line — or a third dead name such as `controls.txt` — and still score
`dead-uncorrected=0`. Route to whoever hardens C1 next round; do not treat as a present defect.

### F4 — INFO (citation fidelity nit, not a pointer defect): C1 row elides the receipt's `rev=` token without an ellipsis

The C1 row quotes `C1=unmet selftest=bad fixtures=bad real=bad pointers=bad failed=tool_absent,…`,
rc 1, while the committed r59 receipt has `… pointers=bad rev=2b9f…e805 failed=…`. The C2 row marks
its elision with `…`; the C1 row does not. Both cells still resolve to the same committed receipts
(verified in §2), so this is a presentation nit only.

### F5 — INFO (measurement hygiene): only `master` is clean; other refs hold uncorrected variants

`git log -S` surfaced `036406ef`, `aef43f27`, `5f0243f8` (empty commit subjects, scratch-residue
commits); `git merge-base --is-ancestor <c> master` → NO for all three. `master`'s post-freeze chain
is `4d036fb0` (freeze) → `772b2b4b`/`ac496c7c` (amendments) → `76904b21` (dispatch) → `398d3225`
(C1 data landing, single correction commit) → `b3c25613` (census row move). Many `refs/jj/keep/*`
refs therefore carry SCORECARD variants with the dead names uncorrected. Every C1 measurement must
pin `b3c25613` (or a later `master`), never "the tip of `--all`". This round measured the pinned R.

## 5. Residual risk and verification gaps

* Not verified by this seat (other arms/seats own them): the C1 receipts arm's byte-equality against
  the r59 counters (the frozen counter reported `receipts=2/2` and rc 0; I did not re-derive it
  independently), the absent-set table, and the round-60 lesson's `late-committed`/`wrong-superseded`
  classification; C2 depth and C3 operability were not run.
* F1 cannot be closed from inside this seat (fleet-repo edit forbidden here) — it needs an L1 closure
  action or an explicit closure statement.
* The dead-name arm's scope is the SCORECARD only; the r59 report's `controls.txt` citation is
  invisible to it by design (F3) and by path (F1).
* No tool was installed or updated in this seat; no pacman transaction was run.

## 6. No-mutation statement

All workspace writes were limited to this report and the seat scratch dir
(`/fast/scratch/hyaku/mori-r60/Mo60Reviewer11`, deleted before yield). No `git commit`, `git add`,
`git checkout`, `jj`, or any other VCS write ran against the lane, the fleet repo, or any sibling
repo; every git command was read-only (`rev-parse`, `log`, `show`, `cat-file`, `grep`, `ls-tree`,
`diff`, `status`).
