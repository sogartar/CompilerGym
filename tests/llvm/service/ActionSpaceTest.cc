// Copyright (c) Facebook, Inc. and its affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.
#include <gtest/gtest.h>

#include <magic_enum.hpp>

#include "compiler_gym/envs/llvm/service/ActionSpace.h"
#include "tests/TestMacros.h"

using namespace ::testing;

namespace compiler_gym::llvm_service {
namespace {

TEST(ActionSpacesTest, getLlvmActionSpace) {
  const auto spaces = getLlvmActionSpaceList();
  ASSERT_EQ(spaces.size(), 1);
  ASSERT_EQ(spaces[0].space().name(), "PassesAll");
  ASSERT_EQ(spaces[0].space().value_case(), Space::ValueCase::kNamedDiscrete);
  EXPECT_EQ(spaces[0].space().named_discrete().names_size(), magic_enum::enum_count<LlvmAction>());
}

}  // anonymous namespace
}  // namespace compiler_gym::llvm_service
