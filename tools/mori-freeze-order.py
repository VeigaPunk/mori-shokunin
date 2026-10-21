#!/usr/bin/env python3
"""Check whether frozen claim inputs predate their implementation commits."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

SCHEMA = "mori-freeze-order-v1"
REGISTER_SCHEMA = "mori-freeze-register-v1"
GIT_TIMEOUT = 60
_ENV_ALLOWLIST = ("PATH", "LANG", "LC_ALL", "LC_CTYPE", "TZ")
_REV_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/@{}~^+-]*\Z")


class InputError(Exception):
    pass


class GitError(Exception):
    pass


def _git_env():
    env = {name: os.environ[name] for name in _ENV_ALLOWLIST
           if name in os.environ}
    env.update({
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
    })
    return env


def _git(repo, *args):
    argv = [
        "git", "--no-optional-locks", "-c", "core.fsmonitor=false",
        "-C", str(repo), *args,
    ]
    try:
        proc = subprocess.run(
            argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=_git_env(), timeout=GIT_TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitError(type(exc).__name__) from None
    return proc


def _valid_revision(rev):
    return (isinstance(rev, str) and bool(_REV_RE.fullmatch(rev))
            and ".." not in rev and "@{" not in rev)


def _resolve_commit(repo, rev):
    if not _valid_revision(rev):
        return None
    proc = _git(repo, "rev-parse", "--verify", "--quiet",
                "--end-of-options", rev + "^{commit}")
    if proc.returncode != 0:
        return None
    try:
        oid = proc.stdout.decode("ascii").strip()
    except UnicodeError:
        raise GitError("invalid-resolved-revision") from None
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", oid):
        raise GitError("invalid-resolved-revision")
    return oid


def _repository_root(repo):
    proc = _git(repo, "rev-parse", "--show-toplevel")
    if proc.returncode != 0:
        raise GitError("repository-root-failed")
    try:
        root = Path(os.fsdecode(proc.stdout.rstrip(b"\n"))).resolve(strict=True)
    except (OSError, RuntimeError):
        raise GitError("repository-root-failed") from None
    return root


def _path_exists(repo, rev, path):
    proc = _git(repo, "cat-file", "-e", rev + ":" + path)
    return proc.returncode == 0


def _changed_paths(repo, commit):
    # -m plus --first-parent makes a merge's change set its first-parent diff.
    proc = _git(
        repo, "diff-tree", "--no-commit-id", "--name-only", "-r",
        "-m", "--first-parent", "-z", commit,
    )
    if proc.returncode != 0:
        raise GitError("diff-tree-failed")
    return {os.fsdecode(item) for item in proc.stdout.split(b"\0") if item}


def _commits_between(repo, base, tip):
    proc = _git(repo, "rev-list", "--reverse", "--topo-order",
                base + ".." + tip)
    if proc.returncode != 0:
        raise GitError("rev-list-failed")
    return [line.decode("ascii") for line in proc.stdout.splitlines() if line]


def _strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate-key")
        result[key] = value
    return result


def _reject_constant(_value):
    raise ValueError("invalid-number")


def _read_json(path, label, repo=None, revision=None, repo_root=None):
    input_path = Path(path)
    relative_path = None
    if revision is not None:
        try:
            resolved_path = input_path.resolve(strict=True)
            relative_path = resolved_path.relative_to(repo_root).as_posix()
            if not relative_path or not resolved_path.is_file():
                raise ValueError("not-a-repository-file")
            input_path = resolved_path
        except (OSError, RuntimeError, ValueError):
            raise InputError("input-revision-mismatch") from None
    try:
        raw = input_path.read_bytes()
    except OSError:
        error = ("input-revision-mismatch" if revision is not None
                 else "unreadable-" + label)
        raise InputError(error) from None
    digest = hashlib.sha256(raw).hexdigest()
    if revision is not None:
        try:
            proc = _git(repo, "show", revision + ":" + relative_path)
        except GitError:
            raise InputError("input-revision-mismatch") from None
        if (proc.returncode != 0
                or hashlib.sha256(proc.stdout).hexdigest() != digest):
            raise InputError("input-revision-mismatch")
    try:
        data = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError, ValueError):
        raise InputError("unreadable-" + label) from None
    return data, digest


def _valid_path(value):
    if not isinstance(value, str) or not value or "\0" in value:
        return False
    if value.startswith("/") or any(part == ".." for part in value.split("/")):
        return False
    return value != "."


def _load_register(path, repo=None, revision=None, repo_root=None):
    data, digest = _read_json(path, "register", repo, revision, repo_root)
    if (not isinstance(data, dict) or data.get("schema") != REGISTER_SCHEMA
            or not isinstance(data.get("claims"), list)):
        raise InputError("invalid-register")
    seen = set()
    claims = []
    for row in data["claims"]:
        if not isinstance(row, dict):
            raise InputError("invalid-register")
        ident = row.get("id")
        base = row.get("base")
        tip = row.get("tip")
        frozen = row.get("frozen")
        impl = row.get("impl")
        declared = row.get("declared")
        ruling = row.get("outside_ruling")
        if (not isinstance(ident, str) or not ident or ident in seen
                or not isinstance(base, str) or not isinstance(tip, str)
                or not isinstance(frozen, list) or not frozen
                or not all(_valid_path(path) for path in frozen)
                or not isinstance(impl, list)
                or not all(_valid_path(path) for path in impl)
                or not isinstance(declared, str)
                or (ruling is not None and not isinstance(ruling, str))):
            raise InputError("invalid-register")
        if not _valid_revision(base):
            raise InputError("invalid-register")
        seen.add(ident)
        claims.append(row)
    return claims, digest


def _load_corrections(path, claim_ids, repo=None, revision=None,
                      repo_root=None):
    if path is None:
        return {}, None
    data, digest = _read_json(
        path, "corrections", repo, revision, repo_root,
    )
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = None
        for key in ("corrections", "rows", "claims"):
            if key in data:
                rows = data[key]
                break
        if not isinstance(rows, list):
            raise InputError("invalid-corrections")
    else:
        raise InputError("invalid-corrections")

    labels = {}
    for row in rows:
        if not isinstance(row, dict):
            raise InputError("invalid-corrections")
        ident = row.get("id", row.get("claim_id"))
        label = row.get("label", row.get("effective_label", row.get("declared")))
        if (not isinstance(ident, str) or ident not in claim_ids
                or not isinstance(label, str)):
            raise InputError("invalid-corrections")
        labels[ident] = label
    return labels, digest


def _tip_overrides(items, claim_ids):
    overrides = {}
    for item in items:
        if "=" not in item:
            raise InputError("invalid-tip-for")
        ident, rev = item.split("=", 1)
        if (not ident or ident not in claim_ids or ident in overrides
                or not _valid_revision(rev)):
            raise InputError("invalid-tip-for")
        overrides[ident] = rev
    return overrides


def _row_result(repo, claim, tip_override, effective_label):
    ident = claim["id"]

[Showing lines 1-250 of 707. Use :251 to continue]    tip = tip_override if tip_override is not None else claim["tip"]
    result = {
        "id": ident,
        "verdict": "could-not-evaluate",
        "co_committed": None,
        "effective_label": effective_label,
        "overclaim": None,
        "oracle_disagreement": None,
        "base_revision": None,
        "tip_revision": None,
    }

    if tip_override is None and tip.startswith("<") and tip.endswith(">"):
        result["reason"] = "placeholder-tip-requires-override"
        return result
    try:
        base_revision = _resolve_commit(repo, claim["base"])
        if base_revision is None:
            result["reason"] = "unknown-base-revision"
            return result
        result["base_revision"] = base_revision
        tip_revision = _resolve_commit(repo, tip)
        if tip_revision is None:
            result["reason"] = "unknown-tip-revision"
            return result
        result["tip_revision"] = tip_revision

        commits = _commits_between(repo, base_revision, tip_revision)
        frozen = set(claim["frozen"])
        impl = set(claim["impl"])
        first_impl = None
        last_frozen = None
        co_committed = False
        for index, commit in enumerate(commits):
            touched = _changed_paths(repo, commit)
            hit_frozen = not frozen.isdisjoint(touched)
            hit_impl = not impl.isdisjoint(touched)
            if hit_impl and first_impl is None:
                first_impl = index
            if hit_frozen:
                last_frozen = index
            if hit_frozen and hit_impl:
                co_committed = True

        if any(not _path_exists(repo, tip_revision, path)
               for path in claim["frozen"]):
            verdict = "absent"
        elif first_impl is None:
            verdict = "no-implementation"
        elif last_frozen is None:
            at_base = all(_path_exists(repo, base_revision, path)
                          for path in claim["frozen"])
            verdict = "pre-build" if at_base else "co-evolved"
        else:
            verdict = "pre-build" if last_frozen < first_impl else "co-evolved"
    except GitError as exc:
        result["reason"] = str(exc)
        return result

    ruling = claim.get("outside_ruling")
    result.update({
        "verdict": verdict,
        "co_committed": co_committed,
        # Frozen label_rule: any verdict other than pre-build falsifies a
        # pre-build label, including no-implementation (nothing ordered yet).
        "overclaim": effective_label == "pre-build" and verdict != "pre-build",
        "oracle_disagreement": ruling is not None and verdict != ruling,
    })
    return result


def _evaluate(repo, claims, corrections, overrides, provenance):
    results = []
    for claim in claims:
        label = corrections.get(claim["id"], claim["declared"])
        results.append(_row_result(
            repo, claim, overrides.get(claim["id"]), label,
        ))
    totals = {
        "claims": len(results),
        "overclaims": sum(row["overclaim"] is True for row in results),
        "oracle_disagreements": sum(
            row["oracle_disagreement"] is True for row in results),
        "could_not_evaluate": sum(
            row["verdict"] == "could-not-evaluate" for row in results),
    }
    return {
        "schema": SCHEMA,
        "claims": results,
        "totals": totals,
        "provenance": provenance,
    }


def _emit(data):
    print(json.dumps(data, sort_keys=True, separators=(",", ":")))


def _error_result(error):
    return {
        "schema": SCHEMA,
        "error": error,
        "claims": [],
        "totals": {
            "claims": 0, "overclaims": 0, "oracle_disagreements": 0,
            "could_not_evaluate": 0,
        },
    }


def _check(args):
    try:
        measured_revision = None
        repo_root = None
        if args.rev is not None:
            measured_revision = _resolve_commit(args.repo, args.rev)
            if measured_revision is None:
                _emit(_error_result("unknown-measured-revision"))
                return 2
            try:
                repo_root = _repository_root(args.repo)
            except GitError:
                _emit(_error_result("input-revision-mismatch"))
                return 2
        claims, register_sha256 = _load_register(
            args.register, args.repo, measured_revision, repo_root,
        )
        ids = {claim["id"] for claim in claims}
        corrections, corrections_sha256 = _load_corrections(
            args.corrections, ids, args.repo, measured_revision, repo_root,
        )
        overrides = _tip_overrides(args.tip_for, ids)
        script_sha256 = hashlib.sha256(
            Path(__file__).resolve().read_bytes()
        ).hexdigest()
    except InputError as exc:
        _emit(_error_result(str(exc)))
        return 2
    except GitError:
        _emit(_error_result("revision-resolution-failed"))
        return 2
    except OSError:
        _emit(_error_result("unreadable-script"))
        return 2

    provenance = {
        "status": "bound" if measured_revision is not None else "unbound",
        "measured_revision": measured_revision,
        "register_sha256": register_sha256,
        "corrections_sha256": corrections_sha256,
        "script_sha256": script_sha256,
        "command_argv": args.command_argv,
        "tip_overrides": list(args.tip_for),
    }
    data = _evaluate(args.repo, claims, corrections, overrides, provenance)
    _emit(data)
    totals = data["totals"]
    if totals["could_not_evaluate"]:
        return 2
    if totals["overclaims"] or totals["oracle_disagreements"]:
        return 1
    return 0


# Selftest support: all fixture repositories and commits live below TMPDIR.
def _fixture_git(repo, *args):
    env = _git_env()
    env.update({
        "GIT_AUTHOR_NAME": "FreezeOrder selftest",
        "GIT_AUTHOR_EMAIL": "freeze-order-selftest@example.invalid",
        "GIT_COMMITTER_NAME": "FreezeOrder selftest",
        "GIT_COMMITTER_EMAIL": "freeze-order-selftest@example.invalid",
    })
    argv = ["git", "--no-optional-locks", "-c", "core.fsmonitor=false",
            "-C", str(repo), *args]
    proc = subprocess.run(
        argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, env=env, timeout=GIT_TIMEOUT,
    )
    if proc.returncode != 0:
        raise RuntimeError("fixture-git-failed")
    return proc.stdout.decode("ascii", errors="strict").strip()


def _new_repo(root, name):
    repo = root / name
    repo.mkdir()
    _fixture_git(repo, "init", "-q")
    _fixture_git(repo, "checkout", "-q", "-b", "main")
    return repo


def _commit(repo, files, message):
    for relative, content in files.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    _fixture_git(repo, "add", "-A")
    _fixture_git(repo, "commit", "-q", "-m", message)
    return _fixture_git(repo, "rev-parse", "HEAD")


def _write_register(root, name, base, tip, frozen, impl,
                    declared="unlabeled", ruling=None):
    path = root / (name + ".register.json")
    row = {
        "id": name,
        "base": base,
        "tip": tip,
        "frozen": frozen,
        "impl": impl,
        "declared": declared,
        "outside_ruling": ruling,
        "ruling_at": None,
    }
    path.write_text(json.dumps({"schema": REGISTER_SCHEMA, "claims": [row]}),
                    encoding="utf-8")
    return path


def _invoke_case(repo, register, expected_rc, expected_verdict,
                 extra=(), expected_fields=None):
    argv = [
        sys.executable, str(Path(__file__).resolve()), "check",
        "--repo", str(repo), "--register", str(register), *extra,
    ]
    proc = subprocess.run(
        argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=GIT_TIMEOUT * 2,
    )
    if proc.returncode != expected_rc:
        raise AssertionError("unexpected-exit")
    try:
        data = json.loads(proc.stdout.decode("utf-8"))
        row = data["claims"][0]
    except (UnicodeError, ValueError, KeyError, IndexError, TypeError):
        raise AssertionError("invalid-json-output") from None
    if row.get("verdict") != expected_verdict:
        raise AssertionError("unexpected-verdict")
    for key, value in (expected_fields or {}).items():
        if row.get(key) != value:
            raise AssertionError("unexpected-" + key)
    return data


def _selftest():
    raw_tmp = os.environ.get("TMPDIR")
    if not raw_tmp:
        print("SELFTEST freeze-order FAIL 0/11", file=sys.stderr)
        return 1

[Showing lines 251-500 of 707. Use :501 to continue]    scratch = Path(raw_tmp).resolve()
    forbidden = (Path("/tmp"), Path("/var/tmp"))
    if (not scratch.is_absolute()
            or any(scratch == path or path in scratch.parents
                   for path in forbidden)):
        print("SELFTEST freeze-order FAIL 0/11", file=sys.stderr)
        return 1
    checkout = Path(__file__).resolve().parents[1]
    try:
        scratch.relative_to(checkout)
    except ValueError:
        print("SELFTEST freeze-order FAIL 0/11", file=sys.stderr)
        return 1

    passed = 0
    try:
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="mori-freeze-order-",
                                         dir=str(scratch)) as temp:
            root = Path(temp)

            # 1. Frozen input committed before implementation.
            repo = _new_repo(root, "frozen-then-impl")
            base = _commit(repo, {"base.txt": "base\n"}, "base")
            _commit(repo, {"frozen.txt": "frozen\n"}, "freeze")
            tip = _commit(repo, {"tools/impl.py": "impl\n"}, "implementation")
            register = _write_register(root, "frozen-then-impl", base, tip,
                                       ["frozen.txt"], ["tools/impl.py"],
                                       declared="pre-build")
            _invoke_case(repo, register, 0, "pre-build")
            passed += 1

            # 2. Frozen and implementation paths touched in the same commit.
            repo = _new_repo(root, "co-committed")
            base = _commit(repo, {"base.txt": "base\n"}, "base")
            tip = _commit(repo, {"frozen.txt": "frozen\n",
                                 "tools/impl.py": "impl\n"}, "together")
            register = _write_register(root, "co-committed", base, tip,
                                       ["frozen.txt"], ["tools/impl.py"],
                                       declared="pre-build")
            _invoke_case(repo, register, 1, "co-evolved",
                         expected_fields={"co_committed": True,
                                          "overclaim": True})
            passed += 1

            # 3. A frozen edit after the first implementation commit.
            repo = _new_repo(root, "frozen-after-impl")
            base = _commit(repo, {"frozen.txt": "initial\n",
                                  "base.txt": "base\n"}, "base")
            _commit(repo, {"tools/impl.py": "impl\n"}, "implementation")
            tip = _commit(repo, {"frozen.txt": "edited\n"}, "edit frozen")
            register = _write_register(root, "frozen-after-impl", base, tip,
                                       ["frozen.txt"], ["tools/impl.py"])
            _invoke_case(repo, register, 0, "co-evolved")
            passed += 1

            # 4. Frozen input already exists at the base revision.
            repo = _new_repo(root, "frozen-at-base")
            base = _commit(repo, {"frozen.txt": "frozen\n",
                                  "base.txt": "base\n"}, "base")
            tip = _commit(repo, {"tools/impl.py": "impl\n"}, "implementation")
            register = _write_register(root, "frozen-at-base", base, tip,
                                       ["frozen.txt"], ["tools/impl.py"])
            _invoke_case(repo, register, 0, "pre-build")
            passed += 1

            # 5. A frozen input missing at tip is absent.
            repo = _new_repo(root, "missing-frozen")
            base = _commit(repo, {"base.txt": "base\n"}, "base")
            tip = _commit(repo, {"tools/impl.py": "impl\n"}, "implementation")
            register = _write_register(root, "missing-frozen", base, tip,
                                       ["frozen.txt"], ["tools/impl.py"])
            _invoke_case(repo, register, 0, "absent")
            passed += 1

            # 6. No implementation commit appears in the range: a pre-build
            #    label is not yet supported, so it is an overclaim (exit 1).
            repo = _new_repo(root, "no-implementation")
            base = _commit(repo, {"frozen.txt": "frozen\n"}, "base")
            register = _write_register(
                root, "no-implementation", base, base, ["frozen.txt"],
                ["tools/impl.py"], declared="pre-build",
            )
            _invoke_case(
                repo, register, 1, "no-implementation",
                expected_fields={"effective_label": "pre-build",
                                 "overclaim": True},
            )
            passed += 1

            # 7. An appended correction replaces the declared effective label.
            repo = _new_repo(root, "correction-flips-label")
            base = _commit(repo, {"base.txt": "base\n"}, "base")
            tip = _commit(repo, {"frozen.txt": "frozen\n",
                                 "tools/impl.py": "impl\n"}, "together")
            register = _write_register(root, "correction-flips-label", base,
                                       tip, ["frozen.txt"], ["tools/impl.py"],
                                       declared="pre-build")
            corrections = root / "correction.json"
            corrections.write_text(json.dumps({"corrections": [{
                "id": "correction-flips-label", "label": "co-evolved",
            }]}), encoding="utf-8")
            _invoke_case(repo, register, 0, "co-evolved",
                         extra=("--corrections", str(corrections)),
                         expected_fields={"effective_label": "co-evolved",
                                          "overclaim": False})
            passed += 1

            # 8. A disagreement with an outside ruling is surfaced.
            repo = _new_repo(root, "oracle-disagreement")
            base = _commit(repo, {"base.txt": "base\n"}, "base")
            _commit(repo, {"frozen.txt": "frozen\n"}, "freeze")
            tip = _commit(repo, {"tools/impl.py": "impl\n"}, "implementation")
            register = _write_register(root, "oracle-disagreement", base, tip,
                                       ["frozen.txt"], ["tools/impl.py"],
                                       ruling="co-evolved")
            _invoke_case(repo, register, 1, "pre-build",
                         expected_fields={"oracle_disagreement": True})
            passed += 1

            # 8b. Round-18 wave-2 MutFreezeOrder M07: the oracle comparison is
            #     exact; a differently cased ruling is still a disagreement.
            register = _write_register(root, "oracle-exact-case", base, tip,
                                       ["frozen.txt"], ["tools/impl.py"],
                                       ruling="PRE-BUILD")
            _invoke_case(repo, register, 1, "pre-build",
                         expected_fields={"oracle_disagreement": True})
            passed += 1

            # 9. An unknown revision is a could-not-evaluate result (exit 2).
            repo = _new_repo(root, "unknown-revision")
            base = _commit(repo, {"frozen.txt": "frozen\n"}, "base")
            register = _write_register(root, "unknown-revision", base, base,
                                       ["frozen.txt"], ["tools/impl.py"])
            _invoke_case(repo, register, 2, "could-not-evaluate",
                         extra=("--tip-for", "unknown-revision=missing-revision"))
            passed += 1

            # 10. Merge first-parent diff contributes the final frozen edit.
            repo = _new_repo(root, "merge-first-parent")
            base = _commit(repo, {"base.txt": "base\n"}, "base")
            frozen_base = _commit(repo, {"frozen.txt": "initial\n"}, "freeze")
            _fixture_git(repo, "checkout", "-q", "-b", "side", frozen_base)
            _commit(repo, {"frozen.txt": "side edit\n"}, "side frozen edit")
            side_tip = _fixture_git(repo, "rev-parse", "HEAD")
            _fixture_git(repo, "checkout", "-q", "main")
            _commit(repo, {"tools/impl.py": "impl\n"}, "implementation")
            _fixture_git(repo, "merge", "--no-ff", "-q", "-m", "merge frozen edit",
                         side_tip)
            tip = _fixture_git(repo, "rev-parse", "HEAD")
            register = _write_register(root, "merge-first-parent", base, tip,
                                       ["frozen.txt"], ["tools/impl.py"])
            _invoke_case(repo, register, 0, "co-evolved")
            passed += 1

            # 11. A placeholder tip without a row-specific override is unknown.
            repo = _new_repo(root, "placeholder-tip")
            base = _commit(repo, {"frozen.txt": "frozen\n"}, "base")
            register = _write_register(root, "placeholder-tip", base,
                                       "<measured round-18 commit>",
                                       ["frozen.txt"], ["tools/impl.py"])
            _invoke_case(repo, register, 2, "could-not-evaluate")
            passed += 1
    except Exception:
        print("SELFTEST freeze-order FAIL %d/12" % passed, file=sys.stderr)
        return 1

    if passed != 12:
        print("SELFTEST freeze-order FAIL %d/12" % passed, file=sys.stderr)
        return 1
    print("SELFTEST freeze-order PASS %d/12" % passed)
    return 0


def _parser():
    parser = argparse.ArgumentParser(
        prog="mori-freeze-order.py",
        description="measure frozen-input timing against implementation history",
    )
    parser.add_argument("--selftest", action="store_true",
                        help="run isolated Git-fixture arms under TMPDIR")
    sub = parser.add_subparsers(dest="command")
    check = sub.add_parser("check", help="evaluate the frozen claim register")
    check.add_argument("--repo", required=True, metavar="R")
    check.add_argument("--register", required=True, metavar="F")
    check.add_argument("--rev", metavar="REV")
    check.add_argument("--corrections", metavar="C")
    check.add_argument("--tip-for", action="append", default=[], metavar="ID=REV")
    return parser


def main(argv=None):
    command_argv = [sys.argv[0], *(sys.argv[1:] if argv is None else argv)]
    parser = _parser()
    args = parser.parse_args(argv)
    args.command_argv = command_argv
    if args.selftest:
        if args.command is not None:
            parser.error("--selftest takes no check arguments")
        return _selftest()
    if args.command != "check":
        parser.error("select check or --selftest")
    return _check(args)


if __name__ == "__main__":
    sys.exit(main())