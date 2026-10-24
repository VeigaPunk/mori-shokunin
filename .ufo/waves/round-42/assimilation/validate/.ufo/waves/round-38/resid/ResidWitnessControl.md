# ResidWitnessControl — round 38 residual falsification (witness sandbox control + one passing fabrication)

Seat: `mori-r38.ResidWitnessControl`. Detection and report only; no remediation, no edits to committed
bytes, no commits in the lane repo. All counters were run over committed bytes (`git show <rev>:<path>`);
this seat mutated nothing in the lane except this report file (other seats' concurrent working-tree
edits are not mine).

## Headline

1. **The assigned control reproduces.** At tip `b6993744` the round-37 token counter prints `C2=met`
   exit 0 on the fabricated-witness clone, and `count-c4.py` prints `C4=unmet` exit 1 with all three
   named witnesses `rejected` (section 2). Both counters match their freeze pins.
2. **FINDING R1 (HIGH) — one fabrication passes `count-c4.py`.** A stub knowledge entry (three
   `anchor:` lines copied verbatim from the tool, no claim, no rows, no commit), a capability row
   rewritten to cite the counter instead of the receipt, and an invented self-consistent live receipt
   (`drifted=1`, `S103 drifted` — the real receipt says `S103 no-copy`, `drifted=10`) print
   **`C4=met` exit 0** (section 3, commit `2ac814ee`). Only the tool half (`named_row_drift`,
   `drift_kill`) is load-bearing; the three "content" checks are resolution/self-consistency checks that
   imitation satisfies. P-C4 as frozen is *literally* satisfied by the fabrication — the falsification
   is against the claim that `C4=met` discriminates content from imitation.
3. **FINDING R2 (MEDIUM) — the witness sandbox does not isolate each witness**, contrary to
   `contract.md`'s "the witness sandbox is the control that isolates each witness". On the sandbox rev
   every negative's rejection is confounded by the other two fabricated files; isolation holds only when
   each witness is projected onto the real tip bytes (section 4).
4. **FINDING R3 (LOW) — the committed C4 receipts predate the pinned v3 counter**: both
   `evidence/c4-after.txt` and `evidence/c4-witness.txt` carry an earlier `count-c4.py` detail format
   (no `empty=`/`unique=`) and were measured at pre-tip revs (`f725f307`, sandbox `d2ee0532` built on
   it), not at the tip `b6993744` with the frozen v3 instrument. Verdicts are unchanged; the receipt of
   record is not reproducible from the pinned bytes at the scored tip (section 5).
5. **FINDING R4 (LOW) — the assignment's counter path is the round-36 counter.** The round-37 token
   counter is `.ufo/waves/round-37/count-c2.py`; `.ufo/waves/round-36/count-c2.py` counts a different
   predicate (append-only gate) and never reads the witnesses. The literal command as written also
   exits 2, because a `--shared` clone's commit is not resolvable in the lane repo (section 2.1).

## 1. Tip and sandbox

- Tip: `git -C …/mori-shokunin rev-parse HEAD` → `b6993744171a05efc627b5e0664489c31aa5214e`.
  The assignment's `rev-parse mori` fails (`fatal: ambiguous argument 'mori'`; there is no `mori` ref —
  HEAD is detached at the cited commit). Verified independently with `git cat-file -t`.
- Instrument pins at the tip (sha256, equal to `evidence/freeze-r38-v3.txt` and
  `evidence/freeze-r37-v3.txt`):
  - `count-c4.py` `8332341c3901ef09e76bbd7f31e8c8e68b4e4ecc5d3002f2d20201c9e7093ba1`
  - `round-37/count-c2.py` `f173a642ac671c2b47f6c11ec1b76a3874e7d12fd1810e25875f0ee3dd7f447e`
  - `fixtures/make-witness-sandbox.py` `1128524c33511b9b133de02ae2feab1b34767ad689e43acf85cfd35bb2d70259`
- Sandbox build (default `--out` avoided so the lane tree stays clean; clone is `git clone --shared`):

```
python3 .ufo/waves/round-38/fixtures/make-witness-sandbox.py \
  b6993744171a05efc627b5e0664489c31aa5214e --out /tmp/r38-witness-control
→ d8c005ebe54abf9e5e4568121cc18531616f3144   (exit 0)
git -C /tmp/r38-witness-control diff --stat <tip> d8c005e
→ .ufo/waves/round-37/evidence/drift-live-r37.txt | 226 ---
  SCORECARD.md                                    | 2189 +----------------------
  corpus/knowledge/source-drift-hardening-r37.md  |  92 +-
  3 files changed, 5 insertions(+), 2502 deletions(-)
```

