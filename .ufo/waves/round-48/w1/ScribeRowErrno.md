# ScribeRowErrno — round 48 w1: SOURCES.md row S481 (errno.h EDQUOT)

Seat: ScribeRowErrno (leaf, no subagents). Lane: mori-shokunin. Intent: draft the lane
SOURCES.md row for the generic Linux errno.h EDQUOT definition as id **S481** and report
the row plus a Gate block with a located quote.

## Draft row (S481) — fenced draft, not applied to corpus/SOURCES.md

```
| S481 | Linux include/uapi/asm-generic/errno.h at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h | code | A | EDQUOT value on Linux (generic ABI) | include/uapi/asm-generic/errno.h:107; tag v7.2; copy corpus/evidence/sources-r48/errno.h sha256 66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be | The generic ABI defines EDQUOT = 122, "Quota exceeded"; architectures with their own errno.h may override the number, so a probe must match the platform's own EDQUOT. | mined | 2026-10-25 | on-release | corpus/knowledge/quota-observability-r48.md |
```

Column-by-column (11 columns, no `|` inside any cell):
- id: S481 (free in lane `corpus/SOURCES.md`: registry ends at S478; grep for `S479`-`S482` rows finds none).
- source: `Linux include/uapi/asm-generic/errno.h at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h` — the URL is byte-identical to the frozen `COPIES` key in `.ufo/waves/round-48/count-c2.py:41`.
- kind: `code`; tier: `A`; scope: `EDQUOT value on Linux (generic ABI)` (as assigned).
- anchor: `include/uapi/asm-generic/errno.h:107; tag v7.2; copy corpus/evidence/sources-r48/errno.h sha256 66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be`.
- status `mined`, opened `2026-10-25`, recheck `on-release` (pinned kernel tag), used-by `corpus/knowledge/quota-observability-r48.md`.

## Gate

Located quote (≤25 words, verbatim from the committed copy, line 107):

```
#define	EDQUOT		122	/* Quota exceeded */
```

Normalized (whitespace collapsed): `#define EDQUOT 122 /* Quota exceeded */` — 7 tokens, located
at `corpus/evidence/sources-r48/errno.h:107`, tag v7.2.

## Evidence (commands, output, exit code)

1. Committed copy line and digest:
   - `grep -n EDQUOT /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r48/errno.h` → `107:#define	EDQUOT		122	/* Quota exceeded */`, exit 0; exactly 1 occurrence (`grep -c EDQUOT` → 1).
   - `sha256sum` committed copy → `66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be`, matching the freeze receipt `evidence/freeze-sha256.txt` line for errno.h (read via `.ufo/waves/round-48/evidence/freeze-sha256.txt`).
   - `wc -l` → 127 lines.
2. Live fetch at tag v7.2 (read-only):
   - `curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h` → saved to scratch `errno-live-generic.h`; `sha256sum` identical to the committed copy; `cmp ... <committed>` → no differences (exit 0); `grep -n EDQUOT` → line 107, same content. Live and committed bytes are identical today.
3. Arch-specific headers (fetched live at tag v7.2 — the check the seat asked for):
   - `arch/mips/include/uapi/asm/errno.h` → `131:#define EDQUOT		1133	/* Quota exceeded */`
   - `arch/sparc/include/uapi/asm/errno.h` → `43:#define	EDQUOT		69	/* Quota exceeded */`
   - `arch/alpha/include/uapi/asm/errno.h` → `46:#define	EDQUOT		69	/* Quota exceeded */`
   - Conclusion: architectures with their own errno.h do differ from the generic value (mips 1133, sparc/alpha 69 vs generic 122). The row scope stays `EDQUOT value on Linux (generic ABI)`; the generic header is the x86-64 value. Arch-specific values are VERIFIED by the fetches above (not left UNVERIFIED), and the divergence is reflected in the row's `teaches` cell without importing arch numbers into the row.

## Constraints observed

- Only my report and scratch (`.scratch/r48-ScribeRowErrno/`) were written; no production file, no SKILL.md/SOURCES.md/corpus/tools/LOG.md/SCORECARD.md, no frozen round-48 file was touched.
- Read-only git/jj: no mutating commands used.
- No tools installed or upgraded (none needed; nothing to record under the 2026-10-19 tooling directive).
- No credential material or private URLs. Scratch files: `errno-live-generic.h`, `errno-live-mips.h`, `errno-live-sparc.h`, `errno-live-alpha.h` (fetched this session, not committed).
