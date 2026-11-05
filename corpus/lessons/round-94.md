# Round 94 — mori lesson (L1 MoriR94, attempt 1)

Entering `84b152308fa6c2f224ad75dff68e525dab9057ac`. Freeze `6b65e7c11f318481d5efa0429cdabb50743a2cc2`
(contract, counters, controls, receipts). Spec `4ae1678df9c190209971ceb4604b71d3e54d779d`. Wave `w1`:
12 seats (executor 3, scout 1, reviewer 2, critic 2, mutation-tester 2, connector 1, scribe 1). Frozen
artifacts: `.ufo/waves/round-94/contract.md`, `count-c1v2.py`, `count-c2v2.py`, `controls-r94.py`.

## Claims and verdicts (frozen predicates; evidence under `.ufo/waves/round-94/`)

- **C1 calibration — met as frozen; admit-candidate (non-author K01, scoped to the instrument).**
  Frozen battery `evidence/controls-r94.txt`: v1 `EMBED_FALSE_PASS v1=3/3`, v2 `v2=0/3`, `live_v2=met`.
  Replay `w1/Mo94E01Replay.md` reproduces the battery (exit 0) and adds four classes (token deleted,
  leading zero, uppercase, doubled hash): v1 false-passes 2/4, v2 0/4. Attack `w1/Mo94R01Atk.md`: eight
  out-of-battery forgeries, 0 v2 false passes; three legitimate forms still read met.
  Named limit: the battery is one file (`counter-win-r77.md`, line 1); mutation `w1/Mo94M01Mut.md` kills the
  R02 class (m1, m1b, m7) but leaves m2, m3, m4 and m6 alive (length clause, census gate, trio floor,
  patched12). The score is not moved.
- **C2 operability — met as frozen; NOT admitted (non-author K01: not an operability move).**
  The predicate `literal_r94=0 … env_i=met env_unset=rc2` holds at the freeze. The critic's reading
  (`w1/Mo94K01Crit.md` §2): no literal was moved (the round-93 counters keep `/home/vgpnk`); the before was
  absence (`files=0`); the met is produced by three new files. The fail-closed arm is weaker than the claim
  says: `env_unset=rc2` also passes when the counter is missing (Python exits 2 on a missing script), and
  the contract says "HOME unset" while the counter sets `HOME=/nonexistent`. R02 attack
  (`w1/Mo94R02Atk.md`): the scan misses host paths in `.json`, `.md`, `.env`, an uppercase `.PY` suffix, and
  split literals; it follows symlinks. Mutation (`w1/Mo94M02Mut.md`): m4 (regex broadened) and m7 (root
  dropped) are killed; m1, m2, m3, m5, m6 survive. Not re-declared after data: the operator rules.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `untracked-orchestrator-marker` — the round-92 and round-93 dispatch markers (`w1.ready`, `w1.ready.dispatched`) stayed untracked in the lane porcelain, so the dispatch record was not durable (`jj-lane.sh state` `untracked=3` at entering; round-93 spot-check D3) | `corpus/lessons/round-93-verifier-spotcheck.md` §1 and §6 D3; `.ufo/waves/round-94/evidence/gitignore-red-before.txt`; `PROTOCOL.md` Invariants (`.ufo/waves/` committed with the round) | round-93 spot-check D3 (non-author); no gate | commit the markers in this round's landing commit (durable, not hidden). Able to fail: `git status --porcelain -- .ufo/waves` lists 3 paths before the landing and none after |
