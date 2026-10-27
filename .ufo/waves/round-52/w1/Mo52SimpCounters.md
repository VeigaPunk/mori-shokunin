# Mo52SimpCounters — dead weight in the round-52 counters and C1 controls

Seat: reader of the four frozen Python instruments of round 52. The counters are frozen (contract §Separability,
round-51 closure routed defect 6), so **nothing in the lane was edited**: every deletion below was applied and
measured on a scratch copy, and the result is a proposal for the successor counter, not a change to this round.

## Frozen pin of the audited bytes

All four files have exactly one commit (`d3a8ea59`, the freeze) and their working-tree bytes equal
`evidence/freeze-sha256.txt`:

```
$ git log --oneline -- .ufo/waves/round-52/count-c1.py .ufo/waves/round-52/count-c2.py \
      .ufo/waves/round-52/controls/c1-controls.py .ufo/waves/round-52/controls/c1-data.py
d3a8ea59 round-52: freeze — contract, C1/C2 counters with selftests, C1 controls and receipts, ...
$ sha256sum .ufo/waves/round-52/count-c1.py .ufo/waves/round-52/count-c2.py \
      .ufo/waves/round-52/controls/c1-controls.py .ufo/waves/round-52/controls/c1-data.py
e864922790451b4026be784d5344d9a06827b251ed3c81bfe26b1c559ee3c300  .ufo/waves/round-52/count-c1.py
0a9ec2ffdd85dd1a2be13f359ad82c0f45f99b781d73f9bcf3fa098d7f3bb74a  .ufo/waves/round-52/count-c2.py
1eb6087fc4e8358c0d136ed29d3b3470fc6b220a4c4e6cd64472bebd5bb14213  .ufo/waves/round-52/controls/c1-controls.py
ff9500a5a2d4bb1e1f372119f2761a3bdd6a98c58af0f025ada77609331ef120  .ufo/waves/round-52/controls/c1-data.py
```

Every line number below is a line of those frozen bytes (`count-c1.py` 786 lines, `count-c2.py` 515,
`c1-controls.py` 73, `c1-data.py` 136).

## Axes named before measuring

A1 dead statements/parameters/constants removed · A2 frozen semantics preserved (selftest tally and real tally
line byte-identical) · A3 duplicated helpers retired · A4 the record stays reproducible (no receipt or predicate
text changes) · A5 no false positive (a live symbol called dead is a defect in this report).

## Method

1. Static: `pyflakes 4.0.3` (no finding), `ruff 0.17.2 --select F,E7,E9` (only `E741` ambiguous `l`, style, not
   dead weight), `vulture 2.16 --min-confidence 30` (no finding), and an AST audit of every module-level
   definition, every function parameter and every import (no unreferenced symbol, no unread parameter).
2. Dynamic: `coverage.py 7.17.0` (line + branch) over each counter's own `--selftest` plus one real run at
   `8524904adb25e44f24d9f25aac7eae909625c18c`, in a frozen-byte copy of the tree.
3. Proof per candidate: patch a scratch copy, re-run `--selftest` and the real run, require the selftest tally
   unchanged and the real output byte-identical (`diff`), with the flag-`rc` unchanged.

## Baselines reproduced from the scratch copies (they agree with the frozen receipts)

```
$ cd $S/base && python3 .ufo/waves/round-52/count-c1.py --selftest        # rc=0
C1_SELFTEST pass=42 fail=0                     # = evidence/selftest-c1.txt
$ python3 .ufo/waves/round-52/count-c2.py --selftest                      # rc=0
C2_SELFTEST pass=45 fail=0                     # = evidence/selftest-c2.txt
$ python3 .ufo/waves/round-52/count-c1.py 8524904a… --repo $S/clone --fleet-repo <fleet> --scratch $S/c1run-base
C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 \
lane_writes=0 manifest=6209bdb8e400 rev=8524904adb25e44f24d9f25aac7eae909625c18c      # rc=0
$ python3 .ufo/waves/round-52/count-c2.py 8524904a… --repo $S/clone
C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok \
entailed=0 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment      # rc=1
$ python3 .ufo/waves/round-52/count-c2.py --hashes 8524904a…
28 lines; all 28 hash= values identical to evidence/c2-hashes-at-data.txt              # rc=0
```

