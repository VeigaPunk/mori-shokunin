# SrcBinaryOwnWork — the installed omp binary as an own-work SOURCES row (C2)

Seat: `MoriR25.SrcBinaryOwnWork` (scribe, leaf). Wave: round-25 / wave 1.
Claim served: **C2 (coverage, new PROVINCE ground)** — the harness background-job runway cap.
Surface owned by this seat: **one** `own-work` SOURCES.md row for the installed binary
`~/.local/bin/omp` as a primary local artifact — tier and `own-work` conventions per
`/home/vgpnk/Projects/shokunin/CORPUS.md` (SOURCES section) and the existing own-work rows in
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`.

**No lane file was edited by this seat.** `corpus/SOURCES.md` is untouched — `git status --porcelain
corpus/SOURCES.md` prints nothing (measured at the current tip `042d75b`; the row in it was landed
by the L1 in `90ed9b7`, not by this seat). `omp` was never executed. The binary was read only as
bytes (`mmap`, `sha256sum`, `stat`).

---

## 1. What was done (executed, in order)

### 1.1 Conventions read first

- `/home/vgpnk/Projects/shokunin/CORPUS.md` — SOURCES section (frozen contract v1): the 11-cell
  registry shape, `kind` enum (includes `own-work`), tier A/B/C definitions, rule 1
  ("A row is a claim. Write it only after opening the source in the round that writes the row"),
  rule 2 (append-only), and the census command set.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:40` — the lane's only existing
  own-work row (**S034**, `Mori live roster census`), whose `source` cell is
  `` `corpus/evidence/roster-r12-20261019T220912Z-live.log` (command: `MORI_SHOKUNIN_ROOT=… bash tools/mori-census.sh`) ``.
  That is the convention this row follows: **an own-work row's locator is a repo path plus the
  command that reproduces it**, never a bare filesystem path and never a URL.
- Fleet-wide own-work rows cross-checked for shape (`grep -rn "own-work" */corpus/SOURCES.md`):
  `audio-shokunin` S012, `chousa-shokunin` S001/S034–S036/S040–S043/S045, `game-dev-2d-shokunin`
  S028–S030, `kaidoku-shokunin` S039/S053/S055/S057/S060/S061/S063/S067/S072,
  `kake-shokunin` S014/S019 — all `kind = own-work`, all `tier = A`, all with a repo path or
  command in the `source` cell.

### 1.2 Binary identity (read-only)

```
stat -c '%s bytes' ~/.local/bin/omp        → 256702432 bytes
sha256sum ~/.local/bin/omp                 → 85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4
file ~/.local/bin/omp                       → ELF 64-bit LSB executable, x86-64, dynamically linked, not stripped
readlink -f "$(command -v omp)"            → /home/vgpnk/.local/bin/omp   (regular file, not a symlink)
stat -c '%y %s'                             → 2026-10-21 20:37:24.615549837 -0300 256702432
```

`command -v omp` → `/home/vgpnk/.local/bin/omp`; `os.path.realpath(shutil.which("omp"))` →
the same path, so the tool's `--binary` default resolves to the bytes measured here.

### 1.3 The two located quotes (byte offsets are decimal, from byte 0 of the file)

Located with a Python `mmap` + `re` scan over the whole 256,702,432-byte file. Both patterns are
the contract's own regexes (C2 rules 2 and 3), so the row's quotes and the tool's parser agree by
construction.

**Clamp** — pattern
`maxRunningJobs:\s*\(\)\s*=>\s*Math\.min\(\s*(\d+)\s*,\s*[\w$]+\.get\([\w$]+\)\s*\)`
→ **1 match, value `100`, byte offset 164406766**.

```
    maxRunningJobs: () => Math.min(100, XPe.get(R))
```

Owning module banner `// packages/coding-agent/src/sdk.ts` at byte 164380488; the enclosing
construction is `const Ui = !u.parentTaskPrefix ? new Xm({ … }) : undefined;`.
Word count of the quote: **5** (`maxRunningJobs: () => Math.min(100, XPe.get(R))`).

**Setting default** — pattern `id:\s*"async\.maxJobs",[^}]{0,300}?default:\s*(\d+)`
→ **1 match, value `100`, byte offset 155231590**.

