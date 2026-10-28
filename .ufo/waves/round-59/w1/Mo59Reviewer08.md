# Mo59Reviewer08 — C2 quote-span attack (adversarial)

Seat: reviewer (attack). Scope: C2 claim-quote mechanics in the frozen counter
`.ufo/waves/round-59/count-c2.py` @ `60b3a76ad0524c8978cc51922940be1c8c388915`
(same bytes at HEAD `8ff344ff18924c1ea63d46c3b3969f9fea05bc51`; counter
selftest `C2_SELFTEST pass=9 fail=0` run from the frozen file, exit 0).
Assigned vectors: (a) byte-exact quote against the WRONG artifact (same text in
two artifacts), (b) quote spanning a `\n` boundary via `offset`, (c) quote
containing a backtick. Result: **one genuine counterexample** (grammar-rejected
claim lines score `C2=met` end-to-end) plus two predicate-coverage notes;
vectors (b) and the forgery half of (a) are robustly rejected — bounded
no-counterexample.

All construction under `/fast/scratch/hyaku/mori-r59/Mo59Reviewer08/` (TMPDIR
set there; scratch cleaned after this receipt was copied). Lane untouched
except this report; fixture repos were throwaway under scratch only.

## Method

1. Read `contract.md`, `count-c1.py`, `count-c2.py` (freeze rev) fully.
2. `eval_entry` is the shared evaluator: live entry arm and all 12 hostile
   trees route through it. The live arm, however, does not use `eval_entry`'s
   boolean — `measure()` lines 303–307 partition the *reason list* into
   `entry_ok` / `rows_ok` / `pins_ok` by prefix.
3. Materialized real artifacts `git show HEAD:.ufo/waves/round-{54..58}/w1-results.json`
   + `round-53` + `round-58/evidence/w1-settlement.json` into scratch
   (LF-terminated JSON, 150–390 KB, 0 CR bytes).
4. Built a throwaway fixture repo under scratch with every input the counter
   needs — real tool (`sha256 == PIN 4c04bf21…` verified), real artifacts at
   `.ufo` paths AND `corpus/evidence/sources-r59/` copies, all 12 hostile trees
   verbatim, a fabricated 11-cell `SOURCES.md` S901 row — and three committed
   revisions: clean entry, +malformed-claim entry, +backtick-claim entry. Ran
   the frozen `count-c2.py` itself with `--repo <fixture>`. This exercises the
   real `measure()` partition, not a copy of it.

## Finding F1 — ADVERSARIAL, confirmed end-to-end: `grammar:` reasons are unrouted in `measure()`; malformed claim lines score `C2=met`

