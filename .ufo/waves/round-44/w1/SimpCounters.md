# SimpCounters — dead weight in the four frozen instruments

Scope: `.ufo/waves/round-44/count-c1.py`, `count-c2.py`, `count-c3.py`,
`tools/mori-gate-registry.py`, at the lane tip `7cb59c6891d4f5d0266fe062565f094da835dc84`.
Output: a routed list. **No instrument byte was edited**; every command below ran
read-only against the lane or in a `/tmp/simp44.cFkNau` copy.

## 0. Verdict

**Zero of the 28 items below can be removed before this round's after-measurement.**
All four files are pinned by sha256 in `.ufo/waves/round-44/evidence/freeze-r44.txt`,
and `contract.md` §Freeze says their "bytes are not amended after any seat scores
them; a defect found post-freeze is recorded as a lesson and routed to round 45,
never patched in place." A deletion is a byte change, so the freeze rule decides
every row uniformly. The per-item value of this report is therefore the *diff* and
the *class*, not a go/no-go: each item is marked

- **DEL** — pure deletion, provably verdict-neutral; round 45 may apply as-is.
- **DEL+ARM** — deletion is verdict-neutral only after an arm is added (or the
  deletion changes which input is scored).
- **ARM** — nothing to delete; the path needs a test arm before it can be trusted
  or dropped.
- **KEEP** — duplication or a guard that is load-bearing; removing it would harm an
  axis (stated per item).

Two items are not simplifications at all but must be reported because they change
what the round's own measurement does:

1. `count-c2.py`'s `--mutants-dir` default (`fixtures/mutants`) names a directory
   that has **never existed in this repo**. With the documented default the counter
   prints `C2=unmet` even though every mutant is committed (receipt §8.3). The
   after-measurement must pass `--mutants-dir .ufo/waves/round-44/fixtures/mutants`.
2. `count-c2.py`'s auditor-absent branch raises `UnboundLocalError` instead of
   printing a verdict (receipt §8.4). Exit code is 1 (the "unmet" code) but no
   `C2=unmet` line is printed — a verdict-map hole, not a simplification.

## 1. Method and instrument identity

`sha256sum` of the four files matches `evidence/freeze-r44.txt` line for line
(4/4), so the bytes analysed are the frozen bytes:

| file | sha256 (matches freeze) |
|---|---|
| `.ufo/waves/round-44/count-c1.py` | `9477824d…71999f83` |
| `.ufo/waves/round-44/count-c2.py` | `0095d0c6…f17f9047` |
| `.ufo/waves/round-44/count-c3.py` | `a12170f1…e9c440c68` |
| `tools/mori-gate-registry.py` | `743996b1…7e125a1f` |

Tools used (installed under the standing tooling directive):

- `pyflakes 4.0.3` — `uv tool install --force pyflakes` (the pre-existing
  `~/.local/bin/pyflakes` symlink was broken; `--force` repaired it).
- `coverage 7.17.0` — already installed via `uv`; used for line **and branch**
  coverage of each instrument's own `--selftest`.

Selftest tallies reproduce the freeze receipt exactly, from the sandbox copy:

```
count-c1: C1_SELFTEST pass=6 fail=0      count-c3: C3_SELFTEST pass=6 fail=0
count-c2: C2_SELFTEST pass=5 fail=0      gate-registry: GATE_REGISTRY_SELFTEST pass=6 fail=0
```

Coverage of each `--selftest` (line / branch):

| instrument | statements | missed | branch arcs missed |
|---|---|---|---|
| `count-c1.py` | 259 | 63 (76%) | 36 |
| `count-c2.py` | 249 | 43 (83%) | 22 |
| `count-c3.py` | 217 | 44 (80%) | 20 |
| `mori-gate-registry.py` | 227 | 41 (82%) | 27 |

The single largest coverage hole in all four is the same one: `main()` is never
entered by any `--selftest` (see item 16).

## 2. Unused imports — none

```
$ ~/.local/bin/pyflakes .ufo/waves/round-44/count-c1.py   → rc=0
$ ~/.local/bin/pyflakes .ufo/waves/round-44/count-c2.py   → rc=0
$ ~/.local/bin/pyflakes .ufo/waves/round-44/count-c3.py   → rc=0
$ ~/.local/bin/pyflakes tools/mori-gate-registry.py       → rc=0
```

Every module-level constant is referenced (`CLASSES`, `GIT_VERBS`, `ID_RE`,
`DIGITS`, `TALLY`, `GOOD_ROW`, `HEADER`, `COUNTER_OK`, `COUNTER_NO_SELFTEST`,
`MUTANT_KILLED`, `MUTANT_SURVIVED`, `ENTRY_OK`, `ROW_OK`, `CENSUS_OK`,
`CENSUS_RED`, `ROW_RE`, `FIELDS`, `CELL_SPLIT`). pyflakes does **not** report
unused *parameters*; those are items 25-28.

