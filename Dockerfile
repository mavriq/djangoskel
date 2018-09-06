ARG PYTHON_VERSION=3.6
ARG RELEASE=stretch

FROM python:${PYTHON_VERSION}-slim-${RELEASE}

ARG PYTHON_VERSION=3.6
ARG RELEASE=stretch

ARG DEBIAN_FRONTEND="noninteractive"
ARG APT_GET="apt-get -y -q --no-install-recommends"

ARG PRE_DEPEND=" \
    apt-transport-https \
    ca-certificates \
    gnupg2 \
    wget \
    "

ARG PG_VERSION=10
ARG PG_REPO="deb http://apt.postgresql.org/pub/repos/apt/ ${RELEASE}-pgdg main"
ARG PG_KEY_URL="https://www.postgresql.org/media/keys/ACCC4CF8.asc"

ARG DEPEND=" \
    bash-completion \
    binutils \
    ca-certificates \
    curl \
    less \
    pgbouncer \
    postgresql-client-${PG_VERSION} \
    locales \
    wget \
"

ARG PYTHON_DEPEND="git"
ARG PIP_DEPEND=" \
    psycopg2-binary \
    ipython \
"

ENV TERM="xterm" \
    LANG="en_US.utf-8" \
    LC_ALL="en_US.utf-8" \
    LESS="-R -M -i --shift=1" \
    LESSCOLOR="always" \
    force_color_prompt="yes" \
#
    DJANGO_PRIVATE_ROOT="/srv/data/private" \
    DJANGO_STATIC_ROOT="/srv/data/static" \
    DJANGO_MEDIA_ROOT="/srv/data/media"

RUN set -x \
    && echo 'en_US.UTF-8 UTF-8' | tee /etc/locale.gen \
    && sed -re 's/# (.*history-search-(backward|forward))/\1/' -i /etc/inputrc \
    && $APT_GET update \
    && if echo "${PRE_DEPEND}" | sed -re 's/\s+//g' | grep -q . \
        ; then \
            $APT_GET install ${PRE_DEPEND} \
            && apt-mark auto ${PRE_DEPEND} \
        ; fi \
    && echo "${PG_REPO}" \
        | tee /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O- "${PG_KEY_URL}" \
        | apt-key add - \
    && $APT_GET update \
    && $APT_GET install ${DEPEND} \
    && if echo "${PIP_DEPEND}" | sed -re 's/\s+//g' | grep -q . \
        ; then \
            if echo "${PYTHON_DEPEND}" | sed -re 's/\s+//g' | grep -q . \
            ; then \
                $APT_GET install ${PYTHON_DEPEND} \
                && apt-mark auto ${PYTHON_DEPEND} \
            ; fi \
            && pip install ${PIP_DEPEND} \
        ; fi \
    && $APT_GET autoremove \
    && $APT_GET clean \
    && rm -rf \
        /root/.cache/pip \
        /var/log/apt/* \
        /var/lib/apt/lists/*

#
ADD ./pip/ /srv/pip/
ADD ./requirements.txt /srv/requirements.txt

RUN set -x \
# установка pip-пакетов, и необходимых для них зависимостей
    && cd /srv \
    && if echo "${PYTHON_DEPEND}" | sed -re 's/\s+//g' | grep -q . \
        ; then \
            $APT_GET update \
            && $APT_GET install ${PYTHON_DEPEND} \
            && apt-mark auto ${PYTHON_DEPEND} \
        ; fi \
    && pip install -r ./requirements.txt \
    && $APT_GET autoremove \
    && $APT_GET clean \
    && rm -rf \
        /root/.cache/pip \
        /var/log/apt/* \
        /var/lib/apt/lists/*

ADD ./src/ /srv/src/

WORKDIR /srv/src

VOLUME \
    /srv/data
