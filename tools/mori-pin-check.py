#!/usr/bin/env python3
"""mori-pin-check — re-measure the self-test pins of SKILL.md's gate registry.

Round 47 (C1, calibration). Replaces round 46's row-wide substring counter
(`count-repins.py`), which turned green when a stale receipt string was moved
to another cell of the same row (`corpus/lessons/round-46.md` M1;
`corpus/lessons/round-46-verifier-spotcheck.md` routed defect 1).

v2 (round 47, after wave-1 seats CritC1Predicate and SentPinExec turned the
frozen v1 — freeze `63eecf27`, sha256 `e3ef425a…` — green on junk edits):
bound commands are restricted, a pin's command may not change from the
baseline, the pinned text must equal the observed text, rows are unique, a
short row naming `selftest` in any case is unparsed, and digest paths stay
inside the measured tree. The round-47 claim P-C1 is scored with the frozen
v1 bytes; v2 is the lane's standing tool.

What it reads
  Every Markdown table in SKILL.md whose header row has a cell named
  `self-test`. Cells are split on unescaped `|`; a data row whose cell count
  differs from its header's and that names `selftest` (any case) is
  `unparsed`; two parsed rows with one name are `duplicate`.
  Only the self-test cell is read for pins (the semantic cell):
    tally pin  — a backticked span that starts with `<PREFIX>SELFTEST`
                 (PREFIX = [A-Z0-9_]*), e.g. `C1_SELFTEST pass=16 fail=0`,
                 `X_SELFTEST: PASS (6 cases)`, `X_SELFTEST: PASS 12/12`.
                 The text after the prefix must carry a digit, else `unparsed`.
    digest pin — a full 64-hex token in the self-test cell; it must equal the
                 sha256 of at least one file path named anywhere in the row
                 that resolves inside the measured tree.

How it measures
  Each tally pin binds to the nearest preceding executable span in the same
  self-test cell: a span containing `--selftest` that starts with an
  interpreter (`python3`, `bash`, `sh`; leading `VAR=value` words dropped),
  or a bare `.py`/`.sh` path (e.g. a named mutant), run as
  `<interpreter> <path> --selftest`. A bound argv must be exactly
  `<python3|python|bash|sh> [-I] [-B] <path> [<rev>] --selftest` with
  `<path>` under `tools/` or `.ufo/waves/round-N/`, no `..`, no `.scratch/`;
  anything else (inline `-c` code, extra arguments) binds nothing.
  If the span is the bare `--selftest`,
  the command is the entry cell's first backticked span cut at its first `[`
  or `-` word, `<rev>`/`<REV>`/`<revision>` replaced by the measured
  revision, plus `--selftest`. No preceding span → `no_command`.
  The command runs (no shell) in the measured tree with TMPDIR set to a fresh
  directory under `<measured tree>/.scratch` (lane tools refuse a TMPDIR
  outside their own lane root); the text after the prefix on the last output
  line containing it must equal the pinned text exactly, and when the pin says
  `fail=0` the exit code must be 0.

Modes
  --rev REV [--repo DIR]   export REV with `git archive` and measure it there
                           (SKILL.md read from REV unless --skill is given)
  --root DIR               measure DIR as-is (selftest and fixtures)
  --skill PATH             read the registry from PATH instead
  --min-tally-pins N       floor on tally pins found (a deleted pin is not a fix)
  --baseline-rev REV       every (row name, pin prefix | sha256) key present in
                           SKILL.md at REV must still be present (`dropped=0`),
                           and each pin's bound argv must equal its argv at REV
                           (`rebound=0`); rows new since REV are not compared.

Output: one `pin line=… kind=… prefix=… state=… …` line per pin, then
  `PIN_CHECK=met|unmet tally_pins=N digest_pins=N mismatches=N unparsed=N
  no_command=N dropped=N rebound=N duplicate=N min_tally_pins=N rev=… baseline=yes|no`
Exit: 0 met · 1 unmet · 2 setup (usage, unresolvable revision, unreadable SKILL).
Read-only over committed bytes: with --rev it writes only its own export
under `<repo>/.scratch` (removed on exit); with --root it writes temp dirs
under `<root>/.scratch`. `--selftest` builds synthetic trees under TMPDIR.
"""
import argparse
import hashlib
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile

TIMEOUT_S = 600
HEX_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
PATH_RE = re.compile(r"[A-Za-z0-9_.][A-Za-z0-9_./-]*\.(?:py|sh|json|md|txt|tsv)")
SPAN_RE = re.compile(r"`([^`]*)`")
REV_WORDS = ("<rev>", "<REV>", "<revision>", "REV")
INTERPRETERS = ("python3", "python", "bash", "sh")
# v2 (round 47, after w1 CritC1Predicate/SentPinExec): a bound command must run a
# registered instrument path — `tools/…` or `.ufo/waves/round-N/…` — never `.scratch/`,
# never `..`, never inline code (`-c`), and carry no argument beyond an optional
# revision and `--selftest`.
SAFE_PATH = re.compile(r"(?:tools|\.ufo/waves/round-[0-9]+)/[A-Za-z0-9_./-]+\.(?:py|sh)")
PY_FLAGS = ("-I", "-B")


def argv_ok(argv, rev):
    if not argv or argv[0] not in INTERPRETERS:
        return False
    i = 1
    while i < len(argv) and argv[0].startswith("python") and argv[i] in PY_FLAGS:
        i += 1
    if i >= len(argv):
        return False
    path = argv[i]
    if (not SAFE_PATH.fullmatch(path) or ".." in path.split("/")
            or "/.scratch/" in "/" + path):
        return False
    rest = argv[i + 1:]
    return rest == ["--selftest"] or (rev is not None and rest == [rev, "--selftest"])


def split_cells(line):
    s = line.strip()
    if not s.startswith("|"):
        return None
    parts = re.split(r"(?<!\\)\|", s)
    if s.endswith("|") and not s.endswith("\\|"):
        parts = parts[1:-1]
    else:
        parts = parts[1:]
    return [p.strip() for p in parts]


def is_separator(cells):
    return all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells) if cells else False


def parse_registry(text):
    """Yield dicts: line, cells, header, idx, state ('ok'|'unparsed')."""
    rows = []
    header = None
    idx = None
    for n, line in enumerate(text.split("\n"), 1):
        cells = split_cells(line)
        if cells is None:
            header = None
            continue
        low = [c.lower() for c in cells]
        if "self-test" in low:
            header, idx = cells, low.index("self-test")
            continue
        if header is None or is_separator(cells):
            continue
        state = "ok" if len(cells) == len(header) else "unparsed"
        rows.append({"line": n, "cells": cells, "header": header, "idx": idx,
                     "state": state, "raw": line})
    return rows


def command_from_span(span, cells, rev):
    """Return argv for one backticked self-test-cell span, or None (v2: only
    argv that passes argv_ok)."""
    if "--selftest" not in span:
        argv = None
        if re.fullmatch(r"[A-Za-z0-9_.][A-Za-z0-9_./-]*\.py", span):
            argv = ["python3", span, "--selftest"]
        elif re.fullmatch(r"[A-Za-z0-9_.][A-Za-z0-9_./-]*\.sh", span):
            argv = ["bash", span, "--selftest"]
        return argv if argv is not None and argv_ok(argv, rev) else None
    argv = derive_command(span, cells, rev)
    return argv if argv is not None and argv_ok(argv, rev) else None


def pin_commands(cells, idx, rev):
    """Bind each tally pin in the self-test cell to the nearest preceding
    executable span: a `--selftest` command, or a bare `.py`/`.sh` path (a
    mutant named after the main command is run as `<interp> <path> --selftest`)."""
    st = cells[idx]
    bound = []
    current = None
    for m in SPAN_RE.finditer(st):
        span = m.group(1)
        pm = re.match(r"([A-Z][A-Z0-9_]*SELFTEST)(.*)$", span, re.S)
        if pm:
            bound.append((pm.group(1), pm.group(2), current))
            continue
        cmd = command_from_span(span, cells, rev)
        if cmd is not None:
            current = cmd
    return bound


