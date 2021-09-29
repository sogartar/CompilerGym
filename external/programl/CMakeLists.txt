project(gflags)
cmake_minimum_required(VERSION 3.15)

include(ExternalProject)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../build_tools/cmake")
find_package(Bazel REQUIRED)

ExternalProject_Add(
    programl
    PREFIX "${CMAKE_CURRENT_BINARY_DIR}/programl"
    URL "https://github.com/ChrisCummins/ProGraML/archive/4f0981d7a0d27aecef3d6e918c886642b231562d.tar.gz"
    URL_HASH "SHA256=c56360aade351eda1c138a594177fcb7cd2cda2a0a6c5c0d9aa62c7f856194bd"
    DOWNLOAD_NO_EXTRACT FALSE
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
)

ExternalProject_Add_Step(programl build_programl
  ALWAYS TRUE
  COMMAND
    "${CMAKE_COMMAND}" -E env "CC=${CMAKE_C_COMPILER}" "CXX=${CMAKE_CXX_COMPILER}"
      "${Bazel_EXECUTABLE}" build
        --verbose_failures
        #--subcommands
        "--cxxopt=-std=c++${CMAKE_CXX_STANDARD}"
        #"--cxxopt=-std=c++${CMAKE_CXX_STANDARD}"
        #"--conlyopt=${CMAKE_C_FLAGS}"
        #"--linkopt=${CMAKE_STATIC_LINKER_FLAGS_INIT} ${CMAKE_SHARED_LINKER_FLAGS_INIT} ${CMAKE_EXE_LINKER_FLAGS_INIT} ${CMAKE_STATIC_LINKER_FLAGS} ${CMAKE_SHARED_LINKER_FLAGS} ${CMAKE_EXE_LINKER_FLAGS}"
        --
        //programl/graph:features
        //programl/graph:program_graph_builder
        //programl/graph/format:node_link_graph
        //programl/ir/llvm:llvm-10
        //programl/proto:programl_cc
        //programl/proto:programl
        #@com_google_absl//absl/container:flat_hash_map
        #@com_google_absl//absl/container:flat_hash_set
        @labm8//labm8/cpp:logging
        @labm8//labm8/cpp:status
        @labm8//labm8/cpp:status_macros
        @labm8//labm8/cpp:statusor
        @labm8//labm8/cpp:string
        @labm8//labm8/cpp:stringpiece
  DEPENDEES update
  WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/programl/src/programl"
)

#ExternalProject_Add_Step(programl install_programl
#  ALWAYS TRUE
#  COMMAND
#    "${CMAKE_COMMAND}" -E env "CC=${CMAKE_C_COMPILER}" "CXX=${CMAKE_CXX_COMPILER}"
#      "${Bazel_EXECUTABLE}" run -c opt //:install -- "${CMAKE_INSTALL_PREFIX}"
#  DEPENDEES build_programl
#  WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/programl/src/programl"
#)
