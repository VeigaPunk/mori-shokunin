# CodeAuxiliary — round-22 falsification: auxiliary and direct-call contracts of `mori-retention-reconcile.py`

- Target: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-reconcile.py` (283 lines). `L<n>` = this file as read.
- Reference gate: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-gate.py` (`G<n>`).
- Governing text: `.ufo/waves/round-22/denominator-correction.md` (read first; `C<n>` = its line), `.ufo/waves/round-22/contract.md` (`K<n>`), `.ufo/waves/round-22/frozen/requirements-v2.json`.
- Frozen artifacts checked for consistency: `frozen/fixture-builder-v2.py` (`B<n>`), `oracle-reconcile-v2.py` (`O<n>`), `frozen/expected-real.json`.
- Mode: static only. Nothing executed (no tool, oracle, selftest, tests, builds, formatters). No production edits. No delegation. Tools installed or updated: none.

## Disclosure and access

- Real input was read through metadata-only projections of `.ufo/waves/round-21/evidence/final/retention-floor.json`: `argv`, `measured_revision`, `exit_code`, stderr length, key names, counts, key shapes, identity-set cardinalities, and one boolean digest equality. No hit text, matched text, or hit path was displayed.
- Git access was read-only plumbing only (`rev-parse`, `merge-base --is-ancestor`, `ls-tree`), plus `iconv` exit status on `ls-tree` output, against `/home/vgpnk/Projects/shokunin/mori-shokunin`.
- One repository-wide pattern search ran over the `mori-shokunin` root before I scoped it. Its visible hits were `.scratch/round22` fixture receipts, round-21/22 evidence, and round-22 build notes. I opened and displayed nothing under `.ufo/interactive-sessions`, `~/.omp`, Documents, private config, or shell history. That search may have enumerated such paths internally; the output cannot rule it out.
- Not done: full recomputation of the 95 real hit identities (requires executing the scan); byte-hashing of the policy and allowlist. Their equality is shown by git blob OIDs, and the receipt's policy digest is compared to the frozen value.

## Summary

| ID | Severity | Lines | Kind | Real input |
|---|---|---|---|---|
| F1 | High | L227 (inputs L200, L210–L212, L233) | Identity/scope: "raw" unallowlisted is a scanner copy; population unverifiable | Triggered: identity figure 9, emitted 4 |
| F2 | Medium-low | L79 (via L143) | Availability: strict name decode applied to every tree row | Not triggered |
| F3 | Low | L93, L98, L127 | Schema strictness where gate accepts | Not checked |
| F4 | Low | L45 | Encoding leniency vs gate strict UTF-8 | Not triggered |
| F5 | Low | L158 | Scope: empty `--repo` binds to process cwd | Not triggered |
| F6 | Low | L58, L88 | Error label; input mode allow-list | Not triggered |

## F1 — `raw_unallowlisted` is the scanner count; the raw population's unallowlisted figure is never computed or checked (High)

**Source, L227:** `'raw_unallowlisted':len(unallowed),'scanner_unallowlisted':len(unallowed)`. `unallowed` (L212) is built from `scanner` (L210), so the two keys are equal in every run by construction.

**Identity reading** (raw identities not in the allowlist, non-author hits included), computed as a set difference between `hits` (L200) and `allowed` (L211), keys `(path,line,class,line_sha256)`:

| Input | Raw identities | Raw not allowlisted (identity) | Emitted `raw_unallowlisted` |
|---|---|---|---|
| Real `retention-floor.json` | 95 | **9** | **4** |
| Synthetic valid (B47–B53, B67) | 5 | 2 (`unallowed.txt` hit, non-author file hit) | 1 |
| Synthetic forbidden (B67, B69–B71) | 5 | 4 (`unallowed.txt`, `allowed.txt` ×2, non-author file hit) | 3 |

Real-input derivation, read-only from the receipt: identity set difference of `hits` minus `allowlisted_hits` is 9. The receipt's `unallowlisted_hits` count and `metric` are 4, and `non_author` is 5. So 9 − 4 = 5 = |non-author|, which forces all five non-author identities to be non-allowlisted. The scanner list those counts rest on is identity-checked by L217–L218.

**Why this is a defect (not only a naming question):**
1. The contract makes raw and scanner populations distinct outputs (`K7`: "reports the raw population and the policy-source-excluded population distinctly"; `C7`: "Preserve raw authoritative lists"). A raw field equal to the scanner field by construction carries no raw-population information.
2. No output carries the unallowlisted population. L233 emits only `raw_hits`, `scanner_hits`, `policy_excluded_hits`. The receipt's `unallowlisted_hits` is identity-checked against the scanner list (L217–L218), so the scanner population is verified; the raw figure is compared to nothing.
3. The frozen artifacts share the same partition, so none can falsify the field. `expected-real.json` L21 pins `raw_unallowlisted: 4`. `O48` (R02 `==1`), `O52` (R11 `==3`), `O53` (R12 `==1`) are scalar predicates. `B67` and `B71` build the receipt's unallowlisted list without non-author identities, matching gate G262–G266. This is the scalar-agreement failure mode that `C5`/M1 names.
4. Alternative reading: `expected-real.json` L21 and `C5` ("raw95 partitions into 86 allowlisted + 4 unallowlisted + 5 non-author") define unallowlisted with non-author precedence. Under that reading L227 is correct and the field is a redundant duplicate. The defect is therefore that the definition is unresolved and unfalsifiable, not that the code departs from the written partition.

