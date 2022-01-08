# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import json
from typing import Callable, Optional, Union, Any, ClassVar

#import networkx as nx
#import numpy as np
from gym.spaces import Space

from compiler_gym.service.proto import (
    Event as Observation,
    ObservationSpace,
    #DoubleRange as ScalarRange,
    py_converters)
from compiler_gym.util.gym_type_hints import ObservationType


# def _json2nx(observation):
#     json_data = json.loads(observation.string_value)
#     return nx.readwrite.json_graph.node_link_graph(
#         json_data, multigraph=True, directed=True
#     )


# def _scalar_range2tuple(sr: ScalarRange, defaults=(-np.inf, np.inf)):
#     """Convert a ScalarRange to a tuple of (min, max) bounds."""
#     return (
#         sr.min.value if sr.HasField("min") else defaults[0],
#         sr.max.value if sr.HasField("max") else defaults[1],
#     )


class ObservationSpaceSpec:
    """Specification of an observation space.

    :ivar id: The name of the observation space.
    :vartype id: str

    :ivar index: The index into the list of observation spaces that the service
        supports.
    :vartype index: int

    :ivar space: The space.
    :vartype space: Space

    :ivar deterministic: Whether the observation space is deterministic.
    :vartype deterministic: bool

    :ivar platform_dependent: Whether the observation values depend on the
        execution environment of the service.
    :vartype platform_dependent: bool

    :ivar default_value: A default observation. This value will be returned by
        :func:`CompilerEnv.step() <compiler_gym.envs.CompilerEnv.step>` if
        :func:`CompilerEnv.observation_space <compiler_gym.envs.CompilerEnv.observation_space>`
        is set and the service terminates.
    """

    message_converter: ClassVar[Callable[[Any], Any]] = py_converters.make_message_default_converter()

    def __init__(
        self,
        id: str,
        index: int,
        space: Space,
        translate: Callable[[Union[ObservationType, Observation]], ObservationType],
        to_string: Callable[[ObservationType], str],
        deterministic: bool,
        platform_dependent: bool,
        default_value: ObservationType,
    ):
        """Constructor. Don't call directly, use make_derived_space()."""
        self.id: str = id
        self.index: int = index
        self.space = space
        self.deterministic = deterministic
        self.platform_dependent = platform_dependent
        self.default_value = default_value
        self.translate = translate
        self.to_string = to_string

    def __hash__(self) -> int:
        # Quickly hash observation spaces by comparing the index into the list
        # of spaces returned by the environment. This means that you should not
        # hash between observation spaces from different environments as this
        # will cause collisions, e.g.
        #
        #     # not okay:
        #     >>> obs = set(env.observation.spaces).union(
        #         other_env.observation.spaces
        #     )
        #
        # If you want to hash between environments, consider using the string id
        # to identify the observation spaces.
        return self.index

    def __repr__(self) -> str:
        return f"ObservationSpaceSpec({self.id})"

    def __eq__(self, rhs) -> bool:
        """Equality check."""
        if not isinstance(rhs, ObservationSpaceSpec):
            return False
        return (
            self.id == rhs.id
            and self.index == rhs.index
            and self.space == rhs.space
            and self.platform_dependent == rhs.platform_dependent
            and self.deterministic == rhs.deterministic
        )

    @classmethod
    def from_proto(cls, index: int, proto: ObservationSpace):
        return cls(id=proto.space.name, index=index,
                            space=self.message_converter(proto.space),
                            translate=self.message_converter, to_string=str,
                            deterministic=proto.deterministic,
                            platform_dependent=proto.platform_dependent,
                            default_value=self.message_converter(proto.default_observation))


    def make_derived_space(
        self,
        id: str,
        translate: Callable[[ObservationType], ObservationType],
        space: Optional[Space] = None,
        deterministic: Optional[bool] = None,
        default_value: Optional[ObservationType] = None,
        platform_dependent: Optional[bool] = None,
        to_string: Callable[[ObservationType], str] = None,
    ) -> "ObservationSpaceSpec":
        """Create a derived observation space.

        :param id: The name of the derived observation space.
        :param translate: A callback function to compute a derived observation
            from the base observation.
        :param space: The :code:`gym.Space` describing the observation space.
        :param deterministic: Whether the observation space is deterministic.
            If not provided, the value is inherited from the base observation
            space.
        :param default_value: The default value for the observation space. If
            not provided, the value is derived from the default value of the
            base observation space.
        :param platform_dependent: Whether the derived observation space is
            platform-dependent. If not provided, the value is inherited from
            the base observation space.
        :param to_string: A callback to convert and observation to a string
            representation. If not provided, the callback is inherited from the
            base observation space.
        :return: A new ObservationSpaceSpec.
        """
        return ObservationSpaceSpec(
            id=id,
            index=self.index,
            space=space or self.space,
            translate=lambda observation: translate(self.translate(observation)),
            to_string=to_string or self.to_string,
            default_value=(
                translate(self.default_value)
                if default_value is None
                else default_value
            ),
            deterministic=(
                self.deterministic if deterministic is None else deterministic
            ),
            platform_dependent=(
                self.platform_dependent
                if platform_dependent is None
                else platform_dependent
            ),
        )
