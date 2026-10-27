# Mo56CritBinderSemantics — attack on the exact-scalar rule of the C2 vote binder

Seat: Mo56CritBinderSemantics (critic, mori round 56 w1). Date: 2026-10-27.
Scope: falsify the dual-shape seat-output vote binder `tools/mori-vote-bind.py`
by attacking its exact-scalar rule (VOTE_RE, line 64) with 10 crafted outputs
plus contrast probes. Lane: mori-shokunin (detection and report only).

## Frozen bytes under attack (verified before the attack)

- Freeze tip `8be2717b0809281d07dffe83dad424a4859e0747`; working HEAD during this
  seat `acc62f54fb0f53b47b428594dc27365150cbd76b` (post-freeze validate commit).
- `git diff 8be2717b..HEAD -- tools/mori-vote-bind.py` printed nothing (rc 0);
  `sha256sum tools/mori-vote-bind.py` =
  `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca`,
  equal to the PIN frozen in `count-c2.py` (pinned at data commit c419fe6d).
- Selftest of the frozen tool: `VOTE_BIND_SELFTEST pass=16 fail=0`, exit 0.
- Frozen counter on the attacked bytes:
  `python3 .ufo/waves/round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747`
  → `C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747`, exit 0;
  same command at HEAD `acc62f54…` → `C2=met …`, exit 0.
- Grammar grounding: the round-55 voter instruction (`.ufo/waves/round-55/w1-input.json`)
  taught voters "Per row: `RECHECK <hash> holds` or `RECHECK <hash> stale — reason + path:line`";
  the ledger disposition column (cell 6, read by `read_ledger`) carries the closed
  word set {`holds`, `stale`} (69/9 of 78 rows in
  `corpus/knowledge/kernel-v7.3-recheck-r55.md`; tally compares `w == want`
  case-sensitively at line 183).

## Method

Read-only `importlib` exec of the frozen module from its absolute path (no copy,
no edit), driving `final_votes()` on each crafted output; every crafted output was
also written to a file under the seat scratch and run through the real CLI
(`python3 tools/mori-vote-bind.py extract <file>`); the in-process verdict and the
CLI verdict agreed on all 18 extract probes. Tally behaviour was probed with a
one-row mini ledger (disposition `holds`) plus a synthetic results.json, through
the real CLI `tally`. Mini-ledger rows follow the committed ledger's cell layout
so `read_ledger` parses them. Python 3.14.8. All scratch under
`/fast/scratch/hyaku/mori-r56/Mo56CritBinderSemantics/` (removed after this
report; key evidence is inlined here).

## Results: the 10 mandated attacks

Each input is shown as a Python string literal (the exact bytes fed to the
extractor). "Binds" means `final_votes()` returned a vote for the hash
`a6e5226259c9` (extract does not consult the ledger, so the selftest hash is
sufficient for bind/no-bind).

1. **Vote with trailing period** — input `'RECHECK a6e5226259c9 holds.'`
   → **does not bind** (channel text). After the word `holds`, the regex needs
   end-of-string or `\s+rest` (`VOTE_RE` line 64); the fused `.` is neither.
   Defensible under the frozen grammar: yes — `holds.` is not the disposition
   word, and the round-55 instruction gave the exact line shape. But it is a
   false negative a reasonable seat could produce (terminal sentence
   punctuation), and the failure is silent.

2. **Vote with markdown bullet** — input `'- RECHECK a6e5226259c9 holds'`
   → **does not bind** (channel text). `line.strip()` removes whitespace only;
   the line then starts with `-`, and `^(RECHECK|ENTAIL)` fails. Same for
   numbered-list and emphasis decoration (verified: `'1. RECHECK a6e5226259c9 holds'`
   and the backtick-quoted `` `RECHECK a6e5226259c9 holds` `` both do not bind).
   Defensible: yes — it matches the protocol's own rule that a vote line starts
   with the verb; but markdown-bulleted vote lists are a plausible seat habit,
   silently zeroed.

3. **Vote inside a JSON array element with a trailing comma in the raw text
   (not parsed as JSON)** — compact input
   `'{"vote_lines": ["RECHECK a6e5226259c9 holds",], "note": "x"}'` and the
   pretty-printed form `'{\n  "vote_lines": [\n    "RECHECK a6e5226259c9 holds",\n  ],\n  "note": "x"}'`
   → **do not bind** (channel text after `json.loads` fails at line 85). In the
   fallback, the vote sits inside quotes on a line starting with `{`, `[`, or `"`
   after strip, so `^` fails. Defensible: the tool never claims
   malformed-JSON recovery, and the fallback is best-effort text. But note the
   recovery asymmetry shown by the contrast probe 3c below, and that
   trailing-comma JSON is the single most common generated-JSON defect: a seat
   emitting it loses its whole vote set silently.

