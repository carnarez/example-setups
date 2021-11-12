"""Common objects used in the other modules."""

import json
import os
import typing

from redis import Redis
from types import SimpleNamespace

engine: Redis = Redis(
    password=os.environ["REDIS_PASSWORD"],
    host=os.environ["REDIS_HOST"],
    port=os.environ["REDIS_PORT"],
    db=os.environ["REDIS_DB"]
)


def json_to_namespace(s: str) -> SimpleNamespace:
    """Convert a nested `JSON` into nested objects.

    Parameters
    ----------
    s : str
        Input [valid] `JSON`.

    Returns
    -------
    : types.SimpleNamespace
        Nested objects.
    """
    return json.loads(s, object_hook=lambda d: SimpleNamespace(**d))


def null_is_null(func: typing.Callable) -> typing.Callable:
    """Decorator to replace `'NULL'` by `NULL` (remove single quote)."""

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).replace("'NULL'", "NULL")

    return wrapper
