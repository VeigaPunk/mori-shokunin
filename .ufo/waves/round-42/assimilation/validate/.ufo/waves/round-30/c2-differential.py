#!/usr/bin/env python3
"""Round-30 C2 full-output differential: entering-tip tool blob vs the tool at <rev>, over every case input of the
five case files at <rev>. Reads committed bytes only. Usage: python3 -I -B c2-differential.py <rev>"""
import json, os, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
BASE = "58b61681a0e3f3b821a17d38a4e713ccd9921615"
TOOL = "tools/mori-oom-killers.py"
FILES = ["cases.json", "cases-supplementary.json", "cases-a2.json", "cases-a2-r29.json", "cases-a2-r30.json"]


def show(rev, path):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    p = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"], stdout=subprocess.PIPE, env=env)
    return p.stdout if p.returncode == 0 else None


def run(tool, inputs, td, n):
    path = os.path.join(td, f"in-{n}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(inputs, fh)
    p = subprocess.run([sys.executable, "-I", "-B", tool, "--inputs", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, json.loads(p.stdout.decode("utf-8")), p.stderr.decode("utf-8", "replace")


def flat(d, prefix=""):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            out.update(flat(v, f"{prefix}{k}."))
    else:
        out[prefix[:-1]] = d
    return out


def state(show_text):
    for line in (show_text or "").splitlines():
        if line.startswith("ActiveState="):
            return line.split("=", 1)[1]
    return None


def main():
    rev = sys.argv[1]
    with tempfile.TemporaryDirectory() as td:
        base, new = os.path.join(td, "base.py"), os.path.join(td, "new.py")
        open(base, "wb").write(show(BASE, TOOL))
        open(new, "wb").write(show(rev, TOOL))
        n = changed = older_changed = disallowed = acted_lost = 0
        for fn in FILES:
            raw = show(rev, f"tools/fixtures/mori-oom-killers/{fn}")
            if raw is None:
                print(f"file_absent={fn}")
                continue
            for case in json.loads(raw)["cases"]:
                n += 1
                a = run(base, case["inputs"], td, f"a{n}")
                b = run(new, case["inputs"], td, f"b{n}")
                if a == b:
                    continue
                changed += 1
                fa, fb = flat(a[1]), flat(b[1])
                diffs = [f"{k}: {json.dumps(fa.get(k))} -> {json.dumps(fb.get(k))}" for k in sorted(set(fa) | set(fb)) if fa.get(k) != fb.get(k)]
                st = state(case["inputs"].get("earlyoom_show"))
                older = fn in FILES[:3]
                older_changed += older
                bad = older and not (case["inputs"].get("earlyoom_show") and st not in (None, "active"))
                disallowed += bad
                lost = a[1].get("verdict") == "KILLER_ACTED" and b[1].get("verdict") != "KILLER_ACTED"
                acted_lost += lost
                print(f"changed {fn} {case['id']} ActiveState={st} exit {a[0]}->{b[0]} " + "; ".join(diffs))
        print(f"inputs={n} changed={changed} older_changed={older_changed} older_disallowed={disallowed} acted_lost={acted_lost}")


main()
