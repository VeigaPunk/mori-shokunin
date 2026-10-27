# Mo53ExecPinCheckNoHarm — operability no-harm: registry pin re-measure and unlanded check (round 53 w1)

Seat: executor, mori-shokunin round 53 wave w1. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`
(read-only except this report). Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecPinCheckNoHarm/`
(created, used, removed at the end; `TMPDIR` pointed at it for every run, `--scratch` passed explicitly).
No credential, session or private-URL material was read or written; no machine id is needed here.

Measured revisions:

| label | rev | what |
|---|---|---|
| R52 (round-52 entering tip) | `20edafa59b38dac1ca358893f0259b1f436372d3` | the round-52 baseline the seat spec compares against |
| DATA (round-53 data commit named in the seat spec) | `2a4213bf8da72f7cd78189baa5bb9be825dca1df` | the rev the seat spec's command names |
| TIP (L1 correction commit, landed during this wave) | `fd86307ad54c13edb8b6dd13182a2ad196f42fcd` | the lane tip when this seat finished |

## 1. Commands actually run (literal)

`--help` was read first for both instruments
(`mori-pin-check.py`: `--rev|--root`, `--repo`, `--skill`, `--min-tally-pins`, `--baseline-rev`,
`--timeout`, `--scratch`, `--selftest`; `mori-unlanded-check.py`: `--repo DIR --round N | --selftest`).
Every run had cwd inside my scratch, `TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecPinCheckNoHarm/tmp`,
and an explicit `--scratch`:

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
  --rev 2a4213bf8da72f7cd78189baa5bb9be825dca1df \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --scratch /fast/scratch/hyaku/mori-r53/Mo53ExecPinCheckNoHarm/pc \
  --baseline-rev 20edafa59b38dac1ca358893f0259b1f436372d3
EXIT=0   (86.19 s)

python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
  --rev 20edafa59b38dac1ca358893f0259b1f436372d3 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --scratch /fast/scratch/hyaku/mori-r53/Mo53ExecPinCheckNoHarm/pc52
EXIT=0   (86.95 s)

python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
  --rev fd86307ad54c13edb8b6dd13182a2ad196f42fcd \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --scratch /fast/scratch/hyaku/mori-r53/Mo53ExecPinCheckNoHarm/pc2 \
  --baseline-rev 2a4213bf8da72f7cd78189baa5bb9be825dca1df
EXIT=0   (98.13 s)

python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-unlanded-check.py \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin --round 53
EXIT=1   (also run for --round 52 and --round 51 as controls)
```

Independent re-measurements in scratch (read-only clones made with `git clone --shared --no-hardlinks`
from the lane; every fixture clone's `git rev-parse --show-toplevel` was asserted to equal the clone dir
before any commit, and the only commit used a throwaway `-c user.name=probe` identity inside the scratch
clone):

```
git archive 2a4213bf | tar -x -C <scratch>/tree53      # archive of the data commit
python3 tools/mori-pin-check.py --selftest              # from that archive -> 125 PASS lines, pass=125 fail=0
python3 .ufo/waves/round-53/count-c1.py --selftest      # -> C1_SELFTEST pass=37 fail=0
python3 .ufo/waves/round-53/count-c2.py --selftest      # -> C2_SELFTEST pass=30 fail=0
python3 -I -B tools/mori-commit-runway.py --selftest    # -> MATCHER: rejected 23/23 ; PASS 23/23
python3 .ufo/waves/round-52/count-c1.py <rev> --repo <clone> --fleet-repo /home/vgpnk/Projects/shokunin --scratch <scratch>
python3 .ufo/waves/round-52/count-c2.py <rev> --repo <clone>
python3 .ufo/waves/round-53/count-c2.py <rev> --repo <clone> --scratch <scratch>
```

Frozen-byte check: every path in `.ufo/waves/round-53/evidence/freeze-sha256.txt` was re-hashed from
`git show <rev>:<path>` at both DATA and TIP — `verified_ok 32 mismatch 0 absent 0` at each. No frozen
byte changed.

## 2. The seat question: is the new SKILL pin enumerated and green?

**Yes at the data commit the seat spec names, and yes at the lane tip — and no pin changed state
since round 52.**

At DATA (`2a4213bf`), the last line of the pin-check run:

```
PIN_CHECK=met tally_pins=37 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df baseline=yes env=0 stale=0
```

The new row's own pin line (SKILL.md line 1208 at that rev):

```
pin line=1208 kind=tally prefix=MORI_COMMIT_RUNWAY_SELFTEST state=match pinned=': PASS 23/23' observed=': PASS 23/23' rc=0 cmd='python3 -I -B tools/mori-commit-runway.py --selftest'
```

Enumerated (it is a parsed self-test row of the `## Round53` registry table, not a hidden or duplicate
row: `hidden=0 duplicate=0`), bound to the claimed instrument (`misattributed=0`), and green —
`state=match`, exit 0, observed tail exactly `': PASS 23/23'`. The tally count rose 36 → 37 against the
round-52 baseline: the row is present, bound and matching. The second sentence of the row
(`MATCHER: rejected 23/23 corrupted expectations`) is prose in the pinned-values cell, not a machine
check; the tool printed exactly that line in my archive run, so the prose is true today.

