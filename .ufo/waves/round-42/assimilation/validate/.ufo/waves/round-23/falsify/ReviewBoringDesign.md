# ReviewBoringDesign — bounded source-level maintainability review of the pinned quota production code

**Verdict: 0 deletions made (read-only seat, no code edits), 15 findings — 3 medium, 12 low —
of which 2 are correctness-bearing and 1 is a duplicate-authority finding.** The pinned
quota probe is functionally careful (output minimisation, refusal over guessing, no
privileged interface), but it carries a **candidate-era header that misidentifies the
shipped artifact**, **one basis token that names a cause that did not occur**, and a
**second, hand-written expectation table that duplicates the sealed case corpus**. None
of these change the frozen case/rule/oracle bytes, and none of them is a reason to
re-run or re-cut anything in this round: the advice below is for the next revision that
touches this file.

---

## 1. Scope, artifacts, identities

| item | identity |
|---|---|
| production pin | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` |
| lane HEAD at review | `6eb889c037163e4886eaa61501258910d6a529b9` (pin is an ancestor) |
| reviewed file | `tools/mori-quota-surface.py` at the pin |
| blob sha256 | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` (66644 bytes, 1920 lines) |
| working-tree copy | identical sha256 (`e4857413…`) — the working tree and the pin agree |
| HEAD blob | identical sha256 (`e4857413…`) — no post-pin drift in this file |
| build artifact compared | `.ufo/waves/round-23/build/ImplQuota/mori-quota-surface-v3.py`, sha256 `5199e97b5ac89a39b3f047586a6e624d7e95041415390750a93f91bf15d55129` |
| sibling build artifacts | `…/ImplQuota/mori-quota-surface.py` `6b553154…`, `…/ImplQuota/mori-quota-surface-v2.py` `5c8b251d…` (wave artifacts, not shipped) |
| sealed expectation corpus | `.ufo/waves/round-23/frozen/quota-cases/` — 30 case files (27 original-derived + 3 supplemental) |
| other authority read | `SKILL.md:586` (r23 quota-surface row), `corpus/knowledge/quota-surface-r23.md`, `.ufo/waves/round-23/contract.md`, `.ufo/waves/round-23/preseal-amendment.md`, `.ufo/waves/round-23/build/MeasureDriver/measure-round23.py` |

All line numbers below refer to the pinned blob `e4857413…`.

## 2. Method and what was deliberately not done

* **Static only.** AST parse + literal text search + hand reading of the pinned bytes.
  The probe was **never executed** — not in fixture mode, not in `--selftest`, not in real
  mode. No oracle, driver, gate, build, test, linter or formatter was run. This seat's
  item does not authorize a fixture/mutation/pinned-driver invocation.
* **No live host reads.** No `/proc/self/mountinfo`, no `/sys/fs/btrfs`, no `stat` of a
  runway target, no `df`, no quota interface of any kind.
* **No semantic reference proof was possible.** The `lsp` device is **not mounted** in
  this environment (`read xd://lsp` → `No such tool`; the mounted-device list contains no
  language-server device). Every "no caller" statement below is therefore a **literal
  text search over the committed tree**, which is the documented fallback and is *not*
  semantic proof. It is recorded as such and never presented as an absence proof.
* Search scope excluded `.git/`, `.jj/` and `.scratch/` from every claim. One early
  repository-wide grep incidentally printed `.scratch/round23/**` (untracked wave copies);
  no claim in this report rests on `.scratch/` bytes, and every cited path was re-read
  from the committed tree.
* **No VCS mutation, no lane index / jj / refs change, no sibling write, no install.**
  No tool was installed or updated (nothing was needed); there is therefore no
  tool/version/channel/reason entry to report.
* Files written: this report only. Scratch copies (read-only extractions of the two
  pinned tools) live under `/fast/scratch/hyaku/mori-r23/ReviewBoringDesign/`.
* **Shared-tree state observed while reviewing** (recorded, not touched):
  `git status --porcelain --untracked-files=no` reported exactly one modified tracked
  file, `.ufo/waves/round-23/build/RevengeTmpfsQuota.md`. That edit is **not** this
  seat's — this seat wrote no file inside the lane other than this report and no file
  outside it but the scratch directory. The pinned quota tool, the reconciler and every
  frozen byte are unchanged by this review; the report makes no claim about the
  `RevengeTmpfsQuota.md` edit.

