#!/usr/bin/env python3
"""Active capabilities-register checker (round 59, C1 — calibration capability).

Reads a SCORECARD.md-shaped file and a MANIFEST.json-shaped file and verifies
that the *active* capabilities register — the unique `## Capabilities` section
whose own preamble declares "current capabilities register" — binds a required
set of `rounds[i].capabilities_added[j]` keys:

  * register identity: exactly one `## Capabilities` section self-declares as
    the current register (a superseded stub does not declare; two declarers
    are ambiguous);
  * keys: every --require'd key appears exactly once anywhere in the register
    table (duplicates anywhere fail; extra non-required rows are ignored);
  * names: for each required row the `capability` cell is nonempty and equals
    the leading name of the MANIFEST string at rounds[i].capabilities_added[j]
    (`name` == string, or string starts with `name (` or `name,` — a bare
    substring hit does NOT bind);
  * manifest object: rounds[i] exists, `lane` == `mori`, and the row's
    `first-working round` cell equals rounds[i].lane_round (integer);
  * pointers: every backticked token of the `evidence` cell is a nonempty
    lane-relative path (never absolute, never containing `..` or `~`), and
    each exists as a file under --root.

Fixture-friendly: file paths come from argv, nothing inside the lane repo is
assumed.  Exit 0 prints `REGISTER_MET`; anything else prints `REGISTER_UNMET`
with machine reasons and exits 1; setup errors exit 2.

Usage:
  mori-register-check.py --scorecard F --manifest F --root DIR
      --require 'rounds[832].capabilities_added[0]' [--require K ...]
  mori-register-check.py --selftest [--scratch DIR]

Selftest builds fixture roots under DIR (default: TMPDIR/mori-register-check*)
and prints `REGCHECK_SELFTEST pass=N fail=0`, exit 0 iff fail=0.
"""
import json
import os
import re
import sys
import tempfile
from pathlib import Path

SCHEMA = "mori-register-check-v1"
DECLARE = "current capabilities register"
LANE = "mori"
CAP_HEAD = re.compile(r"^## Capabilities\b")
SEC_HEAD = re.compile(r"^## ")
KEY_CELL = re.compile(r"^`rounds\[(\d+)\]\.capabilities_added\[(\d+)\]`$")
ROW_START = re.compile(r"^\|")
HEADER = re.compile(r"^\|\s*key\s*\|")
BACKTICK = re.compile(r"`([^`]*)`")


def scorecard_sections(lines):
    """[(start,end,title)] for every `## ` section."""
    heads = [(i, ln) for i, ln in enumerate(lines) if SEC_HEAD.match(ln)]
    out = []
    for j, (i, ln) in enumerate(heads):
        end = heads[j + 1][0] if j + 1 < len(heads) else len(lines)
        out.append((i, end, ln))
    return out


def register_table(lines):
    """Locate the unique self-declared current register; return
    (rows, n_declared, n_caps).  rows = [(lineno1, cells)] of | rows under the
    `| key |` header inside that section."""
    caps = [(s, e) for s, e, t in scorecard_sections(lines) if CAP_HEAD.match(t)]
    declared = [(s, e) for s, e in caps
                if DECLARE in "\n".join(lines[s:e])]
    rows = []
    if len(declared) == 1:
        s, e = declared[0]
        in_table = False
        for i in range(s, e):
            ln = lines[i]
            if not in_table:
                if HEADER.match(ln):
                    in_table = True
                continue
            if not ROW_START.match(ln):
                if rows:
                    break
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            rows.append((i + 1, cells))
    return rows, len(declared), len(caps)


def pointer_ok(tok):
    if not tok or not tok.strip():
        return False
    t = tok.strip()
    if t.startswith("/") or t.startswith("~"):
        return False
    if ".." in t.split("/"):
        return False
    if t.startswith("./"):
        t = t[2:]
    return bool(t)


