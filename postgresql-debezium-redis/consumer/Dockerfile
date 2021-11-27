FROM python:slim

ARG uid=1000

ENV PYTHONUNBUFFERED=1

RUN useradd -M -s /bin/bash -u $uid user \
 && pip install --no-cache-dir redis \
 && echo "Europe/Amsterdam" > /etc/timezone \
 && rm /etc/localtime \
 && dpkg-reconfigure -f noninteractive tzdata \
 && apt-get autoremove --allow-remove-essential -y \
 && apt-get clean -y \
 && rm -fr /tmp/* \
           /var/cache/debconf/*-old \
           /var/lib/apt \
           /var/lib/cache \
           /var/lib/dpkg \
           /var/lib/log

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

USER $uid

WORKDIR /usr/src

COPY app .

ENTRYPOINT ["/bin/bash", "/usr/local/bin/entrypoint.sh"]
