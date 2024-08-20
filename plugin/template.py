from __future__ import annotations

from functools import lru_cache
from typing import Any, Iterable

import jinja2
import sublime

from .constants import PACKAGE_NAME
from .helpers import is_debug_mode


@lru_cache
def load_string_template(template: str, *, keep_trailing_newline: bool = False) -> jinja2.Template:
    return _JINJA_TEMPLATE_ENV.overlay(keep_trailing_newline=keep_trailing_newline).from_string(template)


@lru_cache
def load_resource_template(template_path: str, *, keep_trailing_newline: bool = False) -> jinja2.Template:
    content = sublime.load_resource(f"Packages/{PACKAGE_NAME}/plugin/templates/{template_path}")
    return load_string_template(content, keep_trailing_newline=keep_trailing_newline)


def asset_url(asset_path: str) -> str:
    return f"res://{_plugin_asset_path(asset_path)}"


def command_url(commmand: str, args: dict[Any]) -> str:
    return sublime.command_url(commmand, args)


def include_asset(asset_path: str, *, use_cache: bool = True) -> str:
    if not use_cache or asset_path not in _RESOURCE_ASSET_CACHES or is_debug_mode():
        _RESOURCE_ASSET_CACHES[asset_path] = sublime.load_resource(_plugin_asset_path(asset_path))
    return _RESOURCE_ASSET_CACHES[asset_path]


def multi_replace(message: str, replacements: Iterable[tuple[str, str]]) -> str:
    for old, new in replacements:
        message = message.replace(old, new)
    return message


def _plugin_asset_path(asset_path: str) -> str:
    return f"Packages/{PACKAGE_NAME}/plugin/assets/{asset_path}"


_JINJA_TEMPLATE_ENV = jinja2.Environment(
    extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
)
_JINJA_TEMPLATE_ENV.filters.update(
    multi_replace=multi_replace,
)
_JINJA_TEMPLATE_ENV.globals.update(
    # functions
    asset_url=asset_url,
    include_asset=include_asset,
    is_debug_mode=is_debug_mode,
    command_url=command_url,
)

_RESOURCE_ASSET_CACHES: dict[str, str] = {}
