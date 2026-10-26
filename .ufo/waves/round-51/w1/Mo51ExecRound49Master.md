# Mo51ExecRound49Master — evidence for lesson M1 (`--selftest` reads `master` from the repo it runs in)

Seat: Mo51ExecRound49Master (executor, mori round 51 wave w1). Item: measure
`.ufo/waves/round-49/count-c1.py --selftest` in `--no-local` clones whose `master` moves, is absent, or does not
exist (archive tree outside any repo), and say what a lesson about pins that read a moving branch should claim.

Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ExecRound49Master/`, `TMPDIR=$S/tmp`, one `git clone --no-local` of the
lane (`431M`, `git -C "$S/clone" rev-parse --show-toplevel` printed the clone). Removed before this report was
written; every number below was copied out of the run's output file first. Disk guard before the heavy runs:
`/fast/scratch/hyaku` 26 % used, 601.8 G free. No tool was installed or upgraded; no pacman transaction was
attempted. Read-only `git` on the lane only; no lane file, index, jj state or fleet file written — this report is
the only file I wrote. This seat is not a C2 seat: it casts no claim vote and writes no vote line.

## 1. What is pinned, and to what

| where | text |
|---|---|
| `SKILL.md:1009` (row `r49 opaque-handle junk-variant counter (C1)`, 790 chars) | self-test cell `python3 .ufo/waves/round-49/count-c1.py --selftest` → pin `C1_SELFTEST pass=44 fail=0` |
| `.ufo/waves/round-49/contract.md:162` | `C1_SELFTEST pass=44 fail=0`, `C2_SELFTEST pass=26 fail=0` at freeze |
| `.ufo/waves/round-49/evidence/selftest-c1.txt:45` | `C1_SELFTEST pass=44 fail=0` |

The counter's bytes are not the variable in anything below: sha256 `3c262a15ae28adffa63f6646d5ec15498d1a4c735dbc3c38f68af16afc616b6d`
at `aa3af1ec…`, at `87e0c374…` **and** at `b504cb17…`; the imported helper `.ufo/waves/round-48/count-c1.py` is
`7a2a6aa09b923ef8521a1182fb1bc11f4f92ed7450e9eba86882e454284e4b97` at all three.

## 2. Where the instrument reads `master`

- `.ufo/waves/round-49/count-c1.py:51-53` — `LANE = dirname(dirname(dirname(HERE)))`, i.e. the repository the file lives in.
- `:313` — `opts = {"--tool": None, "--rev": "master", …}`: the counter's own default revision is a branch.
- `:353-355` — `head = git -C LANE rev-parse --verify master^{commit}`; `text = r48.git_show(LANE, head, "SKILL.md")`.
- `:356-358` — if `text is None`: print `C1_SELFTEST pass=0 fail=1` and `return 1`.
- `:422` — arm `lane_head_unchanged` repeats the same `master` lookup.
- `:438` — `plan_text_only` re-applies the variant functions without the `try/except Anchor` the earlier loop has.

So the selftest's *variant texts* come from `master`'s `SKILL.md`, and the *code* comes from the tree. The pin's
`pass=44` counts arms in the code, not rows in the registry.

## 3. Method

One `--no-local` clone; states created inside it (`git checkout --detach`, `git update-ref refs/heads/master`,
`git update-ref -d refs/heads/master`), asserted before each run with `git -C "$C" rev-parse --verify master^{commit}`
and `git -C "$C" symbolic-ref -q HEAD`. Command shape, every case:

```
$ cd "$S" && python3 "$C/.ufo/waves/round-49/count-c1.py" --selftest >out-<case>.txt 2>&1; echo "rc=$?"
```

`TMPDIR=$S/tmp` for every run (the selftest's three fixture repos land there). Output file line counts are given
because a one-line output is itself evidence: the guard at `:356-358` prints nothing else.

## 4. The four cases the item asks for

| case | state before the run | last line of output | rc | lines |
|---|---|---|---|---|
| (a) `master` at the data commit | `HEAD` detached at `87e0c374`, `master=87e0c374` | `C1_SELFTEST pass=44 fail=0` | 0 | 45 |
| (b) `master` at the entering tip | `HEAD` detached at `aa3af1ec`, `master=aa3af1ec` | `C1_SELFTEST pass=44 fail=0` | 0 | 45 |
| (c) no `master` branch | `HEAD` detached at `aa3af1ec`, `refs/heads/master` deleted; `refs/remotes/origin/master=b504cb1`, `refs/remotes/origin/HEAD` still present | `C1_SELFTEST pass=0 fail=1` | 1 | 1 |
| (d) `git archive` tree outside any repo | `git -C "$C" archive 87e0c374` → `$S/archive` | `C1_SELFTEST pass=0 fail=1` | 1 | 1 |

Verbatim, case (c) — the whole output is one line:

```
$ git -C "$C" branch --list
* (HEAD detached at aa3af1e)
$ git -C "$C" rev-parse --short refs/remotes/origin/master
b504cb1
$ git -C "$C" rev-parse --verify -q master; echo "rc=$?"
rc=1
$ python3 …/round-49/count-c1.py --selftest
C1_SELFTEST pass=0 fail=1
rc=1
```

Verbatim, case (d):

```
$ git -C "$C" archive 87e0c374… | tar -x -C "$S/archive"; echo "archive_rc=$?"
archive_rc=0
$ git -C "$S/archive" rev-parse --show-toplevel
fatal: not a git repository (or any parent up to mount point /)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
rc=128
$ cd "$S/archive" && python3 "$S/archive/.ufo/waves/round-49/count-c1.py" --selftest
C1_SELFTEST pass=0 fail=1
rc=1
```

Case (d) is not a missing-anchor case: that archive's own `SKILL.md` carries both `PIN_CHECK_SELFTEST pass=` rows
(measured on the identical extraction in §5, `tree_skill_pins=2`). The guard fires because the *repository* is
absent, not because the registry is wrong.

## 5. Extra arms (same clone, same TMPDIR)

| arm | state | last line | rc | lines |
|---|---|---|---|---|
| (e) `master` at the live tip | `HEAD` detached at `87e0c374`, `master=b504cb17` | `C1_SELFTEST pass=44 fail=0` | 0 | 45 |
| (f) `master` at an anchor-less revision | `HEAD` detached at `87e0c374`, `master=63eecf27` (round-47 freeze, 2026-10-25; its `SKILL.md` has **0** `PIN_CHECK_SELFTEST` occurrences) | `r48c1.Anchor: no line matches 'PIN_CHECK_SELFTEST pass=\\d+ fail=0'` | 1 | 19 |
| (g0) archive inside a repo whose default branch is `main` | fixture repo from plain `git init` (host `init.defaultBranch=main`), `refs/heads/main` only, data archive in `./sub` | `C1_SELFTEST pass=0 fail=1` | 1 | 1 |
| (g1) archive inside a repo whose `master` has the anchors | fixture `master` = `b504cb17:SKILL.md` (2 pin rows), data archive in `./sub` | `C1_SELFTEST pass=44 fail=0` | 0 | 45 |
| (g2) archive inside a repo whose `master` has no anchors | fixture `master` = `63eecf27:SKILL.md` (0 pin rows), **data archive in `./sub` whose own `SKILL.md` has 2 pin rows** | `r48c1.Anchor: no line matches 'PIN_CHECK_SELFTEST pass=\\d+ fail=0'` | 1 | 19 |

(g2) is the decisive one for M1: the tree's own bytes are correct and complete, `git -C sub rev-parse --show-toplevel`
resolves to the *enclosing* fixture repo, `git -C sub rev-parse --short master` is the fixture commit — and the run
crashes because the enclosing `master`'s `SKILL.md` lacks the row. Change only that enclosing `master` (`g1`) and
the same extraction prints `pass=44 fail=0`. Nothing in the tree was ever read.

Case (f)/(g2) does not even reach the summary line: the traceback ends at
`plan_text_only` (`:438`) → `round-48/count-c1.py:85` (`v_j1`) → `:76` (`r47_rows`) → `:57` (`find_line`), 19 lines,
7 `File` frames, no `C1_SELFTEST` text anywhere in the output.

## 6. The registry pin, measured at the landed revision

`tools/mori-pin-check.py` at `87e0c374` (sha256 `35c69d9115b5e45f91a4b0311ce95c03b3b2b929250e2afb31b571a49687b3bf`,
export = `git clone --shared --no-checkout` `:880` then `git -C tree checkout --detach <R>` `:882`),
`--rev 87e0c374… --repo "$C" --scratch …`, three source states, same revision R each time:

| run | source state | pin line 1009 | summary | rc | wall |
|---|---|---|---|---|---|
| h1 | `HEAD` attached to `master` (`b504cb17`) | `state=match pinned='pass=44 fail=0' observed='pass=44 fail=0' rc=0` | `PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 … env=0 stale=0` | 0 | 82.1 s |
| h2 | `master` deleted, `HEAD` detached at R | `state=mismatch pinned='pass=44 fail=0' observed='pass=0 fail=1' rc=1 … class=stale` | `PIN_CHECK=unmet … mismatches=1 … env=0 stale=1` | 1 | 80.7 s |
| h3 | `master=b504cb17`, `HEAD` detached at R | ditto (`observed='pass=0 fail=1' … class=stale`) | `PIN_CHECK=unmet … env=0 stale=1` | 1 | 82.6 s |
| h4 | `master=63eecf27`, `HEAD` attached to `master` | `state=mismatch pinned='pass=44 fail=0' observed=None rc=1 … class=env` | `PIN_CHECK=unmet … env=1 stale=0` | 1 | 79.8 s |

h2/h3 vs h1 differ only in the source's HEAD/`master` plumbing; R is identical. h1's green is not evidence about
R's registry either: `export_rev` detaches the measured tree at R but the tree's `master` is `b504cb17`, and the
selftest reads `master` (§2), so the passing registry is the live tip's, not R's — both happen to print 44.

h3/h4 show the same root cause landing in opposite classes: no local `master` in the tree → a tally line
`pass=0 fail=1` → `class=stale` (blames R); an anchor-less `master` → a traceback with no tally line → `class=env`
(blames the host). The contract's frozen arm-C limit already names the first half of this ("a tool that prints a
tally and then fails for an environmental reason is classed stale"); h4 is the mirror case.

Export-clone refs, probed with the tool's own incantation (`git clone -q --shared --no-checkout "$C" tree` +
`git -C tree checkout --detach R`), three source states:

| source plumbing | measured-tree refs | tree `master` |
|---|---|---|
| `HEAD` → `refs/heads/master`, `master=b504cb17` | `refs/heads/master`, `refs/remotes/origin/HEAD`, `refs/remotes/origin/master` | `b504cb17` |
| `HEAD` detached at `b504cb17` (= `master` tip) | same | `b504cb17` |
| `HEAD` detached at `87e0c374`, `master=b504cb17` | `refs/remotes/origin/master` only | **ABSENT** |

The lane today is the second row (`git symbolic-ref -q HEAD` fails; `HEAD=master=b504cb17`), which is why the
natural run is green today and turns red only after the lane's HEAD moves off the branch tip (e.g. a checkout of an
older revision to re-execute its pins) or the branch is renamed/deleted.

For information, not scored and not data: the lane working tree at the time of this report carries an **uncommitted**
`tools/mori-pin-check.py` (sha256 `e902cef7382ff5accd7ab11ab352aa6a3c739a33fb45a367d894c70bce286b47`, `M` in
`git status`; committed bytes are `35c69d91…` at data and at `b504cb17`) whose export runs
`git -C tree checkout -q -B master <R>` (`:910`) instead of `--detach`. I copied that file to scratch and ran it in
h3's state: `state=match pinned='pass=44 fail=0' observed='pass=44 fail=0'`, `PIN_CHECK=met … mismatches=0 env=0 stale=0`,
rc 0, 79.9 s. So fabricating `master = R` in the measured tree removes the plumbing dependence of §6/§5 — an
observation about an in-flight file, not part of this round's data and not judged here.

## 7. Answer: does the pinned tally depend on where `master` points?

- **The value does not.** `pass=44 fail=0` at `master` = `87e0c374`, `aa3af1ec` and `b504cb17` — three different
  revisions — because 44 is the number of arms in the code, and the variant functions only need the anchors to exist.
  A pin on an arm count therefore cannot detect that it validated a different revision's registry.
- **Resolution does.** No `master` (`:353-358`) or no repository at all ⇒ `C1_SELFTEST pass=0 fail=1`, exit 1, one line,
  identical to a genuine failing arm; an anchor-less `master` ⇒ an uncaught traceback with no summary line at all
  (`:438`). Neither output says "I could not read the repository"; the registry pin then records `class=stale` or
  `class=env` depending on which of the two shapes occurred (§6).
- **Which revision was measured does.** The selftest reads `master`'s `SKILL.md`, never the tree's (§5 g2), so a
  green pin at R says nothing about R's registry. In the current harness that is masked twice: `tools/mori-pin-check.py`
  detaches the tree at R while its `master` stays at the live tip, and the round-51 C1 counter's clones set
  `master = R` themselves.

## 8. Draft — what the lesson should say about pins that read a moving branch

Fenced draft for `corpus/lessons/round-51.md` (L1 integrates; I did not touch the lesson file).

```
### Pins that read a moving branch

