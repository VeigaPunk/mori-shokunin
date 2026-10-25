#!/usr/bin/env python3
"""mori round-45 C1 — hardened ledger counter (frozen instrument).

A ledger is a TSV, one row per figure:

    id<TAB>value<TAB>class<TAB>command[<TAB>CONST=<reason>]

`command` is exactly ONE pipeline and it must read committed bytes: its first
stage is `git <read-verb> ...` naming `@REV@` (each `@REV@` token is replaced by
the revision under measurement). Later stages may only be passive filters, and
the whole row is executed WITHOUT a shell: tokens are split here, each stage is
one `subprocess` call, stdin of stage n is stdout of stage n-1, and every stage
must exit 0 (a rc/pipefail gate — a zero-count `grep` is rc 1 and is read as a
gate failure, never as the figure 0).

Every option is allow-listed per verb (`GIT_OPTIONS`, `FILTER_OPTIONS`): an
unlisted token beginning with `-` is rejected, so no stage can carry a writer
(`sort -o`, `sort --compress-program=`, `uniq IN OUT`), a repo redirect
(`--git-dir`, `--work-tree`, `git -c`) or a second program. `--` ends option
parsing in a stage, so a pattern may start with `-` (`git grep -n --
'--selftest'`). A non-option token may not be an absolute path, may not be a
bare 7-40 hex revision pin, and may not be a bare `#` (a comment smuggled past
the grammar is just another argument to the program); `=` is rejected there too,
except in a filter's positional, where a pattern is data (`grep -oE '^rows=[0-9]+'`).
Filters take no file operands: only `grep` takes a pattern and `tr` takes its
two SETs. The one read-only exception to the writer ban is `grep -o`; `sort -o`
and every other writer spelling stays rejected.

Admissibility (a row is rejected when any of these fails):
  * not one `git` pipeline, or the pipeline does not name `@REV@`;
  * the first stage does not itself name `@REV@`;
  * a shell metacharacter or a command substitution appears (`;`, `&`, `<`,
    `>`, `(`, `)`, `$`, backtick, CR/LF) — there is no `bash -c`, ever;
  * the text resolves the tip itself: `HEAD`, `@{...}`, a hard-coded 40-hex, a
    short 7-39 hex SHA, or `git rev-parse` (not a read verb);
  * an option off its verb's allow-list, an absolute path, a token carrying
    `=`, or a filter carrying its own file operands;
  * the asserted value is `0` while the pipeline reads through a listing verb
    (`ls-tree`, `ls-files`): absence is indistinguishable from a zero count, so
    a genuine zero must come from `show`, `cat-file -e` or `rev-list --count`;
  * the `id` repeats an earlier row's id, or the command text repeats an
    earlier row's command text (whitespace-normalised);
  * the value does not MOVE between the measured revision and `--other-rev`,
    unless the row carries `CONST=<reason>` (the reason must be non-empty).

The row set must also clear the frozen floors: 12 rows over 4 classes.
`--min-rows`/`--min-classes` are clamped UP to those floors, never honoured
below them. `CONST=` exempts one row from the movement test, never the ledger:
`moved>=1` and at most `rows-2` rows may be `CONST`. (The correction's literal
`rows-1` cap would still admit eleven annotated rows plus one mover, so the cap
here is one row tighter: at least two figures must move.)

`--witness-dir DIR`: every `*.tsv` in DIR is one vacuity witness ledger, read
from the worktree (not from `--rev`) and scored by the same engine. Each must be
REJECTED for a DECLARED vacuity class (`revision_sensitivity`, `const_cap`, a
duplicate id/command or a tip-resolving token) and must be at least as large as
the frozen floors: a witness with fewer than `--min-rows` rows or fewer than
`--min-classes` classes proves nothing and makes the run `C1=unmet`. A witness
that would score `C1=met` makes the run `C1=unmet`. Because the witness arm is
part of the frozen predicate, `--other-rev` and `--witness-dir` are both
required for `C1=met` — omitting either prints a FAIL, never a silent skip.

There is no `WORK` mode: scoring reads committed bytes only. An absent path is a
FAIL (an unreadable row), never a zero.

Usage:
  count-c1.py <rev> --other-rev REV [--witness-dir DIR] [--repo PATH]
              [--ledger PATH] [--min-rows N] [--min-classes N] [--timeout S]
  count-c1.py --selftest

Exit: 0 C1=met · 1 C1=unmet · 2 C1_SETUP (usage/unresolvable revision/git timeout).

Predicate: .ufo/waves/round-45/contract.md P-C1 and its Correction 1.
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

FLOOR_ROWS = 12
FLOOR_CLASSES = 4
CLASSES = ("registry", "evidence", "wave", "corpus", "checks")
GIT_VERBS = {"show", "grep", "ls-tree", "ls-files", "rev-list", "cat-file",
             "log", "diff"}
FILTERS = {"grep", "head", "tail", "wc", "sort", "uniq", "cut", "tr", "cat", "nl"}
LISTING_VERBS = {"ls-tree", "ls-files"}
# An option is accepted only by exact match against its stage's allow-list, and
# every option token is checked before it can reach exec: no stage may smuggle a
# writer (`sort -o`, `sort --compress-program=`, `uniq IN OUT`), a repo redirect
# (`--git-dir`, `--work-tree`, `git -c`) or a second program.
GIT_OPTIONS = {
    "show": (),
    "cat-file": ("-e", "-s", "-t", "-p"),
    "rev-list": ("--count",),
    "ls-tree": ("-r", "--name-only", "-l", "-z", "--full-tree"),
    "ls-files": ("-z",),
    "grep": ("-l", "-n", "-v", "-c", "-e", "-E", "-F", "-i", "-w"),
    "log": ("--format=%s", "--format=%H", "--format=%h", "--oneline"),
    "diff": ("--name-only",),
}
FILTER_OPTIONS = {
    # `-o` is a forbidden spelling everywhere else (`sort -o` writes); grep's
    # only-matching flag is read-only and the positional rule below guarantees
    # grep receives no path operand.
    "grep": ("-c", "-o", "-l", "-E", "-F", "-e", "-i", "-v", "-w", "-x"),
    "head": ("-n",),
    "tail": ("-n",),
    "wc": ("-l", "-w"),
    "sort": ("-r", "-n", "-u"),
    "uniq": ("-d", "-u"),
    "cut": ("-f", "-d"),
    "tr": ("-d", "-s"),
    "cat": (),
    "nl": (),
}
# Short options that take a value may be spelled attached (`-f2`, `-d:`, `-eX`).
FILTER_VALUE = {
    "grep": ("-e",), "cut": ("-d", "-f"), "head": ("-n",), "tail": ("-n",),
}
# Filters read stdin. Only `grep` (pattern) and `tr` (two SETs) take positionals;
# a filter that accepts file operands could read or write outside the pipeline.
FILTER_POS = {
    "grep": (1, 1), "head": (0, 0), "tail": (0, 0), "wc": (0, 0),
    "sort": (0, 0), "uniq": (0, 0), "cut": (0, 0), "tr": (1, 2),
    "cat": (0, 0), "nl": (0, 0),
}
BANNED_TOKENS = {"-o", "-S", "-c", "-T", "--compress-program", "--output",
                 "--exec", "--git-dir", "--work-tree", "--no-index",
                 "--path-format"}
DECLARED_PARSE = ("duplicate id", "duplicate command", "resolves the tip")
ID_RE = re.compile(r"^F\d{2,3}$")
DIGITS = re.compile(r"^[0-9]+$")
CONST_RE = re.compile(r"^CONST=(\S.*)$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
HEX7_40 = re.compile(r"^[0-9a-fA-F]{7,40}$")
TIP_RES = (
    re.compile(r"(?<![A-Za-z0-9_])HEAD(?![A-Za-z0-9_])"),
    re.compile(r"@\{"),
    re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{40}(?![0-9a-fA-F])"),
)
MAX_INTERMEDIATE = 8 << 20
MAX_VALUE_BYTES = 32


class Setup(Exception):
    pass


def repo_default():
    here = os.path.abspath(__file__)
    # .ufo/waves/round-45/count-c1.py -> <repo>; a copy at another depth still
    # resolves by walking up to the nearest checkout or gate-registry tool.
    d = os.path.dirname(here)
    while True:
        if os.path.isdir(os.path.join(d, ".git")) or os.path.isfile(
                os.path.join(d, "tools", "mori-gate-registry.py")):
            return d
        up = os.path.dirname(d)
        if up == d:
            return os.path.dirname(here)
        d = up


def child_env():
    """Environment for every git child: no inherited GIT_* redirection.

    A caller's GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE must not retarget a read,
    and host-level config must not alias a builtin into a shell command.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    return env


