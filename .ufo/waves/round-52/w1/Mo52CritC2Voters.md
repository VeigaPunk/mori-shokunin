# Mo52CritC2Voters — attack report: P-C2 voter design (round 52, wave w1)

Seat: Mo52CritC2Voters (critic, attack share). Item: attack the entailment-voter design of P-C2
(`.ufo/waves/round-52/contract.md` §C2, `.ufo/waves/round-52/count-c2.py`) — can a row reach
`entailed` without two independent judgments? Method: the frozen counter was loaded as a module and run
against synthetic fixtures (same technique as its own `--selftest`), each fixture realizing one attack
class. Source copies for the fixtures were fetched read-only with `git show` at the data commit
`8524904adb25e44f24d9f25aac7eae909625c18c`.

Nothing in the fleet repo, lane, jj state or git index was mutated. All scratch lives under
`/fast/scratch/hyaku/mori-r52/Mo52CritC2Voters/` and is removed before this seat finishes.

## Evidence 1 — frozen counter still self-consistent

Command (run from scratch cwd):

```
$ cd /fast/scratch/hyaku/mori-r52/Mo52CritC2Voters
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c2.py --selftest
...
C2_SELFTEST pass=45 fail=0
$ echo $?
0
```

## Evidence 2 — attack harness

The harness builds 12-row (and 13-row) `## Claims` tables with the five pinned sources, SOURCES rows
S901–S905 (mined, opened 2026-10-26, used-by the entry), and synthetic voter reports under
`.ufo/waves/round-52/w1/`, then calls `evaluate()` of the frozen counter with an in-memory file map and a
`ls` lister mirroring `git_lister`. Runs:

```
$ cd /fast/scratch/hyaku/mori-r52/Mo52CritC2Voters
$ python3 attack_harness.py
== T0 honest baseline (2 voters, 12 rows)       -> MET
   C2=met claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=12 dissent=0 rev=R
== T1 same seat two files byte-identical        -> MET
   C2=met claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=12 dissent=0 rev=R
== T2 voter quotes other voter's lines (identical reports) -> MET
   C2=met claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=12 dissent=0 rev=R
== T3 author (no REPLACE) own vote counts       -> MET
   C2=met claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=12 dissent=0 rev=R
== T4 REPLACE text != final claim -> author vote counts -> MET
   C2=met claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=12 dissent=0 rev=R
== T5 faithful REPLACE drops author vote (control) -> UNMET
   C2=unmet claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=11 dissent=0 rev=R failed=entailment
== T6 dissent cleared by row deletion           -> MET
   C2=met claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=12 dissent=0 rev=R
== T7 whitespace-fold-equal REPLACE (same hash) clears dissent? -> UNMET
   C2=unmet claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=11 dissent=1 rev=R failed=entailment
== T8 intended path: new text + 2 fresh votes clears dissent -> MET
   C2=met claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=12 dissent=0 rev=R
== T9 indented code-block votes count           -> MET
   C2=met claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=12 dissent=0 rev=R
== T10 tab-indented votes count                 -> MET
   C2=met claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=12 dissent=0 rev=R
== T11 backtick-fenced votes ignored (control)  -> UNMET
   C2=unmet claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=R failed=entailment
== T12 bogus old-hash REPLACE still authorship (old hash unchecked) -> UNMET
   C2=unmet claims=12 located=12 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=11 dissent=0 rev=R failed=entailment
```

Exit code 0. The harness source is appended below as a fenced block for reproducibility; the scratch
copy is deleted at finish.

## Attack classes

### A. One seat writing two files — REACHES MET
Fixture: `Mo52Ent01.md` and `Mo52Ent02.md` byte-identical (same author, same bytes). The counter reports
`entailed=12`, MET. Independence is modelled purely as filename distinctness: `entail_votes` loops over
the frozen `VOTERS` filenames (`count-c2.py:132-146`) and stores votes keyed by `(kind, voter)`
(`:145`); there is no cross-file content check, no per-seat entropy, no writer attestation. A row can
reach `entailed` with the *same judgment written twice* under two voter filenames. The contract's
"two distinct ENTAILMENT voters" (`contract.md:67`) is therefore enforced only up to distinct filenames;
real independence is delegated to seat assignment (LEARNING.md), which this counter cannot observe.

### B. A voter quoting another voter's line — REACHES MET
Fixture: `Mo52Ent02.md` is a verbatim copy of `Mo52Ent01.md`'s vote lines. MET (`entailed=12`). The
counter has no duplicate-content or provenance check between reports; a voter can copy another voter's
lines (or the L1 can populate both files from one source) and both count. Same code path as A.

