# Mo50bExecReexecR47 — round-47 closure re-execution (round 50, wave a2w1)

Seat: leaf executor. Assigned move: `considerthese/2026-10-26.md` suggestion 3 — re-execute what round 47's
non-author closure only *evidence-verified*. The closure
(`corpus/lessons/round-47-verifier-spotcheck.md` §1–§2) says "No lane gate or selftest was executed as a verdict
source … the remaining gate verdicts are evidence-verified from committed receipts", and it lists the specific
C1/C2 receipts it read instead of running. This report executes those receipts' commands at the scored revisions
and prints, per run, the command, revision, printed final line, exit code, the committed receipt line it should
equal, and an AGREE / DIVERGE / CANNOT-RUN verdict.

Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bExecReexecR47/` (one `git clone --shared --no-checkout` of the lane plus
five `git archive` exports; removed at the end, see §6). No tool install, no pacman transaction, no host log read, no
cgroup write, no mutating git command, nothing written outside this file. `TMPDIR` was set to the scratch `tmp/` for
every run.

## 1. Scored revisions and instrument bytes

`LOG.md` round-47 entry: freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0`, after-receipts measured at
`af2250d80033ded23ec34af328068eeb85007d1c`, report landed at lane tip
`dd17d927ffcb10908c191893472bd60e5d028c29`. Entering revision for the do-nothing controls:
`2d85e33d14198d388fd3cda9cc15ec07e57e7a53`. Registry-audit receipt revision: `4dea3d091820cb3bd73b509b6ec047d017cdb023`.

Instrument bytes re-derived from the clone, not trusted from the contract:

```
$ git -C <lane> show 63eecf27:tools/mori-pin-check.py | sha256sum
e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1  -      # = contract §"Frozen instrument bytes" (v1)
$ git -C <lane> show af2250d8:tools/mori-pin-check.py | sha256sum
9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6  -      # v2, the tree copy at the receipt revision
$ git -C <lane> show 63eecf27:.ufo/waves/round-47/count-c2.py | sha256sum
$ git -C <lane> show af2250d8:.ufo/waves/round-47/count-c2.py | sha256sum
$ git -C <lane> show dd17d927:.ufo/waves/round-47/count-c2.py | sha256sum
fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e  -      # all three identical = contract C2 digest
```

`.ufo/waves/round-47/count-*.py` holds exactly one counter, `count-c2.py`; round 47's C1 counter is the frozen
`tools/mori-pin-check.py` v1 (the contract names its bytes, and `w2/CritC1Verdict.md` states the same). Both are
re-executed below. The frozen v1 was extracted from `63eecf27` and run as a standalone file, because the tree copy at
`af2250d8` is v2 (sha above).

Claim-surface equality between the receipt revision and the final tip, checked rather than assumed:

```
$ git diff --stat af2250d8 dd17d927 -- SKILL.md tools corpus/knowledge corpus/SOURCES.md corpus/QUALITY.md
(empty, rc=0)
$ git show af2250d8:SKILL.md | sha256sum ; git show dd17d927:SKILL.md | sha256sum
2c9772fe5dc19d35bf6ee15a3ef698915384b11eda686e59aa5d0b9413d6005b  -    (both)
```

So a receipt measured at `af2250d8` is a receipt for `dd17d927` on the claim surfaces — but that is an argument,
not an execution. §2 A2 and C2 execute at `dd17d927` directly, which is the one revision the closure ruled on and
where no C1 receipt existed.

## 2. Run table — the L1 can commit this as a receipt

Command form throughout (paths abbreviated): `pin-check` = the named bytes above,
`--repo <clone>` = the `--shared` lane clone, `TMPDIR=<scratch>/tmp`, `timeout 900` per run; my shell cwd was always a
`git archive` export in scratch, and the checker itself exports the revision it measures (a pinned command therefore
runs in the checker's own export, never with the lane as cwd — though see §3: `conform.py` writes its selftest scratch
inside the lane by a hardcoded path).

### A. C1 — frozen `tools/mori-pin-check.py` v1 (`e3ef425a…`)

