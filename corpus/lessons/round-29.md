# Round 29 — lesson (mori, L1 MoriR29)

author: MoriR29 (L1), from the wave-1 seat reports under `.ufo/waves/round-29/w1/` and the round-28 outside check
`corpus/lessons/round-28-verifier-spotcheck.md`.
Contract: `.ufo/waves/round-29/contract.md` (declared at `8a45cefe`; amendments A1–A4 before the data each governs).

## What the round learned

- **The standing Axes table had drifted from the closure record for four rounds.** The fleet MANIFEST carries a
  per-axis `verdicts` map for every mori round; five of six rows did not cite the latest admitted `improved` closure
  and five Last change cells predated it (`count-c1.sh` at `7118f320`: `mismatches=11`). Lane spot-check files are
  missing for rounds 19–22 and round 12's has no per-axis table, so a lane-file-only counter would have passed a stale
  adjacency row (wave-1 CriticC1Design F3, ReviewAxesPointers F1).
- **An `improved` verdict is not a score point.** Every admitted improvement in rounds 12–28 left the score alone
  unless the closure stated a number (wave-1 CriticScorePolicy); the round-28 freshness `5 → 6` proposal
  (`SCORECARD.md:1771`) is recorded, not adopted.
- **A dry run is a send-site no-op** (S155): earlyoom logs the `sending …` line, then returns before `kill()`, so a
  dry-run invocation's send lines record decisions, never deliveries; dry-run is set once per invocation at option
  parsing (S155 patch `:79-82`; S119 for the v1.9.0 line numbers).
- **A journal entry's monotonic stamp is meaningful only within its boot** (S153) and is part of the entry object
  header, rendered as bare unsigned decimal in export and JSON output (S154); a record without a numeric stamp cannot
  be placed in or out of an invocation.

## Mistakes

- **M1 — self-assessment table not updated after admitted closures (class: stale self-assessment).** Evidence: the
  `## Axes` rows at `7118f320` (`SCORECARD.md:10-15`) cite no closure later than round 24 while MANIFEST admits
  improved verdicts in rounds 19, 25, 26 and 28; operability's `round 14 (6 → 7)` contradicts round 14's `unchanged`.
  Captured-by: none (round 25's D5 counter checked scores and the `round 1` rule only). Fix: `.ufo/waves/round-29/count-c1.sh`,
  shown able to fail: `mismatches=11`, exit 1 at `7118f320` (`evidence/c1-before.txt`); `mismatches=0` at
  `420d05ad` (`evidence/c1-after.txt`).
- **M2 — a gate bound into a counted condition before it was run on a known-clean input (class: unscreened
  instrument).** Evidence: amendment A4 made `check-blind-wave.sh` `blind_violations=0` a C2 condition; its first run on
  the round-29 writer wave printed 20 hits (`evidence/blind-check-prefreeze.txt`), among them bare `exit N` lines and
  writer files-opened headings it does not recognise. Captured-by: the L1's pre-freeze run. Fix: QUALITY 85 note; a
  rule that a gate enters a counted condition only after a receipt of it on the round's own inputs. Not yet shown able
  to fail.
- **M3 — a seat report misrooted at the fleet root (class: write outside the lane).** Evidence: `CaseA207c` wrote
  `.ufo/waves/round-29/w1/CaseA207c.md` under `/home/vgpnk/Projects/shokunin/` (20:00:53Z) although the wave context
  named the absolute lane path. Captured-by: the L1's listing of `w1/` while assembling cases (manual). Fix: swept
  byte-exact (`cmp` ok, sha256 `0fe85d0b…a0a`), fleet copy deleted; carried: no automated per-wave check.
- **M4 — round-28 tip receipts did not say they were measured at the parent (class: receipt provenance).** Evidence:
  `round-28-verifier-spotcheck.md:129-130`. Captured-by: the round-28 closure. Fix: QUALITY 87 and
  `.ufo/waves/round-29/make-tip-receipts.sh`; the QUALITY 87 check fails on `1fc6bb0`
  (`header_not_parent=…/tip-count-c1.txt`, wave-1 DraftQualityCriteria).

## Gate (rows opened 2026-10-22 in round 29)

Each line is copied from the drafting seat's report (`.ufo/waves/round-29/w1/SourceJournalMonotonic.md`,
`SourceJournalExport.md`, `SourceEarlyoomDryrun.md`); `—` lines are reject decisions met during the source work
(QUALITY 86).

