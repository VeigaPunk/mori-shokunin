#!/usr/bin/env python3
"""mori round-44 C3 — corpus-coverage conformance counter (frozen instrument).

Checks, at the measured revision, that an admitted knowledge entry on the
round's declared coverage ground is fully registered:
  * the entry file exists and carries `source:` lines naming every declared
    registry id, plus `verified-at:`, `recheck:` and `coverage-map: <map>`;
  * every declared id is a registry row in corpus/SOURCES.md with status `mined`
    and its `used-by` cell naming that entry;
  * the registry census validates on the committed bytes (exit 0);
  * corpus/README.md carries a frontier-map line naming the entry.

Usage:
  python3 count-c3.py <rev|WORK> --entry PATH --row S471 [--row S472 ...]
                      [--repo PATH] [--coverage-map FR5] [--census PATH]
                      [--readme corpus/README.md] [--timeout S]
  python3 count-c3.py --selftest

Exit: 0 C3=met · 1 C3=unmet · 2 C3_SETUP.

Predicate: .ufo/waves/round-44/contract.md P-C3.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
FIELDS = re.compile(r"(?<!\\)\|")


class Setup(Exception):
    pass


def repo_default():
    here = os.path.abspath(__file__)          # <repo>/.ufo/waves/round-44/count-c3.py
    d = os.path.dirname(here)
    while True:
        if os.path.isdir(os.path.join(d, ".git")) or os.path.isfile(
                os.path.join(d, "tools", "mori-gate-registry.py")):
            return d
        up = os.path.dirname(d)
        if up == d:
            return os.path.dirname(here)
        d = up


def git(repo, args, timeout=60):
    try:
        return subprocess.run(["git", "-C", repo] + args, capture_output=True,
                              text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise Setup("git timeout: %s" % " ".join(args))


def read_at(repo, rev, path):
    if rev == "WORK":
        full = os.path.join(repo, path)
        if not os.path.isfile(full):
            return None
        with open(full, "rb") as fh:
            return fh.read()
    if git(repo, ["cat-file", "-e", "%s:%s" % (rev, path)]).returncode != 0:
        return None
    got = git(repo, ["show", "%s:%s" % (rev, path)])
    if got.returncode != 0:
        raise Setup("git show failed for %s:%s" % (rev, path))
    return got.stdout.encode()


def census_rows(text):
    """id -> list of cells for every registry data row."""
    out = {}
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in FIELDS.split(line.strip().strip("|"))]
        out.setdefault(m.group(1), cells)
    return out


def evaluate(repo, rev, entry, rows, coverage_map, census, readme, timeout):
    checks, fails = [], []

    def record(name, ok, detail=""):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    body = read_at(repo, rev, entry)
    record("entry_present", body is not None,
           "absent" if body is None else "%d bytes" % len(body))
    if body is None:
        return checks, fails
    text = body.decode("utf-8", "replace")

    missing = [f for f in ("verified-at:", "recheck:") if f not in text]
    declared = re.findall(r"^source:\s*(S\d{3,})", text, re.M)
    absent_ids = [r for r in rows if r not in declared]
    if "coverage-map:" not in text:
        missing.append("coverage-map:")
    elif coverage_map not in text.split("coverage-map:", 1)[1].splitlines()[0]:
        missing.append("coverage-map %s" % coverage_map)
    record("entry_meta", not missing and not absent_ids,
           "; ".join(missing + ["source: lacks %s" % ",".join(absent_ids)])
           if (missing or absent_ids) else "sources %s" % ",".join(sorted(declared)))

    sources = read_at(repo, rev, "corpus/SOURCES.md")
    if sources is None:
        record("rows_present", False, "corpus/SOURCES.md absent")
        record("census_ok", False, "corpus/SOURCES.md absent")
    else:
        table = census_rows(sources.decode("utf-8", "replace"))
        bad = []
        for rid in rows:
            cells = table.get(rid)
            if not cells:
                bad.append("%s absent" % rid)
                continue
            status = cells[7] if len(cells) > 7 else ""
            used = cells[10] if len(cells) > 10 else ""
            if status != "mined":
                bad.append("%s status=%r" % (rid, status))
            elif entry not in used:
                bad.append("%s used-by does not name the entry" % rid)
        record("rows_present", not bad, "; ".join(bad) or "rows %s mined" % ",".join(rows))

        tmp = tempfile.mkdtemp(prefix="c3-")
        try:
            staged = os.path.join(tmp, "SOURCES.md")
            with open(staged, "wb") as fh:
                fh.write(sources)
            try:
                proc = subprocess.run(["bash", census, "validate", "--file", staged],
                                      capture_output=True, text=True, timeout=timeout,
                                      check=False, cwd=repo)
            except subprocess.TimeoutExpired:
                proc = None
            ok = proc is not None and proc.returncode == 0
            record("census_ok", ok, "exit=%s" % (proc.returncode if proc else "timeout"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    readme_body = read_at(repo, rev, readme)
    record("readme_row", readme_body is not None and entry.encode() in readme_body,
           "absent" if readme_body is None else
           ("names entry" if entry.encode() in readme_body else "no line names the entry"))
    return checks, fails


# --------------------------------------------------------------------------

ENTRY_OK = """# A fixture entry

source: {row} — https://example.invalid/page — quote
verified-at: 2026-10-25
recheck: 90d — `true` -> 1 (ran 2026-10-25)
coverage-map: {cm} — fixture frontier item

