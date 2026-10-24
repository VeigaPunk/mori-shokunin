# RevPriorIntent — round-40 w1 — dead-launch intent reconstruction

Seat: revenger (read-only; findings only, no production edits). Lane: mori-shokunin.
Scored tip: `265a955cc67be4eae97d2dc5a9338a25f31eb29b`. Entering tip: `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3`.
Axis: reconstruct what the dead launch intended, prove which of its bytes landed, which were changed/discarded, and what the landed bytes still owe.

## 1. The dead launch's commit chain (read-only git evidence)

All commands run in /home/vgpnk/Projects/shokunin/mori-shokunin; no mutating git/jj anywhere.

`git log --all --reflog --format='%h %gs|%s'` shows, between `bb1f245` (r39 spot-check) and the round-40 commits, a chain of empty-message working-copy snapshots (jj colocated backend):

```
4dea80f e104694 dc2be8d c2ecbbc b434d01 669b892 2a5d94e | 265a955 8d3badd ede486b
```

Tree-id census (`git rev-parse <c>^{tree}`):

```
4dea80f b05c46953a4d60576ee1ea40ec8342ab3cc0f3aa   (earlier evolving states)
e104694 46e10a6660029ab575bcbfc07153cdc7e07e999f
dc2be8d 4be6940a0b2042e459220ee841ad9293d3e8feeb
c2ecbbc 3f8c0cd00a4f1a4a5802278dab75357a450a2549   <-- dead launch's final tree
b434d01 16bbac9e0ad43e15b880ee3c82bf6c9cecd5d619   <-- transient partial tree
669b892 3f8c0cd00a4f1a4a5802278dab75357a450a2549
2a5d94e 3f8c0cd00a4f1a4a5802278dab75357a450a2549
265a955 3f8c0cd00a4f1a4a5802278dab75357a450a2549   <-- scored tip: SAME tree
```

- `git diff c2ecbbc 2a5d94e` → empty. `git diff 2a5d94e 265a955` → empty. `git diff 669b892 2a5d94e` → empty.
- **The landed scored tip is byte-for-byte the dead launch's final working tree.** `265a955` is a re-commit (describe) of the inherited bytes; the resume launch changed nothing in the inherited instruments at that commit.
- `b434d01` is a transient partial snapshot: `git diff --stat b434d01 669b892` = 26 files, +10828 lines (the witness fixtures, `S229.src`, `conform-scope-r40.md`, `round-39-erratum.md` and the rest were momentarily absent from the snapshot, then restored). Not an intent divergence — the next snapshot restored the identical tree hash `3f8c0cd0…`.
- What the resume launch actually landed, from `git diff --stat 265a955 HEAD`: `8d3badd` (all c10-*/c11-* receipts, freeze-r40.txt, census-end, wave-plan, w1-spec.json 66 items, gen-wave-spec.py, SCORECARD/LOG/lesson, scratch drafts, parity files) and `ede486b` (`conform-v3-conjunct-gutted.py` + S229 SOURCES.md repair). Nothing under the six frozen instrument paths differs 265a955→HEAD (`git diff --stat 265a955 HEAD -- <six paths>` empty).
- Corroboration: `corpus/lessons/round-40.md:23` finding **M23 "inherited-unverified-freeze"** — "the inherited working tree held `contract.md` claiming pins in `evidence/freeze-r40.txt`, but that file did not exist; no before/after receipt existed either — only `census-start.txt` … the resuming L1 re-verified every inherited instrument byte-by-byte … completed the unfinished work (gate selftest arms 12→15; dag-r redesign), and persisted `evidence/freeze-r40.txt`." Matches my independent reconstruction exactly.

**Reconstructed intent (confidence high):** the dead launch built the complete round-40 instrument set — frozen contract, conform v3 (P-C10, 11 arms), count-c8 (SimpCounters D1–D4 applied), gate v3 (P-C11), survivor/extracted/gutted/witness fixtures, S229 source + knowledge entry, r39 erratum — and died before persisting the freeze receipt and any receipt. It also left three untracked root strays and on-lane selftest scratch. The resume launch kept its bytes verbatim, pinned them, and supplied everything the dead launch never ran.

## 2. Inherited artifacts re-verified (this seat, today)

Pins re-hashed over the working tree (`sha256sum <path>`), all equal to `evidence/freeze-r40.txt`:

```
6514914885e6a1249ed7903931b9734a55e828275121353c2727348eae504a8d  .ufo/waves/round-40/contract.md
4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da  .ufo/waves/round-40/count-c8.py
5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf  .ufo/waves/round-40/conform.py
bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec  tools/mori-sources-appendonly.py
8ff91db744c684f7b9b5c1d84e63538602635c52214a2b802afc520e4933acea  .ufo/waves/round-40/fixtures/make-survivor-fixtures.py
0cd7f1d23c88db501288cad7ac4381a44d855aaf79f16dd1be1cda6d71f156da  .ufo/waves/round-40/fixtures/run-c11-dags.py
fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987  fixtures/extracted/conform-v2-r39.py
b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520  fixtures/extracted/count-c7-r39.py
62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7  fixtures/extracted/gate-v2-bb1f2457.py
```

Also re-verified as inherited-and-landed:

- **Gate modification**: `git diff --stat bb1f2457 265a955 -- tools/mori-sources-appendonly.py` → 149 insertions(+), 48 deletions(-) — the v3 (P-C11) rewrite was wholly in the dead tree.
- **Generated fixtures**: 11 `survivor-*.py` + `conform-r39-conjunct-gutted.py` are in snapshot `c2ecbbc`'s tree (`git show --stat c2ecbbc`) and at 265a955 (`git show 265a955:.ufo/waves/round-40/fixtures/generated/conform-r39-conjunct-gutted.py` succeeds).
- **Witness fixtures** ×4 (`witness-token-entry.md`, `witness-dangling-row.md`, `witness-summary-only-live.txt`, `witness-comment-anchors.md`): consumed by the counter (`count-c8.py:518-541` opens all four; `conform.py:75` references the r39 summary-only witness). Present in the dead tree and at 265a955.
- **Corpus**: `corpus/evidence/sources-r40/S229.src` (869 lines), `corpus/knowledge/conform-scope-r40.md` (40 lines), `corpus/lessons/round-39-erratum.md` (28 lines) — all in `c2ecbbc`, landed at 265a955.
- **Predicate fidelity**: contract's P-C10 and P-C11 blockquotes are verbatim-contained (whitespace/quote-normalized) in `conform.py`'s and the gate's PREDICATE strings — both True; consistent with the landed `c10-after.txt` line `check predicate PASS`.
- **Scratch drafts** `scratch/selftest-v3-draft.txt` / `draft2.txt`: untracked during the dead launch (not in `3f8c0cd0…`), landed at 8d3badd. They record the dead launch's unfinished selftest debugging: draft1 = `pass=9 fail=2` (`timeout_scope_shadow` arm flipping only `timeout_scope`; `drain_bind_decoy` arm flipping nothing), draft2 = `pass=11 fail=0` — i.e. two selftest arms the dead launch left miswired, finished by the resume.

## 3. Changed / discarded

- **Three root strays — deleted, exist in no commit, recoverable from committed round-38 bytes.**
  - `git log --all --oneline -- bypass-none.py | bypass-wait.py | count-c1-r38.py` → empty for each; `git rev-list --all --reflog --objects | grep -E '(^|/)(bypass-none|bypass-wait|count-c1-r38)\.py'` → no hits; none appear in any snapshot root listing. They were never committed — untracked root files only.
  - Recoverability proven by execution: extracted `bb1f2457:.ufo/waves/round-39/fixtures/make-m19-bypass.py` and `bb1f2457:.ufo/waves/round-38/count-c1.py` to /tmp and ran `python3 make-m19-bypass.py bb1f2457 <lane> /tmp/strays-rebuild/out` → `GEN_EXIT=0`, "derived 2 drain(s) into bypass-none.py; bypass-wait.py from the primary communicate drain", producing exactly `bypass-none.py` (48715 B), `bypass-wait.py` (48322 B), `count-c1-r38.py` (48680 B). The three strays are the deterministic outputs of the tracked r38 counter bytes plus the tracked r39 builder (which docstrings name all three); their red behavior is recorded in r39 evidence `c8-red-none.txt`/`c8-red-wait.txt`. Precision note: the generator itself is committed under round-39; the source bytes and receipts are the round-38 side — deletion lost nothing.
