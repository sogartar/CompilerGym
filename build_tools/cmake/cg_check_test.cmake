# Copyright 2020 The IREE Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include(CMakeParseArguments)

# cg_check_test()
#
# Creates a test using iree-check-module for the specified source file.
#
# Mirrors the bzl rule of the same name.
#
# Parameters:
#   NAME: Name of the target
#   SRC: mlir source file to be compiled to an IREE module.
#   TARGET_BACKEND: target backend to compile for.
#   DRIVER: driver to run the module with.
#   COMPILER_FLAGS: additional flags to pass to the compiler. Bytecode
#       translation and backend flags are passed automatically.
#   RUNNER_ARGS: additional args to pass to iree-check-module. The driver
#       and input file are passed automatically.
#   LABELS: Additional labels to apply to the test. The package path and
#       "driver=${DRIVER}" are added automatically.
function(cg_check_test)
  if(NOT IREE_BUILD_TESTS)
    return()
  endif()

  # Check tests require (by way of cg_bytecode_module) some tools.
  #
  # On the host, we can either build the tools directly, if IREE_BUILD_COMPILER
  # is enabled, or reuse the tools from an existing build (or binary release).
  #
  # In some configurations (e.g. when cross compiling for Android), we can't
  # always build the tools and may depend on them from a host build.
  #
  # For now we enable check tests:
  #   On the host if IREE_BUILD_COMPILER is set
  #   Always when cross compiling (assuming host tools exist)
  #
  # In the future, we should probably add some orthogonal options that give
  # more control (such as using tools from a binary release in a runtime-only
  # host build, or skipping check tests in an Android build).
  # TODO(#4662): add flexible configurable options that cover more uses
  if(NOT IREE_BUILD_COMPILER AND NOT CMAKE_CROSSCOMPILING)
    return()
  endif()

  cmake_parse_arguments(
    _RULE
    ""
    "NAME;SRC;TARGET_BACKEND;DRIVER"
    "COMPILER_FLAGS;RUNNER_ARGS;LABELS"
    ${ARGN}
  )

  rename_bazel_targets(_NAME "${_RULE_NAME}")

  set(_MODULE_NAME "${_RULE_NAME}_module")

  if(ANDROID)
    # Android's CMake toolchain defines some variables that we can use to infer
    # the appropriate target triple from the configured settings:
    # https://developer.android.com/ndk/guides/cmake#android_platform
    #
    # In typical CMake fashion, the various strings are pretty fuzzy and can
    # have multiple values like "latest", "android-25"/"25"/"android-N-MR1".
    #
    # From looking at the toolchain file, ANDROID_PLATFORM_LEVEL seems like it
    # should pretty consistently be just a number we can use for target triple.
    set(_TARGET_TRIPLE "aarch64-none-linux-android${ANDROID_PLATFORM_LEVEL}")

    cg_bytecode_module(
      NAME
        "${_MODULE_NAME}"
      SRC
        "${_RULE_SRC}"
      FLAGS
        "-iree-mlir-to-vm-bytecode-module"
        "-mlir-print-op-on-diagnostic=false"
        "--iree-hal-target-backends=${_RULE_TARGET_BACKEND}"
        "--iree-llvm-target-triple=${_TARGET_TRIPLE}"
        ${_RULE_COMPILER_FLAGS}
      TESTONLY
    )
  else(ANDROID)
    cg_bytecode_module(
      NAME
        "${_MODULE_NAME}"
      SRC
        "${_RULE_SRC}"
      FLAGS
        "-iree-mlir-to-vm-bytecode-module"
        "-mlir-print-op-on-diagnostic=false"
        "--iree-hal-target-backends=${_RULE_TARGET_BACKEND}"
        ${_RULE_COMPILER_FLAGS}
      TESTONLY
    )
  endif(ANDROID)

  # TODO(b/146898896): It would be nice if this were something we could query
  # rather than having to know the conventions used by cg_bytecode_module.
  set(_MODULE_FILE_NAME "${_MODULE_NAME}.vmfb")

  # cg_bytecode_module does not define a target, only a custom command.
  # We need to create a target that depends on the command to ensure the
  # module gets built.
  # TODO(b/146898896): Do this in cg_bytecode_module and avoid having to
  # reach into the internals.
  set(_MODULE_TARGET_NAME "${_NAME}_module")
  add_custom_target(
    "${_MODULE_TARGET_NAME}"
     DEPENDS
       "${_MODULE_FILE_NAME}"
  )

  # A target specifically for the test. We could combine this with the above,
  # but we want that one to get pulled into cg_bytecode_module.
  add_custom_target("${_NAME}" ALL)
  add_dependencies(
    "${_NAME}"
    "${_MODULE_TARGET_NAME}"
    cg_tools_iree-check-module
  )

  cg_package_ns(_PACKAGE_NS)
  string(REPLACE "::" "/" _PACKAGE_PATH ${_PACKAGE_NS})
  set(_TEST_NAME "${_PACKAGE_PATH}/${_RULE_NAME}")

  # Case for cross-compiling towards Android.
  if(ANDROID)
    set(_ANDROID_EXE_REL_DIR "iree/modules/check")
    set(_ANDROID_REL_DIR "${_PACKAGE_PATH}/${_RULE_NAME}")
    set(_ANDROID_ABS_DIR "/data/local/tmp/${_ANDROID_REL_DIR}")

    # Define a custom target for pushing and running the test on Android device.
    set(_TEST_NAME ${_TEST_NAME}_on_android_device)
    add_test(
      NAME
        ${_TEST_NAME}
      COMMAND
        "${CMAKE_SOURCE_DIR}/build_tools/cmake/run_android_test.${IREE_HOST_SCRIPT_EXT}"
        "${_ANDROID_REL_DIR}/$<TARGET_FILE_NAME:cg_tools_iree-check-module>"
        "--driver=${_RULE_DRIVER}"
        "${_ANDROID_REL_DIR}/${_MODULE_FILE_NAME}"
        ${_RULE_RUNNER_ARGS}
    )
    # Use environment variables to instruct the script to push artifacts
    # onto the Android device before running the test. This needs to match
    # with the expectation of the run_android_test.{sh|bat|ps1} script.
    set(
      _ENVIRONMENT_VARS
        TEST_ANDROID_ABS_DIR=${_ANDROID_ABS_DIR}
        TEST_DATA=${CMAKE_CURRENT_BINARY_DIR}/${_MODULE_FILE_NAME}
        TEST_EXECUTABLE=$<TARGET_FILE:cg_tools_iree-check-module>
    )
    set_property(TEST ${_TEST_NAME} PROPERTY ENVIRONMENT ${_ENVIRONMENT_VARS})
    cg_add_test_environment_properties(${_TEST_NAME})
  else(ANDROID)
    add_test(
      NAME
        "${_TEST_NAME}"
      COMMAND
        "${CMAKE_SOURCE_DIR}/build_tools/cmake/run_test.${IREE_HOST_SCRIPT_EXT}"
        "$<TARGET_FILE:cg_tools_iree-check-module>"
        "--driver=${_RULE_DRIVER}"
        "${CMAKE_CURRENT_BINARY_DIR}/${_MODULE_FILE_NAME}"
        ${_RULE_RUNNER_ARGS}
    )
    set_property(TEST "${_TEST_NAME}" PROPERTY ENVIRONMENT "TEST_TMPDIR=${_NAME}_test_tmpdir")
    cg_add_test_environment_properties(${_TEST_NAME})
  endif(ANDROID)

  list(APPEND _RULE_LABELS "${_PACKAGE_PATH}" "driver=${_RULE_DRIVER}")
  set_property(TEST "${_TEST_NAME}" PROPERTY REQUIRED_FILES "${_MODULE_FILE_NAME}")
  set_property(TEST "${_TEST_NAME}" PROPERTY LABELS "${_RULE_LABELS}")
