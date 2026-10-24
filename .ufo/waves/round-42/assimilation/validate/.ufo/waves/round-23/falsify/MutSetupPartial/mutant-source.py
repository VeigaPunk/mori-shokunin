#!/usr/bin/env python3
"""mori-quota-surface-v3.py — read-only quota-surface probe (FR2 / EDQUOT).

This is the round-23 pre-seal amendment candidate for contract §C2, with the
pre-seal source safety correction applied. It is a new candidate authored
alongside `mori-quota-surface.py` (the original, unaltered) and
`mori-quota-surface-v2.py` (preserved as the rejected unsafe-read source
evidence: v2 still read the btrfs `qgroups/mode` attribute in real mode).

WHAT CHANGED IN v3 (source safety, before the seal)

  The btrfs `qgroups/mode` attribute is NEVER read in real mode. Its show
  function asserts that qgroups are enabled, so a read inside a
  present-but-disabled window can trip a kernel assert on an assert-enabled
  kernel, and a quota disable racing the read makes the read unsafe. The
  real-mode readset is the `qgroups/enabled` attribute only; the reported
  `btrfs_qgroups_mode` is therefore null in real mode. Fixture mode is
  unchanged: a fixture's `qgroups_mode` is projected as `qgroup` or `squota`
  (anything else null), so the primary and supplementary fixture targets are
  unchanged and the default real control is unchanged.

This candidate carries the pre-seal amendment corrections of
`.ufo/waves/round-23/preseal-amendment.md`:

  * ext2/ext3/ext4: quota_state is ALWAYS unknown, enforcement n/a. A
    quota-related option key gives basis `ext_quota_option_unverified`;
    without one the basis stays `ext_quota_superblock_unobservable`. The
    kernel documentation states the plain quota options are ignored by the
    filesystem and only help quota tools recognise volumes, so a mount option
    is not evidence of runtime accounting.
  * btrfs: the qgroups directory means INITIALIZED, not enabled. The
    `qgroups/enabled` attribute (exact 0/1) is the enabled witness. The
    `qgroups/mode` attribute is not read at all in real mode; in fixture
    mode only the values `qgroup` and `squota` are projected and anything
    else yields null.
  * mount resolution: a covering mount point that occurs more than once is
    refused as `ambiguous_overmount` instead of being resolved by line order.
    The selected mount must also hang under the longest strictly shorter
    covering mount when its parent id is present in the snapshot; a parent id
    absent from the snapshot is unknown topology and triggers no refusal.
  * device mismatch preempts the filesystem table, for every filesystem type.
    A preempted row (no cover, ambiguous mount, device mismatch) carries
    `quota_option_keys: []` and `btrfs_qgroups_mode: null`.
  * fixture validation is strict (normalized unique absolute paths, canonical
    st_dev, canonical UUID keys, plain basenames, exact record key sets).
  * output minimization: no mount source, no option value, no UUID and no
    unknown metadata is ever emitted.

WHAT THIS PROBE IS

  A read-only observability probe. `df` capacity percentages cannot see quota
  exhaustion (FR2: the fleet's actually reported disk failures are quota
  events, EDQUOT), so this probe reports, per path, whether a filesystem
  quota mechanism is visibly enabled, visibly disabled, or unknown.

  It never calls quotactl, `btrfs qgroup`, `xfs_quota`, `repquota`, mounts,
  writes, or any other privileged or mutating interface. It reads no
  credential, token or session material. "enabled" means a quota mechanism is
  visibly configured for that mount, not that any per-user, per-group or
  per-project limit exists.

INPUTS (real mode, read-only)

  /proc/self/mountinfo, os.stat(path).st_dev, os.path.realpath(path),
  os.path.realpath(mount_source) basename, directory listings and existence
  under /sys/fs/btrfs/*/devices/ and /sys/fs/btrfs/<uuid>/qgroups, and the
  /sys/fs/btrfs/<uuid>/qgroups/enabled text. The btrfs `qgroups/mode`
  attribute is not in the readset: it is never opened.

  Mount resolution follows proc.rst section 3.5: fields 1-6, then optional
  fields up to the "-" separator, then filesystem type, mount source and
  super options. The separator and the last three fields are read per line.
  The root, the mount point and the source are octal-decoded with exactly
  \\040, \\011, \\012 and \\134; any other backslash escape is a setup error.
  Candidate mounts are those whose mount point equals the resolved path, is
  "/", or is a component prefix of the resolved path. The longest mount point
  wins; when a covering mount point occurs more than once the mount stack is
  not guessed and the path is refused as `ambiguous_overmount`.

CLI

  --path ABS     path to probe; repeatable. Default: the fleet root
                 /home/vgpnk/Projects/shokunin and then /tmp.
  --fixture FILE synthetic mode; the fixture file is the only file opened and
                 no host filesystem state is read.
  --selftest     isolated synthetic fixture arms; takes no other flag.

  Unknown arguments, a relative --path, --fixture together with --path, and
  --selftest together with any other flag are usage errors.

OUTPUT

  Exactly one JSON object on stdout with schema "mori-quota-surface-v1",
  finding_id, exit_code, paths, df_covers_quota and limits. Each path row
  carries exactly path, fstype, mount_point, quota_state, enforcement, basis,
  device_check, quota_option_keys and btrfs_qgroups_mode. Mount sources, non
  quota mount options, option values and UUIDs are never echoed.

  Exit 0  QUOTA_DISABLED       every probed path is visibly quota-disabled.
  Exit 1  QUOTA_ENABLED        at least one path shows a visible quota
                               mechanism. This is a runway-reporting finding:
                               df percentages are insufficient there. It is not
                               a failure claim.
  Exit 2  QUOTA_STATE_UNKNOWN  no path is enabled but at least one path is
                               unknown.
  Exit 2  QUOTA_SETUP          a setup error; no partial verdict is emitted.

LIMITS (stated in every output)

  No per-user, per-group or per-project limit or usage is read. NFS or
  server-side quota and overlay or fuse quota are not covered. A visible
  btrfs qgroups directory does not imply that any limit is set. An ext2/ext3/
  ext4 quota feature in the superblock is unobservable without privileged
  tools. sysfs and mountinfo races during quota enable, disable or remount
  are not excluded. QUOTA_DISABLED is not a capacity or health verdict:
  ENOSPC can coexist with it. The btrfs qgroups mode attribute is never
  read, so btrfs_qgroups_mode is null in real mode.

--selftest builds isolated synthetic fixture documents under a fresh
mkdtemp tree, runs this CLI as a real subprocess per arm, and asserts exit
code, finding_id and per-path identity. Every arm runs in fixture mode, so no
arm reads host filesystem state. Existence of --selftest is not permission to
run it during a wave.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = "mori-quota-surface-v1"
FIXTURE_SCHEMA = "mori-quota-fixture-v1"

SETUP = "QUOTA_SETUP"
ENABLED = "QUOTA_ENABLED"
UNKNOWN = "QUOTA_STATE_UNKNOWN"
DISABLED = "QUOTA_DISABLED"

RC_OK = 0
RC_ENABLED = 1
RC_SETUP = 2

FLEET_ROOT = "/home/vgpnk/Projects/shokunin"
DEFAULT_PATHS = (FLEET_ROOT, "/tmp")

MOUNTINFO = "/proc/self/mountinfo"
BTRFS_SYSFS = "/sys/fs/btrfs"

LIMITS = (
    "no per-user, per-group or per-project limit or usage is read",
    "no NFS or server-side quota and no overlay or fuse quota is covered",
    "a visible btrfs qgroups directory does not imply that any limit is set",
    "an ext2/ext3/ext4 quota feature in the superblock is unobservable without privileged tools",
    "sysfs and mountinfo races during quota enable, disable or remount are not excluded",
    "df capacity percentages never cover quota exhaustion (FR2 / EDQUOT)",
    "QUOTA_DISABLED is not a capacity or health verdict; ENOSPC can coexist",
    "the btrfs qgroups mode attribute is never read, so btrfs_qgroups_mode is null in real mode",
)

FIXTURE_KEYS = frozenset(
    ("schema", "mountinfo", "paths", "device_links", "btrfs_sysfs")
)
PATH_KEYS = frozenset(("path", "realpath", "st_dev"))
# The six primary scored fields. Supplementary metadata is asserted apart and
# never widens the primary denominator.
PRIMARY_FIELDS = frozenset(
    ("path", "fstype", "mount_point", "quota_state", "enforcement", "basis")
)
OUTPUT_FIELDS = frozenset(
    (
        "path",
        "fstype",
        "mount_point",
        "quota_state",
        "enforcement",
        "basis",
        "device_check",
        "quota_option_keys",
        "btrfs_qgroups_mode",
    )
)
UUID_KEYS = frozenset(
    ("devices", "qgroups", "qgroups_enabled", "qgroups_mode")
)

# xfs: the accounting keys, the enforcement-capable keys and the
# "accounting without enforcement" keys, plus the negative noquota key.
XFS_QUOTA_KEYS = frozenset(
    ("usrquota", "uquota", "quota", "grpquota", "gquota", "prjquota", "pquota")
)
XFS_NOENFORCE_KEYS = frozenset(
    ("uqnoenforce", "gqnoenforce", "pqnoenforce", "qnoenforce")
)
XFS_NEGATIVE_KEYS = frozenset(("noquota",))
# ext2/ext3/ext4: the documented option vocabulary. Presence is never
# enablement evidence, so this set only selects the basis token.
EXT_QUOTA_KEYS = frozenset(
    (
        "quota",
        "noquota",
        "usrquota",
        "grpquota",
        "prjquota",
        "usrjquota",
        "grpjquota",
        "jqfmt",
    )
)
# tmpfs: only the documented quota options and the four documented hardlimit
# options. An arbitrary "_hardlimit" suffix is not a quota option.
TMPFS_QUOTA_KEYS = frozenset(
    (
        "quota",
        "usrquota",
        "grpquota",
        "usrquota_block_hardlimit",
        "usrquota_inode_hardlimit",
        "grpquota_block_hardlimit",
        "grpquota_inode_hardlimit",
    )
)

DEVICE_RE = re.compile(r"\A(0|[1-9][0-9]*):(0|[1-9][0-9]*)\Z")
UUID_RE = re.compile(
    r"\A[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z"
)
OCTAL_ESCAPES = {"040": " ", "011": "\t", "012": "\n", "134": "\\"}
BTRFS_MODES = ("qgroup", "squota")


class Invalid(Exception):
    """A setup failure. Never a quota verdict."""


def require(condition, reason):
    if not condition:
        raise Invalid(reason)


def no_duplicates(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, "fixture_duplicate_key")
        obj[key] = value
    return obj


def parse_json(data):
    try:
        text = data.decode("utf-8") if isinstance(data, bytes) else data
        return json.loads(text, object_pairs_hook=no_duplicates)
    except (ValueError, UnicodeError, RecursionError):
        raise Invalid("fixture_invalid_json") from None


class Mount(object):
    """One parsed /proc/self/mountinfo line (proc.rst section 3.5)."""

    __slots__ = (
        "mount_id",
        "parent_id",
        "mount_point",
        "fstype",
        "source",
        "major",
        "minor",
        "super_options",
        "order",
    )

    def __init__(self, mount_id, parent_id, mount_point, fstype, source,
                 major, minor, super_options, order):
        self.mount_id = mount_id
        self.parent_id = parent_id
        self.mount_point = mount_point
        self.fstype = fstype
        self.source = source
        self.major = major
        self.minor = minor
        self.super_options = super_options
        self.order = order


def decode_octal(value):
    """Decode exactly \\040, \\011, \\012 and \\134; refuse anything else."""
    out = []
    index = 0
    length = len(value)
    while index < length:
        char = value[index]
        if char == "\\":
            escape = value[index + 1:index + 4]
            require(
                len(escape) == 3 and escape in OCTAL_ESCAPES,
                "mountinfo_escape_invalid",
            )
            out.append(OCTAL_ESCAPES[escape])
            index += 4
            continue
        out.append(char)
        index += 1
    return "".join(out)


def parse_mountinfo(text):
    mounts = []
    for order, line in enumerate(text.splitlines()):
        if not line.strip():
            # Empty trailing lines carry no mount.
            continue
        fields = line.split()
        require(len(fields) >= 10, "mountinfo_line_unparseable")
        try:
            separator = fields.index("-")
        except ValueError:
            raise Invalid("mountinfo_line_unparseable") from None
        # Fields 1-6 precede the optional fields and the "-" separator.
        require(separator >= 6, "mountinfo_line_unparseable")
        require(len(fields) - separator - 1 == 3, "mountinfo_line_unparseable")
        device = DEVICE_RE.match(fields[2])
        require(device is not None, "mountinfo_line_unparseable")
        decode_octal(fields[3])
        mount_id = int(fields[0]) if fields[0].isdigit() else None
        parent_id = int(fields[1]) if fields[1].isdigit() else None
        mounts.append(
            Mount(
                mount_id=mount_id,
                parent_id=parent_id,
                mount_point=decode_octal(fields[4]),
                fstype=fields[-3],
                source=decode_octal(fields[-2]),
                major=int(device.group(1)),
                minor=int(device.group(2)),
                super_options=fields[-1],
                order=order,
            )
        )
    return mounts


def option_keys(super_options):
    """The super option keys only. Option values are never read."""
    keys = set()
    for item in super_options.split(","):
        item = item.strip()
        if not item:
            continue
        key = item.split("=", 1)[0].strip()
        if key:
            keys.add(key)
    return keys


def quota_option_keys(fstype, keys):
    """The sorted quota-related option keys only, never values."""
    if fstype == "xfs":
        related = XFS_QUOTA_KEYS | XFS_NOENFORCE_KEYS | XFS_NEGATIVE_KEYS
    elif fstype in ("ext2", "ext3", "ext4"):
        related = EXT_QUOTA_KEYS
    elif fstype == "tmpfs":
        related = TMPFS_QUOTA_KEYS
    else:
        # btrfs carries its mechanism in sysfs, not in mount options.
        related = frozenset()
    return sorted(keys & related)


def normalized_absolute(value):
    """An absolute path with no empty, "." or ".." component."""
    if not isinstance(value, str) or not value.startswith("/"):
        return False
    if value == "/":
        return True
    if value.endswith("/"):
        return False
    for part in value[1:].split("/"):
        if part in ("", ".", ".."):
            return False
    return True


def plain_basename(value):
    """A plain nonempty basename: no slash, no control character."""
    if not isinstance(value, str) or not value:
        return False
    if "/" in value:
        return False
    if value in (".", ".."):
        return False
    return not any(ord(char) < 32 or ord(char) == 127 for char in value)


def btrfs_modes(value):
    """Only the two kernel mode values are informational; the rest is null."""
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text if text in BTRFS_MODES else None


def covering_mounts(mounts, resolved):
    """Every mount whose mount point covers the resolved path."""
    covered = []
    for mount in mounts:
        point = mount.mount_point
        if (
            point == resolved
            or point == "/"
            or resolved.startswith(point + "/")
        ):
            covered.append(mount)
    return covered


def resolve_mount(mounts, resolved):
    """The covering mount for a resolved path, or a refusal.

    Returns (mount, refusal). The refusal is None, "no_covering_mount" or
    "ambiguous_overmount".

    A covering mount point that occurs more than once is refused: the mount
    stack order is not derived from line order or reusable mount ids. The
    selected mount must also hang under the longest strictly shorter covering
    mount when its parent id is present in the snapshot; otherwise a new
    mount on a plain ancestor directory could hide an older nested mount.
    A parent id that is absent from the snapshot is unknown topology and
    triggers no refusal.
    """
    covered = covering_mounts(mounts, resolved)
    if not covered:
        return None, "no_covering_mount"
    points = set(mount.mount_point for mount in covered)
    if len(points) != len(covered):
        return None, "ambiguous_overmount"
    best = covered[0]
    for mount in covered[1:]:
        if len(mount.mount_point) > len(best.mount_point):
            best = mount
    shorter = [
        mount for mount in covered
        if len(mount.mount_point) < len(best.mount_point)
    ]
    if shorter:
        ancestor = shorter[0]
        for mount in shorter[1:]:
            if len(mount.mount_point) > len(ancestor.mount_point):
                ancestor = mount
        known = set(mount.mount_id for mount in mounts)
        if (
            best.parent_id is not None
            and ancestor.mount_id is not None
            and best.parent_id in known
            and best.parent_id != ancestor.mount_id
        ):
            return None, "ambiguous_overmount"
    return best, None


def classify_btrfs(device_name, sysfs):
    """The btrfs rows: the enabled attribute is the witness."""
    matched = []
    for uuid in sorted(sysfs):
        if device_name and device_name in sysfs[uuid]["devices"]:
            matched.append(uuid)
    if len(matched) != 1:
        return ("unknown", "n/a", "btrfs_device_unmapped"), None
    record = sysfs[matched[0]]
    if record["qgroups"] is None:
        # The qgroups state could not be inspected: never absent, never
        # disabled.
        return ("unknown", "n/a", "btrfs_device_unmapped"), None
    if record["qgroups"] is False:
        return ("disabled", "n/a", "btrfs_qgroups_dir_absent"), None
    if record["enabled"] is True:
        return ("enabled", "unknown", "btrfs_qgroups_enabled"), record["mode"]
    if record["enabled"] is False:
        return ("disabled", "n/a", "btrfs_qgroups_disabled"), None
    return ("unknown", "n/a", "btrfs_qgroups_enabled_unavailable"), None


def classify(fstype, keys, device_name, sysfs):
    """The filesystem classification table."""
    if fstype == "xfs":
        if "noquota" in keys and (keys & XFS_QUOTA_KEYS or keys & XFS_NOENFORCE_KEYS):
            return ("unknown", "n/a", "xfs_conflicting_quota_options"), None
        if "noquota" in keys:
            return ("disabled", "n/a", "xfs_noquota_option"), None
        if keys & XFS_QUOTA_KEYS:
            return ("enabled", "enforced", "xfs_quota_option"), None
        if keys & XFS_NOENFORCE_KEYS:
            return ("enabled", "accounting_only", "xfs_quota_option"), None
        return ("unknown", "n/a", "xfs_quota_options_absent"), None
    if fstype == "btrfs":
        return classify_btrfs(device_name, sysfs)
    if fstype in ("ext2", "ext3", "ext4"):
        # A mount option is not evidence of runtime quota accounting.
        if keys & EXT_QUOTA_KEYS:
            return ("unknown", "n/a", "ext_quota_option_unverified"), None
        return ("unknown", "n/a", "ext_quota_superblock_unobservable"), None
    if fstype == "tmpfs":
        if keys & TMPFS_QUOTA_KEYS:
            return ("enabled", "enforced", "tmpfs_quota_option"), None
        return ("disabled", "n/a", "tmpfs_quota_options_absent"), None
    return ("unknown", "n/a", "unsupported_fstype"), None


def evaluate(row, mounts, sysfs, device_names):
    """One path row of the output."""
    result = {
        "path": row["path"],
        "fstype": None,
        "mount_point": None,
        "quota_state": "unknown",
        "enforcement": "n/a",
        "basis": "no_covering_mount",
        "device_check": "not_checked",
        "quota_option_keys": [],
        "btrfs_qgroups_mode": None,
    }
    mount, refusal = resolve_mount(mounts, row["realpath"])
    if mount is None:
        result["basis"] = refusal
        return result
    result["fstype"] = mount.fstype
    result["mount_point"] = mount.mount_point
    path_device = row["st_dev"]
    mount_device = (mount.major, mount.minor)
    if mount_device == path_device:
        result["device_check"] = "match"
    elif mount.fstype == "btrfs" and path_device[0] == 0:
        # A btrfs subvolume has an anonymous st_dev; the equality check is
        # skipped instead of reporting a mismatch.
        result["device_check"] = "btrfs_subvolume_skipped"
    else:
        # A device mismatch preempts the filesystem table; a preempted row
        # carries no option keys and no mode.
        result["device_check"] = "mismatch"
        result["quota_state"] = "unknown"
        result["enforcement"] = "n/a"
        result["basis"] = "device_mismatch"
        return result
    keys = option_keys(mount.super_options)
    result["quota_option_keys"] = quota_option_keys(mount.fstype, keys)
    device_name = device_names(mount.source)
    (state, enforcement, basis), mode = classify(
        mount.fstype, keys, device_name, sysfs
    )
    result["quota_state"] = state
    result["enforcement"] = enforcement
    result["basis"] = basis
    result["btrfs_qgroups_mode"] = mode
    return result


def verdict(rows):
    """Enabled wins over unknown; unknown wins over disabled."""
    states = set(row["quota_state"] for row in rows)
    if "enabled" in states:
        return RC_ENABLED, ENABLED
    if "unknown" in states:
        return RC_SETUP, UNKNOWN
    return RC_OK, DISABLED


def scan_btrfs_sysfs():
    """The read-only btrfs sysfs view.

    Each uuid record carries the device names, whether the qgroups directory
    exists (None when it could not be inspected), the enabled attribute and
    the mode text. The mode text is always None here: the mode attribute is
    not read in real mode.
    """
    sysfs = {}
    try:
        names = sorted(os.listdir(BTRFS_SYSFS))
    except OSError:
        # A parent listing error is not an absent qgroups directory.
        return sysfs
    for name in names:
        directory = os.path.join(BTRFS_SYSFS, name)
        try:
            if not os.path.isdir(directory):
                continue
        except OSError:
            continue
        devices = []
        try:
            devices = sorted(os.listdir(os.path.join(directory, "devices")))
        except OSError:
            devices = []
        qgroups = None
        enabled = None
        mode = None
        qgroups_path = os.path.join(directory, "qgroups")
        try:
            os.stat(qgroups_path)
        except FileNotFoundError:
            qgroups = False
        except OSError:
            qgroups = None
        else:
            qgroups = True
            enabled_text = read_sysfs_text(os.path.join(qgroups_path, "enabled"))
            if enabled_text == "1":
                enabled = True
            elif enabled_text == "0":
                enabled = False
            else:
                enabled = None
            # The mode attribute is never read in real mode: its show
            # function asserts that qgroups are enabled, so a read inside a
            # present-but-disabled window can trip a kernel assert, and a
            # disable racing this read makes the read unsafe. The reported
            # mode stays null in real mode.
        sysfs[name] = {
            "devices": devices,
            "qgroups": qgroups,
            "enabled": enabled,
            "mode": mode,
        }
    return sysfs


def read_sysfs_text(path):
    """The stripped text of a sysfs file, or None when it is unreadable."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return None


