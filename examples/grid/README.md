
Containerised test_config
=========================

This directory contains a containerised version of test_config,
a utility for benchmarking storage options backed by HDF5.

Building Image
--------------

The container image is based on Ubuntu:18.04.
[Install Docker](https://docs.docker.com/install/), and then run:

```bash
    $ make build
```

This will create an image: `grid_img:ubuntu18.04` .

Testing
-------

First, ensure that the data directory (in `../../data`) has been populated
using Git LFS [large file storage](https://git-lfs.github.com/).  Do this
with:

```bash
    $ git lfs pull
```

See the README.md at the root of this repository (`../../README.md`) for
further details.

Launch the test container with:

```bash
    $ make test
```

This will leave you at a prompt inside the container (exit with ctrl-D)
where you can now run the tests with:

```bash
    $ make test_run
```

The test will automatically be cleaned up on exiting the container.
