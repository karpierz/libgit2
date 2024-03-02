# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .types  import git_time_t
from .types  import git_signature
from .types  import git_repository

# @file git2/signature.h
# @brief Git signature creation
# @defgroup git_signature Git signature creation
# @ingroup Git

# GIT_BEGIN_DECL

# Create a new action signature.
#
# Call `git_signature_free()` to free the data.
#
# Note: angle brackets ('<' and '>') characters are not allowed
# to be used in either the `name` or the `email` parameter.
#
# @param out new signature, in case of error NULL
# @param name name of the person
# @param email email of the person
# @param time time (in seconds from epoch) when the action happened
# @param offset timezone offset (in minutes) for the time
# @return 0 or an error code
#
git_signature_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_signature)),
    ct.c_char_p,
    ct.c_char_p,
    git_time_t,
    ct.c_int)(
    ("git_signature_new", dll), (
    (1, "out"),
    (1, "name"),
    (1, "email"),
    (1, "time"),
    (1, "offset"),))

# Create a new action signature with a timestamp of 'now'.
#
# Call `git_signature_free()` to free the data.
#
# @param out new signature, in case of error NULL
# @param name name of the person
# @param email email of the person
# @return 0 or an error code
#
git_signature_now = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_signature)),
    ct.c_char_p,
    ct.c_char_p)(
    ("git_signature_now", dll), (
    (1, "out"),
    (1, "name"),
    (1, "email"),))

# Create a new action signature with default user and now timestamp.
#
# This looks up the user.name and user.email from the configuration and
# uses the current time as the timestamp, and creates a new signature
# based on that information.  It will return GIT_ENOTFOUND if either the
# user.name or user.email are not set.
#
# @param out new signature
# @param repo repository pointer
# @return 0 on success, GIT_ENOTFOUND if config is missing, or error code
#
git_signature_default = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_signature)),
    ct.POINTER(git_repository))(
    ("git_signature_default", dll), (
    (1, "out"),
    (1, "repo"),))

# Create a new signature by parsing the given buffer, which is
# expected to be in the format "Real Name <email> timestamp tzoffset",
# where `timestamp` is the number of seconds since the Unix epoch and
# `tzoffset` is the timezone offset in `hhmm` format (note the lack
# of a colon separator).
#
# @param out new signature
# @param buf signature string
# @return 0 on success, GIT_EINVALID if the signature is not parseable, or an error code
#
git_signature_from_buffer = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_signature)),
    ct.c_char_p)(
    ("git_signature_from_buffer", dll), (
    (1, "out"),
    (1, "buf"),))

# Create a copy of an existing signature.  All internal strings are also
# duplicated.
#
# Call `git_signature_free()` to free the data.
#
# @param dest pointer where to store the copy
# @param sig signature to duplicate
# @return 0 or an error code
#
git_signature_dup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_signature)),
    ct.POINTER(git_signature))(
    ("git_signature_dup", dll), (
    (1, "dest"),
    (1, "sig"),))

# Free an existing signature.
#
# Because the signature is not an opaque structure, it is legal to free it
# manually, but be sure to free the "name" and "email" strings in addition
# to the structure itself.
#
# @param sig signature to free
#
git_signature_free = CFUNC(None,
    ct.POINTER(git_signature))(
    ("git_signature_free", dll), (
    (1, "sig"),))

# GIT_END_DECL
