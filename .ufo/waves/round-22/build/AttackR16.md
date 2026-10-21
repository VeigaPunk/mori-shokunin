# AttackR16 — R16: changed allowlist bytes returns 2

Seat: MoriR22.AttackR16 (reviewer, static review only — no tests/builds run).
Scope: frozen requirement R16 exclusively. Sources reviewed: contract.md (lines
11,13,15,19), frozen/fixture-builder.py, frozen/requirements.json,
oracle-reconcile.py, tools/mori-retention-reconcile.py (committed SUT at
8cb4afb), tools/mori-retention-gate.py (semantic baseline, lines 136-158,
226-307), real r21 receipt .ufo/waves/round-21/evidence/final/retention-floor.json
and corpus/evidence/retention-allowlist.json via read-only git plumbing.

## 1. R16 meaning, sharpened

Contract line 11: "Policy and allowlist bytes at input revision must equal bytes
at target revision; mismatches unevaluable, not silently current policy applied
historically." R16 (line 19): "changed allowlist bytes returns2."

The requirement is exactly: the byte sequence of the blob at the CLI `--allowlist`
path in the measured-revision tree MUST equal the byte sequence of the blob at
that same path in the resolved `--rev` (input-revision) tree, checked BEFORE any
recomputation consumes the allowlist. Violation → exit 2 with
finding_id `RETENTION_RECONCILIATION_SETUP` (contract line 15), sanitized error
token only, stderr empty. Exit 1 is RESERVED for a valid receipt that disagrees
with recomputation — a changed allowlist is an unevaluable input, not a
reconciliation mismatch.

### Canonical expected verdict (frozen fixture)

`fixture-builder.py` variant `allowlist-changed` (line 97): the second commit
writes `files[ALLOW]+b'\n'` — allowlist.json gains one trailing newline.
Receipt and policy blobs are unchanged; measured_revision (first commit) is an
ancestor of the input revision (second commit).

- Expected exit: **2**
- Expected finding_id: **RETENTION_RECONCILIATION_SETUP** on stdout JSON
- Expected stderr: empty (oracle `record()` asserts `cp.stderr==''`)
- SUT emits `"error":"allowlist_changed"`; oracle does not assert it (gap, §4)
- Counters/raw_hits: none required; contract requires sanitized error only

The `+newline` fixture is well-chosen: it separates a byte-compare (exit 2)
from both absent-compare (exit 0, receipt still agrees) and
parsed-JSON/row-set compare (exit 0, semantically equal rows). Any impl
returning 0 or 1 fails the oracle row outright.

### Real-repo axis (verified read-only)

Receipt `.ufo/waves/round-21/evidence/final/retention-floor.json` has
`measured_revision=9fb1f911…`, argv `--repo` absolute, `--policy` and
`--allowlist` absolute under it. `git rev-parse` shows the allowlist blob
`f8be55b1…` and policy blob `8bf285bd…` are IDENTICAL at `9fb1f911` and HEAD —
the real receipt passes the R16 gate and reaches recomputation (its
unallowlisted>0 result is R02's business, not R16's).

## 2. SUT behavior on the R16 path

`check()` (tools/mori-retention-reconcile.py:154-228):

1. Line 157: `raw={k:committed(repo,revision,p) …}` — reads receipt/policy/
   allowlist blobs at the INPUT revision via `ls-tree`+`cat-file` (never the
   worktree). `committed()` (81-86) also enforces: exactly one tree entry whose
   name equals the path byte-exactly, mode in {100644,100755}, kind blob —
   committed symlinks/gitlinks → `input_not_regular` (exit 2), satisfying
   contract line 15 "committed symlink input is rejected."
2. Line 161: `measured_revision` must fullmatch 40-or-64-hex AND
   `rev-parse --verify measured^{commit}` must return it unchanged — full
   commit, present, exactly the named object (a tag OID resolves to its
   commit ≠ itself → rejected).
3. Line 163: `merge-base --is-ancestor measured revision`; rc 1 →
   `git_read_failed` → 2 (R14 ordering before R16, immaterial to the arm).
4. **Lines 164-165 — the R16 arm:**
   `for key in ('policy','allowlist'): require(committed(repo,measured,paths[key])==raw[key], key+'_changed')`
   Raw-byte equality of the two blobs at the SAME CLI path. `+newline` fails
   this → `Invalid('allowlist_changed')` → exit 2 JSON. Correct.
