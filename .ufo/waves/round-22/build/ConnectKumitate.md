# ConnectKumitate — round22 retention reconciliation vs kumitate province

Seat: MoriR22.ConnectKumitate (connector, leaf). Read-only; detection/report only.
No production or sibling file edited, no tool installed or updated, and no
build, test, census, pin or scan run. Lane HEAD at read time:
`306e06ecd02e0ea8e544fbd30d1ff7e7359c581e`.

## Verdict

The proposed `tools/mori-retention-reconcile.py` (`contract.md:11-15`) has
**no dispatch authority and no settlement or authentication overlap** with
kumitate. It reads three Git blobs at an explicit revision of mori's own
repository, writes only stdout and its exit code, and references none of
kumitate's objects (`ufo-swarm-*` registry/dispatch/results,
`ufo-task-receipt-v1`, the queue, or reap). Kumitate's `*.{mjs,js,sh,py,json}`
files contain zero matches for `mori`, `retention-reconcile` or `mori-r2`, so
nothing on the kumitate side consumes mori exit codes or output.

The real overlap is **vocabulary**. The words `receipt`, `reconcile` and
`retention` all name kumitate-owned lifecycle objects with authority attached.
None of them is mechanically connected to mori's tool, but the matching names
could let `RETENTION_RECONCILED` or `receipt_match=true` be read as a kumitate
receipt verdict, a settlement, or an authentication claim. The fix is one
prose boundary plus an output-vocabulary constraint (see Proposed move).

## Overlap and non-overlap

| Term or surface | Mori round22 meaning | Kumitate meaning (owner) | Overlap? |
|---|---|---|---|
| receipt (input) | `mori-r21-command-receipt-v1` command wrapper (`contract.md:11`; schema at `.ufo/waves/round-21/evidence/final/retention-floor.json:2-3`) | `ufo-task-receipt-v1` gate on `complete` (`../kumitate-shokunin/SKILL.md:94-95`); `iteration.decision:"continue"` mints successors (`SKILL.md:114-115`) | Name only. The consumers are keyed by schema, and the schemas differ. |
| receipt (tool output) | Provenance (input/tool SHA-256, commits, argv) "appear in receipt" (`contract.md:11`) | Acceptance writes `receipt_snapshot_binding_accepted` (`SKILL.md:125-129`) | Name only. This is a third use of "receipt", and its output schema tag is unspecified (see Risks). |
| reconcile | Exit 0 `RETENTION_RECONCILED` = exact accounting agreement, even when `retention_state=red` (`contract.md:15`) | `ufo-sighting reconcile` verb; `reconcileQueue` arms (`SKILL.md:67,168-173`) | Name only. Mori's is an accounting comparison with no queue or mission effect. |
| settlement | None. The tool reads no `.ufo/waves` dispatch, registry or results objects. | `ufo-swarm-results-v1` operator-supplied settlement (`corpus/knowledge/swarm-wave-lifecycle.md:37-44`); auto-reap is "settlement-licensed", needing a "receipt verdict admitted" (`SKILL.md:174-177`) | **None** structurally. The risk is a reader treating `receipt_match=true` as an "admitted receipt verdict" and so as a licence to reap or continue. |
| authentication | Hashes are provenance. "a source hash is not secrecy/authentication"; "no source authenticates private-data absence" (`contract.md:23`; `PROVINCE.md:130-131`, `:179-181`) | `charter sign <runId>` membrane unseal; `membrane-seal` single writer of record (`SKILL.md:309-312`) | **None.** Mori asserts no identity, authorship or seal. |
| dispatch | None. The `--selftest` arms are local subprocesses on isolated fixtures (`contract.md:11,27`). | Plan/run/record wave CLI, one `task` call per wave (`swarm-wave-lifecycle.md:47-53`) | **None.** No `task`, `agent://`, `wave-slot` or registry write. |
| retention | Private-data line retention over mori's own committed evidence (`PROVINCE.md:126-131`) | Upstream `scripts/ufo-state-retention.mjs` `cap`/`sweep` of runtime state (`corpus/knowledge/remaining-scripts-census.md:706-708`) | Name only. A `retention_state=red` has no path to a sweep. |
| exit codes | 0/1/2 = reconciled, mismatch, setup (`contract.md:15`) | `ufo` CLI 2 = typed refusal; JS scripts 1 typed / 64 usage (`SKILL.md:313-314,463-465`) | No consumer crosses the two (zero kumitate references). |
| mori's own settlement scanner | — | — | Second-order risk: `tools/mori-wave-settlement.py` walks every `*.json` under `.ufo/waves/` (`:105-130`) and selects by `DISPATCH_SCHEMA = "ufo-swarm-wave-dispatch-v1"` (`:34`). Round22 evidence is counted only if it carries that schema. |

Province basis: mori refuses dispatch/orchestration (`PROVINCE.md:12`). Its
report-file `settled` is not kumitate lifecycle settlement or result acceptance
(`PROVINCE.md:150-154`), and "blocks acceptance" means mori's census baseline
only, with a `disposed` row being no reap or re-dispatch licence
(`PROVINCE.md:174-181`). Kumitate owns orchestration and refuses non-domain
work (`../kumitate-shokunin/PROVINCE.md:3-6`).

