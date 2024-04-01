import functools
import json
import typing

import bleach
from starlette.types import ASGIApp, Scope, Receive, Send


def __sanitize_array(array_values: list[typing.Any]) -> list[typing.Any]:
    for index, value in enumerate(array_values):
        if isinstance(value, dict):
            array_values[index] = {
                key: bleach.clean(value) if isinstance(value, str) else value
                for key, value in value.items()
            }
        else:
            array_values[index] = (
                bleach.clean(value) if isinstance(value, str) else value
            )
    return array_values


def sanitize(func: Receive) -> Receive:
    @functools.wraps(func)
    async def wrapper(
        *args: typing.Any, **kwargs: typing.Any
    ) -> typing.MutableMapping[str, typing.Any]:
        message = await func(*args, **kwargs)
        body = message.get("body")
        if not body:
            return message
        if not isinstance(body, bytes):
            return message
        json_body = json.loads(body)
        for key, value in json_body.items():
            if isinstance(value, dict):
                json_body[key] = {
                    key: bleach.clean(value) if isinstance(value, str) else value
                    for key, value in value.items()
                }
            elif isinstance(value, list):
                json_body[key] = __sanitize_array(value)
            else:
                json_body[key] = bleach.clean(value)
        message["body"] = bytes(json.dumps(json_body), encoding="utf-8")
        return message

    return wrapper


class SanitizeMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if "method" not in scope or scope["method"] in ("GET", "HEAD"):
            await self.app(scope, receive, send)
            return
        await self.app(scope, sanitize(receive), send)
