FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y git

RUN mkdir -p /app

WORKDIR /app
RUN pip --no-cache-dir install --upgrade pip setuptools wheel

COPY . /app

RUN pip wheel . --wheel-dir /wheels --find-links /wheels


#
FROM python:3.12-slim

ARG UNAME=sso
ARG UID=993
ARG GID=993
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels

WORKDIR /usr/src/app
RUN chown -R $UNAME:$UNAME /usr/src/app

RUN pip --no-cache-dir install --find-links /wheels --no-index discourse-sso-oidc-bridge

USER $UNAME

# Expose default port
EXPOSE 8080

# Run application with Gunicorn
CMD gunicorn --workers=2 --bind ${BIND_IP:-0.0.0.0}:${BIND_PORT:-8080} discourse_sso_oidc_bridge:app
