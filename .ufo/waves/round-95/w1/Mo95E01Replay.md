# Seat Mo95E01Replay — independent replay of C1 and C2 at the freeze

Round 95 attempt 1, wave w1, role executor. Freeze commit `2dc476d7fdb68bf916685a9f217a92047662baeb`.
All runs independent of every other seat; no counter, predicate, fixture or frozen file was edited.

## 1. Setup

Scratch: `S=/fast/scratch/hyaku/mori-r95/Mo95E01Replay` (`HYAKU_SCRATCH` unset → default used). `TMPDIR=$S` passed explicitly to every counter invocation below. Clone made with read-only git in scratch only; no mutating git command touched the lane, fleet root, or shokuknow.

```
$ git clone --no-local --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin $S/clone   → rc=0
$ git -C $S/clone checkout -q --detach 2dc476d7fdb68bf916685a9f217a92047662baeb             → rc=0
$ git -C $S/clone rev-parse HEAD
2dc476d7fdb68bf916685a9f217a92047662baeb
```

## 2. Pin verification (lane repo, read-only `git show` at the freeze commit)

| File | got sha256 | expected sha256 | MATCH | lane worktree == frozen bytes |
|---|---|---|---|---|
| `.ufo/waves/round-95/count-c1.py` | `6c288d70c39a5736b6aba0b4a0525159010124c0b5494f047a10aab6dfeaa450` | `6c288d70…aa450` | True | True |
| `.ufo/waves/round-95/count-c2.sh` | `014980bc82b71b7a48764b45e7e550050e928956a32cd6e4ef3b4208aa844b9f` | `014980bc…44b9f` | True | True |
| `.ufo/waves/round-94/count-c1v2.py` (pristine counter) | `6eb7fa4cf0ecf86064bb2714a5b93b52bf3356dc6e38e5dc7ee51f7255a7b384` | `6eb7fa4c…7b384` | True | True |

All three pins reproduce; the lane working tree holds the frozen bytes for each.

## 3. C1 replay — `P-C1r95`

Command (exact):

```
TMPDIR="$S" python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-95/count-c1.py \
  2dc476d7fdb68bf916685a9f217a92047662baeb \
  --lane /home/vgpnk/Projects/shokunin/mori-shokunin \
  --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
```

Every stdout line:

```
C1=met survivors=0 killed=7/7 before_r94_survivors=4 r94_survivor_ids=m2,m3,m4,m6 after_survivor_ids=- pristine=green equiv=m5(declared) crash_ids=-
KILL m1 by=R94-L,R94-R,R94-M
KILL m1b by=R94-L,R94-R,R94-M
KILL m2 by=R95-LEN
KILL m3 by=R95-CEN
KILL m4 by=R95-TRIO
KILL m6 by=R95-PAT
KILL m7 by=R94-L,R94-R,R94-M
PRISTINE R94-L C1=unmet 1 admission
PRISTINE R94-R C1=unmet 1 admission
PRISTINE R94-M C1=unmet 1 admission
PRISTINE R95-LEN C1=unmet 1 admission
PRISTINE R95-CEN C1=unmet 1 census
PRISTINE R95-TRIO C1=unmet 1 trio
PRISTINE R95-PAT C1=unmet 1 patched12
```

Exit code: **0**. Expectation reproduced exactly: `C1=met survivors=0 killed=7/7`, pristine green, exit 0. Before field recorded: `before_r94_survivors=4`, `r94_survivor_ids=m2,m3,m4,m6` — matches the frozen before data (round-94 probe survivors m2, m3, m4, m6). Per-mutant kills land on the declared fixtures: m2→R95-LEN, m3→R95-CEN, m4→R95-TRIO, m6→R95-PAT, m1/m1b/m7→the three R94 hash fixtures. m5 listed as `equiv=m5(declared)`, never counted as killed. `after_survivor_ids=-`, `crash_ids=-`.

## 4. C2 replay — `P-C2r95`

Command (exact):

