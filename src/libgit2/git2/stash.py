# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .oid      import git_oid
from .strarray import git_strarray
from .types    import git_signature
from .types    import git_repository
from .checkout import git_checkout_options

# @file git2/stash.h
# @brief Git stash management routines
# @ingroup Git

# GIT_BEGIN_DECL

# Stash flags
#
git_stash_flags = ct.c_int
(
    # No option, default
    #
    GIT_STASH_DEFAULT,

    # All changes already added to the index are left intact in
    # the working directory
    #
    GIT_STASH_KEEP_INDEX,

    # All untracked files are also stashed and then cleaned up
    # from the working directory
    #
    GIT_STASH_INCLUDE_UNTRACKED,

    # All ignored files are also stashed and then cleaned up from
    # the working directory
    #
    GIT_STASH_INCLUDE_IGNORED,

    # All changes in the index and working directory are left intact
    #
    GIT_STASH_KEEP_ALL,

) = (0, 1 << 0, 1 << 1, 1 << 2, 1 << 3)

# Save the local modifications to a new stash.
#
# @param out Object id of the commit containing the stashed state.
# This commit is also the target of the direct reference refs/stash.
# @param repo The owning repository.
# @param stasher The identity of the person performing the stashing.
# @param message Optional description along with the stashed state.
# @param flags Flags to control the stashing process. (see GIT_STASH_* above)
# @return 0 on success, GIT_ENOTFOUND where there's nothing to stash,
# or error code.
#
git_stash_save = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.POINTER(git_signature),
    ct.c_char_p,
    ct.c_uint32)(
    ("git_stash_save", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "stasher"),
    (1, "message"),
    (1, "flags"),))

# Stash save options structure
#
# Initialize with `GIT_STASH_SAVE_OPTIONS_INIT`. Alternatively, you can
# use `git_stash_save_options_init`.
#
class git_stash_save_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # Flags to control the stashing process. (see GIT_STASH_* above)
    ("flags", ct.c_uint32),

    # The identity of the person performing the stashing.
    ("stasher", ct.POINTER(git_signature)),

    # Optional description along with the stashed state.
    ("message", ct.c_char_p),

    # Optional paths that control which files are stashed.
    ("paths", git_strarray),
]

GIT_STASH_SAVE_OPTIONS_VERSION = 1
#define GIT_STASH_SAVE_OPTIONS_INIT = { GIT_STASH_SAVE_OPTIONS_VERSION }

# Initialize git_stash_save_options structure
#
# Initializes a `git_stash_save_options` with default values. Equivalent to
# creating an instance with `GIT_STASH_SAVE_OPTIONS_INIT`.
#
# @param opts The `git_stash_save_options` struct to initialize.
# @param version The struct version; pass `GIT_STASH_SAVE_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_stash_save_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_stash_save_options),
    ct.c_uint)(
    ("git_stash_save_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Save the local modifications to a new stash, with options.
#
# @param out Object id of the commit containing the stashed state.
# This commit is also the target of the direct reference refs/stash.
# @param repo The owning repository.
# @param opts The stash options.
# @return 0 on success, GIT_ENOTFOUND where there's nothing to stash,
# or error code.
#
git_stash_save_with_opts = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.POINTER(git_stash_save_options))(
    ("git_stash_save_with_opts", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "opts"),))

# Stash application flags.
git_stash_apply_flags = ct.c_int
(
    GIT_STASH_APPLY_DEFAULT,

    # Try to reinstate not only the working tree's changes,
    # but also the index's changes.
    #
    GIT_STASH_APPLY_REINSTATE_INDEX,

) = (0, 1 << 0)

# Stash apply progression states
git_stash_apply_progress_t = ct.c_int
(
    GIT_STASH_APPLY_PROGRESS_NONE,

    # Loading the stashed data from the object database.
    GIT_STASH_APPLY_PROGRESS_LOADING_STASH,

    # The stored index is being analyzed.
    GIT_STASH_APPLY_PROGRESS_ANALYZE_INDEX,

    # The modified files are being analyzed.
    GIT_STASH_APPLY_PROGRESS_ANALYZE_MODIFIED,

    # The untracked and ignored files are being analyzed.
    GIT_STASH_APPLY_PROGRESS_ANALYZE_UNTRACKED,

    # The untracked files are being written to disk.
    GIT_STASH_APPLY_PROGRESS_CHECKOUT_UNTRACKED,

    # The modified files are being written to disk.
    GIT_STASH_APPLY_PROGRESS_CHECKOUT_MODIFIED,

    # The stash was applied successfully.
    GIT_STASH_APPLY_PROGRESS_DONE,

) = range(0, 8)

# Stash application progress notification function.
# Return 0 to continue processing, or a negative value to
# abort the stash application.
#
git_stash_apply_progress_cb = GIT_CALLBACK(ct.c_int,
    git_stash_apply_progress_t,  # progress
    ct.c_void_p)                 # payload

