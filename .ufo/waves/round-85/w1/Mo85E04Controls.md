# Mo85E04Controls — defeat controls + standing battery (round 85, wave w1, attempt 1)

Seat: Mo85E04Controls (executor, controls/battery; leaf — no subagents). Date: 2026-11-04.
Lane HEAD at close: `91f657f696a701cae8a03a32e0b6d0407603f0b4` (A1–A4 landed); freeze revision
`ab2608655ea52ba6d151b3a31d69a3b18cd2b41e`. Scope kept: lane writes are exactly
`.ufo/waves/round-85/evidence/battery-r85.txt`, `.ufo/waves/round-85/evidence/controls-r85-defeated.txt`
and this report. Scratch `/fast/scratch/hyaku/mori-r85/Mo85E04Controls` deleted before yield.

## 0. Deliverables and one-line results

1. `controls-r85-defeated.txt` — all three frozen contract defeats executed for real, each with
   command, full output and `rc=`:
   - C1 at the freeze revision: `C1=unmet mutants=2 killed=0 survivors=2 total=2 arms=15
     harness=stub missing=…` rc 1; de-armed fixture copy: identical unmet, rc 1; armed snapshot:
     `C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met` rc 0.
   - C2 corrupted `# counter-sha256:` (one hex digit): `C2=unmet receipts=3 bindings=5 bound=4
     … mismatch=1` rc 1; headerless receipt: `C2=unmet … mismatch=7` rc 1. Both preceded by a
     correct-sha fixture sanity reading `C2=met … mismatch=0` rc 0 on the same grammar.
   - C3 fresh census-stub fixture: `C3=unmet observed=3 aa=unstable own_tokens=0 rcs=1,1,1` rc 1.
2. `battery-r85.txt` — the r84 standing battery command list verbatim (61 commands), from the lane
   root, with the D84-5 header `# battery run at rev=4ffd5a2dc91d966073c4e5f36f54a4cdbaceb24a
   date=2026-11-04T08:15:32-03:00`: `BATTERY pass=57 setup=4 fail=0`, `battery rc=0`.

## 1. Battery (D84-5)

- Command list: the 61 `$ timeout --kill-after=5s 120s …` lines of `battery-r84.txt`, byte-identical
  and in order (58 tool selftests incl. the three bash tools, then round-80 counters at
  `da7631f4…`, round-81 counter selftests). Run from the lane root; `TMPDIR` under this seat's
  scratch (same class of environment as the r84 run — the four TMPDIR-beneath-lane selftests read
  SETUP rc=2 exactly as in r84).
- Result: 57 rc=0, 4 SETUP, 0 FAIL. Per-command rc lines are the receipt's verdict lines
  (57 `… rc=0` + 4 `SETUP …` = 61); command outputs are the run's captured bytes.
- **L1 measurement exchange (MoriR85):** my first classification counted
  `tools/mori-freeze-order.py --selftest` (rc 1, `SELFTEST freeze-order FAIL 0/11`) as FAIL
  (`pass=57 setup=3 fail=1`). MoriR85 ruled it the r84 SETUP class (battery-r84.txt:160, "TMPDIR
  must be beneath checkout; tools/mori-freeze-order.py:509-514"). Amended in place: verdict line
  now `SETUP … rc=1 TMPDIR must be beneath checkout; tools/mori-freeze-order.py:509-514`, summary
  `BATTERY pass=57 setup=4 fail=0`, `battery rc=0`, header note documents the amendment. I agree
  with the classification — my run captured only the stdout FAIL line, the cause is the same
  TMPDIR precondition as the other three SETUPs, and it is r84 behavior reproduced, not a
  regression. My run's own captured output for that command (the single `SELFTEST freeze-order
  FAIL 0/11` line) is untouched in the receipt.
- Provenance: run at worktree HEAD `4ffd5a2d` (A2, 08:15:22). `git diff --stat 4ffd5a2d..91f657f6`
  touches only `.ufo/waves/round-85/` files (contract, count-c3.py, controls receipt) and
  `git diff --stat ab26086..HEAD -- tools` is empty, so every byte the battery exercised is
  identical to current HEAD's.

## 2. C1 (operability) — defeat and armed readings

- Freeze revision (arms not landed there): unmet, `harness=stub`, arms=15, rc 1 — command and full
  output in the receipt.
- De-armed fixture: a shared clone whose `.ufo/waves/round-84/count-c1.py` blob is byte-identical
  to the freeze-revision blob (`5b89a23d`, both arm labels grep 0) grades unmet arms=15 rc 1.
  At the first control pass (08:15:36) this was the *only* possible reading — the arms were not
  landed in the worktree (status empty, label counts 0), which the seat item anticipated.
- Armed reading: the sibling landed the arms in the worktree during the seat (uncommitted; label
  counts observed 0 → 1 → 2 while the edit was in flight). I snapshotted the worktree bytes
  (sha256 `549553123df7…`, both labels exactly once) into a fixture at 08:26:39 and graded them:
  **`C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met` rc 0** — the frozen target
  line, on fixture bytes. The arms-absent / arms-present pair on the same counter shows the
  counter discriminates on the arms, not on something else.
- Not mine to measure: the lane-integration after-value at the graded revision belongs to the C1
  seat's after receipt; my snapshot may differ from the finally landed bytes (the copy was still
  being edited), so the integration run is the binding one.

## 3. C2 (calibration) — defeat receipts

- Fixture grammar sanity: receipts with correct freeze-rev shas read `C2=met … mismatch=0` rc 0 in
  both fixtures — the defeats below are caused solely by the injected corruption.
- Corrupted sha (one hex digit, `da5fb27b…` → `ea5fb27b…`, still 64-hex): `C2=unmet receipts=3
  bindings=5 bound=4 revs=3 limits=3 cmd=3 summary=3 mismatch=1` rc 1, with
  `PROBLEM after-r85.txt sha:.ufo/waves/round-85/count-c1.py` — exactly the frozen defeat shape.
- Headerless receipt: `C2=unmet receipts=3 bindings=4 bound=4 revs=2 limits=2 cmd=2 summary=2
  mismatch=7` rc 1. Composition: 5 parse problems (missing separator/cmd/rev/limits/binding) +
  rev=None + summary missing (no `# ---` ⇒ the header block swallows the file and the body is
  empty, so the body token never counts — A2 parser semantics; the `rev-unresolved` PROBLEM line
  binds zero bindings and adds 0). Satisfies the frozen "mismatch>=1".
