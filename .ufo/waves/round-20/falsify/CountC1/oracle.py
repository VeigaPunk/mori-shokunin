#!/usr/bin/env python3
"""CountC1 falsify oracle (scratch; read-only inputs under the lane).

Set-level truth for C1, computed without comm/sort:
  contract model  = tr ' ' '\n' | grep -v '^MORI_DRIFT:$' | grep . | sort -u
  checker model   = check-register.py drift_tokens (str.split, drop 'MORI_DRIFT:')
"""
import json
import re
from collections import Counter
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mori-shokunin")
S = LANE / ".ufo/waves/round-20/falsify/CountC1"
E = LANE / ".ufo/waves/round-20/evidence"
R13 = LANE / ".ufo/waves/round-13/evidence/drift-classification.json"
R20 = LANE / "corpus/evidence/drift-classification-r20.json"


def load(p):
    return Path(p).read_text(encoding="utf-8")


def contract_model(text):
    lines = text.replace(" ", "\n").split("\n")
    return {ln for ln in lines if ln and ln != "MORI_DRIFT:"}


def checker_model(text):
    return {w for w in text.split() if w != "MORI_DRIFT:"}


def keys_of(p):
    return set(json.loads(load(p))["tokens"].keys())


def anomalies(text):
    out = {}
    for ch in text:
        if ch in " \n":
            continue
        if ch.isspace() or ord(ch) < 32 or ord(ch) > 126:
            k = f"U+{ord(ch):04X}"
            out[k] = out.get(k, 0) + 1
    return out


entering_stdout = load(S / "drift-entering.stdout.txt")
r10_line1 = load(S / "drift-r10-prepin.line1.txt")
r10_full = load(E / "c1-drift-r10-prepin.txt")
postpin = load(E / "c1-drift-r20-postpin.txt")
ej = json.loads(load(E / "c1-drift-entering.json"))

print("== capture integrity")
print("jq -r .stdout scratch == json.stdout + newline:", entering_stdout == ej["stdout"] + "\n")
print("json token_count/unclassified_count/rc:", ej["token_count"], ej["unclassified_count"], ej["rc"])
print("json tokens list == contract model of stdout:", set(ej["tokens"]) == contract_model(entering_stdout),
      "len", len(ej["tokens"]), "distinct", len(set(ej["tokens"])))

print("== token-splitting audit (per capture)")
for label, text in [("entering", entering_stdout), ("r10_line1", r10_line1),
                    ("r10_whole_file", r10_full), ("postpin_whole_file", postpin)]:
    words = text.split()
    print(f"{label}: chars={len(text)} newlines={text.count(chr(10))} ws_words={len(words)} "
          f"distinct_ws_words={len(set(words))} contract_tokens={len(contract_model(text))} "
          f"checker_tokens={len(checker_model(text))} tab={'\t' in text} cr={'\r' in text} "
          f"nonascii_or_ctrl={anomalies(text)}")
    print(f"  contract==checker model: {contract_model(text) == checker_model(text)}")

ent = contract_model(entering_stdout)
r10 = contract_model(r10_line1)
print("== set differences between captures")
print("entering - r10_line1:", sorted(ent - r10))
print("r10_line1 - entering:", sorted(r10 - ent))

r13 = keys_of(R13)
r20 = keys_of(R20)
print("== counts (set semantics)")
for name, toks in [("entering", ent), ("r10_line1", r10)]:
    for rname, rk in [("r13", r13), ("r20", r20)]:
        miss = sorted(toks - rk)
        print(f"{name} vs {rname}: unclassified={len(miss)} {miss}")
print("r13 keys:", len(r13), "orphans (keys not in entering):", sorted(r13 - ent))
print("r20 keys:", len(r20), "r20 keys == entering tokens:", r20 == ent,
      "r20-only:", sorted(r20 - ent), "entering-only:", sorted(ent - r20))
print("entering - r13 == json unclassified_vs_prior_register:",
      sorted(ent - r13) == sorted(ej["unclassified_vs_prior_register"]))

print("== r20 register classes")
r20doc = json.loads(load(R20))
print("schema:", r20doc["schema"], "round:", r20doc["round"])
print("class counts (computed):", dict(Counter(v["class"] for v in r20doc["tokens"].values())))
print("class counts (declared):", r20doc["class_counts"])
empties = [k for k, v in r20doc["tokens"].items() if not (v.get("reason", "").strip() and v.get("evidence", "").strip())]
print("entries with empty reason/evidence:", empties)
for tok in ["-FINDING:WATCHDOG_STALE", "-FINDING:WAVE_UNSETTLED_AGE"]:
    print("DISSENT TOKEN", tok, json.dumps(r20doc["tokens"][tok], ensure_ascii=False))

print("== evidence path pointers (lane-relative, existence only)")
pat = re.compile(r"(?<![\w/.-])((?:\.ufo|tools|corpus|templates|scripts)/[\w./-]+)")
checked = {}
for tok, v in r20doc["tokens"].items():
    for m in pat.finditer(v.get("evidence", "")):
        p = m.group(1).rstrip(".,;:")
        p = re.sub(r"\.(?=$)", "", p)
        if p not in checked:
            checked[p] = (LANE / p).exists()
missing = sorted(p for p, ok in checked.items() if not ok)
print("pointer paths checked:", len(checked), "missing:", missing)
