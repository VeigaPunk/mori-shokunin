# Mo89M02Mut — mutation probe of the C1 binding repair and the twelve C2 arms (round 89 residual)

Seat: Mo89M02Mut (replaces Mo89M01Mut). Judged on: calibration.

## Revisions and inputs
- Subject A: `.ufo/waves/round-87/count-c2.py` at `9f4d20b9290faff54354d6ab6b08982d98d5e72c`, gate sha256 `74fac0a6ec25b994ff943e79feb9cf358063732593eecc6811d60fd2bb3c467d`.
- Subject B: `.ufo/waves/round-88/count-c1.py` (sha256 prefix `d5b83c775d199c66`) and `count-c2.py` (`6c2ac8fd17c907b4`) at `7ce712d4e0fd295d812fc3047ceeb114c3c2a58c`; byte-identical at 9f4d20b9 (`git diff --quiet 7ce712d4 HEAD` asserted in the driver).
- Detector: lane `.ufo/waves/round-89/noharm-c1.py`, sha256 `3b8c7b14fe0d8099de0865235b6ae0c5f981e8189050c41cc1bc2922426d7c7d`, 34 cases, entering rev 30a29797.
- Lane tip when I finished: `bb50c332` (c89e5b6e and bb50c332 landed after 9f4d20b9). `git diff --stat 9f4d20b9 bb50c332` over the gate, round-88 counters, noharm-c1.py and the Mo89R01C1 battery is empty, so the measurements still hold at the tip.
- Scratch: `/fast/scratch/hyaku/mori-r89/Mo89M02Mut/clone` (`git clone --shared`, detached at 9f4d20b9, `--show-toplevel` asserted), TMPDIR=`<scratch>/tmp`. Python 3.14.8. I installed no tools.

## Method
- **Subject A** (`drive_a.py`):
  1. Each mutant's anchor must occur exactly once. The driver writes the mutated gate and commits it in the scratch clone, which gives `mutrev`.
  2. It runs `python3 -I <clone>/.ufo/waves/round-87/count-c2.py --selftest --scratch <S>/tmp` (26 arms).
  3. It runs `python3 -I <lane>/.ufo/waves/round-89/noharm-c1.py <mutrev> --repo <clone>`.
  4. It calls `binding_problems(kill_cmd, [(0*64, tools/mori-record-sweep.py)], True, clone)` on the pristine and mutated modules. This tests the minimal kill case I propose for that mutant.
  5. It runs `git checkout --detach 9f4d20b9` and verifies the restored sha256 equals the pristine sha256.
- Classification:
  - killed-by-selftest: selftest rc≠0 or `FAIL` lines.
  - killed-by-battery-only: selftest green, noharm rc≠0.
  - survived: both green.
- **Subject B** (`drive_b.py`): I mutate one round-88 counter in the clone, run its own `--selftest --scratch`, collect the `FAIL <arm>` labels, evaluate a direct probe on the pristine and mutated modules, then restore with `git checkout -- <file>` and verify the sha256. For B4 I also ran the full counter.

## Baseline (pristine, 9f4d20b9)
selftest rc=0 `C2_COUNTER_SELFTEST pass=26 fail=0`; noharm rc=0 `NOHARM harm=0 open=0 gained=3 cases=34 rev=9f4d20b9290f`. Both are green, so the probe is conclusive.

## Subject A: 41 single-point mutants of the repaired binding

Result: 2 killed by the selftest, 10 killed by the battery only, **29 survived**. Every mutant was restored (`restored=True`, sha `74fac0a6…` on all 41 rows).

