#!/usr/bin/env python3
"""mori-quota-surface.py — read-only quota-surface probe (FR2 / EDQUOT).

WHAT THIS PROBE IS

  A read-only observability probe. `df` capacity percentages cannot see quota
  exhaustion: the fleet's actually reported disk failures are quota events
  (EDQUOT), and a capacity-percent probe cannot see them. This probe reports,
  per path, whether a filesystem quota mechanism is visibly enabled, visibly
  disabled, or unknown.

  It never calls quotactl, `btrfs qgroup`, `xfs_quota`, `repquota`, mounts,
  writes, or any other privileged or mutating interface. It never reads
  credential, token or session material. It reports a surface, not a limit:
  "enabled" means a quota mechanism is visibly configured for that mount, not
  that any per-user, per-group or per-project limit exists.

INPUTS (real mode, read-only)

  /proc/self/mountinfo, os.stat(path).st_dev, os.path.realpath(path),
  os.path.realpath(mount_source) basename, directory listings and existence
  under /sys/fs/btrfs/*/devices/ and /sys/fs/btrfs/<uuid>/qgroups, and the
  text of /sys/fs/btrfs/<uuid>/qgroups/mode when that file is present.

  Mount resolution follows proc.rst section 3.5: fields 1-6, then optional
  fields up to the "-" separator, then filesystem type, mount source and
  super options. Octal escapes (\\040, \\011, \\012, \\134) are decoded in the
  mount point. Candidate mounts are those whose mount point equals the
  resolved path, is "/", or is a prefix of the resolved path followed by
  "/". The longest mount point wins; among equal mount points the last
  mountinfo line wins.

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
  carries path, fstype, mount_point, quota_state, enforcement, basis,
  device_check, quota_option_keys and btrfs_qgroups_mode. Mount sources,
  non-quota mount options and option values are never echoed.

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
  btrfs qgroup directory does not imply that any limit is set. An ext2/ext3/
  ext4 quota feature in the superblock is unobservable without privileged
  tools. sysfs and mountinfo races during quota enable, disable or remount
  are not excluded.

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
    "a visible btrfs qgroup directory does not imply that any limit is set",
    "an ext2/ext3/ext4 quota feature in the superblock is unobservable without privileged tools",
    "sysfs and mountinfo races during quota enable, disable or remount are not excluded",
    "df capacity percentages never cover quota exhaustion (FR2 / EDQUOT)",
)

FIXTURE_KEYS = frozenset(
    ("schema", "mountinfo", "paths", "device_links", "btrfs_sysfs")
)

XFS_QUOTA_KEYS = frozenset(
    ("usrquota", "uquota", "quota", "grpquota", "gquota", "prjquota", "pquota")
)
XFS_NOENFORCE_KEYS = frozenset(
    ("uqnoenforce", "gqnoenforce", "pqnoenforce", "qnoenforce")
)
XFS_NEGATIVE_KEYS = frozenset(("noquota",))
EXT_QUOTA_KEYS = frozenset(
    ("quota", "usrquota", "grpquota", "prjquota", "usrjquota", "grpjquota")
)
TMPFS_QUOTA_KEYS = frozenset(("quota", "usrquota", "grpquota"))

DEVICE_RE = re.compile(r"\A([0-9]+):([0-9]+)\Z")
OCTAL_ESCAPES = {"040": " ", "011": "\t", "012": "\n", "134": "\\"}


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
        "mount_point",
        "fstype",
        "source",
        "major",
        "minor",
        "super_options",
        "order",
    )

    def __init__(self, mount_point, fstype, source, major, minor,
                 super_options, order):
        self.mount_point = mount_point
        self.fstype = fstype
        self.source = source
        self.major = major
        self.minor = minor
        self.super_options = super_options
        self.order = order


def unescape_mount_point(value):
    """Decode the octal escapes the kernel writes in a mount point."""
    out = []
    index = 0
    length = len(value)
    while index < length:
        char = value[index]
        if char == "\\":
            escape = value[index + 1:index + 4]
            if len(escape) == 3 and escape in OCTAL_ESCAPES:
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
            continue
        parts = line.split(" ")
        require(len(parts) >= 6, "mountinfo_line_unparseable")
        try:
            separator = parts.index("-")
        except ValueError:
            raise Invalid("mountinfo_line_unparseable") from None
        # Fields 1-6 precede the optional fields and the "-" separator.
        require(separator >= 6, "mountinfo_line_unparseable")
        require(len(parts) >= separator + 3, "mountinfo_line_unparseable")
        device = DEVICE_RE.match(parts[2])
        require(device is not None, "mountinfo_line_unparseable")
        super_options = parts[separator + 3] if len(parts) > separator + 3 else ""
        mounts.append(
            Mount(
                mount_point=unescape_mount_point(parts[4]),
                fstype=parts[separator + 1],
                source=parts[separator + 2],
                major=int(device.group(1)),
                minor=int(device.group(2)),
                super_options=super_options,
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
        related = TMPFS_QUOTA_KEYS | frozenset(
            key for key in keys if key.endswith("_hardlimit")
        )
    else:
        related = frozenset()
    return sorted(keys & related)


def btrfs_uuids_for_device(device_name, sysfs):
    """Every uuid whose devices directory lists the mount's device."""
    if not device_name:
        return []
    return [
        uuid
        for uuid in sorted(sysfs)
        if device_name in sysfs[uuid]["devices"]
    ]


