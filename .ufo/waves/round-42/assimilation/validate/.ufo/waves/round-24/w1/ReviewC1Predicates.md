# ReviewC1Predicates: claim C1, item R4 (as amended by A4)

Date: 2026-10-22. Seat: MoriR24.ReviewC1Predicates, read-only leaf. No subagent dispatch.
Lane: /home/vgpnk/Projects/shokunin/mori-shokunin.

- Predicate reviewed: R4 as amended by contract amendment A4, commit
  `f38dbbdcd40b9b93aa82ae38a7ef96aed9c49ef2` (`.ufo/waves/round-24/contract.md`, amendment
  text at lines 137-158). The earlier wording ("the commit that first added its dispatch_path")
  is superseded. I checked it only as a comparison.
- Review-time HEAD: `06a7686ed40f53a7455fe526dadf821757bea98a`. The ledger tool bytes
  `tools/mori-dispatch-ledger.py` are identical at base `c725aa37` and at HEAD
  (`git diff --quiet c725aa37 HEAD -- tools/mori-dispatch-ledger.py` exits 0).
- Status: `tools/mori-routed-check.py` does not exist yet (`git cat-file -e HEAD:tools/mori-routed-check.py`
  exits 128). R4 was checked as a specification, against the real ledger tool and against scratch
  fixtures. No R4 code exists to run.

## 1. Short answers

1. **Does `verify` accept `at` in UTC or in local time with an offset?** Yes, both.
   - Committed round-24 row, local `-03:00`: `LEDGER_CLEAN`, exit 0 (real lane, read-only, S16).
   - Fixture row ending in `Z`, same instant: `LEDGER_CLEAN`, exit 0 (S2).
   - Committed round-23 ledger `.ufo/waves/round-23/wave1-ledger.json` at base, eight rows in `Z` form:
     `LEDGER_CLEAN`, exit 0 (S17). This is a real file, not a fixture.
   - Rejected: no offset (naive) and a space instead of `T`. Both give `AT_INVALID`, exit 1 (S3, S4).
     The parser is `tools/mori-dispatch-ledger.py:187-197`.

2. **How should R4 compare `at` with git committer time?** Put both on one UTC clock.
   - Committer time: `git log -1 --format=%ct REV -- <dispatch_path>`. `%ct` is an integer UTC epoch,
     so the timezone of the commit does not matter. Use `%ct` (committer), not `%at` (author).
   - Ledger time: `datetime.fromisoformat(at).timestamp()`. Verify has already rejected naive values.
     Aware datetimes compare by instant, so mixed offsets are safe. Mixed-offset ordering in
     `AT_DECREASING` (line 275) is correct by code reading. I did not test it.
   - Pass when `committer_epoch <= at_epoch`. Because the committer epoch is an integer,
     this is the same as `committer_epoch <= floor(at_epoch)`. The `at` side keeps microseconds.
   - Never compare strings. `"2026-10-22T08:13:00Z" >= "2026-10-22T05:13:57-03:00"` is true, but
     that `at` is 57 s before the commit (S7).
   - Precision limit: git stores whole seconds. A commit and a call in the same second cannot be
     ordered. The `<=` check passes that tie (S6, F5).

3. **Which dispatch file shape does `verify` need: validator run output or `taskCall`?** Either.
   - `verify` and `bind` read committed blobs at REV only (`git cat-file blob REV:path`,
     `tools/mori-dispatch-ledger.py:102-113`). The working tree is never read.
   - The file must parse as JSON with no `NaN` or `Infinity` constants (`_reject_constant`,
     lines 116-117).
   - The payload is the single object with a string `context` and a list `tasks`
     (candidate search, lines 120-148). A candidate under key `run` or `taskCall` wins. Otherwise
     the one candidate anywhere wins. Zero candidates, or two candidates with the same rank,
     give `DISPATCH_FORMAT_INVALID`, exit 2 (S11).
   - Accepted wrappers (S11): the real validator output with a `taskCall` key; the same with `run`;
     a bare `taskCall` object at the root; the object nested under `result.taskCall`; a single
     unknown key; a one-element list. All of them give the same `payload_sha256`.
   - The committed round-24 file `.ufo/waves/round-24/wave1-run.json` is a validator run output
     with a `taskCall` key. It binds to `f3770ceff4a9...`, 36222 bytes, 33 tasks (S10 and S16).
   - Only `context` and `tasks` are hashed (lines 152-157). Other fields in that file are not
     covered (F8).

