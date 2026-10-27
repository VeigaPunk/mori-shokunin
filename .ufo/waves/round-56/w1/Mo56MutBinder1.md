# Mo56MutBinder1 — mutation test of tools/mori-vote-bind.py (round 56, wave w1)

Seat: Mo56MutBinder1 (leaf, no subagents). Date: 2026-10-27. Lane: mori-shokunin.
Target under test: `tools/mori-vote-bind.py`, sha256
`8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca` — byte-identical to the
frozen PIN in `.ufo/waves/round-56/count-c2.py`, i.e. the frozen C2 bytes. Fleet lane HEAD at
test time: `acc62f54fb0f53b47b428594dc27365150cbd76b` (read-only `git rev-parse`); the working
tree tool bytes equal the frozen PIN, so the frozen surface was tested.

Scratch (operator directive 2026-10-25): all copies and fixtures under
`/fast/scratch/hyaku/mori-r56/Mo56MutBinder1/` (`tmp/` as TMPDIR); 9 mutant copies m1..m9
(>= 8 required). Disk guard before runs: `/fast` 28% used, 585G free (ENOSPC: no).
Tooling installs: none needed, none made (pacman paused per orchestrator ruling 2026-10-20;
no uv/npm/binary installs used).

## Method

- Detector (frozen, unmodified): `python3 <copy> --selftest` — 16 cases, prints
  `VOTE_BIND_SELFTEST pass=N fail=M [failed=...]`, exit 0 iff fail=0.
- Verdict rule (as tasked): KILLED iff rc != 0; the killing case is the first failing case in
  the printed `failed=` list. Baseline must pass on pristine bytes, else inconclusive.
- Survivor cross-check (as tasked): rerun the canonical tally over the real committed r55
  bytes and compare with the frozen line. Command shape (paths absolute, read-only):
  `python3 <copy> tally --ledger <repo>/corpus/knowledge/kernel-v7.3-recheck-r55.md --results
  <repo>/.ufo/waves/round-55/w1-results.json --verb RECHECK --voter Mo55Rc01 ... --voter
  Mo55Rc16` (16 padded names, exactly the `VOTERS` construction in `count-c2.py`:
  `"Mo55Rc%02d" % i`, i = 1..16 — no duplicates possible in the frozen list).
- Extra binding probes: `extract` on a scratch fixture to name exactly which additional
  strings a surviving mutant binds.

## Baseline (pristine bytes)

- `--selftest` → `VOTE_BIND_SELFTEST pass=16 fail=0`, rc=0 (run twice: before and after all
  mutant runs). Detector valid; no inconclusive baseline.
- Canonical tally → `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16
  bound_voters=15`, rc=0 — byte-identical to the frozen receipt
  `.ufo/waves/round-56/evidence/tally-r55.txt` and to `EXPECT_TALLY` in `count-c2.py`.

## Mutants and verdicts

Deltas are single-expression edits on the pristine copy; the rest of each file is untouched.
Hashes of the exact bytes run are listed under Restoration.

| id | axis | delta (old → new) | selftest | rc | verdict | killing case |
|----|------|-------------------|----------|----|---------|--------------|
| m1 | A: word charset opened, any lead | `([A-Za-z][A-Za-z0-9_-]*)` → `([A-Za-z0-9_-][A-Za-z0-9_-]*)` | pass=16 fail=0 | 0 | SURVIVED | — |
| m2 | A: word class collapses | `([A-Za-z][A-Za-z0-9_-]*)` → `([A-Za-z0-9_-]+)` | pass=16 fail=0 | 0 | SURVIVED | — |
| m3 | B: rest required | `(?:\s(.*))?` → `\s(.*)` | pass=5 fail=11 | 1 | KILLED | t_plain_binds (raised KeyError, vote without rest no longer binds) |
| m4 | B: rest required, non-empty | `(?:\s(.*))?$` → `\s(.+)$` | pass=5 fail=11 | 1 | KILLED | t_plain_binds (same mode as m3) |
| m5 | C: JSON walk skips dict values | dict branch → `pass` (lists + top strings only) | pass=11 fail=5 | 1 | KILLED | t_json_array_binds (vote_lines values never visited) |
| m6 | C: JSON walk visits keys, not values | `_walk_strings(node[k], acc)` → `_walk_strings(k, acc)` | pass=11 fail=5 | 1 | KILLED | t_json_array_binds |
| m7 | D: inverse probe — roster deduped | `roster = voters if ...` → `roster = sorted(set(voters)) if ...` | pass=16 fail=0 | 0 | SURVIVED | — |
| m8 | A: strict lead-digit variant (slipped) | `([A-Za-z][A-Za-z0-9_-]*)` → `([0-9]],[A-Za-z])[A-Za-z0-9_-]*` grouping slip, see caveat | pass=5 fail=11 | 1 | KILLED | t_plain_binds returned False (word truncated to its first char) |
| m9 | A: strict lead digit-or-letter, capture intact | `([A-Za-z][...])` → `([0-9A-Za-z][A-Za-z0-9_-]*)` | pass=16 fail=0 | 0 | SURVIVED | — |

