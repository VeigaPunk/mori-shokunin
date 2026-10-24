# ContractReview: round 20 C2 frozen contract and oracle review

Seat: MoriR20.ContractReview (leaf reviewer, no subagents).
Frozen inputs read, unmodified: `.ufo/waves/round-20/contract.md` (C2 at lines 49–117) and `.ufo/waves/round-20/frozen/c2-expected.json` (14 cases, lines 7–20). `git status --porcelain` on both is empty; HEAD is e4d9384; sha256 prefixes `0984806922da727a` (c2-expected.json) and `2bbe9d56acddca6d` (contract.md).
Every refinement below is labelled **co-evolved** and is a proposal. Frozen bytes are untouched.

## 0. Bounds, method, disclosures

- Writes: this file and `.ufo/waves/round-20/build/ContractReview/c2-coevolved-cases.json` (22 proposed cases, parsed with `jq`). No edits to `tools/`, `frozen/`, `contract.md`, lane files, or git/jj state. No census, build, selftest, or install. No subagents.
- `tools/mori-wave-settlement.py` does not exist: `git cat-file -e 2061780:tools/mori-wave-settlement.py` returned `fatal: path … does not exist`, rc 128, and it is absent in the worktree. There was nothing to run.
- Analysis was read-only: Python stdlib in the eval kernel walking `<lane>/.ufo/waves/**` for the 21 `*-shokunin` lanes (fleet-root `.ufo/waves` only listed), `jq` (`jq --version` reports jaq 3.1.1), and read-only `git log/status/cat-file`. Fleet-wide `**` globs timed out at 5 s, so I used `os.walk`.
- Disclosure: my first unscoped `grep` over `mori-shokunin/.ufo/` returned matched lines from `.ufo/interactive-sessions/20261015T050057Z/*.jsonl` (retained interactive transcripts) and from `.ufo/worktrees/`. I did not open those files on purpose and I used none of that text. Every fact below comes from lane wave files, the frozen contract and oracle, and two tool headers.
- Live tree: the fleet writes while I review, so counts are snapshots taken 2026-10-21 between about 10:27Z and 10:41Z. Between my passes the payload count went from 179 to 196 (a new `tabi/.ufo/waves/round-20/final-clones/ExecCounter` tree appeared), and kagi `round-25/build-dispatch.json` went from 88/88 missing to 16/88 present. Re-measure at acceptance.

## 1. Summary

Severity: H = yields a wrong verdict on real data or makes a frozen claim untestable. M = needs a pinned rule. L = wording.

| # | Sev | Finding | Refinement |
|---|---|---|---|
| H1 | H | `present` (size > 0) is met by the protocol's own `STATUS: started` first write. The live mori r20 wave is literally `settled` (76/76), and 18 of those reports are still exactly the marker. | CE-2 |
| H2 | H | Filenames do not indicate dispatch (`validation` covers executed payloads; `preview` and `undispatched` cover never-dispatched ones). "Unsettled" reads as "seats failed" even when nothing was dispatched. | CE-3, CE-4 |
| H3 | H | Discovery under `.ufo/waves/**` counts nested lane clones and schema-only records as waves. | CE-5, CE-6 |
| H4 | H | State precedence is unstated. Zero-member and `resumeSends` cases are unhandled. | CE-1, CE-15 |
| H5 | H | Trailer rule: the body key is unnamed, "LAST line" is ambiguous, and real clone bodies end with a non-trailer line (96 tasks). | CE-8 |
| H6 | H | Symlink semantics are internally inconsistent. The rules leave the status for a symlink undefined, and the frozen `not_followed` has no output key. Symlinks occur in the fleet. | CE-7 |
| H7 | H | Oracle keys do not match the output schema (`missing` as count vs list; `members`, `totals`, `reports_present` undefined). The `no_vocab` substring check cannot be guaranteed on fleet runs, because member names containing `dead` reach `missing` lists whenever those members are not present. | CE-9, CE-11, CE-13 |
| M1 | M | Exit codes: zero waves and all-unreadable both exit 0. A missing `.ufo/waves` is unspecified. `--selftest`, `--out` and `--fleet-root` failures are unspecified. `unavailable` gives exit 1 here, while mori-dispatch-ledger gives exit 2 for its analogue. | CE-10 |
| M2 | M | Misroot precedence and fleet-copy checks are unstated. | CE-16 |
| M3 | M | The relation to `tools/mori-misroot-sweep.py` and `tools/mori-dispatch-ledger.py` is not stated. | CE-17 |
| M4 | M | "Byte-identical" needs a pinned serialization and a snapshot identity. `--out` under `.ufo/waves` changes the next scan. | CE-11, CE-12 |
| L1 | L | The live demonstration must name `round-19/wave1-run.json`. The 16-of-64 figure reproduces now. | L1 |

