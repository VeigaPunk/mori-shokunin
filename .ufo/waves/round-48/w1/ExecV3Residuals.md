# ExecV3Residuals — round 48 w1: R7 residuals + R8 selftest arms (candidate patch vs v2)

Seat: ExecV3Residuals (executor, leaf — one labrat probe only, none dispatched).
Lane: mori-shokunin. Date: 2026-10-25.
Scope: draft the R7 and R8 parts of `.ufo/waves/round-48/v3-spec.md` as a patch against
v2 `tools/mori-pin-check.py`, per the seat tasking. Candidate lives in scratch
`.scratch/r48-ExecV3Residuals/`; **no production file was edited** (the lane's
`tools/mori-pin-check.py` working-tree bytes were already mid-edit by a sibling seat at
start — observed, not touched; see §8).

## 1. Bytes under test

| what | sha256 |
|---|---|

| v2 committed at entering tip `e5dbac05` (`git show e5dbac05:tools/mori-pin-check.py`) | `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` |
| v2 working tree at start (`tools/mori-pin-check.py`) | `2753087b4e55c2352e54a8ae20fa37c108c832924b388d9c5ce0965eb64f46f8` (sibling edit in flight; NOT used as base) |
| candidate v3 (`v3-mori-pin-check.py`) — this seat | `b87115032893dadd0cd0d774a10119cbe31f98c7e37ffd44c76d6a089968b403` |

**Interpretation of the counter result.** The C1 acceptance for the candidate alone keeps the
entering do-nothing state: `C1=unmet junk_met=8` — byte-identical per-variant to the frozen
receipt `evidence/control-c1-tool-v2-entering.txt` (entering v2: J1–J8 all `got=met`,
H1–H4 and real `met`). The junk classes J1–J8 are the domain of R1–R6 (header recognition,
visibility/fence/blank-line, non-ASCII and casefolded unparsed, rebound by prefix, line-count
pins, truncated digests) — owned by the sibling seats that build those rules; this seat
implements R7/R8 only. The counter therefore proves **no regression** from v2 on any variant
(`errors=0`, honest + real still met) while the R7/R8 arms are each killed by their own
mutation (§5). The merged candidate (R1–R8) is expected to flip `junk_met` to 0.

All v2 demos below run the committed v2 bytes (`v2-pristine.py`). All lane-tool runs used
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecV3Residuals`.
No tool installed or upgraded (python3 already present; RULES.md read; nothing to record).

## 2. The patch (unified diff, v2 → v3)

Generated with `diff -u v2-pristine.py v3-mori-pin-check.py` (scratch copies); the full
verbatim diff follows.
### 2b. Diff text (verbatim `diff -u v2-pristine.py v3-mori-pin-check.py`)

```diff
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecV3Residuals/v2-pristine.py	2026-10-25 18:34:13.473561216 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecV3Residuals/v3-mori-pin-check.py	2026-10-25 18:46:07.384965869 -0300
@@ -90,6 +90,7 @@
 # revision and `--selftest`.
 SAFE_PATH = re.compile(r"(?:tools|\.ufo/waves/round-[0-9]+)/[A-Za-z0-9_./-]+\.(?:py|sh)")
 PY_FLAGS = ("-I", "-B")
+PIN_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+[Ss][Ee][Ll][Ff][Tt][Ee][Ss][Tt](?![A-Za-z0-9_])")
 
 
 def argv_ok(argv, rev):
@@ -109,14 +110,34 @@
 
 
 def split_cells(line):
+    """Split one GFM table row on unescaped `|`. A pipe is a separator unless
+    it is preceded by an odd number of backslashes: a single `\\|` is an
+    escaped pipe inside a cell; `\\\\|` (two backslashes) is a literal
+    backslash followed by a real separator. v3 (R7 L2): a `\\\\` pair before
+    a pipe no longer hides the separator (v2's single-character lookbehind
+    mis-split such rows)."""
     s = line.strip()
     if not s.startswith("|"):
         return None
