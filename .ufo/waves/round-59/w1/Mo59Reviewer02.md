# Mo59Reviewer02 — C1 register-identity attack (wave w1, round 59)

Seat: reviewer (attack share), read-only. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`,
fleet root touched only via read-only `git show`. No production files, registry, SCORECARD,
LOG, or lane VCS edited; no commits. Scratch `/fast/scratch/hyaku/mori-r59/Mo59Reviewer02/`
(TMPDIR set; `--scratch` passed to the counter; cleaned before yield). Disk guard green at
start (592.6G free on `/fast/scratch/hyaku`). No tool installs (none needed). No subagents.

Measured tip: `8ff344ff18924c1ea63d46c3b3969f9fea05bc51` (wave evidence already landed there;
entering `2b9f0397…`, freeze `60b3a76…` per contract).

## Verdict summary

- **Assigned constructions — no counterexample.** A third declarer, a declarer embedded in
  non-Capabilities sections (both directions), a register table split by a `## ` heading
  (three layouts), and padded-backtick key/name cells all bind exactly as the contract
  predicate requires: every hostile shape is UNMET with the expected reason family; the
  one benign shape (phrase outside `## Capabilities`) neither hijacks nor poisons binding.
- **Adversarial finding (medium):** rows in any *second* `| key |` table inside the same
  declaring `## Capabilities` section are never scanned — a duplicate/tampered row one
  blank line below the register yields a **false `REGISTER_MET`** with empty reasons,
  contradicting the tool's own "duplicates anywhere fail" invariant. This does **not**
  invalidate the frozen C1 counter (no frozen fixture uses the shape; tip verdict and real
  arm verified unchanged), but it is a reachable false-met shape beyond the frozen
  fixture set and a robustness gap in the landed capability.

## Frozen-invariant checks (all hold)

| check | command (read-only) | result |
|---|---|---|
| counter bytes unmodified since freeze | `sha256sum .ufo/waves/round-59/count-c1.py`; `git show 60b3a76…:count-c1.py \| sha256sum`; same at `8ff344ff…` | all `2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd` |
| tool at tip == frozen PIN | `git show 8ff344ff…:tools/mori-register-check.py \| sha256sum` | `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8` (= worktree = PIN) |
| do-nothing control premise | `git show 2b9f0397…:tools/mori-register-check.py` | exit 128 (absent at entering rev → `tool_absent` arm sound) |
| fixture population | `git ls-tree … 8ff344ff…:.ufo/waves/round-59/fixtures-c1/` | 13 dirs, matching contract §9 |
| counter end-to-end at tip | `python3 .ufo/waves/round-59/count-c1.py 8ff344ff… --scratch <seat scratch>` | `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=8ff344ff…`, exit 0; `--selftest` → `C1_SELFTEST pass=6 fail=0`, exit 0 |
| real scorecard declarer uniqueness | grep `current capabilities register` / `^## Capabilities` on `SCORECARD.md` | three `## Capabilities`-titled sections (`:596` stub, `:637` round-12 demonstrations, `:1951` active); exactly one declarer phrase at `:1953` → active register uniquely identified, stubs correctly excluded |

Real arm reproduced directly (two-pass, mirroring the counter): pass 1 `REGISTER_UNMET`
listing 4 pointers (`tools/mori-vote-bind.py`, `.ufo/waves/round-56/evidence/c2-at-landed.txt`,
`tools/mori-driver-liveness.py`, `.ufo/waves/round-56/evidence/c1-at-landed.txt`); pointers
materialized from tip; pass 2 `REGISTER_MET` with
`rounds[832].capabilities_added[0] → "dual-shape seat-output vote binding (tools/mori-vote-bind.py …"`
and `rounds[832].capabilities_added[1] → "strict per-event driver-liveness probe over .ufo/watchdog.lo…"`
— both matching the frozen `BOUND` prefixes; manifest bytes from pinned fleet rev
`2807c6ab…` (2,439,846 bytes).

## Assigned constructions — method and results

Method: the PIN-byte tool loaded via `importlib` from scratch copy `tool_under_test.py`
(sha verified equal to PIN before use); hostile scorecards + manifest written under
`<scratch>/F*/`; `check(scorecard, manifest, root, REQ)` executed per fixture with
`REQ = rounds[832].capabilities_added[0,1]`, manifest `rounds[832] = {lane: mori,
lane_round: 56, capabilities_added: ["alpha bind (does a)", "beta probe (does b)"]}`,
pointer files created in-root. No `lsp` device exists in this seat's tool inventory
(recorded per review protocol); all binding evidence below is executed behavior of the
pinned bytes, not text inference.

