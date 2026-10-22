# SrcEarlyoomTagHistory — SOURCES row draft (earlyoom release/tag history and message-grammar stability)

Scope: open the earlyoom upstream release history (tags API, releases API, README changelog at tag
`v1.9.0`) and compare the message-grammar strings at tags `v1.7`, `v1.8` and `v1.9.0` from
`main.c` / `kill.c` / `msg.h`. Draft **one** `corpus/SOURCES.md` row plus its Gate line.
`corpus/SOURCES.md` was NOT edited (draft only). No lane commit, no jj, no product-code edit, no
unit started/stopped/enabled/restarted, no journal MESSAGE text read.

## Verdict in one line

`v1.9.0` is the tag that carries 1.9.0 (tagged 2025-09-16); of the three queried strings only
`sending SIGTERM when mem avail` changed (absent in v1.7, present and unchanged from v1.8 through
v1.9.0), while `sending %s to process` and `escalating to SIGKILL after` are present in all three
tags with only their trailing fields changed — so the **version line** (`earlyoom <version>`), not
the action line, is what identifies the grammar, and the contract's threshold grammar is a v1.8+
grammar that a v1.7-era invocation never emits.

## Gate

Source 1 — tag list

- URL: https://api.github.com/repos/rfjakob/earlyoom/tags?per_page=100
- Access date: 2026-10-22 (HTTP 200, 13,409 B); sha256 `423c43617a2a299315180292f43447936f6ddde01efff5baece3fc46ed8b1869`
- Tag names and commits (verbatim from the JSON, one per line): `v1.9.0` → `202d4db0d308ca6478f68de68b46cae34896ddaf`;
  `v1.8.2` → `d5791d300aafa77b8f6a3d3d97f481a4ef904a38`; `v1.8.1` → `4965c8315a3a5479b6241ac2ac96e674218df8fd`;
  `v1.8` → `62625072ce8671f497a5cea5fc3db63226469093`; `v1.7` → `ebaea9526bcee14889b00d83a9dd3d038315cee2`.
- There is **no** `v1.9` tag and no `v1.9.0` successor in the list; the newest tag is `v1.9.0`.

Source 2 — release metadata for `v1.9.0`

- URL: https://api.github.com/repos/rfjakob/earlyoom/releases?per_page=30
- Access date: 2026-10-22 (HTTP 200, 23,139 B); sha256 `1426146f23f0e2dd16047a6198ac8ad1c8f6138e5363661083e7bc40bcd35db8`
- Quote, release object for `v1.9.0` (verbatim, 6 words):
  > `"published_at": "2025-09-16T19:11:03Z"`
- The `v1.9.0` release **body is empty** (no prose to quote); the release carries no changelog
  text of its own, so the changelog fact comes from `README.md` (Source 4).

Source 3 — annotated tag object

- URL: https://api.github.com/repos/rfjakob/earlyoom/git/tags/66d78843fd675859a09a52d3f17b1c408a827a34
- Access date: 2026-10-22 (HTTP 200, 2,647 B); sha256 `25bd090a532234befc8afb338856e394c34bf7f58d822779e0c6ff08e0998bf6`
- Ref: https://api.github.com/repos/rfjakob/earlyoom/git/ref/tags/v1.9.0 → HTTP 200, 374 B,
  sha256 `ca30a768555117071a8d07b87366d62aa12f48215bfd302f2cd8ae9932a4b3cd`; the tag object
  `66d78843fd675859a09a52d3f17b1c408a827a34` points at commit `202d4db0d308ca6478f68de68b46cae34896ddaf`.
- Quote, tag object (verbatim, 3 words):
  > `"date": "2025-09-16T19:09:33Z"`

Source 4 — README at tag `v1.9.0`

- URL: https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md
- Access date: 2026-10-22 (HTTP 200, 19,931 B); sha256 `23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd`
- Quote, `README.md:283` (verbatim, 3 words):
  > `* v1.9.0, 2025-09-16`
- Quote, `README.md:299` (verbatim, 3 words):
  > `* v1.8, 2024-04-15`