# Stash application options structure
#
# Initialize with `GIT_STASH_APPLY_OPTIONS_INIT`. Alternatively, you can
# use `git_stash_apply_options_init`.
#
class git_stash_apply_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # See `git_stash_apply_flags`, above.
    ("flags", ct.c_uint32),

    # Options to use when writing files to the working directory.
    ("checkout_options", git_checkout_options),

    # Optional callback to notify the consumer of application progress.
    ("progress_cb", git_stash_apply_progress_cb),

    ("progress_payload", ct.c_void_p),
]

GIT_STASH_APPLY_OPTIONS_VERSION = 1
#define GIT_STASH_APPLY_OPTIONS_INIT = { GIT_STASH_APPLY_OPTIONS_VERSION,
#                                        GIT_STASH_APPLY_DEFAULT,
#                                        GIT_CHECKOUT_OPTIONS_INIT }

# Initialize git_stash_apply_options structure
#
# Initializes a `git_stash_apply_options` with default values. Equivalent to
# creating an instance with `GIT_STASH_APPLY_OPTIONS_INIT`.
#
# @param opts The `git_stash_apply_options` struct to initialize.
# @param version The struct version; pass `GIT_STASH_APPLY_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_stash_apply_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_stash_apply_options),
    ct.c_uint)(
    ("git_stash_apply_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Apply a single stashed state from the stash list.
#
# If local changes in the working directory conflict with changes in the
# stash then GIT_EMERGECONFLICT will be returned.  In this case, the index
# will always remain unmodified and all files in the working directory will
# remain unmodified.  However, if you are restoring untracked files or
# ignored files and there is a conflict when applying the modified files,
# then those files will remain in the working directory.
#
# If passing the GIT_STASH_APPLY_REINSTATE_INDEX flag and there would be
# conflicts when reinstating the index, the function will return
# GIT_EMERGECONFLICT and both the working directory and index will be left
# unmodified.
#
# Note that a minimum checkout strategy of `GIT_CHECKOUT_SAFE` is implied.
#
# @param repo The owning repository.
# @param index The position within the stash list. 0 points to the
#              most recent stashed state.
# @param options Optional options to control how stashes are applied.
#
# @return 0 on success, GIT_ENOTFOUND if there's no stashed state for the
#         given index, GIT_EMERGECONFLICT if changes exist in the working
#         directory, or an error code
#
git_stash_apply = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_size_t,
    ct.POINTER(git_stash_apply_options))(
    ("git_stash_apply", dll), (
    (1, "repo"),
    (1, "index"),
    (1, "options"),))

# This is a callback function you can provide to iterate over all the
# stashed states that will be invoked per entry.
#
# @param index The position within the stash list. 0 points to the
#              most recent stashed state.
# @param message The stash message.
# @param stash_id The commit oid of the stashed state.
# @param payload Extra parameter to callback function.
# @return 0 to continue iterating or non-zero to stop.
#
git_stash_cb = GIT_CALLBACK(ct.c_int,
    ct.c_size_t,          # index
    ct.c_char_p,          # message
    ct.POINTER(git_oid),  # stash_id
    ct.c_void_p)          # payload

# Loop over all the stashed states and issue a callback for each one.
#
# If the callback returns a non-zero value, this will stop looping.
#
# @param repo Repository where to find the stash.
#
# @param callback Callback to invoke per found stashed state. The most
#                 recent stash state will be enumerated first.
#
# @param payload Extra parameter to callback function.
#
# @return 0 on success, non-zero callback return value, or error code.
#
git_stash_foreach = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    git_stash_cb,
    ct.c_void_p)(
    ("git_stash_foreach", dll), (
    (1, "repo"),
    (1, "callback"),
    (1, "payload"),))

# Remove a single stashed state from the stash list.
#
# @param repo The owning repository.
#
# @param index The position within the stash list. 0 points to the
# most recent stashed state.
#
# @return 0 on success, GIT_ENOTFOUND if there's no stashed state for the given
# index, or error code.
#
git_stash_drop = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_size_t)(
    ("git_stash_drop", dll), (
    (1, "repo"),
    (1, "index"),))

# Apply a single stashed state from the stash list and remove it from the list
# if successful.
#
# @param repo The owning repository.
# @param index The position within the stash list. 0 points to the
#              most recent stashed state.
# @param options Optional options to control how stashes are applied.
#
# @return 0 on success, GIT_ENOTFOUND if there's no stashed state for the given
# index, or error code. (see git_stash_apply() above for details)
#
git_stash_pop = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_size_t,
    ct.POINTER(git_stash_apply_options))(
    ("git_stash_pop", dll), (
    (1, "repo"),
    (1, "index"),
    (1, "options"),))

# GIT_END_DECL
