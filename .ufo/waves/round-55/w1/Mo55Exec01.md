# Mo55Exec01 — C1/C2 selftests (unwrapped) and counters at the committed data revision

Seat role: executor (leaf). Scope: run the frozen C1/C2 selftests and counters unwrapped, at the committed data
revision; report exact commands, outputs and exits. **No production edits, no git/jj mutations in the lane.**
Lane repo read-only throughout; all mutation was confined to scratch.

## Environment

- Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` — read-only. `git rev-parse HEAD` = `b8a70adf93ebd9d1e4e95bef8627a220f2fa816b` at every check below.
- Frozen inputs: `c9b908f0bb89974f30b927776ce2450ae4198b10` (contract + counters + controls + source copies).
- Entering tip: `ca52426ea496bc6592e3e867cc9d28843e45f196`.
- Data corrections landed at `51ebd3d3ff5bfa2cdd532f79d5eb6d9702363072` and `b8b7064c2b54c8b6b22c288232a96c43fae1af47`; **this report measures the latter** (`b8b7064c`).
- Python 3.14.8 (GCC 16.2.1), git 2.56.0.
- Scratch: `/fast/scratch/hyaku/mori-r55/Mo55Exec01` (removed before yield). Two scratch clones under it (`clone`, `clone2`);
  `git rev-parse --show-toplevel` was asserted to equal the fixture dir before any commit inside either.
- Disk guard: `scripts/hyaku/disk-guard.sh status` → exit 0, `/fast/scratch/hyaku` 27% used, 593.8G free. No ENOSPC. No install performed; no tool was added or updated.

## 1. Frozen-byte integrity (precondition for every number below)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ sha256sum -c .ufo/waves/round-55/evidence/freeze-sha256.txt
```
→ **every line `OK`; zero mismatches** (all 38 frozen artefacts: contract, both counters, both selftest harnesses, both
control fixtures, both selftest receipts, scope listing, and all 24 pinned source copies).

Frozen-vs-working-tree identity for the instruments, by git blob hash:

| artefact | frozen `c9b908f0` blob | worktree blob | verdict |
|---|---|---|---|
| `.ufo/waves/round-55/count-c1.py` | `256aaab4f017…` | `256aaab4f017…` | SAME |
| `.ufo/waves/round-55/count-c2.py` | `9573d419ec6f…` | `9573d419ec6f…` | SAME |
| `.ufo/waves/round-55/checks/selftest-c1.py` | `7587e326dfd0…` | `7587e326dfd0…` | SAME |
| `.ufo/waves/round-55/checks/selftest-c2.py` | `de211a808ca7…` | `de211a808ca7…` | SAME |
| `.ufo/waves/round-55/controls/c1data.py` | `35ad9c23819f…` | `35ad9c23819f…` | SAME |
| `.ufo/waves/round-55/controls/c2data.py` | `eb5cfd89a77c…` | `eb5cfd89a77c…` | SAME |

The counters were run **unwrapped** — no shell wrapper, no `bash -c`, no output post-processing between the command and
the captured bytes. `python3 -I -B` (isolated mode, no bytecode) was used so no `__pycache__` is written into the lane.

## 2. Selftests, unwrapped

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 -I -B .ufo/waves/round-55/count-c1.py --selftest
C1_SELFTEST pass=44 fail=0
exit=0

$ python3 -I -B .ufo/waves/round-55/count-c2.py --selftest
C2_SELFTEST pass=10 fail=0
exit=0
```

stderr was empty for both. These reproduce the committed receipts `evidence/selftest-c1.txt` (`C1_SELFTEST pass=44 fail=0`,
exit=0) and `evidence/selftest-c2.txt` (`C2_SELFTEST pass=10 fail=0`, exit=0) exactly.

**Selftest re-run from the frozen bytes**, in a pristine clone checked out at `c9b908f0bb89974f30b927776ce2450ae4198b10`
(so the harness, its control fixtures and the counters are all read from the frozen commit, not the worktree):

```
$ git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin <scratch>/clone
$ git checkout c9b908f0bb89974f30b927776ce2450ae4198b10
$ python3 -I -B .ufo/waves/round-55/count-c1.py --selftest
C1_SELFTEST pass=44 fail=0
exit=0
$ python3 -I -B .ufo/waves/round-55/count-c2.py --selftest
C2_SELFTEST pass=10 fail=0
exit=0
```

Identical. The selftests are hermetic over git objects and do not depend on worktree state.

## 3. Counters at the committed data revision `b8b7064c2b54c8b6b22c288232a96c43fae1af47`

```
$ python3 -I -B .ufo/waves/round-55/count-c1.py b8b7064c2b54c8b6b22c288232a96c43fae1af47
C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=b8b7064c2b54c8b6b22c288232a96c43fae1af47 failed=votes
exit=1

