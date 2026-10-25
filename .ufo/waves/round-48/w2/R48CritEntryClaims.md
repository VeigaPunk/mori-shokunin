# R48CritEntryClaims — adversarial read of the 15 claim rows (mori round 48, wave 2)

Seat: R48CritEntryClaims. Lane: mori-shokunin. Leaf seat, no subagent dispatched, no labrat used.
Attacked: the 15 claim cells of `corpus/knowledge/quota-observability-r48.md` at the landed tip
`e4dfff32d4f97c7ef250e9a7538fa75d4f284492`, each against (a) its own quote and (b) the page text the quote
came from; plus every factual sentence in §Boundaries and §Probe shape and the entry's title.

**Verdict: BREAKS (class: overclaim from a scoped exemption to a universal).** One row — row 5 — states a
fact the page falsifies with its own project-quota text; a root-owned workload *can* hit a quota. Two more
rows state more than their page: row 10 keeps one half of a two-part `ESRCH` gloss and adds an unmarked
inference, and row 3 carries an unmarked inference and omits the mechanism (default quotas stored as ID 0's
limits) that changes how its "zero limit" reads. The other 12 rows hold against their quote and against the
surrounding page. In the prose, four defects: an unsourced factual claim (the Solaris `errno=49` sentence), a
mis-cited source (S480 cited for "its reporting tools are not [common]"), an unsourced cost claim ("a syscall
read per id is cheap"), and a **false locator** in the entry header and in `corpus/SOURCES.md:258`
(`§USER COMMANDS quot` — `quot` is in `§ADMINISTRATOR COMMANDS`). The counter cannot see any of these: it
checks that a quote is located, not what section it sits in or whether the claim follows (contract §C2 named
limit; `w1/CritEntryRisk.md` §1).

Impacted axes: **depth** (the row set is the entry's claim surface), secondarily **operability** (rows 5, 10
and 3 change what a probe author would report). Calibration and freshness are untouched: the C2 counter is
frozen and correct about what it measures, and every quote does locate.

## 1. Method

- Normalised all four committed copies with the counter's own `normalise` (`count-c2.py:59-62`: strip
  `<…>`, unescape entities, collapse whitespace), then read each page whole — not only the quote window —
  so "does the page elsewhere support it" is answered from the page, not from the quote.
- Re-located all 15 quotes and their token counts in the normalised copies (all 15 hit; 7–25 tokens).
- Checked each claim cell word by word against the located sentence and its section; recorded the weakest
  word that carries the overreach.
- Read `corpus/SOURCES.md:258-263` (S479-S484), the staged entry
  `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/quota-observability-r38.md` and the
  package root, to attribute the prose claims that have no lane row.

## 2. Row by row — weakest word, and whether the page supports it

