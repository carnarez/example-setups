"""Holds the `sqlalchemy.Engine` object used in the other modules."""

import os

from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://"
    f'{os.environ["POSTGRES_USER"]}:'
    f'{os.environ["POSTGRES_PASSWORD"]}@'
    f'{os.environ["POSTGRES_HOST"]}:'
    f'{os.environ["POSTGRES_PORT"]}/'
    f'{os.environ["POSTGRES_DB"]}',
    future=True,
)
