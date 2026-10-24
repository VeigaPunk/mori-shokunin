# Round 28 wave 1 - BuildCountC2: hardened C2 counter

Seat: MoriR28.BuildCountC2 (executor, leaf). Deliverable: the round-28 C2 counter at
`/fast/scratch/hyaku/mori-r28/BuildCountC2/count-c2.sh` (465 lines) — the L1 copies it into
`.ufo/waves/round-28/count-c2.sh`; this seat writes nothing to the lane except this report.

- sha256: `a7536fc5a404b9f3b4cdaa09f2aeef4dbed6980abb463fafe777df8481c1f638`
  (`sha256sum /fast/scratch/hyaku/mori-r28/BuildCountC2/count-c2.sh`)
- Usage: `bash .ufo/waves/round-28/count-c2.sh <rev>`; exit 0 met, 1 unmet, 2 usage/bad input.
- Sandbox hook: `MORI_C2_LANE=<dir>` overrides the lane path so the same bytes measure a
  clone; unset it defaults to the committed lane. No other interface.
- Drive transcript (fresh clone of the lane at 079a47c6 plus synthetic commits):
  `/fast/scratch/hyaku/mori-r28/BuildCountC2/drive-out.txt` (526 lines); harness `drive.sh`,
  inputs `/fast/scratch/hyaku/mori-r28/BuildCountC2/inputs/`, generator `gen-valid.py`
  (sandbox only — its 20 invented cases are a met-proof fixture, never handed to the L1).

## Hardening against `.ufo/waves/round-27/w1/CriticC2Counter.md`

| Finding | Fix in the new counter | Proof (drive-out.txt) |
|---|---|---|
| F1 verdict+exit-only tags pass | per-rule: >=2 cases, >=2 distinct canonical-JSON inputs, >=1 case pinning the rule's field | S1 trivial20: `a2_rule_checks=fail: ... distinct_inputs<2 ... no_required_field_pin`, unmet (:44-56) |
| F2 field pin vs verdict pin | required-field map is fixed in the script (below); A2-07 requires `earlyoom.earlier_invocation_send_lines` integer >0 per the L1's round-28 change | S11: mutant tool fails field-pinned case `FAIL 0/1`, passes verdict-only (:391-395); S13 pinned-0 unmet (:431-465) |
| F3 forged PASS line in an id | ids must be unique non-empty `str.isprintable()`; exactly one `^MORI_OOM_KILLERS_SELFTEST: ` line required | S2 forged-id: `a2_schema=error case 19 id is not a printable non-empty string`, unmet (:74-76); tool would emit 2 markers anyway (:78-84) |
| F4 FAIL-then-PASS mutant tool | tool exit status checked first; marker count must be exactly 1 | S3: `a2_selftest=FAIL(exit=1)`, unmet (:118-120) |
| F5 weakened frozen cases.json | `rev-parse <rev>:cases.json` must equal `rev-parse fc09f96c...:cases.json` | S4: `frozen_blob=mismatch`, unmet (:131,160-161) |
| F6 rename hides earlier add | `--follow` finds the draft-path add; any `R`/`D` entry fails | S5: `freeze_path=cases-a2-draft.json`, `freeze_renames=1`, `freeze_edits=1`, unmet (:170-178) |
| F7 merge hides earlier add | `--full-history -m` walks every parent; a candidate add is genuine only when no parent carries the file | S7a two real adds: `freeze_adds=2`, unmet (:277-283); S7b merge-add: `freeze_adds=1` after dedup, unmet on content (:311-336) |
| F8 edited freeze history | prints `freeze_commit`, `freeze_path`, `freeze_blob_versions`, `tool_blob_at_freeze` so the recorded LOG.md hash can be compared (counter cannot see rewritten history); blob-version count rejects edit-then-revert | S6b: `freeze_edits=2 freeze_blob_versions=2 cases_changed_since_freeze=1`, unmet (:246-248) |
| F11 silent parse failures / `0 0` | strict JSON+schema validation; `a2_schema=error <reason>` then unmet; absent file prints `a2_schema=absent`/`a2_cases=0`, never a PASS | S9: list-rule and truncated JSON both `a2_schema=error`, unmet (:357,375); S0 absent at 079a47c6 unmet (:18-21) |
| F12 missing frozen file at rev | `cat-file -e` on both fixed paths before any extract | S8: `frozen_absent`, exit 2 (:338-340) |

