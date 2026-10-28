# Mo60SimplifierA3 — de-weight audit of `tools/mori-entry-claims-check.py` (proposals only)

Seat: simplifier, leaf (no subagent dispatch). Round 60, L1 MoriR60.
Mode: read-only on the lane; all materialization inside
`/fast/scratch/hyaku/mori-r60/Mo60SimplifierA3/` (cleaned before yield).
No production file, registry, SCORECARD, LOG or lane VCS was written.

## 0. Pins and method

| item | value |
|---|---|
| freeze revision (contract) | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| lane tip observed during work | `b3c25613` |
| audited file | `tools/mori-entry-claims-check.py` |
| sha256 at worktree / at freeze / at tip | `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` (all three equal) |
| contract's frozen sha (contract.md:73-74) | same `cffe9f33…` |

Every claim below is pinned to `ac496c7c` / `cffe9f33`; the file did not move
during the audit (`sha256sum` re-run after all work still `cffe9f33…`,
`git status --porcelain tools/` empty).

**Semantic-reference proof device: unavailable.** `xd://lsp` is not mounted
(`read xd://lsp` → `No such tool: xd://lsp. Mounted devices: ast_edit, debug,
mcp__…`), so no `references` query was possible. Reference proof is therefore
the literal fallback: fleet-root text grep + AST dataflow, both recorded below.
Not presented as semantic proof.

Fleet-root reference scan (`grep -rln "mori-entry-claims-check\|eval_root"
--include=*.py --include=*.sh --include=*.md --exclude-dir=.git
--exclude-dir=node_modules` over `/home/vgpnk/Projects/shokunin`): 34 files
total, of which 27 are round-60 `w1/*.md` seat reports and exactly 7 are
non-report files — `tools/mori-entry-claims-check.py`,
`corpus/knowledge/entry-claims-hardening-r60.md`,
`.ufo/waves/round-60/{count-c2.py,count-c3.py,build-fixtures-r60.py,
contract.md,build-w1-spec.py}`. No importer (`import …mori_entry` /
`eval_root`) exists anywhere: the tool is consumed only as a subprocess CLI by
`count-c2.py`.

## 1. Premise adjudication (the seat prompt named three targets)

| # | premise | verdict | evidence |
|---|---|---|---|
| 1 | unused `copy_prefix` param | **CONFIRMED** (4 sites, not 1) | F1 below |
| 2 | unused imports | **FALSIFIED** | `pyflakes 4.0.3 Python 3.14.8`: exit 0, no output on the frozen file. Each import is live: `hashlib` L61, `json` L463/L472, `os` L254, `re` L52/56/57, `shutil` L438, `sys` L251/L478, `tempfile` L253, `Path` L46/L87/L253/L463 |
| 3 | "the artifacts-json CLI path unused by the counter" | **FALSIFIED** | `count-c2.py` *writes and passes* it twice: L308 `aj = scratch / "artifacts.json"`, L309 `aj.write_text(json.dumps(ARTIFACTS))`, L313 `"--artifacts-json", str(aj),` (entry arm) and L385-386 `"--artifacts-json", str(scratch / "artifacts.json"),` (hostile-tree arm). `count-c3.py` never invokes the entry tool at all (it runs `count-c2.py` against PoC repos). Inside the tool every `artifacts` use is live: L102-107, L143, L150, L174-175, L234-236, L463, L468 |

The premise that *is* true in that neighbourhood, and which the prompt's third
item seems to have aimed at, is a **different inert CLI surface: `--scratch`**
(F5). The frozen counter passes `--selftest --scratch <dir>` (L184-186) and the
tool accepts it and then discards it.

## 2. Findings with exact pointers

### F1 — `copy_prefix`: dead parameter + dead CLI option + stale docstring (CONFIRMED)
- L84-85 `def eval_root(root, entry_rel, copy_prefix, registry_rel, …)` — zero
  `Name` occurrences of `copy_prefix` inside the body. AST
  (walk of `FunctionDef.eval_root`): `unused params ['copy_prefix']`.