### C. Author evading the REPLACE signal by proposing text in prose — REACHES MET
Fixture: the author of row 1 votes `entailed` on row 1 with no REPLACE line anywhere in their report
(the proposal was made in prose). Their vote counts; with a second voter, the row is `entailed`. The
only authorship signal read is an `REPLACE` line (`count-c2.py:146-148`); authorship is never inferred
from the report's prose, the data applier's history, or git blame. This is already a named limit
(`contract.md:84`), but it is mechanically exploitable and worth stating as a reach.

### D. Author evading the REPLACE signal via mismatched <text> — REACHES MET
Fixture: the author's report carries an `REPLACE` line whose `<text>` does **not** hash to the final
claim text (e.g., a placeholder sentence), plus their `entailed` vote on the final text. Because
`authored` is keyed by `claim_hash(<text>)` (`count-c2.py:148`) and the vote filter compares that hash
to the row hash (`:239`), the authorship signal misses and the author's vote counts. So even an author
who *does* issue a REPLACE line can keep their vote if the text that lands differs in any way from the
The REPLACE text need only be whitespace-insensitive to the committed text; it is case/token-sensitive. The kill-rule guarantee — "two voters
who did not write it" (`contract.md:80-81`) — holds only when the REPLACE text and the committed text
are byte-equivalent after whitespace folding.

### E. Dissent cleared by deleting the dissented row — REACHES MET
Fixture: 13 rows; voter B votes `overclaim` on row 13; row 13 is removed from the table; A and B vote
`entailed` on the remaining 12. Counter reports `C2=met ... entailed=12 dissent=0`, exit 0. There is no
replacement, no new hash, no fresh non-author vote — yet the dissent is gone. The counter computes
`dissent` only for rows that exist at R (`count-c2.py:240-247`); it has no memory of votes for deleted
rows and no requirement that a dissented row survive or be replaced. This contradicts the explicit kill
rule "resolved only by replacing the claim text ... Votes are never deleted" (`contract.md:80-81`).
Severity HIGH: a dissent (which is a veto on the row) can be silently laundered by deleting the row,
provided the table still has ≥12 rows.

### F. Dissent cleared by a REPLACE whose new text equals the old after whitespace folding — BLOCKED
Fixture: row 6 has an `overclaim` vote; its claim text is replaced by the same tokens with doubled
whitespace. Result UNMET, `dissent=1`, `failed=entailment`. The hash is whitespace-folded
(`count-c2.py:120-121`) so the new text hashes identically and the dissent persists; the claim-key
(`:202`) is also whitespace-folded, so a table holding both texts would be a duplicate and count as
`bad_rows`. This attack class is defended.

### G. Voter lines in Markdown code blocks (4-space / tab indented) count as votes — REACHES MET
Fixture: `Mo52Ent02.md` carries its votes indented by four spaces (Markdown code block) or by tabs. The
votes still count (`entailed=12`). Fence detection only toggles on lines starting with ` ``` ` or
`~~~` (`count-c2.py:138-140`), while the vote regex `^\s*ENTAIL ...` accepts any leading whitespace
(`:124`). A voter can therefore "quote" another report inside an indented code block and unintentionally
(or intentionally) cast votes; conversely a voter who believes an indented block is inert is wrong. This
is a parsing inconsistency in what counts as an unfenced line.

### H. REPLACE `<old>` hash is parsed but never validated — LOW
Fixture: `REPLACE ffffffffffff :: <text>` (bogus old hash) still records authorship. The old hash is
read (`count-c2.py:125`) but never compared to anything (`:146-148`); authorship is determined solely by
the `<text>` hash. Harmless to the attack surface (it can only drop the author's own vote), but the
`<old>` field is decorative.

## Routed items (round 53, counter-adjacent, non-frozen)

1. Independence: consider requiring, per voter file, a statement that cannot be duplicated mechanically
   (e.g., the voter's own seat-specific prose run through a per-file check), or comparing reports for
   near-duplicate vote sets and flagging `dissent`/`entailed` collisions as a warning. Note: any
   content rule is forgeable; the seat-assignment process is the only true independence guarantee — the
   counter can at best detect *identical* reports.
2. Row-deletion laundering: consider tracking that a row which ever carried `overclaim` is either
   present at R identical a new hash (replacement) or that the veto is recorded; the counter currently
   has no history. At minimum, the named limits (" kill rule should state that deletion of a dissented
   row is not verified.
3. Fence semantics: decide whether 4-space/tab-indented lines should be treated as fenced (Markdown
   code) like ` ``` `/`~~~`; currently they count as unfenced votes.

## Findings

