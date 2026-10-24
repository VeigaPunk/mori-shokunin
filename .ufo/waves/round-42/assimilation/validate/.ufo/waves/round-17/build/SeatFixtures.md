# SeatFixtures — C1 synthetic fixture packs (round 17, wave 1)

> **Amendment A1 update (2026-10-20):** the A0 counts, hashes and wants below
> are historical. The appended **Amendment A1 delta** section supersedes them
> (54 cases, 44 pack dirs incl. absent `MissingDir`, tree `pins`, readable
> fixtures only).
>
> **A2 strengthening update (2026-10-20):** the appended **A2 fixture
> strengthening** section supersedes both (59 cases, 49 pack dirs, 89 pins).
>
> **PrivacyFinal parser update (2026-10-20):** final state is **66 cases,
> 56 pack dirs (55 present + absent `MissingDir`), 96 pins**; see the
> appended **PrivacyFinal parser counterexamples** section for the final SHA.

Executor: `MoriR17.SeatFixtures-5` (leaf; advisory only). Delivered into this
executor's clone, never the lane checkout:

```
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatFixtures/.ufo/waves/round-17/fixtures/seat/
```

Tree: 34 pack directories (33 present + intentionally absent `MissingDir`),
42 cases in `expected.json`, 61 regular files plus 3 symlinks under the packs.
Every transcript is synthetic ASCII written only from the contract's documented
record shapes (`message`, `session_init`, `custom`, `credential_pin`); no real
session bytes were read or copied. No C1 tool was run (it does not exist yet at
this base); no mutating VCS command, no install, no background work started,
nothing written to `/tmp`.

Per wave rules the executor performs no VCS mutation, so "committed" here
means the fixture files are written into the executor clone's tree for L1
integration, not that a git commit was made.

## Verdict

Fixture deliverable is complete and internally consistent: 42/42 cases match a
contract-derived independent oracle; coverage includes every terminal class,
every listed `errorMessage` token, rate-limit-before-quota ordering, nested
dirs, prefix attribution/filtering, tail boundaries, symlinks/non-jsonl
ignores, the credential_pin trap, chmod-000 unreadable input, empty dir rc0,
missing dir rc2 and the max-files rc2 bound. Residual risks are gate-side
(see Risks), not fixture-side.

## expected.json shape and invocation convention

`expected.json` is exactly `{"cases":[...]}` as the contract prints it. Each
case:

* `id` — unique snake_case id.
* `pack` — pack directory name under `fixtures/seat/`.
* `args` — **extra flags only**, never `--sessions-dir` (agreed 2026-10-20 with
  `MoriR17.SeatGate-5`: gate substitutes `{pack}`/`{fixtures}` and prepends
  `--sessions-dir <fixtures>/<pack>` when absent).
* `want` — `{rc, finding, totals, seats}` on rc0/rc1; on rc2 only
  `{rc, finding}` (no fabricated totals for a setup refusal).
* `want.seats` is the contract's projection `{seat: class}`; tool output
  `seats` is a list of per-seat objects sorted by seat id and the gate projects
  it to `{seat: class}` (agreed with `MoriR17.SeatTool-5` and `SeatGate-5`).
* `want.totals` always carries all seven class keys, zeros included, and
  `sum(totals) == len(seats)`.

## Case table (42 cases)

| case id | pack | args | rc | finding | seats -> class | totals (nonzero) |
|---|---|---|---|---|---|---|
| `rate_limit_zai_status_429` | RateLimitStatus429 | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `zai-status-429`→`dead_rate_limit` | dead_rate_limit:1 |
| `rate_limit_zai_token_429` | RateLimitToken429 | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `zai-token-429`→`dead_rate_limit` | dead_rate_limit:1 |
| `rate_limit_zai_token_underscore` | RateLimitTokenRateLimitUnderscore | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `zai-token-underscore`→`dead_rate_limit` | dead_rate_limit:1 |
| `rate_limit_zai_token_capital` | RateLimitTokenCapitalRateLimit | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `zai-token-capital`→`dead_rate_limit` | dead_rate_limit:1 |
| `rate_limit_zai_token_upper` | RateLimitTokenUpper | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `zai-token-upper`→`dead_rate_limit` | dead_rate_limit:1 |
| `rate_limit_devin_resource_exhausted` | RateLimitResourceExhausted | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `devin-resource-exhausted`→`dead_rate_limit` | dead_rate_limit:1 |
| `rate_limit_zai_retry_exhausted` | RateLimitRetryExhausted | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `zai-retry-exhausted`→`dead_rate_limit` | dead_rate_limit:1 |
| `rate_limit_beats_quota_by_status_and_token` | RateLimitOrdering | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `status-beats-quota`→`dead_rate_limit`, `token-beats-quota`→`dead_rate_limit` | dead_rate_limit:2 |
| `quota_quota_word` | QuotaWord | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `quota-word`→`dead_quota` | dead_quota:1 |
| `quota_quota_usage_limit` | QuotaUsageLimit | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `quota-usage-limit`→`dead_quota` | dead_quota:1 |
| `quota_quota_402` | Quota402 | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `quota-402`→`dead_quota` | dead_quota:1 |
| `quota_quota_credits` | QuotaCredits | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `quota-credits`→`dead_quota` | dead_quota:1 |
| `completed_after_mid_session_error` | Completed | — | 0 | `MORI_SEAT_TERMINAL_OK` | `completed-after-error`→`completed` | completed:1 |
| `completed_trailing_nonmessage_records` | CompletedTrailing | — | 0 | `MORI_SEAT_TERMINAL_OK` | `completed-trailing-nonmessage`→`completed` | completed:1 |
| `aborted_terminal` | Aborted | — | 0 | `MORI_SEAT_TERMINAL_OK` | `aborted-terminal`→`aborted` | aborted:1 |
| `aborted_beats_error_fields` | AbortedErrorFields | — | 0 | `MORI_SEAT_TERMINAL_OK` | `aborted-with-error-fields`→`aborted` | aborted:1 |
| `error_other_thinking_and_bare` | ErrorOther | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `bare-error`→`dead_error_other`, `thinking-loop-error`→`dead_error_other` | dead_error_other:2 |
| `incomplete_toolresult_terminal` | IncompleteToolResult | — | 0 | `MORI_SEAT_TERMINAL_OK` | `incomplete-tool-result`→`incomplete` | incomplete:1 |
| `incomplete_user_terminal` | IncompleteUser | — | 0 | `MORI_SEAT_TERMINAL_OK` | `incomplete-user`→`incomplete` | incomplete:1 |
| `incomplete_tooluse_and_no_stop_reason` | IncompleteToolUse | — | 0 | `MORI_SEAT_TERMINAL_OK` | `no-stop-reason`→`incomplete`, `tool-use-terminal`→`incomplete` | incomplete:2 |
| `unavailable_empty_file` | UnavailableEmpty | — | 0 | `MORI_SEAT_TERMINAL_OK` | `empty`→`unavailable` | unavailable:1 |
| `unavailable_malformed_and_shape` | UnavailableMalformed | — | 0 | `MORI_SEAT_TERMINAL_OK` | `malformed`→`unavailable` | unavailable:1 |
| `unavailable_non_message_records_only` | UnavailableNonMessage | — | 0 | `MORI_SEAT_TERMINAL_OK` | `non-message-only`→`unavailable` | unavailable:1 |
| `unavailable_unreadable_file` | UnreadableFile | — | 0 | `MORI_SEAT_TERMINAL_OK` | `locked`→`unavailable`, `open`→`completed` | completed:1, unavailable:1 |
| `empty_dir_no_jsonl_rc0` | EmptyDir | — | 0 | `MORI_SEAT_TERMINAL_OK` | — | all zero |
| `missing_dir_rc2` | MissingDir | — | 2 | `MORI_SEAT_TERMINAL_SETUP` | — | — |
| `max_files_exceeded` | MaxFiles | `--max-files 1` | 2 | `MORI_SEAT_TERMINAL_SETUP` | — | — |
| `max_files_two_allowed` | MaxFiles | `--max-files 2` | 1 | `MORI_SEAT_TERMINAL_DEAD` | `max-a`→`completed`, `max-b`→`dead_rate_limit` | completed:1, dead_rate_limit:1 |
| `nested_directories` | NestedDirs | — | 0 | `MORI_SEAT_TERMINAL_OK` | `deep-seat`→`completed`, `deep-two`→`incomplete`, `shallow-seat`→`aborted` | completed:1, aborted:1, incomplete:1 |
| `prefix_all` | PrefixAttribution | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `KumitateR17-2.Q`→`aborted`, `SoujiR17-3.W`→`completed`, `SoujiR17-3.Z`→`dead_quota`, `SoujiR17-30.Trap`→`aborted`, `TsukuroiR17.X`→`completed`, `TsukuroiR17.Y`→`dead_rate_limit`, `TsukuroiR17Extra.Xtrap`→`completed` | completed:3, aborted:2, dead_rate_limit:1, dead_quota:1 |
| `prefix_filter_tsukuroi` | PrefixAttribution | `--prefix TsukuroiR17` | 1 | `MORI_SEAT_TERMINAL_DEAD` | `TsukuroiR17.X`→`completed`, `TsukuroiR17.Y`→`dead_rate_limit` | completed:1, dead_rate_limit:1 |
| `prefix_filter_souji` | PrefixAttribution | `--prefix SoujiR17-3` | 1 | `MORI_SEAT_TERMINAL_DEAD` | `SoujiR17-3.W`→`completed`, `SoujiR17-3.Z`→`dead_quota` | completed:1, dead_quota:1 |
| `prefix_filter_kumitate` | PrefixAttribution | `--prefix KumitateR17-2` | 0 | `MORI_SEAT_TERMINAL_OK` | `KumitateR17-2.Q`→`aborted` | aborted:1 |
| `prefix_filter_multi` | PrefixAttribution | `--prefix TsukuroiR17 --prefix SoujiR17-3` | 1 | `MORI_SEAT_TERMINAL_DEAD` | `SoujiR17-3.W`→`completed`, `SoujiR17-3.Z`→`dead_quota`, `TsukuroiR17.X`→`completed`, `TsukuroiR17.Y`→`dead_rate_limit` | completed:2, dead_rate_limit:1, dead_quota:1 |
| `prefix_filter_no_match` | PrefixAttribution | `--prefix Tsukuroi` | 0 | `MORI_SEAT_TERMINAL_OK` | — | all zero |
| `tail_small_window_far_terminal_lost` | TailBoundary | `--max-tail-bytes 1000` | 0 | `MORI_SEAT_TERMINAL_OK` | `tail-far`→`unavailable`, `tail-near`→`completed`, `tail-partial`→`completed` | completed:2, unavailable:1 |
| `tail_default_window_all_classified` | TailBoundary | `--max-tail-bytes 262144` | 0 | `MORI_SEAT_TERMINAL_OK` | `tail-far`→`completed`, `tail-near`→`completed`, `tail-partial`→`completed` | completed:3 |
| `tail_tiny_window_all_unavailable` | TailBoundary | `--max-tail-bytes 64` | 0 | `MORI_SEAT_TERMINAL_OK` | `tail-far`→`unavailable`, `tail-near`→`unavailable`, `tail-partial`→`unavailable` | unavailable:3 |
| `non_jsonl_files_ignored` | NonJsonlIgnored | — | 0 | `MORI_SEAT_TERMINAL_OK` | `good`→`completed` | completed:1 |
| `symlinks_never_followed` | SymlinkIgnore | — | 0 | `MORI_SEAT_TERMINAL_OK` | `real`→`completed` | completed:1 |
| `credential_pin_trap_skipped` | CredentialPinTrap | — | 0 | `MORI_SEAT_TERMINAL_OK` | `credential-trap`→`completed` | completed:1 |
| `mixed_one_seat_per_class` | MixedFinding | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `m-aborted`→`aborted`, `m-completed`→`completed`, `m-incomplete`→`incomplete`, `m-other`→`dead_error_other`, `m-quota`→`dead_quota`, `m-rate`→`dead_rate_limit`, `m-unavailable`→`unavailable` | completed:1, aborted:1, dead_rate_limit:1, dead_quota:1, dead_error_other:1, incomplete:1, unavailable:1 |

