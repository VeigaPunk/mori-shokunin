# Round 30 — lesson (mori, L1 MoriR30)

author: MoriR30 (L1), from the wave-1 seat reports under `.ufo/waves/round-30/w1/` and the round-29 outside check
`corpus/lessons/round-29-verifier-spotcheck.md`.
Contract: `.ufo/waves/round-30/contract.md` (declared at `a66751b1`; amendments A1 `05db57ed`, A2 `3767108e` before the
data each governs; A3 `55f9a694` after the L1 saw the A2 gate's output — disclosed).

## What the round learned

- **Which invocation a send line belongs to is decided by two systemd facts and one earlyoom fact.** systemd stamps
  active-enter only on entry into the active set and keeps it across a stop (S157); `systemctl show` prints the
  unset stamp as a bare `0` (S156); earlyoom's shipped unit restarts it after a kill or crash, so a restart is a new
  version line (S159). The reader's journal is the current boot of the unit (S160); journald itself writes the
  suppression notice (S158). Entry: `corpus/knowledge/earlyoom-invocation-scope-r30.md`.
- **The disputed shape is now pinned blind.** Four writers who read only the rule text wrote eight cases of the
  active, stamp absent or 0, send-then-restart shape; all eight expect `KILLERS_UNKNOWN` and both the entering-tip and
  the changed tool print it (`evidence/c2-freeze-selftest-base.txt`, `c2-freeze-selftest-fixed.txt`). The rule text
  alone does not force that reading (wave-1 ReviewRuleTextShape F1); the agreement is evidence, not proof.
- **A gate must run on the round's own inputs before it is bound.** The round-30 gate was screened on the round-29
  wave and on planted leaks, then bound; on the round-30 writers it flagged the mandated godspeed skill file (A2
  version) and, after A3, a closing sentence under the files-opened heading. Both are instrument false positives; the
  counted C2 condition misses on them.

## Mistakes

- **M1 — a Gate reject reason states a grep result its own pointer contradicts (class: reference-drift).**
  Evidence: `corpus/lessons/round-29.md:65` (S155 reject row) ends "a case-insensitive grep for `dryrun` and
  `version` returned no line in either file", while the same row's source cell names `kill.h`. That file carries
  `:36` `/* Flag --dryrun was passed */` and `:37` `bool dryrun;` — HTTP 200, 1 440 B, fetched
  2026-10-22T21:13:41Z, sha256 `abf8577b434096e1eb980bacc24508e8421af9edbefb0d78cf5b8b5f28160bfb`;
  `grep -in -e dryrun -e version` prints exactly those two lines. The reject decision holds (a flag declaration is
  not the send-site behaviour), so the defect is the reason, not the row:
  `round-29-verifier-spotcheck.md:126` and `:157-158`.
  Captured-by: none. QUALITY 86's awk (`corpus/QUALITY.md:441-444`) reads a reject row's id, source cell and
  `reject, <reason>` shape, never whether the reason is true; the outside spot-check's manual re-open found it.
  Fix: append a correction in this lesson (`round-29.md:65` is not edited): the grep does return `kill.h:36-37`,
  and S155 is rejected because the match is a field declaration, not the behaviour the row needed.
  Shown able to fail: the correction ships with a check that re-runs `grep -icE 'dryrun|version'` on the fetched
  bytes and requires the correction to name `kill.h:36-37`. Red-before is the round-29 row itself (the file
  matches: 2 lines, 2026-10-22T21:13:41Z; the row says "no line"); a correction that repeats "no line" fails the
  line-number assertion; at `e936482` `corpus/lessons/round-30.md` is absent (21:17:19Z), so any check that reads
  this lesson has no subject until the lesson lands.

- **M2 — two quote word-count labels are one high (class: number-drift).**
  Evidence: `corpus/lessons/round-29.md:57` labels the `journal-upload-journal.c:100-101` quote "(11 words)";
  the committed text counts **10** by `wc -w`. `:62` labels the `ca2251fc` patch guard "(17 words)"; the committed
  text counts **16**. Recomputed from the lesson bytes in this session (clock read 2026-10-22T21:13:41Z in the
  same batch); the same two are recorded at `round-29-verifier-spotcheck.md:130`.
  Captured-by: none. No QUALITY criterion counts the words of a quoted excerpt (QUALITY 86's awk,
  `corpus/QUALITY.md:441-444`, reads id/source/decision cells only); the spot-check's §4 `wc -w` re-measure found
  it.
  Fix: append a correction in this lesson giving 10 and 16 with the recompute command; `round-29.md:57` and `:62`
  are not edited. The correction belongs in the lesson only — `awk 'NR==160||NR==161' corpus/SOURCES.md |
  grep -ci word` prints 1 and that match is "wording", so rows S154/S155 carry no count label to correct.
  Shown able to fail: a counter extracts each labelled quote from the row, runs `wc -w` and compares it with the
  label. Red-before at the entering tip: `label=11 words=10`, `label=17 words=16`, exit 1; a corrected label that
  still misses by one keeps failing; the pass state is `words=10`/`words=16`, exit 0.

- **M3 — tip receipts cited only where the receipts check does not read (class: landing; round-29 R1, the
  round-28 M5 shape).**
  Evidence: `round-29-verifier-spotcheck.md:154-156`. At `b581173a` the three receipts exist under
  `.ufo/waves/round-29/evidence/`, but the citations live only at `SCORECARD.md:1796-1797` (`tip-c1.txt`,
  `tip-c2.txt`); `git show b581173a:LOG.md | grep -c 'tip-c1.txt'` prints `0` and the round-29 lesson likewise
  prints `0`. Reproduced 2026-10-22T21:17:19Z: `bash .ufo/waves/round-28/check-tip-receipts.sh b581173a 29` →
  `cited_lane=no` for `count-c1.sh` and `count-c2.sh`, `tip_receipts=unmet`, exit 1.
  Captured-by: QUALITY 84 (`corpus/QUALITY.md:404-412`) and its check, whose default report set is `LOG.md` and
  `corpus/lessons/round-<N>.md` (`check-tip-receipts.sh:37`); the author cited a third file that the default read
  set excludes and ran no check on the tip batch.
  Fix: the round-30 `LOG.md` names the three receipts before the receipts-only batch (`LOG.md:1965-1966`, landed
  `e936482`), and this lesson names the same three basenames. The check concatenates its report set, so the LOG
  citation alone turns `cited_lane=yes`; the round's routing binds both files, so both are written.
  Shown able to fail: the same command at `b581173a 29` prints `tip_receipts=unmet`, exit 1, for exactly the named
  reason (`cited_lane=no`); at the round-30 tip it must print `tip_receipts=met`, exit 0. The lesson half is
  unobserved here: `corpus/lessons/round-30.md` does not exist at `e936482` (21:17:19Z).

- **M4 — the blindness gate is bound into a counted condition before the fixed instrument exists (class: scope;
  round-29 M2 recurs).**
  Evidence: `contract.md:75-79` makes `.ufo/waves/round-30/check-blind-wave.sh` a C2 condition (selftest `PASS`;
  0 on the round-29 writer wave at `d6d5cb0a`; a violation for each planted leak class; `blind_violations=0` at
  the freeze commit), but the file does not exist at the declaration commit: `git ls-tree -r --name-only
  e936482 -- .ufo/waves/round-30` lists no `.sh` (0 matches) and the working tree has none. The round-29
  instrument's first run on its own writer wave printed `blind_violations=20`, exit 1
  (`.ufo/waves/round-29/evidence/blind-check-prefreeze.txt:3,24` at `d6d5cb0a`).
  Captured-by: round-29 M2's rule (`round-29.md:32-37`, `:96-99`: a gate enters a counted condition only after a
  receipt of it on the round's own inputs), still not a QUALITY row. This round's contract is the first
  enforcement: an unscreened gate can now only fail C2, not silently pass it.
  Fix: land the gate with `--selftest` over the four named leak classes and the round-29 wave control, and commit
  the selftest receipt under `.ufo/waves/round-30/evidence/` before the freeze commit.
  Shown able to fail: the round-29 gate is the red control on that same input (`blind_violations=20`, exit 1 at
  `d6d5cb0a`); the fixed gate must print 0 there and ≥1 per planted leak class. Both green values are unobserved
  at `e936482` (no round-30 gate exists). Residual ordering defect, narrowed not removed: condition 4's last
  clause runs the gate at the freeze commit, after the writers' reports are fixed, so a matcher blind spot
  surfaces only once the data is frozen.
- **M5 — the blindness gate was bound into a counted condition before it ran on this round's writer reports (class:
  scope; repeats round-29 M2).** Evidence: A2 gate at `32e287ff` → `blind_violations=4`, every hit the godspeed skill
  path the task hook makes each seat read (`.ufo/waves/round-30/evidence/gate-a2-prefreeze.txt`); A3 gate at the
  freeze `db1ec469` → `blind_violations=1`, `CaseR30a.md:105`, the brief's closing sentence parsed as an entry
  (`evidence/c2-after.txt`, `evidence/gate-a4-diagnostic.txt`). Captured-by: round-29 M2's fix text ("a gate enters a
  counted condition only after a receipt of it on the round's own inputs"), which was never made a QUALITY row and was
  not applied. Fix: QUALITY 93 (this round): a gate bound into a counted condition must carry, before the freeze, a
  committed receipt of the frozen gate on the round's own inputs with every hit adjudicated; shown able to fail at
  `32e287ff` (A2 gate, 4 unadjudicated hits on the round's own wave) and at `db1ec469` (1 hit).

## Gate (rows opened 2026-10-22 in round 30)

Admit lines are written by the L1 from the drafting seats' reports (`w1/SrcShowZeroStamp.md`, `SrcUnitTimestampSet.md`,
`SrcJournaldSuppressed.md`, `SrcEarlyoomServiceRestart.md`, `SrcJournalctlBoot.md`), with each location prefixed by its
file name and each quote checked verbatim against the committed excerpt `corpus/evidence/sources-r30/S###.txt`; reject
lines are copied from the same reports (and `SrcUnitActiveEnter.md`, whose `unit.c` admit draft duplicated
SrcUnitTimestampSet's URL and is merged into S157).

| id | source | access time | sha256 | located quote | decision |
|---|---|---|---|---|---|
| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c | 2026-10-22T21:12:07Z | `b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a` | `bus-print-properties.c:19` (5 words): "bool bus_property_is_timestamp(const char *name) {"; `bus-print-properties.c:23` (4 words): "return endswith(name, \"Timestamp\") \|\|"; `bus-print-properties.c:194` (5 words): "bus_print_property_valuef(name, expected_value, flags, \"%\"PRIu64, u);" | admit, A, mined |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemctl.xml | 2026-10-22T21:12:07Z | `caca7b87ae3bc8730b070a38d814c698acf82c596df9cb47a58fc7510c7b765c` | `:328` (6 words): "By default, empty properties are suppressed." | reject, does not carry the fact: the `show` entry documents property selection and empty suppression only; the fetched 3 118-line page has 0 occurrences of `Monotonic`, `TimestampMonotonic` and `ActiveEnter` (grep -c, each 0), and no sentence on how an unset uint64 timestamp renders — that is a code fact carried by this row's printer URL |
| S157 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c | 2026-10-22T21:12:02Z | `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7` | `unit.c:2773-2774` (7 words): "if (!UNIT_IS_ACTIVE_OR_RELOADING(os) && UNIT_IS_ACTIVE_OR_RELOADING(ns)) u->active_enter_timestamp = u->state_change_timestamp;"; `unit.c:2775-2776` (8 words): "else if (UNIT_IS_ACTIVE_OR_RELOADING(os) && !UNIT_IS_ACTIVE_OR_RELOADING(ns)) u->active_exit_timestamp = u->state_change_timestamp;" | admit, A, mined |
| S157 | https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/time-util.h | 2026-10-22T21:12:50Z | `45e934d294f2ff0ca92cc7f1fcede1ef92862d20b276e305282cec5f3cba37e6` | `:91` (3 words): "dual_timestamp* dual_timestamp_now(dual_timestamp *ts);" | reject, duplicate URL: the URL is already a source of row S154 (corpus/SOURCES.md:160), so it is not a new row; the file declares `dual_timestamp_now` and holds no assignment to `active_enter_timestamp` (grep -c 'u->active_enter_timestamp =' time-util.h = 0) |
| S157 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/service.c | 2026-10-22T21:13:24Z | `9bf8a80bc29ef733648c688e4f40c3d01d6a4f67a877b2b5e23fbf8284c03d9c` | `:1731` (6 words): "unit_notify(u, table[old_state], table[state], s->reload_result == SERVICE_SUCCESS);" | reject, does not carry the fact: the service state machine funnels state changes into `unit_notify` (:1731) and only reads the stamp as a deadline base (:1028), with no assignment to `active_enter_timestamp` in the file (grep -c 'u->active_enter_timestamp =' service.c = 0); the write site is unit.c:2774 |
| S157 | https://raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml | 2026-10-22T21:12:17Z | `59cfeea5144e169369ee81f2b797fe9eb63ec18cb6aa918c2e66a7d5218117ca` | `:2789-2790` (17 words): "The fields are 0 in case such a transition has not yet been recorded on this boot." | reject, duplicate URL already carried by S122 (corpus/SOURCES.md:128 lists this URL and its scope names `ActiveEnterTimestampMonotonic`); the document does carry the fact at :2783-2784 and :2789-2790 |
| S157 | https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/time-util.h | 2026-10-22T21:12:18Z | `45e934d294f2ff0ca92cc7f1fcede1ef92862d20b276e305282cec5f3cba37e6` | `:110-113` (12 words): "static inline bool dual_timestamp_is_set(const dual_timestamp *ts) { return timestamp_is_set(ts->realtime) || timestamp_is_set(ts->monotonic); }" | reject, duplicate URL already carried by S154 (corpus/SOURCES.md:160); the zero-means-unset convention here is corroboration only |
| S157 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-get-properties.c | 2026-10-22T21:12:18Z | `06755221460fbdb8ad7bacbb2d1c34dbea8fc6cc3061e12f9bdc0c408a666071` | `grep -n "int bus_property_get_usec"` over the v262 tree returns nothing; `src/shared/bus-get-properties.h:13` defines the name as `((sd_bus_property_get_t) NULL)` | reject, does not carry the fact: no usec property getter is implemented in this file |
| S157 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-util.h | 2026-10-22T21:12:36Z | `145076586e534df103db9e73d70f65e0ec4b98642607a3c96e23d6088e9b508f` | `grep -n "DUAL_TIMESTAMP"` returns nothing; the file is 73 lines of bus transport and registration declarations | reject, does not carry the fact: the dual-timestamp property macro is at `src/shared/bus-get-properties.h:103` |
| S157 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/dbus-util.h | 2026-10-22T21:12:37Z | `7dac128023d62dd73ab4e0825c177eb8fc0b3175df3dcd91f798710b713a98fe` | `grep -n "DUAL_TIMESTAMP"` returns nothing; the file holds `BUS_DEFINE_SET_TRANSIENT*` macros | reject, does not carry the fact: no `ActiveEnterTimestamp` and no dual-timestamp property macro |
| S157 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.h | 2026-10-22T21:12:37Z | `563a8180f79038ddc28d267cd971c902bd6c1df438ac92cee6e0a6612b8e1eca` | `:313` (2 words): "dual_timestamp active_enter_timestamp;" | reject, carries the field declaration and the :311-315 comment only: no property mapping, no clock call, no zero rule |
| S157 | https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-bus/bus-util.h | 2026-10-22T21:12:37Z | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` | body line 1 (3 words): "404: Not Found" | reject, HTTP 404 at v262 — the header is `src/shared/bus-util.h`, which carries no dual-timestamp macro either |
| S158 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c | 2026-10-22T21:13:19Z | `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2` | `journald-manager.c:1291-1294` (16 words): "if (rl > 1) manager_driver_message(m, c->pid, LOG_MESSAGE_ID(SD_MESSAGE_JOURNAL_DROPPED_STR), LOG_MESSAGE(\"Suppressed %i messages from %s\", rl - 1, c->unit)," | admit, A, mined |
| S158 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-server.c | 2026-10-22T21:13:19Z | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` | body line 1 (3 words): "404: Not Found" | reject, HTTP 404 at v262 — the path serves no file at the tag, and the notice is carried by src/journal/journald-manager.c:1290-1296 at the same tag |
| S158 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-rate-limit.c | 2026-10-22T21:13:19Z | `dfe42099dd8adb3d6c1ad663b8a5a9b8d6550147b6932f65f71fed11b5d6780a` | `:28` (2 words): "unsigned suppressed;" | reject, does not carry the fact — the file holds the per-priority pools and the dropped counter, and `grep -c Suppressed` on the fetched bytes prints 0 |
| S158 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-native.c | 2026-10-22T21:13:19Z | `226a4c01562a972261f0ed0c8238b27447d318e368341a7100476260d9bd3521` | `:288` (8 words): "manager_dispatch_message(m, iovec, n, MALLOC_ELEMENTSOF(iovec), context, tv, priority, object_pid);" | reject, does not carry the fact — the native entry point hands the parsed record to the manager, and `grep -c Suppressed` on the fetched bytes prints 0 |
| S158 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journald.conf.xml | 2026-10-22T21:13:19Z | `ed71e38df308227a94aca77b0840742b2c6ec49c1e43c2376d4aa135908f87f2` | (0 matches) | reject, does not carry the fact — `grep -ci suppress` on the fetched bytes prints 0, so the page documents the limit without the notice wording |
| S158 | https://raw.githubusercontent.com/systemd/systemd/v257/src/journal/journald-server.c | 2026-10-22T21:13:19Z | `0c1bb73b71e9f8331378f55e4e2d35990a48fae2c95607e93bd9ddb6aca21cd3` | `:1304` (9 words): "LOG_MESSAGE(\"Suppressed %i messages from %s\", rl - 1, c->unit)," | reject, wrong version — the row is scoped to v262, and v262 carries the same line at journald-manager.c:1294, so this path adds no v262 evidence |
| S158 | https://raw.githubusercontent.com/systemd/systemd/v252/src/journal/journald-server.c ; https://raw.githubusercontent.com/systemd/systemd/v249/src/journal/journald-server.c | 2026-10-22 (fetch not timestamped; sha256 printed once) | `d9519978462b65c8cd0bb76a2230183aa25ed901b610027e1b8e670557388aad` (101129 B) ; `3478a46c01486eec3ee92dee131510df8436dc7099d9ec88fd53a346ec8466ac` (95661 B) | `:1143` / `:1107` (9 words): "LOG_MESSAGE(\"Suppressed %i messages from %s\", rl - 1, c->unit)," | reject, wrong version — both tags already spell %i and only locate the pre-split file, so neither can be the v262 anchor |
| S158 | https://raw.githubusercontent.com/systemd/systemd/v233/src/journal/journald-server.c | 2026-10-22 (fetch not timestamped; sha256 printed once) | `1434afcf28771525c7e77f0c1fe7fe84dd71933803b59e182e3f37454a066bde` (77853 B) | `:1181` (9 words): "LOG_MESSAGE(\"Suppressed %u messages from %s\", rl - 1, path)," | reject, wrong version and stale form — v233 substitutes a path and prints %u, while v262 prints %i with the unit name, so citing it would misstate the v262 message |
| S158 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-socket.c | 2026-10-22 (grep only; URL not fetched) | — | `corpus/SOURCES.md:160` shows this URL inside row S154 | reject, duplicate URL already carried by S154 |
| S159 | https://github.com/rfjakob/earlyoom/commit/edd3d9438dc564da7b694e5c96c9b3bc63bef2ac.patch | 2026-10-22T21:13:43Z | `dc5a771c9ed178751c0473c9ada89152e70b9da13a048b0af30df6bbb1f2a9a1` | `edd3d943.patch:6-7` (13 words): "Have systemd restart us should we get killed or crash for some reason."; `edd3d943.patch:34-36` (21 words): "+# earlyoom never exits on it's own, so have systemd +# restart it should it get killed for some reason. +Restart=always" | admit, A, mined |
| S159 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in | 2026-10-22T21:13:43Z | `d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd` (1,340 B, 51 lines) | `:17` (1 word): "Restart=always" | reject, duplicate URL — S120 (corpus/SOURCES.md:126) opens this exact URL and already anchors `:17 (Restart=always)`; a second row would repeat the same bytes |
| S159 | https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1 | 2026-10-22T21:12:19Z | `2282f9baf641a8417b97a1785119fd62f08e3560b50fdecfae2019fff3ae259d` (280 B) | body line 1 (4 words): "API rate limit exceeded" | reject, HTTP 403 rate limit (`x-ratelimit-remaining: 0`), no tree body to screen; the URL is also already S151's first URL (corpus/SOURCES.md:157) |
| S160 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c | 2026-10-22T21:12:34Z | `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab` | `journalctl.c:514-517` (12 words): "arg_boot = true; arg_boot_filter = true; arg_boot_id = SD_ID128_NULL; arg_boot_offset = 0;"; `journalctl.c:543-544` (13 words): "OPTION('u', \"unit\", \"UNIT\", \"Show logs from the specified unit\"): r = strv_extend(&arg_system_units, opts.arg);" | admit, A, mined |
| S160 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | 2026-10-22T21:12:34Z | `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` | `:290` (16 words): "The argument may be empty, in which case logs for the current boot will be shown." | reject, duplicate URL: this file is S122's first URL at `corpus/SOURCES.md:128`; it carries the fact but cannot open a new row |
| S160 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/journal-util.c | 2026-10-22T21:14:19Z | `d81dc8bfec7452694c8def5522addb1d608370d5de05e342de3bcfa207ecb5b8` | grep count (0 hits, exit 1): `add_matches_for_unit_full` occurs 0 times in the fetched bytes | reject, does not carry the unit match builder: `grep -c` returns 0; the builder is `src/shared/logs-show.c:1729`, already inside S123 |

### Row changes logged old → new (CORPUS Rules 2)

- New rows S156 (systemd v262 `bus-print-properties.c`), S157 (`unit.c` `unit_notify()`), S158 (`journald-manager.c`
  suppression notice), S159 (earlyoom commit `edd3d943`, `Restart=always`), S160 (`journalctl.c` `-b`/`-u`); status
  `mined`; `used-by` this lesson and `corpus/knowledge/earlyoom-invocation-scope-r30.md`. Rows S156 and S160 carry one
  URL each; their companion files are cited by path only (contract A1 4b: one URL per id). No `status`, `recheck` or
  `used-by` cell of an older row changed.

### Census (round start → round end)

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`: start
(21:05Z, `58b61681`) ten W04, `mori ok`, exit 0 (`.ufo/waves/round-30/evidence/census-start.txt`). End:
`.ufo/waves/round-30/evidence/census-end.txt`.

## Appended corrections to round-29 records (wave 1, DraftCorrectionsR2R3; round-29 text and SOURCES cells untouched)

- **R2 — `corpus/lessons/round-29.md:65`, S155 reject row (`testsuite_cli_test.go` ; `kill.h`).** The reason sentence
  "a case-insensitive grep for `dryrun` and `version` returned no line in either file" is false for `kill.h`. Both
  files were re-fetched at 2026-10-22T21:12:35Z: `kill.h` HTTP 200, 1 440 B, sha256
  `abf8577b434096e1eb980bacc24508e8421af9edbefb0d78cf5b8b5f28160bfb`; `testsuite_cli_test.go` HTTP 200, 9 317 B,
  sha256 `1dc876421c856bde48ab4a63304dab838c585f79c68a807d52b0741d366eb795` — equal to the row's recorded digests and
  sizes. `grep -in -e dryrun -e version kill.h` prints `36:    /* Flag --dryrun was passed */` and
  `37:    bool dryrun;` (exit 0); the same command on `testsuite_cli_test.go` prints nothing (exit 1); `version` matches
  no line in either file. The reject decision stands unchanged, and the located quote (`:36-37`, 8 words over its two
  strings) is correct: both matches are field declarations inside `poll_loop_args_t` (`kill.h:30-38`); the file has 44
  lines and one prototype (`void kill_process(...)`, `kill.h:40`), so it declares the flag and carries no send-site
  behavior.
- **R3 — `corpus/lessons/round-29.md:55-65`, S153-S155 Gate word-count labels.** 16 labels cover 18 quoted strings;
  5 labels are wrong and every quoted string, location and digest is right. Recomputed with `wc -w` on each verbatim
  string:
  - `:57` `journal-upload-journal.c:100-101` label 11 → **10**
  - `:60` `logs-show.c:1266-1267` label 11 → **10**
  - `:61` `journal-importer.c:255` label 5 → **4**
  - `:62` patch `:35-38` label 17 → **16**
  - `:63` `kill.c:272` label 8 → **6**
  The other 11 labels reproduce exactly: `:55` 22 and 24, `:56` 3, `:57` 2, 8, 3 and 4, `:59` 3, `:61` 4,
  `:64` 9 over its two strings, `:65` 8 over its two strings. The routed pair (`round-29-verifier-spotcheck.md:163`)
  names 11 vs 10 and 17 vs 16; three more are reported here (`:60`, `:61`, `:63`), and `:63` is two high, not one. The
  largest true quote is 24 words, so the 25-word quote bound holds either way. The labels entered through the drafting
  seats and were copied into the Gate: `w1/SourceJournalExport.md:81` (labels `2,8,3,11,4`) and `:85` (`4,5`),
  `w1/SourceEarlyoomDryrun.md:72-73` (`17`, `8`). Decisions, quotes, locations and digests are unaffected; the counts
  are corrected here, not edited into the rows.

## Routed defects (round-29 closure §7) — disposition

| Routed | Disposition | Evidence |
|---|---|---|
| R1 tip receipts not cited where the check reads | this lesson and LOG name `tip-c1.txt`, `tip-c2.txt`, `tip-retention.txt` before the receipts-only batch; QUALITY 88 | `.ufo/waves/round-30/w1/TipReceiptsR1.md` |
| R2 false reject reason | appended correction above | `w1/DraftCorrectionsR2R3.md` |
| R3 word-count labels | appended correction above (five labels, not two) and a SOURCES note | same |
| R4 three A2-10 cases | judged tool fix landed `7aa77484`; r29 file `PASS 24/24` | C2.1; `evidence/c2-freeze-selftest-fixed.txt` |
| R5 blindness gate false positives | gate rebuilt with allowlist and self-test (`32e287ff`, A3 `55f9a694`); the counted run still misses (M5) | C2.4 |
| R6 disputed shape | eight blind frozen cases `db1ec469`; A2a limit stated in the C1 entry and SKILL `## Round30` | C2.3; C1 |
| R7 PROVINCE, `SKILL.md:661` | fixed by same-line substitution and a correction block (`af42101d`) | `w1/DraftProvinceR7.md` |

## Tip receipts (routed R1)

The round's last lane batch adds only `.ufo/waves/round-30/evidence/tip-c1.txt`, `tip-c2.txt` and `tip-retention.txt`,
each measured at that batch's parent.

## Wave-2 corrections (appended; the entries above stand as written)

- **M5 retitled** (CriticLessonMistakes): the A2 gate did run on the writer wave before the freeze; the mistake is that
  A3 changed the gate after that run and the changed gate was frozen without being re-run (it already printed
  `blind_violations=1` at `55f9a694`), plus the gate's first-forbidden-line-only reporting, which masked the second hit.
- **M6 (new) — the writer brief contradicted the gate (class: scope).** The brief required a closing sentence directly
  after `## Files opened` with nothing else under that heading, and told every seat to read RULES.md, which the A2
  allowlist forbade (`wave1-spec.json` writer items and context). Captured-by: none. Fix: route R5 again — the gate must
  end the files list at the first non-entry line, report every forbidden line, and its self-test must include a planted
  report written exactly to the brief.
- **M2 count:** five labels were wrong, not two (this lesson's own R3 correction; QUALITY 90 prints 5).
- **R2 text:** `kill.h` holds three prototypes (`:40-42`), not one; the `poll_loop_args_t` struct spans `:10-38`
  (wave-2 ReviewCorrectionsR2R3). The R3 closure pointer is `round-29-verifier-spotcheck.md:159`, not `:163`.
- **QUALITY 93 cannot fail on its stated property** (CriticLessonMistakes: its literal check passes round 29 and a
  sandbox with unadjudicated hits); carried as a named defect to round 31, not counted.
- **Entry fixes after wave 2:** three rows re-pointed to single-file case ids; the a2-09 and a2-10 rows no longer cite
  S160 (CriticC1Admission F5); §3 states that a non-active unit's last-invocation send is counted in no output field
  (F3, routed to the tool); §4 states the disputed shape has no older frozen case (F7); the recheck line is runnable (F8).
  SKILL `## Round30` rows 2–3 carry the same corrections.
- **Residuals carried to round 31:** the gate parser (M6), QUALITY 93, the uncounted last-invocation send, the
  retention policy's blindness to unit/pid/cmdline shapes (wave-2 SentinelPrivacy F1), the S159 row's overlap with S120
  (`Restart=always` already anchored there; S159 adds the commit-message purpose only), `corpus/README.md:337` stale
  `fleet-ledger` pointer (wave-2 ReviewProvinceFix).
