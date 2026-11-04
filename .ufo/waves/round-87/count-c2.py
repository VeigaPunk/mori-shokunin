#!/usr/bin/env python3
"""mori round-87 C2 counter (calibration): a legacy receipt is superseded by a replaying successor.

Frozen predicate P-C2 (`.ufo/waves/round-87/contract.md` — this file, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-87/count-c2.py R` prints
  `C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4
  matched=6 defeated=1 superseded=2 legacy=1 unexpected=0` and exits 0, where the seven
  population receipts all exist at R, every `# counter-sha256:` binding matches its named path's
  bytes at the receipt's own `# rev:`, both `# replay: clone` receipts reproduce their bodies in a
  `--shared` clone checked out at that rev, the one reject receipt still reports a problem, and a
  legacy receipt (no `# replay:` line) counts `superseded` only when a present, problem-free
  successor names it in `# supersedes:`.

`# replay: legacy` receipts are header-bound only and are counted `legacy` unless superseded; the
r85 worktree receipt `after-r85.txt` stays `legacy` because its body is a live-observation run.

Round 89 (P-C1 of `.ufo/waves/round-89/contract.md`; repair 2 at integration): a binding is the
entering token rule minus the positions that provably do not execute the bound path — a shell
comment (POSIX word-start rule), a redirection target, an echo/printf/:/true/false operand, a
CPython `-W`/`-X` value, anything after `-c`/`-m`, anything after the script operand. Path
identity by `normpath`/relative `realpath` (`./tools/x.py` is `tools/x.py`); an absolute token
never binds; quoted command strings (`sh -c '…'`) are searched recursively. Everything else
binds as it did on entry, so this is not execution proof.

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] | count-c2.py --selftest
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`, `git clone --shared`; files only under
--scratch.
"""
import argparse
import hashlib
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

SUBJECT = ".ufo/waves/round-86/count-c2.py"
SUBJECT_ARMS = 13
SUBJECT_LABELS = ("parse_replay", "no_replay_required", "no_replay_reason", "duplicate_replay",
                 "missing_replay", "export_lists_token", "export_needs_repo", "target_arms",
                 "population_shape", "target_line", "marker_literal", "summary_required",
                 "binding_required")

POPULATION = (
    (".ufo/waves/round-85/evidence/after-r85.txt", "met", "legacy", "C1=met"),
    (".ufo/waves/round-85/evidence/record-sweep-r85.txt", "met", "legacy", "RECORD_SWEEP"),
    (".ufo/waves/round-85/evidence/claim-sweep-r85.txt", "met", "legacy", "CLAIM_SWEEP"),
    (".ufo/waves/round-86/evidence/after-c1-r86.txt", "met", "required", "C1=met"),
    (".ufo/waves/round-86/evidence/replay-defeat-r86.txt", "reject", "required", "C1=met"),
    (".ufo/waves/round-87/evidence/record-sweep-r87.txt", "met", "clone", "RECORD_SWEEP"),
    (".ufo/waves/round-87/evidence/claim-sweep-r87.txt", "met", "clone", "CLAIM_SWEEP"),
)

TARGET = ("receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 "
          "matched=6 defeated=1 superseded=2 legacy=1 unexpected=0")
TARGET_LINE = "C2=met " + TARGET

REPLAY = re.compile(r"^#\s*replay:\s*(required|none|clone)\s*$")
NORE = re.compile(r"^#\s*no-replay:\s*(\S.*)$")
CMD = re.compile(r"^#\s*cmd:\s*(\S.*)$")
REV = re.compile(r"^#\s*rev:\s*([0-9a-f]{40})\s*$")
LIMITS = re.compile(r"^#\s*limits:\s*(\S.*)$")
SHA = re.compile(r"^#\s*counter-sha256:\s*([0-9a-f]{64})\s+(\S+)\s*$")
SUPERSEDES = re.compile(r"^#\s*supersedes:\s*(\S+)\s*$")
SEP = re.compile(r"^#\s*---\s*$")
ARMS = re.compile(r"C2_COUNTER_SELFTEST pass=(\d+) fail=(\d+)")
PATHISH = re.compile(r"^[A-Za-z0-9_.][A-Za-z0-9_./-]*$")


