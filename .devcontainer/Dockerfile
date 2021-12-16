# Latest stable version of Debian
FROM mcr.microsoft.com/vscode/devcontainers/base:bullseye

# Ensure Dockerfile is built with devcontainer-cli
ARG vscode
RUN if [[ -z "$vscode" ]] ; then printf "\nERROR: This Dockerfile needs to be built with VS Code !" && exit 1; else printf "VS Code is detected: $vscode"; fi

# Use bash shell
SHELL ["bin/bash", "-l", "-c"]

# Set home directory
ENV HOME="/root"

# Update/upgrade apt-get
RUN apt-get update && apt-get upgrade

# Install NVM (node version manager)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Setup NVM to auto-install node version in .nvmrc
COPY .devcontainer/nvm-autoinstall.sh nvm-autoinstall.sh
RUN cat nvm-autoinstall.sh >> $HOME/.bashrc && echo '' >> $HOME/.bashrc && rm nvm-autoinstall.sh

# Install Node.js
COPY .nvmrc .nvmrc
RUN cat .nvmrc | nvm install

# Install Yarn (node package manager)
RUN npm install -g yarn

# Install Pyenv (Python version manager)
ENV PATH="$HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH"
RUN curl https://pyenv.run | bash
COPY .devcontainer/pyenv.sh pyenv.sh
RUN cat pyenv.sh >> $HOME/.bashrc && rm pyenv.sh

# Install Poetry (Python package manager)
ENV POETRY_VIRTUALENVS_CREATE=false
RUN apt-get install -y python3-pip && pip install poetry

# Install Python build dependencies
RUN apt-get install -y \
  build-essential \
  libbz2-dev \
  libffi-dev \
  liblzma-dev \
  libreadline-dev \
  libsqlite3-dev \
  libssl-dev \
  zlib1g-dev

# Install Python
COPY .python-version /
RUN $HOME/.pyenv/bin/pyenv install
