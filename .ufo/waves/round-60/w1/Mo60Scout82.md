# Mo60Scout82 — sibling overlap (entry-claims / counter-boundary)

Detection and report only. No production edit, no VCS mutation, no sibling write.
Mori boundary read from committed `PROVINCE.md` (working tree clean for every
path cited below). Sibling HEADs pinned 2026-10-28:

| repo | `git rev-parse HEAD` |
|---|---|
| kumitate-shokunin | `14057f3e3899180c95713bace088fb9c0d0046e3` |
| kotodama-shokunin | `44f76d456c1b326a71ffdb381590af825cbf11be` |
| souji-shokunin | `cb443f5499fe4ccaa1f1f035050b0752aefadd92` |
| tabi-shokunin | `0081bfdb93b6bd1bf2853bb128996f1a976b7218` |
| mori-shokunin (tip at read) | `b3c256138f00c704d5aa56eb0332d74506502ef2` |

`git status --porcelain` on every cited path in those five repos printed nothing.

## Mori boundary this scan is held against

`PROVINCE.md:12-18` refuses dispatch/orchestration (kumitate), OS state
(tsukuroi), endpoint health (kama), credentials (kagi); detection and report
only; out of province is reported, never absorbed. `PROVINCE.md:65` — kumitate
owns wave plan/run/record/collect; mori grades `.ufo/waves/*` filesystem shape.
`PROVINCE.md:145-154` — `tools/mori-wave-settlement.py` `settled` is report-file
presence only; result acceptance and re-dispatch stay kumitate's.
`PROVINCE.md:69` and souji `PROVINCE.md:50-52` — souji routes liveness/resource
findings to mori and does not reclaim on mori's behalf.

Round-60 instruments under that boundary (not re-scored here):
`tools/mori-entry-claims-check.py` H1–H5 (grammar blocks, distinct byte spans
≥8, non-degenerate texts, per-copy row binding) and counters G1–G3 (pin-gated
execution, containment-asserted materialization, frozen expect tables).
`corpus/knowledge/entry-claims-hardening-r60.md:6` states the coverage-map:
own claim-verification instruments for wave-settlement evidence; no sibling
surface claimed.

## Negative: no sibling copy of the r60 predicates

Searched production trees (not `.ufo` wave dumps) for
`dup_span|tool_sha|expect_tamper|mori-entry-claims|MIN_SPAN|entry-claims`:

- kumitate `scripts/` + `corpus/knowledge/`
- kotodama `tools/` + `corpus/knowledge/`
- souji `tools/` + `corpus/`
- tabi `scripts/` + `corpus/`

No file implements `mori-entry-claims-v2`, `grammar:` verdict blocking,
`distinct:dup_span`, `tool_sha` as an execution refusal, or `expect_tamper`.
`tool_sha256` hits are a different predicate (below). `git ls-files` on tabi
for `scripts/*quote*`, `scripts/*claim*`, `corpus/knowledge/*quote*` printed
nothing: the round-35 `.ufo/waves/round-35/w2/CritC2Boundary/` quote-bound
probes are wave constructions, not a standing script.

## Nearest equivalents (mechanism-adjacent, not province overlap)

### kumitate — owns these; mori must not absorb them

- `scripts/claims-check.mjs:1-15` contract `kumitate-claims-v1`. Re-derives
  SCORECARD registry `yes` cells as origin-tree **member sections** (live
  own-file anchor + verbatim symbol + distinct member count,
  `MEMBER_COUNT_DRIFT` at `:35`). Not quote-bound K-claims over wave-settlement
  artifact copies. Core band: `PROVINCE.md:12-15`. Name collision only.
- `scripts/wave-census.mjs:1-26` contract `kumitate-wave-census-v1`. Reads
  `ufo-swarm-wave-dispatch-v1` and counts reports present/absent, role totals,
  `COUNT_MISMATCH` / `REGISTRY_MISMATCH`. States a payload proves validation,
  not dispatch (`:19-26`). Same evidence class as mori's filesystem-shape
  settlement scan, already split at mori `PROVINCE.md:65,145-154`. The file
  does not mention mori and does not grade host liveness. The r60 entry-claims
  tool does not census seats or call collect. **No new ownership collision.**
  [INFERENCE] absorbing `wave-census` into mori would cross the recorded
  kumitate boundary; this round's instrument does not.
- `scripts/counter-pins.mjs:32-43` contract `kumitate-counter-pins-v1`.
  sha256 of frozen counter bytes; `..`/absolute is `path-escape`; a symlink is
  not a regular file (`:255-263`). "The gate never writes. It reads the
  registry and the pinned bytes only." Pin and path refusal without executing
  the pinned file. Not G1.
