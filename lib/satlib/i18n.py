"""A minimal gettext-alike: no shelling out to msgfmt, no compiled
.mo files, just a small pure-Python .po reader.

satx: shape and purpose, The scripts, rules out shelling out to
external commands, and stdlib gettext needs a compiled .mo, which
normally comes from msgfmt. Our catalogs are small (a handful of CLI
and report strings), so a direct .po reader is simpler and dependency-
free than vendoring a compiler for a format we can just parse.

Catalog location: SAT Sidecars: Config and Metadata v0.0.13, Interface
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
