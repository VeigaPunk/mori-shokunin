# Mo51ExecHostPathSweep — relocation sweep beyond the registry

Seat: executor (leaf, no subagents). Lane: mori-shokunin. Data commit
`87e0c374537557754bf71dd68036ded3ddc6699c` (R), entering tip
`aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd`. Round-51 contract read first.

Question this seat answers: beyond the five-row registry that C1 arm B exercises through
`tools/mori-pin-check.py`, which lane instruments still carry an absolute host path or a
lane-path assumption, and which of them survive being re-executed from a clone with the lane
working tree hidden?

Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ExecHostPathSweep/` (S). No tool was installed or
upgraded; nothing needed. `/home/vgpnk/Projects/shokuknow` was not opened.

## 0. Method (exact commands)

Assigned sweep (read-only, at R):

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -nE '/home/vgpnk|Projects/shokunin' \
  87e0c374537557754bf71dd68036ded3ddc6699c -- tools .ufo/waves/round-4*/*.py .ufo/waves/round-5*/*.py
```

-> exit 0; **52 files** carry a hit. 32 of them are fixture or scratch copies
(`round-40/fixtures/`, `round-40/scratch/`, `round-41/fixtures/`, `round-42/fixtures/`,
`round-42/fixtures/mutants/`), 2 are the round-42 assimilation duplicates of two tools
(byte-identical, verified by sha256), leaving **18 distinct lane instruments**.

One clone for the whole seat, built the way the frozen counter builds its own
(`.ufo/waves/round-51/count-c1.py:73-82`) so that `master` is R and not the lane's live tip:

```
git clone -q --no-local --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin $S/clone
git -C $S/clone checkout -q -B master 87e0c374537557754bf71dd68036ded3ddc6699c
git -C $S/clone rev-parse --show-toplevel   # -> /fast/scratch/hyaku/mori-r51/Mo51ExecHostPathSweep/clone
```

Both-ways invocation (identical argv; only the mount namespace differs):

```
# visible
cd $S/clone && TMPDIR=$S/clone/.scratch python3 <path> [<rev>] --selftest
# hidden
cd $S/clone && TMPDIR=$S/clone/.scratch bwrap --bind / / --dev /dev --proc /proc \
    --tmpfs /home/vgpnk/Projects/shokunin/mori-shokunin --chdir $S/clone \
    --setenv TMPDIR $S/clone/.scratch -- python3 <path> [<rev>] --selftest
```

`bubblewrap 0.13.1`, `git 2.56.0`, python3 from the host. Each run capped at 300-900 s.

## 1. Inventory — instruments in scope carrying an absolute host path

