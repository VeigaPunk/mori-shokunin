# SimpInstruments — dead weight in the round-45 instruments

Scope: the wave's new code — `.ufo/waves/round-45/count-c1.py`, `count-c2.py`,
`count-c3.py`, `.ufo/waves/round-45/write-scope-run.py`, `tools/mori-gate-registry.py`
(v2), the three added `--selftest` branches (`tools/mori-silence-cases.sh`,
`tools/mori-round19-regressions.py`, `tools/mori-routed-check.py`), and the wave's
fixture scripts (`.ufo/waves/round-45/fixtures/mutants/*.py`, `fixtures/write-scope.json`,
`fixtures/witnesses/*.tsv`).

**Nothing in the lane was edited by this seat.** Every deletion below is a *proposal* with
the line range and the evidence that the range is dead. Scratch (coverage data files, run
outputs) lives in `.ufo/waves/round-45/tmp/SimpInstruments/` and is disposable.

## 0. Caveat that governs every number in this report

Seven of the eight artifacts were **still being rewritten by their executors while I
measured them** (c1 moved six times before settling at `5f2deea0` (08:06) — including after
its author declared it final, §2.1; gr five; c2 six; c3 four; wsr/routed/silence grew once
each; c2/c3 were red at 07:52 and green at 07:53:41). Every figure below is pinned to a
`sha256` and re-verified unchanged *before and after* the run that produced it. If a file's
hash no longer matches §2, treat the line ranges as stale and the finding as "re-read the
quoted code text" — the code text is quoted verbatim for exactly that reason.

## 1. Method

```
$ pyflakes --version            → 4.0.3 (uv tool, /home/vgpnk/.local/bin/pyflakes)
$ coverage --version            → 7.17.0 with C extension (uv tool)
```

No install was needed: both were already present as **uv-tool** binaries. `python3 -m
pyflakes <file>` fails (`No module named pyflakes`, rc=1) because the system interpreter
does not see the uv tool's site-packages; the item's command was therefore run as the CLI
`pyflakes <file>`, which is the same package and the only channel that can see it. Coverage
was run per instrument with

```
COVERAGE_FILE=$TMPDIR/.cov-<tag> coverage run --branch --data-file=… <instrument> --selftest
coverage report --data-file=… -m
coverage json   --data-file=… -o …      # missed lines mapped back to source text
```

i.e. **line + branch coverage of each instrument's own `--selftest` only** — the same
baseline round 44 used (`round-44/w1/SimpCounters.md` §1). `main()` is never entered by any
`--selftest`, so every `main` line shows as missed in all four Python instruments; that
single fact accounts for most of each miss count and is *not* dead code.

For `write-scope-run.py` (no `--selftest` exists) coverage was taken over a **real run**,
`--rev HEAD`, which is the invocation the fixture's own receipt used.

## 2. Pinned bytes, tallies, coverage

Measured 2026-10-25 07:54–07:55 -03, each hash identical before and after its run.

| artifact | sha256 (first 12) | lines | `--selftest` | stmts | miss | cover |
|---|---|---|---|---|---|---|
| `.ufo/waves/round-45/count-c1.py` | `5f2deea0b35c` (settled 08:06) | 1172 | `C1_SELFTEST pass=16 fail=0` rc=0 | 745 | 116 | **82%** |
| `.ufo/waves/round-45/count-c2.py` | `e8ee29eb8852` | 1001 | `C2_SELFTEST pass=10 fail=0` rc=0 | 605 | 168 | **67%** |
| `.ufo/waves/round-45/count-c3.py` | `37fd7c24ff52` | 700 | `C3_SELFTEST pass=19 fail=0` rc=0 | 485 | 76 | **80%** |
| `tools/mori-gate-registry.py` (v2) | `8b82ac999091` | 743 | `GATE_REGISTRY_SELFTEST pass=15 fail=0` rc=0 | 513 | 86 | **78%** |
| `.ufo/waves/round-45/write-scope-run.py` | `e5c81594a3e2` | 504 | *(no `--selftest`; real run `--rev HEAD` → `WRITESCOPE=met` rc=0)* | 354 | 81 | **73%** |
| `tools/mori-routed-check.py` | `b5498a54ceeb` | 1071 | `ROUTED_CHECK_SELFTEST pass=20 fail=0` rc=0 | 560 | 127 | **75%** |
| `tools/mori-silence-cases.sh` | `ff8b69757dea` | 1383 | `MORI_SILENCE_CASES_SELFTEST pass=24 fail=0` rc=0, `bash -n` clean | — | — | bash, not instrumentable |
| `tools/mori-round19-regressions.py` | `3c2c77d4d400` | 1442 | `R19_SELFTEST pass=26 fail=0` rc=0 | 674 | 334 | 48% whole file; added block ≈92% |

