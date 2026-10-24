# RevOracle429 — Counter 429-handling vs contract amendment (C1)

Item attacked: contract.md:53-57 amendment vs `count-c1.py` `oracle_fetch` (~L177-232) and re-probe (~L609-616). Verify the six enumerated behaviors; FAIL on any divergence.

## Method

- Read `contract.md` L39-58 (amendment L53-57), `count-c1.py` L1-63, L177-268, L539-640; constants `ORACLE_TRIES=5` (L81), `ORACLE_BACKOFF=(5,10,20,30)` (L83), `RETRY_AFTER_CAP=120` (L84), `ORACLE_TIMEOUT=30` (L82).
- Empirical probe (scratch, `$TMPDIR`, no lane writes): `python3 /tmp/revoracle429_probe.py` imports `count-c1.py` read-only and drives `oracle_fetch` against a local `ThreadingHTTPServer` on 127.0.0.1 serving scripted statuses; `time.sleep` is recorded, not executed.

Observed outputs (command: `python3 /tmp/revoracle429_probe.py`):

```
A 404->200 -> outcome=('unavailable', None) hits=1 sleeps=[]
B 429->200 -> outcome=('error', 429) hits=2 sleeps=[0.05]
C 429 RA-cap -> outcome=('error', 429) hits=2 sleeps=[120]
D 500x5 -> outcome=('unavailable', None) hits=5 sleeps=[5, 10, 20, 30]
E 404x5 -> outcome=('unavailable', None) hits=1 sleeps=[]
F 429 noheader -> outcome=('error', 429) hits=2 sleeps=[5]
G 429then404 -> outcome=('unavailable', None) hits=2 sleeps=[5]
H 429then500then200 -> outcome=('error', 429) hits=3 sleeps=[5, 10]
I 404then429 -> outcome=('unavailable', None) hits=1 sleeps=[]
```

## Behavior-by-behavior

1. **Up to five tries — PASS.** `for attempt in range(ORACLE_TRIES)` (L193) with `ORACLE_TRIES=5` (L81).
2. **Retry-After honored on 429 (capped) — PASS.** L213-219: `wait = min(max(float(header), 0.0), RETRY_AFTER_CAP)`; cap 120 (L84). Probe B: RA=0.05 → recorded wait 0.05; probe C: RA=99999 → recorded wait 120; malformed header falls back to backoff (L216-219).
3. **5/10/20/30 backoff — PASS.** `ORACLE_BACKOFF=(5,10,20,30)` (L83), indexed by attempt 0..3 (L212, L229). Probe D (five 500s): recorded sleeps `[5, 10, 20, 30]`.
4. **A row answering 429 at any point is excluded even if a later try succeeded — PARTIAL / divergence.** The canonical case passes: L198 returns `("error", 429)` when `throttled` and a later try succeeds (probe B: 429→200 → `('error', 429)`). But when the later try answers a 4xx non-429, the early return at L208-210 fires before the throttled-exclusion, yielding `("unavailable", None)` instead of exclusion (probe G: 429→404 → `('unavailable', None)`, hits=2). Literal rule "answering 429 at any point is excluded" is not honored for this interleaving. Root cause = same lines as item 5.
5. **4xx (non-429) after the last try is unavailable — FAIL.** L208-210 return `"unavailable", None` on the **first** 4xx non-429; no remaining tries are made, so "after the last try" is never reached. Probes A (404 then 200 → `('unavailable', None)`, hits=1, sleeps=[]) and E (404×5 → hits=1) show a transient 4xx that would succeed on retry is permanently witnessed as "unavailable" — contradicting contract L54 "up to five tries, sequential, … backoff 5/10/20/30 s otherwise" and the enumerated requirement. The 4xx should be retried with backoff and declared unavailable only when the last try answers 4xx.
6. **Tool-unavailable re-probe rule — PASS.** L609-616: applies only when the oracle fetched (`want` ∈ fresh/excerpt/drifted) and the tool said `unavailable`; exactly one `oracle_fetch` call (L612 = re-probe once); `outcome == "body"` → mismatch (L613-614); otherwise note `real_excluded_throttled <sid> status=<payload>` (L616) and no mismatch → row excluded. Matches contract L55-57.

## Additional observations (secondary)

- **Docstring/intent vs code (5xx):** docstring L184 documents `("error", status)` for 5xx (excluded), but the last-try path L222-225 returns `("unavailable", None)`; probe D confirms `('unavailable', None)` after 5 hits. Consequence: a 5xx row becomes a required match state rather than excluded; if the tool later fetches it (fresh), the run would fail on a row the author's own spec intended to exclude. Not in the enumerated set; flagged as consistency risk.
- **Receipt horizon:** `evidence/c1-after.txt` (seed 7388485190103051243) shows `oracle_excluded=0`; neither 429 nor 4xx oracle outcomes were exercised in the real arm, so that receipt cannot validate items 4/5. The receipt numbers match the claim (real_rows=220, oracle_fetched=58, oracle_fresh=49, oracle_drifted=9, oracle_excluded=0, mismatches=0, tool_exit=1, C1=met, exit 0).

## Residual risk / verification gaps

- Static + local-server verification only; no live-host 429 was available (and none occurred in the receipt). The 4xx short-circuit is latent in the receipt, but under transient-4xx hosts it converts recoverable rows into oracle-"unavailable" witnesses (false-FAIL or tally distortion).
- No tool installations; stdlib only. No lane files modified (probe scratch under `$TMPDIR`).

## VERDICT: **FAIL** — divergence at `count-c1.py:208-210` (4xx non-429 returns `"unavailable"` on the first try instead of retrying up to five tries with backoff and declaring unavailable only after the last try; also preempts 429-exclusion when interleaved with a later 4xx, affecting item 4). Secondary: L184 vs L225 5xx docstring/code mismatch.