Only the three fixture substitutions differ from the tip; the tool, SOURCES.md, README and the
round-38 `source-drift-content-anchor-r38.md` entry are the real committed bytes.

## 2. Control (a)+(b): token counter accepts, C4 rejects

### 2.1 The command as assigned does not run

```
python3 .ufo/waves/round-36/count-c2.py d8c005ebe54abf9e5e4568121cc18531616f3144   (from the lane)
→ counter setup error: git rev-parse --verify …^{commit} failed in <lane>: fatal: Needed a single revision
→ EXIT=2
```

The clone borrows objects from the lane but its own commit is not in the lane, and every counter
defaults `--repo` to the lane. The counter also has a different predicate: P-C2 of round 36 counts
`tools/mori-sources-appendonly.py` and never reads the three witnesses.

For completeness, that round-36 counter on the sandbox with `--repo`:

```
python3 .ufo/waves/round-36/count-c2.py d8c005e --repo /tmp/r38-witness-control
→ blind arm 24/24; real arm pass; C2=met; EXIT=0
```

`C2=met exit 0` is reproduced, but **vacuously**: it is the round-36 gate passing on the unchanged
append-only tool; it says nothing about the fabricated witnesses. This should not be cited as token
acceptance.

### 2.2 The round-37 token counter accepts the fabrication (the real (a))

```
python3 .ufo/waves/round-37/count-c2.py d8c005e --repo /tmp/r38-witness-control
→ tool_present PASS · selftest PASS (6 arms) · cap_kill PASS · redirect_kill PASS
  knowledge PASS (present=True rows=['S221'] cited_commit=True touches_tool=True)
  capability PASS (rows=1 names_tool=True) · readme PASS · live PASS (present=True sentence=True)
→ C2=met ; EXIT=0
```

The knowledge check is satisfied by `witness-token-entry.md` (tokens `huge_cap`,
`redirect_private_refused`, `1caa242`, one `S2\d\d` id `S221`); the capability check by
`witness-dangling-row.md` (the row names `tools/mori-source-drift.py`, which exists); the live check by
`witness-summary-only-live.txt` (the summary sentence without rows). Same eight PASS lines and
`C2=met` as the committed `evidence/v3-token-control.txt` (that receipt used the `f725f307`-based
sandbox `d2ee0532`; my sandbox is built from the tip).

### 2.3 The round-38 counter rejects the fabrication (b)

```
python3 .ufo/waves/round-38/count-c4.py d8c005e --repo /tmp/r38-witness-control
→ negative witness-token-entry        rejected
  negative witness-dangling-row       rejected
  negative witness-summary-only-live  rejected
  check anchors          PASS (anchors=3 missing=[] empty=0 unique=True)
  check capability       FAIL (paths=['tools/mori-source-drift.py', 'evidence/no-such-receipt.txt']
                                missing=['evidence/no-such-receipt.txt'])
  check live_rows        FAIL (named=0 summary_drifted=10 unknown=[] unique=True)
  check named_row_drift  PASS · drift_kill PASS
→ C4=unmet ; EXIT=1
```

`anchors` passes because the fixture replaces the **round-37** knowledge entry
(`source-drift-hardening-r37.md`), while C4's entry is the untouched round-38
`source-drift-content-anchor-r38.md`. The two failing checks are the intended ones. On the real tip
(`b6993744`, `--repo <lane>`) the counter prints `C4=met` exit 0 with the same check verdicts as the
committed `evidence/c4-after.txt`; the detail strings differ because the committed receipt predates the
pinned v3 counter (R3, section 5).

## 3. FINDING R1 (HIGH): one fabricated binding prints `C4=met` exit 0

### 3.1 Construction (single commit on a fresh `--shared` clone of the tip)

Clone `/tmp/r38-fabrication` at `b6993744`; commit `2ac814eebd6b8965f510c8dc961e9e23e47f4bf7`
("fabricated content binding: copied anchors, rewritten capability path, invented live receipt"):