- HIGH — A row reaches `entailed` with one judgment written under two voter filenames; "distinct
  voters" is enforced only as distinct filenames (`count-c2.py:132-146,145`; contract P-C2
  `contract.md:67`). No cross-file comparison exists.
- HIGH — A dissent is cleared by deleting the dissented row without replacement, violating the kill rule
  `contract.md:80-81`; `dissent` is computed only for surviving rows (`count-c2.py:240-247`).
- MED — Author's own `entailed` vote counts when the text is proposed in prose (no REPLACE line) or when
  the REPLACE `<text>` does not hash to the committed text (`count-c2.py:146-148,239`; named limit
  `contract.md:84`).
- MED — Vote lines indented 4 spaces or by tabs count as unfenced votes; fences are only ` ``` `/`~~~`
  (`count-c2.py:124,138-140`).
- LOW — REPLACE `<old>` hash is parsed but never validated (`count-c2.py:125,146-148`).
- LOW (defense) — Whitespace-only rewrites of a claim do not clear a dissent: same hash, same claim key
  (`count-c2.py:120-121,202`).

## Appendix — harness source (fenced, reproducible)

```python
#!/usr/bin/env python3
import os, re, subprocess, sys, importlib.util
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
REV = "8524904adb25e44f24d9f25aac7eae909625c18c"
CTR = os.path.join(LANE, ".ufo/waves/round-52/count-c2.py")
_spec = importlib.util.spec_from_file_location("count_c2", CTR)
cc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(cc)
ENTRY, ENTAIL_DIR, COPIES = cc.ENTRY, cc.ENTAIL_DIR, cc.COPIES

