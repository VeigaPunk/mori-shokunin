# Receipt counterfeits — a declared mode is verified against the receipt's own header

source: S604 — The Update Framework Specification v1.0.37, §5.3.7 "Update the root role", fetched
2026-11-04, `https://theupdateframework.github.io/specification/v1.0.37/` (raw HTML lines
3502-3506; sha256 `f20fda0dda7128f3b9cc1f12f3d90301b0f6e163576ba285bfe485d1671e8def`)
source: the lane's own gate output `.ufo/waves/round-88/evidence/after-r88.txt` (committed at
`9c775ac2131da13c4c4cfdf2b14077184076f557`, measuring revision `d5e2eda4`)
verified-at: 2026-11-04
recheck: `python3 -I .ufo/waves/round-88/count-c2.py d5e2eda4` prints `C2=met real=met fx=4
clean=1 refused=2 absent=1 arms=23`; re-open S604 on release

## Rule

A receipt in the lane's population is admitted only when all three hold, each failing as a named
problem and an unmet run rather than a count:

1. **Declared mode is carried by the header.** A row the population declares `required` or `clone`
   must carry a replay mode the gate accepts. An absent `# replay:` line *and* `# replay: none`
   (which the header parser normalizes to "no replay" after requiring a `# no-replay:` reason)
   both read `missing-replay` on such a row. The reason is not that replay is expensive: the
   parser otherwise turns "declared replayable" and "carries no replay mode" into the same state,
   so a stripped header is counted `met` without any replay having run.
2. **A bound counter is named by the command.** On a row the population declares replayable
   (`required`/`clone`) — or that carries an explicit `# replay:` marker — every
   `# counter-sha256:` path must appear as a whitespace token of the `# cmd:` line
   (`cmd-binding`). A digest binds bytes; it does not bind the *body* to the command, and a
   command such as `printf '<body>'` reproduces any body while its digest stays genuine.
3. **A superseded target is inside the population.** A `# supersedes:` naming a receipt outside
   the graded population is `SUPERSEDE … absent=1` and fails the run, so a dangling supersede
   chain cannot retire a legacy row by naming something the gate never sees.

A refused row can carry more than one problem — for example a `clone` row with no replay line is
both `missing-replay` and `cmd-binding`, because the binding rule is keyed on the declared mode
while the replay execution is keyed on the parsed marker. The counters report the joined problem
list; neither problem suppresses the other.

## Why S604 grounds it

TUF's root-update procedure admits a new metadata record only when the record's version checks
against the trusted record (`N+1` exactly); on a mismatch the record is discarded, the cycle
aborts and the failure is reported. The transferable shape is verification-before-admission: the
record does not earn a pass for existing, and the refusal is a named outcome, not a suppressed
error.

## Limits (named)

- **Naming is not execution.** `binding_problems` splits the command text on whitespace; a path
  named only inside a shell comment satisfies it while bash never executes it. Measured by the
  round-88 C2 reviewer on fixture `a010047c`: a `clone` receipt whose `# cmd:` is
  `printf 'RECORD_SWEEP fabricated=1\n' # tools/mori-record-sweep.py` reproduces the r87 target
  line. Routed as R89-C2-comment-binding; this entry does not claim execution provenance.
- The gate verifies that a body is produced by its command. It does not verify that the command
  measures the thing the receipt claims to measure: `true` has a reproducible empty body.
- Legacy rows stay header-bound only (no replay); their `# limits:` cell carries the reason, and
  this gate does not re-derive their bodies. `binding_problems` is deliberately scoped to rows the
  population declares replayable (or that carry a replay marker), because a legacy receipt's
  `# limits:` is where its worktree-run exception is recorded and refusing those rows would trade
  one silence for another. Measured: `SCOPE_TABLE rows=7 applied=4 would_refuse=0` on the real
  population.
- Fixture revisions built inside `--shared` clones embed their commit time, so their hashes are
  not citable evidence; only the graded revision and the verdict line are.

## Siblings (cited, not absorbed)

The round-88 connector measured these relations; the sibling owns the stronger rule and mori only
cites it:

- tameshi `tools/count-recheck.py` — value binding (a printed figure equals a recount at the named
  revision). Mori's replay proves reproducibility, not that the figure is right.
- tameshi `tools/receipt-revision-gate.py` — a required-line refusal set (11 codes) and
  positive/verdict rev binding. Mori's rule 1 is one fixed instance of that shape.
- mado `tools/mado-tripwire.py` — unpinned inputs are refused, not downgraded to legacy; its
  provenance disclaimer ("provenance is the snapshot author's claim, not checked") is the sentence
  mori must cite, not restate.
- kotodama `tools/check-receipt-seq.py` — three-revision equality plus carrier parentage; a
  receipt-sequence claim belongs there, not in a new mori rule.
- chousa `corpus/knowledge/receipt-identity-r65.md` and `receipt-digest-provenance-r67.md` — the
  command/body-binding limit and the committed-bytes provenance rule mori implements.

`absorption: none`.
