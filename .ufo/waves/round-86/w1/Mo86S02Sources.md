# Mo86S02Sources — round 86 w1: one opened source, one knowledge entry

Seat: leaf member, sources scribe. Detection/report only. No commit, no push, no git mutation in the
lane. No subagent dispatch. No tool installs (nothing installed this seat; `curl`, `python3` stdlib and
coreutils only).

## 1. Behavior

1. Read the frozen authority `.ufo/waves/round-86/contract.md` (P-C1/P-C2/P-C3, targets, kill rules,
   controls) at the revision in force when this seat started, plus `CORPUS.md` §*SOURCES.md*, the lane
   `corpus/README.md`, and `corpus/knowledge/receipt-provenance-r85.md` for the entry shape and the
   named gap the round fills.
2. Counted the registry with the frozen census parser: **374 rows** before this seat, highest id
   **S601** — `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` →
   `374`; highest via `grep -oE … | sort -V | tail -1` → `S601` (2026-11-04). Confirmed `S602` was
   unused and no row carried the chosen URL (`grep -c 'raw.githubusercontent.com/in-toto'` → `0`).
3. Probed five candidate URLs with a User-Agent and picked one by located quote, not by topic fit
   alone (table in §3).
4. Pinned the chosen bytes under this seat's evidence path, wrote the knowledge entry, appended the
   registry row and a search-log note, then ran the maintained census validator.

## 2. Touched surfaces

| Path | Change | Lines |
|---|---|---|
| `corpus/knowledge/execution-evidence-r86.md` | new entry (frontmatter, K1–K5, `## Gate`) | 133 |
| `corpus/SOURCES.md` | `+3` (row S602; blank; round-86 search-log note) — `git diff --stat` = `1 file changed, 3 insertions(+)` | 463 → 466 |
| `.ufo/waves/round-86/evidence/sources-r86/in-toto-spec-v1.0.md` | new byte pin, 87108 bytes, 2217 lines | — |
| `.ufo/waves/round-86/w1/Mo86S02Sources.md` | this report | — |

No other path was written. `git status --porcelain` at report time shows exactly
` M corpus/SOURCES.md`, `?? corpus/knowledge/execution-evidence-r86.md`,
`?? .ufo/waves/round-86/evidence/sources-r86/` (plus sibling wave staging that predates this seat).

Hashes at report time: `corpus/SOURCES.md` `24cab2a8d9fa6f15c89805dbda16536402687bfbafe4062d3aceacc40870d956`;
`corpus/knowledge/execution-evidence-r86.md`
`6aca39abf884de2141b60470c325d472b97e955849094a4e89d867860df9f3ff`;
pin `17d3326e4cf58234619dbfe821cdc5187e55e2c89f7b63f03699c46588322097`.

## 3. Source opened — S602

**in-toto Specification v1.0.0**, `https://raw.githubusercontent.com/in-toto/docs/v1.0/in-toto-spec.md`.

| fact | value |
|---|---|
| HTTP | 200, no redirect (`%{url_effective}` identical); two fetches byte-identical (`cmp` clean) |
| size / lines | 87108 bytes / 2217 lines (`wc -lc`); UTF-8 BOM; raw Markdown |
| sha256 | `17d3326e4cf58234619dbfe821cdc5187e55e2c89f7b63f03699c46588322097` |
| revision | title page `Version 1.0.0`, dated Jun 02, 2023; tag `v1.0` = annotated tag `91d55f1e…`, dereferenced to commit `926031f40be8db78f992f02f3e50e97a09db5320` |
| pin | `.ufo/waves/round-86/evidence/sources-r86/in-toto-spec-v1.0.md` |
| row | `S602 | spec | A | mined | opened 2026-11-04 | recheck 365d` |
| used-by | `corpus/knowledge/execution-evidence-r86.md` |

Candidate screen (all fetched 2026-11-04, `curl -sSL -A`):

| candidate | outcome | verdict |
|---|---|---|
| `raw.githubusercontent.com/in-toto/docs/v1.0/in-toto-spec.md` | 200, 87108 B, no redirect | **included, S602** |
| `reproducible-builds.org/docs/definition/` | already S600 | excluded (duplicate URL+scope = E04) |
| `arxiv.org/abs/2404.09241` | already S601 (rejected row) | excluded (duplicate URL) |
| `slsa.dev/spec/v1.0/provenance` | 200, 61049 B | excluded — already S060 |
| `sqlite.org/testing.html` | 200, 59623 B | excluded — mutation-testing practice; S598 already grounds mutation adequacy, and the page adds no execution-evidence ground |
| `manpages.debian.org/unstable/reprotest/reprotest.1.en.html` | 200, 52595 B | excluded — the instrument that rebuilds twice and compares build artifacts; a tool behaviour, not a statement about what a record's default verification checks |
| `salsa.debian.org/…/reprotest/-/raw/master/README.rst` | **404** | excluded, never opened |

## 4. Findings (what the source actually grounds)

- **F1 — the split the round needs.** Link metadata carries `command`, `materials`, `products`,
  `byproducts` (`stdout`, `stderr`, `return-value`) and `environment` (pin `:1025-1046`); the
  `command` field is "the command and its arguments as executed by the functionary" (`:1053-1054`).
  The byproducts paragraph then says the field is opaque and
  **"Byproducts are not verified by in-toto’s default verification routine."** (`:1063-1064`, 9 words),
  usable "for further scrutiny during an inspection step". This is the located statement that a
  recorded command plus a recorded body is a *record*, not a *binding* — exactly the gap
  `knowledge/receipt-provenance-r85.md` §K3 ends on ("must re-run the command to make the body a fact
  rather than a claim").
- **F2 — the spec has re-execution, but not body comparison.** An inspection is "operations that need
  to be performed on the final product at the time of verification" (`:787-789`) and its record carries
  `"run": "<COMMAND>"` plus `expected_materials`/`expected_products` artifact rules (`:795-807`). So the
  spec re-runs commands at verification time and compares **artifacts** (hashes via artifact rules); no
  rule compares a recorded `byproducts.stdout` to the inspection's output.
- **F3 — the signature is not the missing check.** A `Link` is "metadata information gathered while
  performing a supply chain step or inspection, signed by the functionary that performed the step"
  (`:318-321`); the document states no check that the recorded command produced the recorded stdout.
- **F4 — negatives carry their sweeps** (on the pin, 2026-11-04): `grep -ci 'reproduc'` → **0** (the
  specification never uses the word); `grep -c 'stdout'` → **16** (prose at `:332`, `:1066`; 14 JSON
  example values); `grep -ci 'byproduct'` → **22**; `grep -ci 'compar'` → **1** (line `:959`, an
  artifact-rule code comment, not a byproduct rule).
- **F5 — mapping recorded in the entry (K4).** `# cmd:` ↔ `command`; `# ---` body ↔
  `byproducts.stdout`; `# counter-sha256:` ↔ artifact hashes (S600's byte comparison, not this source);
  `# rev:` and the scratch export are the lane's own (the spec's `environment` is explicitly opaque,
  `:1070-1073`); the replay pass is the inspection shape with the comparison target changed to the
  recorded body. Not claimed: that in-toto requires reproducibility, that its signature binds
  execution, or that mori implements in-toto.

## 5. Gates run

**G1 — quote is verbatim and inside the word limit.** Both quotes were re-derived from the pin bytes,
not from memory:

```
joined_contains_quote: True
joined_span: 'Byproducts are not verified by in-toto’s default verification routine.'
words: 9
q2_joined: True words: 14
```

Quote 1 spans raw lines 1063-1064 (sentence starts mid-line 1063 after "…step performed."), joined
with one space; the apostrophe is U+2019. Quote 2 is `:1053-1054`.

**G2 — registry census before/after.** 374 → **375** rows; `malformed=0` (NF!=13);
`dupids=` (empty); tier/kind/status enum check prints nothing; `used-by`
`corpus/knowledge/execution-evidence-r86.md` exists on disk.

**G3 — maintained census validator (the seat's required gate).** Command and full output:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf across scopes
mori	W04	S351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S492 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S546 duplicate url www.rfc-editor.org/rfc/rfc8259.txt across scopes
mori	W04	S552 duplicate url doi.org/10.1109/TSC.2026.3698682 across scopes
mori	W04	S565 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/accounting/psi.rst?h=v7.3 across scopes
mori	W04	S566 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/sched/psi.c?h=v7.3 across scopes
mori	W04	S567 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/psi_types.h?h=v7.3 across scopes
mori	W04	S568 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/cgroup-v2.rst?h=v7.3 across scopes
mori	W04	S570 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/kernel-parameters.txt?h=v7.3 across scopes
mori	W04	S571 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/sched/psi.c?h=v7.3 across scopes
mori	W04	S583 duplicate url learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64 across scopes
mori	W04	S585 duplicate url learn.microsoft.com/en-us/windows/win32/api/realtimeapiset/nf-realtimeapiset-queryunbiasedinterrupttime across scopes
mori	W04	S586 duplicate url docs.aws.amazon.com/waf/latest/developerguide/waf-tokens-immunity-times.html across scopes
mori	W04	S587 duplicate url learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64 across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=0
```

`rc=0`, `mori ok`, **W04 warnings only** (the seat spec tolerates W04). No E-code fired. `grep -c 'S602'`
over that output → `0`: the new row raises no finding, and no W04 line names it.

**G4 — no duplicate/URL or schema regression.** `grep -c 'raw.githubusercontent.com/in-toto' corpus/SOURCES.md`
→ `1` (this row only); no other row carries the v1.0 URL or the same URL+scope.

## 6. Revision honesty (the lane moved while this seat ran)

- Start of seat: `HEAD = 4eab48c0f721e5917f7611d51561894873a21ea4` (branch `master`), working tree
  clean except untracked `.ufo/waves/round-86/w1/` and `w1.ready.dispatched`.
- End of seat: `HEAD = 98d15d8f784e55d979b84273aafb45225b8b8ccc` — two sibling commits landed
  (`57104423` routed-defect corrections, `98d15d8f` contract **A1** + C2 counter guard fix).
- A1 (read via `git show 98d15d8f -- .ufo/waves/round-86/contract.md`) adds 13 lines: `--scratch` on
  the C2 subject and the stub guard's three arm labels. **It does not touch P-C1/P-C3, the targets, the
  populations, or any sources/knowledge obligation.** This seat's contract reading remains valid.
- Consequence recorded for the judge: the contract hash I can cite at report time is
  `5fafb32099c3304e3fb388fe3271f92c701a29af7046da45c82c63e45bf533c6` — that is the **post-A1** file
  (the pre-A1 bytes I read are `6b1447c3…` per the A1 diff's `index` line). Files I read and did not
  write: `corpus/knowledge/receipt-provenance-r85.md`
  `1475e28ffd0651fa748990d859846595175c3181bdc190981efe1ec6295e0b80`, `corpus/README.md`
  `1ea45dda95d227ff9ab06b373d48c75cae47b8543704dddf602ece5177ac3430` (both unmodified in the working
  tree, so report-time hashes equal read-time bytes).
- The working-tree diff of `corpus/SOURCES.md` is exactly `+3` lines and contains only my row and my
  search note (`@@ -383,0 +384 @@` and `@@ -463,0 +465,2 @@`): no sibling row was clobbered.

## 7. Out of scope / not done (deliberate)

- **No `corpus/README.md` coverage-map row** for `execution-evidence-r86.md`. The r85 precedent has
  one, but my seat spec names only `SOURCES.md`, the knowledge entry, `…/sources-r86/` and this
  report; writing README would exceed the named write scope and could collide with a sibling index
  owner. Routed to `Mo86S01Lesson` in the same message as the Gate data.
- **No `corpus/lessons/round-86.md` write** — its sole writer (`Mo86S01Lesson`) asked for the Gate
  data instead; sent (id, URL, tier/status, pin path, sha256, bytes/lines, access outcome, both quotes
  with line numbers, the sweeps, and the README note).
- **No commit, no `git add`, no push** — L1 owns the lane commit. The three paths are left as
  working-tree changes for the L1.
- **No durable copy under `corpus/evidence/sources-rNN/`** — r83/r84/r85 kept pins there, but this
  wave's seat spec names `.ufo/waves/round-86/evidence/sources-r86/` and says "that path is yours".
  I followed the seat spec. If the L1 wants the r85 convention too, `cp` of the pinned file is a
  one-line act by whoever owns that path.
- **Extension deviation, disclosed:** the file is saved as `in-toto-spec-v1.0.md`, not `<slug>.html`
  as the seat spec's template reads, because the bytes are raw Markdown; calling them `.html` would
  misdescribe the pin.
- **No correction to any existing row.** Append-only respected: S602 is new; no row was edited.

## 8. Known limits of this seat's work

- Only tag `v1.0` was pinned. `master` was also fetched the same day (2385 lines) and carries the same
  byproducts paragraph at its own numbering (`:1063-1066`), but the row and entry pin the tag, so a
  later master revision cannot silently re-anchor the quote.
- The entry reads the specification as text; it does **not** test any in-toto implementation, and it
  claims nothing about whether a real verifier behaves as the spec says.
- The W04 warning set is pre-existing; I checked only that it contains no `S602` line, not that each
  warning predates this round.
- Two fetches are byte-identical; that is stability within this seat's window, not a long-lived
  guarantee (the row's recheck cadence covers that).
