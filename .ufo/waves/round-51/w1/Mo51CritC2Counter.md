# Mo51CritC2Counter — attack report: count-c2.py (C2 countment arm, data 87e0c374)

Seat: Mo51CritC2Counter (critic, leaf). Lane: mori-shokunin round 51, wave w1.
Scope per assignment: build the cheapest inputs that print `C2=met` without depth or without a real
review, against the FROZEN counter `count-c2.py` (no counter/predicate changes proposed). Data read
read-only from the landed commit `87e0c374537557754bf71dd68036ded3ddc6699c`.

## Method

- The counter's `evaluate(read, rev, ...)` was driven via `importlib` with dict-backed `read`/`ls`
  over the exact committed bytes at `87e0c374` (entry, `corpus/SOURCES.md`, the five `sources-r51`
  copies — byte-identical to the frozen sha256 digests; pins=ok verified in every run).
- Vote files were injected under `.ufo/waves/round-51/w1/`. The lister mirrors the counter's own
  selftest lister (direct children only) and the real `git ls-tree --name-only` behavior.
- Symlink scenarios used a throwaway fixture git repo and the counter's real `git_reader`/
  `git_lister` (`git init` + commit under a throwaway identity in scratch; verified
  `git rev-parse --show-toplevel` = fixture dir before committing).
- Frozen counter sanity: `python3 .ufo/waves/round-51/count-c2.py --selftest` →
  `C2_SELFTEST pass=34 fail=0` (exit 0); `--hashes 87e0c374` row hashes match the driver's
  `claim_hash` for the same cells; `count-c2.py 87e0c374` still reads
  `C2=unmet … entailed=0 dissent=0 failed=entailment` exit=1 (receipt `evidence/c2-at-data.txt`
  reproduced).

## Attack matrix (each line: class → counter verdict)

All 17 dict-backed scenarios scored exactly as expected; the two symlink fixtures were run through the
real git reader.

| class | result | counter line |
|---|---|---|
| A honest ent: one seat file carries 21 `ENTAIL <h> entailed` lines | **MET** `C2=met … entailed=21 dissent=0` | single non-L1 file satisfies the whole entailment arm |
| B ENTAIL line inside a ```` ```` fence (quoted instruction block) | **MET** (same line) | `entail_votes` has no fence awareness; every non-empty line of every `.md` file is regex-tested |
| B2 control: `> ENTAIL …` inside a blockquote | caught (unmet, entailed=0) | line starts with `>`; `^\s*ENTAIL` fails |
| B3 control: `<!-- ENTAIL … -->` line | caught | line starts with `<!--` |
| C ENTAIL line with trailing text, incl. `ENTAIL <h> entailed overclaim` on one line | **MET**, `dissent=0` | `ENTAIL_RE` matches the first verdict word only; trailing text (even the word `overclaim`) is not inspected |
| D uppercase hex (`ENTAIL ABCD… entailed`) | caught | `[0-9a-f]{12}` is lowercase-only |
| E non-lowercase verdict (`Entailed`) | caught | alternation is case-sensitive |
| F1 `MoriR51-votes.md` (exact L1 prefix) | caught (entailed=0) | `name.startswith("MoriR51")` skips |
| F2 `moriR51.md` (lowercase) | **MET** | prefix check is case-sensitive |
| F3 `MORIR51.md` | **MET** | ditto |
| G `Mo51RevA.txt` (non-`.md`) | caught | `name.endswith(".md")` required |
| H second seat file copying the first seat's ENTAIL lines verbatim | **MET** | no content dedupe / authorship check; each file's lines are independent votes |
| I votes in `README.md` (any .md file not starting `MoriR51`) | **MET** | any such file in `w1/` counts as a seat report |
| J quote taken from the kernel-doc comment in `mm_inline.h.v7.2` (`We would like to get this info… until the folio`, with the ` * ` line-split runs) | **MET** | `kind="text"` copies are `normalise_text`-only: comments are not stripped; a located quote may be a comment |
| J2 quote taken from the copyright/license header line of `show_mem.c.v7.2` (`Copyright (C) 2008 Johannes Weiner <hannes@saeurebad.de>`) | **MET** | same |
| K claim row duplicating another row after whitespace/case collapse (two cells differing only by extra spaces / case) | caught (`bad_rows=2`, `source_rows=bad`) | identical-collapsed claims are rejected via the `seen_claims`/`ckey` check |
| M depth-free table: 21 generic filler claims (`observation number NN explains how the kernel estimate formula reads its counters`) over the real quotes, with votes | **MET** `C2=met … entailed=21` | no substantive-content check exists beyond word counts/echo guard |
| L1 symlink fixture: `w1/Mo51Sym.md` is a symlink to a real file **outside** `w1/` holding the votes | caught (entailed=0) | `git show <rev>:<path>` returns the stored link-target string, not the target's content; no following |
| L2 symlink fixture: symlink whose stored target string is literally `ENTAIL 2d0daa4192f1 entailed` | vote counted (`entailed=1`; met only for that row) | the stored link target is read as file content and matches `ENTAIL_RE` |

