# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid

# @file git2/net.h
# @brief Git networking declarations
# @ingroup Git

# GIT_BEGIN_DECL

GIT_DEFAULT_PORT = b"9418"

# Direction of the connection.
#
# We need this because we need to know whether we should call
# git-upload-pack or git-receive-pack on the remote end when get_refs
# gets called.
#
git_direction = ct.c_int
(   GIT_DIRECTION_FETCH,
    GIT_DIRECTION_PUSH,
) = (0,  1)

# Description of a reference advertised by a remote server, given out
# on `ls` calls.
#
class git_remote_head(ct.Structure):
    _fields_ = [
    ("local", ct.c_int),  # available locally
    ("oid",   git_oid),
    ("loid",  git_oid),
    ("name",  ct.c_char_p),
    # If the server send a symref mapping for this ref, this will
    # point to the target.
    ("symref_target", ct.c_char_p),
]

# GIT_END_DECL