`count-c1.py`'s author told me its bytes were final (IRC, 07:47). **That did not hold**: the
file kept moving after the message — `84bf5879` → `f80e75ac` (819 lines) → `fc9b97e5` →
`a5e6577a` (999) → `d908aa9a` (1019) — so c1's findings below are anchored to *code text*
plus AST call-site counts, which survive the churn, and **no c1 line number in this report
should be trusted**; locate the quoted code instead.

### 2.1 Freeze check — the seal does not verify (integration finding, not a deletion)

```
$ sha256sum -c .ufo/waves/round-45/evidence/freeze-r45.txt
SKILL.md: OK
corpus/QUALITY.md: OK
.ufo/waves/round-45/contract.md: OK
.ufo/waves/round-45/figures.tsv: OK
.ufo/waves/round-45/count-c1.py: FAILED
.ufo/waves/round-45/count-c2.py: OK
.ufo/waves/round-45/count-c3.py: OK
.ufo/waves/round-45/write-scope-run.py: OK
.ufo/waves/round-45/fixtures/write-scope.json: OK
.ufo/waves/round-45/fixtures/mutants/count-c1.py: OK
… (c2/c3/gr mutants OK)
sha256sum: '(external) /home/vgpnk/Projects/shokunin/scripts/sources-census.sh': No such file or directory (os error 2)
(external) /home/vgpnk/Projects/shokunin/scripts/sources-census.sh: FAILED open or read
sha256sum: WARNING: 1 computed checksum(s) did NOT match
sha256sum: WARNING: 1 listed file(s) could not be read
rc=1
```

Two facts the after-measurement must know:

**`count-c1.py` is not the byte string the seal names.** Manifest pins `bbe90ce429902ac1…`;
the live file settled at `5f2deea0b35c` (1172 lines, 08:06) after moving six times — `sha256sum
-c` exits 1 at every check, so no after-measurement can be replayed against a named c1 byte
string. The *mutant* IS a clean one-line diff (duplicate-id check disabled) of the **live**
counter now (see G1); the seal's own pair is `bbe90ce4`/`9b339d84` (819 lines), which no
longer describes either live file. Re-seal the counter, or carry the sealed bytes — either
way the current manifest cannot be the freeze for an after-measurement.
**The manifest also contains an entry that can never verify.** The last line ends with
`(external) /home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, hashed
`3fb7261569f4…`, and that path does not exist on this host. Every other entry is
lane-relative and passes. (Whether the census pin is *meant* to be external is C3's
business; as written the manifest cannot reach `all checks OK`.)

Neither is a deletion proposal — §4 is. They are recorded because a freeze manifest that
cannot verify makes every "frozen instrument" claim in this round unfalsifiable.

## 3. pyflakes output (verbatim)

```
.ufo/waves/round-45/count-c1.py … rc=0 <clean>
.ufo/waves/round-45/count-c2.py … rc=0 <clean>
.ufo/waves/round-45/count-c3.py … rc=0 <clean>
tools/mori-gate-registry.py … rc=0 <clean>
.ufo/waves/round-45/write-scope-run.py … rc=0 <clean>
tools/mori-routed-check.py … rc=0 <clean>
tools/mori-round19-regressions.py rc=1
  tools/mori-round19-regressions.py:318:5: local variable 'paths' is assigned to but never used
  tools/mori-round19-regressions.py:750:5: local variable 'repo' is assigned to but never used
```

The two r19 names are **pre-existing**: the round's diff adds lines after 1102 only
(`git diff -U2 tools/mori-round19-regressions.py`: `@@ -1102,4 +1103,303 @@` and
`@@ -1113,5 +1413,16 @@`), so 318 and 750 are outside the added branch. They are listed in
§5 as out-of-scope, not as this round's dead weight.

pyflakes does not report unused *parameters*; those were found with an AST call-site scan
(passcount per function: every call site in the file, positional and keyword) and are §4's
main class.

## 4. Deletion list

Each entry: site, what dies, the proof, the smallest edit, and the corner (if any) where
behaviour is not byte-identical. **DEL** = pure deletion, verdict-neutral. **DEL+ARM** =
neutral only after the named arm exists. **ARM** = nothing to delete; the path needs an arm.

### 4.1 `count-c1.py` — anchored to code text (§2.1: the file moved six times before settling at `5f2deea0`; **no line number below can be trusted**)

**A1 — `git()`'s `timeout` parameter and its `env is not None` fallback. DEL.**
The definition, locate by text:
```python
def git(repo, args, timeout=30, env=None):
    try:
        return subprocess.run(
            ["git", "-C", repo] + args,
            capture_output=True, text=True, timeout=timeout, check=False,
            env=env if env is not None else child_env(),
        )
```
Proof: all three call sites pass `env=env` and none passes `timeout` —
`grep -n 'git(repo' count-c1.py` → 3 hits, each two-argument with `env=` only (AST call-site
scan re-run on `a5e6577a`: `git` 3 calls, `never-supplied=['timeout']`, and the same on the
819-line `f80e75ac`). Consequently `env if env is not None else child_env()` has an
unreachable `else`, and `timeout` is the constant 30 at every call. The `TimeoutExpired`
raise is missed in every coverage run.
Smallest edit: `def git(repo, args, env):`, `timeout=30` inline, `env=env` inline.
Preserves: the 30 s deadline, the `Setup("git timeout: …")` text (it interpolates `args`,
not `timeout`), and the scrubbed environment on every call.

**A2 — `_mk_repo(..., n=12)` fixture parameter. DEL.**
`def _mk_repo(tmp, rows, n=12):`, whose body uses `for k in range(1, n + 1):` twice.
Proof: 9 call sites, every one two-positional (AST scan on both `f80e75ac` and `a5e6577a`:
`_mk_repo` 9 calls, `never-supplied=['n']`); no caller can reach `n`.
Smallest edit: drop the parameter, use the literal `12` twice.
Preserves: the fixture shape (12 data files), every arm's rows (`_honest_rows()` also
defaults to 12).

**A3 — `main()`'s `WORK` guard duplicates `resolve()`'s. DEL (one corner differs).**
The guard, locate by text:
```python
    if args.rev == "WORK":
        print("C1_SETUP WORK is not a scoring revision: measure a committed revision")
        return 2
