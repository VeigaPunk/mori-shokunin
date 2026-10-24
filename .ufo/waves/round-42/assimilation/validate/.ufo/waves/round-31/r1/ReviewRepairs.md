# ReviewRepairs — round-30 routed repairs (D1–D9) at round-31 tip

Seat: non-author checker, residual wave r1. Judged committed bytes at `a29f3e3f7f7259afb07df29c5ee8f68882712e96`
only (`git show` into `/fast/scratch/hyaku/mori-r31/ReviewRepairs/`). Disposition table:
`a29f3e3f:corpus/lessons/round-31.md`, "Routed defects (round-30 closure §7) — disposition". Assignment:
`corpus/lessons/round-30-verifier-spotcheck.md` §7 D1–D9.

## Verdict: all nine routed repairs verified — 9 closed, 0 partly, 0 not closed. No actionable finding.

| Defect | Disposition claim | Verdict | Evidence |
|---|---|---|---|
| D1 blindness gate parser | fixed as C2: `tools/mori-blind-check.sh`; r30 gate untouched; no CaseA210c missing-list expectation | closed | below |
| D2 A1 silent loosening | M2, citing QUALITY 25; A3 named as no precedent | closed | below |
| D3 QUALITY 93 cannot fail | QUALITY 94 supersedes by name; 92 recorded unmet | closed | below |
| D4 "reports its version"; S159/S120 | corrected in place at both mentions + appended section | closed | below |
| D5 coverage-map row | `corpus/README.md:44` | closed | below |
| D6 X1/X2 dry-run flips | pinned; tip `PASS 2/2`, r30 base `FAIL 0/2` | closed | below |
| D7 LOG for `713be294` | appended | closed | below |
| D8 stale SCORECARD counts | appended corrections | closed | below |
| D9 redacted tokens | noted; no history rewrite | closed (note-only) | below |

## Findings by severity

None. Each item verified against primary evidence; details below.

## Per-item evidence

### D1 — closed

- `a29f3e3f:tools/mori-blind-check.sh` exists (366 lines). Parser: the files-opened block opens only on a heading
  containing `files opened`/`opened files` or a `files opened:`/`opened files:` label (`:131-138`), and any heading
  (`#{1,6}`) closes it (`:132-136`) — the round-30 read-past-the-list defect (`CaseR30a.md:105` closing sentence
  parsed as an entry) cannot recur by construction. Every forbidden entry line appends its own
  `path:line:writer-forbidden-opened-path` violation (`:162-167`); hits are printed all, sorted (`:209-215`), not
  first-per-file. Missing-list fires once per file at `:1` (`:204-207`).
- Self-test expected set (`:223-236`) names only `CaseR31*` fixtures; `grep CaseA210c` → absent. No locked
  `CaseA210c.md|writer-missing-files-opened-list` false positive. `c2-fixtures.json:52` records the A210c
  label-form-list shape with only a forbidden-path expectation ("a label-form list counts as a files-opened list").
- Receipts: `evidence/c2-after.txt` — F02 `exact hits=2`, F10 `exact hits=2` (every-hit semantics), `exact=16/16`,
  `C2=met`, exit 0. `evidence/c2-tool-selftest-and-r30.txt` — `--selftest` PASS exit 0; on the round-30 writer wave
  at `5c99f2d4` it prints `scanned=4 blind_violations=3`, the three `writer-missing-files-opened-list` hits, and no
  longer flags `CaseR30a.md:105`. Old gate's one-hit-per-file behaviour confirmed by `evidence/c2-controls.txt:13`
  (do-nothing port: `F02 want=[(3,…),(4,…)] got=[(3,…)]`).
- Round-30 gate bytes untouched: `git diff --stat a12c68ae a29f3e3f -- .ufo/waves/round-30` is empty.

### D2 — closed

