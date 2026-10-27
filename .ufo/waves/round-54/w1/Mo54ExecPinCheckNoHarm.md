# Mo54ExecPinCheckNoHarm — round-54 w1, operability no-harm check of the pin set at the data commit

Seat: executor (leaf). Lane `mori-shokunin`. Measured rev `78295c764093ff1f6cee08d7246679900bde7265`
(round-54 data), comparison revs `0b36d23e596276c70725873621fe15a28c87189f` (round-53 landed, whose
receipt is `.ufo/waves/round-53/evidence/pin-check-at-landed.txt`) and `39dcf4d7e410d362781a47e8365ca23b5c807598`
(round-54 entering tip, the rev that still carries the eight lane-root strays).

Assignment: run `tools/mori-pin-check.py` at the data rev, compare with the round-53 receipt, and answer whether
any tool, pin or selftest reads the eight lane-root files the round removed (`0`, `base.c`, `main.c`, `meminfo.c`,
`oom_kill.c`, `sd-main.c`, `user@.service.in`, `MANPAGE.md`; D3 relocation, commit `1116c092`).

Scratch: `/fast/scratch/hyaku/mori-r54/Mo54ExecPinCheckNoHarm/` (`TMPDIR` set to its `tmp/`), removed at the end of
this seat. No tools installed or upgraded; no pacman invocation; no host write; no git/jj mutation anywhere.
`bash scripts/hyaku/disk-guard.sh status` before the runs: `rc=0`, `/fast/scratch/hyaku 26% use, 595.9G free`.

## 1. Commands and receipts (all from `cd /home/vgpnk/Projects/shokunin/mori-shokunin`)

```
S=/fast/scratch/hyaku/mori-r54/Mo54ExecPinCheckNoHarm
export TMPDIR=$S/tmp
python3 tools/mori-pin-check.py --rev 78295c764093ff1f6cee08d7246679900bde7265 --scratch $S/pc
```

```
PIN_CHECK=met tally_pins=37 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=78295c764093ff1f6cee08d7246679900bde7265 baseline=no env=0 stale=0
exit=0
```

Baseline arm (every pin key of the round-53 SKILL.md must still be present):

```
python3 tools/mori-pin-check.py --rev 78295c764093ff1f6cee08d7246679900bde7265 \
  --baseline-rev 0b36d23e596276c70725873621fe15a28c87189f --scratch $S/pc2
```

```
PIN_CHECK=met tally_pins=37 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=78295c764093ff1f6cee08d7246679900bde7265 baseline=yes env=0 stale=0
exit=0
```

A/B arm at the entering tip, where the eight strays are still at the lane root:

```
python3 tools/mori-pin-check.py --rev 39dcf4d7e410d362781a47e8365ca23b5c807598 --scratch $S/pc3
```

```
PIN_CHECK=met tally_pins=37 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=39dcf4d7e410d362781a47e8365ca23b5c807598 baseline=no env=0 stale=0
exit=0
```

Each run measured 47 pin lines, all `state=match` (`grep -c "state=match"` → 47 in each of the three receipts).
The 47 lines of the data-rev run and of the round-53 receipt are structurally identical (same `line=`, `kind=`,
`prefix=`, `pinned=`); the only textual difference anywhere is the rev token that `mori-pin-check.py` substitutes
for `<REV>` in the two pins at SKILL.md:911-912:

```
diff <(grep '^pin ' round-53-receipt) <(grep '^pin ' data-rev-receipt) -> no output (after normalising the rev token)
35,36c35,36        # un-normalised
< pin line=911 ... cmd='python3 .ufo/waves/round-40/conform.py 0b36d23e596276c70725873621fe15a28c87189f --selftest'
> pin line=911 ... cmd='python3 .ufo/waves/round-40/conform.py 78295c764093ff1f6cee08d7246679900bde7265 --selftest'
< pin line=912 ... cmd='python3 tools/mori-sources-appendonly.py 0b36d23e596276c70725873621fe15a28c87189f --selftest'
> pin line=912 ... cmd='python3 tools/mori-sources-appendonly.py 78295c764093ff1f6cee08d7246679900bde7265 --selftest'
```

The entering-tip run differs from the data-rev run in exactly the same two rev tokens and nothing else
(`diff pin-entering.lines pin-r54.lines`: 2 changed lines, both the rev token).

## 2. Pin set at `78295c76` (47 lines: 37 tally, 8 digest, 2 line-count; every state=match)

| SKILL line | pin key | kind | pinned | state | instrument |
|---|---|---|---|---|---|
| 166 | MORI_SILENCE_CASES_SELFTEST | tally | `pass=24 fail=0` | match | `bash tools/mori-silence-cases.sh --selftest` |
| 168 | - | digest | `533218a566030fda…` | match | `tools/mori-round14-regressions.py` |
| 182 | R19_SELFTEST | tally | `pass=26 fail=0` | match | `tools/mori-round19-regressions.py --selftest` |
| 183 | C1_SELFTEST | tally | `pass=6 fail=0` | match | `.ufo/waves/round-44/count-c1.py --selftest` |
| 184 | - | lines | `743 lines` | match | `tools/mori-gate-registry.py` |
| 184 | GATE_REGISTRY_SELFTEST | tally | `pass=15 fail=0` | match | `tools/mori-gate-registry.py --selftest` |
| 184 | - | digest | `8b82ac999091` | match | `tools/mori-gate-registry.py` |
| 185 | C2_SELFTEST | tally | `pass=5 fail=0` | match | `.ufo/waves/round-44/count-c2.py --selftest` |
| 186 | C3_SELFTEST | tally | `pass=6 fail=0` | match | `.ufo/waves/round-44/count-c3.py --selftest` |
| 187 | MORI_DISK_RATE_SELFTEST | tally | `pass=14 fail=0` | match | `tools/mori-disk-rate.py --selftest` |
| 188 | MORI_WAVE_SETTLEMENT_SELFTEST | tally | `: PASS (23 cases, 23 passed, 0 failed)` | match | `tools/mori-wave-settlement.py --selftest` |
| 189 | MORI_R41_CALIBRATION_SELFTEST | tally | `pass=10 fail=0` | match | `tools/mori-round41-calibration.py --selftest` |
| 190 | C1_SELFTEST | tally | `pass=16 fail=0` | match | `.ufo/waves/round-45/count-c1.py --selftest` |
| 190 | C1_SELFTEST | tally | `pass=15 fail=1` | match | `.ufo/waves/round-45/fixtures/mutants/count-c1.py --selftest` |
| 190 | - | digest | `5f2deea0b35c` | match | `.ufo/waves/round-45/count-c1.py` |
| 191 | C2_SELFTEST | tally | `pass=14 fail=0` | match | `.ufo/waves/round-45/count-c2.py --selftest` |
| 191 | - | digest | `153423c48ca9` | match | `.ufo/waves/round-45/count-c2.py` |
| 191 | - | digest | `9850b3fcc888` | match | `.ufo/waves/round-45/fixtures/mutants/count-c2.py` |
| 192 | - | digest | `37fd7c24ff52…` | match | `.ufo/waves/round-45/count-c3.py` |
| 192 | - | digest | `69bf9b6eb29b…` | match | `.ufo/waves/round-45/fixtures/mutants/count-c3.py` |
| 192 | C3_SELFTEST | tally | `pass=19 fail=0` | match | `.ufo/waves/round-45/count-c3.py --selftest` |
| 192 | C3_SELFTEST | tally | `pass=17 fail=2` | match | `.ufo/waves/round-45/fixtures/mutants/count-c3.py --selftest` |
| 193 | C1_SELFTEST | tally | `pass=6 fail=0` | match | `.ufo/waves/round-44/count-c1.py --selftest` |
| 194 | - | lines | `743 lines` | match | `tools/mori-gate-registry.py` |
| 194 | GATE_REGISTRY_SELFTEST | tally | `pass=15 fail=0` | match | `tools/mori-gate-registry.py --selftest` |
| 194 | - | digest | `8b82ac999091` | match | `tools/mori-gate-registry.py` |
| 195 | C2_SELFTEST | tally | `pass=5 fail=0` | match | `.ufo/waves/round-44/count-c2.py --selftest` |
| 196 | C3_SELFTEST | tally | `pass=6 fail=0` | match | `.ufo/waves/round-44/count-c3.py --selftest` |
| 664 | MORI_PRESSURE_SELFTEST | tally | `: PASS 12/12` | match | `tools/mori-pressure.py --selftest` |
| 665 | ROUTED_CHECK_SELFTEST | tally | `pass=20 fail=0` | match | `python3 -I tools/mori-routed-check.py --selftest` |
| 739 | MORI_OOM_KILLERS_SELFTEST | tally | `: PASS 32/32` | match | `tools/mori-oom-killers.py --selftest` |
| 740 | ROUTED_R24_SELFTEST | tally | `pass=26 fail=0` | match | `tools/mori-routed-r24.py --selftest` |
| 741 | MORI_JOB_RUNWAY_SELFTEST | tally | `: PASS 21/21` | match | `tools/mori-job-runway.py --selftest` |
| 905 | MORI_SOURCE_DRIFT_SELFTEST | tally | `: PASS (6 cases)` | match | `tools/mori-source-drift.py --selftest` |
| 911 | CONFORM_SELFTEST | tally | `pass=11 fail=0` | match | `.ufo/waves/round-40/conform.py <REV> --selftest` |
| 912 | MORI_SOURCES_APPENDONLY_SELFTEST | tally | `pass=22 fail=0` | match | `tools/mori-sources-appendonly.py <REV> --selftest` |
| 938 | PIN_CHECK_SELFTEST | tally | `pass=125 fail=0` | match | `tools/mori-pin-check.py --selftest` |
| 939 | C2_SELFTEST | tally | `pass=13 fail=0` | match | `.ufo/waves/round-47/count-c2.py --selftest` |
| 971 | C1_SELFTEST | tally | `pass=34 fail=0` | match | `.ufo/waves/round-48/count-c1.py --selftest` |
| 972 | C2_SELFTEST | tally | `pass=22 fail=0` | match | `.ufo/waves/round-48/count-c2.py --selftest` |
| 973 | UNLANDED_SELFTEST | tally | `pass=17 fail=0` | match | `tools/mori-unlanded-check.py --selftest` |
| 1009 | C1_SELFTEST | tally | `pass=44 fail=0` | match | `.ufo/waves/round-49/count-c1.py --selftest` |
| 1010 | C2_SELFTEST | tally | `pass=26 fail=0` | match | `.ufo/waves/round-49/count-c2.py --selftest` |
| 1056 | C1_SELFTEST | tally | `pass=34 fail=0` | match | `.ufo/waves/round-50/count-c1.py --selftest` |
| 1057 | C2_SELFTEST | tally | `pass=31 fail=0` | match | `.ufo/waves/round-50/count-c2.py --selftest` |
| 1113 | C2_SELFTEST | tally | `pass=34 fail=0` | match | `.ufo/waves/round-51/count-c2.py --selftest` |
| 1209 | MORI_COMMIT_RUNWAY_SELFTEST | tally | `: PASS 31/31` | match | `tools/mori-commit-runway.py --selftest` |

