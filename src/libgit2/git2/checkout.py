# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .strarray import git_strarray
from .types    import git_object
from .types    import git_repository
from .types    import git_index
from .types    import git_tree
from .diff     import git_diff_file

# @file git2/checkout.h
# @brief Git checkout routines
# @defgroup git_checkout Git checkout routines
# @ingroup Git

# GIT_BEGIN_DECL

# Checkout behavior flags
#
# In libgit2, checkout is used to update the working directory and index
# to match a target tree.  Unlike git checkout, it does not move the HEAD
# commit for you - use `git_repository_set_head` or the like to do that.
#
# Checkout looks at (up to) four things: the "target" tree you want to
# check out, the "baseline" tree of what was checked out previously, the
# working directory for actual files, and the index for staged changes.
#
# You give checkout one of three strategies for update:
#
# - `GIT_CHECKOUT_NONE` is a dry-run strategy that checks for conflicts,
#   etc., but doesn't make any actual changes.
#
# - `GIT_CHECKOUT_FORCE` is at the opposite extreme, taking any action to
#   make the working directory match the target (including potentially
#   discarding modified files).
#
# - `GIT_CHECKOUT_SAFE` is between these two options, it will only make
#   modifications that will not lose changes.
#
#                         |  target == baseline   |  target != baseline  |
#    ---------------------|-----------------------|----------------------|
#     workdir == baseline |       no action       |  create, update, or  |
#                         |                       |     delete file      |
#    ---------------------|-----------------------|----------------------|
#     workdir exists and  |       no action       |   conflict (notify   |
#       is != baseline    | notify dirty MODIFIED | and cancel checkout) |
#    ---------------------|-----------------------|----------------------|
#      workdir missing,   | notify dirty DELETED  |     create file      |
#      baseline present   |                       |                      |
#    ---------------------|-----------------------|----------------------|
#
# To emulate `git checkout`, use `GIT_CHECKOUT_SAFE` with a checkout
# notification callback (see below) that displays information about dirty
# files.  The default behavior will cancel checkout on conflicts.
#
# To emulate `git checkout-index`, use `GIT_CHECKOUT_SAFE` with a
# notification callback that cancels the operation if a dirty-but-existing
# file is found in the working directory.  This core git command isn't
# quite "force" but is sensitive about some types of changes.
#
# To emulate `git checkout -f`, use `GIT_CHECKOUT_FORCE`.
#
#
# There are some additional flags to modify the behavior of checkout:
#
# - GIT_CHECKOUT_ALLOW_CONFLICTS makes SAFE mode apply safe file updates
#   even if there are conflicts (instead of cancelling the checkout).
#
# - GIT_CHECKOUT_REMOVE_UNTRACKED means remove untracked files (i.e. not
#   in target, baseline, or index, and not ignored) from the working dir.
#
# - GIT_CHECKOUT_REMOVE_IGNORED means remove ignored files (that are also
#   untracked) from the working directory as well.
#
# - GIT_CHECKOUT_UPDATE_ONLY means to only update the content of files that
#   already exist.  Files will not be created nor deleted.  This just skips
#   applying adds, deletes, and typechanges.
#
# - GIT_CHECKOUT_DONT_UPDATE_INDEX prevents checkout from writing the
#   updated files' information to the index.
#
# - Normally, checkout will reload the index and git attributes from disk
#   before any operations.  GIT_CHECKOUT_NO_REFRESH prevents this reload.
#
# - Unmerged index entries are conflicts.  GIT_CHECKOUT_SKIP_UNMERGED skips
#   files with unmerged index entries instead.  GIT_CHECKOUT_USE_OURS and
#   GIT_CHECKOUT_USE_THEIRS to proceed with the checkout using either the
#   stage 2 ("ours") or stage 3 ("theirs") version of files in the index.
#
# - GIT_CHECKOUT_DONT_OVERWRITE_IGNORED prevents ignored files from being
#   overwritten.  Normally, files that are ignored in the working directory
#   are not considered "precious" and may be overwritten if the checkout
#   target contains that file.
#
# - GIT_CHECKOUT_DONT_REMOVE_EXISTING prevents checkout from removing
#   files or folders that fold to the same name on case insensitive
#   filesystems.  This can cause files to retain their existing names
#   and write through existing symbolic links.
#
git_checkout_strategy_t = ct.c_int
(
    GIT_CHECKOUT_NONE,  # default is a dry run, no actual updates

    # Allow safe updates that cannot overwrite uncommitted data.
    # If the uncommitted changes don't conflict with the checked out files,
    # the checkout will still proceed, leaving the changes intact.
    #
    # Mutually exclusive with GIT_CHECKOUT_FORCE.
    # GIT_CHECKOUT_FORCE takes precedence over GIT_CHECKOUT_SAFE.
    #
    GIT_CHECKOUT_SAFE,

    # Allow all updates to force working directory to look like index.
    #
    # Mutually exclusive with GIT_CHECKOUT_SAFE.
    # GIT_CHECKOUT_FORCE takes precedence over GIT_CHECKOUT_SAFE.
    #
    GIT_CHECKOUT_FORCE,

    # Allow checkout to recreate missing files
    GIT_CHECKOUT_RECREATE_MISSING,

    # Allow checkout to make safe updates even if conflicts are found
    GIT_CHECKOUT_ALLOW_CONFLICTS,

    # Remove untracked files not in index (that are not ignored)
    GIT_CHECKOUT_REMOVE_UNTRACKED,

    # Remove ignored files not in index
    GIT_CHECKOUT_REMOVE_IGNORED,

    # Only update existing files, don't create new ones
    GIT_CHECKOUT_UPDATE_ONLY,

    # Normally checkout updates index entries as it goes; this stops that.
    # Implies `GIT_CHECKOUT_DONT_WRITE_INDEX`.
    #
    GIT_CHECKOUT_DONT_UPDATE_INDEX,

    # Don't refresh index/config/etc before doing checkout
    GIT_CHECKOUT_NO_REFRESH,

    # Allow checkout to skip unmerged files
    GIT_CHECKOUT_SKIP_UNMERGED,
    # For unmerged files, checkout stage 2 from index
    GIT_CHECKOUT_USE_OURS,
    # For unmerged files, checkout stage 3 from index
    GIT_CHECKOUT_USE_THEIRS,

    # Treat pathspec as simple list of exact match file paths
    GIT_CHECKOUT_DISABLE_PATHSPEC_MATCH,

    # Ignore directories in use, they will be left empty
    GIT_CHECKOUT_SKIP_LOCKED_DIRECTORIES,

    # Don't overwrite ignored files that exist in the checkout target
    GIT_CHECKOUT_DONT_OVERWRITE_IGNORED,

    # Write normal merge files for conflicts
    GIT_CHECKOUT_CONFLICT_STYLE_MERGE,

    # Include common ancestor data in diff3 format files for conflicts
    GIT_CHECKOUT_CONFLICT_STYLE_DIFF3,

    # Don't overwrite existing files or folders
    GIT_CHECKOUT_DONT_REMOVE_EXISTING,

    # Normally checkout writes the index upon completion; this prevents that.
    GIT_CHECKOUT_DONT_WRITE_INDEX,

    # Show what would be done by a checkout.  Stop after sending
    # notifications; don't update the working directory or index.
    #
    GIT_CHECKOUT_DRY_RUN,

    # Include common ancestor data in zdiff3 format for conflicts
    GIT_CHECKOUT_CONFLICT_STYLE_ZDIFF3,

    # THE FOLLOWING OPTIONS ARE NOT YET IMPLEMENTED
    #

    # Recursively checkout submodules with same options (NOT IMPLEMENTED)
    GIT_CHECKOUT_UPDATE_SUBMODULES ,
    # Recursively checkout submodules if HEAD moved in super repo (NOT IMPLEMENTED)
    GIT_CHECKOUT_UPDATE_SUBMODULES_IF_CHANGED,

) = (0,       1 << 0,  1 << 1,  1 << 2,  1 << 4,  1 << 5,  1 << 6,  1 << 7,
     1 << 8,  1 << 9,  1 << 10, 1 << 11, 1 << 12, 1 << 13, 1 << 18, 1 << 19,
     1 << 20, 1 << 21, 1 << 22, 1 << 23, 1 << 24, 1 << 25,
     1 << 16, 1 << 17)

# Checkout notification flags
#
# Checkout will invoke an options notification callback (`notify_cb`) for
# certain cases - you pick which ones via `notify_flags`:
#
# Returning a non-zero value from this callback will cancel the checkout.
# The non-zero return value will be propagated back and returned by the
# git_checkout_... call.
#
# Notification callbacks are made prior to modifying any files on disk,
# so canceling on any notification will still happen prior to any files
# being modified.
#
git_checkout_notify_t = ct.c_int
(
    GIT_CHECKOUT_NOTIFY_NONE,

    # Invokes checkout on conflicting paths.
    #
    GIT_CHECKOUT_NOTIFY_CONFLICT,

    # Notifies about "dirty" files, i.e. those that do not need an update
    # but no longer match the baseline.  Core git displays these files when
    # checkout runs, but won't stop the checkout.
    #
    GIT_CHECKOUT_NOTIFY_DIRTY,

    # Sends notification for any file changed.
    #
    GIT_CHECKOUT_NOTIFY_UPDATED,

    # Notifies about untracked files.
    #
    GIT_CHECKOUT_NOTIFY_UNTRACKED,

    # Notifies about ignored files.
    #
    GIT_CHECKOUT_NOTIFY_IGNORED,

    GIT_CHECKOUT_NOTIFY_ALL,

) = (0, 1 << 0, 1 << 1, 1 << 2, 1 << 3, 1 << 4, 0x0FFFF)

