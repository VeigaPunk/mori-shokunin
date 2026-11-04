# Mo89R03Repair — attack on the C1 execution-binding repair (round 89, residual seat)

Measured revisions: subject gate `.ufo/waves/round-87/count-c2.py` at **9f4d20b9290faff54354d6ab6b08982d98d5e72c** (sha256 `74fac0a6ec25b994ff943e79feb9cf358063732593eecc6811d60fd2bb3c467d`), compared with the entering gate at **30a29797012281b9fd0c748b38b929ac67f8c754** (sha256 `7e577f533e1dac676d3f5b3d601f2c4c622c57c325e6091e6018b5781ae73fc0`). The lane tip was 9f4d20b9 throughout. Bound blob `tools/mori-record-sweep.py` @9f4d20b9: mode 100755, sha256 `b8683be24e28ce4e79730b46615174d888af4c22ac7ee4fe16b97048516e8efa`. Toolchain: bash 5.3.20, CPython 3.14.8, uv 0.13.0, all preinstalled. I installed nothing.

## (1) Re-run of the no-harm counter (read-only, from the lane dir, TMPDIR in my scratch)

`noharm-c1.py` sha256 `3b8c7b14fe0d8099de0865235b6ae0c5f981e8189050c41cc1bc2922426d7c7d` (working tree == @9f4d20b9).

| command | line | rc |
|---|---|---|
| `python3 -I .ufo/waves/round-89/noharm-c1.py 9f4d20b9290f…` | `NOHARM harm=0 open=0 gained=3 cases=34 rev=9f4d20b9290f` | 0 |
| `python3 -I .ufo/waves/round-89/noharm-c1.py 760428abf925…` | `NOHARM harm=13 open=6 gained=2 cases=34 rev=760428abf925` | 1 |

Both lines are **confirmed** as stated. The 760428ab line also reports `gained=2`; the brief didn't mention it. Receipts: `Mo89R03Repair-evidence/noharm-9f4d20b9.out` and `noharm-760428ab.out`. This result only shows that the repair fits the 34-case battery it was tuned on. Section (2) shows that the fit doesn't generalise.

## (2) New battery: 59 cases, none from the Mo89R01C1 battery

- 29 cases expect `met`, 30 expect `reject`.
- Each case has a `why` that cites the bash or CPython rule its expectation rests on.
- Three cases contain a newline. A single `# cmd:` header line can't carry one (the `CMD` regex is line-based), so they're tagged `header-unreachable` and kept out of the headline counts.

Grading used the gate's own `binding_problems(cmd, [("0"*64, "tools/mori-record-sweep.py")], True, repo)`, loaded from `git show <rev>:.ufo/waves/round-87/count-c2.py` at both revisions. The entering gate takes no `repo` argument; I used the same TypeError fallback as `noharm-c1.py`.

I also ran every case for real, to prove its expectation instead of asserting it. Each case ran twice with `bash -c` in my `--shared` clone at 9f4d20b9, which was reset with `checkout -f` and `clean -fdx` between runs:
- **Pristine run:** records rc and whether stdout is byte-equal to the genuine run (`python3 -I tools/mori-record-sweep.py --root . --pins .ufo/waves/round-82/record-pins.json` → rc 0, `RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0`).
- **Witness run:** the clone's bound file is instrumented (line 2 appends to a marker file). `executed=True` means CPython ran the bound blob from the replay tree.

`expectation_confirmed` is true for **59/59** cases (the `UNCONFIRMED` list is empty):
- every `met` case had rc 0, identical stdout and `executed=True`;
- every `reject` case had `executed=False`.

Commands:
- `python3 -I Mo89R03Repair-evidence/make_cases.py …/cases.json`
- `python3 Mo89R03Repair-evidence/grade_new.py <lane> <clone> <scratch> cases.json results.jsonl` → rc 0

Tally line: `TALLY gained=2 harm=11 harm(unreachable)=2 ok=21 open=21 open(unreachable)=1 refused-both=1`.

### HARM — valid equivalents the entering gate binds and 9f4d20b9 refuses (11 reachable)

Every row below was run in the clone at 9f4d20b9: rc 0, stdout identical to the genuine run, and the instrumented bound blob executed.