`diff` of the 42 `item` lines and the tally line against `evidence/c1-at-data.txt`, and of the tally line against
`evidence/c2-at-data.txt`: identical. So the scratch tree measures the same thing the receipts measured.

## Coverage of the frozen bytes (selftest + one real run)

```
count-c1.py  603 stmts  42 miss  224 branch  30 partial  91%
  missing: 129->144, 131, 138->140, 179-180, 192-193, 209, 231-232, 234, 237, 244-245, 256, 261, 328-329,
  345, 371->376, 374->373, 376->378, 394->396, 425, 442, 446, 475-476, 480-482, 490, 494, 496-498, 504,
  506-507, 543, 550-551, 554-558, 565-566, 574->576, 785->exit
count-c2.py  388 stmts  20 miss  118 branch   6 partial  94%
  missing: 74, 88-92, 222->226, 292-299, 306, 308-309, 314-316, 514->exit
```

Exactly **one** unexecuted statement in `count-c1.py` is *unreachable* (446, see S1); 88-92 in `count-c2.py` are
unreachable for the frozen data (see S4). Every other miss is a defensive or predicate-permitted path that the
corpus and the selftest simply never enter — retained, listed under "Unexercised but reachable".

## Candidates proved on scratch copies

### S1 — `count-c1.py:445-446`, the `axes` failure append (MED) — 2 lines

```python
    if len(axis_items) != len(AXES):
        failed.append("axes")
```

`check_axes` (176-213) appends exactly one item per `AXES` entry and has no early `return`, so
`len(axis_items) == len(AXES) == 6` for every input; the branch cannot be taken. Coverage agrees: line 446 is in
the never-executed set. The invariant it guards is already asserted where it can break — the selftest's
`honest_met` check requires `"axes=6"` in the tally line.

Proof: patched copy, `C1_SELFTEST pass=42 fail=0` (unchanged); real run `rc=0`, output byte-identical
(`diff` clean, 42 `item` lines + the same `C1=met items=42 …` line, `lane_writes=0`).

### S2 — `count-c2.py`, the `copies` parameter and its redundant re-test (MED) — net 1 line, 4 sites

- 159 `def evaluate(read, rev, entry_path=None, copies=None, ls=None):` — no caller passes it (317 and 389 are
  the only `evaluate` calls; both pass `entry_path`/`ls` only).
- 163 `copies = copies or COPIES` — a rebinding that always yields the module constant.
- 168 / 222 — the two readers of the dead binding, becoming `COPIES`.
- 226 `row_ok = bool(srow and len(srow) == 11 and …)` — the first conjunct repeats the guard on 221; with `url`
  initialised `None` on 220 and set only inside that guard, `url is not None` already short-circuits the `None`
  and short-row cases.

Proof: patched copy, `C2_SELFTEST pass=45 fail=0`; real run `rc=1`, output byte-identical (same
`C2=unmet claims=28 … failed=entailment` line). The selftest's `indented_row_ok` / `code_indented_row_unmet`
checks still pass, i.e. the 11-cell and the non-parsed (4-space indent → `srow is None`) shapes both behave.

### S3 — `count-c2.py` selftest, three dead knobs (LOW) — 0 net lines

- 361 `def build(claim_rows=None, drop=None, claims=None, votes="all", **kw):` — `drop` is never passed
  (42 call lines of `build(`, the only `drop=` in the file is this signature; they name
  `claim_rows`/`claims`/`status`/`opened`/`used`/`indent`/`votes`), so the branch on 374-375
  (`if drop != sids[u] else {"status": "queued"}`) is dead; the surviving dict filter is the one always taken.
- 332 `def quote_from(url, needle, n=8):` — all 15 calls pass `n`.
- 453 `echo = [q for u, q in qs]` — `u` is bound and never used.

Proof: patched copy, `C2_SELFTEST pass=45 fail=0`; real run byte-identical. Note the `status="queued"` *case* is
not lost: 425 `build(status="queued")` still drives `row_not_mined_unmet` through the keyword filter.

