# Round 27 wave 1 — CriticC2Counter: attack on count-c2.sh before any data exists

Seat: MoriR27.CriticC2Counter (critic, leaf). Target: `.ufo/waves/round-27/count-c2.sh` at 761b4cd
(sha256 `af434082559dca87c3a8546e7322ba314153ca3e9649cdf24176eb8e396185e8`; unchanged at 5fa0a00:
`git diff --stat 761b4cd HEAD -- .ufo/waves/round-27/count-c2.sh` printed nothing). The counter is frozen. This report
lists gaps and the hand checks the closure needs. It does not propose a counter edit.

## Verdict in one paragraph

The counter is fail-closed on the paths it was written for: a bad revision, a missing file, a failing self-test
summary line, a delete and re-add, and a merge that adds the file. It is **fail-open on eight paths** that
let a cases file pin none of the ten A2 rules, or let a failing self-test or a changed file still read
`C2=met`, exit 0. Two of these need no tool change at all: rule tags that do not exercise the rule (F1) and a
forged PASS line in a case id (F3). The `C2=met` line alone MUST NOT be accepted. The closure must run the
hand checks H1–H6 at the end of this report.

## Runs of the real counter (lane, committed bytes)

| Revision | Output | Exit |
|---|---|---|
| `fc09f96c` | `a2_cases=0 a2_rules_covered=0/10`, `C2=unmet` | 1 |
| `deadbeef` | `bad_rev` | 2 |
| `761b4cd` | `a2_cases=0 a2_rules_covered=0/10`, `C2=unmet` | 1 |
| `5fa0a00` (lane HEAD) | `a2_cases=0 a2_rules_covered=0/10`, `C2=unmet` | 1 |
| no argument / two arguments | `usage: count-c2.sh <rev>` | 2 |

Command: `bash .ufo/waves/round-27/count-c2.sh <rev>; echo exit=$?`, run from `/tmp` and `/`. The `fc09f96c` row
matches `.ufo/waves/round-27/evidence/c2-before.txt:3-5`. The run is saved at
`/fast/scratch/hyaku/mori-r27/CriticC2Counter/run-baseline.txt`.

## Sandbox method

All scenarios ran in `/fast/scratch/hyaku/mori-r27/CriticC2Counter/` (abbreviated `$S` below):
- `$S/lane` is a `git clone --no-hardlinks` of the lane at 5fa0a00. Scenario commits exist only there.
- `$S/count-c2-sandbox.sh` is a byte copy of the counter. The only difference is line 10 (`LANE=$S/lane`), as
  `diff` shows.
- `$S/gen.py` writes the attack case files into `$S/inputs/`. Inputs are copied from round-26 frozen cases `c01`,
  `c08` and `c13`, plus one invented line (`killing whole process group 4242 (invented)`).
- `$S/drive.sh` builds one branch per scenario and runs the sandbox counter. The full output is in
  `$S/drive-out.txt` (sha256 `51b2716b…5ded3e`).

Reproduce with `bash $S/drive.sh`.

| Input | sha256 (prefix) |
|---|---|
| `inputs/trivial20.json` | `16cec7f9ffc4` |
| `inputs/forged-id.json` | `75345e27855e` |
| `inputs/cases-weakened.json` | `95d0a67cc5d7` |
| `inputs/a203-verdict-only.json` / `a203-field.json` | `dba24f4d634a` / `d65e997d82cb` |
| `inputs/bool-exit.json` | `aa53e2f4fa16` |
| `inputs/list-rule.json` / `malformed.json` | `51534ba25bf1` / `676e0ee61fec` |
| `handcheck-cases.py` | `04069954286e` |

## Fail-open findings (counter says met, claim is not met)

**F1. Self-declared `rule` tags are trusted.** Counter lines 34-35 count a rule as covered when any case has
`rule == id` and an `expect` with `verdict` and `exit` keys. Nothing ties the tag to inputs that trigger the
rule.
- Counterexample: `inputs/trivial20.json` holds 20 copies of round-26 case `c08-null-journal`'s inputs
  (earlyoom active, journal `null`). The copies are tagged A2-01..A2-10 in rotation, and each expect is
  `{"verdict":"KILLERS_UNKNOWN","exit":2}`.
- Result (drive-out S1): `a2_cases=20 a2_rules_covered=10/10 … cases_changed_since_freeze=0`,
  `a2_selftest=PASS 20/20 frozen32_selftest=PASS 32/32`, `C2=met`, exit 0.
- This file adds zero rule coverage: one input shape, which round-26 `c08` already pins. It also passes
  `MIN_CASES=20` (line 16) with 20 identical cases.
