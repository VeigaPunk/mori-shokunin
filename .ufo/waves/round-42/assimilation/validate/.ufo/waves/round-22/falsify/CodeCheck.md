# CodeCheck: `check()` and direct-call contracts in `tools/mori-retention-reconcile.py`

Seat: CodeCheck (round-22 falsify). Static read only. Correction applied: `denominator-correction.md` (policy_excluded = non-author-glob identities; the policy source is scanned normally).

## Target identity

- Shipping file: `tools/mori-retention-reconcile.py`, HEAD `50b6f75`, working copy clean, 283 lines, sha256 `08dc3c5104ff891c1a2edbaa21aea84bd71acdadbd5f30d45c93558068126987`. All line numbers below are HEAD.
- Retained real run (`.ufo/waves/round-22/evidence/measure1/real-reconciliation.json`) records `tool_sha256` `d6870fb6db7c7d0886f1823b42399821f4f54a4ff0290ee1b43adf9400ac0ce7`, which is blob `3985b3d`. That evidence does not attest HEAD. The `3985b3d`→`50b6f75` diff changes `git()` (returns `cp`, takes `ok=`), `tree`/`committed`/`scan` call sites, `policy_rules` (now also catches OverflowError and RecursionError), `receipt_revision` (now `rev-parse --verify --quiet` peel), merge-base exit handling (`ok=(0,1)`), and `Parser(add_help=False)`. Verdict logic in `check()` L176–233 is unchanged.
- Gate parity reference: `tools/mori-retention-gate.py`, sha256 `cf0896a2ea36f169c9e900c58eefe7e2a900a4c9d67f849f753f4631d8ab829e`.

## Findings (severity order)

### F1. Medium. `raw_unallowlisted` is the scanner-scope count (identity/label; contested by frozen pins)

- L210 `scanner=[h for h in hits if not is_non_author(h)]`; L212 `unallowed=[h for h in scanner if … not in allowed_keys]`; L227 `'raw_unallowlisted':len(unallowed),'scanner_unallowlisted':len(unallowed)`.
- The field named `raw_` never counts non-author hits. The two fields are equal by construction. L216–223 never compare either one, so verdict and exit are unaffected.
- Counterexample, derived from code: one tracked file matching `non_author_paths_glob` with one unallowlisted R-hit and no other hits. Output: `raw_total` 1, `policy_excluded` 1, `scanner_total` 0, `raw_unallowlisted` 0. The gate receipt is metric 0, non_author 1, RETENTION_CLEAN, exit 0, so reconcile exits 0 while the raw population holds one unallowlisted identity.
- Real input, same logic: `allowed` (L211) is computed over raw hits. Raw unallowlisted = 95 − 86 = 9. Emitted value is 4 (retained run: raw_total 95, allowlisted 86, raw_unallowlisted 4, scanner_unallowlisted 4). Pins: `frozen/expected-real.json` L21 = 4; `frozen/fixture-builder-v2.py` L104 = 1 for the synthetic valid fixture.
- Two coherent readings. (a) The v2 three-way partition (allowlisted / unallowlisted / non-author): "unallowlisted" is author-scope, and 4 is correct. (b) The literal raw population: 9 real. The name supports (b); the pins support (a). L1 must rule. Options: rename to an author-scope field and drop the duplicate, or emit the literal raw count and re-pin. Do not change code against the pins without that ruling.

### F2. Low. Error contract: unhandled exceptions exit 1 with a traceback (L269–281; L58)

- L281 `print(...)` sits outside the try (L269–280). The catch list at L279 is `(OSError,UnicodeError,ValueError,TypeError,KeyError,RecursionError)`. Any other exception propagates; Python exits 1 with a traceback. Exit 1 is the MISMATCH code. The gate's equivalent (gate `main` L754–756, `except Exception`) returns sanitized exit 2.
- Counterexample [INFERENCE, not executed]: `check … | head -c 1`. The JSON emitted at L233 (`raw_hits`, `scanner_hits`, `policy_excluded_hits`, tens of KB for the real input) exceeds the stdio buffer, so EPIPE is raised inside `print`, uncaught. Exit is 1, and stderr carries exception text. The contract says "sanitized error code only, never … exception text".
- Same family: L58 maps `subprocess.TimeoutExpired` to `git_unavailable`. That is a sanitized but wrong label.

