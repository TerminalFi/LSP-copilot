import sublime
from .typing import StrEnum as StrEnum
from _typeshed import Incomplete
from enum import IntEnum, IntFlag
from typing import Any, Generic, Iterable, Literal, Mapping, TypeVar
from typing_extensions import NotRequired, TypedDict

INT_MAX: Incomplete
UINT_MAX = INT_MAX
URI = str
DocumentUri = str
Uint = int
RegExp = str

class SemanticTokenTypes(StrEnum):
    Namespace = 'namespace'
    Type = 'type'
    Class = 'class'
    Enum = 'enum'
    Interface = 'interface'
    Struct = 'struct'
    TypeParameter = 'typeParameter'
    Parameter = 'parameter'
    Variable = 'variable'
    Property = 'property'
    EnumMember = 'enumMember'
    Event = 'event'
    Function = 'function'
    Method = 'method'
    Macro = 'macro'
    Keyword = 'keyword'
    Modifier = 'modifier'
    Comment = 'comment'
    String = 'string'
    Number = 'number'
    Regexp = 'regexp'
    Operator = 'operator'
    Decorator = 'decorator'
    Label = 'label'

class SemanticTokenModifiers(StrEnum):
    Declaration = 'declaration'
    Definition = 'definition'
    Readonly = 'readonly'
    Static = 'static'
    Deprecated = 'deprecated'
    Abstract = 'abstract'
    Async = 'async'
    Modification = 'modification'
    Documentation = 'documentation'
    DefaultLibrary = 'defaultLibrary'

class DocumentDiagnosticReportKind(StrEnum):
    Full = 'full'
    Unchanged = 'unchanged'

class ErrorCodes(IntEnum):
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001

class LSPErrorCodes(IntEnum):
    RequestFailed = -32803
    ServerCancelled = -32802
    ContentModified = -32801
    RequestCancelled = -32800

class FoldingRangeKind(StrEnum):
    Comment = 'comment'
    Imports = 'imports'
    Region = 'region'

class SymbolKind(IntEnum):
    File = 1
    Module = 2
    Namespace = 3
    Package = 4
    Class = 5
    Method = 6
    Property = 7
    Field = 8
    Constructor = 9
    Enum = 10
    Interface = 11
    Function = 12
    Variable = 13
    Constant = 14
    String = 15
    Number = 16
    Boolean = 17
    Array = 18
    Object = 19
    Key = 20
    Null = 21
    EnumMember = 22
    Struct = 23
    Event = 24
    Operator = 25
    TypeParameter = 26

class SymbolTag(IntEnum):
    Deprecated = 1

class UniquenessLevel(StrEnum):
    Document = 'document'
    Project = 'project'
    Group = 'group'
    Scheme = 'scheme'
    Global = 'global'

class MonikerKind(StrEnum):
    Import = 'import'
    Export = 'export'
    Local = 'local'

class InlayHintKind(IntEnum):
    Type = 1
    Parameter = 2

class MessageType(IntEnum):
    Error = 1
    Warning = 2
    Info = 3
    Log = 4
    Debug = 5

class TextDocumentSyncKind(IntEnum):
    None_ = 0
    Full = 1
    Incremental = 2

class TextDocumentSaveReason(IntEnum):
    Manual = 1
    AfterDelay = 2
    FocusOut = 3

class CompletionItemKind(IntEnum):
    Text = 1
    Method = 2
    Function = 3
    Constructor = 4
    Field = 5
    Variable = 6
    Class = 7
    Interface = 8
    Module = 9
    Property = 10
    Unit = 11
    Value = 12
    Enum = 13
    Keyword = 14
    Snippet = 15
    Color = 16
    File = 17
    Reference = 18
    Folder = 19
    EnumMember = 20
    Constant = 21
    Struct = 22
    Event = 23
    Operator = 24
    TypeParameter = 25

class CompletionItemTag(IntEnum):
    Deprecated = 1

class InsertTextFormat(IntEnum):
    PlainText = 1
    Snippet = 2

class InsertTextMode(IntEnum):
    AsIs = 1
    AdjustIndentation = 2

class DocumentHighlightKind(IntEnum):
    Text = 1
    Read = 2
    Write = 3

class CodeActionKind(StrEnum):
    Empty = ''
    QuickFix = 'quickfix'
    Refactor = 'refactor'
    RefactorExtract = 'refactor.extract'
    RefactorInline = 'refactor.inline'
    RefactorMove = 'refactor.move'
    RefactorRewrite = 'refactor.rewrite'
    Source = 'source'
    SourceOrganizeImports = 'source.organizeImports'
    SourceFixAll = 'source.fixAll'
    Notebook = 'notebook'

class CodeActionTag(IntEnum):
    LLMGenerated = 1

class TraceValue(StrEnum):
    Off = 'off'
    Messages = 'messages'
    Verbose = 'verbose'

class MarkupKind(StrEnum):
    PlainText = 'plaintext'
    Markdown = 'markdown'

class LanguageKind(StrEnum):
    ABAP = 'abap'
    WindowsBat = 'bat'
    BibTeX = 'bibtex'
    Clojure = 'clojure'
    Coffeescript = 'coffeescript'
    C = 'c'
    CPP = 'cpp'
    CSharp = 'csharp'
    CSS = 'css'
    D = 'd'
    Delphi = 'pascal'
    Diff = 'diff'
    Dart = 'dart'
    Dockerfile = 'dockerfile'
    Elixir = 'elixir'
    Erlang = 'erlang'
    FSharp = 'fsharp'
    GitCommit = 'git-commit'
    GitRebase = 'rebase'
    Go = 'go'
    Groovy = 'groovy'
    Handlebars = 'handlebars'
    Haskell = 'haskell'
    HTML = 'html'
    Ini = 'ini'
    Java = 'java'
    JavaScript = 'javascript'
    JavaScriptReact = 'javascriptreact'
    JSON = 'json'
    LaTeX = 'latex'
    Less = 'less'
    Lua = 'lua'
    Makefile = 'makefile'
    Markdown = 'markdown'
    ObjectiveC = 'objective-c'
    ObjectiveCPP = 'objective-cpp'
    Pascal = 'pascal'
    Perl = 'perl'
    Perl6 = 'perl6'
    PHP = 'php'
    Powershell = 'powershell'
    Pug = 'jade'
    Python = 'python'
    R = 'r'
    Razor = 'razor'
    Ruby = 'ruby'
    Rust = 'rust'
    SCSS = 'scss'
    SASS = 'sass'
    Scala = 'scala'
    ShaderLab = 'shaderlab'
    ShellScript = 'shellscript'
    SQL = 'sql'
    Swift = 'swift'
    TypeScript = 'typescript'
    TypeScriptReact = 'typescriptreact'
    TeX = 'tex'
    VisualBasic = 'vb'
    XML = 'xml'
    XSL = 'xsl'
    YAML = 'yaml'

class InlineCompletionTriggerKind(IntEnum):
    Invoked = 1
    Automatic = 2

class PositionEncodingKind(StrEnum):
    UTF8 = 'utf-8'
    UTF16 = 'utf-16'
    UTF32 = 'utf-32'

class FileChangeType(IntEnum):
    Created = 1
    Changed = 2
    Deleted = 3

class WatchKind(IntFlag):
    Create = 1
    Change = 2
    Delete = 4

class DiagnosticSeverity(IntEnum):
    Error = 1
    Warning = 2
    Information = 3
    Hint = 4

class DiagnosticTag(IntEnum):
    Unnecessary = 1
    Deprecated = 2

class CompletionTriggerKind(IntEnum):
    Invoked = 1
    TriggerCharacter = 2
    TriggerForIncompleteCompletions = 3

class ApplyKind(IntFlag):
    Replace = 1
    Merge = 2

class SignatureHelpTriggerKind(IntEnum):
    Invoked = 1
    TriggerCharacter = 2
    ContentChange = 3

class CodeActionTriggerKind(IntEnum):
    Invoked = 1
    Automatic = 2

class FileOperationPatternKind(StrEnum):
    File = 'file'
    Folder = 'folder'

class NotebookCellKind(IntEnum):
    Markup = 1
    Code = 2

class ResourceOperationKind(StrEnum):
    Create = 'create'
    Rename = 'rename'
    Delete = 'delete'

class FailureHandlingKind(StrEnum):
    Abort = 'abort'
    Transactional = 'transactional'
    TextOnlyTransactional = 'textOnlyTransactional'
    Undo = 'undo'

class PrepareSupportDefaultBehavior(IntEnum):
    Identifier = 1

class TokenFormat(StrEnum):
    Relative = 'relative'

