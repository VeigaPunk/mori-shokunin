measured 2026-10-23T12:03:33Z

# Findings

- Axes: operability—detecting a dirty lane index after helper commits (round-35 M4); operability and append-only coverage—using the registered SOURCES gate and detecting deleted rows (round-35 routed defects 2–3). Sources: `corpus/lessons/round-35.md:68`; `corpus/lessons/round-35-verifier-spotcheck.md:172-180`.
- QUALITY 102 currently invokes `.ufo/waves/round-35/check-sources-appendonly.py` and says deleted rows are not covered (`corpus/QUALITY.md:799-812`). The round-35 closure reports that checker had no SKILL.md registry row or self-test (`corpus/lessons/round-35-verifier-spotcheck.md:175-178`).
- The round-36 contract specifies the registered gate interface, `deleted=[...]` summary field, deletion count, and exit behavior (`.ufo/waves/round-36/contract.md:62-77`). This is contract evidence only; I did not run the gate, its self-test, or the sandbox deletion control.

# Drafts

```DRAFT corpus/QUALITY.md
## Criteria added round 36 — round-35 routed defects 3–4

103. After every lane helper commit, the lane git index contains no staged path and no intent-to-add entry; record the check result in the round's dispatch log immediately after each `landed` line. Check: `bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin` exits 0 after every helper commit, with a corresponding dispatch-log record. Lesson: `corpus/lessons/round-35.md:68` (M4); `corpus/lessons/round-35-verifier-spotcheck.md:179-180` (routed defect 4). Shown able to fail: in a sandbox clone, `git add -N <file>` makes the index check exit 1 (the self-test arm). Not covered: this post-commit check detects index state; it does not prevent prohibited Git operations or certify worktree/untracked-file cleanliness.

104. Append-only correction to QUALITY 102's active Check and deleted-row coverage: run the registered gate `tools/mori-sources-appendonly.py`, not the round-35 wave script as the active check. Its registry entry at `SKILL.md` includes a fixture self-test; its summary lists deleted ids as `deleted=[...]` and counts deletions as append-only violations. The round-35 wave script remains historical evidence. Check: verify the active QUALITY 102 command names the registered gate and its `SKILL.md` registry entry; run `python3 tools/mori-sources-appendonly.py <tip> --round-base <entering tip>`. A sandbox history deleting `S###` must print `deleted=[S###]` and exit 1. Lesson: `corpus/lessons/round-35-verifier-spotcheck.md:172-178` (routed defects 2–3); `.ufo/waves/round-36/contract.md:62-77`. Shown able to fail: the round-35 QUALITY 102 check points to the wave script and explicitly leaves deleted rows uncovered (`corpus/QUALITY.md:802-812`); a sandbox deletion control against the registered gate must produce the stated `deleted=[S###]`, exit-1 result. Not covered: this correction does not validate SOURCES row content or turn round-35 script output into a current gate receipt.
```

# Touched surfaces and gates

- Wrote only this scoped report at `.ufo/waves/round-36/w1/DraftQuality103.md`; `corpus/QUALITY.md` was not modified. These are proposed append-only blocks, not evidence that either criterion is implemented or met.
- No gate, self-test, or build/test command was run. The only command run was `timeout 10s date -u +%FT%TZ` → `2026-10-23T12:03:33Z`.
- No tools were installed or updated.

# Out of scope

- No product code, gate registry, dispatch log, or round evidence was changed. Current gate registration and runtime behavior were not independently checked.

# Artifact

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/w1/DraftQuality103.md`
