# Mo57Reviewer18 — round 57 w1, C2 counter attack (seat report)

Scope: attack the frozen C2 counter `python3 .ufo/waves/round-57/count-c2.py R` against the
C2 predicate in `.ufo/waves/round-57/contract.md` (entry exists, opens with `source:` /
`verified-at:` / `recheck:`, cites a newly opened source row, eight claim rows each with a
located quote in the source copy, states `unclosed` is a pairing count rather than a
present-running count). Detection only: no lane/fleet edits, no commits outside scratch.

## Counter identity

- Working tree `.ufo/waves/round-57/count-c2.py` sha256
  `0fe9e6f4cdde0ac14bd8cad907e948edcb8a51f7c950622cf84cae5f1f75f742` — byte-identical to the
  blob in freeze commit `618562c72a03dc4d17386b715357f863fd327274`
  (`git show 618562c…:.ufo/waves/round-57/count-c2.py | sha256sum` → same digest). The file is
  absent from entering branch rev `53e2b47…` (wave dir landed with the freeze commit).
- Baseline at entering rev (matches `.ufo/waves/round-57/controls.txt`):
  `count-c2.py 53e2b47…` → `C2=unmet claims=0 source=bad rev=53e2b47…`, exit 1.
- No ref named `R` exists in the lane repo at HEAD (`git rev-parse R` → unknown revision);
  runs with literal `R` against the real repo correctly report unmet. Scoring must pass a
  concrete tree-ish.

## Method

Unmodified counter executed via a PATH shim (`git` wrapper in scratch) that rewrites ONLY the
hardcoded `-C /home/vgpnk/Projects/shokunin/mori-shokunin` argument to the fixture repo
(`/fast/scratch/hyaku/mori-r57/Mo57Reviewer18/fx`, its own git repo, tags `R`, `R9`, `R9v`,
`RK`). Shim neutrality proven: same counter, real repo, real rev, through the shim → output
byte-identical to controls (`C2=unmet claims=0 source=bad`, exit 1). Counter script itself
zero-diff.

## Findings

**F1 (high) — counter reports `met` on content violating nearly every contract clause.**
Fixture tag `R`: `count-c2.py R` → `C2=met claims=8 source=ok quotes=ok rev=R`, exit 0. The
fixture entry has: (a) NO `source:`/`verified-at:`/`recheck:` header; (b) eight `| K` rows
whose "quotes" are a single unbalanced backtick plus gibberish present in no source copy (no
source copy exists in the fixture at all); (c) a sentence asserting the OPPOSITE of the
contract claim ("…is a pairing count is REJECTED… `unclosed` is a present-running count");
(d) S548 cited only as a stub registry row (`| S548 | Stub row: never opened, no URL, no
sha256, no quotes, no mined status … | queued |`). "mined" was satisfied by an unrelated
pre-existing `S001` row.

**F2 (high) — `source_ok` does not test a newly opened, actually mined S548.**
`count-c2.py:13`: `source_ok="S548" in entry and "| S548 |" in registry and "mined" in registry`.
- `"mined" in registry` is a global substring over SOURCES.md; at the entering tip the real
  registry already contains "mined" on essentially every source row (grep rc=0; 48 `^| S5`
  rows alone). This clause is pre-satisfied before round 57 opens anything.
- `"| S548 |" in registry` tests row existence only: no URL, no sha256-pinned copy, no
  `mined` status on the S548 row itself, and no parent-diff check that S548 is newly added —
  an S548 inherited from an earlier round would pass.
- `"S548" in entry` matches any prose mention (fixture satisfied it in a footer line), not a
  header citation and not a claim-row citation.

**F3 (high) — "located quote in the source copy" is unverifiable by this counter.**
`count-c2.py:14`: `quote_ok=all("\`" in x and "\`" in x for x in claims)` — both operands are
identical, so ONE dangling backtick per row passes (fixture R: `quotes=ok`). The counter never
reads `corpus/evidence/sources-*` or any copy, so a quote cannot be checked as a substring of
the cited source. Zero-backtick rows do fail (tag `R9`, holding the zero-backtick content:
`C2=unmet claims=8 source=ok quotes=bad`), so the check is not fully vacuous — it just tests
backtick presence, not location or provenance.

**F4 (medium) — `| K` row prefix counts unrelated tables; exact-8 is brittle both ways.**
`count-c2.py:12` matches any line starting `| K`, including `| Known …` rows of an unrelated
limitations table: fixture tag `RK` (no claim table, "NOT a pairing count" sentence, eight
`| Known limitation n |` filler rows) → `C2=met claims=8 source=ok quotes=ok`, exit 0.
Conversely `count-c2.py:15` requires exactly 8: a genuine entry with 9 claim rows reports
`C2=unmet claims=9` exit 1 (tag `R9v`), 7 rows likewise unmet.

**F5 (medium) — the pairing-count semantics claim is tested as a bare substring.**
`count-c2.py:15`: `"pairing count" in entry` — satisfied by negation or any mention (fixtures
R and RK both assert `unclosed` is NOT a pairing count and pass). "rather than a
present-running count" is never tested.

**F6 (low) — required header never checked.** The contract requires the entry to open with
`source:`, `verified-at:`, `recheck:`; no line of count-c2.py inspects them (fixture R omits
all three and reports `met`).

## Honest limits of the attack

- The counter does enforce something: exactly 8 `| K`-prefixed rows, ≥1 backtick per such row,
  an `| S548 |` registry row, the substrings `S548`/`mined`/`pairing count`. Every
  content-level predicate (located quotes, newly opened mined source, header, pairing-vs-
  running semantics) is however bypassable, as demonstrated.
- This shows the counter cannot distinguish an honest entry (in the
  `corpus/knowledge/driver-liveness-r56.md` style) from a content-free fabrication; it does
  not show the wave-1 executor produced such a fabrication. C2's asserted "depth" evidence
  value is bounded by F1–F6 regardless.

## Verdict

C2 counter under-checks the frozen predicate in six named ways (F1–F6); a scratch-only
fixture makes it report `C2=met claims=8 source=ok quotes=ok` with exit 0 on an entry missing
the required header, containing no located quotes, citing a never-opened stub source whose
`mined` clause is satisfied by unrelated rows, and asserting the negation of the pairing-count
claim. If scoring treats `C2=met` as depth evidence for round 57, that evidence is not
trustworthy without a strengthened counter (sha-pinned source copy + quote-as-substring check,
parent-diff "newly opened" test, `mined` status on the S548 row itself, header-line check).
Frozen counters are immutable; this report records the gap, it does not change predicates.

## Reproduction

Scratch fixture (removed after this wave per seat hygiene): `/fast/scratch/hyaku/mori-r57/Mo57Reviewer18/fx`
(tags `R`, `R9`, `R9v`, `RK`), shim `…/bin/git`, driver:
`PATH=…/bin:$PATH python3 .ufo/waves/round-57/count-c2.py <tag>`. All runs above are
copy-pasted outputs; the real-repo runs were executed against absolute path
`/home/vgpnk/Projects/shokunin/mori-shokunin` with `git -C` semantics unchanged.
