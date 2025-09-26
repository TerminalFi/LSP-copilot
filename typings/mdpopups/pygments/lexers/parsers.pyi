from ..lexer import DelegatingLexer, RegexLexer
from _typeshed import Incomplete

__all__ = ['RagelLexer', 'RagelEmbeddedLexer', 'RagelCLexer', 'RagelDLexer', 'RagelCppLexer', 'RagelObjectiveCLexer', 'RagelRubyLexer', 'RagelJavaLexer', 'AntlrLexer', 'AntlrPythonLexer', 'AntlrPerlLexer', 'AntlrRubyLexer', 'AntlrCppLexer', 'AntlrCSharpLexer', 'AntlrObjectiveCLexer', 'AntlrJavaLexer', 'AntlrActionScriptLexer', 'TreetopLexer', 'EbnfLexer']

class RagelLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete

class RagelEmbeddedLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class RagelRubyLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class RagelCLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class RagelDLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class RagelCppLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class RagelObjectiveCLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class RagelJavaLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class AntlrLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class AntlrCppLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class AntlrObjectiveCLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class AntlrCSharpLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class AntlrPythonLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class AntlrJavaLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class AntlrRubyLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class AntlrPerlLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class AntlrActionScriptLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class TreetopBaseLexer(RegexLexer):
    tokens: Incomplete

class TreetopLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def __init__(self, **options) -> None: ...

class EbnfLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
