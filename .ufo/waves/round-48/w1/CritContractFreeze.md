# CritContractFreeze — round 48 w1 freeze critic

Seat: CritContractFreeze (leaf, no subagents). Scope: attack `contract.md` (P-C1, P-C2)
against `count-c1.py`, `count-c2.py` and the receipts under `evidence/` / `controls/`.

**Verdict: no freeze defects found.** Every P-C1 / P-C2 sentence is the same condition as
the counter code and the receipt labels; before-values equal receipts; controls skip the
claimed work and are unmet; the two claims are causally separable; the named limits are
honest. Four precision observations (O1-O4) are recorded, none of which changes a verdict.

## 0. Environment and frozen bytes

- Entering tip `e5dbac05459887d9597ea5d1da0d8e3d024e0d17` resolves; freeze commit
  `4387cf94b69ddce455051a1ff38e93795c2e6cde` resolves; entering is an ancestor of freeze
  (`git merge-base --is-ancestor` → yes).
- Round-47 baseline `2d85e33d14198d388fd3cda9cc15ec07e57e7a53` resolves.
- For every frozen path (`count-c1.py`, `count-c2.py`, `contract.md`, `v3-spec.md`,
  `controls/stub-always-met.py`, `controls/stub-always-unmet.py`,
  `controls/tool-v2-entering.py`, four copies under `corpus/evidence/sources-r48/`,
  `tools/mori-pin-check.py`): `git show 4387cf94:<path> | sha256sum` == worktree sha256
  == `evidence/freeze-sha256.txt` entry. (Freeze commit stat adds exactly the round-48
  files + copies; `tools/mori-pin-check.py` was not part of the freeze commit and is
  unchanged from entering.)

## 1. P-C1 (calibration) — sentence-by-sentence vs `count-c1.py`

Contract line 24-31, 33-34, 36-44, 45-49. Findings:

- Command/output: contract line 24-25 `python3 .ufo/waves/round-48/count-c1.py --tool
  <tools/mori-pin-check.py at R> --rev R` → `C1=met junk_met=0 honest_unmet=0 real=met
  errors=0 variants=12`, exit 0. Code `main()` (count-c1.py:269-303) parses `--tool`,
  `--rev`, default repo = 4× dirname(__file__) = lane root; `verdict()` (257-266) emits
  `C1=%s junk_met=%d honest_unmet=%d real=%s errors=%d variants=%d rev=%s`; `variants=`
  = `len(results)-1` = 12. Exit 0 iff met, else 1. The contract line omits the extra
  `rev=R` field; the listed fields are exactly the code's fields.
- Junk/honest/real expectations: `VARIANTS` (count-c1.py:186-190) = J1-J8 expect
  `unmet`, H1-H4 expect `met`; `measure()` adds the real run (expect `met`). `verdict()`
  requires `junk_met==0`, `honest_unmet==0`, `real=="met"`, `errors==0`.
- Exit-code semantics: `run_tool()` (201-224) requires `PIN_CHECK=met` ↔ rc 0 and
  `PIN_CHECK=unmet` ↔ rc 1; any other rc or missing `PIN_CHECK` line → `error`;
  timeout → `timeout`. Matches "exit 1 on junk, exit 0 on honest/real".
- Flag constants: `MIN_TALLY=26`, `BASELINE="2d85e33d14198d388fd3cda9cc15ec07e57e7a53"`
  (39-40), passed to the tool as `--min-tally-pins 26 --baseline-rev 2d85e33d…`.
- Crash/setup/timeout classification: per-variant `got` is `error`/`timeout`, never
  `unmet`; verdict fails on any. See O1 for an aggregate-count nuance.
- Variants/anchor: variants are edit functions over R's SKILL.md text (git_show at
  228); `Anchor` raised on missing anchor → `measure` returns err → main prints
  `C1_SETUP` and returns 2 (296-298, 280-283). J7/J8 anchors `(743 lines)` and
  `37fd7c24ff52…` are present in SKILL.md@e5dbac05 (grep counts 1/1).
- Before-value: contract 36-37 names `controls/tool-v2-entering.py` sha256 `9832e38c…`
  = `tools/mori-pin-check.py` at `e5dbac05`, receipt `evidence/control-c1-tool-v2-entering.txt`.
  Verified: control file sha256 `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`
  == `git show e5dbac05:tools/mori-pin-check.py` (identical bytes, `cmp` clean) == worktree
  tool. Receipt shows `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12
  rev=e5dbac05…`, rc=1. I re-ran the frozen counter with the entering-tool control at the
  same rev: byte-identical verdict line, rc=1.
