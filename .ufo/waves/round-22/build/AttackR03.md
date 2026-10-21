# AttackR03 — frozen R03 (raw_total=5, policy_excluded=1, scanner_total=4)

Static review only. No tests, builds, or reconciler runs. No implementation candidate existed under `.scratch/round22` when this review ran (glob returned 0 files), so nothing here is a measurement of the new tool. No tools were installed.

Axes affected: calibration (the denominator truth), correctness of the frozen oracle, and provenance (R24).

## 1. Counterexample against the contract's own number: 95/5/90 does not reconcile under exact-path exclusion

The evidence is the committed r21 receipt `.ufo/waves/round-21/evidence/final/retention-floor.json`. Its schema is `mori-r21-command-receipt-v1`, measured_revision=stdout.commit=`9fb1f911…`, and exit 1. I tallied only paths, classes, and counts; no matched text was read.

- The supplied policy path `.ufo/waves/round-18/frozen/c1-policy.json` has **4** hits (R2, R5, R6, R8). All 4 are allowlisted under rule `a`.
- A byte-identical copy at `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` also has 4 hits. It is the same blob, `8bf285bd…`, with policy_sha256 `db06e981…`. Its 4 hits are exactly the receipt's 4 `unallowlisted_hits`.
- `non_author` is **5**, coming from `corpus/lessons/round-1{7,8}-verifier-spotcheck.md`. And 95 − 5 = 90.

So the contract line "raw95 includes5policy source hits, scanner90" matches **raw minus non-author**, not raw minus the supplied policy path. Here is what the contract's own rule ("exactly the supplied policy path … all other hits remain") implies for the real receipt. This is [INFERENCE] from the receipt's identities plus the gate semantics; the reconciler was not run.

| field | expected (real r21 receipt) |
|---|---|
| raw_total | 95 |
| policy_excluded | 4 |
| scanner_total | 91 |
| non_author (raw and scanner) | 5 |
| raw_unallowlisted | 4 |
| scanner_unallowlisted | 4 |

**Risk.** If L1 calibrates the real-run expectation, or the lesson, to 90, an implementation that computes `scanner_total = raw_total - non_author` will "agree" with it. That is the count-subtraction failure the root lesson forbids.

**Correction.** L1 MUST NOT freeze `scanner_total=90` for the real receipt. If the real-run expectation is recorded at all, it should be the table above, marked as an expectation and not an observation. The lesson draft should also correct "5 policy source hits" to "4 supplied-path hits, plus 4 hits in a byte-identical copy that stay in the scanner population; 5 is the non-author count".

## 2. Counterexample: a byte-identical policy copy turns the scanner denominator clean (exit 0, scanner_unallowlisted=0)

In the real repo, run `check --policy .ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` with the same receipt, allowlist, and revision. Every byte check in the contract passes:

- The bytes at the input revision equal the bytes at the measured revision.
- The blob's sha256 equals the receipt's `policy_sha256`.

The tool would then exclude the copy's 4 hits, which are the only unallowlisted ones. The result is scanner_unallowlisted=0, with policy_excluded=4 and scanner_total=91 still "correct". That contradicts R02's requirement that scanner_unallowlisted > 0.

The receipt binds the policy's bytes, not its path. Its `argv` holds absolute worktree paths: `--repo /home/…/mori-shokunin` and `--policy /home/…/.ufo/waves/round-18/frozen/c1-policy.json`.

**Correction (exact criterion).** Bind each input path to the receipt's argv:

- Locate `--repo`, `--rev`, `--policy`, and `--allowlist` in `argv` by exact token position.
- Require `argv[--policy] == argv[--repo] + "/" + <--policy REPO_REL>` as an exact string. Apply the same rule to `--allowlist`.
- On mismatch, exit 2 with finding `RETENTION_RECONCILIATION_SETUP` and the sanitized error `policy_path_unbound` or `allowlist_path_unbound`.

If L1 rejects path binding, it must say so in the contract notes. R03c below would then have to expect policy_excluded={copy} and report the excluded path's identity digests, so the swap is at least visible.

## 3. Counterexample: which revision is the "target"? measured_revision ≠ scanned commit in r21 evidence

In `retention-floor-entering.json`, measured_revision is `9fb1f911…`, while `argv --rev` and `stdout.commit` are both `e9f340ce…`. The hit multisets at the two commits are identical, so an implementation that scans `measured_revision` would reconcile with exit 0 against a tree the receipt never scanned. That is a superficial pass.

**Correction.** Require `measured_revision == stdout.commit == resolve(argv --rev)`, all as full 40/64-hex SHAs. Otherwise exit 2 with `receipt_revision_unbound`. The R03 fixture receipt must satisfy this equality. (This also touches R13 and R24.)

## 4. Concrete R03 fixture (discriminating; counts stay frozen at 5/1/4)

The generator must be deterministic and committed before the implementation:

- Fixed `GIT_AUTHOR_*` and `GIT_COMMITTER_*` names, emails, and dates, for example `2026-10-21T00:00:00Z`.
- `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`.
- Files written with `json.dumps(sort_keys=True, indent=2) + "\n"`, the same as `_write_json` in the gate.
- Freeze C0's SHA in the expected values so the fixture cannot drift silently.

The scan marker is a synthetic token, written `<M>` below. It must be a literal 3+ character uppercase string such as a nonsense trigram, and it must appear nowhere except in the lines listed.

**Commit C0** (the measured revision):

