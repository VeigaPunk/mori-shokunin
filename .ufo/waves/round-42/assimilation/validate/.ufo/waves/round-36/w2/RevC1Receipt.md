# w2 RevC1Receipt — audit of evidence/c1-after.txt (C1 byte-behavior receipt)

Reviewer: mori-r36-w2-RevC1Receipt-13 (falsify + verify seat). Attacks **evidence/c1-after.txt**.
Canonical runtime: Python 3.14.8 (`python3 --version`), frozen v2 counter bytes, git backend, lane HEAD = `bf0df77fee4b6ef54a90aea09335c7617f125151`. No tools installed (nothing needed). Lane untouched (read-only commands only; replay ran on a scratch sandbox repo). Scratch: `/fast/scratch/hyaku/mori-r36/RevC1Receipt-13/`.

## What the receipt contains (exhaustive, byte-level)

`sha256sum .ufo/waves/round-36/evidence/c1-after.txt` → `bdf017cbdace96898839fb3bf3be1799edb3e5ec0dd26918ad12356b994470ea`; 6 lines + trailing newline (repr inspected):

1. `P-C1: at revision R, tools/mori-source-drift.py classifies … oracle-drifted row.`
2. `blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0`
3. `real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0`
4. `C1=met`
5. `seed=7388485190103051243`
6. `C1_EXIT=0`

## Checks (command → observed output)

1. **First line == contract.md:21 P-C1 == counter's printed sentence.** AST-extracted `PREDICATE` from `.ufo/waves/round-36/count-c1.py` and byte-compared all three: `contract:21 == receipt:1 : True`; `counter PREDICATE == receipt:1 : True`; `git show bf0df77:…contract.md` == worktree (`True`); line-21 sha256 `304a3d0afb5682e1…`. The "same sentence printed by the counter and used as the receipt label" holds byte-for-byte.
2. **Counter sha256 == freeze-v2.txt.** `sha256sum .ufo/waves/round-36/count-c1.py` → `86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0`; `git show bf0df77:…count-c1.py | sha256sum` → identical; freeze-v2.txt pins `86dd3b7a…8764c0`. **Match** — the receipt is a receipt of the frozen v2 counter.
3. **Blind arm 40/40, mismatches=0, exit in (0,1).** Receipt line 2 matches the counter's format string exactly (`"blind_rows=%d tool_exit=%s tool_rows=%d mismatches=%d"`); `passed = not mismatches and rc in (0, 1)`; 8 drifted rows force tool exit 1 per the tool spec. **Reproduced**: ran the frozen counter at the pinned seed on a sandbox repo (real arm aborts pre-fetch, zero external requests):
   `MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/RevC1Receipt-13 python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151 --repo <sandbox> --seed 7388485190103051243` → prints the P-C1 sentence, then `blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0`, then `real=unmet worktree_corpus_differs_from_rev` (expected — sandbox corpus differs from R, aborts before any tool run), `C1=unmet`, `seed=7388485190103051243`, `REPLAY_EXIT=1`. The blind line is genuine, seed-reproducible counter output, not a fabrication.
