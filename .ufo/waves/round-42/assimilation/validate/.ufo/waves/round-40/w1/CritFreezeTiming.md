# CritFreezeTiming — freeze-discipline attack (r40 w1)

Role: critic. Target: "Frozen before any data seat or data receipt" (contract.md:5–13) vs. the observed commit/mtime spine. All times -03:00 (receipt's `05:46:06Z` = `02:46:06` local).

## Verdict

**Contract ordering claim is FALSE at commit granularity and unanchored at file granularity; content provenance is airtight.** No instrument byte changed after `265a955c`, and `git show` proves the extracted v2 bytes predate the round — so nothing *content-wise* is wrong. But "frozen before any data seat" is witnessed by **19 ms of mtime ordering** between two uncommitted files, and the freeze receipt's first committed existence (`8d3badd`) is *after* the data commit (`265a955c`) that carries the pinned files plus S229. The freeze was a working-tree event the commit graph cannot order.

## Timeline (observed, not asserted)

| t (-03:00) | event | source |
|---|---|---|
| 01:35 | census-start.txt | mtime |
| 01:45 | contract.md, count-c8.py written | mtime |
| 01:58 | conform.py v3 written | mtime |
| 02:40 | extracted/ + run-c11-dags.py written | mtime |
| **02:41–02:45** | **all c10-red-\*/c11-red-\*/parity receipts — BEFORE any pin exists** | mtimes |
| 02:44:32 | conform-r39-conjunct-gutted.py created (untracked) | mtime |
| 02:45 | c10-red-conjunct consumes it | mtime |
| **02:46:06.1129** | **freeze-r40.txt written (pin over working-tree bytes)** | mtime + receipt text |
| **02:46:06.1320** | **S229.src (round DATA) written — 19 ms after pin** | mtime |
| 02:46:45 | conform-scope-r40.md (data) | mtime |
| 02:47:29 | `265a955c` commit: instruments + extracted + fixtures + **S229 data, atomically** | git |
| 02:49–03:01 | after-receipts; two files rewritten post-commit (see below) | mtimes |
| 02:56:11 | `8d3badd` commit: **freeze receipt + all receipts + SCORECARD** | git |
| 02:56:56 | `ede486b`: S229 registry repair + `conform-v3-conjunct-gutted.py` (first commit) | git |

## Contamination enumeration — which before-receipts ran inputs while mutable

Every c10-red/c11-red receipt (02:41–02:45) predates the pin (02:46:06), so "post-freeze edits" is the wrong frame: they ran in a **pre-pin unanchored window**. Per receipt, the input not anchored to a commit at run time, and the certifier that closes it:

| receipt | unanchored input at run time | closed? |
|---|---|---|
| c10-red-shadow-none/neg, cond, inf, divzero, decoy, underscore, second-popen, tuple (9) | `fixtures/generated/survivor-*.py` (untracked until 265a955c, unhashed in receipt); transitively `make-survivor-fixtures.py` + `count-c8.py` (mutable ≤02:46) | YES — pinned builder rebuilds all 10 survivors byte-identical to committed bytes (MATCH ×10, below) |
| **c10-red-multicounter** | **`count-c8.py` itself is a measured `--counter`**; receipt records no sha; editable 02:41→02:46 | closed by pin content-match only — no run-time hash; weakest surviving certifier |
| **c10-red-conjunct** | interpreter `generated/conform-r39-conjunct-gutted.py` — **not in pin set, untracked until 02:47:29** | closed only by commit content existing; nothing proves run-time bytes == committed bytes |
| c11-red-neveredited / firstparent / readd | `run-c11-dags.py` (mutable) **and** `tools/mori-sources-appendonly.py` v3 — `load_gate()` imports `_make_dag_repo`/`_selftest_dag_cases`/`_selftest_env` from the working-tree v3 gate to build the DAGs the v2 gate judges; repos are `mkdtemp`+`rmtree`, never committed | YES — rebuilt today: identical `b0=07be6c7f1765` base sha and verbatim v2 verdicts (deterministic env, pinned commit dates) |
| c11-before-lane | extracted gate only | YES — verbatim reproduced (`18 changed`, `superseded_as_of=[18]`, `stale=[]`, exit 1) |
| c10-parity | count-c8 mutable; receipt hashes c7 but not c8 | closed by pin content-match only |
| census-start | none (01:35, predates all instruments; reads committed corpus) | immune |

Zero post-freeze committed edits: `git log 265a955c..HEAD -- <all pinned paths>` is empty; working-tree sha256 of every pinned path equals its pin. So the "post-freeze instrument edits" set is **empty at every level below working-tree mtime** — all exposure is the 02:41→02:46 pre-pin window plus the consume-then-commit gaps.

## Extracted-bytes provenance (`git show` — the clean half)

```
git show bb1f2457:.ufo/waves/round-39/conform.py    → fe0be179… = pin = extracted/conform-v2-r39.py
git show bb1f2457:.ufo/waves/round-39/count-c7.py  → b92c65f2… = pin = extracted/count-c7-r39.py
git show bb1f2457:tools/mori-sources-appendonly.py → 62cd4132… = pin = extracted/gate-v2-bb1f2457.py
```

`bb1f2457` is the entering tip, parent of `265a955c`; these blobs existed in the object store before any r40 commit. Even if the working-tree copy had been edited between receipt (02:41) and pin (02:46), the pin+commit comparison detects it **retroactively** — the only undetectable case is edit-then-restore inside that window, which changes nothing observable. The extracted-interpreter channel is the one channel that is structurally sound.

## Additional provenance defects

1. **Consume-then-commit, both conjunct fixtures.** `c10-red-conjunct` (02:45) ran `conform-r39-conjunct-gutted.py` (created 02:44:32, first committed 265a955c); `c10-after-conjunct` ran `conform-v3-conjunct-gutted.py`, **absent from `8d3badd`** (`git ls-tree` empty), first committed 45 s later in `ede486b`. Commit `8d3badd` therefore contains a receipt citing a path no commit yet held.
2. **Evidence files rewritten post-commit.** `c10-after-conjunct.txt` mtime 03:01:55 and `c11-after-fixture-p.txt` mtime 03:00:22 are both *after* `8d3badd` (02:56:11); `git status` is clean, so the rewrites were byte-identical (resumed-attempt overwrite) — benign, but it means `evidence/` is regenerated, not append-only.
3. **census-end predates the S229 registry repair.** census-end.txt (02:50, `mori ok` on SOURCES.md) measured the tree before `ede486b` moved the S229 row inside `## Registry`; the frontier's "census exit 0" covers a layout no commit shipped. (Placement-only move; the W04 row set is unchanged, so the census verdict almost surely stands — but no receipt says so.)
4. **`P-C10 contract==checker PREDICATE: True` is self-certified** inside the receipt the pin lives in — fine as a checksum, but it is not independent attestation of the freeze order.

## Commands run (all under lane root, read-only + .scratch outputs)

- `git log --format='%H %cI %s' -30`; `git show --stat` on `265a955c/8d3badd/ede486b`; `git log --follow` per pinned path → file sets and natal commits above.
- `git show <rev>:<path> | sha256sum` over the 9 pinned paths + 3 extracted files; `sha256sum` on working tree → all match freeze-r40.txt pins; `git log 265a955c..HEAD -- <pinned>` empty.
- `python3 fixtures/extracted/gate-v2-bb1f2457.py bb1f2457 --repo .` → exit 1, identical `changed`/`superseded_as_of`/`stale` lines to c11-before-lane.txt (`.scratch/CritFreezeTiming/c11-before-lane-repro.txt`).
- `python3 fixtures/make-survivor-fixtures.py count-c8.py .scratch/CritFreezeTiming/survivors/` → exit 0; all 10 outputs sha256-match `git show 265a955c:fixtures/generated/survivor-*.py`.
- `python3 fixtures/run-c11-dags.py extracted/gate-v2-bb1f2457.py <lane> .scratch/.../c11-red-repro.txt dag-n dag-p dag-r` → identical `b0=07be6c7f1765`; verdicts verbatim equal to the three c11-red receipts.
- `git ls-tree 8d3badd -- fixtures/generated/conform-v3-conjunct-gutted.py` → empty (absent at receipt-commit time).
- `stat`/`git status --porcelain` for the mtime spine; `git status` clean modulo untracked `.scratch/`, `w1/`.

## Smallest safe correction

Fixable evidence-hygiene defects, not claim-killers — receipts reproduce post-hoc, so the canonical judge can treat this as provenance wording: (1) receipts must record the sha256 of every non-commit-anchored input (counter, fixture, interpreter) at run time; (2) commit the freeze receipt before — not inside — the first commit containing any receipt or data it claims to precede; (3) never consume a generated fixture before the commit that carries it; (4) contract wording: "frozen before data" is unprovable at commit granularity when instruments and data share their natal commit — pin, commit instruments, *then* seat data.

Tooling: none installed (git/python3/coreutils already present).
