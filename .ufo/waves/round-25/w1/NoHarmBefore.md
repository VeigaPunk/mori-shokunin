# NoHarmBefore — round-25 wave-1 no-harm baseline (existing mori gates at 7634be75)

Seat: `MoriR25.NoHarmBefore` (leaf; no subagents dispatched, no lane commits).
Instant of record: **2026-10-22T10:20Z–10:52Z**.
Baseline surface: **`7634be75c74891b5cd2815d0bd5374f89abd7087`** (the round-25 contract commit;
landed in the lane per `.ufo/waves/round-25/contract.md`).
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only for this seat).

**Scope executed:** run every *existing* cheap selftest from a **fresh archive extract** of the
baseline commit (never from the lane checkout), paste command + exit code + summary line, and
record the sha256 of every `tools/*` file at that commit.

**Files written by this seat:** this report only. Nothing else in the lane, at the fleet root, or in
a sibling lane was created, edited, moved or deleted. No tool was installed (see §6).

---

## 1. Method — the extract, and why it is not under `/tmp`

The lane checkout was never used as a run directory. The extract was materialised from git objects
only:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 7634be75c74891b5cd2815d0bd5374f89abd7087 | tar -x -C <tmpdir>
```

Two extracts were made and compared byte-for-byte; they are identical, and identical to the git tree:

| Extract | Path | Note |
|---|---|---|
| E1 | `/tmp/noharm-r25` | the "tmpdir" a reader would naively use |
| E2 | `/home/vgpnk/.cache/mori-r25-w1/extract` | **canonical** run directory |
| E3 | `/home/vgpnk/.cache/mori-r25-w1/r24` | same recipe at the round-24 tip `28b79d3d` (control) |

```
$ diff -rq pristine extract
Only in extract: .scratch
DIFF_RC=1
```

(`pristine` = a third, never-executed extract; the only delta is the scratch dir this seat created.)

**Why the canonical run directory is outside `/tmp`.** Three existing selftests *refuse* a `/tmp`
scratch, so a naive `/tmp` extract cannot run the baseline at all:

| Tool | `/tmp` scratch behaviour | Source |
|---|---|---|
| `mori-dispatch-ledger.py` | `{"finding_id":"SELFTEST_SCRATCH_FORBIDDEN","error":"selftest scratch must not be under a system temp directory"}`, **exit 2** | `tools/mori-dispatch-ledger.py:433-434` |
| `mori-freeze-order.py` | `SELFTEST freeze-order FAIL 0/11`, **exit 1** | `tools/mori-freeze-order.py:500,507,513` (forbidden roots `/tmp`, `/var/tmp`) |
| `mori-retention-gate.py` | `SELFTEST retention-gate FAIL 0/21`, **exit 2** | `tools/mori-retention-gate.py:462,466,468` |
| `mori-round17-jj-regressions.py` | `setup: selftest temp parent may not live under /tmp`, **exit 2** | `tools/mori-round17-jj-regressions.py:1128` (`TMP_ROOTS`), `:1518-1520` |

Observed, not inferred:

```
$ cd /tmp/noharm-r25 && TMPDIR=/tmp/noharm-r25/.scratch python3 -I -B tools/mori-dispatch-ledger.py --selftest ; echo EXIT=$?
{"error":"selftest scratch must not be under a system temp directory","finding_id":"SELFTEST_SCRATCH_FORBIDDEN",...}
EXIT=2
```

**Canonical run environment.** `TMPDIR=<extract>/.scratch` satisfies every gate at once: it is
outside `/tmp` and `/var/tmp`, it is *inside* the checkout (required by `mori-freeze-order.py:514-518`
and `mori-retention-gate.py:457-468`, which demands `TMPDIR == <checkout>/.scratch` exactly), and it
is a real directory, not a symlink.

```
$ mkdir -p /home/vgpnk/.cache/mori-r25-w1/extract/.scratch
$ export TMPDIR=/home/vgpnk/.cache/mori-r25-w1/extract/.scratch
```

Every run below is `cd /home/vgpnk/.cache/mori-r25-w1/extract` first. Python tools are invoked with
`python3 -I -B` (isolated mode, no bytecode written) — the same invocation shape the round-25
contract declares for the new C2 tool.

---

## 2. Which selftests exist (grep of the baseline tree)

`grep -n -- '--selftest' tools/*` over the baseline extract. **19 of the 21 `tools/*.py` offer
`--selftest`; `mori-census.sh` offers it too.** Two tools offer none:

| Tool | `--selftest`? | How it is exercised instead |
|---|---|---|
| `tools/mori-round19-regressions.py` | **no** (`grep -c` = 0) | mode harness: `--content-tool --freeze-tool --expected --output --mode {before,after}`; `tools/mori-round19-regressions.py:1106-1111` |
| `tools/mori-routed-check.py` | **no** (`grep -c` = 0) | `--repo --rev [--round]`; `tools/mori-routed-check.py` usage |
| `tools/mori-silence-cases.sh` | no flag; it *is* the case driver | `bash tools/mori-silence-cases.sh [path-to-census]` (`tools/mori-silence-cases.sh:7-9,179`) |

`mori-census.sh`'s selftest flag, as asked, is in the script header: the usage block at
`tools/mori-census.sh:397` (`usage: mori-census.sh [--selftest] [--pin <path>] [--drift <path>] [--help]`),
its description at `:406-407`, the header comment at `:211-213` ("`--selftest` writes only under
`${TMPDIR:-/tmp}/mori-census-selftest.XXXXXX` and asserts the fixture tree is unchanged"), and the
dispatch at `:4721`.

---

## 3. Baseline results — every command, exit code, summary line

Full sweep, one command per tool, run from the canonical extract with
`TMPDIR=/home/vgpnk/.cache/mori-r25-w1/extract/.scratch`. Wall time for the whole sweep: **41.7 s**
(every individual tool is far below the 2-minute ceiling; the slowest is `mori-census.sh` at 14 s).

| # | Command (from the extract) | Exit | Wall | Summary line (last non-empty stdout line) |
|---|---|---|---|---|
| 1 | `bash tools/mori-census.sh --selftest` | **0** | 14 s | `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` |
| 2 | `python3 -I -B tools/mori-pressure.py --selftest` | **0** | 0 s | `MATCHER: rejected 48/48 corrupted expectations` (line above: `MORI_PRESSURE_SELFTEST: PASS 12/12`) |
| 3 | `python3 -I -B tools/mori-content-review.py --selftest` | **0** | 0 s | `{"exit_code":0,"findings":[{"code":"CONTENT_REVIEW_SELFTEST_CLEAN"}],"schema":"mori-content-review-result-v1","status":"clean"}` |
| 4 | `python3 -I -B tools/mori-dispatch-ledger.py --selftest` | **0** | 1 s | `SELFTEST mori-dispatch-ledger PASS 14/14` |
| 5 | `python3 -I -B tools/mori-evidence-loss.py --selftest` | **0** | 0 s | `{"checks":114,"failures":[],"finding_id":"mori-evidence-loss:audit:aggregator-r10:unresolved","passed":true,"schema":"mori-evidence-loss-selftest-v1"}` |
| 6 | `python3 -I -B tools/mori-freeze-order.py --selftest` | **0** | 1 s | `SELFTEST freeze-order PASS 12/12` |
| 7 | `python3 -I -B tools/mori-journal-window.py --selftest` | **0** | 1 s | `{"cases":16,"failed":0,"failures":[],"finding_id":"MORI_JOURNAL_WINDOW_SELFTEST","passed":16}` |
| 8 | `python3 -I -B tools/mori-misroot-sweep.py --selftest` | **0** | 0 s | `{"arms": 12, "finding": "MORI_MISROOT_SELFTEST_OK", "fixture_bytes": 847, "fixture_sha256": "15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e", "planted_found_with_legacy_pathspec": false, "planted_found_without_pathspec": true, "planted_matched_in": ["path"], "poisoned_paths_absent": true, "sandbox_unchanged": true, "schema": "mori-misroot-sweep-v1"}` |
| 9 | `python3 -I -B tools/mori-retention-gate.py --selftest` | **0** | 1 s | `SELFTEST retention-gate PASS 21/21` |
| 10 | `python3 -I -B tools/mori-retention-reconcile.py --selftest` | **0** | 0 s | `{"finding_id":"RECONCILE_SELFTEST_PASS","passed":4,"privacy_clearance":false,"schema":"mori-retention-reconciliation-v2","total":4}` |
| 11 | `python3 -I -B tools/mori-round13-regressions.py --selftest` | **0** | 0 s | `SELFTEST: pass checks=33 cases=2` |
| 12 | `python3 -I -B tools/mori-round14-regressions.py --selftest` | **0** | 1 s | `SELFTEST: pass checks=20 (parsers + real-gate red rc1/tamper rc2)` |
| 13 | `python3 -I -B tools/mori-round15-regressions.py --selftest` | **0** | 7 s | `SELFTEST PASS selftest_root=/home/vgpnk/.cache/mori-r25-w1/extract/.scratch/mori-r15-selftest-<rand>` (preceded by `SELFTEST control classifier checks: PASS`) |
| 14 | `python3 -I -B tools/mori-round16-context-check.py --selftest` | **0** | 0 s | `{"arms": 15, "claims_runtime_prevention": false, "finding_id": "SELFTEST_OK", "static_only": true}` |
| 15 | `python3 -I -B tools/mori-round16-regressions.py --selftest` | **0** | 5 s | `SELFTEST ok: pin_rc0,green_rc0_verdict_ok,absent_rc1_capability_absent,tool_drift_rc2,bad_want_rc1_mismatch,pack_drift_rc2` |
| 16 | `python3 -I -B tools/mori-round17-context-check.py --selftest` | **0** | 1 s | `{"arms": 31, "claims_runtime_prevention": false, "clauses_checked": 12, "finding_id": "SELFTEST_OK", "static_only": true}` |
| 17 | `python3 -I -B tools/mori-round17-jj-regressions.py --selftest` | **1** | 3 s | `SELFTEST FAIL: ok_rc0: rc=1 mori-round17-jj-regressions: cases=17 match=8 mismatch=9 capability_absent=0 setup_failed=0 assertions=204 failed=9 retained=False` — **see §4** |
| 18 | `python3 -I -B tools/mori-round17-seat-regressions.py --selftest` | **0** | 2 s | `SELFTEST ok: green_rc0_and_manifest,capability_absent_rc1,mismatch_rc1,forbidden_key_rc1,seats_map_projection_rc0,a1_main_sessions_rc0,generated_fifo_rc0,symlink_ancestor_fifo_trap_rc2,unreadable_dirs_sandbox_rc0,root_symlink_rebase_rc0,key_metadata_required_rc1,wrong_type_metadata_rc1,pinned_snapshot_tamper_rc2,prefix_filter_rc0,files_scanned_falsifier_rc1,unreadable_fixture_rc0,fixture_drift_rc2,output_guard_rc2,nonempty_output_rc2` |
| 19 | `python3 -I -B tools/mori-seat-terminal.py --selftest` | **0** | 1 s | `{"arms":49,"finding_id":"SELFTEST_OK","passed":49,"schema":"mori-seat-terminal-selftest-v1","tool_sha256":"de845692000e0318606562dd31877c9a64a88ee0117fa1f22cbc7d4220468af3"}` |
| 20 | `python3 -I -B tools/mori-wave-settlement.py --selftest` | **0** | 0 s | `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)` |
| 21 | `bash tools/mori-silence-cases.sh` (no `--selftest` flag; census case driver) | **0** | 4 s | `MORI_SILENCE_CASES: matched=28 total=28` |

**19 of the 21 selftest entry points are green. One (`mori-round17-jj-regressions.py`) is red in a
plain extract — §4 isolates the cause and proves it is pre-existing and environmental, not a
round-25 regression.**

### 3a. The two tools with no `--selftest`

`mori-round19-regressions.py` pins its oracle to a **git revision** and reads it with
`git show <rev>:<path>` (`tools/mori-round19-regressions.py:25-26,848-863`). An archive extract has
no `.git`, so in the extract it is a setup error:

```
$ cd /home/vgpnk/.cache/mori-r25-w1/extract && TMPDIR=.../extract/.scratch \
  python3 -I -B tools/mori-round19-regressions.py --content-tool tools/mori-content-review.py \
    --freeze-tool tools/mori-freeze-order.py --expected .ufo/waves/round-19/frozen/expected.json \
    --output <out> --mode before
{"error_class":"pinned-oracle-unavailable","mode":"before","schema":"mori-round19-regressions-v1","status":"setup-error"}
EXIT=2
```

Run against a **read-only clone of the lane** placed in this seat's cache (never in the lane), where
the pinned revision `5e393d20daa628a0b4ca9aa6a1626aa54285b3f0` is reachable, it is clean:

```
$ python3 -I -B <extract>/tools/mori-round19-regressions.py --content-tool <extract>/tools/mori-content-review.py \
    --freeze-tool <extract>/tools/mori-freeze-order.py \
    --expected <clone>/.ufo/waves/round-19/frozen/expected.json --output <out> --mode before
EXIT=0
status=baseline-recorded  oracle={revision:5e393d20daa628a0b4ca9aa6a1626aa54285b3f0, sha256:c5c6c67f104ed1baa57a56bfb22728a2e871ca174a4915ff4005eb3485abe22a}
c1.counts={pass:10, total:10, regression:0, capability_absent:0}
c2.counts={pass:12, total:12, regression:0, capability_absent:0}
stability={content_tool_unchanged:true, expected_unchanged:true, freeze_tool_unchanged:true, harness_unchanged:true}
```

The frozen oracle in the clone is byte-identical to the one at the pinned revision
(`git show 5e393d20:.ufo/waves/round-19/frozen/expected.json | sha256sum` =
`c5c6c67f104ed1baa57a56bfb22728a2e871ca174a4915ff4005eb3485abe22a`).

`mori-routed-check.py` (the round-23 routed-defect checker, `--repo --rev [--round]`) is likewise
git-object-bound. Against the clone, at both baseline revisions, for round 24:

```
$ python3 -I -B <extract>/tools/mori-routed-check.py --repo <clone> --rev 7634be75c74891b5cd2815d0bd5374f89abd7087 --round 24
{"base":"c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130","held":4,"items":4,"rev":"7634be75...","round":24,...}
EXIT=0
$ python3 -I -B <extract>/tools/mori-routed-check.py --repo <clone> --rev 28b79d3d1b76824f0c825aabe6cb6c5dc49961bf --round 24
{"base":"c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130","held":4,"items":4,"rev":"28b79d3d...","round":24,...}
EXIT=0
```

---

## 4. The one red selftest: `mori-round17-jj-regressions.py --selftest`

### 4.1 Symptom

```
$ cd /home/vgpnk/.cache/mori-r25-w1/extract && export TMPDIR=/home/vgpnk/.cache/mori-r25-w1/extract/.scratch
$ python3 -I -B tools/mori-round17-jj-regressions.py --selftest
SELFTEST FAIL: ok_rc0: rc=1 mori-round17-jj-regressions: cases=17 match=8 mismatch=9 capability_absent=0 setup_failed=0 assertions=204 failed=9 retained=False
manifest: .../extract/.scratch/mori-r17-jj-selftest-<rand>/out-ok/run-manifest.json ; ok_failed_zero: failed=9; keep_rc0: rc=1
EXIT=1
```

From the retained `run-manifest.json`, the failing set is **exactly one assertion id, once per jj
case**, on 9 of the 17 cases:

```
jj-helper-commit        FAIL: jj_config_redirected | path=.../jj-helper-commit/home/.config/jj
jj-commit-no-bookmark   FAIL: jj_config_redirected | path=.../jj-commit-no-bookmark/home/.config/jj
jj-ambient-author       FAIL: jj_config_redirected | path=.../jj-ambient-author/home/.config/jj
jj-young-ambient-author FAIL: jj_config_redirected | path=.../jj-young-ambient-author/home/.config/jj
jj-sibling-author       FAIL: jj_config_redirected | path=.../jj-sibling-author/home/.config/jj
jj-sidebranch-mirror    FAIL: jj_config_redirected | path=.../jj-sidebranch-mirror/home/.config/jj
jj-unresolved-mirror    FAIL: jj_config_redirected | path=.../jj-unresolved-mirror/home/.config/jj
jj-missingref-mirror    FAIL: jj_config_redirected | path=.../jj-missingref-mirror/home/.config/jj
jj-root-unresolved-closure FAIL: jj_config_redirected | path=.../jj-root-unresolved-closure/home/.config/jj
```

`totals = {cases:17, match:8, mismatch:9, capability_absent:0, setup_failed:0, assertions:204,
failed_assertions:9, failed_cases:9}`. **195 of 204 assertions pass.** Every census-behaviour
assertion in every case (exit code, verdict roll, finding ids, branch_tip/head, refs-unchanged,
author/count/sibling-negative, wrongtip) passes; only the redirect-evidence assertion fails.
The eight git-lane cases pass outright.

### 4.2 What the assertion asks for

`tools/mori-round17-jj-regressions.py:1040-1047`:

```python
if "jj" in sb and sb["jj"]:
    # The jj repo config is written under the redirected HOME, never under
    # the operator's ~/.config/jj. This is the positive redirect evidence.
    check(
        "jj_config_redirected",
        (sb["home"] / ".config" / "jj").exists(),
        f"path={sb['home'] / '.config' / 'jj'}",
    )
```

The sandbox `HOME` is `<case>/home` with `XDG_CONFIG_HOME=<case>/home/.config` and
`JJ_CONFIG=<case>/home/jjconfig.toml` (`tools/mori-round17-jj-regressions.py:222-234`).

### 4.3 Root cause (measured, not inferred)

jj 0.45.1 keeps **repo config outside the repo**, under `<config_root>/jj/repos/<config-id>/`, where
`<config_root>` derives from the *user config directory* — here `XDG_CONFIG_HOME`, i.e.
`<case>/home/.config/jj` — and is independent of `JJ_CONFIG` (the lane's own round-17 findings agree:
`.ufo/waves/round-17/build/JjEnvFacts.md:99-101`, "root_config_dir is computed from the user config
directory, not from `JJ_CONFIG`"). The directory `<config_root>/jj/repos/<config-id>/` is only
materialised when jj actually **resolves a workspace that carries a repo `config-id`**.

Direct probes (all under a redirected `HOME`, `XDG_CONFIG_HOME=$H/.config`,
`JJ_CONFIG=$H/jjconfig.toml`, jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5):

| Probe | Command sequence | Result under `$H` |
|---|---|---|
| P1 | `jj git init --colocate <fresh git repo>` | **no** `$H/.config/jj` — the colocated repo's `.jj/repo/` has no `config-id` |
| P2 | P1, then `jj --config user.name=… metaedit --update-author`, `jj commit`, `jj log` | **no** `$H/.config/jj` |
| P3 | P1, then `jj -R <repo> config path --repo` | **yes**: `$H/.config/jj/repos/<id>/` created (the lookup materialises it) |
| P4 | ancestor dir carrying `.jj/repo/config-id`, then `jj git init --colocate` | **yes**: `$H/.config/jj/repos/<ancestor-config-id>/` created |

P3/P4 pin the mechanism: the directory appears exactly when jj resolves an existing workspace's repo
config id — and because `XDG_CONFIG_HOME` is redirected, it appears **under the sandbox HOME**, which
is precisely the redirect evidence the assertion wants.

In a **plain archive extract there is no jj workspace anywhere above the sandbox**, so no config id is
ever resolved and `<case>/home/.config/jj` is never created. That is the whole failure.

### 4.4 Controlled confirmation

Same tool bytes, same extract, only the *location of the scratch tree* changed.

**(a) Scratch under a synthetic ancestor jj workspace that has a repo `config-id`** (built in this
seat's cache, outside the lane) → **all green**:

```
$ python3 -I -B tools/mori-round17-jj-regressions.py --selftest --scratch <cache>/jjanc/scratch
SELFTEST ok: guard_output_repo_root,guard_output_tools,…,ok_rc0,ok_cases,ok_failed_zero,…
EXIT=0
totals = {cases:17, match:17, mismatch:0, capability_absent:0, setup_failed:0, assertions:204, failed_assertions:0, failed_cases:0}
jj-helper-commit  ok=True  path=.../jj-helper-commit/home/.config/jj      (and 8 more, all ok=True)
```

The sandbox HOME then contains `$H/.config/jj/repos/<ancestor-config-id>/` — the redirect evidence.

**(b) Scratch under an ancestor `.jj` that has *no* `config-id`** → jj cannot resolve it and the
cases fail at setup:

```
cases=17 match=8 mismatch=0 capability_absent=0 setup_failed=9 assertions=94 failed=9
```

**(c) Scratch under an ancestor `.jj` with a *bogus* `config-id`** → jj errors out, setup_failed=9.

### 4.5 It is pre-existing, not a round-25 regression

* The tool file is **byte-identical** at the round-24 tip and at the baseline commit:
  `tools/mori-round17-jj-regressions.py` sha256 `da3e080aa5181e8e00872c1d5f0dd97862c495da03adce0b1aa31e27fbcb89f0`
  at **both** `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf` and `7634be75c74891b5cd2815d0bd5374f89abd7087`
  (`git show <rev>:tools/mori-round17-jj-regressions.py | sha256sum`).
* Run from the round-24-tip extract (E3, same recipe) the failure is **identical**:
  `cases=17 match=8 mismatch=9 … failed=9`, exit 1.
* The lane's own recorded round-17 evidence shows the assertion **passing** — because that run's
  scratch lived under the lane worktree, which *is* a jj workspace with a `config-id`
  (`/home/vgpnk/Projects/shokunin/mori-shokunin/.jj/repo/config-id` = `118d84571a457bac1fa8`;
  the recorded evidence path is
  `.ufo/waves/round-17/evidence/final/jj-after/run-manifest.json`, whose `jj_config_redirected`
  entries are `ok:true` with `totals {cases:17, match:17, failed_assertions:0}`).
  The recorded census/jj binary pair is also identical to this host
  (`jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`).

**Conclusion:** the r17-jj selftest is green *in the lane* and red *in a bare extract*, for one
environmental reason. Nothing in wave 1 changed it, and nothing in wave 1 may be credited/blamed for
it. Any wave-1 verdict that quotes "the r17-jj selftest fails" must carry this qualifier.

---

## 5. sha256 of every `tools/*` file at `7634be75c74891b5cd2815d0bd5374f89abd7087`

Computed from the **git objects** (`git cat-file blob <sha> | sha256sum`), and independently confirmed
against the extracted files (`find tools -type f | xargs sha256sum`): the two lists are identical, so
the extract is byte-faithful. Git blob ids are given for cross-reference.

| sha256 (content) | git blob id | path |
|---|---|---|
| `7098b008d614e84c4328af96d15badef700ea84b75a43ba4a375264a01755fb4` | `48df844a22d74a57204f55a62e54760c7038c60f` | `tools/fixtures/mori-job-runway/cases.json` |
| `aeb80ea080436cb344df8dba7ec19eeecc639e347ae87a14bc6835631f28ca94` | `39cc96ab4c689ceb54e7cfaf64420056e6a289f7` | `tools/fixtures/mori-pressure/cases.json` |
| `9b4c450abd57452fe021470b24a8a6a45d738318848d52a439ad8b5c04302e1e` | `4d00f164be8ea856da80e059a139a5e78c67d17e` | `tools/fixtures/mori-pressure/supplementary-cases.json` |
| `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` | `c7d952d6fabe3137a91b9efbea991317ceba1f3e` | `tools/mori-census.sh` |
| `fa88a6b034d1cdb955fc9db1c0aa38efd44bcc9495d6086873b3ebd6476b29cc` | `b5c42df2b2bf2ce0476b39a03495206541669979` | `tools/mori-content-review.py` |
| `9ec14ed3457596afed70bf1664cc51cc5d39f4ffb54b6cad6bc886b0dbde8441` | `b86525c6a9fe0d44e90127323ff291104dcfb5fd` | `tools/mori-dispatch-ledger.py` |
| `de189084a5d197c43e6f04846b8a10c6ad2bcc488d178490aef949db03738eb6` | `98cc66e1f4cd0bcbc77104dbbe5f1f3be7431ea1` | `tools/mori-evidence-loss.py` |
| `ec1be305d9fbf81d8169554cdb8f681a819f97ee89bb1362f08c4de0b427b547` | `fcd8a017378c600c5d9a47a9d40a171f3bf135c5` | `tools/mori-freeze-order.py` |
| `d61e0d220a1825d738e2b9526b2bdd92047e39a4543d0ca0a040795d84ba0aeb` | `b5b71ef1111608ff21f8053e5acf9e2ad2a5b87a` | `tools/mori-journal-window.py` |
| `51072bd7a891fd24779ecadeb4f624de9583c91f798b86f7017ed20b1d6b04c3` | `bb951a5ed430726b2b1c3695a1dc8d3d6f2206d4` | `tools/mori-misroot-sweep.py` |
| `2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7` | `5785c5b23233a5ed1d2116ab610f9aa0cf3b12ec` | `tools/mori-pressure.py` |
| `cf0896a2ea36f169c9e900c58eefe7e2a900a4c9d67f849f753f4631d8ab829e` | `988c5484428b47766335dbfa245b8a296de5d3d7` | `tools/mori-retention-gate.py` |
| `4599ee1aff95f21714e320a87fd31260f0435aa9c7a9884ac60ab952fe099a36` | `78c676e665d23a68c571a9d13698a6aae13b1500` | `tools/mori-retention-reconcile.py` |
| `23b753c1b0f742ddf7ea4e1e1ff3df6aa16a89dc8742b50c135a9d356db9f53b` | `31360de4f6fd57b12b4137957fba20f8f9442365` | `tools/mori-round13-regressions.py` |
| `533218a566030fdabf7ca6a1c78111ca10be3fb3cb0e4a7b22734959f847e4ef` | `511278e7f9d40e19012ddd95f3052d7e8c449f54` | `tools/mori-round14-regressions.py` |
| `6a55c33cc13e2cd862ebd44db66e8af635a35d7cd2a85168360569c886d62ffe` | `4f06cbdef132aeb5b37b106c5e52849759d92ecc` | `tools/mori-round15-regressions.py` |
| `b0bd0aacfae6532426865f3a2201c162b3d349cefe14fb733716ac44c369cee9` | `fa3595cb3e5c9dbd20f97586dc1c8e926850da1d` | `tools/mori-round16-context-check.py` |
| `e70ed67ce502a7b25fdaa3dac562589df3e4fce02f770ec0adf21f47a1921fce` | `334149d2240fae18472f6a7bd66340c65ec11f4c` | `tools/mori-round16-regressions.py` |
| `ffdcd1154f5bc0d5af45cea6f14a4c125852f1f667ca0990350872261213681c` | `50fb4021cc8eb28c8e9f273894d84d1011722958` | `tools/mori-round17-context-check.py` |
| `da3e080aa5181e8e00872c1d5f0dd97862c495da03adce0b1aa31e27fbcb89f0` | `317959bb815745b581bb3974eaa13ab3f48cd7e5` | `tools/mori-round17-jj-regressions.py` |
| `3f3512c41d94c20c5e8aae55ffe17fa219c4c1146ea99e2248d4f924f5da2314` | `4bdbf7255dd1206e361d2f6e0a0e0bf5a04a4df8` | `tools/mori-round17-seat-regressions.py` |
| `0ccd17307c9ff21e26ac38c5e2734735a34c09bffb1499eb57bcb1bde993c652` | `65b95462b5514fdff2b55c1510afb28e9d6f2c58` | `tools/mori-round19-regressions.py` |
| `cd313053ed5305c444db2159e7a4793adad88a162cabf082b7d37773ea1bfdd7` | `bd1e2862bc977834b43d481a28790ef523adbcac` | `tools/mori-routed-check.py` |
| `de845692000e0318606562dd31877c9a64a88ee0117fa1f22cbc7d4220468af3` | `0d0b1a1494b1ba199574c107b777ccbeb006f876` | `tools/mori-seat-terminal.py` |
| `34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa` | `b6683352c2f2f8c6b5f5afa196975ae6980044ac` | `tools/mori-silence-cases.sh` |
| `79e7f9dedb8a16a9d9257644045c56c57ca97b27ab94640ca487b330527b28f9` | `cf2f5dcdb6d04f91d511a4d811f72e52cd1c1c28` | `tools/mori-wave-settlement.py` |

(`tools/` at this commit = 24 files, 1 510 953 bytes total; 21 `.py` + 2 `.sh` + 3 fixture files.)

---

## 6. Baseline facts the wave-1 build seats need

1. **C2's declared tool is not in the baseline surface.** At `7634be75`:
   `tools/mori-job-runway.py` → **absent** (`git cat-file -e 7634be75:tools/mori-job-runway.py` → exit
   128), and also absent at the round-24 tip. Its frozen fixture
   `tools/fixtures/mori-job-runway/cases.json` **is** present at `7634be75`
   (sha256 `7098b008d614e84c4328af96d15badef700ea84b75a43ba4a375264a01755fb4`, git blob
   `48df844a22d74a57204f55a62e54760c7038c60f`) — i.e. the cases were committed **before** the tool,
   exactly as the contract requires.
2. **C1's declared tool is likewise absent** at `7634be75` and at `28b79d3d`
   (`tools/mori-routed-r24.py` → exit 128).
3. **The C1 D1 replay depends on `mori-pressure.py` running from a temporary extract of R.** The
   pressure selftest is green from an extract (row 2 above), and its frozen case file at the baseline
   is `tools/fixtures/mori-pressure/cases.json`
   (sha256 `aeb80ea080436cb344df8dba7ec19eeecc639e347ae87a14bc6835631f28ca94`). The C1 tool must
   therefore run the pressure selftest under `python3 -I -B` from an extract of R — feasible, but the
   extract must be **outside `/tmp`** and the pressure selftest needs no `TMPDIR` fixture tree, so
   that constraint does not bind it.
4. **`jq` on PATH**: `/home/vgpnk/.local/bin/jq` (jq 1.8.2) precedes `/usr/bin/jq` (jq 1.8.2);
   `MORI_JQ_BIN` defaults to `jq` (`tools/mori-census.sh:317`). Both binaries report the same version,
   so the census is unaffected by the ordering.
5. **`mori-census.sh` selftest writes only under `TMPDIR`** (`${TMPDIR:-/tmp}/mori-census-selftest.*`,
   `tools/mori-census.sh:211-213`); with `TMPDIR` set to the extract's `.scratch`, no residue landed
   in `/tmp` (`ls -d /tmp/mori-census-selftest.*` → none).

### Host / environment facts (for reproducibility)

| Item | Value |
|---|---|
| OS | `linux 7.2.11-arch1-1` (arch x64) |
| `python3` | 3.14.8 |
| `git` | 2.56.0 (`/usr/bin/git`) |
| `jj` | 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5 (`/home/vgpnk/.local/bin/jj`) |
| `jq` | jq 1.8.2 (`/home/vgpnk/.local/bin/jq`, then `/usr/bin/jq`) |
| `bash` | `/usr/bin/bash` |
| Extract root | `/home/vgpnk/.cache/mori-r25-w1/extract` |
| `TMPDIR` for all runs | `/home/vgpnk/.cache/mori-r25-w1/extract/.scratch` |
| Round-25 lane HEAD at the close of this seat's work | `e68855d555341fa291eb482343a741bdd9db7100` (the lane moved during the wave; **this baseline is pinned to `7634be75`**, as assigned) |

**Tool installs:** none. No package manager was invoked; `pacman` was not run (host-wide pause).
Everything used (`python3`, `git`, `jq`, `jj`, `bash`, `tar`) was already present at the versions above.

---

## 7. Host state touched, and cleanup

* The only host-visible writes were inside this seat's cache (`/home/vgpnk/.cache/mori-r25-w1/`) and
  `/tmp/noharm-r25/`. Probe scratch trees and the read-only lane clone were deleted afterwards.
* Two probe artifacts briefly appeared under the operator's `~/.config/jj/repos/` (jj materialises a
  config dir when a probe ran `jj config set --repo probe.key`): `f9d3cd37427dac005308` and
  `1e88a5eff4db2566cc67`. **Both were removed**; `~/.config/jj/repos` is back to its pre-session
  count of **1588** entries, and the newest entry's mtime is `2026-10-22T04:33` (pre-session). The
  six pre-existing `probe.key` config files there are dated 2026-10-20 and are not this seat's.
* The lane working tree was **not** written to: `git status --porcelain` in the lane shows only
  sibling seats' untracked wave-1 reports and `.scratch/` (pre-existing, dated 2026-10-21). No `tools/`
  byte changed; the `git`/`jj` binaries, `~/.omp/agent/config.yml`, `~/.omp/agent/mcp.json`, OMP
  settings and fleet scripts were not touched.

---

## 8. Verdict

**No-harm baseline at `7634be75` (operability axis): 19/21 selftest entry points green; 1 green
outside the lane with a git clone (`mori-round19-regressions.py --mode before`: c1 10/10, c2 12/12);
1 red-in-extract-only (`mori-round17-jj-regressions.py --selftest`, exit 1, 9/204 assertions) whose
cause is measured to be the absence of an enclosing jj workspace with a repo `config-id` in a bare
archive extract — pre-existing at the round-24 tip with byte-identical tool bytes, and green in the
lane per the lane's own round-17 evidence.**

**Carry-forward for the L1:** a wave-1 verifier that runs the existing gates from a *plain* extract
will see the r17-jj selftest red for an environmental reason; a verifier that runs them *in the lane*
(or under a jj workspace) sees it green. Pin the run directory when quoting baseline numbers, and
quote the r17-jj line with the §4 qualifier. Nothing in this seat's evidence attributes the r17-jj
failure to wave-1 work, and nothing in wave 1 may be credited with fixing it.