5. Line 167: the allowlist is parsed only AFTER the byte gate, from `raw`
   bytes already proven equal at both revisions — the compared input IS the
   consumed input (no gap where equal bytes are checked on one file and a
   different file is consumed).

Assessment: the R16 gate in this SUT is byte-exact, blob-sourced (never
worktree), positioned before recomputation, and bound to the CLI `--allowlist`
path (receipt argv path binding at lines 177-182 then ties the CLI path to
the recorded scan). No defect found in the R16 arm itself.

## 3. Semantic ambiguities R16 leaves open (with verdicts)

a) **"bytes" — raw vs canonical.** Blob raw bytes vs parsed-JSON equality vs
   blob-OID equality. Byte/OID compares are equivalent and required;
   JSON-set equality is WRONG (misses `+newline`). The frozen fixture pins
   this. Verdict for reviewers: anything weaker than byte equality fails R16.

b) **Gate vs recompute ordering.** "Unevaluable" means the run must fail
   closed BEFORE the allowlist participates in recomputation. An impl that
   instead silently recomputes with the input-revision allowlist and emits
   MISMATCH/CLEAN has violated the clause even when the exit is also nonzero —
   arm (c) below discriminates this.

c) **Same-path scope.** Comparison is same-CLI-path-across-revisions, not
   whole-tree diff. An impl rejecting because ANY tracked file changed fails
   R01 legitimately (the receipt itself is a new file in the input commit) —
   no false-pass risk, noted for completeness.

d) **Missing vs changed.** Absent allowlist blob at either revision is
   `missing_input_blob` (setup), not `allowlist_changed`. Both exit 2; only
   error-reason-aware assertions can tell them apart.

e) **Rename/move.** If the allowlist moved paths between revisions, both
   comparisons fail closed at `missing_input_blob` — contract gives no rename
   semantics; fail-closed is compliant.

f) **Mode flip.** `100644↔100755` with identical bytes is NOT "changed bytes"
   — contract says bytes; SUT accepts both modes. Acceptable per literal
   contract; flagged as boundary surprise only.

## 4. Superficial-pass risks — what the frozen R16 arm does NOT pin

The oracle arm is `record('R16','allowlist-changed',2,'RETENTION_RECONCILIATION_SETUP')`
— asserts only {exit==2, finding_id, stderr==''}. These impl defects pass it:

- **R16-HIGH — wrong-reason exit 2.** An impl that reaches ANY setup failure
  on this input (allowlist parse crash, binding bug treated as setup, even a
  broken `committed()` that never compares anything) satisfies the oracle row.
  Actionable criterion: the oracle/selftest SHOULD additionally assert
  `v.get('error')=='allowlist_changed'` for R16 (and `'policy_changed'` for
  R15) — one-line predicate strengthening; zero new fixtures. Without it the
  byte-compare could be absent and the row still green via an unrelated fault.

- **R16-HIGH — gate-absent impls survive the fixture's weak mutation class.**
  `+newline` is byte-different but row-identical. An impl with NO byte gate
  exits 0 here and fails R16 — good. But the frozen suite never forces the
  gate to be the thing that fired. See fixture (c) below: a semantically
  DIFFERENT allowlist at input revision makes no-gate impls reach
  recomputation, where they can emit 0 (forged clean) or 1 (MISMATCH) — the
  "current allowlist applied historically" sin the contract names, with a
  plausible-looking verdict.

- **R16-MED — unbound file identity.** Byte-equality only proves something
  about the file the CLI points at. If the impl never binds receipt argv's
  `--allowlist` to the CLI `--allowlist`, an operator can point the check at a
  decoy file that is byte-equal across revisions while the receipt scanned a
  different file → 0/1 with R16 "satisfied." SUT binds (lines 177-182); an
  impl dropping that block must fail. Fixture (d) discriminates.

- **R16-MED — worktree read.** Reading the allowlist from the worktree for
  either endpoint violates "via Git blobs, not worktree" yet passes the frozen
  arm (committed file == worktree in fixture repos). Fixture (e) discriminates.