4. **Real arm thresholds and exclusion handling.** Receipt: `oracle_fetched=58 ≥ 10`, `oracle_fresh=49 ≥ 1`, `oracle_drifted=9 ≥ 1`, `mismatches=0`, `tool_exit=1 ∈ (0,1)`. Code (`real_arm`, `oracle_classify`, `oracle_fetch`): pass requires exactly these plus `rc in (0,1)`; excluded rows are listed with reasons — `oracle_excluded <id> status=<s>` for oracle fetch failures, `real_excluded_throttled <id> status=<s>` when a tool-`unavailable` row's single oracle re-probe does not fetch (contract.md:55-57 rule implemented verbatim, including Retry-After honored on 429 with 5/10/20/30 s backoff, RETRY_AFTER_CAP=120). Here `oracle_excluded=0` and the receipt carries no exclusion notes — consistent (nothing to list; the mechanism is present and printing).
5. **Saturation honesty.** `git show bf0df77:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3}'` → **220** = `real_rows=220` = `tool_rows=220`. `git ls-tree -r --name-only bf0df77 -- corpus/evidence/` → **58** files matching `sources-rN/S###.ext`, **58 distinct ids** = `oracle_fetched=58` with `oracle_excluded=0`: every row holding a committed copy was fetched cleanly; none dropped, none inflated. Margins are wide (58 vs 10; 49 vs 1; 9 vs 1) — no threshold-gaming shape.
6. **Exit 0 and seed printed.** Receipt line 6 `C1_EXIT=0`; counter returns 0 iff met (`met = blind_pass and real_pass` → `C1=met` then `seed=%d`). Seed `7388485190103051243 < 2^63` fits the `os.urandom(8)` draw; it is the seed printed in "Where things stand" and it reproduces the blind arm (check 3). (Line 6 is a capture annotation, not counter output — the counter emits lines 1–5; the annotation agrees with the code's return value.)
7. **No freshness/axis verdict wording.** The receipt's full byte content is shown above: pure frozen-counter output plus the exit annotation. The only verdict-shaped token is `C1=met`, which is the counter's contract-mandated final output for the **byte predicate** (`P-C1 … including at least one oracle-fresh and one oracle-drifted row.` labels the receipt), and contract.md states P-C1 "is still run and reported as evidence of the probe's byte behaviour, not as C1's verdict." No wording anywhere in the receipt asserts a freshness/axis result ("fresh"/"drifted" appear only as frozen rule names inside P-C1 and the `oracle_fresh`/`oracle_drifted` field names). Nothing to attack on this point.

## Findings by severity

No defect found in the receipt. Informational/low, none affecting the receipt's validity:

- **LOW (stale docs inside a frozen artifact).** `count-c1.py` module docstring (lines ~16–21) still describes v1: "the tool runs on a `git archive <rev>` extraction … never the live worktree" and "the oracle runs concurrently with the tool". The v2 code in the same file does the opposite: `real_arm` sets `root = os.path.abspath(repo)`, enforces `git diff --quiet <rev> -- corpus` + no untracked files under `corpus/` (contract.md:53), and runs the tool first, oracle after. Behavior is v2-conformant; the docstring cannot be fixed without breaking the freeze pin — record, don't touch. (Cosmetic `if True:` vestige at the top of `real_arm`, same status.)
- **LOW (provenance).** `c1-after.txt` (and `c2-after.txt`) are **untracked** at review time (`git status --porcelain` → `??`), absent from `bf0df77` and from all history; only the worktree bytes are pinned (sha256 `bdf017cb…`). freeze-v2.txt and the before-receipts are committed. L1 should land the after-receipts with the wave-evidence commit; until then the receipt's provenance rests on this hash.
- **INFO (contract-pin nuance, resolved benign).** Worktree `contract.md` = `065a17b5…` ≠ freeze-v2's `dbd3f6d7…`. Cause: freeze at 12:03:04Z (blob at c1a026cb = the pin), then 5842dc04 appended the 14-line "C1 declared exploratory before data" section. The P-C1 sentence is byte-identical pin→data-commit, and the counter pins (the artifacts the freeze rule protects) match exactly. Consistent with the contract's own declaration text.
- **INFO (verified code nuances, zero effect on this receipt).** (a) `oracle_fresh`/`oracle_drifted` tallies skip the `excerpt` state — here 49+9=58=oracle_fetched, i.e. zero excerpt rows; (b) a row 429'd at any try is excluded even if a later try succeeds (stricter-than-literal, biases *against* passing, documented in `oracle_fetch`); (c) a re-probe-excluded row prints `real_excluded_throttled` but does not increment the `oracle_excluded=` count (contract only requires the print; zero such rows here).

## Residual risk and verification gaps

- The real arm's live-oracle comparison (58 fetches against rate-limited hosts) was **not** re-run — doing so would hammer the hosts and live content may have drifted since; the receipt's real-arm line is accepted on format-exactness, counter-byte identity to the freeze pin, and the seed-reproduced blind arm. This matches the contract's intent to spare those hosts.
- c1-before.txt (`tool_absent / C1=unmet / EXIT=1`, committed at bf0df77) confirms the before state; I did not re-derive it at 6bd57097 (out of seat scope).
- Counter logic beyond the receipt-relevant paths (e.g. full blind-fixture entropy properties) was reviewed by reading, not fuzzed; the C0 25/25 unmet rescore covers control-fitness.

VERDICT: PASS
