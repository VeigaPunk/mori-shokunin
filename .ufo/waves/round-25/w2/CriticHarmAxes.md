# CriticHarmAxes — round 25 wave 2 (falsify): no-harm condition across axes

Seat: `MoriR25.CriticHarmAxes` (critic, leaf). Measured at base `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf`
and at lane tip `07a31ae8e22514bbc603afa13f2de7c8b2424cca` (pinned when I started measuring; HEAD
moved from `e5e1b7bc` to `07a31ae8` during my first calls). All code ran from private `git archive`
extracts under `/fast/scratch/hyaku/mori-r25/w2-CriticHarmAxes/{base,tip}`; git object reads ran
against the lane with `GIT_OPTIONAL_LOCKS=0`.

## Verdict: **broken** — adjacency harmed; freshness/depth weakened; operability held

| Axis | Verdict | Severity of worst finding |
|---|---|---|
| adjacency | **harmed** — the lane's own round-18 retention gate goes from 4 to 88 unallowlisted hits, 1 of them a session-identity hit | high |
| freshness / depth | **weakened** — two admitted statements are now less accurate, and one admitted entry lost its precedence rule while body text still contradicts its corrections | low–medium |
| operability | **held** — no pre-existing tool blob changed; default pressure selftest is byte-identical; dependent gates give the same result | none (one low conformance gap) |
| adjacency (configuration ground) | held in wording: mori does not claim harness configuration; one low duplicate-authority note | low |

---

## F1 (high, adjacency harmed) — the round-18 retention gate's metric rises from 4 to 88 unallowlisted hits

**Counterexample.** This is the lane's own registered gate (`SKILL.md` Gates row "r18 retention (C1)",
credited to **adjacency** in `SCORECARD.md:1131-1152` at base). I ran it over the committed tree at
base and at tip, using the base tool bytes (the blob is unchanged):

```
python3 -I -B base/tools/mori-retention-gate.py scan --repo <lane> --rev <REV> \
  --policy <lane>/.ufo/waves/round-18/frozen/c1-policy.json \
  --allowlist <lane>/corpus/evidence/retention-allowlist.json
```

| rev | exit | hits | allowlisted | unallowlisted (`metric`) |
|---|---|---|---|---|
| `28b79d3d` | 1 | 95 | 86 | **4** (all four inside `.ufo/waves/round-20/falsify/NoHarmRun/rg/…/c1-policy.json`) |
| `07a31ae8` | 1 | 179 | 86 | **88** |

There are 84 new unallowlisted hits, all in round-25 bytes:

- **80 × R7 `operator_config_ref`** (`config\.yml:[0-9]|\.omp/agent/config\.yml`). On lane surfaces they are at
  `LOG.md:1801`, `PROVINCE.md:297`, `SKILL.md:658`, `SKILL.md:663`, `corpus/README.md:488`,
  `corpus/knowledge/harness-job-capacity-r25.md:2,17,176` and `tools/mori-job-runway.py:6,12,631`. The rest are in the
  round-25 contract, wave specs/runs and 17 wave-1 reports.
- **1 × R1 `session_identity` and 1 × R2 `session_store_path`**, both on `.ufo/waves/round-25/w1/SeatGateRelation.md:109`
  (committed in `9ec786e`). These are the classes behind the round-17 privacy harm (`rejected-harmed, adjacency`,
  `SCORECARD.md:1133`). I am not reproducing the content.
- **1 × R9 `session_record_value`** at `SeatGateRelation.md:135`, and **1 × R8 `routing_table_key`** at
  `.ufo/waves/round-25/w1/SrcRejections.md:86`.

**Why this is harm, not a missing allowlist row.** The frozen adjudication rule (`c1-policy.json`,
`adjudication_rule`) allows a row on the allowlist only when "the line carries no value copied from a
private source"; "every other hit is redacted". Several new lines copy values out of the operator config
file, so they cannot be allowlisted:

- `SKILL.md:658`: "this host's the operator's OMP settings file says 200";
- `LOG.md:1801`: "the operator's OMP settings file sets `async.maxJobs: 200`";
- `harness-job-capacity-r25.md:2`: "carries `async:` then `maxJobs: 200`".

The R1/R2 line names a concrete other-session store path. The round-23 closure routed "Preserve four
unallowlisted hits" (`corpus/lessons/round-23-verifier-spotcheck.md:63`). At `28b79d3d` the count was still 4.

**Why the round's no-harm check missed it.** Wave-1 `NoHarmBefore` ran only
`mori-retention-gate.py --selftest` (PASS 21/21, `.ufo/waves/round-25/w1/NoHarmBefore.md:112`), which uses
synthetic sandboxes. It never ran `scan` over the measured revision. The round-24 routed check
(`tools/mori-routed-check.py`) still holds 4 of 4 at both revisions (I ran it). Its R2 item checks only the
retention tool blobs and `privacy_clearance=true` lines, so it cannot see this.

**Smallest safe correction.**
1. Redact the copied values and line references, keeping the surface name:
   - `SKILL.md:658`: replace "the settings file says 200" with "the file the tool reads";
   - `LOG.md:1801` and `harness-job-capacity-r25.md:2`: drop `200` and the line numbers, or point to the
     committed live-run evidence instead.
2. Redact `SeatGateRelation.md:109` (R1+R2) and `:135` (R9) and the copied-value lines in the round-25
   `.ufo` reports, the same way round 18 redacted round-17 build reports.
3. Add L1-ruled, name-only allowlist rows for the lines that only name the surface (rule (a) or (b)):
   - `tools/mori-job-runway.py:6,12,631`
   - `PROVINCE.md:297`
   - `SKILL.md:663`
   - `harness-job-capacity-r25.md:17,176`
   - `corpus/README.md:488`
   - `SrcRejections.md:86`, if it is a key name only
4. Re-run the `scan` at the new tip and commit the output as evidence. Target: unallowlisted 4, with the
   same four round-20 paths.
5. Add the `scan` (not only `--selftest`) to the round's no-harm battery.

## F2 (medium, freshness/depth) — D5 left an admitted round-12 statement false and dropped its prior disclosure

At base, the admitted round-12 section reads: "Correction to the score table at the top of this file (frozen
at round 1; 4 of 6 pointers stale …): the table is left as filed; this section's scores supersede it"
(`SCORECARD.md:616-617` at `28b79d3d`; written in `1f07f1d`). Round 25 rewrote that table
(`SCORECARD.md:10-15` at tip) and left the round-12 sentence unchanged at tip `SCORECARD.md:620-621`. A
reader of the tip file now finds an admitted line saying the top table is "left as filed" and "frozen at
round 1", and it is neither.

The new correction note (`SCORECARD.md:17-19` at tip) says "until round 25 this table still showed the
round-1 scores … with 'round 1' in every row". It does not say that round 12 had already disclosed the
staleness and superseded the table. The D5 mismatch was a known, disclosed stale table, not an undisclosed
contradiction. That is a provenance gap in a calibration claim; under A5's wording it is not a reason to
reject D5.

**Fix.** Append one sentence to the round-25 note:

> SCORECARD.md:620-621 (round 12) had already marked this table frozen and superseded; round 25 rewrote it,
> so that note's "left as filed" no longer holds.

## F3 (low, freshness) — operability "Last change: round 13 (6 → 7)" names a round that was not admitted

Round 13's closure is "status `ok`, admitted `false`, verdict `rejected-harmed`"
(`corpus/lessons/round-13-verifier-spotcheck.md:7`). Operability 7 was first held by an admitted closure in
round 14 ("preserves the verified operability gain and holds coverage6/operability7/…",
`corpus/lessons/round-14-verifier-spotcheck.md:87`).

The other rows check out:
- coverage "round 12 (5 → 6)" and depth "round 12 (4 → 5)" agree with `SCORECARD.md:609-611` and the admitted
  round-12 closure (`round-12-verifier-spotcheck.md:17`);
