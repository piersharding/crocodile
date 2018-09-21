MAKE_DBG ?= ""
KUBE_NAMESPACE ?= "mpi"
MPI_CLUSTER_NAME ?= "crocodile"
NODE ?= minikube
REPLICAS ?= 1
NO_PROCESS ?= 1
PULL_SECRET ?= ""
GITLAB_USER ?= ""
CI_BUILD_TOKEN ?= ""
CI_REGISTRY = gitlab.catalyst.net.nz:4567
CI_REGISTRY_IMAGE ?= $(CI_REGISTRY)/piers/k8s-hack/kube-grid
NFS_SERVER ?= 192.168.0.168
GITLAB_USER_EMAIL ?= ""
KUBE_OPENMPI_REPOSITORY ?= ubuntu
KUBE_OPENMPI_VERSION ?= 18.04
# KUBE_OPENMPI_REPOSITORY ?= gitlab.catalyst.net.nz:4567/piers/k8s-hack/kube-openmpi
# KUBE_OPENMPI_VERSION ?= 0.7.0
#KUBE_OPENMPI_PKG ?= libopenmpi-dev
KUBE_OPENMPI_PKG ?=
HOST ?= docker
DOCKER_HOST ?= tcp://$(HOST):2375
NAME = grid
IMG ?= $(NAME)_img
TAG ?= ubuntu18.04
DOCKER_IMAGE ?= $(IMG):$(TAG)
DOCKERFILE ?= Dockerfile
CACHE ?=
DOCKER = docker
DOCKER_REPO ?= ""
# CROCODILE_REPO ?= https://github.com/SKA-ScienceDataProcessor/crocodile.git
CROCODILE_REPO ?= https://github.com/piersharding/crocodile.git
DOCKER_USER ?= ""
DOCKER_PASSWORD ?= ""
CURRENT_DIR = $(shell pwd)

KUBE_OPENMPI_VERSION ?= 0.7.0
REPOSITORY ?= gitlab.catalyst.net.nz:4567/piers/k8s-hack/kube-openmpi

OPENMPI_VERSION ?= 2.1.2
WITH_OPENMPI_BUILD ?= false

# Args for SSH Uer embedded in container images
SSH_USER ?= openmpi
SSH_UID ?= 1000
SSH_GID ?= 1000

# Args for Base Image
UBUNTU_REPOSITORY ?= ubuntu
UBUNTU_TAG ?= 18.04

TEST_PATH ?= tmp

# do we enable RADOS on the crocodile build?
RADOS ?=
GRID_RADOS ?=

# define overides for above variables in here
-include PrivateRules.mak

HDF5_INC=/usr/include/hdf5/serial
HDF5_LIB=/usr/lib/x86_64-linux-gnu/hdf5/serial

CFLAGS += -Wall -fopenmp -ffast-math -I$(HDF5_INC) -O2 $(RADOS)
LDFLAGS += -fopenmp -O2
LDLIBS = -L$(HDF5_LIB) -lm -lhdf5 -lfftw3
ifdef RADOS
	LDLIBS += -lrados
endif
CC = mpicc

GRID_OBJS = main.o grid.o hdf5.o perf.o
TEST_RECOMBINE_OBJS = recombine.o test_recombine.o grid.o hdf5.o
BENCH_RECOMBINE_OBJS = recombine.o bench_recombine.o hdf5.o config.o producer.o streamer.o grid.o
CONFIG_OBJS = test_config.o config.o recombine.o  hdf5.o

grid : $(GRID_OBJS)
test_recombine : $(TEST_RECOMBINE_OBJS)
recombine : $(BENCH_RECOMBINE_OBJS)
test_config : $(CONFIG_OBJS)

rados_file_create:
	$(CC) h5rados_file_create.c $(LDFLAGS) $(LDLIBS) -lrados -o h5rados_file_create

rados_dset_create:
	$(CC) h5rados_dset_create.c $(LDFLAGS) $(LDLIBS) -lrados -o h5rados_dset_create

rados_dset_write:
	$(CC) h5rados_dset_write.c $(LDFLAGS) $(LDLIBS) -lrados -o h5rados_dset_write

rados_dset_read:
	$(CC) h5rados_dset_read.c $(LDFLAGS) $(LDLIBS) -lrados -o h5rados_dset_read

