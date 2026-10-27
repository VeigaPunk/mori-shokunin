# Mo58Executor46 — C1 do-nothing: frozen counter at the entering revision

Seat type: executor (leaf). Scope: run the frozen C1 counter / selftest / bounded scratch
fixtures only. No production file edited, no commit, no lane VCS mutation, no fleet or
sibling-repo write. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

- Entering revision: `b783d0b892637ce8d20f188cad20e4d8913ca635`
- Freeze revision: `fe8801120a67c1a6b8899d7d0423839caa09e7d0`
- Lane HEAD at measurement: `4272736cfc5147586e1543413772f80daf44b04b`
- Counter measured: `.ufo/waves/round-58/count-c1.py`
- Frozen blob: `a772d56d1fae83efa4ebeb4fcc515007137ae2ba` — identical at freeze, at HEAD,
  and in the worktree (`git rev-parse` / `git hash-object` agree; `git diff` on that path
  is empty). **No post-freeze mutation of the counter bytes.**

## Headline

**The cheapest no-work state that could meet C1's target is: nothing at all.** The
register rows, the evidence pointers and the MANIFEST binding that C1 measures were
all already in the lane at the *entering* revision `b783d0b8…`. The only artifact C1
actually adds is the counter itself. The counter, run unmodified against the entering
revision, already prints the met line and exits 0.

That is not a defect in the claim — it is exactly what "the lane lands a frozen counter
that VERIFIES the two round-56 admitted capabilities are recorded" means, since the rows
landed in round 57 (`30f5f084`, an ancestor of the entering rev). But it does mean the
counter's *measurement* power, not the counter's *presence*, is the whole of C1, and the
falsification burden falls entirely on the §9 controls and the selftest.

## Exact command, output, exit

Working directory: `/home/vgpnk/Projects/shokunin/mori-shokunin`

### C1 at the entering revision (the do-nothing control point)

```
$ python3 .ufo/waves/round-58/count-c1.py b783d0b892637ce8d20f188cad20e4d8913ca635
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=b783d0b892637ce8d20f188cad20e4d8913ca635
exit=0
```

### C1 at the freeze revision and at the landed tip

```
$ python3 .ufo/waves/round-58/count-c1.py fe8801120a67c1a6b8899d7d0423839caa09e7d0
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=fe8801120a67c1a6b8899d7d0423839caa09e7d0
exit=0

$ python3 .ufo/waves/round-58/count-c1.py 4272736cfc5147586e1543413772f80daf44b04b
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=4272736cfc5147586e1543413772f80daf44b04b
exit=0
```

### Counter selftest

```
$ python3 .ufo/waves/round-58/count-c1.py --selftest
C1_SELFTEST pass=4 fail=0
exit=0
```

### Contract §9 "before" controls, reproduced

```
$ git cat-file -e b783d0b892637ce8d20f188cad20e4d8913ca635:.ufo/waves/round-58/count-c1.py
fatal: path '.ufo/waves/round-58/count-c1.py' exists on disk, but not in 'b783d0b8...'
exit=128                      # counter absent at entering rev — matches contract

$ python3 .ufo/waves/round-57/count-c1.py b783d0b892637ce8d20f188cad20e4d8913ca635
C1=unmet rows=0 evidence=bad rev=b783d0b892637ce8d20f188cad20e4d8913ca635
exit=1                        # known wrong-table false-negative, preserved as contrast

$ python3 .ufo/waves/round-57/count-c1.py 4272736cfc5147586e1543413772f80daf44b04b
C1=unmet rows=0 evidence=bad rev=4272736cfc5147586e1543413772f80daf44b04b
exit=1                        # same false-negative still present at the landed tip
```

### Discriminating negative (rows absent) — the counter is not a constant-met

```
$ python3 .ufo/waves/round-58/count-c1.py 2f1d0c5d4a2bec7345c48d0ddfc138898dd3635d
C1=unmet rows=0 pointers=bad manifest=ok binding=ok failed=rows rev=2f1d0c5d...
exit=1                        # parent of the round-57 row-landing commit; rows absent -> unmet
```

