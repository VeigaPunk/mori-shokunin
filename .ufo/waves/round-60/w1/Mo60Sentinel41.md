# Mo60Sentinel41 — execution-boundary re-audit of the round-60 counters

Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Freeze (amended): `ac496c7cde8cad965079858accae3bedfe4a73f2` · entering: `ddfb12fb0838b4307c445194a844f0c4b1950195`
Lane tip during my pass: `b3c256138f00c704d5aa56eb0332d74506502ef2`; `ac496c7` is an ancestor (3 commits ahead).
Work mode: read-only. No commits, no VCS mutation, no lane/fleet writes. All fixtures under
`/fast/scratch/hyaku/mori-r60/Mo60Sentinel41` (created with `mkdir -p`; `TMPDIR` set there; every
fixture repo `git -C <fixture>` and `rev-parse --show-toplevel` asserted).

Pin check first (everything I re-derive below uses revision-pinned `git show`, never a working-tree read):

| path | sha256 @ ac496c7 | sha256 working tree |
|---|---|---|
| `.ufo/waves/round-60/count-c1.py` | `795c1f31…617ddbae` | identical |
| `.ufo/waves/round-60/count-c2.py` | `8c4814f5…3ccdf976` | identical |
| `.ufo/waves/round-60/count-c3.py` | `fabde06c…b5153514` | identical |
| `tools/mori-entry-claims-check.py` | `cffe9f33…e0eae6e69` | identical |
| `tools/mori-settlement-scan.py` | `4c04bf21…ea5ac9a9` | identical |

`grep -n "/home/\|/fast/\|/tmp/\|/var/tmp"` over the three counters → `NONE` (absolute-host-path item honored).

---

## Verdict

**The seat's target sentence is false for count-c1, and C3's «G1 is structural there» exemption is
unsupported.** count-c1 executes **four** distinct repo-supplied blobs (two r59 counters, two tools)
in **21 child invocations**, and **no sha256 comparison to any frozen pin exists anywhere on that
path**. count-c2 is clean: every blob it executes hashes exactly to `PIN_EC`/`PIN_SCAN`. count-c3 is
clean for its own instruments but executes, by design, the unpinned r59 counter as its control — and
its G1 witness is not arm-complete, which I falsified with a mutant.

Verdict recap per counter:

| counter | exec sites | executed bytes pinned? | boundary holds? |
|---|---|---|---|
| count-c1 | `count-c1.py:127-135` (r59 counter), then r59 code | **NO pin at all** (revision constant only) | literal claim false; see F1 |
| count-c2 | `count-c2.py:149` via `run_pinned` | yes — `:147` gate, `:169`/`:179` gated materialize | holds (verified by sha of executed files) |
| count-c3 | `count-c3.py:168,190,243` (`run_counter`), `:210` (`exec_module`) | `c2_b` pinned `:140-141`; **`r59c2_b` unpinned** `:151` | holds for instruments; control arm unpinned by design; G1 witness incomplete (F2) |

---

## F1 — MEDIUM — count-c1 executes repo tool blobs unpinned; contract's C3 kill-rule sentence is false

**Contract text falsified** (`contract.md:122-124`): "count-c1 executes no repo-supplied tool blob
(its re-runs are revision-pinned), so G1 is structural there."

**Code** — `count-c1.py:124-135`:

```python
tmp = Path(scratch) / ("r59counter-%d.py" % idx)
tmp.write_bytes(cb)                      # cb = git show R59_DATA:<r59 counter>
...
p = subprocess.run([sys.executable, str(tmp), R59_DATA, "--repo", ...,
                    "--scratch", str(out_dir)], env={**os.environ, "TMPDIR": ...})
```

The executed r59 counters are r59's *unpatched* shape — write-then-exec, never gated on `tool_ok`:
`.ufo/waves/round-59/count-c2.py:205-210` (`tp.write_bytes(tool_b)` then `subprocess.run([... str(tp) ...])`)
and `.ufo/waves/round-59/count-c1.py:105-110`. That is precisely the hole shape G1 claims to close,
alive one level down inside the round-60 C1 instrument.