.PHONY: clean
clean :
	rm -f $(GRID_OBJS) $(BENCH_RECOMBINE_OBJS) $(TEST_RECOMBINE_OBJS) $(CONFIG_OBJS) grid test_recombine recombine test_config
	rm -f Dockerfile.echo Dockerfile.opr

build:
	  # --build-arg UBUNTU_BASED_BASE_IMAGE=$(KUBE_OPENMPI_REPOSITORY):$(KUBE_OPENMPI_VERSION) \
	$(DOCKER) build $(CACHE) \
	  --build-arg UBUNTU_BASED_BASE_IMAGE=$(UBUNTU_REPOSITORY):$(UBUNTU_TAG) \
	  --build-arg OPENMPI_VERSION=$(OPENMPI_VERSION) \
	  --build-arg WITH_OPENMPI_BUILD=$(WITH_OPENMPI_BUILD) \
	  --build-arg SSH_USER=$(SSH_USER) \
	  --build-arg SSH_UID=$(SSH_UID) \
	  --build-arg SSH_GID=$(SSH_GID) \
	  --build-arg 'arg_crocodile_repo=$(CROCODILE_REPO)' \
	  --build-arg 'arg_grid_rados=$(GRID_RADOS)' \
	  --build-arg 'arg_openmpi_pkg=$(KUBE_OPENMPI_PKG)' \
	  -t $(DOCKER_IMAGE) -f $(DOCKERFILE) .

push: build
	@echo ""
	@echo "*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*"
	@echo "Pushing Image  ... :"
	@echo "DOCKER_IMAGE: $(DOCKER_IMAGE)"
	@echo "Repo: $(DOCKER_REPO):$(TAG)"
	@echo "*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*"

	docker tag $(DOCKER_IMAGE) $(DOCKER_REPO):$(TAG)
	docker push $(DOCKER_REPO):$(TAG)

run:
	@CTNR=`$(DOCKER) ps -q -f name=$(NAME)` && \
	if [ -n "$${CTNR}" ]; then $(DOCKER) rm -f $(NAME); fi
	@echo ''
	@echo '#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#'
	@echo ' booting container, now run "make test_test_config"'
	@echo '                     or run "make test_test_recombine"'
	@echo '#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#'
	@echo ''


	echo $(DOCKER) run --rm --name $(NAME) --hostname $(NAME) \
					-w /src/crocodile/examples/grid \
					--volume $$(pwd)/../../data:/src/crocodile/data \
		            -ti $(DOCKER_IMAGE) bash

	$(DOCKER) run --rm --name $(NAME) --hostname $(NAME) \
					-w /src/crocodile/examples/grid \
					--volume $$(pwd)/../../data:/src/crocodile/data \
		            -ti $(DOCKER_IMAGE) bash

test: build run

test_test_config:
	mkdir -p $(TEST_PATH)
	./test_config $(TEST_PATH)/test_file

test_test_recombine:
	mpirun --allow-run-as-root -n 2 ./recombine --rec-set=T05

test_h5rados_file_create:
	./h5rados_file_create testfilecreate1.h5

test_h5rados_dset_create:
	./h5rados_dset_create testfilecreate1.h5 test1 2 2

test_h5rados_dset_write:
	./h5rados_dset_write testfilecreate1.h5 test1

test_h5rados_dset_read:
	./h5rados_dset_read testfilecreate1.h5 test1

h5radostests: test_h5rados_file_create test_h5rados_dset_create test_h5rados_dset_write test_h5rados_dset_read

checkvars:
	@echo ""
	@echo "*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*"
	@echo "Variables set  ... :"
	@echo "CFLAGS: $(CFLAGS)"
	@echo "LDFLAGS: $(LDFLAGS)"
	@echo "LDLIBS: $(LDLIBS)"
	@echo "DOCKER_HOST (Docker Host - set HOST and/or DOCKER_HOST): $(DOCKER_HOST)"
	@echo "GITLAB_USER (Docker registry user - set GITLAB_USER and CI_BUILD_TOKEN also used for k8s helm deploy): $(GITLAB_USER)"
	@echo "CI_REGISTRY_IMAGE (Registry Image - set CI_REGISTRY_IMAGE): $(CI_REGISTRY_IMAGE)"
	@echo "Image: $(DOCKER_IMAGE)"
	@echo "Repo: $(CI_REGISTRY_IMAGE)"
	@echo "HOST: $(HOST)"
	@echo "*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*"

