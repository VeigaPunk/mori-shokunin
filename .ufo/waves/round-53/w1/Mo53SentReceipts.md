# Mo53SentReceipts — receipt integrity of `round-53/evidence` at `2a4213bf`

Seat: sentinel, leaf (no subagents). Lane: `mori-shokunin`. Scratch: `/fast/scratch/hyaku/mori-r53/Mo53SentReceipts/`
(TMPDIR `…/tmp`, `mkdir -p`'d, removed at the end; the 336 MB harness clone lived there and is gone).
Nothing was written inside the lane: every lane access below is `git show` / `git ls-tree` / `git archive` /
`git clone --shared` **from** the lane, plus reads. `git status --porcelain` on the lane before and after my runs
showed no path added or changed by me.

Scope read: contract (`…/round-53/contract.md`, tip `20edafa5`), `count-c1.py`, `count-c2.py`,
`controls/controls.py`, `controls/c1-data.py`, every file under `…/round-53/evidence/`.

Two facts that fix what "at `2a4213bf`" means for this directory:

```
$ git ls-tree -r --name-only 2a4213bf8da72f7cd78189baa5bb9be825dca1df -- .ufo/waves/round-53/evidence/
17 files: c1-claims.txt c1-scope.txt census-start.txt freeze-sha256.txt selftest-c1.txt selftest-c2.txt sweeps.txt
          control-c1-{all-held,do-nothing,no-votes,v72-copies,witness}.txt
          control-c2-{do-nothing,memoriser,mode-blind,no-band,witness}.txt
$ git ls-tree -r --name-only 95cf78ee -- .ufo/waves/round-53/evidence/     # adds the two at-data receipts
$ git ls-files .ufo/waves/round-53/evidence/selftests/ ; git status --porcelain .ufo/waves/round-53/evidence/selftests/
?? .ufo/waves/round-53/evidence/selftests/                                # never committed anywhere
```

So the directory holds three vintages: **17 files frozen/at-data** (the 16 freeze receipts + `c1-claims.txt` added by
the data commit), **2 at-data receipts** (`c1-at-data.txt`, `c2-at-data.txt`) that landed one commit later in
`95cf78ee`, and **3 untracked** tool-selftest receipts. All 22 are listed below.

Frozen bytes never moved: `git diff f4da3fd4 2a4213bf -- .ufo/waves/round-53/{contract.md,count-c1.py,count-c2.py,controls,evidence}`
shows one addition only (`c1-claims.txt`, 186 lines); no frozen file was edited in place. The working-tree counters
today hash to the freeze list (`ebaff915…` count-c1, `5684b69f…` count-c2, `1833309c…` c1-data, `f7ba7ac1…`
controls.py), so the copies I re-ran are the frozen ones.

## Method

Each receipt was read for (a) a literal command line (`$ …`), (b) a recorded exit code, (c) whether the recorded
command, re-run, reproduces the verdict line. Cheap arms were all run; the ten control receipts cite throwaway
clones, so for those I did two things instead of a naive re-run: rebuilt all ten from the frozen builder
(`controls/controls.py` + `c1-data.py`) in a scratch clone of the lane at `20edafa5`, and then re-derived the four
C2 controls from their **recorded** control commit id alone (`seed = sha256(<full commit id of R>)`, which
`count-c2.py` documents at line 13).

## Receipt table

`repro` = does re-running reproduce the verdict line. `REBUILT` = re-run not possible as written (clone deleted);
result of the substitute check given.

| # | file | literal cmd | exit code | repro | note |
|---|---|---|---|---|---|
| 1 | `c1-scope.txt` | yes | `exit=0` | **yes**, byte-identical | payload (47 lines) `diff`-clean against a fresh `--scope`; `--scope` reads the hardcoded `ENTERING` pin (`count-c1.py:45`), so it cannot drift |
| 2 | `c1-claims.txt` | **no** | **absent** | **partial** | header is not a command: `$ … --scope   (hashes and quotes); claim text from the same parse`. The h/entry/path/quote columns are byte-identical to `--scope`; the `row=`/`claim:` columns come from an unrecorded formatter. Independently checked: 46/46 `claim:` strings occur verbatim in their entry at `20edafa5`; row numbers are 1…46 in ledger-row order (`ledger order == claims order: True` against the ledger table at `2a4213bf`) |
| 3 | `census-start.txt` | yes (trailing `# at entering tip …` shell comment) | `exit=0` | **yes**, byte-identical | 24-line payload (23 W04 + `mori ok`) reproduced with the same command; `validate` is stdout-only (`--out` unused) |
| 4 | `sweeps.txt` | yes, 5 commands | `exit=` per command (1,1,0,0,0) | **yes, 5/5** | sweeps 1–2 still exit 1 with no match; sweep 3 prints the identical six `file:count` rows; sweep 4 prints `0`; sweep 5 (network) prints the identical `v7.2`, `v7.3`, `v7.3^{}` hashes (`c03c1a14507dfaf8b856c2608f9ac216021fc222`) |
| 5 | `selftest-c1.txt` | yes | `exit=0` | **yes**, byte-identical | 38-line payload reproduces `C1_SELFTEST pass=37 fail=0` |
| 6 | `selftest-c2.txt` | yes | `exit=0` | **yes**, byte-identical | 31-line payload reproduces `C2_SELFTEST pass=30 fail=0` |
| 7 | `control-c1-do-nothing.txt` | yes | `exit=1` | **yes** (rev = `20edafa5`, run in the lane) | line identical including `rev=`; as written it points at a deleted clone (see finding F2) |
| 8 | `control-c1-all-held.txt` | yes | `exit=1` | **REBUILT: yes** | identical except `rev=` (`1b0ca6b3…` → `db0403fa…`): `status_ok=44 quote_ok=44 … failed=quote,status` |
| 9 | `control-c1-v72-copies.txt` | yes | `exit=1` | **REBUILT: yes** | identical except `rev=` (`be1605d2…` → `cd462394…`): `pins=bad … failed=pins,quote,status` |
| 10 | `control-c1-no-votes.txt` | yes | `exit=1` | **REBUILT: yes** | identical except `rev=` (`9d57772f…` → `381d65d2…`): `voted=0 … failed=votes` |
| 11 | `control-c1-witness.txt` | yes | `exit=0` | **REBUILT: yes** | identical except `rev=` (`07546461…` → `75df61e4…`): `C1=met … voted=46 dissent=0` |
| 12 | `control-c2-do-nothing.txt` | yes | `exit=1` | **yes** (rev = `20edafa5`) | line identical including `rev=` |
| 13 | `control-c2-mode-blind.txt` | yes | `exit=1` | **REBUILT: no; RE-DERIVED: yes** | rebuild: `agree=51 disagree=29` vs receipt `53/27`; re-derived from the recorded rev `55a9d533…`: `agree=53 disagree=27` with the identical seeded ids (finding F1) |
| 14 | `control-c2-no-band.txt` | yes | `exit=1` | **REBUILT: no; RE-DERIVED: yes** | rebuild `72/8`; re-derived from `dcd51556…`: `71/9` with the identical nine ids, incl. `mode2-band-edge-low` |
| 15 | `control-c2-memoriser.txt` | yes | `exit=1` | **REBUILT: no; RE-DERIVED: yes** | rebuild `77/3`; re-derived from `87f55717…`: `71/9` with the identical ids `seeded-01,04,06,14,19,29,43,44,56` |
| 16 | `control-c2-witness.txt` | yes | `exit=0` | **REBUILT: yes** | `agree=80 disagree=0`, `C2=met`; `rev=` differs |
| 17 | `freeze-sha256.txt` | **no** | **absent** | **verified by derivation** | 32/32 hashes equal the bytes at `f4da3fd4`; completeness in F6 |
| 18 | `c1-at-data.txt` | yes | `exit=1` | **yes**, line identical | `C1=unmet scope=46 … voted=0 dissent=0 … failed=votes`; committed in `95cf78ee`, bytes equal the worktree copy |
| 19 | `c2-at-data.txt` | yes | `exit=0` | **yes**, line identical | `C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok`; I substituted my own `--scratch`, so the reading is scratch-independent |
| 20 | `selftests/mori-commit-runway.txt` | yes | `exit=0` | **yes** from an archive of `2a4213bf` | `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23`; body is the whole 2-line output |
| 21 | `selftests/mori-pin-check.txt` | yes | `exit=0` | **yes** from an archive of `2a4213bf` | `PIN_CHECK_SELFTEST pass=125 fail=0`; body shows 5 of 125 PASS lines (finding F3) |
| 22 | `selftests/mori-unlanded-check.txt` | yes | `exit=0` | **yes** from an archive of `2a4213bf` | `UNLANDED_SELFTEST pass=17 fail=0`; body shows 5 of 17 PASS lines (finding F3) |

Counts: 22 receipts; 20 record a literal command; 20 record an exit code; 21 reproduce their verdict line by one
route or another (19 by direct re-run/archive, 2 more by rebuild/re-derivation); 1 (`c1-claims.txt`) only in part.

## Detail — control commits are gone, and that is not a fabrication

```
$ for c in 1b0ca6b3… 9d57772f… be1605d2… 07546461… 55a9d533… dcd51556… 87f55717… 2890d6c3…; do git cat-file -e $c; done
… ABSENT ×8
$ ls -d /fast/scratch/hyaku/mori-r53/L1/controls/*
ls: cannot access '…/L1/controls/*': No such file or directory
```

The receipts' header is `controls.py`'s own template (`# control %s (parts: %s); clone of the lane at %s%s, control
commit %s`), and rebuilding with the frozen builder reproduces the C1 lines exactly (mod `rev=`) and the C2 lines'
shape, so the generator is established. Re-deriving from the recorded rev closes the gap completely for C2:

```
$ python3 -   # imports the frozen count-c2.py + controls.py WRAPPER, calls evaluate_tree(tree, sha256(rev), SKILL@2a4213bf, live=False)
c2-memoriser  | C2=unmet … n=12 fixtures=80 agree=71 disagree=9 … | ids: 01 04 06 14 19 29 43 44 56
c2-no-band    | C2=unmet … n=12 fixtures=80 agree=71 disagree=9 … | ids: mode2-band-edge-low 04 09 13 15 16 18 40 45
c2-mode-blind | C2=unmet … n=12 fixtures=80 agree=53 disagree=27 … | ids: host-mode0-over mode1-over mode0-limit-mismatch 01 02 04 07 12 18 20 22 23 24 27 29 30 33 35 37 38 40 41 43 44 49 50 57
c2-witness    | C2=met … agree=80 disagree=0
```

Every number and every seeded id in receipts 13–16 is reproduced from the rev alone. `n=12` is the wrapper's fake
selftest count and `n=23` is the real tool's, which is why the at-data receipt reads 23.

## Detail — `freeze-sha256.txt`

```
$ python3 -   # git show f4da3fd4:<path> | sha256 for each listed row
listed entries: 32  ok: 32  bad: 0  missing: 0
freeze-commit files: 33
in commit not listed: ['.ufo/waves/round-53/evidence/freeze-sha256.txt']
listed not in commit: []
```

The one unlisted freeze-commit file is the digest list itself — it cannot contain its own hash. The list covers
`contract.md`, both counters, both control builders, the 18 non-digest receipts, and the 12 `sources-r53` copies,
and every value matches.

## Detail — an honest-looking but fragile re-run surface

At 23:14, mid-run and after my reproductions, another process (the L1 integrating; not me, I wrote nothing in the
lane) edited three data files in the worktree:

```
$ git diff --stat 2a4213bf -- SKILL.md corpus/knowledge/commit-runway-read-r53.md tools/mori-commit-runway.py
 SKILL.md                                   |   2 +-
 corpus/knowledge/commit-runway-read-r53.md |   8 +-
 tools/mori-commit-runway.py                | 159 ++++++++++++++++++++++++++-----
$ sha256sum tools/mori-commit-runway.py ; git show 2a4213bf:tools/mori-commit-runway.py | sha256sum
82924be7…  tools/mori-commit-runway.py
80cb1696…  (at 2a4213bf)
$ python3 -I -B tools/mori-commit-runway.py --selftest        # from today's lane worktree
MATCHER: rejected 23/23 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 28/28
exit=0
```

Receipt 20 says `PASS 23/23` and is right for `2a4213bf`; run from the live worktree the same `$` line now prints
28/28. Nothing false, but the receipt's `$` line carries no rev — only the comment line above it does.
`count-c2.py` scores at the rev (`git archive <rev>`, line 409; `git show <rev>:SKILL.md`, line 414), so my
`c2-at-data` reproduction (which ran after the edits) is unaffected by them.

## Findings

- **MED — `evidence/control-c2-{mode-blind,no-band,memoriser}.txt` (and the contract's control table).** Re-running
  the frozen builder does **not** reproduce the recorded disagreement counts: rebuild gives `51/29`, `72/8`, `77/3`
  against the recorded `53/27`, `71/9`, `71/9`. Cause: `count-c2.py` seeds the 64 generated fixtures with
  `sha256(<full commit id of R>)` (docstring line 13), and R for a control is a fresh throwaway commit, so each
  rebuild draws a different fixture population. The readings are nevertheless exact — re-deriving with the recorded
  rev reproduces every count and every seeded id. Consequence for the round: the numbers in the contract's control
  table are one-shot, and the memoriser's *margin* is seed-dependent (9/64 on the recorded seed, 3/64 on my rebuild)
  although its verdict stays `C2=unmet` in both. No counter or kill-rule change belongs to this round; routing: the
  control receipt should be worded so a reader re-derives (`seed = sha256(rev)` over the frozen builder) instead of
  re-running `controls.py`, and round 54 should treat "control margin is a function of the throwaway commit" as a
  named limit of the C2 control set.
- **LOW — all ten `evidence/control-*.txt`.** The recorded `--repo` argument is a clone that no longer exists and
  whose commit is unreachable in every repo on this host (`git cat-file -e` ABSENT ×8), so no control receipt is
  re-runnable as written and its `rev=` is unresolvable text. Substitutes verified: rebuild reproduces 5/5 C1 lines
  (mod `rev=`); rev-seeded re-derivation reproduces 4/4 C2 lines. The contract discloses the deletion, so this is a
  recorded limit rather than a defect, but the receipts themselves do not say how to re-derive them.
- **LOW — `evidence/selftests/*.txt`.** All three are untracked (no commit pins their bytes) and each body is a
  truncated tail — 5 of 125, 5 of 17, 2 of 2 lines — with no elision marker. Every shown line appears verbatim in my
  re-run and the totals match, so the content is honest; what is missing is byte custody and any sign that output
  was dropped. A receipt that is not committed cannot be shown to be the one that ran.
- **LOW — `evidence/selftests/mori-commit-runway.txt`.** Its `$` line does not name the rev it was run at; from the
  lane worktree today it prints `PASS 28/28`, not the recorded 23/23, because the tool was edited at 23:14. The
  archive is reproducible from `2a4213bf`, so the receipt stands, but the command alone is ambiguous.
- **LOW — `evidence/c1-claims.txt`.** Not a receipt: no command produces the file verbatim (the header says "claim
  text from the same parse") and no exit code is recorded, yet this is the index all twelve voter seats read their
  row numbers from. Independently verified anyway: 46 claim strings verbatim in their entries at `20edafa5`, row
  numbers 1…46 in ledger-row order, h/entry/path/quote columns byte-identical to `--scope`.
- **LOW — `evidence/freeze-sha256.txt`.** Carries neither a command nor an exit code (a derivation, not a run), and
  by construction cannot list itself. Content verified: 32/32 match the bytes at `f4da3fd4`; no frozen file changed
  between the freeze and the data commit.
- **LOW — all receipts.** None records its working directory, and `sweeps.txt` line 1 and the counters' `$` lines use
  lane-relative paths. The fleet root is itself a git repo
  (`git -C /home/vgpnk/Projects/shokunin rev-parse --is-inside-work-tree` → `true`), so running the shared `git grep`
  line from there misfires — it fails loudly (`fatal: unable to parse object 20edafa5…`), so the ambiguity is
  detectable rather than silent.

- **LOW — `r53-data.tar`, lane root (not an evidence file; corroborated, not owned here).** An untracked 51200-byte
  tarball of `tools/` appeared at the lane root at 23:19:41 while this report was being written. It holds the
  `2a4213bf` bytes, not the edited worktree ones (`mori-commit-runway.py` = `80cb1696…` = `git show 2a4213bf:…`;
  `cases.json` = `cea80451…` both sides), so it does not contaminate any receipted byte — but it is an untracked
  file inside a tracked tree. I did not create it; the operator directive to report files created in the lane root
  applies to the seat that did. Occupant of this ground is `w1/Mo53ExecC2Replay.md` finding 8.

UNVERIFIED: who edited the three data files at 23:14 (not me; I wrote nothing in the lane), who wrote
`r53-data.tar`, and whether the control receipts were produced inside the same clone paths they name (the generator
template and the reproduced readings are consistent with it).

Tooling: none installed, upgraded or removed. No pacman transaction was attempted. Network use: one
`git ls-remote https://github.com/torvalds/linux` (read-only, to reproduce `sweeps.txt`). Host reads: none beyond the
counters' own `/proc` reads during a faithful re-run of `count-c2.py`.
