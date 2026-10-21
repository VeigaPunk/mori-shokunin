# ReportContract — SHONEN four boxes + round22 report/CLI contract (assertion-only draft)

Seat `MoriR22.ReportContract`, scout. Scope is limited to `SHONEN.md`, the files it names (`SKILL.md`,
`LOG.md`, `PROVINCE.md`), `.ufo/waves/round-22/{contract.md,frozen/requirements.json}`, and the
evidence the contract names directly: the r21 receipt `.ufo/waves/round-21/evidence/final/retention-floor.json`,
its policy and allowlist blobs, and `tools/mori-retention-gate.py`, whose semantics the contract says must
be reproduced. I did no outside verification and ran no tests, builds, linters, selftests or gates. The only
commands were read-only `git -C <lane> show/ls-tree/log/rev-parse/merge-base/cat-file` plumbing, plus
in-process JSON shape and count extraction on the outputs. I printed no matched text. Lane tip at
read time: `306e06ecd02e0ea8e544fbd30d1ff7e7359c581e`. The entering commit `77a5bbe8…` is its ancestor.
Tool installs and updates: none.

LSP note: no `lsp` device was available to this seat. The symbol locations below come from direct reads of
`tools/mori-retention-gate.py` at the worktree, so they are textual and not semantic proof.

## 1. SHONEN four boxes (assertions about what the files claim; nothing scored)

| Box | Observed in file | Assessment (assertion only) |
|---|---|---|
| SKILL.md has real decision tables, error patterns, checklists and cited sources | `SKILL.md:11` Decision table, `:23` Error patterns, `:149` Checklist (executable), `:156` Gates registry; cited upstream URLs, e.g. `:30` (kernel `oom_kill.c` v7.2, systemd `oomd-util.c` v261) | The structure is present. SKILL.md has **no** row for the round22 reconciler (absent at HEAD: `git cat-file -e HEAD:tools/mori-retention-reconcile.py` failed). The r18 retention gate row is at `:178`. A reconciler registry row and decision-table row would be L1 integration work after measurement. |
| At least one end-to-end domain task executed and logged in LOG.md | `LOG.md:1413` "Round21 final measured outcome" binds measured commit `9fb1f91…`, its argv/digests and the evidence directory | LOG.md asserts this. I did not verify it. Round22 has only a declaration so far (`LOG.md:1442-1457`) and no measured outcome. |
| Instructions executable by an agent without oral context | `SKILL.md:149-154` checklist and per-gate entry/verdict/selftest columns | Asserted for existing gates. For round22, section 2 finds a contract value (5 policy hits, scanner 90) that cannot be reproduced from the named artifacts under the contract's own exact-path rule. That is an oral-context dependency until it is reconciled. |
| No cross-domain bleed (PROVINCE.md still accurate) | `PROVINCE.md:125-131` (r18): mori owns the retention gate over its *own* committed evidence. Exposure assessment, rotation and history rewrite belong to kagi/operator. | The round22 contract keeps `privacy_clearance=false` and allows no actuation or history rewrite (`contract.md:16`), so it stays inside the r18 boundary. PROVINCE has no round22 note yet. I observed no bleed. |

## 2. Report/CLI contract vs the committed receipt (observed facts)

### 2.1 Receipt wrapper shape (`retention-floor.json`, blob at HEAD = blob at `77a5bbe`)

- Top-level fields: `schema`=`mori-r21-command-receipt-v1`, `measured_revision` (40-hex `9fb1f911cfdd6061005c300795f44b1b45523897`), `argv` (11 items), `cwd` (equals the lane root), `started_utc`, `elapsed_seconds` (float), `exit_code`=1 (int), `stdout` (29662 chars of JSON) and `stderr` (empty). All five required fields from `contract.md:11` are present. `cwd`, `started_utc` and `elapsed_seconds` are "unknown fields" the contract says need not be rejected.
- Receipt provenance: the receipt blob is **absent at the measured revision** `9fb1f91` and was first committed in `77a5bbe`. Any valid `--rev` must therefore be `77a5bbe` or a descendant. `9fb1f91` is a strict ancestor of HEAD (observed with `merge-base --is-ancestor`).
- `stdout` JSON keys: `allowlisted_hits`, `commit`, `finding_id`, `forbidden_allowlist`, `hits`, `metric`, `non_author`, `policy_sha256`, `routed`, `unallowlisted_hits`, `warnings`. `commit` equals `measured_revision`. `finding_id`=`RETENTION_FINDINGS`.
- Hit records have exactly `path`, `line` (all int, no bool), `class` and `line_sha256`. The receipt contains no duplicate hit identities.

