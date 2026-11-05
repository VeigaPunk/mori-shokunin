# Mo90Sc01Scope — the 22 provenance counterfeits the r87 receipt gate still binds

Seat: scout (leaf, no dispatch). Scope: **read-only classification only** — no lane edit, no
candidate, no rule proposal. L1: MoriR90.

## 0. Method and provenance of every number below

Entering revision for every read (verified, not cited from memory):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
d1c8488986512a6a0475af88cc52779ce4703e00
$ git -C …/mori-shokunin show d1c8488986512a6a0475af88cc52779ce4703e00:.ufo/waves/round-87/count-c2.py | sha256sum
10c126f8f684fbc0f6aa787e2e01ca1cf8d991a55d0f03082613a66bf7be6bbc  -
$ git -C …/mori-shokunin show 037c02ca43a5ff36e23e449d0d6bcf50a1f2cbec:.ufo/waves/round-87/count-c2.py | sha256sum
10c126f8f684fbc0f6aa787e2e01ca1cf8d991a55d0f03082613a66bf7be6bbc  -      # identical blob
$ git -C …/mori-shokunin show 30a29797012281b9fd0c748b38b929ac67f8c754:.ufo/waves/round-87/count-c2.py | sha256sum
7e577f533e1dac676d3f5b3d601f2c4c622c57c325e6091e6018b5781ae73fc0  -      # the *entering* gate (older)
```

The gate I graded with is the **committed r87 gate blob at the tip** (`10c126f8…`), loaded exactly
as the frozen counter loads it (`git show <rev>:<gate>` → temp file → `importlib`), and I called
its exported `binding_problems(cmd, [("0"*64, "tools/mori-record-sweep.py")], True, repo)`.

The population is the frozen one: `count-c1.py`'s own `load_cases()` (R03 `cases.json` +
C02 `heldout-all.txt` `class=claim` lines), class frozen by the `BRANCH` id set
(`.ufo/waves/round-90/count-c1.py:55`).

Frozen counter run at the tip (the receipt for every count):

```
$ cd …/mori-shokunin && HYAKU_SCRATCH=$S python3 -I .ufo/waves/round-90/count-c1.py \
      d1c8488986512a6a0475af88cc52779ce4703e00 --scratch $S
