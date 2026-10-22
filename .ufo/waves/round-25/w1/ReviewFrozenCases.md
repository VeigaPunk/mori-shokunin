# ReviewFrozenCases: round-25 C2 frozen cases vs contract rules 1-7

Seat: MoriR25.ReviewFrozenCases (leaf reviewer, read-only). Lane: /home/vgpnk/Projects/shokunin/mori-shokunin.
Reviewed HEAD `6a92d5e` (contract amendment A2). This file is the only file written. No edits, no git or jj writes, omp not run, Bun not run.

## Result

- **Case disagreements: 0.** All 21 frozen `expect` objects agree with my independent derivation from rules 1-5 (191 field comparisons). The result also holds under amendment A2's added rule-1 conditions and BOM strip: none of them fires on any frozen config.
- **Regex check (rules 2-3): pass.** The literal text in the contract equals the tool's compiled patterns. Per-case match results agree with every expect. The real binary has one clamp site (100) and one default site (100).
- **Findings:** F1 and F2 (medium: the A2 wording gap, and the landed tool not yet implementing A2), F3 (medium, latent: the selftest can print PASS with nothing checked), F4 and F5 (low: rule-1 ambiguities), F6-F8 (informational).

## Scope and pinning

- Contract `.ufo/waves/round-25/contract.md`: C2 section lines 38-95; rules 1-7 at lines 52, 61, 66, 68, 71, 74, 77; declared after at 87-89; amendment A1 at 97-135; amendment A2 at 137-161.
- Fixture `tools/fixtures/mori-job-runway/cases.json`: 21 cases, blob `48df844a`, sha256 `7098b008...`.
- Tool `tools/mori-job-runway.py`: blob `7071ced9`, sha256 `08217582...`.
- HEAD moved during the review: `09f55b6` (tool landed) to `51ddd01` (A1) to `6a92d5e` (A2). Across all three, the C2 text (contract lines 38-95, identical by hash), the cases blob and the tool blob are unchanged.

## Method

