# EvidenceScribe — round 14 wave report (mori-r14-repair)

- Seat: `MoriR14.EvidenceScribe` (scribe, leaf). Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
- Assignment: audit evidence provenance needed to show red-before (entering `dbe85009253c092fe50e4e93056fceeae273ec31`) and green-after (repaired commit); recommend receipt fields, digests and counting commands. No test, census, oracle, or harness execution. No top-level report, LOG, SCORECARD, or corpus write.
- Tool installs or updates by this seat: **none**. Reads only: `git log`/`git show`/`git rev-parse`/`git status` (read-only), `sha256sum`, `cmp`, `grep`, and `python3` JSON parsing of committed receipts.

## 1. Pinned state observed

| Item | Observed | Source |
|---|---|---|
| HEAD = entering commit | `dbe8500` = `dbe85009253c092fe50e4e93056fceeae273ec31`; subject "round-13 verifier spot-check"; only file changed vs `2e57647` is `corpus/lessons/round-13-verifier-spotcheck.md` | `git log`, `git show --stat dbe8500` |
| Working tree | only untracked `.ufo/waves/round-14/` | `git status --short` |
| Census at entering | `tools/mori-census.sh` sha256 `39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985` (blob at `dbe8500` = working tree) | `git show dbe8500:tools/mori-census.sh \| sha256sum` |
| Oracle at entering | `tools/mori-silence-cases.sh` sha256 `34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa` | same method |
| Harness at entering | `tools/mori-round13-regressions.py` sha256 `02b5974244923fa9cf644ce0795de98f6843b95e43662a6522d6299d8b63e264` (identical at `c13df48` and `dbe8500`) | `git show … \| sha256sum` |
| Harness before c13df48 | `80bd58a` harness sha256 `c518b9967046276f…` (16-char prefix) | `git show 80bd58a:tools/mori-round13-regressions.py \| sha256sum` |
| Round-14 frozen copies | `.ufo/waves/round-14/frozen/mori-census.sh` and `mori-silence-cases.sh` are **byte-identical** to `dbe8500` (`cmp` passed); `frozen/inputs.json` sha256 `33bfeb08bff7ce3572ce19b0e12da4f263c0a79705b0137d0de1c6ca1724f32e` pins only those two digests | `cmp`, `sha256sum` |
| Round-13 frozen (pre-r13 production) | `.ufo/waves/round-13/frozen/mori-census.sh` `3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164`; `mori-silence-cases.sh` `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5`; `inputs.json` `d91690dc0417aecd9bffd507b53cd4e2a32fc6614753c82ccbc0c5b590cfdc3f` | `sha256sum` |

Round-14 `frozen/inputs.json` stores `base_commit` = `dbe8500`, which matches HEAD. The r13 harness' `verify_inputs_file` reads this format, so the frozen-dir check is usable as-is.

## 2. Observed behaviour at entering bytes (static anchors, not re-run)

Read-only grep of `git show dbe8500:tools/mori-census.sh` against the r13 frozen census:

| Claim | Frozen pre-r13 (`3da5b098`) | Entering `dbe8500` (`39abda0a`) | Anchor |
|---|---|---|---|
| Critical user-journal OOM alarm | `emit_finding OOM_KILL_JOURNAL crit` at `:894` | **no `emit_finding OOM_KILL_JOURNAL` line** | frozen `:894`; entering has no emitter |
| Non-fleet unit failure owner route | `emit_finding UNIT_FAILURE_OUT_OF_SCOPE info … tsukuroi owns these` at `:908` | **no emitter** | frozen `:905,:908`; entering none |
| Fleet unit failure | `UNIT_FAILURE_JOURNAL … scope=fleet-units` at `:905` | entering maps `user:unit_failure_record` → `UNIT_FAILURE_JOURNAL` for all user units (`:1026`); `system:unit_failure_record` → `UNIT_FAILURE_JOURNAL_SYSTEM` (`:1027`) | entering `:1026-1027` |
| Kernel OOM severity | n/a | `:1095` sets `sev=warn` only for `user:unit_sigkill_record`; kernel OOM notice stays info | entering `:1095` |
| Unmeasured-class info finding | n/a | `:1041` `JOURNAL_CLASSES_UNMEASURED … reason=no-anchored-structured-field` | entering `:1041` |
| Journal trust note | text class in frozen (`:874`-era `grep -ciE` on MESSAGE text) | `:1126` states `trust=client-supplied field=user:MESSAGE_ID` for the structured surface | entering `:1126` |

Important: `dbe8500` and `3da5b098` are **not** a clean before/after pair. The frozen census is a pre-r13 build whose OOM/unit-failure rows are MESSAGE-text derived (per the r13 spot-check, `corpus/lessons/round-13-verifier-spotcheck.md`, and the frozen grep anchors above). A green-after census must satisfy the **behavioural** contract (structured fixture → critical DRIFT row; split fleet/non-fleet owner routing), not reproduce the frozen text behaviour.

