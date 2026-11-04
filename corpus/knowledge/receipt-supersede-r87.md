# Receipt supersede: a legacy receipt retires only when a successor reproduces its command

source: S603 (`corpus/SOURCES.md`), opened 2026-11-04 from `https://git-scm.com/docs/git-clone`
(sha256 `d31b6c9f293a5dfc52c551b86be211b2d6dad3d2b4cf0d9c696d5fbed713554a`, 107882 bytes, 3391
lines, two fetches byte-identical); S600 (reproducible-builds definition, re-opened this round,
sha256 `a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb`) and S602 (in-toto
execution-record byproducts) are the adjacent rules already held.
verified-at: 2026-11-04
recheck: 365d
coverage-map: corpus/README.md (`## Coverage map`, the `receipt-supersede-r87.md` row)

## What it holds

The r86 receipt grammar graded a body by its headers (command, revision, digest binding, summary
token) and left three receipts `legacy`: their bodies were recorded but never re-derived. This
entry carries the rule that retires that limit, and the two measured facts behind it.

1. **A legacy receipt is superseded, never rewritten.** A new receipt with `# replay: clone` and
   `# supersedes: <legacy name>` is recorded at the same revision and its body must equal the
   stdout of its `# cmd:` replayed in a repository checked out at that revision. The legacy bytes
   stay byte-unchanged; the supersede link is the only new claim, and it is earned by the replay.
2. **The supersede rule reads the replay, not the header.** A successor that carries correct
   headers and digests but a body its command does not produce supersedes nothing. Measured: the
   header-only control (`.ufo/waves/round-87/evidence/controls-r87.txt` §C2) reads
   `matched=4 ... superseded=0 legacy=3 unexpected=2`, rc 1. The first implementation of the rule
   superseded on presence alone and the control caught it before data; the fix
   (`supersede_counts`, which takes only problem-free successors) is armed twice.
3. **The replay environment is part of the command.** A sparse export of the revision is not a
   repository: `RECORD_SWEEP` in a bare tree export reads
   `REVISION_MISMATCH SCORECARD.md:4051 rev-unresolvable` ×3,
   `RECORD_SWEEP ... revisions=3`, rc 1, while the same command in a `git clone --shared` checked
   out at the same revision reads `RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3
   revisions=0`, rc 0. `git-clone(1)` states the difference: a clone is a repository (S603 quote
   at raw lines 2627-2628), and `--shared` shares the object store through alternates
   (raw lines 2696-2699).
4. **A worktree reading is not a revision reading.** `CLAIM_SWEEP` on the live worktree printed
   `pointers=274`; in a clone at the same revision it prints `pointers=266`. The successor records
   the clone value; the r85 worktree receipt is superseded, not corrected in place.

## Decision table

| Observation | Reading |
|---|---|
| a legacy receipt has no `# replay:` line | header-bound only: grade it `legacy` unless a present, problem-free successor names it |
| a successor names the legacy receipt and its body equals the replay's stdout | `superseded`; the successor's replay is the evidence, the legacy bytes stay unchanged |
| a successor names it but its body differs from the replay | the legacy receipt stays `legacy` and the successor is `unexpected`; a failed successor supersedes nothing |
| a successor targets a name absent from the population | `SUPERSEDE ... absent=1`, `unexpected` — the link is dangling evidence, not a supersede |
| the command needs history (`git show`, `merge-base`) | replay in `clone` mode; a sparse export cannot resolve revisions and must not be read as the command's result |
| a body is a live observation (census, PSI, journal) | no successor is possible: the receipt stays `legacy` with that reason stated in the round lesson's Gate |
| same command, worktree versus clone | two different readings; only the clone reading is reproducible from committed bytes |

## Limits

- A replay proves the command's *output* at that revision in that environment; it proves neither
  authorship, nor that the command's own dependencies are what the receipt names, nor the absence
  of a side effect the command leaves outside stdout.
- The clone replay is only as complete as the repository's object store; a shallow or filtered
  clone would break `merge-base` and is not what the counter builds (`git clone --shared`, full
  history, then `checkout <rev>`).
- Superseding does not delete history: the legacy receipt remains readable, and its bytes are what
  a reader comparing old and new counts sees. The successor's `# limits:` line must name any
  numeric difference (measured: `pointers=274` → `266`).
- The rule is a receipt-level rule for this lane's own evidence; it is not a fleet lifecycle,
  result-acceptance or authorship verdict.
