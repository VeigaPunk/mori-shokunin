# FixtureLint — case-file linter for contract §C2

Seat: `MadoR22-2.FixtureLint-8`
Deliverable: `.ufo/waves/round-23/build/FixtureLint/lint-cases.py` (1131 lines)
Heavy scratch copy: `/fast/scratch/hyaku/mori-r23/FixtureLint/lint-cases.py`
Authority: `.ufo/waves/round-23/contract.md` §C2, frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`, plus the additive token layer in `.ufo/waves/round-23/preseal-amendment.md`.
Tool installs: none.

## What the tool does

`lint-cases.py DIR [DIR ...]` walks every `*.json` in each named directory and validates it as a C2 case file. It is a pure file validator: it never executes the C2 probe, never reads host state (`/proc`, `/sys`, `os.stat`), never mutates anything, and never reads a file outside the named directories.

Exit codes, as assigned:

| Code | Meaning |
|---|---|
| 0 | every case file in every directory is valid |
| 1 | at least one case file is invalid; per-file reasons printed |
| 2 | usage error (no directory, unknown option, missing directory) |

Output is one `OK`/`FAIL` line per file with `- reason` lines under each failure and `note:` lines for advisory observations. `--json` emits the same content as one JSON object (`schema: mori-quota-case-lint-v1`, counts, per-file reasons) for machine consumption.

## Checks implemented

**Case envelope** — exact key set (`schema`, `id`, `scenario`, `fixture`, `expected`, `rationale`, `sources`); `schema == mori-quota-case-v1`; non-empty one-line `scenario`; non-empty `rationale`; `sources` is a non-empty list of strings. `id` differing from the file-name stem is a note, not a failure. Duplicate `id` across files is a failure.

**Fixture format** — exact top-level key set (`schema`, `mountinfo`, `paths`, `device_links`, `btrfs_sysfs`); `schema == mori-quota-fixture-v1`; every `paths` entry has exactly `path`, `realpath`, `st_dev`; `path`/`realpath` absolute; `st_dev` matching `MAJ:MIN`; each mountinfo line parseable per proc.rst §3.5 (fields 1–6, optional fields until `-`, then fstype, source, super options), with octal escapes `040/011/012/134` decoded in a single left-to-right pass so an escaped backslash cannot be misread as a second escape.

**Expected verdict** — `expected` key set is exactly `exit`, `finding_id`, `paths`; `exit` an integer in {0,1,2}; `finding_id` a contract finding id; each expected path entry carries the six compared fields (`path`, `fstype`, `mount_point`, `quota_state`, `enforcement`, `basis`). Every token is checked against the contract table only: `quota_state` ∈ {enabled, disabled, unknown}; `enforcement` ∈ {enforced, accounting_only, unknown, n/a}; `basis` drawn from the §C2 classification table and its mount-resolution preamble. Each basis is checked against its own row, so a basis/state or basis/enforcement disagreement is a failure, as is a basis/fstype pairing that the row does not admit. `fstype` and `mount_point` are checked to be null together, matching the contract's output rule.

**Verdict precedence** — from the expected per-path states the tool derives the contract's precedence (any `enabled` → exit 1 `QUOTA_ENABLED`; else any `unknown` → exit 2 `QUOTA_STATE_UNKNOWN`; else exit 0 `QUOTA_DISABLED`) and requires the case's `exit`/`finding_id` to match. `QUOTA_ENABLED` is never suppressed by an unknown sibling, as the contract requires.

**Setup linkage** — a fixture the probe cannot classify (missing/extra top-level key, non-absolute path, malformed `st_dev`, unparseable mountinfo line, and the unreadable-field cases) licenses only a setup verdict; a case expecting a verdict finding with such a fixture is failed, and a case expecting `QUOTA_SETUP` with a classifiable fixture is failed. This is what lets the deliberately malformed fixture case pass while a well-formed fixture cannot claim a setup verdict.

**Real control** — a document whose schema is `mori-r23-c2-real-expected-v1` is validated on its own shape (`expected_exit`/`expected_finding_id`/`expected_paths`) rather than being failed as a malformed case file.

**Amendment layer (additive).** The amendment supersedes several §C2 clauses. The original rows are left unchanged and remain primary; the amendment's rows are admitted as their own basis tokens (`ext_quota_option_unverified`, `btrfs_qgroups_enabled`, `btrfs_qgroups_disabled`, `btrfs_qgroups_enabled_unavailable`, `ambiguous_overmount`), each carrying its own row, so a case written under either authority lints against its own rules instead of being failed by the other's vocabulary. Amendment device_check tokens `mismatch` and `not_checked` are admitted beside the original `match`/`btrfs_subvolume_skipped`. The amendment's required `qgroups_enabled` fixture member is type- and pairing-checked when present; a record omitting it is a note, so an original-contract case is never failed by an amendment-only rule. The amendment's other-backslash-escape rejection is recorded as a note rather than a hard failure, for the same reason.

## Deliberate tolerances (false-failure avoidance)

Recorded so the L1 can see these are choices, not oversights:

- Expected-path **order** differing from the fixture path order is a note; only a different *set* of paths is a failure. The contract fixes no output ordering.
- `id` vs file-name stem is a note — the seal step may rename files.
- Citation formatting inside `sources` is a note; only a non-list or non-string entry fails.
- `device_links` value shape (a basename, an absolute key) and `btrfs_sysfs` record key shape are notes, except where the record is unreadable.
- The three supplementary output fields (`device_check`, `quota_option_keys`, `btrfs_qgroups_mode`) are accepted as optional extras on an expected path entry, shape-checked when present, and noted — the contract's output object carries them, and the six scored fields are what the oracle compares.
- `expected.paths` non-empty under a `QUOTA_SETUP` finding is a note; the contract's setup error carries no partial verdict, but the case author may still have written one.

## Verification actually exercised (disclosure)

Per the L1 instruction, verification is closed. What was exercised, and nothing beyond it:

1. **Static parse / name resolution.** `ast.parse` plus a scope walk of the delivered file: no syntax error, no undefined global, no call to a missing function. Repeated after each edit.
2. **Pure-function checks** on contract-derived vectors only, via an in-process import of the module (the CLI is guarded under `__main__`, so importing ran no file validation): `decode_mount_point` on all four contract escapes plus a plain path; `parse_mountinfo_line` on a realistic btrfs line with optional fields, on a minimal 10-field line, and rejection of a garbage line and a truncated line; `verdict_for_states` on enabled+unknown, unknown+disabled, disabled+disabled and empty; every contract-table basis token present with its row's `quota_state`/`enforcement` matching the contract text; the five amendment basis tokens present.
3. **Two synthetic case files** built in a temporary directory from the contract, never from any proposed case: one valid btrfs case (accepted, with only the expected `qgroups_enabled` note) and a series of deliberately malformed ones — relative path, malformed `st_dev`, extra top-level fixture key, precedence violation, unknown basis token, basis/state disagreement, setup verdict without a cause, setup verdict with a cause (correctly accepted), fstype/basis disagreement. Each was rejected or accepted as intended, with the intended reason text.

**Not exercised:** the linter has never been run over `cases-proposed/`, over any sealed case directory, or over any real case file; no case file content was read while authoring. The `main()` CLI entry point itself was never invoked — the exit codes 0/1/2 are implemented and code-reviewed but not empirically confirmed. L1 owns that measurement.

**One bound deviation to disclose:** the synthetic self-check files were written under `/tmp` (Python's default `tempfile` location) before I noticed the lane bound that forbids `/tmp` for deliberate probes. The two temporary directories were removed immediately (`rm -rf /tmp/lintselfcheck-* /tmp/lintselfcheck2-*`) and are confirmed gone. Nothing was downloaded, no output was persisted there, and no lane path was touched by that detour. Verification is closed now; the remaining heavy scratch is `/fast/scratch/hyaku/mori-r23/FixtureLint`.

## Risks and blockers

- The linter validates **case files against the contract**, not against a probe implementation. It cannot tell whether an expected per-path row is *correct*, only whether it is a contract token and internally consistent with its basis and the run-level precedence. Per-path correctness remains the oracle's measurement.
- The amendment layer is additive and token-level. It does not re-derive the amendment's XFS precedence order, the tmpfs four-key hardlimit vocabulary, the ext always-unknown rule, the mount `ambiguous_overmount` detection, or the parent-ID topology refusal — the linter checks that a case *uses* the amended tokens coherently, not that the fixture would drive the amended probe to that token.
- The original §C2 basis `ext_quota_option` and the amendment's `ext_quota_option_unverified` coexist. A case using the original token lints under the original row; a case using the amended token lints under the amended row. A sealed set mixing them without a clear provenance would be ambiguous to a reader, though each file is internally consistent.
- No blocker for the bounded deliverable. The only open item is L1's post-integration measurement of the CLI exit codes.
