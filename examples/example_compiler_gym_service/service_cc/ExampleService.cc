// Copyright (c) Facebook, Inc. and its affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.
//
// Run the example service on a local port.
#include <fmt/format.h>

#include "compiler_gym/service/CompilationSession.h"
#include "compiler_gym/service/runtime/Runtime.h"
#include "compiler_gym/util/Unreachable.h"

const char* usage = R"(Example CompilerGym service)";

using namespace compiler_gym;
using grpc::Status;
using grpc::StatusCode;

namespace {

template <typename T>
[[nodiscard]] inline Status rangeCheck(const T& value, const T& minValue, const T& maxValue) {
  if (value < minValue || value > maxValue) {
    return Status(StatusCode::INVALID_ARGUMENT, "Out-of-range");
  }
  return Status::OK;
}

class ExampleCompilationSession final : public CompilationSession {
 public:
  using CompilationSession::CompilationSession;

  std::string getCompilerVersion() const final override { return "1.0.0"; }

  std::vector<ActionSpace> getActionSpaces() const final override {
    // The action spaces supported by this service. Here we will implement a
    // single action space, called "default", that represents a command line
    // with three options: "a", "b", and "c".
    ActionSpace space;
    space.mutable_space()->set_name("default");

    space.mutable_space()->mutable_named_discrete()->add_names("a");
    space.mutable_space()->mutable_named_discrete()->add_names("b");
    space.mutable_space()->mutable_named_discrete()->add_names("c");

    return {space};
  }

  std::vector<ObservationSpace> getObservationSpaces() const override {
    ObservationSpace ir;
    ir.mutable_space()->set_name("ir");
    ir.mutable_space()->mutable_string_value()->mutable_length_range()->set_min(0);
    ir.set_deterministic(true);
    ir.set_platform_dependent(false);

    ObservationSpace features;
    features.mutable_space()->set_name("features");
    *features.mutable_space()->mutable_int64_box()->mutable_low()->mutable_shape()->Add() = 3;
    *features.mutable_space()->mutable_int64_box()->mutable_high()->mutable_shape()->Add() = 3;
    for (int i = 0; i < 3; ++i) {
      *features.mutable_space()->mutable_int64_box()->mutable_low()->mutable_values()->Add() = -100;
      *features.mutable_space()->mutable_int64_box()->mutable_high()->mutable_values()->Add() = 100;
    }

    ObservationSpace runtime;
    runtime.mutable_space()->set_name("runtime");
    runtime.mutable_space()->mutable_double_value()->set_min(0);
    runtime.set_deterministic(false);
    runtime.set_platform_dependent(true);

    return {ir, features, runtime};
  }

  [[nodiscard]] grpc::Status init(const ActionSpace& actionSpace,
                                  const compiler_gym::Benchmark& benchmark) final override {
    VLOG(1) << "Starting a compilation session for " << benchmark.uri();
    return Status::OK;
  }

  [[nodiscard]] grpc::Status init(CompilationSession* other) final override {
    VLOG(1) << "Forking the compilation session";
    return Status::OK;
  }

  [[nodiscard]] grpc::Status applyAction(const Event& action, bool& endOfEpisode,
                                         std::optional<ActionSpace>& newActionSpace,
                                         bool& actionHadNoEffect) final override {
    const int numChoices = getActionSpaces()[0].space().named_discrete().names_size();

    // This is the index into the action space's values ("a", "b", "c") that the
    // user selected, e.g. 0 -> "a", 1 -> "b", 2 -> "c".
    const int choiceIndex = action.int64_value();
    LOG(INFO) << "Applying action " << choiceIndex;

    if (choiceIndex < 0 || choiceIndex >= numChoices) {
      return Status(StatusCode::INVALID_ARGUMENT, "Out-of-range");
    }

    // Here is where we would run the actual action to update the environment's
    // state.

    return Status::OK;
  }

  [[nodiscard]] grpc::Status computeObservation(const ObservationSpace& observationSpace,
                                                Event& observation) final override {
    std::cerr << "COMPUTING OBSERVATION" << std::endl;
    LOG(INFO) << "Computing observation " << observationSpace.space().name();
    std::cerr << "CP2" << std::endl;

    if (observationSpace.space().name() == "ir") {
      std::cerr << "IR" << std::endl;
      observation.set_string_value("Hello, world!");
    } else if (observationSpace.space().name() == "features") {
      std::cerr << "IR" << std::endl;
      *observation.mutable_int64_tensor()->mutable_shape()->Add() = 3;
      for (int i = 0; i < 3; ++i) {
        *observation.mutable_int64_tensor()->mutable_values()->Add() = 0;
      }
    } else if (observationSpace.space().name() == "runtime") {
      std::cerr << "IR" << std::endl;
      observation.set_double_value(0);
    } else {
      UNREACHABLE(fmt::format("Unhandled observation space: {}", observationSpace.space().name()));
    }

    return Status::OK;

    std::cerr << "DONE" << std::endl;
  }
};

}  // namespace

int main(int argc, char** argv) {
  runtime::createAndRunCompilerGymService<ExampleCompilationSession>(argc, argv, usage);
}
