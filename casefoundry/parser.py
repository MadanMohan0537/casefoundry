"""Small, auditable parser for numbered Markdown requirement clauses."""

import re

from .models import Requirement


CLAUSE = re.compile(r"^\s*(?:[-*]\s*)?\[(R\d+)\]\s+(.+?)\s*$", re.IGNORECASE)


def parse_requirements(markdown: str) -> list[Requirement]:
    found: list[Requirement] = []
    seen: set[str] = set()
    for line in markdown.splitlines():
        match = CLAUSE.match(line)
        if not match:
            continue
        identifier, text = match.group(1).upper(), match.group(2).strip()
        if identifier in seen:
            raise ValueError(f"duplicate requirement id: {identifier}")
        seen.add(identifier)
        found.append(Requirement(identifier, text))
    if not found:
        raise ValueError("no requirements found; use '[R1] clause' lines")
    return found

