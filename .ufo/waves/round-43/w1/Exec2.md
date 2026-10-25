# Exec2 — mori round 43 w1: assigned C1S counter run

Seat: Exec2 (executor, leaf member — zero subagents dispatched; labrat seat not granted, none spawned).

Axes named for this move: run fidelity (verbatim capture), zero lane mutation, evidence precision, latency.

## Assigned command

Run from `/home/vgpnk/Projects/shokunin/mori-shokunin`:

```
python3 .ufo/waves/round-43/count-c1s.py e3a2b58f72ba3bd52a90646f7285fb85f0ee5dd2
```

### stdout (verbatim)

```
check self_at_rev            FAIL (absent)
C1S=unmet
```

### stderr (verbatim)

```
(empty — zero bytes)
```

### exit code

```
1
```

Wall time ≈ 0.03 s (short-circuit; details below).

## Scoped findings

Measured results (command output + read-only git queries; inferences labeled).

1. **Verdict matches the contract's do-nothing control.** `C1S=unmet`, exit 1, with the sole failing check `self_at_rev (absent)`. Round-43 `contract.md` "Controls" states: "Do-nothing C1S: the counter against the entering tip prints `C1S=unmet`." The entering tip named in the contract is exactly `e3a2b58f72ba3bd52a90646f7285fb85f0ee5dd2`. (Control reproduced; the unmet-on-this-rev outcome is the designed result, not a counter malfunction.)

2. **Rev identity.** `e3a2b58f…` is a commit and is the current lane tip (HEAD): "round-42 verifier spot-check (integrator, hyaku): non-author admit/reject", 2026-10-24 21:13:07 -0300. `git merge-base --is-ancestor` → YES.

3. **Why "absent".** `.ufo/waves/round-43/` does not exist in the rev's tree (`git ls-tree <rev> -- .ufo/waves/round-43/` → empty), and `git show HEAD:.ufo/waves/round-43/count-c1s.py` reports `path … exists on disk, but not in 'HEAD'`. The round-43 counters and contract are working-tree files, not yet committed. The counter therefore returns after its first check (per its own docstring: "A rev that does not contain this file byte-identical to the running file stops after that check") and never exercises `frozen_sha`, `frozen_sig`, `noharm_cwd`, `v5_selftest_17`, the three mutant-kill checks, or `frozen_still_crashes`. No signal about those arms is contained in this run — that is the short-circuit working as written, not evidence they would pass.

4. **Frozen r42 counter integrity at the same tip (side observation, measured).** sha256 of `git show HEAD:.ufo/waves/round-42/count-c1.py` = `105ce075f33120837ba5a49a1ad4f23a3dd7dc17fea506ab917140bc7f2053f6`, equal to `FROZEN_SHA` pinned in count-c1s.py and quoted in contract.md. The frozen artifact is byte-intact at the entering tip.

5. **No mutation, no writes outside my own captures.** The counter reads lane git objects read-only; its `/tmp` sandbox (`mkdtemp` prefix `mori-r43-c1s-`) is allocated only after the `self_at_rev` gate, so this run created no sandbox at all. Only files I created: `/tmp/exec2-c1s-stdout.txt`, `/tmp/exec2-c1s-stderr.txt` (my capture buffers). Lane git index, working tree, and jj state untouched. No production files edited; no fleet/sibling-repo files touched; no tool installs performed. Per AGENTS.md the LOG.md append is not performed here because the dispatcher forbids production edits and lane git mutation for this seat — this report is the evidence record.

Inference summary: items 1–2, 4–5 are measured; the "by design" reading in items 1 and 3 is inferred from the quoted contract.md sentences, not from counter internals I judged.

## Result

Assigned move complete: command executed from the required directory, output captured verbatim, `C1S=unmet` / exit 1, consistent with the frozen contract's do-nothing control for the entering tip.