## 2. Evidence base

Payload = regular JSON whose top-level `schema` is `ufo-swarm-wave-dispatch-v1`. At pass 3 (about 10:40Z) there were 196 payloads: 193 with a `taskCall` object and 3 schema-only records.

- Task checks over the 193 payloads (literal rules, trailer = last non-blank line): present 10,599; missing 1,611; misrooted 1; unparsed 96; empty 0; unsafe 0. The 96 unparsed are three copies of one 32-member rehearsal payload whose bodies end with a `| godspeed` line after the trailer.
- Body key: every observed task uses `task`. `prompt` never occurs. `taskCall: null` occurs in 0 payloads. Non-empty `resumeSends` occurs in 0 (the payload `note` says "one hub send per resumeSends entry").
- Never observed: CRLF, a trailing newline in a body, duplicate trailer paths (0 of 193 payloads), duplicate or missing member names, and suspicious characters in missing trailer paths (0 of 1,600 checked in that pass). Directory or FIFO report paths were not observed either.
- Misroot: one real instance. Souji `round-20/final-dispatch.json` names `.ufo/waves/round-20/final/AuditCase07.md`. That file is absent in the lane and is a regular file at the fleet root. The wave is partial (63 present, 1 misrooted).
- Registry evidence over the 193 payloads (`registry.path` read): every declared member has a non-null agentId in 170 payloads; some do in 3; none do in 15; the registry file is absent in 5.
- Unreadable JSON under waves: 45 files, all JSONDecodeError, none containing the dispatch schema text.
- Symlinks under waves: 20 files and 12 directories. Three are symlinked `*.json` (`…/case-symlink/cases/alias.json → ../target.json`, in tabi clones). Self-referential `symlink-loop` entries exist in kaidoku `round-18/verify/scratch-custody/…` and `round-19/verify/scratch-custody/…`.
- Lanes with no `.ufo/waves`: audio, game-dev-2d, game-dev-3d, kotoba, kotodama. Lore has 1,102 JSON files and 0 payloads. The gen-wave1 GtLane list omits lore, which has no payloads, so the payload inventory is unaffected.
- Frozen oracle exit values are 0 and 1 only. No frozen case exercises exit 2, `--selftest`, `--out`, or a missing `--fleet-root`.

## 3. H1: the start marker satisfies `present`

- `contract.md:74–75` defines `present` as "regular non-symlink file, size > 0". The problem statement (`contract.md:51–54`) is about *retained reports*.
- The seat protocol makes every seat write `STATUS: started` as its first tool call. That instruction is in the shared `taskCall.context` (2,737 characters) of `round-20/wave1-run.json`. It appears there, and in 0 of 76 task bodies.
- Measured at 10:40:40Z with literal rules: all 76 trailer paths are regular files with size > 0, so the wave is `settled` and exits 0. Within them, 18 files are exactly the marker (15–16 bytes, mtime 12.8–13.8 minutes old, so not rewritten since dispatch at 10:26:45–10:27Z). The other 58 have content (1,657–26,955 bytes, mtime 0–13.2 minutes old).
- [INFERENCE] The 18 are either long-running seats or stalled ones. The file alone cannot tell which. An earlier pass with a looser predicate counted 40 marker-like files. I discard that figure as a classifier error.
- Refinement: CE-2.

## 4. H2: "dispatched" and name-based readings

"Spawn record" below means the registry at `registry.path` holds non-null agentIds (see CE-3).

