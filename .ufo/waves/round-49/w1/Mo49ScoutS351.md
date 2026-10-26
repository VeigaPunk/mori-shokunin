# Mo49ScoutS351 — the lane's earlier refusal of the journal-reach theme (row S351)

Seat: scout, leaf, read-only. Lane tip read: `0df17b7b` (round-49 freeze). Date of report 2026-10-25, after the lane tip's author date (2026-10-25 20:30). Observed = read from committed bytes with `grep`/`sed`/`git ls-files`; the `lsp` device was not used (this is prose/Markdown, not code). Nothing was run on the host, no tool run, nothing mutated.

## 1. Where S351 came from

`grep -n S351` over `corpus/SOURCES.md`, `corpus/README.md`, `LOG.md`, `corpus/lessons/`:

| place | line | what it is |
|---|---|---|
| `corpus/SOURCES.md` | 248 | the row itself |
| `corpus/lessons/round-43.md` | 40-46 (Gate bullet), 52-54 (Reject paragraph), 68 (search log), 99 (assimilation) | the lesson that **created** it (Round 43, Gate opened 2026-10-24, author "Kimi fresh L1 (mori-r43)") |
| `corpus/lessons/round-43-verifier-spotcheck.md` | 164, 175, 179, 187 | non-author spot-check: "reject — agree" |
| `corpus/lessons/round-44.md` | 45-48 | second look: "Row S351 stays `rejected` (round 43); not re-opened" |
| `LOG.md` | 2527 | round-43 log summary |
| `corpus/README.md` | no hit | not in the coverage map |

The `## Gate` block of `round-43.md` is at line 12 ("Opened 2026-10-24."). S351's entry there:

> S351 (rejected) — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — quote (Commands section): "--vacuum-size= removes the oldest archived journal files until the disk space they use falls below the specified size". Rejected: the staged `journal-reach-at-ceiling-r46.md` grounds itself in a shokuknow `file://` note and a kernel `MESSAGE` grep, neither of which this lane may treat as evidence. Flip: the public `--vacuum-size=` sentence plus a committed read-only disk-usage receipt, and no MESSAGE grep. recheck `180d`. status rejected.

Gate "Reject" paragraph (round-43.md:52-54), same wording minus "read-only": "Reject: `journal-reach-at-ceiling-r46.md`. Reason: cites a shokuknow `file://` note and a kernel MESSAGE grep. Flip: public `--vacuum-size=` sentence plus a committed disk-usage receipt, no MESSAGE grep. Row S351, status rejected."

## 2. Rejection reason and flip as written (verbatim, `corpus/SOURCES.md:248`)

Row cells: tier B; scope "the archived-journal store's own size ceiling and reach; refused as an admitted source this round"; anchor "journalctl(1) Commands section, --vacuum-size= and --disk-usage entries; … opened 2026-10-24"; status `rejected`; opened `2026-10-24`; recheck `180d`; used-by `—`.

- **Reason (as written):** "REJECTED: the staged journal-reach entry grounds itself in a shokuknow file:// note and a kernel MESSAGE grep, neither of which this lane may treat as evidence"
- **Flip (as written):** "the public --vacuum-size= sentence plus a committed read-only disk-usage receipt, and no MESSAGE grep"

Important reading: the rejection is about the **staged entry's grounding**, not the page. The round-43 spot-check says so directly (`round-43-verifier-spotcheck.md:175`): "Quote present (18 words…). The rejection is about the staged entry's grounding … not about the page; the flip is public-sentence-plus-committed-receipt, which is admissible."

## 3. Does the round-49 plan meet each flip element?

Plan (contract.md:80-83): public sentence from the committed copy + committed read-only receipt + no MESSAGE grep, new row opening `supersedes S351 —`.

