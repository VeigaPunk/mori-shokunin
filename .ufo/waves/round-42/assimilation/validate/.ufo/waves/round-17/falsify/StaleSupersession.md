# StaleSupersession — r16 correction completeness, fresh falsification

Seat: `MoriR17.StaleSupersession-4` (leaf, read-only). Round 17, wave 2, 2026-10-20.
Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Assigned claim: r16 open-queue item 4 corrections are explicitly superseded in
`PROVINCE.md`, `corpus/README.md`, `SKILL.md`,
`corpus/knowledge/journal-cursor-window-r16.md`; historical host systemd 261.2-1 vs
current 262-1 is dated, and no historical text is rewritten.

Entering tip: `24526ea9617cd020fee16c28fe4d4a2789dc28cb`. Observed current tip:
`5c1dfb8d0530c74eb0e1630c2b522b735b486274` (worktree clean except untracked
`.ufo/waves/round-17/falsify/`, wave2 dispatch files).

**Verdict: the supersession claim survives (required corrections 2/2 present, 0
missing). One uncorrected r16 summary statement remains in `corpus/README.md`, and
one citation is second-order. Neither contradicts the dated 261.2-1/262-1 claim,
which I re-verified against the package log.**

## Method

- `git log --oneline 24526ea..HEAD -- PROVINCE.md SKILL.md corpus/README.md corpus/knowledge/journal-cursor-window-r16.md`
  → only `273aa74` (rc0).
- `git diff --numstat 24526ea..HEAD -- <four files>` → PROVINCE `27/0`, SKILL `6/1`,
  README `18/0`, note `13/0`; total `+64/−1` (rc0).
- Obligation source: `corpus/lessons/round-16-verifier-spotcheck.md:220–223`
  (item 4: supersede PROVINCE “verification pending” and the note's `verified-at`
  host-version statement, appended, “do not rewrite history”).
- Version truth: file reads of `/var/log/pacman.log` and one read-only
  `pacman -Q systemd`. No `journalctl` invocation, no live journal query, no
  fixture/gate/selftest run. No tool installed or updated.

## Correction count (entering → current)

