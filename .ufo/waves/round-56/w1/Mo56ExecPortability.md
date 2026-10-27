# Mo56ExecPortability — QUALITY 127 + §7 item 4 portability audit (round 56, wave w1)

Seat: executor / portability audit (round prompt §7 item 4; `corpus/QUALITY.md:1270-1278`).
Lane `mori-shokunin`. Frozen contract read first: `.ufo/waves/round-56/contract.md`.

Audited revision (the freeze tip named by the dispatch): `8be2717b0809281d07dffe83dad424a4859e0747`.
Entering tip: `5b295eeebd87ebd610d8d39bfe2035742f740cfa`. Lane HEAD while I ran: `acc62f54fb0f53b47b428594dc27365150cbd76b`
(the w1-dispatch commit; it adds only `build-w1-spec.py`, `w1-spec.json`, `w1-dispatch.json`, `w1-dispatch.stderr`).
I confirmed the five audited files are **byte-identical** at the freeze tip and at HEAD
(`git rev-parse HEAD:<path>` == `git rev-parse 8be2717b:<path>` for all five), so every observation below is a
statement about the frozen bytes, not about a moving working tree.

Files audited (absolute paths):

```
/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-driver-liveness.py            (479 lines)
/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-vote-bind.py                   (447 lines)
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c1.py           (208 lines)
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c2.py           (170 lines)
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/controls/controls.py  (113 lines)
```

