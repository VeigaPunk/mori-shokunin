# Mo52ExecC2Replay — round 52 w1: C2 replay, hash comparison, five in-memory variants

Seat: `Mo52ExecC2Replay` (leaf executor, no subagents dispatched). Scored revision:
`8524904adb25e44f24d9f25aac7eae909625c18c` (the round-52 data commit; entry blob
`corpus/knowledge/overcommit-commit-limit-r52.md` = `7cec492566f5c93cf13829c0298d8b3f1a034466671120534ac3838bae656447`).
Lane tip seen while running: `075436b1` ("round-52: wave w1 spec …, receipts at data"). Contract read from
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/contract.md`.
Scratch for every run: `/fast/scratch/hyaku/mori-r52/Mo52ExecC2Replay/` with
`TMPDIR=/fast/scratch/hyaku/mori-r52/Mo52ExecC2Replay/tmp`; all runs `cd` into it first.

## 1. Receipts — frozen counter, unmodified

The counter was executed from the lane (its frozen bytes), not from a copy:

```
$ cd /fast/scratch/hyaku/mori-r52/Mo52ExecC2Replay
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c2.py 8524904adb25e44f24d9f25aac7eae909625c18c
C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment
exit=1

$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c2.py --hashes 8524904adb25e44f24d9f25aac7eae909625c18c
row=1 hash=9afaa81505da claim=Mode 0 is the default and refuses only allocations that are plainly too large, so it still lets the host overcommit.
… (28 row lines, see §2 for the byte comparison)
exit=0

$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c2.py --selftest
PASS honest_met
PASS entry_absent_unmet
PASS no_table_unmet
PASS altered_quote_unmet
PASS quote_from_wrong_copy_unmet
PASS short_quote_unmet
PASS long_quote_unmet
PASS duplicate_quote_unmet
PASS claims_floor_unmet
PASS sources_floor_unmet
PASS row_not_mined_unmet
PASS row_opened_other_day_unmet
PASS used_by_missing_unmet
PASS indented_row_ok
PASS code_indented_row_unmet
PASS pin_mismatch_unmet
PASS table_id_uncited_in_source_unmet
PASS verified_at_missing_unmet
PASS header_wrong_unmet
PASS claim_cell_short_unmet
PASS breadcrumb_identical_claims_unmet
PASS claim_echoes_quote_unmet
PASS table_inside_fence_unseen_unmet
PASS other_entry_path_unmet
PASS entail_no_votes_unmet
PASS entail_one_voter_unmet
PASS entail_same_voter_twice_unmet
PASS entail_one_row_single_vote_unmet
PASS entail_dissent_unmet
PASS entail_l1_file_ignored_unmet
PASS entail_non_voter_seat_ignored_unmet
PASS entail_voter_outside_list_ignored_unmet
PASS entail_non_md_ignored_unmet
PASS entail_other_dir_ignored_unmet
PASS entail_fenced_votes_ignored_unmet
PASS entail_fenced_dissent_ignored_met
PASS entail_non_voter_dissent_ignored_met
PASS entail_author_vote_not_counted_unmet
PASS entail_author_plus_two_others_met
PASS entail_fenced_replace_not_authorship_met
PASS entail_hash_of_other_text_unmet
PASS entail_hash_whitespace_folded_met
PASS voters_frozen
PASS words_beyond_counts
PASS text_copy_keeps_angle_brackets
C2_SELFTEST pass=45 fail=0
exit=0
```

The at-data receipt `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/evidence/c2-at-data.txt`
(`sha256 b3a9b50b4014df3f8088c97682c7a112b6aa2c2dd2d38b26fbb66788e121c9de`) records the same command and the same
verdict line; my run reproduces it character for character. Counter bytes match the freeze manifest:

```
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c2.py
0a9ec2ffdd85dd1a2be13f359ad82c0f45f99b781d73f9bcf3fa098d7f3bb74a  …/.ufo/waves/round-52/count-c2.py
$ grep count-c2 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/evidence/freeze-sha256.txt
0a9ec2ffdd85dd1a2be13f359ad82c0f45f99b781d73f9bcf3fa098d7f3bb74a  .ufo/waves/round-52/count-c2.py
```

The module-import work in §3 used a byte-identical scratch copy (`cp` then `sha256sum`, both
`0a9ec2ffdd85dd1a2be13f359ad82c0f45f99b781d73f9bcf3fa098d7f3bb74a`), so importing it cannot create a
`__pycache__` inside the frozen wave directory of the lane.

## 2. Hash comparison against `evidence/c2-hashes-at-data.txt`

```
$ python3 …/count-c2.py --hashes 8524904adb… > hashes-live.txt      # exit=0
$ grep -E '^row=' hashes-live.txt > hashes-live.rows
$ grep -E '^row=' …/evidence/c2-hashes-at-data.txt > hashes-receipt.rows
$ cmp hashes-live.rows hashes-receipt.rows
(no output) exit=0
$ wc -l < hashes-live.rows
28
$ sha256sum hashes-live.rows hashes-receipt.rows
80a2a41fe2b71cf6f352d0228f82cbcf2736c01b372adbcd1ff313bc8cdc7247  hashes-live.rows
80a2a41fe2b71cf6f352d0228f82cbcf2736c01b372adbcd1ff313bc8cdc7247  hashes-receipt.rows
```

All 28 row hashes and claim texts are byte-identical to the receipt. The entry's row count is 28 at R, which is the
`claims=28` in every verdict line below.

## 3. Five in-memory variants of the entry, scored by the imported counter

The counter's `evaluate(read, rev, entry_path, copies, ls)` takes injectable `read`/`ls`, so every variant is scored
inside one process: entry bytes, `corpus/SOURCES.md` and the five frozen copies come from
`git -C <lane> show 8524904adb…:<path>`, and voter reports are synthesized in memory. No file in the lane is written
and no fixture repository is needed. The harness as run (scratch path, removed afterwards):

```python
#!/usr/bin/env python3
"""Score in-memory variants of the round-52 C2 entry with the frozen counter imported as a module."""
import importlib.util
import os
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
REV = "8524904adb25e44f24d9f25aac7eae909625c18c"
SCRATCH = "/fast/scratch/hyaku/mori-r52/Mo52ExecC2Replay"

