# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""Unit tests for //compiler_gym:validate."""
from collections.abc import Collection, Mapping

import google.protobuf.any_pb2 as any_pb2
import numpy as np
import pytest

from compiler_gym.service.proto import (
    BooleanBox,
    BooleanRange,
    BooleanSequenceSpace,
    BooleanTensor,
    ByteBox,
    ByteSequenceSpace,
    BytesSequenceSpace,
    ByteTensor,
    DictEvent,
    DictSpace,
    DiscreteSpace,
    DoubleBox,
    DoubleRange,
    DoubleSequenceSpace,
    DoubleTensor,
    Event,
    FloatBox,
    FloatRange,
    FloatSequenceSpace,
    FloatTensor,
    Int64Box,
    Int64Range,
    Int64SequenceSpace,
    Int64Tensor,
    ListEvent,
    ListSpace,
    NamedDiscreteSpace,
    Space,
    StringSpace,
    StringTensor,
    py_converters,
)
from compiler_gym.spaces import (
    Box,
    Dict,
    Discrete,
    NamedDiscrete,
    Scalar,
    Sequence,
    Tuple,
)
from tests.test_main import main


def test_convert_boolean_tensor_message_to_numpy():
    shape = [1, 2, 3]
    values = [True, False, True, True, False, False]
    tensor_message = BooleanTensor(shape=shape, values=values)
    np_array = py_converters.convert_tensor_message_to_numpy(tensor_message)
    assert np_array.dtype == bool
    assert np.array_equal(np_array.shape, shape)
    flat_np_array = np_array.flatten()
    assert np.array_equal(flat_np_array, values)


def test_convert_numpy_to_boolean_tensor_message():
    tensor = np.array([[True], [False]], dtype=bool)
    tensor_message = py_converters.convert_numpy_to_boolean_tensor_message(tensor)
    assert isinstance(tensor_message, BooleanTensor)
    assert np.array_equal(tensor.shape, tensor_message.shape)
    assert np.array_equal(tensor.flatten(), tensor_message.values)


def test_convert_byte_tensor_message_to_numpy():
    shape = [1, 2, 3]
    values = [1, 2, 3, 4, 5, 6]
    tensor_message = ByteTensor(shape=shape, values=bytes(values))
    np_array = py_converters.convert_tensor_message_to_numpy(tensor_message)
    assert np_array.dtype == np.byte
    assert np.array_equal(np_array.shape, shape)
    flat_np_array = np_array.flatten()
    assert np.array_equal(flat_np_array, values)


def test_convert_numpy_to_byte_tensor_message():
    tensor = np.array([[1], [2]], dtype=np.int8)
    tensor_message = py_converters.convert_numpy_to_byte_tensor_message(tensor)
    assert isinstance(tensor_message, ByteTensor)
    assert np.array_equal(tensor.shape, tensor_message.shape)
    assert tensor.tobytes() == tensor_message.values


def test_convert_int64_tensor_message_to_numpy():
    shape = [1, 2, 3]
    values = [1, 2, 3, 4, 5, 6]
    tensor_message = Int64Tensor(shape=shape, values=values)
    np_array = py_converters.convert_tensor_message_to_numpy(tensor_message)
    assert np_array.dtype == np.int64
    assert np.array_equal(np_array.shape, shape)
    flat_np_array = np_array.flatten()
    assert np.array_equal(flat_np_array, values)


def test_convert_numpy_to_int64_tensor_message():
    tensor = np.array([[1], [2]], dtype=np.int64)
    tensor_message = py_converters.convert_numpy_to_int64_tensor_message(tensor)
    assert isinstance(tensor_message, Int64Tensor)
    assert np.array_equal(tensor.shape, tensor_message.shape)
    assert np.array_equal(tensor.flatten(), tensor_message.values)


def test_convert_float_tensor_message_to_numpy():
    shape = [1, 2, 3]
    values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    tensor_message = FloatTensor(shape=shape, values=values)
    np_array = py_converters.convert_tensor_message_to_numpy(tensor_message)
    assert np_array.dtype == np.float32
    assert np.array_equal(np_array.shape, shape)
    flat_np_array = np_array.flatten()
    assert np.array_equal(flat_np_array, values)