Full zero-inclusive totals are in `expected.json`; the table shows only nonzero
cells for width. Exact `seats`/`totals` are authoritative there.

## Pack digests (sha256)

Recipe (run from `fixtures/seat/`; per-pack aggregate over sorted per-file
`sha256sum` lines). `UnreadableFile/locked.jsonl` is temporarily chmod 600 for
hashing and restored to 000 afterwards; symlinks are excluded by `-type f` (they
are listed separately below).

```sh
chmod 600 UnreadableFile/locked.jsonl
find . -mindepth 1 -maxdepth 1 -type d | LC_ALL=C sort | while read -r d; do
  (cd "$d" && find . -type f -print0 | LC_ALL=C sort -z |
     xargs -0 sha256sum | sha256sum) | cut -d' ' -f1 | sed "s|^|$d  |"
done
chmod 000 UnreadableFile/locked.jsonl
sha256sum expected.json
```

| pack | files | sha256 (aggregate) |
|---|---|---|
| Aborted | 1 | `6b5588af658a0a848c2200a0de6683ef5bab1eec2d81e3a6161db2e7b3aa61b3` |
| AbortedErrorFields | 1 | `d89239b61f2642cc528324014d117e33deb3084319025dd627a2984f95036671` |
| Completed | 1 | `b1965fc67994f2a0fab88abeac620b410933850f5fae402da90f2ac8c4f02dde` |
| CompletedTrailing | 1 | `d5a68365d7b1cecb3433ae89372b11f965c6c81c846372eb8acc6e28c58df5f1` |
| CredentialPinTrap | 1 | `611de6148b0ad46e066c31e2a920b1f6df967d8f0ef6fc72e54dd6232f286449` |
| EmptyDir | 1 | `94fe3bc362dc9047f8395fb8b7df7a3dde4ecc4f8ed091c6d6f1c7c037803bd6` |
| ErrorOther | 2 | `b04c64402820636681e21245f0f00dab360da505eaa9a48fd49a801f9412737c` |
| IncompleteToolResult | 1 | `42cd91c7ac7412d943ae42313b0ae65a8009b11deb863569c0fc3c88b34bb19f` |
| IncompleteToolUse | 2 | `e20574c24fa45930089654fe91f5a1c414967a54a946586ed104e898202d72b7` |
| IncompleteUser | 1 | `632dd2b2ea6e4428af439db1d66422127fe692a47d7522ab9e941bb6fbb6bd22` |
| MaxFiles | 2 | `e0e547312146e3eaf0f51615fd351bd7d48665a852ebe7fd0d6f1014a360136d` |
| MixedFinding | 7 | `fc934b7c45b5e1d4ef4764f98451a8aae876ab2eab92c96951b782de61316297` |
| NestedDirs | 3 | `3b31b73f8dab8014b2ce1f8691225892f68d05752df4a5300c3baaab38653c03` |
| NonJsonlIgnored | 6 | `5bc572ac6be4ca687b30f7728616cfdaa66044fd25772f3e268f1938cb590472` |
| PrefixAttribution | 7 | `dccb63d88fdb2b7d5459d7c6b216f9a442046ba96ed071dd565f102ae52d08d3` |
| Quota402 | 1 | `d58d82bb5f9f857fbced8a0511906b9637f27ae112cad4e2cb3c1024d965a204` |
| QuotaCredits | 1 | `9d58133989c972d9781e7154f9448f1e3a26d78acacb47af50b2d002934c6d5a` |
| QuotaUsageLimit | 1 | `108917bf586a9e0bfd8c995211fffc8857d79aecac046fc1a6776f9348805ba0` |
| QuotaWord | 1 | `d49d4eba09f6fb2d19277bdc498ff4b8c3e556bb5efe1f3a8df5a65d541a8811` |
| RateLimitOrdering | 2 | `060ac6afbe65678637cdd40ad006938d1bcb39947ed593f62834e7011bddc12a` |
| RateLimitResourceExhausted | 1 | `eb919dff1771cb9c225ba4a4e56a403e777ea7b12325244a9cea82d9f6e546cb` |
| RateLimitRetryExhausted | 1 | `2704fce7679347f673bdbe9a4ca14df8f5e0eb254f1eb615dc4134113b568325` |
| RateLimitStatus429 | 1 | `8a4b73c65cce0e68f6fbbd9ec0ecb19d49036ab87328d2a2da21b276dfbc1d2a` |
| RateLimitToken429 | 1 | `fb830bbb602e0451846f8be5dcf9f7d2d4a16d6ca758a77cffe52c7356f90a89` |
| RateLimitTokenCapitalRateLimit | 1 | `ffe5a98011206cac4b6fe42ead47b5938f7261917fd2b5f4b070f1039b7777d9` |
| RateLimitTokenRateLimitUnderscore | 1 | `4199eb50aec1a0c0ad5867055d614377bb39faf0ede76266b6c5da903ca5a5b2` |
| RateLimitTokenUpper | 1 | `9ccaa876bdab8a3696e08508fd8b470dd5116e639bf6e30f9d0dbb74ee057794` |
| SymlinkIgnore | 3 | `efb1dc969e569f51deeb46f478e1c55d704dd339729b9eeb66e5281635a3ca9b` |
| TailBoundary | 3 | `d3025f0d0a166c3bc3488a0467b510e11e06f89bd8448b5a82b2894bef915e15` |
| UnavailableEmpty | 1 | `3135eeb0fa4de50c47583d1661fc9382624c82b553a1746e20977e625ea06db0` |
| UnavailableMalformed | 1 | `0deb89c3ed7bd26742cd4a810b75a8908df52428ef19d02912d13bdd0b3c1780` |
| UnavailableNonMessage | 1 | `0e46ece32868bc8a68230ae8f3dc49f6f72b24bae5636b9ba95326e62a4538ad` |
| UnreadableFile | 2 | `1a22038607035ac5e4958cc4f3cb77c0ecfe72f1c9eba2ac11db504ccfa75cea` |
| MissingDir | 0 (absent) | — intentional: no directory, rc2 case |

