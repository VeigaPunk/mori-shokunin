# ConnectOwnerFinal — round 23, scoped ownership review (read-only, pinned)

**Seat:** `MadoR22-2.ConnectOwnerFinal` (connector, leaf — no subagent dispatch).
**Assigned item:** recheck the final quota province/knowledge boundary against **tsukuroi**
(OS diagnosis/configuration) and **souji** (cleanup).
**Pins read (all read-only, no writes outside this report):**

| Artifact | Revision | sha256 |
|---|---|---|
| `mori-shokunin/PROVINCE.md` | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` | `cdfb32c79be0a1de9954b376024e3190f3be6eabe6290fa2c8d81a3096dc1f63` |
| `mori-shokunin/SKILL.md` | same | `dc7e0f421242de7858a3f0abc1ffca3a4bfc49c5d71984ef9588975282f8702b` |
| `mori-shokunin/corpus/knowledge/quota-surface-r23.md` | same | `2614a8f133072b27a3d5e07a7ad5d70455f509ef4052c01a9ad7e112879b8c84` |
| `mori-shokunin/tools/mori-quota-surface.py` | same | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| `souji-shokunin/PROVINCE.md` | `473e98a` (souji HEAD) | `3a2364d7cbea724485f64d3ff97ce9eb723f013559b969c491343320d582bda8` |
| `tsukuroi-shokunin/PROVINCE.md` | `6266682` (tsukuroi HEAD) | `a296da872e83731f7f7a7737662988558ebb97e4399681a1099fab4a259b7a79` |

Seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` is a strict ancestor of the pinned
production (`measure4/summary.json` → `seal_is_strict_ancestor_of_revision: true`).
Per L1's redirect, the **Core-advancing province draft is void and not integrated**, Main
withdraws production/admitted C2 after the pinned readers settle, **FR2 stays Frontier, Core
unchanged**. This report therefore reviews the **existing** boundary only and proposes no
province Core advance, no quota command, no configuration read, no remediation and no
next-round scope. Every quoted line was read at the pinned bytes above.

---

## 1. Axes

- **A1 — tsukuroi leg.** Does the shipped quota surface read, name or imply anything inside
  tsukuroi's owned ground (host OS diagnosis/configuration: package, systemd unit, driver,
  boot, mount/unit configuration, Snapper/rollback net, superblock quota features)?
- **A2 — souji leg.** Does the boundary correctly state who owns **reclamation/cleanup** of the
  pressure a quota/runway finding reports, without mori absorbing cleanup and without naming a
  lane that may remove files it may not?
- **A3 — negative / no-diagnosis fence (cross-cutting).** Does anything in the existing output
  or docs attribute a *cause*, a *configuring agent*, a *limit* or an *exhaustion verdict*, or
  imply a remediation path?

---

## 2. Verdict per axis (exact bytes, no blanket pass)

### A1 — tsukuroi leg: **holds, at the byte level.** No gap found.

Read-set of the shipped tool is exactly the kernel-visible inputs and nothing else. The whole
file has **three** `open()` sites and **one** `subprocess` site:

- `tools/mori-quota-surface.py:633` `read_sysfs_text(...)` — a sysfs attribute text read.
- `tools/mori-quota-surface.py:660` `open(MOUNTINFO, ...)`, with `MOUNTINFO = "/proc/self/mountinfo"`
  (`:152`).
- `tools/mori-quota-surface.py:697` `open(path, ...)` — the **fixture** document, fixture mode only.
- `tools/mori-quota-surface.py:1823` `subprocess.run(...)` — inside `--selftest` only (re-invoking
  this same CLI per arm).

Everything else is `os.listdir`/`os.stat`/`os.path.realpath` (`:581`, `:594`, `:605`, `:644`,
`:660-684`). There is **no** fstab read, no `systemctl`/`*.mount` read, no Snapper/config read,
no superblock read, no `quotactl`/`ioctl`, no `btrfs`/`xfs_quota`/`repquota`/`mount` invocation and
no write path — the only `subprocess` call is the selftest's own CLI re-execution. Real mode
**never** opens `qgroups/mode`: `scan_btrfs_sysfs` sets `mode = None` (`:599`) and reads only
`qgroups/enabled` (`:611`); `LIMITS` states "the btrfs qgroups mode attribute is never read, so
`btrfs_qgroups_mode` is null in real mode" (`:163`).

The fence is **also stated, in mori's own words, in two places**:
`SKILL.md:601-605` — "Configuration/causes belong to tsukuroi/operator: no fstab, mount units,
Snapper, superblocks, quotactl, btrfs, xfs_quota, repquota, mount or remediation" — and
`corpus/knowledge/quota-surface-r23.md:87-97` ("Ownership fence"), which adds the
realpath/stat automount caveat and the per-ID/EDQUOT-attribution remainder.