| # | rev measured | command (arguments as the receipt shows) | printed final line | rc | committed receipt line | verdict |
|---|---|---|---|---|---|---|
| A1 | `af2250d8` | `pin-check-v1 --repo <clone> --rev af2250d8 --min-tally-pins 26 --baseline-rev 2d85e33d` | `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=af2250d80033ded23ec34af328068eeb85007d1c baseline=yes` | 0 | `evidence/after-c1-v1-frozen.txt` last line (same text, rc=0) | **AGREE** — all 34 body lines byte-identical (33 `pin …` lines = 28 tally + 5 digest, plus the final line); 81.6 s |
| A2 | `dd17d927` | `pin-check-v1 --repo <clone> --rev dd17d927 --min-tally-pins 26 --baseline-rev 2d85e33d` | `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=dd17d927ffcb10908c191893472bd60e5d028c29 baseline=yes` | 0 | *no committed receipt at this revision* (closure's own gap: "after-c1-v1-frozen … are receipts for af2250d8, not T") | **AGREE modulo rev** — body identical to A1 after substituting the rev on both sides; 81.0 s |
| A3 | `2d85e33d` | `pin-check-v1 --repo <clone> --rev 2d85e33d --min-tally-pins 26 --baseline-rev 2d85e33d` (do-nothing) | `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 baseline=yes` | 1 | `evidence/control-c1-donothing.txt` last line (same text, rc=1) | **AGREE** |
| A4 | `2d85e33d` | `pin-check-v1 … --skill controls/control-c1-deleted.md` | `PIN_CHECK=unmet tally_pins=25 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=1 min_tally_pins=26 rev=2d85e33d… baseline=yes` | 1 | `evidence/control-c1-deleted.txt` (same text, rc=1) | **AGREE** |
| A5 | `2d85e33d` | `pin-check-v1 … --skill controls/control-c1-moved.md` | `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33d… baseline=yes` | 1 | `evidence/control-c1-moved.txt` (same text, rc=1) | **AGREE** |
| A6 | `2d85e33d` | `pin-check-v1 … --skill controls/control-c1-truncated.md` | `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33d… baseline=yes` | 1 | `evidence/control-c1-truncated.txt` (same text, rc=1) | **AGREE** |
| A7 | `63eecf27` + `--skill` junk variant | `pin-check-v1 --rev 63eecf27 --min-tally-pins 26 --baseline-rev 2d85e33d --skill controls/c1-junk/skill-vN.md`, nine variants | see A7 table below | — | `evidence/v1-junk/*.txt` | **AGREE**, 9/9 |
| A8 | — | `pin-check-v1 --selftest` | `PIN_CHECK_SELFTEST pass=22 fail=0` | 0 | `evidence/selftest-pin-check.txt` last line | **AGREE** (22 `PASS` lines, same count) |

A7 — the discriminator table the closure read instead of running (`evidence/v1-junk` vs `evidence/v2`), re-executed,
three-column agreement:

| variant | v1 printed line (mine) | v1 receipt | v2 printed line (mine) | v2 receipt | verdict |
|---|---|---|---|---|---|
| skill-v0-frozen | `PIN_CHECK=unmet … mismatches=1 …` rc 1 | same | `PIN_CHECK=unmet … mismatches=1 … rebound=0 duplicate=0` rc 1 | same | AGREE / AGREE |
| skill-v1-honest | `PIN_CHECK=met … mismatches=0 …` rc 0 | same | `PIN_CHECK=met … mismatches=0 …` rc 0 | same | AGREE / AGREE |
| skill-v2-oldcopy | `PIN_CHECK=met …` rc 0 | same | `PIN_CHECK=unmet … no_command=1 …` rc 1 | same | AGREE / AGREE |
| skill-v3-fakeecho | `PIN_CHECK=met …` rc 0 | same | `PIN_CHECK=unmet … no_command=1 …` rc 1 | same | AGREE / AGREE |
| skill-v4-weakened | `PIN_CHECK=met …` rc 0 | same | `PIN_CHECK=unmet … mismatches=1 …` rc 1 | same | AGREE / AGREE |
| skill-v5-renameprefix | `PIN_CHECK=unmet … mismatches=1 …` rc 1 | same | first run `mismatches=2` rc 1 → rerun `mismatches=1` rc 1 | `mismatches=1` rc 1 | AGREE / **DIVERGE-then-AGREE** (see §3) |
| skill-v6-deleted | `PIN_CHECK=unmet tally_pins=25 … dropped=1 …` rc 1 | same | same | same | AGREE / AGREE |
| skill-v7-entrycopy | `PIN_CHECK=met …` rc 0 | same | `PIN_CHECK=unmet … no_command=1 …` rc 1 | same | AGREE / AGREE |
| skill-v8-hide+dup | `PIN_CHECK=met …` rc 0 | same | `PIN_CHECK=unmet … unparsed=1 no_command=1 …` rc 1 | same | AGREE / AGREE |

This reproduces the closure's stated finding exactly: the frozen v1 scores **`met` on five junk variants**
(v2, v3, v4, v7, v8 — the old-copy rebind, the fake echo, the weakened pin, the entry copy, the hidden+duplicate row)
and `unmet` only on v0 (stale pin), v5 (renamed prefix) and v6 (deleted row); v2 scores `unmet` on all eight junk
variants and `met` only on the honest one. The lane's `unprovable` ruling for the frozen counter therefore rests on
reproduced bytes, not on receipts.

### B. C1 — tree copy `tools/mori-pin-check.py` v2 (`9832e38c…`)

| # | rev | command | printed final line | rc | receipt | verdict |
|---|---|---|---|---|---|---|
| B1 | `af2250d8` | `tools/mori-pin-check.py --repo <clone> --rev af2250d8 --min-tally-pins 26 --baseline-rev 2d85e33d` | `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=af2250d80033ded23ec34af328068eeb85007d1c baseline=yes` | 0 | `evidence/after-c1-v2.txt` last line (same text, rc=0) | **AGREE** — byte-identical body (33 `pin …` lines = 28 tally + 5 digest, plus the final line); 77.2 s |
| B2 | — | `tools/mori-pin-check.py --selftest` | `PIN_CHECK_SELFTEST pass=34 fail=0` | 0 | `SKILL.md:938` pin and `evidence/after-c1-v2.txt` line 938 (`observed='pass=34 fail=0'`) | **AGREE** (34 `PASS` lines) |
| B3 | `63eecf27` + junk variants | v2 column of table A7 | as A7 | — | `evidence/v2/*.txt` | **AGREE** 9/9 after the v5 rerun |

### C. C2 — `.ufo/waves/round-47/count-c2.py` (`fc77b933…`, one counter only)

| # | rev | command | printed final line | rc | receipt | verdict |
|---|---|---|---|---|---|---|
| C1 | `af2250d8` | `count-c2.py af2250d8 --repo <clone>` | `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=af2250d80033ded23ec34af328068eeb85007d1c` | 0 | `evidence/after-c2.txt` (identical) | **AGREE** (byte-identical body) |
| C2 | `dd17d927` | `count-c2.py dd17d927 --repo <clone>` | `C2=met events=8 rows=8 … source_row=ok provenance=ok rev=dd17d927ffcb10908c191893472bd60e5d028c29` | 0 | closure §2 C2 re-measured line (same text) | **AGREE** — the closure executed this one; my independent run matches |
| C3 | — | `count-c2.py --selftest` | `C2_SELFTEST pass=13 fail=0` | 0 | `evidence/selftest-c2.txt` last line | **AGREE** (13 `PASS` lines, identical body) |
| C4 | `63eecf27` | `count-c2.py 63eecf27` (do-nothing at freeze) | `C2=unmet events=8 rows=0 … source_row=bad provenance=bad rev=63eecf27… failed=entry_absent,source_row` | 1 | `evidence/control-c2-donothing-at-freeze.txt` | **AGREE** |
| C5 | `63eecf27` | `… --entry controls/control-c2-staged.md` | `C2=unmet events=8 rows=0 … failed=provenance,source_row,table` | 1 | `evidence/control-c2-staged-at-freeze.txt` | **AGREE** |
| C6 | `63eecf27` | `… --entry controls/control-c2-three.md` | `C2=unmet events=8 rows=3 name_mismatch=5 … failed=name_mismatch,source_row` | 1 | `evidence/control-c2-three-at-freeze.txt` | **AGREE** |
| C7 | `2d85e33d` | `count-c2.py 2d85e33d` (do-nothing) | `C2=unmet events=0 rows=0 … pin_mismatch=4 … failed=entry_absent,pins,source_row` | 1 | `evidence/control-c2-donothing.txt` | **AGREE** |
| C8 | `2d85e33d` | `… --entry control-c2-staged.md` | same as C7 | 1 | `evidence/control-c2-staged.txt` | **AGREE** |
| C9 | `2d85e33d` | `… --entry control-c2-three.md` | same as C7 | 1 | `evidence/control-c2-three.txt` | **AGREE** |

Setup note for C7–C9: `count-c2.py` does not exist at `2d85e33d` (it entered at the freeze), so those three receipts
can only be reproduced by running the later script with `--repo <clone> --rev 2d85e33d`; running the script *from* the
`2d85e33d` export returns rc 2 `can't open file …/revs/2d85e33d/.ufo/waves/round-47/count-c2.py` — a setup failure of
my first attempt, not a counter divergence. The receipts themselves show the same shape (script path from a later
tree, target rev `2d85e33d`).

### D. Selftests and audits of the tools round 47 registered / repaired

| # | rev | command | printed final line | rc | receipt | verdict |
|---|---|---|---|---|---|---|
| D1 | `af2250d8` | `pin-check-v1 --selftest` | `PIN_CHECK_SELFTEST pass=22 fail=0` | 0 | `evidence/selftest-pin-check.txt` | **AGREE** |
| D2 | `af2250d8` | `tools/mori-pin-check.py --selftest` (v2) | `PIN_CHECK_SELFTEST pass=34 fail=0` | 0 | `SKILL.md:938` pin / `after-c1-v2.txt` line 938 | **AGREE** |
| D3 | `af2250d8` | `tools/mori-gate-registry.py --selftest` | `GATE_REGISTRY_SELFTEST pass=15 fail=0` | 0 | `SKILL.md:184` pin (`observed='pass=15 fail=0'` in `after-c1-v1-frozen.txt`) | **AGREE** |
| D4 | `4dea3d09` | `tools/mori-gate-registry.py --rev 4dea3d09 --repo <clone> --audit tools/mori-pin-check.py --audit .ufo/waves/round-47/count-c2.py` | `registered=2 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=8` / `REGISTRY=met` | 0 | `evidence/after-registry.txt` | **AGREE** (byte-identical body incl. both `PASS` audit lines) |
| D5 | `af2250d8` | `tools/mori-sources-appendonly.py --selftest` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | 0 | `SKILL.md:912` pin (`observed='pass=22 fail=0'`) | **AGREE** |
| D6 | `4dea3d09` | `tools/mori-sources-appendonly.py 4dea3d09 --round-base 2d85e33d` | `appendonly_violations=18 ids=[S041,…,S193] deleted=[] …` + `supersede_timing … stale_supersede=[]` | 0 | `evidence/after-appendonly.txt` | **AGREE** (byte-identical body, 18 `changed S…` lines included) |

D3 and D5 were executed by the closure itself ("Re-measured: line 912 and gate-registry row"), so my runs confirm an
existing execution; D1, D2, D4 and D6 were evidence-only in the closure and are now executed.

## 3. Divergence record

One divergence, in the v2 junk column, and it did not survive a rerun.

```
$ tools/mori-pin-check.py --repo <clone> --rev 63eecf27 --min-tally-pins 26 \
    --baseline-rev 2d85e33d --skill …/controls/c1-junk/skill-v5-renameprefix.md
(pin line 911, mine)   pin line=911 kind=tally prefix=CONFORM_SELFTEST state=mismatch pinned='pass=11 fail=0'
                       observed=None rc=2 cmd='python3 .ufo/waves/round-40/conform.py 63eecf27… --selftest'
(pin line 911, receipt) pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0'
                       observed='pass=11 fail=0' rc=0 cmd='… same …'
(mine)   PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=2 … rc=1
(receipt) PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 … rc=1
```

Cause: the pinned command is the 11-arm `conform.py --selftest` (`CONFORM_SELFTEST pass=11 fail=0`, 57.8 s measured
standalone), and in that one run it exited 2 = `conformance setup error` (its own exit contract: `Exit: 0 met, 1
unmet, 2 setup error`), so the pin checker recorded `observed=None`. `pin-check` discards the command's stderr, so the
`conformance setup error: …` text is not recoverable from the receipt — this is exactly the class the 2026-10-26
reflection's suggestion 1 calls "can't run here" versus "stale". I re-ran the identical command and got the receipt's
line (`mismatches=1`, line 911 `state=match … rc=0`, 74.1 s), so the divergence is **transient under load**, not a
byte-level disagreement. Both runs were sequential within my batch; the host was running sibling seats' pin checks at
the same time.

Mechanism worth naming, not a counter change: `conform.py` hardcodes `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`
and its selftest allocates under `SCRATCH_ROOT = <LANE>/.ufo/waves/round-40/scratch` (`mori-conform-selftest-*`,
`shutil.rmtree` in `finally`, `conform.py:70,742-743,765`). So every C1 measurement of either pin-check build spawns a
live-lane-writing, timeout-bounded third-party selftest, and one flaky exit flips `PIN_CHECK` from `met` to `unmet`
— under r47's kill rule that reads as "C1 not verified". Observed side effect, not attributable to me alone: during
this re-execution window `git status --porcelain -- .ufo/waves/round-40` listed four untracked
`mori-conform-selftest-*` directories (not gitignored; `git check-ignore` rc 1), and at 10:24:2x four of them were
held by **four concurrent sibling** `conform.py b3e3453d… --selftest` processes (pids 3751677, 3753499, 3805308,
3807247) — i.e. other round-50 seats run the same instrument in the same lane path at the same time. My own runs'
directories were gone by the time I checked (they clean in `finally`); the earlier four names I saw at 10:16 had
disappeared by 10:24. No residue was left for the closure's "no uncommitted round work" check, but the window exists,
and cross-seat concurrency in that path is a live possibility for a load-induced `rc=2`.

B1 (v2 after receipt at `af2250d8`) agrees byte-for-byte on a clean run: `PIN_CHECK=met … rebound=0 duplicate=0 …`
rc 0, 77.2 s — so the v2 column's one transient does not touch the v2 after receipt.

## 4. What this closes and what it does not

Closed by execution (previously evidence-verified only): the frozen v1 after-receipt at `af2250d8` and, additionally,
at the final tip `dd17d927` where the closure said no receipt existed; the frozen v1 do-nothing and the three data
controls; the 9×2 junk discriminator table (the basis of the `unprovable` ruling); the C2 after-receipt, its 13-arm
selftest and all six control receipts; the v2 after-receipt and 34-arm selftest; the gate-registry audit and the
sources-appendonly timing run (neither of which the closure even listed as verified).

Not closed by this report: byte equality of the C2 entry's prose (the counter checks names, field sets, one emitting
call and pins; the closure's own prose/lifecycle reading is separate), the host tracefs reading
(`evidence/host-tracefs.txt`, a host fact, not a counter), the census (`evidence/census-start.txt` /
`census-end.txt`; the closure re-ran `sources-census.sh validate` itself), and the SHA-256 of the four v7.2 source
copies beyond what `count-c2.py` already re-checks (it re-hashes them every run and reported `pin_mismatch=0`).

## 5. Named limits observed (no counter, predicate or kill rule is proposed for change)

1. `pin-check` runs each pinned command once, and several pinned commands are 11–57 s mutation selftests
   (`conform.py`, `mori-gate-registry.py`, `mori-sources-appendonly.py`); a single transient non-zero exit is scored
   as a mismatch (§3). Re-executing a receipt therefore needs the same "rerun before calling it a divergence" step
   this report applied.
2. The frozen v1's `met` on five junk variants is not an accident of one variant: five distinct false-green classes
   reproduce (old-copy rebind, fake echo, weakened pin, entry copy, hidden+duplicate). This is the evidence the
   `unprovable` ruling needs; it is not a defect of the round-47 landing.
3. C1's receipt revisions and its final tip are not the same commit (`af2250d8` vs `dd17d927`). The claim surfaces are
   byte-identical (verified), and A2/B1/C2 now execute at the tip; the remaining asymmetry is only that the committed
   receipt files still name `af2250d8`.
4. `conform.py` hardcodes `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` (`conform.py:70`) and the contract
   names its absolute-path dependency as a limit; the 2026-10-26 reflection reports it exiting 2 off-host on a missing
   `/home/vgpnk/…/round-40/count-c8.py`. I read the hardcode and did not re-run the off-host case, so the off-host
   failure itself is **[INFERENCE]** from that reflection, while the hardcode is observed. Every C1 receipt in this
   round is therefore host-dependent, and my runs are host runs.

## 6. Scratch and housekeeping

Scratch root `/fast/scratch/hyaku/mori-r50/Mo50bExecReexecR47/` held `tmp/` (TMPDIR), `lane-clone/` (the single
`--shared` clone), `revs/{63eecf27,2d85e33d,4dea3d09,af2250d8,dd17d927}/` (`git archive` exports, ~320 MB each),
`frozen/` (v1 checker and `count-c2.py` extracted with `git show`) and `out/` (per-run stdout+rc). Disk guard read
first (`/fast` 618 G free, 24 % used) — no ENOSPC. Removed with `rm -rf` after this report was written; every line
cited above is reproduced in this file.

No mutating git command anywhere: `clone --shared`, `archive`, `show`, `diff --stat`, `log`, `rev-parse`, `status
--porcelain`, `check-ignore` only. `/home/vgpnk/Projects/shokuknow*` untouched. Host reads: none for this move (no
cgroup, proc, journal or dmesg path).

## Findings

1. **LOW (verified, no defect)** — `corpus/lessons/round-47-verifier-spotcheck.md` §2 C1/C2: every verdict that rested
   on a committed receipt reproduces under re-execution at `af2250d8`/`dd17d927`, including the `unprovable` ruling's
   support (frozen v1 `met` on 5 of 9 junk variants). The closure's evidence-verification was not over-claimed.
2. **LOW** — `.ufo/waves/round-47/evidence/after-c1-v1-frozen.txt` and `after-c1-v2.txt` name `rev=af2250d8`, while the
   ruled revision was `dd17d927`. The claim surfaces are byte-identical (`git diff --stat` empty; `SKILL.md` sha
   `2c9772fe…` at both), and I executed the frozen v1 at `dd17d927` with an identical body (A2), so no score moves;
   the receipt header alone does not say "valid at T".
3. **MED** — the r47 C1 instrument pins `conform.py --selftest`, whose `SCRATCH_ROOT` is the live lane
   (`conform.py:70`) and which writes/removes `mori-conform-selftest-*` dirs inside the lane working tree on every
   measurement; under load it can exit 2 and flip a `PIN_CHECK=met` receipt to `unmet` (reproduced once, §3; clean on
   rerun). Concurrency is real, not hypothetical: four sibling `conform.py b3e3453d… --selftest` processes were
   holding four such dirs at 10:24:2x. The round-50 `count-c1.py` does not invoke `conform.py` (grep: no match), so
   this affects re-runs of *r47* receipts, not the round-50 C1 measurement itself.
4. **LOW** — `.ufo/waves/round-47/count-c2.py` has no round-47 sibling `count-c1.py`; C1's adjudicator is the frozen
   `tools/mori-pin-check.py` v1, extracted from `63eecf27`. Anyone re-running "the round-47 counters" from the wave
   directory alone will find only `count-c2.py` and must reconstruct the C1 instrument from the contract's digest —
   which is what §1 did.
5. **LOW** — the three `2d85e33d` C2 control receipts (`evidence/control-c2-{donothing,staged,three}.txt`) cannot be
   reproduced by running the counter *at* that revision (script absent, rc 2 `can't open file`); they require the
   later script with `--repo/--rev`. Reproduced that way they agree exactly (C7–C9). Setup shape, not a counter
   defect.
6. **LOW** — the v2 junk column's `skill-v5-renameprefix` receipt (`evidence/v2/skill-v5-renameprefix.txt`,
   `mismatches=1`) is only reproducible when `conform.py --selftest` passes; the first rerun produced
   `mismatches=2` with `line=911 … observed=None rc=2`. A later reader should treat that receipt as load-sensitive,
   which finding 3 explains.