## 3. Master list

Line numbers are frozen-file line numbers. "arc" = a `coverage --branch`
`missing_branches` entry `(from → to)` that was never taken.

### Provably unreachable

| # | site | construct | proof | r45 |
|---|---|---|---|---|
| 1 | `count-c1.py:98` | `elif cmd.split()[1:2] and cmd.split()[1] not in GIT_VERBS:` — the `cmd.split()[1:2] and` conjunct | line 96 (`if not cmd.startswith("git ")`) plus the `c.strip()` at line 89 mean `cmd` always has ≥2 tokens here. `cmd.split()` is also evaluated 3× on one line. | **DEL** |
| 2 | `mori-gate-registry.py:132` | `label = row[0] if row else "?"` | `row = sorted(matches, …)[0]`; `matches` is non-empty (line 127 `continue`s otherwise). The `else "?"` can never evaluate. | **DEL** |
| 3 | `count-c2.py:112` | `if auditor_path:` inside `selftest_env` | single call site, line 140, sits inside the `else:` of `if auditor is None:` — `auditor_path` is always a real path there. | **DEL** |

### Vacuous pass

| # | site | construct | proof | r45 |
|---|---|---|---|---|
| 4 | `count-c1.py:151,160` | `if not problems:` guards the row loop; `record("commands_reconcile", not mismatches, …)` then reports `all rows match` on an empty list | receipt §8.5: a ledger with one grammar problem prints `rows_parse FAIL` **and** `commands_reconcile PASS (all rows match)`. The second line is a claim about rows that were never run. | **DEL+ARM** (guard the record, or record `n/a`; needs an arm asserting the detail text) |

### Cannot complete

| # | site | construct | proof | r45 |
|---|---|---|---|---|
| 5 | `count-c2.py:133-135` | `if auditor is None:` records two FAILs, then line 160 uses `env`, which is only bound at line 140 in the `else:` branch | receipt §8.4: `UnboundLocalError: cannot access local variable 'env'`. Exit 1 with a traceback and no `C2=` verdict line. arc `133 → 134` untaken by the suite. | **DEL+ARM** (bind `env` before the `if`; add `auditor_absent_unmet`) |

### Duplicated code (frozen; see §4 for why it cannot be collapsed now)

| # | duplication | evidence | r45 |
|---|---|---|---|
| 6 | `class Setup(Exception)` — byte-identical in c1/c2/c3 (normalised hash `3ddf711882`); the auditor uses bare `RuntimeError` instead | AST hash of function/class bodies | **KEEP** — a shared `Setup` requires a shared module (see §4.2) |
| 7 | `_registry(rows)` — byte-identical in `count-c2.py:224` and `mori-gate-registry.py:163` (`ea59d7429d`) | idem | **KEEP** — c2's fixture must build the auditor's own SKILL.md format; a shared helper breaks single-file isolation |
| 8 | `read_at(repo, rev, path)` — `count-c2.py:65` and `count-c3.py:60` byte-identical (`5a83e581f5`); c1 (`8cc571e174`) and the auditor (`7c28ccead3`) are near-copies | idem | **KEEP** |
| 9 | `repo_default()` — four divergent variants: c1 walks up with a comment block, c2/c3 walk up (different comments), the auditor is a 3-line `dirname(dirname(here))` that does **not** walk up | idem | **DEL+ARM** for the auditor variant only: c2 always passes `--repo` (line 137), which masks the divergence; a walk-up auditor needs an arm proving a copied auditor resolves, or the one-liner should be deleted in favour of an explicit `--repo` |
| 10 | `git(repo, args, timeout)` — four variants; only the auditor lacks the `TimeoutExpired → Setup` guard | c1:52-59, c2:57-62, c3:52-57, gr:37-39 | **KEEP** (guard is a real behaviour difference; unifying it is a round-45 design call) |
| 11 | fixture-repo builder — four copies: `_mk_repo` (`count-c1.py:169`, 21 ln) plus three `_mk` variants (`count-c2.py:229` 18 ln, `count-c3.py:176` 16 ln, `mori-gate-registry.py:168` 16 ln) | AST spans | **KEEP** |
| 12 | markdown cell splitter — `count-c3.py:32 FIELDS = re.compile(r"(?<!\\)\|")` and `mori-gate-registry.py:63 CELL_SPLIT = re.compile(r"(?<!\\)\|")`: the same regex, two names, two files | idem | **KEEP** (see §4.3) |
| 13 | column-position authority duplicated *inside* one file: `mori-gate-registry.py` locates the entry cell by hardcoded index 2 (`entry_names(r[2], base)`, lines 122-126) while also parsing the header (`dict(zip(header, row))`, line 133); `count-c3.py` hardcodes `cells[7]` (status) and `cells[10]` (used-by) and never parses a header at all | source | **DEL+ARM** — replacing the hardcoded indices with header lookups changes which column is scored; needs a reordered-header arm first |
| 14 | `count-c2.py` reads every counter twice per evaluation: `present = {c: read_at(...)}` (line 125) and then `materialize(...)` (line 155) re-runs `cat-file -e` + `show` on the same path | source | **DEL+ARM** — derive `counters_present` from `materialize`'s result; the check would move after the `mkdtemp`, so the arm must assert check order |
| 15 | `count-c1.py:158-159` appends the *same* formatted string to `mismatches` and `details`; line 155-156 appends two *different* strings to the same pair | source | **KEEP** — the two lists carry different wording in branch 1, so collapsing them changes the printed detail text |