-    parts = re.split(r"(?<!\\)\|", s)
-    if s.endswith("|") and not s.endswith("\\|"):
-        parts = parts[1:-1]
-    else:
+    parts = []
+    cur = []
+    for i, c in enumerate(s):
+        if c == "|":
+            j = i - 1
+            bs = 0
+            while j >= 0 and s[j] == "\\":
+                bs += 1
+                j -= 1
+            if bs % 2 == 0:
+                parts.append("".join(cur))
+                cur = []
+                continue
+        cur.append(c)
+    parts.append("".join(cur))
+    if parts and parts[0] == "":
         parts = parts[1:]
+    if parts and parts[-1] == "":
+        parts = parts[:-1]
     return [p.strip() for p in parts]
 
 
@@ -177,9 +198,14 @@
 
 
 def pin_commands(cells, idx, rev, eidx=2):
-    """Bind each tally pin in the self-test cell to the nearest preceding
-    executable span: a `--selftest` command, or a bare `.py`/`.sh` path (a
-    mutant named after the main command is run as `<interp> <path> --selftest`)."""
+    """Bind tally pins in the self-test cell to the nearest preceding executable
+    span. Yields (kind, prefix, pinned, words, span):
+      ("pin", prefix, pinned, argv or None, span)  — tally pin
+      ("command", None, None, argv, span)          — bound command
+      ("unparsed", None, None, None, span)         — a SELFTEST token not at
+                                                     the span start (R7 L4)
+    A span that names `--selftest` is a command attempt and never unparsed by
+    this rule. """
     st = cells[idx]
     bound = []
     current = None
@@ -187,11 +213,15 @@
         span = m.group(1)
         pm = re.match(r"([A-Z][A-Z0-9_]*SELFTEST)(.*)$", span, re.S)
         if pm:
-            bound.append((pm.group(1), pm.group(2), current))
+            bound.append(("pin", pm.group(1), pm.group(2), current, span))
             continue
         cmd = command_from_span(span, cells, rev, eidx)
         if cmd is not None:
+            bound.append(("command", None, None, cmd, span))
             current = cmd
+            continue
+        if "--selftest" not in span and PIN_TOKEN_RE.search(span):
+            bound.append(("unparsed", None, None, None, span))
     return bound
 
 
@@ -281,7 +311,9 @@
         if row["state"] != "ok":
             continue
         seen = {}
-        for prefix, _pinned, words in pin_commands(row["cells"], row["idx"], rev, row["eidx"]):
+        for kind, prefix, _pinned, words, _span in pin_commands(row["cells"], row["idx"], rev, row["eidx"]):
+            if kind != "pin":
+                continue
             n = seen.get(prefix, 0)
             seen[prefix] = n + 1
             norm = None if words is None else tuple("<REV>" if w == rev else w for w in words)
@@ -323,7 +355,13 @@
         cells, idx = row["cells"], row["idx"]
         st = cells[idx]
         ordinal = {}
-        for prefix, pinned, words in pin_commands(cells, idx, rev, row["eidx"]):
+        for kind, prefix, pinned, words, span in pin_commands(cells, idx, rev, row["eidx"]):
+            if kind == "unparsed":
+                counts["unparsed"] += 1
+                out.append("pin line=%d kind=span state=unparsed span=%r" % (line, span))
+                continue
+            if kind == "command":
+                continue
             n = ordinal.get(prefix, 0)
             ordinal[prefix] = n + 1
             bkey = (cells[0], prefix, n)
@@ -433,11 +471,16 @@
     if not args.rev and not args.root:
         print("PIN_CHECK_SETUP need --rev or --root", file=sys.stderr)
         return 2
-    repo = os.path.abspath(args.repo)
-    scratch_parent = os.path.join(repo, ".scratch")
-    os.makedirs(scratch_parent, exist_ok=True)
-    scratch = tempfile.mkdtemp(prefix="pin-check-", dir=scratch_parent)
     try:
+        repo = os.path.abspath(args.repo)
+        scratch_parent = os.path.join(repo, ".scratch")
+        os.makedirs(scratch_parent, exist_ok=True)
+        scratch = tempfile.mkdtemp(prefix="pin-check-", dir=scratch_parent)
+    except (OSError, tarfile.TarError) as exc:
+        # R7 L5: setup-class failures exit 2 with one line, never a traceback.
+        print("PIN_CHECK_SETUP %s" % exc, file=sys.stderr)
+        return 2
+    try:
         rev = None
         if args.rev:
             got = export_rev(repo, args.rev, scratch)
@@ -468,6 +511,11 @@
         met, out = check(text, root, scratch, rev, args.timeout, args.min_tally_pins, baseline_text)
         print("\n".join(out))
         return 0 if met else 1
+    except (OSError, tarfile.TarError) as exc:
+        # R7 L5: a setup-class crash (export, archive extraction) exits 2 with
+        # one line, never a traceback.
+        print("PIN_CHECK_SETUP %s" % exc, file=sys.stderr)
+        return 2
     finally:
         shutil.rmtree(scratch, ignore_errors=True)
 
@@ -597,6 +645,49 @@
                       "| name | entry | self-test | owner |\n|---|---|---|---|\n"
                       "| foo | `python3 tools/rev.py <rev>` | `--selftest` → `REV_SELFTEST: PASS (2 cases)` | mori |\n",
                       1, True, None))
+        # ---------------------------------------------------------------- v3 arms
+        # (R7 L2) `\\|` — a literal backslash then a real separator — must split;
+        # the row stays 8 cells and its pin measures (v2 mis-split into 6).
+        v3_l2 = ("| foo | gate | a\\\\| 0 ok | `python3 tools/foo.py --selftest` → "
+                 "`FOO_SELFTEST pass=3 fail=0` | none | none | mori |\n")
+        cases.append(("v3_escaped_double_backslash_pipe", HDR + v3_l2, 1, True, None))
+        # (R7 L4) a SELFTEST tally token not at the start of its span is unparsed.
+        cases.append(("v3_pin_not_at_span_start", HDR + row(
+            "`run: FOO_SELFTEST pass=3 fail=0`"), 1, False, "unparsed"))
+        # (R8) digest pins resolve inside the measured tree even through an in-tree
+        # symlink (MutV2Digest survivor b).
+        with open(os.path.join(base, "outside-secret.py"), "w") as f:
+            f.write("TAMPERED-BYTES-B\n")
+        out_secret = sha256_file(os.path.join(base, "outside-secret.py"))
+        os.symlink(os.path.join("..", "..", "outside-secret.py"),
+                   os.path.join(root, "tools", "link.py"))
+        cases.append(("v3_digest_symlink_escape", HDR + row(
+            good + " at sha256 `%s` of `tools/link.py`" % out_secret),
+            1, False, "mismatch"))
+        # (R8) argv_ok sub-checks, each isolated (MutV2Argv survivors A/B/C).
+        os.makedirs(os.path.join(root, "corpus"))
+        with open(os.path.join(root, "corpus", "probe.py"), "w") as f:
+            f.write(TOOL)
+        cases.append(("v3_argvok_nonregistered_path", HDR + row(
+            "`python3 corpus/probe.py --selftest` → `FOO_SELFTEST pass=3 fail=0`",
+            entry="no command here"), 1, False, "no_command"))
+        cases.append(("v3_argvok_dotdot", HDR + row(
+            "`python3 tools/../tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`",
+            entry="no command here"), 1, False, "no_command"))
+        os.makedirs(os.path.join(root, "tools", ".scratch"))
+        with open(os.path.join(root, "tools", ".scratch", "x.py"), "w") as f:
+            f.write(TOOL)
+        cases.append(("v3_argvok_scratch_path", HDR + row(
+            "`python3 tools/.scratch/x.py --selftest` → `FOO_SELFTEST pass=3 fail=0`",
+            entry="no command here"), 1, False, "no_command"))
+        cases.append(("v3_argvok_extra_arg", HDR + row(
+            "`python3 tools/foo.py --extra --selftest` → `FOO_SELFTEST pass=3 fail=0`",
+            entry="no command here"), 1, False, "no_command"))
+        # (R8) case-insensitive unparsed detection (MutV2Exact survivor C): a
+        # mixed-case `Foo_Selftest` row carries no lowercase `selftest` substring.
+        v3_mixed = ("| foo | gate | `python3 tools/foo.py` | 0 ok | "
+                    "`Foo_Selftest pass=2 fail=0` | none | mori |\n")
+        cases.append(("v3_unparsed_case_insensitive", HDR + v3_mixed, 1, False, "unparsed"))
         for name, text, floor, want_met, want_state in cases:
             scratch = tempfile.mkdtemp(prefix="c-", dir=base)
             text, btext = text if isinstance(text, tuple) else (text, None)
