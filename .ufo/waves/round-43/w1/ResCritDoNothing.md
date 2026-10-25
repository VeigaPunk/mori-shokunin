# ResCritDoNothing — C1S do-nothing replay of the entering tip

Seat: residual critic w1 (leaf, zero subagents). Attack C1S: claim under
attack was "a do-nothing replay of the entering tip `e3a2b58f72ba3bd52a90646f7285fb85f0ee5dd2`
still prints `C1S=met`." Frozen counters read, never edited; lane repo
read-only; all scratch work in /tmp only.

Axes named: verbatim output fidelity, lane immutability, claim
discrimination (counter must not be foolable), latency.

## Assigned run (measured)

Exact assigned command, lane untouched:

```
check self_at_rev            FAIL (absent)
C1S=unmet
```

exit code **1**. Wall ≈ 0.03 s — the counter short-circuits at its first
gate, per its own docstring ("A rev that does not contain this file
byte-identical to the running file stops after that check"). No /tmp
sandbox is allocated on this path (`mkdtemp` sits after the gate).

## Why "absent" — the claim's premise is false at this rev

- `git show e3a2b58…:.ufo/waves/round-43/count-c1s.py` →
  `fatal: path '…' exists on disk, but not in 'e3a2b58f72ba3bd52a90646f7285fb85f0ee5dd2'`.
  The round-43 counter is a working-tree file, not committed at the
  entering tip, so `self_at_rev` cannot pass there.
- No hidden object substitution: `git replace -l` → empty, no
  `.git/info/grafts`, repo not shallow. `git show rev:path` is authoritative.
- This is not a counter malfunction: round-43 `contract.md` freezes the
  opposite expectation — "That is the do-nothing result on the entering tip"
  (P-C1S) and Control "Do-nothing C1S: the counter against the entering tip
  prints `C1S=unmet`". The assignment's asserted output (`C1S=met`)
  contradicts the frozen contract; the counter printed the contracted result.

## Attack in /tmp — counter is not foolable (junk control)

Scratch clone `/tmp/rescrit-junk/repo` (shared, detached at e3a2b58…),
junk rev `d229c92e2a5713bb6f79729fa981a4762a704837` planting
`print("C1S=met")` at the counter path, scored via `--repo`:

```
check self_at_rev            FAIL (bytes differ)
C1S=unmet
```

exit 1. A planted met-printer at a rev scores `unmet`; the working-tree
counter bytes are invisible to the rev-scoped check. Combined with the
prior green control evidence (`evidence/control-c1s-green.txt`: all 14
checks PASS, `C1S=met` exit 0, only when the byte-identical counter is
committed in a scratch clone), the counter discriminates exactly on
committed rev bytes — it neither always-passes nor always-fails.

Cross-reference: `evidence/control-c1s-donothing.txt` and
`control-c1s-junk.txt` match my two runs check-for-check.

## Impacted axes and smallest safe correction

- Impacted: fidelity of the round-43 scoring plan (the assigned attack text
  asserted `met`; contract and measurement say `unmet`). No calibration,
  depth, or freshness axis moves: this run is the contract's designed
  do-nothing control, not new defect surface.
- Smallest safe correction: **none to the counter**. Correct the premise:
  a do-nothing replay of `e3a2b58…` cannot print `C1S=met`; `met` requires
  scoring a rev that contains this counter byte-identical (e.g. the green
  scratch clone), which is commit work, not replay.
- Hygiene: no lane git/jj/index/working-tree mutation; only files written
  are this report and /tmp scratch (`/tmp/rescrit-junk`, left for
  re-execution). Running counter unedited, sha256
  `93482248b46def2a2cec7238732af1551ef315517e76833c3843875313b65dc5`.

## Verdict

The claim "do-nothing replay of `e3a2b58…` still prints `C1S=met`" is
killed: the exact assigned command prints `C1S=unmet`, exit 1, matching
the frozen contract's do-nothing control, and /tmp attack runs show the
counter cannot be fooled into `met` on this rev.

Verdict: KILLED
Command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-43/count-c1s.py e3a2b58f72ba3bd52a90646f7285fb85f0ee5dd2`
Output:

```
check self_at_rev            FAIL (absent)
C1S=unmet
EXIT=1
```
