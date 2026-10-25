# RevQuality — round 47 w2 — QUALITY.md criteria 123–124 (tail at T)

Seat: RevQuality (leaf, no subagents). T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63`, E = `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`, F = `63eecf2738db96f46b0bd02b1b2dfd66787493d0`.

Method: HEAD == T, but the worktree is dirty (`git status --porcelain`: ` M LOG.md`, ` M SCORECARD.md`, 74 untracked sibling scratch/report files), so every T byte was read via `git show T:<path>`. Before running the tracked tool I verified the worktree bytes equal the T blob (`sha256sum tools/mori-pin-check.py` → `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` = `git show T:tools/mori-pin-check.py`). Frozen v1 bytes verified `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` (matches the contract's frozen sha256). All runs with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-RevQuality`. No repo/jj/git-state mutation, no pacman, no tool installs (none needed).

## Criterion 123 (QUALITY.md:1028-1039 at T) — verdict: holds

1. **Lesson-backed — holds.**
   - `corpus/lessons/round-47.md` M1 (number-drift: `SKILL.md:912` stale `pass=15 fail=0`) and M2 (survivor: v1 false greens) exist at T and match the criterion's rationale; M1's fix cell names QUALITY 123 with "red at `2d85e33` (`mismatches=1`, line 912), green after the one-cell repair"; M2's fix cell names the v2 hardening and "P-C1 stays scored by the frozen v1 bytes".
   - `considerthese/2026-10-25.md` suggestion 1 exists; lines 44-46 carry the cited text ("Add a registry pin check … list any mismatch by line number"), file dated 2026-10-25.
2. **Check command runnable — holds.** Run verbatim as written, plus the contract-floor variant (unpiped, true exit codes):
   - `TMPDIR=… python3 tools/mori-pin-check.py --rev 68d66ca5… --baseline-rev 2d85e33…`
     → `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=1 rev=68d66ca5… baseline=yes`, exit 0.
   - Same + `--min-tally-pins 26` → `PIN_CHECK=met … min_tally_pins=26 …`, exit 0.
3. **'Shown able to fail' receipts exist at the cited paths — holds, and reproduce.**
   - All four matches of the cited glob `.ufo/waves/round-47/evidence/control-c1-*.txt` exist at T (`-donothing`, `-deleted`, `-moved`, `-truncated`).
   - Committed receipts (read at T): donothing → `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 … rev=2d85e33… baseline=yes` with `pin line=912 … prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0'`, rc=1; deleted → `dropped=1` unmet rc=1; moved → `mismatches=1` unmet rc=1; truncated → `pinned='pass=2'` mismatch unmet rc=1.
   - Re-ran all four under the tracked T bytes (v2), unpiped, true exit codes: entering `PIN_CHECK=unmet … mismatches=1` (line 912) rc=1; deleted `dropped=1` rc=1; moved `mismatches=1` rc=1; truncated `mismatches=1` (`pinned='pass=2'`) rc=1. Verdict lines match the committed receipts.
   - Forensics: the committed control receipts' verdict lines lack the `rebound=`/`duplicate=` fields v2 prints (v2 docstring lines 63-64 vs v1 lines 48-49), so they were measured with the frozen v1 bytes. The criterion text does not state which bytes measured them; under both v1 and v2 the controls stay unmet, so the able-to-fail claim is robust to the byte version. Consistent with lesson M2 ("P-C1 stays scored by the frozen v1 bytes").
