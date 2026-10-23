# Recheck046 — C1 freshness row S046

Seat: `MoriR32A2.Recheck046` (leaf scout, no subagents, no git/jj writes, no installs needed).
Population source: `.ufo/waves/round-32/c1-population.json` (S046), base row `corpus/SOURCES.md:52`.

## 1. Fetch record

- id: S046
- url (population url, unchanged as url cell): https://git-scm.com/docs/git-merge-base
- fetch command: `curl -sSL --fail -m 60 https://git-scm.com/docs/git-merge-base -o /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck046/S046.src`
- accessed: `2026-10-23T01:31:24Z` (`date -u +%FT%TZ` at the fetch)
- byte size: 41401 bytes (`ls -l S046.src`)
- sha256: `0dc2f88a4935851e824b3d35c8236d7d4ad4603554b2ff24cc25ec83962868f3` (`sha256sum S046.src`)
- scratch copy: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck046/S046.src` (bytes saved unchanged; no excerpt)
- redirects: none. `curl -sS -o /dev/null -w 'effective=%{url_effective} code=%{http_code} redirects=%{num_redirects}\n' -L https://git-scm.com/docs/git-merge-base` printed `effective=https://git-scm.com/docs/git-merge-base code=200 redirects=0`. No moved location to report.
- normalised text used to pick quotes: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck046/S046.text`, produced by `python3 .ufo/waves/round-32/seat-check.py text S046.src` (9418 bytes, one line).

## 2. Ready-to-paste row

Fenced block holds the exact single table line (header the L1 owner must have: `| id | url | accessed | sha256 | quotes | verdict |`):

```
| S046 | https://git-scm.com/docs/git-merge-base | 2026-10-23T01:31:24Z | 0dc2f88a4935851e824b3d35c8236d7d4ad4603554b2ff24cc25ec83962868f3 | "Check if the first <commit> is an ancestor of the second <commit>"; "exit with status 0 if true, or with status 1 if not"; "Errors are signaled by a non-zero status that is not 1" | current |
```

## 3. Quote to teaches-cell support

Teaches cell: "Exit 0 means ancestor, 1 means not ancestor, and another nonzero status means error; a probe must not report every nonzero status as divergence." Scope: "ancestry-check exit status". Anchor: "OPERATION MODES, --is-ancestor; last updated 2.43.0, no changes listed through 2.56.0; opened 2026-10-20".

1. `Check if the first <commit> is an ancestor of the second <commit>` — the `--is-ancestor` definition in OPTIONS; supports the ancestry predicate half of the teaches cell. Verbatim in normalised text at offset ~3915 (the page renders `<commit> ,` with a space before the comma, so the quote is cut at the closing `>` to keep whole-word boundaries and avoid page artefacts). Note the synopsis line `git merge-base --is-ancestor <commit> <commit>` is also present, confirming the mode still exists.
2. `exit with status 0 if true, or with status 1 if not` — the numeric exit contract: 0 = ancestor, 1 = not ancestor. Direct support for the first clause of the teaches cell; the negation "not" is quoted whole.
3. `Errors are signaled by a non-zero status that is not 1` — supports the second clause: any status other than 0/1 is an error, so a probe must not fold every nonzero status into "diverged". Negation "not 1" kept intact; "non-zero" is a hyphen inside the sentence, not PDF line-end hyphenation.

Anchor check: the live page still says `last updated in 2.43.0` and `Changes in the git-merge-base manual 2.43.1 → 2.56.0 no changes` in the changelog block. I did not quote that block because it is page furniture (version-change widget), but it corroborates the anchor cell without contradicting it.

Verdict follows: the live bytes contain all three passages, and each states exactly the teaches-cell claim (0/1/non-1 distinction plus the ancestor predicate). Nothing in the page weakens or changes the claim, so `current`.

## 4. seat-check output (verbatim)

Command:
```
cd /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck046 && timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/seat-check.py row S046 S046.src '"Check if the first <commit> is an ancestor of the second <commit>"; "exit with status 0 if true, or with status 1 if not"; "Errors are signaled by a non-zero status that is not 1"'
```
Output:
```
sha256=0dc2f88a4935851e824b3d35c8236d7d4ad4603554b2ff24cc25ec83962868f3
quotes=3 words=[12, 12, 11] in_copy=[True, True, True]
shared_tokens=['ancestor', 'check', 'exit', 'status'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```
Exit code 0. `live_quotes_ok=True` means the helper's own live re-fetch also contains all three quotes (independent of my saved copy).

## 5. Drift details

None. Verdict is `current`, so no `Round32` correction is owed to `corpus/knowledge/jj-branch-anchor-r17.md`. That file already leans on this row (`corpus/knowledge/jj-branch-anchor-r17.md:23-24,63`: exit 0 = no off-branch finding, exit 1 = `HEAD_BRANCH_MISMATCH`, and line 63 says the merge-base diagnostic relies on S046's numeric error distinction), and the live page still supplies exactly that distinction.

## Notes / bounds compliance

- Wrote only this report and files under `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck046/`. No git/jj writes, no lane edits, no subagents, no background jobs, no pacman (all host pacman transactions paused; no install was needed).
- Only public HTTPS read via `curl`; no bot challenge encountered (single 200, zero redirects).
- Counters were not run; row check R4 (judge receipt) and R1's table placement are the L1 owner's integration step.
