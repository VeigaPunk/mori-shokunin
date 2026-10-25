# ExecRegistryAuditor — gate-registry auditor v2 (C2, P-C2)

Files written (both mine, nothing else touched):

- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-gate-registry.py` — v2, 743 lines,
  sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/fixtures/mutants/mori-gate-registry.py`
  — the v2 bytes plus one inserted line, 744 lines, sha256
  `38d5551a4570ed23e4ab6ceccfc22e506212164132e9dd411aaec8e699f3f13d`
- this report.

CLI shape kept: `--rev`, `--registry`, `--repo`, `--audit` (repeatable),
`--selftest`, verdict `REGISTRY=met|unmet|REGISTRY_SETUP` on exit 0/1/2. Added
`--audit-all` (population mode). The r44 consumer shape still prints
`REGISTRY=met` rc 0, so `.ufo/waves/round-44/count-c2.py` keeps working.

## What the auditor does (P-C2 items 1–6, plus the two critic hardenings)

1. **Whole-file table scope.** `parse_tables()` scans every line of the registry
   file and starts a table at *any* row whose cells (case-insensitive, trimmed)
   equal the eight standard cells; it reads the contiguous `|` rows after it
   (separator rows skipped) and continues scanning after the table. `tables=7`
   over the current `SKILL.md` (headers at lines 162, 524, 588, 643, 718, 796,
   881). A different header is not a table and never a finding.
2. **Own-row attribution.** Only a row whose `entry` cell's *first backticked
   command* invokes the audited path attributes it: `entry_target()` tokenises
   the first backticked span, drops env assignments, `-`-flags and the wrapper
   words (`bash`/`sh`/`python3`/`env`/`time`/…), and takes the first token that
   is a path or `*.py`/`*.sh`; `entry_names()` compares it with the normalised
   audited path. The r44 substring fallback (`base in cell or name in cell`) is
   gone. The attributed name prints as `row='<name>'`; first matching row in
   file order wins.
3. **Duplicate rejection.** Names are collected across all tables; every name
   occurring more than once prints `duplicate name='<n>' lines=<a>,<b>` and
   forces `REGISTRY=unmet`.
4. **Real self-test branch.** Comments and Python triple-quoted blocks are
   blanked first (`mask_python` / `mask_shell`); an occurrence in a comment or
   docstring never counts. Python then requires a parser key
   (`add_argument`/`add_option`), a flag comparison (`== ["--selftest"]`), or a
   membership test whose operand is an argv name (`if "--selftest" in raw:`),
   gated on the file actually parsing argv (`sys.argv`, `argv`, argparse). Shell
   requires the flag as a `case` pattern (`--selftest)`) or an argv marker in a
   three-line window (`$1`, `$@`, `$#`, `case`, `shift`, …).
5. **`--audit-all` population.** `population()` enumerates `tools/*.py`,
   `tools/*.sh`, `.ufo/waves/round-44/count-c*.py` and
   `.ufo/waves/round-45/count-c*.py` **at `--rev`** (`git ls-tree`, direct
   children only; `tools/fixtures` is a directory and is not counted). A
   population run prints `mode=population` and
   `population_digest=<sha256 of the newline-joined sorted target list>`, so the
   audited set is reproducible from the receipt, then the counter line
   `registered=<n> unregistered=<n> no_selftest=<n> duplicate=<n> wrong_row=<n>
   tables=<n>`.
6. **Setup and path safety.** `git rev-parse --verify <rev>^{commit}` runs inside
   the `try`; `subprocess.TimeoutExpired` and every other exception print
   `REGISTRY_SETUP …` and exit 2. Every git child runs with `GIT_*` scrubbed
   (`child_env()`). `--repo` is `os.path.abspath`ed. `safe_relpath()` rejects
   absolute paths and any `..` escape for both audited paths and row entry paths
   before any read; under `WORK` reads are additionally `realpath`-contained.
   An empty population is `REGISTRY_SETUP`, never `met`.

**Critic hardening A — modes are exclusive.** `--audit` together with
`--audit-all` is now `REGISTRY_SETUP` exit 2: a population run can never silently
audit one explicit path and call the population clean. Previously the explicit
list won and printed `REGISTRY=met` for `registered=1`.

**Critic hardening B — the escape cannot be a false cell.** `selftest-flag=<flag>`
is accepted only when (i) the declared flag name contains `test` (so `--a` and
`--repo` are refused) and (ii) the tool's masked bytes carry it as a **parser
key** (`add_argument("--self-test")`) or a **shell `case` pattern**
(`--self-test)`), never as a mere mention. A row that declares a flag the tool
does not hook is `no_selftest`. Declaring the standard flag
(`selftest-flag=--selftest`) is harmless: it falls back to the normal route.