- L448 `opts = {"--root": None, "--entry": None, "--copy-prefix": None,` — the
  option is parsed into `opts` and then only ever *forwarded* to the dead
  parameter: L468 `opts["--root"], opts["--entry"], opts["--copy-prefix"] or "",`.
- L458-459 required-flag gate lists only root/entry/registry/artifacts-json —
  `--copy-prefix` is optional *and* meaningless.
- L32 docstring documents it: `--copy-prefix DIR/`.
- L307 selftest passes a hard-coded literal for it:
  `return eval_root(base, entry, "corpus/evidence/", regf, copies, 4, 2)`.
- Caller proof: `grep -rn "copy_prefix\|copy-prefix"` over the lane returns
  only this tool (L32/84/448/468) plus the round-60 dispatch text that names
  this seat. `count-c2.py` passes no such flag.

Residual meaning: the parameter encodes a *second* resolution convention
(copy path = prefix + artifact) that the implementation does not use — the
actual convention is "the artifacts JSON object keys are root-relative copy
paths" (L102-107, L234-236). Removing it deletes an alternate authority, not a
feature.

### F4 — `reg_rows` is a dead store (new; same class)
```
$ grep -n "reg_rows" tools/mori-entry-claims-check.py
199:    reg_rows = {}
220:            reg_rows[sid] = cells[1]
```
AST classification of every occurrence: `reg_rows -> [(199, 'store'),
(220, 'subscript-store-object')]` — never read. L199 initialises it, L219-220
(the leftover comment `# source cell names artifacts: keep the row's source
cell text` plus the assignment) fills it, and the real H4 binder pass
(L221-238) re-scans the registry independently and builds `binders`, never
`reg_rows`. The reason strings produced by the *rest* of that loop
(`rows:missing` L209, `rows:bad_row` L213, `rows:status` L216, `rows:usedby`
L218) are live and must stay — `h08-row-not-mined` / `h09-usedby-other` and
selftest check 8 depend on them.

### F5 — `selftest(scratch=None)` / `--scratch` is inert (new; the honest version of premise 3)
- L242 `def selftest(scratch=None):` — AST: `selftest … unused params
  ['scratch']`.
- L442-447 `main` parses `--scratch` and hands it to a function that ignores
  it: `scratch = None … return selftest(scratch)`.
- L34 docstring advertises it: `--selftest [--scratch DIR]`.
- Empirical inertness proof (both tools, TMPDIR set to seat scratch):
```
$ python3 tools/v0-frozen/tool.py --selftest --scratch $PWD/scratchprobe/st
ENTRYCLAIMS_SELFTEST pass=13 fail=0
probe-dir-exists=NO
```
The scratch root actually used is `tempfile.mkdtemp(prefix="mori-r60-ecst-",
dir=os.environ.get("TMPDIR") or None)` (L253-254) and is removed in `finally`
(L438). Containment today comes solely from `count-c2.run_pinned` setting
`env={"TMPDIR": str(scratch)}` (count-c2.py L151) — not from this option.

### F6 — no-op statement (new; cosmetic)
L471 `stats["files"] = stats.get("files", 0)` — `eval_root` initialises
`stats = {"claims": 0, "files": 0, …}` (L89) and every return path preserves
the key (L94, L239), so the assignment can never change a value.

### F7 — unused loop binding (new; cosmetic)
L149 `for kid, _t, quote, cfile, kind, n, pin in claims:` binds `pin`, never
used in that loop (the pins loop at L173-186 uses its own `pin`). Other
`_`-prefixed bindings at L126/327/352/366/382/393/401/412/421/427/433 are
deliberate and correct.

## 3. Proposals (deletions only; no behaviour change claimed untested)

All four are one change set; each was materialised and re-verified (see §4).

**P1 — drop `copy_prefix` (F1).** Edits: L84-85 drop the parameter; L307 drop
the literal (`eval_root(base, entry, regf, copies, 4, 2)`); L448 drop
`"--copy-prefix": None,`; L468 drop `opts["--copy-prefix"] or "",`; L32 drop
` --copy-prefix DIR/` from the usage block.
Caller proof: §0 grep — no consumer passes or sets it; the counter's argv is
fixed at count-c2.py L310-316 / L382-388.

