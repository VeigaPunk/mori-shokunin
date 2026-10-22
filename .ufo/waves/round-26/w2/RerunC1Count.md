# Wave-2 seat report — RerunC1Count (attack C1's counted value)

Seat: MoriR26.RerunC1Count, 2026-10-22. Lane tip under attack: `16935e24c93fa7e7567413d7ec091339a5df1474`.
All git access read-only (`rev-parse`, `show`, `log`, `diff`, `merge-base --is-ancestor`, `rev-list`, `cat-file` via `show`).
No tools installed (bash, git, python3 already present); scratch: `/fast/scratch/hyaku/mori-r26/RerunC1Count/` (`lane-root.txt`, `tmp.txt`).
No LSP device available for bash scripts; all checks are command-output and git-object checks, not text-grep proof.

## Method

Ran `bash .ufo/waves/round-26/count-c1.sh <rev>` at `248408f5b6610a85bcbdebe7ac0b4fa7ed51422a`,
`327fbcca022ce363205d6b460a02f7836cf76990`, `16935e24c93fa7e7567413d7ec091339a5df1474`, `deadbeef`,
once with cwd = lane root and once with cwd = `/tmp`, capturing exit codes. Then recomputed all four
numbers with independent Python (regex whitespace collapse + `*` strip over `git show` bytes; distinct
id-set over every `^source:` line, not just the first; line-count vs occurrence-count for the r12 name)
to falsify the script's normalization or its single-source-line shortcut. Verified the working-tree
script and receipt are byte-identical to the tip commit (`git show 16935e24:... | diff - <file>`: identical;
`git diff 16935e24 -- <script> <receipt>`: empty).

Working-tree integrity: the script I executed is the tip's script (commit `99338de`, 2026-10-22 10:21:07,
"contract amendment A1 (committed counters)"), not a local variant.

## Results

Every run below produced exactly four lines; exit codes as shown.

| rev | cwd | stale_present | r26_entry | r26_new_source_ids | r12_names_r26 | exit |
|---|---|---|---|---|---|---|
| 248408f5 | lane root | 4 | absent | 0 | 0 | 0 |
| 248408f5 | /tmp | 4 | absent | 0 | 0 | 0 |
| 327fbcca | lane root | 0 | present | 13 | 4 | 0 |
| 327fbcca | /tmp | 0 | present | 13 | 4 | 0 |
| 16935e24 | lane root | 0 | present | 13 | 4 | 0 |
| 16935e24 | /tmp | 0 | present | 13 | 4 | 0 |
| deadbeef | lane root | bad_rev | — | — | — | 2 |
| deadbeef | /tmp | bad_rev | — | — | — | 2 |

cwd independence is structural, not luck: `count-c1.sh:3` hardcodes `L=/home/vgpnk/Projects/shokunin/mori-shokunin`
and every git call uses `git -C "$L"` (`count-c1.sh:4,8,10,13,15`); no relative paths. The two cwds give byte-identical output.

Independent recomputation (same A1 semantics, different implementation) agrees on every value at every rev:
248408f5 → 4 hits, one per frozen phrase (3 in `userspace-oom-killers-r12.md`, 1 in `corpus/README.md`), r26 entry absent;
327fbcca and 16935e24 → 0 hits, entry present, 13 distinct new ids S114–S126 on its single `source:` line,
4 r12 lines naming the r26 file.

## Verdict per value

- `248408f5` run → **holds.** stale_present=4 / absent / 0 / 0 at both cwds, exit 0; matches receipt
  (`.ufo/waves/round-26/evidence/c1-count.txt:1-6`) and SCORECARD row (SCORECARD.md:1608).
- `327fbcca` run → **holds.** 0 / present / 13 / 4 at both cwds, exit 0; matches receipt (`c1-count.txt:8-13`)
  and SCORECARD row (SCORECARD.md:1608). The 13 equals SOURCES rows S114–S126 inclusive (13 rows).