- `scripts/report-receipt-diff.mjs:10-34` contract
  `kumitate-report-receipt-diff-v3`. Binds labelled report tallies to committed
  receipt bytes; a `..` path or a symlink is `RECEIPT_MISSING` (`:18-19`).
  Declared limit (`:32-34`): a receipt is trusted as written; nothing binds it
  to a counter run. Report-contract gate, not an entry-claims verifier.
- `scripts/counter-rerun.mjs:1-15` compares one named probe's final summary
  line across K runs. Not an unpinned-blob gate.

Kumitate `PROVINCE.md:3-6` refuses anything outside orchestration and tooling.
None of these probes journal/cgroup/watchdog surfaces.

### kotodama — homonyms, linguistic province

`PROVINCE.md:12-14` refuses fleet protocol. No entry-claims or counter
execution gate.

- `tools/check-gate-quotes.py:1-12` — 25-word cap on lesson `## Gate`
  quotations. Quote length, not byte spans.
- `tools/check-cited-lines.py:1-20` — `MULTI-ID` / `TABLE-ID` on `S###`.
- `tools/check-claim-separability.py:1-8` — landed-byte dependency between
  claim units, not quote claims.
- `tools/check-supersession-settlement.py:1-27` and
  `tools/check-settlement-fixture.py:1-18` — SOURCES-row supersession
  (`pending` / `mined` / `used-by`). **Settlement here is a registry-chain
  homonym**, not `.ufo/waves` settlement. Do not merge with mori's FR3 row.
- `tools/harness/basename-couples-resolver.py:464` stamps `tool_sha256` of
  itself into a JSON payload. A digest field, not a gate.

### souji — receipt digest and input fence; existing adjacency unchanged

- `tools/souji-receipt-run.py:1-8,27-37` — `run` re-derives a command at a
  durable rev and writes `tool_sha256` of the tool blob at that rev; refuses
  checkout bytes that differ from the committed blob (`TOOL-CHECKOUT-DIFFERS`)
  and refuses a receipt path outside scratch or inside the repo. `verify`
  (`:350-368`) compares the receipt digest to `git` blob bytes and does not
  re-execute. Lane limit, `corpus/README.md:554` and `:558`: a `verify=ok`
  "binds labelled committed bytes, not the executed program or command
  success." That is the opposite of mori G1 (refuse to execute an unpinned
  blob). Q55 (`corpus/QUALITY.md:129`) is the same receipt rule.
- `tools/souji-rev-pin.py:128-167,343-346` — measured-input walk refuses
  symlinks and `..` (`path-escape-refuse`). Input boundary for souji evidence
  runners, not materialization of a hostile tree and not fleet observation.
- `PROVINCE.md:50-52,77-78,141-143` — host-wide liveness stays mori's; souji
  lists own-uid residue only. **No new overlap.** Do not absorb the receipt
  runner; do not treat `tool_sha256` as G1.

### tabi — opt-in reproduce guard, browser province

`PROVINCE.md:3-19` is browser/web interaction; refuses RE, publishing, secrets.
No fleet or wave-settlement ownership.

- `scripts/check-measurement-binding.mjs:4-11,57-76,623-638` — default path
  compares the counter blob at `measuredRevision` to a declared sha256
  (`counter_digest_mismatch`). `--reproduce` executes only when that check is
  already clean **and** worktree bytes equal the blob at `--at`
  ("Never execute unbound bytes", `:624-638`). Closest execution-refusal analog
  to G1, scoped to tabi's own measurement manifest. It does not materialize
  hostile trees, does not grade `expect.txt`, and does not read mori's
  surfaces.
- `scripts/check-c2-knowledge-round41.mjs:1-7` — presence/provenance of one
  named knowledge entry (frontmatter, six table rows, S146/S147). Not a
  general quote-span verifier.

## Verdict

No overlap with mori's PROVINCE. No sibling instrument claims fleet/host
observability, report-file wave settlement, or the r60 H1–H5 / G1–G3
predicates. The nearest tools are owned inside kumitate (member-claims gate,
wave-census, counter pin, receipt diff), kotodama (quote-cap and SOURCES-row
"settlement"), souji (blob-bound receipts; digest ≠ executed program), and
tabi (measurement-binding reproduce guard). Shared wave-report evidence with
kumitate is the split already written at mori `PROVINCE.md:65,145-154`.
Report, do not absorb.

## Not done

Sibling tools were not executed. `.ufo/` wave dumps were not exhaustively
read after the standing `scripts/`/`tools/`/`corpus/`/`PROVINCE.md` scan;
tabi's round-35 quote-bound probes were confirmed unlanded as scripts.
Parsers of `wave-census.mjs` and `mori-wave-settlement.py` were not diffed.
