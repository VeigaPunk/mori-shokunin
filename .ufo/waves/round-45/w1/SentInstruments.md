# SentInstruments — trust-boundary review of round 45's new instruments

Role: sentinel (leaf). Scope: the four instruments named by the item plus the
`--selftest` branches they gained this wave. Read-only: **no instrument was
edited**. All probes ran against throwaway repos under
`.ufo/waves/round-45/tmp/SentInstruments/`.

## Bytes reviewed (last observed 08:07; see churn note)

| instrument | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-45/count-c1.py` | 49989 | `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` |
| `.ufo/waves/round-45/count-c2.py` | 41633 | `e8ee29eb885270b0aa056617ab1c44fd8663c0b7e680506976bbcd5156959c64` |
| `.ufo/waves/round-45/count-c3.py` | 30465 | `37fd7c24ff52d6aa27f718ef0b0a2f2e4affa7a1cd0ab67c1fa05f028854a98e` |
| `tools/mori-gate-registry.py` (v2) | 31165 | `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` |
| `.ufo/waves/round-45/fixtures/write-scope.json` | 7169 | `2af692da8ec5a25f23c40a3a0b73c12335e880d32dbf22eed89ea276a5b8d753` |
| `.ufo/waves/round-45/write-scope-run.py` (helper) | 19510 | `66475629944f201e0bb6e58541f7e7241691feb88302d0892b2aa58f89511b5c` |

### Churn note (read this before acting on the table)

The instruments were rewritten continuously while I reviewed them: I observed
**ten distinct `count-c2.py` hashes** between 07:44 and 08:00, and `count-c1.py`
was still changing at 08:04:46 (five revisions after I first read it). c3, the
registry, the fixture and the helper were stable from 07:53 onward.

Because of that, line numbers are **not** cited for c1 (they shifted on every
revision); its claims are pinned to the parse-result strings and the behaviour
probe below, which I re-ran on `bbe90ce`, `a564dcc3`, `a784b68a`, `38ce7a2b`
and `5f2deea0` with identical results.

Every *open* finding below was re-proven against the hashes in this table
(H1/H2/H3 at 08:01 on `e8ee29eb`; M2/M3/M4/M5 and the registry regressions at
07:57-08:00). The one finding that was **closed by a later revision** (M1) is
kept with its status stated, because "this was open at 07:48" is itself the
evidence that the class is reachable.

If any of the four instruments changed after the hashes above, re-run these
before quoting the corresponding row:

```
# H1 / H2 / H3 (c2)
MORI_GATE_REGISTRY=/abs/stub.py python3 count-c2.py HEAD --repo <A>   # stub output adopted?
GIT_DIR=<B>/.git   python3 count-c2.py HEAD --repo <A>               # rev= should be A's tip
python3 count-c2.py HEAD --repo <A> --mutants-dir /abs               # outside file executed?

# M1 (c1) — the parser probe; expect REJECTED / ACCEPTED / REJECTED
python3 -c 'import importlib.util as u; s=u.spec_from_file_location("c","<repo>/.ufo/waves/round-45/count-c1.py"); m=u.module_from_spec(s); s.loader.exec_module(m); print([m.parse_ledger(x)[1] for x in ("F01\t3\tregistry\tgit show @REV@:d | bash","F01\t3\tregistry\tgit show @REV@:d | grep -c x","F01\t3\tregistry\tgit show @REV@:d | sort -o /home/x/W")])'

