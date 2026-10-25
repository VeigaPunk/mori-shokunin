# R48SentTools — execution-surface security review of the four landed tools (round 48, w2)

Seat: R48SentTools (mori-shokunin, leaf; no subagent dispatch).
Surface attacked: `tools/mori-pin-check.py` (917 lines), `tools/mori-unlanded-check.py` (209),
`.ufo/waves/round-48/count-c1.py` (397), `.ufo/waves/round-48/count-c2.py` (349) — command
execution (registered selftests run from a git archive), path/argv restrictions, symlink and path
traversal, tar extraction, environment leakage, temp-dir handling, and git invoked against repos
whose config is not ours.
Date: 2026-10-25. All fixtures under
`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48SentTools/`; every run with
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48SentTools`. Host reads
read-only. No lane/fleet file was edited, no git index or jj state touched (only `git init`/
`git commit` inside scratch fixtures; each fixture's `rev-parse --show-toplevel` asserted equal to
the fixture path before its first commit). Nothing installed, no pacman run. No credential
material read or printed (the environment probe used a dummy variable).

## Verdict at the top

- **HOLDS — archive extraction and argv/path restrictions.** `tarfile.extractall(filter="data")`
  refuses escaping symlinks and absolute link targets with a one-line setup error (exit 2, no
  traceback); the argv shape gate rejects `..`, `.scratch` (top and nested), absolute paths,
  trailing arguments, `-c`, `-E`, `bash -x`, and non-`.py`/`.sh` suffixes. I found **no** way to
  make a junk registry edit green through the tool's own path/argv rules, and no shell primitive
  (`shell=True`, `os.system`, `eval`, `exec`, `Popen`) exists in any of the four tools.
- **BREAKS — class `containment` + `evidence-fidelity` + `operability`.** Three docstring promises
  are contradicted by reproduced behaviour:
  1. "The command runs … in the measured tree" — the measured tree is **not** a boundary: the
     export lives under `<repo>/.scratch/pin-check-*/tree`, so an instrument's unqualified `git`
     discovers the **live repository** and can write to it (reproduced: `git reset --hard` from a
     pinned instrument reset the fixture's working tree; `rev-parse --absolute-git-dir` from the
     export resolved to the fixture's `.git`).
  2. "Read-only over committed bytes" — the verdict is a function of ambient repository state (the
     same tree in a fresh single-commit repo scores `PIN_CHECK=unmet`, mismatches=2; in a clone of
     the lane at `e4dfff32` it scores `met`) and of the caller's environment (`PYTHONPATH`
     `sitecustomize` and `BASH_ENV` each flip `PIN_CHECK=unmet` → `met`).
  3. "removed on exit" — interrupted runs leave the full export behind: **100 stale
     `pin-check-*` dirs, ~34 GB**, none touched in 20+ minutes at 19:45 on 2026-10-25; each
     export is ~322 MB because `git archive` of the tip is 324 024 320 bytes.
- `mori-unlanded-check.py` carries three findings on the same surface (the repo it measures):
  `git status` honours the repo's `core.fsmonitor` and executes an arbitrary program (reproduced)
  while the docstring says "Read-only: `git rev-parse` and `git status --no-optional-locks` only";
  `.git/info/exclude` hides an in-scope untracked report (`UNLANDED=clean`); and a `GIT_DIR` in the
  caller's environment makes it compare another repository's index and report `clean` for a
  genuinely untracked report — the round-47 mistake class, with a green receipt.
- `count-c1.py` does not bind the tool under test to the revision (a stub that exists nowhere in
  the revision is executed 13× and scored), and it crashes with a raw traceback (rc 1) instead of
  the documented setup exit 2 when `<repo>/.scratch` does not exist.
- `mori-pin-check.py` forwards `--baseline-rev` to `git show` as an option:
  `--baseline-rev=--output=<path>` writes `<path>:SKILL.md` and empties the baseline, so
  `dropped`/`rebound` can never fire while the line still says `baseline=yes` (F11).

None of these changes the C1/C2 verdict at the landed tip as measured here (see §Tip measurement);
they are limits and defects to route, not a re-scoring of C1/C2 (executors own the predicate runs).

## Findings

| id | severity | tool | class | one-line |
|---|---|---|---|---|
| F1 | medium | count-c1.py | evidence fidelity | `--tool` is executed verbatim; nothing ties those bytes to `tools/mori-pin-check.py` at R |
| F2 | medium | mori-pin-check.py | environment leakage | instruments run with the caller's full environment, no forced `-I`, no `BASH_ENV` scrub; evidence is env-controlled |
| F3 | medium | mori-pin-check.py | containment | measured tree is not isolated: unqualified `git` from an instrument targets the live repo and can mutate it |
| F4 | medium | mori-unlanded-check.py | untrusted-repo git | `core.fsmonitor` from repo config executes a program during `git status` |
| F5 | medium | mori-unlanded-check.py | false clean | `.git/info/exclude` hides an in-scope untracked report; tool prints `UNLANDED=clean` |
| F6 | low | count-c1.py | operability | missing `<repo>/.scratch` ⇒ raw traceback, rc 1 (reads as "unmet", not setup) |
| F7 | low | mori-pin-check.py | containment asymmetry | command paths are checked lexically only; `--root` mode executes an out-of-tree symlink |
| F8 | low | mori-pin-check.py | env-driven redirection | `GIT_DIR` in the caller env redirects `--repo`; the export comes from another repository |
| F9 | medium | mori-unlanded-check.py | false clean (env) | `GIT_DIR` makes the check compare another repo's index and print `UNLANDED=clean` for an untracked report |
| F10 | medium | mori-pin-check.py / count-c1.py | temp-dir hygiene | 100 stale exports, ~34 GB, `.scratch/` untracked and not gitignored |
| F11 | medium | mori-pin-check.py | argument injection | `--baseline-rev=--output=<path>` writes a file and silently empties the baseline (`baseline=yes`, `dropped=0`) |

### F1 — `count-c1.py` does not bind the tool under test to R (medium)

The predicate says "the tool bytes under test (`tools/mori-pin-check.py` at R)", but
`count-c1.py:293` runs `tool = os.path.abspath(opts["--tool"])` and `run_tool` (`:206`) executes
that path directly; the revision is used only for `git show R:SKILL.md` (`:194`). Nothing compares
the executed bytes with `git show R:tools/mori-pin-check.py`.

Reproducer (tiny fixture whose anchors satisfy all 12 variants; the stub exists nowhere in the
revision):

```
$ python3 .scratch/r48w2-R48SentTools/probe3.py
== stub-outside-rev rc=1
   variant name=J1 expect=unmet got=met rc=0        … J1-J8 all got=met rc=0 …
   variant name=H1 expect=met got=met rc=0          … H1-H4 and real got=met rc=0 …
   C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12 rev=548d9c39…
