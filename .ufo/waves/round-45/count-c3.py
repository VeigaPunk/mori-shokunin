#!/usr/bin/env python3
"""mori round-45 C3 — assimilation predicate counter (frozen instrument).

P-C3 (`.ufo/waves/round-45/contract.md`, Correction 1), measured in one run at
`--rev` with `--root <fleet root>` and `--entering-rev <round's entering tip>`:
  0. `--entry` and `--row` are both non-empty, and every `--entry` is **absent**
     at `--entering-rev` (`git cat-file -e REV:<entry>` fails): an entry that
     already existed at the entering tip is not this round's ground;
  1. every `--entry` exists and carries anchored `source:`, `verified-at:`,
     `recheck:` and `coverage-map:` lines;
  2. every `--row S###` is attributed to an entry by that entry's `source:`
     tokens, exists in `corpus/SOURCES.md`, is `mined`, and its `used-by` cell
     names every entry that declares it;
  3. `sources-census.sh validate --root <fleet root> mori` exits 0 with no
     `TMPDIR` override;
  4. `corpus/README.md`'s `## Coverage map` carries a row naming the entry;
  5. the census script invoked is pinned by sha256 in the verdict line.

Round-44 defects closed here: the census arm validates the lane through
`--root` instead of `--file` on a staged copy (`sources-census.sh:566` resolves
`used-by` against the lane directory, so a copy under `$TMPDIR` floods E11 —
the old run was green only when `TMPDIR` happened to be the repo root); every
entry is checked, not one; `source:` id lists, `coverage-map:` values, `used-by`
paths and README map rows compare whole tokens, never substrings; `git
rev-parse` runs inside the setup boundary; a timeout is `C3_SETUP`.

`--coverage-map` is a declared expectation: when given, each entry's
`coverage-map:` line must name at least one of the given values as a whole
token. The census arm reads the worktree registry by construction (its E11 rule
is a disk test); the entry, registry and README checks read the bytes at `--rev`.

Usage:
  python3 count-c3.py <rev|WORK> --entering-rev REV --entry PATH
                      [--entry PATH ...] --row S### [--row S### ...]
                      [--coverage-map FR# ...] [--repo PATH] [--root PATH]
                      [--census PATH] [--readme PATH] [--timeout S]
  python3 count-c3.py --selftest

Exit: 0 C3=met · 1 C3=unmet · 2 C3_SETUP (usage, unresolvable revision, timeout).
"""
import argparse
import contextlib
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "mori"
SOURCES = "corpus/SOURCES.md"
MAP_HEADING = "## Coverage map"

ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
FIELDS = re.compile(r"(?<!\\)\|")
TABLE_ROW = re.compile(r"^ {0,3}\|")
HEADING = re.compile(r"^ {0,3}#{1,2}[ \t]")
MAP_HEAD = re.compile(r"^ {0,3}##[ \t]+Coverage map\b")
SOURCE_LINE = re.compile(r"^source:[ \t]*(.*)$", re.M)
COVERAGE_LINE = re.compile(r"^coverage-map:[ \t]*(.*)$", re.M)
SOURCE_HEAD = re.compile(r"[ \t]*((?:S\d{3,}(?:[,/]?[ \t]*)?)+)")
ID_RE = re.compile(r"S\d{3,}")
MAP_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9._-]*")
FIELD_LINES = ("verified-at:", "recheck:")

# The counter's revision address must be authoritative: an inherited GIT_DIR or
# GIT_WORK_TREE would make `--repo` advisory.
GIT_ENV_KEYS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
                "GIT_NAMESPACE", "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES")


class Setup(Exception):
    pass


def git_env():
    return {k: v for k, v in os.environ.items() if k not in GIT_ENV_KEYS}


def repo_default():
    here = os.path.abspath(__file__)          # <repo>/.ufo/waves/round-45/count-c3.py
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
                              text=True, timeout=timeout, check=False,
                              env=git_env())
    except subprocess.TimeoutExpired:
        raise Setup("git timeout after %ss: git %s" % (timeout, " ".join(args)))


