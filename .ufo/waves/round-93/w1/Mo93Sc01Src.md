# Mo93Sc01Src — round-93 w1 frontier sources S622 / S623 (scout)

Seat: Mo93Sc01Src (scout). Lane repo: /home/vgpnk/Projects/shokunin/mori-shokunin.
Patch base: 6d82b8d7ef6d94a5527737f9242cdf04ad018da7. Access date: 2026-11-05 (UTC).
Scratch clone: /fast/scratch/hyaku/mori-r93/Mo93Sc01Src/clone (git clone --shared --no-checkout,
checkout -B seat 6d82b8d7). No lane file was mutated; no git commit, push, or mutating git/jj
command was run in the lane. The fetched copies live only in the scratch dir and were not
committed or copied into the lane.

## Result

| Item | Status |
|---|---|
| S622 — git-log(1) documentation | opened: https://git-scm.com/docs/git-log (HTTP 200, 375834 bytes, sha256 f206647f…) |
| S623 — Python command line and environment | opened: https://docs.python.org/3/using/cmdline.html (HTTP 200, 171073 bytes, sha256 90ac3b25…) |
| Rows drafted | 2 (S622, S623), 11 cells each, NF=13 on the leading-pipe form |
| Patch | `.ufo/waves/round-93/w1/patches/Mo93Sc01Src.patch` (4306 bytes), `git diff 6d82b8d7` of the scratch clone; `git apply --check` rc 0 at 6d82b8d7 |
| Frozen census validate on the patched tree | exit 0, zero E-codes; one W04 warning (see Limits) |

Both sources opened on the first attempt; no source failed to open, so both rows are drafted.

## Source A (S622) — git-log(1), official

- URL: https://git-scm.com/docs/git-log — HTTP 200, final URL unchanged (no redirect), 375834 bytes.
- sha256 of the fetched bytes: `f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b`
- Two independent fetches are byte-identical (`cmp` rc 0): `f206647f…` both times.
- Version carried by the anchor: the page states **"git-log last updated in 2.56.0"** (Latest
  version panel), i.e. the docs revision the bytes are read at.

Located quotes (tag-stripped copy of the fetched bytes; line numbers are lines of that
stripped copy, which is a 1:1 line-for-line tag strip of the fetched HTML):

1. Section **DIFF FORMATTING**, option `--diff-filter=[(A|C|D|M|R|T|U|X|B)...[*]]`,
   stripped lines 6730-6744; the quoted sentence is at lines 6732-6734:
   > "Select only files that are Added (A), Copied (C), Deleted (D), Modified (M), Renamed (R), have their type"
   (18 words. The `A` filter is what selects added paths.)
2. Section **PRETTY FORMATS**, subsection "Placeholders that expand to information extracted
   from the commit", `%h` placeholder, stripped lines 5493-5504; the quoted words are at
   line 5504:
   > "abbreviated commit hash"
   (3 words.)

The `--format=<format>` option itself is in the **OPTIONS → Commit Formatting** subsection,
stripped lines 4915-4926 (it is the option that carries the `%h` placeholder).

Uniqueness check (on the whitespace-flattened tag-stripped text of the fetched bytes):
`grep -c -F 'Select only files that are Added (A), Copied (C),'` → **1**;
`grep -c -F 'abbreviated commit hash'` → **1**.

Cross-check against upstream source text (not the cited source, used only to confirm the
section attribution is real and not a rendering artefact): git's own
`Documentation/diff-options.adoc` at tag v2.51.1 states the same `--diff-filter` sentence at
its lines 640-650, and `Documentation/git-log.adoc` at v2.51.1 includes
`diff-options.adoc` at its line 137 under its `DIFF FORMATTING` heading — the same section
the rendered page shows. Fetched to scratch only, HTTP 200; not a cited row.

## Source B (S623) — Python command line and environment, official

- URL: https://docs.python.org/3/using/cmdline.html — HTTP 200, final URL unchanged, 171073 bytes.
- sha256 of the fetched bytes: `90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0`
- Two independent fetches are byte-identical (`cmp` rc 0): `90ac3b25…` both times.
- Version carried by the anchor: the page is **Python 3.15.2 documentation** (`/3/` currently
  serves 3.15.2).

Located quote (tag-stripped copy of the fetched bytes, line numbers = lines of that copy):

Section **1.1.3. Miscellaneous options**, option `-I`, stripped lines 527-535:
> "Run Python in isolated mode. This also implies -E, -P and -s options." and
> "All PYTHON* environment variables are ignored, too."

(13 words + 7 words; the second sentence continues the same `-I` entry, stripped lines 531-532.)

