# Mo52ExecR51ArmControls — one control per arm of the frozen round-51 `count-c1.py`

Seat: executor, round 52 wave `w1`, leaf (no subagent). Item: round-51 closure routed defect 3 — 7 of 9
single-arm mutants of `.ufo/waves/round-51/count-c1.py` kept every frozen control verdict
(`corpus/lessons/round-51.md` `## Wave w1 — integrated findings`, named limit beginning "every frozen control
fails on two or more arms at once"; `corpus/lessons/round-51-verifier-spotcheck.md` §5 item 3;
`.ufo/waves/round-51/w1/Mo51MutC1Counter.md`). Deliverable: design (do not apply) one control per arm A–D that a
single-arm mutant would flip, give each control's construction, and show the intact-versus-mutated verdict table;
demonstrate two of them in scratch. Six control commits were built and scored, covering all four arms; six of the
nine mutants are flipped, and the two that are not (m1, m8) are shown to be non-isolable, with the reason.

The counter is frozen: no byte of it was edited, no control was applied to the lane, no fix is proposed here. The
items this design implies are routed to round 53 in §7.

Environment: MACHINE_ID host, Python 3.14.8, git 2.56.0, bubblewrap 0.13.1.
Scratch `/fast/scratch/hyaku/mori-r52/Mo52ExecR51ArmControls/`, `TMPDIR=<scratch>/tmp`; no `/tmp` path is cited;
the scratch tree was removed before this report was filed. `scripts/hyaku/disk-guard.sh status` before the runs:
`/fast/scratch/hyaku 25% used, 603.6G free`. No tool was installed or upgraded; no pacman transaction was run.

Frozen bytes verified by sha256 before and after the runs:
`count-c1.py 622f650c1ade984d8c9abed20e7a7fd08930861a698398f36d4c3a770aff355c`,
`witness/mori-pin-check.py 35c69d9115b5e45f91a4b0311ce95c03b3b2b929250e2afb31b571a49687b3bf`,
`witness/conform.py 7f5174d542bd983552670b06f6cc424b10e53c81e55ecabcdd919f4043bdfa23` (the hashes
`Mo51MutC1Counter.md` and `.ufo/waves/round-51/evidence/freeze-sha256.txt` record).
Base revision for every control: `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd` (the entering tip at which the
mutants were scored). Fixture `K` = one `git clone --no-local` of the lane into scratch; every git call names
`-C K`, and `git -C K rev-parse --show-toplevel` printed the fixture path before the first control commit.
Lane left untouched: `git -C <lane> status --porcelain --untracked-files=all -- .ufo/waves/round-51` prints
nothing after all runs, and the counter's sha256 is unchanged. The counter cannot be run from a copy outside the
lane without `--repo`/`--hide` (both derive from `HERE`); every run below passed both explicitly.

## 1. The frozen suite's structural blindness (restated, not re-derived)

The six frozen control states fail on these arm sets (`.ufo/waves/round-51/evidence/control-c1-*.txt`; the
round-52 `contract.md` "C1 control readings" restates them): do-nothing {A,B,C}, scratch-only {B,C},
conform-only {A,C}, class-only {A,B,D}, always-env {B,C,D}, witness {}. Because every state that fails keeps at least two arms red,
removing one arm's check from the counter can never empty a failing set: the verdict cannot move. A control that
kills a single-arm mutant therefore has to fail on exactly one arm, which no frozen state does.

## 2. Construction rule — green anchor plus one defect

Each control commit is the **witness state** (the state the frozen `witness` receipt scores `C1=met`) plus one
defect keyed to exactly one arm's predicate:

* `tools/mori-pin-check.py` = the witness bytes (`35c69d91…`), with the one defect applied;
* `.ufo/waves/round-40/conform.py` = the witness bytes (`7f5174d5…`) — needed, measured: the frozen
  `class-only` control ships only the pin-check and reads `reloc_mismatch=2`, the witness that also ships the
  conform copy reads `reloc_mismatch=0`;
* `SKILL.md` = base bytes with the reconciler's own self-pin moved from `PIN_CHECK_SELFTEST pass=114 fail=0` to
  the shipped selftest's tally (`pass=119 fail=0` for every witness-derived control, `pass=0 fail=0` for the
  gutted-selftest control) — without the bump, arm B's own pin evaluation reports the self-pin mismatch and arm B
  is red as collateral.

Anchor measured first, so that a red arm in a control is the defect and not the base:

```
$ python3 frozen-count-c1.py 8d902c05e27cdfe54d42adb09587853f1ea3f7eb --repo <scratch>/K --hide <lane> --scratch <scratch>/witness
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=8d902c05e27cdfe54d42adb09587853f1ea3f7eb failed=-
exit=0   wall=99s
```

