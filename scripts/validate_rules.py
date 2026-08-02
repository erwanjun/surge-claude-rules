#!/usr/bin/env python3

from __future__ import annotations

import ipaddress
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULE_DIR = ROOT / "Surge"
ALLOWED_TYPES = {
    "DOMAIN",
    "DOMAIN-SUFFIX",
    "DOMAIN-KEYWORD",
    "IP-CIDR",
    "IP-CIDR6",
    "IP-ASN",
}
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$"
)
DOMAIN_KEYWORD_RE = re.compile(r"^[a-z0-9._-]+$")


def validate_rule(path: Path, line_number: int, line: str) -> str:
    if line != line.strip():
        raise ValueError(f"{path}:{line_number}: leading or trailing whitespace")

    fields = line.split(",")
    rule_type = fields[0]
    if rule_type not in ALLOWED_TYPES:
        raise ValueError(f"{path}:{line_number}: unsupported rule type {rule_type!r}")

    if rule_type in {"DOMAIN", "DOMAIN-SUFFIX"}:
        if len(fields) != 2 or not DOMAIN_RE.fullmatch(fields[1]):
            raise ValueError(f"{path}:{line_number}: invalid domain rule")
    elif rule_type == "DOMAIN-KEYWORD":
        if len(fields) != 2 or not DOMAIN_KEYWORD_RE.fullmatch(fields[1]):
            raise ValueError(f"{path}:{line_number}: invalid domain keyword rule")
    elif rule_type in {"IP-CIDR", "IP-CIDR6"}:
        if len(fields) != 3 or fields[2] != "no-resolve":
            raise ValueError(f"{path}:{line_number}: IP rules must end with no-resolve")
        network = ipaddress.ip_network(fields[1], strict=True)
        expected_version = 4 if rule_type == "IP-CIDR" else 6
        if network.version != expected_version:
            raise ValueError(f"{path}:{line_number}: wrong IP version")
    elif rule_type == "IP-ASN":
        if len(fields) != 3 or fields[2] != "no-resolve" or not fields[1].isdigit():
            raise ValueError(f"{path}:{line_number}: invalid ASN rule")

    return line


def load_rules(path: Path) -> set[str]:
    rules: set[str] = set()
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line or raw_line.startswith("#"):
            continue
        rule = validate_rule(path, line_number, raw_line)
        if rule in rules:
            raise ValueError(f"{path}:{line_number}: duplicate rule {rule!r}")
        rules.add(rule)
    if not rules:
        raise ValueError(f"{path}: no rules found")
    return rules


def main() -> int:
    paths = sorted(RULE_DIR.glob("*.list"))
    if not paths:
        print("No rule files found", file=sys.stderr)
        return 1

    try:
        loaded = {path.name: load_rules(path) for path in paths}
        core = loaded["Claude-Core.list"]
        complete = loaded["Claude.list"]
        missing = core - complete
        if missing:
            raise ValueError(f"Claude.list is missing core rules: {sorted(missing)}")
    except (KeyError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1

    for name, rules in loaded.items():
        print(f"{name}: {len(rules)} valid rules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
