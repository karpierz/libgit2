# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..types  import git_reference
from ..oid    import git_oid

# @file git2/sys/refs.h
# @brief Low-level Git ref creation
# @defgroup git_backend Git custom backend APIs
# @ingroup Git

# GIT_BEGIN_DECL

# Create a new direct reference from an OID.
#
# @param name the reference name
# @param oid the object id for a direct reference
# @param peel the first non-tag object's OID, or NULL
# @return the created git_reference or NULL on error
#
git_reference__alloc = CFUNC(ct.POINTER(git_reference),
    ct.c_char_p,
    ct.POINTER(git_oid),
    ct.POINTER(git_oid))(
    ("git_reference__alloc", dll), (
    (1, "name"),
    (1, "oid"),
    (1, "peel"),))

# Create a new symbolic reference.
#
# @param name the reference name
# @param target the target for a symbolic reference
# @return the created git_reference or NULL on error
#
git_reference__alloc_symbolic = CFUNC(ct.POINTER(git_reference),
    ct.c_char_p,
    ct.c_char_p)(
    ("git_reference__alloc_symbolic", dll), (
    (1, "name"),
    (1, "target"),))

# GIT_END_DECL
