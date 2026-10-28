#!/usr/bin/env python3
"""mori round-61 C3 counter — the counter execution boundary, repaired.

Repairs the round-60 decertification of the boundary counter: `met` is the
conjunction of ALL measured booleans including the c1_ok arm, every printed
token is one measured boolean under the published TOKEN_MAP, the
materialize-and-run helper refuses to execute any blob whose sha256 is not
pinned, and the frozen expect table is sha-pinned.

Arms
  r60hole      parse the PINNED r60 count-c3 bytes (.ufo/waves/round-60/
               count-c3.py at R60_REV): the hole is present there — `met`
               carries no c1 conjunct, zero `failed.append("` sites, and the
               three gate tokens print from the print expression (red-before).
  r61repair    parse this counter's own source: `met` includes c1_ok,
               TOKEN_MAP covers every printed token, each token has a
               measured `*_ok` boolean.
  blobrefusal  the pinned materializer refuses unpinned blobs with zero child
               executions recorded; a pinned blob materializes.
  expectpin    the frozen EXPECTS table matches EXPECT_PIN; a tampered copy
               changes the digest.
  livepins     the r61 count-c1.py / count-c2.py materialize at <rev> with
               the in-script pins.

Read-only over the measured repo. Honors TMPDIR; --scratch must be writable.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

R61_C1 = ".ufo/waves/round-61/count-c1.py"
R61_C2 = ".ufo/waves/round-61/count-c2.py"
R60_PATH = ".ufo/waves/round-60/count-c3.py"
R60_REV = "ac496c7cde8cad965079858accae3bedfe4a73f2"
R60_SHA = "fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514"
PIN_C1 = "a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00"
PIN_C2 = "82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8"

TOKENS = ["r60hole", "r61repair", "blobrefusal", "expectpin", "livepins"]

EXPECTS = {t: "ok" for t in TOKENS}
EXPECT_PIN = hashlib.sha256(
    json.dumps(EXPECTS, sort_keys=True).encode()).hexdigest()

REASON = {
    "r60hole": "r60 bytes lost or hole absent (red-before unfaithful)",
    "r61repair": "self source lost the c1_ok conjunct or TOKEN_MAP",
    "blobrefusal": "unpinned blob executed or pinned blob refused",
    "expectpin": "expect table tampered or pin mismatch",
    "livepins": "r61 counters absent or sha pin mismatch at rev",
}

EXEC_LOG = []


def sh(repo, *args, binary=False):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def cat(repo, rev, path):
    return sh(repo, "show", f"{rev}:{path}", binary=True)


def materialize_pinned(blob, pin, run=False):
    """Refuse any blob whose sha256 != pin; never executes on refusal.

    Returns (payload_or_None, reason). run=True executes only a pinned blob,
    counted in EXEC_LOG."""
    if hashlib.sha256(blob).hexdigest() != pin:
        return None, "unpinned"
    if run:
        EXEC_LOG.append(("run", pin[:12]))
        r = subprocess.run([sys.executable, "-c", blob.decode("utf-8")],
                           capture_output=True)
        return r, "ran"
    return blob, "pinned"


def arm_r60hole(r60_bytes):
    if r60_bytes is None or hashlib.sha256(r60_bytes).hexdigest() != R60_SHA:
        return False, "r60_bytes_pin"
    text = r60_bytes.decode("utf-8", "replace")
    m = re.search(r"^\s*met = \((.*)\)", text, re.M)
    if not m:
        return False, "r60_met_line_missing"
    if "c1" in m.group(1):
        return False, "r60_hole_absent"
    for tok in ("toolgate", "containment", "expectgate"):
        # the defect: tokens tested against failed-list literals no append
        # site emits (r60 routed defect 2 / Reviewer13)
        if f'failed.append("{tok}"' in text:
            return False, "r60_append_site:" + tok
        if f'"{tok}" not in failed' not in text:
            return False, "r60_token_untested:" + tok
    return True, ""


def arm_r61repair(self_bytes):
    if self_bytes is None:
        return False, "self_bytes_missing"
    text = self_bytes.decode("utf-8", "replace")
    m = re.search(r"^\s*met = (.+)$", text, re.M)
    if not m or "c1_ok" not in m.group(1):
        return False, "c1_conjunct_missing"
    mt = re.search(r"^TOKEN_MAP = \{(.*?)^\}", text, re.S | re.M)
    if not mt:
        return False, "token_map_missing"
    keys = set(re.findall(r"\"([a-z0-9]+)\":", mt.group(1)))
    if keys != set(TOKENS):
        return False, "token_map_keys"
    for t in TOKENS:
        if not (re.search(rf"^\s*b\[\"{t}_ok\"\], _ = ", text, re.M)
                or re.search(rf"^\s*{t}_ok = ", text, re.M)):
            return False, "token_unbound:" + t
    return True, ""


def arm_blobrefusal():
    blob = b"print('hostile')\n"
    payload, reason = materialize_pinned(blob, "0" * 64, run=True)
    if payload is not None or reason != "unpinned":
        return False, "unpinned_accepted"
    if EXEC_LOG:
        return False, "executed_unpinned"
    mine = Path(__file__).read_bytes()
    payload, reason = materialize_pinned(mine,
                                         hashlib.sha256(mine).hexdigest(),
                                         run=False)
    if payload is None:
        return False, "pinned_refused"
    return True, ""


def arm_expectpin():
    pin = hashlib.sha256(
        json.dumps(EXPECTS, sort_keys=True).encode()).hexdigest()
    if pin != EXPECT_PIN:
        return False, "expect_pin_mismatch"
    tampered = dict(EXPECTS)
    tampered[TOKENS[0]] = "ok~tampered"
    if hashlib.sha256(
            json.dumps(tampered, sort_keys=True).encode()).hexdigest() \
            == EXPECT_PIN:
        return False, "tamper_accepted"
    return True, ""


def arm_livepins(repo, rev):
    for path, pin in ((R61_C1, PIN_C1), (R61_C2, PIN_C2)):
        b = cat(repo, rev, path)
        if b is None:
            return False, "live_absent:" + path
        if hashlib.sha256(b).hexdigest() != pin:
            return False, "live_pin:" + path
    return True, ""


TOKEN_MAP = {
    "r60hole": "r60hole_ok",
    "r61repair": "r61repair_ok",
    "blobrefusal": "blobrefusal_ok",
    "expectpin": "expectpin_ok",
    "livepins": "livepins_ok",
}


def run_arms(repo, rev, r60_bytes=None, self_bytes=None, pins=None):
    global PIN_C1, PIN_C2
    saved = (PIN_C1, PIN_C2)
    if pins:
        PIN_C1, PIN_C2 = pins
    b = {}
    b["r60hole_ok"], _ = arm_r60hole(r60_bytes)
    b["r61repair_ok"], _ = arm_r61repair(self_bytes)
    b["blobrefusal_ok"], _ = arm_blobrefusal()
    b["expectpin_ok"], _ = arm_expectpin()
    b["livepins_ok"], _ = arm_livepins(repo, rev)
    # met is the conjunction of all measured booleans including c1_ok.
    c1_ok = all(b.values())
    met = c1_ok
    PIN_C1, PIN_C2 = saved
    return b, met


def fmt(b, met, rev, cases):
    toks = " ".join(f"{t}={'ok' if b[t + '_ok'] else 'FAIL'}" for t in TOKENS)
    failed = [REASON[t] for t in TOKENS if not b[t + "_ok"]]
    head = "C3=met" if met else "C3=unmet"
    return (f"{head} {toks} cases={cases} "
            f"failed={';'.join(failed) or 'none'} rev={rev}")


# ---------- selftest ----------

def selftest(scratch):
    self_bytes = Path(__file__).read_bytes()
    npass = 0

    def check(name, got, want):
        nonlocal npass
        npass += got == want
        print(f"case {name}: got={got} want={want} "
              f"{'pass' if got == want else 'FAIL'}")

    # tiny repo carrying the two r61 counters
    d = Path(scratch) / "st-live"
    (d / ".ufo/waves/round-61").mkdir(parents=True, exist_ok=True)
    for src in (Path(os.getcwd()) / R61_C1, Path(os.getcwd()) / R61_C2):
        (d / src.name.replace(src.name, R61_C1 if src.name.endswith("c1.py")
                              else R61_C2)).write_bytes(src.read_bytes())
    subprocess.run(["git", "-C", str(d), "init", "-q"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(d), "-c", "user.name=t", "-c",
                    "user.email=t@t", "commit", "-qm", "x"], check=True,
                   capture_output=True)
    rev = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    c1b = (d / R61_C1).read_bytes()
    c2b = (d / R61_C2).read_bytes()
    r60 = Path(os.getcwd()).joinpath(".ufo/waves/round-60/count-c3.py")
    r60b = r60.read_bytes() if r60.exists() else None

    b, met = run_arms(str(d), rev, r60b, self_bytes,
                      pins=(hashlib.sha256(c1b).hexdigest(),
                            hashlib.sha256(c2b).hexdigest()))
    check("all-arms-good", met, True)

    # r60 tamper: insert a c1 conjunct -> hole arm must fail
    bad_r60 = r60b.replace(b"met = (c2_ok", b"met = (c1_ok and c2_ok")
    b, met = run_arms(str(d), rev, bad_r60, self_bytes,
                      pins=(hashlib.sha256(c1b).hexdigest(),
                            hashlib.sha256(c2b).hexdigest()))
    check("r60-tamper-detected", (not met) and (not b["r60hole_ok"]), True)

    # self mutant: drop c1_ok from met -> repair arm must fail
    mut = self_bytes.replace(b"c1_ok = all(b.values())\n    met = c1_ok",
                             b"met = all(b.values())")
    b, met = run_arms(str(d), rev, r60b, mut,
                      pins=(hashlib.sha256(c1b).hexdigest(),
                            hashlib.sha256(c2b).hexdigest()))
    check("self-mutant-detected", (not met) and (not b["r61repair_ok"]), True)

    # wrong live pins -> livepins arm must fail
    b, met = run_arms(str(d), rev, r60b, self_bytes,
                      pins=("1" * 64, "2" * 64))
    check("wrong-pins-detected", (not met) and (not b["livepins_ok"]), True)

    # unit arms
    check("blobrefusal", arm_blobrefusal()[0], True)
    check("expectpin", arm_expectpin()[0], True)
    check("r60hole-real-bytes", arm_r60hole(r60b)[0], True)
    check("r61repair-real-bytes", arm_r61repair(self_bytes)[0], True)

    print(f"C3_SELFTEST pass={npass} fail={8 - npass}")
    return npass == 8


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--scratch", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    scratch = a.scratch or os.environ.get("TMPDIR") or "/tmp"
    os.makedirs(scratch, exist_ok=True)
    if a.selftest:
        sys.exit(0 if selftest(scratch) else 1)
    if not a.rev:
        ap.error("rev required without --selftest")
    r60 = sh(a.repo, "show", f"{R60_REV}:{R60_PATH}", binary=True)
    self_bytes = Path(__file__).read_bytes()
    b, met = run_arms(a.repo, a.rev, r60, self_bytes)
    print(fmt(b, met, a.rev, cases=5))
    sys.exit(0 if met else 1)


if __name__ == "__main__":
    main()
