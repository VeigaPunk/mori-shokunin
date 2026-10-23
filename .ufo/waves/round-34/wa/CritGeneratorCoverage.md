measured 2026-10-23T06:13:18Z
# CritGeneratorCoverage — static attack on the C1 counter's scenario generator

Scope: the generator in `.ufo/waves/round-34/count-c1-a1.py` (frozen; never modified),
its 12 fixed seeds, and the random draw. Question: which R3/R5 rule *interactions* can
never be drawn, and does the landed tool `tools/mori-disk-rate.py` handle each of them
per `contract.md`?

- Lane `L = /home/vgpnk/Projects/shokunin/mori-shokunin`; revision under attack
  `8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3` (branch master).
- Scratch `S = /fast/scratch/hyaku/mori-r34/a2-CritGeneratorCoverage` (all scratch
  artifacts). The counter was imported read-only via `importlib` (`S/cover_enum.py:11-14`,
  `S/witness.py:11-14`, `S/survivors.py:11-14`); its bytes are unchanged
  (`sha256 c14c3494…b181e2` on disk == `git show 8d56809:.ufo/waves/round-34/count-c1-a1.py`).
- Tool bytes at the tip are the judged object and are byte-identical to the working copy
  (`sha256 370932de…fee76b` both ways).
- Baseline: `timeout 900 python3 L/.ufo/waves/round-34/count-c1-a1.py 8d56809… --seed 424242`
  → `fixed_pass=12/12 random_pass=300/300`, `coverage=ok`, `live=ok`, `C1=met`, exit 0.

## Axes

1. **Drawability** — is each R3×R5 interaction reachable by the generator at all?
2. **Tool conformance** — on each *undrawn* interaction, does the landed tool produce the
   contract's answer? (offline witness each, built by hand, not by the generator)
3. **Counter discrimination** — can the counter tell a tool that gets an undrawn
   interaction wrong from one that gets it right? (mutant survival through the counter's
   own `score_seeds`/`live`/`fed_live`)

## Method

- `S/cover_enum.py`: the oracle's per-device `(class, state)` over the 12 fixed seeds and
  4000 fresh random seeds.
- `S/enum_full.py`: the **R3 marker space** — for a device with a directory in
  `<sysfs>/class/block`, the four markers are (has `partition` entry, has `device` entry,
  `slaves` dir exists, `slaves` dir non-empty), 16 combinations; and the **R5 state
  space** — per device `(in A, in B, malformed A, malformed B, counter fell)`.
- `S/witness.py`: 18 hand-built offline witnesses (W-A … W-R), each checked against the
  contract's expected value *and* against the frozen oracle.
- `S/final_sweep.py`: 17 R3 shapes × 18 meaningful R5 states = 306 combinations, hand-built.
- `S/survivors.py`, `S/mutants78.py`: mutants scored through the counter's own
  `score_seeds` (with its namespace sandbox), `live()` and `fed_live()`.

## Finding 1 — R3 marker space: 12 of 16 shapes can never be drawn

`S/enum_full.py` output (3000 fresh seeds; counts are devices drawn):

| shape (partition, device, slaves_dir, slaves_nonempty) | contract class | drawn |
|---|---|---|
| (F,F,F,F) | virtual | **NEVER** |
| (F,F,F,T) | stacked | **NEVER** (impossible: non-empty implies dir) |
| (F,F,T,F) | virtual | YES 2926 |
| (F,F,T,T) | stacked | YES 2935 |
| (F,T,F,F) | disk | **NEVER** |
| (F,T,F,T) | stacked | **NEVER** |
| (F,T,T,F) | disk | YES 6031 |
| (F,T,T,T) | stacked | **NEVER** |
| (T,F,F,F) | partition | YES 9127 |
| (T,F,F,T) | partition | **NEVER** |
| (T,F,T,F) | partition | **NEVER** |
| (T,F,T,T) | partition | **NEVER** |
| (T,T,F,F) | partition | **NEVER** |
| (T,T,F,T) | partition | **NEVER** |
| (T,T,T,F) | partition | **NEVER** |
| (T,T,T,T) | partition | **NEVER** |

**Cause (generator code).** The generator assigns each class exactly one marker and writes
only that marker: `count-c1-a1.py:171-172` creates the `slaves` dir for every non-partition
class; `:173-174` writes the `partition` entry only for partitions; `:175-176` writes the
`device` entry only for disks; `:177-178` populates `slaves` only for stacked names.
So **no drawn device ever carries two markers**, and the R3 order
(partition → slaves → device → virtual, `count-c1-a1.py:63-69`; tool `mori-disk-rate.py:192-199`)
is never exercised at a branch point.

Witnesses (hand-built, offline): W-D partition+non-empty slaves → tool `partition`;
W-E device+non-empty slaves → tool `stacked`; W-K partition+device → tool `partition`;
W-L stacked+device → tool `stacked`; W-P no slaves dir, no markers → tool `virtual`;
W-Q no partition/device but non-empty slaves → tool `stacked`.
**All six match the contract; the frozen oracle agrees on all six.**

## Finding 2 — R5 state space: 26 of 32 tuples can never be drawn