POPULATION cases=78 branch_cases=8 branch_open=8 harm=0 newopen=0 open=30 gained=2
C1=unmet branch_open=8 harm=0 newopen=0 open=30 cases=78 rev=d1c848898651
BATTERY cases=0 branch_cases=0 branch_open=0 harm=0 newopen=0 paths=0
```

`BATTERY cases=0` — no `battery/*.json` is committed at the tip yet (the battery branch of C1 is
still open; it does not touch this seat's question).

I re-derived the split independently of the counter (own loader, own gate calls) and got the same
partition: **30 counted bound rejects = 8 branch + 22 provenance**; the counter's `open=30` and
`branch_open=8` agree.

Population accounting (independent loader, 81 loaded cases, 78 counted):

* R03 `cases.json` → 59 cases (30 `N-A*` rejects, 29 `N-E*` mets).
* C02 `heldout-all.txt` → the counter's loader regex `^HCASE (\S+) expect=(met|reject) class=claim …`
  (`count-c1.py:51`) admits **22 of the 23 HCASE lines**: the single `class=prov` line
  `HCASE H10-dev-null-then-printf` is **not loaded** and is therefore outside the frozen population.
* Uncounted (`reach` set): `N-E28`, `N-E29`, `N-A27` → 81 − 3 = **78 counted**.

## 1. The count check

Requirement: *bound reject cases − 8 branch cases* must equal *population `open` − `branch_open`*.

| quantity | value | source |
|---|---|---|
| counted bound rejects (after-gate) | 30 | `POPULATION … open=30` |
| counted bound rejects, branch class | 8 | `POPULATION … branch_open=8` |
| **30 − 8** | **22** | provenance class, counted |
| population `open` field | 30 | `POPULATION … open=30` |
| population `branch_open` field | 8 | `POPULATION … branch_open=8` |
| **30 − 8** | **22** | ✔ equal |

**The check closes: 22 = 22.** The 22 are exactly the residual `open` the frozen target pins
(`TARGET = "C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78"`, `count-c1.py:66`): once the
8 branch-class counterfeits are closed, `open` must read exactly 22 — these 22 — or C1 misses.

One further bound-reject case exists but is **outside the counted population**:
`R03:N-A27-heredoc-data` (`reach: header-unreachable`, `cases.json`). It is bound by the gate and
is in the provenance class, but the counter does not count it, so it does not appear in `open`.
It is listed in §2 for completeness and flagged **uncounted**.

Reject-side census of the 78 counted (all measured, not inferred):

| bucket | n |
|---|---|
| rejects, bound after-gate, branch class | 8 |
| rejects, bound after-gate, provenance class | 22 |
| rejects, refused after-gate (already closed by the r87 rule) | 11 |
| rejects, **total counted** | 41 |
| mets, counted | 37 |
| counted total | 78 ✔ |

## 2. The grouped table — 22 counted provenance counterfeits (+1 uncounted)

Mechanism vocabulary is the contract's provenance list (`contract.md` P-C1): *functions,
PATH/interpreter substitution, sitecustomize, blob overwrite, heredoc data, `uv run -m`, `bash -n`,
cat/`$0`*; "other" collects the two shapes the contract does not name (cwd re-resolution, wrong
interpreter, name-description builtin).

**Decidable-by-syntax column** — "can a rule over the *recorded command text alone* (no
execution, no filesystem, no environment) decide that the bound blob is not the thing executed?"

| # | case | mechanism (one line) | family | syntax-decidable? | deciding fact / what is missing |
|---|---|---|---|---|---|
| 1 | `R03:N-A01-path-as-dollar0` | the path is a positional-parameter operand of `sh -c` (the `-c` string is `printf %sn` and expands no `$0`/`$1`) | `cat`/`$0` | **YES** | `sh -c STRING operands…` ⇒ operands are `$0,$1…`, never script operands; the string is in the text and references none. Sibling `N-E21` (`sh -c 'python3 -I "$0" …'`) shows the rule must *also* look for `$0` inside the string — still text-only |
| 2 | `R03:N-A04-cat-path` | `cat tools/mori-record-sweep.py` — cat *reads* the file, never executes it | `cat`/`$0` | **YES** | `cat` is a data-reading command; the gate's `DATA_HEADS` set (`count-c2.py:154`) simply omits `cat` |
| 3 | `R03:N-A06-bash-n` | `bash -n <file>` — bash parses the file and never executes it | `bash -n` | **YES** | the `-n` flag is in the recorded text; `bash -n` is read-only by definition |
| 4 | `R03:N-A07-bash-o-noexec` | `bash -o noexec <file>` — same no-exec semantics via `-o noexec` | `bash -n` | **YES** | the flag pair is in the text |
| 5 | `R03:N-A11-function-shadow` | `python3() { printf …; }` defines a shell function named `python3`; the later `python3 -I tools/…` calls the function, whose body never runs the file | functions / interpreter substitution | **YES** | function-definition text + the shadowed command word + the body: all textual |
| 6 | `R03:N-A12-hash-p` | `hash -p /usr/bin/true python3` rebinds the *name* `python3` in the shell's hash table, so the later `python3 -I tools/…` is not CPython | PATH/interpreter substitution | **YES** (bash-specific) | the hashed target path is literally in the text; needs `hash -p` semantics + "same command list ⇒ same shell". If `/usr/bin/true` were absent the run still would not execute the blob |
| 7 | `R03:N-A13-function-never-called` | `f() ( python3 -I tools/… );` defines `f` and never invokes it; the path is inside the never-run body | function defined and never called | **YES** | the definition and the absence of any call to `f` are both in the text |
| 8 | `R03:N-A14-set-n` | `set -n;` before the invocation ⇒ the shell *reads* the `python3` line but does not execute it (POSIX noexec) | `bash -n` family (`set -n` analogue) | **YES** | `set -n` appears earlier in the same command list |
| 9 | `R03:N-A15-sitecustomize` | `PYTHONPATH=s python3 tools/…` (no `-I`): `site` imports `s/sitecustomize.py`, which `os._exit(0)`s before the script runs | sitecustomize | **NO** | needs CPython's site-import order *and* the shim's content/behavior — interpreter semantics, not text syntax |
| 10 | `R03:N-A16-fake-python-PATH` | `PATH=$PWD/f:$PATH python3 …` makes the interpreter a fake `f/python3` sh script; the blob is never the program that runs | PATH/interpreter substitution | **NO** | which executable PATH resolution picks is a run-time fact, not text: the deciding inputs are the shell's `PATH`, the created `f/python3`, and bash's command hash table — none of them in the recorded text. (The recorded text *is* deterministic in a pristine shell; see §4) |
| 11 | `R03:N-A17-fake-python-relative` | `ln -s /usr/bin/true python3 && ./python3 -I tools/…` — the interpreter is a symlink to `true` | PATH/interpreter substitution | **NO** | the symlink target is a filesystem fact; the gate's `PYTHON` regex matches `basename("./python3")` so it treats it as CPython |
| 12 | `R03:N-A18-overwrite-bound` | `printf … > tools/mori-record-sweep.py;` rewrites the bound path *before* `python3 -I tools/mori-record-sweep.py` runs it, so the executed file is not the bound blob | blob overwrite | **YES** | a redirection whose target equals the bound path occurs earlier in the same command list — purely positional |
| 13 | `R03:N-A19-builtin-cd` | `builtin cd d` changes cwd, so the relative `tools/mori-record-sweep.py` denotes `d/tools/…`, a different file | other (cwd re-resolution) | **YES** (with cwd tracking) | `cd` + a relative operand ⇒ the repo-relative bound path is not what is named; the fake file's existence is irrelevant (either it is a different file or the run fails) |
| 14 | `R03:N-A20-command-cd` | same via `command cd d` | other (cwd re-resolution) | **YES** (with cwd tracking) | as above |
| 15 | `R03:N-A21-env-combined-C` | `env -iCd PATH=$PATH python3 …` — GNU getopt folds `-iCd` into `-i -C d`, so env chdirs to `d` before exec'ing | other (cwd re-resolution) | **YES** (with cwd tracking + getopt cluster folding) | the cluster is in the text; the same reasoning as #13 |
| 16 | `R03:N-A22-env-combined-S` | `env -iS"python3 -c \"print(…)\"" tools/mori-record-sweep.py` — `-S` re-splits the string into argv, so the path becomes `sys.argv` **data** of a `python3 -c` program | PATH/interpreter substitution (argv rewrite) | **YES** (env `-S` semantics) | `-iS<string>` semantics are deterministic from the text: the path lands in argv, never as a script operand. Note the r87 gate deliberately bails here: `head_index` returns `None` for `env -C/-S` (`count-c2.py:243`) |
| 17 | `R03:N-A23-uv-run-module` | `uv run --no-project -q -m tools/mori-record-sweep.py` — `-m` takes a *module name*; `tools/mori-record-sweep.py` is not an importable module, so the file never runs | `uv run -m` | **YES** | `-m` means module-name semantics (the same shape the gate already applies to `python -m` in `python_excluded`, `count-c2.py:254`), and the operand is visibly not a module name. True with or without `uv` installed |
| 18 | `R03:N-A24-uv-run-directory` | `uv run --no-project -q --directory d python3 -I tools/…` — uv chdirs to `d` first, so the relative path names `d/tools/…` | other (cwd re-resolution) | **YES** (with cwd tracking) | the `--directory d` is in the text |
| 19 | `R03:N-A26-bash-runs-python-file` | `bash tools/mori-record-sweep.py` — bash *interprets the Python file as shell*; the file is opened and parsed, but not run as the recorded program | other (wrong interpreter) | **NO** | deciding that the program did not run needs the file's *content* (is it valid shell?) — filesystem, not syntax. The r89 battery itself calls this "arguable: not the bound program's semantics" |
| 20 | `R03:N-A28-dollar-quoted-cd` | `$'cd' d` — ANSI-C quoting yields the word `cd`, so cwd changes to `d` and the relative path re-resolves | other (cwd re-resolution) | **YES** (with cwd tracking + `$'…'` unquoting) | the quoting form is in the text |
| 21 | `R03:N-A29-command-v` | `command -v python3 tools/mori-record-sweep.py` — `command -v` only *describes* names; no operand is executed | other (name description) | **YES** | `command -v` is a query builtin; the gate instead treats `python3` as the head word (`head_index` steps over `command`, `count-c2.py:230`) |
| 22 | `C02:H08-function-def-never-called` | `f() { python3 -I tools/…; };` defines `f`, never calls it; the path is in the never-run body | function defined and never called | **YES** | same as #7 |
| — | `R03:N-A27-heredoc-data` *(uncounted, `reach: header-unreachable`)* | `cat >/dev/null <<'X' … X` — the path is inside the heredoc *body*, i.e. data on `cat`'s stdin | heredoc data | **YES** | heredoc bodies are data by definition; the gate's `shlex`-based tokenizer does not model heredocs |

Grouped by family (counted):

| family | n | cases |
|---|---|---|
| function defined and never called | 2 | A13, H08 |
| PATH/interpreter substitution | 5 | A11, A12, A16, A17, A22 |
| sitecustomize | 1 | A15 |
| blob overwrite | 1 | A18 |
| heredoc data | 0 counted (+1 uncounted) | A27 |
| `uv run -m` | 1 | A23 |
| `bash -n` / no-exec mode | 3 | A06, A07, A14 |
| `cat`/`$0` | 2 | A01, A04 |
| other (cwd re-resolution ×5, wrong interpreter ×1, name-description ×1) | 7 | A19, A20, A21, A24, A28, A26, A29 |
| **total** | **22** | ✔ |

Syntax-decidability split: **18 of 22 are decidable from the recorded command text alone**
(2 functions, 5 interpreter-substitution, 1 blob-overwrite, 1 uv-`-m`, 3 no-exec, 2 cat/`$0`,
plus the 4 cwd cases = 18); **4 are not** — `N-A15` sitecustomize, `N-A16` PATH fake,
`N-A17` relative symlink, `N-A26` bash-runs-.py. The uncounted `N-A27` heredoc is decidable.

### The consequence the L1 must not miss

`count-c1.py:66` pins `TARGET = "C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78"`, and
`open` is computed as *every counted reject case the gate still binds*
(`count-c1.py:146-147`). Since the 22 above are exactly that residual, **closing any one of them
drops `open` to 21 and the frozen C1 predicate misses.** The design ("provenance class is
reported, never targeted") is therefore a *target-pinning* constraint, not only a claim about
decidability: 18 of the 22 have a purely textual rule that could close them, and the target
forbids using it. That is worth stating explicitly in the round-90 write-up, because
`count-c1.py`'s own docstring says the provenance class is "which a syntax rule cannot decide" —
for 18 of the 22 that statement is **false as written**. Any future rule tightening has to move
the target and the target line together, in the same commit, or C1 will read `open=21` and fail
for the wrong reason. (No such change is proposed here; this seat is read-only.)

## 3. Where the gate's rule loses these (mechanism → gate gap)

Measured with the tip gate blob, per case, the *exact* token position it binds:

| case | invocation head | bound token | why the r87 rule does not exclude it |
|---|---|---|---|
| A01 | `sh` | word 8 | `head_index` knows no `sh -c` operand rule; the `-c` string has no whitespace so no recursion |
| A04 | `cat` | word 1 | `DATA_HEADS = {echo, printf, :, true, false}` (`count-c2.py:154`) omits `cat` |
| A06 | `bash` | word 2 | no `bash -n` rule; `bash` is not a wrapper in `WRAPPERS` (`count-c2.py:155`) |
| A07 | `bash` | word 3 | same |
| A11 | `python3` (the *function*) | word 2 | function definitions are invisible to the token model: `f`/`{`/`}` are read as command heads |
| A12 | `python3` | word 2 | `hash` is an ordinary command word; the rebinding is not modelled |
| A13 | `python3` | word 2 | `f` and `(` are read as command heads; the body is not recognised as a definition |
| A14 | `python3` | word 2 | `set -n` is not modelled at all |
| A15 | `python3` (after `PYTHONPATH=s`) | word 2 | `PYTHONPATH=s` is only an assignment prefix; `-I` is absent, so nothing is excluded |
| A16 | `python3` (after `PATH=$PWD/f:$PATH`) | word 3 | the assignment prefix is skipped, the interpreter word is trusted |
| A17 | `./python3` | word 2 | `PYTHON = re.compile(r"python(\d+(\.\d+)*)?$")` is applied to `basename`, so `./python3` is taken for CPython |
| A18 | `python3` | word 2 | the *redirect target* is correctly excluded, but the same path reappears as the script operand and binds there |
| A19/A20/A28 | `python3` | word 2 | `cd` is an ordinary command word; cwd is never tracked, so the relative operand is compared repo-relatively (`same_path`, `count-c2.py:302`) |
| A21 | `env` | word 5 | `head_index` returns `None` for `env` with `-C`/`-S` (`count-c2.py:243-245`) ⇒ *nothing* is excluded for the whole invocation |
| A22 | `env` | word 2 | same `env` bail-out |
| A23 | `uv` | word 5 | `uv` is not in `WRAPPERS`, not `PYTHON`; `-m` is not modelled for `uv` |
| A24 | `uv` | word 8 | same + cwd not tracked |
| A26 | `bash` | word 1 | `bash` is not modelled as an interpreter at all |
| A29 | `python3` | word 3 | `command` is a wrapper with no options (`WRAPPERS["command"] = ()`), so `-v` is walked past and `python3` becomes the head |
| H08 | `{` | word 3 | `{`/`}` are punctuation; the body is read as a command list |
| A27 | `python3` | word 2 | heredoc bodies are not modelled by the `shlex` tokenizer (`shell_tokens`, `count-c2.py:201`) |

## 4. Execution evidence for the mechanisms (scratch fixture, `$HYAKU_SCRATCH/mori-r90/Mo90Sc01Scope`)

Fixture: `tools/mori-record-sweep.py` prints `REAL_SWEEP_BODY`; the recorded command text is run
verbatim in a **pristine** `bash` (`env -i PATH=… HOME=… bash -c`, so no inherited `PATH` and no
inherited hash table); "blob ran" = `REAL_SWEEP_BODY` on **stdout** (stderr is excluded — for
`bash -n`/`bash <file>` bash *echoes the offending line* into stderr, which contains the string
but is not an execution). Result for **all 23 bound provenance cases**:
`real_blob_ran=False` — the recorded blob never executed; the `RECORD_SWEEP …` body came from the
counterfeit mechanism instead. Sample lines:

```
R03:N-A06-bash-n      real_blob_ran=False  out=RECORD_SWEEP … | tools/mori-record-sweep.py: line 1: syntax error near unexpected token `"REAL_SWEEP_BODY"'
R03:N-A23-uv-run-module real_blob_ran=False out=RECORD_SWEEP …
R03:N-A26-bash-runs-python-file real_blob_ran=False out=RECORD_SWEEP …
C02:H08-function-def-never-called real_blob_ran=False out=RECORD_SWEEP …
```

Two probes deserve to be recorded because they are the evidence for "not syntax-decidable":

* **`N-A16` needs a run-time fact, not a textual one.** The recorded text
  `PATH=$PWD/f:$PATH python3 -I tools/mori-record-sweep.py …` deterministically runs the fake
  `f/python3` in a pristine shell — `env -i PATH=/usr/bin:/bin bash -c '…'` printed the fake body
  three times out of three, and also with `python3` pre-hashed to `/usr/bin/python3` and with
  `hash -r` (bash re-resolves through the new `PATH` because the assignment prefix changes
  `PATH`). What makes it *not* syntactically decidable is that the deciding inputs — the
  shell's `PATH`, the freshly created `f/python3`, bash's hash table — are all run-time state
  outside the recorded text. (An earlier run of mine that appeared to make this case flip was
  caused by my own shell's `PATH`/hash pollution, not by the case; the numbers above are from
  `env -i` runs with no inherited state.)
* **`N-A23` fails either way.** With `uv` present: `Error while finding module specification for
  'tools/mori-record-sweep.py' (ModuleNotFoundError: No module named 'tools.mori-record-sweep')`
  — module-name semantics; with `uv` absent: `bash: uv: command not found`. In both worlds the
  bound blob does not run. `N-A24` with `uv` present printed the fake `d/tools/…` body
  (`FAKE_BODY`), never the bound blob.

`N-A25-prod-absolute`, `N-A30-glued-hash`, `N-A02`, `N-A03`, `N-A05`, `C02:H05/H06/H07/H11/H12/H13`
are the 11 counted rejects the r87 rule already refuses — they are not in this table.

## 5. Confidence and open gaps

* High confidence (measured, reproducible): the partition 8 / 22 / 11; the count check; the
  per-case mechanism and the bound-token positions; the "blob never ran" result for all 23.
* Medium confidence: the exact decidability verdict for `N-A22` (`env -iS` argv re-splitting),
  `N-A21` (`-iCd` getopt folding) and `N-A28` (`$'cd'` ANSI-C unquoting) — each needs shell/env
  semantics that are deterministic but not yet implemented anywhere in the lane; my verdicts are
  from the semantics plus the observed runs, not from an existing rule.
* Low confidence / not decided here: whether a *sound* rule could close `N-A11`/`N-A13`/`H08`
  without also closing the branch class (the branch class is control-flow, so the families look
  disjoint, but I did not attempt the rule — out of scope for a read-only seat).
* Known gaps I did not chase: `N-A26` "arguable" status is inherited from the r89 battery's own
  `why` field; the `reach: header-unreachable` reason for `N-A27` is inherited from the frozen
  `cases.json` and not re-derived here.

## 6. Housekeeping

* Tools: **no install or upgrade was performed** — everything used (`git`, `python3`, `bash`,
  `shlex`, `uv` as a *subject* of the probe) was already present. No `pacman` transaction was
  attempted (host-wide pacman pause in force). Tooling-authorisation record: n/a.
* Lane files touched: **none**. `git status --porcelain` in the lane shows only the other seats'
  in-flight `w1/` work (` M .ufo/waves/round-90/w1/Mo90M01Mut.md`); I created no file in the
  lane except this report.
* Scratch: everything ran under `$HYAKU_SCRATCH/mori-r90/Mo90Sc01Scope/` (gate copies, the
  probe scripts, four throwaway fixtures). Removed before yielding; no fixture, clone or temp
  tree of this seat remains on disk.
* No candidate was written (read-only seat).
