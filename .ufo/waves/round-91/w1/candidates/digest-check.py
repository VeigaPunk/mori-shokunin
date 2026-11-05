#!/usr/bin/env python3
"""digest-check.py — verify recorded sha256 digests in a mori corpus/SOURCES.md
registry against the pinned source copies the rows name.

Usage: python3 digest-check.py <SOURCES.md> <pinned-dir>

Scope: every registry row that BOTH names a pinned copy AND records a sha256
in the row's anchor or source cell.  A row is out of scope when it records no
usable copy digest or names no pinned copy.

Per in-scope row one line is printed:

    DIGEST <id> ok|mismatch|prefix-only|unpinned recorded=<value> actual=<sha256>

Final line:

    DIGEST_CHECK rows=<n> ok=<a> mismatch=<b> prefix_only=<c> unpinned=<d>

Exit: 0 only when mismatch=0 and prefix_only=0 and unpinned=0; 1 when any row
is mismatch/prefix-only/unpinned; 2 on setup error.

Pair classification (recorded vs the copy file's full sha256):
  ok           recorded equals actual exactly (64-hex)
  prefix-only  recorded is a strict prefix of actual and actual startswith it
  mismatch     anything else (including a same-length value that differs, and
               a truncated recorded value that is NOT a prefix of actual)
  unpinned     a named pinned copy does not resolve to a file, or "the pinned
               copy" cannot be resolved to a unique file under <pinned-dir>

Per-row verdict: mismatch if any pair mismatches; else prefix-only if any pair
is prefix-only; else ok; unpinned when no pair could be evaluated because a
named copy is missing.

Copy references recognised:
  * repo-relative paths under corpus/evidence/ or .ufo/waves/ (the pinned-copy
    locations), plus any corpus/ or .ufo/ path appearing in a copy/receipt/
    extract/pinned-copy clause;
  * directory paths expand to the regular files they contain;
  * "same page bytes as S<n>" / "same bytes as S<n>" inherits the referenced
    row's copy paths;
  * "the pinned copy" / "pinned copy" with no path resolves by searching
    <pinned-dir> recursively, disambiguated by the row's recorded byte count,
    then by longest common prefix with the recorded digest.

Recorded digests: `sha256`/`SHA-256` labelled hex of 8-64 chars, or a bare
64-hex token, in the row's source or anchor cell.  Digests attributed in their
own clause to a non-copy artifact ("script SHA-256", "git blob", "entry
bytes", "tarball") are ignored.  Each digest is paired with the nearest copy
reference; inside a directory copy the pairing uses the byte count recorded
adjacent to the digest.  Copy files that no digest pairs with are not checked
and are listed by the caller's report, not here.

Paths under ../ or owner/repo/ prefixes are not treated as local copies.

TMPDIR is honoured trivially (no temp files are created); the checker writes
only to stdout/stderr.
"""

import hashlib
import os
import re
import sys

ROW_RE = re.compile(r"^\|\s*(S\d+)\s*\|")
# repo-relative path under corpus/ or .ufo/; lookbehind rejects ../x,
# owner/repo/x and mid-token hits
PATH_RE = re.compile(r"(?<![\w/.-])((?:corpus|\.ufo)/[A-Za-z0-9_./~%\-]+)")
HEX64_RE = re.compile(r"\b[0-9a-f]{64}\b")
LAB_RE = re.compile(r"sha-?256\s*[:=]?\s*`?([0-9a-fA-F]{8,64})", re.I)
BYTES_RE = re.compile(r"([0-9][0-9,]*)\s*(?:bytes|B)\b")
SAME_AS_RE = re.compile(r"same (?:page )?bytes as (S\d+)", re.I)
PINNED_PHRASE_RE = re.compile(r"\b(?:the\s+)?pinned copy\b|\bPINNED copy\b", re.I)
COPY_KW_RE = re.compile(
    r"\b(copy|copies|committed copy|copy unchanged|extract|receipt|receipts|"
    r"pinned copy|pin)\b", re.I)
PINNED_LOC_RE = re.compile(r"(?:corpus/evidence/|\.ufo/waves/)")
NONCOPY_ATTR_RE = re.compile(
    r"(?:script|git blob|entry bytes|tarball)\b[^;]{0,80}sha-?256|"
    r"sha-?256[^;]{0,80}\b(?:script|git blob|entry bytes|tarball)\b",
    re.I)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_rows(path):
    rows = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = ROW_RE.match(line)
            if not m:
                continue
            cells = [c.strip() for c in line.split("|")]
            sid = cells[1]
            source = cells[2] if len(cells) > 2 else ""
            anchor = cells[6] if len(cells) > 6 else ""
            rows.append({"id": sid, "source": source, "anchor": anchor,
                         "text": source + "\n" + anchor})
    return rows


def clean_path(p):
    return re.sub(r"[.,;:)\'\"`/]+$", "", p)