**Counterexample for L1:** a synthetic non-author file containing the synthetic token and no allowlist row. Identity raw unallowlisted = 2; L227 emits 1.

**Decision required:** (a) state in the contract that `raw_unallowlisted` is the scanner partition and remove the duplicate field; or (b) define it as `len(hits) - len(allowed)` (L200, L211), update `O48`/`O52`/`O53` to 2 and 4 (synthetic) and to 9 (real, instead of `expected-real.json` L21's 4), and add identity-set predicates. Under either choice, scalar predicates cannot close the gap. Option (a) would falsify this finding; option (b) requires changing the frozen expectations.

## F2 — every tree row's path is decoded strictly, so one non-UTF-8 name anywhere aborts the scan (Medium-low, latent, fail-closed)

- L79 `name=name.decode('utf8',errors='strict')` in `tree()` (L71–L82) runs for every `ls-tree -r` row. `scan()` L143 consumes all rows, and its kind filter (L144) runs after the decode.
- Gate decodes only blob paths, with `errors="replace"` (G199–G202).
- Counterexample: a tracked file whose name is the bytes `\xff.txt` at the measured revision, with no matches. Gate: scan completes. Reconciler: `Invalid('invalid_tree_path')` (L80), exit 2, for every receipt at that revision.
- Real input: not triggered. `ls-tree -r -z --name-only` at `9fb1f911…`, piped through `iconv -f UTF-8`, exits 0.
- No clearance path (fail-closed). The contract does not specify tree-path decoding. L1 should choose strict (current) or a documented replacement rule and record it.

## F3 — empty class id, empty class list, and empty receipt class are rejected where the gate accepts them (Low, latent)

- L93 `and values` rejects `classes: []`. G63–G66 check only list type.
- L98 `cid and` rejects `"id": ""`. G70–G76 check only `str`.
- L127 `and hit['class']` rejects an empty class on receipt hits. The gate's receipt path does not normalize hits.
- Counterexample: `{"schema":"mori-retention-policy-v1","classes":[],"must_redact_paths":[],"non_author_paths_glob":[]}`. Gate: exit 0, `RETENTION_CLEAN`, zero hits. Reconciler: exit 2, `policy_classes`.
- Real input: not checked (policy not opened). If the strictness is intended, the contract's "unsupported policy" clause should name these cases.

## F4 — `json.loads` runs on raw bytes, so BOM and UTF-16/32 inputs are accepted (Low, leniency)

- L45 passes bytes to `json.loads`, which auto-detects UTF-8 with BOM, UTF-16, and UTF-32. Gate `read_json` (G49–G55; decode at G52) requires strict UTF-8, and `json.loads` on a BOM-prefixed string raises.
- Counterexample: a policy, allowlist, or receipt blob starting with `EF BB BF` or encoded as UTF-16. Reconciler parses it; the gate exits 2 on the same bytes.
- Not a clearance path: an exit-2 gate receipt is rejected by L173 (`receipt_exit_type`). RFC 8259 §8.1 says UTF-8 is required for exchange and lets parsers ignore a BOM, so the BOM tolerance is in spec; the UTF-16/32 acceptance is not. Decide: strict UTF-8, as in the gate.

## F5 — an empty `--repo` binds to the process working directory (Low, scope)

- L158 `repo=Path(a.repo)`: `Path('')` is `.`. git documents `-C ""` as leaving the directory unchanged, so `git -C .` runs against the caller's cwd. Nothing checks that `--repo` is non-empty or absolute; L271 checks presence only.
- Counterexample: run `check --repo '' --rev <sha> …` from inside a different repository that contains `<sha>`. The reconciliation runs against that repository, and the output (L224–L233) carries no repository identity.
- Impact: commit, policy, and allowlist are still resolved by OID and compared, so the result is not a clearance on wrong data. It is an unvalidated identity input.

## F6 — error label and input mode allow-list (Low)

- L58: `subprocess.TimeoutExpired` is reported as `git_unavailable`. Exit 2 either way; label only.
- L88: the three input blobs must have mode `100644` or `100755`. The gate (G199) accepts any non-gitlink blob. Real input: not triggered; all three inputs are `100644` at both `9fb1f911…` and `77a5bbe8…` (checked). Latent for legacy-mode trees.

## Bounded no-findings (auxiliary and direct-call contracts)

- **`auxiliary` L131–L139:** accepts exactly the gate's forbidden and stale row shape (G242–G258: keys `finding_id, path, line=None, class, line_sha256`; kinds at G243 and G253). The duplicate rejection (L138) is unreachable for gate output, because the gate rejects duplicate allowlist keys (G153–G155; reconciler L115). Counter equality (L221–L222) matches the key-tuple shape. Real receipt: `forbidden_allowlist` 0, `warnings` 0, so both empty Counters compare equal.
- **`normalize_hits` L122–L129, `hit_key` L119–L120, `integer` L33–L34:** real receipt hit records have exactly four keys (`class,line,line_sha256,path`), 95 unique identities, numeric lines. `allowlisted_hits` and `unallowlisted_hits` are subsets of `hits` (identity subset counts 0). Bool rejection via `type(value) is int` holds (R18).
- **`scan` L141–L155 vs G89–G103 and G177–G204:** NUL skip (L148), `decode('utf8', errors='replace')` (L149), `split('\n')`, SHA-256 of `line.encode('utf-8')` (L151), and per-class `search` are identical to the gate. The per-oid cache keeps path in identity (L153), which is correct.
- **`check` partition logic L201–L215 vs G235–G288:** must-path allowlist rows are forbidden before the presence check (L205 vs G241); allowed keys come from raw hits (L201 vs G235); non-author exclusion (L208–L210 vs G260–G266); `routed` (L213 vs G268); retention code and finding precedence (L214–L215 vs G280–G288). Identical.
- **Argv binding L176–L189 for the real r21 receipt:** one `--repo` `/home/vgpnk/Projects/shokunin/mori-shokunin` (absolute); one `--rev` equal to `measured_revision` `9fb1f911…`; `--policy` and `--allowlist` absolute under the repo (relative after L186); exit_code 1; stderr empty. Unknown wrapper keys (`cwd`, `elapsed_seconds`, `started_utc`) are ignored, which the contract permits.
- **Inner binding L191–L192 for the real receipt:** `commit` equals `9fb1f911…` (verified). `policy_sha256` equals the frozen `inputs_sha256.policy` `db06e981…` (verified against the frozen value, not rehashed).
- **Revision and blob bindings L165–L170 for real input:** `9fb1f911…` is a commit and an ancestor of `77a5bbe8…` (`merge-base --is-ancestor` succeeded). Policy blob `8bf285bd…` and allowlist blob `f8be55b1…` are identical at both revisions and mode `100644`.
- **Error classification:** receipt identity inconsistencies (L189 `--rev`, L191 `commit`, L192 `policy_sha256`, L168 ancestry, L170 input drift) exit 2. Hit, count, and finding mismatches exit 1 (L217–L223). That matches the contract's "required field inconsistencies fail closed" and "valid receipt disagrees" split. The contract does not name these cases, so L1 should record the mapping.
- **`safe_path` L49–L51, `committed` L84–L89, `tree` L71–L82 (path handling):** `--` separator (L73), exact-name equality (L86), `GIT_LITERAL_PATHSPECS` (L55). No pathspec, glob, or option injection; `..`, `.`, empty components, absolute paths, and control characters are rejected.
- **`resolve` L65–L69:** `--end-of-options` (L67) and OID regex (L68). No defect.
- **`git` L53–L60:** env stripping and `--no-replace-objects` (L57). Replace refs and shallow markers are absent in the real repo (checked), so the gate and reconciler see identical blob views there.
- **`parse` L43–L47 and `no_duplicates` L36–L41:** duplicate-key and NaN/Infinity rejection are correct. The encoding leniency is F4.
- **`main` L268–L283 and `Parser` L235–L236:** subparsers are created with `type(self)`, so sub-level argparse errors route to `Parser.error` and raise `Invalid` (no `SystemExit` path). All `Invalid` codes are fixed strings, so exception text cannot reach output.
- **Output L224–L233:** `raw_hits`, `scanner_hits`, `policy_excluded_hits` carry only path, line, class, and sha. No matched text is emitted on any path I traced.
- **`selftest` L238–L266 (static only, not run):** arm 1 is consistent with exit 0 (no differences); arm 2 (`hits: []` in `wrong.json`) with exit 1; arms 3–4 with exit 2 and `RETENTION_RECONCILIATION_SETUP`.
- **Allocation and repeated work:** `git()` builds an env dict per call (L54); `committed()` runs 5 times (L160, L170); `fnmatch` runs per hit per glob (L208); `tree()` materializes output (L75). All linear and small. `scan` spawns one `git cat-file` per unique blob (L147), the same class of cost the gate pays per entry (G201). None is material.

## Verification gaps (not performed by me; for L1)

- Full recomputation of the real 95 identities and the 86 / 4 / 5 partition requires executing the scan at `9fb1f911…`. The frozen expectations are the only evidence for those counts.
- Policy and allowlist byte hashes were not computed. Their equality is shown by blob OID (both revisions), and the receipt's policy digest equals the frozen value.
- The oracle and selftest were not executed (lane rule).
- F1 must be decided before any frozen `raw_unallowlisted` expectation is treated as evidence.