1. Read C2 rules 1-7 and the fixture. Derived each case's configured state, clamp, setting_default, effective, verdict and exit from the rule text with my own Python, before reading the tool body. Compared every key present in each `expect`.
2. Ran Python `re` (3.14.8, bytes patterns, `finditer`) with the rule-2 and rule-3 regexes over each case's binary and over the real binary.
3. Re-derived all 21 configs under A2's added conditions with a separate checker written from the A2 text (contract.md:139-156). This is my reading of the amendment, not omp's behavior.
4. Read the tool for rule 7 and the regex literals. Probed its private helpers in memory with `sys.dont_write_bytecode = True`. No files written.
5. Ran `python3 -I -B tools/mori-job-runway.py --selftest` once: `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0.

## Per-case comparison

Clamp and setting_default columns show state, value, sites, then regex hits in brackets. The expect agrees for every row.

| id | case | configured | clamp | setting_default | effective | verdict / exit | agrees |
|---|---|---|---|---|---|---|---|
| J01 | host shape, comments | set 200 | found 100, 1 [100] | found 100, 1 [100] | 100 | RUNWAY_CLAMPED / 1 | yes |
| J02 | below clamp | set 50 | found 100, 1 [100] | found 100, 1 [100] | 50 | RUNWAY_AS_CONFIGURED / 0 | yes |
| J03 | equal to clamp | set 100 | found 100, 1 [100] | found 100, 1 [100] | 100 | RUNWAY_AS_CONFIGURED / 0 | yes |
| J04 | no async block | absent | found 100, 1 [100] | found 100, 1 [100] | 100 | RUNWAY_DEFAULT / 0 | yes |
| J05 | no file | absent | found 100, 1 [100] | found 100, 1 [100] | 100 | RUNWAY_DEFAULT / 0 | yes |
| J06 | async without maxJobs | absent | found 100, 1 [100] | found 100, 1 [100] | 100 | RUNWAY_DEFAULT / 0 | yes |
| J07 | non-integer `abc` | malformed | found 100, 1 [100] | found 100, 1 [100] | null | RUNWAY_UNKNOWN / 2 | yes |
| J08 | duplicate maxJobs | malformed | found 100, 1 [100] | found 100, 1 [100] | null | RUNWAY_UNKNOWN / 2 | yes |
| J09 | clamp pattern absent | set 200 | absent, 0 [] | found 100, 1 [100] | null | RUNWAY_UNKNOWN / 2 | yes |
| J10 | clamp sites differ | set 200 | ambiguous, 2 [100, 64] | found 100, 1 [100] | null | RUNWAY_UNKNOWN / 2 | yes |
| J11 | clamp sites equal | set 200 | found 100, 2 [100, 100] | found 100, 1 [100] | 100 | RUNWAY_CLAMPED / 1 | yes |
| J12 | maxJobs 0 floors to 1 | set 0 | found 100, 1 [100] | found 100, 1 [100] | 1 | RUNWAY_CLAMPED / 1 | yes |
| J13 | maxJobs under other block | absent | found 100, 1 [100] | found 100, 1 [100] | 100 | RUNWAY_DEFAULT / 0 | yes |
| J14 | no default in binary | absent | found 100, 1 [100] | absent, 0 [] | null | RUNWAY_UNKNOWN / 2 | yes |
| J15 | trailing comment, blank lines | set 200 | found 100, 1 [100] | found 100, 1 [100] | 100 | RUNWAY_CLAMPED / 1 | yes |
| J16 | config is a directory | unreadable | found 100, 1 [100] | found 100, 1 [100] | null | RUNWAY_UNKNOWN / 2 | yes |
| J17 | clamp spacing variant | set 200 | found 100, 1 [100] | found 100, 1 [100] | 100 | RUNWAY_CLAMPED / 1 | yes |
| J18 | higher clamp 300 | set 250 | found 300, 1 [300] | found 100, 1 [100] | 250 | RUNWAY_AS_CONFIGURED / 0 | yes |
| J19 | nested deeper maxJobs | absent | found 100, 1 [100] | found 100, 1 [100] | 100 | RUNWAY_DEFAULT / 0 | yes |
| J20 | flow mapping | malformed | found 100, 1 [100] | found 100, 1 [100] | null | RUNWAY_UNKNOWN / 2 | yes |
| J21 | default sites differ | set 200 | found 100, 1 [100] | ambiguous, 2 [100, 50] | 100 | RUNWAY_CLAMPED / 1 | yes |

Field comparisons by key: configured state and value 42; clamp state and value 42 plus clamp sites 2; setting_default state and value 42; effective 21; verdict 21; exit 21. Total 191. All agree.

## Regex check (rules 2-3)

- Rule 2 literal equals `CLAMP_RE.pattern` (tools/mori-job-runway.py:96-98): True.
- Rule 3 literal equals `DEFAULT_RE.pattern` (tools/mori-job-runway.py:100): True.
- Hits per case are in the table. J09 is the zero-hit clamp case and J14 the zero-hit default case. J10 and J11 are the multi-hit clamp cases. J21 is the multi-hit default case.
- Real binary (`/home/vgpnk/.local/bin/omp`, 256,702,432 bytes, sha256 `85d9daf3...`, read as bytes, not executed): clamp `[100]`, setting_default `[100]`. This matches the contract's live fact.
- The binary is not valid UTF-8 (decode fails at byte 26, 0x84), so bytes mode is the only run. The rule itself says "binary bytes". All case inputs are ASCII, so bytes and Unicode engine semantics cannot differ on them.

## Amendment A2 check

- Frozen configs: my A2 checker returns no hit on any of the 21 configs, and the BOM strip touches none. A2 leaves all 21 expects valid.
- Landed tool against the A2 text, 12 in-memory probes:

| A2 form | A2 text applied | landed tool at HEAD | agrees |
|---|---|---|---|
| second `async:` block | malformed (contract.md:144) | set 50, AS_CONFIGURED, rc 0 | no |
| `"async":` only | one occurrence, so clause does not fire; no exact header, so absent | absent, DEFAULT, rc 0 | same, see F1 |
| `async :` only | as above | absent, DEFAULT, rc 0 | same, see F1 |
| top-level `<<:` merge key | malformed (contract.md:145) | set 50, AS_CONFIGURED, rc 0 | no |
| tab in block indentation | malformed (contract.md:148) | set 50, AS_CONFIGURED, rc 0 | no |
| `---` document marker | malformed (contract.md:148-149) | set 50, AS_CONFIGURED, rc 0 | no |
| `maxJobs :` (space before colon) | malformed (contract.md:146) | set 50, AS_CONFIGURED, rc 0 | no |
| `"maxJobs":` (quoted key) | malformed (contract.md:146) | absent, DEFAULT, rc 0 | no |
| `maxJobs: 200#x` | malformed (contract.md:150) | set 200, CLAMPED, rc 1 | no |
| `maxJobs: "200"` | malformed (contract.md:150; also non-integer) | malformed, UNKNOWN, rc 2 | yes |
| BOM before `async:` | BOM removed (contract.md:152), then set 50 | absent, DEFAULT, rc 0 | no |
| `<<:` inside async block | malformed (contract.md:147) | absent, DEFAULT, rc 0 | no |

## Findings

### F1 - A2 misses a lone non-exact `async` key (medium)