def resolve_rev(repo, rev, timeout):
    if rev == "WORK":
        return "WORK"
    out = git(repo, ["rev-parse", "--verify", rev + "^{commit}"], timeout)
    if out.returncode != 0:
        raise Setup("cannot resolve revision %r in %s" % (rev, repo))
    return out.stdout.strip()


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


def exists_at(repo, rev, path):
    """Existence at a revision, the `git cat-file -e REV:<path>` question."""
    if rev == "WORK":
        return os.path.isfile(os.path.join(repo, path))
    return git(repo, ["cat-file", "-e", "%s:%s" % (rev, path)]).returncode == 0


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


def entry_sources(text):
    """The id list at the head of each `source:` line, as whole tokens."""
    ids = []
    for m in SOURCE_LINE.finditer(text):
        head = SOURCE_HEAD.match(m.group(1))
        if not head:
            continue
        for tok in ID_RE.findall(head.group(1)):
            if tok not in ids:
                ids.append(tok)
    return ids


def coverage_value(text):
    m = COVERAGE_LINE.search(text)
    return None if m is None else m.group(1)


def entry_forms(entry):
    """The entry path as written, plus its corpus-relative spelling."""
    forms = {entry}
    if entry.startswith("corpus/"):
        forms.add(entry[len("corpus/"):])
    return forms


def names_entry(used, entry):
    """A `used-by` cell names the entry as a whole comma-separated path."""
    forms = entry_forms(entry)
    for part in used.split(","):
        cell = part.strip().strip("`").strip()
        if cell.startswith("./"):
            cell = cell[2:]
        if cell in forms:
            return True
    return False


def coverage_section(text):
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if MAP_HEAD.match(line):
            start = i + 1
            break
    if start is None:
        return None
    out = []
    for line in lines[start:]:
        if HEADING.match(line):
            break
        out.append(line)
    return "\n".join(out)


def map_row_names(section, entry):
    """A table row in the coverage map whose first cell is the entry."""
    forms = entry_forms(entry)
    for line in section.splitlines():
        if not TABLE_ROW.match(line):
            continue
        cells = [c.strip().strip("`").strip()
                 for c in FIELDS.split(line.strip().strip("|"))]
        if cells and cells[0] in forms:
            return True
    return False


