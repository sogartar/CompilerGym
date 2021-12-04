cg_add_all_subdirs()

cg_filegroup(
  NAME "service"
  FILES
    "${CMAKE_CURRENT_LIST_DIR}/gcc_service.py"
    "${CMAKE_CURRENT_LIST_DIR}/compiler_gym-gcc-service"
)
