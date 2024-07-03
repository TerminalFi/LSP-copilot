from __future__ import annotations

import base64
import mimetypes
from functools import lru_cache
from typing import Any

import jinja2
import sublime

from .constants import PACKAGE_NAME


@lru_cache
def load_string_template(template: str, keep_trailing_newlines: bool = False) -> jinja2.Template:
    JINJA_TEMPLATE_ENV.keep_trailing_newline = keep_trailing_newlines
    return JINJA_TEMPLATE_ENV.from_string(template)


@lru_cache
def load_resource_template(resource_name: str, keep_trailing_newlines: bool = False) -> jinja2.Template:
    content = sublime.load_resource(f"Packages/{PACKAGE_NAME}/plugin/templates/{resource_name}")
    return load_string_template(content, keep_trailing_newlines)


@lru_cache
def base64_resource_url(resource_name: str) -> str:
    mime_type = mimetypes.guess_type(resource_name)[0] or "unknown"
    content = sublime.load_binary_resource(f"Packages/{PACKAGE_NAME}/plugin/assets/{resource_name}")
    content_b64 = base64.b64encode(content).decode()
    return f"data:{mime_type};base64,{content_b64}"


JINJA_GLOBALS: dict[str, Any] = {
    "base64_resource_url": base64_resource_url,
}

JINJA_TEMPLATE_ENV = jinja2.Environment(
    extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
)
JINJA_TEMPLATE_ENV.globals.update(JINJA_GLOBALS)
