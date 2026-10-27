#!/usr/bin/env python3
"""Read-only commit-ledger runway read: CommitLimit and Committed_AS, by overcommit mode.

Round 53, claim C2 (coverage axis).  Round 52 admitted what the two /proc/meminfo lines mean
(``corpus/knowledge/overcommit-commit-limit-r52.md``); this tool reads them, with the mode that decides whether
the limit is enforced, and under mode 2 with the error band of the per-CPU counter the kernel's test reads
(``corpus/knowledge/commit-runway-read-r53.md``).  Linux v7.2 sources: mm/util.c (S499), mm/mm_init.c (S511),
lib/percpu_counter.c (S512), include/linux/percpu_counter.h (S513).

Inputs (all read-only; nothing is written outside the selftest's temporary directory):

* ``--meminfo PATH`` (default ``/proc/meminfo``): the lines ``MemTotal``, ``SwapTotal``, ``CommitLimit``,
  ``Committed_AS`` are required, ``Hugetlb`` is optional (0 when absent); each must read ``<digits> kB`` and
  appear once.  Other lines are ignored.
* ``--vm-dir DIR`` (default ``/proc/sys/vm``): ``overcommit_memory``, ``overcommit_ratio``,
  ``overcommit_kbytes``, ``admin_reserve_kbytes``, ``user_reserve_kbytes``, each one non-negative integer.
* ``--cpu-present PATH`` (default ``/sys/devices/system/cpu/present``): a CPU list such as ``0-31`` or
  ``0,2-5``; the count is what ``num_present_cpus()`` sizes the batch with.
* ``--page-kb N`` (default: the system page size in KiB): a power of two.

Reading (``mode`` is ``overcommit_memory``):

* ``limit_recomputed_kb`` = vm_commit_limit(): ``overcommit_kbytes / page`` pages when nonzero, else
  ``(MemTotal - Hugetlb) / page * overcommit_ratio / 100``, plus swap pages, times the page size (integer
  division as in util.c).  ``limit_consistent`` says whether it equals the printed ``CommitLimit``.
* ``headroom_kb`` = CommitLimit - Committed_AS (may be negative; in modes 0 and 1 a negative value is not an
  error, the limit is not enforced there).
* mode 1 (``OVERCOMMIT_ALWAYS``): ``COMMIT_UNLIMITED``, exit 0 — the commit test always passes.
* mode 0 (``OVERCOMMIT_GUESS``): ``COMMIT_HEURISTIC``, exit 0 — only one request larger than RAM + swap is
  refused; ``single_request_cap_kb`` = (ram pages + swap pages) * page.
* mode 2 (``OVERCOMMIT_NEVER``): ``enforced: true``.  ``reserve_kb`` = admin_reserve_kbytes +
  user_reserve_kbytes (the user reserve is the worst case: the kernel holds back min(total_vm/32, reserve) per
  process); ``usable_kb`` = headroom_kb - reserve_kb, the room a large non-root allocation has before the test
  fails.  ``batch_pages`` = max(min(ram_pages / cpus / 256, INT_MAX), max(2 * cpus, 32)) (mm_compute_batch for
  OVERCOMMIT_NEVER) and ``band_kb`` = batch_pages * cpus * page: the test reads the global count without the
  per-CPU deltas, each below one batch.  ``COMMIT_LOW`` (exit 1) when ``usable_kb <= band_kb``: inside the
  counter's own error band an allocation may already be refused.  Otherwise ``COMMIT_OK`` (exit 0).
  ``COMMIT_LOW`` is not a calibrated alert threshold.
* Anything required missing, unreadable or malformed, or a mode outside 0-2: ``COMMIT_UNKNOWN``, exit 2, every
  reading field null, the reason in ``notes``.  A usage error also exits 2.

Output: one JSON object, ``schema: mori-commit-runway-v1``, with the fields above, ``verdict``, ``findings``
(ids: ``over_limit_not_enforced`` when headroom is negative in mode 0/1, ``limit_mismatch`` when the recomputed
limit differs from the printed one, ``inside_band`` with COMMIT_LOW) and ``notes``.

``--selftest`` runs the frozen cases in ``tools/fixtures/mori-commit-runway/cases.json`` (resolved from this
file's directory) in a temporary directory under ``$TMPDIR``, checks that the matcher rejects every corrupted
expectation, and prints ``MORI_COMMIT_RUNWAY_SELFTEST: PASS n/n`` (or ``FAIL`` plus one line per failed case);
exit 0 only when all pass.

Python 3 standard library only; safe under ``python3 -I -B``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple

SCHEMA = "mori-commit-runway-v1"
INT_MAX = 2 ** 31 - 1
MEMINFO_REQUIRED = ("MemTotal", "SwapTotal", "CommitLimit", "Committed_AS")
MEMINFO_OPTIONAL = ("Hugetlb",)
VM_FILES = ("overcommit_memory", "overcommit_ratio", "overcommit_kbytes", "admin_reserve_kbytes",
            "user_reserve_kbytes")
READING_FIELDS = ("mode", "enforced", "commit_limit_kb", "committed_as_kb", "headroom_kb", "reserve_kb",
                  "usable_kb", "band_kb", "batch_pages", "cpus_present", "single_request_cap_kb",
                  "limit_recomputed_kb", "limit_consistent")
EXIT = {"COMMIT_OK": 0, "COMMIT_HEURISTIC": 0, "COMMIT_UNLIMITED": 0, "COMMIT_LOW": 1, "COMMIT_UNKNOWN": 2}
LINE_RE = re.compile(r"^([A-Za-z0-9_()]+):\s*(.*?)\s*$")
KB_RE = re.compile(r"^(\d+) kB$")
CPULIST_RE = re.compile(r"^\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*$")


class InputError(Exception):
    """A required input is missing, unreadable or malformed."""


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="ascii") as f:
            return f.read()
    except FileNotFoundError:
        raise InputError("%s: absent" % path)
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError("%s: unreadable (%s)" % (path, getattr(exc, "strerror", None) or type(exc).__name__))


def parse_meminfo(text: str) -> Dict[str, int]:
    wanted = MEMINFO_REQUIRED + MEMINFO_OPTIONAL
    vals: Dict[str, int] = {}
    for line in text.splitlines():
        m = LINE_RE.match(line)
        if not m or m.group(1) not in wanted:
            continue
        key = m.group(1)
        if key in vals:
            raise InputError("meminfo: %s appears twice" % key)
        kb = KB_RE.match(m.group(2))
        if not kb:
            raise InputError("meminfo: %s is not '<digits> kB'" % key)
        vals[key] = int(kb.group(1))
    missing = [k for k in MEMINFO_REQUIRED if k not in vals]
    if missing:
        raise InputError("meminfo: missing %s" % ",".join(missing))
    vals.setdefault("Hugetlb", 0)
    return vals


def parse_cpulist(text: str) -> int:
    t = text.strip()
    if not CPULIST_RE.match(t):
        raise InputError("cpu present list malformed: %r" % t[:40])
    count = 0
    for part in t.split(","):
        lo, _, hi = part.partition("-")
        a, b = int(lo), int(hi) if hi else int(lo)
        if b < a:
            raise InputError("cpu present range reversed: %s" % part)
        count += b - a + 1
    return count


def parse_vm_value(name: str, text: str) -> int:
    t = text.strip()
    if not re.fullmatch(r"\d+", t):
        raise InputError("vm/%s is not a non-negative integer" % name)
    return int(t)


def unknown(notes: List[str]) -> Tuple[Dict[str, Any], int]:
    out: Dict[str, Any] = {"schema": SCHEMA, "verdict": "COMMIT_UNKNOWN"}
    out.update({k: None for k in READING_FIELDS})
    out["findings"] = []
    out["notes"] = notes
    return out, 2


def evaluate(meminfo_path: str, vm_dir: str, present_path: str, page_kb: int) -> Tuple[Dict[str, Any], int]:
    try:
        mi = parse_meminfo(_read(meminfo_path))
        vm = {name: parse_vm_value(name, _read(os.path.join(vm_dir, name))) for name in VM_FILES}
        cpus = parse_cpulist(_read(present_path))
    except InputError as exc:
        return unknown([str(exc)])
    mode = vm["overcommit_memory"]
    if mode not in (0, 1, 2):
        return unknown(["vm/overcommit_memory=%d is not a known policy (0, 1, 2)" % mode])
    ram_pages = mi["MemTotal"] // page_kb
    swap_pages = mi["SwapTotal"] // page_kb
    huge_pages = mi["Hugetlb"] // page_kb
    if vm["overcommit_kbytes"]:
        allowed = vm["overcommit_kbytes"] // page_kb
    else:
        allowed = (ram_pages - huge_pages) * vm["overcommit_ratio"] // 100
    allowed += swap_pages
    out: Dict[str, Any] = {"schema": SCHEMA}
    out.update({k: None for k in READING_FIELDS})
    out.update(mode=mode, enforced=(mode == 2), commit_limit_kb=mi["CommitLimit"],
               committed_as_kb=mi["Committed_AS"], headroom_kb=mi["CommitLimit"] - mi["Committed_AS"],
               cpus_present=cpus, limit_recomputed_kb=allowed * page_kb,
               limit_consistent=(allowed * page_kb == mi["CommitLimit"]))
    findings: List[Dict[str, Any]] = []
    notes: List[str] = []
    if not out["limit_consistent"]:
        findings.append({"id": "limit_mismatch", "printed_kb": mi["CommitLimit"],
                         "recomputed_kb": out["limit_recomputed_kb"]})
    if mode == 1:
        out["verdict"] = "COMMIT_UNLIMITED"
        notes.append("mode 1 (always): the commit test always passes; CommitLimit is printed, not enforced")
    elif mode == 0:
        out["verdict"] = "COMMIT_HEURISTIC"
        out["single_request_cap_kb"] = (ram_pages + swap_pages) * page_kb
        notes.append("mode 0 (guess): only a single request above RAM + swap is refused; CommitLimit is printed, "
                     "not enforced")
    else:
        batch = max(min(ram_pages // cpus // 256, INT_MAX), max(2 * cpus, 32))
        out["batch_pages"] = batch
        out["band_kb"] = batch * cpus * page_kb
        out["reserve_kb"] = vm["admin_reserve_kbytes"] + vm["user_reserve_kbytes"]
        out["usable_kb"] = out["headroom_kb"] - out["reserve_kb"]
        if out["usable_kb"] <= out["band_kb"]:
            out["verdict"] = "COMMIT_LOW"
            findings.append({"id": "inside_band", "usable_kb": out["usable_kb"], "band_kb": out["band_kb"]})
        else:
            out["verdict"] = "COMMIT_OK"
        notes.append("mode 2 (never): enforced; usable_kb counts the full user reserve (worst case) and band_kb "
                     "is the per-CPU approximation bound, not a measured deviation")
    if mode in (0, 1) and out["headroom_kb"] < 0:
        findings.append({"id": "over_limit_not_enforced", "headroom_kb": out["headroom_kb"]})
    out["findings"] = findings
    out["notes"] = notes
    return out, EXIT[out["verdict"]]


# ---------------------------------------------------------------------------------------------- selftest
def _cases_path() -> str:
    here = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(here, "fixtures", "mori-commit-runway", "cases.json")


def _materialise(case: Dict[str, Any], root: str) -> Tuple[str, str, str]:
    d = os.path.join(root, case["id"])
    os.makedirs(os.path.join(d, "vm"))
    mi = os.path.join(d, "meminfo")
    if case.get("meminfo") is not None:
        with open(mi, "w", encoding="ascii") as f:
            f.write(case["meminfo"])
    for name, value in (case.get("vm") or {}).items():
        if value is not None:
            with open(os.path.join(d, "vm", name), "w", encoding="ascii") as f:
                f.write(value)
    present = os.path.join(d, "present")
    if case.get("present") is not None:
        with open(present, "w", encoding="ascii") as f:
            f.write(case["present"])
    return mi, os.path.join(d, "vm"), present


def _mismatches(case: Dict[str, Any], out: Dict[str, Any], code: int) -> List[str]:
    bad = []
    if code != case["expect_exit"]:
        bad.append("exit %s != %s" % (code, case["expect_exit"]))
    for key, want in case["expect"].items():
        got = out.get(key, "<missing>")
        if got != want or type(got) is not type(want):
            bad.append("%s %r != %r" % (key, got, want))
    want_ids = case.get("expect_findings")
    if want_ids is not None and sorted(f["id"] for f in out.get("findings", [])) != sorted(want_ids):
        bad.append("findings %r != %r" % (sorted(f["id"] for f in out.get("findings", [])), sorted(want_ids)))
    return bad


def _corrupt(case: Dict[str, Any]) -> Dict[str, Any]:
    c = json.loads(json.dumps(case))
    exp = c["expect"]
    exp["verdict"] = "COMMIT_OK" if exp.get("verdict") != "COMMIT_OK" else "COMMIT_LOW"
    return c


def selftest(cases_file: Optional[str] = None) -> int:
    path = cases_file or _cases_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            cases = json.load(f)["cases"]
    except (OSError, ValueError, KeyError) as exc:
        print("MORI_COMMIT_RUNWAY_SELFTEST: FAIL cannot load cases (%s)" % exc)
        return 1
    root = tempfile.mkdtemp(prefix="mori-commit-runway-")
    failed: List[str] = []
    rejected = 0
    try:
        for case in cases:
            mi, vmd, present = _materialise(case, root)
            out, code = evaluate(mi, vmd, present, case.get("page_kb", 4))
            bad = _mismatches(case, out, code)
            if bad:
                failed.append("%s: %s" % (case["id"], "; ".join(bad)))
            if _mismatches(_corrupt(case), out, code):
                rejected += 1
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print("MATCHER: rejected %d/%d corrupted expectations" % (rejected, len(cases)))
    if rejected != len(cases):
        failed.append("matcher accepted a corrupted expectation")
    for line in failed:
        print("FAIL " + line)
    total = len(cases)
    if failed:
        print("MORI_COMMIT_RUNWAY_SELFTEST: FAIL %d/%d" % (total - len([f for f in failed if ":" in f]), total))
        return 1
    print("MORI_COMMIT_RUNWAY_SELFTEST: PASS %d/%d" % (total, total))
    return 0


# ---------------------------------------------------------------------------------------------- cli
class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:  # noqa: D102
        print(json.dumps({"schema": SCHEMA, "verdict": "COMMIT_UNKNOWN", "notes": ["usage: " + message]}))
        sys.exit(2)


def _page_kb_default() -> int:
    try:
        return max(1, os.sysconf("SC_PAGE_SIZE") // 1024)
    except (ValueError, OSError, AttributeError):
        return 4


def main(argv: Optional[List[str]] = None) -> int:
    p = _Parser(prog="mori-commit-runway.py", description="Read-only commit-ledger runway read.")
    p.add_argument("--meminfo", default="/proc/meminfo")
    p.add_argument("--vm-dir", default="/proc/sys/vm")
    p.add_argument("--cpu-present", default="/sys/devices/system/cpu/present")
    p.add_argument("--page-kb", type=int, default=None)
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--cases", default=None, help="selftest cases file (default: the committed fixtures)")
    a = p.parse_args(argv)
    if a.selftest:
        return selftest(a.cases)
    page_kb = a.page_kb if a.page_kb is not None else _page_kb_default()
    if page_kb < 1 or page_kb & (page_kb - 1):
        out, code = unknown(["--page-kb must be a power of two (got %d)" % page_kb])
    else:
        out, code = evaluate(a.meminfo, a.vm_dir, a.cpu_present, page_kb)
    print(json.dumps(out, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
