# Mo94R01Atk — C1 predicate attack (P-C1 `admission_token_ok`), round-94 w1

Attacks the frozen v2 rule `admission_token_ok` in `.ufo/waves/round-94/count-c1v2.py` (freeze
6b65e7c11f318481d5efa0429cdabb50743a2cc2): first whitespace token of `verified-at:` is ≥7 chars and a
prefix of the admission `%h`. All runs go through the public main path
`python3 -I count-c1v2.py R --repo <clone> --census <fleet>/scripts/sources-census.sh`, exit 0 = met, 1 = unmet.
Fixture file: `corpus/knowledge/counter-win-r77.md`; admission hash re-derived exactly as the counter does:
`git log --diff-filter=A --format=%h 7b3fe9d540c9 -- corpus/knowledge/counter-win-r77.md | tail -1` → `6a230c4b`
(re-ran inside the seat clone, same value; donor file `audit-r11.md` → `e4855e8c`). Base 84b152308fa6;
every fixture = one commit on detached BASE changing only that one verified-at line (F6 inserts one decoy
line ahead of the intact original; diff verified per fixture: 2 changed lines, F6 = 1 insertion, file line
counts 119/119/120 asserted). Scratch `/fast/scratch/hyaku/mori-r94/Mo94R01Atk` (one live shared clone,
fixture dirs via `mktemp -d` under it, `TMPDIR`/`HOME` passed explicitly to every counter run); deleted at
the end of this session. No tooling installed. Lane untouched.

## Forgery results (v2 verdicts observed)

