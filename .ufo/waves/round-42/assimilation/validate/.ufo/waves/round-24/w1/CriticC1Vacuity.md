# CriticC1Vacuity — round 24 wave 1, claim C1 vacuity attack

Seat: MoriR24.CriticC1Vacuity (critic, read-only, leaf). Target: C1 in
`.ufo/waves/round-24/contract.md:10-42` (landed at 29c1bf45), routed source
`corpus/lessons/round-23-verifier-spotcheck.md:60-66`. Lane tip observed: 4059ffb5
(wave 1 ledger commit). `tools/mori-routed-check.py` does not exist yet (not at the tip,
not in `/fast/scratch/hyaku/mori-r24-a2/wt-routed`, whose head is 29c1bf4), so this attack
is on the declared predicates, not on an implementation.

## Verdict

"Held 3 of 4 → 4 of 4" is **not a real repair of the routed text**. The before-value is
fixed by construction, and the after-value was already true at 4059ffb, before the check
existed:

- At `--rev c725aa37` every "equals base" predicate in R1–R3 compares an object with itself,
  and the two R1 paths were already absent at base (spot-check lines 33-34; `git rev-parse
  c725aa37:tools/mori-quota-surface.py` fails). So R1–R3 cannot be red at base, whatever
  defect exists. R4 is red at base only because `.ufo/waves/round-24/` did not exist yet.
  It is not red because of the round-23 defect it routes.
- At 4059ffb all four predicates already hold. The `.ufo/waves/round-23` tree OID is
  3e5b2c9d at both c725aa37 and 4059ffb. `tools/mori-dispatch-ledger.py verify --rev 4059ffb5
  --ledger .ufo/waves/round-24/wave1-attempts.json` prints `clean ['LEDGER_CLEAN']`, rc 0.
  The dispatch path was first added in 06d4f4d at 05:13:57 -03:00, which is before the row's
  `at` of 05:14:13.926 -03:00. Any round-24 dispatch that writes a ledger saturates the
  after-value, so the claim is saturated before implementation.
- R1–R3 are preservation obligations ("keep", "preserve", "never alter"). Round 23 never
  broke them, so there is nothing to repair. A predicate for them is a regression tripwire,
  and a tripwire belongs in held-axis monitoring, not in a calibration gain. The table also
  never reads the round-23 self-assessment text that `contract.md:16-17` says it compares
  against.

There is one real behavioural repair, but C1's predicate cannot see it. Round-23 wave 1
binding was retrospective (spot-check line 15). Round-24 wave 1 was bound before the call,
going by a harness-written witness outside the repo (timeline in the R4 section below). C1's
R4 predicate cannot tell that honest ledger from a forged one.

## Counterexamples by item

### R1 — quota capability absent; CaseEscapedSpace row unaltered

- **Counterexample (rename):** re-add the withdrawn probe as `tools/mori-fs-quota.py`, or as
  a function in `tools/mori-census.sh`, plus `corpus/knowledge/quota-r24.md`. Both pinned
  paths stay absent and `frozen/` is untouched, so R1 holds while the capability is back.
  The predicate is a check on two file names, not on the capability.
- **Counterexample (special-casing):** a tool line like `if case_id == "CaseEscapedSpace"`
  breaks the routed "never special-case" clause. R1 has no code predicate.
- **Unprotected copies:** CaseEscapedSpace rows also live outside `frozen/`, in
  `.ufo/waves/round-23/cases-corrected/CaseEscapedSpace.json`, `cases-proposed/`,
  `build/CaseEscapedSpace.md` and `evidence/frozen-contradiction.json` (`git grep -l
  CaseEscapedSpace c725aa37`). Editing them leaves R1 green.
- **Vacuity:** at base, `frozen` OID 0c067e21 equals itself. No round-24 seat writes there.
- Impacted axes: calibration (the claim overstates), coverage and adjacency (the capability
  can return without being detected).

### R2 — four unallowlisted hits, 11/12 red, unknown dispositions, blocked baseline, clearance false

