# Mo95R02Atk — C2 attack (reviewer), round 95 wave w1

Seat: Mo95R02Atk (reviewer). Target: predicate **P-C2r95** at freeze commit
`2dc476d7fdb68bf916685a9f217a92047662baeb` (lane `.ufo/waves/round-95/count-c2.sh`, contract §C2).
Lane read-only throughout; scratch `/fast/scratch/hyaku/mori-r95/Mo95R02Atk` (deleted on exit).

**Verdict: HOLDS** — C2 measures what P-C2r95 says, with the limits named below (one demonstrated, B4).

## Baseline (frozen counter at the freeze commit)

```
$ TMPDIR=$S bash <lane>/.ufo/waves/round-95/count-c2.sh \
    2dc476d7fdb68bf916685a9f217a92047662baeb <lane> /home/vgpnk/Projects/shokunin
HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=2dc476d7fdb6
baseline_rc=0
```

Matches the before receipt (`evidence/before-c2-r95.txt` line 1: same four fields, `census_sha=3fb7261569f4`,
`rev=754f4991198c` there because it was taken at entering HEAD; the census hash is identical).

## B1 — Hidden verification (independent)

Own clone `…/Mo95R02Atk/b1clone` (toplevel asserted), detached at the freeze commit, probed with my own
`unshare -rm` + tmpfs-over-home (same mechanism as the counter, independently driven):

```
probe_absent=yes        # /home/vgpnk/Projects/shokunin/scripts/sources-census.sh gone
fleet_root_absent=yes   # the whole fleet root is under the home dir, so it vanishes too
scratch_present=yes     # /fast/scratch survives (outside home)
usrbin_present=yes
git_log_inside=[2dc476d7 round-95: frozen contract, C1 battery counter, C2 namespace counter, before receipts]
```

The lane clone is readable and `git log` works inside the namespace — the clone (made before entering,
like count-c2.sh does) is the only repo access needed. **Probe-honesty note:** my first probe also ran
`git cat-file -e <clone-path>^{commit}`, which rc=128'd because I passed a path, not a rev — my arg error,
not a namespace effect; corrected in B6 (`rev-parse HEAD^{commit}` → full hash, see below).

## B2 — Literal scan (freeze-commit bytes via `git show`)

```
$ for f in .ufo/waves/round-94/count-c1v2.py .ufo/waves/round-94/count-c2v2.py \
      .ufo/waves/round-94/controls-r94.py .ufo/waves/round-95/count-c1.py .ufo/waves/round-95/count-c2.sh; do
    git show 2dc476d…:"$f" | grep -nE '/home/[a-z]|vgpnk'; done
== each of the five files: (grep rc=1) — no hits
```

**count-c2.sh: zero host literals — as expected. The round-94 counters (count-c1v2.py, count-c2v2.py,
controls-r94.py) also have zero.** The only host literal among the counters is the *before* artifact:
round-93 `count-c1.py:39` `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`, consumed at
line 150 (`bash CENSUS validate --file …`). count-c1v2.py's docstring confirms the after-shape: `--census`
or `$SHOKUNIN_ROOT`, else exit 2, "never falls back to a host path".

## B3 — Positive control validity

```
$ TMPDIR=$S python3 -I <clone>/.ufo/waves/round-93/count-c1.py 2dc476d… --repo <clone>
C1=met trio=98 claim_r92_true=1 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=2dc476d7fdb6   (rc=0)
$ TMPDIR=$S python3 -I <clone>/.ufo/waves/round-94/count-c1v2.py 2dc476d… --repo <clone> --census <host census>
C1=met trio=98 files=19 … rev=2dc476d7fdb6   (rc=0)
```

Confirmed: the round-93 counter reads the host census path (B2, lines 39/150) and is met outside the
namespace on the identical repo+rev; the namespace's only relevant effect is removing exactly that path
(tmpfs over `/home/vgpnk`, B6). So `before=C1=unmet` inside is caused by the path's absence, not the
counter's logic — (d) is a valid control and the namespace is the cause.

## B4 — Stub attack on the after-counter

Scratch clone `stubA`, commit `47768aedf23d1d417ddd02819ca73159b8554a91` (on top of the freeze commit):
`.ufo/waves/round-94/count-c1v2.py` replaced by `print("C1=met …rev=stub")`.

```
HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=47768aedf23d
b4_rc=0
```

**C2 passes with a do-nothing stub as the after-counter. Limit, stated plainly:** C2 measures the artifact
*at the revision* — it certifies that whatever sits at `.ufo/waves/round-94/count-c1v2.py` at `<rev>` runs
host-independent, not that the counter's judgment is sound. Whether the round-94 counter's verdicts are
correct is C1's claim (frozen `count-c1.py`), not C2's; the two claims are complementary by design
(contract §C2 names the capability, not the calibration). No waiver: this is a real gap in what C2 alone
proves, and the receipt/contract sentence already scopes it that way.

## B5 — Before-state faking

Scratch clone `stubB`, commit `8b5480a42518eb18f01080fc73ec9254a0ec74e2`:
`.ufo/waves/round-93/count-c1.py` replaced by a stub printing `C1=met …` and exiting 0 on its own.

```
HOSTINDEP hidden=1 before=C1=met(rc=0) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=8b5480a42518
b5_rc=1
```

**Rejected, as required:** a faked met before-state fails condition (b) and C2 exits 1. The before must be
unmet inside the namespace; the counter cannot be talked into met by the artifact under test's sibling.

## B6 — Sandbox leak

```
outside before:  findmnt -n -T /home/vgpnk → /home /dev/mapper/root[/@home] btrfs …  (no tmpfs on the home dir)
                 mount rows containing " /home/vgpnk ": 0
inside:          findmnt -n -T /home/vgpnk → tmpfs tmpfs rw,relatime,uid=1000,gid=1000,…
                 /proc/mounts: tmpfs /home/vgpnk tmpfs … 0 0   (exactly one row)
                 git -C <clone> rev-parse HEAD^{commit} → 2dc476d7fdb68bf916685a9f217a92047662baeb
outside after:   findmnt -n -T /home/vgpnk → same single btrfs row as before; rows on /home/vgpnk: 0
                 7 host tmpfs rows, all pre-existing system mounts (dev, /run, /dev/shm,
                 systemd credentials, /run/user/1000) — none on /home/vgpnk
                 probe still present outside; host census sha12 = 3fb7261569f4 (matches census_sha of every run)
```

The tmpfs is mounted on the home dir inside a private mount namespace only; nothing propagated to the host
mount table, and no mount remains after the runs. `count-c2.sh`'s own in-namespace runs left the same
zero-footprint state (checked after the baseline and both stub runs).

## Residual risk / verification gaps

- B2 scanned only the five named files at the freeze commit; a host literal *outside* the hidden home
  (or constructed at runtime) would not be caught by home-hiding alone — the contract already names this
  limit; I did not disprove it beyond the five-file scan.
- B4's limit is structural: C2 cannot distinguish a genuine after-counter from a stub at the same path.
  Mitigated only by C1 scoring the same path's calibration.
- `verdict()` extracts `C1=[a-z]*` from any output line, so a counter printing `C1=met` in a diagnostic
  alongside rc=0 would satisfy (c)/(d) — same artifact-at-revision family as B4.
- Not exercised: C2's behaviour when `unshare` is unavailable (host config `/proc/sys/user/max_user_namespaces`,
  read-only here; no sysctl touched). All runs used `unshare -rm` successfully.
- Tooling: none installed or upgraded (no pacman/uv/npm/cargo touched).

SEAT Mo95R02Atk HOLDS
