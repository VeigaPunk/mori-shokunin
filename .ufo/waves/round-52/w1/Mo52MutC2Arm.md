# Mo52MutC2Arm — mutation test of the hardened entailment arm (`count-c2.py`), round 52 wave w1

Seat: `Mo52MutC2Arm` (mutation tester, leaf seat; no subagents dispatched).
Scope: the frozen counter `.ufo/waves/round-52/count-c2.py` at working-tree sha256
`0a9ec2ffdd85dd1a2be13f359ad82c0f45f99b781d73f9bcf3fa098d7f3bb74a`, which equals the freeze entry
(`evidence/freeze-sha256.txt` line 3), so the measured bytes are the frozen bytes.
Detector: `python3 <copy> --selftest` (the frozen self-test; receipt `evidence/selftest-c2.txt`).
Kill rule applied: a mutation is killed iff its selftest exits nonzero.

## Method

- Scratch root: `/fast/scratch/hyaku/mori-r52/Mo52MutC2Arm/` (created for this seat; removed after this report).
- Source skeleton: `<scratch>/lane/corpus/evidence/sources-r52/` holds the five committed copies; each sha256
  was verified against the frozen COPIES digests before any run (all five matched).
- Pristine copy: `<scratch>/lane/.ufo/waves/round-52/count-c2.py`, a byte-identical copy of the frozen file.
- Each mutant: a separate copy at `<scratch>/mut_<name>/.ufo/waves/round-52/count-c2.py`, with
  `<scratch>/mut_<name>/corpus` symlinked to the lane skeleton (the self-test derives its lane root from the
  script path and reads the five copies from `corpus/evidence/sources-r52/`).
- Detector command per run (literal): `python3 <script path> --selftest`; exit code and output recorded.
- Nothing was written into the lane repo, the fleet repo, or any other seat's files: the counter is read-only
  (git show / ls-tree / rev-parse), and the self-test reads only the synthetic fixture and the five source copies.
- No tool installs or upgrades were needed; system `python3` (3.14.8) was used for all runs. `TMPDIR` pointed
  into the scratch (removed with it). Disk guard checked before the runs (615G free on /fast; no ENOSPC).

## Baseline (pristine), before any mutation

Command: `python3 /fast/scratch/hyaku/mori-r52/Mo52MutC2Arm/lane/.ufo/waves/round-52/count-c2.py --selftest`
Exit: 0
Output tail:
- `PASS words_beyond_counts`
- `PASS text_copy_keeps_angle_brackets`
- `C2_SELFTEST pass=45 fail=0`

This matches the frozen receipt `evidence/selftest-c2.txt` (exit=0, 45 PASS lines).

## Mutations and verdicts

Each row: point mutation -> selftest result -> verdict -> killing arm(s).