### S4 — `count-c2.py`, the HTML seam (MED, with the tradeoff named) — 10 lines

`import html` (35), `normalise()` (87-92), the `kind` element of the five `COPIES` tuples (55, 57, 59, 61, 63),
and the two `kind == "html"` ternaries (172, 326-327). All five frozen copies carry kind `"text"`, so `normalise`
is never called: coverage shows 88-92 unexecuted across selftest and real run, and `grep 'kind == "html"'` finds
only 172 and 329.

Proof: patched copy, `C2_SELFTEST pass=45 fail=0`; real run `rc=1`, output byte-identical.

Tradeoff, stated rather than hidden: this is the only HTML path in the lane. P-C2 says only "occurs (whitespace
collapsed) in the committed copy", and every committed copy is raw text, so the seam is unreachable weight today
— but a later source fetched as rendered HTML needs those 6 lines back. **Recommendation: delete at the
successor** (a new kind is a one-line data change when it is actually needed), and record in that round's
contract that no HTML source exists.

### Net of S1–S4 (all four applied to their files)

`count-c1.py` 786 → 784; `count-c2.py` 515 → 504 (combined variant measured: `C2_SELFTEST pass=45 fail=0`,
real output byte-identical, `rc=1`). 13 lines, four dead parameters/knobs plus one redundant guard, one
unreachable branch, one unreachable helper — and no measured line, tally token or exit code changes.

Combined `count-c2.py` patch (the successor's draft; `a/` `b/` prefixes stand for
`.ufo/waves/round-52/count-c2.py`):