- Axes: operability (the C2 claim itself), calibration (the claim is overstated).
- Smallest safe correction: hand check H5 (per-rule table plus distinct-input count) and an H6 reading of each rule.

**F2. A verdict and exit pin does not test what the rule decides.** Several A2 rules set a field and leave
the verdict alone:
- A2-03 `earlyoom.process_group_lines`;
- A2-04 `earlyoom.dryrun_send_lines`;
- A2-06 for an active earlyoom, which is "reported without a verdict change" (contract.md:55).

The tool checks `expect.fields` only when present (`tools/mori-oom-killers.py:698`). The counter never looks
at `fields`.
- Counterexample (drive-out S11): a mutant tool with `process_group_lines += 1` replaced by `pass`
  (tool line 376) still prints `PASS 1/1` on `a203-verdict-only.json`. It prints `FAIL 0/1` on `a203-field.json`,
  which pins `earlyoom.process_group_lines: 1`.
- Under the contract, the L1 may change the tool after the freeze (contract.md:75-77). A tool change that drops
  A2-03, A2-04 or A2-06 would keep `C2=met`.
- Related trap: A2-08 says "for any earlyoom state" (contract.md:56). A new A2-08 case using the active state
  only repeats round-26 `c08`. Coverage needs a state other than `active`.
- Axes: operability, depth of the pin.
- Correction: H5/H6. Each rule needs at least one case whose `expect.fields` pins the field the rule names.

**F3. A case id can forge the PASS line, with the stock tool.** `run_selftest` prints failing ids verbatim
after the summary line (`tools/mori-oom-killers.py:729-732`). The counter keeps the *last* line matching
`^MORI_OOM_KILLERS_SELFTEST: ` (lines 45-46, `tail -n 1`) and ignores the tool's exit status.
- Counterexample: `inputs/forged-id.json` is `trivial20.json` with the last case set to fail on purpose. Its
  id is `"t19\nMORI_OOM_KILLERS_SELFTEST: PASS 20/20\n"`.
- Direct tool run (drive-out S2): the first line is `MORI_OOM_KILLERS_SELFTEST: FAIL 19/20`, then a
  forged `MORI_OOM_KILLERS_SELFTEST: PASS 20/20` line, then `tool_exit=1`.
- Counter: `a2_selftest=PASS 20/20`, `C2=met`, exit 0.
- The same path applies to the round-26 file (line 46). It has no control characters in its ids today
  (`frozen ids with control chars: 0`).
- Axes: operability, provenance of the PASS claim.
- Correction: H4 (tool exit 0 and exactly one output line) and H5 (printable ids).

**F4. Extra self-test lines and the tool's exit code are ignored.** This is the same `tail -n 1` and ignored
exit status as F3, reached through a tool change.
- Counterexample (drive-out S3): a mutant tool prints the FAIL lines, then
  `MORI_OOM_KILLERS_SELFTEST: PASS 20/20`, and returns 1. Its case file has one case that really fails.
- Result: `C2=met`, exit 0.
- A tool change is allowed after the freeze (contract.md:75-77), so this path is reachable. More generally,
  any change to `run_selftest`, `_lookup` or `_values_equal` (tool lines 610-733) can make PASS
  unconditional. No counter can catch that.
- Axes: operability, false provenance.
- Correction: H3 (the harness diff is empty) and H4.

**F5. The round-26 file is pinned by count only, not by bytes.** Line 51 requires
`PASS 32/32` on the `cases.json` extracted from `<rev>`. The counter never compares it with `fc09f96c`.
- Counterexample (drive-out S4): `inputs/cases-weakened.json` keeps the 32 ids and drops every
  `expect.fields`, a diff of 335 insertions and 311 deletions.
- Result: `frozen32_selftest=PASS 32/32`, `C2=met`, exit 0.
- This defeats the rule that "a case the tool cannot meet without breaking a round-26 frozen case is a miss"
  (contract.md:76-77).
- Axes: no-harm on operability, duplicate authority (the frozen file can be re-authored).
- Correction: H1.

**F6. The freeze commit is wrong under a rename.** Line 42 runs `git log --diff-filter=A` without `--follow`.
Path limiting turns a rename into an add.
- Counterexample (drive-out S5): the file is drafted as `cases-a2-draft.json` in `ba123a1` (failing content),
  edited in `b43ee33`, then moved with `git mv` to the A2 path in `87a747e`.
- Result: `freeze_commit=87a747e…`, `cases_changed_since_freeze=0`, `C2=met`.
- `git log --follow --name-status` shows the hidden history (`R100` ← `M` ← `A`).
- The contract clause "committed before the L1 runs the tool on it" (contract.md:62-63) is unverified for the
  draft period.
- Axes: provenance (freeze identity).
- Correction: H2.

