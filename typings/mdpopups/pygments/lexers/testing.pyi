from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['GherkinLexer']

class GherkinLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    feature_keywords: str
    feature_element_keywords: str
    examples_keywords: str
    step_keywords: str
    tokens: Incomplete
