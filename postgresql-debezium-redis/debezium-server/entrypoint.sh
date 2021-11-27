#!/bin/bash

set -e

sleep 10  # wait for postgresql/redis to start properly

exec java $DEBEZIUM_OPTS $JAVA_OPTS -cp "`ls debezium-server-*-runner.jar`":"conf":"lib/*" io.debezium.server.Main
