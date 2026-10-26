# Mo51SimpCounters — dead weight in the round-51 counters, the C1 control builder and pin-check v5

Seat: Mo51SimpCounters (simplifier / dead-weight removal, round 51 wave `w1`).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Fleet root: `/home/vgpnk/Projects/shokunin`.
Scratch: `/fast/scratch/hyaku/mori-r51/Mo51SimpCounters/` (removed at the end of the run; every diff and
output cited below is copied into this file first).

## What I did and did not do

- I wrote **only this file**. No tracked file in the lane, no file under `.ufo/waves/round-51/`, no corpus,
  tool, SKILL/SHONEN/SCORECARD/LOG, no `~/.local/bin`, no PATH directory was created, modified or deleted by
  this seat. Every deletion below was applied to a **scratch copy** and proven there; the patches are
  proposals, because the counters and `controls/` are frozen.
- Read-only git only (`show`, `diff`, `status`, `rev-parse`, `clone`, `for-each-ref`, `log`). Fixture repos live
  under my scratch and `git -C <fixture> rev-parse --show-toplevel` was asserted before any commit there.
- Nothing was installed: `pyflakes` 4.0.3 and `vulture` were already present in `~/.local/bin`; no pacman call
  was made (host-wide pause respected).
- No `lsp`/references server is exposed to this seat (the tool inventory has no `lsp` device), so reference
  evidence is textual (`grep`, `pyflakes`, `vulture`) plus runtime proof (the code actually executes with the
  deleted lines and produces identical bytes). I do not present grep as semantic proof.

## Entry state (measured, not assumed)

Frozen bytes I analysed, hashes of the working tree at the time of the first read (`git diff --stat
87e0c374537557754bf71dd68036ded3ddc6699c HEAD -- <these paths>` printed nothing then, so worktree = data
commit = HEAD `b504cb17` for them):

| file | sha256 | lines |
|---|---|---|
| `.ufo/waves/round-51/count-c1.py` | `622f650c1ade984d8c9abed20e7a7fd08930861a698398f36d4c3a770aff355c` | 266 |
| `.ufo/waves/round-51/count-c2.py` | `19553792d74d8f3ca9c09e6a018b9c66f61a58e8ad78e72b524a69ec892cfb26` | 475 |
| `.ufo/waves/round-51/controls/c1-controls.py` | `8351ba6d4008037ef3f2694b73f9e2e9cad41bb5cb77ea21dc7511556266887a` | 94 |
| `tools/mori-pin-check.py` **at 87e0c37** (`git show 87e0c37:tools/mori-pin-check.py`) | `35c69d9115b5e45f91a4b0311ce95c03b3b2b929250e2afb31b571a49687b3bf` | 1504 |

**Concurrent change by another seat (not mine).** During my run the L1 replaced the working-tree
`tools/mori-pin-check.py` (mtime `2026-10-26 19:56:36`, `git diff --stat` = 96 insertions / 9 deletions, new
sha256 `e902cef7382ff5accd7ab11ab352aa6a3c739a33fb45a367d894c70bce286b47`). Its content is a **v5.1** section
naming sibling reports (`Mo51CritClassRule.md`, `Mo51CritExportClone.md`, `Mo51SentKillSafety.md`). I adapted:
my byte-level claims about "v5" are stated against `35c69d91…`, every pin-check experiment below was run with
the pinned copy extracted with `git show 87e0c37:`, and the two defects I found independently are reported as
corroboration plus evidence that the v5.1 wording/semantics are the right ones (see Findings F1/F2).

## Independent re-measurements (the data I was asked to attack did hold)

1. C1 at the data commit, from my scratch, with the frozen counter (my own clones, my own scratch):

```
$ cd /fast/scratch/hyaku/mori-r51/Mo51SimpCounters && python3 src/c1_orig.py \
    87e0c374537557754bf71dd68036ded3ddc6699c --repo <lane> --hide <lane> --scratch <scratch>/run-orig
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0
            rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no env=2 stale=2
kill_residue_first: -
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0
   rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=-
exit 0
```

   Same line as `evidence/c1-at-data.txt`, with the nesting `mismatches=4 env=2 stale=2` visible, i.e. the
   v5 invariant "env + stale = mismatches" holds on the frozen five-row registry.
