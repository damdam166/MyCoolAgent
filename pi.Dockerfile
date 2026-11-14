FROM node:24-bookworm-slim

ARG PI_VERSION=latest

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates \
    fd-find git ripgrep yt-dlp ffmpeg python3 python3.11-venv python3-pip \
    make tmux vim neovim curl wget jq yq \
    && ln -s /usr/bin/fdfind /usr/local/bin/fd \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g --ignore-scripts "@earendil-works/pi-coding-agent@${PI_VERSION}"

COPY agent /home/node/.pi/agent
RUN chown -R node:node /home/node/

USER node
RUN git clone https://github.com/tmux-plugins/tpm home/node/.tmux/plugins/tpm \
    && git clone https://github.com/tmux-plugins/tmux-sensible /home/node/.tmux/plugins/tmux-sensible

RUN cd /home/node/.pi/agent/extensions/bash-guard && npm install \
    && cd /home/node/.pi/agent/extensions/browser && npm install \
    && cd /home/node/.pi/agent/extensions/web-fetch && npm install \
    && python3 -m venv ~/.pi/agent/skills/pdf-reader/.venv \
    && /home/node/.pi/agent/skills/pdf-reader/.venv/bin/pip install \
        -r /home/node/.pi/agent/skills/pdf-reader/requirements.txt \
    && /home/node/.pi/agent/skills/rss-feed/.venv/bin/pip install \
        -r /home/node/.pi/agent/skills/rss-feed/requirements.txt \
    && pi update --extensions
RUN npx playwright install chromium

# This file is bugged, from the extension...
RUN rm /home/node/.pi/agent/npm/node_modules/awesome-pi-themes/themes/codex-slate.json

ENV PI_CODING_AGENT_DIR=/home/node/.pi/agent
ENV PI_TELEMETRY=0

USER root
RUN mkdir -p /workspace && chown node:node /workspace

USER node
COPY .tmux.conf /home/node/.tmux.conf
WORKDIR /workspace
ENTRYPOINT ["tmux", "new", "-A", "-s", "pi", "'pi'"]

# podman build -t pi-agent:local -f pi.Dockerfile .

# export PI_CODING_AGENT_DIR="/home/node/.pi/agent"
# export OPENROUTER_API_KEY="sk-or-v1-CHANGEME"

# podman run --rm -it \
#     --name AgentSmithResurrection \
#     -h sandboxpi \
#     -e OPENROUTER_API_KEY \
#     -v "$HOME/Documents/currentWork:/workspace/currentWork" \
#     -v "$HOME/.pi/agent/telegram.json:$PI_CODING_AGENT_DIR/telegram.json:ro" \
#     -v "$HOME/.pi/agent/rss.json:$PI_CODING_AGENT_DIR/rss.json:ro" \
#     -v "$HOME/.pi/agent/pi-hermes-memory:$PI_CODING_AGENT_DIR/pi-hermes-memory" \
#     -v "$HOME/.pi/agent/projects-memory:$PI_CODING_AGENT_DIR/projects-memory" \
#     -v "$HOME/.pi/agent/sessions:$PI_CODING_AGENT_DIR/sessions" \
#     localhost/pi-agent:local

