# Mo56ConnKumitate — mori↔kumitate boundary check (round 56, C1 driver-liveness + C2 vote binder)

Seat: connector. Scope: does `tools/mori-driver-liveness.py` (C1) or
`tools/mori-vote-bind.py` (C2) touch kumitate-owned semantics — wave
plan/run/record/collect, lifecycle settlement, result acceptance — and is the
"`in_flight` is a log fact, not a settlement verdict" claim airtight against
kumitate's own definitions? Frozen counters/predicates are out of scope as fix
targets; weaknesses are named limits only.

## Verdict

**Agreement, not contested.** Both tools stay inside mori's FR3/FR5 boundary —
filesystem/log shape only — against every kumitate definition I could locate.
The `in_flight`-as-log-fact claim is airtight **semantically**; its one residue
is lexical (the word collides with a kumitate/ufo term of art), named below as a
LOW limit. No HIGH or MED findings.

## Evidence (commands + output + exit codes)

Boundary sources read:

- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md` — domain: OMP
  task/hub, ufo-fsd scripts & runtime. Owns the *origin* script layer
  (`/home/vgpnk/Projects/ufo-fsd-alpha/scripts/`, rows S1–S8) and runtime layer
  (R1–R11); Frontier holds durable-execution/heartbeat research. Nothing in the
  file claims the fleet's `.ufo/watchdog.log`, the hyaku driver, or hyaku
  wave-handoff files.
- `kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md` — the settlement
  contract this seat must not touch. Two load-bearing statements:
  - :40-44 (round-32 errata): live wave CLI admits only `plan`/`run`/`record`;
    "settlement is operator-supplied `ufo-swarm-results-v1` input to collect."
  - :101-104, :114-120: collect bridges settled member outcomes into the
    `ufo-mission-result-v1` envelope; `STATUS_OUTCOME` maps
    `completed→completed`, `failed→failed`, `timeout→failed`,
    `cancelled|canceled|aborted→aborted`; `collectEntries` joins
    dispatch×results×registry and fails closed on identity conflicts.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md` — :12-16 refuses
  dispatch/orchestration mechanism to kumitate; FR3 (:46) names the split:
  "mori reports filesystem shape; kumitate owns orchestration/result
  semantics"; the round-20 note (:145-154) already disclaims its own `settled`
  as "report-file settlement only, not kumitate's lifecycle settlement or
  result acceptance".

Corpus sweeps (read-only `grep` over `kumitate-shokunin/corpus`):

- `watchdog\.log|in_flight|heartbeat` → zero hits in kumitate `corpus/knowledge`
  defining the fleet watchdog log. Hits are only in wave build reports and in
  ufo-fsd internals (`l0-watch.heartbeat`, runner `staleAfterMs`), i.e., a
  different log at a different root.
- `in_flight|inflight|in-flight|unclosed|pairing` → kumitate uses the word
  family for queue/runner state: `inflightRunnerReservations`
  (`knowledge/queue-and-claim.md:126`), and "the in-flight round" = the highest
  round whose report may not be committed yet
  (`knowledge/round-close-gate.md:174`, `:354` where `in-flight` is a
  lane-round *status word* that the integrator adjudicates).
- `vote|tally|RECHECK|ENTAIL` → zero kumitate knowledge rows on seat-vote
  binding or the vote-line grammar; hits are unrelated tally prose.
- `settle|settlement|outcome|accept` → kumitate's settlement vocabulary is
  mission/wave-member scoped (`settleLiveEvidence`, `reapCandidate`,
  `STATUS_OUTCOME`, admission latches) — never lane×driver-round scoped.