# Checkout performance-reporting structure
class git_checkout_perfdata(ct.Structure):
    _fields_ = [
    ("mkdir_calls", ct.c_size_t),
    ("stat_calls",  ct.c_size_t),
    ("chmod_calls", ct.c_size_t),
]

# Checkout notification callback function
git_checkout_notify_cb = GIT_CALLBACK(ct.c_int,
    git_checkout_notify_t,      # why
    ct.c_char_p,                # path
    ct.POINTER(git_diff_file),  # baseline
    ct.POINTER(git_diff_file),  # target
    ct.POINTER(git_diff_file),  # workdir
    ct.c_void_p)                # payload

# Checkout progress notification function
git_checkout_progress_cb = GIT_CALLBACK(None,
    ct.c_char_p,  # path
    ct.c_size_t,  # completed_steps
    ct.c_size_t,  # total_steps
    ct.c_void_p)  # payload

# Checkout perfdata notification function
git_checkout_perfdata_cb = GIT_CALLBACK(None,
    ct.POINTER(git_checkout_perfdata),  # perfdata
    ct.c_void_p)                        # payload

# Checkout options structure
#
# Initialize with `GIT_CHECKOUT_OPTIONS_INIT`. Alternatively, you can
# use `git_checkout_options_init`.
#
#
class git_checkout_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),  # The version

    ("checkout_strategy", ct.c_uint),  # default will be a safe checkout

    ("disable_filters",   ct.c_int),   # don't apply filters like CRLF conversion
    ("dir_mode",          ct.c_uint),  # default is 0755
    ("file_mode",         ct.c_uint),  # default is 0644 or 0755 as dictated by blob
    ("file_open_flags",   ct.c_int),   # default is O_CREAT | O_TRUNC | O_WRONLY

    ("notify_flags",      ct.c_uint),  # see `git_checkout_notify_t` above

    # Optional callback to get notifications on specific file states.
    # @see git_checkout_notify_t
    #
    ("notify_cb", git_checkout_notify_cb),

    # Payload passed to notify_cb
    ("notify_payload", ct.c_void_p),

    # Optional callback to notify the consumer of checkout progress.
    ("progress_cb", git_checkout_progress_cb),

    # Payload passed to progress_cb
    ("progress_payload", ct.c_void_p),

    # A list of wildmatch patterns or paths.
    #
    # By default, all paths are processed. If you pass an array of wildmatch
    # patterns, those will be used to filter which paths should be taken into
    # account.
    #
    # Use GIT_CHECKOUT_DISABLE_PATHSPEC_MATCH to treat as a simple list.
    #
    ("paths", git_strarray),

    # The expected content of the working directory; defaults to HEAD.
    #
    # If the working directory does not match this baseline information,
    # that will produce a checkout conflict.
    #
    ("baseline", ct.POINTER(git_tree)),

    # Like `baseline` above, though expressed as an index.  This
    # option overrides `baseline`.
    #
    ("baseline_index", ct.POINTER(git_index)),

    ("target_directory", ct.c_char_p),  # alternative checkout path to workdir

    ("ancestor_label", ct.c_char_p),    # the name of the common ancestor side of conflicts
    ("our_label",      ct.c_char_p),    # the name of the "our" side of conflicts
    ("their_label",    ct.c_char_p),    # the name of the "their" side of conflicts

    # Optional callback to notify the consumer of performance data.
    ("perfdata_cb", git_checkout_perfdata_cb),

    # Payload passed to perfdata_cb
    ("perfdata_payload", ct.c_void_p),
]

