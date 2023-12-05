# These are customized rulesets.
# This is nested under hit.signature_name
# Good luck, I guess.

from dataclasses import dataclass
from typing import List


@dataclass
class CharacterTypesRule:
    """The data nested in a rule."""

    start: int
    end: int
    match_percent: int
    order: int


@dataclass
class CharacterType:
    """Standardize the collected data."""

    signature_name: str
    rule_name: str
    rules: List[CharacterTypesRule]


character_types = {
    "MS Office File": CharacterType(
        signature_name="MS Office File",
        rule_name="find-letters",
        rules=[
            CharacterTypesRule(start=65, end=122, match_percent=30, order=201),
        ],
    ),
    "PDF": CharacterType(
        signature_name="PDF",
        rule_name="stats-find",
        rules=[
            CharacterTypesRule(start=15, end=16, match_percent=10, order=201),
            CharacterTypesRule(start=31, end=32, match_percent=10, order=201),
            CharacterTypesRule(start=65, end=122, match_percent=10, order=201),
        ],
    ),
    # All remaining blocks are allocated to JPEG
    "JPEG": CharacterType(
        signature_name="JPEG",
        rule_name="capture-remaining",
        rules=[CharacterTypesRule(start=0, end=255, match_percent=99, order=201)],
    ),
}