| Payload (lane path) | Name hint | Members | Spawn record | Literal state (pass 3) | Adjacent evidence | Reading |
|---|---|---|---|---|---|---|
| mado `fleet-round-1-interactive/dispatch-preview.json` (wave `mado-fleet-1-interactive`) | preview | 32 | registry file absent | unsettled 0/32 | sibling `validation.json`: `dispatchCalls: 0`, `registryPersisted: false`, status `validated_spec_only_dispatch_blocked` | never dispatched |
| revenger `fleet-round-1-interactive/rendered-undispatched.json` | undispatched | 32 | registry file absent | unsettled 0/32 | sibling `routing-assessment-run.json`: `ROUTING_CONTRACT BLOCKED … planned=32 dispatched=0` | never dispatched |
| tabi `round-20/final-clones/{ExecFixtures,ExecFrozen,ExecCounter}/.ufo/rounds/fleet-round-1-interactive-20261015/wave.dispatch.json` (×3) | clone | 32 each | registry absent | unavailable (32 unparsed: `| godspeed` after trailer) | same directory, `wave-validation.json`: `dispatch_calls: 0`, `registry_persisted: False`, `run_not_invoked` | rehearsal copy; never dispatched |
| same directories, `wave-validation.json` (×3) | validation | no `taskCall`, no `wave` | n/a | not a wave | `dispatch_calls: 0` | validation record reusing the dispatch schema id |
| souji `round-20/w1-dispatch.json` (`souji-r20-w1`) | none | 64 | every member has agentId | unsettled 0/64 | none | spawn record present, zero reports |
| tabi `round-12/w1/dispatch.json`; `round-13/w1/dispatch.json` | none | 32; 32 | every member has agentId | unsettled 0/32 each | none | spawn record present, zero reports |
| kama `round-19/falsify/dispatch.json`; `round-21/build/dispatch.json` | none | 66; 86 | registry present, no agentIds | unsettled 0/66; 0/86 | `wave: null` | spawn unknown |
| kake `round-21/wave1-validation.json` | validation | 64 | every member has agentId | settled 64/64 | none | executed; name misleading |
| tabi `round-15` to `round-19` `{w1,w2}/validation.json` (×10) | validation | 32–86 each | every member has agentId | settled 6, partial 4 (e.g., round-17 w2 52/78) | none | executed |
| tameshi `round-20/validation-current.json` | validation | 72 | every member has agentId | partial 27/72 | none | executed in part |

Reading:
1. Names carry no signal. Of the 14 non-nested payloads whose names contain `preview`, `undispatched` or `validation`, 2 were never dispatched and 12 were executed. The three nested schema-only `wave-validation.json` records are also validation-named, and they were never dispatched either (`dispatch_calls: 0`), so the word cuts both ways.
2. The seven non-nested unsettled payloads hold 344 declared members with zero reports. Of those, 128 have spawn records (souji, tabi r12, tabi r13). Those are the real C2 signal: the seats were dispatched and reported nothing. 152 have a registry without agentIds (kama r19, r21), so spawn is unknown. 64 were never persisted (mado, revenger).
3. Spawn records are not universal. Seven settled payloads have no agentIds at all. For example, kaidoku `round-17/wave1-dispatch.json` has 78/78 reports present and its registry has no agentIds. An absent spawn record must therefore never be printed as "not dispatched".
4. Today's output would print "unsettled, exit 1" for the two never-dispatched payloads. A reader would take that as "32 seats failed to report" for each. That implication is what §6 removes.

## 5. H3: discovery scope

- `contract.md:64–65` says "every regular `*.json` under `<lane-root>/.ufo/waves/`". The walk therefore includes nested lane roots. At pass 2 there were 51 dispatch-v1 files under `tabi/.ufo/waves/round-20/final-clones/*/.ufo/…`, which are copies of tabi rounds 12–19.
- Real duplicate wave names within one lane (not nested): `tabi-round-19-w2` (`round-19/w2/dispatch.json` and `round-19/w2/validation.json`), `tameshi-r20-w1` (`run1.json` and `validation-current.json`), and `kengaku-r26-build` (`build-dispatch.json` and `build-registry-rebuild.json`). Identity must be `dispatch_path`, not `wave`. Sixteen kama payloads carry `wave: null`.
- The three schema-only records are neither waves nor counted anywhere in the contract.
- `mori-shokunin/.ufo/waves/round-17/fixtures/seat/NonJsonlIgnored/other.json` is a fixture inside the scan root. It is counted as `unreadable_json`.