@@ -619,6 +710,15 @@
         cli2 = subprocess.run([sys.executable, os.path.abspath(__file__), "--rev", "no-such-rev", "--repo", base],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
         results.append(("cli_bad_rev_rc2", cli2.returncode == 2, "rc=%d" % cli2.returncode))
+        # (R7 L5) CLI arm: a setup-class failure (unusable --repo) exits 2 with
+        # one PIN_CHECK_SETUP line, never a traceback.
+        cli3 = subprocess.run([sys.executable, os.path.abspath(__file__), "--rev", "HEAD",
+                               "--repo", os.path.join(os.sep, "proc", "r48-execv3-nonexistent")],
+                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
+        results.append(("v3_setup_error_exit2",
+                        cli3.returncode == 2 and b"PIN_CHECK_SETUP" in cli3.stdout
+                        and b"Traceback" not in cli3.stdout,
+                        "rc=%d" % cli3.returncode))
     finally:
         shutil.rmtree(base, ignore_errors=True)
     fails = 0
```

## 3. Selftest baseline

- v2 (committed bytes): `TMPDIR=$S python3 $S/v2-pristine.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0`, rc 0 (34/34).
- v3 candidate: `TMPDIR=$S python3 $S/v3-mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=43 fail=0`, rc 0 (43/43 — all 34 v2 arms still pass + 9 new arms). Full log: `.scratch/r48-ExecV3Residuals/selftest-v3.log`.

## 4. Reproducers: failing on v2, passing on the patch

All fixtures under `.scratch/r48-ExecV3Residuals/fix/`. `$S` = that scratch dir.
The `--repo $S` flag pins the tool's own scratch inside the lane; fixtures use `--root`.

### 4.1 L2 — escaped `\\|` mis-split (row `| foo | gate | a\\| 0 ok | … |`)

```
$ TMPDIR=$S python3 $S/v2-pristine.py --root $S/fix/l2/tree --repo $S
pin line=3 kind=row state=unparsed cells=7 header=8
PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=1 rev=- baseline=no
rc=1          (false red: the separator after the literal backslash is swallowed)

$ TMPDIR=$S python3 $S/v3-mori-pin-check.py --root $S/fix/l2/tree --repo $S
pin line=3 kind=tally prefix=FOO_SELFTEST state=match pinned='pass=3 fail=0' observed='pass=3 fail=0' rc=0 cmd='python3 tools/foo.py --selftest'
PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=1 rev=- baseline=no
rc=0
```

### 4.2 L4 — tally pin not at span start silently skipped

```
$ TMPDIR=$S python3 $S/v2-pristine.py --root $S/fix/l4/tree --repo $S
PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=1 rev=- baseline=no
rc=1          (no pin line at all; the claim is never measured)

$ TMPDIR=$S python3 $S/v3-mori-pin-check.py --root $S/fix/l4/tree --repo $S
pin line=3 kind=span state=unparsed span='run: FOO_SELFTEST pass=3 fail=0'
PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=1 rev=- baseline=no
rc=1          (now diagnosed as unparsed, fatal)
```

### 4.3 L5 — setup failure exits 2 with one line, never a traceback

```
$ TMPDIR=$S python3 $S/v2-pristine.py --rev HEAD --repo /nonexistent-r48-execv3
Traceback (most recent call last):
  File ".../v2-pristine.py", line 633, in <module>
    sys.exit(main(sys.argv[1:]))
  ...
PermissionError: [Errno 13] Permission denied: '/nonexistent-r48-execv3'
rc=1          (documented contract exit is 2)

$ TMPDIR=$S python3 $S/v3-mori-pin-check.py --rev HEAD --repo /nonexistent-r48-execv3
PIN_CHECK_SETUP [Errno 13] Permission denied: '/nonexistent-r48-execv3'
rc=2
```

### 4.4 symlink containment of digest paths (MutV2Digest survivor b)

v2 already rejects an in-tree symlink to an out-of-tree file (single point of enforcement =
realpath-inside-root; the selftest had **no arm** for it). The patch keeps the behavior and
adds the arm. Fixture: `fix/sym/tree/tools/link.py` → `../../outside-secret.py` (out of
`fix/sym/tree`), digest pin of the target bytes.

```
$ TMPDIR=$S python3 $S/v2-pristine.py --root $S/fix/sym/tree --repo $S
pin line=3 kind=tally prefix=FOO_SELFTEST state=match pinned='pass=3 fail=0' observed='pass=3 fail=0' rc=0 cmd='python3 tools/foo.py --selftest'
pin line=3 kind=digest state=mismatch digest=d6ee1e3cd02e file=None
PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=1 rev=- baseline=no
rc=1

$ TMPDIR=$S python3 $S/v3-mori-pin-check.py --root $S/fix/sym/tree --repo $S
(byte-identical output, rc=1)
```

### 4.5 argv_ok sub-checks (MutV2Argv survivors A/B/C)

Fixture `fix/argv/tree`: four rows, each with a bound-command span that must be rejected —
`corpus/probe.py` (path shape), `tools/../tools/foo.py` (`..`), `tools/.scratch/x.py`
(`.scratch`), `tools/foo.py --extra --selftest` (trailing arg). v2 and v3 reject all four
(no_command), so the "passing on the patch" evidence is that the arms exist and are killed by
their own mutations (§5). Output is identical under v2 and v3:

```
$ TMPDIR=$S python3 $S/v2-pristine.py --root $S/fix/argv/tree --repo $S
pin line=3 kind=tally prefix=FOO_SELFTEST state=no_command
pin line=4 kind=tally prefix=FOO_SELFTEST state=no_command
pin line=5 kind=tally prefix=FOO_SELFTEST state=no_command
pin line=6 kind=tally prefix=FOO_SELFTEST state=no_command
PIN_CHECK=unmet tally_pins=4 digest_pins=0 mismatches=0 unparsed=0 no_command=4 dropped=0 rebound=0 duplicate=0 min_tally_pins=1 rev=- baseline=no
rc=1
```

### 4.6 case-insensitive unparsed detection (MutV2Exact survivor C)

Fixture `fix/ci/tree`: one honest 8-cell row + one 7-cell row naming `Foo_Selftest pass=2
fail=0` (no lowercase `selftest` substring anywhere in that row's raw).

```
$ TMPDIR=$S python3 $S/v3-mori-pin-check.py --root $S/fix/ci/tree --repo $S
pin line=3 kind=tally prefix=FOO_SELFTEST state=match pinned='pass=3 fail=0' observed='pass=3 fail=0' rc=0 cmd='python3 tools/foo.py --selftest'
pin line=4 kind=row state=unparsed cells=7 header=8
PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=1 rev=- baseline=no
rc=1
```

## 5. Mutation kills — every new arm dies when its rule is removed

Method: each mutant is the candidate with exactly one rule reverted (single point); the
detector is `--selftest` (`TMPDIR=$S python3 $S/mut_<m>.py --selftest`). All nine mutants
exit 1 with **exactly one FAIL arm** (the arm for the removed rule); all other 42 arms stay
PASS. Mutant sources are in scratch (`mut_*.py`).

| mutant | rule removed | FAIL arm (observed) |
|---|---|---|
| `mut_l2.py` | split_cells parity → v2 `(?<!\\)\|` | `FAIL v3_escaped_double_backslash_pipe … PIN_CHECK=unmet … unparsed=1` |
| `mut_l4.py` | `PIN_TOKEN_RE` unparsed-span branch | `FAIL v3_pin_not_at_span_start … PIN_CHECK=unmet … unparsed=0` (silent skip returns) |
| `mut_l5.py` | both L5 try/except wrappers (setup + body) | `FAIL v3_setup_error_exit2 rc=1` (traceback returns) |
| `mut_symlink.py` | realpath-inside-root digest check | `FAIL v3_digest_symlink_escape … PIN_CHECK=met … mismatches=0` (false green) |
| `mut_argv_safe.py` | SAFE_PATH clause | `FAIL v3_argvok_nonregistered_path … PIN_CHECK=met` |
| `mut_argv_dotdot.py` | `..` clause | `FAIL v3_argvok_dotdot … PIN_CHECK=met` |
| `mut_argv_scratch.py` | `/.scratch/` clause | `FAIL v3_argvok_scratch_path … PIN_CHECK=met` |
| `mut_argv_tail.py` | strict argv tail | `FAIL v3_argvok_extra_arg … PIN_CHECK=met` |
| `mut_ci_unparsed.py` | `(?i)` → case-sensitive | `FAIL v3_unparsed_case_insensitive … unparsed=0` |

Representative run (symlink):

```
$ TMPDIR=$S python3 $S/mut_symlink.py --selftest
FAIL v3_digest_symlink_escape  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=1 rev=deadbeef baseline=no
PIN_CHECK_SELFTEST pass=42 fail=1
rc=1
```

Full per-mutant logs: `.scratch/r48-ExecV3Residuals/mut-<m>.log`.

Reproducer-level flips under the same mutations (command runs / claim goes green, i.e. the
removed rule was load-bearing):

```
$ TMPDIR=$S python3 $S/mut_symlink.py --root $S/fix/sym/tree --repo $S
pin line=3 kind=digest state=match digest=d6ee1e3cd02e file=tools/link.py
PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 …    rc=0   (false green)

$ TMPDIR=$S python3 $S/mut_argv_safe.py --root $S/fix/argv/tree --repo $S
pin line=3 kind=tally prefix=FOO_SELFTEST state=match pinned='pass=3 fail=0' observed='pass=3 fail=0' rc=0 cmd='python3 corpus/probe.py --selftest'
… (line 3 flips from no_command to match; same for line 4 under mut_argv_dotdot,
   line 5 under mut_argv_scratch, line 6 under mut_argv_tail)

$ TMPDIR=$S python3 $S/mut_ci_unparsed.py --root $S/fix/ci/tree --repo $S
PIN_CHECK=met tally_pins=1 … unparsed=0 …    rc=0         (false green)

$ TMPDIR=$S python3 $S/mut_l2.py --root $S/fix/l2/tree --repo $S
pin line=3 kind=row state=unparsed cells=7 header=8       (v2 mis-split returns)

$ TMPDIR=$S python3 $S/mut_l4.py --root $S/fix/l4/tree --repo $S
PIN_CHECK=unmet tally_pins=0 …                            (silent skip returns)

$ TMPDIR=$S python3 $S/mut_l5.py --rev HEAD --repo /proc/r48-execv3-nonexistent
Traceback (most recent call last): … FileNotFoundError: [Errno 2] …
rc=1
```

## 6. New selftest arms (text, as they appear in `selftest()`)

```python
        # ---------------------------------------------------------------- v3 arms
        # (R7 L2) `\\|` — a literal backslash then a real separator — must split;
        # the row stays 8 cells and its pin measures (v2 mis-split into 6).
        v3_l2 = ("| foo | gate | a\\\\| 0 ok | `python3 tools/foo.py --selftest` → "
                 "`FOO_SELFTEST pass=3 fail=0` | none | none | mori |\n")
        cases.append(("v3_escaped_double_backslash_pipe", HDR + v3_l2, 1, True, None))
        # (R7 L4) a SELFTEST tally token not at the start of its span is unparsed.
        cases.append(("v3_pin_not_at_span_start", HDR + row(
            "`run: FOO_SELFTEST pass=3 fail=0`"), 1, False, "unparsed"))
        # (R8) digest pins resolve inside the measured tree even through an in-tree
        # symlink (MutV2Digest survivor b).
        with open(os.path.join(base, "outside-secret.py"), "w") as f:
            f.write("TAMPERED-BYTES-B\n")
        out_secret = sha256_file(os.path.join(base, "outside-secret.py"))
        os.symlink(os.path.join("..", "..", "outside-secret.py"),
                   os.path.join(root, "tools", "link.py"))
        cases.append(("v3_digest_symlink_escape", HDR + row(
            good + " at sha256 `%s` of `tools/link.py`" % out_secret),
            1, False, "mismatch"))
        # (R8) argv_ok sub-checks, each isolated (MutV2Argv survivors A/B/C).
        os.makedirs(os.path.join(root, "corpus"))
        with open(os.path.join(root, "corpus", "probe.py"), "w") as f:
            f.write(TOOL)
        cases.append(("v3_argvok_nonregistered_path", HDR + row(
            "`python3 corpus/probe.py --selftest` → `FOO_SELFTEST pass=3 fail=0`",
            entry="no command here"), 1, False, "no_command"))
        cases.append(("v3_argvok_dotdot", HDR + row(
            "`python3 tools/../tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`",
            entry="no command here"), 1, False, "no_command"))
        os.makedirs(os.path.join(root, "tools", ".scratch"))
        with open(os.path.join(root, "tools", ".scratch", "x.py"), "w") as f:
            f.write(TOOL)
        cases.append(("v3_argvok_scratch_path", HDR + row(
            "`python3 tools/.scratch/x.py --selftest` → `FOO_SELFTEST pass=3 fail=0`",
            entry="no command here"), 1, False, "no_command"))
        cases.append(("v3_argvok_extra_arg", HDR + row(
            "`python3 tools/foo.py --extra --selftest` → `FOO_SELFTEST pass=3 fail=0`",
            entry="no command here"), 1, False, "no_command"))
        # (R8) case-insensitive unparsed detection (MutV2Exact survivor C): a
        # mixed-case `Foo_Selftest` row carries no lowercase `selftest` substring.
        v3_mixed = ("| foo | gate | `python3 tools/foo.py` | 0 ok | "
                    "`Foo_Selftest pass=2 fail=0` | none | mori |\n")
        cases.append(("v3_unparsed_case_insensitive", HDR + v3_mixed, 1, False, "unparsed"))
```

CLI arm (added after `cli_bad_rev_rc2`):

```python
        # (R7 L5) CLI arm: a setup-class failure (unusable --repo) exits 2 with
        # one PIN_CHECK_SETUP line, never a traceback.
        cli3 = subprocess.run([sys.executable, os.path.abspath(__file__), "--rev", "HEAD",
                               "--repo", os.path.join(os.sep, "proc", "r48-execv3-nonexistent")],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        results.append(("v3_setup_error_exit2",
                        cli3.returncode == 2 and b"PIN_CHECK_SETUP" in cli3.stdout
                        and b"Traceback" not in cli3.stdout,
                        "rc=%d" % cli3.returncode))
```

## 7. Real-registry non-regression

At the freeze revision (SKILL.md identical at `e5dbac05` and `4387cf94`, sha256
`2c9772fe…`), with the round-47 baseline:

```
$ TMPDIR=$S python3 $S/v3-mori-pin-check.py --rev 4387cf94b69ddce455051a1ff38e93795c2e6cde \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
pin line=939 kind=tally prefix=C2_SELFTEST state=match pinned='pass=13 fail=0' observed='pass=13 fail=0' rc=0 cmd='python3 .ufo/waves/round-47/count-c2.py --selftest'
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=4387cf94b69ddce455051a1ff38e93795c2e6cde baseline=yes
rc=0
```

Full C1 counter run on the candidate (`count-c1.py --tool <v3> --rev 4387cf94 …`) — see
§9 (executed with a no-deadline run; result appended when it lands).

## 8. Environment notes / observed

- The lane working tree has an **uncommitted edit to `tools/mori-pin-check.py`** by a
  sibling seat (`git status` shows ` M tools/mori-pin-check.py`; working-tree sha256
  `2753087b…` ≠ committed v2 `9832e38c…`, diff shows R1–R5-style additions in flight). This
  seat's base is the committed v2 bytes; the track file was never touched by this seat.
- `git archive` invoked with `-C` pointing **inside** the lane (e.g. into
  `.scratch/…`) yields an empty tar (pax_global_header only) because git climbs to the lane
  root while the cwd is untracked — observed while designing the L5 CLI arm; matches the
  `MutV2Rebound` note about a scratch-copy default `--repo` failing with theunreadable
  SKILL.md` rc=2. Not judged here.
- Lane `.scratch` is ~6.3 GB (sibling seat artifacts); full-tree `git archive` exports at
  `--rev` are therefore heavy (~80 s for one run), which is why the full `count-c1.py`
  acceptance is run with no deadline.

## 9. C1 acceptance (count-c1.py on the candidate)

Run: `TMPDIR=$S python3 .ufo/waves/round-48/count-c1.py --tool $S/v3-mori-pin-check.py
--rev 4387cf94b69ddce455051a1ff38e93795c2e6cde --jobs 4` (lane root; no deadline).

```
variant name=J1 expect=unmet got=met rc=0
variant name=J2 expect=unmet got=met rc=0
variant name=J3 expect=unmet got=met rc=0
variant name=J4 expect=unmet got=met rc=0
variant name=J5 expect=unmet got=met rc=0
variant name=J6 expect=unmet got=met rc=0
variant name=J7 expect=unmet got=met rc=0
variant name=J8 expect=unmet got=met rc=0
variant name=H1 expect=met got=met rc=0
variant name=H2 expect=met got=met rc=0
variant name=H3 expect=met got=met rc=0
variant name=H4 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12 rev=4387cf94b69ddce455051a1ff38e93795c2e6cde
rc=1
```

Per-variant result set is byte-identical to the frozen entering-v2 receipt
`evidence/control-c1-tool-v2-entering.txt` (J1–J8 all met, H1–H4 and real met, errors=0):
the R7/R8 patch introduces **no regression** on the C1 predicate. The junk rejection itself
is R1–R6 work (other seats); the R7/R8 contribution is the mutation-killed arms (§5) and the
residual fixes, all verified green on the real registry and on all 34 v2 selftest arms.

## 10. Risks / limits

- The L4 diagnostic is scoped to spans that do **not** contain `--selftest` (command-attempt
  surface) and whose matched token has a non-empty identifier prefix — this keeps the v2
  `v2_inline_code_rejected` arm's `no_command` semantics and avoids prose false positives
  (`selftest()`, `r14-selftest-accepted.json`); both false-positive shapes were observed on
  the real registry with the first (too loose) regex and corrected before final bytes.
- All quoted outputs are observed runs with exit codes; every claim carries its command.
- UNVERIFIED: nothing material. Every command above carries its observed output and exit
  code; the C1 counter result (§9) is the final piece and is recorded in full.
