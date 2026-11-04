# Mo86Sc01Scout — consumer map for the three round-86 surfaces

Read-only reconnaissance. No lane file was edited; the only write is this report.

## State read (siblings land while this runs)

- Lane HEAD `4eab48c0f721e5917f7611d51561894873a21ea4`; freeze commit `5e80229a450fa007d73ad0fb8bc3147e4adf5438`;
  entering revision `fec2b328a4c83e0c61bc09d70e254ca47d547d34`. `git status --porcelain` at read time:
  untracked `.ufo/waves/round-86/w1/`, `.ufo/waves/round-86/w1.ready.dispatched`,
  `.ufo/waves/round-86/evidence/sources-r86/` (siblings' work); no tracked modification.
- sha256 of the bytes actually read:
  - `.ufo/waves/round-85/count-c2.py` `497738932080b8044142e5f49a8a4f3151ab16b876d77d25a8e0771785f8b918`
  - `.ufo/waves/round-85/count-c3.py` `43ad71d8104df29f1be8e3e0cef20d485e35a5f3f70d4994d70adc67b88a2724`
  - `.ufo/waves/round-86/count-c1.py` `1912e87d767aabfaec4aa46992d6212ce9e1f8945792057c8ab9d89651d675f1`
  - `.ufo/waves/round-86/count-c2.py` `fcc1d805b877f6dabc99ba7082fb414fd0e3b4c900822a1fd9ef5285675f8b97`
  - `.ufo/waves/round-86/count-c3.py` `6b7fc2ddb560f58cb155605510fbf4e3f3801d1766050219abdec2ca5c5668c9`
  - `corpus/evidence/drift-classification-r82.txt` `12b4b0779b118e93d0755ff23169dd6eb33646c55717d6506f93f94b355a498a`
  - `tools/mori-receipt-complete.py` `135cb3f0…`, `tools/mori-control-receipt.py` `531d6b52…`,
    `.ufo/waves/round-85/make-receipts.sh` `7fd5e043…`
- Method note: this seat's toolset has **no `lsp` device mounted**, so symbol tracing below is
  whole-file reading of each parser plus text grep for occurrences. No LSP claim is made; a grep
  hit count is reported as a grep count, not as semantic proof. (One `__pycache__` written by a
  pure import for a read-only count was removed; tree restored.)

## Headline risks for the L1

| # | Finding | Surface | Verdict |
|---|---|---|---|
| R1 | `r86/count-c2.py` requires the amended r85 subject to be named literally `def replay_receipt(` (`count-c2.py:325`) | 1 | **breaks:** subject missing that exact symbol name |
| R2 | `r86/count-c2.py` runs the subject with `--scratch` in both modes (`:335`, `:348`); r85 `count-c2.py` argparse has no `--scratch` (`:282-285`) | 1 | **breaks:** argparse exit 2 → `subject=run line=-` |
| R3 | The C1 anchor `all(tokens == first for tokens in token_lines[1:])` occurs **0** times; live form is `all(tokens == token_lines[0] …)` (`count-c3.py:193`) | 2 | **needs-review:** the arm must introduce `first` before any mutant is anchored |
| R4 | `r86/count-c1.py` requires the amended r85 count-c3 `--selftest` to print **exactly 26** passing arms and six `PASS <label>` lines (`:66`, `:113-118`) | 2 | **breaks:** any other arm count, or changed text on the existing 20 |
| R5 | If a `value-changed` row in the classification is relabelled to absorb a contradiction, all four classification counters lose `name_agree`/`derived` | 3 | **breaks:r82/r83/r85/r86 met** |
| R6 | SKILL registry row 19 and the r85 capability rows state the old predicates/tallies | cross | **needs-review:** append-only supersession, never edit |

---

## Surface 1 — `.ufo/waves/round-85/count-c2.py` (receipt grammar)

### 1a. Receipts in the lane that carry the `# cmd:`/`# rev:`/`# counter-sha256:` header

| Receipt (absolute path) | Header lines | Body | Who parses it |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/evidence/after-r85.txt` | 1 `# receipt:`, 2 `# cmd:`, 3 `# rev: 25a74d4c…`, 4-6 three `# counter-sha256:`, 7 `# limits:`, 8 `# ---` | 9-14 | r85 `count-c2.py:32-39` (population row 1); r86 `count-c2.py:39` (legacy) |
| `/…/.ufo/waves/round-85/evidence/record-sweep-r85.txt` | 1-6 (cmd 2, rev 3, sha 4, limits 5, sep 6) | 7-8 (`RECORD_SWEEP`, `rc=0`) | r85 `:34-36`; r86 `:40` (legacy) |
| `/…/.ufo/waves/round-85/evidence/claim-sweep-r85.txt` | 1-6 | 7-8 (`CLAIM_SWEEP`, `rc=0`) | r85 `:36-38`; r86 `:41` (legacy) |

Older-format receipts carry `# rev:` but no `# cmd:`/`# counter-sha256:`; they are outside the
graded population and no counter reads them: `.ufo/waves/round-45/evidence/control-c1.txt:6`,
`control-c2.txt:5`, `control-c3.txt:5`, `control-r44-c1.txt:5`, `control-r44-c2.txt:5`,
`registry-audit-all.txt:3`, `witness-r44-c3-tmpdir.txt:6`,
`.ufo/waves/round-44/w1/ExecC1STip.md:123`. — *none*.

Fleet scan (`/home/vgpnk/Projects/shokunin/.ufo/reports/**`): **no** file carries `# cmd:`,
`# counter-sha256:` or `# replay:` header lines. Only prose describing the r85 receipts:
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-85/mori.md:46,73,77,79`. — *none*.

### 1b. Parsers/writers and whether a `# replay:` addition breaks them

| Consumer (absolute path) | Lines that parse | Effect of `# replay: required` / `# no-replay: …` | Verdict |
|---|---|---|---|
| `/…/.ufo/waves/round-85/count-c2.py` | header split before first `# ---` (`parse_receipt` 58-114); only `HEADER_ANY` 45 = `cmd|rev|limits` and `SHA_ANY` 46 are recognised in the loop 81-96; unknown `#` lines fall through silently; missing/duplicate checks 98-101 | ignored; `replay` cannot match the `rev` alternative (prefix `rep` ≠ `rev`) | **none** (parser) |
| `/…/.ufo/waves/round-86/count-c2.py` | `REPLAY` 46, `NORE` 47, `header_fields` 75-117 (`missing-replay` added 112-113), legacy exemption 208-209, population 38-44, replay execution `replay_body` 139-153 + `export_rev` 119-137, subject gates 324-325, 335, 341, 348-353 | this counter *requires* the new header on its two r86 receipts and exempts the three legacy ones | **breaks:** see R1 (literal `replay_receipt`) and R2 (`--scratch`) |
| `/…/tools/mori-receipt-complete.py` | `FAILED_RE` 77, per-line scan 90-91, token charset 74-77 | header lines are scanned too; inert **unless** the `# cmd:`/`# no-replay:` text contains `failed=<token>`, which would be graded as an anchor line | **needs-review:** keep `failed=` out of every header value |
| `/…/tools/mori-control-receipt.py` | `is_comment` 58-59, `is_command_line` 62-70 (comments excluded 64-65), `CLAIM_RE` 52, `split_sections` 86-89 (`## ` only), `analyze_text` 97-103, `check_receipts` 115-155 | `# replay:`/`# no-replay:` are comments: they can neither bind nor break a section | **none** (note: these three receipts would read *unbound* under this tool because body `rc=0` matches `CLAIM_RE` and there is no `$ ` line — pre-existing, unrelated to replay) |
| `/…/.ufo/waves/round-85/make-receipts.sh` | writes header blocks 161-169, 175-181, 187-193; `sha_at_rev` 100-102; runs counters 131-132 | no parser; rerunning it would regenerate the frozen bodies (do not rerun) | **none** |
| `/…/tools/mori-claim-sweep.py`, `/…/tools/mori-record-sweep.py` | no `cmd:`/`counter-sha256`/receipt code (grep: 0) | they are the *subjects* whose stdout is a receipt body (receipt lines 2 of each) | **none** |
| `/…/tools/mori-pin-check.py` | receipt only in docstring/fixture strings 5, 1424-1465 | no header parsing | **none** |
| `/…/tools/mori-counter-win.py`, `/…/tools/mori-anchor-check.py` | prose only (`:21,57,61,108` / `:23`) | no header parsing | **none** |

Semantic (not parser) note: adding `# replay: required` to a **legacy** r85 receipt would defeat it.
`after-r85.txt:2` runs the two counters with no `--repo`; both default `--repo` to
`dirname(__file__)/../../..` (`count-c1.py:305-306`, `count-c3.py:289-290`), and r86 `export_rev`
(119-137) writes only the `/`-bearing tokens that exist at `# rev:` — no `.git` — so the replay
would exit 2 (setup). `record-sweep-r85.txt:2` / `claim-sweep-r85.txt:2` run `--root .` against that
same non-repo export. The frozen `legacy` label is therefore mechanically necessary, not only
historical. — *needs-review only if someone proposes adding replay to the three legacy receipts.*

Replay-export caveat for the two new `required` receipts: `export_rev` (r86 `count-c2.py:119-137`)
writes only tokens that contain `/` **and** exist at the receipt's `# rev:`; absolute tokens (e.g.
`--repo /home/vgpnk/...`) are silently skipped, and the replay command is then executed in that
export with the skipped argument unchanged (`replay_body` 139-153). So a `required` receipt whose
`# cmd:` names an absolute `--repo` is really graded against the live lane at `rev`, while a
command that omits `--repo` is graded against a non-repo export and fails on rc. The two r86
receipts must therefore spell their `# cmd:` exactly as they intend it — **needs-review** for the
C2 seat, not a parser defect.

