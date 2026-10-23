# w1/RevC1Predicate — C1 re-measurement, three fresh seeds + predicate byte check

Scope: re-measure claim C1 with seeds 41/42/43 at the scored tip `e57c58b57c025364e79d130fbdf764d2674d83d6`, and verify the counter's first printed line is byte-identical to the P-C1 sentence in `.ufo/waves/round-37/contract.md`. Lane untouched; scratch was ephemeral (`/tmp/mori-c1-tool-*`, cleaned by the counter itself). No tools installed (nothing needed — python3 present). Lane repo read-only: no writes, no jj/git mutations; this file is my one written file.

## Axes

1. **Re-measurement stability** — does the frozen counter still print `C1=met` / exit 0 on fresh, previously-unmeasured seeds (41, 42, 43), with blind, real, and challenge arms passing and all three negative fixtures rejected per run?
2. **Predicate byte-fidelity** — is the first line the counter prints byte-identical to the P-C1 sentence frozen in the contract (same bytes, not just same words after normalization)?

## Axis 1 — three fresh seed runs

Command (run once, sequential loop; wall 12.8 s):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && for s in 41 42 43; do python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed $s; echo EXIT=$?; done
```

Every run opened with the P-C1 predicate line (verified byte-identical in Axis 2), then the tool path under a fresh `mkdtemp` (`/tmp/mori-c1-tool-_j08f4cr/…`, `/tmp/mori-c1-tool-1avz9_q7/…`, `/tmp/mori-c1-tool-tmcurpo0/…` — three distinct scratch dirs, no seed-derived collision).

### seed 41

```
blind arm: 24/24 sandbox histories matched the hidden truth (2.1s; coverage: deletions=21 changed-back=14 superseded=12)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=4 ids=[S054,S116,S236] deleted=[S081] superseded=[S054] round_changed=[S081,S116,S236]
  tool:   appendonly_violations=4 ids=[S054,S116,S236] deleted=[S081] superseded=[S054] round_changed=[S081,S116,S236]
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=3 ids=[S179] deleted=[S066,S116] superseded=[S179] round_changed=[S066,S116] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=41
EXIT=0
```

### seed 42

```
blind arm: 24/24 sandbox histories matched the hidden truth (2.2s; coverage: deletions=22 changed-back=16 superseded=8)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=5 ids=[S095,S162] deleted=[S203,S231,S287] superseded=[S095,S162] round_changed=[S162,S203,S231]
  tool:   appendonly_violations=5 ids=[S095,S162] deleted=[S203,S231,S287] superseded=[S095,S162] round_changed=[S162,S203,S231]
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=6 ids=[S210] deleted=[S091,S129,S243,S292,S293] superseded=[S210] round_changed=[S091,S129,S210,S216,S243,S292,S293] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=42
EXIT=0
```

### seed 43

```
blind arm: 24/24 sandbox histories matched the hidden truth (2.3s; coverage: deletions=21 changed-back=15 superseded=10)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=2 ids=[S267] deleted=[S201] superseded=[S267] round_changed=[S201]
  tool:   appendonly_violations=2 ids=[S267] deleted=[S201] superseded=[S267] round_changed=[S201]
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=4 ids=[S193] deleted=[S074,S164,S199] superseded=[] round_changed=[S074,S199,S238] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 3/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=43
EXIT=0
```

Observations across the three fresh seeds:

- **Blind arm**: 24/24 sandbox histories matched the hidden truth each run, with genuinely varying draw coverage (deletions 21/22/21, changed-back 14/16/15, superseded 12/8/10) — the seed actually changes the sampled histories.
- **Real arm**: pass all three; tool and independent oracle agree on the full lane-history lists (18 ids, matching superseded/round_changed), tool exit=1 as expected.
- **Challenge arm**: pass all three; three different run-time-drawn histories in real-arm clothing, tool truth == oracle truth each time (including the forced-deletion witness `deleted=[…]` non-empty in every draw).
- **Negatives**: all three fixtures rejected in all three runs — the memoizer dies on the challenge arm (its published 18-id constant differs from every challenge draw's truth), the constant printer dies blind (`repo200: lists differ`), the summary-only printer dies blind on per-id lines. Note seed 43's summary-only rejection was 3/4 with the same `repo200` per-id failure; the fixture is still killed, exit path unchanged.
- **Verdict/exit**: `C1=met` and `EXIT=0` in all three runs.

## Axis 2 — predicate byte-fidelity

Method (no eyeballing): extracted the P-C1 blockquote from `contract.md` (the 8 `> ` lines under `**P-C1 (frozen…):**`), joined the soft-wrapped lines with single spaces, and byte-compared (`==` on `str` and on `.encode()`) against (a) the first printed line of a fresh counter capture (seed 41 rerun captured to a pipe) and (b) the `PREDICATE` string constant in `count-c1.py:42-52` (printed verbatim at `count-c1.py:850`).

Observed:

- contract sentence: 623 chars; printed first line: 623 chars
- `str-equal: True`, `byte-equal: True`
- `PREDICATE` constant == printed line: True
- sha256 of both: `3fd09482d0af35b81f7bf13cbe55bfa758992bcd8efcd80de2a12ca695a19355`

No difference. The counter prints the frozen sentence byte-for-byte (same 623 bytes as the contract's P-C1 sentence).

## Residual risk / gaps

- The counter's timeout boundary (`tool_timeout`) and the "cannot distinguish slow honest tool from hung one" limit are disclosed contract terms, not exercised here (no arm timed out; all runs finished in seconds).
- Seed-43's summary-only kill was 3/4 rather than 4/4 blind; the fixture still fails the blind arm, so the gate's kill rule holds. No action.
- Runs used `/tmp` scratch (counter-owned `mkdtemp`), not `/fast/scratch`; lane repo was never written by the counter (tool copies run in its own tmp dir), consistent with the contract's scratch-uniqueness disposition (debt g).

**Attacks**: claim C1's measured result and the frozen predicate text (both survive: stable verdict on fresh seeds, exact-byte predicate).

VERDICT: PASS
