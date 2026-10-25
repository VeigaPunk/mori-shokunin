# RevAssimPlan — r48 w1: assimilation-plan review (the plan, not the entry)

Seat: RevAssimPlan (leaf, no subagents dispatched). Reviewed the assimilation **plan**: the frozen
contract `contract.md` (freeze `4387cf9`, entering tip `e5dbac0`) — §C2 preamble, P-C2, Separability,
§Frontier step — against the round prompt's assimilation contract `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-48.md`
§10 (lines 440–545), and the package bytes `/home/vgpnk/Projects/shokuknow/merge/mori/`
(`MERGE-REPORT.md`, `SOURCES.append.md`) plus read-only registry/register facts. Also read
`.ufo/waves/round-48/v3-spec.md` per dispatch. Only this report file was written; no tool installed;
no lane tool run (no scratch needed — all checks were read-only against package and lane files).

## Rule-by-rule verdict

| # | §10 rule | Plan as stated in contract.md | Verdict | Evidence |
|---|---|---|---|---|
| 1 | ONE theme | L53–56 + L97: "Assimilation: theme FR2 (quota)". One theme. | PASS | Package quota set coherent: 6 entries under `knowledge/corpus/knowledge/` (`quota-observability-r38`, `quota-counter-freshness-r39`, `quota-id-to-path-r40`, `quota-id-mapping-files-r41`, `quota-path-listing-r42`, `join-inputs-empty-r43`), all FR2. |
| 2 | 1–3 entries | L63–64 commits exactly one new entry (`quota-observability-r48.md`); L90 "the FR2 entry" (singular). 1 ≤ 3. | PASS | P-C2 + Separability name no second entry. |
| 3 | Re-open every cited source; Gate carries YOUR access date + ≤25-word located quote | L65–70: every row `opened 2026-10-25`, quote 6–25 words located in the committed copies under `corpus/evidence/sources-r48/`. Copies verified present (exactly `aliyun-nas-quota.html`, `errno.h`, `quotactl.2.html`, `xfs_quota.8.html`), pinned by the four frozen URLs in `count-c2.py` L37–44. The staged entry's fifth quota source S481 (RHEL 9 PDF) is dropped with a verified reason (L59–60: HTTP 403, plain + browser UA, 2026-10-25). | PASS | Adopted entry's citation set = the four re-opened sources. See F2 (flip condition missing). |
| 4 | ≥1 admit AND ≥1 reject recorded in `## Gate` | L97 commits the mechanism ("Admit/reject per entry in the lesson `## Gate`"); P-C2 commits the admit. The only planned refusals are source-level (L59–61) and row-level quarantine verdicts (L97–98). No refused **entry** is committed anywhere in the plan. | **AT RISK → F1** | See F1. |
| 5 | Id collision check, 0–3-space pattern, scratch before append | L55–56: "sources staged as S477-S482, which collide with lane S477/S478 and are renumbered by document". Verified against the working tree with the §10 pattern (`^ {0,3}\|[ \t]*S\d{3,}`): lane = 251 unique ids, max **S478**; lane holds S477 and S478; staged quota S479–S482 all free; "new ids start at S479" (dispatch/claims) is feasible — the four adopted rows fit S479–S482 exactly. | PASS | Plan-facts verified; see F4 for registry drift that makes the §10 pre-append check load-bearing. |
| 6 | Schema normalisation (11 columns, ISO recheck, no `\|`) | Plan restates only the id half ("renumbered by document", L55–56). Verified the six staged quota rows (SOURCES.append.md L13–18): **11 columns each, no escaped or literal `\|`, status `mined`, recheck `180d` (valid NNd cadence), used-by present**. The remaining adoption-time normalisation — `opened` 2026-10-23 → 2026-10-25, `used-by` re-point r38 → r48, ids renumbered — is forced by P-C2 (L63–70) and the counter's selftest arms ("unmined row, row opened on another day, missing used-by"), so the plan cannot land un-normalised rows and still print `C2=met`. | PASS | The §10 kengaku-style defects (escaped pipes, prose recheck cells) are absent from mori's quota rows — verified, not assumed. |
| 7 | Quarantine rows not appended until hand-checked this round | L98: "The three quarantine-slice rows (S244, S262, S268) get a hand-check verdict each." Register slice re-derived from the register bytes per §10: mori data rows = **exactly 3**, ids `S244`, `S262`, `S268`; all three carry prose class "the cited source could not be fetched, so no quote was checked" → §10's unchecked family → verdict is `unverifiable` unless the seat fetches and locates (unreachable ≠ fabrication). None of the three ids is in the append set (adopted rows = staged S477/S478/S479/S482 → lane S479–S482), so no quarantine row feeds the entry. | PASS | See F5 for the verdict-semantics obligation. |
| 8 | `doctrine/` not material | Plan never cites `doctrine/`; package contains none — `merge/mori/` top level is `MERGE-REPORT.json`, `MERGE-REPORT.md`, `SOURCES.append.md`, `amendments/`, `knowledge/`. | PASS (vacuous) | Glob listing. |

