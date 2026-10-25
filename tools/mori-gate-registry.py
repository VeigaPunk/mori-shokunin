#!/usr/bin/env python3
"""mori gate-registry auditor (round 45, v2 — P-C2).

Checks the lane's stated gate standard against committed bytes. Every table in
the registry file whose header row is the eight standard cells (name, kind,
entry, verdict map, self-test, pinned values, write scope, owner) is read,
wherever it sits in the file; a table with a different header is not a registry
table and is not a finding. For each audited path exactly one attribution rule
applies: the path's own row is the row whose `entry` cell's first backticked
command invokes that path (`entry_names`). Prose, a substring elsewhere in a
cell, and a row naming another tool never attribute.

A row must carry all eight cells, its entry path must resolve at the audited
revision (and never be absolute or step outside the repo), and the tool must
carry a real self-test argv branch: an occurrence of `--selftest` inside a
comment line or a docstring is not a branch (the r44 silence-oracle false
positive). A row whose self-test is a different flag declares it in its
`self-test` cell as `selftest-flag=<flag>`; that flag's name must contain `test`
(so `--a` or `--repo` cannot stand in for a self-test) and the tool must carry
it as a parser key (`add_argument("--self-test")`) or a shell `case` pattern
(`--self-test)`), never merely mention it. A registry `name` occurring twice is
a finding. A row whose entry names a repo path absent at the revision is a
finding (`wrong_row`).

Usage:
  python3 tools/mori-gate-registry.py --rev <rev|WORK> [--repo PATH]
          [--registry SKILL.md] --audit <repo-relative path> [--audit ...]
  python3 tools/mori-gate-registry.py --rev <rev|WORK> --audit-all [--repo PATH]
  python3 tools/mori-gate-registry.py --selftest

--audit-all enumerates the declared population at --rev: tools/*.py,
tools/*.sh and .ufo/waves/round-44/count-c*.py plus
.ufo/waves/round-45/count-c*.py, then audits every member. It is mutually
exclusive with --audit: supplying both is REGISTRY_SETUP (a population run must
never silently audit one explicit path and call the population clean).

Stdout: one `audit <path> PASS|FAIL row='<name>' (<detail>)` line per audited
path (`row=` only when a row attributes it), one line per duplicate name and
per untrustworthy registry row, `tables=<n>`, `rev=<rev>`, and on a population
run `mode=population` plus `population_digest=<sha256 of the newline-joined
sorted target list>`, then the counter line
`registered=<n> unregistered=<n> no_selftest=<n> duplicate=<n> wrong_row=<n>
tables=<n>`, then `REGISTRY=met|unmet`.

Counter meanings: `registered` audited paths attributed to a well-formed row
whose entry resolves and whose tool carries a real self-test branch;
`unregistered` no row names the path; `no_selftest` the row names it but the
tool has no real self-test argv branch; `duplicate` distinct registry names
occurring more than once; `wrong_row` attributed paths whose row is malformed,
plus registry rows whose entry path is absent at the revision or leaves the
repo; `tables` registry tables read. Only `met` means all of them are zero.

Exit: 0 REGISTRY=met · 1 REGISTRY=unmet · 2 REGISTRY_SETUP (usage, unresolvable
revision, git timeout, absent registry or gate table, empty population). The row
is evidence of a declared standard; the tool's own selftest is what enforces it
(P-C2, .ufo/waves/round-45/contract.md).
"""
import argparse
import contextlib
import hashlib
import io
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile

FIELDS = ["name", "kind", "entry", "verdict map", "self-test",
          "pinned values", "write scope", "owner"]

SELFTEST = "--selftest"
WRAPPERS = {"bash", "sh", "dash", "zsh", "python", "python3", "python3.12",
            "node", "env", "time", "sudo", "exec", "command", "nohup", "uv"}
ENV_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
TOKEN_STRIP = "`'\"()[]<>"
FLAG_DECL = re.compile(r"selftest[- ]flag\s*[:=]\s*`?(-{1,2}[A-Za-z0-9][\w.-]*)`?",
                       re.IGNORECASE)
CELL_SPLIT = re.compile(r"(?<!\\)\|")
PY_ARGV = re.compile(r"(sys\.argv|\bargv\b|add_argument|ArgumentParser|parse_args|"
                     r"parse_known_args|optparse|getopt|args\.(?:selftest|self_test)|"
                     r"parser\.)")
