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
        rules=[CharacterTypesRule(start=65, end=122, match_percent=70,order=201)],
    )
}