4. **Exact row shape the L1 must write:** section 3.

5. **Tip after-value under A4.** It holds on the data. The last commit that changed
   `wave1-run.json` is `06d4f4d263` (committer epoch 1792656837, 08:13:57Z). The row's `at` is
   `2026-10-22T05:14:13.926366-03:00` (epoch 1792656853.926366). The margin is 16.926366 s (S16).
   The tool that would print `"held": 4` does not exist yet, so this is a prediction from the data,
   not a measured result.

## 2. Findings, by severity

### Medium

**F1. A4's spec-to-ledger rule has no matching rule.** A4 says every `wave*-spec.json` "has a
ledger whose last row is `started` or `partial`", but it does not say how a spec is matched to a
ledger. Round 24 is unambiguous today: `wave1-spec.json` line 2 is `"wave": "mori-r24-w1"`, and
the ledger rows carry `"wave": "mori-r24-w1"`. Recommendation (my reading; the contract owner
should confirm it): match by the `wave` value. A spec with no matching ledger at REV is red. Every
matching ledger must verify clean and end in `started` or `partial`. Filename-prefix matching
could give a false green.

**F2. Verify's exit 2 must not become the R4 item's exit.** Dispatch and path failures make
`verify` return 2 with status `could-not-evaluate`:
- `DISPATCH_PATH_UNAVAILABLE` for an absent path (S12).
- `TREE_PATH_INVALID` for `../` or an absolute path (S12).
- `DISPATCH_FORMAT_INVALID` for zero or ambiguous candidates (S11).
- `LEDGER_INVALID` for a ledger path absent at REV (S17).

The contract reserves exit 2 for a repo, rev or base that cannot be read (contract lines 31-33).
Recommendation: any verify exit other than 0 marks R4 red for that ledger, with verify's
`finding_ids` as reasons. The routed tool exits 2 only when `git cat-file -e REV^{commit}` fails.

**F3. Verify does not check ordering. Only the new R4 branch can turn the "at precedes dispatch"
mutant red.** S5: a row whose `at` is 57 s before the dispatch commit gives `LEDGER_CLEAN`,
exit 0. The contract's "able to fail" list includes exactly this mutant (contract line 47). The
R4 branch must do the ordering check itself. Never read "verify clean" as "ordered".

**F4. The superseded first-added wording misses a post-call rewrite. A4 must be implemented.**
S10: the dispatch file is committed at epoch 1792600000. The call's `at` is 1792600100. The file
is then edited at 1792600300, and the ledger row is rewritten to the new hash. Verify is clean
(exit 0) because the row now matches. The first-added predicate says PASS. A4's last-changed
predicate says FAIL. Without the rewrite, verify itself is red (exit 1, `PAYLOAD_SHA256_MISMATCH`
and `PAYLOAD_BYTES_MISMATCH`). The gap is therefore only a row rewrite, and A4 closes it. The
implementer must follow A4, not the old text.

### Low

**F5. Same-second tie (residual, cannot be fixed in the tool).** Git commit times are whole seconds;
`at` has microseconds. S6: `at` = commit + 0.3 s gives PASS; `at` = commit - 0.3 s gives FAIL.
Any `at` inside the commit's own second passes. A strict `<` only changes the exact instant
`at` = `ct`.000000. It cannot order events inside one second, because git records no
sub-second commit time. Document it as a limit.

**F6. Mixed-offset string comparison is wrong.** See S7 in section 1. The checker must compare
parsed instants and never strings.

**F7. Verify does not enforce all of the frozen row fields.** S13: a row without `wave`,
`slot_grant` and `refused_text` is clean. S14: a `partial` last row with `started_ids` 0 is clean,
because the `started_ids` check skips `partial` rows (lines 297-298). The frozen format
(`.ufo/waves/round-18/frozen/c3-ledger-format.json`, `row_fields`) lists these fields as required.
The L1 must write them. R4 does not check them either.

