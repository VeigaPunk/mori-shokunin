# Mo59Scribe48 — round-59 lesson Gate skeleton (draft only)

Seat: scribe, leaf. Work: read-only on the lane; no corpus/registry/SCORECARD/LOG/VCS edits, no
commits, no fleet or sibling writes. Only this report was written.

Inputs read at the start: `.ufo/waves/round-59/contract.md`, `.ufo/waves/round-59/count-c1.py`,
`.ufo/waves/round-59/count-c2.py` (freeze revision `60b3a76ad0524c8978cc51922940be1c8c388915`;
entering revision `2b9f03975bfb6e508f35074ac8181ec8bf54e805`). Lane HEAD observed while working:
`8ff344ff18924c1ea63d46c3b3969f9fea05bc51` ("round-59: validated w1 dispatch payload").
Disk guard at start: `/fast/scratch/hyaku` 27% used, 592.6G free — green; no ENOSPC workaround used.
Scratch root used and removed: `/fast/scratch/hyaku/mori-r59/Mo59Scribe48`
(`TMPDIR` set there for the counter-style runs; receipts inlined below before removal).

## 1. Deliverable — draft `## Gate` block for `corpus/lessons/round-59.md`

Skeleton text, lesson style (same shape as `corpus/lessons/round-58.md` §Gate). All six rows are the
six copies declared by `count-c2.py` `ARTIFACTS`, in that dict's order; every row's `used-by` is
exactly `corpus/knowledge/wave-settlement-artifacts-r59.md`. Quotes are byte-exact at the freeze
revision and ≤25 words (2, 2, 2, 2, 2, 1 words; counted by whitespace split).

```markdown
## Gate

### Sources opened and gate decisions

- **Admit S553 (tier A, own-work).** Re-opened `.ufo/waves/round-54/w1-results.json` at lane freeze `60b3a76ad0524c8978cc51922940be1c8c388915` on 2026-10-28; sha256 `ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f`. Located quote: `"seats": 74,` (line 5, offset 49; 2 words). The object declares 74 seats and carries 74 member objects; keys exactly {name, agent, output, note}; unique names; all ten role tokens. Copy `corpus/evidence/sources-r59/w1-results-r54.json` is to be byte-identical, so the pin is this sha. New row S553 is used by `corpus/knowledge/wave-settlement-artifacts-r59.md`, whose claims are structural, not a verdict about r54's seat quality.
- **Admit S554 (tier A, own-work).** Re-opened `.ufo/waves/round-55/w1-results.json` at the same freeze revision on 2026-10-28; sha256 `2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b`. Located quote: `"seats": 64,` (line 5, offset 49; 2 words). Declares 64 seats and carries 64 members, same key set and role vocabulary; copy `corpus/evidence/sources-r59/w1-results-r55.json`. Used by the same entry.
- **Admit S555 (tier A, own-work).** Re-opened `.ufo/waves/round-56/w1-results.json` at the same freeze revision on 2026-10-28; sha256 `19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761`. Located quote: `"seats": 64,` (line 5, offset 49; 2 words). Declares 64 seats and carries 64 members, same key set and role vocabulary; copy `corpus/evidence/sources-r59/w1-results-r56.json`. Used by the same entry.
- **Admit S556 (tier A, own-work).** Re-opened `.ufo/waves/round-57/w1-results.json` at the same freeze revision on 2026-10-28; sha256 `29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1`. Located quote: `"seats": 64,` (line 5, offset 49; 2 words). Declares 64 seats and carries 64 members, same key set and role vocabulary; copy `corpus/evidence/sources-r59/w1-results-r57.json`. Used by the same entry.
- **Admit S557 (tier A, own-work).** Re-opened `.ufo/waves/round-58/w1-results.json` at the same freeze revision on 2026-10-28; sha256 `a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc`. Located quote: `"seats": 64,` (line 5, offset 49; 2 words). Declares 64 seats and carries 64 members, same key set and role vocabulary; copy `corpus/evidence/sources-r59/w1-results-r58.json`. Used by the same entry.
- **Admit S558 (tier A, own-work) — bounded to the settlement-report shape.** Re-opened `.ufo/waves/round-58/evidence/w1-settlement.json` at the same freeze revision on 2026-10-28; sha256 `b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588`. Located quote: `"schema":"mori-wave-settlement-v1"` (single line, offset 79; 1 word); the same object reports `totals` waves 62, members 3153, present 2760, missing 391, states settled 36 / partial 26, unreadable_json 6, ignored_json 1719. This file is NOT a `ufo-wave-results` object: the frozen scanner returns SETTLEMENT_SCAN_FAIL (`results_not_list`, `seats_mismatch`, `lane_bad`, `wave_bad`, `round_bad`), verified below, so the row may not ground results-grammar claims; copy `corpus/evidence/sources-r59/w1-settlement-r58.json`. Used by the same entry.
- **Reject candidate (verified, no row opened): `.ufo/waves/round-53/w1-results.json` as a C2 claim source.** Re-opened at the same freeze revision on 2026-10-28; sha256 `0d644e0fb9c50101a00f47c4ef95e637bb1b1cf1168b5e49bdd19c2f0e584260`. Located quote: `"report_file": ".ufo/waves/round-53/w1/Mo53Fr01.md"` (line 16, offset 12144; 2 words). The frozen scanner scores the file SETTLEMENT_SCAN_FAIL with 67 reasons, every one `member[N]:extra_keys=report_file` (N=0..66), exit 1; the file is also outside the counter's `ARTIFACTS` map, so a claim citing it fails `files:outside`. Flip: a schema-tolerant scanner admitted by a later frozen contract, or a re-derived r53 artifact without the extra member key. Schema drift is reported, not fixed.
- **Non-author spot-check:** pending the independent round-59 closure; this lane has not treated its own seats as non-authors.
```