| flip element | state at `0df17b7b` | verdict |
|---|---|---|
| (a) public `--vacuum-size=` sentence | `corpus/evidence/sources-r49/journalctl.1.html` is tracked (`git ls-files` lists all four copies). After the counter's own normalisation (script/style/comment dropped, tags stripped, entities decoded, whitespace collapsed) the text reads "--vacuum-size= removes the oldest archived journal files until the disk space they use falls below the specified size. Accepts the usual …" — found; the quoted sentence is 17-18 words, inside the 6-25 word band. The same page also has "--vacuum-size= has only an indirect effect on the output shown by --disk-usage, as the latter includes active journal files, while the vacuuming operation only operates on archived journal files" (this is the sentence to quote for "total can sit above ceiling"). sha256 of the copy: `75440570…9722`. | **met** |
| (b) committed read-only disk-usage receipt | `corpus/evidence/sources-r49/host-journal-reach.txt` (tracked, sha256 `be3952cb…eb12`, captured 2026-10-25T20:43 -03:00; header says no vacuum/rotate/config change run). Holds `journalctl --disk-usage` → 56M, `--system` → 19M, `--user` → 37M, all `[exit 0]`, plus `cat-config`, `stat` of the drop-in, `findmnt`, `--list-boots`. Every command is a read. | **met** |
| (c) no MESSAGE grep | **Not clean by the letter.** The same receipt (lines 95-97) contains `$ journalctl -b 0 -u systemd-journald --no-pager -q -g 'Journal .* is .*max'` — a `journalctl -g` (MESSAGE regex) over the daemon's own limit lines. It is not the *kernel* MESSAGE grep the rejection named (that was `grep -c 'Killed process'`-class), and it is a read-only, unit-scoped filter of the daemon's own start-up line, but the flip text says "no MESSAGE grep" without qualifier, and sibling scout `w1/Mo49ScoutStagedJournal.md` (lines 22, 121, 177) already read the flip that strictly (it refuses `grep -c 'max 256M'` as a MESSAGE grep). The receipt is frozen (cannot be re-captured without changing a frozen sha256), so the entry must choose: (i) cite the daemon line only as an observation with an explicit scope note ("daemon's own limit line via `-u systemd-journald -g`; not a kernel MESSAGE grep and not a retention claim"), or (ii) leave that line unquoted so no claim depends on a MESSAGE grep, and (iii) in every `recheck:` use only `--disk-usage`, `--list-boots`, `findmnt -no FSTYPE /run`, `ls -A /run/log/journal`, `systemd-analyze cat-config`. | **met only if** the entry does not rely on the `-g` lines and its recheck avoids `-g`/`grep`; the receipt content itself is a literal gap |

Other S351 reason elements, as applied to the plan: "shokuknow `file://` note" — the plan cites none (the staged own-work rows S524/S537/S544/S554 are not adopted; contract.md:74). "kernel MESSAGE grep" — none (no `Killed process`/`oom_kill` counter in the plan). So both reasons for rejection are removed; the flip's third clause is the only place with residual doubt, as above.

One count-c2.py detail that bears on (c): the counter's own scaffold `recheck:` line uses `curl … | grep -c SystemMaxUse` (count-c2.py:267) — that is a fixture for a counter selftest, not the entry; the counter does not check the entry's `recheck:` contents, so the "no MESSAGE grep" element is enforced by nothing mechanical. It rests on the reviewers.

## 4. Does `journal-disk-usage-total-r51.md` (S470) already cover ground?

Read `corpus/knowledge/journal-disk-usage-total-r51.md` (12 lines). It:
- cites S470 (journalctl(1) page, opened 2026-10-24, recheck 180d, tier A);
- quotes the `--disk-usage` sentence: "Shows the current disk usage of all journal files. This shows the sum of the disk usage of all archived and active journal files." → a reading is a total, not a per-journal bound and not a vacuum ceiling;
- records one read-only host reading on 2026-10-24: `269M`, exit 0, with "not a license to vacuum, rotate, or change journald";
- says it cites "the `--disk-usage` sentence only" and "No service was signaled".

