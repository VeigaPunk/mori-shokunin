# R48RevQuality — QUALITY.md criteria 125–128 attack (mori round 48, wave w2)

Attacked: `corpus/QUALITY.md` criteria **125, 126, 127, 128** at landed tip
`e4dfff32d4f97c7ef250e9a7538fa75d4f284492` (freeze `4387cf94b69ddce455051a1ff38e93795c2e6cde`,
entering `e5dbac05459887d9597ea5d1da0d8e3d024e0d17`). For each: (a) is it backed by the lesson
row it cites, (b) does its Check command exist and run, (c) is each "Shown able to fail" claim
true (arm present and/or receipt re-run), (d) does it claim anything the landed tool or counter
does not do.

**Verdict: all four criteria HOLD.** No class broken. Two borderline notes at the end
(125's D7 residual is disclosed but the test that would close it exists in the w1 report as a
suggestion only; 128 row-2 claim leans on the sentence after its quote — judged within
tolerance, recorded).

Lane tool runs used `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48RevQuality`.
All git operations read-only (`show`, `ls-tree`, `grep`, `rev-parse`, `log`). No pacman
(paused host-wide), no installs; tooling authorization unused.

## 125 — "A pin is calibrated only when the checker can see it, and it counts what it cannot see." — **HOLDS**

- **Lesson backing — true.** `corpus/lessons/round-48.md` M2 records the entering v2 checker
  printing `PIN_CHECK=met` on eight junk edits with receipt
  `evidence/control-c1-tool-v2-entering.txt` (`junk_met=8`); M3 lists the CritJunkClasses
  classes (D1 decoy digest, D2 continuation tally, D5 other-cell tally, D18 un-backticked
  tally) and the R9/R10 fix mapping, and names D7 as not closed — exactly what the criterion
  claims and disclaims.
- **Check — runs, and `hidden=0 unparsed=0` is real.**
  `python3 tools/mori-pin-check.py --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --baseline-rev e5dbac05459887d9597ea5d1da0d8e3d024e0d17`
  → `PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0
  rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=e4dfff32… baseline=yes`, exit 0
  (every printed `pin …` line `state=match`). `hidden` and `unparsed` are genuine
  counters incremented at `tools/mori-pin-check.py:489–527` and fatal in the `met`
  conjunction at :595–598 — not decorative fields.
- **"every digest binds to the nearest preceding in-tree path of its own cell" — verified in
  code.** Full digests: :584–594 binds `HEX_RE` hits via `_nearest_in_tree_path(st[:dm.start()],
  root)` (:299–303 = last `PATH_RE` match before the digest inside the same cell, resolved
  through `inside_tree` with `realpath` containment). Truncated digests: same helper at
  :314–320 (R6/R10). Selftest arm `r10_digest_decoy_file_in_other_cell` kills the
  elsewhere-in-row decoy.
- **"Shown able to fail" — every named arm exists and passes as a failing arm.**
  `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=60 fail=0`; the
  criterion's named arms printed: `r2_hidden_row_outside_table` (hidden=1),
  `r9a_tally_in_pinned_values_cell` (hidden=1), `r9b_continuation_line_tally` (hidden=1),
  `r9c_tally_outside_backticks` (unparsed=1), `r10_digest_decoy_file_in_other_cell`
  (mismatches=1), `r10_trunc_digest_decoy_file_in_other_cell`, plus
  `r10_digest_binds_to_nearest_preceding_path` as the positive control.
- **J1–J8 under the entering tool (junk_met=8)** — frozen receipt
  `evidence/control-c1-tool-v2-entering.txt` carries it at `e5dbac05`; re-run at the landed
  rev below (126 section) reproduced `junk_met=8` on the entering-tool copy.
- **Not covered: D7 — disclosed accurately.** `w1/CritJunkClasses.md` D7 exists (row names
  instrument A in entry cell, self-test cell runs B; table :328 shows it `met` under v2 and
  `no` under every R1–R10 column). The criterion's disclaimer matches the lesson M3 fix note
  ("a rule turns four legitimate mutant-command rows red"). Honest residual, not an overclaim.

