# Falsification report — `CaseSetupMalformed` (round-23 C2, seat `QSetupMalformed`)

Verdict: **MATCH — the sealed case is satisfied by the pinned production tool.** No mismatch was
found for this case, and no expectation byte, fixture byte, tool byte or oracle byte was edited.

Receipt (machine-readable): `.ufo/waves/round-23/falsify/QSetupMalformed/scan.json`
Scratch (all deliberate probe artefacts): `/fast/scratch/hyaku/mori-r23/QSetupMalformed/`
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Measured revision (production pin): `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`
Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`

---

## 1. Axes

| axis | question | outcome |
|---|---|---|
| A1 truth-to-expectation | does the tool's observed verdict equal the sealed expectation (exit, `finding_id`, ordered six-field tuples)? | yes, 3/3 headline fields |
| A2 identity / provenance | are the executed bytes the pinned bytes, and the compared bytes the sealed bytes? | yes, tool sha256 identical at worktree and pin; case sha256 identical to `frozen/case-decisions.json` |
| A3 discrimination | does the case actually separate "fixture rejected" from "fixture accepted and classified"? | yes structurally (setup gate precedes any classification); no mutant executed — out of seat scope |
| A4 non-interference | fixture mode only, one child, bounded resources, no host quota reads, no writes outside scope | yes |
| A5 honesty | no overclaiming: no aggregate pass claim, wave-level red untouched, gaps declared | yes |

## 2. What was read (inputs, with byte identities)

| item | path | sha256 |
|---|---|---|
| sealed case | `.ufo/waves/round-23/frozen/quota-cases/CaseSetupMalformed.json` (9883 B) | `833cd8a536b33770ef11291ddc4e05ecd9cbf18ff7dcfa9abfe566021b916fe7` |
| selected (corrected) case | `.ufo/waves/round-23/cases-corrected/CaseSetupMalformed.json` | `833cd8a536b33770ef11291ddc4e05ecd9cbf18ff7dcfa9abfe566021b916fe7` (identical to the frozen copy) |
| sealed oracle | `.ufo/waves/round-23/oracle-quota.py` | `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` |
| tool (worktree) | `tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| tool at pin `f3dc07c0` | `git show f3dc07c0…:tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` — **identical to the worktree copy** |

Also read: `contract.md` §C2 (frozen at lane commit `4dc80c1`), `preseal-amendment.md` (C2 final
rules), `frozen/case-decisions.json` row for `CaseSetupMalformed`, the original proposal
`cases-proposed/CaseSetupMalformed.json` (retained untouched), the author's derivation report
`.ufo/waves/round-23/build/CaseSetupMalformed.md` (incl. its appended correction), the case
rationale in full, and the tool's fixture-loading path (`load_fixture`, `probe_fixture`,
`setup_payload`, `main`).

**Case under test.** Fixture top-level keys are exactly `schema`, `mountinfo`, `paths`,
`btrfs_sysfs`; the required `device_links` key is **absent** — the single deliberate defect.
Expectation: `exit = 2`, `finding_id = "QUOTA_SETUP"`, `paths = []` (no partial verdict).

## 3. Execution (fixture mode only, one child)

Fixture copy: `case["fixture"]` → `/fast/scratch/hyaku/mori-r23/QSetupMalformed/fixture.json`
(1155 B, sha256 `760e9dad34359da61f5ea532aacbb0e38625dd093f2ad8fe872ac42d3dd8db18`; re-serialized
JSON, parsed content identical to the case fixture — canonical sha256
`95a9ebf2de82516f1be5cdac9be2b703c8879fd7c9f071c7e0c9daa8d6125101` for both).

```
argv: timeout -k 2 15 prlimit --as=402653184 --nofile=256 \
      python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
      --fixture /fast/scratch/hyaku/mori-r23/QSetupMalformed/fixture.json
cwd:  /fast/scratch/hyaku/mori-r23/QSetupMalformed
env:  TMPDIR=/fast/scratch/hyaku/mori-r23/QSetupMalformed
limits: address space 402653184 B (384 MiB), wall timeout 15 s (kill after 2 s), one child at a time
```

* **exit** `2` (not `124`; the timeout never fired)
* **stderr**: empty
* **stdout** (one JSON object, verbatim):