## 3. Provenance facts from committed r13 receipts (what a green receipt must not repeat)

Read from `.ufo/waves/round-13/evidence/*.json`:

| # | Receipt | Observed | Gap |
|---|---|---|---|
| P1 | `regressions-after-final.json` (outer) `measured_commit=80bd58a`, `exit=1`; inner `evidence.json` `summary.counts={pass:18, fail:1, mutation-red:2}` | `R13_C1_USER_SCOPE_NONZERO` = **fail** (fixture user kernel=3 coredump=1 segfault=1 → `verdict=CLEAN/ok rc=0`) | Inner `evidence.json` has no revision, no harness digest, no argv. Only the wrapper says the commit. |
| P2 | `regressions-accepted.json` (outer) `measured_commit=c13df48`, `exit=0`; inner `summary.counts={pass:19, mutation-red:2}` | Same census `39abda0a`, same oracle `34cd5770`, same seeds `1313/1313`, same fixture text → `R13_C1_USER_SCOPE_NONZERO` = **pass** | Only difference is the harness (`c518b996` → `02b59742`). Commit `c13df48` ("align nonzero fixture finding expectations") changed the **expectation** `KERNEL_OOM_NOTICE_JOURNAL_USER` 0→3, `COREDUMP…` 0→1, `SEGFAULT…` 0→1 to match observed output. The fail receipt was not superseded inside its own directory. |
| P3 | `regression-selftest-final.json` `measured_commit=80bd58a` | Selftest bound to a pre-`c13df48` harness | Already flagged by the r13 spot-check; not a c13df48 selftest. |
| P4 | every `regressions-*/evidence.json` `summary.gate` | `"not-registered (evidence harness)"` | Receipts are not gate-registered, so none is a gate pass. |
| P5 | `regressions-before-final.json` `measured_commit=80bd58a`, `command --baseline` | Baseline mode records `expected-defect` / `baseline-rejected`; it never emits `pass` (`PASS = "pass"` is strict only, harness comment "never marks the new contract pass") | Baseline cannot be the green side. Red-before must use strict mode against the entering bytes, or be recorded as a separate baseline class. |
| P6 | `live-measurement.json` `measured_commit=c13df48` | All-zero live counts (12/12 comparisons `0`) | Live zero proves no false positive on this host only. Positive proof must come from synthetic fixtures labelled as such. |
| P7 | `evidence.json` `targets.*.sha256` | Present and correct (census `39abda0a`, oracle `34cd5770`, SHONEN `508d5b46`, frozen digests) | Good. Keep. Harness digest and expectation digest are absent. |
| P8 | `evidence.json` `runs[]` | Run name, stdout/stderr files under `runs/`, no digests in the JSON | A reader cannot tie a claim to specific stdout bytes without re-hashing files by name. |
| P9 | `C1_FINDINGS` and `C1_SURFACE_TOKENS` in the harness | Expected values live in the harness, which is the same tree as the repair | Expectations and the thing they judge can change in one commit (P2). This is circular unless the expectation digest is pinned before the repair. |
| P10 | `boot=0123456789abcdef0123456789abcdef` in C1 fixture receipts | Synthetic boot id used in fixture rows | Needs an explicit `fixture_kind: synthetic` so no reader mistakes it for a live boot scope. |

## 4. Recommended red-before / green-after design (provenance only)

1. **Expectations first.** Commit (or hash into the red receipt) the r14 expectation table before the repair commit: each claim id, axis, expected state, expected finding id/severity/scope, expected rc, and fixture id. Record its sha256 as `expectations.sha256`. The green receipt must carry the **same** digest. Any change between red and green is a named correction line in the report, never a silent pass (addresses P2, P9).
2. **Red-before side.** Run the strict harness (not `--baseline`) against a **pinned copy** of the entering census: extract `dbe8500:tools/mori-census.sh` to a temp path, record its git blob id and sha256, and pass `--census <copy>` with `--frozen-dir .ufo/waves/round-14/frozen`. Expected: each target claim is `fail` (exit 1). Record which claims fail and why (state, finding id, rc).
3. **Green-after side.** Run the same strict harness, same claim ids, same fixtures, same seeds, against the repaired commit's census blob (extracted the same way, not the working tree). Expected: target claims `pass`, exit 0.
4. **Control side (non-target claims).** Honest oracle, sibling/no-OOM control, and the non-fleet-only and fleet-only cases must be `pass` both before and after. A `pass → fail` flip on a non-target claim is harm, not a footnote.
5. **Pairing rule.** Red and green receipts must share: the same claim id set, `expectations.sha256`, `fixtures.tree_sha256`, `seeds`, oracle digest, SHONEN digest. They must differ only in census blob/sha256 and harness `sha256` if the harness itself changed (which must then be a recorded correction).
6. **Revision binding.** A receipt cites the repaired **tree** and **blob** ids, not just a commit hash. The receipt is generated before the landing commit exists; the landing commit must descend from the cited revision and have a commit time ≥ receipt `generated_utc` (QUALITY 22). Record `clean_tree: true` (empty `git status --porcelain` on the paths the receipt covers) at capture time.
7. **Fixture reuse.** Text-only fixtures (`MESSAGE=` or `"MESSAGE":` carriers) are red-by-design for the repaired census (criterion 15). Do not reuse them as green fixtures. Use `MESSAGE_ID` and structured fields (`UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS`, `COREDUMP_SIGNAL`) with a `fixture_kind: synthetic` label.
8. **Strict mode gate.** A receipt is a gate pass only if the harness is registered (SKILL.md) or the wave lead explicitly labels it `evidence-only`. Today's receipts are `not-registered`; keep that label on any r14 receipt unless registration lands.