Required pinned field per rule (wave context + L1's A2-07 change): A2-01 `earlyoom.scope_complete`,
A2-02 `earlyoom.state`, A2-03 `earlyoom.process_group_lines`, A2-04 `earlyoom.dryrun_send_lines`,
A2-05 `earlyoom.scope_complete`, A2-06 `earlyoom.earlier_invocation_send_lines`, A2-07
`earlyoom.earlier_invocation_send_lines` (int >0), A2-08 `earlyoom.state` (>=1 case pinned to a
value != "active"), A2-09 `earlyoom.state`, A2-10 `earlyoom.scope_complete`.

## Scenario table (sandbox clone of the lane, `MORI_C2_LANE` pointed at it)

| Scenario | Result | Exit |
|---|---|---|
| S0 rev 079a47c6, a2 file absent | `a2_schema=absent a2_cases=0 a2_selftest=absent C2=unmet` | 1 |
| S1 F1 trivial20 self-declared tags | rule_checks fail all rules, `a2_selftest=PASS 20/20` but `C2=unmet` | 1 |
| S2 F3 forged PASS in id (stock tool) | `a2_schema=error`, unmet | 1 |
| S3 F4 mutant tool exit 1 + extra PASS line | `a2_selftest=FAIL(exit=1)`, unmet | 1 |
| S4 F5 weakened frozen cases.json | `frozen_blob=mismatch`, unmet | 1 |
| S5 F6 rename (draft -> git mv) | `freeze_renames=1`, `cases_changed_since_freeze=1`, unmet | 1 |
| S6a F9 delete + re-add | `freeze_adds=2`, unmet | 1 |
| S6b F8 edit then revert | `freeze_blob_versions=2`, `cases_changed_since_freeze=1`, unmet | 1 |
| S7a F7 merge keeps v2 (2 real adds) | `freeze_adds=2`, unmet | 1 |
| S7b F10 merge adds the file | `freeze_adds=1` (deduped -m entries), unmet on rule/content checks | 1 |
| S8 F12 frozen cases.json deleted at rev | `frozen_absent` | 2 |
| S9 F11 list-valued `rule`; truncated JSON; python3->127 | `a2_schema=error ...` / `a2_schema=error json: ...` / `validator produced no result`, all unmet | 1 |
| S10 cwd independence (/, clone, decoy) | identical unmet output each cwd | 1 |
| S11 F2 verdict-only vs field pin under A2-03 mutant tool | stock PASS 1/1 both; mutant `FAIL 0/1` for field-pinned case | - |
| S12 valid synthetic file | `a2_rule_checks=ok a2_selftest=PASS 20/20 C2=met` | 0 |
| S13 valid file, A2-07 pinned 0 | `A2-07(no_required_field_pin)`, unmet | 1 |
| S14 bool `expect.exit` | `a2_schema=error ... expect.exit is missing or not an integer`, unmet | 1 |
| S15 A2-08 all pins `active` | `A2-08(state_pinned_active_only)`, unmet | 1 |
| S16 usage / bad rev / extra arg | `usage: ...` / `bad_rev` / `usage: ...` | 2 |
| python3 exits 127 mid-run (fakebin) | `frozen32_selftest=FAIL(exit=127)`, `validator produced no result`, unmet | 1 |

## Run at the landing revision

`MORI_C2_LANE=<clone> bash count-c2.sh 079a47c61691f2b891d35458057b294ca5a99e77` (also run against
the real lane, same output):

```
rev=079a47c61691f2b891d35458057b294ca5a99e77
tool_blob=3fb78bbc2612c38e463e04083bdb213954647568
frozen_blob=match
frozen32_selftest=PASS 32/32
freeze_commit=none
freeze_path=none
freeze_adds=0
freeze_adds_raw=0
freeze_renames=0
freeze_deletes=0
freeze_edits=0
freeze_blob_versions=0
cases_changed_since_freeze=1
a2_schema=absent
a2_cases=0
a2_selftest=absent
C2=unmet
exit=1
```

## Design decisions and residuals (for the L1)

- "Unchanged since the freeze" is enforced as: exactly one blob version across the whole
  `M`/`A`/`R` history plus tip blob == freeze blob. This rejects edit-then-revert (S6b),
  which the round-27 counter passed — stricter than byte-compare and deliberate: the freeze
  claim is "committed then never touched".
- An add is genuine only if no parent of the candidate commit carries the file. A merge that
  merely differs from one parent therefore does not count (verified: mainline add merged with
  an unrelated branch still reads `freeze_adds=1`, `C2=met`). A merge commit whose diff itself
  first introduces the file counts as the single add — that is where the file first exists;
  flag for the L1 in case the claim wants to forbid merge-introduced freezes entirely.
- `tool_blob_at_freeze` is printed when a freeze commit exists (for LOG.md cross-check, F8).
- Distinct-inputs check is per rule (>=2) and a global `a2_distinct_inputs` tally is printed;
  identical inputs in two different rules do not fail the per-rule check but lower the tally.
- Schema errors exit 1 with `a2_schema=error <reason>`; structural faults (missing/absent
  `inputs`, non-dict `expect`, bool `exit`) are schema errors by design.
- Not checked (process-level, out of counter scope): whether LOG.md recorded the freeze hash
  before the first tool run — the counter prints the facts the L1 needs for that check.
- If the python3 validator emits nothing (interpreter missing mid-run), the counter reports
  `a2_schema=error validator produced no result` and unmet — fail-closed.

## Tooling and bounds

- No tools installed or updated; used python3 3.14.8 and git 2.56.0 as found.
- No lane writes except this report; all commits in the sandbox clone
  (`/fast/scratch/hyaku/mori-r28/BuildCountC2/lane`); no jj, no git ref/index mutation in the
  lane, no pushes. No units touched, no signals sent. All fixture values invented.
- Privacy: sandbox commit metadata uses placeholder author `c <c@s>`; no host session data in
  inputs, outputs, or this report.

## The counter

```bash
#!/usr/bin/env bash
# Round 28, claim C2 counter. Reads committed bytes only: the tool and both case files are
# extracted from <rev> into a temporary directory and the self-test runs there, never on the
# working tree.
#
# Usage: bash .ufo/waves/round-28/count-c2.sh <rev>
#
# Exit codes: 0 when C2=met, 1 when C2=unmet (including any self-test that does not print
# PASS N/N), 2 on a usage error, a bad revision, a missing tool or a missing round-26 file.
# Each of those three input faults prints its own message.
#
# Hardened against .ufo/waves/round-27/w1/CriticC2Counter.md F1-F8 and F11:
#   F1  every rule needs at least two cases with distinct canonical-JSON inputs, and at least
#       one case per rule whose expect.fields pins the field that rule decides;
#   F2  the pinned field per rule is fixed by the wave context and by the L1's round-28
#       change: A2-01 earlyoom.scope_complete, A2-02 earlyoom.state, A2-03
#       earlyoom.process_group_lines, A2-04 earlyoom.dryrun_send_lines, A2-05
#       earlyoom.scope_complete, A2-06 earlyoom.earlier_invocation_send_lines, A2-07
#       earlyoom.earlier_invocation_send_lines with an integer value above 0, A2-08
#       earlyoom.state, A2-09 earlyoom.state, A2-10 earlyoom.scope_complete; A2-08 also needs
#       one case whose pinned earlyoom.state is not "active";
#   F3  case ids must be printable and unique, and the tool must print exactly one
#       MORI_OOM_KILLERS_SELFTEST: line, so a forged PASS line inside an id cannot pass;
#   F4  the tool's exit status is checked, and the PASS line must be the only marker line;
#   F5  the round-26 cases.json blob at <rev> must equal its blob at fc09f96c;
#   F6  the freeze commit is found with --follow, so a rename cannot hide an earlier add,
#       and a rename or a delete of the path is reported and rejected;
#   F7  the freeze commit is found with --full-history -m, so a merge cannot hide an earlier
#       add: exactly one genuine add is required, and the file's blob must be unchanged since;
#   F8  the freeze commit and the blob are printed, so the freeze hash can be compared with
#       the hash written to LOG.md before the first tool run (the counter cannot see a
#       rewritten history);
#   F11 a parse or schema error prints "a2_schema=error <reason>" and C2=unmet; the counter
#       never reports a case count of zero next to a passing self-test.
set -u

# The lane this counter measures. The default is the lane the script is committed in; the
# environment override exists so a sandbox clone can be measured with the same bytes.
LANE=${MORI_C2_LANE:-/home/vgpnk/Projects/shokunin/mori-shokunin}
TOOL=tools/mori-oom-killers.py
FROZEN=tools/fixtures/mori-oom-killers/cases.json
A2=tools/fixtures/mori-oom-killers/cases-a2.json
# The round-26 frozen case file must keep this exact blob for the whole of round 28.
FROZEN_BASE=fc09f96c8036094bef06370dbb4b436edf96e6e3
# The ten round-26 amendment-A2 rules (contract .ufo/waves/round-27/contract.md, C2 rule list).
RULES="A2-01 A2-02 A2-03 A2-04 A2-05 A2-06 A2-07 A2-08 A2-09 A2-10"
MIN_CASES=20
MIN_CASES_PER_RULE=2
FROZEN_CASES=32

[ $# -eq 1 ] || { echo "usage: count-c2.sh <rev>"; exit 2; }
command -v git >/dev/null 2>&1 || { echo "git_missing"; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "python3_missing"; exit 2; }

R=$(git -C "$LANE" rev-parse --verify -q "$1^{commit}") || { echo "bad_rev"; exit 2; }
git -C "$LANE" cat-file -e "$R:$TOOL" 2>/dev/null || { echo "tool_absent"; exit 2; }
git -C "$LANE" cat-file -e "$R:$FROZEN" 2>/dev/null || { echo "frozen_absent"; exit 2; }
git -C "$LANE" rev-parse --verify -q "$FROZEN_BASE^{commit}" >/dev/null || { echo "base_rev_absent"; exit 2; }
git -C "$LANE" cat-file -e "$FROZEN_BASE:$FROZEN" 2>/dev/null || { echo "base_frozen_absent"; exit 2; }

T=$(mktemp -d) || { echo "mktemp_failed"; exit 2; }
trap 'rm -rf "$T"' EXIT

# ---------------------------------------------------------------- extract committed bytes
have_a2=0
git -C "$LANE" cat-file -e "$R:$A2" 2>/dev/null && have_a2=1
extract() {
  # ${1%/*} instead of dirname(1) so a minimal PATH cannot break the extract
  mkdir -p "$T/${1%/*}" || return 1
  git -C "$LANE" show "$R:$1" > "$T/$1" || return 1
}
extract "$TOOL" || { echo "extract_failed"; exit 2; }
extract "$FROZEN" || { echo "extract_failed"; exit 2; }
[ "$have_a2" -eq 1 ] && { extract "$A2" || { echo "extract_failed"; exit 2; }; }

# ---------------------------------------------------------------- checks that need no case file
echo "rev=$R"
tool_blob=$(git -C "$LANE" rev-parse "$R:$TOOL")
frozen_blob=$(git -C "$LANE" rev-parse "$R:$FROZEN")
base_frozen_blob=$(git -C "$LANE" rev-parse "$FROZEN_BASE:$FROZEN")
a2_blob=""
[ "$have_a2" -eq 1 ] && a2_blob=$(git -C "$LANE" rev-parse "$R:$A2")
echo "tool_blob=$tool_blob"
if [ "$frozen_blob" = "$base_frozen_blob" ]; then
  frozen_blob_state=match
else
  frozen_blob_state=mismatch
fi
echo "frozen_blob=$frozen_blob_state"

# ---------------------------------------------------------------- self-test helper
# Runs the extracted tool on one extracted case file. Requires exit status 0 and exactly one
# marker line, which must read "MORI_OOM_KILLERS_SELFTEST: PASS n/n" for the case count n.
selftest() {
  # $1 = case file relative path, $2 = expected case count
  local rel="$1" want="$2"
  local tag out err rc=0 markers=0 line=""
  tag=$(printf '%s' "$1" | tr / _)
  out="$T/$tag.out"
  err="$T/$tag.err"
  ( cd "$T" && python3 -I -B "$TOOL" --selftest --cases "$rel" >"$out" 2>"$err" ) || rc=$?
  markers=$(cat "$out" "$err" | grep -c '^MORI_OOM_KILLERS_SELFTEST: ')
  if [ "$rc" -ne 0 ]; then
    echo "FAIL(exit=$rc)"
    return
  fi
  if [ "$markers" -ne 1 ]; then
    echo "FAIL(markers=$markers)"
    return
  fi
  line=$(cat "$out" "$err" | grep '^MORI_OOM_KILLERS_SELFTEST: ')
  if [ "$line" = "MORI_OOM_KILLERS_SELFTEST: PASS $want/$want" ]; then
    echo "PASS $want/$want"
  else
    echo "FAIL(line=$line)"
  fi
}

frozen_selftest=$(selftest "$FROZEN" "$FROZEN_CASES")
echo "frozen32_selftest=$frozen_selftest"

# ---------------------------------------------------------------- freeze commit and blob history
# --follow keeps a renamed file's earlier add visible; --full-history -m walks every parent of
# a merge, so a merge cannot hide an earlier add. With -m a merge also shows the file as
# "A" against a parent that does not carry it, so a candidate add counts as genuine only when
# no parent of it already has the file. The file's blob must be unchanged since that add.
freeze_out="$T/freeze.txt"
python3 -I -B - "$LANE" "$R" "$A2" "$a2_blob" >"$freeze_out" 2>"$T/freeze.err" <<'PY'
import subprocess, sys

lane, rev, path, tip_blob = sys.argv[1:5]
GIT = ["git", "-C", lane, "-c", "core.quotePath=false"]


def git(*args, ok=(0,)):
    proc = subprocess.run(GIT + list(args), capture_output=True)
    if proc.returncode not in ok:
        return None
    return proc.stdout.decode("utf-8", "replace")


def log(args):
    out = git("log", *args)
    return [] if out is None else out.split("\n")


def blob_at(commit, name):
    out = git("rev-parse", "-q", "--verify", "%s:%s" % (commit, name), ok=(0, 128))
    if out is None:
        return None
    out = out.strip()
    return out or None


def parents(commit):
    out = git("rev-list", "--parents", "-n", "1", commit)
    if out is None:
        return []
    return out.split()[1:]


# Parse "git log --format=%H --name-status" into (commit, status, path) triples.
def history(extra):
    raw = log(["--full-history", "-m", "--follow", "--format=%H", "--name-status"] + extra + [rev, "--", path])
    triples = []
    commit = None
    for line in raw:
        if not line:
            continue
        if len(line) == 40 and all(c in "0123456789abcdef" for c in line):
            commit = line
            continue
        parts = line.split("\t")
        status = parts[0]
        if status[:1] in ("A", "M", "D", "R", "C", "T"):
            if status.startswith("R") or status.startswith("C"):
                name = parts[2] if len(parts) > 2 else path
            else:
                name = parts[1] if len(parts) > 1 else path
            triples.append((commit, status, name))
    return triples


all_entries = history([])
add_entries = history(["--diff-filter=A"])

# With -m a merge contributes one diff per parent, so the same (commit, path) can appear
# several times; deduplicate before counting adds.
add_entries = sorted(set(add_entries))

# A candidate add is genuine when no parent of the commit already carries the file under the
# same name; a merge that only differs from one parent is not an add of its own.
genuine = []
for commit, status, name in add_entries:
    if commit is None:
        continue
    if any(blob_at(par, name) for par in parents(commit)):
        continue
    genuine.append((commit, name))

renames = [t for t in all_entries if t[1].startswith("R")]
deletes = [t for t in all_entries if t[1].startswith("D")]
edits = [t for t in all_entries if t[1].startswith("M")]

# The blob the file has had at every commit that touched it: the file must be unchanged since
# the freeze, so exactly one blob may appear.
blobs = set()
for commit, status, name in all_entries:
    if name != path:
        continue
    value = blob_at(commit, name)
    if value:
        blobs.add(value)

freeze_commit = genuine[0][0] if len(genuine) == 1 else ""
freeze_path = genuine[0][1] if len(genuine) == 1 else ""
freeze_blob = blob_at(freeze_commit, freeze_path) if freeze_commit else ""

changed = 1
if freeze_commit and freeze_blob and tip_blob and freeze_blob == tip_blob and len(blobs) == 1:
    changed = 0

print("freeze_commit=%s" % (freeze_commit or "none"))
print("freeze_path=%s" % (freeze_path or "none"))
print("freeze_adds=%d" % len(genuine))
print("freeze_adds_raw=%d" % len(add_entries))
print("freeze_renames=%d" % len(renames))
print("freeze_deletes=%d" % len(deletes))
print("freeze_edits=%d" % len(edits))
print("freeze_blob_versions=%d" % len(blobs))
print("cases_changed_since_freeze=%d" % changed)
PY
cat "$freeze_out"
freeze_commit=$(grep '^freeze_commit=' "$freeze_out" | cut -d= -f2)
n_adds=$(grep '^freeze_adds=' "$freeze_out" | cut -d= -f2)
n_renames=$(grep '^freeze_renames=' "$freeze_out" | cut -d= -f2)
n_deletes=$(grep '^freeze_deletes=' "$freeze_out" | cut -d= -f2)
changed=$(grep '^cases_changed_since_freeze=' "$freeze_out" | cut -d= -f2)
if [ -n "$freeze_commit" ] && [ "$freeze_commit" != "none" ]; then
  echo "tool_blob_at_freeze=$(git -C "$LANE" rev-parse -q --verify "$freeze_commit:$TOOL" 2>/dev/null || echo none)"
fi

# ---------------------------------------------------------------- the a2 case file
if [ "$have_a2" -ne 1 ]; then
  echo "a2_schema=absent"
  echo "a2_cases=0"
  echo "a2_selftest=absent"
  echo "C2=unmet"
  exit 1
fi

VAL="$T/a2-validation.txt"
python3 -I -B - "$T/$A2" >"$VAL" 2>"$T/a2-validation.err" <<'PY'
import json, sys

RULES = ["A2-%02d" % i for i in range(1, 11)]
# The field each rule decides. The wave context fixes this list; the L1's round-28 change
# replaced the A2-07 pair (actions.sigterm / actions.sigkill) with the field that decides
# A2-07: earlyoom.earlier_invocation_send_lines, whose pinned value must be an integer above 0.
REQ = {
    "A2-01": ("earlyoom.scope_complete",),
    "A2-02": ("earlyoom.state",),
    "A2-03": ("earlyoom.process_group_lines",),
    "A2-04": ("earlyoom.dryrun_send_lines",),
    "A2-05": ("earlyoom.scope_complete",),
    "A2-06": ("earlyoom.earlier_invocation_send_lines",),
    "A2-07": ("earlyoom.earlier_invocation_send_lines",),
    "A2-08": ("earlyoom.state",),
    "A2-09": ("earlyoom.state",),
    "A2-10": ("earlyoom.scope_complete",),
}


def out(key, value):
    sys.stdout.write("%s\t%s\n" % (key, value))


path = sys.argv[1]
try:
    with open(path, encoding="utf-8") as handle:
        raw = handle.read()
except OSError as exc:
    out("schema", "error unreadable: %s" % (exc.strerror or exc,))
    sys.exit(0)
try:
    data = json.loads(raw)
except ValueError as exc:
    out("schema", "error json: %s" % (exc,))
    sys.exit(0)
if not isinstance(data, dict):
    out("schema", "error top level is not an object")
    sys.exit(0)
cases = data.get("cases")
if not isinstance(cases, list):
    out("schema", "error cases is not a list")
    sys.exit(0)
out("cases_raw", len(cases))

problem = None


def fail(reason):
    global problem
    if problem is None:
        problem = reason


seen = set()
for index, case in enumerate(cases):
    if not isinstance(case, dict):
        fail("case %d is not an object" % index)
        continue
    cid = case.get("id")
    if not isinstance(cid, str) or not cid or not cid.isprintable():
        fail("case %d id is not a printable non-empty string" % index)
        continue
    if cid in seen:
        fail("duplicate id %r" % cid)
    seen.add(cid)
    rule = case.get("rule")
    if not isinstance(rule, str) or rule not in RULES:
        fail("case %r rule %r is not exactly one listed rule id" % (cid, rule))
        continue
    inputs = case.get("inputs")
    if not isinstance(inputs, dict):
        fail("case %r inputs is not an object" % cid)
        continue
    why = case.get("why")
    if why is not None and not isinstance(why, str):
        fail("case %r why is not a string" % cid)
        continue
    expect = case.get("expect")
    if not isinstance(expect, dict):
        fail("case %r expect is not an object" % cid)
        continue
    verdict = expect.get("verdict")
    if not isinstance(verdict, str):
        fail("case %r expect.verdict is missing or not a string" % cid)
        continue
    code = expect.get("exit")
    if isinstance(code, bool) or not isinstance(code, int):
        fail("case %r expect.exit is missing or not an integer" % cid)
        continue
    fields = expect.get("fields")
    if fields is not None and not isinstance(fields, dict):
        fail("case %r expect.fields is not an object" % cid)
        continue

if problem is not None:
    out("schema", "error " + problem)
    sys.exit(0)

per = {}
for rule in RULES:
    per[rule] = {"n": 0, "inputs": set(), "field": 0, "nonactive": 0}
for case in cases:
    rule = case["rule"]
    entry = per[rule]
    entry["n"] += 1
    entry["inputs"].add(json.dumps(case["inputs"], sort_keys=True, separators=(",", ":")))
    fields = case["expect"].get("fields")
    if isinstance(fields, dict):
        pinned = False
        for name in REQ[rule]:
            if name not in fields:
                continue
            value = fields[name]
            if rule == "A2-07":
                # A2-07 is decided by earlier-invocation send lines: the pinned value must be
                # an integer above 0 (a boolean is not an integer here).
                if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                    continue
            pinned = True
            break
        if pinned:
            entry["field"] += 1
        if rule == "A2-08" and "earlyoom.state" in fields and fields["earlyoom.state"] != "active":
            entry["nonactive"] += 1

out("rules_covered", sum(1 for rule in RULES if per[rule]["n"] > 0))
out("distinct_inputs", len({json.dumps(c["inputs"], sort_keys=True, separators=(",", ":"))
                             for c in cases}))
for rule in RULES:
    entry = per[rule]
    out("rule_" + rule + "_cases", entry["n"])
    out("rule_" + rule + "_distinct", len(entry["inputs"]))
    out("rule_" + rule + "_field", entry["field"])
    out("rule_" + rule + "_nonactive", entry["nonactive"])
out("schema", "ok")
PY

schema=""
cases_raw=""
covered=""
distinct_total=""
declare -A rule_cases=() rule_distinct=() rule_field=() rule_nonactive=()
while IFS=$'\t' read -r key value; do
  case "$key" in
    schema) schema="$value" ;;
    cases_raw) cases_raw="$value" ;;
    rules_covered) covered="$value" ;;
    distinct_inputs) distinct_total="$value" ;;
    rule_*_cases) rule_cases["${key%_cases}"]="$value" ;;
    rule_*_distinct) rule_distinct["${key%_distinct}"]="$value" ;;
    rule_*_field) rule_field["${key%_field}"]="$value" ;;
    rule_*_nonactive) rule_nonactive["${key%_nonactive}"]="$value" ;;
  esac
done <"$VAL"

if [ -z "$schema" ]; then
  echo "a2_schema=error validator produced no result"
  echo "C2=unmet"
  exit 1
fi
if [ "$schema" != "ok" ]; then
  echo "a2_schema=$schema"
  echo "C2=unmet"
  exit 1
fi
echo "a2_schema=ok"
echo "a2_cases=$cases_raw"
echo "a2_ids=unique"
echo "a2_distinct_inputs=$distinct_total"
echo "a2_rules_covered=${covered:-0}/10"
rule_fail=""
for rule in $RULES; do
  n=${rule_cases["rule_$rule"]:-0}
  distinct=${rule_distinct["rule_$rule"]:-0}
  field=${rule_field["rule_$rule"]:-0}
  nonactive=${rule_nonactive["rule_$rule"]:-0}
  echo "a2_$rule=cases=$n distinct=$distinct field=$field nonactive=$nonactive"
  [ "$n" -ge "$MIN_CASES_PER_RULE" ] || rule_fail="$rule_fail $rule(cases<$MIN_CASES_PER_RULE)"
  [ "$distinct" -ge 2 ] || rule_fail="$rule_fail $rule(distinct_inputs<2)"
  [ "$field" -ge 1 ] || rule_fail="$rule_fail $rule(no_required_field_pin)"
  if [ "$rule" = "A2-08" ] && [ "$nonactive" -lt 1 ]; then
    rule_fail="$rule_fail A2-08(state_pinned_active_only)"
  fi
done
if [ -n "$rule_fail" ]; then
  echo "a2_rule_checks=fail:$rule_fail"
else
  echo "a2_rule_checks=ok"
fi

a2_selftest=$(selftest "$A2" "$cases_raw")
echo "a2_selftest=$a2_selftest"

met=1
[ "$frozen_blob_state" = "match" ] || met=0
[ "$frozen_selftest" = "PASS $FROZEN_CASES/$FROZEN_CASES" ] || met=0
[ "$cases_raw" -ge "$MIN_CASES" ] || met=0
[ "$covered" = "10" ] || met=0
[ -z "$rule_fail" ] || met=0
[ "$a2_selftest" = "PASS $cases_raw/$cases_raw" ] || met=0
[ "$n_adds" -eq 1 ] || met=0
[ "$n_renames" -eq 0 ] || met=0
[ "$n_deletes" -eq 0 ] || met=0
[ "$changed" -eq 0 ] || met=0

if [ "$met" -eq 1 ]; then
  echo "C2=met"
  exit 0
fi
echo "C2=unmet"
exit 1
```
