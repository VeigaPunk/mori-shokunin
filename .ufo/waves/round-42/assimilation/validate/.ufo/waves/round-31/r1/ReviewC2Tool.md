author: mori round 31 residual seat ReviewC2Tool (non-author reviewer)

# C2 tool review — `tools/mori-blind-check.sh` vs rule clauses 1-5 + clause 6 byte-identity

Reviewed bytes: `git show a29f3e3f7f7259afb07df29c5ee8f68882712e96:tools/mori-blind-check.sh`, sha256
`79b774f7736cc9074fa786ad360553987d92096a3864b07212f7a3127924beb8`. The working-tree
`tools/mori-blind-check.sh` hashes to the same value (no drift). Rule text: `.ufo/waves/round-31/rule-text.md`
(identical to contract.md clauses 1-6). Method: code read + held-out briefs run in sandbox git repos under
`/fast/scratch/hyaku/mori-r31/ReviewC2Tool/` (repo, repo2, repo3; GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset;
all commands timeout-capped). My 9 briefs and hand-derived expectations were written to disk before either
fixture file was read. No tools were installed.

## 1. Independence (fixture names, content, order, environment, sandbox path, answer key) — no keying found

| Probe | Result |
|---|---|
| `grep -nE 'c2-fixtures\|count-c2\|fixtures-a1'` over pinned bytes | no match (P-C2-A1 bytes condition holds). The only brief-name literals (`CaseR31a`-`n`, tool:225-237,258-339) live in `--selftest`, which builds its own synthetic repo under `mktemp -d` and never reads the lane's fixtures or answer key; `--selftest` → `PASS`, exit 0 |
| Environment | `env -i PATH=/usr/bin:/bin` run is byte-identical to a normal-env run (22 hits, same lines). No `$USER`/`$HOME`/hostname/uname reads in the source. Poisoned `GIT_DIR=/nonexistent.git GIT_WORK_TREE=...` changes nothing (tool unsets all three at :7) |
| CWD | run from a repo subdir gives `scanned=9 blind_violations=29`, same as repo root (only `git rev-parse --show-toplevel` ties it to the repo, per interface) |
| Names/order/mtimes/nonce (repo3) | my 9 briefs renamed `W90.md`-`W98.md` in shuffled content order, random mtimes, `<!-- nonce 5f3a9c -->` appended to each: output matches my recomputed expectation 29/29 lines exactly (`diff` clean). Hits track content; only name dependence is the documented `{report}` allow substitution (tool:34) |
| Answer key | the tool reads only `<rev>` trees via `rev-parse`/`cat-file -t`/`ls-tree`/`show`; the allow file is caller data. No code path opens any `.json` |

My 9 briefs vs the 27 frozen fixture briefs (extracted from `c2-fixtures.json` sha `1442c14e…` and
`c2-fixtures-a1.json` sha `133547ee…`, both matching the contract's frozen hashes): zero byte-identical
briefs (`exact_content_dups 0`), so the check is genuinely held-out. Fixture shapes not in my set (mid-line
label, multi-path entry, HTML-free variants) and my shapes not in theirs (fenced heading, pipes-only row,
`file:L:M` suffix, detector same-line corner, CRLF) — complementary.

## 2. Clause exactness — held-out runs vs hand-derived rule readings

Ran 14 held-out briefs under my allow file (`derive/allow.txt`) and the critic's: mine S1-S9 (plus S10-S12
corner probes), plus the critic's `CriticC2Counter/heldout/fx/CaseH1-H5` under both my allow and theirs.
Hand-derived first, from rule clauses only. Agreement: every brief matches my rule reading, except the two
clause-1 findings below and two observations.