def extract_copy_paths(text):
    """Ordered unique (path, is_copy_ref) repo-relative mentions.

    is_copy_ref is True when the path sits in a pinned-copy location
    (corpus/evidence/, .ufo/waves/) or its clause carries a copy keyword.
    """
    out = []
    seen = set()
    clauses = re.split(r";", text)
    pos = 0
    clause_spans = []
    for clause in clauses:
        start = text.find(clause, pos)
        clause_spans.append((start, start + len(clause), clause))
        pos = start + len(clause)
    for m in PATH_RE.finditer(text):
        p = clean_path(m.group(1))
        if not p or p in seen:
            continue
        seen.add(p)
        is_copy = bool(PINNED_LOC_RE.search(p))
        if not is_copy:
            for s, e, clause in clause_spans:
                if s <= m.start() < e and COPY_KW_RE.search(clause):
                    is_copy = True
                    break
        out.append((p, is_copy))
    return out


def extract_digests(text):
    """Ordered unique (digest, exempt) recorded digests."""
    found = []
    seen = set()
    pos = 0
    for clause in re.split(r";", text):
        cstart = text.find(clause, pos)
        pos = cstart + len(clause)
        exempt = bool(NONCOPY_ATTR_RE.search(clause))
        covered = []
        for m in LAB_RE.finditer(clause):
            h = m.group(1).lower()
            covered.append(m.span())
            if h not in seen:
                seen.add(h)
                found.append((h, exempt))
        for m in HEX64_RE.finditer(clause):
            if any(s <= m.start() < e for s, e in covered):
                continue
            h = m.group(0).lower()
            if h not in seen:
                seen.add(h)
                found.append((h, exempt))
    return found


def byte_counts_near(text, digest_pos, window=160):
    """Byte counts recorded within `window` chars after a digest position."""
    seg = text[digest_pos:digest_pos + window]
    return [int(m.group(1).replace(",", ""))
            for m in BYTES_RE.finditer(seg)]


def resolve_path(rel, roots):
    """Resolve a repo-relative path against roots; returns (files, missing).

    files: existing regular files (directories expanded one level, sorted).
    missing: True when no root yielded anything.
    """
    files = []
    for root in roots:
        full = os.path.join(root, rel)
        if os.path.isfile(full):
            files.append(full)
        elif os.path.isdir(full):
            try:
                for name in sorted(os.listdir(full)):
                    p = os.path.join(full, name)
                    if os.path.isfile(p):
                        files.append(p)
            except OSError:
                pass
    seen = set()
    uniq = []
    for f in files:
        if f not in seen:
            seen.add(f)
            uniq.append(f)
    return uniq, not uniq


def list_files_recursive(directory):
    out = []
    for dirpath, _dn, filenames in os.walk(directory):
        for name in sorted(filenames):
            p = os.path.join(dirpath, name)
            if os.path.isfile(p):
                out.append(p)
    return out


