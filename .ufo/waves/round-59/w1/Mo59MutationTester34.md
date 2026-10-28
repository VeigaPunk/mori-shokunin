# Mo59MutationTester34 — entry-grammar regex mutation test (C2 counter)

Seat: mutation-tester, round 59 wave w1. Read-only on the lane; all mutations
on scratch copies. No production edits, no commits, no fleet/sibling writes.

## Target and freeze identity

Entry grammar regex of the frozen C2 counter, `count-c2.py:78-80`:

```python
CLAIM = re.compile(
    r"^- \*\*K(\d+)\*\* — .+? Quote: `([^`]+)` "
    r"\((\S+?):(line|offset):(\d+); pin ([0-9a-f]{64})\)\s*$")
```

Frozen predicate grammar (contract.md §C2):
``- **K<d>** — <text>. Quote: `<q>` (<file>:line:<n>|offset:<n>; pin <sha64>)``

- Working-tree counter sha256 `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be`
  == `git show 60b3a76ad0524c8978cc51922940be1c8c388915:.ufo/waves/round-59/count-c2.py`
  (frozen bytes confirmed before testing).
- Baseline behavior reproduced: `python3 count-c2.py 2b9f03975bfb6e508f35074ac8181ec8bf54e805
  --scratch $S/base` → `C2=unmet … failed=…tool_absent…`, exit 1 (frozen do-nothing control);
  `--selftest` → `C2_SELFTEST pass=9 fail=0`, exit 0.

## Method (bounded)

Scratch: `/fast/scratch/hyaku/mori-r59/Mo59MutationTester34/` (disk guard green,
592.6G free on /fast/scratch/hyaku). TMPDIR set there; `--scratch` passed.

1. **Regex probe battery** (`probe.py`): 10 adversarial claim lines vs `CLAIM.match`.
2. **End-to-end battery**: synthetic roots (3 crafted artifact copies, valid
   frontmatter, valid mined S-row with `used-by` = entry) run through the
   counter's own `eval_entry` — same behavioral detector the counter uses in
   `measure()`. Control E1 (grammar-true claims) returns `ok=True`, proving the
   harness; each adversarial family then tested with all spans byte-true.
3. **Mutation battery**: five single-point regex mutants on scratch copies
   (`cp` of pristine, then one edit each). Same detector run on pristine,
   mutated, and restored bytes: `--selftest` + `probe.py` per copy.
4. Restoration: fresh copy re-taken from the lane after the battery
   (`restored.py`), selftest re-run, probe profile compared by md5.

## Findings — constructs the grammar accepts that should not parse

**F1 (headline). Missing `.` before ` Quote:` — accepted end-to-end.**
The frozen grammar requires `<text>. Quote:`; the regex `.+? Quote:` never
checks the period. Entry of 12 claims `- **K11** — claim 0 Quote: `…`` →
`eval_entry` returns `ok=True claims=12 reasons=[]` (E2). The counter would
MET an entry whose claims violate the predicate's frozen grammar.
Mutant M2 (regex tightened to `.+?\. Quote:`) **survives**: `--selftest`
still `pass=9 fail=0` exit 0 → the frozen selftest + 12 hostile trees cannot
see the difference. Detector-grammar mismatch is provably unobserved.

**F2. Quote may embed `; pin <64hex>` (any `;`) — accepted.**
`- **K12** — t. Quote: ` "seats": 2,; pin bbbb…` (…:line:2; pin aaaa…)` parses
with quote = `" "seats": 2,; pin bbbb…"` (P2). End-to-end accept proven (E5,
`ok=True`, offset span into an artifact whose bytes contain the embedded
clause). Downstream the span check stays byte-binding, so F2 alone does not
forge a claim — but the grammar cannot delimit `<q>` against an embedded pin
clause, and mutant M3 (`[^`;]+`) **survives** the frozen detector
(`pass=9 fail=0`; E5 flips ok=True→False only under the mutant).

**F3. Unicode decimal digits in `<d>`/`<n>` — accepted end-to-end.**
Python `\d` matches Unicode Nd and `int()` maps them: `(…:line:٢; pin …)`
parses with n=`'٢'`, `int(n)==2`, span check passes against line 2 (P5, E3
`ok=True`). K-ids too: `**K١٢**` parses (P4). Distinctness is keyed on the raw
text (`seen[kid]`, count-c2.py:127): an entry carrying both `**K13**` and
`**K١٣**` yields 13 claims, **no `distinct:` reason**, `ok=True` (E4) — two
numerically identical ids pass the "all K ids distinct" predicate as distinct.
Mutant M4 (`[0-9]+` for both groups) **survives** (`pass=9 fail=0`; E3 drops
to 8 claims + grammar reasons, E4 gains one grammar reason, only under the
mutant).

**F4 (minor laxities, all regex-accepted, all unobserved by the detector).**
`line:002` (leading zeros, P8); a second `**K19** —` label swallowed by `.+?`
(P10 — text may contain another full K-label); trailing whitespace after `)`
(P11). Mutant M5 (drop `\s*`) **survives** (`pass=9 fail=0`).

**Negative control — the em dash IS pinned.** `-` (hyphen) and `–` (en dash)
in place of `—` are rejected and hit the near-miss heuristic
(`count-c2.py:121` → `grammar:` reason). Mutant M1 (em dash → hyphen) is
**killed**: `C2_SELFTEST pass=6 fail=3` (`FAIL claim_grammar`,
`FAIL claim_grammar_offset`, `FAIL synth_good`), exit 1. The seat hint
"`—` vs `-`" is therefore already covered; the unguarded laxities are F1–F4.

Note: the only grammar-reason hostile tree is t12-malformed-claim
(expect `grammar`), whose malformed construct is a **missing `; pin …`** —
none of F1–F4 is covered by any of the 12 frozen trees.

## Mutation table

| Mutant | Single-point change | Expected detector | Observed | Verdict |
|---|---|---|---|---|
| M1 | `— ` → `- ` (m1.py:79) | selftest kills | `pass=6 fail=3`, exit 1; probe flips to ACCEPT P6 | **killed** |
| M2 | `.+? ` → `.+?\. ` (m2.py:79) | selftest/trees | `pass=9 fail=0`, exit 0; only E2 flips ok=True→False | **survived** (F1 gap) |
| M3 | `([^`]+)` → `([^`;]+)` (m3.py:79) | selftest/trees | `pass=9 fail=0`, exit 0; only E5 flips | **survived** (F2 gap) |
| M4 | `\d+` → `[0-9]+` ×2 (m4.py:79-80) | selftest/trees | `pass=9 fail=0`, exit 0; only E3/E4 flip | **survived** (F3 gap) |
| M5 | `\)\s*$` → `\)$` (m5.py:80) | selftest/trees | `pass=9 fail=0`, exit 0; only P11/trailing-space flips | **survived** (F4 gap) |

## Restoration evidence

- Pristine scratch copy before battery: `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be`.
- Lane file after battery: same sha256; fresh re-copy `restored.py`: same sha256.
- Restored-bytes detector: `C2_SELFTEST pass=9 fail=0`, exit 0.
- Probe profile identical pristine vs restored (ACCEPT/REJECT lines md5
  `cc1eb01e71b90df2b40ad43a446c79d6` both).
- Lane `git status --porcelain` after work: only pre-existing L1/other-seat
  wave paths (`LOG.md`, `SHONEN.md`, `corpus/QUALITY.md`,
  `w1.ready.dispatched`, `w1/`, `corpus/lessons/round-59.md`) — frozen
  counters/contract/fixtures/trees untouched; mutants lived only under the
  scratch dir.

## Verdict

Adversarial finding (not a no-counterexample result): the frozen C2 entry
grammar verifies a slightly **looser** language than the predicate sentence —
F1 (missing period) and F3 (Unicode digits + lookalike-id distinctness bypass)
accept end-to-end through the counter's own `eval_entry`; F2 (`; pin ` inside
quote) and F4 (leading zeros, nested K-label, trailing whitespace) are
regex-level accepts. All four laxities are provably invisible to the frozen
selftest and the 12 hostile trees (surviving mutants M2–M5). Per the frozen
kill rule these are recorded findings only — no counter or contract bytes
changed, no remediation attempted.
