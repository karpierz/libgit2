# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid
from .types  import git_revwalk
from .types  import git_repository

# @file git2/revwalk.h
# @brief Git revision traversal routines
# @defgroup git_revwalk Git revision traversal routines
# @ingroup Git

# GIT_BEGIN_DECL

# Flags to specify the sorting which a revwalk should perform.
#
git_sort_t = ct.c_int
(
    # Sort the output with the same default method from `git`: reverse
    # chronological order. This is the default sorting for new walkers.
    #
    GIT_SORT_NONE,

    # Sort the repository contents in topological order (no parents before
    # all of its children are shown); this sorting mode can be combined
    # with time sorting to produce `git`'s `--date-order``.
    #
    GIT_SORT_TOPOLOGICAL,

    # Sort the repository contents by commit time;
    # this sorting mode can be combined with
    # topological sorting.
    #
    GIT_SORT_TIME,

    # Iterate through the repository contents in reverse
    # order; this sorting mode can be combined with
    # any of the above.
    #
    GIT_SORT_REVERSE,

) = (0, 1 << 0, 1 << 1, 1 << 2)

# Allocate a new revision walker to iterate through a repo.
#
# This revision walker uses a custom memory pool and an internal
# commit cache, so it is relatively expensive to allocate.
#
# For maximum performance, this revision walker should be
# reused for different walks.
#
# This revision walker is *not* thread safe: it may only be
# used to walk a repository on a single thread; however,
# it is possible to have several revision walkers in
# several different threads walking the same repository.
#
# @param out pointer to the new revision walker
# @param repo the repo to walk through
# @return 0 or an error code
#
git_revwalk_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_revwalk)),
    ct.POINTER(git_repository))(
    ("git_revwalk_new", dll), (
    (1, "out"),
    (1, "repo"),))

# Reset the revision walker for reuse.
#
# This will clear all the pushed and hidden commits, and
# leave the walker in a blank state (just like at
# creation) ready to receive new commit pushes and
# start a new walk.
#
# The revision walk is automatically reset when a walk
# is over.
#
# @param walker handle to reset.
# @return 0 or an error code
#
git_revwalk_reset = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk))(
    ("git_revwalk_reset", dll), (
    (1, "walker"),))

# Add a new root for the traversal
#
# The pushed commit will be marked as one of the roots from which to
# start the walk. This commit may not be walked if it or a child is
# hidden.
#
# At least one commit must be pushed onto the walker before a walk
# can be started.
#
# The given id must belong to a committish on the walked
# repository.
#
# @param walk the walker being used for the traversal.
# @param id the oid of the commit to start from.
# @return 0 or an error code
#
git_revwalk_push = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk),
    ct.POINTER(git_oid))(
    ("git_revwalk_push", dll), (
    (1, "walk"),
    (1, "id"),))

# Push matching references
#
# The OIDs pointed to by the references that match the given glob
# pattern will be pushed to the revision walker.
#
# A leading 'refs/' is implied if not present as well as a trailing
# '/\*' if the glob lacks '?', '\*' or '['.
#
# Any references matching this glob which do not point to a
# committish will be ignored.
#
# @param walk the walker being used for the traversal
# @param glob the glob pattern references should match
# @return 0 or an error code
#
git_revwalk_push_glob = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk),
    ct.c_char_p)(
    ("git_revwalk_push_glob", dll), (
    (1, "walk"),
    (1, "glob"),))

# Push the repository's HEAD
#
# @param walk the walker being used for the traversal
# @return 0 or an error code
#
git_revwalk_push_head = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk))(
    ("git_revwalk_push_head", dll), (
    (1, "walk"),))

# Mark a commit (and its ancestors) uninteresting for the output.
#
# The given id must belong to a committish on the walked
# repository.
#
# The resolved commit and all its parents will be hidden from the
# output on the revision walk.
#
# @param walk the walker being used for the traversal.
# @param commit_id the oid of commit that will be ignored during the traversal
# @return 0 or an error code
#
git_revwalk_hide = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk),
    ct.POINTER(git_oid))(
    ("git_revwalk_hide", dll), (
    (1, "walk"),
    (1, "commit_id"),))

# Hide matching references.
#
# The OIDs pointed to by the references that match the given glob
# pattern and their ancestors will be hidden from the output on the
# revision walk.
#
# A leading 'refs/' is implied if not present as well as a trailing
# '/\*' if the glob lacks '?', '\*' or '['.
#
# Any references matching this glob which do not point to a
# committish will be ignored.
#
# @param walk the walker being used for the traversal
# @param glob the glob pattern references should match
# @return 0 or an error code
#
git_revwalk_hide_glob = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk),
    ct.c_char_p)(
    ("git_revwalk_hide_glob", dll), (
    (1, "walk"),
    (1, "glob"),))

