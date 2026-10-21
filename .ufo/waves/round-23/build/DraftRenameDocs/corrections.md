# DraftRenameDocs — append-only corrections for the C1 schema v2 cutover

Seat: `MadoR22-2.DraftRenameDocs-8` (scribe, leaf; no subagent dispatch, no delegation).
Authority: `.ufo/waves/round-23/contract.md` §C1, frozen at lane commit
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8` (contract sha256
`2bb35aefb08d3fafc467260f859453c0f096effe18b2446503f2b2ee87fe69e7`, matching
`frozen/c1-requirements.json.contract_sha256`).
Frozen evidence named by the contract:
`frozen/c1-requirements.json` (sha256 `88e1b912df1a8d5f3ad3da6a9fd3fec751cab7776919c77a8aa83365f84f3184`),
`frozen/c1-expected-real.json` (sha256 `f8e111a5c4d1e8ca00a32b8e96db7986798def8b76d2c8b5275b0feb7fa41bba`),
`oracle-rename.py` (sha256 `a55b2b50d3e7447a1d5312c8b066a13137a6a6895f0343b3240ebf081d97c5f2`).
Tool installs: none (no install, no upgrade, no service touch).

## What this document is

Two **append-only** correction blocks, one per named documentation surface. Nothing
existing is rewritten: each block is added *after* the retained text, which stays
byte-identical (QUALITY #4, "Errata are append-only blocks",
`corpus/QUALITY.md:6`; precedent `.ufo/waves/round-22/denominator-correction.md`).
This seat does not edit `SKILL.md` or `corpus/knowledge/retention-reconciliation-r22.md`;
it drafts the correction text for the seat that owns those files (registry rows:
`DraftSkillRows`; corpus note: `DraftKnowledge`) and for L1's integration.

## Anchor map (at lane commit `4dc80c1`, `git -C <lane> rev-parse HEAD`)

| Surface | Anchor | Existing text (retained unchanged) |
|---|---|---|
| `SKILL.md` | `:556-564` — last paragraph of the "Round22 retention receipt reconciliation" section, file ends at `:564` | "Field caveats (wave2 FinalR02/NoHarm): `raw_unallowlisted` and `scanner_unallowlisted` are one existing gate metric reported twice (both exclude non-author hits)…" |
| `corpus/knowledge/retention-reconciliation-r22.md` | `:27-36` — "Exact populations" paragraph; `:35` starts the sentence the correction addresses, `:36` closes the paragraph (the assignment's named range `:27-35` covers the alias sentences; the sentence runs one line past it) | "The output's `raw_unallowlisted` and `scanner_unallowlisted` intentionally name the same existing policy-filtered metric, not two independent counts. … the frozen field name `raw_unallowlisted` keeps its frozen alias meaning (4) rather than being silently redefined." |

Insertion points are **end of file** for `SKILL.md` (new paragraph after `:564`) and
**end of the "Exact populations" section** for the corpus note (new block after `:36`,
before the blank line and `## Provenance limits` at `:38`).

## Correction block A — append to `SKILL.md` after line 564

```text
Round23 correction (append-only; schema v2 cutover, C1): the reconciler's output
schema is `mori-retention-reconciliation-v2` in every output — check, setup error
and selftest alike. The key `raw_unallowlisted` is removed from every output
(clean cutover, no alias). The in-scope (non-author-filtered) unallowlisted count
is now read from `scanner_unallowlisted` alone; `raw_not_allowlisted` is the raw
complement (raw identities with no allowlist row outside `must_redact_paths`),
unchanged in meaning. The caveat paragraph above described schema v1, where
`raw_unallowlisted` and `scanner_unallowlisted` were one metric reported twice;
against v2 outputs read the in-scope count from `scanner_unallowlisted` and the
raw complement from `raw_not_allowlisted` (9 on the r21 receipt, 95−86). On the
r21 receipt at `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0` the v2 output is exit0
`RETENTION_RECONCILED` with `scanner_total` 90, `scanner_unallowlisted` 4,
`raw_not_allowlisted` 9, `raw_total` 95, `allowlisted` 86, `policy_excluded` 5,
`retention_state` red and `privacy_clearance` false. No other output key, value,
exit code or finding id changes; the r22 evidence artifacts stay byte-unchanged,
the r22 claim stays reproducible at its bound revision
`da40bb20f81da125d798f73cd1653655be1255ca`, and the four unallowlisted hits,
original permission control RED 11/12, two unknown historical dispositions and
blocked baseline acceptance carry unchanged. Nothing here is privacy clearance.
```