| id | token bytes on the verified-at line | v2 observed (rc) | classification | frozen P-C1 text already rejects? |
|----|-------------------------------------|------------------|----------------|-----------------------------------|
| F2 | `6a230c4b,` (comma directly after) | `C1=unmet … adm_ok=18 adm_fail=1 … checks_failed=admission` (1) | admission forgery | yes — token not a prefix |
| F3 | `6a230c４b` (4→U+FF14 fullwidth lookalike) | `… adm_fail=1 … checks_failed=admission` (1) | admission forgery | yes — non-ASCII token not a byte prefix |
| F4 | `6a230c4z` (7-char prefix, 8th char replaced) | `… adm_fail=1 … checks_failed=admission` (1) | admission forgery | yes — not a prefix |
| F5 | `6a230c4b)` (closing paren, no space) | `… adm_fail=1 … checks_failed=admission` (1) | admission forgery | yes — not a prefix |
| F6 | line1 `verified-at: deadbeef (decoy…)` + line2 the true `verified-at: 6a230c4b (…)` | `… adm_fail=1 … patched12=11 … checks_failed=admission,patched12` (1) | admission forgery (true hash on 2nd line; counter reads 1st) | yes — `verified_at()` takes the first `verified-at:` line; decoy token not a prefix |
| F7 | `e4855e8` (7-char prefix of audit-r11's admission, not this file's) | `… adm_fail=1 … checks_failed=admission` (1) | admission forgery (claims another file's admission) | yes — not a prefix of THIS file's `%h` |
| F8 | `6A230C4B` (uppercase) | `… adm_fail=1 … checks_failed=admission` (1) | admission forgery (same commit, different bytes) | yes — prefix is byte-exact |
| F9 | `​6a230c4b` (U+200B zero-width space before hash) | `… adm_fail=1 … checks_failed=admission` (1) | admission forgery (visually identical line) | yes — ZWSP-led token not a prefix |
| F1 | `6a230c4b\t` (trailing tab) | `C1=met trio=98 … adm_ok=19 … patched12=12 seven_same=7 census=ok` (0) | harmless — tab is a token delimiter, token unchanged | no — and correctly so |

Eight genuine admission forgeries, none in the frozen battery (battery = hex-embed left/right/middle).
v2 false passes found: **0/8**. In every forgery the sole non-admission checks stay green
(`trio=98 patched12=12 seven_same=7 census=ok`), so `checks_failed=admission` isolates the defect; F6's
`patched12=11` is inherent to its required second line (diff is +1/−0, not the 1-for-1 line swap
`one_verified_at_change` demands).

## Legitimate forms (must read met — none rejected)

| id | form | v2 observed (rc) |
|----|------|------------------|
| L1 | `verified-at: 6a230c4b (…)` one space — the unmodified base, no fixture commit | `C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=84b152308fa6` (0) |
| L2 | `verified-at:6a230c4b (…)` no space after colon | `C1=met trio=98 … adm_ok=19 … patched12=12 seven_same=7 census=ok` (0) |
| L3 | `verified-at: 6a230c4b\t` hash followed by tab (same fixture as F1) | `C1=met trio=98 … adm_ok=19 … patched12=12 seven_same=7 census=ok` (0) |

## Commands (exact)

Setup and fixture protocol (per fixture; toplevel asserted equal to the fixture dir before committing):

```
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin "$S/clone"
D=$(mktemp -d "$S/fxt-<id>.XXXXXX") && git clone --shared --no-checkout "$S/clone" "$D"
git -C "$D" rev-parse --show-toplevel      # == $D
git -C "$D" checkout -q --detach 84b152308fa6c2f224ad75dff68e525dab9057ac
# rewrite corpus/knowledge/counter-win-r77.md with the one-line variant (python writer, kept bytes otherwise)
git -C "$D" add corpus/knowledge/counter-win-r77.md
git -C "$D" -c user.name=Mo94R01Atk -c user.email=Mo94R01Atk@fixture.invalid -c commit.gpgsign=false \
    commit -q -m "r94 w1 attack fixture <id>"
```

Counter invocation (identical shape for every row; TMPDIR/HOME/SHOKUNIN_ROOT explicit, never inherited):

```
TMPDIR=$S/tmp HOME=$S/tmp SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin python3 -I \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-94/count-c1v2.py <rev> \
  --repo <fixture-clone> --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
```

Observed exits: L1 rc=0; L2 rc=0; L3 rc=0; F2 rc=1; F3 rc=1; F4 rc=1; F5 rc=1; F6 rc=1; F7 rc=1; F8 rc=1; F9 rc=1.
Sample verbatim unmet line (F2, rev b7e5a0a4aaf4): `C1=unmet trio=98 files=19 adm_ok=18 adm_fail=1 patched12=12 seven_same=7 census=ok checks_failed=admission rev=b7e5a0a4aaf4`.
Fixture revs (12-hex): L2 f2075c63d3c5, L3 14defe48dec2, F2 b7e5a0a4aaf4, F3 483e8d7724ce, F4 d761a5806381,
F5 5be5f5b70614, F6 860129d73a1b, F7 9c4d6756593c, F8 9af75f2a83b9, F9 8859272c8178.

## Findings

1. **No bypass.** Eight out-of-battery forgery shapes, zero v2 false passes. The `str.startswith` prefix
   rule (S624 semantics) plus the ≥7 length gate reject every shape whose token is not byte-for-byte a
   prefix of the admission `%h`; the token-boundary fix covers far more than the battery's hex-embeds.
2. **Harmless-form tolerance is deliberate and consistent**: any whitespace run after the colon (space,
   tab, multiple spaces) yields the same token; L2 shows the space after the colon is optional. No legit
   form is rejected — the kill-rule clause "v2 reads any live trio file as adm_fail" is not at risk from
   these shapes.
3. **Diagnosability is clean**: forgeries fail with `checks_failed=admission` alone; the counter's
   admission check is independent of the trio/patched12/seven_same/census checks.
4. **F6 shape is structurally rejected, with a side effect**: the counter reads the FIRST `verified-at:`
   line, so a decoy-first/two-line form can never sneak the true second-line hash past it; the same
   insertion necessarily costs `patched12` (the counter demands exactly one removed+added line). A
   last-line-reading variant of this check WOULD be fooled by F6 — worth keeping in the lesson.
5. **Named limits re-confirmed, not extended**: a true 7-char prefix of the file's own hash still passes
   (by design; the contract's `%h`-shortening limit already covers it). Sub-7 tokens were not separately
   run — the length gate is exercised by the rule text and F4/F7 shapes.

## Residual risk / verification gaps

- v1 was not re-run on these fixtures (seat scope is the v2 predicate; the frozen battery covers v1).
- Compound forgeries (e.g. uppercase+comma) and a full-8-char donor hash were not separately run; both
  fail by the same already-demonstrated non-prefix mechanism.
- Adjacent non-battery axes untouched: no attack on `one_verified_at_change`/`unchanged`/census or on
  unicode-whitespace token splitting (e.g. NBSP) — different seat territory.

Report file count: within the 120-line limit. Scratch (clone, 10 fixture dirs, tmp, driver, results)
removed after this file was written.
