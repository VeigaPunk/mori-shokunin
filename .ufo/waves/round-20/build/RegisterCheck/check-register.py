#!/usr/bin/env python3
"""Check drift tokens against a typed mori drift-classification register."""

import argparse
import json
import sys
from pathlib import Path

SCHEMA = "mori-drift-classification-v1"
CLASSES = frozenset(
    {
        "census-schema-change",
        "roster-change",
        "live-state",
        "census-regression",
    }
)


class InputError(Exception):
    """An input file cannot be read in a supported form."""


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise InputError(f"cannot read {path}: {error}") from error


def drift_tokens(text):
    stripped = text.lstrip()
    if stripped.startswith("{"):
        try:
            capture = json.loads(text)
        except json.JSONDecodeError as error:
            raise InputError(f"invalid JSON drift capture: {error}") from error
        if not isinstance(capture, dict) or not isinstance(capture.get("stdout"), str):
            raise InputError("JSON drift capture must contain a string stdout field")
        text = capture["stdout"]
    return {word for word in text.split() if word != "MORI_DRIFT:"}


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def inspect_register(text):
    try:
        register = json.loads(text)
    except json.JSONDecodeError:
        return {}, 1, {}

    if not isinstance(register, dict):
        return {}, 1, {}

    invalid = 0
    schema_ok = register.get("schema") == SCHEMA
    if not schema_ok:
        invalid += 1

    entries = register.get("tokens")
    if not isinstance(entries, dict):
        return {}, invalid + 1, {}

    valid_entries = {}
    regression_entries = {}
    for token, entry in entries.items():
        class_name = entry.get("class") if isinstance(entry, dict) else None
        if (
            isinstance(token, str)
            and token.strip()
            and isinstance(entry, dict)
            and isinstance(class_name, str)
            and class_name in CLASSES
            and nonempty_string(entry.get("reason"))
            and nonempty_string(entry.get("evidence"))
        ):
            if schema_ok:
                valid_entries[token] = entry
            if class_name == "census-regression":
                regression_entries[token] = entry
        else:
            invalid += 1
            if class_name == "census-regression":
                regression_entries[token] = entry
    return valid_entries, invalid, regression_entries


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "validate drift classifications; DRIFT may be raw MORI_DRIFT stdout "
            "or a JSON capture containing a string stdout field"
        )
    )
    parser.add_argument("register", help="drift-classification JSON register")
    parser.add_argument("drift_stdout", help="captured drift stdout file")
    args = parser.parse_args(argv)

    try:
        register_text = read_text(args.register)
        stdout_text = read_text(args.drift_stdout)
        tokens = drift_tokens(stdout_text)
    except InputError as error:
        print(f"check-register.py: {error}", file=sys.stderr)
        return 2

    valid_entries, invalid, regression_entries = inspect_register(register_text)
    unclassified = sum(token not in valid_entries for token in tokens)
    regression = sum(
        token in regression_entries for token in tokens
    )
    print(
        "MORI_DRIFT_REGISTER: "
        f"unclassified={unclassified} invalid={invalid} "
        f"regression={regression} tokens={len(tokens)}"
    )
    return 0 if unclassified == invalid == regression == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