- A2's first clause fires only on "more than one top-level line whose key ... is async" (contract.md:144-145). A file whose only async-like line is `"async":` or `async :` has one such line, so the clause does not fire. Rule 1's header search needs an exact `async:` (contract.md:52-53) and finds none, so the result is `absent`.
- Observed in memory on the landed tool: `"async":\n  maxJobs: 50\n` and `async :\n  maxJobs: 50\n` both give `absent`, `RUNWAY_DEFAULT`, exit 0. My A2 checker: no hit.
- Why it matters: A2's own finding is that exit-0 answers for forms omp reads differently are the failure to close (contract.md:139-141). [INFERENCE] YAML treats `"async"` and `async` as the same key, so omp probably reads the `maxJobs: 50` block. The tool would then report the default 100 with exit 0.
- Suggested fix for the planner: any top-level key that normalizes to `async` and is not exactly `async:` should abstain (malformed). Not edited.

### F2 - Landed tool does not implement A2 yet (medium while open)

- A2 says "The tool must abstain" (contract.md:141-142). The landed tool (blob `7071ced9`, unchanged since 09f55b6) does not. Nine of the twelve A2 probes disagree (table above). In each, the tool gives a number or the default with exit 0 or 1 where A2 requires abstention. Eight are exit 0; the glued `#` case is exit 1.
- Frozen 21: unaffected (A2 checker: 0 hits). The after-value `PASS 21/21` still holds for the landed tool.
- The supplementary file A2 names (`tools/fixtures/mori-job-runway/supplementary-cases.json`, contract.md:152-155) is absent at HEAD. `git ls-tree --name-only HEAD tools/fixtures/mori-job-runway/` lists only `cases.json`.
- Status: open until the planned tool change lands. After it lands, rerun the selftest and run the supplementary file with `--cases PATH`.

### F3 - Selftest can print PASS with nothing checked (medium, latent)

- `_selftest` uses `document.get("cases") or []` (tools/mori-job-runway.py:409). `expect = case.get("expect") or {}` (line 420). `_compare` iterates only the keys present in `expected` (lines 358-373).
- Observed in memory: `_selftest` with `json.load` patched to `{"cases": []}` (patch restored afterwards) printed `MORI_JOB_RUNWAY_SELFTEST: PASS 0/0` and returned 0. `_compare({}, {"verdict": "WRONG", "exit": 9}, "")` returned `[]`.
- Not triggered today: all 21 expects are populated. But exit 0 is not tied to N = 21, and the planned `--cases PATH` loader (contract.md:152-155) would inherit the same hole.
- Suggested fix: fail when the case count is not the declared N, and when an expect is empty.

### F4 - Signed integers are unpinned (low)

- Tool: `INTEGER_RE = ^[+-]?[0-9]+$` (tools/mori-job-runway.py:105), applied at line 206. Observed: `maxJobs: -1` gives set -1, effective 1, RUNWAY_CLAMPED, exit 1. `maxJobs: +200` gives set 200, CLAMPED, exit 1.
- Rule 1 says "unquoted decimal integer" and "anything else" is malformed (contract.md:52-60). A digits-only reading gives malformed, RUNWAY_UNKNOWN, exit 2, for both.
- A2 does not address signs, and no frozen case covers them.
- The tool's answer for `-1` matches what omp computes if omp accepts -1, because the binary's getter applies `Math.max(1, Math.floor(...))` (see V5). [INFERENCE] omp accepts -1; not verified.
- Suggested: state in rule 1 whether signs count as integers.

### F5 - An under-indented direct key is silently absent (low)

- Observed: `async:\n    enabled: true\n  maxJobs: 50\n` gives configured absent, RUNWAY_DEFAULT, exit 0. Code: tools/mori-job-runway.py:179-194 (child indentation and skip), 311-312 (verdict).
- Rule 1 defines direct children and deeper lines (contract.md:52-60) but not a line indented less than the first child. A2 does not cover it. A user who wrote `maxJobs: 50` gets an exit-0 default verdict.
- Suggested: abstain (malformed) when a block line is indented between column 0 and the first child's indentation. Not edited.

### F6 - Coverage gaps in the frozen set (informational)

