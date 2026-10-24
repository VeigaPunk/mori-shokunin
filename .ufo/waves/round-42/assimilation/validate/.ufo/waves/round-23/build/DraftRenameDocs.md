# DraftRenameDocs — append-only correction drafts for the C1 schema v2 cutover

Seat: `MadoR22-2.DraftRenameDocs-8` (scribe, leaf member; no subagent dispatch, no delegation).
Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md` §C1
(frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`; contract sha256
`2bb35aefb08d3fafc467260f859453c0f096effe18b2446503f2b2ee87fe69e7`, matching
`frozen/c1-requirements.json.contract_sha256`).
Deliverable: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/DraftRenameDocs/corrections.md`.
Tool installs: none — no install, no upgrade, no service or system change. No package
transaction was attempted; the tooling directive's install channel was not needed
(read-only drafting on already-present `git`, `python3`, `sha256sum`, `awk`).

## Behavior delivered

Drafted two **append-only** correction blocks that explain the round-23 C1 schema v2
cutover for the two named documentation surfaces, with no rewrite of any existing
text:

1. `SKILL.md:556` — the "Field caveats (wave2 FinalR02/NoHarm)" paragraph of the
   Round22 retention-receipt-reconciliation section (`:556-564`, file ends at `:564`).
   Appended block states: schema `mori-retention-reconciliation-v2` in every output
   (check, setup error, selftest); key `raw_unallowlisted` removed from every output
   with no alias; `scanner_unallowlisted` carries the in-scope (non-author-filtered)
   unallowlisted count that the removed key carried; `raw_not_allowlisted` is the raw
   complement, semantics unchanged (9 on the r21 receipt, 95−86); no other key, value,
   exit code or finding id changes; r22 evidence stays byte-unchanged and the r22
   claim stays reproducible at its bound revision; carried debt unchanged; no privacy
   clearance.
2. `corpus/knowledge/retention-reconciliation-r22.md:27-35` — the "Exact populations"
   alias paragraph (`:27-36`; the assignment's named range covers the alias
   sentences, the last of which runs one line past `:35` to `:36`). Appended block
   qualifies the retained v1 sentences by date and schema instead of contradicting
   them, and adds the same cutover facts plus the declared consequence that the r22
   frozen oracle's R02/R11/R12 and the r22 driver's whitelist read the removed key
   and therefore no longer pass against post-C1 tool revisions.

Each block also carries the r23 requirement re-expression (R02/R11/R12 read
`scanner_unallowlisted` with the same expected values 1/3/1; R25 requires schema v2
and the absence of `raw_unallowlisted` in every parsed oracle run; R26 requires
`raw_not_allowlisted` to equal an independent identity-level count) and the
no-harm scope: four unallowlisted hits, original permission control RED 11/12, two
unknown historical dispositions, blocked baseline acceptance, `privacy_clearance`
always false.

## Gates

- No test, build, linter, formatter, smoke run, selftest, retention gate or
  reconcile invocation was executed — forbidden in this wave, and L1 measures after
  integration.
- Only read-only `git` plumbing was used (`rev-parse`, `log`, `cat-file`,
  `merge-base --is-ancestor`, `grep`, `show`) plus file reads and `sha256sum`.
- No lane Git index, jj state, commit, branch or worktree was touched; no `git add`,
  `git commit`, `git push` or mutating `jj` command was run. No clone or synthetic
  fixture was created (this seat is neither a writer executor nor a fixture author).
- No live host probe was performed: no `/proc/self/mountinfo` read, no `os.stat` of
  the fleet root or `/tmp`, no `readlink` of `/dev/mapper/*`, no listing under
  `/sys/fs/btrfs`. This seat's items do not name those reads.
- No session transcript was read (none permitted this wave); no credential, auth or
  `agent.db` file was read. No `agent://all` broadcast; no `/tmp` use.

## Touched surfaces

Written (both inside this seat's assigned paths, both untracked wave build outputs):

| Path | Bytes | What |
|---|---|---|
| `.ufo/waves/round-23/build/DraftRenameDocs/corrections.md` | 11273 | the two correction blocks, anchor map, read-only evidence table, no-harm scope, integration checklist |
| `.ufo/waves/round-23/build/DraftRenameDocs.md` | this file | seat report |

Not written (read only): `SKILL.md`, `corpus/knowledge/retention-reconciliation-r22.md`,
`corpus/README.md`, `corpus/lessons/round-22.md`, `corpus/QUALITY.md`,
`corpus/SOURCES.md`, `tools/mori-retention-reconcile.py`,
`.ufo/waves/round-23/contract.md`, `.ufo/waves/round-23/frozen/*`,
`.ufo/waves/round-23/oracle-rename.py`, and the r22 wave's frozen/evidence artifacts.

## Findings (read-only, observed)

1. **The tool is still at v1.** `tools/mori-retention-reconcile.py:16` is
   `SCHEMA='mori-retention-reconciliation-v1'`, and `:234` still emits
   `'raw_unallowlisted':len(unallowed)` next to `'scanner_unallowlisted':len(unallowed)`;
   `'raw_not_allowlisted'` is already present at `:235`. C1 is therefore not yet
   implemented in the lane working tree — the corrections describe the pre-registered
   post-cutover state and are written to be applied when the implementation lands.
2. **The two doc anchors are exactly where the assignment says.**
   `SKILL.md` has 564 lines; `:556` is the "Field caveats" paragraph and `:564` the
   last line. The corpus note has 42 lines; `:27-36` is the alias paragraph, `:38`
   begins `## Provenance limits`. The corpus range in the assignment (`:27-35`) cuts
   one line before the paragraph's end — the correction is therefore anchored after
   `:36`, leaving `:27-36` intact.
3. **`raw_not_allowlisted` = 9 reproduces independently.** Recounting from the
   committed r21 receipt plus the committed allowlist and policy bytes gives raw 95,
   86 allowlisted identities, and 9 raw identities in no allowlist row outside
   `must_redact_paths` — matching `frozen/c1-expected-real.json`
   (`raw_total` 95, `allowlisted` 86, `raw_not_allowlisted` 9,
   `scanner_unallowlisted` 4, `policy_excluded` 5, `scanner_total` 90). The
   recomputed input digests equal the frozen control's `inputs_sha256` exactly
   (receipt `4001e2d9…`, policy `db06e981…`, allowlist `f46c78ec…`); the receipt at
   `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0` hashes to the same `4001e2d9…`.
4. **The declared consequence is real and locatable.** `.ufo/waves/round-22/oracle-reconcile-v2.py:48,52,53`
   read `raw_unallowlisted` in R02/R11/R12; `.ufo/waves/round-22/measure-round22.py:20`
   lists it in its output-key whitelist and `.ufo/waves/round-22/frozen/expected-real.json:21`
   pins `"raw_unallowlisted": 4`. The r22 driver stages the tool from the measured
   revision (`measure-round22.py:59`), and `da40bb20f81da125d798f73cd1653655be1255ca`
   is an ancestor of HEAD, so the r22 claim remains reproducible at that bound
   revision while no longer passing against post-C1 tool revisions.
5. **Residual doc mentions outside the two assigned surfaces** (not corrected here;
   listed for the owning seats): `corpus/lessons/round-22.md:87` ("a truthful
   `raw_not_allowlisted` beside the frozen alias `raw_unallowlisted`"),
   `corpus/README.md:420` (coverage-map row for the r22 note), `SKILL.md:538` (the
   round-22 gate registry row and its frozen-artifact pointers), `SCORECARD.md:1422`
   and `LOG.md:1527` (round-23 pre-registration entries, which already describe the
   rename correctly). The r22 wave's own frozen/evidence/build artifacts mention the
   key in ~150 files and stay byte-unchanged historical evidence.

## Out of scope for this seat

- Applying the corrections to `SKILL.md` and the corpus knowledge note: this seat is
  a scribe drafting text; `SKILL.md` registry rows belong to `DraftSkillRows` and the
  corpus note to `DraftKnowledge`, with L1 integrating.
- The C1 tool change itself, the r23 oracle, the sealed cases and the C2 quota
  probe — other seats.
- Any change to `.ufo/waves/round-22/**` (frozen expectations, oracles, evidence) or
  to `SCORECARD.md` / `LOG.md` round-23 entries.
- Any measurement, gate, selftest or acceptance decision.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/DraftRenameDocs/corrections.md`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/DraftRenameDocs.md`