== nonexistent rc=1
   … all 13 variants got=error rc=2 …
   C1=unmet junk_met=8 honest_unmet=4 real=error errors=13 variants=12 rev=548d9c39…
```

So the counter executes and scores bytes that are not in the revision at all (and an absent path
is only caught because the tool fails, not because the counter checks it). The false-green
direction is: R's `tools/mori-pin-check.py` is weak, the seat passes `--tool` pointing at a
stronger copy (an older fixed version, a scratch rewrite) and the counter prints `C1=met` for
bytes R does not contain. The claim's own command passes the repo path, so the landed receipt is
honest — but the counter cannot enforce that.

Only the tool side is unanchored: the registry side **is** bound (`git show R:SKILL.md`), so a seat
cannot substitute the registry — it can substitute the tool.

Smallest remediation: when `--tool` is given, require
`sha256(open(tool,'rb').read()) == sha256(git show R:tools/mori-pin-check.py)`, else
`C1_SETUP` exit 2; or drop `--tool` and always materialise the tool from R.

### F2 — the caller's environment controls the pin evidence (medium)

`mori-pin-check.py:406` — `env = dict(os.environ, TMPDIR=tmp, PYTHONDONTWRITEBYTECODE="1")` — the
child inherits everything; `argv_ok` *allows* `-I` but never adds it, and shell instruments are run
as plain `bash <path> --selftest` with `BASH_ENV` intact. `count-c1.py:206` inherits the same way.

Reproducers (fixtures whose real tally is `pass=1` while the registry pins `pass=2`, so the honest
verdict is `unmet`):

```
$ python3 .scratch/r48w2-R48SentTools/envprobe.py
py clean    (1, 'PIN_CHECK=unmet … mismatches=1 …')
py PYTHONPATH (0, 'PIN_CHECK=met  … mismatches=0 …')      # sitecustomize.py rewrote print()

$ python3 .scratch/r48w2-R48SentTools/probe2.py
(a) sh clean    (1, 'PIN_CHECK=unmet … mismatches=1 …')
(a) sh BASH_ENV (0, 'PIN_CHECK=met  … mismatches=0 …')     # BASH_ENV exec'd a fake instrument
(b) no var      (1, 'PIN_CHECK=unmet …')
(b) with var    (0, 'PIN_CHECK=met  …')                    # instrument printed the tally only
                                                           # when R48_PROBE_TOKEN=leaked was inherited
```

Impact: (i) the reconciler's verdict is a function of the seat's shell, so a stray `PYTHONPATH`
(after any experiment that sets one) can make stale pins look current — the exact false-green
class C1 exists to exclude; (ii) every executed instrument can read every variable the caller
holds (tokens included), which matters because the tool is meant to be runnable in CI.

Smallest remediation: build the child env from an allowlist (`PATH`, `HOME`, `LANG`, `LC_ALL`,
`TMPDIR`, `PYTHONDONTWRITEBYTECODE`); prepend `-I` for `python*` argv; drop `BASH_ENV`/`ENV` for
`bash`/`sh`. (TMPDIR survives `-I`, so the `tmpdir_inside_measured_tree` arm still holds.)

### F3 — the measured tree is not a boundary; unqualified `git` targets the live repo (medium)

`export_rev` extracts to `<repo>/.scratch/pin-check-XXXX/tree` (`:625`) and `run_cmd` runs the
instrument with `cwd=root` (`:400-410`). The export contains no `.git`, so git discovery walks up
into the live repository. Read-only proof — the pin carries the fixture's absolute git dir, so a
`met` verdict proves the discovery:

```
$ python3 tools/mori-pin-check.py --rev HEAD --repo $S/fix/gitctx2 --min-tally-pins 1
pin line=3 kind=tally prefix=G_SELFTEST state=match
  pinned='gitdir=/…/fix/gitctx2/.git' observed='gitdir=/…/fix/gitctx2/.git' rc=0
  cmd='python3 tools/probe.py --selftest'
PIN_CHECK=met … rc=0
```

Write proof — a pinned instrument runs `git reset --hard HEAD` with no `-C`:

```
$ python3 .scratch/r48w2-R48SentTools/probe6.py
== part2 dirty before: DIRTY EDIT THAT MUST NOT SURVIVE
== part2 rc=0
   pin line=3 … prefix=W_SELFTEST state=match … cmd='python3 tools/probe.py --selftest'
   PIN_CHECK=met … rc=0
== part2 dirty after : committed content
```

The instrument's `git reset --hard` reset the **fixture repository's** working tree, not the
export. Applied to the lane, any code a measured revision carries that runs unqualified `git`
(including a pinned instrument) addresses `/home/vgpnk/Projects/shokunin/mori-shokunin` — its
index and working tree — during a `--rev` run. The lane forbids seats from mutating git state; the
tool creates the condition that makes such a mutation land on the real repo.

The same non-isolation is load-bearing for the verdict: the reconciler is **not** a function of
committed bytes alone. The identical tree scores differently depending on which repository encloses
it (both runs with the same v3 tool bytes, `--min-tally-pins 26`):

| repository | rev | result |
|---|---|---|
| `git clone --no-hardlinks` of the lane (real history) | `e4dfff32` | `PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 … rc=0` (79 s) |
| fresh repo, `git archive e4dfff32` extracted, one commit | its own `HEAD` (`4ed652dd`) | `PIN_CHECK=unmet … mismatches=2 … rc=1` (26 s) |

```
$ python3 $S/good-tool.py --rev HEAD --repo $S/fix/c1-clean --min-tally-pins 26 --baseline-rev HEAD
pin line=182 kind=tally prefix=R19_SELFTEST state=mismatch pinned='pass=26 fail=0' observed='pass=25 fail=1' rc=1
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=mismatch pinned='pass=11 fail=0'
  observed='pass=1 fail=10' rc=1 cmd='python3 .ufo/waves/round-40/conform.py 4ed652dd… --selftest'
PIN_CHECK=unmet tally_pins=31 digest_pins=8 mismatches=2 … rc=1
```

The `conform.py` difference is deterministic, not noise: `CONFORM_SELFTEST pass=1 fail=10` three
times out of three in the copy, `pass=11 fail=0` in the clone (`conform.py` itself calls
`git -C repo rev-parse HEAD`, `conform.py:522`). I did not establish which repository attribute the
`timeout_state` arm depends on (UNVERIFIED); the observable is that `PIN_CHECK=met` means "these
bytes, in a repository that looks like the lane, at measurement time" — not "these committed bytes".
(`R19_SELFTEST` additionally refuses a `TMPDIR` outside the lane root —
`R19_SELFTEST setup=explicit-lane-tmpdir-invalid` when run directly — so that pin is
environment-gated too.)

Smallest remediation: extract into `tempfile.mkdtemp()` **outside** the repository (the child's
`TMPDIR` is already forced inside the tree, so the child contract is unaffected) and run the child
with `GIT_CEILING_DIRECTORIES=<export parent>` or `GIT_DIR`-less `-C <export>`; state in the
docstring that the verdict includes ambient history, or make the two history-reading pins
explicit.

### F4 — `core.fsmonitor` from repo config executes a program during `git status` (medium)

`mori-unlanded-check.py:37-58` runs `git -C repo --no-optional-locks status …` with the repo's own
config. `git status` runs a configured `core.fsmonitor` program.

```
$ git -C "$D" config core.fsmonitor "$S/fsmon.sh"     # fsmon.sh: touch $PWN; exit 0
$ python3 tools/mori-unlanded-check.py --repo "$D" --round 8
UNLANDED=clean round=8
rc=0
PWNED core.fsmonitor executed
```

Remediation verified:

```
$ git -C "$D" --no-optional-locks -c core.fsmonitor=false status --porcelain=v1 -z --untracked-files=all
remediation blocks it
```

Impact: the docstring's "Read-only" is wrong; pointing the check at a repo whose `.git/config` is
not ours (a checkout shipped with a `.git` dir, a shared repo, `GIT_CONFIG_GLOBAL`/`include.path`
chains) executes attacker-chosen code with the caller's privileges. Smallest remediation: add
`-c core.fsmonitor=false` (and `-c core.untrackedCache=false`) to the single `git()` helper, and
consider `GIT_CONFIG_NOSYSTEM=1`.

Contrast with F8 worth recording, and a defect in its own right (F9): the top-level guard at
`:55-57` does **not** catch a redirected `GIT_DIR`. With `GIT_DIR` set and no `GIT_WORK_TREE`,
git takes the worktree from the cwd, so `rev-parse --show-toplevel` still equals `--repo` and the
guard passes — while `git status` compares the **other** repository's index/HEAD against this
worktree.

### F5 — `.git/info/exclude` turns an unlanded report into `UNLANDED=clean` (medium)

```
$ mkdir -p $D/corpus/lessons && echo x > $D/corpus/lessons/round-8.md
$ printf 'corpus/lessons/round-8.md\n' > $D/.git/info/exclude
$ python3 tools/mori-unlanded-check.py --repo "$D" --round 8
UNLANDED=clean round=8
rc=0
$ rm $D/.git/info/exclude && python3 tools/mori-unlanded-check.py --repo "$D" --round 8
UNLANDED=dirty round=8 paths=1
unlanded ?? corpus/lessons/round-8.md
rc=1
```

The docstring names this limit ("anything git ignores is outside the scope on purpose"), but the
tool exists to catch the round-47 mistake (late results never committed) and local exclude state is
exactly what can hide it without touching a tracked file. Smallest remediation: after the status
pass, also read `git ls-files --others` **without** `--exclude-standard` (or `git status
--ignored=matching`) and report in-scope paths that are excluded as a separate class
(`unlanded !! …`), so an excluded report is visible without changing the `clean` semantics for
`__pycache__` etc.

### F6 — `count-c1.py` crashes instead of exiting 2 when `<repo>/.scratch` is missing (low)

`:292` — `tempfile.mkdtemp(prefix="c1-", dir=os.path.join(repo, ".scratch"))` with no
`os.makedirs`. On a fresh repository:

```
$ python3 .ufo/waves/round-48/count-c1.py --tool … --rev HEAD --repo $D …
Traceback (most recent call last):
  File "…/count-c1.py", line 292, in main
    scratch = opts["--scratch"] or tempfile.mkdtemp(prefix="c1-", dir=os.path.join(repo, ".scratch"))
FileNotFoundError: [Errno 2] No such file or directory: '…/fix/c1-tiny/.scratch/c1-_dlffdpk'
rc=1
```

Exit 1 is indistinguishable from "C1=unmet" for a wrapper that only looks at the status code, and
the counter's documented setup contract is exit 2 with one line. Smallest remediation:
`os.makedirs(os.path.join(repo, ".scratch"), exist_ok=True)` inside the same try that prints
`C1_SETUP`.

### F7 — the executed command path is checked lexically only (low)

`argv_ok` (`:124-137`) validates `SAFE_PATH` (`:110`) on the string; `inside_tree` (`:269-275`,
realpath) guards digest/line-count pins but not the command that gets executed. In `--root` mode
(measure a directory as-is) an out-of-tree symlink is executed:

```
$ python3 .scratch/r48w2-R48SentTools/probe5.py    # 18-shape matrix, --root mode
pin line=20 kind=tally prefix=A_SELFTEST state=match … cmd='python3 tools/esc.py --selftest'
PIN_CHECK=unmet … (the other 17 rows exercise the rejections)
```

`tools/esc.py` was a symlink to a file outside the measured root. In `--rev` mode this is blocked
earlier by the tar `data` filter (see N1), so the escape is not reachable from an archive on this
host (CPython 3.14.8); it is reachable from `--root`, and it is the one containment check the
tool's own selftest does not arm (`r7_symlink_digest_not_inside` covers digests only). Smallest
remediation: resolve the bound path with `inside_tree(root, path)` before running, and add the
matching selftest arm.

### F8 — `GIT_DIR` in the caller environment redirects `--repo` (low)

```
$ GIT_DIR=$S/fix/good/.git python3 tools/mori-pin-check.py --rev HEAD --repo $S/fix/env-py --min-tally-pins 1
pin line=3 kind=tally prefix=EVIL_SELFTEST state=match … cmd='python3 tools/evil.py --selftest'
PIN_CHECK=met … rev=1242456182223d0bd23e54634b84dca9345d6059 …
```

`rev=1242456…` is the `good` fixture's HEAD; `env-py`'s HEAD was `18e3f833…`. The tool exported a
different repository than `--repo` names. `git -C` only changes directory; `GIT_DIR` wins. Related
observation: `--repo <subdir>` makes `git archive` archive only that subdirectory, and the run ends
in `PIN_CHECK_SETUP unreadable …/tree/SKILL.md` (exit 2) rather than measuring the parent repo —
harmless, but `mori-unlanded-check` is the only one of the four that verifies `--repo` is a top
level.

Smallest remediation: drop `GIT_DIR`, `GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_INDEX_FILE`,
`GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES` from the env of the tool's own git calls.
(The `mori-unlanded-check` top-level guard is **not** an equivalent defence — see F9.)

### F9 — `GIT_DIR` makes `mori-unlanded-check` report `clean` for a genuinely unlanded file (medium)

Same redirection as F8, applied to the check that exists to catch late unlanded work. Two scratch
repos: `G` tracks `corpus/lessons/round-8.md`; `W` (`--repo`) has the same file untracked.

```
$ python3 tools/mori-unlanded-check.py --repo "$W" --round 8
UNLANDED=dirty round=8 paths=1
unlanded ?? corpus/lessons/round-8.md
rc=1
$ GIT_DIR="$G/.git" python3 tools/mori-unlanded-check.py --repo "$W" --round 8
UNLANDED=clean round=8
rc=0
```

Impact: with `GIT_DIR` in the caller's environment (a seat's shell, a harness wrapper, a
`GIT_DIR`-exporting toolchain), the round's hygiene check silently measures a different repository
and reports `clean` — the round-47 mistake class it was built to prevent, with a green receipt.
Smallest remediation: run the two git calls with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/
`GIT_OBJECT_DIRECTORY` removed from the child env (`env = {k: v for k, v in os.environ.items() if
not k.startswith("GIT_")}`), and keep `GIT_OPTIONAL_LOCKS=0`.


### F10 — interrupted runs leak ~322 MB exports into the working tree (medium, operability)

`main` removes `scratch` in a `finally`, which does not run on SIGKILL/seat timeout. State observed
in the lane at 19:45 on 2026-10-25:

```
$ ls -d .scratch/pin-check-* | wc -l
100
$ find .scratch -maxdepth 1 -name 'pin-check-*' -newermt '-20 minutes' | wc -l
0
$ du -sm <all pin-check-*> …            # earlier total
34G	total                               # one dir: 632 MB; typical 322 MB
$ git archive --format=tar e4dfff32 | wc -c
324024320
$ git check-ignore -v .scratch ; echo rc=$?
rc=1                                    # .scratch is NOT ignored
```

Each leftover is a full export (`tree/` with `corpus/`, `.ufo/waves/` 265 MB). They are untracked
but not ignored, so they appear as `??` paths in `git status` and would be staged by any
`git add -A`; `mori-unlanded-check` deliberately skips `.scratch/`, so the round's own hygiene
check cannot see them. Smallest remediation: (a) sweep stale `pin-check-*`/`c1-*` dirs at startup
(age > timeout), (b) put the export under `tempfile.gettempdir()` rather than inside the repo
(child `TMPDIR` is set independently), (c) add `.scratch/` to `.gitignore`.

### F11 — `--baseline-rev` is passed to `git show` as an option; the baseline is silently emptied (medium)

`mori-pin-check.py:673` builds `["git", "-C", repo, "show", args.baseline_rev + ":SKILL.md"]` with no
`--` separator and no revision validation. argparse refuses a value that starts with `-` in the
space-separated form, but `--baseline-rev=--output=<path>` is accepted and reaches git as
`--output=<path>:SKILL.md`.

```
$ python3 tools/mori-pin-check.py --rev HEAD --repo "$D" --min-tally-pins 1 \
      "--baseline-rev=--output=$PWD/pwn2"
