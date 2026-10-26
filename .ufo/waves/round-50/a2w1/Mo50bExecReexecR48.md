# Mo50bExecReexecR48 — round 48 re-execution at its scored revision

Seat: executor (leaf), `Mo50bExecReexecR48`. Assignment: `considerthese/2026-10-26.md` suggestion 3 —
re-execute what round 48's closure only evidence-verified. Lane `mori-shokunin`, repo
`/home/vgpnk/Projects/shokunin/mori-shokunin`.

Revisions measured:
- scored revision (round-48 closure "lane HEAD after") `14c5110d65a2f225e7316e1996e92090b9b8e7cb`;
- round-48 freeze/landing `4387cf94` → data `e4dfff32d4f97c7ef250e9a7538fa75d4f284492` (the revision every
  committed round-48 C1/PIN_CHECK receipt names), C2 final receipt `91fbbc2a6a3591e3539c10a378c4f68f65c81aa4`;
- entering revision `e5dbac05459887d9597ea5d1da0d8e3d024e0d17` (the three C1 controls and the C2 do-nothing control).

Sources read first: `considerthese/2026-10-26.md` (suggestion 3), `corpus/lessons/round-48-verifier-spotcheck.md`
(everywhere it writes "Evidence-verified, not executed" / "re-measured"), `LOG.md` §"Round 48", and the frozen
`.ufo/waves/round-48/contract.md`. Scratch `/fast/scratch/hyaku/mori-r50/Mo50bExecReexecR48/` (removed at the end;
everything cited below is quoted in this file).

## Verdict (answers first)

**Round 48 reproduces on this host.** 16 measured runs — both frozen counters, all three frozen C1 controls plus the
C2 do-nothing control, the selftests of all four instruments the round registered, and the round's pin-check gate at
both `e4dfff32` and the scored tip — **all AGREE** with the receipt or pin each must equal. **No DIVERGE, no
CANNOT-RUN.** Six of them are **byte-identical** to the committed receipt file (`cmp -s` clean, sha256 equal), and
the pin-check log at `e4dfff32` is byte-identical to the wave-2 seat's own committed log digest
(`26fd6709…`, quoted in `w2/R48ExecRealRegistry.md:81`).

The gap the closure named ("gate verdicts … are evidence-verified from committed receipts") is therefore **closed
for round 48's instrument set on this host**. Three qualifications, none of which changes a round-48 verdict:

1. one of the 31 tally pins (`SKILL.md:911`, `CONFORM_SELFTEST`) is **not revision-scoped** — its command reads and
   writes the live lane tree through a hardcoded absolute path (strace-proven below, plus two work directories it left
   in the lane, removed by this seat), so its `match` is not evidence about R;
2. no `PIN_CHECK` receipt existed for the **scored tip** before this seat (the two committed PIN_CHECK runs name
   `e4dfff32` / `e5dbac05`); the tip is now measured (`PIN_CHECK=met`, 41/41 `state=match`);
3. the C2 final receipt was measured at `91fbbc2a`, one commit before the tip; the tip run is identical except its
   `rev=` field, and `corpus/`+`tools/` are byte-unchanged between the two (`git diff --stat` empty, entry sha256
   `334df177…` at both).

## Method (exact)

Scratch `/fast/scratch/hyaku/mori-r50/Mo50bExecReexecR48`, `TMPDIR=$S/tmp` exported for every run,
`PYTHONDONTWRITEBYTECODE=1`, one clone (the allowance for this seat):

```
$ git clone --shared -q <lane> /fast/scratch/hyaku/mori-r50/Mo50bExecReexecR48/clone
$ git -C $S/clone rev-parse --show-toplevel
/fast/scratch/hyaku/mori-r50/Mo50bExecReexecR48/clone
$ git -C $S/clone checkout -q --detach 14c5110d65a2f225e7316e1996e92090b9b8e7cb
$ git -C $S/clone rev-parse HEAD
14c5110d65a2f225e7316e1996e92090b9b8e7cb
```