## 3. Axes

1. **Correctness preservation** — a change must not alter the six scored fields, exit
   codes, finding ids, or the sealed expectations.
2. **Single authority** — one statement per fact; no duplicated vocabulary, duplicated
   expectation table, or duplicated selection rule.
3. **Dead weight** — code and prose that no live path consumes.
4. **Diagnosability** — when the tool cannot answer, does it name the real cause?
5. **Documentation truth** — does the artifact describe itself as it actually is?

Moves kept here: **advice only**. Every finding below is stated as a candidate change
for a future revision, with its trade-off, so that no axis is harmed while the current
round's frozen bytes and strict red stay exactly as they are.

---

## 4. Findings

### F1 — Medium — the shipped file's header describes a different artifact

`tools/mori-quota-surface.py:2` opens `"""mori-quota-surface-v3.py — read-only
quota-surface probe (FR2 / EDQUOT).` and `:4-8` continue:

> "This is the round-23 pre-seal amendment candidate for contract §C2 … It is a new
> candidate authored alongside `mori-quota-surface.py` (the original, unaltered) and
> `mori-quota-surface-v2.py` (preserved as the rejected unsafe-read source evidence …)"

In the shipped tree this is false three ways over:

* the file's own name is `mori-quota-surface.py`, not `mori-quota-surface-v3.py`;
* `tools/` contains **exactly one** quota tool — the two named siblings exist only as
  wave build artifacts under `.ufo/waves/round-23/build/ImplQuota/`, so the header
  points at paths that do not exist where it says they do;
* the shipped bytes are **not** the v3 candidate: they differ from
  `build/ImplQuota/mori-quota-surface-v3.py` in seven hunks (551, 711, 715-716, 781,
  792, 1537, 1776-1789) — the `classify()` return shape, the strict fixture path rules,
  the `limits` field shape (joined text vs list), the co-evolved selftest device input,
  and two added setup arms. So "the original, unaltered" names as a *different* file the
  very file that was shipped and later amended.

**Why it matters (correctness consequence, doc axis).** The header is the only in-code
statement of the CLI and output contract, and it is wrong about the artifact and
incomplete about the accepted inputs: the shipped code additionally requires a
**nonempty** `paths` list (`:711`) and an **exact** per-path key set (`:715-716`), and
emits `limits` as joined text (`:781`, `:792`) — none of which the header states. Three
authorities now disagree about this tool: the header, `SKILL.md:586`, and
`corpus/knowledge/quota-surface-r23.md`. A maintainer who trusts the header will look
for `mori-quota-surface-v2.py` in `tools/`, will not find it, and will not learn that
the shipped fixture grammar is stricter than the header's "fixture validation is strict
(normalized unique absolute paths, canonical st_dev, canonical UUID keys, plain
basenames, exact record key sets)" line implies.

**Minimal remedy (next revision touching this file).** Replace the header with a
production-tool header: the tool's real name, what it reads, what it refuses, the CLI
surface, the output keys, and the fixture acceptance rules the code actually enforces.
Delete the "WHAT CHANGED IN v3" diff narrative (it is a changelog, not a contract) and
the "authored alongside …" provenance paragraph. Keep the readset paragraph and the
"never reads `qgroups/mode`" paragraph verbatim — those are the load-bearing
safety statements. **Trade-off:** the header loses the candidate history; that history
already lives in `.ufo/waves/round-23/build/ImplQuota/` and in `git log`, so nothing is
lost from the lane.

### F2 — Medium — a btrfs sysfs inspection failure is reported as a *device* failure

`classify_btrfs` (`:465-483`):

```python
    if record["qgroups"] is None:
        # The qgroups state could not be inspected: never absent, never disabled.
        return ("unknown", "n/a", "btrfs_device_unmapped"), None
```

The state is right (`unknown`, enforcement `n/a`) — the refusal is correct. The **basis
token is wrong**: it says the *device* was unmapped, when in fact the device mapped
exactly one UUID (the preceding `len(matched) != 1` test already returned for that
case) and the qgroups **directory state** could not be inspected.