- Observation (no action by this seat): the contract's illustrative headerless line
  `C2=unmet headers=<receipt>` differs in shape from the counter's actual output (PROBLEM lines +
  `RECEIPT … headers=0`); verdict and rc agree.

## 4. C3 (depth) — census-stub defeat, re-derived

Fresh fixture (`git init`, toplevel asserted, five files: 3-line census stub without a
`MORI_DRIFT:` line + byte-exact freeze-rev exports of baseline, classification, snapshot, r83
subject), committed with the fixture identity: counter prints `C3=unmet observed=3 aa=unstable
own_tokens=0 rcs=1,1,1` rc 1 with this seat's own fixture rev (`d74ed43e4975`). The measured
sibling line in `evidence/controls-r85.txt` was read as corroboration only and is never cited as
my run.

## 5. Peers and corrections

- MoriR85: battery reclassification (§1) — applied as ruled and acknowledged.
- ExecEvidence (misroute): their `check-sources-recheck.py` finding names a kotodama-lane draft
  outside my scope; answered with a redirect, claimed nothing.

## 6. Verified / not verified

**Verified (every output above is this seat's own execution):** the six counter runs + armed
snapshot run in `controls-r85-defeated.txt`; the 61-command battery run and its summary; the
blob-identity and label-grep assertions; the freeze-rev sha256 table (git show | sha256sum).
**Not verified by this seat:** the C1/C2/C3 after-values at the integration revision (other
seats'/L1's items); the stability of the armed worktree copy after 08:26:39; the content of
sibling receipts (`after-r85.txt` etc. — absent from my fixtures by construction).
**Honesty notes:** a first control pass ran at 08:15:36 on post-A2 bytes (HEAD `4ffd5a2d`) with
byte-identical outputs modulo fixture commit ids; the receipt carries the settled post-A4 runs so
counter provenance is exact. My first battery summary echo on stdout was malformed
(`fail=61-total=61`); the receipt file itself was always correctly formatted and is now amended.

## 7. Tooling

No tool installed or upgraded (pacman guard respected trivially): used preexisting
python3/git/bash/coreutils/timeout only. Scratch was `/fast/scratch/hyaku/mori-r85/Mo85E04Controls`
(HYAKU_SCRATCH default root), removed before yield; fixture paths cited in the receipts stop
resolving after that deletion by design — each receipt section carries its full rebuild recipe
(D84-5 resolution note).

## 8. Risks / notes for the L1

1. The battery SETUP-classification rule (rc 1 *or* rc 2 with a TMPDIR-precondition cause reads
   SETUP) is now codified only in the receipt header; the round lesson may want it stated once.
2. The C2 contract-vs-counter headerless line-shape divergence (§3) is an observation for the
   contract owner; the frozen predicate (unmet, rc 1) holds either way.
3. None of the above blocks the wave; both receipts are untracked and ready for the L1's commit.
