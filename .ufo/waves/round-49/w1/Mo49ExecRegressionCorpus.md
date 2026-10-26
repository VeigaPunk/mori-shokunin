# Mo49ExecRegressionCorpus — round 49 regression corpus for the pin reconciler (wave w1)

- Seat: `Mo49ExecRegressionCorpus` (executor, wave w1, leaf — no subagent dispatched, none needed)
- Lane: mori-shokunin (fleet & host observability; detection and report only)
- Machine: MACHINE_ID. Date: 2026-10-25.
- Lane tip at work: `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (freeze commit); entering tip
  `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` (the base revision of every artifact here).
- Skill: `/skill:godspeed` (`skill://godspeed` read).
- Assignment: from the frozen counter, dump every SKILL.md-level variant as a body plus a unified diff
  against the base, run it, list the files with sizes, verify each diff is non-empty and that the J/N
  diffs differ pairwise; document the layout at the top of this report.

Nothing was installed or upgraded (no `pacman`, no `uv`, no binary download — nothing was needed).
No lane tool under test was executed and no claim was scored; the frozen counters, controls, corpus,
`SKILL.md`, `SOURCES.md`, `tools/`, `LOG.md`, `SCORECARD.md`, `QUALITY.md` and the jj/git state of the
lane were not written. This seat's writes are exactly: this report and
`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecRegressionCorpus/`.

## Corpus layout (read this first)

Root: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecRegressionCorpus/corpus/`
(scratch, by lane rule: wave seats write only their own report plus `.scratch/r49-<seat>/`; the L1
decides whether to carry this corpus into the lane).

| file | content |
|---|---|
| `base-063be309.md` | the unedited base text: `git show b3e3453d:SKILL.md` (155,921 bytes, 979 lines) |
| `v-<index>-<sha8>.md` | one variant body: the base after that variant's function from `count-c1.py` ran on it |
| `v-<index>-<sha8>.diff` | unified diff of that body against the base, paths `--- a/SKILL.md` / `+++ b/SKILL.md`, 3 lines of context |
| `SHA256SUMS` | `sha256sum` manifest of the 47 artifacts above (`sha256sum -c --quiet SHA256SUMS` passes) |

- `index` is the variant's position in `count-c1.py`'s own `ORDER` list (`count-c1.py:212-213`), two
  digits: `00`-`22`. Indices `23` and `24` are the two fixture-built variants (N10, H5) and are absent
  for the reason in §4.
- `sha8` is the first 8 hex of `sha256(body)` — the same opaque handle style the counter uses
  (`count-c1.py:216-221`). **No file name contains a variant name**, so a mutation seat can hand a
  variant to the tool without the tool (or a filename-sniffing stub) being told what it is.
- The variant name for each index is in §3 of this report and nowhere in the corpus directory.

### How to apply one diff

```sh
D=$(mktemp -d)                                   # any copy dir, not the lane worktree
cp /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecRegressionCorpus/corpus/base-063be309.md "$D/SKILL.md"
cp /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecRegressionCorpus/corpus/v-12-d5f0f9da.diff "$D/"
(cd "$D" && patch -p1 < v-12-d5f0f9da.diff)      # rc 0, "patching file SKILL.md"
cmp "$D/SKILL.md" /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecRegressionCorpus/corpus/v-12-d5f0f9da.md
```

The `.md` file is the expected result of applying its `.diff` to the base; `cmp` is the fidelity check.
`patch` is GNU patch 2.8 on this host. The diffs apply with `-p1` because their paths are
`a/SKILL.md` / `b/SKILL.md`: the patched file must be named `SKILL.md` in the current directory.

### Replaying a corpus variant against a tool (same knobs the counter uses)

`count-c1.run_tool()` (`count-c1.py:224-245`) invokes the tool as

```
python3 -I -B <tool> --rev <R> --repo <lane> --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 [--skill <staged copy>]
```

with `TMPDIR` = the run's scratch and `PYTHONDONTWRITEBYTECODE=1`, and reads the **last**
`PIN_CHECK=(met|unmet)` line of the combined stdout+stderr, cross-checked against rc 0/1 (anything else,
or a rc/verdict mismatch, is `error`). A corpus replay is therefore:

```
TMPDIR=<scratch> python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
  --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 \
  --skill <dir>/SKILL.md
