# Mo94K01Crit — round-94 attempt 1, wave w1 (critic: falsify C1 and C2)

Freeze `6b65e7c1` is an ancestor of lane HEAD `4ae1678d` (later commit adds only the w1 spec/dispatch/registry). Lane not edited. Installs: none.
Scratch `S=/fast/scratch/hyaku/mori-r94/Mo94K01Crit` (clone `$S/clone` at freeze, toplevel asserted; `$S/atk/clone` for fixtures; `TMPDIR=$S/tmp`, `HYAKU_SCRATCH=$S/hs`). Removed; confirmed absent.
`F=/home/vgpnk/Projects/shokunin`, `L=$F/mori-shokunin`.
## 0. Freeze and pins (read-only)
```
git -C $L show --stat 6b65e7c1  -> 9 files, +667, all under .ufo/waves/round-94/
git -C $L diff --stat 84b15230 6b65e7c1  -> same 9 files; no corpus/, SCORECARD, LOG, tools/ path
git -C $L rev-parse <rev>:.ufo/waves/round-93/count-c1.py   -> 45a9d07dc4a1d9be905d847e2e34fa1d9faea2f4 (pin; same at base and freeze)
  count-c2.py -> 7d0a003cf82162b02e9f740f81bfd200f91c6d3c ; controls-r93.sh -> be60882e947fc1827af62f69207f9f9a9f5630f1
```

## 1. C1 calibration
### 1a. Controls battery, fresh run (frozen controls-r94.py, clone at freeze)
```
HYAKU_SCRATCH=$S/hs python3 -I $S/clone/.ufo/waves/round-94/controls-r94.py $S/clone $F
CTRL do-nothing v1=C1=met v2=C1=met
CTRL do-nothing v2_line=C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=84b152308fa6
CTRL left/right/middle: v1=C1=met v2=C1=unmet ... adm_ok=18 adm_fail=1 ... checks_failed=admission
EMBED_FALSE_PASS v1=3/3 v2=0/3 live_v2=met do_nothing_v1=C1=met do_nothing_v2=C1=met
controls_rc=0   (script prints no such line; rc observed 0)
```
Matches `evidence/controls-r94.txt` on every verdict and count (fixture revs differ: commit timestamps).

### 1b. Frozen v1 at base, direct (count-c1.py line 141: `ac[:7] in va`)
```
TMPDIR=$S/tmp python3 -I $S/count-c1-r93.py 84b152308fa6c2f224ad75dff68e525dab9057ac --repo $S/clone
C1=met trio=98 claim_r92_true=1 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=84b152308fa6   rc=0
```
### 1c. v2 on live data
```
SHOKUNIN_ROOT=$F TMPDIR=$S/tmp python3 -I $S/clone/.ufo/waves/round-94/count-c1v2.py 6b65e7c1 --repo $S/clone --report
C1_REPORT rev=6b65e7c11f31 trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12/12 seven_same=7/7 census_rc=0 failures=-   rc=0
```
### 1d. Forgery sweep beyond the three frozen fixtures (scratch commits on counter-win-r77.md, base 84b15230)
| variant | first verified-at token | v1 | v2 | first token names the admission commit? |
|---|---|---|---|---|
| a full hash | `6a230c4b` | met | met | yes |
| b 7-char prefix | `6a230c4` | met | met | yes (legit short) |
| c 6-char prefix | `6a230c` | unmet | unmet | no (<7) |
| d full hash + comma | `6a230c4b,` | met | **unmet** | arguably yes: v2 false reject |
| e prefix7 + `zz` | `6a230c4zz` | **met** | unmet | no (embedded) |
| f wrong token, hash later | `00000000 6a230c4b` | **met** | unmet | no |
| g hash char 8 mutated | `6a230c40` | **met** | unmet | no |
Driver: `python3 -I $S/atk/drive.py $S/atk/clone $S/atk`, then `count-c1v2.py <rev> --repo $S/atk/clone` and `count-c1-r93.py <rev> --repo $S/atk/clone` per rev.
Result: v1 false-passes the 3 frozen fixtures and e, f, g. v2 rejects all 6 forged shapes, with one false reject (d).