Reachability: fixture mode cannot reach it — `load_fixture` requires
`type(qgroups) is bool` (`:753`), so `qgroups` is never `None` there. It is
**real-mode only**, via `scan_btrfs_sysfs`, where `os.stat(<uuid>/qgroups)` raises a
non-`FileNotFoundError` `OSError` and leaves `qgroups = None` (`:601-606`).

**Why it matters (correctness consequence, diagnosability axis).** The basis token is
part of the per-path output contract and is what a consumer keys on to learn *why* a
path is unknown. Two materially different unknowns — "no UUID claims this device" and
"the qgroups state could not be read" — are collapsed onto one token that names the
first. The committed knowledge note lists them as one row ("btrfs device
unassociated/ambiguous, **or sysfs access error** → unknown; do not borrow a different
UUID or conflate access failure with absence"), but the tool's vocabulary does not
keep them apart, so a real-mode access failure is indistinguishable from a mapping
failure — and it is indistinguishable from the genuine unmapped case that *does* mean
"device unmapped". A reader chasing a real-mode unknown on a btrfs path is sent to the
device-mapping question instead of the permission/inspection question.

**Minimal remedy.** Give the inspection failure its own token (e.g.
`btrfs_qgroups_state_unobservable`), leaving `btrfs_device_unmapped` for the
zero-/multi-UUID case. **No state, enforcement, exit code or finding id changes.**
**Trade-off:** this changes a per-path `basis` string in real mode. It does **not**
touch any sealed case: no frozen case produces `qgroups = None` (fixture mode forbids
it), and the frozen real control's fleet-root row expects
`btrfs_qgroups_dir_absent` (a *successful* parent inspection), so the frozen bytes and
the frozen control stay valid. It would need a re-worded knowledge-note row and a
re-run of the real control — i.e. a next-round change, not this one.

### F3 — Medium — two hand-written expectation tables for the same behaviours

The shipped tool carries an inline selftest table of **49 arms** (`:869-1892`, ~1024 of
the file's 1920 lines; arm count taken from an AST walk of the `selftest` body — 49
`arm(`/`cli_arm(` call sites). The sealed corpus `.ufo/waves/round-23/frozen/quota-cases/`
carries **30 case files** with the same scenario shapes and its own expectations
(`expected.exit`, `expected.finding_id`, `expected.paths[]` over the same six scored
fields).

Overlap is large. By hand, these inline arms and frozen cases assert the **same
scenario class**:

| inline arm | frozen case |
|---|---|
| `xfs-usrquota`, `xfs-noquota`, `xfs-conflict-noenforce`, `xfs-accounting-only`, `xfs-options-absent` | `CaseXfsUsrquota`, `CaseXfsOptionsAbsent`, `CaseXfsConflict`, `CaseXfsAccountingOnly`, `CaseXfsMixedEnforce` |
| `ext4-usrquota-unverified`, `ext4-journaled-unverified`, `ext4-options-absent` | `CaseExt4Usrquota`, `CaseExt4Journaled`, `CaseExt4NoOptions` |
| `tmpfs-usrquota`, `tmpfs-hardlimit`, `tmpfs-arbitrary-hardlimit-ignored` | `CaseTmpfsUsrquota`, `CaseTmpfsHardlimit`, `CaseTmpfsNoQuota` |
| `btrfs-qgroups-enabled`, `btrfs-qgroups-disabled`, `btrfs-enabled-unavailable`, `btrfs-qgroups-absent`, `btrfs-device-unmapped`, `btrfs-two-uuids` | `CaseBtrfsQgroup`, `SupplementQgroupDisabled`, `SupplementQgroupUnknown`, `CaseBtrfsUnmapped`, `CaseBtrfsTwoUuids` |
| `ambiguous-overmount`, `parent-id-refusal` | `CaseStacked`, `SupplementHiddenMount` |
| `no-covering-mount`, `xfs-device-mismatch`, `unsupported-fstype` | `CaseNoCover`, `CaseXfsDevMismatch`, `CaseUnsupported` |
| `symlink-resolved-path`, `optional-mountinfo-fields`, `escaped-mount-point` | `CaseSymlinkRealpath`, `CaseOptionalFields`, `CaseEscapedSpace` |
| `enabled-plus-unknown` | `CaseEnabledPlusUnknown` |

**They agree today.** Reading both tables side by side, every overlapping scenario I
compared yields the same `quota_state` / `enforcement` / `basis` tokens (e.g. inline
`btrfs-qgroups-enabled` → `enabled / unknown / btrfs_qgroups_enabled` vs `CaseBtrfsQgroup`
→ `enabled / unknown / btrfs_qgroups_enabled`; inline `ambiguous-overmount` vs
`CaseStacked` → both `ambiguous_overmount` with null fstype/mount_point). This is a
**source reading, not a measured equivalence** — neither table was executed by this seat.

**Why it matters (correctness consequence, single-authority axis).** Two hand-written
expectation tables for one behaviour set drift **silently**: the oracle reads the
frozen cases, the tool's `--selftest` reads its own table, and nothing compares them.
A future change to the classification table that updates only one side leaves the
selftest green against a stale table, or the oracle red against a correct table, with
no third witness. The wave's own doctrine (PROTOCOL's "expected values committed in the
owning repo and independent of the recomputation"; the r23 skill-row note "Where the
selftest's expected values live") is exactly about having **one** such authority.

**Minimal remedy (next revision).** Keep the sealed corpus as the authority for
behaviour and reduce the inline table to what it uniquely owns: the CLI-surface arms
(usage errors, `--fixture`/`--path` exclusivity, `--selftest` exclusivity) and the
output-shape arms (setup payload carries `schema`/`paths: []`, `df_covers_quota` is
false, `limits` is present, per-path key set is exact). Equivalently, move the
behaviour arms into a sibling module that imports the sealed corpus. **Trade-off:** the
contract fixes `--selftest` as a CLI flag of the tool and `SKILL.md:586` names it, so
the flag must stay; shrinking the table changes the tool's byte surface and would need
its own re-measurement. This is weight, not correctness — it can wait for the round that
next touches the file.

### F4 — Low — `Mount.order` is written and never read

`:274` (slot), `:278` (ctor parameter), `:287` (assignment), `:341` (call site).
Literal search over the committed tree finds no reader (`\.order` occurs nowhere else
in `tools/`). It is the vestige of the superseded contract clause "among equal mount
points the **last line wins**", which the pre-seal amendment replaced with a refusal.

**Why it matters.** It is a standing invitation to reintroduce line-order stack
resolution, which `preseal-amendment.md` forbids in as many words ("Do not guess stack
order from line order or reusable IDs"). Deleting the field makes the prohibition
structural rather than documentary.

**Remedy.** Drop the slot, the parameter, the assignment and the keyword argument.
No behaviour change: `order` is not consulted anywhere, so `resolve_mount`'s refusal
logic is untouched. **Safe to do whenever the file is next edited;** it is a pure
deletion.

### F5 — Low — "the longest covering mount" is expressed twice, and the containment rule a third time

`resolve_mount` selects the best covering mount by `len(mount.mount_point)` (`:441-444`)
and then selects the ancestor by **the same string-length rule written out again**
(`:447-451`); `covering_mounts` expresses containment separately as
`point == resolved or point == "/" or resolved.startswith(point + "/")` (`:407-419`).

**Why it matters.** The parent-id consistency check compares the *best* mount against
the *ancestor* chosen by the second copy of the rule. If one copy were ever changed
(e.g. to component count, which is arguably the more natural reading of "longest
component-prefix") and the other not, the `ambiguous_overmount` boundary moves
silently — the refusal fires (or fails to fire) against a differently-chosen ancestor,
and no test would point at the cause.

**Remedy.** One `longest_by_mount_point(mounts)` helper used by both selections.
**Trade-off:** zero behavioural change today (both copies are the same rule), so this
is a readability/drift fix only.

### F6 — Low — loop-invariant work repeated per probed path

`resolve_mount` rescans the full mount list for every path: `covering_mounts` (`:437`),
a set of cover points (`:438`), the best scan (`:441-444`), the shorter list (`:447-449`),
the ancestor scan (`:450-452`), and `known = set(mount.mount_id for mount in mounts)`
(`:454`) — the last is a pure function of the mount list and is rebuilt per path.

**Why it matters.** Cost is O(paths × mounts) with a fresh set allocation per path.
With the default two paths and a normal mount table this is negligible, so this is
weight, not correctness — but the `known` set is the textbook loop-invariant and the
cleanest one-line hoist in the file.

**Remedy.** Compute the id set once per run and pass it in, or resolve all paths
against one precomputed index. **Trade-off:** touches a function signature; do it
together with F5, not separately.

### F7 — Low — the XFS quota vocabulary has two statements

`quota_option_keys` unions three constants on every call —
`XFS_QUOTA_KEYS | XFS_NOENFORCE_KEYS | XFS_NEGATIVE_KEYS` (`:363`) — while `classify`
independently encodes the same vocabulary across three tests (`:489-498`).

**Why it matters.** The emitted `quota_option_keys` list and the emitted
`quota_state`/`enforcement` are two outputs derived from one vocabulary stated twice.
Editing one without the other makes the tool emit a key list that disagrees with the
classification it computed for the same mount. The union is also re-allocated on every
call.

**Remedy.** One module-level `XFS_QUOTA_VOCABULARY` constant used by both, so the
emitted list and the verdict come from one source. **Trade-off:** none; same set
membership.

### F8 — Low — exit code 2 has three meanings, and the constant names only one

`RC_SETUP = 2` (`:147`) is returned for the `QUOTA_STATE_UNKNOWN` verdict (`:567`), for
genuine setup errors (`:789`, `:1912`, `:1915`) and for a closed stdout (`:803`). The
finding id is the only discriminator, which is why
`corpus/knowledge/quota-surface-r23.md` has to instruct readers to "Read finding_id, not
exit code alone".

**Why it matters.** The constant carries the wrong name at the point of use; a reader
following `verdict()` sees `RC_SETUP` returned for a legitimate unknown verdict.

**Remedy — deliberately minimal.** `RC_SETUP = 2` is a **house idiom** across the
mori tools (`tools/mori-misroot-sweep.py:51`, `tools/mori-round16-context-check.py:76`,
`tools/mori-round17-context-check.py:113` all define their own `RC_SETUP = 2`).
Renaming it here would create a second convention, which is worse than the wart.
Instead add a named alias (`RC_UNKNOWN = RC_SETUP`) and use it at `:567`: same value,
no output byte changes, no new convention.

### F9 — Low — a broad `except` turns an internal defect into "the input was bad"

`main` (`:1913-1915`) catches `(OSError, UnicodeError, ValueError, TypeError, KeyError,
RecursionError, MemoryError)` and answers `setup_payload("input_unavailable")`.

**Why it matters, with a concrete reachable instance.** `parse_mountinfo` parses the
id fields with `int(fields[0]) if fields[0].isdigit() else None` (`:329-330`).
`str.isdigit()` is **True for non-decimal digits** — e.g. `'²'` — while `int('²')`
raises `ValueError`. So a mountinfo line whose id field carries such a character
produces the generic `input_unavailable` token, whereas every other malformed line
produces the specific `mountinfo_line_unparseable` (`:325-327`). Two members of one
malformed-input class report different setup tokens, and a genuine programming error
anywhere in the tool would be indistinguishable from a malformed input.

**Remedy.** Parse the id fields with a decimal-only test (e.g. `field.isascii() and
field.isdigit()`), and narrow the catch to the parse failures actually intended
(`OSError`/`UnicodeError`/`ValueError` from input handling) so an internal defect
surfaces as a traceback rather than as a false "bad input".

### F10 — Low — the shipped selftest still creates `mori-quota-v2-*` directories

`:874` — `tempfile.TemporaryDirectory(prefix="mori-quota-v2-")` in a tool whose shipped
identity is the v3/production one (see F1). `SKILL.md:586` documents the selftest's
`TMPDIR` requirement, so the prefix is user-visible in the filesystem. One-token
rename; cosmetic, but it is the second place where the shipped artifact still carries a
candidate's identity.

### F11 — Low — a closed stdout is answered with the setup exit code

`emit` (`:797-804`) answers an `OSError` from `print`/`flush` with `os._exit(RC_SETUP)`.
A broken pipe is not a setup error, and the exit now has yet another meaning, with no
JSON body emitted at all. Cosmetic in practice (the consumer is gone), but the
constant choice mislabels the condition. A distinct non-2 code, or a plain `return`,
would be honest; note that `os._exit` is deliberate (it skips the interpreter's
broken-pipe noise on stderr), so the fix is the code, not the mechanism.

### F12 — Low — `description=__doc__` is never rendered

`parse_args` (`:815-819`) builds an `ArgumentParser` with `add_help=False` and passes
the 124-line module docstring as `description`. With no help action there is no code
path that prints it. It is a pure per-invocation allocation and a second copy of the
CLI contract that no user can reach. Either drop the argument or make the help text
actually reachable — the latter is better, because it would give the corrected header
(F1) a visible surface.

### F13 — Low — a redundant `basename` on an already-basename value

`probe_fixture` (`:687`) applies `os.path.basename(mapped)` to a `device_links` value
that `plain_basename` already proved to contain no slash (`:738`, and the predicate at
`:388-396`). The call is a no-op; the mapping is already a plain basename.

### F14 — Low — "canonical UUID keys" is claimed but not enforced

`UUID_RE` (`:230-232`) accepts uppercase hex, so a non-canonical UUID key passes the
check that the header calls "canonical UUID keys" (`:44-45`). There is **no behavioural
difference today** — UUIDs are only dict keys compared against device *basename* lists,
never against the uuid text — so this is a validation/doc mismatch, not a bug. Either
tighten the regex or stop claiming canonicality.

### F15 — Low — real mode and fixture mode accept different path spellings

Fixture paths must satisfy `normalized_absolute` (absolute; no `""`, `"."` or `".."`
component; no trailing slash — the predicate is `:374-385`, applied at `:720-721`, with
the nonempty-list and exact-key-set rules at `:711` and `:715-716`), while a real-mode
`--path` only has to start with `"/"` (`:1904-1907`). So `/srv/../etc` and `/srv/` are refused in fixture
mode and accepted in real mode. The contract only requires "relative paths" to be
refused, so the code satisfies the contract; the asymmetry is a second acceptance
vocabulary for the same logical input. Worth one shared predicate if the two modes are
ever meant to agree.

---

## 5. Dead-weight ledger — what is **not** dead (do not remove)

* **`--selftest` and its inline arms (F3).** Not dead: `SKILL.md:586` and the
  `corpus/knowledge/quota-surface-r23.md` `recheck:` line both name it as the tool's
  self-test interface, and the contract fixes it as a CLI flag. Its *overlap* with the
  sealed corpus is the finding (F3), not its existence. Note also that the r23 measure
  driver invokes the tool's real-mode CLI (`measure-round23.py:584`) and the oracle
  (`run_quota_oracle`), but **no r23 driver arm exercises `--selftest`** — the same gap
  already recorded for C1 in `build/CriticRenameHarm.md` F5 ("R25 never exercises the
  selftest output"). That is a measurement-coverage observation, not a reason to delete
  the flag.
* **`decode_octal(fields[3])` (`:328`) discards its result.** Not dead weight: the
  amendment requires the root field to be octal-decoded and any other backslash escape
  to be a setup error, so the call is a **validation** call. It is worth a one-line
  comment saying so (`# validated, not used: the root field is not needed`), because a
  reader will otherwise read it as a mistake.
* **`unallowed` in `tools/mori-retention-reconcile.py`.** Checked specifically because
  C1 removed the `raw_unallowlisted` producer key: the list is **still consumed** at
  `:220` (`routed`), `:221` (`retention_code`), `:222` (`retention_finding`), `:226`
  (`metric`) and `:234` (`scanner_unallowlisted`). The C1 clean cutover orphaned
  nothing; there is no dead computation to reclaim there.
* **`option_keys()` returning every super-option key.** Deliberate: the full key set is
  intersected down to the quota vocabulary before anything is emitted, and option
  *values* are never read. The output-minimisation property is intact — I verified
  that `evaluate` writes only the nine documented per-path keys, that
  `real_device_name`'s result is used only for device matching and never emitted, and
  that `record["mode"]` can only ever reach the output as `"qgroup"`, `"squota"` or
  `null` through `btrfs_modes()` (`:399-404`).
* **`Mount.__slots__` + the explicit constructor.** Verbose, but correct and
  keyword-constructed (`:331-342`), so there is no positional mis-ordering risk.
  Replacing it with a `NamedTuple` would remove ~25 lines; it is a style call, not a
  defect, and it is not worth a byte change on its own.
* **`plain_basename` is `:388-396`** and **`btrfs_modes` is `:399-404`** (both cited
  above); `normalized_absolute` is `:374-385`, applied to the fixture path and realpath
  at `:720-721`.

## 6. Preserved contract (must not move)

* Six scored per-path fields and their tokens; `exit_code`/`finding_id` mapping;
  `schema mori-quota-surface-v1`; `df_covers_quota: false`; the `limits` text; the
  setup payload's `paths: []` and fixed-token `error`.
* The output-minimisation property (no mount source, no option value, no UUID, no
  unknown metadata) — F1's rewrite must not reintroduce any of these into the header or
  the code.
* The refusal-over-guessing rules: repeated covering mount point → `ambiguous_overmount`;
  chosen mount whose parent id is present but is not the longest shorter covering mount
  → `ambiguous_overmount`; no cover → `no_covering_mount`; device mismatch preempts
  the filesystem table.
* The btrfs safety property: **real mode never opens `qgroups/mode`**; `enabled` is
  the only real-mode attribute read; `btrfs_qgroups_mode` is null in real mode. (This
  is independently audited in `falsify/InspectModeSafety.md`; nothing in F1-F15 touches
  it, and F1 explicitly says to keep the header's readset paragraphs verbatim.)
* The ext2/3/4 rule: always `unknown`, enforcement `n/a`, basis
  `ext_quota_option_unverified` / `ext_quota_superblock_unobservable`.
* The tmpfs rule: only `quota`/`usrquota`/`grpquota` and the four documented hardlimit
  keys; an arbitrary `_hardlimit` suffix is not a quota option.
* The fixture grammar (`mori-quota-fixture-v1`): exact top-level key set, exact per-path
  key set, canonical `MAJ:MIN`, canonical UUID keys, plain basenames, strict
  qgroups/enabled/mode pairing, duplicate-key and duplicate-path rejection.
* The input fence and the ownership fence: no `quotactl`, `btrfs qgroup`, `xfs_quota`,
  `repquota`, mount, write or privileged interface; no fstab / mount-unit /
  Snapper / superblock reads; no credential, token or session material.
* All frozen case / rule / oracle bytes, the frozen real control, and the C1 source
  byte-guard target (`frozen/c1-source-delta.json`) — **unchanged by this review**; this
  seat edited no source file at all.

## 7. Aggregate advice (ordering, for whoever next owns this file)

1. **F1** first — it is free, it is the artifact's own face, and it currently misstates
   the shipped bytes. Rewrite the header; keep the readset and no-mode paragraphs.
2. **F4 + F10 + F11 + F12 + F13** — a small, behaviour-neutral cleanup (one dead field,
   one stale prefix, one mislabelled exit, one unreachable description, one no-op
   `basename`). Zero behavioural delta.
3. **F7 + F5 + F6 + F9 + F14 + F15** — single-authority and diagnosability work;
   behaviour-preserving except F9's token narrowing, which changes a setup-error token
   for one exotic input class.
4. **F2** — needs its own measurement (a real-mode access-failure path is not
   reachable from a fixture) and a knowledge-note re-word; do it in a round that can
   re-run the real control.
5. **F3** — the largest weight win (up to ~700 lines) and the one with the best
   long-term drift argument, but it changes the tool's byte surface and needs its own
   re-measurement.

## 8. Confidence and gaps

* **High** that F1, F3 (overlap), F4, F5, F6, F7, F8, F9 (reachability), F10-F15 are
  accurate: they are read directly off the pinned blob with line anchors, and the
  "no reader" claims for `Mount.order` are literal-tree searches whose limitation is
  recorded in §2.
* **Medium** on F2's practical impact: the state and enforcement are correct and the
  mis-token only appears in real mode on a btrfs path whose qgroups directory cannot be
  inspected; I did not observe such a host state (no live reads), and the frozen real
  control does not cover it.
* **F3's agreement claim is a reading, not a measurement** — neither table was executed.
* **Not assessed here:** the C1 reconciler's own maintainability beyond the dead-weight
  check in §5; the oracle's internals; the census/other mori tools (out of scope for
  this item); the r23 strict-red contradiction (owned by other seats).
* **No claim is made about promotion, clearance, baseline acceptance, debt, or the
  frozen CaseEscapedSpace contradiction** — this review is source-level and advisory
  only.
