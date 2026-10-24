# AttackMixedBoot — round 16 critic (MoriR16.AttackMixedBoot, leaf)

Target: the shared window contract for `tools/mori-journal-window.py`, the boot-related fixture packs under `.ufo/waves/round-16/fixtures/`, and the peer reports `BootContinuity.md` and `PackBootBoundary.md`. Review only. I wrote only this report. Nothing was executed: no tool, harness, selftest, or journal probe. `tools/mori-journal-window.py` and `tools/mori-round16-regressions.py` do not exist yet, so every attack below is against the contract and the fixtures, not against code.

Installs or updates: none. Tools used (all preinstalled): `curl` for the systemd v261 sources, `python3` to parse the fixture JSON, `man`, and `systemctl --version`.

Deviation (disclosed): one `curl -o` briefly created the scratch file `.ufo/waves/round-16/build/.AttackMixedBoot-jf.c.tmp`. I removed it in the next command, and `ls -a` confirmed it was gone. No other write was made.

## Axes
- **A1 boot binding**: a refusal must not become rc0.
- **A2 forged boot scalar strictness**: no normalization or salvage.
- **A3 provenance / identity**: whether the r15 predicate's boot term keeps its meaning.
- **A4 fixture coverage**: whether these cases can be expressed and are present.
- **A5 output safety**: no record-sourced echo.

## Evidence base
- Host is `systemd 261 (261.2-1-arch)`. `man journalctl` on the host, `--output-fields=`: "__CURSOR, __REALTIME_TIMESTAMP, __MONOTONIC_TIMESTAMP, and _BOOT_ID fields are always printed".
- systemd v261 `src/shared/logs-show.c`. The raw file I fetched hashed to sha256 `5402ad2f…dddb1b`.
  - Lines 1234 and 1268: the JSON `_BOOT_ID` is the **entry header** boot id from `sd_journal_get_monotonic_usec`.
  - Line 1176: the `_BOOT_ID=` data field is suppressed.
  - Lines 1121–1130: a field that occurs more than once becomes an array. Non-printable values become byte arrays. A value over the threshold becomes `null`.
  - Conclusion: real journalctl emits exactly one string `_BOOT_ID`, from the same header source as the cursor's `b=` component and the merge-order key. Arrays, `null`, numbers, duplicate keys, case variants, and dashed forms are **forged-only** in fixtures. The tool must still refuse them; this is strictness, not an emulation of real output.
