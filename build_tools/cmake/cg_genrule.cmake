include_guard(GLOBAL)

include(CMakeParseArguments)
include(cg_macros)

# cg_genrule()
#
# CMake function to imitate Bazel's genrule rule.
#
function(cg_genrule)
  cmake_parse_arguments(
    _RULE
    "PUBLIC;TESTONLY"
    "NAME;COMMAND"
    "SRCS;OUTS;DEPENDS;ABS_DEPENDS"
    ${ARGN}
  )

  if(_RULE_TESTONLY AND NOT COMPILER_GYM_BUILD_TESTS)
    return()
  endif()

  # TODO(boian): remove this renaming when call sites do not include ":" in target dependency names
  rename_bazel_targets(_DEPS "${_RULE_DEPENDS}")

  rename_bazel_targets(_NAME "${_RULE_NAME}")

  make_paths_absolute(
    PATHS ${_RULE_SRCS}
    BASE_DIR "${CMAKE_CURRENT_SOURCE_DIR}"
    RESULT_VARIABLE _SRCS
  )

  make_paths_absolute(
    PATHS ${_RULE_OUTS}
    BASE_DIR "${CMAKE_CURRENT_BINARY_DIR}"
    RESULT_VARIABLE _OUTS
  )

  list(LENGTH _OUTS _OUTS_LENGTH)
  if(_OUTS_LENGTH EQUAL 1)
    get_filename_component(_OUTS_DIR "${_OUTS}" DIRECTORY)
  else()
    set(_OUTS_DIR "${CMAKE_CURRENT_BINARY_DIR}")
  endif()

  # Substitute special Bazel references
  string(REPLACE  "$@" "${_OUTS}" _CMD "${_RULE_COMMAND}")
  string(REPLACE  "$(@D)" "${_OUTS_DIR}" _CMD "${_CMD}")
  #string(REPLACE  "$<" "\"${_SRCS}\"" _CMD "${_CMD}")

  add_custom_command(
    OUTPUT ${_OUTS}
    COMMAND bash -c "${_CMD}"
    DEPENDS ${_DEPS} ${_SRCS}
    VERBATIM
  )

  add_custom_target(${_NAME} ALL DEPENDS ${_OUTS})
  set_target_properties(${_NAME} PROPERTIES
    OUTPUTS "${_OUTS}")

  list(LENGTH _OUTS _OUTS_LENGTH)
  if(_OUTS_LENGTH EQUAL "1")
    set_target_properties(${_NAME} PROPERTIES LOCATION "${_OUTS}")
  endif()

endfunction()