## Contradiction (kumitate domain, carried forward, not absorbed)

`../kumitate-shokunin/SKILL.md:45-48` still documents a `settle` verb, and
`SKILL.md:60-62` still documents a `stale_dispatch_pair` refusal. The round-32
errata in `corpus/knowledge/swarm-wave-lifecycle.md:37-44` say live `main`
admits only `plan`/`run`/`record` and has no `stale_dispatch_pair` token. This
is unchanged since round21's connector. Mori's move names no producer verb, so
it doesn't take a side.

## Affected axes (held scores from `contract.md:5`)

- **adjacency (6): improves.** It closes the one remaining confusable surface
  for the new tool, the receipt/reconcile names, without moving ownership.
- **calibration (5, the C1 target): neutral to slightly better.** It keeps
  "agreement ≠ clearance ≠ authentication ≠ settlement" explicit, as the root
  lesson at `contract.md:23` requires.
- **coverage, operability, depth, freshness: unchanged.** No requirement ID
  (R01–R24), frozen value, CLI flag, exit code or required field changes. A
  schema tag on the output is outside the frozen field list, and unknown fields
  are already tolerated (`contract.md:13`).

## Proposed move (one bounded proposal for L1)

1. **Output vocabulary constraint for the implementation, compatible with the
   contract.** If the tool's output carries a `schema` tag, it uses a
   `mori-`-prefixed value, never `ufo-*`. Its emitted JSON keys exclude
   kumitate's authority words: `iteration`, `decision`, `verdict`, `accepted`,
   `settle`/`settled`/`settlement`, `reap`, `dispatch`, `agentId`. The
   contract's own keys (`receipt_match`, `retention_state`, …) are unaffected.
2. **Append a round22 province note** (append-only, below the round21 notes;
   committed bytes untouched):

   > Round22 retention reconciliation (`tools/mori-retention-reconcile.py`)
   > compares one mori command receipt with an independent recomputation over
   > mori's own committed tree. `RETENTION_RECONCILED`/`receipt_match` mean
   > accounting agreement only: not privacy clearance, not authentication of
   > authorship or absence, and not a kumitate receipt verdict, settlement,
   > reap, continue or re-dispatch licence (kumitate-owned).

## Risks

- **Unseen implementation.** `.scratch/round22` didn't exist at read time, so
  the executors' drafts couldn't be inspected and the constraint in item 1 is
  forward-looking. If ImplReconcile already emits a `ufo-*` tag or a listed key,
  L1 renames it before integration. No sibling was messaged, because no
  violation was observed.
- **Over-tight key ban.** Banning `decision` could collide with a future mori
  field. The ban applies only to this tool's emitted JSON, not to prose or to
  receipt `stdout` bytes, which stay an opaque string.
- **Fixture placement.** If the committed fixture generator (`contract.md:19`)
  ever materializes a `ufo-swarm-wave-dispatch-v1` JSON under `.ufo/waves/`,
  mori's settlement scan and kumitate tooling would count it. Fixtures belong
  under `.scratch/round22` or an isolated temp root (`contract.md:27`).
- **Wording.** "Accounting agreement" is deliberately weaker than "verified".
  The existing round21 rule stands: hashes are provenance, never authentication
  (`PROVINCE.md:179-181`).

## Falsifiable no-axis-harm check (for L1 after integration; not run here)

Let `B` = the entering base `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0` and
`X` = L1's integration commit. Let `E` = every JSON file the integrated tool
emitted into `.ufo/waves/round-22/evidence/`. The claim "no dispatch,
settlement or authentication harm" is **falsified** if any of these fails:

```sh
R=/home/vgpnk/Projects/shokunin/mori-shokunin
B=77a5bbe8a0b41dfbfd2546d024d36e294b814bd0; X=<integration-commit>
# (a) no write outside mori's own lane surfaces
git -C "$R" diff --name-only "$B" "$X" | rg -v '^(tools/mori-retention-reconcile\.py|\.ufo/waves/round-22/|corpus/|PROVINCE\.md$|SKILL\.md$|SCORECARD\.md$|LOG\.md$)'
#   expect: no output
# (b) emitted evidence carries no kumitate schema, authority key, or clearance
for f in $E; do
  jq -e '[.. | objects | keys[] | select(test("^(iteration|decision|verdict|accepted|settled?|settlement|reap|dispatch|agentId)$"))] | length == 0' "$f" &&
  jq -e '[.. | objects | .schema? // empty | strings | select(startswith("ufo-"))] | length == 0' "$f" &&
  jq -e '[.. | objects | select(has("privacy_clearance")) | .privacy_clearance] | all(. == false)' "$f" || echo "FAIL $f"
done
#   expect: no FAIL lines
```

Pass condition: (a) prints nothing, and (b) prints no `FAIL`. On this host,
`jq` resolves to jaq 3.1.1. The filters use only `..`, `objects`, `keys`,
`test`, `startswith`, `has` and `all`, but jaq compatibility of this exact
filter has not been run. One positive line falsifies "harms none" for the
adjacency axis. This check doesn't replace R02/R23. A zero result is not
privacy clearance.

## Tool installs

None.
