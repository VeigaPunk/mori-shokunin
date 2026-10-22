# Wave 2 — Re-open S092 and S093 (seat ReopenS092S093)

Scope: re-open the URLs of SOURCES rows S092 and S093 in `corpus/SOURCES.md` at the
working tree of `mori-shokunin` (HEAD `13208d2a533380e1231dc935b6c338db99f1ddae`;
rows byte-identical at the wave's measured tip `a730ecfe`, see Stability below).
Verified per row: SHA-256 prefix, anchor line numbers against the fetched bytes,
located quotes in the round-24 lesson Gate, and the scope and teaches cells.
Scratch: `/fast/scratch/hyaku/mori-r24-a2/w2/ReopenS092S093/` (fetched bytes kept there).
Tooling directive: no installs or upgrades were performed; `curl`, `sha256sum`, `wc`,
`awk` from the host were sufficient.

Commands run (both rows):

```
curl -fsSL -o cgroup-v2.rst 'https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst'
curl -fsSL -o init-Kconfig  'https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig'
sha256sum cgroup-v2.rst init-Kconfig
```

Stability of the two rows across tips: `git show a730ecfefbdb...:corpus/SOURCES.md`
and the working tree filtered to the `| S092 ` / `| S093 ` rows hash to the same value
(`257342bad21972b9...`). The rows reviewed below are the rows that landed.

---

## S092 — cgroup-v2.rst (docs, tier A) — VERIFIED, survives

Row: `corpus/SOURCES.md:98`; lesson Gate row: `corpus/lessons/round-24.md` (Gate table, S092).

| Check | Claimed | Observed | Verdict |
|---|---|---|---|
| SHA-256 prefix | `a9433bb0e16a67f0` | `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` (3524 lines) | match |
| cgroup.pressure:1066-1081 | heading + read/write/default/non-hierarchical text | heading at 1066; body 1067-1080; 1081 blank; no other section inside the range | match |
| irq.pressure:1083-1087 | heading + read-write nested-keyed | heading 1083; text 1084-1087 | match |
| cpu.pressure:1215-1221 | read-write nested-keyed | heading 1215; `A read-write nested-keyed file.` 1216; trailing sentence 1221 | match |
| memory.pressure:1911-1915 | read-only nested-keyed | heading 1911; `A read-only nested-keyed file.` 1912 | match |
| io.pressure:2171-2175 | read-only nested-keyed | heading 2171; `A read-only nested-keyed file.` 2172 | match |
| Gate anchors `1066-1087, 1215-1221, 1911-1915, 2171-2175` | as above | 1066-1087 is exactly the union of the cgroup.pressure and irq.pressure sections | match |

Located quote (Gate, `1073-1074`): lines 1073-1074 of the fetched file read
`This control attribute is not hierarchical, so disable or enable PSI` /
`accounting in a cgroup does not affect PSI accounting in descendants`. The Gate
quote is the exact concatenation; 22 words, within the 25-word bound.

Scope cell: verified against the anchors. All four per-controller pressure files are
present in the fetched file (1066-region, 1083, 1215, 1911, 2171); access modes are
documented exactly as the cell requires (`cgroup.pressure` read-write single value,
allowed `0`/`1`, default `1`, lines 1067-1068; irq/cpu read-write nested-keyed 1084/1216;
memory/io read-only nested-keyed 1912/2172); the switch semantics (writing 0 disables,
1 re-enables, effect not hierarchical, lines 1070-1075) match "switch semantics only".
Nothing in the anchors claims counter semantics or host availability — the exclusions hold.

Teaches cell: "Each controller carries its own pressure file, and the cgroup.pressure
switch is a per-cgroup 0/1 switch, not a hierarchical one, so disabling PSI accounting
in a cgroup leaves its descendants unaffected." — supported by lines 1066-1075 verbatim.

Cross-reference: `corpus/knowledge/system-pressure-r24.md:23,103` cites S092 with
`cgroup-v2.rst:1066-1087` — the same range verified here.

Findings: none. No overclaim, no anchor drift, digest matches a fresh fetch today.

---

## S093 — init/Kconfig (code, tier A) — VERIFIED with one minor anchor imprecision

Row: `corpus/SOURCES.md:99`; lesson Gate row: `corpus/lessons/round-24.md` (Gate table, S093).

| Check | Claimed | Observed | Verdict |
|---|---|---|---|
| SHA-256 prefix | `a43f09d89309a6bd` | `a43f09d89309a6bd7036c96e0836c30c021f2d56b042be288a15533dd9e944bd` (2321 lines) | match |
| CONFIG_IRQ_TIME_ACCOUNTING:615-624 | option + help | `config IRQ_TIME_ACCOUNTING` at 615; block through `If in doubt, say N here.` 623; 624 blank | match |
| CONFIG_PSI:723-741 | option + help | `config PSI` at 723; block through `Say N if unsure.` 741 | match |
| help-text file list:730-733 | the /proc/pressure/ file list | file-list sentence is 730-731; 732-733 are the next sentence ("These will indicate / the share of walltime...") | **overbroad by 2 lines** (minor) |
| cgroup2 text:735-737 | cgroup2 per-cgroup files | `In kernels with cgroup support, cgroups (cgroup2 only) will / have cpu.pressure, memory.pressure, and io.pressure files, / which aggregate...` | match |
| CONFIG_PSI_DEFAULT_DISABLED:743-760 | option + psi=1 text | `config PSI_DEFAULT_DISABLED` at 743; psi=1 help at 748-750; range covers all substantive help | match |
| psi=1 text:748-750 | opt-in sentence | `If set, pressure stall information tracking will be disabled / per default but can be enabled through passing psi=1 on the / kernel commandline during boot.` | match |

Located quote (Gate, `730–733`): "If you say Y here, the kernel will create
/proc/pressure/ with the pressure statistics files cpu, memory, and io." The text is
exact (joining lines 730-731) and 19 words, within the 25-word bound — but the quote
ends on line 731, not 733. Lines 732-733 belong to the following sentence. The same
`730-733` label appears in the SOURCES anchor cell ("help-text file list:730-733") and
is reused in `corpus/knowledge/system-pressure-r24.md:32`.

Scope cell: verified. All three named options exist in this file at tag v7.2 (615, 723,
743); the CONFIG_PSI help text names the /proc/pressure/ files cpu, memory, io (731);
the psi=1 opt-in that overrides CONFIG_PSI_DEFAULT_DISABLED is at 748-750; "v7.2 only"
holds (tag-pinned URL, digest-stable).

Teaches cell: all three clauses verified — "names only cpu, memory, and io" is accurate
(no irq file anywhere in the CONFIG_PSI help text, 723-741); "CONFIG_PSI_DEFAULT_DISABLED
leaves tracking disabled unless psi=1 is passed" matches 748-750; "CONFIG_IRQ_TIME_ACCOUNTING
is a separate fine-granularity task irq time option" matches 615-617
(`bool "Fine granularity task level IRQ time accounting"`).

Finding (minor, precision not substance): the located-quote/anchor range for the
CONFIG_PSI help-text file list is `730-733`, but the quoted sentence occupies only
`730-731`; lines 732-733 are a different sentence. Content is not misquoted and the
cells do not attribute different words to those lines, so this does not rise to a kill.
Suggested correction: `help-text file list:730-731` in `corpus/SOURCES.md:99`, the
Gate row in `corpus/lessons/round-24.md`, and `corpus/knowledge/system-pressure-r24.md:32`.

---

## Verdict per row

- **S092: confirmed.** Digest, all five anchor ranges, the located quote, scope and
  teaches cells all check against a fresh fetch of the tagged URL.
- **S093: confirmed with one minor precision defect.** Digest, anchors, quote text,
  scope and teaches cells check; the file-list anchor range `730-733` should be
  `730-731` (quote ends at 731).

## Residual risk and verification gaps

- The wave-1 fetch timestamps (08:14:40Z / 08:15:00Z) cannot be reproduced after the
  fact; identity of today's digest with the recorded prefix is the evidence that the
  recorded bytes are the bytes at the tag now. Registry already marks both rows
  `recheck: on-release`.
- The digests were recomputed from `raw.githubusercontent.com`; a tag re-point would
  have surfaced as a digest mismatch and did not.
- Out of scope, not run: rows S090-S091 and S094-S096; the claim that the man-pages
  `proc_pressure` page still does not exist (S097); any mutation testing.
- No files other than this report were created inside the lane repo; no git-mutating
  command touched the lane; scratch only under `/fast/scratch/hyaku/mori-r24-a2/w2/ReopenS092S093/`.
