# Mo53ExecC1Replay — independent replay of the frozen C1 counter (round 53, wave w1)

Role: executor, C1 counter replay. Scope: re-run `count-c1.py` at the data commit, `--selftest`, `--scope`,
and the do-nothing control at the entering tip; compare each with its frozen receipt; then re-derive the claim
from the kernel bytes and the ledger without the counter. No counter, predicate, floor or kill rule changed or
proposed for change here. Everything below is observed evidence (command, output, exit code) unless marked
`[INFERENCE]`.

Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecC1Replay/` (clone `clone-lane`, nine cgit copies in `fetch/`,
`TMPDIR` under it), removed at the end. Nothing was written inside the lane except this report; the lane's
`git status` and every frozen evidence sha256 were unchanged after all runs (verified, see §7).
No tool installed, upgraded or run through pacman; Python 3.14.8 and git 2.56.0 as already present.

## 1. The four receipt comparisons (all four reproduce)

Run from the scratch directory, `TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecC1Replay/tmp`.

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/count-c1.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df
C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df failed=votes
exit=1
```
identical to `evidence/c1-at-data.txt` (that file's two non-output lines, the `$ …` command echo and `exit=1`,
excluded): `identical=True`.

```
$ python3 …/count-c1.py --selftest
ok   honest_met
… 37 lines …
ok   scope_reader
C1_SELFTEST pass=37 fail=0
exit=0
```
identical to `evidence/selftest-c1.txt`, all 37 arm names in the same order: `identical=True`.

```
$ python3 …/count-c1.py --scope
h=2d0daa4192f1 entry=corpus/knowledge/memavailable-estimate-r51.md path=Documentation/filesystems/proc.rst quote=An estimate of how much memory …
… 46 h= lines …
scope=46
exit=0
```
identical to `evidence/c1-scope.txt` (command echo and `exit=0` excluded): `identical=True`, 46 h= lines.

Do-nothing control, run against the lane itself at the entering tip rather than through the L1's clone:

```
$ python3 …/count-c1.py 20edafa59b38dac1ca358893f0259b1f436372d3
C1=unmet scope=46 rows=0 matched=0 status_ok=0 quote_ok=0 source_rows=bad pins=bad provenance=bad held=0 absent=0 holds=0 changed=0 voted=0 dissent=0 rev=20edafa59b38dac1ca358893f0259b1f436372d3 failed=ledger_absent,pins
exit=1
```
identical to `evidence/control-c1-do-nothing.txt` outside its `# control`, `$ …` and `exit=` lines:
`identical=True`. Same output also through `--repo` on my scratch clone. Determinism: three consecutive
runs at the data rev gave one distinct output line (`sort | uniq -c` → `3`).

Bonus, not asked for: the data-commit line is also byte-identical to `evidence/control-c1-no-votes.txt` outside
the rev hash — the data commit is the no-votes state, as the contract says it must be.

## 2. The pins survive an independent re-fetch from cgit

I re-fetched all nine paths myself, `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=v7.3`,
one curl each, into scratch, and compared with the counter's frozen `V73` dict and with `evidence/freeze-sha256.txt`:

| path | http | sha256 (= frozen pin) |
|---|---|---|
| `Documentation/filesystems/proc.rst` | 200 | `bc178ff511e05c1b…` |
| `mm/show_mem.c` | 200 | `c50205bc19974566…` |
| `fs/proc/meminfo.c` | 200 | `d6c5807421a69eac…` |
| `include/linux/mm_inline.h` | 200 | `277e99e23ecc1b5b…` |
| `Documentation/mm/overcommit-accounting.rst` | 200 | `767ab88153c4494e…` |
| `Documentation/admin-guide/sysctl/vm.rst` | 200 | `f81feb3dfca5f054…` |
| `mm/util.c` | 200 | `4dfcce2b8fa8f18c…` |
| `include/linux/mman.h` | 200 | `d7bf787c910d9a7c…` |
| `mm/mmap.c` | 200 | `8e51fb1c10fee694…` |

`9/9 MATCH` against the counter's pins, and `9/9` against `freeze-sha256.txt`. So the pins do not merely prove
"the L1 fetched this": they prove the bytes cgit serves for `?h=v7.3` today. Tag re-verified independently from
the cgit host: `refs/tags/v7.3` → `091b06388b117fefdcb63336ac09956a4914b961`, `refs/tags/v7.3^{}` →
`c03c1a14507dfaf8b856c2608f9ac216021fc222`, matching `evidence/sweeps.txt` and the contract.

