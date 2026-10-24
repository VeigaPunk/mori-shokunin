# QEscapedSpace — round-23 falsification of the sealed C2 case `CaseEscapedSpace`

Seat: `MadoR22-2.QEscapedSpace` · role: falsification reviewer (leaf, no dispatch) ·
scope: exactly one sealed fixture-mode case.

**Verdict: MISMATCH (strict red, reported not excused).** The observed output does
not match the sealed expectation: exit `2` vs expected `1`, finding
`QUOTA_STATE_UNKNOWN` vs expected `QUOTA_ENABLED`, and the first path's ordered
six-field tuple differs in five of six fields. The second path matches exactly.

The mismatch is a genuine contradiction between the **frozen expectation bytes** and
the **sealed parent-ID mount-resolution rule** (source mount id 43, parent id 33,
longest strictly-shorter cover id 42 `/srv` — fixed facts), not an implementation
defect and not an excuse. No source, expectation, case or oracle byte was changed
by this seat, and the case is **not** passed, excluded, relabelled or waived.

---

## 0. Invocation disclosure and scope discipline

* This seat executed **exactly one** probe: one bounded fixture-mode invocation of
  the sealed case (details in §1). It was **not repeated**; after the parent
  directed a static audit of the already-observed contradiction, the work continued
  as source/evidence reading and receipt regeneration only. The retained
  observation lives in the seat scratch tree (`run-observation.json`, `stdout.txt`,
  `stderr.txt`).
* No further scans were run. The case is not declared a pass, not excluded, not
  relabelled. The known red is treated as ground truth and is reported as a red.
* Only these lane paths were written: this report and
  `.ufo/waves/round-23/falsify/QEscapedSpace/scan.json`, plus scratch under
  `/fast/scratch/hyaku/mori-r23/QEscapedSpace/`.

## 1. The single invocation that was executed (fixture mode only)

```
argv (child)        : ["/usr/bin/python3", "-I",
                       "/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py",
                       "--fixture",
                       "/fast/scratch/hyaku/mori-r23/QEscapedSpace/fixture.json"]
wrapper (enforced)  : prlimit --as=402653184 -- timeout --signal=KILL 15s <argv>
address space limit : 402653184 bytes (384 MiB)
timeout             : 15 s (KILL), wall clock far below the bound
mode                : synthetic fixture mode only — never real mode
```

* `real` mode was **not** invoked: no `--path`, no default-path probe, no
  `/proc/self/mountinfo` host read, no `os.stat` of a host path.
* No privileged or mutating interface was called: no `quotactl`, `btrfs qgroup`,
  `xfs_quota`, `repquota`, `mount`, no qgroup/`mode` attribute read, no write.
* No build, lint, test, formatter, gate or smoke run was performed.

## 2. Byte identities (exact, verified)

| Artifact | sha256 | Note |
|---|---|---|
| `frozen/quota-cases/CaseEscapedSpace.json` | `8340738a509e474a94a815637e66b407dfb60c6449511e52db55296d844abeea` | identical to the seal-manifest identity in `evidence/frozen-contradiction.json` and `evidence/measure{2,4}/summary.json`; bytes unmodified |
| scratch `fixture.json` (= `case["fixture"]`, extracted verbatim) | `ab11b8a4a11b12e70b05d13f259c368bc42e0b5baa3b9c2341c310b89b80fb79` | **byte-identical** to the fixture identity the wave-2 driver recorded for this case in `evidence/measure2/c2-after-observed.json` and `evidence/measure4/c2-after-observed.json` |
| `tools/mori-quota-surface.py` (working copy) | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` | equals `git show f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c:tools/mori-quota-surface.py` (pinned production revision) |
| stdout | `95728a38e54c4f2a3196a5e88a7155fbc03f362f5946e837c5308040ca752323` | one JSON object, `schema=mori-quota-surface-v1`; **identical** to the stdout the wave-2 driver recorded for this case in both measure2 and measure4 |
| stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | empty (sha256 of the empty string) |

## 3. Observed output (verbatim stdout, one JSON object)

```json
{"df_covers_quota":false,"exit_code":2,"finding_id":"QUOTA_STATE_UNKNOWN",
 "limits":"no per-user, per-group or per-project limit or usage is read. …",
 "paths":[
  {"basis":"ambiguous_overmount","btrfs_qgroups_mode":null,"device_check":"not_checked",
   "enforcement":"n/a","fstype":null,"mount_point":null,"path":"/srv/my data/sub dir",
   "quota_option_keys":[],"quota_state":"unknown"},
  {"basis":"xfs_noquota_option","btrfs_qgroups_mode":null,"device_check":"match",
   "enforcement":"n/a","fstype":"xfs","mount_point":"/srv","path":"/srv/plain",
   "quota_option_keys":["noquota"],"quota_state":"disabled"}],
 "schema":"mori-quota-surface-v1"}
