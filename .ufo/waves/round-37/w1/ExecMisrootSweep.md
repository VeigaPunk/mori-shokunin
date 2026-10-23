# [seat ExecMisrootSweep] Misroot sweep — fleet-root untracked files naming mori / round-37

**Item attacked:** fleet-root misrooting of mori round-37 seat artifacts. Target command
(mandated, no pathspec): `git -C /home/vgpnk/Projects/shokunin status --porcelain`.
Acceptance: list every untracked candidate whose content names `mori` or `round-37`; state
whether any is a mori round-37 seat file written to the fleet root.

Fleet root = `/home/vgpnk/Projects/shokunin` (read-only for this seat).
Lane repo  = `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only; this report is the
only file written).

## 1. Mandated command output

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
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
?? .ufo/waves/round-34/
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

Raw capture: `/fast/scratch/hyaku/mori-r37/ExecMisrootSweep/status-porcelain.txt`
(also `status-final.txt`, `status-porcelain-all.txt`).

## 2. Complete untracked inventory (20 files, `--untracked-files=all`)

`git ls-files --others --exclude-standard` expands the two directory entries
(`.ufo/waves/round-34/` → 1 file, `scripts/hyaku/__pycache__/` → 2 files) to exactly
**20 untracked files**. Every one was content-scanned with a binary-safe grep for
`mori|round-37`:

```
$ for f in $(git ls-files --others --exclude-standard); do n=$(grep -a -c -E 'mori|round-37' "$f"); printf '%-3s %s\n' "$n" "$f"; done
0   .omp/mcp.json
0   .ufo/state/kotoba.report-baseline
0   .ufo/state/kotodama.report-baseline
0   .ufo/state/revenger.report-baseline
0   .ufo/waves/round-34/w1/ReviewDevReceipts.md
0   0
0   AGENTS.md
0   bm.json
0   live.html
0   live_s228.html
2   nama.html
0   s395.txt
0   scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
0   scripts/hyaku/__pycache__/wave-live.cpython-314.pyc
0   scripts/hyaku/append-closure.py.bak-20261023T040735Z
0   scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z
0   tf_bavelas.html
0   wb2.html
0   write
0   xc.xml
```

Candidate table also saved to
`/fast/scratch/hyaku/mori-r37/ExecMisrootSweep/candidate-table.txt`; content heads of all
20 to `.../heads.txt`.

### The single content-hit candidate

**`nama.html`** (untracked, fleet root, 68855 bytes, mtime 2026-10-22 14:24).

```
$ grep -n -a -o -E '.{0,20}mori.{0,20}' nama.html
251:-of-the-statues/">Memories 1940-1944</a></li
424:-of-the-statues/">Memories 1940-1944</a></li
$ grep -c -a -w -i 'mori' nama.html     -> 0
```

Content head: `<!DOCTYPE html><html lang="en-US" xmlns:og="http://opengraphprotocol.org/schema/" ...`
`<title>Page not found - National Archaeological Museum</title>` — a scraped Greek museum
nav page (Cloudflare/404 capture). Both `mori` occurrences are the substring inside the
English word **"Memories"**; word-boundary `mori` count is **0**. This is a **false
positive**, not a mori-lane reference.

### No candidate names round-37

Zero untracked files at the fleet root contain `round-37` (case-sensitive and
case-insensitive). Zero untracked paths contain `round-37` or `mori` in the path itself.

## 3. Is any mori round-37 seat file misrooted at the fleet root? — NO

Corroborating measurements:

| check | command | observed |
|---|---|---|
| fleet root has no round-37 wave dir | `ls -d /home/vgpnk/Projects/shokunin/.ufo/waves/round-37` | `No such file or directory` |
| no tracked fleet-root round-37 seat paths | `git ls-files \| grep '^\.ufo/waves/round-37/'` | empty |
| no seat-named file at fleet root | `find . -maxdepth 6 \( -name 'Exec*.md' -o -name 'Rev*.md' -o -name 'Crit*.md' -o -name 'Mut*.md' -o -name 'Lab*.md' -o -name 'Scout*.md' -o -name 'Conn*.md' \) -not -path './*-shokunin/*' …` | only `./.ufo/waves/round-34/w1/ReviewDevReceipts.md` |
| mori r37 seat reports live in the lane | `ls mori-shokunin/.ufo/waves/round-37/w1/*.md \| wc -l` | **59** (all present, e.g. `ExecC1Seed41.md`, `RevC1Predicate.md`, `MutC2CapArm.md`, `ScoutFreeze.md`, `ScribeLog.md`) |
| lane r37 tree is the only home of r37 artifacts | `find . -maxdepth 4 \( -name 'count-c1.py' -o -name 'count-c2.py' -o -name 'freeze-r37*' -o -name 'c1-before-memo*' \) -not -path '*/.git/*'` | **empty at fleet root** (no copies) |
| no byte-identical lane-r37 file misrooted at fleet root | `sha256sum` over all 89 files of `mori-shokunin/.ufo/waves/round-37` (excl. `__pycache__`) ∩ `sha256sum` of the 20 fleet-root untracked files | only the SHA of the **empty file** (`e3b0c442…b855`) matches, i.e. `s395.txt` (0 bytes) vs `mori-shokunin/.ufo/waves/round-37/w1-validate.log` (0 bytes) — coincidental, not a copy |
| no fleet-root file carries r37 seat markers | `grep -rIl -E 'freeze-r37\|c1-before-memo\|P-C1\|drift-live-r37\|round-37/w1' --exclude-dir=.git --exclude-dir=.jj --exclude-dir='*-shokunin' --exclude-dir=.tower .` | hits only in tracked historical reports `.ufo/reports/round-{31,32,33,34,35,37}/mori.md` and tracked `MANIFEST.json` — no untracked file |
| the only fleet-root r37/mori-named tracked paths are legitimate fleet-level artifacts | `git ls-files .ufo/reports/round-37/mori.md .ufo/prompts/mori-round-37.md` | both **tracked** (committed fleet report + dispatch prompt). `.ufo/reports/round-37/mori.md` shows as ` M` in the working tree — a tracked fleet report under revision, not an untracked seat file |

The mori round-37 wave tree, its evidence receipts, its 59 seat reports and the counter
scripts exist **only** under `mori-shokunin/.ufo/waves/round-37/`. The lane repo's own
status confirms r37 seat outputs are being written in place (e.g. `?? .ufo/waves/round-37/w1/ExecC2Twice.md`,
`?? .ufo/waves/round-37/evidence/drift-live-r37-tip.txt`) and are not echoed at the fleet
root.

## 4. Adjacent observations (outside the verdict scope — no action taken)

1. **`.ufo/waves/round-34/w1/ReviewDevReceipts.md`** — an untracked **seat report** sitting at
   the *fleet root* under a round-34 wave path. Content head:
   `# [seat ReviewDevReceipts] Amendment-6 dev receipts — internal-consistency audit`.
   Its content names **round-32 / round-33 / round-34 only** (0 hits for `mori`, 0 for
   `round-37`); the report itself states its lane was `tameshi` and scratch was
   `/fast/scratch/hyaku/tameshi-r34-seats/ReviewDevReceipts/`. It is therefore a **round-34
   tameshi** artifact, **not** a mori round-37 seat file, and it does not affect this
   verdict. It is nevertheless a seat-shaped file at the fleet root and is named here so the
   parent can route it (routing decision, not this seat's).
2. **Transient root entry `mori-shukin/`** (typo-shaped, sibling of `mori-shokunin/`) was
   observed by `ls -d */` / `find -maxdepth 1` in two early calls but was unresolvable
   (`stat`, `ls -ld`, `os.listdir`, `os.scandir`) in every probe immediately after, and it
   never appeared in `git status --porcelain` output. It was an empty directory
   (`size 8`) and vanished; nothing of it is in the untracked set. Recorded for awareness
   only — no file was written there by this seat.
3. Remaining untracked files are ordinary fleet-root debris from other lanes/operators:
   scraped/captcha HTML (`bm.json`, `live.html`, `live_s228.html`, `tf_bavelas.html`,
   `wb2.html`, `xc.xml`), an operator agent URI (`write` → `agent://U100N079H334f935b`),
   a stray counter output (`0` → `NF=13 cells=11 double_quotes=0`), an empty `s395.txt`,
   an untracked `AGENTS.md` (fleet-root protocol copy), three `.ufo/state/*.report-baseline`
   files for kotoba/kotodama/revenger, `.omp/mcp.json`, and hyaku `__pycache__`/`.bak`
   artifacts. None names mori or round-37.

## 5. Files changed

- `.ufo/waves/round-37/w1/ExecMisrootSweep.md` (this report, in the lane repo) — the only
  file written.
- Scratch (not part of the repo): `/fast/scratch/hyaku/mori-r37/ExecMisrootSweep/`
  (`status-porcelain.txt`, `status-porcelain-all.txt`, `status-final.txt`,
  `candidate-table.txt`, `heads.txt`).

No tooling was installed or upgraded for this seat (no pacman, no uv/npx/cargo action);
the sweep used only `git`, `grep`, `ls`, `find`, `sha256sum`, `python3` (stdlib) — all
pre-existing.

**VERDICT: PASS** — the only fleet-root untracked file whose content contains the string
`mori` is `nama.html`, where it occurs solely inside the English word "Memories"
(word-boundary `mori` count = 0); **no** untracked file at the fleet root names `round-37`;
and **no** mori round-37 seat file (report, evidence receipt, or counter script) is
misrooted at the fleet root — all 59 r37 seat reports and the r37 contract/counters/
evidence live under `mori-shokunin/.ufo/waves/round-37/`.