## Findings (by severity)

**F1 — medium (rule 4).** The plan as stated in `contract.md` does not commit any Gate **reject**, so
the §10 floor "The lesson's `## Gate` records ≥1 admit and ≥1 reject from the assimilation set" is not
satisfied by the plan alone. Contract lines: L63–70 (P-C2 commits the admit of the single entry), L90
("the FR2 entry", singular — no second entry is taken that could be refused), L59–61 (the only planned
rejections are **source**-level: RHEL 9 PDF "not part of this claim", Solaris `errno=49` "stays
rejected" — a carry-over, not this round's verdict), L97–98 (Gate instruction and quarantine verdicts;
the latter are row-level and their outcome — all three register rows carry the "could not be fetched"
class — is contingent on fetch results). If the closure reads "not part of this claim" as claim scoping
rather than a Gate reject, the round lands `## Gate` at 1 admit / 0 reject and breaks §10 rule 4.
Recommendation (plan-level, not for me to execute): commit one explicit Gate reject — the natural
candidate is recording the S481 refusal as a Gate reject with reason + flip condition, or taking and
refusing one of the five unadopted quota-theme entries (stays within the 1–3 cap).

**F2 — low (rule 3 hygiene).** For the refused source S481 the plan states the reason (L59–60, HTTP 403
verified 2026-10-25) but no **flip condition**; §10 requires "Refused entries keep reason + flip
condition in the Gate block". Same for the Solaris `errno=49` carry-over (L60–61: reason lives in the
prior round, flip condition not restated). Execution must add both to the Gate block or the refusal
records are incomplete per §10.

**F3 — medium (package layer; not a contract break).** `MERGE-REPORT.md` §Adopt checklist conflicts
with §10 on four points; a dispatcher following the checklist verbatim would break rules 2, 3, 4, 6 and
the append-only id rule:
- L121 step 1 names `SOURCES-PROPOSED.md`, which does not exist in `merge/mori/` (top-level listing
  above) — unexecutable as written.
- L122 step 2 "Spot-reopen **a sample** of rows" vs §10 "re-open **every** cited source … the campaign's
  `opened` date and quote prove nothing about this lane".
- L123 step 3 "Append `SOURCES.append.md` to `corpus/SOURCES.md`" = bulk-append of all 136 rows as-is,
  vs §10 "Append only the rows the admitted entries cite; never bulk-append a package" and "no staged
  row is appended as-is" — and it would import the 8 colliding ids S471–S478.
- L124 step 4 "Copy **each** `knowledge/<path>`" (80 entries) vs §10's 1–3 entry cap.
The frozen contract's plan does **not** follow the checklist (one entry, renumber-by-document,
per-entry Gate; §10 makes the package advisory and §10 mechanics binding). No contract line breaks
here — but the round report/lesson should state the deviation from the package checklist explicitly,
since MERGE-REPORT presents itself as "the adoption interface".