- **`mori-conform-selftest-pqmzjj6u/` scratch** (nine `counter-*.py`): dead-launch on-lane selftest scratch, untracked at wave start (`git status` `??`), since removed — conform v3's `scratch` check moves selftest scratch off-lane (`c10-after.txt`: `check scratch PASS (mkdtemp_dir=True root=True)`).
- **`evidence/freeze-r40.txt` — not inherited**: header states "pinned: 2026-10-24T05:46:06Z by L1 mori-r40 attempt 1 (resumed); the prior launch died before persisting this receipt". Created by the resume; pins re-verified above.
- **S229 SOURCES.md placement — repaired post-tip**: at 265a955 the S229 row sat at line 292, appended after the Search-log paragraph (outside `## Registry`); `ede486b` moved it into the Registry table (HEAD: row at line 235, `## Registry` line 3 → `## Paths` line 237). E12.
- **`conform-v3-conjunct-gutted.py` — inherited bytes that landed late**: present as working-tree bytes during the dead launch but in **no commit at 265a955** (`git show 265a955:…` fails; landed only at ede486b, +804). The receipt `c10-after-conjunct.txt` (landed 8d3badd) therefore cited bytes uncommitted at the scored tip — same defect class the contract itself calls out as r39 finding 10.
- Current-wave sibling drift (not dead-launch residue, left untouched): working-tree modifications to `c10-after-selftest.txt` (adds `wall_seconds: 57.371` timing), `c10-after-conjunct.txt`/`c10-red-conjunct.txt` (command lines made absolute) — receipt refreshes; `scr-dag-{n,p,r}.txt` and `.scratch/<SeatName>/` are this wave's seat scratch.

## 4. Contract promises the landed bytes still owe

1. **Reproducibility of the conjunct receipts — VERIFIED PAID, replayed from committed bytes (101 s wall):**
   - `python3 …/fixtures/generated/conform-v3-conjunct-gutted.py 265a955cc…--selftest` → ten `FAIL <arm> … failing=['<arm>', 'selftest_conjunct'] (want [<arm>])`, `CONFORM_SELFTEST pass=0 fail=10`, exit 1 — body **line-identical** to the committed `c10-after-conjunct.txt` (machine-diffed, True).
   - `python3 …/fixtures/generated/conform-r39-conjunct-gutted.py bb1f2457 --selftest` → eight PASS, `CONFORM_SELFTEST pass=8 fail=0`, exit 0 — body **line-identical** to the committed `c10-red-conjunct.txt` (True).
2. **S229 registry placement — PAID at ede486b** (see §3); at the scored tip itself the row was misplaced (owed at scoring time).
3. **OPEN — wave-shape wording**: frozen contract line 171 promises "ONE v2 wave of **64 seats** (policy v2 band 64–128)"; the landed `w1-spec.json` carries **66** items (`jq '.items|length'` → 66; 8d3badd message: "66-seat v2, validated"). The contract is frozen, so the divergence is unreconciled prose — flagged for the integrator (append-only note or accepted band tolerance); this seat does not edit.
4. **Non-owed, checked**: `fixtures/make-ancestry-dags.py` appears in the contract only inside the finding-7/10 description quoting the r39 defect ("a path in no commit") — a mention, not a citation; the contract's other relative `fixtures/…` citations resolve under `.ufo/waves/round-40/fixtures/`. Citation audit over all repo-relative paths in contract.md: nothing else missing at HEAD.
5. **Debt (f)** (SIGTERM/grace): contract marks OPEN, operator-owned — not owed by the landed bytes.

Frontier observed while reconstructing: S229 present in `## Registry` at HEAD grounding C1 (`corpus/knowledge/conform-scope-r40.md`); `census-end.txt` ends `mori ok …/corpus/SOURCES.md`; lesson round-40 mines M23 (≥1 mistake satisfied); gate selftest receipt `pass=15 fail=0`, lane timing line carries 34 as-of ids including S226 with `stale_supersede=[]`.

## 5. Method & bounds

Read-only seat: only this report written inside the lane; stray rebuild confined to `/tmp/strays-rebuild`; no git/jj mutations, no sibling-lane access, no pacman, no tools installed (stock python3/git/jq). Verification commands: `git log/diff/show/ls-tree/rev-list/cat-file` (read-only), `sha256sum`, `jq`, `git show <rev>:<path>` extractions, and the two selftest replays named in §4.

Confidence: high on the tree-identity chain, pin equality, stray non-existence/recoverability, and receipt replay (all machine-checked). Inference, marked as such: `b434d01`'s partial tree read as a transient mid-operation snapshot (motivation unknowable from git alone); the dead launch's motivations beyond its persisted bytes are inference from M23 + the artifact set.