Row drafts (11 cells, the shape `count-c2.py` `eval_entry` reads: `cells[7]` must be `mined`,
`cells[10]` must be exactly the entry path with no trailing comma):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S553 | mori round-54 w1 settlement results — `.ufo/waves/round-54/w1-results.json` at lane revision 60b3a76ad0524c8978cc51922940be1c8c388915 | own-work | A | the committed `ufo-wave-results` object of the r54 inline spawn handoff (top-level lane/round/wave/seats/results) | `"seats": 74,` line 5 (offset 49); top-level lines 2-4; file 452 lines; copy `corpus/evidence/sources-r59/w1-results-r54.json`, sha256 ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f | The r54 results object declares 74 seats and carries 74 member objects with keys exactly name/agent/output/note, unique names and all ten role tokens | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S554 | mori round-55 w1 settlement results — `.ufo/waves/round-55/w1-results.json` at lane revision 60b3a76ad0524c8978cc51922940be1c8c388915 | own-work | A | the committed `ufo-wave-results` object of the r55 inline spawn handoff | `"seats": 64,` line 5 (offset 49); top-level lines 2-4; file 392 lines; copy `corpus/evidence/sources-r59/w1-results-r55.json`, sha256 2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b | The r55 results object declares 64 seats and carries 64 member objects with the same key set, unique names and all ten role tokens | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S555 | mori round-56 w1 settlement results — `.ufo/waves/round-56/w1-results.json` at lane revision 60b3a76ad0524c8978cc51922940be1c8c388915 | own-work | A | the committed `ufo-wave-results` object of the r56 inline spawn handoff | `"seats": 64,` line 5 (offset 49); top-level lines 2-4; file 392 lines; copy `corpus/evidence/sources-r59/w1-results-r56.json`, sha256 19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761 | The r56 results object declares 64 seats and carries 64 member objects with the same key set, unique names and all ten role tokens | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S556 | mori round-57 w1 settlement results — `.ufo/waves/round-57/w1-results.json` at lane revision 60b3a76ad0524c8978cc51922940be1c8c388915 | own-work | A | the committed `ufo-wave-results` object of the r57 inline spawn handoff | `"seats": 64,` line 5 (offset 49); top-level lines 2-4; file 392 lines; copy `corpus/evidence/sources-r59/w1-results-r57.json`, sha256 29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1 | The r57 results object declares 64 seats and carries 64 member objects with the same key set, unique names and all ten role tokens | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S557 | mori round-58 w1 settlement results — `.ufo/waves/round-58/w1-results.json` at lane revision 60b3a76ad0524c8978cc51922940be1c8c388915 | own-work | A | the committed `ufo-wave-results` object of the r58 inline spawn handoff | `"seats": 64,` line 5 (offset 49); top-level lines 2-4; file 392 lines; copy `corpus/evidence/sources-r59/w1-results-r58.json`, sha256 a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc | The r58 results object declares 64 seats and carries 64 member objects with the same key set, unique names and all ten role tokens | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S558 | mori round-58 w1 settlement report — `.ufo/waves/round-58/evidence/w1-settlement.json` at lane revision 60b3a76ad0524c8978cc51922940be1c8c388915 | own-work | A | the committed `mori-wave-settlement-v1` report of the r58 lane scan (waves, totals, per-wave counts) | `"schema":"mori-wave-settlement-v1"` offset 79 (single-line file); totals waves 62, members 3153, present 2760, missing 391, states settled 36 partial 26; copy `corpus/evidence/sources-r59/w1-settlement-r58.json`, sha256 b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588 | The r58 settlement report records 62 discovered waves and 3153 declared members as a 2026-10-27 scan snapshot, not a current census and not a wave-results object | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |

## 2. Verification performed (all read-only)

Artifacts were never modified. Lane working tree is clean for these paths: working-tree sha256 equals
`git show 60b3a76a:<path>` sha256 equals `git show 8ff344ff:<path>` sha256 for all six artifacts plus
the reject candidate.

1. **Real-scan arm (five committed r54–r58 results files).**
   `python3 tools/mori-settlement-scan.py .ufo/waves/round-{54,55,56,57,58}/w1-results.json` →
   `rc=0`, `verdict=SETTLEMENT_SCAN_OK`,
   `files (round,seats,members,duplicates) = (54,74,74,[]), (55,64,64,[]), (56,64,64,[]), (57,64,64,[]), (58,64,64,[])`,
   `failures=[]`.
2. **Drift arm (reject evidence).** `python3 tools/mori-settlement-scan.py .ufo/waves/round-53/w1-results.json`
   → `rc=1`, `verdict=SETTLEMENT_SCAN_FAIL`, 67 reasons, all `member[N]:extra_keys=report_file`,
   `N` 0 through 66; `"report_file"` occurs 67 times in the file (one per member).
3. **S558 boundary evidence.** Same tool on `.ufo/waves/round-58/evidence/w1-settlement.json`
   → `rc=1`, `SETTLEMENT_SCAN_FAIL`, reasons `results_not_list, seats_mismatch, lane_bad, wave_bad, round_bad`.
   Top-level keys: `ignored_json, lane_root, schema, totals, unreadable_json, waves`; `lane_root` is an
   absolute host path `/home/vgpnk/Projects/shokunin/mori-shokunin`.
4. **Byte-exact quotes at the freeze revision.** For each quote the bytes at the stated offset inside
   `git show 60b3a76a:<path>` equal the quote; offsets: S553–S557 `49` (`"seats": 74,` / `"seats": 64,`),
   S558 `79`, reject `12144`. Word counts: 2, 2, 2, 2, 2, 1, 2 (whitespace split) — all ≤25.
5. **Structural counts (json parse).** Every one of the five results files has exactly the four member
   keys {name, agent, output, note}, zero duplicate names, zero null/empty `output`, zero non-null
   `note`, all ten frozen role tokens, and `seats == len(results)`. Settlement totals as quoted in S558.
6. **Registry state.** `corpus/SOURCES.md` has 325 S-rows, highest `S552`; the table header is
   `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`
   (11 cells), matching `count-c2.py` `eval_entry` (`cells[7]=="mined"`, `cells[10]==ENTRY`).
7. **Frozen-state anchor.** `.ufo/waves/round-59/evidence/c2-at-freeze.txt` records
   `C2=unmet … entry=bad rows=bad pins=bad tree=bad claims=0 files=0 … copy_absent:<six copies>` at
   `60b3a76a`; the six copies therefore do not exist yet and their pins must be the artifact shas above.

No tool was installed or updated for this seat. No counter was modified or run with `--selftest`
(the counters' own selftest arms are not this seat's deliverable); the only executable run against
lane data was the frozen scanner, invoked read-only, as a measurement aid for the reject candidate.

