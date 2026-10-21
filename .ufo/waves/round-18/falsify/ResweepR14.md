# Round-14 privacy re-sweep at attacked tip

## Scope and method

Read the round-18 contract, frozen C1/C2/C3 inputs, L1 draft verdicts, and L1 out-of-metric triage before this scan. Scanned tracked text blobs under `.ufo/waves/round-14/` at `e2bfbd6f8dccc51fc06455efc41f720301112dd4` using read-only `git grep -n -I -E` (the `-I` binary exclusion). Secondary in-memory parsing emitted counts, lane-relative path:line references, and hashes only; no matched values were copied here. `git show` context checks were restricted to classifying flagged lines. No files other than this report were written; no tool was installed and no VCS mutation or external URL access occurred.

Counts below are line hits unless expressly called address tokens. Families overlap; counts are not additive. Broad lexical counts include ordinary discussion and fixture terms, not only sensitive values.
## Evidence status

- **Observed:** The revision-scoped `git grep -n -I -E` scans produced the raw counts below; seven matched lines contain paths outside the lane/fleet root. C1 R1 session IDs, R2 store paths, R4 personal Documents paths, R5 shell-history paths, R6 `sudoers`, R8 named routing keys, and config-file paths had no exact hits.
- **[INFERENCE] Classification:** The seven off-fleet home paths are private-context disclosures by location, even though their containing files are lane reports/dispatch inputs. Email tokens outside fixture-context markers are classified by surrounding source/fixture context, not by printing values.
- **Unresolved:** The `SourceFrontier` fallback assignment may be a public/synthetic example or a routing value; its RHS was not established. Capitalized-pair matching is only a broad candidate heuristic and cannot prove absence of all personal names.

## Findings by family

| Family | Broad hits at the measured tip | Classification / precise private-form check |
|---|---:|---|
| Personal names | 986 capitalized two-word candidates; four stricter field/byline candidates | Candidate regex is very noisy. The four stricter candidates resolve to structural headings/citation contexts, not personal identities. No private personal name was confirmed. Residual limitation: this is not a general named-entity detector. |
| Emails | 220 lines, 223 email-shaped tokens | 222 are synthetic-fixture-context (217 have synthetic markers; four more occur in explicit result-fixture rows and one in a scoped-fixture table); one is in public-source context. No private email was confirmed. The public-source-context line is in `build/CensusRepair.md:102`; no value is reproduced. |
| Host-home paths | 6,566 lines contain the searched home prefix | Token-level classification: 6,559 lane/fleet paths, seven paths outside the lane/fleet root (private-context; C1 class: none—R4 is Documents-specific). The seven private-context locations and line-text SHA-256 values are listed below. |
| `.config/` | 0 | No hit (exit 1); no classification required. |
| `sessions` / `session` | 807 | Broad matches are lane/fleet prose and synthetic/evidence material. Exact session-store path: 0; exact frozen R1 session-identity pattern: 0. No private session identity/store value found. |
| Timestamp-like session IDs | 2,229 broad date-time-shaped lines | Synthetic/evidence or lane/fleet timestamps; exact R1 ID pattern: 0 and `Z_<8 hex>` pattern: 0. No session-like identity confirmed. |
| `Documents` | 7 | Generic lane/public-document mentions. Private `Documents` path form: 0. |
| `history` | 66 | Generic lane/public-document mentions. `.bash_history`: 0. |
| `sudo` | 2 | Generic lane/instruction mentions. `sudoers`: 0. |
| `uid` | 36 | Ten numeric-UID-shaped lines share one identical line digest across frozen/test-target copies, so classify as synthetic fixture data; remaining matches are field/schema terminology. No private account identifier confirmed. |
| Provider/model strings | `provider`: 0; `model`: 29; provider/model or recognized model-ID strings: 0 | Ten `model` assignment lines are identical fixture-code copies. Frozen R8 routing-key names: 0. No operator provider/model value found. |
| `fallback` | 90; 86 fallback-family-name matches | Most are lane/fleet prose or fixture terminology. One assignment-shaped line remains unresolved: `build/SourceFrontier.md:168` (SHA-256 below). Nearby context does not establish whether it is a public/source example, synthetic value, or operator routing value; conservatively treat the RHS as possible private context until adjudicated. Frozen R8 key names: 0. |
| `config.yml` / `config.yaml` | 0 | No hit (exit 1). |

