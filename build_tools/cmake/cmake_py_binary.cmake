# Copied from https://github.com/google/iree/blob/main/build_tools/cmake/cmake_cc_binary.cmake[
# Copyright 2019 The IREE Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include(cmake_py_library)

# cmake_cc_binary()
#
# CMake function to imitate Bazel's py_binary rule.
#
# Parameters:
# NAME: name of target (see Note)
# SRCS: List of source files for the binary
# GENERATED_SRCS: List of source files for the binary that are generated by other targets
# DATA: List of other targets and files required for this binary
# DEPS: List of other libraries to be linked in to the binary targets
# PUBLIC: Add this so that this binary will be exported under iree::
# Also in IDE, target will appear in IREE folder while non PUBLIC will be in IREE/internal.
# TESTONLY: When added, this target will only be built if user passes -DIREE_BUILD_TESTS=ON to CMake.
#
# Note:
# cmake_py_binary will create a binary called ${PACKAGE_NAME}_${NAME}, e.g.
# cmake_base_foo with two alias (readonly) targets, a qualified
# ${PACKAGE_NS}::${NAME} and an unqualified ${NAME}. Thus NAME must be globally
# unique in the project.
#
function(cmake_py_binary)
  # Currently the same as adding a library.
  # When install rules are added they will need to split.
  cmake_py_library(${ARGV})
endfunction()