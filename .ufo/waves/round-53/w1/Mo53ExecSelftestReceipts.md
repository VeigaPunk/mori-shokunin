# Mo53ExecSelftestReceipts — round 53 SHONEN tally-pin receipts

Seat: executor (receipts only; the L1 commits the content). Lane: `mori-shokunin`
(fleet + host observability). Wave `w1`, round 53.

Scope of this seat: re-run the three self-test instruments at the round-53 data commit
`2a4213bf8da72f7cd78189baa5bb9be825dca1df` **and** at the tip the L1 landed mid-seat
(`fd86307ad54c13edb8b6dd13182a2ad196f42fcd`, "round-53: data corrections from w1"), from
`git archive` extractions into this seat's scratch, and hand the L1 the literal receipt bodies
(as fenced blocks below) so `SHONEN.md`'s tally-pin box and the round-53 evidence directory
carry receipts whose numbers match the lane's own `SKILL.md` registry row.

Nothing in the lane was written by this seat except this report file.

## 1. Environment and provenance

| item | value |
|---|---|
| contract data commit | `2a4213bf8da72f7cd78189baa5bb9be825dca1df` ("round-53: data — v7.3 recheck ledger (C1), mori-commit-runway tool + fixtures + SKILL Round53 registry row and band entry (C2), rows S502-S513, S499 used-by fixtures") |
| tip landed mid-seat | `fd86307ad54c13edb8b6dd13182a2ad196f42fcd` ("round-53: data corrections from w1 — tool bounded reads/strict parsing/case-id guard (+3 cases, 5 hostile checks), two-sided band reading, CPU-hotplug limit, S514 mm_init.c v7.3, dated host sentence"), 2026-10-26 23:28:22 -0300 |
| entering tip (contract) | `20edafa59b38dac1ca358893f0259b1f436372d3` |
| extraction | `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive <rev> | tar -x -C <scratch>/arc2` (data commit) and `…/arc3` (tip) |
| archive stream sha256 | data commit `4ca2d208cdf8a3618f05af8258ea59bb49c469a4d1e06a8dc656c11fd9806caf`; tip `fdbc0a429c6e2ae097fa6dff58835774e6340a0d164a2e2293dc881ae5d3ad63` |
| scratch root | `/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/` (removed at the end of this seat; §8) |
| TMPDIR per command | `<scratch>/tmp`, `<scratch>/tmp2`, `<scratch>/tmp3` (plus `<scratch>/tmp4`, `<scratch>/tmp5`, `<scratch>/final-tmp`, `<scratch>/c2new` for the reconciler and counter runs) |
| host | linux 7.2.11-arch1-1, x86_64 |
| disk guard before the runs | `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → `/tmp 4% 123.6G`, `/var/tmp 34% 593.0G`, `/fast/scratch/hyaku 25% 608.2G` free; exit 0. No ENOSPC risk; no sweep needed. |

Tool bytes at the two revisions (sha256 of `git show <rev>:<path>`):

```
                                     data commit 2a4213bf                                            tip fd86307a
