# Mo94M02Mut — mutation-test battery on count-c2v2.py (round 94, wave w1)

Mutants are edits to a COPY of the frozen `count-c2v2.py` only; every copy ran in a fixture clone of
the freeze commit `6b65e7c11f318481d5efa0429cdabb50743a2cc2`, one fixture commit per mutant
(parent = freeze, verified). Scratch `$S=/fast/scratch/hyaku/mori-r94/Mo94M02Mut`; clones
`git clone --shared --no-checkout`; every run passed `TMPDIR=$S/tmp` explicitly. No tools installed.

## Gate: unmutated copy at the freeze commit

    TMPDIR=$S/tmp python3 -I $S/work/count-c2v2.py 6b65e7c11f31... --repo $S/fx --root /home/vgpnk/Projects/shokunin

    C2=met literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2 rev=6b65e7c11f31   rc=0

Gate OK — battery proceeded. Pristine copy sha256 `e293ed7d1331…53394` == frozen blob
(`git rev-parse 6b65e7c:.ufo/waves/round-94/count-c2v2.py` = `47513565c36b`, byte-equal by `git show`).

## Battery at the freeze commit (kill rule: KILLED iff verdict or exit != C2=met/0)

Run form per row: `TMPDIR=$S/tmp python3 -I $S/work/mut_<m>.py <commit> --repo $S/fx --root /home/vgpnk/Projects/shokunin`

| mut | change to copy | commit    | observed line (trailing `rev=` dropped)                                                       | rc | verdict |
|-----|----------------|-----------|-----------------------------------------------------------------------------------------------|----|---------|
| m1  | drop `"HOME": "/nonexistent"` from base_env | 71d0e74035e0 | `C2=met literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2`        | 0  | SURVIVED |
| m2  | remove `if not frozen: fails.append("frozen")` | cdb0c04d4aa8 | `C2=met literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2`       | 0  | SURVIVED |
| m3  | remove `if not env_unset_rc2: fails.append("env_unset")` | 3d4780b77f56 | `C2=met literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2`      | 0  | SURVIVED |
| m4  | HOST regex `rb"/home/[a-z_][a-z0-9_-]*"` → `rb"/home/"` | bb124fef58f3 | `C2=unmet literal_r94=2 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2 checks_failed=literal` | 1 | KILLED |
| m5  | `if files < 3:` → `if files < 0:` | 9d3b09a14e6e | `C2=met literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2`        | 0  | SURVIVED |
| m6  | remove `if not env_i: fails.append("env_i")` | d271dd591d02 | `C2=met literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2`        | 0  | SURVIVED |
| m7  | drop `"SHOKUNIN_ROOT": args.root` from base_env | 62a2cb27fd2f | `C2=unmet literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=unmet env_unset=rc2 checks_failed=env_i` | 1 | KILLED |

Killed 2/7 (m4, m7). Mutant sha256 prefixes: m1 `5c03fa8eaff9`, m2 `8f58b7b7e415`, m3 `572d00b6a233`,
m4 `c46344f9039b`, m5 `1877b93c90e2`, m6 `e1be1e24debf`, m7 `cace2b360be6`.

## m4 kill detail (self-scan)

The loosened regex matches the counter's own text: `re.findall(rb"/home/", …)` over the frozen copies
gives `count-c2v2.py: 2` (its docstring `/home/<user>` and its own HOST literal), `count-c1v2.py: 0`.
Under the frozen user-class regex neither matches (`<` and `[` are outside `[a-z_]`), so `literal_r94`
jumps 0→2 and the mutant flags itself.

## Survivor localization (bounded probes in the same fixture; scripts run from $S/work)

| probe | fixture | pristine copy | mutant copy |
|-------|---------|---------------|-------------|
| P_m2, commit f92b616793b6 (append 1 line to `.ufo/waves/round-93/count-c1.py`) | touched R93 blob | `C2=unmet … frozen_r93=changed … checks_failed=frozen` rc=1 | m2: `C2=met … frozen_r93=changed` rc=0 |
| P_m5, commit 5f5cf8e5dbe5 (`git rm .ufo/waves/round-94/controls-r94.py`) | files_r94=2 | `C2=unmet … files_r94=2 … checks_failed=files` rc=1 | m5: `C2=met … files_r94=2` rc=0 |
| P_m6, `--root $S/emptyroot` (empty dir) at freeze | census unresolvable | `C2=unmet … env_i=unmet … checks_failed=env_i` rc=1 | m6: `C2=met … env_i=unmet` rc=0 |

So m2/m5/m6 guards are real but unexercised by the frozen battery: the battery runs only at the freeze
commit, where `frozen=unchanged`, `files=3`, and `env_i=met` hold by construction. Each survivor is a
control-battery gap (contract's kill line), not a predicate defect.

## Vacuity findings (no fixture can diverge)

- **m1** — `count-c1v2.py` never reads HOME. Direct child runs at the freeze (same child invocation the
  counter makes: `python3 -I count-c1v2.py 6b65e7c… --repo $S/fx`, env `HOME=/nonexistent`+`SHOKUNIN_ROOT`
  vs HOME absent): both `C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok` rc=0.
  P-C2's "runs with HOME unset" half is certified by construction, not tested by `env_i`; dropping the
  HOME pin is unobservable on any fixture.
- **m3** — `unset_env` is `base_env` minus `SHOKUNIN_ROOT`, and the child exits 2 whenever census is None
  (observed: `C1_SETUP census path unset: give --census or set SHOKUNIN_ROOT` rc=2). `env_unset=rc2` is
  therefore invariantly true; removing the check cannot change any verdict on any fixture.

## NOT RUN

Nothing — gate, 7 mutants, 6 probes, 3 child runs all executed as shown.

## Restoration evidence

- `git -C <lane> status --porcelain --untracked-files=no` after the battery: empty (tracked lane untouched).
- Lane counters after: `count-c2v2.py e293ed7d1331…53394`, `count-c1v2.py 6eb7fa4cf0ec…7b384` — identical to before.
- All 7 mutant commits' parent == `6b65e7c11f31`; mutants existed only under `$S` (deleted before yield).
- Host changes: none (no sysctls, no pacman, no installs).
