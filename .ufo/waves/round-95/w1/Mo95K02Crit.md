# Mo95K02Crit — round 95 attempt 1, wave w1 (critic: harm check six axes + discernment review)

Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`. Entering `754f4991198c16ddd1d4a3ea9206cfb7d74d6827`;
freeze/HEAD observed `2dc476d7fdb68bf916685a9f217a92047662baeb` (`git rev-parse HEAD`, unchanged across this
seat's runs). Freeze delta `git diff --stat 754f4991..2dc476d7` = exactly 5 files, 399 insertions, all under
`.ufo/waves/round-95/` (contract, count-c1.py 234, count-c2.sh 57, evidence/before-c1-r95.txt, evidence/before-c2-r95.txt).
Pristine counter pin verified: `git show 754f4991:.ufo/waves/round-94/count-c1v2.py | sha256sum` →
`6eb7fa4cf0ecf86064bb2714a5b93b52bf3356dc6e38e5dc7ee51f7255a7b384` = PRISTINE_SHA256. Installs: none.
Scratch `$S=/fast/scratch/hyaku/mori-r95/Mo95K02Crit`, deleted before yield. No git/jj mutation anywhere; read-only git in the lane only.

## Verdict per axis

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | unchanged-or-improved | My fresh run of the frozen battery (§H1 command block): `C1=met survivors=0 killed=7/7 before_r94_survivors=4 r94_survivor_ids=m2,m3,m4,m6` rc=0, byte-identical to `evidence/before-c1-r95.txt`. Fixtures non-vacuous: EXPECTED pristine-verdict mismatch is exit 2 and no mismatch fired. |
| operability | improved (capability reproduced fresh) | My fresh run of `count-c2.sh`: `HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=754f4991198c` rc=0, identical to `evidence/before-c2-r95.txt`. |
| depth | unchanged | No depth claim is made by the frozen artifacts; nothing regressed (§H1: no lane/fleet writes). |
| freshness | unchanged | Counters pin entering `754f4991` and BASE `84b15230`; sha pin verified above; no staleness introduced. |
| coverage | improved, with named residuals | Battery extended 3→7 fixtures; m2/m3/m4/m6 now killed on my run. Residuals: three undeclared uncovered conjuncts demonstrated as survivors (§H4), and the round-94 routed C2-side mutant battery amendment is not present in round 95 (§H5). |
| adjacency | unchanged (no harm) | §H1: counters write only under their scratch; lane porcelain identical before/after; host home and mounts intact. |

## H1. Adjacency — namespace sandbox write paths; NO-HARM

Every write path of the frozen counters (code inspection + runtime evidence):

`count-c2.sh` — all writes under its own scratch:
- `:22-23` `root=${TMPDIR:-…}/mori-r95`; `mkdir -p`; `:24` `mktemp -d "$root/c2-XXXXXX"`; `:25` `trap 'rm -rf -- "$S"' EXIT`. With `TMPDIR=$S` passed by me, everything lands in my scratch.
- `:26-27` `git clone -q --no-local --no-checkout -- "$lane" "$S/clone"` + detach: clone written **into scratch only**; the lane is read (no alternates, no hardlinks into the lane).
- `:28` `cp "$fleet/scripts/sources-census.sh" "$S/census.sh"`: fleet root is **read**; the copy lands in scratch. Fleet census file unchanged (before/after `ls -l`: same size 35466, mtime Oct 19 21:22).
- `:36-39` `in_ns()`: `env -i … unshare -rm sh -c 'mount -t tmpfs tmpfs "$1" …' sh "$home_dir"` — the tmpfs is mounted **inside the new mount+user namespace** over the account home; `env -i` drops the environment; `HOME="$S/home"`.
- `:43` hidden-probe is a `test ! -e` read. `:44-46` the three counter runs read `$S/clone` and write nothing outside scratch.

`count-c1.py` — all writes under its scratch: `:170` `os.makedirs(root)`, `:171` `mkdtemp(prefix="c1-", dir=root)`, `:174` `git clone -q --no-local --no-checkout` into scratch, `:193-196` `v-*` variant dirs, census-fail stub written in scratch, fixture commits made inside the scratch clone only; `:230` `finally: shutil.rmtree(scratch)`. Lane read via `git show`/clone; census script read.

Runtime evidence (lane, before vs after both counter runs):

```
git -C $LANE status --porcelain | tee $S/porcelain-before.txt   # 7 lines
… run count-c1.py (rc=0), run count-c2.sh (rc=0) …
git -C $LANE status --porcelain | tee $S/porcelain-after.txt    # 7 lines
diff porcelain-before.txt porcelain-after.txt → (identical)
git -C $LANE rev-parse HEAD → 2dc476d7fdb68bf916685a9f217a92047662baeb   (unchanged)
```

Porcelain (both snapshots): ` M corpus/SOURCES.md`, plus untracked `.ufo/waves/round-95/evidence/census-before-r95.txt`,
`w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.dispatched`, `w1/`. The tracked modification and the
untracked wave files pre-date my runs (orchestrator/seats, not counters); `corpus/SOURCES.md` is tracked-tree and
was already ` M` before my runs and is byte-wise untouched by them (diff of porcelain identical; counters never
touch the lane tree — their only lane interaction is `git clone --no-local` reads). Granularity note: porcelain
lists `w1/` as a directory, so sibling report writes inside it would not show; the counters' write surfaces are
fully enumerated above and are scratch-only.

Host-state evidence after the namespace runs:

```
ls -l /home/vgpnk/Projects/shokunin/scripts/sources-census.sh   → present, 35466 bytes, mtime Oct 19 21:22 (unchanged)
grep -E 'tmpfs .*/home/vgpnk' /proc/self/mounts                 → no match, grep_rc=1 (no tmpfs leaked to the host mount table)
```

The tmpfs-over-home exists only inside the namespace; on exit it is gone. Nothing under the fleet root or the
lane tracked tree is written by either counter. **NO-HARM.**

## H2. Scratch residue — counters clean up after themselves; NO-HARM

`ls -la /fast/scratch/hyaku/mori-r95` before my runs: six seat dirs (`Mo95Conn01`, `Mo95K01Crit`, `Mo95K02Crit` (empty),
`Mo95M01Mut`, `Mo95M02Mut`, `Mo95Sc01Lesson`). After both counters (and my H4 probes), same six dirs; my dir contains
only my own evidence files (`porcelain-before.txt`, `porcelain-after.txt`, `c1-out.txt`, `c2-out.txt`, `h4-out.txt`,
`h4_driver.py`). **No `c1-*` or `c2-*` directory survives** — `count-c1.py:230` `finally: shutil.rmtree` and
`count-c2.sh:25` `trap rm -rf EXIT` both fired (both runs reached rc=0 paths that pass through the cleanup).
The counters left zero residue under `$HYAKU_SCRATCH/mori-r95`.

## H3. Sysctl and namespace limits — unchanged; NO-HARM

```
cat /proc/sys/user/max_user_namespaces   → 122865 (before all runs)
unshare -rm sh -c 'cat /proc/sys/user/max_user_namespaces' → 2147483647  (the new namespace's own scoped view; a read, not a write)
… both counters ran (each calls unshare -rm) …
cat /proc/sys/user/max_user_namespaces   → 122865 (after all runs)
```

Host value identical before/after; neither counter writes `/proc/sys` (no sysctl access anywhere in
`count-c2.sh` or `count-c1.py`); the only namespace mechanism is `unshare -rm` inside the counters' own scratch
runs, plus one read-only `unshare -rm cat` probe of mine. This matches the contract's stated limit
("read-only here; no sysctl is changed") and the S626/S627 mechanism (mount namespace; per-user-namespace sysctl
view). **NO-HARM.**

## H4. Coverage of the mutant set — NOT complete: three undeclared, uncovered conjuncts (observed survivors)

The seven scored mutants are all killed on my fresh run (rc=0): `KILL m1/m1b/m7 by=R94-L,R94-R,R94-M`,
`KILL m2 by=R95-LEN`, `m3 by=R95-CEN`, `m4 by=R95-TRIO`, `m6 by=R95-PAT`; `crash_ids=-`; m5 declared equivalent
(`count-c1v2.py:183` — `adm_fail != 0` short-circuits; `adm_ok + adm_fail = 19` always). The fixture recipes are
exactly the single-variable kill controls the round-94 mutation probe proposed (`w1/Mo94M01Mut.md`: 5-char
prefix → m2; failing census stub → m3; recheck-line removal → m4; body-only append → m6).

Conjuncts of `count-c1v2.py` **not covered by the seven and not declared** (contract declares only m5; round-94
lesson Mistakes row `control-battery-gap` lists only C1 m2/m3/m4/m6 + C2 m1/m2/m3/m5/m6). I built four further
single-edit mutants, asserted unique anchors, and scored them on the frozen seven-fixture set using the frozen
battery's own `build_fixtures`/`run_counter` unmodified (scratch driver, `pristine_sha 6eb7fa4c…`, 7 fixtures):

| probe | edit (count-c1v2.py line) | verdict on the seven fixtures |
|---|---|---|
| m8 | skip seven_same gate (`:187-188` → `if False:`) | **SURVIVOR** — verdict tuple identical to pristine on all 7 fixtures. No fixture perturbs any SEVEN file, so `checks_failed` never contains `seven_same`; a skip-mutant is undetectable. |
| m9 | `tok = value[0]` → `value[-1]` (`:102`) | KILLED by R95-CEN/R95-PAT/R95-TRIO (some live verified-at values are multi-token, so last-token flips `admission` into `checks_failed` on fixtures whose pristine failure is another gate). First-token selection **is** covered — incidentally, via the checks_failed list; no dedicated fixture needed. |
| m10 | drop the verified-at constraint in `one_verified_at_change` (`:118-119` → `return (len(removed)==1 and len(added)==1)`) | **SURVIVOR** — identical on all 7. On every fixture the constraint is redundant: R94-* replace the line in place (removed and added both verified-at), R95-TRIO removes 1/adds 0, R95-PAT removes 0/adds 1, so the length-1 counts alone decide. A mutation that counts any single changed line as a "verified-at patch" passes the whole battery. |
| m11 | widen the head window (`:65` `n=12` → `n=200`) | **SURVIVOR** — identical on all 7. No fixture places `verified-at:`/keys beyond line 12; this is exactly the window-edge gap the round-94 critic named (`w1/Mo94K02Crit.md` §4: the battery "never exercises the 12-line head edge") — still undeclared in round 95. |

Driver output: `SURVIVOR m8_seven_same_skip diffs=none_identical_on_all_7`, `KILLED m9_last_token
diffs=R95-CEN,R95-PAT,R95-TRIO`, `SURVIVOR m10_verified_at_constraint_drop diffs=none_identical_on_all_7`,
`SURVIVOR m11_window_widen diffs=none_identical_on_all_7`.

Minor rule note: the docstring kill rule is "the `C1=` token plus the checks_failed list", but `count-c1.py:212`
compares the full verdict tuple including returncode — strictly stronger than documented (an exit-code-only
mutant would be killed). Direction is kills-more, so `killed=7/7` is unaffected; one line for the lesson.

Disposition: per the contract's own amendment rule ("a mutant that survives after landing is reported as a
residual, not patched into the frozen battery"), m8/m10/m11 are **residuals to name in the round-95 lesson**, not
a defect of the scored predicate — the C1 claim as frozen (seven killed, pristine green, non-vacuous fixtures,
before reproduced at 4 survivors) holds on my run. Impact if unnamed: coverage/discernment (the battery would
again self-claim more than it kills).

## H5. Discernment — round-94 spot-check §2 disagreements vs round 95

Source: `corpus/lessons/round-94-verifier-spotcheck.md` §2 "Claim re-checks" (C1 verified — no disagreement; C2
axis-move **NOT admitted**, adopting K01's objections `w1/Mo94K01Crit.md` §2c/2e/2f), with the routed set in §6
("next round = 95") and round-94 lesson Mistakes rows 2-3 (`corpus/lessons/round-94.md:35-37`).

| §2 disagreement | Round 95 response | Status |
|---|---|---|
| successor-as-before — C2 "before" was absence of the round-94 files, not a move on a pre-existing artifact (K01 §2f) | P-C2r95's before is the **pre-existing round-93 counter** (`count-c2.sh:31`), measured in-namespace (`C1=unmet(rc=1)` on my run) and restated as a **capability row** with first-working round (contract §C2) — exactly K01's "would change the verdict" option | **ADDRESSED** (my run exits 0; operator acceptance of the capability framing remains the open L0 side) |
| env-fail-open — `env_unset=rc2` also passes when the counter file is missing (K01 §2c; routed fix: "check the C1_SETUP line text, not only the exit code", round-94.md:36) | Not implemented literally: no `count-c2.sh` line greps `C1_SETUP`. Neutralized **structurally**: (c) requires the AFTER counter to print `C1=met` rc 0 (`:51,56` — a missing counter fails), and (d) the positive control requires the same BEFORE counter to print `C1=met` rc 0 outside the namespace (`:53`) — so its in-namespace rc≠0 is attributable to the namespace, not a missing file (a missing counter would print `NONE` and fail (d)) | **PARTIAL** — the fail-open class cannot pass the new gate, but the routed C1_SETUP-text check is unimplemented; the lesson must say which mechanism it claims |
| contract said "HOME unset" while the arm set `HOME=/nonexistent` (K01 §2f) | Superseded by a stronger mechanism: real absence — tmpfs mounted over the actual account home inside `unshare -rm`, `hidden=1` tested on the real probe path (`:33,43`); contract states the limit (hides only the account home; userns availability is host configuration) | **ADDRESSED** |

Still open from spot-check §6 (round 95 does not carry these; correctly or not):

1. §6.2 **C2 half of the frozen-battery amendment** — round-94.md:37 routes C2 mutants m1/m2/m3/m5/m6 of
   `count-c2v2.py` to "a frozen-battery amendment … before any new scoring". Round 95 amends only the C1 battery
   (count-c1.py); there is no C2-side mutant battery in `.ufo/waves/round-95/`. **OPEN.**
2. §6.3 routed C1_SETUP-text check — see PARTIAL above. **OPEN as written.**
3. §6.4 D1 planner binding — contract §Planner discloses the mapping again and keeps D1 operator-owned; matches
   K02 §3 / spot-check: disclosure does not close it. **OPEN (operator).**
4. §6.5 sibling host-literal class — routed via L0 to owning lanes; mori edits no siblings. **OPEN (operator), by design.**
5. §6.6 digest debt P4 and round-90 nonce guard — carried; nothing in round 95 touches them. **OPEN.**
6. Closure note's ask that future rounds commit a **landing-hash receipt** — round-95 evidence/ carries
   entering/freeze receipts only; landing receipts are prospective (L1 at integration). **OPEN (prospective).**

## Commands (exact)

```
# H1/H2/H3 before
mkdir -p /fast/scratch/hyaku/mori-r95/Mo95K02Crit
ls -la /fast/scratch/hyaku/mori-r95; cat /proc/sys/user/max_user_namespaces
git -C $LANE status --porcelain; git -C $LANE rev-parse HEAD

# C1 battery (frozen bytes; TMPDIR explicit)
TMPDIR=$S python3 -I $LANE/.ufo/waves/round-95/count-c1.py 754f4991198c16ddd1d4a3ea9206cfb7d74d6827 \
  --lane $LANE --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh     # rc=0, 118.9 s wall

# C2 namespace counter (frozen bytes; TMPDIR explicit)
TMPDIR=$S bash $LANE/.ufo/waves/round-95/count-c2.sh 754f4991198c16ddd1d4a3ea9206cfb7d74d6827 \
  $LANE /home/vgpnk/Projects/shokunin                                               # rc=0

# H1/H2/H3 after
git -C $LANE status --porcelain; diff porcelain-before.txt porcelain-after.txt      # identical
cat /proc/sys/user/max_user_namespaces; ls -la $S; ls -la /fast/scratch/hyaku/mori-r95
grep -E 'tmpfs .*/home/vgpnk' /proc/self/mounts                                     # no match

# H4 probes
TMPDIR=$S python3 -I $S/h4_driver.py    # reuses frozen build_fixtures/run_counter; rc=0, 66.3 s
```

Cleanup: `rm -rf -- /fast/scratch/hyaku/mori-r95/Mo95K02Crit` executed after this report was written.

SEAT Mo95K02Crit NO-HARM