### No test arm (arm needed, or the path is untested and must stay)

| # | site | what is unarmed | evidence | r45 |
|---|---|---|---|---|
| 16 | c1:293-349, c2:350-384, c3:280-317, gr:273-304 | **`main()` in all four instruments.** No `--selftest` ever calls it, so every CLI argument, the usage exit, the `*_SETUP` exits, the WORK tip fallbacks, the `except Setup` catch and the final verdict print are unexecuted | coverage lines: c1 306-349, c2 363-384, c3 295-317, gr 284-304; arc `304 → 306` (c1) untaken | **ARM** |
| 17 | c1:147-148 | `class_floor` has **no failing arm**: every arm calls `evaluate(..., 12, 4, 20)`, i.e. the defaults; `below_floor` uses 5 rows but still 5 classes ≥ 4 | receipt §8.6: with `min_classes=6` the check does fail, so the check works and nothing tests it. A mutant setting `class_floor` to `True` would survive (the committed mutant disables `row_floor` instead) | **ARM** |
| 18 | c2:149-151 | `tool_selftest` has **no failing arm**: `_base_files()` always embeds the unmodified auditor, so its tally is always `pass=6 fail=0` | `auditor_bytes()` appears twice in the file: its definition and `_base_files` | **ARM** |
| 19 | gr:140-144 | the `entry path does not resolve` branch is **never reached**. The arm named `unresolved_entry_rejected` swaps the *row's* path to `tools/ghost-tool.sh` but still audits `tools/fixture-tool.sh`, so it is refused one branch earlier as `unregistered` | receipt §8.7: arm detail = `unregistered: no row names fixture-tool.sh`. The branch is reachable with a correctly targeted fixture (`audit(..., ["tools/ghost-tool.sh"])` → `row 'fixture gate' entry path does not resolve at 0dfeef3cb0f5`) | **ARM** — the arm is mis-targeted, not the code. `SKILL.md`'s verdict-map cell names this class, so the round currently documents a failure class it cannot demonstrate |
| 20 | gr:122-126 | the **primary** `entry_names` match — the guard that a row *names* the tool rather than merely *passing* it as an argument — never fires in the auditor's own suite | arc `124 → 127` untaken (line 124's condition was always true ⇒ primary always missed). Probe: `entry_names("`bash tools/fixture-tool.sh`", "tools/fixture-tool.sh")` → `False`; `entry_names("`python3 tools/fx-one.py <rev>`", "tools/fx-one.py")` → `True`. `GOOD_ROW` ends the backticked cell at the path, so the `(?:\s|$)` tail cannot match; production rows (SKILL.md, `<rev>` after the path) do match | **ARM** — add a row that only passes the path (`python3 tools/wrapper.py tools/fixture-tool.sh`) and a row shaped like the real registry; the substring fallback currently accepts the former |
| 21 | c1:83-99 | 6 of the 10 `parse_ledger` grammar branches are unarmed: blank/comment skip (83→84), wrong cell count (86→87), bad id (90→91), non-integer asserted (92→93), unknown class (94→95), non-read git verb (98→99). The other four *are* armed: `git`-prefix (junk_producer), `@REV@` (junk_producer), single pipeline (compound_command), non-byte producer (junk_producer) | coverage + receipt §8.8: a direct `parse_ledger` probe produces every one of the 7 messages, so all six unarmed branches are reachable | **ARM** |
| 22 | c1:117-123, 154-156 | `run_row` timeout, non-zero rc, non-integer output, and the `got is None` detail path | arcs 117→118, 119→120, 122→123, 154→155 all untaken | **ARM** |
| 23 | c3:107-108, 114-116, 122-124, 127-128, 142-143 | `coverage-map:` present but wrong value (the arm deletes the key entirely, so only the `not in text` half is armed); `corpus/SOURCES.md` absent; a declared row id absent from the registry; `status != "mined"` (the sibling `used-by` half *is* armed); census timeout | arcs 107→108, 114→115, 122→123, 127→128, and missing lines 115-116, 123-124, 128, 142-143 | **ARM** |
| 24 | c2:96-97, 101-102, 170-172, 252-257 | `run_script` timeout → `None`; `tally_of(None)`; **mutant absent** (the `absent_counter` arm `continue`s at line 159 before the mutant read); `auditor_bytes`'s `raise Setup` and the `MORI_GATE_REGISTRY` override branch | missing lines 96-97, 102, 171-172, 257; arcs 101→102, 170→171, 252→257, 254→252 | **ARM** |
| 25 | gr:68-72, 89-90, 94-95, 101-103, 112-113, 115-116 | `split_row`'s leading-`|` and trailing-`|`/`\|` guards are always-true given the only caller (line 96 filters `startswith("|")`), so the escaped-pipe-last-cell case is untested; no `## Gates` section; a new `## ` section ending the table; a pipe row *before* the header; registry file absent; no `name/kind` header | arcs 68→70, 70→72, 89→90, 94→95, 101→103, 112→113, 115→116 | **ARM** for the escaped-pipe and header-absence cases; the two `split_row` guards are **KEEP** (defensive, and MutRegistry item 5 probes the escaped pipe externally) |
| 26 | all four | **WORK mode.** `read_at`'s `rev == "WORK"` branch, `main`'s WORK tip resolution (`rev-parse master` then `HEAD`) and its double-fallback are unexecuted in every instrument, although `<rev|WORK>` is in every usage string | c1 64→65, c2 66→67, c3 61→62, gr 43→44 and 49→50; missing lines c1 65-69, c2 67-71, c3 62-66, gr 50-54 | **ARM** |
| 27 | argument surface | non-default values never exercised (see §5 table) — including `--min-rows`, `--min-classes` (only ever 12/4), `--min-arms` (only 2), `--mutants-dir` (only its broken default), `--ledger`, `--entry`, `--readme`, `--coverage-map`, `--census` (only a non-default), `--registry`, every `--repo` default | `re.findall` over the arm bodies; all six c1 arms pass `(12, 4, 20)` | **ARM** (one non-default arm per argument, or drop the argument) |
| 28 | dead parameters | `count-c2.py:91 run_script(..., cwd=None, ...)` — never passed; `count-c3.py:176 _mk(tmp, files, commit=True)` — `commit` never read *at all*; `mori-gate-registry.py:168 _mk(..., tool_name="tools/fixture-tool.sh")` — never varied; `count-c1.py:169 _mk_repo(..., commit=True)` — never `False` (arc 185→188 untaken) | call-site greps: `run_script(` ×4 all keyword-free on `cwd`; `_mk(` in c3 has one call site; `_mk(` in gr ×6 all 3-arg; `_mk_repo(` ×6 all 2-arg | **DEL** (pure signature deletion) |

