# Mo92K03Crit — round 92 wave w1, critic report

Seat: Mo92K03Crit (critic, leaf). Entering revision: f63d1ab030d4179576e494342f48ef8718e497a5.
Scratch clone: `<scratch>/repo`, detached at the entering revision, toplevel verified before every change; scratch deleted before yield. Lane not written. No patches produced (critic seat). No tooling installed or upgraded.

Counters: I did NOT execute `count-c1.py` or `count-c2.py` as commands. For C1 I loaded the `missing_keys` function from the lane file text in-process (read-only, no bytecode written) to test synthetic strings. Everything else is measured directly from git objects, the tool, and the registry.

## Verdicts (short)

| Claim | Verdict | Reason (evidence below) |
|---|---|---|
| C1 as worded (every knowledge entry carries the trio) | holds as presence, if landed | presence is all the counter measures; forgeable (§2) |
| C1 as a depth move (depth axis 5 → 6) | does not hold | trio adds traceability metadata, not depth; landing constraint forbids body edits; lane's depth bar is quotes + entailment (§1) |
| C2 as frozen (`C2=met … rc 0`) | does not hold as written | exit-0 clause is unattainable with prefix_only=31 unpinned=1 under the current tool rule; the only route contradicts QUALITY criterion 193 (§3, A6) |
| C2 freshness (AXES drift/stale-flagged) | does not move as drift detection; narrow integrity repair holds | the two stale digests are real and correctly superseded; no live-surface re-verification occurs (§3) |

## 1. C1 depth — decision: depth does NOT move; provenance presence moves

For "depth moves":
- AXES.md:11 defines depth as "verifiable technical detail … cited sources"; a `source:` plus `recheck:` line is a cited, re-runnable pointer.
- LEARNING.md:67-68 makes the trio the defined shape of a knowledge entry ("opens with `source:`, `verified-at:` … and `recheck:`"). Restoring the shape restores a structural bar.
- LEARNING.md:34 (quality trend) treats an entry "found … stale and left unmarked" as harm; 19 entries have no `verified-at` marker at all, so the marker is a real gain on that trend.
- QUALITY.md:4 and :108 / :193 treat resolvable pointers as the lane's validity check; a recheck line is the pointer a future reader resolves.

For "depth does not move":
- QUALITY.md:1079-1081 (criterion 128): "the counter proves location, not entailment"; depth entries are judged by located quotes and entailment, which this claim does not add.
- QUALITY.md:1329-1336 (criterion 140) and :1379 (criterion 143): depth rows need committed entailment votes from non-authors. A trio line is not a vote.
- Contract landing constraint (contract.md:34-39): "no body text, no claim, no admitted conclusion is changed." The decision tables, thresholds and error signatures that AXES.md:11 names as depth cannot change by construction. Only metadata changes.
- Contract:40 names the limit: "the counter checks presence, not provenance quality."
- Population already passing presence (79 of 98 at entering, measured heuristically from git objects, first 12 lines): 25 `recheck:` values are time-only (`90d`, `180d`, `365d`, e.g. `corpus/knowledge/boot-anchor-win-r73.md`), 8 are bare `on-release`, and ~59 `verified-at:` values are date-only with no commit. The counter already rewards lines that the landing rule (contract:36-38) would reject.

Decision: the claim's counter moves; the depth axis does not. Score guidance: keep depth at 5 on this claim alone. Traceability may be recorded as "provenance coverage 79→98 entries", not as depth.

Non-author verifier should check, to decide whether depth moved at all:
1. For 5 of the 19 new trio blocks (include at least 2 of the 7 files with post-admission edits, §2c), confirm the `source:` cites a registry row or path:line whose content the body actually uses (entailment, not just presence).
2. Run each new `recheck:` command at the landing commit; record rc. A `manual — path:line` value must resolve.
3. Confirm no body line changed: `git diff --numstat f63d1ab0 <landing> -- corpus/knowledge` shows only the 19 files, and every added line is a provenance key in the first 12 lines.

## 2. C1 gaming — the minimal forged trio passes the frozen counter