## 6. How output should avoid implying dispatch

The short answer: a dispatch-v1 file is a declaration of members. Only a spawn record shows that a member was spawned. The output should therefore do six things.

1. Say "declared" for the file's contents. Reserve "dispatched" for `spawn_record = ids-recorded`. Never print "dispatched", "seat", "failed", "dead" or "missing seat" for a wave that lacks that record.
2. Keep the frozen `state` values and add `spawn_record` plus `declared_only` (CE-3). A never-dispatched wave still reads `unsettled`, because the frozen `none-present` case needs exit 1 and has no registry. The annotation is what tells the reader the wave is declared-only.
3. Never let filenames (preview, undispatched, validation, dry-run, not-dispatched) change the state, the wording, or the exit (CE-4).
4. Split the totals: `unsettled_spawn_recorded` (the C2 signal) and `unsettled_declared_only` (a review queue). Do not merge them into one "unsettled" count.
5. Keep the exit code unchanged by default, since the frozen cases pin it. Offer an opt-in flag, default off, that excludes declared-only waves from the exit computation. L1 decides whether to adopt it.
6. Identify waves by `dispatch_path` (relative, POSIX). `wave` may be null. Stdout is the same JSON as `--out`, and any prose uses the same vocabulary.

Schematic shape (values are placeholders):
```json
{"dispatch_path":"<lane-relative path>","wave":null,"state":"unsettled","spawn_record":"registry-file-absent","declared_only":true,"members":32,"counts":{"present":0,"started":0,"empty":0,"missing":32,"misrooted":0,"unsafe":0,"unparsed":0},"missing":["<member>","..."]}
```

## 7. Frozen contract: ambiguities and refinements

Line numbers refer to `contract.md`.