| id | function | mutant | selftest | noharm | verdict | minimal kill case (pristine → mutant) |
|---|---|---|---|---|---|---|
| A01 | strip_comment | quotes never open | 26/0 | 0/0 | **survived** | `echo ' #' ; python3 -I T` met: bound→refused |
| A02 | strip_comment | `#` comments anywhere (no word-start rule) | 26/0 | 0/0 | **survived** | `echo a#b; python3 -I T` met: bound→refused |
| A03 | strip_comment | backslash escape ignored | 26/0 | 0/0 | **survived** | `printf \' # ; python3 -I T` reject: refused→bound |
| A04 | strip_comment | any char closes a quote | 26/0 | 0/0 | **survived** | `echo "a b #" ; python3 -I T` met: bound→refused |
| A05 | strip_comment | comment never stripped (`return cmd`) | 26/0 | 0/0 | **survived** | `true # ; python3 -I T` reject: refused→bound |
| A06 | strip_comment | `;#` not a comment | 26/0 | 0/0 | **survived** | `true;# ; python3 -I T` reject: refused→bound |
| A07 | strip_comment | column-0 `#` not a comment | 26/0 | 0/0 | **survived** | `# ; python3 -I T` reject: refused→bound |
| A08 | command_invocations | no operator split | 26/0 | harm=4 | battery-only | E16/E15b/E21/E22 |
| A09 | command_invocations | redirect target not skipped | 26/0 | 0/0 | **survived** | `>/tmp/log python3 -I T` met: bound→refused |
| A10 | command_invocations | fd digit kept | 26/0 | 0/0 | **survived** | `2>err python3 -I T` met: bound→refused |
| A11 | command_invocations | unbalanced quotes → `[]` not None | 26/0 | 0/0 | **survived** | `binding_problems("python3 -I 'tools/x.py", [], True)` = `['cmd-binding']`→`[]` (with one binding both refuse) |
| A12 | unwrap | assignments not unwrapped | 26/0 | harm=1 | battery-only | E08 |
| A13 | unwrap | env -C/-S/--chdir refusal removed | 26/0 | 0/0 | **survived** | `env -C/tmp python3 -I T` reject: refused→bound |
| A14 | unwrap | env -u value not consumed | 26/0 | 0/0 | **survived** | `env -u FOO python3 -I T` met: bound→refused |
| A15 | unwrap | nice -n value not consumed | 26/0 | harm=1 | battery-only | E14 |
| A16 | unwrap | timeout duration not consumed | 26/0 | 0/0 | **survived** | `timeout 60 python3 -I T` met: bound→refused |
| A17 | unwrap | exec -a NAME not consumed | 26/0 | 0/0 | **survived** | `exec -a sweep python3 -I T` met: bound→refused |
| A18 | unwrap | command/exec `-p/-c/-l/--` skip removed | 26/0 | 0/0 | **survived** | `command -p python3 -I T` met: bound→refused |
| A19 | unwrap | env not unwrapped | 26/0 | harm=1 | battery-only | E09 |
| A20 | python_script | **-c/-m/unknown-flag refusal removed** | 26/0 | open=2 | battery-only | A05/A06 (`python3 -c T`, `-m T`) |
| A21 | python_script | **-W/-X value not consumed** | 26/0 | harm=1 open=4 | battery-only | E11, A03/A04/A11/A12 |
| A22 | python_script | glued `-Wvalue` also eats next token | 26/0 | 0/0 | **survived** | `python3 -Wignore T` met: bound→refused |
| A23 | python_script | no break after W/X | 26/0 | harm=1 | battery-only | E11 |
| A24 | python_script | stdin `-` not refused | 26/0 | 0/0 | **survived** | `python3 - T` reject: refused→bound |
| A25 | python_script | `--` returns None | 26/0 | harm=1 | battery-only | E10 |
| A26 | python_script | `--check-hash-based-pycs` value not consumed | 26/0 | 0/0 | **survived** | `python3 --check-hash-based-pycs never T` met: bound→refused |
| A27 | shell_scripts | sh -c string not recursed | 26/0 | harm=1 | battery-only | E19 |
| A28 | shell_scripts | -n/-s/unknown refusal removed | 26/0 | 0/0 | **survived** | `bash -n T` reject: refused→bound |
| A29 | shell_scripts | -o value not consumed | 26/0 | 0/0 | **survived** | `bash -o errexit T` met: bound→refused |
| A30 | shell_scripts | `-ec` not seen as -c | 26/0 | 0/0 | **survived** | `bash -ec 'python3 -I T'` met: bound→refused |
| A31 | invocation_scripts | sh/dash/zsh dropped | 26/0 | 0/0 | **survived** | `sh T` met: bound→refused |
| A32 | uv_run_scripts | any uv subcommand = run | 26/0 | 0/0 | **survived** | `uv venv ./T` reject: refused→bound |
| A33 | uv_run_scripts | uv option value not consumed | 26/0 | 0/0 | **survived** | `uv run --python 3.14 T` met: bound→refused |
| A34 | invocation_scripts | depth limit off | 26/0 | 0/0 | **survived** | 4-deep `bash -c` nest of `python3 -I T`: refused→bound. The pristine gate refuses this valid command; see note 3 |
| A35 | invocation_scripts | direct path exec off | 26/0 | harm=1 gained=2 | battery-only | E18 (E05 was already counted under gained) |
| A36 | executed_scripts | **cd stop removed** | 26/0 | 0/0 | **survived** | `cd /tmp && python3 -I T` reject: refused→bound |
| A37 | executed_scripts | pushd/popd not stops | 26/0 | 0/0 | **survived** | `pushd /tmp && python3 -I T` reject: refused→bound |
| A38 | binding_problems | untokenizable → no problem | 26/0 | 0/0 | **survived** | `python3 -I 'T` reject: refused→bound |
| A39 | binding_problems | any→all | 23/3 FAIL binding_not_in_cmd,binding_comment_dropped,binding_selfprint_refused | open=10 | killed-by-selftest | (`all([])` is True) |
| A40 | same_path | realpath branch off | 26/0 | 0/0 | **survived** | `python3 -I <repo>/T` (absolute) met: bound→refused |
| A41 | binding_problems | replayed short-circuit inverted | 22/4 FAIL binding_not_in_cmd,binding_skipped_for_legacy,binding_comment_dropped,binding_selfprint_refused | open=12 | killed-by-selftest | — |

