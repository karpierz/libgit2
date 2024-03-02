# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid

# GIT_BEGIN_DECL

# Array of object ids
class git_oidarray(ct.Structure):
    _fields_ = [
    ("ids",   ct.POINTER(git_oid)),
    ("count", ct.c_size_t),
]

# Free the object IDs contained in an oid_array.  This method should
# be called on `git_oidarray` objects that were provided by the
# library.  Not doing so will result in a memory leak.
#
# This does not free the `git_oidarray` itself, since the library will
# never allocate that object directly itself.
#
# @param array git_oidarray from which to free oid data

git_oidarray_dispose = CFUNC(None,
    ct.POINTER(git_oidarray))(
    ("git_oidarray_dispose", dll), (
    (1, "array"),))

# GIT_END_DECL