tools/mori-pin-check.py               32685b9306db061d2c2df21e976823d84a4017cc3524194f4ed76327443081f0  32685b9306db061d2c2df21e976823d84a4017cc3524194f4ed76327443081f0
tools/mori-unlanded-check.py          612d50c1590d5a30a1beae19a8e43da3acba18ddd30d47a6b51c2cdeada76109  612d50c1590d5a30a1beae19a8e43da3acba18ddd30d47a6b51c2cdeada76109
tools/mori-commit-runway.py           80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156  b3c123400f41a8e8d62e678d81175956c68a9735643a8a3cd09975666be1ffe4
tools/fixtures/…/cases.json           cea8045192babe3017a2682c17a1647e73c597eaf0330a27643858577cc43b63  3a1aef20cc03fc4e323ad8b5400feeeda7cff1373ccd6f77498a8ebf5c450623
SKILL.md                              aa54d36a99214326e5395bddd59c702e220d3fb362a27d0b1f50921f39db2303  241076efd6147de2b84ef5d25e0e327aa889475a362e28f37d82d127a016fdf8
```

`mori-pin-check.py` and `mori-unlanded-check.py` are byte-unchanged between the two revisions;
the runway tool, its fixtures and `SKILL.md` changed at the corrections commit.

## 2. The three commands, verbatim, with full last lines and exit codes

Run with `cwd` = the extracted archive, `TMPDIR` inside this seat's scratch, no `PYTHONDONTWRITEBYTECODE`
(the instruments are stdlib-only and safe under `-I -B`).

### 2.1 At the contract data commit `2a4213bf`

```
$ cd /fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/arc2 && TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/tmp python3 tools/mori-pin-check.py --selftest
PASS v5_rev_export_outside_repo  rc=0 left=0
PASS v51_scratch_inside_repo_refused  rc=2
PASS v51_default_scratch_tmpdir_and_master_is_rev  rc=0 left=0
PASS cli_met_rc0  rc=0
PASS cli_bad_rev_rc2  rc=2
PIN_CHECK_SELFTEST pass=125 fail=0
exit=0
```

Full stdout: 126 lines — 125 `PASS` lines plus the summary `PIN_CHECK_SELFTEST pass=125 fail=0`.
Zero `FAIL` lines. Exit code 0.

```
$ cd /fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/arc2 && TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/tmp2 python3 tools/mori-unlanded-check.py --selftest
PASS missing_directory_is_setup_error  setup
PASS cli_dirty_rc1  rc=1
PASS cli_setup_rc2  rc=2
PASS cli_usage_rc2  rc=2
UNLANDED_SELFTEST pass=17 fail=0
exit=0
```

Full stdout: 18 lines — 17 `PASS` lines plus the summary `UNLANDED_SELFTEST pass=17 fail=0`.
Zero `FAIL` lines. Exit code 0.

```
$ cd /fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/arc2 && TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/tmp3 python3 -I -B tools/mori-commit-runway.py --selftest
MATCHER: rejected 23/23 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23
exit=0
```

Full stdout: 2 lines. Exit code 0.

### 2.2 At the tip the L1 landed mid-seat, `fd86307a`

```
$ cd /fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/arc3 && TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/tmp python3 tools/mori-pin-check.py --selftest
PASS v5_rev_export_outside_repo  rc=0 left=0
PASS v51_scratch_inside_repo_refused  rc=2
PASS v51_default_scratch_tmpdir_and_master_is_rev  rc=0 left=0
PASS cli_met_rc0  rc=0
PASS cli_bad_rev_rc2  rc=2
PIN_CHECK_SELFTEST pass=125 fail=0
exit=0
exit=0
```

(the tool's own summary line is `PIN_CHECK_SELFTEST pass=125 fail=0`; the tool exits 0)

```
$ cd /fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/arc3 && TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/tmp2 python3 tools/mori-unlanded-check.py --selftest
PASS missing_directory_is_setup_error  setup
PASS cli_dirty_rc1  rc=1
PASS cli_setup_rc2  rc=2
PASS cli_usage_rc2  rc=2
UNLANDED_SELFTEST pass=17 fail=0
exit=0
```

```
$ cd /fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/arc3 && TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/tmp3 python3 -I -B tools/mori-commit-runway.py --selftest
MATCHER: rejected 26/26 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31
exit=0
```

Measured exit codes at the tip: `0`, `0`, `0`. The runway line matches the frozen counter's own
pattern `.ufo/waves/round-53/count-c2.py` `SELFTEST_RE = ^MORI_COMMIT_RUNWAY_SELFTEST: PASS (\d+)/(\d+)$`
with 31 ≥ `MIN_SELFTEST = 12`.

## 3. Comparison with the round-52 receipts

Round-52 receipt dir: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/evidence/selftests/`
(`mori-pin-check.txt` 28.7 KB / 128 lines, `mori-unlanded-check.txt` 1.4 KB / 20 lines). Round 52
shipped two instruments; round 53 adds a third (`mori-commit-runway.py`), so the round-52 set has
no counterpart for the runway receipt.

