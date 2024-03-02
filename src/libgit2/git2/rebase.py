# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

import sys

from .common   import *  # noqa
from .buffer   import git_buf
from .oid      import git_oid
from .types    import git_repository
from .types    import git_signature
from .types    import git_index
from .types    import git_rebase
from .types    import git_annotated_commit
from .commit   import git_commit_create_cb
from .merge    import git_merge_options
from .checkout import git_checkout_options

# @file git2/rebase.h
# @brief Git rebase routines
# @defgroup git_rebase Git merge routines
# @ingroup Git

# GIT_BEGIN_DECL

# Rebase options
#
# Use to tell the rebase machinery how to operate.
#
class git_rebase_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # Used by `git_rebase_init`, this will instruct other clients working
    # on this rebase that you want a quiet rebase experience, which they
    # may choose to provide in an application-specific manner.  This has no
    # effect upon libgit2 directly, but is provided for interoperability
    # between Git tools.
    #
    ("quiet", ct.c_int),

    # Used by `git_rebase_init`, this will begin an in-memory rebase,
    # which will allow callers to step through the rebase operations and
    # commit the rebased changes, but will not rewind HEAD or update the
    # repository to be in a rebasing state.  This will not interfere with
    # the working directory (if there is one).
    #
    ("inmemory", ct.c_int),

    # Used by `git_rebase_finish`, this is the name of the notes reference
    # used to rewrite notes for rebased commits when finishing the rebase;
    # if NULL, the contents of the configuration option `notes.rewriteRef`
    # is examined, unless the configuration option `notes.rewrite.rebase`
    # is set to false.  If `notes.rewriteRef` is also NULL, notes will
    # not be rewritten.
    #
    ("rewrite_notes_ref", ct.c_char_p),

    # Options to control how trees are merged during `git_rebase_next`.
    #
    ("merge_options", git_merge_options),

    # Options to control how files are written during `git_rebase_init`,
    # `git_rebase_next` and `git_rebase_abort`.  Note that a minimum
    # strategy of `GIT_CHECKOUT_SAFE` is defaulted in `init` and `next`,
    # and a minimum strategy of `GIT_CHECKOUT_FORCE` is defaulted in
    # `abort` to match git semantics.
    #
    ("checkout_options", git_checkout_options),

    # Optional callback that allows users to override commit
    # creation in `git_rebase_commit`.  If specified, users can
    # create their own commit and provide the commit ID, which
    # may be useful for signing commits or otherwise customizing
    # the commit creation.
    #
    # If this callback returns `GIT_PASSTHROUGH`, then
    # `git_rebase_commit` will continue to create the commit.
    #
    ("commit_create_cb", git_commit_create_cb),

    *([("reserved", ct.c_void_p)]
      if defined("GIT_DEPRECATE_HARD") else
    # If provided, this will be called with the commit content, allowing
    # a signature to be added to the rebase commit. Can be skipped with
    # GIT_PASSTHROUGH. If GIT_PASSTHROUGH is returned, a commit will be made
    # without a signature.
    #
    # This field is only used when performing git_rebase_commit.
    #
    # This callback is not invoked if a `git_commit_create_cb` is
    # specified.
    #
    # This callback is deprecated; users should provide a
    # creation callback as `commit_create_cb` that produces a
    # commit buffer, signs it, and commits it.
    #
    [("signing_cb", CFUNC(ct.c_int,
                        ct.POINTER(git_buf),
                        ct.POINTER(git_buf),
                        ct.c_char_p,
                        ct.c_void_p))]),

    # This will be passed to each of the callbacks in this struct
    # as the last parameter.
    #
    ("payload", ct.c_void_p),
]

# Type of rebase operation in-progress after calling `git_rebase_next`.
#
git_rebase_operation_t = ct.c_int
(
    # The given commit is to be cherry-picked.  The client should commit
    # the changes and continue if there are no conflicts.
    #
    GIT_REBASE_OPERATION_PICK,

    # The given commit is to be cherry-picked, but the client should prompt
    # the user to provide an updated commit message.
    #
    GIT_REBASE_OPERATION_REWORD,

    # The given commit is to be cherry-picked, but the client should stop
    # to allow the user to edit the changes before committing them.
    #
    GIT_REBASE_OPERATION_EDIT,

    # The given commit is to be squashed into the previous commit.  The
    # commit message will be merged with the previous message.
    #
    GIT_REBASE_OPERATION_SQUASH,

    # The given commit is to be squashed into the previous commit.  The
    # commit message from this commit will be discarded.
    #
    GIT_REBASE_OPERATION_FIXUP,

    # No commit will be cherry-picked.  The client should run the given
    # command and (if successful) continue.
    #
    GIT_REBASE_OPERATION_EXEC,

) = range(0, 6)

