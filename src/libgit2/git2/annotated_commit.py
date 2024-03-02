# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid
from .types  import git_repository
from .types  import git_reference
from .types  import git_annotated_commit

# @file git2/annotated_commit.h
# @brief Git annotated commit routines
# @defgroup git_annotated_commit Git annotated commit routines
# @ingroup Git

# GIT_BEGIN_DECL

# Creates a `git_annotated_commit` from the given reference.
# The resulting git_annotated_commit must be freed with
# `git_annotated_commit_free`.
#
# @param out pointer to store the git_annotated_commit result in
# @param repo repository that contains the given reference
# @param ref reference to use to lookup the git_annotated_commit
# @return 0 on success or error code
#
git_annotated_commit_from_ref = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_annotated_commit)),
    ct.POINTER(git_repository),
    ct.POINTER(git_reference))(
    ("git_annotated_commit_from_ref", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "ref"),))

# Creates a `git_annotated_commit` from the given fetch head data.
# The resulting git_annotated_commit must be freed with
# `git_annotated_commit_free`.
#
# @param out pointer to store the git_annotated_commit result in
# @param repo repository that contains the given commit
# @param branch_name name of the (remote) branch
# @param remote_url url of the remote
# @param id the commit object id of the remote branch
# @return 0 on success or error code
#
git_annotated_commit_from_fetchhead = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_annotated_commit)),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.c_char_p,
    ct.POINTER(git_oid))(
    ("git_annotated_commit_from_fetchhead", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "branch_name"),
    (1, "remote_url"),
    (1, "id"),))

# Creates a `git_annotated_commit` from the given commit id.
# The resulting git_annotated_commit must be freed with
# `git_annotated_commit_free`.
#
# An annotated commit contains information about how it was
# looked up, which may be useful for functions like merge or
# rebase to provide context to the operation.  For example,
# conflict files will include the name of the source or target
# branches being merged.  It is therefore preferable to use the
# most specific function (eg `git_annotated_commit_from_ref`)
# instead of this one when that data is known.
#
# @param out pointer to store the git_annotated_commit result in
# @param repo repository that contains the given commit
# @param id the commit object id to lookup
# @return 0 on success or error code
#
git_annotated_commit_lookup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_annotated_commit)),
    ct.POINTER(git_repository),
    ct.POINTER(git_oid))(
    ("git_annotated_commit_lookup", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "id"),))

# Creates a `git_annotated_commit` from a revision string.
#
# See `man gitrevisions`, or
# http://git-scm.com/docs/git-rev-parse.html#_specifying_revisions for
# information on the syntax accepted.
#
# @param out pointer to store the git_annotated_commit result in
# @param repo repository that contains the given commit
# @param revspec the extended sha syntax string to use to lookup the commit
# @return 0 on success or error code
#
git_annotated_commit_from_revspec = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_annotated_commit)),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_annotated_commit_from_revspec", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "revspec"),))

# Gets the commit ID that the given `git_annotated_commit` refers to.
#
# @param commit the given annotated commit
# @return commit id
#
git_annotated_commit_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_annotated_commit))(
    ("git_annotated_commit_id", dll), (
    (1, "commit"),))

# Get the refname that the given `git_annotated_commit` refers to.
#
# @param commit the given annotated commit
# @return ref name.
#
git_annotated_commit_ref = CFUNC(ct.c_char_p,
    ct.POINTER(git_annotated_commit))(
    ("git_annotated_commit_ref", dll), (
    (1, "commit"),))

# Frees a `git_annotated_commit`.
#
# @param commit annotated commit to free
#
git_annotated_commit_free = CFUNC(None,
    ct.POINTER(git_annotated_commit))(
    ("git_annotated_commit_free", dll), (
    (1, "commit"),))

# GIT_END_DECL