Writers of the surface C1 reads (fleet root, not kumitate's origin scripts):

```
scripts/shokunin-watchdog.sh:66   log() { echo "$(date -Is) $*" >> "$UFO/watchdog.log"; }
scripts/shokunin-watchdog.sh:241-249  launch-fail ... :: <reason>
scripts/shokunin-watchdog.sh:266      launch $lane round=$n pgid=$pid
scripts/shokunin-watchdog.sh:398      wrap $lane round=$n landed; NOT respawning (fleet-wrap)
scripts/shokunin-watchdog.sh:405      complete $lane round=$n; advancing to round=$((n+1))
scripts/shokunin-watchdog.sh:448      lane-dead-no-report $lane round=$n; retry same round
scripts/hyaku/inline.sh:149           launch $lane round=$n pgid=$$ driver=hyaku-inline attempt=$a
scripts/hyaku/inline.sh:176           complete $lane round=$n; hyaku-inline attempt=$a
scripts/hyaku/inline.sh:182           lane-dead-no-report $lane round=$n; retry same round (...)
scripts/hyaku/fleet-commit.sh:46      .ufo/state/*|.ufo/watchdog.log refused as lane commits
```

So the log grammar authority (S544, the two writer scripts) lives in the fleet's
own `scripts/` tree — the orchestration *mechanism* mori refuses to own but
reads as evidence. Mori reading those bytes for grammar is exactly "mori
reports filesystem shape", not absorbing the mechanism.

Tool audit (lines: `tools/mori-driver-liveness.py`):

- :172 emits `"in_flight": row["last_event"] == "launch"` — a pure pairing fact
  over driver-log events per lane×round key `(round, attempt)`.
- :173 emits `"unclosed": len(row["open_launches"])` — same pairing count;
  docstring :35-36 calls it "a pairing count, not a failure claim".
- :237-238 emits verdict `DRIVER_LIVENESS_OK|UNAVAILABLE` and the in-band
  disclaimer "in_flight/unclosed are log-shape facts, not health verdicts".
- The output vocabulary contains **no** settlement words: no `settled`,
  `unsettled`, `outcome`, `accepted`, `member`, `wave`-status, none of
  kumitate's `STATUS_OUTCOME` spellings. Verified against the live output
  below.
- Read-only: the only `open(...,"w")` calls are inside selftest temp fixtures
  (:354, TMPDIR-scoped, `shutil.rmtree` cleanup); production `run()` opens the
  log `"r"` only (:210) and `state_shapes` uses `os.listdir`/`islink`/`isfile`
  with symlinks never followed (:179-198). Nothing writes `.ufo/state` or the
  log.

Live run (read-only, `cd` to my scratch first):

```
$ python3 .../tools/mori-driver-liveness.py --fleet-root /home/vgpnk/Projects/shokunin
verdict=DRIVER_LIVENESS_OK log={lines:1729, malformed:0, other_lines:121, mtime_age_s:~613}
state_dir={regular:21, symlink:0, dir:0, other:0}
lanes=23  mori={launches:66 completes:39 deads:17 in_flight:true unclosed:10}
          kumitate={launches:57 completes:49 deads:9 wraps:3 in_flight:false unclosed:3}
rc=0
```

Tool audit (lines: `tools/mori-vote-bind.py`):

- :64 anchors the vote grammar `^(RECHECK|ENTAIL) <hash12> <word>` — a
  mori-internal wave convention (the round-55 ledger
  `corpus/knowledge/kernel-v7.3-recheck-r55.md` is mori's own; no kumitate
  corpus row defines this grammar; fleet-root grep finds the format only in
  `scripts/hyaku/lane-addendum.md:23-25` as a counter note, not an owned
  grammar).
- :119-132 reads a results file's `results[].output` string fields only.
- :161-202 `tally` joins the ledger's expected disposition words against bound
  vote lines and emits counts (`agree/double/single/zero/dissent`,
  `bound_voters`). It does **not**: join dispatch×results×registry, map
  `STATUS_OUTCOME` statuses, emit member outcomes, or feed a judge/collect —
  `min_votes` is carried in the return dict but never gates a verdict.
- The r55 handoff file shape it parses: top keys `lane/round/wave/seats/results`,
  member fields `agent/name/note/output` (inspected
  `.ufo/waves/round-55/w1-results.json`, python3 read). This is the hyaku
  `<wave>-results.json` handoff, read as bytes; the tool asserts nothing about
  its schema authority.

Frozen guard on the boundary itself: `count-c1.py:45` carries
`HEALTH_WORDS = ("healthy","unhealthy","failed lane","is stuck","wedged")` and
:162-164 kills C1 (`norem`) if the pre-selftest tool text contains any — the
"no health verdict" half of the boundary is mechanically enforced, not just
prose.

## The `in_flight` airtightness question

Is "in_flight is a log fact, not a settlement verdict" airtight against
kumitate's definitions? **Yes, on every axis that matters:**

- *Subject*: kumitate settles wave members (dispatch-member identity ×
  `ufo-swarm-results-v1` status). Mori's key is `(lane, driver-round, attempt)`.
  Disjoint entity spaces — a lane round is not a wave member.
- *Close semantics*: kumitate's closes are operator-supplied statuses mapped by
  `STATUS_OUTCOME`. Mori's closes are `complete`/`wrap`/`lane-dead-no-report`
  driver lines. A driver `complete` records a landed lane round — the entry
  (`driver-liveness-r56.md:56-57`) explicitly disclaims "not a health verdict",
  and the tool never claims a `complete` proves member result acceptance.
- *Trust level*: the entry :60-62 disclaims authenticated-event status
  ("driver-authored shape, not authenticated events"), matching mori's census
  log-freshness arm.

The lexical residue: `in_flight` and `unclosed` are also ufo/kumitate
vocabulary (`inflightRunnerReservations`; "the in-flight round" as an
integrator status word at `round-close-gate.md:354`). A reader importing mori's
field into a settlement sentence would be mis-mapping a homonym — the tool's
`notes[]` disclaims this in-band, and the field set is frozen, so this is a
named limit for consumers, not a defect of the freeze.

Second-order trace: the field could be misused only by a *future* consumer that
equates driver-log pairing with wave settlement. The frozen C1 predicate never
requires such a consumer; the entry and `notes[]` already carry the disclaimer.
Nothing else in the round (contract, counters, entries) elevates `in_flight` to
a settlement claim.

## Contradictions

None found. The one apparent overlap — mori reporting `in_flight` while
kumitate's integrator owns `in-flight` status adjudication — resolves on
inspection: different nouns (driver-log pairing vs lane-round report-status),
different authorities, different entities.

## Named limits (for the record; routed items, not fixes)

1. **Writer-coupled grammar.** The frozen grammar's authority is two writer
   scripts outside this lane's tree. A future writer adding a new line shape
   degrades cleanly: unknown ts-first prose counts as `other_lines` (never
   malformed, never silent), unrecognized event rests count as `malformed`.
   Detection posture holds; grammar re-freeze on writer drift is a future
   round's recheck, not this round's defect.
2. **Homonym risk (LOW above).** `in_flight`/`unclosed` vs ufo queue
   vocabulary — consumers must not re-read these as settlement or capacity
   terms.
3. **C2 reads an operator-supplied artifact as bytes.** The r55 results file is
   settlement *input*; the binder treats it as an output carrier (seat `output`
   strings only) and never asserts schema authority. If the handoff shape
   changes, `read_results` returns `{}` and the tally reads `zero=` honestly —
   fail-visible, not silent.

## Findings

- LOW — `tools/mori-driver-liveness.py:172-173`: field names `in_flight` /
  `unclosed` collide with ufo-queue vocabulary (`inflightRunnerReservations`,
  `queue-and-claim.md:126`) and the integrator's `in-flight` status word
  (`kumitate corpus/knowledge/round-close-gate.md:354`). Semantics are
  airtight as log facts; the collision is lexical only and disclaimed in-band
  (`notes[]` :239) — named limit for future consumers, frozen field set not
  proposed for change.
- LOW — `tools/mori-driver-liveness.py:54-62` + `driver-liveness-r56.md:22-44`:
  the frozen line grammar is anchored on fleet writer scripts outside the
  lane's tree (S544 own-work). New writer line shapes degrade to
  `other_lines`/`malformed` (visible, never silent); acceptable posture —
  recheck-on-writer-drift is the carried route.
- LOW — `tools/mori-vote-bind.py:161-202`: `tally` reads the hyaku
  `<wave>-results.json` member `output` fields as bytes and emits coverage
  counts, never member outcomes; shape drift would read `zero=` honestly.
  No kumitate `collect`/`STATUS_OUTCOME` semantics touched.
- (Agreement statement) C1's `in_flight` claim verified airtight against
  `kumitate corpus/knowledge/swarm-wave-lifecycle.md:40-44,101-120`
  (settlement = operator-supplied `ufo-swarm-results-v1` → `STATUS_OUTCOME` →
  `ufo-mission-result-v1`): disjoint entity space, disjoint close semantics,
  no shared vocabulary in emitted fields. C2's tally likewise outside
  plan/run/record/collect.

Report: .ufo/waves/round-56/w1/Mo56ConnKumitate.md
