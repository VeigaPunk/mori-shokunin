# ReopenS149 — re-open attack on row S149 (supersedes S128) at f2de0ee

Verdict: **holds** — S149's cells match the re-fetched bytes, the named defect is fixed not copied, all four used-by paths cite S149, and no live reader states the defective wording.

seat: MoriR28.ReopenS149 (leaf; no subagents, no background jobs)
target: `f2de0eedcd60d2e354da75265ea6122bc3896073` (attack revision); lane read-only, committed bytes only
scratch: /fast/scratch/hyaku/mori-r28-w2/ReopenS149/ (fetched bytes + row extracts; no clone needed)
lane writes by this seat: this report only

## 1. Source re-opened now (curl, 2026-10-22T18:53–18:57Z)

| URL | access (UTC) | HTTP / bytes | sha256 of bytes fetched | vs Gate line |
|---|---|---|---|---|
| https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html | 2026-10-22T18:53:37Z | 200 / 11,680 | `769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9` | equal |
| https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html | 2026-10-22T18:53:37Z | 200 / 7,955 | `6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc` | equal |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | 2026-10-22T18:54:59Z | 200 / 98,196 | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | equal to anchor |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/fork.c | 2026-10-22T18:54:59Z | 200 / 85,725 | `359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d` | equal |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | 2026-10-22T18:54:59Z | 200 / 34,311 | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | equal |
| man-pages.git `proc_pid_oom_score_adj.5?id=man-pages-6.20` | 2026-10-22T18:56:33Z | 200 / 4,212 | `16a0d4b50deca2828d840350262d936f70934272a276b96c750af050f31161f3` | equal |
| same path `proc_pid_oom_score.5?id=man-pages-6.20` | 2026-10-22T18:56:33Z | 200 / 1,899 | `95c707bd3b4f2d8615085ac5a1bdacbeb5d975cfb94371dcfd4bf33e239f50ea` | equal |

No drift: every digest in S149's anchor cell and the Gate line equals my fetch byte-for-byte. **holds**

## 2. Gate line (corpus/lessons/round-28.md:68)

Verbatim at the stated line: `| S149 | https://man7.org/…/proc_pid_oom_score_adj.5.html ; …/proc_pid_oom_score.5.html (sha256 769edf3b… ; 6169628d… ) | 2026-10-22T17:59:01Z | `769edf3b…` | adj page `:145-146` "The default value for this file is 0; a new process inherits its parent's oom_adj setting." (16 words) | admit, A, mined (SupersedeS128) |` (`corpus/lessons/round-28.md:68` at f2de0ee).
- Located quote is verbatim in my fetched bytes at adj `:145-146` (`scratch …/proc_pid_oom_score_adj.5.html:145-146`), 16 words ≤25.
- Both digests in the line equal §1 fetches; the sha256 column names the first URL's digest, matching the Gate header's own convention (`corpus/lessons/round-28.md:61` note). **holds**

## 3. Every S149 cell vs the bytes (SOURCES.md:154 at f2de0ee; row 4,002 B incl. line prefix)

- **source**: pages "(the v7.2 code that enforces them is S127; the oom_badness scaling and the absent 3% root term are S003)". Fixes the old "code they describe" overstatement (F6); both URLs live (§1). **holds**
- **kind/tier**: docs / A — consistent. **holds**
- **scope**: "the pages **state** inheritance and the CAP_SYS_RESOURCE rule only inside the oom_adj paragraph" — placement claim, true: adj `:134` opens the `oom_adj` paragraph, the sentences sit at `:146-147`, and `grep -i 'inherit|CAP_SYS_RESOURCE|privileged'` on the adj page returns only `:146-147`; on the score page only `:80` ("whether the process is privileged", a badness factor, not a write rule). Comparator corrected to S003 for the 3%/scaling (F3). **holds**
- **anchor** (spot-verified on §1 bytes): adj `:72` (since 2.6.36), `:77-78` (badness 0–1000), `:86-88` (3% root), `:102-103` ("added"), `:104-110` (range, -1000), `:122-127` (oom_adj scaling), `:145-149` (inheritance/privilege), `:175` footer; score `:72-80`, `:97-98`, `:120` footer — all true. base.c `:583-602` (proc_oom_score, formula `:596-597`, [0,2000] comment `:591-595`), `:1089-1101`/`:1213-1231` (oom_adj scaling), `:1131-1133` (`-EACCES` floor gate), `:1155-1157` + `:1174-1176` (`oom_score_adj_min` set only for `CAP_SYS_RESOURCE` writers), `:1242-1256` (read), `:1275-1279` (`-EINVAL` range), `:3351-3353` (`oom_score` S_IRUGO; `oom_score_adj` S_IRUGO|S_IWUSR) — all true. fork.c `:1768-1769` (copies value **and** floor in copy_signal), `:1949-1966` (copy_oom_score_adj), called at `:2558` — all true. oom_kill.c `:199-237` is `oom_badness`; `adj *= totalpages / 1000; points += adj;` is at `:233-234` (inside the cited `:232-234` span; `:232` is a blank line — trivial). `grep -c -i 'root|3%|CAP_SYS|capab'` on all 1,257 lines → **0**, so "no capability term in the function" holds and the 3% clause is unimplemented in v7.2. 6.20 blobs digests equal; their cited lines carry the four blocks. **holds**
- **teaches**: opens exactly `supersedes S128 — ` (em dash). Claims: (a) defect named verbatim; (b) placement is "a documentation gap, not an absent kernel rule" — true per base.c `:1131-1133`, fork.c `:1768-1769`; (c) writable -1000..+1000 scaled by totalpages/1000 (`oom_kill.c:233-234`); (d) read-only [0,2000] export (`base.c:3351`, `:596-597`); (e) 3% clause unimplemented (`oom_kill.c:199-237`, zero capability/root terms). **holds**
- **status `mined` / opened 2026-10-22 / recheck on-release** — matches S128's convention and A1's rule. **holds**
- **used-by**: `corpus/knowledge/oom-victim-selection-r27.md, PROVINCE.md, corpus/README.md, corpus/lessons/round-28.md` — all four cite S149 as a word at f2de0ee (verified below). **holds**

