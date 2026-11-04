# Mo84S02Quality — round 84 w1: QUALITY rows 170–172

Seat `Mo84S02Quality` (scribe). Date 2026-11-04. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering revision `5adf4337b6510dd246b247092c11cbaa97c930d3`; freeze commit
`daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4`; lane tip at report time
`39190f8a8b32af30e6a180f91d77aa92542735d9` (pre-data amendment A2). Detection and report only:
no counter, tool, contract, judge or VCS state was changed by this seat.

## 1. Produced

- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/QUALITY.md` — appended rows **170, 171, 172**
  (lines 1853–1931 at write). Append-only: `git diff --numstat -- corpus/QUALITY.md` → `80 0`
  (80 insertions, 0 deletions; rows 1–169 untouched).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/w1/Mo84S02Quality.md` — this report.

Rows land in the file's existing shape (statement, `Ground:`, `Shown able to fail:`, `Not covered:`),
with every line citation bound to a revision where the cited bytes may move:

| row | statement | ground anchors |
|---|---|---|
| 170 | multi-row anchor graded as a whole, never by first match | `corpus/QUALITY.md:1849-1851`; `.ufo/waves/round-84/contract.md:67-106`; `tools/mori-record-sweep.py:52-63,119-146` at `5adf4337`; `count-c2.py:117-139,262-276` |
| 171 | live-vs-snapshot comparison names each token's delta class | `.ufo/waves/round-84/contract.md:108-131,193-198`; `.ufo/waves/round-83/count-c2.py:243-246` at `5adf4337`; `SCORECARD.md:4230,4265` at `5adf4337`; `count-c3.py:31-34` |
| 172 | detector selftest plus a population control that reads red before the arms | `SCORECARD.md:4271,4278` at `5adf4337`; `.ufo/waves/round-84/contract.md:15-65,163-198`; `count-c1.py:61,296-300,301-313` after A2; `Mo83R01C1.md:229-230` |

## 2. Measurements

Scratch root `S=/fast/scratch/hyaku/mori-r84/Mo84S02Quality` (removed before yield). All commands
run from the lane root unless a `cd` is shown.

### 2.1 Freeze population control before amendment A2 — the frozen anchors did not anchor

```
$ python3 -I .ufo/waves/round-84/count-c1.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4 --scratch "$S/pop"
MUTANT count-c1.py M24a_killed_tally survived rc=0
EXTRA unanchored .ufo/waves/round-83/count-c1.py M24b_green_fail_token occurrences=2
EXTRA unanchored .ufo/waves/round-83/count-c2.py M24c_met_unclassified occurrences=0
EXTRA unanchored .ufo/waves/round-83/count-c2.py M24d_met_residual occurrences=0
C1=unmet mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=green detector=green rev=daa77bd5684c
```

Not the contract's declared freeze control (`mutants=4 killed=0 equivalent=2 survivors=2`,
`contract.md:53-57`). Anchor multiplicities, counted over `git show <rev>:<path>` with the frozen
counter's own `MUTANTS` table:

```
rev          M24a  M24b  M24c  M24d   (count of the frozen `old` string)
c4845c83      1     2     0     0
5adf4337      1     2     0     0
daa77bd       1     2     0     0
dbdb1aaa      1     2     0     0
```

Cause: `M24b`'s anchor also occurs in `.ufo/waves/round-83/count-c1.py`'s own `MUTANTS` table
(line 33) beside `green()` (line 129); the M24c/M24d anchor is split across
`.ufo/waves/round-83/count-c2.py:241-242`. Reported to the L1 (`agent://MoriR84`) as a blocker for
P-C1; the L1 landed pre-data amendment A2 (`39190f8a`), which corrects the three anchors and names
this seat's finding (`contract.md:163-168`).

### 2.2 After A2 — the declared freeze control reproduces

`git show --stat 39190f8a`: `contract.md +37`, `count-c1.py +10/-6` (the `MUTANTS` table only).
`count-c2.py` and `count-c3.py` are byte-unchanged since `daa77bd` (`git diff --stat daa77bd
39190f8a -- .ufo/waves/round-84/`).

Anchor counts with the A2 table: `M24a=1 M24b=1 M24c=1 M24d=1` at both `daa77bd` and `5adf4337`.

