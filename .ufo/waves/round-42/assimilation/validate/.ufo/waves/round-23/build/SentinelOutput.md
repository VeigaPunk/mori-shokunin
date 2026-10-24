# C2 output-schema privacy review

**Severity: Moderate — filesystem metadata disclosure.** Review is limited to the frozen C2 contract; it establishes the output contract, not behavior of an implementation.

## Axes and evidence

- **Privacy:** §C2 permits arbitrary absolute `--path` inputs and reads their real paths, mountinfo, mount-source basenames, and Btrfs sysfs device/UUID data (contract lines 73–80).
- **Utility:** the output needs to distinguish per-input verdicts and preserve the quota classification, but does not need to disclose filesystem locations or identifiers.
- **Contractability:** the declared output includes `path`, `fstype`, `mount_point`, `quota_option_keys`, and `btrfs_qgroups_mode`; it explicitly forbids mount sources, other options, and option-value file names (lines 124–130).

### Findings

1. **Confirmed contract-level disclosure: `path` and `mount_point`.** `path` reflects the caller-supplied absolute path; `mount_point` reflects a decoded host mount path. Either can contain usernames, project/customer names, workspace layout, or volume labels, and output may later be captured or shared. The default path also exposes the configured fleet/project location. This is the material privacy issue in the declared schema.
2. **Option values are correctly excluded by the contract, but need a guard.** `quota_option_keys` is specified as keys only and `usrjquota`/`grpjquota` values can contain quota-file paths or names. Any serialization of the original `key=value` token would violate the explicit no-file-name rule. Also, the `_hardlimit` suffix rule accepts an arbitrary key name; echoing that name is unnecessary and can disclose caller-configured labels.
3. **Device names and Btrfs UUIDs are internal join data, not declared output fields.** The schema does not call for emitting mount sources, device aliases, major:minor values, or UUIDs. Keep them strictly internal; fixture assertions should catch accidental inclusion in output or error text.
4. **`btrfs_qgroups_mode` is raw sysfs text in the contract.** It is not inherently personal data, but it is a variable host-derived string. Emit only a documented, finite mode enum (or null/unknown for an unrecognized value), never unvalidated raw text. Similarly constrain `fstype` to the supported filesystem names plus `other`/null; do not echo arbitrary filesystem-type strings.
5. **The other named result fields are suitable if kept fixed.** `schema`, `finding_id`, `quota_state`, `enforcement`, `basis`, `device_check`, `df_covers_quota`, and fixed `limits` text should remain finite enums/constants rather than interpolating host or fixture data.

## Exact minimization rules

- Replace output `path` with an integer `path_index` in input order. Do not output the given path, realpath, basename, or any path-derived label.
- Remove `mount_point`. If mount relationship is needed for diagnosis, emit only a fixed enum such as `exact`, `ancestor`, or `root`; do not include the mount path.
- Keep `fstype` only as a finite allowlist (`btrfs`, `xfs`, `ext2`, `ext3`, `ext4`, `tmpfs`, `other`) or null.
- Emit only canonical quota-option identifiers from a finite allowlist, never option values or raw tokens. For arbitrary keys matched only by `_hardlimit`, report a canonical `hardlimit` indicator (or boolean), not the original key. In particular, `usrjquota` may appear as a key, but its value/file name must never appear.
- Map Btrfs qgroups mode to an explicitly documented finite enum; unknown values become null/unknown. Never serialize raw sysfs text.
- Never emit mount source, source basename, device name, major:minor, Btrfs UUID, sysfs path, unrecognized mount option, parser excerpt, or interpolated setup-error input. Setup errors should be fixed-schema, non-partial results with no caller/fixture text.
- **Contract impact:** the current C2 output shape and oracle comparison explicitly include `path` and `mount_point` (lines 124–129, 142–145). Replacing them is a contract/oracle change for L1 to authorize; this review does not alter the frozen contract.

## Fixture-level check to add

Use synthetic `--fixture` inputs only (no host reads) with distinct canaries placed in: the requested path and realpath; an escaped mount point; a mount source/device-link key and target; a Btrfs UUID and device list; an ext quota option such as `usrjquota=/private/LEAK_QUOTA_FILE_...`; an arbitrary `*_hardlimit` key; and qgroups mode text. Include a setup-error fixture containing a canary in malformed/unparseable input as well.

For each valid and setup-error fixture, assert that **none** of the canary strings occurs anywhere in serialized stdout or stderr, including JSON keys and values. Also assert the exact minimized object/path-item key sets, allowed enum values for `fstype` and `btrfs_qgroups_mode`, and that every `quota_option_keys` entry is canonical and contains no `=` or path component. Separately assert the expected path-index association and quota verdict so redaction does not mask classification regressions. This remains a fixture-only test; do not use real host paths or device identifiers.