def run(cmd, cwd=None, env=None, timeout=900):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def header_and_body(text):
    """(header lines, body) split at the first `# ---`; body keeps no trailing newline."""
    lines = (text or "").splitlines()
    cut = None
    for number, line in enumerate(lines):
        if SEP.match(line):
            cut = number
            break
    if cut is None:
        return lines, ""
    return lines[:cut], "\n".join(lines[cut + 1:]).rstrip("\n")


def header_fields(lines):
    fields = {"cmd": None, "rev": None, "replay": None, "no_replay": None,
              "limits": None, "supersedes": None, "bindings": []}
    problems = []
    for line in lines:
        m = CMD.match(line)
        if m:
            if fields["cmd"] is not None:
                problems.append("duplicate-cmd")
            fields["cmd"] = m.group(1).strip()
            continue
        m = REV.match(line)
        if m:
            if fields["rev"] is not None:
                problems.append("duplicate-rev")
            fields["rev"] = m.group(1)
            continue
        m = LIMITS.match(line)
        if m:
            if fields["limits"] is not None:
                problems.append("duplicate-limits")
            fields["limits"] = m.group(1).strip()
            continue
        m = SUPERSEDES.match(line)
        if m:
            if fields["supersedes"] is not None:
                problems.append("duplicate-supersedes")
            fields["supersedes"] = m.group(1)
            continue
        m = SHA.match(line)
        if m:
            fields["bindings"].append((m.group(1), m.group(2)))
            continue
        m = REPLAY.match(line)
        if m:
            if fields["replay"] is not None:
                problems.append("duplicate-replay")
            fields["replay"] = m.group(1)
            continue
        m = NORE.match(line)
        if m:
            fields["no_replay"] = m.group(1).strip()
    if fields["replay"] == "none" and (fields["no_replay"] is None
                                      or len(fields["no_replay"].split()) < 3):
        problems.append("missing-no-replay")
    if fields["replay"] == "none":
        fields["replay"] = None
    return fields, problems


def declared_replay_problem(declared_mode, fields):
    """A population row declared required/clone must carry its own `# replay:` line."""
    if declared_mode in ("required", "clone") and fields["replay"] is None:
        return "missing-replay"
    return None


REDIRECTS = frozenset(("<", ">", ">>", "<<", "<<<", ">&", "<&", "&>", "&>>", ">|", "<>"))
CONTROL = frozenset(";&|()")
ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")
PYTHON = re.compile(r"python(\d+(\.\d+)*)?$")
PY_FLAGS = frozenset("bBdEiIOPqsSuvRx")        # CPython short options without a value
DATA_HEADS = frozenset(("echo", "printf", ":", "true", "false"))   # never execute an operand
WRAPPERS = {"exec": ("-a",), "command": (), "nohup": (), "time": (), "stdbuf": (),
            "setsid": (), "nice": ("-n", "--adjustment"), "ionice": ("-c", "-n", "-p", "-P"),
            "timeout": ("-s", "-k", "--signal", "--kill-after"), "env": ("-u", "--unset")}
DEPTH = 3


def entering_binds(cmd, path):
    """The entering (round-88) rule: `path` is a whitespace token of `cmd`, quotes stripped."""
    return path in set(token.strip(";'\"") for token in re.split(r"\s+", cmd or ""))


def strip_comments(cmd):
    """`cmd` with POSIX comments removed (S611): an unquoted, unescaped `#` that starts a word
    begins a comment running to the end of its line; a `#` inside a word belongs to the word.
    Unquoted newlines become `;`; a backslash-newline is removed."""
    out, quote, escaped, word, skipping = [], None, False, False, False
    for ch in cmd:
        if skipping:
            if ch != "\n":
                continue
            skipping = False
        if escaped:
            escaped = False
            if ch == "\n":
                out.pop()
                continue
            out.append(ch)
            word = True
        elif ch == "\\" and quote != "'":
            escaped = True
            out.append(ch)
        elif quote:
            quote = None if ch == quote else quote
            out.append(ch)
        elif ch in "'\"":
            quote = ch
            out.append(ch)
            word = True
        elif ch == "#" and not word:
            skipping = True
        else:
            out.append(";" if ch == "\n" else ch)
            word = not (ch.isspace() or ch in ";&|()<>")
    return "".join(out)


