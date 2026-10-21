# SourceLstat — S068 path-boundary findings

Scope: Python `os.stat`/`os.lstat` semantics for the round-21 accounting evidence-path check. No source edits, census, tests, or tool installs were made.

## Observed

- **S068 reopened.** The registry records Python 3.15.0 `os.stat`/`os.lstat` and scopes the claim to the final path component (`corpus/SOURCES.md:74`). The reopened Python docs say `os.lstat()` does not follow symbolic links; `os.stat()` follows by default and accepts `follow_symlinks=False` to stat a link (`https://docs.python.org/3/library/os.html#os.lstat`, `#os.stat`). The shared “not following symlinks” explanation is specifically about the **last element** of the path (`https://docs.python.org/3/library/os.html#follow-symlinks`). `os.lstat()` is documented as an alias for `os.stat()` on platforms without symlink support.
- The contract requires provenance paths to be relative committed evidence copies and explicitly says the tool rejects absolute/`..` paths **or symlink path components** (`.ufo/waves/round-21/contract.md:14`). Existing settlement notes likewise distinguish a symlink leaf from a symlinked parent (`corpus/knowledge/wave-settlement-r20.md:33-34`).
- **Precise boundary:** one `lstat("root/dir/file")` (or `stat(..., follow_symlinks=False)`) does not establish that every component is link-free. It avoids following the final component only; earlier components still take part in pathname traversal. Thus a symlinked parent can lead the lookup to a regular final file. This is an inference from the docs’ explicit “last element” scope, not a broader guarantee from S068.
- In the isolated candidate snapshot `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py#3522`, the path logic is component-wise rather than a single full-path `lstat`: `_open_directory_absolute` walks the root from `/` with `O_DIRECTORY|O_NOFOLLOW` (`:77-99`); `_open_absolute_regular` does the same for CLI input paths and opens the final file with `O_NOFOLLOW` (`:102-138`); `_read_root_relative` checks each parent and the final leaf with `os.stat(..., dir_fd=..., follow_symlinks=False)`, rejects symlinks, then opens relative to the held parent descriptor with `O_NOFOLLOW` (`:182-225`). Python documents `lstat` as equivalent to `stat(..., follow_symlinks=False)` (`#os.lstat`). The callers are `_check_reference` (`:428-445`) and `audit`’s root setup (`:477-487`). This is source inspection of the isolated candidate, not evidence of integrated or executed behavior.
- Located symlink tests exercise the **final leaf**: the candidate selftest creates `evidence/linked-cleanup.txt` as a symlink and expects `unsafe_symlink` (`.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:971-988`); the fixture runner replaces `row-disposition.json` with a symlink to an outside file (`.scratch/round21/FixtureLoss/fixture-loss.py:246-250`). Those cases do not exercise a symlinked ancestor directory or a symlink supplied as the root.

## Finding and application

**High confidence — S068 is a final-component rule, not an all-components containment rule.** To satisfy contract.md’s “symlink path components” requirement, validation must walk components separately relative to a trusted directory descriptor (or otherwise use a no-follow descriptor traversal); checking only the complete pathname’s final component is insufficient. The isolated candidate uses `stat(..., follow_symlinks=False)` per component plus descriptor-relative `O_NOFOLLOW` opens, so its inspected source addresses that boundary. The candidate’s source alone does not establish the fixtures pass or that it is the integrated tool.

## Remaining unknowns

- The production path `tools/mori-evidence-loss.py` was not found in the observed tree; the inspected implementation is only under `.scratch/round21/ImplLoss/`. No runtime result or integrated behavior is claimed.
- The located fixtures do not cover ancestor/root symlinks. Whether an additional fixture was added elsewhere is unverified.
- `read xd://lsp` returned “No such tool”; no LSP definition/reference/implementation results are available. Direct source reads support the observations above; no grep result is treated as semantic proof.
- No runtime check was performed for concurrent filesystem mutation; source inspection is not a race-freedom test.
