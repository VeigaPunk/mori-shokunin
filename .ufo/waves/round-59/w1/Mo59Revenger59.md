# Mo59Revenger59 — the `.ready` handoff, reverse-engineered (mori rounds 47–59; 56–58 primary)

Verdict: **adversarial findings F1–F4** — the documented handoff mis-specifies both the dispatch
receipt and the settlement artifact — plus **no counterexample** for five positive invariants
(INV1–INV5, §4). Read-only: no production file, corpus, registry, SCORECARD, LOG, or VCS state
was touched. Scratch `/fast/scratch/hyaku/mori-r59/Mo59Revenger59` was created, used for `TMPDIR`
only, and removed; every receipt below is inlined (nothing to copy back).

## 1. Method (bounded)

- Read in full first, as ordered: `.ufo/waves/round-59/contract.md`,
  `.ufo/waves/round-59/count-c1.py`, `.ufo/waves/round-59/count-c2.py` (freeze
  `60b3a76`, entering `2b9f0397`). Neither counter was executed: C1/C2 are this wave's own
  claims, not this seat's, and running them mid-wave would be an unrequested score action.
- Read the writer, not just its output: `scripts/hyaku/inline-dispatcher.py`
  (`register()` :231–271, `finalize()` :288–303, `bootstrap()` :360–394, contract docstring :46–55),
  `scripts/hyaku/ready-watch.sh`, `scripts/hyaku/lane-addendum.md` §6 (:113–119).
- Compared committed bytes to working tree for mori rounds 47–59 (`git ls-files`,
  `git show HEAD:<path>`, `git log --all -- <path>`), and used **file mtimes** as write times,
  because commit times are retroactive (F5).
- Corroborated with the driver's own runtime log, `.ufo/state/inline-dispatcher.log`
  (77,844 lines, `2026-10-26T01:05:36` → `2026-10-28T02:53:55`), which timestamps
  `spawned`/`done`/`partial`/`cap-defer`/`adopted` events. That log is driver runtime state
  (never committed); it is the only source for *when* the driver acted.
- Bounds: mori lane only, rounds 47–59; no counter runs, no fixture repos, no writes.

## 2. Reconstructed contract (who writes what, when)

| Artifact | Writer | Trigger | Evidence |
|---|---|---|---|
| `w1-spec.json` | L1 (`build-w1-spec.py`) | spec build | mtime r56 `10:54:48` |
| `w1-dispatch.json` | L1 (builder) | after validation, before `.ready` | mtime r56 `10:55:13`; `w1/swarm-registry.json` `updatedAt=2026-10-27T13:55:13.930Z` = same second, local −0300 |
| `w1.ready` | **L1** (the seat that owns the round) | after the dispatch payload is validated | `{lane,round,wave,dispatch(abs),l1}`; mtime r56 `10:55:29` (+16 s after dispatch); `l1` = the L1's spawn label (`MoriR56`…`MoriR59a2`), exactly as `L1_PROMPT` instructs |
| `w1.ready.partial` | **dispatcher** `register()` | only while a fill spans ticks; atomic tmp+`os.replace` (:124–129); deleted on completion (:272–274) | absent at rest in r56–r59; `partial mori 56 w1 2 64` … `9 64` log lines |
| `w1.ready.dispatched` | **dispatcher** `register()` :266–267 | **after the LAST seat is spawned** — not on pickup | line 1 timestamp `==` file mtime to the second in r56 `11:08:27`, r57 `12:45:45`, r58 `14:30:58`, r59 `02:53:55`, and each equals the log's `spawned mori <r> w1 64` line |
| `w1-results.json` | **dispatcher** `finalize()` (normal path) | first tick where `nlive==0` (:306–309) | `done mori … round-N/w1-results.json` log timestamps equal results mtime (INV3) |
| `w1-results.json` | **a second, undocumented writer** | operator/L1 recovery after the orchestrator session died | r53 §F3 |

Driver contract docstring (:52–55): "the L1 writes … `<wave>.ready`; we spawn every
`taskCall.tasks[]` seat inline, mark `<ready>.dispatched`, and when no seat is live write
`<dispatch-dir>/<wave>-results.json` and message the L1 `WAVE-DONE`."

## 3. Lifecycle observed, exact timestamps (local `-03:00`)

```
round  ready(mtime)        pickup(1st log)  dispatched(mtime)   results(mtime)
r56    10:55:29 (+16s→)    10:55:45         11:08:27 (+13m02s)  11:34:26
r57    12:38:33 (+14s→)    12:38:47         12:45:45 (+07m12s)  13:06:39
r58    14:21:44 (+03s→)    14:21:47         14:30:58 (+09m14s)  14:43:22
r59    02:52:25            (none logged)    02:53:55 (+01m30s)  absent (wave live)
```