The assignment's "in a `git archive <scored rev>`" needs one correction in practice: both frozen counters shell out
to `git show` / `git rev-parse` (`count-c1.py:git_show`, `count-c2.py`) and `mori-pin-check.py --rev` resolves the
revision through a repository, so a bare archive extraction cannot host them (exit 2, the "unresolvable revision"
class). I therefore materialised **both** and proved them equal:

```
$ git -C <lane> archive 14c5110d65a2f225e7316e1996e92090b9b8e7cb | tar -x -C $S/export     # rc=0
$ diff -r --exclude=.git --exclude=.scratch $S/export $S/clone
DIFF_CLEAN: clone worktree == git archive 14c5110d
```

Frozen instrument bytes at the measured revisions (compare with `.ufo/waves/round-48/evidence/freeze-sha256.txt`):

```
7a2a6aa09b923ef8521a1182fb1bc11f4f92ed7450e9eba86882e454284e4b97  .ufo/waves/round-48/count-c1.py      (= freeze)
0055aed101bd60b1267d160520948b8f412753b38c72b6bda17da841734ee561  .ufo/waves/round-48/count-c2.py      (= freeze)
052a2bf9be032545202ecf5dfae90a50ab2d2001116356493c4005b3a9bc75dd  .ufo/waves/round-48/contract.md      (= freeze)
f93ef57fd977b67fba2068cec21d6161ea2ab14ab083676bf9a78b2cda0d9808  .ufo/waves/round-48/v3-spec.md       (= freeze)
c6f12be844264304fd2007b1f30c4b9a15d4a5414c918588d800021221987b2d  controls/stub-always-met.py          (= freeze)
5b716abc437e1dab2cbf66c304f01e644993f3bc3000345e9f703dcb87c63bf2  controls/stub-always-unmet.py        (= freeze)
9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6  controls/tool-v2-entering.py         (= freeze)
85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1  tools/mori-pin-check.py   (v3; freeze lists the *entering* v2 bytes 9832e38c for this path)
e6695e04026b3da93e0c6406737602a31265970cd5bdfa1ac1d44835ad6a2b85  tools/mori-unlanded-check.py
$ git diff --stat e4dfff32 14c5110d -- tools .ufo/waves/round-48/count-c1.py .ufo/waves/round-48/count-c2.py \
      .ufo/waves/round-48/controls corpus/evidence/sources-r48
(no output — the instrument bytes are identical at the receipt revision and at the scored tip)
```

`SKILL.md` moves +2/−2 between `e4dfff32` and `14c5110d` and the change is prose only — the D7 limit sentence
`closing it as a rule turns four legitimate` → `three legitimate mutant-command rows (190, 191, 192)`. No pin, row
or cell changes; the pinned tally counts (`PIN_CHECK_SELFTEST pass=60`, `UNLANDED_SELFTEST pass=13`,
`C1_SELFTEST pass=34`, `C2_SELFTEST pass=22`) appear exactly once each at the tip.

Isolation: `count-c1.py` was always given an explicit `--scratch` (without it, it would write `<repo>/.scratch`);
`mori-pin-check.py` was given `--repo <scratch clone>`, so its export and its per-command `TMPDIR` landed under the
clone's `.scratch`. Nothing was written to the fleet, the jj state or the git index; no package manager was invoked
(no install was needed). One exception, caused by an instrument and not by this seat's choices, is recorded in F2 and
was cleaned up: while the counters ran, the pinned `SKILL.md:911` command created two
`.ufo/waves/round-40/scratch/mori-conform-selftest-*` work directories **inside the live lane** (that tool's
`SCRATCH_ROOT` is built from its hardcoded `LANE`). This seat removed exactly those two directories
(`rm -rf .ufo/waves/round-40/scratch/mori-conform-selftest-497jhgmw …-6llm2k22`, mtimes 10:11:21 and 10:11:33,
matching the window of this seat's parallel `count-c1` runs; the tool deletes them in its own `finally`, so a sibling
running the same pinned command in the same seconds would have produced an identical transient directory). Afterwards
`git status --porcelain -unormal` listed only the wave's own untracked paths (`.ufo/waves/round-50/a2w1.ready*`,
`.ufo/waves/round-50/a2w1/`), and this report is the only file this seat wrote.

