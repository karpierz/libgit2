# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .buffer   import git_buf
from .strarray import git_strarray
from .types    import git_repository
from .types    import git_reference
from .types    import git_worktree
from .checkout import git_checkout_options

# @file git2/worktrees.h
# @brief Git worktree related functions
# @defgroup git_commit Git worktree related functions
# @ingroup Git

# GIT_BEGIN_DECL

# List names of linked working trees
#
# The returned list should be released with `git_strarray_free`
# when no longer needed.
#
# @param out pointer to the array of working tree names
# @param repo the repo to use when listing working trees
# @return 0 or an error code
#
git_worktree_list = CFUNC(ct.c_int,
    ct.POINTER(git_strarray),
    ct.POINTER(git_repository))(
    ("git_worktree_list", dll), (
    (1, "out"),
    (1, "repo"),))

# Lookup a working tree by its name for a given repository
#
# @param out Output pointer to looked up worktree or `NULL`
# @param repo The repository containing worktrees
# @param name Name of the working tree to look up
# @return 0 or an error code
#
git_worktree_lookup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_worktree)),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_worktree_lookup", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "name"),))

# Open a worktree of a given repository
#
# If a repository is not the main tree but a worktree, this
# function will look up the worktree inside the parent
# repository and create a new `git_worktree` structure.
#
# @param out Out-pointer for the newly allocated worktree
# @param repo Repository to look up worktree for
# @return 0 or an error code
#
git_worktree_open_from_repository = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_worktree)),
    ct.POINTER(git_repository))(
    ("git_worktree_open_from_repository", dll), (
    (1, "out"),
    (1, "repo"),))

# Free a previously allocated worktree
#
# @param wt worktree handle to close. If NULL nothing occurs.
#
git_worktree_free = CFUNC(None,
    ct.POINTER(git_worktree))(
    ("git_worktree_free", dll), (
    (1, "wt"),))

# Check if worktree is valid
#
# A valid worktree requires both the git data structures inside
# the linked parent repository and the linked working copy to be
# present.
#
# @param wt Worktree to check
# @return 0 when worktree is valid, error-code otherwise
#
git_worktree_validate = CFUNC(ct.c_int,
    ct.POINTER(git_worktree))(
    ("git_worktree_validate", dll), (
    (1, "wt"),))

# Worktree add options structure
#
# Initialize with `GIT_WORKTREE_ADD_OPTIONS_INIT`. Alternatively, you can
# use `git_worktree_add_options_init`.
#
class git_worktree_add_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    ("lock", ct.c_int),  # lock newly created worktree

    ("ref", ct.POINTER(git_reference)),  # reference to use for the new worktree HEAD

    # Options for the checkout.
    ("checkout_options", git_checkout_options),
]

GIT_WORKTREE_ADD_OPTIONS_VERSION = 1
#define GIT_WORKTREE_ADD_OPTIONS_INIT {GIT_WORKTREE_ADD_OPTIONS_VERSION,0,NULL,GIT_CHECKOUT_OPTIONS_INIT}

# Initialize git_worktree_add_options structure
#
# Initializes a `git_worktree_add_options` with default values. Equivalent to
# creating an instance with `GIT_WORKTREE_ADD_OPTIONS_INIT`.
#
# @param opts The `git_worktree_add_options` struct to initialize.
# @param version The struct version; pass `GIT_WORKTREE_ADD_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_worktree_add_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_worktree_add_options),
    ct.c_uint)(
    ("git_worktree_add_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Add a new working tree
#
# Add a new working tree for the repository, that is create the
# required data structures inside the repository and check out
# the current HEAD at `path`
#
# @param out Output pointer containing new working tree
# @param repo Repository to create working tree for
# @param name Name of the working tree
# @param path Path to create working tree at
# @param opts Options to modify default behavior. May be NULL
# @return 0 or an error code
#
git_worktree_add = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_worktree)),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.c_char_p,
    ct.POINTER(git_worktree_add_options))(
    ("git_worktree_add", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "name"),
    (1, "path"),
    (1, "opts"),))

# Lock worktree if not already locked
#
# Lock a worktree, optionally specifying a reason why the linked
# working tree is being locked.
#
# @param wt Worktree to lock
# @param reason Reason why the working tree is being locked
# @return 0 on success, non-zero otherwise
#
git_worktree_lock = CFUNC(ct.c_int,
    ct.POINTER(git_worktree),
    ct.c_char_p)(
    ("git_worktree_lock", dll), (
    (1, "wt"),
    (1, "reason"),))

