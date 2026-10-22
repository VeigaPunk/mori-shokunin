# Round-30 w1 — DraftProvinceR7: PROVINCE.md stale statements at `58b61681`

Seat: DraftProvinceR7 (leaf, no subagents). Scope: routed defect R7 first half — PROVINCE.md stale
statements against observed repo state at `58b61681`. I read the contract, `round-29-verifier-spotcheck.md:152-175`,
`round-29/w1/ScoutShonen.md`, then verified every claim with read-only git/read. I wrote nothing except this report.
No commits, no messages, no product or judge edits, no `omp`, no unit/systemd action, no `pacman`.

## Identity

- `git rev-parse 58b61681` → `58b61681a0e3f3b821a17d38a4e713ccd9921615`; lane `HEAD` is `e936482a6070db40049bff46f7da4754b15d41af` (later round-30 commits, not mine).
- `sha256sum PROVINCE.md` = `679a2f24ce4820fbb4ddd5c6369a99eb6477ae8a5fa30fefb3757a110f8c525e`; `git show 58b61681:PROVINCE.md | sha256sum` is the same; `git diff --stat 58b61681 -- PROVINCE.md` prints nothing. All PROVINCE line numbers below are the tip's (also the working tree's).
- `git show 7118f320:PROVINCE.md` is also 384 lines and byte-identical (`git diff 7118f320 58b61681 -- PROVINCE.md` empty), so the scout's file state and mine are the same revision.

## Result in one table

| # | Scout pointer | Actual tip line(s) | Claim at tip | Observed |
|---|---|---|---|---|
| F1 | `PROVINCE.md:32` | `:25` (plus the superseding note at `:98-101`) | "(round-16 build; verification pending)" | **stale**: round 16 admitted; scout's `:32` is unrelated prose |
| F2 | `:236` | `:236`, `:283-284` | round-24 Core row "admission pending" | **stale**: round 24 admitted |
| F3 | `:294` | `:294`, `:353-354` | round-25 Core row "admission pending" | **stale**: round 25 admitted |
| F4 | `:359` | `:359` | round-26 Core row "admission pending" | **stale**: round 26 admitted |
| F5 | `:375` | `:375` | round-27 knowledge "admission pending" | **stale**: round 27 closed `rejected-honest-stop` — not pending |
| F6 | `:66` | `:66` | tsukuroi pointer `PROVINCE.md:21-24,35-44` | **wrong range**: owns is `tsukuroi-shokunin/PROVINCE.md:8-14`; `:21-24` are surface-table rows; `:35-44` is the Adjacent heading/intro |
| F7 | `:68` | `:68` | kagi pointer `SKILL.md:49` | **dead**: `SKILL.md:49` is r15 alarm prose; secret rule is `SKILL.md:374-393` |
| F8 | not in scout | `:47`, `:90`, `:94` | `../fleet-ledger/.ufo/waves/kaika-w1/…` | **unresolvable**: no `fleet-ledger` sibling; the files are at the fleet root, `../.ufo/waves/kaika-w1/` |
| F9 | item 5 | `:44-57` vs `:321` | FR1-FR14 head, FR15 only appended | **real**: FR15 absent from the head Frontier list |
| F10 | item 5 | `:22-28` vs `:103,108,125,132,134,145,236,294,359,375` | head Core list | **undercounted by the scout**: head has 7 bullets, 10 later Core-marked bullets exist only in appended notes (scout said "four") |

Two of the scout's five pointers are off: `:32` (F1) and the counts in item 5 (F10). The remaining three and the
four "admission pending" lines reproduce.

## Evidence (commands and output)

Rounds landed — pinned fleet MANIFEST, `git -C /home/vgpnk/Projects/shokunin show 63729047:MANIFEST.json`:

```text
{"n":16,"v":"admitted","a":true}
{"n":24,"v":"admitted","a":true}
{"n":25,"v":"admitted","a":true}
{"n":26,"v":"admitted","a":true}
{"n":27,"v":"rejected-honest-stop","a":false}
{"n":28,"v":"admitted","a":true}
```

Capabilities in SCORECARD at the tip: `SCORECARD.md:1506,1518` (pressure, `PASS 12/12`), `:1546,1556` (job
runway, `PASS 21/21`), `:1598,1620` (oom killers). Tools present at `58b61681`:

```text
100755 blob 5785c5b2… tools/mori-pressure.py
100755 blob 239dd8eb… tools/mori-job-runway.py
100755 blob 69296b89… tools/mori-oom-killers.py
tool fixtures counts: mori-pressure 12, mori-job-runway 21, mori-oom-killers 32
```

