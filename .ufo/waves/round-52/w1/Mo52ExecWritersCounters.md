# Mo52ExecWritersCounters — round-48/49 `count-c1.py` write scope, and the successor-freeze design

Seat: Mo52ExecWritersCounters (leaf executor, round 52 wave w1). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering lane tip in the contract: `4f266ef2`; data commit scored below: `8524904adb25e44f24d9f25aac7eae909625c18c`.
Lane HEAD when this seat started: `075436b1346ca659afb8be7a46f0e67e4170aa83` (wave-spec commit, after the data commit).
Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ExecWritersCounters/` (one `git clone --shared` of the lane checked out at `8524904`,
`TMPDIR` inside it; removed at the end of this seat). Disk guard before the heavy runs:
`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → rc 0, `/fast/scratch/hyaku` 25 % use, 608.1G free.
No tool was installed or upgraded.

Purpose: the same inventory as the in-lane-writer sweep, for the two counters the round-51 closure §5 item 8 names —
`.ufo/waves/round-48/count-c1.py` and `.ufo/waves/round-49/count-c1.py`, both of which default `--scratch` to
`<repo>/.scratch` — plus the fenced successor-freeze design that item 6/8 routes.

## 1. What was run (literal commands, outputs, exit codes)

All runs used the clone as both the measured repo and the cwd, so the path arithmetic the counters use
(`<repo> = lane` when the file is executed from the lane) is exercised without writing into the lane.
The clone's `master` ref was moved to the data commit (`git -C <clone> update-ref refs/heads/master 8524904…`) so that
the round-49 counter's default `--rev master` measures `8524904`; the clone is scratch and this mutation is disclosed here.