Body-for-body comparison (round-52 receipt body with its `$ …` header line and trailing `rc=0`
stripped, against this seat's full stdout at the data commit):

| instrument | round-52 body sha256 | round-53 body sha256 | verdict |
|---|---|---|---|
| `mori-pin-check.py` | `27d22872d445015c46d2af2e703e986741a05db3a8c580f9dea8df5a50717f85` | `27d22872d445015c46d2af2e703e986741a05db3a8c580f9dea8df5a50717f85` | **byte-identical** |
| `mori-unlanded-check.py` | `22604de3387ebb25eb92e151c41a44a2b2ab9ab77289fa4d1f71e5c61445fe1b` | `22604de3387ebb25eb92e151c41a44a2b2ab9ab77289fa4d1f71e5c61445fe1b` | **byte-identical** |

Both tallies are unchanged across rounds and across the mid-seat corrections commit:
`PIN_CHECK_SELFTEST pass=125 fail=0` and `UNLANDED_SELFTEST pass=17 fail=0`. Round 52's
`SHONEN.md` operability box cites exactly those two numbers (`(125/125)`, `(17/17)`), so
`SHONEN.md` needs no change for these two instruments — only the receipt paths move.

The runway tool's tally **did** move: `23/23` at the contract data commit → `31/31` at the
corrections commit (the L1 added 3 fixture cases and 5 built-in hostile-input checks, and
`SKILL.md:1209` was re-pinned to `: PASS 31/31`). The receipts must therefore be cut at the
revision the lane actually lands.

Determinism: every instrument was run at least twice per revision (archive + `git clone --shared`
checkout, and a second archive extraction). All outputs are byte-identical across runs:

```
27d22872d445015c46d2af2e703e986741a05db3a8c580f9dea8df5a50717f85  pin-check stdout   (data commit, all runs)
22604de3387ebb25eb92e151c41a44a2b2ab9ab77289fa4d1f71e5c61445fe1b  unlanded stdout    (data commit and tip, all runs)
c4decd497a0f581a36c0ec0a9b02f7f9f1653cc330c905d42ee3e2302f6a18de  runway stdout     (data commit, all runs)
d510cbbacfefb018adc33e3c7a5787f0d54645bb05bd02e4dd94bdc66694ebe3  runway stdout     (tip fd86307a, all runs)
```

## 4. The receipt bodies for the L1 to commit

The L1 already wrote three files under `.ufo/waves/round-53/evidence/selftests/` (untracked at
the time of this seat) in the round-52 shape. Two of them still match the tip; the third does
not — see §7, finding 1.

Suggested file contents (paths relative to the lane root; the L1 owns the final location —
`.ufo/waves/round-53/evidence/selftests/` is the round-52 convention and what the L1 already used).
These are cut at the tip `fd86307a`, so the runway tally in the receipt equals the tally the
tip's own `SKILL.md` registry row pins.

`.ufo/waves/round-53/evidence/selftests/mori-pin-check.txt`

```
# run from a git archive of fd86307ad54c13edb8b6dd13182a2ad196f42fcd (lane tip at the time of this receipt), TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/tmp, 2026-10-26T23:41:00-03:00
$ python3 tools/mori-pin-check.py --selftest
PASS v51_scratch_inside_repo_refused  rc=2
PASS v51_default_scratch_tmpdir_and_master_is_rev  rc=0 left=0
PASS cli_met_rc0  rc=0
PASS cli_bad_rev_rc2  rc=2
PIN_CHECK_SELFTEST pass=125 fail=0
exit=0
```

`.ufo/waves/round-53/evidence/selftests/mori-unlanded-check.txt`

```
# run from a git archive of fd86307ad54c13edb8b6dd13182a2ad196f42fcd (lane tip at the time of this receipt), TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/tmp2, 2026-10-26T23:41:00-03:00
$ python3 tools/mori-unlanded-check.py --selftest
PASS missing_directory_is_setup_error  setup
PASS cli_dirty_rc1  rc=1
PASS cli_setup_rc2  rc=2
PASS cli_usage_rc2  rc=2
UNLANDED_SELFTEST pass=17 fail=0
exit=0
```

`.ufo/waves/round-53/evidence/selftests/mori-commit-runway.txt`

```
# run from a git archive of fd86307ad54c13edb8b6dd13182a2ad196f42fcd (lane tip at the time of this receipt), TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/tmp3, 2026-10-26T23:41:00-03:00
$ python3 -I -B tools/mori-commit-runway.py --selftest
MATCHER: rejected 26/26 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31
exit=0
```

sha256 of the three files as written by this seat:

```
03512bc336650534bb89b8a74d85c120ad23a54529bc21e1a919f29107da1802  mori-pin-check.txt
a2275de1ef13a580385fe2bfa1a1afe1e28b7e8537243d713d5a127643db58e6  mori-unlanded-check.txt
6296d9e41371b63d9177c8f21cc68826b1130c9e46acfb7e59509a25822681f6  mori-commit-runway.txt
```

If the L1 prefers to keep the receipts cut at the contract data commit `2a4213bf` (the
revision the contract names), the runway body is instead
`MATCHER: rejected 23/23 corrupted expectations` / `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23` —
but then the receipt no longer matches the tip's own `SKILL.md:1209` pin (`: PASS 31/31`),
which is why this seat recommends cutting at the tip.

### 4.1 Suggested `SHONEN.md` operability-box line (draft — the L1 edits `SHONEN.md`, not this seat)

Current text at `SHONEN.md:7`:

```
- [~] Instructions executable by an agent without oral context — `python3 tools/mori-pin-check.py --selftest` (125/125); `python3 tools/mori-unlanded-check.py --selftest` (17/17); round-52 receipts `.ufo/waves/round-52/evidence/selftests/mori-pin-check.txt`, `.ufo/waves/round-52/evidence/selftests/mori-unlanded-check.txt`
```

Draft for round 53 (two pins unchanged; receipts re-pointed at the round-53 dir; the new
instrument named **without** a tally token, for the reason measured in §5):

```
- [~] Instructions executable by an agent without oral context — `python3 tools/mori-pin-check.py --selftest` (125/125); `python3 tools/mori-unlanded-check.py --selftest` (17/17); round-53 receipts `.ufo/waves/round-53/evidence/selftests/mori-pin-check.txt`, `.ufo/waves/round-53/evidence/selftests/mori-unlanded-check.txt`, `.ufo/waves/round-53/evidence/selftests/mori-commit-runway.txt`
```

## 5. Why the new tool is named in `SHONEN.md` without a tally token (measured, not assumed)

The lane's frozen `SHONEN.md` tally-pin grammar lives in the round-50/52 calibration counter
(`.ufo/waves/round-52/count-c1.py`), whose regexes are:

```
TALLY = \b([A-Z][A-Z0-9_]*SELFTEST) pass=(\d+) fail=(\d+)\b
ANY   = (?:\b([A-Z][A-Z0-9_]*SELFTEST) )?\bpass=(\d+) fail=(\d+)\b
PIN   = `([^`\n]*--selftest[^`\n]*)`(?:\s*\((\d+)/(\d+)\)|\s*(?:→|->)\s*`([A-Z][A-Z0-9_]*SELFTEST) pass=(\d+) fail=(\d+)`)
HIDDEN = \(\s*\d+\s*/\s*\d+\s*\)|\bpass=\d+|SELFTEST
```

Measured against the tool's real output (`MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31`):

* `TALLY.findall("MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31")` → `[]`; `ANY_TALLY.findall(...)` → `[]`.
  The tool prints the `PASS n/n` form, which neither regex reads. The same call on the other two
  instruments returns `('PIN_CHECK_SELFTEST','125','0')` and `('UNLANDED_SELFTEST','17','0')`.
* Therefore a `SHONEN.md` pin of the fraction form
  `` `python3 tools/mori-commit-runway.py --selftest` (31/31) `` is *parsed* as a pin but re-runs
  to `no_tally_or_timeout` → `error`. Driving the frozen counter's own `check_pins()` over that
  candidate line against the real archive tree:

  ```
  ('pin', 'python3 tools/mori-pin-check.py --selftest',        '(125/125)', 'PIN_CHECK_SELFTEST pass=125 fail=0', 'ok')
  ('pin', 'python3 tools/mori-unlanded-check.py --selftest',   '(17/17)',   'UNLANDED_SELFTEST pass=17 fail=0',    'ok')
  ('pin', 'python3 tools/mori-commit-runway.py --selftest',    '(31/31)',   'no_tally_or_timeout',                   'error')
  ```

  The `-I -B` form `` `python3 -I -B tools/mori-commit-runway.py --selftest` (31/31) `` is worse:
  `bound_path()` returns `None` (it requires exactly `python3 <path> --selftest`), so it reads
  `unbound_or_not_regular` → `mismatch`.
* A prose mention of the tool's tally token outside a pin is counted by the counter's `HIDDEN`
  scan (`SELFTEST` matches) and becomes `hidden=1` → `failed=hidden`. Measured:
  `- [~] x — the runway tool prints `MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31`` → `pins=0 hidden=1`.

Consequence for the L1: **do not** write the runway tool's tally token or an `(n/n)` fraction
into `SHONEN.md`. Name the instrument and point at the receipt path (as drafted in §4.1); the
tally itself belongs in `SKILL.md`'s registry row, where it already sits and where the
round-47+ `mori-pin-check.py` registry grammar reads the `PASS n/n` form correctly (§6). This is
a named limit of the frozen calibration counter's `SHONEN.md` grammar (it predates the `PASS n/n`
self-test convention) — routed to round 54, not a change to any frozen counter.

