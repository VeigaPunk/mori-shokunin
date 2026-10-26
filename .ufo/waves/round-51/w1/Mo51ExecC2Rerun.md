# Mo51ExecC2Rerun — independent re-run of the C2 counter (wave w1, round 51)

Seat: executor, leaf. Item: re-run `count-c2.py` independently (data commit, selftest, entering tip, hash listing),
verify the frozen bytes and that the frozen paths did not move between the freeze commit and the data commit.
No subagent was used. No tool was installed or upgraded (nothing was needed).

Environment: MACHINE_ID host, Python 3.14.8, git 2.56.0, disk-guard `status` rc 0 before the runs
(`/fast/scratch/hyaku 25% used, 602.3G free`; `/tmp` 3%, `/home` 35%). Scratch root
`/fast/scratch/hyaku/mori-r51/Mo51ExecC2Rerun/` with `TMPDIR=/fast/scratch/hyaku/mori-r51/Mo51ExecC2Rerun/tmp`;
`/tmp` was not used. All commands were run with the scratch dir as cwd; the counters are read-only
(`git show` / `git ls-tree` / `git rev-parse`), so no clone was needed. Every read path below is absolute.

Revisions: freeze `4677910eae6df3dabd38fe9a0daf1945146a1110`, data `87e0c374537557754bf71dd68036ded3ddc6699c`
(=`87e0c374…`), entering tip `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd`, lane tip observed `b504cb1701568a0038aab9d98ec13d28eff801da`.

## 1. Data commit — counter line

```
$ cd /fast/scratch/hyaku/mori-r51/Mo51ExecC2Rerun && export TMPDIR=$PWD/tmp
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/count-c2.py 87e0c374537557754bf71dd68036ded3ddc6699c
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment
exit=1
```

Identical to `evidence/c2-at-data.txt` (`C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5
source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 … failed=entailment`, exit=1). The one failing arm is
entailment; every other arm (claims floor, located quotes, bad rows, sources floor, source rows, pins, provenance)
reads green exactly as the receipt says. Ran twice in the same session: byte-identical line and exit code both times
(determinism check).

## 2. Selftest — 34 checks

```
$ python3 …/.ufo/waves/round-51/count-c2.py --selftest
PASS honest_met
PASS entry_absent_unmet
PASS no_table_unmet
PASS altered_quote_unmet
PASS quote_from_wrong_copy_unmet
PASS short_quote_unmet
PASS long_quote_unmet
PASS duplicate_quote_unmet
PASS claims_floor_unmet
PASS sources_floor_unmet
PASS row_not_mined_unmet
PASS row_opened_other_day_unmet
PASS used_by_missing_unmet
PASS indented_row_ok
PASS code_indented_row_unmet
PASS pin_mismatch_unmet
PASS table_id_uncited_in_source_unmet
PASS verified_at_missing_unmet
PASS header_wrong_unmet
PASS claim_cell_short_unmet
PASS breadcrumb_identical_claims_unmet
PASS claim_echoes_quote_unmet
PASS table_inside_fence_unseen_unmet
PASS other_entry_path_unmet
PASS entail_no_votes_unmet
PASS entail_one_row_unreviewed_unmet
PASS entail_dissent_unmet
PASS entail_l1_file_ignored_unmet
PASS entail_other_dir_ignored_unmet
PASS entail_hash_of_other_text_unmet
PASS entail_hash_whitespace_folded_met
PASS entail_non_md_ignored_unmet
PASS words_beyond_counts
PASS text_copy_keeps_angle_brackets
C2_SELFTEST pass=34 fail=0
exit=0
```

Matches contract target (`C2_SELFTEST pass=34 fail=0`) and `evidence/selftest-c2.txt` line for line, including the
six entailment-arm controls (no votes, one row unreviewed, dissent, L1-authored file ignored, other directory
ignored, hash of other text, whitespace-folded hash accepted, non-`.md` ignored) — exit 0.

## 3. Entering tip — control reading

```
$ python3 …/.ufo/waves/round-51/count-c2.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd
C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad entailed=0 dissent=0 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=entry_absent,pins
exit=1
```

Exactly the expected `failed=entry_absent,pins`, and identical to `evidence/control-c2-do-nothing.txt` (which also
shows the command and exit=1). The do-nothing control therefore reproduces on this host.

Additionally run at the current lane tip `b504cb17` (the wave-spec/dispatch commit after the data commit):

```
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=b504cb1701568a0038aab9d98ec13d28eff801da failed=entailment
exit=1
```

The spec/dispatch commit changed no C2 arm.

## 4. Hash listing — clean diff against the receipt

