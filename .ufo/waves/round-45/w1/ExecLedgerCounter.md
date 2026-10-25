# ExecLedgerCounter — hardened C1 ledger counter (P-C1 + Correction 1)

Seat: executor, second pass. Scope: `count-c1.py`, its single-check mutant, this report.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only git; nothing committed).

## Landed

| file | bytes | lines | sha256 |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/count-c1.py` | 49989 | 1172 | `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/fixtures/mutants/count-c1.py` | 50023 | 1172 | `50900a3fce687430721e6ab36f4d293c928ddef33a3249477c51667881d2ed07` |

Both untracked (`??`), L1 commits. Pass 1 (`f80e75ac…`) was falsified by
`w1/RevC1Grammar.md`: the `CONST=` escape voided revision sensitivity, filter options were
unchecked (a row executed `sort --compress-program` and wrote with `sort -o`), the tip litmus
matched 40-hex only, `ls-tree` scored an absent path as `0`, and one junk file satisfied the
witness arm. Every one of those is closed below, each with its own `--selftest` arm.

## Ledger contract

`id<TAB>value<TAB>class<TAB>command[<TAB>CONST=<reason>]`, `id` `^F\d{2,3}$`, `value` digits,
`class` ∈ registry|evidence|wave|corpus|checks, `CONST` reason non-empty.

`command` is one pipeline, first stage `git <read-verb> …` naming `@REV@`, later stages only
`grep head tail wc sort uniq cut tr cat nl`. No shell exists: `subprocess.run` is called three
times (lines 185, 413, 713) and `shell=True` occurs 0 times.

**Options are allow-listed per verb** (`GIT_OPTIONS`, `FILTER_OPTIONS`): `ls-tree`
`-r --name-only -l -z --full-tree`; `show` none; `cat-file` `-e -s -t -p`; `rev-list --count`;
`ls-files -z`; `grep` `-l -n -v -c -e -E -F -i -w`; `log --format=%s|%H|%h --oneline`;
`diff --name-only` (required). Filters: `grep -c -o -l -E -F -e -i -v -w -x`, `head/tail -n`,
`wc -l -w`, `sort -r -n -u`, `uniq -d -u`, `cut -f -d`, `tr -d -s`, `cat`, `nl`. Attached
values are legal (`-f2`, `-d:`, `-ePAT`), `--` ends option parsing, and only `grep` (one
pattern) and `tr` (two SETs) take positionals. `sort -o`, `sort -S`,
`sort --compress-program=`, `uniq IN OUT`, `tee`, `awk`/`sed` (their `system()` reaches a
shell), `git -c`, `--git-dir`, `--work-tree`, absolute paths and `=`-bearing arguments are
all rejected.

## Second-pass requirements → code

1. **`moved>=1`, `const` cap, non-empty reasons** — `check_text` records `revision_moves`
   (`moved>=1`) and `const_cap`; both are verdict conditions in `main`'s `fails`. The cap is
   `rows-2`, not the correction's literal `rows-1`: 15 rows with 10 `CONST` passes
   (`const=10 cap=13`), while the falsifier's `S2′` (11 `CONST` + 1 mover) is `C1=unmet` —
   the literal `rows-1` would have admitted it, and the L1 named it as unmet.
   `CONST_RE = ^CONST=(\S.*)$` already rejects an empty reason.
2. **Witnesses must be full-size and vacuous for a declared class** — `_ledger_shape` counts
   raw rows/classes; `_declared_vacuity` accepts only `revision_sensitivity`, `const_cap`, or
   a declared parse class (`duplicate id`, `duplicate command`, `resolves the tip`). Checks
   `witnesses_rejected` (rejected at all) and `witnesses_vacuous` (rejected *and* ≥12 rows/≥4
   classes *and* a declared class). A three-line junk file therefore prints
   `witnesses=1/1 witnesses_vacuous=0/1 failed=witnesses_vacuous`, not a pass.
3. **Stage-option hardening** — `_option_problems`/`_token_problems`/`_git_stage_problems`/
   `_stage_problems` implement the allow-lists above; `BANNED_TOKENS` covers
   `-o -S -c -T --compress-program --output --exec --git-dir --work-tree --no-index
   --path-format`. Two scoped allowances are deliberate and named: `grep -o` (read-only
   only-matching, and grep cannot receive a path) and `=` inside a filter *positional* (a
   pattern is data — the round's own ledger has `grep -oE '^rows=[0-9]+'`). Everywhere else
   `=` and the banned spellings still reject.
4. **Short-SHA pin** — `HEX7_40 = ^[0-9a-fA-F]{7,40}$` on any non-option token, in addition to
   `HEAD`, `@{…}` and 40-hex. `git log --format=%s 3ad8faa @REV@ | wc -l` is now
   `rows_parse FAIL (token '3ad8faa' is a revision-like hex pin, not @REV@)`.
5. **Listing verb scoring absence as 0** — `parse_ledger` rejects an asserted `0` whose
   pipeline contains `ls-tree`/`ls-files`, with `CONST` or without; `rev-list --count`
   (exits 0) and `show`/`cat-file -e` (fail on absence) remain the sanctioned zeros.

## Evidence

Selftest (16 arms; `TMPDIR=…/round-45/tmp/ExecLedgerCounter`):

```
selftest PASS honest_ledger_met
selftest PASS offbyone_row_mismatch
selftest PASS junk_producer_rejected
selftest PASS below_floor_rejected
selftest PASS absent_ledger_unmet
selftest PASS duplicate_id_rejected
selftest PASS duplicate_command_rejected
selftest PASS head_reading_row_rejected
selftest PASS revision_constant_row_rejected
selftest PASS witness_dir_one_passing_witness
selftest PASS all_const_ledger_unmet
selftest PASS const_heavy_ledger_unmet
selftest PASS witness_without_floor_unmet
selftest PASS stage_option_injection_rejected
selftest PASS short_sha_tip_rejected
selftest PASS absent_path_zero_rejected
C1_SELFTEST pass=16 fail=0
rc=0
```

Mutant — the counter with **the duplicate-id check disabled** (one line, `parse_ledger`):

```
@@ -475,7 +475,7 @@
                             "zero count; take a zero from show, cat-file -e or "
                             "rev-list --count" % n)
