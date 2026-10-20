# AttackProvenance — moving worktree/dirty metadata vs committed receipt

Seat `MoriR15.AttackProvenance` (critic, report-only, leaf). Judged on: coverage. Milestone: retain validated positives without fabricated totals.
I made no production edits, ran no gates/tests/builds, installed nothing, and opened no credential/agent-db files.
What I did: read-only `git show/log/status/diff --stat`, `sha256sum`, and JSON reads of committed receipts.

Axes: **coverage** (how far committed receipts can back the C1 claim), **calibration/provenance** (whether metadata claims hold), **operability** (protected: no new gate contract or exit change).

Target under attack: the in-progress ProvenanceCapture edit in `tools/mori-round14-regressions.py`. My last read was sha256 `d5fb5496…`, and it was still changing. HarnessBuild's "revision and exact dirty path scope" for `tools/mori-round15-regressions.py` is in scope too. Line anchors below are from the last read. Function names are the stable anchors.

## Baseline facts (what committed receipts already establish)

- Every r14 wrapper receipt with a `sha256` map binds its four tool files to its `measured_commit` blobs exactly. I re-hashed `git show <measured_commit>:<path>` for `r13-preserved`, `green-after-accepted`, `red-before-accepted`, `r14-selftest-accepted` and `census-selftest`, and all 4×5 match. **No historical byte mismatch was found.**
- `drift-current.json` binds only `census_sha256`. Its baseline input `corpus/evidence/baseline-r10-20261015T2231Z.json` has had no commit since `5be8943` and is clean now. The binding is unrecorded but the bytes are unchanged.
- `r13-preserved/evidence.json` records `revision: {head: 8d22d18…, dirty: true, source: MORI_EVIDENCE_REVISION}`. The head is env-asserted and the dirty flag is a bool.
- The current committed r14 harness (`HEAD:tools/mori-round14-regressions.py:2237`) hashes `__file__` at **emit time**.

## CE1 — content edits to an already-dirty input report `moving: false` (primary)

**Counterexample. I observed this live during this review.**
- `git status --short --untracked-files=all` shows ` M tools/mori-round14-regressions.py` and `?? .ufo/waves/round-15/fixtures/*.json`.
- Both have concurrent writers this round. The harness bytes changed three times while I read them (`capture_revision` moved :408 → :403 → :406). The status line stayed byte-identical the whole time.

Run the gate while that happens:
- start porcelain == end porcelain;
- `revision_delta` (`:478`, branch `elif "head" in checked and "porcelain" in checked` `:498`) returns `moving: False`;
- `evidence.harness.sha256` (`:2430`, inherited from committed `:2237`) hashes the post-edit file, not the module Python loaded.

The committed receipt then binds the verdict to harness bytes that never ran **and** asserts the input did not move. Porcelain carries status codes, not content. Equality cannot prove "not moving".

**Axes:** coverage and calibration harmed (false provenance). Operability neutral.

**Smallest required behavior:**
1. Read `Path(__file__)` bytes once at import, hash them, and emit them as `harness.sha256_loaded`. Keep the emit-time hash and set `moving: true` if the two differ.
2. `moving: false` only when porcelain is equal **and** every declared input's start/end sha256 is equal. Declared inputs are: harness, `--census`, frozen census, `frozen_dir/inputs.json`, and for r15 every fixture pack plus the importlib-loaded r14 module.
3. If content was not compared, emit `moving: null` with `content_compared: false`. Never emit `false`.

These are digests only, with no bytes, and they leave the exit code unchanged.

## CE2 — an env-pinned head makes the head facet vacuous and unbound

**Counterexample.**
- `capture_revision` reads `MORI_EVIDENCE_REVISION` at both captures (`:413-415`, `head_state "ok:env:…"`). So `start.head == end.head` by construction.
- A commit that lands mid-run (L1 or a sibling) is invisible on the head facet. It is caught only if it also changes porcelain.
- The pin is never compared to the real `HEAD`, yet porcelain is computed against the real `HEAD`. A receipt can pair `head: X` (asserted) with a dirty scope relative to `Y`.
- The r13 precedent above (`source: MORI_EVIDENCE_REVISION`) is exactly this shape.