**Detector refinement forced by a real branch.** The round-24 routed counter's
genuine branch is `if "--selftest" in raw:` (the `raw` binding is three lines
above), which the earlier two-line window missed. Python detection is now
pattern-based (parser key / flag comparison / membership test against an argv
name) gated on the file parsing argv, so a real branch is not called
`no_selftest`; shell keeps the window plus an unconditional `case`-pattern
accept. The comment-only arm still fails.

`wrong_row` means: an audited path attributed to a malformed row (wrong cell
count, empty standard cell, entry path absent/escaping), plus any registry row
whose entry path is absent at the revision or leaves the repo. It is summed on
the counter line so a malformed row can never vanish between `registered` and
`unregistered`.

## Evidence (unrun checks are not claimed)

Selftest, rc, arms — `TMPDIR=.ufo/waves/round-45/tmp/ExecRegistryAuditor`:

```
$ TMPDIR=$PWD/.ufo/waves/round-45/tmp/ExecRegistryAuditor python3 tools/mori-gate-registry.py --selftest
selftest PASS registered_row_met
selftest PASS missing_cell_rejected
selftest PASS unresolved_entry_rejected
selftest PASS unregistered_path_rejected
selftest PASS no_selftest_rejected
selftest PASS seven_cell_row_rejected
selftest PASS second_table_registered
selftest PASS duplicate_name_rejected
selftest PASS comment_only_selftest_rejected
selftest PASS empty_population_rejected
selftest PASS audit_all_with_audit_refused
selftest PASS population_mode_and_digest
selftest PASS escape_flag_accepted
selftest PASS escape_flag_name_rejected
selftest PASS escape_flag_mention_rejected
GATE_REGISTRY_SELFTEST pass=15 fail=0
rc=0
```

(The nine required arms, `empty_population_rejected`, and one arm per critic
refusal plus the positive escape. Every arm builds an isolated throwaway git
repo under `$TMPDIR` via `_mk()`.)

Mode refusal and population receipt (worktree):

```
$ python3 tools/mori-gate-registry.py --rev WORK --audit tools/mori-census.sh --audit-all
REGISTRY_SETUP --audit cannot be combined with --audit-all: population mode enumerates the declared population and takes no explicit paths
rc=2
```
```
$ python3 tools/mori-gate-registry.py --rev WORK --audit-all
…
tables=7
rev=WORK
mode=population
population_digest=2d1e9096f7622639f3bb45624ffee594caa81c05ee200c9a22323f86d4a9c056
registered=33 unregistered=6 no_selftest=0 duplicate=0 wrong_row=0 tables=7
REGISTRY=unmet
rc=1
```

An independent enumeration (filesystem `tools/*.py|sh` + both counter globs,
sorted, newline-joined) gives `n=39 sha256=2d1e9096…c056` — identical to the
tool's `population_digest`.

Entering tip `554ff416` (stable receipt, 36 paths):

```
… 29 PASS, 7 FAIL …
audit tools/mori-disk-rate.py           FAIL (no row names tools/mori-disk-rate.py)
audit tools/mori-round19-regressions.py FAIL row='r19 finite regressions' (… no real --selftest argv branch)
audit tools/mori-round41-calibration.py FAIL (no row names tools/mori-round41-calibration.py)
audit tools/mori-routed-check.py        FAIL row='routed round-23 items (r24, C1)' (… no real --selftest argv branch)
audit tools/mori-routed-r24.py          FAIL row='routed round-24 items (r25, C1)' (… no real --selftest argv branch)
audit tools/mori-silence-cases.sh       FAIL row='silence oracle' (… no real --selftest argv branch)
audit tools/mori-wave-settlement.py     FAIL (no row names tools/mori-wave-settlement.py)
tables=7
rev=554ff416459c92f0dea9762f834a556df2990187
mode=population
population_digest=4dbf0ca9823d2af1d6de352b54138bbc261c68a10c9a81e6ef77eb88576292f1
registered=29 unregistered=3 no_selftest=4 duplicate=0 wrong_row=0 tables=7
REGISTRY=unmet
rc=1
```

r44 consumer shape (what `.ufo/waves/round-44/count-c2.py` invokes):