def evaluate(repo, root, rev, entering, entries, rows, maps, census, readme, timeout):
    checks, fails = [], []

    def record(name, subject, ok, detail=""):
        checks.append((name, subject, ok, detail))
        if not ok:
            fails.append(name)

    record("entries_declared", "entries", bool(entries),
           "%d declared" % len(entries) if entries else "no --entry declared")
    record("rows_declared", "rows", bool(rows),
           "%d declared" % len(rows) if rows else "no --row declared")

    declared, texts, readme_section = {}, {}, None
    info = {"census_argv": ["bash", census, "validate", "--root", root, LANE],
            "census_sha256": "absent", "census_rc": None}

    for entry in entries:
        body = read_at(repo, rev, entry)
        record("entry_present", entry, body is not None,
               "absent" if body is None else "%d bytes" % len(body))
        was_there = exists_at(repo, entering, entry)
        record("entering_absent", entry, not was_there,
               "present at entering %s" % entering if was_there else
               "not in %s" % entering)
        texts[entry] = None if body is None else body.decode("utf-8", "replace")
        declared[entry] = entry_sources(texts[entry] or "")

    for entry, text in texts.items():
        if text is None:
            continue
        ids = declared[entry]
        missing = [f for f in FIELD_LINES
                   if not re.search(r"^" + re.escape(f), text, re.M)]
        cm = coverage_value(text)
        seen = set() if cm is None else set(MAP_TOKEN_RE.findall(cm))
        if cm is None:
            missing.append("coverage-map:")
        elif not seen:
            missing.append("coverage-map: names no value")
        elif maps and not seen.intersection(maps):
            missing.append("coverage-map: names none of %s" % ",".join(maps))
        if not ids:
            missing.append("source: names no id")
        if missing:
            detail = "; ".join(missing)
        else:
            matched = ",".join(sorted(seen.intersection(maps))) if maps else \
                cm.split("—")[0].strip()[:60]
            detail = "sources %s; map %s" % (",".join(ids), matched)
        record("entry_meta", entry, not missing, detail)

    if rows:
        subject = "rows=" + ",".join(rows)
        source_body = read_at(repo, rev, SOURCES)
        if source_body is None:
            record("rows_present", subject, False, "%s absent at %s" % (SOURCES, rev))
        else:
            table = census_rows(source_body.decode("utf-8", "replace"))
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
                    continue
                owners = [e for e in entries if rid in declared.get(e, [])]
                if not owners:
                    bad.append("%s declared by no entry" % rid)
                    continue
                for entry in owners:
                    if not names_entry(used, entry):
                        bad.append("%s used-by does not name %s" % (rid, entry))
            record("rows_present", subject, not bad,
                   "; ".join(bad) or "mined and named")

    if not os.path.isfile(census):
        record("census_ok", "census", False, "absent: %s" % census)
    else:
        with open(census, "rb") as fh:
            info["census_sha256"] = hashlib.sha256(fh.read()).hexdigest()
        try:
            proc = subprocess.run(info["census_argv"], capture_output=True,
                                  text=True, timeout=timeout, check=False, cwd=repo)
        except subprocess.TimeoutExpired:
            raise Setup("census timeout after %ss: %s" % (timeout, census))
        info["census_rc"] = proc.returncode
        findings = [l for l in proc.stdout.splitlines() if "\tE" in l][:3]
        tail = "".join("; " + l[:160] for l in findings)
        if proc.returncode != 0 and not findings:
            err = proc.stderr.strip().splitlines()
            tail = "; " + (err[0][:160] if err else "no stderr")
        record("census_ok", "census", proc.returncode == 0,
               "exit=%s%s" % (proc.returncode, tail))

    readme_body = read_at(repo, rev, readme)
    if readme_body is not None:
        readme_section = coverage_section(readme_body.decode("utf-8", "replace"))
    for entry in entries:
        if readme_body is None:
            record("readme_row", entry, False, "%s absent at %s" % (readme, rev))
        elif readme_section is None:
            record("readme_row", entry, False, "no `%s` section" % MAP_HEADING)
        else:
            found = map_row_names(readme_section, entry)
            record("readme_row", entry, found,
                   "map row names it" if found else "no map row names it")

    return checks, fails, info


# ---------------------------------------------------------------- --selftest ---

ENTRY = "corpus/knowledge/fixture-entry-r45.md"
ENTRY_B = "corpus/knowledge/fixture-other-r45.md"

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status "
          "| opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")

ROW_OK = ("| {row} | Fixture page — https://example.invalid/page | docs | A | fixture scope | "
          "section:1-2; opened 2026-10-25 | A fixture teaches cell. | {status} | 2026-10-25 | "
          "90d | {used} |\n")

ENTRY_BODY = """# Fixture entry

source: {sources} — https://example.invalid/page — quote
verified-at: 2026-10-25
recheck: 90d — `true` -> 1 (ran 2026-10-25)
coverage-map: {cm} — fixture frontier item

body
"""

# The fake census records the argv it was handed: the arm must be
# `validate --root <fleet> mori`, never `--file` on a staged copy.
CENSUS_OK = ('#!/bin/sh\nprintf \'%s\\n\' "$*" > "$(dirname "$0")/argv.txt"\nexit 0\n')
CENSUS_RED = ('#!/bin/sh\nprintf \'%s\\n\' "$*" > "$(dirname "$0")/argv.txt"\n'
              'printf \'mori\\tE11\\tS900 missing used-by corpus/knowledge/x.md\\n\'\n'
              'exit 1\n')


def _git(repo, args):
    out = subprocess.run(["git", "-C", repo] + args, capture_output=True,
                         text=True, timeout=60, check=False, env=git_env())
    if out.returncode != 0:
        raise AssertionError("git %s failed: %s" % (" ".join(args), out.stderr.strip()))
    return out


