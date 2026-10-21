# CodeCommitted: committed function and direct-call audit of tools/mori-retention-reconcile.py

## Scope and method

- Target: `tools/mori-retention-reconcile.py` at HEAD `50b6f75`. Committed blob sha256 `08dc3c5104ff891c1a2edbaa21aea84bd71acdadbd5f30d45c93558068126987` equals the worktree file; no staged or unstaged diff.
- Read first: `.ufo/waves/round-22/denominator-correction.md`. Also read: `contract.md` (CLI, evidence and R01–R24 text), `frozen/requirements-v2.json`, `frozen/fixture-builder-v2.py`, `oracle-reconcile-v2.py`, the existing gate `tools/mori-retention-gate.py` (the source of truth for receipt semantics), and the R21 receipt `round-21/evidence/final/retention-floor.json`.
- Method: static reading only. Nothing was executed: no selftest, builder, oracle, test, build, or linter. Real-data numbers are read as fields of the R21 receipt with a read-only JSON filter. No matched text is reproduced.
- Line numbers refer to the file above, unless marked "gate".

## Verdict

- One identity defect with an explicit output-field counterexample (F1). It is medium severity and reproducible from the fixture and from real receipt fields.
- The remaining findings are narrow divergences from the gate or direct-call provenance issues (F2–F8). None changes the 0/1/2 accounting decision for the inputs examined.
- The receipt-visible accounting path (lines 157–233) matches the gate's `_scan_result` (gate 235–288) for every receipt-visible field: hits, unallowlisted, allowlisted, forbidden, warnings, metric, routed, non_author, finding_id, exit code, and the commit and policy digest bindings.

## Findings

### F1 (medium): `raw_unallowlisted` carries the scanner population, so the raw identity breaks

- Source: line 210 defines `scanner`; line 212 defines `unallowed` from `scanner`; line 211 defines `allowed` from the raw `hits`; line 227 emits `'raw_unallowlisted':len(unallowed)`. Line 227 also emits `'scanner_unallowlisted':len(unallowed)`.
- The two output fields are the same variable, so they can never differ for any input.
- Within one output, `raw_total == allowlisted + raw_unallowlisted` must hold, because `allowed` and its complement partition `hits` exactly. Line 227 breaks that identity.
- Counterexample 1 (synthetic `valid` variant; `fixture-builder-v2.py` lines 40–43, 54, 60): raw hits are 5 (policy.json 1 allowlisted; allowed.txt 2 allowlisted; unallowed.txt 1; non-author.txt 1 not allowlisted). The tool emits `raw_total=5`, `allowlisted=3`, `raw_unallowlisted=1`. The raw complement is {unallowed.txt hit, non-author.txt hit}, which is 2. So 5 ≠ 3 + 1.
- Counterexample 2 (real R21 receipt, measured `9fb1f911…`): the receipt's own fields are `hits`=95, `allowlisted_hits`=86, `unallowlisted_hits`=4, `non_author`=5, `metric`=4. The raw complement is 95 − 86 = 9 = 4 + 5, so all five non-author identities are unallowlisted. Line 227 yields 4 for this input.
- The frozen v2 spec encodes the same collapse, so the SUT passes it while the defect stays hidden:
  - `fixture-builder-v2.py` line 104: `'expected_raw_unallowlisted':3 if forbidden else 1`.
  - `oracle-reconcile-v2.py` line 48 (R02: `raw_unallowlisted==1`), line 52 (R11: `==3`), line 53 (R12: `==1`).
  - Under raw-authoritative semantics (correction and contract line 13: "the raw denominator remains authoritative"), the expected values are 2 for valid (R02, R12), and 4 for the forbidden variant (R11).
  - This is the M1 class of error: scalar agreement without population identity.
- Whichever semantics L1 chooses, the current output is wrong. Either `raw_unallowlisted` is raw-scope (`len(hits)` minus `allowed_keys`), or the field must be removed and the contract's "raw/scanner" pair reduced to one field. Changing it requires re-freezing builder line 104 and oracle lines 48, 52 and 53 first.

### F2 (low): direct-call `check` echoes process argv, not the invocation