# Unlock a locked worktree
#
# @param wt Worktree to unlock
# @return 0 on success, 1 if worktree was not locked, error-code
#  otherwise
#
git_worktree_unlock = CFUNC(ct.c_int,
    ct.POINTER(git_worktree))(
    ("git_worktree_unlock", dll), (
    (1, "wt"),))

# Check if worktree is locked
#
# A worktree may be locked if the linked working tree is stored
# on a portable device which is not available.
#
# @param reason Buffer to store reason in. If NULL no reason is stored.
# @param wt Worktree to check
# @return 0 when the working tree not locked, a value greater
#  than zero if it is locked, less than zero if there was an
#  error
#
git_worktree_is_locked = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_worktree))(
    ("git_worktree_is_locked", dll), (
    (1, "reason"),
    (1, "wt"),))

# Retrieve the name of the worktree
#
# @param wt Worktree to get the name for
# @return The worktree's name. The pointer returned is valid for the
#  lifetime of the git_worktree
#
git_worktree_name = CFUNC(ct.c_char_p,
    ct.POINTER(git_worktree))(
    ("git_worktree_name", dll), (
    (1, "wt"),))

# Retrieve the filesystem path for the worktree
#
# @param wt Worktree to get the path for
# @return The worktree's filesystem path. The pointer returned
#  is valid for the lifetime of the git_worktree.
#
git_worktree_path = CFUNC(ct.c_char_p,
    ct.POINTER(git_worktree))(
    ("git_worktree_path", dll), (
    (1, "wt"),))

# Flags which can be passed to git_worktree_prune to alter its
# behavior.
#
git_worktree_prune_t = ct.c_int
(   # Prune working tree even if working tree is valid
    GIT_WORKTREE_PRUNE_VALID,
    # Prune working tree even if it is locked
    GIT_WORKTREE_PRUNE_LOCKED,
    # Prune checked out working tree
    GIT_WORKTREE_PRUNE_WORKING_TREE,
) = (1 << 0, 1 << 1, 1 << 2)

# Worktree prune options structure
#
# Initialize with `GIT_WORKTREE_PRUNE_OPTIONS_INIT`. Alternatively, you can
# use `git_worktree_prune_options_init`.
#
#
class git_worktree_prune_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # A combination of `git_worktree_prune_t`
    ("flags", ct.c_uint32),
]

GIT_WORKTREE_PRUNE_OPTIONS_VERSION = 1
#define GIT_WORKTREE_PRUNE_OPTIONS_INIT {GIT_WORKTREE_PRUNE_OPTIONS_VERSION,0}

# Initialize git_worktree_prune_options structure
#
# Initializes a `git_worktree_prune_options` with default values. Equivalent to
# creating an instance with `GIT_WORKTREE_PRUNE_OPTIONS_INIT`.
#
# @param opts The `git_worktree_prune_options` struct to initialize.
# @param version The struct version; pass `GIT_WORKTREE_PRUNE_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_worktree_prune_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_worktree_prune_options),
    ct.c_uint)(
    ("git_worktree_prune_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Is the worktree prunable with the given options?
#
# A worktree is not prunable in the following scenarios:
#
# - the worktree is linking to a valid on-disk worktree. The
#   `valid` member will cause this check to be ignored.
# - the worktree is locked. The `locked` flag will cause this
#   check to be ignored.
#
# If the worktree is not valid and not locked or if the above
# flags have been passed in, this function will return a
# positive value. If the worktree is not prunable, an error
# message will be set (visible in `giterr_last`) with details about
# why.
#
# @param wt Worktree to check.
# @param opts The prunable options.
# @return 1 if the worktree is prunable, 0 otherwise, or an error code.
#
git_worktree_is_prunable = CFUNC(ct.c_int,
    ct.POINTER(git_worktree),
    ct.POINTER(git_worktree_prune_options))(
    ("git_worktree_is_prunable", dll), (
    (1, "wt"),
    (1, "opts"),))

# Prune working tree
#
# Prune the working tree, that is remove the git data
# structures on disk. The repository will only be pruned of
# `git_worktree_is_prunable` succeeds.
#
# @param wt Worktree to prune
# @param opts Specifies which checks to override. See
#        `git_worktree_is_prunable`. May be NULL
# @return 0 or an error code
#
git_worktree_prune = CFUNC(ct.c_int,
    ct.POINTER(git_worktree),
    ct.POINTER(git_worktree_prune_options))(
    ("git_worktree_prune", dll), (
    (1, "wt"),
    (1, "opts"),))

# GIT_END_DECL
