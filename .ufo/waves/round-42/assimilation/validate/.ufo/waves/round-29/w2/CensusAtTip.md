# CensusAtTip — sources-census at lane tip 8809a3f, S153-S155 contract check

Seat: MoriR29.CensusAtTip (leaf). Lane tip read: 8809a3f (branch master). Read-only git only; no lane writes
except this file; scratch under /fast/scratch/hyaku/mori-r29/w2/CensusAtTip/.

## 1. Validator run — full output and exit code

Command (exact):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Output, verbatim (stdout, in order):

```
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

**Exit code: 0** (`echo "EXIT=$?"` printed `EXIT=0`). No E01-E12 and no W01-W03 lines; the ten W04 are warnings
and the script documents that warnings do not change status (`scripts/sources-census.sh:12-13`).

## 2. W04 count and new-since-round-start

- W04 lines at tip: **10** (`awk -F'\t' '$2=="W04"{n++}END{print n}'` on the run above printed `W04_count=10`).
- Baseline `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-29/evidence/census-start.txt:1-13`,
  stamped `2026-10-22T19:50:48Z`, ends `exit: 0`, and holds the same ten W04 rows.
- Differential check: I stripped the baseline's timestamp line and its `exit: ` trailer and diffed the remainder
  against a fresh run; `diff` printed **IDENTICAL**.
- **New W04 since round start: none (0).** Ids at tip, all pre-existing: S035, S037, S073, S074, S075, S076,
  S147, S148, S149, S150.
- Confound ruled out: the validator itself did not change between baseline and tip — `git log -1` for
  `scripts/sources-census.sh` in the fleet repo is 6a1dd8c (older), its mtime is 2026-10-19 21:22:45, and
  `git diff --stat -- scripts/sources-census.sh` at the fleet root is empty. So the identity is a real
  no-change, not a tool drift.

Census context (`sources-census.sh census --root /home/vgpnk/Projects/shokunin mori`, exit 0):
rows 155; tier A 132 / B 7 / C 16 / invalid 0; status mined 113 / queued 25 / rejected 17 / invalid 0;
missing 0. Row count at the round's entering tip 7118f320 was 152 (`git show 7118f320:corpus/SOURCES.md |
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 152; at tip → 155), i.e. exactly the three new rows.

## 3. Rows S153-S155 against the SOURCES contract (contract text `CORPUS.md:64-135`)

Machine columns from `awk -F'|'` on `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:159-161`:

| id | NF | kind | tier | status | opened | recheck | used-by paths |
|---|---|---|---|---|---|---|---|
| S153 | 13 | docs | A | mined | 2026-10-22 | on-release | corpus/lessons/round-29.md, tools/fixtures/mori-oom-killers/cases-a2-r29.json |
| S154 | 13 | code | A | mined | 2026-10-22 | on-release | same two |
| S155 | 13 | code | A | mined | 2026-10-22 | 180d | same two |

Per-aspect verdicts:

- **Columns** — pass. `NF=13` for all three (11 columns, `CORPUS.md:86`, `CORPUS.md:133-134`), so no stray `|`
  in any cell (`CORPUS.md:88`). Header row `SOURCES.md:5` matches the contract's column order exactly.
- **id** — pass. `S###` format, unique, next unused: ids run 1..155 with no gap and no duplicate
  (`grep -oE '^\| S[0-9]{3,}' | awk` continuity check printed only `last=155`; `uniq -d | wc -l` → 0).
- **kind** — pass. `docs` (S153), `code` (S154, S155) are in the enum at `CORPUS.md:89-90`.
- **tier** — pass. All A, and the A definition covers "official docs, source code, ... maintainer statement"
  (`CORPUS.md:91-96`); S153 is the systemd v262 man-page source, S154 the v262 tree at the release tag, S155 the
  maintainer's commit patch. None is `community`, so the "community is never A" clause is moot.
- **status** — pass. All three `mined`; the definition requires "cited by ≥1 path in used-by" (`CORPUS.md:103`).
  `corpus/lessons/round-29.md` cites all three in its body (`round-29.md:17`, `:20-21`) and in its Gate
  (`round-29.md:55`, `:57`, `:62`). `tools/fixtures/mori-oom-killers/cases-a2-r29.json` carries a top-level
  `"sources": ["S153", "S154", "S155"]` (verified by parsing the JSON: keys `['schema','frozen_with','note','sources','cases']`).
- **opened** — pass. `2026-10-22` is a present ISO date (validator E08 did not fire; run used the default
  `--today` = 2026-10-22Z).
- **recheck** — pass. `on-release`, `on-release`, `180d` are all inside the contract's "ISO date or cadence
  (90d, 180d, on-release)" (`CORPUS.md:105-106`); E09 did not fire, and `overdue` would class the first two as
  symbolic (reported, never judged overdue).
- **used-by shape** — paths are repo-relative and comma-separated (`CORPUS.md:107-108`); both exist on disk
  (`ls -l` shows `round-29.md` 10542 B and `cases-a2-r29.json` 54620 B), consistent with E11 not firing.
