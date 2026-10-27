#!/usr/bin/env python3
"""Round 54 controls (L1 MoriR54): cheap trees that skip the claimed work, scored by the frozen counters before
any wave seat runs. Each control is a commit in a throwaway `git clone --shared` of the lane under
$HYAKU_SCRATCH/mori-r54/l1/controls/<name> (identity set per command inside the clone only; the clone's toplevel
is checked before the first commit). The base of every control is the entering tip plus the frozen overlay
(counters, controls, v7.3 copies) from the lane working tree. Receipts land in ../evidence/control-*.txt.

Usage: controls.py            (all controls)
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WAVE = os.path.dirname(HERE)
LANE = os.path.dirname(os.path.dirname(os.path.dirname(WAVE)))
ENTERING = "39dcf4d7e410d362781a47e8365ca23b5c807598"
SCRATCH = os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "mori-r54", "l1", "controls")
OVERLAY = [".ufo/waves/round-54/count-c1.py", ".ufo/waves/round-54/count-c2.py",
           ".ufo/waves/round-54/controls/c1data.py", ".ufo/waves/round-54/controls/c2data.py",
           ".ufo/waves/round-54/controls/controls.py"]
OVERLAY_DIRS = ["corpus/evidence/sources-r54"]
EVID = os.path.join(WAVE, "evidence")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def git(d, *args, check=True):
    return subprocess.run(["git", "-C", d] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=check, timeout=300).stdout.decode().strip()


def clone(name):
    d = os.path.join(SCRATCH, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(SCRATCH, exist_ok=True)
    subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, d], check=True, timeout=300)
    if os.path.realpath(git(d, "rev-parse", "--show-toplevel")) != os.path.realpath(d):
        raise SystemExit("clone toplevel mismatch for %s" % d)
    git(d, "checkout", "-q", "--detach", ENTERING)
    for p in OVERLAY:
        os.makedirs(os.path.dirname(os.path.join(d, p)), exist_ok=True)
        shutil.copy2(os.path.join(LANE, p), os.path.join(d, p))
    for p in OVERLAY_DIRS:
        shutil.rmtree(os.path.join(d, p), ignore_errors=True)
        shutil.copytree(os.path.join(LANE, p), os.path.join(d, p))
    commit(d, "control base: entering tip + frozen overlay")
    return d


def commit(d, msg):
    if os.path.realpath(git(d, "rev-parse", "--show-toplevel")) != os.path.realpath(d):
        raise SystemExit("refusing to commit outside the clone: %s" % d)
    git(d, "add", "-A")
    git(d, "-c", "user.name=control", "-c", "user.email=control@scratch.invalid", "commit", "-q",
        "--allow-empty", "-m", msg)
    return git(d, "rev-parse", "HEAD")


def score(counter, d, rev, receipt, label, note):
    cmd = ["python3", "-B", os.path.join(LANE, ".ufo/waves/round-54", counter), "--repo", d, rev]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
    out = p.stdout.decode().strip()
    with open(os.path.join(EVID, receipt), "w") as f:
        f.write("control: %s\nnote: %s\ncommand: %s\n%s\nexit=%d\n" % (label, note, " ".join(cmd), out, p.returncode))
    print("%-28s exit=%d %s" % (label, p.returncode, out[:200]))
    return p.returncode, out


def results(names):
    return json.dumps({"lane": "mori", "round": 54, "wave": "w1", "note": "control fixture, not a settlement",
                       "results": [{"name": n, "agent": "reviewer", "output": "control"} for n in names]})


def write(d, rel, text):
    path = os.path.join(d, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def c1_votes(d, c1, names=("Mo54Rc01", "Mo54Rc07"), settle=True):
    _, rows = c1.parse_table(open(os.path.join(d, c1.LEDGER)).read(), c1.HEADER)
    for v in names:
        write(d, c1.VOTE_DIR + v + ".md", "".join("RECHECK %s %s\n" % (r[0], r[6]) for r in rows))
    if settle:
        write(d, c1.RESULTS, results(names))


def run_c1():
    c1 = load("c1", os.path.join(WAVE, "count-c1.py"))
    c1data = load("c1data", os.path.join(HERE, "c1data.py"))
    d = clone("c1-do-nothing")
    score("count-c1.py", d, ENTERING, "control-c1-do-nothing.txt", "c1 do-nothing",
          "the entering tip itself (no ledger, no v7.3 copies)")
    base = git(d, "rev-parse", "HEAD")
    score("count-c1.py", d, base, "control-c1-copies-only.txt", "c1 copies-only",
          "entering tip + the frozen copies and counters, no ledger, rows or votes (the freeze state)")
    d = clone("c1-witness")
    c1data.apply(d)
    c1_votes(d, c1)
    rev = commit(d, "c1 witness")
    score("count-c1.py", d, rev, "control-c1-witness.txt", "c1 witness",
          "feasibility only: c1data.py ledger and rows plus two synthetic voters listed in a fixture results file")
    d = clone("c1-no-votes")
    c1data.apply(d)
    rev = commit(d, "c1 no votes")
    score("count-c1.py", d, rev, "control-c1-no-votes.txt", "c1 no-votes",
          "ledger and rows, no voter; the data commit before the wave must read this")
    d = clone("c1-unsettled")
    c1data.apply(d)
    c1_votes(d, c1, settle=False)
    rev = commit(d, "c1 unsettled voters")
    score("count-c1.py", d, rev, "control-c1-unsettled.txt", "c1 unsettled-voters",
          "witness with the voter files but no orchestrator results file (hand-written votes)")
    d = clone("c1-no-line")
    c1data.apply(d)
    led = os.path.join(d, c1.LEDGER)
    text = open(led).read().split("\n")
    out = []
    for line in text:
        cells = c1.split_cells(line) if line.startswith("|") else None
        if cells and len(cells) == 7 and cells[0] not in ("h",) and not cells[0].startswith("---"):
            cells[4] = "-"
            line = "| " + " | ".join(cells) + " |"
        out.append(line)
    open(led, "w").write("\n".join(out))
    c1_votes(d, c1)
    rev = commit(d, "c1 no lines")
    score("count-c1.py", d, rev, "control-c1-no-line.txt", "c1 no-line",
          "the r53-style all-held relabel: every row held with its v7.2 quote and votes, but no located v7.3 line")
    d = clone("c1-v72-copies")
    v72 = {"mm/memcontrol.c": "corpus/evidence/sources-r50/memcontrol.c.v7.2",
           "mm/oom_kill.c": "corpus/evidence/sources-r50/oom_kill.c.v7.2",
           "lib/percpu_counter.c": "corpus/evidence/sources-r53/percpu_counter.c.v7.2",
           "include/linux/percpu_counter.h": "corpus/evidence/sources-r53/percpu_counter.h.v7.2",
           "include/uapi/asm-generic/errno.h": "corpus/evidence/sources-r48/errno.h",
           "docs:admin-guide/cgroup-v2.html": "corpus/evidence/sources-r50/cgroup-v2.7.2.html",
           "mm/mm_init.c": "corpus/evidence/sources-r53/mm_init.c.v7.2"}
    for key, src in v72.items():
        shutil.copy2(os.path.join(d, src), os.path.join(d, c1.V73[key][0]))
    c1data.apply(d)
    c1_votes(d, c1)
    rev = commit(d, "c1 v7.2 bytes as v7.3")
    score("count-c1.py", d, rev, "control-c1-v72-copies.txt", "c1 v72-copies",
          "the committed v7.2 bytes presented as the v7.3 copies (errno.h is byte-identical across the tags), "
          "ledger, rows and votes derived from them")


def c2_entry(c2, claims, quotes):
    sids = {}
    for sid, url, *_ in load("c2data", os.path.join(HERE, "c2data.py")).NEW_ROWS:
        sids[url] = sid
    sids[c2.CGIT + "Documentation/admin-guide/sysctl/vm.rst?h=v7.3"] = "S507"
    sids[c2.CGIT + "Documentation/filesystems/proc.rst?h=v7.3"] = "S502"
    rows = ["| claim | source | quote |", "|---|---|---|"]
    for c, (u, q) in zip(claims, quotes):
        rows.append("| %s | %s | `%s` |" % (c, sids[u], q.replace("|", "\\|")))
    return "\n".join(["# Memory failure kills (control)", "",
                      "source: " + " ".join(sorted(set(sids[u] for u, _q in quotes))),
                      "verified-at: 2026-10-27", "recheck: on-release — count-c2.py", "", "## Claims", ""]
                     + rows + [""])


def c2_quotes(c2, d):
    texts = {u: c2.normalise_text(open(os.path.join(d, p)).read()) for u, (p, _dg, _k) in c2.COPIES.items()}

    def q(u, needle, n):
        t = texts[u]
        i = t.index(needle)
        return " ".join(t[i:].split(" ")[:n])
    mf, hw, node, tr, vm, proc = list(c2.COPIES)
    return [
        (mf, q(mf, 'pr_err("%#lx: Sending SIGBUS to %s:%d due to hardware memory corruption', 9)),
        (mf, q(mf, 'pr_err("%#lx: forcibly killing %s:%d because of failure', 9)),
        (mf, q(mf, 'pr_err("%#lx: recovery action for %s: %s', 7)),
        (mf, q(mf, '#define pr_fmt(fmt) "Memory failure: " fmt', 6)),
        (hw, q(hw, "Send SIGBUS to the application as soon as the error is detected", 12)),
        (hw, q(hw, "Send SIGBUS when the application runs into the corrupted page.", 10)),
        (node, q(node, "The total number of raw poisoned pages", 10)),
        (node, q(node, "Of the raw poisoned pages on a NUMA node, how many pages are recovered", 14)),
        (tr, q(tr, 'TP_printk("pfn %#lx: recovery action for %s: %s",', 7)),
        (tr, q(tr, "TRACE_EVENT(memory_failure_event, TP_PROTO(unsigned long pfn,", 6)),
        (vm, q(vm, "0: Only unmap the corrupted page from all processes and only kill a process", 14)),
        (vm, q(vm, "The kill is done using a catchable SIGBUS with BUS_MCEERR_AO", 12)),
        (vm, q(vm, "0: Always panic on a memory failure.", 7)),
        (proc, q(proc, "The amount of RAM/memory in KB, the kernel identifies as corrupted.", 12)),
    ]


def c2_votes(d, c2, entry_text, names=("Mo54En01", "Mo54En07")):
    _h, rows = c2.parse_claims(entry_text)
    for v in names:
        write(d, c2.ENTAIL_DIR + v + ".md", "".join("ENTAIL %s entailed\n" % c2.claim_hash(r[0]) for r in rows))
    write(d, c2.RESULTS, results(names))


def run_c2():
    c2 = load("c2", os.path.join(WAVE, "count-c2.py"))
    c2data = load("c2data", os.path.join(HERE, "c2data.py"))
    d = clone("c2-do-nothing")
    score("count-c2.py", d, ENTERING, "control-c2-do-nothing.txt", "c2 do-nothing",
          "the entering tip itself (no entry, no copies)")
    base = git(d, "rev-parse", "HEAD")
    score("count-c2.py", d, base, "control-c2-copies-only.txt", "c2 copies-only",
          "entering tip + frozen copies and counters, no entry or rows (the freeze state)")
    synth = ["observation number %d explains how the kernel reports poisoned memory kills" % i for i in range(14)]
    for name, note, mk in [
        ("witness", "feasibility only: synthetic claim text over real located quotes, rows from c2data.py, two "
                    "synthetic voters listed in a fixture results file", "witness"),
        ("quote-echo", "every claim cell is its quote plus one word (no reading beyond the bytes), rows and votes "
                       "present", "echo"),
        ("unlocated", "claims and votes present, every quote paraphrased (words reordered) so none is located",
         "unlocated"),
        ("no-votes", "entry and rows, no voter; the data commit before the wave must read this", "novotes"),
        ("two-sources", "fourteen located rows drawn from mm/memory-failure.c and vm.rst only, votes present",
         "two"),
    ]:
        d = clone("c2-" + name)
        c2data.apply(d)
        qs = c2_quotes(c2, d)
        claims = list(synth)
        if mk == "echo":
            claims = [q + " here" for _u, q in qs]
        if mk == "unlocated":
            qs = [(u, " ".join(reversed(q.split(" ")))) for u, q in qs]
        if mk == "two":
            mf, vm = list(c2.COPIES)[0], list(c2.COPIES)[4]
            texts = {u: c2.normalise_text(open(os.path.join(d, c2.COPIES[u][0])).read()) for u in (mf, vm)}
            words = {u: texts[u].split(" ") for u in (mf, vm)}
            qs = [(mf, " ".join(words[mf][4000 + 40 * i:4000 + 40 * i + 8])) for i in range(7)] + \
                 [(vm, " ".join(words[vm][2000 + 40 * i:2000 + 40 * i + 8])) for i in range(7)]
        text = c2_entry(c2, claims, qs)
        write(d, c2.ENTRY, text)
        if mk != "novotes":
            c2_votes(d, c2, text)
        rev = commit(d, "c2 " + name)
        score("count-c2.py", d, rev, "control-c2-%s.txt" % name, "c2 " + name, note)


if __name__ == "__main__":
    os.makedirs(EVID, exist_ok=True)
    try:
        run_c1()
        run_c2()
    finally:
        shutil.rmtree(SCRATCH, ignore_errors=True)
