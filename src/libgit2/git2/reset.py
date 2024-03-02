# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .types    import git_object
from .strarray import git_strarray
from .types    import git_repository
from .checkout import git_checkout_options
from .types    import git_annotated_commit

# @file git2/reset.h
# @brief Git reset management routines
# @ingroup Git

# GIT_BEGIN_DECL

# Kinds of reset operation
#
git_reset_t = ct.c_int
(   GIT_RESET_SOFT,   # Move the head to the given commit
    GIT_RESET_MIXED,  # SOFT plus reset index to the commit
    GIT_RESET_HARD,   # MIXED plus changes in working tree discarded
) = (1, 2, 3)

# Sets the current head to the specified commit oid and optionally
# resets the index and working tree to match.
#
# SOFT reset means the Head will be moved to the commit.
#
# MIXED reset will trigger a SOFT reset, plus the index will be replaced
# with the content of the commit tree.
#
# HARD reset will trigger a MIXED reset and the working directory will be
# replaced with the content of the index.  (Untracked and ignored files
# will be left alone, however.)
#
# TODO: Implement remaining kinds of resets.
#
# @param repo Repository where to perform the reset operation.
#
# @param target Committish to which the Head should be moved to. This object
# must belong to the given `repo` and can either be a git_commit or a
# git_tag. When a git_tag is being passed, it should be dereferenceable
# to a git_commit which oid will be used as the target of the branch.
#
# @param reset_type Kind of reset operation to perform.
#
# @param checkout_opts Optional checkout options to be used for a HARD reset.
# The checkout_strategy field will be overridden (based on reset_type).
# This parameter can be used to propagate notify and progress callbacks.
#
# @return 0 on success or an error code
#
git_reset = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_object),
    git_reset_t,
    ct.POINTER(git_checkout_options))(
    ("git_reset", dll), (
    (1, "repo"),
    (1, "target"),
    (1, "reset_type"),
    (1, "checkout_opts"),))

# Sets the current head to the specified commit oid and optionally
# resets the index and working tree to match.
#
# This behaves like `git_reset()` but takes an annotated commit,
# which lets you specify which extended sha syntax string was
# specified by a user, allowing for more exact reflog messages.
#
# See the documentation for `git_reset()`.
#
# @see git_reset
#
git_reset_from_annotated = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_annotated_commit),
    git_reset_t,
    ct.POINTER(git_checkout_options))(
    ("git_reset_from_annotated", dll), (
    (1, "repo"),
    (1, "commit"),
    (1, "reset_type"),
    (1, "checkout_opts"),))

# Updates some entries in the index from the target commit tree.
#
# The scope of the updated entries is determined by the paths
# being passed in the `pathspec` parameters.
#
# Passing a NULL `target` will result in removing
# entries in the index matching the provided pathspecs.
#
# @param repo Repository where to perform the reset operation.
#
# @param target The committish which content will be used to reset the content
# of the index.
#
# @param pathspecs List of pathspecs to operate on.
#
# @return 0 on success or an error code < 0
#
git_reset_default = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_object),
    ct.POINTER(git_strarray))(
    ("git_reset_default", dll), (
    (1, "repo"),
    (1, "target"),
    (1, "pathspecs"),))

# GIT_END_DECL
