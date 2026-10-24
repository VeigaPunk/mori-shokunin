# DraftDriftNote — C1 knowledge note (draft report)

Seat: MoriR20.DraftDriftNote (scribe, leaf). No subagents. No census run. No installs.
Draft: `.ufo/waves/round-20/build/DraftDriftNote/drift-repin-r20.md`

## Behavior

Wrote the C1 knowledge note draft covering: why the r10 pin stayed red (r12 through r20), the closed classification set, the r20 re-pin ritual, and the immediate-drift flap. L1 placeholders are marked `TODO-L1`.

## Findings (path:line or command evidence)

1. **Red for nine rounds, four causes.** Census SHA moved `d7710981…` (pin, `corpus/evidence/baseline-r10-20261015T2231Z.json` header) → `3da5b098…` (`corpus/evidence/drift-r12-20261019T2230Z-after-roster.log:1`) → `87b8d680…` (`.ufo/waves/round-20/evidence/c1-drift-entering.json:3`). Host boot moved to `2026-10-19 08:11:44` (`corpus/evidence/drift-r12-20261019T2204Z-classification.md` §A). The classification was prose at r12, and the r13 register is incomplete (see 2).
2. **Register coverage, recomputed read-only.** Live tokens 50 (`c1-drift-entering.json` `token_count`); r13 register keys 42 (`.ufo/waves/round-13/evidence/drift-classification.json`); live minus register = 8, matching `unclassified_vs_prior_register` exactly. All 42 register keys are present live. Register class mix: 21 `r12 roster schema carried since r10`, 14 `[INFERENCE] … no re-pin/admission claim`, 7 `intentional journal schema/version/mask change`.
3. **Closed set (draft):** `census-schema-change | roster-change | live-state | census-regression`, one class per token, each with an evidence pointer; `census-regression` blocks the re-pin. Classify by cause, not effect. Hard case: `-FINDING:WAVE_UNSETTLED_AGE`, labelled "coverage/evidence-loss regression" in the r12 prose; verdict left to TokWaves and L1.
4. **Flap token set maps to one lane's arm change.** `+path +reason` are row-6 keys (`tools/mori-census.sh:2411` at `87b8d680…`); `-subject_commits -window` are row-A keys (`:2473`); `basis` and `round` changed. [INFERENCE] one lane moved row-A → row-6 between `10:22:12Z` (scratch pin header) and the drift. Eleven pin rows are row-A (`.ufo/waves/round-20/evidence/c1-pin-probe-scratch.json`). Identity is `TODO-L1`.
5. **Scope of the r10 acceptance leg.** `corpus/knowledge/drift-pin-r10.md` §5.5 says drift after ≥60 s is `none`. That holds for clock and counter churn only. Lane arm changes are unmasked by design (§3.3), so the note states the leg must record arm transitions as the stability window.
6. **Discrepancy to resolve:** L1 reports pin at `10:23:18Z`; the scratch file header says `pinned_ts=2026-10-21T10:22:12Z`. Both recorded; `TODO-L1` confirm.
7. **Flap source caveat:** the 65 s drift output was not stored in any file. The flap is taken from the L1's report in `.ufo/waves/round-20/wave1-run.json` (TokPinFlap task text), not from a re-read of the output.

## Touched surfaces

- Created: `.ufo/waves/round-20/build/DraftDriftNote/drift-repin-r20.md` (draft).
- Overwrote: `.ufo/waves/round-20/build/DraftDriftNote.md` (this report; the `STATUS: started` line was replaced).
- Read only: contract, E1–E9 listed in the draft §0, `/tmp/mori-r20/` scratch (`drift-entering.txt`, `pin-probe.json`), `tools/mori-census.sh` (grep for emit sites, not executed).

## Out of scope / not done

- No census run (`--drift`, `--pin`, `--selftest`) by this seat.
- No register, no baseline, no re-pin: all L1 work. The register `corpus/evidence/drift-classification-r20.json` does not exist yet.
- No token classified in the draft beyond the pre-existing register and the one flap lane mapping (marked [INFERENCE]).
- No edits to the census, committed baselines, lane files, git/jj state, MANIFEST or host services.

## Tooling

None installed or updated.

## Checks for the main agent

- After L1 writes the register: `LC_ALL=C comm -23 <(tr ' ' '\n' < DRIFT | grep -v '^MORI_DRIFT:$' | grep . | sort -u) <(jq -r '.tokens|keys[]' REG | LC_ALL=C sort -u) | wc -l` must be 0; the `census-regression` count must be 0 before any pin.
- Confirm `sha256sum tools/mori-census.sh` = `87b8d680…ab28` at the measured commit before pinning.
- Confirm the flap lane identity and the 10:22:12Z / 10:23:18Z discrepancy (`TODO-L1`).
- Note: `comm` gave unreliable output in my shell attempt (sort-order warnings); the set difference was recomputed with a Python set check instead, which agrees with `c1-drift-entering.json`. L1 should use a set-based check, not `comm`, if it reruns the contract command.