### 2.2 Counts on the receipt (identity arithmetic, not subtraction alone)

| Quantity | Value |
|---|---|
| `hits` (raw) | 95 across 32 distinct paths |
| `allowlisted_hits` | 86, a subset of raw |
| `unallowlisted_hits` / `metric` | 4 / 4, a subset of raw, disjoint from allowlisted; all at one path, the round-20 falsify **copy** of the policy file (`.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`) |
| `non_author` (int count only, **no identity list**) | 5. Raw minus allowlisted minus unallowlisted leaves exactly 5 identities: 3 in `corpus/lessons/round-17-verifier-spotcheck.md` and 2 in `corpus/lessons/round-18-verifier-spotcheck.md`. Both match the policy glob `corpus/lessons/round-*-verifier-spotcheck.md`. |
| `forbidden_allowlist`, `warnings`, `routed` | 0, 0, 0 |
| Raw hits at the **exact supplied policy path** `.ufo/waves/round-18/frozen/c1-policy.json` | **4**, all allowlisted, 0 unallowlisted |
| Class histogram (labels only) | R2:3, R4:8, R5:14, R6:37, R7:10, R8:8, R9:15 |

### 2.3 Load-bearing discrepancy: the declared 5 / 90 vs the exact-path rule

`contract.md` says "raw95 (incl5policy) versus90 (scanner)" (`:21`), and the Open-debt clause repeats "raw95 includes5policy source hits, scanner90". `LOG.md:1446-1447` says "raw95 / policy-excluded5 / scanner90". The contract also requires that "Policy-excluded means exactly the supplied policy path, never broad regex/path exclusions" (`contract.md:13`).

Against the committed receipt, the exact-path rule gives **policy_excluded=4, scanner_total=91, raw_unallowlisted=4, scanner_unallowlisted=4** (none of the 4 policy-path hits is unallowlisted). The number 5 instead matches `non_author=5`, which is a different partition: the two verifier-spotcheck lesson files, not the policy path. The difference 95−90=5 therefore cannot come from removing the exact policy path. [INFERENCE] The "scanner90" figure may come from the operator's r21 closure census, which applied a different exclusion such as non-author globs, a second policy copy, or another scanner population. This seat did not open that census because the contract does not name its path. Whether the reconciler should report 4/91, or the contract should be amended, is L1's call. **Freezing 5/90 as expected real values would contradict the exact-path rule.** R03 (synthetic 5/1/4) is unaffected. I sent a one-line notice to `agent://MoriR22`.

### 2.4 Policy/allowlist byte stability (contract `:11`, R15/R16 inputs)

| Rev | policy blob sha256 | allowlist blob sha256 | modes |
|---|---|---|---|
| `9fb1f91` (measured) | `db06e981…3128` | `f46c78ec…c63b` | 100644 / 100644 |
| `77a5bbe` (entering) | same | same | same |
| HEAD `306e06e` | same | same | same |

The receipt's `policy_sha256` equals the policy blob digest `db06e981…`. The receipt records **no allowlist digest**, and its argv passed **absolute worktree paths** for `--policy` and `--allowlist`. The existing gate reads both via `read_json(args.policy)` and `read_json(args.allowlist)` (`tools/mori-retention-gate.py:310-320`), that is from the worktree and not from Git blobs. So blob equality at the measured and input revisions is checkable for both files, but which allowlist bytes the gate actually loaded at measurement time is not authenticated by the receipt. [INFERENCE] A dirty worktree at measurement could not be detected from this receipt alone.

## 3. Existing-gate semantics the independent recomputation must reproduce

All from `tools/mori-retention-gate.py` at the worktree, read textually:

1. **Tree walk** (`:177-204`): the revision is resolved via `cat-file --batch-check` on `<rev>^{commit}`, then `ls-tree -r -z --full-tree`. It skips non-blob entries and mode `160000`. **Symlink entries (mode `120000`, kind blob) are scanned**, so their target text is matched. Paths are decoded UTF-8 with `errors=replace`.
2. **Blob lines** (`:89-103`): a blob containing `\0` anywhere yields no hits (R22). Text is decoded UTF-8 with `errors=replace`. Lines come from **`text.split("\n")`, 1-based**, not `splitlines()`, which would also split on `\r`, `\v`, `\f`, `\x1c-\x1e`, `\x85` and U+2028/2029 and shift line numbers. Each class regex uses `.search` per line, so one line can yield several class hits. `line_sha256` is the sha256 of the replaced-decoded line re-encoded as UTF-8, without the `\n`.
3. **Allowlist key ignores line number** (`:235-261`): the key is `(path, class, line_sha256)`. One allowlist row therefore covers every same-key hit on any line, and duplicate-content lines are all allowlisted.
4. **Forbidden rows** (`:241-248`): an allowlist row whose path is in `must_redact_paths` becomes `allowlist_forbidden` and is **never added to `allowed_keys`**. Hits there stay unallowlisted (R11) and count toward `routed` (`:268`).
5. **Partitions are not disjoint by construction**: `allowed_hits` is computed **without** excluding non-author paths (`:261`), while `unallowlisted_hits` excludes them (`:262-266`). A non-author hit that is also allowlisted appears in `allowlisted_hits` *and* in the `non_author` count. In this receipt they happen to be disjoint. R12 recomputation must therefore glob-match non-author paths directly, not derive them as raw−allowlisted−unallowlisted.
6. **Glob**: `fnmatch.fnmatch` (`:121-122`), where `*` crosses `/`. On posix, `normcase` is the identity, so it equals `fnmatchcase`.
7. **Stale rows** (`:251-258`): non-forbidden rows with no matching hit become `warnings` with `allowlist_stale`.
8. **finding_id precedence** (`:280-287`): `allowlist_forbidden` > `RETENTION_FINDINGS` (metric>0 or population mismatch) > `allowlist_stale` > `RETENTION_CLEAN`. **Exit code** (`:288`) is 1 if metric, forbidden rows or population mismatch, else 0. The receipt's exit 1 / `RETENTION_FINDINGS` with metric 4 is consistent with this rule, which supports R02 (reconciliation exit 0 while `retention_state=red`).
9. **Allowlist container**: the allowlist value may be a dict with a `rows` key (`:317-319`).
10. **Policy schema**: `mori-retention-policy-v1`, keys including `classes`, `must_redact_paths` (3 entries) and `non_author_paths_glob` (2 globs) (`:64-86`).

## 4. Contract gaps and ambiguities (decisions for L1, not resolved here)

- **G1 (high):** the 5/90 vs 4/91 conflict in §2.3.
- **G2:** "ancestor of input revision" (`contract.md:11`) does not say whether equality is allowed. `git merge-base --is-ancestor` accepts equal commits. In practice the receipt is absent at `9fb1f91`, so equality is never valid for this receipt.
- **G3:** the contract requires `--policy`/`--allowlist` as REPO_REL Git blobs, but the receipt's argv carries absolute worktree paths and `cwd`. The contract does not say whether the reconciler must cross-check argv (`--repo`, `--rev`, `--policy`, `--allowlist`, after stripping `cwd`/`--repo`) against its own inputs. Without that check, a receipt produced with a different policy file but the same digest-less allowlist could reconcile.
- **G4:** the receipt binds no allowlist digest (§2.4). R16 can only prove input/measured blob equality, not what the gate loaded.
- **G5:** `non_author` in the receipt is a count, not identities. R12 can validate the count and the derived set only through item 5 of §3, which is exact for this receipt and not guaranteed in general.
- **G6:** the contract requires the new tool's output to carry loaded-input SHA256, executing-tool SHA256, resolved commits and argv (`contract.md:11`, R24). The r21 receipt itself has none of the tool or input digests except `policy_sha256`. R24 must therefore be read as a property of the reconciler's output, not as a validation of the old receipt.
- **G7:** `frozen/requirements.json` lists only the IDs R01–R24, `before_kind=capability_absent`, and `contract_sha256=1658c390…a1a1`. That digest matches `contract.md` at `df880b4` and at HEAD. It holds **no expected values and no fixture generator**, which `contract.md:18` says must be committed before implementation integration. At HEAD they are not committed yet. Observed: only `requirements.json` exists under `round-22/frozen/`, per the `df880b4` stat.

## 5. Confidence and unknowns

- High confidence: the receipt shape, counts, partition identities, policy-path count 4, byte stability and gate line references (direct reads, metadata only).
- Medium: the inference that "5" is the `non_author` partition. The counts match, but the operator's r21 closure census was not opened.
- Unknown: which population "scanner90" was measured on; the allowlist bytes actually loaded at r21 measurement; whether L1 amends the contract or reports 4/91. No privacy or history clearance is implied by anything above. The four unallowlisted hits remain red.
