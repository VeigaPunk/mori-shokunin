# Mo59Executor40 — tool selftests (REGCHECK_SELFTEST / SETSCAN_SELFTEST) + frozen-counter falsification battery

Seat: `Mo59Executor40` (executor). Round 59, wave `w1`.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Freeze rev: `60b3a76ad0524c8978cc51922940be1c8c388915` (amended freeze)
Entering rev: `2b9f03975bfb6e508f35074ac8181ec8bf54e805`
Scratch: `/fast/scratch/hyaku/mori-r59/Mo59Executor40/` (created with `mkdir -p`;
`TMPDIR` pointed there; cleaned before yield).

**No production file, corpus file, registry row, SCORECARD, LOG or lane VCS
mutation.** The only file written outside scratch is this report. All
falsification probes were run against a throwaway clone under scratch
(`git clone --no-checkout --shared` → `$SCRATCH/clone`), never the lane.
The lane working tree was re-verified clean of my writes at the end
(`git status --porcelain` shows only the pre-existing round-59 dispatch
artifacts `w1/`, `w1.ready.dispatched`, `w1-dispatch.stderr`,
`assimilation/` plus other seats' `LOG.md`/`SHONEN.md`/`corpus/QUALITY.md`
edits, none of them mine).

---

## 1. Primary deliverable — both tool selftests with `--scratch`

Both tools were materialized from the **freeze revision** (not the worktree)
into `$SCRATCH/tools/`, so the run is pinned to the frozen bytes:

```
$ git show 60b3a76...:tools/mori-register-check.py   | sha256sum
38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8  -
$ git show 60b3a76...:tools/mori-settlement-scan.py   | sha256sum
4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9  -
```
Both equal the frozen `PIN` constants (`count-c1.py:49`,
`count-c2.py:56`) and equal the worktree bytes (no post-freeze drift).

```
$ export TMPDIR=$SCRATCH
$ python3 $SCRATCH/tools/mori-register-check.py --selftest --scratch $SCRATCH/st-regcheck
REGCHECK_SELFTEST pass=12 fail=0
rc=0

$ python3 $SCRATCH/tools/mori-settlement-scan.py --selftest --scratch $SCRATCH/st-setscan
SETSCAN_SELFTEST pass=10 fail=0
rc=0
```

Both exactly match the frozen expected tokens `REGCHECK_SELFTEST pass=12
fail=0` (`count-c1.py:46`) and `SETSCAN_SELFTEST pass=10 fail=0`
(`count-c2.py:55`). Deterministic: 3 consecutive runs each, identical
output and rc=0.

