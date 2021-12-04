cg_add_all_subdirs()

cg_py_library(
  NAME
    datasets
  SRCS
    "__init__.py"
    "anghabench.py"
    "chstone.py"
    "csmith.py"
  DATA
    compiler_gym::third_party::csmith::all
  DEPS
    compiler_gym::datasets::datasets
    compiler_gym::service::proto::proto
    compiler_gym::util::util
  PUBLIC
)

### BAZEL_TO_CMAKE_PRESERVES_ALL_CONTENT_BELOW_THIS_LINE ###