### F3. Low. Repository identity is not bound (L57, L158, L180–181)

- L158 `repo=Path(a.repo)`: `Path('')` is `.`, so `--repo ""` silently checks the current directory's repository.
- L57 `git -C <dir>`: a non-repository directory inside another checkout (for example an empty directory under `mori-shokunin/.scratch/round22`) makes git discover the enclosing repository, so reads come from the wrong object store. There is no `--show-toplevel` or `--git-dir` check.
- L180–181 only require the receipt's recorded `--repo` to be absolute; it is never compared with L158. Impact is limited because identities are content-addressed and the receipt must still match recomputation. [INFERENCE: the contract does not require an exact repo match.]

### F4. Low, latent. One non-UTF-8 tracked path fails the whole run (L79, L143)

- `tree()` decodes every path with `errors='strict'` (L79), and `scan()` (L143) lists the whole measured tree. One non-UTF-8 name anywhere raises `invalid_tree_path`, so an exact receipt exits 2. The gate's `_scan_git_revision` (gate L202, `path_bytes.decode("utf-8", errors="replace")`) would compute the hit.
- Not triggered by the retained run: it scanned measured `9fb1f911` through the same strict decode (`tree()` is unchanged between `3985b3d` and HEAD) and exited 0. Fail-closed only; no false green.

### F5. Low. Input decoding is wider than the gate (L43–47; gate L49–55)

- `parse()` calls `json.loads(bytes)`, which auto-detects UTF-8 BOM, UTF-16 and UTF-32, and decodes with `surrogatepass`. Gate `read_json` (L52) is strict `raw.decode("utf-8")` followed by `json.loads(str)`, which rejects a BOM.
- Counterexample: a policy or allowlist blob with a UTF-8 BOM (or UTF-16LE). The gate cannot read it and exits 2. HEAD parses and recomputes. This is not a false clearance, because the receipt must still match, but reconcile accepts inputs the gate's contract rejects.

### F6. Low. Over-strict checks with no contract basis (L93, L174)

- L93 `require(isinstance(values,list) and values,'policy_classes')` rejects `"classes": []`. Gate `validate_policy` (L63–70) accepts it and yields zero hits, RETENTION_CLEAN, exit 0. Reconcile exits 2, a false SETUP for a gate-produced receipt.
- L174 `wrapper['stderr']==''` rejects any non-empty stderr. The contract lists `stderr` as a field, not a pass condition. No effect on the retained receipt (stderr is `""`).

### F7. Low. Exit class for a receipt policy-digest disagreement (L192)

- L192 `require(receipt.get('policy_sha256')==digest(raw['policy']),'receipt_policy_digest')` exits 2. The contract's exit 1 is "valid receipt disagrees with recomputation", which arguably covers this. Its exit 2 is also arguable under "input-tree mismatch". L1 must rule.
- `falsify/SourceReject.md` line 34 says this check "yields a mismatch difference (exit 1)". That is wrong at HEAD: `require` raises Invalid, which `main` maps to exit 2 (L277–278), and `differences` never receives this field.

### F8. Material runtime cost, not correctness (L147; L54–57)

- Measured tree `9fb1f911`: 7,715 tracked entries, 4,528 unique object ids (read-only `git ls-tree` count). `scan()` calls `git_out(... 'cat-file','blob', oid)` once per unique id (L147), each through `git()` (env rebuilt per call, L54). A single `check` can spawn up to 4,528 git processes. The gate's `_scan_git_revision` (gate L201) has the same pattern, so this is parity, not a regression. One `git cat-file --batch` stream would remove it.

## Bounded no-findings (HEAD)

