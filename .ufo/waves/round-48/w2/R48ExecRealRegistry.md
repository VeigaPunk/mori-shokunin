# R48ExecRealRegistry — v3 pin reconciler on the real registry at the landed tip, and on the entering registry (round 48, w2)

**Attacked:** the v3 pin reconciler (`tools/mori-pin-check.py` at the landed tip
`e4dfff32d4f97c7ef250e9a7538fa75d4f284492`, blob sha256 `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`)
against (A) the **real registry** `SKILL.md` at that same tip, and (B) the **entering registry**
`SKILL.md` at `e5dbac05459887d9597ea5d1da0d8e3d024e0d17` fed through `--skill` while the measured tree
stays the landed tip. Frozen flags in both runs: `--min-tally-pins 26
--baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53`.

**Verdict: HOLDS — no break found in the real-registry arm.** Run A is `PIN_CHECK=met`, exit 0, with
**zero** mismatch/unparsed/no_command/dropped/rebound/duplicate/hidden findings across 41 pin lines.
Run B is `PIN_CHECK=unmet`, exit 1, with exactly **two** mismatches and nothing else: the predicted
line-168 stale truncated digest (`c39e5a73…`, no in-tree file carries that sha256 prefix) and one
line-938 tally mismatch that is pure version skew (the entering row pins the v2 self-test tally
`pass=34`, the measured landed tree runs the v3 tool, whose self-test prints `pass=60`). Neither is a
defect in v3's reading of the real registry; the landed tip repaired line 168 and moved line 938's pin
to `pass=60`. Class of the result: *real-registry arm re-measured, entering-registry expectation
confirmed, no new false-green/false-red class exposed by these two runs.*