**Evidence (strace of the pinned C1 blob, `-f -s 400 -e trace=execve`, scratch under my dir):**

```
python3 <SCR>/c1/r59counter-0.py 7b86704d… --repo <lane> --scratch <SCR>/c1/rr-0
python3 <SCR>/c1/r59counter-1.py 7b86704d… --repo <lane> --scratch <SCR>/c1/rr-1
python3 <SCR>/c1/rr-0/tool.py  --selftest --scratch <SCR>/c1/rr-0/st
python3 <SCR>/c1/rr-0/tool.py  --scorecard …/fx/f01-stub-only/scorecard.md …   (f01…f13: 13 execs)
python3 <SCR>/c1/rr-0/tool.py  --scorecard <SCR>/c1/rr-0/real/scorecard.md …   (2 execs)
python3 <SCR>/c1/rr-1/tool2.py --selftest --scratch <SCR>/c1/rr-1/st2
python3 <SCR>/c1/rr-1/tool2.py <5 real w1-results.json>
python3 <SCR>/c1/rr-1/tool2.py <round-53/w1-results.json>
```

Blob shas actually executed on that path (hashed at `R59_DATA`):
`tools/mori-register-check.py` = `38b733d8…1472b8` (r59's own PIN; **no r60 pin exists**, no comparison made),
`tools/mori-settlement-scan.py` = `4c04bf21…ea5ac9a9` (= `PIN_SCAN` by coincidence — still executed without comparison),
r59 counters = `2df3ae84…5877be` / revision-pinned only.

**Exploit path (demonstrated, needs caller-environment control):** `count-c1.py` inherits the full
environment into both git and the children (`env={**os.environ, "TMPDIR": ...}`, `:135`) and never
confines the repository identity. With a synthetic commit replacing `7b86704d…` via a replace ref in a
throwaway repo plus `GIT_DIR`/`GIT_ALTERNATE_OBJECT_DIRECTORIES`, the pinned C1 blob executed
**attacker bytes**:

```
$ GIT_DIR=$SCR/repl/.git GIT_ALTERNATE_OBJECT_DIRECTORIES=<lane>/.git/objects \
  python3 <lane>/.ufo/waves/round-60/count-c1.py b3c2561… --repo <lane> --scratch $SCR/c1poc
C1=unmet dead-uncorrected=0 receipts=0/2 absent-set=5/5 lesson=ok rev=b3c2561… failed=receipt:rerun_rc=1,receipts=0/2
$ find $SCR/c1poc -name EXEC-MARKER
$SCR/c1poc/rr-0/st/EXEC-MARKER     ← tools/mori-register-check.py substitution executed
$SCR/c1poc/rr-1/st2/EXEC-MARKER    ← tools/mori-settlement-scan.py substitution executed
```

Note the counter reports the receipt mismatch only **after** the child ran. (`GIT_REPLACE_REFS`
pointing outside the queried repo did **not** substitute in git 2.56.0 — I tested forms `$D/.git` and
`$D/.git/refs/replace`; only `GIT_DIR`/alternates redirection worked. I am not claiming a lever that
did not fire.)

**Impact.** (a) The only place the "unpinned blob never runs" rule is *asserted* rather than coded is the
C3 kill rule; that sentence is wrong, so a C3 reviewer would credit a structural exemption that does not
exist. (b) Under the scored-tree threat model (attacker controls bytes at R only) the executed content
is fixed by `R59_DATA`, so this is **not** a scoring exploit. (c) Defence-in-depth regression: the r60
C1 instrument re-opens the exact r59 construction at a lower layer, and its child environment is inherited.

**Smallest remediation.** Either (i) sha-pin the two r59 counter blobs and the two tool blobs fetched at
`R59_DATA` and refuse to write/exec on mismatch (the `run_pinned` shape already exists in count-c2), or
(ii) keep revision-pinning and correct the contract sentence to say so, plus run the re-run child with a
sanitized env (`GIT_DIR`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_OBJECT_DIRECTORY`, `GIT_REPLACE_REFS`,
`PYTHONPATH` stripped). Two lines in `run_pinned`-style form; no predicate change.

---

## F2 — MEDIUM — G1's witness is not arm-complete and its marker scope is narrower than the tool's reach

**Scope** — `count-c3.py:130-131,173-174`:

```python
def markers_under(root):  return [str(p) for p in Path(root).rglob("EXEC-MARKER")]
...
no_exec = len(markers_under(s_new)) == 0
gated   = "tool_sha" in out and "tool_absent" not in out
```

Two structural limits:

1. The marker is written by the **untrusted blob**, at a path *it* chooses from *its* argv. Only the
   selftest arm passes `--scratch` (`count-c2.py:184`). The entry arm (`count-c2.py:307-316`) and the
   scan and drift arms pass no `--scratch` (`count-c2.py:212,235`), so a marker produced there lands in the
   **counter's CWD**, outside `markers_under(s_new)`.
2. G1's fixture repo contains only the two tool blobs (`count-c3.py:155-158`), so `have_all` is false and
   the entry arm can never reach execution; `REAL_SCAN`/`DRIFT_SCAN` files are absent, so the scan and
   drift arms never run either. **Only the selftest arm is witnessed.**

**Falsification (3-line mutant, built from the freeze blob, sha otherwise `8c4814f5…`):**
`run_pinned` sha check removed, `ec_b`-materialize gate removed, entry-arm `ec_ok` guard removed; run
against an enriched PoC repo (evil tools + `ENTRY` + `SOURCES` + the six artifact copies, fixture
`ce1aaa60…`, built with `git -C` and toplevel assert):

```
$ (cd $SCR/poc-run && python3 $SCR/mut/mutant-c2.py ce1aaa6…  --repo $SCR/poc-full --scratch $SCR/g1m)
C2=unmet … entry=bad … failed=drift,entry,pins,rows,scan,scan_tool_sha,selftest,tool_sha,trees,trees_set
$ find $SCR/g1m      -name EXEC-MARKER      →   (nothing)
$ find $SCR/poc-run  -name EXEC-MARKER      →   $SCR/poc-run/EXEC-MARKER
```

Output contains `tool_sha`, not `tool_absent`, and the scanned root is clean → the shipped predicate
(`:173-174`) yields `toolgate=ok` for a counter that **did execute** the unpinned blob. G1 passes while
the property it certifies is violated.

**Positive control (shipped counter, same enriched PoC, `cd $SCR/poc-run2`):**
`C2=unmet … failed=…,tool_sha,…` and `find` on scratch **and** CWD → no marker anywhere. The shipped
gate holds even when the entry arm is reachable; the defect is in the witness, not the counter.

**Impact.** A mutation-tester can regress any non-selftest arm's gate and G1 still says `ok`; the claim
"never executed by the pinned count-c2" is evidenced only for one of five execution arms.

**Smallest remediation.** `markers_under(scratch)` plus a CWD scan, and add the entry/registry/artifact
inputs to the G1 fixture so the entry arm is actually exercised (the scan/drift arms need the r54–r58 /
r53 files). No predicate change.

**Related, same witness class:** the old-counter control's confinement is also partial. The r59 counter
executes its tool **without** `--scratch` in its scan arm, so with an enriched PoC it wrote two markers —
one under its scratch, one in the CWD:

```
$ (cd $SCR/poc-run3 && python3 $SCR/mut/r59-c2.py ce1aaa6… --repo $SCR/poc-full --scratch $SCR/g1old)
$ find $SCR/g1old -name EXEC-MARKER    → $SCR/g1old/st2/EXEC-MARKER
$ find $SCR/poc-run3 -name EXEC-MARKER → $SCR/poc-run3/EXEC-MARKER
```

With count-c3's 2-file PoC only the `st2` marker exists, so `old_hole` is still true — but the "marker
reproduced" evidence is a single-arm observation, not an arm-complete one.

---

## F3 — MEDIUM — count-c3's own sha is pinned nowhere, so C3's kill rule is unenforceable for C3

`contract.md:122` pins count-c1 (`795c1f31…`) and count-c2 (`8c4814f5…`) — both match. Nothing pins
count-c3: `grep -rn "fabde06c"` over `contract.md` and `evidence/` → **no hits** (its sha is
`fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514`, working tree == freeze).
`c3-at-freeze.txt` is the counter's own output, not a hash of the counter.

**Exploit path.** A one-line edit that prints the target line (or short-circuits `measure`) is
indistinguishable from the frozen record: no downstream instrument hashes count-c3, and the kill rule
("any post-freeze change to counter bytes … invalidates the claim") has nothing to compare against.
This is the one link of the C1→C3 pin chain left open — C3 hashes C1 and C2, C1 and C2 hash their tools,
and C3 hashes nothing upstream of itself.

**Smallest remediation.** Record `count-c3.py`'s sha in the contract (or in a C3 receipt) alongside
`PIN_C1`/`PIN_C2`, and add a `PIN_C3` self-check as count-c3's first act.

---

## F4 — LOW — dead condition weakens the intended scan-arm gate; gate/exec target are separate variables

- `count-c2.py:209`: `if not (ec_ok is not None and scan_ok_sha) or not rfiles:`. `ec_ok` is a `bool`,
  so `ec_ok is not None` is always `True` — the clause is a no-op and the scan arm does not depend on the
  entry-claims pin, which is evidently what the line was written to express. No boundary effect (the scan
  blob is gated on `PIN_SCAN` independently and the executed-file hash confirms it), but the guard that
  reads the pin is not the guard that runs.
- `run_pinned` (`count-c2.py:144-152`) gates on the `blob` **argument** and then executes `tool_path`;
  the two are correlated only by the caller's discipline. A `hashlib.sha256(Path(tool_path).read_bytes())`
  check immediately before `subprocess.run` would make the pin cover the bytes that actually run.

---

## F5 — LOW (nit) — drift/alias arms ignore `materialize()`'s refusal

`count-c2.py:234,257`: the `drift` / `round-53-alias` writes ignore the return value; a refused write
leaves a missing path, the scan then errors, and the arm fails as `drift` — it fails safe, but the reason
is misattributed (no `containment:` token). The tree/entry arms do record the token correctly.

---

## Confirmed positive (no finding) — what I could not break

1. **count-c2 executes only pinned bytes.** Strace + hashes of the executed scripts:
   `c2s/ec-tool.py` = `cffe9f33…` (`PIN_EC`, 15 execs: selftest, h00–h12, real root),
   `c2s/scan-tool.py` = `4c04bf21…` (`PIN_SCAN`, 3 execs: real, drift, alias). No other child exec.
2. **count-c3's instruments are pinned**: `c2-new.py`, `c2-g3.py`, `c2-mod.py` all `8c4814f5…`
   (`PIN_C2`); the sole unpinned exec is the designated control `c2-old.py` = `2df3ae84…` (r59 bytes).
3. **G2 containment holds** against probes beyond the shipped three (pinned module, sha-checked import):
   `../` walk → `False`; `a/../../escape2.txt` → `False`; `a/../inside.txt` → `True`; absolute
   `/tmp/abs-escape.txt` → `False`; **leaf** symlink (`leaf.txt` → `/tmp/leaf-escape.txt`) → `False`;
   nothing written outside the root (`/tmp` probes absent, sibling escape absent).
4. **No repo-configured code execution** on the git plumbing used (`git show`/`cat-file`/`ls-tree`):
   no hooks, no `textconv`, no pager (stdout captured). `tools/mori-entry-claims-check.py` and
   `tools/mori-settlement-scan.py` contain no `exec`/`eval`/`__import__`/`importlib`/`subprocess`
   (grep clean), so hostile tree *content* cannot become code through the pinned tools.
5. **Receipts reproduce byte-exactly** (my runs, pinned revs, my scratch):

   ```
   C1 (b3c2561):  C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c256138f…   == evidence/c1-at-data.txt
   C2 (ac496c7):  C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=ac496c7…   == evidence/c2-at-freeze.txt
   C3 (ac496c7):  C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7…   == evidence/c3-at-freeze.txt
   selftests:     C1_SELFTEST pass=6 fail=0 | C2_SELFTEST pass=8 fail=0 | C3_SELFTEST pass=3 fail=0
   ```
6. **All three do-nothing controls at `ddfb12fb…` reproduce byte-for-byte** (rc=1 each), including
   `C3=unmet … cases=1 … g1_new_skipped,g2_skipped,g3_skipped`.

---

## Observations (not findings)

- Lane working tree carries `M corpus/lessons/round-60.md` plus untracked `evidence/c1-at-data.txt`,
  `w1.ready*`, `w1/` — the in-flight C1 data landing described in the assignment. Not mine; all my
  re-derivations use `git show` at a named revision, so they are unaffected. `find . -name EXEC-MARKER`
  in the lane → none: none of my PoCs wrote into the lane.
- `count-c1.py` has no `materialize()`; the contract's G2 wording "the counters' materialize()" (plural)
  describes count-c2 only. Containment of count-c1's own writes rests on constant filenames
  (`r59counter-%d.py`, `rr-%d/`), which is sound but unpinned-name-by-name.
- `count-c1.py:293`, `count-c2.py:469`, `count-c3.py:295` create an unremoved `mkdtemp` when
  `--scratch` is omitted. Cosmetic (i.e. it leaves litter in `TMPDIR`).
- `contained()` (`count-c2.py:114-129`, `materialize` `:132-141`) is check-then-write (TOCTOU window). Not reachable today: no
  concurrent writer runs while materialize is in flight (the pinned tools create no symlinks), and the
  leaf/`..`/absolute cases are refused as probed above.

---

## Reproduction (scratch only)

```bash
SCR=/fast/scratch/hyaku/mori-r60/Mo60Sentinel41; export TMPDIR=$SCR; mkdir -p $SCR
L=/home/vgpnk/Projects/shokunin/mori-shokunin; F=ac496c7cde8cad965079858accae3bedfe4a73f2
python3 $L/.ufo/waves/round-60/count-c{1,2,3}.py --selftest
python3 $L/.ufo/waves/round-60/count-c1.py b3c256138f00c704d5aa56eb0332d74506502ef2 --scratch $SCR/c1
python3 $L/.ufo/waves/round-60/count-c2.py $F --scratch $SCR/c2
python3 $L/.ufo/waves/round-60/count-c3.py $F --scratch $SCR/c3
# F1: enumerate what count-c1 actually runs
strace -f -qq -s 400 -e trace=execve -o $SCR/exec-c1.log \
  python3 $L/.ufo/waves/round-60/count-c1.py b3c2561… --scratch $SCR/c1
grep '= 0$' $SCR/exec-c1.log | grep -E 'tool2?\.py|r59counter'
```

Inventory of executed script hashes used above was taken with
`find $SCR/c2s $SCR/c3s -maxdepth 2 -name '*.py' -type f -exec sha256sum {} +`.

Scratch (`/fast/scratch/hyaku/mori-r60/Mo60Sentinel41`, 56 MB pre-existing neighbours untouched,
600 GB free on `/fast`) removed after this report was written. No dated receipts were retained by
design; every figure above is reproducible from the commands and pinned revisions in this file.
