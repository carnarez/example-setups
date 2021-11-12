"""Listens to `Redis` on the given topic; print the parsed/inferred SQL statement."""

from common import engine
from parsers import PostgreSQLParser
from time import sleep
from traceback import format_exc

stream = "data.public.test"

if __name__ == "__main__":
    while True:

        try:
            events = engine.xread({stream: "0-0"}, count=None)[0][1]

            for key, event in events:
                try:
                    parser = PostgreSQLParser(
                        list(event.keys())[0].decode(),
                        list(event.values())[0].decode()
                    )
                    statement = parser.parse_event_value()
                    engine.xdel(stream, key)
                 
                    print(statement)
                except:
                    print(format_exc())

        except IndexError:
            pass

        sleep(1)
