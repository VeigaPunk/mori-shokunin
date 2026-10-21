# ReviewFileModes — round-23 falsification (read-only seat)

Scope (assigned): production modes, the unique two-tool changed-path set, the C1 byte-transform
target sha, and the untouched baseline / policy / allowlist / history / permission controls.

Method: read-only Git (`show`/`log`/`status`/`rev-parse`/`ls-tree`/`cat-file`/`merge-base`/`diff`)
plus static reads of committed bytes. **No execution of any tool, oracle, driver or selftest was
performed** (this seat is not authorized to run a fixture/mutation/pinned-driver invocation);
every claim below is a byte-level or tree-level observation. Scratch: only
`/fast/scratch/hyaku/mori-r23/ReviewFileModes/` (extracted production copy for grep). No package
installs were performed and none were needed.

Pinned revisions used: production pin `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`; expectation
seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`; entering `1bfe708a170c877db3319060d0ab38771efe03ac`;
repo HEAD `6eb889c037163e4886eaa61501258910d6a529b9` (evidence-only commit after the pin).

---

## A. Verified axes (no defect found)

### A1 — Production modes are correct and unchanged

* `git diff --raw entering→pin -- tools/` shows **no mode column change** for the modified tool:
  `:100755 100755 414463b 78c676e M tools/mori-retention-reconcile.py`.
* The added production tool is committed executable in the same commit as the implementation
  (1979a9d): `:000000 100755 0000000 2b70064 A tools/mori-quota-surface.py`; it stays `100755`
  through the repair commits (5729e7f, 56ac3b, f3dc07c) and at the pin (`439ff4c`).
* **No file in the whole entering→pin diff changed mode**: every raw entry carries identical
  old/new mode columns. The only non-`100644`/`100755` entries in the pin tree are four
  pre-existing `120000` symlinks under `.ufo/waves/round-17/fixtures/seat/` (unrelated to r23).
* All 22 tracked files in `tools/` are `100755` at the pin; on disk every `tools/*` entry is `755`
  (`stat -c '%a'`), matching the tree (`core.fileMode=true`, and `git status` reports no mode-dirty
  tracked file).
* Both production scripts keep a `#!/usr/bin/env python3` shebang and a
  `if __name__=='__main__': raise SystemExit(main())` / `sys.exit(main())` guard
  (`tools/mori-retention-reconcile.py` tail; `tools/mori-quota-surface.py` lines 1918-1920), so
  importing either module has no host-visible side effect — the production surface is
  script-mode only.

### A2 — The changed-path set is exactly two tools (plus docs/evidence only)

`git diff --raw entering→pin -- tools/` = **exactly two paths**:

```
:000000 100755 0000000 439ff4c A  tools/mori-quota-surface.py
:100755 100755 414463b 78c676e M  tools/mori-retention-reconcile.py
```

No third production executable was added, removed or modified. Excluding the round-23 wave
directory, the whole entering→pin diff is only nine paths:

```
LOG.md, SCORECARD.md, SKILL.md, corpus/SOURCES.md,
corpus/knowledge/quota-surface-r23.md (A), corpus/knowledge/retention-reconciliation-r22.md,
corpus/lessons/round-23.md (A), tools/mori-quota-surface.py (A), tools/mori-retention-reconcile.py (M)
```

All seven documentation/knowledge edits are **insertion-only** (`git diff --numstat`:
143/0, 17/0, 41/0, 13/0, 109/0, 20/0, 125/0) — no historical byte was rewritten, so the
history control is additive, not a rewrite. The pinned driver's own guard agrees byte-for-byte
(`evidence/measure4/summary.json` → `tools_delta.expected == tools_delta.observed ==
[["A","tools/mori-quota-surface.py"],["M","tools/mori-retention-reconcile.py"]]`).

### A3 — The C1 byte-transform target sha is reproduced exactly

`frozen/c1-source-delta.json` declares `entering_sha256 0795bac9…`, `transformed_sha256
4599ee1a…`, `mode 100755`, and exactly two replacements. Independently recomputed from the
committed bytes:

| quantity | declared | recomputed at pin | match |
|---|---|---|---|
| entering `tools/mori-retention-reconcile.py` sha256 | `0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32` | same | ✅ |
| occurrence count of `SCHEMA='mori-retention-reconciliation-v1'` | 1 (implied) | 1 | ✅ |
| occurrence count of `'raw_unallowlisted':len(unallowed),` | 1 (implied) | 1 | ✅ |
| pin file sha256 | `4599ee1aff95f21714e320a87fd31260f0435aa9c7a9884ac60ab952fe099a36` | same | ✅ |
| entering bytes + the two replacements → sha256 | `4599ee1a…` | `4599ee1a…` | ✅ |
| working-tree file sha256 | — | `4599ee1a…` (identical to pin) | ✅ |
| file mode | `100755` | `100755` | ✅ |

The textual diff is exactly two hunks — line 15 (`SCHEMA` v1→v2) and line 233 (removal of the
`'raw_unallowlisted':len(unallowed),` producer fragment); the resulting `check()` payload keeps
`scanner_unallowlisted`, `raw_not_allowlisted`, `raw_total`, `policy_excluded`, `scanner_total`,
`non_author`, `allowlisted`, `forbidden_allowlist`, `retention_state`, `privacy_clearance:False`,
`tool_sha256`, `argv` — i.e. no other key, value, exit code or finding id moved
(`tools/mori-retention-reconcile.py:231-241`). Corroborated by the pinned evidence:
`evidence/measure4/summary.json` → `staged_tools` before=`0795bac9…`, after=`4599ee1a…`,
`c1_supplementary.guards.same_instance_replay` arms with `argv_equal:true`,
`identical_apart_from_special_keys:true`, and the alias counter `misleading_alias_runs 8 → 0`
with the original denominator 26/26.

### A4 — Baseline / policy / allowlist / history / permission controls are untouched

Identical blob id entering → pin for every named control:

| control | path | blob (entering = pin) |
|---|---|---|
| policy | `.ufo/waves/round-18/frozen/c1-policy.json` | `8bf285bd` |
| allowlist | `corpus/evidence/retention-allowlist.json` | `f8be55b1` |
| baseline | `corpus/evidence/baseline-r20-20261021T1051Z.json` | `5b82b42d` |
| baseline | `corpus/evidence/baseline-r10-20261015T2231Z.json` | `3bcf93ae` |
| freeze register (history) | `corpus/evidence/freeze-register.json` | `212fb95f` |
| dispositions (history) | `corpus/evidence/effective-disposition-r21.json` | `62bbd0c0` |
| permission gate (r18) | `tools/mori-retention-gate.py` | `988c5484` |

* `git diff --stat entering→pin -- corpus/evidence/` → empty; `-- .ufo/waves/round-22/` → empty.
* Seal → pin diff over `.ufo/waves/round-23/frozen/`, `.ufo/waves/round-22/frozen/`,
  `oracle-quota.py`, `oracle-rename.py`, `cases-proposed/`, `cases-corrected/`,
  `cases-supplemental/` → **empty** (frozen bytes unchanged since the seal).
* All **43** files listed in `frozen/seal-manifest.json` re-verify at the pin: sha256 **and**
  byte length match for every entry — 0 mismatches.
* Seal discipline holds: `git merge-base --is-ancestor 22772c1 pin` → true, and
  `22772c1` is also an ancestor of the implementation commit `1979a9d`; the reconciler blob at
  the seal equals the entering blob (`414463b`), and the quota production path is **absent** at
  the seal (`git cat-file -e 22772c1:tools/mori-quota-surface.py` → "exists on disk, but not in
  ..."), matching `seal-manifest.production_at_seal`.
* Open debt is carried verbatim, not cleared: `evidence/measure4/summary.json` →
  `carried_open_debt` = unallowlisted 4, `original_permission_control` "RED 11/12 retained
  byte-unchanged, not rerun", historical dispositions "two unknown", baseline acceptance
  "blocked", `privacy_clearance:false`.
* The docs cutover mandated by `preseal-amendment.md` is present and honest:
  `SKILL.md` gains a "Round23 — current reconciliation API and quota visibility" section that
  states `raw_unallowlisted` is REMOVED (not aliased) and that the tools grant no clearance;
  `corpus/knowledge/retention-reconciliation-r22.md` gains "Round23 API correction — schema-v2
  clean cutover" that explicitly marks the older alias paragraph as *historical schema-v1*.
  The remaining `raw_unallowlisted` occurrences in tracked non-`.ufo` files at the pin are
  historical narrative only (LOG.md:1527/1598, SCORECARD.md:1422, SKILL.md:556/570,
  corpus/knowledge/retention-reconciliation-r22.md:27/35/47, corpus/lessons/round-22.md:87,
  corpus/lessons/round-23.md:8/26) — no live producer or consumer of the removed key exists
  outside the frozen/case/oracle evidence.

---

## B. Findings by severity

### F1 — LOW/MEDIUM — stray, stale bytecode of the production tool inside the production tree

`tools/__pycache__/mori-quota-surface.cpython-314.pyc` (58 147 B, mtime 2026-10-21 15:17) sits in
the production `tools/` directory and is **untracked** (`git status --porcelain` → `?? tools/__pycache__/`).
`.gitignore` covers only `.ufo/interactive-sessions/` and `.ufo/worktrees/`, so nothing excludes
`__pycache__/`.

* Staleness evidence: the .pyc header records source mtime `2026-10-21 15:12:42` and source size
  `66301`, while the pinned production file is `66644` bytes (last modified 15:25) — the .pyc was
  compiled from an **earlier** revision of the production tool than the pin.
* Impact: no wrong-code risk (CPython invalidates on mtime+size mismatch), but (a) the artifact
  evidences that the production module was **imported in-process** at least once rather than only
  executed as a CLI, and (b) any future `git add -A` / broad jj-lane sweep would commit a .pyc
  into the production tree and silently enlarge the production changed-path set, which is exactly
  the invariant this wave pins.
* Recommendation: delete `tools/__pycache__/` (and F2) and add `__pycache__/` to `.gitignore`.

### F2 — LOW — generated bytecode inside a frozen/sealed directory

`.ufo/waves/round-22/frozen/__pycache__/fixture-builder-v2.cpython-314.pyc` (mtime 2026-10-21
14:00) was generated by importing the sealed r22 fixture builder. The sealed file itself is
byte-unchanged and the seal manifest enumerates named files only, so the seal is **not** violated
by the presence of the extra directory — but a directory that must remain immutable now holds
generated artifacts, with the same `git add -A` exposure as F1.

### F3 — LOW — production file self-identifies under a wave-build candidate name

`tools/mori-quota-surface.py` line 2 reads `"""mori-quota-surface-v3.py — read-only quota-surface
probe (FR2 / EDQUOT)."""` while the file's production path is `tools/mori-quota-surface.py`.
Because `parse_args` uses `description=__doc__` (`tools/mori-quota-surface.py:816-820`), the
candidate filename can surface in CLI usage/error text. Two further stale v2/v3 markers in the
same file: the selftest scratch prefix `"mori-quota-v2-"` (line 874) and the module docstring
"v2 still read the btrfs `qgroups/mode` attribute…" (line 8).
Production bytes are **not** identical to any wave candidate (production `e4857413…` vs
`build/ImplQuota/mori-quota-surface-v3.py` `5199e97b…`), i.e. the production file was edited
after the candidate drafts and only the self-names were left behind. Cosmetic; no behavioural
effect.

### F4 — LOW — identical bytes committed under two different modes

The sealed C2 oracle exists twice with identical bytes and different modes:
`.ufo/waves/round-23/oracle-quota.py` = `100644` and
`.ufo/waves/round-23/build/OracleQuota/oracle-quota-v3.py` = `100755` (both blob `4fa8d52`,
sha256 `f1f4a027…`). No functional impact: every invocation path is `sys.executable <script>`
(`tools/mori-retention-reconcile.py:266`, `tools/mori-quota-surface.py:1823`), so the exec bit is
never needed, and the pinned driver reports `oracle_sha256 = f1f4a027…` — exactly the sealed
wave-root oracle bytes, so the oracle binding is sound.

### F5 — INFORMATIONAL — production tool was briefly non-functional inside the wave

`tools/mori-quota-surface.py` was first landed at 1979a9d in a state that required the repair
commit 5729e7f ("repair classifier result unpacking"), then two further corrections (56ac3b,
f3dc07c). Seal-before-implementation ordering was respected (seal `22772c1` is a strict ancestor of
`1979a9d`), and the pinned revision is the repaired one; the window between 1979a9d and f3dc07c is
history only. No action; recorded because the pin — not the first landing — is the production
artifact under review.

### F6 — INFORMATIONAL — C2 strict-red status is consistent with the frozen contradiction

`evidence/measure4/summary.json` → `c2.after` = 29/30 with one unmet case, `real_control.match =
true`, `all_claim_checks_pass = false`. This is the declared, expected strict red of the frozen
`CaseEscapedSpace` contradiction and is **not** a defect of the changed-path set, the transform or
the untouched controls examined here; no case/rule/oracle byte was rewritten (frozen tree is
byte-unchanged since the seal, per A4).

---

## C. Residual risk and verification gaps

1. **No runtime execution from this seat.** Mode/CLI behaviour was verified statically (shebang,
   `__main__` guards, argv wiring, `sys.executable` self-spawn). Whether the pinned driver actually
   exercises every mode at the pinned bytes is asserted by `evidence/measure4/summary.json`
   (`driver_binding.executed_sha256 == sealed_sha256 == 5c12fdc0…`), which this seat did not re-run.
2. **Real-mode host reads are out of scope here.** The pin's quota tool reads
   `/proc/self/mountinfo`, `os.stat`/`realpath` and `/sys/fs/btrfs/*/qgroups/enabled` only; static
   reading confirms `qgroups/mode` is never opened in real mode (`mode = None` in
   `scan_btrfs_sysfs`, lines 569-628) and that no `quotactl`/`mount`/`xfs_quota`/`repquota` call
   path exists — but only the RerunPinnedDriver seat may perform the live DEFAULT reads.
3. **Worktree vs commit**: the production tree on disk matches the pin byte-for-byte for both
   tools, and no tracked file is dirty; the only uncommitted items are the two `__pycache__`
   directories (F1/F2) plus sibling seats' untracked wave-23 evidence and this seat's own report.
4. **Interpretation note**: "production modes" was read in both senses — file mode bits (A1) and the
   tool's operating modes (real / fixture / selftest, verified statically). The CLI surface
   observed: `--path` (repeatable, absolute-only), `--fixture` (mutually exclusive with
   `--path`), `--selftest` (mutually exclusive with both), defaults = fleet root + `/tmp`;
   unknown arguments and `--fixture`+`--path` both yield exit 2 `QUOTA_SETUP` (static read of
   `main()`/`parse_args`). A relative **`--fixture` file** path is not rejected by the
   implementation (only `--path` values are checked for absoluteness) — the contract sentence
   "relative paths → exit 2 QUOTA_SETUP" is ambiguous about the fixture file operand; no frozen
   case covers it, so this is recorded as an open interpretation question, not a defect.
5. **Scope discipline**: this seat wrote only this report and its named receipt
   (`.ufo/waves/round-23/falsify/ReviewFileModes/receipt-file-modes.json`, machine-readable
   recomputation of every hash/blob/mode statement above from committed bytes); no code, frozen,
   oracle, lane-index or sibling paths were touched; no `jj` mutation, no `git add/commit`, no live
   host quota read.

Report: .ufo/waves/round-23/falsify/ReviewFileModes.md