- Quote, `README.md:310` (verbatim, 3 words):
  > `* v1.7, 2022-03-05`

Source 5 — `main.c` at tag `v1.9.0`

- URL: https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c
- Access date: 2026-10-22 (HTTP 200, 21,053 B); sha256 `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`
- Quote, `main.c:161` (verbatim, 5 words):
  > `fprintf(stderr, "earlyoom " VERSION "\n");`
- Quote, `main.c:414` (verbatim, 15 words):
  > `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`
- Quote, `main.c:416` (verbatim, 15 words):
  > `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`

Source 6 — `kill.c` at tag `v1.9.0`

- URL: https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c
- Access date: 2026-10-22 (HTTP 200, 21,169 B); sha256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`
- Quote, `kill.c:318` (verbatim, 7 words):
  > `warn("escalating to SIGKILL after %.3f seconds\n", secs);`
- Quote, `kill.c:627` (verbatim, 18 words):
  > `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",`
- Quote, `kill.c:654` (verbatim, 5 words):
  > `warn("kill failed: %s\n", strerror(saved_errno));`

Source 7 — earlier tags (the comparison)

- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.8/main.c → HTTP 200, 19,907 B,
  sha256 `9bdc8209af6f68403f1137a3e86e566a0ca137dc1ec5c46a1fdf099151b2834c`
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.8/kill.c → HTTP 200, 18,052 B,
  sha256 `459af5589d6cc092303dcc1e27783557e8a91e2820565a08fc5094bc87054133`
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.7/main.c → HTTP 200, 17,326 B,
  sha256 `ceaa208361fa112857e30928a0e727711b9da6e86cebaa2f100bbd3d02113412`
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.7/kill.c → HTTP 200, 12,166 B,
  sha256 `1453cd2a6a48de4bafef6032b40c421e433270fddd1bcc94e85a83d80ec65af8`
- Quote, `v1.7/main.c:326` (verbatim, 15 words):
  > `fprintf(stderr, "sending SIGTERM when mem <= " PRIPCT " and swap <= " PRIPCT ",\n",`
- Quote, `v1.7/kill.c:167` (verbatim, 7 words):
  > `warn("escalating to SIGKILL after %.1f seconds\n", secs);`
- Quote, `v1.7/kill.c:377` (verbatim, 15 words):
  > `warn("sending %s to process %d uid %d \"%s\": badness %d, VmRSS %lld MiB\n",`

Source 8 — `msg.h` at tag `v1.9.0` (percentage format)

