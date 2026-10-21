# Round 23 — C2 oracle (`oracle-quota.py`) — scoped findings

Seat: `MadoR22-2.OracleQuota-8` (oracle author, leaf).
Wave: mori round 23, claim **C2 — coverage** (FR2 quota/EDQUOT observability, capability, score held 6).
Contract read in full: `.ufo/waves/round-23/contract.md` (frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`).

## Files written

| Path | Role |
|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/OracleQuota/oracle-quota.py` | **deliverable** — the C2 oracle (executable, 20 441 B) |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/OracleQuota/oracle-quota.py` | writer clone copy, byte-identical to the deliverable |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/OracleQuota.md` | this report |

Both oracle copies are byte-identical:
`sha256 = 982753f4efdb914dedee1dadd4de8c575431d3c992aae50838c8b1f5ae3e1624`
(verified with `sha256sum` on both paths and `diff -q` → identical).

The clone was created exactly as the lane bounds require:
`git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin .scratch/round23/OracleQuota`
(git 2.56.0). No VCS mutation was performed in the lane: no `git add/commit/push`, no mutating
`jj` command; only read-only plumbing (`rev-parse`, `log`, `clone`, `status` of the clone tree)
was used.

## CLI

```
oracle-quota.py --tool PATH --cases DIR --output FILE [--real-expected FILE]
```

* `--tool` — candidate probe, e.g. `tools/mori-quota-surface.py`.
* `--cases` — directory of sealed case files; only `*.json`, **sorted by file name**.
* `--output` — observation record (JSON) path.
* `--real-expected` — optional frozen real-control file.

## Behaviour (as implemented)

Per case file `<name>.json` (in name order):

1. `case['fixture']` is written to a fixture file **beside the output**
   (`<output-stem>-quota-fixtures/<case-stem>.fixture.json`), then the tool is run as
   `[sys.executable, TOOL, '--fixture', <fixture file>]` with a **30 s timeout**.
2. stdout must parse as **exactly one JSON object** (`json.loads` → `dict`).
3. Compared facets: **process exit code**, **`finding_id`**, and the **ordered per-path tuples**
   `(path, fstype, mount_point, quota_state, enforcement, basis)` against `case['expected']`.
   Tuples are order-sensitive; `None`/JSON `null` is compared exactly; missing expected fields
   are `None`.
4. **Tool file absent → `capability_absent` for every case** (no run is attempted). Absence is
   the pre-registered "before" state and is *not* counted as a failure.

With `--real-expected` the tool is additionally run with its default paths
(`[sys.executable, TOOL]`) and compared against the frozen `expected_exit` /
`expected_finding_id` / `expected_paths`, where the per-path tuple additionally carries
**`device_check`** (7-tuple: the 6 above plus `device_check`).

### Recorded evidence (observation file, and one summary line on stdout)

* `argv` — the oracle's own argv **and** the exact argv of every tool invocation.
* `exit` — the tool's exit code (`null` on timeout).
* `stdout`, `stderr` — captured verbatim per run.
* digests — `sha256` of the **tool**, of **every case file** (plus a combined
  `cases_sha256_combined` over name→digest pairs), of the **oracle** itself, of the fixture
  files written, and of the real-control file.
* per-case row: `status` (`pass` / `unmet` / `capability_absent`), `reason`, `details`
  (facet-by-facet expected vs observed values), `run`, `fixture_path`, `fixture_sha256`.
* `counts`: `total`, `pass`, `capability_absent`, `unmet`, plus a `cases_*` breakdown
  (case checks separated from the real-control check).

**Exit status: `0` iff `unmet == 0`.** `capability_absent` is counted in its own bucket and
never makes the run fail, so the pre-registered "before" run (tool absent) exits 0 with
`capability_absent == total`. The stdout summary distinguishes the three states explicitly:

* `R23_C2_QUOTA_CASES_UNMET` — at least one check failed.
* `R23_C2_QUOTA_CAPABILITY_ABSENT` — nothing passed and something was absent (the "before" state).
* `R23_C2_QUOTA_CASES_MATCH` — all checks passed.

This avoids dressing absence up as a match in the summary line.

## Independence and constraints honoured

* Authored **blind**: from the pre-registered contract and the frozen
  `frozen/c2-expected-real.json` only. No implementation was read (neither
  `.ufo/waves/round-23/build/ImplQuota/` nor any candidate probe) and **no proposed case
  content was read** (`.ufo/waves/round-23/cases-proposed/` was not opened).
* **The oracle was not run.** No case file, no tool and no fixture was executed; the only
  validation performed was an `ast.parse` syntax check of the oracle source (parse only —
  the module is never imported or executed), plus `sha256sum`/`diff -q` on the two copies.
* No live host probe was performed by this seat: no `/proc/self/mountinfo`, no `os.stat` of
  the fleet root or `/tmp`, no `readlink` of `/dev/mapper/*`, no `/sys/fs/btrfs` listing, no
  `quotactl`/`btrfs`/`xfs_quota`/`repquota`/`mount`, no privileged or mutating command, no
  process/service/session probes, no `/tmp` usage (TMPDIR was never needed — the oracle
  writes only beside `--output`).
* No delegation, no background jobs, no L2 spawn beyond the single permitted labrat slot
  (none used — this was a leaf authoring task).

## Design decisions the L1 should know when sealing

1. **Case-file key spelling is tolerated, not assumed.** The case authors are independent of
   this oracle, so `expected` is read through documented synonyms, and the alias actually
   used is recorded per case in `details.expected_keys_used`:
   * exit: `exit_code` | `exit` | `expected_exit` | `returncode` | `return_code`
   * finding: `finding_id` | `finding` | `expected_finding_id` | `expected_finding`
   * paths: `paths` | `expected_paths` | `path_expectations` | `per_path` | `path_rows`
   * fixture: `fixture` | `fixture_json` | `fixture_object` | `fixture_data` | `fixture_document`
     (also accepted nested under `input` / `inputs` / `case`).
   If the expected exit/finding/paths are absent from `expected`, the case root is consulted
   as a fallback (recorded as `case_root:<key>`). A `expected` that is a *list* is read as the
   ordered per-path tuples with exit/finding taken from the case root.
   If no exit or no finding id can be located at all, the check is `unmet` with reason
   `expected_shape_unrecognised` — never a silent pass.
2. **Absent `paths` means "no paths".** The contract mandates "no partial verdict" on setup
   errors, so a case that omits `paths` expects an empty path list; a tool that emits paths
   there fails the check.
3. **Fixture writing.** A fixture given as an object is serialised with `indent=2,
   sort_keys=True`; a fixture given as a string is written verbatim. Both are byte-hashed and
   the hash is recorded.
4. **Exit-code comparison** accepts an integer or a numeric string (`"2"` → `2`); anything
   else is `unmet`. Finding ids are compared by exact string equality.
5. **Re-running is safe.** The fixture directory is created with `exist_ok=True` and its files
   are overwritten; the observation file is rewritten. No state outside `<output-stem>-quota-fixtures/`
   and the `--output` path is touched.
6. The real control is counted as one extra check, reported separately under `real_control`
   and also inside `checks` / `counts` (as `<real-control>`), so a drifting host is visible
   as a *drift observation* rather than a case regression.

## Risks and blockers

* **Risk — key-spelling divergence (mitigated, observable).** If the sealed cases spell a key
  outside the alias lists, the affected check reports `unmet` with
  `expected_shape_unrecognised` / `expected_paths_unrecognised`, and the alias table is
  printed in `details.expected_keys_used`. L1 should read that field once after sealing
  rather than assume the aliases cover every author.
* **Risk — case `expected` semantics for setup-error arms.** Under the contract a setup error
  yields exit 2 `QUOTA_SETUP` and no partial verdict, i.e. an empty `paths` list. If a case
  author instead pins a non-empty path list for a setup error, the check will fail against a
  conformant implementation; that is a case-authoring decision the L1 seals, not an oracle
  defect.
* **Risk — real-control drift.** `frozen/c2-expected-real.json` was frozen from an
  independent host observation (fleet root → btrfs `/home`, disabled,
  `btrfs_qgroups_dir_absent`, `btrfs_subvolume_skipped`; `/tmp` → xfs `/tmp`, disabled,
  `xfs_noquota_option`, `match`). A later differing run is host drift (remount/quota enable),
  exactly as the frozen file's own `note` states — it is reported as an `unmet` real-control
  check with the observed facets attached, never rewritten into the oracle.
* **Current state (measured by listing only, no execution):** `tools/mori-quota-surface.py`
  does **not** exist yet in the lane, so the "before" oracle run will report
  `capability_absent` for every sealed case — the pre-registered expectation.
* **Blocker for the "after" measurement:** the oracle can only be exercised by the L1 after
  (a) the cases are sealed and (b) the implementation lands. Both are outside this seat.
* **No blockers for the deliverable itself.**

## Tooling / environment record

* No package was installed or updated in this wave: the oracle uses the **Python 3.14.8**
  standard library only (`argparse`, `hashlib`, `json`, `subprocess`, `sys`, `pathlib`).
* `git` 2.56.0 was used once, read-only, to create the mandated writer clone.
* No full-system upgrade, no service restart, no credential/session material was read.

---

# Addendum — strict v2 oracle (`oracle-quota-v2.py`), added on L1 request

L1 asked (via `agent://MadoR22-2`) for a stricter sibling oracle with **exact case keys/schema only**,
**no aliases**, **no missing expected paths accepted**, plus the supplementary schema/exit/key-set,
`device_check`, options and mode validation requested by `.ufo/waves/round-23/preseal-amendment.md`,
keeping the six-field match as the headline and reporting supplementary checks separately.

## Files (v2)

| Path | Role |
|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/OracleQuota/oracle-quota-v2.py` | **deliverable** — strict v2 oracle (executable, 17 940 B) |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/OracleQuota/oracle-quota-v2.py` | writer-clone copy, byte-identical |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/OracleQuota.md` | this addendum (appended; original section untouched) |

`oracle-quota-v2.py` sha256 = `08c9feb929fbbbe769d75d3ecdc342e5a70a744169dcc21aee0b0951243bbbeb`
(both copies identical).

**The v1 deliverable is untouched and still byte-identical**: `oracle-quota.py`
sha256 = `982753f4efdb914dedee1dadd4de8c575431d3c992aae50838c8b1f5ae3e1624` (re-verified after v2
was written; `sha256sum` on the lane copy and the clone copy).

## Canonical case schema enforced by v2 (no aliases, no missing paths)

```
case file   : exactly {"fixture": <object>, "expected": <object>}
expected    : exactly {"exit_code": <int>, "finding_id": <str>, "paths": [...]}
path entry  : exactly {"path","fstype","mount_point","quota_state","enforcement","basis"}
              plus, optionally, "device_check", "quota_option_keys", "btrfs_qgroups_mode"
```

Any deviation is a hard `unmet` with an explicit reason (`case_key_set:[...]`,
`expected_key_set:[...]`, `expected_paths_not_list`, `expected_path_key_set:[...]`) — never a
silent pass, never an alias read. An alias spelling simply violates the exact key sets and is
rejected. The three key sets live in three constants at the top of the file
(`CASE_KEYS`, `EXPECTED_KEYS`, `PATH_KEYS`/`ALLOWED_PATH_KEYS`) so the L1 can re-pin them in one
edit if the seal uses a different spelling.

## Headline vs supplementary (denominators kept apart)

* **Headline (scored, unchanged denominator):** exit code + `finding_id` + the ordered six-field
  per-path tuples. Reported as `counts = {total, pass, capability_absent, unmet}` exactly as in
  v1; `capability_absent` (tool file absent) remains a non-failure bucket, so the "before" run
  exits 0 with `capability_absent == total`.
* **Supplementary (reported separately, never folded into the headline):** `supplementary_counts`
  and a flat `supplementary_checks` list. Per run:
  1. `schema` — `mori-quota-surface-v1`.
  2. `exit_consistency` — the tool's own `exit_code` field equals the process exit code.
  3. `output_key_set` — exactly `{schema, finding_id, exit_code, paths, df_covers_quota, limits}`.
  4. `path_key_set` — every observed path entry carries exactly the nine contract keys
     (`path, fstype, mount_point, quota_state, enforcement, basis, device_check,
     quota_option_keys, btrfs_qgroups_mode`).
  5. `df_covers_quota` — is `false`.
  6. `limits_text` — non-empty string.
  7. `device_check[i]` — compared **where the case pins it**; the observed value must also be one
     of `{match, mismatch, not_checked, btrfs_subvolume_skipped}`.
  8. `quota_option_keys[i]` — compared **where the case pins it**; the observed value must be a
     sorted, duplicate-free list of strings.
  9. `btrfs_qgroups_mode[i]` — compared **where the case pins it**; `null` or one of
     `{qgroup, squota}` (informational only; never raw text).
  10. `no_leakage` — the fixture's btrfs UUIDs, the mount sources (raw and octal-decoded) and the
      super-option values (`key=value` tokens, and distinctive bare values) must not appear in the
      tool's stdout. Skipped, not faked, when the case has no fixture basis (real control).

**Exit status:** 0 iff the headline has no `unmet` **and** the supplementary set has no `unmet`.
The headline denominator is untouched by the supplementary assertions (they are counted
separately), but a driver that only reads the exit code cannot miss a supplementary violation.
Summary `finding_id`: `R23_C2_QUOTA_CASES_UNMET` (headline) → `R23_C2_QUOTA_SUPPLEMENTARY_UNMET`
(supplementary only) → `R23_C2_QUOTA_CAPABILITY_ABSENT` (nothing passed, tool absent) →
`R23_C2_QUOTA_CASES_MATCH`.

**Real control (v2):** the frozen file is read with its own strict keys
(`expected_exit`, `expected_finding_id`, `expected_paths`), each expected path entry must carry
exactly the seven fields (six + `device_check`), and the same supplementary checks run against the
real output — minus `no_leakage`, which has no fixture basis in real mode (the oracle performs no
host reads; that is not this seat's permitted read).

## Deltas v1 → v2

| Aspect | v1 (`oracle-quota.py`) | v2 (`oracle-quota-v2.py`) |
|---|---|---|
| Case key handling | alias-tolerant (`exit_code`/`exit`/`expected_exit`, …), case-root fallback, nested fixture fallbacks | exact key sets only; no aliases; no fallback; missing `paths` rejected |
| Missing `expected.paths` | accepted as "no paths" | rejected (`expected_key_set`) |
| Expected path entries | dicts or 6-arrays | dicts with the six keys (+ up to three supplementary keys) |
| Supplementary checks | none | 10 named checks, reported separately |
| `device_check` / options / mode | compared only for the real control | compared for cases too, where pinned |
| Leakage | not checked | UUID / mount-source / option-value leakage checked |
| Output key set | not checked | exact top-level and per-path key sets |
| Exit status | 0 iff headline `unmet == 0` | 0 iff headline `unmet == 0` **and** supplementary `unmet == 0` |
| Implementation | ~490 lines with alias tables | ~395 lines, three constants, no alias machinery |

## Independence and constraints (v2)

* Authored from `preseal-amendment.md` + `contract.md` + `frozen/c2-expected-real.json` only.
* **The candidate was not inspected** (no implementation read; `tools/mori-quota-surface.py` still
  absent in the lane) and **no proposed case content was opened** — the canonical case schema was
  derived from the contract and the seat's own task statement, not from the case authors' files.
* **v2 was not run.** Validation was static only: `ast.parse` plus a scope-aware
  name-resolution pass over both oracle files (no unresolved names; only the expected
  closure artefact in the checker). No case file, tool or fixture was executed.
* No host probe, no privileged/mutating command, no `/tmp` use, no delegation, no lane VCS mutation.

## Risks (v2)

* **Seal conformance.** v2 rejects any case whose key sets differ from the canonical schema
  above. If a sealed case carries extra metadata keys (e.g. a `name` field) or a different
  spelling, that case reports `unmet` with the actual key set printed — a loud, one-line-fix
  failure rather than a silent mis-measurement. Re-pin via `CASE_KEYS` / `EXPECTED_KEYS` /
  `PATH_KEYS` at the top of the file, or align the seal.
* **Exact per-path key set.** The contract lists nine per-path keys; an implementation that omits
  one (e.g. `quota_option_keys` for an unsupported fstype) fails `path_key_set` as a supplementary
  violation even though the six-field headline passes.
* **Leakage false positives.** The leakage check inspects only fixture-derived strings (UUIDs,
  absolute mount sources, option tokens/values). Non-path sources (`proc`, `none`, `sysfs`) are
  skipped on purpose, and bare option values shorter than four characters or purely numeric are
  skipped, to avoid flagging ordinary text.
* **Real-control leakage is not checked** (no fixture basis, no host reads in this seat). That is
  a known coverage gap of v2, recorded rather than faked.

---

# Addendum 2 — v3 oracle (`oracle-quota-v3.py`), written to the W1 case contract

L1 rejected v2's invented envelope ("your v2 canonical keys contradict explicit W1 case
contract") and required: exact W1 case keys, `expected` keyed by **`exit`** (not `exit_code`),
`schema` = `mori-quota-case-v1`, primary `paths` exactly six keys, an optional separate
`supplementary_expected` whose shape is documented, a corrected leakage canary rule, and **no
mutation of any author's case file**. v1 and v2 are preserved byte-for-byte; v3 is a third
sibling.

## Files (v3)

| Path | Role |
|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/OracleQuota/oracle-quota-v3.py` | **deliverable** — strict oracle on the W1 contract (executable, 22 196 B) |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/OracleQuota/oracle-quota-v3.py` | writer-clone copy, byte-identical |

Digests after v3 was written (all three siblings present, originals unchanged):

| File | sha256 | bytes |
|---|---|---|
| `oracle-quota.py` (v1) | `982753f4efdb914dedee1dadd4de8c575431d3c992aae50838c8b1f5ae3e1624` | 20 441 |
| `oracle-quota-v2.py` (v2) | `08c9feb929fbbbe769d75d3ecdc342e5a70a744169dcc21aee0b0951243bbbeb` | 17 940 |
| `oracle-quota-v3.py` (v3) | `3a55781773875d104634989fc8a2435de9ff63856004cb82fc71ee5cc786f09f` | 22 196 |

## Canonical case schema enforced by v3

```
case file  : exactly {schema, id, scenario, fixture, expected, rationale, sources}
              + optional {supplementary_expected}; any other key => unmet
schema     : exactly "mori-quota-case-v1"      (value checked, not just presence)
expected   : exactly {exit, finding_id, paths}  (the key is `exit`)
path entry : exactly {path, fstype, mount_point, quota_state, enforcement, basis}
fixture    : passed through untouched — the oracle never judges fixture shape, because a
              deliberately malformed fixture (e.g. `device_links` absent) is a case in its own right
```

No alias reading anywhere: an alias spelling simply violates the exact key sets and is rejected
with the offending key set printed (`case_key_set:[...]`, `case_missing_keys:[...]`,
`case_schema_value:...`, `expected_key_set:[...]`, `expected_path_key_set:[...]`).

### `supplementary_expected` — documented accepted shapes

Optional, separate top-level key (never inside `expected.paths[]`, whose six keys stay exactly
the six scored facets). Accepted:

1. **list** — parallel to `expected.paths`; each item is an object whose keys are a subset of
   `{device_check, quota_option_keys, btrfs_qgroups_mode}` (empty object = nothing pinned).
2. **`{"paths": [ ... ]}`** — the same list nested under `paths`.
3. **`{"0": {...}, "1": {...}}`** — index-keyed map of the same per-path objects.
4. **flat `{device_check: ..., ...}`** — applies to the single expected path; only valid when
   `expected.paths` has exactly one entry (`supplementary_expected_flat_ambiguous` otherwise).

Length mismatches and unknown keys are rejected (`supplementary_expected_length`,
`supplementary_expected_keys:[...]`, `supplementary_expected_shape`). A missing or `null`
`supplementary_expected` means "nothing pinned" and yields no supplementary check.

## Leakage canary rule (corrected)

Canaries are drawn only from the fixture handed to the tool, and only these strings are scanned:

* every btrfs UUID key of `btrfs_sysfs`;
* every **absolute** mount source from the fixture's mountinfo (raw and octal-decoded);
* every **full** `key=value` super-option token;
* every **distinctive** option value — the part after `=`, only when it is ≥ 5 characters,
  contains a non-alphanumeric character, and is not an ordinary value;
* every distinctive device basename from `device_links` / `btrfs_sysfs[*].devices` (≥ 3 chars,
  non-alphanumeric, not a substring of a mount source).

**Never scanned:** option keys (`usrquota`, `noquota`, … — they legitimately appear in
`quota_option_keys`), ordinary values (`rw`, `ro`, `relatime`, `0`, `1`, `defaults`, …),
mount points, the case paths, and the fixture's own `realpath`/`st_dev`. v2's over-broad
"any bare option value ≥ 4 chars" rule is gone.

## Headline, supplementary, exit status (unchanged semantics from v2)

* **Headline (scored, six-field denominator):** exit code + `finding_id` + the ordered six-field
  per-path tuples. `counts = {total, pass, capability_absent, unmet}`; `capability_absent` (tool
  absent) stays a non-failure bucket, so the "before" run exits 0 with `capability_absent == total`.
* **Supplementary (separate counters and a flat check list):** `schema` = `mori-quota-surface-v1`;
  the tool's `exit_code` field equals the process exit; exact top-level key set
  `{schema, finding_id, exit_code, paths, df_covers_quota, limits}`; exact per-path nine-key set;
  `df_covers_quota` false; `limits` a non-empty string; `device_check` / `quota_option_keys` /
  `btrfs_qgroups_mode` compared where pinned (with shape and allowed-value rules); `no_leakage`
  under the corrected canary rule (skipped, not faked, when the case has no fixture basis — the
  real control).
* **Exit status:** 0 iff the headline has no `unmet` **and** the supplementary set has no
  `unmet`. Summary `finding_id`: `R23_C2_QUOTA_CASES_UNMET` → `R23_C2_QUOTA_SUPPLEMENTARY_UNMET`
  → `R23_C2_QUOTA_CAPABILITY_ABSENT` → `R23_C2_QUOTA_CASES_MATCH`.
* The frozen real control keeps its own strict keys (`expected_exit`, `expected_finding_id`,
  `expected_paths` with the seven fields including `device_check`); the case-schema change does
  not touch it.

## Deltas v2 → v3

| Aspect | v2 | v3 |
|---|---|---|
| Case keys | invented `{fixture, expected}` | W1 `{schema, id, scenario, fixture, expected, rationale, sources}` + optional `supplementary_expected` |
| `expected` | `exit_code` | `exit` (W1 spelling) |
| Case `schema` value | not checked | must equal `mori-quota-case-v1` |
| Expected path keys | six + three optional inline | exactly six; supplementary values live in the separate `supplementary_expected` |
| Supplementary source | inline in expected path rows | separate top-level key, four documented shapes |
| Leakage canaries | full tokens + any bare value ≥ 4 chars | full sources / UUIDs / full `key=value` / distinctive non-common values only |
| Fixture validation | none | none (unchanged, deliberately) |

## Independence and constraints (v3)

* No candidate read, no candidate run, no oracle run. The W1 key convention was confirmed from
  the L1 instruction and from the key-set statements in peer case **reports**
  (`build/Case*.md`); **no case JSON file was opened**, and no expectation value is hard-coded
  anywhere — expectations are read from the sealed case files at run time.
* No author's case file was modified; v3 accepts the W1 shape as written.
* No host probe, no privileged/mutating command, no `/tmp` use, no delegation, no lane VCS
  mutation; v1 and v2 left byte-identical (digests re-verified above).
* Static validation only: `ast.parse` plus a scope-aware name-resolution pass over all three
  oracle files (no unresolved names beyond the checker's known closure artefact on the local
  `add` helper, which is defined before use).

## Risks (v3)

* **Supplementary shape drift** — *resolved by Addendum 3*: the canonical wrapper
  `{note, paths:[{path, device_check, quota_option_keys, btrfs_qgroups_mode}]}` is now the
  implemented shape, so the author's file is read as written. Any other shape still fails loudly
  (`supplementary_expected_shape`) rather than silently dropping an assertion.
* **Exact output key set.** An implementation that adds an output key fails the supplementary
  `output_key_set` check while the six-field headline still passes; that is the intended
  separation and is visible in `supplementary_checks`.
* **Canary false positives** are now limited to full sources, UUIDs, full `key=value` tokens and
  distinctive values; ordinary values are excluded by construction.
* **Real-control leakage** remains unchecked (no fixture basis, no host reads in this seat) — an
  acknowledged coverage gap, recorded rather than faked.

---

# Addendum 3 — v3 surgical edit (canonical `supplementary_expected` wrapper)

L1 supplied the last canonical detail from the wave-1 author (no candidate involved): the real
`supplementary_expected` wrapper is

```json
{"note": "<prose>",
 "paths": [{"path": "<row identity>", "device_check": ..., "quota_option_keys": ..., "btrfs_qgroups_mode": ...}]}
```

v3 was **not sealed** when this arrived, so it was edited **surgically in place** (no v4, no
version proliferation). v1 and v2 stay byte-identical.

## Checksums (before → after the surgical edit)

| File | sha256 before | sha256 after | bytes after |
|---|---|---|---|
| `oracle-quota.py` (v1) | `982753f4efdb914dedee1dadd4de8c575431d3c992aae50838c8b1f5ae3e1624` | **unchanged** | 20 441 |
| `oracle-quota-v2.py` (v2) | `08c9feb929fbbbe769d75d3ecdc342e5a70a744169dcc21aee0b0951243bbbeb` | **unchanged** | 17 940 |
| `oracle-quota-v3.py` (v3) | `3a55781773875d104634989fc8a2435de9ff63856004cb82fc71ee5cc786f09f` | `07639853408b640e95e8384b247171d34b8d45b93d73f189e84c874e34720feb` | 23 761 |

The superseded v3 checksum `3a55781773875d104634989fc8a2435de9ff63856004cb82fc71ee5cc786f09f` is
preserved here for the seal audit trail. Lane copy and writer-clone copy of v3 are byte-identical
(`diff -q` clean).

## What changed in v3 (surgical, nothing else)

* `read_supplementary(case_obj, expected_paths)` now reads the canonical wrapper:
  * `note` — prose; **never compared and never echoed**. The case row records only
    `supplementary_note_present: true/false`; the text never reaches the observation file.
  * `paths` — the row list. Each row must be an object whose keys are a subset of
    `{path, device_check, quota_option_keys, btrfs_qgroups_mode}`; `path` is the **verified
    identity** of the expected row it describes: it must match an entry of `expected.paths`, the
    match must be unique, and the matched rows must keep the order of `expected.paths`.
  * Only the fields actually given are compared, and only those land in the supplementary checks
    (`device_check`, `quota_option_keys`, `btrfs_qgroups_mode`). The metadata never enters the
    scored six-field primary expectation — no unscored claim is made for it.
  * A bare list of the same row objects is still accepted; any other wrapper shape is rejected
    loudly (`supplementary_expected_keys:[...]`, `supplementary_expected_shape`,
    `supplementary_expected_paths_not_list`).
* New rejection reasons for a malformed wrapper:
  `supplementary_expected_row_without_path`, `supplementary_expected_path_unknown:<path>`,
  `supplementary_expected_path_ambiguous:<path>`, `supplementary_expected_out_of_order:<path>`.
* Module docstring updated to the canonical wrapper.

## Unchanged in v3 (re-confirmed against the final amendment)

* Canonical case schema: exactly `{schema, id, scenario, fixture, expected, rationale, sources}`
  plus optional `supplementary_expected`; `schema` must equal `mori-quota-case-v1`;
  `expected` exactly `{exit, finding_id, paths}`; each expected path exactly the six scored keys.
* Fixture is never judged by the oracle (deliberately malformed fixtures remain cases).
* Headline (scored): exit code + `finding_id` + ordered six-field tuples; `capability_absent`
  remains a non-failure bucket (before-state exits 0).
* Supplementary, reported separately: `mori-quota-surface-v1` schema, `exit_code` field equals
  the process exit, exact top-level key set, exact per-path nine-key set, `df_covers_quota` false,
  `limits` non-empty, the three metadata fields where given, and the corrected `no_leakage`
  canary rule (full sources, UUIDs, full `key=value` tokens, distinctive non-common values only;
  ordinary values such as `rw`, `0`, `1` and option keys are never scanned).
* Output spelling `btrfs_qgroups_mode` (fixture input keeps `qgroups_mode`), `enforcement` literal
  `n/a`, `quota_option_keys=[]` / `btrfs_qgroups_mode=null` on the no-cover, ambiguous and
  device-mismatch preemption arms — all consistent with what the oracle compares.
* Frozen real control keeps its own strict keys (`expected_exit`, `expected_finding_id`,
  `expected_paths` with `device_check`).

## Independence and constraints (unchanged)

No candidate read, no candidate run, no oracle run, no case JSON opened, no author file mutated.
Static validation only (`ast.parse`, arity check of every `read_supplementary` return, and a
scope-aware name-resolution pass whose only reports are the known closure artefact for the local
`add` helper, which is defined before use).

---

# Addendum 4 — v3 surgical edit (optional setup `error` token)

L1 clarified the source schema before sealing: the amendment says a `QUOTA_SETUP` error carries a
**fixed token**; an optional top-level `error` key is permitted **only** when `finding_id` is
`QUOTA_SETUP`, must be a nonempty ASCII `[a-z_]+` string of at most 64 characters and must not
carry input text. Every other output keeps exactly the six documented keys. The contract never
mandated whether `error` is present, so both variants are valid on the setup path.

v3 was still unsealed, so it was edited **surgically in place** — no v4, no version proliferation.
v1 and v2 remain byte-identical.

## Checksums (before → after this edit)

| File | sha256 before | sha256 after | bytes after |
|---|---|---|---|
| `oracle-quota.py` (v1) | `982753f4efdb914dedee1dadd4de8c575431d3c992aae50838c8b1f5ae3e1624` | **unchanged** | 20 441 |
| `oracle-quota-v2.py` (v2) | `08c9feb929fbbbe769d75d3ecdc342e5a70a744169dcc21aee0b0951243bbbeb` | **unchanged** | 17 940 |
| `oracle-quota-v3.py` (v3) | `07639853408b640e95e8384b247171d34b8d45b93d73f189e84c874e34720feb` | `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` | 25 391 |

Both superseded v3 checksums are preserved here for the seal audit trail
(`3a55781773875d104634989fc8a2435de9ff63856004cb82fc71ee5cc786f09f`, then
`07639853408b640e95e8384b247171d34b8d45b93d73f189e84c874e34720feb`). Lane copy and writer-clone
copy of v3 are byte-identical (`diff -q` clean).

## What changed in v3 (surgical, nothing else)

* New constant `ERROR_TOKEN_RE = re.compile(r"[a-z_]{1,64}")` and `import re`.
* The single `output_key_set` check became two, plus two new ones:
  * `output_keys_allowed` — the top-level keys are a subset of the six documented keys plus the
    optional `error`.
  * `output_key_set` — for `finding_id == "QUOTA_SETUP"`: the six keys, optionally plus `error`;
    for every other finding: **exactly** the six keys (so `error` is rejected elsewhere).
  * `error_token` — when `error` is present it must be a string matching `[a-z_]{1,64}`
    (nonempty, ASCII, ≤ 64 chars) **and** the finding must be `QUOTA_SETUP`. When `error` is
    absent the check passes (both variants are valid on the setup path).
  * `setup_no_partial_verdict` — when `finding_id == "QUOTA_SETUP"`: `paths == []` and
    `df_covers_quota is False` (no partial verdict, no capacity claim).
* Module docstring documents the output key set and the optional setup token.

Everything else in v3 is unchanged: canonical case schema
(`{schema, id, scenario, fixture, expected, rationale, sources}` + optional
`supplementary_expected`, `schema == "mori-quota-case-v1"`, `expected == {exit, finding_id, paths}`,
six-key expected path rows), the canonical `supplementary_expected` wrapper with its `note` prose
never compared or echoed and `path` as verified row identity, the scored six-field headline with
`capability_absent` as a non-failure bucket, the separate supplementary set (schema, exit
consistency, per-path nine-key set, `df_covers_quota`, `limits`, the three metadata fields where
given, corrected `no_leakage` canaries), and the frozen real control with its own strict keys.

## Validation

Static only: `ast.parse`; scope-aware name-resolution pass (no unresolved names beyond the known
closure artefact for the local `add` helper, defined before use); the token pattern was exercised
directly on sample strings (`quota_setup`, `setup`, 64×`x` accepted; empty, 65×`x`, `Quota_Setup`,
`quota setup`, `setup-1` rejected). No oracle, tool or case file was executed; no candidate was
inspected.