### 1e. Verdict and the Mo93R03Atk reading (corpus/lessons/round-93-verifier-spotcheck.md §2)
- The attack calls the round-93 repair bookkeeping (data changed to fit prose). Round 94 changes **no data**: freeze adds no `corpus/knowledge/` byte; live v2 reads 19/19 at base and freeze, same as v1. Only the counter's verdict moves.
- Rebuttal rests on 1d: v1 certifies "each verified-at names the admission commit" **true** for e, f, g, where the sentence is false. v2 reads it false. That is the AXES calibration signal (self-assessment matches observed state; overreach caught), not a relabel of the same facts. The data-repair objection concerns round-93 lines, which round 94 does not re-claim.
- Accepted limit: v2 checks form (first token is a prefix of the git-derived hash), not provenance; the contract names this. Content verification is not claimed.
- Accepted cost: d is a false reject, not a false pass; no live file has it.
- Kill rules (observed): v2 false-pass 0/3 battery and 0/6 extra; live adm_fail 0; v1 battery 3/3; census ok. None fires. Do-nothing (keep v1) reads 3/3 false pass, so the predicate fails.
**C1: admit-candidate, scoped to calibration of the self-check instrument.**

## 2. C2 operability
### 2a. Predicate at freeze (outer `env -u HOME`)
```
env -u HOME TMPDIR=$S/tmp python3 -I $S/clone/.ufo/waves/round-94/count-c2v2.py 6b65e7c1 --repo $S/clone --root $F
C2=met literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2 rev=6b65e7c11f31   rc=0
```
### 2b. Do-nothing (entering base; no round-94 counters)
```
env -u HOME TMPDIR=$S/tmp python3 -I $S/clone/.ufo/waves/round-94/count-c2v2.py 84b15230 --repo $S/clone --root $F
C2=unmet literal_r94=0 files_r94=0 frozen_r93=unchanged env_i=unmet env_unset=rc2 checks_failed=files,env_i rc=1
```
Unmet, but by absence.
### 2c. `env_unset=rc2` does not measure fail-closed
`python3 -I $S/no-such-counter.py` -> "can't open file", rc=2. At do-nothing `env_unset` passes only because Python exits 2 on a missing script. Real fail-closed, observed:
```
env -i PATH=$PATH HOME=/nonexistent TMPDIR=$S/tmp python3 -I $S/clone/.ufo/waves/round-94/count-c1v2.py 6b65e7c1 --repo $S/clone
C1_SETUP census path unset: give --census or set SHOKUNIN_ROOT   rc=2
```
### 2d. Literal arm
```
count-c2v2.py 6b65e7c1 --repo $S/clone --report --scan .ufo/waves/round-93  -> C2_REPORT ... literal=6 files=5   (round-93, frozen, host-bound)
count-c2v2.py 6b65e7c1 --repo $S/clone --report                              -> C2_REPORT ... scan=.ufo/waves/round-94 literal=0 files=3
```
Positive control: scratch commit adds `.ufo/waves/round-94/lit-positive-control.py` containing `/home/vgpnk/Projects/shokunin`; the counter on that rev -> `C2=unmet literal_r94=1 files_r94=4 ... checks_failed=literal,env_i`. The literal arm fires.
Also observed: `env_i` couples to C1 live data. In that tree C1 read unmet (adm_fail=1 from sweep variant g in ancestry), so `env_i=unmet`. An operability check that fails when a knowledge line changes is not measuring operability.