Environment: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit 0;
`/fast/scratch/hyaku 28% use 585.6G free`, `/tmp 4% use 124.0G free`. Scratch
`/fast/scratch/hyaku/mori-r56/Mo56ExecPortability/` (one `git clone --shared` of the lane at the freeze tip, one
probe copy of the two tools, one `strace` output set). Removed at the end (see §6).
No tool was installed or upgraded; no pacman transaction (the orchestrator's pacman guard is host-wide paused).
`strace` was already present (`/usr/bin/strace`); `python3` is 3.14.8; `git` present.
No lane file was written except this report; no fleet-root tracked file was touched; no git/jj mutation was
performed in the lane (read-only `git log/show/diff/rev-parse/ls-tree/grep/clone --shared` only).

## 1. The seat's two greps, verbatim, with exit codes

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && grep -nE "mkdtemp\(dir=[\"']/tmp|/tmp/" \
    tools/mori-driver-liveness.py tools/mori-vote-bind.py .ufo/waves/round-56/count-c1.py \
    .ufo/waves/round-56/count-c2.py .ufo/waves/round-56/controls/controls.py
exit=1          # zero matches, in all five files
```
(Note: `controls.py` is at `.ufo/waves/round-56/controls/controls.py`, not `.ufo/waves/round-56/controls.py` as the
seat brief spelled it. `.ufo/waves/round-56/controls.py` does not exist at the freeze tip:
`wc: …/round-56/controls.py: No such file or directory`. The directory `controls/` holds exactly one file,
`controls.py`. I audited the file that exists.)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && grep -n "/home/vgpnk" \
    tools/mori-driver-liveness.py tools/mori-vote-bind.py .ufo/waves/round-56/count-c1.py \
    .ufo/waves/round-56/count-c2.py .ufo/waves/round-56/controls/controls.py
.ufo/waves/round-56/count-c1.py:178:    repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
.ufo/waves/round-56/count-c2.py:145:    repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
.ufo/waves/round-56/controls/controls.py:70:    repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
exit=0
```

### Classification of every hit

| hit | file:line | what it is | classification |
|---|---|---|---|
| 1 | `count-c1.py:178` | `repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"` — the **default** value of the `--repo` argument, used when `--repo` is not passed | **executable default that breaks off-host replay** (see F-1) |
| 2 | `count-c2.py:145` | same default | **executable default that breaks off-host replay** (see F-1) |
| 3 | `controls/controls.py:70` | same default | **executable default that breaks off-host replay** (see F-1) |

There are **no** `/tmp/` hits and **no** other host-path hits in any of the five files. The two *tools* —
`mori-driver-liveness.py` and `mori-vote-bind.py` — carry **zero** absolute host paths (the grep above returns
nothing for them; `git grep -c -F '/home/vgpnk' 8be2717b -- tools/mori-vote-bind.py` → 0,
`… -- tools/mori-driver-liveness.py` → 0). The three hits are all in the *wave instruments* (counters + controls),
which is where the previous five rounds put their equivalents — see §4.

## 2. PROOF: both tools honour TMPDIR

`strace` was available, so I used it rather than a before/after `/tmp` listing alone. Trace set:
`-e trace=openat,mkdir,mkdirat,creat,symlink` (every syscall that can create a file or directory), `-f` to follow
children, with `TMPDIR` pointed at a scratch directory I created.

```
$ export S=/fast/scratch/hyaku/mori-r56/Mo56ExecPortability
$ mkdir -p $S/tmp && export TMPDIR=$S/tmp
$ strace -f -qq -o $S/trace-driver.txt -e trace=openat,mkdir,mkdirat,creat,symlink \
    python3 …/tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0        # rc=0

$ strace -f -qq -o $S/trace-vote.txt -e trace=openat,mkdir,mkdirat,creat,symlink \
    python3 …/tools/mori-vote-bind.py --selftest
VOTE_BIND_SELFTEST pass=16 fail=0                        # rc=0
```

Trace analysis (counts over the whole trace file):

| trace | writes under `/tmp` (`O_CREAT|O_WRONLY|O_RDWR` on a `/tmp` path) | writes under `$TMPDIR` |
|---|---|---|
| driver-liveness selftest | **0** | 4 (1 `mkdir` + 3 `openat` in `$TMPDIR/mori-driver-liveness-v23i2vxx`) |
| vote-bind selftest | **0** | 12 (2 `mkdir` + 10 `openat` in `$TMPDIR/mori-vote-bind-stmcpze3`, `$TMPDIR/mori-vote-bind-1yqewx3_`) |
| count-c1 (freeze rev) | **0** | 108 |
| count-c2 (freeze rev) | **0** | 35 |
| controls.py (entering rev) | **0** | 136 |

`grep -c '"/tmp' trace-driver.txt` → **0** and `grep -c '"/tmp' trace-vote.txt` → **0**: neither tool so much as
*opened* a path under `/tmp` (not even for reading) while `TMPDIR` pointed elsewhere.

The literal `/tmp` lines in the traces are the ones under my scratch, e.g.:

```
mkdir("/fast/scratch/hyaku/mori-r56/Mo56ExecPortability/tmp/mori-driver-liveness-v23i2vxx", 0700) = 0
openat(AT_FDCWD, "…/tmp/mori-driver-liveness-v23i2vxx/watchdog.log", O_WRONLY|O_CREAT|O_TRUNC|O_CLOEXEC, 0666) = 3
mkdir("/fast/scratch/hyaku/mori-r56/Mo56ExecPortability/tmp/mori-vote-bind-stmcpze3", 0700) = 0
```

Mechanism, in the source: `mori-driver-liveness.py:352` and `mori-vote-bind.py:332,363` all use
`tempfile.mkdtemp(prefix=…, dir=os.environ.get("TMPDIR") or None)` — the environment wins over the platform
default, and `None` means "stdlib default" only when `TMPDIR` is unset. The same pattern is used by the three
wave instruments (`count-c1.py:124`, `count-c2.py:77`, `controls/controls.py:73`).

Independent `/tmp` before/after listing across the whole session:

```
$ ls -1 /tmp > before.txt ; … ; ls -1 /tmp > after.txt ; diff before.txt after.txt
698,699c698
< tameshi-r4-2-regression.BHB4pL
< tameshi-r4-2-selftest.X6VwPu
---
> tameshi-r4-2-regression.h4FXto
```
The only delta in `/tmp` is another seat's rotating temp names — none of the five audited files.

**Verdict: both tools honour TMPDIR. PASS.**

### Two TMPDIR edge cases (limits, not defects of the tools)

* `TMPDIR` pointing at a **non-existent** directory: `tempfile.mkdtemp` raises `FileNotFoundError` inside the
  selftest case, the case is caught by the selftest's `except Exception` arm and counted as a failure:
  ```
  TMPDIR=/nonexistent/dir python3 …/mori-driver-liveness.py --selftest
  DRIVER_LIVENESS_SELFTEST pass=12 fail=1 skipped=0 failed=t_empty_log:EXC:[Errno 2] …            rc=1
  TMPDIR=/nonexistent/dir python3 …/mori-vote-bind.py --selftest
  VOTE_BIND_SELFTEST pass=14 fail=2 failed=t_tally_mini:EXC:…,t_roster_and_name_filter:EXC:…        rc=1
  ```
  The counters/controls do **not** survive it — the `mkdtemp` call is outside their try/except, so they die with a
  raw traceback and **rc=1** (which a caller could misread as "unmet" rather than "setup error"):
  ```
  TMPDIR=/nonexistent/dir python3 …/count-c1.py 8be2717b…
  FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/dir/mori-r56-c1-7oe9iw4y'   rc=1
  ```
  (`count-c2.py` and `controls.py` behave identically.) The frozen contract says exit 2 means "setup"
  (`count-c1.py:29` "Exit 0 met, 1 unmet, 2 setup"); an unusable TMPDIR currently exits **1**, i.e. it is
  reported in the same channel as a substantive "unmet". Routed item, F-4.
* `TMPDIR` set to a **relative** path is honoured literally and resolves against the current working directory
  (`TMPDIR=rel-tmp` → `FileNotFoundError: 'rel-tmp/mori-vote-bind-fcasxorz'`), because `mkdtemp(dir=…)` treats a
  relative `dir` as relative to cwd. Not a portability break for a well-behaved caller (TMPDIR is absolute in
  practice), noted for completeness.

## 3. Off-host replay: what actually travels, what does not

I made one `git clone --shared` of the lane at the freeze tip into scratch and drove the frozen bytes from there.

**Passes off-host (the tools).** The tools derive their fixture tree from `__file__`, not from a host path
(`mori-driver-liveness.py:66-67` `_repo_path()` = `dirname(dirname(abspath(__file__)))`, used by
`_fixture_dir()` at `:251-253`):

```
$ python3 $S/clone/tools/mori-driver-liveness.py --selftest   → DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0   rc=0
$ python3 $S/clone/tools/mori-vote-bind.py --selftest          → VOTE_BIND_SELFTEST pass=16 fail=0                     rc=0
```
`mori-vote-bind.py` has no repo-relative dependency at all (its selftest fixtures are synthesized under TMPDIR),
so it is location-independent by construction. `mori-driver-liveness.py` is location-dependent **by design of its
fixture path**: it needs the tool to sit at `<tree>/tools/mori-driver-liveness.py` with
`<tree>/.ufo/waves/round-56/fixtures/driver/` beside it. Copied out of that shape it degrades silently:

```
$ mkdir -p $S/lonely/tools && cp …/tools/mori-driver-liveness.py $S/lonely/tools/
$ python3 $S/lonely/tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=2 fail=0 skipped=11            rc=0     ← 11 cases skipped, still exit 0
```
Same through a symlink (`os.path.abspath` does not resolve symlinks, so `_repo_path()` points at the link's
directory):
```
$ ln -s …/tools/mori-driver-liveness.py $S/bin/mori-driver-liveness.py
$ python3 $S/bin/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=2 fail=0 skipped=11            rc=0
```
This matters for the *off-host replay* story only in combination with the counter: `count-c1.py` deliberately
materializes the tool under `<cwd>/tool/tools/` and the fixtures under `<cwd>/tool/.ufo/…` so the tool's
`dirname(dirname(__file__))` lands back on the materialized tree (`count-c1.py:71-83` and `:118-124`), and the
counter then runs the tool with `cwd=<cwd>/tool`. That reconstruction works and is why the counter's fixture arm
passes off-host. But the *tool alone* has no such guard, and its `skipped=11` exit code 0 is indistinguishable
from a healthy run by exit status alone. The counter catches it because it string-matches
`DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0` (`count-c1.py:37` `EXPECT_SELFTEST`), so the frozen
predicate is not weakened; the exposure is a user running the tool directly. F-3.

**Fails off-host without `--repo` (the three wave instruments).** All three default `repo` to the host path:

```
$ strace -f -qq -s 120 -e trace=execve python3 $S/clone/.ufo/waves/round-56/count-c1.py <clone-only-rev>
… execve("…/git", ["git", "-C", "/home/vgpnk/Projects/shokunin/mori-shokunin", "rev-parse", …])
C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=56f982e9…   rc=1
$ python3 $S/clone/.ufo/waves/round-56/count-c1.py <clone-only-rev> --repo $S/clone
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=56f982e9…                               rc=0
```
The same script, same revision, in the same directory, gives **two different answers** depending on whether
`--repo` is passed — because without it the counter silently measures the *host* tree, not the tree it was copied
from. The clone-only revision `56f982e950cdaeb4f1ff654eb134b5e57547913b` (a marker commit I made in the clone)
does not exist in the host repo, so the host-tree read yields `failed=tool_absent` while the clone read yields
`C1=met`. The `--repo` override does exist in all three and does work — the defect is that the **default** is a
host path rather than a location-relative derivation. Contrast the previous rounds, which derive the lane root
from `__file__`:

* `.ufo/waves/round-53/count-c1.py:296-297` → `lane_root()` = four `dirname`s up from `__file__`
* `.ufo/waves/round-54/count-c1.py:397-398` → same
* `.ufo/waves/round-55/count-c1.py:440-441` → same
* `.ufo/waves/round-51/count-c1.py:37-38`, `round-52/count-c1.py:483-484` → same idea, `HERE`/`os.path.dirname`

Round 56 is the first of the last six rounds to regress to a hardcoded host path in its counters. F-1.

## 4. QUALITY 127 scope count at the freeze tip, with its scope stated

`corpus/QUALITY.md:1270-1278` states the criterion and its check:

> "Instruments carry no absolute host path, and the count of those that do is stated with its scope. …
> Check: `git ls-tree -r --name-only <rev> -- tools/ | grep -E '\.(py|sh)$' | xargs git grep -l -F '/home/vgpnk' <rev> --`
> lists only files that predate the criterion (3 at `e5dbac05`), and **a new instrument adds none**."

Two scopes are defensible; I measured both, at both revisions, and state which is which.

**(a) The criterion's literal check scope — `tools/` only.** The literal command in the criterion text scopes to
`tools/`:

| revision | tracked `.py`/`.sh` under `tools/` | of those, containing `/home/vgpnk` |
|---|---|---|
| entering `5b295eee` | 36 | 3 — `tools/mori-blind-check.sh`, `tools/mori-misroot-sweep.py`, `tools/mori-round17-context-check.py` (all predate the criterion) |
| freeze `8be2717b` | 38 | **3 — the same three, unchanged** |

**Round 56 adds two new tools and zero new host-path offenders under this scope.** Both new tools are clean:
`mori-driver-liveness.py` and `mori-vote-bind.py` contain no `/home/vgpnk` at all. The criterion's "a new
instrument adds none" clause **holds** under the literal `tools/` scope.

**(b) The criterion's stated scope, which the rationale names as wider than `tools/`.** The rationale says the
defect "reproduces only for the three `tools/` scripts plus ten top-level wave instruments of rounds 40–43; all
tracked `.py`/`.sh` under `tools/` and `.ufo/waves/round-*/` give 395 at both `e5dbac05` and `2d85e33d`". Measured
over exactly that scope (`tools/` + `.ufo/waves/round-*/`, tracked `.py`/`.sh`):

| revision | scope files | with `/home/vgpnk` |
|---|---|---|
| entering `5b295eee` | 943 | **404** |
| freeze `8be2717b` | 948 | **407** |

The **+3** delta is exactly the three round-56 wave instruments, and no removals:

```
$ comm -13 <(hosts at entering) <(hosts at freeze)
.ufo/waves/round-56/controls/controls.py
.ufo/waves/round-56/count-c1.py
.ufo/waves/round-56/count-c2.py
```
Each contributes exactly **one** occurrence (`git grep -c -F '/home/vgpnk' 8be2717b -- <file>` → 1 for each of the
three). So under the criterion's own rationale scope, round 56 **does** add three host-path carriers — all three
being the same `repo = "/home/vgpnk/…"` default line (F-1). Under the narrower `tools/`-only scope it adds none.
The honest statement of the criterion's standing at the freeze tip is therefore:

> QUALITY 127 as literally checked (`tools/` scope) is **satisfied** at the freeze tip: 3 offenders, unchanged,
> all predating the criterion, and the two new round-56 tools add none. QUALITY 127 as scoped by its own
> rationale (`tools/` + `.ufo/waves/round-*/`) moves **404 → 407**, the +3 being the three round-56 counters and
> controls, each adding the identical hardcoded `repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"` default.

## 5. Other portability-relevant observations in the five files

* **`count-c1.py` / `count-c2.py` setup guard is weaker than the last three rounds'.** Both use
  `git rev-parse --verify <rev>` **without** `^{commit}` (`count-c1.py:181`, `count-c2.py:148`). A 40-hex that does
  not exist in the repo still verifies, so the setup guard does not fire:
  ```
  $ git rev-parse --verify 1111111111111111111111111111111111111111   → prints the sha, rc=0
  $ git rev-parse --verify 1111111111111111111111111111111111111111^{commit}   → fatal: Needed a single revision, rc=128
  $ python3 …/count-c1.py 1111111111111111111111111111111111111111
  C1=unmet … failed=tool_absent rev=1111111111111111111111111111111111111111    rc=1
  $ python3 …/round-55/count-c1.py 1111111111111111111111111111111111111111
  C1_SETUP unresolvable revision 1111111111111111111111111111111111111111    rc=2
  ```
  Consequence: a typo'd or never-pushed revision is reported as the **same** `failed=tool_absent` line as the
  legitimate entering-tip do-nothing control, so the do-nothing control's discrimination is weakened — the
  controls.py do-nothing arm passes for a revision that never existed:
  ```
  $ python3 …/controls/controls.py 1111111111111111111111111111111111111111
  do-nothing-c1  PASS C1=unmet … failed=tool_absent rev=1111111111111111111111111111111111111111   rc=0
  ```
  (`count-c1.py`/`count-c2.py` are FROZEN per the dispatch; this is a named limit + a routed item for round 57,
  not a change proposal for this wave. See F-2.)
* **`count-c2.py` reports `selftest=ok … contrast=voted0` on an absent tool.** At the entering tip:
  ```
  $ python3 …/count-c2.py 5b295eee…
  C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=5b295eee… failed=tool_absent   rc=1
  ```
  Every arm field reads `ok` even though the tool is absent and no arm ran. `count-c1.py` has an explicit
  special case for this (`count-c1.py:174-176` prints `selftest=bad fixtures=bad …`); `count-c2.py` does not
  (`count-c2.py:154-166` maps only the arms it knows). The `failed=tool_absent` suffix does disclose the truth,
  and the frozen evidence receipt `evidence/controls.txt` records exactly this line as the entering-tip do-nothing
  receipt — so the counter is self-consistent with its own receipt — but the field-level `ok`s are misleading on
  their face. Named limit, routed to round 57 (F-2).
* **`controls/controls.py` reads the tool and the counters from `HEAD`, not from the enter revision.**
  `git_show(repo, "HEAD", path)` at `:81` and `:94`. That makes the control's byte-level subject depend on the
  repo's current HEAD rather than on the frozen revision the control is meant to characterize. Demonstrated: with
  the clone's HEAD carrying a one-token edit to the tool, the mutant arm whose substitution pattern no longer
  matches reports `ERROR substitution did not apply` and the whole control exits 1:
  ```
  mut:fence-toggle-dropped     ERROR substitution did not apply        rc=1
  ```
  and with the enter-rev pointing at a tree where the tool *is* present, the do-nothing arm flips to `FAIL`:
  ```
  do-nothing-c1  FAIL C1=met selftest=ok … rev=56f982e9…      rc=1
  ```
  The frozen receipt in `evidence/controls.txt` was produced with HEAD == the freeze tip, so it is reproducible
  *today*; but the receipt is not pinned to a revision by construction. Named limit (F-2, same routed item).
* **Dead code / unused imports** (quality, not portability, but they are in the audited files):
  `mori-vote-bind.py:57` imports `hashlib` and never uses it; `controls/controls.py:13` imports `re` and never uses
  it; `controls/controls.py:54` defines `run(repo, rev, path, cwd)` which is never called (the body is inlined at
  `:84-92` and `:100-107`). `mori-vote-bind.py`'s `min_votes` parameter is threaded through `tally()` and printed
  nowhere and changes no output:
  ```
  $ … tally … --verb RECHECK --voter …   → TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
  $ … tally … --verb RECHECK --voter … --min 99   → identical line
  $ … tally … --verb RECHECK --voter … --min 0    → identical line
  ```
* **The C1 counter leaks its scratch tree.** `count-c1.py`/`count-c2.py`/`controls.py` call `mkdtemp` and never
  `rmtree` it (no `shutil` import in any of the three), so each invocation leaves a ~64 KB tree
  (`<tmp>/tool/tools/mori-driver-liveness.py` plus the materialized fixture tree) behind:
  ```
  before=26 after=28   (delta=2 for two counter runs)
  ```
  With `TMPDIR` unset, the same leak lands in `/tmp` — `env -u TMPDIR python3 …/count-c1.py <rev>` created
  `/tmp/mori-r56-c1-b7yexyvn` (I removed the 13 such directories my session created; the pre-session `/tmp`
  listing is unchanged). This is the "residue producer" class the lane lesson `corpus/lessons/round-51.md` M2
  tracks, in a mild form. Low severity because the residue is under `TMPDIR` when set, but it does accumulate in
  `/tmp` for a caller that does not set `TMPDIR` (F-5).
* **The two tools clean up after themselves.** `mori-driver-liveness.py:357-358` does
  `shutil.rmtree(tmp, ignore_errors=True)`; `mori-vote-bind.py:354-355` and `:379-380` do
  `shutil.rmtree(tmp)` inside `try/except OSError`. Neither leaves a residue — the only leftovers in my scratch
  after all runs were the counters' trees. Good.
* **`mori-driver-liveness.py` never writes into the repo.** Confirmed by `git status --porcelain` before/after
  running both tools' selftests and both counters at the freeze tip: `diff` of the two listings is empty
  (`diff_rc=0`). The `__pycache__` entries under `tools/` are `.gitignore`d (`.gitignore:3: __pycache__/`) and
  were not created by my runs (their mtimes predate my session and are unchanged by running the tools as scripts).
* **`mori-driver-liveness.py:345` hardcodes `/nonexistent/mori-driver-liveness-test.log`** as the
  "missing log" probe path. It is a POSIX-root absolute path, not a host path, and it is only ever opened for
  reading (and must not exist) — no write, no portability consequence for the tool's own use. Recorded for
  completeness because the seat's grep family is about absolute paths.

## 6. Scratch hygiene

Scratch root `/fast/scratch/hyaku/mori-r56/Mo56ExecPortability/` — one `git clone --shared` of the lane (at the
freeze tip, plus two probe commits I made *inside the clone*), one `lonely/` probe copy of the two tools, one
`bin/` symlink, one `ro-tmp/` read-only dir, and the strace outputs. `TMPDIR` was exported to
`$S/tmp` for every run. Removed at the end:

```
$ rm -rf /fast/scratch/hyaku/mori-r56/Mo56ExecPortability   # after this report was written
```
The 13 `/tmp/mori-r56-c*-*` directories my session created were removed individually (all 13 had mtimes inside my
session window; the pre-existing `/tmp` entries were left alone).

## 7. Limits of this audit (stated, not hidden)

* I did **not** execute the counters' `--selftest` arms against a tree where the tool is deliberately mutated, so
  I have no independent evidence about the C1/C2 counters' own `--selftest` logic; I only read them.
* `strace` was available and used, so the TMPDIR proof is syscall-level rather than filesystem-diff-level. The
  filesystem diff is reported alongside it as a second, weaker check.
* The QUALITY 127 counts above use `git grep -l -F '/home/vgpnk'` over `git ls-tree -r` output, which counts
  *files*, matching the criterion's own command. I did not count occurrences per file except for the three
  round-56 instruments (1 each).
* I did not measure how the counters behave under a git implementation other than the host's git; the
  `rev-parse --verify` semantics I rely on (accepting a bare 40-hex) are git-version-dependent in principle,
  though they have been stable for many years. The finding is stated against the host's git.
* No conclusion is offered here about whether the frozen counters should be *changed* — the dispatch freezes the
  counters, predicates, controls and kill rules. Every weakness above is stated as a named limit with a routed
  item for round 57, which is what the dispatch asks for.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| **F-1** | **HIGH** | `.ufo/waves/round-56/count-c1.py:178`, `.ufo/waves/round-56/count-c2.py:145`, `.ufo/waves/round-56/controls/controls.py:70` | The default `repo` is the absolute host path `/home/vgpnk/Projects/shokunin/mori-shokunin`. Off-host (clone/archive) replay without `--repo` silently measures the **host** tree instead of the tree the script was copied from — proven: the same script and revision in the same directory returned `C1=unmet … failed=tool_absent` without `--repo` and `C1=met` with `--repo <clone>`. This is the "hidden location dependence" class of `corpus/lessons/round-51.md` M1, and a regression against rounds 51–55, whose counters derive the lane root from `__file__` (`round-55/count-c1.py:440-441`). It is also the **+3** that moves the QUALITY 127 rationale-scope count 404 → 407 at the freeze tip (the literal `tools/`-only scope stays at 3, unchanged). The `--repo` override exists and works, so the fix is a default change, not a new capability. Frozen this wave → routed item for round 57. |
| **F-2** | **MED** | `.ufo/waves/round-56/count-c1.py:181`, `.ufo/waves/round-56/count-c2.py:148`; `.ufo/waves/round-56/count-c2.py:154-166`; `.ufo/waves/round-56/controls/controls.py:81,94` | Three related weaknesses in the frozen instruments, each demonstrated: (a) the setup guard uses `git rev-parse --verify <rev>` without `^{commit}`, so a never-existing 40-hex passes the guard and yields the same `failed=tool_absent` line as the legitimate entering-tip control — and `controls.py`'s do-nothing arm then PASSes for a revision that never existed (rounds 53/54/55 use `^{commit}` and correctly exit 2); (b) `count-c2.py` prints `selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok` on an absent tool, where no arm ran (`count-c1.py` has the explicit special case, `count-c2.py` does not); (c) `controls.py` reads its subject bytes from `HEAD` rather than from the revision under test, so the control receipt is not pinned by construction — a HEAD edit made `mut:fence-toggle-dropped` report `ERROR substitution did not apply` and flipped a do-nothing arm to `FAIL`. Frozen this wave → routed item for round 57. |
| **F-3** | **MED** | `tools/mori-driver-liveness.py:66-67`, `:251-253`, `:345-358` | The tool's fixture tree is derived from `__file__`, so a copy or symlink outside `<tree>/tools/` + `<tree>/.ufo/waves/round-56/fixtures/driver/` yields `DRIVER_LIVENESS_SELFTEST pass=2 fail=0 skipped=11` with **exit 0** — 11 of 13 cases skipped and indistinguishable from a healthy run by exit status. The frozen counter is not weakened (it string-matches `pass=13 fail=0 skipped=0`, `count-c1.py:37`), so the exposure is only to a direct user of the tool. A relative fixture root, or an explicit "fixtures not found ⇒ fail" arm, would close it. Tool text is pinned, so a change carries re-pin consequences → routed item for round 57. |
| **F-4** | **LOW** | `.ufo/waves/round-56/count-c1.py:124`, `.ufo/waves/round-56/count-c2.py:77`, `.ufo/waves/round-56/controls/controls.py:73` | An unusable `TMPDIR` (missing or unwritable) makes the three wave instruments die with an uncaught `FileNotFoundError`/`PermissionError` traceback and **exit 1**, i.e. in the same channel as a substantive "unmet", although the frozen contract reserves exit 2 for "setup". The two *tools* handle it correctly — their selftest catches the exception and reports it as a named failing case with rc=1 (`pass=12 fail=1` / `pass=14 fail=2`). Named limit → routed item for round 57. |
| **F-5** | **LOW** | `.ufo/waves/round-56/count-c1.py:124`, `.ufo/waves/round-56/count-c2.py:77`, `.ufo/waves/round-56/controls/controls.py:73` | None of the three wave instruments removes its `mkdtemp` tree (no `shutil` import in any of them), so each invocation leaves ~64 KB of materialized tool + fixture bytes behind — under `TMPDIR` when the caller sets it, in `/tmp` when they do not (measured: 2 leaked trees per 2 counter runs; 13 `/tmp/mori-r56-c*-*` dirs created by my session, all removed by me). The two tools do clean up (`mori-driver-liveness.py:357-358`, `mori-vote-bind.py:354-355,379-380`). Named limit → routed item for round 57. |
| **F-6** | **LOW** | `tools/mori-vote-bind.py:57`, `:36-45`; `.ufo/waves/round-56/controls/controls.py:13`, `:54-61` | Dead code in the audited files: `hashlib` imported and unused in `mori-vote-bind.py`; `re` imported and unused in `controls.py`; `controls.py:54` `run()` defined and never called; `mori-vote-bind.py`'s `min_votes` parameter is threaded through `tally()` but changes no output (`--min 0`, `--min 2`, `--min 99` produce identical tally lines). No behavioural risk; recorded for the L1's cleanup pass. |
| **F-7** | **LOW** | `tools/mori-driver-liveness.py:345` | Hardcodes the absolute POSIX-root probe path `/nonexistent/mori-driver-liveness-test.log` for the "log absent" selftest case. Read-only, never written, and no host-path leak — but it is an absolute path in an otherwise location-independent tool. Recorded, no action proposed. |

No finding above changes the frozen C1/C2 predicates, the counters' semantics, the controls or the kill rules, and
none of them is offered as a fix for this wave.

Report: .ufo/waves/round-56/w1/Mo56ExecPortability.md
