# Mo49ExecArmsHeader — selftest arms that kill the round-48 partial-removal survivors

Seat: Mo49ExecArmsHeader (leaf executor), wave w1, lane mori-shokunin. Assignment: starting from
round 49's control `.ufo/waves/round-49/controls/tool-r48-merged-witness.py`, add the `--selftest` arms
that kill every survivor listed by the round-48 mutation seats `w2/R48MutV3Header.md`,
`w2/R48MutV3Hidden.md` and `w2/R48MutV3Bind.md`; show for each survivor the mutant, the new arm name, the
arm FAIL on the mutant and PASS on the unmutated copy; keep `--selftest` green on the added copy; keep
`count-c1.py` at `C1=met`; and deliver `arms.diff` applying with `patch -p0`.

Nothing in the lane repository was written. The only files produced are this report and the scratch
directory `.scratch/r49-Mo49ExecArmsHeader/`. No tool was installed or upgraded (python3 only). The frozen
bytes were not touched: `.ufo/waves/round-49/controls/tool-r48-merged-witness.py` still hashes
`c30ab623…`, `tools/mori-pin-check.py` still `85a89a3b…` (`sha256sum`, read-only).

## Base and method

- Base copy: `.scratch/r49-Mo49ExecArmsHeader/mori-pin-check.py`, copied from
  `.ufo/waves/round-49/controls/tool-r48-merged-witness.py`, sha256
  `c30ab6232893d984d1440784b6ce962d7c987c6d5538db0ead2f458a8ea1c9f0` before any edit.
- Baseline detector: `TMPDIR=<scratch> python3 mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST
  pass=65 fail=0`, exit 0.
- Every mutant is a copy of the **arms-added** tool with one single-point edit (`diff -u` against the
  arms copy = one hunk, 2-3 changed lines; checked per mutant). Detector = the tool's own `--selftest`
  (`python3 <mutant> --selftest`, exit 0 ⇒ survivor).
- Result: the arms copy prints `PIN_CHECK_SELFTEST pass=76 fail=0`, exit 0 — eleven new arms, no false
  kill on the unmutated tool, and each of the eleven mutants is killed by the arm named for its rule.

## The eleven arms

| # | survivor (round-48 report) | rule the mutant removes/weakens | mutant (scratch) | new arm |
|---|---|---|---|---|
| 1 | R48MutV3Header.md m2r1 | R1 header aliases matched case-insensitively | `m_r1_nofold` | `r1_header_case_insensitive` |
| 2 | R48MutV3Header.md m2r2 | R2 hidden-row accounting: the `--selftest` trigger | `m_r2_notrigger` | `r2_hidden_selftest_arg_no_token` |
| 3 | R48MutV3Header.md m2r3 | R3 ASCII-strict spans: the non-ASCII first-token branch | `m_r3_nonascii` | `r3_nonascii_decorative_span` |
| 4 | R48MutV3Hidden.md #2 (m-r9a-wk) | R9a other-cell tally scan | `m_r9a_weak` | `r9a_tally_in_pinned_cell_pass_only` |
| 5 | R48MutV3Hidden.md #4 (m-r9b-wk) | R9b continuation-line scan | `m_r9b_weak` | `r9b_continuation_line_selftest_flag` |
| 6 | R48MutV3Hidden.md #6 (m-r9c-wk) | R9c tally outside backticks | `m_r9c_weak` | `r9c_tally_PASS_form_outside_backticks` |
| 7 | R48MutV3Hidden.md #10 (m-av-scratch) | `argv_ok` `/.scratch/` sub-check | `m_av_scratch` | `r7_argv_tools_scratch_rejected` |
| 8 | R48MutV3Hidden.md #11 (m-sl-rm) | `inside_tree` realpath containment | `m_sl_rm` | `r7_symlink_digest_precedes_path_containment` |
| 9 | R48MutV3Hidden.md #12 (m-sl-wk) | `inside_tree` containment separator | `m_sl_wk` | `r7_symlink_digest_prefix_sibling` |
| 10 | R48MutV3Bind.md m_r5a | R5 line-count comparison | `m_r5_gt` | `r5_line_count_overpin_mismatch` |
| 11 | R48MutV3Bind.md m_r10b | R10 digest binds to the nearest *preceding* path | `m_r10_follow` | `r10_digest_following_path_not_bound` |

New names are absent from the original control (each `grep -c` = 0 there, 1 in the copy). The added code
is insertion-only: `arms.diff` has one hunk (`@@ -984,6 +984,60 @@`), 55 inserted lines, 0 deleted lines.