Overlap with the round-49 plan: the `--disk-usage` sentence (a quote the new entry may also need) and the idea "total ≠ ceiling". It does **not** cover: `--vacuum-size=` (S351's quote), `journald.conf(5)` (`SystemMaxUse=`, `RuntimeMaxUse=`, `MaxRetentionSec=` — contract.md:76-77: 0 occurrences in SOURCES.md/knowledge at `b3e3453d`), `systemd-journald.service(8)`, the persistent-vs-volatile split, or the effective ceilings. Its receipt is the 269M capture of 2026-10-24; today's receipt reads 56M (contract.md:108 records the move). S470's row is `mined`, opened `2026-10-24`, used-by only `journal-disk-usage-total-r51.md`.

Consequence for C2: S470 **cannot serve as a row** for the new entry's journalctl quotes. `count-c2.py` requires each row to be opened `2026-10-25` and to list the new entry in `used-by` (contract.md:87-89; selftest arm "row_opened_other_day_unmet", count-c2.py:315-316). Extending S470's used-by in place would be rule-2-legal but fails the counter on the opened date; and S470's `opened` cell cannot change. So the journalctl page needs a fresh row anyway (this is the planned S485-S488 `journalctl.1.html` row), and the `--disk-usage` quote in the new entry cites that new row. S470's entry stays as the per-command definition; the new entry should link to it by path in prose, not duplicate it, and should say the 269M vs 56M difference is a time movement (UNVERIFIED cause; sibling scout `Mo49ScoutStagedJournal.md:13` records no `Vacuuming`/`Deleted` line in retained boots).

## 5. S351 status/used-by under CORPUS.md rule 2 versus supersede

CORPUS.md rule 2 (`/home/vgpnk/Projects/shokunin/CORPUS.md:116`): "Append-only. Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson. A correction is a new row whose `teaches` opens `supersedes S0NN —`."

Option A — change S351 in place (not recommended): would need `status` rejected→`mined` and `used-by` `—`→`corpus/knowledge/journal-reach-r49.md` (status `mined` means "cited by ≥1 path in used-by", CORPUS.md status definition), each logged old→new in `round-49.md` `## Gate`. Defects that cannot be edited away: `opened` stays `2026-10-24` → fails the C2 counter's "opened 2026-10-25"; `teaches` still reads "REJECTED: …; flip: …" on a `mined` row (contradiction, and `teaches` is immutable); the `scope` cell still says "refused as an admitted source this round"; the anchor does not name `journald.conf`/`journald.service`/the receipt; the id is one of several rows on the journalctl URL (S014, S351, S470 — W04, not E04, because scopes differ). It also destroys the rejection-is-taste record ("a rejection is evidence of taste", CORPUS.md status `rejected` — "kept").

Option B — leave S351 untouched, append a new row (this is what contract.md:83 plans, and what rule 2's last sentence prescribes for a correction): the new row (journalctl page, `mined`, `opened 2026-10-25`, used-by `corpus/knowledge/journal-reach-r49.md`) has `teaches` opening exactly `supersedes S351 — ` (three fields: `supersedes`, the id, an em dash; I read the rule text as `supersedes S0NN —`, so S351's row id written as `S351`, then ` —`). The `supersedes` opener also keeps it clear of E04 (duplicate URL+scope without supersedes; `scripts/sources-census.sh` header line 25) should the new row's scope match S351's. Required S351 changes: **none** — `status` stays `rejected`, `used-by` stays `—`, `recheck` stays `180d`. The round lesson `## Gate` should record "S351 unchanged (rejected); superseded by S4xx" with the Gate quote and flip-element table above, so nobody later reads the stale rejection as live. S351's `recheck` of 180d (due 2026-04-22) is not reached; no cadence edit needed.

The census (`scripts/sources-census.sh`) classifies by status: `rejected` rows with a thin `teaches` raise W02; S351 is not thin. No census rule requires a superseded row to change.

## 6. Recommendation to the L1 (facts, not a judge)

1. Option B; S351 byte-identical; new row `teaches` begins `supersedes S351 —` and says the flip was met by a committed copy plus receipt, not by re-reading the rejected staged entry.
2. In the lesson Gate, state the S351 flip element by element (table in §3), including the (c) caveat honestly: the frozen receipt carries one daemon-scoped `-g` line; the entry does not quote it as retention evidence and its `recheck:` uses no `-g`/`grep`.
3. Do not cite S470 as a row of the new entry (opened-date arm); keep it as a prose link.

## Findings

- **MED** — `corpus/evidence/sources-r49/host-journal-reach.txt:95-97`: the frozen receipt includes `journalctl -b 0 -u systemd-journald … -g 'Journal .* is .*max'`, a MESSAGE regex, while S351's flip text (`corpus/SOURCES.md:248`) says "no MESSAGE grep" unqualified. It is the daemon's own unit-scoped limit line, not a kernel-MESSAGE grep, but nothing in `count-c2.py` enforces the clause. Handling: do not rest a claim on those two lines, scope-note them if quoted, use non-`-g` rechecks.
- **MED** — `count-c2.py` checks quotes, rows, pins and provenance but not the entry's `recheck:` text; the "no MESSAGE grep" element of the S351 flip is enforced by review only (count-c2.py:267 shows even its fixture uses `| grep -c`).
- **LOW** — S470 (`corpus/SOURCES.md:249`, opened 2026-10-24) cannot be a source row for the new entry (opened-date arm of the counter); the entry must cite the new journalctl row and treat `journal-disk-usage-total-r51.md` as a prose neighbour. Its 269M reading versus today's 56M is a one-day movement with UNVERIFIED cause.
- **LOW** — S351 must stay untouched: any in-place `status`/`used-by` change cannot fix `opened`, `teaches` or `scope`; supersede is the only path that satisfies C2 and rule 2.
- **LOW** — `corpus/evidence/sources-r49/host-journal-reach.txt:96-97` carries the host name (`plazir27`) in the committed receipt; the machine id is already `MACHINE_ID`. Not a credential; flagged for the L1's redaction pass (another seat, `Mo49ScribeReadme-2`, is already on it).
- **LOW** — `round-43.md:52-54` omits "read-only" from the flip that the `SOURCES.md` row and the Gate bullet carry; the three wordings of one flip differ by that word and by "and". The row (`SOURCES.md:248`) is the authoritative one (it carries the cell the census reads).
