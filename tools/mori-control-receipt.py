#!/usr/bin/env python3
"""mori-control-receipt.py — control-receipt binding guard (mori round 79, C1).

A control receipt is a text file split into sections at lines matching `^## `
(content before the first heading is section `(head)`). A section states count
claims as stripped lines matching `^[A-Za-z][A-Za-z0-9_.-]*=-?[0-9]+$`. The
lane's binding rule: a section that states count claims must also carry at
least one command line — a non-comment line whose stripped text starts with
`$ `, or whose first token is one of the known command verbs, or a non-comment
line containing ` cmd=`. The D78-1 witness
(`.ufo/waves/round-78/evidence/controls-r78.txt`) is a control receipt stating
counts with no counting command; this guard exists to make that shape fail
loudly.

Usage:
  mori-control-receipt.py RECEIPT [RECEIPT ...]   check the named receipts
  mori-control-receipt.py --dir DIR              check every *.txt directly
                                                 under DIR (sorted); may be
                                                 combined with receipt paths
                                                 (dir files first)
  mori-control-receipt.py --selftest             in-memory self-test, no files
  mori-control-receipt.py --help                 this usage

Output per file:
  CONTROL_RECEIPT <path> sections=S claims=C bound=B unbound=U
  unbound <path>#<section> claims=N keys=<k1,k2>     (one per unbound section)
Final line:
  CONTROL_RECEIPT_SUMMARY files=F sections=S claims=C unbound=U

Exit codes: 0 no section with claims is unbound; 1 some is; 2 setup (usage,
missing path, unreadable file). Setup diagnostics print on stdout like every
other line: the program never writes to stderr.

Python 3 standard library only; `python -I` safe; stdout only — no file
writes, no network, no subprocess, no temp files.
"""

import os
import re
import sys

PROG = "mori-control-receipt.py"

# The contract's verb list (frozen in .ufo/waves/round-79/contract.md § C1).
VERBS = frozenset((
    "git", "grep", "egrep", "python", "python3", "bash", "sh", "curl", "wget",
    "wc", "sha256sum", "ls", "cat", "awk", "sed", "jq", "node", "systemctl",
    "journalctl", "df", "du", "ps", "stat", "find", "sort", "comm", "cmp",
    "head", "tail", "xxd", "od", "readlink", "realpath", "ss", "lsof", "tar",
    "zcat", "rg",
))

CLAIM_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*=-?[0-9]+$")

HEAD_SECTION = "(head)"


def is_comment(line):
    return line.strip().startswith("#")


def is_command_line(line):
    """A command line binds a section: `$ cmd`, a verb-led line, or ` cmd=`."""
    if is_comment(line):
        return False
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("$ "):
        return True
    if stripped.split(None, 1)[0] in VERBS:
        return True
    if " cmd=" in line:
        return True
    return False


def claim_key(line):
    """Return the claim key if the stripped line is a count claim, else None."""
    stripped = line.strip()
    if CLAIM_RE.match(stripped):
        return stripped.split("=", 1)[0]
    return None


def split_sections(text):
    """Split receipt text into [name, lines] sections at `^## ` headings."""
    sections = [[HEAD_SECTION, []]]
    for line in text.splitlines():
        if line.startswith("## "):
            sections.append([line[3:].strip(), []])
        else:
            sections[-1][1].append(line)
    return sections


def analyze_text(text):
    """Yield (name, claim_keys, has_command) per section of a receipt body."""
    for name, lines in split_sections(text):
        keys = [k for k in (claim_key(line) for line in lines) if k is not None]
        has_command = any(is_command_line(line) for line in lines)
        yield name, keys, has_command


def dir_txt_names(listdir):
    """Every `*.txt` name, sorted — the --dir collection rule."""
    return sorted(name for name in listdir if name.endswith(".txt"))


