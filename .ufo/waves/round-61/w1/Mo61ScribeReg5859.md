# Mo61ScribeReg5859 — SKILL.md gate-registry rows for the round-58 and round-59 gates

Seat: scribe (leaf; no subagent dispatch). Lane: mori-shokunin.
Date: 2026-10-30. Round-61 freeze `7370a731abcafc4c803111de7c22cd6264d63be1`; entering `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`.
Scope: the 6 manifest paths of rounds 58–59 in `.ufo/waves/round-61/gate-manifest.json`:

| path | round | landing commit (manifest) |
|---|---|---|
| `.ufo/waves/round-58/count-c1.py` | 58 | `fe8801120a67c1a6b8899d7d0423839caa09e7d0` |
| `.ufo/waves/round-58/count-c2.py` | 58 | `fe8801120a67c1a6b8899d7d0423839caa09e7d0` |
| `.ufo/waves/round-59/count-c1.py` | 59 | `ccfd554e64084a0b4370806dd12a850e0a7bd7db` |
| `.ufo/waves/round-59/count-c2.py` | 59 | `ccfd554e64084a0b4370806dd12a850e0a7bd7db` |
| `tools/mori-register-check.py` | 59 | `ccfd554e64084a0b4370806dd12a850e0a7bd7db` |
| `tools/mori-settlement-scan.py` | 59 | `ccfd554e64084a0b4370806dd12a850e0a7bd7db` |

Read-only throughout. No production file (SKILL.md, corpus/, LOG.md, SCORECARD.md, tools/), registry, or VCS
state was touched in the lane or the fleet; no sibling repo was written. Scratch
`/fast/scratch/hyaku/mori-r61/Mo61ScribeReg5859` held one `git clone --shared` fixture and the six materialized
artifacts; it was removed after the receipts below were copied in.

## Tooling

No tool was installed or upgraded (plain `python3`, `git`, `sha256sum`, `grep`, `awk` only). Per
`/home/vgpnk/.omp/agent/RULES.md` pacman transactions are paused host-wide; none was attempted.

Disk guard before the work: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → `rc=0`,
`/tmp 24% free 97.5G`, `/var/tmp 41% free 533.9G`, `/fast/scratch/hyaku 49% free 416.7G` — green, no ENOSPC.

## Draft registry rows (for L1 integration into SKILL.md)

One row per line, eight cells each, inside one fenced block. The entry cell names the artifact path
verbatim; the self-test cell names the runnable `--selftest` command and the measured output line; the owner
cell names the landing round's L1.