## 4. Named defect fixed, not copied

S128's defective teaches ("…inheritance and privilege sentences belong to the legacy oom_adj file, not to oom_score_adj") is false: the kernel gives oom_score_adj its own privilege floor and copies it at fork. S149's teaches does not repeat it — it quotes the old clause only to refute it, then states the verified kernel contract (§3). S128's own row is byte-identical at f2de0ee and 6ebd518f (`cmp` ok — history kept, per QUALITY 81; the false text stays only inside the frozen old row and inside S149's quote-to-refute). The knowledge entry's inheritance/floor facts now carry the correct wording and cite S148 (`corpus/knowledge/oom-victim-selection-r27.md:84-89`). **holds**

## 5. Used-by paths and live readers (QUALITY 77)

`git grep -w S149 f2de0ee` over live readers: PROVINCE.md:377, corpus/README.md:36, corpus/knowledge/oom-victim-selection-r27.md:1 (source header: "S149 (man-pages 6.19 proc_pid_oom_score_adj(5) and proc_pid_oom_score(5) — the documented contract…)"), :66 (twice, as locators), corpus/lessons/round-28.md:68. All four used-by paths cite it. `git grep -w S128` over SKILL.md PROVINCE.md corpus/README.md corpus/knowledge → **0 hits**. Defective-wording sweep (`legacy oom_adj file`, `sentences belong`, `not to oom_score_adj`, `never for oom_score_adj`, `CAP_SYS_RESOURCE rule are documented`) → only hit is S149's own refutation line; no live reader asserts the defect. Official counter `bash .ufo/waves/round-28/count-c1.sh f2de0ee` → `superseding=7/8 ids=S096,S097,S127,S128,S129,S131,S140`, no `fail S149`, `readers_left=0`, `row_identity … bad=0`, `C1=unmet` (true exit 1; only `fail S147 row_absent`, another seat's row). **holds**

## Findings

- None at severity. Trivial: anchor span `oom_kill.c:232-234` begins one line before `adj *= totalpages / 1000;` (`:233-234` are the statements). Knowledge entry cites `mm/oom_kill.c:226-235` for the 3% absence while S149 anchors `:199-237` — both inside `oom_badness`, consistent.

## Residual risk and gaps

- Not re-verified: S127's `include/uapi/linux/oom.h` URL (third URL in S127's source cell, named only transitively by S149), the man-pages 6.19 tarball (S149 cites the man7 HTML, which I fetched), old access timestamps (unre-observable by design).
- `readers_left=0` covers all eight superseded ids at this revision, not just S128 — measured by the lane's own counter.
- C1 as a whole is `unmet` at f2de0ee solely because S147 (supersedes S101) is absent — outside this row's scope.

## Tooling

No installs or upgrades; all tools already present (curl 8.23.0, git 2.56.0, bash 5.3.20, sha256sum 0.8.0). `/home/vgpnk/.omp/agent/RULES.md` tooling directive followed; pacman untouched (paused host-wide). Lane accessed read-only (`git show/grep`); no jj run in the lane, no refs mutated, no service/process touched. No uid, pid, unit name, settings value or host command line in this report.