`S/enum_full.py` draws exactly six tuples, always of the form "present in both samples"
or "present in one, absent in the other, never malformed together with absent":

drawn: `(F,T,F,F,F)`, `(F,T,T,F,F)`, `(T,F,F,F,F)`, `(T,F,F,T,F)`, `(T,T,F,F,F)`, `(T,T,F,F,T)`
never: the other 26 — including every tuple where a **malformed line coexists with a
missing line**, and every tuple where a **malformed line coexists with a falling counter**.

**Cause (generator code).** `count-c1-a1.py:195-199` corrupts a line only when `r > 0.92`.
But `r` was already consumed by the state draw at `:183-192`, whose branches assign
`ina`/`inb` — so the `r > 0.92` branch is only reached from the final `else` at `:191-192`,
which always sets `ina = inb = True`. Corruption therefore *never* reaches a device that is
absent from the other sample, and never reaches a device whose counter fell.

Witnesses: W-F bad line in A, no line in B → tool `bad-line`; W-G no line in A, bad line
in B → `bad-line`; W-H valid A with falling counter, malformed B → `bad-line`;
W-R malformed A only, device in sysfs only → `bad-line`.
**All four match the contract and the frozen oracle.**

## Finding 3 — `absent` is only ever attachable to `partition`

The `(class, state)` grid has 30 cells. Over the 12 fixed seeds, 4000 fresh random seeds,
and 200 independent 300-scenario windows, these are never drawn:

- `(disk, absent)`, `(stacked, absent)`, `(virtual, absent)` — **never drawn, in any seed.**
- `(unknown, absent)` — never drawn **and logically unreachable**: `absent` means no line in
  either sample, so the device entered the R4 set only via the sysfs listing, so its
  directory exists, so R3 cannot return `unknown`. Exhaustive search over all sample
  combinations confirms no input produces it (`S/impossible.py`, `S/final_sweep.py`: the
  306-combination sweep produces 29 of 30 pairs; `unknown/absent` is the only one it cannot).

**Cause (generator code).** `count-c1-a1.py:189-190`: the `absent` branch is reachable only
when `cls.get(n) == "partition"`. Non-partition classes fall through to `:191-192`, which
always emits a line in both samples.

Witnesses: W-A disk+absent → tool `absent`/`null`, host null; W-B stacked+absent → `absent`;
W-C virtual+absent → `absent`. **All three match the contract and the frozen oracle.**

## Finding 4 — the counter's coverage clause cannot detect any of this

`count-c1-a1.py:409` requires only `set(STATES) <= seen["state"] and set(CLASSES) <= seen["class"]`
— the 6 states and 5 classes *separately*, never the 30 pairs. `seen` is filled from the
**oracle's** expectation (`:249-250`), not the tool's, so the clause is about the generator,
not the tool. Measured over 400 windows of 300 scenarios: 0 shortfalls (all six states and
all five classes in every window), while the four `absent` pairs are missing from 200/200
windows. The clause is satisfied while a seventh of the grid is permanently dark.

## Finding 5 — mutants exploiting every undrawn interaction SURVIVE the counter

Scored through the counter's own `score_seeds` (namespace sandbox), `live()` and `fed_live()`,
at the counter's own 300-random-seed count (`S/survivors.py`, `S/mutants78.py`):

| mutant | undrawn interaction exploited | fixed | random | live | fed | verdict |
|---|---|---|---|---|---|---|
| baseline (landed tool) | — | 0/12 | 0/300 | ok | ok | — |
| M1 `absent` honoured only for `partition` | absent×{disk,stacked,virtual} | 0/12 | 0/300 | ok | ok | **survived** |
| M2 `device` checked before `slaves` | R3 order, disk+slaves | 0/12 | 0/300 | ok | ok | **survived** |
| M2b `partition` checked last | R3 order, partition+slaves | 0/12 | 0/300 | ok | ok | **survived** |
| M3 `absent` tested before the malformed sets | R5 order, bad-line vs absent | 0/12 | 0/300 | ok | ok | **survived** |
| M4 `bad-line` only when present in both | R5 order, bad-line vs gone/new | 0/12 | 0/300 | ok | ok | **survived** |
| M5 last line for a name wins (oracle's reading) | R1/R2, duplicate name | 0/12 | 0/300 | ok | ok | **survived** |
| M6 empty basis reports `0`, not `null` | R7, empty basis | 0/12 | 0/300 | ok | ok | **survived** |
| M7 one token count per sample | R2, mixed token counts | 0/12 | 9/300 | ok | ok | killed |
| M8 `slaves` dir ignored | R3, stacked membership | 6/12 | 208/300 | live-class:dm-0 | fed-mismatch | killed |

The live arm adds no discrimination here: on this host every `/sys/class/block` entry
carries exactly one marker — `dm-0` (F,F,T,T), the four disks (F,T,T,F), the six
partitions (T,F,F,F) (`S/host_inventory.py`) — so no real device distinguishes the R3 order
either, and the host's `/proc/diskstats` has only 20-token valid lines, so the live arm
never sees a malformed or absent device at all.

## Finding 6 — the landed tool agrees with the frozen oracle on every hand-built interaction

`S/final_sweep.py`: 17 R3 shapes (16 marker shapes + no-directory) × 18 meaningful R5
states (each sample valid / malformed / absent, × counter-fell) = **306 combinations, all
built by hand**, tool vs frozen oracle: **306/306 agree**. `S/positions.py`: every
non-name token index `corrupt()` can reach (0, 1, 3, 9, 13) × 5 bad values × 3 token
counts — **0 mismatches**. `S/witness.py`: 18 named witnesses, 17 agree with both the
contract and the oracle.

**The one divergence (W-M):** the same device name appearing twice in one sample, with a
malformed line first and a valid line second. The tool reports `bad-line` (its `malformed`
set is sticky, `mori-disk-rate.py:100-105`); the frozen oracle reports `ok` (its `parse`
overwrites `out[name]` per line, `count-c1-a1.py:46-53`). Contract R5 says *"bad-line (a
bad line in either sample)"* — the tool's reading is the one the contract text supports;
the oracle's last-line-wins reading is the counter's own implementation choice
(`count-c1-a1.py:49` assigns `out[name]` unconditionally). A real `/proc/diskstats` never
repeats a device name, and the generator emits each name at most once per sample
(`:180-202`), so this input is unreachable in practice. **This is a defect of the frozen
oracle, not of the landed tool.** It is reported, not fixed: the counter is frozen.