spec = importlib.util.spec_from_file_location("countc2", os.path.join(SCRATCH, "count-c2.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def git_show(path):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (REV, path)],
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=120)
    return p.stdout.decode("utf-8", "surrogateescape") if p.returncode == 0 else None


BASE = {m.ENTRY: git_show(m.ENTRY), "corpus/SOURCES.md": git_show("corpus/SOURCES.md")}
for url, (path, digest, kind) in m.COPIES.items():
    BASE[path] = git_show(path)

p = subprocess.run(["git", "-C", LANE, "ls-tree", "--name-only", REV, m.ENTAIL_DIR],
                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=60)
print("w1 files at data commit: %r" % ([x for x in p.stdout.decode().split("\n") if x],))

entry_text = BASE[m.ENTRY]
header, rows = m.parse_claims(entry_text)
assert header == ["claim", "source", "quote"], header
assert len(rows) == 28, len(rows)
lines = entry_text.split("\n")
hashes = [m.claim_hash(c[0]) for c in rows]
row_idx = []
for c in rows:
    hits = [i for i, l in enumerate(lines) if l.lstrip().startswith("| " + c[0])]
    assert len(hits) == 1, (c[0][:40], hits)
    row_idx.append(hits[0])


def make_io(entry=entry_text, votes=None):
    files = dict(BASE)
    files[m.ENTRY] = entry
    listing = []
    for voter, vlines in (votes or {}).items():
        path = m.ENTAIL_DIR + voter + ".md"
        files[path] = "# %s\n\n%s\n" % (voter, "\n".join(vlines))
        listing.append(path)
    return (lambda path: files.get(path), lambda d: listing if d == m.ENTAIL_DIR else [])


def score(label, **kw):
    read, ls = make_io(**kw)
    met, line = m.evaluate(read, REV, entry_path=m.ENTRY, ls=ls)
    print("%-34s exit=%d %s" % (label, 0 if met else 1, line))
    return met, line


def entry_without(indices, replacement=None):
    out = list(lines)
    for i in indices:
        out[i] = replacement if replacement is not None else None
    return "\n".join(l for l in out if l is not None)


honest = {"Mo52Ent01": ["ENTAIL %s entailed" % h for h in hashes],
          "Mo52Ent02": ["ENTAIL %s entailed" % h for h in hashes]}

score("v0_honest_met", votes=honest)
score("v1_drop_row_1", entry=entry_without([row_idx[0]]), votes=honest)

q14 = m.SPAN.findall(rows[13][2])[0]
c = lines[row_idx[0]].split(" | ")
score("v2_quote_wrong_copy_dup",
      entry=entry_without([row_idx[0]], "%s | %s | `%s` |" % (c[0], c[1], q14)), votes=honest)

seen = set(m.normalise_text(m.SPAN.findall(x[2])[0].replace("\\|", "|")).strip() for x in rows)
U = list(m.COPIES)
s497 = m.normalise_text(BASE[m.COPIES[U[0]][0]])
utilc = m.normalise_text(BASE[m.COPIES[U[2]][0]])
w = utilc.split(" ")
cand = next(" ".join(w[i:i + 10]) for i in range(len(w) - 10)
            if " ".join(w[i:i + 10]) not in s497 and " ".join(w[i:i + 10]) not in seen)
score("v2b_quote_wrong_copy_unique",
      entry=entry_without([row_idx[0]], "%s | %s | `%s` |" % (c[0], c[1], cand)), votes=honest)

h0, claim0 = hashes[0], rows[0][0]
v3 = {"Mo52Ent01": ["REPLACE %s :: %s" % (h0, claim0), "ENTAIL %s entailed" % h0]
                  + ["ENTAIL %s entailed" % h for h in hashes[1:]],
      "Mo52Ent02": ["ENTAIL %s entailed" % h for h in hashes]}
score("v3_replace_author_plus_one", votes=v3)

score("v3b_replace_author_plus_two",
      votes={"Mo52Ent01": ["REPLACE %s :: %s" % (h0, claim0)],
             "Mo52Ent02": ["ENTAIL %s entailed" % h for h in hashes],
             "Mo52Ent03": ["ENTAIL %s entailed" % h for h in hashes]})

score("v4_two_non_voter_seats",
      votes={"Mo52Ent01": ["ENTAIL %s entailed" % h for h in hashes[1:]],
             "Mo52Ent02": ["ENTAIL %s entailed" % h for h in hashes[1:]],
             "Mo52ExecC2Replay": ["ENTAIL %s entailed" % h0],
             "Mo52Critic01": ["ENTAIL %s entailed" % h0]})

score("v5_votes_in_fence",
      votes={"Mo52Ent01": ["ENTAIL %s entailed" % h for h in hashes[1:]],
             "Mo52Ent02": ["ENTAIL %s entailed" % h for h in hashes[1:]],
             "Mo52Ent03": ["```", "ENTAIL %s entailed" % h0, "```"],
             "Mo52Ent04": ["~~~", "ENTAIL %s entailed" % h0, "~~~"]})

keep = 16
h1b = hashes[keep:]
score("v1b_table_at_floor_12", entry=entry_without(row_idx[:keep]),
      votes={"Mo52Ent01": ["ENTAIL %s entailed" % h for h in h1b],
             "Mo52Ent02": ["ENTAIL %s entailed" % h for h in h1b]})

src497 = [i for i, r in enumerate(rows) if r[1].strip() == "S497"]
h1c = [h for i, h in enumerate(hashes) if i not in src497]
score("v1c_drop_source_S497_rows", entry=entry_without([row_idx[i] for i in src497]),
      votes={"Mo52Ent01": ["ENTAIL %s entailed" % h for h in h1c],
             "Mo52Ent02": ["ENTAIL %s entailed" % h for h in h1c]})
```

`v0` is the control that makes the other lines meaningful: the harness injects votes in a form the counter reads,
so a `v1`–`v5` `entailed=` below `28` is the counter rejecting those votes, not the harness failing to supply them.
The first run of the harness did fail exactly there (`entailed=0` for `v0`) because `ls` returned bare file names
while `entail_votes` looks up `ENTAIL_DIR + voter + ".md"`; that is a harness defect of mine, fixed before the
readings below, and it is disclosed here because the counter's `ls` contract (full paths, not bare names) is not
stated in its docstring.

Raw output, whole run:

```
w1 files at data commit: []
rows=28 first_row_line=24 last_row_line=51
v0_honest_met                      exit=0 C2=met claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=28 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c
v1_drop_row_1                      exit=0 C2=met claims=27 located=27 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=27 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c
v2_quote_wrong_copy_dup            exit=1 C2=unmet claims=28 located=26 quote_missing=1 bad_rows=1 sources=5 source_rows=bad pins=ok provenance=ok entailed=27 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=bad_rows,entailment,quote_missing,source_rows
v2b_quote_wrong_copy_unique        exit=1 C2=unmet claims=28 located=27 quote_missing=1 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=28 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=quote_missing
v3_replace_author_plus_one         exit=1 C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=27 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment
v3b_replace_author_plus_two        exit=0 C2=met claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=28 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c
v4_two_non_voter_seats             exit=1 C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=27 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment
v5_votes_in_fence                  exit=1 C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=27 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment
v1b_table_at_floor_12              exit=1 C2=unmet claims=12 located=12 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok entailed=12 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=sources_floor
v1c_drop_source_S497_rows          exit=1 C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=sources_floor
h0=9afaa81505da h14_quote='allowed = ((totalram_pages() - hugetlb_total_pages()) * sysctl_overcom'
v2b_unique_span='// SPDX-License-Identifier: GPL-2.0-only #include <linux/mm.h> #include <linux/slab.h> #include <linux/string.h> #include'
```

### What each line shows

| variant | what changed | reading |
|---|---|---|
| v0 control | two distinct voters, all 28 rows, no authorship | `C2=met … entailed=28` — the harness feeds votes the arm can see |
| v1 one row dropped | row 1 (`S497`) removed from the table, every remaining row voted | `C2=met claims=27 … entailed=27` — **the drop is not noticed** |
| v2 wrong-copy quote, duplicated | row 1's quote replaced by row 14's span (a `mm/util.c` line) | `unmet … located=26 quote_missing=1 bad_rows=1 source_rows=bad failed=bad_rows,entailment,quote_missing,source_rows` |
| v2b wrong-copy quote, unique | row 1's quote replaced by a 10-word `mm/util.c` window that occurs nowhere else in the table | `unmet … located=27 quote_missing=1 bad_rows=0 … failed=quote_missing` |
| v3 authorship + one other voter | voter A carries `REPLACE <h0> :: <its own row text>` and votes `entailed` on it; voter B votes `entailed` on all rows | `unmet … entailed=27 dissent=0 failed=entailment` — A's vote does not count, so row 1 has one counted voter |
| v3b authorship + two others | A's `REPLACE` line, votes from B and C | `C2=met … entailed=28` — the authorship exclusion is per-voter, not per-row |
| v4 two non-voter seats | `Mo52ExecC2Replay` and `Mo52Critic01` carry the only votes on row 1 | `unmet … entailed=27 failed=entailment` — non-voter reports are not read at all |
| v5 votes inside fences | `Mo52Ent03` fenced with ` ``` `, `Mo52Ent04` fenced with `~~~`, both voting row 1 | `unmet … entailed=27 failed=entailment` — fenced lines are invisible |
| v1b table at the floor | 16 rows removed, 12 kept, all voted | `unmet claims=12 sources=3 … failed=sources_floor` |
| v1c one source deleted | all 7 `S497` rows removed, all voted | `unmet claims=21 sources=4 … failed=sources_floor` |

Every required arm holds: a wrong-copy quote is caught by the row's own copy only (`v2b`: `located=27`, the row still
has 28 counted `entailed` votes and the claim is `unmet` on `quote_missing` alone), authorship removes exactly one
voter (`v3` 27 vs `v3b` 28), non-voter seats contribute nothing (`v4`), fenced lines contribute nothing (`v5`), and
the source floor catches whole-source deletion (`v1c`). The one gap the five also expose is `v1`.