## Correction block B — append to `corpus/knowledge/retention-reconciliation-r22.md` after line 36

```text
## Round-23 correction — schema v2 removes the `raw_unallowlisted` alias (append-only)

The sentences above at `:27-36` describe schema `mori-retention-reconciliation-v1`
and stay true of the r22-bound revision `da40bb20f81da125d798f73cd1653655be1255ca`
and of the byte-unchanged r22 evidence artifacts; they are not rewritten here.
Under the C1 cutover (schema `mori-retention-reconciliation-v2`, in every output:
check, setup error, selftest) the key `raw_unallowlisted` is removed from every
output, with no alias. The in-scope unallowlisted count — the value the removed
key carried — is now read from `scanner_unallowlisted` alone, and the raw
complement from `raw_not_allowlisted`, whose meaning is unchanged: raw identities
whose `(path,class,line_sha256)` is in no allowlist row outside `must_redact_paths`.
On the r21 receipt at `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0` the v2 output is
exit0 `RETENTION_RECONCILED` with `raw_total` 95, `allowlisted` 86,
`scanner_total` 90, `policy_excluded` 5, `scanner_unallowlisted` 4,
`raw_not_allowlisted` 9 (95−86), `retention_state` red, `privacy_clearance` false
and no `raw_unallowlisted` key. No other output key, value, exit code or finding
id changes. Consequence, declared not hidden: the r22 frozen oracle
`oracle-reconcile-v2.py` (R02/R11/R12 read the removed key) and `measure-round22.py`
(output whitelist `:20`, and `frozen/expected-real.json:21` pins
`"raw_unallowlisted": 4`) no longer pass against post-C1 tool revisions; the r22
claim stays reproducible at its bound revision
`da40bb20f81da125d798f73cd1653655be1255ca`. The r23 oracle re-expresses all 24 r22
requirements against v2 (`R02`/`R11`/`R12` read `scanner_unallowlisted` with the
same expected values 1/3/1; `R25` requires schema v2 and the absence of the removed
key in every parsed oracle run; `R26` requires `raw_not_allowlisted` to equal an
independent identity-level count — 2 on the synthetic `valid` arm, 4 on the
`forbidden` arm). The four unallowlisted hits, original permission control RED
11/12, both unknown historical dispositions and blocked baseline acceptance carry
unchanged; this correction is calibration of one output key and grants no privacy
clearance.
```

## Read-only evidence behind the numbers cited above

All observed by read-only file reads and read-only `git` plumbing at lane commit
`4dc80c1`; no test, build, linter, formatter, gate or reconcile run was executed,
and no file outside this seat's two assigned outputs was written.