(m8's regex delta in the table is abbreviated; exact bytes hashed below. The intended clean
strict variant is m9, which was also run because m8's kill is attributable to a side-delta.)

m3/m4 full failed list (killing breadth): t_plain_binds, t_json_array_binds,
t_json_nested_binds, t_json_string_doc_binds, t_last_wins_text, t_last_wins_json,
t_dissent_detected, t_entailed_verb_parsed, t_malformed_json_falls_back_to_text, t_tally_mini,
t_roster_and_name_filter — most as KeyError exceptions because rest-less votes stopped
binding. m5/m6 failed set: t_json_array_binds, t_json_nested_binds, t_last_wins_json,
t_entailed_verb_parsed, t_tally_mini. m8 failed set: the same 11 as m3/m4, all returned-False
(no exception) because the captured word became only its leading character.

## Survivor cross-check vs the frozen r55 line

Canonical tally on committed bytes (padded roster, as above):

| copy | tally line | equals frozen? |
|------|------------|----------------|
| pristine | rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15 | yes (baseline) |
| m1 | identical to baseline | yes — frozen line NOT corrupted |
| m2 | identical to baseline | yes — frozen line NOT corrupted |
| m9 | identical to baseline | yes — frozen line NOT corrupted |
| m7 | identical to baseline | yes — frozen line NOT corrupted (no duplicate names in the frozen list) |

So all four survivors leave the frozen round-55 tally byte-identical: the committed corpus
carries only letter-led words (holds / stale / entailed / overclaim shapes) and the frozen
counter passes a fixed, distinct 16-name roster. The survivors are coverage gaps on the
grammar/roster invariants, not corruptions of the frozen claim.

Binding probes (what survivors additionally accept). Fixture lines were, in order: a plain
prose line, a vote-shaped line with junk word `9lives` (leading digit), an ENTAIL-shaped line
with junk word `-notaword` (leading dash), and a vote-shaped line with junk word
`_under_word` (leading underscore); hashes were valid 12-hex strings. `extract` output:

- pristine control: printed nothing, rc=0 (all four junk words rejected).
- m1: bound all three junk shapes — output lines were `VOTE RECHECK a6e5226259c9 9lives text`,
  `VOTE RECHECK 0124918d278a _under_word text`, `VOTE ENTAIL 7b2d297eec60 -notaword text`.
- m2: identical three bindings as m1.
- m9: bound only the leading-digit shape — `VOTE RECHECK a6e5226259c9 9lives text`.

(Each `VOTE ...` line above is the tool's own output record, quoted as received.)

## Axis D — the tasked mutation is vacuous: pristine already double-counts

The seat tasked: "tally counts a voter twice if it appears twice in --voter". Applied to the
frozen bytes this is not a mutation — the pristine `tally()` roster
(`roster = voters if voters is not None else sorted(outputs)`; `--voter action="append"`)
already counts a repeated name at every use site: per-row `nvote`/`words`, and in
`voters`/`bound_voters`. No dedupe exists anywhere on that path. Verified probes on pristine
bytes (canonical ledger/results, read-only):

- Full frozen roster with the first name passed a second time (17 `--voter` args) →
  `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=17 bound_voters=16`
  — voters and bound_voters inflated by the duplicate; frozen line corrupted under this input.
- Single name twice: `--voter Mo55Rc01 --voter Mo55Rc01` → `TALLY rows=78 agree=10 double=10
  single=0 zero=68 dissent=0 voters=2 bound_voters=2` — all 10 rows that Mo55Rc01 alone voted
  flip from single to double (agree stays 10 because both copies agree with the disposition).
  One real voter is reported as two, and single-voted rows are reported as double-voted.
- The dedupe mutant m7 on the same single-name-dup probe → `TALLY rows=78 agree=10 double=0
  single=10 zero=68 dissent=0 voters=1 bound_voters=1` (correct shape), and m7's selftest is
  pass=16 — the 16-case suite cannot distinguish dedupe from no-dedupe in either direction.

Frozen-claim impact: none at P-C2 (the counter's `VOTERS` list is constructed distinct), but
the roster invariant is unpinned by the selftest and unprotected in the tool. Per the round
rules I name this as a limit and a round-57 routed-item candidate; I do not propose touching
the frozen counter/predicate/kill rules.

## m8 attribution caveat

m8 was killed, but its edit also changed capture grouping: `([0-9]|[A-Za-z])[A-Za-z0-9_-]*`
captures only the word's first character (the tail is outside every group), so plain
`holds`-shaped votes fail equality checks and 11 cases return False. The kill therefore does
NOT evidence that the suite pins the leading-character rule — the clean strict variant m9
(leading digit-or-letter, whole word still captured) passes all 16 cases and survives. Only
the fully-opened charsets (m1, m2) and m9 characterize axis A.

## LOW observation (caller contract): silent skip of unknown roster names

My first baseline accidentally passed unpadded names (Mo55Rc1..Mo55Rc9 instead of Mo55Rc01..09;
Mo55Rc10..16 coincide) and got a plausible-looking line with no error:
`TALLY rows=78 agree=38 double=18 single=20 zero=40 dissent=0 voters=16 bound_voters=6`
— unknown names are skipped silently (`outputs.get(name) is None → continue`) while `voters`
still counts them, and 40 rows silently become zero. The frozen counter is unaffected (exact
padded names; verified byte-identical baseline above). Recorded as an observed failure mode of
the CLI contract, not a counter proposal.

## Restoration evidence

- Fleet file before all runs: sha256 `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca`;
  after all runs: identical. The fleet tree was never written by any step (all runs used
  absolute read-only inputs; TMPDIR pointed into the scratch tree; the fleet git/jj state was
  not touched).
- Scratch pristine copy: sha256 identical to the fleet file (copy fidelity), and its post-run
  detector run prints `VOTE_BIND_SELFTEST pass=16 fail=0`, rc=0 (restored/pristine bytes still
  pass).
- Bytes actually run (sha256): m1 `5ed24f517c93cbeed9405a18f8dc4d9fface7d47f4dc24084edf4cccad1fd305`,
  m2 `5626bdc5ffd236affcef2b82ab08ff44dde3ae0c76dc157da3ca29934e920150`,
  m3 `9d7bd1c4dc8bbfa7faa3b4ab3612a56b285764cda0a66eac59f484b76cab5f7b`,
  m4 `29ed5f35f2a3ec0a85c798c94fa43832896bad2a58043224b9b502c11725c82e`,
  m5 `52af26f98117d0e52e7283c06384ff67c75c982b02a555f199df29898ad13298`,
  m6 `bfea054b26a830b57b66d3b4008ab5eae16d1c9e4075ca5b59e9f4d41c422628`,
  m7 `dcd37707f35944907e3234a49be98ccb948e0ebabe9e38df1ed858f5012bd58e`,
  m8 `8a729a985505f6fb583ecc9a0d78fd47e257445b3706a1937471fd7d70ea3222`,
  m9 `d4949341bc7075538886bcfc2efa978477183b1776691a3e8095c094ae6053f4`.
- Scratch disposal: the whole `/fast/scratch/hyaku/mori-r56/Mo56MutBinder1/` tree is removed
  after this report is written (every cited output is reproduced verbatim above).

## UNVERIFIED

None. Every claim above carries a command and observed output from this session. Frozen
receipts (`evidence/tally-r55.txt`, `count-c2.py` PIN/EXPECT_TALLY) were read and compared
against, not re-executed.

## Findings

1. HIGH — coverage gap, word-grammar leading-character rule unpinned: mutants m1, m2, m9 all
   pass the 16-case selftest and survive; with them the binder accepts words with a leading
   digit, dash, or underscore (probe outputs in Binding probes). Concerns:
   `tools/mori-vote-bind.py` VOTE_RE (line 64) + `SELFTEST_CASES` (no case feeds a
   non-letter-led word). Frozen r55 tally unaffected (verified identical). Named limit; not a
   contract change.
2. HIGH — pre-present defect found by a vacuous tasked mutation: `tally()` does not
   deduplicate the `--voter` roster; a repeated name inflates `voters`/`bound_voters` and
   flips that voter's single-voted rows to double (probe: `voters=2 bound_voters=2`, `single=0
   double=10` from one real voter). Concerns: `tally()` roster construction (~line 164) and
   the CLI `--voter` contract. Frozen P-C2 line is safe only because its fixed list is
   distinct.
3. HIGH — coverage gap, roster semantics unpinned: the dedupe-direction mutant m7 survives
   (pass=16), so the selftest pins neither dedupe nor double-count behavior; no case passes a
   duplicate `--voter` name. Concerns: `SELFTEST_CASES` (t_tally_mini / t_roster_and_name_filter).
4. LOW — m8 kill attribution: the strict-lead mutant that was killed (m8) killed via an
   unintended capture-group side-delta; the clean strict variant m9 survives. Axis A's true
   answer is the surviving m1/m2/m9, not m8's kill.
5. LOW — CLI silently skips unknown roster names while still counting them in `voters`
   (observed: unpadded-name run printed `zero=40 bound_voters=6` with rc=0). Concerns:
   `tally()`/`read_results()` name-miss handling; frozen counter unaffected.
