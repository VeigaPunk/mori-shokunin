# RerunC2Count — round-26 wave 2: C2 counted value

Seat: MoriR26.RerunC2Count (leaf; no subagents, no background jobs).
Tip under attack: 16935e24c93fa7e7567413d7ec091339a5df1474 (on master; `merge-base --is-ancestor` true).
Entering tip: 248408f5b6610a85bcbdebe7ac0b4fa7ed51422a.
Scratch: /fast/scratch/hyaku/mori-r26/RerunC2Count/ (tip, first, e4dba, tamper, vacuous, mini, count-c2-mini-copy.sh).
Lane writes: none. Git used read-only only (log, rev-parse, cat-file, ls-tree, show, archive, merge-base, hash-object without -w). `git status` not run (it can refresh the index).
Tools: none installed or updated. Observed: Python 3.14.8 (/usr/bin/python3), git 2.56.0, `jq` = jaq 3.1.1 (/home/vgpnk/.local/bin/jq, not GNU jq). Python agrees with jaq on N (below).

## Verdict per value

| Value | Source | Observed | Verdict |
|---|---|---|---|
| freeze_order=ok | count-c2.sh 16935e24, run from /tmp | ok | holds |
| cases_changed_since_freeze=0 | count-c2.sh 16935e24 | 0; cases blob 5b4dcee7 unchanged from freeze to tip, 327fbcca and 4dba9cc7 | holds |
| N=32 | count-c2.sh 16935e24 (jaq); Python json | 32 both ways; 32 unique IDs | holds |
| PASS 32/32, selftest exit 0 | fresh `git archive` of 16935e24, `--selftest` | PASS 32/32, exit 0 | holds (limit F4) |
| exit=0 line | counter output | selftest exit 0 printed | holds for the selftest |
| counter's own exit status | count-c2.sh line 10 | 0 at tip; 0 even when the selftest FAILs (scratch) | defect (F1, low) |
| 248408f5 "before" | count-c2.sh 248408f5 | `absent cases_commit=none tool_commit=none`, wrapper exit 2; `cat-file -e 248408f5:tools/mori-oom-killers.py` exit 128 | holds |
| c2-count.txt | header revisions 327fbcca, 248408f5 | values reproduced line for line at 327fbcca and 16935e24; header names no tip | values hold; header defect (F3, low) |
| c2-selftest.txt | header revision 4dba9cc7; tool_blob 44dac3fd; cases_blob 5b4dcee7; freeze 5b10649d | blobs equal tip; PASS 32/32 exit 0 reproduced at 4dba9cc7 and tip; supplementary PASS 32/32 reproduced | blobs and values hold; revision header not the tip (F3, low) |

Commit history of the frozen inputs (read-only git):
- cases.json: one commit ever touches it in tip history: 5b10649d (adds it). Blob 5b4dcee7b682c896c8e9f22ed1f8ac58d0176556 at 5b10649d, 327fbcca, 4dba9cc7, 16935e24, and in the working tree (`git hash-object`, no -w).
- tools/mori-oom-killers.py: one add commit c2fdd929 (blob 0df359bc). Later commits 278f02e, 825f988, 93aa1b9, 738eec1 change it (all precede 4dba9cc7). Blob 44dac3fd at 4dba9cc7, 327fbcca, 16935e24, and in the working tree.
- count-c2.sh: committed at 99338de; blob 030d678d at 327fbcca, 4dba9cc7, 16935e24, and in the working tree.
- Ancestry: 5b10649d is an ancestor of c2fdd929 (`merge-base --is-ancestor` true), so freeze precedes tool. 327fbcca and 4dba9cc7 are ancestors of the tip.

## Findings, by severity

### F1 (low) — the counter's exit status cannot report a failed selftest. Defect.

Attacks: C2 counter command (`.ufo/waves/round-26/count-c2.sh`, line 10).
- Line 10 is `python3 -I -B "$D/$T" --selftest; echo "exit=$?"; rm -rf "$D"`. The script's status is the status of its last command, `rm`, so it is 0 whatever the selftest returns.
- Reproduced in a scratch repo (/fast/scratch/hyaku/mori-r26/RerunC2Count/mini). The freeze commit held cases.json with one expectation deliberately wrong; the tool commit held tip bytes. The copy of the counter differed from the lane script only in the L= line. Output: `freeze_order=ok`, `cases_changed_since_freeze=0`, `N=32`, `MORI_OOM_KILLERS_SELFTEST: FAIL 31/32`, `FAIL c01-host-quiet-thresholds: verdict: got 'KILLERS_QUIET' expected 'KILLER_ACTED'`, `exit=1`; counter wrapper exit 0.
- Effect: a gate that reads status treats a failing count as success. Only the printed text carries the result. The contract cites counter exit codes (`absent ... exit 2` before-state), so this is a real gap.
- Owner action (not applied here): end with the selftest's status, e.g. `rc=$?; rm -rf "$D"; exit "$rc"`.

### F2 (low, latent) — the selftest comparator passes a case that lacks its expectation keys. Defect in the tool.