```json
{"df_covers_quota":false,"error":"fixture_key_set","exit_code":2,"finding_id":"QUOTA_SETUP","limits":"no per-user, per-group or per-project limit or usage is read. no NFS or server-side quota and no overlay or fuse quota is covered. a visible btrfs qgroups directory does not imply that any limit is set. an ext2/ext3/ext4 quota feature in the superblock is unobservable without privileged tools. sysfs and mountinfo races during quota enable, disable or remount are not excluded. df capacity percentages never cover quota exhaustion (FR2 / EDQUOT). QUOTA_DISABLED is not a capacity or health verdict; ENOSPC can coexist. the btrfs qgroups mode attribute is never read, so btrfs_qgroups_mode is null in real mode.","paths":[],"schema":"mori-quota-surface-v1"}
```

Real mode was **not** invoked (`--fixture` only, no `--path`); the tool's `main` routes
`args.fixture is not None` → `probe_fixture` → `load_fixture`, and `load_fixture` raises
`Invalid("fixture_key_set")` before any path row is produced, which `main` converts to
`setup_payload(...)` → exit 2. No `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`, `mount`,
sysfs read, `df`, or other host read occurred; no live qgroup/mode value was read.

## 4. Comparison — primary scored fields kept separate from supplementary metadata

Primary field order (the six scored fields, unchanged): `path, fstype, mount_point,
quota_state, enforcement, basis`.

| primary field | expected | observed | match |
|---|---|---|---|
| exit | 2 | 2 | yes |
| `finding_id` | `QUOTA_SETUP` | `QUOTA_SETUP` | yes |
| ordered six-field tuples | `[]` (no path rows) | `[]` (no path rows) | yes |

Ordered tuple lists, computed explicitly from the two objects:

```
expected_tuples = []
observed_tuples = []
tuples_match    = true
```

**Primary denominator for this seat: 1 case, 1 headline comparison (exit + finding_id +
ordered tuple list) — MATCH.** This is a per-case result, not an aggregate pass claim for the
wave.

Supplementary metadata (sealed oracle's separate checks, 10 checks, reported apart from the
primary denominator): `schema`, `exit_consistency`, `output_keys_allowed`, `output_key_set`,
`error_token`, `path_key_set`, `df_covers_quota`, `setup_no_partial_verdict`, `limits_text`,
`no_leakage` — **10 pass / 0 unmet**. The setup output carries the optional top-level error token
`fixture_key_set` (matches the oracle's `[a-z_]{1,64}` token rule) and `paths == []` with
`df_covers_quota == false`, i.e. no partial verdict.

**No leakage:** the oracle's canary set (uuid `1d02a454-…`, mount source `/dev/mapper/root`,
`key=value` option tokens such as `compress=zstd:3`, `subvolid=256`, device basename `dm-0`) does
not occur in stdout; leakage hits `[]`. Independently re-checked by literal substring search:
`/dev/mapper/root`, the uuid, `dm-0`, `zstd:3`, `subvolid=256`, `noquota`, `0:57`, `259:1` and
`vgpnk` are all **absent** from stdout.

## 5. Findings

No blocking finding for this case. Three non-blocking observations for L1, none of which
changes any expectation byte or any tool byte:

1. **LOW — the setup-error output shape is a seventh key the contract never enumerates.**
   Contract §C2 specifies the output object as `schema, finding_id, exit_code, paths,
   df_covers_quota, limits`; the tool's setup output adds a top-level `error` key. The sealed
   oracle explicitly tolerates it (`allowed_keys = OUTPUT_KEYS | {"error"}`, and the token rule
   applies only to `QUOTA_SETUP`), so the case passes — but the contract itself never states
   whether a setup error carries `schema: "mori-quota-surface-v1"`, `paths: []`, and an error
   token. This is exactly ambiguity #1 the case author raised. *Recommendation (L1):* pin the
   setup-error output shape in the contract/knowledge note so a future case can assert it
   directly. No code change, no expectation change.