## 3. The controls: construction and expected verdicts

| arm | control (fixture commit) | the one defect in the committed instrument | intact counter | targeted mutant | mutated counter | flipped |
|---|---|---|---|---|---|---|
| A `kill_residue` | `ctl-A2` `fac68f31…` | with `--rev` and no `--scratch`, the instrument writes `run.log` into `<repo>/.scratch` **after** its export completes | `C1=unmet … failed=kill_residue` exit 1 | `m2ii` (write-detection gate removed, kill at 0.2 s) | `C1=met … failed=-` exit 0 | **yes** |
| B `relocated` | `ctl-B` `7987ae48…` | in `--rev` mode the instrument prints `elapsed=0s` after its `PIN_CHECK=…` verdict line | `C1=unmet … failed=relocated` exit 1 | `m4` (arm B accepts any last line) | `C1=met … failed=-` exit 0 | **yes** |
| C `classified` | `ctl-C5` `5a2a9e59…` | classes misattributed: the two `STLA`/`STLB` mismatch lines print `class=env`, and a decoy line ending `class=stale` is printed beside them (summary totals unchanged) | `C1=unmet … failed=classified` exit 1 | `m5` (class accepted on any line) | `C1=met … failed=-` exit 0 | **yes** |
| C `classified` (second conjunct) | `ctl-C6` `1134c19b…` | the `OKAY` row prints `state=mismatch class=stale` while the instrument's own counts stay `env=2 stale=2` | `C1=unmet … failed=classified` exit 1 | `m6` (OKAY row check dropped) | `C1=met … failed=-` exit 0 | **yes** |
| D `selftest` | `ctl-D7` `75bdbdfa…` | `--selftest` reduced to `PIN_CHECK_SELFTEST pass=0 fail=0` rc 0, and the SKILL.md self-pin moved `114 → 0` to match | `C1=unmet … selftest=pass=0,fail=0 failed=selftest` exit 1 | `m7` (floor `ENTERING_SELFTEST = 0`) | `C1=met … failed=-` exit 0 | **yes** |
| A (first construction) | `ctl-A` `bff1e14c…` | the `--rev` export parent is `<repo>/.scratch` (the pre-v5 defect: the directory is created before any pin runs) | `C1=unmet … failed=kill_residue` exit 1 | `m2ii` | `C1=unmet … kill_residue=1 failed=kill_residue` exit 1 | no — write lands before the 0.2 s kill |
| — (probe) | `ctl-D8` `a261e6b9…` | `--selftest` prints the honest `pass=119 fail=0` then exits 1 | `C1=unmet … failed=relocated,selftest` exit 1 | `m8` (arm D ignores rc) | `C1=unmet … failed=relocated` exit 1 | no — two arms, see §5 |
| A | `ctl-A2` under `m1` | as `ctl-A2` | `failed=kill_residue`, `kill_residue=1` | `m1` (`--untracked-files=all` dropped) | same verdict, `kill_residue=1` | no — equivalent mutant, §5 |

Patches, verbatim (one occurrence each, asserted by the builder; base = witness bytes, line numbers of the
witness file):

```python
# ctl-A2  (witness pc line 923, after `rev, root = got`)
                if not args.scratch:
                    os.makedirs(os.path.join(repo, ".scratch"), exist_ok=True)
                    with open(os.path.join(repo, ".scratch", "run.log"), "w") as f:
                        f.write("pin-check run\n")

# ctl-B   (witness pc line 944-946)
            met, out = check(text, root, scratch, rev, args.timeout, args.min_tally_pins, baseline_text)
            print("\n".join(out))
            if args.rev:
                print("elapsed=0s")
            return 0 if met else 1

# ctl-C5  (witness pc line 825-827, the tally printer)
                counts[kind] += 1
                cls = " class=" + kind
            if prefix in ("STLA_SELFTEST", "STLB_SELFTEST"):
                cls = " class=env"
            if prefix == "STLA_SELFTEST":
                out.append("pin line=%d kind=tally prefix=DECOY_SELFTEST state=note class=stale" % line)

# ctl-C6  (same printer: print state, not the counted state)
            shown = "match" if ok else "mismatch"
            shown_cls = cls
            if prefix == "OKAY_SELFTEST":
                shown = "mismatch"
                shown_cls = " class=stale"

# ctl-D7  (witness pc line 904-905)
    if args.selftest:
        print("PIN_CHECK_SELFTEST pass=0 fail=0")
        return 0

# ctl-D8  (probe: honest tally, contradicting exit code)
    if args.selftest:
        rc = selftest()
        return rc if rc else 1
```

