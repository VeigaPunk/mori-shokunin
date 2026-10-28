# Mo59Reviewer18 — kill-rule / pinning audit (round 59, w1)

Scope: enumerate every byte the freeze pins vs. every byte `met` depends on at
candidate revision R; find under- or over-pinning. Read-only audit; counters run
only with `--scratch` under `/fast/scratch/hyaku/mori-r59/Mo59Reviewer18`
(now cleaned). Lane worktree verified byte-identical to freeze `60b3a76a` for
contract.md / count-c1.py / count-c2.py (sha256
427fca0b… / 2be6fda8… / 2df3ae84…, `git show 60b3a76a:path` vs `sha256sum`).

## What the freeze actually pins

| Class | Bytes | How pinned |
|---|---|---|
| Kill rule | `contract.md`, `count-c1.py`, `count-c2.py` whole files | "any post-freeze change … invalidates" |
| Inside counter bytes | tool SHAs (`38b733d8…` regcheck, `4c04bf21…` setscan), `MANIFEST_REV=2807c6ab` (fleet commit), `EXPECT_SELFTEST` strings, `BOUND` names, `REQUIRE` keys, `ARTIFACTS`/`REAL_SCAN`/`DRIFT_SCAN` lists, `MIN_CLAIMS=10`/`MIN_FILES=3`, `CLAIM` regex, `FRONTMATTER` keys | transitively frozen (inside counter files) |
| Enumerated at R, **bytes unpinned** | `fixtures-c1/` non-`.py` entries (13 at freeze), `trees-c2/` entries (12 at freeze) | only *existence + expect.txt presence* enforced (`count-c1.py:124-139`, `count-c2.py:320-332`); file contents are read at R |
| Read at R, unpinned | `SCORECARD.md`, `corpus/SOURCES.md`, entry `wave-settlement-artifacts-r59.md`, `corpus/evidence/sources-r59/*`, `.ufo/waves/round-5{3..8}/*` anchor artifacts | nothing |
| External | fleet `MANIFEST.json` @ `2807c6ab` | commit SHA; resolves in fleet repo, ancestor of fleet HEAD (verified) |

## F1 — HIGH: frozen hostile corpus is not byte-pinned; subset deletion is met-invisible

The kill rule names counter bytes, contract bytes, predicate sentence, target
output — it does **not** pin the fixture/tree bytes the counters read at
candidate `R`. Consequences, both directions:

- **Hollowing (met preserved, evidence changed):** a landing may rewrite any
  fixture's `scorecard.md`/`manifest.json` or any tree's entry/copies/registry
  so long as the tool still fails with a reason sharing the frozen family
  prefix (`binding`, `span`, `pin`, `rows:…`). Family prefixes are coarse —
  e.g. `f13-empty-pointer` expect `pointers` is covered by *any* pointer
  failure. The counter cannot distinguish "tool resists the frozen corpus" from
  "tool resists a mutated corpus". Claim text says "frozen expect prefix" and
  "frozen to fail" — the prefixes are frozen, the failing inputs are not.
- **DoS (met broken):** the same mutability lets a hostile landing break an
  honest met by changing one fixture's failure family.
- **Deletion invisibility:** only non-emptiness of the corpus is required
  (`if not dirs:` count-c1.py:128; `if not tdirs:` count-c2.py:323). Deleting
  12 of 13 fixtures or 11 of 12 trees leaves `met` reachable — the contract's
  "13 committed trees"/"12 committed trees" cardinality is unverifiable by the
  counter. (Asymmetric hardening exists only against *additions*: any extra
  entry must itself come with expect + failing tree.)

Fix direction (for integrator): pin the 25 corpus trees by sha in the counter,
or extend the kill rule to `fixtures-c1/` and `trees-c2/` bytes.

## F2 — MEDIUM: C1 is already `met` at the freeze revision itself

Both candidate tools were committed *inside the freeze* (`ccfd554e` adds
`tools/mori-register-check.py` @ `02feb85…` + `tools/mori-settlement-scan.py`
@ `4c04bf21…`; `60b3a76a` amends regcheck to `38b733d8…`=PIN). Measured:

```
$ python3 .ufo/waves/round-59/count-c1.py 60b3a76ad0524c8978cc51922940be1c8c388915 --scratch …/c1-freeze
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76a…   exit 0
$ python3 .ufo/waves/round-59/count-c1.py 2b9f0397… --scratch …/c1-entering
C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f0397… failed=tool_absent,selftest,fixtures_absent,real,pointers   exit 1
```

Every C1 arm (selftest, all 13 fixtures, real register, pointers) passes at the
pre-data revision: the wave cannot *fulfill* C1, only regress it. The claim's
"the lane lands a capability" is satisfied by the freeze commits themselves.
C2 is partially pre-landed: at freeze `selftest=ok scan=ok drift=ok` already;
only corpus arms (`entry/rows/pins/tree/copies`) await wave work. Precedent
exists (round-47 freeze `63eecf27` carried `mori-pin-check.py`), so this is
likely intended freeze-landing practice — flagged so the verdict honestly
describes where the delta sits (freeze, not w1).

