# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .types  import git_refdb
from .types  import git_repository

# @file git2/refdb.h
# @brief Git custom refs backend functions
# @defgroup git_refdb Git custom refs backend API
# @ingroup Git

# GIT_BEGIN_DECL

# Create a new reference database with no backends.
#
# Before the Ref DB can be used for read/writing, a custom database
# backend must be manually set using `git_refdb_set_backend()`
#
# @param out location to store the database pointer, if opened.
#          Set to NULL if the open failed.
# @param repo the repository
# @return 0 or an error code
#
git_refdb_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_refdb)),
    ct.POINTER(git_repository))(
    ("git_refdb_new", dll), (
    (1, "out"),
    (1, "repo"),))

# Create a new reference database and automatically add
# the default backends:
#
#  - git_refdb_dir: read and write loose and packed refs
#      from disk, assuming the repository dir as the folder
#
# @param out location to store the database pointer, if opened.
#          Set to NULL if the open failed.
# @param repo the repository
# @return 0 or an error code
#
git_refdb_open = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_refdb)),
    ct.POINTER(git_repository))(
    ("git_refdb_open", dll), (
    (1, "out"),
    (1, "repo"),))

# Suggests that the given refdb compress or optimize its references.
# This mechanism is implementation specific.  For on-disk reference
# databases, for example, this may pack all loose references.
#
# @param refdb The reference database to optimize.
# @return 0 or an error code.
#
git_refdb_compress = CFUNC(ct.c_int,
    ct.POINTER(git_refdb))(
    ("git_refdb_compress", dll), (
    (1, "refdb"),))

# Close an open reference database.
#
# @param refdb reference database pointer or NULL
#
git_refdb_free = CFUNC(None,
    ct.POINTER(git_refdb))(
    ("git_refdb_free", dll), (
    (1, "refdb"),))

# GIT_END_DECL
