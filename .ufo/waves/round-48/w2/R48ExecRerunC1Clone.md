# R48ExecRerunC1Clone — off-host replay of the round-48 instruments (round 48, wave 2)

**Attacked:** the landed tip `e4dfff32d4f97c7ef250e9a7538fa75d4f284492` replayed from a *clone at a
different path* (`/tmp/tmp.F1d7NAFaxc/lane`, `mktemp -d`): `count-c1.py --selftest`,
`count-c2.py e4dfff32… --repo <clone>`, `tools/mori-pin-check.py --selftest`,
`tools/mori-unlanded-check.py --selftest`, plus the full C1 predicate and the pin reconciler's real
arm from the same clone. Every run used `TMPDIR=<clone>/.scratch` (or, for the lane-side control,
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRerunC1Clone`).

**Verdict: HOLDS** — all four required replays and the two extra claim replays reproduce the
in-lane results byte-for-byte from a foreign path, with no path- or user-dependent failure.
Class of the result: *instrument portability confirmed*. Three receipt-level observations (O1-O3)
are recorded below; none changes P-C1 or P-C2, and none is a claim break.

## 0. Clone setup

```
$ D=$(mktemp -d)                                  # D=/tmp/tmp.F1d7NAFaxc
$ git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin "$D/lane"
$ git -C "$D/lane" rev-parse --show-toplevel
/tmp/tmp.F1d7NAFaxc/lane                            # exit 0 — the clone's own top level, not the lane
$ git -C "$D/lane" checkout -q --detach e4dfff32d4f97c7ef250e9a7538fa75d4f284492
$ git -C "$D/lane" rev-parse HEAD
e4dfff32d4f97c7ef250e9a7538fa75d4f284492
$ git -C "$D/lane" status --porcelain | wc -l
0
```

The clone's working tree at the detached tip carries the freeze bytes and the landed tip's
SKILL.md; `.ufo/waves/round-48/w2/` and the `after-*` receipts are **not** in the clone (they are
untracked in the lane — see O3), so the clone is exactly the landed commit.

## 1. The four required replays

Run with `cd "$D/lane"`, `TMPDIR=/tmp/tmp.F1d7NAFaxc/lane/.scratch`.

| # | command | output (last line) | exit |
|---|---|---|---|
| R1 | `python3 .ufo/waves/round-48/count-c1.py --selftest` | `C1_SELFTEST pass=34 fail=0` (34 `PASS` lines, 0 `FAIL`) | 0 |
| R2 | `python3 .ufo/waves/round-48/count-c2.py e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --repo "$D/lane"` | `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492` | 0 |
| R3 | `python3 tools/mori-pin-check.py --selftest` | `PIN_CHECK_SELFTEST pass=60 fail=0` (60 `PASS`, 0 `FAIL`) | 0 |
| R4 | `python3 tools/mori-unlanded-check.py --selftest` | `UNLANDED_SELFTEST pass=13 fail=0` | 0 |

R1 and R3 match the receipts pinned in SKILL.md and `evidence/selftest-c1.txt`
(`C1_SELFTEST pass=34 fail=0`); R2 matches `evidence/after-c2-at-e4dfff32.txt` character for
character (`claims=15`, `sources=4`, `pins=ok`, `provenance=ok`). R4's 13 arms match the
`UNLANDED_SELFTEST pass=13 fail=0` pin the landed registry row (SKILL.md:973) carries, and the
pin reconciler re-observes that pin (`state=match`, see §2). Full logs:
`.scratch/r48w2-R48ExecRerunC1Clone/r1-c1-selftest.txt`, `r2-c2.txt`, `r3-pin-selftest.txt`,
`r4-unlanded-selftest.txt`.

## 2. Extra off-host replays (the claims themselves, from the clone)

**C1 predicate, full run** (7m29.195s wall, 4 jobs; `--scratch` defaulted inside the clone):

```
$ python3 .ufo/waves/round-48/count-c1.py --tool "$D/lane/tools/mori-pin-check.py" \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --repo "$D/lane"
variant name=J1 expect=unmet got=unmet rc=1
variant name=J2 expect=unmet got=unmet rc=1
variant name=J3 expect=unmet got=unmet rc=1
variant name=J4 expect=unmet got=unmet rc=1
variant name=J5 expect=unmet got=unmet rc=1
variant name=J6 expect=unmet got=unmet rc=1
variant name=J7 expect=unmet got=unmet rc=1
variant name=J8 expect=unmet got=unmet rc=1
variant name=H1 expect=met got=met rc=0
variant name=H2 expect=met got=met rc=0
variant name=H3 expect=met got=met rc=0
variant name=H4 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
EXIT=0
```

**Pin reconciler real arm from the clone** (the tool under test, run directly, 123.5s):

```
$ python3 "$D/lane/tools/mori-pin-check.py" --rev e4dfff32… --repo "$D/lane" \
    --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
pin line=972 kind=tally prefix=C2_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 .ufo/waves/round-48/count-c2.py --selftest'
pin line=973 kind=tally prefix=UNLANDED_SELFTEST state=match pinned='pass=13 fail=0' observed='pass=13 fail=0' rc=0 cmd='python3 tools/mori-unlanded-check.py --selftest'
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
EXIT=0
```

**Other replays:** `count-c2.py --selftest` from the clone → `C2_SELFTEST pass=22 fail=0`, exit 0
(matches `evidence/selftest-c2.txt`). `count-c2.py e4dfff32…` with **no** `--repo`, from
`cwd=/tmp` → the counter resolved the clone through `__file__` (four levels up) and printed the
same `C2=met …`, exit 0. `mori-unlanded-check.py --repo "$D/lane" --round 48` → `UNLANDED=clean
round=48`, exit 0 (the clone holds the landed commit and nothing else in scope).

**Frozen bytes in the clone** (each row against the base its path implies):

```
OK   count-c1.py                   7a2a6aa09b92   (manifest:1)
OK   count-c2.py                   0055aed101bd   (manifest:2)
OK   contract.md                   052a2bf9be03   (manifest:3)
OK   v3-spec.md                    f93ef57fd977   (manifest:4)
OK   controls/stub-always-met.py   c6f12be84426   (manifest:5)
OK   controls/stub-always-unmet.py 5b716abc437e   (manifest:6)
OK   controls/tool-v2-entering.py  9832e38c3863   (manifest:7)
OK   aliyun-nas-quota.html         747fef1bcc8c   (manifest:8)
OK   errno.h                       66a5ad60566f   (manifest:9)
OK   quotactl.2.html               0d4ab273503d   (manifest:10)
OK   xfs_quota.8.html              6375e40e9c0e   (manifest:11)
DIFF tools/mori-pin-check.py       9832e38c3863 -> 85a89a3b6ba4   (manifest:12)
verified_ok=11 diff=1
```

The one DIFF is the claim's own subject (see O1).

## 3. Path- and user-dependence probes — no failure found

| probe | result |
|---|---|
| `count-c2.py` through a symlink to the clone (`$D/alias` → `$D/lane`) | `C2=met …` exit 0 |
| `count-c2.py` through a path containing a space (`$D/with space`) | `C2=met …` exit 0 |
| `mori-unlanded-check.py --repo "$D/with space" --round 48` | `UNLANDED=clean round=48` exit 0 (its top-level identity check accepts the space path) |
| `mori-unlanded-check.py --repo "$D/alias" --round 48` | `UNLANDED=clean round=48` exit 0 (symlink accepted) |
| `count-c1.py --selftest` with `HOME=/nonexistent` | `C1_SELFTEST pass=34 fail=0` exit 0 |
| `mori-pin-check.py --selftest` with `HOME=/nonexistent` | `PIN_CHECK_SELFTEST pass=60 fail=0` exit 0 |
| `mori-unlanded-check.py --selftest` with `HOME=/nonexistent`, `cwd=/tmp` | `UNLANDED_SELFTEST pass=13 fail=0` exit 0 |
| absolute-path / user / host references in the four instruments | `grep -nE '/home/\|vgpnk\|getpass\|getuser\|\$USER\|HOME\|expanduser\|socket\.gethostname'` over `count-c1.py count-c2.py tools/mori-pin-check.py tools/mori-unlanded-check.py` → **no match, exit 1** |
| fixture identity inside selftests | `count-c1.py` selftest commits its fixture with `-c user.name=selftest -c user.email=s@s.invalid`; no reliance on ambient git identity |

Mechanism (code read, exercised by the runs above): `count-c1.run_tool` invokes the tool as
`python3 -I -B <tool> --rev … --repo <repo> …` with `TMPDIR` forced to the per-variant scratch
dir, so user site-packages and `PYTHON*` variables cannot leak into a scored run; `count-c2.py`
and `mori-unlanded-check.py` read only via `git -C <repo>` / `git show`.

One path assumption, noted not failed: `count-c1.py` with no `--scratch` does
`tempfile.mkdtemp(prefix="c1-", dir=<repo>/.scratch)`, so `<repo>/.scratch` must exist. It does in
any clone of this lane because `.scratch` is **tracked** here (225 files at the tip); a repo
without it would need `--scratch`. My run left exactly one untracked dir in the clone
(`.scratch/c1-qt8gtadz/`), i.e. nothing was written into the lane.

## 4. Observations (receipt-level; none re-scores a claim)

**O1 — the freeze manifest's tool row is the *entering* bytes, and the contract's fallback
sentence would measure the wrong side of C1.** `evidence/freeze-sha256.txt:12` pins
`tools/mori-pin-check.py` at `9832e38c…`, which is also `controls/tool-v2-entering.py` and the
tool at entering `e5dbac05`; the landed tip's tool is `85a89a3b…` (identical in lane and clone).
Contract lines 13-14 say the frozen bytes are printed at the freeze commit and that "if the
working-tree bytes ever differ, the claim is measured with `git show <freeze>:<path>`". Applied
literally to C1's instrument at `e4dfff32…`, that routes the measurement to the *pre-hardening*
tool, whose receipt is `C1=unmet junk_met=8 … rc=1` (`evidence/control-c1-tool-v2-entering.txt`),
contradicting P-C1's "the tool bytes under test (`tools/mori-pin-check.py` at R)". P-C1's own
wording is what my clone run measures, and it prints `C1=met`; so the claim is not in doubt — the
freeze-manifest line simply cannot serve as a pin for the instrument the claim is about. Round-end
should cite the landed digest `85a89a3b…` for the subject and keep `9832e38c…` as the do-nothing
control only. (w1 `CritContractFreeze.md` already read the row as "not part of the freeze commit
and unchanged from entering"; this seat adds that at the landed tip the row no longer matches, so
`sha256sum -c` reports one FAILED.)

**O2 — `evidence/freeze-sha256.txt` has no single working directory that verifies it.** Its 12
rows use four bases: bare round-48 names (1-4), `controls/…` relative to the round dir (5-7), bare
source-copy names (8-11), and `tools/…` relative to the repo root (12). Run from the round-48
directory:

```
$ (cd .ufo/waves/round-48 && sha256sum -c <(grep -vE '\.html$|errno\.h$' evidence/freeze-sha256.txt))
count-c1.py: OK / count-c2.py: OK / contract.md: OK / v3-spec.md: OK
controls/stub-always-met.py: OK / controls/stub-always-unmet.py: OK
controls/tool-v2-entering.py: OK
sha256sum: tools/mori-pin-check.py: No such file or directory (os error 2)
tools/mori-pin-check.py: FAILED open or read
rc=1
```

and from `corpus/evidence/sources-r48/` the four source rows are all `OK`. Verification therefore
needs the split I used in §2 (11/12 OK by base, 1 DIFF by value). Suggest the round-end receipt
record the per-base command, not a bare `sha256sum -c`.

**O3 — the C1 post-landing receipt is empty and unlanded; C2's is unlanded.**
`evidence/after-c1-at-e4dfff32.txt` is **0 bytes**, mtime `2026-10-25 19:37:41 -03`, untracked;
`evidence/after-c2-at-e4dfff32.txt` (152 B, the `C2=met …` line) is also untracked at the landed
tip. Neither file exists in the clone of `e4dfff32…`. The lane's own routed-defect-1 instrument
reports the state:

```
$ python3 tools/mori-unlanded-check.py --repo /home/vgpnk/Projects/shokunin/mori-shokunin --round 48
UNLANDED=dirty round=48 paths=23
unlanded ?? .ufo/waves/round-48/build-w2-spec.py
unlanded ?? .ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt
unlanded ?? .ufo/waves/round-48/evidence/after-c2-at-e4dfff32.txt
unlanded ?? .ufo/waves/round-48/w2-dispatch.json
unlanded ?? .ufo/waves/round-48/w2-spec.json
unlanded ?? .ufo/waves/round-48/w2-validate.err
unlanded ?? .ufo/waves/round-48/w2.ready
unlanded ?? .ufo/waves/round-48/w2.ready.dispatched
unlanded ?? .ufo/waves/round-48/w2/R48CritEntryClaims.md
unlanded ?? .ufo/waves/round-48/w2/R48ExecCensusEnd.md
unlanded ?? .ufo/waves/round-48/w2/R48ExecLiveRefetch.md
unlanded ?? .ufo/waves/round-48/w2/R48ExecRerunC2.md
unlanded ?? .ufo/waves/round-48/w2/R48MutC2Counter.md
unlanded ?? .ufo/waves/round-48/w2/R48MutUnlanded.md
unlanded ?? .ufo/waves/round-48/w2/R48RevC2Counter.md
unlanded ?? .ufo/waves/round-48/w2/R48RevEntryErrnoAliyun.md
unlanded ?? .ufo/waves/round-48/w2/R48RevEntryQuotactl.md
unlanded ?? .ufo/waves/round-48/w2/R48RevEntryXfs.md
unlanded ?? .ufo/waves/round-48/w2/R48RevHarnessLeak.md
unlanded ?? .ufo/waves/round-48/w2/R48RevQuality.md
unlanded ?? .ufo/waves/round-48/w2/R48RevV3Code.md
unlanded ?? .ufo/waves/round-48/w2/R48ScoutEntryContext.md
unlanded ?? .ufo/waves/round-48/w2/swarm-registry.json
EXIT=1
```

Mid-wave dirt is expected; an empty `after-c1` file is not a receipt. This seat's clone run
supplies the missing line for the record: `C1=met junk_met=0 honest_unmet=0 real=met errors=0
variants=12 rev=e4dfff32…`, exit 0 (§2). The file must be filled and both receipts committed before
the round report claims "after".

**O4 — the two C1 junk-control receipts are byte-identical.** `control-c1-tool-v2-entering.txt`
and `control-c1-stub-always-met.txt` share sha256
`ca32ed7832c3a2cd84bf1ae3aef3d503d2ebda71a13b691f0f48a0e3d059d616` (both `C1=unmet junk_met=8
honest_unmet=0 real=met … rc=1`). This is correct behaviour (the entering tool is green on all
eight junk classes exactly like the always-met stub), but the receipts cannot be told apart from
their bytes; the label is the only discriminator. `control-c1-stub-always-unmet.txt`
(`honest_unmet=4 real=unmet`) is distinct.

## 5. Limits of this seat / UNVERIFIED

- Off-host replay proves the instruments are path- and user-independent and that C1/C2 reproduce
  `met` from a foreign clone; it does **not** judge whether the eight junk classes are the right
  ones, whether the quotes support their claim cells, or the prose of the entry (other w2 seats
  own those).
- The clone was taken from the lane's local repository, so it exercises the same object store;
  it does not re-fetch from any remote. `git clone` from a bare mirror was not tried.
- Not attempted: other users/UIDs (no second account), network filesystems, case-insensitive
  filesystems, a clone path with a newline or non-UTF-8 byte.
- The 7m29s C1 run was executed while many sibling seats were live on the host; timings are
  load-dependent and are not a performance claim.
- The lane-side `mori-unlanded-check` was run read-only; its first invocation took 98s and a later
  one 8.6s under different host load. No lane file was written by this seat other than its own
  report and `.scratch/r48w2-R48ExecRerunC1Clone/`.

## 6. Bounds

Leaf seat; no subagent, no background service beyond the two shell jobs for the long runs; no
`git add/commit/stash/checkout/reset/pull/push` and no `jj` command in the lane (the only
`checkout` ran inside the `mktemp -d` clone, after `rev-parse --show-toplevel` confirmed
`/tmp/tmp.F1d7NAFaxc/lane`); no edit to `tools/`, `SKILL.md`, `SOURCES.md`, `corpus/`, `LOG.md`,
`SCORECARD.md` or frozen files; no mutation of the fleet repo or siblings; no credential material
read. Tooling authorization unused: nothing installed or upgraded, no `pacman`.

Report: .ufo/waves/round-48/w2/R48ExecRerunC1Clone.md