Every observed value equals its pinned value; `rc` is 0 for every tally except the two mutant pins
(`.ufo/waves/round-45/fixtures/mutants/count-c1.py` rc 1 `pass=15 fail=1`, `.../count-c3.py` rc 1 `pass=17 fail=2`),
which match the pinned failing tallies. Diff against the round-53 receipt: no pin changed state, no pin was dropped,
none rebound, no duplicate, hidden, misattributed or stale reading. `SKILL.md` itself is the same blob at all three
revs (`git rev-parse 0b36d23e:SKILL.md 39dcf4d7:SKILL.md 78295c76:SKILL.md` → `4a0679d90df707d31f5b7ad4b7b0943eefd07431`
three times), so the pin set could not move unless a pinned instrument changed; none did:

```
git diff --name-only 0b36d23e 78295c76 -- tools/ .ufo/waves/round-40 .ufo/waves/round-44 .ufo/waves/round-45 \
  .ufo/waves/round-47 .ufo/waves/round-48 .ufo/waves/round-49 .ufo/waves/round-50 .ufo/waves/round-51
(no output)
```

Pending pin movement from the uncommitted seat drafts: the live tree has `M SKILL.md` (+38 lines) and `M PROVINCE.md`,
`M SCORECARD.md`, `M corpus/QUALITY.md`, `M corpus/README.md`, all pure additions (`git diff --stat` → `130 insertions(+),
0 deletions`), and no added SKILL line carries a self-test cell (`git diff SKILL.md | grep -E "^[-+].*(pass=|PASS|lines\`|sha256)"`
→ no output). So the measured 47-pin set is also what an integration commit of the current drafts would carry, unless a
drafting seat adds a pin cell later.