## 5. Recommended receipt fields

Top-level (`evidence.json` or an equivalent sidecar `receipt.json`, same directory as the run outputs):

```
schema                       "mori-round14-receipt-v1" (or the harness schema if extended)
role                         red-before | green-after | control | harm-watch
generated_utc                ISO-8601 Z; must be <= landing commit time
revision                     full 40-hex commit the target bytes came from, or "worktree" + reason
tree_sha                     git rev-parse <revision>^{tree}
clean_tree                   true/false (git status --porcelain empty for covered paths)
entering_commit              dbe85009253c092fe50e4e93056fceeae273ec31
argv                         exact command line (including --census, --frozen-dir, --output, --seed, --nonce)
cwd                          absolute lane root
host                         uname -srm; python3 --version; bash --version
targets:
  census      { path, git_blob_sha1, sha256 }     # 39abda0a… at entering; repaired at green
  oracle      { path, git_blob_sha1, sha256 }     # 34cd5770… unless repaired
  harness     { path, git_blob_sha1, sha256 }     # 02b59742… at entering
  shonen      { path, sha256 }                    # 508d5b46… unless changed
  frozen_dir  { path, inputs_sha256 }             # .ufo/waves/round-14/frozen/inputs.json
  expectations{ path, sha256 }                    # r14 expectation table, committed before repair
entropy:      { shuffle_seed, run_nonce }
fixtures:     { tree_sha256 (hash of sorted file list + contents), kind: synthetic|live, boot_id|null }
summary:      { claims, counts: {…}, exit, gate: registered|not-registered }
claims[]:     { id, axis, expected, observed, status, rc, runs[] }
runs[]:       { name, argv, rc, stdout_path, stdout_sha256, stdout_bytes, stderr_path, stderr_sha256 }
```

Status vocabulary stays the r13 set (`pass`, `fail`, `expected-defect`, `baseline-*`, `mutation-*`, `unavailable`). Do not invent a new "partial" status.

## 6. Recommended counting and verification commands

These are for L1 to run **once after all changes land**. Nothing here was executed by this seat. They read receipt JSON and captured stdout only, and they do not re-run the census, oracle, or harness.

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin

# A. Digest chain: every cited target and frozen file matches its recorded sha256
R=<receipt-dir>
jq -r '..|objects|select(has("path") and has("sha256") and .sha256!=null)|"\(.sha256)  \(.path)"' "$R/evidence.json" | sha256sum -c -
jq -r '.runs[]|"\(.stdout_sha256)  \(.stdout_path)"' "$R/evidence.json" | sha256sum -c -

# B. Recount statuses and compare with the declared summary (must be identical)
jq -n --slurpfile d "$R/evidence.json" '$d[0] | {recount:(.claims|group_by(.status)|map({key:.[0].status,value:length})|from_entries), declared:.summary.counts}'