- **Regex false greens.** Tested in-process against the contract's regex (case-insensitive):
  - Plain JSON and Python dict forms match.
  - These forms do NOT match:
    - escaped JSON inside a receipt's `stdout` string (a backslash before the quote), which
      is exactly how `retention-floor-final.json` embeds tool output (its keys are `argv`,
      `measured_revision`, `exit`, `stdout`, `stderr`);
    - a multi-line JSON value;
    - computed values (`bool(ok)`, `not False`, `1`, `yes`);
    - a hyphenated or camelCase key;
    - string concatenation.
  - The comparison blob uses the key `clearance`, not `privacy_clearance`
    (`git show c725aa37:.ufo/waves/round-23/evidence/retention-floor-final-comparison.json`:
    `"clearance": false`). A new round-24 comparison that sets `clearance` to true is
    invisible to the regex.
- **Behavioural false green.** `tools/mori-retention-reconcile.py:238` at base hardcodes
  `'privacy_clearance':False`. Changing that literal to a computed expression adds no line
  that matches, yet the tool can then grant clearance. R2 neither pins this tool nor runs it.
- **New-receipt false green.** A new round-24 retention receipt that reports
  `unallowlisted: 0` or an accepted baseline supersedes the round-23 facts. Meanwhile the two
  pinned blobs stay byte-equal, so R2 holds.
- **Regex false red, which can block honest work.** At base, six committed files already
  carry a matching literal because critics and mutation seats quote it (`git grep -c -i -E
  <regex> c725aa37`: `round-22/falsify/MutationScope.md`, `round-22/measure-round22.py`,
  `round-23/falsify/C1R04.md`, `C1R15.md`, `C1R17.md`, `ReviewDebtHold.md`). The contract's
  own R2 mutant (`contract.md:39-40`) is exactly such a line. If any round-24 report or
  committed mutant receipt quotes it, R2 turns red on documentation. This report avoids the
  literal on purpose.
- **Vacuity:** the two blobs (4954de42, 1411d94a) equal themselves at base.
- Impacted axes: calibration; operability (false red on reports).

### R3 — transient-source and overwritten-wrapper limitations preserved

- **Counterexample (additive):** add `.ufo/waves/round-23/evidence/transient-source-reconstructed.json`,
  or a round-24 LOG, SCORECARD or knowledge line claiming the lost streams were reconstructed
  or the final archive scanned. Only two evidence blobs and `rejected/` are pinned, not the
  `evidence/` tree (OID 2305d738) and not new claims elsewhere, so R3 holds while the
  routed clauses ("no reconstruction", "not retroactively claimed scanned") are broken.
- **Vacuity:** blobs bfcfb2c8 and ad622617 and the `rejected` tree 43141269 equal
  themselves at base.
- Impacted axes: calibration.

### R4 — bind future dispatches before the call

Observed wave 1 timeline. Times are local -03:00 unless marked; the source of each is given.

| Event | Time | Source (who writes it) |
|---|---|---|
| `wave1-run.json` file born | 05:13:51.265 | `stat` birth time (L1 filesystem) |
| swarm registry `createdAt` | 08:13:51.297Z = 05:13:51.297 | harness, `w1/swarm-registry.json` |
| dispatch commit 06d4f4d | 05:13:57 | git committer time (L1 or jj controlled) |
| bind receipt at rev 06d4f4d | 05:14:03.4 | `/fast/scratch/hyaku/mori-r24-a2/wave1-bind.json`, **scratch only, not committed** |
| ledger row `at` | 05:14:13.926 | L1-written field |
| first round-24 subagent event | 08:14:13.971Z = 05:14:13.971 | harness session `MoriR24/MoriR24.BuildPressureTool.jsonl` (outside the repo) |
| ledger and response written | 05:14:24.07 | `stat` |
| ledger commit 4059ffb | 05:14:40 | git committer time |

So wave 1 really was bound before the call: the commit came about 17 s before the first
harness spawn event. That proof uses a witness R4 never reads. R4's two inputs, committer
time and `at`, are both written by the L1, and the ledger is necessarily written after the
call because it records `result` and `started_ids`.

- **Counterexample (forged order):** dispatch first, then commit the payload with
  `GIT_COMMITTER_DATE` or `JJ_TIMESTAMP` set earlier, then write any later `at`. R4 holds.
  Timestamps in this lane are already known not to be write times: 29c1bf45 has author time
  1792616814 (18:06:54, the same second as base c725aa37) but committer time 1792656655
  (05:10:55 next day). That is jj carrying an attempt-1 author time across a rewrite.
- **Counterexample (placeholder path):** commit a stub `wave2-run.json` early, dispatch, then
  overwrite it with the real payload and write a matching ledger row. "First added" still
  dates the stub, `verify` checks the payload at REV, and R4 holds. The predicate binds the
  existence of the path, not the payload bytes.
