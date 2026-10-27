# Mo57Sentinel61 — C1 calibration sentinel report

Report: `.ufo/waves/round-57/w1/Mo57Sentinel61.md`
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (entering `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`, freeze `618562c72a03dc4d17386b715357f863fd327274`)
Scope: C1 only — independently inspect the two round-56 demonstrations, verify the SCORECARD capability row names and evidence pointers, report any false claim. No writes outside this report; no production edit, no git/jj mutation in the lane or fleet.

## Verdict

The two round-56 demonstrations are **real and reproduce** over committed bytes. The capability **names are defensible only with the qualifiers the round-56 artifacts themselves use**, and the **frozen C1 counter does not measure the predicate its own contract states**: it reads the superseded `— none yet —` table, does not resolve evidence pointers, and does not bind the first-working-round cell. A `C1=met` from `count-c1.py` would therefore not establish C1 as worded.

| Item | Verdict |
|---|---|
| driver-liveness demonstration runs (round 56) | **holds** — selftest 13/13, fixtures, live receipt 1728/0 malformed/23 lanes; re-run today 1742/0/23 |
| vote-binding demonstration runs (round 56) | **holds** — selftest 16/16; frozen tally reproduced byte-exact over round-55 committed bytes |
| Row name `driver-liveness` + first-working 56 | **false unless qualified** "strict per-event probe": a per-lane launch read of the same log predates round 56 (census, `WATCHDOG_STATE_LAG`) |
| Row name `vote-binding` + first-working 56 | **false unless qualified** "dual-shape/anchored": a seat-output vote binder already bound round-55 bytes (`entailed=15`) |
| "the current SCORECARD capabilities table" is what the counter reads | **false** — counter binds the table SCORECARD:1958-1960 declares superseded; rows in the declared current register are invisible |
| "resolvable … evidence pointer" is measured | **false** — fabricated pointer passes with `evidence=ok` (fixture receipt below) |
| "first-working round 56" is measured | **absent** — `| 56 |` anywhere in the row suffices; First-working-round cell may read 44 |

## Positives verified (commands and exact output)

1. Round-56 driver probe, at lane HEAD:
   `python3 tools/mori-driver-liveness.py --selftest` → `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`, rc 0.
   `python3 tools/mori-driver-liveness.py` (live fleet log) → `verdict DRIVER_LIVENESS_OK lines 1742 malformed 0 other 121 lanes 23`. The committed capture `.ufo/waves/round-56/evidence/driver-liveness-live.txt` carries `lines 1728`, `malformed 0`, `other_lines 121`, 23 lanes, `mori unclosed 10`, `in_flight true` — capture-time numbers, not false (the log has grown by 14 lines since).
2. Round-56 vote binder, at lane HEAD:
   `python3 tools/mori-vote-bind.py --selftest` → `VOTE_BIND_SELFTEST pass=16 fail=0`, rc 0.
   Re-derivation from committed bytes (ledger `corpus/knowledge/kernel-v7.3-recheck-r55.md`, results `.ufo/waves/round-55/w1-results.json`, voters `Mo55Rc01..16`):
   `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15` — byte-equal to `.ufo/waves/round-56/evidence/tally-r55.txt`.
3. Frozen pins match HEAD: `sha256sum tools/mori-driver-liveness.py` = `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` (= `count-c1.py:46` PIN); `tools/mori-vote-bind.py` = `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca` (= `count-c2.py:45` PIN).
4. Round-56 counters reproduce at the entering tip:
   `python3 .ufo/waves/round-56/count-c1.py 53e2b476…` → `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok`, rc 0;
   `python3 .ufo/waves/round-56/count-c2.py 53e2b476…` → `C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok`, rc 0.
5. The pre-round-56 contrast is honest: `python3 .ufo/waves/round-55/count-c1.py 5b295eee…` → `… voted=0 dissent=0 … failed=votes`, rc 1; `count-c2.py 5b295eee…` → `… entailed=15 dissent=8 … failed=entailment`.
6. Capability ownership is recorded once, at round 56: fleet `MANIFEST.json` `rounds[832]` (`admitted: true`, `commit mori-shokunin@eac193ca…`) carries exactly two matching `capabilities_added` strings; no earlier admitted mori closure carries a vote/driver capability.
7. Natural evidence pointers resolve at both the closure commit and HEAD: `git cat-file -e eac193ca:.ufo/waves/round-56/evidence/driver-liveness-live.txt` / `…/tally-r55.txt` / `…/c1-at-landed.txt` / `…/c2-at-landed.txt` all ok.
8. Before-state controls are honest: `count-c1.py 53e2b476` / `618562c7` → `C1=unmet rows=0 evidence=bad`, rc 1; `git cat-file -e 53e2b476:corpus/knowledge/watchdog-unclosed-r57.md` → rc 128 (entry absent).

## Findings

### F1 (HIGH, calibration) — the counter reads the superseded capabilities table, not the lane's current register

