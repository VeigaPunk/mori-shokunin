# Mo80Cn01Siblings — sibling-overlap scan for mori round 80 w1 (read-only)

Seat: connector, leaf, no subagent dispatch. Scan question: does another lane already hold the
ground of mori r80's C1/C2/C3, and is any of this round's work a duplicate? All evidence below
is text I read at the current work tree on 2026-11-04; I executed no sibling tool and no mori
counter (verdicts are file:line evidence, not re-measurement). No temp tree was created; nothing
to delete. No tool installs.

## What I did (numbered)

1. Read the frozen contract, do-nothing controls, mori PROVINCE.md:1-20, QUALITY criteria 90/154/
   159/161-164, SKILL.md gate registry (~:1340-1395) and the SCORECARD structure (`## Axes` :6,
   capabilities tables, rounds at EOF).
2. Grepped every lane's `tools/` and `scripts/` for `claim|self-assessment|resolve|pointer`
   (C1), and for `mutant|mutation|survivor` (C2); grepped every lane PROVINCE.md for `tools/`
   (C3); swept the fleet root `scripts/` (incl. `scripts/hyaku/`) for both patterns.
3. Read the nearest hits' headers/bodies: chousa claims-audit[-v2].py, chousa lane-preflight.py,
   kumitate claims-check.mjs / gate-mutants.mjs / counter-pins.mjs, kaidoku round-25
   a2/c1-calibration.py and round-26/30/31/34 mutant harnesses, kake freshness-sweep.mjs and
   citation_lint.py, kama gate-registry-check.py, tameshi mutate-and-run.sh (header + SKILL
   method/service/ledger sections), mado PROVINCE.md round-23 inventory, mori pin-check.py.
4. Checked boundary per claim against mori PROVINCE.md:1-20, and named cross-lane artifacts
   mori's edits could touch.

## Claim verdicts with evidence

### C1 (self-assessment claim sweep) — ADJACENT, not duplicate