```
var XPe = h({
  id: "async.maxJobs",
  protocolDefault: ["rpc"],
  type: "number",
  default: 100
});
```

Owning module banner `// packages/coding-agent/src/tools/settings.ts` at byte 155206756.
Word count of the quote: **8**.

**Version** — `--user-agent=omp/18.12.6` at byte **256648593**; the bundled manifest line
`version: "18.12.6"` at byte **151991030** (inside the `// packages/coding-agent/package.json`
banner at 151990942, manifest `name: "@oh-my-pi/pi-coding-agent"` at 151990993); the in-file
changelog heading `## [18.12.6] - 2026-10-21` at byte 252999412. `18.12.6` occurs 9 times in the
file; `omp/18.12.6` occurs once.

**Uniqueness checks that make the quotes safe to cite** (measured):

- `XPe.get(` occurs exactly **once** in the whole file (byte 164406802) — the accessor the clamp
  reads is the same binding the settings schema declares (`var XPe = h({ id: "async.maxJobs", … })`
  at 155231574; `XPe` is exported as `cfgAsyncMaxJobs` at 171101808).
- The literal `async.maxJobs` occurs **twice**: 96085908 (a settings-UI string table, no
  `id: "` prefix — it cannot satisfy the rule-3 regex) and 155231590 (the definition). The
  contract regex therefore cannot false-positive on the string table.
- `Math.min(100,` alone occurs 16 times in the file (progress bars, quota percentages, …); only
  the full rule-2 pattern is unique. A row that quoted the bare `Math.min(100,` would be
  unciteable; quoting the whole `maxRunningJobs: () => Math.min(100, XPe.get(R))` is exact.

### 1.4 Independent cross-checks (not needed for the row, recorded for the judge)