`expected.json` sha256: `239b9bccfccf30bd78a5466d524044773a5634831aa42a6d791cb6fba2fb574c`
(21607 bytes).

Non-regular entries (not covered by the `-type f` recipe):

* `SymlinkIgnore/Link.jsonl` → `trap.txt` (relative; trap payload is a
  `dead_rate_limit` message — a follower would emit a dead seat).
* `SymlinkIgnore/Dangling.jsonl` → `missing-target.txt` (dangling).
* `SymlinkIgnore/linked-dir` → `real-dir` (directory symlink, target has no
  `*.jsonl`).

## Coverage map

| required coverage | cases / fixture proof |
|---|---|
| completed | `completed_after_mid_session_error`, `completed_trailing_nonmessage_records`, `mixed_one_seat_per_class` |
| aborted | `aborted_terminal`, `aborted_beats_error_fields` (aborted keeps class despite 429/retry fields), prefix seats |
| dead_rate_limit, token `429` | `rate_limit_zai_token_429` (status 500, token path) |
| dead_rate_limit, token `rate_limit` | `rate_limit_zai_token_underscore` |
| dead_rate_limit, token `Rate limit` | `rate_limit_zai_token_capital` |
| dead_rate_limit, token `RATE_LIMITED` | `rate_limit_zai_token_upper` |
| dead_rate_limit, token `resource_exhausted` | `rate_limit_devin_resource_exhausted` |
| dead_rate_limit, `errorStatus == 429` only | `rate_limit_zai_status_429` (message has no token) |
| retry shape | `rate_limit_zai_retry_exhausted` (`Retry budget exhausted after 10 retries`, `429`, `(type=1302)`) |
| rate-limit before quota | `rate_limit_beats_quota_by_status_and_token` (status 429 + “quota exceeded”; and `quota 402 rate_limit credits`) |
| dead_quota, token `quota` | `quota_quota_word` |
| dead_quota, token `usage limit` | `quota_quota_usage_limit` |
| dead_quota, token `402` | `quota_quota_402` (status 402) |
| dead_quota, token `credits` | `quota_quota_credits` |
| dead_error_other | `error_other_thinking_and_bare` (thinking loop; bare error with no message) |
| incomplete role toolResult | `incomplete_toolresult_terminal` |
| incomplete role user | `incomplete_user_terminal` |
| incomplete assistant `toolUse` / missing stopReason | `incomplete_tooluse_and_no_stop_reason` |
| unavailable empty file | `unavailable_empty_file` |
| unavailable malformed/no-message | `unavailable_malformed_and_shape` (bad JSON, list, scalar, missing/non-dict message) |
| unavailable non-message records only | `unavailable_non_message_records_only` |
| unavailable unreadable file | `unavailable_unreadable_file` (`locked.jsonl`, mode 000) |
| nested directories | `nested_directories` (`a/b/c/deep-seat.jsonl`, `a/b/deep-two.jsonl`, `a/shallow-seat.jsonl`) |
| prefix attribution | `prefix_all`: `TsukuroiR17.X`, `TsukuroiR17.Y`, `SoujiR17-3.Z`, `SoujiR17-3.W`, `KumitateR17-2.Q` |
| prefix equality, not substring | `TsukuroiR17Extra.Xtrap` and `SoujiR17-30.Trap` are excluded by `--prefix TsukuroiR17` / `--prefix SoujiR17-3` |
| `--prefix` filtering (single/multi/none) | `prefix_filter_tsukuroi`, `_souji`, `_kumitate`, `_multi`, `_no_match` |
| terminal beyond max-tail from EOF ⇒ unavailable | `tail_small_window_far_terminal_lost` (`tail-far`, terminal first, 12,734 B file, window 1000) |
| huge early content, terminal near EOF ⇒ classified | same case + `tail_default_window_all_classified` (`tail-near`, 481,994 B, window 262144) |
| partial first tail line dropped | `tail-near`/`tail-partial` at 1000; window 64 proves record smaller than window ⇒ unavailable (`tail_tiny_window_all_unavailable`) |
| non-jsonl ignored | `non_jsonl_files_ignored` (`.txt`, `.json`, `.JSONL`, `.jsonl.bak`, dir named `Fake.jsonl`) |
| symlinks ignored | `symlinks_never_followed` (file link with dead payload, dangling link, dir link) |
| credential_pin trap, fake token | `credential_pin_trap_skipped` (`FAKE-SEAT-FIXTURE-TOKEN-NOT-REAL-0000` in `credential_pin` and `custom` records; terminal message stays `completed`) |
| empty dir rc0, zero totals | `empty_dir_no_jsonl_rc0` (`EmptyDir` has only `README.txt`) |
| missing dir rc2 | `missing_dir_rc2` (`MissingDir` absent) |
| max-files bound | `max_files_exceeded` (`--max-files 1`, two files, rc2), `max_files_two_allowed` (rc1) |
| rc1 only when a `dead_*` exists | every rc1 case has ≥1 dead seat; unavailable/aborted/incomplete-only cases are rc0 |

## Builder steps and fixture-specific notes

* `UnreadableFile/locked.jsonl` is a 0-byte file with mode `000`. Building it is
  a required fixture-builder step: write empty, `chmod 000` (restored after the
  hash pass). It is empty on purpose so the expected class is `unavailable`
  both as non-root (EACCES) and as root (empty tail), keeping the pack
  environment-stable.
* `EmptyDir` holds only `README.txt` (no `*.jsonl`) so the directory survives a
  copy/clone; the scan must still report rc0 with all-zero totals.
* `MissingDir` is intentionally absent; gate must pass its path without
  requiring existence.
* `TailBoundary` sizes: `tail-far.jsonl` 12,734 B (terminal first),
  `tail-near.jsonl` 481,994 B (terminal at EOF), `tail-partial.jsonl` 6,155 B
  (6,000-byte first line then terminal). Terminal message lines are >80 B, so
  `--max-tail-bytes 64` cannot contain one.
* `credential_pin` payloads carry only the visibly fake token above; no secret
  material was read, copied or invented from real values.

## Commands run (all read-only/build-only; no C1 tool invocation)

The fixture builder lived only in the executor's `.scratch` (never in the
fixture tree or lane) and was removed after generation; the deliverable is the
pack tree plus `expected.json`.

| command | rc | result |
|---|---|---|
| `TMPDIR=<clone>/.scratch python3 .scratch/build_fixtures.py <fixtures/seat>` | 0 | `oracle: 42 cases consistent` |
| `python3` shape check over `expected.json` | 0 | `shape ok; cases 42 packs 34`; only absent pack `MissingDir` |
| `sha256sum` per-pack aggregate recipe above | 0 | 33 digests; `expected.json` digest recorded |
| `stat`/`readlink` fixture inspection | 0 | mode `000` on `locked.jsonl`; link targets as listed |

Tool availability at build time: `tools/mori-seat-terminal.py` is absent in both
the executor clone and the lane checkout (`ls` rc2), so no tool run was
possible; fixture expectations are contract-derived only. No tool was installed
or upgraded (nothing recorded under the tooling directive).

## Risks / blockers

1. **Gate input hashing vs chmod-000.** If `mori-round17-seat-regressions.py`
   reads every fixture file to pin before/after SHA-256, `locked.jsonl` raises
   EACCES as non-root. The gate must hash metadata/skip-unreadable with a
   manifest note, or the whole run becomes setup rc2 instead of exercising the
   case. Flagged to `MoriR17.SeatGate-5`.
2. **MissingDir existence check.** A gate precondition requiring every `pack`
   directory to exist would reject `missing_dir_rc2`; the agreed interface is to
   pass the path and let the tool decide.
3. **Seats projection.** `want.seats` is a dict; tool output is expected as a
   list of per-seat objects. Gate must project; the contract's output wording
   (“Per seat emit …”, “seats (sorted by seat id)”) is the basis. [INFERENCE]
4. **rc2 want shape.** `totals`/`seats` are omitted for rc2 cases; the contract
   does not specify zero totals on refusal. Gate must compare only present want
   keys (agreed). [INFERENCE]
5. **Literal-token reading.** Token matching is case-sensitive/contains as the
   contract lists them; no lowercase “rate limit” negative case was added, to
   avoid encoding an ambiguous normalization rule.
6. **Prefix no-match rc0** and **missing stopReason ⇒ incomplete** are natural
   readings of “scan complete and zero dead” and “any other stopReason”.
   [INFERENCE]

---

