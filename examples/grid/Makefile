NAME = grid
IMG ?= $(NAME)_img
TAG ?= ubuntu18.04
DOCKER_IMAGE = $(IMG):$(TAG)
DOCKERFILE ?= Dockerfile
CACHE ?=
DOCKER = docker
DOCKER_REPO ?= ""
# CROCODILE_REPO ?= https://github.com/SKA-ScienceDataProcessor/crocodile.git
CROCODILE_REPO ?= https://github.com/piersharding/crocodile.git
DOCKER_USER ?= ""
DOCKER_PASSWORD ?= ""
CURRENT_DIR = $(shell pwd)

TEST_PATH ?= tmp

# define overides for above variables in here
-include PrivateRules.mak

HDF5_INC ?= /usr/include/hdf5/serial
HDF5_LIB ?= /usr/lib/x86_64-linux-gnu/hdf5/serial

CFLAGS += -Wall -fopenmp -ffast-math -I$(HDF5_INC) -O2
LDFLAGS += -fopenmp -O2
LDLIBS = -L$(HDF5_LIB) -lm -lhdf5 -lfftw3
CC = mpicc

GRID_OBJS = main.o grid.o hdf5.o perf.o
TEST_RECOMBINE_OBJS = recombine.o test_recombine.o grid.o hdf5.o
BENCH_RECOMBINE_OBJS = recombine.o bench_recombine.o hdf5.o config.o producer.o streamer.o grid.o
CONFIG_OBJS = test_config.o config.o recombine.o  hdf5.o

grid : $(GRID_OBJS)
test_recombine : $(TEST_RECOMBINE_OBJS)
recombine : $(BENCH_RECOMBINE_OBJS)
test_config : $(CONFIG_OBJS)

.PHONY: clean
clean :
	rm -f $(GRID_OBJS) $(BENCH_RECOMBINE_OBJS) $(TEST_RECOMBINE_OBJS) $(CONFIG_OBJS) grid test_recombine recombine test_config

build:
	$(DOCKER) build $(CACHE) --build-arg 'arg_crocodile_repo=$(CROCODILE_REPO)' \
	-t $(DOCKER_IMAGE) -f $(DOCKERFILE) .

push: build
	docker tag $(DOCKER_IMAGE) $(DOCKER_REPO)$(DOCKER_IMAGE)
	docker push $(DOCKER_REPO)$(DOCKER_IMAGE)

test: build
	@CTNR=`$(DOCKER) ps -q -f name=$(NAME)` && \
	if [ -n "$${CTNR}" ]; then $(DOCKER) rm -f $(NAME); fi
	@echo ''
	@echo '#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#'
	@echo ' booting container, now run "make test_test_config"'
	@echo '                     or run "make test_recombine"'
	@echo '#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#'
	@echo ''
	$(DOCKER) run --rm --name $(NAME) --hostname $(NAME) \
					-w /src/crocodile/examples/grid \
					--volume $$(pwd)/../../data:/src/crocodile/data \
		            -ti $(DOCKER_IMAGE) bash

test_test_config:
	mkdir -p $(TEST_PATH)
	./test_config $(TEST_PATH)/test_file

test_test_recombine:
	mpirun --allow-run-as-root -n 2 ./recombine --rec-set=T05
