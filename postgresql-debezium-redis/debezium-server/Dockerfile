FROM openjdk:11-slim

ARG uid=1000

ENV DEBEZIUM_HOME=/opt/debezium \
    DEBEZIUM_VERSION=1.7.1.Final

RUN useradd -M -s /bin/bash -u $uid debezium \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends -y curl \
 && mkdir -p $DEBEZIUM_HOME/conf $DEBEZIUM_HOME/data \
 && curl -fLSs -o /tmp/debezium.tar.gz https://repo1.maven.org/maven2/io/debezium/debezium-server-dist/$DEBEZIUM_VERSION/debezium-server-dist-$DEBEZIUM_VERSION.tar.gz \
 && tar xzf /tmp/debezium.tar.gz -C $DEBEZIUM_HOME --strip-components 1 \
 && rm $DEBEZIUM_HOME/*.md $DEBEZIUM_HOME/*.txt $DEBEZIUM_HOME/run.sh \
 && chown -R debezium:debezium $DEBEZIUM_HOME \
 && echo "Europe/Amsterdam" > /etc/timezone \
 && rm /etc/localtime \
 && dpkg-reconfigure -f noninteractive tzdata \
 && apt-get autoremove --allow-remove-essential -y curl \
 && apt-get clean -y \
 && rm -fr /tmp/* \
           /var/cache/debconf/*-old \
           /var/lib/apt \
           /var/lib/cache \
           /var/lib/dpkg \
           /var/lib/log

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

USER $uid

WORKDIR $DEBEZIUM_HOME

ENTRYPOINT ["/bin/bash", "/usr/local/bin/entrypoint.sh"]
