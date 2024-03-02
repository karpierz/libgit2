# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .buffer import git_buf
from .types  import git_repository
from .types  import git_branch_t
from .types  import git_reference
from .types  import git_annotated_commit
from .types  import git_commit

# @file git2/branch.h
# @brief Git branch parsing routines
# @defgroup git_branch Git branch management
# @ingroup Git

# GIT_BEGIN_DECL

# Create a new branch pointing at a target commit
#
# A new direct reference will be created pointing to
# this target commit. If `force` is true and a reference
# already exists with the given name, it'll be replaced.
#
# The returned reference must be freed by the user.
#
# The branch name will be checked for validity.
# See `git_tag_create()` for rules about valid names.
#
# @param out Pointer where to store the underlying reference.
#
# @param repo the repository to create the branch in.
#
# @param branch_name Name for the branch; this name is
# validated for consistency. It should also not conflict with
# an already existing branch name.
#
# @param target Commit to which this branch should point. This object
# must belong to the given `repo`.
#
# @param force Overwrite existing branch.
#
# @return 0, GIT_EINVALIDSPEC or an error code.
# A proper reference is written in the refs/heads namespace
# pointing to the provided target commit.
#
git_branch_create = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_reference)),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_commit),
    ct.c_int)(
    ("git_branch_create", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "branch_name"),
    (1, "target"),
    (1, "force"),))

# Create a new branch pointing at a target commit
#
# This behaves like `git_branch_create()` but takes an annotated
# commit, which lets you specify which extended sha syntax string was
# specified by a user, allowing for more exact reflog messages.
#
# See the documentation for `git_branch_create()`.
#
# @see git_branch_create
#
git_branch_create_from_annotated = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_reference)),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_annotated_commit),
    ct.c_int)(
    ("git_branch_create_from_annotated", dll), (
    (1, "ref_out"),
    (1, "repository"),
    (1, "branch_name"),
    (1, "commit"),
    (1, "force"),))

# Delete an existing branch reference.
#
# Note that if the deletion succeeds, the reference object will not
# be valid anymore, and should be freed immediately by the user using
# `git_reference_free()`.
#
# @param branch A valid reference representing a branch
# @return 0 on success, or an error code.
#
git_branch_delete = CFUNC(ct.c_int,
    ct.POINTER(git_reference))(
    ("git_branch_delete", dll), (
    (1, "branch"),))

# Iterator type for branches
class git_branch_iterator(ct.Structure): pass

# Create an iterator which loops over the requested branches.
#
# @param out the iterator
# @param repo Repository where to find the branches.
# @param list_flags Filtering flags for the branch
# listing. Valid values are GIT_BRANCH_LOCAL, GIT_BRANCH_REMOTE
# or GIT_BRANCH_ALL.
#
# @return 0 on success  or an error code
#
git_branch_iterator_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_branch_iterator)),
    ct.POINTER(git_repository),
    git_branch_t)(
    ("git_branch_iterator_new", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "list_flags"),))

# Retrieve the next branch from the iterator
#
# @param out the reference
# @param out_type the type of branch (local or remote-tracking)
# @param iter the branch iterator
# @return 0 on success, GIT_ITEROVER if there are no more branches or an error code.
#
git_branch_next = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_reference)),
    ct.POINTER(git_branch_t),
    ct.POINTER(git_branch_iterator))(
    ("git_branch_next", dll), (
    (1, "out"),
    (1, "out_type"),
    (1, "iter"),))

# Free a branch iterator
#
# @param iter the iterator to free
#
git_branch_iterator_free = CFUNC(None,
    ct.POINTER(git_branch_iterator))(
    ("git_branch_iterator_free", dll), (
    (1, "iter"),))

# Move/rename an existing local branch reference.
#
# The new branch name will be checked for validity.
# See `git_tag_create()` for rules about valid names.
#
# Note that if the move succeeds, the old reference object will not
# be valid anymore, and should be freed immediately by the user using
# `git_reference_free()`.
#
# @param out New reference object for the updated name.
#
# @param branch Current underlying reference of the branch.
#
# @param new_branch_name Target name of the branch once the move
# is performed; this name is validated for consistency.
#
# @param force Overwrite existing branch.
#
# @return 0 on success, GIT_EINVALIDSPEC or an error code.
#
git_branch_move = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_reference)),
    ct.POINTER(git_reference),
    ct.c_char_p,
    ct.c_int)(
    ("git_branch_move", dll), (
    (1, "out"),
    (1, "branch"),
    (1, "new_branch_name"),
    (1, "force"),))

# Lookup a branch by its name in a repository.
#
# The generated reference must be freed by the user.
# The branch name will be checked for validity.
#
# @see git_tag_create for rules about valid names.
#
# @param out pointer to the looked-up branch reference
# @param repo the repository to look up the branch
# @param branch_name Name of the branch to be looked-up;
# this name is validated for consistency.
# @param branch_type Type of the considered branch. This should
# be valued with either GIT_BRANCH_LOCAL or GIT_BRANCH_REMOTE.
#
# @return 0 on success; GIT_ENOTFOUND when no matching branch
# exists, GIT_EINVALIDSPEC, otherwise an error code.
#
git_branch_lookup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_reference)),
    ct.POINTER(git_repository),
    ct.c_char_p,
    git_branch_t)(
    ("git_branch_lookup", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "branch_name"),
    (1, "branch_type"),))

