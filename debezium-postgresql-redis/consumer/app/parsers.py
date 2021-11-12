"""Defines the parsers to infer original statements."""

import json
import typing

from common import json_to_namespace, null_is_null
from types import SimpleNamespace


class Parser:
    """High-level parser object inherited by all parsers."""

    def __init__(self, key: typing.Dict[str, str], value: typing.Dict[str, str]):
        """Pre-parse some contents out of .

        Parameters
        ----------
        key : typing.Dict[str, str]
            `JSON`-formatted key of the event (`Kafka` schema).
        value : typing.Dict[str, str]
            `JSON`-formatted value of the event.

        Attributes
        ----------
        schema : str
            `PostgreSQL` schema in which the event happened.
        tablename : str
            Name of the table impacted by the event.
        operation : str
            Database operation that triggered the event:`c` for `INSERT`, `d` for
            `DELETE`, `r` for `READ`, `t` for `TRUNCATE`, `u` for `UPDATE`. `r` should
            only happen during snapshot creation, and `t` only if requested in the
            `Debezium` connector configuration (see
            [documentation](https://debezium.io/documentation/reference/connectors/postgresql.html#postgresql-property-truncate-handling-mode)).
        colums : typing.Tuple[str]
            List of table columns.
        values : typing.Tuple[str]
            List of modified values.
        """
        self._key: SimpleNamespace = json_to_namespace(key)
        self._value: SimpleNamespace = json_to_namespace(value)

        self.schema: str = self._value.payload.source.schema
        self.tablename: str = self._value.payload.source.table

        self.operation: str = self._value.payload.op


        try:
            c = tuple(vars(self._value.payload.after).keys())
            v = tuple(vars(self._value.payload.after).values())
        except: 
            c = tuple(vars(self._value.payload.before).keys())
            v = tuple(vars(self._value.payload.before).values())

        self.columns: typing.Tuple[str] = c
        self.values: typing.Tuple[str] = tuple(["NULL" if i is None else i for i in v])

    def parse_event_key(self) -> str:
        """Implement event key parsing (`Kafka` stuff; method to overload if needed).

        Returns
        -------
        : str
            Parsed event key.
        """
        raise NotImplementedError
    
    def parse_event_value(self) -> str:
        """Implement event **value** parsing (actual database event).

        Returns
        -------
        : str
            Event value as a SQL statement.
        """
        try:
            return getattr(self, f"parse_{self.operation}")()
        except NameError:
            raise NotImplementedError(f'Cannot parse "{self.operation}" operations.')


class PostgreSQLParser(Parser):
    """Dedicated `PostgreSQL` [`Debezium`-generated] events parser.

    Inherits from the `Parser` object; see associated constructor for more details.

    See also the
    [official documentation](https://debezium.io/documentation/reference/connectors/postgresql.html#postgresql-events)
    for a full description of the parsed content.
    """

    @null_is_null
    def parse_c(self) -> str:
        """Parse an `INSERT` (*e.g.*, create) event.

        Returns
        -------
        : str
            Parsed `SQL` statement.
        """
        target = f"{self.schema}.{self.tablename}"
        columns = ", ".join([c for c in self.columns[1:]])
        values = self.values[1:]

        return f"INSERT INTO {target} ({columns}) VALUES {values}"

    @null_is_null
    def parse_u(self) -> str:
        """Parse an `UPDATE` event.

        Returns
        -------
        : str
            Parsed `SQL` statement.
        """
        target = f"{self.schema}.{self.tablename}"
        sets = ", ".join(
            [f"{c}='{v}'" for c, v in zip(self.columns[1:], self.values[1:])]
        )

        return (
            f"UPDATE {target} "
            f"SET {sets} "
            f"WHERE {self.tablename}.{self.columns[0]}={self.values[0]}"
        )

    def parse_d(self) -> str:
        """Parse an `DELETE` event.

        Returns
        -------
        : str
            Parsed `SQL` statement.
        """
        target = f"{self.schema}.{self.tablename}"

        return (
            f"DELETE FROM {target} "
            f"WHERE {self.tablename}.{self.columns[0]}={self.values[0]}"
        )
