cmake_add_all_subdirs()

cmake_filegroup(
  NAME service
  FILES
    "${CMAKE_CURRENT_LIST_DIR}/compiler_gym-loop_tool-service"
    "${CMAKE_CURRENT_LIST_DIR}/loop_tool_compilation_session.py"
)