- **R16-STRUCTURAL — the receipt never binds the allowlist.** The gate's
  `scan` reads `--allowlist` from the WORKTREE at scan time (retention-gate.py
  line 317 `read_json(args.allowlist)`), and the receipt schema records
  `policy_sha256` but NO `allowlist_sha256`. So even a perfect R16 check
  proves only "the two committed trees agree at this path" — it cannot prove
  the committed blob is what the original scan consumed. The SUT's own
  `receipt_authenticity:'unattested'` field concedes this. This caps what R16
  can ever guarantee; a future receipt-schema `allowlist_sha256` is the real
  fix. Detection-only wave → recorded, not remediated.

## 5. Concrete counterexample fixtures (recommended additions)

All extend `FIX.make` variants; each is a single-variable mutation so the
expected verdict is unambiguous.

**(c) `allowlist-strengthened` — pins gate-before-recompute.**
Second commit replaces allowlist.json rows with the original rows PLUS one
valid row covering the retained `unallowed.txt` hit:
`{'path':'unallowed.txt','class':'R22','line_sha256':<sha of 'R22_SAMPLE retained-red'>,'reason':'forged','rule':'a'}`.
- Correct impl: exit 2 (`allowlist_changed`) — recomputation never runs.
- No-gate impl using input-revision allowlist: recomputed `metric=0`,
  `RETENTION_CLEAN` vs receipt's `metric=1`,exit_code=1 → exit 1
  MISMATCH (masking an unevaluable input as a receipt lie).
- No-gate impl + receipt also forged to claim metric=0: exit 0
  RETENTION_RECONCILED — a forged-clean reconciliation.
- Three-way discriminator (2 vs 1 vs 0); this is THE fixture that proves the
  R16 gate exists rather than being laundered through recomputation.

**(d) `allowlist-decoy` — pins file identity.**
Commit a second file `alt-allow.json` whose bytes differ between measured and
input revisions; keep `allowlist.json` byte-equal across revisions; pass
`--allowlist alt-allow.json` on the CLI while receipt argv still records
`.../allowlist.json` (absolute, matching `--repo` binding).
- Correct impl: exit 2 — via `receipt_path_binding` (SUT) or
  `allowlist_changed`; either proves the checked file is the bound one.
- Impl comparing blobs without argv binding: compares equal `allowlist.json`
  → proceeds → 0/1.
- Discriminates (4)'s unbound-identity risk.

**(e) `allowlist-dirty` — pins blob-not-worktree reads.**
After the second (valid-variant) commit, append a byte to the WORKTREE
`allowlist.json` without committing; run `--rev` = second commit.
- Correct impl: exit 0 RETENTION_RECONCILED (tree endpoints equal; worktree
  irrelevant).
- Worktree-reading impl: exit 2 — false setup rejection.
- Cheap guard for the contract's "via Git blobs, not worktree" clause on the
  allowlist axis (the analogous policy/receipt arms belong to R15/R17
  reviewers).

**(f) `allowlist-symlink-input` — pins regularity at the input endpoint.**
Input-revision tree carries `allowlist.json` as a symlink (120000) whose
TARGET is a file with content equal to the measured blob. Byte-compare-only
impls that follow the link see "equal bytes"; impls checking mode reject.
- Correct: exit 2 (`input_not_regular` in the SUT).
- Deeper discrimination than R21's generic symlink arm, which only puts the
  symlink at the RECEIPT path.

## 6. Verdict

- R16 arm exists in the committed SUT, is byte-exact, blob-sourced,
  same-path, pre-recomputation, and its `+newline` fixture genuinely
  discriminates byte-vs-semantic-vs-absent comparison. No defect in the arm.
- The oracle predicate is lax: any setup failure satisfies R16. Add
  `error=='allowlist_changed'` to the R16/R15 predicates — cheapest
  meaningful strengthening.
- The frozen suite does not force gate-before-recompute (fixture c), bound
  file identity (d), blob-vs-worktree (e), or mode regularity at the changed
  axis (f). Each is a one-commit mutation of the existing builder.
- Structural ceiling: the receipt schema binds `policy_sha256` but no
  `allowlist_sha256`, and the gate consumed a worktree file at scan time —
  R16 can only prove committed-tree agreement, never scan-time fidelity.
  Recorded as residual risk; outside this wave's remediation scope.

Tools installed/updated this seat: none (review only; pacman paused per lane
bounds).
