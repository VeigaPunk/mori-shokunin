# Exec4 — round 43 / wave 1 — mandated sha256 check

Seat: Exec4 (leaf member, mori lane). No subagents dispatched (not probeParent-seated; leaf bounds allow at most one labrat — none spawned).

## Axes

- **Fidelity** — exact dispatcher-mandated command, verbatim stdout/stderr/exit code, no reinterpretation.
- **Isolation** — writes limited to this report file and /tmp scratch; zero mutations to lane Git/jj/index, `.ufo/state`, `.ufo/watchdog.log`, fleet files, sibling repos, or frozen counters.
- **Speed** — single wave, first-pass success, no clarifying loop, no retries.

## Mandated check

Run from `/home/vgpnk/Projects/shokunin/mori-shokunin`:

```
sha256sum corpus/evidence/sources-r42/S235.pdf
```

Verbatim capture (streams redirected to /tmp scratch, then echoed; wall time 0.012 s):

```text
== STDOUT ==
9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020  corpus/evidence/sources-r42/S235.pdf
== STDERR ==
== EXITCODE: 0 ==
```

- **stdout:** `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020  corpus/evidence/sources-r42/S235.pdf`
- **stderr:** (empty)
- **exit code:** 0

Result: S235.pdf reads cleanly; SHA-256 digest `9855a498…7ad8020`. Detection only — no interpretation of source content, no provenance claim beyond the digest of the bytes at that path at run time (2026-10-24, host-local).

## Bounds attestation

- Command executed read-only in the lane dir as mandated by the dispatcher; all other code ran nowhere (no /tmp sandbox code needed beyond stream capture files).
- Files written: only `.ufo/waves/round-43/w1/Exec4.md` (this file) and `/tmp/exec4_stdout.txt`, `/tmp/exec4_stderr.txt`.
- Not touched: lane Git index/history, jj state, `.ufo/state`, `.ufo/watchdog.log`, frozen counters (`.ufo/waves/round-42/count-c1.py`, `.ufo/waves/round-43/count-c1s.py`, `count-c2.py`), fleet root, sibling repos, shokuknow, secrets, host services. No pacman. No model identifiers passed or hardcoded (no subagents at all).

## AGENTS.md note (recorded, not acted on)

`AGENTS.md:4` — "Every change appends a LOG.md entry with the evidence that motivated it." My only change is this mandated report; the round dispatch bound ("Write only your own report file") is the canonical instruction source for this seat, so I did **not** append to the shared `LOG.md` (177 KB, round-shared; concurrent Exec-seat appends would also collide). Deferring the LOG.md entry decision to the L1/tower: tension recorded here, unilaterally resolved by neither rule.

## Remaining risks

- Digest is a point-in-time read; it does not certify the PDF's provenance or immutability (mori reports, never attests authorship).
- LOG.md entry not appended per dispatch bound — tower may want to record the round's evidence there under a single writer.

## Blockers

None.