## 3. The eight removed lane-root files: does anything read them?

Presence/absence, measured:

```
git ls-tree --name-only 78295c76 | grep -E '^(0|base\.c|main\.c|meminfo\.c|oom_kill\.c|sd-main\.c|user@\.service\.in|MANPAGE\.md)$'
(no output, rc 1)                      # absent from the lane root at the data rev
ls -a /home/vgpnk/Projects/shokunin/mori-shokunin
# . .. .git .gitignore .jj .scratch .ufo AGENTS.md LOG.md MINT.md PROVINCE.md README.md SCORECARD.md SHONEN.md SKILL.md considerthese corpus tools
#                             # no strays, and no `--repo/` directory (D3 also removed it)
git ls-files .ufo/waves/round-28/misroot-lane-root .ufo/waves/round-38/misroot-lane-root
.ufo/waves/round-28/misroot-lane-root/MANPAGE.md … base.c … main.c … meminfo.c … oom_kill.c … sd-main.c … user@.service.in
.ufo/waves/round-38/misroot-lane-root/0
```

Byte exactness of the move (sha256 of the blob at `39dcf4d7:<lane-root name>` vs `78295c76:<relocated path>`,
first 16 hex; all `same`, and all eight equal the sha256 prefixes recorded in
`.ufo/waves/round-54/evidence/d3-relocation.txt`):

```
0                b24122a0f0245c0a  b24122a0f0245c0a  same
base.c           cef1a2cf3f34f683  cef1a2cf3f34f683  same
main.c           08656b0bc90c85f2  08656b0bc90c85f2  same
meminfo.c        526e512c89c58cb0  526e512c89c58cb0  same
oom_kill.c       452f1348e79c252e  452f1348e79c252e  same
sd-main.c        5ecdca43a8e0ed08  5ecdca43a8e0ed08  same
user@.service.in 72c2f40dcfced1d8  72c2f40dcfced1d8  same
MANPAGE.md       cc48b02e79255ae2  cc48b02e79255ae2  same
```

Readers, measured:

1. Pins. All 47 pinned selftests pass at `78295c76` (strays absent) and at `39dcf4d7` (strays present at the lane
   root), with identical observed values. No pin moves when the files appear or disappear, so no pinned self-test
   consumes them.
2. Pinned instruments. I extracted the 33 distinct instrument files from the 47 pin commands and searched them for the
   eight names used as a path: the only hits are `SRC_DIR + "oom_kill.c.v7.2"` (`.ufo/waves/round-50/count-c2.py:46`,
   `SRC_DIR = "corpus/evidence/sources-r50/"`), `SRC_DIR + "meminfo.c.v7.2"` (`.ufo/waves/round-51/count-c2.py:52`,
   `SRC_DIR = "corpus/evidence/sources-r51/"`), and docstring prose in `tools/mori-oom-killers.py:41-43,339` naming
   upstream `main.c:` line numbers. None is a lane-root path.
