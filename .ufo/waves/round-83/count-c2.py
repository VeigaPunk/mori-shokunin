#!/usr/bin/env python3
"""mori round-83 C2 counter (calibration): the drift classification is snapshot-bound.

Frozen predicate P-C2 (`.ufo/waves/round-83/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-83/count-c2.py R` prints
  `C2=met snapshot=bound asof=1 tokens=64 agreed=64 residual=0 live=derived` and exits 0, where
  `corpus/evidence/drift-classification-r82.txt` at R carries exactly one `# Snapshot:` line
  naming the frozen raw snapshot, one `# Snapshot-sha256:` line equal to the sha256 of that
  snapshot's bytes at R, and one `# As-of:` line equal to the snapshot's first `# run-start:`
  stamp normalized to UTC whole seconds; the snapshot's last `MORI_DRIFT:` token list is the
  population, every token has one `DRIFT_CLASS` line whose class equals the class derived from
  the baseline bytes at R, no extra token, no malformed or duplicate class line; the `##
  Retired` row `drift-pin-r10` names the baseline, the classification path and the snapshot
  path, and the `freshness` Axes cell keeps `r10 pin retired` plus the classification path and
  no red literal; and one live re-derivation runs at R (census at R against baseline at R),
  exiting 1 with a non-empty token list.

`live=derived` means the live run happened and read red; agreement between the live reading and
the snapshot is reported as `live_tokens=`/`live_agree=` readings, not required — the census is a
live observation, the classification is bound to the snapshot.

Round 84 (P-C3, `.ufo/waves/round-84/contract.md`): the live run's token line is additionally
classified per token against the snapshot's — one `LIVE_DELTA <token> <class>` line per union
token that is not agreed (classes `absent-live`, `added-live`,
`class-changed:<snapshot>-><live>`; `agreed` prints nothing), with the tail extended by
`delta=classified classified= union= absent_live= added_live= class_changed= deltas=`. `met`
additionally requires every union token classified exactly once and `agreed == live_agree`,
and never requires a particular live token count — the live census stays an observation.

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] [--fleet-root DIR] | --selftest
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`; files only under --scratch.
"""
import argparse
import datetime
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASELINE = "corpus/evidence/baseline-r10-20261015T2231Z.json"
CLASSES = "corpus/evidence/drift-classification-r82.txt"
CENSUS = "tools/mori-census.sh"
CARDS = "SCORECARD.md"
CLASS_WORDS = ("added-since-r10", "value-changed", "unexplainable")
CLASS_LINE = re.compile(r"^DRIFT_CLASS\s+(\S+)\s+(\S+)\s*$")
DRIFT = re.compile(r"^MORI_DRIFT:\s*(.*)$")
KEY = re.compile(r"(?:^|\s)([A-Za-z0-9_]+)=")
KEYSHAPE = re.compile(r"^[A-Za-z0-9_]+$")
FROZEN_SNAPSHOT = ".ufo/waves/round-82/evidence/drift-r82-live.txt"
SNAP_LINE = re.compile(r"^#\s*Snapshot:\s*(\S+)\s*$")
SNAP_SHA = re.compile(r"^#\s*Snapshot-sha256:\s*([0-9a-f]{64})\s*$")
ASOF = re.compile(r"^#\s*As-of:\s*(\S+)\s*$")
RUNSTART = re.compile(r"^#\s*run-start:\s*(\S+)")