Definition: Incomplete
DefinitionLink: str
LSPArray: Incomplete
LSPAny: Incomplete
Declaration: Incomplete
DeclarationLink: str
InlineValue: Incomplete
DocumentDiagnosticReport: Incomplete
PrepareRenameResult: Incomplete
DocumentSelector: Incomplete
ProgressToken = int | str
ChangeAnnotationIdentifier = str
WorkspaceDocumentDiagnosticReport: Incomplete
TextDocumentContentChangeEvent: Incomplete
MarkedString: Incomplete
DocumentFilter: Incomplete
LSPObject: Incomplete
GlobPattern: Incomplete
TextDocumentFilter: Incomplete
NotebookDocumentFilter: Incomplete
Pattern = str
RegularExpressionEngineKind = str

class ImplementationParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class Location(TypedDict):
    uri: DocumentUri
    range: Range

class ImplementationRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class TypeDefinitionParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class TypeDefinitionRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class WorkspaceFolder(TypedDict):
    uri: URI
    name: str

class DidChangeWorkspaceFoldersParams(TypedDict):
    event: WorkspaceFoldersChangeEvent

class ConfigurationParams(TypedDict):
    items: list['ConfigurationItem']

class DocumentColorParams(TypedDict):
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class ColorInformation(TypedDict):
    range: Range
    color: Color

class DocumentColorRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class ColorPresentationParams(TypedDict):
    textDocument: TextDocumentIdentifier
    color: Color
    range: Range
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class ColorPresentation(TypedDict):
    label: str
    textEdit: NotRequired['TextEdit']
    additionalTextEdits: NotRequired[list['TextEdit']]

class WorkDoneProgressOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class TextDocumentRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None

class FoldingRangeParams(TypedDict):
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class FoldingRange(TypedDict):
    startLine: Uint
    startCharacter: NotRequired[Uint]
    endLine: Uint
    endCharacter: NotRequired[Uint]
    kind: NotRequired['FoldingRangeKind']
    collapsedText: NotRequired[str]

class FoldingRangeRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class DeclarationParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class DeclarationRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class SelectionRangeParams(TypedDict):
    textDocument: TextDocumentIdentifier
    positions: list['Position']
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class SelectionRange(TypedDict):
    range: Range
    parent: NotRequired['SelectionRange']

class SelectionRangeRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class WorkDoneProgressCreateParams(TypedDict):
    token: ProgressToken

class WorkDoneProgressCancelParams(TypedDict):
    token: ProgressToken

class CallHierarchyPrepareParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class CallHierarchyItem(TypedDict):
    name: str
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    detail: NotRequired[str]
    uri: DocumentUri
    range: Range
    selectionRange: Range
    data: NotRequired['LSPAny']

class CallHierarchyRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class CallHierarchyIncomingCallsParams(TypedDict):
    item: CallHierarchyItem
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

CallHierarchyIncomingCall = TypedDict('CallHierarchyIncomingCall', {'from': 'CallHierarchyItem', 'fromRanges': list['Range']})

class CallHierarchyOutgoingCallsParams(TypedDict):
    item: CallHierarchyItem
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class CallHierarchyOutgoingCall(TypedDict):
    to: CallHierarchyItem
    fromRanges: list['Range']

class SemanticTokensParams(TypedDict):
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class SemanticTokens(TypedDict):
    resultId: NotRequired[str]
    data: list[Uint]

class SemanticTokensPartialResult(TypedDict):
    data: list[Uint]

class SemanticTokensRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    legend: SemanticTokensLegend
    range: NotRequired[bool | dict]
    full: NotRequired[bool | SemanticTokensFullDelta]
    id: NotRequired[str]

class SemanticTokensDeltaParams(TypedDict):
    textDocument: TextDocumentIdentifier
    previousResultId: str
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class SemanticTokensDelta(TypedDict):
    resultId: NotRequired[str]
    edits: list['SemanticTokensEdit']

class SemanticTokensDeltaPartialResult(TypedDict):
    edits: list['SemanticTokensEdit']

class SemanticTokensRangeParams(TypedDict):
    textDocument: TextDocumentIdentifier
    range: Range
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class ShowDocumentParams(TypedDict):
    uri: URI
    external: NotRequired[bool]
    takeFocus: NotRequired[bool]
    selection: NotRequired['Range']

class ShowDocumentResult(TypedDict):
    success: bool

class LinkedEditingRangeParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class LinkedEditingRanges(TypedDict):
    ranges: list['Range']
    wordPattern: NotRequired[str]

class LinkedEditingRangeRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class CreateFilesParams(TypedDict):
    files: list['FileCreate']

class WorkspaceEdit(TypedDict):
    changes: NotRequired[dict['DocumentUri', list['TextEdit']]]
    documentChanges: NotRequired[list[TextDocumentEdit | CreateFile | RenameFile | DeleteFile]]
    changeAnnotations: NotRequired[dict['ChangeAnnotationIdentifier', 'ChangeAnnotation']]

class FileOperationRegistrationOptions(TypedDict):
    filters: list['FileOperationFilter']

class RenameFilesParams(TypedDict):
    files: list['FileRename']

class DeleteFilesParams(TypedDict):
    files: list['FileDelete']

class MonikerParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class Moniker(TypedDict):
    scheme: str
    identifier: str
    unique: UniquenessLevel
    kind: NotRequired['MonikerKind']

class MonikerRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None

class TypeHierarchyPrepareParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class TypeHierarchyItem(TypedDict):
    name: str
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    detail: NotRequired[str]
    uri: DocumentUri
    range: Range
    selectionRange: Range
    data: NotRequired['LSPAny']

class TypeHierarchyRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class TypeHierarchySupertypesParams(TypedDict):
    item: TypeHierarchyItem
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class TypeHierarchySubtypesParams(TypedDict):
    item: TypeHierarchyItem
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class InlineValueParams(TypedDict):
    textDocument: TextDocumentIdentifier
    range: Range
    context: InlineValueContext
    workDoneToken: NotRequired['ProgressToken']

class InlineValueRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class InlayHintParams(TypedDict):
    textDocument: TextDocumentIdentifier
    range: Range
    workDoneToken: NotRequired['ProgressToken']

class InlayHint(TypedDict):
    position: Position
    label: str | list['InlayHintLabelPart']
    kind: NotRequired['InlayHintKind']
    textEdits: NotRequired[list['TextEdit']]
    tooltip: NotRequired[str | MarkupContent]
    paddingLeft: NotRequired[bool]
    paddingRight: NotRequired[bool]
    data: NotRequired['LSPAny']

class InlayHintRegistrationOptions(TypedDict):
    resolveProvider: NotRequired[bool]
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class DocumentDiagnosticParams(TypedDict):
    textDocument: TextDocumentIdentifier
    identifier: NotRequired[str]
    previousResultId: NotRequired[str]
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class DocumentDiagnosticReportPartialResult(TypedDict):
    relatedDocuments: dict['DocumentUri', FullDocumentDiagnosticReport | UnchangedDocumentDiagnosticReport]

class DiagnosticServerCancellationData(TypedDict):
    retriggerRequest: bool

class DiagnosticRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    identifier: NotRequired[str]
    interFileDependencies: bool
    workspaceDiagnostics: bool
    id: NotRequired[str]

class WorkspaceDiagnosticParams(TypedDict):
    identifier: NotRequired[str]
    previousResultIds: list['PreviousResultId']
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class WorkspaceDiagnosticReport(TypedDict):
    items: list['WorkspaceDocumentDiagnosticReport']

class WorkspaceDiagnosticReportPartialResult(TypedDict):
    items: list['WorkspaceDocumentDiagnosticReport']

class DidOpenNotebookDocumentParams(TypedDict):
    notebookDocument: NotebookDocument
    cellTextDocuments: list['TextDocumentItem']

class NotebookDocumentSyncRegistrationOptions(TypedDict):
    notebookSelector: list[NotebookDocumentFilterWithNotebook | NotebookDocumentFilterWithCells]
    save: NotRequired[bool]
    id: NotRequired[str]

class DidChangeNotebookDocumentParams(TypedDict):
    notebookDocument: VersionedNotebookDocumentIdentifier
    change: NotebookDocumentChangeEvent

class DidSaveNotebookDocumentParams(TypedDict):
    notebookDocument: NotebookDocumentIdentifier

class DidCloseNotebookDocumentParams(TypedDict):
    notebookDocument: NotebookDocumentIdentifier
    cellTextDocuments: list['TextDocumentIdentifier']

class InlineCompletionParams(TypedDict):
    context: InlineCompletionContext
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class InlineCompletionList(TypedDict):
    items: list['InlineCompletionItem']

class InlineCompletionItem(TypedDict):
    insertText: str | StringValue
    filterText: NotRequired[str]
    range: NotRequired['Range']
    command: NotRequired['Command']

class InlineCompletionRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class TextDocumentContentParams(TypedDict):
    uri: DocumentUri

class TextDocumentContentResult(TypedDict):
    text: str

class TextDocumentContentRegistrationOptions(TypedDict):
    schemes: list[str]
    id: NotRequired[str]

class TextDocumentContentRefreshParams(TypedDict):
    uri: DocumentUri

class RegistrationParams(TypedDict):
    registrations: list['Registration']

class UnregistrationParams(TypedDict):
    unregisterations: list['Unregistration']

class InitializeParams(TypedDict):
    processId: int | None
    clientInfo: NotRequired['ClientInfo']
    locale: NotRequired[str]
    rootPath: NotRequired[str | None]
    rootUri: DocumentUri | None
    capabilities: ClientCapabilities
    initializationOptions: NotRequired['LSPAny']
    trace: NotRequired['TraceValue']
    workspaceFolders: NotRequired[list['WorkspaceFolder'] | None]

class InitializeResult(TypedDict):
    capabilities: ServerCapabilities
    serverInfo: NotRequired['ServerInfo']

class InitializeError(TypedDict):
    retry: bool

class InitializedParams(TypedDict): ...

class DidChangeConfigurationParams(TypedDict):
    settings: LSPAny

class DidChangeConfigurationRegistrationOptions(TypedDict):
    section: NotRequired[str | list[str]]

class ShowMessageParams(TypedDict):
    type: MessageType
    message: str

class ShowMessageRequestParams(TypedDict):
    type: MessageType
    message: str
    actions: NotRequired[list['MessageActionItem']]

class MessageActionItem(TypedDict):
    title: str

class LogMessageParams(TypedDict):
    type: MessageType
    message: str

class DidOpenTextDocumentParams(TypedDict):
    textDocument: TextDocumentItem

class DidChangeTextDocumentParams(TypedDict):
    textDocument: VersionedTextDocumentIdentifier
    contentChanges: list['TextDocumentContentChangeEvent']

class TextDocumentChangeRegistrationOptions(TypedDict):
    syncKind: TextDocumentSyncKind
    documentSelector: DocumentSelector | None

class DidCloseTextDocumentParams(TypedDict):
    textDocument: TextDocumentIdentifier

class DidSaveTextDocumentParams(TypedDict):
    textDocument: TextDocumentIdentifier
    text: NotRequired[str]

class TextDocumentSaveRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    includeText: NotRequired[bool]

class WillSaveTextDocumentParams(TypedDict):
    textDocument: TextDocumentIdentifier
    reason: TextDocumentSaveReason

class TextEdit(TypedDict):
    range: Range
    newText: str

class DidChangeWatchedFilesParams(TypedDict):
    changes: list['FileEvent']

class DidChangeWatchedFilesRegistrationOptions(TypedDict):
    watchers: list['FileSystemWatcher']

class PublishDiagnosticsParams(TypedDict):
    uri: DocumentUri
    version: NotRequired[int]
    diagnostics: list['Diagnostic']

class CompletionParams(TypedDict):
    context: NotRequired['CompletionContext']
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class CompletionItem(TypedDict):
    label: str
    labelDetails: NotRequired['CompletionItemLabelDetails']
    kind: NotRequired['CompletionItemKind']
    tags: NotRequired[list['CompletionItemTag']]
    detail: NotRequired[str]
    documentation: NotRequired[str | MarkupContent]
    deprecated: NotRequired[bool]
    preselect: NotRequired[bool]
    sortText: NotRequired[str]
    filterText: NotRequired[str]
    insertText: NotRequired[str]
    insertTextFormat: NotRequired['InsertTextFormat']
    insertTextMode: NotRequired['InsertTextMode']
    textEdit: NotRequired[TextEdit | InsertReplaceEdit]
    textEditText: NotRequired[str]
    additionalTextEdits: NotRequired[list['TextEdit']]
    commitCharacters: NotRequired[list[str]]
    command: NotRequired['Command']
    data: NotRequired['LSPAny']

class CompletionList(TypedDict):
    isIncomplete: bool
    itemDefaults: NotRequired['CompletionItemDefaults']
    applyKind: NotRequired['CompletionItemApplyKinds']
    items: list['CompletionItem']

class CompletionRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    triggerCharacters: NotRequired[list[str]]
    allCommitCharacters: NotRequired[list[str]]
    resolveProvider: NotRequired[bool]
    completionItem: NotRequired['ServerCompletionItemOptions']

class HoverParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class Hover(TypedDict):
    contents: MarkupContent | MarkedString | list['MarkedString']
    range: NotRequired['Range']

class HoverRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None

class SignatureHelpParams(TypedDict):
    context: NotRequired['SignatureHelpContext']
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class SignatureHelp(TypedDict):
    signatures: list['SignatureInformation']
    activeSignature: NotRequired[Uint]
    activeParameter: NotRequired[Uint | None]

class SignatureHelpRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    triggerCharacters: NotRequired[list[str]]
    retriggerCharacters: NotRequired[list[str]]

class DefinitionParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class DefinitionRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None

class ReferenceParams(TypedDict):
    context: ReferenceContext
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class ReferenceRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None

class DocumentHighlightParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class DocumentHighlight(TypedDict):
    range: Range
    kind: NotRequired['DocumentHighlightKind']

class DocumentHighlightRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None

class DocumentSymbolParams(TypedDict):
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class SymbolInformation(TypedDict):
    deprecated: NotRequired[bool]
    location: Location
    name: str
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    containerName: NotRequired[str]

class DocumentSymbol(TypedDict):
    name: str
    detail: NotRequired[str]
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    deprecated: NotRequired[bool]
    range: Range
    selectionRange: Range
    children: NotRequired[list['DocumentSymbol']]

class DocumentSymbolRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    label: NotRequired[str]

class CodeActionParams(TypedDict):
    textDocument: TextDocumentIdentifier
    range: Range
    context: CodeActionContext
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class Command(TypedDict):
    title: str
    tooltip: NotRequired[str]
    command: str
    arguments: NotRequired[list['LSPAny']]

class CodeAction(TypedDict):
    title: str
    kind: NotRequired['CodeActionKind']
    diagnostics: NotRequired[list['Diagnostic']]
    isPreferred: NotRequired[bool]
    disabled: NotRequired['CodeActionDisabled']
    edit: NotRequired['WorkspaceEdit']
    command: NotRequired['Command']
    data: NotRequired['LSPAny']
    tags: NotRequired[list['CodeActionTag']]

class CodeActionRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    codeActionKinds: NotRequired[list['CodeActionKind']]
    documentation: NotRequired[list['CodeActionKindDocumentation']]
    resolveProvider: NotRequired[bool]

class WorkspaceSymbolParams(TypedDict):
    query: str
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class WorkspaceSymbol(TypedDict):
    location: Location | LocationUriOnly
    data: NotRequired['LSPAny']
    name: str
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    containerName: NotRequired[str]

class WorkspaceSymbolRegistrationOptions(TypedDict):
    resolveProvider: NotRequired[bool]

class CodeLensParams(TypedDict):
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class CodeLens(TypedDict):
    range: Range
    command: NotRequired['Command']
    data: NotRequired['LSPAny']

class CodeLensRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    resolveProvider: NotRequired[bool]

class DocumentLinkParams(TypedDict):
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class DocumentLink(TypedDict):
    range: Range
    target: NotRequired['URI']
    tooltip: NotRequired[str]
    data: NotRequired['LSPAny']

class DocumentLinkRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    resolveProvider: NotRequired[bool]

class DocumentFormattingParams(TypedDict):
    textDocument: TextDocumentIdentifier
    options: FormattingOptions
    workDoneToken: NotRequired['ProgressToken']

class DocumentFormattingRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None

class DocumentRangeFormattingParams(TypedDict):
    textDocument: TextDocumentIdentifier
    range: Range
    options: FormattingOptions
    workDoneToken: NotRequired['ProgressToken']

class DocumentRangeFormattingRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    rangesSupport: NotRequired[bool]

class DocumentRangesFormattingParams(TypedDict):
    textDocument: TextDocumentIdentifier
    ranges: list['Range']
    options: FormattingOptions
    workDoneToken: NotRequired['ProgressToken']

class DocumentOnTypeFormattingParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    ch: str
    options: FormattingOptions

class DocumentOnTypeFormattingRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    firstTriggerCharacter: str
    moreTriggerCharacter: NotRequired[list[str]]

class RenameParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    newName: str
    workDoneToken: NotRequired['ProgressToken']

class RenameRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    prepareProvider: NotRequired[bool]

class PrepareRenameParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class ExecuteCommandParams(TypedDict):
    command: str
    arguments: NotRequired[list['LSPAny']]
    workDoneToken: NotRequired['ProgressToken']

