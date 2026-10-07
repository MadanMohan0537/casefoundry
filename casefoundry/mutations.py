"""Mutation adequacy for the deterministic sample policy application."""

from __future__ import annotations

from dataclasses import dataclass

from .models import TestCase


MUTATIONS = ("oversize_allowed", "unsafe_extension_allowed", "role_check_removed", "unsupported_answered")


def toy_app(payload: dict, mutation: str | None = None) -> str:
    action = payload.get("action")
    if action == "upload":
        if payload.get("extension") != "txt" and mutation != "unsafe_extension_allowed":
            return "deny"
        if payload.get("size", 0) > 1_000_000 and mutation != "oversize_allowed":
            return "deny"
        return "allow"
    if action == "delete":
        if mutation == "role_check_removed":
            return "allow"
        return "allow" if payload.get("role") == "administrator" else "deny"
    if action == "answer":
        if payload.get("has_source"):
            return "grounded"
        return "grounded" if mutation == "unsupported_answered" else "refuse"
    return "manual-review"


@dataclass(frozen=True)
class MutationReport:
    killed: int
    total: int
    score: float
    survivors: tuple[str, ...]
    matrix: dict[str, list[str]]


def mutation_score(cases: list[TestCase]) -> MutationReport:
    executable = [case for case in cases if case.expected != "manual-review"]
    matrix: dict[str, list[str]] = {}
    survivors: list[str] = []
    for mutation in MUTATIONS:
        killers = [case.id for case in executable
                   if toy_app(case.input) == case.expected and
                   toy_app(case.input, mutation) != case.expected]
        matrix[mutation] = killers
        if not killers:
            survivors.append(mutation)
    killed = len(MUTATIONS) - len(survivors)
    return MutationReport(killed, len(MUTATIONS), killed / len(MUTATIONS),
                          tuple(survivors), matrix)