Disk guard before the heavy runs: `/fast/scratch/hyaku` 24 % used, 617.9 G free
(`scripts/hyaku/disk-guard.sh status` rc 0) — no ENOSPC. Environment: Python 3.14.8, git 2.56.0, 32 cores
(load average ~18 from sibling seats; wall times below are therefore upper bounds).

## Table — every run, its receipt, and the verdict

All commands run with cwd `$S/clone`. `<S>` = `/fast/scratch/hyaku/mori-r50/Mo50bExecReexecR48`.

| # | run (revision) | command | printed final line | rc | receipt it must equal | verdict |
|---|---|---|---|---|---|---|
| 1 | count-c1 selftest (`14c5110d`) | `python3 .ufo/waves/round-48/count-c1.py --selftest` | `C1_SELFTEST pass=34 fail=0` | 0 | `evidence/selftest-c1.txt` | **AGREE** (34 `PASS`, 0 `FAIL` lines above it; receipt stores only the final line) |
| 2 | count-c2 selftest (`14c5110d`) | `python3 .ufo/waves/round-48/count-c2.py --selftest` | `C2_SELFTEST pass=22 fail=0` | 0 | `evidence/selftest-c2.txt` | **AGREE** (22 `PASS`, 0 `FAIL`) |
| 3 | pin-check selftest (`14c5110d`) | `python3 tools/mori-pin-check.py --selftest` | `PIN_CHECK_SELFTEST pass=60 fail=0` | 0 | `SKILL.md:938` pin | **AGREE** (60 `PASS`, 0 `FAIL`) |
| 4 | unlanded selftest (`14c5110d`) | `python3 tools/mori-unlanded-check.py --selftest` | `UNLANDED_SELFTEST pass=13 fail=0` | 0 | `SKILL.md:973` pin | **AGREE** (13 `PASS`, 0 `FAIL`) |
| 5 | C1 counter (`e4dfff32`) | `… count-c1.py --tool tools/mori-pin-check.py --rev e4dfff32… --scratch <S>/s1` | `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32…` | 0 | `evidence/after-c1-at-e4dfff32.txt` | **AGREE — byte-identical** (`b51eab85c945…`, `cmp -s` clean) |
| 6 | C1 counter (**scored tip**) | same with `--rev 14c5110d…` and `--scratch <S>/s2` | `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=14c5110d…` | 0 | `evidence/after-c1-at-e4dfff32.txt` (no tip receipt) | **AGREE modulo `rev=`** (only line 14 differs; file `a0c8238078a6…`) |
| 7 | C1 control do-nothing (`e5dbac05`) | `… --tool .ufo/waves/round-48/controls/tool-v2-entering.py --rev e5dbac05… --scratch <S>/s3` | `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12 rev=e5dbac05…` | 1 | `evidence/control-c1-tool-v2-entering.txt` | **AGREE — byte-identical** (`ca32ed7832c3…`) |
| 8 | C1 control always-met (`e5dbac05`) | `… --tool …/controls/stub-always-met.py --rev e5dbac05…` | `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12 rev=e5dbac05…` | 1 | `evidence/control-c1-stub-always-met.txt` | **AGREE — byte-identical** (`ca32ed7832c3…`) |
| 9 | C1 control always-unmet (`e5dbac05`) | `… --tool …/controls/stub-always-unmet.py --rev e5dbac05…` | `C1=unmet junk_met=0 honest_unmet=4 real=unmet errors=0 variants=12 rev=e5dbac05…` | 1 | `evidence/control-c1-stub-always-unmet.txt` | **AGREE — byte-identical** (`7edc923456a6…`) |
| 10 | C2 counter (`e4dfff32`) | `python3 .ufo/waves/round-48/count-c2.py e4dfff32…` | `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=e4dfff32…` | 0 | `evidence/after-c2-at-e4dfff32.txt` | **AGREE — byte-identical** (`ebd5c1276303…`) |
| 11 | C2 counter (`91fbbc2a`) | `… count-c2.py 91fbbc2a…` | same line, `rev=91fbbc2a…` | 0 | `evidence/after-c2-final.txt` | **AGREE — byte-identical** (`07ce0ee0112d…`) |
| 12 | C2 do-nothing control (`e5dbac05`) | `… count-c2.py e5dbac05…` | `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=e5dbac05… failed=entry_absent,pins` | 1 | `evidence/control-c2-donothing.txt` | **AGREE — byte-identical** (`6491877c61dc…`) |
| 13 | C2 counter (**scored tip**) | `… count-c2.py 14c5110d…` | `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=14c5110d…` | 0 | no tip receipt | **AGREE modulo `rev=`** (entry sha256 `334df177…` at `91fbbc2a` and at the tip) |
| 14 | pin-check gate (`e4dfff32`) | `python3 tools/mori-pin-check.py --rev e4dfff32… --repo <S>/clone --min-tally-pins 26 --baseline-rev 2d85e33d…` | `PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32… baseline=yes` | 0 | `w2/R48ExecRealRegistry.md:79` | **AGREE — byte-identical log** (`26fd6709f8d6…`, the digest that report commits at line 81) |
| 15 | pin-check gate (**scored tip**) | same with `--rev 14c5110d…` | `PIN_CHECK=met tally_pins=31 digest_pins=8 … rev=14c5110d… baseline=yes` (41/41 `state=match`) | 0 | no tip receipt | **AGREE modulo `rev=`** (differs from #14 in lines 911, 912 and the final line only; file `3c59bd035cfb…`) |
| 16 | digest / line-count pins | `sha256sum tools/mori-round14-regressions.py .ufo/waves/round-45/count-c3.py .ufo/waves/round-45/fixtures/mutants/count-c3.py`; `git show 5601d12:tools/mori-round14-regressions.py \| sha256sum`; `wc -l < tools/mori-gate-registry.py` | `533218a56603…` / `37fd7c24ff52…` / `69bf9b6eb29b…` / 743; historic blob `c39e5a73…` | 0 | `w2/R48ExecRealRegistry.md:84-89`, closure §2 C1 | **AGREE** (all five values equal) |

Wall times (upper bounds; 32 cores shared with ~15 sibling seats): #5 5 m 20 s, #6 5 m 22 s, #7 5 m 13 s, #8/#9 0.09 s
each, #14 1 m 20 s, #15 1 m 20 s, #3 5.6 s, #4 0.12 s; the four C2 runs were not timed separately (each returned
inside one shell call). The 0.09 s controls are expected: those stubs print their verdict without running the tool
under test.

