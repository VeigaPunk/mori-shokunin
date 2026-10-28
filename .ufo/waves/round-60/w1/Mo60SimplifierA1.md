# Mo60SimplifierA1 — count-c2 dead-weight / duplicate audit (r60 wave w1)

Seat scope: read `.ufo/waves/round-60/count-c2.py` and **propose** minimal
deletions that preserve the frozen predicate semantics (dead branches,
duplicate failed-append tokens). Report only — the committed bytes are
frozen. Read-only on the lane; no production/corpus/SCORECARD/LOG edits, no
lane VCS mutation, no fleet/sibling writes, no subagents.

- Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`
- Contract read first: `.ufo/waves/round-60/contract.md` (freeze
  `ac496c7cde8cad965079858accae3bedfe4a73f2`, entering
  `ddfb12fb0838b4307c445194a844f0c4b1950195`).
- Lane tip observed at start: `b3c256138f00c704d5aa56eb0332d74506502ef2`
  (tip may move under this wave — every derivation below is pinned to a
  named revision, never to an unpinned working-tree read).
- Scratch: `/fast/scratch/hyaku/mori-r60/Mo60SimplifierA1/` (`mkdir -p`,
  `TMPDIR` set there, `--scratch` under it, removed after this report).
  Disk guard at start: exit 0, `/fast/scratch/hyaku` 26% used, 598.3G free.
  No tools installed or updated (used pre-existing `ruff`, `pyflakes`).

## Instrument identity (revision-pinned)

```
$ git -C <lane> rev-parse ac496c7cde8cad965079858accae3bedfe4a73f2:.ufo/waves/round-60/count-c2.py
af6ac716bf560885ed7ca75198f3e0ab57ab30d4
$ git -C <lane> rev-parse b3c2561:.ufo/waves/round-60/count-c2.py
af6ac716bf560885ed7ca75198f3e0ab57ab30d4          # unchanged since the freeze commit
$ sha256sum <scratch>/base.py                      # materialized via git show ac496c7c:…
8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976
```

That sha256 is exactly `PIN_C2` in `count-c3.py:52`, so the bytes audited are
the frozen bytes.

## Method

1. Static: `ruff check --select F,E7,F841,F811,F821 base.py` → *All checks
   passed*; `pyflakes base.py` → no output. There is no unused symbol /
   unreachable-name weight left; remaining weight is inside boolean
   expressions and one duplicated read.
2. Manual branch audit of all 11 `git_show` call sites in `measure()` and all
   25 `failed.append` sites (`grep -c 'failed.append'` → 25).
3. A/B harness: `var.py` = frozen bytes + the four deletions below
   (sha256 `28f5eae8a513f110b347f8ca63e2c2a48cfb3f5c56489d98551a7f41cf3384de`,
   `python3 -m py_compile` ok, 488 lines both). Both files were run at the
   same pinned revisions with separate `--scratch` dirs and compared as
   whole strings plus exit codes.
4. Extra arms: a throwaway fixture repo under scratch
   (`mktemp -d -p <scratch>`, `git -C "$D" init -q`, toplevel asserted =
   `$D`; content extracted with `git -C <lane> archive ac496c7c … | tar -x -C
   "$D"`) reproducing the tool-sha, scan-tool-sha and entry-absent failure
   arms that the proposed edits touch.

## Proposed deletions (all output-neutral; proven, not asserted)

### D1 — always-true conjunct, `count-c2.py:209`

```diff
-    if not (ec_ok is not None and scan_ok_sha) or not rfiles:
+    if not scan_ok_sha or not rfiles:
```

`ec_ok` is assigned at line 162 as `ec_b is not None and sha256(ec_b) ==
PIN_EC`, i.e. it is always a `bool`; `x is not None` is therefore always
`True` and the conjunct contributes nothing. [INFERENCE: the author's likely
intent was gating the scan arm on the *entry* tool; that gate has never been
in effect — the scan arm depends only on `scan_ok_sha`, as the entering-rev
run below shows.] Exhaustive truth table over the four reachable states:

```
ec_ok=True  scan_ok_sha=True  base=False var=False equal=True
ec_ok=False scan_ok_sha=True  base=False var=False equal=True
ec_ok=False scan_ok_sha=False base=True  var=True  equal=True
ec_ok=True  scan_ok_sha=False base=True  var=True  equal=True
```

`ec_ok=False, scan_ok_sha=True` is not hypothetical: it is the entering
revision `ddfb12fb…`, where the scan arm is `scan=ok drift=ok` and the entry
tool is absent (`tool_absent`). Base and variant produce identical lines
there (see matrix).

### D2 — two redundant `is not None` guards, lines 168 and 178

```diff
-    if ec_b is not None and ec_ok:
+    if ec_ok:
         ec_path.write_bytes(ec_b)  # materialize only when pinned