```

Exit code observed: `2`. No timeout, no signal, no truncation.

## 4. Comparison — primary denominator (six scored fields, ordered)

Primary fields: `path, fstype, mount_point, quota_state, enforcement, basis`.

**Headline**

| Check | Given (sealed) | Actual | Match |
|---|---|---|---|
| exit | `1` | `2` | ✗ |
| finding_id | `QUOTA_ENABLED` | `QUOTA_STATE_UNKNOWN` | ✗ |
| ordered path tuples | see below | see below | ✗ |

**Path 0 — `/srv/my data/sub dir`**

| Field | Given | Actual | Match |
|---|---|---|---|
| path | `/srv/my data/sub dir` | `/srv/my data/sub dir` | ✓ |
| fstype | `xfs` | `null` | ✗ |
| mount_point | `/srv/my data` | `null` | ✗ |
| quota_state | `enabled` | `unknown` | ✗ |
| enforcement | `enforced` | `n/a` | ✗ |
| basis | `xfs_quota_option` | `ambiguous_overmount` | ✗ |

**Path 1 — `/srv/plain`**

| Field | Given | Actual | Match |
|---|---|---|---|
| path | `/srv/plain` | `/srv/plain` | ✓ |
| fstype | `xfs` | `xfs` | ✓ |
| mount_point | `/srv` | `/srv` | ✓ |
| quota_state | `disabled` | `disabled` | ✓ |
| enforcement | `n/a` | `n/a` | ✓ |
| basis | `xfs_noquota_option` | `xfs_noquota_option` | ✓ |

Ordered tuple check: `given != actual` (path 0 differs) → `paths_match = false`.

## 5. Supplementary metadata (reported separately, NOT scored)

This case carries **no** `supplementary_expected` block (`supplementary_note_present:
false` in the driver evidence as well), so no supplementary field is scored for it.
The values below are observation only and do not widen the primary denominator.

| Path | field | Observed |
|---|---|---|
| `/srv/my data/sub dir` | `device_check` | `not_checked` |
| | `quota_option_keys` | `[]` |
| | `btrfs_qgroups_mode` | `null` |
| `/srv/plain` | `device_check` | `match` |
| | `quota_option_keys` | `["noquota"]` |
| | `btrfs_qgroups_mode` | `null` |

These observed values are exactly what the sealed amendment prescribes for a
preempted row (`quota_option_keys=[]`, `btrfs_qgroups_mode=null`,
`device_check=not_checked`), confirming the refusal branch was taken rather than a
partial/degraded verdict path. No mount source, option value, UUID or file name
appears in the output.

## 6. Static audit — seal bytes, parent rule, expected mapping

### 6.1 Seal bytes

* Frozen case bytes: `8340738a509e474a94a815637e66b407dfb60c6449511e52db55296d844abeea`,
  identical in `evidence/frozen-contradiction.json` and in the
  `cases_sha256_combined` / per-case identities of `evidence/measure{2,4}/summary.json`
  (`"worktree_matches_sealed_bytes": true`, `byte_identical: true`).
* The case file carries exactly the sealed keys `{schema, id, scenario, fixture,
  expected, rationale, sources}` — no `supplementary_expected` — and its `expected`
  block carries exactly `{exit, finding_id, paths}` with six-key path entries, so
  the oracle's headline denominator for this case is exactly the six scored fields
  compared in §4.
* The tool bytes at production `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` are
  `e4857413…`, the same bytes the measure4 driver staged
  (`staged_tools["tools/mori-quota-surface.py"].revision.sha256`).

### 6.2 Parent rule (sealed text → implementation)

Sealed text (`preseal-amendment.md`, "Final pre-seal clarifications"):
> "C2 additionally refuses when the chosen mount's parent ID is present in the
> snapshot but is not the ID of the longest strictly-shorter covering mount. Use
> unknown/n/a/ambiguous_overmount with null fstype/mountpoint and not_checked
> device_check. This catches a new mount on a plain ancestor directory hiding an
> older nested mount without any repeated mountpoint; a missing parent ID remains
> unknown topology but does not trigger this extra refusal. Root has no shorter
> cover."

Implementation (`tools/mori-quota-surface.py`):

* `covering_mounts()` — line 407: component-prefix cover, `/` included.
* `resolve_mount()` — line 421; longest cover wins (441-445); the strictly shorter
  covers are reduced to the longest of them (`ancestor`, 446-452); the parent-ID
  refusal fires at 455-461 (`best.parent_id in known and best.parent_id !=
  ancestor.mount_id` → `return None, "ambiguous_overmount"`).
* `evaluate()` — line 514: refusal → `fstype=None, mount_point=None,
  quota_state="unknown", enforcement="n/a", basis="ambiguous_overmount",
  device_check="not_checked"`, `quota_option_keys=[]`, `btrfs_qgroups_mode=null`.
* `verdict()` — line 566: no enabled path, one unknown → exit 2
  `QUOTA_STATE_UNKNOWN`.

### 6.3 Expected mapping — why the sealed expectation cannot be produced

The fixture's mountinfo (decoded):

```
id 42  parent 33  0:44  /            /srv            xfs  …,noquota
id 43  parent 33  0:45  /            /srv/my\040data  xfs  …,usrquota,attr2
id 33  parent  2  0:30  /@           /              btrfs …
id 26  parent 33  0:24  /            /proc           proc …
```

For `/srv/my data/sub dir` the covering mounts are `/` (id 33), `/srv` (id 42) and
`/srv/my data` (id 43, after `\040` decoding). The longest is id 43, whose
`parent_id` is **33**. The longest *strictly shorter* covering mount is `/srv`
(id 42). 33 is present in the snapshot but is not id 42 → the sealed rule refuses.

Fixed facts, unchanged by this seat: **selected mount id 43, parent id 33, longest
strictly-shorter cover id 42 (`/srv`)**. These are the same values recorded in
`evidence/frozen-contradiction.json` (`selected_mount_id: 43`,
`selected_parent_id: 33`, `longest_strictly_shorter_cover: {42, "/srv"}`,
`parent_present_in_snapshot: true`) and they are reproduced by the observed
`ambiguous_overmount` row.

**Root cause of the contradiction.** The frozen expectation was derived under an
earlier clause set: the case's own `rationale` enumerates the `qgroups_enabled`
member addition, the `btrfs_qgroups_enabled` basis rename, the
`ext_quota_option_unverified` change and the duplicated-mountpoint
`ambiguous_overmount` refusal, and asserts that none of them touches this case —
but it does **not** account for the parent-ID refusal clause added in the same
amendment's final pre-seal clarifications. The frozen fixture also carries a
synthetic parent graph that is geometrically inconsistent: mount 43 lives under
`/srv` (id 42) yet declares parent 33 (the `/` btrfs mount). Under the sealed rule
that inconsistency is indistinguishable from a genuine overmount, so the case's
expected `enabled/enforced` row for `/srv/my data/sub dir` is unreachable.

Note also that the escaping itself is handled correctly — the mount point is
decoded to `/srv/my data` and *is* selected as the longest cover; the refusal is
purely the parent-ID clause, not a decoding failure. The `usrquota` option and the
`/srv` `noquota` option are both parsed correctly (visible in path 1's
`quota_option_keys: ["noquota"]` and in the sibling row's `xfs_noquota_option`
basis).

### 6.4 Cross-reference to the ORIGINAL wave-2 driver invocations (read-only)

Both original driver runs are recorded in the committed evidence and agree with the
single observation of this seat:

| Fact | measure2 | measure4 | this seat |
|---|---|---|---|
| oracle | `.ufo/waves/round-23/oracle-quota.py` sha256 `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` | same sha256 | n/a (not run) |
| staged "after" tool sha256 | `7d8c519c5a4f2bb495e871966087fa364e8727b44ba97ab66d5377ce188a5cd8` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` (= production `f3dc07c`) | `e4857413…` (= production `f3dc07c`) |
| staged "entering" tool | absent (`present: false`) | absent (`present: false`) | n/a |
| case sha256 | `8340738a…` | `8340738a…` | `8340738a…` |
| fixture sha256 | `ab11b8a4…` | `ab11b8a4…` | `ab11b8a4…` |
| run exit / timeout / stderr | `2` / `false` / empty | `2` / `false` / empty | `2` / `false` / empty |
| run stdout sha256 | `95728a38e54c4f2a3196a5e88a7155fbc03f362f5946e837c5308040ca752323` | `95728a38e54c4f2a3196a5e88a7155fbc03f362f5946e837c5308040ca752323` | `95728a38e54c4f2a3196a5e88a7155fbc03f362f5946e837c5308040ca752323` |
| headline (exit / finding / paths) | all `false` | all `false` | all `false` |
| case status | `unmet` (reason `null`) | `unmet` (reason `null`) | mismatch (reported) |
| supplementary note present | `false` | `false` | `false` (absent from the case) |
| driver supplementary checks | 9/9 `pass` (schema, exit_consistency, output_keys_allowed, output_key_set, error_token, path_key_set, df_covers_quota, limits_text, no_leakage) | identical | n/a |
| C2 population | `pass 29 / total 30`, `unmet 1`, `capability_absent 0` | `pass 29 / total 30`, `unmet 1`, `capability_absent 0` | n/a |

