cmake_add_all_subdirs()

cmake_py_library(
  NAME loop_tool
  SRCS
    "__init__.py"
    "loop_tool_env.py"
  DATA compiler_gym::envs::loop_tool::service::service
  DEPS
    compiler_gym::envs::compiler_env
    compiler_gym::service::service
    compiler_gym::service::proto::proto
    compiler_gym::service::runtime::runtime
  PUBLIC
)
