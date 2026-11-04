# Mo85C01Critic — round 85 w1 critic (read-only)

Date 2026-11-04; evidence snapshot 08:27–08:29 -03:00 at lane HEAD `91f657f6`
(`git diff --stat ab260865..worktree` for the three counters empty at snapshot; the wave was
live — untracked `w1/`, `battery-r85.txt`, `make-receipts.sh`, corpus edits — so bytes may have
moved after the snapshot; every number below is from my own runs unless marked [L1] for
`evidence/controls-r85.txt` (A4-updated, dated 08:23:09)).

Scratch: `/fast/scratch/hyaku/mori-r85/Mo85C01Critic/` (deleted before yield). No lane file
edited. Read-only git only. No tools installed.

## 1. Verdict table

| claim | reachable-by-do-nothing-control? | same-sentence? | harm? |
|---|---|---|---|
| C1 operability | **No** — skipping the arms reads `C1=unmet … arms=15 harness=stub missing=…` rc 1 (mine, at `2cc4b1ae` and at HEAD `91f657f6`) | 2 disclosed divergences (§5.1); target line prefix-exact | none found (§6.1) |
| C2 calibration | **No** — no receipts at either revision reads `C2=unmet receipts=0 harness=absent` rc 1 (mine) | 2 divergences, both amendment-disclosed, one mis-described (§5.2) | none found (§6.2) |
| C3 depth | **Yes** — the freeze commit alone satisfies P-C3; the counter reads met at the entering revision's subject/host bytes (mine, rc 0, 18.3 s). Ruling: **capability acquisition, not an empty claim**, under the disclosure rules in §3.3 | 1 field-order divergence (§5.3); A3 closed the verdict gap | none found (§6.3) |

All three claims are falsifiable by construction and none is reachable by a stub: the C1 do-nothing
cannot fake killed=2 (the kill rule runs the mutated r84 counter's own selftest), the C2 do-nothing
cannot fake bound=5 (hashes are computed from git bytes), and C3's defeat control (census stub with
no `MORI_DRIFT:` line) reads unmet [L1, controls-r85.txt §C3 defeat].

## 2. Q1 — distinct axes, separability

Distinct axes confirmed: C1 operability, C2 calibration, C3 depth; C2/C3 sit on the lane's lowest
score (5), satisfying AXES.md's lowest-axis rule.

Separability holds — each counter grades only its own subject's bytes at R:

- **C1** reads `.ufo/waves/round-84/count-c1.py` at R (count-c1.py:41 SUBJECT; loader at
  :329-332) plus its own selftest in scratch. No C2 or C3 byte touched.
- **C2** reads the three receipts at R and each bound path **at the receipt's own `# rev:`**
  (post-A1 `make_loader`; A2 diff hunk `grade(loader, rev_ok, make_loader)`). Bound paths:
  `tools/mori-record-sweep.py`, `tools/mori-claim-sweep.py`, and the three r85 counters.
- **C3** reads `tools/mori-census.sh`, the r10 baseline, the r82 snapshot/classification and
  `.ufo/waves/round-83/count-c2.py` at R, and runs the census read-only against the fleet root.

Shared bytes, named: (a) the three r85 counters are simultaneously C2's bound paths and the
instruments grading C1/C3 — pre-wave freeze bytes, not a sibling's landed work, so no causal
coupling; (b) `after-r85.txt` must carry `C1=met` in its body, so C2's receipt *documents* C1's
after value — but the counter only greps the token (shape, not truth, §5.2 note 3); (c) no claim's
after-value depends on a sibling seat's after-value: the arms (C1), the receipts (C2) and the
counter (C3) are disjoint landings.

## 3. Q2 — do-nothing reachability (my runs)

Cheapest control per claim = run the frozen counter at a revision that skips the claimed work.
All from the lane worktree, scratch under my seat dir.

### 3.1 C1 — not reachable by do-nothing

