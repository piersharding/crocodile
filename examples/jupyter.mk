
# Template for making Jupyter notebooks. Will get included
# by Makefiles in subdirectories.

RSTs=  $(NBs:.ipynb=.rst)

JUPYTER ?= jupyter
TIMEOUT = 600

.PHONY: rst
rst: $(RSTs)

%.rst: %.ipynb ../../crocodile/synthesis.py
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=$(TIMEOUT) --to rst $<

%.html: %.rst
	${RST2HTML} $(<:.rstw=.rst)  > $@

.PHONY: clean
clean:
	rm -f ${RSTs}