…
-    if scan_b is not None and scan_ok_sha:
+    if scan_ok_sha:
         scan_path.write_bytes(scan_b)
```

`ec_ok`/`scan_ok_sha` are each defined as `<blob> is not None and sha ==
PIN`, so the extra conjunct is implied. Both edits keep the pinned-blob-only
materialization (G1) intact — exactly one condition remains, and it is the
sha gate.

### D3 — duplicated ENTRY fetch, lines 296–305 (the one real duplicate)

```diff
         b = git_show(repo, rev, rel)
         if b is None:
             have_all = False
+            if rel == ENTRY:
+                failed.append("entry_absent")
             continue
         if materialize(root, rel, b) is False:
             have_all = False
             failed.append("containment:entry")
-    if git_show(repo, rev, ENTRY) is None:
-        failed.append("entry_absent")
```

`ENTRY` is the first element of the loop list at line 296, so line 304 is a
second `git show R:corpus/knowledge/wave-settlement-artifacts-r59.md` for a
blob already read one statement earlier — 11 `git_show` call sites in
`measure()` become 10 (lines 161, 171, 196, 232, 254, 278, 279, 297, 304,
358, 373 → 304 goes). Token condition is identical (`ENTRY` blob absent),
`failed` is `sorted(set(...))` at line 411 so append position is
unobservable. Empirically: fixture commits `81dc2b3` (ENTRY deleted) and
`8fd8999` (ENTRY+SOURCES deleted) each yield `entry_absent_count=1` for base
and variant, byte-identical whole output, and `8fd8999` produces no spurious
`entry_absent` for the missing `SOURCES`.

### D4 — redundant disjunct, line 129 (`contained`, G2 core)

```diff
-    return resolved == root_r or resolved.is_relative_to(root_r)
+    return resolved.is_relative_to(root_r)
```

`Path.is_relative_to(self)` is `True` (a path is relative to itself;
verified on the interpreter that runs the counter, `python3` → 3.14.8:
`Path('/a/b').is_relative_to(Path('/a/b'))` → `True`), so the equality arm is
dead for every input, including the only case where it could matter — target
== root.

Equivalence evidence (imported both modules, same filesystem matrix):

```
inside         base=True  var=True  same=True
root_itself    base=True  var=True  same=True      # the deleted disjunct's only candidate
dotdot_escape  base=False var=False same=True
deep_dotdot    base=False var=False same=True
symlink_dir    base=False var=False same=True
symlink_file   base=False var=False same=True
abs_outside    base=False var=False same=True
materialize in  base=True  var=True  same=True
materialize up  base=False var=False same=True
materialize ln  base=False var=False same=True
EQUIVALENT True   no_escape_leak True
```

Also replayed count-c3's own G2 triple (`../escape.txt`, `inside/f.txt`,
`ln/f.txt` with `ln -> nowhere`): base `(False, True, False, False, False)`,
var `(False, True, False, False, False)`, `C3_G2_TRIPLE_EQUAL True`.

## Duplicate failed-append tokens — finding: none are literally duplicated

Token set from the 25 append sites contains no repeated literal; the only
repeat-append of an *identical* token happens inside three loops, and each is
already collapsed by `sorted(set(failed))` at line 411:

| site | token | repeats |
|---|---|---|
| 206 `containment:scan` | identical string | once per failing `REAL_SCAN` rel (≤5) |
| 303 `containment:entry` | identical string | once per failing materialized rel (≤8) |
| 377 `containment:tree:%s` | identical per tree | once per failing file in that tree |

All three are G2 refusal diagnostics for inputs that cannot occur here (fixed
literal rels; no `..` components and no symlink components below the scratch
root), and deleting them would remove containment evidence the C3 report
leans on. Converting `failed` to a `set`
(and dropping `set()` at 411) is output-neutral but rewrites 25 sites for
zero observable gain — **not proposed**.

## Deliberate non-deletions (deleting these would harm an axis)

- `run_pinned`'s `blob is None or sha256(blob) != expect_pin` gate
  (lines 147–148): G1's core. Every call site already pre-verifies, so the
  `blob is None` half is unreachable *today*; it is the `None` guard that
  keeps `sha256(None)` from raising if a future arm forgets the pre-check.
- `ran and p.returncode …` / `ran2 and p2.returncode …` (220, 249, 268, 329):
  `ran` is invariant-true inside their gates, but it is the short-circuit
  that prevents `None.returncode` if `run_pinned` ever refuses. Rewriting
  them to bare `p.returncode` trades a real safety net for a few bytes.
- `not rfiles` (line 209): with `REAL_SCAN` frozen at 5 entries it is
  unreachable-false, but it is the anti-vacuity guard — without it, an
  emptied `REAL_SCAN` would run the scan tool with no arguments and could
  report `scan=ok` over zero files. Keep.
- `contained`'s symlink-parent walk (119–124) and `materialize`'s `is False`
  contract, because `count-c3.py:205–219` imports this module and calls
  `mod.materialize(...)`.
- `expect_tamper` / `tree:…:frozen|expect|tool|verdict|reasons` paths (G3,
  and `count-c3.py:30` asserts `expect_tamper:h02-malformed-claim`).
- `detail` bookkeeping: every key is read by `main().tok()`.

## Landing constraint (why this stays a proposal)

The bytes are frozen by the contract kill rule, and there is a live sha
coupling: `count-c3.py:52 PIN_C2 = 8c4814f5…ccdf976` equals the current
counter sha, so **any** accepted edit makes `c3` fail `count_c2_sha`/`c2_ok`
until `PIN_C2` (and the count-c3 pin receipt) is re-pinned. A later round
applying D1–D4 must therefore land the counter edit and the re-pin together,
and re-score C2/C3 with fresh receipts.

## Report-only inconsistencies (no bytes changed)

1. `materialize` docstring (133–134) says "Returns **None** on refusal"; the
   code returns `False` (138) and all callers test `is False`. Doc is wrong,
   behaviour is right.
2. Module docstring (47–49) says materialization happens "only … through the
   containment-asserted writer (G2)", but lines 169/179 write the pinned tool
   blobs with `write_bytes` directly, and 234/257 ignore `materialize`'s
   return. That is safe here — constant filenames under `--scratch`, bytes
   sha-gated, and drift/alias arms fail closed (missing file ⇒ tool exits
   non-zero ⇒ `attributed`/`ctrl` False) — but the sentence overstates the
   invariant and the two ignored returns leave no `containment:` token.

## Verification matrix (base = frozen bytes, var = D1–D4 applied)

Real lane, pinned revisions:

| rev | base | var | equal |
|---|---|---|---|
| `ac496c7c…` (freeze) | `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13`, exit 0 | identical | ✅ |
| `ddfb12fb…` (entering) | `C2=unmet … failed=entry,pins,rows,selftest,tool_absent,trees,trees_set`, exit 1 | identical | ✅ |

Fixture repo (`$D`, all commits inside it), same pattern:

| commit | arm exercised | base/var output |
|---|---|---|
| `a30a462` | frozen-subset copy | `C2=met … claims=13 files=6 spans=13`, exit 0, identical |
| `b256182` | ec tool sha drift → `tool_sha`, selftest skipped, 13 × `tree:*:tool` | `C2=unmet … failed=entry,pins,rows,selftest,tool_sha,tree:h00…:tool,…,trees`, exit 1, identical |
| `cd7a8d4` | + scan tool sha drift → `scan_tool_sha`, drift skipped | `… failed=drift,entry,pins,rows,scan,scan_tool_sha,selftest,tool_sha,tree:…:tool,trees`, exit 1, identical |
| `81dc2b3` | ENTRY deleted → `entry_absent` once | identical, `entry_absent_count=1` both |
| `8fd8999` | ENTRY + SOURCES deleted | identical, `entry_absent_count=1` both (no spurious token) |

Selftest: `C2_SELFTEST pass=8 fail=0`, exit 0 for both files.

## Tradeoff and stop condition

Accepted: four expression-level deletions plus one duplicated read removed
(4 boolean terms, 1 subprocess per `measure()` run, 2 lines moved); zero
observable change on 7 compared arm/rev points including every failure arm
the edits touch. Rejected: every remaining `failed.append`, the G2/G3
diagnostics, `run_pinned`'s gate and the `ran` short-circuits — the next
deletion would drop an execution-boundary guard or containment evidence, i.e.
harm the C3/operability axis. Net: `count-c2.py` is within 4 boolean terms of
minimal for its frozen predicate; no duplicate authority, no dead alternate
path, no unreachable adapter was found.

Scratch (`/fast/scratch/hyaku/mori-r60/Mo60SimplifierA1/`, incl. the fixture
repo) removed after this report was written; disk-guard clean throughout.