# C. Red→green transition table (join on claim id; absent = failure)
jq -n --slurpfile b "$RED/evidence.json" --slurpfile a "$GREEN/evidence.json" \
  '[$b[0].claims[] as $x | {id:$x.id, axis:$x.axis, before:$x.status,
     after:((first($a[0].claims[]|select(.id==$x.id))|.status) // "absent")}]'
#  must hold: every target id has before∈{fail,expected-defect} and after=="pass"
#  must hold: no id has after=="absent"
#  harm check: select(.before=="pass" and .after!="pass") is empty for non-target ids

# D. Pairing: same expectations, fixtures, seeds, oracle, SHONEN digests
jq -r '[.targets.expectations.sha256, .fixtures.tree_sha256, (.entropy|tostring), .targets.oracle.sha256, .targets.shonen.sha256]|join(" ")' "$RED/evidence.json" "$GREEN/evidence.json"
#  the two lines must be identical

# E. Revision binding (static, no execution)
git merge-base --is-ancestor "$(jq -r .revision "$GREEN/evidence.json")" "$LANDING" && echo ancestor-ok
git show -s --format=%cI "$LANDING"         # must be >= jq -r .generated_utc "$GREEN/evidence.json"
git rev-parse "$(jq -r .revision "$GREEN/evidence.json"):tools/mori-census.sh"  # must equal targets.census.git_blob_sha1
git show "$(jq -r .revision "$GREEN/evidence.json"):tools/mori-census.sh" | sha256sum

# F. Verdict grammar on captured census stdout (one verdict line, roll word, no MESSAGE)
grep -c '^MORI_CENSUS:' "$R/runs/<name>.stdout"                          # must be 1
grep -oE '^MORI_CENSUS: (CLEAN|DRIFT)' "$R/runs/<name>.stdout" | sort | uniq -c
grep -cE '"MESSAGE"[[:space:]]*:|(^|[^_])MESSAGE=' "$R/runs/<name>.stdout"  # must be 0

# G. Alarm and routing rows on captured stdout (IDs are the r14 names chosen by the repair seats)
grep -oE '^FINDING [A-Z_]+ severity=[a-z]+' "$R/runs/<name>.stdout" | sort | uniq -c
grep -cE '^FINDING <OOM_ID> severity=crit ' "$R/runs/<oom-fixture>.stdout"   # expected 1 for structured OOM fixture
grep -cE '^FINDING <FLEET_ID> ' "$R/runs/<fleet-fixture>.stdout"             # expected 1
grep -cE '^FINDING <NONFLEET_ID> ' "$R/runs/<fleet-fixture>.stdout"          # expected 0 (never summed)

# H. Static emitter inventory (source only; NOT behavioural evidence)
git show dbe8500:tools/mori-census.sh | grep -cE 'emit_finding (OOM_KILL_JOURNAL|UNIT_FAILURE_OUT_OF_SCOPE)\b'   # 0 at entering
git show <repaired>:tools/mori-census.sh | grep -cE 'emit_finding <OOM_ID> crit'                                 # >=1 after repair
```

Rules for interpreting the counts:
- A count of `0` from `grep -c` is a result, not an error. Empty capture (missing file) is `unavailable`, never 0.
- Source-level counts (section H) never substitute for a behavioural row. The r13 spot-check already rejected source-only evidence for C1.
- Scope counts (user/system) are reported per scope and never summed.

## 7. Routed items (owners named; no edits made here)

1. **Harness digest and revision inside each receipt (P1, P2, P3).** Owner: the r14 harness owner / L1. Add `revision`, `tree_sha`, `targets.harness`, and `expectations.sha256` to the inner JSON.
2. **Expectation pinning (P2, P9).** Owner: L1. Freeze the r14 expectation table in a committed file before the repair commit; hash it into the red receipt.
3. **Gate registration (P4).** Owner: L1 / SKILL. Either register the r14 harness or label every receipt `evidence-only`.
4. **Selftest on the delivered revision (P3).** Owner: L1. Run the selftest on the landing bytes, not an earlier revision.
5. **Live vs synthetic label (P6, P10).** Owner: receipt writer. Add `fixtures.kind` and `boot_id` null for synthetic cases.
6. **Stdout digests per run (P8).** Owner: harness owner. Add `stdout_sha256` and `stderr_sha256` into `runs[]`.
7. **Frozen manifest scope.** Owner: L1. Round-14 `frozen/inputs.json` pins only the two entering production scripts. If the harness will also verify the r13 frozen snapshots (`3da5b098`, `448f7738`) as the historical baseline, add them to a separate manifest rather than overwriting the round-14 one.

## 8. Limits

- All entering-state facts above are static (`git show`, `grep`, `cmp`, `sha256sum`). No census, oracle, or harness was executed by this seat; no behavioural claim here is observed.
- The two r13 receipts (P1, P2) were generated at 04:31:01Z and 04:32:34Z by the same committed tree state history; the attribution to the harness change is inferred from the sha256 difference, the commit `c13df48` diff, and the identical census/oracle/seed inputs. [INFERENCE] on causality beyond those facts.
- Line anchors (`:894`, `:908`, `:1026-1027`, `:1041`, `:1095`, `:1126`) are read from `git show` text at the stated commits. They were not re-verified against a running census.
- The round-14 expectation table, fixture generator, and repaired-commit digests do not exist yet. Section 5 is a template; no field value is claimed.
- Working-tree state and wave seats are in flight; only `dbe8500` bytes were used for pins.

## 9. Coordination

- No messages sent. Sibling outputs under `.ufo/waves/round-14/build/` did not exist when read (only `swarm-registry.json`), so no sibling claim was cross-checked.
- No writes outside this file. No commits, no LOG/SCORECARD/corpus changes, no tool installs.
