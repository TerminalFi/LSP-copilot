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

1. Open any file.
1. Execute `Copilot: Sign In` from the command palette.
1. Follow the prompts to authenticate LSP-copilot.
    1. The `User Code` will be auto copied to your clipboard.
    1. Paste the `User Code` into the pop-up GitHub authentication page.
    1. Return to Sublime Text and press `OK` on the dialog.
    1. If you see a "sign in OK" dialog, LSP-copilot should start working since then.

## Settings

Provide user settings in LSP-copilot.sublime-settings (Settings... > Package Settings > LSP > Servers > LSP-copilot)

| Setting                       | Type    | Default | Description                                                         |
| ----------------------------- | ------- | ------- | ------------------------------------------------------------------- |
| auto_ask_completions          | boolean | true    | Auto ask the server for completions. Otherwise, you have to trigger it manually. |
| debug                         | boolean | false   | Enables `debug` mode for LSP-copilot. Enabling all commands regardless of status requirements. |
| hook_to_auto_complete_command | boolean | false   | Ask the server for completions when the `auto_complete` command is called. |
| local_checks                  | boolean | false   | Enables local checks. This feature is not fully understood yet.      |
| telemetry                     | boolean | false   | Enables Copilot telemetry requests for `Accept` and `Reject` completions. |
| proxy                         | string  |        | The HTTP proxy to use for Copilot requests. It's in the form of `username:password@host:port` or just `host:port`. |
| completion_style              | string  | popup   | Completion style. `popup` is the default, `phantom` is experimental ([there are well-known issues](https://github.com/TheSecEng/LSP-copilot/issues)). |

## FAQs

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
 ```

[Copilot]: https://github.com/features/copilot
[Copilot.vim]: https://github.com/github/copilot.vim
[LSP]: https://packagecontrol.io/packages/LSP
[LSP-copilot]: https://packagecontrol.io/packages/LSP-copilot