def common_prefix_len(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def pair_verdict(recorded, actual):
    if recorded == actual:
        return "ok"
    if len(recorded) < len(actual) and actual.startswith(recorded):
        return "prefix-only"
    return "mismatch"


def combine(verdicts, missing_copies):
    if missing_copies:
        return "unpinned"
    if not verdicts:
        return "unpinned"
    if any(v == "mismatch" for v in verdicts):
        return "mismatch"
    if any(v == "prefix-only" for v in verdicts):
        return "prefix-only"
    return "ok"


def main(argv):
    if len(argv) != 3:
        print("usage: digest-check.py <SOURCES.md> <pinned-dir>", file=sys.stderr)
        return 2
    sources_md = os.path.abspath(argv[1])
    pinned_dir = os.path.abspath(argv[2])
    if not os.path.isfile(sources_md):
        print("setup: SOURCES.md not found: %s" % sources_md, file=sys.stderr)
        return 2
    if not os.path.isdir(pinned_dir):
        print("setup: pinned dir not found: %s" % pinned_dir, file=sys.stderr)
        return 2

    md_dir = os.path.dirname(sources_md)
    repo_root = os.path.dirname(md_dir) if os.path.basename(md_dir) == "corpus" else md_dir
    roots = [repo_root, pinned_dir, md_dir]

    try:
        rows = parse_rows(sources_md)
    except OSError as exc:
        print("setup: cannot read %s: %s" % (sources_md, exc), file=sys.stderr)
        return 2
    if not rows:
        print("setup: no registry rows found in %s" % sources_md, file=sys.stderr)
        return 2
    by_id = {r["id"]: r for r in rows}
    pinned_files = list_files_recursive(pinned_dir)

    counts = {"ok": 0, "mismatch": 0, "prefix-only": 0, "unpinned": 0}
    n_rows = 0

    for row in rows:
        sid = row["id"]
        text = row["text"]
        digests = [(h, ex) for h, ex in extract_digests(text) if not ex]
        if not digests:
            continue

        path_mentions = extract_copy_paths(text)
        copy_paths = [p for p, is_copy in path_mentions if is_copy]
        same_as = SAME_AS_RE.search(text)
        has_pinned_phrase = bool(PINNED_PHRASE_RE.search(text))

        # "same bytes as S<n>" inherits the target row's copy paths
        inherited_paths = []
        if same_as:
            target = by_id.get(same_as.group(1))
            if target is not None:
                inherited_paths = [p for p, ic in extract_copy_paths(target["text"]) if ic]

        all_refs = list(dict.fromkeys(copy_paths + inherited_paths))
        resolved = {}   # rel -> [files]
        missing = []    # rel paths that resolve nowhere
        for rel in all_refs:
            files, miss = resolve_path(rel, roots)
            if miss:
                missing.append(rel)
            else:
                resolved[rel] = files

        # "the pinned copy" with no explicit path: search pinned-dir
        pinned_files_for_row = []
        if has_pinned_phrase and not all_refs:
            sizes = set()
            for m in BYTES_RE.finditer(text):
                sizes.add(int(m.group(1).replace(",", "")))
            rec = [h for h, _ in digests]
            scored = []
            for f in pinned_files:
                try:
                    sz = os.path.getsize(f)
                except OSError:
                    continue
                score = None
                if sizes and sz in sizes:
                    score = (2, 0)
                else:
                    try:
                        act = sha256_file(f)
                    except OSError:
                        continue
                    cpl = max(common_prefix_len(h, act) for h in rec)
                    if cpl >= 8:
                        score = (1, cpl)
                if score is not None:
                    scored.append((score, f))
            if scored:
                best = max(s for s, _ in scored)
                cands = [f for s, f in scored if s == best]
                if len(set(cands)) == 1:
                    pinned_files_for_row = cands
                else:
                    missing.append("<ambiguous pinned copy>")
            else:
                missing.append("<unpinned copy>")

        # nothing names a pinned copy -> out of scope
        if not all_refs and not pinned_files_for_row and not missing:
            continue
        if not all_refs and not pinned_files_for_row and missing:
            # pinned phrase present but unresolvable, or only missing refs
            pass

        # pair each digest with the nearest copy reference (file or rel path)
        # build list of (position_hint, files) — position via nearest path mention
        pair_targets = []  # list of (rel_or_None, [files])
        for rel in all_refs:
            if rel in resolved:
                pair_targets.append((rel, resolved[rel]))
        for f in pinned_files_for_row:
            pair_targets.append((None, [f]))

        verdicts = []
        shown_rec = []
        shown_act = []

        # locate each digest's position in text for nearest-path pairing
        digest_positions = []
        for h, _ex in digests:
            idx = text.find(h)
            digest_positions.append((h, idx if idx >= 0 else len(text)))

        # path mention positions for nearest pairing
        path_positions = []
        for p, _ic in path_mentions:
            if p in all_refs:
                idx = text.find(p)
                path_positions.append((p, idx if idx >= 0 else len(text)))

        evaluated = set()
        for h, dpos in digest_positions:
            # candidate targets: explicit resolved paths nearest to digest
            best_rel = None
            best_dist = None
            for p, ppos in path_positions:
                if p not in resolved:
                    continue
                d = abs(ppos - dpos)
                if best_dist is None or d < best_dist:
                    best_dist = d
                    best_rel = p
            targets = []
            if best_rel is not None:
                targets = resolved[best_rel]
            elif path_positions:
                # explicit paths exist but none resolved -> nothing to pair
                continue
            else:
                # no explicit path mention in this row's text (e.g. inherited
                # "same bytes as S<n>" or pinned-phrase resolution): pair the
                # digest with every resolved/inherited/pinned file
                for rel in all_refs:
                    targets.extend(resolved.get(rel, []))
                targets.extend(pinned_files_for_row)
            if len(targets) > 1:
                sizes = byte_counts_near(text, dpos)
                sized = []
                for f in targets:
                    try:
                        if os.path.getsize(f) in sizes:
                            sized.append(f)
                    except OSError:
                        pass
                if len(sized) == 1:
                    targets = sized
                else:
                    # fall back: pair digest with every target file
                    pass
            for f in targets:
                key = (h, f)
                if key in evaluated:
                    continue
                evaluated.add(key)
                try:
                    act = sha256_file(f)
                except OSError:
                    verdicts.append("unpinned")
                    continue
                verdicts.append(pair_verdict(h, act))
                shown_rec.append(h)
                shown_act.append(act)

        row_verdict = combine(verdicts, missing)
        rec_show = shown_rec[0] if shown_rec else (digests[0][0] if digests else "-")
        act_show = shown_act[0] if shown_act else "-"
        print("DIGEST %s %s recorded=%s actual=%s"
              % (sid, row_verdict, rec_show, act_show))
        counts[row_verdict] += 1
        n_rows += 1

    print("DIGEST_CHECK rows=%d ok=%d mismatch=%d prefix_only=%d unpinned=%d"
          % (n_rows, counts["ok"], counts["mismatch"],
             counts["prefix-only"], counts["unpinned"]))
    if counts["mismatch"] or counts["prefix-only"] or counts["unpinned"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