body
"""

ROW_OK = ("| {row} | Fixture page — https://example.invalid/page | docs | A | fixture scope | "
          "section:1-2; opened 2026-10-25 | A fixture teaches cell. | mined | 2026-10-25 | "
          "90d | {used} |")

CENSUS_OK = "#!/bin/sh\n# fixture census\nexit 0\n"
CENSUS_RED = "#!/bin/sh\nexit 1\n"


def _mk(tmp, files, commit=True):
    repo = os.path.join(tmp, "repo")
    os.makedirs(repo, exist_ok=True)
    git(repo, ["init", "-q", "-b", "main"])
    git(repo, ["config", "user.email", "mori@shokunin.local"])
    git(repo, ["config", "user.name", "mori-shokunin"])
    for path, body in files.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(body)
        if path.endswith(".sh"):
            os.chmod(full, 0o755)
    git(repo, ["add", "-A"])
    git(repo, ["commit", "-q", "-m", "fixture"])
    return repo, git(repo, ["rev-parse", "main"]).stdout.strip()


def _files(**over):
    entry = "corpus/knowledge/fixture-entry.md"
    files = {
        "corpus/SOURCES.md": "# SOURCES\n\n## Registry\n\n"
                             "| id | source | kind | tier | scope | anchor | teaches | status "
                             "| opened | recheck | used-by |\n"
                             "|---|---|---|---|---|---|---|---|---|---|---|\n"
                             + ROW_OK.format(row="S901", used=entry) + "\n",
        entry: ENTRY_OK.format(row="S901", cm="FR5"),
        "corpus/README.md": "# README\n\n## Frontier\n\n- fixture row names " + entry + "\n",
        "fixtures/fake-census.sh": CENSUS_OK,
    }
    files.update(over)
    return files


def selftest():
    arms, failures = [], []

    def arm(name, fn):
        try:
            fn()
            arms.append(name)
        except AssertionError as exc:
            failures.append("%s: %s" % (name, exc))
        except Exception as exc:                      # noqa: BLE001
            failures.append("%s: raised %s" % (name, exc))

    def run(files):
        tmp = tempfile.mkdtemp(prefix="c3st-")
        try:
            repo, rev = _mk(tmp, files)
            return evaluate(repo, rev, "corpus/knowledge/fixture-entry.md", ["S901"],
                            "FR5", "fixtures/fake-census.sh", "corpus/README.md", 60)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def honest():
        _c, fails = run(_files())
        assert not fails, fails

    def entry_absent():
        files = _files()
        files.pop("corpus/knowledge/fixture-entry.md")
        _c, fails = run(files)
        assert "entry_present" in fails, fails

    def row_unused():
        files = _files()
        files["corpus/SOURCES.md"] = files["corpus/SOURCES.md"].replace(
            "| corpus/knowledge/fixture-entry.md |", "| — |")
        _c, fails = run(files)
        assert "rows_present" in fails, fails

    def census_red():
        files = _files(**{"fixtures/fake-census.sh": CENSUS_RED})
        _c, fails = run(files)
        assert "census_ok" in fails, fails

    def readme_absent():
        files = _files(**{"corpus/README.md": "# README\n\nno map row\n"})
        _c, fails = run(files)
        assert "readme_row" in fails, fails

    def no_coverage_map():
        files = _files()
        files["corpus/knowledge/fixture-entry.md"] = (
            ENTRY_OK.format(row="S901", cm="FR5").replace("coverage-map: FR5", "ground: FR5"))
        _c, fails = run(files)
        assert "entry_meta" in fails, fails

    arm("registered_entry_met", honest)
    arm("absent_entry_unmet", entry_absent)
    arm("row_without_used_by_unmet", row_unused)
    arm("red_census_unmet", census_red)
    arm("readme_without_row_unmet", readme_absent)
    arm("missing_coverage_map_unmet", no_coverage_map)

    for name in arms:
        print("selftest PASS %s" % name)
    for name in failures:
        print("selftest FAIL %s" % name)
    print("C3_SELFTEST pass=%d fail=%d" % (len(arms), len(failures)))
    return 0 if not failures else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=repo_default())
    ap.add_argument("--entry", default="corpus/knowledge/pid-probe-conclusion-r44.md")
    ap.add_argument("--row", action="append", default=[])
    ap.add_argument("--coverage-map", default="FR5")
    ap.add_argument("--census", default=None)
    ap.add_argument("--readme", default="corpus/README.md")
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.rev or not args.row:
        print("usage: count-c3.py <rev|WORK> --entry PATH --row S### [--row S### ...] [--selftest]")
        return 2
    repo = os.path.abspath(args.repo)
    census = args.census or os.path.join(os.path.dirname(repo), "scripts", "sources-census.sh")
    rev = args.rev
    if rev != "WORK":
        resolved = git(repo, ["rev-parse", "--verify", rev + "^{commit}"])
        if resolved.returncode != 0:
            print("C3_SETUP cannot resolve revision %r" % rev)
            return 2
        rev = resolved.stdout.strip()
    try:
        checks, fails = evaluate(repo, rev, args.entry, args.row, args.coverage_map,
                                 census, args.readme, args.timeout)
    except Setup as exc:
        print("C3_SETUP %s" % exc)
        return 2
    for name, ok, detail in checks:
        print("check %-16s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    print("rev=%s" % rev)
    print("C3=%s" % ("unmet" if fails else "met"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
