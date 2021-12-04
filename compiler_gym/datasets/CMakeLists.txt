cg_add_all_subdirs()

cg_py_library(
  NAME
    datasets
  SRCS
    "__init__.py"
    "benchmark.py"
    "dataset.py"
    "datasets.py"
    "files_dataset.py"
    "tar_dataset.py"
  DEPS
    ::uri
    compiler_gym::service::proto::proto
    compiler_gym::util::util
    compiler_gym::validation_result
  PUBLIC
)

cg_py_library(
  NAME
    uri
  SRCS
    "uri.py"
  PUBLIC
)

### BAZEL_TO_CMAKE_PRESERVES_ALL_CONTENT_BELOW_THIS_LINE ###
