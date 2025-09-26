from . import nodes as nodes
from ._compat import text_type as text_type
from .compiler import CodeGenerator as CodeGenerator, has_safe_repr as has_safe_repr
from .environment import Environment as Environment, Template as Template
from .utils import concat as concat, escape as escape

def native_concat(nodes): ...

class NativeCodeGenerator(CodeGenerator):
    def visit_Output(self, node, frame): ...

class NativeTemplate(Template):
    def render(self, *args, **kwargs): ...

class NativeEnvironment(Environment):
    code_generator_class = NativeCodeGenerator
    template_class = NativeTemplate