| # | command (cwd = `<scratch>/clone`, `TMPDIR=<scratch>/tmp`) | rc | output |
|---|---|---|---|
| 1 | `git clone -q --shared /home/vgpnk/Projects/shokunin/mori-shokunin clone` && `git -C clone checkout -q 8524904…` && `git -C clone update-ref refs/heads/master 8524904…` | 0 | `git rev-parse --show-toplevel` → `<scratch>/clone`; `du -sh` 334M |
| 2 | `python3 .ufo/waves/round-48/count-c1.py --selftest` | 0 | 34 `PASS` lines, last `C1_SELFTEST pass=34 fail=0`, wall 1s |
| 3 | `python3 .ufo/waves/round-49/count-c1.py --selftest` | 0 | 44 `PASS` lines, last `C1_SELFTEST pass=44 fail=0`, wall 0s |
| 4 | `python3 .ufo/waves/round-48/count-c1.py --tool tools/mori-pin-check.py` (no `--repo`, no `--scratch`, no `--rev`) | 0 | `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=8524904adb25e44f24d9f25aac7eae909625c18c`, wall 349s |
| 5 | `python3 .ufo/waves/round-49/count-c1.py --tool tools/mori-pin-check.py` (no `--repo`, no `--scratch`, no `--rev`) | 1 | `C1=unmet junk_met=1 honest_unmet=0 real=met errors=0 variants=26 rev=8524904…`, with `variant name=N1 expect=unmet got=met rc=0`; all 25 other variants as expected; wall 617s |
| 6 | `python3 n1-probe.py` (applies the frozen round-49 `v_n1` edit to `SKILL.md` at `8524904` and runs both pin-check versions with the counter's own argv) | 0 | see §5 |

Both self-test tallies equal the tallies pinned in `SKILL.md` for those rows (`SKILL.md:971` → `pass=34 fail=0`,
`SKILL.md:1009` → `pass=44 fail=0`), so those two pins are live and correct at `8524904`.

## 2. Inventory — the same fields as the in-lane-writer sweep

| field | `.ufo/waves/round-48/count-c1.py` | `.ufo/waves/round-49/count-c1.py` |
|---|---|---|
| frozen sha256 | `7a2a6aa09b923ef8521a1182fb1bc11f4f92ed7450e9eba86882e454284e4b97` (`.ufo/waves/round-48/evidence/freeze-sha256.txt:1`) | `3c262a15ae28adffa63f6646d5ec15498d1a4c735dbc3c38f68af16afc616b6d` (`.ufo/waves/round-49/evidence/freeze-sha256.txt:2`) |
| bytes at `8524904`, at lane HEAD, and in the lane worktree | all three equal the manifest (no in-place drift) | all three equal the manifest (no in-place drift) |
| default repo | `--repo` else `dirname^4(__file__)` (`:284`) — the lane root when the file runs from the lane | `--repo` else `LANE` (`:324`), `LANE = dirname^3(HERE)` (`:53`) |
| default revision | `HEAD` (`:273`) | `master` (`:313`) |
| default scratch | `tempfile.mkdtemp(prefix="c1-", dir=<repo>/.scratch)` (`:292`) | same (`:332`) |
| refusal of an in-repo scratch | none (no `commonpath`/`inside the repo` test anywhere in the file) | none |
| cleanup of the default scratch | none — `main()` never removes it | none |
| what a default run leaves in the measured tree | `<repo>/.scratch/c1-<8 chars>/` with 12 `variant-*.md` copies of `SKILL.md` and 13 empty `c1-<name>-*` child dirs | `<repo>/.scratch/c1-<8 chars>/` with 26 staged `s-*.md` copies, 26 empty `t-*` dirs, and 2 throwaway fixture git repos (`w-*`), ~95 files |
| side effect of importing | none | imports the round-48 counter by path (`:54-56`) → writes `<repo>/.ufo/waves/round-48/__pycache__/count-c1.cpython-314.pyc` unless `PYTHONDONTWRITEBYTECODE` is set |
| docstring claim about writing | `:30` "Read-only over git; the tool under test writes only inside `--scratch`" — true of the child, silent about the counter's own default | `:39` "…the lane repo is only read." — **false as written**: the counter's own default scratch and the import's bytecode cache both land inside the measured repo |
| visibility of those writes | `<repo>/.gitignore:5 .scratch/` and `:3 __pycache__/` hide them from `git status --porcelain`; `git status --porcelain --ignored --untracked-files=all` lists every one | same |
| SKILL.md row | `:971`, write-scope cell "the tool under test writes only under `--scratch`" (true of the child only) | `:1009`, same cell |

Measured residue in the clone after runs 4 and 5:

```
$ ls -d <clone>/.scratch/c1-*
<clone>/.scratch/c1-3pnz7ljo      # round-48 default run
<clone>/.scratch/c1-a8d0z1d0      # round-49 default run
$ for d in …; do echo "$d files=$(find $d -type f | wc -l) size=$(du -sh $d | cut -f1)"; done
…/c1-3pnz7ljo files=12 size=2.2M
…/c1-a8d0z1d0 files=95 size=4.6M
$ git -C <clone> status --porcelain --untracked-files=all | wc -l
0
$ git -C <clone> status --porcelain --ignored --untracked-files=all | grep -c '\.scratch/c1-'
38
$ git -C <clone> status --porcelain --ignored --untracked-files=all | grep -v '\.scratch/' | head -2
!! .ufo/waves/round-48/__pycache__/count-c1.cpython-314.pyc
!! .ufo/waves/round-49/__pycache__/count-c1.cpython-314.pyc
```

A control probe in the same clone (`mkdir .scratch/probe-mo52; touch .scratch/probe-mo52/a.txt`) gave
`git check-ignore -v` → `.gitignore:5:.scratch/`, `--porcelain` silent, `--ignored` → `!! .scratch/probe-mo52/a.txt`,
so the invisibility is the ignore rule, not the tracked `.scratch` content (the clone carries the same 225 tracked
`.scratch` files the lane does).

Lane-side context for that: `git -C <lane> ls-files .scratch | wc -l` → **225** tracked files under `.scratch/`,
added by round-41 commit `aa161e99` ("…round22 strays"); `.gitignore:5` still ignores the directory. Round 41 already
committed in-lane scratch residue once, which is the same hazard this inventory is about.

## 3. Lane status before and after

| reading | before (21:15 -03) | after (21:37 -03) |
|---|---|---|
| `git -C <lane> rev-parse HEAD` | `075436b1346ca659afb8be7a46f0e67e4170aa83` | `075436b1346ca659afb8be7a46f0e67e4170aa83` |
| `scripts/hyaku/jj-lane.sh state <lane>` | `branch=master local=remote=075436b… ahead=0 behind=0 head=detached tracked=0 untracked=29` | `… tracked=8 untracked=72` |
| `git status --porcelain --untracked-files=all \| wc -l` | 28 | 80 |
| `git status --porcelain --ignored --untracked-files=all \| wc -l` | 10335 | 10409 |
| entries under `.scratch/` | 0 | 0 |
| `stat -c %y <lane>/.scratch` | `2026-10-26 10:53:54` | `2026-10-26 10:53:54` (unchanged) |
| `stat -c %y` of `round-48/__pycache__`, `round-49/__pycache__` | `2026-10-25 18:32:45`, `2026-10-25 21:43:07` | unchanged |
| sha256 of the two counters in the worktree | `7a2a6aa0…`, `3c262a15…` | unchanged |

The lane's porcelain/ignored counts grew between the two readings; the growth is sibling wave seats writing their own
reports and readiness files (`w1/Mo52CritC1Scope.md`, `w1.ready.partial`, …), not this seat: `.scratch` mtime, both
`__pycache__` mtimes, the two counter digests and the `.scratch` entry count are unchanged, and every command in §1 ran
with `cwd = <scratch>/clone`. So a default run of either counter is lane-neutral **when pointed at a clone**, and
lane-writing **when pointed at the lane** — which is exactly what the default does when the counter is executed from
the lane, because both derive `repo` from their own file location.

## 4. The measured result that matters for the design: the frozen round-49 counter reads `C1=unmet` today

Run 5, literal tail:

```
variant name=J1 expect=unmet got=unmet rc=1
…
variant name=H4 expect=met got=met rc=0
variant name=N1 expect=unmet got=met rc=0
variant name=N2 expect=unmet got=unmet rc=1
…
variant name=real expect=met got=met rc=0
variant name=real-opaque expect=met got=met rc=0
C1=unmet junk_met=1 honest_unmet=0 real=met errors=0 variants=26 rev=8524904adb25e44f24d9f25aac7eae909625c18c
exit=1
```

The committed round-49 receipt (`.ufo/waves/round-49/evidence/after-c1-at-tip.txt:13`) records
`variant name=N1 expect=unmet got=unmet rc=1` at rev `64c2d5fc…`. N1 is the frozen edit
`v_n1` (`.ufo/waves/round-49/count-c1.py:80`): it appends one line
`<!-- | r49 html comment | gate | \`python3 tools/mori-pin-check.py --rev <rev>\` | 0/1/2 | \`PIN_CHECK_SELFTEST pass=999 fail=0\` | none | none | mori -->`.

Run 6 isolates the cause. Both pin-check versions, same N1 text, same measured revision `8524904`:

```
=== tool=v5.1@8524904 rc=0
PIN_CHECK=met tally_pins=36 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=26 rev=8524904… baseline=yes env=0 stale=0
=== tool=r49-era@64c2d5fc rc=0
PIN_CHECK=met tally_pins=36 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=26 rev=8524904… baseline=yes
```

So `tools/mori-pin-check.py` did not regress: the *measured document* changed the classification. `hidden_rows`
(`tools/mori-pin-check.py:316-345`) recognises a row shape only as `^\s*\|` (`:329`) or `<tr`/`<td` (`:330`); the N1
line starts with `<!--`, `split_cells` (`:207-212`) returns `None` for it, so it is kind `other`. The only branch that
can flag it is R9b (`:339-341`): a continuation line whose nearest preceding non-blank line starts with `|`. At
`64c2d5fc`, `SKILL.md` ended on a table row (`git show 64c2d5fc:SKILL.md | grep -n . | tail -1` →
`| a journal query's window starts before … |`), so N1 was `hidden`. At `8524904`, `SKILL.md` ends on prose
(`…and the class says why the pin failed, never whether the revision is good.`), so N1 is invisible and the gate reads
`met`. A pinned row inside an HTML comment that follows prose is not a `hidden` row in today's gate.

Consequences, both reportable and neither a change I may make:

- the round-49 claim (`C1=met … variants=26`) is a dated reading of a frozen counter against a *living* document; the
  same frozen bytes read `unmet` at any later tip whose `SKILL.md` tail is prose. The counter cannot be used as a
  standing gate without pinning the document revision, which it does (`rev=`) but does not require to be the tip;
- the surviving junk class above is real for today's `SKILL.md` and belongs in round 53's counter work (routed, not
  fixed here; the round-52 counters and kill rules are frozen).

## 5. Draft — successor-freeze design (fenced; the L1 integrates, nothing here was landed)

Constraint: the closure (round-51 §5 items 6 and 8) forbids editing a file an earlier round froze in place, and allows
"copy-on-change, or record a successor freeze". The instruments frozen here are the two counters (digests in §2) and
the two `evidence/freeze-sha256.txt` manifests; their `SKILL.md` rows are the pins a successor must keep true.

````text
DRAFT — successor for the round-48/49 count-c1.py scratch default (round 53; hygiene, not a claim)

The defect (measured, §2): both counters default `--scratch` to `<repo>/.scratch`, where `<repo>` is the lane when
the file is executed from the lane; neither refuses an in-repo scratch and neither removes what it leaves
(2.2 MB / 12 files for round 48, 4.6 MB / ~95 files plus a bytecode cache for round 49), and `.gitignore:3,5`
hides all of it from plain `git status`.

Moving parts, per counter, for the two options the closure allows:

  A. copy-on-change successor under `.ufo/waves/round-53/`
     new:      1 successor file (both counters, `--counter r48|r49`), 1 SKILL.md row, 1 entry in
               `.ufo/waves/round-53/evidence/freeze-sha256.txt`, 1 self-test receipt
     modified: 0 lane files, 0 frozen bytes, 0 pins, 0 manifests
     pins:     `SKILL.md:971` (`pass=34`) and `:1009` (`pass=44`) stay literally true — measured today at
               8524904 with the frozen bytes (§1 runs 2-3); pin-check's `dropped`/`rebound` keys are untouched
     receipts: every round-48/49 receipt still re-runs to the same numbers

  B. in-place edit of the two frozen counters + a recorded successor freeze
     new:      1-2 successor-freeze records, 1 self-test receipt
     modified: 2 counter files (default scratch, refusal, docstring), and — if the fix is to be tested, which is
               the point — 2 self-test arms, so the pinned tallies move 34→35 and 44→45 and the two SKILL.md
               self-test cells must be edited (or two more superseding rows appended)
     pins:     stay valid only if no arm is added, i.e. only if the fix ships unverified; otherwise both cells move
     receipts: `round-48/evidence/selftest-c1.txt` and `round-49/evidence/selftest-c1.txt` stop reproducing
     records:  both `freeze-sha256.txt` manifests go stale, and both contracts' P-C1 sentence ("the predicate is the
               docstring of count-c1.py verbatim") then names bytes that no longer exist at that path

Answer to the question asked: A keeps SKILL.md pins valid with fewer moving parts *of the kind that can break*.
B is smaller in bytes and larger in consequences: 2 digests, 2 manifests, 2 pin texts, 2 receipts and 2 predicate
sentences change meaning, and the only way to avoid the pin move is to leave the fix untested. A costs one new file
and one new row in total (not two) and changes no committed meaning.

Cheapest option, if the L1 wants nothing new in round 53: leave both files frozen and append a write-scope
supersession row per the round-44/45 precedent (`SKILL.md:193-196`, added by `18fd68b0`, where only the cell was
corrected and the instrument was not touched) stating that the default scratch is in-repo and `--scratch` must be
given. That is a note, not a fix: the armed default stays in the code. It is acceptable only as a stopgap.

Successor spec (draft; the round-53 L1 may adjust names):

  .ufo/waves/round-53/count-c1-hermetic.py
    --counter {r48,r49}            which frozen counter to delegate to (required)
    --tool PATH                    the instrument under test (required, unchanged)
    --rev REV                      required; resolved to a 40-hex sha and printed in the verdict line
                                   (no HEAD/master default: run 5 shows why a symbolic default is a date-dependence)
    --scratch DIR                  optional; default mkdtemp under $TMPDIR
    --selftest                     the successor's own arms, below
  behaviour
    1. resolve repo as the frozen counter does, then refuse (exit 2, `C1_SETUP scratch … lies inside the repo`)
       when the chosen scratch OR $TMPDIR lies inside it — os.path.commonpath, the round-52 pattern
       (`.ufo/waves/round-52/count-c1.py:500-506`), extended to TMPDIR, which round 52 does not check
    2. sys.dont_write_bytecode = True before importing the frozen parent, and TMPDIR plus
       PYTHONDONTWRITEBYTECODE=1 in the child env — kills the round-48/__pycache__ side effect of run 5
    3. sha256 the frozen parent and compare with a literal in the successor; mismatch is exit 2
       (`C1_SETUP frozen parent drift`), never a re-score: copy-on-change means the parent cannot move
    4. delegate the scoring verbatim (import and call the frozen measure()/verdict(), as round 49 already imports
       round 48) and print the frozen `C1=…` line unchanged plus one
       `successor counter=r48|r49 scratch=<abs> frozen=<sha12> rev=<40hex>` line
  selftest arms (no variant runs, so it is seconds not minutes)
    scratch_inside_repo_refused · scratch_outside_accepted · tmpdir_inside_repo_refused ·
    parent_sha_matches · parent_sha_mismatch_is_setup · delegation_argv_records_sha ·
    arrow: prints `C1_HERMETIC_SELFTEST pass=<n> fail=0`
  SKILL.md row (append-only; entry cell must name the successor path first, per pin-check R11/R13)
    | r48/r49 counter scratch guard (r53) | gate |
      `python3 .ufo/waves/round-53/count-c1-hermetic.py --counter r48|r49 --tool PATH --rev REV [--scratch DIR]` |
      0 met · 1 the delegated counter's verdict is unmet · 2 `C1_SETUP` (usage, in-repo scratch or TMPDIR, frozen
      parent drift, unresolvable revision) | `python3 .ufo/waves/round-53/count-c1-hermetic.py --selftest` →
      `C1_HERMETIC_SELFTEST pass=<n> fail=0` | frozen parents 7a2a6aa0… (r48) and 3c262a15… (r49), unedited |
      its own scratch under $TMPDIR only; refuses any scratch or TMPDIR inside the measured repo |
      mori |
    The two old rows stay untouched; if the L1 also wants the old write-scope cells annotated, that is the
    round-44/45 supersession row, appended, never a rewrite.
  freeze: add the successor path + sha256 to `.ufo/waves/round-53/evidence/freeze-sha256.txt`; leave the round-48
    and round-49 manifests exactly as they are.
  receipts: the successor's selftest and one delegated run, each with the literal command line, `--scratch` spelled
    out (closure item 7), scratch removed afterwards.