Round-16 evidence: `corpus/lessons/round-16-verifier-spotcheck.md:11` reads
`**status: ok · admitted: true · verdict: admitted.**`; `LOG.md:1061` records the window selftest
"**16/16**" (receipts at `.ufo/waves/round-16/evidence/window-selftest.json`); and PROVINCE already carries its own
superseding note at `:98-101`.

Round-27 evidence: `corpus/lessons/round-27-verifier-spotcheck.md:77` — "verdict **rejected-honest-stop**";
`SCORECARD.md:12` (depth row) — "round 27's depth improvement was verified under a rejected-honest-stop closure and is
not counted".

F6 tsukuroi bytes (read at sibling tip, 189 lines): `tsukuroi-shokunin/PROVINCE.md:8-14` is
`**Owns (surfaces, all read-only probes):** pacman state … what pins/holds exist.`; `:20-23` are the Arch News,
pacnew, initramfs and snapper table rows; `:35-44` is `## Adjacent — finding-to-owner handoffs` plus its intro. The
sibling's routing line is at `:32-33` ("fleet correlation belongs to mori"), which mori's `:288` already cites
correctly.

F7 SKILL bytes: `grep -n 'The r15 repair is deliberately narrow' SKILL.md` → `49:` at both `58b61681` and the
working tree. The secret rule is `SKILL.md:374` (`## Secret-exposure exclusions`), bullets `:379-386` and
`:391-393`.

F8 path sweep (`grep -oE … PROVINCE.md | sort -u | while read … test -e`) reports
`MISS ../fleet-ledger/.ufo/waves/kaika-w1/mori-state.md`, `MISS ../fleet-ledger/.ufo/waves/kaika-w1/mori-art.md`;
`ls -d fleet-ledger` at the fleet root → absent. The targets exist at the fleet root and are committed at the pinned
MANIFEST: `git ls-tree 63729047 .ufo/waves/kaika-w1/mori-state.md` → blob `4494d7cb…`,
`git show 63729047:.ufo/waves/kaika-w1/mori-state.md | sha256sum` =
`6d7ce6a4a0b4e42d89541c783d42d4ce52b93dc4905cf3cf61eb724e2dd6dea5` = the working file. Line anchors still hold:
`:180` is the C5 row containing `ls /scratch` → absent; `:31` is the driver-counter row; `:190` is C15
(counter/MANIFEST). `mori-art.md:91-124` holds the S001-S030 registry table.

F9/F10: `grep -n` on the tip gives FR1 at `:44` … FR14 at `:57`; `FR15` occurs only in the round-25 note
(`:294`, `:321`). Core bullets start at `:22,23,24,25,26,27,28` (7); Core-marked appended bullets at
`:103,108,125,132,134,145,236,294,359,375` (10).

## Replacements

Every item below is a same-line substitution: no line count changes. That matters — the lane cites PROVINCE line
numbers in ~100 places (most frequent `PROVINCE.md:45` ×28, `:53` ×22, `:55` ×17, `:377` ×7; sweep over
`corpus SKILL.md SCORECARD.md LOG.md .ufo/waves/round-2*`), so an insertion would silently re-point all of them.

### F1 — `:25`

```text
old: (round-16 build; verification pending)
new: (round-16 build; admitted round 16 — `corpus/lessons/round-16-verifier-spotcheck.md:11`)
```

### F2 — `:236` and `:283-284`

```text
old: - **Core, one-shot system pressure reading (FR12 partial advance, admission pending):**
new: - **Core, one-shot system pressure reading (FR12 partial advance, admitted round 24):**
```

```text
old:   system CPU `full` flagged undefined. The Core row above is **pending admission** by the
old:   non-author closure. No frontier row is closed, no other lane's surface is claimed, and no remediation
new:   system CPU `full` flagged undefined. The Core row above was **admitted** by the round-24
new:   non-author closure. No frontier row is closed, no other lane's surface is claimed, and no remediation
```

### F3 — `:294` and `:353-354`

```text
old: - **Core, harness background-job capacity runway read (new FR15 advance, admission pending):**
new: - **Core, harness background-job capacity runway read (new FR15 advance, admitted round 25):**
```

```text
old:   run returned `RUNWAY_CLAMPED` with effective 100, exit 1. The Core bullet above is **pending
old:   admission** by the non-author closure. No frontier row is closed, no other lane's surface is
new:   run returned `RUNWAY_CLAMPED` with effective 100, exit 1. The Core bullet above was **admitted
new:   by the round-25 non-author closure. No frontier row is closed, no other lane's surface is
```

