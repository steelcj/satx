"""Composition: read defaults, read overrides, apply the permitted
deltas, write resolved. One operation for both trees.

sat-sidecars-config-and-metadata-v0-0-14.md, One resolver: "Configuration
and metadata are composed by the same operation... There is one
implementation, not two kept in step." Config never needs a field-kind
table -- every config field is received-and-overridable-or-not, decided
by its own `overridable` flag, which is data rather than a lookup.
Metadata needs field_kinds because most Dublin Core elements are local
to the leaf that states them, per sat-sidecars-config-and-metadata-
v0-0-14.md, Field kinds.
"""
from .i18n import report
from .roles import ROLES, outranks


class FieldKindError(Exception):
    """A field with no declared kind is an error rather than a default
    -- sat-sidecars-config-and-metadata-v0-0-14.md, Field kinds:
    "Guessing would make a typo in an element name behave like a new
    local field, silently.\""""


def kind_of(field_kinds: dict, namespace: str, field: str, translate=None) -> str:
    kind = (field_kinds.get(namespace) or {}).get(field)
    if kind is None:
        template = (
            "no declared kind for {namespace}:{field}. "
            "Declare it in field_kinds at the sat root, or correct the element name."
        )
        message = (translate or (lambda s: s))(template).format(namespace=namespace, field=field)
        raise FieldKindError(message)
    return kind


# ------------------------------------------------------------- config

def compose_config(received: dict, local: dict, where: str, problems: list, translate=None) -> dict:
    """Every config field is {value, overridable, status?}. A local
    restatement against a field already overridable: false upstream is
    held and marked inert rather than applied -- sat-configuration-
    cascade-specification-v0-2-2.md, Authority: "Sat's value stands. No
    tier below may change it.\""""
    resolved = {}
    for name in sorted(set(received) | set(local)):
        inherited = received.get(name)
        stated = local.get(name)
        if stated is None:
            if inherited is not None:
                resolved[name] = dict(inherited)
            continue
        if inherited is not None and inherited.get("overridable") is False:
            report(
                problems, "warn", where, translate,
                '"{name}" is locked upstream; override held but not applied', name=name,
            )
            resolved[name] = {**inherited, "inert": True, "heldValue": stated.get("value")}
            continue
        resolved[name] = dict(stated)
    return resolved


# ----------------------------------------------------------- metadata

def merge_rows(
    received: dict, local: dict, authoring_role: str, where: str, problems: list, translate=None
) -> dict:
    """Accumulating rows, keyed by role -- sat-sidecars-config-and-
    metadata-v0-0-14.md, Rows record who decided. A tier writes rows at
    or below its own rank; writing above it is reported rather than
    applied."""
    out = {}
    for role in ROLES:
        a = received.get(role, [])
        b = local.get(role, [])
        if not a and not b:
            continue
        if b and outranks(role, authoring_role):
            report(
                problems, "error", where, translate,
                "{authoring_role} wrote into the {role} row, which outranks it",
                authoring_role=authoring_role, role=role,
            )
            out[role] = [dict(x) for x in a]
            continue
        merged = [dict(x) for x in a]
        for item in b:
            idx = next((i for i, x in enumerate(merged) if x.get("value") == item.get("value")), None)
            if idx is None:
                merged.append(dict(item))
                continue
            if merged[idx].get("overridable") is False:
                report(
                    problems, "warn", where, translate,
                    '"{value}" is locked in the {role} row; held, not applied',
                    value=item.get("value"), role=role,
                )
                merged[idx] = {**merged[idx], "inert": True, "heldValue": item.get("value")}
                continue
            merged[idx] = {**merged[idx], **item}
        out[role] = merged
    return out


def apply_amend(
    rows: dict, amend: dict, amending_role: str, where: str, problems: list, translate=None
) -> dict:
    """sat-sidecars-config-and-metadata-v0-0-14.md, Amendment reaches
    into a lower row. `amend` is {target_role: {field_name: [edits]}};
    only the "subject" field is accumulating today, so field_name is
    always "subject", but the shape is kept general since the spec's
    own worked example nests it this way."""
    if not amend:
        return rows
    out = {role: [dict(item) for item in items] for role, items in rows.items()}
    for target_role, fields in amend.items():
        edits = fields.get("subject", [])
        if not edits:
            continue
        if not outranks(amending_role, target_role):
            report(
                problems, "error", where, translate,
                "{amending_role} cannot amend the {target_role} row",
                amending_role=amending_role, target_role=target_role,
            )
            continue
        row = out.get(target_role)
        if row is None:
            report(
                problems, "error", where, translate,
                "amend targets an empty {target_role} row: {matches}",
                target_role=target_role, matches=[edit["match"] for edit in edits],
            )
            continue
        for edit in edits:
            idx = next((i for i, x in enumerate(row) if x.get("value") == edit["match"]), None)
            if idx is None:
                report(
                    problems, "error", where, translate,
                    "amend matches nothing in the {target_role} row: {match}",
                    target_role=target_role, match=edit["match"],
                )
                continue
            changes = {k: v for k, v in edit.items() if k != "match"}
            amended_by = row[idx].get("amendedBy", []) + [amending_role]
            row[idx] = {**row[idx], **changes, "amendedBy": amended_by}
    return out