**Smallest:** always run `rev-parse HEAD` and use only that observed head in `revision_delta`. Record the env value separately as `asserted_revision` plus `asserted_matches_head: bool`.

## CE3 — prefix-only output exclusion can swallow verdict inputs

**Counterexample.**
- `porcelain_scope` (`:457`) drops every path under `_output_prefix(--output)`.
- `--output .ufo/waves/round-14` puts `.ufo/waves/round-14/frozen/` (frozen census and `inputs.json`) inside the excluded prefix.
- For r15, `--output .ufo/waves/round-15` would exclude all `fixtures/*.json`.
- Fixture rewrites are then excluded noise, and `moving` can still be `false`.

**Smallest:**
- Raise `SetupError` (exit 2, an existing meaning) when `--output` equals or is an ancestor of any declared input path.
- Or exclude only the paths the harness wrote: `targets/`, `fixture_root`, `evidence.json`. A prefix is not enough.

## CE4 — `dirty` is unconditionally true when output is in-repo (repeats the r13 vacuity)

**Counterexample.**
- The start capture (`:2172`) runs after `load_target` has written `output/targets/*.mori-census.sh`.
- With in-repo output (every r14 receipt so far), `"dirty": bool(porcelain)` (`:433`) is always `true`.
- This is the same uninformative `dirty=true` the r14 verifier routed as debt (`corpus/lessons/round-14-verifier-spotcheck.md:83,136`).

**Smallest:** also emit `dirty_outside_output`, computed from the already-filtered `porcelain_scope` list. This is a derived field, not a new contract.

## CE5 — the receipt's `head` is the pre-landing base, not the measured revision

**Counterexample.** The r15 green run will happen at `HEAD=0fa5e0d` with ` M tools/mori-census.sh`.
- `0fa5e0d` is also the commit of the pinned **red** control (`0e41cb83…`).
- The committed green receipt will say `head: 0fa5e0d`. A reader who takes `head` as the measured revision attributes green to the red commit.
- Only per-input digests tie the dirty bytes to the landing commit L. Census and harness are covered. The r15 importlib r14 module and the fixture packs are covered only if HarnessBuild adds them.

**Smallest:**
- Label the field `base_head`, not "revision".
- For each declared input emit `sha256` and `matches_base_head` (a hash of `git show HEAD:path`, read-only). A verifier can then check `git show L:path | sha256sum` equals the receipt digest.

## CE6 — r15 importlib reuse adds an unhashed moving dependency (HarnessBuild)

The r15 harness imports `build_fixture/census_env/Case` from the r14 tool, which ProvenanceCapture is editing this round (CE1 observation).

**Smallest:**
- Read the r14 module bytes once, hash them, and execute from those same bytes (`spec_from_loader` / `exec(compile(bytes))`), or re-hash after `exec_module` and compare.
- Emit the digest as an input.
- Parse fixture packs from the same bytes that are hashed (one read, `json.loads(data)`), never re-reading at emit.

## CE7 — unrouted: r13 tool keeps the asserted-dirty path (not owned this round)

- `tools/mori-round13-regressions.py:1088-1090` accepts `MORI_EVIDENCE_DIRTY=true|false` and has no source label for dirty.
- `round-14/build/HarnessMigration.md:144` documents `MORI_EVIDENCE_DIRTY=false`.
- Its `registry_status` reads the worktree `SKILL.md`, which is ` M SKILL.md` now.
- Any r13-preserved re-run this round keeps the bool-only debt.

**Required:** do not report the r14 dirty-scope debt as closed for r13 receipts. Route it as unclaimed conformance debt. At minimum, record `dirty_source: env|porcelain` next time the r13 tool is owned.

## CE8 — low-risk parsing and config residue (tradeoffs, not judge-rejecting)

- `_porcelain_path` (`:447`) strips C-quotes without unescaping, and splits on `" -> "`. Paths with special characters mis-prefix. This fails in the safe direction (counted as moving). The fix is `-z` with NUL parsing.
- Repo-local config still applies, including `core.fsmonitor`, which would run a hook. I found none set in `.git/config` now. `-c core.fsmonitor=false` closes it.

