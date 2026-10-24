# ResidCensusRegistry — round 38 residual falsification

Reviewer: `mori-r38.ResidCensusRegistry`  
Scope: the four assigned census/registry/quote/round-local append-only checks; detection and report only.  
Axes examined: **operability** (commands and citation resolution), **calibration** (revision provenance and round-local versus historical findings), and **depth** (exact source quotation).

## Revision provenance

The required command

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse mori
```

exited **128**, with `fatal: ambiguous argument 'mori': unknown revision or path not in the working tree.` No `mori` ref was created. The parent explained that this is a jj-colocated lane with detached Git HEAD and branch `master`, not `mori`.

Read-only diagnostics observed:

```text
HEAD: b6993744171a05efc627b5e0664489c31aa5214e
refs/heads/master b6993744171a05efc627b5e0664489c31aa5214e
```

`git show --no-patch --format=fuller` resolved both the target `b6993744171a05efc627b5e0664489c31aa5214e` and entering tip `e33bb561712b32f46861362a3fa43762fa70ae4f`. All blob comparisons below used those full object IDs, not a presumed branch alias.

The live registry and executable used by the requested commands were tied to the target by matching Git blob hashes (`git hash-object` on the absolute live paths versus `git rev-parse <target>:<path>`):

| Path | Live and target blob OID |
|---|---|
| `corpus/SOURCES.md` | `0cc2f36e844ebee598b03ec8a8977316ab6f4b16` |
| `tools/mori-sources-appendonly.py` | `c2c86f4d3ca1c6f9b6d46462fb6481dab543b967` |

## 1. Source census

Executed exactly:

```sh
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Observed **exit 0**. The only diagnostic class was **W04**, 15 `duplicate url … across scopes` warnings for:

```text
S035 S037 S073 S074 S075 S076 S147 S148 S149 S150 S166 S168 S201 S218 S220
```

The final ordinary success line was:

```text
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

No other warning or error class appeared. S226 was not among the duplicate-URL warnings.

## 2. Committed registry delta

Executed:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --no-ext-diff --no-color --unified=0 e33bb561712b32f46861362a3fa43762fa70ae4f:corpus/SOURCES.md b6993744171a05efc627b5e0664489c31aa5214e:corpus/SOURCES.md
```

Observed **3 additions, 0 deletions**:

- `@@ -231,0 +232 @@`: the single new `| S226 | …` row.
- `@@ -284,0 +286,2 @@`: one blank separator and the single `Round 38 bounded search — …` log line (target line 287).

Every changed content line begins with `+`; the only nonblank additions are the S226 row and round-38 search text. Diff headers are not content changes.

An independent comparison loaded both complete registry blobs with `git show <full-OID>:corpus/SOURCES.md`, keyed table rows by their `S###` IDs, and compared the complete original row strings, without cell whitespace normalization:

```text
base_rows=225
target_rows=226
added_rows=[S226]
deleted_rows=[]
existing_rows_changed_bytewise=[]
diff_added_lines=3
diff_deleted_lines=0
diff_added_blank_lines=1
nonblank_changes_only_s226_and_search=true
```

Thus none of the 225 pre-existing rows changed any cell, including the normally mutable cells.

## 3. Lesson Gate quotation

Compared committed `corpus/lessons/round-38.md:9` with committed `corpus/evidence/sources-r38/S226.src:657-659`, both obtained with `git show` at the target. The source lines are:

```text
657 <dd><p>Return the canonical path of the specified filename, eliminating any symbolic
658 links encountered in the path (if they are supported by the operating
659 system). On Windows, this function will also resolve MS-DOS (also called 8.3)
```

The Gate names `S226.src:657-659` and quotes:

> Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system).

This is the source's first sentence **verbatim in text and punctuation**, removing only the opening HTML tags and joining the source's line wraps. There is no ellipsis, omitted clause, or substituted word. Whitespace-delimited word count: **24**, within the **25-word** limit.

## 4. Round-local append-only result

Executed from `/home/vgpnk/Projects/shokunin/mori-shokunin`:

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-sources-appendonly.py b6993744 --round-base e33bb561
```

Observed **exit 0** and the requested `round_changed=[]`:

```text
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]
```

The 18 historical immutable-row differences remain explicitly reported. This result is evidence of no round-local immutable edit/deletion, **not** a claim that historical violations disappeared, that mutable cells were checked by this gate, or that the timing algorithm is globally correct. The independent full-row comparison in check 2 covers the stronger no-existing-cell-edit requirement.

## Residual counterexamples and smallest safe corrections

### A. Required branch alias is absent — environment/procedure, not a content regression

**Counterexample/evidence:** the printed `rev-parse mori` command cannot resolve the delivered tip (exit 128), while `HEAD` and `refs/heads/master` identify the full target OID above.

**Impacted axes:** operability and calibration of reproduction instructions.

**Smallest safe correction:** name the verified full OID or actual `master` ref in the review instructions, preserving disclosure of detached HEAD. Do not manufacture a `mori` ref. The parent's supplied clarification resolves the review prerequisite; no code change or tradeoff is implicated.

### B. Registry/search locators still truncate the full sentence — narrow documentary defect

**Counterexample/evidence:** at the target, `corpus/SOURCES.md:232` quotes the sentence through `system` but labels it `:657-658`; `corpus/SOURCES.md:287` likewise says `S226.src:657-658`. Reading only those two lines ends at `operating`; `system).` is on **659**. The lesson Gate's corrected `657-659` locator is accurate, so this does **not** negate check 3 or the observed four requested check outcomes.

**Impacted axes:** depth (exact source location) and operability (range-based citation replay). No contradictory source wording or loss of the underlying evidence was found.

**Smallest safe correction:** preserve the committed S226 row. Under the append-only registry contract, any corrected immutable anchor belongs in a new row whose `teaches` opens `supersedes S226 —`, with the full `657-659` span; append a search-log correction rather than rewriting the filed search text. Alternatively, leave the present target intact and route this locator-only defect explicitly. Do not silently edit S226 in place or claim the current delta contains that correction. This is fixable citation debt, not an architectural tradeoff; admission remains outside this seat's authority.

## Review boundary

The four requested content checks produced the required observations on the pinned object. The named-ref failure and the two stale registry/search line ranges are disclosed above. No claim admission, round judgment, remediation, integration, commit, ref mutation, index mutation, or jj operation was performed. The only intentional file write was this report.

Tool installs/updates: **none**.
