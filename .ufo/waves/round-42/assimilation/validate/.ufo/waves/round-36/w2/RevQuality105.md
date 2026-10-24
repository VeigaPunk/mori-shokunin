# RevQuality105 — Criterion 105 witness re-derivation (round 36, wave 2)

Seat: `mori-r36-w2-RevQuality105-11` (leaf; no subagent dispatch). Item attacked: **Criterion 105**
(`corpus/QUALITY.md:837-843`) — the witness it rests on: the seven real rows the frozen round-36
P-C1 probe counts `drifted` (S156–S160, S176, S177) are representation differences, not source changes,
per `.ufo/waves/round-36/w1/MineCopyFidelity.md`. This report re-derives that witness independently
today (2026-10-23, ~12:1x–12:3xZ), one fetch per URL, and compares against the digest recorded at open
time (copy header or lesson Gate).

Scratch: `/fast/scratch/hyaku/mori-r36/RevQuality105/` (live fetches `live_S###`). No tools installed
(used `curl` and `python3` already present on the host; `curl` 8.x, `python3` 3.14). Verification below
is the only exercised check.

## Method

For each of the seven rows, fetch the row's URL (redirects followed, `--max-time 90`, body saved to
scratch) and hash:

```
curl -sSL --max-time 90 -o live_S### <URL> && sha256sum live_S###
```

Compare the live sha256 with (a) the copy-header `sha256:` field for the five excerpts
(`corpus/evidence/sources-r30/S###.txt:3`) and (b) the committed full-page snapshot bytes for S176/S177
(`corpus/evidence/sources-r32/S###.src`), which the round-32 Gate recorded.

## Result table

| row | URL | committed copy (sha256 first 16) | Gate sha (first 16) | live sha256 (first 16) | verdict |
|---|---|---|---|---|---|
| S156 | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c` | header `b56aa781…` | `b56aa781…` (round-30.md:114) | `b56aa781be9c29b6…` | header sha == live full-doc sha |
| S157 | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c` | header `47e98d39…` | `47e98d39…` (round-30.md:116) | `47e98d394462e05b…` | header sha == live full-doc sha |
| S158 | `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c` | header `428dc830…` | `428dc830…` (round-30.md:126) | `428dc8308d5caf70…` | header sha == live full-doc sha |
| S159 | `https://github.com/rfjakob/earlyoom/commit/edd3d9438dc564da7b694e5c96c9b3bc63bef2ac.patch` | header `dc5a771c…` | `dc5a771c…` (round-30.md:135) | `dc5a771c9ed17875…` | header sha == live full-doc sha |
| S160 | `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c` | header `285b3d0c…` | `285b3d0c…` (round-30.md:138) | `285b3d0c1217b9a3…` | header sha == live full-doc sha |
| S176 | `https://docs.python.org/3/library/unicodedata.html` | `d3d261bc…` (55,620 B) | `d3d261bc…` (round-32.md:66) | `a82233d1a4dedfe2…` (55,620 B) | footer-only drift (below) |
| S177 | `https://docs.python.org/3/library/html.html` | `650c53ac…` (20,100 B) | `650c53ac…` (round-32.md:67) | `fe0d61d9e8cef672…` (20,100 B) | footer-only drift (below) |

Full live sha256 values:

```
b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a  live_S156
47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7  live_S157
428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2  live_S158
dc5a771c9ed178751c0473c9ada89152e70b9da13a048b0af30df6bbb1f2a9a1  live_S159
285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab  live_S160
a82233d1a4dedfe297b6fe9a2dc263ad48da3c8b7a2acc05b62e2c90abb1cf37  live_S176
fe0d61d9e8cef672b42a96cb9fba27fbeccd9be66b127ec2f9c469e31e0d880e  live_S177
```

Full committed-snapshot shas (S176/S177) and copy-header shas (S156–S160) — see
`corpus/evidence/sources-r32/S176.src`, `S177.src` and `corpus/evidence/sources-r30/S156.txt:3` etc.:
`d3d261bcde4906ce9685d8e362a7bbb0dc4b254b1fc12f70ec46a9db65e77375` (S176.src),
`650c53ac7695b816427335a6fbdf3852c41c01d7458f3b502c2af4e916441bb0` (S177.src); headers
`b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a`,
`47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7`,
`428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`,
`dc5a771c9ed178751c0473c9ada89152e70b9da13a048b0af30df6bbb1f2a9a1`,
`285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab`.

