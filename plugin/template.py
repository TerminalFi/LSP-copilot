from __future__ import annotations

import base64
import mimetypes
from functools import lru_cache

import jinja2
import sublime

from .constants import PACKAGE_NAME


@lru_cache
def load_string_template(template: str, *, keep_trailing_newlines: bool = False) -> jinja2.Template:
    _JINJA_TEMPLATE_ENV.keep_trailing_newline = keep_trailing_newlines
    return _JINJA_TEMPLATE_ENV.from_string(template)


@lru_cache
def load_resource_template(template_path: str, *, keep_trailing_newlines: bool = False) -> jinja2.Template:
    content = sublime.load_resource(f"Packages/{PACKAGE_NAME}/plugin/templates/{template_path}")
    return load_string_template(content, keep_trailing_newlines=keep_trailing_newlines)


@lru_cache
def base64_resource_url(asset: str, is_sublime_cache: bool = False, *, mime_type: str | None = None) -> str:
    mime_type = mime_type or mimetypes.guess_type(asset)[0] or "unknown"
    if is_sublime_cache:
        path = f"{sublime.cache_path()}/{PACKAGE_NAME}/{asset}"
        with open(path, "rb") as file:
            content = file.read()
    else:
        path = f"Packages/{PACKAGE_NAME}/plugin/assets/{asset}"
        content = sublime.load_binary_resource(path)
    content_b64 = base64.b64encode(content).decode()
    return f"data:{mime_type};base64,{content_b64}"


_JINJA_TEMPLATE_ENV = jinja2.Environment(
    extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
)
_JINJA_TEMPLATE_ENV.globals.update({
    # functions
    "base64_resource_url": base64_resource_url,
})
