# Judge11 — wave 2 falsify: r29-a2-10-inactive-lone-missing-stamp

Non-author judge; lane tip `8809a3fe1eaa87a0afa177a15263d174378e7462`; entering tip `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`; pinned fleet rev `63729047644f839fe4c8cc97abd0d8bf741a5787`.

## Sources read (only assigned sources)
- Rule text: `.ufo/waves/round-27/contract.md:40-80`.
- Round-26 spec including output rules and Amendment A2: `.ufo/waves/round-26/contract.md` (190 lines).
- Case: `tools/fixtures/mori-oom-killers/cases-a2-r29.json:953-987`.
- BASE: `/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-10-inactive-lone-missing-stamp.base.json:1-22`.
- FIX: `/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-10-inactive-lone-missing-stamp.fix.json:1-22`.
Did not read tool source, fix diff, other reports, or lessons.

Case inputs have earlyoom inactive and a valid in-scope `earlyoom 1.9.0` record at timestamp 4100000, followed by a send record with no `__MONOTONIC_TIMESTAMP`; oomd is inactive and `oomd_notices=0` (`cases-a2-r29.json:958-970`). The expected values are at `:972-985`. BASE values are at `base.json:2-20`, exit at `:22`; FIX values are at `fix.json:2-20`, exit at `:22`.

## Field-by-field ruling

| field | expected | base | fix | ruling | deciding contract line(s), quoted |
|---|---|---|---|---|---|
| verdict | KILLERS_QUIET | KILLER_ACTED | KILLERS_QUIET | tool error | r26:186-187: “left uncounted”; r26:97-104: “KILLERS_QUIET, exit 0: otherwise” |
| exit | 0 | 1 | 0 | tool error | r26:97-104: “KILLERS_QUIET, exit 0: otherwise”; r26:186-187: “positive evidence elsewhere still stands” (none here) |
| earlyoom.state | inactive | inactive | inactive | matches | — |
| earlyoom.version | 1.9.0 | null | null | tool error | r26:82: “`earlyoom <version>` → version (the first line of an invocation)” |
| earlyoom.grammar | verified-1.9.0 | unverified | unverified | tool error | r26:81-82 identifies the earlyoom 1.9.0 message grammar and version line; r26:91 allows `verified-1.9.0` or `unverified` |
| earlyoom.scope_complete | false | false | false | matches | r26:186-187: “makes the scope incomplete”; r27:58: “makes the scope incomplete” |
| earlyoom.actions | null | null | null | matches | r26:102-104: an inactive killer reports `actions: null` |
| earlyoom.earlier_invocation_send_lines | 0 | 1 | 0 | tool error | r26:186-187: “left uncounted”; r26:175-177: field counts send/escalation lines outside current invocation |
| earlyoom.dryrun_send_lines | 0 | null | null | tool error | r27:52 / r26:166-167: after dryrun, send lines go to this field; no dryrun/send record is countable |
| earlyoom.process_group_lines | 0 | null | null | tool error | r27:51 / r26:164-165: process-group lines are counted in this field; no such line occurs |
| oomd.notices_this_boot | 0 | 0 | 0 | matches | r26:90-98: output field and `oomd_notices > 0` verdict condition; case input is 0 (`cases-a2-r29.json:970`) |

## Findings

- **Verdict and exit — tool error.** The only send record has no numeric timestamp and is “left uncounted” (r26:186-187; r27:58), so it is not positive evidence in scope or an earlier-invocation count. `oomd_notices` is 0 (`cases-a2-r29.json:970`). The contract says `KILLERS_QUIET, exit 0: otherwise` for no positive evidence, and its unknown rule applies when earlyoom is active but incomplete (r26:99-104); this earlyoom is inactive (`cases-a2-r29.json:959`). BASE returns KILLER_ACTED/1 (`base.json:19,22`), contrary to those rules.
- **Earlier-invocation count — tool error.** A2-10 says the timestamp-less record is left uncounted (r26:186-187; r27:58); the field counts send/escalation lines outside the current invocation (r26:175-177). It therefore contributes 0; BASE reports 1 (`base.json:6`).
- **Version and grammar — tool error.** The valid version record is at the invocation boundary 4100000, equal to `ActiveEnterTimestampMonotonic=4100000` (`cases-a2-r29.json:959,963-965`); scope includes timestamps greater than or equal to that boundary (r26:77-80). r26:82 maps `earlyoom <version>` to the version. The case's version and grammar are therefore 1.9.0 / verified-1.9.0 (`cases-a2-r29.json:976-978`); BASE has null / unverified (`base.json:7,12`). The separate malformed record is left uncounted and makes scope incomplete; it does not discard the valid version record (r26:186-187).
- **Dry-run and process-group counters — tool error.** The case contains no `dryrun mode enabled` or `killing whole process group ` line (case:963-969); the rules route those respective lines to the named counters (r26:164-167; r27:51-52). Neither counter has a countable matching line, so its expected zero is correct; BASE emits null (`base.json:5,8`).
- The remaining expected values match BASE and FIX. No mismatch is a case error or unclear text: the case's expected values follow the cited rules.

## FIX assessment, residual risk, and gaps

FIX matches the case on verdict, exit, state, scope_complete, actions, earlier_invocation_send_lines, and oomd.notices_this_boot (`fix.json:3-19,22`). FIX does not match version, grammar, dryrun_send_lines, or process_group_lines (`fix.json:5,7-12`). The three changed fields (verdict, exit, earlier-invocation count; compare `base.json:6,19,22` with `fix.json:6,19,22`) are now correct; none is wrong under the contract. [INFERENCE] Because four expected fields remain mismatched, this single case would not pass unchanged in the draft's selftest; no selftest was run by this judge.

No installs, subagents, live runs, or harness/fleet mutations. No verification beyond the specified contract, case, and output reads.

`Report:` .ufo/waves/round-29/w2/Judge11.md

case_ruling=tool error
