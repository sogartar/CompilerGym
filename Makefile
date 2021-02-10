define HELP
CompilerGym $(VERSION). Available targets:

Setting up
----------

    make init
        Install the build and runtime python dependencies. This should be run
        once before any other targets.


Testing
-------

    make test
        Run the test suite. Test results are cached so that incremental test
        runs are minimal and fast. Use this as your go-to target for testing
        modifications to the codebase.

    make install-test
        Build and install the python package (equivalent to 'make install'),
        then run the full test suite against the installed package, and any
        other tests that require the python package to be installed. This is
        expensive and not typically required for local development.

    make install-fuzz
        Build and install the python package (equivalent to 'make install'),
        then run the fuzz testing suite. Fuzz tests are tests that generate
        their own inputs and run in a loop until an error has been found, or
        until a minimum number of seconds have elapsed. This minimum time is
        controlled using a FUZZ_SECONDS variable. The default is 300 seconds (5
        minutes). Override this value at the command line, for example
        `FUZZ_SECONDS=60 make install-fuzz` will run the fuzz tests for a
        minimum of one minute.

    make itest
        Run the test suite continuously on change. This is equivalent to
        manually running `make test` when a source file is modified. Note that
        `make install-test` tests are not run. This requires bazel-watcher.
        See: https://github.com/bazelbuild/bazel-watcher#installation


Documentation
-------------

    make docs
        Build the HTML documentation using Sphinx. This is the documentation
        site that is hosted at <https://facebookresearch.github.io/CompilerGym>.
        The generated HTML files are in docs/build/html.

    make livedocs
        Build the HTML documentation and serve them on localhost:8000. Changes
        to the documentation will automatically trigger incremental rebuilds
        and reload the changes.


Deployment
----------

    make bdist_wheel
        Build an optimized python wheel. The generated file is in
        dist/compiler_gym-<version>-<platform_tags>.whl

    make install
        Build and install the python wheel.

    make bdist_wheel-linux
        Use a docker container to build a python wheel for linux. This is only
        used for making release builds. This requires docker.


Tidying up
-----------

    make clean
        Remove build artifacts.

    make distclean
        Clean up all build artifacts, including the build cache.

    make uninstall
        Uninstall the python package.

    make purge
        Uninstall the python package and completely remove all datasets, logs,
        and cached files. Any experimental data or generated logs will be
        irreversibly deleted!
endef
export HELP

# Configurable paths to binaries.
CC ?= clang
CXX ?= clang++
BAZEL ?= bazel
IBAZEL ?= ibazel
PANDOC ?= pandoc
PYTHON ?= python3

# Bazel build options.
BAZEL_OPTS ?=
BAZEL_BUILD_OPTS ?= -c opt
BAZEL_TEST_OPTS ?=

# The path of the repository reoot.
ROOT := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))

VERSION := $(shell cat VERSION)
OS := $(shell uname)


##############
# Setting up #
##############

.DEFAULT_GOAL := help

.PHONY: help init

help:
	@echo "$$HELP"

init:
	$(PYTHON) -m pip install -r requirements.txt


############
# Building #
############

# Files and directories generated by python disttools.
DISTTOOLS_OUTS := dist build compiler_gym.egg-info

# Post-build shenanigans to ship libLLVMPolly.so and patch the RPATH.
LLVM_SERVICE_DIR := $(ROOT)/bazel-bin/package.runfiles/CompilerGym/compiler_gym/envs/llvm/service
LLVM_POLLY_SO := $(ROOT)/bazel-bin/external/clang-llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04/lib/libLLVMPolly.so

bazel-build:
	$(BAZEL) $(BAZEL_OPTS) build $(BAZEL_BUILD_OPTS) //:package
ifeq ($(OS),Linux)
	cp -f $(LLVM_POLLY_SO) $(LLVM_SERVICE_DIR)/libLLVMPolly.so
	chmod 666 $(LLVM_SERVICE_DIR)/compiler_gym-llvm-service
	patchelf --set-rpath '$$ORIGIN' $(LLVM_SERVICE_DIR)/compiler_gym-llvm-service
	chmod 555 $(LLVM_SERVICE_DIR)/compiler_gym-llvm-service
endif

bdist_wheel: bazel-build
	$(PYTHON) setup.py bdist_wheel

