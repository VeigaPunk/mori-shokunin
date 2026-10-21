#!/usr/bin/env python3
"""Round-23 measurement driver (MeasureDriver seat).

Read-only over the lane repository. The driver stages both round-23 tools from
the measured revision and from the entering revision with `git show`, runs the
frozen C1 oracle and the sealed C2 oracle before and after, runs the two frozen
real controls, asserts that the seal commit is an ancestor of the measured
revision and that every frozen artefact is byte-identical between the seal and
the measured revision, then writes summary.json.

    measure-round23.py --revision REV --seal SEAL_REV --output ABSENT_DIR

The output directory must not exist. Exit code is 0 iff all_claim_checks_pass.
Every oracle, case file and tool that takes part in a measurement is staged from
the measured revision, so the measurement never depends on the working tree.

No privileged, mutating or host-remediating command is issued. The only host
reads are the ones the C2 real control needs (mountinfo, os.stat, realpath,
readlink of /dev/mapper/*, directory listings under /sys/fs/btrfs).
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

RETENTION_REL = 'tools/mori-retention-reconcile.py'
QUOTA_REL = 'tools/mori-quota-surface.py'

FROZEN_PREFIX = WAVE_REL + '/frozen'
RENAME_ORACLE_REL = WAVE_REL + '/oracle-rename.py'
QUOTA_ORACLE_REL = WAVE_REL + '/oracle-quota.py'
CONTRACT_REL = WAVE_REL + '/contract.md'

R22_BUILDER_REL = '.ufo/waves/round-22/frozen/fixture-builder-v2.py'
R22_REQUIREMENTS_REL = '.ufo/waves/round-22/frozen/requirements-v2.json'

C1_REQUIREMENTS_REL = FROZEN_PREFIX + '/c1-requirements.json'
C1_REAL_REL = FROZEN_PREFIX + '/c1-expected-real.json'
C2_REAL_REL = FROZEN_PREFIX + '/c2-expected-real.json'
QUOTA_CASES_REL = FROZEN_PREFIX + '/quota-cases'

SCHEMA_V2 = 'mori-retention-reconciliation-v2'
ALIAS_KEY = 'raw_unallowlisted'

C1_REQUIREMENT_COUNT = 26
C1_BEFORE_UNMET = ['R25']

REAL_CONTROL_CHECKS = ('C13.c1_real_control_matches_frozen',
                       'C17.c2_real_control_matches_frozen',
                       'C18.c2_oracle_real_control_agrees')

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


class Driver:
    def __init__(self, revision: str, seal: str, output: Path):
        self.revision = revision
        self.seal = seal
        self.output = output
        self.checks = []
        self.observations = []
        self.scratch = LANE / '.scratch' / 'round23' / ('measure-' + output.name)
        self.env = dict(os.environ)
        self.env['TMPDIR'] = str(LANE / '.scratch')
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
               'measured_revision': self.revision, 'argv': [str(x) for x in argv],
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
        if self.scratch.exists():
            # Only this driver's own scratch space is ever removed; the fresh
            # fixture roots below must not exist before the oracles create them.
            shutil.rmtree(self.scratch)
        self.scratch.mkdir(parents=True, exist_ok=False)
        staged = self.scratch / 'staged'
        wave_tree = self.scratch / 'wave-tree'
        wave_tree.mkdir(parents=True, exist_ok=True)

        summary = {
            'schema': 'mori-r23-measurements-v1',
            'measured_revision': self.revision,
            'seal_revision': self.seal,
            'entering_revision': ENTERING,
            'lane': str(LANE),
            'driver_sha256': sha(Path(__file__).read_bytes()),
            'recorded_utc': datetime.now(timezone.utc).isoformat(),
        }

        # 1. revision resolution and seal ancestry --------------------------------
        rev_cp = git_bytes(['rev-parse', '--verify', '--quiet', self.revision + '^{commit}'])
        seal_cp = git_bytes(['rev-parse', '--verify', '--quiet', self.seal + '^{commit}'])
        resolved_revision = rev_cp.stdout.decode('ascii', 'replace').strip()
        resolved_seal = seal_cp.stdout.decode('ascii', 'replace').strip()
        ancestry = git_bytes(['merge-base', '--is-ancestor', self.seal, self.revision])
        ancestry_ok = ancestry.returncode == 0
        self.check('C00.revisions_resolve',
                   rev_cp.returncode == 0 and seal_cp.returncode == 0,
                   'the measured revision and the seal revision must both resolve to commits',
                   measured_revision_resolved=resolved_revision, seal_revision_resolved=resolved_seal)
        self.check('C01.seal_is_ancestor_of_revision', ancestry_ok,
                   'git merge-base --is-ancestor <seal> <revision> must exit 0',
                   argv=['git', '-C', str(LANE), 'merge-base', '--is-ancestor', self.seal, self.revision],
                   returncode=ancestry.returncode)
        summary['ancestry'] = {
            'seal_is_ancestor_of_revision': ancestry_ok,
            'argv': ['git', '-C', str(LANE), 'merge-base', '--is-ancestor', self.seal, self.revision],
            'returncode': ancestry.returncode,
            'seal_revision_resolved': resolved_seal,
            'measured_revision_resolved': resolved_revision,
        }

        # 2. frozen artefacts byte-identical between seal and revision ------------
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
        self.check('C02.frozen_byte_identical_seal_to_revision', frozen_identical,
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
        self.check('C03.sealed_oracles_byte_identical', oracles_identical,
                   'the sealed oracles must be byte-identical between the seal and the revision',
                   divergent=[p for p, r in oracle_rows.items() if not r['byte_identical']])

        contract_seal = git_show(self.seal, CONTRACT_REL)
        contract_rev = git_show(self.revision, CONTRACT_REL)
        contract_same = contract_seal is not None and contract_rev is not None and contract_seal == contract_rev
        self.check('C04.contract_unchanged_since_seal', contract_same,
                   'the pre-registered contract must be unchanged between the seal and the revision')

        summary['sealed_artifacts'] = {'frozen': frozen_rows, 'oracles': oracle_rows,
                                       'contract_byte_identical': contract_same}

        # 3. stage the wave tree (oracles, frozen files, r22 builder) -------------
        for rel in (RENAME_ORACLE_REL, QUOTA_ORACLE_REL, R22_BUILDER_REL, R22_REQUIREMENTS_REL):
            self.stage_bytes(rel, self.revision, wave_tree / rel)
        for path in (frozen_rev or {}):
            self.stage_bytes(path, self.revision, wave_tree / path)
        rename_oracle = wave_tree / RENAME_ORACLE_REL
        quota_oracle = wave_tree / QUOTA_ORACLE_REL
        staged_cases = wave_tree / QUOTA_CASES_REL
        staged_requirements = wave_tree / C1_REQUIREMENTS_REL
        staged_c1_real = wave_tree / C1_REAL_REL
        staged_c2_real = wave_tree / C2_REAL_REL

        worktree_rows = {}
        for rel in (RENAME_ORACLE_REL, QUOTA_ORACLE_REL, C1_REQUIREMENTS_REL, C1_REAL_REL, C2_REAL_REL):
            on_disk = LANE / rel
            committed = git_show(self.revision, rel)
            same = on_disk.is_file() and committed is not None and on_disk.read_bytes() == committed
            worktree_rows[rel] = {'worktree_matches_revision': same}
            self.observe('worktree.' + rel,
                         'working-tree copy compared with the measured revision (informational only)',
                         worktree_matches_revision=same)
        for path in sorted((frozen_rev or {})):
            on_disk = LANE / path
            committed = git_show(self.revision, path)
            same = on_disk.is_file() and committed is not None and on_disk.read_bytes() == committed
            worktree_rows[path] = {'worktree_matches_revision': same}
            self.observe('worktree.' + path,
                         'working-tree copy compared with the measured revision (informational only)',
                         worktree_matches_revision=same)
        summary['worktree_comparison'] = worktree_rows

        # 4. requirement bindings ------------------------------------------------
        requirements = self.json_file(staged_requirements)
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
            actual_bytes = git_show(self.revision, rel)
            actual = sha(actual_bytes) if actual_bytes is not None else None
            same = expected is not None and expected == actual
            bindings_ok = bindings_ok and same
            binding_rows[key] = {'path': rel, 'expected': expected, 'observed': actual, 'matches': same}
        self.check('C05.c1_requirement_bindings', bindings_ok,
                   'the frozen c1-requirements digests must match the committed artefacts at the measured revision',
                   bindings=binding_rows)
        summary['requirement_bindings'] = binding_rows

        # 5. stage the tools from both revisions ---------------------------------
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
        self.check('C06.quota_tool_absent_at_entering_revision', not quota_before_present,
                   'tools/mori-quota-surface.py must be absent at the entering revision (capability absent before)',
                   entering_present=quota_before_present)
        self.check('C07.quota_tool_present_at_measured_revision', quota_after_bytes is not None,
                   'tools/mori-quota-surface.py must exist at the measured revision')
        self.check('C08.retention_tool_present_at_both_revisions',
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

        # 6. C1: oracle before and after -----------------------------------------
        c1_dir = self.scratch / 'c1'
        c1_dir.mkdir(parents=True, exist_ok=True)
        c1_before_out = c1_dir / 'before.json'
        c1_after_out = c1_dir / 'after.json'
        self.check('C20.rename_oracle_present_at_measured_revision', rename_oracle.is_file(),
                   'the frozen C1 oracle must exist at the measured revision')
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
                stderr = 'the frozen C1 oracle is unavailable at the measured revision'
            c1_before = c1_after = _Absent()
        before_obs = self.json_file(c1_before_out)
        after_obs = self.json_file(c1_after_out)

        def unmet_ids(obs):
            if not isinstance(obs, dict):
                return []
            return sorted(str(r.get('id')) for r in obs.get('results', []) if not r.get('pass'))

        def alias_runs(obs):
            """Oracle runs whose JSON output still carries the misleading alias key."""
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

        c1_before_counts = (before_obs or {}).get('counts') or {}
        c1_after_counts = (after_obs or {}).get('counts') or {}
        before_unmet = unmet_ids(before_obs)
        after_unmet = unmet_ids(after_obs)
        before_alias = alias_runs(before_obs)
        after_alias = alias_runs(after_obs)

        self.check('C09.c1_before_requirement_counts',
                   before_obs is not None and c1_before_counts.get('total') == C1_REQUIREMENT_COUNT
                   and before_unmet == C1_BEFORE_UNMET,
                   'before the cutover exactly R25 may be unmet',
                   total=c1_before_counts.get('total'), pass_count=c1_before_counts.get('pass'),
                   unmet=before_unmet, oracle_exit=c1_before.returncode)
        self.check('C10.c1_after_requirement_counts',
                   after_obs is not None and c1_after_counts.get('total') == C1_REQUIREMENT_COUNT
                   and not after_unmet and c1_after_counts.get('unmet') == 0,
                   'after the cutover every requirement must pass',
                   total=c1_after_counts.get('total'), pass_count=c1_after_counts.get('pass'),
                   unmet=after_unmet, oracle_exit=c1_after.returncode)
        self.check('C11.c1_alias_removed',
                   before_alias is not None and before_alias > 0 and after_alias == 0,
                   'misleading_alias_runs must be greater than 0 before and 0 after',
                   before=before_alias, after=after_alias,
                   oracle_counter={'before': (before_obs or {}).get('misleading_alias_runs'),
                                   'after': (after_obs or {}).get('misleading_alias_runs')})
        after_schema_ok = ((after_obs or {}).get('schema_v2_runs')
                           == (after_obs or {}).get('parsed_runs'))
        self.check('C12.c1_schema_v2_after',
                   bool(after_schema_ok) and (after_obs or {}).get('parsed_runs', 0) > 0,
                   'every parsed oracle run after the cutover must carry schema ' + SCHEMA_V2,
                   schema_v2_runs=(after_obs or {}).get('schema_v2_runs'),
                   parsed_runs=(after_obs or {}).get('parsed_runs'))
        for name, path in (('c1-before-observed.json', c1_before_out),
                           ('c1-after-observed.json', c1_after_out)):
            if path.exists():
                (self.output / name).write_bytes(path.read_bytes())

        # 7. C1 real control -----------------------------------------------------
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
                               and real.get('tool_sha256') == sha(retention_after_bytes or b''))
            argv_ok = isinstance(real, dict) and real.get('argv') == [str(x) for x in realcmd[2:]]
            exit_ok = cp.returncode == c1_real.get('expected_exit')
            clearance_ok = isinstance(real, dict) and real.get('privacy_clearance') is False
            real_ok = bool(exit_ok and keys_ok and digests_ok and revisions_ok and tool_digest_ok
                           and argv_ok and clearance_ok and not forbidden_present)
            self.check('C13.c1_real_control_matches_frozen', real_ok,
                       'the C1 real control must reproduce the frozen receipt values exactly',
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
            # the identical real command against the entering revision, for the before/after picture
            beforecmd = list(realcmd)
            beforecmd[1] = retention_before
            bcp = self.record('c1-real-control-entering', beforecmd)
            try:
                breal = json.loads(bcp.stdout)
            except (ValueError, TypeError):
                breal = None
            before_alias_present = isinstance(breal, dict) and ALIAS_KEY in breal
            after_alias_absent = isinstance(real, dict) and ALIAS_KEY not in real
            self.check('C14.c1_alias_present_before_absent_after',
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
            reason = ('frozen c1-expected-real.json is unavailable at the measured revision'
                      if c1_real is None else
                      'tools/mori-retention-reconcile.py is unavailable at the measured revision')
            self.check('C13.c1_real_control_matches_frozen', False, reason)
            self.check('C14.c1_alias_present_before_absent_after', False, reason)
        summary['c1_real_control'] = c1_real_result

        # 8. C2: sealed oracle before, after and with the real control -----------
        c2_real = self.json_file(staged_c2_real)
        case_files = sorted(staged_cases.glob('*.json')) if staged_cases.is_dir() else []
        c2_summary = {'cases': [p.name for p in case_files], 'cases_count': len(case_files),
                      'cases_source': 'staged from the measured revision',
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
                # Fall back to the option names the sealed oracle actually exposes.
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
        self.check('C19.c2_oracle_present_at_measured_revision', quota_oracle.is_file(),
                   'the sealed C2 oracle must exist at the measured revision')
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
                stderr = 'the sealed C2 oracle is unavailable at the measured revision'
            c2_before_cp = c2_after_cp = c2_real_cp = _Absent()
            c2_before_obs = c2_after_obs = c2_real_obs = None

        c2_before_counts = (c2_before_obs or {}).get('counts') or {}
        c2_after_counts = (c2_after_obs or {}).get('counts') or {}
        c2_summary['before'] = c2_before_counts
        c2_summary['after'] = c2_after_counts
        c2_summary['after_with_real_expected'] = (c2_real_obs or {}).get('counts') or {}

        self.check('C15.c2_before_capability_absent',
                   bool(c2_before_obs) and bool(case_files)
                   and c2_before_counts.get('capability_absent') == c2_before_counts.get('total')
                   and c2_before_counts.get('total') == len(case_files),
                   'before the cutover every sealed case must be capability_absent',
                   total=c2_before_counts.get('total'),
                   capability_absent=c2_before_counts.get('capability_absent'),
                   cases=len(case_files), oracle_exit=c2_before_cp.returncode)
        self.check('C16.c2_after_every_case_matches',
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

        # 9. C2 real control, measured directly ---------------------------------
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
            self.check('C17.c2_real_control_matches_frozen', real_ok,
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
            self.check('C18.c2_oracle_real_control_agrees',
                       oracle_real_counts.get('unmet') == 0 and oracle_real_counts.get('total', 0) > 0,
                       'the sealed C2 oracle with --real-expected must report no unmet real-control requirement',
                       counts=oracle_real_counts, oracle_exit=c2_real_cp.returncode)
        else:
            reason = ('frozen c2-expected-real.json is unavailable at the measured revision'
                      if c2_real is None else
                      'tools/mori-quota-surface.py is unavailable at the measured revision')
            self.check('C17.c2_real_control_matches_frozen', False, reason)
            self.check('C18.c2_oracle_real_control_agrees', False, reason)
        c2_summary['real_control'] = c2_real_result
        summary['c2'] = c2_summary

        # 10. summary ------------------------------------------------------------
        deterministic = [c for c in self.checks if c['id'] not in REAL_CONTROL_CHECKS]
        deterministic_pass = all(c['pass'] for c in deterministic)
        real_control_pass = all(c['pass'] for c in self.checks if c['id'] in REAL_CONTROL_CHECKS)
        summary['before'] = {'c1': c1_before_counts, 'c2': c2_before_counts}
        summary['after'] = {'c1': c1_after_counts, 'c2': c2_after_counts}
        summary['c1'] = {
            'before': c1_before_counts,
            'after': c1_after_counts,
            'unmet_before': before_unmet,
            'unmet_after': after_unmet,
            'misleading_alias_runs': {'before': before_alias, 'after': after_alias},
            'oracle': {'before_exit': c1_before.returncode, 'after_exit': c1_after.returncode,
                       'requirements_sha256': sha(staged_requirements.read_bytes())
                       if staged_requirements.is_file() else None},
        }
        summary['checks'] = self.checks
        summary['observations'] = self.observations
        summary['all_claim_checks_pass'] = bool(deterministic_pass and real_control_pass)
        summary['all_claim_checks_pass_excluding_real_controls'] = bool(deterministic_pass)
        summary['real_controls_pass'] = bool(real_control_pass)
        summary['privacy_clearance'] = False
        summary['carried_open_debt'] = {
            'unallowlisted_retention_hits': 4,
            'original_permission_control': 'RED 11/12 retained byte-unchanged, not rerun',
            'historical_dispositions': 'two unknown',
            'baseline_acceptance': 'blocked',
            'privacy_clearance': False,
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