| Fact | How observed |
|---|---|
| `SKILL.md` = 564 lines; `:556` is the "Field caveats" paragraph; `:564` is the last line | `awk 'NR>=528'` over `SKILL.md` |
| corpus note = 42 lines; `:27-36` is the alias paragraph; `:38` starts `## Provenance limits` | `awk 'NR>=24'` over `corpus/knowledge/retention-reconciliation-r22.md` |
| Tool still emits v1 (`SCHEMA='mori-retention-reconciliation-v1'`, `tools/mori-retention-reconcile.py:16`) and still emits `raw_unallowlisted` beside `scanner_unallowlisted` (`:234`), with `raw_not_allowlisted` already present (`:235`) | `git grep -n` over the tracked tool |
| r21 receipt (`77a5bbe8a0b41dfbfd2546d024d36e294b814bd0`) inner commit `9fb1f911cfdd6061005c300795f44b1b45523897`: `hits` 95, `allowlisted_hits` 86, `unallowlisted_hits` 4, `metric` 4, `non_author` 5 | field-projection of `.ufo/waves/round-21/evidence/final/retention-floor.json` |
| Independent identity-level recount from the committed receipt + allowlist + policy bytes: raw 95, allowlisted identities 86, **raw_not_allowlisted = 9** (forbidden `must_redact_paths` rows excluded from the allowlist set) | python3 over `corpus/evidence/retention-allowlist.json`, `.ufo/waves/round-18/frozen/c1-policy.json`, the r21 receipt |
| Input digests recomputed equal `frozen/c1-expected-real.json.inputs_sha256`: receipt `4001e2d9…`, policy `db06e981…`, allowlist `f46c78ec…` | `sha256sum` |
| r22 frozen oracle reads the removed key in R02/R11/R12 (`.ufo/waves/round-22/oracle-reconcile-v2.py:48,52,53`); r22 driver key whitelist lists it (`measure-round22.py:20`) and the frozen real expectation pins `"raw_unallowlisted": 4` (`.ufo/waves/round-22/frozen/expected-real.json:21`) | `git grep -n` |
| r22 driver stages the tool from the measured revision (`git show <rev>:tools/mori-retention-reconcile.py`, `measure-round22.py:59`), so the r22 claim stays reproducible at `da40bb20f81da125d798f73cd1653655be1255ca` (ancestor of HEAD, `git merge-base --is-ancestor` → 0) | read-only `git` plumbing |
| r23 oracle: `misleading_alias_runs` counts parsed oracle runs whose JSON contains `raw_unallowlisted` (`oracle-rename.py:82`); `schema_v2_runs` counts `schema == mori-retention-reconciliation-v2` (`:83`); R25 requires both to hold for every parsed run (`:85`); R26 recomputes `raw_not_allowlisted` independently from the fixture's committed allowlist/policy bytes (`:66-76`, expected 2 on `valid`, 4 on `forbidden`) | `oracle-rename.py` (read) |

## No-harm scope of these corrections

- The correction text states only the C1 rename/deprecation and the schema bump.
  It introduces no new claim, frontier row, retirement, promotion, waiver, privacy
  clearance, pin or baseline acceptance.
- The retained v1 sentences are left in place and are scoped by the correction to
  the r22-bound revision and the byte-unchanged r22 evidence; they are not
  contradicted, only qualified by date and schema.
- Debt carried unchanged by both blocks: four unallowlisted retention hits,
  original permission control RED 11/12, two unknown historical dispositions,
  blocked baseline acceptance, `privacy_clearance` always false.
- Out of scope for these two blocks (other seats / later pass): the registry row
  `SKILL.md:538` (round-22 gate row and its frozen-artifact pointers),
  `corpus/README.md:420` (coverage-map row for the r22 note), the r23 knowledge
  note and lesson rows, and the r22 wave's own frozen/evidence artifacts, which
  stay byte-unchanged historical evidence.

## Integration checklist for the owner of these files

1. Append block A as a new paragraph at the end of `SKILL.md` (after `:564`); do
   not touch `:556-564`.
2. Append block B as a new section at the end of the "Exact populations" section of
   `corpus/knowledge/retention-reconciliation-r22.md` (after `:36`); do not touch
   `:27-36`.
3. After both appends, `git diff` must show additions only for those two files
   (no `-` lines inside the anchored ranges).
4. Re-run the r23 C1 oracle (`oracle-rename.py`) against the post-C1 tool: expect
   `misleading_alias_runs` 0, `schema_v2_runs` = parsed runs, 26/26 requirements,
   and the real control to match `frozen/c1-expected-real.json`
   (`scanner_unallowlisted` 4, `raw_not_allowlisted` 9, `raw_total` 95,
   `allowlisted` 86, `policy_excluded` 5, `scanner_total` 90, `retention_state`
   red, `privacy_clearance` false, exit 0 `RETENTION_RECONCILED`,
   `forbidden_keys: ["raw_unallowlisted"]`).
