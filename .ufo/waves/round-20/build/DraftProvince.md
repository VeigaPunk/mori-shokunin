# DraftProvince — round-20 FR3 province text (report)

Seat: MoriR20.DraftProvince (leaf; no subagents). Candidate: `.ufo/waves/round-20/build/DraftProvince/province-r20.md` (4212 bytes, copied under the lane root).

## Behavior delivered

Candidate text, not yet appended to any file:

1. **`PROVINCE.md` append** (after the Round-18 block at end of file): a Core bullet for per-seat wave settlement from `tools/mori-wave-settlement.py scan`, its per-member statuses (`present`/`empty`/`missing`/`misrooted`/`unsafe`/`unparsed`) and wave states (`settled`/`partial`/`unsettled`/`no-spawn`/`unavailable`); a boundary bullet (missing/empty is not dead/failed/killed and not never-written proof; no dispatch authentication; kumitate owns result semantics; receipt review offline); the FR3 still-open bullet; a name-collision bullet; and a measurement-status bullet that states no count before the L1 receipt is committed.
2. **`corpus/README.md` append** (after the Round19 index-repair block at end of file): a Round-20 coverage row for per-seat wave settlement, and a "FR3 frontier boundary after round 20" section naming the two items that remain frontier: emptied-by-hygiene versus never-written, and dispatch authenticity.
3. **Unchanged in place:** `PROVINCE.md` Core wave-settlement bullet (line 23), FR3 bullet (line 46), and `corpus/README.md` FR3 row (line 334). Their boundary text still holds, so the advance is appended, not substituted.

## Evidence (observed)

- Contract read: `.ufo/waves/round-20/contract.md` C2 defines the status vocabulary, the `Report:` trailer rule (last line, `^Report: write your scoped findings to (\S+)$`), `misrooted`, wave states, and the `dead`/`failed`/`killed` vocabulary ban (`contract.md` C2 block). The candidate matches that text.
- Oracle read: `.ufo/waves/round-20/frozen/c2-expected.json` has 14 cases (`all-present`, `one-missing`, `none-present`, `empty-report`, `misrooted`, `malformed-dispatch`, `no-trailer`, `traversal`, `absolute-path`, `symlink-report`, `other-schema-ignored`, `no-spawn`, `content-not-emitted`, `deterministic`).
- Tool absent: `tools/` in mori-shokunin has no `mori-wave-settlement.py` (directory listing observed). The candidate therefore describes a design; no oracle or live run was executed by this seat, per the assignment.
- Round-19 corroboration (the lane's own records, read only):
  - `.ufo/waves/round-19/wave1-run.json` has schema `ufo-swarm-wave-dispatch-v1` and `taskCall.tasks` length 64. Its task bodies end with `Report: write your scoped findings to .ufo/waves/round-19/build/<Name>.md`, which matches the trailer regex.
  - `.ufo/waves/round-19/wave1-settlement.json` (hand-written, not a dispatch file) records `returned_agent_ids: 64` and a `reports_present` list of 16 names, with separate `known_provider_failed`, `known_cancelled` and `no_report_terminal_cause_unestablished` lists. This supports the rule that a missing report must not be read as a terminal cause.
- Fleet-side context: `corpus/lessons/round-12.md:109` records the souji hygiene-interference candidate as rejected for FR3 and not measured by the census; `corpus/knowledge/dispatch-ledger-r18.md` exists and is cited for the observation-only payload binding.

## Findings and risks

1. **Name collision (medium):** the hand-written `round-19/wave1-settlement.json` uses the schema text `mori-wave-settlement-v1`, the same name the new tool emits. Discovery ignores it (its schema is not `ufo-swarm-wave-dispatch-v1`), so it is counted only as `ignored_json`. The candidate says so explicitly. L1 should decide whether the name needs a change before the tool lands; the contract fixes the name, so this seat did not change it.
2. **Emptied-by-hygiene versus never-written is structurally undecidable from the scan:** a removed report and a never-written report both read `missing`; an emptied report reads `empty`. The candidate keeps this frontier and does not claim a distinction.
3. **Dispatch authenticity:** the scan trusts a `ufo-swarm-wave-dispatch-v1` file as found. The candidate keeps this frontier and points to the round-18 observation-only ledger for payload binding.
4. **No count claimed:** the candidate states no live counts. The 14/14 oracle result, the round-19 reproduction of `reports_present = 16` of 64, and the fleet-wide totals are for L1 to record from `.ufo/waves/round-20/evidence/c2-{before,after}.json`. The round-19 `16` figure is the lane's hand-written record, not a tool output; this seat has not reproduced it with the tool.

## Out of scope / not done

- Not appended to `PROVINCE.md` or `corpus/README.md` (L1 integration owner).
- Not run: the tool, its oracle, the census, any selftest, any build or lint.
- No tool install or update. No pacman action.

## Side effect to disclose (corrected)

My first `_write` resolved a relative path against the fleet root and created `/home/vgpnk/Projects/shokunin/.ufo/waves/round-20/build/DraftProvince/province-r20.md`. I copied that file to the correct lane path (`cmp` equal, 4212 bytes), removed the stray file, and removed the two directories I had created there (`build/DraftProvince`, `build`) with `rmdir`, which only removes empty directories. The fleet repo's `round-20/` directory existed before this seat's actions (other seats' `final/` and `w1/` are untouched). No fleet file was otherwise edited.

## Recommended L1 checks (after integration)

- Append the two blocks in `build/DraftProvince/province-r20.md` only after `tools/mori-wave-settlement.py` passes `c2-expected.json` 14/14 and the round-19 live run is recorded.
- Confirm `PROVINCE.md` line 23, line 46 and `corpus/README.md` line 334 are byte-unchanged.
- Decide on the `mori-wave-settlement-v1` name collision (finding 1) before the append.