Count: 3 unreachable + 1 vacuous + 1 cannot-complete + 10 duplication + 13 unarmed = **28**.

## 4. Why the duplicated parse logic cannot be collapsed now

### 4.1 The freeze rule decides it

`evidence/freeze-r44.txt` pins sha256 for all four files and `contract.md` §Freeze
forbids amendment after any seat scores them. A dedup is an amendment. Additionally
the committed mutants are **one-line diffs of these exact bytes** (`row_floor`,
`mutant_kill`, `census_ok` set to `True`); re-basing any counter invalidates the
property C2 measures (`mutant_kill`), because a mutant must be a mutant *of the
frozen instrument*, not of a rewritten one. Any figure-ledger row that counts bytes
or lines of these files also shifts.

### 4.2 The counters must stay single-file executables — this is structural, not stylistic

`count-c2.py` does not import the counters; it copies each one **alone** into a
temp dir and runs it there:

```
132:  auditor = materialize(repo, rev, "tools/mori-gate-registry.py", tmp)
155:  path = materialize(repo, rev, c, tmp)
 91:  def run_script(path, args, timeout, cwd=None, env=None):
 95:                              cwd=cwd or os.path.dirname(path), env=env)
```

`materialize` writes one basename into `tmp`; `run_script` sets `cwd` to that same
temp dir. A `from mori_common import read_at` would therefore fail with
`ModuleNotFoundError` — in the *green* arm of C2's own selftest, not in some
hypothetical. Deduplicating `Setup`/`read_at`/`git`/`repo_default` (items 6-11)
requires either a vendored-include step inside `materialize` or abandoning C2's
"run the committed bytes as they are" property. That is a design change with a new
predicate, not a simplification.