**P2 — drop the `reg_rows` dead store (F4).** Edits: delete L199; delete
L219-220 (comment + assignment). Keep every `reasons.append("rows:…")` in that
loop. Caller proof: never-read (grep + AST), and the H4 verdict is produced by
the independent `binders` scan.

**P3 — drop the inert `--scratch` (F5).** Edits: `def selftest():` (L242);
L442-447 → `if "--selftest" in argv: return selftest()`; L34 drop
` [--scratch DIR]`. Caller tolerance proof: `count-c2.py` L184-186 keeps
passing `--selftest --scratch <path>`; the tool's option loop (L451-457) skips
unknown tokens one at a time, so the extra pair is harmless — verified
empirically on the edited variant (§4, `v3 … --selftest --scratch … exit=0`).
Alternative (not recommended, recorded for the L1 only): *honour* the option
by using it as `mkdtemp(dir=scratch)`. That adds an authority rather than
removing one, and the contract already routes containment through TMPDIR
(tool docstring L36-37 "writes only inside its own selftest scratch.
Honors TMPDIR", contract.md:109-110 G2, count-c2 L151).

**P4 — drop L471 no-op (F6).**

**P5 — optional, medium risk: remove the duplicate threshold authority.**
`--min-claims`/`--min-files` default to `"10"`/`"3"` (L450) while
`count-c2.py` owns the same numbers as `MIN_CLAIMS = 10` / `MIN_FILES = 3`
(L56-57) and always passes them explicitly. The tool defaults are therefore
never exercised by any existing caller. If a future round wants one authority
for the thresholds, add both keys to the L458-459 required gate and drop the
defaults from L450 and the usage block. **Risk:** changes the exit-2 surface
for a hypothetical caller that omits them; no such caller exists today. I
recommend deferring this one and taking P1-P4, which are provably inert.

### Declined (recorded so nobody re-opens them as "duplication")
- The two registry scans (L200-220 sid-bound checks vs L224-233 binder scan)
  look mergeable but are **not** a deletion: loop 1 takes the *first* matching
  row per frontmatter SID (`break` at L207) while loop 2 accepts *any* row
  whose used-by is this entry. Merging changes verdicts on a registry with
  duplicate SIDs, i.e. it is a predicate change, not de-weighting.
- `span_of`'s `q` for the `line` kind (L64-78) is not dead: the byte-equality
  check at L185 is what enforces "quote equals the whole cited line".

## 4. Evidence — retained behaviour

Harness: `/fast/scratch/hyaku/mori-r60/Mo60SimplifierA3/equiv_driver.py`
(materialises `corpus/knowledge/wave-settlement-artifacts-r59.md`,
`corpus/SOURCES.md` and the 6 copies at `ac496c7c` into a root, materialises all
13 `trees-c2h/*` roots, writes `artifacts.json` = the counter's `ARTIFACTS`
map, then runs **4 tool versions × 14 roots** and compares stdout bytes and
exit codes; read-only on the lane, all writes under the seat scratch).

```
roots: 14 tools: 4 mismatches: 0
real-entry             v0-frozen  exit=0 ok=True  claims=13 spans=13 reasons=[]
tree:h00-good-control  v0-frozen  exit=0 ok=True  claims=10 spans=10 reasons=[]
tree:h01-semantically-empty exit=1 ok=False reasons=['grammar:…', 'text:short=K1', 'text:dup=K1=K2']
tree:h02-malformed-claim    exit=1 ok=False reasons=['grammar:…']
tree:h03-line-offset-alias  exit=1 ok=False spans=9 reasons=['distinct:dup_span=K1=K10']
tree:h04-blank-quote        exit=1 ok=False reasons=['span:blank=K1']
tree:h05-short-quotes       exit=1 ok=False claims=4 reasons=['claims_min:4','files_min:1','span:short=K1',…]
tree:h06-degenerate-text    exit=1 ok=False spans=2 reasons=['text:short=K1',…,'text:dup=K1=K3']
tree:h07-single-row         exit=1 ok=False reasons=['rows:missing=S902',…,'rows:binding=…r55.json']
tree:h08-row-not-mined      exit=1 ok=False reasons=['rows:status=S901',…]
tree:h09-usedby-other       exit=1 ok=False reasons=['rows:usedby=S901',…]
tree:h10-stale-pin          exit=1 ok=False reasons=['pin:1','pin:2','pin:3']
tree:h11-wrong-line         exit=1 ok=False reasons=['span:1']
tree:h12-no-frontmatter     exit=1 ok=False reasons=['frontmatter:source',…]
```
Every variant reproduces the frozen expect table exactly (`h00` ok, the other
twelve fail on their designated reason classes), and the real r59 entry stays
`ok=True claims=13 spans=13` — i.e. no false negative is introduced and no
hostile tree is wrongly passed.

Selftest / lint parity (TMPDIR = seat scratch):
```
v0-frozen            | lines=478 | 'ENTRYCLAIMS_SELFTEST pass=13 fail=0' | rc=0 | pyflakes=clean
v1-no-copy-prefix    | lines=477 | 'ENTRYCLAIMS_SELFTEST pass=13 fail=0' | rc=0 | pyflakes=clean
v2-no-reg-rows       | lines=474 | 'ENTRYCLAIMS_SELFTEST pass=13 fail=0' | rc=0 | pyflakes=clean
v3-no-inert-scratch  | lines=469 | 'ENTRYCLAIMS_SELFTEST pass=13 fail=0' | rc=0 | pyflakes=clean
```
`v3` is P1+P2+P3+P4 together: **478 → 469 lines, 18950 → 18461 bytes**,
9 net lines. Its sha is `348d8f6d81da0a463aa7d2cd49e993a23534ef893face9faaaac4fae499e8a08`
(candidate freeze value *if* the L1 ever adopts the set). The counter's frozen
token `ENTRYCLAIMS_SELFTEST pass=13 fail=0` (count-c2.py `EXPECT_SELFTEST`) is
still produced, and
`v3 --selftest --scratch <dir>` exits 0 with the same summary while creating
no directory at `<dir>` — the exact argv the frozen counter uses.

## 5. Precondition for any adoption

The tool is *frozen and pinned*: contract.md:73-74 and `count-c2.PIN_EC`
(`cffe9f33…`), with G1 refusing to execute any other sha. So these proposals
cannot be applied inside round 60 without breaking C2/C3 (the pin must move and
the counters are immutable after scoring). Recommended landing: next round, as
one commit that (a) applies P1-P4, (b) updates `PIN_EC` and the contract sha to
the new value, (c) refreshes `corpus/knowledge/entry-claims-hardening-r60.md`'s
CLI description if it ever quotes the usage block (it does not today — grep
found no flag text there). No predicate, reason string, schema key or stat key
changes, so the C2 claim text needs no amendment.

## 6. Tradeoff / stopping point

Gain: four dead surfaces removed (one parameter convention, one dead dict,
one inert option, one no-op), 9 lines, zero verdict change; the tool stops
advertising a copy-resolution convention it does not implement and a scratch
option it does not honour. Cost: one pin re-freeze. I stopped at P5 because
the next deletion (the double registry scan) would remove behaviour, not
weight — that is the axis where further simplification stops being free.

## 7. Cleanup and side-effect statement

- Scratch `/fast/scratch/hyaku/mori-r60/Mo60SimplifierA3/` removed; the
  evidence tables and the `v3` diff above are copied into this report first
  (appendix).
- Lane untouched by this seat: `git status --porcelain tools/` empty and the
  tool sha is still `cffe9f33…` after all work. (`git status` does show
  `M corpus/lessons/round-60.md` — that is the concurrent C1 data landing
  described in the round context, not this seat; I wrote nothing under
  `corpus/`.) No `__pycache__`/scratch artifact was created by this seat
  inside the lane (the ignored
  `tools/__pycache__/mori-entry-claims-check.cpython-314.pyc` is not mine — a
  main-script run never writes a `.pyc`; `__pycache__/` is gitignored at
  `.gitignore:3`).
- No commits, no VCS mutation, no fleet/sibling writes, no pacman, no tool
  installs (pyflakes 4.0.3 was already present at `~/.local/bin/pyflakes` and
  was used read-only).

## Appendix — proposed diff (v3 = P1+P2+P3+P4 vs frozen `cffe9f33`)

```diff
--- tools/v0-frozen/tool.py	2026-10-28 13:17:10.333518527 -0300
+++ tools/v3-no-inert-scratch/tool.py	2026-10-28 13:17:10.338796941 -0300
@@ -29,9 +29,9 @@
 Exit 0 iff ok.  Usage errors exit 2.
 
 Usage:
-  mori-entry-claims-check.py --root DIR --entry REL --copy-prefix DIR/
+  mori-entry-claims-check.py --root DIR --entry REL
     --registry REL --artifacts-json FILE --min-claims N --min-files F
-  mori-entry-claims-check.py --selftest [--scratch DIR]
+  mori-entry-claims-check.py --selftest
 
 Read-only over the root it is given; writes only inside its own selftest
 scratch.  Honors TMPDIR; carries no absolute host path.
@@ -81,7 +81,7 @@
     return (n, n + len(q))
 
 
-def eval_root(root, entry_rel, copy_prefix, registry_rel, artifacts, min_claims,
+def eval_root(root, entry_rel, registry_rel, artifacts, min_claims,
               min_files):
     """Evaluate one entry under root.  Returns (ok, reasons, stats)."""
     root = Path(root)
@@ -196,7 +196,6 @@
     except OSError:
         reg = None
         reasons.append("rows:sources_absent")
-    reg_rows = {}
     if reg is not None:
         for sid in sorted(sids):
             hit = None
@@ -216,8 +215,6 @@
                 reasons.append("rows:status=%s" % sid)
             if cells[10] != entry_rel:
                 reasons.append("rows:usedby=%s" % sid)
-            # source cell names artifacts: keep the row's source cell text
-            reg_rows[sid] = cells[1]
     # H4: per-copy row binding. A copy is bound when some registry row that
     # is mined, used-by exactly this entry, and 11 cells wide names that
     # copy's .ufo artifact path in its source cell.
@@ -239,7 +236,7 @@
     return (len(reasons) == 0), reasons, stats
 
 
-def selftest(scratch=None):
+def selftest():
     passed = failed = 0
 
     def chk(name, cond):
@@ -304,8 +301,7 @@
                                               pin(rel)))
 
         def run():
-            return eval_root(base, entry, "corpus/evidence/", regf, copies,
-                             4, 2)
+            return eval_root(base, entry, regf, copies, 4, 2)
 
         # 1: good entry — 4 claims on 4 distinct line spans
         write_entry([cl(1, c1rel, 2, ' "seats": 64-AAAA,'),
@@ -440,12 +436,8 @@
 
 def main(argv):
     if "--selftest" in argv:
-        scratch = None
-        i = argv.index("--selftest")
-        if "--scratch" in argv:
-            scratch = argv[argv.index("--scratch") + 1]
-        return selftest(scratch)
-    opts = {"--root": None, "--entry": None, "--copy-prefix": None,
+        return selftest()
+    opts = {"--root": None, "--entry": None,
             "--registry": None, "--artifacts-json": None,
             "--min-claims": "10", "--min-files": "3"}
     i = 0
@@ -465,10 +457,9 @@
         print("artifacts_json unreadable")
         return 2
     ok, reasons, stats = eval_root(
-        opts["--root"], opts["--entry"], opts["--copy-prefix"] or "",
+        opts["--root"], opts["--entry"],
         opts["--registry"], artifacts, int(opts["--min-claims"]),
         int(opts["--min-files"]))
-    stats["files"] = stats.get("files", 0)
     print(json.dumps({"schema": SCHEMA, "ok": ok, "reasons": reasons,
                       "stats": stats}))
     return 0 if ok else 1
```

Diff totals: 8 hunks, 17 removed / 8 added lines (net −9, matching 478 → 469); v3 sha256 `348d8f6d81da0a463aa7d2cd49e993a23534ef893face9faaaac4fae499e8a08`.
