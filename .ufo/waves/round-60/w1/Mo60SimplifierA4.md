# Mo60SimplifierA4 — builder audit: h04 double-replace leftover + expect/EXPECTS duality

Read-only audit of `.ufo/waves/round-60/build-fixtures-r60.py`. Nothing in the lane was
modified; all patch experiments ran on scratch copies under
`/fast/scratch/hyaku/mori-r60/Mo60SimplifierA4/`.

## Pins used

| item | value |
|---|---|
| lane tip at audit | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| amended freeze | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| builder blob at freeze = at tip | `243da06a0ef36d98e7ac445580d5d0716f7146bb`, sha256 `2343b46d837ccb826d1267f5f38fa40b0d4cb94fefd33b39dc87f549ef2b5970` |
| `trees-c2h` tree at freeze = at tip | `fc3703949d493097cba8134da3aecd116c6a8e6a` |
| `trees-c2h-expects.json` at freeze = at tip | `e190b617cc69ae2dc83cc7d0a3b09ed44cd3c785` |

```
$ git rev-parse ac496c7c:.ufo/waves/round-60/build-fixtures-r60.py HEAD:...
243da06a0ef36d98e7ac445580d5d0716f7146bb
243da06a0ef36d98e7ac445580d5d0716f7146bb
$ diff -r <fresh build> .ufo/waves/round-60/trees-c2h   → empty; "TREES_IDENTICAL"
$ cmp <fresh build>/.ufo/waves/round-60/trees-c2h-expects.json ...  → "EXPECTS_JSON_IDENTICAL"
```

Fresh build in scratch: `trees=13 expects=13`, rc=0, 117 files (matches committed).

## F1 — h04 double-replace leftover (confirmed dead; delete 2 lines)

Builder lines 185-204, h04 block. After `write_tree` (L192-193) the entry is read back,
re-pinned twice, and rewritten:

```
194     # rebuild claims with the extended blob's pin
195     d = OUT / "h04-blank-quote"
196     ep = (d / ENTRY).read_text().splitlines()
197     ep = [ln.replace(pin1, sha(blobs4[C1])) if "`pin" not in ln else ln
198           for ln in ep]
199     # (pins in claims must match the extended blob)
200     fixed = []
201     for ln in ep:
202         fixed.append(ln.replace(pin1, sha(blobs4[C1])))
203     (d / ENTRY).write_text("\n".join(fixed))
```

Proof the L197-198 pass is a no-op on top of L200-202:

* the guard `if "`pin" not in ln` never fires: `0 of 18` lines contain the substring
  `` `pin `` (claim format emits `; pin <sha>)`, no backtick before `pin`), so L197-198
  performs exactly the replacement L202 performs again;
* replacements are idempotent (`pin1` is absent after the first pass), so first pass +
  second pass == single pass.

Removing **only L197-198** (270 → 268 lines) reproduces the frozen artifact exactly:

```
$ python3 build-min.py            → trees=13 expects=13
$ diff -r run-min/.ufo/.../trees-c2h .ufo/.../trees-c2h  → empty  "MIN_PATCH_TREES_BYTE_IDENTICAL"
$ cmp run-min/.../trees-c2h-expects.json ...             → equal  "MIN_PATCH_EXPECTS_IDENTICAL"
$ python3 -m py_compile build-min.py                     → COMPILES
```

Verdicts also unchanged when the patched tree is fed to the lane verifier:

```
h00-good-control      ok=True   reasons=[]
h04-blank-quote       ok=False  reasons=['span:blank=K1']
h01-semantically-empty ok=False reasons=[... 'text:short' ..., 'distinct:dup_span=K1=K2' ...]
```
(expected prefixes `""`, `span:blank`, `distinct:dup_span`+`text:short` all satisfied.)

Side effect that the deletion *keeps*: the read-modify-write at L203 is the only writer
that uses `"\n".join(...)`, so h04's entry is the one tree without a trailing newline
(`lastbyte=0x29`; the other 12 are `0x0a`). Byte-identical repair means keeping that.
A root fix that removes the read-back (below) restores `0x0a` and therefore changes the
frozen tree hash.

## F2 — expect/EXPECTS duality (dead parameter; keep the dict)

`write_tree` carries two authorities for one value:

```
126 def write_tree(name, entry_text, registry_text, extra_copies=None,
127                expect=(), blobs=None):
...
140     (d / "expect.txt").write_text(",".join(EXPECTS.get(name, expect)) + "\n")
```

AST over the whole file: **`calls passing expect=: NONE`**; all 13 call sites (L151, 162,
169, 181, 192, 211, 222, 230, 235, 240, 248, 255, 261) set `EXPECTS[name]` immediately
before, so `EXPECTS.get(name, expect)` always hits and `expect` is unreachable.

Provenance: contract.md, Amendment 1 — "the fixture builder wrote empty expect.txt files
because it never passed the frozen expects into `write_tree`". The fix added *both* a
per-call parameter and the dict; the parameter was never used. The dict is the load-bearing
one (it is serialized to `trees-c2h-expects.json`, and `count-c2.py:83-97` FROZEN_EXPECTS
plus the `expect.txt` comparison at `:358-365` mirror it), so the parameter is the side to
delete.

Hazard of keeping `.get(name, expect)`: a future tree that forgets its `EXPECTS` row gets
`expect.txt == "\n"`, i.e. it silently asserts "this tree must verify" (false-negative
direction). Demonstrated:

```
$ write_tree('h99-forgotten', ...)   (current builder)
current builder wrote expect.txt = '\n' (empty => tree asserts "must verify")
$ write_tree('h99-forgotten', ...)   (with EXPECTS[name])
KeyError: 'h99-forgotten'
```

Second line of defence exists but is in the counter, not the builder: `count-c2.py:348-350`
fails `trees_set` when the committed dir set differs from FROZEN_EXPECTS, and `:358-365`
flags `expect_tamper`. So today the mistake is caught at count time; deleting the parameter
moves the failure to build time.

## F3 — two more dead parameters

* `extra_copies=None` (L126): never referenced in the body, no call passes it
  (`calls passing extra_copies: NONE`) — leftover from an aborted extra-copy path.
* `good_registry(..., full=True)` (L112) with `cells = cells[:9]` (L121): no call passes
  `full` (12 call sites, only `[]`, `mined`, `usedby`). The 9-cell branch is unreachable.
* `write_tree` returns `name` (L142); every call site discards it.

## F4 — documentation drift in `good_claims`

Docstring (L87) says "Distinct spans (lines 2..4 …)" but the loop is
`enumerate(lines[rel], start=3)` → emitted line numbers are 3, 4, 5:

```
$ emitted claims: w1-results-r54.json line 3/4/5, r55 3/4/5, r56 3/4/5, r57 3
```
Cosmetic, but the docstring is the only place that states the span policy.

## F5 — second authority for the same bytes (drift risk, currently equal)

`good_claims` L89-95 hardcodes the three quoted lines per copy as literals instead of
deriving them from `BLOBS` (L43). They are currently identical:

```
$ hardcoded lines == derived from BLOBS: True      # BLOBS[rel].split(b"\n")[2:5]
```

If a future edit changes a `BLOBS` line without the literals (or vice versa), every tree
silently flips to `span:` reasons and `h00-good-control` stops verifying. One derivation
removes the second authority at zero byte cost.

## F6 — dead fixture data (deletion candidate; needs re-freeze, verdict-neutral)

`ART` (L30) and `BLOBS` (L43) carry 6 copies; `REG_COPIES` (L62) has 4. The two r58 copies
(`w1-results-r58.json`, `w1-settlement-r58.json`) are materialized into every tree but are
never cited:

```
$ grep -rl r58 .ufo/waves/round-60/trees-c2h → (none)
$ cited copies across all 13 trees: r54, r55, r56, r57   (10 claims: 3/3/3/1)
```

They cannot be load-bearing: the verifier caches every `artifacts-json` key
(`tools/mori-entry-claims-check.py:102-106`), but only cited copies reach `files:outside`
(`:143`) and row binding iterates `cited_copies` (`:234-238`); a missing, uncited copy
yields `cache=None` and no reason. Cost: 26 of 117 tree files (22%).

Not proposed as the *minimal* cleanup: removing them rewrites `trees-c2h` and the frozen
tree hash for zero verdict change, so it belongs to a re-freeze slot (same class as F1's
root fix), not to a "delete dead weight now" move.

## Minimal cleanup for a future builder (patch, not applied)

Byte-preserving set, in order of value per line deleted:

1. **F1** delete L197-198 (2 lines) — the always-true re-replace pass.
2. **F2** signature `def write_tree(name, entry_text, registry_text, blobs=None):` and
   `EXPECTS[name]` at L140 — one table, build-time KeyError instead of a silent empty
   expect.
3. **F3** drop `extra_copies` (same signature line), drop `full`/`cells[:9]`
   (L112, L121), drop `return name` (L142).
4. **F5** hoist the four cited copies into one constant and derive the quotes, e.g.
   `CLAIM_COPIES = (C1, C2, "corpus/evidence/sources-r59/w1-results-r56.json",
   "corpus/evidence/sources-r59/w1-results-r57.json")` then
   `lines = {rel: BLOBS[rel].split(b"\n")[2:5] for rel in CLAIM_COPIES}`;
   fix the L87 docstring to "lines 3..5".

Combined F1+F2+F3 experiment (scratch `build-patched.py`, 270 → 263 lines) also produced
`PATCHED_TREES_BYTE_IDENTICAL` / `PATCHED_EXPECTS_IDENTICAL`, so 2-4 are byte-neutral both
alone and together.

Root fix, explicitly **not** minimal (changes 1 byte → re-freeze): thread the extended-blob
pin into claim construction and write h04 once, e.g.
`claims = good_claims(pins={C1: sha(blobs4[C1])})` with `claim(..., pin4)`, then delete
L194-203 entirely. Verified equivalent modulo the newline:
`C' == committed + "\n"` and `committed == C' .rstrip`.

Freeze note: the builder is named by the contract (`contract.md:85`) and pinned at
`ac496c7c`; all of the above is for a *future* round's pre-data freeze, never mid-round.

## Preserved contract

* `trees-c2h` bytes (117 files), `trees-c2h-expects.json`, all 13 `expect.txt`, and the
  h00/h01/h04 verifier verdicts are unchanged under F1 and under F1+F2+F3.
* No predicate, reason prefix, or expect entry is touched by any proposal here.
* F6 preserved rather than acted on, because acting costs a re-freeze.

## Tradeoff

The smallest deletion (F1) leaves the h04 entry without a trailing newline and leaves the
read-modify-write structure in place; the structurally clean fix (single write, threaded
pin) buys consistency at the price of a one-byte change in a frozen artifact. Given the
freeze, F1 now / single-write next freeze is the correct split.