def check(scorecard_path, manifest_path, root, require):
    reasons = []
    bound = {}
    all_ptrs = []
    try:
        text = Path(scorecard_path).read_text(encoding="utf-8")
    except OSError:
        return None, ["scorecard_unreadable"], {"bound": bound, "pointers": all_ptrs}
    lines = text.splitlines()
    rows, n_decl, n_caps = register_table(lines)
    if n_decl != 1:
        reasons.append("binding:declared_register=%d(capabilities_sections=%d)"
                       % (n_decl, n_caps))
    keymap = {}
    dup = []
    for _ln, cells in rows:
        if not cells:
            continue
        m = KEY_CELL.match(cells[0])
        if not m:
            continue
        key = cells[0][1:-1]
        if key in keymap:
            dup.append(key)
        keymap[key] = cells
    if dup:
        reasons.append("keys:duplicate=%s" % ",".join(sorted(set(dup))))
    try:
        manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        rounds = manifest.get("rounds")
        if not isinstance(rounds, list):
            raise ValueError("rounds")
    except (OSError, ValueError, AttributeError):
        rounds = None
        reasons.append("manifest:unreadable")
    for want in require:
        cells = keymap.get(want)
        if cells is None:
            reasons.append("keys:missing=%s" % want)
            continue
        if len(cells) < 5:
            reasons.append("keys:short_row=%s" % want)
            continue
        name = cells[1]
        if not name:
            reasons.append("keys:empty_name=%s" % want)
            continue
        m = KEY_CELL.match(cells[0])
        ri, cai = int(m.group(1)), int(m.group(2))
        entry = None
        if rounds is not None:
            if ri >= len(rounds) or not isinstance(rounds[ri], dict):
                reasons.append("manifest:index_missing=%s" % want)
            else:
                obj = rounds[ri]
                if obj.get("lane") != LANE:
                    reasons.append("manifest:lane=%r" % obj.get("lane"))
                cap = obj.get("capabilities_added")
                if not isinstance(cap, list) or cai >= len(cap) \
                        or not isinstance(cap[cai], str):
                    reasons.append("manifest:entry_missing=%s" % want)
                else:
                    entry = cap[cai]
                    if not (entry == name or entry.startswith(name + " (")
                            or entry.startswith(name + ",")):
                        reasons.append("manifest:name=%s" % want)
                lr = obj.get("lane_round")
                if cells[4] != str(lr):
                    reasons.append("manifest:lane_round=%s" % want)
        ptrs = BACKTICK.findall(cells[3])
        all_ptrs.extend(ptrs)
        if not ptrs:
            reasons.append("pointers:none=%s" % want)
        for p in ptrs:
            if not pointer_ok(p):
                reasons.append("pointers:bad=%s" % p)
                continue
            rel = p[2:] if p.startswith("./") else p
            if not (Path(root) / rel).is_file():
                reasons.append("pointers:missing=%s" % p)
        if entry is not None:
            bound[want] = entry
    return (len(reasons) == 0), reasons, {"bound": bound, "pointers": all_ptrs}


def emit(ok, reasons, info):
    out = {"schema": SCHEMA,
           "verdict": "REGISTER_MET" if ok else "REGISTER_UNMET",
           "reasons": reasons, "bound": info.get("bound", {}),
           "pointers": info.get("pointers", [])}
    print(json.dumps(out, sort_keys=True))
    return 0 if ok else 1




# ---------------- selftest ----------------

STUB = ("# s\n\n## Capabilities\n\n| key | capability | what | evidence | first-working round |\n"
        "|---|---|---|---|---|\n| — none yet — | | | | |\n")


def _fixture(root, scorecard, manifest, paths=()):
    root = Path(root)
    (root / "scorecard.md").write_text(scorecard)
    (root / "manifest.json").write_text(manifest)
    for p in paths:
        f = root / p
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("x\n")


def _reg_section(extra_rows=""):
    return ("## Capabilities\n\nThis is the lane's current capabilities register.\n\n"
            "| key | capability | what it can now do | evidence | first-working round |\n"
            "|---|---|---|---|---|\n"
            "| `rounds[832].capabilities_added[0]` | alpha bind | does a. | `tools/a.py`; `.ufo/waves/round-56/evidence/e1.txt` | 56 |\n"
            "| `rounds[832].capabilities_added[1]` | beta probe | does b. | `tools/b.py` | 56 |\n"
            + extra_rows)