class ExecuteCommandRegistrationOptions(TypedDict):
    commands: list[str]

class ApplyWorkspaceEditParams(TypedDict):
    label: NotRequired[str]
    edit: WorkspaceEdit
    metadata: NotRequired['WorkspaceEditMetadata']

class ApplyWorkspaceEditResult(TypedDict):
    applied: bool
    failureReason: NotRequired[str]
    failedChange: NotRequired[Uint]

class WorkDoneProgressBegin(TypedDict):
    kind: Literal['begin']
    title: str
    cancellable: NotRequired[bool]
    message: NotRequired[str]
    percentage: NotRequired[Uint]

class WorkDoneProgressReport(TypedDict):
    kind: Literal['report']
    cancellable: NotRequired[bool]
    message: NotRequired[str]
    percentage: NotRequired[Uint]

class WorkDoneProgressEnd(TypedDict):
    kind: Literal['end']
    message: NotRequired[str]

class SetTraceParams(TypedDict):
    value: TraceValue

class LogTraceParams(TypedDict):
    message: str
    verbose: NotRequired[str]

class CancelParams(TypedDict):
    id: int | str

class ProgressParams(TypedDict):
    token: ProgressToken
    value: LSPAny

class TextDocumentPositionParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position

class WorkDoneProgressParams(TypedDict):
    workDoneToken: NotRequired['ProgressToken']

class PartialResultParams(TypedDict):
    partialResultToken: NotRequired['ProgressToken']

class LocationLink(TypedDict):
    originSelectionRange: NotRequired['Range']
    targetUri: DocumentUri
    targetRange: Range
    targetSelectionRange: Range

class Range(TypedDict):
    start: Position
    end: Position

class ImplementationOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class StaticRegistrationOptions(TypedDict):
    id: NotRequired[str]

class TypeDefinitionOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class WorkspaceFoldersChangeEvent(TypedDict):
    added: list['WorkspaceFolder']
    removed: list['WorkspaceFolder']

class ConfigurationItem(TypedDict):
    scopeUri: NotRequired['URI']
    section: NotRequired[str]

class TextDocumentIdentifier(TypedDict):
    uri: DocumentUri

class Color(TypedDict):
    red: float
    green: float
    blue: float
    alpha: float

class DocumentColorOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class FoldingRangeOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class DeclarationOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class Position(TypedDict):
    line: Uint
    character: Uint

class SelectionRangeOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class CallHierarchyOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class SemanticTokensOptions(TypedDict):
    legend: SemanticTokensLegend
    range: NotRequired[bool | dict]
    full: NotRequired[bool | SemanticTokensFullDelta]
    workDoneProgress: NotRequired[bool]

class SemanticTokensEdit(TypedDict):
    start: Uint
    deleteCount: Uint
    data: NotRequired[list[Uint]]

class LinkedEditingRangeOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class FileCreate(TypedDict):
    uri: str

class TextDocumentEdit(TypedDict):
    textDocument: OptionalVersionedTextDocumentIdentifier
    edits: list[TextEdit | AnnotatedTextEdit | SnippetTextEdit]

class CreateFile(TypedDict):
    kind: Literal['create']
    uri: DocumentUri
    options: NotRequired['CreateFileOptions']
    annotationId: NotRequired['ChangeAnnotationIdentifier']

class RenameFile(TypedDict):
    kind: Literal['rename']
    oldUri: DocumentUri
    newUri: DocumentUri
    options: NotRequired['RenameFileOptions']
    annotationId: NotRequired['ChangeAnnotationIdentifier']

class DeleteFile(TypedDict):
    kind: Literal['delete']
    uri: DocumentUri
    options: NotRequired['DeleteFileOptions']
    annotationId: NotRequired['ChangeAnnotationIdentifier']

class ChangeAnnotation(TypedDict):
    label: str
    needsConfirmation: NotRequired[bool]
    description: NotRequired[str]

class FileOperationFilter(TypedDict):
    scheme: NotRequired[str]
    pattern: FileOperationPattern

class FileRename(TypedDict):
    oldUri: str
    newUri: str

class FileDelete(TypedDict):
    uri: str

class MonikerOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class TypeHierarchyOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class InlineValueContext(TypedDict):
    frameId: int
    stoppedLocation: Range

class InlineValueText(TypedDict):
    range: Range
    text: str

class InlineValueVariableLookup(TypedDict):
    range: Range
    variableName: NotRequired[str]
    caseSensitiveLookup: bool

class InlineValueEvaluatableExpression(TypedDict):
    range: Range
    expression: NotRequired[str]

class InlineValueOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class InlayHintLabelPart(TypedDict):
    value: str
    tooltip: NotRequired[str | MarkupContent]
    location: NotRequired['Location']
    command: NotRequired['Command']

class MarkupContent(TypedDict):
    kind: MarkupKind
    value: str

class InlayHintOptions(TypedDict):
    resolveProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class RelatedFullDocumentDiagnosticReport(TypedDict):
    relatedDocuments: NotRequired[dict['DocumentUri', FullDocumentDiagnosticReport | UnchangedDocumentDiagnosticReport]]
    kind: Literal['full']
    resultId: NotRequired[str]
    items: list['Diagnostic']

class RelatedUnchangedDocumentDiagnosticReport(TypedDict):
    relatedDocuments: NotRequired[dict['DocumentUri', FullDocumentDiagnosticReport | UnchangedDocumentDiagnosticReport]]
    kind: Literal['unchanged']
    resultId: str

class FullDocumentDiagnosticReport(TypedDict):
    kind: Literal['full']
    resultId: NotRequired[str]
    items: list['Diagnostic']

class UnchangedDocumentDiagnosticReport(TypedDict):
    kind: Literal['unchanged']
    resultId: str

class DiagnosticOptions(TypedDict):
    identifier: NotRequired[str]
    interFileDependencies: bool
    workspaceDiagnostics: bool
    workDoneProgress: NotRequired[bool]

class PreviousResultId(TypedDict):
    uri: DocumentUri
    value: str

class NotebookDocument(TypedDict):
    uri: URI
    notebookType: str
    version: int
    metadata: NotRequired['LSPObject']
    cells: list['NotebookCell']

class TextDocumentItem(TypedDict):
    uri: DocumentUri
    languageId: LanguageKind
    version: int
    text: str

class NotebookDocumentSyncOptions(TypedDict):
    notebookSelector: list[NotebookDocumentFilterWithNotebook | NotebookDocumentFilterWithCells]
    save: NotRequired[bool]

class VersionedNotebookDocumentIdentifier(TypedDict):
    version: int
    uri: URI

class NotebookDocumentChangeEvent(TypedDict):
    metadata: NotRequired['LSPObject']
    cells: NotRequired['NotebookDocumentCellChanges']

class NotebookDocumentIdentifier(TypedDict):
    uri: URI

class InlineCompletionContext(TypedDict):
    triggerKind: InlineCompletionTriggerKind
    selectedCompletionInfo: NotRequired['SelectedCompletionInfo']

class StringValue(TypedDict):
    kind: Literal['snippet']
    value: str

class InlineCompletionOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class TextDocumentContentOptions(TypedDict):
    schemes: list[str]

class Registration(TypedDict):
    id: str
    method: str
    registerOptions: NotRequired['LSPAny']

class Unregistration(TypedDict):
    id: str
    method: str

class WorkspaceFoldersInitializeParams(TypedDict):
    workspaceFolders: NotRequired[list['WorkspaceFolder'] | None]