| # | construction | verdict | reasons (exact) | bound |
|---|---|---|---|---|
| F1 | three declaring `## Capabilities` sections (third declarer) | UNMET | `binding:declared_register=3(capabilities_sections=3)`, `keys:missing=` both keys | ∅ (no binding leaks) |
| F2a | declarer phrase in `## Round 59` (prose **and** table row) and `## History`; unique caps declarer intact | MET | ∅ | both keys, correct section |
| F2b | declarer phrase only in a non-Caps section; caps section is the stub | UNMET | `binding:declared_register=0(capabilities_sections=1)`, `keys:missing=` both | ∅ |
| F3a | table split by `## Capabilities` heading; first half declares, holds key0; key1 in second half | UNMET | `keys:missing=rounds[832].capabilities_added[1]` | key0 only (partial; verdict still UNMET) |
| F3b | split table, both halves declare | UNMET | `binding:declared_register=2(capabilities_sections=2)`, `keys:missing=` both | ∅ |
| F3c | declaring section holds only the `\| key \|` header; data rows in second section | UNMET | `keys:missing=` both | ∅ |
| F4 | key cells padded inside backticks: `` ` rounds[832]…` `` and ``` ``rounds[832]…`` ``` | UNMET | `keys:missing=` both (strict `KEY_CELL`, no coercion) | ∅ |
| F4b | name cell backticked (`` `alpha bind` ``) | UNMET | `manifest:name=rounds[832].capabilities_added[0]` | both |
| F7 | control: duplicate key0 in the *same contiguous* table | UNMET | `keys:duplicate=…[0]`, `manifest:name=…[0]` | both |

Reading: declarer ambiguity always fails closed; phrase text outside `## Capabilities`
sections is inert; a `## ` split defeats binding in every layout; padded key cells are
rejected as absent rather than coerced. All four assigned attacks: **tool/counter bind
correctly**.

## Finding 1 (medium) — false REGISTER_MET via second-table row evasion

**Claim violated (tool's own docstring, `tools/mori-register-check.py:12-13`):** "every
--require'd key appears exactly once anywhere in the register table (duplicates anywhere
fail)". A required key appearing **twice** in the declaring section — the second copy in a
second `\| key \|` table after one prose/blank line — still prints `REGISTER_MET` with
empty reasons.

**Mechanism (`:77-84`):** row collection stops at the first non-`\|` line once any rows
exist (`if not ROW_START.match(ln): if rows: break`). Every later table in the same
section — and therefore every duplicate/name/`lane_round`/pointer check over it — is
invisible; `check()` builds `keymap` solely from the first table.

**Demonstrations (all `REGISTER_MET`, `reasons=[]`, `bound` = both keys from table 1):**

| fixture | second-table content (would-be reason if scanned) |
|---|---|
| F5 | duplicate key0 with capability "evil twin", separated by prose (`keys:duplicate`, `manifest:name`) |
| F5b | duplicate key0, separated by a single blank line (`keys:duplicate`) |
| F5c | duplicate key1 with `first-working round` = 99 (`manifest:lane_round`) |
| F5d | duplicate key0 with evidence `` `/etc/passwd` `` (`pointers:bad`) |

**Scope:** the frozen C1 counter is **not** invalidated — none of the 13 frozen fixtures
uses a second-table shape (f03 dup-key is contiguous and still gets `keys:duplicate`), the
tip counter verdict is `C1=met` with real arm binding the true first table, and the real
SCORECARD contains no second `\| key \|` table inside the active section. The defect is a
robustness gap of the landed capability against hostile scorecards beyond the frozen
corpus, and it means the counter's fixture arm would not notice a future regression that
truncates scanning even earlier. Recommendation (advice only — no edits made): census all
`\| key \|`-headed tables within the declaring section for missing/duplicate keys and bind
from the table containing the required keys; or narrow the docstring/contract wording to
"first table only" so the predicate matches the implementation.

## Finding 2 (low) — name-prefix delimiter set wider than documented

Docstring (`:14-17`) states the manifest string must equal `name` or start with `name (`
or `name,`; code (`:168-171`) accepts **any** next char that is non-alnum and not `_`.
Demonstrated: manifest entry `alpha bind: extra` binds scorecard name `alpha bind` → MET
(F6). Real-arm exposure is nil (manifest bytes pinned at `2807c6ab…`; the counter checks
`startswith` on frozen names), and frozen fixtures f08/f09 still cover altered and
substring-only names — but no frozen fixture pins the delimiter set, so a future
loosening here would be unobserved. "Exact name binding" overstates strictness by the
delimiter clause only.

## Observation 3 (informational) — whitespace shapes

- F8, whole-file CRLF: MET with correct binding (CRLF handled by `splitlines` + cell
  strip) — benign.
- F9, UTF-8 BOM: UNMET `binding:declared_register=0(capabilities_sections=0)` — the BOM
  glued to the first heading defeats `^## ` section detection; fails closed, so a BOM'd
  scorecard can never bind (no false-met risk; a real file saved with BOM would break the
  counter loudly rather than silently).

## Residual risk and verification gaps

- Finding 1's reach is demonstrated on synthetic scorecards; the real arm was not
  reproducible with a second table (none exists at tip) — by construction.
- Indented tables (≥1 leading space) fail `ROW_START`/`HEADER` by regex anchor — reasoned
  from the pinned source, not separately executed. Unicode-width backticks and per-line
  mixed EOL not fuzzed (outside the assigned bounded set).
- No `lsp` server available in this seat; no semantic-reference cross-check was possible.
- Evidence receipts (commands and outputs above) were captured into this report before
  scratch cleanup; scratch `/fast/scratch/hyaku/mori-r59/Mo59Reviewer02/` removed at yield.