### 4.3 The two table parsers are not actually the same parser

`count-c3.py:32` and `mori-gate-registry.py:63` hold the same escaped-pipe regex
under two names, but the consumers differ: the auditor locates a header row and
builds `dict(zip(header, row))`; C3 never looks at a header and indexes `cells[7]`
and `cells[10]`. Merging them means picking one column authority (item 13), which
changes which cell is scored — a verdict change. Safe only after the reordered-header
arm exists.

### 4.4 What *could* be deleted without touching any parser

Items 1, 2, 3 and 28 are token-level deletions with no control-flow effect: a
dead conjunct, a dead `else`, an always-true `if`, and four never-passed parameters.
They are the only rows in this report whose diff a reviewer can accept by reading
alone. They are still frozen this round.

## 5. Arguments never exercised with a non-default value

| instrument | argument | arms use | default | note |
|---|---|---|---|---|
| c1 | `--ledger` | the default path | same | only default |
| c1 | `--min-rows`, `--min-classes` | `12`, `4` | same | item 17 |
| c1 | `--timeout` | `20` | same | so item 22's timeout branch is doubly unarmed |
| c1 | `--repo` | arms call `evaluate()` directly | `repo_default()` | `main` untested |
| c2 | `--mutants-dir` | `fixtures/mutants` | same | **and the default is broken in the lane repo** — see §8.3 |
| c2 | `--min-arms` | `2` | same | |
| c2 | `--timeout` | `60` | `120` | exercised |
| c3 | `--census` | `fixtures/fake-census.sh` | `dirname(repo)/scripts/sources-census.sh` | default derivation untested; it resolves to the **fleet root** (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, tracked in the fleet repo, absent at the lane freeze commit) — so C3's census check is not reproducible from lane-committed bytes alone |
| c3 | `--entry`, `--readme`, `--coverage-map` | `fixture-entry.md`, `corpus/README.md`, `FR5` | the same values | only defaults |
| c3 | `--timeout` | `60` | `120` | exercised |
| gr | `--registry` | `SKILL.md` | same | only default |
| gr | `--repo` | explicit fixture repo | `repo_default()` | default untested (item 9) |
| all | positional `<rev>` | never | — | `main` untested in all four |

## 6. Proposed verbatim diffs (round 45; frozen this round)

**R1 — item 1 (`count-c1.py:96-99`), DEL.**
```diff
         if not cmd.startswith("git "):
             problems.append("row %d: command is not a git pipeline" % n)
-        elif cmd.split()[1:2] and cmd.split()[1] not in GIT_VERBS:
-            problems.append("row %d: git verb %r is not a read verb" % (n, cmd.split()[1]))
+        elif cmd.split()[1] not in GIT_VERBS:
+            problems.append("row %d: git verb %r is not a read verb" % (n, cmd.split()[1]))
```

**R2 — item 2 (`mori-gate-registry.py:131-132`), DEL.**
```diff
         row = sorted(matches, key=lambda r: len(r[2]))[0]
-        label = row[0] if row else "?"
+        label = row[0]
```

**R3 — item 3 (`count-c2.py:109-114`), DEL.**
```diff
 def selftest_env(auditor_path):
     """Fixture plumbing: a counter copy run from a temp dir resolves the auditor."""
     env = dict(os.environ)
-    if auditor_path:
-        env["MORI_GATE_REGISTRY"] = auditor_path
+    env["MORI_GATE_REGISTRY"] = auditor_path
     return env
```

**R4 — item 5 (`count-c2.py:130-131`), DEL+ARM.** Bind `env` before the branch so the
absent-auditor path reports instead of crashing; behaviour on the green path is
byte-identical (`selftest_env(auditor)` still overwrites it at line 140).
```diff
     tmp = tempfile.mkdtemp(prefix="c2-")
+    env = dict(os.environ)
     try:
         auditor = materialize(repo, rev, "tools/mori-gate-registry.py", tmp)
```
New arm required: a fixture repo with no `tools/mori-gate-registry.py` asserting
`registry_rows`, `tool_selftest` and `mutant_kill` in `fails` and **no exception**.