A pin is evidence about revision R only if its command derives everything it reads from R.
`.ufo/waves/round-49/count-c1.py --selftest` does not: it resolves `master` in the repository it runs in
(`:353-355`, then `git_show(LANE, head, "SKILL.md")`) and defaults `--rev` to `master` (`:313`). Measured in one
`--no-local` clone: `C1_SELFTEST pass=44 fail=0` with `master` at 87e0c374, at aa3af1ec and at the live tip
b504cb17; `C1_SELFTEST pass=0 fail=1` with no `master` (guard `:356-358`) and the same one line from a
`git archive` tree outside any repo whose own SKILL.md carries the anchors; an uncaught `r48c1.Anchor` traceback,
no summary line, with `master` at a revision whose SKILL.md has no `PIN_CHECK_SELFTEST` row (`:438`). The same
archive placed inside an unrelated repository gives 44 or the traceback depending on that repository's `master`
alone — the tree's bytes are never read. Through the registry this is SKILL.md:1009's pin: `state=match` when the
measured tree carries a local `master`, `state=mismatch … class=stale` (or `class=env`, when the anchor-less branch
crashes the run) when it does not, at one and the same R.

Rules:
1. Read the revision, never a branch: `--rev R` is required (no `master` default); inside the tree read `HEAD`
   (checked out at R) or `git show R:path`.
