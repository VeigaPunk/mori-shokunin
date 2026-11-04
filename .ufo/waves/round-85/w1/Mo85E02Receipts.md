# Mo85E02Receipts — receipt generator + provenance grammar (round 85, wave w1, attempt 1)

Seat: Mo85E02Receipts (executor, leaf — no subagents). Date: 2026-11-04.
Lane: `mori-shokunin`. Freeze `ab2608655ea52ba6d151b3a31d69a3b18cd2b41e`; entering `2cc4b1ae`.
Scope written: `.ufo/waves/round-85/make-receipts.sh` (this seat's deliverable) and this report.
Nothing else in the lane was written: the three receipts were generated only into scratch
clones (the L1 regenerates them at the measured revision); `git status --porcelain` on
`.ufo/waves/round-85/evidence/` in the lane shows no file written by this seat. Read-only git
(`log`, `show`, `diff`, `status`, `rev-parse`, `clone --shared`) on the lane; the only
mutating git ran inside scratch fixture repos under
`/fast/scratch/hyaku/mori-r85/Mo85E02Receipts/` (deleted before this seat yielded), each
asserting `git rev-parse --show-toplevel` equals the fixture dir before its first commit and
using `-c user.name=t -c user.email=t@t`. No tools installed; no pacman transaction; no lane,
OS, unit, service, credential, harness or orchestration state changed.

## 0. Deliverable

`.ufo/waves/round-85/make-receipts.sh` — usage `make-receipts.sh <rev> [--repo DIR]`, run from
the lane root. sha256 of the final bytes (measured, this seat, from the worktree):
`7fd5e04346ece0143c1efc1166cefabec62da8cffe8a4f2659cd1107a099cbd0` (7681 bytes). `bash -n` clean.
Tracked state at report time: the L1 committed the generator at `25a74d4c` (7503 bytes — this
seat's bytes through the limits-wording fix); this seat's final delta (` M` in the worktree,
7 insertions / 2 deletions) adds one `rc=<n>` line per body run with correct `LAST_RC`
plumbing. Every proof in §1-§4 below ran against the final worktree bytes.

It resolves `<rev>` with `git rev-parse <rev>^{commit}` (never invents one), requires `--repo`
to be the git toplevel (fails closed with exit 2), keeps all scratch under
`HYAKU_SCRATCH` (default `/fast/scratch/hyaku`, never /tmp) via a trap, runs the two counters
and the two sweeps exactly as the `# cmd:` lines state, binds the five frozen paths' bytes at
`<rev>` by raw `git show | sha256sum` (identical to the counter's text-mode measure on these
UTF-8, LF-only blobs — confirmed end-to-end by `bound=5` under both counter generations),
appends raw stderr when non-empty and a `rc=<n>` line per run, warns (does not fail) when a
frozen summary token is absent from a body, and writes each receipt atomically (tmp + mv).
One `# cmd:`, one `# rev:`, one `# limits:` (all contain the word `limit`, ≥3 words), exactly
one `# ---`, `# counter-sha256:` lines: 3 for after-r85 (count-c1/2/3.py), 1 each for the two
sweeps. The after-r85 limit sentence states that the C1/C3 bodies are counter runs at the named
revision while the two sweep receipts' bodies are worktree runs pinned to the same bytes by
their bindings.

**Coordinate disclosure.** This file was written at 08:19, before the L1's first message
reached this seat; the L1's scratch fallback existed only in the worktree (never committed —
`git log --all -- .ufo/waves/round-85/make-receipts.sh` is empty at report time) and was
superseded: the L1 tested these 7498-byte bytes in a scratch clone and read the met line.
Nothing of the L1's needed recovery; this seat then re-proved everything below from scratch.

**Frozen-set movement during the wave (all pre-data; counters re-read after each).** A1
`79bb4ed8` (bindings verified at the receipt's own `# rev:` via `make_loader`), A2 `4ffd5a2d`
(header block = everything before the first `# ---`; header-shaped body lines are body text;
loose duplicates; a malformed `# counter-sha256:` is `malformed-binding` and still counts
toward `bindings`; `# limits:` ≥3 words incl. `limit`), A3 `89f82eac` (count-c3 requires the
subject's `C2=met` verdict; selftest 19→20 arms), A4 `91f657f6` (contract/controls prose only;
counters unchanged). The three counters and the contract were never edited by this seat.

## 1. Proof — seat step 2: frozen counter selftest (lane tip)

```text
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 -I .ufo/waves/round-85/count-c2.py --selftest | tail -1
C2_COUNTER_SELFTEST pass=18 fail=0
rc=0
```

## 2. Proof — seat step 1: generation at the freeze revision (scratch only)

```text
$ git clone -q --shared $LANE /fast/scratch/hyaku/mori-r85/Mo85E02Receipts/freeze-clone
$ git -C freeze-clone checkout -q --detach ab2608655ea52ba6d151b3a31d69a3b18cd2b41e
$ cd freeze-clone && HYAKU_SCRATCH=$S/gen bash $LANE/.ufo/waves/round-85/make-receipts.sh \
    ab2608655ea52ba6d151b3a31d69a3b18cd2b41e --repo $PWD
make-receipts.sh: note: body lacks C3=met (the run did not print it at ab260865…)
make-receipts.sh: wrote .ufo/waves/round-85/evidence/after-r85.txt (rev ab260865…)
make-receipts.sh: wrote .ufo/waves/round-85/evidence/record-sweep-r85.txt (rev ab260865…)
make-receipts.sh: wrote .ufo/waves/round-85/evidence/claim-sweep-r85.txt (rev ab260865…)
gen-rc=0
```

Headers as frozen (frozen receipts, freeze-revision run):

```text
# receipt: after-r85.txt
# cmd: python3 -I .ufo/waves/round-85/count-c1.py ab2608655ea52ba6d151b3a31d69a3b18cd2b41e; python3 -I .ufo/waves/round-85/count-c3.py ab2608655ea52ba6d151b3a31d69a3b18cd2b41e
# rev: ab2608655ea52ba6d151b3a31d69a3b18cd2b41e
# counter-sha256: da5fb27b… .ufo/waves/round-85/count-c1.py      (64-hex each; 3 lines)
# limits: named limit — the C1 and C3 bodies above are counter runs at the named revision while the two sweep receipts' bodies are worktree runs pinned to the same bytes by their counter-sha256 bindings
# ---
```

The freeze-revision bodies are honest and unmet, as they must be (the arms are not landed at
the freeze): `C1=unmet mutants=2 killed=0 survivors=2 total=2 arms=15 harness=stub
missing=killed_mutant_with_coupling_not_equivalent,duplicate_coupling_not_equivalent
rc=1`; C3 reads `C3=unmet observed=3 aa=stable subject=unmet rc=1` because in a scratch clone
the census observes the scratch parent as fleet root (live tokens 52 ≠ the real fleet's 64) —
an in-clone artifact, disclosed; on the real lane at the measured revision the C3=met warning
does not fire (L1-confirmed behaviour). Sweep bodies carry `RECORD_SWEEP pending=0 pinned=0
carriers=1 bindings=3 revisions=0 rc=0` and `CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0
stale=0 carriers=4 pointers=266 rc=0`.

## 3. Proof — seat step 3 + L1 defeat control (my own runs)

Freeze-clone, receipts committed on top of the freeze (fixture asserts toplevel; commits with
`-c user.name=t -c user.email=t@t`). The clone's count-c2 bytes are the pre-A1 frozen ones:

```text
$ python3 -I .ufo/waves/round-85/count-c2.py HEAD          # uncorrupted
PROBLEM after-r85.txt summary=C1=met
RECEIPT after-r85.txt headers=1 rev=1 limits=1 bindings=3 bound=3 summary=0
RECEIPT record-sweep-r85.txt headers=1 rev=1 limits=1 bindings=1 bound=1 summary=1
RECEIPT claim-sweep-r85.txt headers=1 rev=1 limits=1 bindings=1 bound=1 summary=1
C2=unmet receipts=3 bindings=5 bound=5 revs=3 limits=3 cmd=3 summary=2 mismatch=1 detector=green
rc=1        # the single mismatch is the absent C1=met summary token at the freeze revision

$ # one hex digit of after-r85.txt binding 1 flipped (da5fb27b… -> ea5fb27b…), committed
$ python3 -I .ufo/waves/round-85/count-c2.py HEAD
PROBLEM after-r85.txt sha:.ufo/waves/round-85/count-c1.py
PROBLEM after-r85.txt summary=C1=met
…
C2=unmet receipts=3 bindings=5 bound=4 revs=3 limits=3 cmd=3 summary=2 mismatch=2 detector=green
rc=1
```

The stale-binding defect moves exactly `bound 5→4, mismatch +1`; at the freeze the baseline
mismatch is the honest summary absence, so the corrupted run prints `mismatch=2`. The frozen
defeat control's exact `bound=4 mismatch=1` form requires met bodies — reproduced at a code
revision (below), which is also the L1's requested met line.

Met direction — fresh `git clone --shared` at code revision `729b794aa7627190afa0ebd6d2d4dd07ae85e2af`
(the committed r84 counter carries the two arms; `C1=met mutants=2 killed=2 survivors=0 total=2
arms=17 r84=met rc=0` measured there), receipts generated by this seat's generator and committed:

```text
$ python3 -I .ufo/waves/round-85/count-c2.py HEAD          # uncorrupted (amended counter bytes)
RECEIPT after-r85.txt headers=1 rev=1 limits=1 bindings=3 bound=3 summary=1
RECEIPT record-sweep-r85.txt headers=1 rev=1 limits=1 bindings=1 bound=1 summary=1
RECEIPT claim-sweep-r85.txt headers=1 rev=1 limits=1 bindings=1 bound=1 summary=1
C2=met receipts=3 bindings=5 bound=5 revs=3 limits=3 cmd=3 summary=3 mismatch=0 detector=green
rc=0

$ # one hex digit of after-r85.txt binding 1 flipped (da5fb27b… -> 0a5fb27b…), committed
$ python3 -I .ufo/waves/round-85/count-c2.py HEAD
PROBLEM after-r85.txt sha:.ufo/waves/round-85/count-c1.py
RECEIPT after-r85.txt headers=1 rev=1 limits=1 bindings=3 bound=2 summary=1
RECEIPT record-sweep-r85.txt headers=1 rev=1 limits=1 bindings=1 bound=1 summary=1
RECEIPT claim-sweep-r85.txt headers=1 rev=1 limits=1 bindings=1 bound=1 summary=1
C2=unmet receipts=3 bindings=5 bound=4 revs=3 limits=3 cmd=3 summary=3 mismatch=1 detector=green
rc=1
```

That is exactly the frozen stale-digest defeat control: `C2=unmet … bound=4 mismatch=1`, rc 1.
`revs=3` held in every run: each `# rev:` resolves to the graded tip or an ancestor.

## 4. Proof — does the header block parse under the frozen `parse_receipt`? Yes.

Direct import of the fixture counter's `parse_receipt` over the three generated receipts:

```text
after-r85.txt          problems=[]  bindings=3  rev=729b794aa762  limits-words=34
record-sweep-r85.txt   problems=[]  bindings=1  rev=729b794aa762  limits-words=24
claim-sweep-r85.txt    problems=[]  bindings=1  rev=729b794aa762  limits-words=24
```

All headers are before the single `# ---` (the A2 body-split rule is satisfied; no body line is
header-shaped), exactly one cmd/rev/limits each, every binding well-formed, `bound=5` under the
counter's own byte verification at the receipts' own revisions (A1 loader). The A2 grammar
changes (loose duplicates, `malformed-binding`, weak-limits) are covered by the counter's own
selftest arms inside the `pass=18 fail=0` run of §1 — this seat exercised the happy path and
the digest-defeat path, not the malformed-line arms.

## 5. L1 report notes (as requested)

1. Header-block-before-`# ---` parsing: compatible — my headers are all above the single
   separator and no body line is header-shaped (bodies are counter/sweep stdout + `rc=` lines).
2. `# limits:` word rule: satisfied (34/24/24 words, literal `limit`).
3. `C3=met` warning behaviour: confirmed — it fires in scratch clones (census sees the scratch
   parent as fleet root → subject unmet → body lacks `C3=met`); it must NOT fire on the real
   lane at the measured revision, where C3 reads met.
4. The stale-digest control was reproduced byte-exactly at a code revision with met bodies:
   `bound=4 mismatch=1` rc 1.

## 6. Risks / limits

- The real receipts are intentionally absent from the lane; the L1 regenerates them at the
  measured revision with this generator (`make-receipts.sh <rev>` from the lane root). The
  generator's bindings pin bytes at `<rev>`; if the counters or sweep tools change between the
  graded revision and generation time, the L1 must pass the graded revision — the receipt
  grammar then reports the drift instead of hiding it, which is the point of P-C2.
- Scratch clones under `/fast/scratch/hyaku/mori-r85/Mo85E02Receipts/` were deleted on yield;
  every command and output above is quoted in full (D84-5 class: receipts carry `# rev:`
  headers; these proof transcripts are self-contained).
- No check was re-run to "confirm" anything beyond what is quoted; unrun checks are not
  claimed.

Files changed: `.ufo/waves/round-85/make-receipts.sh` (new), `.ufo/waves/round-85/w1/Mo85E02Receipts.md`
(this report, new).
