"""Resolve packaged Bench2Drive route XML / weather XML files.

These paths used to be passed around as relative ``"leaderboard/data/..."``
strings, which only worked when running from the Bench2Drive repo root. After
the data directory was moved inside the ``leaderboard`` Python package, the
canonical way to locate them is via :mod:`importlib.resources`.

This module exposes:

* :func:`data_dir` -- :class:`pathlib.Path` to the on-disk ``leaderboard/data``
  directory inside the installed package (or the source checkout when run in
  editable mode).
* :func:`route_xml` -- returns the path to a specific XML, accepting either a
  bare basename (``bench2drive220``) or one with extension.
* :func:`list_route_xmls` -- list every shipped XML.

Example::

    from leaderboard.data_paths import route_xml
    from leaderboard.utils.route_parser import RouteParser

    configs = RouteParser.parse_routes_file(str(route_xml("bench2drive220")), "1711")
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Iterable, List


_PKG = "leaderboard.data"


def data_dir() -> Path:
    """Return the on-disk path to the bundled ``leaderboard/data`` directory."""
    # ``files`` returns a Traversable; on a regular filesystem install it has a
    # concrete ``__fspath__``. Wrap in ``Path`` so callers get a stable type.
    return Path(resources.files(_PKG))


def list_route_xmls() -> List[Path]:
    """Return all packaged ``*.xml`` files under ``leaderboard/data``."""
    return sorted(p for p in data_dir().iterdir() if p.is_file() and p.suffix == ".xml")


def route_xml(name: str) -> Path:
    """Return the absolute path to a packaged XML.

    ``name`` may be the basename with or without ``.xml`` (e.g. ``"bench2drive220"``,
    ``"bench2drive220.xml"``, ``"weather"``).
    """
    if not name.endswith(".xml"):
        name = name + ".xml"
    path = data_dir() / name
    if not path.is_file():
        raise FileNotFoundError(
            f"Packaged route XML {name!r} not found at {path!s}. "
            f"Available: {[p.name for p in list_route_xmls()]}"
        )
    return path


__all__: Iterable[str] = ("data_dir", "list_route_xmls", "route_xml")