Attacks: tools/mori-oom-killers.py:677 (`if "verdict" in expect`), :681 (`if "exit" in expect`), :683 (`fields = expect.get("fields")`, skipped when absent).
- Control: scratch copy in which c03 has `verdict` and `exit` removed: `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`, exit 0.
- The frozen file has no such gap: all 32 cases carry `verdict`, `exit` (int) and a `fields` key (c31 and c32 carry empty fields). So the counted value is unaffected today; the protection is the blob check (cases_changed_since_freeze=0).
- Risk: a future edit to the case file, or a regression in it, would pass silently.

### F3 (low, evidence hygiene) — receipt headers name revisions other than the tip. Values hold on the tip bytes.

Attacks: evidence/c2-count.txt (header revision 327fbcca; block 248408f5); evidence/c2-selftest.txt (header `revision: 4dba9cc7...`).
- The header blobs in c2-selftest.txt (tool 44dac3fd..., cases 5b4dcee7...) and the freeze commit (5b10649d30c9...) equal the tip bytes. The counter blob (030d678d) is unchanged from 99338de to the tip.
- Both receipts' values reproduce at the tip: count-c2 at 327fbcca and 4dba9cc7 gives the same lines as the tip run; selftest at the 4dba9cc7 archive gives PASS 32/32, exit 0.
- No receipt names 16935e24. Owner action: re-capture both receipts at 16935e24, or write the blob-equivalence in the header.

### F4 (info, process limit; the counted statement holds as written) — the 32 frozen cases are no longer held out.

Attacks: contract.md C2 and A2.
- The first tool commit c2fdd929, built before the later changes, already passes the frozen file: archive selftest PASS 32/32, exit 0. The four later tool commits (278f02e, 825f988, 93aa1b9, 738eec1) changed rules and still give PASS 32/32 at the tip. So no later change moved the count.
- But the cases were visible to the L1 during development (A2 says so). The 32 are a regression set, not held-out evidence. The cases and the tool both follow the same contract text, so PASS 32/32 shows agreement with the contract's grammar, not with live earlyoom output. [INFERENCE from the contract text; not tested against live output here.]
- Authorship ("written by WriteOomKillersCases", "built blind by BuildOomKillersTool") rests on commit messages. Not verified by this seat; the contract treats it as a process fact, not part of the count.

### F5 (low, latent) — the counter picks its commits fragilely.

Attacks: count-c2.sh lines 5–9.
- Lines 5 take `tail -1` of a date-ordered `git log --diff-filter=A`. Correct at the tip because each path has exactly one add commit (verified). Wrong if a path were deleted and re-added.
- The counter never asserts that N (from the freeze blob) equals the selftest's own total. Equality rests on cases_changed_since_freeze=0.

### F6 (info) — minor comparator leniency and an exit-code collision in the tool.

- tools/mori-oom-killers.py:614–623 accept string/number equality. The tool emits thresholds as floats (:344, :348, :384–387) and the frozen threshold expectations are floats (10 values: 10.0 and 5.0), so no effect on the count.
- :718 returns 1 on selftest FAIL, the same code the reader uses for KILLER_ACTED (main at :776–782). A wrapper reading exit codes can confuse them.

## Checks that hold

- Tool imports are stdlib only (tool.py:48–55: __future__, argparse, json, re, subprocess, sys, pathlib).
- No case-specific branches: a grep for `c[0-3][0-9]-` hits only comments (e.g. :303, which names frozen case c02 in a comment), help text (:13–16, :744) and the default cases path (:590–592). No code path dispatches on a case ID.
- Sensitivity of the selftest: a scratch copy with three altered expectations (c01 verdict, c02 one field value, c13 exit) gives `FAIL 29/32`, names exactly those three IDs, exit 1. The comparator detects changes.
- Setup errors: missing cases file gives `cannot read cases file ...` and exit 2 (KILLERS_UNKNOWN); empty file gives `... is empty`, exit 2.
- Before-state: `git cat-file -e 248408f5:tools/mori-oom-killers.py` exit 128 (matches contract's "before" claim); counter at 248408f5 prints `absent`, exit 2.
- Supplementary (not counted): cases-supplementary.json has 32 cases, 29 IDs overlap the frozen file, 3 new (c33, c34, c35). `--cases` is honoured (tool.py:781). PASS 32/32 at tip; blob d7c9040b unchanged since 21386b9, before 4dba9cc7.
- Working-tree copies of tool, cases and counter hash to the same blobs as the tip.

## Not run or not established

- Live-run receipt evidence/c2-live-run.txt: not read (outside the counted value).
- Mutation kill rate of the tool: not run here (other seats).
- Authorship of cases and tool: not verified beyond commit messages.
- `git status`: not run (index refresh). Working-tree check covers three files only.
- cases.json `frozen_with` and `note` text: not read beyond their types (kept out of the report).
- The tip archive contains a dangling symlink fixture (.ufo/waves/round-17/fixtures/seat/SymlinkIgnore/Dangling.jsonl). Python shutil.copytree of the full archive fails on it; the counter's tar extraction is unaffected. Not a C2 defect; noted for the owner.

## Summary

- Counted values hold at 16935e24: freeze_order=ok, cases_changed_since_freeze=0, N=32, PASS 32/32, selftest exit 0. The bytes that decide them are identical from 4dba9cc7 to the tip.
- Before-state at 248408f5 holds: absent, exit 2.
- One defect in the counter (F1): its own exit status ignores the selftest. Two low-severity evidence and tool gaps (F2, F3). F4 is a disclosed limit on what the 32 cases can show.