`eval_entry` (counter lines 88–96) emits `grammar:` for every claim-shaped
line that fails the frozen `CLAIM` regex — this is hostile tree **t12's frozen
reject class** (`trees-c2/t12-malformed-claim/expect.txt` = `grammar`,
verified: `git show HEAD:.ufo/waves/round-59/trees-c2/t12-malformed-claim/expect.txt`
→ `grammar`; `eval_entry` on the committed tree →
`['grammar:- **K5** — claim 5. Quote: ` "seats": 3,', 'claims_min:9']`).

But `measure()` lines 303–307 routes only
`frontmatter|distinct|claims_min|files|span|entry_absent` → `entry`,
`rows` → `rows`, `pin` → `pins`. **`grammar:` reaches no arm** — `eval_entry`
returns `ok=False` yet the live entry verdict is `entry_ok=True`, and `met`
(counter line 360) is unaffected. Audit of every prefix `eval_entry` emits:
`frontmatter|grammar|distinct|claims_min|files_min|files|pin|span|rows` —
`grammar` is the only dead end; the `ok` boolean itself is unused by `measure`.

End-to-end receipts (real counter, real artifacts/trees, fixture repo):

    # fixture rev d7ac24db — clean 10-claim entry (control)
    $ python3 .ufo/waves/round-59/count-c2.py d7ac24db70a1a70ae281e52c53dc1b6866440ca1 \
        --repo <fixture> --scratch <scratch>/measure-A
    C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=10 files=3 rev=d7ac24db…   exit 0

    # fixture rev 4a0f828c — identical entry + K11 missing its '; pin' tail
    # (exactly t12's frozen reject class)
    C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=10 files=3 rev=4a0f828c…   exit 0

    # fixture rev 0ba7c7cd — identical + K12 quote containing a backtick
    #   - **K12** — c12. Quote: ` "a`b",` (…w1-results-r56.json:line:2; pin 1953…)
    C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=10 files=3 rev=0ba7c7cd…   exit 0

So a landed entry may carry arbitrarily malformed claim lines — including
content that looks like a claim but evades every pin/span check — and the
counter emits the frozen `C2=met` target with zero diagnostic (`failed=`
absent, `claims=` counts only well-formed lines). The counter defines t12 as
the canonical "malformed claim" reject and then accepts that same defect in
production. Fix shape (informational only; frozen bytes are immutable this
round): add `"grammar"` to the `entry_ok` prefix tuple at line 304, or gate
`entry_ok` on `eval_entry`'s boolean.

Severity: medium-high within counter scope — accept-should-reject, no
diagnostic channel, and it silently converts a frozen reject class into a
live accept. It cannot inflate `claims=` (dropped lines are not counted), so
it cannot manufacture the ≥10 floor, but it lets a malformed entry ship clean.

## Assigned-vector verdicts

### (a) Byte-exact quote against the wrong artifact — PASS by design (provenance not bindable); divergent wrong-file and pin-swap FAIL correctly

- `' "lane": "mori",'` is byte-identical at **line 2** in all five committed
  r54–r58 artifacts (`' "seats": 64,'` identical at line 5 in r55–r58;
  `' "wave": "w1",'` at line 4, `' "results": ['` at line 6 in all five).
  Entry citing `w1-results-r54.json:line:2` with r54's pin while the claim
  prose asserts round-56 provenance: `eval_entry=True`, `entry_ok=True` —
  **vacuously correct**: every frozen check (byte-equality to cited line,
  pin = cited copy's sha) is true. Provenance/intent is not observable by any
  byte-bound counter. → spec-level note, not a counterexample.
- Quote unique to the *other* file cited against the wrong file
  (`"seats": 64,` in r56 only, cited `r54:line:5` where r54 has `"seats": 74,`):
  `eval_entry=False`, reason `span:1`, `entry_ok=False` → **correctly rejected**.
- Cited file carrying another file's pin (r55 copy + r56 sha):
  `eval_entry=False`, reason `pin:1`, `pins_ok=False` → **correctly rejected**.

### (b) Quote spanning a `\n` boundary via `offset:` — unforgeable, correctly bounded

- Quotes come from `read_text().splitlines()` — no `\n`, `\r`, or other
  split boundary can ever occur inside a claim line, hence never inside
  backticks. Any `fb[n:n+len(q)]` slice that crosses a `\n` necessarily
  contains a byte the quote lacks → `span:` mismatch.
- Observed: literal `\n` inside backticks splits into two lines; neither
  parses → `grammar:` + `claims_min:9` → `eval_entry=False`,
  `entry_ok=False` (via `claims_min`) → correctly rejected.
- Boundary-adjacent is legal and passes: `i",` at `offset:15` in r56
  (`bytes[15:18]=b'i",'`; `bytes[18]=b'\n'`) → `eval_entry=True`. A quote may
  end exactly at the newline; it can never include it. Shortest legal quote
  is 3 bytes (`len(q)<3 → span:short`), which also blocks squeezing across
  (the 2-byte `",` at offset 16 → `span:short=2` → rejected).
- Structural caveat: `kind=line` reads `fb.split(b"\n")`, so a CRLF artifact
  line carries a trailing `\r` that a quote can never contain → line-kind
  claims are unquotable on CRLF artifacts (offset-kind remains). All five
  committed artifacts are LF (verified, `grep -c $'\r'` = 0) — latent only.

### (c) Quote containing a backtick — correctly rejected by grammar; but see F1

`[^`]+` in `CLAIM` cannot span a backtick, so the line fails to parse →
`grammar:` reason → `eval_entry=False` (hostile-tree verdict: reject).
Against the **live** arm, per F1: `entry_ok=True` and end-to-end `C2=met`.
The reject machinery works; its reason is simply dropped by the live
partition.

## Predicate-coverage notes (spec-level, not defects vs. the frozen letter)

- **Duplicate-content claims pass**: ten claims quoting the identical span
  (`' "lane": "mori",'` at line 2, across three files) with distinct K-ids →
  `eval_entry=True`, `claims=10`, `files=3`. Frozen predicate requires
  "all K ids distinct" — only key distinctness is checked; an entry can
  satisfy ≥10 claims with one unique byte-string. Contract's "distinct
  claims" intent (round-58 routed defect #4) is enforceable only as K-id
  uniqueness at counter level.
- **`eval_entry`'s `ok` boolean is dead code on the live path** — the
  partition recomputes per-arm verdicts from reasons. Combined with F1,
  the tree arm and live arm disagree on identical input by construction.

## Bounds / gaps

- Lane HEAD `8ff344ff` has the PIN'd tool but no landed C2 entry or
  `sources-r59/` copies yet (pre-data); end-to-end proof therefore ran on a
  scratch fixture repo containing the *committed* tool/artifacts/trees —
  `measure()` executes identically (`git show` against any repo), and the
  clean control produced the exact frozen target line.
- Did not test `count-c1.py` or the scan/drift arms' internals beyond their
  `ok` in fixtures (out of seat scope; sibling seats cover the tool).
- No tools installed; no installs needed (python3 + git only).