class ServerCapabilities(TypedDict):
    positionEncoding: NotRequired['PositionEncodingKind']
    textDocumentSync: NotRequired[TextDocumentSyncOptions | TextDocumentSyncKind]
    notebookDocumentSync: NotRequired[NotebookDocumentSyncOptions | NotebookDocumentSyncRegistrationOptions]
    completionProvider: NotRequired['CompletionOptions']
    hoverProvider: NotRequired[bool | HoverOptions]
    signatureHelpProvider: NotRequired['SignatureHelpOptions']
    declarationProvider: NotRequired[bool | DeclarationOptions | DeclarationRegistrationOptions]
    definitionProvider: NotRequired[bool | DefinitionOptions]
    typeDefinitionProvider: NotRequired[bool | TypeDefinitionOptions | TypeDefinitionRegistrationOptions]
    implementationProvider: NotRequired[bool | ImplementationOptions | ImplementationRegistrationOptions]
    referencesProvider: NotRequired[bool | ReferenceOptions]
    documentHighlightProvider: NotRequired[bool | DocumentHighlightOptions]
    documentSymbolProvider: NotRequired[bool | DocumentSymbolOptions]
    codeActionProvider: NotRequired[bool | CodeActionOptions]
    codeLensProvider: NotRequired['CodeLensOptions']
    documentLinkProvider: NotRequired['DocumentLinkOptions']
    colorProvider: NotRequired[bool | DocumentColorOptions | DocumentColorRegistrationOptions]
    workspaceSymbolProvider: NotRequired[bool | WorkspaceSymbolOptions]
    documentFormattingProvider: NotRequired[bool | DocumentFormattingOptions]
    documentRangeFormattingProvider: NotRequired[bool | DocumentRangeFormattingOptions]
    documentOnTypeFormattingProvider: NotRequired['DocumentOnTypeFormattingOptions']
    renameProvider: NotRequired[bool | RenameOptions]
    foldingRangeProvider: NotRequired[bool | FoldingRangeOptions | FoldingRangeRegistrationOptions]
    selectionRangeProvider: NotRequired[bool | SelectionRangeOptions | SelectionRangeRegistrationOptions]
    executeCommandProvider: NotRequired['ExecuteCommandOptions']
    callHierarchyProvider: NotRequired[bool | CallHierarchyOptions | CallHierarchyRegistrationOptions]
    linkedEditingRangeProvider: NotRequired[bool | LinkedEditingRangeOptions | LinkedEditingRangeRegistrationOptions]
    semanticTokensProvider: NotRequired[SemanticTokensOptions | SemanticTokensRegistrationOptions]
    monikerProvider: NotRequired[bool | MonikerOptions | MonikerRegistrationOptions]
    typeHierarchyProvider: NotRequired[bool | TypeHierarchyOptions | TypeHierarchyRegistrationOptions]
    inlineValueProvider: NotRequired[bool | InlineValueOptions | InlineValueRegistrationOptions]
    inlayHintProvider: NotRequired[bool | InlayHintOptions | InlayHintRegistrationOptions]
    diagnosticProvider: NotRequired[DiagnosticOptions | DiagnosticRegistrationOptions]
    inlineCompletionProvider: NotRequired[bool | InlineCompletionOptions]
    workspace: NotRequired['WorkspaceOptions']
    experimental: NotRequired['LSPAny']

class ServerInfo(TypedDict):
    name: str
    version: NotRequired[str]

class VersionedTextDocumentIdentifier(TypedDict):
    version: int
    uri: DocumentUri

class SaveOptions(TypedDict):
    includeText: NotRequired[bool]

class FileEvent(TypedDict):
    uri: DocumentUri
    type: FileChangeType

class FileSystemWatcher(TypedDict):
    globPattern: GlobPattern
    kind: NotRequired['WatchKind']

class Diagnostic(TypedDict):
    range: Range
    severity: NotRequired['DiagnosticSeverity']
    code: NotRequired[int | str]
    codeDescription: NotRequired['CodeDescription']
    source: NotRequired[str]
    message: str
    tags: NotRequired[list['DiagnosticTag']]
    relatedInformation: NotRequired[list['DiagnosticRelatedInformation']]
    data: NotRequired['LSPAny']

class CompletionContext(TypedDict):
    triggerKind: CompletionTriggerKind
    triggerCharacter: NotRequired[str]

class CompletionItemLabelDetails(TypedDict):
    detail: NotRequired[str]
    description: NotRequired[str]

class InsertReplaceEdit(TypedDict):
    newText: str
    insert: Range
    replace: Range

class CompletionItemDefaults(TypedDict):
    commitCharacters: NotRequired[list[str]]
    editRange: NotRequired[Range | EditRangeWithInsertReplace]
    insertTextFormat: NotRequired['InsertTextFormat']
    insertTextMode: NotRequired['InsertTextMode']
    data: NotRequired['LSPAny']

class CompletionItemApplyKinds(TypedDict):
    commitCharacters: NotRequired['ApplyKind']
    data: NotRequired['ApplyKind']

class CompletionOptions(TypedDict):
    triggerCharacters: NotRequired[list[str]]
    allCommitCharacters: NotRequired[list[str]]
    resolveProvider: NotRequired[bool]
    completionItem: NotRequired['ServerCompletionItemOptions']
    workDoneProgress: NotRequired[bool]

class HoverOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class SignatureHelpContext(TypedDict):
    triggerKind: SignatureHelpTriggerKind
    triggerCharacter: NotRequired[str]
    isRetrigger: bool
    activeSignatureHelp: NotRequired['SignatureHelp']

class SignatureInformation(TypedDict):
    label: str
    documentation: NotRequired[str | MarkupContent]
    parameters: NotRequired[list['ParameterInformation']]
    activeParameter: NotRequired[Uint | None]

class SignatureHelpOptions(TypedDict):
    triggerCharacters: NotRequired[list[str]]
    retriggerCharacters: NotRequired[list[str]]
    workDoneProgress: NotRequired[bool]

class DefinitionOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class ReferenceContext(TypedDict):
    includeDeclaration: bool

class ReferenceOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class DocumentHighlightOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class BaseSymbolInformation(TypedDict):
    name: str
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    containerName: NotRequired[str]

class DocumentSymbolOptions(TypedDict):
    label: NotRequired[str]
    workDoneProgress: NotRequired[bool]

class CodeActionContext(TypedDict):
    diagnostics: list['Diagnostic']
    only: NotRequired[list['CodeActionKind']]
    triggerKind: NotRequired['CodeActionTriggerKind']

class CodeActionDisabled(TypedDict):
    reason: str

class CodeActionOptions(TypedDict):
    codeActionKinds: NotRequired[list['CodeActionKind']]
    documentation: NotRequired[list['CodeActionKindDocumentation']]
    resolveProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class LocationUriOnly(TypedDict):
    uri: DocumentUri

class WorkspaceSymbolOptions(TypedDict):
    resolveProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class CodeLensOptions(TypedDict):
    resolveProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class DocumentLinkOptions(TypedDict):
    resolveProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class FormattingOptions(TypedDict):
    tabSize: Uint
    insertSpaces: bool
    trimTrailingWhitespace: NotRequired[bool]
    insertFinalNewline: NotRequired[bool]
    trimFinalNewlines: NotRequired[bool]

class DocumentFormattingOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class DocumentRangeFormattingOptions(TypedDict):
    rangesSupport: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class DocumentOnTypeFormattingOptions(TypedDict):
    firstTriggerCharacter: str
    moreTriggerCharacter: NotRequired[list[str]]

class RenameOptions(TypedDict):
    prepareProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class PrepareRenamePlaceholder(TypedDict):
    range: Range
    placeholder: str

class PrepareRenameDefaultBehavior(TypedDict):
    defaultBehavior: bool

class ExecuteCommandOptions(TypedDict):
    commands: list[str]
    workDoneProgress: NotRequired[bool]

class WorkspaceEditMetadata(TypedDict):
    isRefactoring: NotRequired[bool]

class SemanticTokensLegend(TypedDict):
    tokenTypes: list[str]
    tokenModifiers: list[str]

class SemanticTokensFullDelta(TypedDict):
    delta: NotRequired[bool]

class OptionalVersionedTextDocumentIdentifier(TypedDict):
    version: int | None
    uri: DocumentUri

class AnnotatedTextEdit(TypedDict):
    annotationId: ChangeAnnotationIdentifier
    range: Range
    newText: str

class SnippetTextEdit(TypedDict):
    range: Range
    snippet: StringValue
    annotationId: NotRequired['ChangeAnnotationIdentifier']

class ResourceOperation(TypedDict):
    kind: str
    annotationId: NotRequired['ChangeAnnotationIdentifier']

class CreateFileOptions(TypedDict):
    overwrite: NotRequired[bool]
    ignoreIfExists: NotRequired[bool]

class RenameFileOptions(TypedDict):
    overwrite: NotRequired[bool]
    ignoreIfExists: NotRequired[bool]

class DeleteFileOptions(TypedDict):
    recursive: NotRequired[bool]
    ignoreIfNotExists: NotRequired[bool]

class FileOperationPattern(TypedDict):
    glob: str
    matches: NotRequired['FileOperationPatternKind']
    options: NotRequired['FileOperationPatternOptions']

class WorkspaceFullDocumentDiagnosticReport(TypedDict):
    uri: DocumentUri
    version: int | None
    kind: Literal['full']
    resultId: NotRequired[str]
    items: list['Diagnostic']

class WorkspaceUnchangedDocumentDiagnosticReport(TypedDict):
    uri: DocumentUri
    version: int | None
    kind: Literal['unchanged']
    resultId: str

class NotebookCell(TypedDict):
    kind: NotebookCellKind
    document: DocumentUri
    metadata: NotRequired['LSPObject']
    executionSummary: NotRequired['ExecutionSummary']

class NotebookDocumentFilterWithNotebook(TypedDict):
    notebook: str | NotebookDocumentFilter
    cells: NotRequired[list['NotebookCellLanguage']]