`count-c1.py:10` is `p.stdout.split("## Capabilities", 1)[1].split("## Saturation", 1)[0]`. The first `## Capabilities` heading is `SCORECARD.md:596`; the first `## Saturation` after it is `SCORECARD.md:604`. The measured slice is therefore lines 596-603 only — the `| — none yet — |` table (`SCORECARD.md:600`), which `SCORECARD.md:1958-1960` states is superseded ("this register supersedes the `— none yet —` table in the first `## Capabilities` section (left as filed at `d677cf3`)"). The lane's declared current register is `SCORECARD.md:1951` ("This is the lane's current capabilities register"), holding 18 `| \`rounds[…]\`` rows (`SCORECARD.md:1969-1988`, rows `:1971-1988`).

Counterexample, run against a scratch fixture repo (exact copy of the frozen counter with only the hardcoded repo path changed; base commit = `SCORECARD.md` at `53e2b476`):

* two rows appended to the **current register** (after `SCORECARD.md:1988`) → `C1=unmet rows=0 evidence=bad`, rc 1;
* two rows appended to the **superseded first table** → `C1=met rows=2 evidence=ok`, rc 0.

Impact: a met C1 can be earned in a table the lane itself declares dead, while the register keeps zero round-56 rows — so the round could claim calibration improvement with the "current capabilities register" still not naming either capability. It also contradicts the predicate sentence in `.ufo/waves/round-57/contract.md` ("the current SCORECARD capabilities table").

Smallest remediation (advisory, not executed): bind the slice to the **last** `## Capabilities` section (the convention `count-c1.py`-comparable `.ufo/waves/round-35/count-c1.py:68` already uses: "the last level-2 section of SCORECARD.md whose heading begins `## Capabilities`"), or, if the register is not the intended target, re-word the predicate to name the section it measures.

### F2 (HIGH, false-claim surface) — "resolvable evidence pointer" is not measured

`count-c1.py:12` only tests the substring `.ufo/waves/round-56/` in the row. Two fixture receipts, both `rc 0`:

* rows citing `.ufo/waves/round-56/DOES-NOT-EXIST.txt` and `.ufo/waves/round-56/ALSO-MISSING/` → `C1=met rows=2 evidence=ok` (confirmed absent: the fixture repo at that commit contains one file, `SCORECARD.md`; `git cat-file -e <rev>:.ufo/waves/round-56/DOES-NOT-EXIST.txt` → "does not exist");
* rows citing real but non-evidential fixture logs (`.ufo/waves/round-56/fixtures/driver/malformed/watchdog.log`, `…/in-flight/watchdog.log`) → `C1=met rows=2 evidence=ok`.

Impact: the predicate's central assurance ("each with a resolvable round-56 evidence pointer", and the contract's "resolving evidence") can be false while the counter prints `evidence=ok`. This is exactly the failure mode that would let a hurried round-57 edit cite an invented receipt.

Smallest remediation: for each row, extract the backticked path(s) and require `git cat-file -e <R>:<path>` (path or path:line-range), and require the path to be under `.ufo/waves/round-56/evidence/` or to name one of the two displayed tools/entries.

### F3 (MED) — the first-working-round cell is not bound

`| 56 |` is a substring test over the whole row line. Fixture receipt: `| driver-liveness | counts lines | 56 | .ufo/waves/round-56/evidence/driver-liveness-live.txt | 44 |` plus a normal vote-binding row → `C1=met rows=2 evidence=ok` with the First-working-round cell reading **44**. Impact: the "first-working round 56" half of the predicate is unverifiable by the counter. Smallest remediation: parse cells and require the last cell to equal `56`.

### F4 (MED, false-claim surface) — both forced names overstate "first-working round 56" unless the row text carries the round-56 qualifier, and the counter cannot see the cell

The counter forces the tokens `driver-liveness` and `vote-binding` (`count-c1.py:11`) and ignores the "what it can now do" cell entirely, so a row may assert a broader capability than round 56 established:

* **driver-liveness.** Reading the same `.ufo/watchdog.log` launch lines for liveness predates round 56. The census silence surface took the log as its launch/close ledger at the round-3 cutover (`1439c473`: "census r2 silence cutover … launch/authorship-aware `probe_silence`"), and today's file anchors are `tools/mori-census.sh:32` (per-lane launch/closure/authorship grading), `:219` (`MORI_TIMELINE_FILE` default `$WATCHDOG_LOG`), `:297-298`, `:660-700` (`ledger_last_launch_round`, grammar `launch <lane> round=N`) and `:751-760` (`WATCHDOG_STATE_LAG` / `WATCHDOG_STATE_AHEAD`; the comparison arm added at `d30b4e43`, 2026-10-15 round 7). The round-56 entry discloses this (`corpus/knowledge/driver-liveness-r56.md:14-19`: "the probe is not the first reader of the log — its new surface is the strict per-event reading"), and `corpus/README.md:345` qualifies it ("the census's launch-epoch silence reading already existed (round 2)"). A row reading `| driver-liveness | reads .ufo/watchdog.log and reports lane liveness | … | 56 |` is false; only "strict per-event pairing probe" is true at 56. Fixture receipt: the fabricated row "reads every lane and reports it alive" passed (`C1=met`).
* **vote-binding.** A seat-output vote binder already worked at round 55 for the ENTAIL arm: `count-c2.py 5b295eee…` prints `entailed=15`, and `SCORECARD.md:2889` records it; `corpus/knowledge/vote-binding-r56.md:20-21` says the same. `corpus/knowledge/vote-binding-r56.md:6` ("new capability … (no prior lane note)") is true for *notes*, not for prior working binding. At round 56 what is new is the anchored, dual-shape, prose-guarded rule (`tools/mori-vote-bind.py:1-45`) and the RECHECK re-bind — that is the qualifier the row must carry, mirroring MANIFEST's own string "dual-shape seat-output vote binding".