```
$ python3 …/.ufo/waves/round-51/count-c2.py --hashes 87e0c374537557754bf71dd68036ded3ddc6699c > hashes.txt
exit=0
$ diff -u …/.ufo/waves/round-51/evidence/c2-hashes-at-data.txt hashes.txt
diff_exit=0
$ wc -l hashes.txt
21 hashes.txt
```

21 rows, no difference. Independent recomputation (Python 3.14.8, my own table parser: header must be exactly
`claim | source | quote`, cells split on unescaped `|`, `sha256(whitespace-collapsed claim).hexdigest()[:12]`)
against `git show 87e0c374:corpus/knowledge/memavailable-estimate-r51.md` and the 21 receipt lines:

```
rows parsed: 21 evidence rows: 21 header: 1
mismatches: []
distinct claims: 21 distinct quotes: 21
```

Every one of the 21 `<h>` values reproduces from the committed entry text, and every claim cell string matches the
receipt verbatim. So the receipt is not a hand-typed transcription of the counter; it is recoverable from R.

## 5. Independent re-check of the non-entailment arms at R

Same independent parser, over `git show 87e0c374:…` for the entry, `corpus/SOURCES.md` and the five copies:

```
independent problems: []          # per row: 1 backticked span, 6–25 words, >=3 words of 3+ letters absent from
                                  # the quote, claim >= 6 words, claim/quote unique, S-id -> SOURCES row -> URL
                                  # among the five frozen, quote found in the whitespace-collapsed copy at R
rows: 21 distinct claims: 21 distinct quotes: 21
SOURCES row count: 269
OK  corpus/evidence/sources-r51/34e431b0.patch      5199 bytes
OK  corpus/evidence/sources-r51/meminfo.c.v7.2      6046 bytes
OK  corpus/evidence/sources-r51/mm_inline.h.v7.2   19417 bytes
OK  corpus/evidence/sources-r51/proc.rst.v7.2     107560 bytes
OK  corpus/evidence/sources-r51/show_mem.c.v7.2    13204 bytes   # each sha256 == freeze-sha256.txt, bytes at R
```

Source spread (rows per S-id): S492 5, S493 8, S494 3, S495 2, S496 3 — all five drawn on, consistent with
`sources=5`. The five copies at R hash to their frozen values, so the `pins=ok` arm is also true from git objects,
not just from the working tree.

