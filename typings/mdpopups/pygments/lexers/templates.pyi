from ..lexer import DelegatingLexer, Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['HtmlPhpLexer', 'XmlPhpLexer', 'CssPhpLexer', 'JavascriptPhpLexer', 'ErbLexer', 'RhtmlLexer', 'XmlErbLexer', 'CssErbLexer', 'JavascriptErbLexer', 'SmartyLexer', 'HtmlSmartyLexer', 'XmlSmartyLexer', 'CssSmartyLexer', 'JavascriptSmartyLexer', 'DjangoLexer', 'HtmlDjangoLexer', 'CssDjangoLexer', 'XmlDjangoLexer', 'JavascriptDjangoLexer', 'GenshiLexer', 'HtmlGenshiLexer', 'GenshiTextLexer', 'CssGenshiLexer', 'JavascriptGenshiLexer', 'MyghtyLexer', 'MyghtyHtmlLexer', 'MyghtyXmlLexer', 'MyghtyCssLexer', 'MyghtyJavascriptLexer', 'MasonLexer', 'MakoLexer', 'MakoHtmlLexer', 'MakoXmlLexer', 'MakoJavascriptLexer', 'MakoCssLexer', 'JspLexer', 'CheetahLexer', 'CheetahHtmlLexer', 'CheetahXmlLexer', 'CheetahJavascriptLexer', 'EvoqueLexer', 'EvoqueHtmlLexer', 'EvoqueXmlLexer', 'ColdfusionLexer', 'ColdfusionHtmlLexer', 'ColdfusionCFCLexer', 'VelocityLexer', 'VelocityHtmlLexer', 'VelocityXmlLexer', 'SspLexer', 'TeaTemplateLexer', 'LassoHtmlLexer', 'LassoXmlLexer', 'LassoCssLexer', 'LassoJavascriptLexer', 'HandlebarsLexer', 'HandlebarsHtmlLexer', 'YamlJinjaLexer', 'LiquidLexer', 'TwigLexer', 'TwigHtmlLexer']

class ErbLexer(Lexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    ruby_lexer: Incomplete
    def __init__(self, **options) -> None: ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
    def analyse_text(text): ...

class SmartyLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class VelocityLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    flags: Incomplete
    identifier: str
    tokens: Incomplete
    def analyse_text(text): ...

class VelocityHtmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class VelocityXmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class DjangoLexer(RegexLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class MyghtyLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class MyghtyHtmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class MyghtyXmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class MyghtyJavascriptLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class MyghtyCssLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class MasonLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class MakoLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class MakoHtmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class MakoXmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class MakoJavascriptLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class MakoCssLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class CheetahPythonLexer(Lexer):
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class CheetahLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class CheetahHtmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class CheetahXmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class CheetahJavascriptLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class GenshiTextLexer(RegexLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class GenshiMarkupLexer(RegexLexer):
    flags: Incomplete
    tokens: Incomplete

class HtmlGenshiLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class GenshiLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class JavascriptGenshiLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class CssGenshiLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class RhtmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class XmlErbLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class CssErbLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class JavascriptErbLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class HtmlPhpLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class XmlPhpLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class CssPhpLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class JavascriptPhpLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class HtmlSmartyLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class XmlSmartyLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class CssSmartyLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class JavascriptSmartyLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class HtmlDjangoLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class XmlDjangoLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class CssDjangoLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class JavascriptDjangoLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class JspRootLexer(RegexLexer):
    tokens: Incomplete

class JspLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class EvoqueLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class EvoqueHtmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class EvoqueXmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class ColdfusionLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class ColdfusionMarkupLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class ColdfusionHtmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class ColdfusionCFCLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class SspLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class TeaTemplateRootLexer(RegexLexer):
    tokens: Incomplete

class TeaTemplateLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class LassoHtmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class LassoXmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class LassoCssLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class LassoJavascriptLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    alias_filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class HandlebarsLexer(RegexLexer):
    name: str
    aliases: Incomplete
    tokens: Incomplete

class HandlebarsHtmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class YamlJinjaLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class LiquidLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete

class TwigLexer(RegexLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class TwigHtmlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
