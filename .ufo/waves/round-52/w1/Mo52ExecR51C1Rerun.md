# Mo52ExecR51C1Rerun — re-execute round-51 C1 at the measured revision

Seat: executor (leaf). Assignment (round-52 wave w1, contract
`.ufo/waves/round-52/contract.md` §considerthese): suggestion 3 of `considerthese/2026-10-26.md` — re-execute what
the round-51 closure only evidence-verified. Concretely: run the frozen round-51 C1 counter at the revision it
measured and compare with the committed receipt, field by field.

- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`; lane tip during this seat
  `075436b1346ca659afb8be7a46f0e67e4170aa83`; entering tip of the round `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`.
- Measured revision: `70e68cdd28c44a95039b9175a947e15664618351` ("round-51: wave w1 integration part 2 …",
  2026-10-26 20:29:13 -0300).
- Receipt compared: `.ufo/waves/round-51/evidence/c1-at-landed.txt` (sha256
  `63671c159719fd574f599d1094bd831cd10a7cb7a542c789b916b47d052771bf`; added by `a5087527`, identical at `8e3df7e5`,
  `a5087527` and HEAD).
- Host: MACHINE_ID, Linux `7.2.11-arch1-1`, 32 CPUs, `MemAvailable: 18513788 kB` / `MemTotal: 31721796 kB`;
  `python3 -V` → `Python 3.14.8`; `git --version` → `git version 2.56.0`; `bwrap --version` → `bubblewrap 0.13.1`.
- Tooling installed or upgraded by this seat: none. Nothing written outside this report and
  `/fast/scratch/hyaku/mori-r52/Mo52ExecR51C1Rerun/` (scratch removed, see §8).

Why the re-execution is a new measurement and not a re-read: the round-51 verifier spot-check states, at
`corpus/lessons/round-51-verifier-spotcheck.md:7`, "… ran no lane gate (`count-c1.py`, `count-c2.py`,
`tools/mori-pin-check.py` were not executed)", and at `:48`, "Both claims rest on lane-owned counters (gates). Per
§Gate standard (Closure consequence) I verified their committed evidence and did not execute them." The counter's
verdict in the receipt was therefore never re-run by the closure.

## 1. The instrument I ran is the frozen one

| check | command | observed |
|---|---|---|
| bytes vs round-51 freeze list | `grep count-c1 .ufo/waves/round-51/evidence/freeze-sha256.txt` | `622f650c1ade984d8c9abed20e7a7fd08930861a698398f36d4c3a770aff355c  .ufo/waves/round-51/count-c1.py` |
| bytes in the working tree | `sha256sum .ufo/waves/round-51/count-c1.py` | `622f650c…355c` (equal to the frozen value) |
| bytes at the measured rev | `git show 70e68cdd:.ufo/waves/round-51/count-c1.py \| sha256sum` | `622f650c…355c` |
| working tree = rev | `git diff --stat 70e68cdd -- .ufo/waves/round-51/count-c1.py` | empty |
| pinned tool bytes at rev and at tip | `git show <rev>:tools/mori-pin-check.py \| sha256sum`, same for `.ufo/waves/round-40/conform.py` | pin-check `32685b93…81f0` at both `70e68cdd` and `075436b1`; conform `7f5174d5…fa23` at both |

So the counter I ran is byte-identical to the frozen predicate, and the two instruments its arms execute are
byte-identical at the measured rev and at today's tip.

## 2. The two runs

Both runs used the literal command from the assignment, with `TMPDIR` inside this seat's scratch and the lane as
the source repo (the counter's default `--repo`/`--hide`, because the script lives in the lane).

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/count-c1.py 70e68cdd28c44a95039b9175a947e15664618351 --scratch /fast/scratch/hyaku/mori-r52/Mo52ExecR51C1Rerun/s
classified: pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 tools/enva.py --selftest' class=env
classified: pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 cmd='python3 tools/envb.py --selftest' class=env
classified: pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 tools/stla.py --selftest' class=stale
classified: pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 cmd='python3 tools/stlb.py --selftest' class=stale
classified: pin line=7 kind=tally prefix=OKAY_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/okay.py --selftest'
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no env=2 stale=2
kill_residue_first: -
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=125,fail=0 rev=70e68cdd28c44a95039b9175a947e15664618351 failed=-
exit=0
WALL=114s
```