all: launch-tiller helm

k8s-clean: clean
	rm -f ssh-key.yaml
	@echo "I'm clean!"

namespace:
	kubectl describe namespace $(KUBE_NAMESPACE) || kubectl create namespace $(KUBE_NAMESPACE)

# ACLs must be applied to the default role so that configmaps can be accessed
tiller-acls: namespace
	kubectl describe namespace $(KUBE_NAMESPACE) ||  kubectl create namespace $(KUBE_NAMESPACE)
	kubectl apply -f tiller-acls.yml
	kubectl apply -f mpi-in-mpi.yml

launch-tiller: tiller-acls
	helm init --service-account tiller \
	  --tiller-namespace $(KUBE_NAMESPACE) \
	  --upgrade

ssh-key.yaml:
	./gen-ssh-key.sh

regisry-creds: namespace
	kubectl create secret -n $(KUBE_NAMESPACE) \
	  docker-registry $(PULL_SECRET) \
	 --docker-server=$(CI_REGISTRY) \
	 --docker-username=$(GITLAB_USER) \
	 --docker-password=$(CI_BUILD_TOKEN) \
	 --docker-email=$(GITLAB_USER_EMAIL) \
	-o yaml --dry-run | kubectl replace -n $(KUBE_NAMESPACE) --force -f -

template: ssh-key.yaml
	helm template chart --namespace $(KUBE_NAMESPACE) \
	  --name $(MPI_CLUSTER_NAME) \
	  -f values.yaml \
	  -f ssh-key.yaml \
	  --set image.repository=$(CI_REGISTRY_IMAGE) \
	  --set image.tag=$(TAG) \
	  --set image.pullSecrets.name=$(PULL_SECRET) \
	  --set image.pullPolicy=Always \
	  --set nodeSelector."kubernetes\.io/hostname"=$(NODE) \
	  --set mpiWorkers.num=$(REPLICAS) \
	    > mpi.yml

helm: template regisry-creds
	kubectl -n $(KUBE_NAMESPACE) apply -f mpi.yml

k8s-test:
	kubectl get -n $(KUBE_NAMESPACE) po $(MPI_CLUSTER_NAME)-master
	# You can run mpiexec now via 'kubectl exec'!
	# hostfile is automatically generated and located '/kube-openmpi/generated/hostfile'
	kubectl -n $(KUBE_NAMESPACE) exec -it $(MPI_CLUSTER_NAME)-master -c mpi-master -- mpiexec --allow-run-as-root \
	  --hostfile /kube-openmpi/generated/hostfile \
	  --mca orte_keep_fqdn_hostnames 1 \
	  --display-map -n $$(($(REPLICAS)+1)) -npernode 1 \
	  sh -c 'echo $$(hostname).crocodile:hello'

k8s-recombine:
	echo $$((($(REPLICAS)+1)*$(NO_PROCESS)))
	kubectl -n $(KUBE_NAMESPACE) exec -it $(MPI_CLUSTER_NAME)-master -c mpi-master -- \
	mpirun --hostfile /kube-openmpi/generated/hostfile \
	       --mca orte_keep_fqdn_hostnames 1 \
	       -wd /src/crocodile/examples/grid \
	       -v \
	       --allow-run-as-root \
	       --mca btl_tcp_if_exclude lo,docker0 \
	       --report-bindings \
	       --display-map \
	       --timestamp-output \
	       --get-stack-traces \
	       --timeout 30 \
	       --report-state-on-timeout \
	       --tag-output \
	       --map-by node \
	       -np $$((($(REPLICAS)+1)*$(NO_PROCESS))) \
	       -x OMP_NUM_THREADS=16 \
	       -x OMP_PROC_BIND=spread \
	       -x OMP_PLACES=cores \
	       -x HDF5_DEBUG=trace \
	       /src/crocodile/examples/grid/recombine \
	       --rec-set=small \
	       --vis-set=lowbd2 \
	       --time=-230:230/256/64 \
	       --freq=-225e6:300e6/4096/64 \
	       /cache/out%d.h5