endfunction()


# cg_check_single_backend_test_suite()
#
# Creates a test suite of iree-check-module tests for a single backend/driver pair.
#
# Mirrors the bzl rule of the same name.
#
# One test is generated per source file.
# Parameters:
#   NAME: name of the generated test suite.
#   SRCS: source mlir files containing the module.
#   TARGET_BACKEND: target backend to compile for.
#   DRIVER: driver to run the module with.
#   COMPILER_FLAGS: additional flags to pass to the compiler. Bytecode
#       translation and backend flags are passed automatically.
#   RUNNER_ARGS: additional args to pass to the underlying iree-check-module
#       tests. The driver and input file are passed automatically. To use
#       different args per test, create a separate suite or cg_check_test.
#   LABELS: Additional labels to apply to the generated tests. The package path is
#       added automatically.
function(cg_check_single_backend_test_suite)
  if(NOT IREE_BUILD_TESTS)
    return()
  endif()

  # Note: we could check IREE_BUILD_COMPILER here, but cross compilation makes
  # that a little tricky. Instead, we let cg_check_test handle the checks,
  # meaning this function may run some configuration but generate no targets.

  cmake_parse_arguments(
    _RULE
    ""
    "NAME;TARGET_BACKEND;DRIVER"
    "SRCS;COMPILER_FLAGS;RUNNER_ARGS;LABELS"
    ${ARGN}
  )

  # Omit tests for which the specified driver or target backend is not enabled.
  # This overlaps with directory exclusions and other filtering mechanisms.
  string(TOUPPER ${_RULE_DRIVER} _UPPERCASE_DRIVER)
  if(NOT DEFINED IREE_HAL_DRIVER_${_UPPERCASE_DRIVER})
    message(SEND_ERROR "Unknown driver '${_RULE_DRIVER}'. Check IREE_ALL_HAL_DRIVERS.")
  endif()
  if(NOT IREE_HAL_DRIVER_${_UPPERCASE_DRIVER})
    return()
  endif()
  string(TOUPPER ${_RULE_TARGET_BACKEND} _UPPERCASE_TARGET_BACKEND)
  if(NOT DEFINED IREE_TARGET_BACKEND_${_UPPERCASE_TARGET_BACKEND})
    message(SEND_ERROR "Unknown backend '${_RULE_TARGET_BACKEND}'. Check IREE_ALL_TARGET_BACKENDS.")
  endif()
  if(DEFINED IREE_HOST_BINARY_ROOT)
    # If we're not building the host tools from source under this configuration,
    # such as when cross compiling, then we can't easily check for which
    # compiler target backends are enabled. Just assume all are enabled and only
    # rely on the runtime HAL driver check above for filtering.
  else()
    # We are building the host tools, so check enabled compiler target backends.
    if(NOT IREE_TARGET_BACKEND_${_UPPERCASE_TARGET_BACKEND})
      return()
    endif()
  endif()

  foreach(_SRC IN LISTS _RULE_SRCS)
    set(_TEST_NAME "${_RULE_NAME}_${_SRC}")
    cg_check_test(
      NAME
        ${_TEST_NAME}
      SRC
        ${_SRC}
      TARGET_BACKEND
        ${_RULE_TARGET_BACKEND}
      DRIVER
        ${_RULE_DRIVER}
      COMPILER_FLAGS
        ${_RULE_COMPILER_FLAGS}
      RUNNER_ARGS
        ${_RULE_RUNNER_ARGS}
      LABELS
        ${_RULE_LABELS}
    )
  endforeach()
