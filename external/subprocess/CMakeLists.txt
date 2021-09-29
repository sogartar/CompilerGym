project(gflags)
cmake_minimum_required(VERSION 3.15)

include(ExternalProject)

ExternalProject_Add(
  subprocess
  PREFIX "${CMAKE_CURRENT_BINARY_DIR}/subprocess"
  GIT_REPOSITORY "https://github.com/arun11299/cpp-subprocess.git"
  GIT_TAG 9c624ce4e3423cce9f148bafbae56abfd6437ea0 #tag v2.0
  CMAKE_ARGS
    -C "${CMAKE_CURRENT_BINARY_DIR}/subprocess_initial_cache.cmake"
    "-DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}"
    "-DCMAKE_CXX_FLAGS=-pthread"
)