def git(repo, args, timeout=30, env=None):
    try:
        return subprocess.run(
            ["git", "-C", repo] + args,
            capture_output=True, text=True, timeout=timeout, check=False,
            env=env if env is not None else child_env(),
        )
    except subprocess.TimeoutExpired:
        raise Setup("git timeout: %s" % " ".join(args))


def resolve(repo, spec, env):
    if spec == "WORK":
        raise Setup("WORK is not a scoring revision: measure a committed revision")
    got = git(repo, ["rev-parse", "--verify", "--quiet", spec + "^{commit}"], env=env)
    if got.returncode != 0:
        raise Setup("cannot resolve revision %r in %s" % (spec, repo))
    sha = got.stdout.strip()
    if not SHA40.match(sha):
        raise Setup("revision %r did not resolve to a commit id" % spec)
    return sha


def read_at(repo, rev, path, env):
    """Committed bytes of `path` at `rev`, or None when the path is absent."""
    probe = git(repo, ["cat-file", "-e", "%s:%s" % (rev, path)], env=env)
    if probe.returncode != 0:
        return None
    got = git(repo, ["show", "%s:%s" % (rev, path)], env=env)
    if got.returncode != 0:
        raise Setup("git show failed for %s:%s" % (rev, path))
    return got.stdout.encode()


# --------------------------------------------------------------------------
# row grammar: one pipeline, no shell
# --------------------------------------------------------------------------

def split_stages(cmd):
    """Quote-aware split of `cmd` on unquoted `|`; no shell is ever involved.

    Quoting is honoured only to let a filter carry a pattern (r44's
    `grep -cE '^ {0,3}\\|...'`). Outside quotes and inside double quotes a
    substitution or shell operator is a hard parse error.
    """
    problems = []
    stages, stage, tok = [], [], []
    quote = None
    i, n = 0, len(cmd)
    while i < n:
        ch = cmd[i]
        if quote == "'":
            if ch == "'":
                quote = None
            else:
                tok.append(ch)
        elif quote == '"':
            if ch == '"':
                quote = None
            elif ch == "\\" and i + 1 < n and cmd[i + 1] in '"\\$`':
                i += 1
                tok.append(cmd[i])
            elif ch in "$`":
                problems.append("command substitution %r inside double quotes" % ch)
            else:
                tok.append(ch)
        elif ch in " \t":
            if tok:
                stage.append("".join(tok))
                tok = []
        elif ch == "|":
            if tok:
                stage.append("".join(tok))
                tok = []
            stages.append(stage)
            stage = []
        elif ch in ";$`<>&()\n\r":
            problems.append("shell metacharacter %r" % ch)
        elif ch == "\\":
            if i + 1 < n:
                i += 1
                tok.append(cmd[i])
        elif ch in "'\"":
            quote = ch
        else:
            tok.append(ch)
        i += 1
    if quote is not None:
        problems.append("unbalanced %s quote" % quote)
    if tok:
        stage.append("".join(tok))
    stages.append(stage)
    return stages, problems


def _option_problems(tok, allowed, prog, value_opts=()):
    if tok in allowed:
        return []
    body = tok[1:]
    if len(body) > 1 and ("-" + body[0]) in value_opts:
        return []                       # attached value: -f2, -d:, -ePATTERN
    if tok.startswith("--"):
        if tok in BANNED_TOKENS:
            return ["%s option %r is forbidden (writer/redirect option)"
                    % (prog, tok)]
        return ["%s option %r is not allowed" % (prog, tok)]
    if any("-" + ch not in allowed for ch in body):
        if any("-" + ch in BANNED_TOKENS for ch in body
               if "-" + ch not in allowed):
            return ["%s option %r is forbidden (writer/redirect option)"
                    % (prog, tok)]
        return ["%s option %r is not allowed" % (prog, tok)]
    return []


