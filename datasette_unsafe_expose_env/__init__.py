from datasette import hookimpl
from datasette.utils.asgi import Response
import os

DEFAULT_REDACT = {"GPG_KEY", "DATABASE_URL", "DATASETTE_SECRET"}


async def env(request, datasette):
    redact = (datasette.plugin_config("datasette-unsafe-expose-env") or {}).get(
        "redact"
    ) or DEFAULT_REDACT
    output = []
    for key, value in os.environ.items():
        if key in redact:
            value = "***"
        output.append("{}={}".format(key, value))
    return Response.text("\n".join(output))


@hookimpl
def register_routes():
    return [(r"^/-/env$", env)]
