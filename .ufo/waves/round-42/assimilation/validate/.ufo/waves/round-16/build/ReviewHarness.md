# ReviewHarness — round-16 pin table and missing-tool-before review (read-only)

Seat: `MoriR16.ReviewHarness` (reviewer, leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scope: pin table and "missing-tool-before" measurement versus the historical bug claims. Read-only.
No execution: no gate, census, selftest, fixture run or build was run. No tool was installed or
updated. Digests were computed with `sha256sum`; structure was checked with `jq`; state was read
with `git status`/`git rev-parse`. Nothing was written except this report.

## Read-time state (changes may be in flight)

Observed 2026-10-20T08:48Z–08:51Z (UTC).

- HEAD `b83edc6ee3db6822382ab673d7e6e984e420f22f`. Uncommitted: `LOG.md`, `PROVINCE.md`,
  `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`; untracked `.ufo/waves/round-16/`
  and `corpus/knowledge/journal-cursor-window-r16.md`.
- **Not present at read time:** `tools/mori-round16-regressions.py`, `tools/mori-journal-window.py`.
  The harness and the production tool this seat reviews have not landed. The findings below are
  therefore about the specification and its pin/gate design, not about executed code.
- **In flight:** `.ufo/waves/round-16/fixtures/` holds 8 of the 16 specified packs
  (BootBoundary, CursorShape, ExactAnchor, KernelUser, MissingAnchor, TypedFields, UnitOom,
  UnitSignal). Missing: KernelSystem, ProcessSignal, RecordShape,
  MalformedCapture, ProducerFailure, Stderr, Bounds, AnchorValidation. No pin table for round 16
  exists yet. Any pin taken before all 16 packs settle would be stale.
- `.ufo/waves/round-16/frozen/` holds `entering-capability.json` (absence receipt) and
  `round15-spec.json` (copy of the round-15 spec).

## Verified clean (read-time digests, no execution)

1. **Round-15 pin table matches disk.** `.ufo/waves/round-15/expected.json`:
   - gate `tools/mori-round15-regressions.py` pinned `6a55c33c…`, current `6a55c33c…`.
   - frozen census pinned `0e41cb83…`, `.ufo/waves/round-15/frozen/mori-census.sh` `0e41cb83…`.
   - r14 helper `tools/mori-round14-regressions.py` pinned `533218a5…`, current `533218a5…`.
   - All 16 fixture packs match their pinned `sha256` (`BootArray` … `UnitUser`).
   - `boundary-expected.json` pins `boundary-fixtures/capture.json` `939881b7…`; current `939881b7…`.
2. **Round-16 entering production pins match disk** (`frozen/entering-capability.json`): all six
   entries match — `tools/mori-census.sh` `f1f8d1b6…`, `mori-silence-cases.sh` `34cd5770…`,
   `mori-round13-regressions.py` `23b753c1…`, `mori-round14-regressions.py` `533218a5…`,
   `mori-round15-regressions.py` `6a55c33c…`, `baseline-r10` `0993b235…`.
3. **Capability absence receipt is honest.** `git cat-file -e b83edc6…:tools/mori-journal-window.py`
   → exit 128, `capability_present: false`. The LOG entry ("capability absence … is not a
   production defect count") states the correct reading.
4. **Old census drift pin still red, not re-pinned.** `.ufo/waves/round-15/evidence/drift-current.json`
   (scope HEAD `26f6589`) reports `MORI_DRIFT` with named `+FINDING`/`-FINDING`/`SURFACE` changes.
   The baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` hash is unchanged (`0993b235…`).
   This is the receipt at `26f6589`, not a fresh run.
5. **Historical round-15 setup failure is fixed in the pin.** `.ufo/waves/round-15/build`
   `boundary-pin-red.json` (exit 2, `want_oom=False contradicts independently valid OOM records=1`
   on `boundary_rc124`) was an oracle-derivation bug. The current `boundary-expected.json` has
   `boundary_rc124`: `want_oom:false`, `want_signal:false`, positives `unavailable:timeout`, so the
   pinned expectation now matches the capture-failure rule.

## HIGH

### H1. The missing-tool "before" proves absence only, not any historical bug

- Spec (`wave1-spec.json`, shared context, and `WindowHarness` item): "missing tool at entering
  baseline records capability_absent, expected finite cases fail". Entering capability is absent
  (`frozen/entering-capability.json`).
- With the tool absent, every case (including OK-expecting controls such as `ExactAnchor`,
  `KernelUser`, `UnitOom`, `TypedFields`) fails identically. That run cannot distinguish "tool
  missing" from "tool wrong". It reproduces none of the claimed bug classes (MESSAGE leakage,
  foreign-boot acceptance, unbounded read, ignored rc/stderr/timeout). Those historical claims are
  not measured by it.
- The round-15 model is the opposite and is what round 16 lacks. Round 15 pinned a frozen
  defective census (`0e41cb83…`, from `git show 0fa5e0d`) and required it to reproduce the
  red state on each red-relevant case: `frozen_red_confirmed 34/34`, `frozen_inconclusive: []`
  (`evidence/red-before-final/run-manifest.json`, `c1-measurement.json`).
- Risk: the round-15 F1 defect (`.ufo/waves/round-15/build/ReviewHarnessGate.md:206-211`) was
  "any frozen failure counts as red_confirmed", which fabricated control confirmation. Under the
  round-16 exit map (`1 mismatch/capability_absent`) an absent tool would produce the same
  rc1 shape as a real behavioral red unless the reason is kept separate.
- Fix (recommend, not implement):
  - Count `capability_absent` in its own summary field, never as `red_confirmed`, never as a
    bug count.
  - Either add frozen mutant controls, one per claimed defect class, each required to reproduce
    its specific failure with a reason check (the r15 F1 fix shape), or explicitly scope the
    entering measurement as capability-only and do not cite it as bug red.
  - Each case in the entering run must carry `capability_absent` as its reason, so a later
    reader cannot mistake it for a behavioral failure.

### H2. The pin cannot represent "tool absent at entering baseline"

- Spec: "pin manifest includes all pack+tool digests" and "must validate every pack digest and
  tool digest before runs". Yet the same spec says a missing tool is recorded as
  `capability_absent` at entering, and `--tool PATH` is "optional".
- There is no defined digest sentinel for an absent tool. Consequences:
  1. A pin taken while the tool is absent has no tool digest to validate.
  2. A tool deleted or renamed after pinning would take the same `capability_absent` path as the
     entering baseline, and would be accepted silently instead of refused as tamper.
  3. A tool that appears after an entering pin (state flips absent → present) is unspecified.
- Fix: the pin records the tool state explicitly, e.g. `{"state":"absent"}` or
  `{"state":"present","sha256":"…"}`. Any run whose observed tool state differs from the pinned
  state is rc2 (tamper), and `capability_absent` is allowed only when the pin itself records
  absence.

### H3. The pin omits the gate's own bytes and the frozen/helper digests

- Round 15 pinned `gate_sha256`, `r14_helper_sha256`, `frozen_sha256`, and each pack digest with
  its expectations (`compare_expected`, `tools/mori-round15-regressions.py:880-940`; the
  `gate_sha256` check is at 902-906).
- The round-16 spec pins only pack and tool digests. Nothing pins the harness's own bytes or its
  expected constants. A gate edit after pinning (relaxing a `want`, adding a skipped case) is
  undetected by the pin.
- Fix: the expected table records the gate `sha256` and every expectation, and the run refuses
  with rc2 when they differ. Mirror the r15 check at lines 902-906.

### H4. Partial `want` fields let a wrong tool pass

- Each case asserts only "selected want fields" (`want: {"records_after_anchor":0}`). The spec's
  own invariant is "no numeric positive totals" on refusal, and "four separate positive counts"
  on success. A tool that emits numeric `positive_*` on an rc2 case passes unless that case happens
  to name the key.
- The no-echo rule ("stdout MUST NOT echo raw cursor or records") and the `PackStderr` canary
  ("secret-shaped canary never echo") are per-pack ideas, not harness-wide checks.
- Fix: the harness, not each pack, enforces for every case:
  - rc2 → no numeric `records_after_anchor` and no numeric `positive_*` keys;
  - rc0 → exact key set (no extra positive keys);
  - stdout and stderr never contain the anchor cursor string, any fixture record payload, or
    the canary.

## MEDIUM

### M1. Output inside the repo can make the run look like it moved

- The spec records "exact porcelain" at start and end and "refuses moving inputs". Output goes
  under the lane, so start and end porcelain differ by the run's own output, and the run marks
  itself moving.
- Round 15 handled this: `dirty_outside_harness_output_paths` (`tools/mori-round15-regressions.py:849`,
  compared at 1752-1753), and an output guard refusing `--output` inside a protected tree
  (line 1421). The round-16 spec mentions neither. The round-15 review F4/F5
  (`ReviewHarnessGate.md:222-238`) recorded exactly this defect.
- Fix: carry both into round 16: exclude the harness output paths from the moving comparison, and
  refuse `--output` inside frozen, fixture, expected, or pre-existing output trees.

### M2. Timeouts and producer-rc mapping can false-red

- The harness must not kill the tool before the tool's own `--timeout` fires. If the harness's
  subprocess deadline is shorter, `timeout:true` cases record a harness kill (rc -9), which
  mismatches the expected rc2 and produces a false red.
- Round 15's F3 (`ReviewHarnessGate.md:217-221`) was the same class: rc124/137 expectations
  mismatched the census mapping, a false red. Round 16's `ProducerFailure` uses rc5/124/137 and
  the `Bounds` pack uses timeout/overflow.
- Fix: the harness deadline exceeds the tool timeout by a stated margin. A harness-side kill is
  classified as `harness_timeout`, not as a tool result. The rc2 expectation for 5/124/137 is
  stated once and selftested for each code.

### M3. `--pin-fixtures` can silently re-pin tampered packs

- Pin mode regenerates the expected table from whatever packs exist now. A tampered pack can be
  re-pinned in one command with no record of the prior digest. The only protection is that the
  committed table shows up in `git diff`.
- Fix: pin refuses to overwrite an existing committed table without an explicit repin flag and a
  recorded reason; it records the prior digest. Pin only after all 16 packs settle (the spec says
  so; enforce it, do not rely on it).

### M4. CLI contract is inconsistent; a mistyped `--tool` becomes a silent baseline

- Interface: `--tool PATH --fixtures DIR --output DIR`. The fixture contract refers to a "normal
  `--expected PATH`" run, which is absent from the stated invocation. No defaults are given for
  `--tool`, `--fixtures` or `--expected`. The round-15 SKILL registry row gives defaults for each.
- `--tool` is described both as a required path and as "optional for missing-before". A mistyped
  path therefore looks like `capability_absent`, which is the entering baseline. The run exits 1,
  so it does not green-wash, but it records a false absence and can be cited as one.
- Fix: define defaults and an explicit `--tool-absent` (or state flag) for the entering run. A
  path that does not exist without that flag is rc2 setup.

## LOW

### L1. Active registry prose still describes a removed flag

- `SKILL.md:134` (r15 row) says `--no-frozen-control` "is selftest-internal and requires the hidden
  `--selftest-child`". The round-15 gate source has zero occurrences of either token
  (`grep -c 'no-frozen-control' tools/mori-round15-regressions.py` → 0), and
  `evidence/control-bypass-refused.json` shows both refused.
- The verifier routed this to round 16 (`corpus/lessons/round-15-verifier-spotcheck.md:282-286`).
  It was not corrected at read time: `SKILL.md` is not in the `git status` modified list.
- Fix: correct the active registry row in a lane-authored commit, and append (do not rewrite) the
  disposition, per the verifier's instruction. Do not copy forward the stale sentence into the
  round-16 row.

### L2. EXIT_STATUS string/number forms need explicit pinned cases

- The round-15 lesson requires both `EXIT_STATUS` `9` as a scalar string and as a number
  (`corpus/QUALITY.md` item 35; `journal-positive-evidence-r15.md`). The round-16
  `ProcessSignal` and `TypedFields` packs should pin both forms explicitly, so the pinned
  expectations cover the typed boundary rather than one form.

## Residual risk and verification gaps

- **Nothing executed.** All findings are static against the spec, the in-flight fixtures, and
  committed round-15 artifacts. No harness or production-tool behavior was observed.
- **Harness and production tool absent at read time.** H1–H4 and M1–M2 are design-level until
  `tools/mori-round16-regressions.py` and `tools/mori-journal-window.py` land. Re-read both, and
  the expected table, before relying on any of them.
- **Pin is self-attesting.** A pin re-taken after an edit is indistinguishable from a legitimate
  one except by reviewing the git diff of the expected table alongside the packs. This is an
  inherent limit of committed pins; M3 narrows it but does not close it.
- **Fixture coverage incomplete (8/16).** Fixture expectations were not reviewed beyond shape
  (`cases` count, unique ids, `want_id`/`want_rc` present). Semantic correctness of the remaining
  packs is unassessed.
- **Drift receipt is historical.** The round-10 pin's red state is the `26f6589` receipt, not a
  current run.

## Required fixes (ordered)

1. H2 + H3: pin records tool state (absent/present+digest) and gate bytes; run refuses on any
   difference (rc2 tamper).
2. H1: keep `capability_absent` separate from red-confirmed; add frozen mutant controls per
   claimed defect class, or scope the entering measurement explicitly as capability-only.
3. H4: harness-wide invariants (rc2 → no positive totals; rc0 → exact key set; no cursor/payload/
   canary echo on stdout or stderr).
4. M1–M4: output exclusion and guard; harness deadline margin and rc mapping selftested for
   5/124/137; pin refuses silent overwrite; define CLI defaults and an explicit absent-tool flag.
5. L1: correct `SKILL.md:134` in a lane commit; append the disposition.
6. L2: pin both `EXIT_STATUS` forms in the ProcessSignal/TypedFields packs.

Re-read `tools/mori-round16-regressions.py`, `tools/mori-journal-window.py`, and the full
`.ufo/waves/round-16/fixtures/` before the L1 verification pass; the fixture set and the expected
table were still changing at read time.