def _token_problems(tok, allow_eq=False):
    """A non-option token: no writer spelling, no redirect, no revision pin.

    `allow_eq` is set for a filter's positional (a pattern/SET is data, so
    `grep -oE '^rows=[0-9]+'` stays legal); option position and every git-stage
    positional still reject `=`.
    """
    problems = []
    if tok == "#":
        problems.append("bare '#' is a comment marker, not an argument")
    if tok.startswith("/"):
        problems.append("absolute path %r" % tok)
    if tok.startswith("~/"):
        problems.append("home-relative path %r" % tok)
    if "=" in tok and not allow_eq:
        problems.append("token %r carries '=' (option-value smuggling)" % tok)
    if HEX7_40.match(tok):
        problems.append("token %r is a revision-like hex pin, not @REV@" % tok)
    for rx in TIP_RES:
        if rx.search(tok):
            problems.append("token %r resolves the tip instead of @REV@" % tok)
            break
    return problems


def _git_stage_problems(stage):
    verb = stage[1]
    allowed = GIT_OPTIONS[verb]
    problems, after_sep = [], False
    for tok in stage[2:]:
        if after_sep:
            problems.extend(_token_problems(tok))
            continue
        if tok == "--":
            after_sep = True
            continue
        if tok.startswith("-"):
            problems.extend(_option_problems(tok, allowed, "git " + verb))
        else:
            problems.extend(_token_problems(tok))
    if verb == "diff" and "--name-only" not in stage[2:]:
        problems.append("git diff is allowed only with --name-only")
    return problems


def _stage_problems(stage, first):
    head = stage[0]
    if head == "git":
        if len(stage) < 2 or stage[1] not in GIT_VERBS:
            return ["git verb %r is not a read verb"
                    % (stage[1] if len(stage) > 1 else "")]
        problems = _git_stage_problems(stage)
        if first and not any("@REV@" in tok for tok in stage):
            problems.append("first stage does not name @REV@")
        return problems
    if first:
        return ["first stage %r is not git" % head]
    if head not in FILTERS:
        return ["pipeline stage %r is not a read filter" % head]
    allowed = FILTER_OPTIONS[head]
    value_opts = FILTER_VALUE.get(head, ())
    problems, positionals, saw_e, after_sep = [], [], False, False
    for tok in stage[1:]:
        if after_sep:
            positionals.append(tok)
            problems.extend(_token_problems(tok, allow_eq=True))
            continue
        if tok == "--":
            after_sep = True
            continue
        if tok.startswith("-") and tok != "-":
            problems.extend(_option_problems(tok, allowed, head, value_opts))
            if tok == "-e" or tok.startswith("-e"):
                saw_e = True
        else:
            positionals.append(tok)
            problems.extend(_token_problems(tok, allow_eq=True))
    lo, hi = FILTER_POS[head]
    if head == "grep" and saw_e:
        lo = 0
    if not lo <= len(positionals) <= hi:
        problems.append("%r takes %d..%d positional argument(s), got %d: a filter "
                        "with its own file operands could read or write outside the "
                        "pipeline" % (head, lo, hi, len(positionals)))
    return problems


def parse_pipeline(cmd):
    """(stages, problems): stages is a list of argv lists, or [] when rejected."""
    stages, problems = split_stages(cmd)
    if any(not st for st in stages):
        problems.append("empty pipeline stage")
    if problems:
        return [], problems
    if "@REV@" not in cmd:
        problems.append("command does not name @REV@")
    for i, st in enumerate(stages):
        problems.extend(_stage_problems(st, i == 0))
    return stages, problems


def run_pipeline(repo, rev, stages, timeout, env):
    """Execute one pipeline as argv stages. Returns (int, "") or (None, why).

    Every stage must exit 0 (pipefail): an absent path or a zero-match `grep`
    is a gate failure, never a zero figure.
    """
    deadline = time.monotonic() + timeout
    data = b""
    for i, argv in enumerate(stages):
        argv = [a.replace("@REV@", rev) for a in argv]
        left = deadline - time.monotonic()
        if left <= 0:
            raise Setup("git timeout after %ss: %s" % (timeout, " ".join(argv)))
        try:
            out = subprocess.run(
                argv, cwd=repo, env=env, input=data,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=left, check=False,
            )
        except subprocess.TimeoutExpired:
            raise Setup("git timeout after %ss: %s" % (timeout, " ".join(argv)))
        except OSError as exc:
            return None, "cannot exec %r: %s" % (argv[0], exc)
        if out.returncode != 0:
            err = out.stderr.decode("utf-8", "replace").strip()[:100]
            return None, "stage %d rc=%d %s" % (i + 1, out.returncode, err)
        data = out.stdout
        if len(data) > MAX_INTERMEDIATE:
            return None, "stage %d emitted %d bytes (cap %d)" % (
                i + 1, len(data), MAX_INTERMEDIATE)
    body = data.decode("utf-8", "replace").strip()
    if len(body) > MAX_VALUE_BYTES:
        return None, "output longer than %d bytes (%r...)" % (MAX_VALUE_BYTES, body[:16])
    if not DIGITS.match(body):
        return None, "output %r is not an integer" % body
    return int(body), ""


# --------------------------------------------------------------------------
# ledger parsing
# --------------------------------------------------------------------------

