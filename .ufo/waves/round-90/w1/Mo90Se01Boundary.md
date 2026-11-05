# Mo90Se01Boundary — adversarial boundary review, round 90

Lane `mori`. Read pin `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD`
→ `d1c8488986512a6a0475af88cc52779ce4703e00`. Contract declares entering
`037c02ca43a5ff36e23e449d0d6bcf50a1f2cbec` (verified by `git rev-parse`); the counter's own
`ENTERING` default is `30a29797012281b9fd0c748b38b929ac67f8c754` (also verified). Subjects:
`.ufo/waves/round-90/count-c1.py` (274 lines, sha per `evidence/controls-r90.txt`), `count-c2.py`
(471 lines), `controls-r90.sh`, `evidence/controls-r90.txt`, `contract.md`.
No file in the lane was edited. No tool installed or upgraded (nothing was needed).
Method: source listing of every write/process site, plus `strace -f -e trace=openat,creat,mkdir,
mkdirat,rename,unlink,unlinkat` over real runs in
`/fast/scratch/hyaku/mori-r90/Mo90Se01Boundary`.

## 1. Write scope and `--scratch` honouring — **FAIL** (C1 selftest); PASS (C1 run, C2)

Every write site, with line:

| file:line | write | target |
|---|---|---|
| count-c1.py:112-113 | `open(path,"w")` + `.write()` | `work/gate_<rev12>.py` (work is under `--scratch`) |
| count-c1.py:171 | `os.makedirs(base)` | `base` = `--scratch` \| `$HYAKU_SCRATCH` \| `tempfile.gettempdir()` |
| count-c1.py:172 | `tempfile.mkdtemp(dir=base)` | under `base` |
| count-c1.py:223 | `tempfile.mkdtemp(dir=os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir())` | **ignores `--scratch`** |
| count-c1.py:225-226 | `open(path,"w")` + `.write(body)` | `deny.py`, `allow.py` in that mkdtemp; **never removed** |
| count-c2.py:119 / :127 | `mkdtemp(dir=scratch)` / `rmtree` | under `--scratch`, removed |
| count-c2.py:229-230, :251-252 | `makedirs` + `open(target,"w")` | `scratch/pristine-*`, `scratch/mut-*` |
| count-c2.py:292-295, :310-315, :362, :374, :381 | `write()` fixture | `scratch/tmp*` |
| count-c2.py:425-427 | `base` / `mkdtemp(dir=base)` | `--scratch` \| `$HYAKU_SCRATCH` \| `/tmp`, removed at :467 |

No hardcoded `/tmp` literal in either file (`grep -n "/tmp"` → none); only
`tempfile.gettempdir()`.

Proof of honouring — `strace`, write-intent opens (`O_WRONLY|O_RDWR|O_CREAT|mkdir|creat`)
filtered to paths outside the declared `--scratch`:

```
python3 -I count-c1.py d1c84889 --repo $LANE --scratch $S/c1run      → rc=1
  C1=unmet branch_open=8 harm=0 newopen=0 open=30 cases=78 rev=d1c848898651
  BATTERY cases=0 branch_cases=0 branch_open=0 harm=0 newopen=0 paths=0
  outside-targets: (none)   writes into lane: 0
python3 -I count-c2.py d1c84889 --repo $LANE --scratch $S/c2run      → rc=1
  C2=unmet ... arms=28,26 detector=green rev=d1c848898651
  outside-targets: (none)   writes into lane: 0   leftovers: 0 entries
python3 -I count-c2.py --selftest --scratch $S/c2st                 → pass=21 fail=0
  outside-targets: (none)
```

The measured (non-selftest) paths are clean: zero writes outside `--scratch`, zero leftovers.

**The C1 selftest is not clean.** `--selftest` ignores `--scratch` (line 223 never reads
`args.scratch`) and never deletes its mkdtemps:

```
python3 -I count-c1.py --selftest --scratch $S/c1st   (HYAKU_SCRATCH=$S/hyak)
  C1_COUNTER_SELFTEST pass=12 fail=0
  files: $S/hyak/tmp5hwtw415/deny.py  $S/hyak/tmppon45j2l/allow.py
  $S/c1st: empty            ← --scratch not honoured
```