- The lane tool already landed in this round reads the same bytes and reports the same numbers:
  `python3 -I -B tools/mori-job-runway.py` prints `binary_sha256 85d9daf3…ccfa4`, `clamp
  {state: found, value: 100, sites: 1}`, `setting_default {state: found, value: 100, sites: 1}`,
  `configured {state: set, value: 200}`, `effective 100`, `verdict RUNWAY_CLAMPED`, exit **1**.
  `python3 -I -B tools/mori-job-runway.py --selftest` prints `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`,
  exit **0** (run for cross-reference only; the tool is another seat's surface).
- The installed file is byte-identical to the published release asset: GitHub API
  `repos/can1357/oh-my-pi/releases/420053191` (tag `v18.12.6`, published 2026-10-21T21:02:53Z)
  lists asset `omp-linux-x64`, size **256702432**, `digest
  sha256:85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`; the release's
  `SHA256SUMS.txt` (934 B, sha256 `72ebc3d92054d3a2e8edafc1acf593ea685e609672b031084459f525a2fc64e5`,
  fetched 2026-10-22) line 8 reads
  `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4  omp-linux-x64`.
  *This identity fact is provenance, not behaviour; it is deliberately kept **out** of the row's
  `teaches` cell (see §5).*

---

## 2. Drafted SOURCES.md row

Header shape checked against `corpus/SOURCES.md:5-6`
(`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`).
**Id: `S102`** — agreed in-channel with `MoriR25.UpstreamTagLocate` on 2026-10-22: that seat's
§6 draft of the same own-work binary row is superseded by this one, no second binary row is added,
and its upstream rows S099–S101 are unaffected. `S098` is `MoriR25.SrcJobManager`'s row;
`S103`+ are `MoriR25.SrcRejections`'. Next free id after the measured maximum `S097` was `S098`.

Draft row — insert **inside the `## Registry` table immediately after the `S097` row** (not at EOF;
EOF placement is validator error `E12`, measured — see §4):

```markdown
| S102 | Installed omp CLI binary — `~/.local/bin/omp` (read-only locator: `python3 -I -B -c "import mmap,re,os,hashlib;p=os.path.expanduser('~/.local/bin/omp');f=open(p,'rb');h=hashlib.sha256();[h.update(c) for c in iter(lambda: f.read(1<<20), b'')];f.seek(0);mm=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ);print('sha256',h.hexdigest(),'size',len(mm));[print(m.start(),mm[max(0,m.start()-30):m.end()+30].decode('utf-8','replace').replace(chr(10),' ')) for pat in (rb'maxRunningJobs:\s*\(\)\s*=>\s*Math\.min\(\s*(\d+)\s*,\s*[\w\$]+\.get\([\w\$]+\)\s*\)',rb'id:\s*\"async\.maxJobs\",[^\}]{0,300}?default:\s*(\d+)') for m in re.finditer(pat,mm)]"`; the same bytes are read by the lane tool `tools/mori-job-runway.py`, command `python3 -I -B tools/mori-job-runway.py --binary ~/.local/bin/omp`) | own-work | A | the compiled-in background-job clamp and the `async.maxJobs` schema default inside the omp build installed on this host, located at byte offsets in one digest; not upstream source semantics, not a live run, not a reading of the running-job count | byte 164406766: "maxRunningJobs: () => Math.min(100, XPe.get(R))" (5 words; owning module comment `// packages/coding-agent/src/sdk.ts` at byte 164380488); byte 155231590: "id: \"async.maxJobs\", protocolDefault: [\"rpc\"], type: \"number\", default: 100" (8 words; owning module comment `// packages/coding-agent/src/tools/settings.ts` at byte 155206756); version byte 256648593: "--user-agent=omp/18.12.6" and manifest byte 151991030: "version: \"18.12.6\""; sha256 85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4; size 256702432 bytes | The installed build clamps the harness background-job runway at 100 whatever `async.maxJobs` is set to, so a configured value above 100 cannot raise the cap | queued | 2026-10-22 | on-release | — |
```

### 2.1 The exact read-only command (copy-pasteable, verified verbatim)

```sh
python3 -I -B -c "import mmap,re,os,hashlib;p=os.path.expanduser('~/.local/bin/omp');f=open(p,'rb');h=hashlib.sha256();[h.update(c) for c in iter(lambda: f.read(1<<20), b'')];f.seek(0);mm=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ);print('sha256',h.hexdigest(),'size',len(mm));[print(m.start(),mm[max(0,m.start()-30):m.end()+30].decode('utf-8','replace').replace(chr(10),' ')) for pat in (rb'maxRunningJobs:\s*\(\)\s*=>\s*Math\.min\(\s*(\d+)\s*,\s*[\w\$]+\.get\([\w\$]+\)\s*\)',rb'id:\s*\"async\.maxJobs\",[^\}]{0,300}?default:\s*(\d+)') for m in re.finditer(pat,mm)]"
```

Observed output (run verbatim from a shell; exit **0**):

```
sha256 85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4 size 256702432
164406766 rentTaskPrefix ? new Xm({     maxRunningJobs: () => Math.min(100, XPe.get(R))   }) : undefined;   if (Ui) {
155231590 tion"   } }); var XPe = h({   id: "async.maxJobs",   protocolDefault: ["rpc"],   type: "number",   default: 100 }); var YPe = h({   id: "asyn
```

A second, equivalent locator (no `mmap`, plain `strings`/`grep`) also verified, for readers who
prefer it:

```sh
strings -a ~/.local/bin/omp | grep -n 'maxRunningJobs: () => Math.min(100, XPe.get(R))'    # → 1162764
strings -a ~/.local/bin/omp | grep -n -A3 'id: "async.maxJobs",'                             # → 903013-903016
strings -a ~/.local/bin/omp | grep -n -- '--user-agent=omp/18.12.6'                          # → 2443432
```

(The `strings` line numbers are stream line numbers, not byte offsets; the row cites byte offsets
because they are stable for this digest. Both locators agree on the content.)

**The command contains no `|` character** — required by CORPUS.md ("No `|` inside any cell") and
checked programmatically over all 11 cells of the draft row.

### 2.2 Cell-by-cell notes for the L1

| cell | value | why |
|---|---|---|
| id | `S102` | agreed with `MoriR25.UpstreamTagLocate` (§2 header); `S098` = `MoriR25.SrcJobManager`, `S099`–`S101` = upstream source/docs rows, `S103`+ = `MoriR25.SrcRejections`. |
| source | title — `~/.local/bin/omp` (read-only locator: `<command>`; same bytes read by `tools/mori-job-runway.py`) | own-work convention per S034: a repo path or a command, never a bare path. The repo path `tools/mori-job-runway.py` is the lane's own re-runnable reader of exactly these bytes; the inline `python3 -I -B -c` command is the standalone reproducer that needs no lane file. **Landing-order note (§2.4):** the tool clause is safe only if S102 lands at or after the tool's landing commit; the standalone command alone reproduces both quotes, so the L1 may drop the tool clause at no cost to the row's evidence. |
| kind | `own-work` | the row's source is a local artifact, not a URL. |
| tier | `A` | primary and authoritative **for this scope**: the bytes are the artifact itself, and the row is the lane's own re-runnable evidence for what this installed build contains. Tier is scoped, not global — the row's `scope` cell excludes upstream semantics. |
| scope | the compiled-in clamp and the `async.maxJobs` schema default inside the installed build, at byte offsets in one digest; **not** upstream source semantics, **not** a live run, **not** the running-job count | names its own exclusions so it cannot be widened into S098/S099/S100's territory or into live host state. |
| anchor | two byte offsets + owning module banners + two version byte offsets + sha256 + size | every element is a measured byte position or digest, not a paraphrase. A quote names its location (CORPUS.md rule). |
| teaches | the installed build clamps the runway at 100 whatever `async.maxJobs` is set to | one grounded learner benefit, phrased as build behaviour (from the bytes), not as a host observation. |
| status | `queued`, used-by `—` | `corpus/lessons/round-25.md` and `corpus/knowledge/harness-job-capacity-r25.md` **do not exist on disk yet** (measured: both `ls` fail). A `mined` row whose used-by path is missing is validator error `E11` (measured — §4). Flip condition below. |
| opened | `2026-10-22` | UTC date the binary was opened and quoted. |
| recheck | `on-release` | the row describes one build of one binary; it must be re-opened when omp moves off 18.12.6 (the binary is replaced on upgrade, so the digest and offsets change). |
| used-by | `—` | matches `queued`. |

**Flip condition (measured, §4).** If the L1 lands the knowledge entry
`corpus/knowledge/harness-job-capacity-r25.md` (the contract's C2 "Sourced" clause names it as the
citing file) **in the same commit** as the row, flip to `status = mined` and
`used-by = corpus/knowledge/harness-job-capacity-r25.md`; the validator is then clean (exit 0,
measured). If the row lands alone, keep `queued` / `—`; landing `mined` with the file absent is
`E11` (exit 1, measured). The contract's C2 "Sourced" clause says the knowledge entry cites "SOURCES.md
rows opened this round (upstream oh-my-pi source at the tag matching 18.12.6, plus the installed
binary as an own-work row)" — this row is that own-work row.

### 2.3 Landing outcome (measured after the L1 landed it)

The L1 landed this row in commit **`90ed9b7`** ("round-25: sources S098-S111 (7 admitted, 7
rejected) and knowledge entry harness-job-capacity-r25 (C2)"), together with the knowledge entry.
Measured at that landing and at the current tip (`HEAD` = `042d75b`):

- **The landed row is byte-for-byte this seat's `mined` draft.** Diffed cell-by-cell against the
  draft in §2: `identical = True` (13 cells, `kind=own-work`, `tier=A`, `status=mined`,
  `used-by=corpus/knowledge/harness-job-capacity-r25.md`).
- The row sits inside the `## Registry` table at `corpus/SOURCES.md:108`, immediately after
  `S101` and before `S103`; the registry now holds **111** rows, `S098`–`S111` included.
- **The `mined` flip is satisfied, not merely planned:** `corpus/knowledge/harness-job-capacity-r25.md`
  now exists (landed in the same commit) and cites the row — its `source:` prologue names
  "S102 (installed binary ~/.local/bin/omp, own-work: 256,702,432 bytes, sha256
  85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4, byte-identical to release asset
  omp-linux-x64 of tag v18.12.6)", and the body cites S102 at F1 (byte 155231590), F2/F3 (the
  clamp) and the error-text section.