- calibration's "12's 6 not held" agrees with `SCORECARD.md:654`.

**Fix.** Change the operability cell to "round 13 work, first admitted round 14 (`round-14-verifier-spotcheck.md:87`)".

## F4 (low, depth) — `system-pressure-r24.md` lost its precedence rule while some body text still contradicts the corrections

The D2 edit replaced "Where this section and a later line disagree, this section wins" with an in-place
correction notice that lists K3, K4, K5, P3 and P4 (tip `system-pressure-r24.md:10-13`). The corrections
section also carries:
- K6 (`:22-24`), P2 (`:25-29`);
- the provenance bullet H1, covering F12, part of F9, U1 and U7 (`:37-41`);
- a citations bullet (`:42-44`).

These were not rewritten in the body. Example: the F7 heading and lead still say the disabled-PSI "errors
surface on read" and that "`psi_disabled` … makes every read fail" (`:118-125`). P2 says that branch "cannot
be reached through a `/proc/pressure` read" at v7.2. The same paragraph does qualify this at `:128`. F12
still reads as a numbered fact with no in-place pointer saying it is not admitted.

The new banner still says each bullet carries "the wording that replaces the body text it contradicts", so
some precedence survives implicitly. The explicit tie-break is gone, though.

What I verified: the K5 in-place rewrite matches v7.2 `psi.c`. I fetched it with curl (sha256 `452318be…`):
line 1268 is `collect_percpu_times`, lines 1269-1270 update the averages only when due, lines 600-602 are the
averages work item, and lines 342-360 are `calc_avgs`. The K3, K4, P3 and P4 rewrites match their bullets.

**Fix.** Add to the banner:

> K6, P2, the provenance bullet and the citations bullet were not rewritten in the body; for those, the bullet governs.

## F5 (low, operability conformance; not harm to existing bytes) — the two new verdict tools have no Gates registry rows

Round 24 registered both of its tools under "### Round24 registry additions" (`SKILL.md:637-642`). Round 25
adds no registry row for `tools/mori-routed-r24.py` (0 mentions in `SKILL.md`) or `tools/mori-job-runway.py`
(mentioned only in the decision table at `SKILL.md:661`). Both produce verdicts with exit maps 0/1/2. The
round-13 closure named exactly this as a PROTOCOL §Gate standard defect
(`round-13-verifier-spotcheck.md:25`).

**Fix.** Add a "Round25 registry additions" table with both rows.

## F6 (low, adjacency) — mechanism semantics are held in mori's `SKILL.md`; no report to kumitate is recorded

The new `PROVINCE.md` notes (tip `PROVINCE.md:335-344`) say the semantics behind the clamp belong to
kumitate: what the job manager counts, the refusal text, and that only the root session builds a manager.
Mori's `SKILL.md:656-661` decision table nonetheless states these semantics, with upstream line anchors, as
mori's "Report as" guidance.

`corpus/lessons/round-25.md`, `LOG.md` and the knowledge entry contain no mention of kumitate. So nothing
routes these facts to the owning lane ("Out of province → report, never absorb", `PROVINCE.md:18`).
Kumitate's OMP contract has no `async.maxJobs` row (`kumitate-shokunin/corpus/knowledge/omp-task-contract.md:197`
records a different setting, `task.maxConcurrency`, as UNKNOWN).

Mori does **not** claim harness configuration ground:
- `SKILL.md:663-673` refuses edits, cancels and wave reshaping;
- `PROVINCE.md` gives configuration to the operator;
- the knowledge entry's "Not claimed" list (`harness-job-capacity-r25.md:289-303`) is explicit.

This is a tradeoff to surface at closure, not a hidden regression.

**Fix.** Add one routed line in the round-25 lesson: "report to kumitate: async.maxJobs clamp facts S098–S104 for its OMP contract".

## Operability — held (commands that show it)

