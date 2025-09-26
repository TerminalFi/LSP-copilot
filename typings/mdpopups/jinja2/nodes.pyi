from ._compat import PY2 as PY2, izip as izip, text_type as text_type, with_metaclass as with_metaclass
from .utils import Markup as Markup
from _typeshed import Incomplete
from collections.abc import Generator

class Impossible(Exception): ...

class NodeType(type):
    def __new__(cls, name, bases, d): ...

class EvalContext:
    environment: Incomplete
    autoescape: Incomplete
    volatile: bool
    def __init__(self, environment, template_name: Incomplete | None = None) -> None: ...
    def save(self): ...
    def revert(self, old) -> None: ...

def get_eval_context(node, ctx): ...

class Node(Incomplete):
    fields: Incomplete
    attributes: Incomplete
    abstract: bool
    def __init__(self, *fields, **attributes) -> None: ...
    def iter_fields(self, exclude: Incomplete | None = None, only: Incomplete | None = None) -> Generator[Incomplete]: ...
    def iter_child_nodes(self, exclude: Incomplete | None = None, only: Incomplete | None = None) -> Generator[Incomplete]: ...
    def find(self, node_type): ...
    def find_all(self, node_type) -> Generator[Incomplete]: ...
    def set_ctx(self, ctx): ...
    def set_lineno(self, lineno, override: bool = False): ...
    def set_environment(self, environment): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    __hash__: Incomplete
    def dump(self): ...

class Stmt(Node):
    abstract: bool

class Helper(Node):
    abstract: bool

class Template(Node):
    fields: Incomplete

class Output(Stmt):
    fields: Incomplete

class Extends(Stmt):
    fields: Incomplete

class For(Stmt):
    fields: Incomplete

class If(Stmt):
    fields: Incomplete

class Macro(Stmt):
    fields: Incomplete

class CallBlock(Stmt):
    fields: Incomplete

class FilterBlock(Stmt):
    fields: Incomplete

class With(Stmt):
    fields: Incomplete

class Block(Stmt):
    fields: Incomplete

class Include(Stmt):
    fields: Incomplete

class Import(Stmt):
    fields: Incomplete

class FromImport(Stmt):
    fields: Incomplete

class ExprStmt(Stmt):
    fields: Incomplete

class Assign(Stmt):
    fields: Incomplete

class AssignBlock(Stmt):
    fields: Incomplete

class Expr(Node):
    abstract: bool
    def as_const(self, eval_ctx: Incomplete | None = None) -> None: ...
    def can_assign(self): ...

class BinExpr(Expr):
    fields: Incomplete
    operator: Incomplete
    abstract: bool
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class UnaryExpr(Expr):
    fields: Incomplete
    operator: Incomplete
    abstract: bool
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Name(Expr):
    fields: Incomplete
    def can_assign(self): ...

class NSRef(Expr):
    fields: Incomplete
    def can_assign(self): ...

class Literal(Expr):
    abstract: bool

class Const(Literal):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...
    @classmethod
    def from_untrusted(cls, value, lineno: Incomplete | None = None, environment: Incomplete | None = None): ...

class TemplateData(Literal):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Tuple(Literal):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...
    def can_assign(self): ...

class List(Literal):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Dict(Literal):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Pair(Helper):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Keyword(Helper):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class CondExpr(Expr):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

def args_as_const(node, eval_ctx): ...

class Filter(Expr):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Test(Expr):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Call(Expr):
    fields: Incomplete

class Getitem(Expr):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...
    def can_assign(self): ...

class Getattr(Expr):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...
    def can_assign(self): ...

class Slice(Expr):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Concat(Expr):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Compare(Expr):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Operand(Helper):
    fields: Incomplete

class Mul(BinExpr):
    operator: str

class Div(BinExpr):
    operator: str

class FloorDiv(BinExpr):
    operator: str

class Add(BinExpr):
    operator: str

class Sub(BinExpr):
    operator: str

class Mod(BinExpr):
    operator: str

class Pow(BinExpr):
    operator: str

class And(BinExpr):
    operator: str
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Or(BinExpr):
    operator: str
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class Not(UnaryExpr):
    operator: str

class Neg(UnaryExpr):
    operator: str

class Pos(UnaryExpr):
    operator: str

class EnvironmentAttribute(Expr):
    fields: Incomplete

class ExtensionAttribute(Expr):
    fields: Incomplete

class ImportedName(Expr):
    fields: Incomplete

class InternalName(Expr):
    fields: Incomplete
    def __init__(self) -> None: ...

class MarkSafe(Expr):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class MarkSafeIfAutoescape(Expr):
    fields: Incomplete
    def as_const(self, eval_ctx: Incomplete | None = None): ...

class ContextReference(Expr): ...
class Continue(Stmt): ...
class Break(Stmt): ...

class Scope(Stmt):
    fields: Incomplete

class OverlayScope(Stmt):
    fields: Incomplete

class EvalContextModifier(Stmt):
    fields: Incomplete

class ScopedEvalContextModifier(EvalContextModifier):
    fields: Incomplete