- **Validator on the live lane file is clean:**
  `sources-census.sh validate --file corpus/SOURCES.md --today 2026-10-22` → `file ok`, exit **0**
  (no `E`/`W` line attributable to S102; the six pre-existing `W04` lines belong to S035/S037/
  S073/S074/S075/S076).
- The knowledge entry's S102 attribution matches this row's scope: it cites S102 for the
  **installed binary's** clamp site and setting default, and cites S099/S100/S101/S103 for the
  upstream source and prose. No upstream claim rests on this row.

One observation for the judge, recorded because it is a scope boundary the knowledge entry
respected: the knowledge entry's `source:` prologue attributes to S102 the byte-identity with
release asset `omp-linux-x64`. That identity was verified in §1.4 of this report (GitHub API
release `420053191` asset digest + `SHA256SUMS.txt` line 8, both equal to the local sha256), but
this seat's row deliberately keeps it **out** of the `teaches` cell, which stays a behaviour claim.
The attribution is therefore supported, and it is supported by §1.4 rather than by the row's
`teaches` text — no row asserts it as taught content.

### 2.4 Landing order for the tool clause (raised by the upstream seat; resolved here)

`MoriR25.UpstreamTagLocate` flagged that the `source` cell names `tools/mori-job-runway.py`, and
that the C2 before-state is `git cat-file -e 28b79d3d:tools/mori-job-runway.py` → exit 128, so a
row naming that path would assert a reproducer that is not in the tree if S102 landed before the
tool. Measured at the lane tip:

```
git cat-file -e HEAD:tools/mori-job-runway.py     → exit 0 (present)
git ls-tree HEAD tools/ | grep mori-job-runway    → 100755 blob 239dd8ebe630400a2739151260e482ad83dea459  tools/mori-job-runway.py
git merge-base --is-ancestor 09f55b6 HEAD        → exit 0 ("round-25: land tools/mori-job-runway.py (C2) after the frozen cases")
git merge-base --is-ancestor 28b79d3d HEAD        → exit 0 (the before-state commit is an ancestor of the tip)
sha256sum tools/mori-job-runway.py                → 5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411
git show HEAD:tools/mori-job-runway.py | sha256sum → 5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411 (identical; worktree clean)
```

So the tool **is** in the tip tree and any commit landing S102 on top of the tip necessarily
contains it; the before-state `28b79d3d` is an ancestor, not the tip. The flag is therefore
resolved for the tip — but the safe landing rule still holds and is recorded here:

- **Option (a), preferred:** land S102 in a commit that is a descendant of `09f55b6` (the tool's
  landing commit). Every commit on the current tip satisfies this.
- **Option (b), costless fallback:** drop the `tools/mori-job-runway.py` clause and keep only the
  standalone `python3 -I -B -c "…"` byte reproducer. That command needs nothing but the binary and
  reproduces both quotes, the sha256 and the size (verified, §2.1). The row's evidence does not
  depend on the tool.

The upstream seat's content cross-check of the row was clean: both quoted spans exact against the
bytes, module-comment offsets are the ones adjacent to the owning code (duplicate copies of the
same banners exist at 164135156 and 154750744 — the "owning module comment" wording keeps the cite
unambiguous), the `teaches` wording matches the single shipped construction site, and the version
cite at 151991030 was corrected to that offset in this row.

### 2.5 Draft `## Gate` block for `corpus/lessons/round-25.md`