- systemd v261 `src/libsystemd/sd-journal/sd-journal.c`.
  - `compare_locations` (lines 1076–1122) and `compare_with_location` (lines 607–664) define the cross-file order. Seqnum is compared only when the `seqnum_id` matches. Otherwise the order is monotonic time within one boot, then `compare_boot_ids` (lines 588–605; it compares the newest realtime of each boot's newest file, same machine only), then realtime, then the xor hash.
  - So records from different boots that live in different seqnum lineages are ordered by timestamp heuristics, not by write order. This upgrades BootContinuity F6 from [UNKNOWN] to a source-backed statement.
- `tools/mori-census.sh` lines 234–236 and 324–336: r13 census binds every counted record to the **current** boot, read from `MORI_BOOT_ID_FILE` (default `/proc/sys/kernel/random/boot_id`), with dashes removed and 32 lowercase hex enforced.
  - Lines 1052–1055: the r15 positive predicates use `$boot` = that current boot.
- Fixture survey: I parsed every pack with `object_pairs_hook` and classified each record's `_BOOT_ID`. Packs present: AnchorValidation, BootBoundary, CursorShape, ExactAnchor, KernelSystem, KernelUser, MissingAnchor, RecordShape, TypedFields, UnitOom, UnitSignal.
  - Every later-record `_BOOT_ID` is either equal to the anchor boot or a well-formed foreign 32-hex value.
  - **Zero** cases use an uppercase, dashed, whitespace-padded, array, null, number, missing, or duplicate-key `_BOOT_ID`.

## Counterexample 1 (decisive, A1/A3): a stale-boot anchor returns rc0 for a dead boot
- **Contract.** It compares the first record and every later record against `anchor.boot_id` only. The CLI (`--anchor --scope [--journalctl] [--timeout] [--max-bytes]`) has no current-boot input.
- **Scenario.** The anchor was written in boot A, then the host rebooted into boot C. `journalctl --cursor=<A anchor>` returns the anchor plus A's tail, and no C record appears after the anchor. This happens in two ways:
  - (a) Scope `user` has no boot-C user-journal writes yet, or the C records sit only in a runtime file before flush.
  - (b) The C records are in a different `seqnum_id` lineage, and `compare_boot_ids` or realtime ordering places them **before** the anchor location (for example after an RTC step). They are then never iterated after the cursor.
- **Result.** The tool returns rc0 `MORI_JOURNAL_WINDOW_OK` with `records_after_anchor=N` (possibly 0) and zero positives. Meanwhile boot C may contain kernel OOMs. "Boot boundary stays unavailable" is violated: a false clean.
- **Regression.** r13 census refused exactly this: a stale stream versus `/proc` boot is unavailable (census.sh:324–327).
- **Identity change.** The r15 predicate's `$boot` term silently changes from "current boot" to "anchor boot". The fixtures cannot catch this because no pack can say what the current boot is.
- **Corroboration.** BootContinuity F5 raises the same gap from the documentation side. This report adds the systemd ordering source and the census precedent, showing the gap is a regression and not only an unsupported claim.
- **Defect class.** A fixable defect, not a tradeoff.
- **Smallest safe correction.** Reuse the r13 pattern.
  - Add `--boot-id-file PATH` (default `/proc/sys/kernel/random/boot_id`). Read it bounded, remove `-` and the trailing `\n` exactly as census:331 does, and require a full match of `[0-9a-f]{32}`.
  - Unreadable or invalid file → rc2 `MORI_JOURNAL_WINDOW_SETUP`.
  - `anchor.boot_id != current` → rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE`, reason `anchor-boot-not-current`, without spawning journalctl.
  - Harness: add an optional per-case `current_boot_id`, defaulting to `anchor.boot_id` so every existing pack stays valid with no harm. Write it to a per-case file under the output dir and pass it via `--boot-id-file`.
  - Selftest stays free of live reads.
  - This is an interface change held by L1 MoriR16. I made no edit.

## Counterexample 2 (A2): last-wins duplicate keys forge a same-boot record
`json.loads('{"_BOOT_ID":"bbbb…","_BOOT_ID":"aaaa…"}')` yields `aaaa…` (CPython keeps the last duplicate key). A later foreign-boot record is then accepted as same-boot and its positives are counted. The same applies to the anchor file (`"boot_id"` twice) and to a duplicate `__CURSOR` that hides a cursor repeat. A `"\u005fBOOT_ID"` spelling decodes to the same key, so detection must happen after decoding: `object_pairs_hook` sees both.
- **Correction.** Parse records and the anchor with an `object_pairs_hook` that raises on a repeated key, mapping to rc2 UNAVAILABLE (record) or SETUP (anchor). Real journalctl never emits duplicate keys (it uses arrays), so this cannot false-refuse genuine output.
- **Residual, out of scope.** The census jq path has the same last-wins semantics. Record it as a residual; there is no census cutover this round.

## Counterexample 3 (A2): normalization helpers launder forged boot scalars
Python helpers that look like validation but normalize. Each one turns a forged value into an accepted equal value.

**Anchor side** (should be SETUP):
- `uuid.UUID(s).hex` accepts uppercase, dashes, `{…}`, and `urn:uuid:`.
- `int(s,16)` accepts `0x`, `_` between digits, and surrounding whitespace.
- `re.match(r'^[0-9a-f]{32}$', s)` accepts a trailing `\n`, because `$` matches before a final newline.
- `\d`, `str.isalnum`, and `str.isdigit` admit Unicode digits.
- `bytes.fromhex` skips whitespace.

**Record side** (should be UNAVAILABLE):
- `.lower()`, `.strip()`, `.replace('-','')`.
- Unwrapping a one-element array `["aaaa…"]` or a byte-array `[97,…]`.
- `str(v)` / `tostring` on a number.
- Defaulting a missing or `null` `_BOOT_ID` to the anchor boot.

The census read of `/proc` legitimately removes dashes. That normalization belongs only to the trusted current-boot file and must never be applied to the anchor or to records.
- **Correction.**
  - Anchor: `type(v) is str and re.fullmatch(r'[0-9a-f]{32}', v)`, applied before any comparison.
  - Records: `type(v) is str and v == anchor_boot` and nothing else. No coercion, no unwrapping, no default.
  - Optional hardening: reject an all-zero anchor `boot_id` (SD_ID128_NULL) as SETUP.

## Counterexample 4 (A1): a "helpful" boot filter erases the boundary
Adding `-b`/`--boot=<anchor>` or a `_BOOT_ID=<anchor>` match to the argv makes journalctl drop foreign-boot records (`add_match_boot_id`, logs-show.c:1814–1825). Every BootBoundary refusal then turns into rc0 with fewer records. The contract argv list already excludes these.
- **Correction.**
  - Harness wrappers should record argv. The harness should assert the exact contract argv: one of `--user`/`--system`, `--cursor=<anchor>`, `--no-tail`, `--quiet`, `--output=json`, `--output-fields=…`, and no `-b`, `--boot`, `--after-cursor`, `--merge`, `--file`, `--directory`, or `FIELD=` match.
  - Otherwise a filtered tool passes the BootBoundary packs only if the wrapper replays fixed stdout regardless of argv. Fixed stdout hides this regression in the harness, though it would occur on a live host.

## Counterexample 5 (A4): refusal cases assert only rc+id, so a wrong-cause refusal passes
The BootBoundary refusals use `want:{}`. I checked each one: the first record equals the anchor cursor, cursors are unique, scope matches, and the only defect is the boot. They are single-cause today, which is good. But a tool that refuses them for an unrelated bug still passes. That tool could even refuse every later record that has `MESSAGE_ID`, if the `same_boot_boundary_ok` control were weaker. The one rc0 control in the pack mitigates this.
- **Correction.** Pin a small `reason` vocabulary and assert it in the refusal `want` (`reason`). Proposed values: `anchor-boot-mismatch` (first record), `foreign-boot` (later record), `anchor-boot-not-current` (CE1), `record-invalid` (shape or type).
- **Note.** `anchor_record_foreign_boot` uses `__CURSOR b=aaaa…` with `_BOOT_ID=bbbb…`. That pairing is impossible from real journalctl, where both come from the entry header (logs-show.c:1218/1234). It is valid as a strictness case, but it must not be described as modelling a real reboot. A real reboot is CE1 plus `foreign_boot_immediately_after_anchor`.

## Coverage gaps to add (A4): forged-scalar cases absent from all packs
Each case: a valid anchor record, then one forged later record that carries an otherwise-positive kernel-OOM id (`fe6faa94e7774663a0da52717891d8ef`, census.sh). Expected: rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE`, `want:{}` or `reason:"foreign-boot"`/`"record-invalid"`.
1. `"_BOOT_ID":"AAAA…"`: uppercase of the anchor.
2. `"_BOOT_ID":"aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"`: the dashed `/proc` form.
3. `"_BOOT_ID":"aaaa…\n"` or a padded space.
4. `"_BOOT_ID":["aaaa…"]` and the byte-array `[97,…]`.
5. `"_BOOT_ID":null`, a number, or the key absent.
6. A duplicate key: `"_BOOT_ID":"bbbb…"` followed by `"_BOOT_ID":"aaaa…"` (CE2).
7. Anchor-side (AnchorValidation already has uppercase and short): add a dashed anchor, a trailing `\n`, an anchor JSON with duplicate `boot_id`, and a `boot_id` given as a non-string. Expected: rc2 `MORI_JOURNAL_WINDOW_SETUP`.
8. CE1: `current_boot_id` = `cccc…` ≠ anchor `aaaa…`, with clean same-boot stdout. Expected: rc2 UNAVAILABLE. This needs the schema extension.

## Tradeoff (not a defect, for the judge)
`foreign_boot_after_same_boot_positive` discards a **valid** same-boot unit-OOM that precedes the boundary, because the contract emits no totals on unavailable. r15 census instead kept valid positives beside unavailable totals (commit `26f6589`). For the window tool, refusing is the contract's no-harm choice, since the window claims no alarm override. The judge must accept it explicitly. Nobody should "fix" it by emitting partial counts.

## Output safety (A5)
Refusal output must not echo a record-sourced `_BOOT_ID`. A forged value can be up to the field threshold, can contain lone surrogates (Python `json.loads` accepts `"\ud800"`; `print` with `ensure_ascii=False` would then raise and give rc1 plus a traceback instead of a stable rc2 id), or can be data from the target. Echo only the validated anchor boot, the validated current boot, or their SHA-256.

## Impacted axes summary
| CE | A1 | A2 | A3 | A4 | A5 | class |
|---|---|---|---|---|---|---|
| 1 stale-boot anchor rc0 | ✗ | | ✗ | ✗ | | fixable defect (needs an L1 interface change) |
| 2 duplicate-key last-wins | ✗ | ✗ | | ✗ | | fixable |
| 3 normalization laundering | ✗ | ✗ | | ✗ | | fixable |
| 4 boot filter in argv | ✗ | | | ✗ | | fixable (harness argv assert) |
| 5 rc+id-only refusals | | | | ✗ | | fixable (reason vocabulary) |
| partial positive discard | | | | | | tradeoff, judge decides |

Report: .ufo/waves/round-16/build/AttackMixedBoot.md
