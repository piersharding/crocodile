ARG UBUNTU_BASED_BASE_IMAGE
FROM $UBUNTU_BASED_BASE_IMAGE

ARG arg_crocodile_repo
RUN \
    echo "Cloning crocodile repo from: ${arg_crocodile_repo}"

ARG arg_openmpi_pkg
RUN \
    echo "Adding packages: ${arg_openmpi_pkg}"

MAINTAINER Piers Harding "piers@catalyst.net.nz"

ARG SSH_USER=openmpi
ENV SSH_USER=$SSH_USER
ARG SSH_UID=1000
ARG SSH_GID=1000
ARG OPENMPI_VERSION
ARG WITH_OPENMPI_BUILD="false"
ARG HOME=/home/$SSH_USER

ENV LANG en_NZ.UTF-8
ENV LANGUAGE en_NZ.UTF-8
ENV LC_ALL en_NZ.UTF-8
ENV HOME /root
# Disable prompts from apt.
ENV DEBIAN_FRONTEND noninteractive

# install ssh and basic dependencies
RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
      locales wget ca-certificates ssh build-essential && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN \
    apt-get update -y && \
    apt-get install -y locales tzdata net-tools dnsutils telnet iproute2 \
            iperf3 fio vim-tiny bash-completion software-properties-common \
            build-essential curl wget fonts-liberation ca-certificates && \
    echo "Setting locales  ..." && /usr/sbin/locale-gen en_US.UTF-8 && \
    /usr/sbin/locale-gen en_NZ.UTF-8 && \
    echo "Setting timezone ..." &&  /bin/echo 'Pacific/Auckland' | tee /etc/timezone && DEBIAN_FRONTEND=noninteractive dpkg-reconfigure --frontend noninteractive tzdata

    # apt-get install -y git make gcc libhdf5-dev libfftw3-dev libopenmpi-dev

RUN \
    apt-get install -y git make gcc \
                       autoconf automake gfortran \
                       libtool libtool-bin \
                       zlib1g-dev libsz2 libaec-dev \
                       librados-dev libfftw3-dev ${arg_openmpi_pkg}
    # apt-get install -y git make gcc libhdf5-dev libfftw3-dev ${arg_openmpi_pkg}

#
# install openmpi
#
RUN echo "WITH_OPENMPI_BUILD=$WITH_OPENMPI_BUILD"
RUN cd /tmp && \
  if [ "$WITH_OPENMPI_BUILD" = "true" ]; then \
  wget -q https://www.open-mpi.org/software/ompi/v$(echo $OPENMPI_VERSION | sed -e s'/\(.*\)\.[0-9]/\1/')/downloads/openmpi-$OPENMPI_VERSION.tar.bz2 && \
  tar -xjf openmpi-$OPENMPI_VERSION.tar.bz2 && \
  cd /tmp/openmpi-$OPENMPI_VERSION && \
  ./configure -v --prefix=/usr --enable-mpi-thread-multiple \
   --enable-languages=c,ada,c++,go,d,fortran,objc,obj-c++ \
   --enable-shared --enable-linker-build-id --libexecdir=/usr/lib \
   --without-included-gettext --enable-threads=posix --libdir=/usr/lib \
   --enable-nls --with-sysroot=/ --enable-clocale=gnu \
   --enable-libstdcxx-debug --enable-libstdcxx-time=yes \
   --with-default-libstdcxx-abi=new --enable-gnu-unique-object \
   --disable-vtable-verify --enable-libmpx --enable-plugin \
   --with-system-zlib --disable-browser-plugin --enable-java-awt=gtk \
   --enable-gtk-cairo --with-arch-directory=amd64 \
   --enable-objc-gc --enable-multiarch --disable-werror --with-arch-32=i686 \
   --with-abi=m64 --with-multilib-list=m32,m64,mx32 --enable-multilib \
   --with-tune=generic --enable-checking=release && \
  make -j2 && \
  make install && \
  rm -r /tmp/openmpi-$OPENMPI_VERSION; \
  else \
  apt-get update -y && \
  apt-get update && apt install -y \
   libopenmpi-dev libopenmpi2 openmpi-common openmpi-bin; \
  fi && \
  mpirun -V && \
  rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
  # if ! grep "cosmic universe" /etc/apt/sources.list; then echo "deb http://nz.archive.ubuntu.com/ubuntu/ cosmic universe" >> /etc/apt/sources.list;fi


