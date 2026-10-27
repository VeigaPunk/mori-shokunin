# Mo56SentPorts — portability sweep of the round-56 diff

Seat: Mo56SentPorts (leaf, no subagents). Lane: mori-shokunin. Diff under test:
`5b295eeebd87ebd610d8d39bfe2035742f740cfa..8be2717b0809281d07dffe83dad424a4859e0747`
(34 files, +2942/−0). All work read-only against the lane repo; the one clone is at
`/fast/scratch/hyaku/mori-r56/Mo56SentPorts/clone` (`git clone --shared`, then removed).

Frozen surface was not modified: no counter, predicate, control or kill rule is
proposed for change here; every defect below is a named limit plus a round-57 route.

## 1. Method

One `--shared` clone of the lane repo into scratch (a *foreign absolute path*), then every
committed executable was exercised against that clone, so any dependence on
`/home/vgpnk/Projects/shokunin/mori-shokunin` or on the fleet-root layout shows up as a
failure or a mismatch. Fixture repo rule was not needed (no fixture repo created); the
clone's `rev-parse --show-toplevel` was `/fast/scratch/hyaku/mori-r56/Mo56SentPorts/clone`
before any ref write, and the only ref written there was one scratch-local tag.

Environment knobs swept: `TMPDIR` (set, unset-parent, spaces), locale (`LC_ALL=C` with and
without PEP 538/540 coercion), working directory, and repo target (worktree, `.git`
objects-only dir, absent path).

## 2. The `/home/vgpnk` grep, hit by hit

Command (exit 0, five hits):

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n '/home/vgpnk' \
  8be2717b0809281d07dffe83dad424a4859e0747 -- .ufo/waves/round-56 \
  tools/mori-driver-liveness.py tools/mori-vote-bind.py \
  corpus/knowledge/driver-liveness-r56.md corpus/knowledge/vote-binding-r56.md \
  corpus/evidence/sources-r56