endfunction()


# cg_check_test_suite()
#
# Creates a test suite of iree-check-module tests.
#
# Mirrors the bzl rule of the same name.
#
# One test is generated per source and backend/driver pair.
# Parameters:
#   NAME: name of the generated test suite.
#   SRCS: source mlir files containing the module.
#   TARGET_BACKENDS: backends to compile the module for. These form pairs with
#       the DRIVERS argument (due to cmake limitations they are separate list
#       arguments). The lengths must exactly match. If no backends or drivers are
#       specified, a test will be generated for every supported pair.
#   DRIVERS: drivers to run the module with. These form pairs with the
#       TARGET_BACKENDS argument (due to cmake limitations they are separate list
#       arguments). The lengths must exactly match. If no backends or drivers are
#       specified, a test will be generated for every supported pair.
#   RUNNER_ARGS: additional args to pass to the underlying iree-check-module tests. The
#       driver and input file are passed automatically. To use different args per
#       test, create a separate suite or cg_check_test.
#   LABELS: Additional labels to apply to the generated tests. The package path is
#       added automatically.
function(cg_check_test_suite)
  if(NOT IREE_BUILD_TESTS)
    return()
  endif()

  cmake_parse_arguments(
    _RULE
    ""
    "NAME"
    "SRCS;TARGET_BACKENDS;DRIVERS;RUNNER_ARGS;LABELS"
    ${ARGN}
  )

  if(NOT DEFINED _RULE_TARGET_BACKENDS AND NOT DEFINED _RULE_DRIVERS)
    set(_RULE_TARGET_BACKENDS "vmvx" "vulkan-spirv" "dylib-llvm-aot")
    set(_RULE_DRIVERS "vmvx" "vulkan" "dylib")
  endif()

  list(LENGTH _RULE_TARGET_BACKENDS _TARGET_BACKEND_COUNT)
  list(LENGTH _RULE_DRIVERS _DRIVER_COUNT)

  if(NOT _TARGET_BACKEND_COUNT EQUAL _DRIVER_COUNT)
    message(SEND_ERROR
        "TARGET_BACKENDS count ${_TARGET_BACKEND_COUNT} does not match DRIVERS count ${_DRIVER_COUNT}")
  endif()

  math(EXPR _MAX_INDEX "${_TARGET_BACKEND_COUNT} - 1")
  foreach(_INDEX RANGE "${_MAX_INDEX}")
    list(GET _RULE_TARGET_BACKENDS ${_INDEX} _TARGET_BACKEND)
    list(GET _RULE_DRIVERS ${_INDEX} _DRIVER)
    set(_SUITE_NAME "${_RULE_NAME}_${_TARGET_BACKEND}_${_DRIVER}")
    cg_check_single_backend_test_suite(
      NAME
        ${_SUITE_NAME}
      SRCS
        ${_RULE_SRCS}
      TARGET_BACKEND
        ${_TARGET_BACKEND}
      DRIVER
        ${_DRIVER}
      COMPILER_FLAGS
        ${_RULE_COMPILER_FLAGS}
      RUNNER_ARGS
        ${_RULE_RUNNER_ARGS}
      LABELS
        ${_RULE_LABELS}
    )
  endforeach()
endfunction()
