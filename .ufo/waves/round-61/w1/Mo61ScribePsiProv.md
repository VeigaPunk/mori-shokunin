# Mo61ScribePsiProv — provenance shell and six source rows

Axes: provenance accuracy, quote locality, registry conformity, scope calibration. Draft only: no corpus, counter, registry, or VCS edits are proposed as executed work.

## Ledger shell and Gate ground

Target for integration: `corpus/knowledge/psi-v73-recheck-r61.md`. Insert the independently drafted 47 pointer rows under `## Pointer ledger`; this shell intentionally supplies no pointer rows. The Gate table is keyed by S-id, not pointer, so it does not add ROW-matching records. The same Gate ground is available for the round lesson's `## Gate`, where the frozen contract requires the fetch log.

```markdown
source: S565 S566 S567 S568 S569 S570 (v7.3); S090 S091 S092 S093 S094 S095 (v7.2), with URLs and pinned-copy anchors below
verified-at: 2026-10-30 — six v7.3 files fetched and compared with the frozen copies; git.kernel.org fetch receipt: .ufo/waves/round-61/w1/Mo61ExecFetch.md; raw.githubusercontent.com twins independently opened this date with matching SHA-256 values
recheck: next kernel release — re-open all six source twins and re-derive the enumerated pointers, locations, and quotes

# PSI v7.2 line pointers rechecked against v7.3

## Scope

This ledger covers exactly the 47 deduplicated v7.2 line-pointer keys enumerated by the frozen round-61 C2 counter from `corpus/knowledge/system-pressure-r24.md`, restricted to `psi.rst`, `psi.c`, `psi_types.h`, `cgroup-v2.rst`, `Kconfig`, and `kernel-parameters.txt`. Comma-list tails without another filename prefix are not independent keys. It does not recheck prose anchors outside those six files, other source files, introduction commits, man pages, or this host's runtime PSI behavior. A passing ledger is not a whole-prose revalidation.

## Status definitions

- `same`: the quote occurs within the enumerated pointer's inclusive line range in the pinned v7.3 copy; the location cell may be `-` and is ignored by the counter.
- `moved`: the original wording survives at a different v7.3 location; the location cell names its file and inclusive line range.
- `changed`: the original wording is replaced; quote the nearest v7.3 wording governing the same claim and name its file and inclusive line range.

Mechanically, `moved` and `changed` receive the same location check: the quote must occur within the stated location range of a pinned copy. The counter does not independently prove historical equality, removal, or semantic equivalence. It requires 5–25 whitespace-separated words, at least eight distinct UTF-8 bytes, pairwise-distinct quotes, exact pointer-set coverage, and at least four cited pinned copies. Historical classification remains an editorial assertion supported by source comparison.

## Pointer ledger

| pointer | status | v7.3 location | quote |
|---|---|---|---|

## Gate

All six raw v7.3 URLs below were opened on 2026-10-30 and returned HTTP 200; their SHA-256 values matched the frozen r61 copies. Quotes are verbatim single-line substrings of those copies. The separate git.kernel.org fetch receipt records byte comparisons and UTC fetch times.

| row | URL | accessed | pinned-copy location | quote |
|---|---|---|---|---|
| S565 | https://raw.githubusercontent.com/torvalds/linux/v7.3/Documentation/accounting/psi.rst | 2026-10-30 | corpus/evidence/sources-r61/psi.rst:57 | `CPU full is undefined at the system level, but has been reported` |
| S566 | https://raw.githubusercontent.com/torvalds/linux/v7.3/kernel/sched/psi.c | 2026-10-30 | corpus/evidence/sources-r61/psi.c:1282 | `CPU FULL is undefined at the system level` |
| S567 | https://raw.githubusercontent.com/torvalds/linux/v7.3/include/linux/psi_types.h | 2026-10-30 | corpus/evidence/sources-r61/psi_types.h:55 | `FULL: Stalled tasks & no working tasks` |
| S568 | https://raw.githubusercontent.com/torvalds/linux/v7.3/Documentation/admin-guide/cgroup-v2.rst | 2026-10-30 | corpus/evidence/sources-r61/cgroup-v2.rst:1070 | `Writing "0" to the file will disable the cgroup PSI accounting.` |
| S569 | https://raw.githubusercontent.com/torvalds/linux/v7.3/init/Kconfig | 2026-10-30 | corpus/evidence/sources-r61/Kconfig:736 | `If you say Y here, the kernel will create /proc/pressure/ with the` |
| S570 | https://raw.githubusercontent.com/torvalds/linux/v7.3/Documentation/admin-guide/kernel-parameters.txt | 2026-10-30 | corpus/evidence/sources-r61/kernel-parameters.txt:5540 | `Enable or disable pressure stall information` |
```

