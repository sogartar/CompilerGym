project(gflags)
cmake_minimum_required(VERSION 3.15)

include(ExternalProject)

# Note that in the Bazel build the commit hash is
# 63b254577ed77a8004a9be6ac707f3dccc4e1fd9.
# This dependency was bumped up to 2e79955ecaec85da13ac8f1245a8b2afa10d31c2
# in order for CMake to be able to find it.
# Hopefully, this does not break the build.
ExternalProject_Add(
  csmith
  PREFIX "${CMAKE_CURRENT_BINARY_DIR}/csmith"
  GIT_REPOSITORY "https://github.com/csmith-project/csmith.git"
  GIT_TAG 30dccd73b78652c4719f36572994778a5b233a4e #tag csmith-2.3.0
  CMAKE_ARGS
    -C "${CMAKE_CURRENT_BINARY_DIR}/csmith_initial_cache.cmake"
    "-DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}"
    "-DCOMPILE_DEFINITIONS=_LIBCPP_ENABLE_CXX17_REMOVED_FEATURES"
)