- L33–34 `integer()`: `type(v) is int` rejects bool for line, metric, routed, non_author and exit_code (R18).
- L36–41 and L43–47: duplicate JSON keys are rejected; NaN and Infinity are rejected through `parse_constant`. The Invalid raised from hooks escapes `except ValueError` and maps to a sanitized code.
- L49–51 `safe_path`: rejects absolute, empty, `.`, `..` and controls (<32, 127). L73 `--` and L55 `GIT_LITERAL_PATHSPECS=1` stop option or pathspec-magic interpretation. L86 requires exact name equality.
- L88 `committed()`: mode 120000 (symlink) and 160000 (gitlink) are rejected (R21).
- L65–69 `resolve()`: `--end-of-options`, `^{commit}`, resolved once.
- L165–170: peel, ancestry, and policy/allowlist byte equality at measured (R13–R16).
- L176–189 argv binding: checked against the retained receipt's argv (absolute `--repo`, absolute in-repo `--policy` and `--allowlist`, `--rev` equal to measured). It is accepted.
- L190–199: the retained receipt's stdout key set (allowlisted_hits, commit, finding_id, forbidden_allowlist, hits, metric, non_author, policy_sha256, routed, unallowlisted_hits, warnings) passes; no population keys are present.
- L208–215 and L223: partition, finding precedence (forbidden > findings > stale > clean) and exit mapping match gate `_scan_result` (gate L226–307).
- L108 allowlist unwrapping of `{"rows": …}` matches gate L318–319. Row schema and duplicate checks match gate `_validate_allowlist`.
- L217–223: multiset comparison over (path, line, class, line_sha256) covers R05–R10 statically.
- L146–153 `scan()`: NUL skip (L148), `split('\n')` with `errors='replace'` (L149), per-blob cache keyed by oid with path kept in each identity. Correct.
- L230–233: `privacy_clearance` is hard-coded False; emitted fields are counts, names, digests, path, line and class. No matched text.
- L154 `normalize_hits(hits)` discards its result, and its duplicate check is unreachable (path is unique per tree; (line, class) is unique per blob; duplicate class ids are rejected in `policy_rules`). Not material.
- L208–210: `is_non_author` is evaluated twice per hit. Not material.

## Corrections to existing falsify notes

- Notes written against `3985b3d` cite line numbers that are +5 at HEAD: raw_unallowlisted L222→L227; unallowed L207→L212; merge-base L163→L168; revision conflict L184→L189; policy digest L187→L192; policy_changed L164–165→L169–170. Examples: `FinalR02.md`, `FinalR22.md`, `FixturePolicyChanged.md`.
- `SourceReject.md` line 34 exit claim: see F7.
- `FinalR22.md` T1 (9 real raw unallowlisted), `FinalR02.md` C2 and `FinalR12.md` B8 agree with F1 and are not overturned here.
- `FinalR22.md` T3 agrees with F4; verified against HEAD.

## Real-run status

- Retained run at `3985b3d`: exit 0, RETENTION_RECONCILED, receipt_match true, differences `[]`, raw 95 / excluded 5 / scanner 90, unallowlisted 4/4, non_author 5, allowlisted 86, forbidden 0, retention_state red, privacy_clearance false.
- HEAD has not been executed on the real input. A static trace of HEAD over the retained receipt and argv finds no failing check, so the expected result is the same exit 0 with identical counters. [INFERENCE]

## Verification gaps

- Nothing was executed. Python behaviours in F2 (EPIPE raised inside `print`), F3 (`Path('')`, `git -C` discovery) and F5 (`json.loads` BOM and UTF-16 handling, gate `json.loads(str)` BOM rejection) rest on documented semantics, not observed runs.
- Not checked: whether any tracked path in measured `9fb1f911` is non-UTF-8 by a fresh listing. F4 relies on the retained exit 0.
- Not checked: git version support for `rev-parse --end-of-options`. Assumed present on current git.
- Out of scope, noted: `selftest()` (L240) uses `tempfile.TemporaryDirectory` without an explicit directory. Under the lane rule it must run with TMPDIR set to `.scratch`.

## Tooling record

- Installed or updated: none.
- Read-only actions: `git show`, `git log`, `git status`, `git rev-parse`, `git ls-tree`; `sha256sum`, `wc`, `cut`, `sort`. No tool executions, tests, builds or linters.
