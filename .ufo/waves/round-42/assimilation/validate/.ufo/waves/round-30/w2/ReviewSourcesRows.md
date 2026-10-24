# ReviewSourcesRows — SOURCES rows S156–S160 vs the SOURCES contract

**Verdict: agree — the five rows conform to the frozen v1 contract; no actionable defect found.**

Scope: `corpus/SOURCES.md:162-166` (rows S156–S160) attacked against CORPUS.md
`## SOURCES.md — where a shokunin learns` (`/home/vgpnk/Projects/shokunin/CORPUS.md:64-155`),
amendment A1 4b (one URL per id), and the round-start census receipt.
Evidence drawn from the lane at master `95cd794` (`git rev-parse master`); the measured
tip in the wave context (`ad0f047`) is two commits back — both used-by targets exist at
the *current* tip, verified below.

## Checks run (all pass)

1. **Column shape.** Contract: 11 cells → `NF==13` under `-F'|'` (`CORPUS.md:136-137`).
   - Working copy: `awk … NF!=13` prints `0` malformed across all 160 rows.
   - Committed tip: `git show master:corpus/SOURCES.md | awk … NF!=13` prints `0`.
   - Each of lines 162–166 has exactly 12 pipes / 11 cells; no `|` inside any cell
     (would have raised the malformed count).

2. **Tier.** All five rows `A`, kind `code` (`SOURCES.md:162-166`). The enum one-liner
   (`CORPUS.md:144-145`) prints nothing — no tier/kind/status violations, no
   `community`-as-A inflation. A-tier is justified: each scope is a pinned release tag
   (`v262`) or a specific commit patch, i.e. primary/authoritative for that scope
   (`CORPUS.md:93-95`). Kind `code` for a `.patch` matches existing precedent (S155).

3. **Status.** All five `mined`, and every `mined` row must be cited by ≥1 `used-by`
   path (`CORPUS.md:103-104`). Both used-by targets cite all five ids:
   - `corpus/lessons/round-30.md` — prose cites S156–S160 at lines 10–14; `## Gate`
     admits each row (`:114` S156, `:116` S157, `:126` S158, `:135` S159, `:138` S160);
     row-change log at `:144-148`. `git show master:corpus/lessons/round-30.md | grep -c
     'S15[6-9]\|S160'` → 38.
   - `corpus/knowledge/earlyoom-invocation-scope-r30.md` — `source:` line 1 names all
     five; decision-table `evidence` column cites S156–S160 at rows `:101-112`;
     `grep -c` at tip → 22.

4. **Recheck.** S156/S157/S158/S160 `on-release`, S159 `180d` — all inside the contract
   cadence enum `90d · 180d · on-release` (`CORPUS.md:105-106`). `opened` is ISO
   `2026-10-22` on every row, matching the Gate access timestamps.

5. **used-by targets exist at the tip.** `git ls-tree 95cd794 -- corpus/lessons/round-30.md
   corpus/knowledge/earlyoom-invocation-scope-r30.md` returns blobs `3c6ac812…` and
   `c4a45b30…`. The contract's missing-used-by one-liner (`CORPUS.md:146-147`) prints
   nothing over the working copy; `git diff master -- corpus/SOURCES.md` is empty.

6. **One URL per row.** Each `source` cell holds exactly one `https://` URL
   (`SOURCES.md:162-166`). S156 and S160 name companions "cited by path only"
   (`src/systemctl/systemctl-show.c`; `src/journal/journalctl-filter.c`,
   `src/journal/journalctl-util.c`) — path citations, not URLs, so the one-URL rule is
   met; the lesson logs this explicitly (`round-30.md:146-147`, "contract A1 4b").

7. **No URL duplicating an older row.** Grep for
   `bus-print-properties|journald-manager\.c|journalctl\.c|edd3d9438dc…|v262/src/core/unit\.c`
   across **all 21 lane registries** (`find -maxdepth 3 -name SOURCES.md`, then grep on
   the enumerated files) returns only mori's own lines 162–166. Within mori,
   `v262/src/core/unit.c` is a different URL than S036's commit-pinned
   `cf8ebfc6159…/src/core/unit.c` (`SOURCES.md:42`). The Gate table documents the
   rejected duplicate candidates and why (`round-30.md:117-140` — e.g. `journalctl.xml`
   rejected as S122's URL, `earlyoom.service.in` rejected as S120's).

8. **Census validate vs round-start receipt.** Command run:
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin mori` → **exit 0**. Output is byte-identical to
   `.ufo/waves/round-30/evidence/census-start.txt`: the same ten `W04` warnings
   (S035, S037, S073–S076, S147–S150, all "duplicate url … across scopes") and the
   closing `mori ok`. **No warning names S156–S160** — the new rows add zero warnings.

9. **Registry integrity around the rows.** Row count `grep -cE '^\|[[:space:]]*S[0-9]{3,}'`
   = 160, ids run S001–S160 with no duplicates (`uniq -d` empty) — S156–S160 are the
   next unused ids, appended after S155 (append-only rule 2 respected: new lines only;
   `git status` shows the registry unmodified vs tip).

## Observations (not defects)

- **S157 anchor carries no sha256** in the row (`SOURCES.md:163`), unlike S156/S158.
  The contract requires "line plus revision" (`CORPUS.md:99-100`); `src/core/unit.c:2763-2777
  ; tag v262 = commit 8cc40e0c…` satisfies it, and the Gate records the sha256
  (`round-30.md:116`). [INFERENCE] Consistent with S143-style rows that omit a hash.
- **S159 `recheck` = `180d`** where `on-release` would arguably fit an immutable patch
  better; `180d` is strictly more conservative. Both are contract-legal.
- The Gate itself (`round-30.md:114` col "located quote" for S156) carries three quoted
  fragments summing to ~14 words — under the ≤25-word rule (rule 1). Quote fidelity is
  the Reopen* scouts' lane, not re-derived here.

## Residual risk / verification gaps

- I did **not** re-fetch the five URLs or re-hash the excerpts (`corpus/evidence/
  sources-r30/S156.txt..S160.txt`); byte-freshness is covered by the wave-2 Reopen
  seats and the Gate receipts.
- The census W04 warnings are pre-existing (present at round start) and name older
  rows; they are cross-scope duplicates by design of earlier rounds, not this item's
  regression.
- Tip moved during review (measured `ad0f047` → current `95cd794`); rows and both
  used-by citations were re-verified at `95cd794`.

## Bounds compliance

- Read-only git only (`rev-parse`, `log`, `ls-tree`, `show`, `diff`, `status`); no
  writes to lane git state. Writes: this report only.
- No installs performed; no pacman transaction attempted (host-wide pause honored).
- No host settings, unit names, session identifiers, or `/etc/default/earlyoom`
  values copied; the rows quote upstream systemd/earlyoom source only.
