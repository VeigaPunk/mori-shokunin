# Mo58Critic32 — C1 do-nothing / pointer-resolution review

## Counterexample: nonexistent evidence pointers score green

At the frozen revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0`, I built a throwaway git fixture with the otherwise conformant active register and the two exact round-56 keys, but replaced **all four evidence paths** with `missing/ghost-{a,b,c,d}.txt` (none exists in the fixture commit). The frozen counter emitted:

```text
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=cee2dececcbaef2f83fda8534f0f37bd59980c0a
EXIT=0
```

This falsifies the frozen §9 required control (“two rows name a nonexistent evidence path” → unmet, `failed=pointers`, exit 1). In `count-c1.py`, `measure()` extracts backticked values, but only invokes `git cat-file -e` when a path starts with `.ufo/`, `tools/`, or `corpus/` (lines 81–85). A repository-relative evidence path such as `missing/ghost-a.txt` contains `/` but matches none of those prefixes, so it is silently ignored and `pointers` remains `ok`. The fixture's missing paths were the only evidence paths in the two rows.

**Impacted axis:** C1 calibration / pointer-resolution validity; the counter can certify rows with nonexistent evidence paths. This is a counter defect, not a score inference.

**Smallest safe correction:** Treat every evidence-field path in the two selected rows as a repo-relative pointer and require `git cat-file -e R:<path>` for each; do not silently skip paths based on an allowlist prefix. Add the `missing/ghost-*.txt` fixture as a required failing arm. This is a recommendation only; I made no production edits.

## Entering-revision no-work baseline

Ran the byte-identical frozen counter from a scratch checkout at the freeze revision against the entering revision. Exact invocation:

```text
python3 .ufo/waves/round-58/count-c1.py b783d0b892637ce8d20f188cad20e4d8913ca635
```

Exact output and exit:

```text
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=b783d0b892637ce8d20f188cad20e4d8913ca635
EXIT=0
```

The target state therefore already existed at entry: active-register rows are at `SCORECARD.md:1989-1990`; all four then-recorded paths resolve at that revision; manifest hints match. The entry revision predates the counter file, while the freeze revision is its descendant. Thus the cheapest no-work state for the C1 data predicate is the entering revision itself (no register/pointer/manifest edits); the round's delta is the verifier/frozen inputs, not new register content. This alone is not a counterexample to the stated claim, which claims verification rather than new rows.

The counter file SHA-256 matched across the working tree and freeze revision: `6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b`. Its `--selftest` produced `C1_SELFTEST pass=4 fail=0`, exit 0. That selftest does not cover the unprefixed-pointer bypass above.

**Target-output note:** Contract’s frozen target includes `selftest=ok`, but the counter’s measurement output uses `failed=none`; the literal token `selftest=ok` does not occur in the frozen counter. If the target is meant as exact output rather than a field summary, this is a frozen target/counter format mismatch.

Method bounded to the frozen counter, contract, entering/freeze git objects, the required pointer-control behavior, and one isolated throwaway fixture. No production/corpus/SCORECARD/LOG/VCS changes; no commits. Scratch cleaned before handoff.
