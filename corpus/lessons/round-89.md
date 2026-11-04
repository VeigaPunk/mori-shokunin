# Round 89 — mori (L1 MoriR89), attempt 1 — lesson

Entering revision `30a29797012281b9fd0c748b38b929ac67f8c754` (r88 closed `rejected-harmed`,
`corpus/lessons/round-88-verifier-spotcheck.md`). Frozen contract
`.ufo/waves/round-89/contract.md` at `d4438695998894aad7ff9b20f46d9f1852ea3c7d`, controls
`.ufo/waves/round-89/evidence/controls-r89.txt` committed before any after-value.

## What the round did

- **C1 (operability)** — the r87 receipt gate binds the executed script by path identity.
  First landing `760428ab` met P-C1 but the w1 reviewer `Mo89R01C1` measured 13 valid
  equivalents newly refused and 6 counterfeit bindings still bound. The binding was repaired
  at `9f4d20b9` (invocation-aware parser, arms unchanged at 26); `noharm-c1.py` reads
  `harm=13 open=6` rc 1 at `760428ab` and `harm=0 open=0 gained=3` rc 0 at `9f4d20b9`.
- **C2 (calibration)** — the twelve r88 survivors armed (seats `Mo89E01ArmsC1`,
  `Mo89E02ArmsC2`), landed `7ce712d4`; P-C2 `C2=met mutants=12 killed=12 survivors=0
  unattributed=0 unanchored=0 arms=28,26` at `9f4d20b9`.
- Receipt `.ufo/waves/round-89/evidence/after-r89.txt` (both predicates and the no-harm line).
- Frontier: S607, S609, S610, S611 admitted, S608 rejected; knowledge
  `corpus/knowledge/execution-binding-r89.md`; QUALITY 186–188.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix, and what makes it able to fail |
|---|---|---|---|
| `met-predicate-hid-operability-harm` — the first C1 landing printed the frozen met line while refusing 13 valid equivalent commands the entering gate bound (`python3 -I -B`, `python3.14`, env prefixes, `--`, `-W ignore`, `nice`, quoted `;`, `&&`, `exec`, `uv run`, `bash -c`) and still binding 6 counterfeits (`-W`/`-X` value lookalikes, `-c`/`-m` values). The contract froze three fixtures and no equivalence battery. | `.ufo/waves/round-89/w1/Mo89R01C1.md:51-100`; `evidence/noharm-760428ab.txt` | QUALITY 185 (no-harm against equivalent valid inputs) — present, but no pre-freeze instrument enforced it | `.ufo/waves/round-89/noharm-c1.py` (the reviewer's battery, entering vs graded gate) and the repair `9f4d20b9`; QUALITY 186. Able to fail: it exits 1 with `harm=13 open=6` on the first landing's bytes. |
| `tokenizer-comment-rule-is-not-the-shell's` — `shlex` treats a mid-word `#` as a comment start (`'a#b c'` → `['a']`, Python 3.14.8), where POSIX appends it to the word (S611); the first landing's `shlex.split(comments=True)` would drop every invocation after `echo x#y;`. Found by the L1 while writing the repair, not by the battery. | `corpus/knowledge/execution-binding-r89.md` rule 1; S611 | none | `strip_comment` applies the POSIX word-start rule and shlex runs with `commenters=''`. Able to fail: the gate's own arm `binding_comment_dropped` still refuses `printf 'body' # tools/x.py`, and `A09-hash-glued` (`'BODY'#tools/…`) stays refused in the battery. |
| `control-fixture-red-before-mutation` — skip-work control 2b appended three labels after the r88 count-c1 subject's own `own_arms_pinned` arm, so the patched pristine was red (`pass=26 fail=2`) before any mutant ran; its two `unattributed` count-c1 lines are the control's breakage, not the attribution rule. | `evidence/controls-r89.txt:44-51`; `controls-r89.sh:50-62`; `w1/Mo89R02C2.md` §4 (F1); `w1/Mo89S02Record.md` §3 | none at freeze | QUALITY 188; the control's attribution reading is cited only from its count-c2 leg. The frozen control is not rewritten. Able to fail: the counter prints `pristine-red` for any red patched subject (`controls-r89.txt:51`). |
| `newness-counted-by-helper-not-by-refusal` — r88 claimed three new gate conditions; the entering gate already refused the absent supersede target. | `corpus/lessons/round-88-verifier-spotcheck.md` routed item 1; `w1/Mo89S02Record.md` §2 | r88 closure | Named append-only corrections in `corpus/knowledge/receipt-counterfeit-r88.md` and `corpus/README.md`; original bytes kept. Able to fail: the entering bytes `1bd5ec3f` refuse the third condition. |
| `fixture-label-polarity` — the frozen r89 C1 counter prints `FX comment accepted problems=cmd-binding` for a refused fixture: the word reports expectation-met, not gate behaviour. | `.ufo/waves/round-89/count-c1.py` FX print; `evidence/after-r89.txt` | `Mo89R01C1` defect 5, `Mo89S02Record` §4 | Frozen instrument, not edited this round; disclosed here and carried. |
| `dead-attack-seats` — three w1 attack seats (`Mo89C01Critic`, `Mo89M01Mut`, `Mo89Se01Boundary`) ended on `402 Insufficient account funds` (opencode-go) with no report; w1-results.json lost every seat's final text (orchestrator kernel restart). | session transcripts `Mo89C01Critic.jsonl` etc. (last assistant `stopReason=error`) | none | Replaced by a 4-seat residual call (`.ufo/waves/round-89/r-dispatch.json`); dead seats stay dead in the record. |

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
