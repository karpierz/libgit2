# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .types    import git_repository
from .types    import git_commit
from .types    import git_index
from .merge    import git_merge_options
from .checkout import git_checkout_options

# @file git2/revert.h
# @brief Git revert routines
# @defgroup git_revert Git revert routines
# @ingroup Git

# GIT_BEGIN_DECL

# Options for revert
#
class git_revert_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # For merge commits, the "mainline" is treated as the parent.
    ("mainline", ct.c_uint),

    # Options for the merging
    ("merge_opts", git_merge_options),

    # Options for the checkout
    ("checkout_opts", git_checkout_options),
]

GIT_REVERT_OPTIONS_VERSION = 1
#define GIT_REVERT_OPTIONS_INIT = { GIT_REVERT_OPTIONS_VERSION,
#                                   0,
#                                   GIT_MERGE_OPTIONS_INIT,
#                                   GIT_CHECKOUT_OPTIONS_INIT }

# Initialize git_revert_options structure
#
# Initializes a `git_revert_options` with default values. Equivalent to
# creating an instance with `GIT_REVERT_OPTIONS_INIT`.
#
# @param opts The `git_revert_options` struct to initialize.
# @param version The struct version; pass `GIT_REVERT_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_revert_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_revert_options),
    ct.c_uint)(
    ("git_revert_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Reverts the given commit against the given "our" commit, producing an
# index that reflects the result of the revert.
#
# The returned index must be freed explicitly with `git_index_free`.
#
# @param out pointer to store the index result in
# @param repo the repository that contains the given commits
# @param revert_commit the commit to revert
# @param our_commit the commit to revert against (eg, HEAD)
# @param mainline the parent of the revert commit, if it is a merge
# @param merge_options the merge options (or null for defaults)
# @return zero on success, -1 on failure.
#
git_revert_commit = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index)),
    ct.POINTER(git_repository),
    ct.POINTER(git_commit),
    ct.POINTER(git_commit),
    ct.c_uint,
    ct.POINTER(git_merge_options))(
    ("git_revert_commit", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "revert_commit"),
    (1, "our_commit"),
    (1, "mainline"),
    (1, "merge_options"),))

# Reverts the given commit, producing changes in the index and working directory.
#
# @param repo the repository to revert
# @param commit the commit to revert
# @param given_opts the revert options (or null for defaults)
# @return zero on success, -1 on failure.
#
git_revert = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_commit),
    ct.POINTER(git_revert_options))(
    ("git_revert", dll), (
    (1, "repo"),
    (1, "commit"),
    (1, "given_opts"),))

# GIT_END_DECL
