# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from compiler_gym.service.proto.compiler_gym_service_pb2 import (
    ActionSpace,
    AddBenchmarkReply,
    AddBenchmarkRequest,
    Benchmark,
    BenchmarkDynamicConfig,
    BooleanBox,
    BooleanRange,
    BooleanSequenceSpace,
    BooleanTensor,
    ByteBox,
    ByteSequenceSpace,
    BytesSequenceSpace,
    ByteTensor,
    Command,
    DictEvent,
    DictSpace,
    DiscreteSpace,
    DoubleBox,
    DoubleRange,
    DoubleSequenceSpace,
    DoubleTensor,
    EndSessionReply,
    EndSessionRequest,
    Event,
    File,
    FloatBox,
    FloatRange,
    FloatSequenceSpace,
    FloatTensor,
    ForkSessionReply,
    ForkSessionRequest,
    GetSpacesReply,
    GetSpacesRequest,
    GetVersionReply,
    GetVersionRequest,
    Int64Box,
    Int64Range,
    Int64SequenceSpace,
    Int64Tensor,
    ListEvent,
    ListSpace,
    NamedDiscreteSpace,
    ObservationSpace,
    SendSessionParameterReply,
    SendSessionParameterRequest,
    SessionParameter,
    Space,
    StartSessionReply,
    StartSessionRequest,
    StepReply,
    StepRequest,
    StringSequenceSpace,
    StringSpace,
    StringTensor,
    Opaque
)
from compiler_gym.service.proto.compiler_gym_service_pb2_grpc import (
    CompilerGymServiceServicer,
    CompilerGymServiceStub,
)
from compiler_gym.service.proto.py_converters import proto_to_action_space

__all__ = [
    "ActionSpace",
    "AddBenchmarkReply",
    "AddBenchmarkRequest",
    "Benchmark",
    "BenchmarkDynamicConfig",
    "BooleanBox",
    "BooleanRange",
    "BooleanSequenceSpace",
    "BooleanTensor",
    "ByteBox",
    "ByteSequenceSpace",
    "ByteTensor",
    "BytesSequenceSpace",
    "Command",
    "CompilerGymServiceConnection",
    "CompilerGymServiceServicer",
    "CompilerGymServiceStub",
    "ConnectionOpts",
    "DictEvent",
    "DictSpace",
    "DiscreteSpace",
    "DoubleBox",
    "DoubleRange",
    "DoubleRange",
    "DoubleSequenceSpace",
    "DoubleTensor",
    "EndSessionReply",
    "EndSessionRequest",
    "Event",
    "File",
    "FloatBox",
    "FloatRange",
    "FloatSequenceSpace",
    "FloatTensor",
    "ForkSessionReply",
    "ForkSessionRequest",
    "GetSpacesReply",
    "GetSpacesRequest",
    "GetVersionReply",
    "GetVersionRequest",
    "Int64Box",
    "Int64List",
    "Int64Range",
    "Int64SequenceSpace",
    "Int64Tensor",
    "ListEvent",
    "ListSpace",
    "NamedDiscreteSpace",
    "NamedDiscreteSpace",
    "ObservationSpace",
    "Opaque",
    "SendSessionParameterReply",
    "SendSessionParameterRequest",
    "ServiceError",
    "ServiceInitError",
    "ServiceIsClosed",
    "ServiceTransportError",
    "SessionParameter",
    "Space",
    "StartSessionReply",
    "StartSessionRequest",
    "StepReply",
    "StepRequest",
    "StringSequenceSpace",
    "StringSpace",
    "StringTensor",
    "proto_to_action_space",
]