**R5 — item 4 (`count-c1.py:160`), DEL+ARM.**
```diff
-    record("commands_reconcile", not mismatches, "; ".join(details[:4]) or "all rows match")
+    record("commands_reconcile", not problems and not mismatches,
+           "; ".join(details[:4]) or ("not run: ledger has grammar problems"
+                                      if problems else "all rows match"))
```
This is the only diff here that changes printed text; the arm must assert the new
detail string.

**R6 — item 28a (`count-c2.py:91,95`), DEL.**
```diff
-def run_script(path, args, timeout, cwd=None, env=None):
+def run_script(path, args, timeout, env=None):
     try:
         return subprocess.run([sys.executable, path] + args, capture_output=True,
                               text=True, timeout=timeout, check=False,
-                              cwd=cwd or os.path.dirname(path), env=env)
+                              cwd=os.path.dirname(path), env=env)
```

**R7 — item 28b (`count-c3.py:176`), DEL.** `commit` is accepted and never read.
```diff
-def _mk(tmp, files, commit=True):
+def _mk(tmp, files):
```

**R8 — item 28c (`mori-gate-registry.py:168,176`), DEL.**
```diff
-def _mk(tmp, rows, tool_body, tool_name="tools/fixture-tool.sh"):
+def _mk(tmp, rows, tool_body):
     ...
-    full = os.path.join(repo, tool_name)
+    full = os.path.join(repo, "tools/fixture-tool.sh")
```

**R9 — item 28d (`count-c1.py:169,185-188`), DEL.**
```diff
-def _mk_repo(tmp, ledger_rows, extra_files=None, commit=True):
+def _mk_repo(tmp, ledger_rows, extra_files=None):
     ...
-    if commit:
-        git(repo, ["add", "-A"])
-        git(repo, ["commit", "-q", "-m", "fixture"])
+    git(repo, ["add", "-A"])
+    git(repo, ["commit", "-q", "-m", "fixture"])
```

**R10 — item 9 (`mori-gate-registry.py:32-34`), DEL+ARM.** One redundant `git
cat-file -e` per audited target: `audit` probes with `exists_at` (line 140) and then
`read_at` (line 145) probes again internally (line 55). `rev` is immutable, so the
double probe cannot change the answer.
```diff
-        if not exists_at(repo, rev, base):
-            results.append((target, False, "row %r entry path does not resolve at %s"
-                            % (label, rev[:12])))
-            ok = False
-            continue
-        body = read_at(repo, rev, base) or b""
+        body = read_at(repo, rev, base)
+        if body is None:
+            results.append((target, False, "row %r entry path does not resolve at %s"
+                            % (label, rev[:12])))
+            ok = False
+            continue
```
Must land together with item 19's correctly targeted arm, or the branch stays
unarmed while its only probe disappears.

**R11 — item 19 (arm, `mori-gate-registry.py:218-226`).** No code change; retarget
the fixture so the branch is reached:
```diff
-        row = GOOD_ROW.replace("tools/fixture-tool.sh", "tools/ghost-tool.sh", 1)
+        row = GOOD_ROW.replace("tools/fixture-tool.sh", "tools/ghost-tool.sh", 1)
         tmp = tempfile.mkdtemp(prefix="grst-")
         try:
             repo, rev = _mk(tmp, [row], tool_ok)
-            _res, ok = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
-            assert not ok, "an entry path that does not resolve was accepted"
+            res, ok = audit(repo, rev, "SKILL.md", ["tools/ghost-tool.sh"])
+            assert not ok, "an entry path that does not resolve was accepted"
+            assert "does not resolve" in res[0][2], res
```

**R12 — item 17 (arm, `count-c1.py`).** Add a `class_floor` arm; the check is
already proven able to fail (§8.6):
```diff
     def below_floor():
         ...  # unchanged
+
+    def class_floor_fails():
+        tmp = tempfile.mkdtemp(prefix="c1st-")
+        try:
+            repo, rev = _mk_repo(tmp, _honest_rows(), {"data.txt": "x\nx\nx\n"})
+            _c, fails, _m = evaluate(repo, rev, ".ufo/waves/round-44/figures.tsv",
+                                     12, 6, 20)
+            assert "class_floor" in fails, fails
+        finally:
+            shutil.rmtree(tmp, ignore_errors=True)
     ...
     arm("below_floor_rejected", below_floor)
+    arm("class_floor_rejected", class_floor_fails)
```