def test_convert_numpy_to_float_tensor_message():
    tensor = np.array([[1], [2]], dtype=np.float32)
    tensor_message = py_converters.convert_numpy_to_float_tensor_message(tensor)
    assert isinstance(tensor_message, FloatTensor)
    assert np.array_equal(tensor.shape, tensor_message.shape)
    assert np.array_equal(tensor.flatten(), tensor_message.values)


def test_convert_double_tensor_message_to_numpy():
    shape = [1, 2, 3]
    values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    tensor_message = DoubleTensor(shape=shape, values=values)
    np_array = py_converters.convert_tensor_message_to_numpy(tensor_message)
    assert np_array.dtype == np.float64
    assert np.array_equal(np_array.shape, shape)
    flat_np_array = np_array.flatten()
    assert np.array_equal(flat_np_array, values)


def test_convert_numpy_to_double_tensor_message():
    tensor = np.array([[1], [2]], dtype=float)
    tensor_message = py_converters.convert_numpy_to_double_tensor_message(tensor)
    assert isinstance(tensor_message, DoubleTensor)
    assert np.array_equal(tensor.shape, tensor_message.shape)
    assert np.array_equal(tensor.flatten(), tensor_message.values)


def test_convert_string_tensor_message_to_numpy():
    shape = [1, 2]
    values = ["a", "b"]
    tensor_message = StringTensor(shape=shape, values=values)
    np_array = py_converters.convert_tensor_message_to_numpy(tensor_message)
    assert np_array.dtype == object
    assert np.array_equal(np_array.shape, shape)
    flat_np_array = np_array.flatten()
    assert np.array_equal(flat_np_array, values)


def test_convert_numpy_to_string_tensor_message():
    tensor = np.array([["a"], ["b"]], dtype=object)
    tensor_message = py_converters.convert_numpy_to_string_tensor_message(tensor)
    assert isinstance(tensor_message, StringTensor)
    assert np.array_equal(tensor.shape, tensor_message.shape)
    assert np.array_equal(tensor.flatten(), tensor_message.values)


def test_numpy_to_tensor_message_converter():
    converter = py_converters.NumpyToTensorMessageConverter()
    tensor = np.array([[1], [2]], dtype=float)
    tensor_message = converter(tensor)
    assert isinstance(tensor_message, DoubleTensor)
    assert np.array_equal(tensor.shape, tensor_message.shape)
    assert np.array_equal(tensor.flatten(), tensor_message.values)


def test_type_based_converter():
    converter = py_converters.TypeBasedConverter(
        conversion_map={FloatTensor: py_converters.convert_tensor_message_to_numpy}
    )
    tensor_message = FloatTensor(shape=[1], values=[1])
    numpy_array = converter(tensor_message)
    assert isinstance(numpy_array, np.ndarray)


def test_event_message_converter():
    message_converter = py_converters.TypeBasedConverter(
        conversion_map={FloatTensor: py_converters.convert_tensor_message_to_numpy}
    )
    event_converter = py_converters.EventMessageConverter(message_converter)
    tensor_message = FloatTensor(shape=[1], values=[1])
    event_message = Event(float_tensor=tensor_message)
    numpy_array = event_converter(event_message)
    assert isinstance(numpy_array, np.ndarray)


def test_list_event_message_converter():
    message_converter = py_converters.TypeBasedConverter(
        conversion_map={FloatTensor: py_converters.convert_tensor_message_to_numpy}
    )
    event_converter = py_converters.EventMessageConverter(message_converter)
    list_converter = py_converters.ListEventMessageConverter(event_converter)
    tensor_message = FloatTensor(shape=[1], values=[1])
    event_message = Event(float_tensor=tensor_message)
    list_message = ListEvent(events=[event_message])
    converted_list = list_converter(list_message)
    assert isinstance(converted_list, Collection)
    assert len(converted_list) == 1
    assert isinstance(converted_list[0], np.ndarray)


def test_to_list_event_message_converter():
    converter = py_converters.TypeBasedConverter(
        conversion_map={int: lambda x: Event(int64_value=x)}
    )
    list_converter = py_converters.ToListEventMessageConverter(converter)
    original_list = [1, 2]
    converted_list = list_converter(original_list)
    assert isinstance(converted_list, ListEvent)
    assert len(converted_list.events) == len(original_list)
    assert converted_list.events[0].int64_value == original_list[0]
    assert converted_list.events[1].int64_value == original_list[1]