- Line 233: `'argv':sys.argv[1:]`. `main(argv=None)` (line 268) parses the passed argv (line 272), but `check(a)` reads `sys.argv` instead.
- Counterexample: from an interpreter whose `sys.argv` is `['-c']`, calling `main(['check','--repo',R,'--rev',REV,'--receipt','receipt.json','--policy','policy.json','--allowlist','allowlist.json'])` returns `"argv":[]`. R24 requires the invocation argv to appear.
- The CLI path is unaffected because the process argv equals the passed argv.
- Direction: pass the parsed argv into `check`, for example by attaching it to the namespace in `main`.

### F3 (low-medium): tracked names are decoded strictly; the gate uses replacement

- Line 79: `name.decode('utf8',errors='strict')`, with line 80 raising `Invalid('invalid_tree_path')`. `scan` (line 143) decodes every tree row, so one non-UTF-8 tracked name makes every `check` on that revision exit 2.
- Gate line 202: `path_bytes.decode("utf-8", errors="replace")`, and gate line 203 still scans the blob.
- Counterexample: a tracked blob whose name bytes are `0xFF` followed by `.txt`, containing the token. The gate records a hit; this tool returns SETUP for every receipt on that revision.
- Contract line 13 asks for the gate's population ("every tracked blob … split newline exactly as existing retention gate"). Strict name decoding is an unrequested divergence. Direction: `errors='replace'`, or declare exit 2 in the spec.

### F4 (low): empty policy classes and empty class ids are rejected where the gate accepts them

- Line 93: `require(isinstance(values,list) and values,'policy_classes')`. Line 98 requires a non-empty class `id`.
- Gate lines 66–67 check only the type of `classes`. Gate line 71 checks only `str`.
- Counterexample: policy `"classes": []`. The gate returns exit 0 `RETENTION_CLEAN` for any tree; this tool returns exit 2 `policy_classes`.
- Acceptable only if L1 classifies an empty class set as "unsupported policy" under the exit-2 text. That needs an explicit decision.

### F5 (low): JSON byte parsing differs from the gate's `read_json`

- Line 45: `json.loads(data, …)` on bytes auto-detects UTF-16/UTF-32 and accepts a UTF-8 BOM. Line 39 rejects duplicate keys. Line 45 `parse_constant` rejects NaN and Infinity.
- Gate line 52: `json.loads(raw.decode("utf-8"))`. It is UTF-8 only, rejects a BOM, takes the last value for duplicate keys, and accepts NaN.
- Counterexample A (accepts more): UTF-16-LE policy bytes parse here and the gate rejects them. A fabricated receipt with a matching `policy_sha256` would pass; the gate could never have produced it.
- Counterexample B (rejects more): a policy with a duplicate `"schema"` key whose last value is valid. The gate accepts it; this tool raises `duplicate_json_key` and exits 2.
- Direction: decode strictly as UTF-8, parse the str, and choose the duplicate-key policy explicitly.

### F6 (low): argv binding rejects some gate-valid forms, and ignores the recorded cwd

- Line 178: `argv.count(flag)==1` rejects `--policy=…` forms that the gate's argparse accepts. The result is SETUP.
- Line 187: `safe_path(recorded)` rejects `./policy.json` because of the `.` component. The gate accepts it. The result is a false SETUP.
- Lines 185–187 bind a relative recorded path to the repo root. The wrapper's `cwd` field is not consulted; real R21 wrappers carry it (`retention-floor.json`, top-level `cwd`). The receipt has no allowlist digest (only `policy_sha256`, line 192), so a relative `--allowlist` recorded under another cwd binds to the committed file without verification.
- Real R21 receipts use absolute paths under the repo root (verified in `retention-floor.json` argv), so no current real receipt is affected.

### F7 (low): an empty `--repo` silently binds to the current directory

- Line 158: `repo=Path(a.repo)`. `Path('')` is `'.'`, so `git -C .` reads the current directory's repository. This should be SETUP.

### F8 (low): timeouts are reported as `git_unavailable`

- Line 57 sets `timeout=60` for each git call. Line 58 maps `TimeoutExpired` to `Invalid('git_unavailable')`. A timeout is reported as unavailability, which misleads the operator. The contract has no timeout text.