The v7.2↔v7.3 drift the ledger narrates is also true on the committed copies: `cmp` over
`sources-r51/*.v7.2` vs `sources-r53/*.v7.3` gives identical bytes for `meminfo.c`, `mman.h`,
`overcommit-accounting.rst`; `diff -u | grep -c '^[-+][^-+]'` gives 3 for `proc.rst`, 22 for `show_mem.c`,
49 for `mm_inline.h`, 64 for `vm.rst`, 14 for `util.c`, 190 for `mmap.c` — exactly the ledger's table.

## 3. The claim re-derived without the counter

My own parser (`indep2.py`, `ledger_check.py` in scratch) re-read the two entry tables at the entering tip,
resolved each `S…` row in `corpus/SOURCES.md` to its `v7.2/` URL, hashed the whitespace-collapsed claim text,
and checked the ledger at `2a4213bf`:

- scope `46`; `held=44`, `absent=2`; the absent pair is exactly `0fbd62f51ce8` and `d7a1dc88dcb3`, both
  `mm/mmap.c` — the two `MAP_NORESERVE` rows the contract predicts.
- 46 ledger rows, one per scope hash, no duplicate, no extra; every `entry` cell names the entry I derived it
  from; every `status` cell equals my derivation; every `quote` cell is one backticked span, 6–25 words, present
  (whitespace-collapsed) in the v7.3 copy — and equal to the v7.2 quote when the status is `held`; every
  `disposition` is `holds`/`changed`; every source row is `mined`, dated `2026-10-26`, carries the frozen v7.3
  URL, and lists the ledger in used-by. **`problems 0` / 46 rows** — the counter's
  `status_ok=46 quote_ok=46 source_rows=ok provenance=ok pins=ok` are not self-referential.
- The v7.3 `mmap.c` really does respell the flag write: lines 563–570 of the v7.3 copy read
  `if (flags & MAP_NORESERVE) { … if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT); … if (file && is_file_hugepages(file)) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT); }`
  — same rule, different spelling, so `absent` + `holds` is the right pair for those two rows.
- `evidence/c1-claims.txt` is faithful: 46 rows, row N is ledger row N (0 order mismatches), every claim hash
  recomputes from the printed claim text, every v7.2 quote matches my parse.
- The three out-of-scope rows are the `S496` rows 19–21 of `memavailable-estimate-r51.md` (the 2014
  `34e431b0` commit patch), exactly the three the contract excludes; 49 claim rows total.

## 4. The vote arm: met, if the reports are committed

At the data commit and at lane HEAD the counter reads `voted=0`, because it reads voter reports with
`git show <rev>:<path>` and `git ls-tree <rev>` only — reports present in the working tree but untracked do not
count. That is the correct reading for both receipts and for the no-votes control.

State of the twelve reports now (all twelve present, sha256 recorded while I ran):

| seat | vote lines | word |
|---|---|---|
| Mo53Fr01–Mo53Fr06 | 12 each | holds |
| Mo53Fr07–Mo53Fr12 | 11 each | holds |

46 rows × 3 votes = 138 vote lines, all `holds`, no dissent, no duplicated hash inside a report, even fence
counts in all twelve, and no stray line of that form in any of the 42 non-voter reports. To test the arm I
committed those twelve reports into my scratch clone (nothing in the lane) and re-ran:

```
$ python3 …/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r53/Mo53ExecC1Replay/clone-lane
C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0 rev=a259adeb059e41cd0e46ec232c3973dbe39ea88d
exit=0
```
— the contract's target line exactly, `voted=46 dissent=0`, exit 0. With only the five reports that existed at
22:47 the same run gives `voted=13`; with the twelve it is 46. **The only thing between the landed tip and
`C1=met` is committing `w1/Mo53Fr*.md`.**

## 5. What I could break, and what held

Against the clone (never the lane):

- uncommitted worktree tamper of a v7.3 copy → still `C1=met`: correct, the scored path reads `git show`.
- committed tamper (`util.c.v7.3` replaced) → `pins=bad status_ok=37 quote_ok=37 held=35 absent=11`, exit 1:
  the pins arm catches a doctored copy and the status arm follows it down.
- one voter flipped to `changed` on one row → `voted=45 dissent=1 failed=votes`, exit 1; the same voter's later
  line flipping back → `C1=met` again: last unfenced line wins, dissent is detected.
- a vote line for a hash outside scope → ignored, still met.
- unresolvable rev → `C1_SETUP unresolvable revision …`, exit 2; bad or missing argument → usage line, exit 2.

## 6. Counter weaknesses (frozen — named limits for round 54, not fixes)