The mutants are single-point edits of the frozen `622f650c…` bytes (sha256 of each in §8), reproducing the
edits `Mo51MutC1Counter.md` §1 recorded: `m1` drops `--untracked-files=all` from `status_lines` (frozen line 83);
`m2ii` replaces the write-detection wait in `arm_kill` (frozen lines 109–119) with `started = True;
time.sleep(0.2)`; `m4` drops `and last.startswith("PIN_CHECK=met")` (line 150); `m5` replaces
`lines[0].endswith("class=" + cls)` with `any(l.endswith("class=" + cls) for l in out)` (line 179); `m6` deletes
the `okay`/`state=match` block (lines 180–181); `m7` sets `ENTERING_SELFTEST = 0` (line 40); `m8` drops
`p.returncode == 0 and` from arm D's return (line 208).

## 4. Demonstrated runs (receipts)

All runs: `cd <scratch>`, `TMPDIR=<scratch>/tmp`, then
`python3 <counter> <rev> --repo <scratch>/K --hide /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <scratch>/<name>`,
four states in parallel; wall time 100–108 s per batch of four.

**Arm A — `ctl-A2`, intact vs `m2ii`** (this is the pair the frozen suite cannot produce):

```
$ python3 frozen-count-c1.py fac68f310b47045496181bf36b67801d1deb3a51 --repo <scratch>/K --hide <lane> --scratch <scratch>/ctl-A2
kill_residue_first: !! .scratch/run.log
C1=unmet kill_residue=1 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=fac68f310b47045496181bf36b67801d1deb3a51 failed=kill_residue
exit=1

$ python3 count-c1-m2ii.py fac68f310b47045496181bf36b67801d1deb3a51 --repo <scratch>/K --hide <lane> --scratch <scratch>/ctl-A2-m2ii
kill_residue_first: -
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=fac68f310b47045496181bf36b67801d1deb3a51 failed=-
exit=0
```

The first construction (`ctl-A`, export parent under the repo) is the counter-example that fixes the timing
requirement: the defect's first in-repo write lands before the mutant's 0.2 s kill, so `m2ii` still reads
`kill_residue=1` and survives even on a single-arm state.

```
$ python3 count-c1-m2ii.py bff1e14c3fbf9bc089da493550a4b954de71d591 --repo <scratch>/K --hide <lane> --scratch <scratch>/ctl-A-m2ii
kill_residue_first: !! .scratch/pin-check-7fs2wzno/tree/
C1=unmet kill_residue=1 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=bff1e14c… failed=kill_residue
exit=1
```

**Arm C — `ctl-C5`, intact vs `m5`, and the same control under `m6` (stays red, so the control is specific)**:

```
$ python3 frozen-count-c1.py 5a2a9e59bf28699665dc1c2b58d57888c2a0ef24 … --scratch <scratch>/ctl-C5
classified: pin line=5 kind=tally prefix=DECOY_SELFTEST state=note class=stale
classified: pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch … class=env
classified: pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch … class=env
classified: PIN_CHECK=unmet tally_pins=5 … env=2 stale=2
C1=unmet kill_residue=0 relocated=met reloc_mismatch=0 classified=bad selftest=pass=119,fail=0 rev=5a2a9e59… failed=classified
exit=1

$ python3 count-c1-m5.py 5a2a9e59bf28699665dc1c2b58d57888c2a0ef24 … --scratch <scratch>/ctl-C5-m5
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=5a2a9e59… failed=-
exit=0

$ python3 count-c1-m6.py 5a2a9e59bf28699665dc1c2b58d57888c2a0ef24 … --scratch <scratch>/ctl-C5-m6
C1=unmet … classified=bad … failed=classified
exit=1
```

**Arm D — `ctl-D7`, intact vs `m7`**:

```
$ python3 frozen-count-c1.py 75bdbdfa08cf979780506589a98ee1dd36cb83a8 … --scratch <scratch>/ctl-D7
C1=unmet kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=0,fail=0 rev=75bdbdfa… failed=selftest
exit=1

$ python3 count-c1-m7.py 75bdbdfa08cf979780506589a98ee1dd36cb83a8 … --scratch <scratch>/ctl-D7-m7
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=0,fail=0 rev=75bdbdfa… failed=-
exit=0
```

**Arms B and C6, and the two probes** (same harness; full verdict lines):

