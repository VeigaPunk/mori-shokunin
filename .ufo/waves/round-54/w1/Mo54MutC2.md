# Mo54MutC2 — mutation test of the frozen C2 counter (round 54, wave w1)

- Seat: Mo54MutC2 (mutation-tester, leaf — no subagents dispatched)
- Lane: mori-shokunin; target: `.ufo/waves/round-54/count-c2.py` at the frozen data rev 78295c764093ff1f6cee08d7246679900bde7265
- Date: 2026-10-27; MACHINE_ID: 432d02b544a5459ebbff9c42ec68334d
- Detector (frozen rule): `python3 count-c2.py --selftest`; mutant **killed iff exit != 0**.
- Scratch: `/fast/scratch/hyaku/mori-r54/Mo54MutC2/` (lane mirror `lane/` + `mutants/` + `tmp/`; TMPDIR pointed inside scratch; removed at the end — see Restoration and cleanup).
- No tools installed or upgraded (none needed); no pacman transaction; no network fetches (all six pinned copies already on disk in the lane and copied byte-for-byte into the scratch mirror); no git/jj mutation anywhere — only read-only `git show`/`rev-parse` inside the lane and file copies into scratch.

## Method

1. Copied the pristine counter (sha256 `d6b42f893b304ca355c03a4e43ad431b268b39ecfe8163c6871bbc0d6550785e`) into a scratch lane mirror at the same relative depth (`lane/.ufo/waves/round-54/count-c2.py`) so the script's `selftest()` lane-root derivation resolves inside scratch, together with byte-copies of the six pinned sources it reads (`corpus/evidence/sources-r54/{memory-failure.c,hwpoison.rst,sysfs-devices-node.v7.3,memory-failure-trace.h}.v7.3`, `corpus/evidence/sources-r53/{vm.rst,proc.rst}.v7.3`).
2. Applied single-point mutations as exact-string replacements (each asserted to occur exactly once in the pristine text); each mutant written to the executable slot and archived under `mutants/<name>.py`; run once with `--selftest` (the selftest is deterministic — survivors and one killed mutant were re-run to confirm identical verdicts).
3. Classified each nonzero result as check-fail (selftest completed, named FAIL lines) or crash (no FAIL lines). No mutant crashed; every kill is a named selftest check failing.
4. For each survivor, ran a probe (`probe.py`) that loads the pristine and mutant modules via importlib and calls their `evaluate()` on hand-built fixtures to show exactly which frozen selftest fixture/assertion fails to discriminate.

## Baselines (pristine)

| Run | Command | Exit | Evidence |
|---|---|---|---|
| lane selftest | `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/count-c2.py --selftest` | 0 | `C2_SELFTEST pass=54 fail=0` |
| scratch-mirror selftest | same script in `lane/` mirror | 0 | `C2_SELFTEST pass=54 fail=0` |
| at-data run | `python3 …/count-c2.py 78295c764093ff1f6cee08d7246679900bde7265` | 1 | `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=78295c76… failed=entailment` |

The at-data line matches the frozen receipt (`claims=21 located=21 … entailed=0 … failed=entailment`): the counter is intact at the data rev; the entailment arm is simply still awaiting votes. Not a defect.

## Mutation table

Pristine sha12 `d6b42f893b30`; "→" column is the mutant sha12. All 14 assigned mutations killed; 2 extra probes survived; 1 extra fence probe killed.

