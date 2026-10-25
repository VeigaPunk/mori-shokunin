# R48MutV3Hidden — w2 falsify: mutation-testing the v3 pin-checker's selftest arms

**Attacked:** the landed v3 instrument `tools/mori-pin-check.py` (blob `85a89a3b…`, byte-equal at tip
`e4dfff3`) via its own bounded detector `--selftest` (exit ≠ 0 ⇒ mutant killed). Twelve single-point
mutants, two per assigned rule: R9a other-cell tallies, R9b continuation lines, R9c tally outside
backticks, R7 `split_cells` backslash-parity, `argv_ok` sub-checks, digest symlink containment.

**Verdict: BREAKS — class: R8 arm-coverage gap (weak or mis-bound oracle arms).** 6/12 mutants are
killed; 6/12 survive `python3 <mutant> --selftest` with exit 0 and pass 60/60 arms, and each survivor
has a SKILL.md variant the mutant scores `met` and the real tool scores `unmet`. Worst case: a mutant
that **removes symlink containment entirely** (`m-sl-rm`) survives, because the arm
`r7_symlink_digest_not_inside` binds the digest to `tools/foo.py` (R10 nearest-preceding) and never
consults the symlink — it would pass even with the symlink deleted. This is a limit of the
instrument's self-verification (v3-spec R8: "every new arm is killed by the mutation that removes its
rule"); it is **not** evidence against P-C1 itself — `count-c1.py` does not run the tool's `--selftest`
(whether C1 still prints `C1=met`: UNVERIFIED, not this seat's detector).

## Baseline (pristine)

- `TMPDIR=<scratch> python3 pristine.py --selftest` → `PIN_CHECK_SELFTEST pass=60 fail=0`, exit 0.
- `sha256(pristine.py)` = `sha256(tools/mori-pin-check.py)` = `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`
  = `git show e4dfff32…:tools/mori-pin-check.py` (read-only check).

## Mutation table (killed ⇔ selftest exit ≠ 0)

| # | rule | mutant (single-point, scratch copy) | change | `--selftest` | killing arm (FAIL line) / survivor |
|---|------|----------|--------|--------------|-------------------------------------|
| 1 | R9a | `m-r9a-rm.py` | `if ci != idx and TALLY_TEXT_RE.search(c):` → `if False and …` (other-cell tally scan disabled) | rc=1, 59/60 | KILLED — `r9a_tally_in_pinned_values_cell` (expects hidden; mutant reports met) |
| 2 | R9a | `m-r9a-wk.py` | same site: pattern → `[A-Z][A-Z0-9_]*SELFTEST\s+pass=\d+\s+fail=\d+` (requires `fail=`) | **rc=0, 60/60** | SURVIVED — reproducer §A1; killing arm §A1 |
| 3 | R9b | `m-r9b-rm.py` | `elif kind == "other" and re.match…` → `elif False and …` (continuation-line scan disabled) | rc=1, 59/60 | KILLED — `r9b_continuation_line_tally` |
| 4 | R9b | `m-r9b-wk.py` | `if TALLY_TEXT_RE.search(raw) or "--selftest" in raw:` → drops the `--selftest` alternative | **rc=0, 60/60** | SURVIVED — reproducer §A2; killing arm §A2 |
| 5 | R9c | `m-r9c-rm.py` | `if TALLY_TEXT_RE.search(SPAN_RE.sub(" ", st)):` → `if False and …` (outside-backticks check disabled) | rc=1, 59/60 | KILLED — `r9c_tally_outside_backticks` |
| 6 | R9c | `m-r9c-wk.py` | same site: pattern → `[A-Z][A-Z0-9_]*SELFTEST[:=]?\s*pass=\d+` (drops `: PASS` form) | **rc=0, 60/60** | SURVIVED — reproducer §A3; killing arm §A3 |
| 7 | R7 split_cells | `m-r7sc-v2.py` | `if bs % 2 == 0:` → `if bs == 0:` (v2 one-backslash regression: `\\|` mis-split) | rc=1, 59/60 | KILLED — `r7_escaped_double_backslash_pipe` (row becomes unparsed) |
| 8 | R7 split_cells | `m-r7sc-ne.py` | `if bs % 2 == 0:` → `if True:` (no escape handling; every `\|` splits) | rc=1, 59/60 | KILLED — `escaped_pipe_cell` (v2 arm; row becomes unparsed) |
| 9 | argv_ok | `m-av-dotdot.py` | drops `".." in path.split("/")` sub-check | rc=1, 59/60 | KILLED — `r7_argv_dotdot_rejected` (binds the command; `state=no_command` never appears) |
| 10 | argv_ok | `m-av-scratch.py` | drops `"/.scratch/" in "/" + path` sub-check | **rc=0, 60/60** | SURVIVED — reproducer §A4; killing arm §A4 |
| 11 | symlink containment | `m-sl-rm.py` | `inside_tree` → `return os.path.isfile(fp)` (realpath containment removed) | **rc=0, 60/60** | SURVIVED — reproducer §A5; killing arm §A5 |
| 12 | symlink containment | `m-sl-wk.py` | containment prefix loses `+ os.sep` (`startswith(realpath(root))`) | **rc=0, 60/60** | SURVIVED — reproducer §A6; killing arm §A6 |

All mutants verified single-point: `diff pristine.py <mutant>` = one hunk, 2 changed lines (3 for
`m-sl-rm`'s two-line return collapse). Detector runs: `TMPDIR=<scratch> python3 <mutant> --selftest`,
each < 60 s.

## Why the survivors live (root causes)

- **#2 / #6:** the R9a/R9c arms are written in exactly one tally shape, `NAME pass=N fail=M` — the
  same shape the weakened patterns still match. `TALLY_TEXT_RE`'s other shapes (`pass=N` without
  `fail=`; `NAME: PASS`) are never exercised in another cell (R9a) or outside backticks (R9c), so the
  weakenings lose real coverage without failing any arm.
- **#4:** the R9b arm's continuation line carries only a tally token; no arm puts `--selftest` on a
  continuation line, so dropping that alternative is invisible to the suite — yet `--selftest` on a
  continuation line is precisely a hidden alternate command (the junk D2 class).
- **#10:** `v2_scratch_path_rejected` uses `.scratch/old/foo.py`, which `SAFE_PATH` already rejects
  (it does not start `tools/`/`.ufo/waves/round-N/`), so the arm does not isolate the `/.scratch/`
  sub-check. Only shapes like `tools/.scratch/…` reach it.
- **#11:** `r7_symlink_digest_not_inside` places the symlink path **after** the digest
  (``… at sha256 `<hex>` of `tools/evil.py` ``). Under R10 (nearest **preceding** in-tree path) the
  binding is `tools/foo.py`, so the mismatch comes from foo.py's hash and the symlink is never
  resolved. The arm is mis-bound and would stay green with `inside_tree` reduced to `isfile`.
- **#12:** no arm references a path whose realpath carries `realpath(root)` as a bare string prefix
  (sibling directory whose name extends the root's basename), so the missing separator is unexercised.

## Reproducers (survivor scores `met`/rc=0, pristine scores `unmet`/rc=1; driver `repro.py`)

Fixture spine for all: 8-column header `HDR` (self-test at cell 4), row
`| foo | gate | <entry> | 0 ok | <self-test cell> | none | none | mori |`,
`tools/foo.py` prints `noise line` + `FOO_SELFTEST pass=3 fail=0`, rc 0.
Run: `python3 <tool> --root <tree> --repo <scratch>`.

### A1 — m-r9a-wk (`pinned values` cell, `pass=` without `fail=`)

Self-test cell: `` `python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0` ``;
pinned-values cell: `` `FOO_SELFTEST pass=999` ``.
- pristine rc=1 `… hidden=1` (other-cell tally); mutant rc=0 `… hidden=0` (pattern needs `fail=`).
- Killing arm text: `cases.append(("r9a_tally_in_pinned_cell_pass_only", HDR + row(GOOD, pinned="\`FOO_SELFTEST pass=999\`"), 1, False, "hidden"))`

### A2 — m-r9b-wk (`--selftest` on a continuation line)

Row = honest GOOD row; directly under it the line
`fallback: `python3 tools/old.py --selftest`` (`tools/old.py` prints `FOO_SELFTEST pass=2 fail=0`).
- pristine rc=1 `… hidden=1`; mutant rc=0 `… hidden=0` (line carries no tally token).
- Killing arm text: `cases.append(("r9b_continuation_line_selftest_flag", HDR + row(GOOD) + "fallback: \`python3 tools/old.py --selftest\`\n", 1, False, "hidden"))`

### A3 — m-r9c-wk (`: PASS` form outside backticks)

Self-test cell: `` `python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`; also X_SELFTEST: PASS (6 cases) ``.
- pristine rc=1 `… unparsed=1` (reason=tally-outside-backticks); mutant rc=0 `… unparsed=0`.
- Killing arm text: `cases.append(("r9c_tally_PASS_form_outside_backticks", HDR + row(GOOD + "; also X_SELFTEST: PASS (6 cases)"), 1, False, "unparsed"))`

### A4 — m-av-scratch (`tools/.scratch/…` bound path)

`tools/.scratch/old/foo.py` prints `noise line` + `FOO_SELFTEST pass=2 fail=0`; self-test cell:
`` `python3 tools/.scratch/old/foo.py --selftest` → `FOO_SELFTEST pass=2 fail=0` `` (entry `no command here`).
`SAFE_PATH` fullmatches this shape; only the `/.scratch/` sub-check rejects it.
- pristine rc=1 `… no_command=1`; mutant rc=0 — runs the scratch tool and scores `met`.
- Killing arm text: `cases.append(("r7_argv_tools_scratch_rejected", HDR + row("\`python3 tools/.scratch/old/foo.py --selftest\` → \`FOO_SELFTEST pass=2 fail=0\`", entry="no command here"), 1, False, "no_command"))`

### A5 — m-sl-rm (symlink resolved through to outside the tree)

`tools/evil.py` → symlink to `<base>/outside.py` (`x = 1\n`); self-test cell:
`` GOOD ; receipt `tools/evil.py` at sha256 `<sha256(outside.py)>` `` — symlink path **before** the digest.
- pristine rc=1 `kind=digest state=mismatch` (realpath outside tree); mutant rc=0 `state=match`
  (sha256 read through the link).
- Killing arm: reorder the existing arm so the symlink is the nearest **preceding** path —
  `cases.append(("r7_symlink_digest_not_inside", HDR + row(GOOD + "; receipt \`tools/evil.py\` at sha256 \`%s\`" % out_digest), 1, False, "mismatch"))`

### A6 — m-sl-wk (realpath string-prefix sibling)

Layout `<base>/case/tree` (measured root) with `tree/esc` → symlink to `<base>/case/treeext`;
`treeext/f.py` = `receipt copy\n`; self-test cell:
`` GOOD ; receipt `esc/f.py` at sha256 `<sha256(treeext/f.py)>` ``.
`realpath(fp)` = `…/case/treeext/f.py` starts-with `realpath(root)` = `…/case/tree` only as a string
prefix; without `+ os.sep` containment passes.
- pristine rc=1 `state=mismatch file=tools/foo.py`; mutant rc=0 `state=match file=esc/f.py`
  (reproduced twice, deterministic).
- Killing arm text: `cases.append(("r7_symlink_digest_prefix_sibling", HDR + row(GOOD + "; receipt \`esc/f.py\` at sha256 \`%s\`" % sibling_digest), 1, False, "mismatch"))` in a fixture where `tree/esc` → `../treeext`.

Driver run (all six, after fixing a path-level bug in my own `build_slwk` — first run had
`treeext` one level too high, which legitimately failed to trigger the prefix weakness):

```
r9a-wk     pristine rc=1 … hidden=1 | mutant rc=0 … hidden=0
r9b-wk     pristine rc=1 … hidden=1 | mutant rc=0 … hidden=0
r9c-wk     pristine rc=1 … unparsed=1 | mutant rc=0 … unparsed=0
av-scratch pristine rc=1 … no_command=1 | mutant rc=0 … all zero
sl-rm      pristine rc=1 … mismatches=1 | mutant rc=0 … mismatches=0
sl-wk      pristine rc=1 … mismatches=1 | mutant rc=0 … mismatches=0
```

## Restoration evidence

- The tracked file was never opened by an edit tool; work happened only on scratch copies under
  `.scratch/r48w2-R48MutV3Hidden/` (`pristine.py`, 12 `m-*.py`, `repro.py`, temp fixtures, all
  removed or left in scratch).
- After all runs: `sha256(tools/mori-pin-check.py)` = `85a89a3b…` (identical to pre-run and to tip
  blob), `git status --porcelain tools/mori-pin-check.py` → empty.
- No git/jj mutating command was run; no file outside scratch + this report was written.

## Limits

- Detector = the tool's own `--selftest` (60 arms) plus the six reproducer pairs above; the C1/C2
  counters were not run (not this seat's instrument). Whether the survivors imply anything about
  `C1=met` at the tip is UNVERIFIED here.
- One mutation pair per rule by assignment; other rule surfaces (R1-R6, R10, R4 rebinding) untouched.
- Scratched mutants are disposable; the reproducers above are the durable record.

Report: .ufo/waves/round-48/w2/R48MutV3Hidden.md
