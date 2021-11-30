# Copyright 2020 The IREE Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# Run all(ish) IREE tests with CTest. Designed for CI, but can be run manually.
# Assumes that the project has already been built at ${REPO_ROOT}/build (e.g.
# with build_tools/cmake/clean_build.sh)

set -x
set -e

if [ -z "$BUILD_DIR" ]; then
  BUILD_DIR="$(git rev-parse --show-toplevel)/build"
fi

# Respect the user setting, but default to as many jobs as we have cores.
export CTEST_PARALLEL_LEVEL=${CTEST_PARALLEL_LEVEL:-$(nproc)}

# Respect the user setting, but default to turning off the vulkan tests
# and turning on the llvmaot ones.
export IREE_VULKAN_DISABLE=${IREE_VULKAN_DISABLE:-0}
export IREE_LLVMAOT_DISABLE=${IREE_LLVMAOT_DISABLE:-0}
# CUDA is off by default.
export IREE_CUDA_DISABLE=${IREE_CUDA_DISABLE:-1}
# The VK_KHR_shader_float16_int8 extension is optional prior to Vulkan 1.2.
# We test on SwiftShader, which does not support this extension.
export IREE_VULKAN_F16_DISABLE=${IREE_VULKAN_F16_DISABLE:-1}

# Tests to exclude by label. In addition to any custom labels (which are carried
# over from Bazel tags), every test should be labeled with the directory it is
# in.
declare -a label_exclude_args=(
  # Exclude specific labels.
  # Put the whole label with anchors for exact matches.
  # For example:
  #   ^nokokoro$
  ^nokokoro$

  # Exclude all tests in a directory.
  # Put the whole directory with anchors for exact matches.
  # For example:
  #   ^bindings/python/iree/runtime$

  # Exclude all tests in some subdirectories.
  # Put the whole parent directory with only a starting anchor.
  # Use a trailing slash to avoid prefix collisions.
  # For example:
  #   ^bindings/
)

if [[ "${IREE_VULKAN_DISABLE?}" == 1 ]]; then
  label_exclude_args+=("^driver=vulkan$")
fi
if [[ "${IREE_LLVMAOT_DISABLE?}" == 1 ]]; then
  label_exclude_args+=("^driver=dylib$")
fi
if [[ "${IREE_CUDA_DISABLE?}" == 1 ]]; then
  label_exclude_args+=("^driver=cuda$")
fi
if [[ "${IREE_VULKAN_F16_DISABLE?}" == 1 ]]; then
  label_exclude_args+=("^vulkan_uses_vk_khr_shader_float16_int8$")
fi

# Join on "|"
label_exclude_regex="($(IFS="|" ; echo "${label_exclude_args[*]?}"))"

cd "$BUILD_DIR"
ctest --timeout 900 --output-on-failure --label-exclude "${label_exclude_regex?}"