def classify(fstype, keys, device_name, sysfs):
    """The contract's quota classification table."""
    if fstype == "xfs":
        if "noquota" in keys and keys & XFS_QUOTA_KEYS:
            return ("unknown", "n/a", "xfs_conflicting_quota_options")
        if "noquota" in keys:
            return ("disabled", "n/a", "xfs_noquota_option")
        if keys & XFS_QUOTA_KEYS:
            return ("enabled", "enforced", "xfs_quota_option")
        if keys & XFS_NOENFORCE_KEYS:
            return ("enabled", "accounting_only", "xfs_quota_option")
        return ("unknown", "n/a", "xfs_quota_options_absent")
    if fstype == "btrfs":
        matched = btrfs_uuids_for_device(device_name, sysfs)
        if len(matched) != 1:
            return ("unknown", "n/a", "btrfs_device_unmapped")
        if sysfs[matched[0]]["qgroups"]:
            return ("enabled", "unknown", "btrfs_qgroups_dir_present")
        return ("disabled", "n/a", "btrfs_qgroups_dir_absent")
    if fstype in ("ext2", "ext3", "ext4"):
        if keys & EXT_QUOTA_KEYS:
            return ("enabled", "unknown", "ext_quota_option")
        return ("unknown", "n/a", "ext_quota_superblock_unobservable")
    if fstype == "tmpfs":
        hardlimit = any(key.endswith("_hardlimit") for key in keys)
        if (keys & TMPFS_QUOTA_KEYS) or hardlimit:
            return ("enabled", "enforced", "tmpfs_quota_option")
        return ("disabled", "n/a", "tmpfs_quota_options_absent")
    return ("unknown", "n/a", "unsupported_fstype")