## Captured receipts (commit-able)

### A. `count-c1.py` at the scored tip — full stdout, `<S>/out/c1-at-tip-14c5110d.txt`, sha256 `a0c8238078a68fe5baa33a3da3eb1e5bab465fce9816020788e652e524fa3373`

```
variant name=J1 expect=unmet got=unmet rc=1
variant name=J2 expect=unmet got=unmet rc=1
variant name=J3 expect=unmet got=unmet rc=1
variant name=J4 expect=unmet got=unmet rc=1
variant name=J5 expect=unmet got=unmet rc=1
variant name=J6 expect=unmet got=unmet rc=1
variant name=J7 expect=unmet got=unmet rc=1
variant name=J8 expect=unmet got=unmet rc=1
variant name=H1 expect=met got=met rc=0
variant name=H2 expect=met got=met rc=0
variant name=H3 expect=met got=met rc=0
variant name=H4 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=14c5110d65a2f225e7316e1996e92090b9b8e7cb
rc=0
```

Byte-identical to `evidence/after-c1-at-e4dfff32.txt` except line 14 (`rev=`), verified with
`diff <mine> <receipt>` (`14c14`).

### B. `count-c2.py` at the scored tip — `<S>/out/c2-at-tip-14c5110d.txt`

```
C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=14c5110d65a2f225e7316e1996e92090b9b8e7cb
rc=0
```

### C. `mori-pin-check.py` at the scored tip — final line and the pins that matter