## Per-survivor receipts (mutant FAIL / unmutated PASS)

### 1. R1 header aliases matched case-insensitively — arm `r1_header_case_insensitive`

- Survivor: R48MutV3Header.md m2r1 (R1 header aliases matched case-insensitively)
- Mutant: `m_r1_nofold` — `scan_lines`: header cells no longer folded — `"").lower()` → `""))` (case folding removed)
- Mutant `--selftest`: `PIN_CHECK_SELFTEST pass=75 fail=1` (rc 1)
- Unmutated copy: `PIN_CHECK_SELFTEST pass=76 fail=0` (rc 0)

```
FAIL r1_header_case_insensitive  PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r1_header_case_insensitive  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
```

### 2. R2 hidden-row accounting: the `--selftest` trigger — arm `r2_hidden_selftest_arg_no_token`

- Survivor: R48MutV3Header.md m2r2 (R2 hidden-row accounting: the `--selftest` trigger)
- Mutant: `m_r2_notrigger` — `hidden_rows` candidate/fence/other branch — `if HIDDEN_TOKEN_RE.search(raw) or "--selftest" in raw:` → token test only
- Mutant `--selftest`: `PIN_CHECK_SELFTEST pass=75 fail=1` (rc 1)
- Unmutated copy: `PIN_CHECK_SELFTEST pass=76 fail=0` (rc 0)

```
FAIL r2_hidden_selftest_arg_no_token  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r2_hidden_selftest_arg_no_token  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
```

### 3. R3 ASCII-strict spans: the non-ASCII first-token branch — arm `r3_nonascii_decorative_span`

- Survivor: R48MutV3Header.md m2r3 (R3 ASCII-strict spans: the non-ASCII first-token branch)
- Mutant: `m_r3_nonascii` — `span_kind` — the `if any(ord(c) > 127 for c in tok0): return "unparsed", "non-ascii-token"` branch deleted
- Mutant `--selftest`: `PIN_CHECK_SELFTEST pass=75 fail=1` (rc 1)
- Unmutated copy: `PIN_CHECK_SELFTEST pass=76 fail=0` (rc 0)

```
FAIL r3_nonascii_decorative_span  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r3_nonascii_decorative_span  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
```

### 4. R9a other-cell tally scan — arm `r9a_tally_in_pinned_cell_pass_only`

- Survivor: R48MutV3Hidden.md #2 (m-r9a-wk) (R9a other-cell tally scan)
- Mutant: `m_r9a_weak` — `hidden_rows` R9a site — `TALLY_TEXT_RE.search(c)` → `[A-Z][A-Z0-9_]*SELFTEST[:=]?\s*pass=\d+\s+fail=\d+`
- Mutant `--selftest`: `PIN_CHECK_SELFTEST pass=75 fail=1` (rc 1)
- Unmutated copy: `PIN_CHECK_SELFTEST pass=76 fail=0` (rc 0)

```
FAIL r9a_tally_in_pinned_cell_pass_only  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r9a_tally_in_pinned_cell_pass_only  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
```

### 5. R9b continuation-line scan — arm `r9b_continuation_line_selftest_flag`

- Survivor: R48MutV3Hidden.md #4 (m-r9b-wk) (R9b continuation-line scan)
- Mutant: `m_r9b_weak` — `hidden_rows` R9b site — drops `or "--selftest" in raw`
- Mutant `--selftest`: `PIN_CHECK_SELFTEST pass=75 fail=1` (rc 1)
- Unmutated copy: `PIN_CHECK_SELFTEST pass=76 fail=0` (rc 0)

```
FAIL r9b_continuation_line_selftest_flag  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r9b_continuation_line_selftest_flag  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
```

### 6. R9c tally outside backticks — arm `r9c_tally_PASS_form_outside_backticks`

- Survivor: R48MutV3Hidden.md #6 (m-r9c-wk) (R9c tally outside backticks)
- Mutant: `m_r9c_weak` — `check()` R9c site — `TALLY_TEXT_RE.search(...)` → `[A-Z][A-Z0-9_]*SELFTEST[:=]?\s*pass=\d+` (the `: PASS` shape dropped)
- Mutant `--selftest`: `PIN_CHECK_SELFTEST pass=75 fail=1` (rc 1)
- Unmutated copy: `PIN_CHECK_SELFTEST pass=76 fail=0` (rc 0)

```
FAIL r9c_tally_PASS_form_outside_backticks  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r9c_tally_PASS_form_outside_backticks  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
```

