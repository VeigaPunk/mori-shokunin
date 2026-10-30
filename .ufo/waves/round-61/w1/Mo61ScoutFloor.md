# Mo61ScoutFloor — independent selftest floor (mori round 61)

**Verdict: ZERO DIVERGENCE.** All three counter selftests, run independently under this
seat's own scratch, reproduce the frozen receipts in `.ufo/waves/round-61/evidence/`
**byte-identical over the whole file** (stdout + `rc=` line) — stronger than the
mandated pass/fail-tally compare, which also matches exactly. No install, no tool
changes, no VCS mutation, no writes outside this report and my scratch.

## Measured revision and byte identity

- `git rev-parse HEAD` (in `/home/vgpnk/Projects/shokunin/mori-shokunin`) →
  `7370a731abcafc4c803111de7c22cd6264d63be1` = the frozen revision; `git status
  --porcelain` empty for `waves/round-61/count-c{1,2,3}.py` and `evidence/`
  (working tree clean, no drift between measured bytes and freeze).
- Working-tree shas of the counters measured this run:
  - `count-c1.py` `a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00`
  - `count-c2.py` `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8`
  - `count-c3.py` `6e1fcd3e29b1496bd41a9adab85ce5a980b8c3c05b033f2fc67b5c664f1e6630`
- Frozen evidence shas: `selftest-c1.txt`
  `cbc4d29bb548f22facf7693e2c056637d714c85a38783dc978d88f1358578bf9`, `selftest-c2.txt`
  `6cc5e04fcd153a8bdcf1719ebff2ed0c04cd0e7ace56a83cfe3b81c7b7efd1aa`, `selftest-c3.txt`
  `e01d3f23fca4864ae5fd88324998843ee99a49968af0dcc26bc0954a1fb3522e`.
- C3's r60 red-before input: `.ufo/waves/round-60/count-c3.py` working-tree sha256 =
  `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514` — exactly the
  contract's frozen r60-freeze pin, so the `r60hole-real-bytes` arm ran against the
  pinned bytes.

## Commands and receipts (verbatim)

Python 3.14.8. Disk guard before work: `/fast/scratch/hyaku` 54% used, 377.2G free
(green). Scratch: `/fast/scratch/hyaku/mori-r61/Mo61ScoutFloor/{c1,c2,c3}`; `--scratch`
passed to every counter; each selftest's synthetic fixture repos (`st-*`) were created
inside that scratch, with `git -C` addressing and the throwaway `t <t@t>` identity used
only there.

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
python3 .ufo/waves/round-61/count-c1.py --selftest --scratch $S/c1
python3 .ufo/waves/round-61/count-c2.py --selftest --floor 1 --scratch $S/c2
python3 .ufo/waves/round-61/count-c3.py --selftest --scratch $S/c3
```

All three: empty stderr, `rc=0`. `cmp` of (stdout + `rc=`) vs the evidence file:
`FULL_IDENTICAL` for each; the extracted tally lines also `cmp`-identical.

### selftest-c1 (vs evidence/selftest-c1.txt, byte-identical)

```
case good: ok=True want=True pass failed=[]
case missing: ok=False want=False pass failed=['missing:tools/absent.py']
case thin: ok=False want=False pass failed=['thin:tools/h.py:owner']
case noselftest: ok=False want=False pass failed=['noselftest:tools/i.py']
case superseded-ok: ok=True want=True pass failed=[]
case unres: ok=False want=False pass failed=['missing:tools/nothere.py']
C1_SELFTEST pass=6 fail=0
rc=0
```

### selftest-c2 (`--floor 1`, vs evidence/selftest-c2.txt, byte-identical)

```
case good: ok=True want=True pass failed=[]
case quote-missing: ok=False want=False pass failed=['quote_missing:a.rst:5-7']
case row-missing: ok=False want=False pass failed=['rows_missing:a.rst:5-7', 'rows_ne_pointers']
case orphan: ok=False want=False pass failed=['rows_orphan:b.c:25', 'quote_words:b.c:25', 'rows_ne_pointers']
case small-span: ok=False want=False pass failed=['span_small:a.rst:5-7']
case dup-quote: ok=False want=False pass failed=['quote_dup:a.rst:9']
case not-mined: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case usedby-miss: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case tampered-copy: ok=False want=False pass failed=['copy_pin:a.rst', 'loc_bad:a.rst:5-7', 'loc_bad:a.rst:9', 'sources_floor']
case no-prov: ok=False want=False pass failed=['provenance']
C2_SELFTEST pass=10 fail=0
rc=0
```

### selftest-c3 (vs evidence/selftest-c3.txt, byte-identical)

```
case all-arms-good: got=True want=True pass
case r60-tamper-detected: got=True want=True pass
case self-mutant-detected: got=True want=True pass
case wrong-pins-detected: got=True want=True pass
case blobrefusal: got=True want=True pass
case expectpin: got=True want=True pass
case r60hole-real-bytes: got=True want=True pass
case r61repair-real-bytes: got=True want=True pass
C3_SELFTEST pass=8 fail=0
rc=0
```

## Finding 1 — C2's frozen receipt is reproducible ONLY with an explicit lowered floor

The evidence files record output and `rc=` but not the invoking command line; the
`--floor 1` requirement lives only in the dispatch payload / seat spec. Probed bare
`python3 .ufo/waves/round-61/count-c2.py --selftest --scratch $S/c2-probe`
(`FLOOR_DEFAULT = 40`, count-c2.py:38): the six synthetic pointers fall below the
default floor, `good` fails with `pointer_floor:6<40` (10 such lines across cases), and
the run goes **red**: `C2_SELFTEST pass=9 fail=1`, `rc=1`. So a future independent
re-runner who invokes `count-c2.py --selftest` the same way as C1/C3 (bare) will see a
red battery and could wrongly declare the frozen receipt unreproducible. Reported, not
fixed (amendments barred). Suggested lesson note (L1's call): record the exact
selftest command lines, or the floor flag, next to the evidence receipts.

## Observations (no divergence, for the lesson's cost-of-entry ledger)

- `count-c3.py:264` hardcodes the case count (`fail={8 - npass}`, `return npass == 8`)
  where C1/C2 use `len(CASES)`/`len(cases)` — cosmetic only today (8 cases exist), but
  an added case would silently break the tally.
- `count-c3.py` selftest is **cwd-sensitive**: it reads `.ufo/waves/round-60/count-c3.py`
  and the r61 counters from `Path(os.getcwd())` (count-c3.py:216-222), not from git; a
  run from any other cwd yields `r60b=None` and a red battery unrelated to counter
  health. My runs used the lane root, matching the receipts.
- `count-c2.py` selftest swaps module globals `PINS`/`FILES`/`NAMES` (count-c2.py:246-254)
  and restores only `PINS`; `FILES`/`NAMES` stay synthetic after selftest. Inert today
  (selftest `sys.exit`s the process before any live measure) but a trap for anyone
  importing the module to run both arms in one process.
- No counter wrote anything into the lane repo: all fixtures landed under my
  `--scratch` (4.8 MB total), and the pre-existing `__pycache__/` in the wave dir is
  untouched by direct script execution.

## Tooling

No installs or upgrades were needed or performed (Python 3.14.8, coreutils
`cmp`/`diff`/`sha256sum` preexisting; channel: none; reason: none required).

## Cleanup

`/fast/scratch/hyaku/mori-r61/Mo61ScoutFloor/` removed after the receipts above were
copied into this report.