```
`resolve()` carries the same ruling as `if spec == "WORK": raise Setup("WORK is not a
scoring revision: measure a committed revision")`, which `main`'s `except Setup` handler
prints as `C1_SETUP <that text>` — byte-identical output, same rc 2. Proof: `resolve` has
exactly two call sites, both in `main`; the `args.rev` guard fires first, so `resolve`'s
guard is reachable **only** through `--other-rev WORK`, and the `main` guard is redundant for
its own input.
Corner that is *not* identical: `count-c1.py WORK --repo <non-git dir>` would print the
`repo is not a git checkout` setup reason instead of the WORK reason (both rc 2). If the
reviewer wants that corner frozen, keep the guard and delete nothing here.

**Explicitly KEEP in c1** (checked, not dead): `resolve()` has **no arm at
all** (every line missed; `main` is the only caller and no arm enters `main`) — that is an
ARM finding for MutCounters, not a deletion. `parse_ledger`'s
`int(asserted) if DIGITS.match(asserted) else -1` sentinel: the `-1` value is never observed
(rows are scored only when `problems` is empty), but the *guard* is load-bearing — deleting
it makes a non-integer ledger raise `ValueError` instead of reporting `rows_parse`.

### 4.2 `count-c2.py` @ `e8ee29eb8852` (1001 lines)

Re-pinned after the file's last edit (it moved three times while I measured). **The quoted
code text is the authority**; the offsets below are from the previous revision
(`922e5e7d582d`, 976 lines) and in `e8ee29eb8852` the five sites sit at: B1 `929–930`/
`941–942`, B2 `108` (call `109`), B3 `743`, B4 `811` (`subject` read at `586`),
B5 `338–369`. The call-site counts (9/9, 1/1, 10/10, 17/17) and the fixture shape are
unchanged in the new bytes — re-verified by AST scan and `grep` on `e8ee29eb8852`.

**B1 — `--rev` is a second spelling of the positional `rev`. DEL.**
Lines 904–905 and 916–917:
```python
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--rev", dest="rev_opt", metavar="REV")
…
    rev = args.rev_opt or args.rev
    if not rev or (args.rev and args.rev_opt):
```
Proof: no receipt, selftest arm or documented invocation of the counter uses `--rev`
(`grep -rn 'count-c2.py' .ufo/waves/round-45/evidence/ .ufo/waves/round-45/w1/` shows the
positional form only — `control-r44-c2.txt:13` runs `count-c2.py 554ff416…` with no
`--rev`; the `--rev` in §P-C2's prose names the *auditor's* flag, which `auditor_arm`
passes at 281). The `(args.rev and args.rev_opt)` disjunct exists only to
police the duplicate spelling, i.e. it is parsing weight created by the alias.
Smallest edit: delete the `--rev` `add_argument` (930), reduce 941–942 to `rev = args.rev` /
`if not rev:` (905 / 916–917 in the 976-line revision; the code text above is identical).
Corner: an out-of-tree caller that has learned `--rev` breaks — which is the deletion.

**B2 — `git()`'s `timeout` parameter. DEL.** Line 107 `def git(repo, args, timeout=30):`;
9/9 call sites are `git(repo, [...])` with no third argument. Inline `30` into the
`run(...)` call at 108. (Unlike c1 this wrapper has no `env` parameter, so nothing else moves.)

**B3 — `_mk()`'s `tables=None` parameter. DEL.** Line 721
`def _mk(tmp, files, tables=None):`; the single call site (inside the arm fixture builder)
passes two arguments. Delete the parameter and the branch that reads it.

**B4 — the arm fixture's `subject` parameter. DEL.** Line 789
`def fixture(files, env=None, subject="tools/fx-counter.py"):`; 10/10 call sites omit
`subject` (all pass `files`, some `env=`), so the default is the only value ever evaluated
and line 562 `name = os.path.basename(subject) if subject else ""` reduces to a constant.
Delete the parameter and inline the literal at 562. Preserves every arm: the surviving-mutant
arm relies on the default name to locate `fixtures/mutants/fx-counter.py`.

**B5 — `expect_of()`'s three unused input shapes. DEL.**
Lines 326–356 accept `dict`, `int`, and `str` (`rc=`/`exit=`/bare-digit/`k=v` pairs):
```python
        elif "exit" in exp:                     # 333-334
        elif isinstance(exp, int): rc = exp      # 340
        elif isinstance(exp, str) and exp.strip(): …  # 341-356
```
Proof: the only producer of `expect` in the repo is
`.ufo/waves/round-45/fixtures/write-scope.json`, and **7/7 entries are dicts** with
`rc` + `repo_unchanged` + `writes_outside_tmpdir` (no `exit`, no int, no string):
```
{'rc': 0, 'stdout_contains': [...], 'repo_unchanged': 'yes', 'writes_outside_tmpdir': 0} | r44-figure-ledger-c1
… same shape for all 7 entries (r44 ×4, r45 ×3)
```
Coverage at the re-pinned bytes is stronger than "the alternates are cold": the selftest
never enters `expect_of` **at all** (343–350, the dict arm itself, are also missed), so the
shape claim rests on the fixture, not on coverage — and the two `elif` chains have no
producer anywhere in the repo.
Smallest edit: keep `if isinstance(exp, dict):` block; delete 345–346 (`exit`), 351–352
(int), 353–368 (string parser) — the `e8ee29eb8852` offsets; in the 976-line revision they
were 333–334 / 340 / 341–356.
Corner: a hand-edited fixture in the string/int dialect would silently default to
`(0, True, 0)` instead of being parsed — acceptable for a fixture authored in this wave, but
state it: this is the one item where the deletion narrows an accepted input language.

**Also unarmed in c2 (ARM, not deletions)**: the whole `WORK` half — `read_at` 113–123,
`population()`'s WORK branch 135–139, `_work_ignore` 173–189 and `materialize_tree`'s WORK
copy 195–207 are all missed although `main` accepts `WORK` at 927; and `main` 916–972.

### 4.3 `count-c3.py` @ `37fd7c24ff52` (700 lines)

**C1 — `read_at()`'s `WORK` branch. DEL.**
Line 115 `if rev == "WORK":` with body 116–120 (`full = os.path.join(repo, path)`, existence
test, open, return bytes). Proof: `read_at` is called only from `evaluate`, and the only two
producers of `evaluate`'s `rev` are (a) `main` line ~688 `resolve_rev(repo, args.rev, …)`,
which cannot return `"WORK"` (it runs `git rev-parse --verify "<rev>^{commit}"`), and (b) the
selftest's `_fixture`, which passes a resolved sha. Every other `read_at` caller therefore
hands it a 40-hex sha.
Smallest edit: delete 115–120 (the WORK arm), keeping the git path. Preserves both the
selftest and the contract run, which are always at a resolved revision.
Corner: a future caller that passes `"WORK"` would get `None` from `cat-file -e WORK:<path>`
instead of reading the worktree — that failure mode is loud (`check` FAIL), not silent.

**C2 — `_expect()`'s `readme` parameter. DEL.** Line 428
`def _expect(fleet, repo, rev, entries, rows, maps, want, readme="corpus/README.md"):`;
17/17 call sites omit it and every one of them relies on the default. Delete the parameter,
inline the literal into the `evaluate` call at 432.

**ARM, not deletion, in c3**: `dedupe` (647) and `relative_entry` (655) are reachable only
from `main` (missed 697–724), which no arm enters — the argparse surface
(`--entering-rev`, `--root`, `--coverage-map`, `--census`, `--readme`, `--timeout`) is
unexercised. `--entering-rev` is **required** by contract Correction 1 and must not be
deleted.

### 4.4 `tools/mori-gate-registry.py` (v2) @ `8b82ac999091` (743 lines)

**D1 — `git()`'s `timeout` parameter. DEL.** Line 112
`def git(repo, args, timeout=30):`; 10/10 call sites omit the third argument. Inline `30`.

**D2 — the second `if not rev:` after a successful `rev-parse`. DEL (defensive).**
Line 706–707, immediately after 703–705:
```python
            rev = resolved.stdout.strip()
            if not rev:
                raise RuntimeError("cannot resolve revision %r" % args.rev)
```
`git rev-parse --verify <x>^{commit}` returns rc 0 only when it printed a commit id, so
`rev` is non-empty on that path; the branch is unreachable and duplicates the rc check two
lines above (same message text). The same shape exists at 497–498 in the fixture helper.
Smallest edit: delete 706–707 and 497–498. Preserves both `REGISTRY_SETUP` texts (the rc
branch keeps them).

**ARM, not deletion, in gr**: `mask_python` (256–277) is **entirely missed** by the
15-arm selftest, and `escape_branch`'s Python arm (342) is missed with it — every fixture
tool that carries a non-default self-test flag is a shell script. The real population
contains `.py` tools, so this is the auditor's largest untested surface (the r44
"silence-oracle" false positive was a comment-only `--selftest`; the arms prove that for
shell bodies only). `safe_relpath` 121–127 and `inside_repo` 132–134 are likewise missed —
path-escape refusals are unarmed. These are arm gaps; a verification-seat finding, not a
simplification.