- URL: https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h
- Access date: 2026-10-22 (HTTP 200, 1,027 B); sha256 `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`
  (identical at `v1.8`; `v1.7`'s `msg.h` is `e0e88f50e382bac81fb1d4f8511f8b1e012e4c76f26af64786b7f9265b0b3df2`).
  Quote, `msg.h:10` (verbatim, 2 words):
  > `#define PRIPCT "%5.2lf%%"`
- `msg.c` at `v1.8` and at `v1.9.0` is byte-identical (sha256 `a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197`).

## Cross-tag grammar comparison (exact strings)

| String | v1.7 | v1.8 | v1.9.0 | changed? |
|---|---|---|---|---|
| `sending SIGTERM when mem avail` | absent (`v1.7/main.c:326` says `mem <=`) | `main.c:382` | `main.c:414` | **introduced in v1.8**, unchanged v1.8→v1.9.0 |
| `SIGKILL when mem avail` | absent (`v1.7/main.c:328` says `mem <=`) | `main.c:384` | `main.c:416` | same |
| `sending %s to process` | `kill.c:377` | `kill.c:539` | `kill.c:627` | prefix stable; trailing fields changed twice (`badness` → `oom_score`+`cmdline` → `oom_score`+`oom_score_adj`+`cmdline`) |
| `escalating to SIGKILL after` | `kill.c:167` (`%.1f seconds`) | `kill.c:230` (`%.3f seconds`) | `kill.c:318` (`%.3f seconds`) | format changed at v1.8, unchanged since |
| `kill failed: ` | `kill.c:395` | `kill.c:558` | `kill.c:654` | unchanged |
| `low memory! at or below SIGKILL limits` | `main.c:431` | `main.c:487` | `main.c:519` | unchanged |
| `low memory! at or below SIGTERM limits` | `main.c:435` | `main.c:491` | `main.c:523` | unchanged |
| `dryrun mode enabled` | `main.c:224` | `main.c:263` | `main.c:295` | unchanged |
| version line `earlyoom " VERSION` | `main.c:109` | `main.c:132` | `main.c:161` | unchanged |

`v1.8`, `v1.8.1` and `v1.8.2` ship **byte-identical** `main.c` and `kill.c`
(sha256 `9bdc8209…b2834c` and `459af558…54133` for all three), so the v1.8.1 changelog line
"Fix trivial test failures caused by message rewording" (`README.md:295`) did not touch these two
files or the grammar.

## Draft row (exact column order of `corpus/SOURCES.md`)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S??? | earlyoom release and tag history with the logged-message grammar at tags v1.7, v1.8 and v1.9.0 — https://api.github.com/repos/rfjakob/earlyoom/tags ; https://api.github.com/repos/rfjakob/earlyoom/releases ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.8/main.c ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.8/kill.c ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.7/main.c ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.7/kill.c | tool | A | which upstream tag carries 1.9.0 and its date, and whether the earlyoom log-message prefixes `sending SIGTERM when mem avail`, `sending %s to process` and `escalating to SIGKILL after` are stable across tags v1.7, v1.8 and v1.9.0; the version line, the two threshold lines, the action line, the escalation line, the kill-failure line, the two low-memory warnings, the dry-run flag and the percentage format at those tags; not kill-selection logic, not the host's unit state, not kill history | tags API: `v1.9.0` → commit `202d4db0d308ca6478f68de68b46cae34896ddaf` (annotated tag `66d78843fd675859a09a52d3f17b1c408a827a34`, tagger date 2025-09-16T19:09:33Z); releases API: `v1.9.0` published 2025-09-16T19:11:03Z; README.md:283 (changelog head); main.c:161 (version), :414 and :416 (thresholds), :295 (dryrun), :519 and :523 (low memory); kill.c:318 (escalation), :627 (action), :654 (kill failed); msg.h:10 (PRIPCT); v1.8 main.c:382 and :384, kill.c:230 and :539; v1.7 main.c:326 and :328, kill.c:167 and :377; sha256 v1.9.0 main.c `08656b0b…f9d0e4`, kill.c `b32e0fad…00bf3`, msg.h `e3660498…de56c`, README.md `23411dbf…74dd`, msg.c `a771c915…5197`; opened 2026-10-22 | The `mem avail` threshold wording was introduced in v1.8 and is unchanged in v1.9.0, so a v1.7-era invocation prints `mem <=` and never the contract's threshold line; the action and escalation prefixes are stable across v1.7–v1.9.0 while their trailing fields change, so the version line, not the action line, identifies the grammar; percentages are printed through a width-5 field, so a single-digit threshold is space-padded. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |

Tier A — reason: the upstream project's own repository and release API, pinned to release tags,
fetched from the project's own endpoints; they are the primary authority for the message grammar
the tool matches, and the tag `v1.9.0` is the exact upstream release the host's binary carries
(`pacman -Q earlyoom` → `earlyoom 1.9.0-1`; `/usr/bin/earlyoom` contains the string
`earlyoom 1.9.0`). No secondary account, vendor page or mirror is used.

Status `mined` — reason: the row's facts are the anchors for the superseding round-26 entry
`corpus/knowledge/userspace-oom-killers-r26.md`, whose `source:` line cites a round-26
`corpus/SOURCES.md` row, and for the C2 tool's grammar version gate; the row therefore has a
consumer in this round. If the L1 prefers the registry's "admitted but not yet used" spelling, the
same row text with status `queued` and used-by `—` is equally consistent; the facts and Gate do
not change.

Split option — the registry keeps one row per URL for code files (S011, S013). If the L1 wants
that shape, the row above can be split into (i) a release-history row (tags API + releases API +
README changelog) and (ii) a code-grammar row (the six `main.c`/`kill.c`/`msg.h` files at the three
tags), with the same tier, status and recheck; the anchors split accordingly.

Registry note: `corpus/SOURCES.md` currently ends at **S113** (last registry row at file line 119).
The assignment mentioned "the last rows S098–S127"; rows S114–S127 do not exist yet, so the next
free id would be `S114` — the row above keeps the id as `S???` as instructed.

## Facts the round can rest on (with line numbers)

1. The tag that carries 1.9.0 is `v1.9.0`; there is no `v1.9` tag. Annotated tag object
   `66d78843fd675859a09a52d3f17b1c408a827a34` → commit `202d4db0d308ca6478f68de68b46cae34896ddaf`
   (tags API; `git/ref/tags/v1.9.0`; `git/tags/66d78843…`).
2. `v1.9.0` is dated 2025-09-16 three ways: tagger date `2025-09-16T19:09:33Z` (tag object),
   release `published_at` `2025-09-16T19:11:03Z` (releases API), README changelog head
   `* v1.9.0, 2025-09-16` (`README.md:283`). The earlier tags are dated `* v1.8, 2024-04-15`
   (`README.md:299`) and `* v1.7, 2022-03-05` (`README.md:310`).
3. The threshold wording `sending SIGTERM when mem avail <= … and swap free <= …,` exists at
   `v1.8/main.c:382` and `v1.9.0/main.c:414` and **not** in v1.7, where the line is
   `sending SIGTERM when mem <= … and swap <= …,` (`v1.7/main.c:326`); the SIGKILL counterpart
   follows the same change (`v1.7/main.c:328` → `v1.8/main.c:384` → `v1.9.0/main.c:416`).
4. `sending %s to process` is present at all three tags (`v1.7/kill.c:377`, `v1.8/kill.c:539`,
   `v1.9.0/kill.c:627`); only the fields after the prefix change (badness → oom_score + cmdline →
   oom_score + oom_score_adj + cmdline).
5. `escalating to SIGKILL after` is present at all three tags (`v1.7/kill.c:167` with `%.1f`,
   `v1.8/kill.c:230` and `v1.9.0/kill.c:318` with `%.3f`); the number format changed once, at v1.8.
6. `kill failed: ` (`v1.7/kill.c:395`, `v1.8/kill.c:558`, `v1.9.0/kill.c:654`),
   `low memory! at or below SIGKILL limits` (`main.c:431` / `:487` / `:519`),
   `low memory! at or below SIGTERM limits` (`main.c:435` / `:491` / `:523`),
   `dryrun mode enabled` (`main.c:224` / `:263` / `:295`) and the version line
   `fprintf(stderr, "earlyoom " VERSION "\n");` (`main.c:109` / `:132` / `:161`) are worded
   identically at all three tags.
7. Percentages are rendered by `PRIPCT`, defined as `"%5.2lf%%"` (`msg.h:10`): always two decimals,
   in a width-5 field, so a single-digit threshold is space-padded (`" 5.00%"`).
8. **Every line number the contract cites for tag `v1.9.0` matches the fetched bytes exactly:**
   `main.c:161` (version), `main.c:414` / `:416` (thresholds), `main.c:519–523` (low memory),
   `main.c:295` (dryrun), `kill.c:318` (escalation), `kill.c:627` (action), `kill.c:654` (kill
   failed). No contract line anchor is off.
9. The threshold lines are printed once per invocation straight to stderr (`main.c:412–417`), while
   the action, escalation, kill-failure, low-memory and dry-run lines go through `warn()`, which
   writes to syslog only when `--use-syslog` was given (`msg.c:19–40`; `main.c:298–300`) and to
   stderr otherwise; under systemd both land in the unit's journal.
10. `v1.8`, `v1.8.1` and `v1.8.2` ship byte-identical `main.c` and `kill.c`
    (sha256 `9bdc8209…b2834c`, `459af558…54133`), and `msg.c` is byte-identical between `v1.8` and
    `v1.9.0` (sha256 `a771c915…5197`); the v1.8.1 "message rewording" did not touch these files.
11. This host runs the same release: `pacman -Q earlyoom` → `earlyoom 1.9.0-1`; the installed
    `/usr/bin/earlyoom` contains the version string `earlyoom 1.9.0`.
12. Grammar-gate conclusion: the contract's grammar set is valid for `v1.8` and `v1.9.0` and is
    **not** valid for `v1.7`; within v1.8/v1.9.0 the only discriminator is the version line, so
    `grammar: "verified-1.9.0"` must be decided from the `earlyoom <version>` line and not from the
    action line.

## Flags for the L1 / contract

- **No contradiction with the contract.** Every line number the contract attributes to tag
  `v1.9.0` was reproduced byte-for-byte from the tag's own `main.c`/`kill.c` (fact 8). The contract's
  `grammar` value `verified-1.9.0` is consistent with the upstream tag, and the host binary is that
  release (fact 11).
- **Grammar-gate caution (the round's decision point):** a v1.8-era invocation emits the *same*
  `mem avail` threshold wording and the *same* action prefix as v1.9.0 (facts 3, 4). Only the
  version line separates them, so the tool must derive `verified-1.9.0` from the version line and
  must not treat "threshold line found" as proof of the 1.9.0 grammar. A v1.7-era invocation is the
  opposite case: its thresholds are unreadable by the contract's prefix, so `thresholds` would be
  `null` while the unit is active — which the contract's rule 2 already routes to
  `KILLERS_UNKNOWN` provided `grammar` is `unverified`.
- **Threshold capture caution:** the contract writes the threshold shapes as `<= <a>%`. Because
  `PRIPCT` is `"%5.2lf%%"` (`msg.h:10`), a single-digit value is space-padded — the emitted text
  can be `… swap free <=  5.00%,` (two spaces). A capture that does not tolerate whitespace between
  `<=` and the number will fail on `5.00` while succeeding on `10.00`. Also note the SIGTERM line
  ends with a comma and the SIGKILL line does not (`main.c:414` vs `:416`), and the SIGKILL line
  carries eight leading spaces (`main.c:416`) — the contract's "stripping leading whitespace" rule
  covers that.
- **Action-count caution:** the signal name in the action line can be `0 (no-op signal)` during
  earlyoom's startup self-test (`kill.c:620–624`, guarded by `enable_debug` at `:626`), so a
  `sending 0 (no-op signal) to process …` line exists in the format but must not be counted as a
  SIGTERM/SIGKILL action. The contract's grammar (`sending SIGTERM to process ` /
  `sending SIGKILL to process `) already excludes it.
- **Privacy:** nothing in this report contains journal MESSAGE text, a process name, a command
  line, a uid, or the value of an `--avoid`/`--prefer` expression. The upstream format strings
  quoted here contain the *shape* of the message, not any host event.
- **Registry shape:** `corpus/SOURCES.md` ends at **S113** (row at file line 119), not S127; rows
  S114–S127 do not exist, so the assignment's "last rows S098–S127" is a stale description of the
  file. The row keeps `S???` as instructed; the next free id would be `S114`.
- **Adjacency, not absorption:** S016 (earlyoom README at master commit `8477c902…`, README sha256
  `b2a34e35…0826c`, which differs from the tag's README) remains valid for the kill flow and the
  `--kernel-oom` delegation. This draft row is tag-pinned (`v1.9.0`) and covers the release history
  plus cross-tag grammar stability; it does not replace S016 and does not re-anchor its facts.
- **Date ambiguity, recorded but not load-bearing:** for `v1.8.1`/`v1.8.2` the README changelog
  dates (2024-04-17, 2024-05-07) differ from the release `published_at` dates (both 2024-05-13),
  so "the date of a tag" is ambiguous in general. For `v1.9.0` all three sources agree on
  2025-09-16.

## Verification trail

- `curl -sS -o tags.json 'https://api.github.com/repos/rfjakob/earlyoom/tags?per_page=100'` → HTTP 200,
  13,409 B, sha256 as recorded; parsed with `python3 -c` (json) to list name → commit sha.
- `curl -sS -o releases.json 'https://api.github.com/repos/rfjakob/earlyoom/releases?per_page=30'` →
  HTTP 200, 23,139 B, sha256 as recorded; parsed with `python3 -c`; the `v1.9.0` release body is the
  empty string.
- `curl -sS -o tagref_v1.9.0.json 'https://api.github.com/repos/rfjakob/earlyoom/git/ref/tags/v1.9.0'`
  → HTTP 200, 374 B; `curl -sS -o tagobj_v1.9.0.json '.../git/tags/66d78843…'` → HTTP 200, 2,647 B.
- `curl -sS -f -o ${t}_{main.c,kill.c,README.md} 'https://raw.githubusercontent.com/rfjakob/earlyoom/${t}/${f}'`
  for `t ∈ {v1.7, v1.8, v1.9.0}` → all HTTP 200; digests recorded above.
- `curl -sS -f -o ${t}_{msg.h,msg.c} …` for `v1.7`, `v1.8`, `v1.9.0`; `sha256sum` shows
  `msg.c` identical for `v1.8` and `v1.9.0` (`a771c915…5197`) and different for `v1.7`.
- `curl -sS -f -o v1.8.1_{main.c,kill.c} …` and `v1.8.2_{main.c,kill.c} …` → HTTP 200; `sha256sum`
  shows them identical to the `v1.8` files.
- `curl -sS -o tree_v1.9.0.json '…/git/trees/202d4db0d…?recursive=1'` → HTTP 200, 19,112 B, sha256
  `8b3c95cf…f3c145`, `truncated: false`; used to confirm the tag's file list (`msg.h`, `msg.c`,
  `globals.h` present; no `earlyoom.h`).
- `curl -sS -f -o v1.9.0_globals.h …` → HTTP 200, 133 B; `PRIPCT` is not defined there — it is
  `msg.h:10`.
- `grep -n -E 'sending |escalating|SIGKILL when mem avail|low memory!|dryrun mode|kill failed'`
  over the six `main.c`/`kill.c` files → the line numbers in the comparison table above.
- A Python scan over the six files for the ten contract grammar strings produced the exact hit
  lists; `sending SIGTERM to process` and `sending SIGKILL to process` have **no** literal hit in any
  file (the source emits `sending %s to process` with the signal name substituted at run time),
  which is why the contract's action prefixes are runtime spellings of `kill.c:627`.
- `pacman -Q earlyoom` → `earlyoom 1.9.0-1`; `ls -l /usr/bin/earlyoom` → 43,520 B, dated
  2025-09-17; `grep -a -o` over that binary → the string `earlyoom 1.9.0`. Read-only queries only.
- Scratch copies of every fetched byte live under
  `/fast/scratch/hyaku/mori-r26/MoriR26.SrcEarlyoomTagHistory/`.

## Out of scope

- Editing `corpus/SOURCES.md`, `corpus/knowledge/userspace-oom-killers-r12.md` or any other lane
  file (draft only).
- The `tools/mori-oom-killers.py` implementation, the fixture cases and the verdict codes
  (other seats); this row only fixes the grammar the tool may claim.
- The host's unit state, the journal contents, any kill history and the C1/C2 counting.
- The `systemd-oomd` side of FR10 (S007/S011/S013 and the v262 rows).

## Tooling

- No install, upgrade or downgrade was performed; no tool was needed beyond what the host already
  provides (`curl`, `python3` for JSON parsing and line scanning, `grep`, `sha256sum`, `pacman -Q`).
- All pacman transactions are PAUSED host-wide per the round bounds, so none was attempted;
  `pacman -Q` is a read-only query, not a transaction.
- Writes: this report file only. No jj command was run anywhere; no git write command was run; no
  lane commit was made; no unit was started, stopped, enabled or restarted; no product code was
  edited.
