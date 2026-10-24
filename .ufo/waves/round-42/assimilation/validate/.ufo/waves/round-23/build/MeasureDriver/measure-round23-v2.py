#!/usr/bin/env python3
"""Round-23 measurement driver, v2 (MeasureDriver seat).

Written after `.ufo/waves/round-23/preseal-amendment.md` and after the L1's
tightening note. The v1 driver (`measure-round23.py`) is preserved unchanged;
this file supersedes it for measurement.

    measure-round23-v2.py --revision REV --seal SEAL_REV --output ABSENT_DIR

What v2 adds over v1 (nothing else changed, and v1 is preserved):

  * strict ancestry: SEAL != REV and `merge-base --is-ancestor SEAL REV` = 0.
  * seal proof: the production quota path is ABSENT at SEAL, and the reconciler
    at SEAL is byte-identical to the entering revision.
  * `tools/` diff seal->REV must be exactly: reconciler modified, quota added.
  * harnesses (oracles, frozen files, r22 builder/requirements) are staged from
    the committed SEAL bytes and executed from there; the working copies are
    compared with their committed bytes; the executing driver must equal the
    committed seal copy of itself.
  * every frozen dependency is hashed; the r22 builder and r22 requirements
    digests are pinned against the frozen c1-requirements.json.
  * the original 26 C1 requirements keep their own denominator and are never
    merged with the supplementary guards.
  * supplementary C1 guards, all byte-exact rather than behavioural:
      - source-byte guard: the production source must equal the *baseline git
        blob* of the entering revision after EXACTLY two transformations
        (SCHEMA v1->v2 literal substitution, deletion of the single alias
        producer fragment, each substring exactly once in the baseline), with
        the target SHA-256 frozen in this driver before the implementation, and
        the file mode unchanged at 100755;
      - discrimination self-test of that guard (no historical r22 mutants);
      - before/after output equality replayed on the SAME synthetic fixture
        instance: a check output must carry the alias before and the frozen tool
        digests, a setup envelope must carry neither, and all other keys and
        values must be equal, including argv (sys.argv[1:] excludes the tool
        path); the after tool must self-report the frozen target SHA-256;
      - selftest output schema;
      - observed real population: the frozen identity pins over the sorted full
        four-tuples (path, line, class, line_sha256) with the r22 driver's exact
        encoding, plus the same-command swapped scanner/policy twin that must
        not match (supplementary C1 only; the original 26 denominator is
        untouched).
  * heavy scratch under /fast/scratch/hyaku/mori-r23/MeasureDriver; /tmp is
    never used.

The output directory must not exist. Exit code is 0 iff all_claim_checks_pass.
No privileged, mutating or host-remediating command is issued; the only host
reads are the ones the C2 real control needs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/mori-shokunin')
WAVE_REL = '.ufo/waves/round-23'
WAVE = LANE / WAVE_REL
ENTERING = '1bfe708a170c877db3319060d0ab38771efe03ac'

SCRATCH_ROOT = Path('/fast/scratch/hyaku/mori-r23/MeasureDriver')

RETENTION_REL = 'tools/mori-retention-reconcile.py'
QUOTA_REL = 'tools/mori-quota-surface.py'

FROZEN_PREFIX = WAVE_REL + '/frozen'
RENAME_ORACLE_REL = WAVE_REL + '/oracle-rename.py'
QUOTA_ORACLE_REL = WAVE_REL + '/oracle-quota.py'
CONTRACT_REL = WAVE_REL + '/contract.md'
AMENDMENT_REL = WAVE_REL + '/preseal-amendment.md'
PROPOSALS_REL = WAVE_REL + '/cases-proposed'
DRIVER_REL = WAVE_REL + '/build/MeasureDriver/measure-round23-v2.py'

R22_BUILDER_REL = '.ufo/waves/round-22/frozen/fixture-builder-v2.py'
R22_REQUIREMENTS_REL = '.ufo/waves/round-22/frozen/requirements-v2.json'

C1_REQUIREMENTS_REL = FROZEN_PREFIX + '/c1-requirements.json'
C1_REAL_REL = FROZEN_PREFIX + '/c1-expected-real.json'
C1_IDENTITIES_REL = FROZEN_PREFIX + '/c1-expected-real-identities.json'
C1_SOURCE_DELTA_REL = FROZEN_PREFIX + '/c1-source-delta.json'
C2_REAL_REL = FROZEN_PREFIX + '/c2-expected-real.json'
QUOTA_CASES_REL = FROZEN_PREFIX + '/quota-cases'

SCHEMA_V1 = 'mori-retention-reconciliation-v1'
SCHEMA_V2 = 'mori-retention-reconciliation-v2'
SCHEMA_LITERAL_V1 = "SCHEMA='" + SCHEMA_V1 + "'"
SCHEMA_LITERAL_V2 = "SCHEMA='" + SCHEMA_V2 + "'"
ALIAS_FRAGMENT = "'raw_unallowlisted':len(unallowed),"
ALIAS_KEY = 'raw_unallowlisted'

# Frozen before the implementation, from the pre-seal amendment and from the
# baseline git blob of the entering revision.
ENTERING_SOURCE_SHA256 = '0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32'
TARGET_SOURCE_SHA256 = '4599ee1aff95f21714e320a87fd31260f0435aa9c7a9884ac60ab952fe099a36'
TARGET_MODE = '100755'

# Only these three keys are treated specially in the before/after output
# comparison; argv is NOT special (same instance -> identical sys.argv[1:]).
SPECIAL_OUTPUT_KEYS = ('schema', ALIAS_KEY, 'tool_sha256')

C1_REQUIREMENT_COUNT = 26
C1_BEFORE_UNMET = ['R25']

ORIGINAL_26_CHECKS = ('C17.c1_before_requirement_counts', 'C18.c1_after_requirement_counts',
                      'C19.c1_alias_removed', 'C20.c1_schema_v2_after')
SUPPLEMENTARY_CHECKS = ('C21.c1_source_byte_guard', 'C22.c1_source_guard_discriminates',
                         'C23.c1_same_instance_output_equivalence', 'C24.c1_selftest_schema',
                         'C35.c1_real_identity_pins')
REAL_CONTROL_CHECKS = ('C25.c1_real_control_matches_frozen', 'C29.c2_real_control_matches_frozen',
                       'C30.c2_oracle_real_control_agrees')

SUBPROCESS_TIMEOUT = 900


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dumps(obj) -> str:
    return json.dumps(obj, sort_keys=True, indent=2) + '\n'


def git_bytes(args, timeout=SUBPROCESS_TIMEOUT):
    return subprocess.run(['git', '-C', str(LANE)] + [str(x) for x in args],
                          capture_output=True, timeout=timeout)


def git_show(rev: str, rel: str):
    """Committed blob bytes for rel at rev, or None when absent."""
    cp = git_bytes(['show', rev + ':' + rel])
    return cp.stdout if cp.returncode == 0 else None


def git_mode(rev: str, rel: str):
    """Committed file mode for rel at rev, or None when absent."""
    cp = git_bytes(['ls-tree', rev, '--', rel])
    if cp.returncode != 0:
        return None
    line = cp.stdout.decode('ascii', 'replace').strip()
    return line.split()[0] if line else None


def git_tree(rev: str, prefix: str):
    """Map of path -> 'mode type oid' for a revision prefix, or None on error."""
    cp = git_bytes(['ls-tree', '-r', '-z', '--full-tree', rev, '--', prefix])
    if cp.returncode != 0:
        return None
    rows = {}
    for record in cp.stdout.split(b'\0'):
        if not record:
            continue
        meta, _, path = record.partition(b'\t')
        mode, kind, oid = meta.split(b' ', 2)
        rows[path.decode('utf-8')] = (mode.decode('ascii') + ' ' + kind.decode('ascii') + ' '
                                      + oid.decode('ascii'))
    return rows


def transform_source(source: bytes):
    """Apply exactly the two pre-registered transformations to the baseline blob.

    Returns (transformed_bytes, reason); reason is None on success.
    """
    try:
        text = source.decode('utf-8')
    except UnicodeDecodeError:
        return None, 'baseline_not_utf8'
    if text.count(SCHEMA_LITERAL_V1) != 1:
        return None, 'schema_literal_not_exactly_once_in_baseline'
    if text.count(ALIAS_FRAGMENT) != 1:
        return None, 'alias_fragment_not_exactly_once_in_baseline'
    out = text.replace(SCHEMA_LITERAL_V1, SCHEMA_LITERAL_V2)
    out = out.replace(ALIAS_FRAGMENT, '', 1)
    return out.encode('utf-8'), None


class Driver:
    def __init__(self, revision: str, seal: str, output: Path):
        self.revision = revision
        self.seal = seal
        self.output = output
        self.checks = []
        self.observations = []
        self.scratch = SCRATCH_ROOT / ('measure-' + output.name)
        self.env = dict(os.environ)
        self.env['TMPDIR'] = str(SCRATCH_ROOT)
        self.env['PYTHONDONTWRITEBYTECODE'] = '1'

    # ---------------------------------------------------------------- helpers
    def check(self, cid: str, ok, detail: str, **extra):
        row = {'id': cid, 'pass': bool(ok), 'detail': detail}
        row.update(extra)
        self.checks.append(row)
        return row

    def observe(self, oid: str, detail: str, **extra):
        row = {'id': oid, 'detail': detail}
        row.update(extra)
        self.observations.append(row)
        return row

    def record(self, name: str, argv, timeout=SUBPROCESS_TIMEOUT):
        cp = subprocess.run([str(x) for x in argv], env=self.env, capture_output=True,
                            text=True, timeout=timeout)
        row = {'schema': 'mori-r23-command-receipt-v1', 'name': name,
               'measured_revision': self.revision, 'seal_revision': self.seal,
               'argv': [str(x) for x in argv],
               'recorded_utc': datetime.now(timezone.utc).isoformat(),
               'exit_code': cp.returncode, 'stdout': cp.stdout, 'stderr': cp.stderr}
        (self.output / (name + '.json')).write_text(dumps(row))
        return cp

    def json_file(self, path):
        try:
            return json.loads(Path(path).read_bytes())
        except (OSError, ValueError):
            return None

    def stage_bytes(self, rel: str, rev: str, target: Path):
        data = git_show(rev, rel)
        if data is None:
            return None
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return data

    # ------------------------------------------------------------- main flow
    def run(self):
        self.output.mkdir(parents=True, exist_ok=False)
        SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
        if self.scratch.exists():
            # Only this driver's own scratch space is ever removed; the fresh
            # fixture roots below must not exist before the oracles create them.
            shutil.rmtree(self.scratch)
        self.scratch.mkdir(parents=True, exist_ok=False)
        staged = self.scratch / 'staged'
        wave_tree = self.scratch / 'wave-tree'
        wave_tree.mkdir(parents=True, exist_ok=True)

        summary = {
            'schema': 'mori-r23-measurements-v2',
            'driver': 'measure-round23-v2.py',
            'measured_revision': self.revision,
            'seal_revision': self.seal,
            'entering_revision': ENTERING,
            'lane': str(LANE),
            'scratch_root': str(SCRATCH_ROOT),
            'driver_sha256': sha(Path(__file__).read_bytes()),
            'driver_path': str(Path(__file__).resolve()),
            'recorded_utc': datetime.now(timezone.utc).isoformat(),
        }

        # 1. revision resolution and strict ancestry ---------------------------
        rev_cp = git_bytes(['rev-parse', '--verify', '--quiet', self.revision + '^{commit}'])
        seal_cp = git_bytes(['rev-parse', '--verify', '--quiet', self.seal + '^{commit}'])
        resolved_revision = rev_cp.stdout.decode('ascii', 'replace').strip()
        resolved_seal = seal_cp.stdout.decode('ascii', 'replace').strip()
        ancestry = git_bytes(['merge-base', '--is-ancestor', self.seal, self.revision])
        ancestry_ok = ancestry.returncode == 0
        distinct = bool(resolved_seal) and bool(resolved_revision) and resolved_seal != resolved_revision
        self.check('C00.revisions_resolve',
                   rev_cp.returncode == 0 and seal_cp.returncode == 0,
                   'the measured revision and the seal revision must both resolve to commits',
                   measured_revision_resolved=resolved_revision, seal_revision_resolved=resolved_seal)
        self.check('C01.seal_is_strict_ancestor_of_revision', ancestry_ok and distinct,
                   'the seal must be a strict ancestor of the measured revision (SEAL != REV and is-ancestor 0)',
                   argv=['git', '-C', str(LANE), 'merge-base', '--is-ancestor', self.seal, self.revision],
                   returncode=ancestry.returncode, seal_equals_revision=not distinct)
        summary['ancestry'] = {
            'seal_is_strict_ancestor_of_revision': bool(ancestry_ok and distinct),
            'argv': ['git', '-C', str(LANE), 'merge-base', '--is-ancestor', self.seal, self.revision],
            'returncode': ancestry.returncode,
            'seal_revision_resolved': resolved_seal,
            'measured_revision_resolved': resolved_revision,
            'seal_equals_revision': not distinct,
        }

        # 2. seal proof ---------------------------------------------------------
        seal_quota = git_show(self.seal, QUOTA_REL)
        self.check('C02.seal_quota_production_path_absent', seal_quota is None,
                   'tools/mori-quota-surface.py must be absent at the seal (production path)',
                   present_at_seal=seal_quota is not None)
        entering_reconciler = git_show(ENTERING, RETENTION_REL)
        seal_reconciler = git_show(self.seal, RETENTION_REL)
        reconciler_identical = (entering_reconciler is not None and seal_reconciler is not None
                                and entering_reconciler == seal_reconciler)
        self.check('C03.seal_reconciler_entering_identical', reconciler_identical,
                   'the reconciler at the seal must be byte-identical to the entering revision',
                   entering_sha256=sha(entering_reconciler) if entering_reconciler else None,
                   seal_sha256=sha(seal_reconciler) if seal_reconciler else None)

        required_at_seal = [
            RENAME_ORACLE_REL, QUOTA_ORACLE_REL, C1_REQUIREMENTS_REL, C1_REAL_REL, C2_REAL_REL,
            CONTRACT_REL, AMENDMENT_REL, R22_BUILDER_REL, R22_REQUIREMENTS_REL, DRIVER_REL,
        ]
        seal_content = {}
        missing_at_seal = []
        for rel in required_at_seal:
            data = git_show(self.seal, rel)
            seal_content[rel] = {'present': data is not None,
                                 'sha256': sha(data) if data is not None else None}
            if data is None:
                missing_at_seal.append(rel)
        seal_cases = git_tree(self.seal, QUOTA_CASES_REL) or {}
        seal_proposals = git_tree(self.seal, PROPOSALS_REL) or {}
        self.check('C04.seal_contains_harnesses_driver_and_dependencies', not missing_at_seal,
                   'the seal must carry the oracles, the driver, the frozen controls, the contract, '
                   'the amendment and the r22 builder/requirements dependencies',
                   missing=missing_at_seal, sealed_cases=len(seal_cases),
                   sealed_proposals=len(seal_proposals))
        self.check('C05.seal_contains_accepted_case_files', len(seal_cases) > 0,
                   'the seal must contain the accepted C2 case files', cases=sorted(seal_cases))
        self.check('C06.seal_contains_original_proposals', len(seal_proposals) > 0,
                   'the seal must retain the original case proposals', proposals=sorted(seal_proposals))
        summary['seal_proof'] = {
            'quota_production_path_absent_at_seal': seal_quota is None,
            'reconciler_entering_identical_at_seal': reconciler_identical,
            'sealed_content': seal_content,
            'sealed_cases': sorted(seal_cases),
            'sealed_proposals': sorted(seal_proposals),
        }

        # 3. the tools/ delta between seal and revision -------------------------
        diff_cp = git_bytes(['diff', '--name-status', self.seal, self.revision, '--', 'tools/'])
        diff_rows = [line for line in diff_cp.stdout.decode('utf-8', 'replace').split('\n') if line.strip()]
        diff_pairs = sorted(tuple(line.split('\t')) for line in diff_rows if '\t' in line)
        expected_diff = sorted([('M', RETENTION_REL), ('A', QUOTA_REL)])
        self.check('C07.tools_delta_seal_to_revision_exact', diff_pairs == expected_diff,
                   'the tools/ delta between seal and revision must be exactly: reconciler modified, '
                   'quota added', observed=diff_pairs, expected=[list(x) for x in expected_diff],
                   raw=diff_rows)
        summary['tools_delta'] = {'observed': [list(x) for x in diff_pairs],
                                  'expected': [list(x) for x in expected_diff]}

        # 4. frozen artefacts byte-identical between seal and revision -----------
        frozen_seal = git_tree(self.seal, FROZEN_PREFIX)
        frozen_rev = git_tree(self.revision, FROZEN_PREFIX)
        frozen_paths = sorted(set(frozen_seal or {}) | set(frozen_rev or {}))
        frozen_rows = {}
        frozen_identical = True
        for path in frozen_paths:
            at_seal = git_show(self.seal, path)
            at_rev = git_show(self.revision, path)
            same = at_seal is not None and at_rev is not None and at_seal == at_rev
            frozen_identical = frozen_identical and same
            frozen_rows[path] = {'seal_sha256': sha(at_seal) if at_seal is not None else None,
                                 'revision_sha256': sha(at_rev) if at_rev is not None else None,
                                 'byte_identical': same}
        self.check('C08.frozen_byte_identical_seal_to_revision', frozen_identical,
                   'every frozen artefact must exist at the seal and at the revision with identical bytes',
                   files=len(frozen_rows),
                   divergent=[p for p, r in frozen_rows.items() if not r['byte_identical']])

        oracle_rows = {}
        oracles_identical = True
        for rel in (RENAME_ORACLE_REL, QUOTA_ORACLE_REL):
            at_seal = git_show(self.seal, rel)
            at_rev = git_show(self.revision, rel)
            same = at_seal is not None and at_rev is not None and at_seal == at_rev
            oracles_identical = oracles_identical and same
            oracle_rows[rel] = {'seal_sha256': sha(at_seal) if at_seal is not None else None,
                                'revision_sha256': sha(at_rev) if at_rev is not None else None,
                                'byte_identical': same}
        self.check('C09.sealed_oracles_byte_identical', oracles_identical,
                   'the sealed oracles must be byte-identical between the seal and the revision',
                   divergent=[p for p, r in oracle_rows.items() if not r['byte_identical']])

        docs_rows = {}
        docs_identical = True
        for rel in (CONTRACT_REL, AMENDMENT_REL):
            at_seal = git_show(self.seal, rel)
            at_rev = git_show(self.revision, rel)
            same = at_seal is not None and at_rev is not None and at_seal == at_rev
            docs_identical = docs_identical and same
            docs_rows[rel] = {'seal_sha256': sha(at_seal) if at_seal is not None else None,
                              'revision_sha256': sha(at_rev) if at_rev is not None else None,
                              'byte_identical': same}
        self.check('C10.contract_and_amendment_unchanged_since_seal', docs_identical,
                   'the pre-registered contract and the pre-seal amendment must be unchanged between '
                   'the seal and the revision', documents=docs_rows)

        summary['sealed_artifacts'] = {'frozen': frozen_rows, 'oracles': oracle_rows,
                                       'documents': docs_rows}

        # 5. dependency pinning -------------------------------------------------
        requirements_bytes = git_show(self.seal, C1_REQUIREMENTS_REL)
        requirements = json.loads(requirements_bytes.decode('utf-8')) if requirements_bytes else None
        binding_targets = {
            'contract_sha256': CONTRACT_REL,
            'fixture_builder_sha256': R22_BUILDER_REL,
            'oracle_sha256': RENAME_ORACLE_REL,
            'r22_requirements_v2_sha256': R22_REQUIREMENTS_REL,
        }
        binding_rows = {}
        bindings_ok = requirements is not None
        for key, rel in binding_targets.items():
            expected = (requirements or {}).get(key)
            at_seal = git_show(self.seal, rel)
            at_rev = git_show(self.revision, rel)
            seal_digest = sha(at_seal) if at_seal is not None else None
            rev_digest = sha(at_rev) if at_rev is not None else None
            same = expected is not None and expected == seal_digest == rev_digest
            bindings_ok = bindings_ok and same
            binding_rows[key] = {'path': rel, 'pinned': expected, 'seal_sha256': seal_digest,
                                 'revision_sha256': rev_digest, 'matches': same}
        self.check('C11.dependencies_pinned', bindings_ok,
                   'the frozen c1-requirements digests must match the committed artefacts at the seal '
                   'and at the revision', bindings=binding_rows)
        summary['dependency_pinning'] = binding_rows

        dependency_digests = {}
        for rel in (R22_BUILDER_REL, R22_REQUIREMENTS_REL, RENAME_ORACLE_REL, QUOTA_ORACLE_REL,
                    DRIVER_REL, CONTRACT_REL, AMENDMENT_REL, RETENTION_REL, QUOTA_REL):
            data = git_show(self.seal, rel)
            dependency_digests[rel] = sha(data) if data is not None else None
        for path, row in sorted(frozen_rows.items()):
            dependency_digests[path] = row['seal_sha256']
        summary['frozen_dependency_digests'] = dependency_digests

        # 6. stage the harnesses from the committed seal bytes -------------------
        for rel in (RENAME_ORACLE_REL, QUOTA_ORACLE_REL, R22_BUILDER_REL, R22_REQUIREMENTS_REL,
                    CONTRACT_REL, AMENDMENT_REL):
            self.stage_bytes(rel, self.seal, wave_tree / rel)
        for path in (frozen_seal or {}):
            self.stage_bytes(path, self.seal, wave_tree / path)
        rename_oracle = wave_tree / RENAME_ORACLE_REL
        quota_oracle = wave_tree / QUOTA_ORACLE_REL
        staged_cases = wave_tree / QUOTA_CASES_REL
        staged_requirements = wave_tree / C1_REQUIREMENTS_REL
        staged_c1_real = wave_tree / C1_REAL_REL
        staged_c1_identities = wave_tree / C1_IDENTITIES_REL
        staged_c1_source_delta = wave_tree / C1_SOURCE_DELTA_REL
        staged_c2_real = wave_tree / C2_REAL_REL

        worktree_rows = {}
        worktree_ok = True
        for rel in (RENAME_ORACLE_REL, QUOTA_ORACLE_REL, C1_REQUIREMENTS_REL, C1_REAL_REL,
                    C2_REAL_REL, R22_BUILDER_REL, R22_REQUIREMENTS_REL):
            on_disk = LANE / rel
            committed = git_show(self.seal, rel)
            same = on_disk.is_file() and committed is not None and on_disk.read_bytes() == committed
            worktree_rows[rel] = {'worktree_matches_sealed_bytes': same}
            worktree_ok = worktree_ok and same
            self.observe('worktree.' + rel,
                         'working-tree copy compared with the committed seal bytes (informational)',
                         worktree_matches_sealed_bytes=same)
        for path in sorted((frozen_seal or {})):
            on_disk = LANE / path
            committed = git_show(self.seal, path)
            same = on_disk.is_file() and committed is not None and on_disk.read_bytes() == committed
            worktree_rows[path] = {'worktree_matches_sealed_bytes': same}
            worktree_ok = worktree_ok and same
            self.observe('worktree.' + path,
                         'working-tree copy compared with the committed seal bytes (informational)',
                         worktree_matches_sealed_bytes=same)
        self.check('C12.working_copies_match_committed_seal_bytes', worktree_ok,
                   'the measured working copies of the harnesses and frozen files must equal their '
                   'committed seal bytes',
                   divergent=[k for k, r in worktree_rows.items() if not r['worktree_matches_sealed_bytes']])
        summary['worktree_comparison'] = worktree_rows

        driver_self = sha(Path(__file__).read_bytes())
        sealed_driver = git_show(self.seal, DRIVER_REL)
        driver_match = sealed_driver is not None and sha(sealed_driver) == driver_self
        self.check('C13.driver_matches_sealed_bytes', driver_match,
                   'the executing driver must be the committed seal copy of itself',
                   executed_sha256=driver_self,
                   sealed_sha256=sha(sealed_driver) if sealed_driver is not None else None,
                   sealed_path=DRIVER_REL)
        summary['driver_binding'] = {'executed_sha256': driver_self,
                                     'sealed_sha256': sha(sealed_driver) if sealed_driver else None,
                                     'matches': driver_match}

        # 7. stage the candidate tools from the measured revision ----------------
        after_dir = staged / 'after'
        before_dir = staged / 'before'
        retention_after = after_dir / 'mori-retention-reconcile.py'
        retention_before = before_dir / 'mori-retention-reconcile.py'
        quota_after = after_dir / 'mori-quota-surface.py'
        quota_before = before_dir / 'mori-quota-surface.py'

        retention_after_bytes = self.stage_bytes(RETENTION_REL, self.revision, retention_after)
        retention_before_bytes = self.stage_bytes(RETENTION_REL, ENTERING, retention_before)
        quota_after_bytes = self.stage_bytes(QUOTA_REL, self.revision, quota_after)
        quota_before_present = git_show(ENTERING, QUOTA_REL) is not None
        if quota_before.exists():
            quota_before.unlink()
        self.check('C14.quota_tool_absent_at_entering_revision', not quota_before_present,
                   'tools/mori-quota-surface.py must be absent at the entering revision',
                   entering_present=quota_before_present)
        self.check('C15.quota_tool_present_at_measured_revision', quota_after_bytes is not None,
                   'tools/mori-quota-surface.py must exist at the measured revision')
        self.check('C16.retention_tool_present_at_both_revisions',
                   retention_after_bytes is not None and retention_before_bytes is not None,
                   'tools/mori-retention-reconcile.py must exist at both revisions')
        summary['staged_tools'] = {
            RETENTION_REL: {
                'revision': {'sha256': sha(retention_after_bytes) if retention_after_bytes else None,
                             'path': str(retention_after)},
                'entering': {'sha256': sha(retention_before_bytes) if retention_before_bytes else None,
                             'path': str(retention_before)},
                'revision_equals_entering': retention_after_bytes == retention_before_bytes,
            },
            QUOTA_REL: {
                'revision': {'sha256': sha(quota_after_bytes) if quota_after_bytes else None,
                             'path': str(quota_after)},
                'entering': {'sha256': None, 'path': str(quota_before), 'present': False},
            },
        }

        # 8. C1 original 26 requirements, before and after -----------------------
        c1_dir = self.scratch / 'c1'
        c1_dir.mkdir(parents=True, exist_ok=True)
        c1_before_out = c1_dir / 'before.json'
        c1_after_out = c1_dir / 'after.json'
        self.check('C31.rename_oracle_present_at_seal', rename_oracle.is_file(),
                   'the frozen C1 oracle must be staged from the seal')
        if rename_oracle.is_file():
            c1_before = self.record('c1-oracle-before',
                                     [sys.executable, rename_oracle, '--tool', retention_before,
                                      '--requirements', staged_requirements, '--output', c1_before_out])
            c1_after = self.record('c1-oracle-after',
                                    [sys.executable, rename_oracle, '--tool', retention_after,
                                     '--requirements', staged_requirements, '--output', c1_after_out])
        else:
            class _Absent:
                returncode = -1
                stdout = ''
                stderr = 'the frozen C1 oracle is unavailable at the seal'
            c1_before = c1_after = _Absent()
        before_obs = self.json_file(c1_before_out)
        after_obs = self.json_file(c1_after_out)

        def unmet_ids(obs):
            if not isinstance(obs, dict):
                return []
            return sorted(str(r.get('id')) for r in obs.get('results', []) if not r.get('pass'))

        def alias_runs(obs):
            if not isinstance(obs, dict):
                return None
            total = 0
            for row in obs.get('runs', []):
                try:
                    parsed = json.loads(row.get('stdout', ''))
                except (ValueError, TypeError):
                    continue
                if isinstance(parsed, dict) and ALIAS_KEY in parsed:
                    total += 1
            return total

        def is_check_output(obj):
            """A reconciliation result carries the counters; a setup envelope does not.

            The reconciler answers a failed check with
            {schema, finding_id, error, privacy_clearance, receipt_match} and never
            emits the alias key or a tool digest there, so the two shapes are compared
            by their own rules.
            """
            return isinstance(obj, dict) and 'raw_total' in obj and 'receipt_match' in obj

        c1_before_counts = (before_obs or {}).get('counts') or {}
        c1_after_counts = (after_obs or {}).get('counts') or {}
        before_unmet = unmet_ids(before_obs)
        after_unmet = unmet_ids(after_obs)
        before_alias = alias_runs(before_obs)
        after_alias = alias_runs(after_obs)

        self.check('C17.c1_before_requirement_counts',
                   before_obs is not None and c1_before_counts.get('total') == C1_REQUIREMENT_COUNT
                   and before_unmet == C1_BEFORE_UNMET,
                   'before the cutover exactly R25 may be unmet',
                   total=c1_before_counts.get('total'), pass_count=c1_before_counts.get('pass'),
                   unmet=before_unmet, oracle_exit=c1_before.returncode)
        self.check('C18.c1_after_requirement_counts',
                   after_obs is not None and c1_after_counts.get('total') == C1_REQUIREMENT_COUNT
                   and not after_unmet and c1_after_counts.get('unmet') == 0,
                   'after the cutover every original requirement must pass',
                   total=c1_after_counts.get('total'), pass_count=c1_after_counts.get('pass'),
                   unmet=after_unmet, oracle_exit=c1_after.returncode)
        self.check('C19.c1_alias_removed',
                   before_alias is not None and before_alias > 0 and after_alias == 0,
                   'misleading_alias_runs must be greater than 0 before and 0 after',
                   before=before_alias, after=after_alias,
                   oracle_counter={'before': (before_obs or {}).get('misleading_alias_runs'),
                                   'after': (after_obs or {}).get('misleading_alias_runs')})
        after_schema_ok = ((after_obs or {}).get('schema_v2_runs')
                           == (after_obs or {}).get('parsed_runs'))
        self.check('C20.c1_schema_v2_after',
                   bool(after_schema_ok) and (after_obs or {}).get('parsed_runs', 0) > 0,
                   'every parsed oracle run after the cutover must carry schema ' + SCHEMA_V2,
                   schema_v2_runs=(after_obs or {}).get('schema_v2_runs'),
                   parsed_runs=(after_obs or {}).get('parsed_runs'))
        for name, path in (('c1-before-observed.json', c1_before_out),
                           ('c1-after-observed.json', c1_after_out)):
            if path.exists():
                (self.output / name).write_bytes(path.read_bytes())

        # 9. C1 supplementary guards ---------------------------------------------
        supplementary = {}

        # 9a. source-byte guard on the baseline git blob
        baseline_mode = git_mode(ENTERING, RETENTION_REL)
        target_mode = git_mode(self.revision, RETENTION_REL)
        guard = {
            'baseline': {'revision': ENTERING, 'path': RETENTION_REL,
                         'sha256': sha(entering_reconciler) if entering_reconciler else None,
                         'pinned_sha256': ENTERING_SOURCE_SHA256,
                         'mode': baseline_mode},
            'transformations': [
                {'kind': 'substitution',
                 'from': SCHEMA_LITERAL_V1, 'to': SCHEMA_LITERAL_V2,
                 'occurrences_in_baseline': (entering_reconciler.decode('utf-8').count(SCHEMA_LITERAL_V1)
                                             if entering_reconciler else None)},
                {'kind': 'deletion',
                 'fragment': ALIAS_FRAGMENT,
                 'occurrences_in_baseline': (entering_reconciler.decode('utf-8').count(ALIAS_FRAGMENT)
                                             if entering_reconciler else None)},
            ],
            'target': {'sha256_frozen_in_driver': TARGET_SOURCE_SHA256,
                       'mode': target_mode, 'mode_frozen_in_driver': TARGET_MODE},
        }
        expected_source, reason = (None, 'baseline_blob_absent')
        if entering_reconciler is not None:
            expected_source, reason = transform_source(entering_reconciler)
        guard['transform_reason'] = reason
        guard['target']['sha256_computed'] = sha(expected_source) if expected_source else None
        guard['observed_sha256'] = sha(retention_after_bytes) if retention_after_bytes else None
        observed_text = (retention_after_bytes.decode('utf-8')
                         if retention_after_bytes is not None else '')
        guard['target']['observed_v2_literal_count'] = observed_text.count(SCHEMA_LITERAL_V2)
        guard['target']['observed_v1_literal_count'] = observed_text.count(SCHEMA_LITERAL_V1)
        guard['target']['observed_alias_fragment_count'] = observed_text.count(ALIAS_FRAGMENT)
        guard_ok = bool(
            expected_source is not None and retention_after_bytes is not None
            and expected_source == retention_after_bytes
            and guard['target']['sha256_computed'] == TARGET_SOURCE_SHA256
            and guard['target']['sha256_frozen_in_driver'] == TARGET_SOURCE_SHA256
            and guard['observed_sha256'] == TARGET_SOURCE_SHA256
            and guard['baseline']['sha256'] == ENTERING_SOURCE_SHA256
            and all(t['occurrences_in_baseline'] == 1 for t in guard['transformations'])
            and guard['target']['observed_v2_literal_count'] == 1
            and guard['target']['observed_v1_literal_count'] == 0
            and guard['target']['observed_alias_fragment_count'] == 0
            and baseline_mode == TARGET_MODE and target_mode == TARGET_MODE)
        # The frozen source-delta artefact must agree with the constants frozen in this driver.
        delta_doc = self.json_file(staged_c1_source_delta)
        delta_rows = {}
        delta_ok = None
        if isinstance(delta_doc, dict):
            expected_replacements = [[SCHEMA_LITERAL_V1, SCHEMA_LITERAL_V2], [ALIAS_FRAGMENT, '']]
            delta_rows = {
                'entering_sha256': {'frozen': delta_doc.get('entering_sha256'),
                                    'driver': ENTERING_SOURCE_SHA256,
                                    'matches': delta_doc.get('entering_sha256') == ENTERING_SOURCE_SHA256},
                'transformed_sha256': {'frozen': delta_doc.get('transformed_sha256'),
                                       'driver': TARGET_SOURCE_SHA256,
                                       'matches': delta_doc.get('transformed_sha256') == TARGET_SOURCE_SHA256},
                'mode': {'frozen': delta_doc.get('mode'), 'driver': TARGET_MODE,
                         'matches': delta_doc.get('mode') == TARGET_MODE},
                'entering_revision': {'frozen': delta_doc.get('entering_revision'),
                                      'driver': ENTERING,
                                      'matches': delta_doc.get('entering_revision') == ENTERING},
                'replacements': {'frozen': delta_doc.get('replacements'),
                                 'driver': expected_replacements,
                                 'matches': delta_doc.get('replacements') == expected_replacements},
                'output_pair_normalization': {
                    'frozen': delta_doc.get('output_pair_normalization'),
                    'driver': list(SPECIAL_OUTPUT_KEYS),
                    'matches': sorted(delta_doc.get('output_pair_normalization') or [])
                    == sorted(SPECIAL_OUTPUT_KEYS)},
                'same_fixture_required': {'frozen': delta_doc.get('same_fixture_required'),
                                          'driver': True,
                                          'matches': bool(delta_doc.get('same_fixture_required'))},
            }
            delta_ok = all(row['matches'] for row in delta_rows.values())
        guard['frozen_source_delta'] = {'present': isinstance(delta_doc, dict), 'fields': delta_rows,
                                        'matches': delta_ok}
        guard_ok = bool(guard_ok and delta_ok is not False)
        guard['matches'] = bool(guard_ok)
        self.check('C21.c1_source_byte_guard', guard_ok,
                   'the production reconciler source must equal the baseline git blob of the entering '
                   'revision after exactly the two pre-registered transformations (each occurring '
                   'exactly once in the baseline), with the target SHA-256 frozen in this driver and '
                   'the file mode unchanged at 100755, and the frozen source-delta artefact must '
                   'agree with the constants frozen in this driver', guard=guard)
        supplementary['source_byte_guard'] = guard

        # 9b. the byte guard must reject any other code delta
        mutants = []
        if expected_source is not None:
            base = expected_source.decode('utf-8')
            candidates = {
                'appended_statement': base + '\n# mori mutant: extra statement\n',
                'removed_line': '\n'.join(line for line in base.split('\n')
                                          if "'receipt_authenticity':" not in line),
                'whitespace_only': base.replace('def check(a):', 'def check(a):  '),
            }
            for name, text in candidates.items():
                data = text.encode('utf-8')
                mutants.append({'mutant': name, 'sha256': sha(data),
                                'guard_rejects': bool(data != expected_source)})
        discriminating = bool(mutants) and all(m['guard_rejects'] for m in mutants)
        self.check('C22.c1_source_guard_discriminates', discriminating,
                   'the byte guard must reject a source that adds, removes or changes any other code',
                   mutants=mutants)
        supplementary['source_guard_mutants'] = mutants

        # 9c. before/after outputs on the SAME synthetic fixture instance
        replay_rows = []
        replay_ok = bool(after_obs) and bool((after_obs or {}).get('runs'))
        after_runs = (after_obs or {}).get('runs') or []
        for index, row in enumerate(after_runs):
            recorded_argv = row.get('argv')
            if not isinstance(recorded_argv, list) or len(recorded_argv) < 2:
                replay_ok = False
                replay_rows.append({'arm': str(row.get('variant')), 'error': 'no_recorded_argv'})
                continue
            before_argv = list(recorded_argv)
            before_argv[1] = str(retention_before)
            after_argv = list(recorded_argv)
            after_argv[1] = str(retention_after)
            bcp = self.record('c1-replay-entering-%02d' % index, before_argv)
            acp = self.record('c1-replay-measured-%02d' % index, after_argv)
            entry = {'arm': str(row.get('variant')), 'same_instance': True,
                     'before_exit': bcp.returncode, 'after_exit': acp.returncode,
                     'differences': []}
            try:
                bobj = json.loads(bcp.stdout)
            except (ValueError, TypeError):
                bobj = None
            try:
                aobj = json.loads(acp.stdout)
            except (ValueError, TypeError):
                aobj = None
            if not isinstance(bobj, dict) or not isinstance(aobj, dict):
                entry['differences'].append('stdout_not_an_object')
            else:
                if bcp.returncode != acp.returncode:
                    entry['differences'].append('exit_code')
                if bcp.stderr != acp.stderr:
                    entry['differences'].append('stderr')
                if bobj.get('schema') != SCHEMA_V1:
                    entry['differences'].append('before_schema')
                if aobj.get('schema') != SCHEMA_V2:
                    entry['differences'].append('after_schema')
                # A reconciliation result carries the counters; a setup envelope carries
                # only the error fields. Each shape is compared by its own rules; a
                # failing exit and a missing output are never suppressed.
                before_check = is_check_output(bobj)
                after_check = is_check_output(aobj)
                entry['before_shape'] = 'check' if before_check else 'setup'
                entry['after_shape'] = 'check' if after_check else 'setup'
                if before_check != after_check:
                    entry['differences'].append('output_shape')
                if before_check:
                    if ALIAS_KEY not in bobj:
                        entry['differences'].append('alias_absent_before')
                    if ALIAS_KEY in aobj:
                        entry['differences'].append('alias_present_after')
                    if set(aobj.keys()) != set(bobj.keys()) - {ALIAS_KEY}:
                        entry['differences'].append('key_set')
                    if bobj.get('tool_sha256') != ENTERING_SOURCE_SHA256:
                        entry['differences'].append('before_tool_sha256')
                    if aobj.get('tool_sha256') != TARGET_SOURCE_SHA256:
                        entry['differences'].append('after_tool_sha256')
                else:
                    # A setup envelope carries neither the alias nor a tool digest.
                    if ALIAS_KEY in bobj or ALIAS_KEY in aobj:
                        entry['differences'].append('alias_in_setup_output')
                    if 'tool_sha256' in bobj or 'tool_sha256' in aobj:
                        entry['differences'].append('tool_sha256_in_setup_output')
                    if set(aobj.keys()) != set(bobj.keys()):
                        entry['differences'].append('key_set')
                for keyname in sorted(set(bobj) - set(SPECIAL_OUTPUT_KEYS)):
                    if keyname not in aobj:
                        entry['differences'].append('missing_key:' + keyname)
                    elif aobj[keyname] != bobj[keyname]:
                        entry['differences'].append('value:' + keyname)
                for keyname in sorted(set(aobj) - set(bobj) - {ALIAS_KEY}):
                    entry['differences'].append('extra_key:' + keyname)
                if bobj.get('argv') != aobj.get('argv'):
                    entry['differences'].append('argv')
                entry['before_tool_sha256'] = bobj.get('tool_sha256')
                entry['after_tool_sha256'] = aobj.get('tool_sha256')
                entry['argv_equal'] = bobj.get('argv') == aobj.get('argv')
            if row.get('stdout') is not None and acp.stdout != row.get('stdout'):
                entry['differences'].append('after_replay_differs_from_oracle_record')
            entry['identical_apart_from_special_keys'] = not entry['differences']
            replay_ok = replay_ok and not entry['differences']
            replay_rows.append(entry)
        self.check('C23.c1_same_instance_output_equivalence', replay_ok,
                   'before and after must be replayed on the same synthetic fixture instance: a check '
                   'output must carry the alias before and the frozen tool digests, a setup envelope '
                   'must carry neither the alias nor a tool digest, and every other key and value '
                   'must be equal, including argv',
                   arms=len(replay_rows),
                   shapes={'check': sum(1 for r in replay_rows if r.get('before_shape') == 'check'),
                           'setup': sum(1 for r in replay_rows if r.get('before_shape') == 'setup')},
                   special_keys=list(SPECIAL_OUTPUT_KEYS),
                   divergent=[r.get('arm') for r in replay_rows if r.get('differences')])
        supplementary['same_instance_replay'] = {'arms': replay_rows}

        # 9d. selftest output schema
        selftest = {'available': False}
        if retention_after.is_file() and retention_before.is_file():
            bcp = self.record('c1-selftest-entering', [sys.executable, retention_before, '--selftest'])
            acp = self.record('c1-selftest-measured', [sys.executable, retention_after, '--selftest'])
            try:
                bobj = json.loads(bcp.stdout)
            except (ValueError, TypeError):
                bobj = None
            try:
                aobj = json.loads(acp.stdout)
            except (ValueError, TypeError):
                aobj = None
            selftest = {
                'available': isinstance(bobj, dict) and isinstance(aobj, dict),
                'entering': {'exit_code': bcp.returncode, 'schema': bobj.get('schema') if bobj else None,
                             'alias_present': bool(bobj) and ALIAS_KEY in bobj,
                             'tool_sha256': bobj.get('tool_sha256') if bobj else None},
                'measured': {'exit_code': acp.returncode, 'schema': aobj.get('schema') if aobj else None,
                             'alias_present': bool(aobj) and ALIAS_KEY in aobj,
                             'tool_sha256': aobj.get('tool_sha256') if aobj else None},
            }
            selftest['pass'] = bool(
                isinstance(bobj, dict) and isinstance(aobj, dict)
                and bobj.get('schema') == SCHEMA_V1 and aobj.get('schema') == SCHEMA_V2
                and ALIAS_KEY not in aobj and ALIAS_KEY not in bobj
                and set(aobj.keys()) == set(bobj.keys())
                and aobj.get('passed') == bobj.get('passed') and aobj.get('total') == bobj.get('total')
                and aobj.get('finding_id') == bobj.get('finding_id')
                and aobj.get('privacy_clearance') is False
                and bcp.returncode == acp.returncode)
        else:
            selftest['pass'] = False
        self.check('C24.c1_selftest_schema', selftest.get('pass'),
                   'the selftest output must carry the v1 schema before and the v2 schema after, with '
                   'no alias key and an otherwise identical payload', selftest=selftest)
        supplementary['selftest'] = selftest

        # 10. C1 real control ----------------------------------------------------
        c1_real = self.json_file(staged_c1_real)
        c1_real_result = {'available': c1_real is not None}
        c1_tool_present = retention_after.is_file()
        if c1_real is not None and c1_tool_present:
            paths = c1_real.get('paths', {})
            realcmd = [sys.executable, retention_after, 'check', '--repo', str(LANE),
                       '--rev', c1_real.get('input_revision'),
                       '--receipt', paths.get('receipt'),
                       '--policy', paths.get('policy'),
                       '--allowlist', paths.get('allowlist')]
            cp = self.record('c1-real-control', realcmd)
            try:
                real = json.loads(cp.stdout)
            except (ValueError, TypeError):
                real = None
            expected = c1_real.get('expected', {})
            key_rows = {}
            keys_ok = True
            for key, value in sorted(expected.items()):
                observed = real.get(key) if isinstance(real, dict) else None
                same = isinstance(real, dict) and type(observed) is type(value) and observed == value
                keys_ok = keys_ok and same
                key_rows[key] = {'expected': value, 'observed': observed, 'matches': same}
            forbidden_present = sorted(k for k in c1_real.get('forbidden_keys', [])
                                       if isinstance(real, dict) and k in real)
            digests_ok = (isinstance(real, dict)
                          and real.get('inputs_sha256') == c1_real.get('inputs_sha256'))
            revisions_ok = (isinstance(real, dict)
                             and real.get('input_revision') == c1_real.get('input_revision')
                             and real.get('measured_revision') == c1_real.get('measured_revision'))
            tool_digest_ok = (isinstance(real, dict)
                               and real.get('tool_sha256') == TARGET_SOURCE_SHA256)
            argv_ok = isinstance(real, dict) and real.get('argv') == [str(x) for x in realcmd[2:]]
            exit_ok = cp.returncode == c1_real.get('expected_exit')
            clearance_ok = isinstance(real, dict) and real.get('privacy_clearance') is False
            real_ok = bool(exit_ok and keys_ok and digests_ok and revisions_ok and tool_digest_ok
                           and argv_ok and clearance_ok and not forbidden_present)
            self.check('C25.c1_real_control_matches_frozen', real_ok,
                       'the C1 real control must reproduce the frozen receipt values exactly and the '
                       'tool must self-report the frozen target SHA-256',
                       exit_code=cp.returncode, expected_exit=c1_real.get('expected_exit'),
                       keys=key_rows, inputs_sha256_match=digests_ok, revisions_match=revisions_ok,
                       tool_sha256_match=tool_digest_ok, argv_match=argv_ok,
                       privacy_clearance_false=clearance_ok, forbidden_keys_present=forbidden_present)
            c1_real_result.update({'exit_code': cp.returncode, 'expected_exit': c1_real.get('expected_exit'),
                                   'keys': key_rows, 'inputs_sha256_match': digests_ok,
                                   'revisions_match': revisions_ok, 'tool_sha256_match': tool_digest_ok,
                                   'argv_match': argv_ok, 'privacy_clearance_false': clearance_ok,
                                   'forbidden_keys_present': forbidden_present, 'match': real_ok,
                                   'finding_id': real.get('finding_id') if isinstance(real, dict) else None,
                                   'schema': real.get('schema') if isinstance(real, dict) else None})
            (self.output / 'c1-real-control.json').write_text(
                dumps(real) if isinstance(real, dict) else dumps(cp.stdout))

            # Observed real population: the frozen identity pins (the r23 copy of the r22
            # file, unchanged) over the full four-tuple, with the r22 driver's exact
            # encoding, plus the same-command swapped twin that must not match.
            identity_doc = self.json_file(staged_c1_identities)
            identity_expected = (identity_doc or {}).get('digests') or {}

            def identity_digest(hits):
                return sha(json.dumps(sorted(tuple(hit[k] for k in ('path', 'line', 'class',
                                                                      'line_sha256'))
                                              for hit in hits), separators=(',', ':')).encode())

            identity_reason = None
            try:
                identity_observed = ({k: identity_digest(real.get(k, [])) for k in identity_expected}
                                     if isinstance(real, dict) else {})
            except (KeyError, TypeError, ValueError) as exc:
                identity_observed = {}
                identity_reason = 'identity_digest_error:' + type(exc).__name__
            identity_match = bool(identity_expected) and identity_observed == identity_expected
            twin_observed = dict(identity_observed)
            twin_observed['scanner_hits'], twin_observed['policy_excluded_hits'] = (
                identity_observed.get('policy_excluded_hits'), identity_observed.get('scanner_hits'))
            identity_twin_rejected = twin_observed != identity_expected
            receipt_pin = (identity_doc or {}).get('receipt_sha256')
            receipt_pin_ok = (receipt_pin is None
                              or (isinstance(real, dict)
                                  and (real.get('inputs_sha256') or {}).get('receipt') == receipt_pin))
            identity_ok = bool(identity_match and identity_twin_rejected and receipt_pin_ok
                               and identity_reason is None)
            self.check('C35.c1_real_identity_pins', identity_ok,
                       'the observed real population must match the frozen identity digests over the '
                       'sorted full four-tuples (path, line, class, line_sha256) with the r22 '
                       "driver's exact encoding, and the swapped scanner/policy twin must not match",
                       expected=identity_expected, observed=identity_observed,
                       identity_match=identity_match, twin_rejected=identity_twin_rejected,
                       receipt_sha256_pin=receipt_pin, receipt_pin_match=receipt_pin_ok,
                       reason=identity_reason, encoding=(identity_doc or {}).get('identity_encoding'))
            c1_real_result['identity_pins'] = {
                'expected': identity_expected, 'observed': identity_observed,
                'identity_match': identity_match, 'twin_rejected': identity_twin_rejected,
                'receipt_sha256_pin': receipt_pin, 'receipt_pin_match': receipt_pin_ok,
                'reason': identity_reason, 'match': identity_ok,
            }
            beforecmd = list(realcmd)
            beforecmd[1] = retention_before
            bcp = self.record('c1-real-control-entering', beforecmd)
            try:
                breal = json.loads(bcp.stdout)
            except (ValueError, TypeError):
                breal = None
            before_alias_present = isinstance(breal, dict) and ALIAS_KEY in breal
            after_alias_absent = isinstance(real, dict) and ALIAS_KEY not in real
            self.check('C26.c1_alias_present_before_absent_after',
                       before_alias_present and after_alias_absent,
                       'the misleading alias must be present in the entering revision output and gone after',
                       entering={'exit_code': bcp.returncode,
                                 'schema': breal.get('schema') if isinstance(breal, dict) else None,
                                 'alias_present': before_alias_present,
                                 'alias_value': breal.get(ALIAS_KEY) if isinstance(breal, dict) else None},
                       measured={'schema': real.get('schema') if isinstance(real, dict) else None,
                                 'alias_present': not after_alias_absent})
            c1_real_result['entering'] = {
                'exit_code': bcp.returncode,
                'schema': breal.get('schema') if isinstance(breal, dict) else None,
                'alias_present': before_alias_present,
                'alias_value': breal.get(ALIAS_KEY) if isinstance(breal, dict) else None,
            }
        else:
            reason = ('frozen c1-expected-real.json is unavailable at the seal'
                      if c1_real is None else
                      'tools/mori-retention-reconcile.py is unavailable at the measured revision')
            self.check('C25.c1_real_control_matches_frozen', False, reason)
            self.check('C26.c1_alias_present_before_absent_after', False, reason)
            self.check('C35.c1_real_identity_pins', False, reason)
        summary['c1_real_control'] = c1_real_result

        # 11. C2: sealed oracle before, after and with the real control ----------
        c2_real = self.json_file(staged_c2_real)
        case_files = sorted(staged_cases.glob('*.json')) if staged_cases.is_dir() else []
        c2_summary = {'cases': [p.name for p in case_files], 'cases_count': len(case_files),
                      'cases_source': 'staged from the committed seal bytes',
                      'oracle_present': quota_oracle.is_file(),
                      'oracle_sha256': sha(quota_oracle.read_bytes()) if quota_oracle.is_file() else None}

        def run_quota_oracle(name, tool, out, real_expected=None):
            out.parent.mkdir(parents=True, exist_ok=True)
            argv = [sys.executable, quota_oracle, '--tool', tool, '--cases', staged_cases,
                    '--output', out]
            if real_expected is not None:
                argv += ['--real-expected', real_expected]
            cp = self.record(name, argv)
            obs = self.json_file(out)
            if obs is None and 'usage' in (cp.stderr or '').lower():
                help_cp = self.record(name + '-help', [sys.executable, quota_oracle, '--help'])
                names = sorted(set(re.findall(r'--[A-Za-z][A-Za-z0-9-]*', help_cp.stdout)))

                def pick(*cands):
                    return next((n for n in names if any(c in n for c in cands)), None)

                tool_opt, cases_opt, out_opt, real_opt = (pick('tool'), pick('case'), pick('out'),
                                                           pick('real'))
                argv = [sys.executable, quota_oracle]
                if tool_opt:
                    argv += [tool_opt, tool]
                if cases_opt:
                    argv += [cases_opt, staged_cases]
                if out_opt:
                    argv += [out_opt, out]
                if real_expected is not None and real_opt:
                    argv += [real_opt, real_expected]
                cp = self.record(name + '-adapted', argv)
                obs = self.json_file(out)
            return cp, obs

        c2_before_out = self.scratch / 'c2' / 'before' / 'before.json'
        c2_after_out = self.scratch / 'c2' / 'after' / 'after.json'
        c2_real_out = self.scratch / 'c2' / 'after-real' / 'after.json'
        self.check('C32.c2_oracle_present_at_seal', quota_oracle.is_file(),
                   'the sealed C2 oracle must exist at the seal')
        if quota_oracle.is_file():
            c2_before_cp, c2_before_obs = run_quota_oracle('c2-oracle-before', quota_before,
                                                           c2_before_out)
            c2_after_cp, c2_after_obs = run_quota_oracle('c2-oracle-after', quota_after, c2_after_out)
            c2_real_cp, c2_real_obs = run_quota_oracle('c2-oracle-after-real', quota_after,
                                                        c2_real_out, real_expected=staged_c2_real)
        else:
            class _Absent:
                returncode = -1
                stdout = ''
                stderr = 'the sealed C2 oracle is unavailable at the seal'
            c2_before_cp = c2_after_cp = c2_real_cp = _Absent()
            c2_before_obs = c2_after_obs = c2_real_obs = None

        c2_before_counts = (c2_before_obs or {}).get('counts') or {}
        c2_after_counts = (c2_after_obs or {}).get('counts') or {}
        c2_summary['before'] = c2_before_counts
        c2_summary['after'] = c2_after_counts
        c2_summary['after_with_real_expected'] = (c2_real_obs or {}).get('counts') or {}

        self.check('C33.c2_before_capability_absent',
                   bool(c2_before_obs) and bool(case_files)
                   and c2_before_counts.get('capability_absent') == c2_before_counts.get('total')
                   and c2_before_counts.get('total') == len(case_files),
                   'before the cutover every sealed case must be capability_absent',
                   total=c2_before_counts.get('total'),
                   capability_absent=c2_before_counts.get('capability_absent'),
                   cases=len(case_files), oracle_exit=c2_before_cp.returncode)
        self.check('C34.c2_after_every_case_matches',
                   bool(c2_after_obs) and c2_after_counts.get('total') == len(case_files)
                   and c2_after_counts.get('unmet') == 0
                   and c2_after_counts.get('pass') == len(case_files),
                   'after the cutover every sealed case must match exactly',
                   total=c2_after_counts.get('total'), pass_count=c2_after_counts.get('pass'),
                   unmet=c2_after_counts.get('unmet'), cases=len(case_files),
                   oracle_exit=c2_after_cp.returncode)
        for name, path in (('c2-before-observed.json', c2_before_out),
                           ('c2-after-observed.json', c2_after_out),
                           ('c2-after-real-observed.json', c2_real_out)):
            if path.exists():
                (self.output / name).write_bytes(path.read_bytes())

        # 12. C2 real control, measured directly --------------------------------
        c2_real_result = {'available': c2_real is not None}
        c2_tool_present = quota_after.is_file()
        if c2_real is not None and c2_tool_present:
            cp = self.record('c2-real-control', [sys.executable, quota_after])
            try:
                observed = json.loads(cp.stdout)
            except (ValueError, TypeError):
                observed = None
            expected_paths = {row.get('path'): row for row in c2_real.get('expected_paths', [])}
            observed_paths = {}
            if isinstance(observed, dict):
                observed_paths = {row.get('path'): row for row in observed.get('paths', [])}
            path_rows = {}
            paths_ok = True
            for path, expected_row in sorted(expected_paths.items()):
                seen = observed_paths.get(path)
                row_ok = isinstance(seen, dict)
                for key in ('fstype', 'mount_point', 'quota_state', 'enforcement', 'basis',
                            'device_check'):
                    if not row_ok or seen.get(key) != expected_row.get(key):
                        row_ok = False
                paths_ok = paths_ok and row_ok
                path_rows[path] = {'expected': expected_row, 'observed': seen, 'matches': row_ok}
            exit_ok = cp.returncode == c2_real.get('expected_exit')
            finding_ok = (isinstance(observed, dict)
                          and observed.get('finding_id') == c2_real.get('expected_finding_id'))
            real_ok = bool(exit_ok and finding_ok and paths_ok and expected_paths
                           and set(observed_paths) == set(expected_paths))
            self.check('C29.c2_real_control_matches_frozen', real_ok,
                       'the C2 real control must reproduce the frozen host observation',
                       exit_code=cp.returncode, expected_exit=c2_real.get('expected_exit'),
                       finding_id=observed.get('finding_id') if isinstance(observed, dict) else None,
                       expected_finding_id=c2_real.get('expected_finding_id'),
                       paths=path_rows, observed_path_set=sorted(observed_paths),
                       expected_path_set=sorted(expected_paths))
            c2_real_result.update({'exit_code': cp.returncode,
                                   'expected_exit': c2_real.get('expected_exit'),
                                   'finding_id': observed.get('finding_id') if isinstance(observed, dict) else None,
                                   'expected_finding_id': c2_real.get('expected_finding_id'),
                                   'paths': path_rows, 'match': real_ok})
            (self.output / 'c2-real-control.json').write_text(
                dumps(observed) if isinstance(observed, dict) else dumps(cp.stdout))
            oracle_real_counts = c2_summary.get('after_with_real_expected') or {}
            self.check('C30.c2_oracle_real_control_agrees',
                       oracle_real_counts.get('unmet') == 0 and oracle_real_counts.get('total', 0) > 0,
                       'the sealed C2 oracle with --real-expected must report no unmet real-control '
                       'requirement', counts=oracle_real_counts, oracle_exit=c2_real_cp.returncode)
        else:
            reason = ('frozen c2-expected-real.json is unavailable at the seal'
                      if c2_real is None else
                      'tools/mori-quota-surface.py is unavailable at the measured revision')
            self.check('C29.c2_real_control_matches_frozen', False, reason)
            self.check('C30.c2_oracle_real_control_agrees', False, reason)
        c2_summary['real_control'] = c2_real_result
        summary['c2'] = c2_summary

        # 13. summary ------------------------------------------------------------
        original_26 = [c for c in self.checks if c['id'] in ORIGINAL_26_CHECKS]
        supplementary_checks = [c for c in self.checks if c['id'] in SUPPLEMENTARY_CHECKS]
        real_controls = [c for c in self.checks if c['id'] in REAL_CONTROL_CHECKS]
        other = [c for c in self.checks
                 if c['id'] not in ORIGINAL_26_CHECKS and c['id'] not in SUPPLEMENTARY_CHECKS
                 and c['id'] not in REAL_CONTROL_CHECKS]
        original_pass = all(c['pass'] for c in original_26)
        supplementary_pass = all(c['pass'] for c in supplementary_checks)
        real_control_pass = all(c['pass'] for c in real_controls)
        other_pass = all(c['pass'] for c in other)

        summary['denominators'] = {'c1_original_requirements': C1_REQUIREMENT_COUNT,
                                   'c2_sealed_cases': len(case_files),
                                   'c1_supplementary_guards': len(supplementary_checks)}
        summary['before'] = {'c1_original_26': c1_before_counts, 'c2': c2_before_counts}
        summary['after'] = {'c1_original_26': c1_after_counts, 'c2': c2_after_counts}
        summary['c1_original_26'] = {
            'denominator': C1_REQUIREMENT_COUNT,
            'before': c1_before_counts,
            'after': c1_after_counts,
            'unmet_before': before_unmet,
            'unmet_after': after_unmet,
            'misleading_alias_runs': {'before': before_alias, 'after': after_alias},
            'oracle': {'before_exit': c1_before.returncode, 'after_exit': c1_after.returncode},
            'pass': bool(original_pass),
        }
        summary['c1_supplementary'] = {
            'guards': supplementary,
            'pass': bool(supplementary_pass),
            'note': 'supplementary guards are reported apart from the original 26 denominator',
        }
        summary['checks'] = self.checks
        summary['observations'] = self.observations
        summary['all_claim_checks_pass'] = bool(original_pass and supplementary_pass
                                                and real_control_pass and other_pass)
        summary['all_claim_checks_pass_excluding_real_controls'] = bool(original_pass
                                                                        and supplementary_pass
                                                                        and other_pass)
        summary['real_controls_pass'] = bool(real_control_pass)
        summary['privacy_clearance'] = False
        summary['carried_open_debt'] = {
            'unallowlisted_retention_hits': 4,
            'original_permission_control': 'RED 11/12 retained byte-unchanged, not rerun',
            'historical_dispositions': 'two unknown',
            'baseline_acceptance': 'blocked',
            'privacy_clearance': False,
        }
        summary['scope_notes'] = {
            'r22_reproduction': "not attempted: the amendment states the r22 driver runs its "
                                "checkout's tool, so the r22 claim is reproducible only in a "
                                "checkout of da40bb20f81da125d798f73cd1653655be1255ca; the r23 "
                                "oracle re-expresses the predicates and no historical r22 mutant "
                                "battery is adapted here",
            'r22_dependencies': 'pinned by digest only (fixture builder and r22 requirements)',
            'source_evidence_kind': 'exact source-byte transform of the baseline git blob, not a '
                                    'behavioural equivalence proof',
        }
        (self.output / 'summary.json').write_text(dumps(summary))
        print(json.dumps({
            'measured_revision': self.revision,
            'seal_revision': self.seal,
            'before': summary['before'],
            'after': summary['after'],
            'all_claim_checks_pass': summary['all_claim_checks_pass'],
        }, sort_keys=True))
        return 0 if summary['all_claim_checks_pass'] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--seal', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        print(json.dumps({'finding_id': 'OUTPUT_DIR_PRESENT', 'output': str(output)}, sort_keys=True))
        return 2
    return Driver(args.revision, args.seal, output).run()


if __name__ == '__main__':
    raise SystemExit(main())