def test_to_dict_event_message_converter():
    converter = py_converters.TypeBasedConverter(
        conversion_map={int: lambda x: Event(int64_value=x)}
    )
    dict_converter = py_converters.ToDictEventMessageConverter(converter)
    original_dict = {"a": 1}
    converted_dict = dict_converter(original_dict)
    assert isinstance(converted_dict, DictEvent)
    assert len(converted_dict.events) == len(original_dict)
    assert converted_dict.events["a"].int64_value == original_dict["a"]


def test_dict_event_message_converter():
    message_converter = py_converters.TypeBasedConverter(
        conversion_map={FloatTensor: py_converters.convert_tensor_message_to_numpy}
    )
    event_converter = py_converters.EventMessageConverter(message_converter)
    dict_converter = py_converters.DictEventMessageConverter(event_converter)
    tensor_message = FloatTensor(shape=[1], values=[1])
    event_message = Event(float_tensor=tensor_message)
    dict_message = DictEvent(events={"event_message_key": event_message})
    converted_list = dict_converter(dict_message)
    assert isinstance(converted_list, Mapping)
    assert len(converted_list) == 1
    assert "event_message_key" in converted_list
    assert isinstance(converted_list["event_message_key"], np.ndarray)


def test_protobuf_any_unpacker():
    unpacker = py_converters.ProtobufAnyUnpacker(
        {"compiler_gym.FloatTensor": FloatTensor}
    )
    any_msg = any_pb2.Any()
    tensor_message = FloatTensor(shape=[1], values=[1])
    any_msg.Pack(tensor_message)
    unpacked_tensor_message = unpacker(any_msg)
    assert tensor_message == unpacked_tensor_message


def test_protobuf_any_unpacker_value_error():
    unpacker = py_converters.ProtobufAnyUnpacker(
        {"IntentionallyWrongType": FloatTensor}
    )
    any_msg = any_pb2.Any()
    tensor_message = FloatTensor(shape=[1], values=[1])
    any_msg.Pack(tensor_message)
    any_msg.type_url = "IntentionallyWrongType"
    with pytest.raises(ValueError):
        unpacker(any_msg)


def test_protobuf_any_converter():
    unpacker = py_converters.ProtobufAnyUnpacker(
        {"compiler_gym.FloatTensor": FloatTensor}
    )
    type_based_converter = py_converters.TypeBasedConverter(
        conversion_map={FloatTensor: py_converters.convert_tensor_message_to_numpy}
    )
    converter = py_converters.ProtobufAnyConverter(
        unpacker=unpacker, message_converter=type_based_converter
    )
    any_msg = any_pb2.Any()
    tensor_message = FloatTensor(shape=[1], values=[1])
    any_msg.Pack(tensor_message)
    tensor = converter(any_msg)
    assert isinstance(tensor, np.ndarray)


def test_message_default_converter():
    value = 5
    converter = py_converters.message_default_converter()
    message = Event(int64_value=value)
    converted = converter(message)
    assert type(converted) == int
    assert value == converted


def test_to_event_message_default_converter():
    converter = py_converters.to_event_message_default_converter()
    val = [{"a": 1}]
    converted_val = converter(val)
    assert isinstance(converted_val, Event)
    assert isinstance(converted_val.event_list, ListEvent)
    assert len(converted_val.event_list.events) == 1
    assert isinstance(converted_val.event_list.events[0], Event)
    assert isinstance(converted_val.event_list.events[0].event_dict, DictEvent)
    assert (
        converted_val.event_list.events[0].event_dict.events["a"].int64_value
        == val[0]["a"]
    )


def test_convert_boolean_range_message():
    range = BooleanRange(min=False, max=True)
    converted_range = py_converters.convert_range_message(range)
    assert converted_range.dtype == bool
    assert converted_range.min == range.min
    assert converted_range.max == range.max


def test_convert_to_boolean_range_message():
    scalar = Scalar(min=False, max=True, dtype=bool, name=None)
    range = py_converters.convert_to_range_message(scalar)
    assert isinstance(range, BooleanRange)
    assert range.min == scalar.min
    assert range.max == scalar.max


def test_convert_int64_range_message():
    range = Int64Range(min=2, max=3)
    converted_range = py_converters.convert_range_message(range)
    assert converted_range.dtype == np.int64
    assert converted_range.min == range.min
    assert converted_range.max == range.max