def _readme(rows_by_entry):
    lines = ["# README", "", MAP_HEADING, "", "| Note | Holds | Sources |", "|---|---|---|"]
    for entry, rows in rows_by_entry:
        lines.append("| `%s` | fixture holds | %s |"
                     % (entry[len("corpus/"):], ", ".join(rows)))
    return "\n".join(lines) + "\n"


def _fixture(base, tag, files, census=CENSUS_OK):
    """<base>/<tag>/fleet = fleet root, .../fleet/mori-shokunin = the lane repo.

    The first commit is the entering tip: it holds no entry, no registry row and
    no map row, so every entry in `files` is absent there.
    """
    fleet = os.path.join(base, tag, "fleet")
    repo = os.path.join(fleet, "mori-shokunin")
    scripts = os.path.join(fleet, "scripts")
    os.makedirs(repo)
    os.makedirs(scripts)
    with open(os.path.join(scripts, "sources-census.sh"), "w", encoding="utf-8") as fh:
        fh.write(census)
    os.chmod(os.path.join(scripts, "sources-census.sh"), 0o755)
    _git(repo, ["init", "-q", "-b", "main"])
    _git(repo, ["config", "user.email", "mori@shokunin.local"])
    _git(repo, ["config", "user.name", "mori-shokunin"])
    with open(os.path.join(repo, "ENTERING.md"), "w", encoding="utf-8") as fh:
        fh.write("# entering tip\n\nno entry, no registry row, no map row.\n")
    _git(repo, ["add", "-A"])
    _git(repo, ["commit", "-q", "-m", "entering"])
    entering = _git(repo, ["rev-parse", "main"]).stdout.strip()
    for path, body in files.items():
        full = os.path.join(repo, path)
        parent = os.path.dirname(full)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(body)
    _git(repo, ["add", "-A"])
    _git(repo, ["commit", "-q", "-m", "fixture"])
    return fleet, repo, _git(repo, ["rev-parse", "main"]).stdout.strip(), entering


def _files(**over):
    files = {
        SOURCES: "# SOURCES\n\n## Registry\n\n" + HEADER
                 + ROW_OK.format(row="S901", status="mined", used=ENTRY),
        ENTRY: ENTRY_BODY.format(sources="S901", cm="FR5"),
        "corpus/README.md": _readme([(ENTRY, ["S901"])]),
    }
    files.update(over)
    return files


def _run(fleet, repo, rev, entering, entries, rows, maps, readme="corpus/README.md"):
    return evaluate(repo, fleet, rev, entering, entries, rows, maps,
                    os.path.join(fleet, "scripts", "sources-census.sh"), readme, 60)


def _expect(fleet, repo, rev, entering, entries, rows, maps, want,
            readme="corpus/README.md"):
    checks, fails, info = _run(fleet, repo, rev, entering, entries, rows, maps, readme)
    if sorted(fails) != sorted(want):
        raise AssertionError("fails=%r want=%r checks=%r" % (fails, want, checks))
    return checks, info


