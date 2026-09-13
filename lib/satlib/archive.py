"""Walk a SAT tree, resolve every node, and build the work index.

Written from SAT Sidecars: Config and Metadata v0.0.13 and SAT
Configuration Cascade Specification v0.2.2. The organizing-directory
handling here is the point of writing this rather than reusing the JS
prototype: a directory is a node, a marked boundary, malformed, or
unaccounted for, and only the first of those participates in cascade.
"""
import re
from pathlib import Path

from .nodes import (
    NodeState, classify, config_path, metadata_path, namespaces_of,
    roles_of, should_ignore, sidecar_dir,
)
from .resolve import compose_namespace, consumer_view, descending
from .yamlio import read_yaml

UUID_RE = re.compile(r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)


def _error(problems, where, message):
    problems.append({"level": "error", "where": where, "message": message})


def _warn(problems, where, message):
    problems.append({"level": "warn", "where": where, "message": message})


def _rel(root: Path, path: Path) -> str:
    return str(path.relative_to(root)) if path != root else "."


def read_field_kinds(root: Path, problems: list):
    """field_kinds is declared once, at the sat root's own subject file
    -- sat-sidecars-config-and-metadata-v0-0-13.md, Field kinds."""
    for state in ("resolved", "overrides", "defaults"):
        doc = read_yaml(config_path(root, True, "sat", "sat", state))
        if doc and doc.get("field_kinds", {}).get("value"):
            return doc["field_kinds"]["value"]
    _error(problems, ".", "no field_kinds declared at the sat root; nothing can be resolved without it")
    return None


def _looks_like_a_glob(text: str) -> bool:
    """Heuristic for satx-shape-and-purpose-v0-0-8.md's ninth error
    case: a .sat-boundary written like a .gitignore pattern rather than
    prose for a human. Prose has spaces; a lone glob token usually
    doesn't."""
    stripped = text.strip()
    if not stripped or " " in stripped or "\n" in stripped.strip():
        return False
    return any(ch in stripped for ch in "*?[]")


def _check_boundary_marker(root: Path, dir_path: Path, problems: list):
    marker = sidecar_dir(dir_path, True) / ".sat-boundary"
    try:
        text = marker.read_text(encoding="utf-8")
    except OSError:
        return
    if _looks_like_a_glob(text):
        _warn(
            problems, _rel(root, dir_path),
            f".sat-boundary looks like a glob pattern ({text.strip()!r}), not prose for a human; "
            f"probably a misunderstanding",
        )


def _audit_organizing_subtree(root: Path, dir_path: Path, problems: list):
    """Descend through organizing territory checking for the one thing
    that must not be there: archived content. Nothing here cascades."""
    try:
        entries = sorted(dir_path.iterdir(), key=lambda e: e.name)
    except OSError:
        return
    for entry in entries:
        if should_ignore(entry.name):
            continue
        if entry.is_dir():
            state = classify(entry, True)
            if state == NodeState.NODE:
                _error(
                    problems, _rel(root, entry),
                    "archived content outside the cascade: a described node beneath an organizing directory",
                )
            elif state == NodeState.MALFORMED:
                _error(
                    problems, _rel(root, entry),
                    "sidecar carries neither a role folder nor a boundary marker",
                )
            elif state == NodeState.BOUNDARY:
                _check_boundary_marker(root, entry, problems)
            _audit_organizing_subtree(root, entry, problems)
        else:
            if classify(entry, False) == NodeState.NODE:
                _error(
                    problems, _rel(root, entry),
                    "archived content outside the cascade: a described node beneath an organizing directory",
                )


def _walk_active(root: Path, dir_path: Path, ancestors_resolved, field_kinds, problems, out_nodes):
    """Recurse through cascade-active territory: real nodes only."""
    for entry in sorted(dir_path.iterdir(), key=lambda e: e.name):
        if should_ignore(entry.name):
            continue
        is_dir = entry.is_dir()
        state = classify(entry, is_dir)
        where = _rel(root, entry)

        if state == NodeState.UNACCOUNTED:
            if is_dir:
                _error(problems, where, "unaccounted for: no sidecar and no .sat-boundary")
                # Nothing to resolve; still worth a shallow look for
                # nested nodes someone described anyway, though this
                # directory itself is neither node nor boundary.
                _audit_organizing_subtree(root, entry, problems)
            # A bare file with no sidecar is simply not a node.
            continue

        if state == NodeState.MALFORMED:
            _error(problems, where, "sidecar carries neither a role folder nor a boundary marker")
            if is_dir:
                _audit_organizing_subtree(root, entry, problems)
            continue

        if state == NodeState.BOUNDARY:
            _check_boundary_marker(root, entry, problems)
            if is_dir:
                _audit_organizing_subtree(root, entry, problems)
            continue

        # NodeState.NODE
        node = _resolve_node(root, entry, is_dir, ancestors_resolved, field_kinds, problems)
        out_nodes.append(node)
        if is_dir:
            _walk_active(root, entry, node["descending"], field_kinds, problems, out_nodes)