def test_convert_float_range_message():
    range = FloatRange(min=2, max=3)
    converted_range = py_converters.convert_range_message(range)
    assert converted_range.dtype == np.float32
    assert converted_range.min == range.min
    assert converted_range.max == range.max


def test_convert_double_range_message():
    range = DoubleRange(min=2, max=3)
    converted_range = py_converters.convert_range_message(range)
    assert converted_range.dtype == float
    assert converted_range.min == range.min
    assert converted_range.max == range.max


def test_convert_boolean_box_message():
    box = BooleanBox(
        low=BooleanTensor(values=[1, 2], shape=[1, 2]),
        high=BooleanTensor(values=[2, 3], shape=[1, 2]),
    )
    converted_box = py_converters.convert_box_message(box)
    assert isinstance(converted_box, Box)
    assert converted_box.dtype == bool
    assert np.array_equal(box.low.shape, converted_box.shape)
    assert np.array_equal(box.high.shape, converted_box.shape)
    assert np.array_equal(box.low.values, converted_box.low.flatten())
    assert np.array_equal(box.high.values, converted_box.high.flatten())


def test_convert_to_boolean_box_message():
    box = Box(
        low=np.array([[False], [True]]),
        high=np.array([[False], [True]]),
        name=None,
        dtype=bool,
    )
    converted_box = py_converters.convert_to_box_message(box)
    assert isinstance(converted_box, BooleanBox)
    assert isinstance(converted_box.low, BooleanTensor)
    assert np.array_equal(converted_box.low.shape, box.shape)
    assert np.array_equal(converted_box.low.values, box.low.flatten())
    assert isinstance(converted_box.high, BooleanTensor)
    assert np.array_equal(converted_box.high.shape, box.shape)
    assert np.array_equal(converted_box.high.values, box.high.flatten())


def test_convert_byte_box_message():
    box = ByteBox(
        low=ByteTensor(values=bytes([1, 2]), shape=[1, 2]),
        high=ByteTensor(values=bytes([2, 3]), shape=[1, 2]),
    )
    converted_box = py_converters.convert_box_message(box)
    assert isinstance(converted_box, Box)
    assert converted_box.dtype == np.int8
    assert np.array_equal(box.low.shape, converted_box.shape)
    assert np.array_equal(box.high.shape, converted_box.shape)
    assert np.array_equal(box.low.values, bytes(converted_box.low.flatten()))
    assert np.array_equal(box.high.values, bytes(converted_box.high.flatten()))


def test_convert_to_byte_box_message():
    box = Box(
        low=np.array([[1], [2]]), high=np.array([[3], [4]]), name=None, dtype=np.int8
    )
    converted_box = py_converters.convert_to_box_message(box)
    assert isinstance(converted_box, ByteBox)
    assert isinstance(converted_box.low, ByteTensor)
    assert np.array_equal(converted_box.low.shape, box.shape)
    assert np.array_equal(
        np.frombuffer(converted_box.low.values, dtype=np.int8), box.low.flatten()
    )
    assert isinstance(converted_box.high, ByteTensor)
    assert np.array_equal(converted_box.high.shape, box.shape)
    assert np.array_equal(
        np.frombuffer(converted_box.high.values, dtype=np.int8), box.high.flatten()
    )


def test_convert_int64_box_message():
    box = Int64Box(
        low=Int64Tensor(values=[1, 2], shape=[1, 2]),
        high=Int64Tensor(values=[2, 3], shape=[1, 2]),
    )
    converted_box = py_converters.convert_box_message(box)
    assert isinstance(converted_box, Box)
    assert converted_box.dtype == np.int64
    assert np.array_equal(box.low.shape, converted_box.shape)
    assert np.array_equal(box.high.shape, converted_box.shape)
    assert np.array_equal(box.low.values, converted_box.low.flatten())
    assert np.array_equal(box.high.values, converted_box.high.flatten())


def test_convert_to_int64_box_message():
    box = Box(
        low=np.array([[1], [2]]), high=np.array([[3], [4]]), name=None, dtype=np.int64
    )
    converted_box = py_converters.convert_to_box_message(box)
    assert isinstance(converted_box, Int64Box)
    assert isinstance(converted_box.low, Int64Tensor)
    assert np.array_equal(converted_box.low.shape, box.shape)
    assert np.array_equal(converted_box.low.values, box.low.flatten())
    assert isinstance(converted_box.high, Int64Tensor)
    assert np.array_equal(converted_box.high.shape, box.shape)
    assert np.array_equal(converted_box.high.values, box.high.flatten())


