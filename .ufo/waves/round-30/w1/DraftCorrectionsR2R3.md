# Round 30 wave 1 — R2 and R3 appended-correction drafts

Seat `MoriR30.DraftCorrectionsR2R3`, leaf (no subagents, no background jobs). Contract read first:
`.ufo/waves/round-30/contract.md` (landed `a66751b1a97fb6422a4756f867d94269de9bcdd5`, entering tip
`58b61681a0e3f3b821a17d38a4e713ccd9921615`); routed items are its §"Routed hygiene" R2 and R3, restated at
`corpus/lessons/round-29-verifier-spotcheck.md:160-163`.

Produced: two ready-to-paste texts — one appended section for the round-30 lesson covering R2 **and** R3, and one
appended note for `corpus/SOURCES.md` covering R3. Nothing in the lane was edited: `corpus/lessons/round-29.md` and
`corpus/SOURCES.md` were read only, and `corpus/lessons/round-30.md` does not exist yet
(`ls corpus/lessons/round-30.md` → `No such file or directory`).

## 1. R2 — the two files, re-fetched

Run in scratch `/fast/scratch/hyaku/mori-r30/MoriR30.DraftCorrectionsR2R3`:

```sh
for f in kill.h testsuite_cli_test.go; do
  curl -sS -o "$f" -w '%{http_code} %{size_download} %{url_effective}\n' \
    "https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/$f"
done
date -u +%FT%TZ
sha256sum kill.h testsuite_cli_test.go
wc -c kill.h testsuite_cli_test.go
```

Output (access time `2026-10-22T21:12:35Z`, recorded immediately after both fetches):

```
200 1440 https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.h
200 9317 https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/testsuite_cli_test.go
2026-10-22T21:12:35Z
abf8577b434096e1eb980bacc24508e8421af9edbefb0d78cf5b8b5f28160bfb  kill.h
1dc876421c856bde48ab4a63304dab838c585f79c68a807d52b0741d366eb795  testsuite_cli_test.go
 1440 kill.h
 9317 testsuite_cli_test.go
```

Both digests and both sizes equal the cells recorded at `corpus/lessons/round-29.md:65`
(`` `1dc87642…` (9 317 B) ; `abf8577b…` (1 440 B) ``), so only the reject *reason* is wrong, not the provenance.

The grep the row names:

```sh
grep -in -e dryrun -e version kill.h
grep -in -e dryrun -e version testsuite_cli_test.go
grep -in version kill.h testsuite_cli_test.go
```

Output:

```
$ grep -in -e dryrun -e version kill.h
36:    /* Flag --dryrun was passed */
37:    bool dryrun;
exit=0
$ grep -in -e dryrun -e version testsuite_cli_test.go
exit=1
$ grep -in version kill.h testsuite_cli_test.go
exit=1
```

So "returned no line in either file" (`corpus/lessons/round-29.md:65`) is **false for `kill.h`** and true only for
`testsuite_cli_test.go`. The reject decision stands on the substance: `kill.h` is 44 lines
(`wc -l kill.h` → `44`), lines 36-37 are declarations inside `poll_loop_args_t` (`kill.h:30-38`, closed by
`} poll_loop_args_t;` at `:38`), the file contains no `kill_wait` text, and its only prototype is
`void kill_process(const poll_loop_args_t* args, int sig, const procinfo_t* victim);` at `kill.h:40`. The published
quote at `round-29.md:65` matches the fetched bytes verbatim (`kill.h:36` and `:37` above), 8 words over its two
strings.

## 2. R2 + R3 — ready-to-paste appended correction for `corpus/lessons/round-30.md`

Append as a new section after the lesson's existing sections. No line starts with `| S`, so the C1 Gate-row scan is
untouched.

