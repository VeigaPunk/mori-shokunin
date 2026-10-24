# ReviewSkillRound30 — falsify review of SKILL `## Round30` rows

Verdict: **defect found** — three of the four Round30 rows (SKILL.md:752-754) reproduce exactly on the tip tool,
but the dry-run row (SKILL.md:755) over-claims `KILLER_ACTED` for "a real send in another invocation": its own
cited frozen case pins `KILLERS_QUIET` for the active-unit ordering it describes, and the tip tool confirms that.

Scope attacked: SKILL.md:752-755 (`## Round30` table, `earlyoom-invocation-scope-r30.md`), against the tool at
lane tip `ad0f0474`, the cited entering-tip blob `58b61681:tools/mori-oom-killers.py`, the entry
`corpus/knowledge/earlyoom-invocation-scope-r30.md`, and earlier SKILL rows (Round26 table, SKILL.md:~684-699).

Method: invented `inputs` objects (all names/values fabricated) run through
`python3 -I -B tools/mori-oom-killers.py --inputs /dev/stdin`; cited blobs re-derived via
`git show 58b61681:tools/mori-oom-killers.py` into `/fast/scratch/hyaku/mori-r30-w2/ReviewSkillRound30/`.

## Findings

### F1 (moderate) — SKILL.md:755: "a real send in another invocation still counts (`KILLER_ACTED`)" is wrong for the active-unit earlier-real/current-dry-run ordering

Row text (SKILL.md:755, `What to conclude`): "… a real send in another invocation still counts (`KILLER_ACTED`),
and a dry-run invocation with no other evidence reads `KILLERS_QUIET`".

- The row cites `a2-07-earlier-real-then-current-dryrun` as grounding. That frozen case pins exactly the
  described shape — an earlier **real** invocation and the **current** dry-run invocation on an `active` unit —
  and expects `KILLERS_QUIET`, exit 0, with `earlyoom.earlier_invocation_send_lines=2` and
  `earlyoom.dryrun_send_lines=1` (`tools/fixtures/mori-oom-killers/cases-a2.json:795`, `expect` printed above).
- Reproduced on the tip tool: active unit, `ActiveEnterTimestampMonotonic=250`, journal
  `earlyoom 1.9.0`@100, `sending SIGTERM …`@200, `earlyoom 1.9.0`@260, `dryrun mode enabled`@270,
  `sending SIGKILL …`@280 → `KILLERS_QUIET`, exit 0, `earlier=1`, `dryrun_send_lines=1` (run `r4b`).
- The `(KILLER_ACTED)` clause is only true when the real send lands in the *current* invocation
  (`a2-07-three-invocations-dryrun-in-the-middle` acts via `actions.sigterm=1`, also cited by the row) or when
  the unit is not `active` (run `r4c`, inactive, earlier real + later dry-run → `KILLER_ACTED` via `earlier=1`).