# Hide the repository's HEAD
#
# @param walk the walker being used for the traversal
# @return 0 or an error code
#
git_revwalk_hide_head = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk))(
    ("git_revwalk_hide_head", dll), (
    (1, "walk"),))

# Push the OID pointed to by a reference
#
# The reference must point to a committish.
#
# @param walk the walker being used for the traversal
# @param refname the reference to push
# @return 0 or an error code
#
git_revwalk_push_ref = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk),
    ct.c_char_p)(
    ("git_revwalk_push_ref", dll), (
    (1, "walk"),
    (1, "refname"),))

# Hide the OID pointed to by a reference
#
# The reference must point to a committish.
#
# @param walk the walker being used for the traversal
# @param refname the reference to hide
# @return 0 or an error code
#
git_revwalk_hide_ref = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk),
    ct.c_char_p)(
    ("git_revwalk_hide_ref", dll), (
    (1, "walk"),
    (1, "refname"),))

# Get the next commit from the revision walk.
#
# The initial call to this method is *not* blocking when
# iterating through a repo with a time-sorting mode.
#
# Iterating with Topological or inverted modes makes the initial
# call blocking to preprocess the commit list, but this block should be
# mostly unnoticeable on most repositories (topological preprocessing
# times at 0.3s on the git.git repo).
#
# The revision walker is reset when the walk is over.
#
# @param out Pointer where to store the oid of the next commit
# @param walk the walker to pop the commit from.
# @return 0 if the next commit was found;
#  GIT_ITEROVER if there are no commits left to iterate
#
git_revwalk_next = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_revwalk))(
    ("git_revwalk_next", dll), (
    (1, "out"),
    (1, "walk"),))

# Change the sorting mode when iterating through the
# repository's contents.
#
# Changing the sorting mode resets the walker.
#
# @param walk the walker being used for the traversal.
# @param sort_mode combination of GIT_SORT_XXX flags
# @return 0 or an error code
#
git_revwalk_sorting = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk),
    ct.c_uint)(
    ("git_revwalk_sorting", dll), (
    (1, "walk"),
    (1, "sort_mode"),))

# Push and hide the respective endpoints of the given range.
#
# The range should be of the form
#   <commit>..<commit>
# where each <commit> is in the form accepted by 'git_revparse_single'.
# The left-hand commit will be hidden and the right-hand commit pushed.
#
# @param walk the walker being used for the traversal
# @param range the range
# @return 0 or an error code
#
#
git_revwalk_push_range = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk),
    ct.c_char_p)(
    ("git_revwalk_push_range", dll), (
    (1, "walk"),
    (1, "range"),))

# Simplify the history by first-parent
#
# No parents other than the first for each commit will be enqueued.
#
# @param walk The revision walker.
# @return 0 or an error code
#
git_revwalk_simplify_first_parent = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk))(
    ("git_revwalk_simplify_first_parent", dll), (
    (1, "walk"),))

# Free a revision walker previously allocated.
#
# @param walk traversal handle to close. If NULL nothing occurs.
#
git_revwalk_free = CFUNC(None,
    ct.POINTER(git_revwalk))(
    ("git_revwalk_free", dll), (
    (1, "walk"),))

# Return the repository on which this walker
# is operating.
#
# @param walk the revision walker
# @return the repository being walked
#
git_revwalk_repository = CFUNC(ct.POINTER(git_repository),
    ct.POINTER(git_revwalk))(
    ("git_revwalk_repository", dll), (
    (1, "walk"),))

# This is a callback function that user can provide to hide a
# commit and its parents. If the callback function returns non-zero value,
# then this commit and its parents will be hidden.
#
# @param commit_id oid of Commit
# @param payload User-specified pointer to data to be passed as data payload
# @return non-zero to hide the commmit and it parent.
#
git_revwalk_hide_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_oid),  # commit_id
    ct.c_void_p)          # payload

# Adds, changes or removes a callback function to hide a commit and its parents
#
# @param walk the revision walker
# @param hide_cb  callback function to hide a commit and its parents
# @param payload  data payload to be passed to callback function
# @return 0 or an error code.
#
git_revwalk_add_hide_cb = CFUNC(ct.c_int,
    ct.POINTER(git_revwalk),
    git_revwalk_hide_cb,
    ct.c_void_p)(
    ("git_revwalk_add_hide_cb", dll), (
    (1, "walk"),
    (1, "hide_cb"),
    (1, "payload"),))

# GIT_END_DECL