```md
## Appended corrections to round-29 records (wave 1, DraftCorrectionsR2R3; round-29 text and SOURCES cells untouched)

- **R2 — `corpus/lessons/round-29.md:65`, S155 reject row (`testsuite_cli_test.go` ; `kill.h`).** The reason sentence
  "a case-insensitive grep for `dryrun` and `version` returned no line in either file" is false for `kill.h`. Both
  files were re-fetched at 2026-10-22T21:12:35Z: `kill.h` HTTP 200, 1 440 B, sha256
  `abf8577b434096e1eb980bacc24508e8421af9edbefb0d78cf5b8b5f28160bfb`; `testsuite_cli_test.go` HTTP 200, 9 317 B,
  sha256 `1dc876421c856bde48ab4a63304dab838c585f79c68a807d52b0741d366eb795` — equal to the row's recorded digests and
  sizes. `grep -in -e dryrun -e version kill.h` prints `36:    /* Flag --dryrun was passed */` and
  `37:    bool dryrun;` (exit 0); the same command on `testsuite_cli_test.go` prints nothing (exit 1); `version` matches
  no line in either file. The reject decision stands unchanged, and the located quote (`:36-37`, 8 words over its two
  strings) is correct: both matches are field declarations inside `poll_loop_args_t` (`kill.h:30-38`); the file has 44
  lines and one prototype (`void kill_process(...)`, `kill.h:40`), so it declares the flag and carries no send-site
  behavior.
- **R3 — `corpus/lessons/round-29.md:55-65`, S153-S155 Gate word-count labels.** 16 labels cover 18 quoted strings;
  5 labels are wrong and every quoted string, location and digest is right. Recomputed with `wc -w` on each verbatim
  string:
  - `:57` `journal-upload-journal.c:100-101` label 11 → **10**
  - `:60` `logs-show.c:1266-1267` label 11 → **10**
  - `:61` `journal-importer.c:255` label 5 → **4**
  - `:62` patch `:35-38` label 17 → **16**
  - `:63` `kill.c:272` label 8 → **6**
  The other 11 labels reproduce exactly: `:55` 22 and 24, `:56` 3, `:57` 2, 8, 3 and 4, `:59` 3, `:61` 4,
  `:64` 9 over its two strings, `:65` 8 over its two strings. The routed pair (`round-29-verifier-spotcheck.md:163`)
  names 11 vs 10 and 17 vs 16; three more are reported here (`:60`, `:61`, `:63`), and `:63` is two high, not one. The
  largest true quote is 24 words, so the 25-word quote bound holds either way. The labels entered through the drafting
  seats and were copied into the Gate: `w1/SourceJournalExport.md:81` (labels `2,8,3,11,4`) and `:85` (`4,5`),
  `w1/SourceEarlyoomDryrun.md:72-73` (`17`, `8`). Decisions, quotes, locations and digests are unaffected; the counts
  are corrected here, not edited into the rows.
```

## 3. R3 — every label in `round-29.md:55-65`, recomputed

Method: for each `(N words)` label take the quoted string or strings it covers, verbatim from the file, and pipe to
`wc -w`. 16 labels, 18 quoted strings, 5 mismatches (11 agree).

| line | row / quote locator | label | `wc -w` | delta |
|---|---|---|---|---|
| 55 | S153 `:61-63` | 22 | 22 | — |
| 55 | S153 `:82-85` | 24 | 24 | — |
| 56 | S153 reject, 404 body | 3 | 3 | — |
| 57 | S154 `journal-def.h:120` | 2 | 2 | — |
| 57 | S154 `sd-journal.c:2839-2841` | 8 | 8 | — |
| 57 | S154 `journald-socket.c:153` | 3 | 3 | — |
| 57 | S154 `journal-upload-journal.c:100-101` | 11 | **10** | one high (routed) |
| 57 | S154 `time-util.h:12` | 4 | 4 | — |
| 59 | S154 reject, 404 body | 3 | 3 | — |
| 60 | S154 reject `logs-show.c:1266-1267` | 11 | **10** | one high (new) |
| 61 | S154 reject `journal-importer.c:251` | 4 | 4 | — |
| 61 | S154 reject `journal-importer.c:255` | 5 | **4** | one high (new) |
| 62 | S155 admit, patch `:35-38` | 17 | **16** | one high (routed) |
| 63 | S155 reject `kill.c:272` | 8 | **6** | two high (new) |
| 64 | S155 reject, manual `:205-206` (two strings) | 9 | 9 | — |
| 65 | S155 reject, `kill.h:36-37` (two strings) | 8 | 8 | — |

Direct re-verification of the five mismatches (run as one loop over the verbatim strings):

```
r = snprintf(buf + pos, size - pos, \"__MONOTONIC_TIMESTAMP=…  ->  10
xsprintf(usecbuf, USEC_FMT, monotonic); r = update_json_data…  ->  10
r = safe_atou64(value, &x);                                   ->  4
if (args.dryrun && sig != 0) { warn(\"dryrun, not actuall…     ->  16
warn(\"dryrun, not actually sending any signal\n\");           ->  6
```

The strings were truncated above only for display; the loop fed the full strings copied from `round-29.md:57,60,61,62,63`
to `printf '%s' "$q" | wc -w`. Escaping is not a confounder: removing the markdown backslashes leaves every one of the
five counts unchanged.

`corpus/SOURCES.md` side: rows S153-S155 are `corpus/SOURCES.md:159-161`, and the whole file carries **zero** `(N words)`
labels (`grep -cE '\([0-9]+ words?\)' corpus/SOURCES.md` → `0`), so no arithmetic inside `SOURCES.md` itself is wrong.
The row cells hold unlabelled backticked anchors (`corpus/SOURCES.md:160`, anchor cell `journal-upload-journal.c:87-101`
and `time-util.h:10-12`); the mislabels exist only in the Gate lines that publish those rows' quotes.

