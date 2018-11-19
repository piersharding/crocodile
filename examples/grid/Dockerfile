ARG UBUNTU_BASED_BASE_IMAGE
FROM $UBUNTU_BASED_BASE_IMAGE

ARG arg_crocodile_repo
RUN \
    echo "Cloning crocodile repo from: ${arg_crocodile_repo}"

MAINTAINER Piers Harding "piers@catalyst.net.nz"

RUN \
    git clone "${arg_crocodile_repo}" --branch io_benchmark_k8s --single-branch --depth 1 /src/crocodile

WORKDIR /src/crocodile
ENV HOME /src/crocodile

RUN \
    cd /src/crocodile \
    && wget -qO- https://github.com/git-lfs/git-lfs/releases/download/v2.4.2/git-lfs-linux-amd64-2.4.2.tar.gz | tar xz \
    && mv git-lfs-*/git-lfs /usr/bin/ && rm -rf git-lfs-* \
    && git lfs install

COPY ./Makefile /src/crocodile/examples/grid/
COPY ./*.h /src/crocodile/examples/grid/
COPY ./*.c /src/crocodile/examples/grid/

ARG arg_grid_rados
RUN \
    echo "Are we enabling RADOS: ${arg_grid_rados}" \
    && cd /src/crocodile/examples/grid \
    && make clean \
    && make checkvars ${arg_grid_rados} \
    && make test_config ${arg_grid_rados} \
    && make recombine ${arg_grid_rados} \
    && make grid ${arg_grid_rados} \
    && rm -f *.o

COPY ./h5* /src/crocodile/examples/grid/

RUN cd /src/crocodile/examples/grid \
    && make rados_file_create \
    && make rados_dset_create \
    && make rados_dset_write \
    && make rados_dset_read

# MPI thread restriction
ENV OMP_NUM_THREADS 16

# vim:set ft=dockerfile:
