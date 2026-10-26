# Mo51ConnCrossClaim — cross-claim pattern finding: the "where it runs" class

Seat: Mo51ConnCrossClaim (leaf connector, cross-claim pattern finding).
Round: 51, wave w1. Lane: mori-shokunin.

Scope per the seat spec: read `round-51/contract.md`, `count-c1.py`, `count-c2.py`, and the
`## Mistakes` tables of `corpus/lessons/round-46.md` – `round-50.md` plus their verifier spot-checks,
and answer: is there a shared class behind C1 (an instrument's result depending on where it runs) and
the earlier rounds' failures (counter setup errors under load r47, off-host pin failure in the
2026-10-26 reflection, `/tmp` residue)?

## 1. Method and evidence read

All readings are from committed bytes; nothing was run on the host. The frozen counters were not
executed (leaf seat; the C1 counter clones, kills and bubblewraps — detection and report only). Every
claim below cites a file:line or a committed receipt.

- `round-51/contract.md` (C1 arms A–D, control table, routed defect 1, named limits).
- `round-51/count-c1.py` (docstring + arms; `git clone --no-local` fixtures, bwrap arm).
- `round-51/count-c2.py` (docstring; entailment arm).
- `round-51/evidence/control-c1-do-nothing.txt`, `control-c1-scratch-only.txt`,
  `control-c1-conform-only.txt`, `c1-at-data.txt`.
- `git diff aa3af1ec..87e0c374` for `tools/mori-pin-check.py` and `.ufo/waves/round-40/conform.py`
  (read-only; observed).
- `corpus/lessons/round-46.md` … `round-50.md` mistakes tables, and the five verifier spot-checks
  (`round-46-verifier-spotcheck.md` … `round-50-verifier-spotcheck.md`).
- `considerthese/2026-10-26.md` (the reflection).
- `corpus/QUALITY.md` criteria 123, 125–128, 133, 136.
- `.ufo/waves/round-50/a2w1/Mo50bExecReexecR47.md` (the r47 re-execution that found the load
  transient).

## 2. The shared class

Yes. All four cited failures are one class: **context-coupled execution — an instrument's verdict is a
function of its ambient execution context (enclosing repository/git reach, working-tree path, scratch
location, host, concurrency state), not only of the bytes it measures.** Each instrument embeds an
implicit assumption about *where* it runs; a different context silently falsifies the assumption and
the verdict changes with no change to the measured object. Four observed manifestations:

| facet | mechanism | evidence |
|---|---|---|
| (a) enclosing-repo coupling | the measured tree sits inside the repo the pins read, so `git -C <tree>` resolves to the enclosing repo | C1 do-nothing vs scratch-only controls |
| (b) baked-in host path | an instrument hardcodes the lane path, so the same bytes differ host vs off-host | reflection lesson 1; C1 arm B |
| (c) shared/fixed scratch inside the measured tree | two runs of one instrument race on one path; one flaky exit flips a verdict | r47 conform.py rc=2 under load; r49 M6 |
| (d) ambient-default scratch (`/tmp`) | scratch/evidence chosen from the world-writable shared default instead of an isolated per-run root; residue outlives the run and contaminates later verification | r12 M9, r15–r24 /tmp rows |

## 3. Recurrence table

| instance | facet | what was observed (committed evidence) | criterion that should have caught it | why it did not |
|---|---|---|---|---|
| r51 C1, entering tip (pre-data controls) | (a), (c) | `control-c1-do-nothing.txt`: `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 …`, first residue path `!! .scratch/pin-check-uphozg94/tree/.gitignore` — v4's `--rev` export lives under `<repo>/.scratch` (contract: `tools/mori-pin-check.py:884-887`), so a SIGKILLed run pollutes the repo it reads. `control-c1-scratch-only.txt`: moving the export out of the repo changes the mismatch count `reloc_mismatch=1 → 3` (three git-reading pins lose the enclosing repo's object store: `round-49/count-c1.py` reads the `master` branch, `tools/mori-round19-regressions.py` and `conform.py` run `git` in the tree). `control-c1-conform-only.txt`: path fix alone leaves `kill_residue=12478` | "a pinned instrument's verdict is invariant under where its tree sits (inside vs outside the repo it reads), and tools never write their export/scratch under the tree they measure" — the invariant now realized by v5 (`git clone --shared` + `--scratch`; docstring "never `<repo>`") | Known since r49: `round-49-verifier-spotcheck.md` §5 item 1 named both files and routed them ("re-executions are not hermetic, D-d"); r50 carried it again (routed defect 4). Routing ≠ enforcement: no gate was keyed to it, so the entering tip still carried v4. The criteria that ran (QUALITY 123/125/126/136) all validate *one run at one place* against a receipt — none compares verdicts across places |
| r47 counter setup error under load (observed in r50 re-execution) | (c) | `Mo50bExecReexecR47.md` §3: the pinned `conform.py --selftest` first ran rc=2 (`conformance setup error`), pin line 911 `observed=None`, `mismatches=2`; rerun reproduced the receipt's `mismatches=1`. Cause: `conform.py:70` `SCRATCH_ROOT = <LANE>/.ufo/waves/round-40/scratch` — selftest scratch written/removed inside the live lane working tree on every measurement; four concurrent sibling `conform.py … --selftest` processes held `mori-conform-selftest-*` dirs at the same moment. A transient rc=2 flips a `PIN_CHECK` `met`→`unmet` | "no pinned instrument writes into the lane working tree it is pinned against; selftest scratch lives under an explicit per-run scratch root" (exactly what r50 D-d named as the fix) | QUALITY 136 (re-execute at the scored revision) runs once, serially, in one location; selftests are single-process; nothing exercised two instances of the same instrument together. The one divergence was smoothed by a rerun ("reports a divergence instead of smoothing it" is the criterion text, but the divergence itself was dispositioned as transient, not as a defect of the instrument) |
| off-host pin failure (2026-10-26 reflection) | (b) | reflection lines 19–24: in a box clone at `950e99be`, `tools/mori-pin-check.py --rev HEAD` reported `mismatches=1` on `SKILL.md:911` `CONFORM_SELFTEST pass=11` with rc=2 `conformance setup error: No such file … /home/vgpnk/…/round-40/count-c8.py`; cause `conform.py:69` hardcodes `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`. "On the host the pin likely holds; off-host it can't." The checker scored "the instrument can't run here" the same as "the pin is stale" (this is what C1 arm C now splits into `class=env`/`class=stale`) | QUALITY 127 ("Instruments carry no absolute host path, and the count of those that do is stated with its scope", `QUALITY.md:1070-1078`) | The criterion's check is a count (`git grep -l -F '/home/vgpnk'`), not a gate, and its own text carves out the very file: "Not covered: older wave instruments (the 10 and the wider 395 are history, not repaired)" — `conform.py` (r40) is excluded by construction; nothing ever ran the pins off-host until the reflection |
| `/tmp` residue (r12–r24, recurring) | (d) | r12 M9: "Scratch (/tmp) evidence cannot be recreated … a `/tmp` path is never evidence"; r15 M5; r16 M7–M14, M21–M27 (verifier `round-16-verifier-spotcheck.md:195-196` checked the named paths, point-in-time); r17 V5/V6; r18 M6; r23 M8; r24 M7 ("seat scratch outside the session scratch root … wrote under `/tmp`; the wave-1 context did not name `/fast/scratch/hyaku/` as the only scratch root") — scratch chosen from the ambient default (`tempfile.gettempdir()` = `/tmp`), shared by every seat, world-writable, and residue outlives the run | "scratch lives under a per-run, per-seat, isolated root, and a run leaves nothing outside it" (the r51 operator directive finally makes this structural: per-seat `/fast/scratch/hyaku/mori-r51/<seat>/`, `TMPDIR` exported, `trap` removal, `/tmp` capped at 50 MB) | The earlier fixes were prose: r24 M7's fix was to *name* the scratch root in the wave context; r16 M2 says it itself: "a context admonition is not runtime prevention". No mechanical post-run stray-write assertion existed; no tool was bound to its granted root |

## 4. Why the existing criteria all missed the class

The lane's calibration criteria are **single-location reproducibility tests**: QUALITY 123/125/126/136
all say "run X once, compare to the committed receipt". They verify that a receipt reproduces *over
time at the same place*; none verifies that a verdict is *invariant across places*. Three specific gaps:

1. QUALITY 136's re-executions ran the frozen counters in `git archive` exports — trees with **no
   repository at all** — so facet (a) (git-object coupling) could never appear, and they ran once,
   serially, so facets (c)/(d) (concurrency, residue) could not appear.
2. QUALITY 127 is a static text count with an explicit historical carve-out; it measures *presence of
   a path literal*, not *behavioral* dependence, and it does not gate.
3. Scratch discipline was prose admonition ("not runtime prevention", stated in r16 and r24) until the
   r51 operator directive.

C1 itself is the first artifact whose *claim surface is the class*: its arms A–D are a run-location
invariance test for one tool (kill residue, bwrap-hidden lane, env/stale classification). The pre-data
controls are in effect the negative controls of the standing check proposed below — the entering tool
fails them, the landed v5 passes them.

## 5. One standing check that would catch the next recurrence

**Run-location invariance sweep**: for every registered instrument row (the same registry `pin-check`
reads), run the pinned command verbatim in at least two differing ambient contexts and require
identical verdicts, plus a cleanliness assertion.

- Context A: `git archive` export into scratch — a tree with **no** repository (facet a).
- Context B: fresh `git clone --shared --no-checkout` + checkout at R, under a **different** scratch
  root and a different `TMPDIR` than A — a tree with **its own** repository, and no enclosing lane
  (facets a, b, c).
- Context C (cheap, optional): B twice concurrently (facet c).
- Assertions: identical exit codes; identical verdict body and last line across A/B (and C); after
  every run, `git status --porcelain --ignored --untracked-files=all` empty in each clone; nothing new
  outside each run's granted scratch root (facet d).
- Run at freeze and at closure; red blocks landing.

Why it catches the next recurrence: it tests the property that failed directly (verdict independent of
run context), on all four axes at once; its negative control already exists in the record — at the
entering tip it would be red on `conform.py` (off-host setup error, reflection lesson 1) and on
pin-check's export-inside-repo (C1 do-nothing/scratch-only receipts). It is a generalization of the two
C1 arms that now verify a single tool, from per-claim to registry-wide and standing. The C1 named
limits note arm B hides only the lane path and proves nothing about another host/user/kernel — the
standing sweep is the natural continuation, and it rides on the existing scratch directive (per-seat
root, `TMPDIR`, disk guard) so it adds no new ambient assumptions.

Residual risk to name (LOW): the landed v5's default scratch is still `tempfile.gettempdir()` when
`--scratch` is not passed, and `conform.py`'s `SCRATCH_ROOT` is now `tempfile.gettempdir()` too —
both are safe only because the harness/counter always pass `--scratch`/`TMPDIR` (and the directive pins
per-seat `TMPDIR`). Any future caller that forgets the explicit root lands back in facet (d). The
standing sweep's cleanliness assertion would catch exactly that.

## 6. Evidence (observed)

```
$ git diff --stat aa3af1ec..87e0c374 -- tools/mori-pin-check.py .ufo/waves/round-40/conform.py SKILL.md SHONEN.md
 .ufo/waves/round-40/conform.py |   7 ++-
 SHONEN.md                      |   2 +-
 SKILL.md                       |   2 +-
 tools/mori-pin-check.py        | 137 ++++++++++++++++++++++++++++++++---------
 4 files changed, 115 insertions(+), 33 deletions(-)
```

```
$ cat .ufo/waves/round-51/evidence/control-c1-do-nothing.txt
kill_residue_first: !! .scratch/pin-check-uphozg94/tree/.gitignore
C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 failed=kill_residue,relocated,classified
exit=1
```