`2f1d0c5d` is the parent of `30f5f084` ("round-57: bind admitted capabilities and recheck
quarantine sources"), which is an ancestor of the entering revision. So the counter does
discriminate on the property it claims to measure; the met-at-entering result is a true
positive, not a stuck green.

## Cheapest no-work state — reproduced end-to-end in an isolated scratch clone

Scratch: `/fast/scratch/hyaku/mori-r58/Mo58Executor46/minimal/lane`, initialized with
`git init` at that explicit path; every git command used `git -C <that path>`;
`git rev-parse --show-toplevel` asserted to that path before committing.

1. Snapshot entering rev `b783d0b8…` into the throwaway repo via `git archive` (commit
   `5ee664d`).
2. Add **only** `.ufo/waves/round-58/count-c1.py` (blob `a772d56d…`, byte-identical to the
   frozen counter). `git diff --name-only` vs the entering snapshot reports exactly one
   path: `.ufo/waves/round-58/count-c1.py`. No SCORECARD.md, MANIFEST.json, corpus, or
   registry edit.
3. Run the counter against that new minimal revision:

```
rev: be66f5e1f57d408e993eec73416393c3c57d5626
rc= 0
out= C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=be66f5e1f57d408e993eec73416393c3c57d5626
```

**Cheapest no-work state = add only the frozen counter; change nothing else.** This is
also what the freeze commit actually did: `git diff --name-only b783d0b8… fe88011…` lists
`contract.md`, `count-c1.py`, `count-c2.py`, `evidence/census-start.txt`,
`evidence/controls.txt`, and **`SCORECARD.md` is byte-identical entering vs freeze**.

Why the register side is already satisfied at entering rev:
- `SCORECARD.md:1953` — the active-register preamble containing the exact sentence
  "the lane's current capabilities register" (the round-35 register).
- `SCORECARD.md:1989-1990` — the two round-56 rows keyed
  `rounds[832].capabilities_added[0]` and `[1]`; 20 `| \`rounds[...]\`` key rows in that
  section (counter requires ≥ 10 for the binding arm).
- All four evidence pointers resolve at entering rev via `git cat-file -e`:
  `tools/mori-vote-bind.py`, `.ufo/waves/round-56/evidence/c2-at-landed.txt`,
  `tools/mori-driver-liveness.py`, `.ufo/waves/round-56/evidence/c1-at-landed.txt` — all rc=0.
- Fleet `MANIFEST.json` `rounds[832].capabilities_added[0]` contains "vote binding" and
  `[1]` contains "driver-liveness" — both hints satisfied.

## Contract §9 do-nothing controls — reproduced independently of the counter's own selftest

I rebuilt the arms from scratch in my own throwaway git repos (own MANIFEST fixture with
`rounds[832].capabilities_added` = the two real hint-bearing strings), importing the frozen
counter module and calling `measure()` with `LANE`/`FLEET` overridden to the fixtures.
All rows below are from arm runs, not from `--selftest`.

| arm | fixture | rc | output |
|---|---|---|---|
| A | only the stub is a `## Capabilities` table | 1 | `C1=unmet rows=0 pointers=ok manifest=bad binding=bad failed=binding` |
| B | two rows, one naming a nonexistent evidence path | 1 | `C1=unmet rows=2 pointers=bad manifest=ok binding=ok failed=pointers` |
| C | conformant active register | 0 | `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none` |
| G | the two rows exist **only** in the superseded stub | 1 | `C1=unmet rows=0 … failed=rows` |
| H | active register with neither row | 1 | `C1=unmet rows=0 … failed=rows` |
| I | duplicate row in the active register | 1 | `C1=unmet rows=3 … failed=rows` |
| K | MANIFEST `rounds[832]` absent | 1 | `C1=unmet rows=2 … manifest=bad failed=manifest` |

Contract §9 arms A and B are satisfied as written: the stub-only fixture scores
`binding=bad` (exit 1) and the nonexistent-evidence-pointer fixture scores
`failed=pointers` (exit 1). Arm G additionally shows the counter refuses to pick the
rows up out of the superseded stub table — the round-57 defect is genuinely fixed, not
merely bypassed.

## Falsification probes that DID produce a green (residual weaknesses)

These are findings about the counter's discrimination, found by probing beyond the
contract's stated arms. Each is a fixture-level result; none is a lane state.

### F1 — pointer resolution only covers three path prefixes (silent skip)

The pointer arm (count-c1.py:110-120) resolves a backticked path only when it starts with
`.ufo/`, `tools/`, or `corpus/`. Any other backticked path is skipped without comment.

```
D_bogus_nonexistent_prefixed_path:  rc=0  C1=met rows=2 pointers=ok …   # `nonexistent/dir/bogus.txt`
E_bogus_bare_name_no_slash:         rc=0  C1=met rows=2 pointers=ok …   # `nonexistent-tool.py`
```

Both fixtures name a path that does not exist in the fixture repo, and both score
`pointers=ok` / `C1=met` / exit 0. The contract's §9 arm B is only triggered because its
sample path happens to be `tools/no-such-tool.py` — i.e. inside a covered prefix. A
nonexistent pointer outside those three prefixes is a silent false green. The two real
round-56 rows only cite `tools/…` and `.ufo/…` paths, so the live claim is unaffected;
the weakness is in the counter's general resolution, and it is exactly the class of
construction the round-57 routed defect 2 was meant to close.

### F2 — MANIFEST binding is a substring hint, not a key binding

Contract C1 requires "each row's key bound to fleet `MANIFEST.json`
`rounds[832].capabilities_added[j]`". The counter instead checks two hardcoded
substrings (`"vote binding"`, `"driver-liveness"`) against the manifest entries
(count-c1.py:29 `MANIFEST_HINTS`, used at :113-118).

```
J_manifest_content_unrelated_hints_only: rc=0  C1=met rows=2 pointers=ok manifest=ok … failed=none
```

A MANIFEST whose `capabilities_added` entries are `"completely unrelated capability
(vote binding of nothing)"` / `"nothing at all here (driver-liveness of nothing)"` scores
`manifest=ok` and `C1=met`, exit 0. Nothing ties the register row's *key* to the
manifest entry — the row key and the manifest check are independent. The real MANIFEST
does carry the right strings, so the live claim holds; the binding is looser than the
predicate sentence describes.

### F3 — MANIFEST is read from the live fleet worktree, not pinned to R

`count-c1.py:111` does `json.load(open(os.path.join(FLEET, "MANIFEST.json")))` — the
working-tree file, with no revision pin and no `git cat-file` resolution. The counter
therefore measures a moving target for the manifest arm: `rounds[832]` is stable today
(fleet `MANIFEST.json` is tracked and clean at `d8ec11dc`), but a counter run against an
old lane revision still consults today's fleet ledger. This is a determinism gap, not a
current miscount.

### F4 — `STUB_MARK` does not match the real stub's punctuation

The counter's stub marker is the ASCII string `"-- none yet --"` (count-c1.py:37), but the
real SCORECARD.md stub at line 600 uses em-dashes: `| — none yet — | | | |`. `grep -c
'-- none yet --'` over the entering-rev SCORECARD.md returns **0**; `grep -c 'none yet'`
returns 2, both em-dash occurrences.

```
L_em_dash_stub_marker_not_detected: rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none
```

A fixture whose active register carries the *real* em-dash stub row alongside the two
conformant rows scores `met`, exit 0 — the stub-refusal arm is inert against the
punctuation the lane actually uses. In the live file the arm is not load-bearing: the
real stub table at `SCORECARD.md:596` also fails the header test (it uses
`| Capability | What it can now do | …`, not `| key | capability |`) and carries no
`rounds[…]` keys, so `_find_register` rejects it on header grounds and arms A/G confirm
the rows are not picked up from it. Still, the intended guard is not the guard that
fires.

### F5 — the contract's frozen target output string cannot be emitted

Contract §C1 declares the frozen target output as:

```
C1=met rows=2 pointers=ok manifest=ok binding=ok selftest=ok rev=R
```

`measure()` never prints `selftest=ok` — the literal string does not occur anywhere in
the counter source (`grep -c 'selftest=ok'` → 0). The actual met line is:

```
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=R
```

Byte comparison of the contract target against the emitted line is **False**. The
selftest verdict is reachable only from the separate `--selftest` invocation
(`C1_SELFTEST pass=4 fail=0`). A literal target-string comparison therefore fails on a
correct counter. This is a contract/reporting inconsistency, not a counter defect; the
frozen predicate and bytes must not be mutated to fix it, so the resolution belongs in
how the target is judged (measure fields from the measure invocation; `selftest=ok`
backed by the separate selftest receipt). `Mo58Critic26` independently reached the same
conclusion on this point; my evidence is the byte-level `target == actual → False` plus
the zero-occurrence grep.

## Bottom line for the L1

1. **Cheapest no-work state**: add only the frozen counter; nothing else. Verified in an
   isolated scratch clone (`be66f5e1…`, rc=0). The counter was already met-at-entering,
   so C1's entire lane-side delta is the counter file — consistent with the freeze commit
   touching only contract/counters/evidence and leaving `SCORECARD.md` byte-identical.
2. **The counter is not a constant green**: it goes `unmet/failed=rows` on the pre-rows
   revision, and `unmet` on stub-only, bad-pointer, absent-rows, duplicate-rows, and
   absent-manifest fixtures. Contract §9 arms A and B reproduce exactly.
3. **C1's met verdict at the entering revision is a true positive**, corroborated by the
   four evidence pointers resolving via `git cat-file -e` and the manifest hints being
   present.
4. **Residual weaknesses (do not invalidate the live claim, but should be routed as
   lessons, not silently dropped)**: F1 pointer-prefix skip, F2 manifest hint-vs-key
   binding, F3 unpinned MANIFEST read, F4 em-dash stub marker inertness, F5 the
   un-emittable `selftest=ok` target token.
5. **Kill rule respected**: the frozen counter blob is `a772d56d…` at the freeze
   revision, at HEAD and in the worktree — identical. `git diff` on
   `.ufo/waves/round-58/count-c1.py` against both freeze and HEAD is empty.

## Files changed

- `.ufo/waves/round-58/w1/Mo58Executor46.md` (this report)
- `.ufo/waves/round-58/w1/Mo58Executor46-evidence/receipt-c1-identity.txt`
- `.ufo/waves/round-58/w1/Mo58Executor46-evidence/receipt-c1-runs.txt`
- `.ufo/waves/round-58/w1/Mo58Executor46-evidence/receipt-c1-fixture-arms.txt`
- `.ufo/waves/round-58/w1/Mo58Executor46-evidence/receipt-c1-minimal-nowork.txt`
- `.ufo/waves/round-58/w1/Mo58Executor46-evidence/c1-entering-stdout.txt`

No production file, corpus registry, SCORECARD, LOG, or lane VCS state was touched. No
commit. Scratch root `/fast/scratch/hyaku/mori-r58/Mo58Executor46/` cleaned before yield.
