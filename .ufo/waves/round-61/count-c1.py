#!/usr/bin/env python3
"""mori round-61 C1 counter — gate-registry completeness for rounds 52-60.

Checks, at a measured revision, that every gate path in the committed manifest
has exactly one conformant, non-superseded row in the lane's SKILL.md
gate-registry tables (header: name | kind | entry | verdict map | self-test |
pinned values | write scope | owner), whose entry path resolves at that
revision and whose self-test cell names a --selftest command.

Read-only over the measured repo: materializes SKILL.md, the manifest and each
entry path via `git show` / `git cat-file -e`. Honors TMPDIR; --scratch must
be a writable directory.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HEADER_CELLS = ["name", "kind", "entry", "verdict map", "self-test",
                "pinned values", "write scope", "owner"]
MANIFEST_DEFAULT = ".ufo/waves/round-61/gate-manifest.json"
SKILL = "SKILL.md"
CELLS = ["name", "kind", "entry", "verdict", "selftest", "pinned", "scope",
         "owner"]


def sh(repo, *args, binary=False):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def cat(repo, rev, path):
    return sh(repo, "show", f"{rev}:{path}", binary=True)


def parse_tables(skill_md):
    """Rows from every gate-registry-shaped table in the file."""
    rows, lines = [], skill_md.splitlines()
    i = 0
    while i < len(lines):
        cells = [c.strip().lower() for c in
                 lines[i].strip().strip("|").split("|")]
        if cells == HEADER_CELLS:
            i += 2  # skip the |---| separator
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                raw = [c.strip() for c in
                       lines[i].strip().strip("|").split("|")]
                if len(raw) == len(CELLS):
                    row = dict(zip(CELLS, raw))
                    row["_line"] = i + 1
                    rows.append(row)
                i += 1
        else:
            i += 1
    return rows


def row_hits(rows, path):
    """Rows whose entry cell names the path (backticks stripped)."""
    hits = []
    for r in rows:
        toks = [t.strip().strip("`") for t in r["entry"].replace("(", " ")
                .replace(")", " ").replace(",", " ").split()]
        if path in toks or path in r["entry"]:
            hits.append(r)
    return hits


def measure(repo, rev, manifest_bytes):
    res = {"gates": 0, "registered": 0, "missing": 0, "thin": 0, "dup": 0,
           "unres": 0, "noselftest": 0, "noowner": 0, "failed": []}
    skill = cat(repo, rev, SKILL)
    if skill is None:
        res["failed"].append("skill_absent")
        return res, False
    rows = parse_tables(skill.decode("utf-8", "replace"))
    try:
        man = json.loads(manifest_bytes.decode())
        gates = [g["path"] if isinstance(g, dict) else g for g in man]
    except Exception:
        res["failed"].append("manifest_unreadable")
        return res, False
    res["gates"] = len(gates)
    if res["gates"] == 0:
        res["failed"].append("manifest_empty")
    for path in gates:
        hits = row_hits(rows, path)
        if not hits:
            res["missing"] += 1
            res["failed"].append("missing:%s" % path)
            continue
        live = [r for r in hits
                if "supersed" not in r["name"].lower()
                and "supersed" not in r["scope"].lower()]
        if len(live) > 1:
            res["dup"] += 1
            res["failed"].append("dup:%s" % path)
            continue
        row = live[0] if live else hits[0]
        empty = [k for k in CELLS if not row[k]]
        if empty:
            res["thin"] += 1
            res["failed"].append("thin:%s:%s" % (path, ",".join(empty)))
            continue
        if "--selftest" not in row["selftest"]:
            res["noselftest"] += 1
            res["failed"].append("noselftest:%s" % path)
            continue
        if cat(repo, rev, path) is None:
            res["unres"] += 1
            res["failed"].append("unres:%s" % path)
            continue
        res["registered"] += 1
    ok = (res["gates"] > 0 and res["registered"] == res["gates"]
          and not res["failed"])
    return res, ok


def fmt(res, ok, rev):
    return (f"{'C1=met' if ok else 'C1=unmet'} gates={res['gates']} "
            f"registered={res['registered']} missing={res['missing']} "
            f"thin={res['thin']} dup={res['dup']} unres={res['unres']} "
            f"noselftest={res['noselftest']} noowner={res['noowner']} "
            f"failed={','.join(res['failed']) or 'none'} rev={rev}")


# ---------- selftest ----------

def table(*rows):
    hdr = ("| name | kind | entry | verdict map | self-test | pinned values"
           " | write scope | owner |\n|---|" + "---|" * 7)
    return hdr + "\n" + "\n".join(rows) + "\n"


GOOD = ("| r61 t (C1) | gate | `tools/g.py` (`--x`) | 0 met · 1 unmet | "
        "`python3 tools/g.py --selftest` → pass=1 | sha 00 | read-only | MoriR61 |")
THIN = ("| r61 t (C2) | gate | `tools/h.py` | 0 met | "
        "`python3 tools/h.py --selftest` | sha 00 | read-only |  |")
NOSF = ("| r61 t (C3) | gate | `tools/i.py` | 0 met | runs by hand | sha 00 |"
        " read-only | MoriR61 |")
SUP = ("| r61 t (C4) | gate | `tools/j.py` | 0 met | "
       "`python3 tools/j.py --selftest` | sha 00 | superseded: see next row |"
       " MoriR61 |")
SUP2 = SUP.replace("(C4)", "(C4b)")

CASES = [
    # (name, table rows, manifest paths, expect met)
    ("good", [GOOD], ["tools/g.py"], True),
    ("missing", [GOOD], ["tools/g.py", "tools/absent.py"], False),
    ("thin", [GOOD, THIN], ["tools/h.py"], False),
    ("noselftest", [NOSF], ["tools/i.py"], False),
    ("superseded-ok", [SUP, SUP2], ["tools/j.py"], True),
    ("unres", [GOOD], ["tools/nothere.py"], False),
]


def selftest(scratch):
    npass = 0
    import shutil
    for name, rows, paths, want in CASES:
        d = Path(scratch) / ("st-" + name)
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True, exist_ok=True)
        (d / SKILL).write_text(table(*rows))
        mp = d / MANIFEST_DEFAULT
        mp.parent.mkdir(parents=True, exist_ok=True)
        mp.write_text(json.dumps(
            [{"path": p, "round": 61, "landing": "0" * 40} for p in paths]))
        for tool in ("g", "h", "i", "j"):
            t = d / "tools" / f"{tool}.py"
            t.parent.mkdir(parents=True, exist_ok=True)
            t.write_text("import sys\nsys.exit(0)\n")
        for args in (["init", "-q"], ["add", "-A"]):
            subprocess.run(["git", "-C", str(d), *args], check=True,
                           capture_output=True)
        subprocess.run(["git", "-C", str(d), "-c", "user.name=t", "-c",
                        "user.email=t@t", "commit", "-qm", "x"],
                       check=True, capture_output=True)
        rev = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
        res, ok = measure(str(d), rev, mp.read_bytes())
        good = ok == want
        npass += good
        print(f"case {name}: ok={ok} want={want} "
              f"{'pass' if good else 'FAIL'} failed={res['failed']}")
    print(f"C1_SELFTEST pass={npass} fail={len(CASES) - npass}")
    return npass == len(CASES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--scratch", default=None)
    ap.add_argument("--manifest", default=MANIFEST_DEFAULT)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    scratch = a.scratch or os.environ.get("TMPDIR") or "/tmp"
    os.makedirs(scratch, exist_ok=True)
    if a.selftest:
        sys.exit(0 if selftest(scratch) else 1)
    if not a.rev:
        ap.error("rev required without --selftest")
    if os.path.isabs(a.manifest) and os.path.isfile(a.manifest):
        data = Path(a.manifest).read_bytes()
    else:
        data = cat(a.repo, a.rev, a.manifest)
    if data is None:
        res = {"gates": 0, "registered": 0, "missing": 0, "thin": 0, "dup": 0,
               "unres": 0, "noselftest": 0, "noowner": 0,
               "failed": ["manifest_unreadable"]}
        ok = False
    else:
        res, ok = measure(a.repo, a.rev, data)
    print(fmt(res, ok, a.rev))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
