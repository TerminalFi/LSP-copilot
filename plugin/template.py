from __future__ import annotations

from functools import lru_cache
from typing import Any

import jinja2

JINJA_TEMPLATE_ENV = jinja2.Environment(
    extensions=[
        "jinja2.ext.do",
        "jinja2.ext.loopcontrols",
    ],
)


@lru_cache
def create_template(template: str) -> jinja2.Template:
    return JINJA_TEMPLATE_ENV.from_string(template)


def render_template(template: str, variables: dict[str, Any]) -> str:
    return create_template(template).render(variables)
