#!/usr/bin/env bash
command -v python3 >/dev/null 2>&1 || { printf 'error=python3_missing\nC2=unmet\n'; exit 2; }
exec python3 -I -B - "$@" <<'PY'
import json, math, os, re, shutil, subprocess, sys, tempfile
from collections import Counter
from pathlib import Path

LANE = os.environ.get("MORI_C2_LANE", "/home/vgpnk/Projects/shokunin/mori-shokunin")
TOOL, FROZEN, A2, NEW = "tools/mori-oom-killers.py", "tools/fixtures/mori-oom-killers/cases.json", "tools/fixtures/mori-oom-killers/cases-a2.json", "tools/fixtures/mori-oom-killers/cases-a2-r29.json"
CHECK, REPORT_DIR = ".ufo/waves/round-29/check-blind-wave.sh", ".ufo/waves/round-29/w1"
WRITERS = ("CaseA207a", "CaseA207b", "CaseA207c", "CaseA207d", "CaseA210a", "CaseA210b", "CaseA210c", "CaseA210d")
RULES = ("A2-07", "A2-10")
REQ = {"A2-07": ("earlyoom.actions.sigterm", "earlyoom.actions.sigkill", "earlyoom.dryrun_send_lines"), "A2-10": ("earlyoom.scope_complete", "earlyoom.actions.sigterm", "earlyoom.earlier_invocation_send_lines")}
SHAPE_PINS = {"A2-07": ("earlyoom.actions.sigterm", "earlyoom.actions.sigkill"), "A2-10": ("earlyoom.actions.sigterm", "earlyoom.actions.sigkill", "earlyoom.actions.escalations", "earlyoom.earlier_invocation_send_lines")}
BASES = {FROZEN: ("fc09f96c8036094bef06370dbb4b436edf96e6e3", 32), A2: ("d21b8bd38b1bf72ec903a19ed543c615564e8278", 30)}
TOP = {"schema", "note", "frozen_with", "sources", "cases"}; CASE = {"id", "why", "inputs", "expect", "rule", "author"}; INPUT = {"earlyoom_show", "oomd_show", "earlyoom_journal", "oomd_notices"}; EXPECT = {"verdict", "exit", "fields"}
AUTHOR_RULE = {n: ("A2-07" if n.startswith("CaseA207") else "A2-10") for n in WRITERS}
MARKER = "MORI_OOM_KILLERS_SELFTEST: "
VERSION = re.compile(r"\bversion\b|\bearlyoom\s+v?\d+(?:\.\d+)+\b", re.I); SEND = re.compile(r"\bsend(?:ing)?\b", re.I)


def run(argv, cwd=None, env=None): return subprocess.run(argv, cwd=cwd, env=env, capture_output=True)
def git(*args):
    p = run(["git", "-C", LANE, *args]); return p.stdout if p.returncode == 0 else None
def text(*args):
    b = git(*args); return None if b is None else b.decode("utf-8", "replace").strip()
def has(rev, path): return git("cat-file", "-e", "%s:%s" % (rev, path)) is not None
def strict_obj(pairs):
    d = {}
    for k, v in pairs:
        if k in d: raise ValueError("duplicate key")
        d[k] = v
    return d
def bad_constant(value): raise ValueError("non-standard number")
def finite_float(value):
    n = float(value)
    if not math.isfinite(n): raise ValueError("non-finite number")
    return n
def load(path):
    with open(path, encoding="utf-8") as f: return json.load(f, object_pairs_hook=strict_obj, parse_constant=bad_constant, parse_float=finite_float)
def canon(value): return json.dumps(value, sort_keys=True, separators=(",", ":"))
def selftest(root, tool, rel, want):
    p = run([sys.executable, "-I", "-B", str(tool), "--selftest", "--cases", rel], cwd=root)
    markers = [x for x in (p.stdout + p.stderr).decode("utf-8", "replace").splitlines() if x.startswith(MARKER)]
    if p.returncode: return "FAIL(exit=%d)" % p.returncode
    if len(markers) != 1: return "FAIL(markers=%d)" % len(markers)
    expected = MARKER + "PASS %d/%d" % (want, want)
    return "PASS %d/%d" % (want, want) if markers[0] == expected else "FAIL(marker_mismatch)"


def history(rev, path, extra=()):
    raw = text("-c", "core.quotePath=false", "log", "--full-history", "-m", "--follow", "--format=%H", "--name-status", *extra, rev, "--", path)
    entries, commit = [], None
    for line in (raw or "").splitlines():
        if re.fullmatch(r"[0-9a-f]{40}", line): commit = line
        elif line:
            p = line.split("\t"); status = p[0]
            if status[:1] in "AMDRCT": entries.append((commit, status, p[2] if status.startswith(("R", "C")) and len(p) > 2 else (p[1] if len(p) > 1 else path)))
    return entries


def freeze(rev, path, tip):
    all_e, adds = history(rev, path), sorted(set(history(rev, path, ("--diff-filter=A",))))
    def blob(c, p): return text("rev-parse", "-q", "--verify", "%s:%s" % (c, p)) if c else None
    def parents(c): return (text("rev-list", "--parents", "-n", "1", c) or "").split()[1:] if c else []
    genuine = [(c, p) for c, _, p in adds if c and not any(blob(parent, p) for parent in parents(c))]
    fc, fp = genuine[0] if len(genuine) == 1 else (None, None); fb = blob(fc, fp)
    versions = {b for c, _, p in all_e if p == path and (b := blob(c, p))}
    return {"freeze_commit": fc or "none", "freeze_path": fp or "none", "freeze_adds": len(genuine), "freeze_adds_raw": len(adds),
            "freeze_renames": sum(s.startswith("R") for _, s, _ in all_e), "freeze_deletes": sum(s.startswith("D") for _, s, _ in all_e),
            "freeze_edits": sum(s.startswith("M") for _, s, _ in all_e), "freeze_blob_versions": len(versions),
            "cases_changed_since_freeze": int(not (fc and fb and tip and fb == tip and len(versions) == 1)),
            "tool_blob_at_freeze": blob(fc, TOOL) or "none"}


def reports(rev):
    found, absent, errors = {}, [], 0
    for name in WRITERS:
        raw = git("show", "%s:%s/%s.md" % (rev, REPORT_DIR, name))
        if raw is None: absent.append(name); found[name] = None; continue
        try:
            m = re.search(rb"```json[ \t]*\r?\n(.*?)\r?\n```", raw, re.S | re.I)
            if not m: raise ValueError
            cases = json.loads(m.group(1), object_pairs_hook=strict_obj, parse_constant=bad_constant, parse_float=finite_float)
            if not isinstance(cases, list): raise ValueError
            found[name] = cases
        except (UnicodeError, ValueError, json.JSONDecodeError): found[name] = None; errors += 1
    return found, absent, errors


def show(show, key):
    for line in show.splitlines():
        k, sep, v = line.partition("=")
        if sep and k == key: return v.strip()
    return None
def mono(value):
    if isinstance(value, bool) or value is None: return None
    try: number = float(value)
    except (TypeError, ValueError, OverflowError): return None
    return number if math.isfinite(number) else None


def shape207(case):
    i = case["inputs"]
    if show(i["earlyoom_show"], "ActiveState") != "active": return False
    raw = show(i["earlyoom_show"], "ActiveEnterTimestampMonotonic"); start = mono(raw)
    if raw is not None and start is None: return False
    bounded = start is not None and start != 0; segments = []; current = None
    for r in i["earlyoom_journal"] or []:
        stamp = mono(r.get("__MONOTONIC_TIMESTAMP"))
        if stamp is None or (bounded and stamp < start): continue
        msg = r["MESSAGE"]
        if VERSION.search(msg): current = {"dry": False, "send": False}; segments.append(current)
        if current is not None:
            if "dryrun mode enabled" in msg.lower(): current["dry"] = True
            if SEND.search(msg) and not current["dry"]: current["send"] = True
    return len(segments) >= 2 and any(s["dry"] for s in segments) and any(s["send"] and not s["dry"] for s in segments)


def shape210(case):
    i = case["inputs"]; state = show(i["earlyoom_show"], "ActiveState"); raw = show(i["earlyoom_show"], "ActiveEnterTimestampMonotonic")
    if state == "active" and raw is not None and mono(raw) != 0: return False
    return any(SEND.search(r["MESSAGE"]) and mono(r.get("__MONOTONIC_TIMESTAMP")) is None for r in (i["earlyoom_journal"] or []))


def blind(rev, root):
    if not has(rev, CHECK): return "not_run", "not_run"
    repo = root / "blind-rev"; env = {k:v for k,v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
    if run(["git", "clone", "--shared", "--no-checkout", LANE, str(repo)], env=env).returncode: return "clone_failed", "unavailable"
    if run(["git", "-C", str(repo), "checkout", "--detach", rev], env=env).returncode: return "checkout_failed", "unavailable"
    p = run(["bash", str(repo / CHECK), rev, REPORT_DIR, r"^CaseA2(07|10)[a-d]\.md$"], cwd=repo, env=env)
    counts = re.findall(rb"(?m)^blind_violations=([0-9]+)$", p.stdout)
    return str(p.returncode), counts[0].decode() if len(counts) == 1 else "missing"


def case_error(c, seen, i):
    if not isinstance(c, dict) or set(c) != CASE: return "case_%d_keys_mismatch" % i
    if not isinstance(c["id"], str) or not c["id"] or not c["id"].isprintable(): return "case_%d_id_not_printable" % i
    if c["id"] in seen: return "duplicate_id"
    if c["rule"] not in RULES: return "case_%d_rule_not_allowed" % i
    a = c["author"]
    if not isinstance(a, str) or not a or not a.isprintable() or a not in AUTHOR_RULE or AUTHOR_RULE[a] != c["rule"]: return "case_%d_author_invalid" % i
    if not isinstance(c["why"], str): return "case_%d_why_not_string" % i
    x = c["inputs"]
    if not isinstance(x, dict) or set(x) != INPUT: return "case_%d_inputs_keys_mismatch" % i
    if not isinstance(x["earlyoom_show"], str) or not isinstance(x["oomd_show"], str): return "case_%d_show_input_not_string" % i
    if x["earlyoom_journal"] is not None and not isinstance(x["earlyoom_journal"], list): return "case_%d_journal_input_invalid" % i
    if isinstance(x["oomd_notices"], bool) or not isinstance(x["oomd_notices"], (int, float)) or (isinstance(x["oomd_notices"], float) and not math.isfinite(x["oomd_notices"])): return "case_%d_oomd_notices_invalid" % i
    journal = x["earlyoom_journal"] or []
    if any(not isinstance(r, dict) or not isinstance(r.get("MESSAGE"), str) for r in journal): return "case_%d_journal_record_invalid" % i
    if any(isinstance(r.get("__MONOTONIC_TIMESTAMP"), bool) or (r.get("__MONOTONIC_TIMESTAMP") is not None and not isinstance(r.get("__MONOTONIC_TIMESTAMP"), (str, int, float))) or (isinstance(r.get("__MONOTONIC_TIMESTAMP"), float) and not math.isfinite(r["__MONOTONIC_TIMESTAMP"])) for r in journal): return "case_%d_monotonic_timestamp_invalid" % i
    e = c["expect"]
    if not isinstance(e, dict) or set(e) != EXPECT: return "case_%d_expect_keys_mismatch" % i
    if not isinstance(e["verdict"], str): return "case_%d_verdict_not_string" % i
    if isinstance(e["exit"], bool) or not isinstance(e["exit"], int): return "case_%d_exit_not_integer" % i
    if not isinstance(e["fields"], dict) or not all(isinstance(k, str) for k in e["fields"]): return "case_%d_fields_invalid" % i
    return None


def main():
    if len(sys.argv) != 2: raise RuntimeError("usage_count-c2.sh_rev")
    if not shutil.which("git"): raise RuntimeError("git_missing")
    rev = text("rev-parse", "--verify", "-q", "%s^{commit}" % sys.argv[1])
    if not rev: raise RuntimeError("bad_rev")
    for p in (TOOL, FROZEN, A2):
        if not has(rev, p): raise RuntimeError("tool_absent" if p == TOOL else ("cases_absent" if p == FROZEN else "cases_a2_absent"))
    for p, base in ((FROZEN, BASES[FROZEN][0]), (A2, BASES[A2][0])):
        if not text("rev-parse", "--verify", "-q", "%s^{commit}" % base) or not has(base, p): raise RuntimeError("baseline_absent")
    out = []
    def emit(k, v): out.append("%s=%s" % (k, v))
    with tempfile.TemporaryDirectory(prefix="mori-c2-") as tmp:
        root = Path(tmp)
        for p in (TOOL, FROZEN, A2, NEW):
            raw = git("show", "%s:%s" % (rev, p))
            if raw is not None:
                dest = root / p; dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(raw)
        blobs = {p: text("rev-parse", "%s:%s" % (rev, p)) for p in (TOOL, FROZEN, A2)}
        bases = {p: text("rev-parse", "%s:%s" % (b, p)) for p, (b, _) in BASES.items()}
        have_new = has(rev, NEW); new_blob = text("rev-parse", "%s:%s" % (rev, NEW)) if have_new else "absent"
        emit("rev", rev); emit("tool_blob", blobs[TOOL]); emit("cases_blob", blobs[FROZEN]); emit("cases_baseline_blob", bases[FROZEN])
        emit("cases_blob_state", "match" if blobs[FROZEN] == bases[FROZEN] else "mismatch")
        emit("cases_a2_blob", blobs[A2]); emit("cases_a2_baseline_blob", bases[A2]); emit("cases_a2_blob_state", "match" if blobs[A2] == bases[A2] else "mismatch"); emit("cases_a2_r29_blob", new_blob)
        tool = root / TOOL; tests = {FROZEN: selftest(root, tool, FROZEN, 32), A2: selftest(root, tool, A2, 30)}
        emit("cases_selftest", tests[FROZEN]); emit("cases_a2_selftest", tests[A2])
        freeze_data = freeze(rev, NEW, new_blob) if have_new else {"freeze_commit":"none", "freeze_path":"none", "freeze_adds":0, "freeze_adds_raw":0, "freeze_renames":0, "freeze_deletes":0, "freeze_edits":0, "freeze_blob_versions":0, "cases_changed_since_freeze":1, "tool_blob_at_freeze":"none"}
        for k, v in freeze_data.items(): emit(k, v)
        report, missing, report_errors = reports(rev)
        for name in missing: emit("writer_absent", name)
        blind_exit, blind_count = blind(rev, root); emit("blind_exit", blind_exit); emit("blind_violations", blind_count)
        new_cases, schema, data = [], "", None
        if have_new:
            try:
                data = load(root / NEW); new_cases = data.get("cases", []) if isinstance(data, dict) and isinstance(data.get("cases"), list) else []
                if not isinstance(data, dict) or set(data) != TOP: schema = "top_level_keys_mismatch"
                elif any(not isinstance(data[k], str) or not data[k].strip() for k in ("schema", "note", "frozen_with")): schema = "metadata_invalid"
                elif not isinstance(data["sources"], list) or not data["sources"]: schema = "sources_invalid"
                elif not isinstance(data["cases"], list): schema = "cases_not_list"
            except (OSError, UnicodeError): schema = "unreadable"
            except json.JSONDecodeError as e: schema = "invalid_json_line_%d" % e.lineno
            except ValueError: schema = "invalid_json_or_duplicate_key"
            seen, valid_cases = set(), []
            if not schema:
                for i, c in enumerate(new_cases):
                    schema = case_error(c, seen, i)
                    if schema: break
                    seen.add(c["id"]); valid_cases.append(c)
            file_counts = Counter(canon(c) for c in new_cases); unselected = 0
            for items in report.values():
                if items is not None:
                    for item in items:
                        key = canon(item)
                        if file_counts[key]: file_counts[key] -= 1
                        else: unselected += 1
            matched = sum(1 for c in new_cases if isinstance(c, dict) and isinstance(c.get("author"), str) and report.get(c["author"]) is not None and canon(c) in {canon(x) for x in report[c["author"]]})
            emit("provenance", "%d/%d unselected=%d" % (matched, len(new_cases), unselected)); emit("provenance_errors", report_errors)
        else:
            unselected = sum(len(x) for x in report.values() if x is not None); matched = 0
            emit("provenance", "0/0 unselected=%d" % unselected); emit("provenance_errors", report_errors)
        valid, rule_fail, shape_ok, input_ok = False, [], False, False
        if not have_new:
            emit("a2_r29_schema", "absent"); emit("a2_r29_cases", 0); emit("a2_r29_ids", "absent"); emit("a2_r29_rules_covered", "0/2")
            emit("a2_r29_distinct_inputs", "0/0"); emit("a2_r29_legacy_input_overlaps", 0); emit("a2_r29_input_checks", "fail:file_absent")
            emit("a2_r29_rule_checks", "fail:file_absent"); emit("shape_a207", "0/0"); emit("shape_a210", "0/0"); emit("a2_r29_selftest", "absent")
        elif schema:
            emit("a2_r29_schema", "error " + schema); emit("a2_r29_cases", len(new_cases)); emit("a2_r29_ids", "invalid")
            emit("a2_r29_rules_covered", "0/2"); emit("a2_r29_distinct_inputs", "0/%d" % len(new_cases)); emit("a2_r29_legacy_input_overlaps", 0)
            emit("a2_r29_input_checks", "fail:schema"); emit("a2_r29_rule_checks", "fail:schema"); emit("shape_a207", "0/0"); emit("shape_a210", "0/0"); emit("a2_r29_selftest", "skipped_schema")
        else:
            n = len(new_cases); per = {r:{"n":0,"inputs":set(),"authors":set(),"unpinned":0} for r in RULES}
            for c in valid_cases:
                e = per[c["rule"]]; e["n"] += 1; e["inputs"].add(canon(c["inputs"])); e["authors"].add(c["author"])
                if not any(k in c["expect"]["fields"] for k in REQ[c["rule"]]): e["unpinned"] += 1
            old_inputs, legacy_errors = set(), 0
            for p in (root / FROZEN, root / A2):
                try:
                    old = load(p)
                    if not isinstance(old, dict) or not isinstance(old.get("cases"), list): legacy_errors += 1; continue
                    for c in old["cases"]:
                        if not isinstance(c, dict) or not isinstance(c.get("inputs"), dict): legacy_errors += 1
                        else: old_inputs.add(canon(c["inputs"]))
                except (OSError, UnicodeError, ValueError, json.JSONDecodeError): legacy_errors += 1
            distinct = len({canon(c["inputs"]) for c in valid_cases}); overlap = len({canon(c["inputs"]) for c in valid_cases} & old_inputs)
            shapes = {r:[] for r in RULES}
            for c in valid_cases:
                f, r = c["expect"]["fields"], c["rule"]
                pin = any(type(f.get(k)) is int and (r != "A2-07" or f[k] > 0) for k in SHAPE_PINS[r])
                if pin and ((r == "A2-07" and shape207(c)) or (r == "A2-10" and shape210(c))): shapes[r].append(c)
            sh = {r: "%d/%d" % (len(shapes[r]), len({c["author"] for c in shapes[r]})) for r in RULES}
            for r in RULES:
                e=per[r]
                if e["n"] < 6: rule_fail.append(r+"(cases<6)")
                if len(e["inputs"]) < 2: rule_fail.append(r+"(distinct_inputs<2)")
                if len(e["authors"]) < 3: rule_fail.append(r+"(authors<3)")
                if e["unpinned"]: rule_fail.append(r+"(case_missing_required_field)")
                emit("a2_r29_%s" % r, "cases=%d distinct=%d authors=%d unpinned=%d" % (e["n"],len(e["inputs"]),len(e["authors"]),e["unpinned"]))
            if n < 12: rule_fail.append("total_cases<12")
            shape_ok = all(len(shapes[r]) >= 2 and len({c["author"] for c in shapes[r]}) >= 2 for r in RULES)
            input_ok = distinct == n and overlap == 0 and legacy_errors == 0
            emit("a2_r29_schema", "ok"); emit("a2_r29_cases", n); emit("a2_r29_ids", "unique_printable")
            emit("a2_r29_rules_covered", "%d/2" % sum(per[r]["n"] > 0 for r in RULES)); emit("a2_r29_distinct_inputs", "%d/%d" % (distinct,n))
            emit("a2_r29_legacy_input_overlaps", overlap); emit("shape_a207", sh["A2-07"]); emit("shape_a210", sh["A2-10"])
            emit("a2_r29_rule_checks", "fail:"+" ".join(rule_fail) if rule_fail else "ok"); emit("a2_r29_shape_checks", "ok" if shape_ok else "fail:shape_threshold")
            emit("a2_r29_input_checks", "ok" if input_ok else "fail:input_distinctness")
            new_test = selftest(root, root / TOOL, NEW, n); emit("a2_r29_selftest", new_test)
            valid = not rule_fail and shape_ok and input_ok and matched == n and unselected == 0 and report_errors == 0 and new_test == "PASS %d/%d" % (n,n)
        ok = valid and blobs[FROZEN] == bases[FROZEN] and blobs[A2] == bases[A2] and tests[FROZEN] == "PASS 32/32" and tests[A2] == "PASS 30/30"
        ok = ok and freeze_data["freeze_adds"] == 1 and freeze_data["freeze_renames"] == 0 and freeze_data["freeze_deletes"] == 0 and freeze_data["cases_changed_since_freeze"] == 0
        ok = ok and blind_exit == "0" and blind_count == "0"
    print("\n".join(out)); print("C2=met" if ok else "C2=unmet"); return 0 if ok else 1

try:
    sys.exit(main())
except RuntimeError as e:
    print("error=%s\nC2=unmet" % e); sys.exit(2)
except Exception:
    print("error=internal_error\nC2=unmet"); sys.exit(2)
PY
