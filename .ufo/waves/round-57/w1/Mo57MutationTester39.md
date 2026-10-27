# C1 mutation probe — Mo57MutationTester39

Frozen predicate/counter: `contract.md` C1; `.ufo/waves/round-57/count-c1.py` lines 7–13. The counter fetches `R:SCORECARD.md` (line 7), counts whole table lines containing either capability token (line 11), and checks only for the round-56 path substring and literal `| 56 |` (line 12). It does not parse table columns or resolve evidence paths.

## Harness and baseline

- Reproduced controls on the pristine frozen counter at lane revision `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`: `C1=unmet rows=0 evidence=bad`, exit 1 (same as `controls.txt`). At freeze revision `618562c72a03dc4d17386b715357f863fd327274`, same output/exit.
- A scratch-only shared clone at entering tip used a fixture counter identical to the frozen counter except for its hard-coded repository path (frozen SHA-256 `7156fb4bb29f27881091b22dfa7ef3d661b1e955a1ec9a4d13e48013f1b368ec`; fixture SHA-256 after repoint `740948d49f01acb676d85442a6e7aa14cb8730da2595be9abac2eeea958a300a`). It reproduced the same entering-tip output.
- Built baseline after-state A in scratch clone, using existing round-56 evidence files `evidence/driver-liveness-live.txt` and `evidence/selftest-vote-bind.txt`. A=`d5b5d7246c61466b95a23fa86a48eaf6c7073244`, SCORECARD SHA-256 `be9b632591a7882a93eb9bdd76dcdc8a9ade6766e6bd5fdcecb3a17948278803`. Detector: `C1=met rows=2 evidence=ok`, exit 0. Baseline therefore passed.

## Mutants and actual outcomes

Each mutant was an isolated scratch-clone commit based on A; before hash is A's SCORECARD SHA-256 above. All outputs below are from the bounded C1 counter.

| Mutant (revision; mutated SCORECARD SHA-256) | Expected | Actual | Verdict |
|---|---|---|---|
| Row 1 Capability name `driver-liveness` → `driver-livenes`; evidence path still contains `driver-liveness` (`7e10cb72c3b2e62f8402541dbae5f66bb6599002`; `c81537f86ee571e9c4fd07d2374c08fdd04e7ee80548e15a16922332d6c98dad`) | Reject typo | `C1=met rows=2 evidence=ok`, exit 0 | Survived — line-level token search is satisfied by the evidence column, not the Capability cell. |
| Row 2 name `vote-binding` → `vote-bnding` (`acf00c5dd799c5a894fe4c7a3b67e27097862e1c`; `a84c6ee6547491b395124f3f11548242c5b89c38dde62233036c778cf02c8c88`) | Reject typo | `C1=unmet rows=1 evidence=bad`, exit 1 | Killed |
| Row 1 typo plus evidence path changed to token-free `.ufo/waves/round-56/evidence/live.txt` (`1df9eb21ee6d99afb05f05b63f4a35aa30c69d8c`; `c3850799bbd1f3e71ddc279db38875957e97a4288b7322cf2ad5a17bcadab58b`) | Reject, as no row contains token | `C1=unmet rows=1 evidence=bad`, exit 1 | Killed; confirms whole-line token presence boundary. |
| Row 1 name → `driver-liveness-probe` (`4fde1b41935a359786f2b35edf930177ec88aba9`; `9e7549757dbde11e900c7cb7617ffa6a3b4c5054aedea6c9bf26e9592d4a83e8`) | Reject altered Capability name | `C1=met rows=2 evidence=ok`, exit 0 | Survived — substring rather than exact field equality. |
| Row 1 evidence → `.ufo/waves/round-55/evidence/driver-liveness-live.txt` (`daa29bc0d7858d91c1071efb1e3fe6ee4e169b20`; `e034287abd88603f7128695d6199e4ada818a7c0f278bf88e4160a2d3e59c7fd`) | Reject wrong-round evidence | `C1=unmet rows=2 evidence=bad`, exit 1 | Killed |
| Row 1 evidence → `.ufo/waves/round-56/evidence/does-not-exist.txt` (`b5a5209b9192d918c26648164a081756e24c1679`; `830078d50d7205608f0409b314e62d481e0bf007e53014b6bffd8fbf894c4a90`) | Reject unresolved pointer | `C1=met rows=2 evidence=ok`, exit 0; `git cat-file -e <rev>:.ufo/waves/round-56/evidence/does-not-exist.txt` failed, exit 128 (“path … does not exist”) | Survived — counter checks only the prefix substring, not resolvability. |
| Row 1 first-working round `56` → `55` (`fdc631223075b84c1d6a7df8ae53dcd752b3859d`; `c47eae080913380e695e928912849ee50d7e7e39c63dd9742d248162a0379269`) | Reject wrong round | `C1=unmet rows=2 evidence=bad`, exit 1 | Killed |

## Restoration / scope evidence

After the final probe, the scratch clone was restored to baseline A `d5b5d7246c61466b95a23fa86a48eaf6c7073244`; restored SCORECARD SHA-256 `be9b632591a7882a93eb9bdd76dcdc8a9ade6766e6bd5fdcecb3a17948278803` exactly matches baseline. Restored detector output: `C1=met rows=2 evidence=ok`, exit 0. Lane HEAD remained `618562c72a03dc4d17386b715357f863fd327274`; its six pre-existing untracked round-57 files remained present. No lane source, commit, or `jj` mutation was made.