## 3. No pin changed state since round 52

Same instrument, same flags, only the measured revision differs:

```
R52 : PIN_CHECK=met tally_pins=36 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=20edafa59b38dac1ca358893f0259b1f436372d3 baseline=no env=0 stale=0
DATA: PIN_CHECK=met tally_pins=37 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df baseline=yes env=0 stale=0
```

Per-pin diff (`diff` of the two runs with the `line=` prefix normalised) — the only differences are the
two rows whose bound command carries the measured revision, plus the one added row:

```
< pin ... prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 20edafa59b38dac1ca358893f0259b1f436372d3 --selftest'
> pin ... prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df --selftest'
< pin ... prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 20edafa59b38dac1ca358893f0259b1f436372d3 --selftest'
> pin ... prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df --selftest'
```

`dropped=0` and `rebound=0` in the baseline-keyed run at DATA: no pin key disappeared and no bound argv
moved. SKILL.md bytes are identical at the round-52 landed tip `e7e056b8a17e54516a3c17798221c30e9902c250`
and at the round-52 entering tip `20edafa5` (same blob `494fc190933e1dff0e1e35f06b10f6f7dcd25818`), so the
baseline registry is the same registry the round-52 receipt measured.

**No pin changed state.** Every pre-existing pin is `state=match` at both revisions; the only change in the
registry is one added row.

## 4. Round-52 receipts, re-measured at the round-53 revs (no harm to the standing claim)

`mori-unlanded-check` and the round-52 counter are the two instruments the round-52 receipts name. Both
were re-run at the round-53 revs:

```
python3 .ufo/waves/round-52/count-c1.py 2a4213bf --repo <clone> --fleet-repo /home/vgpnk/Projects/shokunin --scratch <scratch>
C1=met items=43 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=28 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df

python3 .ufo/waves/round-52/count-c1.py fd86307a --repo <clone> --fleet-repo /home/vgpnk/Projects/shokunin --scratch <scratch>
C1=met items=43 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=28 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=fd86307ad54c13edb8b6dd13182a2ad196f42fcd

python3 .ufo/waves/round-52/count-c2.py fd86307a --repo <clone>
C2=met claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=28 dissent=0 rev=fd86307ad54c13edb8b6dd13182a2ad196f42fcd
```

Diffing the round-52 landed receipt `.ufo/waves/round-52/evidence/c1-at-landed.txt` against my re-run at
the r53 data rev: the 43 `item …` lines are byte-identical; only the trailing `rev=` differs. The two
pins the round-52 receipt lists still read:

```
item pin python3_tools/mori-pin-check.py_--selftest expect=(125/125) got=PIN_CHECK_SELFTEST_pass=125_fail=0 state=ok
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0 state=ok
```

`lane_writes=0` at both r53 revs: the round-53 data and correction commits wrote nothing into the lane
during a pinned command's run. The round-52 claim is unharmed by round 53's data.