4. **Vote as the ONLY content of a JSON array** — input
   `'["RECHECK a6e5226259c9 holds"]'`
   → **binds** (channel json, word `holds`). `_walk_strings` (line 68) walks
   list elements; the single element is a JSON string scalar that matches
   `VOTE_RE` after strip. CLI: `VOTE RECHECK a6e5226259c9 holds json`, rc 0.
   Defensible: yes — this is exactly the JSON string-scalar shape the claim
   covers.

5. **Vote split across two JSON strings** — array input
   `'["RECHECK a6e5226259c9", "holds"]'` and object input
   `'{"vh": "RECHECK a6e5226259c9", "vw": "holds"}'`
   → **do not bind** (channel json). Neither scalar matches alone: the first
   lacks a word after the hash, the second lacks verb+hash. Defensible: yes,
   and this is the strongest correct rejection — joining strings across
   document positions would be unsound.

6. **Vote word `HOLDS` uppercase** — input `'RECHECK a6e5226259c9 HOLDS'`
   → **binds** (channel text, word `HOLDS`). The word class
   `[A-Za-z][A-Za-z0-9_-]*` is case-inclusive and the tally's compare
   `w == want` (line 183) is exact. CLI: `VOTE RECHECK a6e5226259c9 HOLDS text`, rc 0.
   Tally probes over a one-row mini ledger (disposition `holds`, hash
   `7b2d297eec60`):
   - single `HOLDS` → `TALLY rows=1 agree=0 double=0 single=1 zero=0 dissent=0 voters=1 bound_voters=1`
   - single `holds` → `TALLY rows=1 agree=1 double=0 single=1 zero=0 dissent=0 voters=1 bound_voters=1`
   - pair `HOLDS` + `holds` → `TALLY rows=1 agree=0 double=1 single=0 zero=0 dissent=1 voters=2 bound_voters=2`
   - pair both `HOLDS` → `TALLY rows=1 agree=0 double=1 single=0 zero=0 dissent=0 voters=2 bound_voters=2`
   Defensible at the regex level: yes (the grammar binds any cased word; the
   disposition words are a closed set and `HOLDS` is not in it). But the
   dissent conflation is a named limit: one case typo in a unanimous pair
   surfaces as `dissent=1` — a kill-class signal under this lane's own rules —
   with no way to tell a typo from a genuine disagreement.

7. **`'RECHECK a6e5226259c9 holds!'` with bang** — input as quoted
   → **does not bind** (channel text). After `holds` the `!` is neither
   whitespace nor end. Defensible under the exact grammar: yes. False-negative
   prone: emphatic terminal punctuation is a plausible seat habit; silent zero.

8. **A JSON number 42 doc** — input `'42'`
   → **does not bind** (channel json, zero string scalars). Trivially
   defensible: a number doc carries no votes. Cosmetic: the channel label is
   `json` even though nothing was walked.