## 3. Findings for the L1 / entry drafter

- **F1 — S558 must be admitted with a scope bound.** The r58 `w1-settlement.json` is a settlement
  *report*, not a `ufo-wave-results` object: the frozen scanner fails it on five reasons. It is still a
  legitimate claim source for its own schema and `totals`, but the entry must not cite it for
  results-grammar claims, and the lesson must not read its `totals` as a current census (it is the
  2026-10-27 scan snapshot; `ignored_json` 1719 and `unreadable_json` 6 are part of that snapshot).
- **F2 — Frontmatter binding is one S-id per `source:` line.** `count-c2.py` scans only the first ten
  entry lines with `source:\s*(S\d+)`, which captures a single S-id per `source:` occurrence. Six rows
  therefore need six `source: S55N` lines inside lines 1–10, plus `verified-at:`, `recheck:` and
  `coverage-map:` — exactly nine lines, leaving one spare. A single line listing all six ids would bind
  only the first and fail `rows:usedby` for the other five.
- **F3 — Reject is real and uniform, not a single-member quirk.** All 67 r53 members carry the extra
  `report_file` key; the drift is schema-wide. Reported, not fixed (contract: "schema drift, reported
  not fixed"). No registry row should be opened for r53; if the L1 prefers the reject to sit inside
  S553–S558 instead, S558 is the only candidate and the reject bullet plus S558 row swap — but then
  the settlement report loses its claim row and the entry may cite at most five copies.
- **F4 — Row pins are artifact shas, not copy shas-yet.** Because the copies are absent at the freeze
  revision, the numeric pins in the Gate text are the artifact sha256 values; the counter's `tree` arm
  requires each copy to be byte-equal to its artifact at the scored revision, which makes copy sha ==
  pin automatically once the copy is created byte-identically.
- **F5 — `used-by` spelling.** The entry path must appear alone in the last cell — no trailing comma,
  no backticks. Hostile tree `t09-usedby-other` and the round-58 routed defect #2 both target this
  exact cell; a trailing comma breaks the `cells[10] != ENTRY` comparison.
- **F6 — The Gate quotes are offset spans, not line spans,** for two reasons: top-level JSON keys carry
  one leading space (a line-span quote would embed an invisible leading space inside a Markdown code
  span), and the settlement report is a single 230411-byte line. Both forms are legal in the frozen
  entry grammar (`line:<n>` or `offset:<n>`); the draft uses offsets consistently for these rows.

## 4. Limits and non-claims

- I did not create the six copies, the entry, the rows, or any lesson text; everything above outside
  this report is a draft for the L1 to place. The registry row drafts are proposals, not edits.
- The Gate draft assumes the 1:1 mapping S553→r54, S554→r55, S555→r56, S556→r57, S557→r58,
  S558→r58 settlement report, i.e. the `ARTIFACTS` order in `count-c2.py`, which is the only definition
  of "the six artifacts" present at the freeze revision. The alternative mapping (S558 = r53 drift)
  is evidenced above but is a different design decision for the L1.
- No non-author spot-check was performed (not this seat's role); the Gate's spot-check line is left as
  pending exactly as round 58 left it.
- No claim is made about axis scores, counter behavior beyond the runs recorded here, or any other
  seat's work. Only `swarm-registry.json` existed in `.ufo/waves/round-59/w1/` when this seat began;
  after drafting, peer reports appeared and two were checked for a conflicting row mapping. No
  conflict: `Mo59Executor44.md:304-309` drafts the same 1:1 mapping (copy 1..6 → S553..S558) with the
  same six sha256 values, and its `Mo59Executor44.md:324-326` independently reports the same
  one-S-id-per-`source:`-line constraint (F2). `Mo59Scribe49.md` does not assign S553-S558. Neither
  peer report drafts a Gate block for these rows; this report is the only Gate draft seen.
- Scratch `/fast/scratch/hyaku/mori-r59/Mo59Scribe48` was created with `mkdir -p`, used for the
  scanner's stdout receipts (`real.json`, `drift.json`, `settle.json`, `rej.json`, `quotes.txt`), the
  key contents of which are transcribed in §2, and then removed.