Run 2 (same command, `--scratch …/s2`, fresh `TMPDIR`; run 1 stopped at 21:15:33 -0300, run 2 at 21:17:32 -0300)
produced the same 9 counter lines and `exit=0`, `WALL=114s`. Its body text is byte-identical to run 1's.

## 3. Field-by-field comparison with `c1-at-landed.txt`

The receipt holds 10 lines; my run's counter output is lines 2–10 of that receipt plus the same trailer. Removing
the `$ …` header line from both sides and comparing with `diff -u` gave **no differences**: each body is 9 lines,
1219 bytes, sha256 `687510e431bdfd28199a547701d2c5efb95139877c9ef550ee18ff118a86e8e0`, for both run 1 and run 2.

| field (receipt line) | receipt | this seat, at `70e68cdd` | agrees |
|---|---|---|---|
| `ENVA_SELFTEST` row (2) | `state=mismatch pinned='pass=3 fail=0' observed=None rc=2 class=env` | identical | yes |
| `ENVB_SELFTEST` row (3) | `state=mismatch pinned='pass=4 fail=0' observed=None rc=1 class=env` | identical | yes |
| `STLA_SELFTEST` row (4) | `state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 class=stale` | identical | yes |
| `STLB_SELFTEST` row (5) | `state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 class=stale` | identical | yes |
| `OKAY_SELFTEST` row (6) | `state=match … rc=0`, no class | identical | yes |
| classification summary (7) | `PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no env=2 stale=2` | identical | yes |
| `kill_residue_first` (8) | `-` | `-` | yes |
| `C1=` line arm `kill_residue` (9) | `0` | `0` | yes |
| `C1=` line arm `relocated` (9) | `met`, `reloc_mismatch=0` | `met`, `0` | yes |
| `C1=` line arm `classified` (9) | `ok` | `ok` | yes |
| `C1=` line arm `selftest` (9) | `pass=125,fail=0` | `pass=125,fail=0` | yes |
| `C1=` line rev (9) | `70e68cdd28c44a95039b9175a947e15664618351` | same full rev | yes |
| `C1=` line verdict/`failed` (9) | `C1=met … failed=-` | `C1=met … failed=-` | yes |
| exit (10) | `exit=0` | `exit=0` | yes |
| wall clock | not recorded | 114 s (run 1), 114 s (run 2) | receipt silent |

Divergence: **none in any measured field.** The only textual difference between the two files is receipt line 1,
the command echo: the receipt writes the relative script path and the placeholder `--scratch <scratch>`; this seat
records `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/count-c1.py` and the literal scratch
directory. That is the round-51 spot-check's D-b ("the receipt's command line is not literally re-runnable as
written"), re-confirmed here, not a measurement divergence.

Independent corroboration of the largest field: `grep -c '^PASS' .ufo/waves/round-51/evidence/selftests/mori-pin-check.txt`
→ `125`, last line `PIN_CHECK_SELFTEST pass=125 fail=0`, and `selftest=pass=125,fail=0` is what the counter printed
for me from a `git archive` of `70e68cdd` in my own scratch.

The receipt at the earlier rev (`c1-at-data.txt`, `87e0c374`, `selftest=pass=119`) was not compared: different
revision, and the counter measures the tool at the rev it is given.

## 4. Determinism