In the table, `T` = `tools/mori-record-sweep.py`. A cell like "26/0" is the selftest tally pass/fail; "0/0" is noharm harm/open. Every proposed kill case distinguished the pristine gate from its mutant (`distinguishes=True`). A11 is the exception: it is killed only at `bindings=[]` or `executed_scripts` level (see `extra-probes.txt`).

Findings, subject A:
1. **The gate's own 26-arm selftest kills 2 of 41 binding mutants (both in `binding_problems`).** It contains no arm for any of the nine repaired functions' internal rules. The three round-89 arms (`binding_path_identity`, `binding_comment_dropped`, `binding_selfprint_refused`) survive every mutant of `strip_comment`, `command_invocations`, `unwrap`, `python_script`, `shell_scripts`, `uv_run_scripts`, `invocation_scripts` and `executed_scripts`. Selftest-killed = 2/41.
2. **The repair's armour is the 34-case noharm battery, a separate file outside the gate.** It kills 10 more, for 12/41 total. **29 survive both detectors.** That is the unarmed surface. It includes the rules the repair advertises:
   - the quote-aware comment rule: A01–A07, all seven survive;
   - the `cd` stop: A36/A37;
   - `env -C` refusal: A13;
   - `sh -n` refusal: A28;
   - stdin `-` refusal: A24;
   - the `uv run` subcommand guard: A32;
   - untokenizable → refuse: A38;
   - realpath identity: A40.

   Eleven survivors open counterfeits, each turning a correct refusal into a binding: A03, A05, A06, A07, A13, A24, A28, A32, A36, A37, A38 (by kill-case expectation `reject`). The other 18 refuse valid replays (A34 is the policy case in note 3). Every row above gives a one-line kill case.