### 7. `argv_ok` `/.scratch/` sub-check — arm `r7_argv_tools_scratch_rejected`

- Survivor: R48MutV3Hidden.md #10 (m-av-scratch) (`argv_ok` `/.scratch/` sub-check)
- Mutant: `m_av_scratch` — `argv_ok` — the `or "/.scratch/" in "/" + path` clause removed
- Mutant `--selftest`: `PIN_CHECK_SELFTEST pass=75 fail=1` (rc 1)
- Unmutated copy: `PIN_CHECK_SELFTEST pass=76 fail=0` (rc 0)

```
FAIL r7_argv_tools_scratch_rejected  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_argv_tools_scratch_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
```

### 8. `inside_tree` realpath containment — arm `r7_symlink_digest_precedes_path_containment`

- Survivor: R48MutV3Hidden.md #11 (m-sl-rm) (`inside_tree` realpath containment)
- Mutant: `m_sl_rm` — `inside_tree` — returns `os.path.isfile(fp)` (realpath containment removed)
- Mutant `--selftest`: `PIN_CHECK_SELFTEST pass=74 fail=2` (rc 1)
- Unmutated copy: `PIN_CHECK_SELFTEST pass=76 fail=0` (rc 0)

```
FAIL r7_symlink_digest_precedes_path_containment  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_symlink_digest_precedes_path_containment  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
```

### 9. `inside_tree` containment separator — arm `r7_symlink_digest_prefix_sibling`

- Survivor: R48MutV3Hidden.md #12 (m-sl-wk) (`inside_tree` containment separator)
- Mutant: `m_sl_wk` — `inside_tree` — `realpath(root) + os.sep` → `realpath(root)` (bare string prefix)
- Mutant `--selftest`: `PIN_CHECK_SELFTEST pass=75 fail=1` (rc 1)
- Unmutated copy: `PIN_CHECK_SELFTEST pass=76 fail=0` (rc 0)

```
FAIL r7_symlink_digest_prefix_sibling  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_symlink_digest_prefix_sibling  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
```

### 10. R5 line-count comparison — arm `r5_line_count_overpin_mismatch`

- Survivor: R48MutV3Bind.md m_r5a (R5 line-count comparison)
- Mutant: `m_r5_gt` — `check()` line-count branch — `if nl != num:` → `if nl > num:`
- Mutant `--selftest`: `PIN_CHECK_SELFTEST pass=75 fail=1` (rc 1)
- Unmutated copy: `PIN_CHECK_SELFTEST pass=76 fail=0` (rc 0)

```
FAIL r5_line_count_overpin_mismatch  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r5_line_count_overpin_mismatch  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
```

### 11. R10 digest binds to the nearest *preceding* path — arm `r10_digest_following_path_not_bound`

- Survivor: R48MutV3Bind.md m_r10b (R10 digest binds to the nearest *preceding* path)
- Mutant: `m_r10_follow` — `check()` full-digest loop — `_nearest_in_tree_path(st[:dm.start()], root)` → `st[dm.end():]` (nearest following)
- Mutant `--selftest`: `PIN_CHECK_SELFTEST pass=75 fail=1` (rc 1)
- Unmutated copy: `PIN_CHECK_SELFTEST pass=76 fail=0` (rc 0)

```
FAIL r10_digest_following_path_not_bound  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r10_digest_following_path_not_bound  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
```


## Added block (fenced draft — this is exactly what `arms.diff` inserts)