def test_convert_float_box_message():
    box = FloatBox(
        low=FloatTensor(values=[1, 2], shape=[1, 2]),
        high=FloatTensor(values=[2, 3], shape=[1, 2]),
    )
    converted_box = py_converters.convert_box_message(box)
    assert isinstance(converted_box, Box)
    assert converted_box.dtype == np.float32
    assert np.array_equal(box.low.shape, converted_box.shape)
    assert np.array_equal(box.high.shape, converted_box.shape)
    assert np.array_equal(box.low.values, converted_box.low.flatten())
    assert np.array_equal(box.high.values, converted_box.high.flatten())


def test_convert_to_float_box_message():
    box = Box(
        low=np.array([[1], [2]], dtype=np.float32),
        high=np.array([[3], [4]], dtype=np.float32),
        name=None,
        dtype=np.float32,
    )
    converted_box = py_converters.convert_to_box_message(box)
    assert isinstance(converted_box, FloatBox)
    assert isinstance(converted_box.low, FloatTensor)
    assert np.array_equal(converted_box.low.shape, box.shape)
    assert np.array_equal(converted_box.low.values, box.low.flatten())
    assert isinstance(converted_box.high, FloatTensor)
    assert np.array_equal(converted_box.high.shape, box.shape)
    assert np.array_equal(converted_box.high.values, box.high.flatten())


def test_convert_double_box_message():
    box = DoubleBox(
        low=DoubleTensor(values=[1, 2], shape=[1, 2]),
        high=DoubleTensor(values=[2, 3], shape=[1, 2]),
    )
    converted_box = py_converters.convert_box_message(box)
    assert isinstance(converted_box, Box)
    assert converted_box.dtype == float
    assert np.array_equal(box.low.shape, converted_box.shape)
    assert np.array_equal(box.high.shape, converted_box.shape)
    assert np.array_equal(box.low.values, converted_box.low.flatten())
    assert np.array_equal(box.high.values, converted_box.high.flatten())


def test_convert_to_double_box_message():
    box = Box(
        low=np.array([[1.0], [2.0]]),
        high=np.array([[3.0], [4.0]]),
        name=None,
        dtype=np.float64,
    )
    converted_box = py_converters.convert_to_box_message(box)
    assert isinstance(converted_box, DoubleBox)
    assert isinstance(converted_box.low, DoubleTensor)
    assert np.array_equal(converted_box.low.shape, box.shape)
    assert np.array_equal(converted_box.low.values, box.low.flatten())
    assert isinstance(converted_box.high, DoubleTensor)
    assert np.array_equal(converted_box.high.shape, box.shape)
    assert np.array_equal(converted_box.high.values, box.high.flatten())


def test_convert_discrete_space_message():
    message = DiscreteSpace(n=5)
    converted_message = py_converters.convert_discrete_space_message(message)
    assert message.n == converted_message.n


def test_convert_to_discrete_space_message():
    space = Discrete(name=None, n=5)
    converted_space = py_converters.convert_to_discrete_space_message(space)
    assert isinstance(converted_space, DiscreteSpace)
    assert converted_space.n == 5


def test_convert_to_named_discrete_space_message():
    space = NamedDiscrete(name=None, items=["a", "b"])
    converted_space = py_converters.convert_to_named_discrete_space_message(space)
    assert isinstance(converted_space, NamedDiscreteSpace)
    assert np.array_equal(space.names, converted_space.names)


def test_convert_named_discrete_space_message():
    message = NamedDiscreteSpace(names=["a", "b", "c"])
    converted_message = py_converters.convert_named_discrete_space_message(message)
    assert np.array_equal(message.names, converted_message.names)


def test_convert_boolean_sequence_space():
    seq = BooleanSequenceSpace(
        length_range=Int64Range(min=1, max=2),
        scalar_range=BooleanRange(min=True, max=False),
    )
    converted_seq = py_converters.convert_sequence_space(seq)
    assert isinstance(converted_seq, Sequence)
    assert converted_seq.dtype == bool
    assert converted_seq.size_range[0] == 1
    assert converted_seq.size_range[1] == 2
    assert converted_seq.scalar_range.min == True  # noqa: E712
    assert converted_seq.scalar_range.max == False  # noqa: E712


