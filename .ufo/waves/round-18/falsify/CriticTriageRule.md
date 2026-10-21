# Critic: out-of-metric triage rule

## Finding

The L1 rule incorrectly treats provenance (same-wave seat report, lane timeline, or public host log) as a categorical privacy exemption. The closure/minimization boundary is content-based: support may be retained, but private material copied or joined to that support remains disallowed. The frozen C1 classes are explicitly only a recall floor, so an out-of-metric reading-sweep finding does not need to match R1–R9.

## Counterexamples

All citations below identify only location and kind; no private values or excerpts are reproduced. The SHA-256 values are for the complete file at `e2bfbd6`.

- **SW1 other-seat results:** `.ufo/waves/round-17/build/JjEnvFacts.md:25-28` — host home/config paths and environment values. Full-file SHA-256: `185783bb08f4359a713a1049816561eb9082246e695af97c1dc339385cd23088`.
  - This is already separately named as minimization-pending by `out-of-metric-triage.md:26`; it is therefore not a new untracked exposure if that exception is honored. It nevertheless falsifies the SW1 rationale that same-round seat provenance alone makes a report safe.
- **SW4/SW5 lane timeline:** `.ufo/waves/round-17/build/MisrootR16Facts.md:38-46` — paraphrased other-session tool-output/probe summary. Full-file SHA-256: `1edff8b1fefccaed6ea48a7ee8d7ae18ad75f07cc599038174cdfbd021f6e013`.
  - The closure's minimization rule bars paraphrased other-session tool output, not only credentials or transcript dumps. Calling this a lane-owned disclosure/timeline does not change the content kind.
- **Package history:** `.ufo/waves/round-17/build/PacmanTxnToday.md:117-120` — joined operator identity/home-directory context from another report. Full-file SHA-256: `96ec030742fb9141c9b9c049b5b12cf36412c020eec09c8578f520870d92e39e`.
  - Public-log event evidence does not authorize retaining adjacent private attribution/context; the table allows event class and package names, and excludes joined private context.

These are three out-of-metric reading-sweep instances; none is asserted as an R1–R9 hit. The counterexamples attack the blanket rejection rationale, not the frozen C1 count.

## Impacted axes

- **Adjacency:** direct. Private context remains adjacent to committed evidence despite the support-only rule.
- **Calibration of the triage:** direct. The three disposition rationales do not reliably distinguish safe lane evidence from private material embedded in it.
- **C1 frozen metric:** unchanged; these findings are outside its token-class count, consistent with `frozen/c1-policy.json:29`.

## Smallest safe correction

Replace the provenance-based blanket rejects with a content check: same-wave results and lane timelines are rejectable only when they contain no item in the closure's `never` column. Keep ordinary support (path/line, event class, package names) and remove or minimize the embedded/joined private material. Retain the already-pending SW1 exception as an explicit line-level disposition; do not infer privacy-safety from “lane work” or “not a transcript dump.”

## Evidence and actions

Reviewed the round-18 contract and frozen C1–C3 inputs, the L1 draft verdicts and triage, the minimization table, and the cited closure boundary at round-17 tip `e2bfbd6`. Read-only `git grep` line-location queries and `git show | sha256sum` checks were run against that revision; all three targeted location-query pipelines and all three hash pipelines returned `PIPE_RC=0`. No URL access, install/update, test, VCS mutation, or file change other than this report.