**R13 — item 18 (arm, `count-c2.py`).** Embed an auditor whose `--selftest` prints a
failing tally so `tool_selftest` can fail:
```diff
     def mutant_survives():
         ...  # unchanged
+
+    def auditor_selftest_red():
+        broken = auditor_bytes().replace(
+            'print("GATE_REGISTRY_SELFTEST pass=%d fail=%d" % (len(arms), len(failures)))',
+            'print("GATE_REGISTRY_SELFTEST pass=6 fail=1")')
+        tmp = tempfile.mkdtemp(prefix="c2st-")
+        try:
+            repo, rev = _mk(tmp, [GOOD_ROW],
+                            _base_files(**{"tools/mori-gate-registry.py": broken}))
+            _c, fails = evaluate(repo, rev, ["tools/fx-one.py"],
+                                 "fixtures/mutants", 2, 60)
+            assert "tool_selftest" in fails, fails
+        finally:
+            shutil.rmtree(tmp, ignore_errors=True)
     ...
     arm("surviving_mutant_unmet", mutant_survives)
+    arm("red_auditor_selftest_unmet", auditor_selftest_red)
```
The replacement target is verbatim from `mori-gate-registry.py:269`:
`print("GATE_REGISTRY_SELFTEST pass=%d fail=%d" % (len(arms), len(failures)))`.

**R14 — item 20 (arm, `mori-gate-registry.py`).** Add a row that only *passes* the
path, and one shaped like the real registry:
```diff
+    def passed_not_named():
+        row = GOOD_ROW.replace("`bash tools/fixture-tool.sh`",
+                               "`python3 tools/wrapper.py tools/fixture-tool.sh`", 1)
+        tmp = tempfile.mkdtemp(prefix="grst-")
+        try:
+            repo, rev = _mk(tmp, [row], tool_ok)
+            res, ok = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
+            assert not ok, "a row that merely passes the path was accepted: %s" % res
+        finally:
+            shutil.rmtree(tmp, ignore_errors=True)
```
This arm **will fail against the frozen bytes** (the substring fallback accepts the
row). That is the point: it is the arm that proves item 20's hole, and it is why the
fallback cannot be deleted before the primary matcher is made the sole authority.

**R15 — item 27 (`count-c2.py` default).** Repoint or drop `--mutants-dir`'s default;
with `fixtures/mutants` the counter cannot print `C2=met` in this repo (§8.3).
```diff
-    ap.add_argument("--mutants-dir", default="fixtures/mutants")
+    ap.add_argument("--mutants-dir", default=".ufo/waves/round-44/fixtures/mutants")
```

## 7. Tradeoff — where the next deletion would harm an axis

- Deleting the `split_row` guards (item 25) or the `@REV@`/`;`/`&&` grammar checks in
  `parse_ledger` because no arm exercises them would remove the only defence against
  the next caller that does not pre-strip its line, or the next ledger row that
  smuggles a compound command. Unarmed is not unused: the guards are cheap and their
  cost is one comparison.
