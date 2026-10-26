# Mo51MutC1Counter — mutation test of `count-c1.py` (wave w1, round 51)

Seat: mutation-tester, leaf, no subagent. Item: the 8 named single-point mutations of
`.ufo/waves/round-51/count-c1.py` scored at the entering rev `aa3af1ec…` (must stay unmet), with the frozen
controls re-run as needed to decide killed/survived. This report contains the mutant edits, the observed
readings, and the verdicts. No tool was installed or upgraded (nothing was needed).

Environment: MACHINE_ID host, Python 3.14.8, git 2.56.0, bubblewrap 0.13.1. disk-guard `status` ran with rc 0
before the heavy runs: `/fast/scratch/hyaku 25% used, 606.8G free` (earlier probe: 26%, 596.3G). Scratch
`/fast/scratch/hyaku/mori-r51/Mo51MutC1Counter/` with `TMPDIR=<scratch>/tmp`; `/tmp` unused. Every counter run
used an explicit `--scratch` under the seat scratch and explicit `--repo`/`--hide` (the counter's `DEFAULT_REPO`
derives from `HERE`, so copies outside the lane need both). The candidate's internal fresh clones (C0/C1, one per
arm, ~113 MB each) are part of the frozen instrument and were removed by the counter on exit; the only seat-level
clone is the control fixture `ctl/K` (one `git clone --no-local`), used read-only after build.

Frozen bytes verified against `evidence/freeze-sha256.txt`: `count-c1.py` sha256 `622f650c…` (my pristine copy
matches), `controls/c1-controls.py` `8351ba6d…`, witness `mori-pin-check.py` `35c69d91…`, witness `conform.py`
`7f5174d5…`. Both revs resolve (`git rev-parse --verify …^{commit}` rc 0).

## 0. Baseline — pristine counter reproduces the do-nothing receipt

```
$ cd /fast/scratch/hyaku/mori-r51/Mo51MutC1Counter
$ python3 ./pristine-count-c1.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd \
      --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
      --hide /home/vgpnk/Projects/shokunin/mori-shokunin --scratch ./run-pristine
C1=unmet kill_residue=12475 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0
      rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=kill_residue,relocated,classified
exit=1   (35.5 s)
```

Identical to `evidence/control-c1-do-nothing.txt` (residue count inside the contract's observed band 12475–12547;
the receipt itself notes the count varies and that any nonzero value is unmet).

## 1. Mutants and single-point edits

Each mutant is the frozen 622f650c bytes with exactly one behavior point changed (every replacement asserted to
occur exactly once). File `count-c1.py` line numbers refer to the frozen file.

| # | mutation | edit | location |
|---|---|---|---|
| m1 | arm A ignores untracked files | `status` drops `--untracked-files=all` | `status_lines`, line 83 |
| m2i | arm A kills before any write — fail-closed reading | write-detection wait removed (started stays False → `no_progress`, arm A always fails) | `arm_kill`, lines 108–117 |
| m2ii | arm A kills before any write — fail-open reading | same wait removed; arm proceeds to count residue right after an immediate kill (0.2 s), so arm A passes trivially | `arm_kill`, lines 108–117 |
| m3 | arm B drops `--tmpfs` (lane visible) | `--tmpfs`, `lane_hidden` removed from the bwrap argv | `arm_relocated`, line 140 |
| m4 | arm B accepts any last line | `… and last.startswith("PIN_CHECK=met")` dropped from arm B's return | `arm_relocated`, line 150 |
| m5 | arm C accepts class on any line | `lines[0].endswith("class=" + cls)` → `any(l.endswith("class=" + cls) for l in out)` | `arm_classified`, line 179 |
| m6 | arm C drops the OKAY row check | the `okay`/`state=match` block deleted | `arm_classified`, lines 180–181 |
| m7 | arm D floor 0 | `ENTERING_SELFTEST = 114` → `0` | line 40 |
| m8 | selftest exit code ignored | `p.returncode == 0 and …` dropped in arm D's return | `arm_selftest`, line 208 |

## 2. Scoring matrix