Uniqueness check: `grep -c -F 'Run Python in isolated mode.'` → **1**;
`grep -c -F 'All PYTHON* environment variables are ignored, too.'` → **1**.

Section attribution was resolved from the rendered document's own heading stack, not assumed:
walking the `<h1>…<h6>` sequence up to the `-I` anchor id (`cmdoption-I`) gives
`1. Command line and environment → 1.1. Command line → 1.1.3. Miscellaneous options`.

## Rows drafted (verbatim, as they appear in the patch)

File: `.ufo/waves/round-93/w1/patches/Mo93Sc01Src.patch` (2 added lines in
`corpus/SOURCES.md`, appended after the S621 row inside the `## Registry` section).

Row S622:

| S622 | git-log(1) — https://git-scm.com/docs/git-log | docs | A | the --diff-filter status filter (the A filter that selects added paths) and the --format=<format> option with its %h abbreviated-hash placeholder, as used to derive a file's admission commit | OPTIONS, Commit Formatting subsection, --format=<format> option, tag-stripped lines 4915-4926 of the pinned copy; DIFF FORMATTING section, --diff-filter option, tag-stripped lines 6730-6744; PRETTY FORMATS section, "Placeholders that expand to information extracted from the commit", %h placeholder, tag-stripped lines 5493-5504; git-log documentation last updated in 2.56.0, page fetched 2026-11-05, HTTP 200, 375834 bytes, sha256 f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b; quotes: "Select only files that are Added (A), Copied (C), Deleted (D), Modified (M), Renamed (R), have their type" and "abbreviated commit hash" | The A filter selects only added paths and %h prints the abbreviated commit hash, so the commit that added a path is named by an abbreviated hash rather than a full object name. | mined | 2026-11-05 | on-release | corpus/lessons/round-93.md |

Row S623:

| S623 | Python command line and environment — https://docs.python.org/3/using/cmdline.html | docs | A | the -I (isolated mode) interpreter option, as used to run the lane's counters hermetically | section 1.1.3 Miscellaneous options, -I option, tag-stripped lines 527-535 of the pinned copy; Python 3.15.2 documentation, page fetched 2026-11-05, HTTP 200, 171073 bytes, sha256 90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0; quotes: "Run Python in isolated mode. This also implies -E, -P and -s options." and "All PYTHON* environment variables are ignored, too." | Under -I the interpreter ignores PYTHON* environment variables and leaves the script directory and the user site-packages off sys.path, so a counter run under python3 -I is not steered by the caller's environment. | mined | 2026-11-05 | on-release | corpus/lessons/round-93.md |

### Cell-by-cell value check against the seat spec

| Cell | S622 | S623 | Spec |
|---|---|---|---|
| id | S622 | S623 | next unused ids (S621 is the highest in the registry) |
| kind | docs | docs | docs |
| tier | A | A | A |
| status | mined | mined | mined |
| opened | 2026-11-05 | 2026-11-05 | 2026-11-05 |
| recheck | on-release | on-release | on-release |
| used-by | corpus/lessons/round-93.md | corpus/lessons/round-93.md | corpus/lessons/round-93.md for both |
| anchor | carries revision (git-log docs last updated in 2.56.0) + located sections (OPTIONS/Commit Formatting, DIFF FORMATTING, PRETTY FORMATS) | carries version (Python 3.15.2 documentation) + located section (1.1.3 Miscellaneous options) | revision/version + located section |
| source / scope / teaches | as drafted | as drafted | title — canonical URL |

No literal pipe appears inside any cell (checked by the NF=13 test below and by a per-character
pipe count: 13 pipe characters per row = 1 leading + 11 separators + 1 trailing).

## Checks run

1. **NF=13 on the leading-pipe form**, both new rows:
   `awk -F'|' '/^\|[[:space:]]*S62[23][[:space:]]*\|/ {print NR": NF="NF" id="substr($2,1,6)}' corpus/SOURCES.md`
   → `403: NF=13 id= S622` and `404: NF=13 id= S623`.
2. **Whole-registry NF check** (no pre-existing row broken):
   `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {print "BAD "NR}' corpus/SOURCES.md`
   → no output (every registry row is NF=13).
