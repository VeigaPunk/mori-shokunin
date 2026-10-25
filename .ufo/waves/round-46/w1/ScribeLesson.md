# ScribeLesson — round-46 lesson review vs verifier defect and Mistakes fields

Seat: `L1Mori46.ScribeLesson` (scribe, wave 1, leaf — no subagent dispatch). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Measured tip at write time: `9834fed4`
(`git rev-parse HEAD`; `git log --oneline -1`). Scope: review `corpus/lessons/round-46.md`
(18 lines, mtime 2026-10-25 10:07) against (a) the round-46 verifier defect / repair ground
truth (`count-repins.py`, `round-45-verifier-spotcheck.md`, `control-skill.md`, `SKILL.md`,
`AXES.md`), and (b) the Mistakes-table field conventions established in prior lessons and
QUALITY. Read-only: no git/jj mutations, no edits to any other file, no tool install/upgrade,
no pacman. Only write is this report.

## 1. Behaviors observed (reproducible)

Counter runs (read-only):

```
$ python3 .ufo/waves/round-46/count-repins.py <lane>/SKILL.md
MORI_R45_REPINS mismatches=0 rows=4        rc 0
$ python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md
MORI_R45_REPINS mismatches=4 rows=4        rc 1
r44 gate registry (C2): stale/missing 1 pin(s)
r45 ledger counter (C1): stale/missing 2 pin(s)
r45 gate conformance (C2): stale/missing 5 pin(s)
r44 gate registry (C2) — write scope superseded: stale/missing 3 pin(s)
```

Control identity: `sha256sum .ufo/waves/round-46/control-skill.md` =
`ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad`; `git show baabc992:SKILL.md | sha256sum`
= same. The control is byte-identical to the committed r45 SKILL snapshot.

Repair scope: `git diff --stat baabc992 -- SKILL.md` → `SKILL.md | 8 ++++----` (4 insertions /
4 deletions). Diff shows exactly the four predicate rows changed (`r44 gate registry (C2)`,
`r45 ledger counter (C1)`, `r45 gate conformance (C2)`, `r44 gate registry (C2) — write scope
superseded`, SKILL.md:184,190,191,194). Present values equal the spot-check's "committed at
`baabc992`" column: `5f2deea0…`, `153423c4…`, `9850b3fc…`, `8b82ac99…`/743, tallies
16/14/15 (`grep -c` confirms each needle in SKILL.md; `8b82ac99…`, `GATE_REGISTRY_SELFTEST
pass=15 fail=0`, `743 lines` each appear 3× — rows 184/191/194).

Lesson evidence pointer: `corpus/lessons/round-45-verifier-spotcheck.md:50-66` — lines 50–58
hold the calibration ruling and the four-cell table (`:184`/`:190`/`:191`/`:194`), lines 60–62
continue `:191`; accurate.

S474: AXES.md:15 reads verbatim `| **calibration** | Self-assessment quality: gaps named
honestly, confidence graded, overreach caught | … |`; SOURCES.md:253 S474 row exists (own-work,
tier A, mined, opened 2026-10-25, used-by `corpus/lessons/round-46.md`).

## 2. Findings

F1 (factual, fix cell / Gate). The lesson's fix says "The red-before control is committed
alongside the counter." At measured tip `9834fed4` this is **false**: `git status --porcelain`
shows `?? .ufo/waves/round-46/` (both `count-repins.py` and `control-skill.md` untracked),
`?? corpus/lessons/round-46.md`, and modified-uncommitted `LOG.md`, `SCORECARD.md`, `SKILL.md`,
`corpus/SOURCES.md`. No round-46 bytes are committed yet. Disposition pending the wave's commit;
as written, the sentence asserts a state that does not exist at the measured tip.

F2 (Mistakes schema, id). The table header `| class | evidence pointer | captured-by | fix |`
**omits the `id` column** used by every recent lesson (r12–r45: `| id | class | evidence |
captured-by | fix |`) and renames `evidence` → `evidence pointer`. Without an M-id the row
cannot be cited by future QUALITY criteria (established pattern: `lessons/round-N.md#M<id>`).

F3 (Mistakes schema, captured-by). `captured-by` is narrative, not the convention from
r13/r16 scribe rules (a QUALITY criterion number, or `none` with reason). It reads
"round-45 M1-M5 criteria did not cover the self-description cells themselves; calibration
definition in `AXES.md` says self-assessment must match observed state". M1–M5 are mistakes,
not criteria; and QUALITY 40 (registry row swept when its gate/selftest/source changes; active
registry must match delivered entry points and pinned values) directly covers this defect
(also Q41/Q10). The negative "did not cover" claim conflicts with Q40's existence as written;
the cell should name Q40 (or justify `none`).

F4 (precision vs cited source). Lesson: "observed four stale SKILL registry pins at
`baabc992`". The spot-check's own emphasis (lines 60–62) is that `:191` carried **three**
stale values (auditor + counter + mutant digests); four stale *cells* ≠ four stale *pins*.
Minor under-sampling of the cited source.

F5 (Gate / QUALITY 86). The lesson has no `## Gate` decision table and no
"reject sample: none met" declaration; per QUALITY 86's check this reads
`gate_reject_rows=0 none_declared=0` (fail). The lesson's own statement "Rejected: no
assimilation candidates evaluated" requires the declaration form.

F6 (wording). "the lane's own round-45 verifier spot-check" — the r45 spot-check author is
hyaku closure (non-author integrator), not the lane; the following line's "Non-author
spot-check: pending" is in tension with calling it the lane's own.

F7 (verifier scope note). `count-repins.py` checks needle **presence** per row (case-sensitive
substring, whole file, not scoped to the `## Gates` table); it cannot detect a stale pin that
coexists with the corrected needle in the same row, nor absence of stray duplicates elsewhere.
The lesson's "count exact row-to-observation mismatches" is stronger than the counter's actual
behavior. No false-green observed on current bytes (mutation seats probe this).

## 3. Confirmed (lesson correct on)

- Counter rejects the committed old snapshot: 4 mismatches, rc 1 — verified.
- Counter accepts the corrected snapshot: 0 mismatches, rc 0 — verified.
- Control is the true do-nothing prior snapshot (byte-identical to `baabc992:SKILL.md`) — verified.
- Repair touched exactly the four routed cells and no other SKILL row — verified.
- Evidence pointer `round-45-verifier-spotcheck.md:50-66` is accurate — verified.
- S474 quote at AXES.md:15 verbatim; SOURCES row consistent — verified.
- Gate details: "No shokuknow package entries were adopted; assimilation is none"; "No
  considerthese directory was inspected" — no contradicting evidence found; non-author
  spot-check correctly marked pending.

## 4. Limits

- Peer-seat reports for round-46 had not landed at write time (w1 contained only
  `swarm-registry.json`); no dispatched seat's verdict is used or counted as non-author.
- Everything above is read-only observation at tip `9834fed4`; the wave may still commit the
  round-46 files, which would resolve F1 (and possibly F5) after this write.
- No tool installs/upgrades were made; no pacman transaction attempted.