Two full runs of the same command at the same rev produced byte-identical output, including the timing-dependent
arm A (`kill_residue=0`, `kill_residue_first: -`) and the bubblewrap arm B (`relocated=met`,
`reloc_mismatch=0`). This is two samples, not a proof of stability; arm A kills 3 s after the first write, so the
sample does not speak for other kill moments (round-51 contract's own named limit).

## 5. Does the verdict carry beyond the measured rev?

The spot-check's argument, re-measured:

| range | command | observed |
|---|---|---|
| `70e68cdd..8e3df7e5` (round-51 tip) | `git diff --stat 70e68cdd 8e3df7e5 -- tools .ufo/waves/round-40 .ufo/waves/round-51/count-c1.py` | empty |
| `70e68cdd..075436b1` (today's lane tip) | `git diff --stat 70e68cdd 075436b1 -- tools .ufo/waves/round-40 .ufo/waves/round-51/count-c1.py .ufo/waves/round-51/count-c2.py` | empty |

`SKILL.md` is also unchanged across `70e68cdd..075436b1`; the only round-51 files added in that range are
`evidence/c1-at-landed.txt`, `evidence/c2-at-landed.txt`, `evidence/census-end.txt`. Tools and the counter being
byte-identical, the C1 verdict recorded at `70e68cdd` still describes what the instrument does today.

## 6. What the reproduction does and does not settle

It settles that the receipt's numbers are what the frozen instrument prints on this host at that rev, twice, with
the lane as source. It does not settle that the four arms measure a real property of the lane: arm D runs the
tool's own `--selftest`, and arms B/C run the tool over fixtures the tool defines, so a green reading is the
instrument agreeing with itself plus bubblewrap and git behaviour on this host (round-51 contract named limits
carry unchanged).

## 7. Lane and host hygiene of these runs

| check | command | observed |
|---|---|---|
| scratch removed by the counter | `ls -la /fast/scratch/hyaku/mori-r52/Mo52ExecR51C1Rerun/s …/s2` | both empty after the runs; seat scratch removed at the end (§8) |
| round-51 evidence untouched | `git status --porcelain --ignored -- .ufo/waves/round-51/` in the lane | empty, `rc=0` |
| lane `.scratch` untouched | `ls -ld .scratch` | mtime `2026-10-26 10:53:54 -0300`, before this seat started |
| stray dirs in `/var/tmp` | `ls -d /var/tmp/pin-check-*` before run 2 and after it | `4` before, `4` after — my runs contributed none; the four (empty, mode 0700, `21:15:30 -0300`) come from a concurrent seat or from a prior invocation, and `tools/mori-pin-check.py:955` creates `pin-check-*` under `$TMPDIR` (which my runs set) with `$TMPDIR` unset falling back to `/var/tmp` (`:952`) |

Untracked lane residue I observed but did **not** create: `git status` in the lane lists
`.ufo/waves/round-39/scratch/mori-conform-selftest-*` directories (5 at 21:18, all created
`21:16:10`–`21:18:13 -0300`), `corpus/lessons/round-52.md`,
`.ufo/waves/round-52/check-history-rows.py`, `.ufo/waves/round-52/evidence/m2-history-rows.txt` and the wave's own
`w1/*.md` reports. The `mori-conform-selftest-*` tree is what `.ufo/waves/round-40/conform.py`'s self-test writes
under `SCRATCH_ROOT = <repo>/.ufo/waves/round-39/scratch` (`conform.py:735`, `:473`): a lane run of that self-test
still deposits untracked directories in the repo it tests. None appeared during run 1's window
(`21:13:36`–`21:15:30`), and my counter executes `conform.py` only inside its clones (`c0`, `c1`) or the bwrap
namespace where the lane is a `--tmpfs`, so these are a concurrent seat's in-lane runs, not mine.

## 8. Considerthese 3 — answer for the lesson section

Draft (fenced; the L1 integrates, I edit no lesson file):

```
### Re-execution of the round-51 C1 gate (round 52, w1/Mo52ExecR51C1Rerun)

The round-51 closure verified C1 from committed receipts and did not run the gate. Re-run on the same host at the
measured revision `70e68cdd` (`python3 .ufo/waves/round-51/count-c1.py 70e68cdd --scratch <outside the lane>`,
114 s, exit 0), twice, the counter printed the receipt's nine body lines byte for byte
(sha256 `687510e4…`): `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok
selftest=pass=125,fail=0 … failed=-`, with `class=env` x2, `class=stale` x2 and `env=2 stale=2`. Divergence: none
in any measured field; the only difference is the receipt's elided `--scratch <scratch>` command line (D-b). The
carry argument was re-measured: `tools/`, `.ufo/waves/round-40/conform.py`, `SKILL.md` and the counter are
byte-identical from `70e68cdd` to today's tip. What a replay adds is the environment it does not record: python
3.14.8, git 2.56.0, bubblewrap 0.13.1 on Linux 7.2.11 — a future divergence cannot be attributed without them.
```

## 9. Named limits of this report

- Two runs, one host, one rev. Arm A's kill moment (3 s after the first write) and arm B's one hidden path are
  sampled, not proven.
- I re-ran the instrument; I did not independently re-measure the property (no second implementation of the four
  arms). Green means "the frozen counter prints this on this host", which is exactly the gap considerthese 3 names.
- The comparison is against the receipt as committed; the receipt itself is not in the round-51 freeze list
  (`grep -c c1-at-landed …/freeze-sha256.txt` → `0`), so I pinned it by sha256 at three commits instead.
- Residue attribution (mine vs concurrent sibling seats) rests on differential observation (run 1 created none;
  run 2 created none in `/var/tmp`), not on process tracing.

## Findings

1. **LOW — `.ufo/waves/round-51/evidence/c1-at-landed.txt:1`**: the recorded command line elides the scratch path
   (`--scratch <scratch>`), so the receipt is not literally re-runnable as written (round-51 spot-check D-b, still
   open). Re-run agrees on every measured field; the literal command is recorded in §2 of this report.
2. **LOW — `.ufo/waves/round-51/evidence/c1-at-landed.txt`**: the receipt records no environment (python, git,
   bubblewrap versions, kernel). A replay that diverges later cannot tell a host change from a lane change. This
   seat supplies the environment it used (Linux 7.2.11-arch1-1, python 3.14.8, git 2.56.0, bubblewrap 0.13.1).
3. **LOW — `.ufo/waves/round-51/evidence/c1-at-landed.txt` is not covered by the round-51 freeze list**
   (`freeze-sha256.txt` lists the counters and controls, not this receipt). Its bytes are stable (`63671c15…` at
   `a5087527`, `8e3df7e5` and HEAD), but nothing in the round freezes them.
4. **LOW — `tools/mori-pin-check.py:952-955`**: a `pin-check` invocation without `TMPDIR` creates
   `pin-check-*` under `/var/tmp`; a SIGKILLed run (arm A's design) leaves the empty directory behind. Four such
   empty dirs were present on this host; my runs (which set `TMPDIR`) added none. Outside the repo, so the
   `kill_residue` predicate is unaffected; recorded as residue, not a counter defect.
5. **LOW — `.ufo/waves/round-40/conform.py:735`**: a lane run of `conform.py --selftest` deposits untracked
   `mori-conform-selftest-*` directories in `.ufo/waves/round-39/scratch/` of the repo it tests (5 present during
   this seat, created by concurrent seats, none in my run windows). Supports the contract's in-lane-writer
   inventory item (round-51 closure §5 item 8); routed, not changed here.
6. **LOW — claim-level, for the L1's lesson text**: the reproduction confirms the receipt's numbers but is not an
   independent judge of C1's arms (same frozen instrument, same host, same fixtures). The round-51 verdict should
   keep reading "evidence-verified and counter-reproduced", not "independently verified".
