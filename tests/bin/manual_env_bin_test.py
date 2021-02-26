# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Tests for //compiler_gym/bin:manual_env."""
import re
import sys
from difflib import unified_diff
from io import StringIO
from random import seed

import pytest
from absl import app, flags

from compiler_gym.bin.manual_env import main
from compiler_gym.util.capture_output import capture_output
from tests.test_main import main as _test_main

FLAGS = flags.FLAGS

pytest_plugins = ["tests.pytest_plugins.llvm"]


def io_check(input, output, rnd_seed=100):
    """Run the shell with the given input and check the output matches the
    output regex"""
    seed(rnd_seed)
    old_stdin = sys.stdin
    try:
        with capture_output() as out:
            try:
                sys.stdin = StringIO(input)
                main(["argv0", "--env=llvm-v0"])
            except SystemExit:
                pass  # Expected behaviour is to call sys.exit().
        print(out.stdout)

        pattern = (
            r"""Initialized environment in [0-9.mu]*s
Welcome to the CompilerGym Shell!
---------------------------------
Type help or \? for more information.
The 'tutorial' command will give a step by step guide.

"""
            + output
            + r"""

compilergym:[a-zA-Z0-9/-]+> Exiting
"""
        )

        # Strip ANSI escape sequences from output that are used for formatting.
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        stdout = ansi_escape.sub("", out.stdout)
        # Strip trailing whitespace from output.
        stdout = "\n".join(n.rstrip() for n in stdout.split("\n"))

        if not re.match(pattern, stdout):
            # Create a diff between the expected regex and the actual output.
            # Diffing a regex will create a lot of false-positives, since any
            # character groups or other expressions will be different, but can
            # still be helful for tracking down the important differences.
            diff = unified_diff(
                pattern.split("\n"),
                stdout.split("\n"),
                fromfile="Expected output regex",
                tofile="Actual output",
            )
            pytest.fail("\n".join(diff))

    finally:
        sys.stdin = old_stdin


def test_download_cBench(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """require_dataset cBench-v0""",
        r"""compilergym:NO-BENCHMARK> Downloaded dataset cBench-v0 in [0-9.mu]*s
Application must be restarted to make changes visible.""",
    )


def test_list_datasets(cBench_dataset):
    del cBench_dataset  # unused
    io_check("""list_datasets""", r"""compilergym:NO-BENCHMARK> .*cBench-v0.*""")


def test_list_benchmarks(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """list_benchmarks""", r"""compilergym:NO-BENCHMARK> .*cBench-v0/adpcm.*"""
    )


def test_list_actions():
    io_check("""list_actions""", r"""compilergym:NO-BENCHMARK> .*-adce.* -strip.*""")


def test_list_rewards():
    io_check(
        """list_rewards""",
        r"""compilergym:NO-BENCHMARK> .*IrInstructionCount.* ObjectTextSizeOz.*""",
    )


def test_list_observations():
    io_check(
        """list_observations""",
        r"""compilergym:NO-BENCHMARK> Autophase, .*, Programl""",
    )


def test_set_benchmark(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """set_benchmark cBench-v0/adpcm""",
        r"""compilergym:NO-BENCHMARK> Reset benchmark://cBench-v0/adpcm environment in [0-9.mu]*s""",
    )


def test_actions_stack_back_stack(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """set_benchmark cBench-v0/adpcm
        action -mem2reg -adce -adce
        stack
        back
        stack""",
        r"""compilergym:NO-BENCHMARK> Reset benchmark://cBench-v0/adpcm environment in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Action -mem2reg
Action -adce
Action -adce
No effect
Actions -mem2reg -adce -adce in [0-9.mu]*s with reward 0.

compilergym:cBench-v0/adpcm>    Depth | Action   | Effect   | Done   | Reward   |   Cumulative Reward
---------+----------+----------+--------+----------+---------------------
       3 | -adce    | False    | False  | -        |                   0
       2 | -adce    | True     | False  | -        |                   0
       1 | -mem2reg | True     | False  | -        |                   0
       0 | <init>   | False    | False  | 0        |                   0

compilergym:cBench-v0/adpcm> Undid -adce in [0-9.mu]*s

compilergym:cBench-v0/adpcm>    Depth | Action   | Effect   | Done   | Reward   |   Cumulative Reward
---------+----------+----------+--------+----------+---------------------
       2 | -adce    | True     | False  | -        |                   0
       1 | -mem2reg | True     | False  | -        |                   0
       0 | <init>   | False    | False  | 0        |                   0""",
    )