def shell_tokens(cmd):
    """Shell words and operators of a comment-free command; None when it does not tokenize."""
    lexer = shlex.shlex(cmd, posix=True, punctuation_chars=";&|()<>")
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        return list(lexer)
    except ValueError:
        return None


def invocations(tokens):
    """Simple commands as (words, redirect_targets); split on control operators."""
    result, words, targets, target = [], [], [], False
    for token in tokens:
        if target:
            targets.append(token)
            target = False
        elif token in REDIRECTS:
            target = True
        elif set(token) <= CONTROL:
            result.append((words, targets))
            words, targets = [], []
        else:
            words.append(token)
    result.append((words, targets))
    return [(w, t) for w, t in result if w or t]


def head_index(words):
    """Index of the command word behind assignments and exec/env/nice/timeout-style wrappers;
    None when a wrapper's form is not understood (then nothing is excluded)."""
    i = 0
    while i < len(words):
        word, base = words[i], os.path.basename(words[i])
        if ASSIGNMENT.match(word):
            i += 1
        elif base in WRAPPERS:
            i += 1
            while i < len(words) and (words[i].startswith("-") or
                                      (base == "env" and ASSIGNMENT.match(words[i]))):
                option = words[i]
                if base == "env" and ((not option.startswith("--") and set(option[1:]) & {"C", "S"})
                                      or option.split("=")[0] in ("--chdir", "--split-string")):
                    return None
                i += 2 if option in WRAPPERS[base] else 1
            if base == "timeout":
                i += 1                      # the duration operand
        else:
            return i
    return None


def python_excluded(words, h):
    """Word indices a CPython invocation does not execute as its script: option values of
    `-W`/`-X`, the `-c`/`-m` value and every later word, and every word after the script
    operand (S610: "all consecutive arguments will end up in sys.argv"). None when an option
    is not understood."""
    excluded, i = set(), h + 1
    while i < len(words):
        arg = words[i]
        if arg == "--":
            return excluded | set(range(i + 2, len(words)))
        if arg == "-":
            return excluded | set(range(i + 1, len(words)))
        if arg == "--check-hash-based-pycs":
            excluded.add(i + 1)
            i += 2
            continue
        if arg.startswith("--"):
            return None
        if not arg.startswith("-"):
            return excluded | set(range(i + 1, len(words)))
        for j, flag in enumerate(arg[1:], 1):
            if flag in "cm":
                return excluded | set(range(i + 1, len(words)))
            if flag in "WX":
                if j == len(arg) - 1:
                    excluded.add(i + 1)
                    i += 1
                break
            if flag not in PY_FLAGS:
                return None
        i += 1
    return excluded


def excluded_words(words):
    """Word indices provably not executed: operands of echo/printf/:/true/false and the
    non-script words of a CPython invocation."""
    h = head_index(words)
    if h is None:
        return set()
    base = os.path.basename(words[h])
    if base in DATA_HEADS:
        return set(range(h + 1, len(words)))
    if PYTHON.match(base):
        return python_excluded(words, h) or set()
    return set()


def same_path(token, path, repo):
    """True when the relative `token` and the repo-relative `path` name the same file; an
    absolute token never binds (it can name a file outside the replay tree)."""
    if not token or os.path.isabs(token):
        return False
    if os.path.normpath(token) == os.path.normpath(path):
        return True
    if repo:
        return (os.path.realpath(os.path.join(repo, token))
                == os.path.realpath(os.path.join(repo, path)))
    return False


def binds(cmd, path, repo=None, depth=0):
    """True when `path` occurs in `cmd` outside every position that provably does not execute
    it: comments, redirection targets, echo/printf/:/true/false operands and CPython's
    non-script words. A word containing whitespace (a quoted command string, e.g. `sh -c`)
    is searched recursively. When the command does not tokenize, or nesting exceeds DEPTH,
    the entering rule decides — so every refusal beyond the entering rule is an exclusion."""
    tokens = shell_tokens(strip_comments(cmd)) if depth <= DEPTH else None
    if tokens is None:
        return entering_binds(cmd, path)
    for words, _targets in invocations(tokens):
        excluded = excluded_words(words)
        for k, word in enumerate(words):
            if k in excluded:
                continue
            if same_path(word, path, repo):
                return True
            if any(c.isspace() for c in word) and binds(word, path, repo, depth + 1):
                return True
    return False


