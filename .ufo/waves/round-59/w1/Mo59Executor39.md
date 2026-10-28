# Mo59Executor39 — executor findings (round 59, w1)

**Role**: executor. Ran the two frozen counters at the entering revision
`2b9f03975bfb6e508f35074ac8181ec8bf54e805` and at the freeze revision
`60b3a76ad0524c8978cc51922940be1c8c388915`, plus the frozen tools over their
hostile fixture/tree corpora, and probed both counters in throwaway scratch
clones.

**Headline outcome**: at the two assigned revisions — C1 `met` (exit 0) at
freeze, `unmet` (exit 1) at entering; C2 `unmet` (exit 1) at both, every tool
arm green and every data arm red. During the wave the builder landed the C2
data; I isolated the single remaining failure (one claim citing the r53 copy,
which the frozen `ARTIFACTS` map excludes), verified the fix in a sandbox
clone, and the builder applied it. **At lane HEAD `7b86704d` both frozen
claims measure met, exit 0** (§1 "Additional runs"). Six counter-design
findings (F2–F6) remain for the L1 to route forward; they are frozen-bytes
issues that cannot be repaired under this round's kill rule.

**Lane bounds honoured**: read-only on the lane. No commits, no VCS mutation, no
production-file edits, no writes to the fleet root or sibling repos. The only
file written is this report. All fixture work happened in throwaway clones under
`/fast/scratch/hyaku/mori-r59/Mo59Executor39/` with
`git rev-parse --show-toplevel` asserted to equal the clone path before every
mutation. Lane `HEAD` was `8ff344ff18924c1ea63d46c3b3969f9fea05bc51` before and
after every probe (verified at the end of each probe script).

**Tooling**: no installs, no upgrades. `pacman` was not run (host-wide pause).
Everything used was pre-existing (`python3`, `git`, `bash`). Nothing written to
any `PATH` directory.

**Disk guard**: `scripts/hyaku/disk-guard.sh status` was green before heavy work
(`/fast/scratch/hyaku` 27% used, 592.6G free) and re-checked green at the end.

---

## 1. Primary result — both counters, both revisions, full outputs and exit codes

Scratch: `TMPDIR=/fast/scratch/hyaku/mori-r59/Mo59Executor39`, `--scratch` passed
explicitly to every counter invocation.

### C1 — calibration

```
$ python3 .ufo/waves/round-59/count-c1.py 60b3a76ad0524c8978cc51922940be1c8c388915 \
      --scratch $TMPDIR/c1-freeze
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76ad0524c8978cc51922940be1c8c388915
EXIT=0
```

```
$ python3 .ufo/waves/round-59/count-c1.py 2b9f03975bfb6e508f35074ac8181ec8bf54e805 \
      --scratch $TMPDIR/c1-entering
C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f03975bfb6e508f35074ac8181ec8bf54e805 failed=tool_absent,selftest,fixtures_absent,real,pointers
EXIT=1
```

### C2 — depth

```
$ python3 .ufo/waves/round-59/count-c2.py 60b3a76ad0524c8978cc51922940be1c8c388915 \
      --scratch $TMPDIR/c2-freeze
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=60b3a76ad0524c8978cc51922940be1c8c388915 failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,copy_absent:corpus/evidence/sources-r59/w1-results-r55.json,copy_absent:corpus/evidence/sources-r59/w1-results-r56.json,copy_absent:corpus/evidence/sources-r59/w1-results-r57.json,copy_absent:corpus/evidence/sources-r59/w1-results-r58.json,copy_absent:corpus/evidence/sources-r59/w1-settlement-r58.json,entry_absent,tree
EXIT=1
```

```
$ python3 .ufo/waves/round-59/count-c2.py 2b9f03975bfb6e508f35074ac8181ec8bf54e805 \
      --scratch $TMPDIR/c2-entering
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=2b9f03975bfb6e508f35074ac8181ec8bf54e805 failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,copy_absent:corpus/evidence/sources-r59/w1-results-r55.json,copy_absent:corpus/evidence/sources-r59/w1-results-r56.json,copy_absent:corpus/evidence/sources-r59/w1-results-r57.json,copy_absent:corpus/evidence/sources-r59/w1-results-r58.json,copy_absent:corpus/evidence/sources-r59/w1-settlement-r58.json,entry_absent,tree
EXIT=1
```

### Additional runs taken after the builder landed the C2 data mid-wave

The builder committed `be7372114ded3075e5f5a15227ffec977df22f7d` while this
seat was running, so both counters were re-run at that revision:

```
$ python3 .ufo/waves/round-59/count-c2.py be7372114ded3075e5f5a15227ffec977df22f7d --scratch $TMPDIR/c2-head2
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=ok pins=ok tree=ok claims=14 files=7 rev=be7372114ded3075e5f5a15227ffec977df22f7d failed=entry
EXIT=1

$ python3 .ufo/waves/round-59/count-c1.py be7372114ded3075e5f5a15227ffec977df22f7d --scratch $TMPDIR/c1-head2
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=be7372114ded3075e5f5a15227ffec977df22f7d
EXIT=0
```

C2 was still unmet after the data landing, on one claim line — see **F1b**.
The builder then applied the fix I diagnosed (commit `7b86704d`), and both
counters were re-run there:

```
$ python3 .ufo/waves/round-59/count-c2.py 7b86704d7c0754a09958d131b64dbfa2a6d3eaed --scratch $TMPDIR/c2-head3
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=7b86704d7c0754a09958d131b64dbfa2a6d3eaed
EXIT=0

$ python3 .ufo/waves/round-59/count-c1.py 7b86704d7c0754a09958d131b64dbfa2a6d3eaed --scratch $TMPDIR/c1-head3
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d7c0754a09958d131b64dbfa2a6d3eaed
EXIT=0
```

**Both frozen claims are met at lane HEAD `7b86704d`.** The lane working tree
was clean of my activity throughout (`git status --porcelain` showed only wave
artifacts I did not create).

### Selftests

```
$ python3 .ufo/waves/round-59/count-c1.py --selftest
C1_SELFTEST pass=6 fail=0        EXIT=0
$ python3 .ufo/waves/round-59/count-c2.py --selftest
C2_SELFTEST pass=9 fail=0        EXIT=0
```

Both match the contract's frozen selftest expectations exactly
(`contract.md` C1/C2 Selftest lines). No-arg invocation exits 2 (setup) in both
counters, matching the documented `2 setup` code.

### Byte-identity of the frozen artifacts

The working-tree counter bytes are identical to the freeze revision, and both
are absent at the entering revision (empty blob hash `e3b0c442…`):

```
.ufo/waves/round-59/count-c1.py    freeze=2be6fda8c54633fd entering=e3b0c44298fc1c14 worktree=2be6fda8c54633fd
.ufo/waves/round-59/count-c2.py    freeze=2df3ae84f6d66f9e entering=e3b0c44298fc1c14 worktree=2df3ae84f6d66f9e
.ufo/waves/round-59/contract.md    freeze=427fca0bf2a92813 entering=e3b0c44298fc1c14 worktree=427fca0bf2a92813
```

Tool pins match the contract exactly:

```
tools/mori-register-check.py    sha256 38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8  (contract PIN ok)
tools/mori-settlement-scan.py   sha256 4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9  (contract PIN ok)
```

Tool selftests at the freeze revision:

```
REGCHECK_SELFTEST pass=12 fail=0   EXIT=0
SETSCAN_SELFTEST pass=10 fail=0    EXIT=0
```

**My measurements reproduce the L1's frozen evidence byte-for-byte.** The L1's
own receipts (`.ufo/waves/round-59/evidence/c1-at-freeze.txt`,
`c2-at-freeze.txt`, `control-c1-do-nothing.txt`, `control-c2-do-nothing.txt`,
`selftests.txt` at `HEAD`) carry exactly these five lines and exit codes. The
counter is deterministic: repeat runs with fresh scratch dirs produced identical
output (C1 met ×3, C2 unmet ×3, at freeze, entering and HEAD).

---

## 2. C1 real-arm, driven independently

Materializing `SCORECARD.md` from R and `MANIFEST.json` from fleet revision
`2807c6ab8a9b04dcf256682bcd722c695fdd6e14`, running the pinned tool directly:

```
pass1 rc=1 verdict=REGISTER_UNMET
pointers reported (4): tools/mori-vote-bind.py,
                        .ufo/waves/round-56/evidence/c2-at-landed.txt,
                        tools/mori-driver-liveness.py,
                        .ufo/waves/round-56/evidence/c1-at-landed.txt
  cat-file <each of the 4> exists=True
pass2 rc=0 verdict=REGISTER_MET
bound = {
  "rounds[832].capabilities_added[0]": "dual-shape seat-output vote binding (tools/mori-vote-bind.py, 16/16 selftest, r55 tally re-bound 78/78 while the frozen r55 counter reads voted=0 on the same bytes)",
  "rounds[832].capabilities_added[1]": "strict per-event driver-liveness probe over .ufo/watchdog.log (tools/mori-driver-liveness.py, 13/13 selftest, live receipt 1728 log lines / 0 malformed / 23 lanes)"
}
reasons=[]
```

Both bound names match the frozen `BOUND` prefixes in `count-c1.py:38-43`
(`dual-shape seat-output vote binding`, `strict per-event driver-liveness
probe`), and both are byte-equal to `rounds[832].capabilities_added[0]`/`[1]`
in the fleet `MANIFEST.json` at `2807c6ab…` (read directly, independent of the
counter). The two-phase design (learn pointers, materialize them from R, re-run)
is what turns `REGISTER_UNMET` into `REGISTER_MET` — pointer resolution is
genuinely load-bearing, not a stub.

---

## 3. All 13 C1 hostile fixtures — every one scores UNMET with a matching expect prefix

Driven directly with the pinned tool over each committed fixture tree at
`60b3a76a` (fixture `expect.txt`, `scorecard.md`, `manifest.json` and the
pointed-at files materialized from R):

| fixture | rc | expect | verdict | reasons (actual) |
|---|---|---|---|---|
| f01-stub-only | 1 | `binding` | REGISTER_UNMET | `binding:declared_register=0(capabilities_sections=1)`, `keys:missing=…[0]`, `keys:missing=…[1]` |
| f02-two-declared | 1 | `binding` | REGISTER_UNMET | `binding:declared_register=2(capabilities_sections=3)`, `keys:missing=…[0]`, `keys:missing=…[1]` |
| f03-dup-key | 1 | `keys` | REGISTER_UNMET | `keys:duplicate=rounds[832].capabilities_added[0]`, `manifest:name=…[0]` |
| f04-missing-key | 1 | `keys` | REGISTER_UNMET | `keys:missing=rounds[832].capabilities_added[1]` |
| f05-pointer-missing | 1 | `pointers` | REGISTER_UNMET | `pointers:missing=.ufo/waves/round-56/evidence/c2-at-landed.txt` |
| f06-pointer-absolute | 1 | `pointers` | REGISTER_UNMET | `pointers:bad=/etc/passwd` |
| f07-pointer-relative-parent | 1 | `pointers` | REGISTER_UNMET | `pointers:bad=../../etc/passwd` |
| f08-manifest-name-altered | 1 | `manifest:name` | REGISTER_UNMET | `manifest:name=rounds[832].capabilities_added[0]` |
| f09-manifest-substring-only | 1 | `manifest:name` | REGISTER_UNMET | `manifest:name=rounds[832].capabilities_added[0]` |
| f10-manifest-foreign-lane | 1 | `manifest:lane` | REGISTER_UNMET | `manifest:lane='kotoba'` ×2 |
| f11-manifest-wrong-index | 1 | `manifest` | REGISTER_UNMET | `manifest:lane=None`, `manifest:entry_missing=…[0]`, `manifest:lane_round=…[0]`, (…[1] likewise) |
| f12-lane-round-mismatch | 1 | `manifest:lane_round` | REGISTER_UNMET | `manifest:lane_round=…[0]`, `manifest:lane_round=…[1]` |
| f13-empty-pointer | 1 | `pointers` | REGISTER_UNMET | `pointers:none=rounds[832].capabilities_added[1]` |

13/13 UNMET, 13/13 expect prefixes covered. Fixture count at freeze = 13
(`git ls-tree --name-only 60b3a76a:.ufo/waves/round-59/fixtures-c1/`), matching
the contract.

---

## 4. All 12 C2 hostile trees — every one evaluates UNMET with a matching expect prefix

Evaluated with `count-c2.py`'s own `eval_entry` imported read-only, over each
committed tree at `60b3a76a`:

| tree | expect | got_ok | reason prefix matched | actual reason |
|---|---|---|---|---|
| t01-no-frontmatter | `frontmatter` | False | True | `frontmatter:source`, `frontmatter:verified-at`, `frontmatter:recheck`, `frontmatter:coverage-map`, `rows:no_source_ids` |
| t02-dup-k | `distinct` | False | True | `distinct:dup=K1` |
| t03-quote-wrong-line | `span` | False | True | `span:1` |
| t04-stale-pin | `pin` | False | True | `pin:1` |
| t05-few-claims | `claims_min` | False | True | `claims_min:7` |
| t06-outside-file | `files` | False | True | `files:outside=tools/mori-settlement-scan.py` |
| t07-no-row | `rows:missing` | False | True | `rows:missing=S901` |
| t08-extra-cell-row | `rows:bad_row` | False | True | `rows:bad_row=S901` |
| t09-usedby-other | `rows:usedby` | False | True | `rows:usedby=S901` |
| t10-queued-status | `rows:status` | False | True | `rows:status=S901` |
| t11-quote-short | `span` | False | True | `span:short=1` |
| t12-malformed-claim | `grammar` | False | True | `grammar:- **K5** — claim 5. Quote: \` "seats": 3,` |

12/12 UNMET, 12/12 expect prefixes covered. Tree count at freeze = 12, matching
the contract.

## 5. C2 scan arm, driven independently

```
REAL scan rc=0
  verdict=SETTLEMENT_SCAN_OK
    r54  seats=74 members=74 equal=True
    r55  seats=64 members=64 equal=True
    r56  seats=64 members=64 equal=True
    r57  seats=64 members=64 equal=True
    r58  seats=64 members=64 equal=True
DRIFT scan rc=1 (must be nonzero)
  verdict=SETTLEMENT_SCAN_FAIL
  drift file top-level keys: ['lane','note','outputs_recovered','results','round','seats','settled_by','spawned','wave']
```

The r54–r58 files scan OK with `members == seats` on every file; the r53 file
exits nonzero with `SETTLEMENT_SCAN_FAIL`. Both match the contract's scan/drift
arms. Note the drift file carries `report_file` — schema drift observed and
reported, not fixed, as the contract requires.

---

## 6. Findings

### F1 (material, wave-shaping) — C2 is UNMET at the freeze revision; the data arm has not landed yet

> **Update (post-builder commit `be737211`)**: the builder landed the C2 data
> mid-wave. C2 was re-run at that revision and is **still unmet** — for a
> single-line reason isolated in F1b below. The freeze-revision measurement
> below stands as the assigned measurement; F1b is the live blocker.

The frozen C2 target output in `contract.md` is
`C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=N files=F rev=R`
(N ≥ 10, F ≥ 3), exit 0. At the freeze revision the counter returns
**`C2=unmet`, exit 1**, with `selftest=ok scan=ok drift=ok trees=ok` — i.e. every
*tool* arm is green and every *data* arm is red:

```
failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,
       copy_absent:…-r55.json, copy_absent:…-r56.json, copy_absent:…-r57.json,
       copy_absent:…-r58.json, copy_absent:…/w1-settlement-r58.json,
       entry_absent, tree
```

Root cause, confirmed by tree inspection at `60b3a76a`: none of the six
`corpus/evidence/sources-r59/` copies and not
`corpus/knowledge/wave-settlement-artifacts-r59.md` are committed. The
`.ufo` artifacts the copies must mirror **are** all committed and byte-stable
at the freeze revision:

```
.ufo/waves/round-54/w1-results.json          ea48a0cc07fa948c…
.ufo/waves/round-55/w1-results.json          2e5b0a0f94d1fa5b…
.ufo/waves/round-56/w1-results.json          19536201a689c954…
.ufo/waves/round-57/w1-results.json          29e7a35df544315d…
.ufo/waves/round-58/w1-results.json          a57b660d9f41c55d…
.ufo/waves/round-58/evidence/w1-settlement.json b259e73cdddef7ff…
```