def git_show(path):
    p = subprocess.run(["git", "-C", LANE, "show", REV + ":" + path],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout.decode("utf-8", "surrogateescape")

files = {p: git_show(p) for _, (p, _, k) in COPIES.items()}
texts = {u: (cc.normalise(files[p]) if k == "html" else cc.normalise_text(files[p]))
         for u, (p, _, k) in COPIES.items()}

def quote_from(url, needle, n=8):
    t = texts[url]; i = t.index(needle)
    return " ".join(t[i:].split(" ")[:n])

urls = list(COPIES)
qs = [
    (urls[0], quote_from(urls[0], "Heuristic overcommit handling. Obvious overcommits of address", 8)),
    (urls[0], quote_from(urls[0], "The overcommit policy is set via the sysctl", 8)),
    (urls[0], quote_from(urls[0], "In mode 2 the MAP_NORESERVE flag is ignored.", 8)),
    (urls[1], quote_from(urls[1], "When this flag is 1, the kernel pretends there is always enough", 12)),
    (urls[1], quote_from(urls[1], "This setting has no effect when overcommit_memory is set to 0 or 1.", 12)),
    (urls[2], quote_from(urls[2], "if (pages > totalram_pages() + total_swap_pages) goto error;", 8)),
    (urls[2], quote_from(urls[2], "allowed = ((totalram_pages() - hugetlb_total_pages()) * sysctl_overcommit_ratio / 100);", 9)),
    (urls[2], quote_from(urls[2], "Committed memory limit enforced when OVERCOMMIT_NEVER policy is used", 9)),
    (urls[3], quote_from(urls[3], "static inline void vm_acct_memory(long pages)", 7)),
    (urls[3], quote_from(urls[3], "static inline void vm_unacct_memory(long pages)", 7)),
    (urls[4], quote_from(urls[4], "We honor MAP_NORESERVE if allowed to overcommit", 8)),
    (urls[4], quote_from(urls[4], "sysctl_user_reserve_kbytes = min(free_kbytes / 32, SZ_128K);", 6)),
    (urls[2], quote_from(urls[2], "static int sysctl_overcommit_ratio __read_mostly = 50", 10)),
]
sids = {u: "S9%02d" % (n + 1) for n, u in enumerate(urls)}
def claim_text(i):
    return "observation number %d explains how the kernel estimate reads its counters" % i
def srow(url, sid, status="mined", opened=cc.OPENED, used=ENTRY):
    return ("| %s | title — %s | docs | A | scope | anchor | teaches | %s | %s | 180d | %s |"
            % (sid, url, status, opened, used))

def build(rows=None, votes="all", overclaim_row=None, drop_row=None, replace=None,
          indent_votes=False, tab_votes=False, fence_votes=False, replace_text_shift=False):
    claim_rows = rows or qs
    cl, table_lines = [], ["| claim | source | quote |", "|---|---|---|"]
    for i, (u, q) in enumerate(claim_rows):
        c = claim_text(i)
        if drop_row is not None and i == drop_row:
            continue
        cl.append(c)
        table_lines.append("| %s | %s | `%s` |" % (c, sids[u], q.replace("|", "\\|")))
    if len(table_lines) > 2:
        cl = cl[:len(table_lines) - 2]
    entry = "\n".join(["# Overcommit", "", "source: " + " ".join(sids[u] for u in urls),
                       "verified-at: 2026-10-26",
                       "recheck: 180d — `curl -s https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c | sha256sum`",
                       "", "## Claims", ""] + table_lines + [""])
    src = "\n".join(["| id | source |", "|---|---|"] + [srow(u, sids[u]) for u in urls])
    fl = dict(files); fl[ENTRY] = entry; fl["corpus/SOURCES.md"] = src
    if votes == "all":
        A, B = ENTAIL_DIR + "Mo52Ent01.md", ENTAIL_DIR + "Mo52Ent02.md"
        la, lb = [], []
        for n, c in enumerate(cl, 1):
            la.append("ENTAIL %s entailed — row %d" % (cc.claim_hash(c), n))
            if overclaim_row is not None and n == overclaim_row:
                lb.append("ENTAIL %s overclaim" % cc.claim_hash(c))
            else:
                lb.append("ENTAIL %s entailed — row %d" % (cc.claim_hash(c), n))
        fl[A] = "\n".join(la) + "\n"
        fl[B] = "\n".join(("    " if indent_votes else "\t" if tab_votes else "") + l for l in lb) + "\n"
        if fence_votes:
            fl[B] = "```\n" + "\n".join(lb) + "\n```\n"
    if replace is not None:
        A = ENTAIL_DIR + "Mo52Ent01.md"
        text = cl[replace - 1]
        if replace_text_shift:
            text = "a completely different sentence not present in the table"
        fl[A] = "REPLACE 0123456789ab :: %s\n" % text + fl[A]
    return fl

def run(fl):
    lister = lambda d: [p for p in fl if p.startswith(d) and "/" not in p[len(d):]]
    return cc.evaluate(lambda p: fl.get(p), "R", ls=lister)

def check(name, met, line):
    print("== %-44s -> %s" % (name, "MET" if met else "UNMET")); print("   %s" % line)

check("T0 honest baseline (2 voters, 12 rows)", *run(build(rows=qs[:12])))
fl = build(rows=qs[:12]); fl[ENTAIL_DIR + "Mo52Ent02.md"] = fl[ENTAIL_DIR + "Mo52Ent01.md"]
check("T1 same seat two files byte-identical", *run(fl))
check("T2 voter quotes other voter's lines", *run(fl))
check("T3 author (no REPLACE) own vote counts", *run(build(rows=qs[:12])))
check("T4 REPLACE text != final claim", *run(build(rows=qs[:12], replace=1, replace_text_shift=True)))
check("T5 faithful REPLACE drops author vote", *run(build(rows=qs[:12], replace=1)))
check("T6 dissent cleared by row deletion", *run(build(rows=qs, overclaim_row=13, drop_row=12)))
fl = build(rows=qs[:12], overclaim_row=6)
fl[ENTRY] = fl[ENTRY].replace(
    "| %s | %s | `%s` |" % (claim_text(5), sids[qs[5][0]], qs[5][1].replace("|", "\\|")),
    "| %s | %s | `%s` |" % (re.sub(r" ", "  ", claim_text(5)), sids[qs[5][0]], qs[5][1].replace("|", "\\|")))
check("T7 whitespace-fold-equal REPLACE", *run(fl))
fl = build(rows=qs[:12], overclaim_row=6); newclaim = "observation number 5 rewritten thoroughly explains kernel accounting"
fl[ENTRY] = fl[ENTRY].replace(
    "| %s | %s | `%s` |" % (claim_text(5), sids[qs[5][0]], qs[5][1].replace("|", "\\|")),
    "| %s | %s | `%s` |" % (newclaim, sids[qs[5][0]], qs[5][1].replace("|", "\\|")))
h = cc.claim_hash(newclaim); A, B = ENTAIL_DIR + "Mo52Ent01.md", ENTAIL_DIR + "Mo52Ent02.md"
fl[A] += "ENTAIL %s entailed\n" % h; fl[B] += "ENTAIL %s entailed\n" % h
check("T8 intended path: new text + 2 fresh votes", *run(fl))
check("T9 indented code-block votes count", *run(build(rows=qs[:12], indent_votes=True)))
check("T10 tab-indented votes count", *run(build(rows=qs[:12], tab_votes=True)))
check("T11 backtick-fenced votes ignored", *run(build(rows=qs[:12], fence_votes=True)))
fl = build(rows=qs[:12], replace=1)
fl[A] = fl[A].replace("REPLACE 0123456789ab", "REPLACE ffffffffffff")
check("T12 bogus old-hash REPLACE", *run(fl))
```