Verified exact (brief → agreement): heading/label openers at any level and case, words inside the heading
(S1, S6, H1-H4); markers `- `/`* `/`+ `/`N. `/`N) ` incl. indented and multi-digit (S1, H2, H3); prose
closes the block and is never an entry — the round-30 D1 defect is gone (S2, S6); a table outside any block
is not parsed (S2); separator row + row-directly-above withdrawal, aligned `|---|:-:|--|` (S3); blank lines
inside a block skipped, block continues (S6); no-candidate entry = one hit (S3:7, S4:9); named candidates
`LOG.md`/`SCORECARD.md`/`SKILL.md`/`PROVINCE.md` (S4, H2); wrapping strip of backticks, nested quotes,
parens, braces, angle brackets, trailing `,;.` (S4); `:L`, `:L-M` and single-strip `:L:M` suffixes (S4:8);
`file://` and leading `./` stripping, `{report}` per-basename substitution (S9, H5 under critic allow);
missing-list exactly once at line 1 (S5); multi-block entry counting (S6); both round-30 detectors
including 8-line windows, verdict/exit same-line corner, citation one-hit-per-line (S7: 3,4,9,10
run-output + 6 citation — exactly as derived from round-30's bytes). Critic briefs under both allow files:
4/4 expected hits each, mirror-flipping H2 (`* LOG.md`) and H5 (`{report}` own-scratch) exactly as the
rule+allow predicts.

### Findings

- **F1 (LOW) — a fenced `# files opened` line reopens a block (clause 1/3 divergence).** Brief S8:
  `## Files opened` / `- ssh://bh/etc/config` / ` ```json ` / `# files opened` / `- /etc/shadow`. Clause 3
  closes the block at the fence line; clause 1 opens blocks only at "a Markdown heading", and a line inside
  an open code fence is not one. Tool output: `S8.md:2` and **`S8.md:5:writer-forbidden-opened-path`** —
  the fenced list line is parsed as an entry because heading recognition is bare `^#{1,6}[[:space:]]`
  (tool:100, :132-135), fence-blind. Expected per literal clauses: only line 2. Not pinned by any fixture.
- **F2 (LOW) — setext headings are not recognized (clause 1 divergence, two misses + one false hit).**
  Clause 1 says "a Markdown heading (any level)"; ATX-only recognition (tool:100) misses setext. S10
  (`Files opened` / `============` / `- /etc/crontab`): tool prints **`S10.md:1:writer-missing-files-opened-list`**
  and misses the forbidden entry at :3 that a setext-H1 reading requires. S11 (`## Files opened` / allowed
  entry / `Files opened` / `------------` / `- /etc/shadow`): tool prints only `S11.md:2`; a setext-H2
  reading reopens the block and requires a forbidden hit at :5.
- **F3 (observation, interpretation-dependent) — a pipes-and-spaces row is an entry, not a separator.**
  S3 line 6 is `|    |` (only `|` and spaces). Clause 2's "(only `|`, `-`, `:` and spaces)" read as a
  character-set subset makes it a separator row (→ no hit); the tool requires at least one `-` and one `|`
  (tool:144-145: `is_separator` set only when the stripped row is empty of other chars **and** holds
  both `-` and `|`), so it is an entry with no candidate → `S3.md:6:writer-forbidden-opened-path`. The
  tool's reading is the Markdown-coherent one (a real separator needs dashes); flagging only because the
  rule text's literal subset reading disagrees. Rule text could say "containing `-`" to pin it.
- **F4 (observation, robustness) — CRLF briefs double-flag.** S12 (CRLF endings): `docs/manual/crlf.md`
  (allowed under my allow as LF) is flagged `S12.md:3:writer-forbidden-opened-path` because the trailing
  `\r` rides on the last token and the strip list (:54) doesn't remove it, while the allow-file reader
  does strip `\r` (tool:22) — asymmetric. A maximally literal clause 4 also flags it (the token genuinely
  contains `.` and matches no allow line), so this is not a clause violation; it only bites committed CRLF
  briefs. Not pinned by fixtures.

F1/F2 are not regressions: the round-30 gate (`check-blind-wave.sh`, sha `a3c85d9d…`, working tree ==
committed blob) is equally ATX-only and fence-blind; the carried round-30/31 lesson already lists
literal-reading ambiguities ("sub-heading inside a block", "lead-in prose") without pinning these shapes.

## 3. Clause 6 — the two kept detectors are byte-identical to the round-30 gate

- Regex definitions `cite_file_re` … `h2_re` (tool:90-99 = round-30:76-85): extracted and `diff`ed after
  removing the round-30-only `rule_rel`/`rule_abs` lines — **identical**.
- `writer-tool-source-citation` block (tool:179-181 = round-30:121-123): identical lines, same placement
  outside the `protected` gate (fires even inside derivation tables/json fences, as in round-30).
- `writer-tool-run-output` block, `if (( ! protected ))` … pending-counter decrements (round-30:135-154,
  20 lines): extracted from both committed files and `diff`ed — **byte-identical**. The `protected`
  scaffolding feeding it (case-json fences, derivation tables) is likewise unchanged.
- Clause 6 holds. (The files-opened parser, allowlist and output sorting are the rewritten parts, as D1
  requires; round-30's one-hit-per-file and `CaseA210c` self-test expectation are gone.)

## Verdict and residual risk

No gameability found: the gate's output on 23 held-out briefs (9 mine + 5 critic + 9 rename-probe
equivalents) is exactly what the rule text plus caller-supplied allow file predict, under stripped
environments, poisoned git env, renamed/reordered/nonced/random-mtime briefs, and two different allow
files. Defects F1/F2 are real but narrow clause-1 literal divergences (fenced and setext headings) with
no fixture coverage; F3/F4 are observations for the rule owner. Residual gaps: I did not execute
`count-c2.py`/`count-c2-a1.py` myself (the 27-fixture expected sets were taken as given, not re-derived by
hand — out of seat scope; my independence evidence is behavioral, not a proof over all inputs); the
27 committed fixture briefs were content-compared, not run through the gate by me; CRLF/encoding corners
beyond S12 untested.
