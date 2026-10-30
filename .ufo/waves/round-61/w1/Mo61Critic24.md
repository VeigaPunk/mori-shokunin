# Mo61Critic24 — whole-contract falsification sweep (counters vs claimed work)

Lane: mori-shokunin. Freeze `7370a731`, entering `325f7e63`. All work read-only on the
lane/fleet; every experiment ran in a scratch fixture repo created at an explicit path
(`/fast/scratch/hyaku/mori-r61/Mo61Critic24/fx.YmvxPc`, `git init` there, all later git
calls `git -C "$D"`, throwaway identity `t <t@t>` inside it only). Scratch cleaned after
receipts were copied here. No tools installed; no VCS state touched; findings only.

**Question:** cheapest committed-revision path where ALL THREE counters print `met`
without the claimed work — empty tree, entering rev, counters-only tree.

**Answer.** All three print `met` at one committed revision built from three artifacts,
none of which requires the claimed work (fixture rev `6ea3ca4e3388`, arm D below):
(1) **one** SKILL.md registry row whose entry cell lists all 25 manifest paths;
(2) `corpus/knowledge/psi-v73-recheck-r61.md` with 47 mechanically generated rows —
status `changed` on every pointer, quote located in a *different file* than the anchor,
provenance trio filled with stubs — no v7.2 comparison anywhere (v7.2 bytes are not in
the repo at all); (3) six `corpus/SOURCES.md` lines with `opened 2020-01-01`. C3 needs
nothing at all: it is already `met` at the freeze rev, and at a counters-only rev that
does not even contain `count-c3.py` (arm B). Per-claim do-nothing arms: empty tree and
entering rev hold for all three; the counters-only tree **breaks C3**.

## Arms (executed; outputs verbatim)

| arm | fixture rev | C1 | C2 | C3 |
|---|---|---|---|---|
| A empty tree (`--allow-empty` commit) | `2048d804b330` | unmet `manifest_unreadable` | unmet `source_entry_absent` | unmet `livepins=FAIL` |
| B counters-only tree: only `count-c1.py`+`count-c2.py` committed, **no `count-c3.py` at rev** | `d264d1994a12` | unmet | unmet | **`C3=met r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=ok cases=5 failed=none`** |
| C entering rev | `325f7e639916` | unmet (default manifest: `manifest_unreadable`) | unmet `entry_absent` | unmet `livepins=FAIL` |
| D cheapest-all-met: freeze tree + 1 omnibus SKILL row + 47 mechanical ledger rows + 6 SOURCES lines | `6ea3ca4e3388` | `met gates=25 registered=25 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0` | `met pointers=47 rows=47 same=0 moved=0 changed=47 quotes_ok=47 spans_ok=47 sources=6 failed=none` | `met` (all ok) |
| E measured rev commits the **r60 holey counter** at `.ufo/waves/round-61/count-c3.py` (`git show <rev>:…` sha = `fabde06c…` = R60_SHA); good file runs from disk | `d3294f26a15b` | — | — | **`C3=met`** — false pass |
| F registry where **all 25 rows are marked superseded** in the name cell | `1cfb8606f2c0` | **`met gates=25 registered=25`** | — | — |
| G `gate-manifest.json` rewritten to 1 path + 1 row | `90b4a44b833d` | **`met gates=1 registered=1`** | — | — |

Arm D receipts: ledger head `source: (stub trio — values unverified by counter)` /
`verified-at: 1970-01-01` / `recheck: never performed`; first rows
`| psi.rst:60-65 | changed | psi.c:1-1725 | `* Pressure stall information for CPU, memory and IO` |`,
`| psi.c:342-360 | changed | psi_types.h:1-216 | `/* Tracked task states */` |` — the
anchor's file is never consulted for non-`same` rows; quotes are arbitrary copy lines.
Omnibus row: `| r52-r60 gates (bulk registration) | gate | `.ufo/waves/round-52/count-c1.py` … (25 paths) | 0 met · 1 unmet | `python3 -I -B .ufo/waves/round-61/count-c1.py --selftest` → pass | sha 00 | read-only | MoriR61 |`.

## C1 — do-nothing arm holds; the met line is reachable without registry work

- **Holds:** empty tree and entering rev both unmet (arms A/C). At the entering rev the
  registry tables end at r51 and no row names any of the 25 paths (0 of 25 mentioned
  anywhere in SKILL.md at freeze).
- **F1 (medium) — one row registers all 25 gates.** `row_hits` matches
  `path in toks or path in r["entry"]` — a substring test on the whole entry cell
  (`.ufo/waves/round-61/count-c1.py:68`). Arm D: a single row naming all 25 paths in its
  entry cell, with one shared self-test/owner, prints `registered=25 missing=0 dup=0`.
  The contract's target text ("exactly one non-superseded row whose entry cell names the
  path") is literally satisfied, but the calibration intent — a per-gate row with that
  gate's verdict map, self-test and owner — is not measured.
