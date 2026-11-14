# My Pi config files

This is my `~/.pi` folder.
It is the very first agent I ever created, using pi.dev.
It is accessible from *Telegram*, and supports some cool things.

Inspired from
[**_Amosblomqvist_**](https://github.com/amosblomqvist/pi-config/tree/main) and
[**_a Youtube video_**](https://www.youtube.com/watch?v=iKwPaB5TUdI).

Date: 2026/11/14

![My Cool Agent Demo](agent/assets/MyCoolAgent.gif)

### Dealing with Shai Hulud

I encourage you to copy `.npmrc` from `agent/` to `~/.npmrc`.
It uses `min-release-age` (days) to avoid supply chain attacks.
More detail:
[**_guide_**](https://gist.github.com/mcollina/b294a6c39ee700d24073c0e5a4e93104/).

### Containerized environment

It is time to put Jarvis in Jail.
No need for a complex sandbox. No need for a Network policy.
Only a containerized version will be enough here, with very restricted
API keys for `auth.json` and `telegram.json`.

There is also still a risk of a session poisoning, or equivalent,
because it is mounted into the container.
I need this agent to remember things, I don't know how to do without it...

Building.

```bash
podman build -t pi-agent:local -f pi.Dockerfile .
```

Running.

```bash
export PI_CODING_AGENT_DIR="/home/node/.pi/agent"
export OPENROUTER_API_KEY="sk-or-v1-CHANGEME"

podman run --rm -it \
    --name AgentSmithResurrection \
    -h sandboxpi \
    -e OPENROUTER_API_KEY \
    -v "$HOME/Documents/currentWork:/workspace/currentWork" \
    -v "$HOME/.pi/agent/telegram.json:$PI_CODING_AGENT_DIR/telegram.json:ro" \
    -v "$HOME/.pi/agent/pi-hermes-memory:$PI_CODING_AGENT_DIR/pi-hermes-memory" \
    -v "$HOME/.pi/agent/projects-memory:$PI_CODING_AGENT_DIR/projects-memory" \
    -v "$HOME/.pi/agent/sessions:$PI_CODING_AGENT_DIR/sessions" \
    localhost/pi-agent:local
```

## Extensions

- **bash-guard**: Guards `bash` tool calls; prompts for destructive
  ops in main session, hard‑blocks them in subagents.

- **browser**: Playwright‑driven headless Chromium for driving live SPAs.
  Visible only with `/browser on`.

- **pi-naming**: Automatic & manual naming rules for
  session/tab/workspace targets. Config in `config.json`.

- **pi-vim-keys**: Vim keybindings remap
  (escape, `<leader>oe`, `<leader>p`, etc.).
  Colors defined in `assets/config.schema.json`.

- **prompt-snippets**: Toggle tiny standalone prompt rules
  via **alt+s** or `/snippets`. Active snippets appear above the editor.

- **web-fetch**: Web page fetch via readability, linkedom, turndown, unpdf.
  Dependencies: `@mozilla/readability`, `linkedom`, `turndown`, `unpdf`.

- **@juicesharp/rpiv-ask-user-question**: Pi extension. A structured
  questionnaire the model can put to you when it would otherwise guess,
  with typed options instead of free-form replies.

- **@llblab/pi-telegram**: Telegram runtime adapter for Pi.

- **openwiki**: A CLI that uses a DeepAgents documentation agent to generate
  and maintain an OpenWiki for a codebase.

- **pi-hermes-memory**: Persistent memory + session search + secret scanning
  for Pi. Token-aware policy-only memory by default, SQLite FTS5 search,
  auto-consolidation, procedural skills.

- **pi-lens**: Real-time code feedback for pi — LSP, linters, formatters,
  type-checking, structural analysis & booboo.

- **pi-interactive-subagents**: Interactive subagents for pi: spawn, orchestrate,
  and manage sub-agent sessions in tmux.

- **awesome-pi-themes**: A lot of themes.

## Skills

- **pdf-reader**: Read/comprehend PDFs (lecture notes, papers).
  Hybrid text extraction + vision.

- **web-debug**: Debug frontend by driving a live page with
  browser\_\* tools
  (auth, JWT, storage, forms, blank screen, hydration, stale data).

- **youtube-transcript**: Feech YouTube title and transcript
  via yt-dlp captions. Requires yt-dlp and Python.

### EOF
