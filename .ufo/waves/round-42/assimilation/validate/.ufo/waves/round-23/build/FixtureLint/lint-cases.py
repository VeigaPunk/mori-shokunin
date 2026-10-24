#!/usr/bin/env python3
"""lint-cases.py - validate mori round-23 C2 fixture case files.

Authority: ``.ufo/waves/round-23/contract.md`` section C2 (frozen at lane
commit 4dc80c1be48308075e83af17f15fbfe7e95e6cb8), plus the additive token
layer named in ``.ufo/waves/round-23/preseal-amendment.md``.

The linter is a pure file validator.  It reads case JSON files from the
directories named on the command line and checks them against the contract's
case/fixture format:

* case envelope keys (exact), case schema id, scenario/rationale/sources shape;
* fixture keys (exact), fixture schema id, absolute paths, ``MAJ:MIN``
  ``st_dev``, and per-mountinfo-line parseability per proc.rst 3.5;
* expected per-path tokens drawn only from the contract's classification table
  (quota_state, enforcement, basis, fstype/basis pairing);
* expected exit and finding id consistent with the contract's verdict
  precedence given the expected per-path quota states.

Scope note.  The original contract rows are unchanged and remain the primary
rules.  The amendment's superseding rows are admitted ADDITIVELY as their own
basis tokens (see ``AMENDED_BASIS_RULES``) so that a case written under
either authority lints against its own rules instead of being failed by the
other's vocabulary; nothing here redefines an original row.  Where the
amendment adds a fixture member (``qgroups_enabled``) or a device_check token
(``mismatch``, ``not_checked``), the member is required to have the amended
type and pairing, and a record that omits it is noted rather than failed, so
an original-contract case is never failed by an amendment-only rule.

It never executes the C2 probe, never reads host state (``/proc``, ``/sys``,
``os.stat``), never mutates anything, and never reads files outside the
directories named on the command line.

Exit codes:
  0  every case file in every directory is valid
  1  at least one case file is invalid (per-file reasons are printed)
  2  usage error (no directory, unknown option, missing directory)

Usage:
  lint-cases.py [-h] [--json] DIR [DIR ...]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

LINT_SCHEMA = "mori-quota-case-lint-v1"

# ---------------------------------------------------------------------------
# Contract-derived vocabularies (contract section C2).
# ---------------------------------------------------------------------------

CASE_SCHEMA = "mori-quota-case-v1"
FIXTURE_SCHEMA = "mori-quota-fixture-v1"

CASE_KEYS = frozenset(
    {"schema", "id", "scenario", "fixture", "expected", "rationale", "sources"}
)
FIXTURE_KEYS = frozenset({"schema", "mountinfo", "paths", "device_links", "btrfs_sysfs"})
EXPECTED_KEYS = frozenset({"exit", "finding_id", "paths"})
EXPECTED_PATH_REQUIRED = frozenset(
    {"path", "fstype", "mount_point", "quota_state", "enforcement", "basis"}
)
# The contract's per-path output object carries three further fields
# (``device_check``, ``quota_option_keys``, ``btrfs_qgroups_mode``).  A case's
# expected path entry names the six compared fields above; these three are
# accepted as optional extras and shape-checked when present.  They are never
# required and are never compared here.
EXPECTED_PATH_ALLOWED = EXPECTED_PATH_REQUIRED | {
    "device_check",
    "quota_option_keys",
    "btrfs_qgroups_mode",
}
FIXTURE_PATH_KEYS = frozenset({"path", "realpath", "st_dev"})
BTRFS_SYSFS_KEYS = frozenset({"devices", "qgroups", "qgroups_mode"})
# Amendment layer: each btrfs_sysfs UUID record carries a required
# ``qgroups_enabled`` member (true / false / null).  It is additive to the
# original three keys; a record without it is noted, not failed, so original
# proposals still lint under the original contract.
BTRFS_SYSFS_KEYS_AMENDED = BTRFS_SYSFS_KEYS | {"qgroups_enabled"}

FINDING_IDS = frozenset(
    {"QUOTA_SETUP", "QUOTA_ENABLED", "QUOTA_STATE_UNKNOWN", "QUOTA_DISABLED"}
)
QUOTA_STATES = frozenset({"enabled", "disabled", "unknown"})
ENFORCEMENTS = frozenset({"enforced", "accounting_only", "unknown", "n/a"})
# device_check tokens: the original contract names match and
# btrfs_subvolume_skipped; the amendment adds mismatch and not_checked.
DEVICE_CHECKS = frozenset(
    {"match", "mismatch", "btrfs_subvolume_skipped", "not_checked"}
)

KNOWN_FSTYPES = frozenset({"xfs", "btrfs", "ext2", "ext3", "ext4", "tmpfs"})
EXT_FSTYPES = frozenset({"ext2", "ext3", "ext4"})

SETUP_FINDING = "QUOTA_SETUP"

# fstype admission per basis token.
FSTYPE_EXACT = "exact"          # fstype must be one of ``allowed``
FSTYPE_UNCLASSIFIED = "other"   # fstype must be outside KNOWN_FSTYPES
FSTYPE_NON_BTRFS = "non_btrfs"  # fstype must be set and not btrfs
FSTYPE_NULL = "null"            # fstype must be null

# basis -> (quota_states, enforcements, fstype rule, allowed fstypes)
# Transcribed from the contract's classification table (contract C2) plus the
# mount-resolution preamble that defines no_covering_mount and device_mismatch.
BASIS_RULES = {
    "xfs_noquota_option": ({"disabled"}, {"n/a"}, FSTYPE_EXACT, {"xfs"}),
    "xfs_quota_option": (
        {"enabled"},
        {"enforced", "accounting_only"},
        FSTYPE_EXACT,
        {"xfs"},
    ),
    "xfs_conflicting_quota_options": ({"unknown"}, {"n/a"}, FSTYPE_EXACT, {"xfs"}),
    "xfs_quota_options_absent": ({"unknown"}, {"n/a"}, FSTYPE_EXACT, {"xfs"}),
    "btrfs_qgroups_dir_present": ({"enabled"}, {"unknown"}, FSTYPE_EXACT, {"btrfs"}),
    "btrfs_qgroups_dir_absent": ({"disabled"}, {"n/a"}, FSTYPE_EXACT, {"btrfs"}),
    "btrfs_device_unmapped": ({"unknown"}, {"n/a"}, FSTYPE_EXACT, {"btrfs"}),
    "ext_quota_option": ({"enabled"}, {"unknown"}, FSTYPE_EXACT, EXT_FSTYPES),
    "ext_quota_superblock_unobservable": (
        {"unknown"},
        {"n/a"},
        FSTYPE_EXACT,
        EXT_FSTYPES,
    ),
    "tmpfs_quota_option": ({"enabled"}, {"enforced"}, FSTYPE_EXACT, {"tmpfs"}),
    "tmpfs_quota_options_absent": ({"disabled"}, {"n/a"}, FSTYPE_EXACT, {"tmpfs"}),
    "unsupported_fstype": ({"unknown"}, {"n/a"}, FSTYPE_UNCLASSIFIED, None),
    # The mount-resolution preamble (contract C2) fixes quota_state and basis
    # for these two rows but leaves enforcement unstated, so both the table's
    # "n/a" and "unknown" are admitted.
    "no_covering_mount": ({"unknown"}, {"n/a", "unknown"}, FSTYPE_NULL, None),
    "device_mismatch": ({"unknown"}, {"n/a", "unknown"}, FSTYPE_NON_BTRFS, None),
}

# Amendment layer (lane preseal-amendment.md, "C2 final rules superseding only
# erroneous/ambiguous original clauses").  These tokens are ADDITIVE: the
# original contract rows above are unchanged, and each amendment token
# carries its own row so that a case written under either authority lints
# against its own rules instead of being failed by the other's vocabulary.
# Original proposals stay valid under the original rows; amended cases use
# these rows.  Nothing here redefines the original rows.
AMENDED_BASIS_RULES = {
    # ext2/3/4: quota_state is ALWAYS unknown, enforcement n/a.
    "ext_quota_option_unverified": (
        {"unknown"},
        {"n/a"},
        FSTYPE_EXACT,
        EXT_FSTYPES,
    ),
    # btrfs: qgroups directory presence means INITIALIZED, not enabled.
    "btrfs_qgroups_enabled": ({"enabled"}, {"unknown"}, FSTYPE_EXACT, {"btrfs"}),
    "btrfs_qgroups_disabled": ({"disabled"}, {"n/a"}, FSTYPE_EXACT, {"btrfs"}),
    "btrfs_qgroups_enabled_unavailable": (
        {"unknown"},
        {"n/a"},
        FSTYPE_EXACT,
        {"btrfs"},
    ),
    # A covering mountpoint that occurs more than once refuses classification.
    "ambiguous_overmount": ({"unknown"}, {"n/a", "unknown"}, FSTYPE_NULL, None),
}

BASIS_RULES_ALL = dict(BASIS_RULES)
BASIS_RULES_ALL.update(AMENDED_BASIS_RULES)

REAL_CONTROL_SCHEMA = "mori-r23-c2-real-expected-v1"
REAL_CONTROL_KEYS = frozenset(
    {
        "expected_exit",
        "expected_finding_id",
        "expected_paths",
        "schema",
    }
)
REAL_CONTROL_OPTIONAL_KEYS = frozenset(
    {"note", "observed", "observed_utc", "observation_commands"}
)

MAJMIN_RE = re.compile(r"\A\d+:\d+\Z")
SOURCE_ID_RE = re.compile(r"\AS\d{3}\Z")


# ---------------------------------------------------------------------------
# mountinfo parsing (contract C2: "parse mountinfo per proc.rst 3.5").
# ---------------------------------------------------------------------------


# The octal escapes the contract names for a mount point.
MOUNT_POINT_ESCAPES = {"040": " ", "011": "\t", "012": "\n", "134": "\\"}


def decode_mount_point(raw: str) -> str:
    """Decode the octal escapes the contract names: \\040, \\011, \\012, \\134.

    The scan is single pass, left to right, so that an escaped backslash
    (\\134) can never be mistaken for the start of a second escape.
    """
    out = []
    index = 0
    length = len(raw)
    while index < length:
        char = raw[index]
        if char == "\\" and index + 3 < length:
            digits = raw[index + 1 : index + 4]
            if digits in MOUNT_POINT_ESCAPES:
                out.append(MOUNT_POINT_ESCAPES[digits])
                index += 4
                continue
        out.append(char)
        index += 1
    return "".join(out)


def parse_mountinfo_line(line: str):
    """Return a dict for a parseable mountinfo line, else None.

    Fields 1-6 are mandatory, optional fields follow until the '-' separator,
    then fstype, mount source and super options follow the separator.
    """
    parts = line.split()
    if len(parts) < 10:
        return None
    sep = -1
    for index, token in enumerate(parts):
        if token == "-":
            sep = index
            break
    if sep < 6 or len(parts) - sep - 1 != 3:
        return None
    if not MAJMIN_RE.match(parts[2]):
        return None
    raw_mount_point = parts[4]
    mount_point = decode_mount_point(raw_mount_point)
    if not mount_point.startswith("/"):
        return None
    # The amendment names exactly 040, 011, 012 and 134 as the octal escapes
    # and rejects any other backslash escape as a setup verdict.  The linter
    # does not make that a hard failure: it records the observation and lets
    # the case author decide, so an original-contract case is never failed by
    # an amendment-only rule.
    bad_escape = False
    for field in (parts[3], parts[4], parts[sep + 2]):
        index = 0
        while index < len(field):
            if field[index] == "\\":
                digits = field[index + 1 : index + 4]
                if digits not in MOUNT_POINT_ESCAPES:
                    bad_escape = True
                    index += 1
                    continue
                index += 4
                continue
            index += 1
    return {
        "mount_point": mount_point,
        "raw_mount_point": raw_mount_point,
        "fstype": parts[sep + 1],
        "mount_source": parts[sep + 2],
        "super_options": parts[sep + 3],
        "bad_escape": bad_escape,
    }


# ---------------------------------------------------------------------------
# Fixture analysis.
# ---------------------------------------------------------------------------


def analyze_fixture(fixture):
    """Return (causes, notes, info) for one fixture object.

    ``causes`` are the reasons the probe cannot classify the fixture at all.
    The contract enumerates five of them (missing/extra top-level fixture key,
    non-absolute path, malformed st_dev, malformed JSON, unparseable mountinfo
    line); the rest are fields no probe could read.  A cause means the probe
    must answer with a setup verdict, so it constrains the case's expected
    exit and finding id but does not by itself make the case file invalid.

    ``notes`` are observations that do not change either verdict.
    """
    causes = []
    notes = []
    info = {
        "mount_points": set(),
        "fstypes": set(),
    }

    if not isinstance(fixture, dict):
        causes.append("fixture: not a JSON object")
        return causes, notes, info

    keys = set(fixture.keys())
    for missing in sorted(FIXTURE_KEYS - keys):
        causes.append("fixture: missing top-level key %r" % missing)
    for extra in sorted(keys - FIXTURE_KEYS):
        causes.append("fixture: extra top-level key %r" % extra)

    if "schema" in fixture and fixture["schema"] != FIXTURE_SCHEMA:
        causes.append(
            "fixture.schema: %r is not %r" % (fixture["schema"], FIXTURE_SCHEMA)
        )

    if "mountinfo" in fixture:
        mountinfo = fixture["mountinfo"]
        if not isinstance(mountinfo, str):
            causes.append("fixture.mountinfo: not a string")
        else:
            for number, line in enumerate(mountinfo.splitlines(), start=1):
                if not line.strip():
                    continue
                parsed = parse_mountinfo_line(line)
                if parsed is None:
                    causes.append(
                        "fixture.mountinfo line %d: unparseable per proc.rst 3.5" % number
                    )
                else:
                    info["mount_points"].add(parsed["mount_point"])
                    info["mount_points"].add(parsed["raw_mount_point"])
                    info["fstypes"].add(parsed["fstype"])
                    if parsed["bad_escape"]:
                        notes.append(
                            "fixture.mountinfo line %d: a backslash escape other "
                            "than 040, 011, 012 or 134 (the amendment rejects "
                            "these as a setup verdict)" % number
                        )

    if "paths" in fixture:
        paths = fixture["paths"]
        if not isinstance(paths, list):
            causes.append("fixture.paths: not a list")
        else:
            for index, entry in enumerate(paths):
                if not isinstance(entry, dict):
                    causes.append("fixture.paths[%d]: not an object" % index)
                    continue
                entry_keys = set(entry.keys())
                for missing in sorted(FIXTURE_PATH_KEYS - entry_keys):
                    causes.append(
                        "fixture.paths[%d]: missing key %r" % (index, missing)
                    )
                for extra in sorted(entry_keys - FIXTURE_PATH_KEYS):
                    notes.append(
                        "fixture.paths[%d]: extra key %r (the contract's path entry "
                        "names path, realpath, st_dev)" % (index, extra)
                    )
                for field in ("path", "realpath"):
                    if field not in entry:
                        continue
                    value = entry[field]
                    if not isinstance(value, str):
                        causes.append(
                            "fixture.paths[%d].%s: not a string" % (index, field)
                        )
                    elif not value.startswith("/"):
                        causes.append(
                            "fixture.paths[%d].%s: not an absolute path (%r)"
                            % (index, field, value)
                        )
                if "st_dev" in entry:
                    st_dev = entry["st_dev"]
                    if not isinstance(st_dev, str) or not MAJMIN_RE.match(st_dev):
                        causes.append(
                            "fixture.paths[%d].st_dev: not MAJ:MIN (%r)"
                            % (index, st_dev)
                        )

    if "device_links" in fixture:
        device_links = fixture["device_links"]
        if not isinstance(device_links, dict):
            causes.append("fixture.device_links: not an object")
        else:
            for key in sorted(device_links, key=lambda item: str(item)):
                if not isinstance(key, str) or not key.startswith("/"):
                    notes.append(
                        "fixture.device_links: key %r is not an absolute device path"
                        % (key,)
                    )
                value = device_links[key]
                if not isinstance(value, str) or not value:
                    notes.append(
                        "fixture.device_links[%r]: not a non-empty device name" % (key,)
                    )
                elif "/" in value:
                    notes.append(
                        "fixture.device_links[%r]: %r is not a device basename"
                        % (key, value)
                    )

    if "btrfs_sysfs" in fixture:
        sysfs = fixture["btrfs_sysfs"]
        if not isinstance(sysfs, dict):
            causes.append("fixture.btrfs_sysfs: not an object")
        else:
            for uuid in sorted(sysfs, key=lambda item: str(item)):
                entry = sysfs[uuid]
                if not isinstance(entry, dict):
                    causes.append("fixture.btrfs_sysfs[%r]: not an object" % (uuid,))
                    continue
                entry_keys = set(entry.keys())
                for missing in sorted(BTRFS_SYSFS_KEYS - entry_keys):
                    if missing == "qgroups_mode":
                        notes.append(
                            "fixture.btrfs_sysfs[%r]: missing key %r" % (uuid, missing)
                        )
                    else:
                        causes.append(
                            "fixture.btrfs_sysfs[%r]: missing key %r" % (uuid, missing)
                        )
                for extra in sorted(entry_keys - BTRFS_SYSFS_KEYS_AMENDED):
                    notes.append(
                        "fixture.btrfs_sysfs[%r]: extra key %r" % (uuid, extra)
                    )
                if "qgroups_enabled" in entry_keys:
                    enabled = entry["qgroups_enabled"]
                    qgroups = entry.get("qgroups")
                    mode = entry.get("qgroups_mode")
                    if enabled is not None and not isinstance(enabled, bool):
                        causes.append(
                            "fixture.btrfs_sysfs[%r].qgroups_enabled: not true, "
                            "false or null" % (uuid,)
                        )
                    elif qgroups is False:
                        # The amendment: qgroups false (directory absent) must
                        # pair with enabled=null and mode=null.
                        if enabled is not None:
                            causes.append(
                                "fixture.btrfs_sysfs[%r]: qgroups false must pair "
                                "with qgroups_enabled null" % (uuid,)
                            )
                        if mode is not None:
                            causes.append(
                                "fixture.btrfs_sysfs[%r]: qgroups false must pair "
                                "with qgroups_mode null" % (uuid,)
                            )
                    elif enabled is True and qgroups is not True:
                        causes.append(
                            "fixture.btrfs_sysfs[%r]: qgroups_enabled true requires "
                            "qgroups true" % (uuid,)
                        )
                    elif enabled is not True and mode is not None:
                        # enabled=false or null is initialized-but-disabled or
                        # unreadable, so the mode must be null.
                        causes.append(
                            "fixture.btrfs_sysfs[%r]: qgroups_mode must be null "
                            "unless qgroups_enabled is true" % (uuid,)
                        )
                else:
                    notes.append(
                        "fixture.btrfs_sysfs[%r]: no qgroups_enabled member (the "
                        "amendment requires true/false/null; the original contract "
                        "record has no such member)" % (uuid,)
                    )
                devices = entry.get("devices")
                if devices is not None:
                    if not isinstance(devices, list) or not all(
                        isinstance(item, str) for item in devices
                    ):
                        causes.append(
                            "fixture.btrfs_sysfs[%r].devices: not a list of strings"
                            % (uuid,)
                        )
                qgroups = entry.get("qgroups")
                if qgroups is not None and not isinstance(qgroups, bool):
                    causes.append(
                        "fixture.btrfs_sysfs[%r].qgroups: not a boolean" % (uuid,)
                    )
                mode = entry.get("qgroups_mode")
                if mode is not None and not isinstance(mode, str):
                    causes.append(
                        "fixture.btrfs_sysfs[%r].qgroups_mode: not null or a string"
                        % (uuid,)
                    )

    return causes, notes, info


# ---------------------------------------------------------------------------
# Expected-verdict analysis.
# ---------------------------------------------------------------------------


def analyze_expected(expected):
    """Return (reasons, notes, states, states_complete, exit_code, finding_id, entries)."""
    reasons = []
    notes = []
    states = []
    states_complete = True
    exit_code = None
    finding_id = None
    path_entries = []

    if not isinstance(expected, dict):
        return (
            ["expected: not a JSON object"],
            notes,
            states,
            states_complete,
            None,
            None,
            path_entries,
        )

    keys = set(expected.keys())
    for missing in sorted(EXPECTED_KEYS - keys):
        reasons.append("expected: missing key %r" % missing)
    for extra in sorted(keys - EXPECTED_KEYS):
        reasons.append("expected: extra key %r" % extra)

    if "exit" in expected:
        exit_code = expected["exit"]
        if isinstance(exit_code, bool) or not isinstance(exit_code, int):
            reasons.append("expected.exit: not an integer (%r)" % (exit_code,))
            exit_code = None
        elif exit_code not in (0, 1, 2):
            reasons.append("expected.exit: %d is not 0, 1 or 2" % exit_code)

    if "finding_id" in expected:
        finding_id = expected["finding_id"]
        if finding_id not in FINDING_IDS:
            reasons.append(
                "expected.finding_id: %r is not a contract finding id" % (finding_id,)
            )

    if "paths" in expected:
        paths = expected["paths"]
        if not isinstance(paths, list):
            reasons.append("expected.paths: not a list")
        else:
            for index, entry in enumerate(paths):
                if not isinstance(entry, dict):
                    reasons.append("expected.paths[%d]: not an object" % index)
                    states_complete = False
                    continue
                entry_keys = set(entry.keys())
                for missing in sorted(EXPECTED_PATH_REQUIRED - entry_keys):
                    reasons.append(
                        "expected.paths[%d]: missing key %r" % (index, missing)
                    )
                    states_complete = False
                for extra in sorted(entry_keys - EXPECTED_PATH_ALLOWED):
                    reasons.append(
                        "expected.paths[%d]: unexpected key %r" % (index, extra)
                    )
                optional_present = sorted(
                    (entry_keys - EXPECTED_PATH_REQUIRED) & EXPECTED_PATH_ALLOWED
                )
                if optional_present:
                    notes.append(
                        "expected.paths[%d]: optional contract output fields present: %s"
                        % (index, ", ".join(optional_present))
                    )

                # Optional contract output fields, shape-checked when present.
                if "device_check" in entry:
                    device_check = entry["device_check"]
                    if device_check is not None and not isinstance(device_check, str):
                        reasons.append(
                            "expected.paths[%d].device_check: not null or a string"
                            % index
                        )
                    elif isinstance(device_check, str) and device_check not in (
                        DEVICE_CHECKS
                    ):
                        reasons.append(
                            "expected.paths[%d].device_check: %r is not a contract "
                            "device_check token" % (index, device_check)
                        )
                if "quota_option_keys" in entry:
                    option_keys = entry["quota_option_keys"]
                    if not isinstance(option_keys, list) or not all(
                        isinstance(item, str) for item in option_keys
                    ):
                        reasons.append(
                            "expected.paths[%d].quota_option_keys: not a list of strings"
                            % index
                        )
                    elif list(option_keys) != sorted(option_keys):
                        reasons.append(
                            "expected.paths[%d].quota_option_keys: not sorted" % index
                        )
                if "btrfs_qgroups_mode" in entry:
                    mode = entry["btrfs_qgroups_mode"]
                    if mode is not None and not isinstance(mode, str):
                        reasons.append(
                            "expected.paths[%d].btrfs_qgroups_mode: not null or a string"
                            % index
                        )

                path = entry.get("path")
                if "path" in entry:
                    if not isinstance(path, str):
                        reasons.append("expected.paths[%d].path: not a string" % index)
                    elif not path.startswith("/"):
                        reasons.append(
                            "expected.paths[%d].path: not an absolute path (%r)"
                            % (index, path)
                        )

                fstype = entry.get("fstype")
                if "fstype" in entry and fstype is not None:
                    if not isinstance(fstype, str):
                        reasons.append(
                            "expected.paths[%d].fstype: not null or a string" % index
                        )
                        fstype = None

                mount_point = entry.get("mount_point")
                if "mount_point" in entry and mount_point is not None:
                    if not isinstance(mount_point, str):
                        reasons.append(
                            "expected.paths[%d].mount_point: not null or a string" % index
                        )
                        mount_point = None
                    elif not mount_point.startswith("/"):
                        reasons.append(
                            "expected.paths[%d].mount_point: not an absolute path (%r)"
                            % (index, mount_point)
                        )

                quota_state = entry.get("quota_state")
                if "quota_state" in entry:
                    if quota_state not in QUOTA_STATES:
                        reasons.append(
                            "expected.paths[%d].quota_state: %r is not a contract state"
                            % (index, quota_state)
                        )
                        states_complete = False
                    else:
                        states.append(quota_state)
                else:
                    states_complete = False

                enforcement = entry.get("enforcement")
                if "enforcement" in entry and enforcement not in ENFORCEMENTS:
                    reasons.append(
                        "expected.paths[%d].enforcement: %r is not a contract enforcement"
                        % (index, enforcement)
                    )

                basis = entry.get("basis")
                if "basis" in entry:
                    if basis not in BASIS_RULES_ALL:
                        reasons.append(
                            "expected.paths[%d].basis: %r is not a contract basis token"
                            % (index, basis)
                        )
                    else:
                        allowed_states, allowed_enforcements, fstype_rule, allowed = (
                            BASIS_RULES_ALL[basis]
                        )
                        if quota_state is not None and quota_state not in allowed_states:
                            reasons.append(
                                "expected.paths[%d]: basis %r admits quota_state %r, not %r"
                                % (index, basis, sorted(allowed_states), quota_state)
                            )
                        if (
                            enforcement is not None
                            and enforcement not in allowed_enforcements
                        ):
                            reasons.append(
                                "expected.paths[%d]: basis %r admits enforcement %r, not %r"
                                % (index, basis, sorted(allowed_enforcements), enforcement)
                            )
                        if fstype_rule == FSTYPE_NULL:
                            if fstype is not None:
                                reasons.append(
                                    "expected.paths[%d]: basis %r requires fstype null"
                                    % (index, basis)
                                )
                        elif fstype_rule == FSTYPE_EXACT:
                            if fstype is None:
                                reasons.append(
                                    "expected.paths[%d]: basis %r requires a known fstype"
                                    % (index, basis)
                                )
                            elif fstype not in allowed:
                                reasons.append(
                                    "expected.paths[%d]: basis %r does not admit fstype %r"
                                    % (index, basis, fstype)
                                )
                        elif fstype_rule == FSTYPE_UNCLASSIFIED:
                            if fstype is None:
                                reasons.append(
                                    "expected.paths[%d]: basis %r requires an "
                                    "unclassified fstype, not null" % (index, basis)
                                )
                            elif fstype in KNOWN_FSTYPES:
                                reasons.append(
                                    "expected.paths[%d]: basis %r admits only an "
                                    "unclassified fstype, not %r"
                                    % (index, basis, fstype)
                                )
                        elif fstype_rule == FSTYPE_NON_BTRFS:
                            if fstype is None:
                                reasons.append(
                                    "expected.paths[%d]: basis %r requires a chosen "
                                    "fstype" % (index, basis)
                                )
                            elif fstype == "btrfs":
                                reasons.append(
                                    "expected.paths[%d]: basis %r admits a non-btrfs "
                                    "fstype only" % (index, basis)
                                )

                # fstype and mount_point are null together (contract C2 Output).
                if fstype is None and mount_point is not None:
                    reasons.append(
                        "expected.paths[%d]: fstype null requires mount_point null" % index
                    )
                if fstype is not None and mount_point is None:
                    reasons.append(
                        "expected.paths[%d]: mount_point null requires fstype null" % index
                    )

                path_entries.append(entry)

    return reasons, notes, states, states_complete, exit_code, finding_id, path_entries


def verdict_for_states(states):
    """Contract verdict precedence: enabled > unknown > disabled."""
    if "enabled" in states:
        return 1, "QUOTA_ENABLED"
    if "unknown" in states:
        return 2, "QUOTA_STATE_UNKNOWN"
    return 0, "QUOTA_DISABLED"


# ---------------------------------------------------------------------------
# Case-file validation.
# ---------------------------------------------------------------------------


def lint_real_control(document, notes):
    """Validate a frozen real-control document (schema mori-r23-c2-real-expected-v1).

    The real control uses expected_exit / expected_finding_id / expected_paths
    rather than the case envelope's exit / finding_id / paths, so it is checked
    on its own shape instead of being failed as a malformed case file.
    """
    reasons = []
    keys = set(document.keys())
    for missing in sorted(REAL_CONTROL_KEYS - keys):
        reasons.append("real control: missing key %r" % missing)
    for extra in sorted(keys - REAL_CONTROL_KEYS - REAL_CONTROL_OPTIONAL_KEYS):
        reasons.append("real control: extra key %r" % extra)

    exit_code = document.get("expected_exit")
    if not isinstance(exit_code, int) or isinstance(exit_code, bool):
        reasons.append("real control.expected_exit: not an integer")
        exit_code = None
    elif exit_code not in (0, 1, 2):
        reasons.append("real control.expected_exit: %d is not 0, 1 or 2" % exit_code)

    finding_id = document.get("expected_finding_id")
    if finding_id not in FINDING_IDS:
        reasons.append(
            "real control.expected_finding_id: %r is not a contract finding id"
            % (finding_id,)
        )

    states = []
    paths = document.get("expected_paths")
    if not isinstance(paths, list):
        reasons.append("real control.expected_paths: not a list")
    else:
        for index, entry in enumerate(paths):
            if not isinstance(entry, dict):
                reasons.append("real control.expected_paths[%d]: not an object" % index)
                continue
            for field in ("path", "fstype", "mount_point", "quota_state", "enforcement", "basis"):
                if field not in entry:
                    reasons.append(
                        "real control.expected_paths[%d]: missing key %r" % (index, field)
                    )
            quota_state = entry.get("quota_state")
            if quota_state not in QUOTA_STATES:
                reasons.append(
                    "real control.expected_paths[%d].quota_state: %r is not a "
                    "contract state" % (index, quota_state)
                )
            else:
                states.append(quota_state)
            enforcement = entry.get("enforcement")
            if enforcement not in ENFORCEMENTS:
                reasons.append(
                    "real control.expected_paths[%d].enforcement: %r is not a "
                    "contract enforcement" % (index, enforcement)
                )
            basis = entry.get("basis")
            if basis not in BASIS_RULES_ALL:
                reasons.append(
                    "real control.expected_paths[%d].basis: %r is not a contract "
                    "basis token" % (index, basis)
                )
            path = entry.get("path")
            if not isinstance(path, str) or not path.startswith("/"):
                reasons.append(
                    "real control.expected_paths[%d].path: not an absolute path" % index
                )
    if finding_id in FINDING_IDS and states and exit_code is not None:
        want_exit, want_finding = verdict_for_states(states)
        if exit_code != want_exit:
            reasons.append(
                "real control: per-path states %r imply exit %d, found %d"
                % (sorted(set(states)), want_exit, exit_code)
            )
        if finding_id != want_finding:
            reasons.append(
                "real control: per-path states %r imply finding %s, found %r"
                % (sorted(set(states)), want_finding, finding_id)
            )
    return reasons, notes, {"id": None}


def lint_case_file(path):
    """Return (reasons, notes, facts) for one case file."""
    reasons = []
    notes = []
    facts = {"id": None}

    try:
        with open(path, "r", encoding="utf-8") as handle:
            raw = handle.read()
    except OSError as exc:
        return ["file: unreadable (%s)" % exc.__class__.__name__], notes, facts

    try:
        document = json.loads(raw)
    except ValueError as exc:
        return ["file: malformed JSON (%s)" % exc], notes, facts

    if not isinstance(document, dict):
        return ["file: top level is not a JSON object"], notes, facts

    schema = document.get("schema")
    if schema == REAL_CONTROL_SCHEMA:
        return lint_real_control(document, notes)

    keys = set(document.keys())
    for missing in sorted(CASE_KEYS - keys):
        reasons.append("case: missing key %r" % missing)
    for extra in sorted(keys - CASE_KEYS):
        reasons.append("case: extra key %r" % extra)

    if "schema" in document:
        if document["schema"] != CASE_SCHEMA:
            reasons.append(
                "case.schema: %r is not %r" % (document["schema"], CASE_SCHEMA)
            )

    if "id" in document:
        case_id = document["id"]
        if not isinstance(case_id, str) or not case_id.strip():
            reasons.append("case.id: not a non-empty string")
        else:
            facts["id"] = case_id
            stem = os.path.splitext(os.path.basename(path))[0]
            if case_id != stem:
                notes.append(
                    "case.id %r differs from file name stem %r" % (case_id, stem)
                )

    if "scenario" in document:
        scenario = document["scenario"]
        if not isinstance(scenario, str) or not scenario.strip():
            reasons.append("case.scenario: not a non-empty string")
        elif "\n" in scenario:
            reasons.append("case.scenario: not a single line")

    if "rationale" in document:
        rationale = document["rationale"]
        if not isinstance(rationale, str) or not rationale.strip():
            reasons.append("case.rationale: not a non-empty string")

    if "sources" in document:
        sources = document["sources"]
        if not isinstance(sources, list) or not sources:
            reasons.append("case.sources: not a non-empty list")
        else:
            for index, source in enumerate(sources):
                if not isinstance(source, str):
                    reasons.append("case.sources[%d]: not a string" % index)
                elif not SOURCE_ID_RE.match(source):
                    # Citation formatting is advisory: a case is not failed for
                    # how it spells a source anchor.
                    notes.append(
                        "case.sources[%d]: %r is not an S-id of the form S###"
                        % (index, source)
                    )
                elif not ("S077" <= source <= "S084"):
                    notes.append(
                        "case.sources[%d]: %r is outside the contract's S077-S084 range"
                        % (index, source)
                    )

    causes = []
    fixture_info = {
        "mount_points": set(),
        "fstypes": set(),
    }
    if "fixture" in document:
        causes, fixture_notes, fixture_info = analyze_fixture(document["fixture"])
        notes.extend(fixture_notes)

    (
        expected_reasons,
        expected_notes,
        states,
        states_complete,
        exit_code,
        finding_id,
        path_entries,
    ) = analyze_expected(document.get("expected"))
    if "expected" in document:
        reasons.extend(expected_reasons)
        notes.extend(expected_notes)

    finding_known = finding_id in FINDING_IDS

    if finding_known and finding_id == SETUP_FINDING:
        # A setup verdict must be justified by a contract setup cause and must
        # not carry a partial verdict.
        if exit_code is not None and exit_code != 2:
            reasons.append(
                "expected: finding %s requires exit 2, found %r"
                % (SETUP_FINDING, exit_code)
            )
        if isinstance(document.get("expected"), dict):
            paths = document["expected"].get("paths")
            if isinstance(paths, list) and paths:
                notes.append(
                    "expected: finding %s carries no partial verdict, but "
                    "expected.paths is not empty" % SETUP_FINDING
                )
        if not causes:
            reasons.append(
                "expected: finding %s is not backed by a fixture rejection cause; "
                "the fixture is one the probe can classify" % SETUP_FINDING
            )
    elif finding_known and states_complete:
        want_exit, want_finding = verdict_for_states(states)
        if exit_code is not None and exit_code != want_exit:
            reasons.append(
                "expected: per-path states %r imply exit %d, found %r"
                % (sorted(set(states)), want_exit, exit_code)
            )
        if finding_id != want_finding:
            reasons.append(
                "expected: per-path states %r imply finding %s, found %r"
                % (sorted(set(states)), want_finding, finding_id)
            )
        if causes:
            reasons.append(
                "expected: the fixture is not a fixture the probe can classify "
                "(%s), so the case cannot expect a verdict finding" % (causes[0],)
            )

    # Cross-checks between the fixture and the expected per-path results.
    if isinstance(document.get("expected"), dict) and isinstance(
        document.get("fixture"), dict
    ):
        expected_paths = document["expected"].get("paths")
        raw_fixture_paths = document["fixture"].get("paths")
        setup_case = finding_id == SETUP_FINDING
        if isinstance(expected_paths, list) and isinstance(raw_fixture_paths, list):
            if not setup_case and len(expected_paths) != len(raw_fixture_paths):
                reasons.append(
                    "expected.paths: %d entries for %d fixture paths"
                    % (len(expected_paths), len(raw_fixture_paths))
                )
            elif not setup_case:
                fixture_path_values = [
                    entry.get("path")
                    for entry in raw_fixture_paths
                    if isinstance(entry, dict)
                ]
                expected_path_values = [
                    entry.get("path")
                    for entry in expected_paths
                    if isinstance(entry, dict)
                ]
                if sorted(expected_path_values, key=str) != sorted(
                    fixture_path_values, key=str
                ):
                    reasons.append(
                        "expected.paths: %r does not name the same paths as the "
                        "fixture (%r)" % (expected_path_values, fixture_path_values)
                    )
                elif expected_path_values != fixture_path_values:
                    notes.append(
                        "expected.paths: order differs from the fixture path order"
                    )
        for index, entry in enumerate(path_entries):
            if not isinstance(entry, dict):
                continue
            mount_point = entry.get("mount_point")
            if (
                isinstance(mount_point, str)
                and fixture_info["mount_points"]
                and mount_point not in fixture_info["mount_points"]
            ):
                reasons.append(
                    "expected.paths[%d].mount_point %r is not a mount point in "
                    "the fixture mountinfo" % (index, mount_point)
                )
            fstype = entry.get("fstype")
            if (
                isinstance(fstype, str)
                and fixture_info["fstypes"]
                and fstype not in fixture_info["fstypes"]
            ):
                reasons.append(
                    "expected.paths[%d].fstype %r does not occur in the fixture "
                    "mountinfo" % (index, fstype)
                )

    return reasons, notes, facts


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def collect_case_files(directory):
    names = []
    for name in os.listdir(directory):
        if name.endswith(".json") and os.path.isfile(os.path.join(directory, name)):
            names.append(name)
    names.sort()
    return [os.path.join(directory, name) for name in names]


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="lint-cases.py",
        description=(
            "Validate mori round-23 C2 fixture case files against the contract's "
            "case/fixture format."
        ),
    )
    parser.add_argument(
        "directories",
        metavar="DIR",
        nargs="+",
        help="directory holding case files (*.json)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the lint result as one JSON object on stdout",
    )
    args = parser.parse_args(argv)

    for directory in args.directories:
        if not os.path.isdir(directory):
            sys.stderr.write("lint-cases.py: not a directory: %s\n" % directory)
            return 2

    results = []
    seen_ids = {}
    invalid = 0

    for directory in args.directories:
        files = collect_case_files(directory)
        if not files:
            sys.stderr.write(
                "lint-cases.py: warning: no case files (*.json) in %s\n" % directory
            )
        for path in files:
            reasons, notes, facts = lint_case_file(path)
            case_id = facts.get("id")
            if case_id is not None:
                if case_id in seen_ids:
                    reasons.append(
                        "case.id: %r already used by %s" % (case_id, seen_ids[case_id])
                    )
                else:
                    seen_ids[case_id] = path
            if reasons:
                invalid += 1
            results.append(
                {
                    "path": path,
                    "valid": not reasons,
                    "reasons": reasons,
                    "notes": notes,
                }
            )

    total = len(results)
    valid = total - invalid

    if args.json:
        payload = {
            "schema": LINT_SCHEMA,
            "directories": list(args.directories),
            "counts": {"total": total, "valid": valid, "invalid": invalid},
            "files": results,
            "exit_code": 1 if invalid else 0,
        }
        sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    else:
        for record in results:
            if record["valid"]:
                sys.stdout.write("OK   %s\n" % record["path"])
                for note in record["notes"]:
                    sys.stdout.write("     note: %s\n" % note)
            else:
                sys.stdout.write("FAIL %s\n" % record["path"])
                for reason in record["reasons"]:
                    sys.stdout.write("     - %s\n" % reason)
                for note in record["notes"]:
                    sys.stdout.write("     note: %s\n" % note)
        sys.stdout.write(
            "summary: %d case file(s), %d valid, %d invalid\n"
            % (total, valid, invalid)
        )

    return 1 if invalid else 0


if __name__ == "__main__":
    sys.exit(main())