2. C2 at the data commit: `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok
   pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c37…failed=entailment`, rc 1 — identical to
   `evidence/c2-at-data.txt` (this is an entailment-arm gap, not a simplification matter and not my item).
3. The registry pin reconciler, on the **data-commit bytes**, at the data commit:

```
$ python3 <pinned v5 copy> --rev 87e0c374537557754bf71dd68036ded3ddc6699c --repo <lane> --scratch <scratch>/pcr2
PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0
  duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=87e0c374… baseline=no env=0 stale=0
exit 0
```
   The same command with the live (v5.1) working-tree file produced byte-identical output (`diff` empty), so
   the L1's in-flight edit did not change the reading at the data commit.

## Deletions found (each proven on a scratch copy)

Method: each patch asserts its own match count, so a silent no-match aborts. Two proof classes were used —
(i) the counter's own selftest tally plus a real run at `87e0c37` compared byte-for-byte (`rc`, stdout), and
(ii) for arms that need clones, the arm functions imported from the patched module and compared directly.

### D1 `count-c2.py` — the HTML normaliser, `import html`, and the `kind` field of `COPIES` (18 lines)

Every entry of `COPIES` is `"text"`, so `normalise()` is unreachable and the third tuple element is only ever
compared with `"html"`. `normalise_text()` already does what the text branch needs. No selftest arm exercises
the HTML branch, so the dead path is also unverified code.

```diff
 import hashlib
-import html
 import os
@@
-# url -> (committed copy, sha256 of the copy fetched 2026-10-26, kind)
+# url -> (committed copy, sha256 of the copy fetched 2026-10-26)
         (SRC_DIR + "proc.rst.v7.2", "e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126"),
@@ evaluate
-    for url, (path, digest, kind) in copies.items():
+    for url, (path, digest) in COPIES.items():
         b = read(path)
-        norm[url] = normalise(b or "") if kind == "html" else normalise_text(b or "")
+        norm[url] = normalise_text(b or "")
@@ selftest
-def normalise(text):
-    t = re.sub(r"<(script|style)\b.*?</\1\s*>", " ", text, flags=re.S | re.I)
-    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
-    t = re.sub(r"<[^>]+>", " ", t)
-    t = html.unescape(t)
-    return re.sub(r"\s+", " ", t)
-
-
@@ selftest
-    for url, (path, digest, kind) in COPIES.items():
+    for url, (path, digest) in COPIES.items():
-    texts = {u: (normalise(files[p]) if k == "html" else normalise_text(files[p]))
-             for u, (p, d, k) in COPIES.items()}
+    texts = {u: normalise_text(files[p]) for u, (p, d) in COPIES.items()}
```

Tradeoff: if a future row cites an HTML page this branch comes back — but then with a selftest arm, which it
does not have today.

### D2 `count-c2.py` — `evaluate(..., copies=None)` is a seam nothing uses

`grep -n 'copies=' .ufo/waves/round-51/count-c2.py` finds only the signature and `copies = copies or COPIES`;
the selftest injects sources through `read`, never through `copies`.

```diff
-def evaluate(read, rev, entry_path=None, copies=None, ls=None):
+def evaluate(read, rev, entry_path=None, ls=None):
-    copies = copies or COPIES
-    for url, (path, digest) in copies.items():
+    for url, (path, digest) in COPIES.items():
@@
-                for u in copies:
+                for u in COPIES:
```

### D3 `count-c2.py` — the selftest `build(drop=…)` knob never fires

`build` is only called with `status=`, `opened=`, `used=`, `indent=`, `claim_rows=`, `claims=`, `votes=`
(`grep -n 'drop=' count-c2.py` → nothing). With `drop` always `None`, the `{"status": "queued"}` branch is
unreachable and the whole `if drop != sids[u] else …` conditional is dead.