def selftest():
    base = tempfile.mkdtemp(prefix="c3st-")
    arms, failures = [], []

    def arm(name, fn):
        try:
            fn()
            arms.append(name)
        except AssertionError as exc:
            failures.append("%s: %s" % (name, exc))
        except Exception as exc:                      # noqa: BLE001
            failures.append("%s: raised %s: %s" % (name, type(exc).__name__, exc))

    def census_argv(fleet):
        with open(os.path.join(fleet, "scripts", "argv.txt"), encoding="utf-8") as fh:
            return fh.read().strip()

    def registered_entry_met():
        fleet, repo, rev, entering = _fixture(base, "met", _files())
        checks, info = _expect(fleet, repo, rev, entering, [ENTRY], ["S901"], ["FR5"], [])
        want = " ".join(["validate", "--root", fleet, LANE])
        got = census_argv(fleet)
        assert got == want, "census argv %r != %r" % (got, want)
        assert "--file" not in got, got
        assert len(info["census_sha256"]) == 64, info

    def absent_entry_unmet():
        files = _files()
        files.pop(ENTRY)
        fleet, repo, rev, entering = _fixture(base, "absent", files)
        _expect(fleet, repo, rev, entering, [ENTRY], ["S901"], ["FR5"],
                ["entry_present", "rows_present"])

    def row_without_used_by_unmet():
        files = _files()
        files[SOURCES] = files[SOURCES].replace("| %s |" % ENTRY, "| — |")
        fleet, repo, rev, entering = _fixture(base, "noused", files)
        _expect(fleet, repo, rev, entering, [ENTRY], ["S901"], ["FR5"], ["rows_present"])

    def token_collision_row_unmet():
        # S4731 is not S473. The registry holds a mined S473 whose used-by names
        # the entry too, so a substring lookup would print a false C3=met; the
        # entry declares S4731 only, so S473 is attributed to no entry.
        files = _files()
        files[SOURCES] = (HEADER
                          + ROW_OK.format(row="S473", status="mined", used=ENTRY)
                          + ROW_OK.format(row="S4731", status="mined", used=ENTRY))
        files[ENTRY] = ENTRY_BODY.format(sources="S4731", cm="FR5")
        fleet, repo, rev, entering = _fixture(base, "toks", files)
        _expect(fleet, repo, rev, entering, [ENTRY], ["S473"], ["FR5"], ["rows_present"])

    def usedby_suffix_collision_unmet():
        files = _files()
        files[SOURCES] = files[SOURCES].replace(
            "| %s |" % ENTRY, "| %s.bak |" % ENTRY)
        fleet, repo, rev, entering = _fixture(base, "usedsuffix", files)
        _expect(fleet, repo, rev, entering, [ENTRY], ["S901"], ["FR5"], ["rows_present"])

    def coverage_token_collision_unmet():
        # FR1 must not be found inside FR13.
        files = _files()
        files[ENTRY] = ENTRY_BODY.format(sources="S901", cm="FR13")
        fleet, repo, rev, entering = _fixture(base, "covtok", files)
        _expect(fleet, repo, rev, entering, [ENTRY], ["S901"], ["FR1"], ["entry_meta"])

    def red_census_unmet():
        fleet, repo, rev, entering = _fixture(base, "red", _files(), census=CENSUS_RED)
        _expect(fleet, repo, rev, entering, [ENTRY], ["S901"], ["FR5"], ["census_ok"])

    def readme_without_map_row_unmet():
        # The round-44 overclaim: a prose mention anywhere in README is not a
        # coverage-map row.
        files = _files(**{"corpus/README.md":
                          "# README\n\nEntry: `%s` (S901).\n" % ENTRY})
        fleet, repo, rev, entering = _fixture(base, "readmeprose", files)
        _expect(fleet, repo, rev, entering, [ENTRY], ["S901"], ["FR5"], ["readme_row"])

    def readme_without_map_section_unmet():
        files = _files(**{"corpus/README.md":
                          "# README\n\n| Note | Holds |\n|---|---|\n| `%s` | x |\n"
                          % ENTRY[len("corpus/"):]})
        fleet, repo, rev, entering = _fixture(base, "readmenosec", files)
        _expect(fleet, repo, rev, entering, [ENTRY], ["S901"], ["FR5"], ["readme_row"])

    def missing_coverage_map_unmet():
        files = _files()
        files[ENTRY] = ENTRY_BODY.format(sources="S901", cm="FR5").replace(
            "coverage-map: FR5", "ground: FR5")
        fleet, repo, rev, entering = _fixture(base, "nocov", files)
        _expect(fleet, repo, rev, entering, [ENTRY], ["S901"], ["FR5"], ["entry_meta"])

    def multi_entry_met():
        files = _files()
        files[SOURCES] = (HEADER
                          + ROW_OK.format(row="S901", status="mined", used=ENTRY)
                          + ROW_OK.format(row="S902", status="mined", used=ENTRY_B))
        files[ENTRY_B] = ENTRY_BODY.format(sources="S902", cm="FR13")
        files["corpus/README.md"] = _readme([(ENTRY, ["S901"]), (ENTRY_B, ["S902"])])
        fleet, repo, rev, entering = _fixture(base, "multi", files)
        _expect(fleet, repo, rev, entering, [ENTRY, ENTRY_B], ["S901", "S902"],
                ["FR5", "FR13"], [])

    def multi_entry_row_missing_usedby_unmet():
        # Both entries declare S901; the cell names only the first.
        files = _files()
        files[ENTRY_B] = ENTRY_BODY.format(sources="S901", cm="FR5")
        files["corpus/README.md"] = _readme([(ENTRY, ["S901"]), (ENTRY_B, ["S901"])])
        fleet, repo, rev, entering = _fixture(base, "multiunused", files)
        checks, _info = _expect(fleet, repo, rev, entering, [ENTRY, ENTRY_B], ["S901"], [],
                                ["rows_present"])
        detail = [c for c in checks if c[0] == "rows_present"][0][3]
        assert ENTRY_B in detail, detail

    def cwd_tmpdir_independent_met():
        # The round-44 failure: the census arm was green only when TMPDIR was
        # the repo root. Nothing may be staged through TMPDIR now.
        fleet, repo, rev, entering = _fixture(base, "cwd", _files())
        decoy_tmp = os.path.join(base, "decoy-tmp")
        decoy_cwd = os.path.join(base, "decoy-cwd")
        os.makedirs(decoy_tmp)
        os.makedirs(decoy_cwd)
        before = os.environ.get("TMPDIR")
        cwd = os.getcwd()
        try:
            os.environ["TMPDIR"] = decoy_tmp
            os.chdir(decoy_cwd)
            _expect(fleet, repo, rev, entering, [ENTRY], ["S901"], ["FR5"], [])
        finally:
            os.chdir(cwd)
            if before is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = before
        assert os.listdir(decoy_tmp) == [], os.listdir(decoy_tmp)

    def red_census_ignores_tmpdir():
        # A red census stays red whatever TMPDIR says (no second mechanism).
        fleet, repo, rev, entering = _fixture(base, "redtmp", _files(), census=CENSUS_RED)
        before = os.environ.get("TMPDIR")
        try:
            os.environ["TMPDIR"] = repo
            _expect(fleet, repo, rev, entering, [ENTRY], ["S901"], ["FR5"], ["census_ok"])
        finally:
            if before is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = before

    def entering_present_unmet():
        # An entry that already existed at the entering tip is not this round's
        # ground: the measured revision is its own entering revision.
        fleet, repo, rev, _entering = _fixture(base, "entered", _files())
        _expect(fleet, repo, rev, rev, [ENTRY], ["S901"], ["FR5"], ["entering_absent"])

    def empty_rows_unmet():
        fleet, repo, rev, entering = _fixture(base, "norows", _files())
        _expect(fleet, repo, rev, entering, [ENTRY], [], ["FR5"], ["rows_declared"])

    def empty_entries_unmet():
        fleet, repo, rev, entering = _fixture(base, "noentries", _files())
        _expect(fleet, repo, rev, entering, [], ["S901"], [],
                ["entries_declared", "rows_present"])

    def unresolvable_revision_setup():
        fleet, repo, _rev, _entering = _fixture(base, "badrev", _files())
        for bogus in ("0123456789abcdef0123456789abcdef01234567",
                      "fedcba9876543210fedcba9876543210fedcba98"):
            try:
                resolve_rev(repo, bogus, 60)
            except Setup:
                continue
            raise AssertionError("resolve_rev accepted %r" % bogus)

    def usage_is_setup():
        quiet = io.StringIO()
        with contextlib.redirect_stdout(quiet):
            assert main([]) == 2, "empty argv did not return C3_SETUP"
            assert main(["WORK", "--entry", ENTRY, "--row", "S901"]) == 2, \
                "--entering-rev missing did not return C3_SETUP"

    arm("registered_entry_met", registered_entry_met)
    arm("absent_entry_unmet", absent_entry_unmet)
    arm("entering_present_unmet", entering_present_unmet)
    arm("row_without_used_by_unmet", row_without_used_by_unmet)
    arm("token_collision_row_unmet", token_collision_row_unmet)
    arm("usedby_suffix_collision_unmet", usedby_suffix_collision_unmet)
    arm("coverage_token_collision_unmet", coverage_token_collision_unmet)
    arm("red_census_unmet", red_census_unmet)
    arm("readme_without_map_row_unmet", readme_without_map_row_unmet)
    arm("readme_without_map_section_unmet", readme_without_map_section_unmet)
    arm("missing_coverage_map_unmet", missing_coverage_map_unmet)
    arm("multi_entry_met", multi_entry_met)
    arm("multi_entry_row_missing_usedby_unmet", multi_entry_row_missing_usedby_unmet)
    arm("empty_rows_unmet", empty_rows_unmet)
    arm("empty_entries_unmet", empty_entries_unmet)
    arm("cwd_tmpdir_independent_met", cwd_tmpdir_independent_met)
    arm("red_census_ignores_tmpdir", red_census_ignores_tmpdir)
    arm("unresolvable_revision_setup", unresolvable_revision_setup)
    arm("usage_is_setup", usage_is_setup)

    shutil.rmtree(base, ignore_errors=True)
    for name in arms:
        print("selftest PASS %s" % name)
    for name in failures:
        print("selftest FAIL %s" % name)
    print("C3_SELFTEST pass=%d fail=%d" % (len(arms), len(failures)))
    return 0 if not failures else 1


