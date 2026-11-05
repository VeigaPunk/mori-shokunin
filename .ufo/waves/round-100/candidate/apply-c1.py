#!/usr/bin/env python3
"""Round-100 C1 transform: apply the frozen candidate to a lane tree DIR (in place).

Copies candidate/tools/{mori-seat-terminal.py,mori-round17-seat-regressions.py} and
candidate/corpus/knowledge/seat-auth-deaths-r100.md, appends registry rows S637/S638 after S636,
adds the entry to S221 used-by, and edits the two SKILL.md registry rows. Each text edit asserts
exactly one match. Parts can be skipped (--skip tools,gate,knowledge,rows,skill) to build controls.
Usage: apply-c1.py DIR [--skip a,b]
"""
import argparse, pathlib, re, shutil, sys

HERE = pathlib.Path(__file__).resolve().parent
ENTRY = "corpus/knowledge/seat-auth-deaths-r100.md"

ROW_S637 = (
    "| S637 | Connect protocol reference — https://connectrpc.com/docs/protocol/ — pinned copy "
    "`corpus/evidence/sources-r100/S637-connect-protocol.html` | spec | A | the Connect error-code "
    "spellings a provider stream error carries, the code-choice rule between unauthenticated, "
    "permission_denied and resource_exhausted, and the HTTP-to-code mapping | Error Codes table (raw line "
    "637), code-choice paragraph (raw lines 645-650), HTTP to Error Code table (raw line 711) of the pinned "
    "copy; fetched 2026-11-05T23:00:13Z, HTTP 200, 148033 bytes, sha256 "
    "55d644c62a7d094ec836dbc4f9fbcb1f5b0cca27b675ba68902568fef9ca2578; quote \"use unauthenticated if the "
    "user can’t be identified or presents invalid credentials.\" (12 words, raw lines 646-647) | a "
    "lowercase permission_denied or unauthenticated in a provider error is an auth refusal, while a per-user "
    "quota is resource_exhausted, so a death classifier reads auth spellings only after quota evidence "
    "| mined | 2026-11-05 | 180d | " + ENTRY + " |"
)
ROW_S638 = (
    "| S638 | gRPC status codes — https://grpc.github.io/grpc/core/md_doc_statuscodes.html — pinned copy "
    "`corpus/evidence/sources-r100/S638-grpc-statuscodes.html` | spec | A | what PERMISSION_DENIED and "
    "UNAUTHENTICATED mean and what they must not be used for | status-code table rows PERMISSION_DENIED "
    "(raw line 88), RESOURCE_EXHAUSTED (raw line 90), UNAUTHENTICATED (raw line 106) of the pinned copy; "
    "fetched 2026-11-05T23:00:13Z, HTTP 200, 18133 bytes, sha256 "
    "95459b760813d4cde87ad3c449753ff55bbd138cdf6c5bfdfacf6566b763e3c4; quote \"PERMISSION_DENIED must "
    "not be used for rejections caused by exhausting some resource\" (12 words, raw line 88) | an "
    "auth-coded death is never a quota death: explicit exhaustion evidence wins over a permission "
    "spelling, and UNAUTHENTICATED is the missing-credential case | mined | 2026-11-05 | 180d | "
    + ENTRY + " |"
)

SKILL_SEAT_OLD = (
    "| 0 no aged error found, not health · 1 `MORI_SEAT_TERMINAL_DEAD` (aged last-error observations, not "
    "permanent deaths/incidents) · 2 `MORI_SEAT_TERMINAL_SETUP`; inspect unavailable/incomplete/unsettled "
    "totals | `python3 tools/mori-seat-terminal.py --selftest` |"
)
SKILL_SEAT_NEW = (
    "| 0 no aged error found, not health · 1 `MORI_SEAT_TERMINAL_DEAD` (aged last-error observations, not "
    "permanent deaths/incidents) · 2 `MORI_SEAT_TERMINAL_SETUP`; inspect unavailable/incomplete/unsettled "
    "totals; dead classes (r100) `dead_quota` · `dead_rate_limit` · `dead_auth` (HTTP 401/403 or an auth "
    "code spelling, read after quota and rate evidence; `corpus/knowledge/seat-auth-deaths-r100.md`) · "
    "`dead_error_other` | `python3 tools/mori-seat-terminal.py --selftest` (53 arms at round 100, "
    "`auth-*` arms included) |"
)
SKILL_GATE_OLD = (
    "| `python3 tools/mori-round17-seat-regressions.py --selftest` (TMPDIR required, not /tmp) |"
)
SKILL_GATE_NEW = (
    "| `python3 tools/mori-round17-seat-regressions.py --selftest` (TMPDIR required, not /tmp); the class "
    "set carries `dead_auth` since round 100, so the gate refuses a tool without it (`totals_keys`) |"
)


def replace_once(text, old, new, what):
    n = text.count(old)
    if n != 1:
        sys.exit("apply-c1: %s matched %d times" % (what, n))
    return text.replace(old, new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--skip", default="")
    a = ap.parse_args()
    d = pathlib.Path(a.dir)
    skip = set(filter(None, a.skip.split(",")))
    if "tools" not in skip:
        shutil.copyfile(HERE / "tools/mori-seat-terminal.py", d / "tools/mori-seat-terminal.py")
    if "gate" not in skip:
        shutil.copyfile(HERE / "tools/mori-round17-seat-regressions.py",
                        d / "tools/mori-round17-seat-regressions.py")
    if "knowledge" not in skip:
        shutil.copyfile(HERE / ENTRY, d / ENTRY)
    if "rows" not in skip:
        p = d / "corpus/SOURCES.md"
        lines = p.read_text(encoding="utf-8").split("\n")
        idx = [i for i, l in enumerate(lines) if re.match(r"^ {0,3}\| *S636 *\|", l)]
        if len(idx) != 1:
            sys.exit("apply-c1: S636 row matched %d times" % len(idx))
        lines[idx[0] + 1:idx[0] + 1] = [ROW_S637, ROW_S638]
        s221 = [i for i, l in enumerate(lines) if re.match(r"^ {0,3}\| *S221 *\|", l)]
        if len(s221) != 1 or not lines[s221[0]].endswith("corpus/knowledge/source-drift-hardening-r37.md |"):
            sys.exit("apply-c1: S221 row shape unexpected")
        lines[s221[0]] = lines[s221[0]][:-2] + ", " + ENTRY + " |"
        p.write_text("\n".join(lines), encoding="utf-8")
    if "skill" not in skip:
        p = d / "SKILL.md"
        t = p.read_text(encoding="utf-8")
        t = replace_once(t, SKILL_SEAT_OLD, SKILL_SEAT_NEW, "SKILL seat row")
        t = replace_once(t, SKILL_GATE_OLD, SKILL_GATE_NEW, "SKILL gate row")
        p.write_text(t, encoding="utf-8")
    print("apply-c1: applied, skipped=%s" % (",".join(sorted(skip)) or "-"))


if __name__ == "__main__":
    main()