| Obligation (r16 verifier :220–223) | Current correction | Present |
|---|---|---|
| PROVINCE “verification pending” superseded | `PROVINCE.md:96–101` appended: “Supersedes ‘verification pending’ in the same-boot window Core row”, cites closure `:9–17` | yes |
| Knowledge-note `verified-at` host version superseded | `corpus/knowledge/journal-cursor-window-r16.md:138–149` appended: dated 261.2-1 (r16) → 262-1 (today), “No new journal query or re-pin is implied” | yes |
| (not an r16 item; lane's own restatement) | `corpus/README.md:351–366`, including `:361–364` | yes |

Required corrections **2/2**, missing **0**. Supersession statements in scope: **3**
(PROVINCE:98, note:140, README:361). No historical rewrite: both originals are
byte-preserved (`PROVINCE.md:25` still says `(round-16 build; verification pending)`;
`journal-cursor-window-r16.md:2` still says “Host systemd version was not verified”),
and the diff is insertion-only in PROVINCE/README/note. `SKILL.md` carries no
“pending”/261/262 text (`grep -n "pending\|verification\|261\|262"` finds nothing),
so it had 0 r16 obligations.

## Version claim re-verified (not taken on trust)

- `/var/log/pacman.log:2462` `[2026-10-20T09:15:30-0300] [PACMAN] Running 'pacman -Syu …'`;
  `:2464` “starting full system upgrade” `09:15:31`.
- `:2531` `[2026-10-20T09:16:28-0300] [ALPM] upgraded systemd (261.2-1 -> 262-1)` — inside
  the same transaction (started `09:15:30`, before `transaction completed`).
- `pacman -Q systemd` → `systemd 262-1` (rc0).
- r16 observation time was genuinely 261.2-1: `.ufo/waves/round-16/evidence/live-window-user.json`
  `started_at` `2026-10-20T09:12:11.730609+00:00` (= `06:12:11-0300`) and commit
  `9de05bd` at `06:17:08-0300`, both before the `09:16:28-0300` upgrade.
  The note's “inside the 09:16 full-upgrade transaction” is accurate at line
  granularity (the transaction began `09:15:30`; the systemd line is `09:16:28`).

## Findings

1. **Uncorrected stale summary — `corpus/README.md:41` (confidence: high on the
   textual conflict; medium on intent).** The r16 coverage row still ends
   “host systemd 261.2-1 `--help`/`man` checks only, **no journal read**”, while the
   note it summarizes records two live captures: `corpus/knowledge/journal-cursor-window-r16.md:127–133`
   (“one live observation per scope returned `MORI_JOURNAL_WINDOW_OK`,
   `records_after_anchor=0`”; receipts `evidence/live-window-{user,system}.json`).
   The r17 corrections paragraph (`README.md:361–364`) supersedes only the
   host-version half, not “no journal read”. If the cell means “source acquisition
   did no journal read”, it is merely ambiguous; as written it reads as a
   whole-note claim and is false for the L1 captures. This is the one candidate
   missing correction in the four surfaces.
2. **Second-order citation — `corpus/knowledge/journal-cursor-window-r16.md:142–143`
   (confidence: high).** “records host **261.2-1**, as confirmed by
   `corpus/lessons/round-16-verifier-spotcheck.md:220–223`” cites the verifier's
   *instruction to correct*, not the version record. The verifier line itself only
   says “the lesson records host 261.2-1 from version lookups”. The primary records
   are `corpus/lessons/round-16.md:69` (M25: `pacman -Q systemd` → 261.2-1),
   `:73` (M29: `journalctl --version` banner) and `:153`. The claim is true; the
   citation chain is one hop longer than needed and does not name the primary row.
3. **Supersession replaces a verification caveat with a non-verifying source class
   ([INFERENCE], confidence: medium).** `round-16.md:69` classes the 261.2-1
   package query “Inadmissible as verification”. The appended note does not claim
   verification — it says “records”, and “No new journal query or re-pin is
   implied” — so no false statement is made; but a reader may take “superseded” as
   an upgrade from “not verified” to verified. Stating “recorded metadata, not
   verification” explicitly would close this.
4. **PROVINCE discoverability, not a defect (confidence: high).** `PROVINCE.md:25`
   keeps the literal stale phrase; the only supersession is at `:98`, after the
   round-12 Corrections section, with no inline pointer from the Core row. This is
   exactly the append-only discipline the r16 item mandated, so it complies; a
   grepper still sees both statements.
5. **Out-of-scope observation — `SKILL.md:164` (confidence: high).** The single
   deletion in the four files (`6/1`) replaces the census self-test cell
   “104/104 at 8d22d18, census SHA `0e41cb83…`; `.ufo/waves/round-14/evidence/census-selftest.json`”
   with “r17 measured tally and hash in round-17 evidence”. The replacement tally is
   backed: `.ufo/waves/round-17/evidence/census-selftest.json` is rc0,
   `MORI_CENSUS_SELFTEST: PASS (125 cases, 125 passed, 0 failed)`,
   `measured_commit 273aa74…`, `stdout_sha256 d5f0f1ba…`. That receipt contains **no
   census-script SHA**; the only census hash is `PINNED_INPUTS.json`
   `tools/mori-census.sh: 12e8e2d9…`, which lives in `round-17/`, not
   `round-17/evidence/`. Minor wording imprecision, not r16 history and not a
   falsifier of the append-only claim.

## Attacked scope and what remains

Attacked: the four assigned surfaces at entering `24526ea` vs current `5c1dfb8`,
the r16 item-4 obligation text, the dated 261.2-1/262-1 transition, and
append-only preservation of r16 bytes. Not attacked: `LOG.md`, `SCORECARD.md`,
`corpus/QUALITY.md`, `corpus/SOURCES.md`, the r16 wave directory, the truth of
the r16 closure beyond its two quoted supersessions, and any live journal
behaviour. Remaining unknown: whether the lane intended `README.md:41`
“no journal read” as source-acquisition-only (finding 1); no artifact states it.

Per-seat tool record: none installed or updated (no pacman/uv/npx transaction).