| # | mutation (single point) | selftest | verdict | killing arm(s) |
|---|---|---|---|---|
| 1 | MIN_VOTES 2 -> 1 | pass=34 fail=11, exit=1 | killed | entail_one_voter_unmet, entail_same_voter_twice_unmet, entail_one_row_single_vote_unmet, entail_l1_file_ignored_unmet, entail_non_voter_seat_ignored_unmet, entail_voter_outside_list_ignored_unmet, entail_non_md_ignored_unmet, entail_other_dir_ignored_unmet, entail_fenced_votes_ignored_unmet, entail_author_vote_not_counted_unmet, entail_hash_of_other_text_unmet |
| 2 | fence toggle dropped (fenced ENTAIL/REPLACE lines read as unfenced) | pass=42 fail=3, exit=1 | killed | entail_fenced_votes_ignored_unmet, entail_fenced_dissent_ignored_met, entail_fenced_replace_not_authorship_met |
| 3 | any `.md` under w1/ accepted as voter | pass=41 fail=4, exit=1 | killed | entail_l1_file_ignored_unmet, entail_non_voter_seat_ignored_unmet, entail_voter_outside_list_ignored_unmet, entail_non_voter_dissent_ignored_met |
| 4 | VOTERS filter dropped (any file under w1/ accepted) | pass=40 fail=5, exit=1 | killed | entail_l1_file_ignored_unmet, entail_non_voter_seat_ignored_unmet, entail_voter_outside_list_ignored_unmet, entail_non_md_ignored_unmet, entail_non_voter_dissent_ignored_met |
| 5 | authorship subtraction dropped (a voter's own vote counts) | pass=44 fail=1, exit=1 | killed | entail_author_vote_not_counted_unmet |
| 6 | overclaim counted from any file under w1/, not only voters | pass=44 fail=1, exit=1 | killed | entail_non_voter_dissent_ignored_met |
| 7 | REPLACE regex unanchored (`^\s*` removed) | pass=45 fail=0, exit=0 | survived | none exercised |
| 8 | claim hash computed without whitespace folding | pass=44 fail=1, exit=1 | killed | entail_hash_whitespace_folded_met |
| 9 | vote regexes accept uppercase hex | pass=45 fail=0, exit=0 | survived | none exercised |
| 10 | unmet condition `entailed != claims` -> `entailed < claims` | pass=45 fail=0, exit=0 | survived | none exercised (parity, see below) |

Notes on the three survivors (each is a routed limit for round 53):

- #7 — the frozen arm anchors the authorship signal at line start (`^\s*`); the loosened variant would treat the
  middle of a paragraph as a valid position for the authorship marker (a token spelled `REPLACE <h> :: <text>`).
  No self-test control contains such a mid-line token, so the battery cannot distinguish the variants. Routed
  limit: add a control whose fixture contains an unfenced line carrying that spelling after other words (e.g. a
  sentence explaining the syntax) and assert the mid-line occurrence does not count as authorship.
- #9 — the vote regexes are lowercase-hex only; the loosened variant accepts `[0-9A-Fa-f]{12}`. Every self-test
  fixture uses lowercase hashes (produced by `claim_hash`), so uppercase-hex votes are never exercised. Routed
  limit: add controls voting with uppercase-hex hashes (as entailed vote, overclaim vote, and REPLACE line) and
  assert they are ignored.
- #10 — behaviourally inert under the counter's own invariant: `entailed` increments at most once per validated
  table row, so `entailed <= claims` holds always, and `entailed != claims` vs `entailed < claims` are
  equivalent conditions. Routed limit: record this invariant in the counter's Limits block; if a future shape
  ever allowed more than one entailed increment per row, the comparison would need re-decision.

## Per-mutant evidence

For each mutant: script path under `<scratch>/mut_<name>/`, applied change, sha256 (creation; unchanged after
run), command, exit, final selftest line, FAIL list.

1. `min_votes_2to1` — `MIN_VOTES = 2` -> `1` (line 45). sha256 `2f9b1831f4c4b322d9b17b15778e68402bc60f97998bcf288508f65eb8686408`.
   Exit 1. `C2_SELFTEST pass=34 fail=11`. FAIL: entail_one_voter_unmet, entail_same_voter_twice_unmet,
   entail_one_row_single_vote_unmet, entail_l1_file_ignored_unmet, entail_non_voter_seat_ignored_unmet,
   entail_voter_outside_list_ignored_unmet, entail_non_md_ignored_unmet, entail_other_dir_ignored_unmet,
   entail_fenced_votes_ignored_unmet, entail_author_vote_not_counted_unmet, entail_hash_of_other_text_unmet.
2. `drop_fence_toggle` — removed the `fence` tracking block in `entail_votes` (lines 136-141). sha256
   `965ac9215c31bd0dbe52058c81402aafa59650ed6802e8421bceb93899923a62`. Exit 1. `C2_SELFTEST pass=42 fail=3`.
   FAIL: entail_fenced_votes_ignored_unmet, entail_fenced_dissent_ignored_met,
   entail_fenced_replace_not_authorship_met.
3. `accept_any_md` — voters loop iterates over every `.md` file present under ENTAIL_DIR (voter label = basename
   minus `.md`) instead of the frozen VOTERS list (lines 132-135). sha256
   `6f305b01c6d9e971b52807499827d1b288f75b04a0c48bc72b777dad44527381`. Exit 1. `C2_SELFTEST pass=41 fail=4`.
   FAIL: entail_l1_file_ignored_unmet, entail_non_voter_seat_ignored_unmet,
   entail_voter_outside_list_ignored_unmet, entail_non_voter_dissent_ignored_met.
4. `drop_voters_filter` — same loop iterates over every file present (any name/extension). sha256
   `26766aa7a2e6065a7346664166176900e40ddbf7e2c5a5baae0d6c1d8a12388b`. Exit 1. `C2_SELFTEST pass=40 fail=5`.
   FAIL: entail_l1_file_ignored_unmet, entail_non_voter_seat_ignored_unmet,
   entail_voter_outside_list_ignored_unmet, entail_non_md_ignored_unmet, entail_non_voter_dissent_ignored_met.
5. `drop_authorship_subtraction` — `ok_voters` keeps a voter's entailed vote even for hashes in that voter's
   `authored` set (line 239). sha256
   `2ce0f27846cc87548b0273e494976594305e2dd4a6e8204edf4e4a193f55c52d`. Exit 1. `C2_SELFTEST pass=44 fail=1`.
   FAIL: entail_author_vote_not_counted_unmet.
6. `overclaim_from_anyone` — ENTAIL lines are collected from every file under ENTAIL_DIR; overclaim lines from
   any file enter the dissent set, while entailed lines still require the writer to be a frozen voter. sha256
   `8ec562b55b22c748681772c35aa72efbe3e8316b4ff035f59260b6e91c177a63`. Exit 1. `C2_SELFTEST pass=44 fail=1`.
   FAIL: entail_non_voter_dissent_ignored_met.
7. `replace_re_unanchored` — `REPLACE_RE` loses the `^\s*` anchor (line 125), so a REPLACE token anywhere in a
   line is read as authorship. sha256 `8f21bb31827c2eebb90c0d2be4f453d307c34b756c92d60bf273279e936a7805`.
   Exit 0. `C2_SELFTEST pass=45 fail=0`. No FAIL. SURVIVED.
8. `hash_no_ws_folding` — `claim_hash` hashes the raw claim (strip only, no `\s+` -> space collapse). sha256
   `61ef93403e72241169fed36f144592693531ae57493b4f8bc25958ed8392c0c6`. Exit 1. `C2_SELFTEST pass=44 fail=1`.
   FAIL: entail_hash_whitespace_folded_met.
9. `uppercase_hex_accepted` — both vote regexes (lines 124-125) take `[0-9A-Fa-f]{12}` instead of
   `[0-9a-f]{12}`. sha256 `5fd14b30973519e45e4e7f122832519a4f821fc3667e4ef8ba0a317a26ec3165`. Exit 0.
   `C2_SELFTEST pass=45 fail=0`. No FAIL. SURVIVED.
10. `entailed_ge_claims` — unmet condition changed from `entailed != claims` to `entailed < claims` (line 246).
    sha256 `4269844a12516a0c0b1b2491a223aeb39c51d98c9cf1606571d41e8c52a723dc`. Exit 0.
    `C2_SELFTEST pass=45 fail=0`. No FAIL. SURVIVED (parity, see above).

## Restoration evidence

- Pristine copy hashed before all runs and again after all runs: both `0a9ec2ffdd85dd1a2be13f359ad82c0f45f99b781d73f9bcf3fa098d7f3bb74a` — unchanged.
- Every mutant hashed at creation and again after its run: identical for all ten (values above). Runs are read-only; no post-run edits.
- The scratch root was removed after this report: `rm -rf /fast/scratch/hyaku/mori-r52/Mo52MutC2Arm` (see Cleanup). The only write performed inside the lane this seat made is this report file.

## Cleanup

- `rm -rf /fast/scratch/hyaku/mori-r52/Mo52MutC2Arm` executed after writing this report; verified the path no longer exists. `TMPDIR` pointed inside the scratch and was removed with it.

## Findings

- MED — coverage gap: no self-test control exercises a mid-line REPLACE token, so an unanchored authorship regex survives (mutant #7). Concern: `REPLACE_RE` at `.ufo/waves/round-52/count-c2.py:125`; selftest checks at lines 493-499. Routed limit as above.
- MED — coverage gap: no self-test control exercises uppercase-hex vote hashes, so a regex that accepts them survives (mutant #9). Concern: `ENTAIL_RE` / `REPLACE_RE` at lines 124-125; entailment selftest block lines 462-503. Routed limit as above.
- LOW — parity only: `entailed != claims` vs `entailed < claims` are equivalent under the per-row single-increment invariant, so mutant #10 is behaviourally inert and survives by equivalence, not by a test weakness. Concern: line 246; invariant not stated in the counter's Limits block. Routed limit as above.
- All seven behavioural weakenings (quorum, fence handling, voter scope, authorship subtraction, dissent source, hash folding) were killed by the hardened arm's self-test; the arm detects each of them.

All evidence above is observed (command + output + exit code). Nothing required an UNVERIFIED mark.
