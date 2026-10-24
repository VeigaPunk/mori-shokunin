# DraftSkillSection — round 20 SKILL.md section (draft)

Status: DRAFT DELIVERED. Candidate: `.ufo/waves/round-20/build/DraftSkillSection/skill-r20.md` (29 lines, under the 40-line cap). Not merged into `SKILL.md`; L1 integrates.

## Scope and method

- Read `SKILL.md` tail (lines 301–469) and the top decision table (lines 1–22) for style: a `| Intent | Correct surface | Never | Expected output |` table, bold labelled paragraphs, exit maps in prose, and an explicit "Never" column.
- Read the frozen contract `.ufo/waves/round-20/contract.md` (C1 drift re-pin, C2 settlement scan) and the frozen oracle `.ufo/waves/round-20/frozen/c2-expected.json` (14 cases, including `no_vocab` = dead/failed/killed).
- Confirmed `tools/mori-wave-settlement.py` does NOT exist at this tree (glob: path not found). The section is therefore written against the contract and oracle, not against observed tool output. Output field names beyond those in the contract are not used. [INFERENCE: tool lands via C2 integration.]
- Did not run `tools/mori-census.sh` (bounds: heavy CPU, L1 only). The census SHA `87b8d680…ab28` and the `comm` recipe are copied from the contract, not re-measured here.

## Findings embedded in the draft

- `settled`/`no-spawn` → exit 0; `partial`/`unsettled`/`unavailable` → exit 1; usage or unreadable root → exit 2 (contract §C2, oracle cases `all-present`, `no-spawn`, `one-missing`, `none-present`, `traversal`).
- `empty` (size 0), `misrooted` (fleet-root only) and `unsafe`/`unparsed` are all counted as not present (oracle `empty-report`, `misrooted`, `no-trailer`, `traversal`, `absolute-path`).
- Premature-settlement guard is the existing SKILL.md rule (`SKILL.md` "Premature-settlement guard", ~line 370): age the wave first. The draft points at the census `SURFACE waves` age rather than naming a tool field the contract does not specify.
- Drift ritual is the contract's C1 sequence verbatim in order: measure → unclassified count must be 0 → classify (closed four-class set, evidence pointer per token) → any `census-regression` blocks the pin → `--pin baseline-r20-<UTC>.json` → re-run `--drift` and record the result whatever it is. `--pin` writes only its path; `--drift` writes nothing (SKILL.md "Drift pin (r10)" ~line 281).

## Items for the integrator

1. Once `tools/mori-wave-settlement.py` lands, verify the `Expected output` column against the real `mori-wave-settlement-v1` JSON. Any field name not present in the tool must be removed from the section, not kept.
2. The `--out FILE` and `--fleet-root` flags are taken from the contract's usage line; confirm them against the `--help` of the landed tool.
3. The section says "byte-identical on re-run"; that is the contract requirement and the oracle `deterministic` case, not an observed result.
4. The r10 baseline line in the draft (`baseline-r10-20261015T2231Z.json`) matches the path in `SKILL.md` line 299 and the contract; no re-measurement was done.

## Tooling

No installs or updates performed. No pacman transactions (host guard active). No network use.

## Out of scope / not touched

- No edits to `SKILL.md`, `tools/`, any baseline, the census, MANIFEST, or git/jj state.
- No subagents dispatched (leaf seat).
- No retained interactive-session transcripts or `~/.omp` session logs opened.

Checks for the main agent to run once: `wc -l` on the draft (≤40) and the C2 oracle against the landed tool; the C1 `comm` count on the round-20 register (expected 0). I did not run either.