```
$ python3 -I .ufo/waves/round-85/count-c1.py 2cc4b1ae… --scratch $S/c1-enter
C1=unmet mutants=2 killed=0 survivors=2 total=2 arms=15 harness=stub missing=killed_mutant_with_coupling_not_equivalent,duplicate_coupling_not_equivalent rev=2cc4b1ae35a8
rc=1
```
Identical unmet at HEAD `91f657f6` (arms not yet landed at snapshot): rc 1, `rev=91f657f696a7`.
Matches [L1] controls-r85.txt byte-for-byte. Detector green: `C1_COUNTER_SELFTEST pass=18 fail=0`
rc 0 (mine). The target requires landing real arms; a label-only stub fails the kill rule (the
mutated selftest would not go red), so the counter cannot be flattered by the named stub class.

### 3.2 C2 — not reachable by do-nothing

```
$ python3 -I .ufo/waves/round-85/count-c2.py 2cc4b1ae…      → C2=unmet receipts=0 harness=absent rc=1
$ python3 -I .ufo/waves/round-85/count-c2.py 91f657f6       → C2=unmet receipts=0 harness=absent rc=1
```
Detector green: `C2_COUNTER_SELFTEST pass=18 fail=0` rc 0 (mine, post-A2 bytes). The three
receipts must exist at R with verifying hashes at their own `# rev:`; the grammar cannot be
satisfied by an absent or header-only file (A2's loose parser turns malformed headers into named
problems rather than silent passes).

### 3.3 C3 — reachable without any seat work; ruling: capability acquisition, honestly disclosed

- At `2cc4b1ae` the counter file does not exist: `git cat-file -e 2cc4b1ae…:.ufo/waves/round-85/count-c3.py`
  → `fatal: path … exists on disk, but not in '2cc4b1ae…'`, rc 128 (mine) — the before value is the
  absence of the instrument, exactly as A4 restated it.
- The counter itself runs and reads met at the entering revision's subject/host bytes (mine, HEAD
  bytes, 18.3 s):
  `C3=met observed=3 aa=stable own_tokens=64 subject_tokens=64 subject_deltas=0 unmatched=0 unnamed=0 detector=green rev=2cc4b1ae35a8` rc 0 —
  matching [L1] controls-r85.txt. Detector green: `C3_COUNTER_SELFTEST pass=20 fail=0` rc 0 (mine).

Ruling: **capability acquisition, not an empty claim** — with the limits stated. AXES.md
*Capabilities* admits a row only through a demonstrated run; the demonstration exists twice
([L1] and mine). What the claim must not say is that the subject changed: host bytes are
unchanged since r82/r83 and the retroactive met was knowable before the wave ran. The claim's
real content is "the lane can now derive the reconciliation itself instead of asking the subject
to grade itself", which is genuinely new machinery (the defeat control exercises it; my retroactive
run exercises the live path). The report must (a) quote the disclosure that the retroactive met is
not the before value, (b) enter the capabilities row with first-working round 85, and (c) claim no
freshness/coverage move off this counter.

## 4. Q3 — frozen-before-data

- The freeze is real and complete: `ab260865` (2026-11-04 08:00:25 -03:00) adds exactly
  `contract.md` (131 ln), `count-c1.py` (378), `count-c2.py` (311), `count-c3.py` (377),
  `evidence/controls-r85.txt` (30) — nothing else. Entering revision `2cc4b1ae` is 07:46:50,
  i.e. the counters were frozen after the entering revision and before any after-value: no
  `after-r85.txt`, `record-sweep-r85.txt` or `claim-sweep-r85.txt` exists yet (evidence dir at
  snapshot holds only controls + battery + an untracked HTML).
- Four amendments, all committed pre-receipt: A1 `79bb4ed8` 08:12 (C2 binding verified at the
  receipt's own rev — code fix, predicate unchanged), A2 `4ffd5a2d` 08:15 (header-block grammar
  clarifications + selftest 15→18), A3 `89f82eac` 08:16 (C3 requires the subject's `C2=met`
  verdict + selftest 19→20), A4 `91f657f6` 08:23 (truthful C3 entering control in contract and
  controls receipt). None changes a target, kill rule, population or class value; A3/A4
  *strengthen* (verdict token; honest rc-128 entering form). The freeze rule bars *narrowing*
  after data; nothing here narrows.