| Line | Statement | Ambiguity or untestable point | Refinement |
|---|---|---|---|
| 64–67 | Discovery: every regular `*.json` under `.ufo/waves/` | Recursion reaches nested `.ufo` roots (§5). Symlinked JSON and symlinked directories are dropped silently and not counted. Hidden directories and the case of `.json` are unstated. If `.ufo/waves` itself is a symlink, the scan finds zero waves and exits 0. | CE-6, CE-7 |
| 64–65 | Top-level `schema` equals v1 | Schema-only records (no `taskCall`) have no defined treatment. | CE-5 |
| 65–66 | Unparseable JSON counted as `unreadable_json` | I/O errors (EACCES, ELOOP) and invalid UTF-8 are unstated. Unreadable files do not affect the exit, so an all-corrupt lane exits 0. | CE-10 |
| 68–69 | Members are `taskCall.tasks[*]` (`name`, `agent`) | The body key is unnamed (it is `task`). A non-list `tasks`, an absent `taskCall` key, duplicate names, and `resumeSends` are all unaddressed. | CE-5, CE-8, CE-15 |
| 70–73 | "the LAST line of a task matching …" | Three readings are possible: (a) the last line must match, (b) the last matching line counts, (c) the last non-blank line must match. Real clones separate them (96 tasks). Trailing blank lines are unstated. Whether the path is relative to the lane root is unstated (the frozen fixture implies it). A path containing a space becomes `unparsed`, not `missing` (latent). | CE-8 |
| 70–73 | "resolve inside the lane root" | "resolve" suggests realpath, while "no `..` component" suggests lexical checks. Under realpath, a symlinked directory inside the lane passes as present. | CE-7 |
| 74–75 | `present` = regular non-symlink, size > 0 | The start marker (H1). No status is defined for a symlink, a directory, a FIFO, or ELOOP. | CE-2, CE-7 |
| 75–77 | `misrooted`: missing under the lane root and a "regular file" under `--fleet-root` | The fleet copy's size is unstated. Precedence among unsafe, empty and misrooted is unstated. Whether misrooted members appear in `missing` is unstated. | CE-16 |
| 78–81 | Five states with no order | `unavailable` and `unsettled` both hold when every member is unsafe or unparsed. The frozen `traversal` and `absolute-path` cases expect `unavailable`, so `unavailable` must be checked first, but the text does not say so. A zero-member wave makes both `settled` and `unavailable` vacuously true. | CE-1 |
| 79–81 | `unavailable`: "no member had a parseable safe path" | The name suggests "could not evaluate", which mori-dispatch-ledger maps to exit 2. Here it maps to exit 1. | CE-10 |
| 82–86 | Output fields | `members`: count or list (the oracle uses `members: 0`). `counts per status` keys unnamed. `missing` is names here and a count in the oracle. `totals` content undefined. `dispatch_path` relative or absolute unstated. `lane_root` as given or resolved unstated. `wave` for schema-only records unstated. Canonical serialization for "byte-identical" unstated. Stdout versus `--out` unstated. "never paths outside the lane" suggests paths were once emitted. | CE-11 |
| 80–81, 84 | "never says dead, failed or killed"; member names listed in `missing` | Member names are free text from the payload. 32 hits exist (e.g., member names `DeadSeatHistoryR18` and `SubstanceDEADSEATRECORD`). A name appears in `missing` whenever its member is not present, so a raw-bytes check cannot be guaranteed on a fleet run. A sha256 hex digest can also contain `dead`: 61/65536 per digest, about 16.7% across 196 digests (theoretical); observed 0/196 in this pass. | CE-9 |
| 87–88 | Exit 0, 1, 2 | Zero waves exits 0. All-unreadable exits 0. A missing `.ufo/waves` is unspecified; five fleet lanes lack it. An invalid `--fleet-root`, an unwritable or symlinked `--out`, and the `--selftest` result are all unspecified. | CE-10 |
| 90–93 | "14/14 matched by an oracle harness written independently" | No harness path or owner is named. The 14 cases check exit 0 and 1 only and a subset of keys. Output schema conformance is untested. | CE-14 |
| 95–98 | Live demonstration: "reports_present = 16 of 64" | `reports_present` is undefined. "Round-19 wave-1" maps to `round-19/wave1-run.json` (wave `mori-r19-attempt2-build`); the contract should name the file, since `wave1-attempts.json` also exists. "recorded by the non-author closure" cites no path; I did not open MANIFEST. The fleet-wide "totals" are undefined. Reproduced now: 16 present, 48 missing. | L1, CE-11 |
| 100–104 | Counting command reads `.counts.capability_absent` and `.counts.matched` | The schema of those files is undefined. They sit in `.ufo/waves/round-20/evidence/`, so later scans count them as `ignored_json`. | CE-12 |
| 106–109 | Separation from C1 | Silent on `mori-misroot-sweep.py` and `mori-dispatch-ledger.py`, both of which exist (§8). | CE-17 |
| 111–117, 57 | "no writes outside an explicit `--out`" and `--selftest` | `--selftest` needs fixtures. This conflicts with the no-writes rule unless a temp directory is allowed. | CE-10(f) |

Two more terms are untestable until defined: "dispatched seats" (line 52) and "NOT a dead seat" (line 80). §4 supplies the definition of "dispatched".

## 8. Existing tools that overlap (M3)

- `tools/mori-misroot-sweep.py` (header lines 1–35) is a detection-only fleet-root sweep. It runs `git status --porcelain` over untracked files, reads at most 64 KiB of each, and matches lane and round in path or head text. C2's `misrooted` is an exact relative path under `--fleet-root`. The definitions differ. C2 must not read git status, and the contract should say so.
- `tools/mori-dispatch-ledger.py` (header line 2: "Bind and verify per-attempt dispatch payload identities"; exit constants at lines 18–20; `json.dumps(..., sort_keys=True, separators=(",", ":"))` plus LF at line 33). C2 should not re-derive payload identity. The receipt `round-20/wave1-dispatch-receipt.json` carries `taskcall_sha256`, which I reproduced exactly with `json.dumps(taskCall, separators=(',', ':'), ensure_ascii=False) + "\n"` (66,812 bytes). That is one lane-specific instance. No fleet-wide receipt schema exists.

## 9. Co-evolved refinements (CE): proposals, frozen bytes unchanged

Each item is an annex proposal labelled co-evolved. "Frozen effect" is my reading of the 14 expectations. I did not execute the tool.