Impact: the two row names the counter requires are exactly the two names that need a qualifier to keep "first-working round 56" true; the counter cannot check it, so the row text is the only guard. Smallest remediation: require the row's what-cell to contain `strict per-event` for the driver row and `dual-shape` (or `anchored`) for the vote row.

### F5 (MED) — the driver receipt carries an OK-token verdict the entry disclaims

`tools/mori-driver-liveness.py:237` sets `report["verdict"] = "DRIVER_LIVENESS_OK"` (also written into the committed receipt, line 304 region) and `:239` notes "in_flight/unclosed are log-shape facts, not health verdicts"; `corpus/knowledge/driver-liveness-r56.md:25-27` says "the probe makes no health verdict". The round-56 norem arm bans only `("healthy", "unhealthy", "failed lane", "is stuck", "wedged")` (`count-c1.py:45`), so `DRIVER_LIVENESS_OK` is outside it. A capability row that cites the receipt as evidence that lanes are alive would be false. Smallest remediation: require the row to state the shape-fact limit (as `corpus/README.md:800` already does: "no health verdict and no state-value reads") and read `DRIVER_LIVENESS_OK` as probe completion, not lane health.

### F6 (LOW) — the `— none yet —` placeholder may coexist with the rows

Fixture receipt: the placeholder left in place plus the two rows → `C1=met rows=2`. The table would then say "none yet" and list two capabilities. Smallest remediation: require the placeholder row to be gone when the row count is 2.

### F7 (LOW) — AXES allows a command pointer; the counter requires a path under round-56

`AXES.md:62` (fleet root) defines the evidence cell as "evidence pointer (command or path)" (`AXES.md:80` carries the same field in the SCORECARD contract table). `count-c1.py:12` requires the literal `.ufo/waves/round-56/`, so a reproducing command such as `python3 tools/mori-vote-bind.py tally —ledger … --results …` cannot satisfy the counter unless it is accompanied by a round-56 path. Not a false claim by itself, but it narrows the contract's field definition without saying so.

### F8 (INFO) — register completeness is not a property of this claim

The declared current register holds 18 rows, pinned to `MANIFEST.json at fleet commit 37b51a24` (`SCORECARD.md:1954-1956`). Fleet MANIFEST records 41 `capabilities_added` entries across admitted mori closures; 23 of them belong to rounds 36-56 and are absent from the register. Appending two round-56 rows without re-pinning or re-scoping that prose leaves the register's stated invariant ("holds one row per capability that a non-author closure admitted") false for the other 21. This is pre-existing from round 36, not introduced by round 57, but any round-57 wording that calls the table's state "completeness" is false; a scoped wording ("the two round-56 capabilities are now recorded") is true.

## Limits of this report

* The counterexamples above were produced in a throwaway fixture repo under `/fast/scratch/hyaku/mori-r57/Mo57Sentinel61/fx/repo` (toplevel asserted; one file, `SCORECARD.md`, per revision) with a byte-copy of `count-c1.py` whose only change is the hardcoded repo path; the lane tree and counters were not modified.
* "First working" is judged from committed evidence only (MANIFEST closures, lane counters, census code, SCORECARD's own round rows). I did not re-run the round-55 wave, and I cannot verify what any seat held in context.
* The live log reading (1742 lines today) is a capture of a growing file; only the committed receipt's internal numbers (1728/0/121/23) were treated as a claim.
* No provider, host, or fleet-state inference is made; missing sibling reports are not evidence of anything.

## Scratch / tooling

* Scratch: `/fast/scratch/hyaku/mori-r57/Mo57Sentinel61/` (created with `mkdir -p`, `TMPDIR` set there), containing the tally reproduction inputs, the two tool copies, one fixture git repo, and a byte-copy counter. Removed before yielding.
* Tool installs/updates: none. No `pacman`, no network fetch. Commands used: `git show`/`cat-file`/`ls-tree` (read-only), `python3` on lane tools and counters (read-only; counters materialise under my `TMPDIR`).