## 6. Independent confirmation that the registry row pins true

Beyond the three receipts, this seat ran the lane's own registry reconciler over both revisions
to confirm the new `## Round53` registry row is live and matches:

At the contract data commit `2a4213bf`:

```
$ cd <scratch>/arc2 && python3 tools/mori-pin-check.py --rev 2a4213bf8da72f7cd78189baa5bb9be825dca1df --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <scratch>/tmp4
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=125 fail=0' observed='pass=125 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
pin line=973 kind=tally prefix=UNLANDED_SELFTEST state=match pinned='pass=17 fail=0' observed='pass=17 fail=0' rc=0 cmd='python3 tools/mori-unlanded-check.py --selftest'
pin line=1208 kind=tally prefix=MORI_COMMIT_RUNWAY_SELFTEST state=match pinned=': PASS 23/23' observed=': PASS 23/23' rc=0 cmd='python3 -I -B tools/mori-commit-runway.py --selftest'
PIN_CHECK=met tally_pins=37 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df baseline=no env=0 stale=0
exit=0
```

At the tip `fd86307a`:

```
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=125 fail=0' observed='pass=125 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
pin line=973 kind=tally prefix=UNLANDED_SELFTEST state=match pinned='pass=17 fail=0' observed='pass=17 fail=0' rc=0 cmd='python3 tools/mori-unlanded-check.py --selftest'
pin line=1209 kind=tally prefix=MORI_COMMIT_RUNWAY_SELFTEST state=match pinned=': PASS 31/31' observed=': PASS 31/31' rc=0 cmd='python3 -I -B tools/mori-commit-runway.py --selftest'
PIN_CHECK=met tally_pins=37 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=fd86307ad54c13edb8b6dd13182a2ad196f42fcd baseline=no env=0 stale=0
exit=0
```