- `16935e24` run → **holds.** 0 / present / 13 / 4 at both cwds, exit 0; identical to 327fbcca, so the
  wave-2 tip did not regress C1. Not in the receipt because the receipt was committed at `c6ea248`
  (11:15:35) before the tip commit existed (11:27:49) — timeline-explained, not a stale claim; SCORECARD.md:1604
  explicitly pins the measurement at 327fbcca "before wave 2".
- `deadbeef` run → **holds.** `bad_rev`, exit 2 at both cwds (`count-c1.sh:4`), matching receipt
  (`c1-count.txt:15-17`); `rev-parse -q --verify` finds no such object.
- Phrase-list pinning at 28b04940 → **holds.** `count-c1.sh:10` reads the list from the fixed commit
  `28b0494004fe1f064544224eca56dd42605db384:.ufo/waves/round-26/c1-phrases.txt`, and `count-c1.sh:11`
  guards `phrases_read=4` (exit 2 otherwise). `git log -- .ufo/waves/round-26/c1-phrases.txt` shows exactly
  one commit, 28b0494 (2026-10-22 10:10:20, "claim contract, frozen C1 phrase list, before receipts");
  the tip's copy is `diff`-identical to the pinned blob. At 248408f5 the file does not exist in the tree —
  correct, since 28b0494 is 248408f5's child — and the script is immune because it reads the pinned object, not the rev's tree.
- 28b04940 precedes every C1 content commit → **holds.** `git rev-parse 28b0494^` = `248408f5b661…` exactly
  (direct parent). `git log --format='%h %ci %s' 248408f5..16935e24` lists 17 commits, no merges
  (`git rev-list --merges --count` = 0), oldest entry 28b0494 at 10:10:20; every later commit — including the
  superseding entry `327fbcc` (11:14:17), the receipts `c6ea248` (11:15:35), and the tip `16935e2` (11:27:49) —
  descends from it (`merge-base --is-ancestor` yes for 327fbcca and 16935e24; for the others implied by the
  linear parent chain from 248408f5). Ordering: phrase freeze (10:10:20) → counter script (10:21:07) →
  content (11:14:17) → receipt (11:15:35).
- SCORECARD round-26 measured-outcome row → **holds.** SCORECARD.md:1608 states exactly the before/after
  values measured here, with the script path and both full hashes.

## Residual risk (nuances, none a defect)

1. `r12_names_r26` counts **lines** containing the name (`grep -c`, `count-c1.sh:15`), not occurrences:
   at 327fbcca/tip the name occurs 5 times on 4 lines. The printed 4 is faithful to the script's
   definition and to the SCORECARD wording ("names"), but anyone reading it as "mentions" would overstate by one line-wise merge.
2. `r26_new_source_ids` inspects only the first `^source:` line (`grep -m1`, `count-c1.sh:14`). Today the
   r26 entry has exactly one `source:` line carrying all 13 ids (recomputed over all lines: same 13), so
   nothing is missed; a future second `source:` line would be silently ignored.
3. The `tr -d '*'` normalization (`count-c1.sh:9`) could in principle fuse tokens across an asterisk and
   fake a match; none of the four frozen phrases is asterisk-adjacent, and the recomputation found no
   discrepancy, so the counted values are unaffected.
4. The `missing=$f` exit-2 path (`count-c1.sh:8`) is unexercised at these revs (all four listed files exist
   in every tested tree); only the `bad_rev` exit-2 path was exercised.

## Verification gaps

- C2 (`count-c2.sh`), the supplementary cases, and `evidence/c1-before.txt` are outside this seat's mandate; not checked.
- `deadbeef`'s exit-2 provenance rests on `rev-parse` failing for that object name today; a repo that later
  gains an object named `deadbeef…` would flip this branch, but that is inherent to a named-short-hash negative test.
- No LSP server involvement possible (bash scripts); semantic claims above come from git object reads and
  independent recomputation, not grep-as-proof.