### 4.5 `tools/mori-round19-regressions.py` added `--selftest` @ `3c2c77d4d400` (1442 lines; added branch from ≈1106, `run_selftest` at 1158)

**E1 — the `base` half of `claims-bind-expected-tips` cannot fail. DEL.**
Lines 1205–1206:
```python
            if claim["base"] != fixture["expected_bases"][claim["id"]]:
                tips_ok = False
```
`fixture["expected_bases"]` is built as `{claim["id"]: claim["base"] for claim in claims}`
— line 535 of the same file, from the same `claims` list (line 1201 iterates the register
re-read from disk, i.e. a JSON round trip of exactly those dicts). The comparison can only
differ if a duplicate id carries two bases, and `register-claims-unique` (1195–1198) already
rejects that. Coverage: 1206 never executes.
Smallest edit: delete 1205–1206, keep the `tip` half (1202–1204) and the check name — the
tip half compares against an independently written `expected_tips` dict and *can* catch a
future drift, so it is not dead.
Corner: none. `pass=26` becomes an unchanged tally (the arm still counts).

**E2 — `selftest_rejects`' `return False` is unreached (ARM).** Line 1145. All six call
sites (safe_repo_path ×3, output_path ×3 forms, json_load_bytes ×2, tool_path, require_tmpdir
×2) expect a raise, so no arm proves the helper returns `False` for an accepted input — the
helper would still "pass" if it always returned `True`. One line, one arm needed:
`tally.check("rejects-negative-control", not selftest_rejects(lambda: None))`.

