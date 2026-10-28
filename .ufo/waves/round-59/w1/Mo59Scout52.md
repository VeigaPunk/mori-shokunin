# Mo59Scout52 — sibling-lane wave-settlement overlap survey (round 59, C2)

Scope: do kumitate (swarm-wave lifecycle), tsukuroi, or kaidoku already hold claims
about `*-results.json` shape or seat settlement, relative to frozen C2
(`tools/mori-settlement-scan.py` + `corpus/knowledge/wave-settlement-artifacts-r59.md`,
contract `.ufo/waves/round-59/contract.md`, counter `.ufo/waves/round-59/count-c2.py`).
Read-only reconnaissance. Overlap only; no judgment, no remediation.

C2's claim surface (from `count-c2.py:55-76` and `tools/mori-settlement-scan.py:39-110`):
`<wave>-results.json` = top-level object `{lane, round, wave, seats, results[]}`;
`seats` int == `len(results)`; member keyset exactly `{name, agent, output, note}`;
`name` unique; `agent` in the closed 10-role set; `output` null-or-string;
r53 file drifts (extra `report_file` member key).

---

## kumitate — substantial overlap

### (a) Committed gate `scripts/inline-dispatch-evidence.mjs` asserts the same `results[]` shape

`/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/inline-dispatch-evidence.mjs:261-287`:

- `:261-262` reads `${base}/${wave}-results.json`; parse failure → `RESULTS_UNREADABLE`.
- `:283` `const rs = Array.isArray(results.results) ? results.results : [];`
- `:284` `if (results.seats !== rs.length || rs.length !== tasks.length || String(results.round) !== String(round) || results.wave !== wave) findings.push('RESULTS_MISMATCH:count seats=… rows=… dispatched=…')` — the same `seats == len(results)` check as `mori-settlement-scan.py:62-63`, plus dispatch-count and round/wave binding.
- `:285-287` member-name/`agent`-role binding to the dispatch payload:
  `const rn = new Map(rs.map((r) => [r.name, r.agent]));` — confirms `agent` = seat role in the live schema; `RESULTS_MISMATCH:<name>` per unbound/extra member.
- Selftest fixtures (`:447`) build `w1-results.json` as `{lane, round, wave, seats, results: rs}` — the same top-level keyset mori scans.