## SOURCES.md rows

Append inside `## Registry`, before `## Paths`. Mapping follows the counter's FILES order. Raw URLs were independently fetched, rather than substituted without opening; the existing r55 rows S529–S533 use git.kernel.org URLs. All cells below are pipe-free internally; all rows have eleven cells.

```markdown
| S565 | Linux PSI documentation v7.3 — https://raw.githubusercontent.com/torvalds/linux/v7.3/Documentation/accounting/psi.rst | docs | A | v7.3 PSI documentation twin for the round-61 system-pressure pointer ledger | CPU full rule:57-59; interface and units:36-65; tag v7.3; sha256 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692; copy corpus/evidence/sources-r61/psi.rst | Bounds the r61 interface-pointer recheck to the pinned PSI documentation, not host health. | mined | 2026-10-30 | on-release | corpus/knowledge/psi-v73-recheck-r61.md |
| S566 | Linux kernel/sched/psi.c v7.3 — https://raw.githubusercontent.com/torvalds/linux/v7.3/kernel/sched/psi.c | code | A | v7.3 PSI implementation twin for the round-61 system-pressure pointer ledger | CPU full handling:1282-1288; emitter:1290-1296; proc creation:1710-1721; tag v7.3; sha256 c4edc1e7c18ca76e6e29668093fa0b26d4251cb088f2d5feab24681f285ec63f; copy corpus/evidence/sources-r61/psi.c | Grounds located implementation quotes for the r61 recheck without asserting unreviewed code is unchanged. | mined | 2026-10-30 | on-release | corpus/knowledge/psi-v73-recheck-r61.md |
| S567 | Linux include/linux/psi_types.h v7.3 — https://raw.githubusercontent.com/torvalds/linux/v7.3/include/linux/psi_types.h | code | A | v7.3 PSI enum twin for the round-61 system-pressure pointer ledger | resource enum:41-49; state semantics:51-56; state enum:57-70; tag v7.3; sha256 483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc; copy corpus/evidence/sources-r61/psi_types.h | Separates the conditional IRQ resource and full-only IRQ state from untracked IRQ some pressure. | mined | 2026-10-30 | on-release | corpus/knowledge/psi-v73-recheck-r61.md |
| S568 | Linux cgroup v2 documentation v7.3 — https://raw.githubusercontent.com/torvalds/linux/v7.3/Documentation/admin-guide/cgroup-v2.rst | docs | A | v7.3 cgroup pressure documentation twin for the round-61 system-pressure pointer ledger | cgroup.pressure:1066-1081; irq.pressure:1083-1087; tag v7.3; sha256 2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68; copy corpus/evidence/sources-r61/cgroup-v2.rst | Grounds the per-cgroup PSI switch and its non-hierarchical scope without extending the enumerated pointer set. | mined | 2026-10-30 | on-release | corpus/knowledge/psi-v73-recheck-r61.md |
| S569 | Linux init/Kconfig v7.3 — https://raw.githubusercontent.com/torvalds/linux/v7.3/init/Kconfig | code | A | v7.3 PSI build-option twin for the round-61 system-pressure pointer ledger | CONFIG_PSI help file list:736-737; CONFIG_PSI_DEFAULT_DISABLED:749-766; tag v7.3; sha256 d37de2a11baf81cbe6fb3c9ae271e5808a2c6be17f8980fe0375f6e67e677e0d; copy corpus/evidence/sources-r61/Kconfig | Relocates the v7.2 build-option pointers by six lines while retaining their documented file-list and boot-opt-in scope. | mined | 2026-10-30 | on-release | corpus/knowledge/psi-v73-recheck-r61.md |
| S570 | Linux kernel parameters v7.3 — https://raw.githubusercontent.com/torvalds/linux/v7.3/Documentation/admin-guide/kernel-parameters.txt | docs | A | v7.3 PSI boot-parameter twin for the round-61 system-pressure pointer ledger | psi= parameter:5540-5542; tag v7.3; sha256 b5a13c038a27e688380bbcaa8cdbcad24543ad6b64de0c3d5709bc32c94cb39a; copy corpus/evidence/sources-r61/kernel-parameters.txt | Relocates the psi= bool boot-parameter pointer from v7.2 lines 5505-5507 to v7.3 lines 5540-5542. | mined | 2026-10-30 | on-release | corpus/knowledge/psi-v73-recheck-r61.md |
```

## Evidence and outcomes

- `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`: scratch free 422.7G, use 48%; no ENOSPC.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD`: `7370a731abcafc4c803111de7c22cd6264d63be1`.
- Read frozen contract first. Counter evidence: `.ufo/waves/round-61/count-c2.py`, `enumerate_pointers`, `provenance_ok`, and `measure` (lines 56–183 in the opened snapshot). Enumeration printed `47`; all six files occur in the key set.
- `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r61/*` printed all six frozen hashes reproduced in the proposed rows above.
- For each relative upstream path `p` in `{Documentation/accounting/psi.rst,kernel/sched/psi.c,include/linux/psi_types.h,Documentation/admin-guide/cgroup-v2.rst,init/Kconfig,Documentation/admin-guide/kernel-parameters.txt}`, the exact fetch shape was `curl -s -o "raw_$n" -w "%{http_code}" --max-time 30 "https://raw.githubusercontent.com/torvalds/linux/v7.3/$p"`, from seat scratch, with `n=$(basename $p)`. Output, in that order: `psi.rst http=200 sha=11c6b7129103b454`; `psi.c http=200 sha=c4edc1e7c18ca76e`; `psi_types.h http=200 sha=483269b27c82b438`; `cgroup-v2.rst http=200 sha=2750c11a6324e18f`; `Kconfig http=200 sha=d37de2a11baf81cb`; `kernel-parameters.txt http=200 sha=b5a13c038a27e688`. The printed hash receipts are prefixes; the complete pinned hashes came from the separate sha256sum command, not this abbreviated fetch output.
- Located Gate quotes were read directly from the six pinned copies at the locations in the Gate table; each is below 25 words.
- Byte comparison: `cmp <seat-scratch>/raw_<file> /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r61/<file>` for all six files, chained with `&&`, printed `raw_v73_byte_matches=6 rc=0`. This establishes complete byte equality, beyond the abbreviated fetch hash receipts.
- Additional v7.2 fetches used `curl --fail --location --silent --show-error https://raw.githubusercontent.com/torvalds/linux/v7.2/<upstream-path> -o <seat-scratch>/v72/<file>`. SHA-256 outputs: psi.rst `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`; psi.c `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5`; psi_types.h `483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc`; cgroup-v2.rst `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`; Kconfig `a43f09d89309a6bd7036c96e0836c30c021f2d56b042be288a15533dd9e944bd`; kernel-parameters.txt `23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c`.
- Source comparison observed unchanged psi.rst and psi_types.h files; psi.c differs only at line 1026 (`delta < 0` becomes `delta <= 0`), outside all enumerated ranges. Direct Kconfig reads confirmed 730-731 → 736-737 and 743-760 → 749-766. kernel-parameters.txt reads confirmed 5505-5507 → 5540-5542. These comparisons support 44 same / 3 moved / 0 changed, but this is not a C2 execution receipt.
- Registry inspection at freeze printed `rows: 337`, `max id: S564`, `S565-S570 present: 0`; last registry row is `corpus/SOURCES.md:344`, next section `## Paths` at :346. Registry header at :5 has the eleven columns used above.

## Findings and limits

1. Contract conflict, verbatim: `rows S565–S070 appended in the data phase`. Seat assignment instead specifies S565–S570. Draft follows the explicit six-row seat assignment; frozen contract remains untouched.
2. `moved` and `changed` share the same loc-bounded mechanical check; the counter does not establish semantic status against v7.2. The shell says so rather than upgrading a located quote to proof of semantic equivalence.
3. Do not place example pointer rows in the ledger: ROW matching is not fence-aware. Only the actual 47 rows may use that shape.
4. Census E11 requires the used-by ledger file to exist in the scratch mirror and eventual lane before validation. The six rows alone are not a complete landing.
5. A preliminary baseline census attempt used a detached SOURCES file directly under seat scratch; it exited 1 with no captured stdout from the compound command. That location cannot supply the registry's used-by tree. No clean census or C2 result is claimed here; assigned executor owns mirror validation.
6. An exploratory mapping helper initially printed incorrect `moved_to` labels because its formatter used original start/end values. Direct source reads and a corrected per-line mapping confirmed the three destinations stated above. One exploratory helper also failed with `NameError: name 'D' is not defined`; neither output is acceptance evidence.

Touched persistent surface: only this report. Scratch fetches and read receipts are temporary and removed before yielding. Out of scope: 47 ledger data rows, production landing, census acceptance, counters, host remediation, commits, deployment. No tools installed or upgraded. Importing the counter during enumeration may have refreshed Python bytecode cache in the wave directory; no source file was edited, and that incidental cache is not claimed as evidence.