**CE-1 State rules.** Evaluate in this order: `no-spawn` (taskCall is null) → `unavailable` (zero members, or no member has a parseable safe path) → `settled` (all present) → `partial` (at least 1 present and at least 1 not) → `unsettled` (0 present). Frozen effect: consistent with all 14 (traversal and absolute-path expect `unavailable`; none-present expects `unsettled`).

**CE-2 Start marker.** A report whose content, after stripping whitespace, is exactly `STATUS: started` and whose size is at most 64 bytes has status `started`, which counts as not present. Frozen effect: the frozen cases do not pin report bytes, so the harness must write non-marker content into its "non-empty" reports (CE-14). Live effect: mori r20 becomes `partial` (18 started) and exits 1.

**CE-3 Spawn record and declared-only.** For each wave, `spawn_record` is one of: `ids-recorded` (the registry at `registry.path` is a regular file and every declared member has a non-null agentId); `ids-not-recorded` (registry present, some or no agentIds); `registry-file-absent`; `registry-unreadable`; `no-registry-key`. `declared_only` is true unless `spawn_record` is `ids-recorded`. The registry path follows the containment and lstat rules of CE-7. Totals split as in §6. An opt-in flag `--exclude-declared-only` (default off) would remove declared-only waves from the exit computation. Frozen effect: frozen payloads have no registry key, so only the annotation changes, and the exit is unchanged.

**CE-4 No filename inference.** File names never change state, wording, exit, or `declared_only`. Case: `ce-name-invariance`.

**CE-5 Payload definition.** A payload is a regular JSON file whose top-level `schema` equals v1 and which has a `taskCall` key (null allowed, meaning `no-spawn`). A v1 schema without a `taskCall` key is a `schema_collision`, which is counted and gives exit 1. In the current fleet all three collisions are nested, so CE-6 applies first. Frozen effect: `no-spawn` keeps its key, and no frozen payload lacks one.

**CE-6 Nested lane roots.** A directory below `.ufo/waves/` that itself contains a `.ufo` directory is a nested lane root. Do not descend into it. Count its payloads as `nested_dispatch_skipped`. Frozen effect: frozen cases are fresh temp lanes (fixture_note, line 5) and contain no nested `.ufo`.

**CE-7 Symlinks.**
(a) `--lane-root` and `.ufo/waves` must each be a real directory. Otherwise exit 2.
(b) Symlinked directories are not descended. Symlinked files and directories under waves are counted in `skipped_symlinks`, not dropped silently.
(c) For a report path: reject empty, absolute, NUL-containing, and `..`-containing paths (lexical check). Then lstat each component from the lane root. A symlink in any component, or a symlink final entry (dangling or not), is `unsafe` with `reason: symlink`. A non-regular final entry (directory, FIFO, socket, device) is `unsafe` with `reason: not-regular`. Errors other than ENOENT or ENOTDIR (ELOOP, EACCES) are `unsafe` with `reason: unreadable`.
(d) The fleet-root candidate must be lstat-regular. A symlink there is not a misroot.
Frozen effect: `symlink-report` stays exit 1 with present 0. Its `not_followed: true` maps to `reason == "symlink"` (CE-13). The frozen case does not say where the symlink target is; CE-14(vi) pins it, and an outside target is `unsafe` either way.

**CE-8 Trailer.** The body key is `task`. Remove trailing blank lines. Exactly one line may match `^Report: write your scoped findings to (\S+)$`, and it must be the last remaining line. Otherwise the member is `unparsed`, with `reason: trailer-not-last` or `multiple-trailers`. Carriage returns are not stripped, so a CR-terminated trailer is `unparsed`. The path is relative to `--lane-root`. Frozen effect: no-trailer stays `unparsed`. all-present does not depend on whether the harness writes a trailing newline, because the blank-line rule makes it irrelevant. Real-data effect: the 96 `| godspeed` tasks stay `unparsed`, now with a named reason.

**CE-9 Vocabulary.** `dead`, `failed` and `killed` are forbidden as values of enum fields (`state`, `status`, `reason`, `spawn_record`) and as key names. Member names, paths, wave names and hex digests are data and are exempt. The frozen `no_vocab` check stays valid on its synthetic fixture. For fleet runs it is re-scoped to enum fields.