No contested ownership exists on tsukuroi's side: `git ls-tree -r --name-only 6266682` in
`tsukuroi-shokunin` yields **no** path matching `quota|qgroup|edquot`, and tsukuroi's own
routing rule selects the owner "by the question being asked" (`tsukuroi-shokunin/PROVINCE.md:59-60`).
The quota question is a runway question (mori's declared surface, `mori-shokunin/PROVINCE.md:10`),
while mount/unit configuration is tsukuroi's. The split is correct as written.

### A3 — negative / no-diagnosis fence: **holds.** No cause, agent, limit or verdict leaks.

The emitted object is `payload()` (`:774-783`): `schema`, `finding_id`, `exit_code`, `paths`,
`df_covers_quota`, `limits`; the setup variant (`:786-795`) adds only a fixed `error` token with
`paths: []`. A per-path row carries exactly `path, fstype, mount_point, quota_state, enforcement,
basis, device_check, quota_option_keys, btrfs_qgroups_mode` (`OUTPUT_FIELDS`, `:175-186`).
`quota_option_keys` is the sorted set of **recognised key names only** — no option values, no
mount source, no UUID, no filename. `basis` is a closed vocabulary of evidence-class tokens
(`xfs_noquota_option`, `btrfs_qgroups_dir_absent`, `ambiguous_overmount`, `device_mismatch`, …),
never a cause. `df_covers_quota` is a constant `False` (`:780`). `LIMITS` (`:155-164`) carries the
negative statements, including "QUOTA_DISABLED is not a capacity or health verdict; ENOSPC can
coexist". Neither `SKILL.md` nor the knowledge note names a configuring agent as the cause:
Snapper appears only inside the **exclusion** lists (`SKILL.md:601`, note `:90`).

### A2 — souji leg: **GAP — two exact, provable defects in mori's own live documents.**

**Gap S1 (false sibling quotation + dead line-cite in mori's Adjacent table).**
`mori-shokunin/PROVINCE.md:69` reads:

> `| souji | Owns artifact cleanup, not process/fleet health. Its province says "mori-shokunin observes fleet health and reports; souji acts on artifacts" (`../souji-shokunin/PROVINCE.md:40-41`). | …`

At souji's current HEAD `473e98a` that quoted sentence **does not exist**: the string
"souji acts on artifacts" occurs **0** times in souji's current `PROVINCE.md`. Souji replaced it
in its round-18 commit `42d9ff3`; the current adjacency text is at `souji-shokunin/PROVINCE.md:50-52`:

> "mori-shokunin observes fleet and host health (liveness, kill/OOM, runway) and reports; souji lists
> only its own uid's scratch residue and routes liveness or resource findings to mori. Complementary."

And the cited range `40-41` in souji's current bytes is **not** adjacency text at all — it is
souji's **Refuses** list: `:40` "- Any artifact whose owning lane has dirty or unpushed work
touching it." and `:41` "- Publishing, vault approval, remote creation — operator-owned.". The
range was correct only at souji's mint (`ccbb132`, where the bullet sat at line 40) and had
already drifted to line 46 by `42d9ff3^`.

Mori's own file already knows this: `PROVINCE.md:183-190` (Round21 souji-citation erratum) says
"the adjacency table's old quotation is historical; current souji scope is
`../souji-shokunin/PROVINCE.md:8-17,50-52`". So `PROVINCE.md` **contradicts itself**: `:69`
presents a superseded quote as souji's current words at a dead line-cite, while `:183-190`
corrects it. This is not a claim about the withdrawn probe; it is a standing ownership statement
in mori's live file, and `:69` is the cell a reader consults for cleanup ownership.

**Gap S2 (the *reclamation* half of a runway/quota finding is owned by "operator", but mori
never says so — and the one cell that could is the stale one).**
`mori-shokunin/SKILL.md` contains **zero** occurrences of "souji" (verified: `grep -c souji
SKILL.md` → 0), and the two-tier finding→owner routing table (`SKILL.md:350-353`) lists tier 1 =
`tsukuroi` · `kama` · `kumitate` · `mori`, tier 2 = `kumitate` (orchestration) · **operator** (host
mutations, "service restarts, pacman, cgroup limits, mounts, **deletions**"). So the *deletion*
actor is already named: the operator. What is unnamed is the **scratch-residue reclamation
proposal** step that a runway/quota pressure finding would actually need, and the neighbours'
own provinces foreclose the obvious substitutes:

- `tsukuroi-shokunin/PROVINCE.md:27-28`: "Never installs, upgrades, or removes packages; never
  restarts services. Detection and report; the operator remediates." — tsukuroi does not remove
  files. Souji states the same boundary from the other side: "tsukuroi-shokunin repairs host
  operability and never removes packages; souji removes files and never touches the OS"
  (`souji-shokunin/PROVINCE.md:53-54`).
- `souji-shokunin/PROVINCE.md:50-52` narrows souji to "its **own uid's** scratch residue", and
  `:42` refuses "Live lane work products (current-round drafts, uncommitted reports)"; `:17`
  keeps souji at "Dry-run censuses and **removal-list proposals for operator approval**".

The residue class that actually produced this fleet's recorded quota events is **other lanes'**
residue, not souji's own-uid scratch: `souji-shokunin/census/round-8/final-21.json:77` records
"/tmp quota pressure: 13G/16G (80%) … dominated by OTHER lanes' fixture residue (arc2-l3r3-C1-inst
1.6G, seat50 927M, seat44-a4b 885M, coldrun-b 518M, kotodama-r8-o14 345M …)"; and
`census/round-6/final-116.json:192` records "tmpfs 16G size, 13G used, 3.1G avail, 80% —
filesystem not full; git still reported Disk quota exceeded. quota -s printed nothing. Which quota
rejected the write is uncertain" — i.e. the mechanism was never observed and the **pressure** was
residue. `census/round-10/seat-04.json:159` records "The host /tmp DISK QUOTA is active … This is a
host issue, not a tool defect."

So: a quota/runway pressure finding legitimately splits into a *mechanism-configuration* question
(tsukuroi/operator — already routed, `SKILL.md:601`) and a *residue-reclamation* question. The
second question's **deletion** actor is named in mori's registry (`SKILL.md:353`, operator), but
the **proposal** step is not, and the one cell that mentions souji misstates souji's scope in a way
that reads as general artifact authority. The honest, minimal statement is the one mori already
uses elsewhere (`PROVINCE.md:151`: "a misrooted file is routed to its lane L1 (souji's refusal fence
covers live round outputs), never moved by mori"): mori reports; reclamation is **not mori's**;
souji's surface is own-uid, receipt-gated, list/proposal-only; the operator holds the actual
deletion. The gap is the **missing link between the two halves** — the residue is other lanes',
souji's surface is own-uid only, and the deletion is the operator's — none of which any mori
document states together.

### What this seat did **not** find, and did not claim

- No C2 admission is claimed here. At the pinned bytes `measure4/summary.json` records C2
  `pass 29 / total 30` and `all_claim_checks_pass: false`; the one red is the retained frozen
  contradiction (`.ufo/waves/round-23/evidence/frozen-contradiction.json`, `CaseEscapedSpace`,
  sealed expected vs. the parent-ID rule) — untouched here, and to be preserved as-is through
  rollback. C1 at the same pin: original 26 `25/26 → 26/26`, `misleading_alias_runs 8 → 0`. This
  report asserts nothing about either beyond those recorded numbers.
- No privacy clearance, baseline acceptance, frontier closure, promotion or next-round scope is
  asserted. Four unallowlisted retention hits, permission control RED 11/12, two unknown
  dispositions and blocked baseline acceptance are unchanged.
- No sibling file was written; no `fstab`, unit, Snapper, superblock or quota command was read or
  run; no live quota read was performed; no `quotactl`/`ioctl`/`btrfs`/`xfs_quota`/`repquota`/
  `mount` call exists in the shipped path.

---

## 3. Affected axes

- **Adjacency (lane score 6, held)** — improved by A2/S1+S2: mori's own cleanup-ownership cell
  currently asserts a sibling scope that the sibling's pinned bytes do not contain, and the
  reclamation half of a runway pressure finding is not stated as a routed question (the proposal
  step is unnamed, and the link between "other lanes' residue" and "operator deletes" appears in
  no mori document). Both are in-lane ownership statements, fixable without a sibling write.
- **Calibration (C1, held 5)** — **untouched by design**: no key, value, exit code, finding id,
  schema or source byte is in scope of this move.
- **Coverage (C2, held 6)** — **untouched by design**: no case, oracle, frozen byte or production
  byte is in scope; the finding is about the *ownership statement* around the surface, not the
  surface.
- **Freshness/provenance** — mildly improved: the S1 repair re-points a mori citation at the
  sibling's current bytes instead of a 2026-10-18 historical quote.

---

## 4. Proposed move (one, bounded)

**Complete the cleanup-owner half of mori's runway boundary, in one mori-side documentation
commit, sequenced after the C2 rollback.**

Land exactly this, in `mori-shokunin/SKILL.md` and `mori-shokunin/PROVINCE.md` only:

1. **`SKILL.md` tier-1 routing table (`:350-353`)** — add one tier-1 entry for the cleanup
   domain, scoped to souji's *current* declared surface, e.g. a row reading
   `souji` (own-uid scratch residue; receipt-gated removal-list **proposals** for operator
   approval; never live lane work products) — with the tier-2 `operator` row left exactly as it is
   (it already carries "deletions"). This names the only cleanup-surface lane in the fleet
   **without transferring removal authority to it**: souji proposes, the operator deletes.
2. **`SKILL.md` runway row (`:19`)** — one added sentence in the "Never" cell's neighbourhood
   making the split explicit for a disk/quota pressure finding: mechanism configuration →
   `tsukuroi`/operator (`SKILL.md:601`); reclamation of the pressure → the operator (deletions,
   `SKILL.md:353`), with a receipt-gated own-uid residue proposal via souji where that applies and
   never on another lane's live work products; **mori never removes, resizes or reclaims
   anything**. No new surface, no probe, no capability claim, no frontier row.
3. **`PROVINCE.md:69`** — replace the superseded quotation and dead line-cite with souji's
   **current** text and range, i.e. quote `souji-shokunin/PROVINCE.md:50-52` ("mori-shokunin
   observes fleet and host health (liveness, kill/OOM, runway) and reports; souji lists only its
   own uid's scratch residue and routes liveness or resource findings to mori") and cite
   `../souji-shokunin/PROVINCE.md:8-17,50-52` — the same range mori's own r21 erratum
   (`:183-190`) already declares current. This resolves the internal contradiction between
   `:69` and `:183-190` rather than adding a new claim.

**Why this and not the void Core-advancing draft.** The withdrawn draft's subject is *whether a
capability moves to Core* — moot under Main's withdrawal, and it must not be landed. This move's
subject is *who may act on what a runway finding reports*, which is independent of C2's admission:
it is true whether the quota probe ships or is rolled back, because it is grounded in
`SKILL.md:19` (runway surface), `SKILL.md:350-353` (the two-tier routing table),
`corpus/knowledge/audit-r11.md:216` (D21: "operator/tsukuroi diagnose quota if operationally
relevant; no audit cleanup/remediation") and the two sibling provinces' own current bytes. It
needs no C2 result, no capability claim and no frontier change.

**Compatible synthesis across the round's own reports.** `ConnTsukuroi` established that
tsukuroi owns the host mount/unit and Snapper surfaces and that no tsukuroi quota surface exists
(0 hits) — the mechanism leg is therefore closed and needs no text. `ConnSoujiKama` established
souji's cleanup ground and that the historical EDQUOT class was residue-driven, and it recorded
that `QUOTA_DISABLED` coexisted with a 100 %-full `/tmp`. `CriticScopeProvince` ruled the input
list must be a *province* fence, not only an implementation detail. This move takes the ownership
conclusion of the first two and turns it into the one link the standing corpus is missing: the
corpus already says quota **diagnosis** goes to operator/tsukuroi and that mori does no cleanup
(`audit-r11.md:216`) — it never says who *proposes* the reclamation, and mori's one cell that
tries says it wrongly. The synthesis is deliberately **not** a Core movement and **not** a
quota-surface claim; it is a statement of the existing boundary, correct on both sides of C2's
withdrawal.

**Interaction with the C2-withdrawal disposition (read, not modified).**
`.ufo/waves/round-23/rejected/frontier-disposition.txt` (the replacement draft, 172 lines) is the
authoritative *replacement* for the void Core-advancing draft; it contains **no** `souji`,
`cleanup`, `reclaim` or `residue` text at all (verified: 0 matches), and it states "Adjacency is
unchanged: quota configuration and diagnosis stay tsukuroi/operator's". So the mechanism half of
this review is already carried by that draft, and this report adds only the **cleanup** half,
which no round document states. The two do not conflict: that draft's rules forbid editing the
`Core` list, the `Owns` clause and the FR2 row, and this move touches none of them; item 1 adds
one tier-1 routing-table row, item 2 adds one sentence to the runway row, item 3 replaces one
stale cell. If L1 prefers a strictly append-only landing for `PROVINCE.md`, item 3 may instead be
delivered as an appended erratum line next to `:183-190` (which already states the correct souji
scope) — the defect is the stale cell, and either form removes it.

---

## 5. Risks

1. **Over-reach into cleanup authority.** A tier-1 souji row could read as "souji cleans up"
   rather than "souji's surface is own-uid, receipt-gated, list/proposal-only". Mitigate by
   keeping souji's own two qualifiers verbatim ("own uid", "removal-list proposals for operator
   approval") and by leaving tier 2 `operator` (deletions) as the only actor.
2. **Reading the move as a C2 re-admission.** It adds no probe, no command, no capability, no
   frontier row and no `QUOTA_*` verdict; the sentence is a routing rule with a `→` owner. Keep it
   free of the words "Core", "advanced", "admitted", "FR2 advance".
3. **Editing the same files as the C2 rollback.** Sequence strictly after the rollback, in one
   mori-side commit, and land it *after* the pinned readers settle so the reviewed bytes are the
   ones rolled back. If the rollback removes `SKILL.md`'s Round-23 quota paragraph, items 1-2
   still stand alone: they do not depend on any C2 byte.
4. **Cross-lane write.** Only mori's own `PROVINCE.md` and `SKILL.md` are edited. No souji or
   tsukuroi file is touched; souji's current text is *quoted and cited*, never rewritten, and the
   citation is re-verified at souji's HEAD at landing time (souji is mid-round; its province has
   already moved once this round, `42d9ff3`).
5. **Weakening the tsukuroi fence.** The new text must not loosen `SKILL.md:601-605` or the
   note's Ownership fence. The mechanism half must keep pointing at tsukuroi/operator.
6. **No settlement before rollback.** This report does not authorise rollback; it is one pinned
   reader's settlement input.

---

## 6. Verification (owner: L1/parent — this seat ran none of it)

- `grep -c souji mori-shokunin/SKILL.md` → **0** before, ≥1 after (the tier-1 row + the runway
  sentence).
- `grep -n "acts on artifacts" mori-shokunin/PROVINCE.md` → 1 before (`:69`), **0** after.
- `grep -n "souji-shokunin/PROVINCE.md:40-41" mori-shokunin/PROVINCE.md` → 1 before, **0** after;
  the replacement cites `8-17,50-52`, the range mori's own `:183-190` already declares current.
- `git -C souji-shokunin show 473e98a:PROVINCE.md | sed -n '50,52p'` → still the current
  adjacency wording at landing (re-verify: souji may have moved again).
- `git -C souji-shokunin show 473e98a:PROVINCE.md | grep -c "acts on artifacts"` → 0 (the quoted
  sentence is genuinely superseded, not merely relocated).
- `grep -n "souji" mori-shokunin/SKILL.md` → the only occurrences must carry souji's own-uid and
  receipt qualifiers; `grep -n "tsukuroi" mori-shokunin/SKILL.md` → mechanism half unchanged
  (`:601-605` byte-identical).
- `git diff --stat <base> <landed> -- tools/ .ufo/waves/round-23/frozen/ .ufo/waves/round-23/oracle-quota.py
  .ufo/waves/round-23/oracle-rename.py` → **empty** (no production, frozen or oracle byte moves).
- `grep -n "QUOTA_\|FR2" mori-shokunin/SKILL.md` → no new capability/verdict token introduced by
  the landing text.
- `git -C mori-shokunin diff --numstat <base> <landed> -- PROVINCE.md SKILL.md` → the only changed
  files are mori's own two; no sibling repo shows a diff.

---

## 7. Compliance

- **Writes:** this report only. No source, expectation, oracle, case, frozen file, sibling file,
  lane index, jj ref or git object was created, edited or deleted; no `git add/commit/push`, no
  mutating `jj`.
- **Reads:** read-only `git show/log/status/ls-tree/cat-file/merge-base/diff` plus file reads.
  No live quota read, no `quotactl`/`ioctl`/`btrfs`/`xfs_quota`/`repquota`/`mount`, no
  `fstab`/unit/Snapper/superblock read, no journalctl, no process/session probe, no credential or
  `agent.db` read, no session transcript read.
- **Builds/tests/gates/selftests:** none run (not authorised for this item). The shipped tool's
  own `--selftest` was not invoked.
- **Installs/updates:** **none** — no pacman, uv, npm, cargo or release-binary transaction was
  performed, so no tool/version/channel to record; the host-wide pacman pause was untouched.
- **Scratch:** none created; no `/tmp` use, no background jobs, no delegation, no subagents.
- **Scope discipline:** the void Core-advancing province draft was read only to establish that
  it is void and is **not** proposed for landing; this report proposes no Core movement, no
  frontier closure, no remediation, no configuration change and no next-round scope, and claims
  no blanket pass.