```diff
-    def build(claim_rows=None, drop=None, claims=None, votes="all", **kw):
+    def build(claim_rows=None, claims=None, votes="all", **kw):
-            srow(u, sids[u], **({k: v for k, v in kw.items() if k in ("status", "opened", "used", "indent")}
-                                if drop != sids[u] else {"status": "queued"})) for u in urls])
+            srow(u, sids[u], **{k: v for k, v in kw.items() if k in ("status", "opened", "used", "indent")})
+            for u in urls])
```

### D4 `count-c2.py` — an unreachable branch in `parse_claims`

`header = header if rows else None` is only reached after `if header is not None and rows: break`, so when it
runs with non-empty `rows`, `header` is already `None`; with empty `rows` the expression is `None` too. It is
always `None`.

```diff
             if not line.strip():
-                header = header if rows else None
+                header = None
```

### D5 `count-c2.py` — the lane path has three authorities; `count-c1.py` already has one

The 4-level `os.path.dirname` chain appears twice in `main` and again as `here`/`lane` in `selftest`.
`count-c1.py:37-38` already names `HERE` + `DEFAULT_REPO`; using the same names is one convention, not a
second one.

```diff
 SPAN = re.compile(r"`([^`]+)`")
+# One authority for "the lane this file sits in" (count-c1.py names the same two constants).
+HERE = os.path.dirname(os.path.abspath(__file__))
+DEFAULT_REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
@@ main --hashes
-        repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
-        text = git_reader(repo, argv[1])(ENTRY)
+        text = git_reader(DEFAULT_REPO, argv[1])(ENTRY)
@@ main
-    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
+    repo = DEFAULT_REPO
@@ selftest
-    here = os.path.dirname(os.path.abspath(__file__))
-    lane = os.path.dirname(os.path.dirname(os.path.dirname(here)))
+    lane = DEFAULT_REPO
```

### D6 `count-c2.py` — the word tokeniser is written twice inside `words_beyond`

```diff
-def words_beyond(claim, quote):
-    qw = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", quote))
-    return len(set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", claim)) - qw)
+def tokens(text):
+    return set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", text))
+
+
+def words_beyond(claim, quote):
+    return len(tokens(claim) - tokens(quote))
```

### D7 `count-c1.py` — `FIXTURES` and `ROWS` are two authorities for one fixture set

`FIXTURES` keys are `"enva.py"…`, `ROWS` carries `"enva"…` — the same five stems written twice, one with the
`.py` suffix and the pinned tally in the other. A stem rename or a sixth fixture has to be done in two places,
and the two lists are read by two different loops against the same directory. One tuple list keeps the order the
dict/list already had (`enva, envb, stla, stlb, okay`), so both the fixture files and the generated `SKILL.md`
rows are unchanged.

```diff
-FIXTURES = {
+FIXTURE_ROWS = [
+    # (stem, instrument source, pinned tally in its SKILL.md row)
     # env: no tally line at all — setup error naming a missing absolute path, rc 2
-    "enva.py": ("import sys\nif '--selftest' in sys.argv:\n"
-                "    print('setup error: No such file or directory: /nonexistent/lane/count.py')\n"
-                "    sys.exit(2)\n"),
+    ("enva", ("import sys\nif '--selftest' in sys.argv:\n"
+              "    print('setup error: No such file or directory: /nonexistent/lane/count.py')\n"
+              "    sys.exit(2)\n"), "ENVA_SELFTEST pass=3 fail=0"),
     # env: the instrument dies before printing its tally (traceback-like), rc 1
-    "envb.py": ("import sys\nif '--selftest' in sys.argv:\n"
-                "    print('Traceback (most recent call last):')\n"
-                "    print('FileNotFoundError: [Errno 2] No such file or directory')\n"
-                "    sys.exit(1)\n"),
+    ("envb", ("import sys\nif '--selftest' in sys.argv:\n"
+              "    print('Traceback (most recent call last):')\n"
+              "    print('FileNotFoundError: [Errno 2] No such file or directory')\n"
+              "    sys.exit(1)\n"), "ENVB_SELFTEST pass=4 fail=0"),
     # stale: it runs and prints a different tally
-    "stla.py": ("import sys\nif '--selftest' in sys.argv:\n"
-                "    print('STLA_SELFTEST pass=5 fail=0')\n"),
+    ("stla", ("import sys\nif '--selftest' in sys.argv:\n"
+              "    print('STLA_SELFTEST pass=5 fail=0')\n"), "STLA_SELFTEST pass=4 fail=0"),
     # stale: the pinned tally text, but an exit code that contradicts it
-    "stlb.py": ("import sys\nif '--selftest' in sys.argv:\n"
-                "    print('STLB_SELFTEST pass=2 fail=0')\n    sys.exit(1)\n"),
-    "okay.py": ("import sys\nif '--selftest' in sys.argv:\n"
-                "    print('OKAY_SELFTEST pass=1 fail=0')\n"),
-}
-ROWS = [("enva", "ENVA_SELFTEST pass=3 fail=0"), ("envb", "ENVB_SELFTEST pass=4 fail=0"),
-        ("stla", "STLA_SELFTEST pass=4 fail=0"), ("stlb", "STLB_SELFTEST pass=2 fail=0"),
-        ("okay", "OKAY_SELFTEST pass=1 fail=0")]
+    ("stlb", ("import sys\nif '--selftest' in sys.argv:\n"
+              "    print('STLB_SELFTEST pass=2 fail=0')\n    sys.exit(1)\n"), "STLB_SELFTEST pass=2 fail=0"),
+    ("okay", ("import sys\nif '--selftest' in sys.argv:\n"
+              "    print('OKAY_SELFTEST pass=1 fail=0')\n"), "OKAY_SELFTEST pass=1 fail=0"),
+]
@@ arm_classified
-    for name, src in FIXTURES.items():
-        with open(os.path.join(fx, "tools", name), "w") as f:
-            f.write(src)
     body = HDR
-    for stem, tally in ROWS:
+    for stem, src, tally in FIXTURE_ROWS:
+        with open(os.path.join(fx, "tools", stem + ".py"), "w") as f:
+            f.write(src)
```

The instrument sources are byte-identical after the change (only their container/key position changed), which is
what the fixture-tree sha256 in P-b checks; the patch is complete here, nothing is left in scratch.

### D8 `count-c1.py` — `arm_relocated` returns a third value the caller throws away

`main` unpacks `reloc, mism, _ = arm_relocated(...)`; the arm also writes the same lines to
`relocated.out`, which is what `--keep` keeps. The returned copy is unused.

```diff
-    return p.returncode == 0 and last.startswith("PIN_CHECK=met"), mism, out
+    return p.returncode == 0 and last.startswith("PIN_CHECK=met"), mism
@@ main
-        reloc, mism, _ = arm_relocated(repo, rev, w, os.path.abspath(a.hide))
+        reloc, mism = arm_relocated(repo, rev, w, os.path.abspath(a.hide))
```

### D9 `controls/c1-controls.py` — one `git show` whose value is never read

`pyflakes 4.0.3` on the frozen builder:

```
src/controls_orig.py:53:5: local variable 'ent_cf' is assigned to but never used
```

The entering `conform.py` is never used: the `conform-only`, `always-env` and `witness` variants all take
`wit_cf` (the witness copy), and `ent_cf` is referenced nowhere else. It is a full `git show` of a 20 kB file on
every builder run.

```diff
     ent_pc = git(k, "show", "%s:%s" % (base, PC))
-    ent_cf = git(k, "show", "%s:%s" % (base, CF))
     wit_pc = open(os.path.join(HERE, "witness", "mori-pin-check.py")).read()
```

`CF` stays: it is still the dict key of the `conform-only` variant, so deleting the read does not make the
constant dead (`pyflakes` on the patched builder: clean, rc 0).

## Proofs

### P-a — `count-c2.py`, combined (D1+D2+D3+D4+D5+D6): 33 lines deleted, 26 added, 475 → 468 lines

Each candidate was also proven **individually** (D1 alone, D1+D2, D1+D3, D1+D4) — all four readings identical to
the original, so the L1 can take any subset.

```
# selftest, run from a mirror so lane=DEFAULT_REPO holds the five frozen copies
orig  : rc=0  C2_SELFTEST pass=34 fail=0
patch : rc=0  C2_SELFTEST pass=34 fail=0          # diff of full stdout: empty
# real run at the data commit (git objects only, so deterministic)
orig  : rc=1  C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok
               provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment
patch : rc=1  (same line, byte-identical)
# --hashes at the data commit, from a copy inside a clone of the lane
orig  : rc=0  21 rows printed
patch : rc=0  21 rows printed, byte-identical
pyflakes on the patched file: rc 0
```

### P-b — `count-c1.py`, combined (D7+D8): 24 lines deleted, 21 added, 266 → 263 lines

```
# arms imported directly from each module copy, same lane, same revision, separate work dirs
orig  : classified_ok=True  fixture_sha256=63b1f9b40dc58768…  selftest=True pass=119,fail=0
patch : classified_ok=True  fixture_sha256=63b1f9b40dc58768…  selftest=True pass=119,fail=0
CLASSIFIED_LINES_IDENTICAL True
SELFTEST_IDENTICAL True
```

The fixture tree hash covers the five `.py` instruments **and** the generated `SKILL.md`, so both authorities
(`FIXTURES` files, `ROWS` cells) are proven unchanged. The five classified lines the fixture produces (identical
in both):

```
pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 … class=env
pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 … class=env
pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' … class=stale
pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 … class=stale
pin line=7 kind=tally prefix=OKAY_SELFTEST state=match  pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0
PIN_CHECK=unmet … mismatches=4 … env=2 stale=2
```

Whole-counter run, original vs patched, in parallel, same `--repo`/`--hide`/own `--scratch`:

```
=== ORIG ===  C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0
              rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=-      exit 0
=== PATCH === C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0
              rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=-      exit 0
=== DIFF ===  REAL_RUN_OUTPUT_IDENTICAL
```

Including the volatile arms: `kill_residue=0` and `kill_residue_first: -` matched in both runs (the kill arm is
timing-dependent, so this is the strongest available check, not a guarantee for every schedule).

### P-c — `controls/c1-controls.py`, D9: 1 line deleted, 94 → 93 lines

Two builds of the fixture repo, identical except for the deleted line, with fixed author/committer identity and
dates so the commits are byte-comparable (`BASE_REV = aa3af1ec…`, the same base the receipts used):

```
== orig ==                                      == p3 (D9) ==
refs/heads/ctl-always-env  fa8e496d… 34d3d13e…   fa8e496d… 34d3d13e…
refs/heads/ctl-class-only  77b50389… 0358ea25…   77b50389… 0358ea25…
refs/heads/ctl-conform-only 0d569da6… 6be97acc…  0d569da6… 6be97acc…
refs/heads/ctl-scratch-only ce868ed0… 15e8850b…  ce868ed0… 15e8850b…
refs/heads/ctl-witness     22de754c… 3b9ec209…   22de754c… 3b9ec209…
REFS_IDENTICAL True   TREES_IDENTICAL True
```

Both builders exit 0 and print the same `name repo rev` rows, so the dead `git show` had no observable effect on
the control commits the counter scores.

## Candidates examined and **rejected** (not dead, do not delete)

1. **`count-c1.py:249` `kill_residue_first:` — the "unused `first` detail".** `first` is returned by `arm_kill`
   and printed on its own line. `grep -rn 'kill_residue_first'` finds it in
   `evidence/control-c1-do-nothing.txt`-style receipts and in two sibling reports (`Mo51ExecC1Controls.md`,
   `Mo51ConnCrossClaim.md`) as the quoted witness of *which* path the kill left behind. Deleting it changes
   receipt bytes, so it is not behaviour-preserving; it is also the only evidence of the residue's shape.
   Kept. (LOW, see F4.)
2. **"`ROWS`/`FIXTURES` duplication" is not a duplicate-entry problem.** The two hold different data (script
   text vs pinned tally); D7 merges the *stem authority* only. Deleting either list instead would delete the
   fixture or its pin.
3. **`git branch -f ctl-<name>` in the control builder is NOT dead.** I flagged it first (the counter addresses
   each control by SHA, `fresh_clone` never reads a branch) — but `grep -rn 'ctl-' .ufo/waves/round-51`
   shows a consumer: `Mo51ExecC1Controls.md:117-270` reads `git -C <K> show ctl-witness:<path>` and
   `ctl-class-only:` / `ctl-always-env:` to prove the witness/class-only byte claims. The branch names are a used
   affordance of the builder's output and were kept.
4. **The `--root` sentence in the pin-check docstring is true.** I suspected the `with --root it writes temp
   dirs under <root>/.scratch` clause was stale after v5, but `run_cmd()` (`tools/mori-pin-check.py:539-544`,
   unchanged by v5) creates exactly `<root>/.scratch`: after `--root <fixture>` the directory exists
   (`ls -d <fixture>/.scratch` → present). No finding.
5. **`count-c2.py`'s `source_rows=` flag is redundant but must stay.** `srows_ok` is `"ok"` iff
   `ids_in_table and not bad`, and `bad_rows` is appended exactly when `bad` is nonzero, so `source_rows` can
   only add a failure label in the empty-table case where `table`/`claims_floor` already fail. Removing it would
   change the documented output line (`source_rows=ok|bad`), so it is a named limit, not a deletion (LOW, F3).
6. **`count-c1.py`'s double guard `for inside in (repo, os.path.abspath(a.hide))`** checks the same path twice
   when `--hide` is not passed. Removing the duplicate would special-case a default; one extra
   `os.path.commonpath` on a string is not weight. Kept.

## What the v5 diff of `tools/mori-pin-check.py` still owed (attacks on the landed data)

`pyflakes 4.0.3` and `vulture --min-confidence 60` on the data-commit bytes: **no unused import or unused local
left** — v5 already removed `import tarfile` and the `tree.tar` staging, and nothing references the archive path.
So there is no *dead code* left in v5; what remained were two v5 sentences/behaviours that did not match v5:

**F1 (MED, `tools/mori-pin-check.py` at 87e0c37, tally branch around line 824).** `observed = tails.pop() if
len(tails) == 1 else None` then `kind = "env" if observed is None else "stale"` classes **two disagreeing tally
lines** as `env`, while the v5 docstring says `env` = "the pinned command printed no tally line for its prefix",
and the contract's named limit says a tool that prints a tally and then fails is `stale`. Witness (fixture with
one instrument printing `DUAL_SELFTEST pass=1 fail=0` and `DUAL_SELFTEST pass=2 fail=0`, row pinning the first):

```
$ python3 <v5 bytes at 87e0c37> --root <fixture>
pin line=3 kind=tally prefix=DUAL_SELFTEST state=mismatch pinned='pass=1 fail=0' observed=None rc=0 … class=env
PIN_CHECK=unmet … mismatches=1 … env=1 stale=0        exit 1

$ python3 <live worktree, v5.1) --root <same fixture>
pin line=3 kind=tally prefix=DUAL_SELFTEST state=mismatch pinned='pass=1 fail=0' observed=None rc=0 … class=stale
PIN_CHECK=unmet … mismatches=1 … env=0 stale=1        exit 1
```

The instrument ran (rc 0) and printed two tallies: the env label told the reader "could not run here". The
already-present v5.1 in the working tree fixes exactly this, so I do not propose a tool change for this round —
C1's arm C is scored on the five frozen fixtures, and re-scoring under changed bytes is forbidden by the kill
rule. Named limit for the receipt: at `87e0c37` an `env=N` count may include instruments that ran and
disagreed.

**F2 (LOW, same file, `Modes` section line 114 at 87e0c37).** `--rev REV [--repo DIR] export REV with `git
archive` and measure it there` survived v5, although v5 replaced the export with a `git clone --shared`
(the paragraph eight lines below says so). Dead documentation that contradicts the code; v5.1 changes the same
line. Not a tool-code deletion, so nothing in my patch set touches it.

## Contract preserved

- Nothing in the frozen predicate, counter, floor or kill rule was changed or proposed as this round's fix; the
  patches above are successor proposals whose only observable effect is byte-identical output at the data commit.
- The measured readings of C1 and C2 at the data commit are unchanged by every patch (P-a, P-b, P-c).
- I did not edit `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `LOG.md`, `corpus/`, `tools/`,
  `considerthese/`, or any round-51 file other than this report.
- Named limits I leave in place rather than simplify away: the `kill_residue_first:` diagnostic (receipt text),
  `source_rows=` (reported line), the `ctl-*` branches (sibling evidence), the env/stale mislabel at `87e0c37`
  (frozen scoring), and the kill arm's single kill moment (contract-named).

## Findings

- **MED — `tools/mori-pin-check.py` (data commit 87e0c37, tally classification ~line 824):** two disagreeing
  tally lines are labelled `class=env` although the instrument ran and printed; contradicts the tool's own v5
  definition and inflates any `env=N` reading. Independently reproduced; the live v5.1 worktree bytes already
  label the same fixture `class=stale` (F1).
- **LOW — `tools/mori-pin-check.py:114` (data commit):** `Modes` still documents the `--rev` export as `git
  archive`; v5's code and the paragraph below it say `git clone --shared` (F2).
- **LOW — `.ufo/waves/round-51/count-c2.py:51,80-85,153,308-309`:** `import html`, `normalise()` and the
  `"text"`/`kind` tuple element are unreachable dead weight (D1, 18 lines; no selftest arm covers the HTML path).
- **LOW — `.ufo/waves/round-51/count-c2.py:140,149,153,196`:** `evaluate(copies=…)` is a seam with no caller
  (D2).
- **LOW — `.ufo/waves/round-51/count-c2.py:340,343-344`:** `build(drop=…)` and its `{"status": "queued"}` branch
  are unreachable (D3).
- **LOW — `.ufo/waves/round-51/count-c2.py:97-99`:** `header = header if rows else None` always assigns `None`
  (D4).
- **LOW — `.ufo/waves/round-51/count-c2.py:245,262,302`:** the lane path is derived three times; `count-c1.py`
  already owns `HERE`/`DEFAULT_REPO` (D5).
- **LOW — `.ufo/waves/round-51/count-c2.py:75-77`:** the word tokeniser is written twice in `words_beyond`
  (D6).
- **LOW — `.ufo/waves/round-51/count-c1.py:43-60,163-169`:** `FIXTURES` and `ROWS` are two authorities for the
  same five stems, one with `.py` and one with the tally (D7).
- **LOW — `.ufo/waves/round-51/count-c1.py:150,237`:** `arm_relocated` returns a third value its caller discards
  (D8).
- **LOW — `.ufo/waves/round-51/controls/c1-controls.py:53`:** `ent_cf` is an unused `git show` (pyflakes-only
  find; proven side-effect-free against the five control commits) (D9).
- **INFO — `.ufo/waves/round-51/count-c2.py:230-232`:** the `source_rows` failure flag is implied by `bad_rows`;
  kept because the output line is documented (F3-style named limit).
- **INFO — `.ufo/waves/round-51/count-c1.py:249`:** `kill_residue_first:` is not part of the counter's documented
  output but is the residue's only shape evidence and is quoted by sibling reports; keep.
- **INFO — `tools/mori-pin-check.py` (working tree, uncommitted, sha256 `e902cef7…`):** changed by the L1 during
  this wave (v5.1: absent instrument → stale, two tallies → stale, partial output on timeout, measured `master`,
  scratch default `$TMPDIR` else `/var/tmp`). My v5 findings and this edit agree; the data-commit receipt at
  `87e0c37` was measured on `35c69d91…` and re-read identically with the live file.

Report: .ufo/waves/round-51/w1/Mo51SimpCounters.md