**F4 — info (rule 5).** `MERGE-REPORT.md` L9 "lane registry currently holds **243** rows" is stale: the
working tree now has **251** unique ids under the §10 pattern (max S478; drift +8 = S471–S478 now
occupied; staged set S471–S606 collides on 8 ids overall, of which 2 fall inside the quota theme). The
contract already accounts for this (L55–56 renumber-by-document), and §10's scratch-check-before-append
plus guard-proof fixture (a scratch indented-collision fixture must produce nonempty `collisions`)
remain execution obligations the contract does not restate — the check must be re-run at append time
against the then-current registry, not against today's snapshot.

**F5 — info (rule 7).** All three register mori rows carry the prose class "the cited source could not
be fetched, so no quote was checked" — §10's unchecked family. Hand-check verdicts must therefore be
`unverifiable` unless the seat actually fetches the cited source and locates the quote this round
("`unreachable` is not fabrication"), and the verdicts land in the lane's lesson and report, never as
edits to the register (contract L98 is consistent with this).

## Evidence (command → observed output, exit 0 for each)

1. Read-only Python set/schema check (eval cell; reproduces the §10 `grep -oE '^ {0,3}\|…'`/`comm -12`
   logic without shell grep, since tool policy mandates the grep tool for regex search):
   - lane `corpus/SOURCES.md`: 251 ids / 251 unique, max S478, no duplicate ids; S477=True, S478=True,
     S479–S486 all False in lane.
   - staged `SOURCES.append.md`: 136 ids, first S471, last S606; full-set collisions vs lane =
     S471–S478 (8); quota staged ids in lane: S477=True, S478=True, S479/S480/S481/S482=False.
   - staged quota rows L13–18 (S477–S482): `cols=11 escape_pipe=False status='mined'
     opened='2026-10-23' recheck='180d' recheck_iso_or_NNd=True`; S480's used-by is
     `oom-evidence-loss-r38.md, kernel-oom-line-attribution-r12.md` (not the quota entry — consistent
     with the adopted entry citing the other four/five rows); S477/S478/S479/S481/S482 used-by =
     `corpus/knowledge/quota-observability-r38.md`.
   - register `absent-defect-register.md`: data rows per lane — mori **3** (S244, S262, S268, each
     class "the cited source could not be fetched, so no quote was checked"); tabi 38, revenger 26,
     chousa 24, kotodama 21 (matches §10's 2026-10-24 note, re-derived).
   - `merge/mori/` listing; `knowledge/corpus/knowledge/` quota files (6); lane
     `corpus/evidence/sources-r48/` = exactly the four copies.
2. `nl -ba .ufo/waves/round-48/contract.md` — line numbers used for citations above.
3. `grep 'https?://…' .ufo/waves/round-48/count-c2.py` — four frozen URLs + sha256 pins (L37–44):
   xfs_quota.8.html, quotactl.2.html, errno.h (torvalds v7.2 raw), aliyun NAS set-quotas page — each
   matching one committed copy and one staged quota row's URL.
4. Reads: `contract.md`, `v3-spec.md`, `MERGE-REPORT.md` (incl. L117–129 checklist verbatim),
   `SOURCES.append.md` (quota rows), round prompt L440–545.

## Tooling record (operator directive 2026-10-19)

Nothing installed or upgraded; no pacman (paused host-wide); no lane tool executed (TMPDIR rule not
triggered); no writes outside this report.

## Residual risk and verification gaps (UNVERIFIED here)

- I did not fetch the four sources myself; the freeze's committed copies + sha256 pins in `count-c2.py`
  are taken as the re-open receipt (other seats hold the quote manifests).
- I did not run `count-c1.py`/`count-c2.py`, the census, or the freeze sha256 check — counters and
  receipts are other seats'/L1's instruments; nothing here re-audits them.
- The collision check ran against the **current working tree**, not the landed tip; the registry moves
  (243 → 251 observed drift), so §10's scratch re-check immediately before the first append stays
  mandatory and its guard-proof fixture unproven as of this review.
- The S244/S262/S268 payload hand-checks are other seats' assignments; I verified only the slice's
  composition and class cells, not the cited payloads.
- Whether the non-author closure will accept a source-level refusal (S481) as the §10 "reject" is a
  judgment call this seat cannot pre-empt — hence F1 is reported as at-risk, not as a certain break.
