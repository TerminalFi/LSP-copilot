from . import nodes as nodes
from .visitor import NodeTransformer as NodeTransformer
from _typeshed import Incomplete

def optimize(node, environment): ...

class Optimizer(NodeTransformer):
    environment: Incomplete
    def __init__(self, environment) -> None: ...
    def fold(self, node, eval_ctx: Incomplete | None = None): ...
    visit_Add = fold
    visit_Sub = fold
    visit_Mul = fold
    visit_Div = fold
    visit_FloorDiv = fold
    visit_Pow = fold
    visit_Mod = fold
    visit_And = fold
    visit_Or = fold
    visit_Pos = fold
    visit_Neg = fold
    visit_Not = fold
    visit_Compare = fold
    visit_Getitem = fold
    visit_Getattr = fold
    visit_Call = fold
    visit_Filter = fold
    visit_Test = fold
    visit_CondExpr = fold