Ordering: `spec → dispatch.json → ready → [partial …] → dispatched → results`; results appears
**6–45 s after the last seat report is written** in r56–r58 (r56 last report `11:33:59`,
r57 `13:05:53`, r58 `14:42:44`). That is one tick (`every=30`, :337) after the last seat stops
being live — consistent with the documented "when no seat is live".

Round 59 state: `w1.ready` is committed (`8ff344ff`); `w1.ready.dispatched`, `w1/`,
`w1-dispatch.stderr` are **untracked** (`git status --porcelain` → `??`), i.e. the wave is live and
only its settled predecessors are committable evidence.

## 4. Positive invariants — no counterexample (16 committed mori waves, r47–r59)

- **INV1** `results.json` ⇒ `.ready` ∧ `.ready.dispatched`: 16/16. Sweep printed
  `anomalies (results w/o ready): []`, `anomalies (results w/o dispatched): []`.
- **INV2** `.dispatched` line-1 timestamp `==` file mtime: 17/17 committed markers.
- **INV3** results mtime `==` the `done mori` log timestamp: r51, r52, r55, r56, r57, r58 → 6/6
  exact; r54 differs by 1 s (`02:16:51` vs `02:16:50`) — mtime second truncation, not a rewrite.
- **INV4** `results.seats == len(results) == len(dispatch.taskCall.tasks) == len(registry.members)`:
  r56/r57/r58 all 64/64/64/64.
- **INV5** results seat list is name-identical and order-identical to `taskCall.tasks`:
  `names equal: True` in r56, r57, r58.

## 5. Divergences — documented vs observed

### F1 (adversarial) — `.ready.dispatched` is a *spawn-completion* receipt, not a ~15 s pickup receipt
`lane-addendum.md:114`: "The orchestrator's dispatcher takes it within ~15 s (marker
`<wave>.ready.dispatched`)". The two halves do not share a timestamp:

- pickup really is fast — first dispatcher log after the ready: r56 **+16 s** (`10:55:45
  cap-defer … occupied 96`), r57 **+14 s** (`12:38:47 spawn-cap … Mo57Reviewer04`), r58 **+3 s**
  (`14:21:47 cap-defer … occupied 96`);
- the **marker** lags that pickup by **7m12s–13m02s** (r56–r58), 1m30s in r59, and up to **30m12s**
  (r53: ready `22:41:14` → dispatched `23:11:26`). Across all 16 committed waves the marker lag is
  **1m53s–30m12s; never ~15 s**.

Mechanism (code, not inference): `register()` writes the marker only in its final block
(:266–267) after `if len(mine) < len(tasks): … return False, n` (:264–265) has stopped firing.
Seat spawning is throttled by the host gate (`SEAT_CEILING=96` / `HOST_JOB_CAP=100`, :108–110), so a
64-seat wave fills in tranches and each deferred tick logs `cap-defer … occupied 96`.
Consequence: a reader watching "no marker after 15 s ⇒ dispatcher stalled" would mis-read every
r56–r58 fill as a stall, and a reader treating marker time as pickup time would record a 7–13 min
orchestrator latency that never happened.

### F2 — results.json per-seat schema is not the documented one
`lane-addendum.md:116`: "per seat: name, agent, id, status, final output". Observed keys are exactly
`{name, agent, output, note}` for r47, r48, r54, r55, r56, r57, r58 (and r59's frozen-claim
neighbours): **no `id`, no `status`**. `finalize()` :292–296 emits `{'name','agent','output','note'}`;
`note` is `None` unless output was lost. `agent` carries the *role* string (`reviewer`, `revenger`, …),
identical to `registry.members[name].role` for 64/64 seats in r56–r58. So `:119`'s "seat counts, dead
seats and role mix come from results.json" is observable only as `seats`, `note != None`, and
`agent`-as-role; there is no status field to read.

### F3 (adversarial) — results.json has a second writer with a different schema
r53 `w1-results.json` (mtime `2026-10-27T00:14:47`) has **no `done mori` log line at all** and carries
`settled_by: "orchestrator session exit (no seat live)"`, `spawned: 67`, `outputs_recovered: 66`,
a top-level `note` (session killed at `23:57:36` by "an operator-requested `omp update`"), and a
per-seat `report_file` key absent from every dispatcher-written file. Top-level key set:
`['lane','note','outputs_recovered','results','round','seats','settled_by','spawned','wave']` vs the
normal `['lane','results','round','seats','wave']`. One seat is `output: null` (`Mo53RevLedgerProse`).
So "results.json exists" does **not** imply "the dispatcher settled the wave"; the frozen C2 counter's
`DRIFT_SCAN` arm chooses exactly this file to FAIL on, which is the drift being tested.

### F4 (adversarial) — `.ready.dispatched` does not imply settlement at all
r49 `w1` (dispatched `2026-10-25T21:48:31`) and r50 `w1` (dispatched `2026-10-26T05:58:49`, log
`spawned mori 50 w1 40`) carry committed markers, have seat reports on disk (50 and 6 files), and
**never produced `-results.json`**: `git log --all -- .ufo/waves/round-49/w1-results.json` and
`…round-50/w1-results.json` return nothing, and no `done mori … (49|50)` line exists. r50 `w1` was
even `adopted` at `2026-10-26T08:29:36` (log line 1687) and still never
finalized; the round was re-run as `a2w1` (adopted `10:44:06`, `done 10:50:12`). Mechanism: `finalize`
runs only from `tick()` over entries in `WAVES`; a wave that was adopted and then lost with the next
kernel never re-enters `WAVES` (bootstrap skips result-less *and* fully-dead waves, :377–378).
Consequence: 2 of 16 committed mori waves are permanently dispatched-but-unsettled; any predicate
"marker ⇒ settlement" or "one results per marker" is false.

### F5 — marker line 2 is the host *agent label*, not an identity with the seat name
Docstring :46–49: the file "keeps {seat: job id} … so bootstrap() … tracks liveness by job id".
Observed r56–r58: the value is the host-assigned label and it **differs from the seat name** for
**13/64** seats in r56, **2/64** in r57, **2/64** in r58, **0/64** in r59 — always a `-N` dedup
suffix, e.g. `Mo56ScoutSiblingOverlap → Mo56ScoutSiblingOverlap-3`,
`Mo58Reviewer01 → Mo58Reviewer01-2`, `Mo58Reviewer02 → Mo58Reviewer02-3`. Key set and task order are
still exact (`ids.keys() == registry.members` = True, order == `taskCall.tasks` = True). A consumer
that assumes `value == name` happens to be right for r59 and wrong for 17 seats in r56–r58.

### F6 — provenance: committed `.ready`/`.dispatched` are retro-committed evidence, not dispatch-time artifacts
For the primary rounds the markers enter git *after* settlement: r56 markers land in `eac193ca`
(committer `11:42:33`) in the same commit as the results (`11:34:26`); r57 all four files land in one
commit `6f3f8482` (committer `13:14:35`, results `13:06:39`); r58 markers land in `8053ef91`
(committer `15:30:13`) 47 min after results (`14:43:22`) as "wave markers (hyaku orchestrator,
pre-closure)". Therefore `git log -- <marker>` order is the reverse of the lifecycle order; only the
**file mtime** (and the driver log) reconstruct the real sequence. Committed blobs are byte-identical
to the working tree for all r56–r58 markers (sha256 head == worktree).

## 6. Out-of-scope observations (bounded, not scored here)

- Legacy marker format: mori r47–r50 markers are **one line** (timestamp only, no id map); line 2
  first appears in mori r51 (`2026-10-26T19:48:42`). kama r47 already has 2 lines
  (`2026-10-26T18:29:29`), so the format changed between `2026-10-26T09:50:39` (mori r50 `a2w1`,
  1 line) and `2026-10-26T18:29:29`. Any reader doing `lines[1]` unconditionally breaks on 9 legacy
  markers (e.g. `IndexError` on `.ufo/waves/round-49/w1.ready.dispatched`).
- `.partial` is written atomically (:124–129) but `results.json` is not
  (`json.dump(…, open(out,'w'))`, :296): a death mid-write leaves a truncated file that `bootstrap`
  treats as already settled (`if os.path.exists(res): continue`, :376–377) — **[INFERENCE]**, no
  truncated artifact was observed in r47–r59.
- No `notify-failed` line exists for mori in the driver log, so `WAVE-DONE` delivery is consistent
  with the documented flow in r47–r59 (absence of failure is not proof of delivery).
- r56's `w1.ready` has no trailing newline (147 bytes); r57–r59 end with `\n` (148/148/150). JSON
  parse is unaffected; noted only because byte-level evidence tools may flag it.

## 7. Confidence

- Lifecycle ordering, writers, and every timestamp in §3: **high** — three independent sources agree
  (file mtime, marker line 1, driver log), and the marker/mtime equality is exact to the second in
  17/17 markers.
- F1, F2, F4, F5: **high** — counterexamples are committed artifacts plus a direct code pointer.
- F3: **high** for the observed schema/`settled_by` divergence; **medium** for the identity of the
  recovery writer (the file says what happened, not who ran it; the operator session exit and the
  `settled_by` string are the only attribution).
- F6: **high** for commit-vs-mtime order; the *reason* for retro-committing (evidence bundling) is
  **[INFERENCE]** from the commit subjects.
