# RetentionTip: round 26 wave 2 no-harm check (routed item R8)

Lane: /home/vgpnk/Projects/shokunin/mori-shokunin
Candidate tip under check: 16935e24c93fa7e7567413d7ec091339a5df1474
Entering tip: 248408f5b6610a85bcbdebe7ac0b4fa7ed51422a
Rule: the retention scan value at the landed tip must not exceed the entering value (.ufo/waves/round-26/contract.md:123-125). "R8" in this report names that routed item; class R8 is the routing-table-key class (.ufo/waves/round-18/frozen/c1-policy.json:14).

## Verdict

- No-harm (R8): holds. Metric 4 at the tip, 4 at entering. Not worse, not better.
- Allowlist rows: the diff adds four rows, not five. All four hit lines are name-only, so all four are supportable under policy rule (a). No defect found.
- Observations O1 to O3 (section 7) are for the L1. None blocks the round.

## 1. Tooling

- No installs or upgrades. Read /home/vgpnk/.omp/agent/RULES.md in the first batch of the run.
- Used host python3 (standard library only), git (read-only: show, log, ls-tree, cat-file, archive), tar and sha256sum.
- Scratch: /fast/scratch/hyaku/mori-r26/RetentionTip/ (scan-tip.json, scan-base.json, allowlist-base.json, allowlist-tip.json, tip/ archive).
- Writes by this seat: the scratch directory and this report only.

## 2. Scan at the tip (assigned command, run from the lane)

Exit 1 (metric above zero), same as the base run. Output saved to scratch.

- metric 4; hits 113; allowlisted 104; unallowlisted 4; non_author 5 (excluded by policy glob, c1-policy.json:23-26); routed 0; warnings none; forbidden_allowlist none.
- policy_sha256 equals the sha256 of the policy bytes at the tip and of the working-tree file (db06e981...).
- Allowlist: the working-tree file and the tip blob have the same sha256 (9ffcd910...), so the scan's working-tree read matches the tip.

Unallowlisted hits (path | class | line number; no text):

1. .ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json | R2 | 8
2. same path | R5 | 11
3. same path | R6 | 12
4. same path | R8 | 14

Four hits, one path.

## 3. Entering value (base comparison)

- Base re-run at 248408f5 with the base allowlist (read with git show): exit 1; metric 4; hits 109; allowlisted 100; unallowlisted 4. Matches .ufo/waves/round-26/evidence/retention-scan-base.txt:4.
- The unallowlisted set at base equals the set at the tip (same path, class and line hash).
- The round-20 copy already existed at base. It was introduced by commit 71abd41. Its blob is byte-identical to the round-18 frozen policy at the tip.
- Delta from base to tip: hits +4, allowlisted +4, hits removed 0. The four new hits are all class R7, in files changed this round: SKILL.md:718, .ufo/waves/round-26/w1/DraftSkillFr10.md:157, .ufo/waves/round-26/wave1-run.json:247, .ufo/waves/round-26/wave1-spec.json:5. All four are allowlisted at the tip.
- Had those four not been allowlisted, the metric would be 8. The no-harm result therefore rests on the four rows, so each row must be name-only. Section 5 judges that.
- Verdict: holds (4 does not exceed 4).

## 4. Allowlist diff

- git diff 248408f5..16935e24 -- corpus/evidence/retention-allowlist.json: one hunk (@@ -701,6 +701,34 @@), 28 insertions, 0 deletions.
- The diff adds FOUR rows, not five. Rows: base 100, tip 104, removed 0.
- Each new row matches exactly one tip hit by path, class and line_sha256. None is on a must_redact path (c1-policy.json:17-21).
- Matching key: tools/mori-retention-gate.py:235 uses (path, class, line_sha256). A moved or edited line would not match.

## 5. Name-only judgement for the four hit lines

Method: each line was read from a git archive of 16935e24, not from the working tree. For all four, the bytes of the line hash to the scan's line_sha256 (4 of 4). R7 alternatives on each line: alternative 1 (line reference "config.yml:N") matched 0 times; alternative 2 (path ".omp/agent/config.yml") matched once. No other class matches on these lines. No line text is recorded here.