def parse_ledger(text):
    """Return (rows, problems). Row: (id, value, class, command, const, stages)."""
    rows, problems, ids, cmds = [], [], {}, {}
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = line.split("\t")
        if len(cells) not in (4, 5):
            problems.append("row %d: %d TSV cells, want 4 (id/value/class/command) "
                            "or 5 (+ CONST=<reason>)" % (n, len(cells)))
            continue
        fid, asserted, cls, cmd = [c.strip() for c in cells[:4]]
        const = None
        if len(cells) == 5:
            m = CONST_RE.match(cells[4].strip())
            if not m:
                problems.append("row %d: fifth cell is not CONST=<reason>" % n)
            else:
                const = m.group(1).strip()
        if not ID_RE.match(fid):
            problems.append("row %d: id %r is not F<digits>" % (n, fid))
        if not DIGITS.match(asserted):
            problems.append("row %d: value %r is not an integer" % (n, asserted))
        if cls not in CLASSES:
            problems.append("row %d: class %r not in %s" % (n, cls, sorted(CLASSES)))
        if not cmd:
            problems.append("row %d: empty command" % n)
            continue
        stages, cproblems = parse_pipeline(cmd)
        problems.extend("row %d: %s" % (n, p) for p in cproblems)
        if (stages and DIGITS.match(asserted) and int(asserted) == 0
                and any(st[0] == "git" and len(st) > 1 and st[1] in LISTING_VERBS
                        for st in stages)):
            problems.append("row %d: asserted 0 from a listing verb (ls-tree/"
                            "ls-files): an absent path is indistinguishable from a "
                            "zero count; take a zero from show, cat-file -e or "
                            "rev-list --count" % n)
        if False:  # MUTANT: duplicate-id check disabled
            problems.append("row %d: duplicate id %s (first at row %d)" % (n, fid, ids[fid]))
        else:
            ids[fid] = n
        key = " ".join(cmd.split())
        if key in cmds:
            problems.append("row %d: duplicate command text (first at row %d)"
                            % (n, cmds[key]))
        else:
            cmds[key] = n
        rows.append((fid, int(asserted) if DIGITS.match(asserted) else -1,
                     cls, cmd, const, stages))
    return rows, problems


# --------------------------------------------------------------------------
# scoring
# --------------------------------------------------------------------------

def check_text(repo, rev, other_rev, text, min_rows, min_classes, timeout, env):
    """Score one ledger's text. Returns (checks, fails, meta)."""
    checks, fails = [], []

    def record(name, ok, detail=""):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    rows, problems = parse_ledger(text)
    record("rows_parse", not problems,
           "; ".join(problems[:4]) or "%d rows" % len(rows))
    classes = sorted({r[2] for r in rows})
    record("row_floor", len(rows) >= min_rows,
           "rows=%d floor=%d" % (len(rows), min_rows))
    record("class_floor", len(classes) >= min_classes,
           "classes=%s floor=%d" % (",".join(classes) or "-", min_classes))

    mismatches, details, values = [], [], {}
    if not problems:
        for fid, asserted, _cls, _cmd, _const, stages in rows:
            got, why = run_pipeline(repo, rev, stages, timeout, env)
            if got is None:
                mismatches.append("%s unreadable (%s)" % (fid, why))
                details.append("%s <- %s" % (fid, why))
            else:
                values[fid] = got
                if got != asserted:
                    mismatches.append("%s asserted=%d observed=%d" % (fid, asserted, got))
                    details.append("%s asserted=%d observed=%d" % (fid, asserted, got))
    record("commands_reconcile", not mismatches,
           "; ".join(details[:4]) or "all rows match")

    const_ids = [r[0] for r in rows if r[4]]
    moved = 0
    if other_rev is None:
        record("other_rev_present", False,
               "--other-rev not supplied: revision sensitivity unmeasured")
        record("revision_sensitivity", False, "unmeasured (no --other-rev)")
    else:
        record("other_rev_present", True, other_rev)
        constant, unreadable = [], []
        if not problems:
            for fid, _asserted, _cls, _cmd, const, stages in rows:
                if const or fid not in values:
                    continue
                other, why = run_pipeline(repo, other_rev, stages, timeout, env)
                if other is None:
                    unreadable.append("%s unreadable at other-rev (%s)" % (fid, why))
                elif other == values[fid]:
                    constant.append("%s value=%d at both revisions" % (fid, values[fid]))
                else:
                    moved += 1
        ok = not problems and not constant and not unreadable
        if problems:
            detail = "unparsed rows: sensitivity not measured"
        else:
            detail = ("; ".join((constant + unreadable)[:4]) or
                      "%d rows move, %d CONST" % (moved, len(const_ids)))
        record("revision_sensitivity", ok, detail)

    cap = max(0, len(rows) - 2)
    record("revision_moves", moved >= 1,
           "moved=%d floor=1%s" % (moved, " (unparsed)" if problems else ""))
    record("const_cap", bool(rows) and len(const_ids) <= cap,
           "const=%d cap=%d rows=%d (at least two rows must move; Correction 1 "
           "literal cap rows-1=%d)" % (len(const_ids), cap, len(rows),
                                       max(0, len(rows) - 1)))

    meta = {"rows": len(rows), "classes": classes,
            "mismatches": None if problems else len(mismatches),
            "moved": moved, "const": len(const_ids), "problems": problems[:6]}
    return checks, fails, meta


def _ledger_shape(text):
    """Raw size of a candidate witness: rows with >=4 cells, declared classes."""
    nrows, classes = 0, set()
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = line.split("\t")
        if len(cells) < 4:
            continue
        nrows += 1
        cls = cells[2].strip()
        if cls in CLASSES:
            classes.add(cls)
    return nrows, classes


def _declared_vacuity(fails, problems):
    """A witness must fail for a DECLARED vacuity class, not for being junk."""
    if any(k in p for p in problems for k in DECLARED_PARSE):
        return True
    if problems:
        return False
    return "revision_sensitivity" in fails or "const_cap" in fails


