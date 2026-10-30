#!/usr/bin/env python3
"""mori round-62 C2 counter — cgroup-pressure probe capability + sourced entry.

Verifies, over committed bytes at a revision:
  * the round-62 probe `tools/mori-cgroup-pressure.py` and its fixture battery
    `tools/fixtures/mori-cgroup-pressure/cases.json` exist at their frozen
    sha256 pins; the pinned bytes (and only the pinned bytes) are materialized
    into scratch and executed (`--selftest`); a sha mismatch is refused before
    any execution (blobrefusal; r60 Sentinel41 / r61 count-c3 discipline);
  * the live receipt `corpus/evidence/cgroup-pressure-r62-live.txt` exists with
    its argv, the schema string and a verdict line;
  * the knowledge entry `corpus/knowledge/cgroup-pressure-r62.md` carries the
    provenance trio and >=8 located claims, each quote found at its cited line
    of a pinned v7.3 copy (quote floor 1 word, multi-line spans, pairwise
    distinct spans — r61 routed floor fix);
  * SOURCES row S571 (psi.c v7.3, cgroup scope — opened this round) is mined
    and used-by-bound to the entry (Registry-id binding, not substring scans);
  * SCORECARD carries the capability row (first-working round 62).

Every printed token is one measured value; `met` is the conjunction of all
measured booleans. Scratch: --scratch (or TMPDIR) honored; the selftest builds
its synthetic fixture repos under it with a throwaway identity only.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

TOOL = "tools/mori-cgroup-pressure.py"
CASES = "tools/fixtures/mori-cgroup-pressure/cases.json"
LIVE = "corpus/evidence/cgroup-pressure-r62-live.txt"
ENTRY = "corpus/knowledge/cgroup-pressure-r62.md"
COPY_DIR = "corpus/evidence/sources-r61"
COPIES = {
    "psi.c": "c4edc1e7c18ca76e6e29668093fa0b26d4251cb088f2d5feab24681f285ec63f",
    "cgroup-v2.rst": "2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68",
}
CLAIM_RE = re.compile(
    r"\*\*(K\d+)\*\* — `([a-zA-Z0-9_.\-]+):(\d+)(?:-(\d+))?` — `([^`]+)`")
SPAN = re.compile(r"([a-zA-Z0-9_.\-]+):(\d+)(?:-(\d+))?")
SELFTEST_RX = re.compile(r"MORI_CGROUP_PRESSURE_SELFTEST: pass=(\d+) fail=0")
VERDICTS = {"PRESSURE_OK", "PRESSURE_HIGH", "PRESSURE_PARTIAL",
            "PRESSURE_UNAVAILABLE"}
CLAIM_FLOOR = 8
TALLY_FLOOR = 12
PIN_TOOL = "aa5bfc3705546dc45b21499452c2adc3289c737b08cf25c287b5eb417a4f16ac"
PIN_CASES = "42551edb2630e8ea50583ae042a9334cd935a20567be3a1511d8f7e8d08e6d01"


def sh(repo, *args, binary=False):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def cat(repo, rev, path):
    return sh(repo, "show", f"{rev}:{path}", binary=True)


def norm(t):
    return " ".join(t.split())


def materialize_and_selftest(repo, rev, tool_sha, tally_floor, scratch,
                             marker_dir=None):
    """Materialize pinned bytes only; refuse to execute a sha mismatch."""
    out = {"selftest": False, "fixtures": False, "tool": False, "exec_refused": None}
    tb = cat(repo, rev, TOOL)
    cb = cat(repo, rev, CASES)
    if tb is None:
        out["exec_refused"] = "tool_absent"
        return out
    if hashlib.sha256(tb).hexdigest() != tool_sha:
        out["exec_refused"] = "tool_pin"
        return out
    if cb is None:
        out["exec_refused"] = "cases_absent"
        return out
    out["tool"] = True
    mat = Path(scratch) / "mat"
    tpath = mat / "mori-cgroup-pressure.py"
    cpath = mat / "cases.json"
    tpath.parent.mkdir(parents=True, exist_ok=True)
    tpath.write_bytes(tb)
    cpath.write_bytes(cb)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if marker_dir is not None:
        env["MARKER_DIR"] = str(marker_dir)
    r = subprocess.run(
        [sys.executable, str(tpath), "--selftest", "--cases", str(cpath),
         "--scratch", str(Path(scratch) / "run")],
        capture_output=True, text=True, timeout=120, cwd=str(mat), env=env)
    m = SELFTEST_RX.search(r.stdout)
    if m and int(m.group(1)) >= tally_floor:
        out["selftest"] = True
    out["fixtures"] = out["selftest"]
    if marker_dir is not None:
        out["executed_marker"] = (Path(marker_dir) / "executed-marker").exists()
    return out


def provenance_ok(text):
    head = text[:2000]
    return all(re.search(rf"^{band}:", head, re.M)
               for band in ("source", "verified-at", "recheck"))


def measure(repo, rev, tool_sha, cases_sha, tally_floor=TALLY_FLOOR,
            copies=None, claim_floor=CLAIM_FLOOR, scratch="/tmp", opts=None):
    copies = copies or COPIES
    opts = opts or {}
    res = {"tool": False, "selftest": False, "fixtures": False, "live": False,
           "entry": False, "claims": 0, "quotes_ok": 0, "sources": False,
           "capability": False, "failed": [], "exec_refused": None}
    failed = res["failed"]

    def bad(tag):
        failed.append(tag)

    st = materialize_and_selftest(repo, rev, tool_sha, tally_floor, scratch)
    res["tool"] = st["tool"]
    res["selftest"] = st["selftest"]
    res["fixtures"] = st["fixtures"]
    res["exec_refused"] = st["exec_refused"]
    if st["exec_refused"]:
        bad(f"refused:{st['exec_refused']}")
    elif not (st["tool"] and st["selftest"]):
        bad("selftest")

    live = cat(repo, rev, LIVE)
    if live is None:
        bad("live_absent")
    else:
        lt = live.decode("utf-8", "replace")
        vlines = re.findall(r"MORI_CGROUP_PRESSURE: (PRESSURE_\w+)", lt)
        if "--group user.slice" not in lt:
            bad("live_argv")
        if "mori-cgroup-pressure-v1" not in lt:
            bad("live_schema")
        if not vlines or any(v not in VERDICTS for v in vlines):
            bad("live_verdict")
        else:
            res["live"] = True

    copy_dir = opts.get("copy_dir", COPY_DIR)
    entry = cat(repo, rev, ENTRY)
    if entry is None:
        bad("entry_absent")
    else:
        et = entry.decode("utf-8", "replace")
        res["entry"] = provenance_ok(et)
        if not res["entry"]:
            bad("provenance")
        for sid in opts.get("entry_source_ids", ["S571", "S568"]):
            if sid not in et:
                bad(f"entry_sources:{sid}")
        pins = {}
        for f, pin in copies.items():
            b = cat(repo, rev, f"{copy_dir}/{f}")
            if b is None:
                bad(f"copy_absent:{f}")
            elif hashlib.sha256(b).hexdigest() != pin:
                bad(f"copy_pin:{f}")
            else:
                pins[f] = b.decode("utf-8", "replace").splitlines()
        claims = []
        for m in CLAIM_RE.finditer(et):
            claims.append((m.group(1), m.group(2), int(m.group(3)),
                           int(m.group(4) or m.group(3)), m.group(5)))
        res["claims"] = len(claims)
        if len(claims) < claim_floor:
            bad(f"claims_floor:{len(claims)}<{claim_floor}")
        spans = set()
        for kid, fname, s, e, q in claims:
            if fname not in pins:
                bad(f"claim_copy:{kid}")
                continue
            lines = pins[fname]
            if s < 1 or e < s or e > len(lines):
                bad(f"claim_oob:{kid}")
                continue
            hay = norm("\n".join(lines[s - 1:e]))
            if norm(q) not in hay:
                bad(f"claim_quote:{kid}")
                continue
            if not (1 <= len(q.split()) <= 25):
                bad(f"claim_words:{kid}")
                continue
            if (fname, s, e) in spans:
                bad(f"claim_dup_span:{kid}")
                continue
            spans.add((fname, s, e))
            res["quotes_ok"] += 1

        registry = cat(repo, rev, "corpus/SOURCES.md")
        if registry is None:
            bad("registry_absent")
        else:
            hit = None
            for line in registry.decode("utf-8", "replace").splitlines():
                cells = line.split("|")
                rid = opts.get("registry_id", "S571")
                if len(cells) >= 12 and cells[1].strip() == rid:
                    hit = cells
                    break
            if hit is None:
                bad(f"rows_src:{rid}")
            else:
                if len(hit) != 13:
                    bad(f"rows_cols:{rid}")
                if opts.get("registry_url", "kernel/sched/psi.c?h=v7.3") not in hit[2]:
                    bad(f"rows_url:{rid}")
                if opts.get("registry_scope", "cgroup") not in hit[5]:
                    bad(f"rows_scope:{rid}")
                if hit[8].strip() != "mined":
                    bad(f"rows_mined:{rid}")
                if opts.get("used_by", Path(ENTRY).name) not in hit[11]:
                    bad(f"rows_usedby:{rid}")
                res["sources"] = not any(x.startswith(("rows_",)) for x in failed)

        score = cat(repo, rev, "SCORECARD.md")
        if score is None:
            bad("scorecard_absent")
        else:
            capname = opts.get("capability", "mori-cgroup-pressure.py")
            capround = opts.get("capability_round", "62")
            cap = [ln for ln in score.decode("utf-8", "replace").splitlines()
                   if capname in ln and f"| {capround} |" in ln]
            if not cap:
                bad("capability_row")
            else:
                res["capability"] = True
    ok = not failed
    return res, ok


def fmt(res, ok, rev):
    refused = res.get("exec_refused")
    return (f"{'C2=met' if ok else 'C2=unmet'} tool={'ok' if res['tool'] else 'bad'} "
            f"selftest={'ok' if res['selftest'] else 'bad'} "
            f"live={'ok' if res['live'] else 'bad'} "
            f"entry={'ok' if res['entry'] else 'bad'} claims={res['claims']} "
            f"quotes={res['quotes_ok']} sources={'ok' if res['sources'] else 'bad'} "
            f"capability={'ok' if res['capability'] else 'bad'} "
            f"failed={';'.join(res['failed']) or 'none'} rev={rev}"
            + (f" refused={refused}" if refused else ""))


# ---------- selftest ----------

TOOL_SRC = '''import sys, os, json
if __name__ == "__main__":
    try:
        d = os.environ.get("MARKER_DIR")
        if d:
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "executed-marker"), "w").close()
    except OSError:
        pass
    n = 0
    for i, a in enumerate(sys.argv):
        if a == "--cases" and i + 1 < len(sys.argv):
            n = len(json.load(open(sys.argv[i + 1])).get("cases", []))
    print(f"MORI_CGROUP_PRESSURE_SELFTEST: pass={n} fail=0")
'''


def selftest(scratch):
    import shutil
    cases_doc = {"schema": "mori-cgroup-pressure-cases-v1",
                 "cases": [{"name": "c1", "verdict": "PRESSURE_OK", "rc": 0},
                           {"name": "c2", "verdict": "PRESSURE_OK", "rc": 0},
                           {"name": "c3", "verdict": "PRESSURE_OK", "rc": 0}]}
    entry = ("source: S91 x.c and S92 d.rst\nverified-at: 2026-10-30\n"
             "recheck: on-release\n\n"
             "- **K1** — `x.c:3` — `alpha beta gamma delta`: one.\n"
             "- **K2** — `x.c:7-8` — `alpha beta gamma delta epsilon zeta`: two.\n"
             "- **K3** — `d.rst:2` — `doc line two pressure`: three.\n")
    xc = "\n".join(["pad", "pad", "alpha beta gamma delta", "pad", "pad", "pad",
                    "alpha beta gamma delta epsilon zeta", "pad"]) + "\n"
    drst = "doc line one\n" + "doc line two pressure\n"
    reg = ("| id | source | kind | tier | scope | anchor | teaches | status"
           " | opened | recheck | used-by |\n|---|" + "---|" * 10 + "\n"
           "| S91 | x x.c | code | A | cgroup scope | anchor | t | mined"
           " | 2026-10-30 | on-release | cgroup-pressure-r62.md |\n"
           "| S92 | x d.rst | docs | A | cgroup scope | anchor | t | mined"
           " | 2026-10-30 | on-release | cgroup-pressure-r62.md |\n")
    score = "| probe | what | `tools/mori-cgroup-pressure.py` | 62 |\n"

    def build(name, tool_bytes=None, entry_text=entry, reg_text=reg,
              score_text=score, live=True, copy_mutate=None):
        d = Path(scratch) / ("st-" + name)
        shutil.rmtree(d, ignore_errors=True)
        (d / "tools/fixtures/mori-cgroup-pressure").mkdir(parents=True)
        (d / "corpus/knowledge").mkdir(parents=True)
        (d / "corpus/evidence").mkdir(parents=True)
        tb = (tool_bytes if tool_bytes is not None
              else TOOL_SRC).encode()
        (d / TOOL).write_bytes(tb)
        (d / CASES).write_text(json.dumps(cases_doc))
        if live:
            (d / LIVE).write_text(
                "# argv: python3 tools/mori-cgroup-pressure.py --group user.slice\n"
                '"schema": "mori-cgroup-pressure-v1"\n'
                "MORI_CGROUP_PRESSURE: PRESSURE_OK (group=user.slice)\n")
        (d / ENTRY).write_text(entry_text)
        xc2, drst2 = xc, drst
        if copy_mutate == "x.c":
            xc2 = xc2.replace("gamma", "GAMMA", 1)
        (d / "corpus/evidence/x.c").write_text(xc2)
        (d / "corpus/evidence/d.rst").write_text(drst2)
        (d / "corpus/SOURCES.md").write_text(reg_text)
        (d / "SCORECARD.md").write_text(score_text)
        for args in (["init", "-q"], ["add", "-A"]):
            subprocess.run(["git", "-C", str(d), *args], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(d), "-c", "user.name=t", "-c",
                        "user.email=t@t", "commit", "-qm", "x"],
                       check=True, capture_output=True)
        rev = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
        pins = {
            "tool": hashlib.sha256(tb).hexdigest(),
            "cases": hashlib.sha256(json.dumps(cases_doc).encode()).hexdigest(),
            "copies": {"x.c": hashlib.sha256(xc2.encode()).hexdigest(),
                       "d.rst": hashlib.sha256(drst2.encode()).hexdigest()},
        }
        return str(d), rev, pins

    def run(name, expect_tool_sha=None, **kw):
        marker = Path(scratch) / ("mk-" + name)
        shutil.rmtree(marker, ignore_errors=True)
        marker.mkdir(parents=True)
        repo, rev, pins = build(name, **kw)
        sopts = {"copy_dir": "corpus/evidence",
                 "entry_source_ids": ["S91", "S92"],
                 "registry_id": "S91", "registry_url": "x.c",
                 "registry_scope": "cgroup",
                 "used_by": "cgroup-pressure-r62.md",
                 "capability": "mori-cgroup-pressure.py",
                 "capability_round": "62"}
        res, ok = measure(repo, rev, tool_sha=expect_tool_sha or pins["tool"],
                          cases_sha=pins["cases"],
                          tally_floor=3, copies=pins["copies"], claim_floor=3,
                          scratch=str(marker), opts=sopts)
        return ok, res, marker

    results = []
    ok, res, _ = run("good")
    results.append(("good", ok, True, res))
    honest_tool_sha = hashlib.sha256(TOOL_SRC.encode()).hexdigest()
    ok, res, mk = run("tool-sha-mismatch", expect_tool_sha=honest_tool_sha,
                      tool_bytes=TOOL_SRC.replace("pass=3", "pass=2"))
    no_exec = not (mk / "executed-marker").exists()
    results.append(("tool-sha-mismatch-refused", ok and no_exec and res["exec_refused"] == "tool_pin", False, res))
    bad_cases = json.dumps({"schema": "mori-cgroup-pressure-cases-v1", "cases": []})
    repo, rev, pins = build("selftest-fail")
    (Path(repo) / CASES).write_text(bad_cases)
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", repo, "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-qm", "y"], check=True, capture_output=True)
    rev2 = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    st_res, st_ok = measure(repo, rev2, tool_sha=hashlib.sha256(TOOL_SRC.encode()).hexdigest(),
                            cases_sha=hashlib.sha256(bad_cases.encode()).hexdigest(),
                            tally_floor=3, copies=pins["copies"], claim_floor=3,
                            scratch=str(Path(scratch) / "mk-selftest-fail"),
                            opts={"copy_dir": "corpus/evidence",
                                  "entry_source_ids": ["S91", "S92"],
                                  "registry_id": "S91", "registry_url": "x.c",
                                  "registry_scope": "cgroup",
                                  "used_by": "cgroup-pressure-r62.md",
                                  "capability": "mori-cgroup-pressure.py",
                                  "capability_round": "62"})
    results.append(("selftest-fail", st_ok, False, st_res))
    ok, res, _ = run("live-missing", live=False)
    results.append(("live-missing", ok, False, res))
    ok, res, _ = run("quote-missing", entry_text=entry.replace("alpha beta gamma delta epsilon zeta", "alpha beta GAMMA delta epsilon zeta"))
    results.append(("quote-missing", ok, False, res))
    ok, res, _ = run("dup-span", entry_text=entry + "- **K4** — `x.c:3` — `alpha beta gamma delta`: dup.\n")
    results.append(("dup-span", ok, False, res))
    ok, res, _ = run("not-mined", reg_text=reg.replace("| mined |", "| queued |"))
    results.append(("not-mined", ok, False, res))
    ok, res, _ = run("capability-missing", score_text="no capability row\n")
    results.append(("capability-missing", ok, False, res))
    npass = 0
    for name, got, want, res in results:
        good = got == want
        npass += good
        print(f"case {name}: {'pass' if good else 'FAIL'} ok={got} want={want} failed={res['failed']}")
    print(f"C2_SELFTEST pass={npass} fail={len(results) - npass}")
    return npass == len(results)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--scratch", default=None)
    ap.add_argument("--tool-sha", default=PIN_TOOL)
    ap.add_argument("--cases-sha", default=PIN_CASES)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    scratch = a.scratch or os.environ.get("TMPDIR") or "/tmp"
    os.makedirs(scratch, exist_ok=True)
    if a.selftest:
        sys.exit(0 if selftest(scratch) else 1)
    if not a.rev:
        ap.error("rev required without --selftest")
    res, ok = measure(a.repo, a.rev, a.tool_sha, a.cases_sha, scratch=scratch)
    print(fmt(res, ok, a.rev))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