```diff
--- a/.ufo/waves/round-52/count-c2.py
+++ b/.ufo/waves/round-52/count-c2.py
@@ -32,7 +32,6 @@
 kernels or about this host's sysctl values.
 """
 import hashlib
-import html
 import os
 import re
 import subprocess
@@ -49,18 +48,18 @@
 MIN_CLAIM_WORDS = 6
 MIN_BEYOND = 3
 MIN_WORDS, MAX_WORDS = 6, 25
-# url -> (committed copy, sha256 of the copy fetched 2026-10-26, kind)
+# url -> (committed copy, sha256 of the copy fetched 2026-10-26)
 COPIES = {
     "https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/mm/overcommit-accounting.rst":
-        (SRC_DIR + "overcommit-accounting.rst.v7.2", "767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f", "text"),
+        (SRC_DIR + "overcommit-accounting.rst.v7.2", "767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f"),
     "https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/vm.rst":
-        (SRC_DIR + "vm.rst.v7.2", "bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce", "text"),
+        (SRC_DIR + "vm.rst.v7.2", "bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce"),
     "https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c":
-        (SRC_DIR + "util.c.v7.2", "e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c", "text"),
+        (SRC_DIR + "util.c.v7.2", "e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c"),
     "https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mman.h":
-        (SRC_DIR + "mman.h.v7.2", "d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058", "text"),
+        (SRC_DIR + "mman.h.v7.2", "d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058"),
     "https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/mmap.c":
-        (SRC_DIR + "mmap.c.v7.2", "449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545", "text"),
+        (SRC_DIR + "mmap.c.v7.2", "449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545"),
 }
 SPAN = re.compile(r"`([^`]+)`")
 
@@ -82,14 +81,6 @@
 def words_beyond(claim, quote):
     qw = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", quote))
     return len(set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", claim)) - qw)
-
-
-def normalise(text):
-    t = re.sub(r"<(script|style)\b.*?</\1\s*>", " ", text, flags=re.S | re.I)
-    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
-    t = re.sub(r"<[^>]+>", " ", t)
-    t = html.unescape(t)
-    return re.sub(r"\s+", " ", t)
 
 
 def parse_claims(entry_text):
@@ -156,20 +147,19 @@
     return None
 
 
-def evaluate(read, rev, entry_path=None, copies=None, ls=None):
+def evaluate(read, rev, entry_path=None, ls=None):
     entry_path = entry_path or ENTRY
     votes, authored = entail_votes(read, ls or (lambda d: []))
     entailed = dissent = 0
-    copies = copies or COPIES
     failed = []
     # pins
     norm = {}
     pins_ok = True
-    for url, (path, digest, kind) in copies.items():
+    for url, (path, digest) in COPIES.items():
         b = read(path)
         if b is None or hashlib.sha256(b.encode("utf-8", "surrogateescape")).hexdigest() != digest:
             pins_ok = False
-        norm[url] = normalise(b or "") if kind == "html" else normalise_text(b or "")
+        norm[url] = normalise_text(b or "")
     if not pins_ok:
         failed.append("pins")
     entry = read(entry_path)
@@ -219,11 +209,11 @@
             srow = row_cache[sid]
             url = None
             if srow and len(srow) == 11:
-                for u in copies:
+                for u in COPIES:
                     if u in srow[1]:
                         url = u
                         break
-            row_ok = bool(srow and len(srow) == 11 and url is not None and srow[7] == "mined"
+            row_ok = bool(url is not None and srow[7] == "mined"
                           and srow[8] == OPENED
                           and entry_path in [u.strip() for u in re.split(r"[,;]", srow[10])])
             if not row_ok:
@@ -323,13 +313,12 @@
     here = os.path.dirname(os.path.abspath(__file__))
     lane = os.path.dirname(os.path.dirname(os.path.dirname(here)))
     files = {}
-    for url, (path, digest, kind) in COPIES.items():
+    for url, (path, digest) in COPIES.items():
         with open(os.path.join(lane, path), "rb") as f:
             files[path] = f.read().decode("utf-8", "surrogateescape")
-    texts = {u: (normalise(files[p]) if k == "html" else normalise_text(files[p]))
-             for u, (p, d, k) in COPIES.items()}
+    texts = {u: normalise_text(files[p]) for u, (p, d) in COPIES.items()}
 
-    def quote_from(url, needle, n=8):
+    def quote_from(url, needle, n):
         t = texts[url]
         i = t.index(needle)
         return " ".join(t[i:].split(" ")[:n])
@@ -358,7 +347,7 @@
     def claim_text(i):
         return "observation number %d explains how the kernel estimate reads its counters" % i
 
-    def build(claim_rows=None, drop=None, claims=None, votes="all", **kw):
+    def build(claim_rows=None, claims=None, votes="all", **kw):
         rows = ["| claim | source | quote |", "|---|---|---|"]
         cl = []
         for i, (u, q) in enumerate(claim_rows or qs):
@@ -371,8 +360,8 @@
             "recheck: 180d — `curl -s https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c | sha256sum`", "",
             "## Claims", ""] + rows + [""])
         src = "\n".join(["| id | source |", "|---|---|"] + [
-            srow(u, sids[u], **({k: v for k, v in kw.items() if k in ("status", "opened", "used", "indent")}
-                                if drop != sids[u] else {"status": "queued"})) for u in urls])
+            srow(u, sids[u], **{k: v for k, v in kw.items() if k in ("status", "opened", "used", "indent")})
+            for u in urls])
         fl = dict(files)
         fl[ENTRY] = entry
         fl["corpus/SOURCES.md"] = src
@@ -450,7 +439,7 @@
     fl = build(claims=["the same claim repeated for every row of the table"] * 12)
     met, line = run(fl)
     check("breadcrumb_identical_claims_unmet", (not met) and "bad_rows=11" in line)
-    echo = [q for u, q in qs]
+    echo = [q for _, q in qs]
     fl = build(claims=[q + " here" for q in echo])
     met, line = run(fl)
     check("claim_echoes_quote_unmet", (not met) and "bad_rows" in line)
```

`count-c1.py` draft, the whole of S1:

```diff
--- a/.ufo/waves/round-52/count-c1.py
+++ b/.ufo/waves/round-52/count-c1.py
@@ -442,8 +442,6 @@
         failed.append("pins_floor")
     if boxes < MIN_BOXES:
         failed.append("boxes_floor")