The lane working tree already carries untracked copies with **byte-identical
shas** to those artifacts (all seven files under `corpus/evidence/sources-r59/`
in the worktree, including an extra `w1-results-r53.json`), but the entry
`corpus/knowledge/wave-settlement-artifacts-r59.md` is still absent from the
worktree and no `S###` rows exist for it in `corpus/SOURCES.md` (325 rows at
freeze; latest `S552`). The C2 "after" arm is therefore **reachable but not yet
reached** — this is a build-sequencing fact, not a counter defect.

**Feasibility confirmed, not assumed.** I landed a synthetic-but-grammar-exact
data set in a throwaway clone (six copies byte-equal to their `.ufo` artifacts;
an entry with frontmatter `source:/verified-at:/recheck:/coverage-map:` and
claims in the frozen `- **K<n>** — … Quote: \`<q>\` (<file>:line:<n>; pin <sha64>)`
grammar; `SOURCES.md` rows with exactly 11 cells, `status=mined`,
`used-by=corpus/knowledge/wave-settlement-artifacts-r59.md`) and ran the frozen
counter against it:

```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=10 files=5 rev=eec37bbb…
EXIT=0
```

So the C2 after-arm is reachable by landing data — no counter change needed.

### F1b (material — RESOLVED mid-wave) — the builder's committed C2 data failed on exactly one claim line

The builder landed the C2 data in commit
`be7372114ded3075e5f5a15227ffec977df22f7d` ("round-59: land C2 data —
settlement-artifact depth entry, artifact copies, S553-S560 rows, quarantine
slice"). Re-running the frozen counter at that revision:

```
$ python3 .ufo/waves/round-59/count-c2.py be7372114ded3075e5f5a15227ffec977df22f7d --scratch $TMPDIR/c2-head2
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=ok pins=ok tree=ok claims=14 files=7 rev=be7372114ded3075e5f5a15227ffec977df22f7d failed=entry
EXIT=1

$ python3 .ufo/waves/round-59/count-c1.py be7372114ded3075e5f5a15227ffec977df22f7d --scratch $TMPDIR/c1-head2
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=be7372114ded3075e5f5a15227ffec977df22f7d
EXIT=0
```

`rows=ok`, `pins=ok`, `tree=ok` — every data arm now passes except `entry`.
The single reason, isolated by running the counter's own `eval_entry` over the
builder's tree:

```
eval_entry ok=False claims=14 files=7
reasons: ['files:outside=corpus/evidence/sources-r59/w1-results-r53.json']
```

**Cause**: claim **K11** cites the round-53 copy.

```
- **K11** — the round-53 artifact's member entries carry a report_file field — a key absent from r54-r58 members. Quote: `   "report_file": ".ufo/waves/round-53/w1/Mo53Fr01.md"` (corpus/evidence/sources-r59/w1-results-r53.json:line:16; pin 0d644e0fb9c50101…)
```

The frozen counter's `ARTIFACTS` map (`count-c2.py:66-79`) contains exactly six
copies — r54, r55, r56, r57, r58 results and the r58 settlement — and
`eval_entry` rejects any cited file outside that set
(`if f not in ARTIFACTS: reasons.append("files:outside=%s" % f)`,
`count-c2.py:136-138`). **r53 is deliberately excluded**: it is the DRIFT file
(`DRIFT_SCAN = [".ufo/waves/round-53/w1-results.json"]`), the one artifact the
contract requires to *fail* the scan. A claim may cite it as a copy but the
counter's artifact set excludes it. The claim is substantively sound (r53's
members really do carry `report_file`, which r54–r58 do not — a genuine shape
fact) but it is **unciteable** under the frozen predicate.

Everything else the builder landed is correct:
- all six in-set copies are byte-equal to their `.ufo` artifacts (`tree=ok`,
  independently re-verified: `equal=True` for all six);
- `rows=ok` — S553–S559 each have exactly 11 cells, `status=mined`,
  `used-by=corpus/knowledge/wave-settlement-artifacts-r59.md`;
- `pins=ok` — every claim's pin equals its copy's sha256 at the revision;
- 13 other claims parse, K-ids distinct, frontmatter four keys present in the
  first ten lines.

**Minimal fix, verified end-to-end in a throwaway clone** (lane untouched):
delete **only** the single K11 claim line from
`corpus/knowledge/wave-settlement-artifacts-r59.md` — keeping the `S559`
frontmatter source line and keeping `w1-results-r53.json` on disk:

```
removed 1 line(s) (K11 claim only)
S559 frontmatter kept: True
r53 copy still on disk: True
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=53fdf4b1…
EXIT=0
```

Dropping the r53 copy file instead does not help (the claim still cites it);
dropping both the K11 line and the S559 frontmatter line also works
(`claims=13 files=6`, `C2=met`) but is unnecessary — S559's registry row is
valid and harmless. **The one-line deletion of the K11 claim is the whole fix**;
13 claims over 6 files still clears the `MIN_CLAIMS=10` / `MIN_FILES=3`
floors. The r53 `report_file` observation can be preserved as prose in the
entry body (a non-claim line) or as a claim over an in-set artifact.

**RESOLUTION.** The builder applied exactly this fix in commit
`7b86704d7c0754a09958d131b64dbfa2a6d3eaed` ("round-59: data correction — K11
demoted to prose (r53 copy outside frozen ARTIFACTS)"). Re-running both
frozen counters at that revision:

```
$ python3 .ufo/waves/round-59/count-c2.py 7b86704d7c0754a09958d131b64dbfa2a6d3eaed --scratch $TMPDIR/c2-head3
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=7b86704d7c0754a09958d131b64dbfa2a6d3eaed
EXIT=0

$ python3 .ufo/waves/round-59/count-c1.py 7b86704d7c0754a09958d131b64dbfa2a6d3eaed --scratch $TMPDIR/c1-head3
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d7c0754a09958d131b64dbfa2a6d3eaed
EXIT=0
```

**Both claims are now met at lane HEAD.** The K11 observation survives as
prose (entry line 43: "K11's absence claim is bounded to r54–r58 first"), the
`w1-results-r53.json` copy stays on disk, and the S559 registry row is
untouched. `claims=13 files=6` clears the frozen floors (≥10 claims, ≥3 files)
with margin. The counter and contract bytes were not touched — the fix was
purely in the data the counter measures.

### F2 (material) — the counters do not pin the hostile-corpus counts the contract claims

`contract.md` claims "13 committed trees under `.ufo/waves/round-59/fixtures-c1/`"
and "12 committed trees under `.ufo/waves/round-59/trees-c2/`". The counters
enumerate whatever directories exist and require only that each one evaluates
correctly; they never assert the *count*. Probed in scratch clones:

```
Q1: drop f13-empty-pointer  -> 12 fixtures
    C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=8682b989…   rc=0   <-- still MET
Q2/P4: drop t12-malformed-claim -> 11 trees
    C2=… trees=ok …                                                   <-- trees token still ok
P3: duplicate f01 as f14-dup-of-f01 -> 14 fixtures
    C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=c4222c7b…   rc=0
```

Dropping a hostile fixture or tree, or padding the corpus with duplicates,
keeps the claim green. Coverage is therefore a convention, not a counter-
enforced property.

### F3 (material) — a fixture's frozen `expect.txt` prefix is not pinned against the counter, and an empty expect is vacuous

The counter reads each fixture's `expect.txt` at R and checks that some emitted
reason starts with each comma-separated prefix. The expectation text lives in
the same tree the counter is measuring, so it can be retargeted:

```
P1: f01 expect.txt  binding  ->  keys
    C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=fa4aec6a…   rc=0
P5: f03 expect.txt  keys     ->  (empty file)
    C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=1a24729a…   rc=0
```

With an empty `expect.txt`, `expect` splits to `[""]`, and
`r.startswith("")` is true for any reason string — the check degenerates to
vacuous truth, so the fixture passes as long as the tool merely fails. A
stronger check would pin each fixture's expected prefix (and the count) inside
the frozen counter rather than inside the fixture tree. Note that the counter
*does* catch the converse direction: gutting a fixture's `scorecard.md` so the
construction no longer fails is caught (P2 →
`failed=fixture:f05-pointer-missing`), and altering a prefix to one the tool
does not emit is caught (Q3 → `failed=fixture:f01-stub-only`). The hole is
specifically that the *expectation* is attacker-adjacent, not that the
construction is unchecked.

### F4 (material) — a `.py`-suffixed fixture directory is silently skipped

`count-c1.py:132` filters the fixture listing with
`dirs = [n for n in names if not n.endswith(".py")]`. A fixture directory
renamed to end in `.py` is dropped from evaluation without any failure:

```
R2: git mv f13-empty-pointer -> f14-empty.py   (13 dirs still present)
    C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=1b3c7964…   rc=0
```

The directory count is unchanged at 13 yet one fixture is never evaluated.
This is a live coverage hole that a hostile fixture author could use to
neutralize a fixture without touching the counter. `count-c2.py` has no such
filter on `TREES`.

### F5 (material, scope-falsifying) — the C2 "≥10 distinct claims" requirement does not require distinct claims

`count-c2.py` requires ≥10 parsed claims (`MIN_CLAIMS`) and ≥3 distinct cited
files (`MIN_FILES`), and enforces that K-ids are distinct
(`distinct:dup=K<n>`). It does **not** require the *quote content* to be
distinct, nor that the claim prose says anything. Sandbox probe: 12 claims over
3 copies, every claim carrying the **same** quote text and the tautological
prose "seats equals members", each with its own correct pin:

```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=12 files=3 rev=532621c6…
EXIT=0
distinct quote texts used: 1
```

The contract's C2 predicate says "≥10 byte-exact pin-bound claims over ≥3
distinct artifacts" and the routed-defect list item 4 requires "distinct
claims" — the counter enforces distinct *K-ids* only. An entry whose ten claims
are the same sentence about the same line of the same three files satisfies the
frozen predicate. This is exactly the "cheapest entry that scores met without
real claims" falsification the round asked for; it succeeds.

### F6 (material) — the C2 registry binding is one-S-id-per-entry, not one-per-cited-copy

`contract.md` (C2 sourced-claim rule) requires "one [S### row] per cited
artifact copy". `eval_entry` extracts S-ids from the entry's first ten lines
(`SID` regex over `head`) and validates each against the registry, but never
cross-checks the number of cited copies against the number of declared S-ids.
Sandbox probe: 11 claims over **6** distinct copies with a **single** declared
S-id in the frontmatter and a single matching registry row:

```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=11 files=6 rev=d297e926…
EXIT=0
```

Six artifacts cited, one registry row. The contract's "one per cited artifact
copy" rule is not enforced by the frozen counter.

### F7 (informational) — dead code in the frozen counters

`count-c1.py:155-157` computes `got = {…}` from the tool's reasons and never
uses it; the fixture check uses `reasons` directly. Harmless but dead. Also
`count-c1.py:154` builds `got` with a dict comprehension whose `":" in r`
branch is unreachable for the reason strings the tool actually emits.

### F8 (informational) — `TMPDIR` is honoured when `--scratch` is omitted

With `TMPDIR` set and no `--scratch`, the counters create their scratch dirs
under `TMPDIR` (`mori-r59-c1-hjlju7qg`, `mori-r59-c2-_7hhk9_k` appeared under
the probe dir). Matches the counters' documented behaviour.

### F9 (informational) — C1 is stable across the freeze→HEAD range

C1 was `met` at freeze `60b3a76a`, at `8ff344ff`, at `be737211` and at
`7b86704d` — four independent runs, all `met`, exit 0. The intervening commits
(`8ff344ff` dispatch payload, `be737211` C2 data landing, `7b86704d` K11 data
correction) touch only C2 data and never the C1 tool, fixtures or contract.

### F10 (informational) — the round-59 census is green after the data landing

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
exits 0 at the builder's commit, reporting `mori ok …/corpus/SOURCES.md`. The
new rows S553–S560 (including the REJECTED duplicate row S560) raise the
registry count from 325 to 333 and produce no new census warnings.

---

## 7. What the wave should do about F1/F1b — RESOLVED

**F1b is resolved.** The builder applied the diagnosed one-line fix (K11
demoted from a claim to prose) in commit `7b86704d`, and the frozen counters
now report **both claims met** at lane HEAD:

```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=7b86704d…   EXIT=0
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d…                                                 EXIT=0
```

No further action is needed on the data side.

For the record, the landing recipe that worked — all confirmed reachable in a
sandbox clone before the builder landed it (§6 F1):

1. Commit the six `corpus/evidence/sources-r59/` copies **byte-equal** to their
   `.ufo` artifacts at the target revision. The shas are listed in §6 F1; the
   lane worktree already holds byte-identical copies.
2. Commit `corpus/knowledge/wave-settlement-artifacts-r59.md` with the four
   frontmatter keys inside the first ten lines, ≥10 claims in the frozen
   grammar, distinct K-ids, ≥3 distinct cited copies, and each quote
   byte-equal to the cited line/offset span with the copy's own sha256 as pin.
3. Append the S### rows to `corpus/SOURCES.md` — exactly 11 cells, `status`
   cell `mined`, `used-by` cell exactly
   `corpus/knowledge/wave-settlement-artifacts-r59.md`. One row per cited copy
   satisfies the contract even though the counter does not enforce it (F6).

F2–F6 are counter-design findings for the L1/attacker seats. They are frozen
counter bytes, so under the kill rule they cannot be repaired inside this round
— they should be routed as round-60 work or carried as residual risk.

---

## 8. Retained evidence index

All artefacts are under `/fast/scratch/hyaku/mori-r59/Mo59Executor39/`
(cleaned before yield; contents listed for audit):

- `drive-c1-fixtures.sh` → the 13-fixture driver of §3
- `drive-c2-trees.py` → the 12-tree driver of §4
- `drive-c2-scan.py` → the scan/drift driver of §5
- `drive-c1-real.py` → the real-arm driver of §2
- `probe-sandbox.sh` → Q1–Q3 (§6 F2, F3)
- `probe-weaken.sh` → P1–P4 (§6 F2, F3)
- `probe-blank-expect.sh` → P5/P6 (§6 F3)
- `probe-c2-after.py` → the C2 after-arm feasibility clone (§6 F1)
- `probe-c2-degenerate.py` → the degenerate-entry clone (§6 F5)
- `probe-c2-srows.py` → the one-S-row clone (§6 F6)
- `probe-f05-repoint.sh` → the `.py`-suffix and re-point probes (§6 F4)
- `probe-tmpdir.sh` → the TMPDIR/pin-candidate probe (§6 F8)
- `probe-c2-builder.py` → the frozen counter run over the builder's landed data (§6 F1b)
- `diag-builder-entry.py` → the entry line-by-line diagnosis isolating the r53 claim (§6 F1b)
- `diag-builder-copies.py` → copy byte-equality + registry-row audit (§6 F1b)
- `probe-c2-builder-fix.py` → the drop-K11-and-S559 and drop-r53-copy variants (§6 F1b)
- `probe-c2-minimal-fix.py` → the minimal one-line K11-only deletion, verified `C2=met` (§6 F1b)
- `sandbox/`, `sandbox2/`, `sandbox3/`, `sandbox4/`, `sandbox-c2/`,
  `sandbox-c2b/`, `sandbox-c2c/`, `sandbox-builder/`, `sandbox-builder2/`,
  `sandbox-builder4/` — throwaway clones, each asserted to be its own toplevel
  before any mutation

The five primary counter outputs and exit codes are quoted verbatim in §1; the
two post-builder-commit runs are in §1's "Additional runs" subsection.

## 9. Blockers / risks

- **No blockers** for the assigned executor task; both counters ran at both
  assigned revisions with full output and exit codes captured, and again at the
  builder's two commits.
- **F1b is RESOLVED**: after the builder's data landing, C2 failed on exactly
  one claim line (K11 citing the r53 copy, which the frozen `ARTIFACTS` map
  excludes because r53 is the DRIFT file). I isolated the cause, verified the
  one-line fix end-to-end in a throwaway clone, and reported it; the builder
  applied it in commit `7b86704d`. **Both frozen claims now measure met at
  lane HEAD** (§1 "Additional runs").
- **Census is green**: `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin mori` exits 0 after the builder's commit, with
  `mori ok …/corpus/SOURCES.md`. No new S553–S560 warnings.
- **F2–F6 are frozen-bytes findings** and cannot be fixed under the round-59
  kill rule. They should be routed forward rather than patched in place. F4
  (`.py`-suffixed fixture dirs skipped) and F5 (distinct-claims requirement
  not enforced) are the two with the largest residual coverage risk.
- No remediation, no provider inference, no axis-harm judgement was attempted;
  this seat only measured. I did not edit the entry, the registry, the
  contracts, the counters, SCORECARD, or LOG.