# ---------------------------------------------------------------------- main ---

def dedupe(values):
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def relative_entry(repo, entry):
    entry = entry.strip()
    if os.path.isabs(entry):
        full = os.path.abspath(entry)
        if full.startswith(repo + os.sep):
            return os.path.relpath(full, repo)
        return entry
    while entry.startswith("./"):
        entry = entry[2:]
    return entry


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("rev", nargs="?", help="revision to measure, or WORK")
    ap.add_argument("--entering-rev", default=None,
                    help="the round's entering tip; every --entry must be absent there")
    ap.add_argument("--repo", default=repo_default())
    ap.add_argument("--root", default=None, help="fleet root (default: dirname of --repo)")
    ap.add_argument("--entry", action="append", default=[],
                    help="admitted entry path; repeatable")
    ap.add_argument("--row", action="append", default=[],
                    help="declared registry id; repeatable")
    ap.add_argument("--coverage-map", action="append", default=[],
                    help="declared coverage-map value; repeatable")
    ap.add_argument("--census", default=None,
                    help="census script (default: <root>/scripts/sources-census.sh)")
    ap.add_argument("--readme", default="corpus/README.md")
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.rev or not args.entering_rev:
        print("usage: count-c3.py <rev|WORK> --entering-rev REV --entry PATH "
              "[--entry PATH ...] --row S### [--row S### ...] "
              "[--coverage-map FR# ...] [--repo PATH] [--root PATH] "
              "[--census PATH] [--readme PATH] [--timeout S]")
        print("       count-c3.py --selftest")
        return 2

    try:
        repo = os.path.abspath(args.repo)
        if not os.path.isdir(repo):
            raise Setup("repo not a directory: %s" % repo)
        root = os.path.abspath(args.root) if args.root else os.path.dirname(repo)
        if not os.path.isdir(root):
            raise Setup("root not a directory: %s" % root)
        census = args.census or os.path.join(root, "scripts", "sources-census.sh")
        rev = resolve_rev(repo, args.rev, args.timeout)
        entering = resolve_rev(repo, args.entering_rev, args.timeout)
        entries = dedupe([relative_entry(repo, e) for e in args.entry])
        rows = dedupe(args.row)
        checks, fails, info = evaluate(repo, root, rev, entering, entries, rows,
                                       dedupe(args.coverage_map), census,
                                       args.readme, args.timeout)
    except Setup as exc:
        print("C3_SETUP %s" % exc)
        return 2

    for name, subject, ok, detail in checks:
        print("check %-15s %s %s (%s)" % (name, subject, "PASS" if ok else "FAIL", detail))
    print("repo=%s" % repo)
    print("root=%s" % root)
    print("census_arm=%s" % " ".join(info["census_argv"]))
    print("C3=%s rev=%s entering=%s entries=%d rows=%s census_sha256=%s"
          % ("unmet" if fails else "met", rev, entering, len(entries), ",".join(rows),
             info["census_sha256"]))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
