# Module `app`

Listens to `Redis` on the given topic; print the parsed/inferred SQL statement.

# Module `common`

Common objects used in the other modules.

**Functions:**

* [`json_to_namespace()`](#commonjson_to_namespace)
* [`null_is_null()`](#commonnull_is_null)

## Functions

### `common.json_to_namespace`

```python
json_to_namespace(s: str) -> SimpleNamespace:
```

Convert a nested `JSON` into nested objects.

**Parameters:**

* `s` [`str`]: Input [valid] `JSON`.

**Returns:**

* [`types.SimpleNamespace`]: Nested objects.

### `common.null_is_null`

```python
null_is_null(func: typing.Callable) -> typing.Callable:
```

Decorator to replace `'NULL'` by `NULL` (remove single quote).

# Module `parsers`

Defines the parsers to infer original statements.

**Classes:**

* [`Parser`](#parsersparser)
* [`PostgreSQLParser`](#parserspostgresqlparser)

## Classes

### `parsers.Parser`

High-level parser object inherited by all parsers.

**Methods:**

* [`parse_event_key()`](#parsersparserparse_event_key)
* [`parse_event_value()`](#parsersparserparse_event_value)

#### Constructor

```python
Parser(key: typing.Dict[str, str], value: typing.Dict[str, str])
```

Pre-parse some contents out of .

**Parameters:**

* `key` [`typing.Dict[str, str]`]: `JSON`-formatted key of the event (`Kafka` schema).
* `value` [`typing.Dict[str, str]`]: `JSON`-formatted value of the event.

**Attributes:**

* `schema` [`str`]: `PostgreSQL` schema in which the event happened.
* `tablename` [`str`]: Name of the table impacted by the event.
* `operation` [`str`]: Database operation that triggered the event:`c` for `INSERT`, `d` for
    `DELETE`, `r` for `READ`, `t` for `TRUNCATE`, `u` for `UPDATE`. `r` should
    only happen during snapshot creation, and `t` only if requested in the
    `Debezium` connector configuration (see
    [documentation](https://debezium.io/documentation/reference/connectors/postgresql.html#postgresql-property-truncate-handling-mode)).
* `colums` [`typing.Tuple[str]`]: List of table columns.
* `values` [`typing.Tuple[str]`]: List of modified values.

#### Methods

##### `parsers.Parser.parse_event_key`

```python
parse_event_key() -> str:
```

Implement event key parsing (`Kafka` stuff; method to overload if needed).

**Returns:**

* [`str`]: Parsed event key.

##### `parsers.Parser.parse_event_value`

```python
parse_event_value() -> str:
```

Implement event **value** parsing (actual database event).

**Returns:**

* [`str`]: Event value as a SQL statement.

### `parsers.PostgreSQLParser`

Dedicated `PostgreSQL` [`Debezium`-generated] events parser.

Inherits from the `Parser` object; see associated constructor for more details.

See also the
[official documentation](https://debezium.io/documentation/reference/connectors/postgresql.html#postgresql-events)
for a full description of the parsed content.

**Methods:**

* [`parse_c()`](#parserspostgresqlparserparse_c)
* [`parse_u()`](#parserspostgresqlparserparse_u)
* [`parse_d()`](#parserspostgresqlparserparse_d)

#### Constructor

```python
PostgreSQLParser()
```

#### Methods

##### `parsers.PostgreSQLParser.parse_c`

```python
parse_c() -> str:
```

Parse an `INSERT` (*e.g.*, create) event.

**Returns:**

* [`str`]: Parsed `SQL` statement.

**Decoration** via `@null_is_null`.

##### `parsers.PostgreSQLParser.parse_u`

```python
parse_u() -> str:
```

Parse an `UPDATE` event.

**Returns:**

* [`str`]: Parsed `SQL` statement.

**Decoration** via `@null_is_null`.

##### `parsers.PostgreSQLParser.parse_d`

```python
parse_d() -> str:
```

Parse an `DELETE` event.

**Returns:**

* [`str`]: Parsed `SQL` statement.