def test_convert_to_boolean_sequence_space():
    seq = Sequence(
        name=None,
        dtype=bool,
        size_range=(1, 2),
        scalar_range=Scalar(name=None, min=True, max=False, dtype=bool),
    )
    converted_seq = py_converters.convert_to_ranged_sequence_space(seq)
    assert isinstance(converted_seq, BooleanSequenceSpace)
    assert converted_seq.length_range.min == 1
    assert converted_seq.length_range.max == 2
    assert converted_seq.scalar_range.min == True  # noqa: E712
    assert converted_seq.scalar_range.max == False  # noqa: E712


def test_convert_bytes_sequence_space():
    seq = BytesSequenceSpace(length_range=Int64Range(min=1, max=2))
    converted_seq = py_converters.convert_sequence_space(seq)
    assert isinstance(converted_seq, Sequence)
    assert converted_seq.dtype == bytes
    assert converted_seq.size_range[0] == 1
    assert converted_seq.size_range[1] == 2


def test_convert_to_bytes_sequence_space():
    seq = Sequence(name=None, dtype=bytes, size_range=(1, 2))
    converted_seq = py_converters.convert_to_bytes_sequence_space(seq)
    assert isinstance(converted_seq, BytesSequenceSpace)
    assert converted_seq.length_range.min == 1
    assert converted_seq.length_range.max == 2


def test_convert_byte_sequence_space():
    seq = ByteSequenceSpace(
        length_range=Int64Range(min=1, max=2), scalar_range=Int64Range(min=3, max=4)
    )
    converted_seq = py_converters.convert_sequence_space(seq)
    assert isinstance(converted_seq, Sequence)
    assert converted_seq.dtype == np.int8
    assert converted_seq.size_range[0] == 1
    assert converted_seq.size_range[1] == 2
    assert converted_seq.scalar_range.min == 3
    assert converted_seq.scalar_range.max == 4


def test_convert_to_byte_sequence_space():
    seq = Sequence(
        name=None,
        dtype=np.int8,
        size_range=(1, 2),
        scalar_range=Scalar(name=None, min=4, max=5, dtype=np.int8),
    )
    converted_seq = py_converters.convert_to_ranged_sequence_space(seq)
    assert isinstance(converted_seq, ByteSequenceSpace)
    assert converted_seq.length_range.min == 1
    assert converted_seq.length_range.max == 2
    assert converted_seq.scalar_range.min == 4
    assert converted_seq.scalar_range.max == 5


def test_convert_int64_sequence_space():
    seq = Int64SequenceSpace(
        length_range=Int64Range(min=1, max=2), scalar_range=Int64Range(min=3, max=4)
    )
    converted_seq = py_converters.convert_sequence_space(seq)
    assert isinstance(converted_seq, Sequence)
    assert converted_seq.dtype == np.int64
    assert converted_seq.size_range[0] == 1
    assert converted_seq.size_range[1] == 2
    assert converted_seq.scalar_range.min == 3
    assert converted_seq.scalar_range.max == 4


def test_convert_to_int64_sequence_space():
    seq = Sequence(
        name=None,
        dtype=np.int64,
        size_range=(1, 2),
        scalar_range=Scalar(name=None, min=4, max=5, dtype=np.int64),
    )
    converted_seq = py_converters.convert_to_ranged_sequence_space(seq)
    assert isinstance(converted_seq, Int64SequenceSpace)
    assert converted_seq.length_range.min == 1
    assert converted_seq.length_range.max == 2
    assert converted_seq.scalar_range.min == 4
    assert converted_seq.scalar_range.max == 5


def test_convert_float_sequence_space():
    seq = FloatSequenceSpace(
        length_range=Int64Range(min=1, max=2), scalar_range=FloatRange(min=3.1, max=4)
    )
    converted_seq = py_converters.convert_sequence_space(seq)
    assert isinstance(converted_seq, Sequence)
    assert converted_seq.dtype == np.float32
    assert converted_seq.size_range[0] == 1
    assert converted_seq.size_range[1] == 2
    assert np.isclose(converted_seq.scalar_range.min, 3.1)
    assert converted_seq.scalar_range.max == 4