- **anchor** — pass. Each carries exact lines plus a revision: S153 `man/sd_journal_get_realtime_usec.xml:36-39,
  :55-69, :80-86, :100` + `tag v262 = commit 8cc40e0c…`; S154 per-file lines + `tag v262 = annotated tag
  1f7dffaf… peeled to commit 8cc40e0c…`; S155 patch `:21-22, :35-38, :71, :79-82, :90` + commit
  `ca2251fcd222af8c857aec4a26e182cf5f9c596e`. No bare homepage (`CORPUS.md:99`).
- **teaches** — pass on form: one grounded benefit per row, no `REJECTED:` prefix (that form is only for
  rejections, `CORPUS.md:102`).
- **Rule 1 (row written only after opening, Gate records URL/date/≤25-word quote)** — pass on all points I could
  re-run. `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-29.md:53-64` is the Gate table with
  URL, access time, sha256 and located quotes. I re-fetched the sources with curl and all seven claimed digests
  reproduce exactly:
  - S153 `sd_journal_get_realtime_usec.xml` 5 372 B, sha256 `dd224fc9…d334` — match.
  - S154 `journal-def.h` 11 593 B `3ab41534…473d`; `sd-journal.c` 128 242 B `36f5b8e6…d726f`;
    `journald-socket.c` 6 874 B `6cb575c9…d926`; `journal-upload-journal.c` 17 651 B `ff643fa4…d03f`;
    `time-util.h` 10 883 B `45e934d2…37e6` — all five match the sha256 list in `SOURCES.md:160`.
  - S155 patch 2 978 B `893e238e…d4bb` — match.
  Line anchors also spot-checked against those bytes: `s153.xml:61-63` and `:82-85` carry the quoted sentences
  (22-word and 24-word quotes, matching the declared counts; the quote elides the `<constant>` markup and the
  word "Since" — [INFERENCE] harmless for a located quote); `journal-def.h:120` is `le64_t monotonic;`;
  `sd-journal.c:2839-2841`, `journald-socket.c:153`, `journal-upload-journal.c:100-101`, `time-util.h:10-12`
  contain the quoted text; `ca2251fc…patch:21-22/35-38/71/79-82/90` contain the `--dryrun` doc line, the `kill_wait`
  guard, the option-table spelling `dryrun`, the `dryrun mode enabled` warn plus flag set, and the `--dry-run`
  help line.
- **Rule 2 (append-only)** — pass. `git diff 7118f320..8809a3f -- corpus/SOURCES.md` adds exactly three `| S15x`
  lines and **zero** removed `|` lines (`grep -cE '^-\|'` → 0), and the lesson logs the addition
  (`round-29.md:69-72`).

## 4. Observations (for L1 judgement; not validator findings)

1. **used-by member type.** The contract enumerates "repo-relative paths of the knowledge entries or lessons
   citing the row" (`CORPUS.md:107-108`). The second member
   `tools/fixtures/mori-oom-killers/cases-a2-r29.json` is a test fixture, neither a knowledge entry nor a lesson.
   No validator code covers member type (E11 only checks existence), so nothing fires. Status `mined` does not
   depend on it — the lesson alone satisfies "cited by ≥1 path". The lesson records the include deliberately
   (`round-29.md:69-72`). Whether a fixture is admissible is a contract-reading call, not a mechanical failure.
2. **recheck cadence vs source mutability.** S155 pins an immutable commit (`ca2251fc`) yet carries `180d`
   (`SOURCES.md:161`). The contract permits any of the three cadences without tying them to mutability, so this
   conforms; [INFERENCE] the 180d date will never change what the commit says, only whether someone re-confirms
   the row's scope.
3. **Multi-URL source cells.** S154 lists five URLs in one `source` cell separated by ` ; ` (`SOURCES.md:160`).
   The contract says "canonical URL or DOI" singular (`CORPUS.md:89`), but this matches existing rows S148/S149/S150
   and no code rejects it. Recorded as precedent consistency, not a defect.
4. **W04 population is untouched by this round's rows.** S153-S155 add no duplicate-URL warning: the URLs
   `sd_journal_get_realtime_usec.xml`, the five v262 tree files and the earlyoom patch are absent from the
   pre-existing ten W04 ids and from any other scope in the registry.

## 5. What I did not run / remaining unknowns

- I did not re-run the full selftest of `sources-census.sh`, `overdue`, or `shared` modes; only `validate` and
  `census` were exercised, as asked.
- I did not re-open S154's `docs/JOURNAL_EXPORT_FORMATS.md`, `journal-export.c`, `logs-show.c`,
  `journal-importer.c`, or the earlyoom reject rows; those are `—` Gate lines, not registry rows.
- Unknown for L1: whether observation 1 needs a contract amendment (used-by admitting non-lesson artifacts) or a
  row-level edit to cite only the lesson. Both are outside this seat's write bounds.
- No tool installs or upgrades were made; no pacman transaction was attempted. Read-only git only
  (`log`, `show`, `diff`, `status`), plain curl for byte verification.
