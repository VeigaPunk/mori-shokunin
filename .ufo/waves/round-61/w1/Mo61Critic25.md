# Mo61Critic25 — freeze-integrity review

Axes: calibration (C1), freshness (C2), operability (C3), and provenance/freeze integrity. Findings only; no admission or judgment. All references below are lane-relative to `/home/vgpnk/Projects/shokunin/mori-shokunin`; frozen revision `7370a731abcafc4c803111de7c22cd6264d63be1`. No production files or frozen artifacts changed.

## Assigned checks

### 1. C2 frozen met tokens are absent from its formatter

**Counterexample/evidence:** `contract.md:71` requires `rows_src=ok provenance=ok`. `count-c2.py:191-196` prints only `pointers`, `rows`, `same`, `moved`, `changed`, `quotes_ok`, `spans_ok`, `sources`, `failed`, and `rev`. `rows_src` and `provenance` occur only as failure reasons (`:107`, `:182`), never as output fields. Thus even a passing result cannot print those two frozen met tokens. `sources>=4` is a numeric predicate over the emitted `sources=N`, not a literal output token.

C1 (`count-c1.py:123-128`) and C3 (`count-c3.py:193-199`) print every named contract met field. Both additionally print `failed=none`, omitted from their contract met-line examples (`contract.md:42,101`). Extra fields alone are not treated here as a failed subset requirement.

**Impact:** freshness; contract/output provenance. **Smallest safe correction:** report the mismatch under the frozen contract; do not silently equate absent fields with printed evidence or amend this round's counter/contract. A future instrument can emit the two measured statuses explicitly.

### 2. SHA/revision pins are present and match

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin show ac496c7cde8cad965079858accae3bedfe4a73f2:.ufo/waves/round-60/count-c3.py | sha256sum` returned:

```
fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514
```

This equals the full contract SHA (`contract.md:88`) and `count-c3.py:40`. Its revision is present at `count-c3.py:39`. The earlier `4d036fb0` is a commit reference, not a SHA256 pin; it appears in `gate-manifest.json`. Its r60 C3 bytes hash to `546486571e13e151fdec240a32b85a5a4fb71c16440c81a38edb8da12829a5ba`, confirming amendment 2's distinction from the frozen bytes.

Committed r61 C1/C2 blobs hash to the in-script `PIN_C1`/`PIN_C2` (`count-c3.py:41-42`):

```
C1 a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00
C2 82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8
```

All six committed source copies match `count-c2.py:30-37`. Independent fetches from `https://raw.githubusercontent.com/torvalds/linux/v7.3/` also returned identical SHA256s for `Documentation/accounting/psi.rst`, `kernel/sched/psi.c`, `include/linux/psi_types.h`, `Documentation/admin-guide/cgroup-v2.rst`, `init/Kconfig`, and `Documentation/admin-guide/kernel-parameters.txt`.

No missing full SHA256 pin found in the contract.

### 3. Amendments 1–2 are committed before dispatch

`git log --format='%h %ci %s' -- <round-61 contract/counters/evidence paths>` shows the single freeze commit at `2026-10-30 02:05:09 -0300`. `git blame -s` attributes contract amendment lines 3–12 to `7370a731`. Dispatch-file mtime is `2026-10-30 02:12:04.767429785 -0300`; ready-file mtime is `02:12:12.800962999`. Working-tree contract SHA equals committed contract SHA: `0b5e4f49d10b4130ccfc5559d6b4413bf18243011debd8278e00937cf6a1ca7e`.

This supports pre-dispatch final amendment bytes; separate per-amendment history is not available because both first appear in that same commit. No evidence of a post-dispatch amendment found.

## Additional contract/counter counterexamples

### C1 accepts zero non-superseded rows

`contract.md:38` requires exactly one non-superseded row. `count-c1.py:96-103` filters live rows but falls back to `hits[0]` when there are none. The frozen selftest's `superseded-ok` case (`:145-156`) contains two superseded rows and expects success.

A scratch fixture with one resolvable `tools/j.py`, one-path manifest, and two otherwise complete rows whose scopes both say `superseded: retired ...` produced:

```
C1=met gates=1 registered=1 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=none rev=53bbce45559db867fb3b4299cbcfd5e999744a0a
rc=0
```

The fixture's root was `/fast/scratch/hyaku/mori-r61/Mo61Critic25/tmp.gFDyRQJ6P8`; no lane VCS state was changed. A separate in-process synthetic `cat` probe gave the same result: `ok=True registered=1 ... failed=[]` for all-superseded-only rows.

