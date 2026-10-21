# Round-18 C1 digest privacy-risk review

## Verdict

**Severity: Medium (privacy side-channel / candidate-confirmation risk).** The line digests do not reveal a line by themselves, but unsalted SHA-256 is a deterministic confirmation oracle when an observer can propose likely source lines. The committed path, line number, class, and repeated hit inventory narrow the candidate space. Risk is materially higher for short or stereotyped path/key/field lines. No candidate guessing or cracking was attempted.

**Recommendation:** do not add a public salt. For new snapshots and gate output, replace line-level digests with per-file SHA-256 plus per-file/class counts; keep exact per-line comparisons inside the verifier, not in committed JSON. Keep the already-frozen C1 population only as an immutable round-18 contract fixture: changing it now would violate the declared hit-for-hit baseline. That is a freeze constraint, not a conclusion that the digests are safe. For other evidence JSONs with no `line_sha256`, keep as-is for this digest-specific risk only.

## Exploit path and impact

1. An observer obtains the committed hash, its source path/line and class from the frozen population or C1 gate output.
2. The class narrows likely formats (the frozen policy explicitly enumerates identity, session-path, numbered-output, config, routing-key and session-field patterns).
3. The observer forms likely complete-line candidates from known templates or a small value set and hashes each candidate locally. A match confirms the candidate line; the hash itself does not need to be inverted.

The frozen enumerator hashes the entire UTF-8 line directly with SHA-256 and no salt (`.ufo/waves/round-18/frozen/c1-population-cmd.py:34-42`, especially `:41`). The C1 policy explicitly calls its classes a recall floor rather than a privacy proof (`.ufo/waves/round-18/frozen/c1-policy.json:27-29`). This is a confirmation/correlation leak, not evidence that arbitrary high-entropy values can be recovered from SHA-256. Historical source retention remains a separate exposure: replacing hashes in a later tip does not remove the old Git blobs, as the knowledge note itself says (`corpus/knowledge/evidence-minimization-r18.md:44-45`).

## Evidence

- The frozen population reports 119 hits, including 40 in the three `must_redact_paths` (`.ufo/waves/round-18/frozen/c1-population.json:5-10`; hit records occupy `:12-727`). C1 requires this baseline to reproduce hit-for-hit at `d005cdd` (`.ufo/waves/round-18/contract.md:24-29,55-61`).
- The C1 JSON output is a single minified line and carries hash-bearing `hits` and `unallowlisted_hits` arrays (`.ufo/waves/round-18/evidence/c1-before-d005cdd.json:1`). The structured count check found 119 `hits` rows (94 distinct digest values) and 116 `unallowlisted_hits` rows (91 distinct digest values); `routed` is 40. Thus the output repeats line-level identifiers in addition to the frozen population. Of the other four JSON files inspected in `evidence/` (`c2-before.json`, `wave1-context-check.json`, `wave2-context-check.json`, `wave1-dead-seats.json`), recursive JSON-field checks found no `line_sha256` key. This statement is limited to line-digest exposure, not their other contents.
- Length-only review of the 40 routed hit rows found 37 distinct source `path:line` coordinates (some lines matched more than one class):
  - `OmpRetryConfig.md`: 17 hit rows / 16 coordinates; line lengths 35–157; 4 rows are at most 64 characters and 6 are under 80.
  - `PacmanActorTrace.md`: 18 hit rows / 17 coordinates; lengths 44–114; 2 rows are at most 64 and 5 are under 80.
  - `SessionExitCorrelation.md`: 5 hit rows / 4 coordinates; lengths 80–116; none are under 80.
  - Overall: minimum 35 characters, 6 rows at most 64, 8 rows at most 70, and 11 rows under 80.
- The six routed rows at most 64 characters are class/length observations only (no text): `OmpRetryConfig.md:36` R7/35, `:151` R9/55, `:155` R7/56, `:47` R8/62; `PacmanActorTrace.md:146` R5/44 and `:34` R1/62. These short lengths plus their policy classes make candidate confirmation credible for at least some entries. Length alone cannot establish exact guessability, and longer templated lines can also be guessable. I did not inspect or reproduce the source line text.

Length measurements used only read-only `git show` output piped first through `awk '{print length}'`, then a numeric line-number/length selector (no source text was printed):

```text
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d005cdd:.ufo/waves/round-17/build/OmpRetryConfig.md | awk '{print length}' | awk 'NR==4||NR==14||NR==15||NR==21||NR==24||NR==36||NR==40||NR==44||NR==47||NR==151||NR==155||NR==157||NR==158||NR==172||NR==177||NR==210 {printf "%d:%d\\n", NR, $1}'
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d005cdd:.ufo/waves/round-17/build/PacmanActorTrace.md | awk '{print length}' | awk 'NR==31||NR==32||NR==34||NR==36||NR==45||NR==47||NR==48||NR==53||NR==66||NR==90||NR==95||NR==103||NR==144||NR==145||NR==146||NR==147||NR==152 {printf "%d:%d\\n", NR, $1}'
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d005cdd:.ufo/waves/round-17/build/SessionExitCorrelation.md | awk '{print length}' | awk 'NR==5||NR==12||NR==30||NR==107 {printf "%d:%d\\n", NR, $1}'
```

All three calls returned numeric output without a tool error; the shell wrapper did not expose numeric exit statuses (**[INFERENCE]** exit 0 for each successful pipeline). No source line text was output.

## Family decisions

| Family | Decision | Rationale |
|---|---|---|
| Frozen `c1-population.json` (119 line hashes; 40 routed) | **Keep only as the immutable round-18 frozen fixture; replace-by-file-digest in the next versioned baseline.** | Current C1 explicitly requires hit-for-hit reproduction. Do not mutate this freeze in-place. Future snapshots can record per-file content digest and per-file/class counts while the verifier compares individual hits privately/in memory. |
| Three routed-file families (18 / 17 / 5 rows) | **Replace-by-file-digest.** | The observed minimum is 35 characters, and short classed lines make candidate testing plausible. A public salt would not stop guessing; a secret salt/HMAC would add key-management and reproducibility requirements and would change the frozen contract. |
| `evidence/c1-before-d005cdd.json` | **Replace-by-file-digest / aggregate-only output.** | Its two arrays contain 235 hash-bearing rows in total and repeat the per-line identifiers. Emit counts and per-file digests instead of hit-level hashes in future gate evidence. |
| Other four JSON files under `evidence/` | **Keep for this specific issue.** | The recursive field checks found no `line_sha256` keys. This is not a broader privacy approval. |

A whole-file digest is still not secrecy: an exact known candidate file can be confirmed, and Git history remains. It is nevertheless a less revealing committed witness than one digest per sensitive line. The current round-18 knowledge note gets the core limit right—an unsalted digest of a short, guessable line can be confirmed—but **does not state the limit fully**: its advice to commit whole-file digests or long lines can be read as a safety guarantee. Long lines may be templated/low-entropy, and a whole-file digest can also be guessed when the candidate file is known. See `corpus/knowledge/evidence-minimization-r18.md:37-45`.

## Smallest remediation

Do not alter the frozen round-18 snapshot. For the next C1 schema/version, retain per-file counts and file digests in committed population/gate JSON, suppress per-line digests from committed outputs, and preserve hit-level checking only inside the gate. Amend the knowledge note to say that neither line length nor whole-file hashing guarantees secrecy; both remain candidate-confirmation mechanisms, and no hash of guessable private input should be treated as redaction.

No files other than this report were written. No tools were installed or updated.