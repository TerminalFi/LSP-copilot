from __future__ import annotations

import mimetypes
from functools import lru_cache

import jinja2
import sublime

from .constants import PACKAGE_NAME
from .utils import bytes_to_data_url


@lru_cache
def load_string_template(template: str, *, keep_trailing_newlines: bool = False) -> jinja2.Template:
    _JINJA_TEMPLATE_ENV.keep_trailing_newline = keep_trailing_newlines
    return _JINJA_TEMPLATE_ENV.from_string(template)


@lru_cache
def load_resource_template(template_path: str, *, keep_trailing_newlines: bool = False) -> jinja2.Template:
    content = sublime.load_resource(f"Packages/{PACKAGE_NAME}/plugin/templates/{template_path}")
    return load_string_template(content, keep_trailing_newlines=keep_trailing_newlines)


@lru_cache
def base64_resource_url(asset_path: str, *, mime_type: str | None = None) -> str:
    mime_type = mime_type or mimetypes.guess_type(asset_path)[0] or "unknown"
    data = sublime.load_binary_resource(f"Packages/{PACKAGE_NAME}/plugin/assets/{asset_path}")
    return bytes_to_data_url(data, mime_type=mime_type)


def load_resource_asset(asset_path: str, *, use_cache: bool = True) -> str:
    if not use_cache or asset_path not in _RESOURCE_ASSET_CACHES:
        _RESOURCE_ASSET_CACHES[asset_path] = sublime.load_resource(
            f"Packages/{PACKAGE_NAME}/plugin/assets/{asset_path}"
        )
    return _RESOURCE_ASSET_CACHES[asset_path]


_JINJA_TEMPLATE_ENV = jinja2.Environment(
    extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
)
_JINJA_TEMPLATE_ENV.globals.update({
    # functions
    "base64_resource_url": base64_resource_url,
    "load_resource_asset": load_resource_asset,
})

_RESOURCE_ASSET_CACHES: dict[str, str] = {}