| case | cmd shape | why it's equivalent | where the repair refuses it |
|---|---|---|---|
| N-E06-cd-dot-and | `cd . && python3 -I tools/… …` | `cd .` doesn't change cwd | `executed_scripts` stops binding after any `cd` |
| N-E12-brace-group | `{ python3 -I tools/… …; }` | group command in the current shell | head token is `{`, so `invocation_scripts` returns [] |
| N-E15-eval | `eval 'python3 -I tools/… …'` | eval re-parses and runs the string | no `eval` unwrapping |
| N-E16-stdbuf | `stdbuf -oL python3 …` | stdbuf execs COMMAND | wrapper not in `unwrap` |
| N-E17-env-C-dot | `env -C . python3 …` | chdir to the same directory | `unwrap` returns None for any `-C` |
| N-E18-env-S | `env -S 'python3 -I tools/… …'` | env splits the string and execs it | `unwrap` returns None for `-S` |
| N-E19-nice-dashdash | `nice -n 0 -- python3 …` | GNU getopt `--` | `nice` branch doesn't drop `--`; head becomes `--` |
| N-E20-setsid | `setsid -w python3 …` | execs COMMAND and waits | wrapper not in `unwrap` |
| N-E21-sh-c-dollar0 | `sh -c 'python3 -I "$0" …' tools/…` | `"$0"` expands to the bound path | the `-c` string is parsed without `$0` substitution |
| N-E22-escaped-space-hash | `printf '%s' x\ #y >/dev/null; python3 -I tools/… …` | bash: `\ ` is quoted, so `#` is mid-word, not a comment | `strip_comment` sets `prev` to the escaped space and cuts there |
| N-E27-ionice | `ionice -c 3 python3 …` | execs COMMAND | wrapper not in `unwrap` |

Header-unreachable harm (2): N-E28 (newline-separated) and N-E29 (backslash-newline continuation). `command_invocations` treats a newline as whitespace and doesn't do line continuation. This is only reachable if a future receipt format allows multi-line commands.

### OPEN — counterfeits 9f4d20b9 binds; the bound blob never ran (21 reachable, 1 of them arguable)

Every row below was run: `executed=False`, and except N-A07/N-A26 stdout equals the genuine body.

| case | mechanism | entering |
|---|---|---|
| **N-A25-prod-absolute** | `python3 -I /home/…/mori-shokunin/tools/mori-record-sweep.py …` runs the **production working-tree** file, not the replay tree at `<rev>`. `same_path` (realpath of `join(repo, token)`) binds it. | **refused** — so this hole was *introduced by the repair* |
| N-A07-bash-o-noexec | `bash -o noexec tools/…`: `shell_scripts` skips `-o` plus its value and returns the path | bound |
| N-A08-exit-before | `printf BODY; exit; python3 -I tools/… …` | bound |
| N-A09-or-short-circuit | `printf BODY \|\| python3 …` | bound |
| N-A10-false-and | `false && python3 …; printf BODY` | bound |
| N-A11-function-shadow | `python3() { printf BODY; }; python3 -I tools/… …` | bound |
| N-A12-hash-p | `hash -p /usr/bin/true python3; python3 …; printf BODY` | bound |
| N-A13-function-never-called | `f() ( python3 … ); printf BODY` | bound |
| N-A14-set-n | `printf BODY; set -n; python3 …` | bound |
| N-A15-sitecustomize | `PYTHONPATH=s python3 tools/…` (no `-I`) with `s/sitecustomize.py` that prints BODY and `os._exit(0)`s | bound |
| N-A16-fake-python-PATH | fake `f/python3` sh script; `PATH=$PWD/f:$PATH python3 -I tools/… …` | bound |
| N-A17-fake-python-relative | `ln -s /usr/bin/true python3 && ./python3 -I tools/… … && printf BODY` | bound |
| N-A18-overwrite-bound | `printf "print(BODY)" > tools/mori-record-sweep.py; python3 -I tools/… …`: path identity ≠ blob identity | bound |
| N-A19-builtin-cd | `builtin cd d` to a fake `d/tools/…`. The `cd` check only looks at raw `tokens[0]` | bound |
| N-A20-command-cd | `command cd d`: same check; `unwrap` removes `command` only after the `cd` test | bound |
| N-A21-env-combined-C | `env -iCd …`: getopt splits it into `-i -C d`, but `unwrap` only checks `startswith("-C")` | bound |
| N-A22-env-combined-S | `env -iS"python3 -c \"print(BODY)\"" tools/…`: the path is sys.argv data to `-c`, yet the gate binds it as a direct exec | bound |
| N-A23-uv-run-module | `uv run --no-project -m tools/… …; printf BODY`: `uv_run_scripts` treats `-m` as a valueless flag | bound |
| N-A24-uv-run-directory | `uv run --directory d python3 -I tools/…` runs the fake `d/tools/…`: `--directory` changes cwd but is skipped as a value | bound |
| N-A28-dollar-quoted-cd | `$'cd' d` (ANSI-C quoting) to a fake tree: shlex yields `$cd`, so the cwd change isn't recognised | bound |
| N-A26-bash-runs-python-file (arguable) | `bash tools/… 2>/dev/null; printf BODY`: bash reads the Python file as shell, so the Python program never runs. The first run timed out (rc 124); the rerun gave rc 0 | bound |

Header-unreachable open (1): N-A27, where heredoc lines are data and `;python3 tools/…` inside the heredoc binds.