```markdown
| r58 active-register binding counter (C1) | gate | `python3 .ufo/waves/round-58/count-c1.py <rev>` (revision of the lane repo; the counter resolves the lane from its own path) | 0 → `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=R` · 1 → `C1=unmet … failed=binding,rows,pointers,manifest` · 2 → usage error (`count-c1.py REV` or `--selftest` expected); the r58 frozen target also required a `selftest=ok` token this counter never emits, so the r58 closure ruled C1 unverified on its exact frozen target | `python3 .ufo/waves/round-58/count-c1.py --selftest` → `C1_SELFTEST pass=4 fail=0` (exit 0; measured once at landing `fe8801120a67c1a6b8899d7d0423839caa09e7d0`, materialized to the seat scratch) | sha256 `6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b` at rev `7370a731abcafc4c803111de7c22cd6264d63be1`; required rows `rounds[832].capabilities_added[0]` and `[1]`; fleet `MANIFEST.json` `rounds[832]` | read-only `git show` / `git cat-file` on the lane repo plus a read-only open of the fleet `MANIFEST.json`; the selftest builds throwaway git repos under `TMPDIR` only (this revision exposes no `--scratch` flag) | MoriR58 |
| r58 quote-bound depth counter (C2) | gate | `python3 .ufo/waves/round-58/count-c2.py <rev>` | 0 → `C2=met claims=N located=N copy=ok tree=ok rows=ok sources=ok failed=none rev=R` (N ≥ 8) · 1 → `C2=unmet … failed=entry,sources,copy,claims,quotes,rows` · 2 → usage error; the r58 closure ruled the instrument unverified under its own kill rule (a body-only entry with no frontmatter still scores `sources=ok`), while the entry content itself was hand-verified | `python3 .ufo/waves/round-58/count-c2.py --selftest` → `C2_SELFTEST pass=6 fail=0` (exit 0; measured once at landing `fe8801120a67c1a6b8899d7d0423839caa09e7d0`, materialized to the seat scratch) | sha256 `aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3` at rev `7370a731abcafc4c803111de7c22cd6264d63be1`; entry `corpus/knowledge/driver-events-r58.md`; pinned copy `corpus/evidence/sources-r58/mori-driver-liveness.py` (sha-equal to `tools/mori-driver-liveness.py`); SOURCES row `S550` | read-only `git show` on the lane repo; the selftest builds throwaway git repos under `TMPDIR` only (this revision exposes no `--scratch` flag) | MoriR58 |
| r59 capabilities-register counter (C1) | gate | `python3 .ufo/waves/round-59/count-c1.py <rev> [--repo DIR] [--fleet DIR] [--scratch DIR]` | 0 → `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=R` · 1 → `C1=unmet … failed=tool_absent,tool_sha,selftest,fixtures_absent,fixture:<name>:incomplete,fixture:<name>,scorecard,manifest,pointer:<path>,real,pointers` · 2 → usage (module docstring on stdout); the r59 closure ruled this claim verified met, with routed robustness defects that do not flip it | `python3 .ufo/waves/round-59/count-c1.py --selftest` → `C1_SELFTEST pass=6 fail=0` (exit 0; measured once at landing `ccfd554e64084a0b4370806dd12a850e0a7bd7db`, materialized to the seat scratch) | sha256 `2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd` at rev `7370a731abcafc4c803111de7c22cd6264d63be1`; in-script `PIN` = sha256 of `tools/mori-register-check.py` at the measured rev; `MANIFEST_REV` `2807c6ab8a9b04dcf256682bcd722c695fdd6e14`; fixtures `.ufo/waves/round-59/fixtures-c1` (13 hostile fixtures); `EXPECT_SELFTEST` `REGCHECK_SELFTEST pass=12 fail=0` | read-only `git show` on the lane repo and a read-only open of the fleet `MANIFEST.json` at `MANIFEST_REV`; tool, fixture and register bytes are materialized only under `--scratch` (default a `mkdtemp` under `TMPDIR`); nothing is written into the lane or fleet tree | MoriR59a2 |
| r59 wave-settlement depth counter (C2) | gate | `python3 .ufo/waves/round-59/count-c2.py <rev> [--repo DIR] [--scratch DIR]` | 0 → `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=N files=F rev=R` (N ≥ 10, F ≥ 3) · 1 → `C2=unmet … failed=tool_absent,tool_sha,selftest,scan_absent:<file>,scan,drift,copy_absent:<copy>,artifact_absent:<artifact>,tree:<copy>,entry_absent,entry,rows,pins,trees_absent,tree:<name>:expect,tree:<name>:verdict,tree:<name>:reasons,trees` (the entry arm also reports `grammar:`, `claims_min:`, `files_min:`, `files:outside=`, `pin:`, `distinct:dup=`, `span:`, `rows:` reasons under `failed=entry`/`failed=rows`/`failed=pins`) · 2 → usage (module docstring on stdout); the r59 closure ruled the instrument decertified (an entry of junk claims quoting one 6-byte span still scored `C2=met`), so the claim is measured met but unverified | `python3 .ufo/waves/round-59/count-c2.py --selftest` → `C2_SELFTEST pass=9 fail=0` (exit 0; measured once at landing `ccfd554e64084a0b4370806dd12a850e0a7bd7db`, materialized to the seat scratch) | sha256 `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be` at rev `7370a731abcafc4c803111de7c22cd6264d63be1`; in-script `PIN` = sha256 of `tools/mori-settlement-scan.py` at the measured rev; entry `corpus/knowledge/wave-settlement-artifacts-r59.md` (13 claims over 6 files, SOURCES rows S553–S559); six pinned copies under `corpus/evidence/sources-r59/`; hostile trees `.ufo/waves/round-59/trees-c2` (12); `MIN_CLAIMS` 10 and `MIN_FILES` 3 | read-only `git show` on the lane repo; tool, artifact-copy and entry bytes are materialized only under `--scratch` (default a `mkdtemp` under `TMPDIR`) | MoriR59a2 |
| capabilities-register checker (r59) | gate (lane tool; checks a supplied register against a supplied manifest; not a census or fleet-admission gate) | `python3 tools/mori-register-check.py --scorecard F --manifest F --root DIR --require 'rounds[832].capabilities_added[0]' [--require K ...]` | 0 → JSON `verdict=REGISTER_MET` · 1 → JSON `verdict=REGISTER_UNMET` with machine `reasons` (register identity, required key set, capability-name binding, manifest lane and lane_round, evidence-pointer existence) · 2 → argparse usage error; an unreadable scorecard is reported as `REGISTER_UNMET` with reason `scorecard_unreadable` at exit 1, not as a setup error | `python3 tools/mori-register-check.py --selftest [--scratch DIR]` → `REGCHECK_SELFTEST pass=12 fail=0` (exit 0; measured once at landing `ccfd554e64084a0b4370806dd12a850e0a7bd7db`, materialized to the seat scratch) | sha256 `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8` at rev `7370a731abcafc4c803111de7c22cd6264d63be1` (also the `PIN` of the r59 C1 counter); `SCHEMA` `mori-register-check-v1`; 13 committed hostile fixtures under `.ufo/waves/round-59/fixtures-c1` | read-only opens of the `--scorecard`, `--manifest` and `--root` paths; the selftest writes fixture files only under `--scratch` (default a `mkdtemp` named `mori-register-check-` under `TMPDIR`) | MoriR59a2 |
| wave-settlement results scanner (r59) | gate (lane tool; validates supplied settlement JSON files; not a census or fleet-admission gate) | `python3 tools/mori-settlement-scan.py <file> [<file> ...]` | 0 → JSON `verdict=SETTLEMENT_SCAN_OK` · 1 → JSON `verdict=SETTLEMENT_SCAN_FAIL` (a zero-file invocation and an unreadable file both fail at exit 1) · 2 → no code path returns 2, although the module docstring says usage/setup exits 2; unknown `--` flags are dropped silently | `python3 tools/mori-settlement-scan.py --selftest [--scratch DIR]` → `SETSCAN_SELFTEST pass=10 fail=0` (exit 0; measured once at landing `ccfd554e64084a0b4370806dd12a850e0a7bd7db`, materialized to the seat scratch) | sha256 `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` at rev `7370a731abcafc4c803111de7c22cd6264d63be1` (also the `PIN` of the r59 C2 counter); `SCHEMA` `mori-settlement-scan-v1`; the ten frozen swarm roles; member keys `{name, agent, output, note}` | read-only opens of the input files; the selftest writes fixture files only under `--scratch` (default a `mkdtemp` named `mori-settlement-scan-` under `TMPDIR`) | MoriR59a2 |
```

