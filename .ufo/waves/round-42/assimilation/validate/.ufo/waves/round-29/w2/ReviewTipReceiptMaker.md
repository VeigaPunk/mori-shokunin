# Review: `make-tip-receipts.sh` (e1c6bbe7)

## Findings

- **Medium — C1/C2 are not guaranteed to read through the sandbox clone.** The maker clears Git directory overrides, clones the lane, checks out the supplied parent, and invokes each counter from that clone (`.ufo/waves/round-29/make-tip-receipts.sh:30-48,65-77`). But C1 defaults `MORI_C1_LANE_REPO` to the original lane and reads the supplied revision through that path (`.ufo/waves/round-29/count-c1.sh:4,79-82`); C2 likewise defaults `LANE` to the original lane and its `git()` helper reads there (`.ufo/waves/round-29/count-c2.sh:8,22-27,163-166`). The maker does not set either variable to `$clone`. Thus the counters are given the requested commit, but the maker does not guarantee their Git reads come from the clone. No wrong result was demonstrated: both counters use the passed revision, and C2's receipt reports `rev=8809a3fe1eaa87a0afa177a15263d174378e7462` (scratch receipt). This is an isolation gap for the requested sandbox check, not by itself a failure of QUALITY 87's parent-header condition. Retention does explicitly scan `--repo "$clone" --rev "$parent"` (`make-tip-receipts.sh:98-100`).

## Checks and evidence

- **Header: pass, exact line content.** QUALITY 87 specifies the first-parent hash and `round-<N>` substitutions in the literal at `corpus/QUALITY.md:448-452`. The maker resolves and validates a full 40-hex parent (`make-tip-receipts.sh:37-43`), assigns the corresponding round-29 header (`:50`), and writes it as the first line (`:52-62`). For each of the three scratch receipts from the requested run, I compared its first line to the fully substituted QUALITY 87 line; all returned `header_match=yes`. The exact first line for all three was:

  `# measured at parent 8809a3fe1eaa87a0afa177a15263d174378e7462; the landed tip adds only receipt files under .ufo/waves/round-29/evidence/`

- **Run at requested parent:** ran the committed script copy in `/fast/scratch/hyaku/mori-r29/w2/ReviewTipReceiptMaker/` with parent `8809a3fe1eaa87a0afa177a15263d174378e7462`, output directory `.../out`. The committed script bytes and scratch copy both hash to `4bf31a0f32ad04662c06ac3c3f5fce00ec930e46682c80c6da9721fb819dd6eb` (`git show e1c6bbe7d1cd50e7067efe3c125a5848d3d49ccd:.ufo/waves/round-29/make-tip-receipts.sh | sha256sum`; `sha256sum` of scratch copy).

  | Receipt | First line | Exit line |
  |---|---|---|
  | `tip-c1.txt` | `# measured at parent 8809a3fe1eaa87a0afa177a15263d174378e7462; the landed tip adds only receipt files under .ufo/waves/round-29/evidence/` | `exit: 0` |
  | `tip-c2.txt` | same exact line above | `exit: 1` |
  | `tip-retention.txt` | same exact line above | `exit: 1` |

  Terminal output: `wrote .../tip-c1.txt (exit 0)`, `wrote .../tip-c2.txt (exit 1)`, `wrote .../tip-retention.txt (exit 1)`, `maker_exit=0`. The receipts preserve measured-command outcomes; the maker's comment says its own exit 0 means all three receipts were written (`make-tip-receipts.sh:107-108`).

- **Absent counters: pass at receipt level; no fake pass.** At parent `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`, read-only `git cat-file -e` checks reported both round-29 counter paths absent. Running the same scratch copy at that parent produced `tip-c1.txt` and `tip-c2.txt` with `exit: 2`; each receipt also starts with the parent header and records the captured `counter absent at <parent>` message. This follows the explicit absence branch setting `status=2` before `write_receipt` (`make-tip-receipts.sh:65-83`). The maker itself still exits 0 because it successfully wrote the receipts; its status is not a counter pass. QUALITY 84 requires the receipt to carry an exit line and output (`.ufo/waves/round-28/check-tip-receipts.sh:14-22`), and these absence receipts do.

## Residual risk and verification gaps

- The requested execution proves the header and receipt statuses for scratch output, not that a later landing batch has this exact first parent, adds only evidence receipts, or is cited by an earlier-batch report; those are commit/report checks in QUALITY 87 (`corpus/QUALITY.md:448-459`).
- LSP was unavailable: `read xd://lsp` returned `No such tool: xd://lsp` (mounted devices listed only `ast_edit, debug`). I used direct source reads for cited code; text search was only a literal locator. No tools were installed or updated; required `~/.omp/agent/RULES.md` was read.