```python
        # ------------------------------------------------ round-49 w1 (Mo49ExecArmsHeader):
        # killing arms for the eleven single-point survivors the round-48 mutation seats
        # reported — w2/R48MutV3Header.md m2r1/m2r2/m2r3, w2/R48MutV3Hidden.md #2/#4/#6/#10/#11/#12
        # and w2/R48MutV3Bind.md m_r5a/m_r10b. Each arm FAILs on the mutant that removes or
        # weakens its rule and PASSes on the unmutated tool (receipts in
        # .ufo/waves/round-49/w1/Mo49ExecArmsHeader.md).
        os.makedirs(os.path.join(root, "tools", ".scratch", "old"))
        with open(os.path.join(root, "tools", ".scratch", "old", "foo.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('FOO_SELFTEST pass=2 fail=0')\n")
        sibling = os.path.join(base, "treeext")
        os.makedirs(sibling)
        with open(os.path.join(sibling, "f.py"), "w") as f:
            f.write("receipt copy\n")
        os.symlink(os.path.join("..", "treeext"), os.path.join(root, "esc"))
        sibling_digest = sha256_file(os.path.join(sibling, "f.py"))
        # R1 alias spelling is matched case-insensitively (v3 m2r1 deleted `.lower()`).
        cases.append(("r1_header_case_insensitive", HDR.replace("self-test", "Self-Test", 1) + row(good),
                      1, True, None))
        # R2: a row-shaped hidden line carrying `--selftest` and no ASCII SELFTEST token (m2r2).
        cases.append(("r2_hidden_selftest_arg_no_token", HDR + row(good) + "\n"
                      "| hidd | gate | `bash tools/a.sh --selftest` | 0 ok | `clean` | none | none | mori |\n",
                      1, False, "hidden"))
        # R3: a decorative non-ASCII span that never folds to a SELFTEST prefix (m2r3).
        cases.append(("r3_nonascii_decorative_span", HDR + row(good + "; `caf\u00e9 \u2713`"), 1, False, "unparsed"))
        # R9a: another cell's tally written without `fail=` (m-r9a-wk, `pass=\d+\s+fail=\d+`).
        cases.append(("r9a_tally_in_pinned_cell_pass_only",
                      HDR + row(good, pinned="`FOO_SELFTEST pass=999`"), 1, False, "hidden"))
        # R9b: `--selftest` on a continuation line, no tally token (m-r9b-wk).
        cases.append(("r9b_continuation_line_selftest_flag",
                      HDR + row(good) + "fallback: `python3 tools/old.py --selftest`\n", 1, False, "hidden"))
        # R9c: the `NAME: PASS` tally shape outside backticks (m-r9c-wk).
        cases.append(("r9c_tally_PASS_form_outside_backticks",
                      HDR + row(good + "; also X_SELFTEST: PASS (6 cases)"), 1, False, "unparsed"))
        # argv_ok: a `tools/.scratch/…` command is rejected only by the `/.scratch/` sub-check
        # (m-av-scratch); SAFE_PATH itself accepts the shape.
        cases.append(("r7_argv_tools_scratch_rejected", HDR + row(
            "`python3 tools/.scratch/old/foo.py --selftest` \u2192 `FOO_SELFTEST pass=2 fail=0`",
            entry="`python3 tools/.scratch/old/foo.py`"), 1, False, "no_command"))
        # inside_tree: a symlink path placed before its digest is the nearest preceding path, so
        # realpath containment is what rejects it (m-sl-rm dropped containment to isfile).
        cases.append(("r7_symlink_digest_precedes_path_containment", HDR + row(
            good + "; receipt `tools/evil.py` at sha256 `%s`" % out_digest), 1, False, "mismatch"))
        # inside_tree: a realpath that carries realpath(root) only as a bare string prefix, a
        # sibling directory whose name extends the root's basename (m-sl-wk dropped `+ os.sep`).
        cases.append(("r7_symlink_digest_prefix_sibling", HDR + row(
            good + "; receipt `esc/f.py` at sha256 `%s`" % sibling_digest), 1, False, "mismatch"))
        # R5: a line-count pin claiming more lines than the file has (m_r5a flipped `!=` to `>`).
        cases.append(("r5_line_count_overpin_mismatch", HDR + row(
            "`python3 tools/lc.py --selftest` \u2192 `LC_SELFTEST pass=1 fail=0` (43 lines)",
            entry="`python3 tools/lc.py`"), 1, False, "mismatch"))
        # R10: a full digest followed by its own matching path must not bind forward (m_r10b
        # flipped nearest-preceding to nearest-following).
        cases.append(("r10_digest_following_path_not_bound", HDR + row(
            good + "; sha256 `%s` of `tools/slow.py`" % slow_digest), 1, False, "mismatch"))
```

## Full-suite receipt (arms copy, unmutated)

```
$ export TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecArmsHeader
$ python3 mori-pin-check.py --selftest > arms-selftest.txt 2>&1 ; echo EXIT=$?
EXIT=0
$ grep -c '^PASS' arms-selftest.txt ; grep '^PIN_CHECK_SELFTEST' arms-selftest.txt
76
PIN_CHECK_SELFTEST pass=76 fail=0
```

The eleven arms appear in that run as `PASS <arm name>`; the FAIL/PASS pair for each is quoted in
"Per-survivor receipts" above (the `PASS` lines there are taken from this run).

