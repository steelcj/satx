"""The role vocabulary and rank.

sat-configuration-cascade-specification-v0-2-2.md, Vocabulary: "sat,
collection, archive, directory and content are the five possible
roles." Rank order is cascade order: sat outranks everything, content
outranks nothing.
"""

ROLES = ["sat", "collection", "archive", "directory", "content"]
RANK = {role: index for index, role in enumerate(ROLES)}

# sat-configuration-cascade-specification-v0-2-2.md, "The remaining
# subjects": what each role's children field declares, plus sat's own
# baseline. A role's own subjects_needed is {role} | CHILDREN[role],
# since it always states its own children and seeds each child role it
# permits, per "One author folder per role held".
CHILDREN = {
    "sat": ["collection", "archive"],
    "collection": ["collection", "archive"],
    "archive": ["directory", "content"],
    "directory": ["directory", "content"],
    "content": [],
}


def rank_of(role: str) -> int:
    return RANK[role]


def outranks(a: str, b: str) -> bool:
    """True when role `a` outranks role `b`. Equal roles do not outrank
    each other -- sat-configuration-cascade-specification-v0-2-2.md,
    "A role may address itself and the tiers below it, never above"."""
    return RANK[a] < RANK[b]