2. **LOW — exit code 2 is overloaded** between `QUOTA_SETUP` and `QUOTA_STATE_UNKNOWN`. This
   case's expectation is only separable because the oracle compares `finding_id` (and the path
   list), which it does. A driver keyed on exit code alone could not tell a rejected fixture
   from an unclassifiable path. *Recommendation (L1):* state the overload in the contract's
   limits prose. No code change.
3. **INFO — discrimination is structural, not mutant-proven.** The expectation is realised by
   the key-set gate in `load_fixture` (`require(set(obj.keys()) == FIXTURE_KEYS, …)`), which
   precedes any classification, so a lenient implementation that defaulted the missing
   `device_links` to `{}` would have produced `QUOTA_STATE_UNKNOWN` with two path rows
   (`btrfs_device_unmapped` for `/home/…` — the source basename `root` matches no uuid — and
   `xfs_noquota_option` for `/tmp`) instead of `QUOTA_SETUP` with no rows. I did **not** execute
   a lenient mutant: the seat is read-only for source and the assignment authorises execution of
   this one fixture-mode case only. The discrimination claim therefore rests on static reading
   of the pinned tool, not on a measured mutant.

## 6. Verification gaps and residual risk

* The sealed oracle was **not** run end-to-end over the cases directory (that would execute all
  30 sealed cases — outside this seat's authorisation). The comparison above reuses the sealed
  oracle's own `evaluate_case` / `supplementary_checks` / `leakage_hits` functions, applied to
  my single recorded run; the oracle's own `run_tool` subprocess wrapper was deliberately not
  used, so no second execution of the tool occurred.
* The sealed oracle's `TIMEOUT_S` is 30 s; this seat's mandated bound was 15 s with 384 MiB
  address space. The run returned exit 2 (not 124) well inside the bound, so the tighter limit
  is not a source of divergence.
* The fixture copy is a re-serialization of `case["fixture"]` (indent 2), so its file bytes are
  not a verbatim slice of the case file; parsed content is identical (canonical sha256 equal).
* **Scope of this verdict:** one case, one invocation. It says nothing about the other 29 sealed
  cases, and nothing about the real-mode control.
* **Wave-level context, untouched by this seat:** the strict C2 target stays **UNPROVABLE at
  29/30** because of the frozen `CaseEscapedSpace` contradiction (selected expectation 43 /
  parent 33 versus the shorter `/srv` 42, against a rule that requires `unknown`). That case was
  **not** executed here and its red is **not** excused, relabelled or excluded by this report;
  it remains a mismatch to be reported by the seat that owns it. This seat's MATCH does not
  raise, lower or excuse that number.
* The quota selftest arm (49/49, `evidence/quota-selftest-corrected.json`, after the separate
  co-evolved fixture input correction) is a different arm and is **not** this case; it is not
  cited as evidence for it.

## 7. Tooling

No tool was installed or updated: no `pacman`, `uv`, `npx`, `cargo` or release-binary install;
no channel used, therefore no tool/version/channel/reason row is owed. Only read-only repository
reads, one bounded fixture-mode invocation of the pinned tool, and writes limited to this seat's
report, this seat's receipt under `.ufo/waves/round-23/falsify/QSetupMalformed/`, and this seat's
scratch directory `/fast/scratch/hyaku/mori-r23/QSetupMalformed/`. No build, test, lint,
formatter, gate or smoke run. One byproduct was created and removed: importing the sealed oracle
module produced `.ufo/waves/round-23/__pycache__/oracle-quota.cpython-314.pyc`, which was deleted
after use so the lane carries no stray cache from this seat (the pre-existing
`.ufo/waves/round-22/frozen/__pycache__/` and `tools/__pycache__/` entries are not mine and were
left untouched). No fleet/sibling write, no production/frozen/oracle edit, no lane
index/jj/refs touch.

## 8. Files produced by this seat

* `.ufo/waves/round-23/falsify/QSetupMalformed.md` (this report)
* `.ufo/waves/round-23/falsify/QSetupMalformed/scan.json` (receipt: argv, exit, stdout, stderr,
  given/actual fixture fields, tool/case/oracle hashes, primary vs supplementary comparison,
  leakage set, scope notes)
* scratch: `/fast/scratch/hyaku/mori-r23/QSetupMalformed/{fixture.json,given.json,stdout.txt,stderr.txt}`