```
TMPDIR="$S" bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-95/count-c2.sh \
  2dc476d7fdb68bf916685a9f217a92047662baeb \
  /home/vgpnk/Projects/shokunin/mori-shokunin \
  /home/vgpnk/Projects/shokunin
```

Every stdout line:

```
HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=2dc476d7fdb6
```

Exit code: **0**. Expectation reproduced: `hidden=1` (account home absent in the `unshare -rm` tmpfs), the round-93 counter fails inside the namespace (`before=C1=unmet(rc=1)`), the round-94 counter succeeds inside it (`after=C1=met(rc=0)`), and the round-93 positive control outside the namespace succeeds (`control_outside=C1=met(rc=0)`). No host sysctl, mount, or package was touched by this seat; the namespace work happened inside the frozen counter's own `unshare -rm`.

## 5. Do-nothing control replay (round-94 battery alone, from the clone)

Command (exact):

```
TMPDIR="$S" python3 -I $S/clone/.ufo/waves/round-94/controls-r94.py \
  /home/vgpnk/Projects/shokunin/mori-shokunin \
  /home/vgpnk/Projects/shokunin
```

Every stdout line:

```
CTRL do-nothing v1=C1=met v2=C1=met
CTRL do-nothing v1_line=C1=met trio=98 claim_r92_true=1 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=84b152308fa6
CTRL do-nothing v2_line=C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=84b152308fa6
CTRL left rev=2e4a525ab223 v1=C1=met v2=C1=unmet v2_line=C1=unmet trio=98 files=19 adm_ok=18 adm_fail=1 patched12=12 seven_same=7 census=ok checks_failed=admission rev=2e4a525ab223
CTRL right rev=d86a9b86b32e v1=C1=met v2=C1=unmet v2_line=C1=unmet trio=98 files=19 adm_ok=18 adm_fail=1 patched12=12 seven_same=7 census=ok checks_failed=admission rev=d86a9b86b32e
CTRL middle rev=cdf5dd0e91ff v1=C1=met v2=C1=unmet v2_line=C1=unmet trio=98 files=19 adm_ok=18 adm_fail=1 patched12=12 seven_same=7 census=ok checks_failed=admission rev=cdf5dd0e91ff
EMBED_FALSE_PASS v1=3/3 v2=0/3 live_v2=met do_nothing_v1=C1=met do_nothing_v2=C1=met
```

Exit code: **0**. Stated plainly: the control's own expectation `EMBED_FALSE_PASS v2=0/3` (0 of 3 embedded-hash fixtures make the v2 counter falsely pass) exercises the round-94 fixtures only — it does **not** exercise any of the seven round-95 mutants (m1, m1b, m2, m3, m4, m6, m7) or the R95-LEN/CEN/TRIO/PAT fixtures; the mutant kills in §3 come solely from the frozen `count-c1.py` battery. Consistently with the C1 claim, the round-94 battery's do-nothing line is `v2=C1=met` while the §3 battery observes those four mutants surviving it (`before_r94_survivors=4`).

## 6. Tooling authorization

No tool was installed or upgraded. Only `python3`, `bash`, `git` (read-only), and `sha256` were used, all pre-existing.

## 7. Host guard / scope compliance

- Write scope used: this report file and `$S` only. No tracked lane file, `.ufo/state`, `MANIFEST.json`, fleet-root file, or sibling lane touched.
- No mutating git/jj command anywhere; fixture work confined to scratch.
- No sudo, no sysctl/mount/service/package change; the only namespace use was inside the frozen C2 counter's own `unshare -rm`.
- Scratch `S` deleted after these runs (`rm -rf -- $S`); nothing left under `/fast/scratch/hyaku/mori-r95/Mo95E01Replay`.

## Verdict

Every stated expectation reproduced at the freeze commit: pins MATCH (3/3), C1 `C1=met survivors=0 killed=7/7` exit 0 with before `m2,m3,m4,m6`, C2 `HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0)` exit 0, control `EMBED_FALSE_PASS v2=0/3` exit 0. Nothing differs.

SEAT Mo95E01Replay REPLAYED
