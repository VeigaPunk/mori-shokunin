# Mo59Simplifier64 — fixtures-c1 / trees-c2 duplication and gap review (round 59)

Seat: simplifier, leaf. Read-only on the lane: `git show` / `git ls-tree` / file reads plus
two throwaway repos under my own scratch. No production, corpus, SCORECARD, LOG, lane-VCS or
fleet write; the only file I created in the lane is this report.

Question asked: do `fixtures-c1` (13 trees) and `trees-c2` (12 trees) duplicate coverage, and
which obvious cases are missing (e.g. **empty evidence cell vs absent evidence column**)?

## Verdict

No counterexample flips a *frozen* fixture or tree from UNMET to MET: all 13 C1 fixtures and
all 12 C2 trees fail for their frozen expect prefix on the committed bytes, and both counters'
selftests pass (`C1_SELFTEST pass=6 fail=0`, `C2_SELFTEST pass=9 fail=0`). But three
counterexamples do land on **the counters' own arms**, and the fixture/tree sets leave a
reachable, named gap:

1. **Roster vacuity (C1).** `fixtures=ok` is satisfiable with **1 of 13** fixtures present.
2. **Roster vacuity (C2).** `trees=ok` is satisfiable with **1 of 12** trees present.
3. **"Distinct claims" is only distinct K ids (C2).** An entry with 10 claims over **3 distinct
   spans** (each repeated 3–4×) scores `C2=met … claims=10 files=3`.
4. **`f11` is mislabelled and duplicates `f10`+`f12`; its stated class is unreachable.**
5. **The `keys:short_row` class (row with the evidence column absent) has no fixture at all** —
   this is the exact complement of `f13-empty-pointer` (evidence cell present but empty).
6. Under-enforced expect tokens (`pointers`×4, `manifest:lane` ⊂ `manifest:lane_round`,
   `span` ⊃ `span:short`, `files` ⊃ `files_min`, `keys` ⊃ `keys:*`).

## Method (bounded, reproducible)

All commands from `/home/vgpnk/Projects/shokunin/mori-shokunin` unless shown otherwise; scratch
`/fast/scratch/hyaku/mori-r59/Mo59Simplifier64` (mkdir -p, TMPDIR set). Disk guard checked green
first (`27%`, 592.6G free). Two sandbox repos were created with
`D=$(mktemp -d -p $SCRATCH c1repo.XXXX) && git -C "$D" init -q`, `git rev-parse --show-toplevel`
asserted = `$D`, all git calls `git -C "$D"`. Nothing was committed anywhere else.

Arms exercised: both frozen selftests; per-fixture reason sets (tool run directly on
materialized fixture dirs); per-tree reason sets (`importlib` load of the frozen
`count-c2.py` → `eval_entry`); six C1 mutation probes; five C2 mutation probes; two end-to-end
sandbox counter runs with roster deletion; one duplicate-span entry.

## Frozen baseline (what the committed sets actually do)

```
$ python3 .ufo/waves/round-59/count-c1.py --selftest   # C1_SELFTEST pass=6 fail=0, exit 0
$ python3 .ufo/waves/round-59/count-c2.py --selftest   # C2_SELFTEST pass=9 fail=0, exit 0
```

Per-fixture reasons (tool `tools/mori-register-check.py`, sha `38b733d8…472b8` matches
`count-c1.py:PIN` at freeze `60b3a76a`):

| fixture | expect | achieved reasons |
|---|---|---|
| f01-stub-only | binding | `binding:declared_register=0(capabilities_sections=1)`, `keys:missing=…[0]`, `keys:missing=…[1]` |
| f02-two-declared | binding | `binding:declared_register=2(capabilities_sections=3)`, `keys:missing=×2` |
| f03-dup-key | keys | `keys:duplicate=…[0]`, `manifest:name=…[0]` |
| f04-missing-key | keys | `keys:missing=…[1]` |
| f05-pointer-missing | pointers | `pointers:missing=.ufo/…/c2-at-landed.txt` |
| f06-pointer-absolute | pointers | `pointers:bad=/etc/passwd` |
| f07-pointer-relative-parent | pointers | `pointers:bad=../../etc/passwd` |
| f08-manifest-name-altered | manifest:name | `manifest:name=…[0]` |
| f09-manifest-substring-only | manifest:name | `manifest:name=…[0]` |
| f10-manifest-foreign-lane | manifest:lane | `manifest:lane='kotoba'` ×2 |
| f11-manifest-wrong-index | manifest | `manifest:lane=None`, `manifest:entry_missing=…[0]`, `manifest:lane_round=…[0]`, (same ×2 for [1]) |
| f12-lane-round-mismatch | manifest:lane_round | `manifest:lane_round=…[0]`, `…[1]` |
| f13-empty-pointer | pointers | `pointers:none=…[1]` |