- So the literal "another invocation … (`KILLER_ACTED`)" is falsified by the row's own citation for an active
  unit. The grounding entry is consistent: its decision-table row for `a2-07-earlier-real-then-current-dryrun`
  says `KILLERS_QUIET` (`corpus/knowledge/earlyoom-invocation-scope-r30.md:103`), and its §5 sentence ("one
  dry-run invocation does not zero another's real sends") does not equate "still counted" with `KILLER_ACTED`.
  The SKILL row collapsed "still counts as evidence" into a verdict the A2a limit forbids for active units.

### F2 (minor) — SKILL.md:755: "a dry-run invocation with no other evidence reads `KILLERS_QUIET`" is unconditional

- "No other evidence" does not cover unverified grammar or incomplete scope. Invented input `r4d`: active unit,
  `ActiveEnterTimestampMonotonic=50`, journal `earlyoom 9.9.9` + `dryrun mode enabled` + one send, all ≥ 50 →
  `KILLERS_UNKNOWN`, exit 2, `scope_complete=true`, `grammar=unverified` (tip tool; the pre-fix blob prints the
  same). With the stamp missing the same journal is unbounded → also `KILLERS_UNKNOWN`.
- The verified-grammar precondition exists only implicitly. Low severity: the row's never-conclude cell stays
  true (dry-run sends are never positive evidence; `dryrun_send_lines=1` reported in `r4d`).

### F3 (observation, not a round-30 defect) — the Round26 row remains over-broad, but the fix did not break it

- SKILL.md:~695 (Round26 table): "earlyoom is `active` but its `ActiveEnterTimestampMonotonic` is missing or 0,
  **or** the invocation's version line is not in scope → `scope_complete: false`, verdict `KILLERS_UNKNOWN`".
  The stamp disjunct alone does not force UNKNOWN: invented `r1b` (active, stamp 0, send after the last version
  line) prints `KILLER_ACTED` exit 1 on **both** `58b61681` and the tip — i.e. the row was already wrong at the
  entering tip and is not newly falsified by the round-30 fix. Round30 row 1 states it correctly
  ("with no positive evidence"). Worth noting only as residual prose debt; this round improved, not caused, it.
- No earlier SKILL statement is made false by fix `7aa77484`: the Round26 rows "actions is **null**, never zero
  counts" for non-active units and "earlier-invocation sends are positive evidence for a non-active unit" both
  still hold at tip (runs `r3a`-`r3c`, `r3b2`-`r3b5`: `actions=None` in every non-active run; verdicts
  ACTED/ACTED/QUIET respectively). What changed is reporting granularity: for a non-active unit with a retained
  stamp, a send inside the last invocation now lands in the in-scope counters (evidence path
  `counts["sigterm"]…`, tip `mori-oom-killers.py:474-481`) instead of `earlier_invocation_send_lines`
  (`r3b2` tip `earlier=0` vs `58b61681` `earlier=1`, same `KILLER_ACTED`). SKILL.md:754 describes this correctly.

## Verified claims (no defect)

- Row 1 (SKILL.md:752): `r1a` active/missing-stamp/quiet journal → `KILLERS_UNKNOWN` exit 2,
  `scope_complete=false`, `earlier=0`; `r1b` send inside the last-version tail → `KILLER_ACTED` exit 1 with
  `scope_complete=false`. Matches row text and entry §2 (`earlyoom-invocation-scope-r30.md:41-44`).
- Row 2 (SKILL.md:753): `r2` active, stamp 0, send before last version line → `KILLERS_UNKNOWN` exit 2,
  `earlier=1`, `actions.sigterm=0`, `scope_complete=false`. Matches; also consistent with all eight frozen
  `cases-a2-r30.json` expectations (`KILLERS_UNKNOWN`, exit 2 — enumerated).
- Row 3 (SKILL.md:754): `r3a` inactive + earlier send → `KILLER_ACTED`, `actions=null`, `earlier=1`; `r3b2`
  inactive + retained stamp + send only inside last invocation → `KILLER_ACTED`, `earlier=0`, `dryrun_send_lines`
  and `process_group_lines` become `0` (not null) exactly as the fix intends; `r3c`/`r3b5` quiet variants →
  `KILLERS_QUIET`. Matches row and entry §3 (`:48-57`).
- Row 4 (SKILL.md:755), claims that hold: `r4a` current dry-run segment → sends go to `dryrun_send_lines=1`,
  `actions.sigterm=sigkill=0`, verdict `KILLERS_QUIET`; `r4c` non-active unit → earlier real send still acts.
- `58b61681:tools/mori-oom-killers.py` citations all hold the described code at those lines: `:278-302` (active
  unbounded branch + last-version split), `:293-302` (the split itself), `:317-352` (earlier-invocation counter
  incl. per-segment dry-run split), `:333-381` (both segment splits + `close_segment`), `:417-419` (A6 dry-run
  comment), `:424` (`scope_complete` expression), `:465-469` (`acted` — non-active earlier sends positive,
  active report-only), `:487-489` (active + incomplete scope → unknown).
- Contract-line citations hold: rules A2-04/A2-05/A2-06/A2-07 sit at `.ufo/waves/round-27/contract.md:52-55`
  (blob `58b61681`); A2a and the earlier-invocation rule sit at `.ufo/waves/round-26/contract.md:171-172` and
  `:174-179`.
- Every case id cited by the rows exists in `tools/fixtures/mori-oom-killers/cases-a2.json`
  (`a2-05-monotonic-zero-active-quiet`, `a2-05-monotonic-zero-inactive-quiet`, `a2-06-active-earlier-invocation-sends-quiet`,
  `a2-06-inactive-earlier-invocation-sends-acted`, `a2-06-active-earlier-and-current-send-acted`,
  `a2-07-earlier-real-then-current-dryrun`, `a2-07-three-invocations-dryrun-in-the-middle`).
- Consistency with the entry: rows 1-3 track `earlyoom-invocation-scope-r30.md` §2-§4; only row 4's
  `(KILLER_ACTED)` clause deviates from the entry's own table (F1).

## Residual risk / gaps

- The counter pins only fields, not prose; F1/F2 are prose-level mis-statements a `count-c1` pass cannot catch
  (contract §"Uncounted residual" explicitly leaves row-shape accuracy to wave 2 — F1 is that class).
- Not re-run: `count-c1.sh`/`count-c2.sh` (other seats own counter attacks); I verified the underlying facts the
  rows assert instead. `[INFERENCE]` F1 would likely be judged a wording defect, not a counter failure.
- Tooling: none installed; python3/git/read only.
