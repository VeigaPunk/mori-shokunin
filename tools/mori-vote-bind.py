#!/usr/bin/env python3
"""Dual-shape seat-output vote binder (round 56, C2 — operability capability).

The round-55 C1 counter bound an agreeing vote only when the voter's captured
output carried the exact `RECHECK <h> <w>` line as a stripped *text* line; all
fifteen reporting voters emitted structured JSON yields whose `vote_lines`
arrays quote the lines, so the frozen counter read `voted=0` on bytes that
carried 68/78 double-voted rows with zero dissent (the same round's C2 counter,
binding by substring, accepted the identical shape).  This tool is the frozen
fix: one parser that accepts BOTH shapes, so a vote binds no matter how a seat
wraps its final output (operator run-10 binding note; planned round-56 item).

Frozen grammar (a vote is one of):
  <verb> <hash12> <word> [<rest>]
    verb  := RECHECK | ENTAIL
    hash12:= exactly 12 lowercase hex digits (the sha256 key prefix)
    word  := [A-Za-z][A-Za-z0-9_-]*   (holds|stale|entailed|overclaim for the
            tally's agreeing check; the binder itself records any word)
    rest  := free text (ignored by the tally; recorded for audit)

Two channels, chosen per output document, never mixed:
  * JSON channel — if the whole output parses as a JSON value, the vote surface
    is the document's string scalars, walked in document order.  A scalar
    binds iff its STRIPPED content matches the grammar anchored at the start.
    A scalar that merely CONTAINS a vote sentence ("the claim is RECHECK ..")
    does not bind (overclaim guard vs. a loose substring binding).  Fence
    markers inside a scalar make the stripped scalar not start with the verb,
    so a fenced scalar does not bind either.
  * text channel — otherwise, the output is read as lines; fenced blocks
    (lines whose lstrip starts with ``` or ~~~) are skipped, and an unfenced
    line binds iff its STRIPPED content matches the grammar.
Last write wins per (verb, hash) inside the chosen channel.  Which channel
fired is recorded per vote for audit.

Binding unit: the orchestrator-captured final output (the `output` field of a
seat's result record in a wave's *-results.json).  A seat's report file is NOT
required — "bind on files the seat writes" includes the captured output; a
report-less seat's votes still count when its captured output carries them
(the round-55 lost seat Mo55Rc14 carried no votes in either surface, which the
tally reports as single-vote rows, never as zeros).

Usage:
  mori-vote-bind.py extract [--verb RECHECK|ENTAIL] <file> ...
  mori-vote-bind.py tally --ledger PATH --results PATH --verb VERB
      [--voter NAME ...] [--min N] [--disposition-cols N]
  mori-vote-bind.py --selftest

tally output (one line):
  TALLY rows=N agree=N double=N single=N zero=N dissent=N voters=N bound_voters=N
exit 0 always on a completed tally (the caller's counter interprets the line);
exit 2 on usage/setup; selftest exit 0 pass=N fail=0, else exit 1.

Read-only: opens inputs read-only, writes nothing outside TMPDIR selftest
fixtures.  TMPDIR/hyaku scratch only — never /tmp-hardcoded (QUALITY 127).
"""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile

VOTE_RE = re.compile(r"^(RECHECK|ENTAIL)\s+([0-9a-f]{12})\s+([A-Za-z][A-Za-z0-9_-]*)(?:\s(.*))?$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def _walk_strings(node, acc):
    if isinstance(node, str):
        acc.append(node)
    elif isinstance(node, list):
        for x in node:
            _walk_strings(x, acc)
    elif isinstance(node, dict):
        for k in node:
            _walk_strings(node[k], acc)
    return acc


def extract_votes(output):
    """Return (votes, channel): votes = list of dicts {verb,hash,word,rest,seq}."""
    if not isinstance(output, str) or output == "":
        return [], "none"
    try:
        doc = json.loads(output)
    except (ValueError, TypeError):
        doc = None
    votes = []
    if doc is not None:
        for s in _walk_strings(doc, []):
            m = VOTE_RE.match(s.strip())
            if m:
                votes.append({"verb": m.group(1), "hash": m.group(2), "word": m.group(3),
                              "rest": m.group(4) or "", "seq": len(votes), "channel": "json"})
        return votes, "json"
    fence = False
    for line in output.replace("\\n", "\n").split("\n"):
        if FENCE_RE.match(line):
            fence = not fence
            continue
        if fence:
            continue
        m = VOTE_RE.match(line.strip())
        if m:
            votes.append({"verb": m.group(1), "hash": m.group(2), "word": m.group(3),
                          "rest": m.group(4) or "", "seq": len(votes), "channel": "text"})
    return votes, "text"


def final_votes(output):
    """Last-write-wins per (verb, hash) -> {(verb,hash): vote}."""
    votes, channel = extract_votes(output)
    last = {}
    for v in votes:
        last[(v["verb"], v["hash"])] = v
    return last, channel


def read_results(path):
    """name -> output from a wave results.json; malformed/missing -> {}."""
    try:
        with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
            doc = json.load(f)
    except (OSError, ValueError, TypeError):
        return {}
    out = {}
    results = doc.get("results") if isinstance(doc, dict) else None
    if isinstance(results, list):
        for r in results:
            if isinstance(r, dict) and isinstance(r.get("name"), str) and isinstance(r.get("output"), str):
                out[r["name"]] = r["output"]
    return out


def read_ledger(path, verb):
    """hash -> disposition word for the given verb's ledger rows.

    Ledger table rows start with `| `<hash>` |`; the disposition cell index is
    verb-specific: RECHECK -> cell 6 (hash,entry,pointer,v7.3 source,v7.3 lines,
    status,disposition); ENTAIL tables share the same trailing shape here.
    """
    disp = {}
    try:
        with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
            for line in f:
                m = re.match(r"^ {0,3}\|\s*`([0-9a-f]{12})`", line)
                if not m:
                    continue
                cells = [c.strip() for c in line.split("|")]
                cells = cells[1:-1] if line.rstrip().endswith("|") else cells[1:]
                word = None
                if verb == "RECHECK" and len(cells) >= 7:
                    word = cells[6].strip("` ")
                if word:
                    disp[m.group(1)] = word
    except OSError:
        pass
    return disp


def tally(ledger_path, results_path, verb, voters=None, min_votes=2):
    disp = read_ledger(ledger_path, verb)
    outputs = read_results(results_path)
    roster = voters if voters is not None else sorted(outputs)
    rows = {"agree": 0, "double": 0, "single": 0, "zero": 0, "dissent": 0}
    bound_voters = 0
    for h, want in disp.items():
        words = []
        nvote = 0
        for name in roster:
            out = outputs.get(name)
            if out is None:
                continue
            fv, _ = final_votes(out)
            v = fv.get((verb, h))
            if v is None:
                continue
            nvote += 1
            words.append((name, v["word"]))
        distinct = {w for _, w in words}
        if len(distinct) > 1:
            rows["dissent"] += 1
        nagree = sum(1 for _, w in words if w == want)
        if len(words) == 0:
            rows["zero"] += 1
        elif len(words) == 1:
            rows["single"] += 1
            if nagree == 1:
                rows["agree"] += 1
        else:
            rows["double"] += 1
            if nagree == len(words) and len(distinct) == 1:
                rows["agree"] += 1
    for name in roster:
        out = outputs.get(name)
        if out is None:
            continue
        fv, _ = final_votes(out)
        if any(k[0] == verb for k in fv):
            bound_voters += 1
    return {"rows": len(disp), **rows, "voters": len(roster), "bound_voters": bound_voters,
            "min": min_votes}


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

SELFTEST_CASES = []


def case(fn):
    SELFTEST_CASES.append(fn)
    return fn


def _j(**kw):
    return json.dumps(kw)


@case
def t_plain_binds():
    out = "preamble\nRECHECK a6e5226259c9 holds\nmore\nRECHECK 0124918d278a stale"
    fv, ch = final_votes(out)
    return ch == "text" and fv[("RECHECK", "a6e5226259c9")]["word"] == "holds" and \
        fv[("RECHECK", "0124918d278a")]["word"] == "stale"


@case
def t_json_array_binds():
    out = _j(findings="none", vote_lines=["RECHECK 7b2d297eec60 holds", "RECHECK 909839af93ac holds"])
    fv, ch = final_votes(out)
    return ch == "json" and fv[("RECHECK", "7b2d297eec60")]["word"] == "holds" and \
        fv[("RECHECK", "909839af93ac")]["channel"] == "json"


@case
def t_json_nested_binds():
    out = _j(a={"b": [{"c": "RECHECK 68afd0d6fa2f holds"}]})
    fv, ch = final_votes(out)
    return ch == "json" and fv[("RECHECK", "68afd0d6fa2f")]["word"] == "holds"


@case
def t_json_string_doc_binds():
    fv, ch = final_votes(json.dumps("RECHECK 6f9f1d32ac46 holds"))
    return ch == "json" and fv[("RECHECK", "6f9f1d32ac46")]["word"] == "holds"


@case
def t_fenced_text_ignored():
    out = "intro\n```\nRECHECK a6e5226259c9 holds\n```\n"
    fv, _ = final_votes(out)
    return ("RECHECK", "a6e5226259c9") not in fv


@case
def t_fenced_scalar_ignored():
    out = _j(note="```\nRECHECK a6e5226259c9 holds\n```")
    fv, ch = final_votes(out)
    return ch == "json" and ("RECHECK", "a6e5226259c9") not in fv


@case
def t_json_prose_substring_rejected():
    out = _j(findings="the claim is RECHECK a6e5226259c9 holds today, surely")
    fv, _ = final_votes(out)
    return ("RECHECK", "a6e5226259c9") not in fv


@case
def t_junk_rejected():
    for out in ("", "nothing here", _j(findings="none")):
        fv, _ = final_votes(out)
        if fv:
            return False
    return True


@case
def t_hash_len_drift_rejected():
    fv, _ = final_votes("RECHECK a6e5226259c90 holds")
    return ("RECHECK", "a6e5226259c9") not in fv and not fv


@case
def t_last_wins_text():
    out = "RECHECK a6e5226259c9 stale\nRECHECK a6e5226259c9 holds"
    fv, _ = final_votes(out)
    return fv[("RECHECK", "a6e5226259c9")]["word"] == "holds"


@case
def t_last_wins_json():
    out = _j(vote_lines=["RECHECK a6e5226259c9 stale", "RECHECK a6e5226259c9 holds"])
    fv, _ = final_votes(out)
    return fv[("RECHECK", "a6e5226259c9")]["word"] == "holds"


@case
def t_dissent_detected():
    outs = {"A": "RECHECK a6e5226259c9 holds", "B": "RECHECK a6e5226259c9 stale"}
    words = set()
    for o in outs.values():
        fv, _ = final_votes(o)
        v = fv.get(("RECHECK", "a6e5226259c9"))
        if v:
            words.add(v["word"])
    return words == {"holds", "stale"}


@case
def t_entailed_verb_parsed():
    out = _j(vote_lines=["ENTAIL 7b2d297eec60 entailed", "ENTAIL 909839af93ac overclaim — unit"])
    fv, _ = final_votes(out)
    return fv[("ENTAIL", "7b2d297eec60")]["word"] == "entailed" and \
        fv[("ENTAIL", "909839af93ac")]["word"] == "overclaim"


@case
def t_malformed_json_falls_back_to_text():
    # a truncated JSON doc: the vote still sits on its own line, so the text
    # channel binds it; the truncated scalars never parse as a JSON doc.
    out = '{"vote_lines": [\nRECHECK a6e5226259c9 holds\n], "broken": tru'
    fv, ch = final_votes(out)
    return ch == "text" and fv[("RECHECK", "a6e5226259c9")]["word"] == "holds"


@case
def t_tally_mini():
    """A 4-row synthetic ledger + results: 2 double-agree, 1 single, 1 zero."""
    tmp = tempfile.mkdtemp(prefix="mori-vote-bind-", dir=os.environ.get("TMPDIR") or None)
    ledger = os.path.join(tmp, "ledger.md")
    results = os.path.join(tmp, "results.json")
    hashes = ["aaaaaaaaaaaa", "bbbbbbbbbbbb", "cccccccccccc", "dddddddddddd"]
    with open(ledger, "w") as f:
        f.write("| hash | entry | pointer | source | lines | status | disposition |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for h in hashes:
            f.write("| `%s` | e | p | s | l | same | holds |\n" % h)
    res = {"results": [
        {"name": "V1", "output": json.dumps({"vote_lines": ["RECHECK %s holds" % hashes[0],
                                                           "RECHECK %s holds" % hashes[1]]})},
        {"name": "V2", "output": "RECHECK %s holds\nRECHECK %s holds" % (hashes[0], hashes[2])},
        {"name": "V3", "output": json.dumps({"findings": "none"})},
    ]}
    with open(results, "w") as f:
        json.dump(res, f)
    r = tally(ledger, results, "RECHECK", voters=["V1", "V2", "V3"], min_votes=2)
    # h0: V1+V2 double-agree; h1: V1 only; h2: V2 only; h3: none.
    ok = (r["rows"] == 4 and r["double"] == 1 and r["single"] == 2 and r["zero"] == 1
          and r["agree"] == 3 and r["dissent"] == 0 and r["bound_voters"] == 2)
    try:
        import shutil
        shutil.rmtree(tmp)
    except OSError:
        pass
    return ok


@case
def t_roster_and_name_filter():
    tmp = tempfile.mkdtemp(prefix="mori-vote-bind-", dir=os.environ.get("TMPDIR") or None)
    ledger = os.path.join(tmp, "ledger.md")
    results = os.path.join(tmp, "results.json")
    with open(ledger, "w") as f:
        f.write("| hash | entry | pointer | source | lines | status | disposition |\n|---|---|---|---|---|---|---|\n")
        f.write("| `aaaaaaaaaaaa` | e | p | s | l | same | holds |\n")
    res = {"results": [
        {"name": "RosterV", "output": "RECHECK aaaaaaaaaaaa holds"},
        {"name": "Stranger", "output": "RECHECK aaaaaaaaaaaa stale"},
        {"output": "RECHECK aaaaaaaaaaaa stale"},
    ]}
    with open(results, "w") as f:
        json.dump(res, f)
    r = tally(ledger, results, "RECHECK", voters=["RosterV"], min_votes=1)
    ok = r["agree"] == 1 and r["voters"] == 1 and r["dissent"] == 0
    try:
        import shutil
        shutil.rmtree(tmp)
    except OSError:
        pass
    return ok


def selftest():
    passed = failed = 0
    fails = []
    for fn in SELFTEST_CASES:
        try:
            ok = bool(fn())
        except Exception as e:  # noqa: BLE001 - a crash is a failure, not an escape
            ok = False
            fails.append("%s:EXC:%s" % (fn.__name__, e))
        if ok:
            passed += 1
        else:
            failed += 1
            fails.append(fn.__name__)
    line = "VOTE_BIND_SELFTEST pass=%d fail=%d" % (passed, failed)
    if fails:
        line += " failed=" + ",".join(fails)
    print(line)
    return 0 if failed == 0 else 1


def main(argv):
    ap = argparse.ArgumentParser(prog="mori-vote-bind.py")
    sub = ap.add_subparsers(dest="cmd")
    p_ex = sub.add_parser("extract")
    p_ex.add_argument("files", nargs="+")
    p_ex.add_argument("--verb", default=None)
    p_t = sub.add_parser("tally")
    p_t.add_argument("--ledger", required=True)
    p_t.add_argument("--results", required=True)
    p_t.add_argument("--verb", required=True)
    p_t.add_argument("--voter", action="append", default=None)
    p_t.add_argument("--min", type=int, default=2)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest or (a.cmd is None and "--selftest" in argv):
        return selftest()
    if a.cmd == "extract":
        for path in a.files:
            try:
                with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
                    out = f.read()
            except OSError as e:
                print("VOTE_BIND_SETUP: cannot read %s: %s" % (path, e), file=sys.stderr)
                return 2
            fv, channel = final_votes(out)
            for (verb, h), v in sorted(fv.items()):
                if a.verb and verb != a.verb:
                    continue
                print("VOTE %s %s %s %s %s" % (verb, h, v["word"], v["channel"], v["rest"]))
        return 0
    if a.cmd == "tally":
        r = tally(a.ledger, a.results, a.verb, voters=a.voter, min_votes=a.min)
        print("TALLY rows=%(rows)d agree=%(agree)d double=%(double)d single=%(single)d "
              "zero=%(zero)d dissent=%(dissent)d voters=%(voters)d bound_voters=%(bound_voters)d" % r)
        return 0
    print("VOTE_BIND_SETUP: usage", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