Per-tree reasons (`count-c2.py:104-191 eval_entry`): each of the 12 trees emits exactly its own
class, with two trees carrying an extra incidental reason (`t01` + `rows:no_source_ids`,
`t12` + `claims_min:9`).

## Findings

### F1 — C1 fixture roster is not pinned; `fixtures=ok` is vacuous (highest severity)

`count-c1.py:124-127` enumerates `git ls-tree rev:FIXDIR`, keeps every entry that does not end in
`.py`, and only requires the list to be non-empty (`if not dirs: failed.append("fixtures_absent")`).
No name list, no count, no expect-byte pin. The contract says 13 committed trees (§ C1 "Hostile
fixtures (§9, 13 committed trees …)") and the frozen target output is
`… fixtures=ok …`.

Demonstration (sandbox repo holding only the tool, the real `SCORECARD.md`, the two pointer
files, and a copy of the 13 fixtures; `--repo $D --fleet /home/vgpnk/Projects/shokunin`):

```
13 fixtures rev=b7a29f06…  C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=b7a29f06…  exit=0
12 fixtures rev=e799a497…  C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=e799a497…  exit=0   # after git rm f09
 1 fixture  rev=b0d0fea3…  C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=b0d0fea3…  exit=0   # only f13 left
```

The whole frozen target line is reproduced verbatim with 12 of 13 hostile fixtures deleted, and
again with only `f13-empty-pointer` present. The kill rule ("any post-freeze change to counter
bytes, contract bytes, predicate or target output") does not fire: deleting fixture bytes leaves
the counter bytes and the printed output unchanged. So `fixtures=ok` does not witness the
thirteen fixture classes; it witnesses "≥1 directory that happens to fail". Same shape for
`expect.txt`: an empty expect file yields `expect = ['']` (`count-c1.py:140`), and
`r.startswith('')` is true for any reason, so a fixture with an empty expect passes on any
failure.

### F2 — C2 tree roster is not pinned either

`count-c2.py:319-325` has the identical construction (`git ls-tree rev:TREES`, `if not tdirs:
failed.append("trees_absent")`). Sandbox repo with a met-able entry (10 claims / 3 real copies),
the 5 real wave-results files, the r53 drift file, and the 12 trees:

```
12 trees rev=aa5fae57…  C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=10 files=3 rev=aa5fae57…  exit=0
 1 tree  rev=aad2970c…  C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=10 files=3 rev=aad2970c…  exit=0   # only t01 left
```

`trees=ok` with 1 of 12 present. Eleven of the twelve frozen hostile trees can be deleted and
the frozen target line is still printed verbatim.

### F3 — C2 "distinct claims" is distinct K ids only; duplicate spans pass

`count-c2.py:124-128` only rejects a repeated `K<id>`; nothing compares `(file, kind, n, quote)`
triples. Consequence: ten claims over three facts pass. In the same sandbox repo I rewrote the
entry so that K1–K10 cycle the *same* three spans (`r54:line:2`, `r55:line:2`, `r56:line:2`,
each repeated 3–4×) with correct pins:

```
distinct spans: 3        (grep -c '^- \*\*K' → 10)
C2=met selftest=ok … entry=ok rows=ok pins=ok tree=ok claims=10 files=3 rev=e9aa8342…  exit=0
```

This is not hypothetical only in sandboxes: **the committed tree baseline already relies on it.**
Every `trees-c2` entry has 10 claims over exactly 3 spans
(`probe: base tree claims=10 distinct spans=3 -> [(…r54.json,'line','2'),(…r55.json,'line','2'),(…r56.json,'line','2')]`, and `eval_entry` returns `ok=True` for the unmutated tree). Round-58
routed defect 4 asked for "distinct claims"; the counter implements "distinct K ids". A hostile
tree that repeats spans under fresh K ids is absent, and the good-path baseline is itself the
counterexample.

Status of the live data (read-only, working tree at 2026-10-28 02:59Z, uncommitted data landed by
a sibling seat while I was reviewing): `grep -c '^- \*\*K'` → **14 claims**, distinct
`(file:kind:n)` spans → **14**. So the current entry does not exploit the hole — it is latent,
not realised. The counter simply cannot tell the two apart.

### F4 — `f11-manifest-wrong-index` is mislabelled, duplicates f10+f12, and its named class is unreachable

`f11`'s mutation is "move the populated round to 700, leave `rounds[832]` as `{}`, pad to 900"
(`python3 -c "…r=…['rounds']; print(r[832], sorted(r[700]))"` → `{} ['capabilities_added','lane','lane_round']`).
The tool therefore emits `manifest:lane=None`, `manifest:entry_missing`, `manifest:lane_round`
— i.e. f10's class and f12's class plus `entry_missing`. `manifest:index_missing`
(`mori-register-check.py:157`, requires `ri >= len(rounds)`) never fires. Its frozen expect is
the single character-class token `manifest`, which any of those four reasons satisfies. So the
fixture named for "wrong index" tests the two neighbouring classes and leaves its own code path
uncovered; it adds no unique coverage to the set.

### F5 — Missing obvious case: absent evidence column (`keys:short_row`), and four other unowned classes

The tool emits 15 reason classes (`tools/mori-register-check.py:116-186` + `scorecard_unreadable`).
Fixtures own ten of them; these are owned by **no** fixture
(`grep -l 'short_row\|empty_name\|index_missing\|unreadable' fixtures-c1/*/expect.txt` → `(none)`):

| class (tool line) | probe result | fixture |
|---|---|---|
| `keys:short_row` (:146) — row with 4 cells, evidence column absent | `m2-evidence-column-absent exit=1 reasons=['keys:short_row=…[0]']` | **none** |
| `keys:empty_name` (:150) | `m3-empty-name exit=1 reasons=['keys:empty_name=…[0]']` | **none** |
| `manifest:index_missing` (:157) | `m4-index-beyond exit=1 reasons=['manifest:index_missing=…[0]','…[1]']` | none (f11's stated class) |
| `manifest:unreadable` (:139) | `m5-manifest-garbage exit=1 reasons=['manifest:unreadable']` | **none** |
| `scorecard_unreadable` (early return) | not probed (tool needs argv) | **none** |
| `manifest:entry_missing` (:165) | `m6-entry-missing exit=1 reasons=['manifest:entry_missing=…[1]']` | only incidental inside f11's broad token |

**This is the pair the ticket names.** `f13-empty-pointer` is an *empty evidence cell*
(`| … | none | 56 |` → no backticks → `pointers:none`). The *absent evidence column*
(`| … | 56 |` → 4 cells → `keys:short_row`) is a different predicate branch, a different reason
token, and has no fixture. Both are plausible register-writing mistakes — a merged column and a
blank cell look the same to a human reader but score different reasons, and only one is frozen.

### F6 — Missing obvious cases on the C2 tree side

`grep -l 'files_min\|entry_absent\|copy_absent\|sources_absent\|no_source_ids\|short' trees-c2/*/expect.txt` → `(none)`.

| class (count-c2 line) | probe result | tree |
|---|---|---|
| `rows:bad_row` **missing-cell direction** (`len(cells) != 11`, :183) — 10 cells, used-by column absent | `n1-usedby-column-absent ok=False reasons=['rows:bad_row=S901']` | only the 12-cell direction (t08) |
| `rows:usedby` **empty-cell direction** (:189) — 11 cells, `cells[10] == ""` | `n2-usedby-cell-empty(space) ok=False reasons=['rows:usedby=S901']` (the row needs a trailing space: `.strip("|")` erases `\|\|`) | only the other-entry direction (t09) |
| `files_min` (:135) — fewer than 3 cited files | not in any tree | **none** (t06 covers `files:outside`) |
| `entry_absent` (:110) — tree without the entry | **none**; every tree ships one |
| `pin:copy_absent` (:146) — claim cites a copy that is not in the tree | **none** |
| `rows:sources_absent` (:170) | **none** |
| `offset` equality (:158-160) | t11's only `offset:` claim is `Quote: \`ab\`` (2 bytes) and hits `span:short` → `continue` at :153, so the offset branch is **never compared** by any tree (`grep -rn 'offset:' trees-c2/` → 1 hit, t11 K1). Probe `n4-offset-mismatch → ['span:1']` and `n5-offset-correct(2) → ok=True` show the branch works but is unfrozen. The live entry does use it (3 claims at `w1-settlement-r58.json:offset:89/224/237`), so the branch is exercised by data and unpinned by the hostile set. |

Note the same empty-vs-absent pair as F5: an empty used-by cell and an absent used-by column both
fail, but with different tokens and only one direction is frozen (t08 extra cell, t09 other
entry).

### F7 — Duplicated coverage at token granularity (the sets are not as orthogonal as their names)

Token counts on the committed expect files:

```
C1: 4 pointers | 2 manifest:name | 2 keys | 2 binding | 1 manifest:lane_round | 1 manifest:lane | 1 manifest
C2: 2 span     | 1 each rows:usedby/rows:status/rows:missing/rows:bad_row/pin/grammar/frontmatter/files/distinct/claims_min
```

Matching is `any(r.startswith(e) for r in reasons)` (`count-c1.py:158`, `count-c2.py:352-353`),
so prefix collisions collapse distinct classes:

- `'manifest:lane_round=K'.startswith('manifest:lane')` → **True**. Probe: `f10`'s manifest with
  `lane_round=55` and `lane="mori"` yields `['manifest:lane_round=…[0]','manifest:lane_round=…[1]']`
  and **f10's frozen expect `manifest:lane` is still satisfied** (`… satisfied by these? True`).
  f10 therefore does not pin "foreign lane"; only the mutated `kotoba` data does.
- `'pointers:missing=x'.startswith('pointers')` → True; all four pointer fixtures (f05 f06 f07
  f13) share that one token, so missing / absolute / parent-relative / empty-cell are
  indistinguishable to the counter.
- `'span:short=1'.startswith('span')` → True: t03 (wrong line) and t11 (short quote) share the
  token; and `keys:short_row`/`keys:empty_name` would satisfy f03/f04's `keys`.
- `'files_min:2'.startswith('files')` → True: t06's `files` would accept the untested `files_min`.
- `f11`'s bare `manifest` accepts every manifest-family reason (F4).

Genuine (non-duplicate) pairs, for the record: f01/f02 differ (`declared_register=0` vs `=2`);
f03/f04 differ (duplicate vs missing); f08/f09 differ (altered name vs substring-only, the
`entry[len(name)].isalnum()` boundary at `mori-register-check.py:169-170`); t03/t11 differ in
cause but not in token (see above).

### F8 — Dead weight in the frozen counters (simplifier axis, no behavioural effect)

- `count-c1.py:155-157` computes `got = {…}` and never reads it — the normalisation is dead and
  is the only place the reason string is re-split. Deleting it changes no branch.
- `count-c1.py:215-216` imports `importlib.util` and builds `spec` inside `selftest()`; both
  unused (`self` path is never used either).
- `count-c1.py:127` `dirs = [n for n in names if not n.endswith(".py")]` filters a suffix that
  cannot occur under `fixtures-c1/` (13 dirs, no `.py`); it also silently treats a stray *file*
  as a fixture dir (which then fails loudly as `fixture:<name>:incomplete`, so it is noise, not
  a hole).
- Frozen, so not touched: these are candidates only if a future round re-freezes the counters.

## No-harm / clean-cut statements

- No production file, corpus registry, SCORECARD, LOG, lane VCS or fleet path was written; the
  lane tree still shows only the pre-existing untracked `round-59/w1/`, `w1-dispatch.stderr`,
  `w1.ready.dispatched`, `assimilation/` plus this report.
- The two sandbox repos were throwaway (`mktemp -d` under my scratch), each verified with
  `git rev-parse --show-toplevel`; they were deleted with the scratch dir, and the receipt is the
  command/output text above.
- Nothing installed or updated; pacman not run.

## Tradeoff / stop point

Every finding above is *under-enforcement* (a frozen arm that can be satisfied without its
evidence), not a false failure: no frozen tree or fixture scored MET where it should be UNMET on
the committed bytes, so the round's `C1=met`/`C2=met` line is not contradicted — it is weaker
than the contract's prose ("13 committed trees", "12 committed trees", "distinct claims"). The
next deletion that would help is trimming `f11`'s `manifest` token to its actual class and
pinning the roster in both counters; both require a re-freeze, so they are routed, not applied.
Stopping here: further mutation of the frozen byte sets would attack the kill rule, not the
claim.
