"""YAML I/O, per satx: shape and purpose, The scripts.

ruamel.yaml with the modern YAML() API, never PyYAML: PyYAML is YAML
1.1, where "no" is a boolean and also the ISO 639-1 code for Norwegian.

preserve_quotes is set because this module is also used to rewrite
overrides/ files, the only hand-edited state, and round-trip mode
would otherwise strip an archivist's quoting on the next write.
"""
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as DQ

_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.default_flow_style = False
_yaml.width = 100

NOTSET = "<notset>"


def quoted(value: str) -> DQ:
    """Wrap a language tag or slug for explicit quoting on write.

    satx-shape-and-purpose-v0-0-8.md, The scripts: "values the
    specification says to quote are wrapped in DoubleQuotedScalarString
    when written, rather than relying on the dumper to decide."
    """
    return DQ(value)


def read_yaml(path: Path):
    """None when the file is absent. An absent file and an empty one
    are different states -- sat-sidecars-config-and-metadata-v0-0-13.md,
    Every namespace materialises at every node: "Absent means the
    namespace was never declared. Empty means it was declared and
    nothing descended into it." Callers that need to tell the two apart
    check os.path.exists separately; read_yaml returns {} for an empty
    file and None only when the file does not exist.
    """
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        data = _yaml.load(f)
    return data if data is not None else {}


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        if data:
            _yaml.dump(data, f)
        else:
            f.write("")