- Controls: contract 39-41. `controls/stub-always-met.py` (2 lines) prints `PIN_CHECK=met`
  and exits 0 unconditionally — it performs no tool work; re-run gave `C1=unmet
  junk_met=8 …` (green on all junk), rc=1, matching `evidence/control-c1-stub-always-met.txt`.
  `controls/stub-always-unmet.py` prints `PIN_CHECK=unmet` exit 1 unconditionally; re-run
  gave `C1=unmet junk_met=0 honest_unmet=4 real=unmet` rc=1, matching
  `evidence/control-c1-stub-always-unmet.txt`. All three controls are unmet when scored
  with the frozen counter.
- Kill rule/selftest pin: contract 42-44. `C1_SELFTEST pass=34 fail=0` — receipt
  `evidence/selftest-c1.txt` shows exactly that; re-run of `count-c1.py --selftest`
  reproduced `pass=34 fail=0` rc=0. (I independently counted 34 arms: 12 apply + 12
  deterministic + names-unique + 8-junk/4-honest + anchor-absent + 6 verdict shapes +
  missing-anchor-setup.)
- Named limits: contract 45-49. Eight junk classes, not class-of-all-junk: true (J1-J8
  only). Honest edits + real registry are part of the predicate: true (H1-H4 + real).
  Counter does not run the tool's own `--selftest`: `run_tool` never passes that flag;
  command is `[python -I -B tool --rev R --repo DIR --min-tally-pins 26 --baseline-rev
  BASE]` (+ optional `--skill`).

## 2. P-C2 (depth) — sentence-by-sentence vs `count-c2.py`

Contract line 63-70, 72-76, 77-80, 81-85. Findings:

- Entry opening/table: contract 63-65. Code `evaluate()` checks `source:`, `verified-at:`,
  `recheck:` in the first 14 non-blank lines (`head`, 119-121) and parses the table via
  `parse_claims()` requiring header `claim | source | quote` (81-82); `< MIN_CLAIMS(8)
  claims → `claims_floor`. See O3 for the "opens with" wording.
- Row contracts: contract 65-69. Code (133-168): source cell must be one `S[0-9]{3,}`
  id; SOURCES row looked up at R (regex `^\s{0,3}\|\s*SID\s*\|`), must have 11 cells,
  URL among the four `COPIES` keys inside cell 1, cell 7 == `mined`, cell 8 ==
  `2026-10-25` (`OPENED`), the entry path among `used-by` (cell 10, split on `,;`);
  quote cell must contain exactly one backticked span, 6-25 words after whitespace
  collapse, unique in table, and `q in norm[url]` where `norm` = tags stripped (`<[^>]+>`
  → space), entities decoded (`html.unescape`), whitespace collapsed (59-62). ≥3 distinct
  sources (`MIN_SOURCES`). Committed copies matched to frozen sha256 via `pins` check
  (104-110); the four digests in `COPIES` equal the four entries in
  `evidence/freeze-sha256.txt` and match the worktree copy files.
- `git show 4387cf94:<path> | sha256sum` vs worktree vs `evidence/freeze-sha256.txt`: 12/12 OK (8 by direct match; the 4 entries whose freeze-list names carry a directory prefix — 3 controls and `tools/mori-pin-check.py` — matched by value: `c6f12be…`, `5b716abc…`, `9832e38c…`, `9832e38c…`).
- Target line format: contract 75-76 `C2=met claims=N located=N quote_missing=0 bad_rows=0
  sources=S source_rows=ok pins=ok provenance=ok` — code (186-190) emits exactly these
  fields (plus `rev=`; `failed=` when unmet).
- Before-value: contract 74 names `evidence/control-c2-donothing.txt`. Receipt:
  `C2=unmet claims=0 … failed=entry_absent,pins rev=e5dbac05…`, rc=1. Re-run of the frozen
  counter at `e5dbac05` reproduced it exactly. (`pins=bad` because the copies were added at
  freeze, after entering; consistent with the contract's `failed=entry_absent,…`
  ellipsis.)
- Controls: contract 77-80. Do-nothing = entering revision (above). The 22 selftest arms
  (`C2_SELFTEST pass=22 fail=0`; receipt + re-run reproduced) cover each listed scenario:
  entry_absent, no_table ("staged entry byte-exact" stand-in, see O4), altered_quote,
  quote_from_wrong_copy, short_quote, long_quote, duplicate_quote, claims_floor,
  sources_floor, row_not_mined, row_opened_other_day, used_by_missing, indented_row_ok,
  code_indented_row_unmet, pin_mismatch, provenance (uncited table id, missing verified-at),
  header_wrong, claim_cell_short, table_inside_fence_unseen, other_entry_path.
- Named limits: contract 82-85. Code checks quote occurrence + row/provenance alignment
  only; it never relates claim cell to quote, never accesses the network, and ignores
  prose beyond the header/table. Docstring lines 19-20 state the same limits.

## 3. Separability

Contract 87-91. `count-c1.py` reads only `SKILL.md`@R (`git show`, line 228) and executes
the tool path; `count-c2.py` reads only the entry, `corpus/SOURCES.md` and the four copies
under `corpus/evidence/sources-r48/`. Neither counter reads the other claim's surface
(tools vs entry/SOURCES/copies), so "either counter can be run with the other claim's
changes reverted" holds.

## 4. Observations (precision notes, not defects)

- **O1** `count-c1.py:258` — `junk_met` counts any junk variant with `got != "unmet"`,
  so a crash/timeout on a junk variant increments both `junk_met` and `errors`. The
  contract sentence "crash/setup/timeout is errors, never unmet" holds in the per-variant
  `got` column, and the verdict requires both counters zero, so the outcome is identical
  to the contract's reading.
- **O2** The counter measures the tool bytes found at the `--tool` path (disk), not bytes
  fetched at rev R; `"<tools/mori-pin-check.py at R>"` is enforced by process (tool
  committed before measurement), not by the counter. At freeze the control is byte-identical
  to the tool@e5dbac05, so the before-condition coincides.
- **O3** P-C2 "opens with `source:` lines, `verified-at:` and `recheck:`" is implemented as
  "present within the first 14 non-blank lines" (`head`), not literally at the file start.
- **O4** The C2 selftest arm labeled "staged entry byte-exact (no claims table)" uses a
  synthetic 3-line stand-in entry (count-c2.py:287), not the literal staged entry bytes
  from the read-only `merge/mori`; the reason isolation is preserved.

## 5. Commands run (evidence)

All read-only over git; scratch under `.scratch/r48-CritContractFreeze/`, TMPDIR set to it;
no tracked files modified (final `git status --porcelain` shows no tracked changes; a
transient ` M tools/mori-pin-check.py` observed mid-session cleared and the file sha256
stayed `9832e38c…` — attributed to concurrent wave-seat activity).

- `python3 .ufo/waves/round-48/count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0`, rc=0.
- `python3 .ufo/waves/round-48/count-c2.py --selftest` → `C2_SELFTEST pass=22 fail=0`, rc=0.
- `… count-c1.py --tool .ufo/waves/round-48/controls/tool-v2-entering.py --rev
  e5dbac05… --scratch <scr>/enter` → `C1=unmet junk_met=8 honest_unmet=0 real=met
  errors=0 variants=12 rev=e5dbac05…`, rc=1 (matches `evidence/control-c1-tool-v2-entering.txt`).
- `… count-c1.py --tool controls/stub-always-met.py …` → `C1=unmet junk_met=8 …` rc=1
  (matches `evidence/control-c1-stub-always-met.txt`).
- `… count-c1.py --tool controls/stub-always-unmet.py …` → `C1=unmet junk_met=0
  honest_unmet=4 real=unmet …` rc=1 (matches `evidence/control-c1-stub-always-unmet.txt`).
- `python3 .ufo/waves/round-48/count-c2.py e5dbac05…` → `C2=unmet claims=0 … failed=entry_absent,pins`
  rc=1 (matches `evidence/control-c2-donothing.txt`).
- `git show e5dbac05:tools/mori-pin-check.py | sha256sum` =
  `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` = worktree tool =
  `controls/tool-v2-entering.py` (cmp identical).
- `git show 4387cf94:<path> | sha256sum` vs worktree vs `evidence/freeze-sha256.txt`: 11/11 OK.

Report: .ufo/waves/round-48/w1/CritContractFreeze.md
