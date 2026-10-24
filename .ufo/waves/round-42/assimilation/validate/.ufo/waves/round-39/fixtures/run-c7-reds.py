#!/usr/bin/env python3
"""Round-39 C7 red receipts: re-derive that the round-38 counter bytes accept
the four M18 bypass classes on the entering tip (r38 lesson M18).

Builds, under the round-39 scratch directory:
  c7-red-one-char.txt    one-char anchors (`#`, `:`, `==`) pass r38 check_anchors
  c7-red-comment.txt     comment-parked anchors pass r38 check_anchors
  c7-red-classifier.txt  a cheat probe whose row_states detail always carries both
                         state strings passes r38 drift_kill
  c7-red-clone.txt       the fully fabricated self-consistent clone prints C4=met

Usage: run-c7-reds.py <entering-rev> <lane-repo>
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

W = os.path.dirname(os.path.abspath(__file__))
EVIDENCE = os.path.join(W, "..", "evidence")
R38_COUNTER = ".ufo/waves/round-38/count-c4.py"
TOOL_REL = "tools/mori-source-drift.py"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git_show(repo, rev, rel, dest):
    proc = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, rel)],
                          capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        raise SystemExit("git show %s:%s failed: %s" % (rev, rel, proc.stderr))
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(proc.stdout)


def receipt(path, title, lines):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("command: python3 .ufo/waves/round-39/fixtures/run-c7-reds.py "
                 "(section: %s)\n" % title)
        fh.write("\n".join(lines) + "\n")


def main(argv):
    rev, repo = argv[1], os.path.abspath(argv[2])
    scratch = os.path.join(W, "..", "scratch", "c7-reds")
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    r38_path = os.path.join(scratch, "count-c4-r38.py")
    git_show(repo, rev, R38_COUNTER, r38_path)
    r38 = load_module(r38_path, "count_c4_r38")
    tool_text = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, TOOL_REL)],
                               capture_output=True, text=True, timeout=120).stdout

    # 1. one-char anchors
    one_char = "# fabricated entry with one-char anchors\n\nanchor: #\nanchor: :\nanchor: ==\n"
    ok, detail = r38.check_anchors(one_char, tool_text)
    receipt(os.path.join(EVIDENCE, "c7-red-one-char.txt"), "one-char anchors", [
        "r38 check_anchors on a fabricated entry whose anchors are `#`, `:`, `==`:",
        "  accepted=%s (%s)" % (ok, detail),
        "verdict: %s" % ("RED (bypass accepted)" if ok else "not reproduced"),
    ])

    # 2. comment-parked anchors
    comment_entry = open(os.path.join(W, "witness-comment-anchors.md"),
                         encoding="utf-8").read()
    ok, detail = r38.check_anchors(comment_entry, tool_text)
    receipt(os.path.join(EVIDENCE, "c7-red-comment.txt"), "comment-parked anchors", [
        "r38 check_anchors on witness-comment-anchors.md (phrases that occur in the",
        "tool only inside `#` comment lines):",
        "  accepted=%s (%s)" % (ok, detail),
        "verdict: %s" % ("RED (bypass accepted)" if ok else "not reproduced"),
    ])

    # 3. cheat probe passes r38 drift_kill (symmetric substring check)
    cheat = tool_text.replace(
        '"got=%r want=%r" % (got, expected)',
        '"got=%r want=%r (\'S103\', \'drifted\') (\'S103\', \'excerpt\')" % (got, expected)')
    if cheat == tool_text:
        raise SystemExit("cheat substitution anchor absent in probe bytes")
    tool_copy = os.path.join(scratch, "cheat-probe.py")
    with open(tool_copy, "w", encoding="utf-8") as fh:
        fh.write(cheat)
    mutant = os.path.join(scratch, "cheat-probe-mutant.py")
    with open(mutant, "w", encoding="utf-8") as fh:
        fh.write(cheat.replace(r38.DRIFT_MUTANT_FROM, r38.DRIFT_MUTANT_TO))
    rc_honest, arms_honest, out_honest = r38.selftest_arms(tool_copy)
    rc_mut, arms_mut, out_mut = r38.selftest_arms(mutant)
    state = arms_mut.get("row_states", ("", ""))
    flipped = ("('S103', 'drifted')" in state[1]
               and ("('S103', 'excerpt')" in state[1]
                    or "('S103', 'fresh')" in state[1]))
    passed = rc_mut == 1 and state[0] == "FAIL" and flipped
    receipt(os.path.join(EVIDENCE, "c7-red-classifier.txt"), "cheat probe", [
        "cheat: row_states detail always appends ('S103', 'drifted') and",
        "('S103', 'excerpt') regardless of the classification (r38 M18 shape).",
        "honest run: exit=%s row_states=%s" % (rc_honest, arms_honest.get("row_states")),
        "mutated run: exit=%s row_states=%s" % (rc_mut, state),
        "r38 drift_kill accepted=%s" % passed,
        "verdict: %s" % ("RED (bypass accepted)" if passed else "not reproduced"),
    ])

    # 4. fabricated self-consistent clone: stub entry with verbatim real anchors
    #    + invented live receipt (the real ten drifted rows plus S103, which has
    #    no committed copy). r38 checks accept it; the round-39 live_rows_v2
    #    check (committed copy required) rejects it.
    sandbox = os.path.join(scratch, "selfconsistent-sandbox")
    subprocess.run(["git", "clone", "--quiet", "--shared", repo, sandbox],
                   check=True, timeout=300)
    subprocess.run(["git", "-C", sandbox, "checkout", "--quiet", rev],
                   check=True, timeout=120)
    subprocess.run(["git", "-C", sandbox, "config", "user.name", "mori witness"],
                   check=True)
    subprocess.run(["git", "-C", sandbox, "config", "user.email",
                    "witness@shokunin.invalid"], check=True)
    fabricated_entry = (
        "# fabricated binding: verbatim real anchors, invented receipt\n\n"
        "anchor: FETCH_MAX_BYTES = 4 * 1024 * 1024\n"
        "anchor: if not _public_redirect_target(final):\n"
        "anchor: return \"drifted\"\n")
    real_receipt = subprocess.run(
        ["git", "-C", repo, "show",
         "%s:.ufo/waves/round-37/evidence/drift-live-r37.txt" % rev],
        capture_output=True, text=True, timeout=120).stdout
    fabricated_receipt = real_receipt.replace(
        "drifted=10 ", "drifted=11 ").rstrip("\n") + "\nS103 drifted\n"
    targets = {
        "corpus/knowledge/source-drift-content-anchor-r38.md": fabricated_entry,
        ".ufo/waves/round-37/evidence/drift-live-r37.txt": fabricated_receipt,
    }
    for rel, body in targets.items():
        path = os.path.join(sandbox, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
    subprocess.run(["git", "-C", sandbox, "add", *targets.keys()], check=True)
    subprocess.run(["git", "-C", sandbox, "commit", "-q", "-m",
                    "fabricated self-consistent binding (r39 control)"], check=True)
    r38_src_fix = os.path.join(W, "..", "..", "round-38", "fixtures")
    r38_fix = os.path.join(scratch, "fixtures")
    shutil.copytree(r38_src_fix, r38_fix)
    r38_local = os.path.join(scratch, "count-c4-r38.py")
    proc_r38 = subprocess.run([sys.executable, r38_local, "HEAD", "--repo", sandbox],
                              capture_output=True, text=True, timeout=600)
    r38_tail = [l for l in proc_r38.stdout.splitlines()
                if l.startswith(("check", "negative", "C4="))]
    r38_met = "C4=met" in proc_r38.stdout
    c7 = os.path.join(W, "..", "count-c7.py")
    proc_v2 = subprocess.run([sys.executable, c7, "HEAD", "--repo", sandbox,
                              "--seed", "7"],
                             capture_output=True, text=True, timeout=600)
    v2_tail = [l for l in proc_v2.stdout.splitlines()
               if l.startswith(("check", "negative", "C7="))]
    v2_met = "C7=met" in proc_v2.stdout
    receipt(os.path.join(EVIDENCE, "c7-red-clone.txt"), "fabricated clone", [
        "clone: fabricated stub entry (verbatim real anchors) + invented live",
        "receipt (real ten drifted rows plus S103, which has no committed copy)",
        "committed as a sandbox child of %s" % rev[:12],
        "r38 counter: exit=%d" % proc_r38.returncode,
    ] + r38_tail + [
        "verdict r38: %s" % ("RED (fabricated binding accepted)" if r38_met
                             else "not reproduced"),
        "round-39 counter: exit=%d" % proc_v2.returncode,
    ] + v2_tail + [
        "verdict round-39: %s" % ("still accepted (disclosed verbatim-clone bound)"
                                  if v2_met else "rejected (live_rows_v2 copy rule)"),
    ])

    shutil.rmtree(scratch, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