| path | content | hit |
|---|---|---|
| `policy/retention-policy.json` | schema `mori-retention-policy-v1`; one class `{"id":"R1","regex":"<M>"}`; `must_redact_paths: []`; `non_author_paths_glob: ["lessons/*-spotcheck.md"]` | **P**: the regex line self-matches. With sort_keys and indent=2 that is line 5, class R1, and the only hit in the file. |
| `mirror/policy/retention-policy.json` | byte-identical copy of P's file | **C**: line 5, R1. Same line_sha256 as P, different path. |
| `lessons/r1-spotcheck.md` | `<M> one` / *(empty)* / `<M> two` | **N1** at line 1 and **N2** at line 3, both non-author |
| `notes/authored.md` | `intro` / `x <M>` | **A**: line 2, R1 |
| `bin/blob.dat` | bytes containing `<M>` and `\0` | none (NUL blob skipped; a non-skipping implementation gets raw_total=6) |
| `allowlist/retention-allowlist.json` | `{"rows":[{"path":"mirror/policy/retention-policy.json","class":"R1","line_sha256":sha(C line),"reason":"synthetic","rule":"a"}]}` | none |

**Commit C1** (the input revision) is C0 plus `receipts/retention.json`. That file is a `mori-r21-command-receipt-v1` wrapper:

- `measured_revision` = `argv --rev` = `stdout.commit` = full C0 SHA.
- `argv` uses absolute `--repo`, `--policy`, and `--allowlist` under the fixture clone.
- `exit_code` and `stdout` come from a **real subprocess** of the committed `tools/mori-retention-gate.py scan`, with the gate's sha256 recorded.
- The receipt must not be synthesized by the reconciler's own code; a shared bug would otherwise reconcile with itself.

Invocation: `check --repo F --rev C1 --receipt receipts/retention.json --policy policy/retention-policy.json --allowlist allowlist/retention-allowlist.json`

**Expected for R03a:**

- Exit 0, `finding_id=RETENTION_RECONCILED`, `receipt_match=true`, `retention_state="red"`, `privacy_clearance=false` (JSON `false`, not 0).
- Counts:
  - raw_total=5, policy_excluded=1 (P), scanner_total=4 ({C, N1, N2, A})
  - non_author: raw 2, scanner 2
  - allowlisted: raw 1 (C), scanner 1
  - raw_unallowlisted=2 ({P, A}), scanner_unallowlisted=1 ({A})
  - forbidden_allowlist=0
- The receipt itself must show `finding_id=RETENTION_FINDINGS`, exit 1, metric 2, non_author 2, routed 0, warnings [].

Wrong implementations this fixture kills, together with the field each one gets wrong:

| implementation defect | fails on |
|---|---|
| `scanner = raw − non_author` | scanner_total=3 |
| exclusion by blob, digest, line_sha256, or basename/suffix (`endswith(policy.json)`) | policy_excluded=2, scanner_total=3 |
| allowlist keyed on digest alone, ignoring path | P counted as allowlisted, so raw_unallowlisted=1 |
| scanner_unallowlisted copied from raw | 2 instead of 1 |
| NUL blob not skipped | raw_total=6 |
| exit tied to retention_state | returns 1 instead of 0 |

**R03b (raw authority).** Same tree, plus a second allowlist row for A, with the receipt regenerated (metric 1). Expect exit 0, raw_unallowlisted=1 ({P}), scanner_unallowlisted=0, `retention_state="red"` (computed from raw), and privacy_clearance=false. An implementation that derives state from the scanner population would report green here.

**R03c (path swap).** Same as R03a but with `--policy mirror/policy/retention-policy.json`. Expect exit 2, `RETENTION_RECONCILIATION_SETUP`, `policy_path_unbound` (see section 2).

**Optional R03d.** Replace A with a committed symlink `notes/link` whose target string contains `<M>`, keeping counts at 5/1/4. The gate scans mode-120000 blobs, so A becomes line 1 of the target text. An implementation that skips symlinks while scanning, because it misapplies "reject symlink inputs", gets raw_total=4. Symlink rejection applies only to the receipt, policy, and allowlist inputs.

## 5. Semantic ambiguities to freeze before integration

1. **Excluded-identity digest format.** "Digest-only identities" is unspecified. Freeze it as `sha256(json.dumps([path,line,class,line_sha256], separators=(",",":")).encode())`, sorted, and list the expected digest for P. Otherwise the R03 and R04 oracles cannot compare identities.
2. **Policy path that matches a non-author glob.** Freeze the rule: count the hit in policy_excluded only, remove it from the scanner population entirely, and keep it in raw `non_author`. Keep R03 non-overlapping, but cover the overlap in R12.
3. **Non-canonical `--policy` spellings** (`./policy/…`, `policy//…`, a trailing `/`). Either reject them (exit 2, which is my recommendation) or canonicalize; never string-compare a non-canonical path against hit paths, which silently gives policy_excluded=0.
4. **Ancestry of a commit with itself.** Is "measured is an ancestor of input" satisfied when input == measured? `git merge-base --is-ancestor A A` returns 0. Freeze the rule. R03 should use C0 ≠ C1 so the receipt blob stays out of the scanned tree.
5. **Allowlist is not bound by digest in the receipt.** The receipt stdout has no allowlist sha, and r21 read it from an absolute worktree path. Byte equality at target and input revisions is the only binding, so a worktree-dirty allowlist at receipt time can only show up as a mismatch (exit 1). Document this as a limit, not as provenance.
6. **Allowlist file shape.** The gate accepts either a dict with `rows` or a bare list. The reconciler must accept both and must reject other shapes with exit 2.

## Smallest safe correction (summary)

- Freeze R03a, R03b, and R03c exactly as in section 4, with C0's SHA and the excluded-identity digest committed.
- Add argv path binding and revision-triple binding as exit-2 setup checks.
- Strike "5 policy source hits / scanner 90" from the real-run expectation. The real expectation is policy_excluded=4 and scanner_total=91 [INFERENCE].
