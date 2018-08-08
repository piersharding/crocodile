FROM ubuntu:18.04

ARG arg_crocodile_repo
RUN \
    echo "Cloning from: ${arg_crocodile_repo}"

MAINTAINER Piers Harding "piers@catalyst.net.nz"

ENV LANG en_NZ.UTF-8
ENV LANGUAGE en_NZ.UTF-8
ENV LC_ALL en_NZ.UTF-8
ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

RUN \
    apt-get update -y && \
    apt-get install -y locales tzdata net-tools vim-tiny software-properties-common \
            build-essential curl wget fonts-liberation ca-certificates && \
    echo "Setting locales  ..." && /usr/sbin/locale-gen en_US.UTF-8 && \
    /usr/sbin/locale-gen en_NZ.UTF-8 && \
    echo "Setting timezone ..." &&  /bin/echo 'Pacific/Auckland' | tee /etc/timezone && DEBIAN_FRONTEND=noninteractive dpkg-reconfigure --frontend noninteractive tzdata

RUN \
    apt-get install -y git make gcc libhdf5-dev libfftw3-dev libopenmpi-dev

RUN \
    git clone "${arg_crocodile_repo}" --branch io_benchmark --single-branch --depth 1 /src/crocodile

WORKDIR /src/crocodile
ENV HOME /src/crocodile

RUN \
    cd /src/crocodile \
    && wget -qO- https://github.com/git-lfs/git-lfs/releases/download/v2.4.2/git-lfs-linux-amd64-2.4.2.tar.gz | tar xz \
    && mv git-lfs-*/git-lfs /usr/bin/ && rm -rf git-lfs-* \
    && git lfs install

COPY Makefile /src/crocodile/examples/grid/Makefile

RUN cd /src/crocodile/examples/grid \
    && make test_config \
    && make recombine


# vim:set ft=dockerfile:
