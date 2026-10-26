# Mo50bRevLimitsHonesty — contract named limits vs landed data at 487941b

MACHINE_ID: 432d02b544a5459ebbff9c42ec68334d
Seat: reviewer (leaf, no subagents). Scope: the `Named limits` paragraphs under C1 and C2 in
`.ufo/waves/round-50/contract.md`, checked against the landed data and the frozen counters at
`487941b9395e89678af0053cc443cdb49cdee6e3`; then limits the round report must add that the contract
did not name. Detection and report only.

Tooling: nothing installed (no need; pacman untouched). No LSP server is available in this seat (no
`lsp` device mounted), so every check below is text/git-level; grep output is used only for what it
literally shows, never as semantic proof.

## Method (commands run, all read-only)

- Frozen-byte check first: `sha256sum` of working-tree `count-c1.py`, `count-c2.py`, `contract.md`
  = `2d5c3ee5…`, `533c8403…`, `8290c6d4…`, equal to `evidence/freeze-sha256.txt` and to
  `git show 487941b:…` of the same three files — the counters I ran are the frozen counters.
- `python3 .ufo/waves/round-50/count-c1.py 487941b… --scratch <seat tmp>` →
  `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b…`, exit 0.
- `python3 .ufo/waves/round-50/count-c2.py 487941b…` →
  `C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b…`, exit 0.
  (First invocation with `--scratch` exited 2 `C2_SETUP usage` — C2 takes no `--scratch`; re-run without it.)
- Both counter outputs are byte-identical to the L1's receipts at the wave-spec commit
  (`evidence/a2-c1-at-data.txt`, `evidence/a2-c2-at-data.txt`).
- Read at R via `git show`: `SCORECARD.md` (Axes rows), `SHONEN.md`, `corpus/knowledge/oom-memcg-stat-r50.md`,
  `corpus/SOURCES.md` rows S003/S476/S489/S490/S491, both `evidence/selftests/*.txt` receipts,
  `evidence/control-c1-do-nothing.txt`, lessons r47/r49/r28, `SKILL.md`.
- Independent sha256 of the three committed copies at R = the frozen digests in `count-c2.py` COPIES
  (`2d716cb7…`, `8a28e0bc…`, `452f1348…`) — `pins=ok` reproduced outside the counter.
- Live re-fetch (the entry's own recheck command): `curl -fsSL <url> | sha256sum` for the three URLs
  today reproduced all three frozen digests exactly, rc 0 — the committed copies are byte-identical
  to the live pages as of now.
- Fleet pin staleness: `git -C /home/vgpnk/Projects/shokunin log --oneline e0144996…..HEAD -- MANIFEST.json`
  → 2 commits (`28ff97e3` mado r43 closure, `1ce0f8fb` kama r45 closure); diff vs pin = 86 changed
  lines, 0 containing `mori`; mori admitted rounds at pin and at fleet HEAD both end at 49; no mori
  round > 49 exists yet; `e0144996…` is an ancestor of fleet HEAD.
- Spot re-runs: `python3 tools/mori-sources-appendonly.py --selftest` →
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` (tools/ unchanged 487941b→HEAD, diff empty).
- Pointer checks: cited lesson lines read at R — r47:67 (operability row), r47:68 (coverage row),
  r49:75 (calibration row, "C1 verified; no score change claimed"), r49:76 (depth row, "C2 re-measured
  21/21"), r28:92 (freshness row) — all exist and say what the landed cells claim;
  `corpus/lessons/round-19-verifier-spotcheck.md` ABSENT at R (`git cat-file -e` rc≠0), matching the
  adjacency cell's fallback to `MANIFEST.json`; `MANIFEST.json@63729047` rounds[398] = mori round 19,
  verdict `admitted`, `verdicts.adjacency: improved` — the adjacency cell's precise pointer is exact.

## C1 named limits — status at 487941b

| # | contract limit | status | evidence |
|---|---|---|---|
| 1 | Score column not checked (MANIFEST holds verdicts, not scores) | **still true** | `check_axes` reads only cells r[2] (Evidence) and r[3] (Last change); r[1] is never validated (`count-c1.py:111-148`). Landed Score cells are 6/7/5/5/5/6 — unchanged from the entering scores — and the cited closures state held scores (r49:75 "no score change claimed", r49:76 "score 5", r47 rows "no new number"), so the landed data does not exploit the gap where manually checked. |
| 2 | Counter reads the Last-change convention, does not judge it | **still true** | The counter implements exactly the convention (highest admitted round ≤ 49 grading improved/harmed; `manifest_targets`). The landed cells apply it and additionally preserve the prior value ("round 47 (improved, score held); round 26 (improved, score held) before the round-50 correction"); whether the convention itself is the right one is unjudged, as named. |
| 3 | Pin split across lines / outside backticks in another file not enumerated; hidden scan covers SHONEN.md only | **still true, understated in scope** | `evaluate` scans only SHONEN.md (`count-c1.py:208-224`), and only three token forms (`(N/M)`, `pass=N`, `SELFTEST`, `HIDDEN` at `count-c1.py:52`). Tally tokens do exist outside SHONEN.md at R: `SKILL.md:202-205` is dated tally prose ("each measured 2026-10-25": `MORI_SILENCE_CASES… pass=24`, `R19_SELFTEST pass=26`, `ROUTED_CHECK… pass=20`, `ROUTED_R24… pass=26`) whose currency is UNVERIFIED in this seat, plus LOG.md history and lesson receipts. The one known drift site I re-ran is current: `SKILL.md:912` pin ↔ `pass=22 fail=0` re-printed today (the r47 M1 fix holds). So the limit is real and the report should extend it to SKILL.md's dated tally prose as the next likely drift site. |
| 4 | Matching tally proves the instrument prints it at R, not that its arms are good | **still true** | `run()` re-runs both tools from a `git archive` of R with TMPDIR in scratch and compares to the receipts; receipts at R end `PIN_CHECK_SELFTEST pass=114 fail=0` (117 lines) and `UNLANDED_SELFTEST pass=17 fail=0` (20 lines). Arm quality is unjudged, by design. |
| 5 | MANIFEST is fleet-written and trusted; closures not re-judged | **still true** | `manifest_targets` takes verdict dicts at face value; it also trusts axis-key spelling (a missing/typo'd key surfaces as `manifest_has_no_target` error — loud, not silent). |

## C2 named limits — status at 487941b

| # | contract limit | status | evidence |
|---|---|---|---|
| 1 | Located quote proves occurrence in the committed copy, not that the claim follows | **still true; two refinements** | The test is `q in norm[url]` — substring, occurrence count not required unique, and the HTML normalisation keeps nav/head text, so "occurs" is weaker than "occurs where the claim says". Mitigation named in the contract (wave-2 re-open) is running this wave; my partial re-open of the load-bearing rows found no contradiction — notably the rate-limit row: its quote shows `dump_oom_victim` *inside* the guard, but the claim's "victim line" is the `Killed process` line, which `__oom_kill_process` prints at `oom_kill.c:945`, called at `:1042` outside the `if (__ratelimit(&oom_rs))` block (`:1030-1033`); `dump_oom_victim` (`:444`) prints the `oom-kill:` context line, which IS rate-limited. The entry's own terminology (rows 16/20: "Killed process line" vs "oom-kill context line") is consistent and the claim holds. |
| 2 | Three-new-words floor is a floor, not entailment | **still true** | `words_beyond` counts 3+ letter words in the claim absent from the quote; ≥ 3 required; no entailment check anywhere. |
| 3 | v7.2 says nothing about other kernels or cgroup v1 | **still true, now disclosed in-entry** | The entry's own Limits section states "Kernel v7.2 only…" and "cgroup v2 only… nothing here carries over to v1". Spot-checked the v1 prose claim against the frozen copy: `memcontrol.c:1815` prints `memory+swap: usage %llukB, limit %llukB, failcnt %lu` with `memcg->memsw.failcnt` (`:1817`) and kmem lines (`:1819-1820`) — consistent. Disclosure does not resolve the limit; it states it. |
| 4 | No host OOM block read (no MESSAGE grep) | **still true, disclosed in-entry** | Entry Limits: "No host block was read…". This seat likewise ran no MESSAGE grep and triggered no OOM. |
| 5 | Wave-2 reviewers re-open every row and report the result as a limit | **in progress (this wave)** | This seat re-opened the load-bearing rows plus five prose claims (all consistent — see above); the full 22-row re-open belongs to the dedicated falsifier seats. The round report must still carry the re-open result as a limit, per the contract. |

No named limit became false. None is resolved in the sense of no longer applying; C2-3 and C2-4 are
now additionally disclosed inside the entry itself, which is the correct treatment.

## Limits the round report must add that the contract did not name

1. **C1 — MANIFEST pin staleness (MED).** The counter reads MANIFEST.json only at the pinned fleet
   revision `e0144996…` (`count-c1.py:43`, used in `main()`); the contract states the pin in the C1
   surface but the Named limits paragraph does not name its consequence. Post-pin fleet commits
   touching MANIFEST.json already exist (`28ff97e3` mado r43, `1ce0f8fb` kama r45 — 86 diff lines,
   0 mori lines, so the pin is not yet stale for mori data); any later mori closure or verdict edit is
   invisible to the frozen counter, and `THROUGH = 49` (`count-c1.py:40`) caps the window so round
   50's own closure can never be measured by it. The claim is calibrated against a snapshot ledger.
2. **C2 — prose sections are not enumerated (MED).** The counter checks the claims table and the
   first 14 non-empty lines for provenance keys; everything else in the entry — intro paragraph,
   Reading rules, Limits, Boundaries — carries substantive claims with no quote-location or source
   binding: the v1 `memory+swap`/`kmem` caveat, the `K()` pages→kB conversion, the `SEQ_BUF_SIZE`
   overflow warning, the CONFIG-conditional key list, "a missing block is not evidence that the kill
   was global". I spot-checked five of these against the copies (all consistent:
   `memcontrol.c:1815-1820`, `:1794` + `:1757-1758` + `:127`, `:400-1691` ifdefs, `oom_kill.c:1012/:1030`),
   but the counter would not catch a wrong one. The contract's C2-5 re-open commitment covers table
   rows ("every row"), not prose.
3. **C1 — the `(N/M)` pin form does not check the SELFTEST prefix (LOW).** The landed pins are in
   `(N/M)` form (`SHONEN.md`: `` `python3 tools/mori-pin-check.py --selftest` (114/114) ``); the
   counter's n-form comparison checks only the numbers (`check_pins`: `ok = n == o_pass and
   m == o_pass + o_fail`); only the token form checks prefix equality. Mitigated in practice by the
   receipt stem (the receipt keyed by the tool's basename must contain the observed
   `PREFIX pass=P fail=F` line), so a mis-pointed pin needs two tools printing identical counts.
4. **C1 — hidden-scan token coverage (LOW).** `HIDDEN` catches only `(N/M)`, `pass=N` and `SELFTEST`
   (`count-c1.py:52`); a stale tally written as e.g. "114 of 114" or "114 ✓" in SHONEN.md escapes.
   Extension of named limit 3, same file scope.
5. **C1 — Evidence-cell check is substring containment; Last-change cell unchecked after the first
   `;` (LOW).** `need not in evidence` requires the pointer string but validates neither the cited
   line number nor that the cited line supports the cell; text after the first `;` in the Last-change
   cell is free. The landed data is exact where spot-checked (r47:67/68, r49:75/76, r28:92, and the
   adjacency cell's `MANIFEST.json@63729047` rounds[398] pointer verified field-by-field), so this is
   a counter limit, not a landed defect.
6. **C1 — point-in-time calibration; drift resumes (LOW).** The claim is measured at R; nothing in the
   landed data prevents the SHONEN pins or the Axes cells from going stale at the next tool change or
   closure — the exact failure mode C1 mined (pins stale since round 48). Carrier 7 closes K4 for
   SHONEN.md only; the rest stays routed. The report should name C1 as a snapshot, not a standing guard.
7. **C2 — provenance keys are presence-checked only (LOW).** `has("verified-at")`/`has("recheck")`
   match any line starting with the key inside the first 14 non-empty lines; the values (dates, the
   recheck command, its claimed digests) are unvalidated by the counter. Corroboration in this seat:
   the recheck line's three digests equal the frozen COPIES digests, and my own re-fetch today
   reproduced all three exactly — the copies are byte-identical to the live pages as of now.
8. **C2 — S-id pinning is indirect (LOW).** The counter accepts any SOURCES row that is mined, opened
   2026-10-26, names one of the three frozen URLs and lists the entry in used-by; it does not require
   the new rows S489–S491. In the landed data only S489–S491 list the entry in used-by (3 occurrences
   of the entry path in SOURCES.md), so the table is effectively pinned; S003/S476 (same oom_kill.c
   URL, different scope) do not list it.
9. **C1 — selftest receipts are not digest-pinned (LOW).** `evidence/selftests/mori-pin-check.txt`
   and `mori-unlanded-check.txt` are absent from `evidence/freeze-sha256.txt` (the freeze commit
   `950e99be` predates the landing; the receipts ARE the landed data, added at `487941b`). Their
   integrity is enforced only at scoring time by the re-run comparison, not by a pinned digest.
10. **C2 entry provenance (INFO).** The entry's only commit is the orchestrator salvage `9b8562a`
    ("unlanded attempt-1 wave state and knowledge draft"); `git diff 9b8562a 487941b` on the entry is
    empty, so the C2 entry bytes at R are the attempt-1 draft, with attempt 2 adding SOURCES rows and
    the SCORECARD/SHONEN reconciliation around it. Not a defect (counter passes, copies pinned), but
    the round report should state this provenance honestly.
11. **C2 table-parser robustness (INFO).** `parse_claims` resets the header on a blank line before
    the first data row and then silently drops subsequent `|` lines — this can only cause a
    false-unmet (`claims_floor`), never a false-met, so it is a robustness note, not a scoring weakness.

## Findings

- **MED** — C1 named-limit gap: MANIFEST pin staleness unnamed. `count-c1.py:43` (`FLEET_REV =
  e0144996…`), `:40` (`THROUGH = 49`); post-pin fleet MANIFEST commits `28ff97e3`, `1ce0f8fb` (0 mori
  lines today); no mori round > 49 at fleet HEAD; round 50's own closure will be invisible to the
  frozen counter. Report must add this limit.
- **MED** — C2 named-limit gap: entry prose (intro, Reading rules, Limits, Boundaries) is not
  enumerated by `count-c2.py` (table + first-14-lines only); five prose claims spot-checked
  consistent against the copies, but uncountered. Report must add this limit and the re-open result.
- **LOW** — `count-c1.py` `check_pins`: `(N/M)` pin form skips prefix equality; landed SHONEN.md pins
  are `(N/M)` form (receipt-stem mitigation).
- **LOW** — `count-c1.py:52` `HIDDEN`: three token forms only, SHONEN.md only; `SKILL.md:202-205`
  dated tally prose (measured 2026-10-25) sits outside the scan, currency UNVERIFIED;
  `SKILL.md:912` re-ran current (`pass=22 fail=0`).
- **LOW** — `count-c1.py` `check_axes`: Evidence cell substring containment; Last-change cell
  unchecked after first `;`; landed pointers spot-checked exact (r47:67/68, r49:75/76, r28:92,
  `MANIFEST.json@63729047` rounds[398] verified).
- **LOW** — C1 is a point-in-time snapshot; no standing guard against renewed pin/cell drift
  (contract carrier 7: K4 closed for SHONEN.md only).
- **LOW** — `count-c2.py` provenance keys presence-only; recheck digests corroborated by live
  re-fetch today (all three match).
- **LOW** — `count-c2.py` accepts any qualifying SOURCES row; landed data pins the table to
  S489–S491 via used-by (3 occurrences; S003/S476 do not list the entry).
- **LOW** — `evidence/selftests/*.txt` receipts not in `evidence/freeze-sha256.txt`; integrity via
  scoring-time re-run only.
- **INFO** — C2 entry bytes at R are the attempt-1 salvage (`9b8562a`), unchanged at `487941b`.
- **INFO** — `count-c2.py` `parse_claims` blank-line header reset can silently drop rows (false-unmet
  only, never false-met).

Residual risk: the four SKILL.md dated tallies (`SKILL.md:202-205`) were not re-run in this seat —
their currency is UNVERIFIED; everything else above is observed. No counter or predicate change is
proposed anywhere in this report; every gap above is a named limit for the round report, per the
freeze rule.