3. Depth limit (A34): with `DEPTH=3` the pristine gate refuses a valid 4-deep `bash -c` nest, and the mutant binds it. This rule is a policy choice, not a guarded invariant. No detector pins its direction.
4. The -c/-m refusal (A20) and the -W/-X value consumption (A21) are killed only by noharm cases A03–A06/A11/A12/E11, not by any gate arm. If the battery file is dropped or edited, these regressions pass the frozen `--selftest` and the predicate `arms=26`.

## Subject B: 6 extra mutants on neighbouring helper lines (none in the frozen MUTANTS; `in_frozen=False` checked against `round-89/count-c2.py`)

| id | file:helper | mutant | own selftest | FAIL label | verdict | direct probe (pristine → mutant) |
|---|---|---|---|---|---|---|
| B1 | count-c1.py:own_ok_of | arm-count pin dropped (`pass=%d`→`pass=\d+`) | rc=0 28/0 | — | **survived** | `own_ok_of(0,"C1_COUNTER_SELFTEST pass=27 fail=0")` False→True |
| B2 | count-c1.py:own_ok_of | `rc == 0` conjunct dropped | rc=1 27/1 | own_ok_red | killed | — |
| B3 | count-c2.py:met_line | full rev instead of `rev[:12]` | rc=1 25/1 | met_line_derived | killed | — |
| B4 | count-c2.py:main→met_line | `print(met_line(rev[:7]))` | rc=0 26/0 | — | **survived** | full run: `C2=met … arms=26 rev=7ce712d` vs pristine `… rev=7ce712d4e0fd` (both rc=0) |
| B5 | count-c2.py:own_ok_of | `fail=0`→`fail=\d+` | rc=1 25/1 | own_ok_red | killed | — |
| B6 | count-c2.py:clone_root_ok | `==` → `realpath(d).startswith(top)` (enclosing repo / empty accepted) | rc=0 26/0 | — | **survived** | `clone_root_ok("/nonexistent\n","/nonexistent/fx")` and `clone_root_ok("","…")` False→True |

All six were restored with sha equal to pristine. Score: 3 killed / 3 survived.

Findings, subject B:
- The `own_ok_red` arms pin rc and fail, but not the arm count (B1).
- `met_line_derived` tests the helper, not the line `main` prints (B4).
- `clone_root_ok`'s only negative is an unrelated path, so it does not cover a parent prefix or empty output (B6).

Pristine weaknesses observed in passing; both are [INFERENCE] about severity:
- count-c2.py `own_ok_of` accepts any `pass=\d+`, so a run with any arm count reads as green.
- The c1 pin regex `pass=28 fail=0` has no trailing `\b`, so it also matches `fail=05`.

## Evidence (`.ufo/waves/round-89/r/Mo89M02Mut-evidence/`)
- `diffs/A01..A41.diff`, `diffs/B1..B6.diff`.
- `transcript-A.txt` (sha256 `7a775589…`), `transcript-B.txt` (`2b48b557…`).
- `results-A.json` (`cfb28ec4…`), `results-B.json` (`8242a59b…`).
- `drive_a.py`, `drive_b.py`, `extra-probes.txt`.
- Commands: `python3 -I drive_a.py` (rc 0, 11 s); `python3 -I drive_b.py` (rc 0, ~215 s including the B4 full run); the pristine full run of `round-88/count-c2.py 7ce712d4 --repo <clone>` gave rc 0, `C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=26 rev=7ce712d4e0fd`.

The scratch clone was removed after the evidence was saved.

VERDICT Mo89M02Mut C1 partial — the repair's battery claim (harm=0 open=0) reproduces, but the gate arms kill only 2/41 binding mutants and 29/41 survive both the 26 arms and the 34-case battery (11 of them reopen counterfeits)
VERDICT Mo89M02Mut C2 partial — 3/6 neighbouring mutants (B1 own_ok arm-count pin, B4 printed met line, B6 clone_root prefix) survive the twelve new arms