# M2 (c3) — census from disk
bash <root>/scripts/sources-census.sh validate --root <root> mori   # replaced by a stub: marker?
```

`write-scope-run.py` is not in my named list but is the helper `count-c2.py`'s
arm is built from, so it is covered where relevant.

## Findings

Severity is about **evidence integrity**, i.e. whether a receipt printed by the
instrument can be true of something other than the committed bytes at `--rev`.
| # | Sev | One-line finding | Proof (command → observed) |
|---|---|---|---|
| H1 | HIGH | `count-c2.py` executes a program named by inherited `MORI_GATE_REGISTRY`, and that program's output *is* the C2 measurement | `MORI_GATE_REGISTRY=/abs/stub.py python3 count-c2.py HEAD --repo p2` → `auditor /abs/stub.py sha256=4e4c4138973b`, `auditor_selftest PASS`, `mode=population population_digest=deadbeef`, verdict line `rev=b6fc8ef…`; stub's marker file created |
| H2 | HIGH | `count-c2.py`'s `--repo` is advisory: an inherited `GIT_DIR` retargets the measurement | `GIT_DIR=B/.git python3 count-c2.py HEAD --repo A` → `rev=e39bcd0…` (**B**) while `git -C A rev-parse HEAD` (unscrubbed) = `e39bcd0…` and plain c2 = `f43310a…` (**A**) |
| H3 | HIGH | `count-c2.py`'s mutant — the kill-rule evidence — always comes from the working tree, never from `--rev`, and `--mutants-dir` may point anywhere | `mutant_bytes("/nonexistent/repo", "0"*40, abs_dir, "probe.py")` → `b"print('WORKTREE BYTES, no revision consulted')\n"`; `--mutants-dir /abs` → `mutant_kill PASS (count-c2.py pass=1 fail=1)` + marker written outside the repo |
| M1 | MED → **closed 08:00** (re-verified at `5f2deea0`) | On `f80e75ac` (07:47) `count-c1.py` executed uncommitted witness ledgers whose filter stage could write a file (`sort -o`); the 08:00 revision (`bbe90ce`) rejects `-o`, absolute paths and filter file operands, so the primitive is gone | on `f80e75ac`: witness row `git show @REV@:data/p.txt \| sort -o /abs/WROTE` → `rejected` **and** `WROTE` created (6 bytes). On `bbe90ce`: `parse_ledger` → `REJECTED ["sort option '-o' is forbidden (writer/redirect option)", "absolute path '/home/x/WROTE'", "'sort' takes 0..0 positional argument(s)"]`; the same run leaves `WROTE` absent |
| M2 | MED | `count-c3.py` executes the census script from the worktree; its sha256 is printed but never compared to anything, so any census yields `C3=met` | census `touch MARK; printf 'mori\tok\n'; exit 0` at `<root>/scripts/sources-census.sh` → `census_ok PASS (exit=0)`, `C3=met … census_sha256=c3ae3da8…`, marker created |
| M3 | MED | In WORK mode `count-c3.py` reads `--entry`/`--readme` and `count-c2.py` reads `--mutants-dir`/`--write-scope` through `os.path.join(repo, path)` with no containment check; absolute and `..` paths escape | `count-c3.py WORK --entry /abs/entry.md …` → `entry_present /home/…/entry.md PASS (90 bytes)`; same with `--entry ../outside/entry.md` → `PASS (90 bytes)` |
| M4 | MED | The write-scope arm cannot see writes outside its sandbox root, so `writes_outside_tmpdir=0` does **not** mean "writes only under TMPDIR" | fixture entry writing `/tmp/omp-sentinel-ws-probe2` → `writescope tools/real.sh match rc=0 … writes_outside_tmpdir=0 declared='stdout only'`, `writescope_mismatch PASS`, and the `/tmp` file exists |
| M5 | MED (latent) | `tools/mori-gate-registry.py` still accepts a *mention* of `--selftest` in a `.sh` tool as "a real argv branch" (P-C2 item 4); no live tool relies on it | `tools/help.sh` = `case "${1-}" in --help) echo "usage: $0 $@ --selftest"; exit 2 ;; esac` → `PASS row='help' (8 cells, entry resolves, --selftest argv branch)`, `REGISTRY=met`; `bash tools/help.sh --selftest` prints `TOOL=met`, exit 0 |
| L1 | LOW | Every `subprocess.run` has a timeout, but none of the four kills the process group, so a timeout leaves detached children | probe: `subprocess.run([...], timeout=2)` → `TimeoutExpired`; `direct child … alive=False \| grandchild … alive=True`; only `write-scope-run.py` sets `start_new_session=True` (l.272) + `os.killpg` (l.279) |
| L2 | LOW | Absolute operator paths reach stdout and land in committed artifacts (item 7) | `audit /home/…/evil.sh FAIL (audited path is absolute or outside the repo)`; `REGISTRY_SETUP registry path '/home/…' is not repo-relative`; c1 `rev=… repo=/home/…`; c2 `… repo=/home/…`; c3 `repo=/home/… root=/home/… census_arm=bash /home/…`; committed r44 receipt `census-end.txt:2` already carries `/home/vgpnk/…`; new fixture `write-scope.json:10` carries `"repo": "/home/vgpnk/Projects/shokunin/mori-shokunin"` |
| L3 | LOW | `count-c3.py` scrubs a fixed 7-key `GIT_*` list while c1 and the registry strip every `GIT_*` prefix; `GIT_CONFIG_*` survives into c3's git children | `GIT_ENV_KEYS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR", …)` `GIT_ENV_KEYS` (c3, fixed list) vs `child_env()` in c1 and the registry (`not k.startswith("GIT_")`). No read-retargeting exploit found for the verbs c3 uses |
| L4 | LOW | c2/c3/registry fall back to `/tmp` when `TMPDIR` is unset or names a non-existent directory, and a failed `mkdtemp`/`materialize_tree` escapes as an unhandled `OSError` (exit 1, **no verdict line**) instead of `*_SETUP` (exit 2); only c1 creates and honours its `TMPDIR` | `TMPDIR=<absent dir> python3 count-c2.py WORK --repo <lane>` → `OSError: [Errno 28] No space left on device: '/tmp/c2-25w93cgo/ws-01'`, stdout 0 bytes. c2/c3/registry call plain `tempfile.mkdtemp(prefix=…)`; c1's `_tmpdir()` is `base = os.environ.get("TMPDIR") or tempfile.gettempdir(); os.makedirs(base, exist_ok=True)` |

