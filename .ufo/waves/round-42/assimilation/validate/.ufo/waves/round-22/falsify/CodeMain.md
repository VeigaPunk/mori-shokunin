# `main` and direct-call contract audit — `tools/mori-retention-reconcile.py`

**Seat:** MoriR22.CodeMain (read-only leaf, static analysis only; no executions, no edits, no delegation, no installs).
**Target:** /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-reconcile.py at worktree HEAD `50b6f754e7188e8c6352fc8df7b7b5195e697fa8`; `git status --porcelain` shows no entry for the target path, so worktree bytes are the committed bytes. Line numbers below are worktree line numbers.
**Read first:** .ufo/waves/round-22/denominator-correction.md (effective semantics: `policy_excluded` = non-author-glob identities; scanner denominator = raw minus those identities; the supplied policy file is scanned normally), frozen/requirements-v2.json (24 IDs), and the direct producers frozen/fixture-builder-v2.py and oracle-reconcile-v2.py plus tools/mori-retention-gate.py as the receipt-format producer.

Scope honored: `main` (lines 268–282), `Parser.error` (235–236), the direct calls `check` (157–233) and `selftest` (238–266) as invoked from `main`, and the argument contract between them. Deeper helper internals already covered by sibling seats (CodePolicyRules.md, CodeTree.md, CodeNormalizeHits.md) are not re-audited and their findings are not repeated.

## Findings by severity

### F1 — Medium: stdout emission sits outside `main`'s guarded region, so a failing output channel escapes as an unhandled exception with exit status outside the contracted set, conflating infrastructure failure with MISMATCH

**Source.** `try` spans lines 269–280; both failure handlers (277–278 `Invalid`, 279–280 `OSError/UnicodeError/ValueError/TypeError/KeyError/RecursionError`) produce `finding_id=RETENTION_RECONCILIATION_SETUP`, exit 2, and sanitized `error` codes. The single emission `print(json.dumps(result,sort_keys=True,separators=(',',':')))` at line 281 executes after the `try` suite, and `return code` at 282.

**Defect.** The handler at line 279 explicitly lists `OSError`, but the only `OSError` that `main` itself can raise — the write of the result to stdout — is raised at line 281, outside the reach of that handler. When the stdout pipe has no live reader (e.g. the tool is consumed as `mori-retention-reconcile.py check … | head -c 0`, or stdout is redirected to a file on a full filesystem), `print` raises `BrokenPipeError` (an `OSError` subclass) uncaught: CPython writes the traceback (source lines, file paths) to stderr and the process terminates via the unhandled-exception path; the subsequent failing stdout flush at interpreter shutdown is reported by CPython with exit status 120 (both 1 and 120 are outside the contracted `{0,1,2}` set; the traceback on stderr breaches the sanitized-output clause). Either manifestation breaks the exit-channel exclusivity the contract defines — exit 1 is reserved for "valid receipt disagrees with recomputation" — and no reader can distinguish a crash from a MISMATCH verdict.

**Counterexample.** Any consumer that closes the read end before emission. A deterministic infrastructure variant: stdout opened on a full tmpfs. Under both, a fully reconciled receipt (which should print `RETENTION_RECONCILED`, exit 0) instead dies mid-emission with a traceback and a nonzero exit that is neither the agreed verdict nor the sanitized 2.

**Bounded notes.**
- The encoding arm is not reachable: `json.dumps` defaults to `ensure_ascii=True`, so the payload is ASCII-only regardless of tracked-path content; `UnicodeEncodeError` at line 281 cannot occur. Only the write-failure arm is real.
- `json.dumps` itself cannot raise here: `result` is plain dict/list/str/int with unique str keys (no cycles; `raw_hits` shares dict objects with `scanner_hits`/`policy_excluded_hits`, which `dumps` handles).
- Parity, out of scope: the producer `mori-retention-gate.py` has the same shape (`emit(result)` after its `try`, around its lines 756–757), so gate-produced receipts in the wild share the pattern; this does not cure the contract breach in the tool under audit.

### F2 — Low: `--repo` is the one CLI argument with no boundary validation; an empty value silently re-targets reconciliation at the invoking process's CWD repository

**Source.** Line 271 defines the `check` subparser with `--repo` merely `required=True`; line 158 consumes it as `repo=Path(a.repo)` with no `require`. Every other externally supplied name is validated at the boundary: `--receipt/--policy/--allowlist` through `safe_path` (line 159, rejecting empty/`..`/absolute/control chars), `--rev` through `resolve` (lines 65–66, rejecting empty and control chars). `Path('')` normalizes to `PosixPath('.')`, so `git -C .` runs against whatever repository the invoking CWD belongs to.