def binding_problems(cmd, bindings, replayed, repo=None):
    """Every `# counter-sha256:` path must occur in the command outside the positions that
    provably do not execute it (`binds`).

    Round 89 (repair 2): the rule only subtracts from the entering token rule. A bound path
    named only in a shell comment, as a redirection target, as an echo/printf operand, as a
    `-W`/`-X` value, after `python -c`/`-m`, or after another script operand does not bind;
    `./x` and `x` are one path; an absolute token never binds. It is not execution proof:
    control flow (`||`, `exit`, `false &&`), functions and fake interpreters stay as open as
    under the entering rule.
    """
    if not replayed:
        return []
    return ["cmd-binding" for _sha, path in bindings if not binds(cmd or "", path, repo)]


def absent_supersede_targets(superseders, known):
    """(name, target) pairs whose `# supersedes:` names a receipt outside the population."""
    return [(name, target) for name, target in superseders if target not in known]


def supersede_verdict(legacy_name, clean_names, superseders):
    """True when a present, problem-free successor names `legacy_name`."""
    return any(name in clean_names and target == legacy_name
               for name, target in superseders)


def supersede_counts(legacy_rows, clean_names, superseders):
    """(superseded, legacy) over (name, clean) rows; a failed successor supersedes nothing."""
    superseded = legacy = 0
    for name, clean in legacy_rows:
        if clean and supersede_verdict(name, clean_names, superseders):
            superseded += 1
        else:
            legacy += 1
    return superseded, legacy


def export_rev(repo, rev, cmd, dest):
    """Write every repo-relative path named in `cmd` at `rev` into `dest`."""
    written = []
    for token in re.split(r"\s+", cmd):
        token = token.strip(";'\"")
        if not token or token.startswith("-") or "/" not in token or not PATHISH.match(token):
            continue
        probe = run(["git", "-C", repo, "cat-file", "-e", "%s:%s" % (rev, token)])
        if probe.returncode != 0:
            continue
        blob = run(["git", "-C", repo, "show", "%s:%s" % (rev, token)])
        if blob.returncode != 0:
            continue
        target = os.path.join(dest, token)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(blob.stdout)
        written.append(token)
    return written


def replay_body(repo, rev, cmd, scratch, mode="required"):
    """Run `cmd` at `rev`; return (rc, stdout, exported count).

    `required` exports the pathish tokens named in cmd into a scratch tree; `clone` gives the
    command a real `--shared` clone checked out at `rev` (the sweeps resolve git history).
    """
    work = tempfile.mkdtemp(dir=scratch, prefix="replay-")
    env = dict(os.environ)
    env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
               PYTHONDONTWRITEBYTECODE="1")
    exported = 0
    try:
        if mode == "clone":
            target = os.path.join(work, "repo")
            cl = run(["git", "clone", "--shared", "-q", repo, target], env=env)
            if cl.returncode != 0:
                return 125, "", 0
            co = run(["git", "-C", target, "checkout", "-q", rev], env=env)
            if co.returncode != 0:
                return 126, "", 0
            exported = 1
            cwd = target
        else:
            exported = len(export_rev(repo, rev, cmd, work))
            cwd = work
        p = run(["bash", "-c", cmd], cwd=cwd, env=env)
    except subprocess.TimeoutExpired:
        return 124, "", exported
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return p.returncode, (p.stdout or ""), exported


def sha256_at(repo, rev, path):
    """sha256 of one repo-relative blob at `rev`, or None."""
    q = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])
    if q.returncode != 0:
        return None
    return hashlib.sha256(q.stdout.encode("utf-8")).hexdigest()


def ancestor(repo, rev, tip):
    if rev == tip:
        return True
    return run(["git", "-C", repo, "merge-base", "--is-ancestor", rev, tip]).returncode == 0