pin line=3 kind=tally prefix=EVIL_SELFTEST state=match … rc=0
PIN_CHECK=met … dropped=0 rebound=0 … baseline=yes
rc=0
$ ls -la "$PWD/pwn2:SKILL.md"
-rw-r--r-- 1 vgpnk vgpnk 743 Oct 25 20:08 …/pwn2:SKILL.md     # git wrote here
```

Two effects: (a) an arbitrary-path file creation (the `:SKILL.md` suffix is appended to the path,
the content is git's output for the commit), and (b) `--output` suppresses stdout, so
`baseline_text` becomes empty, `pin_keys("")` is empty, and `dropped`/`rebound` can never fire —
while the summary line still says `baseline=yes`. The two junk rules that depend on the baseline
(J-class "delete a pin", "rebind a pin") are then dead, silently. The predicate's own command
passes a fixed hex baseline, so C1 as written is unaffected; a seat that passes a hostile or
mistyped value gets a green-looking receipt with the baseline checks disabled.

Smallest remediation: resolve the baseline once, like `--rev` does
(`git rev-parse --verify <arg>^{commit}` → full sha), and pass the resolved sha; never forward the
raw argument to git.

## Negative results (attacked, did not land)

- **N1 — tar extraction.** `git archive` emits symlink members for tracked symlinks; with
  `filter="data"` both escapes are refused, one line, exit 2:
  `PIN_CHECK_SETUP 'tools/evil.py' would link to '…/outside.py', which is outside the destination`
  and `PIN_CHECK_SETUP 'tools/evil.py' is a link to an absolute path`. A symlink to another in-tree
  file is extracted and executed (`PIN_CHECK=met`, by design). Hardlink members cannot come out of
  `git archive`; UNVERIFIED for a hand-built tar.
- **N2 — `tar.<fmt>.command`.** With `git -C D config tar.tar.command "touch $PWN"`, a full
  `--rev HEAD` run finished `PIN_CHECK=met`, rc 0, and `no exec` (the file was never created):
  `--format=tar` selects the builtin archiver, not a configured filter. git 2.56.0.
- **N3 — shell primitives.** `grep -n "shell=True\|os.system\|eval(\|exec(\|os.popen\|Popen"` over
  the four tools: no matches (rc 1). All subprocesses are argv lists.
- **N4 — argv matrix** (`--root`, 18 shapes): accepted `python3 …`, `python3 -I …`,
  `python3 -B …`, `bash …`, `sh …`, `.ufo/waves/round-48/a.py`, and a bare `tools/a.py` (bound as
  `python3 tools/a.py --selftest`); rejected with `state=no_command` — `python3 -E …`,
  `bash -x …`, `tools/../tools/a.py`, `.scratch/a.py`, `tools/.scratch/a.py`, an absolute path,
  `--selftest extra`, `python3 -c …`, `tools/a.txt`, and `python3 tools/a.py` without the flag. The
  `-c` row additionally raises `unparsed` (`token-not-at-span-start`) and `hidden` (its tally sits
  in the entry cell, R9a).
- **N5 — git option injection (partly landed — see F11).** `--baseline-rev '--output=…'` is
  refused by argparse ("expected one argument"), but the `=` form is *not*; `--rev=--output=…` ends
  in `PIN_CHECK_SETUP unresolvable revision` (rc 2), so only the baseline path is injectable.
- **N6 — `count-c2.py --entry` traversal.** `--entry ../../../etc/passwd` →
  `C2=unmet … failed=entry_absent`; `git show rev:path` reads tracked blobs only, and `--entry`
  cannot leave the repository.
- **N7 — temp-dir cleanup.** An instrument that deletes its `TMPDIR` and replaces it with a symlink
  to a victim directory: the run still scores, and the victim's file survives (`victim intact
  True`) — `shutil.rmtree` does not follow the swapped symlink. A normal exit leaves no
  `pin-check-*` dir in the fixture (`leftover exports … []`).

## Tip measurement (independent, in a clone — not the lane working tree)

I did not run the C1 predicate (executors own that receipt). To measure the tool at the tip without
writing into the lane working tree, I cloned the lane and ran the v3 bytes there:

```
$ git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin $S/clone
$ python3 $S/good-tool.py --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --repo $S/clone \
      --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0
  rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