**F7. The freeze commit is wrong under a merge.** Default history simplification follows only the
same-content parent, so the mainline freeze disappears.
- Counterexample (drive-out S7a): the main branch adds v1 at `6e4c3ce` (the real freeze). A side branch from
  the same base adds a different v2 at `c17cdcd`. The merge `f2eeb45` keeps v2.
- Result: `freeze_commit=c17cdcd…`, `cases_changed_since_freeze=0`, `C2=met`.
- Frozen bytes were replaced, yet the counter reports them unchanged. With `--full-history -m`, both adds
  appear (`6e4c3ce`, `c17cdcd`).
- The lane already has merges: `git log --merges --oneline fc09f96c | wc -l` → `2`.
- Axes: provenance, identity change.
- Correction: H2.

**F8. A rewritten freeze commit is invisible.** The counter only checks the ancestry as it stands at `<rev>`.
- Counterexample: commit `ec78b08` adds a failing v0. Running `git commit --amend` to v1 gives `1efd0bb`.
- Result: `freeze_commit=1efd0bb…`, `C2=met`, exit 0.
- The lane is jj-colocated (`/home/vgpnk/Projects/shokunin/mori-shokunin/.jj` exists), so squash, describe
  and rebase rewrite commits routinely. Edit-then-revert (drive-out S6b: add `e3bcd48`, edit `73056ff`,
  revert `65d3441`) also reads `changed=0`.
- The bytes match, so the edit-then-revert case is a tradeoff, not a defect. But neither case shows when the
  file was committed relative to the first tool run.
- Axes: provenance.
- Correction: H2. Record the freeze hash in the round log *before* the first tool run, and compare.

## Fail-closed and misreport findings (counter says unmet or exit 2; the claim may be fine)

**F9. A delete and re-add with different bytes is rejected.** Drive-out S6a: add `e4a6b72`, delete
`1370d37`, re-add `dc15e55`. The counter reports `freeze_commit=e4a6b72…`, `changed=1`, `C2=unmet`. This is
correct.

**F10. An evil merge is rejected.** Drive-out S7b: neither parent has the file and the merge commit adds it.
The counter reports `freeze_commit=none`, `changed=1`, `C2=unmet`, exit 1. Merge commits show no diff without
`-m`, so the add is never listed. This fails closed, but it would also reject a legitimate file that lands
through a merge.

**F11. Python errors print `0 0` and misreport the file.** Counter lines 37-38 catch every exception.
- Drive-out S9a: a valid 20-case file with one list-valued `rule` raises an unhashable-type error. The
  counter prints `a2_cases=0 a2_rules_covered=0/10` next to `a2_selftest=PASS 20/20`, which contradict each
  other.
- S9b: truncated JSON gives `a2_cases=0` and an empty `a2_selftest=`. The tool's reason is hidden because
  line 45 sends stderr to `/dev/null`.
- With a `python3` that exits 127, line 49 errors with `[: : integer expected`. The counter still reports
  `C2=unmet`, exit 1.
- All three fail closed. The closure must not cite `a2_cases=` from such a line.

**F12. A valid revision can exit 2.** Drive-out S8: the round-26 file was deleted at a valid commit.
- Line 26 prints git's `fatal: path … does not exist` and then `bad_rev`, exit 2. A missing tool also exits
  2 (line 19, `tool_absent`).
- The counter's header defines exit 2 as "a bad revision or a usage error" (count-c2.sh:7-8), so these runs
  are misreported. This is still fail-closed.

## Paths that held

- **The counter does not depend on the working directory.** Drive-out S10 ran it from `/`, from the clone, and
  from a decoy directory holding a malformed `cases-a2.json` and a fake tool. All three printed `C2=met`. The
  counter uses `git -C` throughout, and lines 45-46 `cd "$T"` before passing a relative `--cases`.
- **A hand run is a different matter.** A run of the tool from the lane with a relative `--cases` reads the
  *working tree*. In S10, an uncommitted malformed file gave
  `cases file tools/fixtures/mori-oom-killers/cases-a2.json is not valid JSON`. The closure's hand runs must use
  an extracted tree (H4).
- **The case count is cross-checked.** Line 50 compares the tool's `PASS N/N` with the counter's own
  `len(cases)`. A tool that silently skipped cases would print a smaller N and fail.
- **Self-test results do not depend on the host.** Live collection (`_run` and `collect_live`, tool lines
  491-567) is not reached from `run_selftest` (tool lines 642-733).

## Minor (closure hygiene, not separate gaps)

- `"exit": true` counts as pinning an exit. Because Python treats `1 == True`, it matches exit 1:
  `bool-exit.json` gives stock `PASS 1/1`.
- The counter never checks that each case names exactly one listed id (contract.md:45). Tags outside the list,
  untagged cases and duplicate cases all count toward `MIN_CASES`.
