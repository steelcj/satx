"""A minimal gettext-alike: no shelling out to msgfmt, no compiled
.mo files, just a small pure-Python .po reader.

STOPGAP, not a destination. satx: shape and purpose, The scripts,
rules out shelling out to external commands, and stdlib gettext needs
a compiled .mo, which normally comes from msgfmt. This reader is what
that leaves: msgid/msgstr pairs and a fallback to English, nothing
else. Real gettext gives plural forms, message contexts, and
`msgmerge` to carry translations forward when a source string changes;
none of those exist here. Adopt real gettext, or a pure-Python library
that implements it properly, before this instance's catalogs grow past
a handful of flat strings -- see NEXT.md.

Catalog location: SAT Sidecars: Config and Metadata v0.0.14, Interface
translations are not archived content -- {lang}/messages/{domain}/,
one domain per piece of software, bin and lib today.
"""
import re
from pathlib import Path

_ENTRY_RE = re.compile(r'^(msgid|msgstr)\s+"(.*)"\s*$')
_CONT_RE = re.compile(r'^"(.*)"\s*$')


def _unescape(text: str) -> str:
    return text.replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")


def load_po(path: Path) -> dict:
    """Parses msgid/msgstr pairs, including quoted-string continuation
    lines. Comments and metadata (msgid "") are skipped."""
    catalog = {}
    if not path.is_file():
        return catalog
    msgid = None
    msgstr = None
    field = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        m = _ENTRY_RE.match(line)
        if m:
            if field == "msgstr" and msgid is not None:
                catalog[msgid] = msgstr
            kind, text = m.group(1), _unescape(m.group(2))
            if kind == "msgid":
                msgid, msgstr, field = text, "", "msgid"
            else:
                msgstr, field = text, "msgstr"
            continue
        c = _CONT_RE.match(line)
        if c and field:
            if field == "msgid":
                msgid += _unescape(c.group(1))
            else:
                msgstr += _unescape(c.group(1))
    if field == "msgstr" and msgid is not None:
        catalog[msgid] = msgstr
    catalog.pop("", None)
    return catalog


class Translator:
    """Looks up a string in a loaded catalog, falling back to the
    English source text (the msgid) when the catalog has nothing --
    the same fallback stdlib gettext gives you."""

    def __init__(self, catalog: dict):
        self._catalog = catalog

    def __call__(self, message: str) -> str:
        translated = self._catalog.get(message)
        return translated if translated else message


def translator_for(instance_root: Path, language: str, domain: str) -> Translator:
    """language is the interface_language ("en-ca", "fr"); domain is
    "bin" or "lib". English never needs a catalog: it is the source
    language the strings are written in."""
    base = language.split("-")[0]
    if base == "en":
        return Translator({})
    po_path = instance_root / base / "messages" / domain / f"sat-{domain}.po"
    return Translator(load_po(po_path))


def identity(message: str) -> str:
    """The no-op translator. Returns the English source text (the
    msgid) unchanged; used as report()'s default so every internal
    satlib caller keeps working before it has threaded a real
    translator through."""
    return message


def report(problems: list, level: str, where: str, translate, template: str, **kwargs) -> None:
    """Appends one problem to `problems`, translating `template` --
    the English source string, the msgid -- before filling in
    `kwargs`. Translating before formatting is what keeps the catalog
    entry the static template rather than one entry per interpolated
    value: "sat:identifier is not a urn:uuid: {identifier}" is one
    msgid regardless of how many different identifiers ever appear
    there. `translate` may be None, in which case the message is left
    in English.
    """
    translate = translate or identity
    message = translate(template)
    if kwargs:
        message = message.format(**kwargs)
    problems.append({"level": level, "where": where, "message": message})
