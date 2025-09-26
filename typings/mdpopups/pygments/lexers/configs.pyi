from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['IniLexer', 'RegeditLexer', 'PropertiesLexer', 'KconfigLexer', 'Cfengine3Lexer', 'ApacheConfLexer', 'SquidConfLexer', 'NginxConfLexer', 'LighttpdConfLexer', 'DockerLexer']

class IniLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class RegeditLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class PropertiesLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class KconfigLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: int
    def call_indent(level): ...
    def do_indent(level): ...
    tokens: Incomplete

class Cfengine3Lexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class ApacheConfLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class SquidConfLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    keywords: Incomplete
    opts: Incomplete
    actions: Incomplete
    actions_stats: Incomplete
    actions_log: Incomplete
    acls: Incomplete
    ip_re: str
    tokens: Incomplete

class NginxConfLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class LighttpdConfLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class DockerLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
