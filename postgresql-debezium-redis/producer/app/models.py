"""Defines the `SQLAlchemy` models."""

from common import engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, declared_attr

Base = declarative_base()


class Test(Base):
    """Test database."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    pkey = Column(Integer, autoincrement=True, primary_key=True)
    nickname = Column(String(64))
    fullname = Column(String(128))


if __name__ == "__main__":
    Base.metadata.create_all(engine)
