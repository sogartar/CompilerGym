# Copyright 2020 The IREE Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include(CMakeParseArguments)

# cmake_run_binary_test()
#
# Creates a test that runs the specified binary with the specified arguments.
#
# Mirrors the bzl function of the same name.
#
# Parameters:
# NAME: name of target
# ARGS: arguments passed to the test binary.
# TEST_BINARY: binary target to run as the test.
# LABELS: Additional labels to apply to the test. The package path is added
#     automatically.
#
# Note: the DATA argument is not supported because CMake doesn't have a good way
# to specify a data dependency for a test.
#
#
# Usage:
# cmake_cc_binary(
#   NAME
#     requires_args_to_run
#   ...
# )
# cmake_run_binary_test(
#   NAME
#     requires_args_to_run_test
#   ARGS
#    --do-the-right-thing
#   TEST_BINARY
#     ::requires_args_to_run
# )

function(cmake_run_binary_test)
  if(NOT IREE_BUILD_TESTS)
    return()
  endif()

  cmake_parse_arguments(
    _RULE
    ""
    "NAME;TEST_BINARY"
    "ARGS;LABELS"
    ${ARGN}
  )

  # Prefix the test with the package name, so we get: cmake_package_name
  rename_bazel_targets(_NAME "${_RULE_NAME}")
  cmake_package_ns(_PACKAGE_NS)
  cmake_package_path(_PACKAGE_PATH)
  set(_TEST_NAME "${_PACKAGE_PATH}/${_RULE_NAME}")

  # Replace binary passed by relative ::name with iree::package::name
  rename_bazel_targets(_TEST_BINARY_TARGET "${_RULE_TEST_BINARY}")

  if(ANDROID)
    set(_ANDROID_REL_DIR "${_PACKAGE_PATH}/${_RULE_NAME}")
    set(_ANDROID_ABS_DIR "/data/local/tmp/${_ANDROID_REL_DIR}")

    # Define a custom target for pushing and running the test on Android device.
    set(_TEST_NAME ${_TEST_NAME}_on_android_device)
    add_test(
      NAME
        ${_TEST_NAME}
      COMMAND
        "${CMAKE_SOURCE_DIR}/build_tools/cmake/run_android_test.${IREE_HOST_SCRIPT_EXT}"
        "${_ANDROID_REL_DIR}/$<TARGET_FILE_NAME:${_TEST_BINARY_TARGET}>"
        ${_RULE_ARGS}
    )
    # Use environment variables to instruct the script to push artifacts
    # onto the Android device before running the test. This needs to match
    # with the expectation of the run_android_test.{sh|bat|ps1} script.
    set(
      _ENVIRONMENT_VARS
        TEST_ANDROID_ABS_DIR=${_ANDROID_ABS_DIR}
        TEST_EXECUTABLE=$<TARGET_FILE:${_TEST_BINARY_TARGET}>
        TEST_TMPDIR=${_ANDROID_ABS_DIR}/test_tmpdir
    )
    set_property(TEST ${_TEST_NAME} PROPERTY ENVIRONMENT ${_ENVIRONMENT_VARS})
  else()
    add_test(
      NAME
        ${_TEST_NAME}
      COMMAND
        "${CMAKE_SOURCE_DIR}/build_tools/cmake/run_test.${IREE_HOST_SCRIPT_EXT}"
        "$<TARGET_FILE:${_TEST_BINARY_TARGET}>"
        ${_RULE_ARGS}
    )
    set_property(TEST ${_TEST_NAME} PROPERTY ENVIRONMENT "TEST_TMPDIR=${CMAKE_BINARY_DIR}/${_NAME}_test_tmpdir")
    cmake_add_test_environment_properties(${_TEST_NAME})
  endif()

  list(APPEND _RULE_LABELS "${_PACKAGE_PATH}")
  set_property(TEST ${_TEST_NAME} PROPERTY LABELS "${_RULE_LABELS}")
endfunction()