def _resolve_node(root, node_path, is_dir, ancestors_resolved, field_kinds, problems):
    where = _rel(root, node_path)
    roles = roles_of(node_path, is_dir)

    namespaces = set(namespaces_of(node_path, is_dir)) | set((ancestors_resolved or {}).keys())

    resolved_by_ns = {}
    for namespace in namespaces:
        received = (ancestors_resolved or {}).get(namespace, {})
        for index, role in enumerate(roles):
            local_doc = read_yaml(metadata_path(node_path, is_dir, role, namespace, "overrides")) or {}
            local_rows = local_doc.get("subject", {}) if namespace != "sat" else {}
            amend = local_doc.get("amend", {})
            local_plain = {k: v for k, v in local_doc.items() if k not in ("subject", "amend")}
            step = compose_namespace(
                field_kinds, namespace, received, local_plain, local_rows, amend,
                authoring_role=role, where=where, problems=problems,
                same_node=(index > 0),
            )
            received = step
        resolved_by_ns[namespace] = received

    desc = {ns: descending(field_kinds, ns, fields) for ns, fields in resolved_by_ns.items()}
    consumer = {ns: consumer_view(fields) for ns, fields in resolved_by_ns.items()}

    return {
        "path": node_path, "where": where, "is_dir": is_dir, "roles": roles,
        "resolved": resolved_by_ns, "descending": desc, "consumer": consumer,
    }


def _build_work_index(nodes: list, problems: list) -> dict:
    works = {}
    seen_identifiers = {}
    for n in nodes:
        if "content" not in n["roles"]:
            continue
        sat = n["consumer"].get("sat", {})
        identifier = sat.get("identifier")
        work = sat.get("isVersionOf")

        if not identifier:
            _error(problems, n["where"], "content node has no sat:identifier")
            continue
        if not UUID_RE.match(identifier):
            _error(problems, n["where"], f"sat:identifier is not a urn:uuid: {identifier}")
            continue
        if identifier in seen_identifiers:
            _error(problems, n["where"], f"sat:identifier is not unique; also {seen_identifiers[identifier]}")
        seen_identifiers[identifier] = n["where"]

        if not work:
            _warn(problems, n["where"], "content node has no sat:isVersionOf")
            continue
        if not UUID_RE.match(work):
            _error(problems, n["where"], f"sat:isVersionOf is not a urn:uuid: {work}")
            continue

        dc = n["consumer"].get("dc", {})
        works.setdefault(work, {"work": work, "expressions": []})["expressions"].append({
            "identifier": identifier, "where": n["where"],
            "language": (dc.get("language") or [None])[0],
            "title": (dc.get("title") or [None])[0],
        })

    for w in works.values():
        seen_lang = {}
        for e in w["expressions"]:
            if e["language"] is None:
                continue
            if e["language"] in seen_lang:
                _error(
                    problems, e["where"],
                    f'duplicate language "{e["language"]}" for this work; also {seen_lang[e["language"]]}',
                )
            seen_lang[e["language"]] = e["where"]

    return works


def read_archive(root: Path):
    """The entry point: returns {nodes, works, problems, field_kinds}."""
    root = Path(root).resolve()
    problems = []
    field_kinds = read_field_kinds(root, problems)
    if field_kinds is None:
        return {"nodes": [], "works": {}, "problems": problems, "field_kinds": None}

    root_state = classify(root, True)
    if root_state != NodeState.NODE:
        _error(problems, ".", "instance root has no sidecar role folder")
        return {"nodes": [], "works": {}, "problems": problems, "field_kinds": field_kinds}

    root_node = _resolve_node(root, root, True, {}, field_kinds, problems)
    nodes = [root_node]
    _walk_active(root, root, root_node["descending"], field_kinds, problems, nodes)

    works = _build_work_index(nodes, problems)
    return {"nodes": nodes, "works": works, "problems": problems, "field_kinds": field_kinds}
