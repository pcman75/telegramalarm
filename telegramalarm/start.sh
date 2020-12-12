#!/usr/bin/dumb-init bashio
set -e

bashio::log.info "==> Starting application"

export hostname=$(bashio::addon.hostname)
export portname=$(bashio::addon.ingress_port)
bashio::log.info "Will run ingress on ${hostname}:${portname}"

exec python3 /app/app.py