def select_mount(mounts, resolved):
    """The covering mount: longest mount point, last line on a tie."""
    best = None
    for mount in mounts:
        point = mount.mount_point
        if not (
            point == resolved
            or point == "/"
            or resolved.startswith(point + "/")
        ):
            continue
        if best is None:
            best = mount
            continue
        if len(point) > len(best.mount_point):
            best = mount
        elif len(point) == len(best.mount_point) and mount.order > best.order:
            best = mount
    return best


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
    mount = select_mount(mounts, row["realpath"])
    if mount is None:
        return result
    result["fstype"] = mount.fstype
    result["mount_point"] = mount.mount_point
    keys = option_keys(mount.super_options)
    result["quota_option_keys"] = quota_option_keys(mount.fstype, keys)
    same_device = (mount.major, mount.minor) == row["st_dev"]
    if mount.fstype == "btrfs":
        # A btrfs subvolume has an anonymous st_dev; a mismatch is expected.
        result["device_check"] = "match" if same_device else "btrfs_subvolume_skipped"
    elif not same_device:
        result["device_check"] = "mismatch"
        result["quota_state"] = "unknown"
        result["enforcement"] = "n/a"
        result["basis"] = "device_mismatch"
        return result
    else:
        result["device_check"] = "match"
    device_name = device_names(mount.source)
    if mount.fstype == "btrfs":
        matched = btrfs_uuids_for_device(device_name, sysfs)
        if len(matched) == 1:
            result["btrfs_qgroups_mode"] = sysfs[matched[0]]["qgroups_mode"]
    state, enforcement, basis = classify(
        mount.fstype, keys, device_name, sysfs
    )
    result["quota_state"] = state
    result["enforcement"] = enforcement
    result["basis"] = basis
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
    """The read-only btrfs sysfs view: devices, qgroups, qgroups mode."""
    sysfs = {}
    try:
        names = sorted(os.listdir(BTRFS_SYSFS))
    except OSError:
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
        try:
            qgroups = os.path.isdir(os.path.join(directory, "qgroups"))
        except OSError:
            qgroups = False
        mode = None
        if qgroups:
            try:
                with open(
                    os.path.join(directory, "qgroups", "mode"),
                    "r",
                    encoding="utf-8",
                    errors="replace",
                ) as handle:
                    mode = handle.read().strip() or None
            except OSError:
                mode = None
        sysfs[name] = {
            "devices": devices,
            "qgroups": qgroups,
            "qgroups_mode": mode,
        }
    return sysfs


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
        return links.get(source)

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
    require(isinstance(paths, list), "fixture_paths")
    rows = []
    for item in paths:
        require(isinstance(item, dict), "fixture_path_entry")
        for key in ("path", "realpath", "st_dev"):
            require(key in item, "fixture_path_entry")
        target = item["path"]
        resolved = item["realpath"]
        device = item["st_dev"]
        require(
            isinstance(target, str) and target.startswith("/"),
            "fixture_path_not_absolute",
        )
        require(
            isinstance(resolved, str) and resolved.startswith("/"),
            "fixture_path_not_absolute",
        )
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
        require(
            isinstance(key, str) and isinstance(value, str),
            "fixture_device_links",
        )
    sysfs = obj["btrfs_sysfs"]
    require(isinstance(sysfs, dict), "fixture_btrfs_sysfs")
    for uuid in sorted(sysfs):
        entry = sysfs[uuid]
        require(isinstance(uuid, str) and uuid, "fixture_btrfs_sysfs")
        require(isinstance(entry, dict), "fixture_btrfs_sysfs")
        devices = entry.get("devices")
        qgroups = entry.get("qgroups")
        mode = entry.get("qgroups_mode")
        require(
            isinstance(devices, list)
            and all(isinstance(item, str) for item in devices),
            "fixture_btrfs_sysfs",
        )
        require(type(qgroups) is bool, "fixture_btrfs_sysfs")
        require(mode is None or isinstance(mode, str), "fixture_btrfs_sysfs")
        sysfs[uuid] = {
            "devices": list(devices),
            "qgroups": qgroups,
            "qgroups_mode": mode,
        }
    return mounts, rows, sysfs, links


def payload(finding, code, rows):
    return {
        "schema": SCHEMA,
        "finding_id": finding,
        "exit_code": code,
        "paths": rows,
        "df_covers_quota": False,
        "limits": list(LIMITS),
    }


