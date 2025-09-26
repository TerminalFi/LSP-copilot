from ..lexer import Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['JavaLexer', 'ScalaLexer', 'GosuLexer', 'GosuTemplateLexer', 'GroovyLexer', 'IokeLexer', 'ClojureLexer', 'ClojureScriptLexer', 'KotlinLexer', 'XtendLexer', 'AspectJLexer', 'CeylonLexer', 'PigLexer', 'GoloLexer', 'JasminLexer']

class JavaLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class AspectJLexer(JavaLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    aj_keywords: Incomplete
    aj_inter_type: Incomplete
    aj_inter_type_annotation: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class ScalaLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    op: str
    letter: str
    upper: str
    idrest: Incomplete
    letter_letter_digit: Incomplete
    tokens: Incomplete

class GosuLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class GosuTemplateLexer(Lexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class GroovyLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class IokeLexer(RegexLexer):
    name: str
    filenames: Incomplete
    aliases: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class ClojureLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    special_forms: Incomplete
    declarations: Incomplete
    builtins: Incomplete
    valid_name: str
    tokens: Incomplete

class ClojureScriptLexer(ClojureLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete

class TeaLangLexer(RegexLexer):
    flags: Incomplete
    tokens: Incomplete

class CeylonLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class KotlinLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    kt_name: Incomplete
    kt_id: Incomplete
    tokens: Incomplete

class XtendLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class PigLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class GoloLexer(RegexLexer):
    name: str
    filenames: Incomplete
    aliases: Incomplete
    tokens: Incomplete

class JasminLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...