```
$ python3 -I .ufo/waves/round-84/count-c1.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4 --scratch "$S/pop3"
MUTANT count-c1.py M24a_killed_tally survived rc=0
MUTANT count-c1.py M24b_green_fail_token survived rc=0
MUTANT count-c2.py M24c_met_unclassified equivalent rc=0
MUTANT count-c2.py M24d_met_residual equivalent rc=0
C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 total=4 pristine=green detector=green rev=daa77bd5684c
exit=1
```

```
$ python3 -I .ufo/waves/round-84/count-c1.py --selftest --scratch "$S/det2"
PASS sensitive_killed mutants=1 killed=1 equivalent=0 survivors=0 total=1 pristine=green | MUTANT sensitive.py trip_guard killed rc=1
PASS blind_survives mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=green
PASS blind_case_tally mutants=2 killed=1 equivalent=0 survivors=1 total=2 pristine=green
PASS green_requires_fail_zero mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=red
PASS green_direct green() boundary
PASS killed_direct killed() boundary
PASS duplicate_anchor_excluded mutants=0 killed=0 equivalent=0 survivors=0 total=0 pristine=green
PASS empty_mutation_unmet mutants=0 killed=0 equivalent=0 survivors=0 total=0 pristine=green
PASS red_pristine_reported mutants=0 killed=0 equivalent=0 survivors=0 total=0 pristine=red
PASS equivalent_excluded_when_coupled mutants=1 killed=0 equivalent=1 survivors=0 total=1 pristine=green
PASS equivalent_requires_coupling mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=green
C1_COUNTER_SELFTEST pass=11 fail=0
exit=0
```

The two arms the P-C1 seat must land in `.ufo/waves/round-83/count-c1.py` are the detector's
`blind_case_tally` (`count-c1.py:201`) and `green_requires_fail_zero` (`:209`); the r83 subject
still has neither at this report's revision.

### 2.3 Entering record-sweep tool on the frozen C2 fixtures (row 170, green side)

The fixture generator is the frozen counter's own `build_fixture`/`fixture_verdicts`, imported from
`.ufo/waves/round-84/count-c2.py`; the old tool is `git show 5adf4337:tools/mori-record-sweep.py`.
Driver (run from `$S`, reproduced because the scratch dir is deleted):

```python
import importlib.util, os, subprocess, tempfile
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
ENTERING = "5adf4337b6510dd246b247092c11cbaa97c930d3"
S = "/fast/scratch/hyaku/mori-r84/Mo84S02Quality"
spec = importlib.util.spec_from_file_location(
    "count_c2_r84", os.path.join(LANE, ".ufo/waves/round-84/count-c2.py"))
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
old_dir = os.path.join(S, "tool-entering"); os.makedirs(os.path.join(old_dir, "tools"), exist_ok=True)
old_src = subprocess.run(["git", "-C", LANE, "show", ENTERING + ":tools/mori-record-sweep.py"],
                         capture_output=True, text=True, check=True).stdout
old_tool = os.path.join(old_dir, "tools", "mori-record-sweep.py")
open(old_tool, "w", encoding="utf-8").write(old_src)
new_tool = os.path.join(LANE, "tools", "mori-record-sweep.py")
work = tempfile.mkdtemp(dir=S, prefix="fixtures-")
greens = 0
for kind in ("carrier-ambiguous", "rev-ambiguous", "conformant"):
    new_rc, new_fields, new_out, old_rc = c2.fixture_verdicts(work, new_tool, old_tool, kind)
    details = [l for l in new_out.splitlines() if "MISMATCH" in l or "RECORD_SWEEP" in l]
    print("FIXTURE %-18s entering_rc=%d new_rc=%d new_revisions=%s %s"
          % (kind, old_rc, new_rc, new_fields.get("revisions"), details[:2]))
    if old_rc == 0 and kind in ("carrier-ambiguous", "rev-ambiguous"):
        greens += 1
print("ENTERING_GREEN_AMBIGUOUS=%d/2" % greens)
```

```
FIXTURE carrier-ambiguous  entering_rc=0 new_rc=0 new_revisions=0 ['RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=1 revisions=0']
FIXTURE rev-ambiguous      entering_rc=0 new_rc=0 new_revisions=0 ['RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=1 revisions=0']
FIXTURE conformant         entering_rc=0 new_rc=0 new_revisions=0 ['RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=1 revisions=0']
ENTERING_GREEN_AMBIGUOUS=2/2
```