| path | fabricated content |
|---|---|
| `corpus/knowledge/source-drift-content-anchor-r38.md` | 61-line real entry → 7-line stub: a sentence saying it makes no claim, then three `anchor:` lines copied verbatim from the tool (`FETCH_MAX_BYTES = 4 * 1024 * 1024`, `if not _public_redirect_target(final):`, `return "drifted"`). No source rows, no round, no commit, no reasoning. |
| `SCORECARD.md` (capability row) | evidence cell rewritten from `tools/mori-source-drift.py`; `.ufo/waves/round-37/evidence/c2-after-v3.txt`; `.ufo/waves/round-37/evidence/drift-live-r37.txt` to `tools/mori-source-drift.py`; `.ufo/waves/round-38/count-c4.py` — the row now points at the counter, not at any receipt. |
| `.ufo/waves/round-37/evidence/drift-live-r37.txt` | 230-line live sweep → two lines: `MORI_SOURCE_DRIFT rows=225 fresh=214 excerpt=0 drifted=1 unavailable=0 no-copy=10` and `S103 drifted`. The committed receipt of record says `S103 no-copy`, `drifted=10`, `fresh=53`, `no-copy=162`. |

The tool is untouched real bytes (both selftest arms run the committed tool).

### 3.2 Result

```
python3 .ufo/waves/round-38/count-c4.py 2ac814ee --repo /tmp/r38-fabrication
→ negative witness-token-entry        rejected
  negative witness-dangling-row       rejected
  negative witness-summary-only-live  rejected
  check anchors          PASS (anchors=3 missing=[] empty=0 unique=True)
  check capability       PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-38/count-c4.py']
                                missing=[])
  check live_rows        PASS (named=1 summary_drifted=1 unknown=[] unique=True)
  check named_row_drift  PASS · drift_kill PASS
→ C4=met ; EXIT=0
```

### 3.3 Why each check passes, and what it actually verifies

- `anchors` (`count-c4.py:180`) is substring membership plus count/uniqueness. It cannot tell a
  7-line stub from the 61-line entry; copying three strings that occur in the tool is sufficient.
- `capability` (`:190`, `:160`) requires exactly one keyed row and that every backticked path
  *resolves*. It does not require the row to cite the live receipt, the counter, or any evidence for
  the capability — `.ufo/waves/round-38/count-c4.py` resolving is enough.
- `live_rows` (`:198`) is internal consistency only: named `<S###> drifted` lines == the summary's
  `drifted` count, ids present in the registry. Nothing re-derives the sweep or compares the receipt
  with the tool's output; an invented summary with `drifted=1` and one existing id passes, even though
  it contradicts the tip's receipt of record.
- `named_row_drift` / `drift_kill` are genuine: they execute the committed tool and a textual mutant.
  This half cannot be satisfied by editing the three binding artifacts.

So P-C4 as frozen is satisfied by an imitation binding. The counter discriminates exactly the three
frozen witnesses, not "content" in general: the three content arms are copyable, and only the tool arm
is behavior-derived. This is the r37 M9 class one level up — r37's tokens were real and the content
was imitation; here the strings *resolve* and the corpus work is imitation. `C4=met` is therefore
necessary but not sufficient evidence that the corpus binding was done.

## 4. FINDING R2 (MEDIUM): the witness sandbox does not isolate the witnesses

`contract.md:42-43` claims "the witness sandbox is the control that isolates each witness". The
negative battery (`count-c4.py:324`) projects each fixture onto **the measured rev's** other bytes; on
the sandbox rev the other two fixtures are themselves fabricated, so the conjunction has several false
conjuncts per witness. Evaluated directly with the counter's own functions:

| witness (on `d8c005e`) | own check | other-byte conjuncts | isolated? |
|---|---|---|---|
| `witness-token-entry` | `anchors(token_entry)=False` | rev scorecard has a dangling path → `paths resolve=False`; rev live is summary-only → `live=False` | no (3 false conjuncts) |
| `witness-dangling-row` | `capability(dangling)=True`, `paths resolve=False` | rev live summary-only → `live=False` | no (2 false conjuncts) |
| `witness-summary-only-live` | `live(summary_only)=False` | rev scorecard dangling path → `paths resolve=False` | no (2 false conjuncts) |

On the real tip the same evaluation gives exactly one false conjunct per witness (own check only):
`token-entry: False,True,True,True`; `dangling-row: True,True,False,True`;
`summary-only: True,True,True,False`. The requirement "each must fail at least one check" holds on both
revs, but the sandbox cannot attribute a rejection to a witness. The isolating projection is the real
tip, not the control built for it. If the control is meant to isolate, it needs three clones, one
witness each (or the counter should project each witness onto a fixed real rev, not onto the rev under
test).

## 5. FINDING R3 (LOW): the committed C4 receipts predate the pinned v3 counter

At the committed tip both C4 receipts carry detail strings the pinned counter no longer emits:

- `evidence/c4-after.txt` (committed): `command: … count-c4.py f725f307…`,
  `check anchors PASS (anchors=3 missing=[])`, `check live_rows PASS (named=10 summary_drifted=10 unknown=[])`.
