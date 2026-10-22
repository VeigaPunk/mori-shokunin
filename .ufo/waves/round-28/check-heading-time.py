#!/usr/bin/env python3
"""Round 28, QUALITY 83 check: a dated heading in a contract is never future-dated against the commit that ships it.

Reads committed bytes only. The contract file and every commit timestamp come from git objects at <rev>; the
working tree is never read. For each dated heading the check finds the commit that added that exact line
(`git log --reverse -S<line> -- <path>`) and compares the stated time with that commit's own timestamps.

The bound is the commit's COMMITTER time: that is the instant the commit carrying the text exists in history.
The AUTHOR time is not the bound. In this jj-colocated lane the author time is when the empty change was
opened, not when its content was written, so an honest heading can state a time later than the author time;
keying the check to the author time therefore fails correct text (see the r17 A1 heading, stated 2026-10-20
~16:10, shipped by a commit with author time 15:26:13-03:00 and committer time 16:31:56-03:00).

Granularity. A heading that states a full instant with an explicit zone (Z or +hh:mm) is compared at second
granularity. A heading that states only a date is compared by calendar day against the shipping commit's own
local date, because a bare date claims no second. A heading that states a local clock time with no zone
(prefixed "~") is compared at minute granularity in the commit's own local offset, because such a stamp has no
zone but does claim a minute.

Usage: python3 -I -B .ufo/waves/round-28/check-heading-time.py <rev> <file> [--heading <substring>] [--bound cI|aI]
Prints one line per dated heading and a summary `headings=<n> future_dated=<k>`.
Exit 0 when no heading is future-dated, 1 when one is, 2 on a bad revision, a missing file or a usage error.
"""
import datetime
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
STAMP = re.compile(
    r"(?P<y>\d{4})-(?P<mo>\d{2})-(?P<d>\d{2})"
    r"(?:(?:(?:[T ])?~|[T ])(?P<h>\d{2}):(?P<mi>\d{2})(?::(?P<s>\d{2}))?"
    r"(?P<z>Z|[+-]\d{2}:?\d{2})?)?")
HEAD = re.compile(r"^#{2,6} .*$")


def git(*args):
    return subprocess.run(["git", "-C", LANE] + list(args), capture_output=True, text=True)


def parse_iso(text):
    """Parse a git ISO-8601 timestamp into an aware datetime."""
    t = text.strip()
    if t.endswith("Z"):
        t = t[:-1] + "+00:00"
    return datetime.datetime.fromisoformat(t)


def stated_times(line):
    """Every timestamp a heading states, with the granularity it states it at."""
    out = []
    for m in STAMP.finditer(line):
        y, mo, d = int(m.group("y")), int(m.group("mo")), int(m.group("d"))
        hh, mi, ss = m.group("h"), m.group("mi"), m.group("s")
        z = m.group("z")
        if hh is None:
            out.append((m.group(0), "day", datetime.date(y, mo, d)))
            continue
        if z == "Z":
            tz = datetime.timezone.utc
        elif z:
            z = z.replace(":", "")
            sign = 1 if z[0] == "+" else -1
            tz = datetime.timezone(sign * datetime.timedelta(hours=int(z[1:3]), minutes=int(z[3:5])))
        else:
            tz = None
        moment = datetime.datetime(y, mo, d, int(hh), int(mi), int(ss or 0), tzinfo=tz)
        if tz is None:
            out.append((m.group(0), "local-minute", moment.replace(tzinfo=None)))
        else:
            out.append((m.group(0), "instant", moment))
    return out


def adding_commit(rev, path, line):
    """The commit that added this exact line, with its author and committer times."""
    r = git("log", "--reverse", "--format=%H %aI %cI", "-S" + line, rev, "--", path)
    rows = [x for x in r.stdout.strip().split("\n") if x]
    if not rows:
        return None
    sha, a, c = rows[0].split(" ", 2)
    return sha, a, c


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("usage: check-heading-time.py <rev> <file> [--heading <substring>] [--bound cI|aI]")
        return 2
    rev, path = args[0], args[1]
    only = None
    bound_kind = "cI"
    rest = args[2:]
    i = 0
    while i < len(rest):
        if rest[i] == "--heading" and i + 1 < len(rest):
            only = rest[i + 1]
            i += 2
        elif rest[i] == "--bound" and i + 1 < len(rest):
            if rest[i + 1] not in ("cI", "aI"):
                print("bad_bound")
                return 2
            bound_kind = rest[i + 1]
            i += 2
        else:
            print("bad_arg " + rest[i])
            return 2
    r = git("rev-parse", "--verify", "-q", rev + "^{commit}")
    if r.returncode != 0:
        print("bad_rev")
        return 2
    rev = r.stdout.strip()
    show = git("show", "%s:%s" % (rev, path))
    if show.returncode != 0:
        print("missing_file")
        return 2
    headings = [(n, l) for n, l in enumerate(show.stdout.split("\n"), 1)
                if HEAD.match(l) and STAMP.search(l)]
    if only is not None:
        headings = [(n, l) for n, l in headings if only in l]
    total = 0
    future = 0
    for n, line in headings:
        stamps = stated_times(line)
        if not stamps:
            continue
        added = adding_commit(rev, path, line)
        if added is None:
            print("no_adding_commit %s:%d" % (path, n))
            future += 1
            total += 1
            continue
        sha, a, c = added
        bound = parse_iso(c if bound_kind == "cI" else a)
        for text, kind, value in stamps:
            total += 1
            if kind == "instant":
                ok = value <= bound
                delta = int((bound - value).total_seconds())
            elif kind == "local-minute":
                local = bound.astimezone(bound.tzinfo).replace(tzinfo=None)
                ok = value <= local
                delta = int((local - value).total_seconds())
            else:
                ok = value <= bound.date()
                delta = 0
            if not ok:
                future += 1
            print("heading %s:%d stated=%s granularity=%s added_by=%s aI=%s cI=%s bound=%s delta_s=%d verdict=%s"
                  % (path, n, text, kind, sha[:12], a, c, bound.isoformat(), delta,
                     "ok" if ok else "FUTURE-DATED"))
    print("headings=%d future_dated=%d" % (total, future))
    return 1 if future else 0


if __name__ == "__main__":
    sys.exit(main())