## 126 — "A calibration counter scores named junk edits and honest edits together, and the real registry is one of the honest cases." — **HOLDS**

- **Lesson backing — true.** M2: "a counter that only wants `unmet` on junk is met by a tool
  that rejects every row" is the stub-always-unmet point; the counter's VARIANTS tuple is
  8 junk (`expect=unmet`) + 4 honest (`expect=met`) + `real` (count-c1.py:186–190), verdict at
  :257–266 requires `junk_met=0 honest_unmet=0 real=met errors=0` — real registry scored as an
  honest case, as claimed.
- **Check — runs, prints the claimed line.**
  `python3 .ufo/waves/round-48/count-c1.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492`
  → `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32…`, exit 0
  (all 12 variants + real; per-variant lines J1–J8 `got=unmet`, H1–H4 and real `got=met`).
- **Harness-leak check — present and real.** `w1/CritC1Counter.md` F1 documents both leak
  channels (`variant-J*/H*` basename of `--skill`, `TMPDIR=…/c1-<name>-*`). The landed tool
  contains no branch on either: `grep -nE "variant|basename|environ" tools/mori-pin-check.py`
  hits only :406 (it *sets* `TMPDIR` to its own `pin-tmp-*` dir for child commands) and :707
  (a selftest fixture script). `--skill` is opened only for content (:665); no name check.
  Residual honesty: the *harness* still leaks both channels (count-c1.py:238,247 unchanged) —
  the criterion claims only that the tool doesn't exploit them, which holds.
- **"Shown able to fail" — all three receipts re-run at the landed rev, all reproduced:**
  - `controls/stub-always-met.py` → `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0`, rc=1
    (matches `evidence/control-c1-stub-always-met.txt`).
  - `controls/stub-always-unmet.py` → `C1=unmet junk_met=0 honest_unmet=4 real=unmet errors=0`, rc=1
    (matches `evidence/control-c1-stub-always-unmet.txt`).
  - `controls/tool-v2-entering.py` → `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0`,
    rc=1 (matches `evidence/control-c1-tool-v2-entering.txt` — same byte-identical tool
    `9832e38c…`, same anchors present in SKILL.md at `e4dfff32`).
  - Counter selftest: `C1_SELFTEST pass=34 fail=0` (verdict arms incl.
    `verdict_one_junk_green`, `verdict_error_not_unmet`, `missing_anchor_is_setup`).

## 127 — "Instruments carry no absolute host path, and the count of those that do is stated with its scope." — **HOLDS**