- Deleting `repo_default`'s walk-up loop (c1/c2/c3) in favour of the auditor's
  one-liner would break the off-host replay path (`ExecOffHostReplay`'s clone), which
  is the one property that makes these instruments portable. The divergence in item 9
  should be resolved *toward* the walk-up, not away from it.
- Collapsing the two `mismatches`/`details` lists (item 15) would change the printed
  detail text, and that text is what a reviewer reads when a row is unreadable. The
  duplication is the price of two distinct messages; keep it.
- Deduplicating items 6-12 without first deciding how C2 materializes a counter
  would trade ~80 duplicated lines for the loss of C2's core property ("run the
  committed bytes, unmodified, in isolation"). That is the wrong trade.

Stop condition: every remaining item is either (a) a frozen byte this round, or
(b) a guard whose removal cannot be justified by an arm. The next deletion would
require a new predicate for C2's isolation model, which is a round-45 design
question, not a simplification.

## 8. Receipts

### 8.1 Frozen identity
```
$ sha256sum .ufo/waves/round-44/count-c1.py .ufo/waves/round-44/count-c2.py \
            .ufo/waves/round-44/count-c3.py tools/mori-gate-registry.py
9477824d5eee45f47d49be52902f7bb0cd67a4d038e0ec7e79094c1e71999f83  .ufo/waves/round-44/count-c1.py
0095d0c63afe1312c799dc8f6b8ad66d08eabf6420a9eabde032e894f17f9047  .ufo/waves/round-44/count-c2.py
a12170f1cad4a6a0eb18c14dd50b7e22e1dec4b67e5d44c217f8ed8e9c440c68  .ufo/waves/round-44/count-c3.py
743996b11d19261b87e3ea6c0d0be4c0e5e6750d05f6d603af51dc1a7e125a1f  tools/mori-gate-registry.py
```
Identical to `evidence/freeze-r44.txt` lines 5-8.

### 8.2 Selftest tallies, from the sandbox copy
```
selftest PASS honest_ledger_met / offbyone_row_mismatch / junk_producer_rejected /
             below_floor_rejected / absent_ledger_unmet / compound_command_rejected
C1_SELFTEST pass=6 fail=0                       (exit 0)
C2_SELFTEST pass=5 fail=0                       (exit 0)
C3_SELFTEST pass=6 fail=0                       (exit 0)
GATE_REGISTRY_SELFTEST pass=6 fail=0            (exit 0)
```

### 8.3 The `--mutants-dir` default cannot resolve
```
$ git ls-tree -d 7cb59c68 | awk '{print $4}'
.scratch .ufo considerthese corpus tools

$ git cat-file -e 7cb59c68:fixtures/mutants/count-c1.py      → NO
$ git cat-file -e 7cb59c68:.ufo/waves/round-44/fixtures/mutants/count-c1.py → YES
$ git cat-file -e 1429c791:fixtures/mutants/count-c1.py      → NO

$ python3 .ufo/waves/round-44/count-c2.py 7cb59c68 \
    --counter …/count-c1.py --counter …/count-c2.py --counter …/count-c3.py
check mutant_kill  FAIL (count-c1.py mutant absent; count-c2.py mutant absent; count-c3.py mutant absent)
C2=unmet                                        (exit 1)

$ … same command … --mutants-dir .ufo/waves/round-44/fixtures/mutants
check mutant_kill  PASS (count-c1.py killed (fail=1); count-c2.py killed (fail=1); count-c3.py killed (fail=1))
C2=met                                          (exit 0)
```

### 8.4 The absent-auditor branch crashes
```
fixture repo without tools/mori-gate-registry.py:
  RAISED UnboundLocalError: cannot access local variable 'env' where it is not associated with a value
  File "count-c2.py", line 160, in evaluate
      proc = run_script(path, ["--selftest"], timeout, env=env)
```
`record("registry_rows", False, …)` and `record("tool_selftest", False, …)` (lines
134-135) run first, so the checks are recorded and then lost with the traceback.

### 8.5 Vacuous `commands_reconcile`
```
ledger_present      PASS (567 bytes)
rows_parse          FAIL (row 1: command is not a git pipeline; …)
row_floor           PASS (rows=12 min=12)
class_floor         PASS (classes=checks,corpus,evidence,registry,wave min=4)
commands_reconcile  PASS (all rows match)        <-- no row was run
mismatches meta: None
```

### 8.6 `class_floor` is unarmed but able to fail
```
evaluate(..., 12, 6, 20) → fails=['class_floor']  meta.classes=5
all six arms: evaluate(repo, rev, ".ufo/waves/round-44/figures.tsv", 12, 4, 20)
```

### 8.7 The `unresolved_entry_rejected` arm reaches the wrong branch
```
audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"]) with a row naming tools/ghost-tool.sh
  → ok=False  results=[('tools/fixture-tool.sh', False,
                        'unregistered: no row names fixture-tool.sh')]
audit(repo, rev, "SKILL.md", ["tools/ghost-tool.sh"]) with the same fixture
  → ok=False  results=[('tools/ghost-tool.sh', False,
                        "row 'fixture gate' entry path does not resolve at 0dfeef3cb0f5")]
```

### 8.8 `parse_ledger` branches are reachable (so item 21 is an arm gap, not dead code)
```
row 3: id 'F1' is not F<digits>
row 4: asserted 'x' is not an integer
row 5: class 'nope' not in ['checks', 'corpus', 'evidence', 'registry', 'wave']
row 6: git verb 'config' is not a read verb
row 7: 3 TSV cells, want 4
row 8: command is not a git pipeline
row 8: command does not name @REV@
```
The comment line and the blank line were skipped without a problem, and the
`continue` at line 84 was never taken by any arm.

### 8.9 `entry_names` in the auditor
```
entry_names("`bash tools/fixture-tool.sh`", "tools/fixture-tool.sh")  → False   (GOOD_ROW shape)
entry_names("`python3 tools/fx-one.py <rev>`", "tools/fx-one.py")     → True    (registry shape)
entry_names("`bash tools/fixture-tool.sh --selftest`", "tools/fixture-tool.sh") → True
```
Branch arc `124 → 127` untaken in the auditor's own `--selftest`: the primary matcher
never fired there.

### 8.10 Shared tree untouched
```
$ git -C mori-shokunin status --porcelain
?? .ufo/waves/round-44/w1-spec.json        (pre-existing, not this seat)
```
No instrument was written; all scratch work lived in `/tmp/simp44.cFkNau`, removed
after the run. Tools installed: `pyflakes 4.0.3` (uv, repaired a broken symlink);
`coverage 7.17.0` was already present via uv and was not reinstalled.