def check_witnesses(repo, rev, other_rev, witness_dir, min_rows, min_classes,
                    timeout, env):
    """Every `*.tsv` must be rejected by a declared vacuity class at full size.

    A witness below the frozen row/class floors proves nothing (a three-line
    junk file is `rejected` by any measure), so it makes the run `C1=unmet`
    instead of counting toward `witnesses=n/n`. Returns (checks, fails, meta).
    """
    checks, fails, details = [], [], []
    if not witness_dir:
        checks.append(("witness_dir_present", False, "--witness-dir not supplied"))
        fails.append("witness_dir_present")
        return checks, fails, details
    if not os.path.isdir(witness_dir):
        checks.append(("witness_dir_present", False,
                       "not a directory: %s" % witness_dir))
        fails.append("witness_dir_present")
        return checks, fails, details
    paths = sorted(glob.glob(os.path.join(witness_dir, "*.tsv")))
    checks.append(("witness_dir_present", True,
                   "%s (%d ledger(s))" % (witness_dir, len(paths))))
    for path in paths:
        name = os.path.basename(path)
        if not os.path.isfile(path):
            details.append((name, False, False, "not a regular file"))
            continue
        try:
            with open(path, "rb") as fh:
                text = fh.read().decode("utf-8", "replace")
        except OSError as exc:
            details.append((name, False, False, "unreadable: %s" % exc.strerror))
            continue
        _c, wfails, wmeta = check_text(repo, rev, other_rev, text, min_rows,
                                       min_classes, timeout, env)
        nrows, wclasses = _ledger_shape(text)
        floor_ok = nrows >= min_rows and len(wclasses) >= min_classes
        declared = _declared_vacuity(wfails, wmeta["problems"])
        label = "rows=%d classes=%d fails=%s" % (
            nrows, len(wclasses), ",".join(wfails) or "none")
        if wfails and not floor_ok:
            label += " (below the witness floor %d rows/%d classes: proves nothing)" % (
                min_rows, min_classes)
        elif wfails and not declared:
            label += " (not a declared vacuity class)"
        details.append((name, bool(wfails), floor_ok and bool(wfails) and declared,
                        label))
    rejected = sum(1 for d in details if d[1])
    qualifying = sum(1 for d in details if d[2])
    total = len(details)
    if not paths:
        checks.append(("witnesses_rejected", False,
                       "witnesses=0/0 — no witness ledger in %s" % witness_dir))
        checks.append(("witnesses_vacuous", False,
                       "--witness-dir must be non-empty"))
        fails.extend(["witnesses_rejected", "witnesses_vacuous"])
    else:
        ok = rejected == total
        checks.append(("witnesses_rejected", ok,
                       "witnesses=%d/%d" % (rejected, total)))
        if not ok:
            fails.append("witnesses_rejected")
        ok2 = qualifying == total
        checks.append(("witnesses_vacuous", ok2,
                       "witnesses_vacuous=%d/%d (floor %d rows/%d classes, "
                       "declared vacuity class)"
                       % (qualifying, total, min_rows, min_classes)))
        if not ok2:
            fails.append("witnesses_vacuous")
    return checks, fails, {"witnesses": (rejected, total),
                           "witnesses_vacuous": (qualifying, total),
                           "witness_details": details}


def evaluate(repo, rev, ledger, min_rows, min_classes, timeout,
             other_rev=None, witness_dir=None, env=None):
    checks, fails = [], []
    env = env if env is not None else child_env()
    raw = read_at(repo, rev, ledger, env)
    checks.append(("ledger_present", raw is not None,
                   "absent at %s" % rev[:12] if raw is None else "%d bytes" % len(raw)))
    if raw is None:
        fails.append("ledger_present")
    meta = {"rows": 0, "classes": [], "mismatches": None, "moved": 0, "const": 0,
            "witnesses": (0, 0), "witnesses_vacuous": (0, 0),
            "witness_details": []}
    if raw is not None:
        c2, f2, m2 = check_text(repo, rev, other_rev, raw.decode("utf-8", "replace"),
                                min_rows, min_classes, timeout, env)
        checks.extend(c2)
        fails.extend(f2)
        meta.update(m2)
    w_checks, w_fails, w_meta = check_witnesses(
        repo, rev, other_rev, witness_dir, min_rows, min_classes, timeout, env)
    checks.extend(w_checks)
    fails.extend(w_fails)
    meta.update(w_meta)
    return checks, fails, meta


# --------------------------------------------------------------------------
# selftest: isolated throwaway git repos under $TMPDIR, no live lane state
# --------------------------------------------------------------------------

def _tmpdir():
    base = os.environ.get("TMPDIR") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    return tempfile.mkdtemp(prefix="c1st-", dir=base)


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def _git(repo, args, env):
    got = subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                         text=True, timeout=60, check=False, env=env)
    if got.returncode != 0:
        raise AssertionError("fixture git %s failed: %s"
                             % (" ".join(args), got.stderr.strip()[:120]))
    return got.stdout


def _mk_repo(tmp, rows, n=12):
    """Two-commit throwaway repo; the ledger is committed at the measured rev.

    rev-a: data/pNN.txt holds NN 'x' lines. rev-b: one line appended to each and
    the ledger committed, so an honest row's value differs between the two revs.
    """
    repo = os.path.join(tmp, "repo")
    os.makedirs(repo, exist_ok=True)
    env = child_env()
    _git(repo, ["init", "-q", "-b", "main"], env)
    _git(repo, ["config", "user.email", "mori@shokunin.local"], env)
    _git(repo, ["config", "user.name", "mori-shokunin"], env)
    for k in range(1, n + 1):
        _write(os.path.join(repo, "data", "p%02d.txt" % k), "x\n" * k)
    _write(os.path.join(repo, "data", "const.txt"), "c\n" * 3)
    ledger = ".ufo/waves/round-45/figures.tsv"
    _write(os.path.join(repo, ledger), "\n".join(rows) + "\n")
    _git(repo, ["add", "-A"], env)
    _git(repo, ["commit", "-q", "-m", "fixture rev-a"], env)
    rev_a = _git(repo, ["rev-parse", "HEAD"], env).strip()
    for k in range(1, n + 1):
        with open(os.path.join(repo, "data", "p%02d.txt" % k), "a",
                  encoding="utf-8") as fh:
            fh.write("x\n")
    _git(repo, ["add", "-A"], env)
    _git(repo, ["commit", "-q", "-m", "fixture rev-b"], env)
    rev_b = _git(repo, ["rev-parse", "HEAD"], env).strip()
    return repo, rev_a, rev_b, ledger