`new_rc=0` is the lane **worktree** tool, which at run time was byte-identical to the entering tool
(`sha256 b5d3974ea9ee40acd4f37e4e5fb844249aff0293371e29848ab72f9f103dfc5e` both for
`git show 5adf4337:tools/mori-record-sweep.py` and `sha256sum tools/mori-record-sweep.py`). It is
**not** the all-rows tool: `grep -c ALL_ANCHOR_ROWS tools/mori-record-sweep.py` → `0` at report time.
The R-tool red side (`defeated=2`) was not executed.

### 2.4 The r83 live reading names no token (row 171, failure side)

```
$ git show 5adf4337:.ufo/waves/round-83/count-c2.py | grep -c LIVE_DELTA
0        # rc 1
```

The entering counter's tail prints only `live_tokens=%d live_agree=%d`
(`.ufo/waves/round-83/count-c2.py:243-246` at `5adf4337`, described at `:21`); the r83 record is
`live_tokens=63 live_agree=63` with no token named (`SCORECARD.md:4230` at `5adf4337`; capability
row `:4265`). The classifier and the four delta arms are not landed at report time
(`.ufo/waves/round-83/count-c2.py` byte-unchanged since `daa77bd`).

## 3. Verified / not verified

Verified by this seat (commands above): the pre-A2 population control and its three unanchored
anchors at four revisions; A2's effect (anchors unique, control `mutants=4 … survivors=2` rc 1);
the frozen detector selftest `pass=11 fail=0` rc 0; the entering record-sweep tool green on
`carrier-ambiguous` and `rev-ambiguous`; the absence of `LIVE_DELTA` and `ALL_ANCHOR_ROWS` at
report time; `QUALITY.md` append-only (79/0).

Not verified (and not claimed as passing): the R-tool red on the two ambiguous fixtures
(`defeated=2`); the after-arms `survivors=0`; the four C3 delta arms and any live census; the
record-sweep tool's 44-arm selftest. QUALITY 39 leaves each seat's selftest to the integration
owner; this seat ran no landed seat's new selftest.

## 4. Findings and conflicts

1. **Resolved by A2 — P-C1's frozen anchors did not occur exactly once.** Pre-A2 the population
   control read `mutants=1 killed=0 equivalent=0 survivors=1` with three `unanchored` extras;
   A2 (`contract.md:163-198`) corrects the three anchors and reproduces the declared control.
   The predicate, kill rule, equivalence map, coupling markers and target are byte-unchanged in
   A2; only the anchor strings changed. This seat edited no tool.
2. **Open, recorded only — P-C3 sentence vs counter.** `.ufo/waves/round-84/count-c3.py:196`
   requires `tokens == 64`, while `contract.md:122-124` says the counter's `met` "never requires a
   particular token count, only that every token in the union is classified exactly once and that
   `agreed` equals the counter's `live_agree`". The target line itself carries `tokens=64`
   (`contract.md:112-113`), so the counter matches the target line and contradicts the sentence.
   No claim or counter was changed here.
3. **Historical provenance (r83 record, not rewritten) — the frozen table copied prose as an
   anchor.** `.ufo/waves/round-83/w1/Mo83R01C1.md:235-236` states both c1/c2 anchors were
   "verified unique by the driver before mutation"; the committed r83 bytes show the M24b anchor
   twice and the M24c/M24d shorthand never. A2 names the root cause ("quoted prose",
   `contract.md:170-174`). This is a finding against the r83 report's provenance claim, reported
   verbatim; the r83 bytes were not edited by this seat.

## 5. Bounds and tooling

- Writes: `corpus/QUALITY.md` (rows 170–172), this report, and scratch under
  `/fast/scratch/hyaku/mori-r84/Mo84S02Quality` (removed before yield). No `/tmp` writes.
- Read-only git only: `rev-parse`, `log`, `show`, `show --stat`, `diff --stat`, `diff --numstat`,
  `status`, `merge-base --is-ancestor`. No `add`/`commit`/`checkout`/`reset`/`stash`/`push`, no jj.
- No packages installed or upgraded (pacman paused host-wide; no `uv`/`npx` used).
- No subagent dispatch, no lane/OS/unit/service/credential/harness state touched. Detection and
  report only.
