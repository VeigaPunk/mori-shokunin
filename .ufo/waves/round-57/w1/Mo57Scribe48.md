# Mo57Scribe48 — no-harm and kumitate-boundary review (round 57, C1 calibration / C2 depth)

Seat: scribe, leaf (no dispatch). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`,
frozen at `618562c72a03dc4d17386b715357f863fd327274` (freeze). Entering tip
`53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`. No production edit, commit, jj mutation, host
remediation, secret, or tool install was made. Scratch: `/fast/scratch/hyaku/mori-r57/Mo57Scribe48`
(removed at yield; fixture texts are reproduced below so each measurement is reconstructable).

Scope of this seat, exactly: do the proposed C1/C2 interpretations stay **detection/report only**, and
do they avoid claiming **authoritative settlement semantics owned by kumitate**? Attack the frozen
predicates as written; they were not changed, broadened or re-designed here.

## Verdict

| Question | Verdict | Basis |
|---|---|---|
| Is the frozen C1 claim detection/report only and free of settlement semantics? | **Yes at contract level; not enforced by its counter.** | contract `.ufo/waves/round-57/contract.md:5,7`; counter `count-c1.py:10-13`; measured fixture below prints `C1=met` on a row claiming dead-lane/unhealthy verdicts and on a row claiming "settles the wave's votes … accepted by kumitate". |
| Is C1 free of self-assessment (calibration) harm? | **No, as the counter directs it.** Putting the two rows where the frozen counter can see them lands them in the table `SCORECARD.md:1958-1960` declares superseded, and leaves the current register without the two capabilities. Measured below: register landing = frozen counter unmet *and* round-35 register gate `extra=2`; a reconciled landing keeps both instruments green (measured). |
| Is the frozen C2 claim boundary-preserving? | **Yes — the predicate states the correct direction** (`unclosed` is a pairing count, not a present-running count, `contract.md:7`), matching `tools/mori-driver-liveness.py:34-36`. |
| Does the C2 counter enforce that direction? | **No.** It is a substring test: an entry asserting the exact opposite — "`unclosed` is a present-running count of live processes" — prints `C2=met claims=8 source=ok quotes=ok`, rc 0 (measured). |
| Does either claim infer provider death or settlement from the field? | **No** in the contract and in the w1 reports I inspected (six in full, the rest by grep); the risk is that neither counter would catch it if an entry or row did. |

So: **the claims as frozen are boundary-safe; the gates are not boundary-enforcing.** All honourable
parties to this wave have kept the boundary; the closure must keep doing so by reading prose, because
the frozen counters cannot.

## Boundary frame (authoritative local statements, not my invention)

- `SKILL.md:9` — "Domain: observing whether the fleet and its host are ALIVE and progressing — and
  reporting it. **Detection and report only. This lane never remediates.**"
- `SKILL.md:16` — intent "Did a wave settle?"; `Never` cell: "assuming an unsettled wave is a failed one".
- `corpus/README.md:343` (FR3) — "Mori reports filesystem shape; kumitate owns orchestration/result
  semantics; `empty` alone does not prove never-written".
- `corpus/knowledge/wave-settlement-r20.md:36` — `| every member present | wave settled | that the wave's
  results are accepted (kumitate owns result semantics) |`; `:33` — a `missing` member is
  "**dead, failed or killed**" never to be concluded.
- `/home/vgpnk/Projects/shokunin/MINT.md:27` — "**Domain boundary:** observe and report only. Refuses
  dispatch (kumitate) and OS-package state (tsukuroi). Never remediates."
- `/home/vgpnk/Projects/shokunin/AXES.md` §Capabilities (`:55-64`) — "Rows enter only through a round
  that demonstrates the capability running; a capability without a passing demonstration in the round
  report is pre-claiming and does not enter the table."
- `.ufo/waves/round-57/contract.md:9` — "Vote output is not itself independent verification."
- `corpus/knowledge/driver-liveness-r56.md:62-63` — "`in_flight`/`unclosed` are pairing facts over log
  lines, not health verdicts; a lane with an unclosed launch is *in flight by the log*, not \"stuck\"";
  `:66-68` — the log is "driver-authored shape, not authenticated events".
- `corpus/knowledge/vote-binding-r56.md:67-69` — "A unanimous-but-wrong vote set would still read
  `dissent=0` (the tally counts inter-voter disagreement only) — a named limit, not a quorum guarantee."

## C1 — what the frozen counter actually measures

### C1-a. The register collision (measured, this seat)

`SCORECARD.md` carries two level-2 `## Capabilities` sections:

- `:596` — the placeholder table, row `| — none yet — | | | |` at `:600`, followed at `:604` by
  "Rows enter only through a round that demonstrates the capability running (`AXES.md`
  §Capabilities); **none enter through this rollout**."
- `:1951` — the current register ("Round 35 (claim C1, calibration). This is the lane's current
  capabilities register, the `capabilities` field of the AXES.md SCORECARD contract"), whose paragraph at
  `:1958-1960` says: "As the current self-assessment this register **supersedes** the `— none yet —`
  table in the first `## Capabilities` section (left as filed at `d677cf3`)".

The frozen predicate itself says "the **current** SCORECARD capabilities table" (`contract.md:5`); the
table the counter reads is the one `SCORECARD.md:1958-1960` calls superseded, and the table the lane
calls current (`:1951`) is invisible to it. That is a predicate/counter divergence, not a wording quibble:
the two live instruments disagree about which table is the register.

The frozen round-57 counter reads only the first: `count-c1.py:10`
`s = p.stdout.split("## Capabilities", 1)[1].split("## Saturation", 1)[0]`.
The lane's register instrument reads only the last: `.ufo/waves/round-35/count-c1.py:71` `s = cap[-1]`,
with oracle pinned to `MANIFEST_REV = "37b51a243302e8009c7067431e8a47f9a722fd14"` (`:31`) and an
`extra == 0` arm (`:194`; `extra` collected at `:115`).

Baseline, register gate at the freeze revision (read-only, executed):

```
$ python3 .ufo/waves/round-35/count-c1.py 618562c72a03dc4d17386b715357f863fd327274
...
label=P-C1 rev=618562c72a03dc4d17386b715357f863fd327274 manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
rc=0
```

The content is manifest-supported: fleet `MANIFEST.json` already records
`rounds[832]` = mori 56 **admitted** with exactly two `capabilities_added` entries (vote binding; strict
per-event driver-liveness probe) — but the round-35 gate is pinned to the round-34 closure manifest, so
its oracle is 18 rows and cannot include them.

Measured in a `git clone --shared` of the lane under scratch (`git rev-parse --show-toplevel` printed the
clone path; no mutation of the lane):

| Landing | round-57 `count-c1.py` (repo→clone) | round-35 `count-c1.py <rev> --repo <clone>` |
|---|---|---|
| two rows appended to the **register** (`... extra=2`), rev `ab2899a6a26a459c00f044ea3dc3a9933449d79c` | `C1=unmet rows=0 evidence=bad`, rc 1 | `oracle=18 rows=20 matched=18 missing=0 bad=0 extra=2 mismatches=2 C1=unmet`, rc 1 |
| two rows in the **first table** + a prose (non-row) reconciliation note in the register, rev `f9d4e93c0c2939c76981444e4059a7458c99ea3e` | `C1=met rows=2 evidence=ok`, rc 0 | `oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met`, rc 0 |

Consequence: an implementer who follows `SCORECARD.md:1958-1960` is scored unmet by the frozen counter;
an implementer who follows the frozen counter leaves the current register silent about the two
capabilities and makes `:604` ("none enter through this rollout") false. Both outcomes are a
self-assessment contradiction — a calibration harm — even though the counter prints `met`.

Smallest reconciliation that measured green on both instruments (recommendation, not applied):
1. Enter the two rows in the first table with the bounded wording in §C1-c.
2. Append (never rewrite, `:604` is history) one sentence under it recording that round 57 entered the
   two rows and naming their demonstrations.
3. Append a prose note inside the register naming `rounds[832].capabilities_added[0..1]` and the pinned
   `MANIFEST_REV 37b51a24`, stating that they cannot be register rows without re-pinning. Prose is
   ignored by `register_rows()` (`.ufo/waves/round-35/count-c1.py:65-85` parses `|` rows only), which is
   why the second row of the table above stays `extra=0`.

### C1-b. The frozen C1 counter cannot enforce this seat's boundary (measured fixtures)

A fixture repo under scratch (two commits), the frozen counter copied and only the `repo=` constant
repointed (`git rev-parse --show-toplevel` asserted inside the repo before each commit):

1. **Health verdicts + settlement semantics + a non-existent pointer.** `SCORECARD.md`:

```
## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| driver-liveness | detects dead lanes and reports them unhealthy and wedged | `.ufo/waves/round-56/evidence/does-not-exist.md` | 56 |
| vote-binding | settles the wave's votes authoritatively and marks results accepted by kumitate | `.ufo/waves/round-56/evidence/c1-at-landed.txt` | 56 |
```

   `$ python3 c1.py <rev>` → `C1=met rows=2 evidence=ok`, rc 0. The path does not exist; "unhealthy",
   "wedged" are exactly the words the round-56 arm bans in the tool (`.ufo/waves/round-56/count-c1.py:45`
   `HEALTH_WORDS = ("healthy", "unhealthy", "failed lane", "is stuck", "wedged")`); and the second row
   assigns settlement to kumitate. The round-57 counter carries no such arm.

2. **The pointer column need not hold a pointer.** Rows whose Evidence-pointer cells are `—` and `TBD`,
   with the token `.ufo/waves/round-56/…` placed in the "what it can do" text instead:
   `C1=met rows=2 evidence=ok`, rc 0. `count-c1.py:12` tests substrings anywhere in the row:
   `all(".ufo/waves/round-56/" in x and "| 56 |" in x for x in rows)` — no column binding, no resolution.

The frozen predicate (`contract.md:5`) says "each with a **resolvable** round-56 evidence pointer"; the
counter proves neither resolvability nor column placement. Closure must resolve both pointers by hand
(both named files do resolve at `618562c7`: `.ufo/waves/round-56/evidence/c1-at-landed.txt`,
`…/c2-at-landed.txt`, checked with `git cat-file -e`).

### C1-c. Safe wording for the two rows (derived from the demonstrated scope)

Permitted, each clause traceable to the round-56 artifact:
- driver-liveness: "reads `.ufo/watchdog.log` launch/complete/dead/wrap/fail lines as per-lane pairing
  facts (`in_flight`, `unclosed`, malformed and `other_lines` counts)"; grounded in the tool docstring
  (`tools/mori-driver-liveness.py:1-40`) and the 13/13 selftest. It may **not** say the probe detects
  dead lanes, establishes daemon identity, or closes FR5 — `corpus/README.md:345` keeps pid-identity and
  degraded-pgrep open, and `corpus/knowledge/driver-liveness-r56.md:69-75` names the unrecognized
  `lane-round-failed` class as a grammar-coverage gap.
- vote-binding: "binds `RECHECK`/`ENTAIL` vote lines from both plain-text and JSON-wrapped seat outputs
  over its own committed ledgers"; 16/16 selftest. It may **not** say it settles, admits, verifies or
  gives quorum: `vote-binding-r56.md:67-69` and `contract.md:9` both forbid that reading.

Both rows should carry `| 56 |` and a pointer in the *Evidence pointer* column that resolves at the
measured revision (e.g. the at-landed receipt plus the tool). This is bounded wording, not new scope.

## C2 — what the frozen counter measures, and what the eight statements may say

### C2-a. The `pairing count` arm is direction-blind (measured)

Fixture entry (scratch repo, `corpus/SOURCES.md` holding `| S548 | … | queued |` and one unrelated
`| S1 | … | mined |` row):

```
| id | claim | quote |
|---|---|---|
| K1 | ten tasks are running because of the count | `launch` |
… K2–K8 identical …
`unclosed` is a present-running count of live processes; the phrase "pairing count" is wrong here.
cites S548.
```

`$ python3 c2.py <rev>` → `C2=met claims=8 source=ok quotes=ok`, rc 0. The entry asserts the **negation**
of the frozen predicate and still passes, because `count-c2.py:15` only asks `"pairing count" in entry`.

A second fixture added settlement semantics and still passed: "An `unclosed` pairing means the seat's
work has not settled; the wave is unsettled and its results are not accepted." → `C2=met`. That
sentence is exactly the kumitate-owned claim `wave-settlement-r20.md:36` and `README.md:343` reserve.

### C2-b. Every other C2 arm is structural (measured)

Same fixture repo, one mutation per run:

| Mutation | Frozen counter output |
|---|---|
| no `source:` / `verified-at:` / `recheck:` opening (contract `:7` requires them; only a trailing `source: S548` line present) | `C2=met claims=8 source=ok quotes=ok` |
| S548 row status `queued`; `mined` supplied by an unrelated row | `source=ok` (`count-c2.py:13` tests `"mined" in registry` over the **whole** file) |
| eight identical claim rows | `claims=8` (no distinctness arm) |
| seven real claims + a backticked header row `| Key | claim | \`quote\` |` | `claims=8` (`startswith("| K")` counts the header) |
| no source copy at all (no `corpus/evidence/sources-r57/` exists; registry ends at S547) | `quotes=ok` (`count-c2.py:14` is `all("`" in x and "`" in x …)` — the same predicate twice, so one backtick per row suffices) |

So `C2=met` can certify a file whose row grammar is right and whose content is wrong in every one of the
five ways the frozen predicate names. Closure must read the entry; the counter is a shape fence only.

### C2-c. What the eight statements may and may not say (grounded)

The frozen direction is correct and is supported; these are the exact semantics a claim may rest on
(verified in this seat, not copied from a peer):

- `unclosed` is `len(row["open_launches"])` — `tools/mori-driver-liveness.py:173`; docstring
  `:34-36` "launches with no same-(lane,round,attempt) complete — a pairing count, not a failure claim".
- A launch appends `(round, attempt|None)` (`:114,128,133`); a `complete` sets the key to
  `(round, attempt)` only when the line carries `attempt=` (`:139-143`), and `close_round()` removes
  that key, else the untagged `(round,None)` key (`:116-120`); `wrap` closes only `(round,None)` (`:144-150`).
- `lane-dead-no-report` clears **every** open key of that round (`:151-157`), so the count is not
  `launches − closes`; `launch-fail` is counted but closes nothing (`:158-162`).
- `in_flight` is a *different* field: last parsed event was a launch (`:172`).
- Counterexamples to "running now", measured on the committed receipt
  `.ufo/waves/round-56/evidence/driver-liveness-live.txt` (JSON doc, prose appended after it):
  `mori` `unclosed=10, in_flight=true` (`:195-205`) while `kagi` has `unclosed=10, in_flight=false`
  (`:63-74`); recomputing myself, **9 of 23** lanes have nonzero `unclosed` with `in_flight=false`,
  the residue identity `launches−completes−deads−wraps` holds on only **6 of 23** lanes, `kumitate`
  reads `unclosed=3` against an identity of `−4`, and `Σ unclosed = 124`.
- The count is **not monotone**: `kake` moved `13 → 12` when a later
  `complete kake round=63; hyaku-inline attempt=1` line landed
  (`.ufo/waves/round-56/w1/Mo56ExecDriverFixtures.md:358-380`), and the receipt's `1728` log lines
  re-derive as `1730` today. Do **not** copy `Mo56ExecDriverLive.md:93`'s phrase "monotone
  historical backlog counter" (repeated as finding heading `:504`); it is contradicted by the same
  wave's §8.
- `(round, attempt)` pairing is **asymmetric**, measured on two scratch fixtures with the committed tool
  (`--fixture`, one lane `mori`, round 5): `launch round=5 attempt=1` followed by a bare
  `complete round=5; respawning` leaves `unclosed=1` (a bare close cannot close a tagged launch), while an
  untagged `launch round=5` followed by `complete …; hyaku-inline attempt=1` leaves `unclosed=0` — the
  `elif` at `:119-120` closes the untagged `(round,None)` open when the tagged key is absent. `wrap`
  always uses the `(round,None)` key (`:114`, `:144-150`), so it closes untagged opens only.

Forbidden in any of the eight rows (each crosses a named boundary):
1. "N tasks/processes are running now" / "the lane is alive/dead/stuck/wedged/failed" —
   `driver-liveness-r56.md:62-63`, `.ufo/waves/round-56/count-c1.py:45` word list.
2. "the wave is unsettled / did not settle / results not accepted / verdict outstanding" —
   `wave-settlement-r20.md:36`, `README.md:343`, `SKILL.md:16`.
3. "a missing report or an unclosed launch proves death" — `wave-settlement-r20.md:33`,
   `SKILL.md:9`, and this wave's guard "never … infer provider death from missing reports".
4. "`unclosed=0` proves the round completed" — `:151-157` (a `dead` clears opens) and
   `driver-liveness-r56.md:69-75` (unrecognized closers).

Grounding note, offered as closure practice and **not** a predicate change: one located quote per claim
is what the frozen predicate requires, but a grammar extract can only entail *line-shape* claims. The
pairing/limit claims are entailed by the implementation lines above plus the receipts; if all eight
quotes come from the S548 grammar copy, the interpretive half is only half-grounded. Closure should read
each row's quote against the sentence it supports, and should check the S548 **row** cells
(`| S548 |` present, status `mined`, `used-by` naming the entry, `opened` 2026-10-27) rather than the
counter's file-global `mined` token. `corpus/SOURCES.md` currently ends at S547 and
`corpus/evidence/sources-r57/` does not exist, so C2 is honestly `unmet` until the L1 opens that row and
copy — consistent with `.ufo/waves/round-57/controls.txt:5-7`.

## No-harm ledger

| Axis | Effect of what this seat observed | Note |
|---|---|---|
| coverage | none | C2 is documentation of an existing field; no new surface claimed. |
| operability | none | no tool, gate or counter was changed; all probes read-only. |
| depth | intended improvement, unenforced by the gate | eight rows may overclaim; see §C2-c. |
| freshness | none | no re-pin; `count-c1.py`/`count-c2.py` bytes untouched. |
| calibration | **at risk as the counter directs C1** | two-table contradiction measured (§C1-a); mitigated by the reconciled landing, measured green on both instruments. |
| adjacency | none | no settlement/result semantics were taken; the boundary statements above keep them with kumitate. |

## Verification gaps

- My fixtures are first-run observations under scratch and were removed at yield; the report reproduces
  their content verbatim, not a durable revision proof (the round-54 limit).
- I did not re-verify the fleet `MANIFEST.json` entry's own correctness; I read `rounds[832]` and its two
  `capabilities_added` strings, and used them only to explain why the register oracle is 18 rows.
- The live receipt is a point-in-time capture; my identity and `in_flight` counts are recomputations of
  that committed JSON, not a fresh live read.
- The round-35 gate pins `MANIFEST_REV 37b51a24`; whether a later round should re-pin it is a lane
  decision outside this seat.
- I did not run the candidate C1 rows against any other live instrument (e.g. round-41 calibration), and
  I made no attempt to satisfy, weaken or re-score the frozen predicates.

Report: .ufo/waves/round-57/w1/Mo57Scribe48.md
