from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['CoqLexer', 'IsabelleLexer', 'LeanLexer']

class CoqLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    keywords1: Incomplete
    keywords2: Incomplete
    keywords3: Incomplete
    keywords4: Incomplete
    keywords5: Incomplete
    keywords6: Incomplete
    keyopts: Incomplete
    operators: str
    word_operators: Incomplete
    prefix_syms: str
    infix_syms: str
    primitives: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class IsabelleLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    keyword_minor: Incomplete
    keyword_diag: Incomplete
    keyword_thy: Incomplete
    keyword_section: Incomplete
    keyword_subsection: Incomplete
    keyword_theory_decl: Incomplete
    keyword_theory_script: Incomplete
    keyword_theory_goal: Incomplete
    keyword_qed: Incomplete
    keyword_abandon_proof: Incomplete
    keyword_proof_goal: Incomplete
    keyword_proof_block: Incomplete
    keyword_proof_chain: Incomplete
    keyword_proof_decl: Incomplete
    keyword_proof_asm: Incomplete
    keyword_proof_asm_goal: Incomplete
    keyword_proof_script: Incomplete
    operators: Incomplete
    proof_operators: Incomplete
    tokens: Incomplete

class LeanLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    keywords1: Incomplete
    keywords2: Incomplete
    keywords3: Incomplete
    operators: Incomplete
    punctuation: Incomplete
    tokens: Incomplete