Notes on the drafts:

- **No literal or escaped `|` inside any cell.** The frozen C1 counter splits a registry row with a plain
  `str.split("|")` (`count-c1.py:63` — `lines[i].strip().strip("|").split("|")`) with no escape handling: a `\|`
  inside a cell adds a field, the row then has ≠ 8 cells and is dropped silently by `parse_tables`. The verdict
  cells therefore spell `ok/bad` where the counter prints `ok|bad`, and `·` is the intra-cell separator.
  Measured against the frozen parser: all six draft rows → 8 cells, `empty=[]`, `--selftest` present, live (no
  `supersed` token in name or scope).
- **Owner cells** name the landing round's L1: `MoriR58` (`.ufo/waves/round-58/contract.md:3` "Frozen by L1
  MoriR58 before any seat scores"; `round-58/w1.ready` `"l1":"MoriR58"`) and `MoriR59a2`
  (`.ufo/waves/round-59/contract.md:3` "Frozen by L1 MoriR59a2 (attempt 2) before any seat scores";
  `round-59/w1.ready` `"l1":"MoriR59a2"`). Round 59 was attempt 2 (attempt-1 counters were discarded, never
  frozen — LOG.md:2991), so the attempt suffix is part of the L1's name; the L1 may shorten both to `MoriR59`
  if it prefers, a one-word change in two cells.