```
ctl-B      intact   C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 … failed=relocated        exit=1
ctl-B  m4           C1=met   kill_residue=0 relocated=met   reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 … failed=-                exit=0
ctl-C6     intact   C1=unmet kill_residue=0 relocated=met   reloc_mismatch=0 classified=bad selftest=pass=119,fail=0 … failed=classified     exit=1
ctl-C6 m6           C1=met   kill_residue=0 relocated=met   reloc_mismatch=0 classified=ok  selftest=pass=119,fail=0 … failed=-               exit=0
ctl-D8     intact   C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=1 classified=ok  selftest=pass=119,fail=0 … failed=relocated,selftest  exit=1
ctl-D8 m8           C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=1 classified=ok  selftest=pass=119,fail=0 … failed=relocated          exit=1
ctl-A2 m1           C1=unmet kill_residue=1 relocated=met   reloc_mismatch=0 classified=ok  selftest=pass=119,fail=0 … failed=kill_residue     exit=1
```

`ctl-C6`'s intact reading shows the intended state (`prefix=OKAY_SELFTEST state=mismatch … class=stale` at pin
line 7 while the summary still ends `env=2 stale=2`).

## 5. m1 and m8 have no single-arm control (measured, not argued)

* **m1** (`status_lines` without `--untracked-files=all`): the residue collapses to a directory line but never to
  zero, so any state that makes arm A red keeps it red (`ctl-A2` under `m1`: `kill_residue=1`,
  `failed=kill_residue`, exit 1 — same as the intact counter). Under the frozen predicate ("0 lines") `m1` is an
  **equivalent mutant**: only a control that asserts the residue path list or the count could distinguish it, and
  the contract declares those counts variable ("any nonzero value is unmet").
* **m8** (arm D ignores the selftest exit code): the contradiction cannot be confined to arm D, because arm B
  evaluates the reconciler's own SKILL.md self-pin by running the same `--selftest` invocation; the witness
  pin-check marks a tally whose exit code contradicts it as `class=stale`. `ctl-D8` (honest tally, exit 1) is red
  on **two** arms (`failed=relocated,selftest`), and under `m8` the run stays red on the B arm
  (`failed=relocated`). A single-arm state for `m8` does not exist while the self-pin row is present; deleting
  that row is refused by the instrument's own "a measured tree that ships this instrument must pin it" check.

Both are routed in §7 as counter-selftest items rather than control states.

## 6. Named limits of this design

* The controls are synthetic instrument bytes, not a landing: they show that each arm's check can be flipped,
  not that a real tool would produce the state. `ctl-B` in particular depends on an instrument that keeps
  printing after its verdict line — with `rc ≡ met` (the reason `Mo51MutC1Counter.md` calls m4 dead weight) the
  last-line conjunct is otherwise unreachable.
* The controls ride on the instrument's printed text, not on an independent oracle. A counter arm that passes for
  the wrong reason could still pass a control: `ctl-C5`/`ctl-C6` exercise two conjuncts of arm C; a third way to
  be wrong (e.g. accepting a state string in the wrong position) is not covered.
* Arm A's isolation is timing-dependent, and the measurement makes that explicit: `ctl-A` (write inside the
  first 0.2 s) does not flip `m2ii`; `ctl-A2` (write after the export clone) does. An arm-A control pins the
  kill *point* only as far as its margin (here: clone time, ≫ 0.2 s, and under 3 s).
* Each control is a three-file commit (pin-check + conform + SKILL.md self-pin). A one-file control reads green
  on the wrong arm: the frozen `class-only` receipt shows `reloc_mismatch=2` from exactly that omission.
* Cost: ~100 s per counter run (four arms, three fresh clones of the fixture). Six controls + eight mutant runs
  took 17 runs in five parallel batches; a round-53 suite that ships these as counter selftest arms does not pay
  the clone cost, which is what §7 recommends.

## 7. Routed to round 53 (not applied here)

1. Successor `count-c1`-style counter ships arm-isolating control states in its `--selftest`, not as lane
   commits: the four constructions in §3 plus the C6 variant, each asserted to read `met` under its own mutant
   and `unmet` under the intact checker. That is the same shape as the round-44 C2 "surviving mutant" arm.
2. `m1` and `m8` cannot be killed by a control state (measured, §5): give them in-counter arms — a fixture that
   returns a residue list of two collapsed paths (m1) and a fixture whose tally and exit code disagree fed
   directly to the arm-D parser (m8).
3. Record in each control's receipt the wall time and the clone step, because arm A's verdict depends on the
   defect's first-write moment (the `ctl-A` versus `ctl-A2` pair is the evidence).
