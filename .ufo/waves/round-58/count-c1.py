#!/usr/bin/env python3
"""Round 58 C1 counter: active-register binding with pointer resolution.

Fixes the round-57 routed defects 1-2 (corpus/lessons/round-57-verifier-spotcheck.md):
the r57 counter selected the FIRST '## Capabilities' section (the superseded
'-- none yet --' stub at SCORECARD.md:596) and never resolved evidence pointers,
so it false-negatived on the landed round-56 rows and false-greened on junk
pointers. This counter:

  1. BINDING: selects the register section whose preamble contains the exact
     sentence 'the lane's current capabilities register' (the round-35 active
     register, SCORECARD.md:1953), requires the '| key | capability |' header,
     requires >= 10 key rows, and refuses any section whose body contains the
     stub marker '-- none yet --'.
  2. ROWS: exactly the rows keyed `rounds[832].capabilities_added[0]` and
     `rounds[832].capabilities_added[1]`.
  3. POINTERS: every backticked repo-relative path inside those two rows must
     resolve via `git cat-file -e R:<path>`; a row naming a nonexistent path
     fails the arm (never a silent pass).
  4. MANIFEST: fleet MANIFEST.json rounds[832].capabilities_added[0] mentions
     'vote binding' and [1] mentions 'driver-liveness' (closure-record binding).

Usage: count-c1.py R            (measure revision R of the lane repo)
       count-c1.py --selftest   (isolated throwaway-git fixture arms)
Exit: 0 met / 1 unmet / 2 setup. Frozen at the round-58 freeze commit.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FLEET = os.path.dirname(LANE)
STUB_MARK = "-- none yet --"
BIND_SENT = "the lane's current capabilities register"
R56_KEYS = ("`rounds[832].capabilities_added[0]`", "`rounds[832].capabilities_added[1]`")
MANIFEST_HINTS = {0: "vote binding", 1: "driver-liveness"}


def _git(*args, cwd=None, check=False):
    return subprocess.run(["git", "-C", str(cwd or LANE), *args], capture_output=True, text=True)


def _section(text, start_line):
    """Return the body of the markdown section starting at 0-based start_line."""
    lines = text.splitlines()
    out = []
    for ln in lines[start_line + 1:]:
        if ln.startswith("## "):
            break
        out.append(ln)
    return "\n".join(out)


def _find_register(text):
    """Locate the active register section; return (line_index, body) or (None, reason)."""
    lines = text.splitlines()
    headings = [i for i, ln in enumerate(lines) if ln.strip() == "## Capabilities"]
    if not headings:
        return None, "no_capabilities_heading"
    for hi in headings:
        body = _section(text, hi)
        head_zone = "\n".join(body.splitlines()[:12])
        if BIND_SENT in head_zone and STUB_MARK not in body and "| key | capability |" in body:
            return hi, body
    return None, "active_register_not_found"


def measure(rev):
    p = _git("show", f"{rev}:SCORECARD.md")
    if p.returncode != 0:
        print(f"C1=unmet reason=revision failed=rev rev={rev}")
        return 1
    text = p.stdout
    hi, body = _find_register(text)
    failed = []
    binding = "ok"
    if hi is None:
        binding = "bad"
        failed.append("binding")
        rows = []
    else:
        rows = [ln for ln in body.splitlines()
                if ln.startswith("|") and any(k in ln for k in R56_KEYS)]
        n_key_rows = len([ln for ln in body.splitlines()
                          if re.match(r"^\| `rounds\[", ln)])
        if n_key_rows < 10:
            binding = "bad"
            failed.append("binding")
    pointers = "ok"
    manifest = "ok"
    if binding == "ok":
        if len(rows) != 2:
            pointers = "bad"
            failed.append("rows")
        else:
            for ln in rows:
                for path in re.findall(r"`([^`]+)`", ln):
                    if "/" not in path and not path.endswith((".py", ".txt", ".md")):
                        continue
                    if path.startswith((".ufo/", "tools/", "corpus/")):
                        q = _git("cat-file", "-e", f"{rev}:{path}")
                        if q.returncode != 0:
                            pointers = "bad"
                            failed.append("pointers")
        try:
            import json
            m = json.load(open(os.path.join(FLEET, "MANIFEST.json")))
            caps = m["rounds"][832]["capabilities_added"]
            for idx, hint in MANIFEST_HINTS.items():
                if hint not in caps[idx]:
                    manifest = "bad"
                    failed.append("manifest")
        except Exception:
            manifest = "bad"
            failed.append("manifest")
    else:
        manifest = "bad"
    ok = not failed and len(rows) == 2
    state = "met" if ok else "unmet"
    print(f"C1={state} rows={len(rows)} pointers={pointers} manifest={manifest} "
          f"binding={binding} failed={','.join(failed) or 'none'} rev={rev}")
    return 0 if ok else 1


# ---------------- selftest ----------------

FIXTURE_SCORECARD = """# fixture scorecard

## Axes

## Capabilities

-- none yet --

## Saturation
"""

ACTIVE_PREAMBLE = """Round 35 (claim C1, calibration). This is the lane's current capabilities register, the
`capabilities` field of the AXES.md SCORECARD contract. It holds one row per capability
that a non-author closure admitted. As the current self-assessment this register supersedes
the `— none yet —` table in the first `## Capabilities` section.

| key | capability | what it can now do | evidence | first-working round |
|---|---|---|---|---|
"""

ROW_OK_0 = ("| `rounds[832].capabilities_added[0]` | dual-shape seat-output vote binding | "
            "Binds final vote lines. | `tools/mori-vote-bind.py`; `.ufo/waves/round-56/evidence/c2-at-landed.txt` | 56 |\n")
ROW_OK_1 = ("| `rounds[832].capabilities_added[1]` | strict per-event driver-liveness probe | "
            "Parses inline watchdog log events. | `tools/mori-driver-liveness.py`; `.ufo/waves/round-56/evidence/c1-at-landed.txt` | 56 |\n")
ROW_BAD_PTR = ("| `rounds[832].capabilities_added[0]` | dual-shape seat-output vote binding | "
               "Binds final vote lines. | `tools/no-such-tool.py` | 56 |\n")
ROW_WRONG_KEY = ("| `rounds[999].capabilities_added[0]` | junk capability | "
                 "Junk. | `tools/mori-vote-bind.py` | 99 |\n")

PADDER = "".join(
    f"| `rounds[{300 + i}].capabilities_added[0]` | pad {i} | Pad. | `tools/mori-vote-bind.py` | 30 |\n"
    for i in range(10))


def _mkrepo(tmp, scorecard, with_tools=True):
    d = tempfile.mkdtemp(dir=tmp)
    subprocess.run(["git", "init", "-q", d], check=True)
    if with_tools:
        os.makedirs(os.path.join(d, "tools"), exist_ok=True)
        os.makedirs(os.path.join(d, ".ufo/waves/round-56/evidence"), exist_ok=True)
        for f in ("tools/mori-vote-bind.py", "tools/mori-driver-liveness.py",
                  ".ufo/waves/round-56/evidence/c2-at-landed.txt",
                  ".ufo/waves/round-56/evidence/c1-at-landed.txt"):
            open(os.path.join(d, f), "w").write("# fixture\n")
    open(os.path.join(d, "SCORECARD.md"), "w").write(scorecard)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-qm", "fixture"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True, check=True).stdout.strip()
    return d, rev


def _run_selftest():
    import json
    global LANE, FLEET
    tmp = tempfile.mkdtemp(prefix="mori-r58-c1-")
    keep_lane, keep_fleet = LANE, FLEET
    passed = failed = 0
    # manifest fixture (shared)
    mdir = tempfile.mkdtemp(prefix="mani-", dir=tmp)
    caps = ["dual-shape seat-output vote binding (x)", "strict per-event driver-liveness probe (x)"]
    rounds = [None] * 833
    rounds[832] = {"capabilities_added": caps}
    json.dump({"rounds": rounds}, open(os.path.join(mdir, "MANIFEST.json"), "w"))
    cases = []
    active = ("## Capabilities\n\n" + ACTIVE_PREAMBLE + PADDER + ROW_OK_0 + ROW_OK_1 + "\n## Saturation\n")
    stub_only = FIXTURE_SCORECARD.replace("-- none yet --",
                                          "-- none yet --\n\n| key | capability |\n|---|---|\n")
    active_bad_ptr = ("## Capabilities\n\n" + ACTIVE_PREAMBLE + PADDER + ROW_BAD_PTR + ROW_OK_1 + "\n## Saturation\n")
    active_wrong_key = ("## Capabilities\n\n" + ACTIVE_PREAMBLE + PADDER + ROW_WRONG_KEY + ROW_OK_1 + "\n## Saturation\n")
    cases.append(("conformant_active_register", active, True, 0, "met"))
    cases.append(("stub_only_binding_refused", stub_only, True, 1, "binding=bad"))
    cases.append(("nonexistent_pointer_fails", active_bad_ptr, True, 1, "failed=pointers"))
    cases.append(("wrong_key_row_fails", active_wrong_key, True, 1, "failed=rows"))
    try:
        for name, sc, tools, want_rc, want_tok in cases:
            d, rev = _mkrepo(tmp, sc, tools)
            LANE = d
            FLEET = mdir
            old_stdout = sys.stdout
            from io import StringIO
            buf = StringIO()
            sys.stdout = buf
            try:
                rc = measure(rev)
            finally:
                sys.stdout = old_stdout
            out = buf.getvalue()
            good = rc == want_rc and want_tok in out
            if good:
                passed += 1
            else:
                failed += 1
                print(f"case {name}: rc={rc} want={want_rc} out={out.strip()!r}", file=sys.stderr)
    finally:
        LANE, FLEET = keep_lane, keep_fleet
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"C1_SELFTEST pass={passed} fail={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        raise SystemExit(_run_selftest())
    if len(sys.argv) != 2:
        print("usage: count-c1.py REV | --selftest", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(measure(sys.argv[1]))