4. **No criterion without a lesson — holds** (M1, M2 + considerthese suggestion 1).
5. **Rationale history spot-checked first-hand (endpoints):** round-40 bytes `265a955c` `--selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` rc=0; round-41 freeze `d72ac167` bytes → `pass=22 fail=0` rc=0; SKILL.md at `d72ac167` pins `pass=15 fail=0` (line 889 there; line 912 at E — the criterion's line number is the entering-tip line). SKILL.md at T repairs the cell to `pass=22 fail=0` with the re-measured note.

Minor observations (123):

- **O1 (minor, wording):** the criterion's Check command omits `--min-tally-pins 26`, which contract P-C1 and every committed receipt use. Verbatim (floor 1) it still exits 0 at T (28 ≥ 1) and still catches the stale-pin and dropped classes, but it would not catch a registry gutted below 26 tally pins; the floor is enforced only by the contract's P-C1 command and documented in the registry row's pinned-values cell. Not a falsification; a tightening opportunity for the criterion text.
- **O2 (minor, labeling):** `evidence/selftest-pin-check.txt` records `PIN_CHECK_SELFTEST pass=22 fail=0` — the frozen v1 selftest (22 arms; verdict lines without `rebound=`/`duplicate=`). The current tool prints 34 (`pass=34 fail=0`, exit 0 — re-ran; v2 adds twelve arms per lesson M2) and SKILL.md:938 pins `pass=34 fail=0`, which the check command reproduces (run B2 observed line 938 as match). The receipt is v1-era and labeled "Selftests at freeze" in `w1/ScribeScorecardLog.md:120`, but the filename — and neither criterion — says "v1"; a reader pulling it as the instrument's current selftest receipt sees 22 against the pinned 34. Not cited by criterion 123; no action required for the criteria to hold.

## Criterion 124 (QUALITY.md:1041-1048 at T) — verdict: holds

1. **Lesson-backed — holds:** `corpus/lessons/round-47.md` M3 exists and matches (attribution: the staged entry's "exactly three named tracepoints" vs the source's "such as" (S478) and the header's eight (S475); fix cell names QUALITY 124 and the control receipt).
2. **'Shown able to fail' receipt exists at the cited path — holds, and reproduces byte-for-byte in the verdict line:**
   - `.ufo/waves/round-47/controls/control-c2-three.md` exists at T; `evidence/control-c2-three-at-freeze.txt` exists at T and is identical between af2250d8 and T (absent from the af2250d8→T evidence diff).
   - Re-ran: `TMPDIR=… python3 .ufo/waves/round-47/count-c2.py 63eecf27… --entry .ufo/waves/round-47/controls/control-c2-three.md` → `C2=unmet events=8 rows=3 name_mismatch=5 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=bad provenance=ok rev=63eecf27… failed=name_mismatch,source_row`, exit 1 — exactly the committed receipt's verdict line and the criterion's `name_mismatch=5`.
3. **Rationale's "eight" verified from the pinned bytes:** `grep -c '^TRACE_EVENT('` over `corpus/evidence/sources-r47/include_trace_events_oom.h` at T → 8; the counter independently reports `events=8` at F and T.
4. **The entry carries the enumerating command (the criterion's Check):** `corpus/knowledge/oom-tracepoints-r47.md:5` (recheck: `… | grep -c '^TRACE_EVENT('` on a new tag) and :16 ("The count is mechanical: `grep -c '^TRACE_EVENT(' …"). Positive run `python3 .ufo/waves/round-47/count-c2.py 68d66ca5…` → `C2=met events=8 rows=8 name_mismatch=0 … source_row=ok provenance=ok`, exit 0 — matches the claims section and the SKILL row.
5. **No criterion without a lesson — holds** (M3).
6. **Instrument selftest:** `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0`, exit 0 — matches the SKILL.md:939 pin (also observed as a match inside run B2).

Observation (124):

- **O3 (informational):** the Check field is an admission policy, not a runnable command (unlike 123's); the only runnable artifact is the able-to-fail control, which reproduces. Criterion 122 declares this shape explicitly ("this criterion is the admission, not the instrument"); 124 relies on it without saying so.

## Cross-checks (claims context)

- Contract P-C1 scoring command with the frozen v1 bytes at T (`git show 63eecf27:tools/mori-pin-check.py`, sha256 `e3ef425a…`, run from my scratch with `--repo <lane>`): `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 … rev=68d66ca5… baseline=yes`, exit 0 — the claims' C1 calibration reproduces.
- Claims' "af2250d8 tree equals T for every measured file": verified — `git diff --stat af2250d8 T` restricted to `tools/mori-pin-check.py`, `.ufo/waves/round-47/count-c2.py`, `SKILL.md`, `corpus/knowledge/oom-tracepoints-r47.md`, `corpus/SOURCES.md`, `corpus/evidence/sources-r47/`, `.ufo/waves/round-47/controls/` is empty; only `evidence/` receipts were added/updated between the two revisions (after-* receipts gained their T-measured lines; v2 junk receipts' command annotation gained the af2250d8 rev).
- `count-c2.py` is byte-identical F↔T, so the freeze-scored control run used the same counter bytes as the tip.
- Registry: `evidence/after-registry.txt` shows both new rows registered (`REGISTRY=met`, `registered=2 unregistered=0`, 8 cells each, entry resolves, `--selftest` argv branch).

## Residual risk / verification gaps

- The "from round 40 to round 47" staleness span was verified at its endpoints and at E (r40 bytes → 15; r41 freeze bytes → 22; r41 SKILL pin `pass=15` at line 889; E pin at line 912). Intermediate rounds r42–r46 were not exhaustively re-derived by this seat; `w1/RevPinHistory.md` is the cited measurement for the span.
- The 18 junk-variant receipts (`evidence/v1-junk/`, `evidence/v2/`) were not all re-run by this seat; one v2 receipt read (`skill-v2-oldcopy.txt` → `no_command=1` unmet) plus the v2 selftest arms cover the class. The criteria's cited sets (`control-c1-*`, `control-c2-three`) were fully verified.
- The pin-check tool's export cleanup was verified on normal and setup-error exits (a `--rev no-such-rev` run left the `.scratch/pin-check-*` count unchanged; transient dirs observed mid-flight all disappeared after their runs completed). A SIGKILL mid-run would leave an export — the docstring's "removed on exit" holds only for non-killed exits.
- Exit codes of my first piped invocations (A/B/C/D/I) were masked by `grep` in my own harness; every decisive number in this report comes from the unpiped re-runs (A2/B2/C2/D2-*/E2/I2; F/G/H were unpiped from the start).

## Bottom line

Both criteria hold: lesson-backed, check commands runnable with the claimed verdicts and exit codes, able-to-fail receipts present at the cited paths and reproducible under both the frozen v1 and the tracked v2 bytes, and neither criterion lacks a lesson. Defects found: none that break a criterion; three minor observations (O1 floor omission in 123's Check command, O2 v1-era selftest receipt labeling, O3 124's Check is policy-only).

Report: .ufo/waves/round-47/w2/RevQuality.md
