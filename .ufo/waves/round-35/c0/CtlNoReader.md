# C0 control — CtlNoReader (no-reader / delete), variants A and B

Control: contract §Controls item 2 ("no-reader / delete: the `## Capabilities` sections removed, or an
empty `## Capabilities` heading appended"). Both variants were built and scored in the sandbox clone only;
the lane repo, fleet repo, contract and counter were not modified.

What work it skips: the entire claimed C1 register. It binds none of the 18 admitted capability keys to
their closure, round or evidence; if either variant printed `C1=met` the counter's lower bound would be
defeated.

Counter run (frozen, unmodified):
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py`
sha256 `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167`

## Build

Sandbox (all git commands with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset):

```
mkdir -p /fast/scratch/hyaku/mori-r35/CtlNoReader
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r35/CtlNoReader/clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git -C /fast/scratch/hyaku/mori-r35/CtlNoReader/clone checkout -q -b ctl-no-reader-a f2d28711ee723c969b6c2008d32df498192f9e7b
```

Variant A: two exact-string edits (edit tool) removed the full text of both base sections — `## Capabilities`
(SCORECARD.md:586, empty `— none yet —` table plus its paragraph) and `## Capabilities (round 12
demonstrations)` (SCORECARD.md:627, five rows) — each heading through its body up to the next `## ` heading.
`grep -n '^## Capabilities' SCORECARD.md` after the edits returns nothing. Commit:

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C <clone> \
  -c user.name=ctl -c user.email=ctl@local commit -qam 'ctl: no-reader variant A — remove all ## Capabilities sections'
```

Variant A commit: `aa90aa4f06c5b101d702b47bf766de27d9387edf` (1 file changed, 18 deletions: SCORECARD.md only).

Variant B: `git checkout -q -B ctl-no-reader-b f2d28711ee723c969b6c2008d32df498192f9e7b`, then appended the
section whose exact bytes are saved at `c0/CtlNoReader-register.md` (heading + 5-column header + separator;
no data rows). Commit:

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C <clone> \
  -c user.name=ctl -c user.email=ctl@local commit -qam 'ctl: no-reader variant B — append empty ## Capabilities register (header only)'
```

Variant B commit: `64fe5337570f5fdfd63cf7000f3a3669ada2b241` (1 file changed, 5 insertions: SCORECARD.md only).

## Scores

Variant A:

```
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py aa90aa4f06c5b101d702b47bf766de27d9387edf --repo /fast/scratch/hyaku/mori-r35/CtlNoReader/clone
```

stdout, exit 1:

```
row rounds[313].capabilities_added[0] missing
row rounds[339].capabilities_added[0] missing
row rounds[345].capabilities_added[0] missing
row rounds[353].capabilities_added[0] missing
row rounds[386].capabilities_added[0] missing
row rounds[386].capabilities_added[1] missing
row rounds[386].capabilities_added[2] missing
row rounds[398].capabilities_added[0] missing
row rounds[427].capabilities_added[0] missing
row rounds[443].capabilities_added[0] missing
row rounds[443].capabilities_added[1] missing
row rounds[455].capabilities_added[0] missing
row rounds[455].capabilities_added[1] missing
row rounds[462].capabilities_added[0] missing
row rounds[476].capabilities_added[0] missing
row rounds[476].capabilities_added[1] missing
row rounds[495].capabilities_added[0] missing
row rounds[495].capabilities_added[1] missing
label=P-C1 rev=aa90aa4f06c5b101d702b47bf766de27d9387edf manifest_rev=37b51a243302 register=None oracle=18 rows=0 matched=0 missing=18 bad=0 extra=0 mismatches=18 C1=unmet
```

Exit: 1. Verdict: **unmet** (expected; no counter defect).

Variant B:

```
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py 64fe5337570f5fdfd63cf7000f3a3669ada2b241 --repo /fast/scratch/hyaku/mori-r35/CtlNoReader/clone
```

stdout, exit 1:

```
row rounds[313].capabilities_added[0] missing
row rounds[339].capabilities_added[0] missing
row rounds[345].capabilities_added[0] missing
row rounds[353].capabilities_added[0] missing
row rounds[386].capabilities_added[0] missing
row rounds[386].capabilities_added[1] missing
row rounds[386].capabilities_added[2] missing
row rounds[398].capabilities_added[0] missing
row rounds[427].capabilities_added[0] missing
row rounds[443].capabilities_added[0] missing
row rounds[443].capabilities_added[1] missing
row rounds[455].capabilities_added[0] missing
row rounds[455].capabilities_added[1] missing
row rounds[462].capabilities_added[0] missing
row rounds[476].capabilities_added[0] missing
row rounds[476].capabilities_added[1] missing
row rounds[495].capabilities_added[0] missing
row rounds[495].capabilities_added[1] missing
label=P-C1 rev=64fe5337570f5fdfd63cf7000f3a3669ada2b241 manifest_rev=37b51a243302 register='## Capabilities register' oracle=18 rows=0 matched=0 missing=18 bad=0 extra=0 mismatches=18 C1=unmet
```

Exit: 1. Verdict: **unmet** (expected; no counter defect).

## Summary

- Variant A `C1=unmet`, exit 1, missing=18.
- Variant B `C1=unmet`, exit 1, missing=18.
- Neither variant prints `C1=met`; P-C1's lower bound (`missing == 0`) catches the register-absent and
  register-heading-only forms. No skip-the-work finding, so no contract-a1 amendment is indicated by this control.
- Residual, by construction: B exercises only the header-stripping path (`rows=0` after the `Key` header is
  discarded); a non-`Key`/`Capability` header would surface as `extra=1` and also be unmet.

Sandbox: clone left at /fast/scratch/hyaku/mori-r35/CtlNoReader/clone on branch `ctl-no-reader-b`; no
background processes, no tool installs, no writes outside `c0/` in the lane repo.
