from .actionscript import ActionScript3Lexer as ActionScript3Lexer, ActionScriptLexer as ActionScriptLexer, MxmlLexer as MxmlLexer
from .css import CssLexer as CssLexer, SassLexer as SassLexer, ScssLexer as ScssLexer
from .data import JsonLexer as JsonLexer
from .html import DtdLexer as DtdLexer, HamlLexer as HamlLexer, HtmlLexer as HtmlLexer, JadeLexer as JadeLexer, ScamlLexer as ScamlLexer, XmlLexer as XmlLexer, XsltLexer as XsltLexer
from .javascript import CoffeeScriptLexer as CoffeeScriptLexer, DartLexer as DartLexer, JavascriptLexer as JavascriptLexer, LassoLexer as LassoLexer, LiveScriptLexer as LiveScriptLexer, ObjectiveJLexer as ObjectiveJLexer, TypeScriptLexer as TypeScriptLexer
from .php import PhpLexer as PhpLexer
from .webmisc import DuelLexer as DuelLexer, QmlLexer as QmlLexer, SlimLexer as SlimLexer, XQueryLexer as XQueryLexer

JSONLexer = JsonLexer