## F3 — MEDIUM: C2's "byte-exact pin-bound" anchors float at R

- `tree=ok` checks `sha256(copy)==sha256(artifact)` at R (count-c2.py:267-278).
  Artifact bytes are unpinned: a landing that rewrites `.ufo/waves/round-54/
  w1-results.json` *and* its `sources-r59` copy to the same new bytes passes
  `tree=ok`; claims' `pin <sha64>` self-anchors to the copy. The only
  constraint is the scan arm (the 5 REAL files must still scan OK with
  members==seats) — schema-compatible rewrites evade it. "Pinned to committed
  settlement artifacts" pins *equality*, not *history*.
- `drift=ok` requires only `p.returncode != 0` on the r53 file
  (count-c2.py:258-260). Replacing the drifted r53 artifact with any
  invalid-JSON file satisfies the arm; the contract's stated reason
  ("`report_file` extra keys — schema drift") is unverifiable by the counter.

## F4 — LOW-MED: `grammar:` reasons ignored on the real entry (demonstrated)

`measure()` maps reasons by prefix: `{frontmatter,distinct,claims_min,files,
span,entry_absent}→entry`, `rows→rows`, `pin→pins` (count-c2.py:303-313).
`grammar:` is unmapped, so a malformed claim line in the *landed* entry passes
`entry=ok` — while hostile tree t12 (`expect: grammar`) must fail on the same
defect. Probe (`eval_entry` on a constructed valid root + one malformed claim
line + a junk duplicate S901 row):

```
eval_entry ok=False reasons=['grammar:- **K99** — broken Quote: `x` (…']
REAL-ENTRY MAPPING => entry_ok=True rows_ok=True pins_ok=True
```

Net: the "frozen grammar" the counter enforces on its own hostile corpus is
waived on the artifact the claim is about. Fix: add `grammar` to the `entry`
prefix tuple.

## F5 — LOW: registry-row binding is first-hit-wins + positional

`eval_entry` stops at the first `ROW` match for an SID (count-c2.py:174-178);
a conforming row followed by a `queued`/wrong-`used-by` duplicate is
`rows=ok` (shown in the probe above). Mitigated outside the counter: census
`E03` flags duplicate IDs at round end (`scripts/sources-census.sh:641`), so
the wave-level escape is real but double-gated. Cells `7`/`10` positional
binding is unpinned beyond the 11-cell count — a column reorder at R silently
re-binds.

## F6 — LOW / environmental

`met` requires the fleet repo at default `/home/vgpnk/Projects/shokunin` to
still contain commit `2807c6ab` (reachable ✓). Counter has `--fleet`/`--repo`
overrides, so this is a host assumption, not a byte gap. Scan arm's
`all(members==seats)` is vacuous on an empty `files` list — immaterial since
the tool SHA is pinned (verified `4c04bf21…` at freeze; selftest 10/10).

## Over-pinning

Only granularity: the kill rule pins whole contract/counter files (prose and
docstrings beyond the predicate sentence) — deliberate, standard, benign.
`evidence/*.txt` receipts are frozen bytes no arm requires — informational
over-pin, harmless. Nothing *required* for `met` sits outside the frozen set
except the fleet commit (SHA-pinned) and git/python3 availability.

## Bounded method

- Read contract + both frozen counters in full; mapped every `failed`/reason
  token to its emission site and every arm to its inputs.
- `git show`/`cat-file -e`/`ls-tree` at `60b3a76a`, `ccfd554e`, `2b9f0397`
  (entering ancestor-of-freeze confirmed via `merge-base --is-ancestor`).
- Ran `count-c1.py` at entering (unmet, matches committed do-nothing receipt
  byte-for-byte in shape) and at freeze (met); `count-c2.py` at freeze
  (unmet: corpus arms only); both `--selftest` (6/6, 9/9).
- Direct `eval_entry` probe on a constructed root proving F4+F5.
- Not exercised: full `count-c2.py` at a post-wave landing R (no landing
  exists yet; worktree landing `M corpus/knowledge/…` uncommitted); fleet-repo
  absence scenario for MANIFEST_REV.
- Verdict on freeze self-consistency: counters at `60b3a76a` reproduce both
  frozen selftests and both control shapes; no byte drift vs worktree.

## Summary verdict

Adversarial findings F1–F4 stand: the kill rule under-pins the hostile corpus
and the tested artifacts (F1), C1's after-state is pre-satisfied by the freeze
itself (F2), C2's "byte-exact" anchor and drift rationale float (F3), and the
real-entry arm silently waives the grammar gate its own hostile corpus must
pass (F4). None is a counter-correctness bug under the contract's literal
wording; each weakens what a `met` receipt evidences. F5/F6 are residual-risk
notes. No post-freeze byte drift observed in any frozen file.
