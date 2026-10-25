# RevSkillRows — w2 review of SKILL.md at T (line 912 repair, Round47 section, two new registry rows)

Seat: RevSkillRows (leaf reviewer, mori round 47 wave w2). Reviewed bytes: `git show
68d66ca53d89be5c34a62f46af7c37449d9f9b63:SKILL.md` (939 lines). E→T diff for SKILL.md is
exactly +28/−1: one replaced line (912) plus the `## Round47` section (lines 914–939,
including the two new registry rows at 938–939). All commands run read-only against the lane;
extracted tool bytes and TMPDIR under `.scratch/r47w2-RevSkillRows/`; no tracked path mutated.

## Verdict summary

Line 912 repaired text: **holds** (every historical claim re-measured). `## Round47` section:
**holds** (prose matches tool source, docstring, receipts and w1 reports). Two new registry
rows: **hold on all 8 cells** (cell counts, verdict maps vs docstrings/source, pinned tallies
vs re-run `--selftest`), with two Low defects at the edges of the verdict-map/write-scope
contract (D1, D2) and two informational notes (O3, O4).

## What holds — evidence

### Line 912 repaired text (accuracy of 265a955c / d72ac167 history)

Resolved: `265a955c` = `265a955cc67be4eae97d2dc5a9338a25f31eb29b` (round-40 instruments),
`d72ac167` = `d72ac167535229d737b9fa844513431d9a12f5ea` (round-41 freeze); both touch
`tools/mori-sources-appendonly.py`.

1. "the round-40 bytes at `265a955c` print `pass=15`" — re-ran the extracted bytes:
   `TMPDIR=<scratch> python3 appendonly_265a955c.py --selftest` →
   `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, exit 0. ✔
2. "the round-41 freeze `d72ac167` added seven arms" — d72ac167's tool prints
   `pass=22 fail=0` (exit 0, re-run); the static case list (9 cases) and dag case list
   (6 cases) are unchanged vs 265a955c; d72ac167 adds `_selftest_r41_dag_cases()` with
   exactly 7 cases (`r41-dag-h, -h2, -z, -z2, -2l-early, -2l-late, -x`). 15+7=22. ✔
3. "and the pin was not updated" — `git show 2d85e33:tools/mori-sources-appendonly.py` is
   byte-identical to d72ac167's (`cmp` clean), and E's `SKILL.md:912` pins
   `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` while E's tool prints 22. ✔
4. Repaired pin matches the live tool: T's tool re-run → `pass=22 fail=0`, exit 0; T's
   line 912 pins `pass=22 fail=0`. E→T delta on line 912 is confined to the self-test cell
   (pin 15→22 + the re-measured provenance note); the P-C11 paraphrase and pinned-values
   cells are unchanged. ✔
5. "re-measured round 47 by `tools/mori-pin-check.py`" — `evidence/v2/skill-v0-frozen.txt`
   and `skill-v1-honest.txt` both show `pin line=912 … MORI_SOURCES_APPENDONLY_SELFTEST`
   (v0: `state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0'`; v1: match). ✔
6. P-C11 paraphrase — verbatim P-C11 at `265a955c:.ufo/waves/round-40/contract.md:119`
   says "the timing line's eligible set is every superseded id present at R — a never-edited
   superseded id's last immutable-cell edit is its first-sighting commit … an edit at a
   commit is a change against its first parent's state only: when the first parent lacks the
   path the commit contributes no edits (a delete-then-re-add contributes no changed event
   …)". Line 912's summary is an accurate compression. "r39 closure routed defects 1–4 and
   lesson findings 2/5" matches the r40 contract headings (line 15 "r39 closure routed
   defects 1–4 + lesson findings"; line 103 "… (r39 w1 findings 2/5)"). ✔

### `## Round47` section (lines 914–926)

- "replaces round 46's row-wide substring counter (`count-repins.py`, retired as a
  calibration proof: it turned green when a stale receipt string moved to another cell,
  `corpus/lessons/round-46.md` M1)" — M1 verified verbatim (row-wide substring tests,
  `mismatches=0` rc 0 with stale-pin strings outside their semantic cells);
  `.ufo/waves/round-46/count-repins.py` still present at T (retired, not deleted). ✔
- Mechanism prose vs v2 source (`git show T:tools/mori-pin-check.py`, 633 lines): pins read
  only from each gate table's `self-test` cell (docstring "Only the self-test cell is read
  for pins"); bound `--selftest` re-run inside a `git archive` export (line 402); digest
  pins are full 64-hex tokens (`HEX_RE = …[0-9a-f]{64}…`, line 82) matched against file
  paths named in the row. ✔
- v2 hardening list — each item found in source and exercised by a named selftest arm:
  bound-command grammar `<interp> [-I] [-B] <tools/… or .ufo/waves/round-N/…> [<rev>]
  --selftest` with no `-c`/`.scratch/`/`..` (`SAFE_PATH` line 91; arms
  `v2_inline_code_rejected`, `v2_scratch_path_rejected`); `rebound` vs baseline binding
  (lines 330–335; arms `v2_rebound_to_other_tool`, `v2_entry_rebound`); all prefix-starting
  output lines must agree (arm `v2_disagreeing_tally_lines`, `v2_stale_echo_line_ignored`);
  unique row names (`v2_duplicate_name`); short row naming `selftest` any case → `unparsed`
  (`v2_hidden_row_and_duplicate`); fenced tables not read (`v2_fenced_example_not_counted`);
  entry column from header (`v2_entry_column_from_header`); digest paths inside the measured
  tree (`v2_digest_path_traversal`). ✔
- "The seven junk variants score unmet under v2 and the honest repair met
  (`.ufo/waves/round-47/evidence/v2/`)" — receipts read: `skill-v1-honest.txt` →
  `PIN_CHECK=met … rc=0`; `skill-v2-oldcopy/v3-fakeecho/v4-weakened/v5-renameprefix/
  v6-deleted/v7-entrycopy/v8-hide+dup.txt` → all `PIN_CHECK=unmet … rc=1` (states
  no_command/mismatch/dropped/unparsed as designed); `skill-v0-frozen.txt` → unmet with the
  stale `pass=15` mismatch at line 912. Exactly seven junk variants. ✔
- "wave-1 seats turned the frozen v1 green on junk edits — CritC1Predicate.md v2/v3/v7/v8,
  SentPinExec.md" — CritC1Predicate marks v2/v3/v7/v8 "**MET — FALSE GREEN**"; SentPinExec
  documents v1 accepting inline `-c` and traversal spans. ✔
- "The round-47 claim itself is scored with the frozen v1 bytes (`git show 63eecf27:…`)" —
  `git show 63eecf27…:tools/mori-pin-check.py | sha256sum` →
  `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`, equal to the
  contract's frozen digest. ✔

### Two new registry rows (lines 938–939)

Both rows parse to exactly 8 cells (split on unescaped `|`; header also 8). ✔

Row `registry pin reconciler (r47, C1)`:

- entry cell — every listed flag exists in argparse: `--rev`/`--root` (mutually exclusive),
  `--repo`, `--skill`, `--min-tally-pins`, `--baseline-rev`, `--timeout`; `--root DIR`
  measures a directory as-is. ✔
- verdict map vs source: `met` conjunction is exactly `mismatches==0 and unparsed==0 and
  no_command==0 and dropped==0 and rebound==0 and duplicate==0 and tally_pins>=min_tally`
  (lines 384–387); finding states emitted: `mismatch`/`unparsed`/`no_command`/`dropped`/
  `rebound`/`duplicate`; setup paths: "need --rev or --root" rc 2, unresolvable revision rc
  2, unreadable baseline rc 2, unreadable SKILL rc 2. ✔
- self-test cell — re-ran `python3 …/pin_check_T.py --selftest` (TMPDIR=scratch):
  `PIN_CHECK_SELFTEST pass=34 fail=0`, exit 0 — equals the pinned tally. ✔
- pinned values — floor `--min-tally-pins 26 --baseline-rev 2d85e33…` matches contract
  P-C1; "line-count pins and truncated digests are not checked" matches the tool (only
  `SELFTEST`-prefixed tally spans and full 64-hex tokens are pins). ✔
- write scope — export + per-run TMPDIR created under `<repo>/.scratch`
  (`mkdtemp(prefix="pin-check-", dir=scratch_parent)`, line 439) and removed on exit
  (`shutil.rmtree` in `finally`, line 472); child TMPDIR under the measured tree's
  `.scratch`, also removed (lines 244–256). ✔

Row `r47 tracepoint catalogue (C2)`:

- entry cell — usage matches the counter docstring: `<rev> [--repo DIR] [--entry PATH]`;
  positional rev must precede flags (usage error otherwise). ✔
