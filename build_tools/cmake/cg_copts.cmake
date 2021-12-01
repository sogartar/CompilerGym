# Copyright 2019 The IREE Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#-------------------------------------------------------------------------------
# C/C++ options as used within IREE
#-------------------------------------------------------------------------------
#
#         ██     ██  █████  ██████  ███    ██ ██ ███    ██  ██████
#         ██     ██ ██   ██ ██   ██ ████   ██ ██ ████   ██ ██
#         ██  █  ██ ███████ ██████  ██ ██  ██ ██ ██ ██  ██ ██   ███
#         ██ ███ ██ ██   ██ ██   ██ ██  ██ ██ ██ ██  ██ ██ ██    ██
#          ███ ███  ██   ██ ██   ██ ██   ████ ██ ██   ████  ██████
#
# Everything here is added to *every* cg_cc_library/cg_cc_binary/etc.
# That includes both runtime and compiler components, and these may propagate
# out to user code interacting with either (such as custom modules).
#
# Be extremely judicious in the use of these flags.
#
# - Need to disable a warning?
#   Usually these are encountered in compiler-specific code and can be disabled
#   in a compiler-specific way. Only add global warning disables when it's clear
#   that we never want them or that they'll show up in a lot of places.
#
#   See: https://stackoverflow.com/questions/3378560/how-to-disable-gcc-warnings-for-a-few-lines-of-code
#
# - Need to add a linker dependency?
#   First figure out if you *really* need it. If it's only required on specific
#   platforms and in very specific files clang or msvc are used prefer
#   autolinking. GCC is stubborn and doesn't have autolinking so additional
#   flags may be required there.
#
#   See: https://en.wikipedia.org/wiki/Auto-linking
#
# - Need to tweak a compilation mode setting (debug/asserts/etc)?
#   Don't do that here, and in general *don't do that at all* unless it's behind
#   a very specific IREE-prefixed cmake flag (like IREE_SIZE_OPTIMIZED).
#   There's no one-size solution when we are dealing with cross-project and
#   cross-compiled binaries - there's no safe way to set global options that
#   won't cause someone to break, and you probably don't really need to do
#   change that setting anyway. Follow the rule of least surprise: if the user
#   has CMake's Debug configuration active then don't force things into release
#   mode, etc.
#
# - Need to add an include directory?
#   Don't do that here. Always prefer to fully-specify the path from the IREE
#   workspace root when it's known that the compilation will be occuring using
#   the files within the IREE checkout; for example, instead of adding a global
#   include path to third_party/foo/ and #include <foo.h>'ing, just
#   #include "third_party/foo/foo.h". This reduces build configuration, makes it
#   easier for readers to find the files, etc.
#
# - Still think you need to add an include directory? (system includes, etc)
#   Don't do that here, either. It's highly doubtful that every single target in
#   all of IREE (both compiler and runtime) on all platforms (both host and
#   cross-compilation targets) needs your special include directory. Add it on
#   the COPTS of the target you are using it in and, ideally, private to that
#   target (used in .c/cc files, not in a .h that leaks the include path
#   requirements to all consumers of the API).

set(IREE_CXX_STANDARD ${CMAKE_CXX_STANDARD})

# TODO(benvanik): fix these names (or remove entirely).
set(IREE_ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(IREE_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(IREE_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR})

# Compiler diagnostics.
# Please keep these in sync with build_tools/bazel/iree.bazelrc
cg_select_compiler_opts(IREE_DEFAULT_COPTS
  # Clang diagnostics. These largely match the set of warnings used within
  # Google. They have not been audited super carefully by the IREE team but are
  # generally thought to be a good set and consistency with those used
  # internally is very useful when importing. If you feel that some of these
  # should be different (especially more strict), please raise an issue!
  CLANG
    "-Werror"
    "-Wall"

    # Disable warnings we don't care about or that generally have a low
    # signal/noise ratio.
    "-Wno-ambiguous-member-template"
    "-Wno-char-subscripts"
    "-Wno-deprecated-declarations"
    "-Wno-extern-c-compat" # Matches upstream. Cannot impact due to extern C inclusion method.
    "-Wno-gnu-alignof-expression"
    "-Wno-gnu-variable-sized-type-not-at-end"
    "-Wno-ignored-optimization-argument"
    "-Wno-invalid-offsetof" # Technically UB but needed for intrusive ptrs
    "-Wno-invalid-source-encoding"
    "-Wno-mismatched-tags"
    "-Wno-pointer-sign"
    "-Wno-reserved-user-defined-literal"
    "-Wno-return-type-c-linkage"
    "-Wno-self-assign-overloaded"
    "-Wno-sign-compare"
    "-Wno-signed-unsigned-wchar"
    "-Wno-strict-overflow"
    "-Wno-trigraphs"
    "-Wno-unknown-pragmas"
    "-Wno-unknown-warning-option"
    "-Wno-unused-command-line-argument"
    "-Wno-unused-const-variable"
    "-Wno-unused-function"
    "-Wno-unused-local-typedef"
    "-Wno-unused-private-field"
    "-Wno-user-defined-warnings"

    # Explicitly enable some additional warnings.
    # Some of these aren't on by default, or under -Wall, or are subsets of
    # warnings turned off above.
    "-Wctad-maybe-unsupported"
    "-Wfloat-overflow-conversion"
    "-Wfloat-zero-conversion"
    "-Wfor-loop-analysis"
    "-Wformat-security"
    "-Wgnu-redeclared-enum"
    "-Wimplicit-fallthrough"
    "-Winfinite-recursion"
    "-Wliteral-conversion"
    #"-Wnon-virtual-dtor"
    "-Woverloaded-virtual"
    "-Wself-assign"
    "-Wstring-conversion"
    "-Wtautological-overlap-compare"
    "-Wthread-safety"
    "-Wthread-safety-beta"
    "-Wunused-comparison"
    "-Wvla"

  # TODO(#6959): Enable -Werror once we have a presubmit CI.
  GCC
    "-Wall"
    "-Wno-address-of-packed-member"
    "-Wno-comment"
    "-Wno-format-zero-length"
    # Technically UB but needed for intrusive ptrs
    $<$<COMPILE_LANGUAGE:CXX>:-Wno-invalid-offsetof>
    $<$<COMPILE_LANGUAGE:C>:-Wno-pointer-sign>
    "-Wno-sign-compare"
    "-Wno-unused-function"
)