- `evidence/c4-witness.txt` (committed): sandbox rev `d2ee0532` (a clone-only commit, absent from the
  lane), built from `f725f307` (an ancestor of the tip); `check anchors PASS (anchors=3 missing=[])`,
  `check capability FAIL (paths=['tools/mori-source-drift.py', 'evidence/no-such-receipt.txt'] missing=[…])`,
  `check live_rows FAIL (named=0 summary_drifted=10 unknown=[])`.
- The pinned v3 counter (`8332341c…`, `freeze-r38-v3.txt`) prints
  `anchors=3 missing=[] empty=0 unique=True` and `… unknown=[] unique=True` (my reruns, sections 2.3 and 3.2).

The committed receipts record `C4=met` at `f725f307` and `C4=unmet` on the `d2ee0532` sandbox; my
reruns at the tip and on the rebuilt sandbox give the same verdicts with the pinned v3 bytes, so the
measured claim stands. But the receipts of record are not reproducible from the frozen v3 bytes at the
scored tip. A working-tree re-emission of `c4-after.txt` (modified by another seat during this run, not by me;
it names `b6993744` and uses the v3 fields) matches my tip rerun; it is not committed.
`v3-token-control.txt` is committed and reproduces (same eight PASS lines).

## 6. FINDING R4 (LOW): assignment path/command defects (recorded, not repaired)

- The round-37 token counter is `.ufo/waves/round-37/count-c2.py` (v3, in the r37 freeze);
  `.ufo/waves/round-36/count-c2.py` is a different predicate and never reads the witnesses.
- The literal command without `--repo` exits 2 (section 2.1): counters default `--repo` to the lane and
  cannot resolve a `--shared` clone's commit. Any control run must pass `--repo <clone>`.

## 7. Residual risk and verification gaps

- **Authenticity of the live receipt is unverified by design.** `live_rows` is self-consistency; only a
  network re-run of the probe could distinguish an invented receipt from the sweep of record, and the
  counter deliberately does not do that. A fabricated receipt (section 3) is accepted.
- **Anchor/entry checks are copyable.** Any committed-text check over an entry can be satisfied by
  copying strings; requiring the round's rows/commit would raise the cost but not close the gap. Only
  behavior-derived checks (tool selftest + mutation) resist imitation.
- **Tool arm trust boundary (not exercised).** The counter executes the committed tool and mutates it
  textually (`return "drifted"` → `return "excerpt"`). A tool that inspects its own source/argv and
  emits the expected `row_states` PASS/FAIL strings could satisfy both `named_row_drift` and
  `drift_kill` without a real classifier; not attempted here (one fabrication only), but it is the
  remaining imitation path for the load-bearing half.
- **Not tested:** whether C4 holds when only one fixture is present at a rev (the sandbox packs all
  three); whether `capability` breaks if a second table row ever contains the key (it would return
  `row absent` → fail-closed); macOS/other-git environments.
- **Scope note:** the fabrication clone and the witness sandbox live under `/tmp`; the lane's committed
  bytes and index were not touched. No tools were installed or upgraded; no `pacman` transaction was
  run (host-wide pause honored). Single canonical runtime for every run: `python3 3.14.8`, `git 2.56.0`.
  No `lsp` device is exposed to this seat; no caller/definition analysis was needed for a
  behavior-only falsification — every claim here is execution-derived, not grep-derived.

## 8. Receipts

| command | rev / repo | result |
|---|---|---|
| `make-witness-sandbox.py b6993744 --out /tmp/r38-witness-control` | base `b6993744` | sandbox `d8c005e`, 3 files, +5/−2502 |
| `round-36/count-c2.py d8c005e` (literal) | lane default | setup error, exit 2 |
| `round-36/count-c2.py d8c005e --repo /tmp/r38-witness-control` | sandbox | `C2=met` exit 0 (r36 predicate, witnesses unread) |
| `round-37/count-c2.py d8c005e --repo /tmp/r38-witness-control` | sandbox | `C2=met` exit 0, 8/8 PASS |
| `round-38/count-c4.py d8c005e --repo /tmp/r38-witness-control` | sandbox | `C4=unmet` exit 1, 3 negatives rejected |
| `round-38/count-c4.py b6993744` | lane tip | `C4=met` exit 0 (same verdicts as committed `c4-after.txt`; committed receipt predates v3 — R3) |
| `round-38/count-c4.py 2ac814ee --repo /tmp/r38-fabrication` | fabrication | **`C4=met` exit 0** (three content checks PASS on imitation) |
