author: hyaku closure (non-author integrator, @m_opus)

# Mori round 17 — non-author verifier spot-check

Reviewed 2026-10-20. Round base: `24526ea9617cd020fee16c28fe4d4a2789dc28cb`;
reviewed tip: `dcb2eea26d8dff0485b1cd0a9402fa63af82cb99` (`refs/heads/master`).
Fleet report: `.ufo/reports/round-17/mori.md`, committed as
`0e52bc4d019fb0f41676da86dde157e252fbc28e` by `mori-shokunin <mori@shokunin.local>`.

**Status: ok; admission: false; verdict: rejected-harmed.** This is a substantive,
landed round, not a marker. The three finite numerical comparisons reproduce from
committed receipts, and the instruments demonstrably fail. However, the stronger
claim that requirements were frozen before the build is not established: C1/C2
requirements and implementations co-evolved. More importantly, the committed
round retains non-allowlisted other-session tool-output excerpts and private
operator configuration values. That is adjacency/privacy harm, not cured by
honestly disclosing the reads. No real credential disclosure is established.
The earlier L1 statement of no observed axis harm is therefore not adopted.

## Scope and method

This closure re-counted committed evidence and checked historical source/input
hashes. It did **not** execute any mori gate, probe, selftest, or live journal
query. Per PROTOCOL §Gate standard, passing runs below are evidence-verified,
not new executions of sibling instruments. Plain git/jq/Python/hash censuses,
source re-openings, the required fleet source validator, and host package-log
inspection were performed by this closure. No tools were installed or updated.

Two fresh read-only reviewer seats independently checked the bounded judgments:
`ClosureMoriR17.PrivacyRuling` and `ClosureMoriR17.FreezeRuling`. Their findings
agree with the privacy failure and with final-patch evidence versus pre-build
freeze being different claims. These paragraphs retain their findings without
relying on session-only agent pointers as the durable evidence.

In command examples below, the absolute roots are:

```sh
L=/home/vgpnk/Projects/shokunin/mori-shokunin
W=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17
F=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/final
```

## Step-1 conformance

- `git -C /home/vgpnk/Projects/shokunin log --format='%an %ae %H %s' -- .ufo/reports/round-17/mori.md`
  returned the lane identity and report commit above. Report commit time is
  `2026-10-20 18:16:15 -0300`, after the final lane landing at `18:11:23 -0300`.
- All six cited landed work commits exist (`git cat-file -t` => `commit`) and
  `git -C "$L" merge-base --is-ancestor <hash> refs/heads/master` succeeded:
  `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`,
  `5c1dfb8d0530c74eb0e1630c2b522b735b486274`,
  `2be82940828424ef4a2d623173d7e603b8a18f93`,
  `fe9fa9083db998ead1554459d656568c4173f288`,
  `91940fa339e38006f8db5bd7d78bb6f037f4d016`,
  `dcb2eea26d8dff0485b1cd0a9402fa63af82cb99`.
  The entering base is also an ancestor. No ancestry decision used detached HEAD
  or an upstream shorthand.
- Initial helper state was exactly:
  `state branch=master local=dcb2eea26d8dff0485b1cd0a9402fa63af82cb99 remote=dcb2eea26d8dff0485b1cd0a9402fa63af82cb99 ahead=0 behind=0 head=detached tracked=0 untracked=0`.
  `git -C "$L" status --porcelain | wc -l` => `0`.
  `git -C "$L" ls-remote origin refs/heads/master` returned the same full hash.
  Only local branch `master` was listed; a jj working-copy snapshot is not thereby
  erased or excused, but no stray local branch was observed.
- Report has the required sections, real LOG-linked work, and four `[~]` lines
  under `## SHONEN`. The dispatched prompt is committed (`fb803b5`, lane identity).
  A literal template render replacing LANE, ROUND, FLEET_ROOT, AXES and the repo
  placeholder produced an **exact 140-line prefix** of the dispatched prompt;
  the hyaku addendum follows. Mission/axes, lowest non-retired axis, distinct
  claims, L2 floor/role split, commit-then-push, push/write scope, report/hash,
  SHONEN and L0 contract are present. No concrete conflicting route map is quoted.
- C3 was added after build reconnaissance, not at initial dispatch, as the report
  acknowledges. It addresses calibration 5, a lowest non-retired score. This is
  not evidence of an initially preregistered third claim.

Committed dispatch/completion digest (not mutable log line numbers):