- **F2 (medium) — a superseded-only registry still registers.** `live` filters rows whose
  name/scope contain "supersed"; when `live` is empty the code falls back to
  `row = live[0] if live else hits[0]` (`count-c1.py:96-103`), i.e. it registers the
  superseded row. Arm F: 25 rows all named "… (superseded by next row)" →
  `C1=met registered=25`. Contract target says "exactly one **non-superseded** row".
- **F3 (low) — mention counts as registration.** A path named inside another row's entry
  prose (`… (wrapper; see `<path>` for lineage)`) yields `hits=1 live=1` (micro-probe).
- **F4 (low) — `noowner` is a dead token.** No increment site exists (only the dict inits
  at `count-c1.py:75,214` and the fmt at `:127`). An empty owner cell is caught by the
  generic `thin` branch (`:104-107`), so the kill rule holds — but the frozen met line's
  `noowner=0` is a constant, the same "token printed from a literal no measurement
  produces" shape that round 60 used to decertify C3, un-repaired in C1.
- **F5 (medium) — the frozen 25-gate set is unpinned.** The manifest is read at the
  measured rev (`cat(repo, rev, manifest)`) with no sha check; arm G shows a rewrite to
  1 path + 1 row prints `C1=met gates=1`. The counter accepts a contract violation
  (manifest amendment is barred); only the L1 eyeballing the frozen met-line format
  (`gates=25`) would catch it. The counter cannot detect what it polices.
- **F6 (info) — self-test cells are free text.** The check is `"--selftest" not in
  row["selftest"]` (`:109`); it never verifies the named command exists. Two manifest
  entries have no `--selftest` support in their own source at the freeze rev
  (`.ufo/waves/round-57/count-c1.py`, `.ufo/waves/round-57/verify-c2-source.py` — no
  match for `--selftest`), so a conformant row for them necessarily names a command that
  cannot run; the counter blesses it.

## C2 — do-nothing arm holds; the recheck itself is unmeasured

- **Holds:** empty tree (`source_entry_absent`) and entering rev (`entry_absent`) unmet;
  47 pointers enumerated from `system-pressure-r24.md` at every rev that carries it.
- **F7 (high) — the `same|moved|changed` verdicts are unverifiable, and non-`same` rows
  ignore the anchor entirely.** No v7.2 bytes exist in the measured tree (only the six
  v7.3 copies are pinned), so no counter *could* check a verdict against v7.2; and for
  `moved`/`changed` the quote is located via the row's own loc
  (`count-c2.py:148-152`), never the anchor. Arm D: 47 rows, every one `changed`, locs
  deliberately in other files, quotes = arbitrary copy lines → `C2=met changed=47
  quotes_ok=47 sources=6`. The claimed work (a per-anchor v7.2→v7.3 comparison) is not
  measured at all; a script that copies lines out of the pinned copies satisfies the
  counter.
- **F8 (low) — provenance trio is a label-presence check** (`provenance_ok`,
  `count-c2.py:85-88`): three line-start prefixes in the first 2000 chars. Arm D passed
  with `verified-at: 1970-01-01` / `recheck: never performed`.
- **F9 (low) — "opened this round" is not checked.** The SOURCES.md scan
  (`count-c2.py:176-179`) requires only the copy path, `| S`, `| mined |` and the ledger
  name on one line; arm D passed with `opened 2020-01-01`.
- **F10 (info) — the pointer set floats with a mutable prose file.** Pointers are
  enumerated from `system-pressure-r24.md` *at the measured rev*, floor 40
  (`count-c2.py:183`). The entry is a production file the C2 work is about; rewording it
  (or un-prefixed continuation pointers like `psi.c:342-360,408-411`, which the
  prefix-anchored regex cannot see) moves the required row count between 40 and 47 — up
  to a 15% work reduction that stays met, or an increase the closure learns about only
  from `pointers=N`.
- **F11 (low) — contract/counter met-line divergence.** The contract's frozen C2 met
  predicate reads `… sources>=4 rows_src=ok provenance=ok failed=none`; the counter's
  fmt prints `same=/moved=/changed= sources=N failed=…` and never prints `rows_src` or
  `provenance` tokens. A reviewer matching the frozen line verbatim can never match a
  genuine met run. (C1 and C3's frozen lines do match their fmt output.)

## C3 — do-nothing arm **breaks**: met without the counter, met with the hole committed

- **F12 (high) — the repair arm audits the runner's file, never the measured revision.**
  `main()` sets `self_bytes = Path(__file__).read_bytes()` (`count-c3.py:282`); nothing
  compares it to `git show <rev>:.ufo/waves/round-61/count-c3.py`. Arm E: the measured
  rev commits the **r60 holey counter** at the r61 path (committed bytes sha
  `fabde06c9d0a…` = R60_SHA — receipt above) while the good file runs from disk →
  `C3=met`. The kill rule "any static arm finding the r61 counter itself holey" cannot
  fire on the revision. The committed control receipt shows the same signature: at the
  entering rev, where `.ufo/waves/round-61/count-c3.py` does not exist at all, the
  receipt still prints `r61repair=ok`.
- **F13 (high) — a counters-only tree meets C3.** Arm B: a rev containing only
  `count-c1.py` + `count-c2.py` (no `count-c3.py` at all) prints `C3=met` — `livepins`
  pins only c1/c2, `r60hole` reads the pinned r60 object from history, and the
  self-referential arms read disk. Likewise at the real freeze rev `7370a731` C3 already
  prints met before any closure work (verified on the lane repo, read-only) — consistent
  with an instrument claim, but C3's met line carries no information beyond "the two
  sibling counters are committed unmodified".
- **F14 (medium) — the "met is the conjunction" arm is syntactic.** `arm_r61repair`
  (`count-c3.py:106-124`) checks that the first `met = ` line contains `c1_ok` and that
  `*_ok` assignment sites exist — not that `c1_ok` is computed from the booleans.
  Mutant `c1_ok = True  # hollow` → `r61repair_ok=True`; mutant
  `met = "c1_ok" in TOKEN_MAP` → `r61repair_ok=True`. The exact r60 hole shape (met not
  a conjunction of measurements) survives the repair undetected.
- **F15 (low) — blobrefusal/expectpin measure the file's own bookkeeping.** `EXEC_LOG`'s
  only append site (`count-c3.py:80`) sits inside `run=True` *after* the pin check, so
  "zero child executions recorded" (`if EXEC_LOG:`) is tautological; a mutation that
  executes an unpinned blob without appending passes. `expectpin` recomputes
  `EXPECT_PIN` from `EXPECTS` in the same file (`:48`, `:144`) and hashes a locally
  constructed "tampered" dict — self-referential constants.

## Smallest safe corrections (report-only; amendments barred this round)

- **C3:** pin the counter's own committed bytes at the measured rev exactly as `livepins`
  pins c1/c2 (compare `git show <rev>:.ufo/waves/round-61/count-c3.py` to the audited
  bytes; fail when absent), and make the conjunction check semantic (require
  `c1_ok = all(b.values())`-shaped derivation, or evaluate `met` from the booleans in
  the arm).
- **C1:** reject a path whose only hits are superseded (drop the `hits[0]` fallback);
  require the entry cell to name exactly one path as its own token (or one row per gate);
  sha-pin the manifest; delete or implement `noowner`; optionally verify the named
  self-test command resolves.
- **C2:** either pin the v7.2 anchor quotes so `same` is checkable, or restate the claim
  so the verdict column is declared unverifiable-by-counter; pin the pointer census
  (count + sha of the entry's pointer set at freeze) against the 40-point floor; align
  the contract's frozen met line with the counter's actual fmt output.
- **Controls:** record the exact invocation in each control receipt — the committed
  `control-c1-do-nothing.txt` shows `gates=25` at the entering rev, which is only
  producible with `--manifest` pointing at the freeze-time manifest file (the manifest
  does not exist at `325f7e63`; default run prints `gates=0 manifest_unreadable`), so
  the receipt's printed rev predates the manifest bytes it measured.

Impact axes: calibration (F1-F6, F10), freshness/depth (F7-F9, F11), operability and
duplicate authority (F12-F15 — two sources of truth for the counter's identity: disk vs
rev). None of these is fixable by a seat; all route to the lesson.

## Scope & limitations (bounded handoff, 2026-10-30)

Per the orchestrator's bounded-final-handoff instruction, no probes were run after that
message; every arm and micro-probe above was executed before it, inside the scratch
fixture, and the fixture has been removed (receipts above are the surviving evidence;
fixture revs are therefore no longer resolvable). Explicitly **unverified / not
attempted**: (a) the F10 pointer-floor reduction was reasoned from
`count-c2.py:183` and the enumeration code, not demonstrated with an edited entry
commit; (b) the frozen `--selftest` batteries of the three counters were not re-run by
this seat (their committed receipts in `.ufo/waves/round-61/evidence/` were read, not
reproduced); (c) no live rerun of any counter against the lane repo at revs other than
`7370a731` and `325f7e63`; (d) F5/F6 were established from code reading plus the arm
G execution, not from an exhaustive audit of every registry row shape. The lane and
fleet repos were never mutated; the only file this seat wrote is this report.

