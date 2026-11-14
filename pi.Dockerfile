FROM node:24-bookworm-slim

ARG PI_VERSION=latest

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates \
    fd-find git ripgrep yt-dlp ffmpeg python3 python3.11-venv make \
    && ln -s /usr/bin/fdfind /usr/local/bin/fd \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g --ignore-scripts "@earendil-works/pi-coding-agent@${PI_VERSION}"

COPY agent /home/node/.pi/agent
RUN chown -R node:node /home/node/.pi

USER node
RUN cd /home/node/.pi/agent/extensions/bash-guard && npm install \
    && cd /home/node/.pi/agent/extensions/browser && npm install \
    && cd /home/node/.pi/agent/extensions/web-fetch && npm install \
    && python3 -m venv ~/.pi/agent/skills/pdf-reader/.venv \
    && /home/node/.pi/agent/skills/pdf-reader/.venv/bin/pip install \
        -r /home/node/.pi/agent/skills/pdf-reader/requirements.txt \
    && pi update --extensions
RUN npx playwright install chromium

ENV PI_CODING_AGENT_DIR=/home/node/.pi/agent
ENV PI_TELEMETRY=0

USER root
RUN mkdir -p /workspace && chown node:node /workspace

USER node
WORKDIR /workspace
ENTRYPOINT ["pi"]

# podman build -t pi-agent:local -f pi.Dockerfile .

