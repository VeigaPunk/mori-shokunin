#!/usr/bin/env python3
# Re-open checks for S072 (Wikipedia, Characterization test). Read-only: lane files and scratch copies only.
import hashlib, html, json, os, re, sys
from collections import Counter
from pathlib import Path

BASE = Path("/home/vgpnk/Projects/shokunin/mori-shokunin")
SCR = BASE / ".ufo/waves/round-20/falsify/ReopenS072"
Q = "a means to describe (characterize) the actual behavior of an existing piece of software"
bad = []


def check(name, cond, detail=""):
    print(("HOLDS " if cond else "MISS  ") + name + ((" | " + detail) if detail else ""))
    if not cond:
        bad.append(name)


def plain(path):
    t = Path(path).read_text(encoding="utf-8")
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))


# F1: quote verbatim at the stated location (lead sentence)
lesson = (BASE / "corpus/lessons/round-20.md").read_bytes().decode("utf-8").split("\n")
m = re.search("\u201c(.*?)\u201d", lesson[46])
check("F1 lesson:47 quote byte-equal to Q", bool(m) and m.group(1) == Q)
w = plain(SCR / "s072.html")
check("F1 Q occurs exactly once in rendered page text", w.count(Q) == 1, "count=%d" % w.count(Q))
i = w.find(Q)
check("F1 Q sits in the lead (alias precedes, Overview follows)",
      "(also known as Golden Master Testing" in w[max(0, i - 200):i] and "Overview" in w[i:i + 2000])
raw = (SCR / "s072.html").read_text(encoding="utf-8")
wt = json.loads((SCR / "s072-wikitext.json").read_text(encoding="utf-8"))["parse"]["wikitext"]["*"]
check("F1 raw-byte count 0 in HTML and wikitext; 'actual' is bold markup there",
      raw.count(Q) == 0 and wt.count(Q) == 0 and re.search(r"<b[^>]*>actual</b>", raw) is not None
      and "'''actual'''" in wt)
info = json.loads((SCR / "s072-info.json").read_text(encoding="utf-8"))
pg = list(info["query"]["pages"].values())[0]
print("INFO observed lastrevid=%s touched=%s" % (pg["lastrevid"], pg["touched"]))

# F2: word limit
check("F2 Q <= 25 words", len(Q.split()) <= 25, "words=%d" % len(Q.split()))

# F3 / F5: registry row, tier and status/used-by
S = (BASE / "corpus/SOURCES.md").read_text(encoding="utf-8").split("\n")
hdr = [c.strip() for c in S[4].strip().strip("|").split("|")]
row = [l for l in S if l.startswith("| S072 |")]
cs = [c.strip() for c in row[0].strip().strip("|").split("|")] if len(row) == 1 else []
rec = dict(zip(hdr, cs))
check("F3 S072 row unique and arity equals header", len(row) == 1 and len(cs) == len(hdr),
      "arity=%d header=%d" % (len(cs), len(hdr)))
check("F3 tier == C", rec.get("tier") == "C")
rows = [l for l in S if re.match(r"^\| S\d{3} \|", l)]
pairs = Counter()
rej = []
for l in rows:
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    pairs[(c[3], c[7])] += 1
    if c[7] == "rejected":
        rej.append((c[0], c[-1]))
print("INFO registry rows=%d tier/status=%s" % (len(rows), dict(pairs)))
check("F3 every tier-C row is rejected", all(s == "rejected" for (t, s) in pairs if t == "C"))
check("F5 status == rejected and lesson:47 says 'Reject C'",
      rec.get("status") == "rejected" and "Reject C" in lesson[46])
check("F5 used-by == '—' (no paths to check)", rec.get("used-by") == "—")
check("F5 every rejected row has used-by '—'", all(u == "—" for _, u in rej), str(rej))
hits = []
for d in [BASE / "corpus/knowledge", BASE / "corpus/lessons"]:
    for root, _, files in os.walk(d):
        for f in files:
            p = Path(root) / f
            try:
                lines = p.read_text(encoding="utf-8").split("\n")
            except Exception:
                continue
            for n, line in enumerate(lines, 1):
                if "S072" in line or re.search(r"[Ww]ikipedia|Characterization_test|Characterization test", line):
                    hits.append("%s:%d" % (p.relative_to(BASE), n))
check("F5 only citer under corpus/knowledge + corpus/lessons is lessons/round-20.md:47",
      hits == ["corpus/lessons/round-20.md:47"], str(hits))

# F4: teaching grounded; comparators for the rejection rationale
s67 = plain(SCR / "s067.html")
s66 = (SCR / "s066-README.md").read_text(encoding="utf-8")
sha66 = hashlib.sha256((SCR / "s066-README.md").read_bytes()).hexdigest()
check("F4 S066 pinned README sha256 equals SOURCES.md:72 raw sha",
      sha66 == "db6b2f6a1aa542dbb262dc655c6c40d3703d7c04b89b44adcd6c3e1d3e30de0b", sha66[:12])
q67 = "The purpose of characterization testing is to document your system\u2019s actual behavior, not check for the behavior you wish your system had."
check("F4 S067 quote (lesson:42) present in essay", q67 in s67)
q66 = "Either you will update the master because you expected the changes and they are good"
L66 = s66.split("\n")
check("F4 S066 quote at README line 75 (lesson:41)", len(L66) >= 75 and q66 in L66[74])
check("F4a lead definition grounded: Q once, with alias 'Golden Master Testing'",
      w.count(Q) == 1 and "also known as Golden Master Testing" in w)
print("INFO alias 'golden' occurrences in S067 essay: %d" % s67.lower().count("golden"))
body = {
    "coverage-limit ('every possible input and output')": "every possible input and output",
    "change-detector framing": "change detectors",
    "expected-or-desirable judgement": "expected and/or desirable",
    "no-specification fallback ('conservative path')": "conservative path",
}
for k, v in body.items():
    print("INFO body[%s] wikipedia=%d S067=%d S066=%d" % (k, w.count(v), s67.count(v), s66.count(v)))
cov = "every possible input and output"
contra = w.count(cov) > 0 and s67.count(cov) == 0 and s66.count(cov) == 0
print("F4b FINDING rationale 'adds nothing over S067 for the re-pin ritual' contradicted by body "
      "coverage-limit sentence absent from S067 and S066: %s" % contra)

print("SUMMARY failed HOLDS-checks: %s" % bad)
sys.exit(1 if bad else 0)