class NotebookDocumentFilterWithCells(TypedDict):
    notebook: NotRequired[str | NotebookDocumentFilter]
    cells: list['NotebookCellLanguage']

class NotebookDocumentCellChanges(TypedDict):
    structure: NotRequired['NotebookDocumentCellChangeStructure']
    data: NotRequired[list['NotebookCell']]
    textContent: NotRequired[list['NotebookDocumentCellContentChanges']]

class SelectedCompletionInfo(TypedDict):
    range: Range
    text: str

class ClientInfo(TypedDict):
    name: str
    version: NotRequired[str]

class ClientCapabilities(TypedDict):
    workspace: NotRequired['WorkspaceClientCapabilities']
    textDocument: NotRequired['TextDocumentClientCapabilities']
    notebookDocument: NotRequired['NotebookDocumentClientCapabilities']
    window: NotRequired['WindowClientCapabilities']
    general: NotRequired['GeneralClientCapabilities']
    experimental: NotRequired['LSPAny']

class TextDocumentSyncOptions(TypedDict):
    openClose: NotRequired[bool]
    change: NotRequired['TextDocumentSyncKind']
    willSave: NotRequired[bool]
    willSaveWaitUntil: NotRequired[bool]
    save: NotRequired[bool | SaveOptions]

class WorkspaceOptions(TypedDict):
    workspaceFolders: NotRequired['WorkspaceFoldersServerCapabilities']
    fileOperations: NotRequired['FileOperationOptions']
    textDocumentContent: NotRequired[TextDocumentContentOptions | TextDocumentContentRegistrationOptions]

class TextDocumentContentChangePartial(TypedDict):
    range: Range
    rangeLength: NotRequired[Uint]
    text: str

class TextDocumentContentChangeWholeDocument(TypedDict):
    text: str

class CodeDescription(TypedDict):
    href: URI

class DiagnosticRelatedInformation(TypedDict):
    location: Location
    message: str

class EditRangeWithInsertReplace(TypedDict):
    insert: Range
    replace: Range

class ServerCompletionItemOptions(TypedDict):
    labelDetailsSupport: NotRequired[bool]

class MarkedStringWithLanguage(TypedDict):
    language: str
    value: str

class ParameterInformation(TypedDict):
    label: str | list[Uint | Uint]
    documentation: NotRequired[str | MarkupContent]

class CodeActionKindDocumentation(TypedDict):
    kind: CodeActionKind
    command: Command

class NotebookCellTextDocumentFilter(TypedDict):
    notebook: str | NotebookDocumentFilter
    language: NotRequired[str]

class FileOperationPatternOptions(TypedDict):
    ignoreCase: NotRequired[bool]

class ExecutionSummary(TypedDict):
    executionOrder: Uint
    success: NotRequired[bool]

class NotebookCellLanguage(TypedDict):
    language: str

class NotebookDocumentCellChangeStructure(TypedDict):
    array: NotebookCellArrayChange
    didOpen: NotRequired[list['TextDocumentItem']]
    didClose: NotRequired[list['TextDocumentIdentifier']]

class NotebookDocumentCellContentChanges(TypedDict):
    document: VersionedTextDocumentIdentifier
    changes: list['TextDocumentContentChangeEvent']

class WorkspaceClientCapabilities(TypedDict):
    applyEdit: NotRequired[bool]
    workspaceEdit: NotRequired['WorkspaceEditClientCapabilities']
    didChangeConfiguration: NotRequired['DidChangeConfigurationClientCapabilities']
    didChangeWatchedFiles: NotRequired['DidChangeWatchedFilesClientCapabilities']
    symbol: NotRequired['WorkspaceSymbolClientCapabilities']
    executeCommand: NotRequired['ExecuteCommandClientCapabilities']
    workspaceFolders: NotRequired[bool]
    configuration: NotRequired[bool]
    semanticTokens: NotRequired['SemanticTokensWorkspaceClientCapabilities']
    codeLens: NotRequired['CodeLensWorkspaceClientCapabilities']
    fileOperations: NotRequired['FileOperationClientCapabilities']
    inlineValue: NotRequired['InlineValueWorkspaceClientCapabilities']
    inlayHint: NotRequired['InlayHintWorkspaceClientCapabilities']
    diagnostics: NotRequired['DiagnosticWorkspaceClientCapabilities']
    foldingRange: NotRequired['FoldingRangeWorkspaceClientCapabilities']
    textDocumentContent: NotRequired['TextDocumentContentClientCapabilities']

class TextDocumentClientCapabilities(TypedDict):
    synchronization: NotRequired['TextDocumentSyncClientCapabilities']
    filters: NotRequired['TextDocumentFilterClientCapabilities']
    completion: NotRequired['CompletionClientCapabilities']
    hover: NotRequired['HoverClientCapabilities']
    signatureHelp: NotRequired['SignatureHelpClientCapabilities']
    declaration: NotRequired['DeclarationClientCapabilities']
    definition: NotRequired['DefinitionClientCapabilities']
    typeDefinition: NotRequired['TypeDefinitionClientCapabilities']
    implementation: NotRequired['ImplementationClientCapabilities']
    references: NotRequired['ReferenceClientCapabilities']
    documentHighlight: NotRequired['DocumentHighlightClientCapabilities']
    documentSymbol: NotRequired['DocumentSymbolClientCapabilities']
    codeAction: NotRequired['CodeActionClientCapabilities']
    codeLens: NotRequired['CodeLensClientCapabilities']
    documentLink: NotRequired['DocumentLinkClientCapabilities']
    colorProvider: NotRequired['DocumentColorClientCapabilities']
    formatting: NotRequired['DocumentFormattingClientCapabilities']
    rangeFormatting: NotRequired['DocumentRangeFormattingClientCapabilities']
    onTypeFormatting: NotRequired['DocumentOnTypeFormattingClientCapabilities']
    rename: NotRequired['RenameClientCapabilities']
    foldingRange: NotRequired['FoldingRangeClientCapabilities']
    selectionRange: NotRequired['SelectionRangeClientCapabilities']
    publishDiagnostics: NotRequired['PublishDiagnosticsClientCapabilities']
    callHierarchy: NotRequired['CallHierarchyClientCapabilities']
    semanticTokens: NotRequired['SemanticTokensClientCapabilities']
    linkedEditingRange: NotRequired['LinkedEditingRangeClientCapabilities']
    moniker: NotRequired['MonikerClientCapabilities']
    typeHierarchy: NotRequired['TypeHierarchyClientCapabilities']
    inlineValue: NotRequired['InlineValueClientCapabilities']
    inlayHint: NotRequired['InlayHintClientCapabilities']
    diagnostic: NotRequired['DiagnosticClientCapabilities']
    inlineCompletion: NotRequired['InlineCompletionClientCapabilities']

class NotebookDocumentClientCapabilities(TypedDict):
    synchronization: NotebookDocumentSyncClientCapabilities

class WindowClientCapabilities(TypedDict):
    workDoneProgress: NotRequired[bool]
    showMessage: NotRequired['ShowMessageRequestClientCapabilities']
    showDocument: NotRequired['ShowDocumentClientCapabilities']

class GeneralClientCapabilities(TypedDict):
    staleRequestSupport: NotRequired['StaleRequestSupportOptions']
    regularExpressions: NotRequired['RegularExpressionsClientCapabilities']
    markdown: NotRequired['MarkdownClientCapabilities']
    positionEncodings: NotRequired[list['PositionEncodingKind']]

class WorkspaceFoldersServerCapabilities(TypedDict):
    supported: NotRequired[bool]
    changeNotifications: NotRequired[str | bool]

class FileOperationOptions(TypedDict):
    didCreate: NotRequired['FileOperationRegistrationOptions']
    willCreate: NotRequired['FileOperationRegistrationOptions']
    didRename: NotRequired['FileOperationRegistrationOptions']
    willRename: NotRequired['FileOperationRegistrationOptions']
    didDelete: NotRequired['FileOperationRegistrationOptions']
    willDelete: NotRequired['FileOperationRegistrationOptions']

class RelativePattern(TypedDict):
    baseUri: WorkspaceFolder | URI
    pattern: Pattern

class TextDocumentFilterLanguage(TypedDict):
    language: str
    scheme: NotRequired[str]
    pattern: NotRequired['GlobPattern']

class TextDocumentFilterScheme(TypedDict):
    language: NotRequired[str]
    scheme: str
    pattern: NotRequired['GlobPattern']

class TextDocumentFilterPattern(TypedDict):
    language: NotRequired[str]
    scheme: NotRequired[str]
    pattern: GlobPattern

