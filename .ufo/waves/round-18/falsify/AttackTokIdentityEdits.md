# Round-18 token-redaction attack

## Scope and axes

Reviewed the requested diffs from `d005cdd` to `e2bfbd6` for: redaction completeness on changed lines; residual private values on the changed line or nearby context; preservation of technical meaning; and the L1 name-only allowlist rationale. The three changed files are Markdown, not JSON.

## Findings by severity

### High — personal identity remains in the redacted knowledge entry

`corpus/knowledge/silence-grading-r2.md:146` replaces the operator's full personal Git identity with a placeholder but retains an accented given-name fragment in the same parenthetical. `corpus/knowledge/silence-grading-r2.md:153` still contains the full operator personal name in nearby text, seven lines below the edited line. The latter was not changed by the pinned diff. Together these leave both a name fragment on the redacted line and a full-name occurrence in the same short passage.

This is within the L1's own wider privacy decision rule: the working-copy triage says personal identities/emails are privacy findings (`.ufo/waves/round-18/out-of-metric-triage.md:10-16`) and lists the redaction family at line 29, but that disposition names only `silence-grading-r2.md:146`, not line 153. It is outside the frozen R1-R9 metric, which is explicitly a recall floor rather than a privacy proof (`.ufo/waves/round-18/frozen/c1-policy.json:6-15,29`); therefore this does not by itself falsify the frozen-class C1 count, but it does falsify complete handling of this personal-identity family and weakens the unqualified quality trend at `.ufo/waves/round-18/draft-verdicts.md:16-17`.

Technical meaning is still understandable: the count and author-matching context remain. No JSON validity issue applies.

## Checks that did not find an actionable defect

- `.ufo/waves/round-17/build/OverlapJjSiblings.md:12`: the changed line removes the full operator identity. Its sentence remains coherent. The retained lane report reference, lane-internal revisions, and fleet-lane identity are consistent with the L1's non-private categories (`.ufo/waves/round-18/out-of-metric-triage.md:14-16`); I found no residual session/store/tool-log/config/personal-document token on that line.
- `.ufo/waves/round-17/build/CensusConsumers.md:186`: the author field is replaced while the pipe-delimited record remains structurally readable. The remaining commit revision, fleet-lane committer identity, and subject are not among the private values identified by the triage rule. No technical meaning break found.
- Frozen-class scan of all three target files found no R1-R9 matches. The separate literal identity-pattern scan found two lines in the target set, both in `silence-grading-r2.md` (`:146` and `:153`).
- No JSON file changed in the assigned diffs, so `python3 -m json.tool` was not applicable and was not run.

## Name-only allowlist judgment

The narrow principle is sound, not a blanket exemption. The frozen policy allows an outside-`must_redact_paths` hit only when its line carries no value copied from a private source and it is an instruction/boundary/contract surface name, a field/key name in lane tool code/contract/synthetic fixture, or a non-author file the lane cannot edit (`.ufo/waves/round-18/frozen/c1-policy.json:17-29`). Thus name-only field, record-type, and surface mentions may be allowlistable when each row satisfies that exact context rule. Personal-name fragments or values copied from private material do not qualify. The L1 draft describes 55 remaining hits at `daceeec` as name-only and says allowlist rows are pending (`.ufo/waves/round-18/draft-verdicts.md:8`); I did not inspect those 55 individual candidate lines or certify the whole set.

## Residual risk and verification gaps

- The frozen regex scan cannot establish privacy completeness; its own `known_limit` delegates unrepresented private context to the reading sweep (`.ufo/waves/round-18/frozen/c1-policy.json:29`). This review found a personal-identity residual not represented by R1-R9.
- `git diff-tree -r --name-only e2bfbd6 95c6158 --` the three target files produced no paths (exit 0), so the pinned source findings also remain in the tracked files at the later commit checked.
- Provenance note: the working-copy read of `.ufo/waves/round-18/out-of-metric-triage.md:25-35` includes the personal-identity disposition at line 29. `git show` of the tracked `e2bfbd6` and `95c6158` versions returned an earlier triage text. The line-29 disposition above is therefore cited as the working-copy L1 reading, not asserted as committed at either revision.
- No runtime tests, builds, or JSON checks were run; none were required for these Markdown-only diffs. No tools were installed or updated.

## Commands and results

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-17/build/OverlapJjSiblings.md` — exit 0; one changed line.
- Same diff command for `.ufo/waves/round-17/build/CensusConsumers.md` — exit 0; one changed line.
- Same diff command for `corpus/knowledge/silence-grading-r2.md` — exit 0; one changed line.
- `git grep -n` identity-pattern scan at `e2bfbd6` over the three target paths, piped to `cut -d: -f1,2,3` — pipeline exit 0; two matching locations, at `corpus/knowledge/silence-grading-r2.md:146,153` (patterns omitted to avoid reproducing the personal identity).
- Exact frozen R1-R9 regex scan over the three target files, with `pipefail` — exit 1 (no matches).
- `git diff-tree -r --name-only 29b0dc7 e2bfbd6 -- .ufo/waves/round-18/frozen/` — exit 0, no frozen-input drift.
- `git diff-tree -r --name-only e2bfbd6 95c6158 -- <three target paths>` — exit 0, no target-file paths reported.