rc=0
```

`good-tool.py` is `git show e4dfff32:tools/mori-pin-check.py` copied byte-for-byte out of that
archive. So the landed v3 bytes do score `met` on the landed registry in a repository that carries
the real history — the C1 direction holds for this input; the caveats are F1 (the counter would
accept any other `--tool` path too) and F2/F3 (the environment and the enclosing repository are
part of the measurement).

## Working-tree observations (not this seat's)

At 20:07 on 2026-10-25 the lane working tree showed `M SKILL.md`, `M
corpus/knowledge/quota-observability-r48.md` (both mtime 20:03:31) and untracked
`.ufo/waves/round-40/scratch/mori-conform-selftest-*` (24 dirs, newest 20:08) beside the 100
`pin-check-*` export dirs of F10. None of these was created by this seat: every run here passed
`--repo` pointing at a scratch fixture, and my `conform.py` invocations ran inside the copy and the
clone. Origin UNVERIFIED (concurrent seats). Two reasons to record it: the C1 predicate reads
`SKILL.md` from the revision (`git show R:SKILL.md`), so a modified working tree does not change its
registry side — but the tool bytes come from the path handed to `--tool` (F1); and the round-40
scratch dirs are outside `mori-unlanded-check`'s round-48 scope, so the round's own hygiene check
cannot see them.

## Limits of this seat

- I did not re-run the C1/C2 predicates at the tip (executors own those receipts); I measured the
  tool at the tip only in a `git clone --no-hardlinks` of the lane (see §Tip measurement).
- I did not audit all 31 pinned instruments for unqualified `git` writes; F3's mutation was proved
  with my own instrument, not with a lane instrument.
- CPython < 3.11.4 (`extractall` without `filter=`) is untested: [INFERENCE] the `TypeError` is
  caught by `main`'s `except Exception` and exits 2, never an unfiltered extraction.
- Only git 2.56.0 / CPython 3.14.8 on this host were exercised.
- Findings F1-F11 are defects and limits of the instruments; none of them re-scores C1 or C2.
