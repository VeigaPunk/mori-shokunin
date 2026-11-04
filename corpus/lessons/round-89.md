# Round 89 — mori (L1 MoriR89), attempt 1 — lesson

Entering revision `30a29797012281b9fd0c748b38b929ac67f8c754` (r88 closed `rejected-harmed`,
`corpus/lessons/round-88-verifier-spotcheck.md`). Frozen contract
`.ufo/waves/round-89/contract.md` at `d4438695998894aad7ff9b20f46d9f1852ea3c7d`, controls
`.ufo/waves/round-89/evidence/controls-r89.txt` committed before any after-value.

## What the round did

- **C1 (operability)** — the r87 receipt gate refuses comment-only and self-printing bindings
  and accepts `./path`. Three gate versions: first landing `760428ab` met P-C1 but `Mo89R01C1`
  measured 13 valid equivalents newly refused; repair 1 `9f4d20b9` fitted that battery
  (`noharm harm=0`) and the residual seats `Mo89R03Repair`/`Mo89C02Critic` measured it harmed
  on 78 new cases (`heldout harm=12 newopen=1`); repair 2 `7715bb56` (entering rule minus
  provably non-executing positions) reads `harm=0 newopen=0` on both batteries and P-C1 met.
  Repair 2 has no non-author attack of its own.
- **C2 (calibration)** — the twelve r88 survivors armed (seats `Mo89E01ArmsC1`,
  `Mo89E02ArmsC2`), landed `7ce712d4`; P-C2 `C2=met mutants=12 killed=12 survivors=0
  unattributed=0 unanchored=0 arms=28,26` at `9f4d20b9` and `7715bb56`. Assurance partial:
  a canary that prints every declared arm's FAIL label also reaches the target
  (`Mo89C02Critic` forge-c1/c2b), and 3 of 6 neighbouring mutants survive (`Mo89M02Mut` B1/B4/B6).
- Receipts `.ufo/waves/round-89/evidence/after-r89.txt` (repair 1) and
  `evidence/after-r89-final.txt` (repair 2: four counters, each rc 0).
- Frontier: S607, S609, S610, S611 admitted, S608 rejected; knowledge
  `corpus/knowledge/execution-binding-r89.md`; QUALITY 186–188.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix, and what makes it able to fail |
