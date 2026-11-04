source: S605 (supersedes S604's wrong locator) — https://theupdateframework.github.io/specification/v1.0.37/ — §5.3 Update the root role, step 5.3.5; sentence at raw lines 3505-3506
verified-at: 2026-11-04; gate subject d5e2eda494877a85edaa4e287d6ad81843d9a8a1
recheck: `mkdir -p "${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r88/recheck" && python3 -I .ufo/waves/round-88/count-c2.py d5e2eda494877a85edaa4e287d6ad81843d9a8a1 --scratch "${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r88/recheck"`; re-open S605 after 365 days
evidence: `.ufo/waves/round-88/evidence/after-r88.txt`, committed at 9c775ac2131da13c4c4cfdf2b14077184076f557, measures d5e2eda494877a85edaa4e287d6ad81843d9a8a1
coverage-map: `corpus/README.md`, Round-88 knowledge addition: receipt counterfeits

# Receipt counterfeits — declared mode, token binding and target presence

## Observed rules

The round instrument `.ufo/waves/round-87/count-c2.py` adds three necessary conditions to its
existing ancestry, digest, summary-token and replay checks. A failed condition appends a named
problem, changes the counts, and prevents an expected-met row from being clean; these are not
sufficient conditions for admission.

1. A population row declared `required` or `clone` with parsed replay mode `None` is
   `missing-replay`. This includes a missing `# replay:` line and `# replay: none` with a valid
   waiver (the parser normalizes `none` to `None`). Required rows cannot waive their declaration.
2. On a row declared `required`/`clone`, or carrying a parsed replay marker, each binding path
   must be a whitespace token of the shell command text after stripping surrounding quotes and
   semicolons; otherwise `cmd-binding`. This checks naming, not executed argv.
3. A supersede target absent from the population's **present basenames** emits
   `SUPERSEDE … absent=1` and fails. A present target that is not a legacy row passes this check
   but retires nothing; target existence is not a proof of valid supersession lineage.

These conditions are exercised by the four fixtures in the r88 counter. The frozen stripped
fixture still names its bound counter, so it reports **only** `missing-replay`. A different
stripped row whose command also omits its binding can carry both problems.

Observed complete summary, reproduced by the reviewer with the explicit scratch argument:
`C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23 rev=d5e2eda49487`, rc 0.

## Source and the limit of the analogy

Stored source: `.ufo/waves/round-88/evidence/sources-r88/tuf-spec-v1.0.37.html`, 248698 bytes,
4997 lines; SHA-256 `f20fda0dda7128f3b9cc1f12f3d90301b0f6e163576ba285bfe485d1671e8def`.
The page's root-update heading is §5.3; its fifth ordered-list item contains this 23-word quote
(raw lines 3505-3506, once in tag-stripped text):

> If the version of the new root metadata file is not N+1, discard it, abort the update cycle,
> and report the rollback attack.

TUF specifies update metadata, not mori receipts, command provenance or mutation coverage. Only
the verification-before-admission shape transfers; the implementation claims come from the
committed gate and observed reports, not from TUF.

## Measured limits

- **Naming is not execution.** A path in a shell comment passes the token test although bash
  never uses it. See `.ufo/waves/round-88/w1/Mo88R02ReviewC2.md:7-16`; the recorded command is
  `printf 'RECORD_SWEEP fabricated=1\n' # tools/mori-record-sweep.py`.
- **Self-printing still passes if the path is also a token.** The critic's command is exactly
  `printf 'RECORD_SWEEP fabricated=1 tools/mori-record-sweep.py \n'`. The space before `\n` is
  load-bearing: without it the path token includes the escape and is refused. See
  `.ufo/waves/round-88/w1/Mo88C01Critic.md:115-136` and `Mo88S02Knowledge.md:207-221`.
- **Token spelling is not path identity.** Quoted paths pass but `./tools/mori-record-sweep.py`
  is refused despite a successful genuine replay; critic report `:97-113`.
- Empty binding lists satisfy the path rule vacuously. The population's `bindings=9 bound=9`
  target detects changes to its own fixed set, not arbitrary missing provenance.
- `POPULATION` is lane-authored input, not independently trusted history. Declaring a row legacy
  and stripping its marker bypasses both replay-related rules. A new receipt/count changes the
  fixed target and reads unmet; this is a round instrument, not a general receipt validator.
- A clean legacy successor can participate in supersession without replay; self-supersession is
  not refused by the helper. Limits-cell content is not verified beyond word/count checks.
- No current real row is falsely refused: `SCOPE_TABLE rows=7 applied=4 would_refuse=0`
  (`.ufo/waves/round-88/w1/Mo88Sc01Scope.md:17-23`). This says nothing about other spellings.
- Scratch fixture commit hashes in seat reports are run identifiers, not resolvable evidence.
  The reports contain the transformations and output needed to reconstruct them.

## Siblings — cited, not absorbed

The connector's comparison is `.ufo/waves/round-88/w1/Mo88K01Conn.md:48-64,118-142`:

- tameshi `tools/count-recheck.py:2-4` checks a printed value against a recount; reproducibility
  alone does not establish correctness. `tools/receipt-revision-gate.py:28-30,139-159` carries
  eleven revision/digest/required-line/ancestry codes, including content-drift refusal mori lacks.
- tameshi `tools/evidence-disposition.py:1524-1542` checks stronger supersession lineage.
- mado `tools/mado-tripwire.py:143-151` expressly leaves snapshot/transcript provenance unproved.
- kotodama `tools/check-receipt-seq.py:131-157,179-196` owns revision equality and carrier parentage.
- chousa `corpus/knowledge/receipt-identity-r65.md:16` and `receipt-digest-provenance-r67.md:15`
  distinguish identity, content binding and provenance.

`absorption: none`.

## Round-89 correction of record — newness, not the number of conditions

Supersedes the attribution at lines 11–14, not the three-condition decision table:
round 88 added **two** conditions (`missing-replay` and token `cmd-binding`) and extracted
`absent_supersede_targets` plus coverage for an **existing** absent-target refusal.
The entering r87 gate already tested `target not in known`; the r88 entering control
already refused the absent target. Evidence: `corpus/lessons/round-88-verifier-spotcheck.md`,
“Newness attribution defect found by this closure”; entering and after gate bytes at
`1bd5ec3fa260458f74eb32a2e5bb157209c5934d` and `d5e2eda494877a85edaa4e287d6ad81843d9a8a1`.
The original lines remain historical, not a standing claim of three new behaviors.

Round 89 replaces raw token spelling with a bounded script-position check; see
`execution-binding-r89.md` for the measured positives, counterfeits and limitations.