def grade_population(loader, repo, rev, scratch, population=POPULATION):
    """(ok, lines, counts) for the frozen population at one revision."""
    lines = []
    counts = {"receipts": 0, "absent": 0, "bindings": 0, "bound": 0, "revs": 0,
              "limits": 0, "cmd": 0, "summary": 0, "replay": 0, "matched": 0,
              "defeated": 0, "legacy": 0, "superseded": 0, "unexpected": 0}
    ok = True
    present = []
    clean_names = set()
    superseders = []
    legacy_rows = []
    for path, expect, replay_mode, token in population:
        text = loader(path)
        name = os.path.basename(path)
        if text is None:
            counts["absent"] += 1
            lines.append("RECEIPT %s absent=1 expect=%s" % (name, expect))
            if expect != "reject":
                ok = False
            continue
        present.append(name)
        counts["receipts"] += 1
        header, body = header_and_body(text)
        fields, problems = header_fields(header)
        missing_replay = declared_replay_problem(replay_mode, fields)
        if missing_replay:
            problems.append(missing_replay)
        problems.extend(binding_problems(fields["cmd"], fields["bindings"],
                                         replay_mode in ("required", "clone")
                                         or fields["replay"] is not None, repo))
        if fields["supersedes"]:
            superseders.append((name, fields["supersedes"]))
        if replay_mode != "legacy" or fields["replay"] is not None:
            counts["replay"] += 1
        if fields["cmd"]:
            counts["cmd"] += 1
        if fields["limits"] and "limit" in fields["limits"].lower() \
                and len(fields["limits"].split()) >= 3:
            counts["limits"] += 1
        if token in body:
            counts["summary"] += 1
        else:
            problems.append("summary")
        rev_ok = bool(fields["rev"]) and ancestor(repo, fields["rev"], rev)
        if rev_ok:
            counts["revs"] += 1
        else:
            problems.append("rev")
        for sha, bpath in fields["bindings"]:
            counts["bindings"] += 1
            measured = sha256_at(repo, fields["rev"] or "", bpath) if rev_ok else None
            if measured == sha:
                counts["bound"] += 1
            else:
                problems.append("sha:" + bpath)
        mode = replay_mode
        if mode == "legacy" and fields["replay"] == "required":
            mode = "required"
        if mode in ("required", "clone") and fields["replay"] is not None:
            rc, out, exported = replay_body(repo, fields["rev"] or "", fields["cmd"] or "",
                                            scratch, mode)
            if rc != 0:
                problems.append("replay-rc:%d" % rc)
            if body != out.rstrip("\n"):
                problems.append("replay-mismatch")
            lines.append("REPLAY %s mode=%s rc=%d exported=%d" % (name, mode, rc, exported))
        clean = not problems
        if clean:
            clean_names.add(name)
        if expect == "reject":
            if problems:
                counts["defeated"] += 1
            else:
                counts["unexpected"] += 1
                ok = False
        elif clean:
            counts["matched"] += 1
        else:
            counts["unexpected"] += 1
            ok = False
        if mode == "legacy":
            legacy_rows.append((name, clean))
        lines.append("RECEIPT %s expect=%s %s problems=%s"
                     % (name, expect, "met" if clean else "failed", ",".join(problems) or "-"))
    counts["superseded"], counts["legacy"] = supersede_counts(
        legacy_rows, clean_names, superseders)
    for name, target in absent_supersede_targets(superseders, set(present)):
        counts["unexpected"] += 1
        lines.append("SUPERSEDE %s target=%s absent=1" % (name, target))
        ok = False
    return ok, lines, counts


def selfcheck(scratch):
    """Detector arms over synthetic receipts and commands (no lane file is touched)."""
    cases = []
    good = ("# cmd: python3 -c \"print('body')\"\n"
            "# rev: %s\n"
            "# replay: required\n"
            "# ---\nbody\n" % ("a" * 40))
    header, body = header_and_body(good)
    fields, problems = header_fields(header)
    cases.append(("parse_replay", not problems and fields["replay"] == "required"
                  and fields["rev"] == "a" * 40 and body == "body", str(problems)))
    sup = good.replace("# replay: required\n",
                       "# replay: clone\n# supersedes: old-receipt.txt\n")
    fields, problems = header_fields(header_and_body(sup)[0])
    cases.append(("parse_supersedes",
                  not problems and fields["supersedes"] == "old-receipt.txt"
                  and fields["replay"] == "clone", str(problems)))
    dup = sup.replace("# supersedes: old-receipt.txt\n",
                      "# supersedes: old-receipt.txt\n# supersedes: other.txt\n")
    cases.append(("duplicate_supersedes",
                  "duplicate-supersedes" in header_fields(header_and_body(dup)[0])[1], "dup"))
    cases.append(("supersede_matched",
                  supersede_verdict("old.txt", {"new.txt"},
                                    [("new.txt", "old.txt")]), "match"))
    cases.append(("supersede_absent_target",
                  not supersede_verdict("old.txt", set(), [("new.txt", "old.txt")]),
                  "absent"))
    cases.append(("supersede_requires_clean",
                  supersede_counts([("old.txt", True)], set(),
                                   [("new.txt", "old.txt")]) == (0, 1),
                  "unclean successor"))
    cases.append(("supersede_counts_positive",
                  supersede_counts([("old.txt", True)], {"new.txt"},
                                   [("new.txt", "old.txt")]) == (1, 0), "clean successor"))
    cases.append(("supersede_wrong_target",
                  not supersede_verdict("old.txt", {"new.txt"},
                                        [("new.txt", "other.txt")]), "other"))
    none = good.replace("# replay: required\n", "# replay: none\n")
    cases.append(("no_replay_required",
                  "missing-no-replay" in header_fields(header_and_body(none)[0])[1], "reason"))
    none_ok = none.replace("# replay: none\n", "# replay: none\n# no-replay: live observation "
                           "cannot be replayed\n")
    fields, problems = header_fields(header_and_body(none_ok)[0])
    cases.append(("no_replay_reason", not problems and fields["no_replay"]
                  and fields["replay"] is None, str(problems)))
    missing = good.replace("# replay: required\n", "")
    cases.append(("legacy_mode_no_problem",
                  header_fields(header_and_body(missing)[0])[1] == [], "legacy"))
    cases.append(("clone_mode_parsed",
                  header_fields(header_and_body(
                      good.replace("# replay: required", "# replay: clone"))[0])[0]["replay"]
                  == "clone", "clone"))
    cases.append(("body_trailing_newline",
                  header_and_body("# ---\nbody\n\n")[1] == "body"
                  and header_and_body("# ---\nbody \n")[1] == "body ", "rstrip"))
    cases.append(("population_shape",
                  len(POPULATION) == 7
                  and sum(1 for row in POPULATION if row[2] == "legacy") == 3
                  and sum(1 for row in POPULATION if row[2] == "clone") == 2
                  and sum(1 for row in POPULATION if row[1] == "reject") == 1, "3/2/1"))
    cases.append(("target_line", TARGET_LINE == "C2=met " + TARGET
                  and "superseded=2" in TARGET and "legacy=1" in TARGET
                  and "replay=4" in TARGET, "line"))
    cases.append(("subject_arms", SUBJECT_ARMS == 13
                  and len(SUBJECT_LABELS) == 13, "13/13"))
    # --- round-88 arms: the declared-mode and cmd-binding rules and the absent-target branch ---
    missing = good.replace("# replay: required\n", "")
    fields, problems = header_fields(header_and_body(missing)[0])
    cases.append(("missing_replay_required",
                  not problems and declared_replay_problem("required", fields) == "missing-replay",
                  str(problems)))
    cases.append(("missing_replay_clone",
                  declared_replay_problem("clone", fields) == "missing-replay"
                  and declared_replay_problem("legacy", fields) is None, "clone/legacy"))
    bindings = [("a" * 64, "tools/x.py")]
    cases.append(("binding_not_in_cmd",
                  binding_problems("# cmd: printf 'x'", bindings, True) == ["cmd-binding"],
                  "vacuous cmd"))
    cases.append(("binding_in_cmd_ok",
                  binding_problems("python3 -I tools/x.py", bindings, True) == [], "named"))
    cases.append(("binding_skipped_for_legacy",
                  binding_problems("# cmd: printf 'x'", bindings, False) == [], "legacy"))
    cases.append(("absent_target_helper",
                  absent_supersede_targets([("n.txt", "gone.txt"), ("m.txt", "n.txt")],
                                           {"m.txt", "n.txt"}) == [("n.txt", "gone.txt")], "gone"))
    # --- round-89 arms: path identity, comment tokens and data-position paths ---
    cases.append(("binding_path_identity",
                  binding_problems("python3 -I ./tools/x.py", bindings, True) == [],
                  "./spelling"))
    cases.append(("binding_comment_dropped",
                  binding_problems("printf 'body' # tools/x.py", bindings, True)
                  == ["cmd-binding"], "comment token"))
    cases.append(("binding_selfprint_refused",
                  binding_problems("python3 -c \"print('body')\" tools/x.py", bindings, True)
                  == ["cmd-binding"], "path as data"))
    cases.append(("marker_literal", "supersede_verdict" in
                  open(os.path.abspath(__file__)).read(), "label"))
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
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c2-r87-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
        if not a.rev:
            print("C2_SETUP usage: count-c2.py <rev> | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else a.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print("C2_SETUP unresolvable revision " + a.rev, file=sys.stderr)
            return 2
        rev = p.stdout.strip()

        def loader(path):
            q = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])
            return q.stdout if q.returncode == 0 else None

        own = run(["python3", "-I", os.path.abspath(__file__), "--selftest",
                   "--scratch", scratch])
        own_out = (own.stdout or "") + (own.stderr or "")
        own_ok = (own.returncode == 0 and "C2_COUNTER_SELFTEST" in own_out
                  and re.search(r"C2_COUNTER_SELFTEST pass=(\d+) fail=0", own_out) is not None)

        subject = loader(SUBJECT)
        if subject is None:
            print("C2=unmet receipts=0 subject=absent rev=%s" % rev[:12])
            return 1
        missing = [label for label in SUBJECT_LABELS if label not in subject]
        if missing:
            print("C2=unmet subject=stub missing=%s rev=%s" % (",".join(missing), rev[:12]))
            return 1
        sdir = tempfile.mkdtemp(dir=scratch, prefix="subject-")
        spath = os.path.join(sdir, SUBJECT)
        os.makedirs(os.path.dirname(spath), exist_ok=True)
        open(spath, "w", encoding="utf-8").write(subject)
        srun = run(["python3", "-I", spath, "--selftest", "--scratch", scratch])
        sout = (srun.stdout or "") + (srun.stderr or "")
        arms = None
        for m in ARMS.finditer(sout):
            arms = (int(m.group(1)), int(m.group(2)))
        labels_ok = all(("PASS " + label) in sout for label in SUBJECT_LABELS)
        subject_selftest_ok = srun.returncode == 0 and arms == (SUBJECT_ARMS, 0) and labels_ok

        ok, lines, counts = grade_population(loader, repo, rev, scratch)
        for line in lines:
            print(line)
        tail = ("receipts=%d absent=%d bindings=%d bound=%d revs=%d limits=%d cmd=%d summary=%d "
                "replay=%d matched=%d defeated=%d superseded=%d legacy=%d unexpected=%d"
                % (counts["receipts"], counts["absent"], counts["bindings"], counts["bound"],
                   counts["revs"], counts["limits"], counts["cmd"], counts["summary"],
                   counts["replay"], counts["matched"], counts["defeated"],
                   counts["superseded"], counts["legacy"], counts["unexpected"]))
        if not own_ok:
            print("C2=unmet %s detector=red rev=%s" % (tail, rev[:12]))
            print(own_out.strip())
            return 1
        if not subject_selftest_ok:
            print("C2=unmet %s subject=selftest arms=%s labels=%s rev=%s"
                  % (tail, arms, labels_ok, rev[:12]))
            print((sout.strip().splitlines() or [""])[-1])
            return 1
        if not ok or tail != TARGET:
            print("C2=unmet %s detector=green rev=%s" % (tail, rev[:12]))
            return 1
        print("C2=met %s rev=%s" % (tail, rev[:12]))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