|---|---|---|---|
| `met-predicate-hid-operability-harm` — the first C1 landing printed the frozen met line while refusing 13 valid equivalent commands the entering gate bound (`python3 -I -B`, `python3.14`, env prefixes, `--`, `-W ignore`, `nice`, quoted `;`, `&&`, `exec`, `uv run`, `bash -c`) and still binding 6 counterfeits (`-W`/`-X` value lookalikes, `-c`/`-m` values). The contract froze three fixtures and no equivalence battery. | `.ufo/waves/round-89/w1/Mo89R01C1.md:51-100`; `evidence/noharm-760428ab.txt` | QUALITY 185 (no-harm against equivalent valid inputs) — present, but no pre-freeze instrument enforced it | `.ufo/waves/round-89/noharm-c1.py` (the reviewer's battery, entering vs graded gate) and the repair `9f4d20b9`; QUALITY 186. Able to fail: it exits 1 with `harm=13 open=6` on the first landing's bytes. |
| `tokenizer-comment-rule-is-not-the-shell's` — `shlex` treats a mid-word `#` as a comment start (`'a#b c'` → `['a']`, Python 3.14.8), where POSIX appends it to the word (S611); the first landing's `shlex.split(comments=True)` would drop every invocation after `echo x#y;`. Found by the L1 while writing repair 1, not by the battery; repair 1 still mishandled an escaped blank before `#` (Mo89R04Corpus F4, Mo89R03Repair N-E22). | `corpus/knowledge/execution-binding-r89.md` rule 1; S611; `r/Mo89R04Corpus.md` §2 | none | `strip_comments` (repair 2) applies the POSIX word-start rule, treats an escaped character as a word character, and shlex runs with `commenters=''`. Able to fail: N-E22 reads `harm` at `9f4d20b9` and `ok` at `7715bb56` (`evidence/heldout-revs.txt`); the gate arm `binding_comment_dropped` still refuses `printf 'body' # tools/x.py`. |
| `control-fixture-red-before-mutation` — skip-work control 2b appended three labels after the r88 count-c1 subject's own `own_arms_pinned` arm, so the patched pristine was red (`pass=26 fail=2`) before any mutant ran; its two `unattributed` count-c1 lines are the control's breakage, not the attribution rule. | `evidence/controls-r89.txt:44-51`; `controls-r89.sh:50-62`; `w1/Mo89R02C2.md` §4 (F1); `w1/Mo89S02Record.md` §3 | none at freeze | QUALITY 188; the control's attribution reading is cited only from its count-c2 leg. The frozen control is not rewritten. Able to fail: the counter prints `pristine-red` for any red patched subject (`controls-r89.txt:51`). |
| `newness-counted-by-helper-not-by-refusal` — r88 claimed three new gate conditions; the entering gate already refused the absent supersede target. | `corpus/lessons/round-88-verifier-spotcheck.md` routed item 1; `w1/Mo89S02Record.md` §2 | r88 closure | Named append-only corrections in `corpus/knowledge/receipt-counterfeit-r88.md` and `corpus/README.md`; original bytes kept. Able to fail: the entering bytes `1bd5ec3f` refuse the third condition. |
| `fixture-label-polarity` — the frozen r89 C1 counter prints `FX comment accepted problems=cmd-binding` for a refused fixture: the word reports expectation-met, not gate behaviour. | `.ufo/waves/round-89/count-c1.py` FX print; `evidence/after-r89.txt` | `Mo89R01C1` defect 5, `Mo89S02Record` §4 | Frozen instrument, not edited this round; disclosed here and carried. |
| `dead-attack-seats` — three w1 attack seats (`Mo89C01Critic`, `Mo89M01Mut`, `Mo89Se01Boundary`) ended on `402 Insufficient account funds` (opencode-go) with no report; w1-results.json lost every seat's final text (orchestrator kernel restart). | session transcripts `Mo89C01Critic.jsonl` etc. (last assistant `stopReason=error`) | none | Replaced by a 4-seat residual call (`.ufo/waves/round-89/r-dispatch.json`); dead seats stay dead in the record. |
| `repair-scored-on-its-own-fitting-battery` — repair 1 was declared harm-free on the 34-case battery it had been written against; 78 new cases measured 12 harms and one counterfeit it newly opened (an absolute path resolved against the production checkout). A positive model of "what executes" refuses every form it does not model. | `r/Mo89R03Repair.md` findings 1–2; `r/Mo89C02Critic.md` held-out section; `evidence/heldout-revs.txt` | QUALITY 186 "Not covered: a fixed battery is overfittable" — named, not enforced | QUALITY 189; repair 2 is built as entering-rule-minus-named-exclusions. Able to fail: `heldout-c1.py 9f4d20b9` exits 1 (`harm=12 newopen=1`). Repair 2's own batteries were read by its author — the next independent attack is the closure's. |
| `entry-overclaimed-execution` — the first landed entry said a path binds iff "a file the command executes"; control flow, uncalled functions and `uv run --directory` bind without executing it. S608's flip text ("none needed … S611 and the receipt replay now carry" the execution claim) overclaims the same way: S611 is token recognition only and the replay does not show the script ran. | `r/Mo89R04Corpus.md` F1, F2; `corpus/SOURCES.md` S608 | Mo89R04Corpus (non-author) | Entry rewritten to the exclusion rule with "not execution proof" as its first limitation. S608's cells are immutable once landed: its correct flip is recorded here — *admit only a source documenting that the tokenized command is the one the shell ran*; no such source is held. |
| `coupled-claim-anchor` — the frozen C2 mutant `C2-target` anchors on `arms=26`, a literal the C1 landing wrote into the r88 count-c2 subject; C2 cannot read met on a tree without the C1 landing, so the two claims are not fully causally separable (11 of 12 mutants are). | `w1/Mo89Sc01Scope.md` §5 | Mo89Sc01Scope (non-author) | Frozen; disclosed. Next contract: re-derive every anchor at the entering revision and refuse a population whose anchor is another claim's output. Able to fail: at `30a29797` the counter reads `unanchored=5`, including `C2-target`. |

## Gate

Sources opened this round (access date 2026-11-04 for every row):

| Row | URL | Located quote (≤25 words) | Decision |
|---|---|---|---|
| S607 | https://docs.python.org/3.14/library/shlex.html | "All characters from the comment beginner to end of line are ignored" | admit, tokenizer scope only |
| S608 | https://docs.python.org/3.14/library/shlex.html | "The shlex class makes it easy to write lexical analyzers for simple syntaxes resembling that of the Unix shell" | **reject** — a tokenizer cannot show what a shell ran |
| S609 | https://docs.python.org/3.14/library/os.path.html#os.path.normpath | "This string manipulation may change the meaning of a path that contains symbolic links." | admit |
| S610 | https://docs.python.org/3.14/using/cmdline.html | "When called with -c command, it executes the Python statement(s) given as command." / "all consecutive arguments will end up in sys.argv" | admit |
| S611 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | "If the previous character was part of a word, the current character shall be appended to that word." | admit |

S607/S609/S610 opened by `Mo89S01Sources` (fetch/locator receipt
`w1/Mo89S01Sources/sources/fetch-and-locator-receipt.txt`); S611 opened by the L1 (pinned
`evidence/sources-r89/posix-shell-v3-chap02.html`, sha256 `0889867a…`, two fetches identical).
No existing row's `status`/`recheck`/`used-by` changed. Sourced claim: C1's repair rests on
S611 (comment rule) and S610 (`-c`/`-m` data) — cited by the knowledge entry.
Assimilation: none (no `merge/mori/` theme taken).

## considerthese

`considerthese/2026-10-26.md` Suggestion 2 ("follow the unfixed critic flags forward"):
landed as the carry-over ledger below, from `w1/Mo89K01Conn.md` §4, updated at integration.

| r88 flag | r89 state |
|---|---|
| D3 kill attribution / checksum canary | fixed — P-C2 kill rule + canary arm |
| D2 `./path` refusal, comment and selfprint evasions | fixed — C1, repaired `9f4d20b9` |
| D4 twelve survivors, `want_met`, FX clean wording | fixed — `7ce712d4` |
| newness overstatement | fixed — corrections of record |
| r87 unarmed clauses, F3 host-path replay, label-substring arms | routed, carried (contract out-of-scope) |
| planned depth item 3 (r86 value-channel census) | routed, carried |
| FX label polarity in the frozen r89 counter; residual battery overfit | new, carried |

## Mistakes (repair 2, appended at integration)

| Class | Evidence pointer | Captured-by | Fix, and what makes it able to fail |
|---|---|---|---|
| `repair-tuned-on-its-own-battery` — repair 1 (`9f4d20b9`) reached `NOHARM harm=0 open=0` on the 34-case battery it was written against, while the residual reviewer's 59-case held-out battery measured `harm=11` valid equivalents refused and the critic measured three non-executing-branch counterfeits graded `met` end-to-end. | `.ufo/waves/round-89/r/Mo89R03Repair.md` §2; `r/Mo89C02Critic.md` (b) and §(b) e2e; `evidence/heldout-revs.txt` (`9f4d20b9`: `HELDOUT harm=12 newopen=1 open=25`) | QUALITY 185/186 named no-harm but no *held-out* instrument existed before data | repair 2 (`7715bb56`) and `heldout-c1.py` (78 cases from the two residual seats, `--selftest`-less by design, four revisions receipted). Able to fail: `heldout-c1.py` exits 1 with `harm=24` at `760428ab` and `harm=12` at `9f4d20b9`, and 0 at the landed revision. |
| `execution-model-overclaimed` — repair 1's docstring and the knowledge entry claimed the rule binds "a file the command executes"; the held-out battery showed valid equivalents refused and non-executing branches bound, so the model was neither sound nor harm-free. | `corpus/knowledge/execution-binding-r89.md` “Round-89 repair 2” (supersedes the framing); `r/Mo89C02Critic.md` §(a) | none — no criterion required the claimed semantics to be measured against a battery the author did not write | the landed rule is subtract-only and the entry says so, with the 30 open classes named. Able to fail: `heldout-c1.py` prints the per-case `entering`/`after` cells that contradict the old wording. |

## Round-89 correction of record — repair 2 staleness and the S608 flip text

Supersedes the considerthese ledger's `D2` cell (`| D2 ./path refusal, comment and selfprint
evasions | fixed — C1, repaired 9f4d20b9 |`, bytes kept) and the S608 row's flip wording in
`corpus/SOURCES.md` (an immutable cell; the correction lives here, per CORPUS.md rule 2).

- **D2**: the evasions and the `./path` refusal are fixed for the frozen fixtures and for both
  batteries at **repair 2 `7715bb56`**; they are not execution proof, and the control-flow
  counterfeits bind as they did on entry (30 of 78 held-out cases). The row's `9f4d20b9` named
  the repair that a non-author battery then falsified.
- **S608 flip** (`Mo89R04Corpus` F2): the rejected row's flip text says the verdict changes when
  `shlex` "documents shell execution". `shlex`'s own warning says it is "only designed for Unix
  shells" — the flip overclaims what the page could ever license. Correct flip: the row would be
  reconsidered if a page documented a *shell execution model* (grammar plus execution order), not
  a tokenizer. `shlex` stays rejected at its tokenizer scope.
- **Source digest drift** (`Mo89R04Corpus` D-src-1): the three docs.python.org page digests moved
  on the same date (the "Last updated" footer only: 16:58 → 21:57 UTC); a recheck must match on
  the quote and section, not the page sha256. S611's pinned copy matched byte-for-byte.