### Private-context locations (values withheld)

These seven lines contain at least one host-home path outside the lane/fleet root. C1 has no matching class for these general paths; R4 only covers personal Documents paths. SHA-256 is over the matched line text bytes, excluding its trailing newline.

- `.ufo/waves/round-14/build/GateConformance.md:8` — `6ebfb49e9f96aae431f25c7911af58abf82dc80b1be85482eaa680e6d1dc78ba`
- `.ufo/waves/round-14/build/JournalSentinel.md:218` — `39f1ab04cffee19e2bce1472179f49f3189a119583fb38c81f28bc5e11934b8e`
- `.ufo/waves/round-14/build/ProtectedInventory.md:30` — `452f9f808868298513835fe1f833346c4baefbddcbeaa51fab372f38ad35c2f6`
- `.ufo/waves/round-14/build/ProtectedInventory.md:157` — `3b88d73e976a796a2adca86cf8e0e2c373c906daa10c424d2721b68120b3f4db`
- `.ufo/waves/round-14/build/ProtectedInventory.md:240` — `9b36871c91bc1f96b2146b8133e96b1a2d7df6fd84e00a38f568e91fbb436c34`
- `.ufo/waves/round-14/dispatch.json:357` — `dc7a8ccd70cb3b43ac00622da7e117d72ac9cfa35ac2114ac2851e41e4c3ea81`
- `.ufo/waves/round-14/spec.json:3` — `a2498177d20c528a64e175c0b575793b9aa282d1887e995c1c32182f5648185e`

The unresolved fallback assignment-shaped line is **not** confirmed private; its line-text SHA-256 is `ad66d954446e96fe6fd38e7f6a8805f65dd2d839bb5c30192c7d43fa7cbef3aa` (`build/SourceFrontier.md:168`). It does not match a frozen C1 class.

## Comparison with L1 triage

**Confirmed triage gap:** `.ufo/waves/round-18/out-of-metric-triage.md:28` classifies the JjEnvFacts HOME/XDG path family as non-private on the rationale that the home path is already present in lane paths. This resweep distinguishes lane/fleet paths from paths outside that root and found seven of the latter. The broad rejection rationale does not disposition these off-fleet host-home paths. This is the family missed by the triage; it is outside C1 R1–R9 (see `frozen/c1-policy.json:7-15,29`).

**Possible, not proven, gap:** the triage's general operator-config/routing-values rule (`out-of-metric-triage.md:10-13`) may cover the unresolved fallback assignment, but there is no family-specific disposition or evidence tying this `SourceFrontier` row to a fixture/public source. Keep its value out of the handoff unless the L1 establishes that context. C1 R8 names only specific routing keys (`frozen/c1-policy.json:14`), none of which matched here.

Other requested families are already represented in the triage’s privacy rule (`out-of-metric-triage.md:10-17`) or explicit dispositions (`:23-29`), and the precise private forms checked here were absent. In particular, names/emails are explicitly addressed at `:29`; this sweep found only fixture/public-source email contexts, not an operator identity.

## Minimal redaction

For the seven off-fleet path lines, replace the host-specific absolute path with `$HOME/<redacted>` (or a neutral fixture path if that location matters). For the unresolved fallback row, preserve only the field/key label and replace its RHS with `<routing-value-redacted>` until its source is established. If any email candidate is later reclassified as personal, replace it with `<email>` or a reserved `.invalid` fixture address.

## Commands and exit codes

All scans used the read-only form `git -C <lane> grep -n -I -E <family-pattern> e2bfbd6 -- .ufo/waves/round-14/`; exit 0 means one or more matches and exit 1 means no matches. Broad-family results: email, names, host-home prefix, sessions, timestamp candidates, Documents, history, sudo, uid, fallback, and model each exited 0; `.config/`, provider/model-ID query, and `config.yml|config.yaml` exited 1. Precise checks for session-store path, exact R1 session ID, `Z_<8 hex>`, private Documents path, `.bash_history`, `sudoers`, provider term, and R8 key names exited 1. Numeric UID, model-assignment, fallback-assignment, and the strict name/byline queries exited 0. An initial Boolean home-path query was malformed and exited 128; it was replaced by the successful broad home-prefix scan plus value-free path-token classification above. Context-only `git show e2bfbd6:<path>` checks succeeded (exit 0) for the flagged email/name/fallback sections. No URLs were accessed.
