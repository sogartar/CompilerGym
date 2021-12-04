# Installation

Install the latest CompilerGym release using:

    pip install -U compiler_gym

CompilerGym requires Python >= 3.6. The binary works on macOS and Linux (on
Ubuntu 18.04, Fedora 28, Debian 10 or newer equivalents).

## Building from Source

If you prefer, you may build from source. This requires a modern C++ toolchain
and bazel.

### macOS

On macOS the required dependencies can be installed using
[homebrew](https://docs.brew.sh/Installation):

```sh
brew install bazelisk buildifier clang-format hadolint prototool zlib
export LDFLAGS="-L/usr/local/opt/zlib/lib"
export CPPFLAGS="-I/usr/local/opt/zlib/include"
export PKG_CONFIG_PATH="/usr/local/opt/zlib/lib/pkgconfig"
```

Now proceed to [All platforms](#all-platforms) below.

### Linux

On debian-based linux systems, install the required toolchain using:

```sh
sudo apt install clang-9 clang-format golang libjpeg-dev libtinfo5 m4 make patch zlib1g-dev
mkdir -pv ~/.local/bin
wget https://github.com/bazelbuild/bazelisk/releases/download/v1.7.5/bazelisk-linux-amd64 -O ~/.local/bin/bazel
wget https://github.com/hadolint/hadolint/releases/download/v1.19.0/hadolint-Linux-x86_64 -O ~/.local/bin/hadolint
chmod +x ~/.local/bin/bazel ~/.local/bin/hadolint
go get github.com/bazelbuild/buildtools/buildifier
GO111MODULE=on go get github.com/uber/prototool/cmd/prototool@dev
export PATH="$HOME/.local/bin:$PATH"
export CC=clang
export CXX=clang++
```


### All platforms

We recommend using
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
to manage the remaining build dependencies. First create a conda environment
with the required dependencies:

    conda create -n compiler_gym python=3.8
    conda activate compiler_gym
    conda install -c conda-forge cmake pandoc patchelf

Then clone the CompilerGym source code using:

    git clone https://github.com/facebookresearch/CompilerGym.git
    cd CompilerGym

There are two primary git branches: `stable` tracks the latest release;
`development` is for bleeding edge features that may not yet be mature. Checkout
your preferred branch and install the python development dependencies using:

    git checkout stable
    make init

The `make init` target only needs to be run on initial setup and after pulling
remote changes to the CompilerGym repository.

Run the test suite to confirm that everything is working:

    make test

To build and install the `compiler_gym` python package, run:

    make install

**NOTE:** To use the `compiler_gym` package that is installed by `make install`
you must leave the root directory of this repository. Attempting to import
`compiler_gym` while in the root of this repository will cause import errors.

When you are finished, you can deactivate and delete the conda
environment using:

    conda deactivate
    conda env remove -n compiler_gym

## Building from source with CMake

### Dependency instructions for Ubuntu

#### CMake
Requires CMake (==3.20).
```
wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
sudo apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main"
sudo apt update
sudo apt install kitware-archive-keyring
sudo rm /etc/apt/trusted.gpg.d/kitware.gpg
sudo apt update
sudo apt install cmake=3.20\* cmake-data=3.20\*
```

#### Compiler

```
sudo apt-get install clang-9 clang++-9 lld-9 patchelf tar bzip2
```

#### Ninja
```
sudo apt-get install ninja-build
```

#### Python
```
sudo apt-get install python3 python3-pip python3-venv
```

Setup a virtual environment.
```
python3 -m venv compiler_gym_venv
source compiler_gym_venv/bin/activate
```

```
pip install --upgrade pip
# in the source directory
python -m pip install -r requirements.txt
```

#### programl
To build programl internally it requires Bazel.
```
sudo apt install apt-transport-https curl gnupg
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg
sudo mv bazel.gpg /etc/apt/trusted.gpg.d/
echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
sudo apt update && sudo apt install bazel-4.0.0
```

#### protobuf
To build protobuf internally:
```
sudo apt-get install autoconf libtool make
```

### Build speed optimization

```
# For faster rebuilds
sudo apt-get install ccacke
```

### Dependency Arguments
By default most dependencies are built together with Compiler Gym. To search for a dependency instead use:
```
-DCOMPILER_GYM_<dependency>_PROVIDER=external
```

* `COMPILER_GYM_BOOST_PROVIDER`
* `COMPILER_GYM_GFLAGS_PROVIDER`
* `COMPILER_GYM_GLOG_PROVIDER`
* `COMPILER_GYM_GRPC_PROVIDER`
* `COMPILER_GYM_GTEST_PROVIDER`
* `COMPILER_GYM_NLOHMANN_JSON_PROVIDER`
* `COMPILER_GYM_PROTOBUF_PROVIDER`

```
export SOURCE_DIR=<path to source directory>
export BOULD_DIR=<path to build directory>

cmake -GNinja \
  -DCMAKE_C_COMPILER=clang-9 \
  -DCMAKE_CXX_COMPILER=clang++-9 \
  -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache \ # For faster rebuilds, can be removed
  -DCMAKE_EXE_LINKER_FLAGS_INIT="-fuse-ld=lld" -DCMAKE_MODULE_LINKER_FLAGS_INIT="-fuse-ld=lld" -DCMAKE_SHARED_LINKER_FLAGS_INIT="-fuse-ld=lld" \ # For faster builds, can be removed
  -DPython3_FIND_VIRTUALENV=FIRST \
  -S "$SOURCE_DIR" \
  -B "$BUILD_DIR"

cmake  --build "$BUILD_DIR"
```