def test_reward(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """set_benchmark cBench-v0/adpcm
        set_default_reward IrInstructionCount
        action -mem2reg
        reward
        reward IrInstructionCountNorm
        stack""",
        r"""compilergym:NO-BENCHMARK> Reset benchmark://cBench-v0/adpcm environment in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Reward IrInstructionCount in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Action -mem2reg
Reward: 181.000000
Actions -mem2reg in [0-9.mu]*s with reward 181.0.

compilergym:cBench-v0/adpcm> 0.000000
Reward IrInstructionCount in [0-9.mu]*s

compilergym:cBench-v0/adpcm> 0.404018
Reward IrInstructionCountNorm in [0-9.mu]*s

compilergym:cBench-v0/adpcm>    Depth | Action   | Effect   | Done   |   Reward |   Cumulative Reward
---------+----------+----------+--------+----------+---------------------
       1 | -mem2reg | True     | False  |      181 |                 181
       0 | <init>   | False    | False  |        0 |                   0

compilergym:cBench-v0/adpcm>    Depth | Action   | Effect   | Done   |   Reward |   Cumulative Reward
---------+----------+----------+--------+----------+---------------------
       1 | -mem2reg | True     | False  |      181 |                 181
       0 | <init>   | False    | False  |        0 |                   0""",
    )


def test_observation(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """set_benchmark cBench-v0/adpcm
        set_default_observation IrInstructionCount
        action -mem2reg
        observation
        observation IrInstructionCountOz
        """,
        r"""compilergym:NO-BENCHMARK> Reset benchmark://cBench-v0/adpcm environment in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Observation IrInstructionCount in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Action -mem2reg
Observation: 267
Actions -mem2reg in [0-9.mu]*s with reward 0.

compilergym:cBench-v0/adpcm> 267
Observation IrInstructionCount in [0-9.mu]*s

compilergym:cBench-v0/adpcm> 206
Observation IrInstructionCountOz in [0-9.mu]*s

compilergym:cBench-v0/adpcm> 206
Observation IrInstructionCountOz in [0-9.mu]*s""",
    )


def test_try_all_actions(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """set_benchmark cBench-v0/adpcm
        set_default_reward IrInstructionCount
        try_all_actions""",
        r"""compilergym:NO-BENCHMARK> Reset benchmark://cBench-v0/adpcm environment in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Reward IrInstructionCount in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Action: -add-discriminators Reward: 0.000000
Action: -adce Reward: 1.000000
(.|\n)*
Got actions in [0-9.mu]*s
 Action                          | Effect   | Done   |   Reward
---------------------------------+----------+--------+---------
 -mem2reg                        | True     | False  |      181
 -sroa                           | True     | False  |      181
 -newgvn                         | True     | False  |       74
 -gvn                            | True     | False  |       72
(.|\n)*
 -structurizecfg                 | True     | False  |      -25
 -bounds-checking                | True     | False  |      -60""",
    )


def test_simplify_stack(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """set_benchmark cBench-v0/adpcm
        set_default_reward IrInstructionCount
        action -mem2reg -adce -adce
        simplify_stack
        stack""",
        r"""compilergym:NO-BENCHMARK> Reset benchmark://cBench-v0/adpcm environment in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Reward IrInstructionCount in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Action -mem2reg
Reward: 181.000000
Action -adce
Reward: 2.000000
Action -adce
Reward: 0.000000
No effect
Actions -mem2reg -adce -adce in [0-9.mu]*s with reward 183.0.

compilergym:cBench-v0/adpcm>
compilergym:cBench-v0/adpcm>    Depth | Action   | Effect   | Done   |   Reward |   Cumulative Reward
---------+----------+----------+--------+----------+---------------------
       2 | -adce    | True     | False  |        2 |                 183
       1 | -mem2reg | True     | False  |      181 |                 181
       0 | <init>   | False    | False  |        0 |                   0""",
    )


def test_simplify_stack_no_reward(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """set_benchmark cBench-v0/adpcm
        action -mem2reg -adce -adce
        simplify_stack
        stack""",
        r"""compilergym:NO-BENCHMARK> Reset benchmark://cBench-v0/adpcm environment in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Action -mem2reg
Action -adce
Action -adce
No effect
Actions -mem2reg -adce -adce in [0-9.mu]*s with reward 0.

compilergym:cBench-v0/adpcm>
compilergym:cBench-v0/adpcm>    Depth | Action   | Effect   | Done   | Reward   |   Cumulative Reward
---------+----------+----------+--------+----------+---------------------
       2 | -adce    | True     | False  | -        |                   0
       1 | -mem2reg | True     | False  | -        |                   0
       0 | <init>   | False    | False  | 0        |                   0""",
    )