This seat is a dispatched executor, not a judge: the numbers below are observations, not a verdict on
P-C1 (that is `count-c1.py`'s `C1=` line, measured elsewhere).

## 0. Setup and environment

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git rev-parse HEAD
e4dfff32d4f97c7ef250e9a7538fa75d4f284492
$ git status --porcelain=v1 | grep -v '^?? '   # no modified/staged entries (empty); only untracked files
$ sha256sum tools/mori-pin-check.py
85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1  tools/mori-pin-check.py
$ git show e4dfff32d4f97c7ef250e9a7538fa75d4f284492:tools/mori-pin-check.py | sha256sum
85a89a3b…ffff82e1  -                      # working tree == landed blob
$ git show e5dbac05459887d9597ea5d1da0d8e3d024e0d17:tools/mori-pin-check.py | sha256sum
9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6  -   # entering v2, == freeze control
$ git show e5dbac05…:SKILL.md > .scratch/r48w2-R48ExecRealRegistry/SKILL-entering-e5dbac05.md
$ sha256sum …/SKILL-entering-e5dbac05.md   ;  wc -l
2c9772fe5dc19d35bf6ee15a3ef698915384b11eda686e59aa5d0b9413d6005b   939
$ wc -l SKILL.md
979
```

TMPDIR for both runs: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRealRegistry`.
The tool exports the measured revision with `git archive` into `<repo>/.scratch/pin-check-*` and removes
it in a `finally` (`tools/mori-pin-check.py:685 shutil.rmtree(scratch, ignore_errors=True)`); both runs
here exited through that path (rc 0 and rc 1, no traceback). The shared `<repo>/.scratch` is used by
every concurrent seat: **97** `pin-check-*` directories remain there, **94** of them stamped between
19:30 and 19:50 local (a window that contains my two runs but also other seats' runs), so leftovers
exist from other/killed runs; I did not remove any (they may belong to live seats' runs) and cannot
attribute a specific directory to my two runs. Read-only
git only (`rev-parse`, `show`, `cat-file`, `log`); no git add/commit/checkout/reset, no jj mutation, no
production file edited. The only tracked-tree deltas at report time are untracked files
(`git status --porcelain=v1` shows no ` M`/`A `/`M ` lines; `?? .ufo/waves/round-48/w2/` includes this
report).

Tooling note: `/usr/bin/time` is not installed on this host; timing used the bash `time` keyword with
`TIMEFORMAT`. **No install was performed** — `pacman` transactions are paused host-wide and the missing
`time` binary is not on the task path. Nothing else was installed or upgraded.

## 1. Run A — the real registry at the landed tip (the required arm)

```
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRealRegistry \
  python3 tools/mori-pin-check.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --min-tally-pins 26 \
    --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
```

- **exit code: 0** (`RC=0`; stderr empty).
- **time:** `real 2m1.324s`, `user 27m54.757s`, `sys 16m48.335s` (bash `time`; CPU >> wall because the
  pinned self-tests themselves fan out).
- **output:** 41 `pin …` lines, **all 41 `state=match`** — therefore **no non-match line to paste**.
  Composition: 31 tally pins, 8 digest pins (5 full 64-hex + 3 truncated `hex…`), 2 line-count pins.
- **final line, verbatim:**

```
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
```

Selected lines that carry the two v3-new kinds and the v3 self-pin (full log:
`.scratch/r48w2-R48ExecRealRegistry/real.out`, sha256 `26fd6709f8d61c54b9acbf1ba58a1240ef2302d884aceaf3dad5a9ccab603006`):

```
pin line=168 kind=digest state=match digest=533218a566030fda… file=tools/mori-round14-regressions.py
pin line=184 kind=lines state=match pinned='743 lines' file=tools/mori-gate-registry.py observed=743
pin line=192 kind=digest state=match digest=37fd7c24ff52… file=.ufo/waves/round-45/count-c3.py
pin line=192 kind=digest state=match digest=69bf9b6eb29b… file=.ufo/waves/round-45/fixtures/mutants/count-c3.py
pin line=194 kind=lines state=match pinned='743 lines' file=tools/mori-gate-registry.py observed=743
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=60 fail=0' observed='pass=60 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
pin line=971 kind=tally prefix=C1_SELFTEST state=match pinned='pass=34 fail=0' observed='pass=34 fail=0' rc=0 cmd='python3 .ufo/waves/round-48/count-c1.py --selftest'
pin line=972 kind=tally prefix=C2_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 .ufo/waves/round-48/count-c2.py --selftest'
pin line=973 kind=tally prefix=UNLANDED_SELFTEST state=match pinned='pass=13 fail=0' observed='pass=13 fail=0' rc=0 cmd='python3 tools/mori-unlanded-check.py --selftest'
```

Pinned instruments exercised (31 tally pins bound to **27 distinct command strings** over 19 distinct
prefixes): `C1_SELFTEST` ×5,
`C2_SELFTEST` ×5, `C3_SELFTEST` ×4, `GATE_REGISTRY_SELFTEST` ×2, and one each of `CONFORM`,
`MORI_DISK_RATE`, `MORI_JOB_RUNWAY`, `MORI_OOM_KILLERS`, `MORI_PRESSURE`, `MORI_R41_CALIBRATION`,
`MORI_SILENCE_CASES`, `MORI_SOURCE_DRIFT`, `MORI_SOURCES_APPENDONLY`, `MORI_WAVE_SETTLEMENT`,
`PIN_CHECK`, `R19`, `ROUTED_CHECK`, `ROUTED_R24`, `UNLANDED` — every observed tail equals its pin and
every `fail=0` pin ran rc 0 (the two deliberately-red mutant pins at lines 190/192 pin `fail=1`/`fail=2`
and ran rc 1, matching).

## 2. Run B — the entering registry `e5dbac05` through `--skill`

```
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRealRegistry \
  python3 tools/mori-pin-check.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --min-tally-pins 26 \
    --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 \
    --skill /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRealRegistry/SKILL-entering-e5dbac05.md
```

- **exit code: 1** (`RC=1`; stderr empty).
- **time:** `real 6m10.191s`, `user 23m7.944s`, `sys 12m28.588s`. Wall time is host-load sensitive
  (sibling w2 seats were running concurrently); CPU time is the stable figure.
- **output:** 38 `pin …` lines = 28 tally + 8 digest (5 full + 3 truncated) + 2 line-count; 36 match,
  2 mismatch.
- **every non-match line, verbatim (the complete set):**

```
pin line=168 kind=digest state=mismatch digest=c39e5a73… file=None
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=mismatch pinned='pass=34 fail=0' observed='pass=60 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
```

- **final line, verbatim:**

```
PIN_CHECK=unmet tally_pins=28 digest_pins=8 mismatches=2 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
```

(full log: `.scratch/r48w2-R48ExecRealRegistry/entering.out`, sha256
`a3169b39b90a1b6ad19e18b5ef3b61f74fd8942ebe585cb22b272a83365f1bb6`)

### 2.1 Line 168 — the expected stale truncated digest

`SKILL.md:168` (entering, `r14 regressions` row) carries, in its self-test cell, the truncated digest
`c39e5a73…` described as the "harness SHA". The cell's nearest preceding in-tree path is
`tools/mori-round14-regressions.py`; at the measured revision `e4dfff32` that file hashes
`533218a566030fda…` (Run A line 168 pins exactly that and matches). I confirmed independently that no
file in the landed tree carries the pinned prefix: `git archive e4dfff32 | tar -x` into scratch, then
`find … -type f -exec sha256sum {} +` over **12,187 files** → `grep -c '^c39e5a73'` = **0**,
`grep -c '^533218a5'` = 2 (receipt `.scratch/r48w2-R48ExecRealRegistry/tree-sha256.txt`, sha256
`62cfec24a61d44ca137cf04fb8bb3e76770e5c9b1f357dd63060be1e63c7ee00`). The prefix belongs to the
historical r14 harness blob: `git show 5601d12:tools/mori-round14-regressions.py | sha256sum` and
`git show 0fa5e0d:…` both give `c39e5a7352666d09…`. This is the finding w1 `ExecRealRegistryAudit`
predicted and the landed tip repaired. **This is the expected line-168 mismatch; it is a stale registry
pin at `e5dbac05`, not a v3 false red.**

Emit detail worth recording: the mismatch line prints `file=None` even though a path *was* bound — the
emitter at `tools/mori-pin-check.py:513-518` prints the `hit` (the path whose sha256 matched) rather than
the bound path, so `file=None` means "no bound path whose sha256 starts with this prefix", which here is
the bound-but-wrong case, not the no-path case. `state=mismatch` itself is correct.

### 2.2 Line 938 — version skew, not a registry defect at `e5dbac05`

`SKILL.md:938` at `e5dbac05` pins the reconciler's own self-test tally `PIN_CHECK_SELFTEST pass=34
fail=0`. That pin was true **at the entering revision**: the entering tool blob is v2, sha256
`9832e38c…`, and running that exact blob's self-test gives

```
$ git show e5dbac05…:tools/mori-pin-check.py > .scratch/r48w2-R48ExecRealRegistry/pin_v2_entering.py
$ TMPDIR=…/.scratch/r48w2-R48ExecRealRegistry python3 …/pin_v2_entering.py --selftest | tail -2
PASS cli_bad_rev_rc2  rc=2
PIN_CHECK_SELFTEST pass=34 fail=0
RC=0
```

Run B measures the landed tree (v3, 60 self-test arms), so the observed tail is `pass=60 fail=0` while
the entering registry still pins `34`. This mismatch is an artifact of pairing an entering registry with
a landed tree — the two are not the same revision, and the assignment deliberately asks for that pairing.
The landed registry pins `pass=60` and matches (Run A, line 938).

## 3. Findings inventory (both runs)

| finding class | Run A (landed real registry) | Run B (entering registry via `--skill`) | distinct findings |
|---|---|---|---|
| `mismatch` | 0 | 2 (line 168 stale truncated digest; line 938 version-skew tally) | 2, both explained above |
| `unparsed` | 0 | 0 | none |
| `hidden` | 0 | 0 | none |
| `no_command` | 0 | 0 | none |
| `dropped` | 0 | 0 | none |
| `rebound` | 0 | 0 | none |
| `duplicate` | 0 | 0 | none |
| tally floor (26) | 31 ≥ 26 | 28 ≥ 26 | — |

**No distinct hidden/unparsed/no_command/dropped/rebound/duplicate finding exists in either run.** The
entering registry parses to **55** self-test rows, all `state=ok` — the same 55 rows the w1
`ExecRealRegistryAudit` got from v2's parser, so no table was lost to v3's header rule; the landed
registry parses to **58** rows, all `state=ok` (`parse_registry` re-read in this seat's scratch,
`pin_v3_copy.py`, sha256 `85a89a3b…ffff82e1`).

## 4. Coverage observations (not findings against P-C1)

1. **Pin coverage of the registry is partial by construction.** Run A prints pins for 30 of the 58
   parsed self-test rows; the other **28 rows carry no tally, digest or line-count pin** in their
   self-test cell (prose-only), so `PIN_CHECK=met` says nothing about them. The same 28 rows are
   pin-free at entering (27 of 55 rows carry pins). Pin-free rows at the landed tip: `census`,
   `drift pin`, `r13 regressions`, `r15 regressions`, `r16 regressions`, `r16 context check`,
   `journal window (r16)`, `seat terminal status (r17)`, `r17 seat regressions`, `r17 jj regressions`,
   `misroot sweep (r17)`, `r17 context check`, `r18 retention (C1)`, `r18 freeze-order (C2)`,
   `r18 dispatch ledger (C3)`, `r19 content review (C1)`, `retained-loss audit`,
   `evidence-loss rule comparison`, `retention reconciliation schema-v2 (r23)`, `blind-writer gate
   (r31)`, `source drift (r36)`, `SOURCES append-only (r36)`, `index clean (r36)`,
   `C1 counter challenge arm (r37)`, `content-anchor check (r38)`, `counter conformance (r38)`,
   `fabricated-content check v2 (r39)`, `counter conformance v2 (r39)`. This is the tool's documented
   reading rule (only backticked pins in the self-test cell count), not a regression; it is recorded so
   a reader does not over-read `met` as "all 58 rows re-measured".
2. **Mismatch diagnosability:** as noted in §2.1, a truncated-digest mismatch prints `file=None`
   whether no path was bound or the bound path's digest differs. Correct verdict, weaker evidence
   trail. (Full-digest mismatches print the bound path, `file=<path>`.)
3. The 28 rows are stable across both runs, so the three landed rows (`r48 junk-variant counter (C1)`,
   `r48 quota entry counter (C2)`, `unlanded check (r48)`) are all pin-bearing and all match.
4. **A pinned instrument writes outside the measured tree.** The `CONFORM_SELFTEST` pin (line 911) runs
   `.ufo/waves/round-40/conform.py <rev> --selftest`; that script hardcodes the live lane
   (`conform.py:69` `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`, `:70` `SCRATCH_ROOT =
   os.path.join(LANE, ".ufo", "waves", "round-40", "scratch")`, `:742-743` `mkdtemp(..., dir=SCRATCH_ROOT)`),
   so even when the reconciler exports `--rev` into `.scratch/pin-check-*` and runs with `cwd=<export>`,
   the conform self-test creates its scratch in the **live lane**. Observed: **12** leftover
   `mori-conform-selftest-*` directories with files under the live lane's
   `.ufo/waves/round-40/scratch/` at the moment of the check (the count moves as concurrent seats create
   and clean their own). None carries an mtime inside this seat's run windows
   (Run A 19:35-19:37, Run B 19:38-19:44 local; the leftovers are stamped 18:46 and 19:48 by other
   seats' concurrent runs), so the reconciler's own `--rev` cleanup claim held for these two runs; the
   class of side effect is nevertheless real. `python3 tools/mori-unlanded-check.py --repo . --round 48`
   (read-only, rc 1) reports 30 in-scope paths and **none** of the conform directories, because
   `in_scope` covers only `.ufo/waves/round-48/`, `corpus/`, `tools/` and top-level `*.md`
   (`tools/mori-unlanded-check.py:48-51`) — so the leak is invisible to this round's unlanded gate.
   This is an observation about a pinned instrument, not a v3 rule failure; v3 cannot see writes a
   measured command makes outside the tree it is handed.

## 5. Receipts and constraints

| artifact | path | sha256 |
|---|---|---|
| Run A stdout (41 pin lines + final) | `.scratch/r48w2-R48ExecRealRegistry/real.out` | `26fd6709f8d61c54b9acbf1ba58a1240ef2302d884aceaf3dad5a9ccab603006` |
| Run A timing (stderr of the `time` group) | `.scratch/r48w2-R48ExecRealRegistry/time-real.txt` | — |
| Run B stdout (38 pin lines + final) | `.scratch/r48w2-R48ExecRealRegistry/entering.out` | `a3169b39b90a1b6ad19e18b5ef3b61f74fd8942ebe585cb22b272a83365f1bb6` |
| Run B timing | `.scratch/r48w2-R48ExecRealRegistry/time-entering.txt` | — |
| entering `SKILL.md` copy | `.scratch/r48w2-R48ExecRealRegistry/SKILL-entering-e5dbac05.md` | `2c9772fe5dc19d35bf6ee15a3ef698915384b11eda686e59aa5d0b9413d6005b` |
| v3 tool copy used for `parse_registry` | `.scratch/r48w2-R48ExecRealRegistry/pin_v3_copy.py` | `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1` |
| entering v2 tool copy (self-test check) | `.scratch/r48w2-R48ExecRealRegistry/pin_v2_entering.py` | `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` |
| `mori-unlanded-check.py --repo . --round 48` output (read-only, rc 1, 30 in-scope paths) | `.scratch/r48w2-R48ExecRealRegistry/unlanded.out` | — |
| sha256 of every file in the `e4dfff32` export (12,187 lines) | `.scratch/r48w2-R48ExecRealRegistry/tree-sha256.txt` | `62cfec24a61d44ca137cf04fb8bb3e76770e5c9b1f357dd63060be1e63c7ee00` |

Constraints honored: no production file, tool, SKILL.md, SOURCES.md, corpus, LOG, SCORECARD or frozen
round-48 file edited; only this report plus scratch under
`.scratch/r48w2-R48ExecRealRegistry/`; both lane-tool runs used the lane-root `TMPDIR`; no fleet-repo,
sibling-lane, git-index or jj mutation; no credentials read or copied; no subagents.

## 6. Limits / UNVERIFIED

- I did not run `count-c1.py` (the `C1=` predicate is another seat's arm); this report says only what the
  tool itself printed on the real and entering registries.
- The host was under concurrent w2 load, so the wall-clock numbers are not a stable benchmark; CPU time
  is reported alongside.
- The 28 pin-free rows were enumerated with the tool's own `parse_registry`, but their self-test claims
  were **not** executed by me — UNVERIFIED whether those claims still hold; v3 does not measure them.
- I did not check whether `--skill` paths outside the measured tree are intended to be allowed by the
  spec; I used it exactly as the assignment directed and report the result.