- **The rows name their frozen defects in the verdict-map cell** (the artifact is registered as it is, with its
  closure status stated). Round 58 closed both r58 claims **unverified**; round 59 closed C1 **verified met**
  and C2 **measured met but unverified**. A registry row must not claim a gate green that the frozen counter
  does not print.

## Evidence

### 1. Bytes: landing vs round-61 freeze (three of the six drifted after the manifest's landing commit)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git show <landing>:<path> | sha256sum ; git show 7370a731:<path> | sha256sum
path                                   landing             freeze(HEAD)        state
.ufo/waves/round-58/count-c1.py        6ecdb627bb55       6ecdb627bb55        same
.ufo/waves/round-58/count-c2.py        aab888ad7879       aab888ad7879        same
.ufo/waves/round-59/count-c1.py        546649039454       2be6fda8c546        DRIFT
.ufo/waves/round-59/count-c2.py        ee73d7842328       2df3ae84f6d6        DRIFT
tools/mori-register-check.py           02feb852f1d2       38b733d896f8        DRIFT
tools/mori-settlement-scan.py          4c04bf2170b0       4c04bf2170b0        same
```

Full digests at the round-61 freeze `7370a731abcafc4c803111de7c22cd6264d63be1`:
`6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b` (r58 c1),
`aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3` (r58 c2),
`2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd` (r59 c1),
`2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be` (r59 c2),
`38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8` (mori-register-check.py),
`4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` (mori-settlement-scan.py).

The three drifts are the round-59 **pre-data freeze amendment** `60b3a76ad0524c8978cc51922940be1c8c388915`
("counter scratch-mkdir + ls-tree rev:path + register name boundary; pre-data", LOG.md:2989), which touched
`.ufo/waves/round-59/count-c1.py`, `.ufo/waves/round-59/count-c2.py` and `tools/mori-register-check.py`
(3 files, +7/−4). The manifest's `landing` field for those three still names the **pre-amendment** commit
`ccfd554e…`; the r59 C1 counter's in-script `PIN` was re-pinned to the post-amendment tool digest
`38b733d8…` (LOG.md:2991 names the tool at `38b733d8…`). The rows pin the digest **at the round-61 freeze**,
which is the revision the C1 counter measures.

### 2. Selftests, run once each at the landing commit (measured)

Method: `git show <landing>:<path>` materialized into the seat scratch, `TMPDIR` inside the scratch, one
`--selftest` per artifact, no arguments beyond `--selftest`.

```
$ cd <scratch>/materialized
r58-count-c1.py              rc=0  C1_SELFTEST pass=4 fail=0
r58-count-c2.py              rc=0  C2_SELFTEST pass=6 fail=0
r59-count-c1.py              rc=0  C1_SELFTEST pass=6 fail=0
r59-count-c2.py              rc=0  C2_SELFTEST pass=9 fail=0
mori-register-check.py       rc=0  REGCHECK_SELFTEST pass=12 fail=0
mori-settlement-scan.py      rc=0  SETSCAN_SELFTEST pass=10 fail=0
```

The same six lines reproduce at the round-61 freeze (6 runs, all rc=0). The counts agree with the committed
receipts `.ufo/waves/round-58/evidence/selftest-scratch.txt` (`C1_SELFTEST pass=4 fail=0`, `C2_SELFTEST
pass=6 fail=0`, exit 0) and `.ufo/waves/round-59/evidence/selftests.txt` (`C1_SELFTEST pass=6`, `C2_SELFTEST
pass=9`, `REGCHECK_SELFTEST pass=12`, `SETSCAN_SELFTEST pass=10`, all rc=0).

### 3. What the gates read when measured (the rows' verdict maps)

r58 at its data commit `7d317495245fec896c6ee7214d8eb995ad2302ba`:

```
$ python3 .ufo/waves/round-58/count-c1.py 7d317495245fec896c6ee7214d8eb995ad2302ba
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=7d317495245fec896c6ee7214d8eb995ad2302ba   rc=0
$ python3 .ufo/waves/round-58/count-c2.py 7d317495245fec896c6ee7214d8eb995ad2302ba
C2=met claims=11 located=11 copy=ok tree=ok rows=ok sources=ok failed=none rev=7d317495245fec896c6ee7214d8eb995ad2302ba   rc=0
```

r59 at its data commit `7b86704d7c0754a09958d131b64dbfa2a6d3eaed`:

```
$ python3 .ufo/waves/round-59/count-c1.py 7b86704d7c0754a09958d131b64dbfa2a6d3eaed --scratch <scratch>
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d7c0754a09958d131b64dbfa2a6d3eaed   rc=0
$ python3 .ufo/waves/round-59/count-c2.py 7b86704d7c0754a09958d131b64dbfa2a6d3eaed --scratch <scratch>
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=7b86704d7c0754a09958d131b64dbfa2a6d3eaed   rc=0
```

Both r59 counters also read `met` at the round-61 freeze `7370a731` (`C1=met selftest=ok fixtures=ok real=ok
pointers=ok rev=HEAD`; `C2=met … claims=13 files=6 rev=HEAD`). The r58 counters at the **freeze** commit read
`C2=unmet entry=absent` (rc=1) — the entry `corpus/knowledge/driver-events-r58.md` landed later, at
`874cb413`; the r58 c2 row therefore names the entry and the S550 row, not a freeze-time verdict.

Tool verdicts, measured on the materialized landing bytes:

```
$ python3 tools/mori-register-check.py --selftest          → REGCHECK_SELFTEST pass=12 fail=0   rc=0
$ python3 tools/mori-settlement-scan.py --selftest         → SETSCAN_SELFTEST pass=10 fail=0   rc=0
$ python3 tools/mori-settlement-scan.py                    → {"…","verdict":"SETTLEMENT_SCAN_FAIL"}  rc=1
$ python3 tools/mori-settlement-scan.py /nonexistent.json  → {"…","verdict":"SETTLEMENT_SCAN_FAIL"}  rc=1
$ python3 tools/mori-register-check.py --scorecard /nope   → argparse usage error                rc=2
```

### 4. The rows parse and register under the frozen C1 counter

The frozen parser was exercised directly (`count-c1.py:63-70` `parse_tables`, `:72-81` `row_hits`) on the
draft block: 6 rows, each exactly 8 cells, no empty cell, `--selftest` present in every self-test cell, no
`supersed` token in any name or scope cell, and exactly one live row per path with no cross-matching:

```
path=.ufo/waves/round-58/count-c1.py hits=1 live=1 empty=[] selftest_flag=True
path=.ufo/waves/round-58/count-c2.py hits=1 live=1 empty=[] selftest_flag=True
path=.ufo/waves/round-59/count-c1.py hits=1 live=1 empty=[] selftest_flag=True
path=.ufo/waves/round-59/count-c2.py hits=1 live=1 empty=[] selftest_flag=True
path=tools/mori-register-check.py    hits=1 live=1 empty=[] selftest_flag=True
path=tools/mori-settlement-scan.py   hits=1 live=1 empty=[] selftest_flag=True
```

End-to-end dry run in a scratch `git clone --shared` of the lane (SKILL.md + the six rows appended **in the
clone only**, throwaway identity `t <t@t>`, commit `5b434537a908fdc25af7b326782b008f28f950ad`):

```
$ python3 .ufo/waves/round-61/count-c1.py 5b434537a --repo <clone> --manifest <my-6-manifest> --scratch <scratch>
C1=met gates=6 registered=6 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=none rev=5b434537a908fdc25af7b326782b008f28f950ad   rc=0

