# ReopenS154 — falsify row S154 and its Gate lines

Seat: MoriR29.ReopenS154 (leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Tip judged: `8809a3fe1eaa87a0afa177a15263d174378e7462` (`git rev-parse HEAD`, 20:33Z).
Content judged from the committed tip (`git show HEAD:...`), not the working tree, because a peer
mutation test was touching `corpus/lessons/round-29.md` during the check window (see O1).
All URLs fetched 2026-10-22T20:36:21Z (UTC) into `/fast/scratch/hyaku/mori-r29/w2/ReopenS154/src2/`
(receipt: `src2/receipt.txt`); an earlier independent fetch at ~20:33Z into `src/` produced identical digests.
No tool installs or upgrades were needed or made.

## Verdict

**The S154 admission stands.** Every URL resolves to the recorded bytes, every located quote is
verbatim at its stated line and under 25 words, the row has 11 columns, and both `used-by` files cite
`S154` as a whole word. Three documentation defects were found and none of them falsifies the taught
fact: one recorded word count is not reproducible (F1), one clause of `teaches` is true for only one of
the two cited writers (F2), and the *lesson* line that consumes the row attributes the JSON half to
S154 although the row explicitly excludes JSON (F3).

## Claim table (claim | recorded | observed | holds?)

| # | Claim | Recorded | Observed | Holds? |
|---|---|---|---|---|
| 1 | Registry shape | header `corpus/SOURCES.md:9` has 11 cells | `awk -F'|'` on `:160`: header cols 11, S154 cols 11 (id/source/kind/tier/scope/anchor/teaches/status/opened/recheck/used-by) | yes |
| 2 | kind / tier | `code` / `A` | sources are `.c`/`.h` at a release tag | yes (kind); tier A is a judgement, not testable here |
| 3 | journal-def.h URL | HTTP 200, 11,593 B, `3ab41534…d8473d` | 200, 11,593 B, `3ab41534b3d6ef19ada59f6df60c74742f2900a2c278980ea3d16b8379d8473d` | yes |
| 4 | sd-journal.c URL | 128,242 B, `36f5b8e6…ad726f` | 200, 128,242 B, `36f5b8e64cd60b6843705734cc49fdf129c6740e236118f3cde6603c44ad726f` | yes |
| 5 | journald-socket.c URL | 6,874 B, `6cb575c9…a5d926` | 200, 6,874 B, `6cb575c9f43d1293004b2d6184826a4a819b222ad6fdcaa69a1778f8cda5d926` | yes |
| 6 | journal-upload-journal.c URL | 17,651 B, `ff643fa4…81fd03f` | 200, 17,651 B, `ff643fa4a9af51184e12aa4581b3e1b19f98d0d68a4b8d8cf6e41a4de81fd03f` | yes |
| 7 | time-util.h URL | 10,883 B, `45e934d2…ba37e6` | 200, 10,883 B, `45e934d294f2ff0ca92cc7f1fcede1ef92862d20b276e305282cec5f3cba37e6` | yes |
| 8 | Tag identity | annotated tag `1f7dffaf…` peeled to commit `8cc40e0c…` | `git ls-remote https://github.com/systemd/systemd 'refs/tags/v262*'`: `1f7dffaf714cc4488159c498b7a17cf34c5a96d5 refs/tags/v262`, `8cc40e0c5e9234bf45084751ac53b1fbfe70b492 refs/tags/v262^{}` | yes |
| 9 | `journal-def.h:120` member, macro opens `:116` | `le64_t monotonic;` inside `EntryObject__contents` | `:116` `#define EntryObject__contents {`, `:117` `ObjectHeader object;`, `:120` `le64_t monotonic;` | yes |
| 10 | `sd-journal.c:2839-2841` | `uint64_t t = le64toh(o->entry.monotonic); if (!VALID_MONOTONIC(t)) return -EBADMSG;` | identical on `:2839`,`:2840`,`:2841`, inside `sd_journal_get_monotonic_usec` (boot-ID check at `:2830-2836`) | yes |
| 11 | `journald-socket.c:146-154` | comment `Synthesise __REALTIME_TIMESTAMP and __MONOTONIC_TIMESTAMP`; `"__MONOTONIC_TIMESTAMP="USEC_FMT"\n\n"` | `:146-147` comment verbatim; `:153` `xsprintf(monotonic_buf, "__MONOTONIC_TIMESTAMP="USEC_FMT"\n\n", ts->monotonic);`; `:154` iovec push | yes |
| 12 | `journal-upload-journal.c:87-101` | `case ENTRY_MONOTONIC`; `__MONOTONIC_TIMESTAMP=` format | `:87` `case ENTRY_MONOTONIC: {`; `:91` `sd_journal_get_monotonic_usec`; `:100-101` `r = snprintf(buf + pos, size - pos,` / `"__MONOTONIC_TIMESTAMP="USEC_FMT"\n", monotonic);` | yes |
| 13 | `time-util.h:10-12` | `PRI_USEC PRIu64`, `USEC_FMT "%" PRI_USEC` | `:9` `PRI_NSEC PRIu64`, `:10` `PRI_USEC PRIu64`, `:11` `NSEC_FMT`, `:12` `USEC_FMT "%" PRI_USEC` | yes |
| 14 | Gate quote word counts | 2, 8, 3, 11, 4 | whitespace-token counts 2, 8, 3, **10**, 4 (F1) | 4 of 5; all ≤25 |
| 15 | teaches: member of the entry object header | "a member of the entry object header" | `journal-def.h:116-120` (`ObjectHeader object;` then `le64_t monotonic;`) | yes |
| 16 | teaches: not of the enumerated field list | "not of the enumerated field list" | no synthetic `__MONOTONIC_TIMESTAMP` in `journal-file.c` (grep: 0) or `sd-journal.c` (grep: 0); the field line is manufactured only by the printers (`logs-show.c:969`, `journald-socket.c:153`) | yes (absence evidence, not a positive statement in the cited bytes) |
| 17 | teaches: every complete entry yields one | "so every complete entry yields one" | header member is unconditional; `journal-file.c:1037` rejects an `OBJECT_ENTRY` whose stamp fails `VALID_MONOTONIC`; `VALID_MONOTONIC(u)` is `u < (1ULL << 55)` (`journal-file.h:154-158`, accepts 0). The macro is not in the five cited files | yes, with [INFERENCE] on the macro |
| 18 | teaches: export prints it from that accessor, unquoted decimal | "prints it from that accessor as an unquoted unsigned decimal" | `journal-upload-journal.c:91` calls the accessor then `:100-101` prints bare decimal; `journald-socket.c:153` prints `ts->monotonic` (a `dual_timestamp`), not `o->entry.monotonic` | partial (F2) |
| 19 | teaches: `USEC_FMT` is `"%" PRIu64` | `USEC_FMT "%" PRI_USEC`, `PRI_USEC PRIu64` | `time-util.h:10,12` | yes |
| 20 | status / Gate decision | `mined`, `admit, A, mined` | consistent fields; no other row cell changed (`lessons/round-29.md:69` says so) | yes |
| 21 | used-by lesson | `corpus/lessons/round-29.md` | file exists; `grep -nw S154` hits `:21`, `:57`, `:69` | yes |
| 22 | used-by fixture | `tools/fixtures/mori-oom-killers/cases-a2-r29.json` | file exists; top-level `"sources": [ "S153", "S154", "S155" ]` at `:6-10`, `"S154",` at `:7` (word cite) | yes |
| 23 | Reject: JOURNAL_EXPORT_FORMATS.md duplicate of S122 | URL inside S122 | `corpus/SOURCES.md:128` contains that exact URL (grep count 1 in the registry); my fetch: 200, 8,556 B, `207a646c067be133ff711f039bb2997a706bc5c146b7db6aa0f0350997b25543` (drafter never fetched it, so no hash was recorded) | yes |
| 24 | Reject: journal-export.c 404, export writer is `logs-show.c:911` | 404, 14 B, `d5558cd4…`; `:911` | 404, 14 B, `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` (body "404: Not Found"); `logs-show.c:911` is `static int output_export(` | yes |
| 25 | Reject: logs-show.c duplicate of S123; quote `:1266-1267` | 87,278 B, `abc2fc1f…`; "(11 words)" | 200, 87,278 B, `abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f`; URL in `corpus/SOURCES.md:129`; quote verbatim at `:1266-1267`, 10 whitespace tokens (F1) | hash/line/duplicate yes; count off by one |
| 26 | Reject: journal-importer.c adds no format evidence; base 0 | 16,644 B, `bfef6c03…`; `:251` 4 words, `:255` 5 words | 200, 16,644 B, `bfef6c03c28cc2f6fff3792dafb723a35c0831bc9b72ca4bd3ff6ea9eb9e0bdc`; `:251` `value = startswith(line, "__MONOTONIC_TIMESTAMP=");` (4 words); `:255` `r = safe_atou64(value, &x);` (4 tokens, not 5); `safe_atou64` → `safe_atou64_full(s, 0, …)` at `parse-util.h:85-87`, so base 0 is confirmed | basis yes; one count off by one |

Quotes were checked by normalizing whitespace and requiring exact containment in the fetched bytes
(`python3`), then re-printing the numbered lines. Every located quote is verbatim; the longest is 10
(or 11 if a format string is counted as two fragments), far below the 25-word cap.

## Findings

- **F1 (minor, Gate/recorded counts).** The Gate line's `journal-upload-journal.c:100-101` quote is
  recorded as **11 words**; whitespace tokenization gives **10**. The same off-by-one appears twice in the
  reject rows: `logs-show.c:1266-1267` recorded 11 / observed 10, `journal-importer.c:255` recorded 5 /
  observed 4. The cap ("<=25 words") holds for all of them, so this does not falsify any admission; it is a
  count-method inconsistency (C-token vs whitespace counting) that a future counter should not treat as
  evidence of a longer quote.
- **F2 (minor, `teaches` wording).** "the export format prints it **from that accessor**" is supported by
  `journal-upload-journal.c:91,100-101` (which calls `sd_journal_get_monotonic_usec`), but the other
  cited writer, `journald-socket.c:153`, prints `ts->monotonic` from journald's own `dual_timestamp`, not
  from the entry object. The unquoted-decimal half is true for both. Suggested narrowing: "the writers
  that emit the export line print it unquoted decimal, one of them from the entry accessor".
- **F3 (defect outside the row, in the consuming lesson).** `corpus/lessons/round-29.md:21` says the stamp
  is "rendered as bare unsigned decimal in export **and JSON output** (S154)". Row S154's own scope cell
  excludes "the JSON rendering (S122 … S123)", and the JSON encoder renders the value as a JSON string
  (`logs-show.c:1266-1267`: `update_json_data(h, flags, "__MONOTONIC_TIMESTAMP", usecbuf, …)`), which
  `corpus/SOURCES.md:129` (S123) describes as the encoder "that makes a printable value a string". The JSON
  half is therefore cited to the wrong row and, as written ("bare … in JSON"), contradicts S123. Fix:
  either drop "and JSON output", or say "quoted JSON string (S123)".
- **F4 (scope note, not a falsification).** The canonical `journalctl -o export` printer is
  `logs-show.c:911` `output_export`, which prints `"__MONOTONIC_TIMESTAMP=" USEC_FMT "\n"` at `:969` from
  the accessor. That file is S123's URL and the Gate here rejects it as a duplicate, so S154 itself does
  not carry the export printer — only two producers of the same line format (`journald-socket.c`,
  `journal-upload-journal.c`). The taught fact is still verified by the cited bytes; if the L1 wants the
  export printer itself under S154, that is an added citation, not a correction.
- **O1 (observed repository state, for the L1 only).** During the check window
  `corpus/lessons/round-29.md` was dirty against `8809a3fe`: at 20:35Z the four S154 reject rows and the
  S153/S155 reject rows carried their row id instead of the section's documented `—` marker
  (`git diff --numstat`: 8/8 lines); by 20:36:33Z that hunk was gone and only an unrelated line-10 text
  change remained. I judged the tip (`git show HEAD:`), where all reject rows carry `| — |` and match
  `.ufo/waves/round-29/w1/SourceJournalExport.md` verbatim, including the S154 admit row (compared
  byte-for-byte modulo the `S15x`→`S154` id substitution: identical). Nothing in this report depends on
  the transient state.

## Unresolved / inference

- The drafter's access times (19:56:08Z–19:59:10Z in `corpus/lessons/round-29.md:57-61`) cannot be
  replayed. Content identity is nevertheless pinned: raw.githubusercontent serves tag `v262`, whose peeled
  commit is `8cc40e0c…`, and two independent fetches 3 minutes apart reproduced every recorded sha256.
- [INFERENCE] "every complete entry yields one" relies on `VALID_MONOTONIC` (`journal-file.h:157`, outside
  the five cited URLs) and on `journal-file.c:1037`'s object validation. That inference is consistent, but
  it is not stated in any S154-cited file.
- [INFERENCE] The row's tier `A` and the `recheck: on-release` policy are editorial choices; I did not test
  them.
