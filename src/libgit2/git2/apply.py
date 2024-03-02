# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .types  import git_repository
from .diff   import git_diff
from .diff   import git_diff_delta
from .diff   import git_diff_hunk
from .types  import git_index
from .types  import git_tree

# @file git2/apply.h
# @brief Git patch application routines
# @defgroup git_apply Git patch application routines
# @ingroup Git

# GIT_BEGIN_DECL

# When applying a patch, callback that will be made per delta (file).
#
# When the callback:
# - returns < 0, the apply process will be aborted.
# - returns > 0, the delta will not be applied, but the apply process
#      continues
# - returns 0, the delta is applied, and the apply process continues.
#
# @param delta The delta to be applied
# @param payload User-specified payload
# @return 0 if the delta is applied, < 0 if the apply process will be aborted
#  or > 0 if the delta will not be applied.
#
git_apply_delta_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_diff_delta),  # delta
    ct.c_void_p)                 # payload

# When applying a patch, callback that will be made per hunk.
#
# When the callback:
# - returns < 0, the apply process will be aborted.
# - returns > 0, the hunk will not be applied, but the apply process
#      continues
# - returns 0, the hunk is applied, and the apply process continues.
#
# @param hunk The hunk to be applied
# @param payload User-specified payload
# @return 0 if the hunk is applied, < 0 if the apply process will be aborted
#  or > 0 if the hunk will not be applied.
#
git_apply_hunk_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_diff_hunk),  # hunk
    ct.c_void_p)                # payload

# Flags controlling the behavior of git_apply
git_apply_flags_t = ct.c_int
(   # Don't actually make changes, just test that the patch applies.
    # This is the equivalent of `git apply --check`.
    GIT_APPLY_CHECK,
) = (1 << 0,)

# Apply options structure
#
# Initialize with `GIT_APPLY_OPTIONS_INIT`. Alternatively, you can
# use `git_apply_options_init`.
#
# @see git_apply_to_tree, git_apply
#
class git_apply_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),  # The version

    # When applying a patch, callback that will be made per delta (file).
    ("delta_cb", git_apply_delta_cb),

    # When applying a patch, callback that will be made per hunk.
    ("hunk_cb", git_apply_hunk_cb),

    # Payload passed to both delta_cb & hunk_cb.
    ("payload", ct.c_void_p),

    # Bitmask of git_apply_flags_t
    ("flags", ct.c_uint),
]

GIT_APPLY_OPTIONS_VERSION = 1
#define GIT_APPLY_OPTIONS_INIT = { GIT_APPLY_OPTIONS_VERSION }

# Initialize git_apply_options structure
#
# Initialize a `git_apply_options` with default values. Equivalent to creating
# an instance with GIT_APPLY_OPTIONS_INIT.
#
# @param opts The `git_apply_options` struct to initialize.
# @param version The struct version; pass `GIT_APPLY_OPTIONS_VERSION`
# @return 0 on success or -1 on failure.
#
git_apply_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_apply_options),
    ct.c_uint)(
    ("git_apply_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Apply a `git_diff` to a `git_tree`, and return the resulting image
# as an index.
#
# @param out the postimage of the application
# @param repo the repository to apply
# @param preimage the tree to apply the diff to
# @param diff the diff to apply
# @param options the options for the apply (or null for defaults)
# @return 0 or an error code
#
git_apply_to_tree = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index)),
    ct.POINTER(git_repository),
    ct.POINTER(git_tree),
    ct.POINTER(git_diff),
    ct.POINTER(git_apply_options))(
    ("git_apply_to_tree", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "preimage"),
    (1, "diff"),
    (1, "options"),))

# Possible application locations for git_apply
git_apply_location_t = ct.c_int
(   # Apply the patch to the workdir, leaving the index untouched.
    # This is the equivalent of `git apply` with no location argument.
    GIT_APPLY_LOCATION_WORKDIR,

    # Apply the patch to the index, leaving the working directory
    # untouched.  This is the equivalent of `git apply --cached`.
    GIT_APPLY_LOCATION_INDEX,

    # Apply the patch to both the working directory and the index.
    # This is the equivalent of `git apply --index`.
    GIT_APPLY_LOCATION_BOTH,
) = (0, 1, 2)

# Apply a `git_diff` to the given repository, making changes directly
# in the working directory, the index, or both.
#
# @param repo the repository to apply to
# @param diff the diff to apply
# @param location the location to apply (workdir, index or both)
# @param options the options for the apply (or null for defaults)
# @return 0 or an error code
#
git_apply = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_diff),
    git_apply_location_t,
    ct.POINTER(git_apply_options))(
    ("git_apply", dll), (
    (1, "repo"),
    (1, "diff"),
    (1, "location"),
    (1, "options"),))

# GIT_END_DECL