Both `PIN_CHECK=met`, exit 0, 37 tally pins, 0 mismatches. The `--rev` mode reads the registry
from the revision and measures the tools there, so these are landed-revision readings, not
working-tree readings.

For completeness, the two frozen round-53 counters at the tip `fd86307a` (read-only, run by this
seat only to confirm the receipts describe a live tree):

```
$ python3 .ufo/waves/round-53/count-c2.py fd86307ad54c13edb8b6dd13182a2ad196f42fcd --scratch <scratch>/c2new
C2=met tool=present selftest=pass n=31 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=fd86307ad54c13edb8b6dd13182a2ad196f42fcd
exit=0

$ python3 .ufo/waves/round-53/count-c1.py fd86307ad54c13edb8b6dd13182a2ad196f42fcd
C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=fd86307ad54c13edb8b6dd13182a2ad196f42fcd failed=votes
exit=1
```

C2 is met at the tip with `n=31` — the same `n` the §4 runway receipt carries. C1 is unmet at the
tip solely on `failed=votes` (`voted=0`): the vote arm reads the RECHECK voters' reports from the
**committed** tree, and the wave reports are untracked mid-wave. That is the expected pre-vote
state and is outside this seat's scope; it is recorded here only so the L1 knows the C1 reading
this seat observed.