### F4 — `:359`

```text
old: - **Core, one-shot userspace OOM killer read (FR10 partial advance, admission pending):**
new: - **Core, one-shot userspace OOM killer read (FR10 partial advance, admitted round 26):**
```

### F5 — `:375`

```text
old: - **Core, knowledge (FR10 partial advance, admission pending):** how earlyoom 1.9.0 and the Linux 7.2 kernel choose
new: - **Core, knowledge (FR10 partial advance; round 27 closed `rejected-honest-stop`, so this advance is not admitted):** how earlyoom 1.9.0 and the Linux 7.2 kernel choose
```

### F6 — `:66` (evidence cell only)

```text
old: `../tsukuroi-shokunin/PROVINCE.md:21-24,35-44`
new: `../tsukuroi-shokunin/PROVINCE.md:8-14`
```

The rest of that row (R12Connector sentence, the two tsukuroi knowledge files, `PROVINCE.md:12-16`) resolves and
stays.

### F7 — `:68`

```text
old: `SKILL.md:49`
new: `SKILL.md:374-393`
```

### F8 — `:47`, `:90`, `:94`

```text
old: ../fleet-ledger/.ufo/waves/kaika-w1/
new: ../.ufo/waves/kaika-w1/
```

(repeated on all three lines; the path resolves from the lane root to `/home/vgpnk/Projects/shokunin/.ufo/…`.)

### F9/F10 — head lists (choose one; both are pointer-safe)

Preferred, no shift: append one correction block at EOF (after line 384).

```markdown
## Round-30 correction — head lists

The `## Core` head (`:22-28`) lists seven bullets and does not repeat the Core additions appended per round:
round 17 `:103`, `:108`; round 18 `:125`, `:132`, `:134`; round 20 `:145`; round 24 `:236`; round 25 `:294`;
round 26 `:359`; round 27 `:375`. The `## Frontier` head (`:44-57`) lists FR1-FR14; FR15 is the round-25 appended
row at `:321`. Neither head is a completeness claim, and this block moves no line.
```

Alternative if the head itself must name FR15: append to the FR14 bullet on `:57` (same line, no shift):

```text
old: ... telemetry emission belongs to the emitting lanes and orchestration.
new: ... telemetry emission belongs to the emitting lanes and orchestration. FR15 (harness background-job capacity runway) is appended in the round-25 note at `:321`.
```

## Checked and not defects

- `:47` FR4 first-evidence line anchors (`:31,190`) still carry driver-counter/MANIFEST material; only the path prefix is wrong (F8).
- `:288` tsukuroi `PROVINCE.md:30-33` is accurate at sibling bytes.
- `:65` kumitate `PROVINCE.md:3-6` is thin but line 3 does say "scopes OMP task/hub"; the wave plan/run/record/collect claim is carried by `swarm-wave-lifecycle.md:28-34,91-120`, which resolves (140 lines).
- `:67` kama `:3-15,40-53` and `:69` souji `:8-17,50-52` resolve (souji `:50-52` is the mori adjacency paragraph). Souji's pinned-commit equality (`fe7590b3`) was not re-verified — it needs git in a sibling repo, which this seat did not run.
- `:371` `tsukuroi-shokunin@157ee255:corpus/knowledge/memory-pressure-r25.md` exists in the sibling working tree (402 lines); the pinned commit was not re-verified for the same reason.
- All lane-local paths cited by PROVINCE resolve at the tip (tools, fixtures, knowledge, lessons, `PROVINCE.md`, `SKILL.md`), apart from the three F8 prefixes.
- Rounds 28 (admitted) and 29 (rejected-honest-stop) have no PROVINCE note. No statement is false because of that; whether the lane wants a per-round note is the L1's call, not a defect I can ground in a contract.

## Limits

- The scout's `:32` is a bad pointer: editing there would corrupt the Round-15 prose at `:30-33`. Use `:25`.
- Sibling files were read at their current working-tree bytes, not pinned revisions (except the fleet-root kaika files, pinned at `63729047`). [INFERENCE] tsukuroi/kumitate/kama/souji line numbers are stable enough for this round but are not revision-pinned here.
- Line-count safety is measured for the lane's own citations; fleet-wide references outside the lane were not swept.
- No tool was installed or upgraded; no settings, session or credential material was read or copied.

## Files touched

- This report only: `.ufo/waves/round-30/w1/DraftProvinceR7.md`.