**Counterexample.** `mori-retention-reconcile.py check --repo '' --rev HEAD --receipt receipt.json --policy policy.json --allowlist allowlist.json` executed inside any Git worktree does not fail setup; it reconciles that unrelated worktree's HEAD and can return `RETENTION_RECONCILED` with internally consistent provenance fields (`input_revision`, `inputs_sha256`, `tool_sha256` all describing the wrong tree). Under the contract's exit-2 class ("malformed/unreadable input, invalid … path") an empty `--repo` should be refused, mirroring the tool's own treatment of empty `--rev`/`--receipt`.

**Bounded honesty.** This is a validation-scope gap against the tool's own convention, not a producer/consumer divergence: the gate's `_git` passes `--repo` to `git -C`, and `git -C ''` is a documented no-op for an empty operand, so producer and consumer behave identically here. Impact is bounded by read-only operation; the harm is a mis-scoped verdict, not mutation.

## Bounded no-finding statements (main + direct-call surface)

- **Argparse routing.** `--selftest` combined with a subcommand (273–274), a subcommand without required flags, unknown flags, `-h` (both parsers `add_help=False`), and repeated subcommands all reach `Parser.error` (235–236) or the `require` guards → `usage` → exit 2. No reachable combination yields exit 0/1 without running the corresponding arm.
- **Exception mapping and sanitization.** All `Invalid` reasons in the reachable graph are fixed ASCII literals (247, 252, 264 included); `str(exc)` at 278 therefore emits codes only. `parse`'s handlers and the `parse_constant`/`no_duplicates` hooks convert malformed JSON (including duplicate keys and NaN/Infinity constants) into `Invalid`, not into the broad handler. Reachable internal raises after validation are covered by the line-279 tuple (`raw[key]` KeyError at 163/219 is caught; argv indexing is guarded by `recorded_option` length checks, 177–178).
- **Boolean/type leaks.** `integer` (33–34) uses `type(value) is int`, closing the bool route for `exit_code` (170), `metric`/`routed`/`non_author` (193), and receipt hit `line` (124); `auxiliary` requires `line is None` (133), which booleans fail. No bool can influence a compared field or a finding.
- **`main`→`check` result contract.** `check` returns `(dict, int(bool(differences)))` (233); exit 0/1/2 mapping and the output schema (`raw_total`/`policy_excluded`/`scanner_total`/`raw_unallowlisted`/`scanner_unallowlisted`/`non_author`/`retention_state`/`privacy_clearance:false`/`exclusion_basis:'non_author_paths_glob'`, 224–233) implement the effective denominator correction — `policy_excluded` is the non-author-glob identity population (204–205), the policy file itself is scanned as a normal input (policy blob is in `scan`'s tree walk; no path- or blob-based exclusion of it exists), and `scanner_total` counts raw hits minus those identities. No receipt-sourced string is ever emitted (output carries recomputed identities, digests, and this process's own `argv` only), consistent with the no-matched-text rule.
- **`main`→`selftest` contract.** `selftest` returns `(result, int(passed!=total))` (266) with four isolated real-subprocess arms asserting exit code, `finding_id`, `privacy_clearance is False`, and empty stderr (260–265); internal fixture failures raise `Invalid`, which `main` maps to setup 2 rather than a fake FAIL/PASS verdict — fail-closed, as required.
- **Allocation/repeated work.** Nothing material at this level: `scan`'s per-oid blob/parse cache (143–151) already removes the only quadratic risk across the 95-hit real input; the discarded `Counter` in `scan`'s `normalize_hits` call and the re-derived Counters in the differences loop (217–218) are O(hits) redundancies, immaterial at the observed denominator.

## Already-dispositioned items deliberately not repeated

`raw_unallowlisted` ≡ `scanner_unallowlisted` alias (NoHarm.md NH1), missing `--allowlist` rejected via `recorded_option` (NoHarm.md), `policy_rules` non-empty-classes divergence from the gate (CodePolicyRules.md), whole-tree call-tree no-finding (CodeTree.md).

## Residual risk and verification gaps

- F1's exact interpreter exit status (1 vs 120 on the shutdown flush) and F2's `git -C ''` no-op are [INFERENCE] from CPython/POSIX/git documented behavior; this seat executed nothing, so they are not runtime-confirmed. The defect classification does not depend on which of the two statuses appears.
- Whether any retained r21 receipt was produced with a relative or empty `--repo` was not probed (no evidence-file reads beyond the frozen/oracle set), so the practical reachability of F2 in the real receipt corpus is unverified.
- LSP device is not mounted in this environment (no `lsp` tool available), so caller/definition checks were done by literal source inspection; semantic-reference evidence is not claimed. No tool installs were needed or made (nothing to record under the tooling directive).
