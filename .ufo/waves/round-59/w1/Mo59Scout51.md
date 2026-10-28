# Mo59Scout51 — mori absent-defect-register slice recon (round 59, quarantine slice)

Read-only recon. Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` was read, never edited; lane repo read-only (no git writes); live fetches ran in scratch `/fast/scratch/hyaku/mori-r59/Mo59Scout51` (TMPDIR there), cleaned after copying receipts here. No tool installed or upgraded; disk-guard green at start (592.6G free on /fast/scratch/hyaku).

## 1. Slice re-derivation (per contract §Quarantine, the canonical awk)

```sh
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='mori' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
```
Output (identical to round-45 derivation; the command is frozen in `.ufo/waves/round-45/w1/ExecCollisionGuard.md:222-224`):
```
 S244`   the cited source could not be fetched, so no quote was checked
 S262`   the cited source could not be fetched, so no quote was checked
 S268`   the cited source could not be fetched, so no quote was checked
```
Slice = **exactly 3 rows, no new rows since round 45**: `absent-defect-register.md:356-358`, all in the `## Rows whose quotes were NEVER CHECKED` table (the file's own class text calls these `unreachable`, *not* the fabrication class — header lines 13-14; 109 never-checked rows total over 18 lanes):

| line | lane | round | id | class | cited source |
|---|---|---|---|---|---|
| 356 | mori | round1 | S244 | cited source could not be fetched | https://doi.org/10.1145/3643916.3644413 |
| 357 | mori | round4 | S262 | cited source could not be fetched | https://doi.org/10.1109/TSC.2026.3698682 |
| 358 | mori | round5 | S268 | cited source could not be fetched | https://doi.org/10.1109/TSC.2026.3698682 |

Note: S262 and S268 cite the *same* DOI (ROMA, IEEE TSC 2026) — two distinct registry rows for one document.

## 2. Identity / staging / lane registry state

- Literal ids absent from staging: `grep -c` on `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` — S244/S262/S268 all 0. Renumbered counterparts: S244→S483 (SOURCES.append.md:19, DOI 10.1145/3643916.3644413), S262→S501 (:37), S268→S507 (:43), both DOI 10.1109/TSC.2026.3698682.
- Lane registry `corpus/SOURCES.md`: no S244 row (S551:331 is the same rationale-paper DOI, status `rejected`); S262 present at line 243 (status A, OpenAlex abstract scope); no S268 row, but the same DOI is held by S478:257 (publisher VOR PDF, pinned sha256) and S552:332.

## 3. Fresh hand-check (2026-10-28, this seat)

Commands and observed outputs (scratch: `/fast/scratch/hyaku/mori-r59/Mo59Scout51/`):

```sh
curl -sS -L -A "$UA" 'https://doi.org/10.1145/3643916.3644413'   # S244
# http=403 size=5684 → https://dl.acm.org/doi/10.1145/3643916.3644413  (ACM blocks this UA)
curl -sS -L -A "$UA" 'https://arxiv.org/abs/2403.18832'          # S244 arXiv carrier
# http=200 size=41919
curl -sS -L -A "$UA" 'https://doi.org/10.1109/TSC.2026.3698682'  # S262+S268
# http=202 size=0 → https://ieeexplore.ieee.org/document/11540439/  (still 202/0 bytes, drift reported not fixed)
curl -sS -L -A "$UA" 'https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf'  # S268 VOR
# http=200 size=2357114 type=application/pdf
sha256sum roma_ielx8.pdf
# 1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2  == S478/S552 pinned digest
curl -sS 'https://api.openalex.org/works/W7163066205?select=title,doi,abstract_inverted_index'  # S262
# http=200 size=2766; title/doi/abstract_inverted_index all identical to committed copy
# corpus/evidence/sources-r42/S262.oa.json
```

Located quotes:

- **S244** — reachable? *partially*: ACM DOI landing 403 from this host, but the same paper's arXiv abstract fetched cleanly. Quote: the register row carries **no quote span and no locator** (never-checked table has only the DOI); the staged counterpart S483 grounds on the abstract. In the fetched abstract I located: *"We find that 98.9% of commits in our dataset contain sentences with rationale information."* → **UNVERIFIABLE** (no intended quarantine quote to check; not fabrication). Matches round-58 recheck verdict (SOURCES.md:391).
- **S262** — reachable? *yes via OpenAlex* (DOI landing still 202/0; OpenAlex live response byte-equal in title/doi/inverted-index to committed `corpus/evidence/sources-r42/S262.oa.json`). Located quote at abstract positions 27–39: *"the default Out-of-Memory (OOM) mechanism lack sufficient container context when selecting victim processes."* — grounds the row's abstract-level teaches. → **PRESENT** (admitted since round 42; row unchanged).
- **S268** — reachable? *yes via publisher VOR PDF*: fresh fetch sha256 `1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2`, byte-identical to the r48-scout fetch and the S478/S552 recorded digest. Located quote (pdftotext lines 139–141): *"It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping to record OOM-triggering process metadata."* → **PRESENT** (in staged counterpart S507; the register row itself had no quote — the quote was located in its renumbered twin).

## 4. Verdicts vs prior rounds

| row | r48 scout | r58 recheck | r59 (this seat) |
|---|---|---|---|
| S244 | PRESENT via arXiv (fetch resolves prior failure) | unverifiable (no intended quote/locator) | **UNVERIFIABLE** — carrier reachable, no quarantine quote exists to check |
| S262 | PRESENT via OpenAlex | PRESENT (quote pos 27–39) | **PRESENT** — live OpenAlex byte-equal to committed copy |
| S268 | PRESENT via VOR PDF | PRESENT | **PRESENT** — sha256 matches lane-pinned PDF |

None is fabrication-class; all three were `unreachable`-class rows (quote never checked), and all three source carriers are now reachable from this host, with the DOI landing pages still not serving bytes (ACM 403, IEEE 202/0). Slice count unchanged: still 3 mori rows, no additions.

Opened paths: absent-defect-register.md (1-40, 329-375); mori-shokunin `corpus/SOURCES.md` (243, 257, 331-332, 385-395); shokuknow `merge/mori/SOURCES.append.md` (19, 37, 43); `.ufo/waves/round-45/w1/ExecCollisionGuard.md` (awk, 222-224); `.ufo/waves/round-48/w1/ScoutQuarantineS268.md`, `ScoutQuarantineS262.md`, `ScoutQuarantineS244.md`; `.ufo/waves/round-59/contract.md`, `count-c1.py`, `count-c2.py`; `corpus/evidence/sources-r42/S262.oa.json`.