def _honest_rows(n=12):
    rows = []
    for k in range(1, n + 1):
        cls = CLASSES[(k - 1) % len(CLASSES)]
        rows.append("F%02d\t%d\t%s\tgit show @REV@:data/p%02d.txt | grep -c x"
                    % (k, k + 1, cls, k))
    return rows


def _cmd_of(row):
    return row.split("\t")[3]


def _witness_revconst(rows):
    out = list(rows)
    out[-1] = "F12\t3\tcorpus\tgit show @REV@:data/const.txt | grep -c c"
    return out


def _witness_head(rows):
    out = list(rows)
    out[0] = "F01\t2\tregistry\tgit show HEAD:data/p01.txt | grep -c x"
    return out


def _witness_dupcmd(rows):
    out = list(rows)
    out[3] = "F04\t4\tchecks\t" + _cmd_of(out[2])
    return out


def _witness_dir(tmp, bodies):
    d = os.path.join(tmp, "witnesses")
    os.makedirs(d, exist_ok=True)
    for name, rows in bodies:
        _write(os.path.join(d, name), "\n".join(rows) + "\n")
    return d


def _expect_met(repo, rev_a, rev_b, ledger, witness_dir):
    checks, fails, meta = evaluate(repo, rev_b, ledger, FLOOR_ROWS, FLOOR_CLASSES,
                                   30, rev_a, witness_dir)
    detail = "; ".join("%s(%s)" % (n, d) for n, ok, d in checks if not ok)
    assert not fails, "honest run failed: %s" % detail
    assert meta["mismatches"] == 0, meta
    return meta