## 4. R3 — ready-to-paste appended correction note for `corpus/SOURCES.md`

Insert after the Round 24 search paragraph (`corpus/SOURCES.md:206`), before `## Leads (unopened)`
(`corpus/SOURCES.md:208`), following the precedent at `corpus/SOURCES.md:188` (`Correction (append-only, 2026-10-20,
Registry seat): …`). It starts with no `|`, so the Registry row parser and the census are unaffected.

```md
Correction (append-only, 2026-10-22, round-30 wave-1 DraftCorrectionsR2R3): five word-count labels published for rows S154 and S155 in `corpus/lessons/round-29.md` `## Gate` are wrong; the S153-S155 cells in this file carry no word-count label, so no cell here is edited. True `wc -w` values: `journal-upload-journal.c:100-101` 10, not 11 (`round-29.md:57`); `logs-show.c:1266-1267` 10, not 11 (`:60`); `journal-importer.c:255` 4, not 5 (`:61`); patch `:35-38` 16, not 17 (`:62`); `kill.c:272` 6, not 8 (`:63`). Quoted text, line locations, sha256 cells and the admit/reject decisions stand, as do scope, kind, tier, status, recheck and used-by. The mislabels entered through the drafting seats (`w1/SourceJournalExport.md:81,85`; `w1/SourceEarlyoomDryrun.md:72-73`) and were copied into the Gate; the corrected counts are also appended to `corpus/lessons/round-30.md`.
```

## 5. Gates — each shown able to fail, red now

R2 check (red now: the false sentence is in the lesson; green after the L1 appends the block):

```sh
grep -n 'returned no line in either file' corpus/lessons/round-29.md
# 65:| S155 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/testsuite_cli_test.go ; ...
grep -q '36:    /\* Flag --dryrun was passed \*/' corpus/lessons/round-30.md
# exit 2 now: corpus/lessons/round-30.md: No such file or directory
```

R3 check (red now, green after the append; it counts corrected pairs, so a restated wrong label cannot pass):

```sh
grep -c 'label 11 → \*\*10\*\*' corpus/lessons/round-30.md   # expect 2
grep -c 'label 5 → \*\*4\*\*'   corpus/lessons/round-30.md   # expect 1
grep -c 'label 17 → \*\*16\*\*' corpus/lessons/round-30.md   # expect 1
grep -c 'label 8 → \*\*6\*\*'   corpus/lessons/round-30.md   # expect 1
# all four exit 2 now (lesson absent)
```

A wrong-label restatement would fail the R3 check because the block spells the corrected value in bold; a block that
omitted `:60`, `:61` or `:63` would fail its count. No counted claim is made by this seat: the QUALITY rows for R2/R3
are the L1's.

## 6. Bounds, tools, limits

- Wrote only this report and `/fast/scratch/hyaku/mori-r30/MoriR30.DraftCorrectionsR2R3/` (`kill.h`,
  `testsuite_cli_test.go`, `wc-audit.sh`, `mislabels.txt`, `gate-55-65.txt`, `sources-159-161.txt`). No lane file was
  written or edited; no git or jj command ran at all (read-only or otherwise); no unit, systemd, `/etc` or fleet script
  was touched; no host unit name, uid, pid, journal MESSAGE or `/etc/default/earlyoom` value was read into this report.
  No line of `tools/mori-oom-killers.py` source and none of that tool's output appears here.
- Tools: none installed or updated; no pacman transaction was run, so the tooling directive has nothing to record.
- Sources were opened only by plain `curl` to the public raw URLs; no bot challenge was passed.
- Limits: counts are of the strings **as published** in `corpus/lessons/round-29.md:55-65`; the only upstream bytes
  compared this round are `kill.h` and `testsuite_cli_test.go` (§1). `[INFERENCE]` none is needed for the counts; the
  claim that the published systemd/earlyoom quotes match upstream verbatim is **not** re-established here.
- Out of scope, untouched: `corpus/lessons/round-29.md` and `corpus/SOURCES.md` themselves (drafts only), the source
  seats' reports, other rounds' Gate labels, `LOG.md`, and the round-29 note at `corpus/SOURCES.md:188` about rendered
  systemd 262 line numbers.
- Observation for the canonical judge, not a ruling: the closure's R3 text
  (`corpus/lessons/round-29-verifier-spotcheck.md:163`) says "S154/S155 word-count labels one high (11 vs 10, 17 vs
  16)"; the recomputation finds five wrong labels, of which three are outside that text and one (`kill.c:272`, 8 vs 6)
  is two high.