## C1 receipt (unchanged predicate, copy at the entering revision)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=$PWD/.scratch/r49-Mo49ExecArmsHeader python3 .ufo/waves/round-49/count-c1.py \
    --tool $PWD/.scratch/r49-Mo49ExecArmsHeader/mori-pin-check.py \
    --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 3 \
    --scratch $PWD/.scratch/r49-Mo49ExecArmsHeader/c1-scratch
variant name=J1 expect=unmet got=unmet rc=1
variant name=J2 expect=unmet got=unmet rc=1
variant name=J3 expect=unmet got=unmet rc=1
variant name=J4 expect=unmet got=unmet rc=1
variant name=J5 expect=unmet got=unmet rc=1
variant name=J6 expect=unmet got=unmet rc=1
variant name=J7 expect=unmet got=unmet rc=1
variant name=J8 expect=unmet got=unmet rc=1
variant name=H1 expect=met got=met rc=0
variant name=H2 expect=met got=met rc=0
variant name=H3 expect=met got=met rc=0
variant name=H4 expect=met got=met rc=0
variant name=N1 expect=unmet got=unmet rc=1
variant name=N2 expect=unmet got=unmet rc=1
variant name=N3 expect=unmet got=unmet rc=1
variant name=N4 expect=unmet got=unmet rc=1
variant name=N5 expect=unmet got=unmet rc=1
variant name=N6 expect=unmet got=unmet rc=1
variant name=N7 expect=unmet got=unmet rc=1
variant name=N8 expect=unmet got=unmet rc=1
variant name=N9 expect=unmet got=unmet rc=1
variant name=H6 expect=met got=met rc=0
variant name=H7 expect=met got=met rc=0
variant name=N10 expect=unmet got=unmet rc=1
variant name=H5 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
variant name=real-opaque expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
EXIT=0
```

Full receipt: `.scratch/r49-Mo49ExecArmsHeader/c1-arms.txt` (wall 950 s). `--jobs 3` as instructed.

## arms.diff

- Path: `.scratch/r49-Mo49ExecArmsHeader/arms.diff` (sha256 `544dd6efc9c5e88ad7418dedb430c44848568e428ac58d640f3c016f051e9a12`).
- Headers carry the lane-relative path, so `patch -p0` applies from the lane root:
  `cd /home/vgpnk/Projects/shokunin/mori-shokunin && patch -p0 < .scratch/r49-Mo49ExecArmsHeader/arms.diff`.
- Applied proof (throwaway tree, the frozen control itself never written):
  `mkdir -p $T/.ufo/waves/round-49/controls`, copy the control there, `cd $T && patch -p0 < arms.diff` →
  `patching file .ufo/waves/round-49/controls/tool-r48-merged-witness.py`; `cmp` of the patched file
  against the arms copy → identical; both sha256 `84c5e4cc90f1378aaa9f02ac38665b62e3f1ab2bd116a83c32a51a6d60e385d1`.

## Provenance

- Arms copy sha256 (after the edit): `84c5e4cc90f1378aaa9f02ac38665b62e3f1ab2bd116a83c32a51a6d60e385d1`.
- Mutant sha256: m_r1_nofold `52762bcb9530141d397371d92085ce820b0bfe3bc4cf5a8f24cca43ee1ed09f0`
m_r2_notrigger `ab18c4cd83f9415a9cf93af8873f799d5c5922bbaa9b64b8a36a16811c83a1f7`
m_r3_nonascii `7f868fc837469b6ae4a55fb06f3cd2cbc4ca1a7857148a005270fb0df343e8e4`
m_r9a_weak `76660c0a3ba5cbf12711bcc5b7437ded88fc89b8b009a36645eceab1c95ea5fd`
m_r9b_weak `b7805dd93710dc7f396074ce86ebc5aa1e80520396327589be5c09b5b59b7961`
m_r9c_weak `1b82cda5d53ab8b42953574121f51a866b3bcdd4d37bacddf4235443ed2c12c9`
m_av_scratch `a3a809a3494f7f7f0bb25654045f3151b4ad9c71d8b9a517ca7c57230dd156e0`
m_sl_rm `c18493ddfadabe3d99e9fda37b21b9ea78887514e22d330fa22f3c2507018271`
m_sl_wk `758560371ee5b33bd4fa91bfa85f761886684501d44c5cb6d0a8d630d690c89d`
m_r5_gt `ffda30fe56e56a59d9f9b188f90a6c6913717c1328655b2f04a5f8bdb3f23a6e`
m_r10_follow `f9d244dea654e77855266af794338f0649a3dd91d558fd4858ba75b0bd6cfd8b`
- Scratch: `.scratch/r49-Mo49ExecArmsHeader/` (`mori-pin-check.py`, `m_*.py`, `m_*.selftest.txt`,
  `arms-selftest.txt`, `arms.diff`, `c1-arms.txt`, `c1-scratch/`). Every lane-tool run used
  `TMPDIR=<scratch>`; the selftest builds its trees under that TMPDIR.
- No git/jj mutating command was run. `git status --porcelain -uno` shows only a sibling seat's
  `M corpus/SOURCES.md`; no path I touched is tracked.

## Limits

- Detector is the tool's own `--selftest` only; `count-c1.py` does not run `--selftest` (the contract
  says so), so these arms add no C1 signal — the C1 receipt above shows only that the arms did not
  disturb the byte-level predicate.
- Single-point mutants only, one per survivor, at the site the round-48 seat mutated. A compound or
  differently-shaped weakening of the same rules is untested here.
- I kept the pre-existing arm `r7_symlink_digest_not_inside` unchanged (it is mis-bound: the digest
  precedes the symlink path, so R10 binds `tools/foo.py`). The corrected-order arm
  `r7_symlink_digest_precedes_path_containment` is the one that actually exercises the symlink; leaving
  both means the suite carries one arm whose name overstates its coverage.
- `m_sl_rm` (containment removed) fails both symlink arms — the second is `r7_symlink_digest_prefix_sibling`.
  That is a consequence of the rule, not a false red: the unmutated tool passes both.
- `r7_argv_tools_scratch_rejected` differs from the arm text proposed in `R48MutV3Hidden.md` §A4: the
  entry cell names the same `tools/.scratch/old/foo.py` instrument instead of "no command here", so the
  only difference left between pristine and mutant is the `/.scratch/` sub-check (with "no command here"
  the mutant also trips R11 `misattributed`, which is a weaker isolation).
- `r7_symlink_digest_prefix_sibling` is discriminating only while the sibling file's bytes differ from
  every in-tree file that can serve as the nearest-preceding fallback (`tools/foo.py`). My first draft
  wrote `TOOL` into `treeext/f.py`; the digest then also matched `tools/foo.py` and the arm false-redded
  on the unmutated tool (`FAIL r7_symlink_digest_prefix_sibling PIN_CHECK=met`). The shipped fixture writes
  `receipt copy\n`, which is unique in the fixture tree.

## Findings

- **MED** — `.ufo/waves/round-49/controls/tool-r48-merged-witness.py` selftest arm `r7_symlink_digest_not_inside`
  (line 938 of the arms copy, unchanged by this seat) is mis-bound: the symlink path follows the digest, so
  the digest binds to `tools/foo.py` and the arm passes without resolving the symlink. Backed by the new
  `r7_symlink_digest_precedes_path_containment`, but the old arm's name still overstates what it tests.
- **MED** — the same control's R9a/R9c arms only exercise the `NAME pass=N fail=M` tally shape; before this
  change a weakened `TALLY_TEXT_RE` (`pass=\d+` without `fail=`, or `: PASS` dropped) survived 60/60 arms
  (`w2/R48MutV3Hidden.md` #2/#6). Now killed by `r9a_tally_in_pinned_cell_pass_only` and
  `r9c_tally_PASS_form_outside_backticks`.
- **MED** — R1 case folding, the R2 `--selftest` trigger, the R3 non-ASCII branch, the R9b `--selftest`
  alternative, argv_ok's `/.scratch/` sub-check, `inside_tree` containment (removed and separator-lost),
  R5's `!=`→`>`, and R10's preceding→following flip each survived the 60-arm suite. Each is now killed by
  the arm named for it in the table above; the arms copy is 76/76 green.
- **LOW** — `r7_symlink_digest_prefix_sibling` is byte-sensitive: if the sibling fixture ever shares bytes
  with `tools/foo.py` the arm false-reds on the tool (observed once in this seat, fixed by distinct sibling
  bytes). Anyone editing the fixture should keep the sibling content unique.
- **LOW** — the witness is a control, not the claim's tool. The arms are black-box (they assert only
  `met`/`unmet` and a state token), and ten of the eleven mutated site strings occur verbatim in the
  entering `tools/mori-pin-check.py` (`85a89a3b…`); the R1 fold is written there as
  `low = [c.lower() for c in cells]` (v3 line 201) instead of the witness's NFKC chain. I did not apply
  `arms.diff` to `tools/mori-pin-check.py`; landing the arms on the claim's tool is the L1's step.
