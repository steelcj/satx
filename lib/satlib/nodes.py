"""Node discovery, sidecar paths, and the organizing-directory boundary.

Written from SAT Sidecars: Config and Metadata v0.0.13 and satx: Shape
and Purpose v0.0.8. This is the module the JS prototype at
.claude/reference/sat-reader-v0.0.1/ gets wrong: it predates
.sat-boundary and treats an absent sidecar as meaning organizing. Here,
absence is an error (Unaccounted for) and the marker is the signal.
"""
from pathlib import Path

from .roles import ROLES

BOUNDARY_MARKER = ".sat-boundary"

IGNORED_NAMES = {".DS_Store", "Thumbs.db", ".git"}


def sidecar_dir(node_path: Path, is_dir: bool) -> Path:
    """.{node}.assets/, beside a file node or inside a directory node --
    sat-configuration-cascade-specification-v0-2-2.md, Where a sidecar
    sits."""
    name = node_path.name
    base = node_path if is_dir else node_path.parent
    return base / f".{name}.assets"


def has_sidecar(node_path: Path, is_dir: bool) -> bool:
    return sidecar_dir(node_path, is_dir).is_dir()


def roles_of(node_path: Path, is_dir: bool) -> list:
    """Role folders inside the sidecar, in rank order. Empty if the
    sidecar is absent, holds only the boundary marker, or holds
    neither."""
    sc = sidecar_dir(node_path, is_dir)
    if not sc.is_dir():
        return []
    found = [e.name for e in sc.iterdir() if e.is_dir() and e.name in ROLES]
    return sorted(found, key=ROLES.index)


def is_boundary_marked(node_path: Path, is_dir: bool) -> bool:
    """True when the sidecar carries .sat-boundary. satx-shape-and-
    purpose-v0-0-8.md, Organizing directories declare themselves: "The
    presence of the file is the whole signal.\""""
    return (sidecar_dir(node_path, is_dir) / BOUNDARY_MARKER).is_file()


class NodeState:
    """What a directory or file is, from the sidecar alone."""

    NODE = "node"                # has a role folder
    BOUNDARY = "boundary"        # marker present, no role folder
    MALFORMED = "malformed"      # sidecar exists, neither role nor marker
    UNACCOUNTED = "unaccounted"  # no sidecar at all


def classify(node_path: Path, is_dir: bool) -> str:
    sc = sidecar_dir(node_path, is_dir)
    if not sc.is_dir():
        return NodeState.UNACCOUNTED
    roles = roles_of(node_path, is_dir)
    marked = is_boundary_marked(node_path, is_dir)
    if roles:
        return NodeState.NODE
    if marked:
        return NodeState.BOUNDARY
    return NodeState.MALFORMED


def namespaces_of(node_path: Path, is_dir: bool) -> list:
    """Metadata namespaces declared across every role the node holds."""
    found = set()
    sc = sidecar_dir(node_path, is_dir)
    for role in roles_of(node_path, is_dir):
        meta = sc / role / "metadata"
        if meta.is_dir():
            found.update(e.name for e in meta.iterdir() if e.is_dir())
    return sorted(found)


def config_path(node_path: Path, is_dir: bool, author: str, subject: str, state: str) -> Path:
    return sidecar_dir(node_path, is_dir) / author / "config" / subject / state / "config.yml"


def metadata_path(node_path: Path, is_dir: bool, author: str, namespace: str, state: str) -> Path:
    return sidecar_dir(node_path, is_dir) / author / "metadata" / namespace / state / f"{namespace}.yml"


def should_ignore(name: str) -> bool:
    """sat-configuration-cascade-specification-v0-2-2.md, What SAT
    ignores: filesystem noise is never a candidate content node. This
    also skips sidecars themselves: `.{name}.assets/` is bookkeeping
    that belongs to its node, not a sibling node to classify in its own
    right -- the JS prototype's walkNodes makes the same exclusion."""
    if name.startswith("."):
        return True
    if name in IGNORED_NAMES:
        return True
    if name.endswith(".swp") or name.endswith("~"):
        return True
    return False
