# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common     import *  # noqa
from .credential import git_credential_acquire_cb
from .cert       import git_transport_certificate_check_cb

# GIT_BEGIN_DECL

# The type of proxy to use.
#
git_proxy_t = ct.c_int
(   # Do not attempt to connect through a proxy
    #
    # If built against libcurl, it itself may attempt to connect
    # to a proxy if the environment variables specify it.
    #
    GIT_PROXY_NONE,
    # Try to auto-detect the proxy from the git configuration.
    #
    GIT_PROXY_AUTO,
    # Connect via the URL given in the options
    #
    GIT_PROXY_SPECIFIED,
) = range(0, 3)

# Options for connecting through a proxy
#
# Note that not all types may be supported, depending on the platform
# and compilation options.
#
class git_proxy_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # The type of proxy to use, by URL, auto-detect.
    #
    ("type", git_proxy_t),

    # The URL of the proxy.
    #
    ("url", ct.c_char_p),

    # This will be called if the remote host requires
    # authentication in order to connect to it.
    #
    # Returning GIT_PASSTHROUGH will make libgit2 behave as
    # though this field isn't set.
    #
    ("credentials", git_credential_acquire_cb),

    # If cert verification fails, this will be called to let the
    # user make the final decision of whether to allow the
    # connection to proceed. Returns 0 to allow the connection
    # or a negative value to indicate an error.
    #
    ("certificate_check", git_transport_certificate_check_cb),

    # Payload to be provided to the credentials and certificate
    # check callbacks.
    #
    ("payload", ct.c_void_p),
]

GIT_PROXY_OPTIONS_VERSION = 1
#define GIT_PROXY_OPTIONS_INIT = {GIT_PROXY_OPTIONS_VERSION}

# Initialize git_proxy_options structure
#
# Initializes a `git_proxy_options` with default values. Equivalent to
# creating an instance with `GIT_PROXY_OPTIONS_INIT`.
#
# @param opts The `git_proxy_options` struct to initialize.
# @param version The struct version; pass `GIT_PROXY_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_proxy_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_proxy_options),
    ct.c_uint)(
    ("git_proxy_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# GIT_END_DECL