- **Lesson backing — true.** `corpus/lessons/round-48.md` Gate/considerthese paragraph cites
  `considerthese/2026-10-25.md` suggestion 2 ("Keep a host-path portability list… The count is
  13 files today", operator-authored, file dated 2026-10-25) and records the same 3 + 10 = 13
  reproduction plus the wider 395. Verified directly:
  - tools/ at `e5dbac05` → exactly 3: `mori-blind-check.sh`, `mori-misroot-sweep.py`,
    `mori-round17-context-check.py`; identical list at `2d85e33d` and at the landed tip —
    all three predate the criterion (present at `e5dbac05`).
  - rounds 40–43 top-level wave instruments at `e5dbac05` → **10** (reproduced).
  - all tracked `.py`/`.sh` under `tools/` + `.ufo/waves/round-*/` at `e5dbac05` → **395**
    (reproduced).
- **Check — runs.** `git ls-tree -r --name-only <rev> -- tools/ | grep -E '\.(py|sh)$' |
  xargs git grep -l -F '/home/vgpnk' <rev> --` → the same 3 files at `e5dbac05`,
  `2d85e33d`, and `e4dfff32` ("lists only files that predate the criterion (3 at e5dbac05)"
  — true, and the landed tip adds none).
- **"a new instrument adds none" — true.** `count-c1.py`, `count-c2.py`,
  `tools/mori-pin-check.py`, `tools/mori-unlanded-check.py` contain no `/home/vgpnk`; the only
  `.py`/`.sh` under `.ufo/waves/round-48/` at the tip carrying one is `build-w1-spec.py`.
- **"Shown able to fail" — true.** The same command run over `.ufo/waves/round-48/` lists
  `e4dfff32:.ufo/waves/round-48/build-w1-spec.py` (a wave builder, matching the lesson's
  parenthetical). **Not covered** (the 10 and the 395 stay unrepaired history) is stated, not
  hidden.

## 128 — "A depth entry carries a located quote per claim, and the counter proves location, not entailment." — **HOLDS**

- **Lesson backing — true.** Gate (the admit bullet for the rewritten
  `corpus/knowledge/quota-observability-r48.md`, 15 rows) + "Wave 1 — integrated findings":
  `w1/CritC2Counter.md` shows eight 8–10-word `<script>`/JSON fragments score
  `C2=met claims=8 located=8` (receipt quoted in the report, :16–20);
  `w1/CritEntryRisk.md` §2 shows six claim/quote pairs a reader rejects (P1 overclaim, P2
  negation context, P3 example scope, P4 other filesystem, P5 vendor page, P6 number from an
  example) — the six rejection classes the criterion's reviewer checklist names.
- **Check — runs, `met`.**
  `python3 .ufo/waves/round-48/count-c2.py e4dfff32d4f97c7ef250e9a7538fa75d4f284492`
  → `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok
  provenance=ok`, exit 0. "Counter proves location, not entailment" is the counter's own
  stated limit (count-c2.py docstring :19–20) and the entry says so in prose (:20–22).
- **Reviewer re-open — done for all 15 rows** against the normalised committed copies:
  every quote located verbatim; claims match or under-claim their quote. Spot-verified
  contexts: xfs_quota item 3 block (rows 1–2 — the enforcement-switchable half of row 2's
  claim is the sentence immediately after the quote, contiguous: "However, it is possible to
  turn on/off limit enforcement any time quota accounting is turned on"), items 8–9 (rows 3, 5),
  §USER COMMANDS `quot` (row 7); quotactl.2 DESCRIPTION grace-period sentence (row 9 —
  "after this" refers to the grace period named in the same sentence), ERRORS ESRCH (row 10),
  `quotactl_fd` NOTES (row 11 — mount-point claim is verbatim context); errno.h:107 `#define`
  (row 12 — 122 comes from the define, not the comment → not a P6); Aliyun `dd` output @
  offset 5042, `subPath` content, `管理配额` console text (rows 13–15 — claims scoped to "the
  vendor's … page", not asserted as Linux facts → not P5). No row hits a rejection class.
- **"Shown able to fail" — true.** `count-c2.py --selftest` → `C2_SELFTEST pass=22 fail=0`;
  the three named arms are present in code and pass: `altered_quote_unmet` (:290–292),
  `quote_from_wrong_copy_unmet` (:293–295), `used_by_missing_unmet` (:315–316). Receipt
  `evidence/control-c2-donothing.txt` exists and shows
  `C2=unmet … failed=entry_absent,pins` rc=1.
- **Not covered — stated and real.** The counter's `normalise()` still strips tags only
  (script/JSON bodies remain searchable — the F1-of-128 attack persists by design), and
  entailment is excluded by the contract itself. Both disclaimers match the code.

## Residual risk / verification gaps

1. **126 harness leak persists at the harness level** (frozen, out of attack scope): a future
   tool could still key on `variant-J*` basenames or `c1-<name>-*` TMPDIR. The criterion only
   requires the landed tool not to — verified.
2. **125's D7 stays uncovered by design**; the criterion discloses it. If a future registry
   row splits entry/self-test across instruments, nothing catches it.
3. **128 row 2** ("Accounting is chosen at mount time, while enforcement can be switched
   afterwards") draws its second clause from the sentence *following* the quoted one — within
   the criterion's "around the quote" tolerance; recorded, not counted against HOLD.
4. Verification method note: absence of a variant/scratch-name branch in the tool was shown
   by code inspection (`grep` of `variant|basename|environ|__file__` + reading the `--skill`
   and `run_cmd` paths), not by running a decoy-named skill file — the counter's own control
   set covers the classes and all reproduced.
