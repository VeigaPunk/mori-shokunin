measured 2026-10-23T05:44:10Z
# MutQ98 — QUALITY 98 checklist mutation probe

Axes: calibration (false acceptance), required-shape coverage, pre-data chronology, exact restoration. These are probe concerns, not claimed axis moves.

## Result and interpretation

**The stated checks (a)-(c) reject missing no-decision coverage and late receipts, but accept substituting an already-scored absent-tool control for no-decision work.** That survivor is a checklist-coverage finding, not permission to alter 98 or the frozen claim. Results below use an explicit family interpretation of (a); the literal-`once` caveat and the stronger normative text are discussed below.

Sources were pinned with `git show b9fb029e:.ufo/waves/round-34/contract.md`, `git show b9fb029e:.ufo/waves/round-34/evidence/c1-controls.txt`, `git show fdf4371f:.ufo/waves/round-33/contract.md`, and `git show 8d56809a:corpus/QUALITY.md` in my isolated clone. Saved inputs are under `/fast/scratch/hyaku/mori-r34/a2-MutQ98/`; none came from the untrusted round-34 `w1/` drafts. The tested rule is `/fast/scratch/hyaku/mori-r34/a2-MutQ98/quality98.md:3-19`.

## Detector and baseline

The bounded detector is `/fast/scratch/hyaku/mori-r34/a2-MutQ98/check-q98.py:1-118`; complete actual command arguments, stdout, stderr and exits are preserved in `/fast/scratch/hyaku/mori-r34/a2-MutQ98/all-runs.json`. Each invocation used `timeout 20s prlimit --as=536870912 --cpu=15 --nofile=128 -- python3`, the same detector, the relevant contract file, the unchanged `r34-receipt.txt`, the sandbox clone, and the same two `q98-*` refs. Its nested Git commands also have time and memory limits.

- (a): seven semicolon-delimited shape families, allowing the alternatives joined by “or”; the three no-decision subcases are grouped into one covered family. This interpretation is explicit in the detector, not a change to the source criterion.
- (b): each unique table control names a recorded P-C1-A1 result; all baseline results are `C1=unmet`. The table's `C-echo` maps to receipt `C-echo-v1-literal`. Original table and receipt: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/pristine.md:69-81`, `/fast/scratch/hyaku/mori-r34/a2-MutQ98/r34-receipt.txt:2-37`. Amendment controls also have receipt lines at `r34-receipt.txt:29-49`.
- (c): actual Git ancestry, not commit dates. Baseline receipt is `b9fb029e05dcfb79757c46821dc4b61cb79d1a29`; first C1 tool-data commit is `ba525e1a0394154837eea5090e8bd27ed69c539c`; ancestry exits 0. Evidence: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/probe-summary.txt:3-10`.

All three scratch copies passed before mutation. The pristine fourth reference copy also passed. Thus the following kills are not baseline failures under this family interpretation.

| Input | (a) | (b) | (c) | Detector exit | Result |
|---|---|---|---|---:|---|
| Pristine round 34 | pass | pass | pass | 0 | accept |
| 1. Delete no-decision rows | fail | pass | pass | 1 | killed |
| 2. Substitute absent-tool controls | pass | pass | pass | 0 | survived checklist |
| 3. Receipt after data | pass | pass | fail | 1 | killed |
| Round 33, hand assessment | fail | pass | pass | not a script run | reject |

Actual round-34 outputs: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/probe-summary.txt:3-22`. Round-33 assessment: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/round33-hand.txt:1-15`.

## Mutant 1 — delete the three no-decision rows

Smallest assigned deletion: original contract lines 73-75, leaving the receipt and all other contract bytes alone. The preserved edit is `/fast/scratch/hyaku/mori-r34/a2-MutQ98/mutations.patch:1-12`.

Expected detector: reject at (a), since there is no no-decision mapping. Actual triple: pristine exit 0; mutated exit 1 (`a=0 b=1 c=1`, seven remaining named controls); restored exit 0. Evidence: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/probe-summary.txt:5-6,11-12,17-18`.

VERDICT: killed

## Mutant 2 — retain shape names, replace their work with absence

Only the three no-decision control cells changed: each now names `C-absent: base tip, no tool`, with its existing `unmet` expectation. The shape names remain verbatim. No receipt was forged or edited: the already-committed C-absent result is `tool=absent C1=unmet` under P-C1-A1. Evidence: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/mutations.patch:13-27`, `/fast/scratch/hyaku/mori-r34/a2-MutQ98/r34-receipt.txt:2-4`.

Expected semantic detector: reject, because tool absence does not test a delivered tool's lack of decision work. Actual stated-check triple: exits 0 / 0 / 0; mutated output is `a=1 b=1 c=1`, seven unique named controls, no missing receipts. Evidence: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/probe-summary.txt:7-8,13-14,19-20`.

VERDICT: survived