def read_file(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def check_receipts(paths, read_text, out):
    """Check receipts; return 0/1 by the binding rule, 2 on setup failure.

    Every line, setup diagnostics included, goes to `out`: the program never
    writes to stderr.
    """
    total_sections = total_claims = total_unbound = 0
    any_unbound = False
    for path in paths:
        try:
            sections = list(analyze_text(read_text(path)))
        except (OSError, ValueError) as exc:
            print("%s: cannot read receipt: %s: %s" % (PROG, path, exc),
                  file=out)
            return 2
        unbound = []
        n_claims = 0
        n_bound = 0
        for name, keys, has_command in sections:
            if not keys:
                continue
            n_claims += len(keys)
            if has_command:
                n_bound += 1
            else:
                unbound.append((name, keys))
        print("CONTROL_RECEIPT %s sections=%d claims=%d bound=%d unbound=%d"
              % (path, len(sections), n_claims, n_bound, len(unbound)),
              file=out)
        for name, keys in unbound:
            print("unbound %s#%s claims=%d keys=%s"
                  % (path, name, len(keys), ",".join(keys)), file=out)
        total_sections += len(sections)
        total_claims += n_claims
        total_unbound += len(unbound)
        any_unbound = any_unbound or bool(unbound)
    print("CONTROL_RECEIPT_SUMMARY files=%d sections=%d claims=%d unbound=%d"
          % (len(paths), total_sections, total_claims, total_unbound),
          file=out)
    return 1 if any_unbound else 0


def usage(out):
    out.write(__doc__.split("Usage:", 1)[1].rstrip() + "\n")


def main(argv):
    args = argv[1:]
    selftest = False
    dirpath = None
    paths = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--selftest":
            selftest = True
        elif arg == "--dir":
            i += 1
            if i >= len(args):
                print("%s: --dir needs a value" % PROG, file=sys.stdout)
                return 2
            dirpath = args[i]
        elif arg.startswith("--dir="):
            dirpath = arg[len("--dir="):]
        elif arg in ("-h", "--help"):
            usage(sys.stdout)
            return 0
        elif arg.startswith("-"):
            print("%s: unknown option: %s" % (PROG, arg), file=sys.stdout)
            return 2
        else:
            paths.append(arg)
        i += 1
    if selftest:
        return run_selftest()
    if not paths and dirpath is None:
        usage(sys.stdout)
        print("%s: no receipt path and no --dir given" % PROG, file=sys.stdout)
        return 2
    files = []
    if dirpath is not None:
        if not os.path.isdir(dirpath):
            print("%s: --dir: not a directory: %s" % (PROG, dirpath),
                  file=sys.stdout)
            return 2
        names = [n for n in dir_txt_names(os.listdir(dirpath))
                 if os.path.isfile(os.path.join(dirpath, n))]
        if not names:
            print("%s: --dir: no .txt files under: %s" % (PROG, dirpath),
                  file=sys.stdout)
            return 2
        files.extend(os.path.join(dirpath, n) for n in names)
    files.extend(paths)
    return check_receipts(files, read_file, sys.stdout)


def run_selftest():
    """In-memory self-test: no files written, no subprocess, stdout only."""
    import io
    from contextlib import redirect_stderr, redirect_stdout

    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
        print("case %02d %-38s %s" % (passed + failed, name,
                                      "pass" if cond else "FAIL"))

    _MISSING = object()

    def mem_reader(store):
        def read(path):
            value = store.get(path, _MISSING)
            if value is _MISSING:
                raise FileNotFoundError(2, "no such file", path)
            if isinstance(value, Exception):
                raise value
            return value
        return read

    def run(store, args_paths):
        """Run check_receipts over in-memory files; return (rc, stdout)."""
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = check_receipts(args_paths, mem_reader(store), out)
        return rc, out.getvalue(), err.getvalue()

    def run_main(argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = main(argv)
        return rc, out.getvalue(), err.getvalue()

    # 1. bound section: `$ cmd` above the count in the (head) section.
    rc, out, _ = run({"m:1": "$ wc -l /etc/hosts\nmatched=7\n"}, ["m:1"])
    check("bound section ($ cmd above count)",
          rc == 0 and "CONTROL_RECEIPT m:1 sections=1 claims=1 bound=1 unbound=0" in out
          and out.rstrip().endswith("CONTROL_RECEIPT_SUMMARY files=1 sections=1 claims=1 unbound=0"))

    # 2. unbound section: a count with no counting command.
    rc, out, _ = run({"m:2": "matched=7\n"}, ["m:2"])
    check("unbound section (count, no command)",
          rc == 1 and "unbound m:2#(head) claims=1 keys=matched" in out
          and "CONTROL_RECEIPT m:2 sections=1 claims=1 bound=0 unbound=1" in out
          and "CONTROL_RECEIPT_SUMMARY files=1 sections=1 claims=1 unbound=1" in out)

    # 3. a `# comment` line is NOT a command; a commented claim is no claim.
    rc, out, _ = run({"m:3": "# wc -l /etc/hosts\n# matched=7\nmatched=7\n"}, ["m:3"])
    check("comment line neither command nor claim",
          rc == 1 and "unbound m:3#(head) claims=1 keys=matched" in out)

    # 4. the inline `cmd=` form binds.
    rc, out, _ = run({"m:4": "probe cmd=wc -l /etc/hosts\nmatched=7\n"}, ["m:4"])
    check("inline cmd= line binds the section",
          rc == 0 and "bound=1 unbound=0" in out)

    # 5. section-level split across two ## headings (plus (head)).
    rc, out, _ = run({"m:5": "a=1\n## second\nb=2\n## third\n$ echo done\nc=3\n"}, ["m:5"])
    check("split across two ## headings",
          rc == 1 and "CONTROL_RECEIPT m:5 sections=3 claims=3 bound=1 unbound=2" in out
          and "unbound m:5#(head) claims=1 keys=a" in out
          and "unbound m:5#second claims=1 keys=b" in out)

    # 6. non-integer key=value lines are NOT claims.
    rc, out, _ = run({"m:6": "url=https://example.com/x\n"
                             "run-start=2026-11-04T05:32:25Z\n"
                             "entering=84c6cbc3b47c\n"}, ["m:6"])
    check("non-integer key=value not a claim",
          rc == 0 and "CONTROL_RECEIPT m:6 sections=1 claims=0 bound=0 unbound=0" in out)

    # 7. negative integer claims are claims.
    rc, out, _ = run({"m:7": "delta=-3\nzero=-0\n"}, ["m:7"])
    check("negative integer claim",
          rc == 1 and "claims=2" in out and "keys=delta,zero" in out)

    # 8. an empty file: one empty (head) section, no claims, rc 0.
    rc, out, _ = run({"m:8": ""}, ["m:8"])
    check("empty file",
          rc == 0 and "CONTROL_RECEIPT m:8 sections=1 claims=0 bound=0 unbound=0" in out
          and "CONTROL_RECEIPT_SUMMARY files=1 sections=1 claims=0 unbound=0" in out)

    # 9. a missing path is setup failure rc 2 (real filesystem, no writes),
    #    with the diagnostic on stdout and stderr untouched (stdout only).
    rc, out, err = run_main([PROG, "/nonexistent/mori-r79-selftest/absent.txt"])
    check("missing path rc 2, diagnostic on stdout",
          rc == 2 and "cannot read receipt" in out and err == "")

    # 10. a receipt with no claims at all is not unbound.
    rc, out, _ = run({"m:10": "## notes\njust prose, no claims\n$ ls\n"}, ["m:10"])
    check("receipt with no claims rc 0",
          rc == 0 and "CONTROL_RECEIPT m:10 sections=2 claims=0 bound=0 unbound=0" in out)

    # 11. a verb-led first token is a command line.
    rc, out, _ = run({"m:11": "git status --short\nclean=1\n"}, ["m:11"])
    check("verb-led first token binds",
          rc == 0 and "bound=1 unbound=0" in out)

    # 12. indentation does not rescue a comment or defeat a claim.
    rc, out, _ = run({"m:12": "   # git status\n\tcount=2\n"}, ["m:12"])
    check("indented comment/claim handled",
          rc == 1 and "claims=1" in out and "keys=count" in out)

    # 13. the claim-key character class: digits-lead and +values are no claims.
    rc, out, _ = run({"m:13": "2fast=1\nkey=+5\nn=1x\nrun.key-1=42\n"}, ["m:13"])
    check("claim key character class",
          rc == 1 and "claims=1" in out and "keys=run.key-1" in out)

    # 14. `cmd=` without the leading space does not bind (containment form).
    rc, out, _ = run({"m:14": "cmd=ls\ncount=1\n"}, ["m:14"])
    check("bare cmd= without space does not bind",
          rc == 1 and "unbound m:14#(head) claims=1 keys=count" in out)

    # 15. multi-file aggregation in the summary; rc 1 from the unbound file.
    rc, out, _ = run({"m:15a": "n=1\n", "m:15b": "$ ls\nn=2\n"}, ["m:15a", "m:15b"])
    check("summary aggregates across files",
          rc == 1 and "CONTROL_RECEIPT_SUMMARY files=2 sections=2 claims=2 unbound=1" in out)

    # 16. --dir collection: *.txt only, sorted, non-txt ignored.
    check("dir collection filters and sorts",
          dir_txt_names(["b.txt", "a.txt", "c.md", "z.txt~", "10.txt", "2.txt"])
          == ["10.txt", "2.txt", "a.txt", "b.txt"])

    # 17. an unreadable file is setup failure rc 2, diagnostic on stdout.
    rc, out, err = run({}, ["m:17"])
    # empty store => FileNotFoundError => rc 2 with the receipt named
    check("unreadable file rc 2, diagnostic on stdout",
          rc == 2 and "m:17" in out and "cannot read receipt" in out and err == "")

    # 18. an unbound section line names the section heading text.
    rc, out, _ = run({"m:18": "## 4. the witness section\ncorrection=0\n"}, ["m:18"])
    check("unbound line carries heading text",
          rc == 1 and "unbound m:18#4. the witness section claims=1 keys=correction" in out)

    # 19. every rc 2 setup path prints its diagnostic/usage on stdout and
    #     writes nothing to stderr (the stdout-only rule, error paths too).
    ok19 = True
    for argv in ([PROG], [PROG, "--bogus"], [PROG, "--dir"],
                 [PROG, "--dir", "/nonexistent/mori-r79-selftest"],
                 [PROG, "/nonexistent/mori-r79-selftest/absent.txt"]):
        rc2, out2, err2 = run_main(argv)
        ok19 = ok19 and rc2 == 2 and err2 == "" and out2 != ""
    check("rc 2 diagnostics on stdout only", ok19)

    print("CONTROL_RECEIPT_SELFTEST pass=%d fail=%d" % (passed, failed))
    return 0 if (failed == 0 and passed >= 10) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