**E3 — duplicated TMPDIR save/restore. DEL (pure dedup).** Lines 1293–1306: two
`try/finally` blocks with the same save/restore, differing only in the `else:
os.environ.pop(...)` arm of the second. Neither block changes any printed value; the pair
can become one helper `with tmpdir_env(value):`. Behaviour-neutral, so it is a dedup rather
than a dead-code deletion; I flag it separately for that reason.

**E4 — pre-existing pyflakes dead locals (out of this round).** 318 `paths`, 750 `repo`;
both predate the added block (§3). Not this round's weight; delete only if the lane is
sweeping the file anyway.

### 4.6 `.ufo/waves/round-45/write-scope-run.py` @ `e5c81594a3e2` (504 lines)

This script has **no `--selftest`** (`python3 write-scope-run.py --selftest` → argparse
`unrecognized arguments`, rc=2), so its only exercise is the receipt's real runs. Its three
receipted invocations are `.ufo/waves/round-45/evidence/write-scope.txt` lines 57
(`--rev HEAD`), 230 (`--work`) and 388–389 (`--repo … --rev HEAD --fixture …`).

**F1 — `--keep` (406) and its branch. DEL.**
```python
    ap.add_argument("--keep", action="store_true")   # 406
…
        if args.keep: print("sandbox_kept=%s" % runroot)   # finally block
```
No receipt passes `--keep`; the branch's only effect is not deleting the sandbox. It is the
sole print path that is unreachable from every recorded run.
**F2 — `--only` (407) and its filter. DEL.** No receipt passes it; the filter at
`selected = [e for e in entries if not args.only or e["id"] in args.only]` reduces to
`entries` on every recorded run.
**F3 — `--timeout` (405) and `_find`'s `timeout` parameter (130). DEL.**
`_find(root, args, timeout=600)` has 3/3 call sites omitting the argument, and the CLI flag
that would feed it is passed by no receipt (all runs use the 900 s default). Deleting the
flag collapses `run_one(…, args.timeout, …)` to the same 900 s constant.
Corner for F1–F3: these are the only knobs that make an ad-hoc debugging run possible. The
prompt did not ask for them and no receipt exercises them; if the integrator wants a
debuggable runner, keep `--keep` and say so in the SKILL row instead.