# Amendment A1 delta (L1, 2026-10-20) — supersedes the counts/hashes/wants above

Updated in place in the executor clone at
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatFixtures/.ufo/waves/round-17/fixtures/seat/`.
All 42 prior case ids are retained; 12 cases were added and 3 prior wants were
changed. Final tree: **44 pack dirs** (43 present + intentionally absent
`MissingDir`), **54 cases**, **78 regular files**, **3 symlinks**, **0 source
FIFOs** (the FIFO is sandbox-generated from case metadata), and a top-level
`pins` map with **81 entries**. `expected.json` sha256:
`b684c63bf3cebe70f24d3d02f3f0df4f63aad3f547a365a3ca1864f5f57cb01f`.

A1 effects applied to every case/transcript:

* every `args` starts with `--now-ms 1761000000000`; no case relies on wall time;
* `want` uses `finding_id` (not `finding`);
* `want.totals` carries all eight classes, including `error_unsettled`;
* every `*.jsonl` intended as scannable starts with
  `{"type":"session","version":3}` within the first 4096 bytes (schema pack
  intentionally violates this);
* every deadline error record carries `completedAt` (or `timestamp` in one
  case); old records are `NOW-2000000`, settle boundary `NOW-900000`,
  60s-settle old `NOW-120000`, recent `NOW-100000`, timestamp-recent `NOW-50000`;
* default `--max-tail-bytes` is now 524288; the old explicit-window tail cases
  are unchanged and a default-window case was added.

## Case-table delta

| case id | pack | extra args (after --now-ms) | rc | finding_id | seats -> class | totals (nonzero) |
|---|---|---|---|---|---|---|
| `rate_limit_beats_quota_by_status_and_token` (CHANGED) | RateLimitOrdering | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `status-beats-quota`→`dead_quota`, `token-beats-quota`→`dead_quota` | dead_quota:2 |
| `prefix_filter_no_match` (CHANGED) | PrefixAttribution | `--prefix Tsukuroi` | 2 | `MORI_SEAT_TERMINAL_SETUP` | — | — |
| `mixed_one_seat_per_class` (CHANGED) | MixedFinding | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `m-aborted`→`aborted`, `m-completed`→`completed`, `m-incomplete`→`incomplete`, `m-other`→`dead_error_other`, `m-quota`→`dead_quota`, `m-rate`→`dead_rate_limit`, `m-unavailable`→`unavailable`, `m-unsettled`→`error_unsettled` | completed:1, aborted:1, dead_rate_limit:1, dead_quota:1, dead_error_other:1, error_unsettled:1, incomplete:1, unavailable:1 |
| `error_unsettled_default_settle` (NEW) | ErrorUnsettled | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `boundary`→`dead_rate_limit`, `recent`→`error_unsettled`, `timestamp-recent`→`error_unsettled` | dead_rate_limit:1, error_unsettled:2 |
| `error_unsettled_custom_settle_60` (NEW) | ErrorUnsettled | `--settle-seconds 60` | 1 | `MORI_SEAT_TERMINAL_DEAD` | `boundary`→`dead_rate_limit`, `recent`→`dead_rate_limit`, `timestamp-recent`→`error_unsettled` | dead_rate_limit:2, error_unsettled:1 |
| `code_quota_1113_beats_429` (NEW) | CodeQuota1113 | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `code-1113`→`dead_quota` | dead_quota:1 |
| `code_quota_1308_beats_429` (NEW) | CodeQuota1308 | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `code-1308`→`dead_quota` | dead_quota:1 |
| `code_rate_1302_beats_quota_token` (NEW) | CodeRate1302QuotaWord | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `code-1302-quota`→`dead_rate_limit` | dead_rate_limit:1 |
| `retry_after_1_retry` (NEW) | RetrySingle | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `retry-one`→`dead_rate_limit` | dead_rate_limit:1 |
| `main_session_excluded_from_totals` (NEW) | MainSessionExclusion | — | 0 | `MORI_SEAT_TERMINAL_OK` | `nested-ok`→`completed` | completed:1 |
| `duplicate_stems_two_entries` (NEW) | DuplicateStems | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | `d1/stem`→`dead_rate_limit`, `d2/stem`→`dead_rate_limit` | dead_rate_limit:2 |
| `schema_version_unavailable` (NEW) | SchemaVersionUnavailable | — | 0 | `MORI_SEAT_TERMINAL_OK` | `absent`→`unavailable`, `late`→`unavailable`, `version2`→`unavailable` | unavailable:3 |
| `malformed_lines_skipped` (NEW) | MalformedLineSkip | — | 0 | `MORI_SEAT_TERMINAL_OK` | `malformed-then-completed`→`completed` | completed:1 |
| `fifo_skipped` (NEW) | FifoSkip | — | 0 | `MORI_SEAT_TERMINAL_OK` | `real`→`completed` | completed:1 |
| `tail_a1_default_window` (NEW) | TailBoundary | — | 0 | `MORI_SEAT_TERMINAL_OK` | `tail-far`→`completed`, `tail-near`→`completed`, `tail-partial`→`completed` | completed:3 |

Semantics behind the delta:

* **Quota before rate limit (A1.1).** `RateLimitOrdering` now expects
  `dead_quota` for both a 429+“quota exceeded” record and a
  “quota 402 rate_limit credits” record. The id is retained for stability; its
  old name reflects A0 ordering.
* **Code before tokens (A1.10).** `(type=1113)` and `(type=1308)` force
  `dead_quota` under HTTP 429; `(type=1302)` forces `dead_rate_limit` even when
  the message also contains “quota”.
* **Settle window (A1.2).** Boundary record at exactly `now-900000` is settled
  (strictly newer is required for `error_unsettled`); `--settle-seconds 60`
  makes the 100 s-old record dead and keeps the 50 s-old `timestamp` record
  unsettled.
* **Main sessions (A1.3).** `MainSessionExclusion` has a root file
  `2026-10-20T15-00-00Z_0123abcd.jsonl` (matches the stem regex) whose terminal
  is a dead rate-limit error. It must be `kind: "main"`, counted in
  `main_sessions`, excluded from totals/dead/by_*; the graded seat is only
  `nested-ok` (completed), so rc0.
* **Duplicate stems (A1.3).** `DuplicateStems/d1/stem.jsonl` and
  `d2/stem.jsonl` are two entries with distinct `key` paths (`d1/stem`,
  `d2/stem`) and the same stem `stem`; totals count both rate-limits and
  `want.seats` is keyed by key paths. This also pins that `key` is the path
  relative to the sessions dir without `.jsonl`.
* **Prefix matched none (A1.4).** `prefix_filter_no_match` is now rc2
  `MORI_SEAT_TERMINAL_SETUP`, not a false clean rc0.
* **Schema (A1.6).** `SchemaVersionUnavailable` covers absent header, version 2,
  and a version-3 header pushed past byte 4096 by a 5000-byte first record;
  all three seats are `unavailable`.
* **Robustness (A1.5).** `MalformedLineSkip` has a valid header, malformed JSON,
  non-dict messages and an invalid-UTF-8 line, then a completed terminal;
  `FifoSkip` source holds only one regular completed transcript and case
  `fifo_skipped` carries `"fifo_files": ["pipe.jsonl"]`; the gate creates the
  FIFO only in its per-case sandbox, so only the regular seat is scanned.

## Pack digests (A1 final; sha256sum recipe over regular files)

Recipe unchanged from above, run from `fixtures/seat/` (symlinks are excluded
by `find -type f`; sandbox-only FIFOs never exist in source):

```sh
find . -mindepth 1 -maxdepth 1 -type d | LC_ALL=C sort | while read -r d; do
  (cd "$d" && find . -type f -print0 | LC_ALL=C sort -z |
     xargs -0 sha256sum | sha256sum) | cut -d' ' -f1 | sed "s|^|$d  |"
