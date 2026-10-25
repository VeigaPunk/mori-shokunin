# R48ExecRerunC2 — C2 re-run + five in-memory entry variants (round 48, wave 2)

**Attacked:** P-C2 at the landed tip `e4dfff32d4f97c7ef250e9a7538fa75d4f284492` — the frozen
`count-c2.py` counter (sha256 `0055aed1…`, identical at freeze `4387cf94`, entering `e5dbac05` and
the tip), the landed FR2 entry `corpus/knowledge/quota-observability-r48.md`, its SOURCES rows and
the four committed copies under `corpus/evidence/sources-r48/`. Five fresh entry variants were run
through `count-c2.evaluate` in memory.

**Verdict: HOLDS.** The claim command prints `C2=met …` and exits 0; `--selftest` prints
`C2_SELFTEST pass=22 fail=0` and exits 0; three of the five fresh variants are killed
(`quote_missing`, `provenance`). Two survive and are recorded as limits, not as a re-score:
V1 (row removal above the 8-row floor — the predicate's own wording is "at least 8 rows") and
V5 (a quote lifted from `<script>`/JSON text inside the Aliyun copy is still *located*, which is
the predicate's named limit "it does not check that the claim cell follows from the quote",
extended to "the located span need not be page prose").

All commands run with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRerunC2`.
No tracked file was written; the entry text for every variant lived only in memory.

## 1. Claim command (receipt reproduced byte-identically)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=…/.scratch/r48w2-R48ExecRerunC2 python3 .ufo/waves/round-48/count-c2.py e4dfff32d4f97c7ef250e9a7538fa75d4f284492
C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
EXIT=0
```

This matches the pre-existing receipt `.ufo/waves/round-48/evidence/after-c2-at-e4dfff32.txt`
(same line, `rc=0`) character for character. `claims=15` ≥ N(8), `sources=4` ≥ S(3),
`quote_missing=0`, `bad_rows=0`, `pins=ok` (all four copies match their frozen sha256 at R),
`provenance=ok`. The do-nothing control `evidence/control-c2-donothing.txt` still prints
`C2=unmet … failed=entry_absent,pins` at `e5dbac05`, `rc=1` (read, not re-run).

## 2. Counter selftest

```
$ TMPDIR=… python3 .ufo/waves/round-48/count-c2.py --selftest
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
PASS table_inside_fence_unseen_unmet
PASS other_entry_path_unmet
C2_SELFTEST pass=22 fail=0
EXIT=0
```

22 arms, matching the contract's "`C2_SELFTEST`, 22 arms at freeze". Observed mechanism worth
recording: `selftest()` opens the copies from the **working tree** (`open(os.path.join(lane, path))`),
not from a revision; the revision-side pin evidence comes from `pins=ok` in the claim run.

## 3. Frozen instrument bytes

```
$ sha256sum .ufo/waves/round-48/count-c2.py
0055aed101bd60b1267d160520948b8f412753b38c72b6bda17da841734ee561
$ git show 4387cf94b69ddce455051a1ff38e93795c2e6cde:.ufo/waves/round-48/count-c2.py | sha256sum
0055aed101bd60b1267d160520948b8f412753b38c72b6bda17da841734ee561
$ git show e4dfff32d4f97c7ef250e9a7538fa75d4f284492:.ufo/waves/round-48/count-c2.py | sha256sum
0055aed101bd60b1267d160520948b8f412753b38c72b6bda17da841734ee561
$ grep -n count-c2 .ufo/waves/round-48/evidence/freeze-sha256.txt
2:0055aed101bd60b1267d160520948b8f412753b38c72b6bda17da841734ee561  count-c2.py
```

Working tree, freeze and tip agree; `git diff --stat 4387cf94 e4dfff32 -- count-c2.py count-c1.py
contract.md` printed nothing. The predicate was measured with the frozen bytes, not a drifted copy.

## 4. Five in-memory variants (`evaluate`, rev label `R-variant`)

Harness: `.scratch/r48w2-R48ExecRerunC2/variants.py` — loads the frozen counter with
`importlib`, serves `git show e4dfff32:<path>` for every path except the entry, and asserts each
variant text differs from the landed entry before scoring. Each variant was run once; the exit code
mirrors the counter's (0 met / 1 unmet).

```
$ TMPDIR=… python3 .scratch/r48w2-R48ExecRerunC2/variants.py
V1_drop_one_row              C2=met claims=14 located=14 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=R-variant
V1_drop_one_row              EXIT=0
V2_swap_two_sources          C2=unmet claims=15 located=13 quote_missing=2 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=R-variant failed=quote_missing
V2_swap_two_sources          EXIT=1
V3_16th_bogus_quote          C2=unmet claims=16 located=15 quote_missing=1 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=R-variant failed=quote_missing
V3_16th_bogus_quote          EXIT=1
V4_break_provenance          C2=unmet claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=bad rev=R-variant failed=provenance
V4_break_provenance          EXIT=1
V5_script_text_quote         C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=R-variant
V5_script_text_quote         EXIT=0
HARNESS_EXIT=0
```

| # | variant | construction | verdict | class |
|---|---|---|---|---|
| V1 | drop one row | removed the S480 `quotactl_fd ()` row (15 → 14 rows) | **met**, exit 0 | survivor — above the 8-row floor |
| V2 | swap two sources | S479 `quot` sentence and S480 `ESRCH` sentence traded source cells | **unmet**, exit 1, `quote_missing=2` | killed |
| V3 | 16th row, bogus quote | appended a row citing S479 with `this sentence appears in no committed copy of any of the four frozen sources` | **unmet**, exit 1, `quote_missing=1` | killed |
| V4 | break provenance | deleted the `source: S480 — …` line while its three rows stay in the table | **unmet**, exit 1, `provenance=bad` | killed |
| V5 | quote replaced by script text | the S482 failing-write quote replaced by `window.globalData = { nodeId: "477385", website: "cn", language: "zh", }` | **met**, exit 0 | survivor — located span is not page prose |

### V5 detail (the interesting survivor)

- The span is **10 words** (inside 6–25), unique in the table, and `count-c2.normalise` finds it in
  the committed copy at normalised offset 431:
  `located: True`, `table occurrences in entry: 0` before the variant.
- In the raw copy it sits inside a `<script>` block:
  `raw.find('window.globalData') = 2851`, `rfind('<script',0,2851) > rfind('</script>',0,2851)` → `True`,
  context `… <script>\n    window.globalData = {\n      nodeId: "477385", …`.
- Mechanism: `normalise()` strips only tags (`re.sub(r"<[^>]+>", " ", text)`), so script and embedded
  JSON bodies remain in the searched text. The landed entry itself already states the page embeds its
  body twice (rendered text and JSON), so any JSON-escaped or script-embedded copy of a sentence is
  equally locatable — the predicate cannot tell prose from page machinery.

### V1 detail

`claims=14` is still ≥ `MIN_CLAIMS = 8`, so removal of a located row is invisible to the predicate.
This is the predicate as frozen ("at least 8 rows"), not a counter defect: the floor, not an exact
count, is the rule. Recorded so wave 2 does not mistake a 14-row entry for a 15-row one.

## 5. What this does and does not establish

- Establishes: P-C2's counting command is met at the landed tip with the frozen bytes; the counter's
  22 arms all pass; source-swap, bogus-quote and provenance-break variants are rejected with the
  expected `failed=` reason and exit 1; the committed copies pin to their frozen sha256 at R.
- Does not establish: that any claim cell follows from its quote (named limit; V5 shows the located
  span may be script text), that the copies are the live pages today (copies dated 2026-10-25), or
  anything about the entry's prose or boundaries. `--selftest` was read as a receipt, not as part of
  the predicate (contract, named limits).
- Not run: no network fetch, no `git` mutation, no edit to `tools/`, `SKILL.md`, `SOURCES.md`,
  `corpus/`, `LOG.md`, `SCORECARD.md` or any frozen file. No pacman (host-wide pause); no tool was
  installed or upgraded.

## Files

- Written: `.ufo/waves/round-48/w2/R48ExecRerunC2.md` (this report).
- Scratch only: `.scratch/r48w2-R48ExecRerunC2/variants.py`.

## Risks / blockers

- None blocking. Residual limit for the round record: `normalise()` keeps script/JSON text, so a
  future entry could quote page machinery and still print `C2=met`; a wave-3 counter that strips
  `<script>` bodies would close it, but that changes the predicate and cannot re-score this round.
- The pre-existing `.ufo/waves/round-48/__pycache__/` (18:32, `cpython-314`, git-ignored) predates
  this seat; I did not create or remove it.
