# The OKF chat/voice app image (ADR-0005). Stdlib-only Python -- there is nothing to
# `pip install`, so the image stays tiny and has no third-party supply chain.
#
# Build context is the REPO ROOT (see docker-compose.yml), so paths below are repo-relative.
FROM python:3.12-slim

# Run as a non-root user; the app only ever reads the bundle.
RUN useradd --create-home --uid 10001 okf
WORKDIR /app

# The application (headless POCs + the thin web/voice server) and a baked copy of the
# bundle as a fallback. In Compose the bundle is instead mounted read-only at /data/okf
# (so `git pull` on the host refreshes it without a rebuild); OKF_BUNDLE selects which.
COPY chat/ /app/chat/
COPY okf/ /app/okf/
COPY scripts/ /app/scripts/

USER okf
WORKDIR /app/chat
EXPOSE 8080

# Defaults; every one is overridable via the environment (deploy/.env).
ENV OKF_CHAT_HOST=0.0.0.0 \
    OKF_CHAT_PORT=8080 \
    OKF_BUNDLE=/data/okf

CMD ["python3", "server.py"]