```
$ tail -2 .ufo/waves/round-51/evidence/control-c1-scratch-only.txt
kill_residue_first: -
C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad selftest=pass=114,fail=0 failed=relocated,classified
exit=1
```

```
$ tail -2 .ufo/waves/round-51/evidence/control-c1-conform-only.txt
kill_residue_first: !! .scratch/pin-check-rgdihbt2/tree/.gitignore
C1=unmet kill_residue=12478 relocated=met reloc_mismatch=0 classified=bad selftest=pass=114,fail=0 failed=kill_residue,classified
exit=1
```

```
$ tail -2 .ufo/waves/round-51/evidence/c1-at-data.txt
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=-
exit=0
```

conform.py diff (entering → data): `LANE` changed from a hardcoded host path to
`os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))`;
`SCRATCH_ROOT` changed from `<LANE>/.ufo/waves/round-40/scratch` to `tempfile.gettempdir()`.

pin-check v4→v5 diff: `export_rev()` changed from `git archive` under `<repo>/.scratch` to
`git clone --shared` + `--detach` checkout; `scratch_parent` changed from `os.path.join(repo, ".scratch")`
to `--scratch DIR` or `tempfile.gettempdir()`; mismatch lines now carry `class=env`/`class=stale` and
the summary ends `env=N stale=N`; new selftest arms `v5_class_env_setup_error`,
`v5_class_env_timeout`, `v5_class_stale_tally`, `v5_class_stale_digest`,
`v5_rev_export_outside_repo` (asserts `grpo` has no `.scratch` and the scratch dir is empty after the run).

## 7. Housekeeping

Scratch `/fast/scratch/hyaku/mori-r51/Mo51ConnCrossClaim/` was created for this seat and is removed on
finish (this report contains every citation needed). No tool installed (none needed); no `pacman`
transaction; no fleet/lane mutation; no host reads beyond the committed files above.

## Findings

1. **HIGH** — Non-hermetic instrument class is real and recurring: C1's pre-data controls
   (`round-51/evidence/control-c1-do-nothing.txt`, `control-c1-scratch-only.txt`,
   `control-c1-conform-only.txt`) show the same pin-check bytes yielding `reloc_mismatch` 1 vs 3 and
   `kill_residue` 12547 vs 0 vs 12478 purely by where the export and the scratch sit; the landed v5
   fixes it (`c1-at-data.txt`: 0/0/0/ok). The class spans `tools/mori-pin-check.py` v4 (export under
   `<repo>/.scratch`) and `conform.py` (hardcoded lane path, scratch inside the lane).
2. **HIGH** — The r47 load-sensitive receipt is the same class via shared fixed scratch:
   `Mo50bExecReexecR47.md` §3 observed `conform.py --selftest` rc=2 (transient) flipping line 911 from
   `state=match` to `observed=None`/`mismatches=2`, with four concurrent sibling processes holding
   `mori-conform-selftest-*` dirs; the scrub is `conform.py:70` (`SCRATCH_ROOT` = live lane path).
3. **MED** — Off-host pin failure (reflection `2026-10-26.md:19-24`) is the same class via a baked-in
   host path (`conform.py:69`); it also exposed the classifier gap C1 arm C now closes
   (`class=env` vs `class=stale`).
4. **MED** — `/tmp` residue (r12 M9, r15–r24 rows) is the same class via ambient-default scratch;
   the r51 operator directive is the first structural fix (per-seat root + trap + cap).
5. **MED** — The standing criteria could not catch the class because they are single-location
   reproducibility checks: QUALITY 136 ran in `git archive` exports (no repo) once, serially; QUALITY
   127 is a static count with an explicit historical carve-out ("Not covered: older wave instruments"),
   so `conform.py` was out of scope by construction.
6. **LOW** — v5's and conform.py's new default scratch is `tempfile.gettempdir()`; safety now depends
   on callers always passing `--scratch`/`TMPDIR` (the counter and the directive do). A caller that
   forgets falls back into the `/tmp` facet. Proposed standing check (run-location invariance sweep)
   would catch this and the next recurrence.
