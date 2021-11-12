**[`Debezium`](https://debezium.io/) playground,
[`PostgreSQL`](https://www.postgresql.org/) &
[`Redis Streams`](https://redis.io/topics/streams-intro).** Following the quick schema:

```text
 +----------+      +------------+      +----------+      +-------+      +----------+
 | producer |----> | postgresql | <----| debezium |----> | redis | <----| consumer |
 +----------+      +------------+      +----------+      +-------+      +----------+
```

* The **producer** generates some quick [queries](producer/app/app.py) to commit to the
  database. Do not throw me the stone, those are from the `SQLAlchemy` documentation.
* The **`PostgreSQL` database** is `Debezium` source: it holds the data, _i.e._,
  receives the `SQL` queries triggering the next steps.
* Star of the show, the **`Debezium` server** listens to all `INSERT`, `UPDATE`,
  `DELETE` events emitted via the `pgoutput` native plugin. It then posts the latter
  events to `Redis Streams`.
* **`Redis Streams`** -as a cheaper alternative to `Kafka` in our case- is `Debezium`
  sink: it receives the events posted by `Debezium`.
* The **consumer** listens to the given `Redis Streams` topic, parses the messages and
  tries to print the event as emitted by the producer for further comparison.

Run with `docker-compose up --build`. Output should be (after all the initialization):

```text
dbz-prod | INSERT INTO test (nickname, fullname) VALUES (:nickname, :fullname)
dbz-prod | INSERT INTO test (nickname) VALUES (:nickname)
dbz-prod | UPDATE test SET fullname=:fullname WHERE test.nickname = :nickname_1
dbz-prod | UPDATE test SET fullname=:fullname WHERE test.nickname = :nickname_1
dbz-prod | DELETE FROM test WHERE test.nickname = :nickname_1
dbz-prod | DELETE FROM test WHERE test.nickname = :nickname_1
```

from the producer (see [`producer/app/app.py`](producer/app/app.py) file for exact
queries) and:

```text
dbz-cons | INSERT INTO public.test (nickname, fullname) VALUES ('spongebob', 'SpongeBob Squarepants')
dbz-cons | INSERT INTO public.test (nickname, fullname) VALUES ('patrick', NULL)
dbz-cons | UPDATE public.test SET nickname='spongebob', fullname='Yellow Idiot' WHERE test.pkey=3
dbz-cons | UPDATE public.test SET nickname='patrick', fullname='Patrick the Star' WHERE test.pkey=4
dbz-cons | DELETE FROM public.test WHERE test.pkey=3
dbz-cons | DELETE FROM public.test WHERE test.pkey=4
```

from the consumer.
