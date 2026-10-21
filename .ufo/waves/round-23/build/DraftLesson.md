# DraftLesson — scoped findings report (round-23, lane `mori`)

Seat: `MadoR22-2.DraftLesson-8` — scribe/drafter for the lesson text, read-only, leaf member
(no subagent dispatch; no delegation performed).
Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Deliverable artifact: `.ufo/waves/round-23/build/DraftLesson/mistakes.md`.

## Behavior actually performed

1. Read the wave contract in full (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`,
   164 lines) and the host tooling directive (`/home/vgpnk/.omp/agent/RULES.md`).
2. Enumerated the lane commits in scope with read-only `git -C` plumbing. `1bfe708..4dc80c1`
   contains **exactly one commit** — `4dc80c1` "round-23: pre-register misleading-field cutover
   and quota-surface contract" (8 files, 427 insertions). All process rows below therefore
   concern `4dc80c1`.
3. Read the r22 evidence chain to locate the two routed items: `MANIFEST.json` `rounds[427]`
   (the r22 closure entry, index 427 of 428), `corpus/lessons/round-22.md`,
   `corpus/knowledge/retention-reconciliation-r22.md`, `corpus/QUALITY.md`,
   `.ufo/waves/round-22/{contract.md,frozen/requirements-v2.json,frozen/expected-real.json,
   frozen/fixture-builder-v2.py,oracle-reconcile-v2.py,refinement-reconcile.py,measure-round22.py}`,
   `tools/mori-retention-reconcile.py` at `8cb4afb` / `da40bb2` / `1bfe708`,
   `tools/mori-freeze-order.py`, `.ufo/waves/round-18/frozen/c2-register.json`,
   `corpus/evidence/freeze-register.json`, `SCORECARD.md`, `LOG.md`.
4. Read the r23 pre-registration artifacts at `4dc80c1`: `contract.md`,
   `frozen/c1-requirements.json`, `frozen/c1-expected-real.json`, `frozen/c2-expected-real.json`,
   `oracle-rename.py`, `LOG.md`, `SCORECARD.md` diff.
5. Cross-read the sibling wave-1 build reports that overlap this seat's subject
   (`build/CriticFreezeOrder.md`, `build/CriticRenameHarm.md`, `build/ReviewOracleRename.md`) to
   avoid double-counting and to record conflicts verbatim.
6. Recomputed, read-only, every digest the r23 frozen files pin, and confirmed all match the
   committed bytes.

## Gates and evidence discipline

* **No test, build, lint, formatter, smoke run, oracle run, driver run or tool execution was
  performed.** No `quotactl`, `btrfs`, `xfs_quota`, `repquota`, mount or privileged command was
  invoked; no live host probe of any kind was made. Every "fix" in the artifact is a
  *pre-registered* mechanism with an explicitly stated red/green or mutant-kill demonstration for
  L1 to execute after integration.
* Only read-only `git` plumbing (`log`, `show`, `ls-tree`, `rev-parse`, `rev-list`), file reads,
  JSON reads and `sha256sum` were used. All paths touched are inside the lane except the two
  read-only files named by the assignment (`contract.md`, `RULES.md`) and the fleet
  `MANIFEST.json` (read-only).
* **Tool installs / updates: none.** No tool was needed; nothing was installed or upgraded, so
  there is no install record to report.
* No lane Git index, jj state, commit, worktree or branch was mutated; no `git add`/`commit`/
  `push`/mutating `jj` command was run. Nothing was written at the fleet root. No background job
  was started. No session transcript was read (this wave permits none).
* Negative results are reported as such: all seven pinned digests match, and the r23 oracle's
  R26 literals (2 and 4) are arithmetically consistent with the frozen r22 builder and the tool
  at `1bfe708` — no digest or arithmetic defect was found there.

## Findings (candidate `## Mistakes` rows, artifact `build/DraftLesson/mistakes.md`)

Nine candidate rows, in the repo's existing round-22 table shape
(`ID | Class | Evidence pointer | Captured-by | Fix / fail-capability`):

| ID | one-line class | assignment item |
|---|---|---|
| M1 | expectation co-committed with the implementation it is supposed to bound; the co-evolution was never rendered as a `co-evolved` verdict and never entered the freeze register | (a) |
| M2 | frozen output key name accepted at freeze time with no key↔population binding (a "raw"-named key carrying the policy-filtered count) | (b) |
| M3 | the pre-registration presents a status-neutral MANIFEST defect as a routed claim — `rounds[427]` routes only the rename | (c) |
| M4 | frozen expectation file mixes an observed before with a predicted after under one shape, unlabelled, with one field carrying two types | (c) |
| M5 | author-side oracle frozen with no authorship disclosure; r22's explicit disclosure precedent dropped | (c) |
| M6 | the pre-registration's own declared consequence misstates its measurement instrument (staging claim and named breakage both wrong) | (c) |
| M7 | "measured by the r23 oracle only" drops the layer that supplies the requirement reasons, and the price (14 of r22's 22 mutants) is not stated | (c) |
| M8 | mechanical field substitution degraded frozen R02 to a tautology — sibling-corroborated, with the sibling conflict recorded verbatim | (c) |
| M9 | contract clause "SCHEMA … in every output (check, setup error, selftest)" has no frozen witness — sibling-corroborated | (c) |

### The two assigned items, stated plainly

**(a) r22 `frozen/expected-real.json` landed with the implementation.** `8cb4afb` ("round-22:
implement independent retention accounting reconciliation") contains **both**
`.ufo/waves/round-22/frozen/expected-real.json` (30 lines) **and**
`tools/mori-retention-reconcile.py` (274 lines). `MANIFEST.json` `rounds[427]` records it under
`verification.rechecks` → "Defects (status-neutral): … `frozen/expected-real.json` committed with
implementation, not pre-freeze (disclosed in SCORECARD)". `SCORECARD.md:1375-1376` carries the
append-only correction ("…not pre-build"). It was **never** a numbered row of the round-22
`## Mistakes` table, and — decisively — **no `r22` claim row exists in
`.ufo/waves/round-18/frozen/c2-register.json`** (`claims` = r17-C1..C3, r18-C1..C3) and
**`corpus/evidence/freeze-register.json` holds one correction only** (`r17-C3`). The append-only
vehicle that the `r17-C3` precedent demonstrates — a correction row grading a declared
`pre-build` as `co-evolved` — was available in-lane and was not used, so QUALITY #52
(`corpus/QUALITY.md:161-165`) was never triggered for r22.

**(b) the misleading frozen field name was accepted at freeze time.** At
`1bfe708:tools/mori-retention-reconcile.py:234` the tool emits
`'raw_unallowlisted':len(unallowed)` and `'scanner_unallowlisted':len(unallowed)` — one value
under two names, with the "raw"-named key carrying the **policy-filtered** count; the true raw
complement only appeared later, as `raw_not_allowlisted` at `:235`, added at `da40bb2`, i.e.
**after** the implementation commit `8cb4afb`. The name was frozen into the r22 oracle
(`oracle-reconcile-v2.py:52,56,57`) and the frozen builder
(`fixture-builder-v2.py:104`), then *documented* rather than corrected
(`corpus/knowledge/retention-reconciliation-r22.md:27-36`: "…intentionally name the same existing
policy-filtered metric"). MANIFEST `rounds[427]` ruled the *value* honest ("`raw_unallowlisted=4`
is HONEST, no re-freeze this round") but the *name* misleading, and routed the rename out
("Routed: rename `raw_unallowlisted` by pre-registration; carry debt."). No r22 build seat raised
"this name asserts the wrong population"; the defect was caught only by the closure, one round
late. QUALITY #70 (`corpus/QUALITY.md:282-292`) is the rule that should have caught it at freeze
time, and QUALITY #14 has no key-name clause.

## Conflicts recorded verbatim (for the canonical judge)

`build/CriticFreezeOrder.md` L9 #3 — "Redundant R02 conjunct… Values are equal, so nothing is
lost. Do not edit the oracle (it is frozen); disclose only."
`build/ReviewOracleRename.md` §5 W1 — "the 'both names denote the same number' agreement property
is no longer observable… *Not a defect*".
`build/CriticRenameHarm.md` §3 — "R02 now reads `scanner_unallowlisted==1` twice; this is harmless
because the tool at `1bfe708` sets both keys from `len(unallowed)` (tool line 234)."
This seat's narrower reading, recorded without overrule: the deleted conjunct was a
cross-population probe, redundant on today's two arms but unrecoverable on any future arm where
the populations coincide.

## Touched surfaces

* Written (2 files, both assigned to this seat, both inside the lane, both new):
  * `.ufo/waves/round-23/build/DraftLesson/mistakes.md` — the candidate `## Mistakes` rows.
  * `.ufo/waves/round-23/build/DraftLesson.md` — this report.
* Read-only: the files listed under "Behavior actually performed". **No production, frozen,
  contract, corpus, `tools/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md` or
  `MANIFEST.json` file was modified.** The `mistakes.md` rows are *candidates*; nothing was
  written into `corpus/lessons/`.

## Out of scope / deliberately not done

* Not written into `corpus/lessons/round-23.md` — that file does not exist and belongs to the L1.
* No edit to `contract.md`, `frozen/c1-*.json`, `frozen/c2-expected-real.json` or
  `oracle-rename.py`, all frozen at `4dc80c1` with published digests. Every proposed remedy is
  therefore written as an **appended** artifact (seal manifest, appended correction row, new
  check), never as an edit to a frozen file.
* No `tools/mori-freeze-order.py` run, no register row appended to
  `.ufo/waves/round-18/frozen/c2-register.json` or `corpus/evidence/freeze-register.json`:
  that is a round-18 artifact write and an L1 decision; it is *proposed* in M1, not performed.
* No oracle run, no fixture creation, no mutant, no driver pre-flight — prohibited in this wave.
* Not read: `.ufo/interactive-sessions`, `~/.omp` sessions, operator config, `Documents`, shell
  history, `agent.db`; no live journal/process/service/session probes; no `.scratch` candidate
  implementation; `build/ImplQuota/` was never opened.
* Rows deliberately **not** written (with reasons) are listed in the artifact under "Rows
  deliberately not written (and why)" — notably: r22's requirement rewrite was a *legitimate
  append-only correction* and not a mistake; and the r23 before-measurement is *required* by
  QUALITY #63 — the defect is the missing label (M4), not the measurement.

## Open decisions for the L1

1. **M8** — accept the three-seat "harmless, disclose only" reading, or this seat's narrower one.
   Both are in the artifact verbatim; the judge should decide, not this seat.
2. **M6 / M3** — both corrections must land as *appended* seal-manifest rows, since
   `contract.md` is frozen with a published sha256 (`2bb35aef…69e7`).
3. **M1** — confirm the lane permits an r23 append to the round-18 register and correction file
   before it is done.
4. **M7** — the price of "the r23 oracle only" (14 of r22's 22 mutants un-killed) is the most
   consequential of the seven process rows and belongs in the contract's declared-consequence
   text, not only in this lesson's candidate table.

Tool installs or updates: **none**.
