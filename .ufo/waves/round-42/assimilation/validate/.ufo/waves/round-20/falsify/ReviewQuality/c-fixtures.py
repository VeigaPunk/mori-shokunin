#!/usr/bin/env python3
# Scratch checks for MoriR20.ReviewQuality (falsification of QUALITY 64-68).
# Read-only against the lane: runs the lane's tools/mori-wave-settlement.py `scan` and the lane's
# register checker. Fixture trees and copies live under /tmp/rq-fixtures, never under .ufo/waves/,
# so no fixture dispatch file can enter a lane scan. Writes c-results.txt beside this file.
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
TOOL = os.path.join(LANE, "tools/mori-wave-settlement.py")
CHECK = os.path.join(LANE, ".ufo/waves/round-20/build/RegisterCheck/check-register.py")
REG = os.path.join(LANE, "corpus/evidence/drift-classification-r20.json")
R13 = os.path.join(LANE, ".ufo/waves/round-13/evidence/drift-classification.json")
DRIFT = os.path.join(LANE, ".ufo/waves/round-20/evidence/c1-drift-entering.json")
RECEIPT = os.path.join(LANE, ".ufo/waves/round-20/evidence/c2-live-mori.json")
KNOWLEDGE = os.path.join(LANE, "corpus/knowledge/drift-repin-r20.md")
LESSON = os.path.join(LANE, "corpus/lessons/round-20.md")
VOLATILE = os.path.join(LANE, ".ufo/waves/round-20/build/VolatileContract.md")
FX = "/tmp/rq-fixtures"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c-results.txt")
lines = []


def say(text):
    lines.append(text)
    print(text)


def sha256(path):
    with open(path, "rb") as stream:
        return hashlib.sha256(stream.read()).hexdigest()


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as stream:
        stream.write(data if isinstance(data, bytes) else data.encode("utf-8"))


def dispatch(members, schema="ufo-swarm-wave-dispatch-v1"):
    tasks = []
    for name, rel in members:
        body = "Fixture task body\n"
        if rel is not None:
            body += "Report: write your scoped findings to " + rel
        tasks.append({"name": name, "agent": "reviewer", "task": body})
    return json.dumps({"schema": schema, "wave": "fx", "taskCall": {"tasks": tasks}}).encode()


def rep(name):
    return ".ufo/waves/round-1/build/%s.md" % name


def scan(lane_root):
    proc = subprocess.run([sys.executable, TOOL, "scan", "--lane-root", lane_root],
                          capture_output=True, text=True)
    try:
        doc = json.loads(proc.stdout)
    except ValueError:
        doc = None
    return proc.returncode, doc, proc.stderr.strip()[-200:]


def keys_below(obj, acc):
    if isinstance(obj, dict):
        for key, value in obj.items():
            acc.add(key)
            keys_below(value, acc)
    elif isinstance(obj, list):
        for value in obj:
            keys_below(value, acc)
    return acc


def drift_tokens(path):
    stdout = json.load(open(path, encoding="utf-8"))["stdout"]
    out = set()
    for line in stdout.split("\n"):
        for token in line.split(" "):
            if token and token != "MORI_DRIFT:":
                out.add(token)
    return out


say("tool_sha256 " + sha256(TOOL))
say("check_register_sha256 " + sha256(CHECK))
say("register_sha256 " + sha256(REG))
say("quality_sha256 " + sha256(os.path.join(LANE, "corpus/QUALITY.md")))
say("lesson_sha256 " + sha256(LESSON))
say("receipt_sha256 " + sha256(RECEIPT))

shutil.rmtree(FX, ignore_errors=True)

# A: one wave with a present, an empty, a stub and a missing member
a = os.path.join(FX, "A", "lane")
write(os.path.join(a, ".ufo/waves/round-1/dispatch.json"),
      dispatch([("MemberPresent", rep("A")), ("MemberEmpty", rep("B")),
                ("MemberStub", rep("C")), ("MemberMissing", rep("D"))]))
write(os.path.join(a, rep("A")), b"report\n")
write(os.path.join(a, rep("B")), b"")
write(os.path.join(a, rep("C")), b"STATUS: started\n")
rc, doc, err = scan(a)
wave = doc["waves"][0]
say("A rc=%d state=%s counts=%s missing_names=%s" % (
    rc, wave["state"], json.dumps(wave["counts"], sort_keys=True), wave["missing"]))