-    if len(axis_items) != len(AXES):
-        failed.append("axes")
     met = not failed
     out = ["item %s %s expect=%s got=%s state=%s" % (k, re.sub(r"\s+", "_", name), re.sub(r"\s+", "_", want),
                                                      re.sub(r"\s+", "_", got), st)
```

## Duplication (measured; nothing deletable now, because both sides are frozen)

- `count-c2.py` and `round-51/count-c2.py`: **10 of 13 functions byte-identical** — `split_cells`,
  `normalise_text`, `words_beyond`, `normalise`, `parse_claims`, `claim_hash`, `sources_row`, `git_reader`,
  `git_lister`, `main` — 93 of 515 lines (18 %). Only `entail_votes`, `evaluate` and `selftest` differ.
- `count-c1.py` and `round-50/count-c1.py`: **4 of 20 functions byte-identical** — `split_cells` (85),
  `manifest_targets` (96), `bound_path` (228), `git` (460) — 34 of 786 lines (4 %).
- Inside round 52, the same two helpers are spelled twice: `split_cells` at `count-c1.py:85-89` (one-line
  conditional) and `count-c2.py:68-75` (if/else) — **0 disagreements over all 972 `|` lines** of SCORECARD,
  SHONEN, SOURCES, QUALITY, README and the C2 entry at `8524904a`; and whitespace collapse at `count-c1.py:92-93`
  (`ws`, strips) vs `count-c2.py:78-79` (`normalise_text`, callers strip) — equal after `.strip()` on all 4528
  non-blank lines of the same files.
- The control harnesses are *not* duplicated: `round-52/controls/c1-controls.py` shares no identical function
  with round-50's or round-51's (`sh`, `main` are new bodies); only the clone→commit→score pattern recurs.

Proposal for the successor (one convention, not a second one): a module beside the successor counter
(`.ufo/waves/round-NN/countlib.py`) holding `split_cells`, `collapse`, `claim_hash`, `TALLY`/`ANY_TALLY`, and the
`git show`/`git ls-tree` readers; the successor counter imports it, the frozen counters keep their own copies.
That retires 93+34 duplicated lines at the successor without touching a frozen byte. It is a **design decision
for round 53**, not a safe mechanical deletion: it adds an import dependency that a copied-to-scratch counter
would also need (the counters are today single-file by construction).

## Refuted candidates (hints from the seat brief, checked rather than assumed)

- `ws` is **live**: defined `count-c1.py:92`, called at 399 and 403 (locator arm).
- `LIVING` is **live**: defined `count-c1.py:69`, iterated at 325 (`check_living`).
- `HIDDEN` is **live**: defined `count-c1.py:79`, applied at 224 (`parse_shonen`) to the line with pins removed.
  It is not a duplicate of `TALLY`/`ANY_TALLY`: those parse a command's output at run time, `HIDDEN` detects a
  tally token left in the *document* after pins are blanked.
- `controls/c1-controls.py` and `controls/c1-data.py` have **no dead symbol**: every module constant, helper and
  part name is reached by `CONTROLS` or by `main`; AST audit finds no unreferenced definition and no unread
  parameter; pyflakes and vulture find nothing. The one redundancy is structural: `locator` is only ever run
  together with `axes` (five of the seven `CONTROLS` values carry `axes,locator`; `receipts-only` and
  `living-only` carry neither, and no value names `locator` alone). Merging them would make the
  `parts: axes,locator` header line in five frozen receipts (`evidence/control-c1-{axes-only,rewrite-in-place,
  delete-stale-pins,repeat-stale-tally,witness}.txt`) no longer literal — harm to A4 for no measured gain, so
  **not proposed**.

## Unexercised but reachable — retained, named, not called dead

- `count-c1.py:445-446` is the only unreachable statement (S1). The rest of the coverage misses are branches the
  predicate allows and this corpus does not enter: 179-180 (MANIFEST has no target for an axis), 192-193 (a row
  with ≠4 cells), 209 (no closure score for an axis), 231-232/234/237/244-245 (shlex/`argv` rejects in
  `bound_path`/`living_argv`), 256/261 (tally with no observation, pinned prefix ≠ observed), 328-329 (a living
  file absent), 345 (a living pin in `(N/M)` form — none exists today), 425 (SHONEN absent), 442 (`pins_floor`),
  543/550-551/554-558 (archive failure, timeout, prefix-less tally fallback — allowed by P-C1's living arm but
  unused), 565-566 (the lane-write printer, correctly silent), 129-140 partials in `axes_table`, 475-507 (usage
  and setup errors).
- `count-c2.py:74` (a table row without a trailing `|`), 221→226 false path (an S row that is not 11 cells),
  291-299 (`--hashes`; exercised separately, see below), 306 (`--entry` parse — no run passed `--entry`),
  307-316 (usage/setup errors).

These are cheap insurance against inputs the predicate names; deleting them would shrink the file and widen the
predicate's blind spots at once.

## Two named instrument limits found while proving (not fixes; round-53 items)

1. `count-c2.py`'s `--hashes` mode takes no `--repo`: `main` parses `--repo` only after the `--hashes` dispatch
   (300-306), while the `--hashes` branch (291-299) computes `repo` from `dirname⁴(__file__)` and cannot be
   pointed at a clone. Running the scratch copy read
   `C2_SETUP entry absent at 8524904a…` (rc=2) until the lane's own copy was run; the lane copy then printed the
   28 hashes identical to `evidence/c2-hashes-at-data.txt`. A successor should parse `--repo` before the
   `--hashes` dispatch (`count-c1.py:468-478` already does the equivalent).
2. `count-c1.py`'s selftest never enters `pins_floor` (442) although it enters `boxes_floor`: a probe with a
   SHONEN fixture carrying one pin and four boxes read `failed=mismatch,pins_floor` (reachable and correct), so
   the branch is a **test gap**, not dead code. Same for 179-180, 192-193, 209 and 425 (see above): P-C1's
   floors and edges have no selftest case while boxes does.

## Scratch, tools, host state

- Scratch (removed after the outputs above were copied into this report):
  `/fast/scratch/hyaku/mori-r52/Mo52SimpCounters/{tmp,clone,base,patch,venv,out,verify}` — one
  `git clone --shared` of
  the lane (`rev-parse --show-toplevel` asserted equal to the clone dir, detached at `8524904a…`), frozen-byte
  copies of the four files plus the five `corpus/evidence/sources-r52/` copies, `TMPDIR` inside the scratch.
  Disk guard read at start: `/fast/scratch/hyaku` 26 % used, 601.5 G free; no ENOSPC.
- Tooling: no pacman transaction (host-wide pause respected). Installed `coverage.py 7.17.0` into a scratch venv
  with `uv pip install --python $S/venv/bin/python coverage` (uv channel, scratch-only, reason: line and branch
  coverage to separate unreachable statements from unexercised ones). `ruff 0.17.2`, `vulture 2.16`,
  `pyflakes 4.0.3` were already at `~/.local/bin` and were run read-only; nothing was written to any PATH
  directory.
- Lane state: I wrote only this report. The lane working tree was being edited by other seats throughout the
  measurement; at the close check (21:29:00) `git status --porcelain` listed eight modified tracked files
  (`LOG.md` 21:27:28, `SKILL.md` 21:27:28, `corpus/QUALITY.md` 21:27:00, `SCORECARD.md` 21:27:34,
  `corpus/README.md` 21:27:34, `corpus/SOURCES.md` 21:25:49,
  `corpus/knowledge/overcommit-commit-limit-r52.md` 21:26:22, `SHONEN.md` 21:28:50) plus new untracked
  `corpus/lessons/round-51-erratum.md`, `corpus/lessons/round-52.md` and
  `.ufo/waves/round-52/r39-conform-selftest.sh`. None of it is mine, and `sha256sum -c` against
  `evidence/freeze-sha256.txt` still read OK for all four audited files at close. Every measurement here reads
  the committed revision through `git show` from a clone, so those in-flight edits enter no number above.

## Named limits of this audit

- Coverage says "not executed by the selftest plus one real run at `8524904a`"; by itself that is not
  unreachability. S1 and S4 rest on a construction argument (one item per axis; five literal `"text"` kinds) on
  top of the coverage, and both were also proved by patching and re-running.
- The real-run comparison uses `--repo <clone at 8524904a>`, so it proves the patch does not change the
  measurement; it does not re-argue P-C1/P-C2 themselves.
- "Byte-identical function" is a text measure of duplication, not proof that two instruments should share code;
  the import proposal is left as a decision with its cost stated.
- The seven C1 controls were not rebuilt (eight `--no-local` clones); the applier `c1-data.py` was audited
  statically instead, and no deletion is proposed for it.

## Findings

1. MED — `count-c1.py:445-446`: unreachable `axes` failure branch; deleting it leaves `C1_SELFTEST pass=42
   fail=0` and a byte-identical `C1=met items=42 …` line (S1).
2. MED — `count-c2.py:159,163,168,222,226`: the `copies` parameter is never passed and only rebinds `COPIES`; the
   `row_ok` guard re-tests the 221 guard. Deleting leaves `C2_SELFTEST pass=45 fail=0` and an identical real
   line (S2).
3. MED — `count-c2.py:35,55,57,59,61,63,87-92,172,326-327`: the HTML seam is unreachable for the five frozen
   `"text"` copies (coverage: 88-92 never executed). Deleting is proved neutral; it removes the only HTML path,
   so the successor should delete it deliberately (S4).
4. LOW — `count-c2.py:332,361,374-375,453`: selftest-only dead knobs (`quote_from`'s `n=8` default, `build`'s
   `drop` argument and its `{"status": "queued"}` branch, the unused comprehension variable `u`) (S3).
5. MED — `count-c2.py` vs `round-51/count-c2.py`: 10 byte-identical functions, 93 of 515 lines; and
   `count-c1.py` vs `round-50/count-c1.py`: 4 byte-identical functions, 34 of 786 lines. A shared
   `countlib.py` at the successor retires 127 duplicated lines in one move.
6. LOW/MED — `count-c1.py:85-89` vs `count-c2.py:68-75` (`split_cells`, two spellings) and `count-c1.py:92-93`
   vs `count-c2.py:78-79` (whitespace collapse with the `.strip()` in a different place): semantically identical
   on 972 table lines and 4528 text lines; they are the second convention inside one wave.
7. LOW — `count-c1.py:442`: the selftest never enters `pins_floor` (it does enter `boxes_floor`); a one-pin
   fixture reads `failed=mismatch,pins_floor`, so this is a selftest gap for a frozen floor, not dead code.
8. LOW — `count-c1.py:179-180,192-193,209,425`: the selftest has no case for "MANIFEST target absent", "row with
   ≠4 cells", "no closure score" or "SHONEN absent"; all four branches are correct by reading and never executed
   by `--selftest`.
9. LOW — `count-c2.py:291-299`: `--hashes` cannot be pointed at a clone (no `--repo`); a scratch copy reads
   `C2_SETUP entry absent at 8524904a…` (rc=2). The lane copy reproduces the 28 frozen hashes.
10. LOW — `count-c2.py:74` and `count-c1.py:554-558,261,345`: predicate-permitted branches the corpus never
    enters (row without trailing `|`, prefix-less tally, prefix mismatch, `(N/M)` living pin). Retain; deleting
    them would silently widen the predicates' blind spots.
11. LOW — `controls/c1-data.py:88,111-112` (`locator` part): no control runs it without `axes`, but merging
    changes the `parts:` header of five frozen receipts. Not proposed.
12. LOW/INFO — the lane working tree was being edited by other seats while this seat measured (final check
    21:29:00: ` M LOG.md`, ` M SCORECARD.md`, ` M SHONEN.md`, ` M SKILL.md`, ` M corpus/QUALITY.md`,
    ` M corpus/README.md`, ` M corpus/SOURCES.md`, ` M corpus/knowledge/overcommit-commit-limit-r52.md`; new
    untracked `corpus/lessons/round-51-erratum.md`, `corpus/lessons/round-52.md`,
    `.ufo/waves/round-52/r39-conform-selftest.sh`). None of it was written by this seat, and the four audited
    files still matched `evidence/freeze-sha256.txt` at close; every number above comes from the committed
    revision `8524904a` through a clone.
