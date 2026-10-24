measured 2026-10-23 (attempt 2, wave 2, seat `RevMisroot`)

# RevMisroot — fleet-root misroot sweep (r16–r17 seat-output misrooting class)

Item attacked: **seat-output misrooting** — a wave-2 seat resolving its `Report:` trailer against the
fleet root `/home/vgpnk/Projects/shokunin` instead of the lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`,
leaving w2 report files (or any untracked file whose content names `mori` or `round-36`) as strays in the
fleet repo, in particular under `/home/vgpnk/Projects/shokunin/.ufo/waves/round-36/`.

Scope: fleet root only, detection and report only (mori province). Nothing copied, moved, or deleted; no
git state change; lane repo read-only except this report file. Tooling installs: **none** (nothing to record).

---

## 1. Mandated command: `git status --porcelain` (no pathspec)

```
git -C /home/vgpnk/Projects/shokunin status --porcelain
```

Output (verbatim, 33 lines = 15 tracked-modified + 18 untracked entries):

```
 M .scratch/goal-20261023-hyaku-24h.md
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
 M .ufo/waves/hyaku/PHASE5.md
 M scripts/hyaku/hyaku.env
?? .omp/mcp.json
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
?? 0
?? AGENTS.md
?? bm.json
?? live.html
?? live_s228.html
?? nama.html
?? s395.txt
?? scripts/hyaku/__pycache__/
?? scripts/hyaku/append-closure.py.bak-20261023T040735Z
?? scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z
?? tf_bavelas.html
?? wb2.html
?? write
?? xc.xml
```

The 15 ` M ` entries are tracked-modified (watchdog baselines, hyaku 24h-session bookkeeping) — outside
this item (item = untracked files); listed for completeness. Note `scripts/hyaku/__pycache__/` is collapsed
here, so per-file content scanning used the `-uall` expansion below.

## 2. Untracked expansion: `git status --porcelain -uall`

```
git -C /home/vgpnk/Projects/shokunin status --porcelain -uall
```

19 untracked files (same as §1 except the collapsed dir expands):

```
?? .omp/mcp.json
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
?? 0
?? AGENTS.md
?? bm.json
?? live.html
?? live_s228.html
?? nama.html
?? s395.txt
?? scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
?? scripts/hyaku/__pycache__/wave-live.cpython-314.pyc
?? scripts/hyaku/append-closure.py.bak-20261023T040735Z
?? scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z
?? tf_bavelas.html
?? wb2.html
?? write
?? xc.xml
```

**Names vs `mori` / `round-36` / `r36`:** none of the 19 names contains any of them (verbatim list above;
the three `.ufo/state/*` names are `kotoba` / `kotodama` / `revenger` baselines).

## 3. Content scan of every scannable untracked file (16 of 19)

The three `.ufo/state/kotoba|kotodama|revenger.report-baseline` files are under the hard-bounds
never-touch path `/home/vgpnk/Projects/shokunin/.ufo/state/` and were **excluded from content reading**
(68 bytes each; mtimes 2026-10-23 15:04, 2026-10-23 15:17, 2026-10-21 14:54 −0300). This exclusion is
documented, not silent (see Residual gaps).

Command (untracked list cached at `/fast/scratch/hyaku/mori-r36/RevMisroot/untracked.txt`):

```
cd /home/vgpnk/Projects/shokunin && D=/fast/scratch/hyaku/mori-r36/RevMisroot && mkdir -p "$D" && git status --porcelain -uall | grep '^??' | cut -c4- > "$D/untracked.txt" && wc -l < "$D/untracked.txt" && while IFS= read -r f; do case "$f" in .ufo/state/*) printf 'EXCLUDED(never-touch .ufo/state) %s\n' "$f"; continue;; esac; n=$(grep -aicE 'mori|round-36' -- "$f" 2>/dev/null); n=${n:-0}; printf '%s MATCH_LINES=%s\n' "$f" "$n"; if [ "$n" -gt 0 ]; then grep -ainE -m 3 'mori|round-36' -- "$f" 2>/dev/null | cut -c1-200 | sed "s|^|    > |"; fi; done < "$D/untracked.txt"; echo SCAN_DONE
```

Output (verbatim):

```
19
.omp/mcp.json MATCH_LINES=0
EXCLUDED(never-touch .ufo/state) .ufo/state/kotoba.report-baseline
EXCLUDED(never-touch .ufo/state) .ufo/state/kotodama.report-baseline
EXCLUDED(never-touch .ufo/state) .ufo/state/revenger.report-baseline
0 MATCH_LINES=0
AGENTS.md MATCH_LINES=0
bm.json MATCH_LINES=0
live.html MATCH_LINES=0
live_s228.html MATCH_LINES=0
nama.html MATCH_LINES=2
    > 251:		<li id="menu-item-11660" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-11660"><a href="https://www.namuseum.gr/en/to-moyseio/istoria-toy-moyseioy/the-rescue-of-the-st
    > 424:		<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-11660"><a href="https://www.namuseum.gr/en/to-moyseio/istoria-toy-moyseioy/the-rescue-of-the-statues/">Memories 1940
s395.txt MATCH_LINES=0
scripts/hyaku/__pycache__/append-closure.cpython-314.pyc MATCH_LINES=0
scripts/hyaku/__pycache__/wave-live.cpython-314.pyc MATCH_LINES=0
scripts/hyaku/append-closure.py.bak-20261023T040735Z MATCH_LINES=0
scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z MATCH_LINES=0
tf_bavelas.html MATCH_LINES=0
wb2.html MATCH_LINES=0
write MATCH_LINES=0
xc.xml MATCH_LINES=0
SCAN_DONE
```

The `.pyc` files were scanned with `grep -a` (binary read as text): 0 matches each.

**The single hit, `nama.html` (68865 bytes), is a byte-level false positive.** Both matched lines are a
scraped National Archaeological Museum of Athens menu where the case-insensitive substring `mori` falls
inside the English word "Memories" ("Memories 1940"). Disambiguation commands and observed outputs:

```
cd /home/vgpnk/Projects/shokunin && grep -cE 'mori' nama.html
→ 2
cd /home/vgpnk/Projects/shokunin && grep -cniE '\bmori\b|round-36|mori-shokunin' nama.html
→ 0
```

No word-boundary `mori`, no `mori-shokunin`, no `round-36` anywhere in the file → it names neither the
mori lane nor round-36. Reported anyway because the sweep predicate is byte-level; disposition is L1's.

## 4. Mandated check: no w2 report files under `/home/vgpnk/Projects/shokunin/.ufo/waves/...`

1. **Path probe (decisive):** `/home/vgpnk/Projects/shokunin/.ufo/waves/round-36` does not exist at the
   fleet root (directory read + glob both: `Path not found: .ufo/waves/round-36`). The trailer
   `.ufo/waves/round-36/w2/RevMisroot.md` resolved against the fleet root therefore cannot exist —
   no misrooted w2 report is possible at the probed location, regardless of ignore rules.
2. **Glob `/home/vgpnk/Projects/shokunin/.ufo/waves/**/w2/**`** (hidden on, gitignore off): **no files**.
3. **Glob `/home/vgpnk/Projects/shokunin/.ufo/waves/**/*w2*`**: only entries are an **empty** `round-12/w2/`
   directory (also empty per `round-12/w2/*` glob) and pre-existing, unrelated session dirs
   (`kaika/`, `kaika-w2j/`, `shokunin-train-20261013-w2/`, other `shokunin-train-*-wNN/`) containing no
   round-36 seat reports (dated 3d–1w ago, before this round).
4. **Attribution of fleet `.ufo` entries that DO contain the string `round-36`** (glob
   `/home/vgpnk/Projects/shokunin/.ufo/**/*round-36*`) — all outside `.ufo/waves/`, all tracked
   infrastructure, none seat output:
   - `.ufo/prompts/{mori,kake,kumitate}-round-36.md` and `.ufo/prompts/closure/{kake,kumitate}-round-36.md`:
     `git ls-files --error-unmatch` → TRACKED for all five (one per lane: mission-prompt registry).
   - `.ufo/reports/round-36/` containing only `kake.md` (10733 B, 2026-10-22 23:35), `kotodama.md`
     (3817 B, 2026-10-19), `kumitate.md` (15911 B, 2026-10-21): `git check-ignore -v` exit=1 (not
     ignored) and absent from untracked status ⇒ tracked; this is the per-lane report ledger, has no
     `w2` files and no mori entry yet (round in progress). No mori lane file missing-action flagged —
     lane report placement is L1's mechanism, not a w2-seat misroot.

## 5. Saturation — what was checked

- exact mandated `git status --porcelain` (§1, verbatim) — untracked entry set captured;
- `git status --porcelain -uall` (§2) — 19 untracked files, all accounted for: 16 content-scanned, 3
  excluded by the `.ufo/state/` never-touch bound (documented above, not silent);
- content regex `mori|round-36` (`grep -a -i -c`, then line samples) over all 16 scannable files;
  15× zero, 1× substring false positive disproven by word-boundary/`round-36` re-check (§3);
- untracked file NAMES vs `mori` / `round-36` / `r36` — none (§2);
- fleet `.ufo/waves/round-36` existence — absent (§4.1);
- fleet `.ufo/waves/**/w2/**` and `**/*w2*` — no w2 report files (§4.2–4.3);
- fleet `.ufo/**/*round-36*` — tracked prompt/report-ledger infra only, attributed (§4.4);
- tooling installs — none performed.

## Residual risk / verification gaps

- Contents of the three `.ufo/state/{kotoba,kotodama,revenger}.report-baseline` files unverified
  (hard-bounds never-touch `.ufo/state/`). They are 68-byte watchdog baselines for non-mori lanes; a
  `mori` mention there would be bookkeeping, not seat output. This is the only unscanned content in the
  untracked set.
- Tracked files (including the 15 modified) were not content-scanned — item scope is untracked strays.
- Unrelated fleet-root slop observed and left in place (no remediation in mori province; L1 owns the
  sweep disposition): lost-redirect artifacts `0` (31 B) and `write` (25 B), scrape files `live.html`,
  `live_s228.html`, `nama.html`, `tf_bavelas.html`, `wb2.html`, `bm.json`, `xc.xml`, `s395.txt` (0 B),
  `AGENTS.md`, `.omp/mcp.json`, `scripts/hyaku/__pycache__/`, two `.bak-*20261023T040735Z` files — none
  references mori or round-36 (§3).

VERDICT: PASS — no untracked file in the fleet root names `mori` or `round-36` (one byte-level
"Memories" substring false positive documented and disproven), and no w2 report file exists under
`/home/vgpnk/Projects/shokunin/.ufo/waves/` (the `round-36` directory is absent there entirely).
