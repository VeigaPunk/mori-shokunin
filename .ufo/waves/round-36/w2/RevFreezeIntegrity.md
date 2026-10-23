# RevFreezeIntegrity — round-36 wave 2 (falsify + verify, attempt 2)

- Seat: mori-r36-w2-RevFreezeIntegrity-14, reviewer (leaf, no subagents). Date: 2026-10-23.
- Item attacked: **freeze integrity at the landed tip** — `evidence/freeze-v2.txt` pins vs actual bytes at `bf0df77fee4b6ef54a90aea09335c7617f125151`.
- Method: read-only git against the lane repo (`git cat-file`, `git archive`, `git log`, `git status`, `sha256sum`). No lane file edited except this report; no pacman; no tools installed.
- Tip identity measured: `git rev-parse HEAD` → `bf0df77fee4b6ef54a90aea09335c7617f125151` (HEAD is the landed tip; there is no later commit to check). Data commit bf0df77 "round-36: C1/C2 data …" 2026-10-23 15:20:10 -0300; declaration commit 5842dc0 09:09:14 -0300.

## Findings by severity

### F1 — DEFECT (FAIL driver): contract.md freeze-pin drifts from the landed tip
- Pin: `.ufo/waves/round-36/evidence/freeze-v2.txt:2` records
  `dbd3f6d793239a2f729f89778847eb47b901167fa7a98f57269621f4273c4127  contract.md`.
- Measured at tip:
  `git cat-file blob bf0df77fee4b6ef54a90aea09335c7617f125151:.ufo/waves/round-36/contract.md | sha256sum`
  → `065a17b523b29840df8f1d516ca50eedb0da5e7d614198567439514a099dd93b`. Working-tree file hashes identically (`065a17b5…`), so tip and worktree agree — both disagree with the pin. **Drift confirmed.**
- Provenance (all measured):
  - `git cat-file blob c1a026c:.ufo/waves/round-36/contract.md | sha256sum` → `dbd3f6d7…` — the pin is the c1a026c bytes ("C0 control receipts … counters re-designed before data (v2)", 09:03:05 -0300; freeze-v2.txt header stamp 12:03:04Z = 09:03:04 -0300).
  - `git diff c1a026c 5842dc0 -- .ufo/waves/round-36/contract.md` → single tail hunk `@@ -110,3 +110,17 @@`, 14 insertions, 0 deletions: the appended section `## C1 declared exploratory before data (12:10Z, after wave-1 CritAxisFit)` (now at `contract.md:114`). Commit 5842dc0, 09:09:14 -0300 — **6 minutes after the pin was recorded**.
  - `git log --format='%h %ci %s' -- .ufo/waves/round-36/evidence/freeze-v2.txt` → last touched at c1a026c; **freeze-v2.txt was never re-issued after 5842dc0 edited contract.md**, and the data commit bf0df77 landed with the stale pin.
- Mitigation (characterization, not absolution): the drift hunk is append-only at the tail; lines 1–109 of the pinned and landed contract are byte-identical, so the frozen predicate sentences — P-C1 at `contract.md:21`, P-C2 at `contract.md:23` — are unchanged between pin and tip, and the P-C2 label line in the working-tree receipt `evidence/c2-after.txt:1` is the same sentence. The C2/C1 predicate *text* chain is intact; the freeze *discipline* is not: the pin's own claim (whole-file sha256 of contract.md) is false at the tip it freezes.
- Per the seat bound "FAIL on any drift": this is drift on a pinned artifact. **FAIL.**