1. **Author-exclusion compares escaped text.** `final_votes` stores a proposed quote as
   `ws(text.strip("`"))` but `one_quote` unescapes `\|` → `\|`; so a proposal written with an escaped pipe never
   matches the row quote and the proposer's vote is **not** excluded. Probe: row quote
   `vm_flags |= VM_NORESERVE under mode 2`, proposal written `vm_flags \|= …` → `agree=2` (author counts);
   proposal written raw `vm_flags |= …` → `agree=1` (author excluded, intended). Unreachable with today's data:
   no ledger row quote contains a literal pipe (the only pipe in the file is in the prose table, line 100), and
   no report has any proposal line. LOW.
2. **"Does not count" is applied to the agreement arm only.** The predicate says a proposer's line does not
   count; the counter drops it from `agree` but still lets it set `dissent` (`any(word != disp for word in
   v.values())`). A proposer who proposes the quote and votes the other word makes a row dissent that the
   predicate's plain reading would pass. Fail-closed (harder, never easier), and unreachable today. LOW.
3. **A second table appended after the ledger is silently ignored.** `parse_table` stops at the first non-`|`
   line once rows have begun, so "exactly one table … and no other row" is enforced only forwards: a decoy table
   placed *before* is parsed (and fails loudly, `rows=1 matched=0`), a decoy table *after* is not seen
   (`rows=46`, unchanged). LOW.
4. **`--selftest` is not rev-pinned.** It reads the nine copies from `lane_root()` on disk, not from a revision;
   a tampered worktree copy makes it die with an uncaught `ValueError: substring not found` (traceback, exit 1)
   rather than a named failed arm. The scored path is unaffected. LOW.
5. Boundary margins in the data, not the counter: four quotes sit exactly at `MIN_WORDS=6`
   (`10ac5a250ac2`, `1cadeed9914b`, `967021950067`, `9cb0e908f997`) and one at 24 of 25
   (`61b7677d56fe`). Any future rewording of those cells flips `quote_ok` without touching the rule. LOW,
   informational.

## 7. Footprint

No file created or modified inside `/home/vgpnk/Projects/shokunin/mori-shokunin` except this report. Verified:
`sha256sum evidence/*.txt` before and after all runs → unchanged; lane `git status --porcelain` still shows only
the pre-existing untracked `w1/`, `w1.ready*`, `evidence/selftests/`. The counter is read-only by construction
(`git show`, `git ls-tree`, `git rev-parse`, one `open(..., "rb")` in the selftest) — confirmed by grep. All nine
cgit fetches and the clone lived under scratch (338 MB) and were deleted.

## Findings

- **LOW — counter, `count-c1.py:179` and `:249`:** the author-exclusion arm compares an escaped proposal text
  against an unescaped row quote, so a proposal containing a literal pipe does not exclude its proposer's vote.
  Unreachable with the current ledger (no row quote has a pipe) and with the current reports (no proposal lines).
  Route to round 54; the counter is frozen.
- **LOW — counter, `count-c1.py:250`:** "a voter's line does not count for a row whose quote that voter
  proposed" is implemented for the 2-agreeing-voters arm only; the proposer's other-word line still raises
  `dissent`. Stricter than the predicate sentence, so fail-closed; route to round 54.
- **LOW — counter, `count-c1.py:99-110`:** `parse_table` stops at the first non-`|` line, so a second
  ledger-shaped table after the real one is not detected; only a decoy placed before it is (that one fails
  loudly).
- **LOW — counter, `count-c1.py:334-345`:** `--selftest` reads the v7.3 copies from the working tree via
  `lane_root()` instead of a revision, so it is not rev-pinned and a tampered copy crashes it with an uncaught
  `ValueError` instead of a named failed arm.
- **MED — landing step, `.ufo/waves/round-53/w1/Mo53Fr01.md`–`Mo53Fr12.md`:** the vote arm reads voter reports
  only through `git show`/`git ls-tree` at the scored revision; the twelve reports are currently untracked, so
  both the data commit and lane HEAD read `voted=0` (`failed=votes`, exit 1). Committing the twelve real reports
  into a scratch clone yields the contract's exact target line, `C1=met … voted=46 dissent=0`, exit 0. The
  landed tip must include them.
- **LOW — data, `corpus/knowledge/kernel-v7.3-recheck-r53.md`:** five quote cells sit on a word-count boundary
  (four at the 6-word floor, one at 24 of 25); any rewording there flips `quote_ok` without a rule change.
- **No finding — reproducibility.** All four receipts reproduce byte-for-byte outside their command/exit
  framing; the nine pins re-fetch identical from cgit; scope 46 / held 44 / absent 2 / 46 rows / 0 problems
  re-derived from the entry tables, `SOURCES.md` and the kernel copies without the counter.
