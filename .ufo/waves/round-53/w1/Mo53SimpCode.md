# Mo53SimpCode — dead-weight pass over count-c1.py, count-c2.py, controls/c1-data.py, controls/controls.py, tools/mori-commit-runway.py

Seat: Mo53SimpCode (simplifier, leaf). Round 53, wave w1. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scratch: `/fast/scratch/hyaku/mori-r53/Mo53SimpCode/` (removed at the end; everything cited here is copied in).
Nothing in this report changes a predicate, a counter, a control, a floor or a kill rule. The counters and the
control builder are frozen: every deletion there is a **proposal for a successor**, proven on scratch copies.
The tool is data: the three tool deletions are marked **safe now**.

## Axes

1. bytes of dead code (unused bindings, unreachable fallbacks, dead files written, always-empty knobs);
2. authorities for one fact (exit-code literals, vocabulary literals, duplicated constants);
3. zero observable change (identical stdout/stderr/exit for every arm the receipts use, and identical applied
   trees for the control builder).

A move was kept only when it improved 1 or 2 with 3 held exactly.

## Bytes analysed

Data commit `2a4213bf8da72f7cd78189baa5bb9be825dca1df`; each file extracted with
`git show 2a4213bf:<path>` and compared with the working tree:

| file | data bytes (sha256) | working tree when I read it |
|---|---|---|
| `.ufo/waves/round-53/count-c1.py` | `ebaff915…27005d` | identical |
| `.ufo/waves/round-53/count-c2.py` | `5684b69f…b168c5` | identical |
| `.ufo/waves/round-53/controls/c1-data.py` | `1833309c…909fd3` | identical |
| `.ufo/waves/round-53/controls/controls.py` | `f7ba7ac1…f1035a` | identical |
| `tools/mori-commit-runway.py` | `80cb1696…6156` (316 lines) | **rewritten during this wave**, landed as `b3c12340…ffe4` (435 lines) |

