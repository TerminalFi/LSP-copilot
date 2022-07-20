# LSP-copilot

Github Copilot support for Sublime's LSP plugin.

Uses [Copilot][] Distribution which uses OpenAI Codex to suggest code and entire functions in real-time right from your editor.

### Prerequisites

* An active subscription is required to use Github Copilot.

### Installation

1. Install [LSP][] from Package Control.
1. Install LSP-copilot from git
    1. Go to folder Packages:
        * Windows: `%APPDATA%\Sublime Text\Packages`
        * OS X: `~/Library/Application\ Support/Sublime\ Text/Packages`
        * Linux: `~/.config/sublime-text/Packages/`
    1. Run: `git clone git@github.com:TheSecEng/LSP-copilot.git` via command line or terminal
1. Restart Sublime

### Setup

On initial use, follow the steps below:

1. Launch `Copilot: Sign In` from the `Command Pallete`
1. Follow the prompts to Authenticate your Copilot extension
    1. Paste `User Code` into Github's authentication flow
    1. Return to `Sublime Text` and press `Ok` on the dialog
1. Use `LSP-copilot`


[Copilot]: https://github.com/features/copilot
[LSP]: https://github.com/sublimelsp/LSP
