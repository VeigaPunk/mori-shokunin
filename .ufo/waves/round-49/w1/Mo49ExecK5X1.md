# Mo49ExecK5X1 — X1 (a registry finding that exits as a setup error) and K5 (namespace join)

author-date: 2026-10-25
lane tip cited: `0df17b7b` (round-49 freeze; entering tip `b3e3453d`)
seat: w1 executor, leaf (no subagent spawned)

**Deliverable.** One scratch copy, `.scratch/r49-Mo49ExecK5X1/mori-pin-check.py` (sha256
`dfff623251ba6cfa4b82912e947f54ec630a7fe5c17ed0d0053c494643d2dfb9`), built from
`.ufo/waves/round-49/controls/tool-r48-merged-witness.py` (sha256 `c30ab623…`, 1020 lines). It carries
two rule changes and four new `--selftest` arms:

| change | class | was | now |
|---|---|---|---|
| X1 | a junk row makes a baseline row's bound command unresolvable | exit 2, one `PIN_CHECK_SETUP can only join an iterable`, **no finding line** | exit 1, `pin line=N kind=tally prefix=P state=no_command` |
| K5 | a prefix shared by ≥2 baseline instruments admits any new argv | `met` | `rebound` unless the new argv's instrument basename is one of the prefix's baseline basenames (a new round's copy of the same instrument) |
| arms | — | `PIN_CHECK_SELFTEST pass=65 fail=0` | `PIN_CHECK_SELFTEST pass=69 fail=0` |

No tracked file, no frozen byte, no git or jj state was touched; the L1 integrates.

## Acceptance

```
$ TMPDIR=$LANE/.scratch/r49-Mo49ExecK5X1 python3 -I -B \
    .scratch/r49-Mo49ExecK5X1/mori-pin-check.py --selftest
… 69 PASS lines, 0 FAIL …
PIN_CHECK_SELFTEST pass=69 fail=0            EXIT=0
```

```
$ TMPDIR=$LANE/.scratch/r49-Mo49ExecK5X1 python3 .ufo/waves/round-49/count-c1.py \
    --tool $LANE/.scratch/r49-Mo49ExecK5X1/mori-pin-check.py \
    --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 \
    --scratch .scratch/r49-Mo49ExecK5X1/acc-c1 --jobs 3
variant name=J1 expect=unmet got=unmet rc=1        … J2-J8 identical …
variant name=H1 expect=met got=met rc=0            … H2-H4 identical …
variant name=N1 expect=unmet got=unmet rc=1        … N2-N9 identical …
variant name=H6 expect=met got=met rc=0
variant name=H7 expect=met got=met rc=0
variant name=N10 expect=unmet got=unmet rc=1
variant name=H5 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
variant name=real-opaque expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
COUNTER_EXIT=0                               (wall 1258.48 s)
```

Diff against the witness: 69 diff lines, 47 added lines, 2 hunks (`check()` rebound branch,
`selftest()` arm block); receipt `.scratch/r49-Mo49ExecK5X1/witness.diff`.

## Method

- Scratch root `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecK5X1` for every
  lane-tool run; `git show <rev>:SKILL.md` wrote the two registries used for measurement
  (`SKILL-b3e3453.md`, 979 lines; `SKILL-2d85e33.md`, 912 lines).
- X1 reproduced on the unmodified witness first (same two shapes the round-48 critic reported), then
  fixed, then re-run end to end through the exact `count-c1.py` argv (`-I -B`, `--min-tally-pins 26
  --baseline-rev 2d85e33d…`).
- K5 measured statically through the tool's own `pin_bindings()` (no commands run) before writing the
  rule: 15 baseline prefixes, their bound-argv sets, and every key present at `b3e3453d` but absent at
  `2d85e33d` were enumerated, so the rule's cost on the real registry is known before it scores anything.
- Every new arm was shown to kill the code it guards by importing the pristine witness and scoring the
  same texts through it (`TypeError` for X1; `met` for the K5 reject arm).
- Read-only over the lane: no `git add/commit/stash/checkout/reset/pull/push`, no jj mutation, no write
  outside `.scratch/r49-Mo49ExecK5X1/` and this report. No tool installed or updated.
- Bytecode residue: importing the witness module from `controls/` for the arm-kill proofs created
  `.ufo/waves/round-49/controls/__pycache__/tool-r48-merged-witness.cpython-314.pyc` (21:39); removed
  after the proofs. `git status --porcelain` afterwards lists no modified tracked file and no untracked
  file from this seat outside `.scratch/r49-Mo49ExecK5X1/` and `w1/Mo49ExecK5X1.md`.
- Host: Python 3.14.8, git 2.56.0, `sudo -n` not used.

## X1 — a junk row must not turn a registry finding into a setup exit

Reproducers (each is `SKILL.md@b3e3453` with both baseline self-test spans re-pointed; the span occurs
twice, rows 184 and 194, both present at `2d85e33d`, so `bkey in base_bind` with a valid baseline argv
and `norm is None`):

| arm | edit | witness (before) | copy (after) |
|---|---|---|---|
| `x1a-dot-slash-baseline-row` | `python3 tools/mori-gate-registry.py --selftest` → `python3 ./tools/mori-gate-registry.py --selftest` | `rc=2`, 1 line: `PIN_CHECK_SETUP can only join an iterable` | `rc=1`, 42 lines; `pin line=184 … state=no_command`, `pin line=194 … state=no_command`; `PIN_CHECK=unmet tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=2 dropped=0 rebound=0 …` |
| `x1b-inline-c-baseline-row` | same span → `python3 -c "print(1)" --selftest` | `rc=2`, same one line | `rc=1`, 42 lines; `state=no_command` on rows 184 and 194 plus the digest/line pins they orphaned; `PIN_CHECK=unmet tally_pins=31 digest_pins=8 mismatches=2 unparsed=2 no_command=2 dropped=0 rebound=0 …` |

Cause (witness `check()`, lines 606-616): the rebound branch fired on `norm != base_bind[bkey]` with
`norm is None`, and the finding formatter then did `" ".join(norm)`; `main`'s blanket `except Exception`
(761-763) relabelled the `TypeError` as `PIN_CHECK_SETUP`, so the run printed no `pin … state=` line at
all. `count-c1.py` classifies rc 2 / no `PIN_CHECK=` line as `error`, so this was never green — it hid
the findings instead, which is the operability defect.

Fix: the rebound decision is now taken only when `norm is not None`; a pin whose bound command is
unresolvable falls through to the existing `no_command` branch (fatal, exit 1). One join site existed
(`grep -n 'join(' ` → line 616 was the only argv join; 655 joins `words` after the `words is None`
`continue`).

Arms added (both kill the witness):

- `x1_baseline_binding_disappears` — baseline row `foo` bound to `tools/foo.py`; current row same name,
  span `python3 ./tools/foo.py --selftest`. Expect unmet + `state=no_command`.
- `x1_baseline_binding_inline_code` — same with `python3 -c "…" --selftest`. Same expectation.

Falsifier that the arm is not vacuous: the two texts scored through the pristine witness module raise
`TypeError: can only join an iterable`; the copy scores `PIN_CHECK=unmet … no_command=1` and prints
`pin line=3 kind=tally prefix=FOO_SELFTEST state=no_command`.

Fuzz of neighbouring shapes (all `met=False`, no exception, in-process `check()` on a fixture tree):
pin-only cell, `..` path, absent instrument, unknown prefix, digest/line-count/truncated-digest on an
absent path, empty self-test cell, extra cell, non-ASCII instrument. See Limits item L1 for the one
shape that stays `met`.

## K5 — a multi-instrument prefix admits only its own family

Measured at the baseline `2d85e33d` (through `pin_bindings`, nothing executed):

| prefix | baseline bound argvs |
|---|---|
| `C1_SELFTEST` | `.ufo/waves/round-44/count-c1.py`, `.ufo/waves/round-45/count-c1.py`, `.ufo/waves/round-45/fixtures/mutants/count-c1.py` |
| `C2_SELFTEST` | `.ufo/waves/round-44/count-c2.py`, `.ufo/waves/round-45/count-c2.py` |
| `C3_SELFTEST` | `.ufo/waves/round-44/count-c3.py`, `.ufo/waves/round-45/count-c3.py`, `.ufo/waves/round-45/fixtures/mutants/count-c3.py` |
| the other 12 prefixes | 1 argv each |

So the old exemption (`len(set) > 1` → any new argv) covered exactly three prefixes, and every banked
member is the same instrument basename in a different round directory. At `b3e3453d` five pin keys are
absent from the baseline, three of them joins into those namespaces — all three are the same family:

```
r47 tracepoint catalogue (C2)  C2_SELFTEST  ('python3', '.ufo/waves/round-47/count-c2.py', '--selftest')
r48 junk-variant counter (C1)  C1_SELFTEST  ('python3', '.ufo/waves/round-48/count-c1.py', '--selftest')
r48 quota entry counter (C2)   C2_SELFTEST  ('python3', '.ufo/waves/round-48/count-c2.py', '--selftest')
```

Rule written: a new key whose prefix exists in the baseline is `rebound` when its argv is not in the
prefix's baseline set **unless** the new argv's instrument basename is one of that set's basenames.
Single-instrument prefixes behave exactly as before (exact membership). Cost on the real registry: the
three joins above have matching basenames → **0 rows red**; confirmed by `real=met` and `real-opaque=met`
in the acceptance run (and by the direct run below).

Arms added:

- `k5_namespace_new_instrument_rejected` — baseline `NS_SELFTEST` banked by `round-1/ns.py` and
  `round-2/ns.py`; a new row claims and runs `tools/stub.py` printing `NS_SELFTEST pass=3 fail=0`
  (self-consistent, so R11 cannot see it). Expect unmet + `state=rebound`. The pristine witness scores
  this text `PIN_CHECK=met` — the arm is not vacuous.
- `k5_namespace_family_join_admitted` — same baseline, new row runs `round-3/ns.py` (same basename,
  new round). Expect met, so the rule is a narrowing and not a freeze.

Deliberately unchanged (see Findings F3): a new row that re-runs an argv already in the set stays
admitted — it binds the same command to the same prefix and its pin must still match the observed text.

## Direct real-registry run (same tool, same flags as the `real` arm)

```
$ python3 -I -B .scratch/r49-Mo49ExecK5X1/mori-pin-check.py --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 \
    --repo $LANE --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes
REAL_EXIT=0                                   (wall 412.63 s)
```

`rebound=0` and `misattributed=0` at the real tip: the K5 narrowing and the X1 arm change cost no landed
row, and the 31 landed tally pins still bind.

## What the L1 must decide before landing

1. **Arm-set merge.** This copy's 69 arms = witness 65 + 2 X1 + 2 K5. Sibling seat
   `w1/Mo49ExecArmsBindUnlanded.md` reports its own witness-derived copy at 67 (F4/F5 arms). Landing both
   needs a union, and the SKILL.md self row (line 938) pin must then be repinned to the union's tally
   (`pass=60` at `b3e3453d` already disagrees with the witness's 65; the acceptance run above shows the
   counter's `real` arm stays met only because it measures the *lane* tool at `b3e3453d`, not the copy).
2. **K5 is a narrowing, not a closure by construction.** If a future instrument legitimately joins
   `C1_SELFTEST` under a different basename, it is now `rebound` and the registry must either reuse the
   family basename or take a new prefix. No landed row needs that today (0 breakages measured).

## Limits

- **L1 (LOW).** A `--selftest` span that `argv_ok` rejects *after* a valid command span, with no tally
  pin bound to it, is `ignore`, not a finding: `two_same_prefix_second_bad`
  (`` `python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`; `python3 ./tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0` ``)
  scores `PIN_CHECK=met`. Nothing false is claimed (no pin is bound to the junk span), so this is a
  reporting gap of the R7 class, not a false green.
- **L2 (LOW).** The K5 rule is a basename check: a committed stub at `.ufo/waves/round-9/count-c1.py`
  that prints `C1_SELFTEST …` and whose row claims that same path is still admitted. Closing that needs
  an explicit namespace cell in the registry (the round-48 critic's suggestion), i.e. a paired
  tool+registry change outside this seat.
- **L3.** I did not re-score the other round-48 classes (K2 env prefix, K3 pin deletion, K4 pins outside
  the self-test cell, K6 floor slack, K7 line-count rebinding, K8 rc-free PASS pins); my copy keeps the
  witness's behaviour there. The frozen 26 variants pass, which says nothing about those classes.
- **L4.** The X1 fix reports `no_command` for a disappeared binding and no longer emits a `rebound` line
  for it; a reader looking for the word `rebound` on that shape will not find it. The state is still
  fatal and still names row, line and prefix.
- **L5.** The two X1 arms are in-process (`check()`); the exit-code part is evidenced by the lane-variant
  runs (`rc=1`, pasted above), not by a git-fixture CLI arm inside `--selftest` (adding one would make
  the pinned tally depend on whether `git` is installed).
- **L6.** UNVERIFIED: I did not run `count-c1.py` with `--jobs 4` (contract's 10-minute figure) nor the
  round-48 counter; `--jobs 3` wall was 1258 s for 28 runs.

## Findings

| # | severity | finding | file / line |
|---|---|---|---|
| F1 | MED | X1: a junk row that makes a baseline row's bound command unresolvable produced `PIN_CHECK_SETUP can only join an iterable` (exit 2) and **no** `pin … state=` line, because the rebound formatter joined `None` and `main`'s blanket `except` relabelled the `TypeError` as a setup failure. Fixed: `norm is None` now falls through to `no_command` (exit 1); two arms added. | `.ufo/waves/round-49/controls/tool-r48-merged-witness.py:606-612` (rebound decision), `:616` (the `" ".join`), `:761-763` (the mask); fixed in `.scratch/r49-Mo49ExecK5X1/mori-pin-check.py:605-628` |
| F2 | MED | K5: the `len(set) > 1` exemption let any new argv join `C1/C2/C3_SELFTEST`. Closed to the instrument's own family (basename), which is what all three landed round-47/48 joins are; two arms added, one rejecting and one admitting. | `tool-r48-merged-witness.py:610`; fixed in the copy `:614-624` |
| F3 | LOW | A new row re-running an argv already banked by a namespace prefix is still admitted (duplicate authority for one command). Both rows must match the observed text, so nothing false is claimed; left open by design. | copy `:614-620` |
| F4 | LOW | A `--selftest` span rejected by `argv_ok` after a valid command span, carrying no pin, is silently ignored rather than reported. | copy `span_kind()` / `command_from_span()` |
| F5 | LOW | The copy's tally is 69 while the landed registry's self row pins `pass=60`; the union with `w1/Mo49ExecArmsBindUnlanded.md` (67) must be landed with a repinned self row, or the row goes red on the first landing. | `SKILL.md:938` |
| F6 | LOW | K5 rule cost: a future new instrument joining `C1/C2/C3_SELFTEST` under a different basename is now `rebound` and needs a new prefix or an explicit namespace cell. | copy `:614-624` |