```

| # | Hit | Class | Behaviour |
|---|---|---|---|
| 1 | `.ufo/waves/round-56/controls/controls.py:70` | executable default, argument-honouring | `repo = "/home/vgpnk/.../mori-shokunin"`, overridden by `--repo DIR` (line 71-72) |
| 2 | `.ufo/waves/round-56/count-c1.py:178` | executable default, argument-honouring | same shape; `--repo DIR` (line 179-180) |
| 3 | `.ufo/waves/round-56/count-c2.py:145` | executable default, argument-honouring | same shape; `--repo DIR` (line 146-147) |
| 4 | `.ufo/waves/round-56/evidence/census-start.txt:24` | prose/record | a census row recording the measured path of `corpus/SOURCES.md`; data, not executed |
| 5 | `.ufo/waves/round-56/evidence/driver-liveness-live.txt:287` | prose/record | `"path": "/home/vgpnk/Projects/shokunin/.ufo/watchdog.log"` inside the frozen live JSON report; data |

Zero hits in `tools/mori-driver-liveness.py`, `tools/mori-vote-bind.py`,
`corpus/knowledge/driver-liveness-r56.md`, `corpus/knowledge/vote-binding-r56.md`, or
`corpus/evidence/sources-r56/`. The registry rows S544/S545 carry zero `/home/` hits
(`grep -c '/home/'` over both rows → 0). The fixture tree carries zero `/home/` hits and
its only symlink is relative (`state-shapes/state/kake.round` → `mori.round`), so the
frozen fixtures replay anywhere.

So: nothing executable is *hard-bound*; the three defaults are host paths that are
superseded by an argument — but they are the *only* resolution when no argument is given,
which is exactly how the frozen contract writes the replay commands (§5, F2).

## 3. Default-path behaviour of the two counters (the seat's fallback question)

Argument honoured, at a foreign checkout path, both counters grade `met`:

```
$ python3 clone/.ufo/waves/round-56/count-c1.py 8be2717b… --repo /fast/scratch/hyaku/mori-r56/Mo56SentPorts/clone
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
EXIT=0
$ python3 clone/.ufo/waves/round-56/count-c2.py 8be2717b… --repo /fast/scratch/hyaku/mori-r56/Mo56SentPorts/clone
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
EXIT=0
```

The default (no `--repo`) is *cwd-blind* and always targets the hardcoded host path. Proof
that it ignores the checkout under test: a rev that exists only in the clone

```
$ git -C <clone> tag proofonly-56 8be2717b…            # ref written in scratch clone only
$ git -C /home/vgpnk/.../mori-shokunin rev-parse proofonly-56
fatal: ambiguous argument 'proofonly-56': unknown revision or path not in the working tree.   (EXIT 128)
$ cd <clone>; python3 .ufo/waves/round-56/count-c1.py proofonly-56
C1_SETUP: unresolvable revision proofonly-56                                                   EXIT=2
$ python3 .ufo/waves/round-56/count-c1.py proofonly-56 --repo /fast/scratch/…/clone
C1=met … rev=8be2717b0809281d07dffe83dad424a4859e0747                                          EXIT=0
```

With the same rev resolvable in both repos, the default invocation from the clone's own
directory silently measured the *fleet* repo instead of the checkout it was standing in:

```
$ cd <clone>; python3 .ufo/waves/round-56/count-c1.py 8be2717b…      # no --repo
C1=met … EXIT=0
$ cd <scratch>; python3 clone/.ufo/waves/round-56/count-c2.py 8be2717b…   # no --repo, other cwd
C2=met … EXIT=0
```

Off-host the same code path is loud, not silent (absent path → `git -C` fails):
`--repo <absent dir>` → `C1_SETUP: unresolvable revision …`, EXIT=2.

Positive portability facts for the counters (all EXIT=0):
- objects-only target works — `--repo <clone>/.git` gives `C1=met …` and `C2=met …`, so no
  working tree is required (a bare mirror replays);
- no network: `grep -E 'import (socket|urllib|http|requests|ssl)|urlopen'` over both
  counters, `controls/controls.py` and both tools → no match (EXIT 1 from grep);
- no writes into the checkout: `git -C clone status --porcelain` empty after a dozen runs;
- `TMPDIR` containing spaces is safe (everything is argv, never a shell):
  `TMPDIR="/fast/…/tmp with space"` → `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`
  EXIT=0, `VOTE_BIND_SELFTEST pass=16 fail=0` EXIT=0, `C1=met …` EXIT=0;
- `controls/controls.py` also runs at a foreign path, default overridden by `--repo`:
  `do-nothing-c1 PASS`, `do-nothing-c2 PASS`, 8 mutants `KILLED`, EXIT=0.

## 4. `/tmp` writes regardless of `TMPDIR` — §7 item 4 does NOT reproduce

No committed tool or counter hardcodes `/tmp`. Every temp allocation is
`tempfile.mkdtemp(..., dir=os.environ.get("TMPDIR") or None)`:
`count-c1.py:124`, `count-c2.py:77`, `controls.py:73`, `tools/mori-driver-liveness.py:352`,
`tools/mori-vote-bind.py:332,363`. The only literal `/tmp` string in the diff is prose in
`tools/mori-vote-bind.py:54` (“TMPDIR/hyaku scratch only — never /tmp-hardcoded”).

Falsifiers run (this is the point of the item — an explicit `dir=` is a *hard* dependency,
not a fallback):

```
$ TMPDIR=/fast/…/Mo56SentPorts/no-such-tmp python3 clone/tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=12 fail=1 skipped=0 failed=t_empty_log:EXC:[Errno 2] No such file or directory: '/fast/…/no-such-tmp/mori-driver-liveness-_m9fzn_6',t_empty_log
EXIT=1
$ TMPDIR=/fast/…/no-such-tmp python3 clone/tools/mori-vote-bind.py --selftest
VOTE_BIND_SELFTEST pass=14 fail=2 skipped=0 failed=t_tally_mini:EXC:[Errno 2]…,t_tally_mini,t_roster_and_name_filter:EXC:[Errno 2]…
EXIT=1
```

Both tools fail loudly inside the bad `TMPDIR` path and never silently relocate to `/tmp`.
With a valid `TMPDIR` the artefacts appear there and nowhere else (no `mori-vote-bind-*` or
`mori-driver-liveness-*` residue survives: the tools clean up their own temp trees).

Follow-on observation (F5 below): the *counters* leave their `mkdtemp` trees behind —
after three counter runs the scratch `TMPDIR` held
`mori-r56-c1-8j70uhz0, mori-r56-c1-8p4umc1x, mori-r56-c1-fki6gwwb,
mori-r56-c2-3qdohbo4, mori-r56-c2-bvaoarpq`.

## 5. Findings

### F2 — MED — the frozen contract's replay command has no `--repo`, and the default is a host path
`.ufo/waves/round-56/count-c1.py:178`, `.ufo/waves/round-56/count-c2.py:145`,
`.ufo/waves/round-56/controls/controls.py:70`; contract commands at
`.ufo/waves/round-56/contract.md:31` and `:52` (`python3 .ufo/waves/round-56/count-c1.py R`
— no `--repo`).

Exploit path: an off-host verifier replays the contract verbatim from a clone. `--repo` is
absent, so the counter targets `/home/vgpnk/Projects/shokunin/mori-shokunin`, which does not
exist there: `C1_SETUP: unresolvable revision …`, EXIT=2. Worse, on a host where that exact
path *does* exist (a second checkout, a shared workstation), the default is silently
cwd-blind: proof above, `count-c1.py proofonly-56` from inside the clone fails while the
same rev with `--repo <clone>` grades `met`, and `count-c1.py 8be2717b…` from inside the
clone grades the fleet repo, not the clone in the caller's directory. Impact: replay
either fails loudly, or measures the wrong tree with no signal in the output line. Smallest
remediation (round 57, counters are frozen this round): make `--repo` default to
`git -C "$PWD" rev-parse --show-toplevel` and keep the absolute path only as a last-resort
fallback; and write the contract command as `count-c1.py R --repo .`.

### F1 — MED — both counters crash (empty stdout, EXIT=1) under an ASCII locale, which collides with the graded `unmet` exit code
`.ufo/waves/round-56/count-c1.py:50-51` and `.ufo/waves/round-56/count-c2.py:50-51`
(`subprocess.run(["git","-C",repo,"show",…], capture_output=True, text=True)`); same
`text=True` locale decoding at `count-c1.py:59,83,91`, `count-c2.py:62,149`,
`controls.py:50,89,107`.

Every `git show` decodes with the *locale* encoding, while the sha helpers correctly use
`encode("utf-8","surrogateescape")` — an asymmetry. `corpus/SOURCES.md` at the freeze tip
carries 14 non-ASCII lines (em dashes, lane names), so any host whose Python preferred
encoding is ASCII aborts in `git_show`:

```
$ LC_ALL=C LANG=C LC_CTYPE=C PYTHONCOERCECLOCALE=0 PYTHONUTF8=0 \
  python3 clone/.ufo/waves/round-56/count-c1.py 8be2717b… --repo <clone>
  File "…/count-c1.py", line 119, in evaluate
  File "…/count-c1.py", line 50, in git_show
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe2 in position 69: ordinal not in range(128)
EXIT=1
$ (same for count-c2.py, position 75, EXIT=1)
$ … count-c1.py … 2>/dev/null | wc -c
0
```

Impact: zero predicate bytes on stdout and EXIT=1 — byte-for-byte the same grade channel as
the control receipts' `C1=unmet … failed=tool_absent` (EXIT=1). A grader keyed on the exit
code records a false *unmet*; a grader keyed on text sees no verdict at all. Scope is
narrow but real: on this host plain `LC_ALL=C` still coerces to UTF-8
(`locale.getpreferredencoding(False)` → `utf-8`, `C1=met …` EXIT=0) and `PYTHONUTF8=1`
is `C2=met …` EXIT=0; the failure needs coercion disabled
(`PYTHONCOERCECLOCALE=0`/`PYTHONUTF8=0`), which minimal container and scheduler images do
set. Smallest remediation (round 57): add `encoding="utf-8", errors="surrogateescape"` to
the subprocess calls, and make an unexpected exception print a `*_SETUP` line and exit 2 —
i.e. stop overloading exit 1.

### F3 — LOW — the driver probe's selftest silently skips 11 of 13 cases and still reports success by exit code when invoked through a symlink
`tools/mori-driver-liveness.py:67` (`os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`
— `abspath`, not `realpath`) with `_fixture_dir()` at `:251-262`; a missing fixture tree
makes each case return `None`, which the runner counts as *skipped*, not failed.

```
$ ln -s clone/tools/mori-driver-liveness.py link-driver.py
$ python3 link-driver.py --selftest
DRIVER_LIVENESS_SELFTEST pass=2 fail=0 skipped=11
EXIT=0
```

(`tools/mori-vote-bind.py` via symlink is unaffected: `VOTE_BIND_SELFTEST pass=16 fail=0`,
EXIT=0 — its fixtures are built in `TMPDIR`.) Impact: an operator or harness that installs
a symlink shim gets "selftest ok" by exit code with 11 of 13 cases never run, i.e. the
tool's own exit contract is unsound; the counter's exact-string match
(`EXPECT_SELFTEST … skipped=0`) catches it as `selftest=bad`, so C1 grading is protected.
Smallest remediation: use `os.path.realpath`, and make the selftest exit non-zero when
`skipped` is non-zero outside an explicit `--allow-skip`.

### F4 — LOW — `evidence/freeze-sha256.txt` is not a self-verifying manifest anywhere
`.ufo/waves/round-56/evidence/freeze-sha256.txt` lines 11-12 (absolute `/home/vgpnk` paths),
lines 7-8 (`tools/…@6ced9da9` — `@rev` suffixes that are not filenames).

```
$ cd <clone>; sha256sum -c .ufo/waves/round-56/evidence/freeze-sha256.txt
sha256sum: WARNING: 6 listed file(s) could not be read ; EXIT=1
$ cd <clone>/.ufo/waves/round-56; sha256sum -c evidence/freeze-sha256.txt
contract.md: OK / count-c1.py: OK / count-c2.py: OK / controls/controls.py: OK
tools/mori-driver-liveness.py@6ced9da9: FAILED open or read
tools/mori-vote-bind.py@6ced9da9: FAILED open or read
/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r56/rfc8259.txt: OK
/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r56/watchdog-log-grammar.txt: OK
sha256sum: WARNING: 2 listed file(s) could not be read ; EXIT=1
```

The two absolute entries validate only on the machine that wrote them; off-host they vanish.
Grading is unaffected because the counters recompute both tool shas from git bytes and pass
`pins` — independently confirmed: `tools/mori-driver-liveness.py` at `6ced9da9` and at
`8be2717b` both hash to `6b3dba74…be997` (= counter PIN), and `tools/mori-vote-bind.py` at
both revs to `8be1acdb…a6bca` (= counter PIN). Smallest remediation: relative paths from the
receipt's own directory, no `@rev` suffix in the hash line, and a separate prose line naming
the data commit.

### F5 — LOW — the counters leak their scratch trees
`count-c1.py:124`, `count-c2.py:77`, `controls.py:73` `mkdtemp` with no `rmtree`; five
`mori-r56-c1-*`/`mori-r56-c2-*` directories remained in `TMPDIR` after three runs. Not a
correctness risk; on a `TMPDIR`-less host these land in `/tmp` and accumulate per replay.
Smallest remediation: `try/finally` with `shutil.rmtree(..., ignore_errors=True)` as the two
tools already do.

### F6 — LOW (informational) — the probe's default fleet root is layout-dependent, but degrades loudly
`tools/mori-driver-liveness.py:470-472`: default root is `dirname(repo path)`, i.e. it assumes
the checkout is a child of the fleet root. In a checkout at any other layout:

```
$ cd <clone>; python3 tools/mori-driver-liveness.py --now 1800000000
 "path": "/fast/scratch/hyaku/mori-r56/Mo56SentPorts/.ufo/watchdog.log", "state": "absent"
 "verdict": "DRIVER_LIVENESS_UNAVAILABLE"  rc 2  (EXIT=2)
$ python3 tools/mori-driver-liveness.py --fleet-root /home/vgpnk/Projects/shokunin --now 1800000000
DRIVER_LIVENESS_OK  lanes=23  log=1729 lines, malformed=0  (EXIT=0)
```

No false liveness claim is produced (absent is never zero), and `--fleet-root`, `--log`,
`--state-dir`, `--fixture` are all honoured; the derived path is echoed in the report so the
misresolution is visible. Worth one sentence in the round-57 doc: replay passes
`--fleet-root` explicitly.

## 6. Not observed / UNVERIFIED

- UNVERIFIED: portability of the two `corpus/evidence/sources-r56/*` fetches against the
  upstream network (no re-fetch attempted; sha256 61a5378f…/38ba3e6b… match the S544/S545
  rows and the receipt pins on this host).
- UNVERIFIED: behaviour on Windows/macOS filesystems (the `state-shapes` symlink fixture and
  the `120000` materialisation path are POSIX-only by construction; out of scope for the
  Linux fleet).
- No pacman transaction run; no tool installed (nothing was needed). Disk guard read before
  the runs: `/fast/scratch/hyaku` 28% used, 582.3G free.

## Findings

- **F2 (MED)** — `.ufo/waves/round-56/count-c1.py:178`, `count-c2.py:145`,
  `controls/controls.py:70`, and the contract's replay commands at `contract.md:31,52`: the
  hardcoded `/home/vgpnk` default is the only resolution when `--repo` is omitted (which the
  contract does), so off-host replay exits 2 and same-host replay silently measures the wrong
  checkout.
- **F1 (MED)** — `.ufo/waves/round-56/count-c1.py:50-51` and `count-c2.py:50-51` (plus every
  other `text=True` git call): locale-dependent decode of non-ASCII `corpus/SOURCES.md`
  aborts with empty stdout and EXIT=1 under coercion-disabled ASCII locales, indistinguishable
  from a graded `unmet`.
- **F3 (LOW)** — `tools/mori-driver-liveness.py:67,251-262`: `abspath` instead of `realpath`
  makes symlinked invocation skip 11 of 13 selftest cases while exiting 0.
- **F4 (LOW)** — `.ufo/waves/round-56/evidence/freeze-sha256.txt:7-8,11-12`: `sha256sum -c`
  fails from the repo root (6 unreadable) and from the receipt's own directory (2 unreadable);
  pins themselves verified correct against the counters' constants.
- **F5 (LOW)** — `.ufo/waves/round-56/count-c1.py:124`, `count-c2.py:77`,
  `controls/controls.py:73`: `mkdtemp` without cleanup; five scratch trees left behind.
- **F6 (LOW, informational)** — `tools/mori-driver-liveness.py:470-472`: default fleet root
  is `dirname(repo)`; outside the fleet-root layout the no-arg run reports
  `DRIVER_LIVENESS_UNAVAILABLE` rc 2 (loud, cwd/arg-honouring).
- **Non-finding (falsified)** — §7 item 4 (“writes under `/tmp` regardless of `TMPDIR`”) does
  not reproduce: every temp allocation passes `dir=os.environ.get("TMPDIR") or None`
  (`count-c1.py:124`, `count-c2.py:77`, `controls.py:73`, `tools/mori-driver-liveness.py:352`,
  `tools/mori-vote-bind.py:332,363`); `TMPDIR` at a nonexistent path fails loudly and never
  falls back to `/tmp`; the only literal `/tmp` is prose at `tools/mori-vote-bind.py:54`.