def strip_env(words):
    while words and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", words[0]):
        words.pop(0)
    return words


def derive_command(span, cells, rev):
    """argv for a span containing `--selftest`; the bare flag borrows the entry cell."""
    try:
        words = strip_env(shlex.split(span))
    except ValueError:
        return None
    if words and words[0] in INTERPRETERS:
        return words
    if span.strip() != "--selftest":
        return None
    entry_spans = SPAN_RE.findall(cells[2] if len(cells) > 2 else "")
    if not entry_spans:
        return None
    ewords = []
    try:
        entry_words = shlex.split(entry_spans[0].replace("\\|", "|"))
    except ValueError:
        return None
    for w in entry_words:
        if w.startswith("[") or w.startswith("-"):
            break
        ewords.append(rev if (w in REV_WORDS and rev) else w)
    ewords = strip_env(ewords)
    if not ewords or ewords[0] not in INTERPRETERS or any(w.startswith("<") for w in ewords):
        return None
    return ewords + ["--selftest"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def run_cmd(words, root, scratch, timeout):
    # TMPDIR lives inside the measured tree (<root>/.scratch): lane tools such as
    # mori-round19-regressions.py refuse a TMPDIR outside their own lane root.
    tmp_parent = os.path.join(root, ".scratch")
    os.makedirs(tmp_parent, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="pin-tmp-", dir=tmp_parent)
    env = dict(os.environ, TMPDIR=tmp, PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run(words, cwd=root, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=timeout)
        return proc.returncode, proc.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return None, "timeout"
    except OSError as exc:
        return None, "oserror: %s" % exc
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def pin_keys(text):
    """Multiset {(row name, pin kind/prefix): count} over parsed rows — no commands run."""
    keys = {}
    for row in parse_registry(text):
        if row["state"] != "ok":
            continue
        st = row["cells"][row["idx"]]
        name = row["cells"][0]
        for m in SPAN_RE.finditer(st):
            pm = re.match(r"([A-Z][A-Z0-9_]*SELFTEST)", m.group(1))
            if pm:
                k = (name, pm.group(1))
                keys[k] = keys.get(k, 0) + 1
        for _ in HEX_RE.findall(st):
            k = (name, "sha256")
            keys[k] = keys.get(k, 0) + 1
    return keys

def pin_bindings(text, rev):
    """{(row name, prefix, ordinal): bound argv with the revision as `<REV>`}."""
    out = {}
    for row in parse_registry(text):
        if row["state"] != "ok":
            continue
        seen = {}
        for prefix, _pinned, words in pin_commands(row["cells"], row["idx"], rev):
            n = seen.get(prefix, 0)
            seen[prefix] = n + 1
            norm = None if words is None else tuple("<REV>" if w == rev else w for w in words)
            out[(row["cells"][0], prefix, n)] = norm
    return out


def check(text, root, scratch, rev, timeout, min_tally, baseline_text=None):
    out = []
    counts = {"tally_pins": 0, "digest_pins": 0, "mismatches": 0,
              "unparsed": 0, "no_command": 0, "dropped": 0, "rebound": 0,
              "duplicate": 0}
    base_bind = {}
    if baseline_text is not None:
        now = pin_keys(text)
        for k, n in sorted(pin_keys(baseline_text).items()):
            gone = n - now.get(k, 0)
            if gone > 0:
                counts["dropped"] += gone
                out.append("pin kind=baseline state=dropped row=%r pin=%s count=%d" % (k[0], k[1], gone))
        base_bind = pin_bindings(baseline_text, "<REV>")
    names = {}
    for row in parse_registry(text):
        if row["state"] == "ok":
            names[row["cells"][0]] = names.get(row["cells"][0], 0) + 1
    for name, n in sorted(names.items()):
        if n > 1:
            counts["duplicate"] += n - 1
            out.append("pin kind=row state=duplicate row=%r count=%d" % (name, n))
    cache = {}
    for row in parse_registry(text):
        line = row["line"]
        if row["state"] == "unparsed":
            if re.search(r"(?i)selftest", row["raw"]):
                counts["unparsed"] += 1
                out.append("pin line=%d kind=row state=unparsed cells=%d header=%d"
                           % (line, len(row["cells"]), len(row["header"])))
            continue
        cells, idx = row["cells"], row["idx"]
        st = cells[idx]
        ordinal = {}
        for prefix, pinned, words in pin_commands(cells, idx, rev):
            n = ordinal.get(prefix, 0)
            ordinal[prefix] = n + 1
            bkey = (cells[0], prefix, n)
            norm = None if words is None else tuple("<REV>" if w == rev else w for w in words)
            if bkey in base_bind and base_bind[bkey] is not None and norm != base_bind[bkey]:
                counts["rebound"] += 1
                out.append("pin line=%d kind=tally prefix=%s state=rebound baseline_cmd=%r cmd=%r"
                           % (line, prefix, " ".join(base_bind[bkey]),
                              " ".join(norm) if norm else None))
            counts["tally_pins"] += 1
            if not re.search(r"\d", pinned):
                counts["unparsed"] += 1
                out.append("pin line=%d kind=tally prefix=%s state=unparsed pinned=%r"
                           % (line, prefix, pinned))
                continue
            if words is None:
                counts["no_command"] += 1
                out.append("pin line=%d kind=tally prefix=%s state=no_command" % (line, prefix))
                continue
            key = tuple(words)
            if key not in cache:
                cache[key] = run_cmd(words, root, scratch, timeout)
            rc, text_out = cache[key]
            seen = [l for l in text_out.splitlines() if prefix in l]
            observed = seen[-1].split(prefix, 1)[1] if seen else None
            want = pinned.strip()
            # v2: the observed tail must equal the pinned text exactly (a weakened pin
            # such as `pass=22` for `pass=22 fail=0` is a mismatch).
            ok = observed is not None and observed.strip() == want
            if ok and re.search(r"\bfail=0\b", want) and rc != 0:
                ok = False
            if not ok:
                counts["mismatches"] += 1
            out.append("pin line=%d kind=tally prefix=%s state=%s pinned=%r observed=%r rc=%s cmd=%r"
                       % (line, prefix, "match" if ok else "mismatch", want,
                          (observed or "").strip()[:80] if observed is not None else None,
                          rc, " ".join(words)))
        for digest in HEX_RE.findall(st):
            counts["digest_pins"] += 1
            paths = sorted(set(PATH_RE.findall(row["raw"])))
            hit = None
            for p in paths:
                rel = os.path.normpath(p)
                if os.path.isabs(rel) or rel == ".." or rel.startswith(".." + os.sep):
                    continue
                fp = os.path.join(root, rel)
                if (os.path.realpath(fp).startswith(os.path.realpath(root) + os.sep)
                        and os.path.isfile(fp) and sha256_file(fp) == digest):
                    hit = rel
                    break
            if hit is None:
                counts["mismatches"] += 1
            out.append("pin line=%d kind=digest state=%s digest=%s file=%s"
                       % (line, "match" if hit else "mismatch", digest[:12], hit))
    met = (counts["mismatches"] == 0 and counts["unparsed"] == 0
           and counts["no_command"] == 0 and counts["dropped"] == 0
           and counts["rebound"] == 0 and counts["duplicate"] == 0
           and counts["tally_pins"] >= min_tally)
    out.append("PIN_CHECK=%s tally_pins=%d digest_pins=%d mismatches=%d unparsed=%d "
               "no_command=%d dropped=%d rebound=%d duplicate=%d min_tally_pins=%d rev=%s baseline=%s"
               % ("met" if met else "unmet", counts["tally_pins"], counts["digest_pins"],
                  counts["mismatches"], counts["unparsed"], counts["no_command"],
                  counts["dropped"], counts["rebound"], counts["duplicate"], min_tally, rev or "-",
                  "yes" if baseline_text is not None else "no"))
    return met, out


def export_rev(repo, rev, dest):
    try:
        full = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", rev + "^{commit}"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=60, check=True).stdout.decode().strip()
        arc = subprocess.run(["git", "-C", repo, "archive", "--format=tar", full],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=300, check=True).stdout
    except (subprocess.SubprocessError, OSError):
        return None
    tarpath = os.path.join(dest, "tree.tar")
    with open(tarpath, "wb") as f:
        f.write(arc)
    tree = os.path.join(dest, "tree")
    os.mkdir(tree)
    with tarfile.open(tarpath) as t:
        t.extractall(tree, filter="data")
    os.unlink(tarpath)
    return full, tree


def main(argv):
    ap = argparse.ArgumentParser(prog="mori-pin-check.py")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--rev")
    g.add_argument("--root")
    ap.add_argument("--repo", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--skill")
    ap.add_argument("--min-tally-pins", type=int, default=1)
    ap.add_argument("--baseline-rev", help="every pin key (row name, prefix) in SKILL.md at this "
                    "revision must still be present (a deleted pin is not a fix)")
    ap.add_argument("--timeout", type=int, default=TIMEOUT_S)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.rev and not args.root:
        print("PIN_CHECK_SETUP need --rev or --root", file=sys.stderr)
        return 2
    repo = os.path.abspath(args.repo)
    scratch_parent = os.path.join(repo, ".scratch")
    os.makedirs(scratch_parent, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="pin-check-", dir=scratch_parent)
    try:
        rev = None
        if args.rev:
            got = export_rev(repo, args.rev, scratch)
            if got is None:
                print("PIN_CHECK_SETUP unresolvable revision %s" % args.rev, file=sys.stderr)
                return 2
            rev, root = got
        else:
            root = os.path.abspath(args.root)
        skill = args.skill or os.path.join(root, "SKILL.md")
        try:
            with open(skill, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            print("PIN_CHECK_SETUP unreadable %s" % skill, file=sys.stderr)
            return 2
        baseline_text = None
        if args.baseline_rev:
            try:
                bp = subprocess.run(["git", "-C", repo, "show", args.baseline_rev + ":SKILL.md"],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            except (subprocess.SubprocessError, OSError):
                bp = None
            if bp is None or bp.returncode != 0:
                print("PIN_CHECK_SETUP unreadable baseline %s" % args.baseline_rev, file=sys.stderr)
                return 2
            baseline_text = bp.stdout.decode("utf-8", "replace")
        met, out = check(text, root, scratch, rev, args.timeout, args.min_tally_pins, baseline_text)
        print("\n".join(out))
        return 0 if met else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


# ---------------------------------------------------------------- selftest
HDR = "| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n|---|---|---|---|---|---|---|---|\n"
TOOL = ("import sys\n"
        "if '--selftest' in sys.argv:\n"
        "    print('noise line')\n"
        "    print('FOO_SELFTEST pass=3 fail=0')\n"
        "    sys.exit(int(open(__file__ + '.rc').read()) if __import__('os').path.exists(__file__ + '.rc') else 0)\n")
SLOW = "import time, sys\nif '--selftest' in sys.argv:\n    time.sleep(30)\n    print('SLOW_SELFTEST pass=1 fail=0')\n"
REVTOOL = ("import sys\n"
           "if len(sys.argv) == 3 and sys.argv[2] == '--selftest' and sys.argv[1] == 'deadbeef':\n"
           "    print('REV_SELFTEST: PASS (2 cases)')\n"
           "else:\n    print('REV_SELFTEST: FAIL'); sys.exit(1)\n")
MUT = "import sys\nif '--selftest' in sys.argv:\n    print('FOO_SELFTEST pass=2 fail=1'); sys.exit(1)\n"
TMPTOOL = ("import os, sys\n"
           "root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))\n"
           "t = os.path.realpath(os.environ.get('TMPDIR', '/'))\n"
           "if '--selftest' in sys.argv:\n"
           "    ok = t.startswith(root + os.sep)\n"
           "    print('TMP_SELFTEST pass=%d fail=%d' % (1 if ok else 0, 0 if ok else 1)); sys.exit(0 if ok else 1)\n")


def row(selftest_cell, entry="`python3 tools/foo.py`", pinned="none"):
    return "| foo | gate | %s | 0 ok | %s | %s | none | mori |\n" % (entry, selftest_cell, pinned)


def selftest():
    base = tempfile.mkdtemp(prefix="pin-selftest-")
    results = []
    try:
        root = os.path.join(base, "tree")
        os.makedirs(os.path.join(root, "tools"))
        with open(os.path.join(root, "tools", "foo.py"), "w") as f:
            f.write(TOOL)
        with open(os.path.join(root, "tools", "slow.py"), "w") as f:
            f.write(SLOW)
        with open(os.path.join(root, "tools", "rev.py"), "w") as f:
            f.write(REVTOOL)
        with open(os.path.join(root, "tools", "mut.py"), "w") as f:
            f.write(MUT)
        with open(os.path.join(root, "tools", "tmp.py"), "w") as f:
            f.write(TMPTOOL)
        digest = sha256_file(os.path.join(root, "tools", "foo.py"))
        good = "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`"
        mut_ok = good + "; the mutant `tools/mut.py` reads `FOO_SELFTEST pass=2 fail=1` rc 1"
        mut_bad = good + "; the mutant `tools/mut.py` reads `FOO_SELFTEST pass=3 fail=0`"
        cases = [
            ("honest", HDR + row(good), 1, True, None),
            ("stale_tally", HDR + row("`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=2 fail=0`"), 1, False, "mismatch"),
            ("stale_in_cell_true_elsewhere", HDR + row(
                "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=2 fail=0`",
                pinned="`FOO_SELFTEST pass=3 fail=0`"), 1, False, "mismatch"),
            ("pin_moved_out_of_cell", HDR + row("`python3 tools/foo.py --selftest`",
                                                pinned="`FOO_SELFTEST pass=3 fail=0`"), 1, False, None),
            ("digest_ok", HDR + row(good + " at sha256 `%s` of `tools/foo.py`" % digest), 1, True, None),
            ("digest_stale", HDR + row(good + " at sha256 `%s` of `tools/foo.py`" % ("0" * 64)), 1, False, "mismatch"),
            ("malformed_row", HDR + "| foo | gate | `python3 tools/foo.py` | %s | none | mori |\n" % good, 0, False, "unparsed"),
            ("no_command", HDR + row("`FOO_SELFTEST pass=3 fail=0`", entry="no command here"), 1, False, "no_command"),
            ("digitless_pin", HDR + row("`python3 tools/foo.py --selftest` → `FOO_SELFTEST: PASS`"), 1, False, "unparsed"),
            ("timeout", HDR + row("`python3 tools/slow.py --selftest` → `SLOW_SELFTEST pass=1 fail=0`",
                                  entry="`python3 tools/slow.py`"), 1, False, "mismatch"),
            ("bare_flag_rev_entry", HDR + row("`--selftest` → `REV_SELFTEST: PASS (2 cases)`",
                                              entry="`python3 tools/rev.py <rev> [--repo DIR]`"), 1, True, None),
            ("escaped_pipe_cell", HDR + row(good, entry="`python3 tools/foo.py --scope user\\|system`"), 1, True, None),
            ("below_floor", HDR + row(good), 2, False, None),
            ("mutant_pin_bound_to_mutant", HDR + row(mut_ok), 2, True, None),
            ("mutant_pin_wrong", HDR + row(mut_bad), 2, False, "mismatch"),
            ("tmpdir_inside_measured_tree", HDR + row("`python3 tools/tmp.py --selftest` → `TMP_SELFTEST pass=1 fail=0`",
                                                      entry="`python3 tools/tmp.py`"), 1, True, None),
        ]
        with open(os.path.join(root, "tools", "big.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('BIG_SELFTEST pass=33 fail=0')\n")
        cases.append(("token_boundary_truncated_pin", HDR + row(
            "`python3 tools/big.py --selftest` → `BIG_SELFTEST pass=3`", entry="`python3 tools/big.py`"),
            1, False, "mismatch"))
        two = HDR + row(good) + row(good).replace("| foo |", "| bar |", 1)
        cases.append(("baseline_row_deleted", (HDR + row(good), two), 1, False, "dropped"))
        cases.append(("baseline_all_present", (two, two), 1, True, None))
        # v2 arms — the w1 CritC1Predicate/SentPinExec false-green classes (each green under v1).
        stale = "`FOO_SELFTEST pass=2 fail=0`"
        os.makedirs(os.path.join(root, ".scratch", "old"))
        with open(os.path.join(root, ".scratch", "old", "foo.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('FOO_SELFTEST pass=2 fail=0')\n")
        with open(os.path.join(root, "tools", "old.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('FOO_SELFTEST pass=2 fail=0')\n")
        cases.append(("v2_inline_code_rejected", HDR + row(
            "`python3 -c \"print('FOO_SELFTEST pass=2 fail=0')\" --selftest` → " + stale,
            entry="no command here"), 1, False, "no_command"))
        cases.append(("v2_scratch_path_rejected", HDR + row(
            "`python3 .scratch/old/foo.py --selftest` → " + stale, entry="no command here"),
            1, False, "no_command"))
        cases.append(("v2_weakened_pin_exact", HDR + row(
            "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3`"), 1, False, "mismatch"))
        cases.append(("v2_rebound_to_other_tool", (HDR + row("`python3 tools/old.py --selftest` → " + stale),
                                                   HDR + row(good)), 1, False, "rebound"))
        cases.append(("v2_entry_rebound", (HDR + row("`--selftest` → " + stale, entry="`python3 tools/old.py`"),
                                           HDR + row("`--selftest` → `FOO_SELFTEST pass=3 fail=0`")),
                      1, False, "rebound"))
        hidden = ("| foo | gate | `python3 tools/foo.py` | 0 ok | `python3 tools/foo.py --selftest` → "
                  "`foo_selftest pass=2 fail=0` | none | mori |\n")
        cases.append(("v2_hidden_row_and_duplicate", (HDR + hidden + row(good) + row(good), HDR + row(good)),
                      1, False, "unparsed"))
        cases.append(("v2_duplicate_name", HDR + row(good) + row(good), 1, False, "duplicate"))
        with open(os.path.join(base, "outside.py"), "w") as f:
            f.write("x = 1\n")
        out_digest = sha256_file(os.path.join(base, "outside.py"))
        cases.append(("v2_digest_path_traversal", HDR + row(
            good + " at sha256 `%s` of `../outside.py`" % out_digest), 1, False, "mismatch"))
        for name, text, floor, want_met, want_state in cases:
            scratch = tempfile.mkdtemp(prefix="c-", dir=base)
            text, btext = text if isinstance(text, tuple) else (text, None)
            met, out = check(text, root, scratch, "deadbeef", 5, floor, btext)
            ok = met == want_met and (want_state is None or any("state=%s" % want_state in l for l in out))
            results.append((name, ok, out[-1]))
        # rc arm: tool prints the pinned tally but exits non-zero.
        with open(os.path.join(root, "tools", "foo.py.rc"), "w") as f:
            f.write("1")
        scratch = tempfile.mkdtemp(prefix="c-", dir=base)
        met, out = check(HDR + row(good), root, scratch, "deadbeef", 5, 1)
        results.append(("nonzero_rc_with_fail0", (not met) and any("state=mismatch" in l for l in out), out[-1]))
        os.unlink(os.path.join(root, "tools", "foo.py.rc"))
        # CLI arm: --root through main(), exit codes.
        with open(os.path.join(root, "SKILL.md"), "w") as f:
            f.write(HDR + row(good))
        cli = subprocess.run([sys.executable, os.path.abspath(__file__), "--root", root, "--repo", base],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        results.append(("cli_met_rc0", cli.returncode == 0 and b"PIN_CHECK=met" in cli.stdout, "rc=%d" % cli.returncode))
        cli2 = subprocess.run([sys.executable, os.path.abspath(__file__), "--rev", "no-such-rev", "--repo", base],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        results.append(("cli_bad_rev_rc2", cli2.returncode == 2, "rc=%d" % cli2.returncode))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    fails = 0
    for name, ok, last in results:
        print("%s %s  %s" % ("PASS" if ok else "FAIL", name, last))
        fails += 0 if ok else 1
    print("PIN_CHECK_SELFTEST pass=%d fail=%d" % (len(results) - fails, fails))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