say("A payload_keys_anywhere_with_time=%s" % sorted(k for k in keys_below(doc, set()) if "time" in k.lower()))

# B: lane with no .ufo/waves at all (legitimate zero) and C: .ufo/waves is a symlink to a real dispatch
b = os.path.join(FX, "B", "lane")
write(os.path.join(b, "README.md"), "no dispatch record here\n")
rc, doc, err = scan(b)
say("B no_waves_dir rc=%d waves=%d ignored=%d unreadable=%d" % (
    rc, len(doc["waves"]), doc["ignored_json"], doc["unreadable_json"]))

c = os.path.join(FX, "C", "lane")
elsewhere = os.path.join(FX, "C", "elsewhere")
write(os.path.join(elsewhere, "round-1", "dispatch.json"), dispatch([("Ok", "reports/OK.md")]))
write(os.path.join(c, "reports", "OK.md"), b"report\n")
os.makedirs(os.path.join(c, ".ufo"), exist_ok=True)
os.symlink(elsewhere, os.path.join(c, ".ufo", "waves"))
rc, doc, err = scan(c)
say("C symlinked_waves_dir_with_one_dispatch rc=%d waves=%d ignored=%d unreadable=%d" % (
    rc, len(doc["waves"]), doc["ignored_json"], doc["unreadable_json"]))

# D: one settled wave beside an unreadable dispatch-shaped file and a dispatch with another schema
d = os.path.join(FX, "D", "lane")
write(os.path.join(d, ".ufo/waves/round-1/dispatch.json"), dispatch([("Ok", rep("OK"))]))
write(os.path.join(d, rep("OK")), b"report\n")
write(os.path.join(d, ".ufo/waves/round-1/dispatch-truncated.json"),
      b'{"schema":"ufo-swarm-wave-dispatch-v1","wave":"x","taskCall":{"tasks":[')
write(os.path.join(d, ".ufo/waves/round-1/dispatch-v2.json"),
      dispatch([("Lost", rep("LOST"))], schema="ufo-swarm-wave-dispatch-v2"))
rc, doc, err = scan(d)
say("D rc=%d waves=%d states=%s ignored=%d unreadable=%d" % (
    rc, len(doc["waves"]), [x["state"] for x in doc["waves"]], doc["ignored_json"], doc["unreadable_json"]))

# E: seat start-marker byte variants
e = os.path.join(FX, "E", "lane")
variants = {"Exact": b"STATUS: started", "ExactNL": b"STATUS: started\n",
            "CRLF": b"STATUS: started\r\n", "DoubleNL": b"STATUS: started\n\n",
            "Space": b"STATUS: started \n", "Lower": b"status: started\n"}
write(os.path.join(e, ".ufo/waves/round-1/dispatch.json"), dispatch([(k, rep("E-" + k)) for k in variants]))
for k, v in variants.items():
    write(os.path.join(e, rep("E-" + k)), v)
rc, doc, err = scan(e)
say("E rc=%d state=%s members=%s" % (
    rc, doc["waves"][0]["state"], {m["name"]: m["status"] for m in doc["waves"][0]["members"]}))

# Live receipt (10:46Z) internal consistency
receipt = json.load(open(RECEIPT, encoding="utf-8"))
say("receipt top_keys=%s" % sorted(receipt.keys()))
say("receipt time_like_keys=%s" % sorted(k for k in keys_below(receipt, set()) if "time" in k.lower() or "utc" in k.lower()))
say("receipt waves=%d unreadable=%d ignored=%d" % (
    receipt["totals"]["waves"], receipt["unreadable_json"], receipt["ignored_json"]))
say("receipt sum(len(missing_names))=%d sum(counts.missing)=%d sum(counts.stub)=%d" % (
    sum(len(w["missing"]) for w in receipt["waves"]),
    sum(w["counts"]["missing"] for w in receipt["waves"]),
    sum(w["counts"]["stub"] for w in receipt["waves"])))
for w_ in receipt["waves"]:
    if w_["counts"]["stub"]:
        say("receipt stub_wave=%s state=%s counts.missing=%d len(missing)=%d" % (
            w_["dispatch_path"], w_["state"], w_["counts"]["missing"], len(w_["missing"])))

# Current lane waves tree, scanned with the tool's own discovery functions (import from a copy)
copy_dir = os.path.join(FX, "tool-copy")
os.makedirs(copy_dir, exist_ok=True)
copy = os.path.join(copy_dir, "mws_copy.py")
shutil.copyfile(TOOL, copy)
spec = importlib.util.spec_from_file_location("mws_copy", copy)
mws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mws)
found = mws._dispatch_files(mws._wave_root(LANE))
v1, unreadable = [], []
for path, rel in found:
    raw = mws._read_regular_bytes(path)
    if raw is None:
        unreadable.append((rel, "no-bytes", False))
        continue
    try:
        document = json.loads(raw, parse_constant=mws._reject_json_constant)
    except ValueError:
        unreadable.append((rel, "decode", b"ufo-swarm-wave-dispatch-v1" in raw))
        continue
    if isinstance(document, dict) and document.get("schema") == mws.DISPATCH_SCHEMA:
        v1.append(rel)
say("waves_tree json_files=%d dispatch_v1=%d unreadable=%d" % (len(found), len(v1), len(unreadable)))
for item in unreadable:
    say("  unreadable %s kind=%s has_dispatch_schema_bytes=%s" % item)
residual = json.load(open(os.path.join(LANE, ".ufo/waves/round-18/residual-drafting-taskcall.json"), encoding="utf-8"))
say("residual_round18 schema=%s note_prefix=%r" % (residual.get("schema"), residual.get("note", "")[:60]))

# Register: counting command (set difference) versus the strict checker, on the lane file and on mutants
drift = drift_tokens(DRIFT)
reg = json.load(open(REG, encoding="utf-8"))
r13 = json.load(open(R13, encoding="utf-8"))


def counting(obj):
    return len(drift - set(obj["tokens"].keys()))


def strict(path):
    proc = subprocess.run([sys.executable, CHECK, path, DRIFT], capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip()


say("drift_tokens=%d register_tokens=%d" % (len(drift), len(reg["tokens"])))
say("r13 counting_unclassified=%d" % counting(r13))
say("r13 strict=%s" % (strict(R13),))
say("r20 counting_unclassified=%d" % counting(reg))
say("r20 strict=%s" % (strict(REG),))
mutants = {}
m1 = json.loads(json.dumps(reg))
m1["tokens"]["+SURFACE:lane.audio"]["class"] = "census-regression"
mutants["m1-regression"] = m1
m2 = json.loads(json.dumps(reg))
m2["tokens"]["+SURFACE:lane.chousa"]["class"] = "maybe-live"
mutants["m2-badclass"] = m2
m3 = json.loads(json.dumps(reg))
m3["tokens"]["+SURFACE:lane.lore"].pop("evidence", None)
mutants["m3-noevidence"] = m3
for name, obj in mutants.items():
    path = os.path.join(FX, name + ".json")
    write(path, json.dumps(obj, indent=1, ensure_ascii=False))
    say("%s counting_unclassified=%d strict=%s" % (name, counting(obj), strict(path)))

counts = {}
for value in reg["tokens"].values():
    counts[value["class"]] = counts.get(value["class"], 0) + 1
say("register class_counts=%s" % sorted(counts.items()))
knowledge_text = open(KNOWLEDGE, encoding="utf-8").read()
say("knowledge_note_claims_29_19_2=%s" % ("census-schema-change 29" in knowledge_text and "roster-change 2" in knowledge_text))
for key in sorted(k for k in reg["tokens"] if k.startswith("-")):
    value = reg["tokens"][key]
    say("minus %s class=%s blind_spot=%s" % (key, value["class"], bool(value.get("blind_spot"))))

lesson_text = open(LESSON, encoding="utf-8").read()
volatile_text = open(VOLATILE, encoding="utf-8").read()
say("lesson_mentions_adjudication=%s" % ("Adjudicat" in lesson_text))
say("volatile_contract_has_H2_or_H3=%s" % ("H2" in volatile_text or "H3" in volatile_text))

with open(OUT, "w", encoding="utf-8") as stream:
    stream.write("\n".join(lines) + "\n")
say("wrote " + OUT)