```
$ python3 tools/mori-gate-registry.py --rev 554ff416 --repo . \
    --audit .ufo/waves/round-44/count-c1.py --audit .ufo/waves/round-44/count-c2.py \
    --audit .ufo/waves/round-44/count-c3.py
… 3 × PASS …
registered=3 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=7
REGISTRY=met
rc=0
```

Path safety, `..`/absolute entry rows, `GIT_*` scrub (throwaway repo; rows name
`../outside.sh` and `/etc/hostname`; `GIT_DIR` set in the parent):

```
$ GIT_DIR=/nonexistent/gitdir python3 tools/mori-gate-registry.py --rev ba1da0d3 \
    --repo <tmp>/escape/repo --audit tools/ok.sh --audit ../outside.sh
audit tools/ok.sh            FAIL (no row names tools/ok.sh)
audit ../outside.sh          FAIL (audited path is absolute or outside the repo)
wrong_row line=5 row='outside' entry=../outside.sh absolute or outside the repo
wrong_row line=6 row='abs' entry=/etc/hostname absolute or outside the repo
registered=0 unregistered=2 no_selftest=0 duplicate=0 wrong_row=2 tables=1
REGISTRY=unmet
rc=1
```

Setup exits: unresolvable revision → `REGISTRY_SETUP cannot resolve revision
'deadbeef00'` rc=2; absent registry → `REGISTRY_SETUP registry absent at
554ff416459c: NOPE.md` rc=2; usage → `REGISTRY_SETUP usage` rc=2.

Attribution/duplicate/malformed/escape fixtures (throwaway repos):

```
# a path named only in another row's PROSE is not attributed
audit tools/prose-tool.sh  FAIL (no row names tools/prose-tool.sh)   … tables=1   rc=1
# duplicate name across two tables
duplicate name='same' lines=7,13
registered=1 unregistered=0 no_selftest=0 duplicate=1 wrong_row=0 tables=2        rc=1
# malformed row is counted, never invisible
audit tools/t.sh  FAIL row='t' (row has 7 cells, expected 8)
registered=0 unregistered=0 no_selftest=0 duplicate=0 wrong_row=1 tables=1        rc=1
# escape refused when the flag name lacks 'test', even though the tool hooks it
audit tools/t.sh  FAIL row='t' (row 't' declares selftest-flag --check, but tools/t.sh has no --check parser key or case pattern (a self-test flag name must also contain 'test'))
registered=0 unregistered=0 no_selftest=1 duplicate=0 wrong_row=0 tables=1        rc=1
# escape accepted for a self-test-named, actually hooked case pattern
audit tools/t.sh  PASS row='t' (8 cells, entry resolves, --self-test argv branch)
registered=1 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=1        rc=0
# escape refused when the flag is only mentioned (inside a printf under case)
audit tools/t.sh  FAIL row='t' (row 't' declares selftest-flag --self-test, but tools/t.sh has no --self-test parser key or case pattern …)
registered=0 unregistered=0 no_selftest=1 duplicate=0 wrong_row=0 tables=1        rc=1
```

The same three shapes are pinned as selftest arms (`escape_flag_accepted`,
`escape_flag_name_rejected`, `escape_flag_mention_rejected`).

Determinism: two `--audit-all` runs at one revision are byte-identical.

## Mutant (delivered)

`fixtures/mutants/mori-gate-registry.py` is the v2 bytes with one inserted line
in `parse_tables()` (`break  # MUTANT: read only the FIRST registry table`),
disabling exactly the whole-file table check. `diff -u` shows only that
`@@ -225,6 +225,7 @@` hunk.

```
$ python3 .ufo/waves/round-45/fixtures/mutants/mori-gate-registry.py --selftest
selftest FAIL second_table_registered: a row in a second table was not read: {… 'tables': 1 …}
GATE_REGISTRY_SELFTEST pass=14 fail=1
rc=1
$ python3 …/mutants/mori-gate-registry.py --rev WORK --audit-all
mode=population
population_digest=2d1e9096…c056
registered=22 unregistered=17 no_selftest=0 duplicate=0 wrong_row=0 tables=1
REGISTRY=unmet
rc=1
```

The mutant is caught by its own `--selftest` and prints `unmet`, never `met`.

## One defect I found and fixed in my own build

`--repo` used to default to `dirname(dirname(__file__))`. A relocated copy (the
mutant under `.ufo/…/fixtures/mutants/`) therefore pointed at `…/fixtures`,
where the population is empty — and `git -C` walks up to the lane repo, so it
read the real `SKILL.md`, audited zero paths and printed `REGISTRY=met rc=0`.
Fixed by `repo_default()` walking up to the nearest ancestor holding `tools/`
and `SKILL.md`, plus `audit()` raising `empty population: an audit with no paths
cannot be met`. Arm `empty_population_rejected` pins it; consumers should still
pass `--repo` explicitly.

