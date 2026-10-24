#!/usr/bin/env python3
# S072 re-open checks, round 2. Lane edits moved the lesson Gate row from :47 to :51, so rows are located by content.
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


# lesson: locate Gate row by content
lesson_text = (BASE / "corpus/lessons/round-20.md").read_bytes().decode("utf-8")
L = lesson_text.split("\n")
print("INFO lesson sha256=%s lines=%d" % (hashlib.sha256(lesson_text.encode("utf-8")).hexdigest(), len(L)))
gate = [(k, l) for k, l in enumerate(L, 1) if l.startswith("| S072 |")]
check("F1 exactly one Gate row for S072 in lesson", len(gate) == 1, "lines=%s" % [k for k, _ in gate])
gl = gate[0][1]
mq = re.search("\u201c(.*?)\u201d", gl)
check("F1 Gate-row quote byte-equal to Q", bool(mq) and mq.group(1) == Q)
check("F5 Gate-row decision says 'Reject C.'", "Reject C." in gl)
print("INFO lines citing S072 in lesson:", [k for k, l in enumerate(L, 1) if "S072" in l])

# F1 / F2: rendered Wikipedia lead, raw HTML, wikitext, word count
w = plain(SCR / "s072.html")
check("F1 Q occurs exactly once in rendered page text", w.count(Q) == 1, "count=%d" % w.count(Q))
i = w.find(Q)
check("F1 Q sits in the lead (alias precedes, Overview follows)",
      "(also known as Golden Master Testing" in w[max(0, i - 200):i] and "Overview" in w[i:i + 2000])
raw = (SCR / "s072.html").read_text(encoding="utf-8")
wt = json.loads((SCR / "s072-wikitext.json").read_text(encoding="utf-8"))["parse"]["wikitext"]["*"]
check("F1 raw-byte count 0 in HTML and wikitext (bold 'actual' markup)",
      raw.count(Q) == 0 and wt.count(Q) == 0 and re.search(r"<b[^>]*>actual</b>", raw) is not None
      and "'''actual'''" in wt)
info = json.loads((SCR / "s072-info.json").read_text(encoding="utf-8"))
pg = list(info["query"]["pages"].values())[0]
print("INFO Wikipedia observed lastrevid=%s touched=%s" % (pg["lastrevid"], pg["touched"]))
check("F2 Q <= 25 words", len(Q.split()) <= 25, "words=%d" % len(Q.split()))

# F3 / F5: registry
S_text = (BASE / "corpus/SOURCES.md").read_text(encoding="utf-8")
S = S_text.split("\n")
print("INFO SOURCES sha256=%s lines=%d" % (hashlib.sha256(S_text.encode("utf-8")).hexdigest(), len(S)))
hdr = [c.strip() for c in S[4].strip().strip("|").split("|")]
parsed, arity_bad = {}, []
for l in S:
    if re.match(r"^\| S\d{3} \|", l):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) != len(hdr):
            arity_bad.append(c[0])
        parsed[c[0]] = dict(zip(hdr, c))
print("INFO registry rows=%d arity-mismatch=%s" % (len(parsed), arity_bad))
rec = parsed.get("S072", {})
check("F3 S072 row present, arity ok, tier == C",
      "S072" in parsed and "S072" not in arity_bad and rec.get("tier") == "C")
pairs = Counter((v.get("tier"), v.get("status")) for v in parsed.values())
print("INFO tier/status pairs=%s" % dict(pairs))
check("F3 every tier-C row is rejected", all(s == "rejected" for (t, s) in pairs if t == "C"))
check("F5 S072 status == rejected", rec.get("status") == "rejected")
check("F5 S072 used-by == '—' (registry convention: no paths)", rec.get("used-by") == "—")
rej = [(k, v.get("used-by")) for k, v in sorted(parsed.items()) if v.get("status") == "rejected"]
check("F5 all rejected rows carry used-by '—'", all(u == "—" for _, u in rej), str(rej))

# lesson-stated rule (round-20.md:55): "CORPUS.md: lessons citing a row are listed"
cite_rows = []
for k, l in enumerate(L, 1):
    m1 = re.match(r"^\| (S\d{3}) \|", l) or re.match(r"^- \*\*(S\d{3})", l)
    if m1:
        cite_rows.append((k, m1.group(1)))
gaps = []
print("INFO round-20.md Gate/spot-check rows vs used-by:")
for k, sid in cite_rows:
    v = parsed.get(sid, {})
    ub = v.get("used-by", "<missing>")
    ok = "corpus/lessons/round-20.md" in ub
    if not ok:
        gaps.append(sid)
    print("   line %d %s status=%s used-by=%s lesson_rule_met=%s" % (k, sid, v.get("status"), ub, ok))
check("F5 lesson-stated rule met for S072 (cited at round-20.md:51 and :73)", "S072" not in gaps)
print("INFO rule gaps (cited by round-20.md, used-by lacks it): %s" % sorted(set(gaps)))

# reverse citations under corpus/knowledge and corpus/lessons
hits = []
for d in [BASE / "corpus/knowledge", BASE / "corpus/lessons"]:
    for root, _, files in os.walk(d):
        for f in sorted(files):
            p = Path(root) / f
            try:
                lines = p.read_text(encoding="utf-8").split("\n")
            except Exception:
                continue
            for n, line in enumerate(lines, 1):
                if "S072" in line or re.search(r"[Ww]ikipedia|Characterization_test|Characterization test", line):
                    hits.append("%s:%d" % (p.relative_to(BASE), n))
print("INFO citers under corpus/knowledge + corpus/lessons: %s" % hits)
check("F5 every citer is lessons/round-20.md (no knowledge note cites S072)",
      len(hits) > 0 and all(h.startswith("corpus/lessons/round-20.md:") for h in hits), str(hits))

# F4: teaching grounded; comparators for the rejection rationale
s67 = plain(SCR / "s067.html")
s66 = (SCR / "s066-README.md").read_text(encoding="utf-8")
check("F4 S066 pinned README sha256 == SOURCES raw sha (db6b2f6a...de0b)",
      hashlib.sha256((SCR / "s066-README.md").read_bytes()).hexdigest()
      == "db6b2f6a1aa542dbb262dc655c6c40d3703d7c04b89b44adcd6c3e1d3e30de0b")
q67 = "The purpose of characterization testing is to document your system\u2019s actual behavior, not check for the behavior you wish your system had."
check("F4 S067 quote (lesson S067 Gate row) present in essay", q67 in s67)
q66 = "Either you will update the master because you expected the changes and they are good"
L66 = s66.split("\n")
check("F4 S066 quote at README line 75", len(L66) >= 75 and q66 in L66[74])
check("F4a lead definition grounded (Q once; alias 'Golden Master Testing' in lead)",
      w.count(Q) == 1 and "also known as Golden Master Testing" in w)
print("INFO 'golden' occurrences in S067 essay: %d" % s67.lower().count("golden"))
body = {
    "coverage-limit ('every possible input and output')": "every possible input and output",
    "change-detector framing": "change detectors",
    "expected-or-desirable judgement": "expected and/or desirable",
    "no-specification fallback ('conservative path')": "conservative path",
}
for k, v in body.items():
    print("INFO body[%s] wikipedia=%d S067=%d S066=%d" % (k, w.count(v), s67.count(v), s66.count(v)))
cov = "every possible input and output"
print("F4b FINDING registry rationale 'adds nothing over S067 for the re-pin ritual' is contradicted "
      "(coverage-limit present only in Wikipedia body): %s"
      % (w.count(cov) > 0 and s67.count(cov) == 0 and s66.count(cov) == 0))

print("SUMMARY failed checks: %s" % bad)
sys.exit(1 if bad else 0)
