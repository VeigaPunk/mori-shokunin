# RevC1Receipts — round 40 wave 1 (C1 receipt discipline)

Seat: read-only reviewer. Scope: every `.ufo/waves/round-40/evidence/c10-*.txt`
(25 files: 11 `c10-red-*`, 13 `c10-after*`, `c10-parity.txt`).

Ground truth used: the receipts **as committed** at `ede486b` (identical at
`8d3badd` — verified: no c10 blob differs between the two commits), the pins in
`evidence/freeze-r40.txt`, and the scored/entering commits
`265a955cc67be4eae97d2dc5a9338a25f31eb29b` / `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3`.

Inspection time: 2026-10-24T03:02–03:05-03:00. Hashes below are as observed then;
the evidence directory is being written to while the wave runs (finding F1).

## Verdict on the asked checks

- **No c10 receipt is missing any of the three** (command, measured rev, exit
  code). Checked on the committed bytes of all 25 files; see the parse table
  below. `c10-parity.txt` is the only partial: its "command" is prose (F4), and
  its exits are two `c7_exit=0` / `c8_exit=0` lines rather than one `EXIT=`.
- **Red receipts ran the v2 bytes.** All 10 v2-based red receipts name
  `fixtures/extracted/conform-v2-r39.py`; its sha256
  `fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987` equals both
  the freeze pin and `git show bb1f2457:.ufo/waves/round-39/conform.py` (sha256),
  and equals the disk file. The two remaining before receipts name the r39
  gutted copy, tracked at `265a955cc`. `c10-parity.txt`'s stated count-c7 sha
  `b92c65f2…` equals the extracted file and the `bb1f2457` blob. Caveat: the red
  receipts do **not** carry the instrument sha in-file (F3).
