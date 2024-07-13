from __future__ import annotations

from functools import lru_cache

import jinja2
import sublime

from .constants import PACKAGE_NAME
from .helpers import is_debug_mode


@lru_cache
def load_string_template(template: str, *, keep_trailing_newlines: bool = False) -> jinja2.Template:
    _JINJA_TEMPLATE_ENV.keep_trailing_newline = keep_trailing_newlines
    return _JINJA_TEMPLATE_ENV.from_string(template)


@lru_cache
def load_resource_template(template_path: str, *, keep_trailing_newlines: bool = False) -> jinja2.Template:
    content = sublime.load_resource(f"Packages/{PACKAGE_NAME}/plugin/templates/{template_path}")
    return load_string_template(content, keep_trailing_newlines=keep_trailing_newlines)


def include_asset(asset_path: str, *, use_cache: bool = True) -> str:
    if not use_cache or asset_path not in _RESOURCE_ASSET_CACHES or is_debug_mode():
        _RESOURCE_ASSET_CACHES[asset_path] = sublime.load_resource(
            f"Packages/{PACKAGE_NAME}/plugin/assets/{asset_path}"
        )
    return _RESOURCE_ASSET_CACHES[asset_path]


def asset_url(asset_path: str) -> str:
    return f"res://Packages/{PACKAGE_NAME}/plugin/assets/{asset_path}"


_JINJA_TEMPLATE_ENV = jinja2.Environment(
    extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
)
_JINJA_TEMPLATE_ENV.globals.update({
    # functions
    "asset_url": asset_url,
    "include_asset": include_asset,
    "is_debug_mode": is_debug_mode,
})

_RESOURCE_ASSET_CACHES: dict[str, str] = {}