4. The round-52 counters share the same weakness by construction: no round-52 C1 control isolates one arm — e.g.
   `.ufo/waves/round-52/evidence/control-c1-axes-only.txt` reads `mismatches=5` spread over two arms (2 `pin`
   items and 3 `living` items red), so the axes repair alone cannot flip any single-arm mutant. The same
   green-anchor-plus-one-defect rule applies to `.ufo/waves/round-52/count-c1.py` arms (axes / pins / living /
   locators) and to `count-c2.py`'s entailment arm.

## 8. Control and mutant byte identities (for a rerun)

```
control revs (fixture K, parent aa3af1ec):  ctl-witness 8d902c05  ctl-A bff1e14c  ctl-A2 fac68f31
                                            ctl-B 7987ae48  ctl-C5 5a2a9e59  ctl-C6 1134c19b
                                            ctl-D7 75bdbdfa  ctl-D8 a261e6b9
committed pin-check bytes:  ctl-A 1c712f2a4455  ctl-A2 df94098f8e2c  ctl-B 4dbbdde2505d
                            ctl-C5 5fec75ea9972  ctl-C6 cf42310c141b  ctl-D7 47d1f9a17bbb
mutant counters:  m1 4db9ba7da73a  m2ii 1c563e0f61a3  m4 81a6bc2d65be  m5 866c98456f2c
                  m6 1ba94294c86a  m7 39ea0d0bff50  m8 bb5514ee7314
```

Rerun: `git clone --no-local <lane> <scratch>/K`; from `aa3af1ec` apply the three files per control and commit
(`-C K`, throwaway identity); score with
`python3 .ufo/waves/round-51/count-c1.py <control-rev> --repo <scratch>/K --hide <lane> --scratch <scratch>/<name>`.
The fixture commits are not reachable from the lane and the scratch tree was removed after the runs.

## Findings

- **HIGH — `.ufo/waves/round-51/count-c1.py` arms A–D (lines 98–208): the arm-level sensitivity the frozen
  suite lacks is constructible.** Six control commits — one defect per arm — read exactly one failing arm under
  the frozen counter (`failed=kill_residue`, `failed=relocated`, `failed=classified` ×2, `failed=selftest`) and
  flip to `C1=met` under the matching single-arm mutant. The round-51 routed defect 3 is closable by adding
  these states, not by re-scoring.
- **HIGH — same file, `status_lines` line 83 (m1): equivalent mutant.** `ctl-A2` under `m1` reads
  `kill_residue=1 failed=kill_residue` exit 1, identical to the intact counter; no control state can flip it
  under the frozen "0 lines" predicate. A residue-list assertion, or an in-counter fixture, is required.
- **HIGH — same file, `arm_selftest` line 208 (m8): no single-arm control exists.** `ctl-D8` (clean tally,
  exit 1) is red on `relocated` and `selftest` together, because arm B's self-pin of the reconciler evaluates the
  same `--selftest` invocation; under `m8` the verdict stays `unmet failed=relocated`. An in-counter arm feeding
  a disagreeing tally/rc pair to the parser is the only isolation.
- **MED — same file, `arm_kill` lines 109–119: arm A's control must place the defect's first in-repo write after
  the kill point.** `ctl-A` (export directory created immediately) leaves `m2ii` alive at `kill_residue=1`;
  `ctl-A2` (write after the export) flips it to `met`. This is the operational form of the named limit "arm A
  measures one kill moment, so a tool that delays its in-repo write past 3 s scores 0" — the delay threshold is
  now demonstrated, not only asserted.
- **MED — same file, arm C lines 177–183: two independent conjuncts need two controls.** `ctl-C5` (class bound
  to the wrong line, with the right class string elsewhere) flips only `m5`; under `m6` it stays
  `failed=classified`. `ctl-C6` (OKAY row tagged) flips only `m6`. A single arm-C control cannot cover both.
- **LOW — controls need the witness pair plus the self-pin bump.** The frozen `class-only` receipt shows
  `reloc_mismatch=2` where the witness shows 0, from shipping the pin-check without the conform copy; a control
  committed as a one-file change reads red on the arm it is not testing.
- **LOW — deployment caveat carried from `Mo51MutC1Counter.md`:** the frozen counter's `DEFAULT_REPO`/`--hide`
  derive from its own path, so a copy outside the lane must be given both explicitly (done in every run above);
  a bare run of a copy would hide the scratch tree instead of the lane.
- **Verified clean:** frozen counter bytes unchanged (`622f650c…`), lane's `.ufo/waves/round-51` unmodified, no
  file created by this seat inside the lane, no tool installed, no pacman transaction. UNVERIFIED: nothing in
  this item depends on host state, so no host reading is claimed.