- One discipline tension to disclose, not a violation: a `C3=met` reading existed on record in
  the frozen controls (07:59:58, pre-A3 bytes) before A3 changed the counter's semantics
  (08:16). Strengthening after a recorded met is not goalpost-moving, but the after run must be
  produced by the post-A3 bytes — [L1] re-measured at 08:23:09 and my run confirms the same
  line, so the record is consistent. The report should pin the counter bytes (sha256) that
  produced the after value.
- Two prose defects in the amendment layer itself (§5.2 notes 1–2): A2 asserts "the contract's
  rule list now states it" for the ≥3-word limits rule, but contract.md:77-78 still reads only
  `<text containing the word "limit">` (the frozen section correctly cannot be rewritten; A2's
  wording is what is false), and the frozen defeat-control sentence contract.md:86-87
  (`C2=unmet headers=<receipt>`) is not producible by the counter — superseded by A2's
  `mismatch>=1` wording, which the amendment records.
- Uncommitted worktree edits observed during the wave (`count-c3.py` `M` at ~08:17, resolved by
  snapshot; corpus/SKILL edits) are seat landing work, not counter tampering: at snapshot
  worktree counters == HEAD == committed A4 bytes.

## 5. Q4 — same-sentence (contract ↔ counter ↔ receipt label), with line numbers

### 5.1 C1

| # | contract | counter | divergence |
|---|---|---|---|
| 1 | target `C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met` (contract.md:22, :52) | printed line appends ` rev=<12hex>` (count-c1.py:371) | benign suffix; same convention in the entering control [L1]; not a mismatch |
| 2 | pristine selftest "green with exactly 17 arms **and carries both new arm labels**" (contract.md:23-24) | labels enforced as **source-bytes markers** (count-c1.py:49-52, :105-106, :349-356); `arms_ok()` (count-c1.py:109-114) which checks `PASS <label>` in pristine **output** is dead in the met path (called only from selfcheck :236-244) | the label clause is enforced weaker than written (a real-but-mislabeled arm would pass). A2 bullet 1 converts this into a named limit ("an arm whose name is present but whose assertion is vacuous is the round's mutation-probe finding, not a met-path clause"). Disclosed; the kill rule still dominates (a vacuous arm cannot kill X1/X2). Keep the limit in the report verbatim. |
| 3 | kill rule wording (contract.md:28-31) | count-c1.py:14-18 + `green()`/`killed()` :91-98, met gate :168 | equal (rc≠0 OR `fail=<n>`, n>0, conditional on green pristine; unanchored/empty excluded from the count) |
| 4 | r84 no-harm clause `C1=met … total=4` (contract.md:25-26) | R84 regex :58 + re-run :362-371 | equal |

### 5.2 C2

| # | contract | counter | divergence |
|---|---|---|---|
| 1 | rule list: `# limits: <text containing the word "limit">` (contract.md:77-78) | `weak-limits` also requires ≥3 words (count-c2.py, A2 version ~:112-115) | counter stricter than the frozen rule list. Disclosed by A2 bullet 3 — **but A2 mis-describes its own fix**: it says "the contract's rule list now states it", and the rule list does not (it cannot, being frozen). The rule lives only in the amendment. Requires the report/lesson to state that. |
| 2 | defeat control "a receipt without headers reads `C2=unmet headers=<receipt>` rc 1" (contract.md:86-87) | no `headers=<receipt>` literal exists anywhere in count-c2.py (only `RECEIPT <name> headers=%d rev=…` :192-196) | the frozen sentence describes an unproducible output. A2 bullet 4 supersedes it (`mismatch>=1`); the frozen body text contradicts the amendment by design. Report must cite A2 as authoritative. |
| 3 | "every bound path's bytes **at that revision** hash to the stated sha256" (contract.md:65-66) | pre-A1 code verified at the graded tip; A1 fixed it (`make_loader(rev)`) | was a code-vs-predicate defect, fixed pre-data by A1 with a measured probe; closed. Residual named: the `summary` check greps the receipt body for its token (`C1=met`, `RECORD_SWEEP`, `CLAIM_SWEEP`) — shape-checked only; a receipt can quote `C1=met` before C1's run exists. Not machine-checkable; acceptance must re-run `count-c1.py R` live and the report must say the tokens are receipt-shape, not live grades. |
| 4 | receipt labels (contract.md:71-75) | RECEIPTS tuple tokens (`C1=met`, `RECORD_SWEEP`, `CLAIM_SWEEP`, count-c2.py:31-39) | equal |
| 5 | target (contract.md:62, :83) | printed line appends ` detector=green rev=<12hex>` (count-c2.py:306) | benign suffix |