This verdict is **only for (a)-(c)**. Full 98 explicitly restricts generic absence to skip-work/content-free; applying that sentence by hand rejects this mutant. Therefore the result demonstrates an incomplete checklist, not acceptance by the complete normative requirement. Citation: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/quality98.md:6-12`.

## Mutant 3 — move receipt after actual tool data in sandbox history

The contract and receipt bytes did not change. In the clone only, I constructed a synthetic first-data commit from pre-receipt parent `24603186b555dddb88ebd607e415e27bdea747b4`, adding precisely the actual tool and its provenance file. Its child uses the original `ba525e1a` final tree, introducing the original receipt and A1 bytes after data. Actual command/output evidence: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/history-trace.json`.

- Synthetic first data: `14594507111bd0da7e854dd22bcbce193c50c127`.
- Synthetic later receipt: `9bd97babc925ac77bef6a3977276fb5c9f3f30d5`.
- `git cat-file -e <synthetic-first-data>:.ufo/waves/round-34/evidence/c1-controls.txt` exits 128: the receipt is genuinely absent there, not merely relabeled.
- Later receipt blob and original receipt blob both equal `3bc54a46efb70e254b651324cba75e6968731ffb`.

Expected detector: reject at (c). Actual triple: exits 0 / 1 / 0. Mutant output is `a=1 b=1 c=0`, `merge_base_exit=1`; restored ancestry exits 0. Evidence: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/probe-summary.txt:9-10,15-16,21-30`.

VERDICT: killed

## Round 33 historical negative

The actual contract at `fdf4371f` lists nine control categories but no no-decision control or reasoned inapplicability, and has no controls table: (a) rejects it. Exact list: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/round33.md:66-71`.

For (b), each of those nine named categories has a committed A1 receipt line. The hand mapping includes do-nothing, honest junk, all-false judge, no-reader judge, missing R-J, stale SHA, fabricated sources, re-registered source, and id/label shortcut. Each mapped line prints `C1=unmet`; mappings and original receipt line numbers are preserved at `/fast/scratch/hyaku/mori-r34/a2-MutQ98/round33-hand.txt:3-12`.

For (c), `git merge-base --is-ancestor fdf4371fb6d5f7c4e8b1f29f4735afaead5d45c9 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` exits 0 with empty stdout. The latter is the first entry-data commit in the recorded `git log --reverse -- corpus/knowledge/disk-write-rate-r33.md` output. Command receipt: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/round33-ancestry.json:1-19`. Overall: rejected by (a). This is a historical negative, not a fourth mutated/restored copy. Historical C1 counter scores were read, not rerun.

## Important baseline limitations

1. Literal “once” is not satisfied by the positive example: no-decision occupies three rows. The detector reports `a_literal_exactly_once=false` on every round-34 run. If “once” means exactly one physical row, pristine already fails, so all three strict-reading mutation comparisons are **inconclusive**, not kills. Evidence: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/pristine.md:73-75`, `/fast/scratch/hyaku/mori-r34/a2-MutQ98/probe-summary.txt:23`.
2. Full 98 also says a guard-tripped control discharges only skip-work/content-free, while the pristine table maps server echo to `unmet (guard)` and its matching receipt records a dirty guard. Thus I do not certify pristine as passing the entire normative 98. Evidence: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/quality98.md:6-8`, `/fast/scratch/hyaku/mori-r34/a2-MutQ98/pristine.md:78`, `/fast/scratch/hyaku/mori-r34/a2-MutQ98/r34-receipt.txt:26-28`.

The kills/survivor above are precisely scoped to the stated (a)-(c), family-normalized reading. No C2 admission judgment is made.

## Exact restoration and hashes

SHA-256 of the source contract and every restored contract:
`695c8412769da278932b44198649853c140d0eeda88e7591f71bc2950765cc11`.

| Scratch contract | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|---|
| drop-no-decision.md | source hash above | `2a6a50a5e74a06aee30dfbffbdd5b0fde2ed6bfc57b82e479728c0e95e061f08` | source hash above |
| generic-absence.md | source hash above | `08f3fe835523a4b71f432a270e525dded4a45354a1262afb75a82ea6d9d22101` | source hash above |
| late-receipt.md | source hash above | source hash above | source hash above |

Receipt SHA-256 remained `fb15da4786671b9a341399f658dbed2375f306b06f31eefe25a9e255928976ab` throughout. Both history refs were restored to their original `b9fb029e` / `ba525e1a` commits before the restored detector runs. These are measured hashes/ref values, not inferred restoration: `/fast/scratch/hyaku/mori-r34/a2-MutQ98/probe-summary.txt:5-22,25-28`.

Only this report was written in the lane; all mutations, synthetic commits and evidence files stayed in the assigned scratch directory. All launched commands were bounded foreground operations and returned; no load files, subagents, background jobs, judge runtime, omp invocation, tool install or tool update were used. Available tools reported `Python 3.14.8` and `git version 2.56.0` from bounded `python3 --version && git --version`. No frozen counter, contract, criterion or source was repaired. Probe complete.