GIT_REBASE_OPTIONS_VERSION = 1
#define GIT_REBASE_OPTIONS_INIT = { GIT_REBASE_OPTIONS_VERSION, 0, 0, NULL,
#                                   GIT_MERGE_OPTIONS_INIT,
#                                   GIT_CHECKOUT_OPTIONS_INIT, NULL, NULL }

# Indicates that a rebase operation is not (yet) in progress.
GIT_REBASE_NO_OPERATION = sys.maxsize  # SIZE_MAX

# A rebase operation
#
# Describes a single instruction/operation to be performed during the
# rebase.
#
class git_rebase_operation(ct.Structure):
    _fields_ = [
    # The type of rebase operation.
    ("type", git_rebase_operation_t),

    # The commit ID being cherry-picked.  This will be populated for
    # all operations except those of type `GIT_REBASE_OPERATION_EXEC`.
    #
    ("id", git_oid),

    # The executable the user has requested be run.  This will only
    # be populated for operations of type `GIT_REBASE_OPERATION_EXEC`.
    #
    ("exec", ct.c_char_p),
]

# Initialize git_rebase_options structure
#
# Initializes a `git_rebase_options` with default values. Equivalent to
# creating an instance with `GIT_REBASE_OPTIONS_INIT`.
#
# @param opts The `git_rebase_options` struct to initialize.
# @param version The struct version; pass `GIT_REBASE_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_rebase_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_rebase_options),
    ct.c_uint)(
    ("git_rebase_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Initializes a rebase operation to rebase the changes in `branch`
# relative to `upstream` onto another branch.  To begin the rebase
# process, call `git_rebase_next`.  When you have finished with this
# object, call `git_rebase_free`.
#
# @param out Pointer to store the rebase object
# @param repo The repository to perform the rebase
# @param branch The terminal commit to rebase, or NULL to rebase the
#               current branch
# @param upstream The commit to begin rebasing from, or NULL to rebase all
#                 reachable commits
# @param onto The branch to rebase onto, or NULL to rebase onto the given
#             upstream
# @param opts Options to specify how rebase is performed, or NULL
# @return Zero on success; -1 on failure.
#
git_rebase_init = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_rebase)),
    ct.POINTER(git_repository),
    ct.POINTER(git_annotated_commit),
    ct.POINTER(git_annotated_commit),
    ct.POINTER(git_annotated_commit),
    ct.POINTER(git_rebase_options) )(
    ("git_rebase_init", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "branch"),
    (1, "upstream"),
    (1, "onto"),
    (1, "opts"),))

# Opens an existing rebase that was previously started by either an
# invocation of `git_rebase_init` or by another client.
#
# @param out Pointer to store the rebase object
# @param repo The repository that has a rebase in-progress
# @param opts Options to specify how rebase is performed
# @return Zero on success; -1 on failure.
#
git_rebase_open = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_rebase)),
    ct.POINTER(git_repository),
    ct.POINTER(git_rebase_options) )(
    ("git_rebase_open", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "opts"),))

# Gets the original `HEAD` ref name for merge rebases.
#
# @param rebase The in-progress rebase.
# @return The original `HEAD` ref name
#
git_rebase_orig_head_name = CFUNC(ct.c_char_p,
    ct.POINTER(git_rebase))(
    ("git_rebase_orig_head_name", dll), (
    (1, "rebase"),))

# Gets the original `HEAD` id for merge rebases.
#
# @param rebase The in-progress rebase.
# @return The original `HEAD` id
#
git_rebase_orig_head_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_rebase))(
    ("git_rebase_orig_head_id", dll), (
    (1, "rebase"),))

# Gets the `onto` ref name for merge rebases.
#
# @param rebase The in-progress rebase.
# @return The `onto` ref name
#
git_rebase_onto_name = CFUNC(ct.c_char_p,
    ct.POINTER(git_rebase))(
    ("git_rebase_onto_name", dll), (
    (1, "rebase"),))

# Gets the `onto` id for merge rebases.
#
# @param rebase The in-progress rebase.
# @return The `onto` id
#
git_rebase_onto_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_rebase))(
    ("git_rebase_onto_id", dll), (
    (1, "rebase"),))

# Gets the count of rebase operations that are to be applied.
#
# @param rebase The in-progress rebase
# @return The number of rebase operations in total
#
git_rebase_operation_entrycount = CFUNC(ct.c_size_t,
    ct.POINTER(git_rebase))(
    ("git_rebase_operation_entrycount", dll), (
    (1, "rebase"),))