## 4. Commit-state probe: votes must be committed at R

Because `entail_votes` is fed by `git ls-tree <rev> .ufo/waves/round-52/w1/`, a voter report that exists only in the
working tree cannot be seen. Measured in a throwaway `--shared` clone of the lane at the data commit
(`git clone -q --shared -n <lane> $S/clone-votes`, then `git -C "$D" checkout -q 8524904adb…`;
`git -C "$D" rev-parse --show-toplevel` printed `/fast/scratch/hyaku/mori-r52/Mo52ExecC2Replay/clone-votes`,
`.git` = 1.9 M):

```
# two voter reports (all 28 rows entailed each) written into the clone's working tree, NOT committed
$ python3 ./count-c2.py 8524904adb25e44f24d9f25aac7eae909625c18c --repo "$D"
C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment
exit=1

# same two files committed in the clone (throwaway identity, -c user.name/-c user.email)
$ git -C "$D" add .ufo/waves/round-52/w1/Mo52Ent01.md .ufo/waves/round-52/w1/Mo52Ent02.md
$ git -C "$D" -c user.name=probe -c user.email=probe@scratch.invalid commit -q -m "scratch probe: two voter reports"
$ python3 ./count-c2.py a7558b9077d25b7b0c0b8bbe2013c35138ed5f8a --repo "$D"
C2=met claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=28 dissent=0 rev=a7558b9077d25b7b0c0b8bbe2013c35138ed5f8a
exit=0

# re-scoring the data commit in the same clone, now that the votes exist later in history
$ python3 ./count-c2.py 8524904adb25e44f24d9f25aac7eae909625c18c --repo "$D"
C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment
exit=1
```

