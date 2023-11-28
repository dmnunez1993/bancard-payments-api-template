FROM ubuntu:22.04

# Set up user as it's on the host
ARG USER_UID
ARG USER_NAME

RUN groupadd -g ${USER_UID} ${USER_NAME}
RUN useradd -r -u ${USER_UID} -g ${USER_UID} ${USER_NAME}

LABEL Description="Image to facilitate development of Backend Payments Api Template app."

ENV DEBIAN_FRONTEND=noninteractive

# Install required packages to run apps
RUN apt-get update && apt-get install -y build-essential git bash-completion python3-pip wget autoconf libtool unzip curl vim

# Install databases
RUN apt-get update && apt-get install -y postgresql postgresql-14 postgresql-server-dev-14 libpq-dev

# Install redis
RUN apt-get update && apt-get install -y redis redis-server

# Install virtualenv
RUN pip3 install virtualenv

# Setup postgresql
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV BACKEND_DB_USER=postgres
ENV BACKEND_DB_PASSWORD=postgres
ENV BACKEND_DB_NAME=bancard_payments_api
ENV BACKEND_DB_HOST=localhost
ENV BACKEND_DB_PORT=5432

COPY ./conf/pg_hba.conf pg_hba.conf
COPY ./conf/postgresql.conf postgresql.conf

# Install misc
RUN apt-get update && apt-get install -y sudo

RUN echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/docker

# Set up locales
RUN apt-get update && apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

# Set up terminal colors
ENV TERM=xterm-256color
COPY ./scripts/00-aliases.sh /etc/profile.d/
COPY ./scripts/02-colors.sh /etc/profile.d/

# Set up executables for creating the environment
COPY ./scripts/attach_env /usr/local/bin
COPY ./scripts/setup_env /usr/local/bin
COPY ./scripts/setup_postgresql /usr/local/bin
COPY ./scripts/setup_vscode_settings /usr/local/bin

# Set up user
USER ${USER_NAME}
ENV HOME=/home/${USER_NAME}

# Set up pythonpath
ENV PYTHONPATH=/bancard_payments_api/backend

# Set up additional configuration
ENV BACKEND_ACCESS_SECRET=access_secret
ENV BACKEND_REFRESH_SECRET=refresh_secret
ENV BACKEND_SECRET_KEY=secret_key
ENV ALLOWED_ORIGINS=http://localhost:3000