### 5.3 C3

| # | contract | counter | divergence |
|---|---|---|---|
| 1 | target `C3=met observed=3 aa=stable own_tokens=N subject_tokens=N unmatched=0 unnamed=0` (contract.md:94, :111) | printed tail `…own_tokens=%d subject_tokens=%d subject_deltas=%d unmatched=%d unnamed=%d` (count-c3.py:359-362) | **field-order divergence**: `subject_deltas` interleaves, so the frozen target is not a contiguous substring of the emitted line. A3's bullet documents the exact tail. The report must quote the actual bytes; the r86 contract should pin the actual tail (or the counter should print the target-ordered form). |
| 2 | subject "prints a `C2=met` tail" (contract.md:98-99) | pre-A3 checked only rc 0 + `live=derived`; A3 added `verdict=met` (count-c3.py:342) | was a code-weaker-than-sentence gap; A3 closed it pre-data with selftest 19→20 (`subject_verdict_required`). Closed. |
| 3 | classes/derivation table (contract.md:106-109) | `derive()` count-c3.py:78-89, `CLASS_WORD` :47 | equal (the frozen r83 table; `unexplainable` never equals a derived class by construction) |
| 4 | three stable observations exiting 1 (contract.md:95-98) | `observe_three` rc==1 ∧ non-empty ∧ identical (count-c3.py:285-291) | equal |

### 5.4 C1 provenance anchor divergence (false-provenance class, must be disclosed)

contract.md:32-35 attributes the two-mutant population to Mo84R01C1.md §5 and pins the anchors at
`.ufo/waves/round-84/count-c1.py:150-151`. Verified at `2cc4b1ae`:

- r84 counter :150-151 = `if not k and coupling is not None:` / `coupled = all(base.count(marker) == 1 for marker in coupling)` — the r85 MUTANTS table matches this byte-for-byte, 1× occurrence (0× for the r83 spelling).
- Mo84R01C1.md §5's table (:250-256) records X2 as `coupled = base.count(coupling) == 1 → >= 1`, measured on the **r83** counter (:177-178), not on r84 bytes.

So the X2 anchor text differs between the cited measurement and the frozen population (X1's text
is identical in both counters). The carry-over is semantic, not textual. The report must not
claim the r84 reviewer measured these exact r84-byte anchor strings; it should state the r85
counter re-pinned X2 to the refactored r84 line and that the survival semantics were re-measured
directly (my runs: both survive at the entering revision, both `rc=0`).

## 6. Q5 — no-harm

1. **C1 cannot reduce the r84 counter's coverage.** Deleting an old arm or breaking the frozen
   mutants would flip the r84 counter's frozen 4-mutant line, and the met path re-runs the r84
   counter at R and regex-checks `C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4`
   (count-c1.py:58, :362-371) — enforced, not decorative. Arms growth 15→17 is additive.
2. **C2's grammar cannot flatter an honest miss.** Every failure mode lands in `PROBLEM` lines +
   `mismatch` → `C2=unmet`; A2's loose parser specifically closes the silent-header blind spot
   (a malformed second `# rev:` is now `duplicate-rev`/`bad-rev`, a malformed sha line is a
   counted `malformed-binding`). The one stricter-than-contract check (≥3-word limits) is
   disclosed; the receipt template in the selftest satisfies it.
