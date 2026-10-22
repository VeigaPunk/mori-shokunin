#!/usr/bin/env bash
set -euo pipefail
if (($# != 2)); then printf 'usage: count-c1.sh <lane-rev> <fleet-rev>\n' >&2; exit 2; fi
export MORI_C1_LANE_REPO="${MORI_C1_LANE_REPO:-/home/vgpnk/Projects/shokunin/mori-shokunin}"
export MORI_C1_FLEET_REPO="${MORI_C1_FLEET_REPO:-/home/vgpnk/Projects/shokunin}"
exec python3 - "$@" <<'PY'
import json, os, re, subprocess, sys

AXES = ("coverage", "operability", "depth", "freshness", "calibration", "adjacency")
BASE = "7118f320a5ef18d20c1e361eff77db0e1a97b2d6"
SPOT = "corpus/lessons/round-{round}-verifier-spotcheck.md"
MANIFEST_CITE = "MANIFEST.json@63729047 mori round {round}"
VERDICTS = "improved|unchanged|harmed|unprovable-but-better"
AXIS_LINE = re.compile(r"^\|\s*(coverage|operability|depth|freshness|calibration|adjacency)\s*\|\s*(" + VERDICTS + r")\s*\|")
POINTER = re.compile(r"([^`:\s]+):([0-9]+)(?:-([0-9]+))?")
TRANSITION = re.compile(r"([0-9]+)\s*(?:→|->)\s*([0-9]+)")

class InputError(Exception): pass

git_env = os.environ.copy()
for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"): git_env.pop(key, None)

def git(repo, *args):
    try: return subprocess.run(["git", "-C", repo, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=git_env, check=False)
    except OSError as exc: raise InputError("cannot run git: {}".format(exc)) from exc

def resolve(repo, rev, label):
    result = git(repo, "rev-parse", "--verify", "--end-of-options", rev + "^{commit}")
    if result.returncode: raise InputError("bad {} revision".format(label))
    return result.stdout.decode("ascii", "strict").strip()

def blob(repo, rev, path):
    result = git(repo, "show", "{}:{}".format(rev, path))
    return result.stdout if result.returncode == 0 else None

def text_blob(repo, rev, path, label):
    data = blob(repo, rev, path)
    if data is None: raise InputError("missing {}: {}".format(label, path))
    try: return data.decode("utf-8")
    except UnicodeDecodeError as exc: raise InputError("invalid UTF-8 in {}: {}".format(label, path)) from exc

def axis_rows(text, label):
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == "## Axes"), -1)
    if start < 0: raise InputError("missing ## Axes in {}".format(label))
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    rows, count = {}, 0
    for line in lines[start + 1:end]:
        cells = line.split("|") if line.startswith("|") else []
        if len(cells) < 2 or cells[1].strip() not in AXES: continue
        count += 1; axis = cells[1].strip()
        if len(cells) < 5: raise InputError("malformed {} row in {}".format(axis, label))
        if axis in rows: raise InputError("duplicate {} row in {}".format(axis, label))
        rows[axis] = {"score": cells[2].strip(), "row": line, "last": cells[4].strip()}
    if count != 6 or set(rows) != set(AXES): raise InputError("expected exactly six distinct Axes rows in {}".format(label))
    return rows

def manifest_rounds(text):
    try: data = json.loads(text)
    except json.JSONDecodeError as exc: raise InputError("malformed MANIFEST.json") from exc
    if not isinstance(data, dict) or not isinstance(data.get("rounds"), list): raise InputError("malformed MANIFEST.json rounds")
    return data["rounds"]

def admitted(entry): return isinstance(entry, dict) and entry.get("verdict") == "admitted"
def verdict(entry, axis): return entry.get("verdicts", {}).get(axis) if isinstance(entry.get("verdicts"), dict) else None
def axis_lines(text):
    return [(m.group(1), m.group(2)) for line in text.splitlines() for m in [AXIS_LINE.match(line)] if m]
def score_line(line, axis, old, new):
    if not re.search(r"\b{}\b".format(re.escape(axis)), line): return False
    return any((int(a), int(b)) == (old, new) for a, b in TRANSITION.findall(line))
def non_author(entry):
    verification = entry.get("verification")
    reviewer = verification.get("reviewer") if isinstance(verification, dict) else None
    if not isinstance(reviewer, str) or "non-author" not in reviewer.lower(): return False
    return reviewer.split("(", 1)[0].strip().lower() not in ("", "reviewer", "unknown", "none")

def main():
    if len(sys.argv) != 3: raise InputError("usage: count-c1.sh <lane-rev> <fleet-rev>")
    lane, fleet = os.environ["MORI_C1_LANE_REPO"], os.environ["MORI_C1_FLEET_REPO"]
    lane_rev, fleet_rev = resolve(lane, sys.argv[1], "lane"), resolve(fleet, sys.argv[2], "fleet")
    current = axis_rows(text_blob(lane, lane_rev, "SCORECARD.md", "scorecard"), "SCORECARD.md")
    baseline = axis_rows(text_blob(lane, BASE, "SCORECARD.md", "baseline scorecard"), "baseline SCORECARD.md")
    for axis in AXES:
        if not re.fullmatch(r"[0-9]+", baseline[axis]["score"]): raise InputError("invalid baseline score for {}".format(axis))
        baseline[axis]["score"] = int(baseline[axis]["score"])
    rounds = manifest_rounds(text_blob(fleet, fleet_rev, "MANIFEST.json", "manifest"))
    mori = []
    for index, entry in enumerate(rounds):
        if not isinstance(entry, dict) or entry.get("lane") != "mori": continue
        number = entry.get("round")
        if not isinstance(number, int) or isinstance(number, bool): continue
        mori.append((index, number, entry))
    admitted_rounds = {n for _, n, entry in mori if admitted(entry)}
    cache = {}
    def file_text(path):
        if path not in cache:
            data = blob(lane, lane_rev, path); cache[path] = None if data is None else data.decode("utf-8", "replace")
        return cache[path]
    def spot_text(number): return file_text(SPOT.format(round=number))
    latest = {}
    for axis in AXES:
        candidates = [(n, i, e) for i, n, e in mori if 12 <= n <= 28 and admitted(e) and verdict(e, axis) == "improved"]
        latest[axis] = max(candidates, key=lambda x: (x[0], x[1])) if candidates else None
    disagreements = {axis: 0 for axis in AXES}
    for _, number, entry in mori:
        if not 12 <= number <= 28: continue
        text = spot_text(number)
        if text is not None:
            for axis, observed in axis_lines(text):
                if observed != verdict(entry, axis): disagreements[axis] += 1

    def cite_lines(row, path):
        return [int(m.group(1)) for m in re.finditer(r"`" + re.escape(path) + r":([0-9]+)`", row)]
    def manifest_lines(row, citation):
        return [int(m.group(1)) for m in re.finditer(re.escape(citation) + r":([0-9]+)", row)]
    def score_basis(row, axis, old, new):
        for _, number, entry in mori:
            if not admitted(entry): continue
            path, text = SPOT.format(round=number), spot_text(number)
            if text is not None:
                lines = text.splitlines()
                for n in cite_lines(row, path):
                    if 1 <= n <= len(lines) and score_line(lines[n - 1], axis, old, new): return "{}:{}".format(path, n)
            else:
                cite = MANIFEST_CITE.format(round=number)
                serialized = json.dumps(entry, ensure_ascii=False, separators=(",", ":")).splitlines()
                for n in manifest_lines(row, cite):
                    if 1 <= n <= len(serialized) and score_line(serialized[n - 1], axis, old, new): return "{}:{}".format(cite, n)
        return None
    def unprovable_basis(row, axis):
        for _, number, entry in mori:
            if not admitted(entry) or not non_author(entry): continue
            path, text = SPOT.format(round=number), spot_text(number)
            if text is not None:
                lines = text.splitlines()
                for n in cite_lines(row, path):
                    if 1 <= n <= len(lines):
                        match = AXIS_LINE.match(lines[n - 1])
                        if match and match.group(1) == axis and match.group(2) == "unprovable-but-better": return "{}:{}".format(path, n)
            else:
                cite = MANIFEST_CITE.format(round=number)
                serialized = json.dumps(entry, ensure_ascii=False, separators=(",", ":")).splitlines()
                for n in manifest_lines(row, cite):
                    if (1 <= n <= len(serialized) and verdict(entry, axis) == "unprovable-but-better"
                            and "unprovable-but-better" in serialized[n - 1]): return "{}:{}".format(cite, n)
        return None

    output, mismatches = [], 0
    for axis in AXES:
        row, text, kinds, count = current[axis], current[axis]["row"], set(), 0
        recent = latest[axis]
        if recent is None: round_number = None
        else:
            round_number, _, _ = recent
            path, content = SPOT.format(round=round_number), spot_text(round_number)
            if content is None:
                if MANIFEST_CITE.format(round=round_number) not in text: kinds.add(1); count += 1
            else:
                lines, table, refs = content.splitlines(), axis_lines(content), cite_lines(text, path)
                valid = bool(refs)
                if table:
                    valid = any(1 <= n <= len(lines) and (m := AXIS_LINE.match(lines[n - 1])) is not None
                                and m.group(1) == axis and m.group(2) == "improved" for n in refs)
                if not valid: kinds.add(1); count += 1

        change = re.match(r"^round\s+([0-9]+)\b", row["last"])
        last_ok = bool(change)
        if change:
            last_n = int(change.group(1)); last_ok = last_n in admitted_rounds and (recent is None or last_n >= recent[0])
        score_n = int(row["score"]) if re.fullmatch(r"[0-9]+", row["score"]) else None
        arrow = re.search(r"\(\s*([0-9]+)\s*(?:→|->)\s*([0-9]+)(?=\s*(?:;|\)|$))", row["last"])
        if arrow and (score_n is None or int(arrow.group(2)) != score_n): last_ok = False
        # Amendment A2 kind 2b: a stated (X → Y) for round N needs MANIFEST verdicts.<axis> == improved for round N.
        if arrow and change and not any(n == int(change.group(1)) and verdict(e, axis) == "improved" for _, n, e in mori): last_ok = False
        if score_n is not None and score_n == baseline[axis]["score"] and not arrow and "(improved, score held)" not in row["last"]: last_ok = False
        if not last_ok: kinds.add(2); count += 1

        dead = 0
        for token in re.findall(r"`([^`]+)`", text):
            pointer = POINTER.fullmatch(token); path = pointer.group(1) if pointer else token
            if "/" not in token and not re.search(r"\.(?:md|json|py|sh)$", path): continue
            data = blob(lane, lane_rev, path)
            if data is None: dead += 1
            elif pointer and len(data.splitlines()) < max(int(pointer.group(2)), int(pointer.group(3) or pointer.group(2))): dead += 1
        if dead: kinds.add(3); count += dead

        score, basis, kind4 = row["score"], "held", False
        if re.fullmatch(r"[0-9]+", score):
            value = int(score)
            if not 0 <= value <= 10: basis, kind4 = "none", True
            elif value != baseline[axis]["score"]:
                basis = score_basis(text, axis, baseline[axis]["score"], value) or "none"; kind4 = basis == "none"
        elif score == "unprovable-but-better":
            basis = unprovable_basis(text, axis) or "none"; kind4 = basis == "none"
        else: basis, kind4 = "none", True
        if kind4: kinds.add(4); count += 1
        if disagreements[axis]: kinds.add(5); count += disagreements[axis]
        mismatches += count
        labels = ",".join(str(n) for n in sorted(kinds)) or "none"
        output.append("axis={} score={} basis={} R={} kinds={}".format(axis, score, basis, round_number if round_number is not None else "none", labels))
    print("\n".join(output)); print("mismatches={}".format(mismatches))
    print("C1={}".format("met" if mismatches == 0 else "unmet"))
    return 0 if mismatches == 0 else 1

try: sys.exit(main())
except InputError as exc:
    print("count-c1: {}".format(exc), file=sys.stderr); sys.exit(2)
PY