### H1 detail — the environment can supply the whole C2 measurement

`count-c2.py:959`:

```python
auditor = args.auditor or os.environ.get("MORI_GATE_REGISTRY")
```

The value is read with `os.path.isfile` from disk, copied to a temp path and
executed (`run([sys.executable, mat, "--rev", rev, "--repo", repo, "--audit-all"], …)`).
Nothing distinguishes a fixture stub from the committed auditor: the receipt
prints `auditor <path> sha256=…` (a *path*, not "this is the committed bytes")
and then adopts whatever counters and `mode=`/`population_digest=` the program
prints. P-C2 requires "one run over the committed bytes at `--rev`"; with one
inherited variable the committed bytes are never read.

Observed:

```
$ MORI_GATE_REGISTRY=$T/audstub/stub.py python3 count-c2.py HEAD --repo p2
auditor /home/vgpnk/…/audstub/stub.py sha256=4e4c4138973b
check auditor_selftest     PASS (pass=1 fail=0)
C2=unmet tables=1 registered=1 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0
        writescope_mismatch=0 mode=population population_digest=deadbeef
        population_members=1 auditor_selftest=pass=1/fail=0 …
marker after: -rw-r--r-- … audstub/MARK
```

Smallest remediation: accept the env var only in an explicit fixture mode
(e.g. honour it only when `--selftest` or a new `--auditor-source=fixture` is
given), and print `auditor_source=env|argv|revision` on every run with the
instrument's *resolved* sha256 pinned to the revision when the source is
`revision`.

### H2 detail — `--repo` is not authoritative

`run()` (c2 l.100) passes `env=None` unless the caller supplies one, and `git()`
never supplies one, so every git child inherits the ambient environment —
c1 (`child_env()`), the registry (`child_env()`) and c3 (`git_env()`) all
supply one. Observed, same pair of repos (A tip `f43310a…`, B tip `e39bcd0…`):

```
$ python3 count-c2.py HEAD --repo A                     → rev=f43310a3edfa2ea7d1ed5b887faff7a5c9e8af10
$ GIT_DIR=B/.git python3 count-c2.py HEAD --repo A      → rev=e39bcd088f5a4c94eb3e8de05e8f1ca36f64630d
$ GIT_DIR=B/.git git -C A rev-parse HEAD               → e39bcd088f5a4c94eb3e8de05e8f1ca36f64630d
```

The verdict line then reads `rev=<B> repo=<A path>`: a receipt that names one
repository and measures another. Both repos are ordinary git checkouts with the same
fixture shape, so the only variable is the environment.

Control (same attack, other instruments): `GIT_DIR=B/.git … mori-gate-registry.py
--rev HEAD --repo A` printed `rev=f43310a…` (A) — scrub works; c1 likewise
printed A's tip under `GIT_DIR=B/.git`.

Smallest remediation: give `count-c2.py` the same `child_env()` the other two
carry (`{k: v for k, v in os.environ.items() if not k.startswith("GIT_")}`)
and use it for `git()` and for the auditor/mutant/write-scope children.

### H3 detail — the mutant is never the committed mutant

`count-c2.py:960-962` makes the directory absolute before use:

```python
mutants = args.mutants_dir
if not os.path.isabs(mutants):
    mutants = os.path.join(repo, mutants)
```

so `mutant_bytes` (l.487) always takes the `os.path.isabs` branch (l.490) — the
`read_at(repo, rev, …)` fallback immediately below is dead for every CLI run:

```python
def mutant_bytes(repo, rev, mutants_dir, name):
    if not name:
        return None
    if os.path.isabs(mutants_dir):
        full = os.path.join(mutants_dir, name)
        if not os.path.isfile(full):
            return None
        with open(full, "rb") as fh:
            return fh.read()
    return read_at(repo, rev, mutants_dir.rstrip("/") + "/" + name)
```

The bytes are then written to `<tmp>/mutant-<name>`, `chmod 0755`, and run as
`[sys.executable, mfile, "--selftest"]`. With `--rev` a real commit and the
mutant absent from that commit, the run still reports `mutant=killed`:

```
$ python3 count-c2.py HEAD --repo p2 --mutants-dir $T/mutabs
check mutant_present       PASS (/home/…/mutabs/count-c2.py)
check mutant_kill          PASS (count-c2.py pass=1 fail=1)
marker after: -rw-r--r-- … mutabs/MARK      # written by the outside file
```

Two consequences: (a) the kill-rule evidence is worktree state at any `--rev`;
(b) `--mutants-dir` is an execution entry point for a file outside the repo.
Smallest remediation: resolve the mutant with `read_at(repo, rev, rel_path)`
only (materialise the bytes at `rev`), and reject a `mutants-dir` that is not a
repo-relative path.

### M1 detail — the witness write channel (open at 07:47, closed at 08:00)

`check_witnesses()` opens each `*.tsv` with `open(path, "rb")` and
feeds its text to `check_text` → `run_pipeline`. That is intrinsic to the
predicate (witnesses must be *rejected*, so they must be evaluated), but on
`f80e75ac` the execution was not sandboxed and the filter allowlist (l.66)
includes `sort`, whose `-o FILE` writes anywhere:

```
$ cat witness/w1.tsv
F01	3	registry	git show @REV@:data/p.txt | sort -o /home/…/wtest/WROTE
$ python3 count-c1.py $REV --other-rev $OTHER --repo repo --witness-dir witness   # f80e75ac
witness w1.tsv                   rejected (row_floor,class_floor,commands_reconcile)
marker after: -rw-r--r-- … WROTE        # 6 bytes, written by a rejected witness
```

The 08:00 revision (`bbe90ce`) closes it at parse time — `parse_ledger` now
rejects the writer option, the absolute path and the file operand:

```
sort -o abs -> REJECTED ["row 1: sort option '-o' is forbidden (writer/redirect option)",
                          "row 1: absolute path '/home/x/WROTE'",
                          "row 1: 'sort' takes 0..0 positional argument(s), got 1: …"]
sort plain  -> ACCEPTED stages=[['git','show','@REV@:data/p.txt'], ['sort']]
nl abs      -> REJECTED ["absolute path '/home/x/f'", "'nl' takes 0..0 positional argument(s)"]
```

Re-running the same witness on `bbe90ce` leaves `WROTE` absent. What remains is
the weaker property that witness ledgers are still read from disk, i.e.
uncommitted input can still steer *which* committed bytes are read (and can
still choose `grep` patterns), but it can no longer write. Running witness
pipelines with `cwd=` a scratch dir would close the residual read-side coupling;
no action is warranted for the write side on the bytes cited here.

### M2 detail — the census digest is decorative

`count-c3.py:704` defaults the census to `<root>/scripts/sources-census.sh`,
`l.300` hashes the file, `l.302` runs it with `bash`. Nothing compares the
digest to a pinned value and nothing reads the script at `--rev`, so the arm's
green is only as good as whatever file is on disk at that path. Observed with a
census that only touches a marker and prints `mori<TAB>ok`:

```
check census_ok       census PASS (exit=0)
census_arm=bash /home/…/c3z/fleet/scripts/sources-census.sh validate --root /home/…/c3z/fleet mori
C3=met rev=c53aee8… entering=5ab7c11… entries=1 rows=S900 census_sha256=c3ae3da8…
marker after: -rw-r--r-- … c3z/CENSUS_RAN
```

P-C3 item 5 ("pinned by digest in the run's stdout") is satisfied literally;
the risk is that `C3=met` can be produced by an uncommitted script, and that a
TOCTOU window exists between the hash and the `bash` read. Smallest
remediation: require `--census-sha256 <expected>` (or read the census from
`rev` when the lane carries it) and compare before running.

### M3 detail — WORK-mode escapes survive in c2 and c3 (v2 registry closed them)

c3 `read_at()`/`exists_at()` and c2 `read_at()` (l.118-120) join the operator path
onto `repo` without a containment check. Observed:

```
$ python3 count-c3.py WORK --entering-rev $REV --repo p3/repo --root p3 \
      --entry /home/…/p3/outside/entry.md --row S900 --census /bin/true
check entry_present   /home/…/p3/outside/entry.md PASS (90 bytes)
check entry_present   ../outside/entry.md PASS (90 bytes)      # same file, '..' form
```

The registry v2 rejects exactly these shapes (`safe_relpath` l.118 + `inside_repo` l.131 in
`tools/mori-gate-registry.py`), and I confirmed it at WORK and at a
revision for `--registry`, `--audit` and a committed symlink:

```
audit /home/…/outside/evil.sh FAIL (audited path is absolute or outside the repo)
REGISTRY_SETUP registry path '/home/…/outside/SKILL.md' is not repo-relative
audit tools/link.sh FAIL row='evil' (row 'evil' entry path tools/link.sh does not resolve at WORK)
```

