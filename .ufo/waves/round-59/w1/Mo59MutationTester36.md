# Mo59MutationTester36 — fixture expect-file semantics probe

Seat: mutation-tester (leaf; no sub-dispatch). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Detector: frozen `count-c1.py` / `count-c2.py` at freeze `60b3a76a`, run read-only against a
disposable scratch clone (`/fast/scratch/hyaku/mori-r59/Mo59MutationTester36/lane-mut`, `git clone` of the
lane) with `--repo` pointing at the clone. Lane repo untouched (`git status` clean throughout);
all commits landed only inside the scratch clone. `disk-guard.sh status`: green (27% used, 592G free)
before and during the probe.

## Question

If an expect file lists two prefixes and only one reason fires, does the counter still pass it?

## Answer — two-part, demonstrated

- **Uncovered second prefix → NO (counter catches it).** `matched = all(any(r.startswith(e) ...) for e
  in expect)` (`count-c1.py:158`; mirror `count-c2.py:352`) requires *each* prefix covered by some
  emitted reason. M2/M5 below: killed.
- **Single reason covering both prefixes → YES, passes (survives).** Coverage is per-*prefix*, not
  per-*reason*: one emitted reason can satisfy every prefix in the list. M1/M4 below: survived.
  An expect file therefore cannot express "at least two distinct reasons"; a fixture whose frozen
  intent was `binding AND pointers` is indistinguishable from one satisfied by a single `binding:*` hit.

## Mutants (one mutated file per commit; every rev differs from baseline in exactly that file)

Baseline rev `8ff344ff` (lane HEAD; tools at frozen PINs — C1 met; C2 entry arm pre-landed so `C2=unmet`
but `trees=ok`, i.e. the hostile-tree detector arm was live).

| # | file | expect bytes | sha256 | detector output | verdict |
|---|------|--------------|--------|-----------------|---------|
| M1 | fixtures-c1/f01/expect.txt | `binding,binding:declared_register\n` | `d9e26401…` | `C1=met selftest=ok fixtures=ok real=ok pointers=ok` rc=0 | **SURVIVED** — emitted `binding:declared_register=0(capabilities_sections=1)` alone covered both prefixes |
| M2 | same | `binding,pointers\n` | `9a97569f…` | `C1=unmet … failed=fixture:f01-stub-only` rc=1 | KILLED — `pointers` uncovered (f01 emits no `pointers:*`) |
| M3 | same | empty file (0 B) | `e3b0c442…` | `C1=met fixtures=ok` rc=0 | **SURVIVED** — C1 splits without an empty filter (`count-c1.py:140`); `expect=['']` and `r.startswith('')` is true for any reason → any-UNMET-verdict pass with zero coverage |
| M4 | trees-c2/t01/expect.txt | `frontmatter,frontmatter:source\n` | `bbea55c0…` | `trees=ok` (failed list: only pre-existing copy_absent/entry_absent/tree) | **SURVIVED** — `frontmatter:source` reason covered both prefixes |
| M5 | same | `frontmatter,pin\n` | `69270a5b…` | adds `tree:t01-no-frontmatter:reasons,trees` | KILLED — `pin` uncovered |
| M6 | same | empty file (0 B) | `e3b0c442…` | adds `tree:t01-no-frontmatter:verdict,trees` | KILLED — C2 filters empties (`count-c2.py:333`) and `want_ok = not expect` flips the polarity: empty expect *requires* a clean tree; 5 reasons → verdict mismatch |

f01 emitted reasons (tool run on committed fixture): `binding:declared_register=0(...)`,
`keys:missing=...[0]`, `keys:missing=...[1]` — frozen expect `binding` covered by reason #1 only.
t01 emitted: `frontmatter:source`, `frontmatter:verified-at`, `frontmatter:recheck`,
`frontmatter:coverage-map`, `rows:no_source_ids`.

## Commands (exact)

```
python3 .ufo/waves/round-59/count-c1.py <rev> --repo <scratch>/lane-mut --fleet /home/vgpnk/Projects/shokunin --scratch <dir>
python3 .ufo/waves/round-59/count-c2.py <rev> --repo <scratch>/lane-mut --scratch <dir>
```
Mutant revs: M1=`417137f6`, M2=`63bf5740`, M3=`bc5fdd68`, M4=`7d87cae1`, M5=`32b8afb0`, M6=`f0703c0a` (scratch clone only).

## Findings

1. **Coverage-finding (surviving mutants): expect lists are a cover relation over strings, not a
   reason count.** Two prefixes satisfiable by one reason. Contract phrase "covering its frozen
   expect prefix" holds literally, but the semantics is weaker than it reads: `all/any` with
   `startswith` is monotone — adding prefixes that nest inside an already-covered reason is free.
   Frozen battery unaffected (all 25 expect files are single-prefix; verified by dumping every
   `expect.txt` at `60b3a76a`), so this is a latent spec gap, not a live kill. Had any frozen expect
   been written `binding,pointers` intending two distinct reason classes, the counter would pass it
   on `binding` alone — no detection.
2. **C1/C2 asymmetry on empty expect.** C1: empty file → `['']` → vacuous pass on any UNMET verdict
   (M3). C2: empty file → `[]` → treated as "clean tree expected", hostile tree kills it (M6).
   Same extension point, opposite semantics; a future empty/whitespace-only expect file added to
   fixtures-c1 silently degrades to "verdict != MET".
3. **Dead matcher state.** `got` at `count-c1.py:154-157` normalizes reason keys (`key:sub` before
   `=`) but is never read — the check that actually runs is raw `r.startswith(e)` on the whole
   reason including `=…` payload. Whitespace inside a comma list is also not stripped
   (`"binding, pointers"` would fail to match `pointers:*`; code-derived from line 140, not run).

## Restoration evidence

After the battery: `git reset --hard 8ff344ff18924c1ea63d46c3b3969f9fea05bc51` in the scratch clone
(clone is disposable; lane never mutated). Post-restore:
`git status --porcelain` empty; `f01/expect.txt` sha256 `587d24cd…` == lane HEAD bytes (verified via
`git show HEAD:…` diff — byte-equal); `t01/expect.txt` sha256 `a39cb081…` == lane HEAD bytes.
Scratch dir `/fast/scratch/hyaku/mori-r59/Mo59MutationTester36` (clone + run dirs) deleted after
this report was written.

## Bounded method statement

Six point mutations, one file each, exact frozen counter as detector, pristine baseline reproduced
first (C1 `met` @ `8ff344ff`; C2 `trees=ok`), restored bytes verified. Bound: only
f01-stub-only / t01-no-frontmatter were mutated; other fixtures serve as unchanged controls and all
passed as frozen. No production, registry, SCORECARD, LOG, or VCS mutation in the lane.
