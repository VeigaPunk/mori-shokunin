# ScoutWaveSettlement — wave-1 settlement evidence at `a730ecf`

Seat: `MoriR24.ScoutWaveSettlement` (scout, leaf — no subagents dispatched).
Rev measured: `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (lane `master`).
Objects read: `.ufo/waves/round-24/{wave1-spec,wave1-run,wave1-attempts,wave1-assignments}.json`,
`.ufo/waves/round-24/w1/swarm-registry.json`, `.ufo/waves/round-24/w1/*.md`,
`.ufo/waves/round-24/wave1-response.txt`, `.ufo/waves/round-24/evidence/wave1-bind.json`,
`tools/mori-dispatch-ledger.py`, agent history (`history://`).

## Verdict

**Survivor.** Every part of the settlement claim holds at `a730ecf`: 33 members, 33 report
files, roles identical across all three role-bearing artifacts, no unaccounted or duplicated
seat, and `mori-dispatch-ledger.py verify` clean and falsifiable. Three caveats narrow what
the artifacts alone prove (§Caveats); none contradicts the claim.

## Claim tested

"33 members, every member has a report file in `.ufo/waves/round-24/w1/`, roles match, no dead
or replaced seat is unreported, and `python3 -I tools/mori-dispatch-ledger.py verify --repo …
--rev a730ecf… --ledger .ufo/waves/round-24/wave1-attempts.json` is clean."

## Commands run and outputs

### 1. Ledger verify (the declared clean result)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 -I ./tools/mori-dispatch-ledger.py verify \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --rev a730ecfefbdb5c31b1db13aca2c40eecd5e97abc \
    --ledger .ufo/waves/round-24/wave1-attempts.json
{"finding_id":"LEDGER_CLEAN","finding_ids":["LEDGER_CLEAN"],"findings":[],"ledger_path":".ufo/waves/round-24/wave1-attempts.json","mode":"verify","rev":"a730ecfefbdb5c31b1db13aca2c40eecd5e97abc","rows":[{"attempt":1,"index":1,"reasons":[],"result":"started","started_ids":33,"status":"bound","tasks_count":33}],"schema":"mori-dispatch-ledger-v1","status":"clean","totals":{"bound":1,"ledger_findings":0,"rows":1,"unbound":0}}
EXIT=0
```

Reproduced identically in a fresh `git clone --no-hardlinks` of the lane checked out at
`a730ecf`, run against the clone's own path (`EXIT=0`).

### 2. Independent recomputation of the bound digest

The ledger stores `payload_sha256 f3770cef…` and `payload_bytes 36222`
(`wave1-attempts.json:7-8`). Hashing the raw `wave1-run.json` file gives
`18a0994e88d7b972…` / 43,254 bytes, which does **not** match — expected, because
`_payload_identity` hashes only the canonical `{"context","tasks"}` object
(`tools/mori-dispatch-ledger.py:127-165`). Recomputing that canonical form myself from the
committed file:

```
canonical sha256: f3770ceff4a97719923f9c0c5c69a56ba2649a638aea9c62c2602cb386c129a2
canonical bytes: 36222
ledger row     : f3770ceff4a97719923f9c0c5c69a56ba2649a638aea9c62c2602cb386c129a2
match: True
```

So the row binds to the 33-task payload actually committed at the rev, not to a stale or
unrelated payload.

### 3. Does `clean` mean anything? Two mutants in a private clone

Clone: `/fast/scratch/hyaku/mori-r24-a2/w2/MoriR24.ScoutWaveSettlement/lane`
(`git clone --no-hardlinks`, `checkout a730ecf`). Mutants committed only in that clone;
the lane repo, its index and its jj state were never touched.

- Baseline at `a730ecf`: `LEDGER_CLEAN`, exit 0 (identical to §1).
- Mutant A `3df2637bc07135b81435c7f35c2d9e2c10b63b30` — `payload_sha256` set to 64 zeros:
  `{"finding_id":"LEDGER_UNBOUND","finding_ids":["PAYLOAD_SHA256_MISMATCH"],…,"status":"failed",…,"unbound":1}`, `EXIT=1`.
- Mutant B `440adad134c073fb27fa4a083455e23df792dd8a` — `started_ids` 33 → 32:
  `{"finding_id":"LEDGER_FINDINGS","finding_ids":["STARTED_IDS_MISMATCH"],…,"status":"failed"}`, `EXIT=1`.
  (`STARTED_IDS_MISMATCH` is the check at `tools/mori-dispatch-ledger.py:300-302`.)

The clean result is therefore discriminating, not vacuous. The verifier also checks
`payload_bytes` (`:236-237`), `tasks_count` (`:238-239`), contiguous attempts (`:267`),
ascending `at` (`:276`), and single-`started`-last (`:291-295`). The tool blob is identical
at the rev and in the working tree (`rev_blob = work_blob = b86525c6a9fe0d44e90127323ff291104dcfb5fd`),
so the result is reproducible with the rev's own bytes.

### 4. Membership: 33, everywhere

Extracted with `python3 -I` from the five artifacts:

```
spec items: 33            run counts: {'spawn': 33, 'resume': 0, 'total': 33}
run taskCall.tasks: 33    assignments: 33    registry members: 33    (all kind spawn)
attempts: tasks_count 33, started_ids 33, result started, refused_text null
response.txt: 33 listed jobs
history: 33 MoriR24 wave-1 agent ids (all parent MoriR24, all parked)
spec names == registry names: True       run task order == spec item order: True
assignment keys == spec names: True      assignment values == registry agentIds: True
```

Anchors: `wave1-spec.json:6` (`items`), `wave1-run.json:16-19` (counts), `:234`
(`taskCall`), `:404` (`resumeSends: []`), `wave1-attempts.json:3,9,11,13`,
`w1/swarm-registry.json:7`.

### 5. Report files: 33, real, unmodified since the rev

`git ls-tree -r a730ecf -- .ufo/waves/round-24/w1` lists exactly 33 `.md` files plus
`swarm-registry.json`; the name set equals the registry member set exactly. Each report is
substantive — 7,181 bytes (`ReviewRetentionState.md`) to 61,933 bytes (`LivePressureCapture.md`),
130–914 lines — no symlinks, no zero-byte or placeholder files. Blob comparison of all 33
working-tree reports against the rev produced zero `DIFF` lines, as did the same comparison
for the five JSON artifacts. The 33 run trailers all read
`Report: write your scoped findings to .ufo/waves/round-24/w1/<member>.md` — zero path
mismatches against member names.

### 6. Roles match

Role triples (spec item `role`, run task `agent`, registry `role`) agree for all 33 members,
zero mismatches. Counts: scribe 12, executor 5, critic 5, scout 4, reviewer 4, connector 2,
mutation-tester 1 (sum 33). `wave1-response.txt` names exactly those seven role kinds.
Report bodies do not self-declare a role field, so role equality is a property of the three
metadata artifacts, not of the reports.

### 7. No dead or replaced seat

- Registry: all 33 members `kind: spawn`; no `resume` member; `run.resumeSends` empty;
  the ledger has one attempt, `result: started`, `refused_text: null`.
- Agent history: the 33 wave-1 ids all exist (parent `MoriR24`, status `parked`). The
  69 MoriR24 seats in history are exactly wave 1 (33) ∪ wave 2 (36), with **zero**
  unaccounted ids; no wave-1 id carries a `-2` replacement suffix, and no wave-2 id reuses
  a wave-1 name (`w1 ids ∩ w2 ids = ∅`).
- No w1 report and no contract text mentions a seat dying, being replaced or respawned; the
  only `replac*` hits are ordinary prose about replacing text in documents.
- Provenance of the files: all 33 seat transcripts contain a 60-character slice from the
  middle of their exact dispatched task and their own report path. 31 show a direct
  `write(...)` or `edit(...)` call on their own report path; `LivePressureCapture` copied its
  report in with `bash cp`; `BuildPressureTool` shows no lane write and its report landed with
  the tool in `6ee62487` (see caveat 4).

### 8. Binding chronology (spot check, C1's R4 territory)

`git log -1 --format=%cI` on the rev: `wave1-spec.json` and `wave1-run.json` were added by
`06d4f4d26311eb6fa425ee471496816ddf1d8966` at `2026-10-22T05:13:57-03:00`; the ledger row is
`at 2026-10-22T05:14:13.926366-03:00` (`wave1-attempts.json:4`); the ledger itself was added by
`4059ffb` at `05:14:40-03:00`. Dispatch commit precedes the row's `at`, which precedes the
row's own commit. `evidence/wave1-bind.json` records the same digest `f3770cef…` at rev
`06d4f4d`. Note that `verify` does **not** check this ordering; it was checked separately
here (see caveat 5).

## Caveats and limits

1. **The registry records membership only.** Every member has `kind`, `agentId`, `role` and
   `item: null` — no status, no completion flag, no report path (`w1/swarm-registry.json:8-12`
   and all 33 siblings). The member→report pairing therefore rests on name convention, the
   run task trailers and the transcripts, not on a registry field. A registry key could in
   principle exist without a report; here all 33 do have one.
2. **"No dead seat" is a negative inference.** The ledger certifies the dispatch outcome
   (`started`, 33 ids) only; no artifact records per-seat liveness or a death event. The
   evidence is: 33 planned ids = 33 history ids = 33 reports, plus zero unaccounted or
   duplicated ids. That is strong, but it is absence-of-counterexample, not a positive record.
3. `wave1-run.json` embeds a `registry.members` copy in which all 33 `agentId` values are
   `null`, while `w1/swarm-registry.json` has them filled. A naive member-by-member comparison
   reports 33 diffs. The timestamps fit a pre-spawn draft that was filled after the call
   (`createdAt 08:13:51.297Z`, `updatedAt 08:14:34.622Z`, registry committed `08:14:40Z`,
   `w1/swarm-registry.json:4-5`). [INFERENCE] This is a draft-then-fill sequence, not a
   contradiction; the bound payload is the `taskCall`, which carries no member ids.
4. **One report's authoring is not visible in its transcript.** `BuildPressureTool.md` was
   committed in `6ee62487` together with `tools/mori-pressure.py`; the seat's transcript ends
   with its findings and the report trailer but shows no lane write (it worked in
   `/fast/scratch/hyaku/mori-r24-a2/wt-pressure`). The file's content is scope-consistent and
   its presence satisfies the claim; whether the L1 transcribed it is not established.
5. `verify` checks payload binding and ledger-internal shape, not chronology; a ledger whose
   row `at` precedes its dispatch commit would still be "clean". The contract's R4 covers
   that, and the actual times here are ordered correctly (§8).
6. Roles in the reports themselves were not graded (no role field); the match is across spec,
   run and registry only.

## Not run

- No full-content review of the 33 reports (only size, header, trailer, blob identity and
  transcript provenance); content correctness is other seats' scope.
- No exhaustive byte-diff of the embedded registry beyond `agentId` (the only differing field).
- No check of wave-2 settlement (36 members) beyond the unaccounted-seat comparison.
- No mutation of `wave1-spec.json`, `wave1-assignments.json` or the registry, and no mutants
  in the lane repo; both mutants ran in the private clone only.

## Tooling

No installs or upgrades (`pacman` untouched, no `uv`/`npx`/binary installs). Tools used:
`python3`, `git` (read-only in the lane; commits only in the private clone), `sha256sum`,
`grep`, `find`, `stat`.

Report: `.ufo/waves/round-24/w2/ScoutWaveSettlement.md`