**Frozen counter selftests** (the counters' own `--selftest` mode):

```
$ python3 .ufo/waves/round-59/count-c1.py --selftest
C1_SELFTEST pass=6 fail=0
rc=0

$ python3 .ufo/waves/round-59/count-c2.py --selftest
C2_SELFTEST pass=9 fail=0
rc=0
```
Matches contract.md §C1 (`C1_SELFTEST pass=6 fail=0`) and §C2
(`C2_SELFTEST pass=9 fail=0`).

---

## 2. Frozen counters at the three revisions

```
$ python3 .ufo/waves/round-59/count-c1.py 60b3a76... --scratch $SCRATCH/c1-freeze
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76ad0524c8978cc51922940be1c8c388915
rc=0

$ python3 .ufo/waves/round-59/count-c1.py 2b9f0397... --scratch $SCRATCH/c1-enter
C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f03975bfb6e508f35074ac8181ec8bf54e805 failed=tool_absent,selftest,fixtures_absent,real,pointers
rc=1

$ python3 .ufo/waves/round-59/count-c1.py 8ff344ff... --scratch $SCRATCH/c1-head
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=8ff344ff18924c1ea63d46c3b3969f9fea05bc51
rc=0
```

```
$ python3 .ufo/waves/round-59/count-c2.py 60b3a76... --scratch $SCRATCH/c2-freeze
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=60b3a76... failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,...,copy_absent:corpus/evidence/sources-r59/w1-settlement-r58.json,entry_absent,tree
rc=1

$ python3 .ufo/waves/round-59/count-c2.py 2b9f0397... --scratch $SCRATCH/c2-enter
C2=unmet selftest=bad scan=bad drift=bad trees=bad entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=2b9f0397... failed=copy_absent:...,drift,entry_absent,scan,selftest,tool_absent,tree,trees,trees_absent
rc=1

$ python3 .ufo/waves/round-59/count-c2.py 8ff344ff... --scratch $SCRATCH/c2-head
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=8ff344ff... failed=copy_absent:...,entry_absent,tree
rc=1
```

**Frozen bytes unchanged** (kill-rule check, contract.md §C1/§C2):

```
2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd  count-c1.py   (freeze == worktree)
2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be  count-c2.py   (freeze == worktree)
427fca0bf2a928133c09b37746e58a2d98c6c551651046f31320531a43de107e  contract.md    (freeze == worktree)
```

**Status reading:** C1 is **met** at the freeze revision and at lane HEAD.
C2 is **unmet** at the freeze revision and at HEAD — its `entry`/`rows`/
`pins`/`tree` arms need `corpus/knowledge/wave-settlement-artifacts-r59.md`
and the six copies under `corpus/evidence/sources-r59/`, neither of which
exists at any revision currently in the lane (`git cat-file -e
60b3a76:corpus/knowledge/wave-settlement-artifacts-r59.md` → absent). The
`trees=ok` token must not be read as `C2=met`.

---

## 3. Hostile-fixture battery (C1) — 13/13 UNMET with the frozen expect prefix

Each fixture extracted at the freeze revision into scratch and run against
the frozen tool with `--require rounds[832].capabilities_added[0]
--require rounds[832].capabilities_added[1]`. **Every fixture returns rc=1
and `verdict=REGISTER_UNMET`**; the reason set covers its `expect.txt`
prefix.

| fixture | expect | rc | reasons (verbatim) |
|---|---|---|---|
| f01-stub-only | `binding` | 1 | `binding:declared_register=0(capabilities_sections=1)`; `keys:missing=rounds[832].capabilities_added[0]`; `keys:missing=rounds[832].capabilities_added[1]` |
| f02-two-declared | `binding` | 1 | `binding:declared_register=2(capabilities_sections=3)`; both `keys:missing=` |
| f03-dup-key | `keys` | 1 | `keys:duplicate=rounds[832].capabilities_added[0]`; `manifest:name=…[0]` |
| f04-missing-key | `keys` | 1 | `keys:missing=rounds[832].capabilities_added[1]` |
| f05-pointer-missing | `pointers` | 1 | `pointers:missing=.ufo/waves/round-56/evidence/c2-at-landed.txt` |
| f06-pointer-absolute | `pointers` | 1 | `pointers:bad=/etc/passwd` |
| f07-pointer-relative-parent | `pointers` | 1 | `pointers:bad=../../etc/passwd` |
| f08-manifest-name-altered | `manifest:name` | 1 | `manifest:name=rounds[832].capabilities_added[0]` |
| f09-manifest-substring-only | `manifest:name` | 1 | `manifest:name=rounds[832].capabilities_added[0]` |
| f10-manifest-foreign-lane | `manifest:lane` | 1 | `manifest:lane='kotoba'` ×2 |
| f11-manifest-wrong-index | `manifest` | 1 | `manifest:lane=None`; `manifest:entry_missing=…[0]`; `manifest:lane_round=…[0]`; … (same ×2) |
| f12-lane-round-mismatch | `manifest:lane_round` | 1 | `manifest:lane_round=…[0]`; `manifest:lane_round=…[1]` |
| f13-empty-pointer | `pointers` | 1 | `pointers:none=rounds[832].capabilities_added[1]` |

---

## 4. Hostile-tree battery (C2) — 12/12 UNMET with the frozen expect prefix

Each tree extracted at the freeze revision and evaluated with the frozen
counter's own `eval_entry()` (imported from `count-c2.py`, not re-implemented).
**All 12: `ok=False`, verdict matches expectation, expect prefix covered.**

| tree | expect | eval_entry | reasons (verbatim) | claims/files |
|---|---|---|---|---|
| t01-no-frontmatter | `frontmatter` | UNMET | `frontmatter:source`; `frontmatter:verified-at`; `frontmatter:recheck`; `frontmatter:coverage-map`; `rows:no_source_ids` | 10/3 |
| t02-dup-k | `distinct` | UNMET | `distinct:dup=K1` | 10/3 |
| t03-quote-wrong-line | `span` | UNMET | `span:1` | 10/3 |
| t04-stale-pin | `pin` | UNMET | `pin:1` | 10/3 |
| t05-few-claims | `claims_min` | UNMET | `claims_min:7` | 7/3 |
| t06-outside-file | `files` | UNMET | `files:outside=tools/mori-settlement-scan.py` | 10/4 |
| t07-no-row | `rows:missing` | UNMET | `rows:missing=S901` | 10/3 |
| t08-extra-cell-row | `rows:bad_row` | UNMET | `rows:bad_row=S901` | 10/3 |
| t09-usedby-other | `rows:usedby` | UNMET | `rows:usedby=S901` | 10/3 |
| t10-queued-status | `rows:status` | UNMET | `rows:status=S901` | 10/3 |
| t11-quote-short | `span` | UNMET | `span:short=1` | 10/3 |
| t12-malformed-claim | `grammar` | UNMET | `grammar:- **K5** — claim 5. Quote: ` "seats": 3,,`; `claims_min:9` | 9/3 |

---

## 5. Scan arm evidence (C2) — real files OK, r53 drift FAIL

Real scan over the five `REAL_SCAN` files materialized at the freeze rev
(`count-c2.py:69-75`), each with the `.ufo` artifact byte-identical:

```
verdict=SETTLEMENT_SCAN_OK   rc=0
r54 seats=74 members=74 | r55 64/64 | r56 64/64 | r57 64/64 | r58 64/64
```
All five satisfy `members == seats`.

Drift file `.ufo/waves/round-53/w1-results.json`:
```
verdict=SETTLEMENT_SCAN_FAIL  rc=1
failures: member[0..66]:extra_keys=report_file   (67 members, all with the extra key)
```
Exactly the frozen expectation ("`report_file` extra keys — schema drift,
reported not fixed").

Full sweep of **all 16** committed `*-results.json` at the freeze rev:
14 wave-results files scan OK with `members==seats`; the r53 file FAILS on
`extra_keys=report_file`; and the two round-23 falsify artifacts
(`.ufo/waves/round-23/falsify/*/bounded-results.json`, schema
`mori-r23-mut-*-summary-v1`) fail with `results_not_list` / `seats_mismatch`
/ `lane_bad` / `wave_bad` / `round_bad` — they are not wave-results objects
and are correctly rejected. They are outside `REAL_SCAN`, so the counter is
unaffected.

---

## 6. Falsification probes — counter arms that do **not** discriminate

All probes run on the scratch clone `$SCRATCH/clone` (a throwaway
`git clone --shared` of the lane at the freeze rev). Every probe is a
commit in that clone; the lane was never written to.

### F1 — C1 `real` arm accepts a truncated capability-name cell (HIGH)

`count-c1.py:200` checks `all(bmap[k].startswith(v) for k, v in BOUND.items())`
— a **prefix** test on the MANIFEST string, and the tool's own name rule
(`tools/mori-register-check.py:168-171`) accepts `entry.startswith(name)`
when the next char is not alnum/`_`. The SCORECARD capability cell is
therefore never required to *equal* the frozen bound name.

Probe: shorten both SCORECARD capability cells to `dual` / `strict`.
```
$ python3 .ufo/waves/round-59/count-c1.py 3505bd39... --repo $SCRATCH/clone --scratch $S/mut-c1name
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=3505bd39f0b0da93cb730a59812b07d14e8b240b
rc=0
```
Tool-level confirmation: `verdict=REGISTER_MET`, `reasons=[]`.
The contract's C1 claim reads "exact key/name/pointer binding"; the name
binding is a prefix match, so `dual` satisfies it. The register row can
name the capability `dual` and still score C1=met.

### F2 — C1 `real` arm ignores the "what it can now do" cell entirely (MEDIUM)

`count-c1.py:200` / `tools/mori-register-check.py:145-176` read cells
`[0]` (key), `[1]` (capability), `[3]` (evidence) and `[4]` (round). Cell
`[2]` — the descriptive column — is never read.

Probe: replace both descriptive cells with `TOTAL NONSENSE DESCRIPTION` /
`ALSO NONSENSE`.
```
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=4f6e01e309d7f65601d59e59462bd2c26e079cac
rc=0
```

### F3 — C1 `real` arm accepts *any* resolvable evidence pointer (MEDIUM)

The pointer arm only checks that the backticked path is safe and exists
under `--root` / `git cat-file -e R:path`. It does not bind the pointer to
the round-56 artifacts the claim names.

Probe: replace both evidence cells with `` `README.md`; `corpus/SOURCES.md` ``.
```
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=4cdf3b66bf2bba9d8bb49cdb752a0b89a02a96b5
rc=0
```
(For contrast, pointers to a path absent from the repo *do* fail:
`pointers:missing=…`; and a fleet-repo path fails the `git cat-file`
check: `failed=pointer:PROTOCOL.md,…`.)

### F4 — C1 fixture arm does not pin the fixture *count* (MEDIUM)

`count-c1.py:124-129` lists whatever directories exist under
`fixtures-c1/` and requires each to fail; there is no `len(dirs) == 13`
assertion. Deleting one of the 13 fixtures still yields `fixtures=ok`:
```
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=ec9f91bfb3092bacc1d194934c226da949762888
rc=0
```
(13 → 12 fixtures, arm still green.) The same holds for the C2 tree arm:
deleting `t12-malformed-claim` (12 → 11 trees) still yields `trees=ok` and
`C2=met` on a probe tree — see F8.

### F5 — C1 fixture arm: an emptied `expect.txt` is not detected (LOW)

`count-c1.py:140` splits `expect.txt` on `,`; an empty file yields
`[""]`, and `any(r.startswith("") for r in reasons)` is trivially true for
any reason list. Probe with `f13/expect.txt` emptied:
```
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=c2d09246937f7d9473ef6036c232bea4d93d491b
rc=0
```
The fixture still has to fail, but no longer has to fail *for the frozen
reason*. Low impact (the expect files are frozen bytes), but it is an
unguarded step of the frozen battery.

### F6 — C2 `entry` arm tolerates malformed claim lines (HIGH)

`count-c2.py:122` records `grammar:<line>` for a claim-shaped line that
fails the `CLAIM` regex, but `count-c2.py:303-305` computes `entry_ok`
from the reason prefixes `("frontmatter","distinct","claims_min","files",
"span","entry_absent")` — **`grammar` is not in that tuple**, so a
grammar-violating line never flips `entry` to bad.

Probe: a valid 12-claim entry plus one extra claim-shaped line whose
quoted span contains a newline (so it cannot match `CLAIM`):
```
$ python3 .ufo/waves/round-59/count-c2.py 74f981509c618df61afae7f9f88e05d5bdc626b9 --repo $S/clone --scratch $S/mut-grammar
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=12 files=6 rev=74f981509c618df61afae7f9f88e05d5bdc626b9
rc=0
```
The direct `eval_entry()` call confirms the reason is present and
*unhandled*:
```
ok=False  reasons=['grammar:- **K3** — S901 offset span over .ufo/wa', …]  stats={'claims': 12, 'files': 6}
entry_ok per counter logic: True     rows_ok: True     pins_ok: True
```
Note the asymmetry: the hostile tree `t12-malformed-claim` *is* detected
(`grammar:` reason, `ok=False`) — because the tree arm tests `ok != want_ok`
rather than the reason-prefix tuple. The same defect in the **real** entry
is invisible.

### F7 — C2 `rows` arm: S-ids are harvested only from the entry's first 10 lines (HIGH)

`count-c2.py:112` takes `head = lines[:10]` and `count-c2.py:161-163`
harvests S-ids with `SID = re.compile(r"source:\s*(S\d+)")` **only over
those 10 lines**. An S-id mentioned in a claim body line is never checked,
and a claim may cite a copy whose S-id has no registry row at all.

Probe A — entry declares only `source: S901` in the head while its 12
claims name `S901`…`S906`; the registry keeps only the `S901` row:
```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=12 files=6 rev=a4acafa0ad8f0e12edb17c36d6a247a713574da4
rc=0
```
Six distinct artifacts cited, one registry row. The contract's C2 claim
requires "the registry rows those claims cite (status mined, `used-by`
exactly the entry)" and "one per cited artifact copy" — that per-copy
binding is not enforced by the counter.

Probe B (same shape, 6 source lines in the head but the used-by cell
carrying a trailing comma, `…,r59.md, |`) → `rows=bad` (`rows:usedby=S901`).
So a trailing comma in `used-by` *is* caught; what is not caught is a
missing S-row per copy.

Probe C — `used-by` naming two entries (`…,r59.md, corpus/knowledge/other.md`)
→ `rows=bad` for all six ids. Exact-match on `used-by` works.

Probe D — registry rows dated `2019-01-01` / recheck `9999d` → `C2=met`.
The counter checks `cells[7] == "mined"` and `cells[10] == ENTRY` but not
the `opened` / `recheck` columns, so the contract's "S### rows opened this
round" is not enforced.

### F8 — C2 tree arm does not pin the tree *count* (MEDIUM)

`count-c2.py:320-324` iterates whatever tree directories exist; no
`len(tdirs) == 12` assertion. With a valid entry and only 11 of 12 trees
present:
```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=12 files=6 rev=60faf1566636b34902f6e09cb3f106a29c1bd315
rc=0
```

### F9 — C2 drift arm accepts *any* non-zero exit, not the named drift (LOW)

`count-c2.py:255-259` requires only `p.returncode != 0` for the r53 file.
Probe: replace the r53 file with non-JSON text → still `drift=ok`. The
counter does not require the failure to be the `report_file` extra-key
drift the contract names.

### F10 — C2 `tree` arm is sound against a symlinked copy (control)

Probe: replace one copy with a symlink to `/etc/passwd` → `tree=bad`
(`tree:corpus/evidence/sources-r59/w1-results-r55.json`) plus
`copy_absent:` for the rest. Symlink substitution is detected.

---

## 7. Non-vacuity controls (the green arms are discriminating)

- **C1 fixtures arm fires.** Restoring `f04-missing-key`'s scorecard and
  manifest to the real register (so it scores MET) → the counter reports
  `failed=fixture:f04-missing-key`, `fixtures=bad`, rc=1. The arm is not
  vacuous.
- **C1 tool-SHA arm fires.** Appending one byte to
  `tools/mori-register-check.py` → `failed=tool_sha,…`, rc=1.
- **C1 MANIFEST-revision pin fires.** Pointing `--fleet` at a repo that
  does not contain `2807c6ab…` → `failed=manifest,real,pointers`, rc=1.
- **C2 data arms are reachable.** A probe tree (6 byte-equal copies, a
  12-claim entry with correct pins/spans, 6 registry rows) makes the
  frozen counter print the contract's exact target shape:
  `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=12 files=6`, rc=0.
  So C2 is satisfiable — the missing ingredient is only the landed data.
- **C2 scan/drift arms fire.** Replacing the r53 file's content changes the
  drift verdict; replacing a REAL_SCAN file's content breaks `scan`.
- **C2 tree arm fires.** A repaired tree (frontmatter prepended to `t01`)
  flips to `ok=True` and is rejected by the counter as
  `tree:t01:verdict`.

---

## 8. Findings summary

| # | Arm | Severity | Finding |
|---|---|---|---|
| F1 | C1 `real` name binding | HIGH | Prefix match, not equality — the SCORECARD capability cell may be `dual` / `strict` and C1 still scores `met`. |
| F2 | C1 `real` descriptive cell | MEDIUM | The "what it can now do" column is never read; nonsense text scores `met`. |
| F3 | C1 `real` evidence pointer | MEDIUM | Evidence pointers need only resolve; `README.md` + `corpus/SOURCES.md` satisfy the round-56 rows. |
| F4 | C1 fixture / C2 tree count | MEDIUM | Neither arm pins its fixture/tree count; deleting one of 13 / 12 keeps the arm green. |
| F5 | C1 empty `expect.txt` | LOW | Emptyed expect file is not detected; the fixture no longer has to fail for the frozen reason. |
| F6 | C2 `entry` grammar | HIGH | `grammar:` reasons are excluded from the `entry_ok` prefix tuple; a malformed claim line in the real entry is invisible, while the same defect *is* caught in hostile tree `t12`. |
| F7 | C2 `rows` S-id harvesting | HIGH | S-ids are read only from the entry's first 10 lines; six cited artifacts can be backed by one registry row, and `opened`/`recheck` are unchecked. |
| F8 | C2 tree count | MEDIUM | (same as F4, tree side) |
| F9 | C2 drift reason | LOW | Any non-zero exit satisfies the drift arm; the named `report_file` drift is not required. |
| F10 | C2 `tree` symlink | control | Symlinked copy is correctly detected (`tree=bad`). |

**Cross-cutting note.** F1, F2, F3 and F7 are *predicate-width* findings:
the frozen counters prove less than the frozen contract sentences claim
("exact key/name/pointer binding"; "the registry rows those claims cite
… one per cited artifact copy"; "rows opened this round"). F6, F8 and F9
are *counter-implementation* findings: a reason the counter computes is
computed but not acted on, or a count the contract names is not asserted.
The kill rule (frozen bytes/predicate/target) is intact — every counter and
contract byte equals the freeze — so these are findings about the frozen
artefacts, not post-freeze drift.

## 9. Status of the two frozen claims

### 9a. At the freeze revision and at lane HEAD `8ff344ff` (first read)

- **C1 = met** at `60b3a76` and at `8ff344ff` — the frozen target string
  is reproduced exactly, rc=0, and every hostile fixture fails for its
  frozen reason. The counter is byte-frozen and reproducible.
- **C2 = unmet** at both — the tool, selftest, scan, drift and trees arms
  were green, but `corpus/knowledge/wave-settlement-artifacts-r59.md`, the
  six `corpus/evidence/sources-r59/` copies and their registry rows did not
  exist yet at any lane revision. The entry arm is reachable (F7 probe
  reaches `C2=met claims=12 files=6`), so C2 was data-blocked, not
  structurally blocked.

### 9b. After the mid-wave landing — re-verified at HEAD `08127c99`

The C2 data landed while this seat was working
(`be737211` "land C2 data", `7b86704d` "data correction — K11 demoted to
prose", `bf6c0ad3` "integrate w1", `08127c99` "orchestrator dispatched
marker"). Re-ran everything at the new tip:

```
$ git show HEAD:tools/mori-register-check.py | sha256sum
38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8  -   (== frozen PIN)
$ git show HEAD:tools/mori-settlement-scan.py | sha256sum
4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9  -   (== frozen PIN)

$ python3 tools/mori-register-check.py --selftest --scratch $S/st-r2
REGCHECK_SELFTEST pass=12 fail=0    rc=0
$ python3 tools/mori-settlement-scan.py --selftest --scratch $S/st-s2
SETSCAN_SELFTEST pass=10 fail=0     rc=0

$ python3 .ufo/waves/round-59/count-c1.py --selftest
C1_SELFTEST pass=6 fail=0           rc=0
$ python3 .ufo/waves/round-59/count-c2.py --selftest
C2_SELFTEST pass=9 fail=0           rc=0

$ python3 .ufo/waves/round-59/count-c1.py 08127c99... --scratch $S/f-c1
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=08127c99c2f28115a4e7bd3bb28f24593bdfd483
rc=0
$ python3 .ufo/waves/round-59/count-c2.py 08127c99... --scratch $S/f-c2
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=08127c99c2f28115a4e7bd3bb28f24593bdfd483
rc=0
```

Counter and contract bytes are still byte-identical to the freeze
(`count-c1.py` `2be6fda8…`, `count-c2.py` `2df3ae84…`, `contract.md`
`427fca0b…`) — the kill rule holds.

**Landed data, independently checked** (not via the counter): the entry
`corpus/knowledge/wave-settlement-artifacts-r59.md` is 6084 bytes, has the
four frontmatter keys in its first ten lines, **13** claim lines over
**6** distinct frozen `ARTIFACTS` copies, and `eval_entry()` on the
materialized landed tree returns `ok=True, reasons=[], stats={'claims': 13,
'files': 6}`. The registry carries `S553`–`S559`, each an 11-cell row with
`status=mined` and `used-by` exactly
`corpus/knowledge/wave-settlement-artifacts-r59.md`; `S560` is the
round-58 reconciliation row for the duplicate `S552` DOI (contract §routed
defect 2) with `status=rejected`, `used-by=corpus/lessons/round-59.md`.

### 9c. F6 and F7 re-confirmed against the **landed** data (not just a synthetic probe)

Both headline findings were re-run on a scratch clone of the *landed* HEAD,
so they are not artifacts of my probe generator:

**F6 (grammar tolerance) on the landed entry** — append one malformed
claim-shaped line (quote spanning a newline, so it cannot match the
`CLAIM` regex) to the real landed entry:
```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=aee6642e52a4deb20b8eb7290d097abf4a58bb6c
rc=0
```
The malformed line is invisible to the `entry` arm on real data.

**F7 (per-copy S-row binding) on the landed data** — delete the
`source: S558` head line *and* the `S558` registry row from the landed
entry, leaving the claims still citing
`corpus/evidence/sources-r59/w1-settlement-r58.json`:
```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=fc7ee2eb3ae63681b77f49cf45b2aa4223e928c0
rc=0
```
A cited artifact copy with **no** registry row at all still scores C2=met.
The counter *does* catch a row that is declared but missing
(`rows=bad` when only the `S559` row is deleted, rev `6b4a7c47`) — it
checks the ids it harvested, but never the reverse direction (every cited
copy must have a row).

**Final status: C1 = met and C2 = met at HEAD `08127c99`, both rc=0, both
byte-frozen, both reproducible.** The findings above are properties of the
*frozen counters themselves*, not of the landing: they are gaps in what the
frozen arms prove relative to the frozen contract sentences, and they would
permit a later revision to keep a `met` verdict while the underlying
binding degrades.

## 10. Risks / blockers

- No blocker for this seat's item. Both claims are `met` at HEAD
  `08127c99` (§9b).
- **F7 is the finding with the most forward risk.** Because the counter
  checks only the S-ids it harvests from the entry's first ten lines, a
  later revision can drop a registry row for a still-cited artifact copy
  and keep the `met` verdict (§9c). The landed data is currently *correct*
  on this axis — `S553`–`S559` are seven 11-cell `mined` rows, one per
  cited copy, each with `used-by` exactly the entry — but the counter does
  not enforce that correspondence, so a future revision can regress
  silently.
- **F6 is the finding with the widest blast radius.** Any future entry
  carrying a malformed claim-shaped line (a quote containing a newline, a
  missing pin, a doubled comma) is scored `entry=ok` on the real data,
  while the *same* defect is caught in hostile tree `t12-malformed-claim`.
  The two arms disagree about the same input class.
- **F1/F2/F3 mean the C1 register's prose is unpoliced.** The landed
  register happens to spell the capability names in full
  (`dual-shape seat-output vote binding`,
  `strict per-event driver-liveness probe`) and to point at the round-56
  artifacts, but the counter would accept `dual` / `strict`, nonsense
  descriptions, or `README.md` as evidence. If a later revision shortens
  the names or repoints the evidence, the counter still reports `met` and
  the register sentence has silently degraded.
- **F4/F8 mean the hostile batteries are self-limiting.** The 13 fixtures
  and 12 trees are only checked while present; deleting one keeps the arm
  green. The committed batteries are currently complete (13 and 12,
  verified in §3/§4), so this is a guard-rail gap rather than a live
  defect — but a future revision that drops a fixture or tree loses the
  corresponding coverage without the counter noticing.

## 11. Tooling

No package installed or updated; no `pacman` transaction (paused
host-wide, not invoked). No remote script fetched. Disk guard checked
before heavy work — green (`/fast/scratch/hyaku` 592.6G free, 27% use;
`/tmp` 122.2G free); no ENOSPC.

## 12. Cleanup

`/fast/scratch/hyaku/mori-r59/Mo59Executor40/` (tools, probe builder, the
two scratch clones with their probe branches, all counter scratch dirs) was
removed after the receipts above were captured. `TMPDIR` was pointed there
for every command. The lane working tree was not written to; the only lane
file created is this report.

Lane tree state at yield (other seats' in-flight work is included and was
not touched by me):

```
$ git status --porcelain
 M .ufo/waves/round-59/w1/Mo59MutationTester32.md
?? .ufo/waves/round-59/w1/Mo59Executor40.md
?? .ufo/waves/round-59/w1/Mo59MutationTester31.md
$ git rev-parse HEAD
08127c99c2f28115a4e7bd3bb28f24593bdfd483
```
