# ScoutMisroot — fleet untracked files vs mori r38

Axes: complete porcelain coverage; word-boundary lane/round naming (not substrings); byte sizes; no deletes.

Command (no pathspec), fleet repo `/home/vgpnk/Projects/shokunin`, re-run matched the first capture:

```
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
?? .omp/mcp.json
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
?? .ufo/waves/hyaku/inline-run-20261023.md
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

Nothing deleted. No tools installed. Default porcelain collapses `scripts/hyaku/__pycache__/`; `git status --porcelain -uall` expands it to the two `.pyc` rows below. Both were scanned.

Predicate: content names this lane/round iff a word-boundary `mori` / `mori-shokunin` / `MoriR38`, or `round-38` / `round 38`, is present. Full-file byte scan (Python, every untracked byte including the pycs).

## Candidate (names this lane/round)

| path | bytes | names mori r38 | mori seat wrote it |
|---|---:|---|---|
| `.ufo/waves/hyaku/inline-run-20261023.md` | 3989 | YES | NO — hyaku driver card |

Evidence, `inline-run-20261023.md`:

- Line 43: `| mori | 38 | 1 | 19:34 |` — lane `mori` and round `38` in the same claims row. Byte offsets of the two `mori` tokens: 2176 and 3707.
- Line 66: `kotodama/kumitate/kama/mori attempt counters` — lane name only.
- Lines 3–6: "Parent omp session IS the driver"; the card lists nine lanes (tameshi 35, mado 28, kake 44, kotodama 64, kotoba 62, kumitate 50, kama 31, mori 38, chousa 37). No `mori-shokunin`, no `MoriR38`, no `.ufo/waves/round-38/` path.

Inference (high): a fleet/hyaku orchestrator wrote the card; a mori seat did not. It is still the one untracked file that names this lane and round, so it is the candidate. Untracked, so there is no commit author.

## Every other untracked path (does not name this lane/round)

| path | bytes | names mori r38 | what the bytes are |
|---|---:|---|---|
| `.omp/mcp.json` | 285 | no | MCP stub, server `rea`, `rea-agents@6.7.0` |
| `.ufo/state/kotoba.report-baseline` | 68 | no | `63 e3b0c442…` (empty-blob sha256) |
| `.ufo/state/kotodama.report-baseline` | 68 | no | `64 e3b0c442…` |
| `.ufo/state/revenger.report-baseline` | 68 | no | `62 e3b0c442…` |
| `0` | 31 | no | `NF=13 cells=11 double_quotes=0` |
| `AGENTS.md` | 5921 | no | fleet-root agent guide; generic `lane`, no `mori` |
| `bm.json` | 5563 | no | Cloudflare "Just a moment…" HTML (misnamed) |
| `live.html` | 57113 | no | museum.ie collections page |
| `live_s228.html` | 5196 | no | Anubis challenge page (OpenEdition) |
| `nama.html` | 68855 | no | namuseum.gr 404. Substring only: "Memories" at offsets 35264 and 47416 — not the token `mori` |
| `s395.txt` | 0 | no | empty |
| `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` | 10738 | no | bytecode; zero `mori` bytes |
| `scripts/hyaku/__pycache__/wave-live.cpython-314.pyc` | 10708 | no | bytecode; zero `mori` bytes |
| `scripts/hyaku/append-closure.py.bak-20261023T040735Z` | 5757 | no | hyaku closure helper backup; generic `lane` |
| `scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z` | 2857 | no | hyaku fleet-commit backup; generic `lane` |
| `tf_bavelas.html` | 5583 | no | Cloudflare "Just a moment…" HTML |
| `wb2.html` | 620 | no | archive.org Wayback bot-block page |
| `write` | 25 | no | `agent://U100N079H334f935b` |
| `xc.xml` | 237 | no | Perseus "Too many requests" HTML |

No untracked **filename** contains `mori` or `round-38`.

## Not a candidate (tracked dirty, lane in the path)

`.ufo/state/mori.report-baseline` is ` M` (tracked, worktree-modified), not `??`. It names the lane in the path. It is outside the untracked set. Not read (driver-runtime path). Not deleted.

## Unknowns

- Filesystem owner is not a seat id; authorship of the run card is from its own text, not from `git log` (untracked).
- Whether some other seat dropped the scraped HTML / `0` / `write` / `s395.txt` is open. None of those bytes name mori or round 38.