```

(`--skill` is the staged/patched copy; the counter passes it only when the job has one, i.e. for every
SKILL.md-level variant and for `real-opaque`, `count-c1.py:227-228` inside `run_tool`, path staged at `count-c1.py:256-262`.)

## 1. The script

`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecRegressionCorpus/dump-variants.py`
(9,368 bytes, `chmod +x`, `#!/usr/bin/env python3`, `sys.dont_write_bytecode = True`).

What it does:

1. loads the frozen counter with `importlib.util.spec_from_file_location` on
   `.ufo/waves/round-49/count-c1.py` (the counter itself imports the round-48 counter by path, so its
   `HERE`/`LANE` resolution is the real one, not a copy);
2. reads the base with `git -C <lane> show b3e3453d:SKILL.md` (read-only git; `REV` is overridable as
   `argv[1]`, default the entering tip);
3. applies **every** variant function it finds in the counter — `r48.VARIANTS` (J1-J8, H1-H4) followed by
   `NEW_VARIANTS` (N1-N9, H6, H7), i.e. the same list `plan()` iterates (`count-c1.py:264`) — to that text;
4. writes `v-<index>-<sha8>.md` and `v-<index>-<sha8>.diff`, the diff produced by `difflib.unified_diff`
   over `splitlines(keepends=True)` with `a/SKILL.md` / `b/SKILL.md` headers and `n=3`;
5. verifies (a) every diff non-empty and correctly headed, (b) no body equals the base, (c) the 17 J/N
   diffs are pairwise distinct, (d) no two bodies are byte-identical, (e) every diff applies with
   `patch -p1 --dry-run` **and** a real apply reproduces the body byte-for-byte, and (f) every dumped body
   is byte-identical to the copy the frozen counter's own `plan_text_only()` stages for the tool;
6. prints the mapping table (index, variant, expected verdict, sha8, body bytes, diff lines, file);
7. exits 0 only if every check passed. A variant anchor absent at the chosen revision is reported as a
   `FAIL <variant>: variant function raised Anchor: …` line and a non-zero exit — never silently skipped.

## 2. Run and observed output

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecRegressionCorpus \
  PYTHONDONTWRITEBYTECODE=1 python3 .scratch/r49-Mo49ExecRegressionCorpus/dump-variants.py \
  b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
stagecheck: 24 staged bodies compared against count-c1.plan_text_only(); real-opaque copy not written by plan_text_only (path appended only)
base=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 sha8=063be309 bytes=155921 lines=979
variants_dumped=23 failures=0 patch_ok=23/23

index  variant  expect  sha8      bytes  diff_lines  file
    0  J1       unmet   4e787a19  155918          16  v-00-4e787a19.diff
    1  J2       unmet   365e93c6  156118          10  v-01-365e93c6.diff
    2  J3       unmet   0f4a856c  156116          10  v-02-0f4a856c.diff
    3  J4       unmet   3a459dcd  156214          10  v-03-3a459dcd.diff
    4  J5       unmet   97312d94  155935          15  v-04-97312d94.diff
    5  J6       unmet   666eef87  155921          12  v-05-666eef87.diff
    6  J7       unmet   61335b6f  155921          11  v-06-61335b6f.diff
    7  J8       unmet   2e6b38f1  155921          11  v-07-2e6b38f1.diff
    8  H1       met     10418425  155976           8  v-08-10418425.diff
    9  H2       met     487b11e0  155922          11  v-09-487b11e0.diff
   10  H3       met     f6d76050  155921          11  v-10-f6d76050.diff
   11  H4       met     1e1d311c  156138          10  v-11-1e1d311c.diff
   12  N1       unmet   d5f0f9da  156073           8  v-12-d5f0f9da.diff
   13  N2       unmet   163bc29c  156184          10  v-13-163bc29c.diff
   14  N3       unmet   baeb0a64  156072          10  v-14-baeb0a64.diff
   15  N4       unmet   0aabc494  156068           8  v-15-0aabc494.diff
   16  N5       unmet   a7deda5f  156378          10  v-16-a7deda5f.diff
   17  N6       unmet  963ccc97  156476          12  v-17-963ccc97.diff
   18  N7       unmet   d8ef1995  156225          10  v-18-d8ef1995.diff
   19  N8       unmet   c8d64139  155925          11  v-19-c8d64139.diff
   20  N9       unmet  5b755aed  156270          10  v-20-5b755aed.diff
   21  H6       met     194c8262  156033          12  v-21-194c8262.diff
   22  H7       met     5e22774a  156007          12  v-22-5e22774a.diff