**CE-10 Exit codes.**
- Exit 2: `--lane-root` is not a real directory; `.ufo/waves` is missing or is not a real directory; `--fleet-root` is given but is not a real directory; `--out` is not writable, is a symlink, or lies inside `.ufo/waves/`.
- Exit 1: `waves == []` with `unreadable_json > 0`; any `schema_collision`; any `unknown_dispatch_schema` (a `ufo-swarm-wave-dispatch-` prefix with a version other than v1).
- Exit 0: otherwise. Zero waves with no unreadable files is an explicit "nothing declared", and the output lists it.
- `--selftest`: exit 0 on pass, 1 on fail. It writes only inside a temp directory it removes. That is the stated exception to "no writes outside `--out`".
Frozen effect: none of the 14 uses exit 2. `malformed-dispatch` and `other-schema-ignored` keep exit 0 because each has a valid wave. `no-spawn` keeps exit 0. Naming: `unavailable` (state, exit 1) and mori-dispatch-ledger's `could-not-evaluate` (exit 2) differ, and the annex should record that.

**CE-11 Output keys and types.** `lane_root` = realpath. `fleet_root` = realpath or null. `dispatch_path` = relative POSIX path from the lane root. `wave` = string or null. `dispatch_sha256` = sha256 of raw bytes. `members` = array of `{index, name, agent, status, reason}` with no paths and no report bytes. `counts` = object with `present, started, empty, missing, misrooted, unsafe, unparsed`. `missing` = sorted names of members whose status is not `present`, duplicates kept. `totals` = `{waves, members, counts, states, spawn_record counts, declared_only_waves, unsettled_spawn_recorded, unsettled_declared_only, nested_dispatch_skipped, skipped_symlinks, schema_collisions, unknown_dispatch_schema, ignored_json, unreadable_json}`. Totals count payloads, not distinct wave names. Serialization: `json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"`, the same convention as mori-dispatch-ledger. Frozen effect: `members: 0` in `no-spawn` maps to `len(members)` (CE-13).

**CE-12 Snapshot identity and self-interference.** Add `discovery_sha256` = sha256 over the sorted lines `relpath NUL sha256 LF` for every candidate JSON file (payloads, ignored, unreadable, skipped). Two runs are comparable only when it matches. The `--out` path is excluded from discovery, and `--out` may not lie inside `.ufo/waves/` (exit 2). Stdout and the `--out` file carry identical bytes. Frozen effect: `deterministic` still holds on an unchanged fixture.

**CE-13 Oracle key mapping (annex, not frozen).** Process exit → `exit`. `waves[0].state` → `state`. `waves[0].counts.<k>` → `<k>`. `len(waves[0].missing)` → `missing` (count). `waves[0].missing` → `missing_names`. `len(waves[0].members)` → `members`. A member with `reason == "symlink"` → `not_followed`. Top-level `ignored_json`, `unreadable_json` and `len(waves)` → `waves`. Enum-only vocabulary → `no_vocab`. Two-run stdout equality plus equal `discovery_sha256` → `byte_identical`. A byte search of stdout and of the `--out` file → `*_contains_canary`.

**CE-14 Harness obligations for the frozen 14.** The harness must make these explicit, without editing frozen bytes: (i) non-empty reports are not the start marker; (ii) `empty-report`'s second report is non-empty; (iii) the `misrooted` fleet copy is non-empty; (iv) `malformed-dispatch`'s valid wave is non-empty and not the marker; (v) `no-spawn` has no `resumeSends`; (vi) the `symlink-report` target is inside the lane (the outside variant becomes its own case); (vii) `deterministic` runs without `--out` inside the tree; (viii) the body key is `task`, the trailer is the last line, and a trailing newline is optional.

**CE-15 Resume-only waves.** `taskCall: null` with a non-empty `resumeSends` is `unavailable` (exit 1) until a resume-member rule is written. This is latent: no fleet payload has non-empty `resumeSends`.

**CE-16 Misroot precedence.** For each member, in order: unsafe (checked first; the fleet root is never consulted), then present, started or empty (the lane path exists), then misrooted (the lane path is ENOENT or ENOTDIR, the fleet path is lstat-regular, and its size is > 0), then missing. A 0-byte fleet copy is `missing`. Misrooted counts as not present and is listed in `missing`, with its status in `members`. Frozen effect: the frozen `misrooted` case keeps present 1 and misrooted 1, provided its fleet copy is non-empty (CE-14(iii)).

