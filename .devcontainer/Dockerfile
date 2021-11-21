# Latest stable version of Debian
FROM mcr.microsoft.com/vscode/devcontainers/base:bullseye

# Ensure Dockerfile is built with devcontainer-cli
ARG vscode
RUN if [[ -z "$vscode" ]] ; then printf "\nERROR: This Dockerfile needs to be built with VS Code !" && exit 1; else printf "VS Code is detected: $vscode"; fi

# Use bash shell
SHELL ["bin/bash", "-l", "-c"]

# Set home directory
ENV HOME "/root"

# Install NVM (node version manager)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Setup NVM to auto-install node version in .nvmrc
COPY .devcontainer/nvm-autoinstall.sh nvm-autoinstall.sh
RUN cat nvm-autoinstall.sh >> $HOME/.bashrc && echo '' >> $HOME/.bashrc && rm nvm-autoinstall.sh

# Install Node.js version in .nvmrc
COPY .nvmrc .nvmrc
RUN cat .nvmrc | nvm install

# Install Yarn (node package manager)
RUN npm install -g yarn

# Install Pyenv (python version manager)
RUN \
  apt-get update && \
  apt-get upgrade && \
  apt-get install -y python3-venv && \
  curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

# Setup Pyenv init script
ENV PATH "$HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH"
COPY .devcontainer/pyenv.sh pyenv.sh
RUN cat pyenv.sh >> $HOME/.bashrc && echo '' >> $HOME/.bashrc && rm pyenv.sh

# Install Poetry (python package manager)
RUN \
  apt-get update && \
  apt-get upgrade && \
  apt-get install -y python3-dev tk-dev && \
  curl -sSL https://install.python-poetry.org | python3