no SKILL.md diff (fixture-built or real-run entries): N10,H5,real,real-opaque
EXIT=0
```

Run three times (default revision; then with the revision passed explicitly; then again after check 5 was
added): identical `sha8` values every time — the corpus is deterministic. The last run's full stdout is
saved at `.scratch/r49-Mo49ExecRegressionCorpus/dump-run.txt`.

## 3. Files with sizes (23 diffs + 23 bodies + base + manifest)

Bodies are ~152 KB each because each is a full SKILL.md (~156 KB); the diffs are the small artifacts.
`±` counts *added* / *removed* lines including blank ones; every diff is a single hunk.

| index | variant | expected | sha8 | body bytes | diff bytes | hunks | +lines | -lines |
|---|---|---|---|---|---|---|---|---|
| 00 | J1 | unmet | `4e787a19` | 155918 | 4290 | 1 | 3 | 3 |
| 01 | J2 | unmet | `365e93c6` | 156118 | 2293 | 1 | 1 | 0 |
| 02 | J3 | unmet | `0f4a856c` | 156116 | 2291 | 1 | 1 | 0 |
| 03 | J4 | unmet | `3a459dcd` | 156214 | 2389 | 1 | 1 | 0 |
| 04 | J5 | unmet | `97312d94` | 155935 | 4109 | 1 | 4 | 2 |
| 05 | J6 | unmet | `666eef87` | 155921 | 3470 | 1 | 2 | 1 |
| 06 | J7 | unmet | `61335b6f` | 155921 | 7863 | 1 | 1 | 1 |
| 07 | J8 | unmet | `2e6b38f1` | 155921 | 11777 | 1 | 1 | 1 |
| 08 | H1 | met | `10418425` | 155976 | 517 | 1 | 2 | 0 |
| 09 | H2 | met | `487b11e0` | 155922 | 3470 | 1 | 1 | 1 |
| 10 | H3 | met | `f6d76050` | 155921 | 2281 | 1 | 1 | 1 |
| 11 | H4 | met | `1e1d311c` | 156138 | 2313 | 1 | 1 | 0 |
| 12 | N1 | unmet | `d5f0f9da` | 156073 | 614 | 1 | 2 | 0 |
| 13 | N2 | unmet | `163bc29c` | 156184 | 727 | 1 | 4 | 0 |
| 14 | N3 | unmet | `baeb0a64` | 156072 | 615 | 1 | 4 | 0 |
| 15 | N4 | unmet | `0aabc494` | 156068 | 609 | 1 | 2 | 0 |
| 16 | N5 | unmet | `a7deda5f` | 156378 | 921 | 1 | 4 | 0 |
| 17 | N6 | unmet | `963ccc97` | 156476 | 1021 | 1 | 6 | 0 |
| 18 | N7 | unmet | `d8ef1995` | 156225 | 768 | 1 | 4 | 0 |
| 19 | N8 | unmet | `c8d64139` | 155925 | 3473 | 1 | 1 | 1 |
| 20 | N9 | unmet | `5b755aed` | 156270 | 813 | 1 | 4 | 0 |
| 21 | H6 | met | `194c8262` | 156033 | 578 | 1 | 6 | 0 |
| 22 | H7 | met | `5e22774a` | 156007 | 552 | 1 | 6 | 0 |

The `expected` column is copied from the counter's own `VARIANTS`/`NEW_VARIANTS` tables
(`round-48/count-c1.py:186-190`, `count-c1.py:206-209`); this seat asserts no verdict — wave 2 measures.

Directory inventory (exact):

```
$ ls -l corpus | wc -l   → 49 lines (48 entries + "total")
$ ls corpus/v-*.diff | wc -l  → 23
$ ls corpus/v-*.md   | wc -l  → 23
$ ls corpus/base-*.md | wc -l → 1    (base-063be309.md, 155921 bytes)
$ sha256sum corpus/base-*.md corpus/v-*.md corpus/v-*.diff > corpus/SHA256SUMS   (47 lines, 4276 bytes)
$ sha256sum -c --quiet corpus/SHA256SUMS → no output, EXIT=0
$ find . -type f | wc -l  → 50   (48 corpus files + dump-variants.py + dump-run.txt)
$ du -sb .                → 3819137 bytes
```

Full per-file sizes (bytes) as `ls -l` printed them: diffs 517-11777; bodies 155918-156476; base 155921;
`SHA256SUMS` 4276. No file in the corpus dir carries a variant name.

## 4. What is *not* in the corpus, and why

`count-c1.py`'s `ORDER` has 26 entries (`count-c1.py:212-213`); 23 of them are SKILL.md-level variant
functions and are all dumped. The other three:

- **N10 and H5** are not functions over SKILL.md. They are built by `fixture_variant()`
  (`count-c1.py:174-203`): a throwaway git repository whose `tools/probe.py` gains a third selftest arm,
  with the fixture registry pin left at 2 (N10) or moved to 3 (H5). They are **repository-level** edits,
  so a `patch -p1` diff against the lane's `SKILL.md` would be the wrong artifact (applying it would dress
  the mori registry in fixture rows). A seat that needs them calls
  `count-c1.fixture_variant(dest, move_pin)` directly — it returns `(dir, new_commit, baseline_commit)`
  and refuses to run if the directory is not its own repository toplevel.
- **`real` and `real-opaque`** are the unedited SKILL.md read twice (by revision and through an
  opaque-named copy), not variants; the base file `base-063be309.md` already is their text.

Consequence for wave 2: the corpus covers **17 of 18 junk** classes and **6 of 7 honest** classes
(J8 junk + H4 honest are present; the missing pair is exactly N10/H5). Any count of "variants covered by
the corpus" must read 23, not 26.

## 5. Checks and their observed results

| check | command | observed |
|---|---|---|
| dumped all 23 SKILL.md variant functions | §2 run | `variants_dumped=23 failures=0`, `EXIT=0` |
| every diff non-empty and headed `--- a/SKILL.md` / `+++ b/SKILL.md` | in-script check 1 | 0 failures (`failures=0`) |
| no body equals the base | in-script check 1 | 0 failures |
| J/N diffs pairwise distinct | in-script check 2 (136 pairs) | 0 failures |
| no two bodies identical | in-script check 2 | 0 failures |
| each diff applies with `patch -p1 --dry-run` | in-script check 3 | `patch_ok=23/23` |
| each real apply reproduces its body | in-script check 4 (`patch`, then byte compare) | 0 failures |
| each body equals the counter's staged copy | in-script check 5 (`count-c1.plan_text_only()` on the base, then byte compare of all 23 bodies) | `stagecheck: 24 staged bodies compared against count-c1.plan_text_only()`, 0 failures |
| independent recount of distinctness | `python3` over `corpus/v-*.diff` (inline, see below) | `files: diff=23 body=23 base=1`; `jn_diffs=17 pairs=136 collisions=0`; `bodies=23 distinct=23`; `diffs=23 distinct=23`; `total_bytes=3647486` (that sum covers the 23 diffs + 23 bodies; the base is 155921 more) |
| manifest integrity | `sha256sum -c --quiet corpus/SHA256SUMS` | exit 0, no output |
| frozen bytes untouched by this seat | `sha256sum -c .ufo/waves/round-49/evidence/freeze-sha256.txt` | `ok=31 failed=0` |

The independent recount selected the J/N family by index (`00`-`07` for J1-J8, `12`-`20` for N1-N9 = 17
files) and compared `sha256` of the diff bytes over all 136 pairs. All 23 diffs are distinct, not only
the J/N ones.

Sanity spot-checks of diff shape (read from the corpus, not from the counter's prose): `v-19-c8d64139.diff`
(index 19, N8) is a one-line replacement inside the existing reconciler row — one `-` and one `+` — as N8
is specified to re-point that row; `v-12-d5f0f9da.diff` (index 12, N1) is a pure append of a blank line and
the HTML-commented gate row. The three large diffs (`v-06`, `v-07`, `v-05`/`v-09`) are large because the
lines they edit are single very wide table rows (max line length 1543 / 1990 / 1270-1271 bytes), not because
they touch many rows: each is still 1 hunk with 1-2 changed lines.

Environment used: Python 3.14.8, GNU patch 2.8, `git -C <lane> rev-parse HEAD` = `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`,
`git show b3e3453d:SKILL.md | wc -c` = 155921. `TMPDIR` was the seat scratch for every run; no `/tmp` use
by lane tooling.

## 6. Regenerating against the landed tip

The corpus base is the **entering** tip, because that is the revision the assignment named and the text the
counter's variants were frozen against. Once wave 1 lands tool or registry changes, `SKILL.md` rows move and
these diffs may no longer apply (context mismatch) — the counter re-applies its functions to *R*'s text, so
the corpus must be regenerated the same way:

```
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecRegressionCorpus \
PYTHONDONTWRITEBYTECODE=1 python3 \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecRegressionCorpus/dump-variants.py <landed-tip>
```

Two variants depend on literal cells of SKILL.md that the landed tip must keep for the counter itself to
work: J7 replaces `(743 lines)` once (`round-48/count-c1.py:141-144`) and J8 replaces `37fd7c24ff52…`
(`round-48/count-c1.py:147-150`). If a landed edit rewrote those cells the script exits non-zero with a
`variant function raised Anchor: …` line and the table names the variant — that failure is itself the
signal that the counter's anchors moved, and it is reported, not swallowed.

## 7. Write scope, hygiene, and what I did not do

- Writes: this report; `.scratch/r49-Mo49ExecRegressionCorpus/` (script, `dump-run.txt`, `corpus/` with 48
  files, 3.82 MB total). The script's `patchcheck/` and `stagecheck/` temp dirs are removed after their
  checks (`ls -d patchcheck stagecheck` → both absent); no fixture repository was created (N10/H5 were not
  built), so no throwaway git repo exists anywhere.
- No write to any lane file, the frozen round-49 files, the fleet repo, sibling lanes, `jj` state or the git
  index. No `git add/commit/stash/checkout/reset/pull/push`, no mutating `jj` command; the only git calls
  were `show` and `rev-parse`. `/home/vgpnk/Projects/shokuknow/{merge/mori,}` was not read or run this seat.
- The pre-existing `.ufo/waves/round-49/__pycache__/` (`count-c1.cpython-314.pyc` 37,519 B, mtime
  21:24:26; `count-c2.cpython-314.pyc` 27,022 B, mtime 21:43:07) was **not** touched by this seat: the
  script sets `sys.dont_write_bytecode = True` and the runs carried `PYTHONDONTWRITEBYTECODE=1`; both mtimes
  are unchanged after the runs (checked again after the final run).
- Host reads: none needed for this assignment (no journal/`systemctl`/`sudo` call).
- `patch` and `python3` were already present; nothing installed, so there is no tool/version/channel record
  to make.

## Limits

- The corpus is a **replay aid**, not a scorer: it carries the counter's own expected verdicts but proves
  nothing about any tool. Only `count-c1.py` scores, and only at the landed tip (contract §C1).
- Byte fidelity of the bodies against the counter's staging is **measured**, not argued: check 5 calls the
  frozen `count-c1.plan_text_only()` on the same base, which writes `s-<hash>.md` copies exactly as `plan()`
  does (`count-c1.py:248-262`, `434-441`), and compares all 23 against the corpus — 0 differences. It covers
  the 23 SKILL.md variants only; N10/H5 staging (`fixture_variant()`) was not exercised by this seat.
  `plan_text_only()` appends a `real-opaque` path without writing the file (`count-c1.py:445-446`), so that
  one copy could not be compared — see finding 6. No tool was run, so no verdict was measured.
- The corpus lives in `.scratch`, which the round-48 closure routed for cleanup at round end; if wave 2 is to
  use it, the L1 must regenerate it (one command, §6) or carry it into the lane.
- Coverage is 23 of 26 `ORDER` entries by construction (§4); N10/H5 are reproducible only through
  `fixture_variant()`.

## Findings

1. **MED** — the corpus cannot represent N10 and H5, the two fixture-built variants, because they are
   repository-level edits (`fixture_variant()` writes `tools/probe.py` plus a fixture `SKILL.md`), not
   SKILL.md functions. A wave-2 seat replaying only
   `.scratch/r49-Mo49ExecRegressionCorpus/corpus/v-*.diff` therefore covers 17 of 18 junk classes and 6 of 7
   honest classes; the two missing ones are exactly the pair that moves a second tracked file, and they are
   the pair the contract routes as the fixture-built honest/junk control. Concerns
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecRegressionCorpus/corpus/` (§4 of this
   report).
