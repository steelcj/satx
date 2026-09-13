"""Create a new SAT node.

Written from sat-init-decisions-v0.0.4.md and sat-instance-file-
system-layout-v0.0.2.md, which settle every question this module
raises: two roles at the instance root, an identifier minted at every
node, contextual fields prompted at every tier with Enter meaning
accept-and-write-nothing, and a new instance shipping with its own
en/fr documentation-archive layout rather than a bare skeleton.

Scoped to exactly one command, `sat init`: the instance itself, plus
the en/ and fr/ archives, bin/lib/venvs boundaries, that SAT ships
with any instance. Creating a user collection, archive, directory or
content node is the same underlying mechanism (create_node, below),
extended with per-role thin commands and eventually a preseed, and is
deliberately deferred rather than half-built here.
"""
import uuid
from pathlib import Path

from .nodes import sidecar_dir
from .resolve import compose_namespace, descending
from .roles import CHILDREN, ROLES
from .yamlio import quoted, write_yaml

# This prototype's own version -- see sat-virtual-environments-v0-0-1.md
# and venvs/sat/0.5.0/. Once sat-tool exists, this is read from the
# installed artifact rather than hardcoded here.
SAT_VERSION = "0.5.0"

# Matches the field_kinds table declared at satx's own root, extended
# past the sidecar spec's worked example with DC 1.1's three remaining
# elements (source, relation, coverage) for a complete declaration.
DC_FIELD_KINDS = {
    "publisher": "contextual", "rights": "contextual", "language": "contextual",
    "creator": "contextual", "contributor": "contextual", "coverage": "contextual",
    "subject": "accumulating",
    "title": "local", "description": "local", "date": "local", "type": "local",
    "format": "local", "source": "local", "relation": "local",
    "identifier": "identity",
}
SAT_FIELD_KINDS = {"identifier": "identity", "isVersionOf": "identity", "slug": "local", "order": "contextual"}
FIELD_KINDS = {"dc": DC_FIELD_KINDS, "sat": SAT_FIELD_KINDS}


def mint() -> str:
    """A urn:uuid, v4, generated once and immutable -- sat-init-
    decisions-v0.0.4.md, Identity minting. Never derived from a slug,
    a path, or content."""
    return f"urn:uuid:{uuid.uuid4()}"


def _field(value, overridable=None, status=None):
    field = {"value": value}
    if overridable is not None:
        field["overridable"] = overridable
    if status is not None:
        field["status"] = status
    return field


def _write_config_subject(node: Path, is_dir: bool, author: str, subject: str, defaults: dict) -> None:
    base = sidecar_dir(node, is_dir) / author / "config" / subject
    write_yaml(base / "defaults" / "config.yml", defaults)
    write_yaml(base / "overrides" / "config.yml", {})
    write_yaml(base / "resolved" / "config.yml", defaults)


def _write_metadata_namespace(
    node: Path, is_dir: bool, author: str, namespace: str, defaults: dict, overrides: dict
) -> dict:
    resolved = compose_namespace(
        FIELD_KINDS, namespace, defaults, overrides, {}, {},
        authoring_role=author, where=str(node), problems=[],
    )
    base = sidecar_dir(node, is_dir) / author / "metadata" / namespace
    write_yaml(base / "defaults" / f"{namespace}.yml", defaults)
    write_yaml(base / "overrides" / f"{namespace}.yml", overrides)
    write_yaml(base / "resolved" / f"{namespace}.yml", resolved)
    return resolved


def _subjects_needed(role: str) -> list:
    """A node's author folder addresses itself and each child role it
    seeds -- sat-configuration-cascade-specification-v0-2-2.md, One
    author folder per role held. Self-referencing roles (collection,
    directory) already list themselves in CHILDREN; roles that do not
    self-nest (sat, archive) need it added explicitly."""
    return [role] + [c for c in CHILDREN[role] if c != role]


def _subject_config_defaults(subject: str, interface_language: str, default_metadata: str) -> dict:
    return {
        "children": _field(list(CHILDREN[subject]), overridable=False),
        "default_metadata": _field(quoted(default_metadata), overridable=False),
        "interface_language": _field(quoted(interface_language), overridable=False),
    }


def _prompt_contextual(translate, label: str, inherited) -> dict | None:
    """Enter accepts the inherited value and writes nothing; typing
    writes an override, even one that happens to match what was
    inherited -- sat-init-decisions-v0.0.4.md, What seeding writes,
    per role: "I accept what I am given" and "I claim this value,
    which happens to match" are different statements."""
    shown = inherited[0] if inherited else ""
    answer = input(translate("{label} [{default}]: ").format(label=label, default=shown)).strip()
    if not answer:
        return None
    return _field([answer], overridable=True)


def _prompt_required(translate, label: str) -> str:
    while True:
        answer = input(translate("{label}: ").format(label=label)).strip()
        if answer:
            return answer


def _boundary(node: Path, note: str) -> None:
    sc = sidecar_dir(node, True)
    sc.mkdir(parents=True, exist_ok=True)
    (sc / ".sat-boundary").write_text(note, encoding="utf-8", newline="\n")