$ python3 -I -B .ufo/waves/round-55/count-c2.py b8b7064c2b54c8b6b22c288232a96c43fae1af47
C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=b8b7064c2b54c8b6b22c288232a96c43fae1af47 failed=entailment
exit=1
```

Both match the values the L1 recorded in the contract and in `evidence/c1-at-data.txt` / `evidence/c2-at-data.txt`:
scope=78 / rows=78 / matched=78 / status_ok=78 / line_ok=78, 69 same + 7 moved + 2 changed, 0 votes, exit 1;
and 23 claims / 23 located / 0 missing / 0 bad rows / 9 sources / 0 votes, exit 1.

**Receipt reproduction.** Normalising only the `rev=` field, my run at `b8b7064c` is byte-identical to the committed
`evidence/c1-at-data.txt` and `evidence/c2-at-data.txt` (diff exit 0 for both). The committed receipts were captured at
`f70051ddcb903dc6c4393c410f8bab054951af82`; re-running the counters at that exact revision reproduces the committed
receipts byte-for-byte as well.

**Determinism.** Three consecutive runs of each counter at `b8b7064c` collapse to a single distinct line each.

## 4. Surrounding revisions (control and history)

| revision | C1 | C2 |
|---|---|---|
| `ca52426e` (entering tip) | `C1=unmet scope=78 rows=0 … source_rows=bad pins=bad provenance=bad … failed=ledger_absent,pins` — exit 1 | `C2=unmet claims=0 … failed=entry_absent,pins` — exit 1 |
| `c9b908f0` (frozen inputs) | `C1=unmet scope=78 rows=0 … pins=ok provenance=bad … failed=ledger_absent` — exit 1 | `C2=unmet claims=0 … pins=ok provenance=bad … failed=entry_absent` — exit 1 |
| `51ebd3d3` (first correction) | `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 … failed=votes` — exit 1 | `C2=unmet claims=23 located=21 quote_missing=1 bad_rows=1 sources=9 source_rows=bad pins=ok … failed=bad_rows,entailment,quote_missing,source_rows` — exit 1 |
| `b8b7064c` (measured data rev) | `failed=votes` — exit 1 | `failed=entailment` — exit 1 |
| `b8a70adf` (lane tip) | `failed=votes` — exit 1 | `failed=entailment` — exit 1 |

The entering-tip outputs are byte-identical to the committed do-nothing controls `evidence/control-c1-do-nothing.txt`
and `evidence/control-c2-do-nothing.txt` (diff exit 0 for both). The `51ebd3d3` → `b8b7064c` step is what fixes C2's
`quote_missing=1 bad_rows=1 source_rows=bad` down to `located=23 bad_rows=0 source_rows=ok`; that correction is real
and is visible in the counters, not merely asserted.

**Scope reproduction.** `count-c1.py --scope` emits 78 lines; sorted, it is byte-identical to the committed
`evidence/c1-scope.txt` (diff exit 0, 0 differing lines).

## 5. Feasibility witness — is the vote arm the only remaining blocker?

To separate "the data is wrong" from "the votes are missing", I committed a **synthetic** two-voter set into a scratch
clone (scratch only; the lane was never touched) and re-ran both counters:

```
C1=met scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=78 dissent=0 failed=  → exit 0
C2=met claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=23 dissent=0 → exit 0
```

So at the committed data revision every data-side arm of both predicates is already green: scope, rows, match, status,
line, source rows, pins, provenance, claims, quote location and the 9-source floor. **The single remaining blocker on
both axes is the vote arm** (`failed=votes` / `failed=entailment`), which is exactly what the contract's target requires
the wave to supply. The counters are satisfiable at this revision; they are not failing closed for any other reason.

## 6. Current real-seat state (measured, for the L1's benefit)

With the **real** seat reports currently in `.ufo/waves/round-55/w1/` committed into a scratch clone alongside a
dispatcher-shaped `w1-results.json` (output = the seat's own vote lines), the counters read:

```
C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=68 dissent=0 … failed=votes   → exit 1
C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=15 dissent=8 … failed=entailment → exit 1
```

- C1: 15 of the 16 RECHECK seats have reported. Union of real votes covers **78/78** scoped rows, but **68 rows have
  ≥2 voters and 10 rows have exactly 1**. All 10 single-voter rows are covered only by `Mo55Rc13`:
  `a6e5226259c9`, `0124918d278a`, `6f9f1d32ac46`, `68afd0d6fa2f`, `0527161c4edd`, `82952b5a6ec2`, `2ba00a976118`,
  `d0338d4263b9`, `bfb67ed4f174`, `53875978a00b`. `Mo55Rc14` has written no report. Every real vote word is `holds`;
  zero dissent.
- C2: all 12 ENTAIL seats have reported, but **8 rows carry at least one `overclaim` dissent** —
  `faeadb48a5f8` (En04), `e581c99e0a8d` (En01, En10), `420d69d60ee5` (En04), `4aab9fc1a48b` (En04, En11),
  `d51f0bfc539f` (En11), `51e630031934` (En01, En04, En10, En11), `c159bdf1a5a9` (En11), `b7cd35201fee` (En04).
  I re-verified three of these disputes directly against the pinned copies and they hold up:
  - Row 2 (`e581c99e0a8d`), claim "any field a filesystem never sets reaches userspace as zero": pinned
    `sources-r55/statfs.c.v7.3:67-68` fills `f_frsize` from `f_bsize` and `:92` assigns `f_flags` after the filesystem
    handler returns, so "any field … as zero" is too broad.
  - Row 14 (`51e630031934`), claim "reports zero available space once its metadata profile can take no further chunk
    allocations": pinned `sources-r55/btrfs_super.c.v7.3:1809-1811` requires `!mixed && space_info->full` **and**
    `(total_free_meta < thresh || total_free_meta - thresh < block_rsv->size)`, so the metadata-full gate alone is
    insufficient.
  - Rows 11/12 (`4aab9fc1a48b`, `d51f0bfc539f`), XFS inode total: pinned `sources-r55/xfs_super.c.v7.3:954-964` applies
    `min(..., XFS_MAXINUMBER)`, then the `maxicount` cap, then a `max(..., sb_icount)` floor — so the reported total is
    neither necessarily the stated sum nor always capped by `maxicount`.
  These are substantive, source-cited disputes, not artifact noise. `Mo55En09` and `Mo55En10` have already proposed
  `REPLACE` corrections for `e581c99e0a8d` and `51e630031934`.
- No `w1-results.json` exists in the lane yet. The counters read the bound seat output from
  `.ufo/waves/round-55/w1-results.json` **at the measured revision**, so that file must be committed alongside the seat
  reports for any vote to count. It is written by the dispatcher (`scripts/hyaku/inline-dispatcher.py:289`, `finalize()`).

## 7. Hazards found in the frozen instruments

These are properties of the **frozen** counters, which the contract forbids me to change. They are reported, not fixed.

**(a) The C1 output-binding `startswith` branch is dead code — it can never match.** `count-c1.py:301-302`:

```python
bound = voter in outputs and any(l == "RECHECK %s %s" % (h, w) or l.startswith("RECHECK %s %s ")
                                  for l in out_lines)