### 2e. Host independence and HOME
```
SHOKUNIN_ROOT=$S/fleet2 env -u HOME TMPDIR=$S/tmp python3 -I $S/clone/.ufo/waves/round-94/count-c1v2.py 6b65e7c1 --repo $S/clone
  -> C1=met ... census=ok rc=0   ($S/fleet2/scripts/sources-census.sh = copy of the census)
env -u HOME TMPDIR=$S/tmp python3 -I $S/count-c1-r93.py 84b15230 --repo $S/clone
  -> C1=met ... census=ok rc=0   (round-93 v1 already runs with HOME unset)
grep -nE "/home/|vgpnk" $F/scripts/sources-census.sh -> no matches (rc=1)
```
HOME was never a dependency of either counter. The host dependency the move removes is the round-93 `CENSUS` literal (`count-c1.py:39`, `count-c2.py:39`), replaced by `SHOKUNIN_ROOT` in v2. That replacement is real.

### 2f. Verdict: NOT-ADMIT as framed (no operability move on an existing artifact)
- No literal was moved. Round-93 counters keep `/home/vgpnk` (frozen). Lane-wide host-literal count over runnable counters: 6 before (2d), 6 after. The predicate's `literal_r94=0` is true of three files created this round.
- The C2 "before" is absence (2b: files=0). "Met" is produced by new files that run off-host: a capability/coverage fact, not an operability move on the same artifact.
- HOME independence pre-dates round 94 (2e). The HOME clause is not a change.
- Defects (observed): env_unset passes on a missing counter (2c); claim text says "HOME unset" but the counter sets `HOME=/nonexistent` (`count-c2v2.py:106`); env_i couples to C1 data (2d); scan covers `.py`/`.sh` only, while `contract.md:20` and `evidence/entering-c2-r94.txt` carry the literal in prose.
- Would change the verdict: a before→after on a pre-existing host-bound counter (e.g. round-93 unmet on a host without `/home/vgpnk`, met after an append-only successor), or a restatement as a capability row with first-working round.

## 3. Harm check (freeze; landing is prospective)
- Freeze touches only round-94 files. No SCORECARD, LOG, corpus/ or tools/ row changed; no score moved at the freeze.
- Landing risk (adjacency and calibration, not a score move): the planned `.gitignore` rule for `*.ready.dispatched` (`evidence/gitignore-red-before.txt`: `check_ignore_rc=1`) would hide the round-93 D3 finding. Live `git -C $L status --porcelain` shows `?? .ufo/waves/round-92/w1.ready.dispatched`, `?? .ufo/waves/round-93/w1.ready`, `?? .ufo/waves/round-94/w1.ready`. Round-93 D3 routed these to "commit or move", not "ignore". Recommend the landing routes D3 or names the exception.
- Expected score moves: C1 calibration only, if admitted. C2 operability: none on existing artifacts.

## 4. Kill-rule check
| claim | kill rule | measured by | fires on do-nothing? |
|---|---|---|---|
| C1 | v2 false-passes battery / live adm_fail / census | controls `v2=0/3`; count-c1v2 `adm_fail=0 census=ok` | no |
| C1 | v1 battery expectation fails | controls `v1=3/3` | no |
| C2 | literal_r94 > 0 | count-c2v2 `--report` | no (arm proven by 2d) |
| C2 | files_r94 < 3 | count-c2v2 `files_r94` | **yes** (0 at base) |
| C2 | frozen_r93 changed | count-c2v2 `frozen_r93` | no |
| C2 | env_i unmet | count-c2v2 `env_i` | **yes** (unmet at base) |
| C2 | env_unset not rc2 | count-c2v2 `env_unset` | no, but vacuous at absence (2c) |
All kill rules are measurable from the frozen commands. C2's `files` and `env_i` rules fire on do-nothing (correct). No C1 kill rule is satisfied by doing nothing.

## 5. Verdicts
- C1 calibration: **admit-candidate**, scoped to the instrument (1e). Proof: 1a, 1c, 1d.
- C2 operability: **not-admit as framed** (2f). Proof: 2a–2e.
- No other axis moved at the freeze (3). Landing `.gitignore` plan flagged (3).