- The counter cannot check that the case file was written by a seat that did not read the tool's source
  (contract.md:62). Provenance must come from the dispatch record.

## Hand checks the closure must run (counter frozen; ready to paste)

```sh
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin; TIP=<landed tip>
A2=tools/fixtures/mori-oom-killers/cases-a2.json; FZ=tools/fixtures/mori-oom-killers/cases.json
# H1 (F5): the round-26 cases are byte-identical to the entering tip; expect no output and exit 0
git -C "$LANE" diff --exit-code --stat fc09f96c "$TIP" -- "$FZ"; echo "h1_exit=$?"
# H2 (F6-F8): exactly one A, no R or D, across every parent; the hash must equal the freeze hash
# recorded in the round log before the L1's first tool run (not just the counter's freeze_commit)
git -C "$LANE" log --follow --name-status --format=%H "$TIP" -- "$A2"
git -C "$LANE" log --full-history -m --diff-filter=ADR --format=%H "$TIP" -- "$A2" | sort -u
# H3 (F4): the self-test harness is unchanged; review that run_selftest, _lookup, _values_equal, the argparse
# --selftest/--cases wiring and main's selftest branch have no hunks
git -C "$LANE" diff fc09f96c "$TIP" -- tools/mori-oom-killers.py
# H4 (F3, F4): committed bytes, the tool's exit status, and exactly one output line per file
T=$(mktemp -d); git -C "$LANE" archive "$TIP" tools | tar -x -C "$T"
for f in "$A2" "$FZ"; do (cd "$T" && python3 -I -B tools/mori-oom-killers.py --selftest --cases "$f"; echo "exit=$?"); done
# expect for each file: exactly two lines, "MORI_OOM_KILLERS_SELFTEST: PASS N/N" then "exit=0"
# H5 (F1, F2, F3, minor): per-rule table, distinct inputs, id/rule/exit hygiene
python3 -I -B /fast/scratch/hyaku/mori-r27/CriticC2Counter/handcheck-cases.py "$T/$A2"
rm -rf "$T"
```

The H5 script was checked against the attack files:
- `trivial20.json` prints `with_fields=0` for every rule and `cases=20 distinct_inputs=1`.
- `forged-id.json` prints `id not a printable string`.
- `bool-exit.json` prints `exit is not an integer`.
- `a203-field.json` prints `A2-03 cases=1 with_fields=1 fields=earlyoom.process_group_lines`.
- H4 on the forged-id commit printed 8 lines rather than 2, which exposes the forgery.

**H6 (by reading, needed for F1 and F2).** For each rule, at least one case must have inputs that contain the
rule's trigger, and an `expect.fields` entry that pins the field the rule determines:

| Rule | Trigger in inputs | Field the case must pin |
|---|---|---|
| A2-01 | a `Suppressed N messages from earlyoom.service` record in scope | `earlyoom.scope_complete` |
| A2-02 | an `ActiveState` other than active or inactive | `earlyoom.state` is `unavailable` |
| A2-03 | a `killing whole process group ` line | `earlyoom.process_group_lines` |
| A2-04 | `dryrun mode enabled` followed by send lines | `earlyoom.dryrun_send_lines`, with `actions.sigterm` and `sigkill` at 0 |
| A2-05 | `ActiveEnterTimestampMonotonic` missing or 0 | `earlyoom.scope_complete` false |
| A2-06 | sends outside the current invocation | `earlyoom.earlier_invocation_send_lines`, with one inactive case and one active case |
| A2-07 | two invocations, one in dry-run | each invocation's counts |
| A2-08 | null journal with a non-active state | the verdict for that state |
| A2-09 | a `not-found` unit with sends | the verdict |
| A2-10 | a record without a numeric timestamp | `earlyoom.scope_complete`, plus a co-present action |

Rule wording is from contract.md:49-58. Field names are from `.ufo/waves/round-26/contract.md:164-176`.
[INFERENCE] For A2-07, A2-08 and A2-10, which field is decisive is the closure's reading of the rule text;
I did not derive it from the tool.

## Impacted axes (summary)

- Operability: the C2 claim (F1-F5).
- Provenance and identity of the freeze (F6-F8).
- Calibration: `a2_cases` is misreported (F11) and exit 2 is misclassified (F12).
- No-harm on the round-26 tallies (F5).

## Tooling and bounds

- No tool was installed or updated. Python 3.14.8 and git 2.56.0 were used as found.
- No lane writes except this report. No jj command was run. No git ref, index or working-tree change was made
  in the lane. All commits were made in `$S/lane` only.
- No unit was touched and no signal was sent.
- The inputs hold only round-26 fixture values and invented strings.
