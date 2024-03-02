# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..types  import git_reflog_entry

# GIT_BEGIN_DECL

git_reflog_entry__alloc = CFUNC(ct.POINTER(git_reflog_entry))(
    ("git_reflog_entry__alloc", dll),)

git_reflog_entry__free = CFUNC(None,
    ct.POINTER(git_reflog_entry))(
    ("git_reflog_entry__free", dll), (
    (1, "entry"),))

# GIT_END_DECL