def test_convert_to_float_sequence_space():
    seq = Sequence(
        name=None,
        dtype=np.float32,
        size_range=(1, 2),
        scalar_range=Scalar(name=None, min=4, max=5, dtype=np.float32),
    )
    converted_seq = py_converters.convert_to_ranged_sequence_space(seq)
    assert isinstance(converted_seq, FloatSequenceSpace)
    assert converted_seq.length_range.min == 1
    assert converted_seq.length_range.max == 2
    assert np.isclose(converted_seq.scalar_range.min, 4)
    assert np.isclose(converted_seq.scalar_range.max, 5)


def test_convert_double_sequence_space():
    seq = DoubleSequenceSpace(
        length_range=Int64Range(min=1, max=2), scalar_range=DoubleRange(min=3.1, max=4)
    )
    converted_seq = py_converters.convert_sequence_space(seq)
    assert isinstance(converted_seq, Sequence)
    assert converted_seq.dtype == float
    assert converted_seq.size_range[0] == 1
    assert converted_seq.size_range[1] == 2
    assert converted_seq.scalar_range.min == 3.1
    assert converted_seq.scalar_range.max == 4


def test_convert_to_double_sequence_space():
    seq = Sequence(
        name=None,
        dtype=np.float64,
        size_range=(1, 2),
        scalar_range=Scalar(name=None, min=4.0, max=5.0, dtype=np.float64),
    )
    converted_seq = py_converters.convert_to_ranged_sequence_space(seq)
    assert isinstance(converted_seq, DoubleSequenceSpace)
    assert converted_seq.length_range.min == 1
    assert converted_seq.length_range.max == 2
    assert converted_seq.scalar_range.min == 4.0
    assert converted_seq.scalar_range.max == 5.0


def test_convert_string_sequence_space():
    seq = BytesSequenceSpace(length_range=Int64Range(min=1, max=2))
    converted_seq = py_converters.convert_sequence_space(seq)
    assert isinstance(converted_seq, Sequence)
    assert converted_seq.dtype == bytes
    assert converted_seq.size_range[0] == 1
    assert converted_seq.size_range[1] == 2


# def test_convert_to_string_sequence_space():
#     seq = Sequence(name=None, dtype=str, size_range=(1, 2))
#     converted_seq = py_converters.convert_to_string_sequence_space(seq)
#     assert isinstance(converted_seq, StringSequenceSpace)
#     assert converted_seq.length_range.min == 1
#     assert converted_seq.length_range.max == 2


def test_convert_string_space():
    space = StringSpace(length_range=Int64Range(min=1, max=2))
    converted_space = py_converters.convert_sequence_space(space)
    assert isinstance(converted_space, Sequence)
    assert converted_space.dtype == str
    assert converted_space.size_range[0] == 1
    assert converted_space.size_range[1] == 2


def test_convert_to_string_space():
    space = Sequence(name=None, size_range=(1, 2), dtype=str)
    converted_space = py_converters.convert_to_string_space(space)
    assert isinstance(converted_space, StringSpace)
    assert converted_space.length_range.min == 1
    assert converted_space.length_range.max == 2


def test_space_message_converter():
    message_converter = py_converters.TypeBasedConverter(
        conversion_map={StringSpace: py_converters.convert_sequence_space}
    )
    space_converter = py_converters.SpaceMessageConverter(message_converter)
    val = StringSpace(length_range=Int64Range(min=1, max=2))
    space_message = Space(string_value=val, name="myspace")
    converted_space = space_converter(space_message)
    assert isinstance(converted_space, Sequence)
    assert converted_space.dtype == str
    assert converted_space.size_range[0] == 1
    assert converted_space.size_range[1] == 2
    assert converted_space.name == "myspace"


def test_list_space_message_converter():
    message_converter = py_converters.TypeBasedConverter(
        conversion_map={StringSpace: py_converters.convert_sequence_space}
    )
    space_converter = py_converters.SpaceMessageConverter(message_converter)
    list_converter = py_converters.ListSpaceMessageConverter(space_converter)
    space_message = ListSpace(
        spaces=[
            Space(
                string_value=StringSpace(length_range=Int64Range(min=1, max=2)),
                name="myspace",
            )
        ]
    )
    converted_space = list_converter(space_message)
    assert isinstance(converted_space, Tuple)
    assert len(converted_space.spaces) == 1
    assert converted_space.spaces[0].dtype == str
    assert converted_space.spaces[0].size_range[0] == 1
    assert converted_space.spaces[0].size_range[1] == 2
    assert converted_space.spaces[0].name == "myspace"