The third line is the useful one: the arm is pinned to the tree at R in both directions, so votes committed later do
not retroactively satisfy the data commit. Consequence for integration, measured on the live lane: at tip `075436b1`
the twelve voter reports are untracked (`git ls-tree --name-only HEAD .ufo/waves/round-52/w1/` lists only
`swarm-registry.json`; `git status --porcelain` shows the reports as `??`), and the counter at that tip reads

```
$ python3 …/count-c2.py 075436b1
C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=075436b1346ca659afb8be7a46f0e67e4170aa83 failed=entailment
exit=1
```

so `C2=met` exists only at a commit that contains the reports — the L1 must commit w1 and score that commit, and a
`C2=met` run against the working tree is not a reading at all.

## 5. Scratch, writes, tooling

- Scratch `mkdir -p /fast/scratch/hyaku/mori-r52/Mo52ExecC2Replay/{tmp,clone-votes}`; every run `cd` there;
  `TMPDIR` exported to `…/Mo52ExecC2Replay/tmp`. Clone removed (`rm -rf`), `tmp` and the counter copy removed
  before finishing; nothing cited above lives only in scratch.
- Writes: this report only. No git/jj mutation in the lane or the fleet root (only `show`, `ls-tree`, `log`,
  `status`, `rev-parse`, `clone FROM` the lane); the only commits were in the scratch clone, with a throwaway
  identity and `rev-parse --show-toplevel` asserted equal to the clone before the first commit. No file was created
  inside the lane by any tool run: the counter was imported from a scratch copy so no `__pycache__` was written under
  `.ufo/waves/round-52/`.
