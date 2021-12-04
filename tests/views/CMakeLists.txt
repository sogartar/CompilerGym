cg_add_all_subdirs()

cg_py_test(
  NAME
    observation_test
  SRCS
    "observation_test.py"
  DEPS
    compiler_gym::service::proto::proto
    compiler_gym::views::views
    tests::test_main
)

cg_py_test(
  NAME
    reward_test
  SRCS
    "reward_test.py"
  DEPS
    compiler_gym::views::views
    tests::test_main
)