## 7. Findings

### 7.1 The L1's untracked runway receipt is stale relative to the tip

`.ufo/waves/round-53/evidence/selftests/mori-commit-runway.txt` (untracked, written 22:41:44)
records `MATCHER: rejected 23/23 corrupted expectations` / `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23`
measured at `2a4213bf`. The tip the L1 subsequently landed (`fd86307a`, 23:28) prints
`MATCHER: rejected 26/26 corrupted expectations` / `MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31`,
and `SKILL.md:1209` at the tip pins `: PASS 31/31`. The receipt therefore disagrees with the
tip's own registry row. The §4 draft is the same receipt re-cut at the tip; the L1 should
replace the file with it (the other two receipts are unaffected — their instruments did not
change).

### 7.2 A transient working-tree inconsistency was measured and then resolved by the L1

Between this seat's first and second readings the working tree briefly carried `SKILL.md:1208`
pinning `: PASS 31/31` while `tools/fixtures/mori-commit-runway/cases.json` had been reverted to
the 23-case data bytes (`git` reported it clean at sha256 `cea80451…`), so the tool printed
`PASS 28/28` and the reconciler reported on a scratch copy:

```
pin line=1208 kind=tally prefix=MORI_COMMIT_RUNWAY_SELFTEST state=mismatch pinned=': PASS 31/31' observed=': PASS 28/28' rc=0 class=stale
```

