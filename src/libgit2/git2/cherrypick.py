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

# @file git2/cherrypick.h
# @brief Git cherry-pick routines
# @defgroup git_cherrypick Git cherry-pick routines
# @ingroup Git

# GIT_BEGIN_DECL

# Cherry-pick options
#
class git_cherrypick_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # For merge commits, the "mainline" is treated as the parent.
    ("mainline", ct.c_uint),

    # Options for the merging
    ("merge_opts", git_merge_options),

    # Options for the checkout
    ("checkout_opts", git_checkout_options),
]

GIT_CHERRYPICK_OPTIONS_VERSION = 1
#define GIT_CHERRYPICK_OPTIONS_INIT = { GIT_CHERRYPICK_OPTIONS_VERSION,
#                                       0,
#                                       GIT_MERGE_OPTIONS_INIT,
#                                       GIT_CHECKOUT_OPTIONS_INIT }

# Initialize git_cherrypick_options structure
#
# Initializes a `git_cherrypick_options` with default values. Equivalent to creating
# an instance with GIT_CHERRYPICK_OPTIONS_INIT.
#
# @param opts The `git_cherrypick_options` struct to initialize.
# @param version The struct version; pass `GIT_CHERRYPICK_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_cherrypick_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_cherrypick_options),
    ct.c_uint)(
    ("git_cherrypick_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Cherry-picks the given commit against the given "our" commit, producing an
# index that reflects the result of the cherry-pick.
#
# The returned index must be freed explicitly with `git_index_free`.
#
# @param out pointer to store the index result in
# @param repo the repository that contains the given commits
# @param cherrypick_commit the commit to cherry-pick
# @param our_commit the commit to cherry-pick against (eg, HEAD)
# @param mainline the parent of the `cherrypick_commit`, if it is a merge
# @param merge_options the merge options (or null for defaults)
# @return zero on success, -1 on failure.
#
git_cherrypick_commit = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index)),
    ct.POINTER(git_repository),
    ct.POINTER(git_commit),
    ct.POINTER(git_commit),
    ct.c_uint,
    ct.POINTER(git_merge_options))(
    ("git_cherrypick_commit", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "cherrypick_commit"),
    (1, "our_commit"),
    (1, "mainline"),
    (1, "merge_options"),))

# Cherry-pick the given commit, producing changes in the index and working directory.
#
# @param repo the repository to cherry-pick
# @param commit the commit to cherry-pick
# @param cherrypick_options the cherry-pick options (or null for defaults)
# @return zero on success, -1 on failure.
#
git_cherrypick = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_commit),
    ct.POINTER(git_cherrypick_options))(
    ("git_cherrypick", dll), (
    (1, "repo"),
    (1, "commit"),
    (1, "cherrypick_options"),))

# GIT_END_DECL
