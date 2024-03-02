# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .types  import git_transport
from .types  import git_remote

# @file git2/transport.h
# @brief Git transport interfaces and functions
# @defgroup git_transport interfaces and functions
# @ingroup Git

# GIT_BEGIN_DECL

# Callback for messages received by the transport.
#
# Return a negative value to cancel the network operation.
#
# @param str The message from the transport
# @param len The length of the message
# @param payload Payload provided by the caller
#
git_transport_message_cb = GIT_CALLBACK(ct.c_int,
    git_buffer_t, # str,
    ct.c_int,     # len,
    ct.c_void_p)  # payload

# Signature of a function which creates a transport
#
git_transport_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(ct.POINTER(git_transport)),  # out,
    ct.POINTER(git_remote),  # owner,
    ct.c_void_p)             # param

# GIT_END_DECL