Offsets are byte offsets in the normalised copy under `corpus/evidence/sources-r48/` (the counter's view).

| # | weakest word in the claim cell | beyond the quote? | page elsewhere supports it? | verdict |
|---|---|---|---|---|
| 1 | "separate states" (quote: "distinguishes between") | rewording only | yes — §QUOTA ADMINISTRATION item 3 ("it is possible to turn on/off limit enforcement any time quota accounting is turned on"; `uqnoenforce`) and `disable` ("Disables quota enforcement, while leaving quota accounting active.") | HOLDS |
| 2 | "chosen" at mount time | no | yes — item 3, plus `off` ("Quota can only be switched back on subsequently by unmounting and then mounting again."); item 4 (`rootflags=`) is still mount time | HOLDS |
| 3 | "**every** user" (drops the accounting-on precondition) and the whole "so a zero limit and a zero usage are different things" clause | second clause: **yes, unmarked inference** | first clause: item 9 + item 8 ("keep quota accounting on the superuser"); second clause: not stated — and §Default Quotas ("These limits are stored and displayed as ID 0's limits, although they do not actually limit ID 0", offset 6144) makes a displayed `0` mean *default quota*, not *no limit* | PARTIAL (see §3.3) |
| 4 | "is still" (quote: "can be used as") | modal strengthening | yes, provided accounting is on — the page's phrase is unconditional in §QUOTA OVERVIEW (offset 3306) | HOLDS (precondition unstated) |
| 5 | "**cannot** hit a quota" | **yes — and the page contradicts it** | **no — the page's project-quota section falsifies it** | **BREAKS** (see §3.1) |
| 6 | "sees" / "at the hard limit" | no (near-verbatim, offset 4072) | yes; §CAVEATS (offset 18587) only adds the converse ("enforcement can thus sometimes happen in situations where the user is under quota") — it does not weaken this row | HOLDS (entry omits the caveat; see §4) |
| 7 | "not a one-shot probe" | yes — cost conclusion, unmarked inference | partly: "it may also take a long time" is the page's own hedge, but the same sentence also says `quot` uses bulkstat "to **quickly** scan an entire filesystem" (offset 14807) — the page carries both | HOLDS with unmarked inference |
| 8 | "are" (quote: "can be used to set") | modal strengthening | yes — §DESCRIPTION, quote at offset 899; "can be set for each filesystem" at offset 1088 supports "on one filesystem" | HOLDS |
| 9 | "After the grace period" | no — "after this" refers to "more than grace period duration (one week by default) at a time" | yes — and S479 agrees ("If the timer pops … treated as if the hard limit has been reached") | HOLDS |
| 10 | "**means** quotas are not turned on" and "which is **not the same** observation as a usage of zero" | first clause: keeps half the quote; second clause: **not on the page at all** | no — the page's own first sentence is "No disk quota is found for the indicated user." (offset 3524), a per-id absence; nothing on the page compares `ESRCH` with a zero reading | BREAK-lite (see §3.2) |
| 11 | "by mount point" | narrows the interface | partly — §NOTES says "works on the mount point", but §DESCRIPTION says the fd "referring to a file or directory on the filesystem being manipulated"; the "no block device" half is supported ("avoids this limitation", tmpfs) | HOLDS (imprecise: the interface is an fd, not the mount point) |
| 12 | "The generic Linux ABI header" | no | yes — `include/uapi/asm-generic/errno.h:107` (`#define EDQUOT 122`), verified in the committed copy; §Boundaries supplies the arch variance (S483 1133, S484 69, both line pins verified) | HOLDS |
| 13 | "**prints**" | yes — modal | no: the page presents the line as 预期返回 ("the expected return is as follows"), a documented expectation, not an observed run | HOLDS with overstatement (documented expectation, not observation) |
| 14 | "is a feature of a subdirectory mounted by `subPath`" | no | yes — and the page's 使用限制 narrows it further (only NFS 通用型 NAS, only dynamic volumes via `subpath`; static volumes and `sharepath`/`filesystem` mounts excluded) | HOLDS (narrowing omitted) |
| 15 | "a separate console page" | no | yes — NAS 控制台 → 文件系统列表 → 配额管理 → 管理配额 | HOLDS |

## 3. The three defects

### 3.1 Row 5 — BREAKS: "so a root-owned workload cannot hit a quota"

Exact claim cell:

> `Limits are never enforced on the superuser or on group and project ID zero, so a root-owned workload cannot hit a quota.`

The quote ("limits are never enforced on the superuser (nor are they enforced for group and project ID
zero)", offset 9294; the ID-zero parenthetical begins at 9338) supports the first clause. The "so …" clause is an inference the page does not make,
and the page's own text supplies the counterexample:

1. The exemption is scoped to **IDs**, not to writers: the same sentence exempts only "group and project ID
   zero".
2. §DIRECTORY TREE QUOTA: "Once this has been done, new files created in the tree will automatically be
   accounted to the tree based on their project identifier." (offset 16368).
3. §EXAMPLES sets such a limit: `# xfs_quota -x -c 'limit -p bhard=1g logfiles' /var`.

A root-owned workload creating files inside a project-quota'd tree is accounted to that tree's **nonzero**
project ID, whose hard limit *is* enforced; the write fails with EDQUOT exactly as row 6 describes. So a
root-owned workload can hit a quota, on the page's own three sentences. The page also never states which ID a
write is charged to for user or group quotas, so the row's inference has no on-page basis even in the
user-quota case. The row is also unmarked, while the entry does mark a weaker inference in §Probe shape —
inconsistent marking. §Boundaries' guard ("The root and ID-zero exemption is stated for XFS (S479); this entry
does not extend it to other filesystems") scopes the exemption by *filesystem*, not by *ID*, so it does not
rescue the row.

Impact: a mori probe author acting on this row would treat a root process's `Disk quota exceeded` as
impossible — i.e. suppress the one observation the lane exists to report.

Smallest safe correction (keep the row, drop the overreach):

> `Limits are never enforced on the superuser or on group and project ID zero (S479); a limit on any other id, or on a nonzero project id, is enforced for files accounted to it — §DIRECTORY TREE QUOTA accounts files created in a project tree to the tree's project id, and §EXAMPLES sets `limit -p bhard=1g`.`

If the entry wants the workload sentence at all it must be marked `[INFERENCE]` and say what it assumes
(writes charged to user ID 0, no project quota on the target tree).

### 3.2 Row 10 — BREAK-lite: `ESRCH` narrowed, then hardened by the probe shape

Exact claim cell:

> `` `ESRCH` from the quota syscall means quotas are not turned on, which is not the same observation as a usage of zero. ``

The quoted sentence is two: "No disk quota is found for the indicated user. Quotas have not been turned on for
this filesystem." The claim keeps only the second and asserts it as the errno's *meaning*. The page's first
sentence is a per-id absence, which is not the same statement as a filesystem-level "not turned on", and the
page gives no precedence between them. The second clause ("not the same observation as a usage of zero") is
not on the page at all; it is an inference from the return-value section ("On success, 0 is returned; on
error, -1 is returned"). §Probe shape then hardens it — "treat `ESRCH` as not turned on, **never** as zero" —
which turns the per-id half into a filesystem-level verdict. No local source settles which half applies when
(the lane holds no `fs/quota/dquot.c` copy; S089 has a row, not a committed copy), so the page is the whole
evidence and it supports the narrower reading only.

Smallest safe correction: state both sentences and mark the comparison as inference, e.g. "`ESRCH` carries
two statements on the page — no quota found for this id, and quotas not turned on for this filesystem (S480);
it is an error return, so it is not a successful read of zeros `[INFERENCE]`."

### 3.3 Row 3 — unmarked inference plus a missing mechanism

Exact claim cell:

> `XFS accounts usage for every user, including users that have no limit set, so a zero limit and a zero usage are different things.`

- "for every user" is unconditional; the page makes accounting conditional on the mount (row 2's own quote).
- "so a zero limit and a zero usage are different things" is not stated anywhere on the page — it is an
  inference (a fair one: the page lists "current usage, soft limit, hard limit, and time limit" as four
  numbers).
- The entry never mentions default quotas (`grep -ci 'default quota'` on the entry → 0). The page's §Default
  Quotas says the subsystem "allows a default quota to be enforced for any user, group or project which does
  not have a quota limit explicitly set. These limits are stored in and displayed as ID 0's limits, although
  they do not actually limit ID 0." A probe author reading "a zero limit" therefore has a live ambiguity the
  entry does not resolve: a `0` in the limit field of ID 0 is the default-quota store, and a user with no
  explicit limit is governed by that default. This is the one place where a *missing* page mechanism matters
  more than the wording.

Smallest safe correction: mark the second clause `[INFERENCE]` and add one clause naming the default-quota
store, or drop the clause.

## 4. §Boundaries prose — each factual sentence, marked

| # | exact text | marking |
|---|---|---|
| B1 | "mori observes and reports quota state; it never sets a limit, starts accounting, changes a grace period or runs a repair." | lane policy (scope), not a source fact — fine as written, but it is policy, not evidence |
| B2 | "No quota command was run against this host for this entry." | process claim, self-attested — **UNVERIFIED** by me (no host command history read) |
| B3 | "122 is the generic header's value (S481)." | **sourced** — verified `errno.h:107` in the committed copy |
| B4 | "Linux v7.2 `arch/mips` defines `EDQUOT` as 1133 (S483, `#define EDQUOT 1133 /* Quota exceeded */`, line 131)" | **sourced** — line 131 verified in the committed copy |
| B5 | "and `arch/sparc` as 69 (S484, line 43)" | **sourced** — line 43 verified |
| B6 | "A probe matches the platform's own constant, or the symbolic name, never a copied number." | advice, follows from B3-B5 — fine |
| B7 | "A Japanese vendor document that quotes `errno=49` describes Solaris and stays rejected for this lane." | **unsupported** — see §5.1 |
| B8 | "`xfs_quota(8)` is XFS" | **sourced** — S479 NAME ("manage use of quota on XFS filesystems") |
| B9 | "the `quotactl(2)` syscall is common to quota-supporting Linux filesystems" | **[INFERENCE]**, unmarked — S480 never says "common to quota-supporting filesystems"; it is inferred from the generic `Q_*` ops plus the XFS/XQM bypass |
| B10 | "but its reporting tools are not (S480)" | **unsupported by the cited source** — see §5.2 |
| B11 | "The root and ID-zero exemption is stated for XFS (S479); this entry does not extend it to other filesystems." | **sourced** + scope; note it scopes by filesystem and does not cover row 5's ID/workload leap (§3.1) |
| B12 | "S482 documents one vendor's NAS directory quota. It is a comparison shape … not authority for mori's own alert thresholds, which stay local and labelled (FR8)." | scope statement + lane-local label (FR8) — fine |
| B13 | "The page embeds its body twice (rendered text and JSON), so a byte-identical re-fetch is not expected" | **sourced by direct inspection** — two occurrences of the body strings in the copy (escaped JSON at offset 26584, rendered HTML at 81419) |
| B14 | "the quotes are stable, the file hash is not" | self-attested recheck claim — **UNVERIFIED** by me (no re-fetch made) |
| B15 | "the PDF answered HTTP 403 to the freeze fetch, and the claims stay out until a lane row is opened for them" | **sourced** against the lesson's Gate record (freeze 403; `w1/ScoutStagedQuota.md` later 200 — the entry's "to the freeze fetch" is precise and does not claim unreachability today) |

## 5. The four prose defects

### 5.1 Unsourced: the Solaris sentence

> "A Japanese vendor document that quotes `errno=49` describes Solaris and stays rejected for this lane."

Nothing in this entry sources "describes Solaris": the four claim sources are S479-S482 (man pages, errno.h,
the Aliyun page) and the two boundary rows S483/S484 are Linux arch headers; `grep -cE 'Solaris|errno=49'
corpus/SOURCES.md` → 0 (exit 1). The package's staged entry asserts the same thing and points at
`REJECTIONS.md` A1, but `/home/vgpnk/Projects/shokuknow/merge/mori/REJECTIONS.md` does not exist (exit 2), and
no other package file mentions Solaris. The fact is true of Solaris, but in this entry it is an unsourced
assertion inside a Boundaries list whose other sentences are all cited. Smallest correction: mark it
`[INFERENCE]`/drop the identification and keep only the decision ("a document quoting a different number for
the same symbolic name describes a different platform, so it is rejected"), which B3-B5 do support.

### 5.2 Mis-cited: "but its reporting tools are not (S480)"

S480 (quotactl.2) lists `quota(1)`, `quotacheck(8)`, `quotaon(8)` in §SEE ALSO and the referrer list adds
`repquota(8)`, `setquota(8)` — it says nothing about whether those tools are filesystem-specific. The
sentence was inherited from the staged entry, where it read "ext4 uses `quota(1)` / `repquota(1)` instead"
with no lane row either. The nearest on-page support is a *different* source: S479 item 1 ("The quotacheck
command has no effect on XFS filesystems"). Smallest correction: cite S479 for the tool-scope half, or mark
it `[INFERENCE]` and drop the "(S480)".

### 5.3 Unsourced cost claim in §Probe shape

> "price the reading: a syscall read per id is cheap, `quot` scans the filesystem (S479)"

The `quot` half is sourced (offset 14927). "a syscall read per id is cheap" is sourced by nothing in the
entry — no page in the copy set carries any cost or latency statement. It is the kind of number-free claim
that still steers a probe author's design. Mark `[INFERENCE]` or drop.

### 5.4 False locator in the entry header and in the registry row

The entry's first source line and `corpus/SOURCES.md:258` both place `quot` in `§USER COMMANDS`:

> "§QUOTA OVERVIEW, §QUOTA ADMINISTRATION items 3, 8, 9, §USER COMMANDS `quot`"  (entry)
> "… QUOTA ADMINISTRATION items 3, 8 and 9, USER COMMANDS quot; …"  (SOURCES.md:258)

`quot` is in `§ADMINISTRATOR COMMANDS`: normalised offsets — `USER COMMANDS top` 6245, `ADMINISTRATOR
COMMANDS top` 9790, `quot [ -g | -p | -u ]` 14695, `DIRECTORY TREE QUOTA top` 15676; the `quot` entry sits
between `restore` and `project`, after the administrator heading. The quote is still located (so C2 stays
met), which is exactly the blind spot: the counter checks the quote, not the locator. Class: false
provenance. Smallest correction: change `USER COMMANDS` to `ADMINISTRATOR COMMANDS` in the entry header and
in the S479 row's locator cell.

Two smaller prose notes, same class, low severity:
- "The lane held the kernel's quota flags (S078, S084, S088, S089) and the mount-option vocabulary (S077,
  S082, S085)" — S085 is `fs/proc_namespace.c` ("per-mount field assembly and path escaping"), code, not
  vocabulary; S084 ("tmpfs quota options … tmpfs quota flags") is the vocabulary-shaped row. The IDs all
  exist (verified), only the two buckets are swapped.
- "no row on the user-space reporting surface" — wider than its receipt (a four-token grep → 0). A user-space
  disk-usage reporting row does exist: `S470 journalctl(1) --disk-usage`. It is journal usage, not filesystem
  quota, so the sentence survives only under an unstated "for filesystem quota" qualifier.

## 6. Title and the `[INFERENCE]` block

- Title: "…; `df` cannot see it" — **unmarked inference**. The page says `free` "Reports filesystem usage,
  much like the df(1) utility" and that `report`/`quota` carry the per-id view; no source states that `df`
  cannot show quota state. Mark it, or say "`df`-equivalent output shows capacity, not per-id quota".
- Title: "Quota exhaustion is a **per-id** state" — universal that one of its own sources does not fit:
  S482's directory quota is scoped to a *subdirectory path* (row 14), not to an id. §Boundaries scopes S482 as
  another product's semantics, so the title survives only by that scope; as written it is wider than its
  evidence.
- `[INFERENCE]` block: "… has a per-id filesystem limit in play, **not a full device**". The block is
  correctly labelled, but its stated justification ("the sources say the string comes from the failing write
  and the state lives in a separate report") supports only the first half. No copy says what a full device
  reports (ENOSPC appears nowhere in the four copies), so "not a full device" is an inference the label does
  not cover. The `[INFERENCE]` is otherwise sound; S479's §CAVEATS (enforcement can fire while under quota)
  is consistent with "a limit in play" and should be named if the block is kept.

## 7. What this review does not cover (limits of the seat)

- I did not re-fetch any page: "the quotes are stable" (B14) and the live page state are **UNVERIFIED** here;
  the copies are the evidence, dated 2026-10-25.
- I read no host mount state and ran no quota command (read-only lane), so nothing here measures the fleet.
- I did not run `count-c1.py`/`count-c2.py`; the C2 predicate is not in question — all 15 quotes locate in
  the committed copies (probe below), which is all the counter claims.
- No kernel source copy exists in the lane for `ESRCH` semantics, so §3.2 stays at "the page supports the
  narrower reading", not "the kernel does X".
- This is a dispatched seat, not an independent judge.

## 8. Evidence log (observed commands, output, exit)

All lane commands with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48CritEntryClaims`.
No file under `tools/`, `corpus/`, `.ufo/waves/round-48` frozen paths, `SKILL.md`, `SOURCES.md`, `LOG.md`,
`SCORECARD.md` was written; the only lane writes are this report and
`.scratch/r48w2-R48CritEntryClaims/`. `grep -c ENOSPC` / `grep -c 'No space left'` over the six normalised
copies → 0 each (the §6 "not a full device" note).

1. `python3 .scratch/r48w2-R48CritEntryClaims/norm.py` → `xfs_quota.8.html 21066 / quotactl.2.html 7203 /
   errno.h 5727 / aliyun-nas-quota.html 18090 / arch-mips-errno.h 5866 / arch-sparc-errno.h 5598` chars, exit 0.
2. Quote-location probe (replicates `count-c2.py:59-62`) → all 15 rows: `pos` ≥ 0, `words` 7–25
   (e.g. `row05 S479 words=25 pos=4072`, `row11 S481 words= 7 pos=5021`, `row14 S482 words= 7 pos=4752`), exit 0.
   Row 1 (the row my first slice skipped) re-checked: `XFS distinguishes between quota accounting and limit
   enforcement.` at offset 8137.
3. `git show e4dfff32:corpus/evidence/sources-r48/errno.h | sed -n '100,112p'` → `EDQUOT 122` is line 107;
   `arch-mips-errno.h:131` → `#define EDQUOT 1133`; `arch-sparc-errno.h:43` → `#define EDQUOT 69`, exit 0.
4. `git show e5dbac05:corpus/SOURCES.md | grep -cE 'xfs_quota|quotactl|EDQUOT|repquota'` → `0`, grep exit 1
   (the entry's "→ 0" is accurate).
5. `git show e5dbac05:corpus/SOURCES.md | grep -nE '^ {0,3}\| *S0(77|78|82|84|85|88|89) *\|'` → rows 83, 84, 88,
   90, 91, 94, 95 printed; all seven IDs exist.
6. `sed -n '94,98p;166,170p' corpus/knowledge/audit-r11.md` → line 96 carries
   `printf: write error: Disk quota exceeded`; line 168 is F13, same class; `sed -n '18,22p'
   corpus/knowledge/seat-terminal-status-r17.md` → the `dead_quota` row maps "Z.AI type 1113/1308 or quota
   token", exit 0. Both "What the lane held before" citations are accurate.
7. Section offsets in the normalised `xfs_quota.8.html` → `USER COMMANDS top` 6245, `ADMINISTRATOR COMMANDS top`
   9790, `quot [ -g | -p | -u ]` 14695, `DIRECTORY TREE QUOTA top` 15676 (the §5.4 finding), exit 0.
8. Page sentences located for the findings: item-8 exemption 9294 (ID-zero parenthetical 9338); project-tree
   accounting 16368; bulkstat sentence 14807; §CAVEATS reservation 18587; §Default Quotas 6001/6144; item-3
   enforcement toggle 8291; `limit -p bhard=1g logfiles` example 18001.
9. `grep -cE 'Solaris|errno=49' corpus/SOURCES.md` → `0`, grep exit 1; `ls
   /home/vgpnk/Projects/shokuknow/merge/mori/REJECTIONS.md` → "No such file or directory", exit 2; `find . -iname
   "*REJECT*"` in the package → no output.
10. Aliyun duplicate-body check: `'dd: closing output file' count= 2` in the normalised copy; raw offsets 26584
    (escaped JSON) and 81419 (rendered HTML) — B13 verified. `lastModifiedTime: 1791872777000` →
    2026-10-13T06:26:17Z, matching the entry's "page meta last-modified 2026-10-13".
11. `git show e5dbac05:corpus/SOURCES.md | grep -nE 'disk usage|df\(1\)|du\(1\)|quota-tools'` → one line,
    `S470 journalctl(1) --disk-usage`, exit 0 (the §5.4 negative-claim note).
12. `grep -ci` on the entry for `default quota`, `ID 0`, `bulkstat`, `CAVEATS`, `reservation` → 0 each; for
    `project` → 2, `quotactl_fd` → 3, `ESRCH` → 3.
13. `git rev-parse HEAD` in the lane → `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`; `git status --porcelain`
    listed only untracked (`??`) entries — other seats' `.scratch/` and `.ufo/waves/round-40/scratch/` dirs —
    and no tracked file in a modified state.
14. Tooling: nothing installed or updated (operator RULES.md read; pacman untouched).
15. `find . -name "dquot*" -not -path "./.git/*"` in the lane → no `dquot` copy (the walk reported one broken
    symlink inside `.scratch/pin-check-0phxs6op/`, `os error 2`; no file matched), so §3.2's "no local source
    settles which half applies" is grounded. `git status --porcelain | grep -v '^?? .scratch/'` → only
    untracked `??` entries (this report and other seats' scratch), no tracked file modified by me.
