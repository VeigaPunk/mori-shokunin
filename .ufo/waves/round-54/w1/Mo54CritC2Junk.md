# Mo54CritC2Junk — C2 counter attack

## Counterexample

The frozen counter accepts materially dishonest depth. All fixture commits below were made in a `git clone --shared` under `/fast/scratch/hyaku/mori-r54/Mo54CritC2Junk/clone`, after verifying `git rev-parse --show-toplevel` returned that clone path. Fixture author was `Mo54CritC2Junk fixture <mo54critc2junk@fixture.invalid>`; no fleet repo/index/jj state was changed.

Command used for each result:

```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/count-c2.py <rev> --repo /fast/scratch/hyaku/mori-r54/Mo54CritC2Junk/clone
```

Observed outputs (exit codes shown):

- Data/spec base `2d0347a32b6befd7fd946a83319e04f6d8f004b9`, exit 1: `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=2d0347a32b6befd7fd946a83319e04f6d8f004b9 failed=entailment`
- Honest entry plus two fabricated ENTAIL files and fabricated `w1-results.json`, fixture rev `453a59034d188ac725e2b2c40114f95cea7958d5`, exit 0: `C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=453a59034d188ac725e2b2c40114f95cea7958d5`
- Junk claims over boilerplate/unrelated quotes, fixture rev `6f40b413d38a0fd7ec8000a0d229803d88c777f6`, exit 0: `C2=met claims=17 located=17 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=17 dissent=0 rev=6f40b413d38a0fd7ec8000a0d229803d88c777f6`
- One proposition restated 14 times with verb/noun swaps and unique nonce words, fixture rev `f9dda5022e54f914a0478f3d3c1d807157823649`, exit 0: `C2=met claims=14 located=14 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=14 dissent=0 rev=f9dda5022e54f914a0478f3d3c1d807157823649`

Variant A's junk claims each consisted of six synthetic tokens (`zephN quillN varmintN oblongN sprocketN tumbleN`) absent from their quotes. Quotes included source-code includes/license boilerplate and sysfs ABI metadata for unrelated node attributes; they were located and passed the 6–25 whitespace-token check. Variant B used 14 distinct, located quotes over all six sources, but claims were syntactic restatements of the same generic proposition with word swaps and nonce tails. Thus the static checks ensure literal uniqueness, not semantic breadth or relevance.

## Assessment

- The cheapest edit set for `C2=met` was adding two voter reports with an `ENTAIL <hash> entailed` line for every row plus `w1-results.json` listing those names; the honest entry and all pinned source data were untouched. At least two distinct voters are required by `MIN_VOTES=2` (`count-c2.py:51`, vote tally `:255-260`); all files can be included in the same commit as the data. This demonstrates the vote arm accepts repository bytes as attestations; the counter does not authenticate the author of voter files or independently bind them to an orchestrator event. Results-name binding only checks a name in committed JSON (`:140-151`).
- The strongest content counterexample is Variant A: arbitrary claims and unrelated boilerplate quotes pass every mechanical arm. `words_beyond` counts unique tokens not present in the quote, not relevance (`count-c2.py:91-93`); row validation checks only word counts, literal uniqueness, quote length, and location (`:215-250`). Only the ENTAILMENT votes can stop this class, and they are lane-seat judgments, not external verification (the counter docstring itself names this limit, `:29-33`). The fixture's fabricated votes show that the vote arm itself does not stop dishonest bytes when an attacker can author both reports and settlement record.
- Variant B shows a second class only the entailment votes could distinguish: near-duplicate propositions pass the folded exact-string uniqueness check (`:219-229`) by changing surface words and adding nonce tokens. The table can reach its 14-row floor without 14 independent propositions.
- A results file written by an arbitrary fixture committer is not, by itself, proof that the production orchestrator will accept or preserve that file. This attack establishes only that the counter trusts committed `w1-results.json` content and report bytes; real orchestrator write-protection/settlement provenance was not tested here. Treat that as a counter boundary and route the binding/authorship question to round 55, not as a claim about orchestrator behavior.

Smallest safe correction for a future round: make settlement/vote authorship externally verifiable and bind the counter to an orchestrator-authenticated result artifact; separately require source-relevant, substantively distinct claims/quotes, since token-difference and literal-uniqueness rules cannot establish entailment. These are routed limits, not proposed changes to the frozen round-54 predicate. No counter or contract edits made.

## Evidence

- `git clone --shared` from `/home/vgpnk/Projects/shokunin/mori-shokunin`; clone toplevel was `/fast/scratch/hyaku/mori-r54/Mo54CritC2Junk/clone`.
- Base was resolved with read-only `git rev-parse --verify 2d0347a3^{commit}` to `2d0347a32b6befd7fd946a83319e04f6d8f004b9`.
- Counter command and all outputs/exit codes are recorded verbatim above. The fixture commits are available only in the temporary clone; they were not imported into the lane repo.
- Working-tree state was already dirty in the lane when inspected (`PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md` modified); no cleanup or edits were made to those user changes.

## Findings

- HIGH — `.ufo/waves/round-54/count-c2.py:91-93, 215-250`: unrelated/gibberish claims with located boilerplate quotes satisfy all static content checks.
- HIGH — `.ufo/waves/round-54/count-c2.py:219-229`: near-duplicate claims with superficial word swaps/nonce tails satisfy literal uniqueness and minimum beyond-word tests.
- HIGH — `.ufo/waves/round-54/count-c2.py:137-166, 255-260`: the counter accepts votes and results by committed bytes; fake voter reports/results were sufficient to make the honest entry pass. Production orchestrator protection is UNVERIFIED.
- LOW — `.ufo/waves/round-54/count-c2.py:51`: `MIN_VOTES=2` is the minimum cost of the fake-vote fixture, but independent names do not establish independent authorship.