- Unreadable binary: no case of 21. `_materialize` always writes the binary as text (tools/mori-job-runway.py:388-391). So rule 2/3 `unreadable` and rule 6 `binary_sha256: null` are never exercised.
- Assertions: `setting_default.sites` in 0 of 21 cases; `clamp.sites` in 2 (J01, J11). `schema`, `config_path`, `binary_path` and `binary_sha256` are never asserted, because `_compare` checks only `expect` keys (tools/mori-job-runway.py:421).
- Rule 4 branches not reached: configured `set` with setting_default `absent` (the default should not matter, so effective is still computed); configured `absent` with setting_default `ambiguous` (UNKNOWN); configured `absent` with clamp `ambiguous` or `absent` (UNKNOWN). Of the 64 (configured x clamp x setting_default) state combinations, 8 are reached.
- Rule 1 edges outside the frozen set: quoted integer, empty value, column-0 comment inside the block, header comment, non-UTF-8 config, BOM. Probed in memory: quoted and empty give malformed; a column-0 comment inside the block gives set 50 (correct, since it does not end the block); a header comment gives set 50 (correct).
- Rule 2/3 edges: two-argument `.get(a, b)` (no match), clamp value 0, and a default more than 300 characters after the id (no match).
- Suggested: put these in the A2 supplementary file. A2 says that file is not counted, so the frozen gate will not cover them.

### F7 - Wording (informational)

- contract.md:99-101 says "C2 is unchanged except wording." The C2 text (lines 38-95) is byte-identical across the freeze and HEAD. The only C2-facing addition is the F6 paragraph (contract.md:133-135), which sits outside rules 1-7. The statement is right in substance but overstated.
- contract.md:158-161 lists "`--config`/`PI_CONFIG_FILES` overlays" among things the tool does not read. The tool has its own `--config` option (tools/mori-job-runway.py:458). The text probably means omp's overlay flag; it should say so.

### F8 - Evidence status (informational)

- `runway-selftest.txt` is absent. contract.md:127-130 requires it after the last tool change. That change is still pending (F2), so it is not yet due.
- `runway-live-run.json` and `runway-live-run.meta` exist in the working tree but not in HEAD's tree. `git ls-tree --name-only HEAD .ufo/waves/round-25/evidence/` lists only `wave1-bind.json`. The C2 Sourced bullet says the live run is committed as evidence (contract.md:90-91).

## Verified (positive)

- V1 Pinning: cases blob `48df844a` at 7634be7, at HEAD, and in the working tree. The tool landed after the freeze (09f55b6 follows 7634be7).
- V2 Selftest: `PASS 21/21`, exit 0 in this review, at tool blob `7071ced9`.
- V3 Rule 7 mechanics: config `null` gives no file (`_materialize`, lines 376-392). `{"dir": true}` gives a directory (lines 382-383), which reads as unreadable. Each case runs inside a `TemporaryDirectory` (line 415). Exit is compared (line 419). Only `expect` keys are compared (line 421).
- V4 Regex literals: identical to the contract (see above).
- V5 Rule 4 formula at the consumer: in the omp binary, class `Xm` sets `this.#P = e.maxRunningJobs` in its constructor. Its getter `#R` returns `Math.max(1, Math.floor(t ?? v))`, where `t` is the function's value, `Math.min(100, XPe.get(R))` at the one clamp site. So the parenthetical in rule 4 holds. J12's floor-to-1 agrees with this.
- V6 Tool hygiene: stdlib only (tools/mori-job-runway.py:69-79). No subprocess or exec. Writes occur only in `_materialize`, which only `_selftest` calls, inside its temp directory.
- V7 Fixture hygiene: no duplicate JSON keys (checked with `object_pairs_hook`). All five keys are present in every case. All inputs are ASCII.

## Verification gaps

- LSP device not mounted: `xd://lsp` returned "No such tool. Mounted devices: ast_edit, debug." So no LSP definition, reference or diagnostic queries were possible. Caller claims rest on reading the file (`evaluate` 316-322, `_selftest` 413-421, `main` 496-504). Text search was used only for the regex literal lines.
- In-process probes import the tool and call private helpers (`_parse_config`, `_effective`, `_verdict`, `_compare`, `_selftest`). They depend on the current layout.
- Not exercised: the selftest FAIL output. It needs a failing fixture, and writing one is out of bounds.
- Regex engine: Python `re` over bytes, per the rule's "bytes" wording. No JS engine was run, and Bun was not invoked (reviewer rule). A2's Bun-based claims (tested against Bun 1.4.3) are not re-run.
- The live running-job count and any omp execution are out of scope (contract: frontier).

## Tools

- None installed or updated by this seat. Used: system `python3` 3.14.8, git (read-only subcommands), sha256sum, coreutils. RULES.md was read; it is the tooling directive already in context, so there is nothing to record.

## Checks for the main agent

- None required from this seat.
- After the planned tool change: run `python3 -I -B tools/mori-job-runway.py --selftest` (expect `PASS 21/21`). Run the supplementary file via `--cases PATH` once it exists; A2 says it is not counted. Re-verify F1-F5 at the new tool blob.