# build HDF5
RUN \
    git clone https://bitbucket.hdfgroup.org/scm/~nfortne2/hdf5_naf.git \
     --branch hdf5_rados --single-branch --depth 1 /tmp/src && \
    cd /tmp/src && \
    ./autogen.sh && \
    export CC=/usr/bin/mpicc && \
    export LIBS="-lrados" && \
    export CPPFLAGS="-I/usr/lib/x86_64-linux-gnu/openmpi/include/openmpi -I/usr/lib/x86_64-linux-gnu/openmpi/include/openmpi/opal/mca/event/libevent2022/libevent -I/usr/lib/x86_64-linux-gnu/openmpi/include/openmpi/opal/mca/event/libevent2022/libevent/include -I/usr/lib/x86_64-linux-gnu/openmpi/include" && \
    export LDFLAGS="-pthread -L/usr/lib -L/usr/lib/x86_64-linux-gnu/openmpi/lib -lmpi_cxx -lmpi -lrados -lpthread -lsz -lz -ldl -lm" && \
    ./configure --prefix=/usr --host=x86_64-linux-gnu \
          --build=x86_64-linux-gnu \
           --enable-parallel=yes \
          --libdir=/usr/lib/x86_64-linux-gnu \
          --mandir=/usr/share/man \
          --with-default-plugindir=/usr/lib/x86_64-linux-gnu/hdf5/plugins \
          --with-pthread \
          --enable-unsupported \
          --enable-shared \
           --enable-build-mode=production \
          --disable-sharedlib-rpath --with-zlib --with-default-api-version=v18 \
          --with-szlib \
          --enable-fortran \
          --enable-threadsafe --enable-cxx && \
          make VERBOSE=1 V=1 && \
          make check-s && \
          make install && \
          cd /tmp && rm -rf /tmp/src

# Create ssh user(openmpi) and setup ssh key dir
# - ssh identity file and authorized key file is expected to
#   be mounted at /ssh-keys/$SSH_USER
RUN addgroup --gid $SSH_GID $SSH_USER
RUN adduser -q --gecos "" --disabled-password --uid $SSH_UID --gid $SSH_GID $SSH_USER
RUN mkdir -p /ssh-key/$SSH_USER && chown -R $SSH_USER:$SSH_USER /ssh-key/$SSH_USER
RUN mkdir -p /.sshd/host_keys && \
  chown -R $SSH_USER:$SSH_USER /.sshd/host_keys && chmod 700 /.sshd/host_keys
RUN mkdir -p /.sshd/user_keys/$SSH_USER && \
  chown -R $SSH_USER:$SSH_USER /.sshd/user_keys/$SSH_USER && chmod 700 /.sshd/user_keys/$SSH_USER
VOLUME /ssh-key/$SSH_USER

RUN mkdir -p $HOME && chown $SSH_USER:$SSH_USER $HOME && chmod 755 $HOME
VOLUME $HOME

COPY rootfs /

EXPOSE 2022

# sshd can be run either by root or $SSH_USER
CMD ["/init.sh"]

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
    echo "Are we enabling RADOS: ${arg_grid_rados}"

RUN cd /src/crocodile/examples/grid \
    && make clean \
    && make test_config ${arg_grid_rados} \
    && make recombine ${arg_grid_rados} \
    && make grid ${arg_grid_rados}

COPY ./h5* /src/crocodile/examples/grid/
COPY ./ceph.conf /src/crocodile/examples/grid/

RUN cd /src/crocodile/examples/grid \
    && make rados_file_create \
    && make rados_dset_create \
    && make rados_dset_write \
    && make rados_dset_read

# MPI thread restriction
ENV OMP_NUM_THREADS 16

# vim:set ft=dockerfile:
