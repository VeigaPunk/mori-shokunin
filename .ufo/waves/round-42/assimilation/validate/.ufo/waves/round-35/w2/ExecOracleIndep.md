measured 2026-10-23T09:15:26Z

# ExecOracleIndep — independent re-derivation of C1 at `cedb0ec4f3a4f672804deac388b7191258f01fcd`

Scope: independent oracle for P-C1 without the counter. Own 98-line script (no import, no copy of
`count-c1.py`); counter run only as the thing compared against. Lane writes: this file only. Scratch:
`/fast/scratch/hyaku/mori-r35/ExecOracleIndep/` (`indep-c1.py`, `mine-tip.txt`, `counter-tip.txt`,
`mine-base.txt`, `mut-m{1..5}-{mine,counter}.txt`, clone `clone-lane`). No installs, no pacman.

Inputs: lane `git show` at `cedb0ec`; fleet `git show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json`
(sha256 `0b414b8a…ae9952`). Frozen counter copied to scratch first; sha256
`27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167`, equal to the assignment value.

## Method (independent, contract arms)

Per register row in the **last** `## Capabilities` section: key membership in the admitted-capability set
(`rounds[i].capabilities_added[j]`, `admitted is True`, non-empty list: 12 entries, 18 keys), round-cell
equality with the MANIFEST closure round, evidence path present in `ls-tree -r` at the tip and at the
closure commit, present in `diff --name-only --no-renames prev..commit` for **both** readings of "previous
mori closure" (previous mori MANIFEST entry, and previous *admitted* closure), allowed prefix, capability-
string-named path equality, whole-path occurrence in the closure record (verification JSON, capability
strings, spot-check files, fleet report at `MANIFEST_REV`). Extras, duplicates and missing keys counted.

Commands: `timeout 300 python3 indep-c1.py cedb0ec4f3a4f672804deac388b7191258f01fcd` (mine, exit 0 always);
`timeout 300 python3 count-c1-frozen.py cedb0ec4f3a4f672804deac388b7191258f01fcd --repo <lane> --fleet /home/vgpnk/Projects/shokunin` (counter).

## Output

mine: `mine-summary heading='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 met=True`
counter: `label=P-C1 rev=cedb0ec4f3a4f672804deac388b7191258f01fcd manifest_rev=37b51a243302
register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met` (exit 0)
base `dd76eb79` both: `heading='## Capabilities (round 12 demonstrations)' rows=5 matched=0 missing=18
bad=0 extra=5`; counter adds `mismatches=23 C1=unmet`. All 12 unique closure commits are ancestors of the
tip (`git merge-base --is-ancestor` ×12, all exit 0).

## Agreement table (counter per-row line vs mine)

| key | counter | mine | agree |
|---|---|---|---|
| `rounds[313].capabilities_added[0]` | matched | ok | yes |
| `rounds[339].capabilities_added[0]` | matched | ok | yes |
| `rounds[345].capabilities_added[0]` | matched | ok | yes |
| `rounds[353].capabilities_added[0]` | matched | ok | yes |
| `rounds[386].capabilities_added[0]` | matched | ok | yes |
| `rounds[386].capabilities_added[1]` | matched | ok | yes |
| `rounds[386].capabilities_added[2]` | matched | ok | yes |
| `rounds[398].capabilities_added[0]` | matched | ok | yes |
| `rounds[427].capabilities_added[0]` | matched | ok | yes |
| `rounds[443].capabilities_added[0]` | matched | ok | yes |
| `rounds[443].capabilities_added[1]` | matched | ok | yes |
| `rounds[455].capabilities_added[0]` | matched | ok | yes |
| `rounds[455].capabilities_added[1]` | matched | ok | yes |
| `rounds[462].capabilities_added[0]` | matched | ok | yes |
| `rounds[476].capabilities_added[0]` | matched | ok | yes |
| `rounds[476].capabilities_added[1]` | matched | ok | yes |
| `rounds[495].capabilities_added[0]` | matched | ok | yes |
| `rounds[495].capabilities_added[1]` | matched | ok | yes |

18/18 label agreement, same order, base agrees (5 extra labels, 18 missing), mismatch counts agree.
Spot checks by hand: `git diff 1fc6bb0e 52435f2 -- tools/mori-blind-check.sh` non-empty; `git diff 20e2255
bf7cdc478` contains `corpus/SOURCES.md`; `20e2255` == `1f07f1d^`.

## Mutants (sandbox clone, branch per mutant, `git commit` in scratch only)

| id | mutation of `cedb0ec` | mine | counter | killed |
|---|---|---|---|---|
| M1 | r12 row round cell `12`→`13` | `bad round=13` | `bad round=13!=12` | yes |
| M2 | r19 evidence → `tools/no-such-tool.py` | `bad absent-at-tip` | `bad absent-at-rev` | yes |
| M3 | r24 evidence → `tools/mori-census.sh` | `bad not-changed-prev-entry,not-changed-prev-admitted,named,unnamed-in-record` | `bad weak-path` | yes |
| M4 | r19 evidence → `tools/mori-pressure.py` (absent at `2061780`) | `bad absent-at-commit,…` | `bad weak-path` | yes |
| M5 | extra row keyed `rounds[372].capabilities_added[0]` (r17, rejected) | `extra:not-in-oracle` | `extra` | yes |

## Risks / residuals

- Common-mode by construction: both read the same MANIFEST fields and the same `git diff`/`ls-tree`
  plumbing; a schema misreading would not self-report. Mitigated by reading entries 313/339/495 directly.
- "Previous mori closure commit" is ambiguous; the counter uses the previous mori MANIFEST entry
  (rejected rounds included). Measured both readings on all 18 rows: no row flips, so the result is
  invariant here.
- My script always exits 0; agreement is on per-row labels and the `met` flag, not exit codes.
- Neither oracle judges the prose truth of the "what it can now do" cell or the choice among several
  strong artifacts; the contract states this residual for non-author reviewers.
- M5 formatting only: the counter's extra line echoes the raw cell with backticks, mine strips them.

## Script (as run, 98 lines)

```python
#!/usr/bin/env python3
"""ExecOracleIndep r35w2: independent C1 re-derivation (own code; no count-c1.py import or copy).
Per row: key membership, round, evidence at tip and at closure commit, changed vs prev-mori-entry
and prev-admitted-closure bases, allowed prefix, named in the closure record. Read-only git."""
import json, re, subprocess, sys

REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
MAN, BASE0 = "37b51a243302e8009c7067431e8a47f9a722fd14", "20e2255"
ALLOWED = ("tools/", "corpus/knowledge/", "corpus/evidence/", "corpus/SOURCES.md")
ARGV = sys.argv[1:]
def opt(n, d): return ARGV[ARGV.index(n) + 1] if n in ARGV else d
def git(repo, *a):
    p = subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True)
    return p.returncode, p.stdout
def val(repo, *a):
    rc, out = git(repo, *a)
    if rc: raise SystemExit("git failed: %s" % " ".join(a))
    return out
def files(rev): return set(val(REPO, "ls-tree", "-r", "--name-only", rev).splitlines())
def delta(a, b): return set(val(REPO, "diff", "--name-only", "--no-renames", a, b).splitlines())
def body(rev, path):
    rc, out = git(REPO, "show", "%s:%s" % (rev, path))
    return out if rc == 0 else None
def table(text):
    lines = text.splitlines()
    cut = [i for i, l in enumerate(lines) if l.startswith("## Capabilities")]
    if not cut: return None, []
    s = cut[-1]
    e = next((i for i in range(s + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    rows = []
    for l in lines[s + 1:e]:
        c = [x.strip() for x in l.strip().strip("|").split("|")] if l.strip().startswith("|") else None
        if c and not all(re.fullmatch(r":?-{3,}:?", x) for x in c if x): rows.append(c)
    if rows and rows[0][0].strip("` ").lower() in ("key", "capability"): rows = rows[1:]
    return lines[s], rows
def main():
    tip = val(REPO, "rev-parse", "--verify", ARGV[0] + "^{commit}").strip()
    man = json.loads(val(FLEET, "show", MAN + ":MANIFEST.json"))
    oracle, last_any, last_adm = {}, BASE0, BASE0
    for i, r in enumerate(man["rounds"]):
        if r.get("lane") != "mori": continue
        c = val(REPO, "rev-parse", "--verify", r["commit"].split("@", 1)[1] + "^{commit}").strip()
        caps = r.get("capabilities_added") or []
        if r.get("admitted") and caps:
            rec = [json.dumps(r.get("verification") or {}, ensure_ascii=False)] + caps
            for p, h in re.findall(r"mori-shokunin/([A-Za-z0-9_./-]+)@([0-9a-f]{7,40})", rec[0]):
                b = body(h, p)
                rec += [b] if b is not None else []
            rc, rep = git(FLEET, "show", "%s:%s" % (MAN, r.get("report") or ""))
            rec += [rep] if rc == 0 else []
            for j, cap in enumerate(caps):
                oracle["rounds[%d].capabilities_added[%d]" % (i, j)] = {
                    "round": r["round"], "at": files(c), "a": delta(last_any, c), "b": delta(last_adm, c),
                    "text": "\n".join(rec),
                    "named": set(re.findall(r"((?:tools|corpus/knowledge)/[A-Za-z0-9_./-]*[A-Za-z0-9_])", cap))}
        last_any = c
        last_adm = c if r.get("admitted") else last_adm
    head, rows = table(body(tip, "SCORECARD.md") or "")
    at_tip, seen, res = files(tip), set(), []
    for c in rows:
        key = c[0].strip("` ") if c else ""
        if key not in oracle:
            res.append((key, "extra:" + ("duplicate" if key in seen else "not-in-oracle"), []))
            continue
        seen.add(key)
        o, why = oracle[key], []
        if len(c) != 5: why.append("cells=%d" % len(c))
        else:
            if c[4].strip("` ") != str(o["round"]): why.append("round=%s" % c[4].strip("` "))
            toks = re.findall(r"`([^`]+)`", c[3])
            if not 1 <= len(toks) <= 2: why.append("evidence-paths=%d" % len(toks))
            for t in toks:
                m = re.fullmatch(r"([A-Za-z0-9_.][A-Za-z0-9_./-]*)(?::(\d+)(?:-(\d+))?)?", t)
                if not m: why.append("not-a-path:%s" % t); continue
                p, lo, hi = m.groups()
                if p not in at_tip: why.append("absent-at-tip:%s" % p); continue
                if lo and not 1 <= int(lo) <= int(hi or lo) <= len((body(tip, p) or "").splitlines()):
                    why.append("range:%s" % t); continue
                arms = (("absent-at-commit", p in o["at"]), ("not-changed-prev-entry", p in o["a"]),
                        ("not-changed-prev-admitted", p in o["b"]), ("prefix", p.startswith(ALLOWED)),
                        ("named", not o["named"] or p in o["named"]),
                        ("unnamed-in-record", re.search(r"(?<![A-Za-z0-9_./-])" + re.escape(p)
                                                        + r"(?![A-Za-z0-9_./-])", o["text"]) is not None))
                why += ["%s:%s" % (n, p) for n, hit in arms if not hit]
        res.append((key, "ok" if not why else "bad", why))
    missing = sorted(k for k in oracle if k not in seen)
    for k, s, w in res: print("mine %s %s %s" % (k, s, ",".join(w)))
    for k in missing: print("mine %s missing" % k)
    bad = sum(1 for _, s, _ in res if s == "bad")
    extra = sum(1 for _, s, _ in res if s.startswith("extra"))
    matched = sum(1 for _, s, _ in res if s == "ok")
    print("mine-summary heading=%r oracle=%d rows=%d matched=%d missing=%d bad=%d extra=%d met=%s" %
          (head, len(oracle), len(rows), matched, len(missing), bad, extra,
           matched == len(oracle) and not missing and not bad and not extra))
if __name__ == "__main__":
    REPO, FLEET = opt("--repo", REPO), opt("--fleet", FLEET)
    main()
```

## Verdicts

VERDICT: no defect found — independent oracle reproduces C1=met at `cedb0ec4f3a4f672804deac388b7191258f01fcd`;
all four assigned arms (key membership, round equality, path existence at tip and at closure commit,
changed vs previous closure) pass for 18/18 rows and agree with the counter line for line.
VERDICT: agree — audit of `count-c1.py` against the independent oracle at tip, at base `dd76eb79`, and on
five sandbox mutants.
VERDICT: holds — frozen claim C1: the register in SCORECARD.md's last `## Capabilities` section binds each
of the 18 capabilities MANIFEST@37b51a24 records under admitted mori closures.
VERDICT: killed — mutants M1 (wrong round), M2 (dangling path), M3 (stale pointer), M4 (absent at closure
commit), M5 (rejected-round key), each rejected by both oracles.