| Hit | Rule | Verdict | Basis |
|---|---|---|---|
| wave1-run.json:247 | a | name-only | Wave-1 dispatch bounds text. It names operator-owned surfaces by path and key name only (default config path and MCP settings path). No config contents, no line references. |
| wave1-spec.json:5 | a | name-only | Same text family. Its bytes differ from line 247 by one 3-character span (difflib count; text not recorded). |
| SKILL.md:718 | a | name-only | Gate-registry row. Only the default path of the operator settings file, plus key names ("async", "maxJobs"). The numerals 50 and 100 are illustrative literals, not operator values (see the check below). |
| .ufo/waves/round-26/w1/DraftSkillFr10.md:157 | a | name-only | Byte-identical to SKILL.md:718 (same line hash). |

Numerals check (boolean output only; settings file at the operator home, path ~/.omp/agent/config.yml):

- The "maxJobs" key is present.
- The configured maxJobs value does not equal 50, and does not equal 100.
- The literal 50 appears nowhere in the file.

So the numerals in the registry row are not copies of the operator's configured value. Limit: the literal 100 was checked only against the maxJobs key, not across the whole file.

Non-R7 content in the two wave-context lines: host-state facts (earlyoom version string, an active-since timestamp, systemd-oomd state, systemd version). These are not operator settings and not session records, and no frozen class covers them. [INFERENCE] They are not private under the frozen policy. Flagged as O3.

## 6. Sweep beyond the hit lines (counts and shapes only; no text recorded)

Files: SKILL.md, DraftSkillFr10.md, wave1-run.json, wave1-spec.json, all at the tip. Each token was checked by the characters around it, not by reading the whole file.

- Flag names "--avoid" and "--prefer": 3 to 4 lines per file (6 to 8 mentions). Every mention next to a non-slash character is a name mention in a rule list. None is followed by "=", a quote or a digit.
- Defaults-file variable name: 1 to 2 mentions per file, in rule text or quoted list items. None is followed by "=" or a digit.
- "cmdline": 2 mentions in each wave file, in rule lists. No /proc/<digit> path in any of the four files.
- Journal field name MESSAGE: 4 to 12 lines per file, in rule or field-name context. [INFERENCE from shapes; not read in full.]
- uid or pid followed by a number: 0 matches. Session-store path: 0. UUID-like session id: 0. Home paths other than the lane user: 0.

Verdict: no value-shaped leak in the windows checked. Not a full read of wave1-run.json (428 lines added) or DraftSkillFr10.md (299 lines). The policy calls the regex classes a recall floor (c1-policy.json:29), so this is a verification gap, not a proof.

## 7. Observations (no defect)

- O1 (floor composition). The entering value and the tip value are both made of the four class-pattern lines of an identical copy of the frozen policy under .ufo/waves/round-20/falsify/NoHarmRun/rg/. The policy's own lines 8, 11, 12 and 14 hold patterns (session-store, shell-history, sudoers, routing-key names), not operator values, so the four are name-only. They are not allowlisted. An L1 decision (allowlist under rule (b), or drop the copy) would bring the metric to 0. I do not recommend acting this round, because the contract requires only no increase.
- O2 (count). The brief says five rows; the diff has four. Any closure note should say four.
- O3 (non-R7 host state). The two wave-context lines carry host-state facts (earlyoom version string, active-since timestamp, systemd-oomd state, systemd version). The frozen classes do not cover these, and I judged them not private under the policy. This is a judgement call for the L1.

## 8. Verification gaps (not run, or limits)

- Not run: a full reading of wave1-run.json and DraftSkillFr10.md beyond the hit lines. Only count and shape checks were run.
- Not run: the literal 100 across the whole settings file (checked only against the maxJobs key).
- Not run: the tool's own selftest (not assigned).
- Not run: review of other allowlisted rows (out of scope; the 100 base rows are unchanged in the diff).
- The scan was run as assigned. I did not re-implement it; its results are the tool's.

## 9. Recommendation

- Accept the no-harm result for 16935e24: 4 does not exceed 4.
- Record four new rows, not five, in any closure note.
- L1 to decide O1 (floor composition) and O3 (host-state detail).