done
sha256sum expected.json
```

| pack | files | sha256 (aggregate) |
|---|---|---|
| Aborted | 1 | `38d6d061ffc5dd9e3f1f0b4a119ea600d56f1913e16a21f61aa203f59c0f2bfd` |
| AbortedErrorFields | 1 | `88b358c9ad2d3ba4fd262dd22e443044662c1397455a5d679fdd30f79616ed1f` |
| CodeQuota1113 | 1 | `f7c8f4bc2abde0d3ebafcd6ef9863f1383b532ef7ff51149589ab119043b09a4` |
| CodeQuota1308 | 1 | `c06daf96f50635b2ecb6c1dd7884b0b5d18787868a634210abc30f4994704d92` |
| CodeRate1302QuotaWord | 1 | `987dc603478573309afdb8b17dff6b87e31393fb3565a299f829e4fa50754d49` |
| Completed | 1 | `77526fe4644d932b18c204b827aa81ef173734e91e381a7b5f412248e84bafd2` |
| CompletedTrailing | 1 | `bbf8e7d7de86df6352716af627d85247869545f80eab8854b0e4360f860deeec` |
| CredentialPinTrap | 1 | `3613df2f859ff53d0032955d6e743de6a0caa4186821bdcc2dc17f21618db2c2` |
| DuplicateStems | 2 | `1c614b3dcc97bc195deaa56166e86bfec82d85e1528ec9330aac64b7c7de5c17` |
| EmptyDir | 1 | `94fe3bc362dc9047f8395fb8b7df7a3dde4ecc4f8ed091c6d6f1c7c037803bd6` |
| ErrorOther | 2 | `97d910227e6e76b5c9e809464196a94e8dffa344ecd6906e16360992c3b0e3f3` |
| ErrorUnsettled | 3 | `a129b85aeed3e384c514ab30ddba1f643cc6a17c132fe082dec1b06abe6ebec0` |
| FifoSkip | 1 | `131834891d60e158b8926d6b78620d3acb63866422bd91a2fe2f4248a3d9270c` |
| IncompleteToolResult | 1 | `d8677bfd84a2159013cb5d2fa68a41e175a22eb70890b5b907f8c1db83d627f7` |
| IncompleteToolUse | 2 | `518a3849b0fd51fc0260c98e0f641c097c575325d0620997301719ba5f8e88b0` |
| IncompleteUser | 1 | `4a4ccd68447f184552b12d433f9a1136a52a95e29c917e5f328aae3475466aa2` |
| MainSessionExclusion | 2 | `70a7439121726f774adc80fceb894493e48160526ff02d14708f6782ceeee230` |
| MalformedLineSkip | 1 | `0fb380d814061147d15481abdd7e8f2e1f33fa7715a8fff067431ea38b75bc2e` |
| MaxFiles | 2 | `b049250769189ee8a8c1128768ef297aef1985e8c52a2afbf3c61eb152602d66` |
| MixedFinding | 8 | `91ba93ffac2044f0a486c78dd14838a12e4e66bb291cde483192f71dd5bf9f53` |
| NestedDirs | 3 | `6e69931d5a6ca534940aec9e40ac63825ed8177622c0c00db81764ed1bab2054` |
| NonJsonlIgnored | 6 | `358a514eff3c059829aced2b692320212d56ae3e84cfb9feed1b48989abfd76f` |
| PrefixAttribution | 7 | `722113103cca79e54940681b728b086657d9bf1f76cea5961f237c10c38590f1` |
| Quota402 | 1 | `0fb86211fca66bc4106cc76adc90a03b06869dba2dd4c89339886790bbac3610` |
| QuotaCredits | 1 | `b9ea2372a20a5a072c968b313d761163d0b15cf8466149b66bac7fc08e9a2008` |
| QuotaUsageLimit | 1 | `b27d70499f4a44ca8a08f4358f868c9e924e9f7b139f6ff92cfb323ffb256609` |
| QuotaWord | 1 | `89a0133f23b8e685ddf7e6a684929be882386511b052a223125e26ede1504c7c` |
| RateLimitOrdering | 2 | `326775e29594deae17699f64dd8e9f1a84644d280f142bbffb790938152d8fcf` |
| RateLimitResourceExhausted | 1 | `69081d76f7be23768a126a64850e4394b682c36c615a2061b4b48a248ae5a54c` |
| RateLimitRetryExhausted | 1 | `5d0acb137f85195d5475d0a0691b1b1ab12210b2b6559fbae09b16b6e171b6cf` |
| RateLimitStatus429 | 1 | `48ae8dd43e50dc96da4505d6d2280b0f44f148c3381e6fe1fd1f8f31a211a431` |
| RateLimitToken429 | 1 | `9f2687a760af17adb56944e67c7294ae645bdbf87758a6efdd86c854247ca170` |
| RateLimitTokenCapitalRateLimit | 1 | `4663f3c4a5ea140ebc1123292758ffca1fe427f3882a840ee9a3bd16c4812a46` |
| RateLimitTokenRateLimitUnderscore | 1 | `949cf685cfdd44229e2bca5d7466e461fa4a7ceafcb7e1596d5c486dc4f2ba82` |
| RateLimitTokenUpper | 1 | `e72d477e16c20894635d25c4de9a1b237650a859f08315b1b99409217a5aadd8` |
| RetrySingle | 1 | `a28c19a3498c2decc10ada843d9afeb05a3b6a4f12e0d08dd0ff508ff49b1f57` |
| SchemaVersionUnavailable | 3 | `2cee595e314f21b47bff4c97b21716419875fae4711152f0b659fd1e240270d8` |
| SymlinkIgnore | 3 | `12c928f0ef3e66f25a2a0f769b9a52ecb0cdf8be6c5c7ad8196f29c4a40896cb` |
| TailBoundary | 3 | `5ac48b1fbb7ede76a2010f71fc9d1a9adddbf099476647348340e9a3622f9763` |
| UnavailableEmpty | 1 | `3135eeb0fa4de50c47583d1661fc9382624c82b553a1746e20977e625ea06db0` |
| UnavailableMalformed | 1 | `e35c3a8f0bde7864c06a8efa025efbbc32841dd4d61fab9220854815cb80310d` |
| UnavailableNonMessage | 1 | `30a567139d69ec86a41f28935cf4e333f24174774d5e8cb0f1af96453ea0e0cc` |
| UnreadableFile | 2 | `852189f6d2cb22d673dfa3d3eb3234468563290ae7e4c3940f636de24ff1574c` |
| MissingDir | 0 (absent) | — intentional: no directory, rc2 case |

`expected.json` sha256:
`b684c63bf3cebe70f24d3d02f3f0df4f63aad3f547a365a3ca1864f5f57cb01f`.

## Tree `pins` and sandbox metadata

`expected.json` top-level `pins` maps every non-directory entry except
`expected.json` to lowercase sha256 (81 entries = 78 regular + 3 symlinks;
directories omitted; **no FIFO exists in source**):

* regular file → `sha256(content bytes)`;
* symlink → `sha256(link target text UTF-8, no newline)`; targets:
  `Link.jsonl -> trap.txt`, `Dangling.jsonl -> missing-target.txt`,
  `linked-dir -> real-dir`;
* FIFO entries are **not pinned**: case `fifo_skipped` carries
  `"fifo_files": ["pipe.jsonl"]` (pack-relative); the source path must not
  exist and the gate creates it only in the per-case sandbox;
* `UnreadableFile/locked.jsonl` is **0644, size 0** and pinned as
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

No mode-000 file remains in the clone. The unreadable fixture is recreated by
the gate: case `unavailable_unreadable_file` carries
`"unreadable_files": ["locked.jsonl"]` (pack-relative, agreed with
`MoriR17.SeatGate-5`); the gate copies the pack into
`output/cases/<id>/sessions`, chmods 000 only in that copy, and discards it.
The gate must `os.mkfifo` the listed `fifo_files` only inside the sandbox copy
(never `copyfile`, never the source tree).

Independent pin check (read-only Python, same hash rules): 81 tree entries,
81 pins, extra 0, missing 0, mismatches 0.

## A1 verification commands

| command | rc | result |
|---|---|---|
| `TMPDIR=<clone>/.scratch python3 .scratch/build_fixtures_a1.py <fixtures/seat>` | 0 | `oracle: 54 cases consistent` |
| pin cross-check over lstat/walk (regular/symlink rules above) | 0 | 81/81, no extra/missing/mismatch |
| `sha256sum` per-pack aggregate recipe | 0 | 43 present-pack digests + `expected.json` |
| `grep`/`head` shape checks | 0 | version-3 headers; `completedAt` present; tail sizes 12,765 / 482,025 / 6,186 B |

No C1 tool was run (`tools/mori-seat-terminal.py` is not this seat's file and
was not executed); no VCS mutation, install, background work or `/tmp` write.
The A1 builder lived only in the executor's `.scratch` and was removed after
generation; the deliverable is the pack tree plus `expected.json`.

Post-handoff FIFO fix (L1, 2026-10-20): the source
`FifoSkip/pipe.jsonl` FIFO was removed (Git/jj cannot persist it), case
`fifo_skipped` gained `"fifo_files": ["pipe.jsonl"]`, its pin entry was
dropped, and pins/expected.json were re-hashed to
`b684c63bf3cebe70f24d3d02f3f0df4f63aad3f547a365a3ca1864f5f57cb01f`
(81 entries). The tool was not rerun.

## Updated risks

1. **Pins enforcement.** Any tree edit after this report invalidates
   `expected.json` pins → gate rc2 `snapshot_tampered`. Recompute pins with the
   same rules (regular content, symlink target text; FIFO paths unpinned) if a
   fixture changes.
2. **Sandbox copy coverage.** Gate must create each case's `fifo_files` with
   `os.mkfifo` only in its per-case copy and must honour `unreadable_files`
   only there; source chmod/mkfifo would break pins and the handoff rule.
3. **MissingDir in sandbox mode.** rc2 case has no pack directory, so the copy
   step must pass the absent source path through rather than failing setup.
4. **Schema reading window.** `SchemaVersionUnavailable/late.jsonl` only works
   if the tool honours the 4096-byte header window; a whole-file scan would
   wrongly classify it `completed`.
5. **Duplicate keys.** `DuplicateStems` expects `key` = sessions-dir-relative
   path without `.jsonl`; `want.seats` is keyed by those paths, not stems.
6. **Strict settle boundary.** Exactly `now - settle*1000` is settled (dead);
   only strictly newer is `error_unsettled`.

---

# A2 fixture strengthening (L1/CriticC1Final/CaseReview03/12/14/15/18/25/26, 2026-10-20)

Applied in place in the executor clone's `fixtures/seat` tree; no tool, gate,
selftest or test was run. Final state:

* **59 cases** (+5 new, 2 renamed, several wants strengthened);
* **89 pins** = 85 regular files + 4 symlinks (no source FIFO);
* **49 pack dirs** (48 present + intentionally absent `MissingDir`);
* `expected.json` sha256
  `30978148ea75ac81d213ac4fe2c7aa669c74c55ddebce1eed33050c0b3f100c2`.

## Review-driven changes

* **want.reason on setup cases (CaseReview14/18 + security):**
  `missing_dir_rc2`=`unavailable-dir`, `max_files_exceeded`=`too-many-files`,
  `prefix_filter_no_match`=`prefix-matched-none`,
  `root_symlink_setup_rc2`=`root-symlink`,
  `unreadable_dir_setup_rc2`=`walk-error`.
* **want.records (CaseReview12/15/25/26):** per A1 relative key, subset of
  `{key,prefix,retries,error_code,retry_exhausted,reason}` with type-strict
  comparison. Added to: `unavailable_empty_file` (schema),
  `unavailable_malformed_and_shape` / `unavailable_non_message_records_only`
  (no-message), `unavailable_unreadable_file` (locked=unreadable,
  open=completed), `tail_small_window_far_terminal_lost` (far=no-message),
  `schema_version_unavailable` (all three=schema), `nested_directories`
  (relative keys + prefixes), `retry_after_1_retry` (retries 1,
  retry_exhausted true, code 1302), `rate_limit_zai_retry_exhausted`
  (10/true/1302), the three code cases (1113/1308/1302),
  `duplicate_stems_two_entries` (d1/stem,d2/stem), `error_other_*`
  (thinking-loop retry false; bare-error reason terminal-time),
  `rate_limit_devin_resource_exhausted`, `rate_limit_free_model_*`
  (retry false), `unknown_time_*` (terminal-time), `unknown_code_1309`
  (code 1309).
* **want.top (CaseReview25/26):** `duplicate_stems_two_entries`
  `{duplicate_stems:1, main_sessions:0}`; `main_session_excluded_from_totals`
  `{main_sessions:1, duplicate_stems:0}`.
* **Relative seat keys (CaseReview15 + gate):** `nested_directories` now keys
  `want.seats`/`want.records` by `a/b/c/deep-seat`, `a/b/deep-two`,
  `a/shallow-seat` (flat packs already key==stem).
* **toolResult control fix:** `IncompleteToolResult` now has a preceding
  assistant `stop` (completed) before the terminal `toolResult`, so dropping
  the toolResult would yield `completed`, not the same `incomplete` class.
* **quota 402 isolation:** `Quota402` terminal has `errorStatus: null` and
  relies only on the `402` message token (class `dead_quota` unchanged).
* **tail naming:** `tail_default_window_all_classified` renamed to
  `tail_explicit_262144_all_classified`; the distinct true-default case
  `tail_a1_default_window` (no flag) remains.
* **security packs:** `SecurityRootSymlink` contains tracked symlink
  `root-link -> target` plus `target/inside.jsonl`; case args pin
  `--sessions-dir {pack}/root-link`, rc2 `root-symlink`.
  `SecurityUnreadableDir` holds `root-ok.jsonl` + `sub/inside.jsonl`; case
  metadata `unreadable_dirs: ["sub"]` (gate chmods only the sandbox copy),
  rc2 `walk-error`. Sources stay readable.

## A2/CriticC1Final corrections (recorded)

* **bare `resource_exhausted`:** no longer a rate cause; the existing
  `rate_limit_devin_resource_exhausted` case now expects
  `dead_error_other` (rc1, other=1). New control
  `RateLimitFreeModel/free-model.jsonl` carries
  `resource_exhausted: Reached free model rate limit` and expects
  `dead_rate_limit` (lower-case `rate limit` token).
* **timestamp-free terminal error:** class `unavailable`,
  per-record `reason: "terminal-time"`, never aged dead.
  `ErrorOther/bare-error.jsonl` updated to unavailable/terminal-time, and
  `UnknownTime/unknown-time.jsonl` is the dedicated control (error with
  429/1302/rate text but no `completedAt`/`timestamp` -> unavailable,
  reason terminal-time, rc0).
* **unknown type code under 429:** `UnknownCode1309` has `errorStatus: 429`,
  `vendor failure (type=1309)`, no rate/quota text, settled timestamp ->
  `dead_error_other` (code 1309 not 1113/1308/1302).
  [INFERENCE] A bare 429 with no unknown code keeps A1's rate-limit rule
  (`RateLimitStatus429` unchanged); only the unknown-code evidence suppresses
  the HTTP fallback.
* **ID clean cutover:** `rate_limit_beats_quota_by_status_and_token` renamed
  `quota_precedes_rate_limit_status_and_token` (semantics unchanged:
  quota-first). Prior case-54 receipts retain the old id by design.

## Case-table delta

| case id | pack | args (after --now-ms) | rc | finding_id | reason/top | seats -> class | totals nonzero |
|---|---|---|---|---|---|---|---|
| `rate_limit_devin_resource_exhausted` (CHANGED) | RateLimitResourceExhausted | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | — | `devin-resource-exhausted`→`dead_error_other` | dead_error_other:1 |
| `quota_precedes_rate_limit_status_and_token` (CHANGED) | RateLimitOrdering | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | — | `status-beats-quota`→`dead_quota`, `token-beats-quota`→`dead_quota` | dead_quota:2 |
| `error_other_thinking_and_bare` (CHANGED) | ErrorOther | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | — | `bare-error`→`unavailable`, `thinking-loop-error`→`dead_error_other` | dead_error_other:1, unavailable:1 |
| `nested_directories` (CHANGED) | NestedDirs | — | 0 | `MORI_SEAT_TERMINAL_OK` | — | `a/b/c/deep-seat`→`completed`, `a/b/deep-two`→`incomplete`, `a/shallow-seat`→`aborted` | completed:1, aborted:1, incomplete:1 |
| `tail_explicit_262144_all_classified` (CHANGED) | TailBoundary | `--max-tail-bytes 262144` | 0 | `MORI_SEAT_TERMINAL_OK` | — | `tail-far`→`completed`, `tail-near`→`completed`, `tail-partial`→`completed` | completed:3 |
| `main_session_excluded_from_totals` (CHANGED) | MainSessionExclusion | — | 0 | `MORI_SEAT_TERMINAL_OK` | top={"duplicate_stems": 0, "main_sessions": 1} | `nested-ok`→`completed` | completed:1 |
| `duplicate_stems_two_entries` (CHANGED) | DuplicateStems | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | top={"duplicate_stems": 1, "main_sessions": 0} | `d1/stem`→`dead_rate_limit`, `d2/stem`→`dead_rate_limit` | dead_rate_limit:2 |
| `rate_limit_free_model_resource_exhausted` (NEW) | RateLimitFreeModel | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | — | `free-model`→`dead_rate_limit` | dead_rate_limit:1 |
| `root_symlink_setup_rc2` (NEW) | SecurityRootSymlink | `--sessions-dir {pack}/root-link` | 2 | `MORI_SEAT_TERMINAL_SETUP` | reason=root-symlink | — | — |
| `unreadable_dir_setup_rc2` (NEW) | SecurityUnreadableDir | — | 2 | `MORI_SEAT_TERMINAL_SETUP` | reason=walk-error | — | — |
| `unknown_time_terminal_error_unavailable` (NEW) | UnknownTime | — | 0 | `MORI_SEAT_TERMINAL_OK` | — | `unknown-time`→`unavailable` | unavailable:1 |
| `unknown_code_1309_dead_error_other` (NEW) | UnknownCode1309 | — | 1 | `MORI_SEAT_TERMINAL_DEAD` | — | `unknown-code-1309`→`dead_error_other` | dead_error_other:1 |

## Final pack digests (A2; sha256sum recipe over regular files)

Recipe unchanged; symlinks excluded by `find -type f` and pinned separately.

| pack | files | sha256 (aggregate) |
|---|---|---|
| Aborted | 1 | `38d6d061ffc5dd9e3f1f0b4a119ea600d56f1913e16a21f61aa203f59c0f2bfd` |
| AbortedErrorFields | 1 | `88b358c9ad2d3ba4fd262dd22e443044662c1397455a5d679fdd30f79616ed1f` |
| CodeQuota1113 | 1 | `f7c8f4bc2abde0d3ebafcd6ef9863f1383b532ef7ff51149589ab119043b09a4` |
| CodeQuota1308 | 1 | `c06daf96f50635b2ecb6c1dd7884b0b5d18787868a634210abc30f4994704d92` |
| CodeRate1302QuotaWord | 1 | `987dc603478573309afdb8b17dff6b87e31393fb3565a299f829e4fa50754d49` |
| Completed | 1 | `77526fe4644d932b18c204b827aa81ef173734e91e381a7b5f412248e84bafd2` |
| CompletedTrailing | 1 | `bbf8e7d7de86df6352716af627d85247869545f80eab8854b0e4360f860deeec` |
| CredentialPinTrap | 1 | `3613df2f859ff53d0032955d6e743de6a0caa4186821bdcc2dc17f21618db2c2` |
| DuplicateStems | 2 | `1c614b3dcc97bc195deaa56166e86bfec82d85e1528ec9330aac64b7c7de5c17` |
| EmptyDir | 1 | `94fe3bc362dc9047f8395fb8b7df7a3dde4ecc4f8ed091c6d6f1c7c037803bd6` |
| ErrorOther | 2 | `97d910227e6e76b5c9e809464196a94e8dffa344ecd6906e16360992c3b0e3f3` |
| ErrorUnsettled | 3 | `a129b85aeed3e384c514ab30ddba1f643cc6a17c132fe082dec1b06abe6ebec0` |
| FifoSkip | 1 | `131834891d60e158b8926d6b78620d3acb63866422bd91a2fe2f4248a3d9270c` |
| IncompleteToolResult | 1 | `b67c866f2c68b3fe259b60a221dab46578ee3f1828ab92e64e4383f361e51414` |
| IncompleteToolUse | 2 | `518a3849b0fd51fc0260c98e0f641c097c575325d0620997301719ba5f8e88b0` |
| IncompleteUser | 1 | `4a4ccd68447f184552b12d433f9a1136a52a95e29c917e5f328aae3475466aa2` |
| MainSessionExclusion | 2 | `70a7439121726f774adc80fceb894493e48160526ff02d14708f6782ceeee230` |
| MalformedLineSkip | 1 | `0fb380d814061147d15481abdd7e8f2e1f33fa7715a8fff067431ea38b75bc2e` |
| MaxFiles | 2 | `b049250769189ee8a8c1128768ef297aef1985e8c52a2afbf3c61eb152602d66` |
| MixedFinding | 8 | `91ba93ffac2044f0a486c78dd14838a12e4e66bb291cde483192f71dd5bf9f53` |
| NestedDirs | 3 | `6e69931d5a6ca534940aec9e40ac63825ed8177622c0c00db81764ed1bab2054` |
| NonJsonlIgnored | 6 | `358a514eff3c059829aced2b692320212d56ae3e84cfb9feed1b48989abfd76f` |
| PrefixAttribution | 7 | `722113103cca79e54940681b728b086657d9bf1f76cea5961f237c10c38590f1` |
| Quota402 | 1 | `ea5e170f0db14d1ffeb7d3914e3d59514e6c217416d1d9f9d8bf9ae993d94fd1` |
| QuotaCredits | 1 | `b9ea2372a20a5a072c968b313d761163d0b15cf8466149b66bac7fc08e9a2008` |
| QuotaUsageLimit | 1 | `b27d70499f4a44ca8a08f4358f868c9e924e9f7b139f6ff92cfb323ffb256609` |
| QuotaWord | 1 | `89a0133f23b8e685ddf7e6a684929be882386511b052a223125e26ede1504c7c` |
| RateLimitFreeModel | 1 | `43813cecce0ea378bf91c79109f9c0d4c1169304f68915036938e0d62122885a` |
| RateLimitOrdering | 2 | `326775e29594deae17699f64dd8e9f1a84644d280f142bbffb790938152d8fcf` |
| RateLimitResourceExhausted | 1 | `69081d76f7be23768a126a64850e4394b682c36c615a2061b4b48a248ae5a54c` |
| RateLimitRetryExhausted | 1 | `5d0acb137f85195d5475d0a0691b1b1ab12210b2b6559fbae09b16b6e171b6cf` |
| RateLimitStatus429 | 1 | `48ae8dd43e50dc96da4505d6d2280b0f44f148c3381e6fe1fd1f8f31a211a431` |
| RateLimitToken429 | 1 | `9f2687a760af17adb56944e67c7294ae645bdbf87758a6efdd86c854247ca170` |
| RateLimitTokenCapitalRateLimit | 1 | `4663f3c4a5ea140ebc1123292758ffca1fe427f3882a840ee9a3bd16c4812a46` |
| RateLimitTokenRateLimitUnderscore | 1 | `949cf685cfdd44229e2bca5d7466e461fa4a7ceafcb7e1596d5c486dc4f2ba82` |
| RateLimitTokenUpper | 1 | `e72d477e16c20894635d25c4de9a1b237650a859f08315b1b99409217a5aadd8` |
| RetrySingle | 1 | `a28c19a3498c2decc10ada843d9afeb05a3b6a4f12e0d08dd0ff508ff49b1f57` |
| SchemaVersionUnavailable | 3 | `2cee595e314f21b47bff4c97b21716419875fae4711152f0b659fd1e240270d8` |
| SecurityRootSymlink | 1 | `96863975b6bcbc77ba9100722bac6098ad99aaf63a83160442b2fdaa48046b9f` |
| SecurityUnreadableDir | 2 | `1ae51ad51eb32bdaecb22fc1ad02a63d0a0650e9ddd12f7d2842eac86bcb1885` |
| SymlinkIgnore | 3 | `12c928f0ef3e66f25a2a0f769b9a52ecb0cdf8be6c5c7ad8196f29c4a40896cb` |
| TailBoundary | 4 | `910350faf1a24e81f713efe9b6a5f841f3a2f0e1772e58c31fa8547d78bc7683` |
| UnavailableEmpty | 1 | `3135eeb0fa4de50c47583d1661fc9382624c82b553a1746e20977e625ea06db0` |
| UnavailableMalformed | 1 | `e35c3a8f0bde7864c06a8efa025efbbc32841dd4d61fab9220854815cb80310d` |
| UnavailableNonMessage | 1 | `30a567139d69ec86a41f28935cf4e333f24174774d5e8cb0f1af96453ea0e0cc` |
| UnknownCode1309 | 1 | `38f8bc9575eb4f4fe1a403a2f5e1dacab86e7a4cbe8c15037debefdd765c904f` |
| UnknownTime | 1 | `f3f3449b163e58fc53f71187ebe5324cd6d938514ee802b81609e51261f44afe` |
| UnreadableFile | 2 | `852189f6d2cb22d673dfa3d3eb3234468563290ae7e4c3940f636de24ff1574c` |
| MissingDir | 0 (absent) | — intentional: no directory, rc2 case |

`expected.json` sha256:
`30978148ea75ac81d213ac4fe2c7aa669c74c55ddebce1eed33050c0b3f100c2`.

## Pins and sandbox metadata (A2 final)

* 89 pins = 85 regular + 4 symlinks; directories omitted; `expected.json`
  excluded; **no source FIFO**.
* Existing symlinks: `SymlinkIgnore/{Link,Dangling,linked-dir}` plus the new
  `SecurityRootSymlink/root-link -> target`; the root-link pin is
  `sha256(b"target")` =
  `34a04005bcaf206eec990bd9637d9fdb6725e0a0c0d4aebf003f17f4c956eb5c`.
* `FifoSkip` source has only `real.jsonl`; `fifo_files: ["pipe.jsonl"]` is
  sandbox-only (gate `os.mkfifo`).
* `SecurityUnreadableDir` metadata `unreadable_dirs: ["sub"]`; source `sub` is
  a readable real directory, chmod 000 only in the per-case sandbox copy.
* No mode-000 regular file exists in the source tree; all fixture sources are
  readable.

## Verification (no tool/gate/test run)

| command | rc | result |
|---|---|---|
| `TMPDIR=<clone>/.scratch python3 .scratch/strengthen_a2.py <fixtures/seat>` | 0 | `wrote 59 cases, 88 pins` (A2 base) |
| `TMPDIR=<clone>/.scratch python3 .scratch/tail_gap.py <fixtures/seat>` | 0 | `gap bytes 300062 total 300197 cases 59 pins 89` |
| structural validator over expected.json + tree + pins | 0 | `ok cases 59 pins 89`; rc counts 0:26, 1:28, 2:5; totals sums match |
| `sha256sum` per-pack recipe + `sha256sum expected.json` | 0 | table above; expected SHA recorded |
| `readlink`/`stat` spot checks | 0 | root-link -> target; target/inside.jsonl present; sources readable |

No C1 tool, gate, selftest, test, build or formatter was run. No VCS write.
The A2 transform script lived only in the executor's `.scratch` and is removed
after this report.

## A2 residual risks

1. **Gate metadata implementation.** `want.reason/top/records`, relative
   `want.seats` keys, `unreadable_dirs`, and root-link arg rebasing were
   confirmed with SeatGate; any loader mismatch is a gate-side fix.
2. **Tool A2 semantics.** `terminal-time`, `root-symlink`, `walk-error`, and
   unknown-code fallback must match the tool owner's wave2 implementation;
   fixtures pin the L1/SeatTool-confirmed strings.
3. **429-without-code interpretation.** [INFERENCE] `RateLimitStatus429`
   remains `dead_rate_limit` per A1; only an unknown code (1309) suppresses
   the HTTP fallback to `dead_error_other`.
4. **Tracked symlink.** `SecurityRootSymlink/root-link` is persisted as a
   symlink (Git/jj capable); the gate rebases the `{pack}/root-link` suffix
   into its sandbox and passes the sandbox path to the tool.
5. **Pins.** Any later edit to fixture bytes must recompute `pins`; mismatch
   yields gate `snapshot_tampered` rc2 before any run.

## Final CaseReview20 tail-default fix (supersedes the counts above)

* Added `TailBoundary/tail-old-default-gap.jsonl`: v3 session header plus a
  completed terminal, followed by **300,062 bytes** of benign `custom` padding
  (`seq`/`payload` ticks); total file **300,197 bytes** (<1 MiB). The terminal
  message is therefore 300,062 bytes before EOF — strictly >262,144 and
  <524,288. `tail_a1_default_window` still passes only `--now-ms` (no
  `--max-tail-bytes`).
* Expected behaviour: default 512 KiB reads the whole 300 KB file and sees the
  terminal -> `completed` (4 completed, rc0). An old 256 KiB default would
  drop the terminal -> `unavailable`; the explicit `--max-tail-bytes 262144`
  case now pins exactly that (`completed:3, unavailable:1`), and the 1000/64
  byte window cases were updated (`completed:2, unavailable:2`;
  `unavailable:4`).
* Case count stays **59** (no new case); pins increase by one to **89**
  (85 regular + 4 symlinks). `TailBoundary` pack aggregate:
  `910350faf1a24e81f713efe9b6a5f841f3a2f0e1772e58c31fa8547d78bc7683`
  (4 files).
* Final `expected.json` sha256:
  `30978148ea75ac81d213ac4fe2c7aa669c74c55ddebce1eed33050c0b3f100c2`.
* No tool, gate, selftest or test was run; no VCS write. The tail-gap
  transform script lived only in `.scratch` and is removed.

---

# PrivacyFinal parser counterexamples (final, 2026-10-20)

Tool owner informed; no tool, gate, selftest or test was run. These are the
surviving parser counterexamples from PrivacyFinal, not padding.

Final state: **66 cases**, **96 pins** = 92 regular + 4 symlinks, **56 pack
dirs** (55 present + intentionally absent `MissingDir`). `expected.json`
sha256:
`78071149679cf9871343286baff411cd0cb9215952521a8ed4dffd1d823853a9`.

## New cases

| case id | pack | rc | finding_id | seat -> class | totals nonzero |
|---|---|---|---|---|---|
| `escaped_quota_token_classified` | EscapedQuota | 1 | `MORI_SEAT_TERMINAL_DEAD` | `quota-escaped`→`dead_quota` | dead_quota:1 |
| `escaped_rate_token_classified` | EscapedRate | 1 | `MORI_SEAT_TERMINAL_DEAD` | `rate-escaped`→`dead_rate_limit` | dead_rate_limit:1 |
| `malformed_field_lines_skipped` | MalformedFieldSkip | 0 | `MORI_SEAT_TERMINAL_OK` | `malformed-field-skip`→`completed` | completed:1 |
| `decimal_timestamp_unknown_age` | DecimalTimestamp | 0 | `MORI_SEAT_TERMINAL_OK` | `decimal-timestamp`→`unavailable` | unavailable:1 |
| `decimal_schema_version_unavailable` | DecimalSchema | 0 | `MORI_SEAT_TERMINAL_OK` | `decimal-schema`→`unavailable` | unavailable:1 |
| `decimal_status_not_429` | DecimalStatus | 1 | `MORI_SEAT_TERMINAL_DEAD` | `decimal-status`→`dead_error_other` | dead_error_other:1 |
| `long_code_13_digit_unknown` | LongCode13 | 1 | `MORI_SEAT_TERMINAL_DEAD` | `long-code-13`→`dead_error_other` | dead_error_other:1 |

## Counterexample detail

* **Escaped tokens decode before matching.**
  `EscapedQuota/quota-escaped.jsonl:2` stores literal
  `"qu\u006fta exceeded"` (bytes; `json.loads` -> `"quota exceeded"`) and must
  be `dead_quota`. `EscapedRate/rate-escaped.jsonl:2` stores
  `"rate_\u006cimit"` (-> `"rate_limit"`) and must be `dead_rate_limit`.
  `want.records` pins key/prefix/retry false/null/code null for both.
* **Malformed field escape/number skips the line, not the session.**
  `MalformedFieldSkip/malformed-field-skip.jsonl` is: v3 header; assistant
  `stop`; a message line with invalid JSON escape `bad\qescape`; a message line
  with invalid JSON number `"completedAt":01`. Both lines fail strict JSON
  parse and must be skipped; the preceding `stop` remains terminal ->
  `completed` (rc0), never a false error.
* **No silent decimal truncation.**
  - `DecimalTimestamp/decimal-timestamp.jsonl:2` has
    `"completedAt":1760998000000.5` (JSON float) plus a 429/rate message.
    Non-integer terminal age is unknown: class `unavailable`,
    per-record `reason: "terminal-time"` (rc0), not an aged dead rate-limit.
  - `DecimalSchema/decimal-schema.jsonl:1` has `"version":3.0` (float). Only
    integer version 3 is accepted: class `unavailable`,
    `reason: "schema"` (rc0).
  - `DecimalStatus/decimal-status.jsonl:2` has `"errorStatus":429.0` (float)
    with generic text. A decimal status is not integer 429 and supplies no
    vendor cause: class `dead_error_other` (rc1), not `dead_rate_limit`.
* **13-digit unknown type code under 429.**
  `LongCode13/long-code-13.jsonl:2` has `errorStatus: 429` and
  `vendor failure (type=9999999999999)` (13 digits) with no rate/quota text.
  The unknown code does not fall back to HTTP status: class
  `dead_error_other` (rc1); `want.records.error_code` pins the full
  `"9999999999999"`.

## New pack digests (prior A2 table rows are unchanged)

| pack | files | sha256 (aggregate) |
|---|---|---|
| EscapedQuota | 1 | `4623c766877479e67dd5324ae387c8e282b7781ccb4b0f859a69b4ee15b0a527` |
| EscapedRate | 1 | `38a5bcd25951e665c1a727e95e51678ea3d89964830f36999f28d841e23e1b89` |
| MalformedFieldSkip | 1 | `36171d53cdde6ff6cd888535966fc1229560ca22b378e518dbe7f4bc379417f6` |
| DecimalTimestamp | 1 | `6cc13630224794915e5fc4707f51e4189bc4fa83aa2823f2a94c4748c3aa3ce2` |
| DecimalSchema | 1 | `0d4335aad71590fda397517ab339c1a00b6a098458a2f59198f1c911908627b9` |
| DecimalStatus | 1 | `c8e9cd9326e4e67eeb2e9fb60e09f7bbacb36c56cd3e50e2fd9e2107fe6d9ce2` |
| LongCode13 | 1 | `762dc017b6c13263b62c13bb7ed6c8a9ab5d803afc375ac664ead1fdce6e3c64` |
| MissingDir | 0 (absent) | — intentional: no directory, rc2 case |

## Verification

| command | rc | result |
|---|---|---|
| `TMPDIR=<clone>/.scratch python3 .scratch/parser_cases.py <fixtures/seat>` | 0 | `cases 66 pins 96` |
| parse/type spot checks (`json.loads`) | 0 | escapes decode to `quota exceeded` / `rate_limit`; malformed lines fail; decimal fields are float |
| structural validator over expected.json + tree + pins | 0 | totals sums match seats; pins exact (96); no extra/missing |
| `sha256sum` per-pack recipe + `sha256sum expected.json` | 0 | 7 new packs above; final expected SHA recorded |

No C1 tool, gate, selftest, test, build or formatter was run; no VCS write.
The parser-case transform script lived only in `.scratch` and is removed.

## PrivacyFinal residual risk

The classifications above depend on the tool owner's announced parser fixes
(strict JSON line skipping; type-strict timestamp/version/status; escaped
tokens decoded before matching; unknown long codes not falling back to 429).
Any tool-side deviation is a real C1 parser bug caught by these cases.
