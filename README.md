# LSP-copilot

GitHub Copilot support for Sublime Text LSP plugin provided through [Copilot.vim][].

This plugin uses [Copilot][] distribution which uses OpenAI Codex to suggest codes
and entire functions in real-time right from your editor.

## Prerequisites

* Network connection.
* Active GitHub Copilot subscription.

    Note that GitHub Copilot is free until August 22, 2022. You can start your trail on [this][Copilot] page.

## Installation

Currently, LSP-copilot is not on Package Control.

1. Install [LSP][] via Package Control.
1. Clone LSP-copilot to your `Packages` folder.
    1. Run `sublime.packages_path()` in Sublime Text console. It will show the path of your `Packages` folder.
    1. Open terminal in the `Packages` folder and then run `git clone git@github.com:TheSecEng/LSP-copilot.git`
1. Restart Sublime Text.

## Setup

On the first time use, follow the steps below:

1. Execute `Copilot: Sign In` from the command palette.
1. Follow the prompts to authenticate LSP-copilot.
    1. The `User Code` will be auto copied to your clipboard.
    1. Paste the `User Code` into the pop-up GitHub authentication page.
    1. Return to Sublime Text and press `OK` on the dialog.
    1. If you see a "sign in OK" dialog, LSP-copilot should start working since then.


[Copilot]: https://github.com/features/copilot
[Copilot.vim]: https://github.com/github/copilot.vim/tree/release/copilot/dist
[LSP]: https://packagecontrol.io/packages/LSP
