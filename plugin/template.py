from __future__ import annotations

from functools import lru_cache

import jinja2
import sublime

from .constants import PACKAGE_NAME

JINJA_TEMPLATE_ENV = jinja2.Environment(
    extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
)

JINJA_TEMPLATE_ENV2 = jinja2.Environment(
    extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"], keep_trailing_newline=True
)


@lru_cache
def load_string_template(template: str, keep_trailing_newlines: bool = False) -> jinja2.Template:
    if keep_trailing_newlines:
        return JINJA_TEMPLATE_ENV2.from_string(template)
    return JINJA_TEMPLATE_ENV.from_string(template)


@lru_cache
def load_resource_template(resource_name: str, keep_trailing_newlines: bool = False) -> jinja2.Template:
    content = sublime.load_resource(f"Packages/{PACKAGE_NAME}/plugin/templates/{resource_name}")
    return load_string_template(content, keep_trailing_newlines)