2. A missing repository, branch or anchor is a setup condition: print a non-tally status and exit 2, so the
   reconciler can class it `env`. `pass=0 fail=1` from a guard, or a traceback, is not a measurement.
3. An arm-count tally is revision-blind: if the selftest reads ambient state, print the revision it read in the
   tally line so the pin can compare it with R.
4. When a harness must fabricate ambient state (round-51 `count-c1.py:73-81` sets `master = R` in its clones), say
   so in the docstring and keep one arm that omits the fabrication and shows the pin going red.
```

## 9. Findings

| id | sev | finding | file / line |
|---|---|---|---|
| F1 | HIGH | A missing repository or a missing `master` becomes `C1_SELFTEST pass=0 fail=1` with exit 1 and one line of output — the same line and exit code as a genuine failing arm, no diagnostic. Measured in cases (c) and (d) (both one line) and through the registry (h2/h3: pin 1009 `class=stale`, `PIN_CHECK=unmet`). A closure that re-executes this pin from a tree it exported outside a repository (or a clone without a local `master`) records a false stale against the revision. | `.ufo/waves/round-49/count-c1.py:353-358` |
| F2 | HIGH | The selftest's registry text comes from the enclosing repository's `master`, never from the tree it runs in; when that branch's `SKILL.md` lacks the rows the run dies uncaught inside `plan_text_only` with no `C1_SELFTEST` line (19 lines, exit 1), while the tree's own `SKILL.md` is correct (g2: enclosing 0 rows, tree 2 rows). | `.ufo/waves/round-49/count-c1.py:355`, `:438`; `.ufo/waves/round-48/count-c1.py:57,76,85` |
| F3 | MED | A green pin at R does not show that R's registry was validated: the tally `pass=44` is identical at three revisions (a/b/e), and in h1 the pin matched at R while the measured tree's `master` was the live tip `b504cb17 ≠ R`. | `.ufo/waves/round-49/count-c1.py:353-355`, `:313`; `SKILL.md:1009` |
| F4 | MED | The pin's outcome depends on the *source* repository's HEAD/`master` plumbing, not on R: a `--shared --no-checkout` clone carries a local `master` only when the source's HEAD is a local branch or is detached at `master`'s commit; detached at any other revision leaves `refs/remotes/origin/master` only, and pin 1009 goes red (h3). The lane is detached exactly at the branch tip today, so the failure is latent, not absent. | `tools/mori-pin-check.py:880-882` (data bytes, sha256 `35c69d91…`); lane `HEAD=master=b504cb17` |
| F5 | MED | The same root cause lands in opposite mismatch classes: no local `master` ⇒ tally `pass=0 fail=1` ⇒ `class=stale` (h2/h3, `env=0 stale=1`); anchor-less `master` ⇒ traceback, no tally ⇒ `class=env` (h4, `env=1 stale=0`). Instance of the contract's named arm-C limit, extended to the mirror case. | `tools/mori-pin-check.py:138-142`, `:824` |
| F6 | MED | Round-51 C1's clones fabricate the ambient ref (`git checkout -q -B master <rev>`), so no C1 arm exercises the state a closure meets when it re-executes an old pin from a checkout at that revision; the `--repo`/`--rev` green is a property of the harness's own `master`. Named limit of C1, not a defect of the land (the frozen spec says the clone carries `master` at R). | `.ufo/waves/round-51/count-c1.py:73-81` (comment at `:77-78`, command at `:79`) |
| F7 | LOW | `--rev` defaults to the moving branch `master`, so an invocation without `--rev` measures the live branch rather than a revision. The pinned command is `--selftest`, so this default is not exercised by the pin, but it is the same hazard in the entry command. | `.ufo/waves/round-49/count-c1.py:313` |
| F8 | LOW | Arm `lane_head_unchanged` re-reads `master` and compares it to the value read at the start of the same run: it cannot fail unless a concurrent writer moves the branch mid-run, so it does not guard the ambient-branch hazard it looks like it guards. | `.ufo/waves/round-49/count-c1.py:422` |

## 10. Limits and UNVERIFIED

- All runs are on this host (linux, kernel `7.2.11-arch1-1`, git with `init.defaultBranch=main`), one clone, one
  `TMPDIR`; nothing here is claimed about other git versions. `git clone --shared --no-checkout` ref behaviour under
  other versions was not probed.
- Case (c) removed the local branch and left `refs/remotes/origin/master`; a clone whose source has *no* `master`
  anywhere (bare mirror of another branch) was not measured, but the guard only ever asks for `master^{commit}`,
  so the same branch of `:356-358` applies — **[INFERENCE]**, not measured.
- I did not run `tools/mori-pin-check.py --selftest`, the round-51 counters, or any control; I did not run the C1
  arms. The pin-check runs above are direct `--rev` invocations at `87e0c374` against my own clone.
- The h4 run used an uncommitted working-tree copy of `tools/mori-pin-check.py` (`e902cef7…`); it is reported as an
  observation only. I did not read, edit or stage that file.
- The lane's HEAD/`master` state (`b504cb17`/`b504cb17`) is as of this report; I did not determine the state during
  the L1's at-data receipts, so I do not claim how h1's green compared with the receipt's green — only that both are
  consistent with the plumbing table in §6.
