# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .buffer import git_buf
from .net    import git_direction
from .types  import git_refspec

# @file git2/refspec.h
# @brief Git refspec attributes
# @defgroup git_refspec Git refspec attributes
# @ingroup Git

# GIT_BEGIN_DECL

# Parse a given refspec string
#
# @param refspec a pointer to hold the refspec handle
# @param input the refspec string
# @param is_fetch is this a refspec for a fetch
# @return 0 if the refspec string could be parsed, -1 otherwise
#
git_refspec_parse = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_refspec)),
    ct.c_char_p,
    ct.c_int)(
    ("git_refspec_parse", dll), (
    (1, "refspec"),
    (1, "input"),
    (1, "is_fetch"),))

# Free a refspec object which has been created by git_refspec_parse
#
# @param refspec the refspec object
#
git_refspec_free = CFUNC(None,
    ct.POINTER(git_refspec))(
    ("git_refspec_free", dll), (
    (1, "refspec"),))

# Get the source specifier
#
# @param refspec the refspec
# @return the refspec's source specifier
#
git_refspec_src = CFUNC(ct.c_char_p,
    ct.POINTER(git_refspec))(
    ("git_refspec_src", dll), (
    (1, "refspec"),))

# Get the destination specifier
#
# @param refspec the refspec
# @return the refspec's destination specifier
#
git_refspec_dst = CFUNC(ct.c_char_p,
    ct.POINTER(git_refspec))(
    ("git_refspec_dst", dll), (
    (1, "refspec"),))

# Get the refspec's string
#
# @param refspec the refspec
# @returns the refspec's original string
#
git_refspec_string = CFUNC(ct.c_char_p,
    ct.POINTER(git_refspec))(
    ("git_refspec_string", dll), (
    (1, "refspec"),))

# Get the force update setting
#
# @param refspec the refspec
# @return 1 if force update has been set, 0 otherwise
#
git_refspec_force = CFUNC(ct.c_int,
    ct.POINTER(git_refspec))(
    ("git_refspec_force", dll), (
    (1, "refspec"),))

# Get the refspec's direction.
#
# @param spec refspec
# @return GIT_DIRECTION_FETCH or GIT_DIRECTION_PUSH
#
git_refspec_direction = CFUNC(git_direction,
    ct.POINTER(git_refspec))(
    ("git_refspec_direction", dll), (
    (1, "spec"),))

# Check if a refspec's source descriptor matches a reference
#
# @param refspec the refspec
# @param refname the name of the reference to check
# @return 1 if the refspec matches, 0 otherwise
#
git_refspec_src_matches = CFUNC(ct.c_int,
    ct.POINTER(git_refspec),
    ct.c_char_p)(
    ("git_refspec_src_matches", dll), (
    (1, "refspec"),
    (1, "refname"),))

# Check if a refspec's destination descriptor matches a reference
#
# @param refspec the refspec
# @param refname the name of the reference to check
# @return 1 if the refspec matches, 0 otherwise
#
git_refspec_dst_matches = CFUNC(ct.c_int,
    ct.POINTER(git_refspec),
    ct.c_char_p)(
    ("git_refspec_dst_matches", dll), (
    (1, "refspec"),
    (1, "refname"),))

# Transform a reference to its target following the refspec's rules
#
# @param out where to store the target name
# @param spec the refspec
# @param name the name of the reference to transform
# @return 0, GIT_EBUFS or another error
#
git_refspec_transform = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_refspec),
    ct.c_char_p)(
    ("git_refspec_transform", dll), (
    (1, "out"),
    (1, "spec"),
    (1, "name"),))

# Transform a target reference to its source reference following the refspec's rules
#
# @param out where to store the source reference name
# @param spec the refspec
# @param name the name of the reference to transform
# @return 0, GIT_EBUFS or another error
#
git_refspec_rtransform = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_refspec),
    ct.c_char_p)(
    ("git_refspec_rtransform", dll), (
    (1, "out"),
    (1, "spec"),
    (1, "name"),))

# GIT_END_DECL
