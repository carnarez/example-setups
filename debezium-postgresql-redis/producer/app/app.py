"""Submit `SQL` queries to the `PostgreSQL` database."""

from common import engine
from models import Test
from sqlalchemy import insert, delete, update
from sqlalchemy.orm import Session

statements = [
    insert(Test).values(nickname="spongebob", fullname="SpongeBob Squarepants"),
    insert(Test).values(nickname="patrick"),
    update(Test).where(Test.nickname == "spongebob").values(fullname="Yellow Idiot"),
    update(Test).where(Test.nickname == "patrick").values(fullname="Patrick the Star"),
    delete(Test).where(Test.nickname == "spongebob"),
    delete(Test).where(Test.nickname == "patrick"),
]

if __name__ == "__main__":
    with Session(engine, future=True) as session:
        for s in statements:
            print(s)
            try:
                session.execute(s)
                session.commit()
            except:
                session.rollback()
                raise