### F9 (performance note, not blocking): one git process per distinct blob

- Line 147 runs `git cat-file blob` once per distinct blob. Tracked entries at HEAD number 7,900 (`git ls-files` count), so a check can spawn up to about 7,900 processes.
- The gate does the same (gate line 201) and has no oid cache. This is parity, not a regression. It costs runtime only; one `cat-file --batch` stream would remove the spawn cost.

## Bounded no-findings (checked against current source)

- `require` and `integer` (lines 27–34): `type(value) is int` rejects `True` for line, metric and exit_code.
- `no_duplicates` and `parse` (lines 36–47): `Invalid` is not a `ValueError` subclass, so the duplicate-key and constant Invalids propagate with their reasons.
- `safe_path` (lines 49–51): rejects absolute paths, empty components, `.`, `..`, controls and DEL.
- `git` (lines 53–60): strips `GIT_*`, sets `--no-replace-objects`, `GIT_LITERAL_PATHSPECS`, `GIT_NO_LAZY_FETCH`. `ls-tree` path (line 73) is literal, and the exact single-row check (line 86) means glob arguments cannot be accepted by accident.
- `resolve` (lines 65–69): `--end-of-options`, full-OID regex, peel to commit.
- `committed` (lines 84–89): only mode 100644/100755 blobs. Symlinks (120000) and gitlinks (160000) are rejected, as R21 requires.
- `policy_rules` (lines 91–105): schema check; duplicate ids rejected (line 98); must/non-author type checks match gate lines 82–85; regex compile errors are caught (line 100).
- `allow_rows` (lines 107–117): exact key set; class must be known; sha regex; non-blank reason; rule in {a, b, c}; duplicate key rejected. The dict-with-`rows` form is accepted exactly as gate lines 318–319.
- `normalize_hits` and `auxiliary` (lines 122–139): field sets equal the gate's emitted sets (gate 111, 246–247, 289–301). The real R21 receipt's stdout keys include every required key.
- `scan` (lines 141–155): NUL skip (line 148 matches gate 90–91); replacement decode (line 149 matches gate 92); `split('\n')` (line 149 matches gate 94); `search` (line 151 matches gate 96); digest of the replaced line (line 151 matches gate 101); kind filter (line 144 matches gate 199 for gitlinks); symlink blobs are scanned on both sides; the oid cache (line 146) changes no result.
- `check` validation (lines 157–199): peel (165), ancestor (168), policy and allowlist byte equality at measured (169–170), exit, stderr and argv types (173–176), argv binding (177–189), commit (191), policy digest (192), counter types (193), population-field rejection (199). Every failure exits 2.
- Partitions (lines 201–215) are line-equivalent to gate `_scan_result` (gate 260–268). Allowed includes non-author overlap; unallowlisted excludes non-author; forbidden takes precedence (280–281); exit code (288).
- `differences` (lines 216–223) compares every receipt-visible gate field.
- `privacy_clearance` is hard-coded False (line 230). The exit mapping and constant error reasons are at lines 233 and 277–280. `Parser.error` (lines 235–236) prevents argparse from writing to stderr.
- `selftest` (lines 238–265): four arms, each asserting exit, finding_id, privacy_clearance and empty stderr. Statically traced: R01 MATCH, injected-hit MISMATCH, `../` SETUP, unknown-flag SETUP. Not executed.
- Repeated work: one `tree()` call inside `scan`; about five `committed` subprocess pairs. Apart from F9, no material allocation issue.

## Verification gaps

- Nothing was executed. The selftest, builder, oracle and R01–R24 rows were traced statically only.
- Real-data numbers (95, 86, 4, 5, 4) are the R21 receipt's own fields for measured `9fb1f911…`. They were not recomputed by scanning HEAD.
- Non-author glob semantics (`fnmatch`, where `*` crosses `/`) are identical to gate line 122. They were not tested against the corpus.

## Tool record

- No installs or updates. Read-only git 2.56.0 plumbing (show, log, status, ls-files, diff). `sha256sum` and `wc` were used only for checksums and counts.
