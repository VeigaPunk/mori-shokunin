# Mo60Sentinel43 — leakage audit (r60 evidence receipts + QUALITY 127 counters)

Seat: sentinel, read-only. No remediation, no VCS/corpus/SCORECARD writes.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

Pinned revisions (every re-derivation below names its revision; the lane tip
moved under this seat, so no unpinned working-tree read is used as evidence):

| role | revision |
|---|---|
| contract freeze | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| entering | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| lane tip observed during audit | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| r59 data revision (C1 receipts) | `7b86704d7c0754a09958d131b64dbfa2a6d3eaed` |

Instrument bytes are frozen across all three r60 revisions and the working
tree (so every run below is a run of the frozen instrument):

```
count-c1 795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae  (= PIN_C1 in count-c3)
count-c2 8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976  (= PIN_C2 in count-c3)
count-c3 fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514
tools/mori-entry-claims-check.py cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69  (= PIN_EC)
tools/mori-settlement-scan.py   4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9  (= PIN_SCAN)
```

## Verdict

The six claim-bearing r60 receipt classes (`c1-at-data`, `c2-at-freeze`,
`c3-at-freeze`, `control-c{1,2,3}-do-nothing`) and the two receipt-arm
receipts (`r59-c1-met`, `r59-c2-met`) contain **no scratch/TMPDIR path and no
host path**, and all of them reproduce **byte-for-byte on this host** from
committed bytes when run under a scratch dir whose name carries a probe token
(the token never appears in stdout/stderr). One committed r60 evidence file
does carry a host path (`census-start.txt:26`), and the C1 receipt arm is
silently bound to the host fleet path through a revision-pinned r59 default
(the r60 interface cannot override it). Both are findings, not claim
falsifications on this host.

## Findings

### F1 — `evidence/census-start.txt:26` embeds an absolute host path (medium, receipt portability)

```
$ git show b3c2561:.ufo/waves/round-60/evidence/census-start.txt | sed -n '26p' | od -c | head -2
0000000   m   o   r   i  \t   o   k  \t   /   h   o   m   e   /   v   g
0000020   p   n   k   /   P   r   o   j   e   c   t   s   /   s   h   o
```

Line 26 is `mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`.
The census tool prints the resolved registry path, so the receipt is
checkout-path dependent: run from the same host with a relative root it emits
`mori\tok\t./mori-shokunin/corpus/SOURCES.md` instead. Impact: this receipt
cannot reproduce byte-for-byte on any checkout whose path differs — the exact
property the seat contract states for receipt bytes. It is not read by any
r60 claim (no kill rule covers it), so no C1/C2/C3 target changes.

Related facts:
- `evidence/census-start.txt` is byte-identical to
  `round-59/evidence/census-start.txt` (`sha256
  8f69db481d48b873a327a2f6d9a046e5d041e25e0acd1870fadab88ff39fd9fa` both).
  A fresh run today at `b3c2561` (337 SOURCES rows, mid-wave) produces the
  same bytes, so the W04 warning set is genuinely stable; the identity is not
  evidence of a stale copy, but it does mean the receipt cannot distinguish
  rounds.
- The receipt records no command line and no `--root`, and it does not carry
  the `333 rows` figure the contract's Census paragraph asserts (SOURCES rows:
  333 at `7b86704d` and `ac496c7c`, 337 at `b3c2561`). That count is
  re-derivable from git, but not from the receipt.

Smallest remediation (report only): regenerate the census receipt with
registry paths relativized (or `--root .` from the lane parent) and a
`command:`/row-count header, as rounds 54/56 receipts already do.

### F2 — C1 receipts arm is bound to the host fleet path through the pinned r59 counter (medium-high, C1 portability)

`count-c1.py` re-runs the revision-pinned r59 counter with only `--repo` and
`--scratch`:

```
count-c1.py rerun_receipt() -> [sys.executable, str(tmp), R59_DATA, "--repo", <abs lane>, "--scratch", <out>]
```

The r59 counter defaults `fleet = "/home/vgpnk/Projects/shokunin"`
(`git show 7b86704d:.ufo/waves/round-59/count-c1.py:247`) and reads the fleet
MANIFEST from it (`:169` `mf = git_show(fleet, MANIFEST_REV, "MANIFEST.json")`,
`MANIFEST_REV = 2807c6ab…` at `:45`). r60 `count-c1.py` exposes no `--fleet`
flag (`grep -n fleet .ufo/waves/round-60/count-c1.py` → rc=1).

Reproduced:

```
# as r60 invokes it (default fleet)
$ python3 r59-c1.py 7b86704d… --repo <lane> --scratch <probe>
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d…
# identical to evidence/r59-c1-met.txt

# fleet relocated / absent — the "any checkout" case
$ python3 r59-c1.py 7b86704d… --repo <lane> --fleet /nonexistent-fleet-xyz --scratch <probe>
C1=unmet selftest=ok fixtures=ok real=bad pointers=bad rev=7b86704d… failed=manifest,real,pointers   (rc=1)
# same result with --fleet <lane repo> (wrong repo)
```

Impact: `r59-c1-met.txt` byte-equality holds only where the fleet repo sits at
the baked-in path. On a relocated fleet the C1 receipts arm drops to 0/2 and
`C1` becomes `unmet`; the r60 counter cannot be told where the fleet is.
`count-c1.py`'s docstring ("Read-only on the repo: git show / cat-file only")
also understates the scope — the re-run transitively reads a second repo at a
host-absolute default. `r59-c2-met.txt` has no such dependency (`r59 count-c2`
has no `fleet` reference; reproduced byte-identically with explicit `--repo`).

Smallest remediation (report only): pass `--fleet` (derived from `--repo`'s
parent, or a new r60 flag) when re-running the pinned r59 counter, or state the
fleet-path precondition next to the receipts arm.

### F3 — failure-branch path emission in `count-c3.py` (low, unreachable in met state)

`markers_under()` returns `str(p)` (absolute paths, `count-c3.py:130`); the G1
arm joins them into the `failed=` token:

```
179:        if not no_exec:
180:            failed.append("g1_new_executed:%s" % ",".join(
181:                markers_under(s_new)))
```

If the toolgate ever catches an execution, the counter's failure output embeds
the scratch absolute path, so that failure receipt would not be
checkout-portable (met-state output is clean — verified below). No committed
receipt depends on this branch.

### F4 — QUALITY 127 sweep: counters/tools clean; the wave-spec builder is not (info, scope)

Definitive grep over the three r60 counters (pattern
`(/home/|/Users/|X:\|/fast/|/var/tmp|/tmp|HYAKU_SCRATCH|$HOME|~/)`): rc=1, no
hit. Pinned tools: 0 hits each. `build-fixtures-r60.py`: 0 hits. All `--repo`
defaults are `.`; all temp dirs are `--scratch` or
`tempfile.mkdtemp(dir=os.environ.get("TMPDIR") or None)`.

Counting instruments (`tools/*.py|*.sh` containing `/home/vgpnk`) at
`ddfb12fb`, `ac496c7c`, `b3c2561`:

```
3  tools/mori-blind-check.sh
3  tools/mori-misroot-sweep.py
3  tools/mori-round17-context-check.py
```

— the same three at all three revisions; no r60 instrument adds one, which is
QUALITY 127's "a new instrument adds none" clause.

Not counters, but carrying absolute host paths (disclosed because the contract
says "no r60 instrument carries an absolute host path"):

| file | hits |
|---|---|
| `.ufo/waves/round-60/build-w1-spec.py` | 7 (`LANE`/`FLEET` at `:9-10`, embedded ticket text) |
| `.ufo/waves/round-60/w1-spec.json` (derived) | 50 |
| `.ufo/waves/round-60/w1-dispatch.json` (derived) | 50 |
| `.ufo/waves/round-60/contract.md` | 2 (prose census command) |
| `.ufo/waves/round-60/evidence/census-start.txt` | 1 (F1) |

The sentence is true for the counters and the two pinned tools; it is false
for the wave-spec builder/its JSON, which are dispatch artifacts rather than
measuring instruments. No run of the counters depends on them.

### F5 — lane-wide scope of path-bearing committed evidence (info)

```
$ git grep -lE '(/home/vgpnk|/fast/scratch|HYAKU_SCRATCH|TMPDIR=)' b3c2561 \
    -- ':(glob).ufo/waves/round-*/evidence/*' | wc -l
369
```

Round-60 contributes exactly 1 (`evidence/census-start.txt`, F1); the other
368 predate r60 and are unchanged at `ddfb12fb` (mostly census receipts and
control receipts that record their absolute command line). The nearest
preceding scratch-path receipt is `round-59/evidence/selftests.txt:1`
(`# selftests (TMPDIR=/fast/scratch/hyaku/mori-r59/L1)`); r60 has no
equivalent. Scope statement for QUALITY 127: r60 adds one host-path receipt
and zero scratch-path receipts.

## Positive evidence — receipt reproduction matrix

Every run used `--repo .` from the lane root, an explicit scratch dir whose
name contains `SENTINELMARKER43`, and `TMPDIR` set to it. `marker_hits` is the
probe token count in combined stdout/stderr (0 everywhere).

| receipt | command | rc | marker_hits | bytes |
|---|---|---|---|---|
| `c1-at-data.txt` (`b3c2561` after-state) | `count-c1.py b3c2561 --repo . --scratch <probe>` | 0 | 0 | **identical** |
| `c1-at-data.txt`, implicit scratch (`TMPDIR` only, no `--scratch`) | `count-c1.py b3c2561 --repo .` | 0 | 0 | **identical** |
| `c2-at-freeze.txt` | `count-c2.py ac496c7c --repo . --scratch <probe>` | 0 | 0 | **identical** |
| `c3-at-freeze.txt` | `count-c3.py ac496c7c --repo . --scratch <probe>` | 0 | 0 | **identical** |
| `control-c1-do-nothing.txt` | `count-c1.py ddfb12fb --repo . --scratch <probe>` | 1 | 0 | **identical** |
| `control-c2-do-nothing.txt` | `count-c2.py ddfb12fb --repo . --scratch <probe>` | 1 | 0 | **identical** |
| `control-c3-do-nothing.txt` | `count-c3.py ddfb12fb --repo . --scratch <probe>` | 1 | 0 | **identical** |
| `r59-c1-met.txt` (independent re-run at `7b86704d`, default fleet) | `r59-c1.py 7b86704d --repo <lane> --scratch <probe>` | 0 | 0 | **identical** |
| `r59-c2-met.txt` (independent re-run at `7b86704d`) | `r59-c2.py 7b86704d --repo <lane> --scratch <probe>` | 0 | 0 | **identical** |

Byte scan of the committed `evidence/` set at `b3c2561` (grep counts of the
QUALITY-127 pattern): 0 for every file except `census-start.txt:1`; all files
end with LF; `r59-absent-set.md`'s only non-ASCII bytes are three UTF-8 em
dashes (no control characters). Dead-rev (`000…0`) runs of all three counters
also emit no path token (`failed=` members are relative `.ufo/...` paths or
fixed tokens), so the failure shapes are path-free apart from F3.

Working-tree cleanliness after all runs: only the pre-existing untracked
`evidence/c1-at-data.txt` and `w1.ready*` markers; the counters themselves
remain byte-identical to `ac496c7c`/`b3c2561`.

## Method / limits

- Read-only: `git show`/`git cat-file`/`git grep`/`git ls-tree`; counters were
  executed with `--repo .` and scratch under
  `/fast/scratch/hyaku/mori-r60/Mo60Sentinel43/` (scratch removed before
  yield; no git writes in the lane, no fixture repos needed).
- Disk guard green before work: `/tmp` 14% used, `/fast/scratch/hyaku` 26%
  used, 600 GiB free.
- F2 is a portability/trust-boundary finding measured on this host; it does
  not show any wrong output here — on this host C1 receives `receipts=2/2`.
- Not in scope: seat reports, LOG/SCORECARD content, and the truth of the C1
  after-state itself (other seats own those).