- M2 (`a29f3e3f:corpus/lessons/round-31.md` `## Mistakes`) names the class (undisclosed-contract-relaxation) and
  cites QUALITY 25 at `corpus/QUALITY.md:50` — verified: line 50 is criterion 25 "narrowing is an explicit
  correction, not a silent edit".
- Line citations verified: `a66751b1:.ufo/waves/round-30/contract.md:32-36` is condition 3 with "exactly one";
  `05db57ed:.ufo/waves/round-30/contract.md:124` is "nothing is narrowed" inside the A1 preamble; `:136-137` holds
  "A case id may occur in more than one eligible file only when every copy's `inputs` and `expect` are identical"
  inside added 3a text — the relaxation is real. `round-30-verifier-spotcheck.md:38-39` identifies the original
  contract; `:34-37` records the relaxation; `:179-181` is D2. A3 (`55f9a694`) is explicitly named "not a precedent
  for any later amendment", matching the spotcheck's instruction.

### D3 — closed

- `a29f3e3f:corpus/QUALITY.md` row 94 (tail): "Supersedes criterion 93 (routed D3 … criterion 93 stays as written)" —
  names 93, appended as a new row per LEARNING, 93 not rewritten.
- Can fail: the check is mechanical (receipt ancestor of freeze, receipt's gate blob equals `F:<gate>`, one
  non-author adjudication line per hit, two-forbidden-entries replay prints two hit lines). "Shown able to fail"
  cites two real failures: round-30 freeze `db1ec469` has no adjudicated receipt of the freeze blob (consistent
  with `round-30-verifier-spotcheck.md:176-183`), and the round-30 parser prints one hit for two forbidden entries —
  verified at `evidence/c2-controls.txt:13` (`F02 diff want=[(3, …), (4, …)] got=[(3, …)]`).