GIT_CHECKOUT_OPTIONS_VERSION = 1
#define GIT_CHECKOUT_OPTIONS_INIT = { GIT_CHECKOUT_OPTIONS_VERSION, GIT_CHECKOUT_SAFE }

# Initialize git_checkout_options structure
#
# Initializes a `git_checkout_options` with default values. Equivalent to creating
# an instance with GIT_CHECKOUT_OPTIONS_INIT.
#
# @param opts The `git_checkout_options` struct to initialize.
# @param version The struct version; pass `GIT_CHECKOUT_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_checkout_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_checkout_options),
    ct.c_uint)(
    ("git_checkout_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Updates files in the index and the working tree to match the content of
# the commit pointed at by HEAD.
#
# Note that this is _not_ the correct mechanism used to switch branches;
# do not change your `HEAD` and then call this method, that would leave
# you with checkout conflicts since your working directory would then
# appear to be dirty.  Instead, checkout the target of the branch and
# then update `HEAD` using `git_repository_set_head` to point to the
# branch you checked out.
#
# @param repo repository to check out (must be non-bare)
# @param opts specifies checkout options (may be NULL)
# @return 0 on success, GIT_EUNBORNBRANCH if HEAD points to a non
#         existing branch, non-zero value returned by `notify_cb`, or
#         other error code < 0 (use git_error_last for error details)
#
git_checkout_head = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_checkout_options))(
    ("git_checkout_head", dll), (
    (1, "repo"),
    (1, "opts"),))

# Updates files in the working tree to match the content of the index.
#
# @param repo repository into which to check out (must be non-bare)
# @param index index to be checked out (or NULL to use repository index)
# @param opts specifies checkout options (may be NULL)
# @return 0 on success, non-zero return value from `notify_cb`, or error
#         code < 0 (use git_error_last for error details)
#
git_checkout_index = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_index),
    ct.POINTER(git_checkout_options))(
    ("git_checkout_index", dll), (
    (1, "repo"),
    (1, "index"),
    (1, "opts"),))

# Updates files in the index and working tree to match the content of the
# tree pointed at by the treeish.
#
# @param repo repository to check out (must be non-bare)
# @param treeish a commit, tag or tree which content will be used to update
# the working directory (or NULL to use HEAD)
# @param opts specifies checkout options (may be NULL)
# @return 0 on success, non-zero return value from `notify_cb`, or error
#         code < 0 (use git_error_last for error details)
#
git_checkout_tree = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_object),
    ct.POINTER(git_checkout_options))(
    ("git_checkout_tree", dll), (
    (1, "repo"),
    (1, "treeish"),
    (1, "opts"),))

# GIT_END_DECL
