# Mo52ExecR51C2Rerun — round-51 C2 counter re-executed (round 52, wave w1)

Seat: re-execution of the round-51 C2 instrument (considerthese 2026-10-26 suggestion 3: "re-execute what
closures only evidence-verified"), C2 only. Read-only on the lane: no build/lint/test, no lane mutation, one
write (this file). Scratch `/fast/scratch/hyaku/mori-r52/Mo52ExecR51C2Rerun/` (TMPDIR set to its `tmp/`),
removed at the end. No tool installed or upgraded.

Instrument: `.ufo/waves/round-51/count-c2.py` (round-51 freeze `4677910e`, sha256
`19553792d74d8f3ca9c09e6a018b9c66f61a58e8ad78e72b524a69ec892cfb26`), read-only (`git show`, `git ls-tree`,
`git rev-parse`, one `open(..., "rb")` in `--selftest`; no write call anywhere — see "write surface" below).

Revisions:

| label | rev | commit subject |
|---|---|---|
| measured (receipt) | `70e68cdd28c44a95039b9175a947e15664618351` | round-51: wave w1 integration part 2 — all 68 reports and results, … |
| contract entering tip | `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d` | round-51 verifier spot-check (integrator, hyaku) |
| round-52 freeze | `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2` | round-52: freeze — contract, C1/C2 counters with selftests, … |
| round-52 data (assigned tip) | `8524904adb25e44f24d9f25aac7eae909625c18c` | round-52: data — C1 Axes cells lead with round 51, … |
| lane HEAD when I finished | `075436b1346ca659afb8be7a46f0e67e4170aa83` | round-52: wave w1 spec (68 seats, v2 validated), dispatch, receipts at data |

The lane advanced `8524904a` → `075436b1` while I was running; the assigned tip is measured below and the new
HEAD was re-read as well (it changes none of the instrument's read paths).

## 1. Commands, outputs, exits (literal)

Literal recorded command of the receipt, run from the lane root exactly as the receipt records it:

```
$ python3 .ufo/waves/round-51/count-c2.py 70e68cdd28c44a95039b9175a947e15664618351
C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=70e68cdd28c44a95039b9175a947e15664618351
exit=0
```

Selftest:

```
$ python3 .ufo/waves/round-51/count-c2.py --selftest
PASS honest_met
… 33 further PASS lines, all PASS …
C2_SELFTEST pass=34 fail=0
exit=0
```

At the assigned tip, and at the two intervening revs:

```
$ python3 .ufo/waves/round-51/count-c2.py 8524904adb25e44f24d9f25aac7eae909625c18c
C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c
exit=0

$ python3 .ufo/waves/round-51/count-c2.py 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d
C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d
exit=0

$ python3 .ufo/waves/round-51/count-c2.py d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2
C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2
exit=0

$ python3 .ufo/waves/round-51/count-c2.py 075436b1346ca659afb8be7a46f0e67e4170aa83
C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=075436b1346ca659afb8be7a46f0e67e4170aa83
exit=0
```

(For the two command forms that take `--repo`, the clone check in §4 used
`python3 <.ufo/waves/round-51/count-c2.py> <rev> --repo <scratch clone>`.)

## 2. Comparison with the receipts — agreement, no divergence

| run | line differs from receipt only in | exit | verdict |
|---|---|---|---|
| `70e68cdd` (literal replay) | nothing — byte-identical | 0 | receipt reproduced exactly |
| `--selftest` | nothing — byte-identical | 0 | receipt reproduced exactly (`pass=34 fail=0`) |
| `8524904a` (assigned tip) | `rev=` field only | 0 | every arm identical: claims 21, located 21, quote_missing 0, bad_rows 0, sources 5, source_rows ok, pins ok, provenance ok, entailed 21, dissent 0 |
| `4f266ef2`, `d3a8ea59`, `075436b1` (supplementary) | `rev=` field only | 0 | same, unchanged |

```
$ diff .ufo/waves/round-51/evidence/c2-at-landed.txt <literal replay capture>
(no output)  → IDENTICAL
$ diff .ufo/waves/round-51/evidence/selftest-c2.txt <selftest capture>
(no output)  → IDENTICAL
```

Byte-identity of the compared artefacts:

| file | sha256 |
|---|---|
| `.ufo/waves/round-51/evidence/c2-at-landed.txt` | `abeba7178091e21ae04802e5dd7182ecfb07503a2ba88a725b728f7d1c9b3a0c` |
| my literal replay capture | `abeba7178091e21ae04802e5dd7182ecfb07503a2ba88a725b728f7d1c9b3a0c` |
| `.ufo/waves/round-51/evidence/selftest-c2.txt` | `5963af652b826e1bf6808cd8cab232ccc234fe2df4d1ae7e9522e4ae82abfee3` |
| my selftest capture | `5963af652b826e1bf6808cd8cab232ccc234fe2df4d1ae7e9522e4ae82abfee3` |

The receipt records 3 lines (command, counter line, `exit=0`); the selftest receipt 36 lines (34 `PASS` +
summary + `exit=0`). Both are matched line-for-line, not just in the tally. The round-51 instrument has 34
selftest arms, not the 45 of the round-52 C2 counter — different instruments, compared only against their own
receipt.

Claim-text hashes also agree across the two ends of the window: `--hashes 70e68cdd` and `--hashes 8524904a`
produce 21 identical `row=/hash=/claim=` lines (`diff` empty, exit 0), so the tip's `entailed=21` is 21 votes on
the same claim texts the receipt scored, not on reworded cells.

## 3. Why the tip agrees — measured mechanism, not assumption

1. Five commits sit between `70e68cdd` and `8524904a` (`a5087527`, `8e3df7e5`, `4f266ef2`, `d3a8ea59`,
   `8524904a`). Per-commit check of the instrument's read paths (the r51 entry, `corpus/SOURCES.md`,
   `corpus/evidence/sources-r51/`, `.ufo/waves/round-51/w1/`, the counter itself): the only change in the whole
   range is `corpus/SOURCES.md` at `8524904a`, `5 ++++` insertions (`S497`–`S501`, round-52 overcommit rows).
2. Those insertions are append-only at line 273+ and use ids `S497`–`S501`; the r51 entry cites `S492`–`S496`
   (`source:` lines at the tip). `sources_row()` matches by exact `S<id>`, so there is no shadowing, and
   `git diff 70e68cdd 8524904a -- corpus/SOURCES.md` contains no `-` line (no row rewritten).
3. The counter is revision-addressed: `main` resolves `repo` from `__file__` and reads only `git show`/`ls-tree`
   at the requested rev. Working-tree bytes cannot affect a rev run except through the pinned-copy digests, and
   `git diff --stat 8524904a -- <read paths>` was empty (no working-tree drift on any of them).
4. The instrument's bytes never changed after the round-51 freeze: sha256 `19553792…` is identical in the
   working tree and at `70e68cdd`, `4f266ef2`, `d3a8ea59`, `8524904a`; `git log -- .ufo/waves/round-51/count-c2.py`
   lists one commit only (`4677910e` freeze).
5. The five copies the pin arm hashes are intact in the working tree (each equals the frozen digest in the
   `COPIES` table): `proc.rst.v7.2` `e760f716…`, `show_mem.c.v7.2` `dba76b26…`, `meminfo.c.v7.2` `d6c58074…`,
   `mm_inline.h.v7.2` `2d4accbb…`, `34e431b0.patch` `9f571a04…`.
6. Write surface: the only subprocess calls in the script are `git show`, `git ls-tree --name-only`,
   `git rev-parse --verify`; the only `open()` is `--selftest`'s `open(..., "rb")`. Nothing in the lane was
   created or modified by running it (`grep -nE 'open\(|os\.remove|shutil|write\(|subprocess\.run'` over the
   script returns only those sites plus the docstring lines).

## 4. Independence checks

- **Clone, not lane cwd.** `git clone -q --shared --no-checkout --no-hardlinks <lane> <scratch>/clone` (asserted
  `rev-parse --show-toplevel` equals the clone), then the same counter with `--repo <clone>`: identical lines at
  both `70e68cdd` and `8524904a`. The agreement is a property of the revision, not of the lane working tree.
- **Selftest sensitivity.** A fake lane in scratch (`<scratch>/fakelane/.ufo/waves/round-51/count-c2.py` plus the
  five copies, because `--selftest` derives `lane` from `__file__` and reads the working tree) reproduces
  `C2_SELFTEST pass=34 fail=0` / exit 0 with intact copies. Appending a single byte to
  `fakelane/corpus/evidence/sources-r51/show_mem.c.v7.2` flips it to `pass=31 fail=3`, exit 1; the three are
  exactly the checks that require `met` (`honest_met`, `indented_row_ok`,
  `entail_hash_whitespace_folded_met`), all through `pins=bad`. So a passing `--selftest` in the lane is itself
  evidence that the five working-tree copies match the frozen digests — consistent with the sha256 check in §3.5.

## 5. Divergence risks and named limits (observations; no counter change proposed)

1. **The re-run corroborates round-51's arm, which is weaker than round-52's.** The r51 arm accepts one voter
   (`.ufo/waves/round-51/count-c2.py:37` `ENTAIL_DIR`, `:38` `L1_PREFIX = "MoriR51"`, `:219` the `overclaim`
   test; there is no `REPLACE` handling and no author exclusion in the file at all). Measured at `8524904a` over
   the 68 `.md` files in `.ufo/waves/round-51/w1/`: 11 files carry votes, 47 vote lines in total (42 `entailed`,
   5 `overclaim`), over 26 distinct claim hashes of which 21 are the current rows; per row, 17 rows
   have 2 `entailed` voters and 4 rows have exactly 1 — `0a908e8eb4f3`, `d901a2d666fb`, `6c2327e19df1`,
   `7e14f1771092`. Under round-52's ≥2-distinct-voter arm, 4 of the 21 r51 rows would not hold. Nothing about
   the r51 verdict changes (its frozen arm is what it was); the limit is that re-running it cannot be quoted as
   evidence for the hardened arm.
2. **`dissent=0` at the tip does not mean "never contested".** The tip still carries 5 `overclaim` records, on 4
   claim hashes (`102feb3debfa`, `5d06a2ae70cf`, `a06f1037d952`, `ec0f6c97eeba`), none of which is among the 21
   current rows: they are votes on pre-replacement wording, retained because votes are never deleted. The
   instrument reads `dissent` only for hashes present in the table, so `dissent=0` is correct-by-arm. A reader
   who quotes `dissent=0` without that sentence overstates the review history of the current text.
3. **A historical vote directory stays readable and writable by later rounds.** `ENTAIL_DIR` is the literal
   `.ufo/waves/round-51/w1/`, so any later seat that wrote a report there could change a round-51 reading
   (round-52 votes go to `.ufo/waves/round-52/w1/`, so there is no interference today: `ls-tree` at `8524904a`
   for `.ufo/waves/round-52/w1/` lists 0 entries). This is the same class as round-51 closure defect 6, now on
   the vote side.
4. **Receipts are committed after the revision they measure.** `c2-at-landed.txt` and `selftest-c2.txt` do not
   exist at `70e68cdd`: `git diff --name-status 70e68cdd 8524904a -- .ufo/waves/round-51/evidence/` reports `A`
   for `c2-at-landed.txt`, `c1-at-landed.txt` and `census-end.txt` (added by `a5087527`); the counter selftest
   receipt came with the freeze `4677910e`. A future predicate of the form "the receipt exists at R" would
   therefore be false for every R that is the measured revision; the receipt must be fetched from a revision
   after R.
5. **Repo location is derived from the script path.** `main` computes `repo` from `__file__` four levels up, so a
   copy of the counter outside the lane silently targets the wrong repository unless `--repo` is passed. Both
   facts are why §4's clone check passed `--repo` explicitly.

## 6. What I did not check

- I did not re-run the round-51 **C1** counter (another seat's assignment) and did not score round-52's own
  counters or claims.
- I did not verify the 21 quotes against the upstream URLs (no network fetch); only against the committed copies,
  which is what the instrument does.
- I did not touch the host's `/proc/meminfo`, sysctls or any cgroup state; this seat made no host reads beyond
  none at all.

## Findings

1. **LOW** — `.ufo/waves/round-51/evidence/c2-at-landed.txt` (and `c1-at-landed.txt`, `census-end.txt`) exist
   only from `a5087527` onward, not at the measured rev `70e68cdd`; any predicate demanding a receipt at the
   measured revision is unsatisfiable (route: r53 counter design).
2. **LOW** — `.ufo/waves/round-51/count-c2.py:37` fixes the vote directory to `.ufo/waves/round-51/w1/`, so a
   later seat writing there would alter a historical reading (no such file today; route with item 1).
3. **LOW** — the r51 entailment arm accepts one voter and has no author exclusion; 4 of 21 rows
   (`0a908e8eb4f3`, `d901a2d666fb`, `6c2327e19df1`, `7e14f1771092`) would fail round-52's ≥2-voter arm, so the
   successful re-run must not be cited as support for the hardened arm.
4. **LOW** — `dissent=0` at `8524904a` coexists with 5 retained `overclaim` records on 4 non-current hashes;
   quoting `dissent=0` alone overstates the review history of the current text.
5. **INFO (no defect)** — receipt reproduction is exact: literal replay at `70e68cdd` and `--selftest` are
   byte-identical to their receipts (`abeba717…`, `5963af65…`), and the reading is unchanged at `4f266ef2`,
   `d3a8ea59`, `8524904a` and `075436b1`. No divergence to report.

Report: `.ufo/waves/round-52/w1/Mo52ExecR51C2Rerun.md`