- Criterion 92 recorded unmet at the round-30 tip inside row 94 (`limit_stated=no`); the wave-1
  `w1/ScoutQuality92.md` receipt exists and reports the re-run (`pinned=8 … frozen=yes`, rc 1 per disposition; the
  report discusses `pinned=8` conjuncts and 92's mechanism).

### D4 — closed

- `grep -n -i version` on `a29f3e3f:corpus/knowledge/earlyoom-invocation-scope-r30.md`: no unqualified "reports its
  version" anywhere. In-place text `:54-55` now reads "reports the last version line inside that retained scope
  (`earlyoom.version` is `null` when no version line is at or after the stamp; round-31 …)". The only other
  "reports its version" occurrence is inside the appended `## Round-31 correction (routed D4 …)` (`:141-153`)
  quoting the old text — a record, not an assertion.
- S159/S120 split: `:23-26` names both ("S159 is the commit that introduced the line … `Restart=always` … and S120
  is the [shipped `earlyoom.service.in`]"); the correction section cites S120 as `earlyoom.service.in` v1.9.0
  carrying `Restart=always` at `:17` (`corpus/SOURCES.md:126`) — matches the spotcheck's S120 row exactly.

### D5 — closed

- `a29f3e3f:corpus/README.md:44` is a coverage-map row for `knowledge/earlyoom-invocation-scope-r30.md`, scope text
  naming version-line segmentation, the active-enter bound, earlier-invocation/dry-run separation, and grounds
  `S118–S120, S122, S154–S160` — consistent with the entry's own source line.

### D6 — closed

- Ran myself: `python3 -I -B <scratch copy of a29f3e3f:tools/mori-oom-killers.py> --selftest --cases <fixture>` —
  `cases-r31-dryrun-flips.json` PASS 2/2 exit 0; all older fixtures pass: `cases.json` 32/32, `cases-supplementary.json`
  32/32, `cases-a2.json` 30/30, `cases-a2-r29.json` 24/24, `cases-a2-r30.json` 8/8. No regression.
- `git diff --stat a12c68ae a29f3e3f -- tools/fixtures tools/mori-oom-killers.py`: only
  `cases-r31-dryrun-flips.json` +85; no older fixture and not the tool changed.
- The two cases `r31-x1-stopped-dryrun-escalation-acted` / `r31-x2-stopped-prestamp-dryrun-send-acted` pin
  CriticHarmAxes X1/X2 at the tip verdict `KILLER_ACTED` (`frozen_with` names `.ufo/waves/round-30/w2/CriticHarmAxes.md`
  X1/X2; `note` states unreachability from stock earlyoom 1.9.0). Lane receipt `evidence/d6-dryrun-flips.txt`:
  tip tool `PASS 2/2` exit 0; round-30 base tool (`58b61681`) `FAIL 0/2` exit 1 — the flips are pinned, not
  silently consistent. Named in the lesson disposition row and LOG.

### D7 — closed

- `LOG.md` appended section "appended correction to the round-30 log (routed D7)" names
  `713be294669272b8b29e9a8cd60c5313704a2ee1`, records subject (36 seats: 18 reviewer, 7 scout, 6 critic,
  4 mutation-tester, 1 sentinel) and the five files. Verified: `git show --stat 713be294` — same subject, same five
  paths (`w1/swarm-registry.json`, `wave2-dispatch.json`, `wave2-run.err`, `wave2-run.json`, `wave2-spec.json`),
  "5 files changed, 1067 insertions(+)". Append-only.

### D8 — closed

- Appended correction 1: the retained round-30 row at `SCORECARD.md:1820` records `count-c1.sh ee61010d` with
  `new_ids=5 new_id_rows=13 excerpts_ok=5/5` (verified — that is the earlier measurement); the correction's cited
  receipt `evidence/tip-c1.txt:1-2,16-18` measures counter at parent `926ac1460c0b9a542725257870f530f98e94e4b1` and
  reports `rows=13 rows_ok=13 new_ids=4 new_id_rows=12 excerpts_ok=4/4 skill_rows=4`, `C1=met`, exit 0 — verified
  verbatim. Correction is true and keeps C1=met.
- Appended correction 2: `contract.md:76-78` (tip blob of the frozen round-30 contract) holds the "(it reports 0 on
  the round-29 writer wave at `d6d5cb0a` …)" parenthetical inside condition 4; A2 text at `:170-172` requires an
  exact expected `(file, rule)` set and excludes the 20 adjudicated false positives; the gate
  `.ufo/waves/round-30/check-blind-wave.sh:172-180` documents exactly nine expected pairs (counted: 8
  forbidden-opened-path + 1 missing-list for A210c, over 8 files) and its self-test at `:217-230` requires
  `scanned=8`, `blind_violations=9`, each expected pair exactly once, and none of the `false_hits` paths. The
  "reports 0" parenthetical is indeed stale; the correction records the inconsistency without editing the frozen
  contract — exactly what was routed.

### D9 — closed (note-only)

- §7 D9 asks only for a note. The disposition row records it ("noted; no history rewrite (operator-owned)").
  Nothing else owed by the lane.

## Residual risks (not defects)

- The new gate reports `writer-missing-files-opened-list` at `<file>:1` regardless of where the list should sit —
  cosmetic; positions for missing-list hits are file-level by design.
- `w1/ScoutQuality92.md`'s exact `limit_stated=no` string is quoted by the disposition/QUALITY 94 rather than
  re-printed in full in the report tail I read; the report does confirm the check mechanism and `pinned=8`.
- QUALITY 94's second can-fail leg cites the old parser's F02 failure — valid as "shown able to fail" for the
  superseding property, and the new tool's own fixture suite also covers the shape (F02 `exact hits=2`).

## Verification gaps

- I did not re-run the C2 counter or the bwrap-isolated A1 scoring (P-C2-A1 judged by other seats); D1 rests on
  `evidence/c2-after.txt`, `evidence/c2-tool-selftest-and-r30.txt`, plus my read of the parser.
- `count-c1-a1.py` / `count-c2-a1.py` controls receipts were not re-executed (out of this seat's scope).

## Tooling

No installs or updates; nothing needed (git, python3, grep/sed already present). No processes left running.