Entering: all mutants scored at `aa3af1ec…` (`--repo`/`--hide` = the lane; this is exactly the do-nothing
control state). Witness: the frozen witness control rebuilt from the frozen builder/witness bytes (same trees the
frozen `controls/c1-controls.py` builds: base + witness pin-check + witness conform.py + SKILL.md pin cell 114→119)
as a commit in a throwaway clone; fresh hashes because the L1's original K was cleaned. All runs: `python3
<counter> <rev> --repo <repo> --hide <lane> --scratch <scratch>`, cwd = seat scratch, logs under `<scratch>/logs/`
(kept until cleanup).

| counter | entering reading (aa3af1ec…) | exit | witness reading | exit | verdict |
|---|---|---|---|---|---|
| pristine | `unmet kill_residue=12475 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 failed=kill_residue,relocated,classified` | 1 | `met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 failed=-` | 0 | baseline |
| m1 | `unmet kill_residue=1 … failed=kill_residue,relocated,classified` | 1 | `met … failed=-` | 0 | **SURVIVED** |
| m2i | `unmet kill_residue=none … failed=kill_residue,relocated,classified` (no_progress) | 1 | **`unmet kill_residue=none relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 failed=kill_residue`** | 1 | **KILLED** |
| m2ii | `unmet kill_residue=0 relocated=unmet … failed=relocated,classified` | 1 | `met … failed=-` | 0 | **SURVIVED** |
| m3 | `C1_SETUP lane path still visible inside bwrap` | 2 | `C1_SETUP lane path still visible inside bwrap` | 2 | **KILLED** |
| m4 | `unmet kill_residue=12476 … failed=kill_residue,relocated,classified` | 1 | `met … failed=-` | 0 | **SURVIVED** |
| m5 | `unmet kill_residue=12476 … failed=kill_residue,relocated,classified` | 1 | `met … failed=-` | 0 | **SURVIVED** |
| m6 | `unmet kill_residue=12476 … failed=kill_residue,relocated,classified` | 1 | `met … failed=-` | 0 | **SURVIVED** |
| m7 | `unmet kill_residue=12475 … failed=kill_residue,relocated,classified` | 1 | `met … failed=-` | 0 | **SURVIVED** |
| m8 | `unmet kill_residue=12475 … failed=kill_residue,relocated,classified` | 1 | `met … failed=-` | 0 | **SURVIVED** |

All 9 entering runs stay unmet as required. m4–m8 produce byte-identical verdict lines to the pristine counter
(the 12475/12476 residue difference is the documented run-to-run band, not a mutation effect). m1's first residue
collapses to a directory line (`kill_residue_first: !! .scratch/pin-check-tjna661q/`); m2ii's arm A passes
vacuously (`kill_residue=0`, `failed=` list loses kill_residue).

### 2.1 Killed mutants — how the frozen controls caught them

- **m2i** (arm A kills before any write, fail-closed): the WITNESS control flips `met`/exit 0 → `unmet
  failed=kill_residue`/exit 1. The positive control is the only frozen state that can see arm A fail on a good
  landing; it does.
- **m3** (arm B drops `--tmpfs`): the probe inside bwrap sees the real lane (`<lane>/SKILL.md` exists) and exits 2;
  `arm_relocated` raises → the counter prints `C1_SETUP lane path still visible inside bwrap` and exits 2 on every
  state (6.6 s, both entering and witness). Every frozen receipt records exit 0/1, so any control distinguishes it.
  The kill rule also treats exit 2 as not-verified, so the mutant fails closed and cannot endanger the claim.

### 2.2 Survived mutants — limits of the frozen counter

Each survivor leaves every frozen state's VERDICT unchanged; the reported receipt *lines* change only in fields the
contract explicitly declares variable (kill_residue count). Structural reason: every frozen control state fails on
≥2 arms at once — do-nothing {A,B,C}, scratch-only {B,C}, conform-only {A,C}, class-only {A,B,D}, always-env
{B,C,D} — so removing one arm check can never empty a failing set, and the witness (all arms green) is unaffected by
a removed check that would only trigger on a defect. No control isolates a single arm.

- **m1** (arm A ignores untracked files): verified with a micro-fixture that `git status --porcelain --ignored`
  without `-uall` still lists any residue as a collapsed directory line (`!! .scratch/`): detection is preserved,
  only the path count collapses (12475 → 1). The do-nothing/conform-only receipt fields would read 1 (not 12475+
  ), which the contract explicitly treats as equivalent (”any nonzero value is unmet”). LOW limit.
- **m2ii** (arm A kills before any write, fail-open): arm A passes trivially — the kill lands ~0.2 s after launch,
  before anything is written, so `kill_residue=0` for ANY tool, including one that would write residue later. Extra
  probe (rebuilt conform-only control, tree = frozen `{CF: witness conform.py}` on base): m2ii reads `unmet
  kill_residue=0 relocated=met reloc_mismatch=0 classified=bad selftest=pass=114,fail=0 failed=classified` (exit 1)
  vs the frozen receipt `failed=kill_residue,classified` — verdict unchanged, arm-A absence visible only in the
  field. HIGH limit: arm A's measurement is the first to go if the write-detection wait is lost, and the frozen
  suite cannot see it.
- **m4** (arm B accepts any last line): redundant today — `mori-pin-check.py` returns rc 0 iff `PIN_CHECK=met`
  (line 946), so `p.returncode == 0` already gates every unmet state (all unmet runs rc 1). The last-line check
  would only matter for a tool whose rc and last line disagree. LOW limit.
- **m5** (arm C accepts class on any line): the class string may come from any output line; the per-pin binding is
  unenforced. The always-env control still fails (no `class=stale` line anywhere) and the summary `env=2 stale=2`
  still gates, so no frozen state flips; a tool that emits the right class strings but attaches them to the wrong
  pins would pass. MED limit.
- **m6** (arm C drops the OKAY row check): the match row is unverified; only the summary last line (` env=2
  stale=2`) remains, and it counts mismatches, not the match row. A tool that tags the matching pin too (without
  changing the env/stale totals) would pass. MED limit.
- **m7** (arm D floor 0): `PIN_CHECK_SELFTEST pass=0 fail=0` (rc 0) would pass arm D, i.e. a gutted selftest with
  all tests removed is accepted. No frozen state has a clean tally below 114. MED limit.
- **m8** (selftest exit code ignored): a tool printing a clean tally then exiting nonzero passes arm D. rc
  contradiction is only exercised in arm C's stlb fixture, never in arm D. MED limit.

## Findings

- **HIGH — `count-c1.py` line 108–117 (arm A), and by construction the whole counter: 7 of 9 single-point mutants
  survive the entire frozen control suite at the verdict level** (m1, m2ii, m4, m5, m6, m7, m8). Every frozen
  control state fails on ≥2 arms simultaneously; none isolates a single arm, so any single-arm check can be removed
  without changing a single verdict. The counter's four arms are only exercised jointly; arm-level sensitivity is
  not pinned by the frozen controls.
- **HIGH — `count-c1.py` `arm_kill` (lines 108–117): arm A can pass vacuously** (m2ii). Killing before the tool
  writes makes `kill_residue=0` trivially; demonstrated at entering (`kill_residue=0` vs pristine 12475) and on the
  conform-only control (`failed=classified` vs receipt `failed=kill_residue,classified`). A pin-check whose first
  write lands after the kill moment would escape arm A entirely. The named limit “arm A kills at one moment and
  proves nothing about a kill at another moment” extends to: with the write-detection gate gone, any early kill
  proves nothing.
- **MED — `count-c1.py` line 179 (arm C): class-to-pin binding unenforced** (m5). The required `class=env`/
  `class=stale` string may come from any output line, so misattributed classes pass; only the summary totals and the
  always-env control's missing-stale failure keep the arm honest on the frozen states.
- **MED — `count-c1.py` lines 180–181 (arm C): the OKAY row check can be dropped** (m6). The summary ` env=2
  stale=2` line counts mismatches and does not verify the matching pin carries no class.
- **MED — `count-c1.py` line 40 (arm D): the 114 floor can be dropped** (m7). A selftest reporting `pass=0
  fail=0` with rc 0 would pass; the floor is what prevents a gutted selftest from passing.
- **MED — `count-c1.py` line 208 (arm D): the selftest exit code can be ignored** (m8). rc contradiction is only
  exercised by arm C's stlb fixture, never by arm D.
- **LOW — `count-c1.py` line 83 (arm A): `--untracked-files=all` only guards count granularity** (m1). Any
  visible residue still collapses to ≥1 line, so detection is preserved; the receipt count fields (12475+ → 1) are
  contractually variable.
- **LOW — `count-c1.py` line 150 (arm B): the `PIN_CHECK=met` last-line check is dead weight given the tool's rc
  contract** (m4) — `mori-pin-check.py` returns 0 iff `PIN_CHECK=met` (line 946). It would matter only for a tool
  whose rc and last line disagree.
- **Verified positives**: the witness control caught the fail-closed arm-A mutant (m2i: met → unmet, exit 0 → 1),
  and the probe converts the missing `--tmpfs` into `C1_SETUP` exit 2 on every state (m3). Both killed mutants fail
  closed or are detected by the positive leg; the survivors are the limits listed above.
- UNVERIFIED: scratch-only, class-only and always-env control states were not re-run under every survivor; their
  verdict invariance follows from the failing-arm sets (≥2 arms per state) and the single-arm edits, and only the
  do-nothing (entering), conform-only and witness states were re-run empirically under the relevant mutants.
- Deployment caveat (not a mutation): `DEFAULT_REPO`/`--hide` default derive from the counter's own path
  (`HERE`); a copy run outside the lane needs explicit `--repo`/`--hide` (used for every run above).
