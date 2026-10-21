# Wave 2 falsification — SessionExitCorrelation

## Scope and verdict

Reviewed `.ufo/waves/round-17/build/SessionExitCorrelation.md` at attacked revision `e2bfbd6f8dccc51fc06455efc41f720301112dd4`, against original revision `d005cdd` and the closure route `corpus/lessons/round-17-verifier-spotcheck.md:339-346`. The lane's current `HEAD`/`master` was later (`95c615836c2cf74ee11539c4289a1ce06a81cfcb`); findings below are pinned to the requested attacked revision, not that later tip.

**Verdict: partial minimization; residual privacy findings remain.** The replacement removes the original concrete session-store path, transcript names, and non-allowlisted disposal-field values. It retains session-linked timestamps and an individual-transcript paraphrase. It preserves the seat's core conclusions and has correct original-blob provenance.

## Findings by severity

### High — session-linked snapshot timestamps remain

At the attacked file's `:12`, the snapshot retains both exact time endpoints tied to the live session corpus. These are session-linked identifiers even though the session path is withheld at `:11`; do not reproduce the values. This is a residual identity-bearing disclosure under the assignment's privacy boundary. The two endpoints are also part of the surrounding corpus-snapshot/result material at `:11-13`.

### High — an individual transcript is still paraphrased

At attacked-file `:42`, the second sentence describes one particular transcript by its record count, terminal-message class, and marker state. The transcript filename is withheld, but this is still a single-artifact paraphrase rather than a corpus-level count/class tally. The minimization table permits aggregate counts/classes while prohibiting paraphrased other-session output (`corpus/knowledge/evidence-minimization-r18.md:24-30`). The same line also retains a per-group time breakdown; redact the individual example and review whether that breakdown is needed.

### Medium — nonessential output narrative remains

Attacked-file `:49-50` retains prose interpretations of the observed drift and tail-reader behavior beyond the seat's core conclusions. These are derived descriptions of session-corpus output, not merely the required verdict-level conclusion. Keep aggregate count/class material only where needed; the decision table distinguishes permitted counts/classes from paraphrased output (`corpus/knowledge/evidence-minimization-r18.md:24-30`). Other table/tally material at `:23-36`, `:40-43`, and `:47-48` is aggregate count/class reporting and is not independently flagged here.

## Requested category checks

- **Direct session identity/path:** No concrete session-directory token, session-store path, or transcript filename appears in the attacked replacement; `:11` withholds the path and `:42` omits the example's filename. The remaining exact snapshot times at `:12` are nevertheless a session-linked identifier risk. The seat name at `:3` is lane identity, not session identity.
- **Operator config/routing; personal document/history/privileged-config facts:** None observed in the attacked replacement. It contains no operator routing/configuration values, personal-document or shell-history facts, or privileged-config fact. Its Git-history/provenance statement at `:5` is not shell history or operator configuration.
- **Session-record values:** No non-allowlisted `reason`/`kind` values remain: the replacement says those disposal-detail values are withheld at `:18` and `:23`. Remaining field/class aggregates at `:41` are aggregate contract-metadata counts, permitted by `corpus/knowledge/evidence-minimization-r18.md:29`; they do not restore the original disposal values. The frozen class definition identifies the prohibited session-record-value family at `.ufo/waves/round-18/frozen/c1-policy.json:15`.
- **Seat conclusions:** Yes. Attacked-file `:54-56` retains the original advisory conclusions, including that disposal is not an outcome signal, the limited interpretation of marker presence, and the stated uncertainty about longer-term irreversibility. These correspond to original-file `:105-117`. The answer-level findings also remain at attacked-file `:40-43`.
- **Provenance:** Correct. `git rev-parse d005cdd:.ufo/waves/round-17/build/SessionExitCorrelation.md` returned blob `61578ee9ad2204e8c4d5c93e778668bc9e583aee`; `git cat-file blob 61578ee9ad2204e8c4d5c93e778668bc9e583aee | sha256sum` returned `437b902fbc1c74174e06549a107e2dfbab315d8bca0dcfc55dde36175a57a7bf`. Both match the replacement's provenance at `:5`. That required pointer identifies the original Git object; the historical original remains recoverable and this tip-only minimization does not erase prior exposure.

## Residual risk and verification gaps

The remaining scope/tally details are mostly aggregate counts/classes, which the decision table allows. The clearest actionable residues are the session-tied timestamps (`:12`) and the individual example (`:42`), with extra narrative at `:49-50`. The report does not establish that the historical object or other repository copies have been sanitized; history is unchanged.

Read-only evidence used: `git show e2bfbd6f8dccc51fc06455efc41f720301112dd4:.ufo/waves/round-17/build/SessionExitCorrelation.md` and `git show d005cdd:.ufo/waves/round-17/build/SessionExitCorrelation.md` both returned numbered content (successful output; the shell wrapper did not expose a separate numeric pipeline status); `git rev-parse` and the blob-hash pipeline returned output without error. No source-code callers or runtime behavior were in scope; no build, test, lint, formatter, or LSP check was run. No VCS mutation, tool installation, or scratch output was performed.