## Verdict for the judge

Fixable defects, not tradeoffs: CE1, CE2, CE3, CE4, CE5, CE6. Do not accept `moving: false`, `dirty`, or `head` from these receipts as provenance until the corrections above land. CE1 and CE2 are false-negative provenance, and the judge should reject them as written.

None of this changes C1 alarm behavior or exit codes. The corrections touch evidence fields only, plus one existing exit-2 setup refusal (CE3). The earlier r14 receipts stay valid: their digests match their measured commits.

Tools installed/updated: none.

## Addendum — peer cross-links received after broadcast (not independently re-verified here)

- `MoriR15.AttackCountVacuity`: the red control `0e41cb83…` equals `git show 0fa5e0d:tools/mori-census.sh`; worktree census is now dirty. Build the control from the git blob and hash executed bytes at load and end — a worktree path would carry CE1 false provenance.
- `MoriR15.AttackFixtureOracle`: per-case stub mode (`ignore-filters` vs `honor`) must be pinned alongside fixture digests; flipping mode makes mixed cases vacuous while every hash still matches. Extends CE6: hash the case→mode map too.
- `MoriR15.ReviewHarnessPacks`: pack schema has no per-pack sha256; harness must record path+sha256 per pack at load (CE6).
- `MoriR15.SecurityPrivacy`: digest-only remediation compatible with P8; never copy record bodies into evidence.
- Pack seats self-reported final sha256 (e.g. CleanControls `3e2e4df9…`, NegativeStatus `e8b91ad1…`, NegativeInvalid `a25b39f1…`, BootArray `a746fa2b…`); harness load-time digests should be compared against these, any mismatch = foreign writer.
- `MoriR15.PackProcessUser` refinement to CE5: untracked inputs (all fixture packs) have no `HEAD:path` blob; `matches_base_head` must be `false`/absent (not a capture error, never head-derived), leaving the load-time sha256 as their only binding. Additional self-reported pack digests: ProcessUser `0e7c89c5…`, KernelSystem `9c607784…` (cross-check only, not trusted pins).
- My earlier `agent://all` broadcast was a coordination-scope error (reached other lanes and Main); later coordination is restricted to `agent://MoriR15` / exact `MoriR15.<seat>`.

## Disposition spot-check (read-only grep, no execution)

`MoriR15.ProvenanceCapture` reported fixes in both r13/r14 gates. Statically observed in r14: `asserted_revision` separate from real HEAD (`capture_revision` :414-439); owned-path allowlist in `porcelain_scope`; `dirty_excluding_harness_output` start/end; `inputs_changed`/`harness_changed` from digests; `not_measured` discloses residual content gap; `HARNESS_SHA_IMPORT` module-level digest (r14 :346, r13 :510) used as `harness_sha_start` (r14 :2232, r13 :1303). CE1–CE4 addressed as written; residual (other already-dirty non-target paths) is disclosed, not claimed. CE6 remains HarnessBuild-owned; CE7 r13 env-dirty override not re-checked. Behavior unverified until L1 runs the gates.

CE7/CE8 follow-up (static read): r13 now emits `dirty_source` (`env:MORI_EVIDENCE_DIRTY`|`porcelain`) and `dirty_captured` beside the still-overridable `dirty` (main receipt `:2753-2755`, setup/tamper `:3159-3161`); both gates pass `-c core.fsmonitor=false` (r13 `:1230`, r14 `:405`). CE7 closed as a label, not a contract change. Maintainability nit only: in r13 the instance attribute `self.dirty_source` (set `:1145`, `:1316`) shadows the staticmethod `Harness.dirty_source()` (`:1290`); it works because an instance attribute wins over a non-data descriptor, but renaming one side avoids a future `self.dirty_source()` call on a string. CE8 quoting kept conservative (fails toward disclosure): accepted tradeoff.

Nit closed (static grep): method renamed `Harness.dirty_source_label()` (`:1290`), callers `:1316`, `:3160`; attribute and evidence key `dirty_source` unchanged; no stale `dirty_source()` call remains. Open item from this seat: CE6 only (HarnessBuild-owned). All dispositions unexecuted; L1 verifies.
