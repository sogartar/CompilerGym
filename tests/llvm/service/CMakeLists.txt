cg_add_all_subdirs()

cg_cc_test(
  NAME
    ActionSpaceTest
  SRCS
    "ActionSpaceTest.cc"
  DEPS
    compiler_gym::envs::llvm::service::ActionSpace
    tests::TestMacros
    tests::TestMain
  ABS_DEPS
    GTest::GTest
    magic_enum
)
