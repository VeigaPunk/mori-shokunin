# Mo95Lab01 — labrat probe H1 (round 95, wave w1)

Seat: Mo95Lab01 (revenger / labrat probe; leaf, no subagents). Lane HEAD entering: `754f4991198c16ddd1d4a3ea9206cfb7d74d6827`.
Frozen revision used: `2dc476d7fdb68bf916685a9f217a92047662baeb` (checked out detached in a `git clone --no-local --no-checkout` under scratch; `git rev-parse --show-toplevel` = clone dir before first use).
Scratch: `/fast/scratch/hyaku/mori-r95/Mo95Lab01` (`HYAKU_SCRATCH` unset, default used). Deleted by the driver's `trap ... EXIT` (verified below). Every counter run passed `TMPDIR` explicitly.

## Hypothesis

**H1.** The round-93 counter's C2 "before" verdict (`C1=unmet` inside the namespace) is caused **only** by the census path under the account home directory being absent, and **not** by the counter's logic. The counter's only host-bound input is `CENSUS = /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`.ufo/waves/round-93/count-c1.py`, module constants; the file has no other absolute path).

## Prediction (written before the run)

- With a copy of the census placed at the literal path inside the namespace (after the tmpfs mount, same `unshare -rm` command), round-93 counter prints `C1=met` and rc 0.
- Falsifier arm: the same placement of a census stub that exits 1 prints `C1=unmet` with `census` in `checks_failed`. If it printed `C1=met`, H1 is refuted.
- Second arm: round-94 counter with `--census` pointing at the stub at the literal path prints `C1=unmet` with `census` failing.

## Procedure as run (and one deviation)

Namespace wrapper (`ns`, verbatim from the driver):

```sh
env -i PATH="$PATH" HOME="$S/home" TMPDIR="$S" \
  unshare -rm sh -c '
    home=$1; stage=$2; shift 2
    mount -t tmpfs tmpfs "$home" || { echo "NS mount failed"; exit 97; }
    lit="$home/Projects/shokunin/scripts/sources-census.sh"
    echo "NS literal_after_mount=$( [ -e "$lit" ] && echo present || echo absent )"
    if [ "$stage" != - ]; then
      mkdir -p "$home/Projects/shokunin/scripts" && cp "$stage" "$lit" || { echo "NS copy failed"; exit 98; }
      echo "NS literal_after_copy=$( [ -e "$lit" ] && echo present || echo absent ) sha=$(sha256sum "$lit" | cut -c1-12)"
    fi
    exec "$@"
  ' sh "$HOME_DIR" "$stage" "$@"
```

