# Mo53MutC1 — mutation test of the frozen round-53 C1 counter

Seat: Mo53MutC1 (mutation-tester, leaf). Round 53, wave w1. Claim under attack: **C1** (freshness, the v7.3
recheck). Subject: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/count-c1.py`
(544 lines), the frozen counter. Nothing in this report proposes a change to a predicate, counter, floor or kill
rule; every survivor below is a named limit routed to round 54.

Scratch (operator directive 2026-10-25): `/fast/scratch/hyaku/mori-r53/Mo53MutC1/` — `tmp/`, `lane/` (a 4-level
skeleton `<seat>/lane/.ufo/waves/round-53/count-c1.py` + `lane/corpus/evidence/sources-r53/*`, so the counter's own
`lane_root()` resolves and `--selftest` reads the committed v7.3 copies), one `git clone --shared` of the lane at
`<seat>/clone` for the fixture commits. Disk guard read before the run
(`scripts/hyaku/disk-guard.sh status` → rc 0, no ENOSPC). No pacman, no install, no network fetch. Scratch removed at
the end (see §Scratch removal).

## 1. Subject and detector

Frozen bytes, and they are the freeze-listed bytes:

```
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/count-c1.py
ebaff9158362b905961e9c23b2e91790df135e3b344327030c6f67a2db27005d  .ufo/waves/round-53/count-c1.py
$ git -C mori-shokunin show f4da3fd4:.ufo/waves/round-53/evidence/freeze-sha256.txt | grep count-c1
ebaff9158362b905961e9c23b2e91790df135e3b344327030c6f67a2db27005d  .ufo/waves/round-53/count-c1.py
```

Detector (bounded, as tasked): `python3 <mutant> --selftest`. **killed iff exit ≠ 0.** The selftest is the counter's
own 37-arm in-memory fixture suite; a survivor is therefore a statement about the *selftest's* coverage of that line,
not about the counter's behaviour on the landed data. Every survivor was additionally probed end-to-end (below),
because a selftest survivor with a concrete false-`met` is materially worse than one without.

Baseline (pristine bytes, same command on the same path):

```
$ python3 lane/.ufo/waves/round-53/count-c1.py --selftest; echo "exit=$?"
C1_SELFTEST pass=37 fail=0
exit=0
```

Baseline is clean → a mutant's nonzero exit is a kill, not an inherited failure. Baseline live reading at the landed
data commit (read-only `git show`, `--repo` the lane):

```
$ python3 lane/.ufo/waves/round-53/count-c1.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df --repo /home/vgpnk/Projects/shokunin/mori-shokunin
C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df failed=votes
exit=1
```

(`failed=votes` is expected at the data commit: no voter report is committed there yet, matching
`evidence/c1-at-data.txt`.)

## 2. Protocol

Per mutation: pristine bytes → apply **one** semantic replacement (each anchor asserted to occur exactly once in the
pristine text) → write into the scratch lane path → `--selftest` → live reading at `2a4213b` → **restore the pristine
bytes byte-exactly** → re-run `--selftest` and re-hash. Before-hash for every run: `ebaff9158362…`; after-restore
hash for every run: `ebaff9158362…`, restore-selftest rc 0 (table column *rest*).

21 mutations: the 14 the seat named (M01–M14 cover exactly that list) plus 7 further single-point defects on checks
the list did not name (M15–M21). Line numbers are the frozen counter's.

## 3. Results

`killed` = `--selftest` exit ≠ 0. `mut sha` = first 12 hex of the mutated bytes. `rack` = the selftest arms that
failed (the killing checks).

| id | mutation (frozen counter line) | mut sha | selftest | verdict | killing arm(s) | rest |
|---|---|---|---|---|---|---|
| M01 | `MIN_VOTES = 2` → `1` (:51) | a9c7195314be | rc 1 | killed | one_voter_unmet, same_voter_twice_unmet, non_voter_dissent_ignored_but_one_voter_unmet | ok |
| M02 | vote fence toggle dropped, fenced lines count (:168-173) | 25d6742392ec | rc 1 | killed | fenced_votes_unmet, fenced_dissent_ignored_met, fenced_quote_proposal_ignored_met | ok |
| M03 | last-wins → first-wins (:176) | 17e34b431f46 | rc 1 | killed | revised_dissent_met | ok |
| M04 | votes read from any report file in the vote dir, not the frozen 12 seats (:163-166) | 78521bb476a0 | rc 1 | killed | non_voters_unmet, non_voter_dissent_ignored_but_one_voter_unmet | ok |
| M05 | authorship subtraction dropped from `agree` (:249) | fa85d26ecbf2 | rc 1 | killed | author_vote_not_counted_unmet | ok |
| M06 | status derivation always `held` (:226) | c3dbee658fb7 | rc 1 | killed | honest_met, held_labelled_absent_unmet, indented_rows_met, revised_dissent_met, fenced_dissent_ignored_met, fenced_quote_proposal_ignored_met, all_changed_with_votes_met | ok |
| M07 | held rows need not equal their v7.2 quote (:232) | e26beb22cc32 | rc 1 | killed | held_with_other_quote_unmet | ok |
| M08 | quote word bounds dropped (:231) | 88ed7959f0d9 | rc 1 | killed | replacement_too_short_unmet | ok |
| **M09** | **scope read at the scored rev instead of the entering tip (:325)** | 95c4828122c7 | **rc 0** | **SURVIVED** | — | ok |
| M10 | SOURCES used-by check dropped (:239) | 73f04479f7ca | rc 1 | killed | row_usedby_unmet | ok |
| M11 | SOURCES opened-date check dropped (:239) | cd40d58df0db | rc 1 | killed | row_opened_earlier_unmet | ok |
| **M12** | **v7.2 URL accepted as the v7.3 source URL (:238)** | 42106ec1fcbe | **rc 0** | **SURVIVED** | — | ok |
| M13 | sha256 pin comparison dropped (:188) | 7ffdbffc8afa | rc 1 | killed | pin_tampered_unmet | ok |
| **M14** | **`c["rows"] != len(d)` dropped (:254)** | 657cbb85ec6e | **rc 0** | **SURVIVED** | — | ok |
| M15 | `MIN_WORDS` 6 → 1 (:53) | d00f013d78b7 | rc 1 | killed | replacement_too_short_unmet | ok |
| **M16** | **`MAX_WORDS` 25 → 1000 (:53)** | 1c564b54e40a | **rc 0** | **SURVIVED** | — | ok |
| M17 | status derivation inverted (:226) | b774aa42dc00 | rc 1 | killed | honest_met, held_labelled_absent_unmet, indented_rows_met, revised_dissent_met, fenced_dissent_ignored_met, fenced_quote_proposal_ignored_met, all_changed_with_votes_met | ok |
| M18 | table fence toggle dropped in `parse_table` (:102-105) | 54c1eba89d9b | rc 1 | killed | scope_reader | ok |
| M19 | vote comparison `>=` → `>` (:252) | 73e25a05ac9e | rc 1 | killed | honest_met, indented_rows_met, revised_dissent_met, fenced_dissent_ignored_met, author_vote_not_counted_unmet, fenced_quote_proposal_ignored_met, all_changed_with_votes_met | ok |
| **M20** | **`matched != len(d) or rows != len(d)` check dropped entirely (:254-255)** | 2f48ee1ae142 | **rc 0** | **SURVIVED** | — | ok |
| M21 | dissent check never fires (:250-251) | 2d7f2f6a76e2 | rc 1 | killed | dissent_unmet | ok |

16 killed, 5 survived, 0 inconclusive (baseline clean, all restores clean).

Live-reading differential at `2a4213b` (beyond the tasked detector, recorded for completeness): only M06 and M17
change the printed line, both to `status_ok=44 quote_ok=44 failed=quote,status,votes` / `status_ok=0 …`. No survivor
changes the reading at `2a4213b`, because the vote arm fails there for everyone (`voted=0`) — the survivors were
therefore probed on fixtures instead (§4).

## 4. Survivors: fixture probes

One clone, `git clone --shared` from the lane (toplevel asserted equal to the clone dir before the first commit),
four fixture commits on top of the data commit plus two commits that add the two synthetic voter reports, then
pristine vs mutant at the same rev. Vote reports were generated from the ledger itself (one unfenced
seat-sized final line per ledger hash, two distinct seats, 46 lines each) so the vote arm is satisfied; in P5/P6 the
only difference from a compliant state is the probed violation.

### 4.1 M09 — scope read at the scored revision (survived; false-unmet, frozen-clause drift)

P1 (`2ee71b0a88e8daeffb54128c077f1bf0cb53ab3d`): one claim row appended to the r52 claim table after the data commit,
still citing a v7.2 file, so the entering-tip scope is unchanged (46) but a scope read at R would see 47.

```
pristine rc=1 C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=2ee71b0a… failed=votes
M09      rc=1 C1=unmet scope=47 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=2ee71b0a… failed=quote,rows,status,votes
```

P-C1 says D is read "at the entering tip". The mutant lets an editable table move D, so a claim-row edit landed after
the freeze flips an otherwise compliant ledger to `unmet`. The selftest cannot see it: it calls `scope()` directly on
a synthetic entering tree (`scope_reader`, :532) and never runs `main()`, which is the only place the revision choice
exists (:310 `--scope` branch, :325 scored branch). **Arm text for round 54:** an arm that drives `main()` twice over
a fixture repo whose claim table differs between the entering tip and the scored rev, asserting `scope=` equals the
entering-tip count in both runs. False-`met` not shown: the two observed directions (row added, row deleted,
source URL edited) all remove a hash from D and are caught as `bad_rows`.

### 4.2 M12 — v7.2 URL accepted as the v7.3 source URL (survived; **false-met**)

P2 (`604557d8c93c9f1101b3549a2a5cbe27ec810b80`): S510's URL rewritten to the v7.2 URL of the same path; P6
(`0c91aa839a4864d61630476ddb108bd7cf30e632`): P2 plus the two voter reports.

```
P2 pristine rc=1 C1=unmet … source_rows=bad … failed=bad_rows,votes
P2 M12      rc=1 C1=unmet … source_rows=ok  … failed=votes

P6 pristine rc=1 C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=bad pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0 failed=bad_rows
P6 M12      rc=0 C1=met   scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok  pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0
```

With the vote arm satisfied, M12 reads **C1=met, exit 0** on a ledger whose source row names the stale v7.2 anchor —
exactly the clause the freshness claim exists to enforce ("carries the frozen v7.3 URL of that path"). The selftest
arm `row_v72_url_unmet` (:459) applies one URL to all nine S-rows (`srow(p, **kw) for p in V73`), so with the URL
check widened for the row's *own* path the other eight rows still fail and `source_rows=bad` keeps the arm green —
the arm passes for the wrong reason. **Arm text for round 54:** set the v7.2 URL on exactly one S-row (the one the
probed ledger row cites) and assert `source_rows=bad`. Note the frozen bytes reject this ledger; the gap is in the
selftest, which is the gate a future counter revision is frozen through.

### 4.3 M16 — `MAX_WORDS` upper bound unasserted (survived; **false-met**)

P3 (`61e0bcfeccc641d8c032d6b8348eca07067baf92`): the absent `mm/mmap.c` row carries a **26-word** v7.3 quote (one
over the bound; the minimally plausible violation — the real instance is the two-sentence MAP_NORESERVE rule, 26
words, located in the copy). P5 (`8627bcf7d044d2a84f0af5a7b89b4ed7ea9366d9`): P3 plus the two voter reports.

```
P3 pristine rc=1 C1=unmet … quote_ok=45 … failed=quote,votes
P3 M16      rc=1 C1=unmet … quote_ok=46 … failed=votes

P5 pristine rc=1 C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=45 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0 failed=quote
P5 M16      rc=0 C1=met   scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0
```

Losing `MAX_WORDS` lets a 26-word quote cell pass as a located quote and, with votes, reads **C1=met**. Only the lower
bound is asserted: `replacement_too_short_unmet` (:439) is the sole word-count arm, and M15 (min 6→1) is killed by it
while M16 (max 25→1000) is invisible. **Arm text for round 54:** an arm with a 26-word located quote on an absent row
asserting `quote` in the failed list.

### 4.4 M14 / M20 — the `rows` family is redundant and its arms are weakly asserted (survived; verdict-preserving)

P4 (`6d0dd0866bf9a7edf02b31e30aced8ba54ed108d`): one 5-cell row appended to the ledger table.

```
pristine rc=1 C1=unmet scope=46 rows=47 matched=46 … failed=bad_rows,rows,votes
M14      rc=1 C1=unmet scope=46 rows=47 matched=46 … failed=bad_rows,votes
M20      rc=1 C1=unmet scope=46 rows=47 matched=46 … failed=bad_rows,votes   (same as M14 on this fixture)
```

Only the diagnostic label changes; the verdict is untouched, because `rows != len(d)` is subsumed: a missing row fails
`matched != len(d)` and also `status`/`quote`/`votes`, an extra row is `bad_rows` (malformed, unknown hash, duplicate
or wrong entry). So M14 and M20 are equivalent mutants — a coverage finding about the *selftest's* assertions, not a
hole in the verdict: the arms `no_table_unmet` (:409), `missing_row_unmet` (:412), `extra_row_unmet` (:415) assert
`"rows" in line`, and the counter line always contains `rows=N` — the assertion is vacuous on the failure label, so
dropping the check cannot be seen. **Arm text for round 54:** assert membership of the parsed `failed=` list, not a
substring of the whole line.

## 5. Restoration evidence

Every mutant was written only to `/fast/scratch/hyaku/mori-r53/Mo53MutC1/lane/.ufo/waves/round-53/count-c1.py`.
After each run the pristine bytes were rewritten and re-hashed:

```
base   sha256 = ebaff9158362b905961e9c23b2e91790df135e3b344327030c6f67a2db27005d  (37/37 arms, rc 0)
M01..M21 restored sha256 = ebaff9158362…  restore selftest rc = 0   (all 21, no exception)
```

The lane's own file was never opened for writing and still hashes to the freeze entry:

```
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/count-c1.py
ebaff9158362b905961e9c23b2e91790df135e3b344327030c6f67a2db27005d  …/round-53/count-c1.py
```

No git/jj mutation in the lane or the fleet root; the only commits are in the scratch clone, under a fixture identity
configured inside that clone, with `git -C <clone> rev-parse --show-toplevel` asserted before the first commit.

## 6. Limits of this probe

- The detector is the counter's own selftest. A killed mutant shows that suite covers the line; it does not show the
  landed data would fail. Conversely every survivor is a statement about the suite, and the frozen counter on the
  landed data is correct on all five points — I verified the pristine bytes reject each probed fixture.
- Fixtures use two synthetic voter seats (`Mo53Fr01`, `Mo53Fr07`) whose lines were generated from the ledger's own
  dispositions; that satisfies the vote arm mechanically and proves nothing about the real wave's votes. No claim is
  made about the twelve real RECHECK seats.
- `--selftest` reads the nine v7.3 copies from `lane_root()`; the scratch skeleton carries an exact copy of
  `corpus/evidence/sources-r53/` (12 files, 408 K) and the pins still verify inside it, so the fixture path is the
  same code path.
- One clone, four fixture commits plus two vote commits, all removed with the scratch.
- `MAX_WORDS` was mutated to 1000 rather than to a smaller plausible number: any value ≥ 26 survives, since no arm
  carries a quote longer than 25 words.

## 7. Scratch removal

```
$ rm -rf -- /fast/scratch/hyaku/mori-r53/Mo53MutC1
$ test -e /fast/scratch/hyaku/mori-r53/Mo53MutC1; echo "exists=$?"
exists=1
```

`results.json`, `probes.json`, `probes2.json` and the two drivers lived only there; their content is transcribed
above. No file was created inside `/home/vgpnk/Projects/shokunin/mori-shokunin` by this seat.

## Findings

1. **MED — `count-c1.py:53` with `:231` (and selftest arms at `:439`): the `MAX_WORDS = 25` upper bound has no
   selftest arm.** A 26-word located quote on an absent row survives `--selftest` (M16, rc 0) and, with the vote arm
   satisfied, reads `C1=met` exit 0 (P5). P-C1's "6 to 25 words" clause is enforced only on the lower bound; a future
   counter revision could drop the upper bound and still be frozen green.
2. **MED — `count-c1.py:238` with selftest arm `:459`: the per-row v7.3-URL requirement is not asserted per row.**
   M12 (accept the v7.2 URL of the same path) survives (rc 0) and reads `C1=met` on a ledger whose source row names
   the stale v7.2 anchor (P2/P6). The arm applies one v7.2 URL to all nine S-rows, so eight rows keep
   `source_rows=bad` and the arm passes for the wrong reason.
3. **MED — `count-c1.py:325`: `main()`'s scope-read revision is untested.** M09 (scope read at R) survives (rc 0);
   with one claim row added after the freeze the scope moves 46→47 and a compliant ledger reads `unmet`
   (P1). The selftest exercises `scope()` only through a synthetic reader (`:532`), never the revision choice, so the
   frozen "read at the entering tip" clause is unpinned by the suite.
4. **LOW — `count-c1.py:254-255` with selftest arms `:409`, `:412`, `:415`: the `rows`/`matched` family is redundant
   and its arms assert a substring the line always carries.** M14 (rows==len(d) dropped) and M20 (whole check
   dropped) both survive (rc 0); P4 shows only the `rows` label disappears. The arms' `"rows" in line` is satisfied by
   the `rows=N` field, so they assert only "not met".
5. **LOW (observation, not this seat's) — lane root hygiene:** `mori-shokunin/0` is a tracked 31-byte instrument
   output (`NF=13 cells=11 double_quotes=0`) added by round 38 (`96f7f97e`, 2026-10-23, "misroot relocations (0,
   m9)"), and `mori-shokunin/--repo/` is an empty untracked directory from 2026-10-24. Neither was created or
   modified here; both sit in the path a future `git show <rev>:0` sweep would trip over.