2. **LOW** — the corpus base is pinned to `b3e3453d`, the entering tip; after wave 1 lands, the diffs'
   context may no longer match the moved `SKILL.md` registry rows, and only the regeneration path
   (`dump-variants.py <landed-tip>`) keeps the corpus usable. Concerns
   `.scratch/r49-Mo49ExecRegressionCorpus/dump-variants.py:37` (the `REV` default) and §6.
3. **LOW** — the index→variant mapping exists only in this report and in `count-c1.py`'s `ORDER`; the corpus
   directory deliberately reveals nothing. A wave-2 seat that receives the corpus without this report cannot
   tell junk from honest, and would have to recompute the mapping from `count-c1.py` (or re-derive bodies).
   Concerns `corpus/` file naming vs `count-c1.py:212-213`.
4. **LOW** — J7 and J8 (§6) bind variant application to two literal cells of `SKILL.md` (`(743 lines)` and
   `37fd7c24ff52…`); a landed edit to either cell makes the corpus and the counter's own `plan()` fail at the
   same anchor, so the two move together — but a seat regenerating the corpus against a landed tip that still
   contains them should not read the successful regeneration as evidence that the counter passes. Concerns
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c1.py:141-150`.
5. **LOW** — `.ufo/waves/round-49/__pycache__/` holds `count-c1.cpython-314.pyc` and `count-c2.cpython-314.pyc`
   that are not listed in `evidence/freeze-sha256.txt` and were created before this seat's runs (mtimes
   21:24:26 and 21:43:07 at freeze+work, vs this seat's runs after 21:50). The frozen bytes themselves verify
   (`sha256sum -c` → `ok=31 failed=0`), so this is untracked byproduct residue only; unlike round 48's
   `.scratch` residue it needs no reclamation decision beyond deleting the directory. Concerns
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-49/__pycache__/`.
6. **LOW** — `count-c1.plan_text_only()` appends a `real-opaque` job whose staged path is never written: the
   loop's `with open(...)` runs only for the 23 variant functions, and the `real-opaque` append at
   `count-c1.py:445-446` reuses `tag = opaque(rev, text)` without creating `s-<tag>.md`. The full `plan()`
   does stage that copy (`count-c1.py:266` calls `stage()`), and the counter's selftest uses a fake runner
   that never opens the path, so nothing observed today breaks — but any arm that reads `real-opaque`'s
   staged file, or a future `plan_text_only`-based measurement, would score `error` instead of `met`.
   Observed by this seat's check 5: `stagecheck: … real-opaque copy not written by plan_text_only`.
   Concerns `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-49/count-c1.py:445-446`.