**F8. Only `context` and `tasks` are bound.** The hash covers `{"context", "tasks"}` only
(lines 152-157). Fields such as `counts`, `registry`, `policy`, `resumeSends` and `note` in
`wave1-run.json` are not covered. A change to those fields does not unbind a row. The claim
"the dispatch file is bound" must be read as "the task payload is bound".

**F9. One payload per ledger.** Verify takes each dispatch path's identity at REV, once per path
(identity cache, `tools/mori-dispatch-ledger.py:206` and 226-233), and checks every row against it.
A change to `context` or `tasks` after the first row makes every earlier row unbound at every later
REV (S10, v2). A changed payload therefore needs a new dispatch file and a new attempts file.

**F10. Delete-and-re-add after the call counts as a later change.** S9: P (epoch 1792600000)
adds the file, Q (1792600100) removes it, R (1792600200) re-adds the same bytes, and a row has
`at` 1792600150. A4 gives FAIL; first-added gives PASS. A4's "last changed" reading is the intended
one. The L1 must not delete and re-add a dispatch file.

**F11. Naming drift.** The round-24 dispatch file is `wave1-run.json`. The frozen text says
`<wave>-dispatch.json` (`c3-ledger-format.json`, `payload_identity`). Round 18 used
`wave1-dispatch.json`. Verify does not check names. Pick one name for future waves.

### Info

**F12. Self-attestation (residual, already acknowledged by A4).** Both `at` and the committer
date are written by the lane. `GIT_COMMITTER_DATE` sets any date; my fixtures use it. R4 proves
recorded order, not the order the harness observed.

**F13. A4's before-claim, checked. One correction to my earlier draft.** At `c725aa37` with
`--round 23`:
- `wave1-ledger.json`: eight rows in `Z` form, `dispatch_path` `.ufo/waves/round-23/wave1-run.json`.
  Verify is clean (S17), but every row's `at` (2026-10-21T17:03:11Z to 17:24:14Z) is earlier than
  the last change of that file, commit `22772c1` (epoch 1792606259, 18:10:59Z). The rows are
  46.7 to 67.8 minutes early. R4 is red by ordering, as A4 says.
- `wave1-attempts.json`: legacy shape with `utc` keys, no `at`, no `dispatch_path` and no
  `payload_sha256`. Verify exit 1 with `LEGACY_ROW_UNBOUND`, `AT_INVALID` and `STARTED_MISSING`
  (S17). R4 is red by shape.

So the before-value holds. A4's words "round-23 wave-1 ledger rows (`at` 17:03Z–17:24Z)" are
accurate for `wave1-ledger.json` only.

**F14. Tool health.** `TMPDIR=/fast/scratch/hyaku/mori-r24-a2/review-c1-r4/selftest-tmp python3 -I tools/mori-dispatch-ledger.py --selftest`
printed `SELFTEST mori-dispatch-ledger PASS 14/14`, exit 0, at HEAD.

## 3. Exact ledger row the L1 must write

File: `.ufo/waves/round-24/wave1-attempts.json`, a JSON array. The name must end in
`-attempts.json` or `-ledger.json` for A4's glob. The committed row below is the real one from
`4059ffb5e4b81da6f4a1a00056ba8364cac123c8`. Use exactly these eleven keys, and no others:

```json
[
  {
    "attempt": 1,
    "at": "2026-10-22T05:14:13.926366-03:00",
    "wave": "mori-r24-w1",
    "dispatch_path": ".ufo/waves/round-24/wave1-run.json",
    "payload_sha256": "f3770ceff4a97719923f9c0c5c69a56ba2649a638aea9c62c2602cb386c129a2",
    "payload_bytes": 36222,
    "tasks_count": 33,
    "slot_grant": "granted lane=mori wave=r24-w1 seats=33 live=36 pending=0 cap=200",
    "result": "started",
    "refused_text": null,
    "started_ids": 33
  }
]
```

