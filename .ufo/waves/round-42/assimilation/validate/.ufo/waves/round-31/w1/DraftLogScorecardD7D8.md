# Round 31 wave 1 — D7/D8 draft findings

## Scope and outcome

Prepared append-only draft text for routed defects D7 (LOG) and D8 (SCORECARD). No product, contract, or scorecard file was edited; only this report is written. No test, gate, validator, counter, or other runtime check was run. No tool was installed. This is source and receipt inspection, not execution evidence.

## Evidence and provenance

- Read the requested last-60-lines view of `LOG.md`, then the relevant current tail (`LOG.md:1983-2007`). The round-30 build/measurement entry currently ends with the tip-receipt note at `LOG.md:1983-1988`; the round-31 declaration/freeze follows at `LOG.md:1990-2007`.
- Read the measured-outcome row at `SCORECARD.md:1820` and tip receipt `.ufo/waves/round-30/evidence/tip-c1.txt:1-18`.
- Read the condition-4 text at `.ufo/waves/round-30/contract.md:76-78` and A2 at `.ufo/waves/round-30/contract.md:170-172`.
- Read `.ufo/waves/round-30/check-blind-wave.sh:172-180,215-229` to compare the stated round-29 count with the documented self-test expectations.
- Exact read-only command for D7:

  ```sh
  timeout 120s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/mori-shokunin show --stat 713be294
  ```

  Outcome: commit `713be294669272b8b29e9a8cd60c5313704a2ee1`, dated `Thu Oct 22 19:02:20 2026 -0300`; subject says round-30 wave-2 spec, validator run and dispatch payload (36 seats: 18 reviewer, 7 scout, 6 critic, 4 mutation-tester, 1 sentinel), plus wave-1 registry. Stat: `.ufo/waves/round-30/w1/swarm-registry.json` (219 lines), `wave2-dispatch.json` (221), `wave2-run.err` (empty), `wave2-run.json` (439), and `wave2-spec.json` (188); 5 files changed, 1067 insertions.
- The tip receipt’s command identifies measurement at parent `926ac1460c0b9a542725257870f530f98e94e4b1` (receipt lines 1-2). Its line 16 is `rows=13 rows_ok=13 new_ids=4 new_id_rows=12 excerpts_ok=4/4 skill_rows=4`; lines 17-18 report `C1=met`, exit 0.
- The old SCORECARD row at line 1820 says `new_ids=5 new_id_rows=13 excerpts_ok=5/5`; it is an earlier measurement at `ee61010d` (blob `6c47dd03`), not the metric printed in the later tip receipt.
- A2 says the round-29 self-test checks an exact expected `(file, rule)` set and excludes the 20 adjudicated false positives (`contract.md:170-172`). The gate lists nine expected pairs (`check-blind-wave.sh:172-180`); its self-test requires `scanned=8` and `blind_violations=9`, validates all nine pairs once, and rejects any of the false-hit paths (`check-blind-wave.sh:215-229`). This is source inspection, not a gate run.

## Ready-to-paste LOG.md append (D7)

Append after the existing round-31 material; do not insert into or rewrite the round-30 history.

```markdown
## Round 31 (attempt 1, L1 MoriR31) — appended correction to the round-30 log

- **D7, append-only correction:** round-30 wave-2 spec, validator run and dispatch payload landed in `713be294669272b8b29e9a8cd60c5313704a2ee1`; the commit subject records 36 seats (18 reviewer, 7 scout, 6 critic, 4 mutation-tester, 1 sentinel) and the wave-1 registry. `git show --stat 713be294` lists `.ufo/waves/round-30/w1/swarm-registry.json`, `.ufo/waves/round-30/wave2-dispatch.json`, `.ufo/waves/round-30/wave2-run.err`, `.ufo/waves/round-30/wave2-run.json` and `.ufo/waves/round-30/wave2-spec.json` (5 files changed, 1067 insertions). This records the later wave-2 artifact commit without changing the round-30 measured outcomes above.
```

## Ready-to-paste SCORECARD.md append (D8)

Append after the current scorecard material. Keep the original row and frozen contract unchanged; the quoted line numbers identify the historical text being clarified.

Old SCORECARD text (`SCORECARD.md:1820`):

```text
| C1 depth, invocation-scope decision table (sourced S156–S160) | `count-c1.sh 58b61681` → entry absent, `C1=unmet`, exit 1 (`.ufo/waves/round-30/evidence/c1-before.txt`) | `count-c1.sh ee61010d` (blob `6c47dd03`) → `rows=13 rows_ok=13 new_ids=5 new_id_rows=13 excerpts_ok=5/5 skill_rows=4`, `C1=met`, exit 0 (`evidence/c1-after.txt`) | improved, pending closure; depth held at 5 (no closure states a move) |
```

Old contract text (`.ufo/waves/round-30/contract.md:76-78`):

```text
   `--selftest` prints `PASS` (it reports 0 on the round-29 writer wave at `d6d5cb0a` whose 20 hits were adjudicated
   false positives, and it reports a violation for each planted leak class: tool line citation, tool output marker,
   forbidden path in a files-opened list, missing files-opened list); and run at the freeze commit on
   `.ufo/waves/round-30/w1` with writer regex `^CaseR30[a-d]\.md$` it prints `blind_violations=0`.
```

Proposed appended correction:

```markdown
## Round 31 (attempt 1, L1 MoriR31) — appended corrections to round-30 measured outcome (D8)

- **C1 tip-receipt correction (append-only; the historical row above is retained):** the row at `SCORECARD.md:1820` records the earlier `ee61010d` measurement (`new_ids=5 new_id_rows=13 excerpts_ok=5/5`). The later tip receipt `.ufo/waves/round-30/evidence/tip-c1.txt:1-2,16-18` measures the counter at parent `926ac1460c0b9a542725257870f530f98e94e4b1` and reports `rows=13 rows_ok=13 new_ids=4 new_id_rows=12 excerpts_ok=4/4 skill_rows=4`, `C1=met`, exit 0. Use the receipt values when describing the round-30 tip outcome; the C1 verdict remains met.
- **Frozen-contract consistency note (not a contract amendment):** condition 4's parenthetical at `.ufo/waves/round-30/contract.md:76-78` says the round-29 writer-wave check “reports 0.” Amendment A2 instead requires comparison with an exact expected set and exclusion of the 20 adjudicated false positives (`contract.md:170-172`). The gate documents nine expected `(file, rule)` reports (`check-blind-wave.sh:172-180`) and its self-test requires `scanned=8`, `blind_violations=9`, each expected pair exactly once, and none of the known false-hit paths (`check-blind-wave.sh:215-229`). The unqualified zero-report parenthetical is stale against that nine-report expectation; this note records the inconsistency without editing the frozen contract or claiming a gate rerun.
```

## Gates, touched surfaces, and limits

- **Gates:** none executed. The only command executed was the read-only `git show --stat` above; no runtime result is asserted for the gate or counters.
- **Touched surface:** `.ufo/waves/round-31/w1/DraftLogScorecardD7D8.md` only.
- **Out of scope / intentionally unchanged:** `LOG.md`, `SCORECARD.md`, `.ufo/waves/round-30/contract.md`, counters, gate, and all product files. No git/jj writes, commits, publication, or deployment.
- **Artifact:** `.ufo/waves/round-31/w1/DraftLogScorecardD7D8.md`.