# Gets the index of the rebase operation that is currently being applied.
# If the first operation has not yet been applied (because you have
# called `init` but not yet `next`) then this returns
# `GIT_REBASE_NO_OPERATION`.
#
# @param rebase The in-progress rebase
# @return The index of the rebase operation currently being applied.
#
git_rebase_operation_current = CFUNC(ct.c_size_t,
    ct.POINTER(git_rebase))(
    ("git_rebase_operation_current", dll), (
    (1, "rebase"),))

# Gets the rebase operation specified by the given index.
#
# @param rebase The in-progress rebase
# @param idx The index of the rebase operation to retrieve
# @return The rebase operation or NULL if `idx` was out of bounds
#
git_rebase_operation_byindex = CFUNC(ct.POINTER(git_rebase_operation),
    ct.POINTER(git_rebase),
    ct.c_size_t)(
    ("git_rebase_operation_byindex", dll), (
    (1, "rebase"),
    (1, "idx"),))

# Performs the next rebase operation and returns the information about it.
# If the operation is one that applies a patch (which is any operation except
# GIT_REBASE_OPERATION_EXEC) then the patch will be applied and the index and
# working directory will be updated with the changes.  If there are conflicts,
# you will need to address those before committing the changes.
#
# @param operation Pointer to store the rebase operation that is to be performed next
# @param rebase The rebase in progress
# @return Zero on success; -1 on failure.
#
git_rebase_next = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_rebase_operation)),
    ct.POINTER(git_rebase))(
    ("git_rebase_next", dll), (
    (1, "operation"),
    (1, "rebase"),))

# Gets the index produced by the last operation, which is the result
# of `git_rebase_next` and which will be committed by the next
# invocation of `git_rebase_commit`.  This is useful for resolving
# conflicts in an in-memory rebase before committing them.  You must
# call `git_index_free` when you are finished with this.
#
# This is only applicable for in-memory rebases; for rebases within
# a working directory, the changes were applied to the repository's
# index.
#
# @param index The result index of the last operation.
# @param rebase The in-progress rebase.
# @return 0 or an error code
#
git_rebase_inmemory_index = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index)),
    ct.POINTER(git_rebase))(
    ("git_rebase_inmemory_index", dll), (
    (1, "index"),
    (1, "rebase"),))

# Commits the current patch.  You must have resolved any conflicts that
# were introduced during the patch application from the `git_rebase_next`
# invocation.
#
# @param id Pointer in which to store the OID of the newly created commit
# @param rebase The rebase that is in-progress
# @param author The author of the updated commit, or NULL to keep the
#        author from the original commit
# @param committer The committer of the rebase
# @param message_encoding The encoding for the message in the commit,
#        represented with a standard encoding name.  If message is NULL,
#        this should also be NULL, and the encoding from the original
#        commit will be maintained.  If message is specified, this may be
#        NULL to indicate that "UTF-8" is to be used.
# @param message The message for this commit, or NULL to use the message
#        from the original commit.
# @return Zero on success, GIT_EUNMERGED if there are unmerged changes in
#        the index, GIT_EAPPLIED if the current commit has already
#        been applied to the upstream and there is nothing to commit,
#        -1 on failure.
#
git_rebase_commit = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_rebase),
    ct.POINTER(git_signature),
    ct.POINTER(git_signature),
    ct.c_char_p,
    ct.c_char_p)(
    ("git_rebase_commit", dll), (
    (1, "id"),
    (1, "rebase"),
    (1, "author"),
    (1, "committer"),
    (1, "message_encoding"),
    (1, "message"),))

# Aborts a rebase that is currently in progress, resetting the repository
# and working directory to their state before rebase began.
#
# @param rebase The rebase that is in-progress
# @return Zero on success; GIT_ENOTFOUND if a rebase is not in progress,
#         -1 on other errors.
#
git_rebase_abort = CFUNC(ct.c_int,
    ct.POINTER(git_rebase))(
    ("git_rebase_abort", dll), (
    (1, "rebase"),))

# Finishes a rebase that is currently in progress once all patches have
# been applied.
#
# @param rebase The rebase that is in-progress
# @param signature The identity that is finishing the rebase (optional)
# @return Zero on success; -1 on error
#
git_rebase_finish = CFUNC(ct.c_int,
    ct.POINTER(git_rebase),
    ct.POINTER(git_signature))(
    ("git_rebase_finish", dll), (
    (1, "rebase"),
    (1, "signature"),))

# Frees the `git_rebase` object.
#
# @param rebase The rebase object
#
git_rebase_free = CFUNC(None,
    ct.POINTER(git_rebase))(
    ("git_rebase_free", dll), (
    (1, "rebase"),))

# GIT_END_DECL