```

The `startswith` argument is the **literal** string `"RECHECK %s %s "` — the `% (h, w)` substitution present on the
equality branch is missing. A real candidate line never starts with that literal, so the second disjunct is always
`False`. Verified mechanically: `"RECHECK 7b2d297eec60 holds — row 1".startswith("RECHECK %s %s ")` is `False`, while the
correctly-substituted form is `True`.

Consequence — the contract at `contract.md` prescribes the per-row vote form
`RECHECK <hash> holds` **or** `RECHECK <hash> stale — reason + path:line`. The suffixed (stale) form **cannot bind**
under the frozen counter. Measured, with a ledger whose row disposition was set to `stale` and two voters agreeing:

| seat output line | voted | dissent | met |
|---|---|---|---|
| bare `RECHECK <hash> stale` | 78 | 0 | True |
| contract form `RECHECK <hash> stale — reason + path:line` | 0 | 0 | False |

The same holds for `holds` with any suffix (`— row 1`): suffix-tolerant binding was the evident intent of the
`startswith` branch, and the missing substitution silently removes it. **Today this is latent, not fatal** — all 78
ledger dispositions are currently `holds` and all 15 real RECHECK seats emit the bare form, so every real vote binds.
It becomes live the moment any row's disposition is corrected to `stale`, or any seat appends a row annotation to its
vote line. The C1 selftest does not catch it: `checks/selftest-c1.py:57,59` always build bare vote lines, so the dead
branch is never exercised.

**(b) A `stale` vote is dissent regardless of the ledger disposition.** `count-c1.py` counts `other = [w for w, bound in
v.values() if w != disp]` as dissent **from the report text alone**, bound or not. A seat that judges a row `stale`
therefore sets `dissent=1` and forces `failed=votes` while the ledger still says `holds` — the two sides must be
corrected together or the axis cannot close.

**(c) C2 overclaim votes are sticky and cannot be withdrawn.** `count-c2.py:169` adds a vote when
`m.group(2) == "overclaim" or ("ENTAIL %s %s" % (…) in out)` — an `overclaim` counts from the report text alone, and
`entail_votes` has **no last-wins rule** (unlike C1's `final_votes`). Measured: a seat that writes an `overclaim` line
and then a correcting `entailed` line still yields `dissent=1`, `entailed=22`, `met=False`. The only ways out are to
remove the `overclaim` line from the report or to land the corrected claim text via `REPLACE`.

**(d) Row 4's claim hash is unstable under the pending correction.** Row 4's claim text differs between the committed
revision and a working-tree edit observed mid-run (`"unprivileged process may still use"` → `"unprivileged user may still
use"`), changing its hash from `22a23e3fb849` to `45120996891a`. Five ENTAIL seats (`En01`, `En04`, `En07`, `En11`,
`En12`) voted against `22a23e3fb849`. If the corrected row-4 text is committed without re-voting, row 4's votes are
orphaned and C2 loses that row. **The working-tree edit was reverted by another actor during my run** — at the time of
writing, `git diff -- corpus/knowledge/disk-runway-enospc-r55.md` is empty and row 4 reads
`…limited to what an unprivileged process may still use` again, so row 4's hash at `b8b7064c` and in the worktree agree
at `22a23e3fb849`. The hazard is recorded because the row-4 rewrite was live minutes ago and two seats have already
flagged it (`Mo55Rev01`, `Mo55Simple02`).