````

Why this is smaller than in-place in practice: the successor is ~60 lines, imports rather than copies (so the variants
J1–J8/H1–H7 and the N-set stay single-sourced in the frozen parents), and the only new state is one row and one freeze
entry. The in-place route touches exactly the artifacts the lane treats as history.

## 6. Named limits / UNVERIFIED

- The default-run evidence is measured in a clone at `8524904`, not in the lane: running either counter from the lane
  is the hazard under test and was not executed. The path arithmetic (`dirname^4` / `LANE = dirname^3`) and the
  measured clone writes are what establish the lane behaviour.
- The round-49 default run took 617 s and the round-48 default run 349 s on this host with `--jobs 4`; timings are not
  a claim.
- The `.scratch` invisibility is verified for this repo's `.gitignore` and this git; a reader whose clone lacks the
  ignore rule would see the writes in plain porcelain.
- I did not run `tools/mori-pin-check.py` against the lane's `SKILL.md` (no lane write, and the round-52 C1 counter is
  the frozen instrument for that). The two pins in §1 were checked by re-running each counter's own `--selftest`.
- The claim that a pinned row inside an HTML comment following prose is invisible is established for the single N1
  shape and revision `8524904`; I did not enumerate other comment shapes (multi-line comments, comment inside a
  table cell).
