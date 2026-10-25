# ResCritJunk — C1S junk self-attestation attack (round 43, w1)

## Axes named
- A1 execution fidelity: stub run from /tmp only; real counter run unmodified from its lane path.
- A2 evidence integrity: every command pasted with verbatim stdout and exit code.
- A3 lane bounds: no frozen-counter edit, no lane git/jj/index mutation; only file written is this report.
- A4 claim adjudication: does a body of just `print("C1S=met")` get scored `met` (junk win) or `unmet` (guard holds).

## Attack
Contract control "Do-nothing C1S junk" (contract.md L60-61): a scratch rev whose
`count-c1s.py` only prints `C1S=met` must be scored `C1S=unmet` by this counter.
The guard is `self_at_rev` (count-c1s.py L91-97): the running file must be
byte-identical to `<rev>:.ufo/waves/round-43/count-c1s.py` or the counter bails
early with `C1S=unmet`.

Setup (all in /tmp; lane read-only throughout):
- `/tmp/mori-r43-w1-c1s-junk/count-c1s-real-copy.py` — pre-attack copy of the real counter (172 lines).
- `/tmp/mori-r43-w1-c1s-junk/count-c1s-stub.py` — 2 lines: shebang + `print("C1S=met")`.
- Scratch git rev `3eb02b954d7da41c7ef8411d300538596a00e95a` in
  `/tmp/mori-r43-w1-c1s-junk/scratch-rev`, carrying the stub at
  `.ufo/waves/round-43/count-c1s.py`.

## Evidence

1. Stub self-attests met (the junk behavior under attack):

```
$ python3 /tmp/mori-r43-w1-c1s-junk/count-c1s-stub.py; echo "exit=$?"
C1S=met
exit=0
```

2. Real counter at that same rev rejects the junk:

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-43/count-c1s.py 3eb02b954d7da41c7ef8411d300538596a00e95a --repo /tmp/mori-r43-w1-c1s-junk/scratch-rev; echo "exit=$?"
check self_at_rev            FAIL (bytes differ)
C1S=unmet
exit=1
```

3. Do-nothing control at the entering tip pinned during review (`e3a2b58f72ba…`,
   counter then untracked): also `C1S=unmet` — matches contract L32-35/L59.

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-43/count-c1s.py e3a2b58f72ba3bd52a90646f7285fb85f0ee5dd2; echo "exit=$?"
check self_at_rev            FAIL (absent)
C1S=unmet
exit=1
```

## Residuals checked (no defect found)
- Counter integrity: `cmp` of lane counter vs pre-attack copy → byte-identical;
  frozen counter never edited. Stub differs (172 vs 2 lines) and is not an
  authority — no duplicate verdict path exists: only the byte-identity gate
  decides which output is evidence.
- No false provenance: real counter executed from its canonical lane absolute
  path, unmodified; `--repo` only redirects where `<rev>` bytes are read from.
- Lane mutation: none (all writes in /tmp + this report). Note: lane HEAD moved
  `e3a2b58f…` → `dde525ea…` from concurrent seat activity mid-review; probes are
  rev-pinned so the evidence above is reproducible. At the new tip,
  `git show dde525ea:.ufo/waves/round-43/count-c1s.py | cmp` against the running
  file → byte-identical (green-path `C1S` scoring at that tip is the planner
  seat's control, out of this seat's scope).
- Premature saturation: none — early `self_at_rev` bail is the contract-mandated
  do-nothing path, not a truncated verdict.

## Impacted axes
A4 (claim adjudication): attack rejected — junk self-attestation cannot flip C1S.
A1/A2/A3: clean; no correction needed anywhere.

## Smallest safe correction
None. The `self_at_rev` byte-identity gate fully covers the planted-junk case;
the contract's junk control holds as written.

Verdict: SURVIVED — command and output:

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-43/count-c1s.py 3eb02b954d7da41c7ef8411d300538596a00e95a --repo /tmp/mori-r43-w1-c1s-junk/scratch-rev; echo "exit=$?"
check self_at_rev            FAIL (bytes differ)
C1S=unmet
exit=1
```