## Findings

| severity | finding | evidence |
|---|---|---|
| High | C1 vote-binding `startswith` branch is dead code (missing `% (h, w)`), so the contract-prescribed suffixed vote form `RECHECK <hash> stale — reason + path:line` can never bind. Latent today (all dispositions `holds`, all real seats emit bare lines); live as soon as any row is corrected to `stale` or any seat annotates its vote line. Frozen counter — not modified by me. | `mori-shokunin/.ufo/waves/round-55/count-c1.py:301-302`; `mori-shokunin/.ufo/waves/round-55/contract.md:26` (per-row vote form); `mori-shokunin/.ufo/waves/round-55/checks/selftest-c1.py:57,59` (selftest never exercises a suffixed output); measured `voted=0 met=False` for the suffixed form vs `voted=78 met=True` for the bare form |
| High | C2 currently carries substantive dissent on 8 of 23 rows, from 4 seats, each with exact source citations; C2 cannot close without landing corrected claim text (`REPLACE`) and re-voting. Two `REPLACE` proposals already exist (En09, En10) covering 2 of the 8 disputed rows. | `mori-shokunin/.ufo/waves/round-55/w1/Mo55En01.md:13,25`; `…/Mo55En04.md:19,25,29,32,41`; `…/Mo55En10.md:53,65`; `…/Mo55En11.md:23,24,26,28`; corroborating pinned sources `mori-shokunin/corpus/evidence/sources-r55/statfs.c.v7.3:67-68,92`; `…/btrfs_super.c.v7.3:1809-1811`; `…/xfs_super.c.v7.3:954-964` |
| Medium | C1 has 10 scoped rows with only one settled RECHECK voter (all covered solely by `Mo55Rc13`); `Mo55Rc14` has filed no report. `MIN_VOTES=2`, so these 10 rows cannot satisfy the vote arm. | `mori-shokunin/.ufo/waves/round-55/count-c1.py:16` (`MIN_VOTES = 2`); affected hashes `a6e5226259c9`, `0124918d278a`, `6f9f1d32ac46`, `68afd0d6fa2f`, `0527161c4edd`, `82952b5a6ec2`, `2ba00a976118`, `d0338d4263b9`, `bfb67ed4f174`, `53875978a00b`; `mori-shokunin/.ufo/waves/round-55/w1/` (no `Mo55Rc14.md`) |
| Medium | C2 `overclaim` votes are sticky: they count from report text alone and there is no last-wins rule, so a seat cannot withdraw an overclaim by appending a correcting `entailed` line. | `mori-shokunin/.ufo/waves/round-55/count-c2.py:169`; measured `entailed=22 dissent=1 met=False` for the self-correcting report |
| Medium | No `w1-results.json` is committed in the lane; the counters read bound seat output from that path **at the measured revision**, so votes cannot count until the dispatcher writes it and it is committed with the seat reports. | `mori-shokunin/.ufo/waves/round-55/count-c1.py:20,296-299`; `mori-shokunin/.ufo/waves/round-55/count-c2.py:158`; producer `scripts/hyaku/inline-dispatcher.py:289` |
| Low | C1 counts a `stale` vote as dissent from report text alone, bound or not, so ledger disposition and voter word must be corrected together. | `mori-shokunin/.ufo/waves/round-55/count-c1.py:392-396`; selftest assertion `mori-shokunin/.ufo/waves/round-55/checks/selftest-c1.py:182-186` |
| Low | Row 4's claim hash is unstable (`22a23e3fb849` ⇄ `45120996891a`) under a working-tree rewrite that was live during this seat's run and has since been reverted; five seats voted against the committed hash, so committing the rewrite without re-voting orphans row 4. | `mori-shokunin/.ufo/waves/round-55/w1/Mo55Rev01.md:174,212`; `…/Mo55Simple02.md:163`; `mori-shokunin/.ufo/waves/round-55/w1/Mo55En01.md:15`; `…/Mo55En04.md:22`; `…/Mo55En11.md:16`; `…/Mo55En12.md:18` |
| Info | Both frozen selftests pass unwrapped and are hermetic: 44/44 and 10/10, exit 0, reproduced identically from a pristine clone checked out at the frozen commit `c9b908f0`. All 38 frozen artefacts match `evidence/freeze-sha256.txt`. Counters are deterministic and reproduce the committed receipts byte-for-byte (rev field aside). | `mori-shokunin/.ufo/waves/round-55/evidence/selftest-c1.txt`; `…/evidence/selftest-c2.txt`; `…/evidence/freeze-sha256.txt`; `…/evidence/c1-at-data.txt`; `…/evidence/c2-at-data.txt`; `…/evidence/control-c1-do-nothing.txt`; `…/evidence/control-c2-do-nothing.txt`; `…/evidence/c1-scope.txt` |
| Info | At the committed data revision `b8b7064c` every data-side arm of both predicates is green (scope 78/78, matched 78, status_ok 78, line_ok 78, source_rows ok, pins ok, provenance ok, 69 same / 7 moved / 2 changed; 23 claims / 23 located / 0 missing / 0 bad rows / 9 sources / pins ok / provenance ok). The sole remaining blocker on both axes is the vote arm. A synthetic two-voter witness drives both counters to `met`, exit 0. | `mori-shokunin/.ufo/waves/round-55/count-c1.py`; `…/count-c2.py`; measured at `b8b7064c2b54c8b6b22c288232a96c43fae1af47` |

