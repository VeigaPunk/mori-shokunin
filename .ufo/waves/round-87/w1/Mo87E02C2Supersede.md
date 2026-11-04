# Mo87E02C2Supersede — C2 supersede rule attacked with committed fixtures (round 87, w1)

seat: `Mo87E02C2Supersede` · lane: mori · round 87 · attempt 1 · date 2026-11-04
axes worked: **calibration** (primary), **operability** (fixture driver only)
claim attacked: **C2** — `.ufo/waves/round-87/contract.md` P-C2
scope: detection and report only. No lane commit, no counter edit, no fixture retained outside the
report. Scratch `/fast/scratch/hyaku/mori-r87/Mo87E02C2Supersede` deleted after this file was written.

**Result in one paragraph.** The frozen target line reproduces exactly (counts segment equal to the
counter's own `TARGET`, rc 0) at the claim revision `98f48dba` and at the lane tips this seat
measured. The supersede *rule* behind that line does **not** implement two properties the round's
wording states: (a) a receipt that is itself `legacy` — no `# replay:` line — can retire another
legacy receipt with a `# supersedes:` line (required fixture 4; the seat's stated expectation "it
must supersede nothing" fails); (b) the target line is reachable with **zero replays** and
fabricated bodies by deleting the two `# replay: clone` headers (fixture 5), because the replay mode
comes from the frozen population row and the replay body is skipped when the header is absent while
the `replay` tally still counts the receipt. Fixture 2 (stale bodies) and fixture 3 (absent target)
behave as specified. One ancillary fact: the counter bytes frozen at `142542e0` cannot print the
target at `98f48dba` after C1 landed; the A1-amended counter is load-bearing (measured, not judged).

## Authority read (bytes actually read, recorded because siblings land work concurrently)

| file | identity I read |
|---|---|
| `.ufo/waves/round-87/contract.md` | sha256 `bf208a448e096da4da5169e1b27db1b1ca97999119a2e43e49954c894042eb07`, blob `e0a2156a754e` |
| `.ufo/waves/round-87/count-c2.py` at HEAD | sha256 `264a43f04af1f9f939da7b3890f608a669a0c7fc2922656ee83f35adb236b14d`, blob `269842f7e764` |
| `.ufo/waves/round-87/count-c2.py` at `142542e0` and `98f48dba` | sha256 `e1dfd45a161b11a1ddfeae9bfe3d83f0f4f64c7d93dc0f85fc81d18e87ba7166`, blob `073276ee8a1d` |
| `.ufo/waves/round-87/evidence/controls-r87.txt` | sha256 `53d65a426632acdb5c88721a2e7847110780e8c668f8c8fbd4b1bdd5df75e616` |
| `.ufo/waves/round-87/evidence/probe-r87.txt` | sha256 `530e35e6058edfa5d690343e149e53392e3daa81ea3f13f3fe7224f26db3180d` |
| `.ufo/waves/round-87/evidence/record-sweep-r87.txt` | sha256 `213a7558e155ea4eaeec8472767fa8371b44948e40b59cf9ac8437954641f4ac`, blob `fc454e2c17e0` |
| `.ufo/waves/round-87/evidence/claim-sweep-r87.txt` | sha256 `429a5dca94d32e14bd3614524fd9c441d682ba3986bceda4a98a0a4354a296b8`, blob `96db2da39db2` |
| `corpus/lessons/round-86-verifier-spotcheck.md` (`## Routed defects`) | sha256 `820e5a49c69a5def9595e8c464e378b2f7b8ad0cce8dd210677bf2628fcfb203`, eight items read |
| `SCORECARD.md` `## Planned (round 87)` | items 1–3 read at the same worktree |
| `.ufo/waves/round-86/count-c2.py` (the C2 subject) | blob `71829635cdf0` at both `98f48dba` and my clean fixture rev |
| lane HEAD when I cloned | `b9e6f68d887c570909c7bacc8bac86579d850d1d` |
| lane HEAD at the last rerun | `728bc5f48363e668710579ed2b7822632383178a` (lane advanced mid-seat; sibling evidence files landed) |

A1 is real and load-bearing: `git diff 98f48dba HEAD -- .ufo/waves/round-87/count-c2.py` is only
`SUBJECT_ARMS 11 -> 13` and the two added labels `summary_required`, `binding_required`. `TARGET` and
`TARGET_LINE` are unchanged; the A1 commit `b9e6f68d` is a child of the C2 commit `98f48dba`
(`142542e0` freeze → `03b66a43` C1 → `98f48dba` C2 → `b9e6f68d` A1).

## Setup

- Four required fixtures, each in its own `git clone --shared` of `/home/vgpnk/Projects/shokunin/mori-shokunin`;
  `git -C <clone> rev-parse --show-toplevel` asserted equal to the clone path before the first commit;
  commits with `-c user.name=t -c user.email=t@t`.
- Every counter run is the frozen lane counter:
  `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-87/count-c2.py HEAD --repo <clone> --scratch <scratch>/scratch-<name>`.
  `--scratch` is added to the seat-spec form so nothing is written under `/tmp`; it changes no
  measurement. stdout and stderr were captured per run; **stderr was empty on every captured run**.
- Counter detector at HEAD: `C2_COUNTER_SELFTEST pass=17 fail=0`; the subject sub-gate reports
  `arms=(13, 0) labels=True` in every tail line.
- The clean fixture is an empty commit on the clone's `b9e6f68d` tip, so its population bytes are the
  lane's. Verified `git rev-parse` blob identity to `98f48dba` for all seven receipt paths and the
  subject: `SAME` on all eight.
- This seat's own run at the claim revision `98f48dba` (lane repo, frozen counter at HEAD) prints:
  `C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=98f48dba3267`, rc 0.
  A rerun at the moved lane tip `728bc5f4` prints the same counts with `rev=728bc5f48363`, rc 0.

## Required fixture 1 — clean: the two landed successors byte-exactly

fixture rev `6f603f1dc39731475d86fa05f14407d134bdf8c5` (empty commit on `b9e6f68d`; diff: none).
`record-sweep-r87.txt` blob `fc454e2c…`, `claim-sweep-r87.txt` blob `96db2da3…`, both identical to
`98f48dba`.

```text
RECEIPT after-r85.txt expect=met met problems=-
RECEIPT record-sweep-r85.txt expect=met met problems=-
RECEIPT claim-sweep-r85.txt expect=met met problems=-
REPLAY after-c1-r86.txt mode=required rc=0 exported=1
RECEIPT after-c1-r86.txt expect=met met problems=-
REPLAY replay-defeat-r86.txt mode=required rc=0 exported=1
RECEIPT replay-defeat-r86.txt expect=reject failed problems=replay-mismatch
REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT record-sweep-r87.txt expect=met met problems=-
REPLAY claim-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT claim-sweep-r87.txt expect=met met problems=-
C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=6f603f1dc397
rc=0
```

Checked mechanically: the segment after `C2=met ` and before ` rev=` equals the counter's `TARGET`
byte-for-byte (`True`), and equals the contract's target. Fixture 1 is the positive control: the
clean shape is met.

## Required fixture 2 — stale body: one byte in each successor body, headers untouched

fixture rev `2a46a757c2444fa21da773fa67e3ec35f9ba02b1`.

```diff
diff --git a/.ufo/waves/round-87/evidence/claim-sweep-r87.txt b/.ufo/waves/round-87/evidence/claim-sweep-r87.txt
index 96db2da3..646c4695 100644
--- a/.ufo/waves/round-87/evidence/claim-sweep-r87.txt
+++ b/.ufo/waves/round-87/evidence/claim-sweep-r87.txt
@@ -6,4 +6,4 @@
 # supersedes: claim-sweep-r85.txt
 # limits: named limit — the body is the command's stdout in a --shared clone checked out at # rev: and reads pointers=266 where the r85 worktree receipt read 274, so the older count is not reproducible from committed bytes and this receipt is the reproducible successor, not a re-derivation of it
 # ---
-CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=266
+CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=267
diff --git a/.ufo/waves/round-87/evidence/record-sweep-r87.txt b/.ufo/waves/round-87/evidence/record-sweep-r87.txt
index fc454e2c..2ceb2b13 100644
--- a/.ufo/waves/round-87/evidence/record-sweep-r87.txt
+++ b/.ufo/waves/round-87/evidence/record-sweep-r87.txt
@@ -6,4 +6,4 @@
 # supersedes: record-sweep-r85.txt
 # limits: named limit — the body is the command's stdout in a --shared clone checked out at # rev:, so it reproduces from committed bytes; it supersedes the r85 worktree receipt and does not re-derive that receipt's bytes
 # ---
-RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0
+RECORD_SWEEP pending=1 pinned=0 carriers=1 bindings=3 revisions=0
```

```text
RECEIPT after-r85.txt expect=met met problems=-
RECEIPT record-sweep-r85.txt expect=met met problems=-
RECEIPT claim-sweep-r85.txt expect=met met problems=-
REPLAY after-c1-r86.txt mode=required rc=0 exported=1
RECEIPT after-c1-r86.txt expect=met met problems=-
REPLAY replay-defeat-r86.txt mode=required rc=0 exported=1
RECEIPT replay-defeat-r86.txt expect=reject failed problems=replay-mismatch
REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT record-sweep-r87.txt expect=met failed problems=replay-mismatch
REPLAY claim-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT claim-sweep-r87.txt expect=met failed problems=replay-mismatch
C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=4 defeated=1 superseded=0 legacy=3 unexpected=2 detector=green rev=2a46a757c244
rc=1
```

As specified: both successors trip `replay-mismatch`, `superseded=0 legacy=3`, rc 1. The
`# supersedes:` header does not carry the day; the replay verdict does. This confirms the rule's
clean-successor conjunct on fresh bytes.

## Required fixture 3 — absent target: one successor names a receipt outside the population

fixture rev `2f46e48f67985ac054048d004143f3cd371da413`.

```diff
diff --git a/.ufo/waves/round-87/evidence/record-sweep-r87.txt b/.ufo/waves/round-87/evidence/record-sweep-r87.txt
index fc454e2c..4687002f 100644
--- a/.ufo/waves/round-87/evidence/record-sweep-r87.txt
+++ b/.ufo/waves/round-87/evidence/record-sweep-r87.txt
@@ -3,7 +3,7 @@
 # rev: 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee
 # counter-sha256: b8683be24e28ce4e79730b46615174d888af4c22ac7ee4fe16b97048516e8efa tools/mori-record-sweep.py
 # replay: clone
-# supersedes: record-sweep-r85.txt
+# supersedes: record-sweep-r84.txt
 # limits: named limit — the body is the command's stdout in a --shared clone checked out at # rev:, so it reproduces from committed bytes; it supersedes the r85 worktree receipt and does not re-derive that receipt's bytes
 # ---
 RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0
```

```text
RECEIPT after-r85.txt expect=met met problems=-
RECEIPT record-sweep-r85.txt expect=met met problems=-
RECEIPT claim-sweep-r85.txt expect=met met problems=-
REPLAY after-c1-r86.txt mode=required rc=0 exported=1
RECEIPT after-c1-r86.txt expect=met met problems=-
REPLAY replay-defeat-r86.txt mode=required rc=0 exported=1
RECEIPT replay-defeat-r86.txt expect=reject failed problems=replay-mismatch
REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT record-sweep-r87.txt expect=met met problems=-
REPLAY claim-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT claim-sweep-r87.txt expect=met met problems=-
SUPERSEDE record-sweep-r87.txt target=record-sweep-r84.txt absent=1
C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=1 legacy=2 unexpected=1 detector=green rev=2f46e48f6798
rc=1
```

As specified: `SUPERSEDE … absent=1`, `unexpected=1`, rc 1. The dangling name retires nothing; the
other successor still retires `claim-sweep-r85.txt` (`superseded=1`).

## Required item 4 — a `# supersedes:` line on a legacy receipt (no replay)

fixture rev `15d2385f5bed362a564ebbeaddada8343ca61e5c`. I added one header line to a receipt that
is `legacy` in the population and has no `# replay:` line.

```diff
diff --git a/.ufo/waves/round-85/evidence/record-sweep-r85.txt b/.ufo/waves/round-85/evidence/record-sweep-r85.txt
index ce09b873..8124c9c6 100644
--- a/.ufo/waves/round-85/evidence/record-sweep-r85.txt
+++ b/.ufo/waves/round-85/evidence/record-sweep-r85.txt
@@ -2,6 +2,7 @@
 # cmd: python3 -I tools/mori-record-sweep.py --root . --pins .ufo/waves/round-82/record-pins.json
 # rev: 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee
 # counter-sha256: b8683be24e28ce4e79730b46615174d888af4c22ac7ee4fe16b97048516e8efa tools/mori-record-sweep.py
+# supersedes: after-r85.txt
 # limits: named limit — this body is a worktree run while the binding pins the sweep tool bytes at the revision, not the worktree bytes
 # ---
 RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0
```

```text
RECEIPT after-r85.txt expect=met met problems=-
RECEIPT record-sweep-r85.txt expect=met met problems=-
RECEIPT claim-sweep-r85.txt expect=met met problems=-
REPLAY after-c1-r86.txt mode=required rc=0 exported=1
RECEIPT after-c1-r86.txt expect=met met problems=-
REPLAY replay-defeat-r86.txt mode=required rc=0 exported=1
RECEIPT replay-defeat-r86.txt expect=reject failed problems=replay-mismatch
REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT record-sweep-r87.txt expect=met met problems=-
REPLAY claim-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT claim-sweep-r87.txt expect=met met problems=-
C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=3 legacy=0 unexpected=0 detector=green rev=15d2385f5bed
rc=1
```

**`superseded=3 legacy=0`.** The legacy receipt's `# supersedes:` line retired `after-r85.txt`.
Compared with fixture 1 the only delta is that one added header line; the three legacy rows are
fixed, two were already retired by the r87 successors, so the third increment is `after-r85.txt`.
This contradicts the seat's stated expectation ("it must supersede nothing") and the round's own
wording that the rule "*requires the successor's replay*".

Attribution pair, isolating that line from the real successors (two fixtures, both branch cleanly
from the lane tip; their only edits are the two successor `# supersedes:` lines removed):

| fixture | rev | edit | tail |
|---|---|---|---|
| `nosuper` | `8e38681ff9b117a0e207b21f731df5e5269b3aac` | both successor `# supersedes:` lines deleted | `C2=unmet … replay=4 matched=6 defeated=1 superseded=0 legacy=3 unexpected=0 detector=green rev=8e38681ff9b1` rc 1 |
| `legacyonly` | `c936b39b0f3841b04480fc30f9e404993551085b` | same, plus `# supersedes: after-r85.txt` on the legacy r85 receipt | `C2=unmet … replay=4 matched=6 defeated=1 superseded=1 legacy=2 unexpected=0 detector=green rev=c936b39b0f38` rc 1 |

With every successor supersede link gone, the legacy receipt's line alone retires exactly one legacy
receipt (`0 -> 1`). The effect cannot be attributed to a replaying successor, because none carries a
supersede line in `legacyonly`.

Two controls on the same shape:

- `legacy-superseder-absent`, rev `1cf0a655d577c172af5753fe9e961cbfd21e4ef8`: the legacy receipt
  names `after-r84.txt` (absent from the population).
  `SUPERSEDE record-sweep-r85.txt target=after-r84.txt absent=1`, tail
  `… matched=6 defeated=1 superseded=2 legacy=1 unexpected=1 detector=green rev=1cf0a655d577`, rc 1.
  The line is parsed into the superseder set (it is checked against the known names) but retires
  nothing when the target is absent.
- `legacy-superseder-unclean`, rev `0d7a856518af550a9a652d13108d522cb37de04f`: the legacy receipt
  names a present target but its own binding byte is broken (`…16e8efa` -> `…16e8efb`).
  `RECEIPT record-sweep-r85.txt expect=met failed problems=sha:tools/mori-record-sweep.py`, tail
  `… matched=5 defeated=1 superseded=1 legacy=2 unexpected=1 detector=green rev=0d7a856518af`, rc 1.
  The clean gate does gate a legacy superseder — but only cleanliness, never replay.

### Mechanism (line numbers in `count-c2.py` at HEAD)

- `:242` `superseders.append((name, fields["supersedes"]))` — every present receipt with the header
  enters the superseder list, in the header pass, before any replay verdict.
- `:133-137` `supersede_verdict` returns `any(name in clean_names and target == legacy_name …)`.
  `clean_names` is the set of every problem-free receipt (`:282-283`), legacy included. There is no
  `# replay:` test and no population-role test on the superseder.
- `:139-151` `supersede_counts` then flips a clean legacy row to `superseded` on that verdict alone.

So the implemented rule is "a present, clean receipt names it", not P-C2's "a present, problem-free
**successor** names it". The r85 receipt is not a successor in the frozen population.

## Extra fixture 5 — the target line with no replay at all

fixture rev `85e8bd763281ea37622a3315103c8a5733712694`. Both `# replay: clone` lines deleted; both
bodies replaced with values the commands do not print (summary tokens kept, headers/digests/rev
untouched).

```diff
diff --git a/.ufo/waves/round-87/evidence/claim-sweep-r87.txt b/.ufo/waves/round-87/evidence/claim-sweep-r87.txt
index 96db2da3..5f352e80 100644
--- a/.ufo/waves/round-87/evidence/claim-sweep-r87.txt
+++ b/.ufo/waves/round-87/evidence/claim-sweep-r87.txt
@@ -2,8 +2,7 @@
 # cmd: python3 -I tools/mori-claim-sweep.py --root . --pins .ufo/waves/round-80/claim-pins.json
 # rev: 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee
 # counter-sha256: 4ac6b52615a427d1f7d8993ab636a5830bcde744c4a51f22d9157833d940ba1d tools/mori-claim-sweep.py
-# replay: clone
 # supersedes: claim-sweep-r85.txt
 # limits: named limit — the body is the command's stdout in a --shared clone checked out at # rev: and reads pointers=266 where the r85 worktree receipt read 274, so the older count is not reproducible from committed bytes and this receipt is the reproducible successor, not a re-derivation of it
 # ---
-CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=266
+CLAIM_SWEEP mismatches=7 unresolved=7 tallies=7 stale=7 carriers=7 pointers=777
diff --git a/.ufo/waves/round-87/evidence/record-sweep-r87.txt b/.ufo/waves/round-87/evidence/record-sweep-r87.txt
index fc454e2c..1acdb88c 100644
--- a/.ufo/waves/round-87/evidence/record-sweep-r87.txt
+++ b/.ufo/waves/round-87/evidence/record-sweep-r87.txt
@@ -2,8 +2,7 @@
 # cmd: python3 -I tools/mori-record-sweep.py --root . --pins .ufo/waves/round-82/record-pins.json
 # rev: 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee
 # counter-sha256: b8683be24e28ce4e79730b46615174d888af4c22ac7ee4fe16b97048516e8efa tools/mori-record-sweep.py
-# replay: clone
 # supersedes: record-sweep-r85.txt
 # limits: named limit — the body is the command's stdout in a --shared clone checked out at # rev:, so it reproduces from committed bytes; it supersedes the r85 worktree receipt and does not re-derive that receipt's bytes
 # ---
-RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0
+RECORD_SWEEP pending=7 pinned=7 carriers=7 bindings=7 revisions=7
```

```text
RECEIPT after-r85.txt expect=met met problems=-
RECEIPT record-sweep-r85.txt expect=met met problems=-
RECEIPT claim-sweep-r85.txt expect=met met problems=-
REPLAY after-c1-r86.txt mode=required rc=0 exported=1
RECEIPT after-c1-r86.txt expect=met met problems=-
REPLAY replay-defeat-r86.txt mode=required rc=0 exported=1
RECEIPT replay-defeat-r86.txt expect=reject failed problems=replay-mismatch
RECEIPT record-sweep-r87.txt expect=met met problems=-
RECEIPT claim-sweep-r87.txt expect=met met problems=-
C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=85e8bd763281
rc=0
```

**The frozen target line, rc 0, with no `REPLAY` lines for either successor and `problems=-` on
fabricated bodies.** Mechanism:

- `:243-244` `if replay_mode != "legacy" or fields["replay"] is not None: counts["replay"] += 1`
  — a population row declared `clone` increments the `replay` tally even when the receipt carries no
  `# replay:` line.
- `:269` `if mode in ("required", "clone") and fields["replay"] is not None:` — the replay (and the
  body comparison inside it) runs only when the *header* is present. Missing header ⇒ no `# cmd:`
  execution, no `replay-mismatch`, `problems` stays empty.
- `:295` `supersede_counts` therefore sees both r87 receipts as clean and both supersede.

Consequence for calibration: `replay=4`, `matched=6` and the whole frozen target string do not
discriminate this shape. The printed target is compatible with zero replays and arbitrary bodies.
The counter never validates that a population row declared `# replay: clone` is actually present in
the receipt; it inherits the mode from the population and silently degrades to a header-only grade.
Whether this is scored as a C2 miss or as a defect of the target's discriminating power is the L1's
call; this seat records the behaviour and the exact bytes.

## Ancillary measurement — the freeze bytes cannot print the target after C1

Counter extracted from `142542e0` (sha256 `e1dfd45a…`, blob `073276ee8a1d`), run against the same
clean population bytes:

- at the clean fixture rev (`6f603f1dc397`):
  `C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 subject=selftest arms=(13, 0) labels=True rev=6f603f1dc397`, rc 1, its own `C2_COUNTER_SELFTEST pass=13 fail=0`.
- at the claim revision `98f48dba`:
  `C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 subject=selftest arms=(13, 0) labels=True rev=98f48dba3267`, rc 1.

All other counts already equal the target; only the subject sub-gate is red. The subject blob at
`98f48dba` is `71829635cdf0`, identical to the one my clean fixture rev and HEAD carry, and C1
landed in `98f48dba`'s parent `03b66a43`. Therefore the target at `98f48dba` is reachable only with
the A1-amended counter (`264a43f0…`), which is what this seat ran for every fixture. The contract
discloses A1 and the target string is unchanged (verified by diff); this is an ordering fact, not a
fresh judgement.

## The rule as measured

| shape | result |
|---|---|
| two successors, `# replay: clone`, bodies reproduce | met; exact target; rc 0 (fixture 1) |
| same, one body byte changed per successor | both `replay-mismatch`; `superseded=0 legacy=3`; rc 1 (fixture 2) |
| successor names a name outside the population | `SUPERSEDE … absent=1`; `unexpected=1`; rc 1 (fixture 3) |
| successor names it but is unclean | supersedes nothing (fixture 2 and `legacy-superseder-unclean`) |
| **legacy receipt (no replay) carries `# supersedes: <present legacy>`** | **retires it** (`superseded+1`, `legacy-1`); rc 0-eligible (fixture 4, `legacyonly`) |
| legacy receipt carries `# supersedes:` naming an absent receipt | `absent=1`, `unexpected=1`; retires nothing (4b) |
| successors lose `# replay:` headers, bodies fabricated | **exact target, rc 0, no replay run** (fixture 5) |

## What this seat did not run / limits

- Did not run `.ufo/waves/round-87/count-c1.py`; no C1 measurement or audit here.
- Did not independently re-run the three r86 counters' `--selftest`; the subject gate result
  `arms=(13, 0) labels=True` is what the frozen counter reported in its own tail line.
- Did not test a target-legacy row that is itself unclean (the symmetric gate). Not needed for the
  seat's four items.
- Fixtures lived in deleted scratch; the rebuild recipe is the diff plus the command in each
  section, applied to a `--shared` clone at `b9e6f68d`.
- No tool install or upgrade (nothing was needed); no lane, OS, service, credential or orchestration
  state changed. The lane worktree had sibling changes before and during this seat; I touched only
  this report file.
- All runs used `--scratch` under `/fast/scratch/hyaku/mori-r87/Mo87E02C2Supersede`; never `/tmp`.
- One interactive print during the seat showed a stray `775` on the counter's stderr pipe. Two
  immediate repeat runs at the same revision returned empty stderr (`repr(stderr) == ''`), and the
  captured per-fixture stderr files are all zero bytes, so it is recorded here as an unexplained
  transient, not evidence.

## Handoff

- Files written: this report only.
- Behaviour measured: the frozen target reproduces exactly at `98f48dba` under the A1 counter
  (fixture 1 and this seat's own claim-revision run); the supersede rule retires on "present and
  clean", not "replaying successor" (fixture 4 + pair), and the target is reachable with no replay
  at all (fixture 5).
- Risks: if C2 is scored as a miss, the two findings above are the ones that bound what the target
  line certifies; if it is scored as met, the same two findings are r88 routed items (a superseder
  role check at `:242`/`:133`, and a population-row replay-declaration check at `:243`/`:269`).
  This seat does not decide that.