Two consequences worth recording:

1. The stdout of this case is **byte-identical** across the measure2 tool bytes
   (`7d8c519c…`), the measure4 tool bytes (`e4857413…`, = production `f3dc07c`)
   and this seat's own invocation. The case's red is therefore invariant under the
   round's co-evolved tool correction and is not an artefact of it.
2. The case is the single `unmet` member of the 29/30 C2 population in both
   driver runs, and it is the only member whose red is a sealed-rule contradiction
   rather than a defect in the tool.

## 7. Disposition and non-mutation statement

* Verdict: **MISMATCH** on exit, finding_id and the ordered six-field tuple —
  reported as a strict red for this case; **not** excused, **not** waived, **not**
  relabelled, **not** excluded, **not** special-cased, **not** declared a pass.
* Frozen bytes untouched: `CaseEscapedSpace.json` sha256 is still
  `8340738a509e474a94a815637e66b407dfb60c6449511e52db55296d844abeea`; the tool
  still matches production `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.
* This seat wrote only: this report and
  `.ufo/waves/round-23/falsify/QEscapedSpace/scan.json`, plus scratch under
  `/fast/scratch/hyaku/mori-r23/QEscapedSpace/`. No sibling path, no lane index, no
  refs, no production/frozen/oracle file, no git mutation, no jj mutation, no
  subagent dispatch.
* The strict C2 target therefore stays **UNPROVABLE** (29/30); this case
  contributes no evidence for admission, and the pinned driver's exit 1 remains
  expected on account of this strict red.
* Routing: the contradiction between the frozen expectation and the sealed
  parent-ID rule is a pre-seal derivation defect. Diagnosing it (case
  re-derivation against the final clause set, or an explicit rule carve-out decided
  by L1) is outside this seat's authority; no such change was made here.

## 8. Residual risk and verification gaps

* The red is confirmed at three independent points (measure2, measure4, this
  seat) with byte-identical stdout, so it is not a harness artefact.
* Not verified here (outside a single-case, single-invocation seat): the other 29
  sealed cases, the real-mode control, the C1 arms, the driver ancestry/pinning
  checks, and any tool revision other than the two staged bytes above.
* The parent-ID rule itself is unexercised in a *positive* direction by this case:
  it is only shown to fire. Whether it fires correctly for a genuine overmount
  (repeated mount point) and whether it over-fires on a benign synthetic parent
  graph are properties of the other sealed cases, not of this one.
* No tool was installed or updated in this seat (no pacman/uv/cargo/npm action);
  only stock `python3`, `prlimit` and `timeout` were used.