| `fix-hides-evidence` — the wave's proposed `.gitignore` rule `.ufo/waves/*/*.ready.dispatched` passed its own check-ignore (exit 1 before, exit 0 after) while it would hide durable markers: 33 tracked legacy markers match it (`w1/Mo94E03Gitig.md`) | `.ufo/waves/round-94/w1/patches/gitignore-d3.patch` (not applied) | critic K02 (non-author), `w1/Mo94K02Crit.md` §2 | rejected as written; the fix is the commit above. Able to fail: `git ls-files -ci --exclude-standard` lists the 33 tracked legacy markers under the rule |
| `located-quote-tag-artifact` — the frozen contract's P5 quote reads `prefix , otherwise` (a space before the comma). The space came from replacing tags with spaces; on the visible text the sentence has no space, so the tag-stripped count of the contract's form is 0 | `.ufo/waves/round-94/contract.md` P5; `w1/Mo94S01Src.md` §2; corrected count below | none (the frozen quote was not checked against the tag-stripped page) | this lesson's Gate quotes the visible text, and the count is taken on the tag-stripped copy: `Return True if string starts with the prefix, otherwise return False.` = 1 (contract form = 0) |
| `successor-as-before` — the C2 "before" was absence (no round-94 counter at the entering revision), so `literal_r94=0` is true of three new files, not a move on an existing artifact | `w1/Mo94K01Crit.md` §2f; `.ufo/waves/round-94/evidence/entering-c2-r94.txt` | critic K01 after the data (the freeze gate did not require a pre-existing before) | routed to the next round: an operability before must be measured on a pre-existing artifact, or the claim is restated as a capability row. Not fixed |
| `env-fail-open-missing-counter` — `env_unset=rc2` also holds when the counter file is missing (Python exits 2), so the fail-closed arm does not test the counter's own C1_SETUP path | `w1/Mo94K01Crit.md` §2c | critic K01 | routed to round 95: check the C1_SETUP line text, not only the exit code. Not fixed |
| `control-battery-gap` — mutation survivors m2, m3, m4, m6 in C1 and m1, m2, m3, m5, m6 in C2: the frozen battery has no fixture that flips those conjuncts (C1 has single-variable fixtures in `w1/Mo94M01Mut.md`, unrun as frozen controls) | `w1/Mo94M01Mut.md` gap summary; `w1/Mo94M02Mut.md` | mutation-tester seats (this round's wave) | routed to round 95: a frozen-battery amendment, with the single-variable fixtures, before any new scoring. Not fixed |

## Routed defects (not fixed this round)

- **D1 planner (round-93 spot-check).** The shape line in the contract discloses that the L1 holds the planner
  seat and the validator refuses `planner`. Critic K02 §3: the disclosure does not close it. Open, operator-owned
  (the policy's topology slot is not bound to the L1 in any artifact).
- **R02.** Closed for the C1 predicate by the v2 token rule (`count-c1v2.py` `admission_token_ok`); the frozen
  round-93 counter keeps its substring test as history (`count-c1.py:141`).
- **Counter host path.** The round-93 counters keep `/home/vgpnk` (`count-c1.py:39`, `count-c2.py:39`,
  `controls-r93.sh:81`); the round-94 counters carry none (C2 scan). The round-93 literals are frozen history.
- **Sibling host-literal class.** Connector `w1/Mo94Conn01.md`: no sibling carries the R02 admission defect; seven
  siblings carry the host literal `/home/vgpnk` in live tooling (chousa, kaidoku, kama and four more). Routed to the
  operator through `.ufo/l0-questions.md`; no sibling was edited.
- **Digest debt P4** (31 prefix-only rows, S125 unpinned) and the **round-90 nonce guard** (QUALITY 191) are carried.

## Gate (sources, protocol §2b)

| Row | URL | Access and recomputation | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S624 | https://docs.python.org/3/builtins/stdtypes.html#str.startswith (the `library/` path redirects here; `-L`) | 2026-11-05; 815447 bytes; sha256 `2397d83204d8901b852e5dcb72cb1b5cbf311e9db1f15116089b85ab21d22b68`; re-fetched and re-hashed by scout `w1/Mo94S01Src.md` (same bytes) | "Return True if string starts with the prefix, otherwise return False." (anchor `id="str.startswith"`; tag-stripped count 1) | **admit** (mined; used-by this lesson). Teaches: `str.startswith(p)` is True when the string begins with `p`; the round-94 counter applies it to the first token of `verified-at:` (at least 7 characters) against the admission `%h`, so a hash inside a longer token is rejected. It does not show that the admission commit introduced the current content. |
| S625 | https://docs.python.org/3/library/re.html | 2026-11-05; 257722 bytes; sha256 `0c8785564b3058239f29ba01fae820c4c7591525e39ef8221a23d72e0dc7e31f`; opened by the L1 this round | "Matches if the current position in the string is not preceded by a match for ... ." (the `(?<!...)` negative lookbehind) | **reject** (kept as a row). `REJECTED: the admission test is a prefix test, so no regex lookaround is needed; flip: a counter that matches the admission token with a regular expression.` Not spot-checked by a non-author yet (named). |

The S622 row (git-log, `%h` abbreviation) was not re-opened this round: it is cited as a prior admit and not as a
new claim source. The S624 quote in the contract (`prefix , otherwise`) is corrected here (see Mistakes).

## Assimilation and considerthese

- **Assimilation: none.** The lane checkout carries no `merge/mori/` package; shokuknow was not opened.
- **considerthese.** The newest file, `considerthese/2026-10-26.md`, has one still-unimplemented item in practice:
  suggestion 3 (the round after a closure re-executes that closure's counter at the scored revision). Round 93's
  reading ("no proposal is still unimplemented") was wrong for items 1–3; this is the correction of record (round
  93's file is not edited). Evidence for suggestion 3: `.ufo/waves/round-94/evidence/rerun-r93-counters-at-8edbb86d.txt`
  (`count-c1.py` → `C1=met … adm_ok=19`, rc 0; `count-c2.py` → `C2=met … home_literals=0`, rc 0). QUALITY 136
  already binds this rule; the re-run is the round-94 application.

## Trend verdicts (lane)

- **Expansion: unchanged.** No knowledge entry admitted; two registry rows (S624 mined, S625 rejected).
- **Quality: unchanged.** No admitted entry was superseded or found false; the 19 round-92 `verified-at` lines were
  re-checked by the frozen counter (`adm_ok=19`).
- **Discernment: improved.** Two disagreements became grounded criteria: the R02 substring defect (QUALITY 202) and
  the dispatch-marker durability defect (QUALITY 204, from the round-93 spot-check D3). The round-93 calibration
  reading was rebutted with data (critic K01 §1e). The reject S625 is not yet non-author spot-checked (named).

## Frontier and sourced claim

- Sourced claim (frontier step): C1 rests on S624 (opened this round, re-verified by a scout).
- Mistake mined: yes (six rows above; each names captured-by and a fix or a routed fix).
