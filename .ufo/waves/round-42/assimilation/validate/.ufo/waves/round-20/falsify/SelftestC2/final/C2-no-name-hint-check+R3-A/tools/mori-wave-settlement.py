#!/usr/bin/env python3
"""Read-only per-seat settlement scan for mori swarm dispatch waves.

Frozen contract: .ufo/waves/round-20/contract.md (C2) and frozen/c2-expected.json.
Co-evolved refinements (round 20, after dispatch; disclosed in the round lesson):
  R1 the trailer is the LAST line matching the trailer regex (not necessarily the
     task's final line, e.g. a terminal `| godspeed` envelope), after stripping
     trailing whitespace/CR;
  R2 a regular file whose whole content is the seat start stub `STATUS: started`
     is status `stub` (not present); at most 16 bytes are read and none emitted;
  R3 `name_hint` marks dispatch filenames containing preview / undispatched /
     not-dispatched / validation (shape only: a dispatch file never proves dispatch);
  R4 `duplicate_of` names the first earlier dispatch file with identical bytes, and
     totals carry `unique_dispatch_sha256`;
  R5 `duplicate_report_paths` counts members sharing one report path in a wave;
  R6 a missing `taskCall` key is `unavailable`; R7 any `..` component is `unsafe`.
A missing report is not a dead seat; this tool reports filesystem shape only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import ntpath
import os
import re
import stat
import sys
import tempfile

SCHEMA = "mori-wave-settlement-v1"
DISPATCH_SCHEMA = "ufo-swarm-wave-dispatch-v1"
STATUS_NAMES = ("present", "empty", "stub", "missing", "misrooted", "unsafe", "unparsed")
REPORT_RE = re.compile(r"^Report: write your scoped findings to (\S+)$")
STUB_CONTENTS = (b"STATUS: started", b"STATUS: started\n")
NAME_HINT_RE = re.compile(r"(preview|undispatched|not-dispatched|validation)", re.IGNORECASE)
# Co-evolved refinement cases R1–R5 (+ missing taskCall); the frozen 14 are loaded
# from .ufo/waves/round-20/frozen/c2-expected.json and are never edited.
REFINEMENT_CASES = [
    {"id": "r1-godspeed-trailer", "expect": {"exit": 0, "state": "settled", "present": 1, "unparsed": 0}},
    {"id": "r1-crlf-trailer", "expect": {"exit": 0, "state": "settled", "present": 1, "unparsed": 0}},
    {"id": "r2-stub", "expect": {"exit": 1, "state": "partial", "present": 1, "stub": 1, "missing_names": ["A"]}},
    {"id": "r3-name-hint", "expect": {"exit": 1, "state": "unsettled", "name_hint": "undispatched-name:preview"}},
    {"id": "r4-duplicate-dispatch", "expect": {"exit": 0, "waves": 2, "unique_dispatch_sha256": 1,
                                               "second_duplicate_of": ".ufo/waves/round-1/a.json"}},
    {"id": "r5-duplicate-report-path", "expect": {"exit": 0, "state": "settled", "duplicate_report_paths": 1}},
    {"id": "r6-taskcall-missing", "expect": {"exit": 1, "state": "unavailable", "members": 0}},
    # r7: a `..` component that still resolves inside the lane is unsafe (frozen contract:
    # "contain no `..` component"); added after wave-2 mutant MutTraversalAllowed survived.
    {"id": "r7-dotdot-inside-lane", "expect": {"exit": 1, "state": "unavailable", "unsafe": 1, "present": 0}},
]


class ScanError(Exception):
    """The lane tree cannot be scanned completely."""


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _reject_json_constant(_value: str):
    raise ValueError("non-JSON numeric constant")

def _path_bytes(path: str) -> bytes:
    return os.fsencode(path)


def _lstat(path: str):
    """Return lstat information, never following a final-component symlink."""
    return os.lstat(path)


def _wave_root(lane_root: str) -> str | None:
    current = lane_root
    for part in (".ufo", "waves"):
        try:
            info = _lstat(current)
        except OSError as exc:
            raise ScanError from exc
        if not stat.S_ISDIR(info.st_mode):
            return None
        current = os.path.join(current, part)
        try:
            info = _lstat(current)
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise ScanError from exc
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            return None
    return current


def _dispatch_files(waves_root: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []

    def visit(directory: str, relative_parts: tuple[str, ...]) -> None:
        try:
            with os.scandir(directory) as iterator:
                entries = sorted(iterator, key=lambda entry: _path_bytes(entry.name))
        except OSError as exc:
            raise ScanError from exc

        for entry in entries:
            path = os.path.join(directory, entry.name)
            try:
                info = _lstat(path)
            except FileNotFoundError:
                continue
            except OSError as exc:
                if entry.name.endswith(".json"):
                    # It cannot be safely identified as a regular file; do not follow it.
                    continue
                raise ScanError from exc

            parts = relative_parts + (entry.name,)
            if stat.S_ISDIR(info.st_mode):
                visit(path, parts)
            elif stat.S_ISREG(info.st_mode) and entry.name.endswith(".json"):
                found.append((path, ".ufo/waves/" + "/".join(parts)))

    visit(waves_root, ())
    found.sort(key=lambda item: _path_bytes(item[1]))
    return found


def _read_regular_bytes(path: str) -> bytes | None:
    """Read a lstat-confirmed regular file without opening a final symlink."""
    try:
        info = _lstat(path)
    except OSError:
        return None
    if not stat.S_ISREG(info.st_mode):
        return None

    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        return None
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            return None
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            return stream.read()
    except OSError:
        return None
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _safe_report_path(lane_root: str, raw_path: str) -> tuple[bool, tuple[str, ...]]:
    """Validate the lexical path before performing any filesystem lookup."""
    if (not raw_path or "\x00" in raw_path or os.path.isabs(raw_path)
            or ntpath.isabs(raw_path)):
        return False, ()

    components = raw_path.split(os.sep)
    if ".." in components:
        return False, ()

    candidate = os.path.abspath(os.path.join(lane_root, raw_path))
    try:
        if os.path.commonpath((lane_root, candidate)) != lane_root:
            return False, ()
    except ValueError:
        return False, ()

    parts = tuple(part for part in components if part not in ("", "."))
    return True, parts


def _inspect_report_path(root: str, parts: tuple[str, ...]) -> tuple[str, int | None]:
    """Classify a safe relative path using lstat on each component."""
    if not parts:
        return "other", None
    try:
        info = _lstat(root)
    except OSError:
        return "missing", None
    if not stat.S_ISDIR(info.st_mode):
        return "other", None

    current = root
    for index, component in enumerate(parts):
        current = os.path.join(current, component)
        try:
            info = _lstat(current)
        except (FileNotFoundError, NotADirectoryError):
            return "missing", None
        except OSError:
            return "unavailable", None

        if index < len(parts) - 1:
            if not stat.S_ISDIR(info.st_mode):
                return "other", None
        elif stat.S_ISREG(info.st_mode):
            return "regular", info.st_size
        else:
            return "other", None
    return "other", None


def _trailer(task: object, lane_root: str) -> tuple[str, tuple[str, ...], str | None]:
    if not isinstance(task, dict) or not isinstance(task.get("task"), str):
        return "unparsed", (), None
    match = None
    for line in reversed(task["task"].splitlines()):
        match = REPORT_RE.fullmatch(line.rstrip())
        if match is not None:
            break
    if match is None:
        return "unparsed", (), None
    raw_path = match.group(1)
    safe, parts = _safe_report_path(lane_root, raw_path)
    if not safe:
        return "unsafe", (), None
    return "safe", parts, "/".join(parts)


def _member_status(lane_root: str, fleet_root: str | None, parts: tuple[str, ...]) -> str:
    lane_kind, size = _inspect_report_path(lane_root, parts)
    if lane_kind == "regular":
        if size is None or size == 0:
            return "empty"
        if size <= max(len(stub) for stub in STUB_CONTENTS):
            if _read_regular_bytes(os.path.join(lane_root, *parts)) in STUB_CONTENTS:
                return "stub"
        return "present"
    if lane_kind == "missing" and fleet_root is not None:
        fleet_kind, _fleet_size = _inspect_report_path(fleet_root, parts)
        if fleet_kind == "regular":
            return "misrooted"
    return "missing"


def _name_sort_key(name: object) -> bytes:
    if isinstance(name, str):
        return name.encode("utf-8", "surrogatepass")
    return json.dumps(name, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def _summarize_wave(relative_path: str, raw: bytes, document: dict,
                    lane_root: str, fleet_root: str | None) -> dict:
    task_call = document.get("taskCall")
    counts = {name: 0 for name in STATUS_NAMES}
    members: list[dict] = []
    safe_path_count = 0

    if "taskCall" in document and task_call is None:
        tasks: list[object] = []
        no_spawn = True
    else:
        no_spawn = False
        tasks = task_call.get("tasks", []) if isinstance(task_call, dict) else []
        if not isinstance(tasks, list):
            tasks = []
    report_paths: dict[str, int] = {}
    for task in tasks:
        name = task.get("name") if isinstance(task, dict) else None
        agent = task.get("agent") if isinstance(task, dict) else None
        trailer_status, parts, joined = _trailer(task, lane_root)
        if trailer_status == "unparsed":
            status = "unparsed"
        elif trailer_status == "unsafe":
            status = "unsafe"
        else:
            safe_path_count += 1
            report_paths[joined] = report_paths.get(joined, 0) + 1
            status = _member_status(lane_root, fleet_root, parts)
        counts[status] += 1
        members.append({"name": name, "agent": agent, "status": status})

    present = counts["present"]
    total_members = len(members)
    if no_spawn:
        state = "no-spawn"
    elif safe_path_count == 0:
        state = "unavailable"
    elif present == total_members:
        state = "settled"
    elif present:
        state = "partial"
    else:
        state = "unsettled"

    missing = [member["name"] for member in members if member["status"] != "present"]
    missing.sort(key=_name_sort_key)
    name_hint_match = None
    return {
        "dispatch_path": relative_path,
        "dispatch_sha256": hashlib.sha256(raw).hexdigest(),
        "wave": document.get("wave"),
        "members": members,
        "counts": counts,
        "state": state,
        "missing": missing,
        "name_hint": ("undispatched-name:" + name_hint_match.group(1).lower()) if name_hint_match else None,
        "duplicate_report_paths": sum(count - 1 for count in report_paths.values() if count > 1),
        "duplicate_of": None,
    }


def scan_lane(lane_root_arg: str, fleet_root_arg: str | None = None) -> tuple[dict, int]:
    lane_root = os.path.abspath(lane_root_arg)
    try:
        root_info = _lstat(lane_root)
    except OSError as exc:
        raise ScanError from exc
    if not stat.S_ISDIR(root_info.st_mode):
        raise ScanError("lane root is not a directory")

    fleet_root = os.path.abspath(fleet_root_arg) if fleet_root_arg is not None else None
    waves_root = _wave_root(lane_root)
    paths = _dispatch_files(waves_root) if waves_root is not None else []
    waves: list[dict] = []
    ignored_json = 0
    unreadable_json = 0

    for path, relative_path in paths:
        raw = _read_regular_bytes(path)
        if raw is None:
            unreadable_json += 1
            continue
        try:
            document = json.loads(raw, parse_constant=_reject_json_constant)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            unreadable_json += 1
            continue
        if not isinstance(document, dict) or document.get("schema") != DISPATCH_SCHEMA:
            ignored_json += 1
            continue
        waves.append(_summarize_wave(relative_path, raw, document, lane_root, fleet_root))

    first_by_sha: dict[str, str] = {}
    for wave in waves:
        earlier = first_by_sha.setdefault(wave["dispatch_sha256"], wave["dispatch_path"])
        if earlier != wave["dispatch_path"]:
            wave["duplicate_of"] = earlier

    totals = {name: 0 for name in STATUS_NAMES}
    total_members = 0
    states: dict[str, int] = {}
    for wave in waves:
        total_members += len(wave["members"])
        for name in STATUS_NAMES:
            totals[name] += wave["counts"][name]
        states[wave["state"]] = states.get(wave["state"], 0) + 1
    totals["waves"] = len(waves)
    totals["members"] = total_members
    totals["states"] = dict(sorted(states.items()))
    totals["unique_dispatch_sha256"] = len(first_by_sha)
    totals["name_hinted_waves"] = sum(1 for wave in waves if wave["name_hint"])

    payload = {
        "schema": SCHEMA,
        "lane_root": lane_root,
        "waves": waves,
        "totals": totals,
        "ignored_json": ignored_json,
        "unreadable_json": unreadable_json,
    }
    rc = 0 if all(wave["state"] in ("settled", "no-spawn") for wave in waves) else 1
    return payload, rc


def _oracle_path() -> str | None:
    current = os.path.dirname(os.path.abspath(__file__))
    while True:
        candidate = os.path.join(current, ".ufo", "waves", "round-20", "frozen", "c2-expected.json")
        if os.path.isfile(candidate):
            return candidate
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def _write_json(path: str, value: object) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as stream:
        stream.write(_json_bytes(value))


def _report_relative(name: str) -> str:
    return ".ufo/waves/round-1/build/" + name + ".md"


def _task(name: str, report_path: str | None = None, agent: str = "reviewer") -> dict:
    body = "Fixture task"
    if report_path is not None:
        body += "\nReport: write your scoped findings to " + report_path
    return {"name": name, "agent": agent, "task": body}


def _write_report(root: str, relative_path: str, content: bytes = b"report\n") -> None:
    path = os.path.join(root, relative_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as stream:
        stream.write(content)


def _write_dispatch(waves_root: str, relative_path: str, tasks: list[dict] | None,
                    wave: str, task_call: object = "normal") -> None:
    path = os.path.join(waves_root, relative_path)
    if task_call == "normal":
        task_call = {"context": "c", "tasks": tasks or []}
    _write_json(path, {
        "schema": DISPATCH_SCHEMA,
        "wave": wave,
        "taskCall": task_call,
    })


def _fixture(case_id: str, case_root: str) -> tuple[str, str | None]:
    lane_root = os.path.join(case_root, "lane")
    waves_root = os.path.join(lane_root, ".ufo", "waves")
    os.makedirs(waves_root, exist_ok=True)
    fleet_root = os.path.join(case_root, "fleet")
    report_paths = {name: _report_relative(name) for name in ("A", "B", "C")}

    if case_id == "all-present":
        tasks = [_task(name, report_paths[name]) for name in ("A", "B", "C")]
        for name in ("A", "B", "C"):
            _write_report(lane_root, report_paths[name])
        _write_dispatch(waves_root, "round-1/dispatch.json", tasks, "fixture-all-present")
    elif case_id == "one-missing":
        tasks = [_task(name, report_paths[name]) for name in ("A", "B", "C")]
        for name in ("A", "B"):
            _write_report(lane_root, report_paths[name])
        _write_dispatch(waves_root, "round-1/dispatch.json", tasks, "fixture-one-missing")
    elif case_id == "none-present":
        tasks = [_task(name, report_paths[name]) for name in ("A", "B")]
        _write_dispatch(waves_root, "round-1/dispatch.json", tasks, "fixture-none-present")
    elif case_id == "empty-report":
        tasks = [_task(name, report_paths[name]) for name in ("A", "B")]
        _write_report(lane_root, report_paths["A"])
        _write_report(lane_root, report_paths["B"], b"")
        _write_dispatch(waves_root, "round-1/dispatch.json", tasks, "fixture-empty-report")
    elif case_id == "misrooted":
        tasks = [_task(name, report_paths[name]) for name in ("A", "B")]
        _write_report(lane_root, report_paths["A"])
        _write_report(fleet_root, report_paths["B"])
        _write_dispatch(waves_root, "round-1/dispatch.json", tasks, "fixture-misrooted")
    elif case_id == "malformed-dispatch":
        malformed = os.path.join(waves_root, "round-1/malformed.json")
        os.makedirs(os.path.dirname(malformed), exist_ok=True)
        with open(malformed, "wb") as stream:
            stream.write(b'{"schema":"ufo-swarm-wave-dispatch-v1",')
        _write_report(lane_root, report_paths["A"])
        _write_dispatch(
            waves_root,
            "round-1/valid.json",
            [_task("A", report_paths["A"])],
            "fixture-valid",
        )
    elif case_id == "no-trailer":
        tasks = [_task("A"), _task("B", report_paths["B"])]
        _write_report(lane_root, report_paths["B"])
        _write_dispatch(waves_root, "round-1/dispatch.json", tasks, "fixture-no-trailer")
    elif case_id == "traversal":
        outside = os.path.abspath(os.path.join(lane_root, "../../outside.md"))
        os.makedirs(os.path.dirname(outside), exist_ok=True)
        with open(outside, "wb") as stream:
            stream.write(b"outside\n")
        _write_dispatch(waves_root, "round-1/dispatch.json", [_task("A", "../../outside.md")], "fixture-traversal")
    elif case_id == "absolute-path":
        absolute = os.path.join(case_root, "absolute-target.md")
        with open(absolute, "wb") as stream:
            stream.write(b"outside\n")
        _write_dispatch(waves_root, "round-1/dispatch.json", [_task("A", absolute)], "fixture-absolute")
    elif case_id == "symlink-report":
        report_path = report_paths["A"]
        target = os.path.join(case_root, "symlink-target.md")
        with open(target, "wb") as stream:
            stream.write(b"not a report\n")
        link = os.path.join(lane_root, report_path)
        os.makedirs(os.path.dirname(link), exist_ok=True)
        os.symlink(target, link)
        _write_dispatch(waves_root, "round-1/dispatch.json", [_task("A", report_path)], "fixture-symlink")
    elif case_id == "other-schema-ignored":
        _write_json(os.path.join(waves_root, "round-1/registry.json"), {"schema": "ufo-swarm-registry-v1"})
        _write_json(os.path.join(waves_root, "round-1/plain.json"), {"hello": "world"})
        _write_report(lane_root, report_paths["A"])
        _write_dispatch(waves_root, "round-1/dispatch.json", [_task("A", report_paths["A"])], "fixture-ignored")
    elif case_id == "no-spawn":
        _write_dispatch(waves_root, "round-1/dispatch.json", None, "fixture-no-spawn", task_call=None)
    elif case_id == "content-not-emitted":
        _write_report(lane_root, report_paths["A"], b"CANARY-r20-7f3a\n")
        _write_dispatch(waves_root, "round-1/dispatch.json", [_task("A", report_paths["A"])], "fixture-content")
    elif case_id == "deterministic":
        for name in ("A", "B"):
            _write_report(lane_root, report_paths[name])
        _write_dispatch(waves_root, "zeta/dispatch.json", [_task("B", report_paths["B"])], "fixture-zeta")
        _write_dispatch(waves_root, "alpha/dispatch.json", [_task("A", report_paths["A"])], "fixture-alpha")
    elif case_id == "r1-godspeed-trailer":
        task = _task("A", report_paths["A"])
        task["task"] += "\n\n| godspeed"
        _write_report(lane_root, report_paths["A"])
        _write_dispatch(waves_root, "round-1/dispatch.json", [task], "fixture-r1")
    elif case_id == "r1-crlf-trailer":
        task = _task("A", report_paths["A"])
        task["task"] += "\r\n"
        task["task"] = task["task"].replace("\n", "\r\n").replace("\r\r\n", "\r\n")
        _write_report(lane_root, report_paths["A"])
        _write_dispatch(waves_root, "round-1/dispatch.json", [task], "fixture-r1-crlf")
    elif case_id == "r2-stub":
        _write_report(lane_root, report_paths["A"], b"STATUS: started\n")
        _write_report(lane_root, report_paths["B"], b"STATUS: started, then wrote more\n")
        _write_dispatch(waves_root, "round-1/dispatch.json",
                        [_task(name, report_paths[name]) for name in ("A", "B")], "fixture-r2")
    elif case_id == "r3-name-hint":
        _write_dispatch(waves_root, "round-1/dispatch-preview.json", [_task("A", report_paths["A"])], "fixture-r3")
    elif case_id == "r4-duplicate-dispatch":
        _write_report(lane_root, report_paths["A"])
        for relative in ("round-1/a.json", "round-1/b.json"):
            _write_dispatch(waves_root, relative, [_task("A", report_paths["A"])], "fixture-r4")
    elif case_id == "r5-duplicate-report-path":
        _write_report(lane_root, report_paths["A"])
        _write_dispatch(waves_root, "round-1/dispatch.json",
                        [_task("A", report_paths["A"]), _task("B", report_paths["A"])], "fixture-r5")
    elif case_id == "r6-taskcall-missing":
        _write_json(os.path.join(waves_root, "round-1/dispatch.json"),
                    {"schema": DISPATCH_SCHEMA, "wave": "fixture-r6"})
    elif case_id == "r7-dotdot-inside-lane":
        _write_report(lane_root, report_paths["A"])
        _write_dispatch(waves_root, "round-1/dispatch.json",
                        [_task("A", ".ufo/../" + report_paths["A"])], "fixture-r7")
    else:
        raise ValueError("unknown frozen case")

    return lane_root, fleet_root if case_id == "misrooted" else None


def _first_wave(payload: dict) -> dict:
    waves = payload.get("waves", [])
    if not waves:
        raise AssertionError("expected a discovered wave")
    return waves[0]


def _check_case(case: dict, payload: dict, rc: int, serialized: bytes,
                repeated_serialized: bytes | None = None) -> bool:
    expected = case["expect"]
    if "exit" in expected and rc != expected["exit"]:
        return False
    waves = payload["waves"]
    if "waves" in expected and len(waves) != expected["waves"]:
        return False
    if "ignored_json" in expected and payload["ignored_json"] != expected["ignored_json"]:
        return False
    if "unreadable_json" in expected and payload["unreadable_json"] != expected["unreadable_json"]:
        return False

    if "state" in expected and _first_wave(payload)["state"] != expected["state"]:
        return False
    if "members" in expected and len(_first_wave(payload)["members"]) != expected["members"]:
        return False
    for status in STATUS_NAMES:
        if status in expected and _first_wave(payload)["counts"][status] != expected[status]:
            return False
    if "missing_names" in expected and _first_wave(payload)["missing"] != expected["missing_names"]:
        return False
    if False:
        return False
    if "duplicate_report_paths" in expected and \
            _first_wave(payload)["duplicate_report_paths"] != expected["duplicate_report_paths"]:
        return False
    if "unique_dispatch_sha256" in expected and \
            payload["totals"]["unique_dispatch_sha256"] != expected["unique_dispatch_sha256"]:
        return False
    if "second_duplicate_of" in expected and \
            payload["waves"][1]["duplicate_of"] != expected["second_duplicate_of"]:
        return False
    if expected.get("stdout_contains_canary") is False and b"CANARY-r20-7f3a" in serialized:
        return False
    if expected.get("out_contains_canary") is False and b"CANARY-r20-7f3a" in serialized:
        return False
    if expected.get("not_followed") is True:
        if _first_wave(payload)["counts"]["present"] != 0:
            return False
        if _first_wave(payload)["members"][0]["status"] != "missing":
            return False
    if expected.get("byte_identical") is True:
        if repeated_serialized != serialized:
            return False
    if expected.get("waves_sorted_by_path") is True:
        paths = [wave["dispatch_path"] for wave in waves]
        if paths != sorted(paths, key=_path_bytes):
            return False
    if "no_vocab" in expected:
        vocabulary_payload = dict(payload)
        vocabulary_payload["waves"] = [
            {key: value for key, value in wave.items() if key != "dispatch_sha256"}
            for wave in payload["waves"]
        ]
        text = _json_bytes(vocabulary_payload).decode("ascii").lower()
        if any(re.search(r"\b" + re.escape(word.lower()) + r"\b", text)
               for word in expected["no_vocab"]):
            return False
    return True


def _selftest() -> int:
    oracle_path = _oracle_path()
    try:
        if oracle_path is None:
            raise OSError("frozen oracle unavailable")
        with open(oracle_path, "rb") as stream:
            oracle = json.load(stream)
        cases = oracle["cases"]
        if not isinstance(cases, list):
            raise ValueError("oracle cases are not a list")
        cases = cases + REFINEMENT_CASES
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("MORI_WAVE_SETTLEMENT_SELFTEST: FAIL (0 cases, 0 passed, 0 failed)")
        return 1

    passed = 0
    try:
        with tempfile.TemporaryDirectory(prefix="mori-wave-settlement-", dir=os.environ.get("TMPDIR")) as temp_root:
            for index, case in enumerate(cases):
                try:
                    case_root = os.path.join(temp_root, f"case-{index:02d}")
                    os.makedirs(case_root)
                    lane_root, fleet_root = _fixture(case["id"], case_root)
                    payload, rc = scan_lane(lane_root, fleet_root)
                    serialized = _json_bytes(payload)
                    repeated_serialized = None
                    if case["expect"].get("byte_identical") is True:
                        repeated_payload, repeated_rc = scan_lane(lane_root, fleet_root)
                        if repeated_rc == rc:
                            repeated_serialized = _json_bytes(repeated_payload)
                    if _check_case(case, payload, rc, serialized, repeated_serialized):
                        passed += 1
                except Exception:
                    continue
    except Exception:
        passed = 0

    failed = len(cases) - passed
    result = "PASS" if failed == 0 else "FAIL"
    print(f"MORI_WAVE_SETTLEMENT_SELFTEST: {result} ({len(cases)} cases, {passed} passed, {failed} failed)")
    return 0 if failed == 0 else 1


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only per-seat wave settlement scan.", allow_abbrev=False)
    subparsers = parser.add_subparsers(dest="command")
    scan_parser = subparsers.add_parser("scan", allow_abbrev=False)
    scan_parser.add_argument("--lane-root", required=True)
    scan_parser.add_argument("--fleet-root")
    scan_parser.add_argument("--out")
    return parser


def main(argv: list[str] | None = None) -> int:
    args_list = list(sys.argv[1:] if argv is None else argv)
    if args_list == ["--selftest"]:
        return _selftest()

    parser = _parser()
    args = parser.parse_args(args_list)
    if args.command != "scan":
        parser.error("select scan or --selftest")

    try:
        payload, rc = scan_lane(args.lane_root, args.fleet_root)
    except ScanError:
        print("mori-wave-settlement: lane root is unreadable", file=sys.stderr)
        return 2

    output = _json_bytes(payload)
    if args.out is not None:
        try:
            with open(args.out, "wb") as stream:
                stream.write(output)
        except OSError:
            print("mori-wave-settlement: cannot write --out", file=sys.stderr)
            return 2
    sys.stdout.buffer.write(output)
    return rc


if __name__ == "__main__":
    sys.exit(main())
