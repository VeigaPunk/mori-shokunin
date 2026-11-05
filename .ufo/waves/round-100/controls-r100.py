#!/usr/bin/env python3
"""Round-100 pre-freeze controls: build each control tree from the entering revision, score it with the
frozen counters, and print `<id> expect=<verdict> got=<verdict> AS_EXPECTED|UNEXPECTED` plus the counter line.

C1 (count-c1.py --seed SEED):
  K0  do-nothing (entering tree)                                  expect unmet
  K1  blanket forgery: every non-quota/non-rate death -> dead_auth expect unmet (N3/N5)
  K2  status-only: no auth spellings                               expect unmet (A2/A3/A5)
  K3  spelling-only: no 401/403 status rule                        expect unmet (A1/A4)
  K4  auth read before quota/rate (precedence flipped)             expect unmet (N1/N2)
  K5  template-lookup forgery: dead_auth iff the message contains one of the counter's fixed A1/A2
      template fragments (no status rule, no spelling rule)        expect unmet (A4/A5)
  K6  candidate without knowledge entry and rows                   expect unmet (sourced)
  K7  candidate tool, round-17 gate not updated                    expect unmet (r17gate)
  K8  candidate without the SKILL.md row edits                     expect unmet (registry)
  P1  full candidate                                               expect met
C2 (count-c2.py):
  K0c do-nothing                                                   expect unmet (mismatch)
  K1c delete the stated counts of mismatched rows                  expect unmet (altered)
  K2c correction text with wrong numbers (K->K)                    expect unmet (mismatch)
  K3c blanket correction on every row with a stated count          expect unmet (spurious)
  K4c rewrite stated numbers in place                              expect unmet (altered)
  K5c correction appended to the wrong row                         expect unmet (mismatch, spurious)
  P2  apply-c2.py                                                  expect met
Usage: controls-r100.py --rev REV --work DIR [--seed N]
"""
import argparse, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
CAND = HERE / "candidate"
TOOL = "tools/mori-seat-terminal.py"


def tree(work, name, rev):
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    a = subprocess.Popen(["git", "-C", str(LANE), "archive", rev], stdout=subprocess.PIPE)
    subprocess.run(["tar", "-x", "-C", str(d)], stdin=a.stdout, check=True)
    a.wait()
    return d


def apply_c1(d, skip=""):
    cmd = [sys.executable, str(CAND / "apply-c1.py"), str(d)]
    if skip:
        cmd += ["--skip", skip]
    subprocess.run(cmd, check=True, capture_output=True)


def sub_once(path, old, new):
    t = path.read_text(encoding="utf-8")
    n = t.count(old)
    if n < 1:
        sys.exit("controls: mutation anchor missing in %s: %r" % (path, old[:60]))
    path.write_text(t.replace(old, new), encoding="utf-8")


def c1(d, work, seed):
    r = subprocess.run([sys.executable, str(HERE / "count-c1.py"), "--root", str(d), "--seed", str(seed),
                        "--work", str(work)], capture_output=True, text=True)
    first = r.stdout.splitlines()[0] if r.stdout else "C1=? " + r.stderr[-200:]
    return ("met" if r.returncode == 0 else "unmet" if r.returncode == 1 else "setup"), first