class NotebookDocumentFilterNotebookType(TypedDict):
    notebookType: str
    scheme: NotRequired[str]
    pattern: NotRequired['GlobPattern']

class NotebookDocumentFilterScheme(TypedDict):
    notebookType: NotRequired[str]
    scheme: str
    pattern: NotRequired['GlobPattern']

class NotebookDocumentFilterPattern(TypedDict):
    notebookType: NotRequired[str]
    scheme: NotRequired[str]
    pattern: GlobPattern

class NotebookCellArrayChange(TypedDict):
    start: Uint
    deleteCount: Uint
    cells: NotRequired[list['NotebookCell']]

class WorkspaceEditClientCapabilities(TypedDict):
    documentChanges: NotRequired[bool]
    resourceOperations: NotRequired[list['ResourceOperationKind']]
    failureHandling: NotRequired['FailureHandlingKind']
    normalizesLineEndings: NotRequired[bool]
    changeAnnotationSupport: NotRequired['ChangeAnnotationsSupportOptions']
    metadataSupport: NotRequired[bool]
    snippetEditSupport: NotRequired[bool]

class DidChangeConfigurationClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class DidChangeWatchedFilesClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    relativePatternSupport: NotRequired[bool]

class WorkspaceSymbolClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    symbolKind: NotRequired['ClientSymbolKindOptions']
    tagSupport: NotRequired['ClientSymbolTagOptions']
    resolveSupport: NotRequired['ClientSymbolResolveOptions']

class ExecuteCommandClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class SemanticTokensWorkspaceClientCapabilities(TypedDict):
    refreshSupport: NotRequired[bool]

class CodeLensWorkspaceClientCapabilities(TypedDict):
    refreshSupport: NotRequired[bool]

class FileOperationClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    didCreate: NotRequired[bool]
    willCreate: NotRequired[bool]
    didRename: NotRequired[bool]
    willRename: NotRequired[bool]
    didDelete: NotRequired[bool]
    willDelete: NotRequired[bool]

class InlineValueWorkspaceClientCapabilities(TypedDict):
    refreshSupport: NotRequired[bool]

class InlayHintWorkspaceClientCapabilities(TypedDict):
    refreshSupport: NotRequired[bool]

class DiagnosticWorkspaceClientCapabilities(TypedDict):
    refreshSupport: NotRequired[bool]

class FoldingRangeWorkspaceClientCapabilities(TypedDict):
    refreshSupport: NotRequired[bool]

class TextDocumentContentClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class TextDocumentSyncClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    willSave: NotRequired[bool]
    willSaveWaitUntil: NotRequired[bool]
    didSave: NotRequired[bool]

class TextDocumentFilterClientCapabilities(TypedDict):
    relativePatternSupport: NotRequired[bool]

class CompletionClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    completionItem: NotRequired['ClientCompletionItemOptions']
    completionItemKind: NotRequired['ClientCompletionItemOptionsKind']
    insertTextMode: NotRequired['InsertTextMode']
    contextSupport: NotRequired[bool]
    completionList: NotRequired['CompletionListCapabilities']

class HoverClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    contentFormat: NotRequired[list['MarkupKind']]

class SignatureHelpClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    signatureInformation: NotRequired['ClientSignatureInformationOptions']
    contextSupport: NotRequired[bool]

class DeclarationClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    linkSupport: NotRequired[bool]

class DefinitionClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    linkSupport: NotRequired[bool]

class TypeDefinitionClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    linkSupport: NotRequired[bool]

class ImplementationClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    linkSupport: NotRequired[bool]

class ReferenceClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class DocumentHighlightClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class DocumentSymbolClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    symbolKind: NotRequired['ClientSymbolKindOptions']
    hierarchicalDocumentSymbolSupport: NotRequired[bool]
    tagSupport: NotRequired['ClientSymbolTagOptions']
    labelSupport: NotRequired[bool]

class CodeActionClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    codeActionLiteralSupport: NotRequired['ClientCodeActionLiteralOptions']
    isPreferredSupport: NotRequired[bool]
    disabledSupport: NotRequired[bool]
    dataSupport: NotRequired[bool]
    resolveSupport: NotRequired['ClientCodeActionResolveOptions']
    honorsChangeAnnotations: NotRequired[bool]
    documentationSupport: NotRequired[bool]
    tagSupport: NotRequired['CodeActionTagOptions']

class CodeLensClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    resolveSupport: NotRequired['ClientCodeLensResolveOptions']

class DocumentLinkClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    tooltipSupport: NotRequired[bool]

class DocumentColorClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class DocumentFormattingClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class DocumentRangeFormattingClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    rangesSupport: NotRequired[bool]

class DocumentOnTypeFormattingClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class RenameClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    prepareSupport: NotRequired[bool]
    prepareSupportDefaultBehavior: NotRequired['PrepareSupportDefaultBehavior']
    honorsChangeAnnotations: NotRequired[bool]

class FoldingRangeClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    rangeLimit: NotRequired[Uint]
    lineFoldingOnly: NotRequired[bool]
    foldingRangeKind: NotRequired['ClientFoldingRangeKindOptions']
    foldingRange: NotRequired['ClientFoldingRangeOptions']

class SelectionRangeClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class PublishDiagnosticsClientCapabilities(TypedDict):
    versionSupport: NotRequired[bool]
    relatedInformation: NotRequired[bool]
    tagSupport: NotRequired['ClientDiagnosticsTagOptions']
    codeDescriptionSupport: NotRequired[bool]
    dataSupport: NotRequired[bool]

class CallHierarchyClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class SemanticTokensClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    requests: ClientSemanticTokensRequestOptions
    tokenTypes: list[str]
    tokenModifiers: list[str]
    formats: list['TokenFormat']
    overlappingTokenSupport: NotRequired[bool]
    multilineTokenSupport: NotRequired[bool]
    serverCancelSupport: NotRequired[bool]
    augmentsSyntaxTokens: NotRequired[bool]

class LinkedEditingRangeClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class MonikerClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class TypeHierarchyClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class InlineValueClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class InlayHintClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    resolveSupport: NotRequired['ClientInlayHintResolveOptions']

class DiagnosticClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    relatedDocumentSupport: NotRequired[bool]
    relatedInformation: NotRequired[bool]
    tagSupport: NotRequired['ClientDiagnosticsTagOptions']
    codeDescriptionSupport: NotRequired[bool]
    dataSupport: NotRequired[bool]

class InlineCompletionClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class NotebookDocumentSyncClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    executionSummarySupport: NotRequired[bool]

class ShowMessageRequestClientCapabilities(TypedDict):
    messageActionItem: NotRequired['ClientShowMessageActionItemOptions']

class ShowDocumentClientCapabilities(TypedDict):
    support: bool

class StaleRequestSupportOptions(TypedDict):
    cancel: bool
    retryOnContentModified: list[str]

class RegularExpressionsClientCapabilities(TypedDict):
    engine: RegularExpressionEngineKind
    version: NotRequired[str]

class MarkdownClientCapabilities(TypedDict):
    parser: str
    version: NotRequired[str]
    allowedTags: NotRequired[list[str]]

class ChangeAnnotationsSupportOptions(TypedDict):
    groupsOnLabel: NotRequired[bool]

class ClientSymbolKindOptions(TypedDict):
    valueSet: NotRequired[list['SymbolKind']]

class ClientSymbolTagOptions(TypedDict):
    valueSet: list['SymbolTag']

class ClientSymbolResolveOptions(TypedDict):
    properties: list[str]

class ClientCompletionItemOptions(TypedDict):
    snippetSupport: NotRequired[bool]
    commitCharactersSupport: NotRequired[bool]
    documentationFormat: NotRequired[list['MarkupKind']]
    deprecatedSupport: NotRequired[bool]
    preselectSupport: NotRequired[bool]
    tagSupport: NotRequired['CompletionItemTagOptions']
    insertReplaceSupport: NotRequired[bool]
    resolveSupport: NotRequired['ClientCompletionItemResolveOptions']
    insertTextModeSupport: NotRequired['ClientCompletionItemInsertTextModeOptions']
    labelDetailsSupport: NotRequired[bool]

class ClientCompletionItemOptionsKind(TypedDict):
    valueSet: NotRequired[list['CompletionItemKind']]

class CompletionListCapabilities(TypedDict):
    itemDefaults: NotRequired[list[str]]
    applyKindSupport: NotRequired[bool]

class ClientSignatureInformationOptions(TypedDict):
    documentationFormat: NotRequired[list['MarkupKind']]
    parameterInformation: NotRequired['ClientSignatureParameterInformationOptions']
    activeParameterSupport: NotRequired[bool]
    noActiveParameterSupport: NotRequired[bool]

