# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .types    import git_repository
from .types    import git_remote
from .checkout import git_checkout_options
from .remote   import git_fetch_options

# @file git2/clone.h
# @brief Git cloning routines
# @defgroup git_clone Git cloning routines
# @ingroup Git

# GIT_BEGIN_DECL

# Options for bypassing the git-aware transport on clone. Bypassing
# it means that instead of a fetch, libgit2 will copy the object
# database directory instead of figuring out what it needs, which is
# faster. If possible, it will hardlink the files to save space.
#
git_clone_local_t = ct.c_int
(
    # Auto-detect (default), libgit2 will bypass the git-aware
    # transport for local paths, but use a normal fetch for
    # `file://` urls.
    GIT_CLONE_LOCAL_AUTO,

    # Bypass the git-aware transport even for a `file://` url.
    GIT_CLONE_LOCAL,

    # Do no bypass the git-aware transport
    GIT_CLONE_NO_LOCAL,

    # Bypass the git-aware transport, but do not try to use
    # hardlinks.
    GIT_CLONE_LOCAL_NO_LINKS,

) = range(0, 4)

# The signature of a function matching git_remote_create, with an additional
# void* as a callback payload.
#
# Callers of git_clone may provide a function matching this signature to override
# the remote creation and customization process during a clone operation.
#
# @param out the resulting remote
# @param repo the repository in which to create the remote
# @param name the remote's name
# @param url the remote's url
# @param payload an opaque payload
# @return 0, GIT_EINVALIDSPEC, GIT_EEXISTS or an error code
#
git_remote_create_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(ct.POINTER(git_remote)),  # out
    ct.POINTER(git_repository),          # repo
    ct.c_char_p,                         # name
    ct.c_char_p,                         # url
    ct.c_void_p)                         # payload

# The signature of a function matching git_repository_init, with an
# additional ct.c_void_p  as callback payload.
#
# Callers of git_clone my provide a function matching this signature
# to override the repository creation and customization process
# during a clone operation.
#
# @param out the resulting repository
# @param path path in which to create the repository
# @param bare whether the repository is bare. This is the value from the clone options
# @param payload payload specified by the options
# @return 0, or a negative value to indicate error
#
git_repository_create_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(ct.POINTER(git_repository)),  # out
    ct.c_char_p,                             # path
    ct.c_int,                                # bare
    ct.c_void_p)                             # payload

# Clone options structure
#
# Initialize with `GIT_CLONE_OPTIONS_INIT`.
# Alternatively, you can use `git_clone_options_init`.
#
class git_clone_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # These options are passed to the checkout step. To disable
    # checkout, set the `checkout_strategy` to
    # `GIT_CHECKOUT_NONE`.
    #
    ("checkout_opts", git_checkout_options),

    # Options which control the fetch, including callbacks.
    #
    # The callbacks are used for reporting fetch progress, and for acquiring
    # credentials in the event they are needed.
    #
    ("fetch_opts", git_fetch_options),

    # Set to zero (false) to create a standard repo, or non-zero
    # for a bare repo
    #
    ("bare", ct.c_int),

    # Whether to use a fetch or copy the object database.
    #
    ("local", git_clone_local_t),

    # The name of the branch to checkout. NULL means use the
    # remote's default branch.
    #
    ("checkout_branch", ct.c_char_p),

    # A callback used to create the new repository into which to
    # clone. If NULL, the 'bare' field will be used to determine
    # whether to create a bare repository.
    #
    ("repository_cb", git_repository_create_cb),

    # An opaque payload to pass to the git_repository creation callback.
    # This parameter is ignored unless repository_cb is non-NULL.
    #
    ("repository_cb_payload", ct.c_void_p),

    # A callback used to create the git_remote, prior to its being
    # used to perform the clone operation. See the documentation for
    # git_remote_create_cb for details. This parameter may be NULL,
    # indicating that git_clone should provide default behavior.
    #
    ("remote_cb", git_remote_create_cb),

    # An opaque payload to pass to the git_remote creation callback.
    # This parameter is ignored unless remote_cb is non-NULL.
    #
    ("remote_cb_payload", ct.c_void_p),
]

GIT_CLONE_OPTIONS_VERSION = 1
#define GIT_CLONE_OPTIONS_INIT = { GIT_CLONE_OPTIONS_VERSION,
#                                  { GIT_CHECKOUT_OPTIONS_VERSION,
#                                    GIT_CHECKOUT_SAFE },
#                                  GIT_FETCH_OPTIONS_INIT }

# Initialize git_clone_options structure
#
# Initializes a `git_clone_options` with default values. Equivalent to creating
# an instance with GIT_CLONE_OPTIONS_INIT.
#
# @param opts The `git_clone_options` struct to initialize.
# @param version The struct version; pass `GIT_CLONE_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_clone_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_clone_options),
    ct.c_uint)(
    ("git_clone_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Clone a remote repository.
#
# By default this creates its repository and initial remote to match
# git's defaults. You can use the options in the callback to
# customize how these are created.
#
# @param out pointer that will receive the resulting repository object
# @param url the remote repository to clone
# @param local_path local directory to clone to
# @param options configuration options for the clone.  If NULL, the
#        function works as though GIT_OPTIONS_INIT were passed.
# @return 0 on success, any non-zero return value from a callback
#         function, or a negative value to indicate an error (use
#         `git_error_last` for a detailed error message)
#
git_clone = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_repository)),
    ct.c_char_p,
    ct.c_char_p,
    ct.POINTER(git_clone_options))(
    ("git_clone", dll), (
    (1, "out"),
    (1, "url"),
    (1, "local_path"),
    (1, "options"),))

# GIT_END_DECL