3. Tools generally. A search of `tools/*.py` for the eight names in a path position returns only unrelated matches
   (`GIT_OPTIONAL_LOCKS`, `"0" * 64` digests, fixture prose). `tools/mori-gate-registry.py` builds its population from
   `ls_at(repo, rev, "tools")` plus its `COUNTER_DIRS` (line 184-190), never the lane root; `tools/mori-source-drift.py`
   lists `corpus/evidence` (line 80). No tool globs `*.c` at the lane root.
4. Lane-level scanners. `tools/mori-wave-settlement.py scan --lane-root …` run on a `git archive` export of the entering
   tip and of the data rev gives identical totals, so the relocation is invisible to it:

```
39dcf4d7: {"empty":0,"members":2823,"misrooted":0,"missing":381,"present":2440,"states":{"partial":22,"settled":35},
           "stub":2,"unparsed":0,"unsafe":0,"waves":57,"unique_dispatch_sha256":57}  unreadable=6 ignored=1703 exit=1
78295c76: {"empty":0,"members":2823,"misrooted":0,"missing":381,"present":2440,"states":{"partial":22,"settled":35},
           "stub":2,"unparsed":0,"unsafe":0,"waves":57,"unique_dispatch_sha256":57}  unreadable=6 ignored=1703 exit=1
```

The non-zero exit is the pre-existing partial state of 22 of 57 waves in a tracked-only export (the in-flight wave's
untracked reports are not in any commit); it is the same at both revs and is not caused by the removal. The tool's
selftest pin (line 188, 23/23) is the pinned instrument and it matches.
5. Receipts. `LOG.md:1881-1883` records the round-28 sweep that copied those files to the lane root; the relocation
   receipt names each destination. `corpus/SOURCES.md` gained used-by entries only (S502, S507, S508, S514) and ten new
   rows (S515-S524); its diff contains no path reference to the lane-root copies. No document cites the lane-root
   paths as live evidence (the only textual hits are upstream URLs and historical LOG prose).

## 4. Limits of this check

- The pin arm measures `--selftest` instruments only. A live (non-selftest) reading that consumed one of the eight
  files would not appear as a pin; I bounded that risk by reading the 33 pinned instrument files and `tools/*.py` for
  the names, which cannot see dynamically constructed paths.
- `mori-pin-check.py --rev` measures an export of the committed rev; untracked wave-54 seat reports are outside every
  measurement here, and the live working tree's uncommitted doc edits were inspected separately (§2) rather than measured.
- The `diff` of two pin receipts must normalise the `<REV>` substitution, or the two pins at SKILL.md:911-912 read as
  changed while both are `match`.
- I did not run the full live instrument suite, the census, or any retention/evidence-loss scan; only the pins, the
  three pin-check arms and the wave-settlement A/B were run.

## Findings

1. LOW — no pin changed state at the data rev; the removed lane-root files are read by no pinned instrument, tool or
   selftest. `tools/mori-pin-check.py` at `78295c76` reads `PIN_CHECK=met tally_pins=37 digest_pins=8 … dropped=0
   rebound=0 … stale=0` exit 0, identical (modulo the rev token) to `.ufo/waves/round-53/evidence/pin-check-at-landed.txt`,
   and identical at `39dcf4d7` where the strays still exist. Concerns `SKILL.md` lines 166-1209 (the 47 pin cells).
2. LOW — the pins at `SKILL.md:911` and `SKILL.md:912` embed the measured revision (`<REV>`, substituted by
   `tools/mori-pin-check.py`), so two receipts taken at different revs differ textually on those two lines although both
   are `state=match`; a literal receipt-to-receipt diff shows a false change. Comparison procedure, not data.
3. LOW (named limit, carried for round 55) — the operability pin arm is selftest-only: it proves the instruments'
   self-tests still pass, not that a live collection run reads the same inputs. For this round the eight removed files
   are outside every instrument I read, but a future lane-root removal would need the live readers checked by hand.
4. INFO — `tools/mori-wave-settlement.py scan` exits 1 on a tracked-only export at both revs (22 partial of 57 waves,
   `missing=381`), unchanged by the relocation; the pinned instrument (`--selftest`, 23/23) is the one the pin set
   measures. Recorded so the L1 does not read an exit 1 from that scan as a regression.
