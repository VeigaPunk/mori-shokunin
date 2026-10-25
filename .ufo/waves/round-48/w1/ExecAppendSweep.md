# ExecAppendSweep — w1 report (round 48)

Seat: ExecAppendSweep (leaf). Lane: mori-shokunin. Task: sweep the entering tip
`e5dbac05459887d9597ea5d1da0d8e3d024e0d17` for unlanded round-47 leftovers and drift in the
lane's own gate rows.

Commands run from `/home/vgpnk/Projects/shokunin/mori-shokunin` with
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecAppendSweep` (created).
Read-only git only. No tool installs were needed (python3 available); nothing installed.

## 1. Worktree sweep

`git status --porcelain` (lane repo):

```
?? .scratch/r48-ExecAppendSweep/
?? .scratch/r48-l1/
?? .ufo/waves/round-48/w1-dispatch.json
?? .ufo/waves/round-48/w1-spec.json
?? .ufo/waves/round-48/w1-validate.err
?? .ufo/waves/round-48/w1.ready
?? .ufo/waves/round-48/w1/
```

No modified tracked files (only `??` entries; tracked tree clean at HEAD).

`git ls-files --others --exclude-standard` (excluding `.scratch`):

```
.ufo/waves/round-48/w1-dispatch.json
.ufo/waves/round-48/w1-spec.json
.ufo/waves/round-48/w1-validate.err
.ufo/waves/round-48/w1.ready
.ufo/waves/round-48/w1/swarm-registry.json
```

Every untracked item outside `.scratch` sits under `.ufo/waves/round-48/` (wave-harness state).
`corpus/evidence/sources-r48/` contributes no untracked entries: its four committed copies are
already tracked at the freeze commit (see below). `HEAD` = freeze commit
`4387cf94b69ddce455051a1ff38e93795c2e6cde` whose parent is the entering tip `e5dbac05`
(`git rev-parse 4387cf94^` → `e5dbac05459887d9597ea5d1da0d8e3d024e0d17`). No unlanded
round-47 leftovers on disk.

## 2. Late round-47 reports tracked at e5dbac05

`git ls-tree -r e5dbac05459887d9597ea5d1da0d8e3d024e0d17 --name-only` → each present:

- `.ufo/waves/round-47/w2/CritV2Junk.md` ✓
- `.ufo/waves/round-47/w2/MutV2Rebound.md` ✓
- `.ufo/waves/round-47/w2/ScoutMisroot.md` ✓
- `.ufo/waves/round-47/w2-results.json` ✓

## 3. Append-only gate at e5dbac05

Command:

```
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecAppendSweep \
python3 tools/mori-sources-appendonly.py \
  e5dbac05459887d9597ea5d1da0d8e3d024e0d17 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --round-base 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
```

Exit code: **0**.

Verdict lines:

```
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226,S229,S235] round_changed=[]
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226,S229,S235] stale_supersede=[]
```

Round-window signals are clean: `round_changed=[]` and `deleted=[]`. The 18 `ids` /
36 `superseded` are history-wide pre-round findings: the output is byte-identical (same ids,
same superseded list, same exit 0, same empty `round_changed`) to round-47's receipt
`.ufo/waves/round-47/w2/ExecAppendOnly.md`. No gate drift.

## 4. Census

Command:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Exit code: **0**.

Last line:

```
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

Full output is byte-identical (`cmp -s` → `IDENTICAL_TO_CENSUS_START`) to the frozen
round-start receipt `.ufo/waves/round-48/evidence/census-start.txt` (20 W04 warnings + one ok).
No census drift.

## Evidence / risks

- Evidence: exact command + output + exit code above; read-only git except scratch writes;
  TMPDIR confined to scratch; census output captured to
  `.scratch/r48-ExecAppendSweep/census.out` (cmp-verified against the frozen receipt).
- Risk: none beyond the recorded history-wide append-only findings (pre-round, unchanged from
  round-47).
- Blockers: none. No tools installed (python3 available; no pacman/uv/npm action needed).