def init_instance(root: Path, translate) -> None:
    """Creates a new SAT instance at `root`: its own two-role sidecar
    (`sat` and `collection`, per sat-instance-file-system-layout-
    v0.0.2.md's ruling that a node holding both archives and
    collections is acting as a collection), the bin/lib/venvs
    boundaries, and en/ and fr/ as SAT's own documentation archives,
    each with a docs/ directory node and a messages/ boundary.

    No user collections, archives, directories or content: those are
    separate, later commands over the same create_node mechanism.
    """
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise FileExistsError(f"{root} is not empty; refusing to initialize over existing content")

    interface_language = input(
        translate("Interface language [en]: ")
    ).strip() or "en"
    default_metadata = "dc-1.1"

    # ---- sat role: the software's own identity, nothing editorial ----
    field_kinds_value = {"dc": dict(DC_FIELD_KINDS), "sat": dict(SAT_FIELD_KINDS)}
    sat_baseline = {
        "roles": _field(list(ROLES), overridable=False),
        "sat_version": _field(quoted(SAT_VERSION), overridable=False),
        "children": _field(list(CHILDREN["sat"]), overridable=False),
        "default_metadata": _field(quoted(default_metadata), overridable=False),
        "interface_language": _field(quoted(interface_language), overridable=False),
        "field_kinds": _field(field_kinds_value, overridable=False),
    }
    _write_config_subject(root, True, "sat", "sat", sat_baseline)
    for subject in CHILDREN["sat"]:  # sat is not self-referencing; sat itself is written above
        _write_config_subject(
            root, True, "sat", subject,
            _subject_config_defaults(subject, interface_language, default_metadata),
        )
    _write_metadata_namespace(root, True, "sat", "dc", {}, {})
    root_identifier = mint()
    _write_metadata_namespace(root, True, "sat", "sat", {}, {"identifier": _field(quoted(root_identifier))})

    # ---- collection role: the same node, organizing en/, fr/, and ----
    # ---- (later) content/ -- this is where editorial facts belong ----
    print(translate("This instance's own collection settings, inherited by every archive beneath it."))
    root_dc_overrides = {}
    rights = _prompt_contextual(translate, "rights", None)
    if rights:
        root_dc_overrides["rights"] = rights
    publisher = _prompt_contextual(translate, "publisher", None)
    if publisher:
        root_dc_overrides["publisher"] = publisher
    for subject in _subjects_needed("collection"):
        _write_config_subject(
            root, True, "collection", subject,
            _subject_config_defaults(subject, interface_language, default_metadata),
        )
    root_dc_resolved = _write_metadata_namespace(root, True, "collection", "dc", {}, root_dc_overrides)
    root_dc_descending = descending(FIELD_KINDS, "dc", root_dc_resolved)
    _write_metadata_namespace(root, True, "collection", "sat", {}, {})

    _boundary(
        root / "bin",
        "Commands, by role. Organizing: no sidecar of its own, holds no role, "
        "none of it participates in the cascade.\n",
    )
    _boundary(
        root / "lib",
        "Libraries, by role. Organizing: no sidecar of its own, holds no role, "
        "none of it participates in the cascade.\n",
    )
    _boundary(
        root / "venvs",
        "Virtual environments, keyed by what they serve: venvs/{artifact}/"
        "{version}/. Organizing: no sidecar of its own, holds no role, none of "
        "it participates in the cascade.\n",
    )

    # ---- en/ and fr/: SAT's own documentation archives, paired as ----
    # ---- one aggregating work, per sat-init-decisions-v0.0.4.md ----
    docs_work = mint()
    languages = [("en", "English"), ("fr", "French")]
    for tag, label in languages:
        _create_doc_archive(root, tag, label, root_dc_descending, docs_work, interface_language, translate)

    print(translate("Done."))


def _create_doc_archive(
    root: Path, tag: str, label: str, received_dc: dict, docs_work: str, interface_language: str, translate
) -> None:
    archive = root / tag
    print(translate("Archive {tag} ({label})").format(tag=tag, label=label))

    for subject in _subjects_needed("archive"):
        _write_config_subject(
            archive, True, "archive", subject,
            _subject_config_defaults(subject, interface_language, "dc-1.1"),
        )

    archive_dc_local = {"language": _field([quoted(tag)], overridable=False)}
    rights = _prompt_contextual(translate, "rights", received_dc.get("rights", {}).get("value"))
    if rights:
        archive_dc_local["rights"] = rights
    publisher = _prompt_contextual(translate, "publisher", received_dc.get("publisher", {}).get("value"))
    if publisher:
        archive_dc_local["publisher"] = publisher
    archive_dc_resolved = _write_metadata_namespace(archive, True, "archive", "dc", received_dc, archive_dc_local)
    archive_dc_descending = descending(FIELD_KINDS, "dc", archive_dc_resolved)

    archive_identifier = mint()
    _write_metadata_namespace(
        archive, True, "archive", "sat", {},
        {"identifier": _field(quoted(archive_identifier)), "isVersionOf": _field(quoted(docs_work))},
    )

    docs = archive / "docs"
    for subject in _subjects_needed("directory"):
        _write_config_subject(
            docs, True, "directory", subject,
            _subject_config_defaults(subject, interface_language, "dc-1.1"),
        )
    _write_metadata_namespace(docs, True, "directory", "dc", archive_dc_descending, {})
    _write_metadata_namespace(docs, True, "directory", "sat", {}, {"identifier": _field(quoted(mint()))})

    if tag == "en":
        note = (
            f"Message catalogs for {root.name}/bin and {root.name}/lib, in this language.\n\n"
            "Empty: the source strings in bin and lib are written in English, so there is\n"
            "nothing here to translate into English. A catalog appears here only if the\n"
            "source language changes. See fr/messages for what a populated one looks like.\n"
        )
    else:
        note = (
            f"Message catalogs for {root.name}/bin and {root.name}/lib, in this language.\n\n"
            "Empty for now: no catalog has been extracted or translated into this language yet.\n"
        )
    _boundary(archive / "messages", note)
