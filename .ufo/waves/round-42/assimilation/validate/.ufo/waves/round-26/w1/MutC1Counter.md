# MutC1Counter — mutation report for the C1 counting command

Seat: MoriR26.MutC1Counter. Round 26, wave 1. Date: 2026-10-22.
Lane repo untouched. All probes ran in the isolated scratch clone
`/fast/scratch/hyaku/mori-r26/wt-mutc1` (branch `r26-wt-mutc1`, base
`28b0494`); mutant commits live on sandbox-only branches `mut-c1/M1…M8`.
The old counter is the contract `.ufo/waves/round-26/contract.md` command
(with `git -C <repo>` pointed at the scratch clone, the sole substitution);
the new counter is `bash .ufo/waves/round-26/count-c1.sh <rev>` run from the
lanes (amendment A1; lane path baked in, and it reads the frozen phrase list
via `git show 28b049400…:c1-phrases.txt`, so it is rev-pinned for phrases).

## 1. Counter semantics (what the two commands print)

Old command prints `stale_present=n` (0..4 frozen phrases still present in
their exact file, byte-fixed, line-scoped) and `r26_entry=present|absent`.
New command prints `stale_present`, `r26_entry`, `r26_new_source_ids`
(count of S### ids in the r26 entry's `source:` line with id > 113) and
`r12_names_r26` (occurrences of `userspace-oom-killers-r26.md` in the r12
file). The new counter additionally folds whitespace (`tr -s ' \n\t'`,
strips `*`) before the fixed-string match, exits 2 on bad rev or missing
file, and reads the phrase list from a pinned commit.

Both counters accept "0 / present" as the declared after-state. I define
- KILLED = counter output on the mutant ≠ the accepted after-state
  (old: `stale_present=0 && r26_entry=present`; new: same, plus it flags
  `r26_new_source_ids=0` or `r12_names_r26` drop as observable changes).
- SURVIVED = counter output on the mutant is byte-identical to baseline in
  the fields that gate the claim, even though the mutant keeps a stale
  present-tense statement alive.

## 2. Reference baseline (fixed state)

Built in the scratch clone as `mut-c1/fixed` (dbe95cd):
- r12.md claim host-state bullet and Observed paragraph rewritten as dated
  past-tense records; the four frozen phrases removed from their files;
- `corpus/knowledge/userspace-oom-killers-r26.md` added with a `source:`
  line carrying round-26 S-ids (S114…S126) and host state.

Baseline outputs:
- old: `stale_present=0 r26_entry=present`
- new: `stale_present=0 r26_entry=present r26_new_source_ids=11 r12_names_r26=3`

## 3. Mutants and verdicts

| M | defect at F1 site (r12 claim sentence) | old | new | old verdict | new verdict | stale statement still alive? |
|---|---|---|---|---|---|---|---|
| M1 | paraphrase: dated rewrite replaced by present-tense `…units are inactive, so a probe must render…` (no frozen bytes) | 0/present | 0/present, r12_names_r26=2 | SURVIVES | SURVIVES (signal only) | yes |
| M2 | re-case: `were inactive` → `were Inactive` | 0/present | 0/present | SURVIVES | SURVIVES | yes (same wording) |
| M3 | move to another file: claim sentence moved to `oom-kill-counter-kernel-only-r12.md`; r12 keeps paraphrase | 0/present | 0/present | SURVIVES | SURVIVES | yes (moved file) |
| M4 | split the line: frozen sentence split across two lines | 0/present | **1/present** | SURVIVES | KILLED | yes |
| M5a | emphasis inside phrase: `**were inactive**` | 0/present | 0/present | SURVIVES | SURVIVES | yes |
| M5b | emphasis around whole phrase: `**On 2026-10-19 … inactive**` | 0/present | 0/present | SURVIVES | SURVIVES | yes |
| M6 | zero-width space inside `inactive` | 0/present | 0/present | SURVIVES | SURVIVES | yes (invisible) |
| M7 | delete only the r26 entry | 0/**absent** | 0/absent, r26_new_source_ids=0 | KILLED | KILLED | — (missing superseding entry) |
| M8 | banner without fixing: banner added, frozen phrase kept | **1/present** | 1/present | KILLED | KILLED | yes (phrase kept) |

Hash evidence (before/after): the reference r12 blob sha256
`e9217da94e0e6139ee2e53c12a63b3c3eea22f61082b37ec774ee7c0d2cbdb95`,
restored after the run (working tree sha256 matches; `git status` clean).

## 4. Findings

1. Old counter kills only literal-preserving mutants (M7, M8). It is blind
   to paraphrase, case, file-move, line-split, emphasis and zero-width
   insertion — the eight listed evasion classes, six survive.
2. New counter (A1) additionally kills M4 (split the line) via whitespace
   folding. It still SURVIVES M1/M2/M3/M5/M6: fixed-string matching cannot
   flag paraphrase, case, moved-file, or zero-width-space mutations; that is
   a semantic gap, not fixable by whitespace folding.
3. New counter's `r12_names_r26` is a helpful second signal: M1/M3/M6 drop
   it from 3 to 2 (the superseding entry is no longer named in r12). It is
   not gating today; I recommend making it a gate (≥1) so a fix cannot
   silently unhook r12 from the r26 entry.
4. `r26_new_source_ids` gates the "opened in round 26" requirement partially
   by ID range (S>113); it cannot tell whether the row was actually opened
   this round. Acceptable heuristic; keep.
5. The old counter reads the phrase list from the working tree, not from the
   tested rev (new counter pins to 28b049400…). Recommend using the pinned
   form only.

## 5. Stronger counter (stays one command over committed bytes)

Proposal: keep `count-c1.sh` shape, add (a) whitespace folding (already
present), (b) case-folding (`tr 'A-Z' 'a-z'`) and stripping of zero-width
space (`tr -d '\u200b'`) before matching, and (c) a gate on
`r12_names_r26≥1`. Command (verbatim, one line over committed bytes):

```sh
R=${1:?rev}; L=/home/vgpnk/Projects/shokunin/mori-shokunin; git -C "$L" rev-parse -q --verify "$R^{commit}" >/dev/null || { echo bad_rev; exit 2; }; n=0; while IFS='|' read -r f p; do b=$(git -C "$L" show "$R:$f" 2>/dev/null) || { echo "missing=$f"; exit 2; }; printf '%s' "$b" | tr -d '\u200b' | tr 'A-Z' 'a-z' | tr -s ' \n\t' '   ' | grep -q -F -- "$(printf '%s' "$p" | tr 'A-Z' 'a-z')" && n=$((n+1)); done < <(git -C "$L" show 28b0494004fe1f064544224eca56dd42605db384:.ufo/waves/round-26/c1-phrases.txt); echo "stale_present=$n"; git -C "$L" cat-file -e "$R:corpus/knowledge/userspace-oom-killers-r26.md" && echo r26_entry=present || echo r26_entry=absent; git -C "$L" show "$R:corpus/knowledge/userspace-oom-killers-r12.md" | grep -c -F 'userspace-oom-killers-r26.md'
```

This kills M2 (case), M4 (split) and gates M1/M3/M6 via the r12_names_r26
drop; paraphrase remains outside any fixed-string counter's reach (report as
accepted residual).
