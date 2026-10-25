#!/usr/bin/env python3
"""mori gate-registry auditor (round 44).

Checks the lane's stated gate standard (SKILL.md section `## Gates`) against
committed bytes: for every audited tool path, a registry row must name it in its
`entry` cell with all eight standard cells non-empty (name, kind, entry, verdict
map, self-test, pinned values, write scope, owner), the named tool path must
resolve at the audited revision, and the tool must carry a `--selftest` mode.

Usage:
  python3 tools/mori-gate-registry.py --rev <rev|WORK> [--repo PATH]
          [--registry SKILL.md] --audit <repo-relative path> [--audit ...]
  python3 tools/mori-gate-registry.py --selftest

Exit: 0 REGISTRY=met · 1 REGISTRY=unmet · 2 REGISTRY_SETUP.

The row is evidence of a declared standard; the tool's selftest is what enforces
it (P-C2, .ufo/waves/round-44/contract.md).
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

FIELDS = ["name", "kind", "entry", "verdict map", "self-test",
          "pinned values", "write scope", "owner"]


def repo_default():
    here = os.path.abspath(__file__)          # <repo>/tools/mori-gate-registry.py
    return os.path.dirname(os.path.dirname(here))


def git(repo, args, timeout=30):
    return subprocess.run(["git", "-C", repo] + args, capture_output=True,
                          text=True, timeout=timeout, check=False)


def exists_at(repo, rev, path):
    if rev == "WORK":
        return os.path.isfile(os.path.join(repo, path))
    return git(repo, ["cat-file", "-e", "%s:%s" % (rev, path)]).returncode == 0


def read_at(repo, rev, path):
    if rev == "WORK":
        full = os.path.join(repo, path)
        if not os.path.isfile(full):
            return None
        with open(full, "rb") as fh:
            return fh.read()
    if not exists_at(repo, rev, path):
        return None
    got = git(repo, ["show", "%s:%s" % (rev, path)])
    if got.returncode != 0:
        raise RuntimeError("git show failed for %s:%s" % (rev, path))
    return got.stdout.encode()


CELL_SPLIT = re.compile(r"(?<!\\)\|")


def split_row(line):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip() for c in CELL_SPLIT.split(body)]


def entry_names(cell, base):
    """True when the entry cell invokes `base` itself, not merely passes it."""
    pattern = r"^(?:(?:bash|sh|python3|node|time|env)\s+)*" + re.escape(base) + r"(?:\s|$)"
    return re.search(pattern, cell.strip().lstrip("`").strip()) is not None


def parse_gate_table(text):
    """Rows of the `## Gates` table, header located by its field names."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().lower() == "## gates":
            start = i
            break
    if start is None:
        return None, None
    header, rows = None, []
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if not stripped.startswith("|"):
            continue
        cells = split_row(stripped)
        low = [c.lower() for c in cells]
        if header is None:
            if len(cells) >= 8 and low[0] == "name" and low[1] == "kind":
                header = low
            continue
        if set("".join(cells)) <= {"-", ":"}:
            continue
        rows.append(cells)
    return header, rows


def audit(repo, rev, registry_path, targets):
    raw = read_at(repo, rev, registry_path)
    if raw is None:
        raise RuntimeError("registry absent at %s: %s" % (rev, registry_path))
    header, rows = parse_gate_table(raw.decode("utf-8", "replace"))
    if header is None:
        raise RuntimeError("no gate table with a name/kind header in %s" % registry_path)

    results, ok = [], True
    for target in targets:
        base = target.rstrip("/")
        name = os.path.basename(base)
        matches = [r for r in rows
                   if len(r) >= 3 and entry_names(r[2], base)]
        if not matches:
            matches = [r for r in rows
                       if len(r) >= 3 and (base in r[2] or name in r[2])]
        if not matches:
            results.append((target, False, "unregistered: no row names %s" % name))
            ok = False
            continue
        row = sorted(matches, key=lambda r: len(r[2]))[0]
        label = row[0] if row else "?"
        cells = dict(zip(header, row)) if len(row) >= len(header) else {}
        missing = [f for f in FIELDS if not (cells.get(f) or "").strip()]
        if missing:
            results.append((target, False, "row %r missing cells: %s"
                            % (label, ",".join(missing))))
            ok = False
            continue
        if not exists_at(repo, rev, base):
            results.append((target, False, "row %r entry path does not resolve at %s"
                            % (label, rev[:12])))
            ok = False
            continue
        body = read_at(repo, rev, base) or b""
        if b"--selftest" not in body:
            results.append((target, False, "row %r tool has no --selftest mode" % label))
            ok = False
            continue
        results.append((target, True, "row %r: 8 cells, entry resolves, --selftest present"
                        % label))
    return results, ok


# --------------------------------------------------------------------------

GOOD_ROW = ("| fixture gate | gate | `bash tools/fixture-tool.sh` | 0 clean · 1 failed · "
            "2 could-not-evaluate | `bash tools/fixture-tool.sh --selftest` | in-script "
            "cases | stdout only | mori |")
