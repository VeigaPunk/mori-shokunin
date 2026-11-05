# Mo94E02Relo — relocation + HOME-isolation check of round-94 counters (w1)

2026-11-05. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`, freeze `6b65e7c11f318481d5efa0429cdabb50743a2cc2`.
Scratch `S=/fast/scratch/hyaku/mori-r94/Mo94E02Relo` (created, trap `rm -rf -- "$S"` EXIT set; deleted before yield).
No tool installs. Nothing NOT RUN. Lane untouched (read-only git inside the shared clone only).

## Setup

```
mkdir -p "$S/fleet/scripts" && cp /home/vgpnk/Projects/shokunin/scripts/sources-census.sh "$S/fleet/scripts/sources-census.sh"
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin "$S/clone"
git -C "$S/clone" rev-parse --show-toplevel
git -C "$S/clone" checkout -q --detach 6b65e7c11f318481d5efa0429cdabb50743a2cc2
```

Observed: clone ok; `rev-parse --show-toplevel` printed `$S/clone` (asserted before the detach checkout);
clone HEAD after checkout: `6b65e7c1`.

## Run 1 — count-c1v2 relocated, isolated HOME

```
cd "$S" && env -i PATH="$PATH" HOME=/nonexistent TMPDIR="$S" SHOKUNIN_ROOT="$S/fleet" \
  python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-94/count-c1v2.py \
  6b65e7c11f318481d5efa0429cdabb50743a2cc2 --repo "$S/clone"
```

```
C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=6b65e7c11f31
rc=0
```

The `census=ok` verdict came from the relocated copy: `census_path` resolves
`$SHOKUNIN_ROOT/scripts/sources-census.sh` (count-c1v2.py:69-74) and invoked it as
`bash <census> validate --file <extracted tree>/corpus/SOURCES.md` under `HOME=/nonexistent`.

## Run 2 — count-c1v2 with no SHOKUNIN_ROOT and no --census (fail-closed)

```
cd "$S" && env -i PATH="$PATH" HOME=/nonexistent TMPDIR="$S" \
  python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-94/count-c1v2.py \
  6b65e7c11f318481d5efa0429cdabb50743a2cc2 --repo "$S/clone"
```

```
C1_SETUP census path unset: give --census or set SHOKUNIN_ROOT
rc=2
```

Matches the contract's `env_unset=rc2` expectation: no silent fallback, fails closed as C1_SETUP.

## Run 3 — count-c2v2 relocated, isolated HOME

```
cd "$S" && env -i PATH="$PATH" HOME=/nonexistent TMPDIR="$S" SHOKUNIN_ROOT="$S/fleet" \
  python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-94/count-c2v2.py \
  6b65e7c11f318481d5efa0429cdabb50743a2cc2 --repo "$S/clone" --root "$S/fleet"
```

```
C2=met literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2 rev=6b65e7c11f31
rc=0
```

`env_i=met` here is a second, independent HOME-isolation observation: count-c2v2 re-ran the
*extracted* count-c1v2.py with `HOME=/nonexistent` + `SHOKUNIN_ROOT=$S/fleet` and got `C1=met`
rc 0; its unset re-run returned rc 2 (`env_unset=rc2`). At the freeze rev the C2 predicate line
reads exactly as contract P-C2 specifies (`literal_r94=0 files_r94=3 frozen_r93=unchanged …`).

## Step 5 — host-path greps on the relocated census copy

```
grep -n '/home/' "$S/fleet/scripts/sources-census.sh"   # no output
```
rc=1 — zero `/home/` matches in the copied script.

```
grep -n 'HOME\|~' "$S/fleet/scripts/sources-census.sh"
```
rc=0 — 18 matches, all awk/bash regex match operators (`~`, `=~`, `!~`, e.g. line 52
`s !~ /^[0-9]{4}-...$/`), no `HOME` variable use, no `~user` path. Same result holds for the
counters themselves: Run 1/3 executed with a `/home/`-free environment and passed, and
count-c2v2's own literal scan over `.ufo/waves/round-94/*.py` reported `literal_r94=0`.

## Dependencies the relocated run hides or needs

- Needs exactly `$SHOKUNIN_ROOT/scripts/sources-census.sh` to exist (created in setup). If the
  env var is set but the file is missing, the census subprocess fails (`census=rc127` → C1 unmet):
  fails closed, no hidden host fallback.
- Hidden by relocation: count-c1v2 calls census only as `validate --file <tree>/corpus/SOURCES.md`,
  so census's own default `ROOT=${SHOKUNIN_ROOT:-realpath(dirname($0))/..}` is never exercised and
  no `corpus/`, `shokunin.conf` or lane directories are needed beside the copied script. On the real
  fleet the counter needs only the fleet root handed over via `SHOKUNIN_ROOT`.
- Runtime deps observed working under `env -i`: `bash`, GNU coreutils (`date -u` for TODAY since
  the counter passes no `--today`; affects only validate's E08 future-opened check), `gawk`
  (iso_epoch), `git`, `python3` (isolated `-I`), `tar` extraction via git archive.
- HOME: unused everywhere — both counters and the census script completed with `HOME=/nonexistent`;
  the counters' git calls never read `~/.gitconfig` (read-only: log/archive/diff/rev-parse only).

## Mapping to the wave claims (freeze rev, this seat's scope)

- C2 operability: `env_i=met env_unset=rc2` observed directly (Runs 1–3); the counter family runs
  relocated with no home literal and fails closed without a census source.
- C1 live branch at freeze: `C1=met … adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok`
  (Run 1) — consistent with contract P3/P-C1's live-data expectation; the embedded-fixture battery
  itself is `controls-r94.py`'s job, not run here (out of seat scope).