```
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=14c5110d65a2f225e7316e1996e92090b9b8e7cb baseline=yes
pin line=168 kind=digest state=match digest=533218a566030fda… file=tools/mori-round14-regressions.py
pin line=184 kind=lines state=match pinned='743 lines' file=tools/mori-gate-registry.py observed=743
pin line=192 kind=digest state=match digest=37fd7c24ff52… file=.ufo/waves/round-45/count-c3.py
pin line=192 kind=digest state=match digest=69bf9b6eb29b… file=.ufo/waves/round-45/fixtures/mutants/count-c3.py
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 14c5110d… --selftest'
pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0
```

42 lines total (41 pin lines, all `state=match`, plus the verdict line); file `<S>/out-pin-14c5110d.txt`
sha256 `3c59bd035cfbc024e6f747238f30b63312c1fd587ec429c2fb8c2ed8f2ccdb98`. The `e4dfff32` run of the same
command, `<S>/out-pin-e4dfff32.txt`, is sha256
`26fd6709f8d61c54b9acbf1ba58a1240ef2302d884aceaf3dad5a9ccab603006` — the digest `w2/R48ExecRealRegistry.md:81`
publishes for that seat's log, i.e. an exact byte reproduction of a committed round-48 artefact a day later, from a
different `--repo`.

### D. Selftest tallies (arms)

`C1_SELFTEST`: 34 `PASS` / 0 `FAIL`. `C2_SELFTEST`: 22 `PASS` / 0 `FAIL`. `PIN_CHECK_SELFTEST`: 60 `PASS` /
0 `FAIL`. `UNLANDED_SELFTEST`: 13 `PASS` / 0 `FAIL`.

### E. The revision-scoping probe (`SKILL.md:911`)

```
$ strace -f -qq -e trace=openat,stat,newfstatat -o strace-conform.txt \
    timeout 300 python3 .ufo/waves/round-40/conform.py 14c5110d65a2f225e7316e1996e92090b9b8e7cb --selftest
PASS scratch            scratch parent moved off-lane -> only scratch failed
PASS selftest_conjunct  communicate timeout keyword stripped -> only selftest_conjunct failed
CONFORM_SELFTEST pass=11 fail=0
rc=0
$ grep -c '/home/vgpnk/Projects/shokunin/mori-shokunin' strace-conform.txt
3077
$ grep -E 'round-(39|40)/' strace-conform.txt | grep -o '/home/vgpnk[^"]*' | sort -u | head
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/contract.md
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/fixtures/hang-after-flush.py
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/count-c8.py
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/scratch
```

`.ufo/waves/round-40/conform.py:69` is `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` and line 71 builds
`DEFAULT_COUNTERS` from it, so this pinned command reads the **live lane** while the rest of the run measures the
revision. It happens to agree today (`.ufo/waves/round-40/count-c8.py` sha256 `4e4d50eb1e96…` in the live lane and in
the `14c5110d` extract are equal), which is why `mismatches=0` here; in an environment without `/home/vgpnk` the same
pin is the single `mismatch` the 2026-10-26 reflection recorded (`SKILL.md:911`, `conformance setup error: No such
file … round-40/count-c8.py`).

## Residuals — round-48 material this seat did **not** re-execute