## Residuals (report only — the counter is frozen and was not modified)

1. **The counter cannot discriminate the R3 order.** M2 and M2b violate contract R3 and
   still yield `C1=met`. The landed tool implements R3's stated order
   (`mori-disk-rate.py:192-199`), but the counter does not certify it.
2. **The counter cannot discriminate R5's precedence order.** M3 and M4 violate contract R5
   and still yield `C1=met`.
3. **The counter cannot certify `absent` for non-partition classes** (M1) nor the R7
   empty-basis rule (M6).
4. **The coverage clause is weaker than it looks**: it certifies 6 states and 5 classes
   separately, so a generator that never produced `(disk, absent)` still reports
   `coverage=ok` — as this one does, on 200/200 windows.
5. **The frozen oracle's duplicate-name reading differs from contract R5 text** (Finding 6).
   If the generator emitted a repeated device name, the landed tool would be scored
   `C1=unmet` while being contract-correct.
6. **No flake found in the coverage clause.** 400 windows of 300 scenarios produced no
   window missing a state or a class. An earlier per-pair wobble (`unknown/new` absent in 1
   of 40 windows) sits inside a pair the clause never tests and did not recur over 200
   windows.

## Smallest safe correction

None in the tool and none in the counter (both frozen). The safe corrections are in the
**evidence** the L1 records, not in the judged objects:

- Record the eight undrawn R3 marker shapes that are physically realisable, the 26 undrawn
  R5 tuples and the four permanently-dark `(class, absent)` cells as a **declared coverage
  limitation of P-C1-A1**, alongside the contract's existing residual list. The claim "the
  tool matches the counter's oracle on the 12 fixed and 300 drawn scenarios" is true and
  remains true; the *counter's* discriminating power over R3/R5 order is the residual.
- Carry the hand-built witnesses (W-A … W-R, notably W-D, W-E, W-F, W-G, W-H, W-K, W-L,
  W-P, W-Q, W-R) as out-of-counter evidence that the landed tool implements the contract's
  R3 order and R5 precedence on the interactions the counter cannot reach.
- The mutant table is the concrete statement of the limitation: seven contract-violating
  tools would each be scored `C1=met`.
- A *counter* change is safe post-freeze only as a **new** counter, not an edit to
  `count-c1-a1.py`: a new counter would add the multi-marker and mixed-state draws and a
  pair-level coverage clause. This round's kill rule and the `C1=met` label remain bound to
  the frozen counter.

## Tooling

No tool was installed or updated. Python 3.14.8 (system), `git` and `awk` as shipped.
`pacman` was not invoked (all pacman transactions are PAUSED host-wide per the operator
directive). No network fetch, no block device, no settings file, no harness edit.
Every command was run under `timeout` (≤900 s) with the scratch tree under
`/fast/scratch/hyaku/mori-r34/a2-CritGeneratorCoverage`; no background job was left
running and no process tree outlived the seat.

VERDICT: no defect found — the landed tool handles every undrawn R3/R5 interaction per
contract (306/306 hand-built combinations agree with the frozen oracle; 17 of 18 named
witnesses agree with both, the 18th being a defect of the frozen oracle, not the tool).

VERDICT: survived — the counter cannot discriminate the R3 order (M2, M2b), the R5
precedence order (M3, M4), `absent` outside the partition class (M1), the R7 empty-basis
rule (M6), or the R1/R2 duplicate-name reading (M5): seven contract-violating mutants
all score `C1=met`.

VERDICT: supported — the claim "the tool matches the counter's oracle on the 12 fixed
seeds and 300 drawn scenarios" (measured: `fixed_pass=12/12 random_pass=300/300`,
`C1=met`, exit 0 at the tip), with the counter's *discriminating power* over R3/R5 order
reported as a declared residual rather than amended.
