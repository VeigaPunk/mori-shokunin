# Mo52ExecProseLines — `file:line` verification, overcommit entry (round 52, w1)

Seat: Mo52ExecProseLines (executor, leaf). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Measured revision: **8524904adb25e44f24d9f25aac7eae909625c18c** (the data commit named in the dispatch).
Lane HEAD during this seat: `075436b1346ca659afb8be7a46f0e67e4170aa83`; the entry and every source copy I read are
byte-identical between `8524904a` and the working tree, so the working-tree `sed` reads below are reads of the data
commit's bytes.

Scope: every `file:line` reference in the **prose**, the **Reading rules (mori)** table and the **Boundaries** of
`corpus/knowledge/overcommit-commit-limit-r52.md`. Five reference sites; all five were printed with `sed -n` and
read against the cited file. No claim text was edited (L1 integrates); no vote lines were emitted by this seat — the
vote forms are reserved to the twelve ENTAILMENT reports.

## 0. Revision equality and file identity

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git rev-parse HEAD
075436b1346ca659afb8be7a46f0e67e4170aa83
$ git diff --stat 8524904adb25e44f24d9f25aac7eae909625c18c -- \
    corpus/evidence/sources-r51 corpus/evidence/sources-r52 \
    corpus/knowledge/overcommit-commit-limit-r52.md corpus/SOURCES.md