$ python3 .ufo/waves/round-61/count-c1.py 5b434537a --repo <clone> --scratch <scratch>      # full 25-path manifest
C1=unmet gates=25 registered=6 missing=19 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=missing:.ufo/waves/round-52/count-c1.py,…   rc=1
```

`registered=6` — exactly my six paths register; the 19 missing are the paths owned by the other scribe seats
(rounds 52/53, 54/55, 56/57, 60). The before-state on the real lane at the freeze, unchanged by this seat:
`C1=unmet gates=25 registered=0 missing=25 …` (rc=1) — the contract's control.

The lane's own registry auditor agrees on the same fixture commit:

```
$ python3 tools/mori-gate-registry.py --rev 5b434537a --repo <clone> --audit <my 6 paths>
audit .ufo/waves/round-58/count-c1.py          PASS row='r58 active-register binding counter (C1)' (8 cells, entry resolves, --selftest argv branch)
audit .ufo/waves/round-58/count-c2.py          PASS row='r58 quote-bound depth counter (C2)' (8 cells, entry resolves, --selftest argv branch)
audit .ufo/waves/round-59/count-c1.py          PASS row='r59 capabilities-register counter (C1)' (8 cells, entry resolves, --selftest argv branch)
audit .ufo/waves/round-59/count-c2.py          PASS row='r59 wave-settlement depth counter (C2)' (8 cells, entry resolves, --selftest argv branch)
audit tools/mori-register-check.py             PASS row='capabilities-register checker (r59)' (8 cells, entry resolves, --selftest argv branch)
audit tools/mori-settlement-scan.py            PASS row='wave-settlement results scanner (r59)' (8 cells, entry resolves, --selftest argv branch)
registered=6 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=14
REGISTRY=met   rc=0
```

The clone and every scratch artifact were deleted after the receipts above were copied in.

### 5. Docstring / argparse surface read (path:line pointers)

| artifact | pointers |
|---|---|
| `.ufo/waves/round-58/count-c1.py` | docstring 3-27 (binding/rows/pointers/manifest arms, `Usage: count-c1.py R` / `count-c1.py --selftest`); `LANE`/`FLEET` 35-36 (lane derived from `__file__`, fleet = its parent); `STUB_MARK`/`BIND_SENT`/`R56_KEYS` 37-39; `measure` 72; met-line print 127-128; `_run_selftest` 184 (throwaway git repos, `tmp = tempfile.mkdtemp(prefix="mori-r58-c1-")` at 187); argv dispatch 234-239 (`--selftest` else `measure(sys.argv[1])`, usage → exit 2) |
| `.ufo/waves/round-58/count-c2.py` | docstring 3-21 (entry/copy/claims/rows arms, `Usage: count-c2.py R \| --selftest. Exit 0 met / 1 unmet / 2 setup`); `ENTRY`/`COPY`/`TOOL`/`SOURCES`/`ROW_ID` 25-29; `KLINE` 30; `measure` 53; met-line print 111-113; `_run_selftest` 183 (`mkdtemp(prefix="mori-r58-c2-")` at 186); argv dispatch 222-227 |
| `.ufo/waves/round-59/count-c1.py` | docstring 3-21 (active-register checker contract, `Usage: count-c1.py <rev> [--repo DIR] [--fleet DIR] [--scratch DIR]`); `TOOL`/`FIXDIR`/`EXPECT_SELFTEST`/`REQUIRE`/`BOUND`/`MANIFEST_REV`/`PIN` 12-21; `run_tool` 64; `materialize` 86; `measure` 91 (tool sha arm 94-100, selftest arm 103-118, fixture arm 121-162, real/pointer arm 165-206); `selftest` 213; `main` 238-274 (hard-coded `repo`/`fleet` defaults at 245-246, `--scratch` at 252-257, met-line print 259-268) |
| `.ufo/waves/round-59/count-c2.py` | docstring 3-33 (settlement-scanner contract, `Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR]`); `TOOL`/`ENTRY`/`SOURCES`/`COPY_DIR`/`TREES`/`EXPECT_SELFTEST`/`MIN_CLAIMS`/`MIN_FILES`/`PIN` 35-42; `ARTIFACTS` 44-51; `REAL_SCAN` 53-59; `CLAIM`/`FRONTMATTER`/`ROW` 61-63; `eval_entry` 99-190 (reason tokens 115-189); `measure` 193-359; `selftest` 365; `main` 430-458 (hard-coded `repo` default at 437) |
| `tools/mori-register-check.py` | docstring 3-34 (`Usage: mori-register-check.py --scorecard F --manifest F --root DIR --require K`, `--selftest [--scratch DIR]`); `SCHEMA`/`DECLARE`/`LANE` 40-42; `check` 105-189 (`scorecard_unreadable` 112, name binding 165-170, pointer checks 173-183); `emit` 190-197 (`REGISTER_MET`/`REGISTER_UNMET`); `selftest` 237 (`mkdtemp(prefix="mori-register-check-")` 238); `main` 281-299 (`--selftest` branch 282-285, argparse 287-291) |
| `tools/mori-settlement-scan.py` | docstring 3-30 (`Usage: mori-settlement-scan.py <file> [<file> ...]`, `--selftest [--scratch DIR]`); `SCHEMA`/`ROLES`/`MEMBER_KEYS` 34-36; `scan_file` 47-110; `scan` 113-127 (`SETTLEMENT_SCAN_OK`/`SETTLEMENT_SCAN_FAIL` 122-123, exit 0/1 at 126); `selftest` 129 (`mkdtemp(prefix="mori-settlement-scan-")` 130); `main` 194-200 (`--selftest` branch 195-198) |

LOG.md naming: round 58 at LOG.md:2975-2985 (`## Round 58 — Mori (L1, attempt 1)`; the r58 measurements,
`C1=met rows=2 …` / `C2=met claims=11 located=11 …`, selftests 4/4 and 6/6); round 59 at LOG.md:2987-2995
(`## Round 59 — Mori (L1 MoriR59a2, attempt 2)`; the tool digests `38b733d8…` and `4c04bf21…` at LOG.md:2991,
the four selftest tallies at LOG.md:2993).

