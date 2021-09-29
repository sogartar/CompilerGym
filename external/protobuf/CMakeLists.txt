project(protobuf)
cmake_minimum_required(VERSION 3.15)

include(ExternalProject)
include(ProcessorCount)

find_package(Git REQUIRED)

ProcessorCount(_JOBS)
ExternalProject_Add(
  protobuf
  PREFIX "${CMAKE_CURRENT_BINARY_DIR}/protobuf"
  GIT_REPOSITORY "https://github.com/protocolbuffers/protobuf.git"
  GIT_TAG fde7cf7358ec7cd69e8db9be4f1fa6a5c431386a #v3.13.0
  CONFIGURE_COMMAND ""
  BUILD_COMMAND ""
  INSTALL_COMMAND ""
)

ExternalProject_Add_Step(protobuf build_protobuf
  ALWAYS TRUE
  COMMAND
    "${CMAKE_COMMAND}" -E env "CC=${CMAKE_C_COMPILER}" "CXX=${CMAKE_CXX_COMPILER}"
      "${CMAKE_COMMAND}"
        -C "${CMAKE_CURRENT_BINARY_DIR}/protobuf_initial_cache.cmake"
        "-DGIT_EXECUTABLE=${GIT_EXECUTABLE}"
        "-DGIT_REPOSITORY_DIR=${CMAKE_CURRENT_BINARY_DIR}/protobuf/src/protobuf"
        "-DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}"
        -P "${CMAKE_CURRENT_SOURCE_DIR}/build_protobuf.cmake"
  DEPENDEES update
  WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/protobuf/src/protobuf"
)