The round-53 counters at the tip, for reference (not this seat's claim to judge):

```
python3 .ufo/waves/round-53/count-c1.py fd86307a --repo <clone>
C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=fd86307a failed=votes
python3 .ufo/waves/round-53/count-c2.py fd86307a --repo <clone> --scratch <scratch>
C2=met tool=present selftest=pass n=31 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=fd86307ad54c13edb8b6dd13182a2ad196f42fcd
```

`failed=votes` at the tip is the expected pre-vote state: the twelve RECHECK voters' reports are
untracked wave files and are not at any revision.

## 5. Unlanded check

```
python3 tools/mori-unlanded-check.py --repo <lane> --round 52
UNLANDED=clean round=52
EXIT=0

python3 tools/mori-unlanded-check.py --repo <lane> --round 53
UNLANDED=dirty round=53 paths=66
unlanded ?? .ufo/waves/round-53/evidence/selftests/mori-commit-runway.txt
unlanded ?? .ufo/waves/round-53/evidence/selftests/mori-pin-check.txt
unlanded ?? .ufo/waves/round-53/evidence/selftests/mori-unlanded-check.txt
unlanded ?? .ufo/waves/round-53/w1.ready
unlanded ?? .ufo/waves/round-53/w1.ready.dispatched
unlanded ?? .ufo/waves/round-53/w1/<seat reports …>
EXIT=1
```

Exit 1, as expected mid-wave: every listed path is `??` (untracked seat reports, wave markers and the
L1's own three round-53 selftest receipts). `git status --porcelain | grep -vc '^??'` = 0 at the tip — no
tracked file is modified, staged or deleted, so the committed bytes are what every measurement above
read. The path count grew during the wave (37 → 59 → 62 → 66) as seats wrote their reports. The
round-end receipt must read `UNLANDED=clean round=53` after the L1 lands the wave output.

Note the scope of the instrument: `in_scope()` covers `.ufo/waves/round-N/`, `corpus/`, `tools/` and
root-level `*.md`, so a root-level non-`.md` artifact is invisible to it (see Finding 4).

## 6. What changed during this wave (operability-relevant)

The L1 landed a correction commit `fd86307a` ("round-53: data corrections from w1 — tool bounded
reads/strict parsing/case-id guard (+3 cases, 5 hostile checks), two-sided band reading, CPU-hotplug
limit, S514 mm_init.c v7.3, dated host sentence") while this seat was measuring. It changed
`tools/mori-commit-runway.py`, `tools/fixtures/mori-commit-runway/cases.json` (23 → 26 cases),
`SKILL.md` (the r53 row's pinned tally `: PASS 23/23` → `: PASS 31/31`, and the case count 23 → 26),
`corpus/knowledge/commit-runway-read-r53.md` and `corpus/SOURCES.md` (+S514) and added
`corpus/evidence/sources-r53/mm_init.c.v7.3`.

Re-measured at TIP: the registry is still green, and the moved pin is green at its new value:

```
pin line=1209 kind=tally prefix=MORI_COMMIT_RUNWAY_SELFTEST state=match pinned=': PASS 31/31' observed=': PASS 31/31' rc=0 cmd='python3 -I -B tools/mori-commit-runway.py --selftest'
PIN_CHECK=met tally_pins=37 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=fd86307ad54c13edb8b6dd13182a2ad196f42fcd baseline=yes env=0 stale=0
```

The per-pin diff R52 → TIP is the same shape as R52 → DATA: only the two revision-carrying commands
move, plus the one added row, and at TIP that row's pinned text is `': PASS 31/31'` matching the tool's
output at that rev. So the pin *value* moved inside round 53 (23/23 → 31/31) but no pin ever changed
*state*.

## 7. Side effects of my runs

- Lane: the only tracked file I wrote is this report. One gitignored byproduct: importing
  `tools/mori-unlanded-check.py` with `importlib` (to enumerate in-scope paths) wrote
  `tools/__pycache__/mori-unlanded-check.cpython-314.pyc` (18 KB, `.gitignore:3`) into the lane at
  23:18:47 — bytecode cache only, no tracked byte affected; left in place rather than deleted.
- `mori-pin-check.py` runs its pinned instruments inside its own exported tree under `--scratch`
  (my scratch), with `TMPDIR` inside that tree; the lane's own `.scratch/` (10 entries, all dated
  Oct 24–26 10:53, i.e. pre-existing) was not touched by my runs.
- The tool's own write scope holds: `python3 -I -B tools/mori-commit-runway.py --selftest` run with
  `TMPDIR` in my scratch left nothing behind in `TMPDIR` or in the cwd (its temp dir is `mkdtemp` +
  `rmtree`).
- Host: reads only. `/proc/meminfo`, `/proc/sys/vm/*`, `/sys/devices/system/cpu/present` via the tool's
  live leg; no sysctl/cgroup/swap write, no OOM trigger, no large allocation, no kernel-log message
  grep, no `systemctl`/`journalctl` maintenance. Disk guard before the heavy runs:
  `/fast/scratch/hyaku` 25 %, 608.4 GB free — no ENOSPC. No pacman, no tool installs.
- Scratch removed at the end (two `--shared` clones, one archive tree, ~1 GB total, all mine).

## 8. Named limits of this seat's evidence

- Pins measured, not audited: a `state=match` line proves the pinned instrument prints today's pinned
  text at that revision; it does not prove the instrument's arms are good (the contract's named limit for
  C1).
- The `--rev` mode measures committed bytes; untracked wave output never entered any measurement.
- Three revisions were in play while I measured (R52, DATA, TIP). The DATA readings are what the seat
  spec asked for; the TIP readings are the current state; the intermediate working-tree state was moving
  under me (see Finding 2) and is reported as a snapshot with timestamps, not as a verdict.
- Whether the L1's correction commit `fd86307a` is the final landed tip for round 53 is UNVERIFIED from
  here; this seat reads the lane, it does not decide the tip.
- The three `.ufo/waves/round-53/evidence/selftests/*.txt` receipts I read are untracked working-tree
  files (Finding 1); their content is reproduced verbatim above so a reader can check my comparison.

## Findings

- **MED — the round-53 selftest receipts are unlanded and now stale.**
  `.ufo/waves/round-53/evidence/selftests/{mori-pin-check.txt,mori-unlanded-check.txt,mori-commit-runway.txt}`
  exist only as untracked working-tree files (`git ls-tree -r fd86307a .ufo/waves/round-53/evidence/selftests/`
  → 0 entries), whereas the round-52 equivalents are committed
  (`git ls-tree -r 20edafa5 .ufo/waves/round-52/evidence/selftests/` → 2 files). They are also stale:
  `mori-commit-runway.txt` records `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23` while the landed tip
  `fd86307a` prints `PASS 31/31`. Consequence: the wave-end receipt cannot cite these files as-is —
  they must be re-taken at the landed tip and committed. (Concerns the receipt files, not the claim.)
- **MED — the C2 counter's registry arm is textual, so a stale SKILL tally would not have been caught
  by it.** `count-c2.py`'s registry check is `if line.lstrip().startswith("|") and TOOL in line and
  "--selftest" in line: registry = "ok"` — it never compares the row's pinned tally with the tool's
  output. Measured on a scratch snapshot of the mid-wave working tree (SKILL.md row pinned `: PASS 31/31`
  while the tool printed `: PASS 28/28`): `count-c2.py` still read `C2=met … n=28 … registry=ok`, while
  `mori-pin-check.py` on the same bytes read
  `PIN_CHECK=unmet … mismatches=1 stale=1` with
  `pin line=1208 kind=tally prefix=MORI_COMMIT_RUNWAY_SELFTEST state=mismatch pinned=': PASS 31/31' observed=': PASS 28/28' class=stale`.
  `mori-pin-check.py` is the only instrument in the lane that ties a SKILL pinned tally to the tool's
  actual output. Named limit / routed item for round 54 (the counters are frozen for this round; no
  change proposed here).
- **LOW — round-53 evidence receipts are excerpts, where round-52's were full transcripts.**
  `.ufo/waves/round-53/evidence/selftests/mori-pin-check.txt` carries 4 `PASS` lines before the tally
  line; the round-52 file of the same name carries all 125. Same for `mori-unlanded-check.txt` (4 vs 17
  `PASS` lines). The recorded tallies are truthful and I reproduced them independently from the data-rev
  archive (`PIN_CHECK_SELFTEST pass=125 fail=0` from 125 `PASS` lines; `UNLANDED_SELFTEST pass=17
  fail=0`), but a reader cannot audit the 121 omitted arms from the receipt.
- **LOW — a stray untracked tarball sits in the lane root and the unlanded check cannot see it.**
  `/home/vgpnk/Projects/shokunin/mori-shokunin/r53-data.tar` (51,200 bytes, mtime 23:19, containing the
  data-commit `tools/mori-commit-runway.py` and `cases.json`) is untracked and outside
  `mori-unlanded-check.py`'s scope (`in_scope()` matches `corpus/`, `tools/`, `.ufo/waves/round-N/` and
  root-level `*.md`), so it never appears in the `UNLANDED=` listing even though `git status` shows it
  as `?? r53-data.tar`. It is also scratch material outside the wave's scratch root. Not mine (my
  archives went to `/fast/scratch/…`); attribution UNVERIFIED.
- **LOW — the r53 registry row pins no digest of the tool or its fixtures.**
  `digest_pins=8` is unchanged from round 52, and the new row's pinned-values cell names
  `tools/fixtures/mori-commit-runway/cases.json` without a sha256, unlike older rows that pin their
  instrument's digest. A byte change in the tool that preserves the printed tally is therefore invisible
  to `mori-pin-check.py`; the tally pin covers behaviour, not bytes.
- **INFO — the r53 pin *value* moved inside the round.** The registry row's pinned tally went from
  `: PASS 23/23` (DATA) to `: PASS 31/31` (TIP) together with the tool, and the row's case count from 23
  to 26; both are consistent with the tool at their respective revisions, and the pin was `state=match`
  at each. Nothing to fix; recorded because any wave seat that cites "23/23" must cite the data commit
  explicitly, since the tip no longer prints it.
