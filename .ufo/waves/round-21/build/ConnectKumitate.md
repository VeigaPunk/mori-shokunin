# ConnectKumitate — round21 evidence-loss audit vs kumitate province

Seat: MoriR21.ConnectKumitate-4 (connector, leaf). Read-only. Detection/report only.
No production file edited, no tool installed, no census/pin/build/test run.

## Verdict

The proposed audit (`contract.md:13-16`) is read-only toward dispatch: it reads
`--required`, `--accounting` and hash-bound files beneath `--root`, emits stdout
JSON, makes no live writes, and its `pin_allowed` covers only mori's own census
`--pin`. It doesn't touch `ufo-swarm-*` registry, dispatch or results objects.
**There are no dispatch-mutation findings.**

Two wording collisions remain in the uncommitted round21 province prose, and
together they could let the audit be read as a lifecycle or acceptance ruling.

1. **Unqualified "acceptance".** `PROVINCE.md:170` (working tree) says mori
   "blocks acceptance". The same file already gives *result acceptance* to
   kumitate (`PROVINCE.md:150`, `:153`), and kumitate uses "Acceptance" for
   receipt binding (`../kumitate-shokunin/SKILL.md:125-126`). The contract's
   claim is narrower. It says "operationally blocking **baseline** acceptance"
   (`contract.md:7`), and QUALITY69 says "blocks baseline acceptance" in the
   working-tree `corpus/QUALITY.md` diff. The province line drops "baseline".
2. **The `disposition: settlement` enum value isn't qualified in the province.** The
   frozen contract (`3b792db:.ufo/waves/round-21/contract.md:14`) lets a
   `disposed` row carry `disposition settlement|cleanup-accounted`. In kumitate,
   settlement is the `ufo-swarm-results-v1` record (`../kumitate-shokunin/SKILL.md:45-48`;
   `../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:40-41`), and
   auto-reap is "settlement-licensed" (`../kumitate-shokunin/SKILL.md:174-177`).
   The province doesn't say that a mori `disposed`/`settlement` row only *cites*
   an independent record. As written, a reader could take it as mori's
   lifecycle settlement, or as a licence to reap or re-dispatch. The contract
   enum is frozen, so the fix has to be prose only.

## Evidence

| Point | Location |
|---|---|
| Mori refuses dispatch/orchestration | `PROVINCE.md:12` |
| Report-file `settled` ≠ kumitate lifecycle settlement or result acceptance | `PROVINCE.md:150-154` |
| Dispatch ledger is observation only; plan, retry and adjudication are kumitate's | `PROVINCE.md:134-138` |
| Round21 note: "blocks acceptance" (unqualified) | `PROVINCE.md:170` (uncommitted; `git diff HEAD -- PROVINCE.md` adds `:162-173`) |
| FR3 settlement and independent disposition stay frontier | `PROVINCE.md:168-171`; `PROVINCE.md:46` |
| Kumitate owns orchestration and refuses non-domain work | `../kumitate-shokunin/PROVINCE.md:3-6` |
| Kumitate settlement = `ufo-swarm-results-v1`, never a judge input | `../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:40-41,100-104` |
| Reap is settlement-licensed | `../kumitate-shokunin/SKILL.md:174-177` |
| Lifecycle display is "never artifact acceptance" | `../kumitate-shokunin/SKILL.md:462` |
| Audit interface (frozen) | `git -C …/mori-shokunin show 3b792db` (contract + frozen files); `contract.md:14-16` |
| Retained provenance has `independent_wave_disposition: null`, `settlement: unknown` | `.ufo/waves/round-21/evidence/historical-provenance.json:38-39` |
| Lesson rejects a forged `independent` boolean as authenticated authorship | `corpus/lessons/round-21.md:30` |
| Tool not yet present | `tools/mori-evidence-loss.py` absent at scan time (glob) |

## Contradiction (adjacent, report to kumitate; not absorbed)

`../kumitate-shokunin/SKILL.md:45-48` documents a `settle --registry [--results]`
verb. `../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:37-44`
(round-32 errata) says live `main` admits only `plan`/`run`/`record`, and that
settlement is operator-supplied. Mori doesn't need to resolve which one is
right, because the fix below doesn't name a producer verb. It's left as an
unknown in kumitate's domain.

## Affected axes

- C1 freshness: improves. A `disposed` row can no longer be read as mori's
  settlement, and the pin blocker is scoped to mori's own baseline.
- C2 calibration: neutral to slightly better. "Baseline acceptance" now matches
  QUALITY69's wording.
- Coverage: unchanged. No capability is added or removed, and the frozen
  contract, cases and rules are untouched.

## Proposed move (smallest precise wording fix)

Edit the uncommitted round21 section of `PROVINCE.md` in place. It isn't
committed yet, so this isn't a history rewrite. Change one phrase and add one
sentence.

Replace `PROVINCE.md:170`:

```
mori retains the unknown identities and provenance and blocks acceptance,
```

with:

```
mori retains the unknown identities and provenance and blocks acceptance of
its own census baseline (pin),
```

Then insert this before `The existing bounded report-presence capability remains distinct.` (`:172`):

```
An audit `disposed` row only cites a hash-bound independent record; it is not
mori's lifecycle settlement, result acceptance, or a reap/re-dispatch licence
(kumitate-owned).
```

If L1 has already committed the section, append the same two clauses as a
dated round21 erratum line under it instead. Don't edit committed bytes.

## Risks

- Saying "cites" rather than "proves" is deliberate: the `independent` flag is
  self-asserted (`corpus/lessons/round-21.md:30`). Strengthening it would
  overclaim.
- Naming `ufo-swarm-results-v1` as the example producer would take a side in
  the kumitate `settle` contradiction. The proposed text names no schema or verb.
- Second-order effect: if ImplLoss's `--selftest` writes fixtures shaped like
  `ufo-swarm-wave-dispatch-v1` under `.ufo/waves/`, mori's own
  `mori-wave-settlement.py scan` (`PROVINCE.md:146`) and kumitate tooling would
  pick them up. The contract requires isolated fixtures with no live writes
  (`contract.md:16`), and this has to hold in the implementation.

## Verification (for L1, after the tool lands)

1. Read-only check that the tool doesn't touch orchestration objects or write
   outside the temp dir:
   `rg -n "ufo-swarm|swarm-registry|swarm-dispatch|wave-slot" tools/mori-evidence-loss.py`
   should return nothing. Also check with
   `rg -n "open\(.*['\"]w|write_text|write_bytes|os\.replace|shutil" tools/mori-evidence-loss.py`
   that every match is under a `tempfile` selftest root.
2. Vocabulary check: `rg -n "accept|settled|lifecycle" tools/mori-evidence-loss.py`.
   Output keys should be limited to the contract set
   (`omitted,retained,unresolved,disposed,invalid,pin_allowed,issues`).
3. Province check: after the edit,
   `rg -n "blocks acceptance" PROVINCE.md` should match only text qualified by
   "census baseline (pin)".

## Unknowns

- Who authored the uncommitted round21 `PROVINCE.md` section, and whether L1
  treats it as frozen. Not determinable read-only without journals or sessions,
  which are out of bounds.
- Implementation details of the final audit, such as fixture location and
  output keys. The tool was absent at scan time.