**Deviation.** The procedure says to copy `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` to the literal path *inside* the namespace. The source lies under the home directory, so the tmpfs mount hides it; a copy made after the mount cannot read it. The copy was therefore staged from a scratch file made *before* the namespace (`cp` on the host, sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` for both source and stage, checked in the driver output), and the copy inside the namespace happens after the mount. The bytes at the literal path are identical to the host census. The predicate and prediction are unchanged.

## Observed (exact lines; rc = exit status of the command under `unshare`)

Host preconditions:
```
3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  /fast/scratch/hyaku/mori-r95/Mo95Lab01/stage/census-real.sh
host literal census exists outside ns: yes
clone HEAD=2dc476d7fdb68bf916685a9f217a92047662baeb
getent home=/home/vgpnk
```

| Arm | Command (round-93 unless noted) | Observed | rc |
|---|---|---|---|
| A0 positive control | outside namespace | `C1=met trio=98 claim_r92_true=1 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=2dc476d7fdb6` | 0 |
| A1 no copy | in ns, nothing staged | `NS literal_after_mount=absent` / `C1=unmet trio=98 ... seven_same=7 census=rc127 checks_failed=census rev=2dc476d7fdb6` | 1 |
| **A2 HYPOTHESIS** | in ns, real census copied to literal path | `NS literal_after_mount=absent` / `NS literal_after_copy=present sha=3fb7261569f4` / `C1=met trio=98 ... seven_same=7 census=ok rev=2dc476d7fdb6` | 0 |
| A3 FALSIFIER | in ns, stub `exit 1` at literal path (sha `fa5057ab7da9`) | `NS literal_after_copy=present sha=fa5057ab7da9` / `C1=unmet trio=98 ... census=rc1 checks_failed=census rev=2dc476d7fdb6` | 1 |
| A4 extra control | in ns, stub `exit 0` at literal path (sha `fc138bcff5ca`) | `NS literal_after_copy=present sha=fc138bcff5ca` / `C1=met trio=98 ... census=ok rev=2dc476d7fdb6` | 0 |
| **B1 SECOND ARM** | round-94 `count-c1v2.py --census <literal>`, in ns, stub exit 1 at literal path | `NS literal_after_copy=present sha=fa5057ab7da9` / `C1=unmet trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=rc1 checks_failed=census rev=2dc476d7fdb6` | 1 |
| B2 round-94, nothing staged | in ns, `--census <literal>` absent | `NS literal_after_mount=absent` / `C1=unmet trio=98 ... census=rc127 checks_failed=census rev=2dc476d7fdb6` | 1 |
| B3 round-94, real copy | in ns, `--census <literal>`, real copy | `NS literal_after_copy=present sha=3fb7261569f4` / `C1=met trio=98 ... census=ok rev=2dc476d7fdb6` | 0 |
| C cross-check | frozen `count-c2.sh 2dc476d7… <lane> <fleet>`, TMPDIR explicit | `HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=2dc476d7fdb6` | 0 |

Driver exit: `DRIVER_EXIT=0`. Each arm's rc is the rc of the counter process (`unshare -rm` execs the command; the driver's `echo "rc=$?"` follows each arm).

## Verdict

**H1 SUPPORTED.**

- Prediction A2 held: with the census at the literal path inside the namespace, round-93 counter printed `C1=met` and rc 0.
- Falsifier A3 held: a census stub exiting 1 at the same path gave `C1=unmet ... census=rc1 checks_failed=census`, rc 1. The counter did not print `C1=met`, so the falsifier did not refute H1.
- Second arm B1 held: round-94 counter with `--census` on the stub gave `C1=unmet ... checks_failed=census`, rc 1.
- A4 adds a control: with an exit-0 census at the same path, the round-93 counter in the namespace gives `C1=met` rc 0. So every non-census check passes inside the namespace; the census return code at the literal path is the only namespace-sensitive input. This is what "the cause is the path, not the logic" rests on.
- The absent-path vs present-but-failing distinction is visible in the rc: absent gives `census=rc127` (A1, B2), a present failing stub gives `census=rc1` (A3, B1). Both are `C1=unmet`.

## Limits

1. **The copy changes the namespace.** It adds a file at the literal path and creates `Projects/shokunin/scripts/`. The test therefore shows the verdict depends on the file at that path (its exit status), and that nothing else in the counter flips. It does not show the counter is host-free on paths other than the one constant; the round-93 source contains only the `CENSUS` literal among absolute paths, but a second literal elsewhere would not be caught by this probe. Only A0/A4 bear on the logic: they show the other checks pass in the namespace when the census returns 0.
2. **Staging deviation** as described above: the copy is from a host-side staged file, not from the home-directory path after the mount (the source is hidden by the mount). Content is byte-identical (same sha256).
3. **The census's root.** `sources-census.sh validate --file` derives `ROOT` from `dirname $0/..` when `SHOKUNIN_ROOT` is unset (census line 88). The copy's directory creation is part of the test, so this probe does not separately test whether the census needs anything else under its root; it did not, since A2/B3 passed with exit 0.
4. **Single run per arm**; no repetition or timing variance measured. The probe does not test `user_namespaces(7)` availability beyond the fact that `unshare -rm` ran here (`/proc/sys/user/max_user_namespaces` = 122865, read-only).
5. The probe changes no tracked file, sysctl, mount outside its own namespace, or package. No subagents were used.

## Tools

None installed, upgraded, or removed. (`unshare` util-linux 2.42.4, `/usr/bin/python3`, `/usr/bin/bash`, `/usr/bin/git` were used as found.)

## Cleanup

Scratch `/fast/scratch/hyaku/mori-r95/Mo95Lab01` removed by the driver's `trap 'rm -rf -- "$S"' EXIT` (see check below). A temporary copy of the driver at `/tmp/mo95lab01-driver.sh` (4053 bytes, under 50 MB) was removed after the run.