$ echo exit=$?
exit=0
```
(empty diff: entry, both copy trees and SOURCES.md are unchanged since the data commit)

Locator inventory of the entry at `8524904a` (all `:[0-9]` occurrences outside the source/recheck/sweep header
lines), so the list below is complete:

```
$ git show 8524904a:corpus/knowledge/overcommit-commit-limit-r52.md | grep -nE ':[0-9]' | grep -vE '^\s*[0-9]+:\|'
14:`Committed_AS`, printed at `fs/proc/meminfo.c:125-126` in the round-51 copy (S494, as `vm_commit_limit()` and
65:OS-state triage is tsukuroi's ground (`../tsukuroi-shokunin/PROVINCE.md:8-14,28`: detection and report, the operator
71:- `Committed_AS` is a per-CPU counter; the meminfo line is its full sum (`util.c.v7.2:937-940`), and the mode-2
72:  test uses a cheaper approximate read (`util.c.v7.2:994`). The two can differ by up to the batch size per CPU.
```
(the table-row site on entry line 58 was filtered out by the row-start pattern and is verified separately in §2)

Source-copy identity: the five round-52 copies hash to the recheck list in the entry header, and the live upstream
v7.2 bytes hash to the same values (so the copies are the cited tag's bytes, and line numbering in the copies is
upstream line numbering):

```
$ sha256sum corpus/evidence/sources-r52/*.v7.2
d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058  corpus/evidence/sources-r52/mman.h.v7.2
449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545  corpus/evidence/sources-r52/mmap.c.v7.2
767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f  corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2
e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c  corpus/evidence/sources-r52/util.c.v7.2
bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce  corpus/evidence/sources-r52/vm.rst.v7.2

$ for u in .../v7.2/Documentation/mm/overcommit-accounting.rst .../v7.2/Documentation/admin-guide/sysctl/vm.rst \
           .../v7.2/mm/util.c .../v7.2/include/linux/mman.h .../v7.2/mm/mmap.c; do
      printf '%s ' "$(basename "$u")"; curl -fsSL --max-time 30 "$u" | sha256sum; done
overcommit-accounting.rst 767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f  -
vm.rst bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce  -
util.c e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c  -
mman.h d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058  -
mmap.c 449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545  -
rc=0

$ curl -fsSL .../v7.2/fs/proc/meminfo.c | sha256sum
d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda  -
$ sha256sum corpus/evidence/sources-r51/meminfo.c.v7.2
d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda  corpus/evidence/sources-r51/meminfo.c.v7.2
```
The round-51 meminfo copy's hash also equals the `sha256` recorded in the S494 row (`corpus/SOURCES.md:273`).

## Verdict table

| entry line | reference as written | resolves to (copy actually printed) | verdict |
|---|---|---|---|
| 14 (prose) | `fs/proc/meminfo.c:125-126` "in the round-51 copy (S494, as `vm_commit_limit()` and `vm_memory_committed()`)" | `corpus/evidence/sources-r51/meminfo.c.v7.2:125-126` | **holds** (parenthetical imprecise, F1) |
| 58 (reading rules, row 1) | `util.c.v7.2:969-977` — "the limit is printed, not enforced" | `corpus/evidence/sources-r52/util.c.v7.2:969-977` | **holds** |
| 65 (prose, before Boundaries) | `../tsukuroi-shokunin/PROVINCE.md:8-14,28` — "detection and report, the operator remediates" | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:8-14` and `:28` | **holds** (lane-root-relative, F5) |
| 71 (Boundaries) | `util.c.v7.2:937-940` — "the meminfo line is its full sum" | `corpus/evidence/sources-r52/util.c.v7.2:937-940` | **holds** |
| 72 (Boundaries) | `util.c.v7.2:994` — "the mode-2 test uses a cheaper approximate read" | `corpus/evidence/sources-r52/util.c.v7.2:994` | **holds** |

Downstream/no-line references in the same three sections, checked for existence: `oom-memcg-stat-r50.md`
(reading-rules row 3) — exists, 13010 bytes; `FR8` (Boundaries) — live row `corpus/README.md:348`, open per
`corpus/README.md:481`; `S494` (prose) — row `corpus/SOURCES.md:273` names the copy and its sha; the sweep receipt
`coverage-map` names, `.ufo/waves/round-52/evidence/sweep-overcommit.txt` — exists, 434 bytes, rc 0.

## 1. Entry line 14 — `fs/proc/meminfo.c:125-126` (prose): holds

```
$ sed -n '125,126p' corpus/evidence/sources-r51/meminfo.c.v7.2
	show_val_kb(m, "CommitLimit:    ", vm_commit_limit());
	show_val_kb(m, "Committed_AS:   ", committed);
rc=0
```
125 → `CommitLimit` from `vm_commit_limit()`, 126 → `Committed_AS`. Both `show_val_kb` calls are unconditional in
`meminfo_show`, so the prose's "printed under every mode" rests on bytes that are mode-independent. The clause is
also the only place the entry fixes *where* the two lines are printed, and it says which copy: that copy is the
round-51 one, and its hash is the S494 hash.

Precision note (F1): line 126 prints the local `committed`, not a direct call; the assignment is 79 lines earlier.

```
$ sed -n '46p' corpus/evidence/sources-r51/meminfo.c.v7.2
	committed = vm_memory_committed();
rc=0
$ grep -n "committed" corpus/evidence/sources-r51/meminfo.c.v7.2
37:	unsigned long committed;
46:	committed = vm_memory_committed();
126:	show_val_kb(m, "Committed_AS:   ", committed);
```

## 2. Entry line 58 — `util.c.v7.2:969-977` (reading rules, row 1): holds

Rule text: ``Committed_AS > CommitLimit under mode 0 or 1 → normal: the limit is printed, not enforced
(`util.c.v7.2:969-977`)``.

```
$ sed -n '969,977p' corpus/evidence/sources-r52/util.c.v7.2
	if (sysctl_overcommit_memory == OVERCOMMIT_ALWAYS)
		return 0;

	if (sysctl_overcommit_memory == OVERCOMMIT_GUESS) {
		if (pages > totalram_pages() + total_swap_pages)
			goto error;
		return 0;
	}

rc=0
```
The range contains exactly the two loose-mode branches: mode 1 returns success at 969-970, mode 0 only compares the
single request against `totalram_pages() + total_swap_pages` at 972-975. The limit is computed at **978**
(`allowed = vm_commit_limit();`), one line past the end of the cited range, and is consulted only at 994 — so
`969-977` is the correct, tight range for "not enforced in modes 0 and 1": the cited range stops precisely before
the first use of the limit.

## 3. Entry line 65 — `../tsukuroi-shokunin/PROVINCE.md:8-14,28` (prose): holds

```
$ sed -n '8,14p' ../tsukuroi-shokunin/PROVINCE.md
**Owns (surfaces, all read-only probes):** pacman state (`pacman -Qkk`
verify loops, foreign/AUR census, `.pkg.tar.zst` receipt discipline),
systemd user units & timers (`systemctl --user`, unit files, failed
states), journal/boot triage (`journalctl -b`, dmesg error classes),
driver/firmware plane (kernel modules, nvidia driver + GSP firmware
presence, `nvidia-smi` shape). Update-safety questions: what an -Syu
would touch, what pins/holds exist.
$ sed -n '28p' ../tsukuroi-shokunin/PROVINCE.md
never restarts services. Detection and report; the operator remediates.
```
`8-14` is tsukuroi's owned-surface paragraph (all read-only probes); `28` carries verbatim the sentence the entry
quotes, "detection and report, the operator remediates". The sentence's claim ("OS-state triage is tsukuroi's
ground ... detection and report, the operator remediates") holds on those two spans. tsukuroi's file hash during
this seat: `b05f846d94781f64468b3c8e4038f53d71dfc53f3cf16075e3d26f53c2bb2580`.

Resolution is lane-root-relative: the same pointer in `corpus/knowledge/memavailable-estimate-r51.md:70`, and
`corpus/lessons/round-51-verifier-spotcheck.md:123-124` records that this pointer "resolves to tsukuroi's OS-state
ownership and its 'detection and report; the operator remediates' line". From the entry's own directory
(`corpus/knowledge/`) the path does not resolve — `corpus/tsukuroi-shokunin` does not exist (`ls: cannot access`).

## 4. Entry line 71 — `util.c.v7.2:937-940` (Boundaries): holds

```
$ sed -n '937,940p' corpus/evidence/sources-r52/util.c.v7.2
unsigned long vm_memory_committed(void)
{
	return percpu_counter_sum_positive(&vm_committed_as);
}
rc=0
```
`percpu_counter_sum_positive` takes the lock and sums every CPU's contribution, i.e. the exact total; the entry
calls it "its full sum" and that is what the four cited lines are. `meminfo.c:46` (see §1) is this function, so
"the meminfo line is its full sum" is supported end to end.

## 5. Entry line 72 — `util.c.v7.2:994` (Boundaries): holds

```
$ sed -n '994p' corpus/evidence/sources-r52/util.c.v7.2
	if (percpu_counter_read_positive(&vm_committed_as) < allowed)
rc=0
```
Single-line and unambiguous: `percpu_counter_read_positive` is the approximate read (`fbc->count`, per-CPU deltas
unfolded), and the line sits after the mode-1 and mode-0 early returns of §2, so it is reached only in the mode-2
path. The contrast the sentence draws — exact sum for `Committed_AS`, approximate read for the mode-2 test — is
exactly what `:937-940` vs `:994` show.

## Method, limits of this seat

- Every verdict above is a printed-bytes verdict: `sed -n '<range>p' <copy>` with `rc=0`, plus the copy hashes in
  §0 tying those copies to tag v7.2 and to the entry's recheck list. No claim that v7.2 says the same about other
  kernels, and none about this host's live `vm.*` values.
- I did not run `count-c1.py` or `count-c2.py`, did not score any arm, did not read another seat's report, and did
  not edit the entry, SOURCES.md, the copies, or anything under `.ufo/waves/round-52/` except this file.
- Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ExecProseLines/` (`tmp/` only; the curl pipelines wrote no file) was
  removed at the end of the run. Nothing was written into the lane or the fleet root by this seat.
- Tooling: none installed or upgraded; only `sed`, `grep`, `sha256sum`, `wc`, `ls`, `git show/diff/rev-parse` and
  `curl` were used, all read-only.

## Findings

- **LOW — entry:14, parenthetical provenance.** "(S494, as `vm_commit_limit()` and `vm_memory_committed()`)" read
  against lines 125-126 shows `vm_memory_committed()` nowhere in that pair: 126 prints the local `committed`,
  assigned at `meminfo.c:46`. The reference is not wrong, but a reader who greps only 125-126 cannot see the second
  symbol. `:46,125-126` would carry it. No data change needed for the claim; wording only, L1's call.
- **LOW — entry:14 vs 58/71/72, two locator styles.** The meminfo locator is the upstream path
  (`fs/proc/meminfo.c:125-126`); the four `util.c` locators are copy basenames (`util.c.v7.2:...`). Both resolve
  (S494 names the copy; `util.c.v7.2` is unique under `corpus/evidence/sources-r*/`, and basename citation is the
  lane convention — `meminfo.c.v7.2`, `oom_kill.c.v7.2`, `memcontrol.c.v7.2` elsewhere), but a grep for the
  upstream path inside the lane finds nothing.
- **LOW — entry:60, reading-rules row 3 has no locator.** The row quotes the exemption warning as
  `__vm_enough_memory: pid: N, comm: X, bytes: B not enough memory for the allocation`; the bytes behind it are
  `util.c.v7.2:998-999` (`pr_warn_ratelimited("%s: pid: %d, comm: %s, bytes: %lu not enough memory for the
  allocation\n", __func__, ...)`). The quote is accurate (96 chars, `__func__` supplies the prefix) but it is the
  only claim-bearing quote in the three sections with no `file:line`.
- **LOW — entry:65, `PROVINCE.md:8-14` is the generic ownership span for this sentence.** The memory-specific
  evidence in the same file is `:30-31` ("Host memory and kill-event measurements support OS triage; they do not
  establish which fleet wave caused pressure or whether an endpoint works"). `:28` covers "detection and report, the
  operator remediates" exactly; `:30-31` would make the "OS-state triage is tsukuroi's ground" half explicit for a
  memory reader.
- **LOW — entry:65, pointer is lane-root-relative.** `../tsukuroi-shokunin/PROVINCE.md` resolves from
  `/home/vgpnk/Projects/shokunin/mori-shokunin`, not from `corpus/knowledge/` where the entry lives. Same form and
  same target as round 51 (`memavailable-estimate-r51.md:70`), and the round-51 lesson confirms the resolution, so
  it holds; noted because a reader resolving relative to the entry's directory reaches a missing path.
