cg_add_all_subdirs()

cg_py_test(
  NAME "actions_test"
  SRCS "actions_test.py"
  DEPS
    compiler_gym::compiler_gym
    tests::test_main
)
