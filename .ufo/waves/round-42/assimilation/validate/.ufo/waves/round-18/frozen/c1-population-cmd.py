#!/usr/bin/env python3
"""Round-18 C1 frozen-population enumerator (reference only, not the gate).

Usage: c1-population-cmd.py <lane-repo> <rev> <policy.json>
Prints JSON: every (path, line, class, line_sha256) hit of the frozen classes
in tracked blobs at <rev>. Read-only: git ls-tree / git cat-file only. Prints
no matched text, only SHA-256 of each hit line.
"""
import fnmatch, hashlib, json, re, subprocess, sys

repo, rev, policy_path = sys.argv[1:4]
policy = json.load(open(policy_path, encoding="utf-8"))
classes = [(c["id"], re.compile(c["regex"])) for c in policy["classes"]]


def git(*args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True).stdout


commit = git("rev-parse", "--verify", rev + "^{commit}").decode().strip()
entries = git("ls-tree", "-r", "-z", commit).split(b"\0")
hits = []
for entry in entries:
    if not entry:
        continue
    meta, path = entry.split(b"\t", 1)
    mode, kind, oid = meta.split()
    if kind != b"blob" or mode == b"160000":
        continue
    data = git("cat-file", "blob", oid.decode())
    if b"\0" in data:
        continue
    text = data.decode("utf-8", errors="replace")
    for no, line in enumerate(text.split("\n"), 1):
        for cid, rx in classes:
            if rx.search(line):
                hits.append({
                    "path": path.decode("utf-8", errors="replace"),
                    "line": no,
                    "class": cid,
                    "line_sha256": hashlib.sha256(line.encode("utf-8")).hexdigest(),
                })
non_author = policy["non_author_paths_glob"]
must = set(policy["must_redact_paths"])
summary = {
    "hits": len(hits),
    "non_author": sum(1 for h in hits if any(fnmatch.fnmatch(h["path"], g) for g in non_author)),
    "must_redact": sum(1 for h in hits if h["path"] in must),
    "files": len({h["path"] for h in hits}),
}
summary["metric_before"] = summary["hits"] - summary["non_author"]
print(json.dumps({"schema": "mori-retention-population-v1", "commit": commit,
                  "policy_sha256": hashlib.sha256(open(policy_path, "rb").read()).hexdigest(),
                  "summary": summary, "hits": hits}, indent=1))