| Mut | Single-point edit (old → new) | Verdict | Detector evidence (exit / failing checks) | sha12 → |
|---|---|---|---|---|
| M01 | `MIN_VOTES = 2` → `1` | killed | 1; `entail_one_voter_unmet` + 12 more entail checks | 5b41670d0f4b |
| M02 | results binding dropped: `if path not in present or voter not in settled:` → `if path not in present:` | killed | 1; `entail_voter_not_in_results_unmet`, `entail_results_absent_unmet`, `entail_results_malformed_unmet`, `entail_unsettled_dissent_ignored_met` | 86ac6be77c2d |
| M03 | REPLACE-authorship dropped: remove `and h not in authored.get(who, set())` from `ok_voters` | killed | 1; `entail_author_vote_not_counted_unmet` | 965c20d1401e |
| M04 | vote-reading fence toggle dropped (in `entail_votes`): `fence = not fence` → `fence = False` | killed | 1; `entail_fenced_votes_ignored_unmet`, `entail_fenced_dissent_ignored_met`, `entail_fenced_replace_not_authorship_met` | 1dd1ae82d5ac |
| M05 | `MIN_BEYOND = 3` → `0` | killed | 1; `claim_echoes_quote_unmet` | 1de745a4788a |
| M06 | `MIN_CLAIMS = 14` → `1` | killed | 1; `claims_floor_unmet` | 20530c85608c |
| M07 | `MIN_SOURCES = 4` → `1` | killed | 1; `sources_floor_unmet` | 1351bf9ee7de |
| M08 | quote uniqueness dropped: remove `q in seen_quotes or` from the row guard | killed | 1; `duplicate_quote_unmet` | d96d8d899d36 |
| M09 | claim uniqueness dropped: remove `or ckey in seen_claims` from the row guard | killed | 1; `breadcrumb_identical_claims_unmet` | 2839278b0441 |
| M10 | `OPENED` widened: `("2026-10-26", "2026-10-27")` → `("2026-10-25", "2026-10-26", "2026-10-27")` | killed | 1; `row_opened_other_day_unmet` | c41476b4725f |
| M11 | used-by dropped: remove `and entry_path in [u.strip() …srow[10]])` from `row_ok` | killed | 1; `used_by_missing_unmet` | 0b51f669696c |
| M12 | pins content check dropped: `if b is None or hashlib.sha256(…).hexdigest() != digest:` → `if b is None:` | killed | 1; `pin_mismatch_unmet` | 3167e369f909 |
| M13 | provenance subset dropped: remove `and ids_in_table <= cited` from the `prov = "ok"` guard | killed | 1; `table_id_uncited_in_source_unmet` | 045095677d2d |
| M14 | overclaim dissent ignored: `if any(k == "overclaim" for k, _ in v):` → `if False:` | killed | 1; `entail_dissent_unmet` | 3173ca28cdd2 |
| M15 | extra: `MIN_CLAIM_WORDS = 6` → `1` | **SURVIVED** | 0 (twice: `C2_SELFTEST pass=54 fail=0`) | 79dac95a7970 |
| M16 | extra: `MIN_WORDS, MAX_WORDS = 6, 25` → `6, 99` | **SURVIVED** | 0 (twice: `C2_SELFTEST pass=54 fail=0`) | 51effa979400 |
| M17 | extra: table-reading fence toggle dropped (in `parse_claims`): `fence = not fence` → `fence = False` | killed | 1; `table_inside_fence_unseen_unmet` | 68ec6eed8181 |

Determinism re-runs: M15 exit 0, M16 exit 0, M01 exit 1 (`pass=41 fail=13`) — identical to first runs. Diffs of both survivors against pristine are exactly the one constant line each (`55c55` / `57c57`).

## Survivors — arm text each needs

Both survivors are detector-coverage gaps in the selftest, not live-predicate gaps: the probe shows pristine `evaluate()` still rejects the discriminating fixtures (unmet, `bad_rows=1`) while the mutant accepts (met). The frozen counter currently enforces both constants correctly.

### M15 (`MIN_CLAIM_WORDS` 6 → 1)

Cause: the only selftest fixture with a short claim (`claim_cell_short_unmet`, claim `"short claim"`) is also rejected by `words_beyond` (= 2 < 3), so the word floor is never isolated; the check passes for the wrong reason under the mutant.

Probe output (fixture builder replicating the frozen selftest's `build()`):

```
== Case A: frozen claim_cell_short fixture (claims[3]='short claim') under M15 ==
A [pristine] unmet | C2=unmet claims=14 located=13 quote_missing=0 bad_rows=1 sources=6 source_rows=bad pins=ok provenance=ok entailed=13 dissent=0 rev=R failed=bad_rows,entailment,source_rows
A [M15     ] unmet | C2=unmet claims=14 located=13 quote_missing=0 bad_rows=1 sources=6 source_rows=bad pins=ok provenance=ok entailed=13 dissent=0 rev=R failed=bad_rows,entailment,source_rows
== Case B: M15 arm — short claim whose words are absent from its quote ==
words_beyond(claim_b3, qs[3]) = 4 ; word count = 4
B [pristine] unmet | C2=unmet claims=14 located=13 quote_missing=0 bad_rows=1 sources=6 source_rows=bad pins=ok provenance=ok entailed=13 dissent=0 rev=R failed=bad_rows,entailment,source_rows
B [M15     ] met | C2=met claims=14 located=14 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=14 dissent=0 rev=R
```

Arm needed (round 55): a check whose short claim has fewer than 6 words **and** `words_beyond >= 3` against its own quote — e.g. claims[3] = `kernel kills poisoned pages` (4 words, beyond = 4) with all other rows unchanged; assert `not met and "bad_rows=1" in line`. That fixture kills M15 (Case B) and leaves pristine unmet.

### M16 (`MAX_WORDS` 25 → 99)

Cause: two stacked weaknesses. (a) The only overlong-quote fixture (`long_quote_unmet`, `"poison" × 26`) is fabricated text that also fails location, so under the mutant the row's failure mode flips from `bad_rows=1` to `quote_missing=1`/`bad_rows=0`; (b) the check asserts the substring `"bad_rows" in line`, and `"bad_rows=0"` contains `"bad_rows"`, so the flipped line still satisfies the assertion.

Probe output:

```
== Case C: M16 arm — real 26-word located quote in row 3 ==
quote C words = 26 ; words_beyond(claim_text(3), q) = 9
C [pristine] unmet | C2=unmet claims=14 located=13 quote_missing=0 bad_rows=1 sources=6 source_rows=bad pins=ok provenance=ok entailed=13 dissent=0 rev=R failed=bad_rows,entailment,source_rows
C [M16     ] met | C2=met claims=14 located=14 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=14 dissent=0 rev=R
== Case D: frozen long_quote fixture (poison x26, not located) under M16 ==
D [pristine] unmet | C2=unmet claims=14 located=13 quote_missing=0 bad_rows=1 sources=6 source_rows=bad pins=ok provenance=ok entailed=13 dissent=0 rev=R failed=bad_rows,entailment,source_rows
D [M16     ] unmet | C2=unmet claims=14 located=13 quote_missing=1 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=14 dissent=0 rev=R failed=quote_missing
```

Arm needed (round 55): a check whose overlong quote is a **real located** span — e.g. 26 words taken from the memory-failure copy at the `pr_err("%#lx: Sending SIGBUS …` line (beyond = 9) — asserted as `not met and "bad_rows=1" in line`; that kills M16 (Case C). Independently, tightening the loose substring assertions (below) removes the masking that let the fabricated fixture pass.

## Named limits (frozen-counter weaknesses found; routed items for round 55 — no change proposed or made this round)

- The selftest has no fixture that isolates `MIN_CLAIM_WORDS` (short-claim fixture conflated with `words_beyond`) — a drift of that constant is invisible to `--selftest`. (M15)
- The selftest has no fixture that isolates `MAX_WORDS` with a located quote, and its assertion style masks failure-mode flips — a drift of that constant is invisible to `--selftest`. (M16)
- Eight selftest checks assert the substring `"bad_rows" in line` (`short_quote_unmet`, `long_quote_unmet`, `duplicate_quote_unmet`, `row_not_mined_unmet`, `row_opened_other_day_unmet`, `used_by_missing_unmet`, `claim_cell_short_unmet`, `claim_echoes_quote_unmet`), which also matches `bad_rows=0`; exact-count assertions (`bad_rows=1`) would discriminate failure modes. (enabler of M16)
- Scope note: the battery covered the two fence toggles separately (M04 vote-reading, M17 table-reading) — both killed; no other untested single point was identified in the assigned list.

## Findings

- MED — `count-c2.py` selftest cannot kill a `MIN_CLAIM_WORDS` drift (M15 survived, exit 0 twice); concern: `.ufo/waves/round-54/count-c2.py` selftest fixture `claim_cell_short_unmet` (masked by `words_beyond`). Arm text above; route to round 55.
- MED — `count-c2.py` selftest cannot kill a `MAX_WORDS` drift (M16 survived, exit 0 twice); concern: selftest fixture `long_quote_unmet` (fabricated, unlocated quote) plus substring assertion. Arm text above; route to round 55.
- MED — substring assertion `"bad_rows" in line` matches `bad_rows=0` in eight selftest checks; concern: `.ufo/waves/round-54/count-c2.py` selftest assertion style; route to round 55.
- LOW — live predicate intact: pristine `evaluate()` rejects both discriminating fixtures and the at-data run matches the frozen receipt (`claims=21 located=21 … entailed=0 … failed=entailment`, exit 1); the survivors are detector-coverage gaps only.
- All 14 assigned mutations killed by named selftest checks; no counter change proposed or made; counters/predicates/controls/kill rules untouched.

## Restoration and cleanup

- After the battery the executable slot was rewritten with pristine bytes: sha256 `d6b42f893b304ca355c03a4e43ad431b268b39ecfe8163c6871bbc0d6550785e` — identical to the pre-run pristine hash (`RESTORED_SHA … OK` in the driver output); post-restore selftest exit 0, `C2_SELFTEST pass=54 fail=0`.
- The lane repo itself was never written: all mutation work happened on scratch copies; the only lane write is this report file.
- Scratch `/fast/scratch/hyaku/mori-r54/Mo54MutC2/` removed after the report was written (verified absent below).