- **Counterexample (coverage):** R4 needs only "at least one" `round-24/*-attempts.json`. A
  wave 2 dispatched without a ledger, or with a ledger named `*-ledger.json` (the round-23
  convention: `round-23/wave1-ledger.json`, `wave2-ledger.json`), is never examined.
- **Round-23 evidence that the timing clause has teeth, but is aimed at the wrong round:**
  applying it to `round-23/wave1-ledger.json` at base shows every `at` (17:03:11Z to
  17:24:14Z) precedes the dispatch commit 22772c1 (15:10:59 -03:00 = 18:10:59Z). That is red,
  which is the real round-23 defect. Yet that ledger verifies `clean ['LEDGER_CLEAN']`, so
  `verify` alone does not detect a retrospective binding. `round-23/wave1-attempts.json`
  fails with `AT_INVALID, LEGACY_ROW_UNBOUND, STARTED_MISSING`. Neither file is in R4's scope.
- **Implementation traps** (none exist yet; listed for BuildRoutedCheck):
  - Compare absolute instants. Round-23 rows use `Z` and commits use -03:00, so a naive
    string compare gives the wrong order.
  - Committer time has whole-second resolution while `at` has microseconds, so a commit at
    .9 s is recorded at the floor and can look earlier than an `at` in the same second.
- **Partial coverage:** routed item 4 also requires source writers in separate worktrees and
  accurate reports of extra invocations and resource units. R4 encodes none of that, yet the
  item is counted as held.
- Impacted axes: calibration (false provenance: self-attested ordering is presented as
  verified).

## Smallest safe corrections

1. **R1–R3 → one strong pin plus additive guards.** Require `git rev-parse
   REV:.ufo/waves/round-23` to equal 3e5b2c9d (the base tree). This covers `frozen`,
   `rejected`, all evidence and the CaseEscapedSpace copies, and it already holds at the tip.
   Then add:
   - R1: no path added under `tools/` or `corpus/knowledge/` between base and REV whose blob
     names a quota mechanism (`quotactl|qgroup|usrquota|prjquota|grpquota|Q_GETQUOTA`), and
     no added line under `tools/` containing `CaseEscapedSpace`.
   - R2: pin `tools/mori-retention-reconcile.py` (and `mori-retention-gate.py`) to base, or
     require a declared claim to change them. Replace the regex with a JSON walk over every
     added or changed `.json` blob, decoding JSON-in-string fields such as `stdout`, that
     fails on any `privacy_clearance` or `clearance` key with a truthy value. Exclude `.md`
     reports, so quoted mutants are not false reds.
   - R3: fail on any path added under `.ufo/waves/round-23/`. This is implied by the tree
     pin; state it as the reason.
2. **Relabel R1–R3** as held-axis regression guards, not "repaired" items. They should not
   count toward a calibration movement.
3. **R4:**
   - Scan every round-24 ledger (`*-attempts.json` and `*-ledger.json`).
   - Require every round-24 `wave*-run.json` and `*/swarm-registry.json` to be referenced
     by a row whose result is `started`.
   - Date the commit that introduced the REV blob OID of `dispatch_path` (its last change),
     not the first add.
   - Require each row to carry `bound_rev`, which must equal that commit and be an ancestor
     of the ledger commit, and commit the bind receipt (today it sits only in scratch).
   - Compare UTC instants with a strict 1 s margin.
4. **Honest before-value:** run the strengthened R4 over the round-23 wave 1 ledgers at base.
   That gives red, from the real defect, instead of red from "the round-24 directory is
   absent".
5. **Tradeoff for the canonical judge (not fixable within "committed bytes only"):** every
   committed timestamp is written by the L1, so R4 can prove internal consistency, not
   pre-call ordering. Either import a harness-owned spawn time into committed evidence (the
   session first-event time; the registry `createdAt` is plan time, 32 ms after the run file
   was born, so it is not a spawn witness), or label R4 "self-attested ordering". In its
   current form, R4 should not be admitted as a verified repair.

## Not run / tooling

- Not run: `tools/mori-routed-check.py`, which does not exist yet; any sandbox mutant; the
  dispatch-ledger selftest.
- Run (read-only git object reads, `python3 -I -B`, no files written in the lane): ledger
  `verify` over 15 ledgers at c725aa37 and one at 4059ffb5; the regex probe in-process.
- No installs or updates.
