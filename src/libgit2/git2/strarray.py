# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa

# @file git2/strarray.h
# @brief Git string array routines
# @defgroup git_strarray Git string array routines
# @ingroup Git

# GIT_BEGIN_DECL

# Array of strings
class git_strarray(ct.Structure):
    _fields_ = [
    ("strings", ct.POINTER(ct.c_char_p)),
    ("count",   ct.c_size_t),
]

# Free the strings contained in a string array.  This method should
# be called on `git_strarray` objects that were provided by the
# library.  Not doing so, will result in a memory leak.
#
# This does not free the `git_strarray` itself, since the library will
# never allocate that object directly itself.
#
# @param array The git_strarray that contains strings to free

git_strarray_dispose = CFUNC(None,
    ct.POINTER(git_strarray))(
    ("git_strarray_dispose", dll), (
    (1, "array"),))

# GIT_END_DECL