Forged header (a careless seat's minimum):
```
source: S999 (no such row)
verified-at: 2026-11-05
recheck: 90d
```
Result on the entering body of `corpus/knowledge/audit-r11.md` (missing=3 at entering): `missing_keys` returns `[]` (counter rule passes; python exec rc 0).

Other passing shapes (all `absent=[]`):
- empty values: `source:` / `verified-at:` / `recheck:` with nothing after the colon;
- trio inside an HTML comment (`<!-- … -->`) or inside a fenced code block at lines 1-12;
- trio on lines 1-12 but unrelated to the body.
Counter rule: key must start a line within the first 12 lines (count-c1.py `missing_keys`, `HEAD_LINES = 12`); value is never inspected.

Would a non-author reject the forged trio under the frozen rules? Yes, on each clause:
- `source: S999`: no row (`grep -c '^| S999 ' corpus/SOURCES.md` = 0); "source must cite something real" fails.
- `verified-at: 2026-11-05`: a date, not a commit; contract:36 requires the admission commit (`git log --diff-filter=A`) which contains the file.
- `recheck: 90d`: neither a command nor path:line; contract:38 fails it.
- empty values and comment/fence placement: fail "true at its commit" (contract:36) and are visible on a read.

Additional gaming and calibration points:
a. The counter accepts ANY value after the key. The 79 already-passing entries show the population is already weak (§1), so `C1=met` does not discriminate.
b. No no-harm clause for body text. The landing constraint "no body text changed" (contract:34-35) is not measured by `count-c1.py` at all. A seat can edit bodies and still meet C1.
c. 7 of the 19 files were edited after admission (`git log -- <file>` touches > 1): audit-r11 (2), drift-pin-r10 (2), execution-binding-r89 (2), kernel-v7.3-recheck-r53 (3), silence-grading-r2 (3), surfaces-r8 (2), workstate-win-r71 (2). The contract's verified-at rule names the admission commit, which certifies a body the file no longer has. The verifier must either accept that wording explicitly or name the later commit for these 7.
d. Admission commits exist for all 19 (`git log --diff-filter=A` returned one each). Presence of the commit is therefore not in doubt; what it certifies is.

## 3. C2 freshness — decision: freshness does not move; the integrity correction holds narrowly; the claim as frozen is unmet

Facts I verified at f63d1ab0:
- S615 recorded digest `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0` (corpus/SOURCES.md:397) does not equal the pinned copy `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5` (`.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html`, 362493 bytes). Real defect.
- S235 recorded digest `…4a30cda99359e6df057ad8020` (corpus/SOURCES.md:241) does not equal the pinned copy `…4a30dca99359e6df057ad8020` (`corpus/evidence/sources-r42/S235.pdf`, 6482693 bytes). Real defect (one c↔d transposition).
- Successors S619 (`7891…42f5`) and S620 (`9855…dca…`) equal the pinned bytes (recomputed with `git show f63d1ab0:<path> | sha256sum`).
- In scratch I appended S619/S620 after S618 and ran the entering tool: `DIGEST S619 ok`, `DIGEST S620 ok`, `DIGEST S615 mismatch`, `DIGEST S235 mismatch`, `DIGEST_CHECK rows=123 ok=89 mismatch=2 prefix_only=31 unpinned=1` (rc 1). So the successor classification precondition is met.
- No knowledge body quotes the wrong digests. `git grep` for the recorded values hits only corpus/SOURCES.md:241/:397, round-91/round-90 lessons, and historical `.ufo/waves/` files.

Why freshness does not move:
- AXES.md:14 defines freshness as "drift detection — skill claims re-verified against live surfaces; stale items flagged or fixed." The digest gate re-hashes committed, immutable pinned bytes. It cannot detect live-source drift, and this round adds no live re-fetch (successors are "pinned bytes only", S619/S620 rows).
- README.md:571 and :755 record the lane's own freshness practice as re-fetches or re-reads at a new tag. This claim does not do either.
- What does move: two stale items are flagged (`superseded-by`) and corrected by successor rows, which AXES.md:14 accepts as "flagged or fixed." That is an integrity repair. Record it as such. Do not raise freshness 5→6 on it.

Why the claim as frozen is unmet (the decisive finding):
- Predicate (contract:48-52, count-c2.py:138-139 `run_rc`): the tool run must exit 0 with `prefix_only=31 unpinned=1`.
- The tool exits 1 whenever prefix-only or unpinned rows exist: `tools/mori-source-digest.py:434-435` (`if counts["mismatch"] or counts["prefix-only"] or counts["unpinned"]: return 1`), and its docstring says the same.
- Scratch run A6 (S615 and S235 rows removed from the scratch registry, so mismatch=0): `DIGEST_CHECK rows=119 ok=87 mismatch=0 prefix_only=31 unpinned=1`, rc 1. So mismatch=0 alone does not make the run exit 0.
- prefix_only and unpinned cannot be repaired (contract:101-102, append-only; QUALITY 193 "a prefix agreement is prefix-only and fails the gate; … unpinned and fails it").
- So the exit-0 clause requires changing the tool's exit rule to ignore prefix-only and unpinned. That contradicts QUALITY.md:2245 (criterion 193). The contract's landing constraint (contract:67-69) constrains classification, not exit code, so the change is not forbidden by text, but it converts 32 failing rows into a green gate. That is a calibration harm (AXES.md:15, LEARNING.md:35 discernment).
- Resolution belongs to the operator/L1 (AXES.md:34-36 "let the operator rule"): either (a) a new QUALITY row superseding 193 with the debt named, or (b) the claim is recorded unmet. The critic recommends (b) unless (a) is ruled explicitly.

Landing risk (implementation): the supersession text "supersedes S615" lives in the registry's `teaches` column (cell 7, the 8th pipe field). `parse_rows` (tools/mori-source-digest.py:91-104) reads only cells 2 and 6 (source and anchor). A supersession implementation that reads only those cells will never see the supersedes rows; `superseded=2` then fails. Supersession logic must parse cell 7 and the counter's negative fixtures do not cover this.

## 4. Trade check — harm by axis, measurement, and missing no-harm clauses

Harm candidates and the measurement that would show harm:

| Axis | Possible harm | Measurement that would show it | Counter covers it? |
|---|---|---|---|
| coverage | knowledge population or README map changes | `ls corpus/knowledge/*.md \| wc -l` = 98 after landing; no README coverage rows added or removed by this round | population floor yes (98); README not checked |
| operability | per-row output of the tool changes for the 119 unchanged rows; exit rule changes | byte diff of the `DIGEST <id> …` lines for every row except S615, S235, S619, S620 vs the entering run; `--selftest` exit code | no: C2 checks counts only |
| adjacency | knowledge bodies or sibling lanes begin citing the wrong digests; successor pinned copies move out of `.ufo/waves/round-90/` | `git grep` for the two recorded wrong digests returns only SOURCES.md and historical lessons/waves; successor pins resolve | no |
| calibration | the gate reports green with 31 prefix-only and 1 unpinned rows; selftest passes on mutants | exit-rule diff; mutation kills of the supersession logic (missing successor, successor digest flipped, successor naming a different copy); a `supersedes` row for another ID must not suppress a mismatch | partial: negatives=2 only; selftest is self-reported (count-c2.py:126-130 accepts any `pass=N fail=0`, N≥8) |
| freshness | none beyond the two items above | n/a | n/a |
| depth | body edits (forbidden) | `git diff` over corpus/knowledge body lines | no: C1 has no body no-harm clause |

Which no-harm clauses exist: count-c2.py:144-145 checks `prefix_only == 31` and `unpinned == 1` by count. So prefix-only and unpinned counts are covered, but the check is count-only and blind to swaps (one row moved from ok to prefix-only and another from prefix-only to ok keeps the count at 31).

Missing no-harm measures (critic recommendation to the L1, none may be added to the frozen counters):
1. Identity of the 31 prefix-only and 1 unpinned rows against the entering list (set equality of IDs), not counts.
2. ok count = 89 and rows = 123 after landing (count-c2.py checks neither).
3. Per-row byte diff of every unchanged DIGEST line (the landing constraint says classification of other rows is unchanged; only a line diff proves it).
4. Body-only diff of corpus/knowledge (C1 has no such clause).
5. Literal-ID check: `grep -n 'S615\|S235' tools/mori-source-digest.py` must be empty of hard-coded IDs; the counter cannot detect ID special-casing.
6. Successor-copy identity: a successor naming a different pinned copy must not supersede (not among the two negatives).

## 5. Verdict per claim and the falsifying check the L1 must run

C1: holds as presence only; does not hold as depth. Falsifying check (after integration at landing rev R): `git diff --numstat f63d1ab0 R -- corpus/knowledge` must show only the 19 listed files and only provenance-key lines in the first 12 lines; then run every new `recheck:` command at R and require rc 0 (or path:line resolution) and every `verified-at:` to name a commit whose tree contains the file (`git cat-file -e <commit>:<path>`). Any failure falsifies the "trio is true at its commit" predicate even though `C1=met`.

C2: does not hold as written. Freshness does not move beyond flagging two stale digests. Falsifying check (decisive): run `python3 -I tools/mori-source-digest.py corpus/SOURCES.md .ufo/waves/round-90/w1/Mo90S01Sources/sources` at R and read `$?`. If it is 1 (expected while prefix_only=31 unpinned=1 stand, as in A6), the exit-0 clause is unmet and the L1 must not admit C2 without an explicit operator ruling on QUALITY 193. Also run the selftest and the negative fixtures against a mutant that drops the successor check; if the mutant still exits 0, C2 is falsified.

## Attack log (exit codes)

- A1 forged-trio presence test (in-process `missing_keys` on synthetic text, lane file read-only): rc 0; forged prefix, comment, fence and empty-value cases all `absent=[]`; line-13 placement correctly `absent` (window enforced).
- A2 trio classification of the 79 complete entries (git objects at f63d1ab0, heuristic regexes): rc 0; recheck time-only 25, bare on-release 8, date-only verified-at ~59.
- A3 admission and touch count for the 19 files (`git log --diff-filter=A`, `git log`): rc 0; 7 files edited post-admission.
- A4 digest recompute at f63d1ab0 (`git show … | sha256sum`): rc 0 for both pinned copies; S615 and S235 recorded values differ from bytes; S619 and S620 values equal bytes.
- A5 entering tool with S619/S620 appended (scratch, after S618): rc 1; S619 ok, S620 ok, S615 and S235 mismatch; `rows=123 ok=89 mismatch=2 prefix_only=31 unpinned=1`.
- A6 entering tool with S615 and S235 rows removed (scratch): rc 1; `rows=119 ok=87 mismatch=0 prefix_only=31 unpinned=1`. Exit-0 clause unattainable without changing the tool's exit rule.
- Not run: negative fixtures A and B and `--selftest` (need the landed tool; not produced by this seat). Mutation of supersession logic (mutation-tester's item). The C1 and C2 counters as commands on any clone.
- Dead end: AXES.md and LEARNING.md live at the fleet root (`/home/vgpnk/Projects/shokunin/AXES.md`, `…/LEARNING.md`), not in the lane; cited from there. Read-only.

Scratch directory deleted before yield.