Named so that "all AGREE" is not read as wider than it is. These are one-off command outputs committed as evidence,
not frozen counters or registered-instrument selftests: `evidence/census-start.txt`, `evidence/census-end.txt`
(`sources-census.sh validate`), `evidence/sweep-quota-rows.txt`, `evidence/after-appendonly.txt`, and the wave-1/wave-2
in-report measurements (e.g. `w2/R48ExecD7.md`'s mutant runs). Also out of scope by the lane rules: anything requiring
a kernel-log MESSAGE read or a cgroup/host-state change.

## Findings

- **F1 — LOW (no defect; the measured claim).** Round 48 reproduces: 16/16 runs AGREE with the receipt or pin each
  must equal, six byte-identically (`cmp -s`), and the `e4dfff32` pin-check log is byte-identical to
  `w2/R48ExecRealRegistry.md:81`'s committed digest. The closure's "evidence-verified, not executed" gap is closed
  for this host. Concerns `.ufo/waves/round-48/` in full.
- **F2 — MED (`SKILL.md:911`, `.ufo/waves/round-40/conform.py:69`).** One of the 31 tally pins is not
  revision-scoped: the pinned `CONFORM_SELFTEST` command reads the live lane through a hardcoded absolute path
  (strace: 3077 accesses under `/home/vgpnk/Projects/shokunin/mori-shokunin`, including
  `.ufo/waves/round-40/count-c8.py` and `.ufo/waves/round-39/contract.md`) while printing `pass=11 fail=0` rc 0. A
  `pin-check --rev R` `match` on that line is therefore not evidence about R, and off-host it is the pin that turns
  `unmet`. Round 48's C1 verdict is unaffected (the pin passes and `real=met` either way), but the lane's own QUALITY
  127 rule ("instruments carry no absolute host path") is violated by a file a gate pin depends on. The leak is not
  read-only: `conform.py:70` also builds `SCRATCH_ROOT` from that same `LANE`, so the pinned command **creates work
  directories in the live lane** — this seat's runs left `mori-conform-selftest-497jhgmw` and `…-6llm2k22` under
  `.ufo/waves/round-40/scratch/` (mtimes 10:11:21 / 10:11:33) while the measured repository was the scratch clone; both
  were removed by this seat and `git status` no longer lists them. A round-51 seat re-running `count-c1.py` or
  `pin-check --rev` off-clone therefore touches, and can leave debris in, the lane it is measuring. Reported only —
  no counter, predicate or pin change is proposed here.
- **F3 — LOW (`SKILL.md:938` / `evidence/freeze-sha256.txt`).** Before this seat there was **no committed receipt for
  `PIN_CHECK=met` at round 48's scored tip**: `freeze-sha256.txt` records the *entering v2* tool (`9832e38c…`) for
  `tools/mori-pin-check.py`, the two committed PIN_CHECK runs name `e5dbac05` (`w1/ExecSkillRowsRun.md:54`) and
  `e4dfff32` (`w2/R48ExecRealRegistry.md:79`), and the v3 obligation in `v3-spec.md:20` ("the real SKILL.md at the
  landed tip must stay `PIN_CHECK=met`") had no receipt at `14c5110d`. Now measured: `met`, 41/41 `state=match`,
  `tally_pins=31 digest_pins=8`, rc 0 (row 15). Section C of this report is the commit-able receipt.
- **F4 — LOW (`evidence/after-c2-final.txt`).** The C2 final receipt was measured at `91fbbc2a`, one commit before
  the scored tip, so "C2 at the landed tip" rested on a rev one commit behind it. Harmless in fact — `git diff --stat
  91fbbc2a 14c5110d -- corpus tools` is empty and the entry sha256 is `334df177…` at both — and now measured at the
  tip (row 13). Worth stating because the same pattern (receipt measured before the last two receipt-only commits)
  recurs with F3.
- **F5 — LOW (`evidence/control-c1-tool-v2-entering.txt`, `evidence/control-c1-stub-always-met.txt`).** Those two
  committed control receipts are **byte-identical** (`ca32ed7832c3…`, `cmp -s` clean): on the printed line set the
  frozen counter cannot distinguish the entering v2 tool from a constant-liar stub, because both are green on all
  eight junk edits and both end `real=met` (the stub prints it by construction). The discrimination in the evidence
  set comes from `control-c1-stub-always-unmet.txt` (`7edc9234…`), which flips the four honest arms and `real`. A
  limit of the evidence set as committed, not a re-score: the predicate was frozen before the data and nothing here
  proposes changing it.
- **F6 — LOW (scope line, no file defect).** The residuals listed above (census, sweep, append-only, wave-2 in-report
  measurements) remain evidence-verified only. If the lane wants suggestion 3 to cover them, the next seat needs a
  brief that names those commands; they are not part of "frozen counters + registered tools' selftests".
- **F7 — LOW (usage, `count-c1.py` `--scratch` default).** `count-c1.py` falls back to `tempfile.mkdtemp(dir=…/.scratch)`
  inside the measured repo when `--scratch` is not given, and `mori-pin-check.py --rev` materialises its export under
  `<repo>/.scratch`; a later re-execution brief should keep passing `--scratch` and `--repo <clone>` so a re-run cannot
  write into the lane (this seat did both; the only lane writes that did occur were the two CONFORM work directories
  reported and removed under F2).
