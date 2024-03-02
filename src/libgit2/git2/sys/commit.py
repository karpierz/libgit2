# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..oid    import git_oid
from ..types  import git_repository
from ..types  import git_signature

# @file git2/sys/commit.h
# @brief Low-level Git commit creation
# @defgroup git_backend Git custom backend APIs
# @ingroup Git

# GIT_BEGIN_DECL

# Create new commit in the repository from a list of `git_oid` values.
#
# See documentation for `git_commit_create()` for information about the
# parameters, as the meaning is identical excepting that `tree` and
# `parents` now take `git_oid`.  This is a dangerous API in that nor
# the `tree`, neither the `parents` list of `git_oid`s are checked for
# validity.
#
# @see git_commit_create
#
git_commit_create_from_ids = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_signature),
    ct.POINTER(git_signature),
    ct.c_char_p,
    ct.c_char_p,
    ct.POINTER(git_oid),
    ct.c_size_t,
    (ct.POINTER(git_oid) * 0))( # []
    ("git_commit_create_from_ids", dll), (
    (1, "id"),
    (1, "repo"),
    (1, "update_ref"),
    (1, "author"),
    (1, "committer"),
    (1, "message_encoding"),
    (1, "message"),
    (1, "tree"),
    (1, "parent_count"),
    (1, "parents"),))

# Callback function to return parents for commit.
#
# This is invoked with the count of the number of parents processed so far
# along with the user supplied payload.  This should return a git_oid of
# the next parent or NULL if all parents have been provided.
#
git_commit_parent_callback = GIT_CALLBACK(ct.POINTER(git_oid),
    ct.c_size_t,  # idx
    ct.c_void_p)  # payload

# Create a new commit in the repository with an callback to supply parents.
#
# See documentation for `git_commit_create()` for information about the
# parameters, as the meaning is identical excepting that `tree` takes a
# `git_oid` and doesn't check for validity, and `parent_cb` is invoked
# with `parent_payload` and should return `git_oid` values or NULL to
# indicate that all parents are accounted for.
#
# @see git_commit_create
#
git_commit_create_from_callback = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_signature),
    ct.POINTER(git_signature),
    ct.c_char_p,
    ct.c_char_p,
    ct.POINTER(git_oid),
    git_commit_parent_callback,
    ct.c_void_p)(
    ("git_commit_create_from_callback", dll), (
    (1, "id"),
    (1, "repo"),
    (1, "update_ref"),
    (1, "author"),
    (1, "committer"),
    (1, "message_encoding"),
    (1, "message"),
    (1, "tree"),
    (1, "parent_cb"),
    (1, "parent_payload"),))

# GIT_END_DECL