Nearest three instruments (each scoped to its own lane; none implements mori's pins-file arms
over mori's carriers):

1. `chousa-shokunin/tools/claims-audit-v2.py:2-5` — "flags self-assessment statements in a
   frozen claims file that committed files contradict"; TSV rule file (anchor + check class),
   `--root`, `FLAG <id> <rule> <detail>` + `FLAGGED=<k>/<n> AUDIT=PASS|FAIL` (:24-31). Classes:
   section-contains[-at], git-first-commit, file-kind, verbatim-heading, lane-wide-sweep.
   Same concept (declared claims vs committed bytes), different mechanism: rule rows authored
   per statement vs mori's graded-row walk (Axes + capabilities + SHONEN) with
   unresolved-pointer, live-selftest-tally and stale-literal arms.
2. `kumitate-shokunin/scripts/claims-check.mjs:2-10` — "the member-claims gate": resolves each
   SCORECARD surface-registry row's `yes — <note>` claim into the note's member sections and
   fails on named shapes (`SECTION_FILE_UNRESOLVED`, `MEMBER_COUNT_DRIFT`, …). Resolves
   declared claims against committed bytes, but only kumitate's 19-row surface registry and its
   own corpus/scripts; no tally or stale-literal arm.
3. `kaidoku-shokunin/tools/round-25/a2/c1-calibration.py:2-6` — "count self-assessment
   mismatches at one revision … five fixed items, each comparing a lane self-assessment
   statement (SCORECARD, LOG, SHONEN, QUALITY) with observed repository state … reads only Git
   blobs at --rev". Same carriers as mori (SCORECARD/LOG/SHONEN/QUALITY), but five hard-coded
   kaidoku items, no pins file, no child selftest execution.

Adjacent in-lane precedent worth naming to the scribe: `tools/mori-pin-check.py:2-6` ("re-measure
the self-test pins of SKILL.md's gate registry", v3 r48) is the tally/digest-pin ancestor of C1's
tally arm, and `chousa-shokunin/tools/lane-preflight.py:19-22` (G04 shonen-pointers, G05
scorecard-paths: "every corpus/ tools/ .ufo/ path in the evidence cell of a SCORECARD
capabilities table row exists under ROOT") is the unresolved-arm ancestor; kama's
`tools/gate-registry-check.py:44-52` grades registry rows for meaning incl. cited-path
existence (`kama-shokunin/PROVINCE.md:152-155`). kake's `scripts/freshness-sweep.mjs:3-13`
("one command re-executes every quantified standing claim the lane makes"; §paths resolves cited
FS paths vs the live FS) is the same genre again. Duplicate? No — every one is single-lane
scoped; a fleet-wide glob for `*claim-sweep*` returns only mori's own in-flight
`mori-shokunin/tools/mori-claim-sweep.py` (work tree, see "Work-tree note").

### C2 (mutation adequacy of a selftest) — ADJACENT, not duplicate

The fleet-wide pattern is owned ground, explicitly routed: `kengaku-shokunin/PROVINCE.md:304-306`
— "mutation testing of a lane's own gate is a fleet-wide pattern, not kengaku ground — tameshi's
`tools/mutate-and-run.sh` and kumitate's `gate-mutants.mjs` are the precedents".

- `tameshi-shokunin/tools/mutate-and-run.sh:1-40` — the fleet's generic runner ("inject→run→
  restore with byte-identity proof"; "the target is never written: every mutant is a fresh byte
  copy"). Its frontmatter owns the method (`SKILL.md:3`: "Verification-fixture craft for …
  'mutation testing'"). Its `--regression` leg ledger (SKILL.md:951-960, ten legs since r51)
  replays pinned blobs of kagi/kumitate/kimi/tsukuroi/mado gates — mori's count-c2.py is not a
  leg. Its round-6 "mutation service" is opt-in, recommendations-only (SKILL.md:822-853,
  886-909); mori r80 does not request it and builds a frozen single-purpose harness instead.
- `kumitate-shokunin/scripts/gate-mutants.mjs:1-7,35-36` — kumitate's own-gate harness; K43 kill
  predicate; `TARGETS = ['cite-check', 'wave-census']` only.
- Embedded per-tool mutant batteries (same pattern, no shared artifact): chousa
  `research-gate.sh:5944-6003` + `freeze-check.py:386-389`; kaidoku round-26
  `c1-id-identity.py:707-833` (`--mutants` expectation file), round-30/31 refusal-mutant
  counters, round-34 `replay-gate.py:165-280`; kake `citation_lint.py:260-263` (mutant F);
  fleet `scripts/hyaku/disk-guard.sh:1165-1177` (seeded-defect selftest arm).

No committed instrument anywhere targets `.ufo/waves/round-79/count-c2.py`; mori's r80
six-mutant harness (frozen grammar `MUTATION_C2 survivors=S killed=K total=6`, controls-r80.txt
§C2 shows `survivors=2` at `d5888922`) duplicates the pattern, not any artifact. The r79
mutation-seat S595 sourcing mirrors tameshi's recipe (one exact edit per fresh copy, kill = suite
red) without reusing its tool — consistent with tameshi's owner-hardens rule (the lane owns its
gate; tameshi only reports).

### C3 (province instrument inventory) — ADJACENT; mado is the shape to align to

Two lanes already keep own-lane tool inventories in PROVINCE:

- Closest shape, `mado-shokunin/PROVINCE.md:20-35`: "Round-23 refinement (C3 lane-tool
  inventory …): the lane's own analysis instruments are named here so the province accounts for
  every tracked tool it runs." Table header (:22): `| Tool | Reads | Writes | Owner and adjacent
  lanes |`, one row per tool. Crucially the wave-2 correction (:35) widened the scope: "the
  inventory above covers every tracked file under `tools/`, not 'every tracked tool it runs'" —
  exactly the completeness bar mori's 55/55 target bakes in from the start. mori's contract
  freezes different columns (class, registry row or `—`, one-line purpose, append-only
  `## Instrument inventory (round 80)` at EOF), so the scribe should keep the contract's
  columns and borrow mado's scope discipline, not its column set.
- `kama-shokunin/PROVINCE.md:17` ("lane instruments (the capability repertoire, `SCORECARD.md`
  canonical list)") and the round-42 note (:173-177): "The Owns table now lists every `tools/`
  and `registry/` surface the SCORECARD capability list cites" — inventory keyed to the
  SCORECARD citations rather than the full `tools/` tree (kama's bar is weaker than mori's).
- Cross-lane inventory format (for contrast): `kengaku-shokunin/PROVINCE.md:340-345` rows of
  `| lane | instrument | description | evidence |` covering siblings — that is routing
  evidence, not an own-inventory, and mori should not imitate it.

"Registry row" vocabulary: the SKILL gate registry rows are `| name | kind | entry | verdict
map | self-test | pinned values | write scope | owner |` (mori SKILL.md, row 13
control-receipt-guard at ~:1365); the C3 section's registry-row cell should cite those row
positions (or `—` for the 41-1 instruments that have none).

## Boundary (ticket item 4) — all three claims stay inside mori's province

mori PROVINCE.md:1-20: fleet & host observability; read-only probes; refuses dispatch/
orchestration (→kumitate), OS/systemd state (→tsukuroi), endpoint health (→kama), credential
material (→kagi); "Detection and report only — never remediation."

- C1: in-province. It is calibration of mori's own record — the province already holds this
  class: PROVINCE.md:132-133 ("judging the lane's own claim labels against commit order,
  `tools/mori-freeze-order.py` … is calibration of mori's own record, not a fleet ruling"). The
  sweep reads committed bytes and spawns only pinned tools' `--selftest` read-only children —
  the same execution class as the census's read-only probes. No dispatch, no OS state, no
  endpoint, no credential. The token grammar `(corpus|tools|.ufo)/…` under `--root` (a mori
  export) cannot scan sibling lanes even where mori carriers cite them relatively — mori
  PROVINCE.md:287 cites `../tsukuroi-shokunin/tools/tsukuroi-census.sh:376,1100-1115`, whose
  leading `../` the grammar does not match.
- C2: in-province. Own-instrument operability over mori's own counter; mutants are applied to a
  scratch copy under TMPDIR/`--scratch`; tree stays read-only; no sibling artifact executed.
- C3: in-province. Documentation of mori's own instruments; it also discharges the named
  province-stale debt (PROVINCE.md:397-400: "sixteen `tools/` files and six fixture directories
  are not named here (ScoutProvinceStale items 4–5)").

## Sibling artifacts that could be harmed (ticket item 5)

- `kengaku-shokunin/PROVINCE.md:105` cites `mori tools/mori-retention-reconcile.py:169-177`.
  None of the three claims edits that file (deliverables: new `tools/mori-claim-sweep.py`,
  selftest-region arms in `.ufo/waves/round-79/count-c2.py`, PROVINCE.md append-only EOF,
  SCORECARD row + capabilities row, SKILL registry row 14, `.ufo/waves/round-80/*`) — no
  sibling-cited mori line moves.
- tameshi's `--regression` legs materialize from git blobs at pinned revisions; work-tree edits
  in mori cannot touch them. mori's harness never invokes tameshi's tool — no coupling.
- chousa's `lane-preflight.py` G04/G05 read a lane's files only when a caller points `--root` at
  it; mori r80 writes no chousa file and no shared `scripts/` file.
- Shared fleet files (`scripts/hyaku/*`, `LOG.md`, `MANIFEST.json`): mori r80 edits none (bounds).
- Residual (mori-internal, for the reviewer not a sibling): adding selftest arms to
  `.ufo/waves/round-79/count-c2.py` can shift line numbers any mori r79 receipt quoted; the
  contract already binds the hunks to the selftest region with a diff proof, but receipts quoting
  absolute line numbers should be checked by the wave's reviewer seat.

## Work-tree note (observation, not graded here)

The wave is mid-flight: `git -C mori-shokunin rev-parse HEAD` → `57451ecbbc5a63cfa…` (entering
was `d5888922`); `git status --porcelain` shows `M SCORECARD.md` and `?? tools/mori-claim-sweep.py`.
The stale literal is already corrected in the work tree: my grep for `selftest 18 in-memory`
finds 0 hits, and SCORECARD.md:4016 now reads "selftest 19 in-memory cases" with a
`## Round-80 correction (D79-1, calibration)` section at :4018. Controls-r80.txt had measured
`grep -c 'selftest 18 in-memory cases' SCORECARD.md` → 1 at the entering state. This does not
change any verdict above: the duplicate question is about sibling lanes, and no sibling holds
any of the three grounds.

## What I could not verify / negatives

- "protocol" (ticket item 2): no lane directory named `protocol*` exists at the fleet root
  (`ls` listing checked); the referent is the fleet-root `PROTOCOL.md` (tameshi SKILL.md:1780
  notes "the lane holds none"). No mutation harness lives there; nothing to report beyond that.
- Fleet-root `m-rev-vs-rev.py` is a copy of souji's coverage-map agreement instrument
  (docstring :1-3), not a claim resolver; excluded from the C1 nearest-three.
- Stray untracked dir `kumitate-shokinin/kumitate-shokunin/` (git: "pathspec did not match")
  sits at the fleet root — not a lane, not scanned; surfaced to the orchestrator as hygiene.
- I did not execute any sibling instrument or any mori counter, so kill/survivor behavior of the
  r80 harness is taken from controls-r80.txt, not re-measured by me.

## Own defects (caught and corrected)

1. My first grep for `selftest 18 in-memory` returned zero hits and I nearly recorded "the stale
   literal is absent" — wrong frame. The controls receipt (grep -c → 1 at `d5888922`) contradicted
   me; re-grepping `in-memory cases` showed the row now reads 19 at SCORECARD.md:4016: the C1
   seat had already corrected the work tree. Work-tree vs committed-state confusion, caught by
   the control, reported as observation only.
2. First C1 sweep covered lane `*/scripts` but not the fleet root `scripts/`; a second sweep over
   `/home/vgpnk/Projects/shokunin/scripts` closed the gap (fleet helpers are dispatch/wave/disk/
   jj tooling; no claim resolver).
3. My repo-wide grep of kumitate matched binary jj op-store blobs (`.jj/repo/op_store/…`) and
   wasted a page of noise; narrowing to `scripts/*.mjs` globs + targeted reads fixed it. Lesson:
   glob the real source dirs first in jj-colocated lanes.