def test_tuple_to_list_space_message_converter():
    to_message_converter = py_converters.TypeBasedConverter(
        conversion_map={Discrete: py_converters.convert_to_discrete_space_message}
    )
    to_space_converter = py_converters.ToSpaceMessageConverter(to_message_converter)
    to_list_converter = py_converters.ToListSpaceMessageConverter(to_space_converter)
    space = Tuple(name=None, spaces=[Discrete(name="discrete", n=5)])
    converted_space = to_list_converter(space)
    assert isinstance(converted_space, ListSpace)
    assert len(converted_space.spaces) == 1
    assert isinstance(converted_space.spaces[0], Space)
    assert converted_space.spaces[0].name == "discrete"
    assert hasattr(converted_space.spaces[0], "discrete")
    assert converted_space.spaces[0].discrete.n == 5


def test_to_list_space_message_converter():
    to_message_converter = py_converters.TypeBasedConverter(
        conversion_map={Discrete: py_converters.convert_to_discrete_space_message}
    )
    to_space_converter = py_converters.ToSpaceMessageConverter(to_message_converter)
    to_list_converter = py_converters.ToListSpaceMessageConverter(to_space_converter)
    space = Tuple(name=None, spaces=[Discrete(name="discrete", n=5)])
    converted_space = to_list_converter(space)
    assert isinstance(converted_space, ListSpace)
    assert len(converted_space.spaces) == 1
    assert isinstance(converted_space.spaces[0], Space)
    assert converted_space.spaces[0].name == "discrete"
    assert hasattr(converted_space.spaces[0], "discrete")
    assert converted_space.spaces[0].discrete.n == 5


def test_dict_space_message_converter():
    message_converter = py_converters.TypeBasedConverter(
        conversion_map={StringSpace: py_converters.convert_sequence_space}
    )
    space_converter = py_converters.SpaceMessageConverter(message_converter)
    dict_converter = py_converters.DictSpaceMessageConverter(space_converter)
    space_message = DictSpace(
        spaces={
            "key": Space(
                string_value=StringSpace(length_range=Int64Range(min=1, max=2)),
                name="myspace",
            )
        }
    )
    converted_space = dict_converter(space_message)
    assert isinstance(converted_space, Dict)
    assert len(converted_space.spaces) == 1
    assert "key" in converted_space.spaces
    assert converted_space.spaces["key"].dtype == str
    assert converted_space.spaces["key"].size_range[0] == 1
    assert converted_space.spaces["key"].size_range[1] == 2
    assert converted_space.spaces["key"].name == "myspace"


def test_to_dict_space_message_converter():
    to_message_converter = py_converters.TypeBasedConverter(
        conversion_map={Discrete: py_converters.convert_to_discrete_space_message}
    )
    to_space_converter = py_converters.ToSpaceMessageConverter(to_message_converter)
    to_dict_converter = py_converters.ToDictSpaceMessageConverter(to_space_converter)
    space = Dict(name=None, spaces={"key": Discrete(name="discrete", n=5)})
    converted_space = to_dict_converter(space)
    assert isinstance(converted_space, DictSpace)
    assert len(converted_space.spaces) == 1
    assert "key" in converted_space.spaces
    assert isinstance(converted_space.spaces["key"], Space)
    assert converted_space.spaces["key"].name == "discrete"
    assert hasattr(converted_space.spaces["key"], "discrete")
    assert converted_space.spaces["key"].discrete.n == 5


def test_to_space_message_default_converter():
    space = Tuple(
        name="list",
        spaces=[
            Dict(
                name="dict",
                spaces={"key": Box(name="box", low=0, high=1, shape=[1, 2])},
            )
        ],
    )
    converted_space = py_converters.to_space_message_default_converter()(space)
    assert isinstance(converted_space, Space)
    assert converted_space.name == "list"
    assert converted_space.space_list.spaces[0].name == "dict"
    assert converted_space.space_list.spaces[0].space_dict.spaces["key"].name == "box"


if __name__ == "__main__":
    main()
