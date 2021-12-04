cg_add_all_subdirs()

cg_py_test(
  NAME
    connection_test
  SRCS
    "connection_test.py"
  DEPS
    compiler_gym::compiler_gym
    compiler_gym::envs::envs
    compiler_gym::service::service
    tests::test_main
)