## 6. Frozen bytes and frozen-path drift

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum -c …/.ufo/waves/round-51/evidence/freeze-sha256.txt
corpus/evidence/sources-r51/34e431b0.patch: OK
corpus/evidence/sources-r51/meminfo.c.v7.2: OK
corpus/evidence/sources-r51/mm_inline.h.v7.2: OK
corpus/evidence/sources-r51/proc.rst.v7.2: OK
corpus/evidence/sources-r51/show_mem.c.v7.2: OK
.ufo/waves/round-51/contract.md: OK
.ufo/waves/round-51/controls/c1-controls.py: OK
.ufo/waves/round-51/controls/witness/conform.py: OK
.ufo/waves/round-51/controls/witness/mori-pin-check.py: OK
.ufo/waves/round-51/count-c1.py: OK
.ufo/waves/round-51/count-c2.py: OK
.ufo/waves/round-51/evidence/census-start.txt: OK
.ufo/waves/round-51/evidence/control-c1-always-env.txt: OK
.ufo/waves/round-51/evidence/control-c1-class-only.txt: OK
.ufo/waves/round-51/evidence/control-c1-conform-only.txt: OK
.ufo/waves/round-51/evidence/control-c1-do-nothing.txt: OK
.ufo/waves/round-51/evidence/control-c1-scratch-only.txt: OK
.ufo/waves/round-51/evidence/control-c1-witness.txt: OK
.ufo/waves/round-51/evidence/control-c2-do-nothing.txt: OK
.ufo/waves/round-51/evidence/selftest-c2.txt: OK
.ufo/waves/round-51/evidence/sweep-memavailable.txt: OK
exit=0
```

All 21 listed files (17 under `.ufo/waves/round-51/`, 5 copies) verify against the working tree: nothing frozen has
been edited since the freeze. Cross-check via git objects instead of the working tree:

```
$ git -C …/mori-shokunin show 87e0c374:….ufo/waves/round-51/count-c2.py | sha256sum
19553792d74d8f3ca9c09e6a018b9c66f61a58e8ad78e72b524a69ec892cfb26  -      # == freeze-sha256.txt entry for count-c2.py
```

Frozen-path drift between freeze and data:

```
$ git -C …/mori-shokunin diff --stat 4677910eae6df3dabd38fe9a0daf1945146a1110 87e0c374537557754bf71dd68036ded3ddc6699c -- .ufo/waves/round-51/count-c1.py .ufo/waves/round-51/count-c2.py .ufo/waves/round-51/contract.md .ufo/waves/round-51/controls
(no output)
exit=0
$ git -C …/mori-shokunin diff --name-status 4677910… 87e0c37… -- <same four paths> | wc -l
0
```

The diff is empty, as required. Both counters, the contract and `controls/` are byte-identical at the freeze commit
and at the data commit, so the C2 reading above was produced by the frozen counter scored against the landed data,
under an unchanged contract. `git rev-parse --verify <rev>^{commit}` resolves all three named revisions (rc 0 each).

## 7. Where the entailment votes would have to live

The counter reads votes from the git tree at R only (`git_lister` at `count-c2.py:259` → `git ls-tree --name-only
<rev> .ufo/waves/round-51/w1/`; `entail_votes` at `count-c2.py:120-129`), not from the working tree. At both the data
commit and the current lane tip that directory does not exist in the tree:

```
$ git -C …/mori-shokunin cat-file -e 87e0c374:.ufo/waves/round-51/w1 ; echo $?
fatal: path '.ufo/waves/round-51/w1' exists on disk, but not in '87e0c374537557754bf71dd68036ded3ddc6699c'
128
$ git -C …/mori-shokunin cat-file -e b504cb17:.ufo/waves/round-51/w1 ; echo $?
fatal: path '.ufo/waves/round-51/w1' exists on disk, but not in 'b504cb1701568a0038aab9d98ec13d28eff801da'
128
$ git -C …/mori-shokunin ls-tree -r --name-only 87e0c374 -- .ufo/waves/round-51/w1 | wc -l
0
$ git -C …/mori-shokunin ls-tree -r --name-only b504cb17 -- .ufo/waves/round-51/w1 | wc -l
0
$ git -C …/mori-shokunin log --oneline --all -- .ufo/waves/round-51/w1
(no output, rc 0)
```

So `entailed=0` at `87e0c374…` is a true reading of an empty vote set, not a counter fault. The consequence for the
round: the 21-row table can only reach `C2=met` at a commit that contains the w1 reports — the data commit named as
the landing cannot carry the votes, and the final C2 measurement therefore has to be taken at the successor commit
the L1 makes after integrating the seat reports. Reports currently sitting in the working tree
(`w1/Mo51CritEntail01.md`, `w1/Mo51CritEntail07.md`) contribute nothing until committed, and `w1` is not ignored
(`git check-ignore -v` on a report there exits 1; `.gitignore` lists only `.ufo/interactive-sessions/` and
`.ufo/worktrees/`), so a plain commit carries them.

## Findings

- **MED — `.ufo/waves/round-51/w1/` absent at every commit (data `87e0c374…` and lane tip `b504cb17`)**: the
  entailment arm of P-C2 is measured with `git ls-tree <rev> .ufo/waves/round-51/w1/`, and that tree entry does not
  exist at either revision (`git cat-file -e` rc 128, `ls-tree -r` 0 entries, `git log --all` for the path empty).
  C2 consequently reads `failed=entailment` at the named landing by construction. The measured R for the final C2
  reading must be the successor commit that contains the seat reports; `87e0c374…` cannot show `C2=met`. This is an
  ordering requirement, not a counter weakness — the counter behaves exactly as its docstring says.
- **LOW — `count-c2.py:259` `git_lister` is non-recursive**, so a report in a subdirectory of `w1/` would be
  invisible to the arm. Evidence: `git ls-tree --name-only HEAD .ufo/waves/round-51/evidence/` prints the bare
  directory name `selftests` next to the files, and `entail_votes` (`count-c2.py:124`) drops it because the name does
  not end `.md`. Flat reports only; a nested draft would silently not count.
- **LOW — `count-c2.py:38,124` excludes by filename prefix `MoriR51`**, so any non-L1 seat whose report filename
  happens to start with that string would be silently ignored (its votes and any overclaim in it). No such file exists
  in `w1/` now (working tree: `Mo51CritEntail01.md`, `Mo51CritEntail07.md`, `swarm-registry.json`); named as a
  limit, not a defect to fix mid-round.
- No other finding: the C2 data-commit line, the 34-check selftest, the entering-tip control, the 21-row hash
  receipt, the five copy pins, the frozen-file hashes and the freeze→data frozen-path diff all reproduce exactly, and
  my independent parse of the entry, SOURCES rows and the five copies found no structural or location defect in the
  21 rows.
