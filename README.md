# LSP-copilot

![Copilot](https://raw.githubusercontent.com/TheSecEng/LSP-copilot/master/docs/screenshot.png)

GitHub Copilot support for Sublime Text LSP plugin provided through [Copilot.vim][].

This plugin uses [Copilot][] distribution which uses OpenAI Codex to suggest codes
and entire functions in real-time right from your editor.

## Prerequisites

* Public network connection.
* Active GitHub Copilot subscription.

## Installation

1. Install [LSP][] and [LSP-copilot][] via Package Control.
1. Restart Sublime Text.

## Setup

On the first time use, follow the steps below:

1. Execute `Copilot: Sign In` from the command palette.
1. Follow the prompts to authenticate LSP-copilot.
    1. The `User Code` will be auto copied to your clipboard.
    1. Paste the `User Code` into the pop-up GitHub authentication page.
    1. Return to Sublime Text and press `OK` on the dialog.
    1. If you see a "sign in OK" dialog, LSP-copilot should start working since then.


## FAQs

### My Sublime Text freezes after installing this plugin

It's likely that you are using Node v18, which is [unsupported](https://github.com/github/copilot.vim/blob/554460008f18cbffecb9f1e5de58fec8410dc16f/autoload/copilot/agent.vim#L378-L387) by the copilot server.
For workarounds, see [#51](https://github.com/TheSecEng/LSP-copilot/issues/51#issuecomment-1216545673).

### Pressing `Tab` commits autocompletion rather than Copilot's suggestion

There is no way for a plugin to know which one is wanted. But you can define your own dedicate keybinding to commit
Copilot's suggestion.

```js
{
    "keys": ["YOUR_OWN_DEDICATE_KEYBINDING"],
    "command": "copilot_accept_completion",
    "context": [
        {
            "key": "setting.copilot.completion.is_visible"
        }
    ]
},
```

### I see `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` error

If working behind a VPN and/or Proxy, you may be required to add your CA file into the NODE environment.
See below for LSP-copilots support for this.

In LSP-copilot's plugin settings, add the following `env` key:

 ```js
 {
   "env": {
       "NODE_EXTRA_CA_CERTS": "/path/to/certificate.crt",
   },
   // other custom settings...
 }

[Copilot]: https://github.com/features/copilot
[Copilot.vim]: https://github.com/github/copilot.vim/tree/release/copilot/dist
[LSP]: https://packagecontrol.io/packages/LSP
[LSP-copilot]: https://packagecontrol.io/packages/LSP-copilot
