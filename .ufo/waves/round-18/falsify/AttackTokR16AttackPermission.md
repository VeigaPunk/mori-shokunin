# AttackTokR16AttackPermission — wave-2 falsification of the r18 token redactions in `.ufo/waves/round-16/build/AttackPermission.md`

Seat: `MoriR18Recovery.AttackTokR16AttackPermission-2` (falsifier, leaf; no subagent dispatch).
Range: entering `d005cdd` → attacked `e2bfbd6`. The only commit touching the file in range is
`b8f5c6c` (`git log --oneline d005cdd..e2bfbd6 -- <path>`, exit 0, single row), matching the
triage row "Frozen-class identity tokens in 22 non-routed files … commit b8f5c6c"
(`.ufo/waves/round-18/out-of-metric-triage.md`, Dispositions table).

## Axes

(A) redaction completeness per changed line, (B) residual values on the same/neighbouring
lines, (C) semantic/structural breakage (markdown, JSON validity where applicable), (D)
consistency of the L1's keep-name-only allowlist decision with the frozen rule.

## Method (what actually ran; all exit 0)

1. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-16/build/AttackPermission.md` — 1 file, 2 insertions, 2 deletions; hunks `@@ -13,7 +13,7 @@` and `@@ -62,6 +62,6 @@` (changed lines 16 and 65).
2. `git -C … show d005cdd:<path>` and `show e2bfbd6:<path>` — full both-rev content read; 68 lines each (line-count stable, 1:1 replacement).
3. `grep AttackPermission` on `.ufo/waves/round-18/frozen/c1-population.json` — exactly 2 rows: line 16 class R2 (`line_sha256` b77377f6…f406), line 65 class R2 (`line_sha256` f2c2aa76…ecf7f).
4. sha256 of pre-edit lines 16 and 65 (no-newline variant, via `git show | python3 -c` checksum pipeline): b77377f6cdfdbd9a… and f2c2aa7606429ffd… — both reproduce the frozen population hashes, confirming the enumeration bound exactly the two lines the edit changed.
5. Scripted scan of the post-edit tip blob against all nine classes of `frozen/c1-policy.json` (R1–R9, regexes as frozen): `any_class_hit = False`; the only lines containing `withheld` are 16 and 65.
6. No C1 gate execution (not this seat's tool; sibling MutRetentionGate owns it). No JSON in the changed set, so `python3 -m json.tool` is N/A. No scratch writes anywhere; no tool installs or upgrades (nothing installed; channel N/A).

## Per-changed-line judgment

### Line 16 (hunk `@@ -13,7 @@`) — Counterexamples evidence header

- (A) Completeness: the sole private token on the line was class R2 (session_store_path) — a glob into the session store including the project subdirectory and per-seat transcript name pattern. Replaced wholesale by the placeholder. No R1/R3/R4/R5/R6/R7 token occurred on the line. **Complete.**
- (B) Residuals: same line — none. Neighbouring lines 13–19 (P1 table row and header) carry lane-internal operation timestamps, `/tmp` artifact names/sizes and a lane background-job id; all are round-16 lane work or world-readable host temp metadata, explicitly non-findings under the triage decision rule (`.ufo/waves/round-18/out-of-metric-triage.md`, "Decision rule"). No session-record value, routing value, or per-seat retry value remains.
- (C) Meaning: backticks balanced, sentence intact; the table below still identifies the seats, so dropping the non-private `MoriR16/MoriR16.<Seat>.jsonl` pattern costs only locator precision, no claim. Line count unchanged, so line-number citations from other lane files into this file remain valid. Markdown valid; not JSON.
- Over-redaction note (minor, no-harm): the replacement removed the project subdirectory and file-name pattern together with the store root, though only the R2 root was the private token. Strictly more conservative than required; accepted.

### Line 65 (hunk `@@ -62,6 @@`) — own-conduct reads bullet

- (A) Completeness: sole token class R2, removed; remaining text keeps only class-level mentions ("raw cursor and 32-hex values") with an explicit assertion that none appear, which the file's own scan statement corroborates. No other token class on the line. **Complete.**
- (B) Residuals: neighbours 62–68 (classification line, conduct bullets) contain `/tmp` metadata-read descriptions only — no session-record, routing, or retry values.
- (C) Meaning: "`<session-store path withheld>*.jsonl` seat transcripts" preserves the glob semantics readably; markdown intact; not JSON. Cosmetic awkwardness only.

## Population/triage binding cross-check

- Frozen population (`.ufo/waves/round-18/frozen/c1-population.json:38-41,43-47`): 2 hits, both R2, both redacted — the triage family "Frozen-class identity tokens in 22 non-routed files … token-redacted" matches this file's token kind (store path).
- Disposition was redact, not allowlist: consistent with `frozen/c1-policy.json` `adjudication_rule` (redaction is strictly safer than allowlisting and needs no row) and leaves no allowlist surface to go stale for this file.

## Axis D — the L1's keep-name-only decision as applied to this file

Name-only mentions retained at `e2bfbd6`, each judged against the triage decision rule and the frozen `adjudication_rule` (a)/(b):

| Retained mention (line) | Kind | Verdict |
|---|---|---|
| `toolCall` (:16) | assistant-message field name, no value | allowlist-consistent (rule: field names, not values) |
| `__CURSOR`, `_BOOT_ID` (:~46) | journal field names; sentence asserts values masked and repo-scan found 0 real cursors | allowlist-consistent; metadata-about, not content-of |
| `agent.db*` (:65) | credential-adjacent surface name used in a negation ("not … a credential file") | allowlist-consistent |
| `bg_2667` (:P5 row), commit `1ccac09` (:P4 row), lane report paths (`build/Province.md:3` etc.), seat names, lane event timestamps | lane-internal ids/paths of the round under review | non-findings per the triage decision rule |
| cursor-shape sketch `s=0…0;i=1;b=0…0;…` (:severity note) | shape, not an instance; file itself reports a 0-hit scan for real 32-hex cursors in `build/*.md` | allowlist-consistent |

**Verdict: sound.** No residual value in this file is misclassified as a name-only mention;
the decision matches how sibling rows (SeatNaming family) were treated and the frozen rule's
(a)/(b) categories. One boundary observation, not a defect: rule (b) literally scopes field
names to "lane tool code, a contract or synthetic fixture", while `toolCall` here is a field
name cited in a build report — it is covered in spirit by the triage rule's "field names"
carve-out and by (a) as a boundary statement, but the two rule texts do not name this exact
case. If the L1 wants the allowlist corpus airtight, one clarifying clause would close it;
as applied here it changes no outcome.

## Findings

No blocking or major finding. The two redactions are complete, correctly bound to the frozen
population rows (hash-verified), leave no missed value on the same or neighbouring lines,
preserve line numbering and both lines' technical meaning, and scan to zero against all nine
frozen classes at `e2bfbd6`. Minor notes only: over-redaction of the non-private
name pattern on :16 (accepted, safer direction) and the rule-text boundary gap on field-name
citations in reports (Axis D, no outcome change).

## Residual risk and verification gaps

1. History is not rewritten: the R2 tokens remain present at `d005cdd` and every earlier revision; the repair reduces tip-state exposure only, not historical exposure. This is declared (`contract.md` repair-first item 1: exposure assessment operator/kagi-owned), so it is not counted against the round's claims — but no C1 "before/after" number may be read as exposure reduction.
2. The placeholder text itself discloses the category of what was withheld ("session-store"); inherent to any redaction marker, judged harmless.
3. Draft-verdicts' "55 remaining hits at `daceeec`, all name-only … pending allowlist rows" (`.ufo/waves/round-18/draft-verdicts.md`, C1 row) does not include this file (fully redacted, zero pending rows) — no tension, but the 55 and revision `daceeec` were not audited under this item.
4. Only the tip blob was regex-scanned; the pre-edit scan was by manual class inspection over full both-rev content plus hash binding, not a scripted R1–R9 run (irrelevant post-edit, since the population proves exactly two class occurrences existed).
5. No gate execution and no JSON validation were applicable from this seat (methods above); sibling seats own the gate arms.