- Host reads: none were needed; no sysctl, cgroup, swap or watermark was touched, and no kernel log message text was
  grepped.
- Tooling: nothing installed or upgraded (no pacman, no uv/npx/binary); `python3` from the host was sufficient.

## Findings

1. **MED — a dropped row is invisible to the counter.** `v1_drop_row_1` reads `C2=met claims=27 … entailed=27 …`
   (`count-c2.py` `MIN_CLAIMS = 12` and per-row entailment; no expected row set). Any row may be removed — or the
   table rewritten — and the claim still reads met as long as ≥ 12 rows and 5 sources with votes remain. The data
   commit's author decided 28 rows and froze the hash list in `evidence/c2-hashes-at-data.txt`, but the counter never
   compares against it. Counter frozen this round: this is a named limit for the report and a round-53 item (a
   successor arm that reads a frozen expected-hash list and requires the table's hash set to equal it, or
   `claims == len(frozen list)`). Concerned file:
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c2.py` (`evaluate`, `MIN_CLAIMS`).
2. **MED — `C2=met` exists only in a commit.** Votes are read with `git ls-tree <rev> .ufo/waves/round-52/w1/`, so
   untracked reports are invisible; at tip `075436b1` all twelve reports are `??` and the counter reads
   `entailed=0 failed=entailment`. Integration ordering, not a counter defect: the L1 must commit the voter reports
   before scoring, and must report the revision it scored. Concerned file:
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c2.py` (`git_lister`, `entail_votes`).
3. **LOW — the `ls` callback's contract is undeclared.** `entail_votes` looks up
   `ENTAIL_DIR + voter + ".md"` in the value returned by `ls`, which for the shipped `git_lister` are
   directory-prefixed paths; the docstring does not say so, and my first harness supplied bare names and silently got
   `entailed=0`. Any future in-memory fixture that returns bare names passes a vacuous arm. Concerned file:
   `count-c2.py` (`entail_votes`, `git_lister`).