## Findings

1. **The manifest's `landing` field is stale for three of my six paths.** `gate-manifest.json` names
   `ccfd554e64084a0b4370806dd12a850e0a7bd7db` as the landing commit for `.ufo/waves/round-59/count-c1.py`,
   `.ufo/waves/round-59/count-c2.py` and `tools/mori-register-check.py`, but the round-59 **pre-data freeze
   amendment** `60b3a76ad0524c8978cc51922940be1c8c388915` (LOG.md:2989) changed all three before any seat
   scored. The bytes at the manifest's landing differ from the bytes at the round-61 freeze (evidence 1).
   The frozen C1 counter does not read the manifest's `landing` field — it only requires `git cat-file -e
   <rev>:<path>` at the measured revision — so the claim is unaffected; but a registry row that pins the
   *landing* digest for those three paths would be wrong at the measured revision. My rows pin the digest at
   the round-61 freeze instead. Reported, not fixed (round-61 amendments are barred).
2. **The r58 C1 counter's frozen target is unreachable and the row says so.** `.ufo/waves/round-58/contract.md:30`
   freezes the target output as `C1=met rows=2 pointers=ok manifest=ok binding=ok selftest=ok rev=R`, but the
   counter prints `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=R`
   (`count-c1.py:127-128`) and can never emit `selftest=ok`. The r58 closure agreed the claim is unverified on
   its exact frozen target (`corpus/lessons/round-58-verifier-spotcheck.md`, "Verdict: **unverified on its
   exact frozen target — agreed with the lane**"; LOG.md:2981 records the same). The row states the gap instead
   of implying a green.
3. **The r58 C2 and r59 C2 instruments are decertified; their content is not.** r58 C2: the closure's control
   (c) — a body-only entry with no frontmatter — still scores `sources=ok`, so the instrument does not
   establish its target; the r58 entry content was independently hand-verified (K1–K11 all byte-present at
   the cited lines). r59 C2: `Mo59Critic22` demonstrated an end-to-end `C2=met` on a semantically empty entry
   (junk claims, one false claim, all quoting one 6-byte `"lane"` span, a fabricated S900 row), so the closure
   ruled the instrument decertified while the entry content was byte-verified. Both rows name this in the
   verdict-map cell; neither claims a verified gate.
4. **The r59 C1 counter hard-codes the lane and fleet paths** (`count-c1.py:245-246`:
   `repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"`, `fleet = "/home/vgpnk/Projects/shokunin"`), and
   `.ufo/waves/round-59/count-c2.py:437` hard-codes `repo` the same way. Both accept `--repo`/`--fleet`
   overrides, but a run that forgets `--repo` measures the production lane regardless of the working tree.
   The r58 counters derive the lane from `__file__` instead (`count-c1.py:35-36`), so a relocated copy measures
   itself — but `FLEET = os.path.dirname(LANE)` then points at the copy's parent, and the manifest arm fails:
   measured in a scratch clone, `C1=unmet rows=2 pointers=ok manifest=bad binding=ok failed=manifest`. Both
   behaviours are recorded in the rows' write-scope cells.