**CE-17 Relation to other tools (annex text).** C2 does not run or read `git status`, does not verify payload identity, and does not replace `mori-misroot-sweep.py` or `mori-dispatch-ledger.py`. A ledger verdict may be cited by reference only. C2 reports `spawn_record` from registry data and nothing more.

## 10. Frozen oracle (`c2-expected.json`): each case under the annex

| Case (line) | Touched by | Expected under the annex | Note |
|---|---|---|---|
| all-present (7) | CE-1, CE-2, CE-8 | exit 0, settled, present 3 | CE-14(i) |
| one-missing (8) | CE-2, CE-11 | exit 1, partial, present 2, missing_names [C] | |
| none-present (9) | CE-3 | exit 1, unsettled, present 0 | annotation only |
| empty-report (10) | CE-1 | exit 1, partial, present 1, empty 1 | CE-14(ii) |
| misrooted (11) | CE-16 | exit 1, partial, present 1, misrooted 1 | CE-14(iii) |
| malformed-dispatch (12) | CE-10 | exit 0, waves 1, unreadable 1 | CE-14(iv) |
| no-trailer (13) | CE-8 | exit 1, partial, present 1, unparsed 1 | |
| traversal (14) | CE-1, CE-7 | exit 1, unavailable, unsafe 1, present 0 | |
| absolute-path (15) | CE-1, CE-7 | exit 1, unavailable, unsafe 1 | |
| symlink-report (16) | CE-7, CE-13 | exit 1, present 0, `not_followed` ⇔ reason symlink | CE-14(vi) |
| other-schema-ignored (17) | CE-5, CE-10 | exit 0, ignored_json 2, waves 1 | |
| no-spawn (18) | CE-5, CE-11, CE-15 | exit 0, no-spawn, members 0 | |
| content-not-emitted (19) | CE-11 | exit 0, canary absent from stdout and `--out` | |
| deterministic (20) | CE-9, CE-12 | byte-identical; no_vocab on enum fields | CE-14(vii) |

By reading, I found no frozen case that the annex contradicts. The annex adds 22 cases in `build/ContractReview/c2-coevolved-cases.json`. They cover exit 2, nested roots, symlink components, marker-only reports, trailer variants, spawn records, schema collisions, and vocabulary on member names. None of them is frozen.

## 11. Verification gaps and [INFERENCE] markers

- No tool and no harness exist. Every "frozen effect" statement comes from reading the expectations, not from running them.
- Live counts are snapshots. Pass 2 and pass 3 differ (179 → 196 payloads; kagi r25 88/88 missing → 16/88 present; the mori r20 marker count moved). Re-measure at acceptance.
- The meaning of "spawn record" rests on two observations. In mori r20 the receipt's `returned_count` (76) equals the number of non-null registry agentIds (76). The never-dispatched payloads carry `dispatched=0` or `dispatchCalls: 0` beside them. I did not read the `record` verb's source, so the equivalence is [INFERENCE].
- The receipt canonicalization in §8 rests on one instance.
- The 18 marker-only seats may still be running ([INFERENCE], §3).
- I did not read MANIFEST.json, the knowledge notes, or any transcript. C1 was out of scope and is not reviewed here.

## 12. Checks for the main agent after integration

1. Run the 14 frozen cases unchanged against the tool. Expect `c2-after.json` `counts.matched` = 14 and `capability_absent` = 0 (`contract.md:100–104`). Confirm the frozen bytes are unchanged: `git status --porcelain -- .ufo/waves/round-20/frozen .ufo/waves/round-20/contract.md` prints nothing.
2. Run the 22 co-evolved cases once L1 accepts CE-1 to CE-17. They are not part of the frozen count.
3. Re-run the fleet census at acceptance for the payload count, the status census, the spawn-record classes, and the seven unsettled payloads. Record the timestamp.
4. Confirm the live demonstration names `round-19/wave1-run.json` and reproduces 16 present and 48 missing.

Tooling record: no installs and no upgrades. Tools used: `jq` (jaq 3.1.1, already installed), Python 3 stdlib in the eval kernel, and read-only `git` subcommands (`cat-file`, `log`, `status`). Nothing wrote to any lane.