4. **LOW — `--hashes` ignores `--repo`.** `main` special-cases `--hashes` before option parsing, so a seat scoring a
   clone cannot obtain that clone's hashes:
   `python3 …/count-c2.py --hashes 8524904adb… --repo DIR` → `C2_SETUP usage: count-c2.py <rev> [--repo DIR] [--entry PATH] | --selftest`, exit=2.
   The hashes are then only obtainable at the lane's own revision, which happened to be enough here. Concerned file:
   `count-c2.py` (`main`).
5. **LOW — non-voter votes are wholly invisible, including dissent.** `v4_two_non_voter_seats` gives row 1 two seats
   outside the frozen twelve and reads `entailed=27`; a non-voter `overclaim` is likewise ignored (selftest
   `entail_non_voter_dissent_ignored_met`). This matches the frozen P-C2 (`voters are exactly the frozen list`), and
   it is a named limit in the contract — recorded here so a wave-seat disagreement filed by a non-voter is not later
   mistaken for a lost vote. Concerned file: `count-c2.py` (`entail_votes`, `VOTERS`).
6. **LOW — an author's own `entailed` vote is dropped without any diagnostic.** `v3` reads `dissent=0` with
   `entailed=27`: the seized vote is not reported as an exclusion, so a wrongly filed authorship line lowers
   `entailed` silently and the verdict names only `failed=entailment`. Recovering which voter was excluded requires
   re-deriving authorship by hand. Concerned file: `count-c2.py` (`evaluate`, `ok_voters`).
7. **LOW — the two wrong-copy shapes are distinguished only by accident.** When the borrowed span duplicates an
   existing row's quote (`v2`), the row is rejected as `bad_rows` *and* `quote_missing` and `source_rows` go bad —
   four failed arms for one defect; when it is unique (`v2b`), only `quote_missing` fires. Both are caught, so this
   is a legibility item, not a hole; it matters because `v2`'s `located=26` is arithmetically confusing (28 rows − 1
   bad − 1 missing). Concerned file: `count-c2.py` (`evaluate` loop, `seen_quotes`/`bad` ordering).