## Measurement against the L1's expectation (not adjusted)

Expected after the row seats land: `registered=39 unregistered=0 no_selftest=0
duplicate=0 wrong_row=0 tables=7` (33 `tools/*.py|sh` + 3 round-44 counters + 3
round-45 counters).

Measured on the worktree at 2026-10-25T07:58:50-03:00:
`registered=33 unregistered=6 no_selftest=0 duplicate=0 wrong_row=0 tables=7`,
`GATE_REGISTRY_SELFTEST pass=15 fail=0` rc=0, `REGISTRY=unmet` rc=1, digest
`2d1e9096…c056` (39 paths).

The six residuals are all missing rows, not missing branches: the three r45
counters (`.ufo/waves/round-45/count-c1.py|c2.py|c3.py`) and the three orphan
tools (`tools/mori-disk-rate.py`, `tools/mori-wave-settlement.py`,
`tools/mori-round41-calibration.py`). All six tools/counters now carry a real
`--selftest` argv branch (verified individually: `mori-disk-rate.py` parser key,
`mori-wave-settlement.py` parser key, `mori-round41-calibration.py`
`if "--selftest" in argv:`, and the three counters), so landing the rows should
reach `registered=39 … no_selftest=0`. `SKILL.md` is still unmodified
(`git status --porcelain -- SKILL.md` empty; a 240-second watcher on `SKILL.md`
and `HEAD` saw no change), so the rows had not landed when I measured; I may not
write `SKILL.md`.

## Copy-paste candidate for SKILL.md (L1 integrates; I may not edit it)

The `r44 gate registry (C2)` row claims `pass=6`, which this build supersedes.
The replacement row below was validated with the auditor itself (scratch repo:
`PASS row='r44 gate registry (C2)'`, `REGISTRY=met rc=0`). It needs the
`pass=15` tally and the new verdict map updated by the L1 if the arm list is
cited:

```
| r44 gate registry (C2) | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <repo-relative path> [--audit ...]` or `--audit-all` (`--registry PATH`, `--repo PATH`, `--selftest`) | 0 `REGISTRY=met` · 1 `REGISTRY=unmet` (unregistered path, a row that does not name the audited path, a missing standard cell, an entry path that does not resolve at the revision, a duplicate registry name, a wrong row, or no real self-test argv branch in the tool) · 2 `REGISTRY_SETUP` (usage, `--audit` with `--audit-all`, unresolvable revision, git timeout, absent registry or gate table, empty population) | `python3 tools/mori-gate-registry.py --selftest` → `GATE_REGISTRY_SELFTEST pass=15 fail=0`: good row, missing cell, unresolved entry, unregistered path, tool without `--selftest`, seven-cell row, row in a second table, duplicate name, comment-only `--selftest`, empty population, `--audit`+`--audit-all` refusal, population mode/digest, escape accepted, escape name refused, escape mention refused | in-script fixture registry rows; the audited surface is every eight-cell table in this SKILL.md at `--rev`; population runs print `population_digest` | stdout only; reads the registry and tool bytes at `--rev`; selftest writes only throwaway git repos under the caller `$TMPDIR` | mori |
```

For reaching `C2=met`, the remaining work is rows only: rows for the three r45
counters and the three orphan tools (`mori-disk-rate.py`,
`mori-wave-settlement.py`, `mori-round41-calibration.py`). Every path in the
39-member population now carries a real `--selftest` argv branch.

## Risks / limits

- A Python membership test counts only when its operand is an argv-shaped name
  (`raw`, `argv`, `args`, `sys.argv`, `arguments`, `options`, `opts`, `tokens`,
  `words`); a differently named argv variable would be a false negative (unmet,
  never a false met).
- A short string constant that literally reads `"--selftest" in raw` would count
  as a branch; no current tool has that shape. Comments and docstrings never
  count.
- The escape is strict by design: a self-test under a flag whose name lacks
  `test` is not admissible, and a mention is not a hook.
- A registry table is read only when its header is literally the eight standard
  cells; a header-less resumption of pipe rows is not a table (the seven current
  tables are contiguous).
- `wrong_row` is a finding counter, not a partition of the population.
- At `WORK` the population includes uncommitted r45 counters, so the worktree
  receipt moves while peers edit; the entering-tip receipt is the stable one.
- No tools were installed or upgraded; python3 and git were already present.