- **After receipts ran the landed bytes at 265a955cc.** The named checker
  `.ufo/waves/round-40/conform.py` has sha256
  `5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf` = freeze
  pin = `git show 265a955cc:.ufo/waves/round-40/conform.py` = disk; mtime
  01:58:55 < freeze 02:46:06 < commit 02:47:29 < after-receipt mtimes
  02:47:46–02:49:20 (pre-drift), and 10 after receipts carry
  `head_pin … pin=265a955cc… tip=265a955cc…`, so HEAD was the scored tip when
  they ran. `c10-after-divzero.txt` carries `pin=None tip=265a955cc…` (the
  fixture's module-level `NAME = 1/0` kills the counter — declared). The two
  selftest-family receipts (`c10-after-selftest.txt`, `c10-after-conjunct.txt`)
  have no repo-tip anchor; see residual risk.
- **No claim-content contradiction found** between receipts and contract: nine
  survivor fixtures map exactly as declared (5× `timeout_scope`
  FAIL: shadow-none/shadow-neg/cond/inf/divzero; 4× `drain_bind` FAIL:
  decoy/underscore/second-popen/tuple), all `CONFORM=unmet` exit 1; red
  counterparts `CONFORM=met` exit 0 except divzero exit 2 with no CONFORM line
  (declared); gutted-conjunct red `pass=8 fail=0` exit 0, after
  `pass=0 fail=10` exit 1 with `selftest_conjunct` in every failing list;
  multicounter red met, after unmet with per-counter `drain_bind` +
  `selftest_conjunct` violations for `survivor-barecomm.py`; selftest
  `pass=11 fail=0` exit 0.

## Findings

### F1 — HIGH (evidence integrity): three frozen c10 receipts were overwritten during wave 1

`git diff --name-only ede486b -- .ufo/waves/round-40/evidence` prints exactly:

```
.ufo/waves/round-40/evidence/c10-after-conjunct.txt
.ufo/waves/round-40/evidence/c10-after-selftest.txt
.ufo/waves/round-40/evidence/c10-red-conjunct.txt
```

Disk vs committed (`ede486b`) sha256, mtime:

| file | committed sha256 (ede486b) | disk sha256 | disk mtime |
|---|---|---|---|
| `c10-after-conjunct.txt` | `7da50a8b116bba96f76b10e090a5fb177150bd5e468c7adda64c1671738f79a7` | `f344af2e370741bd97eb4ac7e7d6198b7600ba083609e5a49673f0c51b23562b` | 03:01:55.589558155 |
| `c10-red-conjunct.txt` | `65b49f80e5a2b99abad9ffe791c902987c9e9b1a788eb4a8ac734d480515336c` | `ff06efc956d3d10b4b929cab9bb962bfd0d12b445338d29d4d3e488f0ec71601` | 03:01:55.589558155 |
| `c10-after-selftest.txt` | `8cd8486bfca9790318b9df9b5df19ccef08457b2dfbc7a82d6deb620674d50f7` | `aa10d6eb543b795bc2ef97aa092e1423395ed541d03f92126562a7283fbecd90` | 03:02:20.284238549 |

Exact diffs (committed → disk):

- both conjunct receipts: only line 1, lane-relative path →
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/…`
  (rest byte-identical);
- `c10-after-selftest.txt`: command wrapped in
  `TIMEFORMAT='WALL_SECONDS=%3R'; time …`, plus added `revision: 265a955cc…`,
  `wall_seconds: 57.371` and the shell `real/user/sys` lines; the 11 PASS lines,
  `CONFORM_SELFTEST pass=11 fail=0` and `EXIT=0` are unchanged.

Attribution (sibling reports, read-only): `w1/ExeConjunctAfter.md` contains both
conjunct commands with absolute paths, and `w1/ExeConformSelftest.md` says "The
complete output is retained in the evidence receipt" while recording
`git rev-parse HEAD` = `ede486b…` for its run. The two conjunct files share the
same nanosecond mtime (a single bulk write).

Why it matters: receipts were frozen/committed before seats ran (`8d3badd`,
02:56:11; `ede486b`, 02:56:56). Disk bytes no longer identify the frozen
receipts. In particular the added `revision: 265a955cc…` line in the on-disk
selftest receipt is an argument echo, not a measurement: the same report states
HEAD was `ede486b` at that run (the selftest arms are HEAD-independent, so no
result contradiction results, but the line cannot be read as a measured rev).
**Reviewers must quote `git show ede486b:<path>` for these three, not disk.**
Recommend restoring the three from `ede486b` or recording the rewrite as an
append-only erratum with attribution.

### F2 — LOW: freeze pin set is narrower than the contract states

`contract.md` says the pins cover "the fixture builders **and the
survivor-fixture payloads**". `freeze-r40.txt` pins only the builders
(`make-survivor-fixtures.py`, `run-c11-dags.py`) and the instruments; no
generated payload and neither gutted-conjunct copy is pinned there.

Closure I performed (so the gap does not taint the receipts):

- all six freeze paths match disk **and** the `265a955cc` blobs (sha256:
  contract `65149148…`, count-c8 `4e4d50eb…`, conform `5025b966…`, gate
  `bde5a9a3…`, builder `8ff91db7…`, dag runner `0cd7f1d2…`);
- `make-survivor-fixtures.py count-c8.py /tmp/revc1-survivors` regenerated all
  ten payloads **byte-identical** (`SAME` ×10); all ten are tracked at
  `265a955cc` and disk == blob (`SAME` ×10; plus `conform-r39-conjunct-gutted.py`
  `SAME`);
- `conform-v3-conjunct-gutted.py` (the `c10-after-conjunct.txt` instrument) is
  absent from the freeze and was committed only at `ede486b` (02:56:56), after
  the receipt ran (≤02:56). Its identity is reconstructed, not recorded: disk
  sha256 `20e324228735d39ad6bb293aac9dfd4b3a27a009a0f2ecf222731771bd2aaabf` =
  the `ede486b` blob, and `diff conform.py <gutted>` is exactly
  `734d733 <         CONJUNCT_MUTATION,` — the landed checker minus that one
  entry. The r39 gutted copy derives from the v2 bytes by removing the 4-line
  `("selftest_conjunct", …)` entry (verified by diff) and is tracked at
  `265a955cc`.

### F3 — LOW: red receipts do not name the v2 instrument bytes in-file

The ten v2-based red receipts name only the extracted path; the sha lives in
`freeze-r40.txt` (and, for count-c7 only, in `c10-parity.txt`). Verified here:
extracted conform `fe0be179…` = `git show bb1f2457:.ufo/waves/round-39/conform.py`
sha256 = freeze pin; extracted count-c7 `b92c65f2…` = `bb1f2457` blob = freeze
pin = the sha printed by `c10-parity.txt`; extracted gate `62cd4132…` =
`bb1f2457:tools/mori-sources-appendonly.py`. So provenance is sound but rests on
the freeze receipt, not on each receipt ("the before receipts name the exact
instrument bytes they ran" is satisfied only by path, not by digest).

### F4 — LOW: `c10-parity.txt` names its command in prose

`command: parity count-c7-r39 (disk == bb1f2457 bytes) vs count-c8 on rev
bb1f2457, seed 20261024` — rev and both exits are present (`c7_exit=0`,
`c8_exit=0`), but there is no executable argv (no runner path) and no single
`EXIT=`. The stated count-c7 sha was independently confirmed (F3). Replay
requires inferring the harness invocation.

### F5 — LOW: no recorded cwd; instrument paths are lane-relative

All 25 committed receipts use lane-relative instrument paths and record no
working directory. `/home/vgpnk/Projects/shokunin/.ufo/waves/round-40` does not
exist (verified), so a replay launched from the fleet root cannot resolve them
and the lane root must be inferred. The two rewritten conjunct receipts use
absolute paths; the frozen ones do not.

## Verified results (commands and outputs)

Ran from `/home/vgpnk/Projects/shokunin/mori-shokunin`:

1. `ls .ufo/waves/round-40/evidence/c10-*.txt | wc -l` → `25`
   (`c10-red-*` 11, `c10-after*` 13, parity 1); `git ls-tree --name-only ede486b
   .ufo/waves/round-40/evidence/ | grep -c c10-` → `25`.
2. Three-part parse over `git show ede486b:<path>` (python heredoc, regex
   `^command:`, `bb1f2457…|265a955cc…`, `EXIT=`/`_exit=`): every file has
   command + rev + exit; result table:
   red rev `bb1f2457` (all 11), after rev `265a955cc` (all 13), parity both;
   `missing-completeness: none`.
3. Same parse on disk copies: all 25 still carry command + rev + exit
   (the three F1 rewrites changed the command line but kept the rev and `EXIT=`).
4. Consistency assertions: `met`↔`EXIT=0`, `unmet`↔`EXIT=1` → `issues: none`;
   red head pins `pin=bb1f2457bb8d… tip=bb1f2457bb8d…` (9 receipts; divzero and
   conjunct have none), after head pins `pin=tip=265a955cc…` (10 receipts;
   divzero `pin=None tip=265a955cc…`, selftest/conjunct none).
5. `sha256sum` / `git show` comparisons:
   - extracted conform `fe0be179…` == `git show bb1f2457:.ufo/waves/round-39/conform.py`;
   - extracted count-c7 `b92c65f2…` == `git show bb1f2457:.ufo/waves/round-39/count-c7.py`;
   - extracted gate `62cd4132…` == `git show bb1f2457:tools/mori-sources-appendonly.py`;
   - landed conform `5025b966…` == freeze pin == `git show 265a955cc:.ufo/waves/round-40/conform.py` == disk;
   - all 11 generated payloads: disk == `265a955cc`/`ede486b` blob (`SAME`).
6. `python3 .ufo/waves/round-40/fixtures/make-survivor-fixtures.py
   .ufo/waves/round-40/count-c8.py /tmp/revc1-survivors` → wrote 10 files;
   `diff` each vs `fixtures/generated/` → `SAME` ×10.
7. `diff conform.py fixtures/generated/conform-v3-conjunct-gutted.py` → only
   `734d733 <         CONJUNCT_MUTATION,` (exit 1);
   `diff fixtures/extracted/conform-v2-r39.py
   fixtures/generated/conform-r39-conjunct-gutted.py` → removes the 4-line
   `("selftest_conjunct", …)` entry (exit 1).
8. `git diff --name-only ede486b -- .ufo/waves/round-40/evidence` → the three
   files in F1; per-file `sha256sum` and `stat -c '%y'` as tabulated.
9. `git rev-parse bb1f2457` → `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3`;
   `git rev-parse 265a955cc` → `265a955cc67be4eae97d2dc5a9338a25f31eb29b`;
   `git show -s --format='%H %cI %s' 265a955cc` → commit time
   `2026-10-24T02:47:29-03:00`; `stat` extracted instruments →
   `02:40:45` (before every red receipt), `conform.py` → `01:58:55`.
10. `ls /home/vgpnk/Projects/shokunin/.ufo/waves/round-40` → does not exist
    (F5).

No tool was installed or upgraded for this seat.

## Residual risk

- Receipts are records, not signatures. The only self-anchor is `head_pin`:
  10 after receipts print `pin=tip=265a955cc…` and after-divzero prints
  `tip=265a955cc…`. `c10-after-selftest.txt` and `c10-after-conjunct.txt` carry
  no tip anchor; their `265a955cc` is the argv value. The on-disk selftest copy
  demonstrably ran under HEAD `ede486b` (its author's report), which is harmless
  for a HEAD-independent selftest but means the receipt does not measure the tip.
- The "ran the landed bytes" conclusion for 02:47–02:49 rests on sha equality at
  inspection time plus mtime/freeze/commit ordering; a modify-and-revert between
  the run and inspection would be invisible.
- F1 drift is live: `c10-after-selftest.txt` was written 16 s before my `stat`,
  and scratch selftest dirs were being created at 03:03. Evidence bytes may have
  changed again after the hashes above.
- I did not re-execute any receipt and did not audit checker semantics (predicate
  soundness, drain/scope logic); those are other seats. `check predicate PASS` on
  the red receipts was not semantically re-derived.
