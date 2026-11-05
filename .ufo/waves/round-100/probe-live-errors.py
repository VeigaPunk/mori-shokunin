#!/usr/bin/env python3
"""Pre-freeze data walk (L1, round 100): terminal-error shapes in recent OMP seat transcripts.

Reads the last <=300 KB of each *.jsonl under SESSIONS modified in the last DAYS days, takes the
last type=message record, and for stopReason=error prints COUNTS ONLY keyed by errorStatus and by
which round-99 token families (quota, rate) and round-100 auth spellings the errorMessage carries.
No message text is printed (lane redaction rule). Usage: probe-live-errors.py SESSIONS [DAYS]
"""
import collections, json, os, sys, time

QUOTA = ("quota", "usage limit", "402", "credits")
RATE = ("429", "rate_limit", "Rate limit", "rate limit", "RATE_LIMITED")
AUTH = ("permission_denied", "PERMISSION_DENIED", "unauthenticated", "UNAUTHENTICATED",
        "authentication_error", "permission_error")

root = sys.argv[1]
days = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
cut = time.time() - days * 86400
cnt = collections.Counter()
files = 0
for dp, _dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(".jsonl"):
            continue
        p = os.path.join(dp, f)
        try:
            if os.path.getmtime(p) < cut:
                continue
            with open(p, "rb") as h:
                h.seek(0, 2)
                size = h.tell()
                h.seek(max(0, size - 300000))
                text = h.read().decode("utf-8", "replace")
        except OSError:
            continue
        files += 1
        last = None
        for line in text.splitlines():
            if '"type":"message"' not in line:
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            if obj.get("type") == "message":
                last = obj.get("message") or {}
        if not last or last.get("stopReason") != "error":
            continue
        msg = last.get("errorMessage") or ""
        q = any(t in msg for t in QUOTA)
        r = last.get("errorStatus") == 429 or any(t in msg for t in RATE)
        a = last.get("errorStatus") in (401, 403) or any(t in msg for t in AUTH)
        r99 = "dead_quota" if q else "dead_rate_limit" if r else "dead_error_other"
        cnt[(last.get("errorStatus"), r99, "auth-evidence" if a else "-")] += 1
print("files_read", files, "window_days", days)
for (status, cls, auth), n in sorted(cnt.items(), key=lambda kv: -kv[1]):
    print(n, "status=%s" % status, "r99_class=%s" % cls, auth)
other_auth = sum(n for (s, c, a), n in cnt.items() if c == "dead_error_other" and a == "auth-evidence")
other = sum(n for (s, c, a), n in cnt.items() if c == "dead_error_other")
print("r99_dead_error_other", other, "of_which_auth_evidence", other_auth)