Field rules:
- `attempt`: integer, contiguous from 1 (`ATTEMPTS_NONCONTIGUOUS`, line 267).
- `at`: ISO-8601 with an explicit offset, `Z` or `±HH:MM`. Taken immediately before the call. It must be
  at or after the last-change commit time of `dispatch_path` (R4). Microseconds are fine.
  Uppercase `T` and `Z` are safest; the parser also accepts `t` and `z`.
- `wave`: the spec's `wave` value, here `mori-r24-w1`. Verify does not check it (F7). F1's matching rule needs it.
- `dispatch_path`: repo-relative committed path of the validator output. No `..`, no leading `/`, no
  backslash (`_validate_tree_path`, lines 91-99).
- `payload_sha256`, `payload_bytes`, `tasks_count`: copy from `bind` run at the dispatch commit. Never
  compute them by hand. A one-byte difference gives `PAYLOAD_SHA256_MISMATCH`.
- `slot_grant`: the wave-slot `granted` line for this attempt, or null. Not checked by verify.
- `result`: `refused`, `started` or `partial`. Exactly one row is `started` or `partial`, and it is the
  last row (`STARTED_MISSING` line 291, `DUPLICATE_STARTED`, `STARTED_NOT_LAST`).
- `refused_text`: the exact refusal text for refused rows, else null. Not checked by verify.
- `started_ids`: count of returned agent ids. For `started` it must equal `tasks_count` (line 301).
  For `partial` verify does not check it (F7), so write the true count anyway.

Process, in order:
1. Write the validator output to `.ufo/waves/round-24/wave1-run.json` and commit it. This is the
   dispatch commit. Never edit this file after step 4.
2. Run `python3 -I tools/mori-dispatch-ledger.py bind --repo <lane> --rev <dispatch commit> --dispatch .ufo/waves/round-24/wave1-run.json`.
   Copy `payload_sha256`, `payload_bytes` and `tasks_count` from its output.
3. Capture `at` immediately before the task call. Build the row. Set `result`, `started_ids` and
   `refused_text` from the observed result before committing. The frozen format says rows are
   "appended before the call result is known and completed with the observed result". A pending
   row must not be committed with an out-of-set `result` (`RESULT_INVALID`, line 282).
4. Commit the ledger. Then run verify at that REV. It must print `LEDGER_CLEAN`, exit 0. Then run the
   R4 ordering check with the rule in section 1.2, using the REV's tool bytes
   (`git show REV:tools/mori-dispatch-ledger.py`), so the verifier matches the REV.

## 4. What I ran (read-only toward the lane)

Files read: the godspeed skill; `contract.md` (worktree, plus `git log -p` for amendments A1-A4);
`tools/mori-dispatch-ledger.py` (lines 37-113, 115-349, 544-576, plus a grep for line numbers);
`.ufo/waves/round-18/frozen/c3-ledger-format.json`; `.ufo/waves/round-24/wave1-attempts.json`;
`.ufo/waves/round-24/wave1-spec.json` (lines 1-40 and 18-21 raw); `corpus/lessons/round-23-verifier-spotcheck.md:55-70`.

Git, read-only (`-c core.pager=cat`): `rev-parse`, `log` (with `--format`, `--diff-filter=A`,
`--reverse`, `--merges`, `-1`), `show -s`, `show --name-only`, `show` of blobs, `cat-file -e` and
`cat-file blob`, `ls-tree`, `diff-tree`, `status --porcelain`, `diff --quiet`. Result: the round-24
ledger and dispatch files were touched only by `06d4f4d` and `4059ffb5`. Round-24 path history has no
merges. `tools/mori-routed-check.py` is absent at base and at HEAD.

Verify and selftest, run from the lane with its committed tool:
- `python3 -I tools/mori-dispatch-ledger.py verify --repo <lane> --rev HEAD --ledger .ufo/waves/round-24/wave1-attempts.json`:
  `LEDGER_CLEAN`, exit 0, at the then-HEAD. At 06a7686e it is also exit 0 (S16).
- `--selftest` with `TMPDIR` set to a scratch directory outside `/tmp`: `PASS 14/14`, exit 0.

