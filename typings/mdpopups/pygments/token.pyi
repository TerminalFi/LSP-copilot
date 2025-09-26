from _typeshed import Incomplete

class _TokenType(tuple):
    parent: Incomplete
    def split(self): ...
    subtypes: Incomplete
    def __init__(self, *args) -> None: ...
    def __contains__(self, val) -> bool: ...
    def __getattr__(self, val): ...

Token: Incomplete
Text: Incomplete
Whitespace: Incomplete
Escape: Incomplete
Error: Incomplete
Other: Incomplete
Keyword: Incomplete
Name: Incomplete
Literal: Incomplete
String: Incomplete
Number: Incomplete
Punctuation: Incomplete
Operator: Incomplete
Comment: Incomplete
Generic: Incomplete

def is_token_subtype(ttype, other): ...
def string_to_tokentype(s): ...

STANDARD_TYPES: Incomplete