### F2 — observation: cited data receipts are absent from the landed tip
- `git ls-tree -r --name-only bf0df77 .ufo/waves/round-36/evidence/` lists `c0-rescore-v2.txt, c1-before.txt, c2-before.txt, census-start.txt, freeze-v2.txt, freeze.txt, refs/ref-c1.py, refs/ref-c2.py` — **no c1-after.txt, no c2-after.txt**.
- `git status --porcelain .ufo/waves/round-36/` shows `?? .ufo/waves/round-36/evidence/c1-after.txt` and `?? .ufo/waves/round-36/evidence/c2-after.txt`.
- The round claims cite "data receipt evidence/c2-after.txt" and "evidence/c1-after.txt"; those receipts exist only as untracked working-copy files. Nothing at the pushed tip carries them, so their provenance cannot be verified from the landed tip (hashes of the on-disk files were not pinned anywhere I could find — no `sha256` line in either file's grep). Not one of my three named checks, but it is a freeze-integrity gap at the tip: the only artifacts frozen at the tip are the pre-data set.

### F3 — observation: C0 judgment prose grew after the C0 receipt
- In `git log --name-only 5842dc0..bf0df77`, the data commit added `.ufo/waves/round-36/c0/CtlJ12.md` (+140 lines, `git diff --stat 5842dc0 bf0df77`), i.e. C0 judgment material landed with the data commit, ~6 h after `c0-rescore-v2.txt` (c1a026c, 09:03). The rescore receipt pins control *program* hashes only, and `c0/controls/J12.py` is byte-identical to its header hash (see C2 below), so no pinned value is affected. Recording for completeness: judgment docs under `.ufo/waves/round-36/c0/` are not freeze-controlled.

## Verified clean (measured)

### C1 — counter pins hold
`git cat-file blob bf0df77:<path> | sha256sum`:
- `count-c1.py` → `86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0` = freeze-v2.txt:3 pin. MATCH.
- `count-c2.py` → `c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34` = freeze-v2.txt:4 pin. MATCH.

### C2 — all 25 c0 control programs byte-identical to rescore headers (exceeds the 6 spot-check minimum)
Extracted the tip tree read-only and hashed:
`git archive bf0df77 .ufo/waves/round-36/c0/controls | tar -x -C /fast/scratch/hyaku/mori-r36/RevFreezeIntegrity && sha256sum …` — 25/25 match the `sha256=` in the `== J*/K*` headers of `evidence/c0-rescore-v2.txt`:

| control | tip sha256 (prefix) | header match |
|---|---|---|
| J1 | da68bfba | ✓ | 
| J2 | f34cdbde | ✓ |
| J3 | d639aa1f | ✓ |
| J4 | d7e45111 | ✓ |
| J5 | 276b6b19 | ✓ |
| J6 | 6c8d4be4 | ✓ |
| J7 | 4d919ac6 | ✓ |
| J8 | 3332b68e | ✓ |
| J9 | 75849ce2 | ✓ |
| J10 | fe92f448 | ✓ |
| J11 | ede4cfdc | ✓ |
| J12 | 9d34bfe1 | ✓ |
| J13 | 4e05a96c | ✓ |
| K1 | 648ade0e | ✓ |
| K2 | 0a08726c | ✓ |
| K3 | c1af37d9 | ✓ |
| K4 | 07c40ade | ✓ |
| K5 | e24689da | ✓ |
| K6 | 33e2e39f | ✓ |
| K7 | 9c7933bc | ✓ |
| K8 | 6c3dc0ee | ✓ |
| K9 | 231ec3ea | ✓ |
| K10 | 755b6392 | ✓ |
| K11 | 1039f3a7 | ✓ |
| K13 | 6ed1fa01 | ✓ |

The `counter=` sha256 in every header also matches the tip blobs above (13×86dd3b7a, 12×c7edaacf). Bonus: rescore REF1/REF2 hashes `0d9c808b…`/`08874f8f…` equal the committed `evidence/refs/ref-c1.py` / `ref-c2.py` (`sha256sum` measured). Their `control=` paths point at `/fast/scratch/...` scratch copies I cannot re-hash, so the REF identity rests on hash equality with the committed refs — recorded as a residual gap, not a defect.

### C3 — nothing under `.ufo/waves/round-36/` changed after the data commit
- Canonical check `git log --name-only --format='COMMIT %h %s' 5842dc0..bf0df77` (range = exactly the data commit): 34 round-36 files touched — `w1/*.md`, `swarm-registry.json`, `w1-dispatch.json`, `w1-spec.json`, `dispatch-log.txt`, `c0/CtlJ12.md`. **None** of the frozen set (contract.md, count-c1.py, count-c2.py, c0/controls/*, evidence/*) is among them; the range check as literally specified (post-tip activity) is empty because HEAD == bf0df77.
- Working-copy drift vs tip: `git diff --name-only HEAD -- .ufo/waves/round-36/` → only `dispatch-log.txt` (live dispatch log, not pinned). Untracked additions listed in F2 plus `w2/*`, `w2-*.json`, `gen-w2-spec.py`, `__pycache__/` — none overwrite a pinned file.

## Residual risk & verification gaps
- F1 is bounded: predicate sentences byte-identical (single tail hunk measured); the practical risk is procedural — any future re-pin must be regenerated, or the next contract edit silently widens the gap. A freeze-v3 re-pin (or a one-line amendment to freeze-v2.txt) would close it; remediation is out of my lane.
- c1-after/c2-after receipts (F2) unverifiable from the tip; if the round treats the tip as the evidence boundary, the data receipts are currently outside it.
- Rescore REF control= paths are scratch-resident; identity asserted via hash equality with committed refs only.

## Tools/installations
None installed; no pacman invoked; scratch used only at `/fast/scratch/hyaku/mori-r36/RevFreezeIntegrity/`.

## What this item attacks
The pinned-freeze chain at bf0df77: contract.md/count-c1.py/count-c2.py bytes vs `evidence/freeze-v2.txt`, the 25 C0 control programs vs `evidence/c0-rescore-v2.txt` headers, and the post-data immutability of `.ufo/waves/round-36/`.

VERDICT: FAIL — contract.md at the landed tip (sha256 065a17b5…) drifts from its freeze-v2 pin (dbd3f6d7…), drift introduced by 5842dc0 six minutes after the pin and never re-pinned (pin drift confined to the appended C1-exploratory section; P-C1/P-C2 predicate bytes unchanged; both counter pins and all 25 control hashes verified clean).