k8s-hdf5-test:
	echo $$((($(REPLICAS)+1)*$(NO_PROCESS)))
	kubectl -n $(KUBE_NAMESPACE) exec -it $(MPI_CLUSTER_NAME)-master -c mpi-master -- \
	mpirun --hostfile /kube-openmpi/generated/hostfile \
	       --mca orte_keep_fqdn_hostnames 1 \
	       -wd /src/crocodile/examples/grid \
	       -v \
	       --allow-run-as-root \
	       --mca btl_tcp_if_exclude lo,docker0 \
	       --report-bindings \
	       --display-map \
	       --timestamp-output \
	       --tag-output \
	       --map-by node \
	       -np $$((($(REPLICAS)+1)*$(NO_PROCESS))) \
	       -x OMP_PROC_BIND=spread \
	       -x OMP_PLACES=cores \
	       /src/crocodile/examples/grid/h5rados_file_create \
	       testfilecreatempi1.h5


# variable options:
# OMP_NUM_THREADS=32,16,12
# OMP_PROC_BIND=true,spread
# OMP_PLACES=sockets,cores
	       # -npernode 2 \
# -npernode 2,4,8
	       # --mca btl tcp,sm,self \
	       # --mca btl_tcp_if_include eth0 \

#  mpirun -np <2*nodes> -npernode 1 -bynode ...
# mpi_tasks_per_node=2
# application="/src/crocodile/examples/grid/recombine"
# export OMP_NUM_THREADS=16
# np=$[${numnodes}*${mpi_tasks_per_node}]
# CMD="mpirun -prepend-rank -ppn 1 -npernode 2 /src/crocodile/examples/grid/recombine $options"


delete: template
	kubectl -n $(KUBE_NAMESPACE) delete -f mpi.yml

rmi:
	$(DOCKER) rmi $(DOCKER_IMAGE)

nfs:
	CONTAINER_EXISTS=$$($(DOCKER) ps -aqf ancestor=itsthenetwork/nfs-server-alpine) && \
	if [ -n "$${CONTAINER_EXISTS}" ]; then $(DOCKER) rm -f $${CONTAINER_EXISTS}; fi
	docker run -d --name nfs --net=host --privileged -p 2049:2049 \
	-v /home/piers/git/private/SKA-crocodile/data:/data \
	-e SHARED_DIRECTORY=/data itsthenetwork/nfs-server-alpine:latest

	# -v $$(pwd)/../../data:/data \


services: nfs

.ONESHELL:
Dockerfile.echo:
	cat <<- EOF > $@
		FROM gitlab.catalyst.net.nz:4567/piers/k8s-hack/kube-grid:openmpi18.04
		MAINTAINER Piers Harding "piers@catalyst.net.nz"
		CMD mpiexec --allow-run-as-root \
			--display-map \
			sh -c 'echo $$(hostname).crocodile:hello'
	EOF

.ONESHELL:
Dockerfile.opr:
	cat <<- EOF > $@
		FROM gitlab.catalyst.net.nz:4567/piers/k8s-hack/kube-grid:openmpi18.04
		MAINTAINER Piers Harding "piers@catalyst.net.nz"
		CMD mpiexec --allow-run-as-root \
			--display-map \
			sh -c 'echo $$(hostname).crocodile:hello'
		CMD mpirun \
		       -wd /src/crocodile/examples/grid \
		       -v \
		       --allow-run-as-root \
		       --mca btl_tcp_if_exclude lo,docker0 \
		       --report-bindings \
		       --display-map \
		       --timestamp-output \
		       --tag-output \
		       --map-by node \
		       -np $$((($(REPLICAS)+1)*$(NO_PROCESS))) \
		       -x OMP_NUM_THREADS=16 \
		       -x OMP_PROC_BIND=spread \
		       -x OMP_PLACES=cores \
		       /src/crocodile/examples/grid/recombine \
		       --rec-set=small \
		       --vis-set=lowbd2 \
		       --time=-230:230/256/64 \
		       --freq=-225e6:300e6/4096/64 \
		       /cache/out%d.h5
	EOF

echo: Dockerfile.echo
	docker build -t $(IMG):echo -f Dockerfile.echo .
	docker tag $(IMG):echo $(DOCKER_REPO):echo
	docker push $(DOCKER_REPO):echo

opr: Dockerfile.opr
	docker build -t $(IMG):opr -f Dockerfile.opr .
	docker tag $(IMG):opr $(DOCKER_REPO):opr
	docker push $(DOCKER_REPO):opr