Documentation consumers of the grammar (would go stale if the grammar is extended without a
superseding row): `/…/corpus/knowledge/receipt-provenance-r85.md:59-62,67-75,85-86`;
`/…/corpus/README.md:897-901`; `/…/SCORECARD.md:4380`; `/…/PROVINCE.md:657-660`;
`/…/SKILL.md:1371`; `/…/LOG.md:5274`; the header template in
`/…/.ufo/waves/round-85/build-w1-spec.py:164-167`; and the quoted template in
`/…/.ufo/waves/round-85/w1/Mo85E02Receipts.md:80-84` (historical seat report — no parser).

---

## Surface 2 — `.ufo/waves/round-85/count-c3.py` (helpers and executors)

### 2a. Helper inventory and copies

Definitions in the surface file: `baseline_names:58`, `derive:68`, `live_delta:83`,
`drift_tokens:107`, `classifications:116`, `subject_signal:133`, `reconcile:149`, `observe:168`,
`observe_three:187`, `subject_run:197`; constants 36-40, `OBSERVATIONS:50`; the stability
expression is inline at 191-193; the `met` expression at 357-358.

Anchors the r86 C1 counter needs (occurrence counts measured with `grep -c -F` over the current
bytes): `all(rc == 1 for rc in rcs)` 191 → 1; `if word == "agreed":` 160 → 1;
`subject_tokens == len(own_tokens)` 357 → 1; `fields.get("verdict") == "met"` 342 → 1;
`all(tokens == first for tokens in token_lines[1:])` → **0** (live text at 193 compares to
`token_lines[0]`). `controls-r86.txt:15,31-36` already records `C3-03-order occurrences=0`.
`stability` as a named helper does not exist at this revision (contract requires its extraction).

Copies (no imports anywhere; the file names are hyphenated and the only `importlib` load among the
r8x counters is `r84/count-c3.py:120-121` loading `r83/count-c2.py`):

- `/…/.ufo/waves/round-82/count-c2.py`: 55, 65, 79, 122 (older shape, no `live_delta`)
- `/…/.ufo/waves/round-83/count-c2.py`: 66, 76, 90, 123, 169
- `/…/.ufo/waves/round-85/count-c3.py`: 58, 68, 83, 107, 116, 133, 149, 187, 197
- `/…/.ufo/waves/round-86/count-c3.py`: 53, 63, 86, 96, 101, 110, 119, 139, 148, 161, 188 —
  independent copy; its `stability` takes three arguments (101) and drops volatile field names,
  and its `reconcile` has a different signature (188). No import edge; a **name collision only**,
  relevant to grep-based review, not to behaviour.

### 2b. Executors (things that run the file or depend on its output shape)

| Executor (absolute path) | Lines | What it needs from this file | Verdict |
|---|---|---|---|
| `/…/.ufo/waves/round-86/count-c1.py` | `SUBJECT` 32, `MUTANTS` 37-52, `ARM_LABELS` 53-61, `TARGET` 65, `TARGET_ARMS` 66, `selftest_run` 75-87, `arms_ok` 113-118, `grade` 120-174 | copies the file at R into scratch and runs **only** `--selftest`; needs exactly 26 passing arms and all six `PASS <label>` lines | **breaks:** see R4; also any changed byte-count anchor (R3) |
| `/…/.ufo/waves/round-85/make-receipts.sh` | 131-132 (body 1), `sha_at_rev` 100-102 | runs `count-c1.py` then `count-c3.py` at `<rev>` to produce `after-r85.txt`; bindings are resolved at `25a74d4c` (receipt 4-6) so later edits do not invalidate them | **none** (do not rerun; it would rewrite a frozen body) |
| `/…/SKILL.md` registry row 19 | 1371 (full line, 2365 chars) | names the file and pins the r85 target `C3=met observed=3 aa=stable own_tokens=N subject_tokens=N unmatched=0 unnamed=0`; self-test cell pins revision-scoped tallies `C1=18 / C2=15 / C3=19` "measured … at `ab260865`" (current bytes are 18/20 for C2/C3) | **needs-review:** supersede, do not edit; reconcile the already-stale 15/19 |
| `/…/SCORECARD.md` capability row | 4381 | "runs … three times … **20 detector arms** `pass=20 fail=0`" | **needs-review:** stale at 26 arms |
| `/…/PROVINCE.md` | 662-666 | describes the three-run observation and the file as evidence-only instrument | **needs-review:** prose still true; no tally |
| `/…/corpus/lessons/round-85-verifier-spotcheck.md` | 65 (sha `43ad71d8…` MATCH), 91 (`pass=20`), 97 (after body), 144 ("18/18/20 detector arms") | historical, append-only | **none** (historical reading; do not rewrite) |
| `/…/LOG.md` | 5297-5302 | round-85 record of the instrument | **none** |

CLI compatibility: `--selftest`, `--scratch`, `--repo`, `--fleet-root` exist in `main` 286-300; the
r86 C1 counter passes only `--selftest` (75-87), so no new flag is needed here. — *none*.

---

## Surface 3 — `corpus/evidence/drift-classification-r82.txt`

Shape at the read bytes: 8 header lines (1-8, incl. `# Snapshot:` 6, `# Snapshot-sha256:` 7,
`# As-of:` 8) and 64 `DRIFT_CLASS` rows (9-72). 19 rows are `value-changed`
(35, 55-72); **14** are bare-key rows (`+attribution` 35; `-attribution` 59; `-example` 60;
`-rowb_files` 61; `-subject_commits` 62; `-window` 63; `age_s` 65; `basis` 66; `boot` 67;
`io_avg_unavailable` 68; `launch_epoch` 69; `obs` 70; `round` 71; `volatile_fields` 72) and 5 are
name-shaped (`-FINDING:` 55-57, `-SURFACE:` 58, `HEADER` 64) — matching the frozen `value_rows=14`.

### Readers

| Reader (absolute path) | Lines | What it extracts | Verdict under a value-channel reading |
|---|---|---|---|
| `/…/.ufo/waves/round-82/count-c2.py` | `CLASSES` 40, `CLASS_LINE` 44, `classifications` 79, call 153; fixtures 235, 257, 270 | token + class only; derives names from the baseline | **none** if bytes untouched; **breaks:name_agree/derived** if a row is relabelled |
| `/…/.ufo/waves/round-83/count-c2.py` | `CLASSES` 46, `CLASS_LINE` 50, `classifications` 123, call 258; fixtures 347-351, 404-405 | same | **none** / **breaks** as above |
| `/…/.ufo/waves/round-85/count-c3.py` | `CLASSES` 39, `CLASS_LINE` 43, `classifications` 116-131, call 349; `live_delta` consumes `stated` 94-105; fixture 247-248 | same; `stated` also supplies the snapshot class | **none** / **breaks** (its `agreed`/`class-changed` outcomes move) |
| `/…/.ufo/waves/round-86/count-c3.py` | `CLASSES` 34, `CLASS_LINE` 41, `classifications` 119-137, call 328; fixtures 219-220 | same, then the value channel reads **baseline + live report**, never this file's values | **none** / **breaks** (`derived`/`name_agree` at 342) |
| `/…/.ufo/waves/round-84/count-c3.py` | `SUBJECT` 34 + `importlib` 120-121 | transitive: executes the r83 counter, which reads the file | **none** / **breaks** transitively |
| Docs | `SCORECARD.md:13,60`; `PROVINCE.md:620`; `LOG.md:5086,5148`; `corpus/lessons/round-82-verifier-spotcheck.md:87`; `corpus/lessons/round-83-verifier-spotcheck.md:60,63`; `corpus/lessons/round-82.md:180` | prose/rows quoting 64/45/19 and the file path | **needs-review:** the r86 finding (2 contradicting rows) is a *report* fact; these rows must not be "fixed" by editing the classification |

The value channel itself (r86 `count-c3.py`): `atom_map` 86-94, `stability` 101-108, `value_body`
139-146, `value_verdict` 148-159, `reconcile` 188-204, `VALUE` print 336-337, `met` 342-344; it
reads `BASELINE` 35 and the live full report (`observe … drift=False` 161-186). No reader of the
classification file parses values, so **no reader is affected by the capability itself** — only by
an edit to the file.