def c2(d, work):
    r = subprocess.run([sys.executable, str(HERE / "count-c2.py"), "--root", str(d), "--repo", str(LANE)],
                       capture_output=True, text=True)
    first = r.stdout.splitlines()[0] if r.stdout else "C2=? " + r.stderr[-200:]
    return ("met" if r.returncode == 0 else "unmet" if r.returncode == 1 else "setup"), first


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--seed", type=int, default=100)
    a = ap.parse_args()
    work = pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    rows = []

    def rec(cid, expect, got, line):
        ok = got == expect
        rows.append(ok)
        print("%s expect=%s got=%s %s | %s" % (cid, expect, got, "AS_EXPECTED" if ok else "UNEXPECTED", line),
              flush=True)

    s = a.seed
    d = tree(work, "K0", a.rev); rec("K0", "unmet", *c1(d, work, s))
    d = tree(work, "K1", a.rev); apply_c1(d)
    t = d / TOOL
    sub_once(t, '        return "dead_error_other", None\n    if view["quota_token"]:',
             '        return "dead_auth", None\n    if view["quota_token"]:')
    sub_once(t, '    if _auth_evidence(view):\n        return "dead_auth", None\n    return "dead_error_other", None\n\n\ndef _auth_evidence',
             '    return "dead_auth", None\n\n\ndef _auth_evidence')
    rec("K1", "unmet", *c1(d, work, s))
    d = tree(work, "K2", a.rev); apply_c1(d)
    sub_once(d / TOOL, 'AUTH_TOKEN_BYTES = tuple(token.encode("ascii") for token in AUTH_TOKENS)',
             'AUTH_TOKEN_BYTES = ()')
    rec("K2", "unmet", *c1(d, work, s))
    d = tree(work, "K3", a.rev); apply_c1(d)
    sub_once(d / TOOL, "AUTH_STATUSES = frozenset((401, 403))", "AUTH_STATUSES = frozenset()")
    rec("K3", "unmet", *c1(d, work, s))
    d = tree(work, "K4", a.rev); apply_c1(d)
    sub_once(d / TOOL, '        return "dead_error_other", None\n    if view["quota_token"]:',
             '        return "dead_error_other", None\n    if _auth_evidence(view):\n        return "dead_auth", None\n    if view["quota_token"]:')
    rec("K4", "unmet", *c1(d, work, s))
    d = tree(work, "K5", a.rev); apply_c1(d)
    frags = ["Invalid 'Authorization'", "Unauthorized", "Forbidden: key revoked", "subscription does not have",
             "invalid x-api-key", "token expired", "permission_denied: This model", "unauthenticated: token",
             "PERMISSION_DENIED: caller", "UNAUTHENTICATED: request", "(type=authentication_error)",
             "permission_error"]
    sub_once(d / TOOL, "AUTH_STATUSES = frozenset((401, 403))", "AUTH_STATUSES = frozenset()")
    sub_once(d / TOOL, 'AUTH_TOKENS = (\n    "permission_denied",\n    "PERMISSION_DENIED",\n    "unauthenticated",\n    "UNAUTHENTICATED",\n    "authentication_error",\n    "permission_error",\n)',
             "AUTH_TOKENS = %r" % (tuple(frags),))
    rec("K5", "unmet", *c1(d, work, s))
    d = tree(work, "K6", a.rev); apply_c1(d, "knowledge,rows"); rec("K6", "unmet", *c1(d, work, s))
    d = tree(work, "K7", a.rev); apply_c1(d, "gate"); rec("K7", "unmet", *c1(d, work, s))
    d = tree(work, "K8", a.rev); apply_c1(d, "skill"); rec("K8", "unmet", *c1(d, work, s))
    d = tree(work, "P1", a.rev); apply_c1(d); rec("P1", "met", *c1(d, work, s))

    sys.path.insert(0, str(HERE))
    import importlib.util
    spec = importlib.util.spec_from_file_location("c2", HERE / "count-c2.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

    def edit_rows(d, fn):
        p = d / "corpus/SOURCES.md"
        lines = p.read_text(encoding="utf-8").split("\n")
        p.write_text("\n".join(fn(lines)), encoding="utf-8")

    d = tree(work, "K0c", a.rev); rec("K0c", "unmet", *c2(d, work))

    def k1(lines):
        out = []
        for l in lines:
            if m.ROW.match(l) and any(k != w for k, w in m.stated(l)):
                l = re.sub(r"(\d+) words", "words", l)
            out.append(l)
        return out
    d = tree(work, "K1c", a.rev); edit_rows(d, k1); rec("K1c", "unmet", *c2(d, work))

    def k2(lines):
        out = []
        for l in lines:
            mm = [(k, w) for k, w in m.stated(l) if k != w] if m.ROW.match(l) else []
            if mm:
                parts = l.split("|")
                parts[6] = parts[6].rstrip(" ") + " " + m.correction_text([(k, k) for k, _w in mm]) + " "
                l = "|".join(parts)
            out.append(l)
        return out
    d = tree(work, "K2c", a.rev); edit_rows(d, k2); rec("K2c", "unmet", *c2(d, work))

    def k3(lines):
        out = []
        for l in lines:
            ss = m.stated(l) if m.ROW.match(l) else []
            if ss:
                mm = [(k, w) for k, w in ss if k != w] or [(ss[0][0], ss[0][1])]
                parts = l.split("|")
                parts[6] = parts[6].rstrip(" ") + " " + m.correction_text(mm) + " "
                l = "|".join(parts)
            out.append(l)
        return out
    d = tree(work, "K3c", a.rev); edit_rows(d, k3); rec("K3c", "unmet", *c2(d, work))

    def k4(lines):
        out = []
        for l in lines:
            if m.ROW.match(l):
                for k, w in [(k, w) for k, w in m.stated(l) if k != w]:
                    l = l.replace("%d words" % k, "%d words" % w, 1)
            out.append(l)
        return out
    d = tree(work, "K4c", a.rev); edit_rows(d, k4); rec("K4c", "unmet", *c2(d, work))

    def k5(lines):
        out = list(lines)
        idx = [i for i, l in enumerate(out) if m.ROW.match(l)]
        for j, i in enumerate(idx):
            mm = [(k, w) for k, w in m.stated(out[i]) if k != w]
            if mm:
                tgt = idx[j - 1]
                parts = out[tgt].split("|")
                parts[6] = parts[6].rstrip(" ") + " " + m.correction_text(mm) + " "
                out[tgt] = "|".join(parts)
        return out
    d = tree(work, "K5c", a.rev); edit_rows(d, k5); rec("K5c", "unmet", *c2(d, work))
    d = tree(work, "P2", a.rev)
    subprocess.run([sys.executable, str(CAND / "apply-c2.py"), str(d)], check=True, capture_output=True)
    rec("P2", "met", *c2(d, work))
    bad = rows.count(False)
    print("CONTROLS_DONE unexpected=%d rev=%s seed=%d" % (bad, a.rev, s))
    shutil.rmtree(work, ignore_errors=True)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