9. **Empty object `{}** — input `'{}'`
   → **does not bind** (channel json). Trivially defensible.

10. **A JSON array of numbers with the vote as digits** — input
    `'[82, 69, 67, 72, 69, 67, 75, 32, 97, 54, 101, 53, 50, 50, 54, 50, 53, 57, 99, 57, 32, 104, 111, 108, 100, 115]'`
    (ASCII codes of the canonical line)
    → **does not bind** (channel json). Defensible: yes, and this is the other
    strongest correct rejection — numbers are not string scalars, and decoding
    numeric char codes is outside any claimed surface.

Summary of the ten: eight do not bind (1, 2, 3, 5, 7, 8, 9, 10) and two bind
(4, 6). Every verdict is
defensible under the frozen grammar; four of them (1, 2, 3, 7) are silent
false negatives a reasonable seat could produce, and one (6) binds with a
misleading tally consequence.

## Contrast probes (same defect class, whitespace flip)

- Input `'RECHECK a6e5226259c9 holds .'` (period separated by a space)
  → **binds**, word `holds`, rest `.`. So `holds.` is zeroed while `holds .`
  is counted: one inserted space flips bind↔no-bind for terminal punctuation.
- Input `'RECHECK a6e5226259c9 holds !'` → **binds**, rest `!`. Same flip for
  the bang case.
- Input `'{"vote_lines": [\nRECHECK a6e5226259c9 holds\n], "broken": tru'`
  (malformed JSON, bare vote token on its own line — the shape the frozen
  selftest `t_malformed_json_falls_back_to_text` accepts) → **binds** (channel
  text). So the malformed-JSON fallback binds a bare token but not a quoted
  string element (case 3): two malformed documents in the same defect class
  are treated oppositely. Both outcomes are individually defensible; the
  asymmetry is the named limit.
- Input `json.dumps('RECHECK a6e5226259c9 holds.')` (case 1 as a JSON string
  scalar) → **does not bind**: the exact-scalar rule applies identically in
  both channels.
- CRLF: input `'RECHECK a6e5226259c9 holds\r'` → **binds** (strip removes the
  CR). NBSP-separated and tab-separated fields also bind (`\s` and `strip()`
  are Unicode-aware).

## Additional false-negative probes (beyond the 10)

- JSON string scalar with the vote after an internal newline
  (`json.dumps('status: ok\nRECHECK a6e5226259c9 holds')`) → **does not bind**:
  `^` anchors at the scalar start (line 91 applies `VOTE_RE` to the whole
  scalar; no MULTILINE). A seat that packs a summary and a vote into one
  JSON string loses the vote.
- Text with an unbalanced fence before the vote
  (`'intro\n```python\nexample\nRECHECK a6e5226259c9 holds'`) → **does not
  bind**: the fence toggle (lines 98-101) silences the rest of the output
  after one fence-looking line. Balanced fences behave (vote after the close
  binds; the fenced copy does not).
- Vote placed as a JSON object key (`json.dumps({'RECHECK a6e5226259c9 holds':
  'value'})`) → **does not bind**: `_walk_strings` walks values only (line 71
  iterates `node[k]`), not keys. LOW; keys are not string scalars in the
  claimed sense, but a seat emitting a vote-keyed map is plausible.
- Unicode word: `'RECHECK a6e5226259c9 h\u00f6lds'` → **does not bind**:
  the word class `[A-Za-z]` is ASCII-only. UNVERIFIED only in that no real
  disposition word contains non-ASCII (the closed set is ASCII by
  construction), so this is theoretical.

## False negatives a reasonable seat could produce (inventory for the L1)

1. Terminal sentence punctuation fused to the word — `… holds.`, `… stale,`,
   `… holds!` — silently zeroed (cases 1, 7; flips with one space).
2. Markdown decoration — bullets, numbering, emphasis, backticks — silently
   zeroed (case 2 and probes).
3. Case drift of the disposition word — binds but counts against agreement;
   in a pair it reads as `dissent=1`, kill-class (case 6 + tally probes).
4. Malformed JSON wrapping (trailing commas, the common generated-JSON
   defect) with quoted votes — the whole vote set is silently zeroed, while a
   bare-token malformed doc binds (case 3 vs probe 3c).
5. Multi-line JSON string scalar with the vote after an internal newline —
   silently zeroed (probe above).
6. Unbalanced fence earlier in the report — the remainder is silently zeroed
   (probe above).
7. Vote emitted as a JSON object key — silently zeroed (probe above).
8. Non-ASCII letters in the word — rejected by the ASCII word class
   (theoretical; the disposition set is ASCII).

The extract CLI gives no signal for any of these: on a no-bind it prints
nothing and exits 0 (observed on cases 1, 2, 3b, 7 above), so a seat cannot
distinguish "my vote was counted" from "my vote silently vanished" without
re-running the regex mentally. The tally surface makes silent loss worse: a
zeroed vote is reported as `zero`/`single`, the same surface as abstention
(probe: single trailing-period vote → `TALLY rows=1 agree=0 … zero=1 …
bound_voters=0`).

## Impacted axes

- C2 operability (the claim under attack): the frozen predicate still passes
  (verified above); all ten attack verdicts are defensible under the frozen
  grammar, so no kill. The findings are named limits on the binder's
  operational semantics, not counter defects; the counters, predicates,
  controls and kill rules are untouched.
- C1 coverage: unaffected (separable; no shared file was read for anything
  but the ledger word set).
- Calibration (via the dissent conflation, case 6): a typo surfaces as
  dissent, which this lane's rules treat as a kill-class signal — a future
  round that binds a real wave could mis-grade a unanimous row.

## Smallest safe correction (named limits + routed items; nothing applied)

Per the freeze rules I changed nothing. The smallest safe corrections, in
increasing cost order, for the L1 to weigh for round 57 (routed items, not
counter changes):

1. Zero-cost documentation (voter-facing instruction, any wave spec that
   teaches the vote line): state the three hard edges — (a) nothing may be
   fused to the disposition word (punctuation must be absent or space-
   separated rest); (b) the word is case-sensitive and must be copied exactly
   from the ledger; (c) JSON output must be strictly valid (no trailing
   commas), and a multi-line summary string must not carry the vote after an
   internal newline.
2. Zero-cost tooling note: the extract CLI's silent no-bind (exit 0, no
   output) makes every false negative invisible; a stderr "no votes bound"
   note or a `--strict` mode would convert silent loss into observable loss.
   Routed as an optional tool-data change with re-pin consequences for the
   L1 to weigh.
3. Optional data-level hardening for the L1 to weigh (would change the pinned
   tool sha, so flagged, not proposed as a fix here): strip one layer of
   surrounding markdown decoration/quotes before matching, or normalize the
   disposition-word compare with `casefold()`. Each widens the bound surface;
   each also weakens the exact-scalar property that makes the current grammar
   defensible, so I do not recommend either without a protocol-level
   decision.

## Hygiene

- Read-only over the lane repo: only reads and two frozen-counter executions
  (both materialize under `TMPDIR=/fast/scratch/hyaku/mori-r56/Mo56CritBinderSemantics/tmp`).
  No git/jj mutation anywhere; no host writes; no tools installed; no pacman
  (host-wide pause respected). No clone was needed (import-by-path + CLI on
  scratch files). No network use.
- Scratch `/fast/scratch/hyaku/mori-r56/Mo56CritBinderSemantics/` removed after
  this report was written (trap-equivalent: verified absent post-write).
- This report starts no line with the words RECHECK, ENTAIL, QUOTE or REPLACE
  (verified with grep before landing; all vote text is quoted inside sentences
  or table cells).
- No credential material, sessions, or private URLs; no machine identifiers.

## UNVERIFIED

- Whether any round-55 voter output actually contained any of the false-
  negative shapes above (the re-bound tally reports `bound_voters=15/16`, and
  the missing voter is recorded as carrying no votes in either surface; I did
  not diff the 16 outputs against the 8 inventory shapes — that census is a
  different seat's item).
- Behaviour under non-UTF-8 output bytes with surrogate escapes (the reader
  uses `errors="surrogateescape"`; the regex is applied after decode, and I
  did not craft invalid-UTF-8 fixtures).
- Interaction with `min_votes` / disposition-cols flags beyond the default
  path exercised by the frozen counter.

## Findings

- **F1 (MED)** — `tools/mori-vote-bind.py:64` (`VOTE_RE`): punctuation fused
  to the disposition word silently drops the vote; one inserted space flips
  the verdict (cases 1, 7 vs probes 1b, 7b). No diagnostic from the extract
  CLI (silent no-bind, exit 0). Named limit; correction items 1 and 2 above.
- **F2 (MED)** — `tools/mori-vote-bind.py:103` (text channel `line.strip()` +
  anchored `^`): markdown decoration (bullets, numbering, emphasis,
  backticks) silently drops the vote (case 2 + probes). Named limit;
  correction items 1 and 2.
- **F3 (MED)** — `tools/mori-vote-bind.py:85-106` (JSON-fallback asymmetry):
  malformed JSON with a trailing comma zeroes the whole quoted vote set,
  while the same defect class with a bare token binds (case 3 vs probe 3c).
  Given how common trailing-comma JSON is in generated output, this is the
  highest-volume silent-loss path. Named limit; correction items 1 and 2.
- **F4 (MED)** — `tools/mori-vote-bind.py:64` + `:183` (bind is
  case-inclusive, agreement compare is exact): a case-typoed disposition word
  binds but counts against agreement, and in a pair surfaces as `dissent=1` —
  kill-class under lane rules (case 6 + tally probes). Calibration risk;
  correction item 1 (and optionally 3, with re-pin cost).
- **F5 (LOW)** — `tools/mori-vote-bind.py:91` (`^` anchors at scalar start,
  no MULTILINE): a vote after an internal newline inside a JSON string scalar
  does not bind. Named limit; correction item 1.
- **F6 (LOW)** — `tools/mori-vote-bind.py:98-101` (fence toggle): an
  unbalanced fence earlier in the output silences all later votes. Named
  limit; correction item 1.
- **F7 (LOW)** — `tools/mori-vote-bind.py:68-76` (`_walk_strings` walks
  values only) and `:64` (ASCII word class): votes emitted as JSON object
  keys, or with non-ASCII word letters, do not bind. Named limit.
- **F8 (LOW)** — `tools/mori-vote-bind.py:417` (`--voter` is
  `action="append"`): `--voter A B` argparse-errors (rc 2); names must be
  repeated one per flag. The frozen counter passes flags correctly (verified
  at `count-c2.py:105-107`), so this is human-CLI usability only.