Adjacent observations (evidence for the L1/falsify seat; outside my surface):
- `r86/count-c3.py:8` docstring says `value_rows=19`; `TARGET:44` and `met:343` require 14. The
  code is self-consistent with 14 (measured by pure import over the committed bytes:
  `derived=64 name_agree=64 value_rows=14`, `verdicts=14`); only the docstring is stale.
- `.ufo/waves/round-86/evidence/controls-r86.txt:50-53` prints **two** `VALUE` lines
  (`round absent`, `volatile_fields absent`) and `contradicting=2`, but the committed counter prints
  one `VALUE` line per value row (`:336-337`; `reconcile` appends 14 verdicts, `verdicts.append`
  201) and `contradicting` counts only `equal` verdicts (`:202`). Two `absent` verdicts cannot
  yield `contradicting=2`. That control section is not the full/consistent output of the committed
  bytes — flag for the falsify seat.

---

## Surface 4 — sibling-lane overlap (read-only; no sibling file was modified)

| Lane / path:lines | Rule it holds | Relation to mori r86 |
|---|---|---|
| chousa `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/receipt-pin.py:2-20,24-27,50-60` | `REVISION=`/`EXIT=`/`SHA256=` header, committed-blob digest; docstring: header consistency is **not** execution authenticity | **complements** (different header format; no body-vs-command check) |
| chousa `/…/chousa-shokunin/corpus/knowledge/receipt-identity-r65.md:29` | states the gap: "There is no command/body binding … Replaying a valid header with fabricated output can pass." | mori's P-C2 closes exactly this in the mori receipt family — **complements**, no conflict |
| chousa `/…/corpus/knowledge/receipt-expectation-digests-r40.md:5-20` | expectation-file sha256 binding | **complements** (bytes, not body) |
| chousa `/…/corpus/knowledge/receipt-verifier-subject-r39.md:5-28` | verifier sha + subject-counter sha, fail-closed `FAMILIES` | **complements** |
| kotodama `/…/kotodama-shokunin/tools/check-receipt-seq.py:2-38` | header equality (stamped/evaluated/measured/tree/counter sha), `--lands` tree reads, `--topo` carrier parentage | **complements**; different keys, no replay |
| tsukuroi `/…/tsukuroi-shokunin/tools/check-revision-binding.py:1-45` and `/…/check-cited-receipts-r62.py:1-30` | revision-gate binding; cited-receipt landing | **complements** |
| all lanes, `*-shokunin/tools/` + `*-shokunin/corpus/knowledge/` | `value-changed`: **0 hits outside mori**; `# replay: required|none`: **0 hits outside mori** | mori's vocabulary/header are lane-local: no duplicate, no conflict |
| mori itself `/…/tools/mori-evidence-loss.py:36` | `ALLOWED_CLASSES = {"census-regression","live-state"}` (r20 register vocabulary) | distinct from `value-changed`; no reader conflates them |

---

## Cross-cutting landing checklist (what a landing must not forget)

1. `r86/count-c2.py` hard contracts on the amended r85 subject: literal `def replay_receipt(`
   (`:325`), `--scratch` accepted in selftest and real mode (`:335`, `:348`), exactly 21 arms and
   three `PASS` labels (`:30-31`, `:341`), target line equality (`:32-34`, `:353`).
2. `r86/count-c1.py` hard contracts on the amended r85 count-c3: exactly 26 arms, six specific
   `PASS` labels, and all six anchors occurring exactly once (`:32`, `:37-66`, `:113-118`); the
   `C3-03-order` anchor must be introduced (R3).
3. Registry/report rows to supersede **append-only**: `SKILL.md:1371`; `SCORECARD.md:4380` (18 arms),
   `SCORECARD.md:4381` (20 arms); `PROVINCE.md:657-666`; the grammar index row
   `corpus/README.md:897-901`.
4. Do not edit `corpus/evidence/drift-classification-r82.txt` to make a contradiction disappear
   (R5), and do not rerun `.ufo/waves/round-85/make-receipts.sh` (it rewrites frozen receipt
   bodies).

## Remaining unknowns

- Whether `tools/mori-pin-check.py --baseline-rev` treats the revision-scoped tallies in
  `SKILL.md:1371` as live pins or resolves them at `ab260865`; only that tool's own baseline run can
  settle it. Stated as an open question, not a claim.
- I did not execute any census or counter run: every line number is from committed/working bytes at
  the state above. A sibling landing after 09:2x -03 may move hashes; re-check sha256 before citing.
