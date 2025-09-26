from ..markdown import Extension as Extension
from ..markdown.preprocessors import Preprocessor as Preprocessor
from _typeshed import Incomplete

class SnippetPreprocessor(Preprocessor):
    RE_ALL_SNIPPETS: Incomplete
    RE_SNIPPET: Incomplete
    base_path: Incomplete
    encoding: Incomplete
    check_paths: Incomplete
    tab_length: Incomplete
    def __init__(self, config, md) -> None: ...
    def parse_snippets(self, lines, file_name: Incomplete | None = None): ...
    seen: Incomplete
    def run(self, lines): ...

class SnippetExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    md: Incomplete
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