def test_hill_climb(monkeypatch, cBench_dataset):
    del cBench_dataset  # unused
    i = 0

    def incr():
        nonlocal i
        i += 1
        return i

    monkeypatch.setattr("random.randrange", lambda _: incr())

    io_check(
        """set_benchmark cBench-v0/adpcm
        set_default_reward IrInstructionCount
        hill_climb 2
        stack""",
        r"""compilergym:NO-BENCHMARK> Reset benchmark://cBench-v0/adpcm environment in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Reward IrInstructionCount in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Step: 1 Action: -adce Reward: 1.000000 Accept: True
Step: 2 Action: -aggressive-instcombine Reward: 0.000000 Accept: False
Hill climb complete in [0-9.mu]*s. Accepted 1 of 2 steps for total reward of 1.0.

compilergym:cBench-v0/adpcm>    Depth | Action   | Effect   | Done   |   Reward |   Cumulative Reward
---------+----------+----------+--------+----------+---------------------
       1 | -adce    | True     | False  |        1 |                   1
       0 | <init>   | False    | False  |        0 |                   0""",
    )


def test_greedy(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """set_benchmark cBench-v0/adpcm
        set_default_reward IrInstructionCount
        greedy
        stack""",
        r"""compilergym:NO-BENCHMARK> Reset benchmark://cBench-v0/adpcm environment in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Reward IrInstructionCount in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Action: -add-discriminators Reward: 0.000000
Action: -adce Reward: 1.000000
(.|\n)*
Action: -mem2reg Reward: 181.000000
(.|\n)*
Action: -mergereturn Reward: -1.000000
Step: 1 Selected action: -mem2reg Reward: 181.000000
Greedy 1 steps in [0-9.mu]*s

compilergym:cBench-v0/adpcm>    Depth | Action   | Effect   | Done   |   Reward |   Cumulative Reward
---------+----------+----------+--------+----------+---------------------
       1 | -mem2reg | True     | False  |      181 |                 181
       0 | <init>   | False    | False  |        0 |                   0""",
    )


def test_commandline(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """set_benchmark cBench-v0/adpcm
        action -mem2reg -adce
        commandline""",
        r"""compilergym:NO-BENCHMARK> Reset benchmark://cBench-v0/adpcm environment in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Action -mem2reg
Action -adce
Actions -mem2reg -adce in [0-9.mu]*s with reward 0.

compilergym:cBench-v0/adpcm> \$ opt -mem2reg -adce input.bc -o output.bc""",
    )


def test_reset(cBench_dataset):
    del cBench_dataset  # unused
    io_check(
        """set_benchmark cBench-v0/adpcm
        action -mem2reg -adce
        reset
        stack""",
        r"""compilergym:NO-BENCHMARK> Reset benchmark://cBench-v0/adpcm environment in [0-9.mu]*s

compilergym:cBench-v0/adpcm> Action -mem2reg
Action -adce
Actions -mem2reg -adce in [0-9.mu]*s with reward 0.

compilergym:cBench-v0/adpcm> Reset in [0-9.mu]*s

compilergym:cBench-v0/adpcm>    Depth | Action   | Effect   | Done   |   Reward |   Cumulative Reward
---------+----------+----------+--------+----------+---------------------
       0 | <init>   | False    | False  |        0 |                   0""",
    )


def test_unrecognized_flags():
    FLAGS.unparse_flags()
    with pytest.raises(app.UsageError) as ctx:
        main(["argv0", "unknown-option"])
    assert str(ctx.value) == "Unknown command line arguments: ['unknown-option']"


def test_missing_required_flag():
    FLAGS.unparse_flags()
    with pytest.raises(app.UsageError) as ctx:
        main(["argv0"])
    assert str(ctx.value) == "Neither --env or --local_service_binary is set"


def test_ls_env():
    with capture_output() as out:
        try:
            main(["argv0", "--ls_env"])
        except SystemExit:
            pass  # Expected behaviour is to call sys.exit().
    assert "llvm-" in out.stdout


if __name__ == "__main__":
    _test_main()