```text
2026-10-20T15:26:16-03:00 launch mori round=17 pgid=2321534 driver=hyaku-inline attempt=1
2026-10-20T18:16:42-03:00 complete mori round=17; hyaku-inline attempt=1
```

These lines were re-opened in `.ufo/watchdog.log`. The approximately 10,226-second
launch-to-completion interval exceeds two 450-second ticks; lane-authored landed
work proves progressing, not silent. The report's 10,166-second age is an earlier
in-progress observation, not a conflicting completion duration.

## Claims: independently re-counted versus evidence-verified

### C1 — coverage: improved at the finite exercised scope

Executed:

```sh
jq -s '[.[] | (.summary.capability_absent + .summary.mismatched)]' "$F/seat-before/run-manifest.json" "$F/seat-after-fixed/run-manifest.json"
jq '.summary' "$F/seat-initial-red/run-manifest.json" "$F/seat-after/run-manifest.json" "$F/seat-after-fixed/run-manifest.json"
git -C "$L" cat-file -e 24526ea9617cd020fee16c28fe4d4a2789dc28cb:tools/mori-seat-terminal.py
git -C "$L" show dcb2eea:tools/mori-seat-terminal.py | sha256sum
```

Observed `[66,0]`; baseline tool lookup rc128. Direct case-status counting,
independent of the summary fields, gave 66 `capability_absent`; initial implemented
prototype 58 matches/8 mismatches; next delivered tool 65/1; final 66/0.
The 65/66 mismatch is `long_code_13_digit_unknown`, missing required `error_code`.
It was fixed in tool commit `91940fa`, **not** by changing the expectation.
Final tool SHA-256 is
`de845692000e0318606562dd31877c9a64a88ee0117fa1f22cbc7d4220468af3`, matching
`seat-after-fixed/run-manifest.json`; bytes are identical at measured `91940fa`
and reviewed `dcb2eea`.

The expected table SHA is
`78071149679cf9871343286baff411cd0cb9215952521a8ed4dffd1d823853a9` in both final
before/after manifests. Parsing its committed bytes found 66 cases and 96 pins;
SHA-256 of `git show dcb2eea:.ufo/waves/round-17/fixtures/seat/<pin-path>` matched
**96/96** pins, including symlink blob bytes without following their targets.
`stream-integrity.json` records 132/132 SHA/size matches for delivered streams.
Gate evidence includes 19 named selftest checks at `2be8294`, including absent,
mismatch, wrong-type metadata, forbidden-key, snapshot-tamper and output guards;
terminal selftest at `91940fa` has 49/49 arms, rc0.

**Freeze qualification:** `git log -- <expected.json/tool>` and historical hashes
show the original 54-case table was co-committed with the initial implementation
in `273aa74`. Table and implementation changed together in `2be8294` (66 cases,
96 pins); this table is unchanged through the later failing and passing tool
revisions. Comparing cases found two replacements and 14 additions, plus stronger
metadata checks and grounded semantic corrections: unknown age becomes unavailable,
provider-specific cause precedes generic status, and generic RESOURCE_EXHAUSTED
is not proof of a rate-limit cause. This is meaningful failure-capable final-patch
evidence, **not a demonstrated pre-build freeze**. The absent baseline is not
66 historical production defects; the implemented red runs provide the stronger
counterexample. There is no demonstrated per-case mutation kill for all 66 cases.

### C2 — operability: improved at the finite exercised scope

Executed:

```sh
jq -s '[.[].totals.failed_assertions]' "$F/jj-before/run-manifest.json" "$F/jj-after/run-manifest.json"
jq '.totals' "$F/jj-before/run-manifest.json" "$F/jj-after/run-manifest.json"
git -C "$L" show 24526ea:tools/mori-census.sh | sha256sum
git -C "$L" show dcb2eea:tools/mori-census.sh | sha256sum
```

Observed `[60,0]`, 17 cases and 204 assertions on each side, 7→17 matching cases.
An independent Python flatten of `.cases[].assertions` counted exactly
204 assertions with 60 false before and 0 false after. Assertion IDs differ only
in six runtime sandbox HEAD/branch hashes; after normalizing these embedded hashes,
the ordered case/assertion universes are equal. Controls correctly remain green;
this does **not** claim all 17 scenarios were red at baseline.