**Status at the current tip (`042d75b`): `corpus/lessons/round-25.md` does not exist yet** (measured:
`ls` fails). The knowledge entry that cites S102 landed in `90ed9b7`, but the round lesson — and
with it the `## Gate` section that CORPUS.md rule 1 requires ("the round lesson's `## Gate` records,
for every new row, the URL, the access date, and a ≤25-word quote with its location grounding
`teaches`") — is still pending. The block below is this seat's draft contribution for the L1's
lesson; it is **not** landed, and this seat did not create the lesson file.

Modelled on the round-24 Gate table (`.ufo/waves/round-24/w1/SrcPsiTypes.md` §3). One row per
decision; the located quote with its location grounds the `teaches` cell (CORPUS.md rule 1).

```markdown
## Gate

Source rows opened this round for C2 (harness background-job runway, new PROVINCE ground).
The installed binary was opened read-only on 2026-10-22 (bytes only; `omp` was never executed).
An own-work row is primary for the bytes of one artifact at one digest and is not evidence of
upstream source semantics, of a live run, or of the running-job count.

| Row | Opened source / access date | Located literal quote (≤25 words) | Gate |
|---|---|---|---|
| S102 | installed binary `~/.local/bin/omp` (own-work), sha256 `85d9daf3…ccfa4`, 256702432 bytes; locator `python3 -I -B -c "…mmap/re…"`; 2026-10-22 | byte 164406766: "maxRunningJobs: () => Math.min(100, XPe.get(R))" (5 words) / byte 155231590: "id: \"async.maxJobs\", protocolDefault: [\"rpc\"], type: \"number\", default: 100" (8 words) | A/mined for the clamp and the setting default compiled into the installed build (both 100, one site each). Not evidence of upstream source text, of the live running-job count, of the per-session scope of the cap, or of any configuration surface the tool abstains on. |
```

---

## 3. What this row supports — and what it does not

**Supports (read from the bytes):**

1. The installed build carries a hard clamp of **100** on the harness background-job runway, at
   exactly one site (byte 164406766), in the expression
   `maxRunningJobs: () => Math.min(100, XPe.get(R))`.
2. The installed build declares `async.maxJobs` as a numeric setting whose schema **default is
   100** (`protocolDefault: ["rpc"]`), at exactly one site (byte 155231590).
3. Therefore the effective cap of this build is `min(100, configured)` whatever the config file
   says; a configured value above 100 cannot raise it.
4. The installed file is the omp **18.12.6** build (version bytes 256648593 / 151991030 /
   changelog 252999412) at sha256 `85d9daf3…ccfa4`, 256702432 bytes.

**Does NOT support (boundaries the L1 must not blur):**

- **Not upstream source semantics.** The row quotes compiled/minified bytes (`XPe`, `R`,
  `h({…})`) at byte offsets. What upstream *source* says is S099 (`sdk.ts`), S100
  (`tools/settings.ts`) and S101 (`docs/settings.md`) — other rows, other scopes. A C2 entry that
  cites this binary row for "upstream documents a maximum of 100" is misattributed.
- **Not the live running-job count.** The cap number is in the bytes; how many jobs run *now* is
  not readable from outside the session. That stays frontier (contract, C2 scope bounds).
- **Not the per-session scope of the cap.** "One job manager per root session, shared with
  subagents" is a code-path claim from the sibling seats' byte reads; this row carries two
  literals and their locations only.
- **Not a claim about the config file.** the operator's OMP settings file is a different artifact with a
  different row (or no row); `async.maxJobs: 200` on this host is a config fact, not a binary
  fact. The row's `teaches` deliberately says "whatever `async.maxJobs` is set to" rather than
  naming 200.
- **Not the manager's own fallback default.** `var v = 15;` (byte 160031518) and the
  "Background job limit reached" throw (byte 160033342) belong to S098's row; they are optional
  supporting bytes and are **not** claimed here.
- **Not release provenance as behaviour.** The byte-identity with release asset `omp-linux-x64`
  (§1.4) was verified but is kept out of `teaches`; it is identity/provenance, not behaviour.
- **Not a claim that any value is writable or effective at runtime.** The row says what the build
  contains, not what a given session ended up using.

---

## 4. Validator falsifiers (read-only; the lane file was never touched)

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` was run against **copies of the lane
corpus under `/tmp`** (`/tmp/v12`, `/tmp/v13mined`, `/tmp/v13b`, `/tmp/vfin` — each a copy of
`corpus/` plus `SKILL.md`). `corpus/SOURCES.md` in the lane was not modified by this seat
(`git status --porcelain corpus/SOURCES.md` prints nothing). The only modified file under
`corpus/` at the tip is `corpus/lessons/round-24.md` — a **sibling seat's** uncommitted D3
correction (routed defect D3, append-only, 4 inserted lines), not this seat's edit and not
attributable to this seat's work.

After the L1's landing, the validator was also run on the **live lane file**:
`sources-census.sh validate --file corpus/SOURCES.md --today 2026-10-22` → `file ok`, exit **0**,
no `E`/`W` line attributable to S102.

| case | what was tested | validator result |
|---|---|---|
| baseline (lane registry as-is) | — | exit **0**; six pre-existing `W04` lines (S035/S037/S073/S074/S075/S076) + `ok` |
| draft row inserted after S097, `queued` + used-by `—` | proposed landing shape | exit **0**, `ok`; census counts rows **98**, tier A=83 B=6 C=9, status mined=62 queued=26 rejected=10 |
| draft row inserted after S097, `mined` + used-by `corpus/knowledge/harness-job-capacity-r25.md`, **file absent** | the risky landing | exit **1** with **`E11 S102 missing used-by corpus/knowledge/harness-job-capacity-r25.md`** |
| same, **file present** | flipped landing shape | exit **0**, `ok` |
| draft row appended at end of file instead of inside the Registry table | wrong placement | exit **1** with **`E12 S102 row outside Registry section`** |
| anchor size edited to a wrong value (`256702433`) | number-drift probe on the anchor | exit **0**, `ok` — the validator does **not** check anchor numbers; only the row's own citation and the locator command do. Recorded so the judge knows the anchor's numbers are evidence-backed by §1.2/§1.3, not by the validator. |

The row therefore adds **no** `E01` (11 cells → NF=13, checked), **no** `E02` (numeric id), **no**
`E03` (unique id), **no** `E04`/`W04` (the `source` cell contains no `http(s)://` URL, so the
URL-duplicate rules cannot fire), **no** `E05`–`E10` (kind `own-work`, tier `A`, status in enum,
`opened` an ISO date, `recheck` a symbolic cadence), **no** `E12` when placed inside the Registry
table, and **no** `E11` provided the L1 keeps it `queued` or lands the knowledge note in the same
commit.