- `git diff --name-status 28b79d3d 07a31ae8 -- tools/` shows `A` for `tools/fixtures/mori-job-runway/{cases,supplementary-cases}.json`,
  `tools/mori-job-runway.py` and `tools/mori-routed-r24.py`, and `M` only for
  `tools/fixtures/mori-pressure/supplementary-cases.json`. A sha256 comparison of every file in the two
  extracts confirms that no other pre-existing `tools/` file changed (`mori-pressure.py` and
  `fixtures/mori-pressure/cases.json` match byte for byte).
- Pressure selftest, default:
  `python3 -I -B tools/mori-pressure.py --selftest` prints `PASS 12/12` / `MATCHER: rejected 48/48 corrupted expectations`,
  exit 0, at both base and tip. The two outputs are byte-identical (`cmp` showed no difference). The committed
  D1 evidence body (`evidence/pressure-selftest.txt` lines 6-7) equals the tip run.
- Pressure selftest, supplementary (`--cases tools/fixtures/mori-pressure/supplementary-cases.json`):
  - base: `PASS 7/7` / `rejected 28/28`, exit 0;
  - tip: `PASS 16/16` / `rejected 64/64`, exit 0;
  - base tool on the tip file: also `16/16` / `64/64`.

  The change is append-only. S01–S07 are identical objects at base and tip; S08–S16 are new. Only the file's
  `note` field changed, and it still says the 12-case after-value is unaffected. The output changes only by
  the added cases.
- `tools/mori-routed-check.py --repo <lane> --rev <REV>` gives held 4 of 4 (R1–R4 all held), exit 0, at both
  `28b79d3d` and `07a31ae8`.
- `mori-round13-regressions.py` reads the `SKILL.md` Gates row. `SKILL.md` has 0 deleted lines and +31
  appended after line 642. The matched row at `SKILL.md:167` is unchanged.
- Every pre-existing lane document that changed has **0 deleted lines**, measured with `diff base tip`:
  `SOURCES.md` (+16), `QUALITY.md` (+19), `LOG.md` (+12), `SKILL.md` (+31), `PROVINCE.md` (+65),
  `corpus/README.md` (+40), `lessons/round-24.md` (+4) and `.gitignore` (+1, `tools/__pycache__/`). The only
  in-place edits are `SCORECARD.md:10-15` (D5) and `system-pressure-r24.md` (D2), covered in F2–F4.
- Host facts in the new text that I re-checked:
  - the operator's OMP settings file lines 244-245 read `async:` / `maxJobs: 200`;
  - `omp` is 256,702,432 bytes;
  - the clamp pattern matches once, at byte 164406766;
  - the throw text starts at byte 160033342;
  - the tip `mori-job-runway.py` live run returns `RUNWAY_CLAMPED`, effective 100, exit 1.

## Freshness — other admitted edits checked and found accurate

The round-24 lesson D3 correction (`lessons/round-24.md:97-100`) is scoped to `4f05dd5a` and is accurate
there: I measured `PASS 7/7` / `28/28` on the base copy of the file. The same command at tip prints
`PASS 16/16`, because the file grew in the same commit `ec840f9`. The sentence is pinned to a commit, so it
is not false; a present-tense reader could misread it.

## Disclosures

- No tools installed or upgraded. No pacman, no omp, no jj.
- My first lane command included a plain `git status --short` before I set `GIT_OPTIONAL_LOCKS=0`. Git may
  have refreshed stat data in the lane index as a result; no index entries or content were changed.
  Every later git command ran with optional locks off.
- Unrun: the full selftests of the other pre-existing tools (their blobs and fixtures are unchanged, and
  wave-1 `NoHarmBefore` ran them); `mori-content-review.py check` (its population is frozen at round 19).
- I deleted the large extracts after measuring. Kept under `/fast/scratch/hyaku/mori-r25/w2-CriticHarmAxes/`:
  `ret.{28b79d3d,07a31ae8}.json` (path, line, class and line sha256 only), `rc.*.json`, the pressure output
  files and `psi-v7.2.c`.