The 26-case fixture bytes (sha256 `3a1aef20cc03fc4e323ad8b5400feeeda7cff1373ccd6f77498a8ebf5c450623`,
28393 bytes) are what the corrections commit landed, and the tip's `cases.json` now hashes to
exactly that. The inconsistency was resolved by the L1's own commit before this seat finished;
it is recorded because it explains why the receipts had to be re-cut, and because the same
overwrite was reported to this fleet by `Mo53SimpCode` (their own seat's finding).

### 7.3 Lane residue observed (not created by this seat)

`git status --porcelain` in the lane shows, besides the L1's edits and the wave's own untracked
files: an untracked `r53-data.tar` at the lane root (51 KB, dated 23:19) and a pre-existing
`.scratch/` directory holding only artifacts dated 2026-10-21…2026-10-25 (older rounds). Neither
was created by this seat. `head2.tar`, seen earlier in this seat's run, is no longer present.

### 7.4 `UNLANDED` for round 53 is dirty mid-wave (expected)

`python3 tools/mori-unlanded-check.py --repo . --round 53` on the live lane exits 1 with
`UNLANDED=dirty round=53 paths=63` — the expected mid-wave state (untracked `w1/` reports, the
evidence dir, `w1.ready*`). No `tools/` or `corpus/` path is listed.

## 8. Scope and hygiene note

No tool, counter, predicate, control or kill rule was proposed for change, and no frozen file
was edited. The one weakness this seat measured (§5 — the calibration counter's `SHONEN.md`
grammar cannot read the `PASS n/n` self-test convention round 53's new tool uses) is reported as
a named limit and a routed item for round 54, per the contract's rule that a counter weakness is
never repaired in the round that found it.

Residue: this seat created nothing inside `/home/vgpnk/Projects/shokunin/mori-shokunin` except
this report file. The only git operations were read-only (`rev-parse`, `log`, `show`, `status`,
`archive`, and a `git clone --shared` **from** the lane into this seat's scratch); no `git`/`jj`
mutation was performed in the lane or the fleet repo. The scratch tree
`/fast/scratch/hyaku/mori-r53/Mo53ExecSelftestReceipts/` was removed after the runs
(`/fast/scratch/hyaku` at 26 % used, 596 G free afterwards).

## Findings

| # | severity | finding | where |
|---|---|---|---|
| 1 | **MED** | The L1's untracked receipt `.ufo/waves/round-53/evidence/selftests/mori-commit-runway.txt` records `PASS 23/23` (measured at `2a4213bf`), but the tip the L1 landed mid-seat (`fd86307a`) prints `PASS 31/31` and `SKILL.md:1209` pins `: PASS 31/31`. The receipt disagrees with the tip's own registry row; re-cut it at the tip (§4). The other two receipts are unaffected (their instruments are byte-unchanged). | `.ufo/waves/round-53/evidence/selftests/mori-commit-runway.txt` vs `SKILL.md:1209`, `tools/mori-commit-runway.py` at `fd86307a` |
| 2 | **MED** | The frozen `SHONEN.md` tally-pin grammar (round-50/52 calibration counter, `TALLY`/`ANY_TALLY`) reads only `PREFIX pass=N fail=K`. The round-53 tool prints `MORI_COMMIT_RUNWAY_SELFTEST: PASS n/n`, which neither regex matches, so a `SHONEN.md` pin on it would re-run to `no_tally_or_timeout` (error), a `-I -B` pin is `unbound_or_not_regular` (mismatch), and a prose mention of the token counts `hidden=1`. Measured by driving the frozen `check_pins()` over candidate lines against the real tree. Named limit + round-54 routing item; **not** a counter change proposed for this round. | `.ufo/waves/round-52/count-c1.py:71-79` (grammar), `tools/mori-commit-runway.py` (output form) |
| 3 | **LOW** | The L1's untracked `evidence/selftests/mori-unlanded-check.txt` body keeps four trailing `PASS` lines and omits `PASS missing_directory_is_setup_error  setup`; the receipt is still valid (the tally line is present) but the round-52 receipts carry the full tail. The §4 draft uses the five-line form. | `.ufo/waves/round-53/evidence/selftests/mori-unlanded-check.txt` |
| 4 | **LOW** | The lane root holds an untracked `r53-data.tar` (51 KB, 2026-10-26 23:19) and a pre-existing `.scratch/` with artifacts from 2026-10-21…25. Not created by this seat; reported so the L1 can decide before the round-53 `UNLANDED` check is run for the close. | lane root `/home/vgpnk/Projects/shokunin/mori-shokunin` |
| 5 | **LOW** | `python3 tools/mori-unlanded-check.py --repo . --round 53` on the live lane exits 1 with `UNLANDED=dirty round=53 paths=63` — the expected mid-wave state (untracked `w1/` reports, evidence dir, `w1.ready*`); no `tools/` or `corpus/` path is listed. | lane working tree, round 53 |