## S156–S160: excerpt body-line fidelity

Each committed excerpt is a 5-field header plus tab-prefixed `N<TAB>text` lines covering the `lines`
span. For each file, every body line was compared to the live fetched file's line at its stated number
(script under scratch; output below). All lines match; the excerpt is a true selection of live lines, so
the only difference between the committed file and the full document is the header + line-number prefix +
subsetting — a representation difference, not a source change.

```
S156 body_lines_checked= 73 bad= []
S157 body_lines_checked= 17 bad= []
S158 body_lines_checked=  6 bad= []
S159 body_lines_checked= 27 bad= []
S160 body_lines_checked= 39 bad= []
```

## S176/S177: full-page diff against the live body

Observed commands and output:

```
$ cmp live_S176 <repo>/corpus/evidence/sources-r32/S176.src
live_S176 .../S176.src differ: char 55367, line 721
$ diff live_S176 .../S176.src
721c721
<       Last updated on Oct 23, 2026 (18:17 UTC).
---
>       Last updated on Oct 23, 2026 (00:01 UTC).

$ cmp live_S177 .../S177.src
live_S177 .../S177.src differ: char 19847, line 370
$ diff live_S177 .../S177.src
370c370
<       Last updated on Oct 23, 2026 (18:17 UTC).
---
>       Last updated on Oct 23, 2026 (00:01 UTC).
```

`cmp -l` counts exactly **4 differing bytes** per row; sizes are identical to the committed snapshots
(55,620/20,100 B). The only difference in 74,720 compared bytes is the docs.python.org build footer
timestamp (`00:01 UTC` at commit → `18:17 UTC` now); the page was rebuilt several times on
2026-10-23. The committed bytes equal the round-32 Gate's recorded shas byte-for-byte, so the snapshot is
exactly what the Opening round hashed; the "drift" is the page's own build cycle. The admitted quotes
(S176.src:516-517,533-536; S177 unescape entry) sit outside the changed footer line and are unchanged in
the live body.

## Cross-checks

- Gate registry digests: `round-30.md:114,116,126,135,138` carry `b56aa781…`, `47e98d39…`,
  `428dc830…`, `dc5a771c…`, `285b3d0c…` — identical to the copy headers and to today's live shas.
  `round-32.md:66-67` carry `d3d261bc…` / `650c53ac…` — identical to the committed snapshot shas.
- The lane's own read-only probe re-run today classifies the same seven rows `drifted`
  (`MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162`, exit 1; S210/S211
  additionally drifted — round-36 supersede rows whose copies are raw HTML, outside this item).
  `drifted` ≠ changed source per `corpus/knowledge/source-drift-r36.md:15-19`, consistent with this
  re-derivation.
- Multi-epoch consistency: wave 1 observed S176/S177 live shas `e6dddcc2…`/`8a531a2d…` (footer `09:57
  UTC`) at ~11:54–12:02Z; this re-derivation observes `a82233d1…`/`fe0d61d9…` (footer `18:17 UTC`),
  sizes unchanged — exactly the build-cycle hypothesis.
- The frozen grants-C1 receipt (`.ufo/waves/round-36/evidence/c1-after.txt`) does not claim freshness of
  these rows; it reports byte-measurement only (`oracle_drifted=9`). No inference of freshness admission
  from C1 is made anywhere in this item.

## Observations (not defects of the attacked witness)

- `corpus/QUALITY.md:840` and `corpus/knowledge/source-drift-r36.md:19` cite
  `corpus/lessons/round-36.md` (M1), which currently does not exist in `corpus/lessons/` (it is being
  drafted by the wave-2 ScribeLesson seat per `gen-w2-spec.py:508`). Dangling until that seat lands; out
  of this item's scope.
- Criterion 105's phrasing "count the row as a source change only when they differ" is mechanical for the
  five excerpts (header sha == live sha) and requires the diff step for S176/S177, where the shas do
  differ but the diff is footer-only; the criterion's own "Shown able to fail" paragraph supplies that
  nuance. No witness row contradicts the criterion.

## VERDICT

**PASS** — no defect found in the attacked item. Criterion 105's witness re-derives cleanly: all five
excerpt rows (S156–S160) have header sha256 == live full-document sha256 and every committed excerpt line
matches the live file byte-for-byte at its stated line number; S176/S177 differ from the committed
snapshots in exactly the `Last updated on …` build-footer line (4 bytes each, identical sizes). None of
the seven drifted rows is a changed source.