So kumitate already enforces, at its own lane gate: top-level object, `results` array,
`seats==len(results)`, per-member `name`/`agent` fields, and member-name uniqueness is
implicitly required by its 1:1 map (a dup name collapses the map and is caught only
through the count/dispatch arms — weaker than mori's `duplicate_names`).

### (b) `corpus/knowledge/swarm-wave-lifecycle.md` — schema + role-enum + join claims

`/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md`:

- `:107-110` `RESULTS_SCHEMA = 'ufo-swarm-results-v1'`, `REGISTRY_SCHEMA`,
  `DISPATCH_SCHEMA`, `PLAN_SCHEMA` constants with `MAX_INPUT_BYTES`/`MAX_REGISTRY_BYTES`.
- `:62-65` `SWARM_ROLES` exported closed set: `scout, reviewer, critic, connector,
  sentinel, executor, mutation-tester, revenger, simplifier, scribe` — byte-identical
  vocabulary to `mori-settlement-scan.py:39-40` `ROLES` (including the planner
  exclusion, "Planner / distiller / labrat / Main are frozen-topology seats, not
  swarm lanes").
- `:40-41` "settlement is operator-supplied `ufo-swarm-results-v1` input to collect" —
  i.e., the `*-results.json` file is the collect input, and per `:122-129`
  `collectEntries` requires every dispatch member ↔ exactly one results row
  (`unmapped_member` / `unexpected_member` / `duplicate_member` refusals) — a
  *cross-artifact* (dispatch ↔ results) join, beyond mori's per-file shape scan.
- `:114-120` `STATUS_OUTCOME`/`FAILURE_CLASS_REASON` freeze the status→outcome map and
  typed failure causes — settlement *semantics* (outcome classification), not shape.

### (c) `corpus/QUALITY.md` — settlement evidence claims, and one direct tension

`/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/QUALITY.md:991-997` (Q59) and
`:923-927` (Q58):

- `:993` "the non-author spot-check re-runs the same gate … and re-derives the dead set
  from the transcripts, **never from `results.json`**" — an explicit claim that
  `*-results.json` is NOT the authoritative dead-seat record (host transcripts are).
  Tension with C2's use of the file as the settlement artifact: consistent only because
  mori's scan measures shape/consistency (seats==members, keyset), not seat death.
- `:995` enumerates `RESULTS_MISMATCH` among the gate's failure codes; `:996` committed
  controls include `results-name-swap` → `RESULTS_MISMATCH` — a control battery over
  the same member-name binding C2's tool re-implements (`duplicate_names`, `agent_bad`).
- `:924` documents schema drift in the *registry* side: `w1/swarm-registry.json`
  `members` is "an object with `agentId: null` on all 32 seats" read as
  `REGISTRY_UNREADABLE:members-absent` by the dispatch-actual gate — a second
  members-object-vs-list fact adjacent to C2's member list check.

### (d) Lessons-level reads of `results[]` shape

- `corpus/lessons/round-65-verifier-spotcheck.md:20` — verifier re-derives seat totals:
  `git show 52f8497:.ufo/waves/round-65/w1-results.json | jq '.results | length'` →
  "45 results, 45 with non-empty output" (same `output` non-null check as
  `mori-settlement-scan.py:93-98`; verified: r65 file has keys
  `{lane, results, round, seats, wave}`, member keys `{agent, name, note, output}`).
- `corpus/lessons/round-41.md:200-202` — "The census counts a report as present when it
  is a non-empty regular file; it does not detect a `STATUS: started` stub (sibling
  lane mori's settlement scan does). On rounds 38–41 the eight payload report counts
  agree with mori's scan" — kumitate already knows/uses mori's settlement scan;
  cross-lane agreement claimed for rounds 38–41.
- `corpus/lessons/round-60-verifier-spotcheck.md:186-191` (R60-V6) — "27/32 seats
  settled `exit=-9 session=null`" read from `launcher-progress.tsv`, not results.json.

## tsukuroi — moderate overlap

### (a) Committed gates consume the same `results[]` member shape and give `output` JSON semantics

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-record-r42.py:17,122`,
`check-scrub-record-r43.py:22,181`, `check-scrub-record-r44.py:26,208-213` (r44 quoted):

- `:26` "the seat is a task of `.ufo/waves/round-44/w2-dispatch.json` (taskCall.tasks,
  same name and agent role, exactly once) with exactly one result of the same name and
  role in `w2-results.json`".
- `:208-213` `res = load_json(lane, rev, f'{WAVE}/{wave}-results.json') …`
  `ent = [r for r in (res.get('results') or []) if r.get('name') == name and r.get('agent') == role]`
  `if len(ent) != 1 or not isinstance(ent[0].get('output'), str): return None, None`
- `:193-203` `declared_line()`: if `output` parses as a JSON object it must hold string
  `verdict_line`, and a `verdict` key when present must equal that line's verdict word;
  otherwise the output's FIRST line must fullmatch the declared verdict. This is a
  committed claim about `output`'s *content semantics* (double-encoded JSON) that
  mori's scanner treats as opaque (checks null/string/non-empty only, `:93-98`).

Overlap: same `{name, agent, output}` member reading and exactly-once binding;
tsukuroi adds per-seat `output` verdict semantics mori deliberately does not bind.
(Also `check-scrub-grounding-r45.py` and `check-scrub-admission-r46/r47.py` hit the
same grep — same family.)

### (b) Ownership routing: settlement questions are mori's

`corpus/knowledge/adjacency-handoffs-fleet-r1.md:52-53` and
`adjacency-handoffs-fleet-r1.json:94-95`: ADJ-05 hands "Silence/settlement without a
dispatch-mechanism defect" to mori (`"negative_recipient": "mori"`); the JSON
counterexample reads "A lane silence or wave-settlement question without a
dispatch-mechanism defect goes to mori." — an explicit sibling claim that
wave-settlement knowledge belongs to mori, not tsukuroi/kumitate.

### (c) Post-settlement record rules

`corpus/knowledge/seat-boundary-r22.md:29-31`: "After settlement, preserve raw report
bytes, observed error attribution and sanitized request metadata. Mark incomplete
trace coverage could-not-evaluate … Report actual request violations, strict receipt
faults and cohort accounting separately. Never replace failed seats …" — seat-
settlement *policy*, not artifact shape.

## kaidoku — moderate overlap, different artifact family

### (a) `tools/round-30/settle-gate.py` — settlement gate that deliberately does NOT read `*-results.json`

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/settle-gate.py:1-56`:
its ledger is `swarm-registry.json` (`members` "object of names", `:98-100` — same
members-as-dict fact kumitate QUALITY :924 documents) plus a lane-authored
`settle.tsv` (`name<TAB>status<TAB>utc<TAB>report_sha256[<TAB>note]`, `:17-31`), then
report bytes on disk (`REPORT_ABSENT`, `REPORT_SHA_MISMATCH`, `:34-42`). The
orchestrator `*-results.json` is not an input at all — a divergent settlement record
design versus both C2's scan and kumitate's gate.

### (b) `tools/round-42/prefile-gate.py` — results-file *presence* and a second naming variant

`:6-8` "every `.ufo/waves/round-N/<wave>.ready` has a `<wave>.ready.dispatched` marker
AND a results file (`<wave>-results.json` or `rN-<wave>-results.json` beside the
dispatch json)"; `:218` candidate list
`["%s/%s-results.json" % (base, wave), "%s/r%d-%s-results.json" % (base, self.n, wave)]`.
Kaidoku asserts an `r<N>-<wave>-results.json` naming variant C2's counter does not
cover (C2 scans only `<wave>-results.json`); presence-only, no shape claim.

### (c) `tools/round-40/ledger-status.py` — same member fields as an input ledger

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-40/ledger-status.py:203-211`
reads `doc.get("results")` as a list of seat objects; `:144-161` uses `seat["name"]`
and `seat["output"]` (output scanned for report-path tokens); `:186-195` *writes*
`status`, `report`, `report_bytes`, `report_source`, `status_previous` onto the copy —
which under `mori-settlement-scan.py:78-84` would be `extra_keys` drift (like r53's
`report_file`). Confirms `extra member keys` is a real, cross-lane drift class.

### (d) `corpus/evidence/round-25/proposal/` — a different "settlement" artifact

`actual-seat-budget.json:13-14` `"registry": "swarm-registry.json"`,
`"terminal_settlement": "wave1-settlement.json"`; `distillation.md:184,196` —
`wave1-settlement.json` pins each seat's report bytes ("63/64 settlement pins match
their settlement pin byte-for-byte"; the P55 mismatch is the round's central defect).
That is a lane-authored pin-settlement record (kaidoku's own convention), NOT the
orchestrator `*-results.json` — related concept, different artifact.

### (e) `corpus/QUALITY.md` — settlement-adjacent process claims

`:57` (row 47) "A round is filed only after its last seat has settled, and
`tools/round-29/prefile-check.sh <LANE>` exits 0 … Whether a seat is still running is
not visible in the lane"; `:135` (row 76) "A round's record states seat totals,
settled seats and outstanding seats with timestamps in the same commit as any stop."
Same settlement-accounting requirement class as mori's QUALITY, different mechanism.

## mori-side boundary fact (recorded for context, not a sibling claim)

`mori-shokunin/corpus/SOURCES.md:329` row **S549** — mori itself opened kumitate's
`swarm-wave-lifecycle.md` (copy `corpus/evidence/sources-r57/kumitate-wave-lifecycle.md`)
and **rejected** it: "describes kumitate-owned result collection rather than mori's
log pairing parser; flip only if the claim becomes about settlement ownership."
The C2 claim direction ("orchestrator `*-results.json` settlement artifacts") is the
direction that row flags: kumitate owns the collect-side semantic contract; mori's
frozen scope is the file-as-recorded shape. The overlap is real but boundary-clear.

---

## Overlap summary

| Surface | kumitate | tsukuroi | kaidoku | C2 coverage status |
|---|---|---|---|---|
| `seats == len(results)` | `inline-dispatch-evidence.mjs:284` | — | — | duplicated assertion |
| `results[]` member `name`/`agent` | `:283-287` | `check-scrub-record-r42/43/44` | `ledger-status.py:203-211` | duplicated reading |
| member keyset exactly {name,agent,output,note} | — (name/agent only bound) | — (same + `output` first-line rule) | — | **unclaimed elsewhere** |
| `agent` ∈ closed 10-role set | `swarm-wave-lifecycle.md:62-65` (`SWARM_ROLES`, same 10 names) | implicit (per-seat role binding) | — | vocabulary claimed by kumitate; enum check unclaimed |
| `output` semantics | non-empty count (`round-65-verifier-spotcheck.md:20`) | `verdict_line`/`verdict` JSON + first-line fullmatch (r44 `:193-203`) | report-path tokens | mori only checks null/str/non-empty |
| extra member keys = drift (r53 `report_file`) | — | — | `ledger-status.py` *adds* keys on copies | **unclaimed elsewhere** |
| dead-seat settlement authority | QUALITY:993 "never from `results.json`" (transcripts) | adjacency ADJ-05 → mori | `settle-gate.py` (registry+settle.tsv, no results.json) | potential semantic clash flagged |
| results-file naming | `<wave>-results.json` | same | also `r<N>-<wave>-results.json` | C2 covers one variant |

## Remaining unknowns

- Whether kumitate's `dispatch-actual.json` (`members` array + non-null `agentId`,
  QUALITY :926) is the upstream replacement contract the round-60 `members`-dict
  registry violated — the two gate schemas disagree in committed kumitate docs.
- No sibling lane holds a claim about `.ufo/waves/round-58/evidence/w1-settlement.json`
  (schema `mori-wave-settlement-v1`, keys `{ignored_json, lane_root, schema, totals,
  unreadable_json, waves}`) — that artifact family appears mori-only.
- kaidoku rounds 25/40/41 use additional settlement-adjacent ledgers
  (`wave1-settlement.json`, `ledger-status` copies, `rN-<wave>-results.json` naming);
  their exact byte-shape contracts were surveyed at header level only.

## Method / evidence

- Read: `.ufo/waves/round-59/contract.md` (full), `count-c1.py`, `count-c2.py` (full),
  `tools/mori-settlement-scan.py:1-204` (working-tree copy).
- Grep sweeps: `results\.json|settlement|seat.*settle` over
  `kumitate-shokunin/corpus`, `tsukuroi-shokunin/corpus`, `kaidoku-shokunin/corpus`
  (78 files hit; all knowledge entries and the cited tools opened at the quoted lines).
- Shape verification: `python3 json.load` over mori r53–r58 `*-results.json` (r54–r58
  member keys `{agent,name,note,output}`; r53 w1 adds `report_file` → drift arm) and
  kumitate `round-65/w1-results.json` (identical schema).
- Scratch: `mkdir -p /fast/scratch/hyaku/mori-r59/Mo59Scout52` created, unused
  (all reads read-only), removed with `rmdir`. No fixture repos needed; no git writes.
- No tools installed (pacman paused host-wide; nothing needed beyond python3/grep).

Report written by seat Mo59Scout52; sibling lanes read-only, nothing mutated.