HEADER = "| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |"


def _registry(rows):
    return ("# SKILL\n\n## Gates\n\n" + HEADER + "\n"
            + "|---|---|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n")


def _mk(tmp, rows, tool_body, tool_name="tools/fixture-tool.sh"):
    repo = os.path.join(tmp, "repo")
    os.makedirs(repo, exist_ok=True)
    git(repo, ["init", "-q", "-b", "main"])
    git(repo, ["config", "user.email", "mori@shokunin.local"])
    git(repo, ["config", "user.name", "mori-shokunin"])
    with open(os.path.join(repo, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(_registry(rows))
    full = os.path.join(repo, tool_name)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(tool_body)
    git(repo, ["add", "-A"])
    git(repo, ["commit", "-q", "-m", "fixture"])
    rev = git(repo, ["rev-parse", "main"]).stdout.strip()
    return repo, rev


def selftest():
    arms, failures = [], []
    tool_ok = "#!/bin/sh\n# --selftest mode\n"

    def arm(name, fn):
        try:
            fn()
            arms.append(name)
        except AssertionError as exc:
            failures.append("%s: %s" % (name, exc))
        except Exception as exc:                      # noqa: BLE001
            failures.append("%s: raised %s" % (name, exc))

    def good():
        tmp = tempfile.mkdtemp(prefix="grst-")
        try:
            repo, rev = _mk(tmp, [GOOD_ROW], tool_ok)
            res, ok = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
            assert ok, res
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def missing_cell():
        row = GOOD_ROW.replace("| in-script cases ", "|  ")
        tmp = tempfile.mkdtemp(prefix="grst-")
        try:
            repo, rev = _mk(tmp, [row], tool_ok)
            _res, ok = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
            assert not ok, "a row with an empty pinned-values cell was accepted"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def unresolved_entry():
        row = GOOD_ROW.replace("tools/fixture-tool.sh", "tools/ghost-tool.sh", 1)
        tmp = tempfile.mkdtemp(prefix="grst-")
        try:
            repo, rev = _mk(tmp, [row], tool_ok)
            _res, ok = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
            assert not ok, "an entry path that does not resolve was accepted"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def unregistered():
        tmp = tempfile.mkdtemp(prefix="grst-")
        try:
            repo, rev = _mk(tmp, [GOOD_ROW], tool_ok)
            _res, ok = audit(repo, rev, "SKILL.md", ["tools/other-tool.sh"])
            assert not ok, "an unregistered path was accepted"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def no_selftest_mode():
        tmp = tempfile.mkdtemp(prefix="grst-")
        try:
            repo, rev = _mk(tmp, [GOOD_ROW], "#!/bin/sh\nexit 0\n")
            _res, ok = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
            assert not ok, "a tool without --selftest was accepted"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def seven_columns():
        row = GOOD_ROW.rstrip("|")
        cells = [c.strip() for c in row.strip().strip("|").split("|")][:-1]
        short = "| " + " | ".join(cells) + " |"
        tmp = tempfile.mkdtemp(prefix="grst-")
        try:
            repo, rev = _mk(tmp, [short], tool_ok)
            _res, ok = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
            assert not ok, "a seven-cell row was accepted"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    arm("registered_row_met", good)
    arm("missing_cell_rejected", missing_cell)
    arm("unresolved_entry_rejected", unresolved_entry)
    arm("unregistered_path_rejected", unregistered)
    arm("no_selftest_rejected", no_selftest_mode)
    arm("seven_cell_row_rejected", seven_columns)

    for name in arms:
        print("selftest PASS %s" % name)
    for name in failures:
        print("selftest FAIL %s" % name)
    print("GATE_REGISTRY_SELFTEST pass=%d fail=%d" % (len(arms), len(failures)))
    return 0 if not failures else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--rev")
    ap.add_argument("--repo", default=repo_default())
    ap.add_argument("--registry", default="SKILL.md")
    ap.add_argument("--audit", action="append", default=[])
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.rev or not args.audit:
        print("usage: mori-gate-registry.py --rev <rev|WORK> --audit <path> [...] [--selftest]")
        return 2
    repo = os.path.abspath(args.repo)
    rev = args.rev
    if rev != "WORK":
        resolved = git(repo, ["rev-parse", "--verify", rev + "^{commit}"])
        if resolved.returncode != 0:
            print("REGISTRY_SETUP cannot resolve revision %r" % rev)
            return 2
        rev = resolved.stdout.strip()
    try:
        results, ok = audit(repo, rev, args.registry, args.audit)
    except Exception as exc:                          # noqa: BLE001
        print("REGISTRY_SETUP %s" % exc)
        return 2
    for target, good, detail in results:
        print("audit %-40s %s (%s)" % (target, "PASS" if good else "FAIL", detail))
    print("rev=%s" % rev)
    print("REGISTRY=%s" % ("met" if ok else "unmet"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