def run(cmd, cwd=None, env=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def baseline_names(text):
    surfaces, findings = set(), set()
    for line in text.splitlines():
        if line.startswith("SURFACE "):
            surfaces.add(line[len("SURFACE "):].split(":", 1)[0])
        elif line.startswith("FINDING "):
            findings.add(line[len("FINDING "):].split(" severity=", 1)[0])
    return surfaces, findings, set(KEY.findall(text))


def derive(token, names):
    surfaces, findings, keys = names
    body = token.lstrip("+-")
    if body.startswith("SURFACE:"):
        return "value-changed" if body[len("SURFACE:"):] in surfaces else "added-since-r10"
    if body.startswith("FINDING:"):
        return "value-changed" if body[len("FINDING:"):] in findings else "added-since-r10"
    if body in ("VERDICT", "HEADER", "BLANK"):
        return "value-changed"
    if not KEYSHAPE.match(body):
        return "value-changed"          # frozen table: "anything else" is value-changed
    return "value-changed" if body in keys else "added-since-r10"


def live_delta(snapshot_tokens, live_tokens, names, stated):
    """Per-token delta between the snapshot token line and the live run's (pure).

    Ordered (token, class) list over the union of the two token lines — snapshot
    order first, then live-only tokens in live order, every token exactly once.
    The live class is derive(token, names); the snapshot class is the stated one
    (derived only as fallback when the token carries no DRIFT_CLASS line).
    Classes: absent-live, added-live, agreed, class-changed:<snapshot>-><live>.
    """
    live_set = set(live_tokens)
    pairs = []
    seen = set()
    for token in snapshot_tokens:
        if token in seen:
            continue
        seen.add(token)
        if token not in live_set:
            pairs.append((token, "absent-live"))
            continue
        snap_cls = stated.get(token) or derive(token, names)
        live_cls = derive(token, names)
        if snap_cls == live_cls:
            pairs.append((token, "agreed"))
        else:
            pairs.append((token, "class-changed:%s->%s" % (snap_cls, live_cls)))
    for token in live_tokens:
        if token in seen:
            continue
        seen.add(token)
        pairs.append((token, "added-live"))
    return pairs


def classifications(text):
    stated, malformed, duplicates = {}, 0, 0
    for line in text.splitlines():
        if not line.startswith("DRIFT_CLASS"):
            continue
        m = CLASS_LINE.match(line)
        if not m or m.group(2) not in CLASS_WORDS:
            malformed += 1
            continue
        if m.group(1) in stated:
            duplicates += 1
        stated[m.group(1)] = m.group(2)
    return stated, malformed, duplicates


def header(text):
    """The provenance block: snapshot path, its sha256 and the as-of moment.

    R02 repair (pre-data): each line must occur exactly once, and the path must be the frozen
    snapshot. A duplicate line would make the receipt true under one reading and false under
    another, which the frozen sentence ("exactly one each") forbids.
    """
    snap, digest, asof = None, None, None
    seen = {"snap": 0, "sha": 0, "asof": 0}
    for line in text.splitlines():
        if not line.startswith("#"):
            break
        m = SNAP_LINE.match(line)
        if m:
            seen["snap"] += 1
            snap = m.group(1)
            continue
        m = SNAP_SHA.match(line)
        if m:
            seen["sha"] += 1
            digest = m.group(1)
            continue
        m = ASOF.match(line)
        if m:
            seen["asof"] += 1
            asof = m.group(1)
    if seen["snap"] != 1 or seen["sha"] != 1 or seen["asof"] != 1:
        return None, None, None
    return snap, digest, asof


def drift_tokens(text):
    tokens = []
    for line in text.splitlines():
        m = DRIFT.match(line)
        if m:
            tokens = [token for token in m.group(1).split() if token != "none"]
    return tokens


def run_start(text):
    m = RUNSTART.search(text)
    if not m:
        return None
    try:
        stamp = datetime.datetime.fromisoformat(m.group(1))
    except ValueError:
        return None
    if stamp.tzinfo is None:
        return None
    return stamp.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def section_rows(text, heading):
    inside, rows = False, []
    for line in text.splitlines():
        if re.match(r"^##\s", line):
            inside = line.strip() == heading
            continue
        if inside and line.lstrip().startswith("|"):
            cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
            if cells:
                rows.append((cells, line))
    return rows


def retired_ok(text, snapshot):
    for cells, line in section_rows(text, "## Retired"):
        if cells and cells[0] == "drift-pin-r10":
            return BASELINE in line and CLASSES in line and snapshot in line
    return False


def cell_state(text):
    for cells, line in section_rows(text, "## Axes"):
        if cells and cells[0].strip("` ") == "freshness":
            return ("r10 pin retired" in line and CLASSES in line
                    and "round-10 drift pin still red" not in line)
    return False


def live_read(census, baseline, scratch, fleet_root):
    work = tempfile.mkdtemp(dir=scratch)
    paths = {}
    for name, body in ((CENSUS, census), (BASELINE, baseline)):
        target = os.path.join(work, name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(body)
        paths[name] = target
    env = dict(os.environ)
    env.update(TMPDIR=work, MORI_SHOKUNIN_ROOT=fleet_root)
    try:
        p = run(["bash", paths[CENSUS], "--drift", paths[BASELINE]], cwd=work, env=env)
    except subprocess.TimeoutExpired:
        return None, [], "timeout"
    output = (p.stdout or "") + (p.stderr or "")
    return p.returncode, drift_tokens(output), ""


def grade(loader, scratch, fleet_root):
    census = loader(CENSUS)
    baseline = loader(BASELINE)
    cards = loader(CARDS)
    classes = loader(CLASSES)
    if census is None or baseline is None or cards is None:
        return False, "setup=census/baseline/SCORECARD absent", []
    if classes is None:
        return False, "snapshot=absent tokens=0 agreed=0 residual=0 live=unavailable", []
    snap_path, snap_sha, asof = header(classes)
    if snap_path is None:
        return False, "snapshot=absent tokens=0 agreed=0 residual=0 live=unavailable", []
    if snap_path != FROZEN_SNAPSHOT:
        return False, ("snapshot=unbound:path=%s tokens=0 agreed=0 residual=0 "
                       "live=unavailable" % snap_path), []
    snapshot = loader(snap_path)
    if snapshot is None:
        return False, ("snapshot=unbound:snapshot-absent tokens=0 agreed=0 residual=0 "
                       "live=unavailable"), []
    notes = []
    live_rc, live_tokens, live_reason = live_read(census, baseline, scratch, fleet_root)
    stated, malformed, duplicates = classifications(classes)
    names = baseline_names(baseline)
    snapshot_tokens = drift_tokens(snapshot)
    agreed = 0
    residual = 0
    unclassified = [token for token in snapshot_tokens if token not in stated]
    for token in snapshot_tokens:
        if token not in stated:
            continue
        if stated[token] == "unexplainable":
            residual += 1
        elif stated[token] == derive(token, names):
            agreed += 1
    stale = [token for token in stated if token not in snapshot_tokens]
    residual += duplicates
    digest = hashlib.sha256(snapshot.encode("utf-8")).hexdigest()
    hash_ok = snap_sha is not None and digest == snap_sha
    stamp = run_start(snapshot)
    asof_ok = asof is not None and stamp is not None and asof == stamp
    live_ok = live_rc == 1 and bool(live_tokens)
    live_agree = len([token for token in live_tokens
                      if stated.get(token) == derive(token, names)])
    retired = retired_ok(cards, snap_path)
    cell = cell_state(cards)
    delta_pairs = live_delta(snapshot_tokens, live_tokens, names, stated)
    union_n = len(delta_pairs)
    absent_live = sum(1 for _, cls in delta_pairs if cls == "absent-live")
    added_live = sum(1 for _, cls in delta_pairs if cls == "added-live")
    class_changed = sum(1 for _, cls in delta_pairs if cls.startswith("class-changed:"))
    deltas = absent_live + added_live + class_changed
    met = (hash_ok and asof_ok and bool(snapshot_tokens) and not unclassified
           and residual == 0 and malformed == 0 and duplicates == 0 and not stale
           and agreed == len(snapshot_tokens) and live_ok and retired and cell
           and agreed == live_agree
           and union_n == len(set(token for token, _ in delta_pairs)))
    tail = ("snapshot=%s asof=%d tokens=%d agreed=%d residual=%d live=%s "
            "live_tokens=%d live_agree=%d delta=classified classified=%d union=%d "
            "absent_live=%d added_live=%d class_changed=%d deltas=%d"
            % ("bound" if (hash_ok and asof_ok) else "unbound",
               1 if asof_ok else 0, len(snapshot_tokens), agreed,
               residual + malformed, "derived" if live_ok else "unavailable",
               len(live_tokens), live_agree, union_n, union_n,
               absent_live, added_live, class_changed, deltas))
    if not hash_ok:
        notes.append("snapshot-hash-mismatch stated=%s measured=%s"
                     % (snap_sha, digest[:64]))
    if not asof_ok:
        notes.append("asof-mismatch stated=%s snapshot-run-start=%s" % (asof, stamp))
    if live_rc != 1:
        notes.append("metric=live-census-rc:%s%s"
                     % (live_rc, (":" + live_reason) if live_reason else ""))
    for token in unclassified[:6]:
        notes.append("unclassified " + token)
    for token in snapshot_tokens:
        if token in stated and stated[token] != "unexplainable":
            if stated[token] != derive(token, names):
                notes.append("class-disagrees %s stated=%s derived=%s"
                             % (token, stated[token], derive(token, names)))
    for token in stale[:6]:
        notes.append("stale-classification " + token)
    if malformed:
        notes.append("malformed-classification-lines=%d" % malformed)
    if duplicates:
        notes.append("duplicate-classification-lines=%d" % duplicates)
    if not retired:
        notes.append("retired-row-missing-paths")
    if not cell:
        notes.append("freshness-cell-red")
    for token, cls in delta_pairs:
        if cls != "agreed":
            notes.append("LIVE_DELTA %s %s" % (token, cls))
    return met, tail, notes


def selfcheck(scratch):
    cases = []
    base = ("# mori-drift-baseline v1\n# volatile_fields=x\n"
            "# --- canonical output follows ---\n"
            "SURFACE watchdog: pid=1 state=ok\n"
            "FINDING OOM_KILL_JOURNAL severity=crit paths=a\n"
            "lane.mori fields=1\nMORI_CENSUS: DRIFT (findings=0 drift=0)\n")
    stub = ("#!/bin/sh\nprintf 'MORI_DRIFT: +SURFACE:lane.new +audit fields +VERDICT\\n'\n"
            "exit 1\n")
    snapshot = ("# run-start: 2026-11-04T07:45:13.552564+00:00\n# cwd: /x\n"
                "$ bash tools/mori-census.sh --drift corpus/evidence/"
                "baseline-r10-20261015T2231Z.json\n"
                "MORI_DRIFT: +SURFACE:lane.new +audit fields +VERDICT\nrc=1\n")
    cards_clean = (
        "# t\n\n## Axes\n\n| Axis | Score | Evidence | Last change |\n|---|---|---|---|\n"
        "| freshness | 5 | r10 pin retired at corpus/evidence/drift-classification-r82.txt "
        "| round 83 |\n\n## Retired\n\n| Axis | Reason | Round |\n|---|---|---|\n"
        "| drift-pin-r10 | retired: baseline corpus/evidence/"
        "baseline-r10-20261015T2231Z.json fully classified at "
        "corpus/evidence/drift-classification-r82.txt from .ufo/waves/round-82/evidence/"
        "drift-r82-live.txt | 82 |\n")
    digest = hashlib.sha256(snapshot.encode("utf-8")).hexdigest()
    good = {
        "+SURFACE:lane.new": "added-since-r10",
        "+audit": "added-since-r10",
        "fields": "value-changed",
        "+VERDICT": "value-changed",
    }

    def build(label, head, rows, cards=cards_clean, rc=1):
        d = tempfile.mkdtemp(dir=scratch, prefix="c2-" + label + "-")
        files = {CENSUS: stub if rc == 1 else
                 "#!/bin/sh\nprintf 'MORI_DRIFT: none\\n'\nexit 0\n",
                 BASELINE: base, CARDS: cards,
                 ".ufo/waves/round-82/evidence/drift-r82-live.txt": snapshot}
        if rows is not None:
            files[CLASSES] = head + "".join(
                "DRIFT_CLASS %s %s\n" % (token, cls) for token, cls in rows.items())
        for name, body in files.items():
            target = os.path.join(d, name)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            open(target, "w", encoding="utf-8").write(body)
        loader = lambda path: (open(os.path.join(d, path), encoding="utf-8").read()
                               if os.path.exists(os.path.join(d, path)) else None)  # noqa: E731
        return grade(loader, scratch, d)

    head = ("# Date: 2026-11-04\n# Baseline: " + BASELINE + "\n"
            "# Snapshot: .ufo/waves/round-82/evidence/drift-r82-live.txt\n"
            "# Snapshot-sha256: " + digest + "\n"
            "# As-of: 2026-11-04T07:45:13Z\n")
    met, tail, notes = build("clean", head, good)
    cases.append(("conformant", met and "tokens=4" in tail and "live=derived" in tail,
                  tail + " | " + ";".join(notes)))
    nohead = head.replace("# Snapshot: .ufo/waves/round-82/evidence/drift-r82-live.txt\n", "")
    met, tail, _ = build("nohead", nohead, good)
    cases.append(("snapshot_absent", (not met) and "snapshot=absent" in tail, tail))
    badsha = head.replace(digest, "0" * 64)
    met, tail, notes = build("badsha", badsha, good)
    cases.append(("hash_mismatch", (not met) and "snapshot=unbound" in tail
                  and any("hash" in n for n in notes), tail))
    badasof = head.replace("2026-11-04T07:45:13Z", "2026-11-04T07:45:14Z")
    met, tail, notes = build("badasof", badasof, good)
    cases.append(("asof_mismatch", (not met) and "asof=0" in tail, tail))
    partial = dict(good)
    partial.pop("+audit")
    met, tail, _ = build("partial", head, partial)
    cases.append(("unclassified_token", (not met) and "agreed=3" in tail, tail))
    wrong = dict(good, fields="added-since-r10")
    met, tail, _ = build("wrong", head, wrong)
    cases.append(("class_disagrees", (not met) and "agreed=3" in tail, tail))
    met, tail, _ = build("green", head, good, rc=0)
    cases.append(("green_live_unmet", (not met) and "live=unavailable" in tail, tail))
    dup = head + "DRIFT_CLASS +audit added-since-r10\n" + "".join(
        "DRIFT_CLASS %s %s\n" % (token, cls) for token, cls in good.items())
    d = tempfile.mkdtemp(dir=scratch, prefix="c2-dup2-")
    for name, body in ((CENSUS, stub), (BASELINE, base), (CARDS, cards_clean),
                       (".ufo/waves/round-82/evidence/drift-r82-live.txt", snapshot),
                       (CLASSES, dup)):
        target = os.path.join(d, name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(body)
    loader = lambda path: (open(os.path.join(d, path), encoding="utf-8").read()
                           if os.path.exists(os.path.join(d, path)) else None)  # noqa: E731
    met2, tail2, _ = grade(loader, scratch, d)
    cases.append(("duplicate_line_residual", (not met2) and "residual=1" in tail2, tail2))
    bad_card = cards_clean.replace(" from .ufo/waves/round-82/evidence/"
                                   "drift-r82-live.txt", "")
    met, tail, notes = build("nocardsnap", head, good, cards=bad_card)
    cases.append(("retired_row_snapshot_required",
                  (not met) and any("retired-row" in n for n in notes), tail))
    red_cards = cards_clean.replace("r10 pin retired", "round-10 drift pin still red")
    met, tail, _ = build("redcell", head, good, cards=red_cards)
    cases.append(("red_cell_keeps_unmet", (not met) and "live=derived" in tail, tail))
    dup_head = head + "# Snapshot: .ufo/waves/round-82/evidence/drift-r82-live.txt\n"
    met, tail, _ = build("duphead", dup_head, good)
    cases.append(("duplicate_header_unmet", (not met) and "snapshot=absent" in tail, tail))
    foreign = head.replace(".ufo/waves/round-82/evidence/drift-r82-live.txt",
                           "corpus/evidence/other-snapshot.txt", 1)
    met, tail, notes = build("foreign", foreign, good)
    cases.append(("foreign_snapshot_path_unmet",
                  (not met) and any("snapshot=unbound" in n for n in notes) is False
                  and "snapshot=unbound" in tail, tail))
    # P-C3 delta arms: pure classifier over synthetic snapshot/live pairs (no census run).
    names = ({"surface.other"}, set(), {"fields"})
    pairs = live_delta(["+SURFACE:lane.new", "fields"],
                       ["+SURFACE:lane.new", "fields"], names,
                       {"+SURFACE:lane.new": "added-since-r10",
                        "fields": "value-changed"})
    cases.append(("delta_agreed", pairs == [("+SURFACE:lane.new", "agreed"),
                                            ("fields", "agreed")], str(pairs)))
    pairs = live_delta(["+audit"], [], names, {"+audit": "added-since-r10"})
    cases.append(("delta_absent_live", pairs == [("+audit", "absent-live")], str(pairs)))
    pairs = live_delta([], ["+VERDICT"], names, {})
    cases.append(("delta_added_live", pairs == [("+VERDICT", "added-live")], str(pairs)))
    pairs = live_delta(["fields"], ["fields"], names, {"fields": "added-since-r10"})
    cases.append(("delta_class_changed",
                  pairs == [("fields",
                             "class-changed:added-since-r10->value-changed")], str(pairs)))
    ok = sum(1 for _, good_case, _ in cases if good_case)
    for label, good_case, line in cases:
        print("%s %s %s" % ("PASS" if good_case else "FAIL", label, line))
    print("C2_COUNTER_SELFTEST pass=%d fail=%d" % (ok, len(cases) - ok))
    return 0 if ok == len(cases) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--scratch")
    ap.add_argument("--fleet-root")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c2-r83-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
        if not a.rev:
            print("C2_SETUP usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] | --selftest",
                  file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else a.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print("C2_SETUP unresolvable revision " + a.rev, file=sys.stderr)
            return 2
        rev = p.stdout.strip()
        fleet = a.fleet_root or (os.path.dirname(repo) if repo.endswith("-shokunin")
                                 else repo)

        def loader(path):
            q = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])
            return q.stdout if q.returncode == 0 else None

        met, tail, notes = grade(loader, scratch, fleet)
        if tail.startswith("setup="):
            print("C2_SETUP " + tail, file=sys.stderr)
            return 2
        for note in notes:
            print(note)
        print("C2=%s %s rev=%s" % ("met" if met else "unmet", tail, rev[:12]))
        return 0 if met else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