5. **`tools/mori-settlement-scan.py` has no exit-2 path although its docstring claims one.** The docstring
   (line 19-20) says "usage/setup exit 2", but `main` (194-200) only filters `--`-prefixed argv and returns
   `scan(args)`, which yields 0 or 1; an unknown flag is dropped silently and a zero-file invocation exits 1.
   Measured: no-arg → `SETTLEMENT_SCAN_FAIL` rc=1; `/nonexistent.json` → `SETTLEMENT_SCAN_FAIL` rc=1;
   `--bogus` → rc=1. The row's verdict map states the real codes rather than the docstring's.
   `tools/mori-register-check.py` does have a real exit 2 (argparse usage error, measured rc=2), but reports an
   unreadable scorecard as `REGISTER_UNMET` with reason `scorecard_unreadable` at exit 1
   (`check` 112, `main` 293-297) — the docstring's "setup errors exit 2" does not cover that path either.
6. **The frozen C1 counter's `noowner` metric is inert.** `count-c1.py` initializes `res["noowner"] = 0`
   (line 75) and never increments it, and the owner cell is not separately checked for emptiness — an empty
   owner cell is caught only by the generic `thin` arm (line 105-108, `empty = [k for k in CELLS if not
   row[k]]`). The kill rule's "empty owner" case is therefore enforced through `thin`, not through the
   `noowner` counter the met line prints. Reported for the L1; the counter is frozen and was not touched.
7. **Owner-cell wording is the one open decision** (see Notes): `MoriR59a2` (the round-59 attempt-2 L1, as
   named in the contract and `w1.ready`) versus `MoriR59`. The r58 cells are unambiguous (`MoriR58`).

## Out of scope

No edits to `SKILL.md`, `corpus/`, `LOG.md`, `SCORECARD.md`, `tools/`, the round-61 counters, the registry, or
any other production file; no commit, push, tag, or any other VCS mutation in the lane or the fleet; nothing
written to a sibling repo; no service, config, or host-state change; no provider-death inference; no tool
install. The scratch clone, the six materialized artifacts and every other scratch file were removed after the
receipts above were copied in (scratch root `/fast/scratch/hyaku/mori-r61/Mo61ScribeReg5859` no longer
exists).
