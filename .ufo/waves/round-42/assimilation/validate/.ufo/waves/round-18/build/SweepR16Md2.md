# Earlier-round Markdown privacy sweep — round 16

## Scope and method

- Examined the 32 tracked Markdown files in `.ufo/waves/round-16/build/` from `PackProcessSignal.md` through `WindowTool.md` in `git ls-files` order, at the entering revision `d005cdde0e009dea6c0cc29b37163de536528658`.
- Searched the frozen C1 classes R1–R9 from `.ufo/waves/round-18/frozen/c1-policy.json:6-15` and the requested supplementary tokens. The case-sensitive class-only search returned no matches. The supplementary-token hits were read with surrounding context; a broader case-insensitive hit in `SiblingScope.md:14` led to the adjacent disclosure below.
- Read-only evidence commands and outcomes: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files '.ufo/waves/round-16/*.md'` slice count 32 (exit 0); committed line digest command `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d005cdde0e009dea6c0cc29b37163de536528658:.ufo/waves/round-16/build/SiblingScope.md | awk 'NR==20 {printf "%s", $0}' | sha256sum` (exit 0). The digest follows the frozen population tool's UTF-8 line-byte rule (`.ufo/waves/round-18/frozen/c1-population-cmd.py:40-41`). No external URLs were opened.

## Finding

- `.ufo/waves/round-16/build/SiblingScope.md:20` — **manual finding, outside frozen classes R1–R9**; count: 1 line. Kind: local account identifier and privileged-group membership (identity/authorization metadata). SHA-256 of the line bytes: `737771706c75d9dfc9d6db94181652a17ce0a3f3eb8f5bcd99c503d588e321a6`.
  - Minimal redaction: remove the identifying account and group-membership clause; retain only non-identifying probe-scope details.

## Other reviewed hits

No direct frozen-class hit was found. The remaining supplementary-token matches and their surrounding lines were ordinary technical/editorial uses of history or cursor fallback terminology, not other-session output, personal-document or shell-history paths, privileged-configuration contents, routing values, or credentials. This is a bounded finding for the specified 32-file sweep and searched terms, not a claim about unsearched content.