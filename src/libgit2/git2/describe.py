# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .buffer import git_buf
from .types  import git_object
from .types  import git_repository

# @file git2/describe.h
# @brief Git describing routines
# @defgroup git_describe Git describing routines
# @ingroup Git

# GIT_BEGIN_DECL

# Reference lookup strategy
#
# These behave like the --tags and --all options to git-describe,
# namely they say to look for any reference in either refs/tags/ or
# refs/ respectively.
#
git_describe_strategy_t = ct.c_int
(   GIT_DESCRIBE_DEFAULT,
    GIT_DESCRIBE_TAGS,
    GIT_DESCRIBE_ALL,
) = range(0, 3)

# Describe options structure
#
# Initialize with `GIT_DESCRIBE_OPTIONS_INIT`. Alternatively, you can
# use `git_describe_options_init`.
#
class git_describe_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    ("max_candidates_tags", ct.c_uint),  # default: 10

    ("describe_strategy", ct.c_uint),    # default: GIT_DESCRIBE_DEFAULT

    ("pattern", ct.c_char_p),

    # When calculating the distance from the matching tag or
    # reference, only walk down the first-parent ancestry.
    #
    ("only_follow_first_parent", ct.c_int),

    # If no matching tag or reference is found, the describe
    # operation would normally fail. If this option is set, it
    # will instead fall back to showing the full id of the
    # commit.
    #
    ("show_commit_oid_as_fallback", ct.c_int),
]

GIT_DESCRIBE_DEFAULT_MAX_CANDIDATES_TAGS = 10
GIT_DESCRIBE_DEFAULT_ABBREVIATED_SIZE    = 7

GIT_DESCRIBE_OPTIONS_VERSION = 1
#define GIT_DESCRIBE_OPTIONS_INIT = { GIT_DESCRIBE_OPTIONS_VERSION,
#                                     GIT_DESCRIBE_DEFAULT_MAX_CANDIDATES_TAGS }

# Initialize git_describe_options structure
#
# Initializes a `git_describe_options` with default values. Equivalent to creating
# an instance with GIT_DESCRIBE_OPTIONS_INIT.
#
# @param opts The `git_describe_options` struct to initialize.
# @param version The struct version; pass `GIT_DESCRIBE_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_describe_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_describe_options),
    ct.c_uint)(
    ("git_describe_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Describe format options structure
#
# Initialize with `GIT_DESCRIBE_FORMAT_OPTIONS_INIT`. Alternatively, you can
# use `git_describe_format_options_init`.
#
#
class git_describe_format_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # Size of the abbreviated commit id to use. This value is the
    # lower bound for the length of the abbreviated string. The
    # default is 7.
    #
    ("abbreviated_size", ct.c_uint),

    # Set to use the long format even when a shorter name could be used.
    #
    ("always_use_long_format", ct.c_int),

    # If the workdir is dirty and this is set, this string will
    # be appended to the description string.
    #
    ("dirty_suffix", ct.c_char_p),
]

GIT_DESCRIBE_FORMAT_OPTIONS_VERSION = 1
#define GIT_DESCRIBE_FORMAT_OPTIONS_INIT = { GIT_DESCRIBE_FORMAT_OPTIONS_VERSION,
#                                            GIT_DESCRIBE_DEFAULT_ABBREVIATED_SIZE }

# Initialize git_describe_format_options structure
#
# Initializes a `git_describe_format_options` with default values. Equivalent to creating
# an instance with GIT_DESCRIBE_FORMAT_OPTIONS_INIT.
#
# @param opts The `git_describe_format_options` struct to initialize.
# @param version The struct version; pass `GIT_DESCRIBE_FORMAT_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_describe_format_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_describe_format_options),
    ct.c_uint)(
    ("git_describe_format_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# A struct that stores the result of a describe operation.
#
class git_describe_result(ct.Structure): pass

# Describe a commit
#
# Perform the describe operation on the given committish object.
#
# @param result pointer to store the result. You must free this once
# you're done with it.
# @param committish a committish to describe
# @param opts the lookup options (or NULL for defaults)
# @return 0 or an error code.
#
git_describe_commit = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_describe_result)),
    ct.POINTER(git_object),
    ct.POINTER(git_describe_options))(
    ("git_describe_commit", dll), (
    (1, "result"),
    (1, "committish"),
    (1, "opts"),))

# Describe a commit
#
# Perform the describe operation on the current commit and the
# worktree. After performing describe on HEAD, a status is run and the
# description is considered to be dirty if there are.
#
# @param out pointer to store the result. You must free this once
# you're done with it.
# @param repo the repository in which to perform the describe
# @param opts the lookup options (or NULL for defaults)
# @return 0 or an error code.
#
git_describe_workdir = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_describe_result)),
    ct.POINTER(git_repository),
    ct.POINTER(git_describe_options))(
    ("git_describe_workdir", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "opts"),))

# Print the describe result to a buffer
#
# @param out The buffer to store the result
# @param result the result from `git_describe_commit()` or
# `git_describe_workdir()`.
# @param opts the formatting options (or NULL for defaults)
# @return 0 or an error code.
#
git_describe_format = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_describe_result),
    ct.POINTER(git_describe_format_options))(
    ("git_describe_format", dll), (
    (1, "out"),
    (1, "result"),
    (1, "opts"),))

# Free the describe result.
#
# @param result The result to free.
#
git_describe_result_free = CFUNC(None,
    ct.POINTER(git_describe_result))(
    ("git_describe_result_free", dll), (
    (1, "result"),))

# GIT_END_DECL