**Impact:** calibration, duplicate/stale authority. **Smallest safe correction:** route this as a frozen-counter defect; future counter requires `len(live)==1`, with an all-superseded negative fixture. Do not apply this change now.

`noowner` is also never incremented (`count-c1.py:75,127,214` are its only occurrences). Empty owner correctly fails through `thin`, so this is a dead diagnostic field, not an additional met bypass.

### C2 default selftest does not reproduce the green receipt

Command (absolute script path, cwd lane, fresh scratch):

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r61/Mo61Critic25/st2b
```

Result:

```
case good: ok=False want=True FAIL failed=['pointer_floor:6<40']
C2_SELFTEST pass=9 fail=1
rc=1
```

`count-c2.py:291,297` passes default floor 40 into the selftest; repeated text deduplicates to six pointers (`:205-208`, `:57-65`). The committed receipt instead records `case good: ok=True ... failed=[]` and `pass=10 fail=0`. A nondefault floor could explain this, but the receipt contains no invocation, so the precise original command is not established. This does not prove a post-freeze edit or fabricated receipt.

**Impact:** freshness/operability and receipt reproducibility. **Smallest safe correction:** disclose invocation discrepancy; retain frozen bytes and recover the original command provenance rather than claim the default selftest passes.

### C1 control needs an explicit out-of-band manifest

At entering revision `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`, default invocation produces `C1=unmet gates=0 ... failed=manifest_unreadable`, rc=1. `git cat-file -e <entering>:.ufo/waves/round-61/gate-manifest.json` confirms absence. Supplying `--manifest /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/gate-manifest.json` reproduces the committed receipt's complete first line exactly (`1131` characters, no literal ellipsis), with gates=25/missing=25 and rc=1.

**Impact:** control provenance, not a do-nothing-met bypass. **Smallest safe correction:** record the absolute manifest override and its frozen digest when describing this control; do not imply the default invocation reproduces it. The apparent ellipsis in earlier tool output was display truncation, not file content.

### C3 structural/expect pins fail cheap negative controls

Scratch copies only, original counter unchanged:

1. Replace `c1_ok = all(b.values())` with `c1_ok = True`, keeping `met = c1_ok`. Run against entering revision. Result:

```
C3=met r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r61 counters absent or sha pin mismatch at rev rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb
rc=0
```

`arm_r61repair` (`:108-123`) checks the `c1_ok` spelling, not its dependency on all arms. This is a structural-validator weakness demonstrated on a mutant, not a claim that unmodified `run_arms` currently ignores booleans.

2. Replace `EXPECTS = {t: "ok" for t in TOKENS}` with `{t: "bad" for t in TOKENS}`. At freeze revision the mutant still prints:

```
C3=met r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=ok cases=5 failed=none rev=7370a731abcafc4c803111de7c22cd6264d63be1
rc=0
```

`EXPECT_PIN` is derived from the same table at import (`:46-48`), so changing the table changes the supposed pin. This conflicts with the independent frozen-expect-table claim (`contract.md:97,108-109`). `TOKEN_MAP` values are likewise not read by the formatter (`count-c3.py:194`) and its static check checks keys rather than values (`:113-123`).

**Impact:** operability, false provenance. **Smallest safe correction:** report these kill-rule-relevant findings without patching frozen artifacts. A future instrument needs an independently fixed expect digest and a dependency-sensitive negative test.

## Verification boundaries / cleanup

Disk guard before work: green, scratch free `371.8G`; no ENOSPC. C1 selftest printed `pass=6 fail=0`; C3 selftest printed `pass=8 fail=0`. Their initial piped shell statuses were not reliable exit-status evidence; C2 fresh unpiped rc=1 above is reliable. C2/C3 entering controls reproduced, rc=1 each. No tools installed or updated. No production edits, integration, lane/fleet commits, or canonical judgment performed. Scratch copies, downloads, and fixture are removed before yielding; small receipts are embedded above.

Self-evaluation: accuracy 4 (explicitly distinguishes mutants, unmodified logic, display truncation and unrecorded invocation); completeness 4 (all three assigned freeze checks covered; per-amendment independent history unavailable); clarity 4 (line references and receipts provided, ancillary findings longer than core); actionability 4 (future corrections only, current freeze respected); conciseness 3 (extra counterexamples beyond token/pin/timing remit). Overall 3.8. Improvement applied: removed strict-equality claims for harmless extra fields and corrected the false receipt-elision suspicion. Main should use the core token mismatch and documented counterexamples, not infer an admission decision from this review.
