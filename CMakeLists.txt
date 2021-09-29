cmake_minimum_required(VERSION 3.20)

if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    set(DARWIN TRUE)
endif()

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

project(compiler_gym ASM C CXX)

set(CMAKE_C_STANDARD 11 CACHE STRING "C standard to be used.")
set(CMAKE_CXX_STANDARD 17 CACHE STRING "C++ standard to be used.")

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

list(APPEND CMAKE_MODULE_PATH
  ${CMAKE_CURRENT_LIST_DIR}/build_tools/cmake/
)

include(cmake_macros)
include(cmake_copts)
include(cmake_genrule)
include(cmake_cc_binary)
include(cmake_cc_library)
include(cmake_cc_test)
include(cmake_py_binary)
include(cmake_py_library)
include(cmake_py_test)
include(cmake_python)
include(cmake_lit_test)
include(cmake_add_all_subdirs)
include(cmake_check_test)
include(cmake_run_binary_test)
include(cmake_filegroup)
include(grpc)
include(protobuf)

set(CMAKE_PYTHONPATH "$ENV{PYTHONPATH}" CACHE STRING "PYTHONPATH environment variable during build step.")
if (CMAKE_PYTHONPATH)
  string(PREPEND CMAKE_PYTHONPATH ":")
endif()
string(PREPEND CMAKE_PYTHONPATH "${CMAKE_BINARY_DIR}")
include(set_command_pythonpath)

set(DEFAULT_CMAKE_BUILD_TYPE "Release")
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "No build type selected, default to ${DEFAULT_CMAKE_BUILD_TYPE}")
  set(CMAKE_BUILD_TYPE "${DEFAULT_CMAKE_BUILD_TYPE}" CACHE STRING "Build type (default ${DEFAULT_CMAKE_BUILD_TYPE})" FORCE)
endif()

set(CMAKE_POSITION_INDEPENDENT_CODE TRUE)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

include(external/external.cmake)
add_subdirectory(compiler_gym/)
# add_subdirectory(tests/)