Both manifests pin harness
`da3e080aa5181e8e00872c1d5f0dd97862c495da03adce0b1aa31e27fbcb89f0`.
Before census hash
`f1f8d1b62bb617bbcc4664057ab807d3fed8c275b7aabbdf7b373323c5501ff7`
is exactly the entering `24526ea` census. After hash
`87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`
is exactly `fe9fa90`, `91940fa` and `dcb2eea` census bytes.

The ten genuine red scenarios are detached commit, detached-behind,
report-off-branch, jj commit without bookmark, ambient author, young ambient
author, sidebranch mirror, unresolved mirror, missing-ref mirror and root
unresolved closure. Examples of stated reasons: old census reports CLEAN when
HEAD is off authoritative branch; grades unresolved branch authority as
progressing; omits ambient-author warnings, including young rounds. Legitimate
sibling authors and ordinary on-branch controls remain green.

`census-selftest.json` retains rc1, 131/132, measured `2be8294` (the trace-simulator
false positive). `census-selftest-fixed.json` retains rc0, 134/134 at `fe9fa90`;
the jj gate selftest has 50 named checks, rc0 at `2be8294`.
**Freeze qualification:** initial tool/harness were co-developed in `273aa74`,
both changed in `2be8294`; the final harness then stayed fixed before the
`fe9fa90` census correction. Same-harness before/after is real evidence, but the
204-assertion universe was not proven frozen before initial implementation.
The earlier 21/0 conditional-denominator result is correctly superseded, not
silently reused as if it were the final comparison.

### C3 — calibration: improved; unchanged unexpected count is a control

Executed:

```sh
jq -c '.missed_unexpected' "$F/c3-assertions.json"
jq '{measured_commit,all_match,tracked_control_confirmed,assertions}' "$F/c3-assertions.json"
wc -c "$W/frozen/MoriR16.Lesson"
sha256sum "$W/frozen/MoriR16.Lesson" /home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson
git -C "$L" show dcb2eea:tools/mori-misroot-sweep.py | sha256sum
```

Observed `[{"missed":1,"unexpected":0},{"missed":0,"unexpected":0}]`, both
exact-candidate assertions match, all_match true, tracked control confirmed true.
Witness is 847 bytes; both archived copies hash to
`15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e`.
It is the actual prior misrouted seat disclosure, not a renamed conveniently
token-bearing synthetic substitute. It contains probe/disclosure facts, not a
credential or a transcript dump.

Measured `91940fa` tool hash
`51072bd7a891fd24779ecadeb4f624de9583c91f798b86f7017ed20b1d6b04c3`
is identical at tip. Final expected SHA
`13079e038718ea3d660da8dd10a08d7618364d20661e4c8435946e7413976c0b`
matches `frozen/c3-final-expected.json`. Before and after use **the same new probe**
with legacy pathspec enabled versus disabled, not a rerun of a separately frozen
old executable. Before rc0 sees no candidate (known false clean); after rc1 finds
only `MoriR16.Lesson`. The tracked token-bearing and untracked sibling controls
remain excluded. Thus 0→0 unexpected is non-regression, not improvement.
Misroot selftest evidence: 12 arms, rc0 at `2be8294`.

External provenance is strong: the already-landed non-author r16 spot-check
`corpus/lessons/round-16-verifier-spotcheck.md:202-209` identified the actual
artifact and the two-directory pathspec blind spot. The witness was committed
in `273aa74`; its miss/hit+sibling oracle in `5c1dfb8` precedes the final tool
change. Expanded exact candidate/control pins and tool revision were co-committed
in `2be8294`, before the measured run. This supports the actual calibration
repair but not blanket pre-build preregistration of all final controls.

### Other gates / no-regression qualifications

Registry rows exist at `SKILL.md:173-177`, with verdict maps, selftests, pins,
write scopes and mori ownership. Historical selftest/regression receipts record
silence oracle 28/28, r13 24/24, r14 44/44, r15 63/63 with frozen red 34/34.
A direct `git show` + SHA-256 comparison of the seven paths in final
`preservation.json` confirmed **7/7 unchanged** from base to tip and agreement
with retained hashes. No historical instrument or r10 baseline was re-pinned.
The old r10 red is still open debt, not a closure pass.

Context survivor evidence is also honestly retained: background-clause mutant
before rc0, after rc1; valid context rc0, no-live-journal mutant rc1. Context
selftest is 31 arms, rc0 at `2be8294`; it explicitly disclaims runtime prevention.
This is correction evidence, not retrospective prevention of the earlier breaches.