3. **C3 is detection-only.** Census runs from scratch copies with `MORI_SHOKUNIN_ROOT=<fleet>`,
   `HYAKU_SCRATCH` pinned to the counter's scratch; no lane or host state is written. The
   reconciliation adds a real invariant (a future subject/classification drift flips
   `unmatched`/`unnamed` → unmet) rather than masking one. No coverage/freshness/adjacency claim
   is smuggled in by it, provided the report keeps C3 in depth (§3.3c).
4. **No axis verdict is endangered by the others.** The three landings are disjoint (§2); the
   only cross-claim coupling is documentation (the after receipt quoting C1's tail).

## 7. Required before the report may claim admission

1. Quote actual emitted tails, not the frozen target strings, wherever the report cites a counter
   line (C3's `subject_deltas` interleave; C1/C2's `detector=green rev=` suffixes), and log the
   C3 field-order divergence in the round lesson as the F-class residual.
2. State that the C2 defeat-control literal `C2=unmet headers=<receipt>` (contract.md:86-87) is
   superseded by A2's `mismatch>=1` form, and that A2's "the contract's rule list now states it"
   is inaccurate — the ≥3-word rule lives in the amendment only (contract.md:77-78 unchanged).
3. Disclose the X2 anchor-text carry-over (r83 `coupled = base.count(coupling) == 1` per
   Mo84R01C1 §5 vs the frozen r84-byte anchor `coupled = all(base.count(marker) == 1 for marker
   in coupling)`), and present X1/X2 as semantics inherited, anchors re-pinned and re-measured.
4. Keep A2's C1 named limit verbatim in the report (label-in-bytes enforcement, vacuous-arm case
   left to the mutation probe) — it is the honest description of the met path.
5. Pin the sha256 of the counter bytes that produced each after value (A1-A3 changed two
   counters after the freeze; the after runs must be attributable to post-A3 bytes).
6. Mark C2's summary tokens as receipt-shape checks; acceptance re-runs `count-c1.py R` live so
   `C1=met` in `after-r85.txt` is corroborated by a live run, not just quoted.
7. When the arms land (17), update every citation of the r84 selftest tally to 17 — QUALITY 172
   still says `pass=11` (D84-2); failing to update it in the same round that moves the number to
   17 would re-commit D84-2 on this round's own landing.
8. Enter the C3 capabilities row with first-working round 85 and the retroactive-met disclosure;
   claim no freshness/coverage/subject-state move from C3.

Non-blocking: the pre-arm `battery-r85.txt` (rev `4ffd5a2d`, 08:15:32) predates A3's count-c3
change; it pins no r85 counter selftest (r84 command list), so no staleness — but a post-A4
battery receipt would be cleaner if the report cites detector greenness per counter (my runs
already supply 18/18/20 at A4 bytes).

## 8. Verified / not verified

**Verified (my own runs at snapshot):** C1 entering + HEAD unmet lines and rc; C2 entering + HEAD
unmet lines and rc; all three counter selftests green (18/18/20, rc 0) at A4 bytes; C3 counter
absence at `2cc4b1ae` (rc 128) and full retroactive met run (rc 0, 18.3 s); freeze-commit file
list and timestamps; A1-A4 diffs and commit times; r84/r83 anchor bytes at the entering revision
with occurrence counts; `arms_ok` dead in the C1 met path; no `headers=<receipt>` literal in
count-c2.py; RECEIPTS tokens equal to the contract table.

**Not verified by me (cited as [L1]):** the C3 defeat control over the stub fixture repo and the
record/claim sweep lines in controls-r85.txt (fixtures under the L1's scratch, no longer
re-runnable from my seat without rebuilding the fixture; the sweep tools themselves are outside
this round's claims). The A1 hand-built receipt probe ("reads C2=met … rc 0") is quoted from the
amendment text only — no receipt exists at snapshot to reproduce it against real bytes.