SH_ARGV = re.compile(r'("\$@"|\$\*|\$#|\$\{[0-9@]|\$[1-9]\b|\bcase\b|\bshift\b|'
                     r'\$arg\b|\$\{arg)')
COUNTER_DIRS = (".ufo/waves/round-44", ".ufo/waves/round-45")
COUNTER_RE = re.compile(r"count-c.*\.py$")


def repo_default():
    """The nearest ancestor holding tools/ and SKILL.md (a relocated copy still
    resolves the lane, never a bare dirname guess)."""
    here = os.path.dirname(os.path.abspath(__file__))
    probe = here
    while True:
        if (os.path.isdir(os.path.join(probe, "tools"))
                and os.path.isfile(os.path.join(probe, "SKILL.md"))):
            return probe
        parent = os.path.dirname(probe)
        if parent == probe:
            return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        probe = parent


def child_env():
    """The environment for git children: no inherited GIT_* redirection."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def git(repo, args, timeout=30):
    return subprocess.run(["git", "-C", repo] + args, capture_output=True,
                          text=True, timeout=timeout, check=False,
                          env=child_env())


def safe_relpath(path):
    """Normalise a repo-relative path; None when absolute or escaping the repo."""
    if not path:
        return None
    p = path.replace("\\", "/")
    if p.startswith("/") or re.match(r"^[A-Za-z]:", p):
        return None
    norm = posixpath.normpath(p)
    if norm in (".", "..") or norm.startswith("../"):
        return None
    return norm


def inside_repo(repo, path):
    root = os.path.realpath(repo)
    full = os.path.realpath(os.path.join(root, path))
    return full == root or full.startswith(root + os.sep)


def exists_at(repo, rev, path):
    if rev == "WORK":
        return inside_repo(repo, path) and os.path.isfile(os.path.join(repo, path))
    return git(repo, ["cat-file", "-e", "%s:%s" % (rev, path)]).returncode == 0


def read_at(repo, rev, path):
    if rev == "WORK":
        if not exists_at(repo, rev, path):
            return None
        with open(os.path.join(repo, path), "rb") as fh:
            return fh.read()
    if not exists_at(repo, rev, path):
        return None
    got = git(repo, ["show", "%s:%s" % (rev, path)])
    if got.returncode != 0:
        raise RuntimeError("git show failed for %s:%s" % (rev[:12], path))
    return got.stdout.encode()


def ls_at(repo, rev, dirpath):
    """Repo-relative files directly under dirpath at rev (never recursive)."""
    d = dirpath.strip("/")
    if rev == "WORK":
        base = os.path.join(repo, d)
        if not inside_repo(repo, d) or not os.path.isdir(base):
            return []
        return sorted(d + "/" + n for n in os.listdir(base)
                      if os.path.isfile(os.path.join(base, n)))
    got = git(repo, ["ls-tree", "--name-only", rev, "--", d + "/"])
    if got.returncode != 0:
        raise RuntimeError("git ls-tree failed for %s:%s" % (rev[:12], d))
    out = []
    for line in got.stdout.splitlines():
        p = line.strip()
        if not p.startswith(d + "/"):
            continue
        rest = p[len(d) + 1:]
        if not rest or "/" in rest:
            continue
        out.append(p)
    return sorted(out)


def population(repo, rev):
    """The declared C2 population at rev: tools/*.py, tools/*.sh, round counters."""
    targets = []
    for p in ls_at(repo, rev, "tools"):
        if p.endswith((".py", ".sh")):
            targets.append(p)
    for d in COUNTER_DIRS:
        for p in ls_at(repo, rev, d):
            if COUNTER_RE.match(posixpath.basename(p)):
                targets.append(p)
    return sorted(set(targets))


# ---- registry tables ------------------------------------------------------

def split_row(line):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip() for c in CELL_SPLIT.split(body)]


def is_standard_header(cells):
    return [c.lower() for c in cells] == FIELDS


def is_separator(cells):
    return (bool(cells) and any("-" in c for c in cells)
            and all(c and set(c) <= set("-: ") for c in cells))


def parse_tables(text):
    """Every pipe table whose header row is the eight standard cells."""
    lines = text.splitlines()
    tables, i = [], 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and is_standard_header(split_row(lines[i])):
            rows, j = [], i + 1
            while j < len(lines) and lines[j].strip().startswith("|"):
                cells = split_row(lines[j])
                if not is_separator(cells):
                    rows.append({"line": j + 1, "cells": cells})
                j += 1
            tables.append({"line": i + 1, "rows": rows})
            i = j
        else:
            i += 1
    return tables


def entry_target(cell):
    """The repo path the entry cell invokes: first backticked command's script."""
    m = re.search(r"`([^`]+)`", cell or "")
    if not m:
        return None
    for tok in m.group(1).split():
        t = tok.strip(TOKEN_STRIP)
        if not t or t.startswith("-") or t in WRAPPERS or ENV_ASSIGN.match(t):
            continue
        if "/" in t or posixpath.basename(t).endswith((".py", ".sh")):
            return posixpath.normpath(t)
    return None


def entry_names(cell, base):
    """True when the entry cell's first command invokes `base` itself."""
    tok = entry_target(cell)
    wanted = safe_relpath(base)
    return tok is not None and wanted is not None and tok == wanted


# ---- real self-test branch ------------------------------------------------

def mask_python(text):
    """Blank comment text and triple-quoted blocks, preserving line positions."""
    out, i, n = [], 0, len(text)
    while i < n:
        if text.startswith('"""', i) or text.startswith("'''", i):
            quote = text[i:i + 3]
            out.append("   ")
            i += 3
            while i < n and not text.startswith(quote, i):
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            if i < n:
                out.append("   ")
                i += 3
        elif text[i] == "#":
            while i < n and text[i] != "\n":
                out.append(" ")
                i += 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def mask_shell(text):
    """Blank `#` comments, preserving line positions."""
    out = []
    for line in text.splitlines():
        m = re.search(r"(^|\s)#", line)
        if m:
            line = line[:m.start(1) + len(m.group(1))]
        out.append(line)
    return "\n".join(out)


def _flag_in_python_tests(masked, flag):
    """A parser key, a flag comparison, or a membership test against argv."""
    f = re.escape(flag)
    pattern = (
        r"(?:add_argument|add_option)\(\s*[\"']" + f + r"[\"']"
        r"|[\"']" + f + r"[\"']\s*(?:==|!=|\bin\s+(?:raw|argv|args|sys\.argv|"
        r"arguments|options|opts|tokens|words)\b)"
        r"|(?:==|!=)\s*\[?\s*[\"']" + f + r"[\"']"
        r"|\bin\s*[\(\[]\s*[\"']" + f + r"[\"']"
    )
    return re.search(pattern, masked) is not None


def selftest_flag(body, path, flag=SELFTEST):
    """True when `flag` appears in argv handling, never only in a comment."""
    text = (body or b"").decode("utf-8", "replace")
    if path.endswith(".sh"):
        masked = mask_shell(text)
        lines = masked.splitlines()
        for i, line in enumerate(lines):
            if flag not in line:
                continue
            if re.search(r"^\s*(?:[^\s|()]+\|)*" + re.escape(flag) + r"\s*[|)]", line):
                return True
            if SH_ARGV.search(" ".join(lines[max(0, i - 2):i + 1])):
                return True
        return False
    masked = mask_python(text)
    if not PY_ARGV.search(masked):
        return False
    return _flag_in_python_tests(masked, flag)


def declared_flag(cell):
    """The flag a row declares for its self-test, when it is not --selftest."""
    m = FLAG_DECL.search(cell or "")
    return m.group(1) if m else None


def escape_branch(body, path, flag):
    """A declared non-standard self-test flag must look like one and be a real
    hook: a Python parser key or a shell `case` pattern, never a mere mention."""
    if "test" not in flag.lstrip("-").lower():
        return False
    text = (body or b"").decode("utf-8", "replace")
    shell = path.endswith(".sh")
    masked = mask_shell(text) if shell else mask_python(text)
    f = re.escape(flag)
    if shell:
        pattern = r"(?m)^\s*(?:[^\s|()]+\|)*" + f + r"\s*\)"
    else:
        pattern = r"(?m)(?:add_argument|add_option)\(\s*[\"']" + f + r"[\"']"
    return re.search(pattern, masked) is not None


# ---- the audit ------------------------------------------------------------

def audit(repo, rev, registry_path, targets):
    if not targets:
        raise RuntimeError("empty population: an audit with no paths cannot be met")
    reg = safe_relpath(registry_path)
    if reg is None:
        raise RuntimeError("registry path %r is not repo-relative" % registry_path)
    raw = read_at(repo, rev, reg)
    if raw is None:
        raise RuntimeError("registry absent at %s: %s" % (rev[:12], registry_path))
    tables = parse_tables(raw.decode("utf-8", "replace"))
    if not tables:
        raise RuntimeError("no registry table with the eight standard cells in %s"
                           % registry_path)

    rows = []
    for number, table in enumerate(tables, 1):
        for row in table["rows"]:
            rows.append(dict(row, table=number))

    seen = {}
    for row in rows:
        cells = row["cells"]
        name = cells[0].strip() if cells and cells[0].strip() else ""
        if name:
            seen.setdefault(name, []).append(row["line"])
    duplicates = [{"name": n, "lines": ls} for n, ls in sorted(seen.items())
                  if len(ls) > 1]

    wrong_rows = []
    for row in rows:
        cells = row["cells"]
        tok = entry_target(cells[2]) if len(cells) > 2 else None
        if tok is None:
            continue
        safe = safe_relpath(tok)
        name = cells[0].strip() if cells and cells[0].strip() else "?"
        if safe is None:
            wrong_rows.append({"line": row["line"], "name": name,
                               "entry": tok, "why": "absolute or outside the repo"})
        elif not exists_at(repo, rev, safe):
            wrong_rows.append({"line": row["line"], "name": name,
                               "entry": safe, "why": "absent at %s" % rev[:12]})

    results, ok = [], True

    def fail(target, status, detail, name=None):
        nonlocal ok
        ok = False
        results.append({"target": target, "ok": False, "status": status,
                        "row": name, "detail": detail})

    for target in targets:
        safe = safe_relpath(target)
        if safe is None:
            fail(target, "unregistered", "audited path is absolute or outside the repo")
            continue
        matches = [r for r in rows
                   if len(r["cells"]) >= 3 and entry_names(r["cells"][2], safe)]
        if not matches:
            fail(target, "unregistered", "no row names %s" % safe)
            continue
        row = matches[0]
        cells = row["cells"]
        name = cells[0].strip() if cells and cells[0].strip() else "?"
        if len(cells) != len(FIELDS):
            fail(target, "wrong_row", "row has %d cells, expected %d"
                 % (len(cells), len(FIELDS)), name)
            continue
        missing = [f for f, c in zip(FIELDS, cells) if not c.strip()]
        if missing:
            fail(target, "wrong_row", "row '%s' missing cells: %s"
                 % (name, ", ".join(missing)), name)
            continue
        tok = entry_target(cells[2])
        entry = safe_relpath(tok or "")
        if entry is None:
            fail(target, "wrong_row", "row '%s' entry path %r is absolute or outside "
                 "the repo" % (name, tok), name)
            continue
        if not exists_at(repo, rev, entry):
            fail(target, "wrong_row", "row '%s' entry path %s does not resolve at %s"
                 % (name, entry, rev[:12]), name)
            continue
        body = read_at(repo, rev, entry) or b""
        flag = declared_flag(cells[4])
        if flag and flag != SELFTEST:
            if not escape_branch(body, entry, flag):
                fail(target, "no_selftest", "row '%s' declares selftest-flag %s, but %s "
                     "has no %s parser key or case pattern (a self-test flag name must "
                     "also contain 'test')" % (name, flag, entry, flag), name)
                continue
        elif not selftest_flag(body, entry, SELFTEST):
            fail(target, "no_selftest", "row '%s' tool has no real %s argv branch"
                 % (name, SELFTEST), name)
            continue
        used = flag or SELFTEST
        results.append({"target": target, "ok": True, "status": "registered",
                        "row": name,
                        "detail": "8 cells, entry resolves, %s argv branch" % used})

    if duplicates or wrong_rows:
        ok = False
    stats = {"registered": 0, "unregistered": 0, "no_selftest": 0, "wrong_row": 0}
    for entry in results:
        stats[entry["status"]] = stats.get(entry["status"], 0) + 1
    return {"results": results, "ok": ok, "tables": len(tables),
            "duplicates": duplicates, "wrong_rows": wrong_rows, "stats": stats}


# ---- selftest -------------------------------------------------------------

GOOD_ROW = ("| fixture gate | gate | `bash tools/fixture-tool.sh` | 0 clean · 1 failed · "
            "2 could-not-evaluate | `bash tools/fixture-tool.sh --selftest` | in-script "
            "cases | stdout only | mori |")
HEADER = "| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |"
SEPARATOR = "|---|---|---|---|---|---|---|---|"
TOOL_OK = ('#!/bin/sh\ncase "${1-}" in\n  --selftest) echo ok; exit 0 ;;\nesac\n'
           'exit 0\n')


def _registry(rows, extra=None):
    text = ("# fixture registry\n\n## Gates\n\n" + HEADER + "\n" + SEPARATOR + "\n"
            + "".join(r + "\n" for r in rows))
    if extra is not None:
        text += ("\n## Later registry\n\n" + HEADER + "\n" + SEPARATOR + "\n"
                 + "".join(r + "\n" for r in extra))
    return text


def _mk(tmp, rows, tool_body, extra_rows=None, extra_tools=None):
    repo = os.path.join(tmp, "repo")
    os.makedirs(repo, exist_ok=True)
    git(repo, ["init", "-q", "-b", "main"])
    git(repo, ["config", "user.email", "mori@shokunin.local"])
    git(repo, ["config", "user.name", "mori-shokunin"])
    with open(os.path.join(repo, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(_registry(rows, extra_rows))
    files = {"tools/fixture-tool.sh": tool_body}
    files.update(extra_tools or {})
    for name, body in files.items():
        full = os.path.join(repo, name)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(body)
    git(repo, ["add", "-A"])
    commit = git(repo, ["commit", "-q", "-m", "fixture"])
    if commit.returncode != 0:
        raise RuntimeError("fixture commit failed: %s" % commit.stderr.strip()[:200])
    rev = git(repo, ["rev-parse", "main"]).stdout.strip()
    if not rev:
        raise RuntimeError("fixture revision unresolved")
    return repo, rev


def selftest():
    arms, failures = [], []

    def arm(name, fn):
        tmp = tempfile.mkdtemp(prefix="grst-")
        try:
            fn(tmp)
            arms.append(name)
        except AssertionError as exc:
            failures.append("%s: %s" % (name, exc))
        except Exception as exc:                      # noqa: BLE001
            failures.append("%s: raised %r" % (name, exc))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def _selftest_cell(cell):
        old = "`bash tools/fixture-tool.sh --selftest`"
        assert old in GOOD_ROW, "fixture self-test cell moved"
        return GOOD_ROW.replace(old, cell)

    def _capture(argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(argv)
        return rc, buf.getvalue()

    def good(tmp):
        repo, rev = _mk(tmp, [GOOD_ROW], TOOL_OK)
        rep = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
        assert rep["ok"], rep
        assert rep["tables"] == 1, rep["tables"]
        assert rep["results"][0]["status"] == "registered", rep["results"][0]
        assert rep["results"][0]["row"] == "fixture gate", rep["results"][0]

    def missing_cell(tmp):
        row = GOOD_ROW.replace("| in-script cases ", "|  ")
        assert row != GOOD_ROW, "fixture row edit missed"
        repo, rev = _mk(tmp, [row], TOOL_OK)
        rep = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
        assert not rep["ok"], "a row with an empty pinned-values cell was accepted"
        assert rep["results"][0]["status"] == "wrong_row", rep["results"][0]
        assert "pinned values" in rep["results"][0]["detail"], rep["results"][0]

    def unresolved_entry(tmp):
        row = GOOD_ROW.replace("tools/fixture-tool.sh", "tools/ghost-tool.sh")
        repo, rev = _mk(tmp, [row], TOOL_OK)
        rep = audit(repo, rev, "SKILL.md", ["tools/ghost-tool.sh"])
        assert not rep["ok"], "an entry path that does not resolve was accepted"
        assert rep["results"][0]["status"] == "wrong_row", rep["results"][0]
        assert "does not resolve" in rep["results"][0]["detail"], rep["results"][0]

    def unregistered(tmp):
        repo, rev = _mk(tmp, [GOOD_ROW], TOOL_OK)
        rep = audit(repo, rev, "SKILL.md", ["tools/other-tool.sh"])
        assert not rep["ok"], "an unregistered path was accepted"
        assert rep["results"][0]["status"] == "unregistered", rep["results"][0]

    def no_selftest_mode(tmp):
        repo, rev = _mk(tmp, [GOOD_ROW], "#!/bin/sh\nexit 0\n")
        rep = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
        assert not rep["ok"], "a tool without --selftest was accepted"
        assert rep["results"][0]["status"] == "no_selftest", rep["results"][0]

    def seven_columns(tmp):
        cells = split_row(GOOD_ROW)[:-1]
        short = "| " + " | ".join(cells) + " |"
        repo, rev = _mk(tmp, [short], TOOL_OK)
        rep = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
        assert not rep["ok"], "a seven-cell row was accepted"
        assert rep["results"][0]["status"] == "wrong_row", rep["results"][0]
        assert "7 cells" in rep["results"][0]["detail"], rep["results"][0]

    def second_table(tmp):
        repo, rev = _mk(tmp, [], TOOL_OK, extra_rows=[GOOD_ROW])
        rep = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
        assert rep["ok"], "a row in a second table was not read: %r" % (rep,)
        assert rep["tables"] == 2, rep["tables"]

    def duplicate_name(tmp):
        twin = GOOD_ROW.replace("tools/fixture-tool.sh", "tools/twin-tool.sh")
        repo, rev = _mk(tmp, [GOOD_ROW, twin], TOOL_OK,
                        extra_tools={"tools/twin-tool.sh": TOOL_OK})
        rep = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
        assert not rep["ok"], "a duplicate registry name was accepted"
        assert rep["duplicates"] and rep["duplicates"][0]["name"] == "fixture gate", \
            rep["duplicates"]

    def comment_only(tmp):
        body = "#!/bin/sh\n# --selftest is deliberately a comment here\nexit 0\n"
        repo, rev = _mk(tmp, [GOOD_ROW], body)
        rep = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
        assert not rep["ok"], "a comment-only --selftest occurrence was accepted"
        assert rep["results"][0]["status"] == "no_selftest", rep["results"][0]

    def empty_population(tmp):
        repo, rev = _mk(tmp, [GOOD_ROW], TOOL_OK)
        try:
            audit(repo, rev, "SKILL.md", [])
        except RuntimeError as exc:
            assert "empty population" in str(exc), exc
        else:
            raise AssertionError("an audit of zero paths was accepted")

    def audit_all_with_audit_refused(tmp):
        repo, rev = _mk(tmp, [GOOD_ROW], TOOL_OK)
        rc, out = _capture(["--rev", rev, "--repo", repo,
                            "--audit", "tools/fixture-tool.sh", "--audit-all"])
        assert rc == 2, (rc, out)
        assert "REGISTRY_SETUP" in out, out
        assert "REGISTRY=met" not in out, out

    def population_mode_and_digest(tmp):
        repo, rev = _mk(tmp, [GOOD_ROW], TOOL_OK)
        rc, out = _capture(["--rev", rev, "--repo", repo, "--audit-all"])
        assert rc == 0, (rc, out)
        assert "mode=population" in out, out
        want = hashlib.sha256(b"tools/fixture-tool.sh").hexdigest()
        assert "population_digest=%s" % want in out, out

    def escape_flag_accepted(tmp):
        row = _selftest_cell("`bash tools/fixture-tool.sh --self-test` "
                             "(selftest-flag=--self-test)")
        repo, rev = _mk(tmp, [row], TOOL_OK.replace("--selftest", "--self-test"))
        rep = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
        assert rep["ok"], rep
        assert "--self-test" in rep["results"][0]["detail"], rep["results"][0]

    def escape_flag_name_rejected(tmp):
        row = _selftest_cell("`bash tools/fixture-tool.sh --a` (selftest-flag=--a)")
        repo, rev = _mk(tmp, [row], TOOL_OK.replace("--selftest", "--a"))
        rep = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
        assert not rep["ok"], "a selftest-flag without 'test' in its name was accepted"
        assert rep["results"][0]["status"] == "no_selftest", rep["results"][0]

    def escape_flag_mention_rejected(tmp):
        row = _selftest_cell("`bash tools/fixture-tool.sh --self-test` "
                             "(selftest-flag=--self-test)")
        body = ('#!/bin/sh\ncase "$1" in\n'
                '  --help) printf "run with --self-test\\n"; exit 0 ;;\n'
                'esac\nexit 0\n')
        repo, rev = _mk(tmp, [row], body)
        rep = audit(repo, rev, "SKILL.md", ["tools/fixture-tool.sh"])
        assert not rep["ok"], "a mere mention of the escape flag was accepted"
        assert rep["results"][0]["status"] == "no_selftest", rep["results"][0]

    arm("registered_row_met", good)
    arm("missing_cell_rejected", missing_cell)
    arm("unresolved_entry_rejected", unresolved_entry)
    arm("unregistered_path_rejected", unregistered)
    arm("no_selftest_rejected", no_selftest_mode)
    arm("seven_cell_row_rejected", seven_columns)
    arm("second_table_registered", second_table)
    arm("duplicate_name_rejected", duplicate_name)
    arm("comment_only_selftest_rejected", comment_only)
    arm("empty_population_rejected", empty_population)
    arm("audit_all_with_audit_refused", audit_all_with_audit_refused)
    arm("population_mode_and_digest", population_mode_and_digest)
    arm("escape_flag_accepted", escape_flag_accepted)
    arm("escape_flag_name_rejected", escape_flag_name_rejected)
    arm("escape_flag_mention_rejected", escape_flag_mention_rejected)

    for name in arms:
        print("selftest PASS %s" % name)
    for name in failures:
        print("selftest FAIL %s" % name)
    print("GATE_REGISTRY_SELFTEST pass=%d fail=%d" % (len(arms), len(failures)))
    return 0 if not failures else 1


# ---- CLI ------------------------------------------------------------------

def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--rev")
    ap.add_argument("--repo", default=repo_default())
    ap.add_argument("--registry", default="SKILL.md")
    ap.add_argument("--audit", action="append", default=[])
    ap.add_argument("--audit-all", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.audit and args.audit_all:
        print("REGISTRY_SETUP --audit cannot be combined with --audit-all: population "
              "mode enumerates the declared population and takes no explicit paths")
        return 2
    if not args.rev or not (args.audit or args.audit_all):
        print("usage: mori-gate-registry.py --rev <rev|WORK> (--audit <repo-relative "
              "path> [--audit ...] | --audit-all) [--registry PATH] [--repo PATH]")
        print("REGISTRY_SETUP usage")
        return 2

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        print("REGISTRY_SETUP repo is not a directory: %s" % repo)
        return 2
    try:
        rev = args.rev
        if rev != "WORK":
            resolved = git(repo, ["rev-parse", "--verify", rev + "^{commit}"])
            if resolved.returncode != 0:
                raise RuntimeError("cannot resolve revision %r" % args.rev)
            rev = resolved.stdout.strip()
            if not rev:
                raise RuntimeError("cannot resolve revision %r" % args.rev)
        targets = population(repo, rev) if args.audit_all else list(args.audit)
        report = audit(repo, rev, args.registry, targets)
    except subprocess.TimeoutExpired as exc:
        print("REGISTRY_SETUP git timeout: %s" % exc)
        return 2
    except Exception as exc:                          # noqa: BLE001
        print("REGISTRY_SETUP %s" % exc)
        return 2

    for entry in report["results"]:
        label = "PASS" if entry["ok"] else "FAIL"
        row = (" row='%s'" % entry["row"]) if entry["row"] else ""
        print("audit %-40s %s%s (%s)" % (entry["target"], label, row, entry["detail"]))
    for dup in report["duplicates"]:
        print("duplicate name='%s' lines=%s"
              % (dup["name"], ",".join(str(n) for n in dup["lines"])))
    for wrong in report["wrong_rows"]:
        print("wrong_row line=%d row='%s' entry=%s %s"
              % (wrong["line"], wrong["name"], wrong["entry"], wrong["why"]))
    stats = report["stats"]
    print("tables=%d" % report["tables"])
    print("rev=%s" % rev)
    if args.audit_all:
        print("mode=population")
        print("population_digest=%s"
              % hashlib.sha256("\n".join(sorted(targets)).encode("utf-8")).hexdigest())
    print("registered=%d unregistered=%d no_selftest=%d duplicate=%d wrong_row=%d tables=%d"
          % (stats["registered"], stats["unregistered"], stats["no_selftest"],
             len(report["duplicates"]),
             stats["wrong_row"] + len(report["wrong_rows"]), report["tables"]))
    print("REGISTRY=%s" % ("met" if report["ok"] else "unmet"))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