bdist_wheel-linux:
	rm -rf build
	docker build -t chriscummins/compiler_gym-linux-build packaging
	docker run -v $(ROOT):/CompilerGym --rm chriscummins/compiler_gym-linux-build:latest /bin/sh -c 'cd /CompilerGym && make bdist_wheel'
	mv dist/compiler_gym-$(VERSION)-py3-none-linux_x86_64.whl dist/compiler_gym-$(VERSION)-py3-none-manylinux2014_x86_64.whl
	rm -rf build

all: docs bdist_wheel bdist_wheel-linux

.PHONY: bdist_wheel bdist_wheel-linux

#################
# Documentation #
#################

docs/source/changelog.rst: CHANGELOG.md
	echo "..\n  Generated from $<. Do not edit!\n" > $@
	echo "Changelog\n=========\n" >> $@
	$(PANDOC) --from=markdown --to=rst $< >> $@

docs/source/contributing.rst: CONTRIBUTING.md
	echo "..\n  Generated from $<. Do not edit!\n" > $@
	$(PANDOC) --from=markdown --to=rst $< >> $@

docs/source/installation.rst: README.md
	echo "..\n  Generated from $<. Do not edit!\n" > $@
	sed -n '/^## Installation/,$$p' $< | sed -n '/^## Trying/q;p' | $(PANDOC) --from=markdown --to=rst >> $@

GENERATED_DOCS := \
	docs/source/changelog.rst \
	docs/source/contributing.rst \
	docs/source/installation.rst \
	$(NULL)

gendocs: $(GENERATED_DOCS)

docs: gendocs install
	$(MAKE) -C docs html

livedocs: gendocs
	$(MAKE) -C docs livehtml


###########
# Testing #
###########

COMPILER_GYM_SITE_DATA ?= "/tmp/compiler_gym/tests/site_data"
COMPILER_GYM_CACHE ?= "/tmp/compiler_gym/tests/cache"

test:
	$(BAZEL) $(BAZEL_OPTS) test $(BAZEL_TEST_OPTS) //...

itest:
	$(IBAZEL) $(BAZEL_OPTS) test $(BAZEL_TEST_OPTS) //...

tests-datasets:
	cd .. && python -m compiler_gym.bin.datasets --env=llvm-v0 --download=cBench-v0 >/dev/null

pytest:
	mkdir -p /tmp/compiler_gym/wheel_tests
	rm -f /tmp/compiler_gym/wheel_tests/tests
	ln -s $(ROOT)/tests /tmp/compiler_gym/wheel_tests
	cd /tmp/compiler_gym/wheel_tests && pytest -n auto tests -k "not fuzz"

install-test: | install tests-datasets pytest

# The minimum number of seconds to run the fuzz tests in a loop for. Override
# this at the commandline, e.g. `FUZZ_SECONDS=1800 make fuzz`.
FUZZ_SECONDS ?= 300

fuzz:
	mkdir -p /tmp/compiler_gym/wheel_fuzz_tests
	rm -f /tmp/compiler_gym/wheel_fuzz_tests/tests
	ln -s $(ROOT)/tests /tmp/compiler_gym/wheel_fuzz_tests
	cd /tmp/compiler_gym/wheel_fuzz_tests && pytest tests -p no:sugar -x -vv -k fuzz --seconds=$(FUZZ_SECONDS)

install-fuzz: | install tests-datasets fuzz

post-install-test:
	$(MAKE) -C examples/makefile_integration clean
	SEARCH_TIME=3 $(MAKE) -C examples/makefile_integration test

.PHONY: test install-test post-install-test


################
# Installation #
################

install: bazel-build
	$(PYTHON) setup.py install

.PHONY: install


##############
# Tidying up #
##############

# A list of all filesystem locations that CompilerGym may use for storing
# files and data.
COMPILER_GYM_DATA_FILE_LOCATIONS = \
    $(HOME)/.cache/compiler_gym \
    $(HOME)/.local/share/compiler_gym \
    $(HOME)/logs/compiler_gym \
    /dev/shm/compiler_gym \
    /tmp/compiler_gym \
    $(NULL)

.PHONY: clean distclean uninstall purge

clean:
	$(MAKE) -C docs clean || true
	rm -rf $(GENERATED_DOCS) $(DISTTOOLS_OUTS)

distclean: clean
	bazel clean --expunge

uninstall:
	$(PYTHON) -m pip uninstall -y compiler_gym

purge: distclean uninstall
	rm -rf $(COMPILER_GYM_DATA_FILE_LOCATIONS)