| instrument (at R) | hits | kind of host path | `--selftest`? | in SKILL.md registry? |
|---|---|---|---|---|
| `tools/mori-round17-context-check.py` | 8 | **executable default**: `_FLEET_ROOT = "/home/vgpnk/Projects/shokunin"` (line 118) compiled into the clause regexes (lines 261-275); the rest is fixture text (508, 535, 557, 559, 565) | yes, 31 arms | row 177, **no tally pin** |
| `tools/mori-misroot-sweep.py` | 3 | prose only: module docstring (6, 20) and a comment (355) | yes, 12 arms | row 176, **no tally pin** |
| `tools/mori-blind-check.sh` | 1 | selftest **fixture string**: the allow-file heredoc (line 247) lists the absolute lane path as a permitted "Files opened" line | yes, prints `PASS` | row 817, **no tally pin** |
| `.ufo/waves/round-41/conform.py` | 1 | **executable default**: `LANE` (line 66), and `DEFAULT_COUNTERS`/`DEFAULT_CONTRACT`/`HANG_FIXTURE` are all built from it (67-72), so `--repo` does not move them | yes, 14 arms | **no row** |
| `.ufo/waves/round-42/conform.py` | 1 | same shape (line 73, 74-79) | yes, 17 arms | **no row** |
| `.ufo/waves/round-40/count-c8.py` | 1 | **executable default**: `DEFAULT_REPO` (55) and `SCRATCH_ROOT = os.path.join(DEFAULT_REPO, ".ufo/waves/round-39/scratch")` (62) — it writes into the lane | no (`--selftest` is unrecognised) | **no row** |
| `.ufo/waves/round-42/count-c1.py` | 1 | **executable default**: `LANE` (27); also `mkdtemp(dir="/tmp")` (167) | no | **no row** |
| `.ufo/waves/round-42/count-c2.py` | 1 | **executable default**: `LANE` (23) | no | **no row** |
| `.ufo/waves/round-42/count-c3.py` | 1 | **executable default**: `LANE` (20) | no | **no row** |
| `.ufo/waves/round-43/count-c1s.py` | 1 | **executable default**: `LANE` (21); also `mkdtemp(dir="/tmp")` (119) | no | **no row** |
| `.ufo/waves/round-43/count-c2.py` | 1 | **executable default**: `LANE` (13) | no | **no row** |
| `.ufo/waves/round-50/controls/c2-controls.py` | 1 | **executable default**: `STAGED = "/home/vgpnk/Projects/shokuknow/merge/mori"` (20); `LANE` is derived from its own path (17-19) | no | **no row** |
| `.ufo/waves/round-40/gen-wave-spec.py` | 3 | **executable defaults** `LANE` (16) / `FLEET` (17), interpolated into every emitted seat brief | no (spec generator) | **no row** |
| `.ufo/waves/round-48/build-w1-spec.py` | 12 | `L`/`F`/`S` constants, interpolated into emitted briefs | no (spec generator) | **no row** |
| `.ufo/waves/round-48/build-w2-spec.py` | 5 | same | no | **no row** |
| `.ufo/waves/round-49/build-w1-spec.py` | 13 | same | no | **no row** |
| `.ufo/waves/round-50/build-w1-spec.py` | 7 | same | no | **no row** |
| `.ufo/waves/round-50/build-a2w1-spec.py` | 6 | same | no | **no row** |

Executable-default hits (14 files) are the ones that can break off-host replay; the three prose
and fixture hits cannot. The 32 fixture/scratch copies inherit their parent's text and are not
instruments (they are scored as fixtures by their own harnesses).

## 2. Both-ways selftest results

Every instrument above with a real `--selftest` mode, run from the clone at R, lane visible
vs lane `--tmpfs`-hidden. `<rev>` = R where the CLI needs a positional revision.

| instrument | visible | hidden | reading |
|---|---|---|---|
| `tools/mori-blind-check.sh` | rc 0, `PASS` | rc 0, `PASS` | **pass/pass** — the host path is fixture text only |
| `tools/mori-misroot-sweep.py` | rc 0, `{"arms": 12, "finding": "MORI_MISROOT_SELFTEST_OK", …}` | rc 0, identical | **pass/pass** — host path is docstring/comment only |
| `tools/mori-round17-context-check.py` | rc 0, `{"arms": 31, …, "finding_id": "SELFTEST_OK"}` | rc 0, identical | **pass/pass** — but see finding F3: the constant is a code default |
| `.ufo/waves/round-41/conform.py <R> --repo $S/clone` | rc 0, `CONFORM_SELFTEST pass=14 fail=0` | rc 2, `conformance setup error: [Errno 2] No such file or directory: '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/count-c8.py'` | **pass/fail** |
| `.ufo/waves/round-42/conform.py <R> --repo $S/clone` | rc 0, `CONFORM_SELFTEST pass=17 fail=0` | rc 2, same setup error | **pass/fail** |
| `.ufo/waves/round-40/count-c8.py` | rc 2, `count-c8.py: error: unrecognized arguments: --selftest` | rc 2, same | no selftest mode (the `--selftest` grep hits are prose) |
| `.ufo/waves/round-42/count-c1.py` | rc 1, `check pins_present FAIL (.ufo/waves/round-42/evidence/freeze-r42.txt)` / `C1=unmet` | rc 1, same | no selftest mode: argv[0] is the revision, so `--selftest` is read as a revision |
| `.ufo/waves/round-43/count-c1s.py` | rc 2, `usage: count-c1s.py <rev> [--repo LANE]` | rc 2, same | no selftest mode |
| spec generators (`gen-wave-spec.py`, five `build-*-spec.py`), `controls/c2-controls.py`, `count-c2.py`, `count-c3.py`, `count-c2.py` (r43) | — | — | no `--selftest` argparse flag (verified by source: `add_argument("--selftest")` count = 0) |

Without `--repo`, `round-41/conform.py --selftest` and `round-42/conform.py --selftest` both
exit 2 on the visible side too (`conformance setup error: expected str, bytes or os.PathLike
object, not NoneType`, because `rev` defaults to `None`), and under bwrap they exit 2 on the
lane path. So the relocated run only works if the caller supplies **both** `<rev>` and
`--repo <clone>`; even then it dies the moment the lane path is absent.

## 3. Registry pin coverage — what C1 arm B actually exercises

`tools/mori-pin-check.py --rev R --repo $S/clone` (v5, the tool C1 arm B runs), twice:

```
# lane visible, no bwrap           RC=0
PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=87e0c374537557754bf71dd68036ded3ddc6699c baseline=no env=0 stale=0
# under bwrap, lane tmpfs-hidden   RC=0
PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 … env=0 stale=0
```

The two output files are byte-identical (`diff -q` -> identical). So **the 35 tally pins and 8
digest pins all re-execute from the clone with the lane hidden**: every instrument the registry
pins is already relocation-clean, and the sweep finds no new breakage inside arm B's reach.

Two more runs of the same tool at R, for the caller-state question in F2:

```
# --repo = the live lane (attached at master b504cb17, one commit past R)   RC=0
PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 … env=0 stale=0
# --repo = a clone with HEAD detached at R and master = b504cb17            RC=1
PIN_CHECK=unmet tally_pins=35 digest_pins=8 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=87e0c374537557754bf71dd68036ded3ddc6699c baseline=no env=0 stale=1
pin line=1009 kind=tally prefix=C1_SELFTEST state=mismatch pinned='pass=44 fail=0' observed='pass=0 fail=1' rc=1 cmd='python3 .ufo/waves/round-49/count-c1.py --selftest' class=stale
```

The pins land on 34 distinct SKILL.md lines:
`166,168,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,664,665,739,740,741,905,911,912,938,939,971,972,973,1009,1010,1056,1057`.

Against the registry tables:

- main gate table, SKILL.md:164-196 — **33 rows, 17 pinned, 16 unpinned** (unpinned:
  164 census, 165 drift pin, 167 r13 regressions, 169-175 the r15/r16/r17 gates and probes,
  **176 misroot sweep**, **177 r17 context check**, 178-181 the r18/r19 gates);
- rows 545 (retained-loss audit), 546 (evidence-loss rule comparison), 609 (retention
  reconciliation schema-v2), **817 blind-writer gate** — self-test cells exist, no tally or
  digest pin at all.

Consequence for this seat's question: the three lane tools that carry a *real* host-path
default and a working `--selftest` — `tools/mori-round17-context-check.py` (row 177),
`tools/mori-misroot-sweep.py` (row 176), `tools/mori-blind-check.sh` (row 817) — are all in the
registry but none of them carries a pin the reconciler can bind, so **C1 arm B never executes
them**. Their selftest cells read like `python3 tools/mori-misroot-sweep.py --selftest` with no
`<PREFIX>SELFTEST pass=N` token, which is exactly the shape `pin_keys` ignores. The same holds
for the five round-40..43 instruments with absolute `LANE` defaults (round-41/42 `conform.py`,
round-42 `count-c1/c2/c3.py`, round-43 `count-c1s/c2.py`): they have no registry row at all.
`tools/mori-blind-check.sh` prints a bare `PASS`, so even a hand-written pin would need a tally
token the tool does not emit.

## 4. Lane-path assumptions with no absolute path (also swept)

These do not match the assigned grep but are the same defect class, and C1 arm B does cover
them — they are the reason arm B is green:

| instrument | assumption | both ways |
|---|---|---|
| `.ufo/waves/round-40/conform.py:72` | `LANE` derived from `os.path.abspath(__file__)` (the round-51 fix); selftest scratch under `<repo>/.ufo/waves/round-41/scratch` | pinned at row 911, met/met |
| `.ufo/waves/round-49/count-c1.py:353,422` | reads branch `master` from the repo it runs in | pinned at row 1009; met/met here because the caller's HEAD is its `master` tip — see F2 |
| `.ufo/waves/round-44/count-c1.py:323` | `git rev-parse master` in the measured repo | pinned at 183/193, met/met |
| `tools/mori-round17-jj-regressions.py:132` | `BRANCH = "master"` in its own sandboxes | row 175, no pin; not re-run in this seat |
| `.ufo/waves/round-41/conform.py:928`, `.ufo/waves/round-42/conform.py:944` | selftest scratch `os.path.join(repo, ".ufo/waves/round-41|42/scratch")` — writes **inside** the repo it measures, before it validates `rev` | see F1 and §5 incident |
| `.ufo/waves/round-42/count-c1.py:167`, `.ufo/waves/round-43/count-c1s.py:119` | `tempfile.mkdtemp(…, dir="/tmp")` — ignores `TMPDIR` | not selftest-capable |
| `tools/mori-silence-cases.sh:309` | non-selftest branch falls back to `mktemp -d /tmp/…`; the `--selftest` branch correctly requires an absolute `TMPDIR` (303-307) | pinned at row 166, met/met |

## 5. The list the next round should fix

Ordered by blast radius. None of these is a change to a frozen counter, predicate, control or
kill rule; they are instrument and registry-cell repairs.

1. **`.ufo/waves/round-41/conform.py` and `.ufo/waves/round-42/conform.py`** — replace
   `LANE = "/home/vgpnk/…"` with the round-40 recipe (`LANE =
   os.path.dirname×4(os.path.abspath(__file__))`), and build `DEFAULT_COUNTERS`,
   `DEFAULT_CONTRACT`, `HANG_FIXTURE` from the **resolved `--repo`** rather than from the
   module constant. This is the one pair that fails both ways today (`pass=14`/`pass=17`
   visible, rc 2 hidden) and is the direct successor of the defect C1 fixed in pin-check v5.
2. **The selftest scratch root in the same two files** (`round-41:928`, `round-42:944`) — move
   `os.makedirs(os.path.join(repo, ".ufo", "waves", "round-41", "scratch"))` under `TMPDIR`
   and create it **after** argument validation. As written, a bare `--selftest` with no `rev`
   writes into whatever `--repo` resolves to, which defaults to the live lane (observed; §6).
3. **`tools/mori-pin-check.py:873-884` (`export_rev`)** — make the measured tree carry the
   branch the pins read: after `checkout --detach <rev>`, also set `master` (e.g.
   `git -C <tree> update-ref refs/heads/master <full>`) or, if a pin must not read a branch,
   change `.ufo/waves/round-49/count-c1.py` to take its head from `HEAD` instead of `master`.
   Today the verdict depends on the caller's checkout shape and a green pin can read `stale`
   (F2). This is the highest-value item after 1-2 because the reconciler is what a closure runs.
4. **`tools/mori-round17-context-check.py:118`** — make `_FLEET_ROOT` a `--fleet-root` option
   defaulting to the parent of the directory the script lives in, so the clause regexes match
   the fleet root of the host being checked rather than this host's literal.
5. **`.ufo/waves/round-40/count-c8.py:55,62`** — `DEFAULT_REPO` absolute and `SCRATCH_ROOT`
   inside the repo; it is the counter of record that round-41/42 `conform.py` shells out to, so
   it carries the lane path one level deeper. Give it `--repo`/`--scratch` defaults resolved
   from `__file__`/`TMPDIR`.
6. **`.ufo/waves/round-42/count-c1.py`, `count-c2.py`, `count-c3.py`,
   `.ufo/waves/round-43/count-c1s.py`, `count-c2.py`** — `LANE` absolute in all five; the two
   `count-c1*` also hardcode `dir="/tmp"` and so ignore `TMPDIR`. Same `__file__` recipe.
7. **`.ufo/waves/round-50/controls/c2-controls.py:20`** — `STAGED` absolute into
   `/home/vgpnk/Projects/shokuknow`; take it from a flag or from the repo's sibling root.
8. **Registry cells (SKILL.md rows 176, 177, 817)** — add a tally the reconciler can bind, or
   state in the cell that the row is un-pinned. Today the registry implies three gates are
   re-measured and nothing re-measures them; `mori-blind-check.sh` would first have to print a
   `<PREFIX>SELFTEST` line instead of a bare `PASS`.
9. **Spec generators** (`round-40/gen-wave-spec.py`, `round-48/build-w1/w2-spec.py`,
   `round-49/build-w1-spec.py`, `round-50/build-w1-spec.py`, `build-a2w1-spec.py`) — lowest
   priority: absolute `LANE`/`FLEET`/`S` in an emitted seat brief is intentional (seats are
   dispatched on this host), but the generator itself is not replayable elsewhere. Either
   accept and document, or take the roots from argv.

## 6. Incidents and self-disclosure

**I wrote one empty directory into the lane, then removed it.** The first sweep pass ran
`python3 .ufo/waves/round-41/conform.py --selftest` with no revision; that call reaches
`os.makedirs(os.path.join(repo, ".ufo", "waves", "round-41", "scratch"))` before it validates
`rev`, and `repo` defaults to the absolute lane path. It created
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-41/scratch` (empty,
mtime 2026-10-26 19:50:33, i.e. that run; `round-42/scratch` was not created). I removed it with
`rmdir` (which only succeeds on an empty directory; it did), and confirmed
`git -C <lane> status --porcelain -- .ufo/waves/round-41 .ufo/waves/round-42` is empty and the
lane HEAD is still `b504cb1701568a0038aab9d98ec13d28eff801da`. No tracked file, index entry or
jj state was touched. This is the same defect class as finding F1 and is reported, not hidden.

Every later run used `--repo $S/clone`, so the scratch trees landed in my own clone. My scratch
clone was moved to a detached HEAD for one receipt and restored with
`git checkout -q -B master 87e0c374…`; it contains no commit of mine.

The lane's live `master` is one commit past R (`b504cb17` "round-51: wave w1 spec/dispatch"), so
a clone of the lane detached at R — the shape the lane's own round-48 replay recipe produces —
is exactly the caller state that makes F2 fire.

## Findings

**F1 — HIGH — `.ufo/waves/round-41/conform.py:928` and `.ufo/waves/round-42/conform.py:944`.**
Their `--selftest` creates `os.path.join(repo, ".ufo", "waves", "round-41|42", "scratch")`
inside the repository it measures, *before* validating `rev`; `--repo` defaults to the absolute
live-lane constant (lines 66 / 73). A bare `--selftest` invocation therefore writes into the
live lane from any cwd (observed: an empty `round-41/scratch` created at 19:50:33 and removed by
me). This is the residue-inside-the-measured-repo class that C1 arm A closed in pin-check v5,
still live in two instruments that no registry pin re-executes.

**F2 — MED — `tools/mori-pin-check.py:873-884` (`export_rev`) with
`.ufo/waves/round-49/count-c1.py:353,422`.** The measured tree is `git clone --shared
--no-checkout <repo>` plus `checkout --detach <rev>`. Git creates a **local** branch in that
clone only when the source's HEAD coincides with a branch tip; with a detached `--repo` whose
`master` points elsewhere, the measured tree has `refs/remotes/origin/master` but no
`refs/heads/master`. `.ufo/waves/round-49/count-c1.py` reads `master` from the tree it runs in,
so its selftest dies before any arm runs. Reproduced in scratch, one variable changed at a time
(`git clone -q --shared --no-checkout $S/clone probe/t && git -C probe/t checkout -q --detach R`,
then `python3 .ufo/waves/round-49/count-c1.py --selftest`):

| source clone | measured tree's `master` | result |
|---|---|---|
| HEAD detached at R, `master` = R | `87e0c37` | `C1_SELFTEST pass=44 fail=0` |
| HEAD detached at R, `master` = live lane tip `b504cb17` | `(no branch)`, `git rev-parse --verify master^{commit}` -> `fatal: Needed a single revision` | `C1_SELFTEST pass=0 fail=1` |

Whole-tool receipts, all with `--rev R`: `--repo` = my first clone (HEAD detached at R,
`master` = `b504cb17`) gave `PIN_CHECK=unmet … mismatches=1 … stale=1` with
`.ufo/waves/round-49/count-c1.py --selftest` observed `pass=0 fail=1`; `--repo` = the clone with
`master` = R gave `PIN_CHECK=met … env=0 stale=0` (both attached and detached HEAD); `--repo` =
the live lane (attached at `master` = `b504cb17`, one commit past R) gave `PIN_CHECK=met … env=0
stale=0`. C1 arm B is green because the frozen counter's `fresh_clone`
(`.ufo/waves/round-51/count-c1.py:78-81`) runs `checkout -B master <rev>` before measuring, so
its `--repo` HEAD is its `master` tip. A closure that follows the lane's own replay recipe
(`.ufo/waves/round-48/build-w2-spec.py:62`: "in the clone use `git -C \"$D/lane\" checkout -q
--detach {T}`") and then runs `mori-pin-check.py --rev <T> --repo <that clone>` gets a false
red on a pin that is green, classed `stale` rather than `env`.

**F3 — MED — `tools/mori-round17-context-check.py:118`.** `_FLEET_ROOT` is an executable
default compiled into the `no_fleet_root_writes` clause regexes (261-275). It passes both ways
only because the selftest fixtures and the matcher share the same literal; off this host the
gate would accept a spec naming this host's fleet root and reject a correct spec naming another.
Static text validation only, as the registry row already says, but the constant makes the
"correct" text host-specific.

**F4 — MED — SKILL.md rows 176, 177, 817 (misroot sweep, r17 context check, blind-writer
gate).** All three carry a `--selftest` command in the self-test cell and none carries a tally
or digest token, so `pin_keys` binds nothing and C1 arm B never runs them — while they are
exactly the three tools with host-path defaults that do run. 16 of the 33 main-table rows
(164, 165, 167, 169-181) and rows 545, 546, 609, 817 are in the same state. The registry reads
as if these gates are re-measured; they are not.

**F5 — MED — `.ufo/waves/round-41/conform.py:66` and `.ufo/waves/round-42/conform.py:73`.**
`LANE` is absolute and `DEFAULT_COUNTERS`, `DEFAULT_CONTRACT` and `HANG_FIXTURE` are built from
it, so `--repo` moves the tree under test but not the instruments it loads. Measured: relocated
selftest passes with `--repo` (`pass=14` / `pass=17`) and exits 2 under bwrap with
`No such file or directory: '<lane>/.ufo/waves/round-40/count-c8.py'`. Neither file has a
registry row, so nothing re-executes them.

**F6 — LOW — `.ufo/waves/round-40/count-c8.py:55,62`.** `DEFAULT_REPO` absolute plus
`SCRATCH_ROOT` under `<lane>/.ufo/waves/round-39/scratch`: the counter of record that both
`conform.py` versions shell out to still writes inside the lane. No `--selftest` mode, so the
assigned grep's three hits there are prose.

**F7 — LOW — `.ufo/waves/round-42/count-c1.py:167`, `.ufo/waves/round-43/count-c1s.py:119`.**
`tempfile.mkdtemp(prefix=…, dir="/tmp")` ignores `TMPDIR`, against the lane's own scratch
discipline (operator directive 2026-10-25: every temp file under the seat's scratch root).
`.ufo/waves/round-43/count-c1s.py` also returns rc 2 on `--selftest` because argv[0] is its
revision.

**F8 — LOW — `tools/mori-blind-check.sh:247`.** The selftest allow-file heredoc hardcodes the
absolute lane path and `/fast/scratch/hyaku/mori-r31/{report}` as permitted "Files opened"
entries. Harmless today (it is fixture text, and the run is pass/pass both ways) but it pins a
round-31 scratch layout into a standing tool.

**F9 — LOW — `.ufo/waves/round-50/controls/c2-controls.py:20`.** `STAGED` is an absolute
`/home/vgpnk/Projects/shokuknow/merge/mori` path; the control script is otherwise
self-relative. It cannot be replayed by a seat that does not mount that tree.