**KEEP (proved exercised, cannot be deleted)**: `--rev` **and** `--work` — receipts use both
(57 uses `--rev HEAD`, 230 uses `--work`), even though they are two spellings of one input
(`rev = "WORK" if args.work else args.rev` silently ignores `--rev` when both are given).
That silent-ignore is a defect to note, not a deletion: both spellings are receipted.

### 4.7 The wave's fixture scripts / data

**G1 — all four mutants are now clean one-site diffs against their live instruments.**
`diff -u` against the live instrument:
```
count-c1.py:          2 changed lines  (-  if fid in ids:  /  +  if False:  # MUTANT: duplicate-id check disabled)
count-c2.py:          2 changed lines  (-  record("writescope_mismatch", ws["mismatch"] == 0, …  /  +  record("writescope_mismatch", True, … (check disabled))
count-c3.py:          2 changed lines  (-  record("census_ok", …, proc.returncode == 0,  /  +  record("census_ok", "census", True,)
mori-gate-registry.py:1 changed line   (+  break  # MUTANT: read only the FIRST registry table)
```
Each turns exactly one arm red in its own instrument: the c1 mutant runs `C1_SELFTEST
pass=15 fail=1`, the c2 mutant `C2_SELFTEST pass=9 fail=1`. (The c1 mutant was stale — a
mutant of the sealed 819-line counter — until the executor regenerated it against the
1172-line counter; now the pair is coherent again and §2.1's staleness point narrows to the
manifest pin itself.)

**G2 — stray build artifact inside a fixture directory. DEL (hygiene).**
`.ufo/waves/round-45/fixtures/mutants/__pycache__/mori-gate-registry.cpython-314.pyc`
(41562 bytes, 07:48) is a Python bytecode cache sitting in the mutants fixture directory;
it is not a mutant, is not read by anything, and will be copied by any tree materialisation
that ignores only `.git`. Delete the `__pycache__` directory. (The instrument that produced
it imports/execs the mutant; the fix is to run mutants with `PYTHONDONTWRITEBYTECODE=1`, not
to keep the artifact.)

`fixtures/witnesses/*.tsv` and `fixtures/write-scope.json` are data the arms read; no dead
weight found (the three witness ledgers are each consumed by `check_witnesses`, which fails
if any is *accepted*).

### 4.8 The two remaining added `--selftest` branches

`tools/mori-routed-check.py` @ `b5498a54ceeb`: the added block is **wired** (`--selftest`
dispatches; `ROUTED_CHECK_SELFTEST pass=20 fail=0` rc=0) and the AST call-site scan found no
never-supplied parameter in the added functions. 127 missed lines are `main` (1006–1067) and
its refusal paths plus the row checks' failure arms. Nothing to delete; the unarmed failure
arms are MutCounters' territory. (`--round` is used, via `dest="round_number"`.)

`tools/mori-silence-cases.sh` @ `ff8b69757dea`: bash — no coverage instrument exists here,
so I make **no coverage claim**. What I can state by reading and running: the argv branch is
real (`--selftest) SELFTEST=1; shift` at 189, `--selftest takes no census path` at 193,
`MORI_SILENCE_CASES_SELFTEST pass=24 fail=0` rc=0), `bash -n` is clean, and the self re-exec
at 257–258 (`exec bash "$SELF" --selftest`) is live (it fires only when the entropy pins are
exported, which is why it is not dead). No deletion proposed for this file.

## 5. Proposed deletions I could NOT prove dead

1. **gr `mask_python` (256–277) / `escape_branch` Python arm (342).** Unarmed by the
   selftest, but the real population contains `.py` tools; deleting would silently stop
   testing their self-test flag detection. **ARM, not DEL.**
2. **c1 `resolve()` (123–132).** Zero coverage, but it is the only revision resolver in the
   file and `--other-rev` depends on it. **ARM.**
3. **c2's `WORK` branches** (`read_at` 113–123, `population` 135–139, `_work_ignore` 173–189,
   `materialize_tree` 195–207). Unarmed, but `main` explicitly accepts `WORK` (927) and a
   reviewer can call it; I cannot show the branch is unreachable. **ARM.**