class ClientCodeActionLiteralOptions(TypedDict):
    codeActionKind: ClientCodeActionKindOptions

class ClientCodeActionResolveOptions(TypedDict):
    properties: list[str]

class CodeActionTagOptions(TypedDict):
    valueSet: list['CodeActionTag']

class ClientCodeLensResolveOptions(TypedDict):
    properties: list[str]

class ClientFoldingRangeKindOptions(TypedDict):
    valueSet: NotRequired[list['FoldingRangeKind']]

class ClientFoldingRangeOptions(TypedDict):
    collapsedText: NotRequired[bool]

class DiagnosticsCapabilities(TypedDict):
    relatedInformation: NotRequired[bool]
    tagSupport: NotRequired['ClientDiagnosticsTagOptions']
    codeDescriptionSupport: NotRequired[bool]
    dataSupport: NotRequired[bool]

class ClientSemanticTokensRequestOptions(TypedDict):
    range: NotRequired[bool | dict]
    full: NotRequired[bool | ClientSemanticTokensRequestFullDelta]

class ClientInlayHintResolveOptions(TypedDict):
    properties: list[str]

class ClientShowMessageActionItemOptions(TypedDict):
    additionalPropertiesSupport: NotRequired[bool]

class CompletionItemTagOptions(TypedDict):
    valueSet: list['CompletionItemTag']

class ClientCompletionItemResolveOptions(TypedDict):
    properties: list[str]

class ClientCompletionItemInsertTextModeOptions(TypedDict):
    valueSet: list['InsertTextMode']

class ClientSignatureParameterInformationOptions(TypedDict):
    labelOffsetSupport: NotRequired[bool]

class ClientCodeActionKindOptions(TypedDict):
    valueSet: list['CodeActionKind']

class ClientDiagnosticsTagOptions(TypedDict):
    valueSet: list['DiagnosticTag']

class ClientSemanticTokensRequestFullDelta(TypedDict):
    delta: NotRequired[bool]
R = TypeVar('R')

class Request(Generic[R]):
    __slots__: Incomplete
    method: Incomplete
    params: Incomplete
    view: Incomplete
    progress: Incomplete
    partial_results: Incomplete
    def __init__(self, method: str, params: Any = None, view: sublime.View | None = None, progress: bool = False, partial_results: bool = False) -> None: ...
    @classmethod
    def initialize(cls, params: InitializeParams) -> Request: ...
    @classmethod
    def complete(cls, params: CompletionParams, view: sublime.View) -> Request: ...
    @classmethod
    def signatureHelp(cls, params: SignatureHelpParams, view: sublime.View) -> Request: ...
    @classmethod
    def codeAction(cls, params: CodeActionParams, view: sublime.View) -> Request: ...
    @classmethod
    def documentColor(cls, params: DocumentColorParams, view: sublime.View) -> Request: ...
    @classmethod
    def colorPresentation(cls, params: ColorPresentationParams, view: sublime.View) -> Request: ...
    @classmethod
    def willSaveWaitUntil(cls, params: WillSaveTextDocumentParams, view: sublime.View) -> Request: ...
    @classmethod
    def documentSymbols(cls, params: DocumentSymbolParams, view: sublime.View) -> Request: ...
    @classmethod
    def documentHighlight(cls, params: DocumentHighlightParams, view: sublime.View) -> Request: ...
    @classmethod
    def documentLink(cls, params: DocumentLinkParams, view: sublime.View) -> Request: ...
    @classmethod
    def semanticTokensFull(cls, params: SemanticTokensParams, view: sublime.View) -> Request: ...
    @classmethod
    def semanticTokensFullDelta(cls, params: SemanticTokensDeltaParams, view: sublime.View) -> Request: ...
    @classmethod
    def semanticTokensRange(cls, params: SemanticTokensRangeParams, view: sublime.View) -> Request: ...
    @classmethod
    def prepareCallHierarchy(cls, params: CallHierarchyPrepareParams, view: sublime.View) -> Request[list[CallHierarchyItem] | Error | None]: ...
    @classmethod
    def incomingCalls(cls, params: CallHierarchyIncomingCallsParams) -> Request: ...
    @classmethod
    def outgoingCalls(cls, params: CallHierarchyOutgoingCallsParams) -> Request: ...
    @classmethod
    def prepareTypeHierarchy(cls, params: TypeHierarchyPrepareParams, view: sublime.View) -> Request: ...
    @classmethod
    def supertypes(cls, params: TypeHierarchySupertypesParams) -> Request: ...
    @classmethod
    def subtypes(cls, params: TypeHierarchySubtypesParams) -> Request: ...
    @classmethod
    def resolveCompletionItem(cls, params: CompletionItem, view: sublime.View) -> Request: ...
    @classmethod
    def resolveDocumentLink(cls, params: DocumentLink, view: sublime.View) -> Request: ...
    @classmethod
    def inlayHint(cls, params: InlayHintParams, view: sublime.View) -> Request: ...
    @classmethod
    def resolveInlayHint(cls, params: InlayHint, view: sublime.View) -> Request: ...
    @classmethod
    def rename(cls, params: RenameParams, view: sublime.View, progress: bool = False) -> Request: ...
    @classmethod
    def prepareRename(cls, params: PrepareRenameParams, view: sublime.View, progress: bool = False) -> Request: ...
    @classmethod
    def selectionRange(cls, params: SelectionRangeParams) -> Request: ...
    @classmethod
    def foldingRange(cls, params: FoldingRangeParams, view: sublime.View) -> Request: ...
    @classmethod
    def workspaceSymbol(cls, params: WorkspaceSymbolParams) -> Request: ...
    @classmethod
    def resolveWorkspaceSymbol(cls, params: WorkspaceSymbol) -> Request: ...
    @classmethod
    def documentDiagnostic(cls, params: DocumentDiagnosticParams, view: sublime.View) -> Request: ...
    @classmethod
    def workspaceDiagnostic(cls, params: WorkspaceDiagnosticParams) -> Request: ...
    @classmethod
    def shutdown(cls) -> Request: ...
    def __repr__(self) -> str: ...
    def to_payload(self, id: int) -> dict[str, Any]: ...

class Error(Exception):
    code: Incomplete
    data: Incomplete
    def __init__(self, code: int, message: str, data: Any = None) -> None: ...
    @classmethod
    def from_lsp(cls, params: Any) -> Error: ...
    def to_lsp(self) -> dict[str, Any]: ...
    def __str__(self) -> str: ...
    @classmethod
    def from_exception(cls, ex: Exception) -> Error: ...
T = TypeVar('T', bound=None | bool | int | Uint | float | str | Mapping[str, Any] | Iterable[Any])

class Response(Generic[T]):
    __slots__: Incomplete
    request_id: Incomplete
    result: Incomplete
    def __init__(self, request_id: Any, result: T) -> None: ...
    def to_payload(self) -> dict[str, Any]: ...

class Notification:
    __slots__: Incomplete
    method: Incomplete
    params: Incomplete
    def __init__(self, method: str, params: Any = None) -> None: ...
    @classmethod
    def initialized(cls) -> Notification: ...
    @classmethod
    def didOpen(cls, params: DidOpenTextDocumentParams) -> Notification: ...
    @classmethod
    def didChange(cls, params: DidChangeTextDocumentParams) -> Notification: ...
    @classmethod
    def willSave(cls, params: WillSaveTextDocumentParams) -> Notification: ...
    @classmethod
    def didSave(cls, params: DidSaveTextDocumentParams) -> Notification: ...
    @classmethod
    def didClose(cls, params: DidCloseTextDocumentParams) -> Notification: ...
    @classmethod
    def didChangeConfiguration(cls, params: DidChangeConfigurationParams) -> Notification: ...
    @classmethod
    def didChangeWatchedFiles(cls, params: DidChangeWatchedFilesParams) -> Notification: ...
    @classmethod
    def didChangeWorkspaceFolders(cls, params: DidChangeWorkspaceFoldersParams) -> Notification: ...
    @classmethod
    def exit(cls) -> Notification: ...
    def __repr__(self) -> str: ...
    def to_payload(self) -> dict[str, Any]: ...

class Point:
    row: Incomplete
    col: Incomplete
    def __init__(self, row: int, col: int) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    @classmethod
    def from_lsp(cls, point: Position) -> Point: ...
    def to_lsp(self) -> Position: ...
    def __ge__(self, other): ...
    def __gt__(self, other): ...
    def __le__(self, other): ...

class ResponseError(TypedDict):
    code: int
    message: str
    data: NotRequired['LSPAny']

class CodeLensExtended(TypedDict):
    range: 'Range'
    command: NotRequired['Command']
    data: NotRequired['LSPAny']
    session_name: str
RangeLsp = Range