-        if fid in ids:
+        if False:  # MUTANT: duplicate-id check disabled
             problems.append("row %d: duplicate id %s (first at row %d)" % (n, fid, ids[fid]))
         else:
             ids[fid] = n
```

`diff -u` exit 1, exactly that hunk; `--selftest`:

```
selftest FAIL duplicate_id_rejected: []
C1_SELFTEST pass=15 fail=1
rc=1
```

One disabled check, one arm caught, nothing else moves.

### Falsifier's seven shapes, re-run as negative controls

Their attack repo is intact (`.ufo/waves/round-45/tmp/RevC1Grammar/attack-repo`, shared clone,
real commits), the witness dir is the lane's three fixtures, `--other-rev 554ff416`:

| shape | receipt (`failed=`) | rc |
|---|---|---|
| S1a `sort -S 1K --compress-program=<script>` | `C1=unmet … failed=revision_moves,revision_sensitivity,rows_parse` (`sort option '-S' is forbidden`) | 1 |
| S1b `sort -o <abs path>` | `C1=unmet … failed=revision_moves,revision_sensitivity,rows_parse` (`'-o' is forbidden`, `absolute path`) | 1 |
| S2 all-12-`CONST` | `C1=unmet … failed=const_cap,revision_moves` (`revision_moves FAIL (moved=0 floor=1)`, `const_cap FAIL (const=12 cap=10)`) | 1 |
| S2′ 11-`CONST` + 1 mover | `C1=unmet … failed=const_cap` (`moved=1` PASS, `const=11 cap=10` FAIL) | 1 |
| S3 junk-only witness dir | `C1=unmet … witnesses=1/1 witnesses_vacuous=0/1 failed=witnesses_vacuous` (`junk.tsv NOT-PROVING (rows=0 …)`) | 1 |
| S4 short-SHA tip pin | `C1=unmet … failed=revision_moves,revision_sensitivity,rows_parse` | 1 |
| S5 absent path via `ls-tree`, 0 | `C1=unmet … failed=revision_moves,revision_sensitivity,rows_parse` (`asserted 0 from a listing verb`) | 1 |

Positive control, same harness (`atk/honest.tsv` at `4e505037`, lane witnesses):

```
C1=met mismatches=0 rows=12 classes=checks,corpus,evidence,registry,wave floor_rows=12
floor_classes=4 rev=4e505037… other_rev=554ff416… witnesses=3/3 witnesses_vacuous=3/3
rc=0
```

**No canary moved.** `CANARY_COMPRESS` mtime `07:51:03`, 0 bytes; `CANARY_SORT` mtime
`07:51:01`, 863491 bytes — both unchanged across every run above (`stat` before and after),
i.e. neither the program nor the writer ran.

### The round's real ledger

`.ufo/waves/round-45/figures.tsv` exists (2184 bytes, 15 rows) but is **untracked**, so the
CLI at the tip cannot read it:

```
check ledger_present         FAIL (absent at 3ad8faaa637a)
check witnesses_rejected     PASS (witnesses=3/3)
check witnesses_vacuous      PASS (witnesses_vacuous=3/3 (floor 12 rows/4 classes, declared vacuity class))
C1=unmet mismatches=? rows=0 … rev=3ad8faaa637ae466c61f9427fea1c208bf49ea82 … witnesses=3/3 witnesses_vacuous=3/3 failed=ledger_present
rc=1
```

Scoring its **bytes** at the tip (direct `check_text`, not a CLI verdict):

```
rows_parse PASS (15 rows)   row_floor PASS (15)   class_floor PASS (5)
const_cap  PASS (const=10 cap=13 rows=15)   revision_moves PASS (moved=1 floor=1)
commands_reconcile FAIL   mismatches=5
  F01 asserted=246 observed=245
  F02 asserted=75  observed=74
  F03 asserted=55  observed=54
  F05 asserted=53  observed=43
  F08 asserted=33  observed=28