The tool was rewritten by another seat while this wave ran (`M tools/mori-commit-runway.py`, 316 → 347 → 429 →
435 lines, digests `335836d7…`, `82924be7…`, `b3c12340…` observed between 23:13 and 23:24) and landed mid-wave as
commit `fd86307a` (`round-53: data corrections from w1 — tool bounded reads/strict parsing/case-id guard (+3
cases, 5 hostile checks), …`). So the tool hunks were measured **twice**: first against the data bytes (the
claim's data), then against the landed bytes (`git show fd86307a:tools/mori-commit-runway.py`), and the section
below gives the landed line numbers. The four frozen files are byte-identical in both places, so their proposals
stand as written.

Tooling: `ruff 0.17.2` (`--select F401,F811,F821,F841,ARG,B006,B007,B008,B012,B015,B016,B018,B023,B025,PIE790,RET503,RET504,SIM201`
plus `F,ARG,B,SIM,PIE,RET,C4,PLR,PLC`), `vulture 2.16`, Python 3.14.8. Nothing installed, nothing upgraded
(no pacman, no uv tool). Scratch checks ran with `TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53SimpCode/tmp`.

## Method (what counts as proof here)

Every deletion was applied to a scratch copy of the file and then measured against the original with the same
command:

* **counters**: `--selftest` tally line, a real run at the data commit, a real run at a rev that carries the
  twelve-vote snapshot, `--scope`, `--fixtures`, and both usage-error paths;
* **control builder**: `c1-data.py --print-table`, `--print-rows`, and `apply()` in four part sets — the applied
  tree id (`git write-tree`) must match, and the tree must score identically under the frozen `count-c1.py`;
* **tool**: `--selftest` on the 23 data-commit cases and again on the landed 26-case file, every case
  materialised and run through both tools field by field, the failing-case report (two falsified expectations,
  plus one malformed case id on the landed bytes), the live host read on its stable fields, and the two
  usage-error paths.

Driver: `/fast/scratch/hyaku/mori-r53/Mo53SimpCode/verify.py` (in scratch, removed), 24 checks,
`VERIFY checks=24 fail=0` at the end. Two harness artefacts were found and normalised, not papered over:
`rev=` differs between two commits of the same tree (stripped before comparison), and `Committed_AS` moves
between two live reads (stable fields only, `committed_as_kb` / `headroom_kb` / `usable_kb` dropped).

## Deletions safe now — `tools/mori-commit-runway.py` (landed `fd86307a`, 435 lines)

```
--- tools/mori-commit-runway.py  (fd86307a, b3c12340)      +++ simplified
@@ -182,7 +182,7 @@  def unknown(notes)
-    return out, 2
+    return out, EXIT["COMMIT_UNKNOWN"]
@@ -356,6 +356,7 @@  def selftest(cases_file=None)
     failed: List[str] = []
     rejected = 0
     checks = 0
+    misses = 0
     try:
         seen = set()
         for n, case in enumerate(cases):
             ...
             if why is not None:
+                misses += 1
                 failed.append("case[%d]: malformed (%s)" % (n, why))
                 continue
             ...
             if bad:
+                misses += 1
                 failed.append("%s: %s" % (case["id"], "; ".join(bad)))
             ...
                 if not ok:
+                    misses += 1
                     failed.append("%s: unexpected result" % name)
@@ -383,3 +386,2 @@
-        print("MORI_COMMIT_RUNWAY_SELFTEST: FAIL %d/%d" % (checks - len([f for f in failed
-                                                                         if not f.startswith("matcher")]), checks))
+        print("MORI_COMMIT_RUNWAY_SELFTEST: FAIL %d/%d" % (checks - misses, checks))
@@ -394,7 +397,7 @@  class _Parser(argparse.ArgumentParser)
     def error(self, message: str) -> None:
         print(json.dumps({... "notes": ["usage: " + message]}))
-        sys.exit(2)
+        sys.exit(EXIT["COMMIT_UNKNOWN"])
```

* **T1/T2 — one authority for "cannot evaluate = 2".** The value lives in three places in the landed file:
  `EXIT["COMMIT_UNKNOWN"]` (`:87`, never read), `unknown()`'s literal return (`:185`), and `_Parser.error`'s
  `sys.exit(2)` (`:397`). Reading the table entry instead of the two literals deletes the duplicate authority and
  *uses* the entry that was dead. Verdict/JSON/exit unchanged: usage error and bad `--page-kb` both still `rc=2`
  with byte-identical stdout, on the data bytes and on the landed bytes.
* **T3 — the FAIL numerator was derived by classifying a message.** `failed` mixes per-case reasons
  (`"<id>: <reason>"`), hostile-check reasons (`"<name>: unexpected result"`) and one matcher verdict
  (`"matcher: accepted a corrupted expectation"`), and the score was recomputed as
  `checks - len([f for f in failed if not f.startswith("matcher")])` (`:386-387`) — arithmetic coupled to the
  punctuation and prefix of messages this file also writes. Counting the three failure classes where they are
  appended removes the second bookkeeping. Proof of no change, landed bytes: `--selftest` prints the same
  `MATCHER: rejected 26/26 … PASS 31/31`; a cases file with two falsified expectations and one malformed case id
  prints the same four lines and ends `MORI_COMMIT_RUNWAY_SELFTEST: FAIL 24/27` (checked char for char); all 26
  landed cases diverge in 0 fields. On the data bytes the same hunk was `total - len([f for f in failed if ":" in
  f])` → `matched`, proven with `FAIL 21/23` on both sides.

Not dead there (so no T4): there is **no** unused import, constant, function or dead branch in either tool
version — AST scan for never-loaded top-level names returns only `annotations` (`from __future__`), ruff's
F401/F811/F821/F841/ARG/B007 arms are clean on both, and vulture's only hit is `_Parser.error` (60 % confidence),
which is a **false positive** (argparse calls `error()`); deleting it would break the JSON usage error.
`--cases` is likewise not dead: the SKILL registry row has documented `[--selftest [--cases FILE]]` since the
data commit and two wave seats (`Mo53SentC2Hostile`, `Mo53ExecC2Replay`) drive it. Both are recorded below as
rejected.

## Deletion proposals — frozen files (successor applies, in a new freeze)

### count-c1.py (data `ebaff915…`) — 4 changed lines

```
@@ -183,7 +183,7 @@  def evaluate(read, rev, d, ls=None):
-def evaluate(read, rev, d, ls=None):
+def evaluate(read, rev, d, ls):
@@ -186,7 +186,7 @@
-    for path, (copy, digest, url) in V73.items():
+    for path, (copy, digest, _) in V73.items():
@@ -193,7 +193,7 @@
-    votes, proposed = final_votes(read, ls or (lambda _d: []))
+    votes, proposed = final_votes(read, ls)
@@ -338,7 +338,7 @@  def selftest()
-    for path, (copy, digest, url) in V73.items():
+    for copy in (spec[0] for spec in V73.values()):
```

* **C1a (`:183` + `:193`)** — dead fallback. `evaluate` has two call sites (`main` passes
  `git_lister(repo, full)`, `selftest.run()` passes a lister); neither can pass `None`, so the default and the
  `ls or (lambda _d: [])` branch are unreachable. This is the only deletion in the five files whose
  unreachability is static rather than exercised (see Limits).
* **C1b (`:186`)** — `url` is never read in `evaluate`'s loop (the URL is read later as `V73[path][2]`).
* **C1c (`:338`)** — `path`, `digest` and `url` are all unread in `selftest`'s loop; only `copy` is used.
  ruff B007 names exactly these three (and C1b) and nothing else in the file.

### count-c2.py (data `5684b69f…`) — 6 changed lines

```
@@ -100,7 +100,7 @@  def unknown():
-    out.update(schema=SCHEMA, verdict="COMMIT_UNKNOWN", enforced=None, limit_consistent=None)
+    out.update(schema=SCHEMA, verdict="COMMIT_UNKNOWN")
@@ -307,8 +307,8 @@  def live_check(tool)
-    c1, w1 = ref(before, vm, present, page_kb)
-    c2, w2 = ref(after, vm, present, page_kb)
+    _, w1 = ref(before, vm, present, page_kb)
+    _, w2 = ref(after, vm, present, page_kb)
@@ -545,3 +545,0 @@  def selftest()
-        memo = os.path.join(base, "memo.json")
-        with open(memo, "w") as f:
-            json.dump({fx["name"]: ref_for(fx) for fx in frozen_fixtures()}, f)
```

* **C2a (`:100`)** — `enforced=None` and `limit_consistent=None` restate what the comprehension on `:99`
  (`{k: None for k in FIELDS}`) has just written. The tool's own `unknown()` already has the trimmed form.
* **C2b (`:307-308`)** — `live_check` uses only `w1`/`w2`; the two `ref()` exit codes are never read.
* **C2c (`:545-547`)** — the selftest writes `memo.json` into its temporary tree and never opens it again: the
  memoriser arm is built from `REF_TOOL.replace(...)` (`memo_src`), not from the file. Deleted: a dead write, a
  dead variable, and 3 lines. `json` stays used (`main`, `compare`).

### controls/c1-data.py (data `1833309c…`) — 8 changed lines

```
@@ -45,2 +45,1 @@
-DISPOSITION = {}  # hash -> "changed"; every other row "holds"
 LEDGER = C.LEDGER
@@ -47,1 +46,1 @@
-R53 = "corpus/evidence/sources-r53/"
+R53 = C.SRC_DIR
@@ -116,2 +115,2 @@  def row_line(r)
-    return "| %s | ... | mined | 2026-10-26 | on-release | %s |" % (
-        sid, source, kind, tier, scope, anchor, teaches, used)
+    return "| %s | ... | mined | %s | on-release | %s |" % (
+        sid, source, kind, tier, scope, anchor, teaches, C.OPENED, used)
@@ -126,1 +125,1 @@  def table_lines(...)
-    out = ["| h | entry | status | source | quote | disposition |", "|---|---|---|---|---|---|"]
+    out = ["| " + " | ".join(C.HEADER) + " |", "|" + "---|" * len(C.HEADER)]
@@ -130,2 +129,1 @@
-        out.append("| %s | `%s` | %s | %s | `%s` | %s |" % (..., DISPOSITION.get(h, "holds")))
+        out.append("| %s | `%s` | %s | %s | `%s` | holds |" % (...))
@@ -156,1 +154,1 @@  apply(...) votes
-                    "RECHECK %s %s" % (h, DISPOSITION.get(h, "holds")) for h in sorted(d)) + "\n")
+                    "RECHECK %s holds" % h for h in sorted(d)) + "\n")
```

* **D1 (`:45`, `:131`, `:156`)** — `DISPOSITION` is assigned `{}` and nothing in the lane ever writes it
  (`grep -rn DISPOSITION` over `*.py/*.sh/*.md` finds only these three lines plus unrelated
  `mori-evidence-loss.py` hits). Both uses are `DISPOSITION.get(h, "holds")`, so both halves of a two-branch
  expression are dead: the value is always `"holds"`. The docstring does not mention the knob. Every control
  receipt agrees — all four C1 controls print `holds=46 changed=0`.
* **D2 (`:47`)** — `R53` retypes `count-c1.SRC_DIR`, which the same module already imports as `C`; `CG`, `LEDGER`
  and `T73` are already derived/labelled the same way.
* **D3 (`:116`)** — the row date retypes `count-c1.OPENED` (the counter is the authority for the opened date: a
  SOURCES row only counts if `srow[8] == OPENED`).
* **D4 (`:126`)** — the ledger header row retyped `count-c1.HEADER` as markdown text. If `HEADER` ever changes,
  the applier would emit a table the counter refuses. Building the row from `C.HEADER` deletes the second
  authority and cannot drift.

### controls/controls.py (data `f7ba7ac1…`) — no deletion candidate

ruff/vulture clean, AST scan clean, every one of `HERE/W/LANE/E/C1/C2/FREEZE_COPY/WRAPPER/WHAT` and every
function is loaded; the per-control `rmtree` is deliberate early space freeing, not redundancy. One LOW
duplicate authority found and **not** applied: `E = "20edafa5…"` retypes `count-c1.ENTERING`; deriving it means
loading a frozen counter module into the control builder for one literal, which costs more than the duplicate.
Reported, not changed.

## Rejected deletions (and why they would harm an axis)

* **`--cases` (tool)**: dead-looking in isolation, but documented in the SKILL registry row at the data commit and
  used by two wave seats for hostile-input probing. Deleting it would shrink operability to save one argument.
* **`EXIT["COMMIT_UNKNOWN"]` entry**: the entry is never read — but the right fix is to read it (T1/T2), not to
  delete it; deleting the mapping would leave the verdict table incomplete.
* **Shared `lane_root()` (count-c1 ≡ count-c2) and the tool's `parse_cpulist`/`parse_vm_value` vs the counter's
  `parse_present`/`parse_int_file`**: deliberate duplication. The first keeps each counter runnable with the
  other claim's data reverted (contract §Separability); the second is what makes the fixture arm able to disagree
  with the tool at all (C2's named limit is that REF and the tool share an author, not that they share code).
  Factoring either would delete the arm, not the weight.
* **`c = dict(rows=0, …)` → literal (C408), `V73` two-step rebuild, `enforced`/`final_votes` shape, `_page_kb_default`'s
  unreachable `AttributeError`**: style or one-line cosmetics with no dead behaviour. Left alone.

## Verification receipts (scratch, both versions, same command)

```
c1 --selftest                     C1_SELFTEST pass=37 fail=0            (base and mod, rc=0)
c1 real, votes present (DREV)     C1=met   … voted=46 dissent=0        (base and mod, rc=0)
c1 real, at data (no votes)       C1=unmet … voted=0 dissent=0 failed=votes   (rc=1; matches evidence/c1-at-data.txt)
c1 --scope                        scope=46
c2 --selftest                     C2_SELFTEST pass=30 fail=0
c2 real at data                   C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0
                                  registry=ok live=ok rev=2a4213bf…      (matches evidence/c2-at-data.txt)
c2 --fixtures at DREV             80 lines, identical
c1-data --print-table             48 lines, identical (C.HEADER-built header, C.OPENED date, no DISPOSITION)
c1-data --print-rows              12 lines, identical
c1-data apply ledger,allheld,rows,votes        tree cc063ebbd7b5e6eb  score C1=unmet … status_ok=44 quote_ok=44 failed=quote,status
c1-data apply ledger,rows,votes,v72copies      tree f227e6f7f424411a  score C1=unmet … pins=bad held=46 failed=pins,quote,status
c1-data apply ledger,rows                      tree e108ea3fadea7114  score C1=met … voted=46
c1-data apply ledger,allheld                   tree 4e50bcf65303acd1  score C1=unmet … status_ok=44
tool --selftest                   MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23
tool on 23 frozen cases           0 differences (field-by-field, 15 fields + exit)
tool FAIL report (2 falsified)    MATCHER: rejected 23/23 · FAIL <id>: … · MORI_COMMIT_RUNWAY_SELFTEST: FAIL 21/23
tool live JSON (stable fields)    identical
tool usage / bad --page-kb        rc=2, identical stdout
VERIFY checks=24 fail=0
```

Same hunks re-measured on the landed bytes (`fd86307a`, 435 lines, `b3c12340…ffe4`):

```
selftest (26 cases + 5 hostile)   MATCHER: rejected 26/26 · MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31   (both, rc=0)
FAIL report (2 falsified + 1 malformed case id)   same four lines · MORI_COMMIT_RUNWAY_SELFTEST: FAIL 24/27
all landed cases through both     26 cases, 0 differing fields, 0 differing exit codes
usage error / bad --page-kb       rc=2, byte-identical stdout
TOOLCHECKS=5 fail=0
```

DREV = `55bc20fe9e32afa062c2e7efa78512644fdca747`, my scratch commit of the data tree plus a snapshot of the
twelve-vote directory (so the vote arm actually counts votes: `voted=46`). The all-held, v72-copies and no-votes
trees score exactly as the frozen receipts say, which is the point: the applier's output is unchanged, so the
controls it builds are unchanged.

## Preserved contract

`count-c1.py`'s verdict line, its `--scope`/`--selftest` output and exit codes; `count-c2.py`'s verdict line,
`--fixtures` lines, selftest tally and exit codes; `c1-data.py`'s table, rows and applied trees; `controls.py`
untouched; the tool's JSON fields, verdicts, exit codes, selftest lines and per-case behaviour. No predicate
sentence, threshold, floor, voter list, frozen URL, digest or date was touched, and the diff touches no line that
computes a reading.

## Mistake I made in this wave (disclosed; repaired by the owner's commit)

At 23:17:32 I created a scratch `tools/fixtures` **symlink** and then redirected a `git show` into
`…/fixtures/mori-commit-runway/cases.json` through it, which wrote **into the lane** and replaced another seat's
uncommitted 26-case fixture with the data commit's 23-case bytes. For ~20 minutes the working tree was
inconsistent: the hardened tool printed `MATCHER: rejected 23/23` / `MORI_COMMIT_RUNWAY_SELFTEST: PASS 28/28`
while its uncommitted SKILL row said `PASS 31/31`. I did not write to the lane again: I recorded the two
byte-identical scratch snapshots of the 26-case file that other seats held
(`3a1aef20…450623`, 28393 bytes, extra ids `unknown-memtotal-30-digits`, `unknown-cpulist-overlapping`,
`unknown-cpulist-above-ceiling`, in
`/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/wt/tools/fixtures/mori-commit-runway/cases.json` and
`/fast/scratch/hyaku/mori-r53/Mo53ExecPinCheckNoHarm/clone/tools/fixtures/mori-commit-runway/cases.json`) and
messaged the owning seat.

**State now:** commit `fd86307a` landed the tool hardening with the 26-case fixture
(`git show HEAD:tools/fixtures/mori-commit-runway/cases.json` = `3a1aef20…450623`, blob `91d7d941`), so the
damage is repaired and the tree is consistent — `python3 -I -B tools/mori-commit-runway.py --selftest` prints
`MATCHER: rejected 26/26` / `MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31`, matching the SKILL row, and
`git status --porcelain` shows no modified file of the five I studied. No claim reading was ever affected
(`count-c2` only requires n ≥ 12 and scored `n=23 … agree=80` throughout). Lesson for the report: a scratch
`symlink` to a lane directory is a write path; use a real directory copy.

## Limits of this pass

* Equality of a tally and of a real-run line proves no change on the **exercised** paths. Only C1a is argued
  statically (two call sites, neither can pass `None`); everything else is exercised by an arm or by the applier
  tree comparison.
* The counters are frozen, so their proposals cannot be scored in this round. A successor must apply them in one
  freeze and re-run `evidence/selftest-c1.txt` / `selftest-c2.txt` and the at-data receipts; the round-52 rule
  (a frozen file is never edited in place, measure with `git show <freeze>:<path>`) forbids the L1 patching them
  now as a fix for this round.
* The tool moved twice while I measured (316 → 347 → 435 lines) and landed as `fd86307a`; the three tool hunks
  were run against **both** the data bytes and the landed bytes, but a later edit by anyone else invalidates the
  line numbers, not the hunks.
* `vulture 2.16` reports one false positive in the tool (`_Parser.error`); recorded so a later simplification
  pass does not delete it.

## Findings

1. **HIGH (self-inflicted, repaired) — `tools/fixtures/mori-commit-runway/cases.json`, working tree, 23:17:32.**
   My scratch symlink redirected a `git show` into the lane and replaced an uncommitted 26-case fixture with the
   23-case data-commit bytes; for ~20 minutes the hardened tool printed `PASS 28/28` against a SKILL row claiming
   `PASS 31/31`. Repaired by the owner's commit `fd86307a` (fixture blob `91d7d941`, `3a1aef20…450623`), and the
   tree now prints `PASS 31/31`; no claim reading was affected. Recorded because it shows a leaf seat's scratch
   symlink is a lane write path.
2. **MED — `tools/mori-commit-runway.py:87, :185, :397` (landed `fd86307a`).** "Cannot evaluate = 2" exists
   three times: the `EXIT["COMMIT_UNKNOWN"]` table entry (never read through `EXIT`), `unknown()`'s literal
   return, `_Parser.error`'s `sys.exit(2)`. Safe now; patch T1/T2 above, proven identical on both tool versions
   (`usage error` / `bad --page-kb` → `rc=2`, same stdout).
3. **LOW — `tools/mori-commit-runway.py:386-387` (landed) and `:275` (data bytes).** The selftest's FAIL
   numerator is recomputed by classifying `failed` messages on a prefix (`not f.startswith("matcher")`, landed)
   or on punctuation (`":" in f`, data). Count the three failure classes where they are appended instead (patch
   T3): `PASS 31/31` unchanged, `FAIL 24/27` on a file with two falsified expectations and one malformed case id
   unchanged, 26 cases with 0 differing fields.
4. **MED — `.ufo/waves/round-53/count-c1.py:183, :193`.** Unreachable `ls=None` default and
   `ls or (lambda _d: [])` fallback in `evaluate`; both call sites pass a lister. Proposal for round-54 freeze.
5. **LOW — `.ufo/waves/round-53/count-c1.py:186, :338`.** Four unused loop bindings (`url` in `evaluate`;
   `path`, `digest`, `url` in `selftest`); ruff B007 is the only static signal in the whole file.
6. **LOW — `.ufo/waves/round-53/count-c2.py:100`.** `enforced=None, limit_consistent=None` restate the
   comprehension above them; the tool's `unknown()` already dropped them.
7. **LOW — `.ufo/waves/round-53/count-c2.py:307-308`.** `live_check` unpacks two `ref()` exit codes it never
   reads (`c1`, `c2`).
8. **MED — `.ufo/waves/round-53/count-c2.py:545-547`.** The selftest writes `memo.json` into its temporary tree
   and never reads it (a dead file plus a dead variable in the frozen counter's own selftest). Proposal.
9. **MED — `.ufo/waves/round-53/controls/c1-data.py:45, :131, :156`.** `DISPOSITION` is an always-empty knob:
   both `DISPOSITION.get(h, "holds")` sites can only return `"holds"`, and no file in the lane writes the dict.
   Deleting it changes no control (all receipts say `holds=46 changed=0`). Proposal.
10. **LOW — `.ufo/waves/round-53/controls/c1-data.py:47, :116, :126`.** Three literals retype counter constants
    the module already imports: `R53` ≙ `C.SRC_DIR`, the row date ≙ `C.OPENED`, the ledger header row ≙
    `C.HEADER` (the last one can silently produce a table the counter refuses). Proposals.
11. **LOW — `.ufo/waves/round-53/controls/controls.py:17`.** `E` retypes `count-c1.ENTERING`; deriving it costs
    a module load, so it is reported and not applied.
12. **LOW — `tools/mori-commit-runway.py:395` (landed) / `:283` (data bytes), `_Parser.error`.** vulture
    flags it as an unused method at 60 % confidence; it is argparse's error hook and is live. Recorded so it is
    not deleted by a later pass.