3. **Frozen registry validator** (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`,
   the same script the frozen counters invoke), on the patched scratch tree:
   `bash scripts/sources-census.sh validate --file corpus/SOURCES.md` → **exit 0, zero E-codes**.
   The only finding naming either new row is the warning
   `file W04 S622 duplicate url git-scm.com/docs/git-log across scopes` (see Limits).
4. **Patch reproducibility**: `git -C <scratch clone> diff 6d82b8d7 > …/patches/Mo93Sc01Src.patch`;
   then, on a fresh checkout of 6d82b8d7, `git apply --check` → rc 0 and `git apply` → rc 0,
   `git diff --stat` → `corpus/SOURCES.md | 2 ++`.
5. **Byte identity of both fetches**: second `curl -sSL` of each URL; `cmp` rc 0 for both
   (sha256 unchanged).
6. **Quote uniqueness**: `grep -c -F` on the whitespace-flattened tag-stripped bytes → 1 for
   each of the four quoted fragments.

## Limits, dependencies and open items for the L1

1. **The rows' `used-by` creates a landing-order dependency (E11).** With the two rows added
   but `corpus/lessons/round-93.md` not yet on disk, the frozen validator reports
   `file E11 S622 missing used-by corpus/lessons/round-93.md` (same for S623) and **exits 1**.
   Verified directly in the scratch clone: with a placeholder `corpus/lessons/round-93.md`
   present the same tree validates with exit 0; with it absent the same tree exits 1.
   The lesson draft (seat Mo93S01Lesson) places `## Mistakes` and `## Gate` in
   `corpus/lessons/round-93.md`, so the L1 must land that file **in the same commit** as these
   two rows, or both frozen counters' `census=ok` conjunct fails at the landing revision.
   This is the same shape as the round-91 landing, where `corpus/SOURCES.md` (S617/S618),
   `corpus/knowledge/calibration-arming-r91.md` and `corpus/lessons/round-91.md` landed together
   (commit bee9f21e).
2. **W04 on S622's URL.** `https://git-scm.com/docs/git-log` is already carried by **S059**
   (tier C, rejected, scope = porcelain log ordering for the C2 freeze-order verdict). S622
   carries a different scope (the admission-commit derivation), so the validator's E04
   (same URL *and* same scope) does not fire; only the W04 cross-scope warning fires. W04 does
   not affect the exit code (verified: exit 0). If the L1 prefers zero new warnings, S622's
   source cell could name the versioned page `https://git-scm.com/docs/git-log/2.56.0`
   instead — but that URL was **not** fetched or verified by this seat, so it is not proposed
   as-is.
3. **S622's `teaches` cell is narrower than the C1 claim's full derivation.** The cited page
   grounds two facts: (a) the `A` filter of `--diff-filter` selects added paths, and (b) `%h`
   is the abbreviated commit hash. It does **not** state that the abbreviated hash is 7
   characters — that is `core.abbrev`'s default, which this page does not mention
   (`grep -c 'core\.abbrev'` on the fetched bytes → 0). The counter's `ac[:7]` prefix test is
   therefore a lane convention this row does not source. The row's scope says "as used to
   derive a file's admission commit", not "as the source of the 7-character length".
4. **S623's anchor carries the version, not a per-release pin.** `https://docs.python.org/3/`
   is a rolling alias; the bytes read on 2026-11-05 are Python 3.15.2. The anchor records
   "Python 3.15.2 documentation" plus the sha256 and byte count of those bytes, which is what
   makes the row re-checkable, but the URL itself will serve different bytes after the next
   3.x release — hence `recheck on-release` rather than a fixed date.
5. **Both rows are `mined`, so they assert a citation that does not exist yet.** `used-by`
   names `corpus/lessons/round-93.md`, which the lesson seat drafts and the L1 lands; the
   citation is real only after that landing. The lesson draft's `## Gate` scaffold already
   reserves S622/S623 rows for the L1 to fill from this report (its line 94 and 95), so the
   gate table and these two rows should be reconciled by the L1 at integration.
6. **Fetched copies are scratch-only.** They were never written into the lane, and the scratch
   dir was deleted before this report was yielded. Only the two-row patch and this report
   persist as artifacts.
7. **Not run by this seat, reported as unrun:** `count-c1.py` and `count-c2.py` at the round-93
   landing (the landing revision does not exist yet — both counters must be run by the L1 at
   integration); `controls-r93.sh` (it writes fixtures and is the L1's rerun); the
   `sources-census.sh census` / `overdue` / `shared` modes (only `validate` bears on the frozen
   `census=ok` conjunct and was run).

## Tooling

No installs or upgrades. Used pre-existing `curl`, `git`, `awk`, `grep`, `cmp`, `sha256sum`,
`python3` (standard library only). `pacman` was not run. Nothing was created, modified or
deleted under `~/.local/bin` or any other PATH directory. No fleet-root tracked file
(`LOG.md`, `SCORECARD.md`, `MANIFEST.json`, …) was touched; the only lane writes are this
report and the patch file, both under `.ufo/waves/round-93/w1/`.

Report: .ufo/waves/round-93/w1/Mo93Sc01Src.md