def real_device_name(source):
    """The basename of the resolved mount source, e.g. dm-0."""
    if not isinstance(source, str) or not source.startswith("/"):
        return source
    try:
        resolved = os.path.realpath(source)
    except OSError:
        resolved = source
    base = os.path.basename(resolved)
    return base if base else source


def probe_real(paths):
    mounts, rows, sysfs = real_inputs(paths)
    evaluated = [evaluate(row, mounts, sysfs, real_device_name) for row in rows]
    code, finding = verdict(evaluated)
    return payload(finding, code, evaluated), code


def real_inputs(paths):
    try:
        with open(MOUNTINFO, "r", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
    except OSError:
        raise Invalid("mountinfo_unreadable") from None
    mounts = parse_mountinfo(text)
    rows = []
    for path in paths:
        try:
            status = os.stat(path)
        except OSError:
            raise Invalid("path_stat_failed") from None
        rows.append(
            {
                "path": path,
                "realpath": os.path.realpath(path),
                "st_dev": (os.major(status.st_dev), os.minor(status.st_dev)),
            }
        )
    return mounts, rows, scan_btrfs_sysfs()


def probe_fixture(path):
    mounts, rows, sysfs, links = load_fixture(path)

    def device_names(source):
        mapped = links.get(source)
        if mapped is not None:
            return os.path.basename(mapped)
        return os.path.basename(source)

    evaluated = [evaluate(row, mounts, sysfs, device_names) for row in rows]
    code, finding = verdict(evaluated)
    return payload(finding, code, evaluated), code


def load_fixture(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = handle.read()
    except OSError:
        raise Invalid("fixture_unreadable") from None
    except UnicodeError:
        raise Invalid("fixture_invalid_json") from None
    obj = parse_json(data)
    require(isinstance(obj, dict), "fixture_not_object")
    require(set(obj.keys()) == FIXTURE_KEYS, "fixture_key_set")
    require(obj["schema"] == FIXTURE_SCHEMA, "fixture_schema")
    mountinfo = obj["mountinfo"]
    require(isinstance(mountinfo, str), "fixture_mountinfo")
    mounts = parse_mountinfo(mountinfo)
    paths = obj["paths"]
    require(isinstance(paths, list) and paths, "fixture_paths")
    rows = []
    seen = set()
    for item in paths:
        require(isinstance(item, dict) and set(item) == PATH_KEYS,
                "fixture_path_entry")
        target = item["path"]
        resolved = item["realpath"]
        device = item["st_dev"]
        require(normalized_absolute(target), "fixture_path_not_normalized")
        require(normalized_absolute(resolved), "fixture_path_not_normalized")
        require(target not in seen, "fixture_duplicate_path")
        seen.add(target)
        require(isinstance(device, str), "fixture_st_dev_malformed")
        match = DEVICE_RE.match(device)
        require(match is not None, "fixture_st_dev_malformed")
        rows.append(
            {
                "path": target,
                "realpath": resolved,
                "st_dev": (int(match.group(1)), int(match.group(2))),
            }
        )
    links = obj["device_links"]
    require(isinstance(links, dict), "fixture_device_links")
    for key, value in links.items():
        require(isinstance(key, str) and key, "fixture_device_links")
        require(plain_basename(value), "fixture_device_links")
    sysfs = obj["btrfs_sysfs"]
    require(isinstance(sysfs, dict), "fixture_btrfs_sysfs")
    for uuid in sorted(sysfs):
        entry = sysfs[uuid]
        require(isinstance(uuid, str) and UUID_RE.match(uuid), "fixture_btrfs_uuid")
        require(isinstance(entry, dict), "fixture_btrfs_sysfs")
        require(set(entry.keys()) == UUID_KEYS, "fixture_btrfs_record_keys")
        devices = entry["devices"]
        qgroups = entry["qgroups"]
        enabled = entry["qgroups_enabled"]
        mode = entry["qgroups_mode"]
        require(isinstance(devices, list), "fixture_btrfs_sysfs")
        for device in devices:
            require(plain_basename(device), "fixture_btrfs_devices")
        require(type(qgroups) is bool, "fixture_btrfs_qgroups")
        require(enabled is None or type(enabled) is bool, "fixture_btrfs_enabled")
        require(mode is None or isinstance(mode, str), "fixture_btrfs_mode")
        if qgroups is False:
            # An absent qgroups directory pairs with no enabled attribute and
            # no mode text.
            require(enabled is None, "fixture_btrfs_qgroups_pairing")
            require(mode is None, "fixture_btrfs_qgroups_pairing")
        if enabled is not True:
            # In fixture mode the mode text is projected only when the
            # enabled attribute is 1.
            require(mode is None, "fixture_btrfs_mode_pairing")
        sysfs[uuid] = {
            "devices": list(devices),
            "qgroups": qgroups,
            "enabled": enabled,
            "mode": btrfs_modes(mode),
        }
    return mounts, rows, sysfs, links


def payload(finding, code, rows):
    return {
        "schema": SCHEMA,
        "finding_id": finding,
        "exit_code": code,
        "paths": rows,
        "df_covers_quota": False,
        "limits": ". ".join(LIMITS) + ".",
    }


def setup_payload(reason):
    return {
        "schema": SCHEMA,
        "finding_id": SETUP,
        "exit_code": RC_SETUP,
        "paths": [evaluate({"path": FLEET_ROOT, "realpath": FLEET_ROOT}, [], {}, os.path.basename)],
        "df_covers_quota": False,
        "limits": ". ".join(LIMITS) + ".",
        "error": reason,
    }


def emit(body, code):
    try:
        print(json.dumps(body, sort_keys=True, separators=(",", ":")))
        sys.stdout.flush()
    except OSError:
        # A closed stdout cannot carry a verdict.
        os._exit(RC_SETUP)
    return code


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Invalid("usage")

    def exit(self, status=0, message=None):
        raise Invalid("usage")


def parse_args(argv=None):
    parser = Parser(
        description=__doc__,
        add_help=False,
        allow_abbrev=False,
    )
    parser.add_argument("--path", action="append", metavar="ABS")
    parser.add_argument("--fixture", metavar="FILE")
    parser.add_argument("--selftest", action="store_true")
    return parser.parse_args(argv)


def mount_line(mount_id, device, mount_point, fstype, source, super_options,
               optional="", parent=25):
    """One synthetic mountinfo line (proc.rst section 3.5 field order)."""
    parts = [
        "%d %d %s / %s rw,relatime" % (mount_id, parent, device, mount_point),
    ]
    if optional:
        parts.append(optional)
    parts.extend(["-", fstype, source, super_options])
    return " ".join(parts)


def fixture(mountinfo, paths, device_links=None, btrfs_sysfs=None, extra=None,
            drop=None):
    body = {
        "schema": FIXTURE_SCHEMA,
        "mountinfo": mountinfo,
        "paths": paths,
        "device_links": device_links or {},
        "btrfs_sysfs": btrfs_sysfs or {},
    }
    if extra:
        body.update(extra)
    if drop:
        for key in drop:
            body.pop(key, None)
    return body


def path_entry(path, realpath=None, st_dev="259:1"):
    return {"path": path, "realpath": realpath or path, "st_dev": st_dev}


def uuid_record(devices, qgroups, enabled, mode=None):
    return {
        "devices": list(devices),
        "qgroups": qgroups,
        "qgroups_enabled": enabled,
        "qgroups_mode": mode,
    }


def selftest():
    """Isolated synthetic fixture arms. No arm reads host filesystem state."""
    tool = Path(__file__).resolve()
    failures = []
    arms = []
    with tempfile.TemporaryDirectory(prefix="mori-quota-v2-") as tmp:
        root = Path(tmp)

        def write_fixture(name, body):
            target = root / ("%s.json" % name)
            if isinstance(body, bytes):
                target.write_bytes(body)
            else:
                target.write_text(json.dumps(body, sort_keys=True), encoding="utf-8")
            return target

        def arm(name, body, want_code, want_finding, want_paths):
            arms.append(
                (
                    name,
                    ["--fixture", str(write_fixture(name, body))],
                    want_code,
                    want_finding,
                    want_paths,
                )
            )

        def cli_arm(name, argv, want_code, want_finding):
            arms.append((name, argv, want_code, want_finding, None))

        xfs_line = mount_line(36, "259:1", "/srv", "xfs", "/dev/sda1", "rw,usrquota")
        arm(
            "xfs-usrquota",
            fixture(xfs_line, [path_entry("/srv")]),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/srv",
                    "fstype": "xfs",
                    "mount_point": "/srv",
                    "quota_state": "enabled",
                    "enforcement": "enforced",
                    "basis": "xfs_quota_option",
                    "device_check": "match",
                    "quota_option_keys": ["usrquota"],
                }
            ],
        )
        arm(
            "xfs-noquota",
            fixture(
                mount_line(36, "259:1", "/srv", "xfs", "/dev/sda1", "rw,noquota"),
                [path_entry("/srv")],
            ),
            RC_OK,
            DISABLED,
            [
                {
                    "path": "/srv",
                    "fstype": "xfs",
                    "mount_point": "/srv",
                    "quota_state": "disabled",
                    "enforcement": "n/a",
                    "basis": "xfs_noquota_option",
                    "device_check": "match",
                    "quota_option_keys": ["noquota"],
                }
            ],
        )
        arm(
            "xfs-conflict-noenforce",
            fixture(
                mount_line(36, "259:1", "/srv", "xfs", "/dev/sda1", "rw,noquota,uqnoenforce"),
                [path_entry("/srv")],
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/srv",
                    "fstype": "xfs",
                    "mount_point": "/srv",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "xfs_conflicting_quota_options",
                    "quota_option_keys": ["noquota", "uqnoenforce"],
                }
            ],
        )
        arm(
            "xfs-accounting-only",
            fixture(
                mount_line(36, "259:1", "/srv", "xfs", "/dev/sda1", "rw,uqnoenforce"),
                [path_entry("/srv")],
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/srv",
                    "fstype": "xfs",
                    "mount_point": "/srv",
                    "quota_state": "enabled",
                    "enforcement": "accounting_only",
                    "basis": "xfs_quota_option",
                    "quota_option_keys": ["uqnoenforce"],
                }
            ],
        )
        arm(
            "xfs-options-absent",
            fixture(
                mount_line(36, "259:1", "/srv", "xfs", "/dev/sda1", "rw,attr2,inode64"),
                [path_entry("/srv")],
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/srv",
                    "fstype": "xfs",
                    "mount_point": "/srv",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "xfs_quota_options_absent",
                    "quota_option_keys": [],
                }
            ],
        )
        arm(
            "ext4-usrquota-unverified",
            fixture(
                mount_line(37, "8:1", "/srv", "ext4", "/dev/sdb1", "rw,usrquota,data=ordered"),
                [path_entry("/srv", st_dev="8:1")],
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/srv",
                    "fstype": "ext4",
                    "mount_point": "/srv",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "ext_quota_option_unverified",
                    "quota_option_keys": ["usrquota"],
                }
            ],
        )
        arm(
            "ext4-journaled-unverified",
            fixture(
                mount_line(
                    37,
                    "8:1",
                    "/srv",
                    "ext4",
                    "/dev/sdb1",
                    "rw,usrjquota=aquota.user,jqfmt=vfsv0",
                ),
                [path_entry("/srv", st_dev="8:1")],
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/srv",
                    "fstype": "ext4",
                    "mount_point": "/srv",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "ext_quota_option_unverified",
                    "quota_option_keys": ["jqfmt", "usrjquota"],
                }
            ],
        )
        arm(
            "ext4-options-absent",
            fixture(
                mount_line(37, "8:1", "/srv", "ext4", "/dev/sdb1", "rw"),
                [path_entry("/srv", st_dev="8:1")],
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/srv",
                    "fstype": "ext4",
                    "mount_point": "/srv",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "ext_quota_superblock_unobservable",
                    "quota_option_keys": [],
                }
            ],
        )
        arm(
            "tmpfs-usrquota",
            fixture(
                mount_line(38, "0:38", "/dev/shm", "tmpfs", "tmpfs", "rw,usrquota"),
                [path_entry("/dev/shm", st_dev="0:38")],
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/dev/shm",
                    "fstype": "tmpfs",
                    "mount_point": "/dev/shm",
                    "quota_state": "enabled",
                    "enforcement": "enforced",
                    "basis": "tmpfs_quota_option",
                    "quota_option_keys": ["usrquota"],
                }
            ],
        )
        arm(
            "tmpfs-hardlimit",
            fixture(
                mount_line(
                    39,
                    "0:39",
                    "/run/lane",
                    "tmpfs",
                    "tmpfs",
                    "rw,grpquota_block_hardlimit=1m",
                ),
                [path_entry("/run/lane", st_dev="0:39")],
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/run/lane",
                    "fstype": "tmpfs",
                    "mount_point": "/run/lane",
                    "quota_state": "enabled",
                    "enforcement": "enforced",
                    "basis": "tmpfs_quota_option",
                    "quota_option_keys": ["grpquota_block_hardlimit"],
                }
            ],
        )
        arm(
            "tmpfs-arbitrary-hardlimit-ignored",
            fixture(
                mount_line(40, "0:40", "/run/lane", "tmpfs", "tmpfs", "rw,other_hardlimit=1m"),
                [path_entry("/run/lane", st_dev="0:40")],
            ),
            RC_OK,
            DISABLED,
            [
                {
                    "path": "/run/lane",
                    "fstype": "tmpfs",
                    "mount_point": "/run/lane",
                    "quota_state": "disabled",
                    "enforcement": "n/a",
                    "basis": "tmpfs_quota_options_absent",
                    "quota_option_keys": [],
                }
            ],
        )
        btrfs_line = mount_line(
            65, "0:30", "/home", "btrfs", "/dev/mapper/root", "rw,subvol=/@home"
        )
        arm(
            "btrfs-qgroups-enabled",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "1d02a454-c549-4a35-b567-89d60902af8e": uuid_record(
                        ["dm-0"], True, True, "squota"
                    )
                },
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/home",
                    "fstype": "btrfs",
                    "mount_point": "/home",
                    "quota_state": "enabled",
                    "enforcement": "unknown",
                    "basis": "btrfs_qgroups_enabled",
                    "device_check": "btrfs_subvolume_skipped",
                    "quota_option_keys": [],
                    "btrfs_qgroups_mode": "squota",
                }
            ],
        )
        arm(
            "btrfs-qgroups-disabled",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "1d02a454-c549-4a35-b567-89d60902af8e": uuid_record(
                        ["dm-0"], True, False, None
                    )
                },
            ),
            RC_OK,
            DISABLED,
            [
                {
                    "path": "/home",
                    "fstype": "btrfs",
                    "mount_point": "/home",
                    "quota_state": "disabled",
                    "enforcement": "n/a",
                    "basis": "btrfs_qgroups_disabled",
                    "device_check": "btrfs_subvolume_skipped",
                    "quota_option_keys": [],
                    "btrfs_qgroups_mode": None,
                }
            ],
        )
        arm(
            "btrfs-enabled-unavailable",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "1d02a454-c549-4a35-b567-89d60902af8e": uuid_record(
                        ["dm-0"], True, None, None
                    )
                },
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/home",
                    "fstype": "btrfs",
                    "mount_point": "/home",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "btrfs_qgroups_enabled_unavailable",
                    "device_check": "btrfs_subvolume_skipped",
                    "quota_option_keys": [],
                    "btrfs_qgroups_mode": None,
                }
            ],
        )
        arm(
            "btrfs-qgroups-absent",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "1d02a454-c549-4a35-b567-89d60902af8e": uuid_record(
                        ["dm-0"], False, None, None
                    )
                },
            ),
            RC_OK,
            DISABLED,
            [
                {
                    "path": "/home",
                    "fstype": "btrfs",
                    "mount_point": "/home",
                    "quota_state": "disabled",
                    "enforcement": "n/a",
                    "basis": "btrfs_qgroups_dir_absent",
                    "device_check": "btrfs_subvolume_skipped",
                    "quota_option_keys": [],
                    "btrfs_qgroups_mode": None,
                }
            ],
        )
        arm(
            "btrfs-device-unmapped",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "1d02a454-c549-4a35-b567-89d60902af8e": uuid_record(
                        ["dm-9"], True, True, "qgroup"
                    )
                },
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/home",
                    "fstype": "btrfs",
                    "mount_point": "/home",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "btrfs_device_unmapped",
                    "quota_option_keys": [],
                }
            ],
        )
        arm(
            "btrfs-two-uuids",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "1d02a454-c549-4a35-b567-89d60902af8e": uuid_record(
                        ["dm-0"], True, True, "qgroup"
                    ),
                    "2d02a454-c549-4a35-b567-89d60902af8e": uuid_record(
                        ["dm-0"], False, None, None
                    ),
                },
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/home",
                    "fstype": "btrfs",
                    "mount_point": "/home",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "btrfs_device_unmapped",
                    "quota_option_keys": [],
                }
            ],
        )
        arm(
            "btrfs-device-mismatch",
            fixture(
                mount_line(65, "0:30", "/home", "btrfs", "/dev/mapper/root", "rw"),
                [path_entry("/home", st_dev="8:1")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "1d02a454-c549-4a35-b567-89d60902af8e": uuid_record(
                        ["dm-0"], True, True, "qgroup"
                    )
                },
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/home",
                    "fstype": "btrfs",
                    "mount_point": "/home",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "device_mismatch",
                    "device_check": "mismatch",
                    "quota_option_keys": [],
                }
            ],
        )
        arm(
            "ambiguous-overmount",
            fixture(
                "\n".join(
                    [
                        mount_line(70, "259:1", "/srv", "xfs", "/dev/sda1", "rw,usrquota"),
                        mount_line(71, "259:2", "/srv", "xfs", "/dev/sdb1", "rw,noquota"),
                    ]
                ),
                [path_entry("/srv", st_dev="259:1")],
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/srv",
                    "fstype": None,
                    "mount_point": None,
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "ambiguous_overmount",
                    "device_check": "not_checked",
                    "quota_option_keys": [],
                    "btrfs_qgroups_mode": None,
                }
            ],
        )
        arm(
            "no-covering-mount",
            fixture(
                mount_line(72, "259:1", "/srv", "xfs", "/dev/sda1", "rw,usrquota"),
                [path_entry("/elsewhere/place")],
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/elsewhere/place",
                    "fstype": None,
                    "mount_point": None,
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "no_covering_mount",
                    "device_check": "not_checked",
                    "quota_option_keys": [],
                    "btrfs_qgroups_mode": None,
                }
            ],
        )
        arm(
            "xfs-device-mismatch",
            fixture(
                mount_line(73, "259:1", "/srv", "xfs", "/dev/sda1", "rw,usrquota"),
                [path_entry("/srv", st_dev="8:1")],
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/srv",
                    "fstype": "xfs",
                    "mount_point": "/srv",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "device_mismatch",
                    "device_check": "mismatch",
                    "quota_option_keys": [],
                    "btrfs_qgroups_mode": None,
                }
            ],
        )
        arm(
            "parent-id-refusal",
            fixture(
                "\n".join(
                    [
                        mount_line(90, "259:1", "/srv", "xfs", "/dev/sda1", "rw,usrquota", parent=25),
                        mount_line(33, "259:9", "/", "xfs", "/dev/sdb1", "rw,noquota", parent=33),
                        mount_line(25, "259:8", "/other", "xfs", "/dev/sdc1", "rw", parent=33),
                    ]
                ),
                [path_entry("/srv", st_dev="259:1")],
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/srv",
                    "fstype": None,
                    "mount_point": None,
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "ambiguous_overmount",
                    "device_check": "not_checked",
                    "quota_option_keys": [],
                    "btrfs_qgroups_mode": None,
                }
            ],
        )
        arm(
            "parent-id-consistent",
            fixture(
                "\n".join(
                    [
                        mount_line(90, "259:1", "/srv", "xfs", "/dev/sda1", "rw,usrquota", parent=33),
                        mount_line(33, "259:9", "/", "xfs", "/dev/sdb1", "rw,noquota", parent=33),
                    ]
                ),
                [path_entry("/srv", st_dev="259:1")],
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/srv",
                    "fstype": "xfs",
                    "mount_point": "/srv",
                    "quota_state": "enabled",
                    "enforcement": "enforced",
                    "basis": "xfs_quota_option",
                    "device_check": "match",
                    "quota_option_keys": ["usrquota"],
                }
            ],
        )
        arm(
            "parent-id-absent",
            fixture(
                "\n".join(
                    [
                        mount_line(90, "259:1", "/srv", "xfs", "/dev/sda1", "rw,usrquota", parent=999),
                        mount_line(33, "259:9", "/", "xfs", "/dev/sdb1", "rw,noquota", parent=33),
                    ]
                ),
                [path_entry("/srv", st_dev="259:1")],
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/srv",
                    "fstype": "xfs",
                    "mount_point": "/srv",
                    "quota_state": "enabled",
                    "enforcement": "enforced",
                    "basis": "xfs_quota_option",
                    "device_check": "match",
                    "quota_option_keys": ["usrquota"],
                }
            ],
        )
        arm(
            "unsupported-fstype",
            fixture(
                mount_line(74, "0:41", "/srv", "overlay", "overlay", "rw,lowerdir=/x"),
                [path_entry("/srv", st_dev="0:41")],
            ),
            RC_SETUP,
            UNKNOWN,
            [
                {
                    "path": "/srv",
                    "fstype": "overlay",
                    "mount_point": "/srv",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "unsupported_fstype",
                    "quota_option_keys": [],
                }
            ],
        )
        arm(
            "enabled-plus-unknown",
            fixture(
                "\n".join(
                    [
                        mount_line(75, "259:1", "/srv", "xfs", "/dev/sda1", "rw,usrquota"),
                        mount_line(76, "8:1", "/other", "ext4", "/dev/sdb1", "rw"),
                    ]
                ),
                [path_entry("/srv"), path_entry("/other", st_dev="8:1")],
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/srv",
                    "fstype": "xfs",
                    "mount_point": "/srv",
                    "quota_state": "enabled",
                    "enforcement": "enforced",
                    "basis": "xfs_quota_option",
                },
                {
                    "path": "/other",
                    "fstype": "ext4",
                    "mount_point": "/other",
                    "quota_state": "unknown",
                    "enforcement": "n/a",
                    "basis": "ext_quota_superblock_unobservable",
                },
            ],
        )
        arm(
            "escaped-mount-point",
            fixture(
                mount_line(77, "259:2", "/srv\\040data", "xfs", "/dev/sdc1", "rw,usrquota"),
                [path_entry("/srv data", st_dev="259:2")],
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/srv data",
                    "fstype": "xfs",
                    "mount_point": "/srv data",
                    "quota_state": "enabled",
                    "enforcement": "enforced",
                    "basis": "xfs_quota_option",
                }
            ],
        )
        arm(
            "optional-mountinfo-fields",
            fixture(
                mount_line(
                    78,
                    "259:3",
                    "/srv",
                    "xfs",
                    "/dev/sdd1",
                    "rw,usrquota",
                    optional="shared:1 master:2 propagate_from:3",
                ),
                [path_entry("/srv", st_dev="259:3")],
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/srv",
                    "fstype": "xfs",
                    "mount_point": "/srv",
                    "quota_state": "enabled",
                    "enforcement": "enforced",
                    "basis": "xfs_quota_option",
                }
            ],
        )
        arm(
            "symlink-resolved-path",
            fixture(
                mount_line(79, "259:4", "/real", "xfs", "/dev/sde1", "rw,usrquota"),
                [path_entry("/link", realpath="/real", st_dev="259:4")],
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/link",
                    "fstype": "xfs",
                    "mount_point": "/real",
                    "quota_state": "enabled",
                    "enforcement": "enforced",
                    "basis": "xfs_quota_option",
                }
            ],
        )
        arm(
            "longest-mount-point-wins",
            fixture(
                "\n".join(
                    [
                        mount_line(80, "259:5", "/", "xfs", "/dev/sdf1", "rw,noquota"),
                        mount_line(81, "259:6", "/srv/data", "xfs", "/dev/sdg1", "rw,usrquota"),
                    ]
                ),
                [path_entry("/srv/data", st_dev="259:6")],
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/srv/data",
                    "fstype": "xfs",
                    "mount_point": "/srv/data",
                    "quota_state": "enabled",
                    "enforcement": "enforced",
                    "basis": "xfs_quota_option",
                }
            ],
        )
        arm(
            "invalid-octal-escape",
            fixture(
                mount_line(82, "259:7", "/srv\\135x", "xfs", "/dev/sdh1", "rw,usrquota"),
                [path_entry("/srv")],
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-malformed-st-dev",
            fixture(
                mount_line(83, "259:8", "/srv", "xfs", "/dev/sdi1", "rw,usrquota"),
                [path_entry("/srv", st_dev="00:57")],
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-relative-path",
            fixture(
                mount_line(84, "259:9", "/srv", "xfs", "/dev/sdj1", "rw,usrquota"),
                [{"path": "relative/path", "realpath": "relative/path", "st_dev": "259:9"}],
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-dotdot-path",
            fixture(
                mount_line(85, "259:10", "/srv", "xfs", "/dev/sdk1", "rw,usrquota"),
                [{"path": "/srv/../etc", "realpath": "/srv/../etc", "st_dev": "259:10"}],
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-duplicate-path",
            fixture(
                mount_line(86, "259:11", "/srv", "xfs", "/dev/sdl1", "rw,usrquota"),
                [path_entry("/srv", st_dev="259:11"), path_entry("/srv", st_dev="259:11")],
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-non-canonical-uuid",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "not-a-uuid": uuid_record(["dm-0"], True, True, "qgroup")
                },
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-device-name-with-slash",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "1d02a454-c549-4a35-b567-89d60902af8e": uuid_record(
                        ["dm/0"], True, True, "qgroup"
                    )
                },
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-qgroups-pairing",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "1d02a454-c549-4a35-b567-89d60902af8e": uuid_record(
                        ["dm-0"], False, True, None
                    )
                },
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-extra-record-key",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "1d02a454-c549-4a35-b567-89d60902af8e": dict(
                        uuid_record(["dm-0"], True, True, "qgroup"), extra="x"
                    )
                },
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-missing-record-key",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "1d02a454-c549-4a35-b567-89d60902af8e": {
                        "devices": ["dm-0"],
                        "qgroups": True,
                        "qgroups_enabled": True,
                    }
                },
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-extra-top-level-key",
            fixture(
                mount_line(87, "259:12", "/srv", "xfs", "/dev/sdm1", "rw,usrquota"),
                [path_entry("/srv", st_dev="259:12")],
                extra={"unexpected": True},
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-unparseable-mountinfo",
            fixture("this is not a mountinfo line\n", [path_entry("/srv")]),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-malformed-json",
            b"{ not json",
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-empty-path-population",
            fixture(xfs_line, []),
            RC_SETUP,
            SETUP,
            [],
        )
        arm(
            "setup-extra-path-record-key",
            fixture(xfs_line, [dict(path_entry("/srv"), unexpected=True)]),
            RC_SETUP,
            SETUP,
            [],
        )
        cli_arm(
            "setup-unknown-argument",
            ["--unknown-flag"],
            RC_SETUP,
            SETUP,
        )
        cli_arm(
            "setup-relative-path-argument",
            ["--path", "relative/path"],
            RC_SETUP,
            SETUP,
        )
        cli_arm(
            "setup-fixture-with-path",
            [
                "--fixture",
                str(write_fixture("fixture-with-path", fixture(xfs_line, []))),
                "--path",
                "/srv",
            ],
            RC_SETUP,
            SETUP,
        )
        cli_arm(
            "setup-selftest-with-path",
            ["--selftest", "--path", "/srv"],
            RC_SETUP,
            SETUP,
        )

        for name, argv, want_code, want_finding, want_paths in arms:
            command = [sys.executable, str(tool)] + argv
            completed = subprocess.run(command, capture_output=True, text=True)
            label = "arm %s" % name
            if completed.stderr:
                failures.append("%s: stderr was not empty" % label)
            try:
                body = json.loads(completed.stdout)
            except ValueError:
                failures.append("%s: stdout is not one JSON object" % label)
                continue
            if completed.returncode != want_code:
                failures.append(
                    "%s: rc=%d want=%d" % (label, completed.returncode, want_code)
                )
            if body.get("finding_id") != want_finding:
                failures.append(
                    "%s: finding_id=%r want=%r"
                    % (label, body.get("finding_id"), want_finding)
                )
            if body.get("schema") != SCHEMA:
                failures.append(
                    "%s: schema=%r want=%r" % (label, body.get("schema"), SCHEMA)
                )
            if body.get("df_covers_quota") is not False:
                failures.append("%s: df_covers_quota was not false" % label)
            if want_paths is None:
                if body.get("paths") != []:
                    failures.append("%s: a setup error carried a partial verdict" % label)
                continue
            rows = body.get("paths") or []
            if len(rows) != len(want_paths):
                failures.append(
                    "%s: path count=%d want=%d" % (label, len(rows), len(want_paths))
                )
                continue
            for index, want in enumerate(want_paths):
                got = rows[index]
                for key in sorted(want):
                    # The six primary fields and the supplementary metadata
                    # are scored separately: the primary denominator is never
                    # widened by a metadata key.
                    kind = "primary" if key in PRIMARY_FIELDS else "supplementary"
                    if got.get(key) != want[key]:
                        failures.append(
                            "%s: %s paths[%d].%s=%r want=%r"
                            % (label, kind, index, key, got.get(key), want[key])
                        )
                if set(got.keys()) != OUTPUT_FIELDS:
                    failures.append("%s: paths[%d] carried an unexpected key" % (label, index))

    if failures:
        return emit(
            {
                "schema": SCHEMA,
                "finding_id": "QUOTA_SELFTEST_FAIL",
                "exit_code": RC_ENABLED,
                "arms": len(arms),
                "failures": failures,
            },
            RC_ENABLED,
        )
    return emit(
        {
            "schema": SCHEMA,
            "finding_id": "QUOTA_SELFTEST_OK",
            "exit_code": RC_OK,
            "arms": len(arms),
        },
        RC_OK,
    )


def main(argv=None):
    try:
        args = parse_args(argv)
        if args.selftest:
            require(args.path is None and args.fixture is None, "usage")
            return selftest()
        if args.fixture is not None:
            require(not args.path, "usage")
            body, code = probe_fixture(args.fixture)
        else:
            paths = list(args.path) if args.path else list(DEFAULT_PATHS)
            for path in paths:
                require(
                    isinstance(path, str) and path.startswith("/"),
                    "path_not_absolute",
                )
            body, code = probe_real(paths)
    except Invalid as exc:
        return emit(setup_payload(str(exc)), RC_SETUP)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError,
            RecursionError, MemoryError):
        return emit(setup_payload("input_unavailable"), RC_SETUP)
    return emit(body, code)


if __name__ == "__main__":
    sys.exit(main())