Residue on the host from the round's own runs (`controls-r90.sh:45` invokes the selftest with
**no** `--scratch`, and the script does not export `HYAKU_SCRATCH`, so `gettempdir()` is used):

```
/tmp/tmpbv62l39j  deny.py   2026-11-04 20:13:03
/tmp/tmpnx_8nwcu  allow.py  2026-11-04 20:13:03
/tmp/tmpmcedf8s3  deny.py   2026-11-04 20:23:23
/tmp/tmpf1yd5206  allow.py  2026-11-04 20:23:23
/tmp/tmprgxypr3l  deny.py   2026-11-04 20:26:48   ← matches controls header 2026-11-04T20:26:46
/tmp/tmpmn2z5k0v  allow.py  2026-11-04 20:26:48
```

Six dirs, two per selftest (one `mkdtemp` per `fake()` call), all still on disk. The committed
control evidence therefore narrates a run that wrote outside its scratch and leaked.

Severity: **medium** (no lane corruption; host residue in the shared `/tmp`, cross-seat hygiene,
violates the seat scratch rule via the round's own script). Smallest remediation: line 223 →
`tempfile.mkdtemp(dir=args_scratch_or_hyaku)` and a `finally: shutil.rmtree`; `controls-r90.sh:45`
→ pass `--scratch "$SCRATCH/c1st"` and export `HYAKU_SCRATCH`.

## 2. Mutation of the lane or any repo — **PASS**

Every `git` invocation, by line:

| file:line | argv | class |
|---|---|---|
| count-c1.py:91 | `git -C repo ls-tree -r --name-only <rev> -- .ufo/waves/round-90/battery/` | read-only |
| count-c1.py:98 | `git -C repo show <rev>:<battery path>` | read-only |
| count-c1.py:108 | `git -C repo show <rev>:<.ufo/waves/round-87/count-c2.py>` | read-only |
| count-c1.py:179 | `git -C <repo> rev-parse --show-toplevel` | read-only |
| count-c1.py:181 | `git -C repo rev-parse --verify <rev>^{commit}` | read-only |
| count-c2.py:434 | `git -C <repo> rev-parse --show-toplevel` | read-only |
| count-c2.py:436 | `git -C repo rev-parse --verify <rev>^{commit}` | read-only |
| count-c2.py:443 | `git -C repo show <rev>:<path>` | read-only |

No `add/commit/checkout/reset/stash/pull/push/clone/worktree` and no `subprocess` with
`shell=True` (grep for `shell=True` → none). The only non-git subprocess is
`python3 -I <copy> --selftest` (count-c2.py:123, :446) run with `cwd` inside scratch and
`GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM=/dev/null` — executes lane-derived bytes at R, writes
nothing. Empirical: the `strace` runs above show **0** write-intent opens under the lane, and
`git -C <lane> status --porcelain` is identical before and after my runs (same 7 entries; the new
`w1/*.md` files are sibling seats', written after my first status).

## 3. Credential-shaped material, fleet-root writes, sibling-lane writes — **PASS**

Scanned every file under `.ufo/waves/round-90/` (13 files, incl. `w1-spec.json`,
`w1-spec.inherited.json`, `w1-dispatch.json`, `w1/*.md`) for
`AKIA…|ghp_…|github_pat_|sk-…|xox[baprs]-|-----BEGIN …PRIVATE KEY|eyJ….eyJ…|api[_-]?key|secret|passw|credential|bearer|netrc|~/.ssh`:

```
AKIA/ghp_/sk-/xox/BEGIN KEY/base64-JWT count per file: 0   (all 11 non-w1 files)
case-insensitive api_key|secret|passw|credential|bearer|netrc|~/.ssh  → only `import tokenize`
```

Absolute `/home` paths occur only in `controls-r90.sh:5,25` (`LANE=/home/vgpnk/Projects/shokunin/
mori-shokunin`, used for `cd` and a read-only `spec_from_file_location`) and in the dispatch
artifacts: `grep -oE "/home/vgpnk/Projects/shokunin/[a-z0-9_.-]+"` over `w1-spec.json` and
`w1-dispatch.json` yields exactly one distinct value, `mori-shokunin`, 61 times each. No
fleet-root file (`LOG.md`, `SCORECARD.md`, `MANIFEST.json`, `.ufo/state/`, `.scratch/`) is named
as a write target and none is touched by either counter (`--repo` defaults to the lane). No
sibling-lane path appears anywhere in the round directory.

## 4. Does `load_battery` execute code from the battery JSON? — **PASS on execution, FAIL on trust**

`load_battery` (count-c1.py:89-104) does `git show` + `json.loads` and `dict(item, …)` only. There
is no `eval`, `exec`, `compile`, `pickle`, `yaml`, `runpy`, `__import__` or `shell=True` in either
counter (grep output: only `re.compile` false positives). The command text reaches
`gate.binding_problems(cmd, …)`, a text predicate. **So no battery file can execute code.**

But four fields of the untrusted file are honoured verbatim, which lets a battery file satisfy the
claim's own guard clause:

* `class` — `load_battery` never assigns a class; `tally` reads `case.get("class")`
  (count-c1.py:148) straight from the JSON, so `branch_cases` and `branch_open` are
  **self-declared**.
* `reach` — `counted = not case.get("reach")` (count-c1.py:139) lets any case exclude itself.
* `name` — printed unsanitised (count-c1.py:152). A `\n` in `name` emits a whole extra physical
  line, including a forged `C1=` verdict.
* `expect` — anything that is not `met` falls into the `reject` branch of `tally`.

Demonstrated against a scratch fixture repo (`git init -q`, toplevel asserted
`/fast/scratch/hyaku/mori-r90/Mo90Se01Boundary/fixture-battery`), 14 entries, no real counterfeit:

```
load_battery → n cases: 14; classes: 12× "branch" (from JSON); reach: [..., True] on one entry
tally        → {'cases': 13, 'branch_cases': 12, 'branch_open': 0, ...}   ← >=12 clause met by declaration
physical output line 2: 'C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78 rev=deadbeefcafe …'
```

Impact: the C1 guard "`branch_cases >= 12`, written by a seat that did not author the rule" is not
measured at all — it is whatever the JSON says. A hostile or careless battery also reaches a
cheap crash (non-dict item → `TypeError`, exit 1, not the setup status 2) and unbounded memory
(`json.loads` of a huge blob), and can forge the printed verdict.

Severity: **high** for the `branch_cases` clause; **medium** for the output injection.

Two further boundary facts in the same function's neighbourhood:

* `gate_at` (count-c1.py:106-119) `exec_module`s the gate fetched from R. The counter is not a
  pure reader of R: a malicious gate committed at R runs at import time with the counter's
  privileges (lane is inside the operator's HOME).
* `bound` (count-c1.py:121-124) dispatches on `except TypeError` to drop the `repo` argument.
  A `TypeError` raised *inside* a four-argument gate is caught and re-invoked with three
  arguments, silently reclassifying or double-executing the gate. Severity: **medium**.

Smallest remediation: whitelist the fields (`harden` each item to `{name, expect, cmd}` of
`str`, reject unknown keys, `re.sub(r"\s", " ", name)`), and derive the battery class from the
frozen `BRANCH` ids or from a counter-side rule rather than from the file.

## 5. Frozen predicate vs printed sentence, byte for byte — **PASS for the two verdict lines, FAIL for `BATTERY`**

Extracted with `ast.literal_eval` on the `TARGET` assignments and a backtick regex on
`contract.md`:

```
contract C1 : 'C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78 rev=<12>'
emitted  C1 : 'C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78 rev=<12>'   equal: True
contract C2 : 'C2=met mutants=15 killed=15 survivors=0 unattributed=0 unanchored=0 isolated=0 literal_anchors=0 arms=29,27 rev=<12>'
emitted  C2 : 'C2=met mutants=15 killed=15 survivors=0 unattributed=0 unanchored=0 isolated=0 literal_anchors=0 arms=29,27 rev=<12>'   equal: True
```

(`C1` emits `TARGET + " rev=" + rev[:12]`, count-c1.py:203-207; `C2` emits
`"C2=met %s rev=%s" % (TARGET, rev[:12])`, count-c2.py:464. `rev[:12]` is exactly the contract's
`<12>`. The real line at `d1c84889` is
`C1=unmet branch_open=8 harm=0 newopen=0 open=30 cases=78 rev=d1c848898651`.)

`BATTERY` does **not** match. Contract (`contract.md:9`):
`BATTERY cases=<n> branch_cases=<n> branch_open=0 harm=0`. Printed (count-c1.py:209):
`BATTERY cases=%d branch_cases=%d branch_open=%d harm=%d newopen=%d paths=%d`, and in practice
`BATTERY cases=0 branch_cases=0 branch_open=0 harm=0 newopen=0 paths=0`
(`evidence/controls-r90.txt`). Six fields against four: equality fails, and only the first five
fields match as a prefix. Worse, `tally` prints a **second** line with the same `BATTERY` prefix
and a different field set (count-c1.py:156-158):
`BATTERY cases=13 branch_cases=12 branch_open=0 harm=0 newopen=0 open=0 gained=0`.
Amendment A3's stated purpose — "the frozen predicate sentence and the printed line are the same
string" — is therefore not achieved. A checker doing an exact-line match on the contract sentence
fails on both lines; a prefix match passes on both, and picks up the wrong line first.
Severity: **medium** (a verifier can read the wrong `BATTERY` line). Smallest remediation: make
count-c1.py:209 print exactly the contract's five fields (drop `newopen=`, `paths=`), or correct
the contract sentence to the printed form, and give the tally summary a different label.

## Adjacent defects (found while proving the above)

1. **Entering revision is not the contract's entering revision.** `count-c1.py:50` defaults
   `ENTERING = 30a29797…` (round-88 spot-check), while the contract's entering is `037c02ca…`.
   The round-87 gate blob differs between them —
   `30a29797: 7acdeb2e…`, `037c02ca: 8ff54155…`, `git diff --stat … → 219 insertions(+), 5
   deletions(-)` — so `harm`/`newopen` are graded against a pre-repair baseline. On the frozen 78
   cases the tally is identical today (`branch_open=8 harm=0 newopen=0 open=30` under both
   baselines, both runs above), so no number moves now; it is a provenance defect, **medium**.
2. **The frozen population is read from the working tree, not from R.** `R03`/`C02`
   (count-c1.py:74-75) are resolved from `__file__`, and `load_cases` opens them directly
   (count-c1.py:76-77). A dirty tree changes the 78 cases while `rev=<12>` still labels the run.
   The control evidence was produced that way (in-lane run at 20:26). Severity: **medium**.
3. **`C2=met` prints the constant, not the measurement.** count-c2.py:461-464 prints
   `TARGET` after `target_split(tail)` validates it; the measured `tail` is only ever printed on
   the unmet path. Values are therefore correct-by-validation but not the measured string, so a
   field added to `tail` would silently not appear. Severity: **low**.
4. **Latent scratch escape in C2.** `target = os.path.join(tree, path)` (count-c2.py:229, :251)
   returns `path` unchanged if a mutant path were absolute, and does not reject `..`; the frozen
   `MUTANTS` paths are relative today. Severity: **low** (guarded by a frozen constant, not by
   the code).

## Summary

| # | Question | Verdict |
|---|---|---|
| 1 | writes outside `--scratch` | **FAIL** — C1 selftest (count-c1.py:223-226), 6 dirs leaked in `/tmp` by the round's own control run; C1 run and C2 clean under strace |
| 2 | mutates the lane / any repo | **PASS** — 8 git calls, all `ls-tree`/`show`/`rev-parse`; 0 lane writes |
| 3 | credentials / fleet-root / sibling-lane writes | **PASS** — none found |
| 4 | battery JSON executes code | **PASS** (data only) / **FAIL** trust: `class`, `reach`, `name`, `expect` taken from the file; `branch_cases>=12` is self-certifiable; `C1=` line forgeable |
| 5 | predicate sentence == printed sentence | **PASS** for `C1=`/`C2=` (byte-equal modulo `<12>`) / **FAIL** for `BATTERY` (6 fields printed vs 4 frozen; second same-prefix line) |

Scratch `/fast/scratch/hyaku/mori-r90/Mo90Se01Boundary` removed before this report was yielded:
`rm -rf` then `test ! -e` (see the run log in the seat transcript). Nothing was installed; no
pacman, no network.
