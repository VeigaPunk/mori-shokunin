#!/usr/bin/env python3
# FamWavesIo (round 20, falsify scratch) - read-only replay of the C1 claims for
# -FINDING:WAVE_UNSETTLED_AGE, obs and io_avg_unavailable. Does NOT run the census.
# Writes nothing; reads git history (git show), the fleet wave dirs, and lane files.
import hashlib
import json
import math
import os
import re
import stat
import subprocess
import time

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET_WAVES = "/home/vgpnk/Projects/shokunin/.ufo/waves"
UNSET_S = 7200
NOW = int(time.time())
CLOSED = re.compile(r'"(closed|settled)"[ \t\r\n\f\v]*:[ \t\r\n\f\v]*true|"status"[ \t\r\n\f\v]*:[ \t\r\n\f\v]*"closed"')


def git_show(rev):
    r = subprocess.run(["git", "-C", LANE, "show", f"{rev}:tools/mori-census.sh"], capture_output=True, check=True)
    return r.stdout


def fn_body(data, name):
    out, on = [], False
    for ln in data.decode("utf-8", "replace").split("\n"):
        if not on and re.match(r"^" + re.escape(name) + r"\(\) *\{", ln):
            on = True
        if on:
            out.append(ln)
            if ln == "}":
                break
    return "\n".join(out).encode()


def h8(b):
    return hashlib.sha256(b).hexdigest()[:8]


def part1_identity():
    r10, head = git_show("5be8943"), git_show("fe9fa90")
    print("[1] whole-file sha256  5be8943=%s  fe9fa90(HEAD blob)=%s"
          % (hashlib.sha256(r10).hexdigest()[:8], hashlib.sha256(head).hexdigest()[:8]))
    for f in ["probe_waves", "emit_finding", "emit_surface", "cap", "probe_disk", "dev_of", "io_of",
              "drift_scan", "drift_field_report", "drift_report"]:
        a, b = h8(fn_body(r10, f)), h8(fn_body(head, f))
        print("    %-20s r10=%s head=%s %s" % (f, a, b, "IDENTICAL" if a == b else "CHANGED"))


def newest(d):
    best = None
    for root, _, files in os.walk(d):
        for f in files:
            st = os.lstat(os.path.join(root, f))
            if stat.S_ISREG(st.st_mode) and (best is None or st.st_mtime > best):
                best = st.st_mtime
    return None if best is None else math.floor(best)


def live_findings():
    """Mirror of probe_waves (census lines 865-932) over the fleet wave dirs."""
    out = []
    for name in sorted(os.listdir(FLEET_WAVES)):
        d = os.path.join(FLEET_WAVES, name)
        if not os.path.isdir(d) or name.startswith(("round-", ".")):
            continue

        def ex(n):
            return os.path.isfile(os.path.join(d, n))

        reg, disp, run = int(ex("swarm-registry.json")), int(ex("dispatch.json")), int(ex("run.json"))
        settle = any(ex(n) for n in ("results.json", "closeout.json", "mission-result.json", "closeout.md"))
        if not settle:
            for c in ("swarm-registry.json", "dispatch.json", "run.json", "spec.json"):
                if ex(c):
                    txt = open(os.path.join(d, c), "rb").read().decode("latin-1")
                    if any(CLOSED.search(l) for l in txt.splitlines()):
                        settle = True
                        break
        nt = newest(d)
        age = 0 if nt is None else NOW - nt
        if not settle and (reg or disp or run) and age > UNSET_S:
            out.append(f"FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave={name} age_s={age} "
                       f"threshold_s={UNSET_S} reg={reg} disp={disp} run={run} settle=0 ts=X script_sha256=0000")
    return out


def norm(l):
    l = re.sub(r"\bage_s=[0-9]+", "age_s=<V>", l)
    l = re.sub(r"\bts=[^ ;)]*", "ts=<V>", l)
    l = re.sub(r"\bscript_sha256=[0-9a-f]+", "script_sha256=<V>", l)
    return re.sub(r"\b(reg|disp|run|settle)=[0-9]+", r"\1=<V>", l)


def census_scan(line):
    """Mirror of drift_scan (census lines 2826-2843): whitespace tokens without '=' are skipped."""
    kv, keys = {}, []
    for tok in line.split():
        tok = tok[1:] if tok.startswith("(") else tok
        tok = tok[:-1] if tok.endswith(";") else tok
        tok = tok[:-1] if tok.endswith(")") else tok
        if "=" not in tok:
            continue
        k, v = tok.split("=", 1)
        if not re.fullmatch(r"[A-Za-z0-9_]+", k):
            continue
        if k not in kv:
            keys.append(k)
        kv[k] = kv.get(k, "") + v
    return kv, keys


def line_id(l):
    p = l.split()
    return "FINDING:" + p[1] if p[0] == "FINDING" else p[0]


def drift_report(base, new):
    """Mirror of drift_report (census lines 2874-2918): exact match, same-id leftovers, added lines."""
    bu, nu = [False] * len(base), [False] * len(new)
    for i, b in enumerate(base):
        for j, n in enumerate(new):
            if not nu[j] and n == b:
                bu[i] = nu[j] = True
                break
    rep = set()
    for i, b in enumerate(base):
        if bu[i]:
            continue
        j = next((j for j, n in enumerate(new) if not nu[j] and line_id(n) == line_id(b)), None)
        if j is None:
            rep.add("-" + line_id(b))
            continue
        nu[j] = True
        kb, kn = census_scan(b)[0], census_scan(new[j])[0]
        for k in kb:
            if k not in kn:
                rep.add("-" + k)
            elif kb[k] != kn[k]:
                rep.add(k)
        for k in kn:
            if k not in kb:
                rep.add("+" + k)
    for j, n in enumerate(new):
        if not nu[j]:
            rep.add("+" + line_id(n))
    return sorted(rep), sum(bu)


def baseline_lines():
    return open(f"{LANE}/corpus/evidence/baseline-r10-20261015T2231Z.json", encoding="utf-8").read().split("\n")


def part2_wave_pairing():
    base = baseline_lines()
    wave_base = base[25:36]  # 1-indexed lines 26-36
    assert all(l.startswith("FINDING WAVE_UNSETTLED_AGE") for l in wave_base)
    live = live_findings()
    print("[2] baseline WAVE lines 26-36: %d | live aged-unsettled (replica): %d" % (len(wave_base), len(live)))
    for l in live:
        print("      live:", l.split()[3])
    toks, exact = drift_report([norm(l) for l in wave_base], [norm(l) for l in live])
    print("    exact-matched lines: %d" % exact)
    print("    replayed WAVE-family drift tokens:", toks)


def part3_disk():
    b12 = baseline_lines()[11]  # 1-indexed line 12
    assert b12.startswith("SURFACE disk:")
    cur = b12.replace("io_avg_since_boot=dm-0:<V>Bps/<V>s io_avg_unavailable=tmpfs:not-a-block-device",
                      "io_avg_since_boot=dm-0:<V>Bps/<V>s nvme0n1p1:<V>Bps/<V>s io_avg_unavailable=none")
    assert cur != b12
    kb, kn = census_scan(b12)[0], census_scan(cur)[0]
    print("[3] disk row: io_avg_since_boot first-element equal=%s" % (kb["io_avg_since_boot"] == kn["io_avg_since_boot"]))
    print("    keys whose compared value changed:", sorted(k for k in kb if k in kn and kb[k] != kn[k]))
    cur2 = b12.replace("targets=/home/vgpnk/Projects/shokunin /tmp;", "targets=/home/vgpnk/Projects/shokunin;")
    assert cur2 != b12
    k2 = census_scan(cur2)[0]
    print("    dropping /tmp from targets= compared-value changes:", sorted(k for k in kb if kb[k] != k2.get(k)))


def part4_register():
    reg = json.load(open(f"{LANE}/corpus/evidence/drift-classification-r20.json", encoding="utf-8"))
    ent = json.load(open(f"{LANE}/.ufo/waves/round-20/evidence/c1-drift-entering.json", encoding="utf-8"))
    tok = reg["tokens"]
    counts = {}
    for v in tok.values():
        counts[v["class"]] = counts.get(v["class"], 0) + 1
    print("[4] register entries=%d declared=%s computed=%s" % (len(tok), reg["class_counts"], counts))
    print("    entering tokens missing from register:", [t for t in ent["tokens"] if t not in tok])
    print("    entries without evidence:", [k for k, v in tok.items() if not v.get("evidence")])
    for t in ["-FINDING:WAVE_UNSETTLED_AGE", "obs", "io_avg_unavailable"]:
        print("    %-28s class=%s" % (t, tok[t]["class"]))


if __name__ == "__main__":
    part1_identity()
    part2_wave_pairing()
    part3_disk()
    part4_register()