def _manifest(cap0="alpha bind (does a)", cap1="beta probe (does b)", lane="mori", lane_round=56, n=833, at=832):
    rounds = [{} for _ in range(n)]
    rounds[at] = {"lane": lane, "lane_round": lane_round,
                  "capabilities_added": [cap0, cap1]}
    return json.dumps({"rounds": rounds})


REQ = ["rounds[832].capabilities_added[0]", "rounds[832].capabilities_added[1]"]
PTRS = ("tools/a.py", ".ufo/waves/round-56/evidence/e1.txt", "tools/b.py")


def selftest(scratch=None):
    base = Path(scratch or tempfile.mkdtemp(prefix="mori-register-check-",
                                            dir=os.environ.get("TMPDIR") or None))
    base.mkdir(parents=True, exist_ok=True)
    passed = failed = 0

    def case(name, scorecard, manifest, paths, want_ok, want_reason=None, req=REQ):
        nonlocal passed, failed
        d = base / name
        d.mkdir(parents=True, exist_ok=True)
        _fixture(d, scorecard, manifest, paths)
        ok, reasons, _b = check(d / "scorecard.md", d / "manifest.json", d, req)
        good = (ok == want_ok) and (want_reason is None or any(
            r.startswith(want_reason) for r in reasons))
        if good:
            passed += 1
        else:
            failed += 1
            print("FAIL %s: ok=%s reasons=%s" % (name, ok, reasons), file=sys.stderr)

    good_sc = STUB + "\n" + _reg_section()
    case("met", good_sc, _manifest(), PTRS, True)
    case("stub_only", STUB, _manifest(), PTRS, False, "binding")
    case("two_declared", _reg_section() + "\n## Capabilities\n\nThis is the lane's current capabilities register.\n",
         _manifest(), PTRS, False, "binding")
    case("dup_key", good_sc + "| `rounds[832].capabilities_added[0]` | gamma | g. | `tools/a.py` | 56 |\n",
         _manifest(), PTRS, False, "keys:duplicate")
    case("missing_pointer", good_sc, _manifest(), PTRS[:1], False, "pointers:missing")
    case("abs_pointer", STUB + "\n" + _reg_section().replace("`tools/a.py`", "`/etc/passwd`", 1),
         _manifest(), PTRS, False, "pointers:bad")
    case("wrong_name", good_sc, _manifest(cap0="gamma bind (does a)"), PTRS, False, "manifest:name")
    case("substring_only", good_sc, _manifest(cap0="xxalpha bind"), PTRS, False, "manifest:name")
    case("wrong_index", good_sc, _manifest(n=900, at=700), PTRS, False, "manifest:")
    case("foreign_lane", good_sc, _manifest(lane="kotoba"), PTRS, False, "manifest:lane")
    case("missing_key", STUB + "\n" + _reg_section().replace("`rounds[832].capabilities_added[1]`",
                                                             "`rounds[999].capabilities_added[0]`"),
         _manifest(), PTRS, False, "keys:missing")
    case("no_table", STUB + "\n## Capabilities\n\nThis is the lane's current capabilities register.\n",
         _manifest(), PTRS, False, "keys:missing")
    line = "REGCHECK_SELFTEST pass=%d fail=%d" % (passed, failed)
    print(line)
    return 0 if failed == 0 else 1


def main(argv):
    if "--selftest" in argv:
        i = argv.index("--scratch") if "--scratch" in argv else -1
        scratch = argv[i + 1] if 0 <= i < len(argv) - 1 else None
        return selftest(scratch)
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--scorecard", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--require", action="append", default=[])
    a = ap.parse_args(argv)
    ok, reasons, bound = check(a.scorecard, a.manifest, a.root, a.require)
    if ok is None:
        print(json.dumps({"schema": SCHEMA, "verdict": "REGISTER_UNMET",
                          "reasons": reasons, "bound": {}}))
        return 1
    return emit(ok, reasons, bound)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
