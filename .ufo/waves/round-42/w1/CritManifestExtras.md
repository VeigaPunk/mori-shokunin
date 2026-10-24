# CritManifestExtras — manifest extra-path / empty-freeze-fence attack

Scope: `corpus/knowledge/inheritance-d72ac16-r42.md` at landed tip
`34b926730c30e0251e1aec531863d8355dc491f1` (worktree blob `8afe3231` == committed
blob, no drift). Read-only review; probe scripts and scratch files lived only in
`/tmp`. No tools installed (python3 + git sufficed).

## Assigned checks — all three pass

1. **No extra path sneaks in via prose.** `count-c3.py:60-67` collects paths only
   inside ``` fences (`line.strip().startswith("```")` toggle +
   `[A-Za-z0-9_./+-]+` fullmatch + must contain `/`). Independent re-parse of the
   committed blob: exactly 8 bare ` ``` ` lines (balanced, no info-strings), and
   **zero** path-matching lines outside fences — even a naive full-file regex
   reader would collect the same 145. The 155 slashy prose tokens are all inline
   citations, never line-alone, so they cannot mint a counted path under either
   reader. Fence set == commit inherited set exactly: `diff-tree -r d72ac16` → 165
   paths; categorize-complement → 145 inherited / 20 freeze; fence minus
   inherited = ∅, inherited minus fence = ∅, no duplicate fence lines.
2. **Freeze fence really is empty.** `### freeze` (line 181, sole occurrence) is
   the last section; its fence at lines 190-191 contains zero content lines and
   the file ends there (od-verified, no trailing path bytes). "Empty by
   construction" is moreover enforced by construction *plus* by the counter:
   `manifest_no_extras` and the absence of a `manifest_freeze_rows` check mean any
   path line inside that fence lands in `extra` → C3=unmet. An empty-but-noisy
   (comment) fence is safe too: non-path tokens are not fullmatched.
3. **Recheck command runs and returns 165.** Literal
   `git -C <lane> diff-tree --no-renames --no-commit-id --name-only -r
   d72ac167535229d737b9fa844513431d9a12f5ea | wc -l` → **165**. d72ac16 is an
   ancestor of the tip (`merge-base --is-ancestor` rc=0); rename-aware diff-tree
   also returns 165, so `--no-renames` hides nothing.

Full counter run for corroboration:
`python3 .ufo/waves/round-42/count-c3.py 34b9267…` → 13/13 PASS, `C3=met`, rc=0.

## Counterexample found — false provenance citation (verdict-neutral)

**Claim:** manifest line 187 and `contract.md` P-C3 (line 77) both state the
named-freeze set is "enumerated in `evidence/freeze-r42.txt`"; count-c3.py's
docstring and `LOG.md:2421` repeat it.

**Fact:** `.ufo/waves/round-42/evidence/freeze-r42.txt` enumerates the
**round-42** freeze set — 19 sha256-prefixed paths. Intersecting it with the
actual d72ac16 freeze complement:

- only **8** of its 19 paths are in the 20-path freeze set
  (`round-41/conform.py`, `contract.md`→r41 fixtures count-c8/survivors×3/
  extracted×2, `tools/mori-sources-appendonly.py`); note `contract.md` in
  freeze-r42 is `.ufo/waves/round-42/` and `.ufo/waves/round-39/`, not r41's;
- **12** of the 20 freeze paths are absent from it (r41 `contract.md`,
  `w1-spec.json`, 3 evidence files, `run-r41-controls.py`,
  `build-dags-r40.py`, `freeze-r41.txt` itself, `tools/mori-round41-calibration.py`,
  `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/conform-bindings-r41.md`);
- **11** paths in it were not added by d72ac16 at all (round-42 contract,
  counters, 6 r42 fixtures, r39 contract).

There is in fact **no committed file** that enumerates exactly the 20: the r41
pin file `.ufo/waves/round-41/evidence/freeze-r41.txt` names only 18 of the 20
(it could not pin itself or the still-mutable `corpus/SOURCES.md`, and it pins
`.ufo/waves/round-40/evidence/freeze-r40.txt` which the manifest itself scores
as *inherited*, not freeze). The only exact enumerations are the commit
diff-tree complement and the manifest's own prose list. This also makes
line 8's "named in `evidence/freeze-r41.txt` … and the round-41 declaration"
half-true: the pin file names 18, not 20.

**Why it does not sink the grade:** count-c3 derives the freeze set from the
diff-tree categorization complement, never opening freeze-r42.txt — all three
checked quantities (20/145 split, per-category wants, no-extras) are
git-grounded. The defect is confined to prose provenance: a reader following the
citation is sent to a list that is wrong in membership (missing 12, containing
11 non-freeze) *and* wrong in count (19 lines vs claimed 20). It is the
extra-path attack surfacing in the one place the fence parser cannot see: the
cited authority. False provenance — impacted axis: **provenance/citation
accuracy**; verdict honesty unaffected.

## Smallest safe correction

1. Manifest (unfrozen — direct edit): replace line 187's
   "`enumerated in .ufo/waves/round-42/evidence/freeze-r42.txt`" with a truthful
   pointer, e.g. "enumerated as the complement of the 145 by the recheck command
   above (the r41 pin file names 18 of the 20; `freeze-r41.txt` and `corpus/
   SOURCES.md` entered the set without their own pins)". Keep the fence empty.
2. `contract.md` P-C3 + `count-c3.py` docstring (frozen bytes — cannot edit):
   record a C3-provenance erratum in `LOG.md`/`SCORECARD.md` round-42 sections,
   same mechanism as the three C2 errata already filed.
3. `LOG.md:2421` (record, unfrozen): same citation fix as (1).

Severity: minor — correctable prose defect, not a contract violation; the
canonical judge should not reject on it, but the citation should not survive
unerrata'd since four landed locations repeat it.