(For completeness: v1 of the same tool *did* accept all three —
`REGISTRY=met` from `/abs/SKILL.md`, from `../outside/SKILL.md`, and from a
repo symlink pointing outside. That regression is closed.)

### M4 detail — the write-scope metric measures the wrong boundary

`count-c2.py:410`:

```python
obs["outside"] = (len(changed) + len(tree_digest(home))
                  + len(set(os.listdir(root)) - {"repo", "tmp", "home"}))
```

`changed` are files **inside** the sandbox copy, so a repo write is counted
twice (once as `repo_changed`, once as `outside`), and nothing outside the
sandbox root is inspected at all. A fixture entry whose command writes
`/tmp/…`, `/home/<user>/…` or the real lane is scored `writes_outside_tmpdir=0`
and `writescope_mismatch` stays 0:

```
writescope tools/real.sh match rc=0 repo_unchanged=yes writes_outside_tmpdir=0 declared='stdout only'
check writescope_mismatch  PASS (mismatch=0)
marker after: -rw-r--r-- 1 vgpnk vgpnk 1 … /tmp/omp-sentinel-ws-probe2
```

This directly underwrites P-C2 item 6 ("the audited write-scope cells make no
false claim"): the arm certifies a claim it did not test. Smallest remediation:
either state the metric as "writes into the copied tree / redirected HOME"
(exactly what is measured) and stop calling it `writes_outside_tmpdir`, or
observe the run under a mount/pid namespace (the repo already depends on
nothing exotic) so absolute writes are visible.

### M5 detail — a mention still counts as a branch, for `.sh`

`selftest_flag` (registry l.304-321) now has a strict limb and a heuristic limb:

```python
if re.search(r"^\s*(?:[^\s|()]+\|)*" + re.escape(flag) + r"\s*[|)]", line):
    return True
if SH_ARGV.search(" ".join(lines[max(0, i - 2):i + 1])):
    return True
```

The Python path was hardened this wave (`_flag_in_python_tests`: a parser key,
a comparison, or a membership test) and my earlier Python repro now correctly
fails. The shell heuristic has no such requirement: any line carrying the flag
within two lines of `"$@"`, `$*`, `$#`, `$N`, `case` or `shift` is accepted.
A `--help` branch that merely prints usage therefore passes as a "real argv
branch", which is precisely the r44 silence-oracle class moved from comments to
strings:

```
$ python3 mori-gate-registry.py --rev WORK --repo p6/repo --registry SKILL.md --audit tools/help.sh
audit tools/help.sh      PASS row='help' (8 cells, entry resolves, --selftest argv branch)
REGISTRY=met
$ bash p6/repo/tools/help.sh --selftest     →  TOOL=met   (no self-test ran)
```

Latent today: all four `.sh` tools in the declared population carry a real
branch (`mori-census.sh:4721` `--selftest) selftest=1; shift ;;`,
`mori-silence-cases.sh:189`, `mori-blind-check.sh:359`, `mori-index-clean.sh:218`),
and `--audit-all` at WORK prints `no_selftest=0`. Smallest remediation: require,
for `.sh`, the same grammar as the strict limb — the flag followed by `)` or `|`
as a branch target — and treat the `SH_ARGV` window only as a tie-breaker that
must also see the flag as a comparison (`[ "$1" = --selftest ]`,
`[[ $1 == --selftest ]]`, `case … --selftest)`).

### L4 detail — `/tmp` fallback turns a setup failure into a traceback

Python's `tempfile` silently falls back through its candidate list when `TMPDIR`
is missing or unusable; only c1 pins the directory. Observed while running the
end-to-end arm without creating the `TMPDIR` directory first (a transiently
full `/tmp`: the partition held 114 GB at the time):

```
$ TMPDIR=$T/wsreal2 python3 count-c2.py WORK --repo <lane>     # $T/wsreal2 did not exist
Traceback (most recent call last):
  …
OSError: [Errno 28] No space left on device: '/tmp/c2-25w93cgo/ws-01'
stdout: 0 bytes
```

Two things are wrong with that, independent of my setup mistake: the counter
wrote its whole sandbox into `/tmp` (the operator's round rules forbid `/tmp`
because it filled mid-round on 2026-10-24), and the failure produced exit 1 with
no `C2_SETUP` line — a receipt that is a traceback. The contract's exit map
reserves 2 for "could-not-evaluate". The same run with the directory created
finished in 6.6 s (see below), so this is purely the fallback/pathing gap.
Smallest remediation: `base = os.environ.get("TMPDIR") or <lane>/.scratch`;
`os.makedirs(base, exist_ok=True)`; `mkdtemp(dir=base)`; wrap `mkdtemp` and
`materialize_tree` in `except OSError → Setup`.

## Answers to the seven checks

**(1) `shell=True`, `os.system`, `eval`, `exec`, `pickle`, `yaml.load` — none.**
```
$ grep -nE "shell=True|os\.system|os\.popen|\beval\(|\bexec\(|pickle|yaml\.|__import__|runpy|pty\.spawn|import_module" \
    count-c1.py count-c2.py count-c3.py mori-gate-registry.py
none found
```
The r44 `bash -c` pipeline is gone: c1 parses the ledger into argv stages
(`split_stages`, quote-aware, rejects `; $ ` < > & ( ) \n \r`) and validates
every stage against `GIT_VERBS`/`FILTERS`. Replaying the r44 injection ledger
(`… | bash`) against r45 c1 now yields
`rows_parse FAIL (row 1: pipeline stage 'bash' is not a read filter)` and the
payload marker is **not** created (r44 bytes created it).

**(2) Timeouts — every `subprocess.run` has one; none kills a process group.**
| site | timeout |
|---|---|
| c1 `git()` | `timeout=timeout` (arg, default 20) |
| c1 `run_pipeline()` per stage | `timeout=left` (remaining budget) |
| c1 fixture `_git()` | `timeout=60` |
| c2 `run()` | `timeout=timeout` (default 120) |
| c2 `git archive` in `materialize_tree()` | `timeout=120` |
| c2 `sandbox_run()` child | `timeout=timeout` |
| c3 `git()` | `timeout=timeout` (default 120) |
| c3 census arm | `timeout=timeout` |
| c3 fixture `_git()` | `timeout=60` |
| registry `git()` | `timeout=timeout` (default 30) |
| c2 fixture-auditor stub's own `git ls-tree` (inside the stub string) | **none** — bounded only by the outer `run(..., timeout)` that invokes the stub |

No `start_new_session`, no `killpg`, no `setsid` in any of the four; only
`write-scope-run.py` uses `start_new_session=True` (l.272) and
`os.killpg(os.getpgid(proc.pid), signal.SIGKILL)` (l.279). Probe with the exact
call shape (`subprocess.run([sys.executable, "spawner2.py"], …, timeout=2)`):

```
TimeoutExpired
direct child 1626220 alive=False | grandchild 1626328 alive=True
```

A timed-out instrument therefore leaves detached `git`/`grep`/`sed` children
running after the counter returns `*_SETUP` — relevant because the counters run
under a wall-clock budget in a shared fleet.

**(3) `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` — c1 ✔, registry ✔, c3 partial, c2 ✘.**
- c1 `child_env()`: strips every `GIT_*`, sets `GIT_CONFIG_NOSYSTEM=1`,
  `GIT_CONFIG_GLOBAL=/dev/null`, `LC_ALL=LANG=C`. Proven: under `GIT_DIR=B`,
  `--repo A` still prints A's tip (`rev=f43310a…`) while raw git prints B's.
- registry `child_env()`: strips every `GIT_*`, sets
  `GIT_TERMINAL_PROMPT=0`. Proven identically (`rev=f43310a…` vs raw `e39bcd0…`).
- c3 `git_env()`: strips a fixed 7-key list; `GIT_DIR` is in it, so
  `--repo` stays authoritative for read retargeting, but `GIT_CONFIG_GLOBAL`,
  `GIT_CONFIG_COUNT/KEY_*/VALUE_*`, `GIT_CONFIG_SYSTEM` survive (L3). I found no
  read-retargeting exploit through them for `rev-parse`/`cat-file`/`show`.
- c2: no scrub at all → H2.

**(4) Path escapes — registry v2 closed the class; c2/c3 WORK mode did not.**
| surface | at a revision | in WORK |
|---|---|---|
| registry `--registry` | rejected (`not repo-relative`) | rejected |
| registry `--audit` | FAIL `absolute or outside the repo` | FAIL same |
| registry entry cell (committed symlink) | FAIL `does not resolve at …` | FAIL same |
| c1 `--ledger` | git-relative, no escape (WORK refused outright) | n/a |
| c1 `--witness-dir` | **absolute by design; reads (and executes) disk ledgers**; the file-write channel was closed at 08:00, the uncommitted read remains (M1) | n/a |
| c2 `--mutants-dir` | **absolute/`..` accepted, executed** (H3) | same |
| c2 `--write-scope` | absolute accepted (l.417) | same |
| c3 `--entry`/`--readme` | git-relative | **absolute and `..` escape** (M3) |
| c3 `--census` | any path, executed (M2) | same |

**(5) Uncommitted program execution — c2 and c3 execute worktree bytes; c1 executes uncommitted ledger text; the registry executes nothing.**
- c2: auditor (`MORI_GATE_REGISTRY`/`--auditor`, H1), mutant (always worktree, H3),
  write-scope fixture argv (l.417 → `shlex.split` when a string → `run` with
  `cwd=sand`; earlier proven with a `/tmp` write, M4).
- c3: census script from disk, digest printed but unverified (M2).
- c1: witness ledgers from disk, no sandbox; the `sort -o` write primitive was
  observable at 07:47 and is rejected at 08:00 (M1). The uncommitted read remains.
- registry: text analysis of committed bytes only — it never executes the
  audited tool (the `--selftest` check is static). That is also why M5 has to be
  decided textually.

**(6) What each instrument writes, and where.** See the verdict table below:
all four `--selftest` runs are `rc=0`, leave the sandbox copy byte-identical,
leave the lane repo untouched (`git status --porcelain` diff empty), and remove
their own `mkdtemp` trees.

**(7) Absolute operator paths on stdout / in committed artifacts — yes, all four.**
```
registry: audit /home/…/outside/evil.sh FAIL (audited path is absolute or outside the repo)
registry: REGISTRY_SETUP registry path '/home/…/outside/SKILL.md' is not repo-relative
c1:       C1=met … rev=<sha> repo=/home/…/wtest/repo other_rev=<sha> witnesses=1/1
c2:       C2=… rev=<sha> repo=/home/…/path/p2/repo
c2:       check writescope_fixture PASS (/home/…/ws-probe2.json)
c3:       repo=/home/…  root=/home/…  census_arm=bash /home/…/sources-census.sh validate --root /home/… mori
```
This is already the committed convention: `.ufo/waves/round-44/evidence/census-end.txt:2`
is `# command: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`,
and the round's own new fixture carries one at `write-scope.json:10`
(`"repo": "/home/vgpnk/Projects/shokunin/mori-shokunin"`). If that fixture is
committed, item 6's evidence file itself leaks the operator path. Remediation is
either to print repo-relative paths (the absolute value adds nothing a receipt
needs — `rev` already identifies the measurement) or to state in the write-scope
fixture that the absolute `repo` field is deliberate and machine-specific.

## Write-scope verdict table (item 6)

Method: `tmp/SentInstruments/writescope.sh` copies a minimal skeleton (the four
instruments + `tools/` + `SKILL.md` + fixtures) into `tmp/SentInstruments/ws/<label>`,
snapshots sha256 of every file, runs the instrument's own `--selftest` with
`TMPDIR` and `HOME` inside the harness's scratch, re-snapshots, and diffs. The
lane repo is snapshotted with `git status --porcelain` before and after.

| instrument | `--selftest` rc | tally | sandbox tree diff | lane diff | writes under TMPDIR | observed outside sandbox | declared cell / fixture `expect` | verdict |
|---|---|---|---|---|---|---|---|---|
| `tools/mori-gate-registry.py` | 0 | `pass=15 fail=0` | none | none | `grst-*` created and removed | none attributable | "stdout only; … writes only under the caller TMPDIR" / `rc=0, repo_unchanged=yes, outside=0` | **MATCH** |
| `count-c1.py` | 0 | `pass=16 fail=0` | none | none | `c1st-*` created and removed | none attributable | see fixture r45 entry (`checkable:false`, `expect rc=0`) | **MATCH** |
| `count-c2.py` | 0 | `pass=10 fail=0` | none | none | `c2-*`, `c2st-*` created and removed | none attributable | `expect rc=0, repo_unchanged=yes, writes_outside_tmpdir=0` | **MATCH** |
| `count-c3.py` | 0 | `pass=19 fail=0` | none | none | `c3st-*` created and removed | none attributable | `expect rc=0, repo_unchanged=yes, writes_outside_tmpdir=0` | **MATCH** |

Caveats that belong with the table:
- "none attributable" is honest but weak: `/tmp` was concurrently used by
  sibling seats (`tameshi-r43-*`, `chousa-*` appeared and vanished mid-run), so
  the `/tmp` listing diff is noisy. The positive evidence is the sandbox and
  lane diffs plus code: all four use `tempfile.mkdtemp` (TMPDIR-honouring) and
  `shutil.rmtree` in `finally`; a grep for `open("…/tmp|/home…", "w")` finds
  nothing.
- With `TMPDIR` unset, all four fall back to `/tmp` and do write there (observed:
  `/tmp/c1st-7sbu1gs9` created and cleaned during a direct, TMPDIR-less
  `count-c1.py --selftest`). The table's "writes under TMPDIR" column is true of
  the harness runs, in which `TMPDIR` is set; it is not a property of the code
  under an unset `TMPDIR` (L4).
- The `writes_outside_tmpdir=0` column in the fixture is **not** a measurement
  of absolute writes (M4). The table above separates what I observed from what
  the fixture asserts, precisely because the arm's metric does not cover the
  boundary its name implies.
- The three r45 fixture entries are `checkable: false` with `row: null`, so
  nothing yet ties them to a committed `SKILL.md` write-scope cell. The arm runs
  them anyway; when the scribe lands the rows, the note in the fixture says the
  runner re-derives the cell. Until then `writescope_mismatch=0` says nothing
  about the r45 rows.

### The arm's own end-to-end verdict (for comparison)

`TMPDIR=<lane-scratch> python3 .ufo/waves/round-45/count-c2.py WORK --repo <lane>`
(6.6 s, exit 0) — the arm's own view of the same question:

```
writescope .ufo/waves/round-44/count-c1.py match rc=0 repo_unchanged=yes writes_outside_tmpdir=0 …
writescope .ufo/waves/round-44/count-c2.py match …
writescope .ufo/waves/round-44/count-c3.py match …
writescope tools/mori-gate-registry.py    match …
writescope .ufo/waves/round-45/count-c1.py SKIP (fixture marks it uncheckable)
writescope .ufo/waves/round-45/count-c2.py SKIP (fixture marks it uncheckable)
writescope .ufo/waves/round-45/count-c3.py SKIP (fixture marks it uncheckable)
check writescope_entries   PASS (checked=4 skipped=3)
check writescope_mismatch  PASS (mismatch=0)
C2=met tables=7 registered=39 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0
        writescope_mismatch=0 mode=population population_digest=2d1e9096… mutant=killed rev=WORK
```

So on the current fixture, three of the four instruments in my scope are
**skipped, not checked** by the arm; the four rows I ran independently (this
report's table) are the missing evidence. That is the honest reading of
`writescope_mismatch=0` at WORK today: it covers the r44 counters and the
registry, not the r45 counters. It also means the arm would report `PASS` for an
r45 counter that wrote the whole lane repo, until the fixture entries are made
checkable.

## Closed this wave (regressions I re-tested against r44 bytes and v1)

| r44/v1 defect | status on the bytes reviewed (c1 @ `5f2deea0`, c2 @ `e8ee29eb`, c3 @ `37fd7c24`, registry @ `8b82ac99`) |
|---|---|
| ledger text executed via `bash -c` (arbitrary shell) | **closed** — r44 replay rejected as `not a read filter`; payload not executed |
| c1 filter stages could write files (`sort -o FILE`, absolute-path filter operands) from uncommitted witness ledgers | **closed in `bbe90ce` (08:00), re-verified at `5f2deea0`** — `-o`/absolute paths/filter operands rejected at parse; it *was* open at 07:47 (`f80e75ac`), which is why this class stays on the list |
| `--registry`/`--audit` absolute, `..`, and symlink escapes (v1: `REGISTRY=met` from `/abs/SKILL.md`) | **closed** — `safe_relpath` + `inside_repo`; all three rejected at WORK and at a revision |
| `GIT_DIR` retargeting the audited repo (c1, registry) | **closed** — prefix scrub + proof |
| Python `--selftest` mention in a usage string counted as a branch | **closed** — `_flag_in_python_tests`; my earlier repro now FAILs |
| v1 registry could not see a second standard table | **closed** — `parse_tables` walks every table (`tables=7` on SKILL.md, `tables=2` fixture arm) |
| no process-group kill | **partially closed** — only in `write-scope-run.py` (L1) |

## Limits of this review

- I did not run the counters' *scoring* path end to end against the real fleet
  (that needs `--entering-rev`/`--root`/`--census` values the executors own);
  my c3 scoring probe used a synthetic fleet, which is enough to prove the
  census and entry channels.
- The instruments were being rewritten during the review; the hashes above are
  the ones reviewed (c1 was still moving at 08:04:46). If any instrument changed
  after those hashes, re-run the commands in the churn note before quoting the
  corresponding row.
- `write-scope-run.py` is outside my named scope; I noted only its
  process-group handling, which is the correct pattern the counters should copy.

## Tooling

No installs, no upgrades. `python3` (host), `git`, `sha256sum`, `pgrep`/`kill`
(probe cleanup) only. Scratch: `.ufo/waves/round-45/tmp/SentInstruments/`
(harness `writescope.sh`, probes, throwaway repos). Transient `/tmp` scratch
created by instrument runs (`/tmp/c2-…`, `/tmp/c1st-…`) was removed by the
instruments' own cleanup; nothing persists outside the scratch directory. No
instrument, SKILL.md, contract, or other seat's report was modified.