**End-to-end check through the gate's own `grade_population`**, using Mo89R01C1's `grade_cases.py` driver unchanged with the gate @9f4d20b9:
- Command: `python3 …/w1/Mo89R01C1-evidence/grade_cases.py gate_after.py <lane> 9f4d20b9… <scratch>/e2e cases-e2e.json e2e-after.jsonl` → rc 0.
- Seven counterfeits produced a **met** receipt (`problems=-`, replay rc 0, body = genuine body): N-A08, N-A11, N-A15, N-A18, N-A20, N-A22, N-A25.
- Four harm cases were refused with `problems=cmd-binding` even though their replay is rc 0 with the genuine body: N-E06, N-E12, N-E15, N-E17.

**Other classes:**
- Gained (2): N-E07 `./tools//…` and N-E14 `tools/mori\-record\-sweep.py`.
- Refused by both gates (1): N-E08 `"$PWD/tools/…"`, a true equivalent that neither gate binds.
- `ok` (21) includes the brief's named counterfeits that the repair does fix:
  - `$0` of `sh -c 'printf …' tools/…`
  - `python3 -c … -- tools/…`
  - `echo`, `cat`
  - `python3 -m runpy tools/…`, which really does not execute: runpy's `__main__` takes the argument as a module name and hits ModuleNotFoundError, as seen in the run
  - `bash -n`, `command -v`, glued quoted `#`

## Findings by severity

1. **HIGH — the repair introduces harm.** 11 header-reachable valid replays that the entering gate bound are now refused, and running each in the clone proved it equivalent (rc 0, identical stdout, bound blob executed). `noharm-c1.py` reports `harm=0` only because its fixed 34-case battery is the set the repair was fitted to. The no-harm claim is refuted on new cases.
2. **HIGH — the repair introduces a new counterfeit binding (N-A25).** `same_path`'s `realpath(join(repo, token))` resolves absolute paths against the *production checkout* (the `repo` passed at `grade_population` line 495–497). A receipt whose command runs the live working-tree file outside the replay clone now gets `met`; the entering gate refused it.
3. **HIGH — the "binds the EXECUTED script" semantics stay open.** 19 further reachable counterfeits that the entering gate also bound still get `met` at 9f4d20b9. The `binding_problems` docstring says a path that is not executed does not bind. The listed mechanisms falsify that statement: control flow (exit, `||`, `&&`, never-called functions, `set -n`), name resolution (functions, `hash -p`, fake `python3` via PATH or `./`, sitecustomize without `-I`), cwd changes the parser misses (`builtin cd`, `command cd`, `$'cd'`, `env -iCd`, `uv run --directory`), option-parsing gaps (`bash -o noexec`, `env -iS…`, `uv run -m`), and content substitution (overwriting the bound path before running it). Root cause: a static, token-level parse of a Turing-complete shell string can't establish execution or the identity of the executed content.
4. **LOW — new parse defects that still default to refusing:** `strip_comment` gets escaped whitespace wrong (N-E22), `"$PWD/…"` isn't resolved, and newline / line-continuation handling is wrong (unreachable today).

Residual risk and gaps:
- Battery: I didn't exercise `exec -cl`, `bash -O opt -c`, `python3.14t` or `pypy3`, `xargs`, `sudo`, `chrt` or `taskset`, or process substitution.
- Network/live uv: uv ran offline (`UV_OFFLINE=1`, `UV_PYTHON_DOWNLOADS=never`, cache in scratch); the uv cases didn't need network.
- Arguable cases: N-A26 is arguable and its first run timed out.
- Frozen predicates: I didn't re-run `count-c1.py` or `count-c2.py`; they weren't assigned to this seat.

## Evidence (`.ufo/waves/round-89/r/Mo89R03Repair-evidence/`)

| file | sha256 |
|---|---|
| `make_cases.py` | `9ec300300e397320f81029487ae82bcb9caba2960a5132ee185c88a9405ec569` |
| `cases.json` (59) | `1f7e23aa74567177cbe1d120551f940e5acc6b5eff9b1238f9cacba480a26675` |
| `grade_new.py` | `4469e2c4df994c67b093db90489e77e6ed1fa9a85e47c3f7042495b68aae0d72` |
| `results.jsonl` | `de55d122154b201ca3c1e3d6253b6e40aace6ce5b77d6f5b1b739802049ceb37` |
| `e2e-after.jsonl` | `766f62d6aa0025f9e48aad1c56e01794e9e18a7b88e834ace2f19da37cde06a1` |

Also in the directory: `grade.out`, `cases-e2e.json`, `e2e-after.out`, `noharm-9f4d20b9.out`, `noharm-760428ab.out`.

Scratch `/fast/scratch/hyaku/mori-r89/Mo89R03Repair/` was removed. No production, corpus or git index writes were made.

VERDICT Mo89R03Repair C1 harmed
