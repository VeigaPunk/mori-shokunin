# ExecRerunC1v1 — w2 rerun of frozen v1 C1 pin-check at landed tip T

**Seat:** ExecRerunC1v1 (mori round 47, wave w2 — falsify the landed round).
**Attack target:** C1 calibration claim — P-C1 scored with the FROZEN v1 bytes of
`tools/mori-pin-check.py` (freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0`, sha256
`e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`) at landed tip
T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63` with `--min-tally-pins 26
--baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` → `PIN_CHECK=met`.
**Verdict: HOLDS.** (See reproduction below; no kill rule triggered.)

## Reproduction (exact frozen sequence)

Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecRerunC1v1`
(also used as `TMPDIR` for the lane-tool run).

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git show 63eecf2738db96f46b0bd02b1b2dfd66787493d0:tools/mori-pin-check.py > .scratch/r47w2-ExecRerunC1v1/v1.py
$ sha256sum .scratch/r47w2-ExecRerunC1v1/v1.py
e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1  .scratch/r47w2-ExecRerunC1v1/v1.py
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecRerunC1v1 \
  python3 .scratch/r47w2-ExecRerunC1v1/v1.py \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --rev 68d66ca53d89be5c34a62f46af7c37449d9f9b63 \
    --min-tally-pins 26 \
    --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 \
    > .scratch/r47w2-ExecRerunC1v1/rerun-c1-T.txt 2>&1
$ echo $?
0
```

Observed summary line (last line of `rerun-c1-T.txt`):

```
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=68d66ca53d89be5c34a62f46af7c37449d9f9b63 baseline=yes
```

- `PIN_CHECK=met` ✓; exited **0** ✓ (evidence receipt also records `rc=0`).
- `tally_pins=28 ≥ 26` floor ✓; `mismatches=0`, `unparsed=0`, `no_command=0`, `dropped=0` ✓.
- All 33 pin lines report `state=match` with `pinned == observed` and identical `rc`
  (including both expected-failing mutant pins `rc=1` at lines 190/192 and the
  `PIN_CHECK_SELFTEST pass=34 fail=0` self-pin at SKILL.md:938).

## Line-by-line comparison vs evidence/after-c1-v1-frozen.txt

Frozen receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/evidence/after-c1-v1-frozen.txt`
(measured at `af2250d8`, whose tree equals T for every measured file — verified below).
`diff after-c1-v1-frozen.txt rerun-c1-T.txt` reports exactly 3 hunks, all fully explained
by the receipt being recorded at `af2250d8` while this seat's assigned run targets T
(the claim itself is stated for `--rev T`):

| Receipt | Rerun @ T | Explanation |
|---|---|---|
| line 1: `$ python3 <frozen v1> --rev af2250d8…` | absent | recording-harness echo, not v1.py output; not part of the check |
| line 31: conform.py selftest `cmd='…conform.py af2250d8…'` | `cmd='…conform.py 68d66ca…'` | `--rev` interpolated into the conform selftest command; `pinned='pass=11 fail=0'`, `observed='pass=11 fail=0'`, `rc=0`, `state=match` identical |
| line 32: mori-sources-appendonly.py selftest `cmd='…af2250d8…'` | `cmd='…68d66ca…'` | same — `pinned='pass=22 fail=0'`, `observed='pass=22 fail=0'`, `rc=0`, `state=match` identical |
| line 35: summary `rev=af2250d8…` | `rev=68d66ca…` | rev field tracks the measured revision; every other field identical (`tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 baseline=yes`) |
| line 36: `rc=0` | exit 0 captured via shell `$?` | same |

All 33 pin records (receipt lines 2–34) match byte-for-byte between receipt and rerun.

## Tree-equality of measured files (af2250d8 vs T)

`git diff --name-only af2250d80033ded23ec34af328068eeb85007d1c 68d66ca53d89be5c34a62f46af7c37449d9f9b63`
lists **26 files, all under `.ufo/waves/round-47/evidence/` plus w1 results/ready markers**
(`.ufo/waves/round-47/w1-results.json`, `w1.ready`, `w1.ready.dispatched`). None of the
measured files (SKILL.md, `tools/*`, `.ufo/waves/round-40/conform.py`,
`.ufo/waves/round-44|45/*`, `.ufo/waves/round-47/count-c2.py`) differ, so measuring at T
vs af2250d8 exercises identical bytes; the only output deltas are the rev-string embeds above.

## Risks / notes

- v1.py selftest passes under the rerun (`SKILL.md:938` pin: `pass=34 fail=0`).
- The check measures SKILL.md at the target rev (`--rev` path); no `--skill` override used.
- No tools installed for this seat (used existing `python3` 3.14.8 and `git`; RULES.md read,
  no channel install needed). No lane state mutated; writes confined to the seat scratch dir
  and this report file.
- Scope limit (from contract): a per-run selftest execution does not prove determinism;
  this seat re-measures the claim's verdict, it does not re-adjudicate the predicate design
  (that was w1's CritC1Predicate/RevPinCheckCode work).

## Exact retained evidence

- Scratch v1.py: `.scratch/r47w2-ExecRerunC1v1/v1.py` (sha256
  `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`).
- Rerun output: `.scratch/r47w2-ExecRerunC1v1/rerun-c1-T.txt` (34 lines, exit 0).
- Receipt compared: `.ufo/waves/round-47/evidence/after-c1-v1-frozen.txt`.