```

Those are **worktree** measurements, not committed ones: `corpus/SOURCES.md` is modified
(worktree 246 vs tip 245), `corpus/lessons` has 75 tracked-plus-new files vs 74 at the tip,
`corpus/knowledge` 55 vs 54, and `SKILL.md` (modified) has 53 gate/probe rows vs 43 at the
tip. The ledger's grammar is clean under the new counter; its values must be re-measured **at
the commit that carries the wave-2 edits** — a counter that read the worktree would be exactly
the vacuity C1 removes, so this is the counter reporting the truth, not a counter defect.

The lane's three witnesses are untouched and still score `witnesses=3/3
witnesses_vacuous=3/3` (each 12 rows / 5 classes; `w-dup`/`w-head` fail `rows_parse` on a
declared class — duplicate id/command, tip-resolving token — and `w-revconst` fails
`revision_sensitivity`).

## Verdict line (self-describing)

```
C1=<met|unmet> mismatches=<n|?> rows=<n> classes=<csv|-> floor_rows=12 floor_classes=4
rev=<40-hex> repo=<abs> other_rev=<40-hex|-> witnesses=<rejected>/<total>
witnesses_vacuous=<proving>/<total> [failed=<check,…>]
```

Per-witness lines print `rejected` / `NOT-PROVING` / `ACCEPTED` with `rows= classes= fails=`
and the reason for the state.

## Risks and residuals

- **`const_cap` is one row tighter than Correction 1's text** (`rows-2`, not `rows-1`), because
  the literal cap admits S2′ (11 `CONST` + 1 mover) which the L1 explicitly required to be
  unmet. The check prints both numbers (`cap=10 … Correction 1 literal cap rows-1=14`).
- **Two scoped allowances** are needed for real rows to parse: `grep -o` and `=` inside a
  filter positional. Both are read-only; the writer spellings (`sort -o`, `-S`,
  `--compress-program`, `--output`, `--exec`, `uniq IN OUT`) stay dead, and no filter may take
  a file operand. If the L1 wants a literal global `-o`/`=` ban, the round's ledger row F14
  (`grep -oE`) and F15 (`'^rows=[0-9]+'`) cannot parse — named here rather than silently
  relaxed.
- **`awk`/`sed` remain excluded** (`system()` reaches a shell); r44's `figures-r43.tsv` rows
  14–15 therefore still fail `rows_parse`. Loud, not silent.
- **A genuine zero needs a zero-exiting producer**: zero-match `grep` is rc 1 (gate failure),
  and `ls-tree`+0 is a parse error; use `rev-list --count`.
- **Witnesses are read from the worktree** and scored at `--rev`; a witness built on
  uncommitted bytes is rejected as `unreadable`/`revision_sensitivity`, which the per-witness
  line exposes.
- No live `C1=met` is possible until the ledger is committed (and re-measured); the met path is
  proven by the honest control above and by `honest_ledger_met`.

## Disclosure

- No tool installs or upgrades; no pacman, no network. VCS: read-only (`log`, `status`,
  `ls-files`, `check-ignore`); nothing staged or committed.
- Scratch `.ufo/waves/round-45/tmp/ExecLedgerCounter/` is empty; every selftest repo was
  removed in a `finally`. The falsifier's `tmp/RevC1Grammar/` tree was read only.
- Earlier in this seat I removed two wave-local `__pycache__` dirs while cleaning my own
  compile artifacts and re-compiled the sibling sources (`count-c2`, `count-c3`,
  `mori-gate-registry` mutant) to restore their caches; they are gitignored, no tracked byte
  changed. Recorded again for the record.

## Handoff

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/count-c1.py --selftest
#   → C1_SELFTEST pass=16 fail=0, rc=0
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/fixtures/mutants/count-c1.py --selftest
#   → C1_SELFTEST pass=15 fail=1, rc=1   (duplicate-id check caught)
```

Registry row prose for `SKILL.md` (ScribeRegistryRows owns the edit):
entry `python3 .ufo/waves/round-45/count-c1.py <rev> --repo . --other-rev <rev> --witness-dir .ufo/waves/round-45/fixtures/witnesses`;
verdict map `0 C1=met · 1 C1=unmet · 2 C1_SETUP`; self-test
`python3 .ufo/waves/round-45/count-c1.py --selftest` → `C1_SELFTEST pass=16 fail=0` (rc 0) and
mutant `…/fixtures/mutants/count-c1.py --selftest` → `pass=15 fail=1` (rc 1); write scope:
nothing outside `$TMPDIR` (selftest repos only); the ledger and witness dir are read-only
inputs.