Scratch fixtures (one in-session Python script, not saved to the lane). Each fixture is a fresh git
repository under `/fast/scratch/hyaku/mori-r24-a2/review-c1-r4/fx-pwdodtmd/`. The script used the lane's
committed tool bytes (`git cat-file blob HEAD:tools/mori-dispatch-ledger.py`, copied to scratch) and
real committed blobs from the lane. Committer dates were set with `GIT_COMMITTER_DATE`:
- S1 committed shape with local offset: clean, exit 0. A4 PASS.
- S2 `Z` form: clean, exit 0. A4 PASS.
- S3 naive `at`: exit 1, `AT_INVALID`.
- S4 space separator: exit 1, `AT_INVALID`.
- S5 `at` 57 s before the dispatch commit: clean, exit 0. A4 FAIL.
- S6 same-second: `+0.3 s` PASS, `-0.3 s` FAIL.
- S7 string versus instant comparison: string says "after" (true), instant says "before" (correct).
- S8 rename into the dispatch path: the rename commit is both the oldest added and the last changer.
- S9 delete then re-add: A4 FAIL, first-added PASS.
- S10 post-call edit: edit without rewrite gives exit 1 (`PAYLOAD_SHA256_MISMATCH`); rewrite gives clean; A4 FAIL; first-added PASS.
- S11 wrapper shapes: section 1.3. Duplicates and missing candidates: exit 2.
- S12 bad paths: exit 2 (`DISPATCH_PATH_UNAVAILABLE`, `TREE_PATH_INVALID` twice).
- S13 missing optional fields: clean, exit 0.
- S14 `partial` with `started_ids` 0: clean, exit 0.
- S15 refusals only: exit 1, `STARTED_MISSING`.
- S16 real lane at HEAD (read-only): A4 PASS; verify clean, exit 0.
- S17 real lane at base (read-only): round-23 attempts exit 1; round-23 `wave1-ledger.json` clean; round-24 attempts exit 2 (path absent).
- A4 before-value (F13), computed with `git log -1 --format=%H %ct c725aa37 -- .ufo/waves/round-23/wave1-run.json`
  (`22772c1`, 1792606259) against the eight `at` values of `wave1-ledger.json`: all eight FAIL.

Caller search, text fallback only (no `lsp` device is available in this seat, so this is not semantic
proof): `SKILL.md:180`, `SCORECARD.md:1141`, `corpus/knowledge/dispatch-ledger-r18.md:3`,
`corpus/lessons/round-18.md:57`, and the tool itself.

Installs and upgrades: none. Versions in use: git 2.56.0, Python 3.14.8.

Writes: this report is the only file I created in the lane. Fixtures and selftest scratch live under
`/fast/scratch/hyaku/mori-r24-a2/review-c1-r4/`, outside the lane.

## 5. Gaps and what I did not run

- The routed tool does not exist. The R4 branch was not executed as code. The rules above are a
  specification, tested against the real verify and against fixtures.
- No mutation run on any R4 branch. The four sandbox mutants are the implementer's job. F3 says the
  "at precedes dispatch" mutant must be tested on the R4 branch.
- No `lsp` device in this seat. Caller coverage is text search only.
- Not verified: harness call times (not observable from git); committer times beyond the lane's own
  commits; R1-R3 and C2.

## 6. Corrections to my earlier draft in this file

- The earlier draft reviewed the pre-A4 wording (first-added). Everything above uses A4 (last changed).
- The round-23 `at` values come from `wave1-ledger.json`, not from `wave1-attempts.json` (F13).
- The early-`at` fixture is 57 s before the commit, not 37 s.
- HEAD moved during the review (`f7eb430c`, then `f38dbbdc`, then `06a7686e`). These results are for
  `06a7686e`. The verify tool bytes are unchanged across that range.
- Two commands listed in the earlier draft were never run: `git show -s` on `c725aa37`, and
  `git cat-file -p HEAD:.ufo/waves/round-24/wave1-attempts.json`. The earlier claim that the round-24
  paths were clean was wrong. They hold untracked peer reports under `.ufo/waves/round-24/w1/`.
  None of those are mine, except this report.