---

## 5. Findings for the canonical judge

1. **The clamp and the schema default are single-site facts in this build.** One match each for
   the contract's rule-2 and rule-3 regexes over the whole 256,702,432-byte file (measured). A
   row citing "the binary contains a 100 clamp" is citable; a row citing the bare `Math.min(100,`
   would not be (16 occurrences of that fragment exist).
2. **The accessor is provably the same binding.** `XPe.get(` occurs once in the entire file, at
   the clamp site (byte 164406802), and `var XPe = h({ id: "async.maxJobs", … })` is the only
   `XPe` definition (byte 155231574); `XPe` is exported as `cfgAsyncMaxJobs` (byte 171101808).
   The clamp therefore reads the setting this row's schema default belongs to. That link is
   stronger than "two numbers that happen to be 100".
3. **The literal `async.maxJobs` appears twice, but only once in the contract's regex** — the
   other occurrence (byte 96085908) is a settings-UI string table with no `id: "` prefix. A
   `grep -c 'async.maxJobs'` census would report 2 and mis-describe the build; the row cites the
   byte offset of the definition, not a count.
4. **Number discipline.** The row's numbers are: clamp 100 at byte 164406766; setting default 100
   at byte 155231590; sha256 `85d9daf3…ccfa4`; size 256702432; version 18.12.6 at bytes
   256648593 / 151991030 / 252999412. Each was printed by the command in §2.1 or by `sha256sum` /
   `stat` / `stat -c '%s'`; none is asserted from a summary. The contract's own C2 preamble states
   the same size, version and "once and once" counts, and this seat's independent measurement
   agrees with all of them.
5. **The row cannot become a host-state claim.** Its `scope` and `teaches` cells are phrased in
   build terms ("the installed build clamps …"); the config value 200, the live running-job count,
   the per-session scope and the YAML-abstention rules belong to other rows and to the tool.
6. **One own-work binary row, agreed.** The upstream seat's draft binary row and this seat's
   sharpened version were reconciled in-channel on 2026-10-22: id `S102` stands, this row is the
   one, and no second own-work row for the same bytes is proposed. Duplicate ids are a validator
   error (`E03`), and two rows for one artifact would also invite scope drift.
7. **Placement is not cosmetic.** Measured: appending the row at end-of-file is `E12`; it must go
   inside the `## Registry` table right after `S097`.
8. **The `mined` flip is a landing-order hazard, not a content problem.** Measured: `mined` +
   `used-by corpus/knowledge/harness-job-capacity-r25.md` is `E11` while that file is absent and
   clean once it exists. Land the row and the knowledge note together, or keep the row `queued`.
