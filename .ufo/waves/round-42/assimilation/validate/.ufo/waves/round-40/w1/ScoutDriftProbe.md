# ScoutDriftProbe — mori-r40-w1 seat report

**Question:** did `tools/mori-source-drift.py` (the drift-probe target the `anchors_v2` check reads, via `.ufo/waves/round-40/count-c8.py`) change between round-39 tip `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3` and scored tip `265a955cc67be4eae97d2dc5a9338a25f31eb29b`?

**Answer: NO — byte-identical at both revs and in the working tree. No silent change; anchors_v2 reads the same bytes it did at r39.**

## Commands run (all in /home/vgpnk/Projects/shokunin/mori-shokunin)

1. `git log --oneline bb1f2457..265a955cc -- tools/mori-source-drift.py`
   Output: **empty** (no commits in the range touch the path). For contrast, the same range has exactly one commit total: `265a955 round-40: instruments — conform v3 (P-C10), gate v3 (P-C11), S229, r39 erratum`, and it does not touch this file.

2. `git diff bb1f2457 265a955cc -- tools/mori-source-drift.py | head -50`
   Output: **empty** — zero diff.

3. `git rev-parse bb1f2457:tools/mori-source-drift.py 265a955cc:tools/mori-source-drift.py`
   ```
   162ee87b5b0789c6815f967f3db93d277bab38d9
   162ee87b5b0789c6815f967f3db93d277bab38d9
   ```
   Same blob at both revs.

4. `git hash-object tools/mori-source-drift.py` → `162ee87b5b0789c6815f967f3db93d277bab38d9` (working tree == committed blob; `git status --porcelain -- tools/mori-source-drift.py` → empty). File is 466 lines.

5. `git log --oneline -3 -- tools/mori-source-drift.py` — last touched at `e57c58b` (round-37 freeze, "drift hardening entry"); before that `1caa242` (round-36 read-cap + redirect policy) and `bf0df77` (round-36 probe creation).

6. Consumer confirmation: `grep -n "anchors_v2\|source-drift" .ufo/waves/round-40/count-c8.py` → `TOOL_REL = "tools/mori-source-drift.py"` (line 56), `ENTRY_REL = "corpus/knowledge/source-drift-content-anchor-r38.md"` (line 57), `check_anchors_v2` at line 290, called at line 466; anchors are read from `tool_text` (line 475 joins workdir + `mori-source-drift.py`).

7. Spot-check (read-only, beyond the brief): extracted the three `anchor:` lines from `corpus/knowledge/source-drift-content-anchor-r38.md` —
   - `FETCH_MAX_BYTES = 4 * 1024 * 1024`
   - `if not _public_redirect_target(final):`
   - `return "drifted"`
   All 3 occur byte-exactly in the working-tree tool (`missing: []`). Since the blob is identical at bb1f2457 and 265a955cc, anchors_v2 sees identical content at both revs.

## Notes / boundaries

- The prose line "1. **Anchors.** Every line of this lane's round-38 knowledge entry beginning `anchor:` names a code" contains the substring "anchor:" but is not an anchor line (does not start with `anchor:`); `anchors_from` in count-c8.py line 235 parses only real anchor lines. An earlier naive substring parse of mine flagged it; corrected, no real anchor is missing.
- `cmp` against fleet repo: `/home/vgpnk/Projects/shokunin/tools/mori-source-drift.py` does not exist in the fleet worktree — this is a lane-only tool. No drift there.
- No pacman transactions; no tools installed (nothing needed). No files mutated; no git/jj mutations; read-only seat honored.

**Residual risk: none found.** The C7/anchors_v2 surface is stable across the r39→r40 boundary.