| id | source | access time | sha256 | located quote | decision |
|---|---|---|---|---|---|
| S153 | https://raw.githubusercontent.com/systemd/systemd/v262/man/sd_journal_get_realtime_usec.xml | 2026-10-22T19:55:54Z | `dd224fc99710940d4e5d362aaa54768afc05dc1778c5cffa22595dbc1556d334` | `:61-63` (22 words): "the monotonic clock begins new with every reboot, it only defines a well-defined point in time when used together with an identifier"; `:82-85` (24 words): "If the boot ID parameter was passed NULL and the monotonic timestamp of the current journal entry is not of the current system boot" | admit, A, mined |
| — | https://raw.githubusercontent.com/systemd/systemd/v262/man/sd_journal_get_monotonic_usec.xml | 2026-10-22T19:56:12Z | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` | body line 1 (3 words): "404: Not Found" | reject, 404: the v262 manual source carries both functions on the sd_journal_get_realtime_usec page, so no separately named monotonic page exists to open |
| S154 | https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-journal/journal-def.h (with sd-journal.c, journald-socket.c, journal-upload-journal.c and time-util.h at the same tag) | 2026-10-22T19:57:34Z | `3ab41534b3d6ef19ada59f6df60c74742f2900a2c278980ea3d16b8379d8473d` | `journal-def.h:120` "le64_t monotonic;" (2 words); `sd-journal.c:2839-2841` "uint64_t t = le64toh(o->entry.monotonic); if (!VALID_MONOTONIC(t)) return -EBADMSG;" (8 words); `journald-socket.c:153` "xsprintf(monotonic_buf, \"__MONOTONIC_TIMESTAMP=\"USEC_FMT\"\\n\\n\", ts->monotonic);" (3 words); `journal-upload-journal.c:100-101` "r = snprintf(buf + pos, size - pos, \"__MONOTONIC_TIMESTAMP=\"USEC_FMT\"\\n\", monotonic);" (11 words); `time-util.h:12` "#define USEC_FMT \"%\" PRI_USEC" (4 words) | admit, A, mined |
| — | https://raw.githubusercontent.com/systemd/systemd/v262/docs/JOURNAL_EXPORT_FORMATS.md | 2026-10-22T19:57:53Z (grep only; URL not fetched) | — | `corpus/SOURCES.md:128` shows this URL inside row S122 | reject, duplicate URL already carried by S122 |
| — | https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-journal/journal-export.c | 2026-10-22T19:56:08Z | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` | body line 1 (3 words): "404: Not Found" | reject, HTTP 404 at v262 — no such file; the export writer is src/shared/logs-show.c:911 |
| — | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c | 2026-10-22T19:56:08Z | `abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f` | `:1266-1267` (11 words): "xsprintf(usecbuf, USEC_FMT, monotonic); r = update_json_data(h, flags, \"__MONOTONIC_TIMESTAMP\", usecbuf, SIZE_MAX);" | reject, duplicate URL already carried by S123 (corpus/SOURCES.md:129); JSON string form kept as corroboration only |
| — | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/journal-importer.c | 2026-10-22T19:57:34Z | `bfef6c03c28cc2f6fff3792dafb723a35c0831bc9b72ca4bd3ff6ea9eb9e0bdc` | `:251` (4 words): "value = startswith(line, \"__MONOTONIC_TIMESTAMP=\");"; `:255` (5 words): "r = safe_atou64(value, &x);" | reject, adds no format evidence: it only matches the field name and parses base 0 (parse-util.h:86-88), so it cannot support a decimal-only claim |
| S155 | https://github.com/rfjakob/earlyoom/commit/ca2251fcd222af8c857aec4a26e182cf5f9c596e.patch | 2026-10-22T19:59:28Z | `893e238ea3b7f512f0506ccc87e0decfea8846e2e4b0704c51ced2820465d4bb` | patch `:35-38` (17 words): "if (args.dryrun && sig != 0) { warn(\"dryrun, not actually sending any signal\n\"); return 0; }" | admit, A, mined |
| — | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | 2026-10-22T19:59:10Z | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` | `:272` (8 words): "warn(\"dryrun, not actually sending any signal\n\");" | reject, duplicate URL — S118 rows v1.9.0 kill.c and already anchors `:272` |
| — | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md | 2026-10-22T19:59:10Z | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` | `:205-206` (9 words): "#### \-\-dryrun" / "dry run (do not kill any processes)" | reject, duplicate URL — S115 rows the v1.9.0 manual with `--dryrun` in its scope |
| — | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/testsuite_cli_test.go ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.h | 2026-10-22T19:56:07Z | `1dc876421c856bde48ab4a63304dab838c585f79c68a807d52b0741d366eb795` (9 317 B) ; `abf8577b434096e1eb980bacc24508e8421af9edbefb0d78cf5b8b5f28160bfb` (1 440 B) | `kill.h:36-37` (8 words): "/* Flag --dryrun was passed */" / "bool dryrun;" | reject, does not carry the fact — kill.h only declares the flag field, and a case-insensitive grep for `dryrun` and `version` returned no line in either file |

### Row changes logged old → new (CORPUS Rules 2)

- New rows S153 (systemd v262 `sd_journal_get_realtime_usec.xml`), S154 (systemd v262 entry-object monotonic stamp,
  `journal-def.h` and export writers), S155 (earlyoom commit `ca2251fc` dry-run option); status `mined`; `used-by`
  this lesson and `tools/fixtures/mori-oom-killers/cases-a2-r29.json` (top-level `sources` key). No `status`,
  `recheck` or `used-by` cell of an older row changed.

### Census (round start → round end)

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`: start
(19:50:48Z, `7118f320`) ten W04, `mori ok`, exit 0. End: see the closing section below.

## Routed defects (round-28 closure §6) — disposition

| Routed | Disposition | Evidence |
|---|---|---|
| 1 late wave-2 outputs | `MutCountC1Amended`, `MutHeadingCheck`, `MutTipReceiptCheck` re-verified (findings reproduced, no verdict impact), committed as evidence; `wave1-run.err` (0 bytes) committed; `FixR1Runway.md` disposed out of the lane (privacy) | `w1/ReviewLate*.md`; `e1c6bbe7`, `3a147138`; LOG round 29 |
| 2 C2 blindness, A2-07/A2-10 shapes | C2: 24 blind cases frozen at `d6d5cb0a` | contract C2, A2–A4 |
| 3 Gate rejects | this Gate carries reject rows; QUALITY 86 | above |
| 4 tip receipts at parent | QUALITY 87, `make-tip-receipts.sh` | M4 |
| 5 census count | appended correction in `round-28.md` | `3a147138` |
| 6 carried debt | inventoried (wave-1 ScoutCarriedDebt): all items open at `7118f320`, carried by name | `w1/ScoutCarriedDebt.md` |
