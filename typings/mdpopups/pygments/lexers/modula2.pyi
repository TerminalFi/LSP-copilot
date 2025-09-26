from ..lexer import RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['Modula2Lexer']

class Modula2Lexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
    common_reserved_words: Incomplete
    common_builtins: Incomplete
    common_pseudo_builtins: Incomplete
    pim_lexemes_to_reject: Incomplete
    pim_additional_reserved_words: Incomplete
    pim_additional_builtins: Incomplete
    pim_additional_pseudo_builtins: Incomplete
    iso_lexemes_to_reject: Incomplete
    iso_additional_reserved_words: Incomplete
    iso_additional_builtins: Incomplete
    iso_additional_pseudo_builtins: Incomplete
    m2r10_lexemes_to_reject: Incomplete
    m2r10_additional_reserved_words: Incomplete
    m2r10_additional_builtins: Incomplete
    m2r10_additional_pseudo_builtins: Incomplete
    objm2_lexemes_to_reject: Incomplete
    objm2_additional_reserved_words: Incomplete
    objm2_additional_builtins: Incomplete
    objm2_additional_pseudo_builtins: Incomplete
    aglet_additional_reserved_words: Incomplete
    aglet_additional_builtins: Incomplete
    aglet_additional_pseudo_builtins: Incomplete
    gm2_additional_reserved_words: Incomplete
    gm2_additional_builtins: Incomplete
    gm2_additional_pseudo_builtins: Incomplete
    p1_additional_reserved_words: Incomplete
    p1_additional_builtins: Incomplete
    p1_additional_pseudo_builtins: Incomplete
    xds_additional_reserved_words: Incomplete
    xds_additional_builtins: Incomplete
    xds_additional_pseudo_builtins: Incomplete
    pim_stdlib_module_identifiers: Incomplete
    pim_stdlib_type_identifiers: Incomplete
    pim_stdlib_proc_identifiers: Incomplete
    pim_stdlib_var_identifiers: Incomplete
    pim_stdlib_const_identifiers: Incomplete
    iso_stdlib_module_identifiers: Incomplete
    iso_stdlib_type_identifiers: Incomplete
    iso_stdlib_proc_identifiers: Incomplete
    iso_stdlib_var_identifiers: Incomplete
    iso_stdlib_const_identifiers: Incomplete
    m2r10_stdlib_adt_identifiers: Incomplete
    m2r10_stdlib_blueprint_identifiers: Incomplete
    m2r10_stdlib_module_identifiers: Incomplete
    m2r10_stdlib_type_identifiers: Incomplete
    m2r10_stdlib_proc_identifiers: Incomplete
    m2r10_stdlib_var_identifiers: Incomplete
    m2r10_stdlib_const_identifiers: Incomplete
    dialects: Incomplete
    lexemes_to_reject_db: Incomplete
    reserved_words_db: Incomplete
    builtins_db: Incomplete
    pseudo_builtins_db: Incomplete
    stdlib_adts_db: Incomplete
    stdlib_modules_db: Incomplete
    stdlib_types_db: Incomplete
    stdlib_procedures_db: Incomplete
    stdlib_variables_db: Incomplete
    stdlib_constants_db: Incomplete
    dialect_set_by_tag: bool
    algol_publication_mode: bool
    treat_stdlib_adts_as_builtins: Incomplete
    def __init__(self, **options) -> None: ...
    dialect: Incomplete
    lexemes_to_reject: Incomplete
    reserved_words: Incomplete
    builtins: Incomplete
    pseudo_builtins: Incomplete
    adts: Incomplete
    modules: Incomplete
    types: Incomplete
    procedures: Incomplete
    variables: Incomplete
    constants: Incomplete
    def set_dialect(self, dialect_id) -> None: ...
    def get_dialect_from_dialect_tag(self, dialect_tag): ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