## Named limits (what the counter cannot see — all confirmed by the runs above)

1. **Any non-`MoriR51`-prefixed `.md` file in `w1/` is a voter** (A, F2/F3, H, I). The L1 can
   plant a file named anything except the exact `MoriR51` prefix; a seat can copy another seat's vote
   lines; a generic file such as `README.md` votes. The counter cannot authenticate a seat or a role.
2. **A single file satisfies the whole entailment arm** (A). Contract round-shape asks for votes by
   at least two seats of different roles; P-C2's documented sentence and the counter require only
   `>= 1` line in non-L1-named files — the two-seat requirement is not enforceable by this counter.
3. **Fenced/indented code blocks are not excluded** (B). A quoted instruction block whose lines
   start with `ENTAIL` votes; only line-initial prose (`>` blockquotes, `<!--` comments) is safe.
4. **Trailing text is ignored, including the word `overclaim`** (C). A line
   `ENTAIL <h> entailed overclaim` is counted as an entailed vote with zero dissent.
5. **Quotes may come from comments or license headers** (J, J2). Text copies are only
   whitespace-normalised; C comments and the copyright line are valid quote locations.
6. **Claims need no substance** (M). The only content guards are word counts and the
   words-beyond-quote minimum; generic filler claims pass.
7. **Symlink votes are possible but only in a contrived form** (L2): a symlink whose stored
   destination string itself starts with `ENTAIL <h> entailed` casts a vote, because `git show`
   returns the raw link-target string. Symlinks to real files do not leak votes (L1).

## What is caught (controls)

- Uppercase hash hex (D), non-lowercase verdict words (E), non-`.md` vote files (G), exact
  `MoriR51` prefix (F1), blockquote/HTML-comment lines (B2/B3), hash of other text (selftest
  `entail_hash_of_other_text_unmet`), whitespace-collapsed duplicate claims (K), symlinks pointing at
  real content (L1), votes outside `w1/` (selftest `entail_other_dir_ignored_unmet`), and the
  overclaim-block (selftest `entail_dissent_unmet`).

## Verification footprint

- `python3 .ufo/waves/round-51/count-c2.py --selftest` → `C2_SELFTEST pass=34 fail=0` exit=0.
- `python3 .ufo/waves/round-51/count-c2.py --hashes 87e0c374` → rows 1/2/21 hashes
  `2d0daa4192f1` / `eba2b78b47f3` / `50f54829ae20` (match driver).
- `python3 .ufo/waves/round-51/count-c2.py 87e0c374` →
  `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok
  provenance=ok entailed=0 dissent=0 rev=87e0c374… failed=entailment` exit=1.
- Driver harness (dict-backed `evaluate`) run in scratch; 17/17 scenarios as predicted. Symlink
  fixtures: `git init` in scratch, commit under throwaway identity, `rev-parse --show-toplevel`
  verified; both `sym_out` (`C2=unmet … entailed=0`) and `sym_trick` (`entailed=1`) read through the
  counter's own git reader/lister.
- `df -h /fast` → 598G free (no ENOSPC); disk-guard script present.

## Findings

- HIGH — `count-c2.py:120-130` (`entail_votes`) + `:117` (`ENTAIL_RE`): any `.md` file in `w1/`
  not starting with the exact byte string `MoriR51` counts as a voter; fence lines, copied lines and
  planted files (README.md, L1-written files with case-variant names) all score `entailed`. C2 can
  print `C2=met` with no genuine non-L1 review.
- HIGH — `count-c2.py:218-222`: a single vote file satisfies the entire entailment arm (contract
  round-shape two-seat/different-roles requirement unenforced; P-C2's sentence only demands one
  line per row in any non-L1-named file).
- MED — `count-c2.py:117`: trailing text after the verdict is ignored; `ENTAIL <h> entailed
  overclaim` counts as entailed with `dissent=0`.
- MED — `count-c2.py:80-85,153` (`normalise` vs `normalise_text`): text-kind copies are only
  whitespace-normalised; comments and license-header lines are valid quote locations (J, J2).
- MED — `count-c2.py:75-77,191-192`: claims need only pass word-count/echo guards; generic filler
  claims are depth-free (M).
- LOW — `count-c2.py:117`: a symlink whose stored target string reads as an ENTAIL line votes (L2);
  symlinks to real content do not.
- LOW — `count-c2.py:117`: case-sensitivity of hex/verdict (D/E) and the exact `MoriR51` prefix
  (F1) are the only authorship-ish filters; all are trivially bypassed by case variants.
- No counter/predicate/control change is proposed (frozen); the above are named limits for the
  report. No lane files were modified; only this report was written in `w1/`.
