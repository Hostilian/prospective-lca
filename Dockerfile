# Reproducible local container for the offline synthetic workbench.
# No licensed databases, credentials, or confidential AWAM data are copied.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY app ./app
COPY demo ./demo
COPY schemas ./schemas
COPY pyproject.toml README.md LICENSE-or-INTERNAL-USE-NOTICE.md ./

RUN useradd --create-home --uid 10001 awam \
    && mkdir -p /app/exports/demo \
    && chown -R awam:awam /app

USER awam

# Build the self-contained demo during image construction so the default
# container is immediately useful and does not need network access at runtime.
RUN python -m app.cli demo --out /app/exports/demo

EXPOSE 8765

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8765/', timeout=2)"

CMD ["python", "-m", "app.cli", "serve", "--dir", "/app/exports/demo", "--host", "0.0.0.0", "--port", "8765"]