9. **The tool clause in the `source` cell is already safe at the tip, but the fallback is free.**
   The upstream seat flagged that `tools/mori-job-runway.py` is absent at the C2 before-state
   `28b79d3d` (measured: `git cat-file -e 28b79d3d:tools/mori-job-runway.py` → exit 128). Measured
   at the tip: the tool is present in `HEAD` (blob `239dd8ebe6…`) and `09f55b6` (its landing
   commit) is an ancestor of `HEAD`, so any commit landing S102 on the current tip contains it
   (§2.4). If the L1 nevertheless lands S102 earlier, dropping the tool clause costs nothing — the
   standalone `python3 -I -B -c "…"` command reproduces both quotes, the sha256 and the size from
   the binary alone.

---

## 6. Gates, touched surfaces, out of scope

- **Gates observed:** `corpus/SOURCES.md` read-only by this seat — this seat did not edit, stage
  or commit it, and ran no `git add`/`commit`/`stash`/`checkout`/`reset`/`pull`/`push` and no
  mutating `jj` command in the lane or at the fleet root. (The L1 landed the drafted row itself in
  `90ed9b7`; see §2.3 — the landing is the L1's edit, not this seat's, and the landed row is
  byte-identical to this seat's draft.) `omp` was **never executed**: the binary was opened only as
  bytes via `mmap`, `sha256sum`, `stat`, `file`, `readlink`. No settings file was written or
  edited (the operator's OMP settings file was read at lines 244–245 only). No `~/.omp` session
  transcript content was read; only file paths and public tool output appear here.
- **Touched surfaces (writes):** this report file only —
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-25/w1/SrcBinaryOwnWork.md`.
  Everything else this seat produced lives in `/tmp` (validator copies, the extracted command
  script, the fetched `SHA256SUMS.txt`) and outside the lane repo.
- **Out of scope / not done:** no edit by this seat to `corpus/SOURCES.md`,
  `corpus/lessons/round-25.md` or any other lane file; no product-code edit; no
  commit/push/publish/deploy; no execution of `omp`; no edit to the operator's OMP settings file,
  `~/.omp/agent/mcp.json` or any OMP setting; no upstream source row (S098–S101 belong to other
  seats); no judgment on the C2 tool's config-parsing half, the frozen cases, or the
  YAML-abstention amendment (A2) — all other seats' surfaces.
- **Tooling:** **no install or upgrade was performed by this seat**, so nothing is recorded under
  the tooling directive. Everything used was already present on the host: Python 3.14.8 (stdlib
  only — `mmap`, `re`, `hashlib`, `os`), GNU strings (GNU Binutils) 2.47, `sha256sum` 0.8.0,
  GNU Awk 5.4.1, GNU grep 0.2.0, `curl` (GitHub API + release asset), Linux 7.2.11-arch1-1. The
  pacman guard (all pacman transactions paused host-wide) was never engaged.

---

## 7. Artifact paths

- **Landed row:** `corpus/SOURCES.md:108` — id `S102`, landed by the L1 in commit `90ed9b7`,
  byte-identical to this seat's draft (§2.3). Validator on the live lane file: `ok`, exit 0.
- Draft row (as proposed, before landing): §2 of this report.
- Draft `## Gate` block (for `corpus/lessons/round-25.md`): §2.5 of this report.
- Landing outcome after the L1 landed the row: §2.3 of this report.
- Landing-order resolution for the tool clause (raised by the upstream seat): §2.4 of this report.
- Standalone reproducer command (verbatim, exit 0): §2.1 of this report.
- Citing knowledge entry (landed in `90ed9b7`): `corpus/knowledge/harness-job-capacity-r25.md`.
- Validator copies (outside the lane): `/tmp/v12/mori-shokunin/corpus/SOURCES.md` (queued shape),
  `/tmp/v13mined/…` and `/tmp/v13b/…` (mined shape, file absent / present), `/tmp/vfin/…`
  (final re-check).
- Release digest cross-check (outside the lane): `/tmp/SHA256SUMS-omp.txt`, 934 B, sha256
  `72ebc3d92054d3a2e8edafc1acf593ea685e609672b031084459f525a2fc64e5`, fetched 2026-10-22.
- This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-25/w1/SrcBinaryOwnWork.md`.

**Report: `.ufo/waves/round-25/w1/SrcBinaryOwnWork.md`**
