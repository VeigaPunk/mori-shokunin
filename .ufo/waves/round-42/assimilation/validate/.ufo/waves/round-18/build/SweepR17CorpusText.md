# Round-17 corpus-text privacy sweep

## Scope and method

Reviewed the requested read-only diff `24526ea9617cd020fee16c28fe4d4a2789dc28cb..dcb2eea26d8dff0485b1cd0a9402fa63af82cb99` for `SKILL.md PROVINCE.md SCORECARD.md LOG.md corpus/`, then resolved findings against tip `d005cdde0e009dea6c0cc29b37163de536528658`. The diff contains 12 files, 999 insertions and one deletion. Hashes below are SHA-256 of each UTF-8 line with its LF omitted, matching the frozen population's `line_sha256` convention.

Commands (all read-only; each returned exit 0):

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat 24526ea9617cd020fee16c28fe4d4a2789dc28cb dcb2eea26d8dff0485b1cd0a9402fa63af82cb99 -- SKILL.md PROVINCE.md SCORECARD.md LOG.md corpus/`
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --unified=0 24526ea9617cd020fee16c28fe4d4a2789dc28cb dcb2eea26d8dff0485b1cd0a9402fa63af82cb99 -- SKILL.md PROVINCE.md SCORECARD.md LOG.md corpus/`
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log -1 --format='%H' d005cdd`
- Used the frozen C1 population/policy for path-and-class matching, then line-only searches and `git show d005cdd:<path> | sed -n '<line>p' | tr -d '\n' | sha256sum` for contextual review and hashes.

## Findings

### Retained session identity / cross-session linkage

- `corpus/lessons/round-17.md:93` — R1-category session identity; the frozen R1 expression does not recognize this form. **SHA-256:** `a51aedeff8e2d4ce40b40314e62d6ce906202578ab8484056e57d13819b7bc92`. Redact the session label; preserve only the bounded conclusion that actor attribution is unverified.
- `corpus/lessons/round-17.md:92` — cross-session output linkage via a log/UUID reference, without the UUID value on this line. **SHA-256:** `32ea9d4a7c2df87f52178569d863e3c0b105fd2601abfd5f12f105cb9bdf38b7`. Remove the linkage and retain only the actor-attribution limitation.
- `PROVINCE.md:114` — repeats the cross-session correlation at summary level, with no session identifier value. **SHA-256:** `6e76ba91d3c8835f096857b8335eadbd6fbf20df0ab619ff3eee89a63f317044`. Replace with an actor-unresolved handoff statement.
- `LOG.md:1153` — points to the actor-correlation material. **SHA-256:** `0c505025083f1d1e2f15b21756b4d2051daf365d566fad984f6a08aa6f40966a`.
- `LOG.md:1271` — repeats that other-session command-stream correlation was retained. **SHA-256:** `9abf828a6eaf6ef59bb292e25565ff6f4b4f256b8c32824a80d98e9ba656151a`.

  `LOG.md` is append-only: correct the two LOG references with an appended minimization note, not a rewrite. For the other files, remove the linkage and retain only the non-attribution conclusion.

### Model-assignment/session-record values

- `LOG.md:1268` — actual provider/model labels associated with the observed cohort; this is a contextual operator model-assignment/session-record value not matched by the frozen C1 expressions. **SHA-256:** `2b1ae6a1944c015b6e7c66ac94b145725dc662b70829ba9c6790d024c411c2a3`.
- `corpus/lessons/round-17.md:341` — first model value in the repeated breakdown. **SHA-256:** `64fc7dd2a1b9832ecf51d46500d18123407e3428179f8234ae6afbd1841b4e02`.
- `corpus/lessons/round-17.md:342` — second model value in the repeated breakdown. **SHA-256:** `a1ccf50b6a52d5490f20d72091c891acecae99653165bab46578f6849a04c8d6`.

  Minimal redaction: remove the model labels, retaining only coarse aggregate status counts if needed. Because `LOG.md` is append-only, use an appended correction note there.

### Metadata that points to a retained raw identifier

- `corpus/lessons/round-17.md:343` — says the final receipt redacts a directory identifier. **SHA-256:** `34922591d3c5665ed628cf3627f1ea14eaf51773134ed4a7ed44acb4057d9f2f`.
- `corpus/lessons/round-17.md:344` — refers to raw/canonical hashes and an older unredacted identifier. **SHA-256:** `9db28b1cd8f08e9079663f2fd15b9f7de1fb19963d446b521170ea7aff607c63`.
- `corpus/lessons/round-17.md:345` — says that identifier's historical copy remains. **SHA-256:** `b2bd64cc63dff36958ee638cfe7fc52e9ccc84ad1ef41cbcf42c3cdaa909c592`.

  These lines do not print the identifier itself, but disclose that a raw session/directory identity remains elsewhere. Remove that detail; if needed, retain only a generic note that a canonical receipt is archived.

### Lower-confidence execution identifiers [INFERENCE]

- `corpus/lessons/round-17.md:67` — contains a specific background-job handle. **SHA-256:** `3cc288de5d425612d393882c4ab23f6aa0ae7f4255ff31679d9196998022fac1`. If this is a session/job identity, replace it with a generic background-job reference.
- `corpus/lessons/round-17.md:73` — contains a specific operation identifier and reviewer-seat label. **SHA-256:** `f2b778d3791ede1fbd68b43dafaffdef6a66e6071d75edda0a8acc365090c631`. If these identify a session operation/participant, remove them and retain the generic VCS-observation finding.

## Frozen-pattern result and exclusions

Among the changed files in this sweep, the frozen C1 population has one regex hit: `corpus/lessons/round-17.md:241`, class **R6** (`privileged_config`), line SHA-256 `469c83039fa897c68dae0d9329873ce365e8f33c477841b3964731cac7b00948`. It names a restricted configuration surface only; it contains no configuration values or contents. Under the frozen policy's surface-only adjudication rule (a), it is allowlistable and is not a retained-config finding.

No R2/R3/R4/R5/R7/R8/R9 regex hit occurred in the changed-file set. The contextual session and model findings above are outside that regex coverage. Other reviewed mentions of sensitive surfaces/fields describe their names or limits only; no private document, history, privileged-config contents, credential, or non-allowlisted field value was copied into the scoped additions. No URLs were opened and no tools were installed or updated.