4. **c3 `dedupe` (647) / `relative_entry` (655).** Main-only; `main` is untested, not dead.
   **ARM.**
5. **r19 tips half (1202–1204).** `expected_tips` holds the same values as the claims today,
   so it cannot fail *now*, but it is an independently written dict, so it would catch a
   future edit that changes one without the other. I can only prove the `base` half (E1)
   tautological. **KEEP.**
6. **wsr `--rev`/`--work` (401–402).** Both are receipted (§4.6); deleting either edits a
   recorded run. **KEEP.**
7. **c1's `-1` sentinel in `parse_ledger`.** Unobservable, but the guard prevents a
   `ValueError` on a malformed ledger. **KEEP.**
8. **r19's two pyflakes locals (318, 750).** Real dead assignments, but pre-existing, i.e.
   outside "the round's new code". Their deletion is safe; I record them rather than claim
   them.

## 6. Duplication that must NOT be collapsed (the isolation rule still binds)

The counters are run **as single files copied alone into a temp dir** by
`count-c2.py`'s `materialize_tree`/`auditor_arm`, so a shared module would break C2's own
green arm — the round-44 argument (`round-44/w1/SimpCounters.md` §4.2) still holds and was
not re-litigated. Confirmed duplication left in place:

- `child_env()` (c1 98–110, strips every `GIT_*`) vs `git_env()` (c3 75–76, strips an
  explicit five-key tuple) vs gr's `git` (no scrub in the wrapper) — same intent, three
  behaviours; unifying is a design call, not a deletion.
- `repo_default()` in four shapes (c1 83–95 walks up; c2 78–92; c3 77–89; gr 90–101 one-line
  `dirname(dirname(abspath))`); only gr's variant can differ, and only when `--repo` is
  omitted — `main` is untested in all four, so no arm can prove any of them right.
- the eight-cell markdown table parser exists three times: gr `parse_tables`
  (214–231)/`split_row` (196–203), c2's `_registry` fixture builder, and wsr's
  `parse_gate_rows`+`FIELDS`/`HEADER_CELLS`.
- the sandbox-copy+digest pair: c2 `materialize_tree`/`tree_digest` (191–230) and wsr
  `copy_rev`/`digest_files` (~84–125) do the same job for two different claims.

## 7. What the integrator should take from this

- **One integrity finding before anything else (§2.1)**: `sha256sum -c
  evidence/freeze-r45.txt` exits 1 — `.ufo/waves/round-45/count-c1.py` is `5f2deea0b35c`
  (1172 lines) while the manifest pins `bbe90ce4…`; and the manifest's `(external)
  …/scripts/sources-census.sh` entry cannot be read on this host. The c1 mutant has been
  regenerated against the live counter, so the after-measurement's remaining blocker is the
  manifest pin itself, not the mutant pair.
- 18 **DEL** groups with proofs (A1–A3, B1–B5, C1, C2, D1, D2, E1, E3, F1–F3, G2),
  ≈70 lines net, none of which changes a selftest tally or a printed verdict line except
  A3's non-git-repo corner and B5's accepted-input language.
- 8 **ARM** items where the next deletion would harm the instrument, not help it — chief
  among them gr's `mask_python`/Python escape path, which is the auditor's largest untested
  surface and the exact shape of the r44 false positive.
- one **mutant** note: all four mutants are now clean one-site diffs that each turn exactly
  one selftest arm red (G1) — nothing to route.
- an observation, not a verdict: at 07:52 `count-c2.py` and `count-c3.py` were **red**
  (`C2_SELFTEST pass=7 fail=1`, `C3_SELFTEST pass=2 fail=14`, the latter a
  `TypeError: evaluate() missing 1 required positional argument`). Both were green at
  07:53:41 (`pass=10 fail=0` @ `aeec57ad`, `pass=19 fail=0` @ `37fd7c24`). That window is a
  mid-write state, recorded because I measured it; it is not a claim about the final bytes.
