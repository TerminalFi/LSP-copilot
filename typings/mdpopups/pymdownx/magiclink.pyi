from . import util as util
from ..markdown import Extension as Extension
from ..markdown.inlinepatterns import InlineProcessor as InlineProcessor, LinkInlineProcessor as LinkInlineProcessor
from ..markdown.treeprocessors import Treeprocessor as Treeprocessor
from _typeshed import Incomplete

MAGIC_LINK: int
MAGIC_AUTO_LINK: int
DEFAULT_EXCLUDES: Incomplete
RE_MAIL: str
RE_LINK: str
RE_AUTOLINK: str
RE_TWITTER_USER: str
RE_GITHUB_USER: str
RE_GITLAB_USER: str
RE_BITBUCKET_USER: str
RE_ALL_EXT_MENTIONS: str
RE_TWITTER_EXT_MENTIONS: Incomplete
RE_GITHUB_EXT_MENTIONS: Incomplete
RE_GITLAB_EXT_MENTIONS: Incomplete
RE_BITBUCKET_EXT_MENTIONS: Incomplete
RE_INT_MENTIONS: str
RE_GIT_EXT_REPO_MENTIONS: Incomplete
RE_GIT_INT_REPO_MENTIONS: str
RE_GIT_EXT_REFS: Incomplete
RE_GIT_INT_EXT_REFS: str
RE_GIT_INT_MICRO_REFS: str
RE_REPO_LINK: Incomplete
RE_USER_REPO_LINK: Incomplete
RE_SOCIAL_LINK: Incomplete
SOCIAL_PROVIDERS: Incomplete
PROVIDER_INFO: Incomplete

class _MagiclinkShorthandPattern(InlineProcessor):
    user: Incomplete
    repo: Incomplete
    labels: Incomplete
    provider: Incomplete
    def __init__(self, pattern, md, user, repo, provider, labels) -> None: ...

class _MagiclinkReferencePattern(_MagiclinkShorthandPattern):
    def process_issues(self, el, provider, user, repo, issue) -> None: ...
    def process_commit(self, el, provider, user, repo, commit) -> None: ...
    def process_compare(self, el, provider, user, repo, commit1, commit2) -> None: ...

class MagicShortenerTreeprocessor(Treeprocessor):
    ISSUE: int
    PULL: int
    COMMIT: int
    DIFF: int
    REPO: int
    USER: int
    base: Incomplete
    repo_shortner: Incomplete
    social_shortener: Incomplete
    base_user: Incomplete
    repo_labels: Incomplete
    labels: Incomplete
    excludes: Incomplete
    def __init__(self, md, base_url, base_user_url, labels, repo_shortner, social_shortener, excludes) -> None: ...
    def shorten_repo(self, link, class_name, label, user_repo) -> None: ...
    def shorten_user(self, link, class_name, label, user_repo) -> None: ...
    def shorten_diff(self, link, class_name, label, user_repo, value, hash_size) -> None: ...
    def shorten_commit(self, link, class_name, label, user_repo, value, hash_size) -> None: ...
    def shorten_issue(self, link, class_name, label, user_repo, value, link_type) -> None: ...
    def shorten_issue_commit(self, link, provider, link_type, user_repo, value, hash_size) -> None: ...
    def shorten_user_repo(self, link, provider, link_type, user_repo) -> None: ...
    def get_provider(self, match): ...
    def get_social_provider(self, match): ...
    def get_type(self, provider, match): ...
    def is_my_repo(self, provider, match): ...
    def is_my_user(self, provider, match): ...
    def excluded(self, provider, match): ...
    hide_protocol: Incomplete
    my_repo: Incomplete
    my_user: Incomplete
    def run(self, root): ...

class MagiclinkPattern(LinkInlineProcessor):
    ANCESTOR_EXCLUDES: Incomplete
    def handleMatch(self, m, data): ...

class MagiclinkAutoPattern(InlineProcessor):
    def handleMatch(self, m, data): ...

class MagiclinkMailPattern(InlineProcessor):
    ANCESTOR_EXCLUDES: Incomplete
    def email_encode(self, code): ...
    def handleMatch(self, m, data): ...

class MagiclinkMentionPattern(_MagiclinkShorthandPattern):
    ANCESTOR_EXCLUDES: Incomplete
    def handleMatch(self, m, data): ...

class MagiclinkRepositoryPattern(_MagiclinkShorthandPattern):
    ANCESTOR_EXCLUDES: Incomplete
    def handleMatch(self, m, data): ...

class MagiclinkExternalRefsPattern(_MagiclinkReferencePattern):
    ANCESTOR_EXCLUDES: Incomplete
    my_user: Incomplete
    my_repo: Incomplete
    def handleMatch(self, m, data): ...

class MagiclinkInternalRefsPattern(_MagiclinkReferencePattern):
    ANCESTOR_EXCLUDES: Incomplete
    my_repo: bool
    my_user: bool
    def handleMatch(self, m, data): ...

class MagiclinkExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def setup_autolinks(self, md, config) -> None: ...
    def setup_shorthand(self, md, int_mentions, ext_mentions, config) -> None: ...
    def setup_shortener(self, md, base_url, base_user_url, config, repo_shortner, social_shortener) -> None: ...
    def get_base_urls(self, config): ...
    user: Incomplete
    repo: Incomplete
    provider: Incomplete
    labels: Incomplete
    is_social: Incomplete
    git_short: Incomplete
    social_short: Incomplete
    repo_shortner: Incomplete
    social_shortener: Incomplete
    shortener_exclusions: Incomplete
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
