import os

from uvicorn.workers import UvicornWorker


def to_int(val, default):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


class BaserowUvicronWorker(UvicornWorker):
    """
    Enhanced uvicorn worker class to handle additional uvicorn-specific options
    passed as env variables.

    Unfortunately, gunicorn doesn't support passing worker-specific options, like
    `--limit-concurrency`. We cannot pass them as CLI options, but we can
    pass them as env variables and inject them during startup to
    UvicornWorker.CONFIG_KWARGS.

    Supported parameters:
    `UVICORN_LIMIT_CONCURRENCY`
    """

    CONFIG_KWARGS = {
        "loop": "asyncio",
        "http": "h11",
        "lifespan": "off",
        "limit_concurrency": to_int(os.getenv("UVICORN_LIMIT_CONCURRENCY"), None),
    }