def compose_namespace(
    field_kinds: dict,
    namespace: str,
    received: dict,
    local_plain: dict,
    local_rows: dict,
    amend: dict,
    authoring_role: str,
    where: str,
    problems: list,
    same_node: bool = False,
    translate=None,
) -> dict:
    """One namespace at one node. `received` is the parent's descending
    output for this namespace; `local_plain` is this node's own stated
    fields excluding accumulating ones; `local_rows` and `amend` cover
    the namespace's one accumulating field, `subject`, if any.

    `same_node` is True when `received` is not an ancestor's output but
    an earlier role's own resolved output at this same multi-role node
    -- sat-configuration-cascade-specification-v0-2-2.md, One author
    folder per role held: "A multi-role node writes one layer per role
    it holds, and those layers resolve in role order." A local or
    identity field a later role does not restate is still this node's
    own value in that case, not an ancestor's leaking through, so it
    carries forward rather than being dropped.
    """
    resolved = {}
    names = (set(received) | set(local_plain)) - {"subject"}
    for name in names:
        try:
            kind = kind_of(field_kinds, namespace, name, translate=translate)
        except FieldKindError as exc:
            problems.append({"level": "error", "where": where, "message": str(exc)})
            continue

        if kind in ("local", "identity"):
            if name in local_plain:
                resolved[name] = dict(local_plain[name])
            elif same_node and name in received:
                resolved[name] = dict(received[name])
            # Otherwise never received: a value reaching here from an
            # ancestor's `received` means its descending() filter
            # failed upstream, so it is dropped rather than trusted.
            continue

        # contextual
        inherited = received.get(name)
        stated = local_plain.get(name)
        if stated is None:
            if inherited is not None:
                resolved[name] = dict(inherited)
            continue
        if inherited is not None and inherited.get("overridable") is False:
            report(
                problems, "warn", where, translate,
                '"{name}" is locked upstream; override held but not applied', name=name,
            )
            resolved[name] = {**inherited, "inert": True, "heldValue": stated.get("value")}
            continue
        resolved[name] = dict(stated)

    if "subject" in field_kinds.get(namespace, {}):
        received_rows = received.get("subject", {})
        merged = merge_rows(received_rows, local_rows or {}, authoring_role, where, problems, translate)
        merged = apply_amend(merged, amend or {}, authoring_role, where, problems, translate)
        if merged:
            resolved["subject"] = merged

    return resolved


def descending(field_kinds: dict, namespace: str, resolved: dict) -> dict:
    """What a node passes down: local and identity fields never
    descend. sat-sidecars-config-and-metadata-v0-0-14.md, Field kinds:
    "Local fields must not be received, and the failure is silent.\""""
    out = {}
    for name, entry in resolved.items():
        if name == "subject":
            out[name] = entry
            continue
        try:
            kind = kind_of(field_kinds, namespace, name)
        except FieldKindError:
            continue
        if kind in ("local", "identity"):
            continue
        out[name] = entry
    return out


def consumer_view(resolved: dict) -> dict:
    """The view a consumer receives: deprecated items and <notset>
    entries are excluded here and kept in `resolved`, per sat-sidecars-
    config-and-metadata-v0-0-14.md, Removal is not reset."""
    out = {}
    for name, entry in resolved.items():
        if name == "subject":
            rows = {}
            for role, items in entry.items():
                kept = [i for i in items if i.get("status") != "deprecated" and i.get("value") != "<notset>"]
                if kept:
                    rows[role] = kept
            if rows:
                out[name] = rows
            continue
        if entry.get("status") == "deprecated":
            continue
        if entry.get("value") == "<notset>":
            continue
        out[name] = entry.get("value")
    return out