- `UNVERIFIED`: whether any historical round-48/49 default run wrote into the lane; the lane's `.scratch` has no
  `c1-*` residue now and no receipt records the `--scratch` used (round-48/49 receipts carry no command line), so the
  claim cannot be settled from the record.

## Findings

- **MED — `.ufo/waves/round-48/count-c1.py:292` and `.ufo/waves/round-49/count-c1.py:332`**: the default `--scratch` is
  `<repo>/.scratch` where `<repo>` is the lane when executed from the lane, there is no in-repo refusal, and the
  scratch is never removed; measured residue 2.2 MB / 12 files (r48) and 4.6 MB / ~95 files (r49). Already routed as
  round-51 closure §5 item 8; the fix belongs in the copy-on-change successor (§5 draft).
- **MED — `tools/mori-pin-check.py:316-345` (`hidden_rows`)**: a pinned row written as an HTML comment is `hidden`
  only when its nearest preceding non-blank line is a table row (R9b); after prose it is invisible and the gate reads
  `met` (N1 at `8524904`, both v5.1 and the round-49-era tool). Routed to round 53 as a counter defect; no change made
  here.
- **MED — `.ufo/waves/round-49/count-c1.py` (frozen)**: re-run at `8524904` it reads `C1=unmet junk_met=1` (N1) where
  its committed receipt at `64c2d5fc` reads met; the frozen counter is date-dependent on the measured document's tail
  and cannot be a standing gate at a later tip. A successor must pin the revision and must not inherit a
  document-tail-sensitive arm (§5 items 1 and 4).
- **LOW — `.ufo/waves/round-49/count-c1.py:54-56`**: importing the round-48 counter writes
  `<repo>/.ufo/waves/round-48/__pycache__/count-c1.cpython-314.pyc` inside the measured tree unless
  `PYTHONDONTWRITEBYTECODE` is set; measured in the clone. The successor sets `sys.dont_write_bytecode` (§5 item 2).
- **LOW — `.ufo/waves/round-49/count-c1.py:39`**: the docstring says "the lane repo is only read"; the counter's own
  default scratch and the import's bytecode cache contradict it. The SKILL.md write-scope cells (`:971`, `:1009`) are
  narrower and true (they describe the tool under test only).
- **LOW — lane `.scratch/` is tracked (225 files, round-41 commit `aa161e99`) while `.gitignore:5` ignores it**: a
  successor's scratch can never be committed under the same name without ambiguity, and the tracked files make
  `.scratch` look like history. Design note only; no lane change proposed here.
- **LOW — revision defaults differ** (`HEAD` at `round-48/count-c1.py:273` vs `master` at `round-49/count-c1.py:313`):
  the same invocation measures different revisions depending on the checkout state; the successor requires `--rev` and
  prints the resolved 40-hex sha (§5).