def selftest():
    passes, failures = [], []

    def arm(name, fn):
        try:
            fn()
            passes.append(name)
        except AssertionError as exc:
            failures.append("%s: %s" % (name, exc))
        except Exception as exc:                     # a crash is a failed arm
            failures.append("%s: %s: %s" % (name, type(exc).__name__, exc))

    def honest_ledger_met():
        tmp = _tmpdir()
        try:
            rows = _honest_rows()
            repo, rev_a, rev_b, ledger = _mk_repo(tmp, rows)
            wdir = _witness_dir(tmp, [("w-revconst.tsv", _witness_revconst(rows)),
                                      ("w-head.tsv", _witness_head(rows)),
                                      ("w-dupcmd.tsv", _witness_dupcmd(rows))])
            meta = _expect_met(repo, rev_a, rev_b, ledger, wdir)
            assert meta["witnesses"] == (3, 3), meta
            assert all(d[1] for d in meta["witness_details"]), meta
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def offbyone_row_mismatch():
        tmp = _tmpdir()
        try:
            rows = _honest_rows()
            cells = rows[0].split("\t")
            cells[1] = str(int(cells[1]) + 1)
            rows[0] = "\t".join(cells)
            repo, rev_a, rev_b, ledger = _mk_repo(tmp, rows)
            _c, fails, meta = evaluate(repo, rev_b, ledger, FLOOR_ROWS,
                                       FLOOR_CLASSES, 30, rev_a)
            assert "commands_reconcile" in fails, fails
            assert meta["mismatches"] == 1, meta
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def junk_producer_rejected():
        tmp = _tmpdir()
        try:
            base = _honest_rows()
            for junk in ("echo 3",
                         "bash -c 'git show @REV@:data/p01.txt | grep -c x'"):
                rows = list(base)
                cells = rows[0].split("\t")
                cells[3] = junk
                rows[0] = "\t".join(cells)
                repo, rev_a, rev_b, ledger = _mk_repo(os.path.join(tmp, junk[:4]), rows)
                _c, fails, meta = evaluate(repo, rev_b, ledger, FLOOR_ROWS,
                                           FLOOR_CLASSES, 30, rev_a)
                assert "rows_parse" in fails, "%r accepted: %s" % (junk, fails)
                assert meta["mismatches"] is None, meta
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def below_floor_rejected():
        tmp = _tmpdir()
        try:
            repo, rev_a, rev_b, ledger = _mk_repo(tmp, _honest_rows(5))
            _c, fails, meta = evaluate(repo, rev_b, ledger, FLOOR_ROWS,
                                       FLOOR_CLASSES, 30, rev_a)
            assert "row_floor" in fails, fails
            assert meta["rows"] == 5, meta
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def absent_ledger_unmet():
        tmp = _tmpdir()
        try:
            repo, rev_a, rev_b, _ledger = _mk_repo(tmp, _honest_rows())
            _c, fails, meta = evaluate(repo, rev_b, ".ufo/waves/round-45/absent.tsv",
                                       FLOOR_ROWS, FLOOR_CLASSES, 30, rev_a)
            assert "ledger_present" in fails, fails
            assert meta["mismatches"] is None, meta
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def duplicate_id_rejected():
        tmp = _tmpdir()
        try:
            rows = _honest_rows()
            cells = rows[1].split("\t")
            cells[0] = rows[0].split("\t")[0]
            rows[1] = "\t".join(cells)
            repo, rev_a, rev_b, ledger = _mk_repo(tmp, rows)
            _c, fails, meta = evaluate(repo, rev_b, ledger, FLOOR_ROWS,
                                       FLOOR_CLASSES, 30, rev_a)
            parsed, problems = parse_ledger("\n".join(rows) + "\n")
            assert any("duplicate id" in p for p in problems), problems
            assert "rows_parse" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def duplicate_command_rejected():
        tmp = _tmpdir()
        try:
            rows = _honest_rows()
            cells = rows[3].split("\t")
            cells[3] = _cmd_of(rows[2])
            rows[3] = "\t".join(cells)
            repo, rev_a, rev_b, ledger = _mk_repo(tmp, rows)
            _c, fails, meta = evaluate(repo, rev_b, ledger, FLOOR_ROWS,
                                       FLOOR_CLASSES, 30, rev_a)
            parsed, problems = parse_ledger("\n".join(rows) + "\n")
            assert any("duplicate command" in p for p in problems), problems
            assert "rows_parse" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def head_reading_row_rejected():
        variants = ("git show HEAD:data/p01.txt | grep -c x",
                    "git rev-parse @REV@",
                    "git show 0123456789abcdef0123456789abcdef01234567:data/p01.txt"
                    " | grep -c x",
                    "git show @{u}:data/p01.txt | grep -c x")
        for junk in variants:
            rows = _honest_rows()
            cells = rows[0].split("\t")
            cells[3] = junk
            rows[0] = "\t".join(cells)
            _parsed, problems = parse_ledger("\n".join(rows) + "\n")
            assert problems, "%r parsed as honest" % junk
            assert any("resolves the tip" in p or "not a read verb" in p
                       for p in problems), (junk, problems)

    def revision_constant_row_rejected():
        tmp = _tmpdir()
        try:
            rows = _witness_revconst(_honest_rows())
            repo, rev_a, rev_b, ledger = _mk_repo(tmp, rows)
            _c, fails, meta = evaluate(repo, rev_b, ledger, FLOOR_ROWS,
                                       FLOOR_CLASSES, 30, rev_a)
            assert "revision_sensitivity" in fails, fails
            assert meta["mismatches"] == 0, meta
            rows[11] = rows[11] + "\tCONST=fixture constant by construction"
            _write(os.path.join(repo, ledger), "\n".join(rows) + "\n")
            _git(repo, ["commit", "-q", "-am", "const annotation"], child_env())
            rev_c = _git(repo, ["rev-parse", "HEAD"], child_env()).strip()
            _c, fails2, _m = evaluate(repo, rev_c, ledger, FLOOR_ROWS,
                                      FLOOR_CLASSES, 30, rev_a)
            assert "revision_sensitivity" not in fails2, fails2
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def witness_dir_one_passing_witness():
        tmp = _tmpdir()
        try:
            rows = _honest_rows()
            repo, rev_a, rev_b, ledger = _mk_repo(tmp, rows)
            wdir = _witness_dir(tmp, [("w-revconst.tsv", _witness_revconst(rows)),
                                      ("w-head.tsv", _witness_head(rows)),
                                      ("w-honest.tsv", rows)])
            _c, fails, meta = evaluate(repo, rev_b, ledger, FLOOR_ROWS,
                                       FLOOR_CLASSES, 30, rev_a, wdir)
            assert meta["witnesses"] == (2, 3), meta
            assert meta["witnesses_vacuous"] == (2, 3), meta
            assert "witnesses_rejected" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def all_const_ledger_unmet():
        tmp = _tmpdir()
        try:
            rows = [r + "\tCONST=fixture figure held constant"
                    for r in _honest_rows()]
            repo, rev_a, rev_b, ledger = _mk_repo(tmp, rows)
            wdir = _witness_dir(tmp, [
                ("w-revconst.tsv", _witness_revconst(_honest_rows())),
                ("w-head.tsv", _witness_head(_honest_rows())),
                ("w-dupcmd.tsv", _witness_dupcmd(_honest_rows()))])
            _c, fails, meta = evaluate(repo, rev_b, ledger, FLOOR_ROWS,
                                       FLOOR_CLASSES, 30, rev_a, wdir)
            assert meta["moved"] == 0 and meta["const"] == 12, meta
            assert "revision_moves" in fails, fails
            assert "const_cap" in fails, fails
            assert "revision_sensitivity" not in fails, fails
            assert meta["witnesses_vacuous"] == (3, 3), meta
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def const_heavy_ledger_unmet():
        tmp = _tmpdir()
        try:
            honest = _honest_rows()
            rows = [honest[0]] + [r + "\tCONST=fixture figure held constant"
                                  for r in honest[1:]]
            repo, rev_a, rev_b, ledger = _mk_repo(tmp, rows)
            _c, fails, meta = evaluate(repo, rev_b, ledger, FLOOR_ROWS,
                                       FLOOR_CLASSES, 30, rev_a)
            assert meta["moved"] == 1 and meta["const"] == 11, meta
            assert "const_cap" in fails, fails
            assert "revision_moves" not in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def witness_without_floor_unmet():
        tmp = _tmpdir()
        try:
            repo, rev_a, rev_b, ledger = _mk_repo(tmp, _honest_rows())
            wdir = os.path.join(tmp, "witnesses")
            os.makedirs(wdir)
            _write(os.path.join(wdir, "junk.tsv"),
                   "garbage line one\ngarbage line two\ngarbage line three\n")
            _write(os.path.join(wdir, "junk12.tsv"), "\n".join(
                "garbage\t%d\t%s\tnot a git pipeline"
                % (i, CLASSES[i % len(CLASSES)]) for i in range(12)) + "\n")
            _c, fails, meta = evaluate(repo, rev_b, ledger, FLOOR_ROWS,
                                       FLOOR_CLASSES, 30, rev_a, wdir)
            assert meta["witnesses"] == (2, 2), meta
            assert meta["witnesses_vacuous"] == (0, 2), meta
            assert "witnesses_rejected" not in fails, fails
            assert "witnesses_vacuous" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def stage_option_injection_rejected():
        rejects = (
            "git ls-tree -r --name-only @REV@ | sort -S 1K "
            "--compress-program=/tmp/prog.sh | wc -l",
            "git ls-tree -r --name-only @REV@ | sort -o /tmp/out | wc -l",
            "git ls-tree -r --name-only @REV@ | sort -T /tmp | wc -l",
            "git --git-dir /tmp/x show @REV@:SKILL.md",
            "git -c core.pager=cat show @REV@:SKILL.md",
            "git --work-tree=/tmp show @REV@:SKILL.md",
            "git show @REV@:SKILL.md | grep -c x | tee /tmp/y",
        )
        for cmd in rejects:
            _rows, problems = parse_ledger("F01\t5\twave\t%s\n" % cmd)
            assert problems, "%r parsed as honest" % cmd
        accepts = (
            "git ls-tree -r --name-only @REV@ .ufo | grep -c '\\.md$'",
            "git log --format=%s @REV@ | wc -l",
            "git cat-file -e @REV@:SKILL.md | wc -l",
            "git rev-list --count @REV@",
            "git grep -l x @REV@ -- corpus | grep -c .",
            "git diff --name-only @REV@ @REV@~1 | wc -l",
            "git show @REV@:SKILL.md | grep -cE '^ {0,3}\\|'",
        )
        for cmd in accepts:
            _rows, problems = parse_ledger("F01\t5\twave\t%s\n" % cmd)
            assert not problems, "%r rejected: %s" % (cmd, problems)

    def short_sha_tip_rejected():
        for pin in ("3ad8faa", "deadbeef0",
                    "3ad8faaa637ae46661f9427fea1c208bf49ea82"):
            rows = _honest_rows()
            cells = rows[11].split("\t")
            cells[3] = "git log --format=%%s %s @REV@ | wc -l" % (pin,)
            rows[11] = "\t".join(cells)
            _p, problems = parse_ledger("\n".join(rows) + "\n")
            assert any("revision-like hex pin" in p or "resolves the tip" in p
                       for p in problems), (pin, problems)
        rows = _honest_rows()
        rows[11] = "F12\t12\tchecks\tgit log --format=%s @REV@ | wc -l"
        _p, problems = parse_ledger("\n".join(rows) + "\n")
        assert not problems, problems

    def absent_path_zero_rejected():
        for const in (None, "CONST=path absent at both revisions, so the figure is 0"):
            cell = ("0\twave\tgit ls-tree -r --name-only @REV@ "
                    "corpus/no-such-dir-r45 | wc -l")
            if const:
                cell += "\t" + const
            _p, problems = parse_ledger("F01\t%s\n" % cell)
            assert any("asserted 0 from a listing verb" in p for p in problems), (
                const, problems)
        _p, problems = parse_ledger(
            "F01\t0\twave\tgit rev-list --count @REV@ -- .ufo/waves/round-45\n")
        assert not problems, problems
        _p, problems = parse_ledger(
            "F01\t5\twave\tgit ls-tree -r --name-only @REV@ corpus | wc -l\n")
        assert not problems, problems

    arm("honest_ledger_met", honest_ledger_met)
    arm("offbyone_row_mismatch", offbyone_row_mismatch)
    arm("junk_producer_rejected", junk_producer_rejected)
    arm("below_floor_rejected", below_floor_rejected)
    arm("absent_ledger_unmet", absent_ledger_unmet)
    arm("duplicate_id_rejected", duplicate_id_rejected)
    arm("duplicate_command_rejected", duplicate_command_rejected)
    arm("head_reading_row_rejected", head_reading_row_rejected)
    arm("revision_constant_row_rejected", revision_constant_row_rejected)
    arm("witness_dir_one_passing_witness", witness_dir_one_passing_witness)
    arm("all_const_ledger_unmet", all_const_ledger_unmet)
    arm("const_heavy_ledger_unmet", const_heavy_ledger_unmet)
    arm("witness_without_floor_unmet", witness_without_floor_unmet)
    arm("stage_option_injection_rejected", stage_option_injection_rejected)
    arm("short_sha_tip_rejected", short_sha_tip_rejected)
    arm("absent_path_zero_rejected", absent_path_zero_rejected)

    for name in passes:
        print("selftest PASS %s" % name)
    for name in failures:
        print("selftest FAIL %s" % name)
    print("C1_SELFTEST pass=%d fail=%d" % (len(passes), len(failures)))
    return 0 if not failures else 1


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------

def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=repo_default())
    ap.add_argument("--ledger", default=".ufo/waves/round-45/figures.tsv")
    ap.add_argument("--other-rev")
    ap.add_argument("--witness-dir")
    ap.add_argument("--min-rows", type=int, default=FLOOR_ROWS)
    ap.add_argument("--min-classes", type=int, default=FLOOR_CLASSES)
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    if not args.rev:
        print("usage: count-c1.py <rev> --other-rev REV [--witness-dir DIR] "
              "[--repo PATH] [--ledger PATH] [--selftest]")
        print("C1_SETUP usage: a committed scoring revision is required")
        return 2
    if args.rev == "WORK":
        print("C1_SETUP WORK is not a scoring revision: measure a committed revision")
        return 2

    repo = os.path.abspath(args.repo)
    min_rows = max(FLOOR_ROWS, args.min_rows)
    min_classes = max(FLOOR_CLASSES, args.min_classes)
    timeout = max(1, args.timeout)
    witness_dir = os.path.abspath(args.witness_dir) if args.witness_dir else None
    env = child_env()

    try:
        if not os.path.isdir(os.path.join(repo, ".git")):
            raise Setup("repo is not a git checkout: %s" % repo)
        rev = resolve(repo, args.rev, env)
        other_rev = resolve(repo, args.other_rev, env) if args.other_rev else None
        checks, fails, meta = evaluate(repo, rev, args.ledger, min_rows,
                                       min_classes, timeout, other_rev,
                                       witness_dir, env)
    except Setup as exc:
        print("C1_SETUP %s" % exc)
        return 2

    for name, ok, detail in checks:
        print("check %-22s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    for name, rejected, vacuous, label in meta["witness_details"]:
        state = ("rejected" if vacuous else
                 "NOT-PROVING" if rejected else "ACCEPTED")
        print("witness %-24s %s (%s)" % (name, state, label))
    print("floors rows>=%d classes>=%d (frozen; requested --min-rows %d "
          "--min-classes %d)" % (min_rows, min_classes, args.min_rows,
                                 args.min_classes))
    rejected_n, total_n = meta["witnesses"]
    vac_n, _vac_total = meta["witnesses_vacuous"]
    verdict = "C1=met" if not fails else "C1=unmet"
    print("%s mismatches=%s rows=%d classes=%s floor_rows=%d floor_classes=%d "
          "rev=%s repo=%s other_rev=%s witnesses=%d/%d witnesses_vacuous=%d/%d%s"
          % (verdict, "?" if meta["mismatches"] is None else meta["mismatches"],
             meta["rows"], ",".join(meta["classes"]) or "-", min_rows,
             min_classes, rev, repo, other_rev or "-", rejected_n, total_n,
             vac_n, total_n,
             "" if not fails else " failed=" + ",".join(sorted(set(fails)))))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