def setup_payload(reason):
    return {
        "schema": SCHEMA,
        "finding_id": SETUP,
        "exit_code": RC_SETUP,
        "paths": [],
        "df_covers_quota": False,
        "limits": list(LIMITS),
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
               optional=""):
    """One synthetic mountinfo line (proc.rst section 3.5 field order)."""
    parts = [
        "%d 25 %s / %s rw,relatime" % (mount_id, device, mount_point),
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


def selftest():
    """Isolated synthetic fixture arms. No arm reads host filesystem state."""
    tool = Path(__file__).resolve()
    failures = []
    arms = []
    with tempfile.TemporaryDirectory(prefix="mori-quota-") as tmp:
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
                }
            ],
        )
        arm(
            "xfs-conflicting-options",
            fixture(
                mount_line(36, "259:1", "/srv", "xfs", "/dev/sda1", "rw,noquota,usrquota"),
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
                }
            ],
        )
        arm(
            "ext4-usrquota",
            fixture(
                mount_line(37, "8:1", "/srv", "ext4", "/dev/sdb1", "rw,usrquota,data=ordered"),
                [path_entry("/srv", st_dev="8:1")],
            ),
            RC_ENABLED,
            ENABLED,
            [
                {
                    "path": "/srv",
                    "fstype": "ext4",
                    "mount_point": "/srv",
                    "quota_state": "enabled",
                    "enforcement": "unknown",
                    "basis": "ext_quota_option",
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
                }
            ],
        )
        arm(
            "tmpfs-hardlimit",
            fixture(
                mount_line(39, "0:39", "/run/lane", "tmpfs", "tmpfs", "rw,size_hardlimit=1G"),
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
                }
            ],
        )
        arm(
            "tmpfs-options-absent",
            fixture(
                mount_line(40, "0:40", "/run/lane", "tmpfs", "tmpfs", "rw,size=65536k"),
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
                }
            ],
        )
        btrfs_line = mount_line(
            65, "0:30", "/home", "btrfs", "/dev/mapper/root", "rw,subvol=/@home"
        )
        arm(
            "btrfs-qgroups-present",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:57")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "uuid-one": {
                        "devices": ["dm-0"],
                        "qgroups": True,
                        "qgroups_mode": "quota",
                    }
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
                    "basis": "btrfs_qgroups_dir_present",
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
                    "uuid-one": {
                        "devices": ["dm-0"],
                        "qgroups": False,
                        "qgroups_mode": None,
                    }
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
                    "uuid-one": {
                        "devices": ["dm-9"],
                        "qgroups": True,
                        "qgroups_mode": "quota",
                    }
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
                    "uuid-one": {
                        "devices": ["dm-0"],
                        "qgroups": True,
                        "qgroups_mode": "quota",
                    },
                    "uuid-two": {
                        "devices": ["dm-0"],
                        "qgroups": False,
                        "qgroups_mode": None,
                    },
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
                }
            ],
        )
        arm(
            "btrfs-device-match",
            fixture(
                btrfs_line,
                [path_entry("/home", st_dev="0:30")],
                device_links={"/dev/mapper/root": "dm-0"},
                btrfs_sysfs={
                    "uuid-one": {
                        "devices": ["dm-0"],
                        "qgroups": True,
                        "qgroups_mode": "none",
                    }
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
                    "basis": "btrfs_qgroups_dir_present",
                }
            ],
        )
        arm(
            "unsupported-fstype",
            fixture(
                mount_line(41, "0:41", "/srv", "overlay", "overlay", "rw,lowerdir=/x"),
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
                }
            ],
        )
        arm(
            "no-covering-mount",
            fixture(
                mount_line(42, "259:1", "/srv", "xfs", "/dev/sda1", "rw,usrquota"),
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
                }
            ],
        )
        arm(
            "xfs-device-mismatch",
            fixture(
                mount_line(43, "259:1", "/srv", "xfs", "/dev/sda1", "rw,usrquota"),
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
                }
            ],
        )
        arm(
            "enabled-plus-unknown",
            fixture(
                "\n".join(
                    [
                        mount_line(44, "259:1", "/srv", "xfs", "/dev/sda1", "rw,usrquota"),
                        mount_line(45, "8:1", "/other", "ext4", "/dev/sdb1", "rw"),
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
                mount_line(46, "259:2", "/srv\\040data", "xfs", "/dev/sdc1", "rw,usrquota"),
                [path_entry("/srv data")],
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
                    47,
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
                mount_line(48, "259:4", "/real", "xfs", "/dev/sde1", "rw,usrquota"),
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
                        mount_line(49, "259:5", "/", "xfs", "/dev/sdf1", "rw,noquota"),
                        mount_line(50, "259:6", "/srv/data", "xfs", "/dev/sdg1", "rw,usrquota"),
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
            "last-line-wins-on-tie",
            fixture(
                "\n".join(
                    [
                        mount_line(51, "259:7", "/srv", "xfs", "/dev/sdh1", "rw,usrquota"),
                        mount_line(52, "259:7", "/srv", "xfs", "/dev/sdi1", "rw,noquota"),
                    ]
                ),
                [path_entry("/srv", st_dev="259:7")],
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
                }
            ],
        )
        arm(
            "setup-malformed-st-dev",
            fixture(
                mount_line(53, "259:8", "/srv", "xfs", "/dev/sdj1", "rw,usrquota"),
                [path_entry("/srv", st_dev="not-a-device")],
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-relative-path",
            fixture(
                mount_line(54, "259:9", "/srv", "xfs", "/dev/sdk1", "rw,usrquota"),
                [{"path": "relative/path", "realpath": "relative/path", "st_dev": "259:9"}],
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-extra-top-level-key",
            fixture(
                mount_line(55, "259:10", "/srv", "xfs", "/dev/sdl1", "rw,usrquota"),
                [path_entry("/srv", st_dev="259:10")],
                extra={"unexpected": True},
            ),
            RC_SETUP,
            SETUP,
            None,
        )
        arm(
            "setup-missing-top-level-key",
            fixture(
                mount_line(56, "259:11", "/srv", "xfs", "/dev/sdm1", "rw,usrquota"),
                [path_entry("/srv", st_dev="259:11")],
                drop=["device_links"],
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
                failures.append("%s: schema=%r want=%r" % (label, body.get("schema"), SCHEMA))
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
                    if got.get(key) != want[key]:
                        failures.append(
                            "%s: paths[%d].%s=%r want=%r"
                            % (label, index, key, got.get(key), want[key])
                        )

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
