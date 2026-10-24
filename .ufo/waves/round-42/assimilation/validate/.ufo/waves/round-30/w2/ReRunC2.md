# MoriR30.ReRunC2 — wave-2 falsify report (C2 measured value)

**Verdict: AGREE** — reporting C2 as a miss is correct under the contract. The C2 counter
(commit blob 8ac9535e) prints `C2=unmet`, exit 1, at every measured rev, and the freeze-gate
blob prints `blind_violations=1` (not 0), so contract A2 condition 4 fails.

## 1. Counter runs (all from commit blob 8ac9535e via `git show <rev>:.ufo/waves/round-30/count-c2.sh`)

| rev | key lines | C2 / exit |
|---|---|---|
| `ad0f047` (measured tip at assignment) | r29 PASS 24/24; older PASS 32/32 / 32/32 / 30/30; blobs_ok=yes; r29_blob_ok=yes; freeze=db1ec469; cases=8; authors=4; provenance=8/8 unselected=0; shape=8/4; pins 8/8 blob_match; base+fixed selftest PASS 8/8; verdicts 8/8; differential=94/94 changed=2 disallowed=0 acted_lost=0 errors=0; receipts=3/3; gate_selftest=PASS; gate_mutants=4/4; scanned=4; **blind_violations=1** | C2=unmet, exit 1 |
| `713be294` (current HEAD) | identical to ad0f047 row | C2=unmet, exit 1 |
| `58b61681` (before-receipt point) | writer_absent=CaseR30a-d; r29 FAIL 21/24; freeze=none; cases=0; receipts=0/3; gate_selftest=not_run; scanned=not_run | C2=unmet, exit 1 (expected before-state; matches c2-before premise) |
| `2ec25cc1` | identical to ad0f047 row | C2=unmet, exit 1 |

All lines above are literal counter output from the runs; each run returned exit 1. The
measured outcome at the assignment tip (ad0f047) is reproduced exactly, and it also holds at
the current lane tip (713be294).

## 2. Freeze-gate run (freeze blob at db1ec469)

Command (cwd = lane root, per assignment):
```
bash <(git -C /home/vgpnk/Projects/shokunin/mori-shokunin show db1ec469:.ufo/waves/round-30/check-blind-wave.sh) db1ec469 .ufo/waves/round-30/w1 '^CaseR30[a-d]\.md$'
```
Output, exit 1:
```
scanned=4
blind_violations=1
.ufo/waves/round-30/w1/CaseR30a.md:105:writer-forbidden-opened-path
```
The freeze gate blob is the A3 version: `git rev-parse db1ec469:...check-blind-wave.sh` =
`dbcbe50e…` = `git rev-parse 55f9a69:...check-blind-wave.sh` (A3 commit); the A2 version at
32e287ff is a different blob (`893e69d1…`).

## 3. Why blind_violations=1 at the freeze commit — the flagged line

`git show db1ec469:.ufo/waves/round-30/w1/CaseR30a.md` (lines 95–105):
```
95: ## Files opened
96: /home/vgpnk/.agents/skills/godspeed/SKILL.md
97: /home/vgpnk/.omp/agent/RULES.md
98: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/rule-text.md
99-103: https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c|kill.c|msg.h|MANPAGE.md, https://raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml
104: (blank)
105: The scratch JSON passed python3 json.load; I opened no lane tool source, lane tool output, lane fixture, or other report.
```
Line 105 is the writer's closing prose sentence, placed directly after the Files-opened list
(no heading separates it). The gate keeps `in_files_list` active until the next `## ` heading,
so it inspects line 105 as a list entry. A scratch reproduction of `inspect_entry_line`
(`/fast/scratch/hyaku/mori-r30-w2/MoriR30.ReRunC2/inspect_test.sh`) against the exact line
bytes shows the trigger: token `json.load;` has its trailing `;` stripped → candidate
`json.load`, which contains `.` → treated as a path-like token → fails the A3 allowlist →
`writer-forbidden-opened-path`. `entry_forbidden=1` confirmed.

So the single violation is a **gate parsing false positive**: the writer opened no such path
(the sentence explicitly denies it); the prose token `json.load;` is misparsed as a file path.
All real opened paths on lines 96–103 pass the A3 allowlist.

## 4. Is reporting C2 as a miss correct under the contract? — Yes

- A2 condition 4 (contract.md): "... run at the freeze commit on `.ufo/waves/round-30/w1`
  with writer regex `^CaseR30[a-d]\.md$` it prints `blind_violations=0`". Measured at the
  freeze blob: 1. Condition fails → C2=unmet. No false-positive exemption exists in the
  contract; "A declared claim is never withdrawn or narrowed; a miss is reported as a miss."
- A3 does not rescue it: the freeze blob **is** the A3 gate and still counts the line-105
  violation. A3 only admits the two host instruction files (lines 96–97), which are not the
  flagged line.
- Author's receipt `evidence/c2-after.txt` matches our measurement exactly (blind_violations=1,
  C2=unmet, exit 1 at 2ec25cc1), and commit 0b828c2's message names the same fact
  ("CaseR30a.md:105 closing sentence parsed as a files-opened entry").
- Corroboration: the A2 gate blob (32e287ff) run at the freeze commit prints `scanned=4`,
  `blind_violations=4`, one `writer-forbidden-opened-path` per report (first-forbidden-per-file:
  CaseR30a.md:96, CaseR30b.md:116, CaseR30c.md:79, CaseR30d.md:110 — the godspeed SKILL.md
  path), consistent with A3's disclosure of the pre-A3 run.

## Findings by severity

1. **None (no contract breach).** C2=unmet is the correct contractual status; the miss stands.
2. **Medium — gate defect (candidate R5 residual):** `check-blind-wave.sh` has no way to stop
   list scanning at the end of a Files-opened list; post-list prose is inspected as entries and
   path-like tokens (e.g. `json.load;`) trip `writer-forbidden-opened-path`. This undermines the
   blindness gate's precision on prose-rich reports and explains the one violation that decides
   the miss. Not a C2 fix (the contract binds the freeze blob), but a legitimate defect to
   report to the integration owner.

## Residual risk / verification gaps

- I did not audit CaseR30b-d reports line-by-line beyond the gate scan; the gate scanned all 4
  and flagged only CaseR30a.md:105 (A3 blob), so the other three have no forbidden path under
  the A3 allowlist.
- Whether the gate defect should change the round's C2 judgment is a contract/closure call for
  the L1; under the written contract the miss is correct.
- No tools installed; no tooling-directive installs to record. Read-only git only; no writes in
  the lane except this report.