- verdict map vs source/docstring: exit 0 met / 1 unmet with `failed=` tags
  `entry_absent, provenance, table, name_mismatch, field_mismatch, callsite_mismatch,
  pins, source_row` (all named in the row's parenthetical) / 2 `C2_SETUP` on usage or
  unresolvable revision. ✔
- self-test cell — re-ran `--selftest`: `C2_SELFTEST pass=13 fail=0`, exit 0 — equals the
  pinned tally. ✔
- pinned values — in-script `PINS` (4 entries) vs recomputed sha256 of T's committed copies:
  `include_trace_events_oom.h 82f04ad4…`, `mm_oom_kill.c 452f1348…`,
  `mm_page_alloc.c 439ae8ec…`, `fs_proc_base.c cef1a2cf…` — all four equal;
  `ROW_ID = "S475"` and entry `corpus/knowledge/oom-tracepoints-r47.md` match the
  constants. ✔
- live run at T: `python3 .ufo/waves/round-47/count-c2.py 68d66ca…` →
  `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0
  pin_mismatch=0 source_row=ok provenance=ok`, exit 0 — the row's met line verbatim. ✔
- write scope "none (read-only `git show`)" — counter runs only `git show`/`git rev-parse`
  (read-only). ✔ (see O4)

## Defects

### D1 (Low) — pin-check's setup-exit contract is broken for `--repo` failures; the row's "2 → PIN_CHECK_SETUP" cell inherits the overpromise (w1 RevPinCheckCode L5, still open in v2)

The docstring promises "Exit: 0 met · 1 unmet · 2 setup" and the row's verdict map cell
promises `2 → PIN_CHECK_SETUP`. But in v2 the scratch setup sits outside the `try`:
`os.makedirs(scratch_parent, exist_ok=True)` (line 438) and
`tempfile.mkdtemp(prefix="pin-check-", dir=scratch_parent)` (line 439) precede `try:` at
line 440, so an unresolvable/unwritable `--repo` dies with a traceback, exit 1, and no
`PIN_CHECK_SETUP` line. Repro (v2 bytes at T):

```
$ TMPDIR=<scratch> python3 pin_check_T.py --rev 68d66ca… --repo /nonexistent-r47w2-revskillrows
  … PermissionError: [Errno 13] Permission denied: '/nonexistent-r47w2-revskillrows'   rc=1
```

The row's enumerated rc-2 conditions (no `--rev`/`--root`, unresolvable revision or
baseline, unreadable SKILL) all do exit 2 (selftest `cli_bad_rev_rc2` PASS), so the cell is
not strictly false — but a setup-class failure outside that enumeration exits 1 with a
traceback, contradicting the docstring's exit contract the row restates. Fails loud, not a
false green. Fix: wrap lines 437–439 in the setup handler and print `PIN_CHECK_SETUP`.

### D2 (Low) — row 1's limits cell omits v2's digest-candidate extension whitelist

The limits cell says "line-count pins and truncated digests are not checked" (the
contract's named limits). v2 additionally restricts digest candidate paths to
`PATH_RE = …\.(?:py|sh|json|md|txt|tsv)` (line 83): a digest pin whose row names only files
with other extensions (`.c`, `.h`, `.jsonl`, … — exactly the extension of the round-47
kernel copies under `corpus/evidence/sources-r47/`) can never match and always measures
`state=mismatch`. w1 `RevPinCheckCode.md` L7 flagged this as "not in the contract's named
limits"; the landed row repeats the contract limits without adding it. Fails safe (false
red, never a false green); no live row is affected today (the four `.c`/`.h` digests live
in count-c2's `PINS`, not in a SKILL digest pin).

### O3 (informational) — citation placement in the v2 sentence

"…and digest paths stay inside the measured tree (w1 `RevPinCheckCode.md` M1/M3/L1 closed
the same round)" — the parenthetical trails the digest-path item, whose motivating finding
is w1 `SentPinExec.md` F2 (probe: digest lookup escapes the tree); M1/M3/L1 map to the
all-prefix-lines-agree, fenced-tables, and entry-from-header items. Also closed but
uncited: M2 (exact-equality matcher) and the escaped-pipe / flag-strip derivations
(selftest arms `escaped_pipe_cell`, `bare_flag_rev_entry`). Ambiguous placement, not a
false claim.

### O4 (informational) — row 2 write-scope shorthand

Row 2 says "none (read-only `git show`)"; the counter also runs `git rev-parse --verify`
(its own docstring: "Read-only: `git show` / `git rev-parse` only"). Both read-only;
shorthand only.

## Residual risk and verification gaps

- I did not re-run the C1 claim command itself (`--min-tally-pins 26 --baseline-rev E` at
  T) — the measurement seat owns the live run; my tally checks are the per-tool selftests
  plus the committed `evidence/v2/` receipts (measured at af2250d8, whose tree equals T for
  the measured files per the assignment; I did not independently diff af2250d8's tree).
- The C2 catalogue's field-level content accuracy (the entry's 8 rows vs the real v7.2
  header semantics) is the Scribe/Mut seats' surface; I verified the counter, its pins and
  its live verdict only.
- `git archive` edge cases (symlinks, `export-ignore`) untested here (w1 RevPinCheckCode
  residual note stands).
- Nothing in scope was left UNVERIFIED: every prose claim I checked reproduced from
  committed bytes, re-runs, or committed receipts.