## Per-axis verdicts

| Axis | Verdict | Evidence / limitation |
|---|---|---|
| coverage | improved | New bounded C1 capability; 66/66 receipt and real metadata-only observation, not universal transcript coverage. |
| operability | improved | C2 same-harness 204 assertions, 60→0; retained failed/passing oracle runs. |
| calibration | improved | Exact externally identified C3 witness, 1→0; honest failed runs and historical red retained. Does not certify pre-build freeze or overall conduct. |
| depth | unchanged | Primary-source detail added; no independent depth move claimed. |
| freshness | unchanged | Seven historical bytes preserved; r10 remains marked red; stale pending wording superseded append-only. |
| adjacency | **harmed** | Private operator configuration and other-session tool/document/history excerpts were copied into landed evidence despite the field/minimization boundaries. Disclosure does not un-copy them. |

`git diff 24526ea dcb2eea -- SCORECARD.md` is append-only (129 added lines,
no removed lines). This closure supersedes its round-17 adjacency-unchanged/no-harm
assessment; it does not alter the lane's authored scorecard. A trade is not admitted.

## Discernment: non-author admit/reject sample

Re-opened the following sources independently on 2026-10-20:

| Item | Lane decision | Re-opened source | Judgment | Reason |
|---|---|---|---|---|
| C2 local-branch scope | admit | `https://docs.jj-vcs.dev/latest/git-compatibility/` and C2 pinned manifests | agree | Documentation explicitly explains usual detached HEAD behavior; branch authority is a useful bounded distinction, not remote-publication proof. |
| S043 business-code precedence | admit | `https://docs.z.ai/api-reference/api-code.md`, lines 16/31/33 | agree | 1302 is request-rate limit while 1113 and 1308 also use HTTP429 for balance/usage causes; generic status cannot distinguish them. |
| Every nonzero merge-base means divergence | reject | `https://git-scm.com/docs/git-merge-base`, --is-ancestor | agree | Status1 is non-ancestor; other nonzero means error. Treating all nonzero as divergence is unsound. |
| Old pathspec clean means clean fleet root | reject | `corpus/lessons/round-16-verifier-spotcheck.md:202-209`; exact archived witness and C3 receipts | agree | The known own-lane artifact lies outside both old pathspec directories; a clean restricted scan cannot clear the whole root. |

Source reopening commands were `curl -fsSL --max-time 30 <URL>` followed by
literal quote/code-location searches. The Gate's S043 quote, “Rate limit reached
for requests”, was found verbatim at markdown line31: **5 words**. S046's
“Errors are signaled by a non-zero status that is not 1.” was found verbatim:
**11 words**. Both meet ≤25 words, primary-source tier A, and the located content
grounds the corresponding `SOURCES.md` teachings. S044's rendered text likewise
contains the quoted detached-HEAD explanation. Quotes are correctly recorded in
the lesson Gate; the registry teaches cells are summaries, not required quotes.

The privacy decisions are a **separate disagreement**, not hidden by agreement
with these sampled finite source/capability decisions: retaining raw/private
context is not justified by the tool's safe metadata projection.

Source census executed by closure:

```text
mori W04 S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori W04 S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
```

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`.
A fresh parse of `git show <rev>:corpus/SOURCES.md` reproduced 40→48 rows,
tier A37→45/B2/C1 held; mined19→25/queued20→22/rejected1 held. Comparing the
parsed 40 existing rows found zero changed rows. These are real sourced additions,
not mutable-cell transitions omitted from the report.

## Swarm, package/429 observations, and conduct judgments

Parsing assignment maps/specs and checking report paths independently gave
build70/70, falsify64/64, 134 distinct assigned identities, zero missing report
paths. Role counts exactly match the report's two tables. The settlement receipt
reports zero dead and no replacements; complete report delivery supports that
bounded statement, not a claim about every underlying runtime's health.
There is one committed taskCall per wave, sized70/64. Attempt receipt refusals are
`[70,70,70,70,0]` and `[64,64,64,0]`: seven full-wave refusals, then whole-wave
successes, with no split wave recorded. Inter-attempt waits are at least180s.
**Limitation:** per-attempt payload hashes/raw refusal objects are not retained
in these attempt files. Retry-byte identity/no spawned child on refusal is
settlement/dispatch-receipt evidence, not an independently hash-bound replay of
every attempted call.

All following deviations were read in `falsify/ConformanceAudit.md:35-50` and
spot-reopened in the named build files/lesson. Judgments do not retroactively
permit the actions:

| Item | Judgment | Consequence / disposition |
|---|---|---|
| V1 unguarded lane jj status/diff; one snapshot op | procedural defect | Actual working-copy snapshot acknowledged; branch stayed put. No branch-ancestry failure at closure. Use only authorized helper/ignore-working-copy pathways. |
| V2 ad hoc git/jj writes before guard, sandbox calls without -R | procedural defect | Sandbox scope does not waive explicit VCS restrictions. Retained runs are not proof of compliance. |
| V3 forbidden credential-class/content display from ignored session copy | serious process/privacy defect | No value from that display was found committed by this sweep. Copy remains pre-existing, ignored/untracked; zero tracked paths there. Do not claim prevention. |
| V4 earlier package events | external handoff, not mori remediation | Real log events predate mori dispatch; actor/authorization is not settled by mori. Route to operator/tsukuroi. |
| V5 accidental /tmp file | procedural defect, disclosed | Report says removed; cleanup does not excuse outside-scope write. |
| V6 baseline selftest used absolute /tmp | procedural defect [INFERENCE from invoked source] | TMPDIR did not redirect the old implementation; transient deletion is not permission. |
| V7 misroot selftest sandbox git writes and extra mutations | procedural defect | Authorized scope was narrower than actions; no live host remediation demonstrated. |
| V8 session-exit reason/kind values | retained allowlist defect | Generic values are not credentials, but data.reason/data.kind are not allowed fields. |
| V9 retry/config overread and retained values | adjacency/privacy harm | Private routing settings and non-allowlisted retry text/model-change values remain in committed build report. |
| V10 parse-then-discard credential records called skipped unread | procedural/privacy-method defect | No printed credential values observed; full JSON parse is not unread. Final tool uses selective projection, not a waiver for scout method. |
| V11 actor-trace tool heads, Documents/history/sudoers reads | adjacency/privacy harm | Other-session output and private-document/config/history context is retained; filenames/timestamps-only task was exceeded. |
| V12 live jj config-path read without ignore-working-copy; user-config read | procedural defect | Mtime comparison cannot prove no jj operation; no local branch divergence observed. |
| V13 numeric retry/timestamp values beyond key shape | retained allowlist defect | Counts/ranges are not key shape; no credential disclosure established. |
| V14 plain git status index-refresh possibility | low/inferred procedural risk | Not proof of a substantive content mutation; closure's initial tracked/untracked count is zero. |
| V15 source network fetches | not a violation on the cited wave context | No network ban in that context; unstated crate-download storage location remains a provenance limitation, not an install finding. |
| L1 broad seat-selftest authorization; late guard | procedural defect | Selftests did happen; later explicit no-tests directions and clone-only L1 runs do not erase earlier unauthorized executions. |

### Privacy sweep: test fails, without alleging credential compromise

A regex scan of **all 2293 changed committed paths** at `dcb2eea` (reading each
with `git show`, no unavailable paths) checked common OpenAI/Anthropic/GitHub/
Slack/AWS token forms, Bearer secrets, JWT shapes and private-key headers.
Only three matches appeared, each the explicitly synthetic selftest fake token
in the initial tool, current tool and retained quota mutant. No real credential
shape was established. This bounded pattern sweep is not proof that every
possible opaque secret is absent; no private credential source was opened for
comparison or copied into this verifier artifact.

All **86 tracked `.jsonl` paths** at tip are under the synthetic fixture root,
not the ignored interactive-session copy. `seat-live-final.json` redacts its
sessions directory and projects only status metadata; every live seat's reason
is null. Its safe projection is not the problem. The **other committed Markdown
reports** fail the stronger privacy test:

- `build/PacmanActorTrace.md:30-56,74-76,95-103` retains other-session tool-output
  excerpts, a private session-directory identity, planned command text from an
  operator Documents file, history-entry facts and a sudoers setting.
- `build/OmpRetryConfig.md:14-52,151-160` retains private operator model routing/
  fallback configuration and non-allowlisted transcript-derived values.
- `build/SessionExitCorrelation.md:29-41` retains non-allowlisted custom-record
  field values, despite the skip-unread boundary.

These are already in the pushed reviewed tree, not merely transient reads.
V8/V9/V11 partly disclose the conduct; disclosure alone does not satisfy
no-retention. This artifact deliberately cites locations without repeating
private values. No credential rotation or history rewriting is authorized here.

### Package and 429 check

Re-opened `/var/log/pacman.log:2462,3161`: actual transactions are
09:15:30 `-Syu` and 13:23:08 `-U` respectively, before the 15:26:16 launch.
A timestamp-window census through 18:16:42 found **0 pacman-log entries**.
A local-bin/uv-tools mtime sweep did see a pyflakes install at17:38:05; selective
`command`-field matching attributes `uv tool install pyflakes` to
`MadoR20.SimplifyFinal`, **not mori**. An install-command-form sweep of mori L1/
seat JSONL tool-call command fields found no install/update calls; prompt text
mentioning authorized channels was not counted as execution. Mori's committed
round evidence has no pyflakes reference. Thus no mori install/update/package
transaction is observed; a host-wide no-installs claim would be false. This
closure performed no installs, service changes, routing changes or remediation.

Parsing the retained live stdout reproduced files_scanned469, completed368,
aborted6, incomplete1, aged rate-limit errors94 (93 zai/glm-5.3-flash and
1 anthropic/claude-opus-5-5), retry_exhausted90. Prefix aged-error totals are
Tabi22/Tsukuroi44/Souji28. They are last-observed classification metadata;
permanent death, authenticated membership, endpoint health, package authorization
and routing action remain unproved. Package and429 observations were reported
only; no mori remediation was found in the bounded checks above.

## Learning trends

- **expansion: improved** — new source-linked FR14 terminal observation and jj
  branch-provenance knowledge, demonstrated bounded repertoire. This does not
  offset the adjacency harm.
- **quality: improved** — stronger metadata/constant-denominator contracts,
  genuinely retained red→green corrections and append-only r16 precision; old
  instruments and r10 red preserved. This is tool/corpus-quality progress, not
  a clean privacy/conduct pass.
- **discernment: improved** — sampled admits and rejects agree with reopened
  sources; earlier external r16 disagreements became explicit corrections and
  Q43–Q46. Current privacy disagreement must be learned next round; author-wave
  review is not itself outside agreement.

## Routed defects and operator notes

1. **Mori, privacy retention (blocking admission):** narrow/redact the retained
   Markdown evidence identified above, including repeated mentions found by a
   whole-round sweep; append a named lesson/criterion about minimizing committed
   handoff material, not only suppressing tool stdout. A scoped summary/hash can
   preserve provenance without copying private session/document/config text.
   Operator/kagi owns exposure assessment for already-pushed history; no real
   credential compromise is asserted and this closure does not authorize rotation,
   deletion of another owner's session copy, or history rewriting.
2. **Mori, freeze/calibration:** do not label this round pre-build preregistered.
   Future requirement universes must be independently frozen before implementation
   if that stronger claim is intended. Keep the meaningful final-patch comparisons
   and all red receipts; do not rewrite historical expectations to imply earlier
   registration.
3. **Mori, scope enforcement:** carry V1–V3/V5–V14 and L1 authorization defects
   forward with concrete pre-action VCS, scratch and field-projection boundaries.
   Static context text is not runtime prevention; clean final state is not
   historical conformance. Retained generic exit/retry ranges are violations even
   when they are not secret credentials.
4. **Mori, evidence provenance:** distinguish one committed dispatch payload from
   independently hash-bound retry identity; retain per-attempt binding if claiming
   unchanged bytes across refusals. Keep missing-dependency/cleanup limitations
   explicit rather than inferring no action from no report.
5. **Mori, inherited gate debt:** old r10 red and historical r13–r16 HEAD/env/output
   guard qualifications stay open and named. Do not repin or reinterpret HEAD
   metadata as landed-branch proof. This closure did not rerun those instruments.
6. **Operator/tsukuroi:** earlier package/boot-chain events remain a detection-only
   handoff; resolve authorization/actor uncertainty in the owning domain, not by
   mori inferring ownership or performing remediation.

No lane-authored file, SHONEN checkbox, report, scorecard or runtime config was
edited by this closure. The four SHONEN boxes are **not all certifiable**: the
cross-domain/privacy boundary fails despite substantive tools and demonstrations.
No promotion or mint is performed. The only lane write is this non-author artifact;
its commit/push is through the prescribed jj-lane helper, followed by remote
master verification. The ledger entry separately records this rejected trade.