## Scope and hygiene

- Files changed: **this report only** — `mori-shokunin/.ufo/waves/round-55/w1/Mo55Exec01.md`.
- No production edit, no git/jj mutation, no commit or push in the lane repo or any sibling repo. Lane HEAD unchanged at
  `b8a70adf` before and after. The only lane-tree delta visible to me (`SCORECARD.md`, `corpus/QUALITY.md`,
  `corpus/lessons/round-54.md`, and the untracked `w1/` directory) is other seats' work, not mine.
- No vote emitted: this seat is not in the frozen RECHECK (`Mo55Rc01`–`Mo55Rc16`) or ENTAIL (`Mo55En01`–`Mo55En12`)
  voter lists, and no line in this report begins with a vote token.
- Source-only: no sysctl/mount/cgroup write, no OOM/ENOSPC forcing, no module load, no repair, no quota or host change.
- No tool installed or updated; no `pacman` invocation.
- No secret, private URL, or model name appears in this report. The only URLs referenced are the public kernel.org cgit
  base already recorded in the frozen counters.
- Scratch `/fast/scratch/hyaku/mori-r55/Mo55Exec01` (including both clones) removed after the measurements above were
  captured.
- Unverified / not done: I did not run the wave dispatcher, did not commit the dispatcher-written `w1-results.json`,
  did not judge any claim's substance beyond the three disputes I re-verified against pinned sources, and did not
  modify the frozen counters despite the defects in §7 — the contract forbids it and the fix is the L1's call.