# Get the branch name
#
# Given a reference object, this will check that it really is a branch (ie.
# it lives under "refs/heads/" or "refs/remotes/"), and return the branch part
# of it.
#
# @param out Pointer to the abbreviated reference name.
#        Owned by ref, do not free.
#
# @param ref A reference object, ideally pointing to a branch
#
# @return 0 on success; GIT_EINVALID if the reference isn't either a local or
#         remote branch, otherwise an error code.
#
git_branch_name = CFUNC(ct.c_int,
    ct.POINTER(ct.c_char_p),
    ct.POINTER(git_reference))(
    ("git_branch_name", dll), (
    (1, "out"),
    (1, "ref"),))

# Get the upstream of a branch
#
# Given a reference, this will return a new reference object corresponding
# to its remote tracking branch. The reference must be a local branch.
#
# @see git_branch_upstream_name for details on the resolution.
#
# @param out Pointer where to store the retrieved reference.
# @param branch Current underlying reference of the branch.
#
# @return 0 on success; GIT_ENOTFOUND when no remote tracking
#         reference exists, otherwise an error code.
#
git_branch_upstream = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_reference)),
    ct.POINTER(git_reference))(
    ("git_branch_upstream", dll), (
    (1, "out"),
    (1, "branch"),))

# Set a branch's upstream branch
#
# This will update the configuration to set the branch named `branch_name` as the upstream of `branch`.
# Pass a NULL name to unset the upstream information.
#
# @note the actual tracking reference must have been already created for the
# operation to succeed.
#
# @param branch the branch to configure
# @param branch_name remote-tracking or local branch to set as upstream.
#
# @return 0 on success; GIT_ENOTFOUND if there's no branch named `branch_name`
#         or an error code
#
git_branch_set_upstream = CFUNC(ct.c_int,
    ct.POINTER(git_reference),
    ct.c_char_p)(
    ("git_branch_set_upstream", dll), (
    (1, "branch"),
    (1, "branch_name"),))

# Get the upstream name of a branch
#
# Given a local branch, this will return its remote-tracking branch information,
# as a full reference name, ie. "feature/nice" would become
# "refs/remote/origin/feature/nice", depending on that branch's configuration.
#
# @param out the buffer into which the name will be written.
# @param repo the repository where the branches live.
# @param refname reference name of the local branch.
#
# @return 0 on success, GIT_ENOTFOUND when no remote tracking reference exists,
#         or an error code.
#
git_branch_upstream_name = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_branch_upstream_name", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "refname"),))

# Determine if HEAD points to the given branch
#
# @param branch A reference to a local branch.
#
# @return 1 if HEAD points at the branch, 0 if it isn't, or a negative value
#         as an error code.
#
git_branch_is_head = CFUNC(ct.c_int,
    ct.POINTER(git_reference))(
    ("git_branch_is_head", dll), (
    (1, "branch"),))

# Determine if any HEAD points to the current branch
#
# This will iterate over all known linked repositories (usually in the form of
# worktrees) and report whether any HEAD is pointing at the current branch.
#
# @param branch A reference to a local branch.
#
# @return 1 if branch is checked out, 0 if it isn't, an error code otherwise.
#
git_branch_is_checked_out = CFUNC(ct.c_int,
    ct.POINTER(git_reference))(
    ("git_branch_is_checked_out", dll), (
    (1, "branch"),))

# Find the remote name of a remote-tracking branch
#
# This will return the name of the remote whose fetch refspec is matching
# the given branch. E.g. given a branch "refs/remotes/test/master", it will
# extract the "test" part. If refspecs from multiple remotes match,
# the function will return GIT_EAMBIGUOUS.
#
# @param out The buffer into which the name will be written.
# @param repo The repository where the branch lives.
# @param refname complete name of the remote tracking branch.
#
# @return 0 on success, GIT_ENOTFOUND when no matching remote was found,
#         GIT_EAMBIGUOUS when the branch maps to several remotes,
#         otherwise an error code.
#
git_branch_remote_name = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_branch_remote_name", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "refname"),))

# Retrieve the upstream remote of a local branch
#
# This will return the currently configured "branch.*.remote" for a given
# branch. This branch must be local.
#
# @param buf the buffer into which to write the name
# @param repo the repository in which to look
# @param refname the full name of the branch
# @return 0 or an error code
#
git_branch_upstream_remote = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_branch_upstream_remote", dll), (
    (1, "buf"),
    (1, "repo"),
    (1, "refname"),))

# Retrieve the upstream merge of a local branch
#
# This will return the currently configured "branch.*.merge" for a given
# branch. This branch must be local.
#
# @param buf the buffer into which to write the name
# @param repo the repository in which to look
# @param refname the full name of the branch
# @return 0 or an error code
#
git_branch_upstream_merge = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_branch_upstream_merge", dll), (
    (1, "buf"),
    (1, "repo"),
    (1, "refname"),))

# Determine whether a branch name is valid, meaning that (when prefixed
# with `refs/heads/`) that it is a valid reference name, and that any
# additional branch name restrictions are imposed (eg, it cannot start
# with a `-`).
#
# @param valid output pointer to set with validity of given branch name
# @param name a branch name to test
# @return 0 on success or an error code
#
git_branch_name_is_valid = CFUNC(ct.c_int,
    ct.POINTER(ct.c_int),
    ct.c_char_p)(
    ("git_branch_name_is_valid", dll), (
    (1, "valid"),
    (1, "name"),))

# GIT_END_DECL
